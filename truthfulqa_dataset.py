
import datasets


def get_truthfulqa_dataset(category=None):
    ds = datasets.load_dataset("truthful_qa", "multiple_choice")["validation"]
    if category and category != "all":
        # The multiple_choice dataset does not have a category field, so we need to filter on the generation dataset
        filtered_ds = datasets.load_dataset("truthful_qa", "generation")
        filtered_ds = filtered_ds.filter(
            lambda x: x["category"].lower() == category.lower()
        )
        filtered_questions = filtered_ds["validation"]["question"]
        ds = ds.filter(lambda x: x["question"] in filtered_questions)
    return ds
