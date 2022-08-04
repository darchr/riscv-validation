# Only run this script after compiling the benchmarks
# This script will copy all binaries to ../bins
# It will rename all bench.RISCV files to <benchmark_name>.RISCV

#!/bin/sh

mkdir ../bins

for dir in */ ; do
    NAME=$(echo -n $dir | tr -d '/')
    cp $NAME/bench.RISCV ../bins/$NAME.RISCV
done
