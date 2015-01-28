#!/usr/bin/python

# import binascii
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

buf = create_string_buffer(buf_size)
print buf

for i in range(buf_size):
	# buf[i] = random.randrange(0,256)
	buf[i] = chr(random.randrange(0,256))

def tnext(tcount, tdone):
	rc = lib.rabin_out(rp)
	assert rc == tdone
	count = rp.contents.block_size
	block_done = rp.contents.block_done
	print count, block_done
	assert count == tcount
	assert block_done == tdone

def ptr_add(ptr, x):
	addr = cast(ptr, c_void_p)
	addr.value += x
	return cast(addr, type(ptr))

rc = lib.rabin_in(rp, buf, buf_size, 1)
assert rc == 0

tnext(15848, 1)
tnext(1132, 1)
tnext(5728, 1)
tnext(10064, 1)

# relocate
lib.rabin_reset(rp)
dst = addressof(buf)
src = addressof(buf) + 15848
count = 1132
memmove(dst, src, count)
rc = lib.rabin_in(rp, buf, buf_size, 1)
assert rc == 0
tnext(1132, 1)

# run it out
print
lib.rabin_reset(rp)
rc = lib.rabin_in(rp, buf, buf_size, 1)
assert rc == 0
i = 0
while True:
	rc = lib.rabin_out(rp)
	assert rc == 1
	count = rp.contents.block_size
	block_done = rp.contents.block_done
	start = rp.contents.frag_start
	h = hashlib.md5(buf[start:start+count]).hexdigest() 
	print start, count, block_done, h
	assert block_done == 1
	i += 1
	if rp.contents.eof:
		break
print i
assert i == 19

lib.rabin_free(byref(rp))
