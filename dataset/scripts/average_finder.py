import json
from glob import glob

import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

# Initialize OpenAI client
client = OpenAI(
    api_key='API COMES HERE')


# Embedding function using OpenAI
def get_embedding(text: str) -> np.ndarray:
    """
    Generate embedding for given text using OpenAI's text-embedding-3-small (or large) model.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)


# Read all result_*.json files
input_files = glob("result_*.json")

data_pairs = []
for file_path in input_files:
    with open(file_path, 'r') as f:
        try:
            content = json.load(f)
            llm_output_raw = content.get("llm_output", {})
            gt_output = content.get("gt", {})

            if isinstance(llm_output_raw, str):
                try:
                    llm_output = json.loads(llm_output_raw)
                except json.JSONDecodeError:
                    continue
            else:
                llm_output = llm_output_raw

            if not isinstance(llm_output, dict) or "description" not in llm_output:
                continue
            if "description" not in gt_output:
                continue

            casey_desc = llm_output["description"]
            nvd_desc = gt_output["description"]

            data_pairs.append({
                "file": file_path,
                "casey": casey_desc,
                "nvd": nvd_desc
            })

        except Exception:
            continue

# Compute embeddings and cosine similarity
cosine_scores = []
casey_texts = [item["casey"] for item in data_pairs]
nvd_texts = [item["nvd"] for item in data_pairs]

casey_embeddings = [get_embedding(text) for text in casey_texts]
nvd_embeddings = [get_embedding(text) for text in nvd_texts]

for emb_casey, emb_nvd in zip(casey_embeddings, nvd_embeddings):
    cos_sim = cosine_similarity([emb_casey], [emb_nvd])[0][0]
    cosine_scores.append(cos_sim)

# Compute average text lengths
length_casey = [len(text.split()) for text in casey_texts]
length_nvd = [len(text.split()) for text in nvd_texts]

# Combine results
results = []
for i, item in enumerate(data_pairs):
    results.append({
        "file": item["file"],
        "cosine_similarity": cosine_scores[i],
        "length": {
            "casey_word_count": length_casey[i],
            "nvd_word_count": length_nvd[i]
        }
    })

# Compute averages
average_result = {
    "cosine_similarity_avg": float(np.mean(cosine_scores)),
    "average_length_words": {
        "casey": float(np.mean(length_casey)),
        "nvd": float(np.mean(length_nvd))
    }
}

final_output = {
    "pairwise_scores": results,
    "averages": average_result
}

# Save output to JSON
with open("description_analysis_report.json", "w") as f_out:
    json.dump(final_output, f_out, indent=2)

print("✅ Analysis complete. Results saved to description_analysis_report.json")
