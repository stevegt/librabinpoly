#!/usr/bin/python

from ctypes import *
import sys
import timeit

sys.path.append('..')
import rabinpoly as lib

fn = sys.argv[1]

libc = CDLL("libc.so.6")

fopen = libc.fopen
fread = libc.fread
feof = libc.feof
fread.argtypes = [c_void_p, c_size_t, c_size_t, c_void_p]

window_size = 32
min_block_size = 2**14
avg_block_size = 2**15
max_block_size = 2**16
buf_size = max_block_size*2

def run():
    rp = lib.rp_init(
       window_size, avg_block_size, min_block_size, max_block_size)
    rpc = rp.contents

    buf = create_string_buffer(buf_size)

    fh = fopen(fn, "rb")

    total_size = 0
    while True:
        if rpc.state & lib.RP_IN:
            fread_size = fread(buf, 1, buf_size, fh)
            rc = lib.rp_in(rp, buf, fread_size)
            assert rc == 1
        if rpc.state & lib.RP_OUT:
            rc = lib.rp_out(rp)
            assert rc == 1
            total_size += rpc.frag_size
        if rpc.state & lib.RP_RESET:
            assert feof(fh)
            break

    lib.rp_free(rp)
    print total_size


print timeit.timeit('run()', setup="from __main__ import run",
        number=100)
# run()
