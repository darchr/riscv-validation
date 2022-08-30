# This script will run all configured benchmarks and place the output CSVs
# in plots/
# Usage: ./run_benchmarks.sh <perf_binary> <microbench_perf_iters> <microbenchmarks_argv[1]>

#!/bin/sh

./scripts/microbench.sh $1 $2
mv -f microbench/perf_microbench.csv ./plots

./scripts/microbenchmarks.sh $1 $3
mv -f microbenchmarks/ayaz_perf_microbenchmarks.csv ./plots
