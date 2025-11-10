gpt_folders = [
    "PATHS COME HERE"
]

llama_folders = [
    "PATHS COME HERE",
]

import json
import os
from collections import Counter, defaultdict
from typing import List, Dict, Any


def analyze_single_folder(folder_path: str) -> Dict[str, Any]:
    # Store statistics grouped by comparison type
    stats = defaultdict(lambda: {"ext": [], "cwe": [], "cvss": []})

    if not os.path.isdir(folder_path):
        print(f"⚠️ Skipping invalid folder: {folder_path}")
        return {}

    # Walk through all json files
    for fname in os.listdir(folder_path):
        if not fname.startswith("result_") or not fname.endswith(".json"):
            continue

        fpath = os.path.join(folder_path, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️ Could not read {fpath}: {e}")
            continue

        gt = data.get("gt", {})
        vuln = gt.get("vulnerability", {})
        files = vuln.get("file_level", [])
        cwes = gt.get("cwe", [])
        cvss_score = gt.get("cvss_score")

        # Helper: get file extensions
        extensions = []
        for fl in files:
            name = fl.get("name", "")
            if "." in name:
                extensions.append(name.split(".")[-1])

        # 1. is_vulnerable_comparison
        if data.get("is_vulnerable_comparison") != "IDENTICAL":
            stats["is_vulnerable_comparison"]["ext"].extend(extensions)
            stats["is_vulnerable_comparison"]["cwe"].extend(cwes)
            if isinstance(cvss_score, (int, float)):
                stats["is_vulnerable_comparison"]["cvss"].append(cvss_score)

        # 2. is_security_vulnerable_comparison
        if data.get("is_security_vulnerable_comparison") != "IDENTICAL":
            stats["is_security_vulnerable_comparison"]["ext"].extend(extensions)
            stats["is_security_vulnerable_comparison"]["cwe"].extend(cwes)
            if isinstance(cvss_score, (int, float)):
                stats["is_security_vulnerable_comparison"]["cvss"].append(cvss_score)

        # 3. cwe_comparison
        if data.get("cwe_comparison") != "IDENTICAL":
            stats["cwe_comparison"]["ext"].extend(extensions)
            stats["cwe_comparison"]["cwe"].extend(cwes)
            if isinstance(cvss_score, (int, float)):
                stats["cwe_comparison"]["cvss"].append(cvss_score)

        # 4. severity_comparison
        if data.get("severity_comparison") != "IDENTICAL":
            stats["severity_comparison"]["ext"].extend(extensions)
            stats["severity_comparison"]["cwe"].extend(cwes)
            if isinstance(cvss_score, (int, float)):
                stats["severity_comparison"]["cvss"].append(cvss_score)

        # 5. cvss_score_comparison (check first element of list is not True)
        cvss_cmp = data.get("cvss_score_comparison")
        if isinstance(cvss_cmp, list) and len(cvss_cmp) > 0 and cvss_cmp[0] is not True:
            stats["cvss_score_comparison"]["ext"].extend(extensions)
            stats["cvss_score_comparison"]["cwe"].extend(cwes)
            if isinstance(cvss_score, (int, float)):
                stats["cvss_score_comparison"]["cvss"].append(cvss_score)

    # Prepare final report for this folder
    report = {}
    for key, values in stats.items():
        ext_counter = Counter(values["ext"])
        cwe_counter = Counter(values["cwe"])
        avg_cvss = sum(values["cvss"]) / len(values["cvss"]) if values["cvss"] else None

        report[key] = {
            "top_extensions": [ext for ext, _ in ext_counter.most_common(3)],
            "top_cwes": [cwe for cwe, _ in cwe_counter.most_common(3)],
            "avg_cvss": avg_cvss,
        }

    return report


def analyze_results(folder_paths: List[str]) -> Dict[str, Any]:
    all_reports = {}
    for folder in folder_paths:
        all_reports[folder] = analyze_single_folder(folder)
    return all_reports


if __name__ == "__main__":
    # Example: multiple folders
    result = analyze_results(llama_folders)

    # Save to JSON file
    output_file = "llama_noise_destroyed_analysis.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print(f"✅ Report saved to {output_file}")
