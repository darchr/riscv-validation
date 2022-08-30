# This script will run all VRG microbenchmarks, and store instructions, cycles 
# and seconds in a formatted csv file

#!/bin/sh
cd $(dirname $0)/../microbench
echo "Benchmark,instructions,cycles,seconds,branches,branch-misses" > perf_microbench.csv

for dir in */ ; do
    echo "Running $dir"
    PERF_DATA=$($1 stat -r $2 -e cycles,instructions,branches,branch-misses -o /dev/stdout $dir/bench.RISCV)

    INSTRUCTIONS=$(echo $PERF_DATA | grep -o -E '[0-9]+ instructions' | grep -o -E '[0-9]+' | tr -d '\n')

    CYCLES=$(echo $PERF_DATA | grep -o -E '[0-9]+ cycles' | grep -o -E '[0-9]+')

    SECONDS=$(echo $PERF_DATA | grep -o -E "[0-9]+.[0-9]+\s?\+?\-?\s?[0-9]+?.?[0-9]+? seconds time elapsed" | grep -o -E '[0-9]+.[0-9]+' | head -n1)

    BRANCHES=$(echo $PERF_DATA | grep -o -E '[0-9]+ branches' | grep -o -E '[0-9]+')

    BRANCH_MISSES=$(echo $PERF_DATA | grep -o -E '[0-9]+ branch-misses' | grep -o -E '[0-9]+')

    echo $dir,$INSTRUCTIONS,$CYCLES,$SECONDS,$BRANCHES,$BRANCH_MISSES | tr -d '/' >> perf_microbench.csv
done
