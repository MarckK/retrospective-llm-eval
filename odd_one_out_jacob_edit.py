import datasets
import yaml
from typing import Callable
import numpy as np
import random

from truthfulqa_dataset import load_truthfulqa

DATASET_FILENAME = "crafted_nora+vasco_v1-gram.jsonl"
# DATASET_FILENAME = "crafted_dataset_unfiltered.jsonl"


def extract_random_samples(ds: datasets.Dataset, k: int = 1) -> (list[dict], datasets.Dataset):
    """Sample an item and return the modified dataset without the sampled item."""

    if k > len(ds):
        raise ValueError(f"Cannot sample {k} items from a dataset of length {len(ds)}")

    indices = np.random.choice(len(ds), k, replace=False)
    return [ds[int(i)] for i in indices], ds.select([i for i in range(len(ds)) if i not in indices])


def generic_sample_to_str(sample: dict) -> str:
    """Encode a sample as a string."""
    return yaml.dump(sample)


def truthfulqa_sample_to_str(sample: dict, exclude_options: bool=False) -> str:
    """Represent a TruthfulQA sample as a human-legible string."""
    s = ""
    s += "Sample:\n"
    s += f"\tquestion: {sample['question']}\n"
    if not exclude_options:
        s += "\tchoices:\n"
        sorted_choices_and_labels = sorted(zip(sample["mc1_targets"]["choices"], sample["mc1_targets"]["labels"]), key=lambda x: x[0])
        for choice, label in sorted_choices_and_labels:
            s += f"\t\t- {choice}" + (" (correct)" if label in [1, "1"] else "") + "\n"
    return s


def make_odd_one_out_sample(
        odd_sample: dict,
        regular_samples: list[dict],
        question="Which of the following is different from the others?",
        sample_to_str: Callable[[dict], str] = generic_sample_to_str
    ) -> dict:
    """Create an odd-one-out question from the given samples."""
    sample_to_str(odd_sample)
    encoded_samples = [sample_to_str(odd_sample)] + [
        sample_to_str(sample) for sample in regular_samples
    ]
    labels = [1] + [0] * len(regular_samples)
    randomized_samples = list(zip(encoded_samples, labels))
    random.shuffle(randomized_samples)
    encoded_samples, labels = zip(*randomized_samples)
    return {
        "question": question,
        "targets": {
            "choices": list(encoded_samples),
            "labels": list(labels)
        }
    }


def make_odd_one_out_samples_from_datasets(
        odd_dataset: datasets.Dataset,
        regular_dataset: datasets.Dataset,
        num_regular_to_show_per_odd: int = 2,
        num_samples: int = 1,
        sample_to_str: Callable[[dict], str] = generic_sample_to_str,
        replace_odd_dataset: bool = False,
        replace_regular_dataset: bool = False
    ) -> (list[dict], datasets.Dataset, datasets.Dataset):
    """Create random odd-one-out questions from the given datasets."""
    samples = []
    for _ in range(num_samples):
        odd_one_out, ds_odd = extract_random_samples(odd_dataset, 1)
        odd_one_out = odd_one_out[0]
        regular_samples, ds_regular = extract_random_samples(regular_dataset, num_regular_to_show_per_odd)
        if not replace_odd_dataset:
            odd_dataset = ds_odd
        if not replace_regular_dataset:
            regular_dataset = ds_regular
        samples.append(make_odd_one_out_sample(odd_one_out, regular_samples, sample_to_str=sample_to_str))
    return samples, odd_dataset, regular_dataset


if __name__ == "__main__":
    # @TODO move to tests
    ds1 = load_truthfulqa("Misconceptions")
    ds1 = ds1.remove_columns(["mc2_targets"])
    ds2 = datasets.load_dataset(
            "json", data_files='data/datasets/crafted_nora+vasco_v1-gram.jsonl'
        )["train"]

    # Create multiple odd-one-out questions
    odd_one_out_samples = make_odd_one_out_samples_from_datasets(
        ds2, ds1, 2, 4, sample_to_str=truthfulqa_sample_to_str
    )
    for sample in odd_one_out_samples[0]:
        print(generic_sample_to_str(sample))
