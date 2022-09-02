# riscv-validation
Scripts/tests/configurations needed for configuring a real RISC-V board in gem5 live here

## Setup
1. Clone darchr/gem5 and this repo.
    ```sh
    git clone https://github.com/darchr/gem5.git gem5_darchr
    git clone https://github.com/darchr/riscv-validation.git
    ```

2. Compile gem5 for RISCV from the REU2022/riscv-validation branch.
    ```sh
    cd gem5_darchr
    git checkout --track origin/REU2022/riscv-validation
    scons build/RISCV/gem5.opt -j<threads>
    ```

3. Compile the benchmarks for RISCV.
    ```sh
    ./build_benchmarks.sh <C_compiler_name>
    ```
    For example, if compiling on a RISCV host running Ubuntu 22.04.
    ```sh
    ./build_benchmarks.sh gcc
    ```
    If compiling on a non-RISCV host with a cross compiler installed.
    ```sh
    ./build_benchmarks.sh riscv64-linux-gnu-gcc
    ```
    This will put all microbench-vertical binaries in microbench_vertical-bins
    and all microbenchmark-suite binaries in microbenchmark_suite-bins.

4. Run all benchmarks on hardware. Pass the perf binary path, number of perf
iterations on microbench-vertical (-r flag for perf), and the command line
argument for microbenchmark-suite binaries as positional arguments 1, 2, and 3
respectively. For example, if you are using the patched kernel that allows for
additional perf events on the HiFive Unmatched:
    ```sh
    ./run_benchmarks.sh ../kernel/linux-5.19.4/tools/perf/perf 10 1000000000
    ```
    This will output perf CSV files into plots/.

5. Run benchmarks on gem5. To run, the board configuration script path and
benchmark binaries path must be passed as an argument to`scripts/gem5_bench.sh`.
The script must be run from the gem5 source directory.
    ```sh
    cd <gem5_source>
    <path_to_scripts_dir>/gem5_bench.sh <gem5_run_sctipt> <bench-bins-dir> <argv_for_binaries>
    ```
    Example:
    ```sh
    cd ~/gem5_darchr
    ../riscv-validation/scripts/gem5_bench.sh configs/example/gem5_library/hifive-run.py ../riscv-validation/microbench-bins
    ../riscv-validation/scripts/gem5_bench.sh configs/example/gem5_library/hifive-run.py ../riscv-validation/microbenchmark_suite-bins 100
    ```
    This will generate microbench_vertical-out/gem5_microbench.csv and
    microbenchmark_suite-out/gem5_microbenchmark_suite.csv containing the stats.

More detailed instructions for gathering data from both hardware and gem5
can be found in [scripts/README.md](scripts/README.md).
