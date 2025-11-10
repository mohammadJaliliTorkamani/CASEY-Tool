import os
import json
from sklearn.metrics import precision_recall_fscore_support, classification_report

# folder path (update this variable)
folder_path = "DIR COMES HERE"

# collect predictions and ground truth
y_true = []
y_pred = []

for filename in os.listdir(folder_path):
    if filename.startswith("result_") and filename.endswith(".json"):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, "r") as f:
            data = json.load(f)

            if type(data.get("llm_output", {})) != dict:
                continue
            gt_sev = data.get("gt", {}).get("severity")
            pred_sev = data.get("llm_output", {}).get("severity")

            if gt_sev and pred_sev and (pred_sev in ["LOW","MEDIUM","HIGH","CRITICAL"]):  # only consider valid entries
                y_true.append(gt_sev.upper())
                y_pred.append(pred_sev.upper())

# compute metrics
if y_true and y_pred:
    print("Classification Report (Precision, Recall, F1 per severity class):")
    print(classification_report(y_true, y_pred, digits=3))
else:
    print("No valid data found to evaluate.")
