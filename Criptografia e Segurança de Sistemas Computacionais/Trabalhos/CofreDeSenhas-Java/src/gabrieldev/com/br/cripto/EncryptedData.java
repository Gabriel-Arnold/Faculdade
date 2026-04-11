package gabrieldev.com.br.cripto;

public class EncryptedData {

    private final byte[] salt;
    private final byte[] iv;
    private final byte[] ciphertext;

    public EncryptedData(byte[] salt, byte[] iv, byte[] ciphertext) {
        this.salt = salt;
        this.iv = iv;
        this.ciphertext = ciphertext;
    }

    public byte[] getSalt() {
        return salt;
    }

    public byte[] getIv() {
        return iv;
    }

    public byte[] getCiphertext() {
        return ciphertext;
    }
}