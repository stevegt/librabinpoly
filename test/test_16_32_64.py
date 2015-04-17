#!/usr/bin/python

from ctypes import *
import random

from rabinpoly import *
# http://code.google.com/p/ctypesgen/issues/detail?id=13
CBFUNC = CFUNCTYPE(UNCHECKED(c_size_t), POINTER(struct_RabinPoly),
		POINTER(c_ubyte), c_size_t)

class Stream(object):
	def __init__(self, size):
		self.size = size
		self.pos = 0
		self.eof = False
		self.buf = ''
		random.seed(42)
	def read(self, rp, dst, size):
		if self.eof:
			rp.contents.error = -1
			return 0
		for i in range(size):
			dst[i] = random.randrange(0,256)
		self.pos += size
		if self.pos == self.size:
			self.eof = True
		return size

window_size = 32
min_block_size = 16384
avg_block_size = 32768
max_block_size = 65536
buf_size = 512*1024

rp = rp_new(window_size, 
		avg_block_size, min_block_size, max_block_size, buf_size)
rpc = rp.contents

stream = Stream(buf_size)
rpc.func_stream_read = CBFUNC(stream.read)
rp_from_stream(rp, None)

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

for ref in refs:
	length = ref[0]
	block_done = ref[1]
	rc = rp_block_next(rp)
	if rc:
		print 'rc', rc
		break
	size = rpc.block_size
	assert length == size, (length, size)

rp_free(rp)
