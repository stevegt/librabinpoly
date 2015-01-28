#!/usr/bin/python

from ctypes import *
import random


import rabinpoly

lib = rabinpoly.lib

window_size = 32
min_block_size = 16384
avg_block_size = 32768
max_block_size = 65536

rp = lib.rabin_init(
		window_size, avg_block_size, min_block_size, max_block_size)


random.seed(42)
buf_size = 512*1024
print buf_size

buf = create_string_buffer(buf_size)

for i in range(buf_size):
	buf[i] = chr(random.randrange(0,256))

def rnext(start, size, tcount, tdone):
	print start, size,
	bs = cast(addressof(buf) + start, c_char_p)
	rc = lib.rabin_in(rp, bs, size, 0)
	assert rc == 0
	rc = lib.rabin_out(rp)
	assert rc == 1
	count = rp.contents.frag_size
	print count, 
	assert count == tcount
	done = rp.contents.block_done
	print done, 
	assert done == tdone
	print
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
