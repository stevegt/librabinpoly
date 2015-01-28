#!/usr/bin/python

# import binascii
from ctypes import *
import hashlib
import random


import rabinpoly

lib = rabinpoly.lib

window_size = 32
min_block_size = 1024
avg_block_size = 8192
max_block_size = 65536

rp = lib.rabin_init(
		window_size, avg_block_size, min_block_size, max_block_size)


random.seed(42)
buf_size = 128*1024
buf = create_string_buffer(buf_size)

class Mockfile(object):

	def __init__(self):
		self.txt = ''
		self.pos = 0

	def read(self, size):
		txt = self.txt[self.pos:self.pos + size]
		self.pos += len(txt)
		return txt

	def append(self, txt):
		self.txt += txt

def mkmf(size):
	print 'building mock file...'
	mf = Mockfile()
	for i in range(size):
		mf.append(chr(random.randrange(0,256)))
	print 'done'
	return mf

hashes = [

		(0, 15848, "6e982e9acea7f824f31d800ae43e5918"),
		(15848, 1132, "a1ea67cfe56e976504c3ec66fba5196a"),
		(16980, 5728, "c327d179d8615158acbff9dba35e2cfa"),
		(22708, 10064, "8ebf4a11e100133a9f7e0d85c5dd7f16"),
		(32772, 20295, "a5b82ad6a8ed93f38541f28809c6a708"),
		(53067, 1091, "2494fb1d416224ccb857c581f9829a8c"),
		(54158, 4336, "80763754510e3cc810f5fc7bd6d1743f"),
		(58494, 1514, "a6b3638460b7e93a62359842c78851cb"),
		(60008, 4938, "4c0e00eab9c208f3c52eb029a8df6bf1"),
		(64946, 13019, "b31bfe08d23b1c1b1ca3391dd90953e2"),
		(77965, 3910, "de7c951986d1b60a1b516d35649027ec"),
		(81875, 3146, "8e5874755e5e23aae7531be62f508b5a"),
		(85021, 5636, "a497e1b49e79e4c3a27c81c135f470e9"),
		(90657, 22865, "9693e9e0dae72e8cda2e372a09d169d2"),
		(113522, 5237, "2d699b2f5a2602b828285ddaa3dd06ea"),
		(118759, 8987, "319edf2d96808204d2b2442ee0ad9a6b"),
		(127746, 1263, "834bcae5208fefdd7fa3b094d9dbb08c"),
		(129009, 7043, "b079b8522bc2de51cf56e5892e114e42"),
		(136052, 8751, "4447997a89c37ea9f6d63390043a340b"),
		(144803, 8912, "308346299782cc037a707752078567b8"),
		(153715, 4850, "d35656ccb01a4f3dbe583fd3696b7f2b"),
		(158565, 9379, "f75d88d9db36a5d1af61bc4f0cca0e0c"),
		(167944, 23747, "178e43655f4fe2fd91ded757fa0c625e"),
		(191691, 7955, "02fc218bec17a2688108e2f8eb2daef7"),
		(199646, 11073, "54357e7f95c0148a1c25a77bde4a37c6"),
		(210719, 4836, "c5ab4f1104ebe504093fd15e72da5205"),
		(215555, 6505, "93b86708a0b3d88b4d7a23fba0a73b2a"),
		(222060, 5574, "ab84145bf26c276188f6bf0be8f71471"),
		(227634, 3052, "6ac335959af844584e952214df38636d"),
		(230686, 7697, "f7f8cd7b15f1a077f483efd7547456c3"),
		(238383, 6361, "81774f631ce8823fd05a58bd2f9c80ad"),
		(244744, 1250, "bee2e1c170fa63ac87d6b031402645a9"),
		(245994, 4751, "fb3b523cee07d4de0a232e68d9ca2f51"),
		(250745, 1856, "7f576fdd0a471c9e6f190a9d473be4e3"),
		(252601, 1427, "285d76027e29e7a51479ee0fc83eaa3a"),
		(254028, 7699, "21bb81f67bd54a467d991aa6470cf844"),
		(261727, 4062, "95491dc682276692279290b5d795e408"),
		(265789, 8536, "57b51f6bb5a176e4a021d892413d2127"),
		(274325, 5121, "1223d41bc023e798a22918870fe40254"),
		(279446, 8448, "140164c305dd7e1737e8fc071e8b969e"),
		(287894, 16112, "fa9c325061abebe7578595e87a4d541a"),
		(304006, 5619, "9634c786c890229d76ae346fcff612ac"),
		(309625, 16319, "a93b79c6c8786761edcf0819cb541919"),
		(325944, 4831, "6e49ad383fd1ded16a36455ea4a9de1f"),
		(330775, 6367, "54fb011052959bd66500bea119446f47"),
		(337142, 1279, "3a13b4ca01d399c7d976956ae6c64ed2"),
		(338421, 3355, "767019da0ab7e236723a93c7b1da8df6"),
		(341776, 8884, "b4643c08a8894c0f33f95c3617fdc806"),
		(350660, 2082, "d21ea6bd83171a493e621c3bf2a85909"),
		(352742, 7083, "75594434ae99cb6eb504aacf703fc90c"),
		(359825, 4346, "94c08d3d99960bf89e3aaa85ea076599"),
		(364171, 7292, "61ddd866f07a4bc704cb30f8cad03f8d"),
		(371463, 2781, "e4fe96abc752b0e9d38c5dbd7c7b7e2e"),
		(374244, 7631, "498a7b2eb60d3124a84bea9b07a49153"),
		(381875, 14724, "a8a27dfc23237832a21de7094ceb1ecf"),
		(396599, 1614, "82ae3fa2a3d31c3f49963588445a9141"),
		(398213, 3234, "ab0cdf05ddd799a5ffa0ec564454e425"),
		(401447, 6687, "86a0e0ec0f9ba39967883365e6a305ad"),
		(408134, 3263, "8bc0774171bdd3dc7e299ff1c94c9d26"),
		(411397, 8623, "9991081da8c918af940b9c99a70db11e"),
		(420020, 7469, "4c42b080cbbc084a04d2c7ebf98b15ea"),
		(427489, 9316, "8d06f502c600fabe8e847345a496ebc9"),
		(436805, 11461, "72a84279be2161d15fcdc686fae77c60"),
		]

mf = mkmf(int(buf_size*3.42))

i = 0
ref_block_start = 0
hasher = hashlib.md5()
eof  = 0
while not eof:
	txt = mf.read(max_block_size)
	if len(txt) < max_block_size:
		eof = 1
	buf.value = txt
	rc = lib.rabin_in(rp, buf, len(txt), eof)
	assert rc == 0
	while lib.rabin_out(rp):
		start = rp.contents.frag_start
		count = rp.contents.frag_size
		assert start + count <= buf_size
		hasher.update(buf[start:start+count])
		block_done = rp.contents.block_done
		if block_done:
			block_start = rp.contents.block_start
			assert hashes[i][0] == block_start
			size = rp.contents.block_size
			assert hashes[i][1] == size
			h = hasher.hexdigest()
			assert hashes[i][2] == h
			print '(%d, %d, "%s"),' % (block_start, size, h)
			assert ref_block_start == block_start
			ref_block_start += size
			i += 1
	if rp.contents.eof == 1:
		assert eof == 1

print i
assert i == len(hashes)

lib.rabin_free(byref(rp))
