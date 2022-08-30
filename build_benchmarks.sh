# This script will compile both microbench and microbenchmarks
# produced binaries will be stored in <suite_name>-out directory
# Usage: ./build_all.sh <compiler_binary_name>

#!/bin/sh

CC_RISCV=$1 make -C microbench RISCV -j4
CC=$1 make -C microbenchmarks
./microbench/gather_binaries.sh
./microbenchmarks/gather_binaries.sh
