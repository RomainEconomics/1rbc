import sys
from .utils import check_true_values, format_results, TempStat

TRUE_VALUES_PATH = "true_values.txt"

if __name__ == "__main__":
    file_path = sys.argv[1]

    cities: dict[bytes, TempStat] = {}

    with open(file_path, "rb") as file:
        for idx, line in enumerate(file):
            city, temp = line.split(b";")
            if city in cities:
                cities[city].update(float(temp))
            else:
                cities[city] = TempStat(float(temp))

    res = format_results(cities)
    check_true_values(TRUE_VALUES_PATH, res)
