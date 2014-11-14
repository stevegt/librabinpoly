AUTOMAKE_OPTIONS = foreign
# ACLOCAL_AMFLAGS = -I m4

# SUBDIRS = doc man script src
SUBDIRS = src test


#
# testing bits
# 

BENCHFN=/tmp/rabin-benchmark.test
export LD_LIBRARY_PATH := $(CURDIR)/src/.libs:$(LD_LIBRARY_PATH)
export PYTHONPATH := $(CURDIR)/src:$(PYTHONPATH)

.PHONY: test 

test: 
	test/test_load.py
	test/test_zeros.py
	test/test_ones.py
	test/test_next.py
	test/test_reset.py
	test/test_16_32_64.py
	test/test_write.py

$(BENCHFN): 
	dd if=/dev/urandom of=$(BENCHFN) bs=1M count=10

benchmark: $(SO) $(BENCHFN)
	test/benchmark.py $(BENCHFN)

