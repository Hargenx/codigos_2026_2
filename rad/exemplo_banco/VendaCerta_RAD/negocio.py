import re
import sqlite3
from collections.abc import Sequence
from datetime import datetime
from decimal import Decimal

from banco import Banco


class ErroNegocio(ValueError):
    """Regra de negócio violada por uma operação do usuário."""


def preco_em_centavos(valor: str) -> int:
    """Aceita valores simples em reais: 12,50 ou 12.50 (sem milhar)."""
    valor = valor.strip()
    if not re.fullmatch(r"\d+(?:[,.]\d{1,2})?", valor):
        raise ErroNegocio("Preço inválido. Exemplo: 89,90 (sem separador de milhar).")
    centavos = int(Decimal(valor.replace(",", ".")) * 100)
    if centavos <= 0:
        raise ErroNegocio("O preço deve ser maior que zero.")
    return centavos


def reais(centavos: int) -> str:
    inteiros, cent = divmod(centavos, 100)
    milhares = f"{inteiros:,}".replace(",", ".")
    return f"R$ {milhares},{cent:02d}"


def inteiro_nao_negativo(valor: int, campo: str) -> int:
    if type(valor) is not int or valor < 0:
        raise ErroNegocio(f"{campo} deve ser um inteiro maior ou igual a zero.")
    return valor


class Loja:
    def __init__(self, banco: Banco):
        self.banco = banco

    def cadastrar_produto(self, sku: str, nome: str, preco: int,
                          estoque: int, minimo: int) -> int:
        sku, nome = sku.strip().upper(), nome.strip()
        if not sku or not nome:
            raise ErroNegocio("SKU e nome são obrigatórios.")
        if not isinstance(preco, int) or preco <= 0:
            raise ErroNegocio("O preço deve ser positivo.")
        inteiro_nao_negativo(estoque, "Estoque")
        inteiro_nao_negativo(minimo, "Estoque mínimo")
        try:
            with self.banco.conectar() as con:
                cur = con.execute(
                    "INSERT INTO produtos (sku, nome, preco_centavos, estoque, minimo) "
                    "VALUES (?, ?, ?, ?, ?)", (sku, nome, preco, estoque, minimo))
                return int(cur.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise ErroNegocio("Já existe um produto com esse SKU.") from exc

    def atualizar_produto(self, produto_id: int, sku: str, nome: str,
                          preco: int, minimo: int) -> None:
        sku, nome = sku.strip().upper(), nome.strip()
        if not sku or not nome or preco <= 0:
            raise ErroNegocio("Informe SKU, nome e preço válido.")
        inteiro_nao_negativo(minimo, "Estoque mínimo")
        try:
            with self.banco.conectar() as con:
                cur = con.execute(
                    "UPDATE produtos SET sku=?, nome=?, preco_centavos=?, minimo=? WHERE id=?",
                    (sku, nome, preco, minimo, produto_id))
                if cur.rowcount == 0:
                    raise ErroNegocio("Produto não encontrado.")
        except sqlite3.IntegrityError as exc:
            raise ErroNegocio("Já existe um produto com esse SKU.") from exc

    def receber_estoque(self, produto_id: int, quantidade: int) -> None:
        if type(quantidade) is not int or quantidade <= 0:
            raise ErroNegocio("A quantidade recebida deve ser positiva.")
        with self.banco.conectar() as con:
            cur = con.execute(
                "UPDATE produtos SET estoque=estoque+? WHERE id=?",
                (quantidade, produto_id))
            if cur.rowcount == 0:
                raise ErroNegocio("Produto não encontrado.")

    def produtos(self) -> list[sqlite3.Row]:
        with self.banco.conectar() as con:
            return con.execute("SELECT * FROM produtos ORDER BY nome, id").fetchall()

    def vender(self, cliente: str, itens: Sequence[tuple[int, int]]) -> int:
        """Vende vários itens atomicamente; preços são consultados no banco."""
        if not itens:
            raise ErroNegocio("Adicione pelo menos um produto à venda.")
        cliente = cliente.strip() or "Consumidor final"
        if len(cliente) > 100:
            raise ErroNegocio("O nome do cliente tem no máximo 100 caracteres.")
        unicos: dict[int, int] = {}
        for produto_id, quantidade in itens:
            if type(produto_id) is not int or type(quantidade) is not int or quantidade <= 0:
                raise ErroNegocio("Itens e quantidades devem ser inteiros positivos.")
            unicos[produto_id] = unicos.get(produto_id, 0) + quantidade

        with self.banco.conectar() as con:
            con.execute("BEGIN IMMEDIATE")  # Bloqueia outra escrita enquanto confere o estoque.
            linhas = []
            total = 0
            for produto_id, quantidade in unicos.items():
                produto = con.execute(
                    "SELECT * FROM produtos WHERE id=?", (produto_id,)).fetchone()
                if produto is None:
                    raise ErroNegocio(f"Produto #{produto_id} não encontrado.")
                if produto["estoque"] < quantidade:
                    raise ErroNegocio(
                        f"Estoque insuficiente de {produto['nome']}: "
                        f"disponível {produto['estoque']}, solicitado {quantidade}.")
                subtotal = produto["preco_centavos"] * quantidade
                total += subtotal
                linhas.append((produto, quantidade, subtotal))

            cur = con.execute(
                "INSERT INTO vendas (criada_em, cliente, total_centavos) VALUES (?, ?, ?)",
                (datetime.now().astimezone().isoformat(timespec="seconds"), cliente, total))
            venda_id = int(cur.lastrowid)
            for produto, quantidade, subtotal in linhas:
                atualizado = con.execute(
                    "UPDATE produtos SET estoque=estoque-? WHERE id=? AND estoque>=?",
                    (quantidade, produto["id"], quantidade))
                if atualizado.rowcount != 1:
                    raise ErroNegocio("O estoque mudou durante a venda. Tente novamente.")
                con.execute(
                    "INSERT INTO itens_venda "
                    "(venda_id, produto_id, sku, nome, quantidade, preco_centavos, subtotal_centavos) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (venda_id, produto["id"], produto["sku"], produto["nome"],
                     quantidade, produto["preco_centavos"], subtotal))
            return venda_id

    def cancelar_venda(self, venda_id: int) -> None:
        """Cancela somente uma vez e devolve as quantidades ao estoque."""
        with self.banco.conectar() as con:
            con.execute("BEGIN IMMEDIATE")
            venda = con.execute(
                "SELECT status FROM vendas WHERE id=?", (venda_id,)).fetchone()
            if venda is None:
                raise ErroNegocio("Venda não encontrada.")
            if venda["status"] != "CONCLUIDA":
                raise ErroNegocio("Essa venda já foi cancelada.")
            itens = con.execute(
                "SELECT produto_id, quantidade FROM itens_venda WHERE venda_id=?",
                (venda_id,)).fetchall()
            for item in itens:
                con.execute("UPDATE produtos SET estoque=estoque+? WHERE id=?",
                            (item["quantidade"], item["produto_id"]))
            con.execute("UPDATE vendas SET status='CANCELADA' WHERE id=?", (venda_id,))

    def vendas(self) -> list[sqlite3.Row]:
        with self.banco.conectar() as con:
            return con.execute("SELECT * FROM vendas ORDER BY id DESC").fetchall()

    def itens_da_venda(self, venda_id: int) -> list[sqlite3.Row]:
        with self.banco.conectar() as con:
            return con.execute("SELECT * FROM itens_venda WHERE venda_id=? ORDER BY id",
                               (venda_id,)).fetchall()

    def resumo(self) -> tuple[int, int, int]:
        """Retorna total faturado, número de vendas concluídas e alertas de estoque."""
        with self.banco.conectar() as con:
            resumo = con.execute(
                "SELECT COALESCE(SUM(total_centavos),0), COUNT(*) FROM vendas "
                "WHERE status='CONCLUIDA'").fetchone()
            alertas = con.execute(
                "SELECT COUNT(*) FROM produtos WHERE estoque<=minimo").fetchone()[0]
            return int(resumo[0]), int(resumo[1]), int(alertas)

    def carregar_demonstracao(self) -> int:
        """Insere catálogo fictício apenas quando a loja não tem produtos."""
        exemplos = [
            ("MOU-USB", "Mouse USB", 4990, 15, 4),
            ("TEC-ABNT", "Teclado ABNT2", 8990, 8, 2),
            ("CAB-HDMI", "Cabo HDMI 2 m", 3590, 20, 5),
            ("SSD-500", "SSD 500 GB", 29990, 6, 2),
            ("FON-500", "Fonte 500 W", 23990, 4, 2),
        ]
        with self.banco.conectar() as con:
            if con.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]:
                raise ErroNegocio("O catálogo de demonstração só pode ser carregado em uma loja vazia.")
            con.executemany(
                "INSERT INTO produtos (sku, nome, preco_centavos, estoque, minimo) "
                "VALUES (?, ?, ?, ?, ?)", exemplos)
        return len(exemplos)
