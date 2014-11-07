CFLAGS=-Wall -fPIC
LDFLAGS=-L.
LIBS=-lcrypto -lssl
OBJECTS=rabinpoly.o msb.o
SO=librabinpoly.so.0
BENCHFN=/tmp/rabin-benchmark.test

export LD_LIBRARY_PATH := =$(CURDIR):$(LD_LIBRARY_PATH)
export PYTHONPATH := $(CURDIR):$(PYTHONPATH)

ifdef DEBUG
	CFLAGS+=-g
endif

.PHONY: test 

all: test
	
test: $(SO)
	test/test_load.py
	test/test_zeros.py
	test/test_ones.py
	test/test_next.py
	test/test_reset.py
	test/test_16_32_64.py

$(BENCHFN): 
	dd if=/dev/urandom of=$(BENCHFN) bs=1M count=10

benchmark: $(SO) $(BENCHFN)
	test/benchmark.py $(BENCHFN)

$(SO): $(OBJECTS)
	gcc -shared -fPIC -Wl,-soname,$(SO) -o $(SO) $(OBJECTS) -lc

%.o : %.c 
	gcc $(CFLAGS) -c -o $@ $<

%.c : %.h

.PHONY: clean

clean : 
	rm -f $(OBJECTS) $(SO)
