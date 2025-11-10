import json
import tiktoken

def average_description_tokens(json_path: str):
    # Load tokenizer for gpt-3.5-turbo-16k
    enc = tiktoken.encoding_for_model("gpt-4o-mini")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    token_counts = []
    for obj in data:
        desc_tokens = len(enc.encode(obj.get("description", "")))
        token_counts.append(desc_tokens)

    avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0
    return avg_tokens


if __name__ == "__main__":
    json_path = "JSON PATH COMES HERE"  # change this path
    avg = average_description_tokens(json_path)
    print(f"Average description tokens (gpt-4o-mini): {avg:.2f}")
