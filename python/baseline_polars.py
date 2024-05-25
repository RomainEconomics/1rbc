import polars as pl
from .utils import check_true_values

TRUE_VALUES_PATH = "true_values.txt"


if __name__ == "__main__":
    q1 = (
        pl.scan_csv(
            "measurements.txt",
            separator=";",
            has_header=False,
            new_columns=["city", "temp"],
            dtypes=[pl.String, pl.Float32],
        )
        .group_by("city")
        .agg(
            min_val=pl.col("temp").min(),
            max_val=pl.col("temp").max(),
            mean_val=pl.col("temp").mean(),
        )
    )
    df = q1.collect(streaming=True)
    df = df.sort("city")

    format_values = [
        (str(i[0]), str(round(i[1], 1)), str(round(i[2], 1)), str(round(i[3], 1)))
        for i in df.to_pandas().itertuples(index=False, name=None)
    ]

    check_true_values(TRUE_VALUES_PATH, format_values)
