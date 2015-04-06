#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <rabinpoly.h>
// #include <crypto.h>
#include <openssl/md5.h>



int main(int argc, char **argv){
	int i;

	printf("argc %d\n", argc);
	for (i=0; i < argc; i++) {
		printf("argv[%d] %s\n", i, argv[i]);
	}

	// http://stackoverflow.com/questions/10324611/how-to-calculate-the-md5-hash-of-a-large-file-in-c
	// http://stackoverflow.com/questions/10129085/read-from-stdin-write-to-stdout-in-c
	
	unsigned char digest[MD5_DIGEST_LENGTH];
    // char *filename="file.c";
    // FILE *inFile = fopen (filename, "rb");
    MD5_CTX mdctx;

	// if (inFile == NULL) {
	//     printf ("%s can't be opened.\n", filename);
	//     return 0;
	// }

	unsigned int window_size = 32;
	size_t min_block_size = 1024;
	size_t avg_block_size = 8192;
	size_t max_block_size = 65536;

	rabinpoly_t *rp;
   
	rp = rabin_init(
			window_size, avg_block_size, min_block_size, max_block_size);

	size_t buf_size = 128*1024;
	unsigned char buf[buf_size];


    // MD5_Init (&mdctx);
    // while ((bytes = fread (data, 1, 1024, stdin)) != 0)
        // MD5_Update (&mdctx, data, bytes);
    // MD5_Final (digest,&mdctx);
    // for(i = 0; i < MD5_DIGEST_LENGTH; i++) printf("%02x", digest[i]);

	int rc;
	size_t fread_count;
	MD5_Init(&mdctx);
	while (1) {

		if (RABIN_OUT & rp->state) {
			rc = rabin_out(rp); 
			assert (rc == 1);
		}

		if (PROCESS_FRAGMENT & rp->state) {
			assert (rp->frag_start + rp->frag_size <= buf_size);
			if (rp->frag_size) {
				MD5_Update(&mdctx, buf+rp->frag_start, rp->frag_size);
			}
		}

		if (PROCESS_BLOCK & rp->state) {
			MD5_Final(digest, &mdctx);
			printf("%zu %zu ", rp->block_start, rp->block_size);
			for (i = 0; i < MD5_DIGEST_LENGTH; i++) {
				printf("%02x", digest[i]);
			}
			printf("\n");
			MD5_Init(&mdctx);
		}

		if (RABIN_IN & rp->state) {
			fread_count = fread(buf, 1, buf_size, stdin);
			if (fread_count < buf_size) {
				if (ferror(stdin)) {
					return EIO;
				}
			}
			rc = rabin_in(rp, buf, fread_count);
			assert (rc == 1);
		}

		if (RABIN_RESET & rp->state) {
			assert (feof(stdin));
			break;
		}
	}

	rabin_free(rp);

	return 0;
}
