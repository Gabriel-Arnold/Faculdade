def codificar_base4(texto):
    """Recebe uma string legivel e retorna sua representacao em Base4."""
    bytes_texto = texto.encode("utf-8")
    partes = []

    for byte in bytes_texto:
        digitos = []
        valor = byte

        for _ in range(4):
            digitos.append(str(valor % 4))
            valor //= 4

        partes.append("".join(reversed(digitos)))

    return "".join(partes)


def decodificar_base4(texto_codificado):
    """Recebe uma string em Base4 e retorna o conteudo legivel original."""
    if len(texto_codificado) % 4 != 0:
        raise ValueError("O texto codificado deve ter tamanho multiplo de 4.")

    if any(digito not in "0123" for digito in texto_codificado):
        raise ValueError("O texto codificado deve conter apenas os digitos 0, 1, 2 e 3.")

    bytes_decodificados = bytearray()

    for i in range(0, len(texto_codificado), 4):
        grupo = texto_codificado[i:i + 4]
        bytes_decodificados.append(int(grupo, 4))

    return bytes(bytes_decodificados).decode("utf-8")


if __name__ == "__main__":
    texto_original = input("Digite uma string: ")

    texto_codificado = codificar_base4(texto_original)
    texto_decodificado = decodificar_base4(texto_codificado)

    print("Codificado em Base4:", texto_codificado)
    print("Decodificado:", texto_decodificado)
