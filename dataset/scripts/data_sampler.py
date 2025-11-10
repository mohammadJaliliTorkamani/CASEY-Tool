import json
import random
import os

# Path to your JSON file
json_file_path = "JSON PATH COMES HERE"

# Helper: get file extension from full path
def get_file_extension(filename):
    ext = os.path.splitext(filename)[1].lower()  # includes dot, e.g. '.py'
    return ext if ext else None

# Load JSON array
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

if not isinstance(data, list):
    raise ValueError("The JSON data must be an array.")

filtered_data = []

for item in data:
    vulnerability = item.get("vulnerability", {})
    file_level = vulnerability.get("file_level", [])
    if not file_level:
        continue

    # Get all file extensions in this item
    exts = {get_file_extension(f.get("name", "")) for f in file_level}

    # Keep only if all extensions are the same and known
    if len(exts) == 1 and None not in exts:
        item["lang"] = exts.pop()
        filtered_data.append(item)

# Randomly sample up to 100 items
sample_size = min(100, len(filtered_data))
sampled_data = random.sample(filtered_data, sample_size)

# Save sampled data
output_file = "JSON PATH COMES HERE"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(sampled_data, f, ensure_ascii=False, indent=4)

print(f"Saved {sample_size} samples to {output_file}")
