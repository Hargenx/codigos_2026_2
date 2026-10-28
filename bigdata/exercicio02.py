eventos = [
    {"id": 1, "temp": 28.5, "ts": "2026-10-28T10:00:00"},
    {"id": 2, "temp": None, "ts": "2026-10-28T10:00:01"},
    {"id": 3, "temp": 250, "ts": "2026-10-28T10:00:02"},
]

validos = []
quarentena = []

for evento in eventos:
    temp = evento.get("temp")

    if temp is None:
        quarentena.append((evento, "temp ausente"))
    elif not -50 <= temp <= 150:
        quarentena.append((evento, "temp fora do intervalo"))
    else:
        validos.append(evento)

print(validos)
print(quarentena)
