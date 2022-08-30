# How to create your own Board using the gem5 Standard Library

## Cache Hierarchy
1. Choose a cache hierarchy that is best for your system.
2. Adjust the parameters if the cache already exists in ``gem5.components.cachehierarchies``
3. If the cache hierarchy does not exist, you can create one using ``AbstractCacheHierarchy`` and the specific components that exist in chi, ruby or classic.
4. One thing to note is that if you are changing associativity, you might need to explicitly initialize the cache component, like 

    ```python
    self.l1dcaches = [L1DCache(size=self._l1d_size, assoc=self._l1d_assoc)
                for i in range(board.get_processor().get_num_cores())
            ]
    ```
    in the ```incorporate_cache``` function


## Core

### Creating the Core

1. Choose a CPU that your core is most close to. The current CPU models supported in gem5 are:

    - _SimpleAtomicCPU_, a functional in-order CPU that does not simulate any timing delays.
    - _SimpleTimingCPU_, a functional in-order CPU that simulates timing delays, but not in caches or BP.
    - _MinorCPU_, an in-order CPU that simulates cache level latencies in detail, for caches and BP.
    - _O3CPU_, an out-of-order CPU that simulates cache level latencies in detail, for caches and BP.
    - _KVMCPU_, Kernel-based virtual machine that can only run on x86 and ARM.

2. Add the following import statements to your file

    ```python
    from m5.objects import (
    BaseMMU,
    Port,
    BaseCPU,
    Process,
    )
    from m5.objects.Base{YOUR_CPU_NAME}CPU import *

    ```

3. Go into the source code of your chosen CPU. It can be found in ``src/cpu/{YOUR_CPU_NAME}/Base{YOUR_CPU_NAME}CPU.py``

4. To add a different latency to specific types of instructions, inherit the _DefaultFU_ functions functions in your file and assign the ``opLat`` parameter in those functions as necessary.

5. To bring all the FU functions together, you need to create an _FUPool_ that inherits from the FUPool of your chosen CPU and assign your FU functions as a list to the ``funcUnits`` parameter. As an example:

    ``` python
    class U74FUPool(MinorFUPool):
        funcUnits = [
            U74IntFU(),
            U74IntMulFU(),
            U74IntDivFU()
        ]
    ```

5. To add a branch predictor, navigate to ``src/cpu/pred/BranchPredictor.py``, and choose your branch predictor. If you need to edit some parameters, you can inherit from a branch predictor and do so.

6. To create a core from all your inherited functions, you need to create a CPU that inherits from an ISA-specific version of your chosen CPU. 

    For RISC-V Minor CPU, this CPU is called ``RiscvMinorCPU``. Other CPUs can be found in ``src/arch/{ISA}``.

    In this class, you can also edit the latencies of the pipeline. These parameters are the same as those in ``src/cpu/{YOUR_CPU_NAME}/Base{YOUR_CPU_NAME}CPU.py/Base{YOUR_CPU_NAME}CPU``

    To add your function pool and branch predictor to this CPU:

    ``` python
    executeFuncUnits = {YOUR_FU_POOL}
    branchPred = {YOUR_BP}
    ```

### Adding the Core to the gem5 Standard Library

1. To add your core to the Standard Library, inherit from ``AbstractCore`` from ``gem5.components.processors.abstract_core``, and design it to be similar to SimpleProcessor from ``src/python/gem5/components.processors/simple_core.py``

2. Assign the CPU you created in `self.core` and assign the core_id accepted into the stdlib core as cpu_id in your created core. If your core runs on a specific ISA, it is also recommended to add a requires statement for that ISA.

    ``` python
    self._isa = {ISA}
    requires(isa_required=self._isa)
    self.core = {YOUR_CPU}(cpu_id=core_id)
    ```
     

## Processor



## Board
