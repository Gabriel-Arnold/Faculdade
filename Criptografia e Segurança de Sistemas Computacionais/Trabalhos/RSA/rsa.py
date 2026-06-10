import argparse
import base64
import json
from pathlib import Path


N = 125423226362721279485400322243712478923500891808454136005118175374819944016038670052917978202912662999293147065596484572049211448747873888088178315440481859596137981522539346521336785055950809893357400033240226180002656609817819318390052242999411441809193872193553976814838218887172219522295577954497951544837
E = 65537
D = 55229700621050298376019163215150196518810934841390022597490050248591311234247218808568593816589965080742190383539816413091355924125530502408360742867340057260140639581900433343993227953482707575513526364823391209000319181126515321726188922079679852696833444003558698816231663857136925071856378006462225661253


def tamanho_bloco() -> int:
    tamanho_modulo = (N.bit_length() + 7) // 8
    return tamanho_modulo - 1


def cifrar_arquivo(nome_arquivo: str) -> Path:
    origem = Path(nome_arquivo)
    dados = origem.read_bytes()
    bloco_bytes = tamanho_bloco()
    blocos = []

    for inicio in range(0, len(dados), bloco_bytes):
        bloco = dados[inicio : inicio + bloco_bytes]
        numero = int.from_bytes(bloco, byteorder="big")
        cifrado = pow(numero, E, N)
        blocos.append([len(bloco), str(cifrado)])

    pacote = {"algoritmo": "RSA", "blocos": blocos}
    conteudo_json = json.dumps(pacote, separators=(",", ":"))
    conteudo_base64 = base64.b64encode(conteudo_json.encode("utf-8")).decode("ascii")

    destino = origem.with_name(origem.name + ".cifrado")
    destino.write_text(conteudo_base64, encoding="utf-8")
    return destino


def decifrar_arquivo(nome_arquivo: str) -> Path:
    origem = Path(nome_arquivo)
    conteudo_base64 = origem.read_text(encoding="utf-8").strip()
    conteudo_json = base64.b64decode(conteudo_base64.encode("ascii")).decode("utf-8")
    pacote = json.loads(conteudo_json)

    partes = []
    for tamanho_original, bloco_cifrado in pacote["blocos"]:
        numero = pow(int(bloco_cifrado), D, N)
        partes.append(numero.to_bytes(int(tamanho_original), byteorder="big"))

    if origem.name.endswith(".cifrado"):
        destino = origem.with_name(origem.name.removesuffix(".cifrado"))
        if destino.exists():
            destino = destino.with_name(destino.name + ".decifrado")
    else:
        destino = origem.with_name(origem.name + ".decifrado")

    destino.write_bytes(b"".join(partes))
    return destino


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aplicacao RSA com dois comandos: cifrar e decifrar."
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    parser_cifrar = subparsers.add_parser("cifrar", help="cifra um arquivo")
    parser_cifrar.add_argument("arquivo", help="nome do arquivo que sera cifrado")

    parser_decifrar = subparsers.add_parser("decifrar", help="decifra um arquivo")
    parser_decifrar.add_argument("arquivo", help="nome do arquivo que sera decifrado")

    return parser


def main() -> None:
    parser = criar_parser()
    args = parser.parse_args()

    if args.comando == "cifrar":
        destino = cifrar_arquivo(args.arquivo)
        print(f"Arquivo cifrado criado: {destino}")
    elif args.comando == "decifrar":
        destino = decifrar_arquivo(args.arquivo)
        print(f"Arquivo decifrado criado: {destino}")


if __name__ == "__main__":
    main()
