#!/usr/bin/python

from ctypes import *
import random

import rabinpoly as lib

window_size = 32
min_block_size = 16384
avg_block_size = 32768
max_block_size = 65536
buf_size = 512*1024
buf = create_string_buffer(buf_size)

rp = lib.rp_init(window_size, 
			avg_block_size, min_block_size, max_block_size)
rpc = rp.contents

random.seed(42)

for i in range(buf_size):
	buf[i] = chr(random.randrange(0,256))

def Split(rp, buf, buf_size):
	while True:
		if rpc.state & lib.RP_IN:
			print rpc.state
			bs = cast(addressof(buf), c_char_p)
			rc = lib.rp_in(rp, bs, buf_size, 0)
			assert rc == 1
		if rpc.state & lib.RP_OUT:
			rc = lib.rp_out(rp)
			assert rc == 1
		if rpc.state & lib.RP_PROCESS_FRAGMENT:
			yield rpc.block_size
		if rpc.state & lib.RP_PROCESS_BLOCK:
			pass
		if rpc.state & lib.RP_RESET:
			return;

refs = [
		(22708, 1),
		(65536, 1),
		(39502, 1),
		(17057, 1),
		(65536, 1),
		(17295, 1),
		(38959, 1),
		(21301, 1),
		(65536, 1),
		(18033, 1),
		(25136, 1),
		(65536, 1),
		(34529, 1),
		(27624, 0),
	]

fragments = Split(rp, buf, buf_size)
for ref in refs:
	length = ref[0]
	block_done = ref[1]
	size = fragments.next()
	assert length == size
	if block_done:
		assert rpc.state & lib.RP_PROCESS_BLOCK 

lib.rp_free(rp)
