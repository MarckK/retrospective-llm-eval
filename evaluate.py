import click
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
@click.option("--verbose", is_flag=True, default=False, help="Provide verbose output.")
def evaluate_truthfulqa(
    model,
    # output_file,
    use_chat_encoding_for_everything,
    category,
    api_url,
    num_samples,
    verbose,
):
    # if output_file:
    #     raise NotImplementedError("Writing to file not yet implemented")

    # @TODO improve this
    if api_url:
        openai.api_base = api_url + "/v1"
        print("** Using API base:", openai.api_base, "**")

    ds = load_truthfulqa(category)
    if num_samples != -1:
        ds = ds.select(range(num_samples))
    print("Evaluating on", len(ds), "samples")
    results = evaluate_truthfulqa_dataset_mc1_on_model(
        ds,
        model,
        use_chat_encoding_for_everything=use_chat_encoding_for_everything,
        verbose=verbose,
    )
    print(results)
    return results


if __name__ == "__main__":
    dotenv.load_dotenv()
    evaluate_truthfulqa()
