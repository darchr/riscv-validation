# This script will run all memory microbenchmark-suite binaries, and store
# instruction counts and cycle counts in a formatted csv file

# provide the path to the perf binary as argument $1
# provide the number of repetitions per benchmarks as argument $2
# provide the array size as argument $3

#!/bin/sh

cd $(dirname $0)/..

echo "Benchmark,Instructions,Cycles,Seconds,Branches,Branch-misses" > perf_microbenchmark_suite_mem.csv

for exe in microbenchmark_suite_mem-bins/* ; do
    echo Running $(basename $exe)
    PERF_DATA=$($1 stat -r 1 -e cycles,instructions,branches,branch-misses -o /dev/stdout ./$exe $2 $3)

    INSTRUCTIONS=$(echo $PERF_DATA | grep -o -E '[0-9]+ instructions' | grep -o -E '[0-9]+' | tr -d '\n')
    CYCLES=$(echo $PERF_DATA | grep -o -E '[0-9]+ cycles' | grep -o -E '[0-9]+')
    SEC=$(echo $PERF_DATA | grep -o -E "[0-9]+.[0-9]+ seconds time elapsed" | grep -o -E '[0-9]+.[0-9]+')
    BRANCHES=$(echo $PERF_DATA | grep -o -E '[0-9]+ branches' | grep -o -E '[0-9]+')
    BRANCH_MISSES=$(echo $PERF_DATA | grep -o -E '[0-9]+ branch-misses' | grep -o -E '[0-9]+')

    echo $exe,$INSTRUCTIONS,$CYCLES,$SEC,$BRANCHES,$BRANCH_MISSES >> perf_microbenchmark_suite_mem.csv
done
