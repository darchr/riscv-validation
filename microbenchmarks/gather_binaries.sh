# Only run this script after compiling the benchmarks
# This script will copy all binaries to ../microbenchmarks-bins
# It will rename all bench.RISCV files to <benchmark_name>.RISCV

#!/bin/sh

cd $(dirname $0)

rm -rf ../microbenchmarks-bins
mkdir ../microbenchmarks-bins

for exe in $(ls | grep -o -E '^([^.]+)$') ; do
    if [ "$exe" = "LICENSE" ] || [ "$exe" = "Makefile" ]; then
        continue
    fi

    cp $exe ../microbenchmarks-bins/$exe.RISCV
done
