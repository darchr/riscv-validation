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
    This will put all microbench binaries in microbench-bins and all
    microbenchmarks binaries in microbenchmarks-bins.

Setup is now complete. Instructions for gathering data from hardware and gem5
can be found in [scripts/README.md](scripts/README.md).