import json
import random
import os

# Path to your JSON file
input_file_path = "JSON PATH COMES HERE"

# Output file names
train_file_path = "JSON PATH COMES HERE"
val_file_path = "JSON PATH COMES HERE"

# Load the JSON array
with open(input_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Ensure data is a list
if not isinstance(data, list):
    raise ValueError("The JSON file does not contain an array of objects.")

# Shuffle the data
random.shuffle(data)

# Split into 80% train, 20% validation
split_index = int(len(data) * 0.8)
train_data = data[:split_index]
val_data = data[split_index:]

# Save the datasets
with open(train_file_path, "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=2, ensure_ascii=False)

with open(val_file_path, "w", encoding="utf-8") as f:
    json.dump(val_data, f, indent=2, ensure_ascii=False)

print(f"Training set saved to {os.path.abspath(train_file_path)} ({len(train_data)} items)")
print(f"Validation set saved to {os.path.abspath(val_file_path)} ({len(val_data)} items)")
