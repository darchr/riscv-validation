# Copyright (c) 2022 The Regents of the University of California
# All rights reserved.
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

import m5
from m5.objects import *
from m5.util import convert
from os import path
from typing import Type


class L1Cache(Cache):
    assoc = 8
    size = '32kB'
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    writeback_clean = True

    def __init__(self):
        super(L1Cache, self).__init__()

class L1DCache(L1Cache):
    assoc = 8
    size = '32kB'
    tag_latency = 1
    data_latency = 1
    response_latency = 1

    def __init__(self):
        super(L1Cache, self).__init__()

class L1ICache(L1Cache):
    assoc = 4
    size = '32kB'
    def __init__(self):
        super(L1Cache, self).__init__()

class L2Cache(Cache):
    assoc = 16
    size = '2MB'
    # tag_latency = 
    # data_latency = 
    # response_latency = 
    # mshrs = 
    # tgts_per_mshr = 
    writeback_clean = False

    def __init__(self):
        super(L2Cache, self).__init__()
        


