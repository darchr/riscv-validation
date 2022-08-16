# This script will run all microbenchmarks, and store instructions and cycles
# in a formatted csv file
# to run, symlink this script to the top level directoriy of microbench

#!/bin/sh

echo "Benchmark,instructions,cycles,seconds,ipc,ips" > microbench.csv

for dir in */ ; do
    echo "Running $dir"
    PERF_DATA=$(perf stat -r 1 -e cycles:u,instructions:u -o /dev/stdout $dir/bench.RISCV)

    INSTRUCTIONS=$(echo $PERF_DATA | grep -o -E '[0-9]+ instructions' | grep -o -E '[0-9]+' | tr -d '\n')

    CYCLES=$(echo $PERF_DATA | grep -o -E '[0-9]+ cycles' | grep -o -E '[0-9]+')

    SECONDS=$(echo $PERF_DATA | grep -o -E "[0-9]+.[0-9]+ seconds time elapsed" | grep -o -E '[0-9]+.[0-9]+')

    echo -n $dir,$INSTRUCTIONS,$CYCLES,$SECONDS, | tr -d '/' >> microbench.csv
    python3 -c "print($INSTRUCTIONS/$CYCLES, end=',')" >> microbench.csv
    python3 -c "print($INSTRUCTIONS/$SECONDS)" >> microbench.csv
done
