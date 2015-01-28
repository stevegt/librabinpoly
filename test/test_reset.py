#!/usr/bin/python

import binascii
from ctypes import *
import random

import rabinpoly

lib = rabinpoly.lib

window_size = 32
min_block_size = 1024
avg_block_size = 8192
max_block_size = 65536

rp = lib.rabin_init(window_size, avg_block_size, min_block_size, max_block_size)

random.seed(42)
buf_size = 128*1024

buf = create_string_buffer(buf_size)

for i in range(buf_size):
	buf[i] = chr(random.randrange(0,256))

start = 0

rc = lib.rabin_in(rp, buf, buf_size, 0)
assert rc == 0
rc = lib.rabin_out(rp)
assert rc == 1
count = rp.contents.frag_size
print count
assert count == 15848
start += count

# short read
bs = cast(addressof(buf) + start, c_char_p)
print addressof(buf), bs
rc = lib.rabin_in(rp, bs, 10, 0)
assert rc == 0
rc = lib.rabin_out(rp)
assert rc == 1
count = rp.contents.frag_size
print count
assert count == 10
assert rp.contents.block_done == 0
start += count

# resume
bs = cast(addressof(buf) + start, c_char_p)
rc = lib.rabin_in(rp, bs, buf_size-start, 0)
assert rc == 0
rc = lib.rabin_out(rp)
assert rc == 1
count = rp.contents.block_size
print count
assert count == 1132
assert rp.contents.block_done == 1

# reset
start -= 10
lib.rabin_reset(rp)
bs = cast(addressof(buf) + start, c_char_p)
rc = lib.rabin_in(rp, bs, buf_size-start, 0)
assert rc == 0
rc = lib.rabin_out(rp)
assert rc == 1
count = rp.contents.frag_size
print count
assert count == 1132
assert rp.contents.block_done == 1

lib.rabin_free(byref(rp))
