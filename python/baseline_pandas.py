import sys
import pandas as pd
from .utils import check_true_values

TRUE_VALUES_PATH = "true_values.txt"

if __name__ == "__main__":
    file_path = sys.argv[1]

    colnames = ["city", "temp"]
    dtypes = {"city": "string", "temp": "float32"}

    final_df = pd.DataFrame(columns=["city", "min", "max", "sum", "count"])

    final_df = final_df.astype(
        {
            "city": "string",
            "min": "float32",
            "max": "float32",
            "sum": "float32",
            "count": "int32",
        }
    )

    for df in pd.read_csv(
        file_path,
        sep=";",
        names=colnames,
        dtype=dtypes,
        chunksize=1_000_000,
    ):
        temp_res = df.groupby("city", as_index=False).agg(
            min=pd.NamedAgg(column="temp", aggfunc="min"),
            max=pd.NamedAgg(column="temp", aggfunc="max"),
            sum=pd.NamedAgg(column="temp", aggfunc="sum"),
            count=pd.NamedAgg(column="temp", aggfunc="count"),
        )
        final_df = (
            pd.concat([final_df, temp_res], axis=0)
            .groupby("city", as_index=False)
            .agg(
                min=pd.NamedAgg(column="min", aggfunc="min"),
                max=pd.NamedAgg(column="max", aggfunc="max"),
                sum=pd.NamedAgg(column="sum", aggfunc="sum"),
                count=pd.NamedAgg(column="count", aggfunc="sum"),
            )
        )

    format_values = [
        (str(i[0]), str(round(i[1], 1)), str(round(i[2], 1)), str(round(i[3])))
        for i in final_df.itertuples(index=False, name=None)
    ]

    check_true_values(TRUE_VALUES_PATH, format_values)
