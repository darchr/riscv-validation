# This script will run all configured benchmarks and place the output CSVs
# in plots/
# Usage: ./run_benchmarks.sh <perf_binary> <microbench_perf_iters> <microbenchmark-suite_argv[1]>

#!/bin/sh

./scripts/microbench.sh $1 $2
mv -f microbench/perf_microbench.csv ./plots

./scripts/microbenchmark-suite.sh $1 $3
mv -f microbenchmark-suite/perf_microbenchmark_suite.csv ./plots
