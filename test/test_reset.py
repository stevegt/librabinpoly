#!/usr/bin/python

import binascii
from ctypes import *
import random

import rabinpoly as lib

window_size = 32
min_block_size = 1024
avg_block_size = 8192
max_block_size = 65536

rp = lib.rp_init(window_size, avg_block_size, min_block_size, max_block_size)

random.seed(42)
buf_size = 128*1024

buf = create_string_buffer(buf_size)

for i in range(buf_size):
	buf[i] = chr(random.randrange(0,256))

start = 0

rc = lib.rp_in(rp, buf, buf_size)
assert rc == 1
rc = lib.rp_out(rp)
assert rc == 1
count = rp.contents.frag_size
print count
assert count == 15848
assert rp.contents.state & lib.RP_PROCESS_BLOCK 
start += count

# short read
lib.rp_reset(rp)
bs = cast(addressof(buf) + start, c_char_p)
print addressof(buf), bs
rc = lib.rp_in(rp, bs, 10)
assert rc == 1
rc = lib.rp_out(rp)
assert rc == 1
count = rp.contents.frag_size
print count
assert count == 10
assert rp.contents.state & lib.RP_PROCESS_BLOCK == 0
start += count

# resume
bs = cast(addressof(buf) + start, c_char_p)
rc = lib.rp_in(rp, bs, buf_size-start)
assert rc == 1
rc = lib.rp_out(rp)
assert rc == 1
count = rp.contents.block_size
print count
assert count == 1132
assert rp.contents.state & lib.RP_PROCESS_BLOCK 

# reset
start -= 10
lib.rp_reset(rp)
bs = cast(addressof(buf) + start, c_char_p)
rc = lib.rp_in(rp, bs, buf_size-start)
assert rc == 1
rc = lib.rp_out(rp)
assert rc == 1
count = rp.contents.frag_size
print count
assert count == 1132
assert rp.contents.state & lib.RP_PROCESS_BLOCK 

lib.rp_free(rp)
