import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Fine-tuned cumulative data ---
data = [
    # data matrix comes here
]

df = pd.DataFrame(data, columns=["Metric", "Distance", "Description+file", "Description+method", "Description+hunk",
                                 "Description"])

# --- Save heatmap for each metric ---
for metric in df["Metric"].unique():
    subset = df[df["Metric"] == metric].set_index("Distance")
    subset = subset.drop(columns=["Metric"])

    plt.figure(figsize=(6, 4))
    sns.heatmap(subset, annot=True, fmt="d", cmap="YlOrBr", cbar=True)
    plt.title(f"CASEY Heatmap - {metric}")
    plt.ylabel("Distance")
    plt.xlabel("Prompt")

    # Save as PNG
    filename = metric.replace(" ", "_").replace("(", "").replace(")", "").replace("=", "eq").replace("⊆", "subset")
    plt.savefig(f"casey_heatmap_{filename}.png", dpi=300, bbox_inches="tight")
    plt.close()
