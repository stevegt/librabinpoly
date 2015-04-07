#!/usr/bin/python

# import binascii
from ctypes import *
import hashlib
import random

import rabinpoly as lib

window_size = 32
min_block_size = 1024
avg_block_size = 8192
max_block_size = 65536

rp = lib.rp_init(
		window_size, avg_block_size, min_block_size, max_block_size)
rpc = rp.contents

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
			(15848, 1132, "dcea3255b032bc3ccca611b502cf099e"),
			(16980, 5728, "242a8fbb9726e2d1dfe28114bfda94bc"),
			(22708, 10064, "e55afa930a5182ca060e9c688c36539c"),
			(32772, 20295, "34b8450b06a5954f54d4a3c0ce5590c1"),
			(53067, 1091, "778cb24f608c432b290162849250d4ef"),
			(54158, 4336, "02d097473ffc4da2d990093d4604b90c"),
			(58494, 1514, "33f47c8dbd50e0dac65826a00d7e2e9d"),
			(60008, 4938, "7e985d27b5e655fd49380b9525f203d1"),
			(64946, 13019, "f9168624b89aa84bfe62b614e950fc33"),
			(77965, 3910, "0d05cce517fc9e7548147e721fa4e167"),
			(81875, 3146, "a0de5d38f8c7a457fbb05ed6f1a62b15"),
			(85021, 5636, "c5f7de047e0e718ca5db7e0b51321681"),
			(90657, 22865, "0129cbbe2f2c39982011650b5564da90"),
			(113522, 5237, "9c55de35686dcade88cb7cc5dfe452c6"),
			(118759, 8987, "c02786b2e2e297510db94d32804372f8"),
			(127746, 1263, "51440938e4772cb640ae4556e2cbb515"),
			(129009, 7043, "9733e0976c04f38f398e3e75c42a0c4d"),
			(136052, 8751, "bc06a8c349eb2de4cf8cba083f267976"),
			(144803, 8912, "6ea063b2f40d0ebe39d51cd724b7372a"),
			(153715, 4850, "376022b5fa7f8c9d4c8f83f28ad409bd"),
			(158565, 9379, "460af7b97f84239bacec132e6023e4b7"),
			(167944, 23747, "070ff3747e89a3f821efd095efd92e57"),
			(191691, 7955, "bc567c42241f60e27e839226518ed7f0"),
			(199646, 11073, "c64256f4134af363da07d74fd1b1d9e2"),
			(210719, 4836, "86f4b41317bcaa269cd25e72677daf29"),
			(215555, 6505, "5c2950e13d3bc564548c5e09fbc31870"),
			(222060, 5574, "30c898176a772990da8fb02abc14e010"),
			(227634, 3052, "f4a4ac54363ee69463bcfd9fb059496e"),
			(230686, 7697, "a4a4ea8eb488a757116d6702bf0b1097"),
			(238383, 6361, "d98b1bdebeb3140dc18480e8b378df1b"),
			(244744, 1250, "6fa1fc8ae3533530321de4dba3a9d32b"),
			(245994, 4751, "58e4ddeaabddb19095bb8aa5cb9bfff5"),
			(250745, 1856, "929319912fdc82589f5f71411f93e94c"),
			(252601, 1427, "f47e298de393845aa6dbab7ff2bc945d"),
			(254028, 7699, "025237640bbcbf2929436d4be0cc9b6f"),
			(261727, 4062, "642d61f5b482579bea6f8b83e38746e7"),
			(265789, 8536, "6c4cb6e0947c2f4df4fb74e564473de4"),
			(274325, 5121, "d1d88d3ae1b7e5e70fb2f30cd1510924"),
			(279446, 8448, "13cdb056d77e1f6235257045ca719714"),
			(287894, 16112, "2dc86381aa2f14aac6eb1fa7e722180e"),
			(304006, 5619, "86e55e749458e561b9876dd1179cf751"),
			(309625, 16319, "d82bba654df8b86d129453ec529df7b2"),
			(325944, 4831, "e563b7743d13fda9b0eaf417d93d71b6"),
			(330775, 6367, "e609ec98de2d18f61c50efd937ccdf9e"),
			(337142, 1279, "006001156dcc3ef097f9b665b71bda92"),
			(338421, 3355, "4894f8a8e77f0ad043f4a8d3f69c3aaf"),
			(341776, 8884, "977d577b78a539e9ed356fd25e60539f"),
			(350660, 2082, "29940887ad65796a05375256231dcf6c"),
			(352742, 7083, "14d825d0729e74e9cd22efc16fde4358"),
			(359825, 4346, "40a6b8d66642e497f17ea61ede2fa4c9"),
			(364171, 7292, "5d183ea69746c75e8ab255069d74fbc7"),
			(371463, 2781, "e5c11ca066b813a7b400173778d10b63"),
			(374244, 7631, "6c6dbe75ad9e846a5f1bf20df07c78e7"),
			(381875, 14724, "971bfc208e67f6dd4b6f6c14f0c0afe8"),
			(396599, 1614, "aff557f925ed6125acafe00d5a64f947"),
			(398213, 3234, "9c81123af69389d3810004c8611a8e4e"),
			(401447, 6687, "0c5bd0b732e3ffca4a2efe75a6d025f3"),
			(408134, 3263, "625285cc5e6815a4678136b8c654f88b"),
			(411397, 8623, "76bf7f6b34c80c72ba0bf248296b55b7"),
			(420020, 7469, "982cf5a078165e33b294c161527f4859"),
			(427489, 9316, "62b87f83b0538e2ccf258a47cb57433c"),
			(436805, 25539, "2d8a03a78b4d3ebc7a0cdbe59f4de240"),
			(462344, 1716, "a6a5fab99097330e20a68c8fe467275c"),
			(464060, 5766, "377aa79fca2eda9c3ca05ad9ef0aa679"),
			(469826, 12790, "0b1013148fc57e5e447741d3d856068e"),
			(482616, 14048, "5d6a8ad794604f5cb49ef2e2b9dfa03e"),
			(496664, 15104, "2eff4e07d566ece2f58c841bd6340ee5"),
			(511768, 3035, "a5e8ba5ff3dd43f60b6cfd1c44c81f66"),
			(514803, 11335, "9209e9a8f087b1384ecfbe205edcfba8"),
			(526138, 6905, "212434bbe3cae644a448956b0d0c0189"),
			(533043, 4578, "9566836aa8d998ffd617fe4a96736922"),
			(537621, 4860, "1b6f988ace3ce6d5099131da8de0d850"),
			(542481, 7631, "b326898aab28ee2c8a0272ed55922ae6"),
			(550112, 3495, "ba5437a9d5a7425a726966f662bfdeb5"),
			(553607, 11235, "f8adcbec462cc4e4937b7ad24145340d"),
			(564842, 10327, "10f7ed0bb10dc0445e9d765e58961a09"),
			(575169, 4849, "ea52984f77ed1bad578d00fdf5e5f86d"),
			(580018, 1573, "890c4dbf21b64490f0536752ecc36f34"),
			(581591, 4116, "74d8c585f512a74cdf6041a3f29ccad8"),
			(585707, 5030, "1447128756954a3778b8ae64f74fc1a5"),
			(590737, 11738, "21d2cb8b9303772d8b02d416d8ef0f83"),
			(602475, 26990, "00976f7b9961c100d616d6ba9a6fac06"),
			(629465, 21451, "8f14642450473c43f2d1b217edf4b781"),
			(650916, 2146, "c59ad3aedeca20cfbbb9dc11bc0ac3f3"),
			(653062, 6616, "53f1973b3f240cfe7f4002b18c354717"),
			(659678, 3976, "029bb0782cafb540ce2cdbac539f9665"),
			(663654, 1954, "047cac444384fd58dca6b131aa79e0a1"),
			(665608, 3420, "15ace2ddd7cca259da1cf094cedae5e9"),
			(669028, 7996, "e0b642547bf6508e4866932e6f7d8a73"),
			(677024, 9090, "4e447ed911b1fc53aee77f3b4fedbfde"),
			(686114, 16262, "ed484c9358c1d431c6a6bcdf041db7cf"),
			(702376, 14898, "42cd5430240c8432e0acbbc0d7626b8b"),
			(717274, 1732, "6a7cb886e78f3d93a6e09f5f3ba680e5"),
			(719006, 15342, "213e65a09e76291925a38bca35c6e7f8"),
			(734348, 10260, "692f40b8d0e47f6ef2eb739c7b1298ae"),
			(744608, 24297, "5baa84ad7ea8805f1116ebd9e0749f38"),
			(768905, 13742, "084cd0ff05ae1b644649c08f3d1632ca"),
			(782647, 7365, "5c9404ebd7970beefd168db58029be0f"),
			(790012, 1066, "5b7fb7777a676c430d71c53b60fa30a6"),
			(791078, 35492, "0f2d365b763908bff9c52dc47489f3b4"),
			(826570, 1168, "805c5e1549006bd923b4bac4c0083ec6"),
			(827738, 17535, "d303438e0866bc249d9906ab67dee130"),
			(845273, 15466, "48e72bda7432326dd8e3b070a0a81341"),
			(860739, 12971, "a88079218b90b327d287b70bb34a75ca"),
			(873710, 2894, "a554984db87eb1fab9f969b5302ba647"),
			(876604, 5748, "91787742bb1927ff8f27184935db90d5"),
			(882352, 11305, "90becb5d91c9836c5c82ed06ba72e069"),
			(893657, 1819, "39c69900bd35906a2622aa8ec8c9770b"),
			(895476, 7592, "aa5788f9d4efbdbf5c116ec49cfd6f1b"),
			(903068, 3836, "263a82e18cc442523c7719441bb241ad"),
			(906904, 1150, "a269208b0cbfce20432f32739e4cd589"),
			(908054, 3871, "74af77c47c31de2f6f2f6e3aebf4203e"),
			(911925, 8182, "3709dd59ee4ffc5c39179b201dd3845d"),
			(920107, 5741, "a37f5c0368dc1bc28c9aead853f3ccc8"),
			(925848, 6082, "2b3e5098ac3f3f0af242002c70859258"),
			(931930, 3050, "1384cbff3d890aaddfef3e911814279c"),
			(934980, 1915, "838a6902ef0c658a4714f08b2bfcb18c"),
			(936895, 3066, "529bdc708637f110f18382f9771c1599"),
			(939961, 8867, "11b59f46946a6ed107851f5757a8e8a4"),
			(948828, 3101, "edf9c3204f8839abfd832682be312891"),
			(951929, 4736, "f04aaf01aaa2f21770e9cb8a57d1d5fe"),
			(956665, 8197, "2eeba9cb73af246bd8e6cffd8a354340"),
			(964862, 5870, "04d113ef8e6a4ad50a1f1916eb7f9abd"),
			(970732, 19498, "684ebbfd64a3f653121673db66918338"),
			(990230, 13825, "b44dd55a00a04540ea32bd3df6bd0618"),
			(1004055, 11064, "3d3c8533c3cf84651d9233a8c2157bec"),
			(1015119, 1693, "052aa647101f994f5127f51a8ae2055f"),
			(1016812, 4617, "15f6963205e6bcea1a66a699c5f50baf"),
			(1021429, 10478, "5a7007c43c416bb9982b2f0f669fdc2d"),
			(1031907, 6192, "23db887c75d336b41f11632b2dc84d20"),

		]

# mf = mkmf(int(buf_size*3.42))
mf = open('test/data/random-42x1M.dat', 'r')

i = 0
ref_block_start = 0
hasher = hashlib.md5()
while True:
	if rpc.state & lib.RP_IN:
		txt = mf.read(max_block_size)
		buf.value = txt
		rc = lib.rp_in(rp, buf, len(txt))
		assert rc == 1
	if rpc.state & lib.RP_OUT:
		rc = lib.rp_out(rp)
		assert rc == 1
	if rpc.state & lib.RP_PROCESS_FRAGMENT:
		start = rpc.frag_start
		count = rpc.frag_size
		assert start + count <= buf_size
		hasher.update(buf[start:start+count])
	if rpc.state & lib.RP_PROCESS_BLOCK:
		block_start = rpc.block_start
		size = rpc.block_size
		h = hasher.hexdigest()
		print '(%d, %d, "%s"),' % (block_start, size, h)
		hasher = hashlib.md5()
		assert hashes[i][0] == block_start
		assert hashes[i][1] == size
		assert hashes[i][2] == h
		assert ref_block_start == block_start
		ref_block_start += size
		i += 1
	if rpc.state & lib.RP_RESET:
		assert not mf.read()
		break

print i
assert i == len(hashes)
assert rpc.state & lib.RP_RESET

lib.rp_free(rp)
