# This script will compile both microbench and microbenchmark-suite
# Produced binaries will be stored in <suite_name>-out directory
# Usage: ./build_all.sh <compiler_binary_name>

#!/bin/sh

CC_RISCV=$1 make -C microbench RISCV -j4
CC=$1 make -C microbenchmark-suite
./microbench/gather_binaries.sh
./microbenchmark-suite/gather_binaries.sh
