# this script will run all microbenchmarks on the gem5 hiFive Unmatched Board
# In SE mode and produce a CSV file with stats for instructions, cycles, ipc

# REQUIREMENTS:
# This script must be run from the root gem5 source directory
# The benchmark binaries must be located in ./bins/ and have extension .RISCV
# USAGE: ./gem5_microbench.sh <path_to_gem5_config_script>
# example:
    # ./gem5_microbench.sh ./src/python/gem5/prebuilt/hifivenew/HiFiveRun.py 

#!/bin/sh

echo "Benchmark,instructions,cycles,ipc" > gem5_microbench.csv

for bin in bins/* ; do
    ./build/RISCV/gem5.opt $1 --riscv_binary=$bin

    echo -n $(basename $bin .RISCV), >> gem5_microbench.csv

    INSTRUCTIONS=$(grep board.processor.cores.core.numInsts m5out/stats.txt | grep -o -E '[0-9]+')
    echo -n $INSTRUCTIONS, >> gem5_microbench.csv

    CYCLES=$(grep numCycles m5out/stats.txt | grep -o -E '[0-9]+')
    echo -n $CYCLES, >> gem5_microbench.csv

    IPC=$(grep ipc m5out/stats.txt | grep -o -E '0.[0-9]+')
    echo $IPC >> gem5_microbench.csv
done