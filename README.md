librabinpoly
============

Rabin fingerprinting library in C, for chunking files into
content-delimited variable sized blocks.

Includes python bindings.  The python library uses ctypes, so the C
library is pure C.  This makes it possible to add other language
bindings; send me pull requests.

The API should not be considered stable until we reach version 1.X.

Install
=======

From tarball
------------

    ./configure
    make 
    make test
    make install


From git
--------

    make -f autotools.mk
    ./configure
    make
    make test
    make install


History
=======

(Please send me pull requests for any corrections or additional
information anyone wants to add here.  I want to set the record
straight, and also think that understanding the history helps with
understanding the code.)

It all started with Michael O. Rabin's 1981 paper "Fingerprinting by
Random Polynomials", TR-15-81, Harvard University.  (As of this
writing, a copy of the paper can be found at
http://www.xmailserver.org/rabin.pdf.)

The earliest implementation I know of is the 1999 code by David
Mazieres <dm@uun.org> for the Low-Bandwidth File System project:

http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.28.8654 

The authoritative location for LBFS and SFS appears to be
http://pdos.csail.mit.edu/lbfs/dist.html.  The LBFS CVS server is
down, but the CVS repository is archived at http://www.fs.net/.  

David's rabinpoly implementation in SFS is written in C++.  I don't
know if this is his first implementation, or if David wrote an earlier
version in C.  Later implementations crediting David are found in both
C and C++. 

Several later rabinpoly derivatives include some \_LPCOX_DEBUG\_ debug
statements.  LPCOX appears to be Landon Cox
(http://www.cs.duke.edu/~lpcox/), one of the co-authors on the 2002
paper "Pastiche: Making Backup Cheap and Easy":
https://www.usenix.org/legacy/event/osdi02/tech/full_papers/cox/cox.pdf

The last archive.org capture of the Pastiche web page was in 2004:
https://web.archive.org/web/20040211222605/http://mobility.eecs.umich.edu/pastiche/

So far I haven't been able to find the Pastiche code itself -- it
seems to have dropped off the net.

Sometime around 2002-2004, Niraj Tolia, apparently starting from
Landon's Pastiche code, converted rabinpoly to a stand-alone library.
I haven't been able to find Niraj's version.  Niraj also cited the
Pastiche paper in two papers of his own:
http://dl.acm.org/citation.cfm?id=1060316&preflayout=flat.  

In 2003-2005, Hyang-Ah Kim <hakim@cs.cmu.edu>, starting from Niraj's
version, repackaged and re-released rabinpoly, adding support for a
configurable sliding window size. Her code can be found at
http://www.cs.cmu.edu/~hakim/software/, and is in C++.  It still has
Landon's debug statements in it.  Hyang-Ah's README is where I got the
clue about Niraj.

In 2006, Geert Bosch <bosch@adacore.com> attached a C version of
rabinpoly to an email message he sent to the git developers' mailing
list, crediting David Mazieres' Rabinpoly code and D. Phillips's fls
code. This version appears to share a common ancestor with Hyang-Ah's
code, but doesn't include Landon's debug statements.  His rabinpoly.h
says "Translated to C and simplified by Geert Bosch (bosch@gnat.com)".
Geert's email message includes a description of the internal working
of the algorithm.
http://www.gelato.unsw.edu.au/archives/git/0604/18872.html

Junio C Hamano did some cleanup and checked Geert's code into git-core
at
https://code.google.com/p/git-core/source/detail?r=fd2bbdd2386ea0c558aba95711ef53c4552a6146&path=/rabinpoly.c
-- it's not clear to me at the moment whether it was ever used though,
by git or any other package.

In 2010, Bobby Martin wrote rabin-tool, starting from Hyang-Ah's
version: https://github.com/wurp/rabin-tool

In 2010, Dan Stromberg (http://stromberg.dnsalias.org/~dstromberg/) 
refactored Hyang-Ah's C++ code into a python library, adding test
cases.  http://stromberg.dnsalias.org/svn/pyrabinf/trunk/ 

In 2013, Pavan Kumar Alampalli <pavankumar@cmu.edu>,
(http://www.pdl.cmu.edu/People/pavan.shtml) credits Hyang-Ah in a
pure-C version he worked on.  This version appears to be either a
merge of Hyang-Ah's C++ code into Geert's C code, or a completely new
C translation (still trying to figure that out).  Unlike other
derivatives, this code does *not* include Landon's debug statements.
It can be found at
http://www.ece.cmu.edu/~ganger/746.spring13/projects/proj2_fuse/746-handout/src/dedup-lib/.

Pavan's version is used for Greg Ganger's 15-746/18-746 Storage
Systems course at CMU (http://www.ece.cmu.edu/~ganger).  I'm basing
my first version of librabinpoly on this code.


Other rabinpoly libraries
-------------------------

An unrelated C implementation by Joel Tucci can be found at
https://github.com/joeltucci/rabin-fingerprint-c.  This version
doesn't use David's ubiquitous bit-shifting algorithms, and I don't
know how fast or compliant it is compared to David's code. 

AZ Huang converted Joel's version to a Python module:
https://github.com/aitjcize/pyrabin. I've forked and contributed to
AZ's version at https://github.com/stevegt/pyrabin.

There is a succinct description of Rabin's algorithm in Bill Dwyer's
Java implementation:  https://github.com/themadcreator/rabinfingerprint/blob/master/src/main/java/org/rabinfingerprint/fingerprint/RabinFingerprintPolynomial.java
