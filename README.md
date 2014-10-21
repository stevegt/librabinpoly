libdedup
========

Rabin fingerprinting and deduplication library in C.

History
-------

(Please send me pull requests for any corrections or additional
information anyone wants to add here.  I want to set the record
straight, but also think that understanding the history helps with
understanding the code.)

It all started with Michael O. Rabin's 1981 paper "Fingerprinting by
Random Polynomials", TR-15-81, Harvard University.  (As of this
writing, a copy of the paper can be found at
http://www.xmailserver.org/rabin.pdf.)

The earliest implementation I know of is the 1999 code by David
Mazieres (dm@uun.org) for the Low-Bandwidth File System project:

http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.28.8654 

The authoritative location for LBFS and SFS appears to be
http://pdos.csail.mit.edu/lbfs/dist.html.  The LBFS CVS server is
down, but the CVS repository is archived at http://www.fs.net/.  

David's rabinpoly implementation in SFS is written in C++.  I don't
know if this is his first implementation, or if David wrote an earlier
version in C.  Later implementations crediting David are found in both
C and C++. 

In 2003-2005, Hyang-Ah Kim (hakim@cs.cmu.edu) packaged and re-released
rabinpoly, adding support for a configurable sliding window size. Her
code can be found at http://www.cs.cmu.edu/~hakim/software/.  This
version is in C++.

In her README, Hyang-Ah mentions earlier modifications, including a
conversion to standalone, by Niraj Tolia et al.  I haven't found a
copy of Niraj's version yet.

In 2013, Pavan Kumar Alampalli (pavankumar@cmu.edu,
http://www.pdl.cmu.edu/People/pavan.shtml) credits Hyang-Ah in a
pure-C version he worked on.  I'm not yet sure who did the port to C.  

Pavan's version was used for Greg Ganger's 15-746/18-746 Storage
Systems course at CMU (http://www.ece.cmu.edu/~ganger).  The code can
be found at
http://www.ece.cmu.edu/~ganger/746.spring13/projects/proj2_fuse/746-handout/src/dedup-lib/.

More history details can be found at
https://github.com/wurp/rabin-tool/blob/master/README.

A tantalyzing C version can be found in an 2006 version of git source,
at http://www.gelato.unsw.edu.au/archives/git/att-18872/rabinpoly.c --
I don't know yet where or if this fits into the family tree.  


Other rabinpoly libraries
-------------------------

An unrelated C implementation by Joel Tucci can be found at
https://github.com/joeltucci/rabin-fingerprint-c.  This version
doesn't use David's ubiquitous bit-shifting algorithms, and I don't
know how fast or compliant it is compared to David's code. 

AZ Huang converted Joel's version to a Python module:
https://github.com/aitjcize/pyrabin. I've forked and contributed to
AZ's version at https://github.com/stevegt/pyrabin.

