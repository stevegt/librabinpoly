''' 
Copyright (C) 2014 Steve Traugott (stevegt@t7a.org)
 
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA 

'''








from ctypes import *

import os
# print os.environ['LD_LIBRARY_PATH']

class Rabinpoly_t(Structure):
	_fields_ = [
		("poly", c_ulonglong),  # Actual polynomial
		("window_size", c_uint),        # in bytes
		("avg_block_size", c_ulong),  # in bytes
		("min_block_size", c_ulong),  # in bytes
		("max_block_size", c_ulong),  # in bytes

		("block_start", c_ulong),  # block start position in input stream 
		("block_size", c_ulong),   # size of the current active block 
		("block_done", c_int),     # 1 if current block is complete, else 0

		("inbuf", c_char_p),  		# input buffer
		("inbuf_pos", c_ulong),  	# current position in input buffer
		("inbuf_size", c_ulong),  	# size of input buffer
		("frag_start", c_ulong),  	# fragment start position 
		("frag_size", c_ulong),  	# size of current fragment

		("eof_in", c_int), 			# 1 if input is at eof, else 0
		("eof", c_int), 			# 1 if output is at eof, else 0
	
		("fingerprint", c_ulonglong),      # current rabin fingerprint
		("fingerprint_mask", c_ulonglong), 
									# to check if we are at block boundary

		("buf", POINTER(c_ubyte)),  # circular buffer of size 'window_size'
		("bufpos", c_uint),         # current position in circular buffer

		("shift", c_int),
		("T", c_ulonglong * 256),       # Lookup table for mod
		("U", c_ulonglong * 256),
		]

lib = CDLL("librabinpoly.so.0")

lib.rabin_init.argtypes = [c_uint, c_ulong, c_ulong, c_ulong]
lib.rabin_init.restype = POINTER(Rabinpoly_t)

lib.rabin_in.argtypes = [
        POINTER(Rabinpoly_t), c_char_p, c_ulong, c_int]
lib.rabin_in.restype = c_int

lib.rabin_out.argtypes = [POINTER(Rabinpoly_t)]
lib.rabin_out.restype = c_int

lib.rabin_reset.argtypes = [POINTER(Rabinpoly_t)]

lib.rabin_free.argtypes = [POINTER(POINTER(Rabinpoly_t))]


