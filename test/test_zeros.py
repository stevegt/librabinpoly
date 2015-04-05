#!/usr/bin/python

from ctypes import *
import hashlib

import rabinpoly as lib

window_size = 32
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536

rp = lib.rabin_init(
		window_size, avg_segment_size, min_segment_size, max_segment_size)
rpc = rp.contents

buf_size = 512*1024

buf = create_string_buffer(buf_size)

for i in range(buf_size):
	buf[i] = chr(0)
# buf[0] = chr(0x01);

lib.rabin_reset(rp)
i = 0
rc = lib.rabin_in(rp, buf, buf_size)
assert rc == 1
while True:
	if rpc.state & lib.RABIN_IN: 
		rc = lib.rabin_in(rp, buf, 0)
		assert rc == 1
	if rpc.state & lib.RABIN_OUT: 
		rc = lib.rabin_out(rp)
		assert rc == 1
	if rpc.state & lib.PROCESS_FRAGMENT:
		print rpc.inbuf_pos, rpc.inbuf_size, rpc.block_size, rpc.state
		assert rpc.state & lib.PROCESS_BLOCK, rpc.state
		count = rpc.frag_size
		assert count > 0
		assert count == rpc.block_size 
		start = rpc.frag_start
		assert start < buf_size
		assert start + count <= buf_size
		print start, count, 
		assert count == 65536
		h = hashlib.md5(buf[start:start+count]).hexdigest() 
		assert h == 'fcd6bcb56c1689fcef28b57c22475bad'
		print h
		i += 1
	if rpc.state & lib.RABIN_RESET: 
		break

print i
assert i == 8

lib.rabin_free(rp)
