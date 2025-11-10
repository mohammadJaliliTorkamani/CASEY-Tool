import json
from collections import Counter

def bucketize_cvss(file_name: str):
    """
    Count CVSS scores in 10 buckets (0–1, 1–2, ..., 9–10).
    """
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)

    buckets = Counter()

    for entry in data:
        score = entry.get("cvss_score")
        if isinstance(score, (int, float)) and 0 <= score <= 10:
            # Find bucket index (0–9)
            bucket_index = int(score) if score < 10 else 9
            bucket_label = f"{bucket_index}–{bucket_index+1}" if bucket_index < 9 else "9–10"
            buckets[bucket_label] += 1

    # Ensure all buckets are present, even if zero
    all_buckets = {f"{i}–{i+1}" if i < 9 else "9–10": buckets.get(f"{i}–{i+1}" if i < 9 else "9–10", 0) for i in range(10)}
    return all_buckets


# Example usage
if __name__ == "__main__":
    file_path = "JSON PATH COMES HERE"  # replace with your JSON file
    cvss_buckets = bucketize_cvss(file_path)
    print("CVSS score distribution (10 buckets):")
    for bucket, count in cvss_buckets.items():
        print(f"{bucket}: {count}")
