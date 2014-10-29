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

lib = CDLL("librabinpoly.so.0")

lib.rabin_init.argtypes = [c_uint, c_uint, c_uint, c_uint]
lib.rabin_init.restype = POINTER(Rabinpoly_t)

lib.rabin_segment_next.argtypes = [
        POINTER(Rabinpoly_t), POINTER(c_ubyte), c_int, POINTER(c_int)]
lib.rabin_segment_next.restype = c_uint

lib.rabin_reset.argtypes = [POINTER(Rabinpoly_t)]

lib.rabin_free.argtypes = [POINTER(POINTER(Rabinpoly_t))]
