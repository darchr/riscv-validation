from HiFiveCache import HiFiveCacheHierarchy
from HiFiveCPU import U74CPU
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.utils.requires import requires
from gem5.isas import ISA
from gem5.components.boards.simple_board import SimpleBoard
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.memory.memory import ChanneledMemory


requires(isa_required=ISA.RISCV)

cache_hierarchy = HiFiveCacheHierarchy(
    l1d_size="32kB", l1i_size="32kB", l2_size="2MB"
)
memory = SingleChannelDDR4_2400("16GB")

## [AddrRange(start=0x80000000, size='1024MB')]
processor = SimpleProcessor(cpu_type=CPUTypes.MINOR, num_cores=4)

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
binary = Resource("riscv-hello")
board.set_se_binary_workload(binary)

simulator = Simulator(board=board)
simulator.run()
