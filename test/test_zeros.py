#!/usr/bin/python

from ctypes import *
import hashlib

import rabinpoly as lib

window_size = 32
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536
buf_size = 512*1024

rp = lib.rp_new(
		window_size, avg_segment_size, min_segment_size,
		max_segment_size, buf_size)
rpc = rp.contents

buf = create_string_buffer(buf_size)

for i in range(buf_size):
	buf[i] = chr(0)
# buf[0] = chr(0x01);

lib.rp_from_buffer(rp, buf, buf_size)

i = 0
while True:
	rc = lib.rp_block_next(rp)
	if (rc):
		break
	assert rpc.block_size == max_segment_size, rpc.block_size
	# http://blogs.skicelab.com/maurizio/ctypes-and-pointer-arithmetics.html
	block_addr = cast(rpc.block_addr, c_void_p).value
	inbuf = cast(rpc.inbuf, c_void_p).value
	block_start = block_addr - inbuf
	block_end = block_start + rpc.block_size
	print block_start, block_end
	block = rpc.inbuf[block_start:block_end]
	block = ''.join(map(chr,block))
	h = hashlib.md5(block).hexdigest() 
	print h
	assert h == 'fcd6bcb56c1689fcef28b57c22475bad'
	i += 1

print i
assert i == 8

lib.rp_free(rp)
