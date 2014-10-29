#!/usr/bin/python

import binascii
from ctypes import *
import random

import rabinpoly

lib = rabinpoly.lib

window_size = 32
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536

rp = lib.rabin_init(
		window_size, avg_segment_size, min_segment_size, max_segment_size)


random.seed(42)
buf_size = 128*1024

buf = (c_ubyte * buf_size)()
# buf = create_string_buffer(buf_size)
print buf
buf_start = addressof(buf)
c_ubyte_p = POINTER(c_ubyte)
is_new_segment = c_int()

for i in range(buf_size):
	buf[i] = random.randrange(0,256)
	# buf[i] = chr(random.randrange(0,256))

start = 0
bs = cast(buf_start + start, c_ubyte_p)
print bs
count = lib.rabin_segment_next(rp, bs, buf_size, is_new_segment)
print count, is_new_segment.value
assert count == 9294
assert is_new_segment.value == 1
start += count

bs = cast(buf_start + start, c_ubyte_p)
print bs
count = lib.rabin_segment_next(rp, bs, buf_size-start, is_new_segment)
print count, is_new_segment.value
assert count == 22416
assert is_new_segment.value == 1
start += count

# short read
bs = cast(buf_start + start, c_ubyte_p)
print bs
count = lib.rabin_segment_next(rp, bs, 10, is_new_segment)
print count, is_new_segment.value
assert count == 10
assert is_new_segment.value == 0
start += count

# resume
bs = cast(buf_start + start, c_ubyte_p)
print bs
count = lib.rabin_segment_next(rp, bs, buf_size-start, is_new_segment)
print count, is_new_segment.value
assert count == 3315
assert is_new_segment.value == 1
start += count

# reset
start -= 3325
lib.rabin_reset(rp)
bs = cast(buf_start + start, c_ubyte_p)
print bs
count = lib.rabin_segment_next(rp, bs, buf_size-start, is_new_segment)
print count, is_new_segment.value
assert count == 3325
assert is_new_segment.value == 1
start += count

lib.rabin_free(byref(rp))
