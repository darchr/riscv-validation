## Specs for the HiFive Unmatched

### Cache Hierarchy
- L1D Size : 32kB
- L1D Associativity : 8
- L1I Size : 32kB
- L1I Associativity : 4
- L2 Size : 2MB
- L2 Associativity : 16
- MMU Size : 4kiB

### Memory
- 16GB DDR4 subsystem
- Starting address : 0x80000000

### CPU
- Inherited from MinorCPU
- Latencies: Int inst. (3 cycles), Mul inst. (3 cycles), Mem inst. (3 cycles), Div inst. (6 cycles)

### Board
- Clock Freq.: 1.2 GHz (base: 1.0 GHz, upper limit: 1.5 GHz)
