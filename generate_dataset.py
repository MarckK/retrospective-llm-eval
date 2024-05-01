import datasets
import json
import litellm
import pandas as pd
import tqdm

# @TODO make deterministic

from truthfulqa_dataset import load_truthfulqa


def generate_similar_dataset_sample(
    samples: datasets.Dataset,
    model_name="gpt-4-1106-preview",
    max_tokens=500,
    api_base=None,
):
    samples = samples.shuffle()
    resp = litellm.completion(
        model=model_name,
        base_url=api_base,
        messages=[
            {
                "role": "user",
                "content": "Continue this list:\n\n"
                + "\n".join("* " + json.dumps(sample) for sample in samples),
            }
        ],
        temperature=1.0,
        # max_tokens=max_tokens,
        stop=["\n*"],
    )
    content = resp.choices[0].message.content.strip().split("\n\n")[0].replace("* ", "")
    # @TODO find cleaner way to do this
    return datasets.Dataset.from_pandas(
        pd.DataFrame.from_records([json.loads(content)])
    )


def generate_similar_dataset(
    dataset: datasets.Dataset,
    target_size: int,
    model_name="gpt-3.5-turbo",
    examples_per_generation=5,
    max_tokens_per_sample=500,
):
    generated_samples = []
    for _ in tqdm.trange(target_size):
        generated_samples.append(
            generate_similar_dataset_sample(
                # Random selection each time
                samples=dataset.select(range(len(dataset)))
                .shuffle()
                .select(range(examples_per_generation)),
                model_name=model_name,
                # max_tokens=max_tokens_per_sample,
            )
        )
    return datasets.concatenate_datasets(generated_samples)


if __name__ == "__main__":
    ds = load_truthfulqa(category="Misconceptions", type="Non-Adversarial")
    new_ds = generate_similar_dataset(ds, 100, model_name="gpt-4-1106-preview")
    new_ds.to_csv("generated_truthfulqa_dataset.csv")
