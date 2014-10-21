// $Id$

/* 
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

#ifndef _RABINPOLY_H_
#define _RABINPOLY_H_ 

#include <sys/types.h>
#include <string.h>
#include "dedup.h"

struct rabinpoly {
	u_int64_t poly;					// Actual polynomial
	unsigned int window_size;		// in bytes
	unsigned int avg_segment_size;	// in KB
	unsigned int min_segment_size;	// in KB
	unsigned int max_segment_size;	// in KB


	u_int64_t fingerprint;		// current rabin fingerprint
	u_int64_t fingerprint_mask;	// to check if we are at segment boundary

	u_char *buf;				// circular buffer of size 'window_size'
	unsigned int bufpos;		// current position in ciruclar buffer
	unsigned int cur_seg_size;	// tracks size of the current active segment 

  	int shift;
	u_int64_t T[256];		// Lookup table for mod
	u_int64_t U[256];
};

#endif /* !_RABINPOLY_H_ */
