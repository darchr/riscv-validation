# Only run this script after compiling the benchmarks
# This script will copy all binaries to ../microbench_vertical-bins
# It will rename all bench.RISCV files to <benchmark_name>.RISCV

#!/bin/sh

cd $(dirname $0)

rm -rf ../microbench_vertical-bins
mkdir ../microbench_vertical-bins

for dir in */ ; do
    NAME=$(echo -n $dir | tr -d '/')
    cp $NAME/bench.RISCV ../microbench_vertical-bins/$NAME.RISCV
done
