import json
from collections import Counter


def count_severities(file_name: str):
    """
    Count the frequency of each 'severity' field in a JSON file.
    The JSON file should contain an array of objects.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)

    severity_counter = Counter()

    for entry in data:
        severity = entry.get("severity")
        if severity:
            severity_counter[severity.lower()] += 1  # normalize to lowercase

    return severity_counter


# Example usage
if __name__ == "__main__":
    file_path = "JSON PATH COMES HERE"
    severity_counts = count_severities(file_path)
    print("Severity frequencies:")
    for sev, count in severity_counts.most_common():
        print(f"{sev}: {count}")
