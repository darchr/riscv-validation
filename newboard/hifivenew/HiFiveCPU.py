# Copyright (c) 2022 The Regents of the University of California.
# All Rights Reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
import m5
from m5.objects import *
from m5.util import convert
from os import path


# from configs/example/riscv/fs_linux.py

# def generateMemNode(state, mem_range):
#     node = FdtNode("memory@%x" % int(mem_range.start))
#     node.append(FdtPropertyStrings("device_type", ["memory"]))
#     node.append(FdtPropertyWords("reg",
#         state.addrCells(mem_range.start) +
#         state.sizeCells(mem_range.size()) ))
#     return node


# def generateDtb(system):
#     state = FdtState(addr_cells=2, size_cells=2, cpu_cells=1)
#     root = FdtNode('/')
#     root.append(state.addrCellsProperty())
#     root.append(state.sizeCellsProperty())
#     root.appendCompatible(["riscv-virtio"])

#     for mem_range in system.mem_ranges:
#         root.append(generateMemNode(state, mem_range))

#     sections = [*system.cpu, system.platform]

#     for section in sections:
#         for node in section.generateDeviceTree(state):
#             if node.get_name() == root.get_name():
#                 root.merge(node)
#             else:
#                 root.append(node)

#     fdt = Fdt()
#     fdt.add_rootnode(root)
#     fdt.writeDtsFile(path.join(m5.options.outdir, 'device.dts'))
#     fdt.writeDtbFile(path.join(m5.options.outdir, 'device.dtb'))


class U74IntFU(MinorDefaultIntFU):
    opLat = 1


class U74IntMulFU(MinorDefaultIntMulFU):
    opLat = 3


class U74IntDivFU(MinorDefaultIntDivFU):
    opLat = 6  # not implemented 6 or 68 cycles
    # microops or another method to implement division?
    pass


class U74FloatSimdFU(MinorDefaultFloatSimdFU):
    pass


class U74PredFU(MinorDefaultPredFU):
    pass


class U74MemFU(MinorDefaultMemFU):
    opLat = 3


class U74MiscFU(MinorDefaultMiscFU):
    pass


class U74FUPool(MinorFUPool):
    funcUnits = [
        U74IntFU(),
        U74IntFU(),
        U74IntMulFU(),
        U74IntDivFU(),
        U74FloatSimdFU(),
        U74PredFU(),
        U74MemFU(),
        U74MiscFU(),
    ]


class U74BP(TournamentBP):
    BTBEntries = 16
    RASSize = 6
    localHistoryTableSize = 3600

    indirectBranchPred = SimpleIndirectPredictor()
    indirectBranchPred.indirectSets  = 8

# create U74 from SimpleProcessor parent for stdlib compatibility
class U74Processor(SimpleProcessor):
    def __init__(
        self,
        cpu_type,
        num_cores,
    ) -> None:
        super().__init__(
            cpu_type=cpu_type,
            num_cores=num_cores,
            isa=ISA.RISCV,
        )


class U74CPU(BaseMinorCPU):
    fetch1FetchLimit = 2
    fetch1ToFetch2BackwardDelay = 0
    fetch2InputBufferSize = 1
    decodeInputBufferSize = 1
    executeInputBufferSize = 1
    decodeToExecuteForwardDelay = 2
    executeFuncUnits = U74FUPool()
    branchPred = U74BP()
