import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_casey = [
    # data matrix comes here
]

data_base = [
    # data matrix comes here
]

# --- Create DataFrames ---
cols = ["Metric", "Distance", "Description+file", "Description+method", "Description+hunk", "Description"]
df_base = pd.DataFrame(data_base, columns=cols)
df_casey = pd.DataFrame(data_casey, columns=cols)

# --- Compute Difference (Fine-tuned - Baseline) ---
df_diff = df_casey.copy()
for col in ["Description+file", "Description+method", "Description+hunk", "Description"]:
    df_diff[col] = df_casey[col] - df_base[col]

# --- Plot Difference Heatmap for each metric ---
for metric in df_diff["Metric"].unique():
    subset = df_diff[df_diff["Metric"] == metric].set_index("Distance")
    subset = subset.drop(columns=["Metric"])

    plt.figure(figsize=(6, 4))
    sns.heatmap(subset, annot=True, fmt="d", cmap="RdYlGn", center=0, cbar=True)
    plt.title(f"Differential Heatmap - {metric}") #(CASEY - Baseline)
    plt.ylabel("Distance")
    plt.xlabel("Prompt")

    # Save as PNG
    filename = metric.replace(" ", "_").replace("(", "").replace(")", "").replace("=", "eq").replace("⊆", "subset")
    plt.savefig(f"diff_heatmap_{filename}.png", dpi=300, bbox_inches="tight")
    plt.close()
