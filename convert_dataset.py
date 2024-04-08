import datasets
import numpy as np
import os


def convert_exported_law_dataset():
    if not os.path.exists("datasets/crafted_dataset_law_exported.csv"):
        return

    law_ds = datasets.load_dataset(
        "csv", data_files="datasets/crafted_dataset_law_exported.csv"
    )["train"]

    law_ds = law_ds.map(lambda x:
        dict(
            question=x["Rewritten in style"],
            mc1_targets=dict(
                choices=[
                    x
                    for x in [
                            x["Correct"],
                    ] + [
                        x[f"Incorrect{i}"]
                        for i in range(1, 11)
                    ]
                    if x
                ],
                labels=np.array(
                    [1] + [0] * (sum(bool(x[f"Incorrect{i}"]) for i in range(1, 11)) - 1),
                    dtype=np.int32
                )
            ),
        ),
        remove_columns=law_ds.column_names
    )

    law_ds.to_pandas().to_csv("datasets/crafted_dataset_law_v4.csv")


if __name__ == "__main__":
    convert_exported_law_dataset()
