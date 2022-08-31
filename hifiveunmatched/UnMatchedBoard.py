#Copyright (c) 2022 The Regents of the University of California.
#All Rights Reserved
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

import m5
from m5.objects import *
from m5.util import convert
from os import path
from UnMatchedCacheHierarchy import *
from UnMatchedProcessor import *

class SiFiveUnmatched(System):

    def __init__(self, sbi, disk, cpu_type, num_cpus):
        super(SiFiveUnmatched, self).__init__()

        # Set up the clock domain and the voltage domain
        self.clk_domain = SrcClockDomain()
        self.clk_domain.clock = '3GHz'
        self.clk_domain.voltage_domain = VoltageDomain()
        self.cpu_clk_domain = SrcClockDomain()
        self.cpu_clk_domain.voltage_domain = VoltageDomain()
        self.cpu_clk_domain.clock = '3GHz'

        # DDR memory range starts from base address 0x80000000
        self.mem_ranges = [AddrRange(start=0x80000000, size='16GB')]

         # Create the main memory bus
        # This connects to main memory
        self.membus = SystemXBar(width = 64) # 64-byte width

        self.membus.badaddr_responder = BadAddr()
        self.membus.default = Self.badaddr_responder.pio

        # Set up the system port for functional access from the simulator
        self.system_port = self.membus.cpu_side_ports

        # Create the CPUs for our system.
        self.createCPU(cpu_type, num_cpus)

        # HiFive platform
        # This is based on a HiFive RISCV board and has
        # only a limited number of devices so far i.e.
        # PLIC, CLINT, UART, VirtIOMMIO
        self.platform = HiFive()

        # create and intialize devices currently supported for RISCV
        self.initDevices(self.membus, disk)

        # Create the memory controller
        self.createMemoryControllerDDR4()

        self.setupInterrupts()

        # using RiscvLinux as the base full system workload
        self.workload = RiscvLinux()

        # this is user passed berkeley boot loader binary
        # currently the Linux kernel payload is compiled into this
        # as well
        self.workload.object_file = sbi

        # Generate DTB (from configs/example/riscv/fs_linux.py)
        generateDtb(self)
        self.workload.dtb_filename = path.join(m5.options.outdir, 'device.dtb')
        # Default DTB address if bbl is bulit with --with-dts option
        self.workload.dtb_addr = 0x87e00000


        # Linux boot command flags
        kernel_cmd = [
            "console=ttyS0",
            "root=/dev/vda",
            "ro",
            "cma=512M@0-4G"
        ]
        self.workload.command_line = " ".join(kernel_cmd)

        def createCPU(self, cpu_type, num_cpus):
        # the default cpu will be atomic cpu
            if cpu_type == "atomic":
                self.cpu = [AtomicSimpleCPU(cpu_id = i)
                                for i in range(num_cpus)]
                self.mem_mode = 'atomic'

                for cpu in self.cpu:
                    cpu.createThreads()

            elif cpu_type == "timing":
                self.cpu = [TimingSimpleCPU(cpu_id = i)
                                        for i in range(num_cpus)]
                self.mem_mode = 'timing'
                for cpu in self.cpu:
                    cpu.createThreads()

            elif cpu_type == "minor":
                self.cpu = [U74CPU(cpu_id = i)
                                        for i in range(num_cpus)]
                self.mem_mode = 'timing'
                for cpu in self.cpu:
                    cpu.createThreads()

            elif cpu_type == "o3":
                self.cpu = [DerivO3CPU(cpu_id = i)
                                        for i in range(num_cpus)]
                self.mem_mode = 'timing'
                for cpu in self.cpu:
                    cpu.createThreads()
            else:
                m5.fatal("No CPU type {}".format(cpu_type))

        def switchCpus(self, old, new):
            assert(new[0].switchedOut())
            m5.switchCpus(self, list(zip(old, new)))

            
        self.l2bus = L2XBar()
        self.l2cache = L2Cache()
        self.l2cache.mem_side = self.membus.cpu_side_ports
        self.l2cache.cpu_side = self.l2bus.mem_side_ports

        def setupInterrupts(self):
            for cpu in self.cpu:
                # create the interrupt controller CPU and connect to the membus
                cpu.createInterruptController()

        def createMemoryControllerDDR4(self):
            self.mem_cntrls = [
                MemCtrl(dram = DDR4_2400_8x8(range = self.mem_ranges[0]),
                        port = self.membus.mem_side_ports)
            ]

        def initDevices(self, membus, disk):

            self.iobus = IOXBar()
            

            # Set the frequency of RTC (real time clock) used by
            # CLINT (core level interrupt controller).
            # This frequency is 1MHz in SiFive's U54MC.
            # Setting it to 100MHz for faster simulation (from riscv/fs_linux.py)
            self.platform.rtc = RiscvRTC(frequency=Frequency("100MHz"))

            # RTC sends the clock signal to CLINT via an interrupt pin.
            self.platform.clint.int_pin = self.platform.rtc.int_pin

            # VirtIOMMIO
            image = CowDiskImage(child=RawDiskImage(read_only=True), read_only=False)
            image.child.image_file = disk
            # using reserved memory space
            self.platform.disk = MmioVirtIO(
                vio=VirtIOBlock(image=image),
                interrupt_id=0x8,
                pio_size = 4096,
                pio_addr=0x10008000
            )

            # From riscv/fs_linux.py
            uncacheable_range = [
                *self.platform._on_chip_ranges(),
                *self.platform._off_chip_ranges()
            ]
            # PMA (physical memory attribute) checker is a hardware structure
            # that ensures that physical addresses follow the memory permissions

            # PMA checker can be defined at system-level (system.pma_checker)
            # or MMU-level (system.cpu[0].mmu.pma_checker). It will be resolved
            # by RiscvTLB's Parent.any proxy

            for cpu in self.cpu:
                cpu.mmu.pma_checker =  PMAChecker(uncacheable=uncacheable_range)

            self.bridge = Bridge(delay='50ns')
            self.bridge.mem_side_port = self.iobus.cpu_side_ports
            self.bridge.cpu_side_port = self.membus.mem_side_ports
            self.bridge.ranges = self.platform._off_chip_ranges()

            # Connecting on chip and off chip IO to the mem
            # and IO bus
            self.platform.attachOnChipIO(self.membus)
            self.platform.attachOffChipIO(self.iobus)

            # Attach the PLIC (platform level interrupt controller)
            # to the platform. This initializes the PLIC with
            # interrupt sources coming from off chip devices
            self.platform.attachPlic()

