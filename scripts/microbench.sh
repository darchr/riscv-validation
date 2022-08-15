# This script will run all microbenchmarks, and store instructions and cycles
# in a formatted csv file
# to run, symlink this script to the top level directoriy of microbench

#!/bin/sh

echo "Benchmark,instructions,cycles,ipc" > microbench.csv

for dir in */ ; do
    PERF_DATA=$(perf stat -r 1 -e cycles:u,instructions:u -o /dev/stdout $dir/bench.RISCV)

    echo -n $dir | tr -d '/' >> microbench.csv
    echo -n "," >> microbench.csv

    INSTRUCTIONS=$(echo $PERF_DATA | grep -o -E '[0-9]+ instructions' | grep -o -E '[0-9]+' | tr -d '\n')
    echo -n $INSTRUCTIONS >> microbench.csv
    echo -n "," >> microbench.csv

    CYCLES=$(echo $PERF_DATA | grep -o -E '[0-9]+ cycles' | grep -o -E '[0-9]+')
    echo -n $CYCLES >> microbench.csv
    echo -n "," >> microbench.csv

    python3 -c "print($INSTRUCTIONS/$CYCLES)" >> microbench.csv
done
