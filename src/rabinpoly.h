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

#include <sys/types.h>

#define RP_IN                   1
#define RP_OUT                  2
#define RP_PROCESS_FRAGMENT     4
#define RP_PROCESS_BLOCK        8
#define RP_RESET               16

typedef struct {
	u_int64_t poly;						// Actual polynomial
	unsigned int window_size;			// in bytes
	size_t avg_block_size;	    // in bytes
	size_t min_block_size;	    // in bytes
	size_t max_block_size;	    // in bytes

	int state;	        

	size_t frag_start;	    // fragment start position in input buffer
	size_t frag_size;	    // size of the current fragment

	size_t block_start;	    // block start position in input stream 
	size_t block_size;	    // size of the current active block 

	unsigned char *inbuf;  				// input buffer
	size_t inbuf_pos;    	// current position in input buffer
	size_t inbuf_size;   	// size of input buffer

	u_int64_t fingerprint;		// current rabin fingerprint
	u_int64_t fingerprint_mask;	// to check if we are at block boundary

	unsigned char *buf;				// circular buffer of size 'window_size'
	unsigned int bufpos;		// current position in circular buffer

  	int shift;
	u_int64_t T[256];		// Lookup table for mod
	u_int64_t U[256];
} RabinPoly;

extern RabinPoly *rp_init(unsigned int window_size,
						size_t avg_block_size, 
						size_t min_block_size,
						size_t max_block_size);
extern void rp_reset(RabinPoly *rp);
extern void rp_free(RabinPoly *rp);
extern int rp_in(RabinPoly *rp, unsigned char *buf, size_t size);
extern int rp_out(RabinPoly *rp);

#endif /* !_RABINPOLY_H_ */

