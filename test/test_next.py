#!/usr/bin/python

# import binascii
from ctypes import *
import hashlib
import random


import rabinpoly as lib

window_size = 32
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536

rp = lib.rp_init(
		window_size, avg_segment_size, min_segment_size, max_segment_size)
rpc = rp.contents

random.seed(42)
buf_size = 128*1024
print buf_size

buf = create_string_buffer(buf_size)
print buf

for i in range(buf_size):
	# buf[i] = random.randrange(0,256)
	buf[i] = chr(random.randrange(0,256))

def tnext(tcount, tdone):
	rc = lib.rp_out(rp)
	assert rc == 1
	if tdone:
		assert rpc.state & lib.RP_PROCESS_BLOCK 
	count = rpc.block_size
	assert count == tcount

def ptr_add(ptr, x):
	addr = cast(ptr, c_void_p)
	addr.value += x
	return cast(addr, type(ptr))

rc = lib.rp_in(rp, buf, buf_size, 1)
assert rc == 1

tnext(15848, 1)
tnext(1132, 1)
tnext(5728, 1)
tnext(10064, 1)

# relocate
lib.rp_reset(rp)
dst = addressof(buf)
src = addressof(buf) + 15848
count = 1132
memmove(dst, src, count)
rc = lib.rp_in(rp, buf, buf_size)
assert rc == 1
tnext(1132, 1)

# run it out
print
lib.rp_reset(rp)
rc = lib.rp_in(rp, buf, buf_size)
assert rc == 1
i = 0
while True:
	rc = lib.rp_out(rp)
	if rpc.state & lib.RP_RESET: 
		break
	assert rc == 1
	count = rpc.block_size
	assert rpc.state & lib.RP_PROCESS_FRAGMENT, rpc.state
	start = rpc.frag_start
	h = hashlib.md5(buf[start:start+count]).hexdigest() 
	print start, count, h
	i += 1
	if rpc.state & lib.RP_IN: 
		rc = lib.rp_in(rp, buf, 0)
		assert rc == 1

print i
assert i == 19

lib.rp_free(rp)
