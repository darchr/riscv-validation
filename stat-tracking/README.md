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

2. Copy `gem5_bench.sh` into the root directory of the gem5 source.
    ```sh
    cp gem5_bench.sh <path_to_gem5_source>
    ```

3. Move the binaries into the gem5 source. This may require moving the binaries
across from the HiFive Unmatched to the machine running gem5, if the Unmatched
is the host for compilation.
    ```sh
    mv ../bins <path_to_gem5_source>/microbench
    ```

4. Change the current working directory to the gem5 directory.
    ```sh
    cd <path_to_gem5_source>
    ```

5. To run, the board configuration script path and benchmark binaries path
must be passed as an argument to `gem5_bench.sh`. For example,
    ```sh
    ./gem5_bench.sh src/python/gem5/prebuilt/hifiveunmatched/hifive-run.py ./microbench/
    ```
    This will generate gem5_microbench.csv containing the stats.

## Microbenchmarks
A Script is provided for running the [aakahlow/microbenchmarks](https://github.com/aakahlow/microbenchmarks) on hardware.

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

## Running newStatsTrack.py

1. Go into newStatsTrack.py and add the stat you want to track with the function call ```plot([YOUR STAT])```.

2. Edit ```pd.read_csv()``` to have the path of the .csv files to the gem5 and the perf runs.

3. Run the file ```python3 newStatsTrack.py```.

4. It will generate a graph comparing perf and gem5.

5. It will also generate ```statsdump.csv``` which compares your chosen stat as a % difference from gem5.

