#!/usr/bin/python

# import binascii
from ctypes import *
import hashlib
import random

import rabinpoly as lib

window_size = 32
min_block_size = 1024
avg_block_size = 8192
max_block_size = 65536

rp = lib.rabin_init(
		window_size, avg_block_size, min_block_size, max_block_size)
rpc = rp.contents

random.seed(42)
buf_size = 128*1024
buf = create_string_buffer(buf_size)

mf = open('test/data/pmlog.dat', 'r')

i = 0
hasher = hashlib.md5()
while True:
	if rpc.state & lib.RABIN_IN:
		txt = mf.read(max_block_size)
		buf.value = txt
		rc = lib.rabin_in(rp, buf, len(txt))
		assert rc == 1
	if rpc.state & lib.RABIN_OUT:
		rc = lib.rabin_out(rp)
		assert rc == 1
	if rpc.state & lib.PROCESS_FRAGMENT:
		start = rpc.frag_start
		count = rpc.frag_size
		assert start + count <= buf_size
		hasher.update(buf[start:start+count])
	if rpc.state & lib.PROCESS_BLOCK:
		block_start = rpc.block_start
		size = rpc.block_size
		h = hasher.hexdigest()
		print '(%d, %d, "%s"),' % (block_start, size, h)
		hasher = hashlib.md5()
		i += 1
	if rpc.state & lib.RABIN_RESET:
		assert not mf.read()
		break

print i
assert rpc.state & lib.RABIN_RESET

lib.rabin_free(rp)
