# microbench
This is a fork from darchr/microbench, which itself is a fork from 
VerticalResearchGroup/microbench. This configuration of microbench is
for use with the HiFive Unmatched board running Ubuntu 22.04. All optmization
flags have been removed, including the universal -O3 and local -O1 and -O2 in
benchmarks DP1d, EF, DPcvt, MIP, DP1f. The code for the benchmarks has been
modified to significantly increase the instruction counts. To do this, the
iterations were increased until the IPC change stabliized. Some benchmarks
were removed due to certain issues. The removed benchmarks are, \
CF1: The ROI is not clearly defined by Vertical Research Group. \
CRm: There is a segmentation fault in the original VRG code. \
ML2, ML2\_st, MM, MM\_st, STL2b: increasing iterations was not possible due to
the nature of the code.

To build RISCV binaries for the Unmatched board running Ubuntu 22.04,
```shell
make RISCV -j4
```

The binaries can also be built using a cross compiler on a non-RISCV host by
passing in the name of the cross compiler binary to `make` variable CC\_RISCV,
```shell
CC_RISCV=riscv64-linux-gnu-gcc make RISCV
```

To set the path to RISCV compiler, change `$CC_RISCV` in `make.config` file.  

The binaries are named `bench.RISCV` on each subdirectory.

To run all benchmarks under perf on a RISCV host and generate a CSV with stats,
```shell
../scripts/microbench.sh
```

From the original README file,

> Hi,
> 
> This is an *extremely* simple microbenchmark suite.
> 
> Its intended purpose is in the validation of general purpose out-of-order  
> cores, by targetting individual micro-architectural features or effects.  
> Of course this is by no means an exhaustive collection of necessary bencharks  
> to test every mechanism in an OOO processor.  This is merely a starting point.  
> 
> To use this, you should only need bash, make and python.  
> 
> Configure the versions of the compiler and python (tested with python-2.7):  
> > vim make.config
> 
> To make the benchmarks:  
> > make
> 
> Clean the benchmarks:  
> > make clean
> 
> Describe basically what each benchmark is for:  
> > describe.sh
> 
> Run a benchmark: (no args on any current benchmark)  
> > cd CCa  
> > ./test
> 
> Tony Nowatzki  
> Tuesday, April 14th, 2015  
> 
> PS: Also, some benchmarks use an LFSR setting to get a particular working set.  
> Please see lfsr_settings.txt for example values. (bench ML2 uses this)  
