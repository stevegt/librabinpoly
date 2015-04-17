#!/usr/bin/python

# import binascii
from ctypes import *
import random


from rabinpoly import *
# http://code.google.com/p/ctypesgen/issues/detail?id=13
CBFUNC = CFUNCTYPE(UNCHECKED(c_size_t), POINTER(struct_RabinPoly),
		POINTER(c_ubyte), c_size_t)

window_size = 32
min_block_size = 1024
avg_block_size = 8192
max_block_size = 65536
buf_size = max_block_size * 2

rp = rp_new(
		window_size, avg_block_size, min_block_size, max_block_size,
		buf_size)
rpc = rp.contents

random.seed(42)

class Mockfile(object):

	def __init__(self, size):
		self.txt = ''
		self.pos = 0
		for i in range(size):
			self.txt.append(chr(random.randrange(0,256)))

	def read(self, rp, dst, size):
		txt = self.txt[self.pos:self.pos + size]
		self.pos += len(txt)
		return txt

	def append(self, txt):
		self.txt += txt

EOF = -77

class Stream(object):
	def __init__(self, size):
		self.size = size
		self.pos = 0
		self.eof = False
		random.seed(42)
	def read(self, rp, dst, size):
		if self.eof:
			assert (rp.contents.error == EOF)
			return 0
		for i in range(size):
			dst[i] = random.randrange(0,256)
			self.pos += 1
			if self.pos == self.size:
				self.eof = True
				rp.contents.error = EOF
				break
		return i+1

def teof(size):
	stream = Stream(size)
	rp_from_stream(rp, None)
	rpc.func_stream_read = CBFUNC(stream.read)
	total = 0
	while True:
		rc = rp_block_next(rp)
		total += rpc.block_size
		if rc:
			assert rc == EOF
			break
		print size, total
	assert total == size, (total, size)

teof(127)
teof(min_block_size-1)
teof(min_block_size)
teof(min_block_size+1)
teof(1548)
teof(4787)
teof(avg_block_size-1)
teof(avg_block_size)
teof(avg_block_size+1)
teof(9342)
teof(42789)
teof(max_block_size-1)
teof(max_block_size)
teof(max_block_size+1)
teof(82748)


rp_free(rp)
