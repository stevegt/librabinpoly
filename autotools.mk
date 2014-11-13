# http://dadinck.50webs.com/computer/auto-howto.html
#

all: config.status

configure.in:
	autoscan
	vimdiff configure.scan configure.in

ltmain.sh:
	libtoolize

aclocal.m4: configure.in ltmain.sh
	aclocal

configure: configure.in aclocal.m4 
	autoconf

Makefile.in: Makefile.am configure.in aclocal.m4 
	automake --foreign --add-missing --copy

config.h.in: configure.in 
	autoheader

config.status config.cache config.log config.h Makefile: Makefile.in
	./configure

