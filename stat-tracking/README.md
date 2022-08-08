# Tracking Stats for Benchmarks run on Hardware and Gem5

This directory contains code and scripts for running various benchmarks and
logging performance statistics on the HiFive Unmatched hardware and gem board.

## Microbench
Scripts are provided for running the VRG microbenchmarks on gem5 and hardware.

### Hardware
Make sure that the benchmarks have been [compiled](../microbench/README.md) in
`../microbench`. Then run this script in the microbench directory.
```sh
cd ../microbench
../stat-tracking/microbench.sh
```
This will generate microbench.csv containing the stats.

### GEM5
Make sure that the board has been [compiled](../newboard/README.md) into gem5
and that the benchmarks have been [compiled](../microbench/README.md).

1. Collect the benchmark binaries into one directory.
    ```sh
    cd ../microbench
    ./gather_binaries.sh
    cd ../stat-tracking
    ```
    This will put all benchmark binaries in `../bins`

2. Copy `gem5_microbench.sh` into the root directory of the gem5 source.
    ```sh
    cp gem5_microbench.sh <path_to_gem5_source>
    ```

3. Move the binaries into the gem5 source.
    ```sh
    mv ../bins <path_to_gem5_source>
    ```

4. Change the current working directory to the gem5 directory.
    ```sh
    cd <path_to_gem5_source>
    ```

5. To run, the board configuration script path must be passed as an argument to
`gem5_microbench.sh`. For example,
    ```sh
    ./gem5_microbench.sh ./src/python/gem5/prebuilt/hifivenew/HiFiveRun.py
    ```
    This will generate gem5_microbench.csv containing the stats.

## Microbenchmarks
A Script are provided for running the [aakahlow/microbenchmarks](https://github.com/aakahlow/microbenchmarks) on hardware.

### Hardware
Make sure that the benchmarks have been compiled in `../microbenchmarks`.
There will be errors compiling some. Ignore them. Then run the script in 
the microbench directory.
```sh
cd ../microbenchmarks
make
../stat-tracking/microbench.sh <repetitions>
```
This will generate microbenchmarks.csv containing the stats.