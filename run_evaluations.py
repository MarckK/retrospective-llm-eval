import subprocess
import os
import json

# Function to check if a file contains valid JSON data
def is_valid_json(file_path):
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True
    except (IOError, ValueError):
        return False

# Define the list of models to iterate over
models = ["babbage-002", "davinci-002", "gpt-3.5-turbo", "gpt-4-turbo-2024-04-09"]

# Define the topk values to iterate over
topks = [1, 2]

# Loop through each model
for model in models:
    # Loop through each topk value
    for topk in topks:
        # Adjust filenames based on topk value
        if topk == 1:
            crafted_output_file = f"runs/run_crafted_law_{model}.txt"
            orig_output_file = f"runs/run_orig_law_{model}.txt"
        else:
            crafted_output_file = f"runs/run_crafted_law_{model}_topk{topk}.txt"
            orig_output_file = f"runs/run_orig_law_{model}_topk{topk}.txt"

        # Check if output files already exist and contain valid JSON
        if os.path.exists(crafted_output_file) and is_valid_json(crafted_output_file):
            print(f"Evaluation for model {model} with topk={topk} already done. Skipping.")
        else:
            # Command for the crafted dataset (law category)
            crafted_cmd = [
                "python",
                "evaluate_dataset.py",
                "--verbose",
                "--topk",
                str(topk),
                "--dataset-file",
                "data/datasets/law_non-adv.csv",
                "--model",
                model
            ]
            with open(crafted_output_file, "w") as f:
                subprocess.run(crafted_cmd, stdout=f)
            print(f"Executed with model {model} for crafted dataset with topk={topk}. Output saved to {crafted_output_file}.")

        if os.path.exists(orig_output_file) and is_valid_json(orig_output_file):
            print(f"Evaluation for model {model} with topk={topk} already done. Skipping.")
        else:
            # Command for the original dataset (law category)
            orig_cmd = [
                "python",
                "evaluate_dataset.py",
                "--verbose",
                "--topk",
                str(topk),
                "--category",
                "law",
                "--model",
                model
            ]
            with open(orig_output_file, "w") as f:
                subprocess.run(orig_cmd, stdout=f)
            print(f"Executed with model {model} for original dataset with topk={topk}. Output saved to {orig_output_file}.")
