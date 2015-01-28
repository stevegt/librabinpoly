#!/usr/bin/python

from ctypes import *
import sys
import timeit

sys.path.append('..')
import rabinpoly

fn = sys.argv[1]

lib = rabinpoly.lib
libc = CDLL("libc.so.6")

fopen = libc.fopen
fread = libc.fread
fread.argtypes = [c_void_p, c_size_t, c_size_t, c_void_p]

window_size = 32
min_block_size = 2**14
avg_block_size = 2**15
max_block_size = 2**16
buf_size = max_block_size*2

def run():
    rp = lib.rabin_init(
       window_size, avg_block_size, min_block_size, max_block_size)

    buf = create_string_buffer(buf_size)

    fh = fopen(fn, "rb")

    total_size = 0
    eof = 0
    while not eof:
        fread_size = fread(buf, 1, buf_size, fh)
        if fread_size < buf_size:
            eof = 1
        rc = lib.rabin_in(rp, buf, fread_size, eof)
        assert rc == 0
        while lib.rabin_out(rp):
            frag_size = rp.contents.frag_size
            total_size += frag_size

    lib.rabin_free(byref(rp))
    # print total_size


print timeit.timeit('run()', setup="from __main__ import run",
        number=100)
# run()
