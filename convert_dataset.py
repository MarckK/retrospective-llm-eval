import datasets
import numpy as np
import os


files_to_process = [
    ("from-sheet_kunvar_jacob-edit_v1.csv", "kunvar_jacob-edit_v1.csv")
]


def convert_exported_dataset(inpath, outpath):
    if not os.path.exists(f"data/datasets/{inpath}.csv"):
        return

    in_ds = datasets.load_dataset(
        "csv", data_files=f"data/datasets/{inpath}.csv"
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

    in_ds.to_pandas().to_csv(f"data/datasets/{outpath}_.csv")


if __name__ == "__main__":
    for inpath, outpath in files_to_process:
        convert_exported_dataset(inpath, outpath)
