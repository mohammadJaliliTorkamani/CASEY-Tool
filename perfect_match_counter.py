import json
import os

# Two directory paths
dir1 = "DIE PATH 1"
dir2 = "DIR PATH 2"

# Fields to compare
fields_to_check = ["is_vulnerable", "is_security_vulnerable", "cwe", "severity", "cvss_score"]

# Initialize counters
match_counts = {field: 0 for field in fields_to_check}

# Iterate over JSON files in dir1
for filename in os.listdir(dir1):
    if not filename.endswith(".json"):
        continue

    file1_path = os.path.join(dir1, filename)
    file2_path = os.path.join(dir2, filename)

    if not os.path.exists(file2_path):
        continue

    try:
        with open(file1_path, "r", encoding="utf-8") as f1, open(file2_path, "r", encoding="utf-8") as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
    except (json.JSONDecodeError, OSError):
        print(f"Skipping {filename}, invalid JSON or file error")
        continue

    llm1 = data1.get("llm_output", {})
    llm2 = data2.get("llm_output", {})
    gt = data1.get("gt", data2.get("gt", {}))

    # Check each field
    for field in fields_to_check:
        if field == "is_vulnerable" or field == "is_security_vulnerable":
            if (type(llm1) == type(llm2) == dict) and llm1.get(field) and llm2.get(field):
                match_counts[field] += 1
        else:
            print((field in llm1), (field in llm2), (field in gt), (type(llm1), type(llm2)))
            if (field in llm1) and (field in llm2) and (field in gt) and (type(llm1) == type(llm2) == dict):
                val1 = llm1.get(field)
                val2 = llm2.get(field)
                gt_val = gt.get(field)

                # Check equality with gt as well
                if val1 == val2 == gt_val:
                    match_counts[field] += 1

# Save aggregate results in dir2
output_path = os.path.join(dir2, "perfect_match_results.json")
with open(output_path, "w", encoding="utf-8") as out_file:
    json.dump(match_counts, out_file, indent=4)

print(f"Perfect match summary saved to {output_path}")
