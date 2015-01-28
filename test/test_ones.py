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

for i in range(buf_size):
	buf[i] = chr(1)
# buf[0] = chr(0x01);

lib.rabin_reset(rp)
i = 0
rc = lib.rabin_in(rp, buf, buf_size, 1)
assert rc == 0
while True:
	rc = lib.rabin_out(rp)
	assert rc == 1
	assert rp.contents.block_done == 1
	count = rp.contents.frag_size
	assert count > 0
	assert count == rp.contents.block_size 
	start = rp.contents.frag_start
	assert start < buf_size
	assert start + count <= buf_size
	print start, count, 
	assert count == 65536
	h = hashlib.md5(buf[start:start+count]).hexdigest() 
	assert h == 'ae5c932ab2e19291dd20c2c4ac382428'
	print h
	i += 1
	if rp.contents.eof:
		break
print i
assert i == 8

lib.rabin_free(byref(rp))
