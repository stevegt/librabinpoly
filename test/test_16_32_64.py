#!/usr/bin/python

from ctypes import *
import random

from rabinpoly import *
# http://code.google.com/p/ctypesgen/issues/detail?id=13
CBFUNC = CFUNCTYPE(UNCHECKED(c_int), POINTER(struct_RabinPoly))

class RabinPoly(object):

	def __init__(self, window_size, 
			min_block_size, avg_block_size, max_block_size, buf_size):
		self.rp = rp_new(window_size, 
					avg_block_size, min_block_size, max_block_size, buf_size)
		self.rpc = self.rp.contents
		self.rpc.func_stream_read = CBFUNC(self.stream_read)
		self.rpc.func_block_start = CBFUNC(self.block_start)
		self.filled = False
		self.ctr = 0

	def stream_process(self, stream):
		rp_stream_process(self.rp, stream)

	def stream_read(self, rp):
		if self.filled:
			return -1
		random.seed(42)
		for i in range(self.rpc.buf_size):
			self.rpc.inbuf[i] = random.randrange(0,256)
		self.filled = True
		self.rpc.inbuf_read_count = buf_size
		self.ctr += 1
		print 'read done'
		return 0

	def block_start(self, rp):
		print 'hello'
		self.ctr += 1
		return 0

rp = RabinPoly(
		window_size = 32,
		min_block_size = 16384,
		avg_block_size = 32768,
		max_block_size = 65536,
		buf_size = 512*1024,
	)

rp.stream_process(None)
print rp.ctr


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
