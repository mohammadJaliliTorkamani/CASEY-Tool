import json
import os
import shutil
import subprocess
from typing import List, Dict, Any
from urllib.parse import urlparse

from git import Repo

import constants
from extractor import Extractor

# Supported programming languages and their file extensions
SUPPORTED_LANGS = {".c", ".cpp", ".go", ".java", ".js", ".php", ".py", ".rb", ".ts"}

# Path to directory containing pttrhn scripts for each language
METHOD_EXTRACTORS_SCRIPTS_DIR = "../extractors/"


def extract_description(cve_obj: Dict[str, Any]) -> str:
    for desc in cve_obj.get("descriptions", []):
        if desc.get("lang") == "en":
            return desc.get("value")
    return None


def extract_cwes(cve_obj: Dict[str, Any]) -> set[str]:
    cwes = set()
    for weakness in cve_obj.get("weaknesses", []):
        for desc in weakness.get("description", []):
            cwes.add(desc.get("value"))
    return cwes


def extract_cvss(cve_obj: Dict[str, Any]):
    metrics = cve_obj.get("metrics", {})
    # Pick newest CVSS metric (e.g., cvssMetricV30 over cvssMetricV2)
    for key in sorted(metrics.keys(), reverse=True):
        if key.startswith("cvssMetric") and metrics[key]:
            entry = metrics[key][0]
            cvss = entry.get("cvssData", {})
            return (cvss.get("baseSeverity"), cvss.get("baseScore"), cvss.get("version"))
    return None, None, None


def extract_github_patch_links(cve_obj: Dict[str, Any]) -> List[str]:
    urls = []
    for ref in cve_obj.get("references", []):
        tags = ref.get("tags", [])
        url = ref.get("url", "")
        if "Patch" in tags and "github.com" in url and "/commit/" in url:
            urls.append(url)
    return urls


def run_git_command(repo_path: str, args: List[str]) -> str:
    result = subprocess.run(
        ['git', '-C', repo_path] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(args)}\n{result.stderr}")

    return result.stdout


def get_deleted_lines_from_diff(diff_text: str) -> Dict[str, List[Dict[str, Any]]]:
    """Parses the git diff --unified=0 output to extract deleted lines and their line numbers."""
    deleted_lines_by_file = {}
    current_file = None
    current_line_idx = None
    processing_hunk = False

    for line in diff_text.splitlines():
        if line.startswith('diff --git'):
            current_file = None
            processing_hunk = False
        elif line.startswith('--- a/'):
            current_file = line[6:]
        elif line.startswith('@@'):
            if current_file is None:
                continue
            # Format: @@ -start,count +start,count @@
            parts = line.split(' ')
            removed_info = parts[1]  # like '-42,2'
            if ',' in removed_info:
                start_line = int(removed_info[1:].split(',')[0])
            else:
                start_line = int(removed_info[1:])
            current_line_idx = start_line
            deleted_lines_by_file.setdefault(current_file, [])
            processing_hunk = True
        elif processing_hunk:
            if line.startswith('-') and not line.startswith('---'):
                deleted_lines_by_file[current_file].append({
                    "line_no": current_line_idx,
                    "content": line[1:]
                })
                current_line_idx += 1
            elif not line.startswith('+'):
                current_line_idx += 1

    return deleted_lines_by_file


def get_file_content_at_commit(repo_path: str, file_path: str, commit_hash: str) -> str:
    return run_git_command(repo_path, ['show', f'{commit_hash}:{file_path}'])


def get_deleted_lines_grouped_by_method(repo_path: str, commit_hash: str):
    result = []

    # Get the diff of the commit with no context lines (for exact deletions)
    diff_output = run_git_command(repo_path, ['diff', f'{commit_hash}^', commit_hash, '--unified=0'])
    deleted_lines_by_file = get_deleted_lines_from_diff(diff_output)

    for file_path, deleted_lines in deleted_lines_by_file.items():
        if not any(file_path.endswith(ext) for ext in SUPPORTED_LANGS):
            continue

        if len(deleted_lines) == 0:
            continue

        # Get file content before the commit
        pre_commit_content = get_file_content_at_commit(repo_path, file_path, f'{commit_hash}^')

        # Write content to a temp file for method extraction
        _, ext = os.path.splitext(file_path)

        tmp_file_path = "./tmp_file" + ext
        methods = []
        try:
            tmp_file = open(tmp_file_path, "w")
            tmp_file.write(pre_commit_content)
            tmp_file.close()
            methods = extract_methods(tmp_file_path)
        finally:
            os.remove(tmp_file_path)

        method_edits = []

        for method_name, start_line, end_line in methods:
            method_deleted_lines = [
                line for line in deleted_lines
                if start_line <= line["line_no"] <= end_line
            ]
            if method_deleted_lines:
                method_edits.append({
                    "code": method_name,
                    "start_line": start_line,
                    "end_line": end_line,
                    "edited_lines": method_deleted_lines
                })

        if method_edits:
            result.append({
                file_path: {
                    "pre_commit_content": pre_commit_content,
                    "pre_commit_edited_methods": method_edits
                }
            })

    return result


def extract_file_info(repo_dir: str, commit_hash: str):
    _obj = get_deleted_lines_grouped_by_method(repo_dir, commit_hash)
    files = []
    methods = []
    lines = []

    for o in _obj:
        for file_name, file_obj in o.items():
            file_content = file_obj['pre_commit_content']
            files.append({'name': file_name, 'content': file_content})

            methods_content_obj = file_obj['pre_commit_edited_methods']
            for method_obj in methods_content_obj:
                methods.append(method_obj['code'])

                for edited_line_obj in method_obj['edited_lines']:
                    if len(edited_line_obj['content']) > 0:
                        lines.append({'line_no': edited_line_obj['line_no'], 'content': edited_line_obj['content']})

    return files, methods, lines


def extract_methods(file_path: str) -> List[Dict]:
    return Extractor(file_path).extract_methods()


def process_cve_records(file) -> List[Dict[str, Any]]:
    dataset = []
    id_counter = 1

    with open(file, "r") as f:
        root = json.load(f)

    vulnerabilities = root.get("vulnerabilities", [])
    for vul_idx, vuln in enumerate(vulnerabilities):
        print(f"Vul {vul_idx + 1} / {len(vulnerabilities)}")
        cve = vuln.get("cve", {})
        patch_links = extract_github_patch_links(cve)
        if not patch_links:
            continue

        description = extract_description(cve) or None
        cwes = extract_cwes(cve)
        severity, score, version = extract_cvss(cve)

        for link in patch_links:
            parsed = urlparse(link)
            parts = parsed.path.strip("/").split("/")
            if len(parts) < 4 or parts[2] != "commit":
                continue
            owner, repo_name, _, commit_hash = parts[0], parts[1], parts[2], parts[3]
            if owner == "torvalds" or repo_name == "linux":
                continue

            git_url = f"https://github.com/{owner}/{repo_name}.git"
            tmp_root = f"./tmp/{owner}_{repo_name}"
            os.makedirs(tmp_root, exist_ok=True)

            try:
                print(git_url)
                repo = Repo.clone_from(git_url, tmp_root)
                repo.git.checkout(commit_hash)
                modified_files, modified_methods, modified_hunks = extract_file_info(tmp_root, commit_hash)
                if len(modified_files) > 0 and len(modified_methods) > 0 and len(modified_hunks) > 0:
                    dataset.append({
                        "id": id_counter,
                        "cve": cve.get("id"),
                        "description": description,
                        "vulnerability": {
                            "file_level": modified_files,
                            "method_level": modified_methods,
                            "hunk_level": modified_hunks
                        },
                        "cwe": cwes,
                        "severity": severity,
                        "cvss_score": score,
                        "cvss_version": float(version)
                    })
                    print(f"    ===> Found {id_counter} valid items by now!")
                    id_counter += 1
                # break
            except Exception as e:
                print(f"Warning: failed processing {git_url}@{commit_hash} due to {e}")
                continue
            finally:
                shutil.rmtree(tmp_root)

    return dataset


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


if __name__ == "__main__":
    input_json_file = "JSON PATH COMES HERE"

    results = process_cve_records(input_json_file)
    print(f"Found {len(results)} valid vulnerabilities")
    with open(constants.TOTAL_DATASET_PATH, "w") as f_out:
        json.dump(results, f_out, indent=2, default=set_default)

    print(f"Dataset saved to {constants.TOTAL_DATASET_PATH}")
