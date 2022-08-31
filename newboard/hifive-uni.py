from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from python.gem5.prebuilt.hifiveunmatched.hifive_b import HiFiveBoard


board = HiFiveBoard("1.2GHz", "2MB", True)

command =  "echo 'This is running on U74 CPU core.';" \
        + "sleep 1;" \
        + "m5 exit;"

board.set_kernel_disk_workload(
    kernel=Resource("riscv-bootloader-vmlinux-5.10"),
    disk_image=Resource("riscv-ubuntu-20.04-img"),
    readfile_contents=command,
)

#board.set_se_binary_workload(
#    Resource("riscv-hello")
#)

simulator = Simulator(
    board=board
)
simulator.run()