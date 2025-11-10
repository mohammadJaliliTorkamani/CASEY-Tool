import json
import tiktoken

def average_description_tokens(json_path: str):
    # Load tokenizer for gpt-4o-mini
    enc = tiktoken.encoding_for_model("gpt-4o-mini")

    llm_token_counts = []
    gt_token_counts = []

    with open(json_path, "r", encoding="utf-8") as f:
        obj = json.load(f)

        results = obj.get("results", [])
        for item in results:
            llm_desc = item.get("llm_description", "")
            gt_desc = item.get("gt_description", "")

            if llm_desc:
                llm_token_counts.append(len(enc.encode(llm_desc)))
            if gt_desc:
                gt_token_counts.append(len(enc.encode(gt_desc)))

    avg_llm = sum(llm_token_counts) / len(llm_token_counts) if llm_token_counts else 0
    avg_gt = sum(gt_token_counts) / len(gt_token_counts) if gt_token_counts else 0

    return avg_llm, avg_gt


if __name__ == "__main__":
    json_path = "JSON PATH 1 COMES HERE"  # change this path
    json_path2 = "JSON PATH 2 COMES HERE"  # change this path
    avg_llm, avg_gt = average_description_tokens(json_path)
    print(f"Average LLM description tokens (gpt-4o-mini): {avg_llm:.2f}")
    print(f"Average GT description tokens  (gpt-4o-mini): {avg_gt:.2f}")
