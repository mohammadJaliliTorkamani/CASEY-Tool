import json
import os
import re

import requests

CVE_REGEX = re.compile(r"^CVE-(\d{4})-(\d{4,})$", re.IGNORECASE)
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/CVEProject/cvelistV5/{commit_or_branch}/cves/{year}/{prefix_dir}/{cve}.json"

# Use "main" or a specific commit hash
GITHUB_BRANCH = "main"


def cve_to_github_path(cve_id: str) -> str:
    m = CVE_REGEX.match(cve_id)
    if not m:
        raise ValueError(f"Invalid CVE format: {cve_id}")
    year = m.group(1)
    num = m.group(2)

    prefix = num[:2] if len(num) >= 2 else num.zfill(2)
    prefix_dir = f"{prefix}xxx"

    return GITHUB_RAW_BASE.format(
        commit_or_branch=GITHUB_BRANCH,
        year=year,
        prefix_dir=prefix_dir,
        cve=cve_id.upper()
    )


def fetch_cve_from_github(cve_id: str, save_dir: str = "cvelist_json") -> str:
    url = cve_to_github_path(cve_id)
    os.makedirs(save_dir, exist_ok=True)
    out_path = os.path.join(save_dir, f"{cve_id.upper()}.json")

    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(resp.content)
        print(f"✅ Saved {cve_id} → {out_path}")
        return out_path
    elif resp.status_code == 404:
        print(f"❌ Not found: {cve_id}")
        return None
    else:
        print(f"⚠️ Error fetching {cve_id}: {resp.status_code}")
        return None


def main():
    input_file = "JSON PATH COMES HERE"  # change this to your actual file path

    # Load the JSON array
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load {input_file}: {e}")
        return

    # Expecting array of { "cve": "CVE-xxxx-xxxxx" }
    for item in data:
        cve_id = item.get("cve")
        if not cve_id:
            print(f"Skipping entry without 'cve': {item}")
            continue
        try:
            fetch_cve_from_github(cve_id)
        except Exception as e:
            print(f"Error handling {cve_id}: {e}")


if __name__ == "__main__":
    main()
