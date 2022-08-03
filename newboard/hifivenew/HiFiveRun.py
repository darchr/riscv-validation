from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from HiFiveBoard import HiFiveUnmatchedBoard

board = HiFiveUnmatchedBoard()

binary = Resource("riscv-hello")
board.set_se_binary_workload(binary)

simulator = Simulator(board=board)
simulator.run()