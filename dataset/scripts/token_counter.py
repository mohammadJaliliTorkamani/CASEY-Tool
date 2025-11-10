import json

import tiktoken

# ==== CONFIG ====
jsonl_file_path = "JSONL PATH COMES HERE"  # <-- set your path here
model_name = "gpt-4o-mini"


def count_tokens_in_jsonl(jsonl_file_path: str, model: str = model_name):
    enc = tiktoken.encoding_for_model(model)

    total_tokens = 0
    num_examples = 0

    with open(jsonl_file_path, "r") as f:
        for line in f:
            if not line.strip():
                continue  # skip empty lines
            item = json.loads(line)
            num_examples += 1

            if "messages" in item and isinstance(item["messages"], list):
                for message in item["messages"]:
                    if "content" in message and isinstance(message["content"], str):
                        total_tokens += len(enc.encode(message["content"]))

    avg_tokens = total_tokens / num_examples if num_examples else 0
    return total_tokens, avg_tokens, num_examples


if __name__ == "__main__":
    total, avg, count = count_tokens_in_jsonl(jsonl_file_path)
    print(f"Total examples: {count}")
    print(f"Total tokens ({model_name}): {total}")
    print(f"Average tokens per example: {avg:.2f}")
