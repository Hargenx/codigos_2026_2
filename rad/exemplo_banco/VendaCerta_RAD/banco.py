import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


class Banco:
    def __init__(self, caminho: str | Path):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.criar_tabelas()

    @contextmanager
    def conectar(self) -> Iterator[sqlite3.Connection]:
        conexao = sqlite3.connect(self.caminho, timeout=10)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        try:
            with conexao:
                yield conexao
        finally:
            conexao.close()

    def criar_tabelas(self) -> None:
        with self.conectar() as conexao:
            conexao.executescript("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY,
                    sku TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    preco_centavos INTEGER NOT NULL CHECK(preco_centavos > 0),
                    estoque INTEGER NOT NULL DEFAULT 0 CHECK(estoque >= 0),
                    minimo INTEGER NOT NULL DEFAULT 0 CHECK(minimo >= 0)
                );
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY,
                    criada_em TEXT NOT NULL,
                    cliente TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'CONCLUIDA'
                        CHECK(status IN ('CONCLUIDA', 'CANCELADA')),
                    total_centavos INTEGER NOT NULL CHECK(total_centavos > 0)
                );
                CREATE TABLE IF NOT EXISTS itens_venda (
                    id INTEGER PRIMARY KEY,
                    venda_id INTEGER NOT NULL REFERENCES vendas(id),
                    produto_id INTEGER NOT NULL REFERENCES produtos(id),
                    sku TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                    preco_centavos INTEGER NOT NULL CHECK(preco_centavos > 0),
                    subtotal_centavos INTEGER NOT NULL CHECK(subtotal_centavos > 0)
                );
            """)
