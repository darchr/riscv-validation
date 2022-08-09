# Only run this script after compiling the benchmarks
# This script will copy all binaries to ../bins
# It will rename all bench.RISCV files to <benchmark_name>.RISCV

#!/bin/sh

rm -rf ../bins
mkdir ../bins

for exe in $(ls | grep -o -E '^([^.]+)$') ; do
    if [ "$exe" = "LICENSE" ] || [ "$exe" = "Makefile" ]; then
        continue
    fi

    cp $exe ../bins/$exe.RISCV
done
