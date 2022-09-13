# Only run this script after compiling the benchmarks
# This script will copy all binaries to ../microbenchmark_suite-bins
# It will rename all bench.RISCV files to <benchmark_name>.RISCV

#!/bin/sh

cd $(dirname $0)

rm -rf ../microbenchmark_suite-bins
mkdir ../microbenchmark_suite-bins

for exe in $(ls | grep -o -E '^([^.]+)$') ; do
    if [ "$exe" = "LICENSE" ] || [ "$exe" = "Makefile" ]; then
        continue
    fi

    cp $exe ../microbenchmark_suite-bins/$exe.RISCV
done
