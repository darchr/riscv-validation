# This script will remove all RISC-V binaries

#!/bin/sh

make -C microbench-vertical clean
make -C microbenchmark-suite clean
rm -rf microbench_vertical-bins microbenchmark_suite-bins
