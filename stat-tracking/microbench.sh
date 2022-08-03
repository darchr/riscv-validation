# This script will run all microbenchmarks, and store instructions and cycles
# in a formatted csv file
# to run, symlink this script to the top level directoriy of microbench

#!/bin/sh

echo "Benchmark,instructions,cycles" > microbench.csv

for dir in */ ; do
    PERF_DATA=$(perf stat -e cycles:u,instructions:u -o /dev/stdout $dir/bench)
    echo -n $dir | tr -d '/' >> microbench.csv
    echo -n "," >> microbench.csv
    echo $PERF_DATA | grep -o -E '[0-9]+ instructions' | grep -o -E '[0-9]+' | tr -d '\n' >> microbench.csv
    echo -n "," >> microbench.csv
    echo $PERF_DATA | grep -o -E '[0-9]+ cycles' | grep -o -E '[0-9]+' >> microbench.csv
done
