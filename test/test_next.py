#!/usr/bin/python

import binascii
from ctypes import *
import hashlib
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
	bs = cast(buf_start + start, c_ubyte_p)
	count = lib.rabin_segment_next(rp, bs, size, is_new_segment)
	h = hashlib.md5(buf[start:start+count]).hexdigest() 
	print start, count, is_new_segment.value, h
	assert count == tcount
	assert is_new_segment.value == tseg
	return count

start = 0
count = rnext(start, buf_size, 15848, 1)
start += count

count = rnext(start, buf_size-start, 1132, 1)
start += count

# short read
count = rnext(start, 10, 10, 0)

# reread
count = rnext(start, buf_size-start, 5728, 1)
start += count

# continue
count = rnext(start, buf_size-start, 10064, 1)
start += count

# relocate
lib.rabin_reset(rp)
dst = buf_start
src = buf_start + 15848
count = 1132
memmove(dst, src, count)
count = rnext(0, buf_size, 1132, 1)
start += count

# run it out
print
lib.rabin_reset(rp)
start = 0
i = 0
while True:
	bs = cast(buf_start + start, c_ubyte_p)
	count = lib.rabin_segment_next(rp, bs, buf_size-start, is_new_segment)
	h = hashlib.md5(buf[start:start+count]).hexdigest() 
	print start, count, is_new_segment.value, h
	start += count
	if start < buf_size:
		assert is_new_segment.value == 1
	else:
		assert is_new_segment.value == 0
		break
	i += 1
print i
assert i == 18

lib.rabin_free(byref(rp))
