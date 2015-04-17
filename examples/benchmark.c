#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <rabinpoly.h>
// #include <crypto.h>
// #include <openssl/md5.h>


int main(int argc, char **argv){
	int i;

	printf("argc %d\n", argc);
	for (i=0; i < argc; i++) {
		printf("argv[%d] %s\n", i, argv[i]);
	}

	unsigned int window_size = 32;
	size_t min_block_size = 1024;
	size_t avg_block_size = 8192;
	size_t max_block_size = 65536;
	size_t buf_size = max_block_size * 10;

	RabinPoly *rp;
   
	rp = rp_new(window_size, 
            avg_block_size, min_block_size, max_block_size, buf_size);
	rp_from_stream(rp, stdin);

    for (;;) {
        
        int rc = rp_block_next(rp);
        if (rc) {
            assert (rc == EOF);
            break;
        }

    }

    assert(feof(stdin));

	rp_free(rp);

	return 0;
}
