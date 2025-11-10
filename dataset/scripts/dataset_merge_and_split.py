import json
import random
import tiktoken   # pip install tiktoken
import ijson      # pip install ijson

# ====== SETTINGS ======
# Smallest context: GPT-4o-mini (16384) vs LLaMA 3/3 (128K (but due to hardware limitation during fine-tuning, 2048) → use 2048
# Then take 70% margin for prompt overhead
MAX_CONTEXT_TOKENS = int(2048 * 0.75)

# Tokenizer — GPT-4o-mini tokenizer used as an approximation for both models
encoding = tiktoken.encoding_for_model("gpt-4o-mini")

from decimal import Decimal

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def count_tokens(text: str) -> int:
    return len(encoding.encode(text, disallowed_special=()))

def record_token_count(record: dict) -> int:
    """Sum tokens for all file_level name and content fields."""
    total = 0
    try:
        for file_item in record.get("vulnerability", {}).get("file_level", []):
            total += count_tokens(file_item.get("name", ""))
            total += count_tokens(file_item.get("content", ""))
    except (TypeError, AttributeError):
        pass
    return total

def sample_from_large_json(file_name: str, max_per_file: int = 300):
    """Stream-sample records from a large JSON array without loading it all."""
    sampled = []
    skipped_count = 0

    # For a top-level JSON array:
    json_path = "item"
    # If instead your data is like { "records": [ ... ] }, change to:
    # json_path = "records.item"

    with open(file_name, "r", encoding="utf-8") as f:
        for record in ijson.items(f, json_path):
            if record_token_count(record) <= MAX_CONTEXT_TOKENS:
                sampled.append(record)
                if len(sampled) >= max_per_file:
                    break
            else:
                skipped_count += 1

    print(f"ℹ️ {file_name}: kept {len(sampled)}, skipped {skipped_count} over {MAX_CONTEXT_TOKENS} tokens")
    return sampled

def merge_and_shuffle(file_list, output_file, max_per_file=300):
    """Merge samples from multiple files, shuffle, and save."""
    merged_data = []

    for file_name in file_list:
        merged_data.extend(sample_from_large_json(file_name, max_per_file))

    random.shuffle(merged_data)

    merged_data = convert_decimals(merged_data)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Saved {len(merged_data)} records into '{output_file}'.")

# ====== FILE GROUPS ======
fine_tune_group_files = [
    "JSON FILES COME HERE",
]

evaluation_group_files = [
    "JSON FILES COME HERE",
]

# ====== PROCESS ======
merge_and_shuffle(evaluation_group_files, "JSON PATH COMES HER")
merge_and_shuffle(fine_tune_group_files, "JSON PATH COMES HERE")
