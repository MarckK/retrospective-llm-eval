import subprocess
import os
import json
import time
from multiprocessing import Pool, Manager

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

# Define parallelism
num_parallel_model_evaluations = 5
num_parallel_trials_per_evaluation = 5


# Function to execute evaluation and print warning if it takes too long
def execute_evaluation(cmd_output_file, max_duration, results):
    cmd, output_file = cmd_output_file
    start_time = time.time()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    while process.poll() is None:
        time.sleep(1)
        if time.time() - start_time > max_duration:
            results.append((output_file, time.time() - start_time))
            process.terminate()
            return
    end_time = time.time()
    duration = end_time - start_time
    if duration > max_duration:
        results.append((output_file, duration))

# Generate commands for each combination of model and topk value
evaluation_commands = []
for model in models:
    for topk in topks:
        if topk == 1:
            crafted_output_file = f"runs/run_crafted_law_{model}.txt"
            orig_output_file = f"runs/run_orig_law_{model}.txt"
        else:
            crafted_output_file = f"runs/run_crafted_law_{model}_topk{topk}.txt"
            orig_output_file = f"runs/run_orig_law_{model}_topk{topk}.txt"

        if not (os.path.exists(crafted_output_file) and is_valid_json(crafted_output_file)):
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
            evaluation_commands.append((crafted_cmd, crafted_output_file))

        if not (os.path.exists(orig_output_file) and is_valid_json(orig_output_file)):
            orig_cmd = [
                "python",
                "evaluate_dataset.py",
                "--verbose",
                "--topk",
                str(topk),
                "--parallelism",
                num_parallel_trials_per_evaluation,
                "--category",
                "law",
                "--model",
                model
            ]
            evaluation_commands.append((orig_cmd, orig_output_file))

# Execute evaluations in parallel
with Manager() as manager:
    warning_results = manager.list()  # Shared list to store warning results
    with Pool(num_parallel_model_evaluations) as pool:
        pool.starmap(execute_evaluation, [(cmd_output_file, 3600, warning_results) for cmd_output_file in evaluation_commands])

    # Print warning messages for evaluations exceeding time limit
    for output_file, duration in warning_results:
        print(f"Warning: Evaluation for {output_file} took {duration/60:.2f} minutes.")

print("All evaluations completed.")
