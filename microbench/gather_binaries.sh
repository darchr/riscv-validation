# Only run this script after compiling the benchmarks
# This script will copy all binaries to ../microbench-bins
# It will rename all bench.RISCV files to <benchmark_name>.RISCV

#!/bin/sh

cd $(dirname $0)

rm -rf ../microbench-bins
mkdir ../microbench-bins

for dir in */ ; do
    NAME=$(echo -n $dir | tr -d '/')
    cp $NAME/bench.RISCV ../microbench-bins/$NAME.RISCV
done
