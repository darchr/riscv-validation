from HiFiveCache import HiFiveCacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.utils.requires import requires
from gem5.isas import ISA

requires(isa_required=ISA.RISCV)

cache_hierarchy = HiFiveCacheHierarchy(l1d_size='32kB', l1i_size='32kB', l2_size='2MB')
memory = SingleChannelDDR4_2400('16GB')
