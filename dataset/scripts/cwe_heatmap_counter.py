import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import re

def get_cwe_binned_counts(file_name: str, bin_size: int = 100):
    """
    Reads the 'cwe' field (list of CWE identifiers) from each object in the JSON file,
    groups them into ranges of `bin_size`, and returns labels and values.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)

    cwe_counter = Counter()

    # Collect all CWE identifiers
    for entry in data:
        cwes = entry.get("cwe", [])
        if isinstance(cwes, list):
            cwe_counter.update(cwes)

    if not cwe_counter:
        print(f"No CWE data found in {file_name}")
        return [], []

    # Bin CWEs into ranges
    binned_counter = Counter()
    for cwe, count in cwe_counter.items():
        match = re.search(r"\d+", cwe)  # extract number
        if match:
            cwe_num = int(match.group())
            start = ((cwe_num - 1) // bin_size) * bin_size + 1
            end = start + bin_size - 1
            bin_label = f"CWE-{start}–{end}"
            binned_counter[bin_label] += count

    # Sort bins numerically
    bin_items = sorted(
        binned_counter.items(),
        key=lambda x: int(re.search(r"\d+", x[0]).group())
    )
    labels, values = zip(*bin_items)
    return labels, values


def get_title(counter):
    if counter == 1:
        return "Evaluation Dataset"
    elif counter == 2:
        return "Fine-tuning (Training) Dataset"
    else:
        return "Fine-tuning (Validation) Dataset"


def save_multiple_cwe_heatmaps(file_paths, output_png="multi_cwe_heatmap.png", bin_size=100):
    """
    Takes multiple JSON files and creates stacked vertical heatmaps,
    each with its own colorbar.
    """
    fig, axes = plt.subplots(len(file_paths), 1, figsize=(12, 3 * len(file_paths)))

    if len(file_paths) == 1:
        axes = [axes]  # make iterable if only one

    counter = 0
    for ax, file_name in zip(axes, file_paths):
        counter += 1
        labels, values = get_cwe_binned_counts(file_name, bin_size)
        if not labels:
            continue

        values_array = np.array(values).reshape(1, -1)

        im = ax.imshow(values_array, cmap="Reds", aspect="auto")
        ax.set_xticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right")

        # Vertical Y-axis label instead of tick
        ax.set_yticks([])
        ax.set_ylabel("", rotation=90, va="center")

        ax.set_title(get_title(counter))

        # Individual colorbar for each subplot
        cbar = fig.colorbar(im, ax=ax, orientation="vertical", fraction=0.025, pad=0.02)
        cbar.set_label("Frequency")

    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    plt.close()

    print(f"✅ Multi-heatmap saved as {output_png}")


# Example usage
if __name__ == "__main__":
    file_paths = [
        "JSON PATHS COME HERE ",
    ]
    save_multiple_cwe_heatmaps(file_paths, "../../diagrams/multi_cwe_heatmap.png", bin_size=100)
