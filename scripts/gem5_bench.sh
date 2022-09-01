# this script will run all microbenchmarks on the gem5 hiFive Unmatched Board
# In SE mode and produce a CSV file with stats for instructions, cycles, ipc

# REQUIREMENTS:
# This script must be run from the root gem5 source directory
# The benchmark binaries must be located in directory $2
# the stats will be outputed in <benchmark_suite_name>-out/
# USAGE: ./gem5_bench.sh <parallel_threads> <path_to_gem5_config_script> <path_to_RISCV_binaries_dir> <argv[1]>
# example:
    # ./gem5_microbench.sh 1 ./src/python/gem5/prebuilt/hifivenew/HiFiveRun.py microbenchmarks 10

#!/bin/bash

collect_stats () {
    BENCH=$1
    INSTRUCTIONS=$(grep board.processor.cores.core.numInsts $BENCH/stats.txt | grep -o -E '[0-9]+')
    CYCLES=$(grep numCycles $BENCH/stats.txt | grep -o -E '[0-9]+')
    SEC=$(grep simSeconds $BENCH/stats.txt | grep -o -E '[0-9]+.[0-9]+')
    BRANCHES=$(grep board.processor.cores.core.committedControl_0::IsCondControl $BENCH/stats.txt | grep -o -E '[0-9]+' | tail -n1)
    BRANCH_MISSES=$(grep board.processor.cores.core.branchPred.condIncorrect $BENCH/stats.txt | grep -o -E '[0-9]+')

    echo $(basename $BENCH),$INSTRUCTIONS,$CYCLES,$SEC,$BRANCHES,$BRANCH_MISSES >> $OUTDIR/gem5_$SUITE.csv
}

SUITE=$(basename $3 | cut -d '-' -f1)
OUTDIR=$SUITE-out
rm -rf $OUTDIR
mkdir $OUTDIR
echo "Benchmark,instructions,cycles,seconds,branches,branch-misses" > $OUTDIR/gem5_$SUITE.csv

parallel -j$1 ./build/RISCV/gem5.opt --outdir=$OUTDIR/$(basename {} .RISCV) $2 {} --argv=$4 ::: $3/*

# Workaround for GNU parallel not executing `basename` in --outdir flag
for dir in $OUTDIR/$3/*; do
    mv -f $dir $OUTDIR/$(basename $dir .RISCV) 
done
rm -rf $OUTDIR/$3

# Collect stats into CSV file
# Limitation of GNU parallel: Cannot watch CSV populate as script is running
    # Have to wait for all benchmarks to finish before CSV is written to
for bench in $OUTDIR/*/ ; do
    collect_stats $bench
done
