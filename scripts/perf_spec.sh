# USAGE: ./perf_spec.sh <perf_binary> <spec_input_size>
    # <spec_input_size> can be "test", "train", and "ref"
# depends on gnu-parallel: sudo apt install parallel
# spec must be compiled and initialized with `source shrc`
# Runs benchmarks listed on http://resources.gem5.org/resources/spec-2006 except
# for 416.gamess and 481.wrf due to spec build errors with those benchmarks
# the number of threads is limited to 4, U740 processor has 4 accessible cores

#!/bin/bash

OUTDIR=perf-spec-$2-out
mkdir -p $OUTDIR
echo "Benchmark,Instructions,Cycles,Seconds,Branches,Branch-misses" > $OUTDIR/perf_spec2006_$2.csv

BENCHES="bzip2 gcc bwaves mcf milc zeusmp gromacs cactusADM leslie3d namd gobmk povray calculix hmmer sjeng GemsFDTD libquantum h264ref tonto lbm omnetpp astar sphinx3 998.specrand 999.specrand"

# Run all SPEC 2006 benchmarks in BENCHES
for bench in $BENCHES; do
    $1 stat -e instructions,cycles,branches,branch-misses -o $OUTDIR/$bench.out runspec --size $2 --iterations 1 --noreportable --config riscv.cfg --nobuild $bench
done

# collect statistics
for bench in $OUTDIR/*.out ; do
    INSTRUCTIONS=$(grep -o -E '[0-9]+\s+instructions' $bench | grep -o -E '[0-9]+')
    CYCLES=$(grep -o -E '[0-9]+\s+cycles' $bench | grep -o -E '[0-9]+')
    TIMESEC=$(grep -o -E '[0-9]+.[0-9]+\s?\+?\-?\s?[0-9]+?.?[0-9]+?\s+seconds time elapsed' $bench | grep -o -E '[0-9]+.[0-9]+' | head -n1)
    BRANCHES=$(grep -o -E '[0-9]+\s+branches' $bench | grep -o -E '[0-9]+')
    BRANCH_MISSES=$(grep -o -E '[0-9]+\s+branch-misses' $bench | grep -o -E '[0-9]+')
    echo $(basename --suffix=.out $bench),$INSTRUCTIONS,$CYCLES,$TIMESEC,$BRANCHES,$BRANCH_MISSES >> $OUTDIR/perf_spec2006_$2.csv
done
