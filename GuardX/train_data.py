import re

# Step 1: Read the data from the text file
file_path = 'train_data_log.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# Step 2: Process the data
def extract_metrics(lines):
    metrics = {}
    current_model = None
    current_section = None
    model_types = ["Logistic Regression Model", "Random Forest Model Class-imbalanced", "Random Forest Model Class-Balanced"]

    for line in lines:
        line = line.strip()

        # Match the model names and accuracy
        if any(model_type in line for model_type in model_types):
            for model_type in model_types:
                if model_type in line:
                    current_model = model_type
                    break
            if "Accuracy" in line:
                accuracy = float(line.split(":")[-1].strip())
                if current_model not in metrics:
                    metrics[current_model] = {"Accuracy": accuracy, "Metrics": [], "Best Parameters": None}
                else:
                    metrics[current_model]["Accuracy"] = accuracy
                current_section = "Accuracy"
            elif "Best Parameters" in line:
                best_parameters = re.findall(r'\{.*?\}', line)[0]
                if current_model not in metrics:
                    metrics[current_model] = {"Accuracy": None, "Metrics": [], "Best Parameters": best_parameters}
                else:
                    metrics[current_model]["Best Parameters"] = best_parameters
                current_section = "Best Parameters"

        # Match the precision, recall, f1-score lines
        elif re.match(r'^\s*\w', line) and current_model and current_section:
            parts = line.split()
            if len(parts) == 5:
                category = parts[0]
                precision = float(parts[1])
                recall = float(parts[2])
                f1_score = float(parts[3])
                support = int(parts[4])
                metrics[current_model]["Metrics"].append({
                    "Category": category,
                    "Precision": precision,
                    "Recall": recall,
                    "F1-Score": f1_score,
                    "Support": support
                })

        # Handle overall accuracy, macro avg, and weighted avg
        elif line.startswith("accuracy") or line.startswith("macro avg") or line.startswith("weighted avg"):
            if current_model and current_section:
                parts = line.split()
                category = parts[0] + " " + parts[1]
                precision = float(parts[2])
                recall = float(parts[3])
                f1_score = float(parts[4])
                support = int(parts[5])
                metrics[current_model]["Metrics"].append({
                    "Category": category,
                    "Precision": precision,
                    "Recall": recall,
                    "F1-Score": f1_score,
                    "Support": support
                })

    return metrics

# Extract metrics from the log file
metrics = extract_metrics(lines)

