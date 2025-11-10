import json
from collections import Counter

def count_cvss_versions(file_name: str):
    """
    Count frequency of each 'cvss_version' in a JSON file.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)

    version_counter = Counter()

    for entry in data:
        version = entry.get("cvss_version")
        if version:
            version_counter[str(version)] += 1  # convert to string just in case

    return version_counter


# Example usage
if __name__ == "__main__":
    file_path = "JSON PATH COMES HERE"  # replace with your JSON file
    version_counts = count_cvss_versions(file_path)
    print("CVSS version frequencies:")
    for ver, count in version_counts.most_common():
        print(f"{ver}: {count}")
