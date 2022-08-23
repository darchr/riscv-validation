# This script will run all microbenchmarks, and store instructions and cycles
# in a formatted csv file

# provide the number of repetitions per benchmarks as argument $1

# regex for the loop: https://stackoverflow.com/questions/36743957/how-to-loop-through-files-that-match-a-regular-expression-in-a-unix-shell-script
    # ignore files without extension

#!/bin/sh

echo "Benchmark,instructions,cycles,seconds,ipc,ips" > microbenchmarks.csv

for exe in $(ls | grep -o -E '^([^.]+)$') ; do
    if [ "$exe" = "LICENSE" ] || [ "$exe" = "Makefile" ]; then
        continue
    fi

    echo Running $exe
    PERF_DATA=$(perf stat -r 1 -e cycles:u,instructions:u -o /dev/stdout ./$exe $1)

    INSTRUCTIONS=$(echo $PERF_DATA | grep -o -E '[0-9]+ instructions' | grep -o -E '[0-9]+' | tr -d '\n')
    CYCLES=$(echo $PERF_DATA | grep -o -E '[0-9]+ cycles' | grep -o -E '[0-9]+')
    SECONDS=$(echo $PERF_DATA | grep -o -E "[0-9]+.[0-9]+ seconds time elapsed" | grep -o -E '[0-9]+.[0-9]+')

    echo $exe,$INSTRUCTIONS,$CYCLES,$SECONDS >> microbenchmarks.csv
done
