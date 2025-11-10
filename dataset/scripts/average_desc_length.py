import json

def average_description_length(file_name: str):
    """
    Calculate the average length of the 'description' field
    in a JSON file containing an array of objects.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_length = 0
    count = 0

    for entry in data:
        description = entry.get("description")
        if description:
            total_length += len(description)
            count += 1

    if count == 0:
        return 0  # avoid division by zero
    return total_length / count


# Example usage
if __name__ == "__main__":
    file_path = "JSON PATH COMES HERE"  # replace with your JSON file
    avg_len = average_description_length(file_path)
    print(f"Average description length: {avg_len:.2f} characters")
