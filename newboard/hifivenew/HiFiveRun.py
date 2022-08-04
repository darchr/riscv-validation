import argparse
from gem5.resources.resource import Resource, CustomResource
from gem5.simulate.simulator import Simulator
from HiFiveBoard import HiFiveUnmatchedBoard

# collect optional CLI arg for RISCV binary to run
parser = argparse.ArgumentParser(description="Binary to run on system")
parser.add_argument(
    "--riscv_binary", type=str, help="The RISCV binary to execute on the CPU",
    default="riscv-hello",
)
args = parser.parse_args()

board = HiFiveUnmatchedBoard()

# run default binary if no binary provided, otherwise run CLI provided resource
if args.riscv_binary == "riscv-hello":
    board.set_se_binary_workload(
        Resource(args.riscv_binary)
    )
else:
    board.set_se_binary_workload(
        CustomResource(args.riscv_binary)
    )

simulator = Simulator(board=board)
simulator.run()