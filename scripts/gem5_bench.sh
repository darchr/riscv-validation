# this script will run all microbenchmarks on the gem5 hiFive Unmatched Board
# In SE mode and produce a CSV file with stats for instructions, cycles, ipc

# REQUIREMENTS:
# This script must be run from the root gem5 source directory
# The benchmark binaries must be located in directory $2
# the stats will be outputed in <benchmark_suite_name>-out/
# USAGE: ./gem5_bench.sh <path_to_gem5_config_script> <path_to_RISCV_binaries_dir> <argv[1]>
# example:
    # ./gem5_microbench.sh ./src/python/gem5/prebuilt/hifivenew/HiFiveRun.py microbenchmarks 10

#!/bin/sh
run_sim () {
    BENCH=$(basename $2 .RISCV)

    ./build/RISCV/gem5.opt --outdir=$OUTDIR/$BENCH $1 $2 --argv=$3

    INSTRUCTIONS=$(grep board.processor.cores.core.numInsts $OUTDIR/$BENCH/stats.txt | grep -o -E '[0-9]+')
    CYCLES=$(grep numCycles $OUTDIR/$BENCH/stats.txt | grep -o -E '[0-9]+')
    SECONDS=$(grep simSeconds $OUTDIR/$BENCH/stats.txt | grep -o -E '[0-9]+.[0-9]+')
    BRANCHES=$(grep board.processor.cores.core.commitedControl_0::CondCtrl $OUTDIR/$BENCH/stats.txt | grep -o -E '[0-9]+' | tail -n1)
    BRANCH_MISSES=$(grep board.processor.cores.core.branchPred.condIncorrect $OUTDIR/$BENCH/stats.txt | grep -o -E '[0-9]+')

    echo $BENCH,$INSTRUCTIONS,$CYCLES,$SECONDS,$BRANCHES,$BRANCH_MISSES >> $OUTDIR/gem5_$SUITE.csv
}

SUITE=$(basename $2 | cut -d '-' -f1)
OUTDIR=$SUITE-out
mkdir $OUTDIR
echo "Benchmark,instructions,cycles,seconds,branches,branch-misses" > $OUTDIR/gem5_$SUITE.csv

for bin in $2/* ; do
    run_sim $1 $bin $3 &
done

wait
