import click
import datasets
import dotenv
import pandas as pd

from truthfulqa_evaluation import evaluate_truthfulqa_dataset_mc1_on_model

def get_truthfulqa_dataset():
    return datasets.load_dataset("truthful_qa", "multiple_choice")["validation"]


# Define click arguments

@click.command()
@click.option("--model-name", default="gpt-3.5-turbo", help="The name of the model to evaluate on. See LiteLLM docs for more info.")
# @click.option("--output-file", default="results.csv", help="The name of the file to write the results to.") #@TODO
@click.option("--use-chat-encoding-for-everything", default=True, help="If True, use the chat-model encoding for everything.")
@click.option("--category", default="all", help="The category of the TruthfulQA dataset to evaluate on.")
@click.option("--num-samples", default=-1, help="The number of samples from the TruthfulQA dataset to evaluate on.")
def evaluate_truthfulqa(
    model_name,
    # output_file,
    use_chat_encoding_for_everything,
    category,
    num_samples,
):
    # if output_file:
    #     raise NotImplementedError("Writing to file not yet implemented")

    ds = get_truthfulqa_dataset()
    if category != "all":
        ds = ds.filter(lambda x: x["category"] == category)
    if num_samples != -1:
        ds = ds.select(range(num_samples))
    print("Evaluating on", len(ds), "samples")
    results = evaluate_truthfulqa_dataset_mc1_on_model(
        ds,
        model_name,
        use_chat_encoding_for_everything=use_chat_encoding_for_everything,
    )
    print(results)
    return results


if __name__ == "__main__":
    dotenv.load_dotenv()
    evaluate_truthfulqa()
