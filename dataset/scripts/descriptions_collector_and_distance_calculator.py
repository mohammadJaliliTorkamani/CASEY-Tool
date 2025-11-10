key="API KEY GOES HERE"
import json
import os
import random
import re
import numpy as np
from openai import OpenAI

# === CONFIG ===
TARGET_SAMPLES = 50

# Initialize OpenAI client
client = OpenAI(
    api_key=key
)

# === Folder mapping for GPT & LLaMA ===
LEVELS = {
    "file_level": {
        "gpt": "DIR PATH COMES HERE",
        "llama": "DIR PATH COMES HERE"
    },
    "method_level": {
        "gpt": "DIR PATH COMES HERE",
        "llama": "DIR PATH COMES HERE"
    },
    "hunk_level": {
        "gpt": "DIR PATH COMES HERE",
        "llama": "DIR PATH COMES HERE"
    }
}

pattern = re.compile(r"^result_\d+\.json$")

def collect_files(folder):
    """Collect all result_*.json files from a folder."""
    if not os.path.isdir(folder):
        return []
    return [f for f in os.listdir(folder) if pattern.match(f)]

def get_embedding(text: str):
    """Get embedding vector from OpenAI GPT-4o-mini embedding model."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    v1, v2 = np.array(vec1), np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def validate_file_across_levels(fname):
    """
    Check that a file is valid across ALL levels and both GPT + LLaMA:
    - File exists
    - Has non-empty gt.description
    - Has non-empty llm_output.description
    """
    for lvl, folders in LEVELS.items():
        for model in ["gpt", "llama"]:
            fpath = os.path.join(folders[model], fname)
            if not os.path.exists(fpath):
                return False
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                gt_desc = data.get("gt", {}).get("description", "")
                llm_desc = data.get("llm_output", {}).get("description", "")
                if not gt_desc or not llm_desc:
                    return False
            except:
                return False
    return True

def sample_global_files(target):
    """Sample filenames valid across ALL levels & models."""
    # Step 1: collect intersection of filenames
    common_files = None
    for lvl, folders in LEVELS.items():
        gpt_files = set(collect_files(folders["gpt"]))
        llama_files = set(collect_files(folders["llama"]))
        level_common = gpt_files & llama_files
        common_files = level_common if common_files is None else (common_files & level_common)

    if not common_files:
        raise RuntimeError("❌ No common files across all levels and models")

    common_files = list(common_files)
    random.shuffle(common_files)

    # Step 2: validate across all levels
    valid = [f for f in common_files if validate_file_across_levels(f)]

    if len(valid) < target:
        raise RuntimeError(f"❌ Only found {len(valid)} valid aligned samples, need {target}")

    return valid[:target]

def process_level(level_name, gpt_folder, llama_folder, sample_files):
    """Process one level with globally aligned sample files."""
    print(f"\n=== Processing {level_name} ===")

    gpt_results = []
    llama_results = []

    for fname in sample_files:
        gpt_path = os.path.join(gpt_folder, fname)
        llama_path = os.path.join(llama_folder, fname)

        try:
            with open(gpt_path, "r", encoding="utf-8") as f:
                gpt_data = json.load(f)
            with open(llama_path, "r", encoding="utf-8") as f:
                llama_data = json.load(f)

            gt_desc = gpt_data.get("gt", {}).get("description", "")
            gt_cwe = gpt_data.get("gt", {}).get("cwe", [])
            gt_vuln = gpt_data.get("gt", {}).get("vulnerability", None)

            gpt_llm_desc = gpt_data.get("llm_output", {}).get("description", "")
            llama_llm_desc = llama_data.get("llm_output", {}).get("description", "")

            # Embeddings & similarity
            gt_emb = get_embedding(gt_desc)

            gpt_emb = get_embedding(gpt_llm_desc)
            gpt_sim = cosine_similarity(gpt_emb, gt_emb)

            llama_emb = get_embedding(llama_llm_desc)
            llama_sim = cosine_similarity(llama_emb, gt_emb)

            gpt_results.append({
                "file_name": fname,
                "llm_description": gpt_llm_desc,
                "gt_description": gt_desc,
                "gt_vulnerability": gt_vuln,
                "gt_cwe": gt_cwe,
                "llm_embedding": gpt_emb,
                "gt_embedding": gt_emb,
                "cosine_similarity": gpt_sim
            })

            llama_results.append({
                "file_name": fname,
                "llm_description": llama_llm_desc,
                "gt_description": gt_desc,
                "gt_vulnerability": gt_vuln,
                "gt_cwe": gt_cwe,
                "llm_embedding": llama_emb,
                "gt_embedding": gt_emb,
                "cosine_similarity": llama_sim
            })

        except Exception as e:
            print(f"⚠️ Error with {fname}: {e}")
            continue

    # Save outputs
    for model, results in [("gpt", gpt_results), ("llama", llama_results)]:
        avg_sim = None
        if results:
            sims = [r["cosine_similarity"] for r in results if r["cosine_similarity"] is not None]
            avg_sim = sum(sims) / len(sims) if sims else None
        output = {
            "average_cosine_similarity": avg_sim,
            "results": results
        }
        out_name = f"{model}_description_similarity_results_{level_name}.json"
        with open(out_name, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        print(f"💾 Saved {out_name} with {len(results)} records")

# === Run globally aligned ===
global_samples = sample_global_files(TARGET_SAMPLES)
print(f"🎲 Selected {len(global_samples)} common valid files across all levels")

for level, folders in LEVELS.items():
    process_level(level, folders["gpt"], folders["llama"], global_samples)

print("\n✅ Finished processing all levels with globally aligned samples")
