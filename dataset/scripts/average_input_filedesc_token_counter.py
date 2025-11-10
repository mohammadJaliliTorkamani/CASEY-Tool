import json
import tiktoken

def average_tokens(json_path: str):
    # Load the tokenizer for gpt-4o-mini
    enc = tiktoken.encoding_for_model("gpt-4o-mini")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    token_counts = []
    for obj in data:
        # count tokens in description
        desc_tokens = len(enc.encode(obj.get("description", "")))
        token_counts.append(desc_tokens)

        # count tokens in file_level -> name + content
        file_level = obj.get("vulnerability", {}).get("file_level", [])
        for fl in file_level:
            name_tokens = len(enc.encode(fl.get("name", "")))
            content_tokens = len(enc.encode(fl.get("content", "")))
            token_counts.append(name_tokens + content_tokens)

    # avoid division by zero
    avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0
    return avg_tokens


if __name__ == "__main__":
    json_path = "JSON PATH COMES HERE"
    avg = average_tokens(json_path)
    print(f"Average tokens (gpt-4o-mini): {avg:.2f}")
