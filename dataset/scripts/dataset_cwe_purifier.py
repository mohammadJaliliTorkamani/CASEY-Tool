import json
import re
import os

# List of JSON file paths
file_paths = [
    "JSON PATHS COME HERE"
]

# Pattern for valid CWE strings: CWE- followed by digits
cwe_pattern = re.compile(r"^CWE-\d+$")

for path in file_paths:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError(f"File {path} does not contain a list of objects.")

        cleaned_data = []
        for obj in data:
            if isinstance(obj, dict) and "cwe" in obj and isinstance(obj["cwe"], list):
                # Keep only valid CWE strings
                obj["cwe"] = [c for c in obj["cwe"] if isinstance(c, str) and cwe_pattern.match(c)]
                # Add object only if it still has CWEs after cleaning
                if obj["cwe"]:
                    cleaned_data.append(obj)
            else:
                # Skip if 'cwe' key missing or not a list
                continue

        with open(path, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

        # Get file size in KB
        file_size_kb = os.path.getsize(path) / 1024
        print(f"✅ Cleaned and saved: {path} — {file_size_kb:.2f} KB")

    except Exception as e:
        print(f"Error processing {path}: {e}")
