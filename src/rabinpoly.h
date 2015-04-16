/* 
 * Copyright (C) 2014 Steve Traugott (stevegt@t7a.org)
 * Copyright (C) 2013 Pavan Kumar Alampalli (pavankumar@cmu.edu)
 * Copyright (C) 2004 Hyang-Ah Kim (hakim@cs.cmu.edu)
 * Copyright (C) 2000 David Mazieres (dm@uun.org)
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
 * USA
 *
 */

/*
 * http://www.umich.edu/~eecs381/handouts/CHeaderFileGuidelines.pdf
 */

#ifndef _RABINPOLY_H_
#define _RABINPOLY_H_ 

#include <stdio.h>
#include <sys/types.h>

typedef struct RabinPoly {
	u_int64_t poly;						// Actual polynomial
	unsigned int window_size;			// in bytes
	size_t avg_block_size;	    // in bytes
	size_t min_block_size;	    // in bytes
	size_t max_block_size;	    // in bytes

	int error;
	FILE *stream;

	unsigned char *fragment_addr;	 // fragment start address
	size_t fragment_size;	    // size of the current fragment

	size_t block_streampos;	    // block start position in input stream 
	size_t block_size;	    // size of the current active block 

	unsigned char *inbuf;  		// input buffer
	size_t inbuf_pos;    	    // current position in input buffer
	size_t inbuf_size;   	    // size of input buffer
	size_t inbuf_read_count;   	// most recently loaded input data byte count

	u_int64_t fingerprint;		// current rabin fingerprint
	u_int64_t fingerprint_mask;	// to check if we are at block boundary

	unsigned char *circbuf;				// circular buffer of size 'window_size'
	unsigned int circbuf_pos;		// current position in circular buffer

  	int shift;
	u_int64_t T[256];		// Lookup table for mod
	u_int64_t U[256];

    int (*func_block_start)(struct RabinPoly*);
    int (*func_block_end)(struct RabinPoly*);
    int (*func_fragment_end)(struct RabinPoly*);
    int (*func_stream_read)(struct RabinPoly*);

} RabinPoly;

extern RabinPoly *rp_new(unsigned int window_size,
						size_t avg_block_size, 
						size_t min_block_size,
						size_t max_block_size,
                        size_t inbuf_size);
extern int rp_stream_process(RabinPoly *rp, FILE *stream);
extern void rp_free(RabinPoly *rp);

#endif /* !_RABINPOLY_H_ */

