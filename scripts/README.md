# Tracking Stats for Benchmarks run on Hardware and Gem5

This directory contains code and scripts for running various benchmarks and
logging performance statistics on the HiFive Unmatched hardware and gem5 board.

## Microbench
Scripts are provided for running the VRG microbenchmarks on gem5 and hardware.

### Hardware
Make sure that the benchmarks have been
[compiled](../microbench-vertical/README.md) in
`../microbench-vertical`. Then run this script in the microbench-vertical
directory and pass in the path to the perf binary and the number of iterations
that perf should do per benchmark (-r flag for perf).
Perf will automatically report the average for the statistics.
```sh
cd ../microbench
../scripts/microbench-vertical.sh <perf_binary_path> <perf_iterations>
```
This will generate perf\_microbench\_vertical.csv containing the stats.

### GEM5
Make sure that the benchmarks have been
[compiled](../microbench-vertical/README.md).

1. Collect the benchmark binaries into one directory.
    ```sh
    cd ../microbench-vertical
    ./gather_binaries.sh
    cd ../scripts
    ```
    This will put all benchmark binaries in `../microbench_vertical-bins`

2. Copy `gem5_bench.sh` into the root directory of the gem5 source.
    ```sh
    cp gem5_bench.sh <path_to_gem5_source>
    ```

3. Move the binaries into the gem5 source. If the binaries were compiled on
hardware, this will require moving the binaries across from the HiFive Unmatched
to the machine running gem5, if the Unmatched is the host for compilation.
    ```sh
    mv ../microbench_vertical-bins <path_to_gem5_source>/microbench
    ```

4. Change the current working directory to the gem5 directory.
    ```sh
    cd <path_to_gem5_source>
    ```

5. To run, the board configuration script path and benchmark binaries path
must be passed as an argument to `gem5_bench.sh`. For example,
    ```sh
    ./gem5_bench.sh src/python/gem5/prebuilt/hifiveunmatched/hifive-run.py ./microbench_vertical-bins/
    ```
    This will generate microbench_vertical-out/gem5_microbench.csv containing
    the stats.

## Microbenchmark-suite
A Script is provided for running the [aakahlow/microbenchmarks](https://github.com/aakahlow/microbenchmarks) on hardware.

### Hardware
Make sure that the benchmarks have been compiled in `../microbenchmark-suite`
and have been gathered into `../microbenchmark_suite-bins/` using
`../microbenchmark-suite/gather_binaries.sh`. Then run the script.
```sh
cd ../microbenchmark-suite
make -j4
./gather_binaries.sh
../scripts/microbenchmark-suite.sh <perf_binary_path> <benchmark_argv[1]>
```
This will generate perf\_microbenchmark\_suite.csv in the root directory
containing the stats.

### GEM5
Make sure that the benchmarks have been compiled in `../microbenchmark-suite`.

1. Collect the benchmark binaries into one directory.
    ```sh
    cd ../microbenchmark-suite
    ./gather_binaries.sh
    cd ../scripts
    ```
    This will put all benchmark binaries in `../microbenchmark_suite-bins`

2. Copy `gem5_bench.sh` into the root directory of the gem5 source.
    ```sh
    cp gem5_bench.sh <path_to_gem5_source>
    ```

3. Move the binaries into the gem5 source. This may require moving the binaries
across from the HiFive Unmatched to the machine running gem5, if the Unmatched
is the host for compilation.
    ```sh
    mv ../microbenchmark_suite-bins <path_to_gem5_source>/microbenchmark_suite-bins
    ```

4. Change the current working directory to the gem5 directory.
    ```sh
    cd <path_to_gem5_source>
    ```

5. To run, the board configuration script path, benchmark binaries path and the
number of repetitions must be passed as an argument to `gem5_bench.sh`. For
example,
    ```sh
    ./gem5_bench.sh src/python/gem5/prebuilt/hifiveunmatched/hifive-run.py ./microbenchmark-suite_bins/ 1000
    ```
    This will generate microbenchmark_suite-out/gem5_microbenchmark_suite.csv containing the stats.

## Running StatsTrack.py

1. Go into ```../plots/StatsTrack.py``` and add the stat you want to track with the function call ```plot([YOUR STAT])```.

2. Edit ```pd.read_csv()``` to have the path of the .csv files to the gem5 and the perf runs.

3. Edit line 19 and line 38 with the name of the .csv you want the difference stats to write to.

4. Run the file ```python3 StatsTrack.py```.

5. It will generate a graph comparing perf and gem5.

6. It will also generate a .csv with the name you chose which compares your chosen stat as a % difference from gem5.

