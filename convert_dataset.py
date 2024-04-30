import datasets
import numpy as np
import os


IN_CSV_LABEL = "jacob"

def convert_exported_dataset():
    if not os.path.exists(f"data/datasets/{IN_CSV_LABEL}.csv"):
        return

    in_ds = datasets.load_dataset(
        "csv", data_files=f"data/datasets/{IN_CSV_LABEL}.csv"
    )["train"]

    in_ds = in_ds.map(lambda x:
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
                    [1] + [0] * sum(bool(x[f"Incorrect{i}"]) for i in range(1, 11)),
                    dtype=np.int32
                )
            ),
        ),
        remove_columns=in_ds.column_names
    )

    in_ds.to_pandas().to_csv(f"data/datasets/crafted_{IN_CSV_LABEL}_new.csv")


if __name__ == "__main__":
    convert_exported_dataset()
