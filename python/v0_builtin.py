import sys
from .utils import check_true_values, format_results

TRUE_VALUES_PATH = "true_values.txt"


class TempStat:
    def __init__(self, temp: float):
        self.min_val = temp
        self.max_val = temp
        self.sum_val = temp
        self.count = 1

    def mean(self) -> float:
        return self.sum_val / self.count

    def update(self, temp: float):
        self.min_val = min(self.min_val, temp)
        self.max_val = max(self.max_val, temp)
        self.sum_val += temp
        self.count += 1


if __name__ == "__main__":
    file_path = sys.argv[1]

    cities: dict[str, TempStat] = {}

    with open(file_path, "r") as file:
        for idx, line in enumerate(file):
            city, temp = line.split(";")
            if city in cities:
                cities[city].update(float(temp))
            else:
                cities[city] = TempStat(float(temp))

    res = format_results(cities)
    check_true_values(TRUE_VALUES_PATH, res)
