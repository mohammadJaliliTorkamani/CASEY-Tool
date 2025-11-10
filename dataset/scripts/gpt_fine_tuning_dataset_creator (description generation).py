import json
from typing import List
import constants

# ==== CONFIG ====
json_file_path = "JSON PATH COMES HERE"

# ==== ASSISTANT FIELD CREATOR ====
def create_assistant_field(description: str) -> str:
    """
    Creates a JSON string for the assistant field.
    """
    data = {
        "description": description  # A natural language explanation of the vulnerability
    }
    return json.dumps(data)

# ==== SYSTEM FIELD CREATORS ====
def system_file(record):
    return constants.LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_FILE

def system_method(record):
    return constants.LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_METHOD

def system_hunk(record):
    return constants.LLM_SYSTEM_FIELD_FOR_DESCRIPTION_GENERATION_USING_HUNK

# ==== USER FIELD CREATORS ====
def user_file(record):
    def format_files(files, delimiter="-----------"):
        lines = []
        for file in files:
            lines.append(f'file name: "{file["name"]}"')
            lines.append(f'file content: "{file["content"]}"')
        blocks = ["\n".join(lines[i:i + 2]) for i in range(0, len(lines), 2)]
        return f"\n{delimiter}\n".join(blocks)

    def format_cwes(cwes):
        return str(cwes)

    record_files = record['vulnerability']['file_level']
    return constants.LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_FILE % (
            format_files(record_files), format_cwes(record['cwe']))

def user_method(record):
    def join_methods(methods, delimiter="-----------"):
        return f"\n{delimiter}\n".join(methods)

    def format_cwes(cwes):
        return str(cwes)

    record_methods = record['vulnerability']['method_level']

    return constants.LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_METHOD % (
        join_methods(record_methods), format_cwes(record['cwe']))

def user_hunk(record):
    def join_lines(lines, delimiter="-----------"):
        return f"\n{delimiter}\n".join(hunk["content"] for hunk in lines)

    def format_cwes(cwes):
        return str(cwes)

    record_hunks = record['vulnerability']['hunk_level']
    return constants.LLM_USER_FIELD_FOR_DESCRIPTION_GENERATION_USING_HUNK % (
            join_lines(record_hunks), format_cwes(record['cwe']))

# ==== MODE CONFIG (only file, method, hunk) ====
mode_map = {
    "file": (system_file, user_file),
    "method": (system_method, user_method),
    "hunk": (system_hunk, user_hunk)
}

# ==== MAIN PROCESSING ====
with open(json_file_path, "r", encoding="utf-8") as f:
    records = json.load(f)

for mode, (system_func, user_func) in mode_map.items():
    dataset = []
    for record in records:
        system_text = system_func(record)
        user_text = user_func(record)

        # Now assistant only contains description text
        assistant_text = create_assistant_field(
            description=record["description"]
        )

        dataset.append({
            "messages": [
                {"role": "system", "content": system_text},
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": assistant_text}
            ]
        })

    output_path = f"../gpt_fine_tuning_validation_{mode}.jsonl"
    with open(output_path, "w", encoding="utf-8") as out_f:
        for item in dataset:
            out_f.write(json.dumps(item) + "\n")
    print(f"Dataset created: {output_path}")
