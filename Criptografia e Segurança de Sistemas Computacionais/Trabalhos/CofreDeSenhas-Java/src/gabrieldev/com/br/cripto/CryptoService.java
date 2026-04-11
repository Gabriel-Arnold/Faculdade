package gabrieldev.com.br.cripto;

import java.security.SecureRandom;
import java.util.Arrays;

import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class CryptoService {

    private static final int BLOCK_SIZE = 16;
    private static final int KEY_SIZE = 32;
    private static final int SALT_SIZE = 16;
    private static final int IV_SIZE = 16;
    private static final int PBKDF2_ITERATIONS = 100000;

    public static EncryptedData encrypt(byte[] plaintext, String password) throws Exception {
        byte[] salt = randomBytes(SALT_SIZE);
        byte[] iv = randomBytes(IV_SIZE);
        byte[] key = deriveKey(password, salt);

        byte[] padded = pad(plaintext);
        byte[] ciphertext = encryptCbc(padded, key, iv);

        return new EncryptedData(salt, iv, ciphertext);
    }

    public static byte[] decrypt(byte[] salt, byte[] iv, byte[] ciphertext, String password) throws Exception {
        byte[] key = deriveKey(password, salt);
        byte[] padded = decryptCbc(ciphertext, key, iv);
        return unpad(padded);
    }

    public static byte[] deriveKey(String password, byte[] salt) throws Exception {
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, PBKDF2_ITERATIONS, KEY_SIZE * 8);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        return factory.generateSecret(spec).getEncoded();
    }

    private static byte[] randomBytes(int size) {
        byte[] out = new byte[size];
        new SecureRandom().nextBytes(out);
        return out;
    }

    private static byte[] pad(byte[] data) {
        int padding = BLOCK_SIZE - (data.length % BLOCK_SIZE);
        byte[] out = Arrays.copyOf(data, data.length + padding);

        for (int i = data.length; i < out.length; i++) {
            out[i] = (byte) padding;
        }

        return out;
    }

    private static byte[] unpad(byte[] data) {
        if (data.length == 0 || data.length % BLOCK_SIZE != 0) {
            throw new IllegalArgumentException("Padding inválido.");
        }

        int padding = data[data.length - 1] & 0xFF;

        if (padding < 1 || padding > BLOCK_SIZE) {
            throw new IllegalArgumentException("Padding inválido.");
        }

        for (int i = data.length - padding; i < data.length; i++) {
            if ((data[i] & 0xFF) != padding) {
                throw new IllegalArgumentException("Padding inválido.");
            }
        }

        return Arrays.copyOf(data, data.length - padding);
    }

    private static byte[] encryptCbc(byte[] plaintext, byte[] key, byte[] iv) {
        AES aes = new AES(key);
        byte[] output = new byte[plaintext.length];
        byte[] previous = Arrays.copyOf(iv, iv.length);

        for (int i = 0; i < plaintext.length; i += BLOCK_SIZE) {
            byte[] block = Arrays.copyOfRange(plaintext, i, i + BLOCK_SIZE);
            byte[] xored = xor(block, previous);
            byte[] encrypted = aes.encryptBlock(xored);

            System.arraycopy(encrypted, 0, output, i, BLOCK_SIZE);
            previous = encrypted;
        }

        return output;
    }

    private static byte[] decryptCbc(byte[] ciphertext, byte[] key, byte[] iv) {
        AES aes = new AES(key);
        byte[] output = new byte[ciphertext.length];
        byte[] previous = Arrays.copyOf(iv, iv.length);

        for (int i = 0; i < ciphertext.length; i += BLOCK_SIZE) {
            byte[] block = Arrays.copyOfRange(ciphertext, i, i + BLOCK_SIZE);
            byte[] decrypted = aes.decryptBlock(block);
            byte[] plain = xor(decrypted, previous);

            System.arraycopy(plain, 0, output, i, BLOCK_SIZE);
            previous = block;
        }

        return output;
    }

    private static byte[] xor(byte[] a, byte[] b) {
        byte[] out = new byte[a.length];

        for (int i = 0; i < a.length; i++) {
            out[i] = (byte) (a[i] ^ b[i]);
        }

        return out;
    }
}