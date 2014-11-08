#!/usr/bin/python

from ctypes import *
import hashlib
import random


import rabinpoly

lib = rabinpoly.lib

window_size = 32
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536

rp = lib.rabin_init(
		window_size, avg_segment_size, min_segment_size, max_segment_size)


random.seed(42)
buf_size = 128*1024

buf = create_string_buffer(buf_size)
buf_start = addressof(buf)
c_ubyte_p = POINTER(c_ubyte)

for i in range(buf_size):
	buf[i] = chr(random.randrange(0,256))
	# buf[i] = 'a'

lengths = [
		15848,
		1132,
		5728,
		10064,
		20295,
		1091,
		4336,
		1514,
		4938,
		13019,
		3910,
		3146,
		5636,
		22865,
		5237,
		8987,
		1263,
		2063,
		]

leni = 0
def callback(rp, buf, size, is_eof):
	global leni
	b = buffer(buf, 0, size)
	h = hashlib.md5(b).hexdigest() 
	print "callback: %d %s" % (size, h)
	assert size == lengths[leni]
	leni += 1
	return 0

cbfunc = rabinpoly.cbfunc_t(callback)

start = 0
bs = cast(buf_start + start, c_ubyte_p)
is_eof = 1
lib.rabin_write(rp, bs, buf_size, is_eof, cbfunc)
print leni
assert leni == 18

lib.rabin_free(byref(rp))
