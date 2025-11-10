import json
import tiktoken

def average_tokens_desc_method(json_path: str):
    # Load tokenizer for gpt-4o-mini
    enc = tiktoken.encoding_for_model("gpt-4o-mini")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    token_counts = []
    for obj in data:
        # description tokens
        desc_tokens = len(enc.encode(obj.get("description", "")))
        token_counts.append(desc_tokens)

        # method_level tokens
        method_level = obj.get("vulnerability", {}).get("method_level", [])
        for method_item in method_level:
            method_tokens = len(enc.encode(method_item))
            token_counts.append(method_tokens)

    avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0
    return avg_tokens


if __name__ == "__main__":
    json_path = "JSON PATH COMES HERE"  # change this path
    avg = average_tokens_desc_method(json_path)
    print(f"Average tokens (description + method_level, gpt-4o-mini): {avg:.2f}")
