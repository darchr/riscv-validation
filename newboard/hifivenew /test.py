from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from HiFiveCache import HiFiveCacheHierarchy
from HiFiveCPU import U74CPU


# Obtain the components.
cache_hierarchy = HiFiveCacheHierarchy(
    l1d_size="32kB", l1i_size="32kB", l2_size="2MB"
)
memory = SingleChannelDDR4_2400("16GiB")
processor = SimpleProcessor(cpu_type=U74CPU, num_cores=1)

# Add them to the board.
board = SimpleBoard(
    clk_freq="3GHz", processor=processor, memory=memory, cache_hierarchy=cache_hierarchy
)

# Set the workload.
binary = Resource("x86-hello64-static")
board.set_se_binary_workload(binary)

# Setup the Simulator and run the simulation.
simulator = Simulator(board=board)
simulator.run()