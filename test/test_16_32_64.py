#!/usr/bin/python

import binascii
from ctypes import *
import hashlib
import random


import rabinpoly

lib = rabinpoly.lib

window_size = 32
min_segment_size = 16384
avg_segment_size = 32768
max_segment_size = 65536

rp = lib.rabin_init(
		window_size, avg_segment_size, min_segment_size, max_segment_size)


random.seed(42)
buf_size = 512*1024
print buf_size

# buf = (c_ubyte * buf_size)()
buf = create_string_buffer(buf_size)
print buf
buf_start = addressof(buf)
c_ubyte_p = POINTER(c_ubyte)
is_new_segment = c_int()

for i in range(buf_size):
	# buf[i] = random.randrange(0,256)
	buf[i] = chr(random.randrange(0,256))

def rnext(start, size, tcount, tseg):
	skip = min_segment_size - 256
	skip = min(skip, size - 256)
	skip = max(skip, 0)
	skip = 0
	size -= skip
	bs = cast(buf_start + start + skip, c_ubyte_p)
	print start, tcount, start + tcount
	count = lib.rabin_segment_next(rp, bs, size, is_new_segment) + skip
	h = hashlib.md5(buf[start:start+count]).hexdigest() 
	print start, count, skip, is_new_segment.value, h
	assert count == tcount
	assert is_new_segment.value == tseg
	return count

lengths = [
		22708,
		65536,
		39502,
		17057,
		65536,
		17295,
		38959,
		21301,
		65536,
		18033,
		25136,
		65536,
		34529,
	]
start = 0
for length in lengths:
	count = rnext(start, buf_size-start, length, 1)
	start += count

rnext(start, buf_size-start, 27624, 0)

lib.rabin_free(byref(rp))
