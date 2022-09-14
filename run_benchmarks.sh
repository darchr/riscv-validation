# This script will run all configured benchmarks and place the output CSVs
# in plots/
# Usage: ./run_benchmarks.sh <perf_binary> <microbench-vertical_perf_iters> <microbenchmark-suite_argv[1]> <microbenchmark-suite mem argv[1]> <microbenchmark-suite mem argv[2]>

#!/bin/sh

./scripts/microbench-vertical.sh $1 $2
mv -f microbench-vertical/perf_microbench_vertical.csv ./plots

./scripts/microbenchmark-suite.sh $1 $3
mv -f perf_microbenchmark_suite.csv ./plots

./scripts/microbenchmark-suite-mem.sh $1 $4 $5
mv -f perf_microbenchmark_suite_mem.csv ./plots
