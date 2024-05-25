import sys
from .utils import check_true_values

TRUE_VALUES_PATH = "true_values.txt"


if __name__ == "__main__":
    file_path = sys.argv[1]

    cities: dict[str, list] = {}

    with open(file_path, "r") as file:
        for line in file:
            city, temp = line.split(";")
            temp = float(temp)
            if city in cities:
                values = cities[city]
                values[0] = min(values[0], temp)
                values[1] = max(values[1], temp)
                values[2] += temp
                values[3] += 1
            else:
                cities[city] = [temp, temp, temp, 1]

    sorted_keys = sorted(cities.keys())
    res = []

    for city in sorted_keys:
        stat = cities[city]

        min_val = stat[0]
        max_val = stat[1]
        mean_val = round(stat[2] / stat[3], 1)

        res.append(
            (
                city,
                str(min_val),
                str(max_val),
                str(mean_val),
            )
        )

    check_true_values(TRUE_VALUES_PATH, res)
