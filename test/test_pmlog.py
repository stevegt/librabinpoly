#!/usr/bin/python

# import binascii
from ctypes import *
import hashlib

from rabinpoly import *

# import errno
# python's errno module doesn't include EOF
EOF = -1

window_size = 32
min_block_size = 1024
avg_block_size = 8192
max_block_size = 65536
buf_size = 128*1024

rp = rp_new(window_size, 
		avg_block_size, min_block_size, max_block_size, buf_size)
rpc = rp.contents

rp_from_file(rp, 'test/data/pmlog.dat')


i = 0
ref_block_streampos = 0
hasher = hashlib.md5()
while True:
	rc = rp_block_next(rp)
	if (rc):
		assert rc == EOF
		break
	block_size = rpc.block_size
	# http://blogs.skicelab.com/maurizio/ctypes-and-pointer-arithmetics.html
	block_addr = cast(rpc.block_addr, c_void_p).value
	inbuf = cast(rpc.inbuf, c_void_p).value
	block_start = block_addr - inbuf
	block_end = block_start + rpc.block_size
	block = rpc.inbuf[block_start:block_end]
	block = ''.join(map(chr,block))
	h = hashlib.md5(block).hexdigest() 
	block_streampos = rpc.block_streampos
	print '(%d, %d, "%s"),' % (block_streampos, block_size, h)
	# assert hashes[i][0] == block_streampos, hashes[i]
	# assert hashes[i][1] == block_size, hashes[i]
	# assert hashes[i][2] == h, hashes[i]
	# assert ref_block_streampos == block_streampos
	ref_block_streampos += block_size
	i += 1

assert i == 3
assert ref_block_streampos == 196608

rp_free(rp)
