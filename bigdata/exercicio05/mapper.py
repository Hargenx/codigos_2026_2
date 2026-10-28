import sys

for linha in sys.stdin:
    regiao, _, valor = linha.strip().split(",")
    print(f"{regiao}\t{float(valor)}")