CFLAGS=-Wall -fPIC
LDFLAGS=-L.
LIBS=-lcrypto -lssl
OBJECTS=rabinpoly.o msb.o
SO=librabinpoly.so.0

export LD_LIBRARY_PATH := =$(CURDIR):$(LD_LIBRARY_PATH)
export PYTHONPATH := $(CURDIR):$(PYTHONPATH)

ifdef DEBUG
	CFLAGS+=-g
endif

.PHONY: test 

all: test
	
test: $(SO)
	test/test_load.py
	test/test_next.py
	test/test_reset.py

$(SO): $(OBJECTS)
	gcc -shared -fPIC -Wl,-soname,$(SO) -o $(SO) $(OBJECTS) -lc

%.o : %.c 
	gcc $(CFLAGS) -c -o $@ $<

%.c : %.h

.PHONY: clean

clean : 
	rm -f $(OBJECTS) $(SO)
