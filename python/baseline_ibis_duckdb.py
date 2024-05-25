import sys
import ibis
from .utils import check_true_values

TRUE_VALUES_PATH = "true_values.txt"


if __name__ == "__main__":
    file_path = sys.argv[1]

    data = ibis.read_csv(file_path, names=["city", "temp"], sep=";")

    res = (
        data.group_by("city")
        .aggregate(
            min_val=data.temp.min(),
            max_val=data.temp.max(),
            mean_val=data.temp.mean().round(1),
        )
        .order_by("city")
    )

    df = res.to_pandas()

    format_values = [
        (str(i[0]), str(i[1]), str(i[2]), str(i[3]))
        for i in df.itertuples(index=False, name=None)
    ]

    check_true_values(TRUE_VALUES_PATH, format_values)
