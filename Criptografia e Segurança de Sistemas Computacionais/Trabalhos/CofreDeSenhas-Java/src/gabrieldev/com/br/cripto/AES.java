package gabrieldev.com.br.cripto;

import java.util.ArrayList;
import java.util.List;

public class AES {
	
	//byte[] key = ... // 32 bytes
	//AES256 aes = new AES256(key);

	//byte[] encrypted = aes.encryptBlock(block);
	//byte[] decrypted = aes.decryptBlock(encrypted);

    private static final int[] S_BOX = new int[]{
        0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
        0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
        0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
        0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
        0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
        0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
        0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
        0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
        0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
        0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
        0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
        0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
        0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
        0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
        0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
        0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
    };

    private static final int[] INV_S_BOX = new int[256];
    private static final int[] RCON = new int[]{0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36};

    static {
        for (int i = 0; i < 256; i++) {
            INV_S_BOX[S_BOX[i]] = i;
        }
    }

    private final List<byte[]> roundKeys;

    public AES(byte[] key) {
        this.roundKeys = expandKey(key);
    }

    // =========================
    // PUBLIC API
    // =========================

    public byte[] encryptBlock(byte[] block) {
        byte[][] state = toState(block);

        addRoundKey(state, roundKeys.get(0));

        for (int r = 1; r < 14; r++) {
            subBytes(state);
            shiftRows(state);
            mixColumns(state);
            addRoundKey(state, roundKeys.get(r));
        }

        subBytes(state);
        shiftRows(state);
        addRoundKey(state, roundKeys.get(14));

        return fromState(state);
    }

    public byte[] decryptBlock(byte[] block) {
        byte[][] state = toState(block);

        addRoundKey(state, roundKeys.get(14));

        for (int r = 13; r > 0; r--) {
            invShiftRows(state);
            invSubBytes(state);
            addRoundKey(state, roundKeys.get(r));
            invMixColumns(state);
        }

        invShiftRows(state);
        invSubBytes(state);
        addRoundKey(state, roundKeys.get(0));

        return fromState(state);
    }

    // =========================
    // CORE AES
    // =========================

    private static byte[][] toState(byte[] block) {
        byte[][] state = new byte[4][4];
        for (int c = 0; c < 4; c++) {
            for (int r = 0; r < 4; r++) {
                state[r][c] = block[c * 4 + r];
            }
        }
        return state;
    }

    private static byte[] fromState(byte[][] state) {
        byte[] out = new byte[16];
        for (int c = 0; c < 4; c++) {
            for (int r = 0; r < 4; r++) {
                out[c * 4 + r] = state[r][c];
            }
        }
        return out;
    }

    private static void addRoundKey(byte[][] state, byte[] roundKey) {
        for (int c = 0; c < 4; c++) {
            for (int r = 0; r < 4; r++) {
                state[r][c] ^= roundKey[c * 4 + r];
            }
        }
    }

    private static void subBytes(byte[][] state) {
        for (int r = 0; r < 4; r++) {
            for (int c = 0; c < 4; c++) {
                state[r][c] = (byte) S_BOX[state[r][c] & 0xFF];
            }
        }
    }

    private static void invSubBytes(byte[][] state) {
        for (int r = 0; r < 4; r++) {
            for (int c = 0; c < 4; c++) {
                state[r][c] = (byte) INV_S_BOX[state[r][c] & 0xFF];
            }
        }
    }

    private static void shiftRows(byte[][] state) {
        state[1] = rotateLeft(state[1], 1);
        state[2] = rotateLeft(state[2], 2);
        state[3] = rotateLeft(state[3], 3);
    }

    private static void invShiftRows(byte[][] state) {
        state[1] = rotateRight(state[1], 1);
        state[2] = rotateRight(state[2], 2);
        state[3] = rotateRight(state[3], 3);
    }

    private static void mixColumns(byte[][] state) {
        for (int c = 0; c < 4; c++) {
            int a0 = state[0][c] & 0xFF;
            int a1 = state[1][c] & 0xFF;
            int a2 = state[2][c] & 0xFF;
            int a3 = state[3][c] & 0xFF;

            state[0][c] = (byte) (gfMul(a0,2)^gfMul(a1,3)^a2^a3);
            state[1][c] = (byte) (a0^gfMul(a1,2)^gfMul(a2,3)^a3);
            state[2][c] = (byte) (a0^a1^gfMul(a2,2)^gfMul(a3,3));
            state[3][c] = (byte) (gfMul(a0,3)^a1^a2^gfMul(a3,2));
        }
    }

    private static void invMixColumns(byte[][] state) {
        for (int c = 0; c < 4; c++) {
            int a0 = state[0][c] & 0xFF;
            int a1 = state[1][c] & 0xFF;
            int a2 = state[2][c] & 0xFF;
            int a3 = state[3][c] & 0xFF;

            state[0][c] = (byte) (gfMul(a0,14)^gfMul(a1,11)^gfMul(a2,13)^gfMul(a3,9));
            state[1][c] = (byte) (gfMul(a0,9)^gfMul(a1,14)^gfMul(a2,11)^gfMul(a3,13));
            state[2][c] = (byte) (gfMul(a0,13)^gfMul(a1,9)^gfMul(a2,14)^gfMul(a3,11));
            state[3][c] = (byte) (gfMul(a0,11)^gfMul(a1,13)^gfMul(a2,9)^gfMul(a3,14));
        }
    }

    // =========================
    // KEY EXPANSION
    // =========================

    private static List<byte[]> expandKey(byte[] key) {
        List<byte[]> words = new ArrayList<>();

        for (int i = 0; i < 32; i += 4) {
            words.add(new byte[]{key[i],key[i+1],key[i+2],key[i+3]});
        }

        while (words.size() < 60) {
            byte[] temp = words.get(words.size() - 1).clone();
            int i = words.size();

            if (i % 8 == 0) {
                temp = subWord(rotWord(temp));
                temp[0] ^= (byte) RCON[i/8 - 1];
            } else if (i % 8 == 4) {
                temp = subWord(temp);
            }

            byte[] prev = words.get(i - 8);
            byte[] newWord = new byte[4];

            for (int j = 0; j < 4; j++) {
                newWord[j] = (byte) (prev[j] ^ temp[j]);
            }

            words.add(newWord);
        }

        List<byte[]> roundKeys = new ArrayList<>();

        for (int r = 0; r < 15; r++) {
            byte[] rk = new byte[16];
            for (int j = 0; j < 4; j++) {
                System.arraycopy(words.get(r*4+j), 0, rk, j*4, 4);
            }
            roundKeys.add(rk);
        }

        return roundKeys;
    }

    private static byte[] rotWord(byte[] w) {
        return new byte[]{w[1],w[2],w[3],w[0]};
    }

    private static byte[] subWord(byte[] w) {
        return new byte[]{
            (byte) S_BOX[w[0] & 0xFF],
            (byte) S_BOX[w[1] & 0xFF],
            (byte) S_BOX[w[2] & 0xFF],
            (byte) S_BOX[w[3] & 0xFF]
        };
    }

    // =========================
    // UTILS
    // =========================

    private static byte[] rotateLeft(byte[] arr, int n) {
        byte[] out = new byte[4];
        for (int i = 0; i < 4; i++) {
            out[i] = arr[(i + n) % 4];
        }
        return out;
    }

    private static byte[] rotateRight(byte[] arr, int n) {
        byte[] out = new byte[4];
        for (int i = 0; i < 4; i++) {
            out[(i + n) % 4] = arr[i];
        }
        return out;
    }

    private static int gfMul(int a, int b) {
        int result = 0;
        for (int i = 0; i < 8; i++) {
            if ((b & 1) != 0) result ^= a;
            boolean high = (a & 0x80) != 0;
            a = (a << 1) & 0xFF;
            if (high) a ^= 0x1B;
            b >>= 1;
        }
        return result;
    }
}
