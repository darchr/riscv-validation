# This script will compile both microbench-vertical and microbenchmark-suite
# Produced binaries will be stored in <suite_name>-out directory
# Usage: ./build_all.sh <compiler_binary_name>

#!/bin/sh

CC_RISCV=$1 make -C microbench-vertical RISCV -j4
CC=$1 make -C microbenchmark-suite -j4
./microbench-vertical/gather_binaries.sh
./microbenchmark-suite/gather_binaries.sh
