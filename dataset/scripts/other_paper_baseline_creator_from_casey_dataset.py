import json

# CONFIGURATION
MODE = "MULTI"  # "SINGLE" or "MULTI"
LEVEL = "FULL"  # "PURE" or "FULL"

# Input JSON file
input_path = "JSON PATH COMES HERE"  # change to your actual input file

# Determine output path based on config
output_filename = f"{MODE}_{LEVEL}.json"
output_path = output_filename


def extract_func(obj, mode, level):
    """
    level = "FULL": use file_level -> list of objects with "content"
    level = "PURE": use method_level -> list of strings
    mode = "SINGLE": only the first element
    mode = "MULTI": concatenate all elements
    """
    obj = obj.get("vulnerability", [])
    if level == "FULL":
        items = obj.get("file_level", [])
        if mode == "SINGLE":
            if items:
                return items[0].get("content", None)
            return None
        else:  # MULTI
            contents = []
            for item in items:
                content = item.get("content", "")
                if content:
                    contents.append(content)
            return "".join(contents) if contents else None

    else:  # PURE
        items = obj.get("method_level", [])
        if mode == "SINGLE":
            if items:
                return items[0]
            return None
        else:  # MULTI
            return "".join(items) if items else None


def extract_cwe(obj):
    """
    Extract the first element of "cwe" if present.
    """
    cwe_list = obj.get("cwe", [])
    if isinstance(cwe_list, list) and len(cwe_list) > 0:
        return cwe_list[0]
    return None


def process_json(input_path, output_path, mode, level):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    vulnerable_entries = []

    for obj in data:
        func_value = extract_func(obj, mode, level)
        cwe_value = extract_cwe(obj)
        vulnerable_entries.append({
            "func": func_value,
            "cwe": cwe_value
        })

    # Wrap in a top-level "vulnerable" field
    wrapped_output = {"vulnerable": vulnerable_entries}

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(wrapped_output, f, indent=4)

    print(f"Output written to {output_path}")


if __name__ == "__main__":
    process_json(input_path, output_path, MODE, LEVEL)
