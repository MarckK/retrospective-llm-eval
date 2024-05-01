import datasets
import numpy as np
import os


def convert_exported_dataset(inpath: str, outpath: str) -> bool:
    if not os.path.exists(inpath):
        return False

    in_ds = datasets.load_dataset("csv", data_files=inpath)["train"]

    in_ds = in_ds.map(lambda x:
        dict(
            question=x["Rewritten in style"],
            mc1_targets=dict(
                choices=[
                    x
                    for x in [
                            x["Correct"],
                    ] + [
                        x.get(f"Incorrect{i}")
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

    in_ds.to_pandas().to_csv(outpath)

    return True


if __name__ == "__main__":
    for file in os.listdir("data/datasets"):
        if file.startswith("from-sheet_") and file.endswith(".csv"):
            try:
                newfile = file.replace("from-sheet_", "")
                inpath = f"data/datasets/{file}"
                outpath = f"data/datasets/{newfile}"
                if convert_exported_dataset(inpath, outpath):
                    print(f"Updated {outpath}")
            except Exception as e:
                print(f"Failed to update {file}: {e}")
