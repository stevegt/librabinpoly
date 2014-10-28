#!/usr/bin/python

from ctypes import *

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

print Rabinpoly_t.poly
print Rabinpoly_t.buf
print Rabinpoly_t.bufpos
print Rabinpoly_t.shift
print Rabinpoly_t.T

lib = CDLL("librabinpoly.so.0")

window_size = 32
min_segment_size = 1024
avg_segment_size = 8192
max_segment_size = 65536

print lib
lib.rabin_init.restype = POINTER(Rabinpoly_t)
print lib.rabin_init.restype
rp = lib.rabin_init(
		window_size, avg_segment_size, min_segment_size, max_segment_size)
print rp
print rp.contents.window_size
assert rp.contents.window_size == window_size

print rp.contents.T[1]
assert rp.contents.T[1] == 13827942727904890243

lib.rabin_free(byref(rp))
