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
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536
buf_size = 128*1024
c_ubyte_p = POINTER(c_ubyte)

def run():
    rp = lib.rabin_init(
       window_size, avg_segment_size, min_segment_size, max_segment_size)

    # buf = create_string_buffer(buf_size)
    buf = (c_ubyte * buf_size)()
    buf_start = addressof(buf)
    is_new_segment = c_int()

    fh = fopen(fn, "rb")

    total_size = 0
    while True:
        fread_size = fread(buf, 1, buf_size, fh)
        if not fread_size:
            break
        start = 0
        while True:
            bs = cast(buf_start + start, c_ubyte_p)
            size = min(fread_size, buf_size-start)
            blob_size = lib.rabin_segment_next(
                    rp, bs, size, is_new_segment)
            total_size += blob_size
            # print start, blob_size,
            start += blob_size
            # print start, buf_size, is_new_segment
            if start >= buf_size:
                # assert is_new_segment.value == 0
                break
            # assert is_new_segment.value == 1

    lib.rabin_free(byref(rp))
    # print total_size


print timeit.timeit('run()', setup="from __main__ import run",
        number=100)
# run()
