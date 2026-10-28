import sys

atual, total = None, 0.0
for linha in sys.stdin:
    regiao, valor = linha.strip().split("\t")
    valor = float(valor)
    if atual is not None and regiao != atual:
        print(f"{atual}\t{total:.2f}")
        total = 0.0
    atual = regiao
    total += valor
if atual is not None:
    print(f"{atual}\t{total:.2f}")
