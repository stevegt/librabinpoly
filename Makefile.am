AUTOMAKE_OPTIONS = foreign
# ACLOCAL_AMFLAGS = -I m4

# SUBDIRS = doc man script src
SUBDIRS = src test python examples

#
# tests
# 

BENCHFN=/tmp/rabin-benchmark.test
export LD_LIBRARY_PATH := $(CURDIR)/src/.libs:$(LD_LIBRARY_PATH)
export PYTHONPATH := $(CURDIR)/python:$(PYTHONPATH)

.PHONY: test 

test: test/data/random-42x1M.dat test/data/pmlog.dat python/rabinpoly.py
	test/test_load.py
	test/test_16_32_64.py
	test/test_zeros.py
	test/test_ones.py
	test/test_hash.py
	test/test_eof.py
	test/test_pmlog.py


$(BENCHFN): 
	dd if=/dev/urandom of=$(BENCHFN) bs=1M count=10

benchmark: $(SO) $(BENCHFN)
	test/benchmark.py $(BENCHFN)
	time examples/benchmark < $(BENCHFN)

test/data/random-42x1M.dat:
	git cat-file -p 3a44d8491c56b1fdf39c7f753cfa8b4c618e9f1d > $@

test/data/pmlog.dat:
	git cat-file -p 821bafa6af7025b5c8dd4ea73d9599081ae5a68e > $@

lint:
	cppcheck --enable=all src/*.c src/*.h
	make clean && scan-build -V make

python/rabinpoly.py: src/rabinpoly.h
	ctypesgen.py -L $(LD_LIBRARY_PATH) -l rabinpoly -o python/rabinpoly.py $(CURDIR)/src/rabinpoly.h
