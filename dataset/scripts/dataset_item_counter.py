import json
import os

# List of JSON file paths
file_paths = [
    "JSON PATH COMES HERE"
]

for path in file_paths:
    try:
        if not os.path.exists(path):
            print(f"⚠ File not found: {path}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            print(f"{path}: {len(data)} items")
        else:
            print(f"{path}: Not a list (type: {type(data).__name__})")

    except Exception as e:
        print(f" Error processing {path}: {e}")
