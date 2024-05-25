import os
import io
import sys
import itertools
import multiprocessing as mp
from .utils import check_true_values, format_results, TempStat


TRUE_VALUES_PATH = "true_values.txt"


def find_chunk_boundaries(filename: str, workers: int) -> list[tuple[int, int]]:
    file_size = os.path.getsize(filename)
    chunk_size = file_size // workers
    chunks = []

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
        for _ in range(workers):
            end = find_new_line(f, start + chunk_size)
            chunks.append((start, end))
            start = end
    return chunks


def process_chunk(file_path: str, chunk: tuple[int, int]) -> dict[bytes, TempStat]:
    cities = {}
    with open(file_path, "rb") as file:
        file.seek(chunk[0])
        for line in file:
            if file.tell() >= chunk[1]:
                break

            city, temp = line.split(b";")
            if city in cities:
                cities[city].update(float(temp))
            else:
                cities[city] = TempStat(float(temp))

    return cities


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


if __name__ == "__main__":
    file_path = sys.argv[1]
    num_chunks = int(sys.argv[2])

    chunks = find_chunk_boundaries(file_path, num_chunks)

    with mp.Pool(num_chunks) as pool:
        chunks = pool.starmap(process_chunk, zip(itertools.repeat(file_path), chunks))

    cities = merge_chunks(chunks)

    res = format_results(cities)
    check_true_values(TRUE_VALUES_PATH, res)
