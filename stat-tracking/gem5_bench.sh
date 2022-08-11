# this script will run all microbenchmarks on the gem5 hiFive Unmatched Board
# In SE mode and produce a CSV file with stats for instructions, cycles, ipc

# REQUIREMENTS:
# This script must be run from the root gem5 source directory
# The benchmark binaries must be located in directory $2
# USAGE: ./gem5_microbench.sh <path_to_gem5_config_script> <path_to_RISCV_binaries_dir> <argv[1]>
# example:
    # ./gem5_microbench.sh ./src/python/gem5/prebuilt/hifivenew/HiFiveRun.py microbenchmarks 10

#!/bin/sh

CSV=$(echo $2 | tr -d ./)
echo "Benchmark,instructions,cycles,ipc" > gem5_$CSV.csv

for bin in $2/* ; do
    ./build/RISCV/gem5.opt $1 --riscv_binary=$bin --argv=$3

    echo -n $(basename $bin .RISCV), >> gem5_$CSV.csv

    INSTRUCTIONS=$(grep board.processor.cores.core.numInsts m5out/stats.txt | grep -o -E '[0-9]+')
    echo -n $INSTRUCTIONS, >> gem5_$CSV.csv

    CYCLES=$(grep numCycles m5out/stats.txt | grep -o -E '[0-9]+')
    echo -n $CYCLES, >> gem5_$CSV.csv

    IPC=$(grep ipc m5out/stats.txt | grep -o -E '0.[0-9]+')
    echo $IPC >> gem5_$CSV.csv
done