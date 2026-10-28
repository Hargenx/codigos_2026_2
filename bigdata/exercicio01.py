EVENTOS_S = 75_000
BYTES_EVENTO = 900
REPLICACAO = 3

bytes_dia = EVENTOS_S * BYTES_EVENTO * 86_400
tb_dia = bytes_dia / 1_000_000_000_000
tb_fisico = tb_dia * REPLICACAO

print(f"Bruto: {tb_dia:.2f} TB/dia")
print(f"HDFS:  {tb_fisico:.2f} TB/dia")
