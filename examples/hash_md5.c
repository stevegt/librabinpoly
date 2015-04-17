#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <rabinpoly.h>
// #include <crypto.h>
#include <openssl/md5.h>

// http://stackoverflow.com/questions/10324611/how-to-calculate-the-md5-hash-of-a-large-file-in-c
// http://stackoverflow.com/questions/10129085/read-from-stdin-write-to-stdout-in-c

int main(int argc, char **argv){
    MD5_CTX mdctx;
    unsigned char digest[MD5_DIGEST_LENGTH];
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
        
        MD5_Init(&mdctx);

        int rc = rp_block_next(rp);
        if (rc) {
            assert (rc == EOF);
            break;
        }

        MD5_Update(&mdctx, rp->block_addr, rp->block_size);
        MD5_Final(digest, &mdctx);
        printf("%zu %zu ", rp->block_streampos, rp->block_size);
        for (i = 0; i < MD5_DIGEST_LENGTH; i++) {
            printf("%02x", digest[i]);
        }
        printf("\n");

    }

    assert(feof(stdin));

	rp_free(rp);

	return 0;
}
