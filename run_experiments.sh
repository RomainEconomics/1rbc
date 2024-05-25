#!/bin/bash

result_dir="results"
file_path="measurements.txt"

mkdir -p "$result_dir/python"
mkdir -p "$result_dir/rust"

# Some of them are very slow to run, and are run 5 times. Comment out the ones that are not needed

declare -a array=(
	"python -m python.baseline_ibis_duckdb $file_path"
	"python -m python.baseline_polars $file_path"
	"python -m python.baseline_pandas $file_path"
	"python -m python.v0_builtin $file_path"
	"pypy -m python.v0_builtin_with_pypy $file_path"
	"pypy -m python.v1_pypy_list $file_path"
	"pypy -m python.v2_pypy_bytes $file_path"
	"pypy -m python.v3_pypy_temp_parsing $file_path"
	"pypy -m python.v4_pypy_mp $file_path 320"
	"pypy -m python.v5_pypy_mp_v2 $file_path 320"
	"./rust/target/release/v1_buffer_reader $file_path"
	"./rust/target/release/v1_bytes $file_path"
	"./rust/target/release/v2_faster_hash $file_path"
	"./rust/target/release/v3_fast_float $file_path"
	"./rust/target/release/v4_parse_temp $file_path"
	"./rust/target/release/v5_mmap $file_path"
	"./rust/target/release/v6_multi_threading_v1 $file_path 320"
)

for cmd in "${array[@]}"; do
	if [[ $cmd == *"python"* ]]; then
		lang="python"
		res=$(awk -F "." '{print $2}' <<<"$cmd")
		filename=$(awk '{print $1}' <<<"$res")
	else
		lang="rust"
		res=$(awk -F " " '{print $1}' <<<"$cmd")
		filename=$(awk -F " " '{print $1}' <<<"$res" | sed 's/.*\///')
	fi
	hyperfine --runs 5 "$cmd" --export-json "$result_dir/$lang/results_$filename.json" --show-output
done
