from m5.ext.pystats.simstat import SimStat
from m5.ext.pystats.jsonserializable import JsonSerializable
from gem5.resources.resource import Resource, CustomResource
from gem5.simulate.simulator import Simulator
from python.gem5.prebuilt.hifiveunmatched.hifive_board import \
    HiFiveBoard

board = HiFiveBoard(clk_freq="1.2GHz", l2_size="2MB", is_fs=False)

board.set_se_binary_workload(
         Resource("riscv-hello")
     )

stats_df = SimStat.to_df()
stats_df.to_csv('stats.csv')

simulator = Simulator(board=board)
simulator.run()