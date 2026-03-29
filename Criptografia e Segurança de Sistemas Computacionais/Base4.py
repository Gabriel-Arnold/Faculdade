def encode64(txt):
    resultado = []

    for char in txt:
        ascii_val = ord(char)
        base4 = ""

        while ascii_val > 0:
            base4 = str(ascii_val % 4) + base4
            ascii_val //= 4
        
        base4 = base4.zfill(4)

        resultado.append(base4)

    return " ".join(resultado)

def decode64(txt_codificado):
    resultado = []
    blocos = txt_codificado.split()

    for bloco in blocos:
        decimal = int(bloco, 4)
        char = chr(decimal)
        resultado.append(char)
    
    return "".join(resultado)

msg = "Gabriel"

codificado = encode64(msg)
decodificado = decode64(codificado)

print("Codificado: ", codificado)
print("Decodificado: ", decodificado)

