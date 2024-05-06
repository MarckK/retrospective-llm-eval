#!/bin/bash

# Define the list of models to iterate over
models=("babbage-002" "davinci-002" "gpt-3.5-turbo" "gpt-4-turbo-2024-04-09")

# Define the topk values to iterate over
topks=(1 2)
# topks=(3)

# Loop through each model
for model in "${models[@]}"; do
  # Loop through each topk value
  for topk in "${topks[@]}"; do
    # Adjust filenames based on topk value
    if [ "$topk" -eq 1 ]; then
      crafted_output_file="runs/run_crafted_law_${model}.txt"
      orig_output_file="runs/run_orig_law_${model}.txt"
    else
      crafted_output_file="runs/run_crafted_law_${model}_topk${topk}.txt"
      orig_output_file="runs/run_orig_law_${model}_topk${topk}.txt"
    fi

    # Command for the crafted dataset (law category)
    python evaluate_dataset.py --verbose --topk "$topk" --dataset-file data/datasets/law_non-adv.csv --model "$model" > "$crafted_output_file"
    echo "Executed with model $model for crafted dataset with topk=$topk. Output saved to $crafted_output_file."

    # Command for the original dataset (law category)
    python evaluate_dataset.py --verbose --topk "$topk" --category law --model "$model" > "$orig_output_file"
    echo "Executed with model $model for original dataset with topk=$topk. Output saved to $orig_output_file."
  done
done
