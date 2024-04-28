import click
import datasets
import dotenv
import openai

from truthfulqa_evaluation import evaluate_truthfulqa_dataset_mc1_on_model
from truthfulqa_dataset import load_truthfulqa


@click.command()
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    help="The name of the model to evaluate on. See LiteLLM docs for more info.",
)
# @click.option("--output-file", default="results.csv", help="The name of the file to write the results to.") #@TODO
@click.option(
    "--use-chat-encoding-for-everything",
    default=True,
    help="If True, use the chat-model encoding for everything.",
)
@click.option(
    "--category",
    default="Misconceptions",
    help="The category of the TruthfulQA dataset to evaluate on.",
)
@click.option(
    "--num-samples",
    default=-1,
    help="The number of samples from the TruthfulQA dataset to evaluate on.",
)
@click.option(
    "--api-url",
    default=None,
    help="The API url to use to query an LLM.",
)
@click.option(
    "--dataset-file",
    default=None,
    help="The path to a dataset file to evaluate on.",
)
@click.option(
    "--topk",
    default=1,
    help="Number of distinct options to pick.",
)
@click.option("--verbose", is_flag=True, default=False, help="Provide verbose output.")
def evaluate_truthfulqa(
    model,
    # output_file,
    use_chat_encoding_for_everything,
    category,
    api_url,
    num_samples,
    dataset_file,
    topk,
    verbose,
):
    # if output_file:
    #     raise NotImplementedError("Writing to file not yet implemented")

    # @TODO improve this
    if api_url:
        openai.api_base = api_url + "/v1"
        print("** Using API base:", openai.api_base, "**")

    if dataset_file:
        if dataset_file.endswith(".csv"):
            ds = datasets.load_dataset("csv", data_files=dataset_file)["train"]
            #@TOOD clean this up
            def array(x, dtype=None):
                return x
            def int32(x, dtype=None):
                return x
            def int64(x, dtype=None):
                return x
            ds = ds.map(
                lambda x: {
                    "question": x["question"],
                    "mc1_targets": eval(x["mc1_targets"], dict(globals(), array=array, int32=int32, int64=int64), locals()),
                }
            )
        elif dataset_file.endswith(".json") or dataset_file.endswith(".jsonl"):
            ds = datasets.load_dataset("json", data_files=dataset_file)["train"]
        else:
            raise ValueError("Unknown dataset file type")
        print(ds)
        print(ds["mc1_targets"])
    else:
        ds = load_truthfulqa(category)
    if num_samples != -1:
        ds = ds.select(range(num_samples))
    print("Evaluating on", len(ds), "samples")
    results = evaluate_truthfulqa_dataset_mc1_on_model(
        ds,
        model,
        topk=topk,
        use_chat_encoding_for_everything=use_chat_encoding_for_everything,
        verbose=verbose,
    )
    print(results)
    return results


if __name__ == "__main__":
    dotenv.load_dotenv()
    evaluate_truthfulqa()
