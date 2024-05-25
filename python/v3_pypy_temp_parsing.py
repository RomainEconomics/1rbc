import sys
from .utils import check_true_values, format_results, TempStat

TRUE_VALUES_PATH = "true_values.txt"


def parse_temp(temp: bytes) -> int:
    """We suppose that all temperatures are valid and are such that:

    - b"1.3"
    - b"-1.3"
    - b"13.1"
    - b"-13.1"

    We don't handle any other case (b"111.3" would give a bad result for ex).
    """
    temp = temp.strip()
    L = len(temp)

    zero = ord(b"0")

    if L == 5:
        return -((temp[1] - zero) * 100 + (temp[2] - zero) * 10 + (temp[4] - zero))

    if L == 4:
        if temp[0] == 45:  # b"-"
            return -((temp[1] - zero) * 10 + (temp[3] - zero))
        else:
            return (temp[0] - zero) * 100 + (temp[1] - zero) * 10 + (temp[3] - zero)
    if L == 3:
        return (temp[0] - zero) * 10 + (temp[2] - zero)

    raise ValueError(f"Invalid temperature: {temp}")


if __name__ == "__main__":
    file_path = sys.argv[1]

    cities: dict[bytes, TempStat] = {}

    with open(file_path, "rb") as file:
        for idx, line in enumerate(file):
            city, temp = line.split(b";")
            temp = parse_temp(temp)
            if city in cities:
                cities[city].update(temp)
            else:
                cities[city] = TempStat(temp)

    res = format_results(
        cities, integer=True
    )  # The temperatures are now integer, we need to divide them by 10. to compare with the true results
    check_true_values(TRUE_VALUES_PATH, res)
