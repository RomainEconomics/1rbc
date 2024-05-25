import multiprocessing as mp
import itertools
import sys
from .utils import (
    check_true_values,
    find_chunk_boundaries,
    merge_chunks,
    format_results,
    TempStat,
    parse_temp,
)

TRUE_VALUES_PATH = "true_values.txt"


def process_chunk(file_path: str, chunk: tuple[int, int]) -> dict[bytes, TempStat]:
    cities = {}
    with open(file_path, "rb") as file:
        file.seek(chunk[0])
        for line in file:
            if file.tell() >= chunk[1]:
                break

            sep = line.find(b";")
            city, temp = line[:sep], line[sep + 1 :]

            if city in cities:
                cities[city].update(parse_temp(temp))
            else:
                cities[city] = TempStat(parse_temp(temp))

    return cities


if __name__ == "__main__":
    file_path = sys.argv[1]
    num_chunks = int(sys.argv[2])

    chunks = find_chunk_boundaries(file_path, num_chunks)

    with mp.Pool(num_chunks) as pool:
        chunks = pool.starmap(process_chunk, zip(itertools.repeat(file_path), chunks))

    cities = merge_chunks(
        chunks
    )  # note that the typing returs an error because we change the TempStat class

    res = format_results(
        cities, integer=True
    )  # The temperatures are now integer, we need to divide them by 10. to compare with the true results
    check_true_values(TRUE_VALUES_PATH, res)
