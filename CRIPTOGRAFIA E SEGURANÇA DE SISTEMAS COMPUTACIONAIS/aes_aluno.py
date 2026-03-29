# AES-256 implementation (educacional)

S_BOX = [
    99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,118,
    202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,
    183,253,147,38,54,63,247,204,52,165,229,241,113,216,49,21,
    4,199,35,195,24,150,5,154,7,18,128,226,235,39,178,117,
    9,131,44,26,27,110,90,160,82,59,214,179,41,227,47,132,
    83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,
    208,239,170,251,67,77,51,133,69,249,2,127,80,60,159,168,
    81,163,64,143,146,157,56,245,188,182,218,33,16,255,243,210,
    205,12,19,236,95,151,68,23,196,167,126,61,100,93,25,115,
    96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,
    224,50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,
    231,200,55,109,141,213,78,169,108,86,244,234,101,122,174,8,
    186,120,37,46,28,166,180,198,232,221,116,31,75,189,139,138,
    112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,158,
    225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,
    140,161,137,13,191,230,66,104,65,153,45,15,176,84,187,22
]

INV_S_BOX = [0]*256
for i in range(256):
    INV_S_BOX[S_BOX[i]] = i

RCON = [
    0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36
]


def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1)


def mul(a, b):
    res = 0
    for i in range(8):
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res


class AES256:
    def __init__(self, key: bytes):
        if len(key) != 32:
            raise ValueError("Chave deve ter 32 bytes")
        self.Nk = 8
        self.Nr = 14
        self.round_keys = self.key_expansion(key)

    # =========================
    # KEY EXPANSION
    # =========================
    def key_expansion(self, key):
        w = [list(key[i:i+4]) for i in range(0, 32, 4)]

        for i in range(8, 4*(self.Nr+1)):
            temp = w[i-1].copy()

            if i % 8 == 0:
                temp = self.sub_word(self.rot_word(temp))
                temp[0] ^= RCON[(i//8)-1]
            elif i % 8 == 4:
                temp = self.sub_word(temp)

            word = [a ^ b for a, b in zip(w[i-8], temp)]
            w.append(word)

        return [sum(w[i:i+4], []) for i in range(0, len(w), 4)]

    def sub_word(self, word):
        return [S_BOX[b] for b in word]

    def rot_word(self, word):
        return word[1:] + word[:1]

    # =========================
    # CORE OPERATIONS
    # =========================
    def add_round_key(self, state, round_key):
        return [s ^ k for s, k in zip(state, round_key)]

    def sub_bytes(self, state):
        return [S_BOX[b] for b in state]

    def inv_sub_bytes(self, state):
        return [INV_S_BOX[b] for b in state]

    def shift_rows(self, s):
        return [
            s[0], s[5], s[10], s[15],
            s[4], s[9], s[14], s[3],
            s[8], s[13], s[2], s[7],
            s[12], s[1], s[6], s[11]
        ]

    def inv_shift_rows(self, s):
        return [
            s[0], s[13], s[10], s[7],
            s[4], s[1], s[14], s[11],
            s[8], s[5], s[2], s[15],
            s[12], s[9], s[6], s[3]
        ]

    def mix_columns(self, s):
        res = []
        for i in range(4):
            col = s[i*4:(i+1)*4]
            res += [
                mul(col[0],2)^mul(col[1],3)^col[2]^col[3],
                col[0]^mul(col[1],2)^mul(col[2],3)^col[3],
                col[0]^col[1]^mul(col[2],2)^mul(col[3],3),
                mul(col[0],3)^col[1]^col[2]^mul(col[3],2)
            ]
        return res

    def inv_mix_columns(self, s):
        res = []
        for i in range(4):
            col = s[i*4:(i+1)*4]
            res += [
                mul(col[0],14)^mul(col[1],11)^mul(col[2],13)^mul(col[3],9),
                mul(col[0],9)^mul(col[1],14)^mul(col[2],11)^mul(col[3],13),
                mul(col[0],13)^mul(col[1],9)^mul(col[2],14)^mul(col[3],11),
                mul(col[0],11)^mul(col[1],13)^mul(col[2],9)^mul(col[3],14)
            ]
        return res

    # =========================
    # ENCRYPT
    # =========================
    def encrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("Bloco deve ter 16 bytes")

        state = list(block)
        state = self.add_round_key(state, self.round_keys[0])

        for r in range(1, self.Nr):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state, self.round_keys[r])

        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, self.round_keys[self.Nr])

        return bytes(state)

    # =========================
    # DECRYPT
    # =========================
    def decrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16:
            raise ValueError("Bloco deve ter 16 bytes")

        state = list(block)
        state = self.add_round_key(state, self.round_keys[self.Nr])

        for r in range(self.Nr-1, 0, -1):
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)
            state = self.add_round_key(state, self.round_keys[r])
            state = self.inv_mix_columns(state)

        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        state = self.add_round_key(state, self.round_keys[0])

        return bytes(state)