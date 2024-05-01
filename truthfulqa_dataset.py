
import datasets


def load_truthfulqa(category=None, type=None):
    ds = datasets.load_dataset("truthful_qa", "multiple_choice")["validation"]
    if category and category != "all":
        # The multiple_choice dataset does not have a category field, so we need to filter on the generation dataset
        filtered_ds = datasets.load_dataset("truthful_qa", "generation")
        filtered_ds = filtered_ds.filter(
            lambda x: x["category"].lower() == category.lower()
        )
        filtered_questions = filtered_ds["validation"]["question"]
        ds = ds.filter(lambda x: x["question"] in filtered_questions)
    if type and type != "all":
        ds2 = datasets.load_dataset("truthful_qa", "generation")["validation"]
        question2type = {x["question"]: x["type"].lower() for x in ds2}
        ds = ds.filter(lambda x: question2type[x["question"]] == type.lower())
    return ds
