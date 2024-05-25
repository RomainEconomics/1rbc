# 1 Billion Row Challenge

In this repo, I explore the [1 Billion Row Challenge](https://github.com/gunnarmorling/1brc).

The goal of this challenge is to read a 1 Billion row csv file composed of two columns (city and temperature) and perform some basic operations on it (min, max and mean).

If the original challenge is in Java, I will use Python (my main language), as well as Rust (which I'm learning at the moment).

At the moment, my results are as follows:

| Strategy              | Language |   Mean | StdDev | Median |    Min |    Max |
| :-------------------- | :------- | -----: | -----: | -----: | -----: | -----: |
| v6_multi_threading_v1 | Rust     |   4.71 |   0.17 |   4.76 |   4.46 |   4.88 |
| baseline_ibis_duckdb  | Python   |  11.25 |   0.52 |  11.34 |  10.71 |  11.82 |
| baseline_polars       | Python   |  20.18 |  12.76 |  11.81 |  11.63 |  40.37 |
| v5_mmap               | Rust     |  29.85 |   1.12 |  29.34 |  29.27 |  31.84 |
| v5_pypy_mp_v2         | Python   |  34.77 |   9.42 |  32.78 |  24.41 |  46.29 |
| v4_parse_temp         | Rust     |  39.34 |   0.13 |  39.28 |  39.24 |  39.56 |
| v3_fast_float         | Rust     |  41.97 |   0.07 |  41.94 |  41.92 |  42.08 |
| v4_pypy_mp            | Python   |  42.67 |   7.67 |  39.17 |  34.52 |  54.08 |
| v2_faster_hash        | Rust     |  44.32 |   0.15 |  44.28 |  44.19 |   44.5 |
| v1_bytes              | Rust     |  53.73 |   0.78 |  54.14 |   52.4 |   54.3 |
| v0_buffer_reader      | Rust     |  77.43 |   5.76 |  75.23 |  74.19 |  87.68 |
| v3_pypy_temp_parsing  | Python   |  96.24 |   0.55 |  96.32 |  95.52 |  96.81 |
| v2_pypy_bytes         | Python   | 124.39 |   0.78 | 124.15 |  123.7 | 125.73 |
| v1_pypy_list          | Python   | 181.59 |   0.37 | 181.74 | 181.09 |    182 |
| v0_builtin_with_pypy  | Python   | 184.76 |   1.34 | 184.33 | 182.98 | 186.19 |
| baseline_pandas       | Python   | 217.59 |   4.66 | 215.74 | 214.61 | 225.84 |
| v0_builtin            | Python   | 703.82 |   12.6 | 699.51 | 695.57 | 725.97 |

What has been done:

- use plain python and rust
- use some common libraries (pandas, polars, duckdb) to see if we can do better (result is yes, with Rust and using multithreading)
  - polars is actually written in Rust, whereas duckdb is written in C++. But both can be called directly from python, which we do here.
- pypy to speed up python code (by a factor of at least 3)
- bytes instead of string
- faster parsing of temperature
- read file by chunk and distributes over multi process (for python) or over multiple threads (for rust)
- mmap (only in rust)
- hyperfine to measure time and output the different metrics

TBD:

- I'd also like to be able to call rust directly from python (using Maturin and Pyo3)
- learn how to use flamegraph, both with python and with rust

Ressources used to help me with this challenge:

- Rust:
  - [Curious Coding](https://curiouscoding.nl/posts/1brc/)
  - [aminediro](https://aminediro.com/)
- Python:
  - [YT](https://www.youtube.com/watch?v=utTaPW32gKY)

## How to run the code

Since the file is very large, it will be needed to generate it. See 1BRC repo to see how to do so. We will suppose the file in the root of the project and its name will be "measurements.txt".

### For Python

```bash
python -m ven venv
source venv/bin/activate
pip install -r requirements.txt

python -m python.<strategy> measurements.txt
```

### For Rust

For Rust, we need to compile the code first:

```bash
cd rust && cargo build --release
```

Then, we can simply run the code:

```bash
./rust/target/release/<strategy> measurements.txt
```

### To run all strategies

```bash
chmod +x run_expirements.sh
./run_experiments.sh
```

### To format the results

This will generate the markdown table above:

```bash
python format_results.py
```
