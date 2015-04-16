#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <rabinpoly.h>
// #include <crypto.h>
#include <openssl/md5.h>

MD5_CTX mdctx;
unsigned char digest[MD5_DIGEST_LENGTH];

int block_start(RabinPoly *rp) {
    MD5_Init(&mdctx);
    return 0;
}

int block_end(RabinPoly *rp) {
	int i;
    MD5_Final(digest, &mdctx);
    printf("%zu %zu ", rp->block_streampos, rp->block_size);
    for (i = 0; i < MD5_DIGEST_LENGTH; i++) {
        printf("%02x", digest[i]);
    }
    printf("\n");
    MD5_Init(&mdctx);
    return 0;
}

int fragment_end(RabinPoly *rp) {
    assert (rp->fragment_addr + rp->fragment_size <= rp->inbuf + rp->inbuf_read_count);
    MD5_Update(&mdctx, rp->fragment_addr, rp->fragment_size);
    return 0;
}

int main(int argc, char **argv){
	int i;

	printf("argc %d\n", argc);
	for (i=0; i < argc; i++) {
		printf("argv[%d] %s\n", i, argv[i]);
	}

	// http://stackoverflow.com/questions/10324611/how-to-calculate-the-md5-hash-of-a-large-file-in-c
	// http://stackoverflow.com/questions/10129085/read-from-stdin-write-to-stdout-in-c
	
    // char *filename="file.c";
    // FILE *inFile = fopen (filename, "rb");

	// if (inFile == NULL) {
	//     printf ("%s can't be opened.\n", filename);
	//     return 0;
	// }

	unsigned int window_size = 32;
	size_t min_block_size = 1024;
	size_t avg_block_size = 8192;
	size_t max_block_size = 65536;
	size_t buf_size = 128*1024;

	RabinPoly *rp;
   
	rp = rp_new(
			window_size, avg_block_size, min_block_size, max_block_size, buf_size);

    rp->func_block_start = block_start;
    rp->func_block_end = block_end;
    rp->func_fragment_end = fragment_end;
    
    int rc = rp_stream_process(rp, stdin);
    assert(rc == EOF);
    assert(feof(stdin));

	rp_free(rp);

	return 0;
}

