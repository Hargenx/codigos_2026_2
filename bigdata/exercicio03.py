lote = [
    {"event_id": "a1", "valor": 10},
    {"event_id": "a2", "valor": 20},
    {"event_id": "a1", "valor": 10},
]

vistos = set()
saida = []

for evento in lote:
    chave = evento["event_id"]

    if chave not in vistos:
        vistos.add(chave)
        saida.append(evento)


print(saida)
