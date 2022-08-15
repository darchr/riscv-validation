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

3. On a HiFive Unmatched board running Ubuntu, clone this repo and
compile the benchmarks.
    ```sh
    git clone https://github.com/darchr/riscv-validation.git
    cd riscv-validation/microbench
    make RISCV -j4
    cd ../microbenchmarks
    make -j4
    ```

Setup is now complete. Instructions for gathering data from hardware and gem5
can be found in [scripts/README.md](scripts/README.md).