
# here's the right way to do this now:
all: 
	autoreconf

# following adapted from:
# http://dadinck.50webs.com/computer/auto-howto.html

# all: config.status

configure.ac: Makefile.am
	autoscan
	vimdiff configure.scan configure.ac

ltmain.sh:
	libtoolize --install --copy

aclocal.m4: configure.ac ltmain.sh
	# aclocal -I m4
	aclocal 

configure: configure.ac aclocal.m4 
	autoconf

Makefile.in: Makefile.am configure.ac aclocal.m4 config.h.in
	automake -i --foreign --add-missing --copy

config.h.in: configure.ac 
	autoheader

config.status config.cache config.log config.h Makefile: Makefile.in
	./configure

