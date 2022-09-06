# This script will run all microbenchmark-suite binaries, and store instructions
# and cycles in a formatted csv file

# provide the number of repetitions per benchmarks as argument $1

# regex for the loop: https://stackoverflow.com/questions/36743957/how-to-loop-through-files-that-match-a-regular-expression-in-a-unix-shell-script
    # ignore files without extension

#!/bin/sh
cd $(dirname $0)/../microbenchmark-suite

echo "Benchmark,Instructions,Cycles,Seconds,Branches,Branch-misses" > perf_microbenchmark_suite.csv

for exe in $(ls | grep -o -E '^([^.]+)$') ; do
    if [ "$exe" = "LICENSE" ] || [ "$exe" = "Makefile" ]; then
        continue
    fi

    echo Running $exe
    PERF_DATA=$($1 stat -r 1 -e cycles,instructions,branches,branch-misses -o /dev/stdout ./$exe $2)

    INSTRUCTIONS=$(echo $PERF_DATA | grep -o -E '[0-9]+ instructions' | grep -o -E '[0-9]+' | tr -d '\n')
    CYCLES=$(echo $PERF_DATA | grep -o -E '[0-9]+ cycles' | grep -o -E '[0-9]+')
    SEC=$(echo $PERF_DATA | grep -o -E "[0-9]+.[0-9]+ seconds time elapsed" | grep -o -E '[0-9]+.[0-9]+')
    BRANCHES=$(echo $PERF_DATA | grep -o -E '[0-9]+ branches' | grep -o -E '[0-9]+')
    BRANCH_MISSES=$(echo $PERF_DATA | grep -o -E '[0-9]+ branch-misses' | grep -o -E '[0-9]+')

    echo $exe,$INSTRUCTIONS,$CYCLES,$SEC,$BRANCHES,$BRANCH_MISSES >> perf_microbenchmark_suite.csv
done