#!/usr/bin/python

import binascii
from ctypes import *
import random

class Rabinpoly_t(Structure):
	_fields_ = [
		("poly", c_ulonglong),  # Actual polynomial
		("window_size", c_uint),       # in bytes
		("avg_segment_size", c_uint),  # in KB
		("min_segment_size", c_uint),  # in KB
		("max_segment_size", c_uint),  # in KB

		("fingerprint", c_ulonglong),      # current rabin fingerprint
		("fingerprint_mask", c_ulonglong), # to check if we are at segment boundary

		("buf", POINTER(c_ubyte)),  # circular buffer of size 'window_size'
		("bufpos", c_uint),        # current position in circular buffer
		("cur_seg_size", c_uint),  # tracks size of the current active segment 

		("shift", c_int),
		("T", c_ulonglong * 256),       # Lookup table for mod
		("U", c_ulonglong * 256),
		]

lib = CDLL("librabinpoly.so.0")

window_size = 32
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536

lib.rabin_init.restype = POINTER(Rabinpoly_t)
rp = lib.rabin_init(
		window_size, avg_segment_size, min_segment_size, max_segment_size)


random.seed(42)
buf_size = 128*1024

# buf = (c_ubyte * buf_size)()
buf = create_string_buffer(buf_size)
is_new_segment = c_int()

for i in range(buf_size):
	buf[i] = chr(random.randrange(0,256))

lib.rabin_segment_next.argtypes = [POINTER(Rabinpoly_t),
		# POINTER(c_ubyte), c_int, POINTER(c_int)]
		c_char_p, c_int, POINTER(c_int)]
lib.rabin_segment_next.restype = c_uint

start = 0
count = lib.rabin_segment_next(rp, buf, buf_size, is_new_segment)
print count, is_new_segment.value
assert count == 9294
assert is_new_segment.value == 1
start += count

count = lib.rabin_segment_next(rp, buf[start], buf_size-start, is_new_segment)
print count, is_new_segment.value
assert count == 1302
assert is_new_segment.value == 1
start += count

# short read
count = lib.rabin_segment_next(rp, buf[start], 10, is_new_segment)
print count, is_new_segment.value
assert count == 10
assert is_new_segment.value == 0

# reread
count = lib.rabin_segment_next(rp, buf[start], buf_size-start, is_new_segment)
print count, is_new_segment.value
assert count == 4493
assert is_new_segment.value == 1
start += count




lib.rabin_free(byref(rp))
