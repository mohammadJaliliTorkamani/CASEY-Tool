import json
from collections import Counter

# Path to your JSON file
json_path = "JSON PATH COMES HERE"  # Replace with your actual JSON path

# Load JSON data
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Flatten all CWE entries into a single list
all_cwes = []
for item in data:
    cwe_list = item.get("cwe", [])
    all_cwes.extend(cwe_list)

# Count frequency of each CWE
cwe_counts = Counter(all_cwes)

# Get the top 3 most common CWEs
top_three = cwe_counts.most_common(3)

# Print results
print("Top 3 most frequent CWEs:")
for cwe, count in top_three:
    print(f"{cwe}: {count}")
