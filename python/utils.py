import os
import io

####################################################################################################
## Helper functions for formatting and checking results
####################################################################################################


def format_results(
    cities: dict, integer: bool = False
) -> list[tuple[str, str, str, str]]:
    """The keys will either be strings or bytes. If they are bytes, we convert them to strings."""
    if isinstance(next(iter(cities.keys())), bytes):
        cities = {k.decode(): v for k, v in cities.items()}

    sorted_keys = sorted(cities.keys())
    res = []

    for city in sorted_keys:
        stat = cities[city]

        min_val = stat.min_val
        max_val = stat.max_val
        mean_val = round(stat.mean(), 1)

        if integer:
            min_val /= 10.0
            max_val /= 10.0
            mean_val = round(mean_val / 10.0, 1)

        res.append(
            (
                city,
                str(min_val),
                str(max_val),
                str(mean_val),
            )
        )
    return res


def check_true_values(file_path: str, res: list[tuple[str, str, str, str]]) -> bool:
    true_values = []

    with open(file_path, "r") as f:
        for line in f:
            city, min_val, max_val, mean_val = line.strip().split(";")
            true_values.append((city, min_val, max_val, mean_val))

    check = true_values == res

    print("Check true values: ", check)

    if not check:
        print(res)  # for debugging

    return check


####################################################################################################
# Functions extracted from a script and reused in the following parts
####################################################################################################


class TempStat:
    """Extracted from v0_builtin.py"""

    def __init__(self, temp: float | int):
        self.min_val = temp
        self.max_val = temp
        self.sum_val = temp
        self.count = 1

    def mean(self) -> float:
        return self.sum_val / self.count

    def update(self, temp: float | int):
        self.min_val = min(self.min_val, temp)
        self.max_val = max(self.max_val, temp)
        self.sum_val += temp
        self.count += 1


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


def find_chunk_boundaries(filename: str, chunks: int) -> list[tuple[int, int]]:
    """Extracted from the v5_pypy_mp.py script.

    To be able to parallelize reading the file, we need to give each process its chunk.
    This function, given a number of chunks, will return a list of tuples with the start
    and end for each chunk.

    Note that we can't cut a chunk at any index, otherwise we might break a line.
    Thus we ensure that the end of a chunk is at the end of a line.
    """
    file_size = os.path.getsize(filename)
    chunk_size = file_size // chunks
    chunks_idxs = []

    def find_new_line(f: io.BufferedReader, start: int):
        f.seek(start)
        while True:
            chunk = f.read(2048)
            if b"\n" in chunk:
                return start + chunk.index(b"\n") + 1
            if len(chunk) < 2048:
                return f.tell()
            start += len(chunk)

    with open(filename, "rb") as f:
        start = 0
        for _ in range(chunks):
            end = find_new_line(f, start + chunk_size)
            chunks_idxs.append((start, end))
            start = end
    return chunks_idxs


def merge_chunks(chunks: list[dict[bytes, TempStat]]) -> dict[bytes, TempStat]:
    cities = {}

    for chunk in chunks:
        for city, stat in chunk.items():
            if city in cities:
                cities[city].min_val = min(cities[city].min_val, stat.min_val)
                cities[city].max_val = max(cities[city].max_val, stat.max_val)
                cities[city].sum_val += stat.sum_val
                cities[city].count += stat.count
            else:
                cities[city] = stat

    return cities
