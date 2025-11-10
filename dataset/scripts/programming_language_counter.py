import json
import os
from collections import Counter

def count_extensions(file_name: str):
    """
    Count file extensions from a JSON file.
    The JSON file should contain an array of objects, each with
    vulnerability -> file_level -> list of objects with 'name'.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)

    ext_counter = Counter()

    for entry in data:
        vulnerability = entry.get("vulnerability", {})
        file_level = vulnerability.get("file_level", [])
        for file_obj in file_level:
            name = file_obj.get("name")
            if name and "." in name:
                _, ext = os.path.splitext(name)
                if ext:  # skip files without extension
                    ext_counter[ext.lower()] += 1

    return ext_counter


# Example usage
if __name__ == "__main__":
    file_path = "JSON PATH COMES HERE"  # replace with your JSON file
    ext_counts = count_extensions(file_path)
    print("File extension frequencies:")
    for ext, count in ext_counts.most_common():
        print(f"{ext}: {count}")
