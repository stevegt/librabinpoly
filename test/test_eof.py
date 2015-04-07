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

rp = lib.rp_init(
		window_size, avg_block_size, min_block_size, max_block_size)
rpc = rp.contents

random.seed(42)
buf_size = max_block_size 

class Mockfile(object):

	def __init__(self):
		self.txt = ''
		self.pos = 0

	def read(self, size):
		txt = self.txt[self.pos:self.pos + size]
		self.pos += len(txt)
		return txt

	def append(self, txt):
		self.txt += txt

def mkmf(size):
	mf = Mockfile()
	for i in range(size):
		mf.append(chr(random.randrange(0,256)))
	return mf

def teof(mf_size):
	mf = mkmf(mf_size)
	eof = 0
	while True:
		if rpc.state & lib.RP_IN:
			txt = mf.read(max_block_size)
			if len(txt) < max_block_size:
				eof = 1
			buf = create_string_buffer(txt)
			rc = lib.rp_in(rp, buf, len(txt))
			assert rc == 1
		if rpc.state & lib.RP_OUT:
			rc = lib.rp_out(rp)
			assert rc == 1
		if rpc.state & lib.RP_RESET:
			assert eof == 1
			break
	lib.rp_reset(rp)

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


lib.rp_free(rp)
