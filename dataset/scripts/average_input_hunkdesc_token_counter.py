import json
import tiktoken

def average_tokens_desc_hunk(json_path: str):
    # Load tokenizer for gpt-4o-mini
    enc = tiktoken.encoding_for_model("gpt-4o-mini")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    token_counts = []
    for obj in data:
        # description tokens
        desc_tokens = len(enc.encode(obj.get("description", "")))
        token_counts.append(desc_tokens)

        # hunk_level content tokens
        hunk_level = obj.get("vulnerability", {}).get("hunk_level", [])
        for hunk in hunk_level:
            content_tokens = len(enc.encode(hunk.get("content", "")))
            token_counts.append(content_tokens)

    avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0
    return avg_tokens


if __name__ == "__main__":
    json_path = "JSON PATH COMES HERE"  # change this path
    avg = average_tokens_desc_hunk(json_path)
    print(f"Average tokens (description + hunk_level content, gpt-4o-mini): {avg:.2f}")
