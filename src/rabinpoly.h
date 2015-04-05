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

#define RABIN_IN          1
#define RABIN_OUT         2
#define PROCESS_FRAGMENT  4
#define PROCESS_BLOCK     8
#define RABIN_RESET      16

// XXX remove struct name
// XXX change most of these to size_t
struct rabinpoly {
	u_int64_t poly;						// Actual polynomial
	unsigned int window_size;			// in bytes
	unsigned long avg_block_size;	    // in bytes
	unsigned long min_block_size;	    // in bytes
	unsigned long max_block_size;	    // in bytes

	int state;	        

	unsigned long frag_start;	    // fragment start position in input buffer
	unsigned long frag_size;	    // size of the current fragment

	unsigned long block_start;	    // block start position in input stream 
	unsigned long block_size;	    // size of the current active block 

	u_char *inbuf;  				// input buffer
	unsigned long inbuf_pos;    	// current position in input buffer
	unsigned long inbuf_size;   	// size of input buffer

	u_int64_t fingerprint;		// current rabin fingerprint
	u_int64_t fingerprint_mask;	// to check if we are at block boundary

	u_char *buf;				// circular buffer of size 'window_size'
	unsigned int bufpos;		// current position in circular buffer

  	int shift;
	u_int64_t T[256];		// Lookup table for mod
	u_int64_t U[256];
};
// XXX rename rabinpoly_t, move to tail of struct decl 
typedef struct rabinpoly rabinpoly_t;


extern rabinpoly_t *rabin_init(unsigned int window_size,
						unsigned long avg_block_size, 
						unsigned long min_block_size,
						unsigned long max_block_size);
extern void rabin_reset(rabinpoly_t *rp);
extern void rabin_free(rabinpoly_t *rp);
extern int rabin_in(rabinpoly_t *rp, u_char *buf, unsigned long size);
extern int rabin_out(rabinpoly_t *rp);

#endif /* !_RABINPOLY_H_ */
















