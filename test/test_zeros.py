#!/usr/bin/python

from ctypes import *
import hashlib

import rabinpoly

lib = rabinpoly.lib

window_size = 32
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536

rp = lib.rabin_init(
		window_size, avg_segment_size, min_segment_size, max_segment_size)

buf_size = 512*1024

buf = create_string_buffer(buf_size)
buf_start = addressof(buf)
c_ubyte_p = POINTER(c_ubyte)
is_new_segment = c_int()

for i in range(buf_size):
	buf[i] = chr(0)
# buf[0] = chr(0x01);

lib.rabin_reset(rp)
start = 0
i = 0
while True:
	bs = cast(buf_start + start, c_ubyte_p)
	count = lib.rabin_segment_next(rp, bs, buf_size-start, is_new_segment)
	assert count == 65536
	h = hashlib.md5(buf[start:start+count]).hexdigest() 
	assert h == 'fcd6bcb56c1689fcef28b57c22475bad'
	print start, count, is_new_segment.value, h
	start += count
	assert start <= buf_size
	if start == buf_size:
		break
	i += 1
print i
assert i == 7

lib.rabin_free(byref(rp))
