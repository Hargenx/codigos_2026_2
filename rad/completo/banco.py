# banco.py

import sqlite3
from pathlib import Path
from typing import Any, ClassVar

from logger_config import logger
from marca import Marca
from pessoa import Pessoa
from veiculo import Veiculo


class BancoDeDados:
    CAMPOS_PESSOA_PERMITIDOS: ClassVar[frozenset[str]] = frozenset(
        {"nome", "nascimento", "oculos"}
    )

    def __init__(self, nome_banco: str = "banco.sqlite") -> None:
        self.caminho_banco = Path(__file__).resolve().parent / nome_banco
        self.conn: sqlite3.Connection | None = None

    def conectar(self) -> None:
        try:
            self.conn = sqlite3.connect(self.caminho_banco)

            self.conn.row_factory = sqlite3.Row

            # O SQLite não habilita a verificação de FKs automaticamente
            # em todas as configurações.
            self.conn.execute("PRAGMA foreign_keys = ON")

            logger.info("Conexão com o banco realizada com sucesso.")

        except sqlite3.Error:
            logger.exception("Erro ao conectar ao banco de dados.")
            raise

    def _obter_conexao(self) -> sqlite3.Connection:
        if self.conn is None:
            raise RuntimeError(
                "Banco de dados não conectado. "
                "Execute conectar() antes de realizar operações."
            )

        return self.conn


    def criar_tabelas(self) -> None:
        conn = self._obter_conexao()

        try:
            with conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Pessoa (
                        cpf TEXT PRIMARY KEY,
                        nome TEXT NOT NULL,
                        nascimento TEXT NOT NULL,
                        oculos INTEGER NOT NULL
                            CHECK (oculos IN (0, 1))
                    )
                    """
                )

                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Marca (
                        id INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL,
                        sigla TEXT NOT NULL
                    )
                    """
                )

                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Veiculo (
                        placa TEXT PRIMARY KEY,
                        cor TEXT NOT NULL,
                        cpf_proprietario TEXT NOT NULL,
                        id_marca INTEGER NOT NULL,

                        FOREIGN KEY (cpf_proprietario)
                            REFERENCES Pessoa(cpf)
                            ON UPDATE CASCADE
                            ON DELETE RESTRICT,

                        FOREIGN KEY (id_marca)
                            REFERENCES Marca(id)
                            ON UPDATE CASCADE
                            ON DELETE RESTRICT
                    )
                    """
                )

            logger.info("Tabelas criadas com sucesso.")

        except sqlite3.IntegrityError:
            logger.exception(
                "Erro de integridade durante a criação das tabelas."
            )
            raise

        except sqlite3.OperationalError:
            logger.exception(
                "Erro operacional durante a criação das tabelas."
            )
            raise

        except sqlite3.DatabaseError:
            logger.exception(
                "Erro de banco durante a criação das tabelas."
            )
            raise

        except sqlite3.Error:
            logger.exception(
                "Erro geral do SQLite durante a criação das tabelas."
            )
            raise

    def adicionar_coluna_motor(self) -> None:
        conn = self._obter_conexao()

        try:
            colunas = conn.execute(
                "PRAGMA table_info(Veiculo)"
            ).fetchall()

            nomes_colunas = {
                coluna["name"]
                for coluna in colunas
            }

            if "motor" in nomes_colunas:
                logger.info(
                    "A coluna 'motor' já existe na tabela Veiculo."
                )
                return

            with conn:
                conn.execute(
                    """
                    ALTER TABLE Veiculo
                    ADD COLUMN motor TEXT
                    """
                )

            logger.info(
                "Coluna 'motor' adicionada com sucesso."
            )

        except sqlite3.Error:
            logger.exception(
                "Erro ao adicionar coluna à tabela Veiculo."
            )
            raise

    def inserir_pessoa(self, pessoa: Pessoa) -> None:
        conn = self._obter_conexao()

        try:
            with conn:
                conn.execute(
                    """
                    INSERT INTO Pessoa (
                        cpf,
                        nome,
                        nascimento,
                        oculos
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        pessoa.cpf,
                        pessoa.nome,
                        pessoa.nascimento.isoformat(),
                        int(pessoa.oculos),
                    ),
                )

            logger.info(
                "Pessoa %s inserida com sucesso.",
                pessoa.cpf,
            )

        except sqlite3.IntegrityError:
            logger.exception(
                "Erro de integridade ao inserir pessoa %s.",
                pessoa.cpf,
            )
            raise

        except sqlite3.Error:
            logger.exception(
                "Erro ao inserir pessoa %s.",
                pessoa.cpf,
            )
            raise

    def inserir_marca(self, marca: Marca) -> None:
        conn = self._obter_conexao()

        try:
            with conn:
                conn.execute(
                    """
                    INSERT INTO Marca (
                        id,
                        nome,
                        sigla
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        marca.id,
                        marca.nome,
                        marca.sigla,
                    ),
                )

            logger.info(
                "Marca %s inserida com sucesso.",
                marca.id,
            )

        except sqlite3.IntegrityError:
            logger.exception(
                "Erro de integridade ao inserir marca %s.",
                marca.id,
            )
            raise

        except sqlite3.Error:
            logger.exception(
                "Erro ao inserir marca %s.",
                marca.id,
            )
            raise

    def inserir_veiculo(self, veiculo: Veiculo) -> None:
        conn = self._obter_conexao()

        try:
            with conn:
                conn.execute(
                    """
                    INSERT INTO Veiculo (
                        placa,
                        cor,
                        cpf_proprietario,
                        id_marca
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        veiculo.placa,
                        veiculo.cor,
                        veiculo.proprietario.cpf,
                        veiculo.marca.id,
                    ),
                )

            logger.info(
                "Veículo %s inserido com sucesso.",
                veiculo.placa,
            )

        except sqlite3.IntegrityError:
            logger.exception(
                "Erro de integridade ao inserir veículo %s.",
                veiculo.placa,
            )
            raise

        except sqlite3.Error:
            logger.exception(
                "Erro ao inserir veículo %s.",
                veiculo.placa,
            )
            raise

    def atualizar_pessoa(self, pessoa: Pessoa) -> None:
        conn = self._obter_conexao()

        try:
            with conn:
                cursor = conn.execute(
                    """
                    UPDATE Pessoa
                    SET
                        nome = ?,
                        nascimento = ?,
                        oculos = ?
                    WHERE cpf = ?
                    """,
                    (
                        pessoa.nome,
                        pessoa.nascimento.isoformat(),
                        int(pessoa.oculos),
                        pessoa.cpf,
                    ),
                )

            if cursor.rowcount == 0:
                logger.warning(
                    "Nenhuma pessoa encontrada com CPF %s.",
                    pessoa.cpf,
                )
                return

            logger.info(
                "Pessoa %s atualizada com sucesso.",
                pessoa.cpf,
            )

        except sqlite3.Error:
            logger.exception(
                "Erro ao atualizar pessoa %s.",
                pessoa.cpf,
            )
            raise

    def atualizar_pessoa_campos(
        self,
        cpf: str,
        **campos: Any,
    ) -> None:
        conn = self._obter_conexao()

        if not campos:
            raise ValueError(
                "Informe pelo menos um campo para atualizar."
            )

        campos_invalidos = (
            set(campos)
            - self.CAMPOS_PESSOA_PERMITIDOS
        )

        if campos_invalidos:
            raise ValueError(
                "Campos não permitidos: "
                + ", ".join(sorted(campos_invalidos))
            )

        atribuicoes: list[str] = []
        valores: list[Any] = []

        for nome_campo, valor in campos.items():
            atribuicoes.append(
                f"{nome_campo} = ?"
            )

            if nome_campo == "nascimento":
                valor = valor.isoformat()

            elif nome_campo == "oculos":
                valor = int(valor)

            valores.append(valor)

        valores.append(cpf)

        sql = f"""
            UPDATE Pessoa
            SET {", ".join(atribuicoes)}
            WHERE cpf = ?
        """

        try:
            with conn:
                cursor = conn.execute(
                    sql,
                    tuple(valores),
                )

            if cursor.rowcount == 0:
                logger.warning(
                    "Pessoa %s não encontrada.",
                    cpf,
                )
                return

            logger.info(
                "Pessoa %s atualizada com sucesso.",
                cpf,
            )

        except sqlite3.Error:
            logger.exception(
                "Erro ao atualizar pessoa %s.",
                cpf,
            )
            raise

    def atualizar_veiculo(
        self,
        veiculo: Veiculo,
    ) -> None:
        conn = self._obter_conexao()

        try:
            with conn:
                cursor = conn.execute(
                    """
                    UPDATE Veiculo
                    SET
                        cor = ?,
                        cpf_proprietario = ?,
                        id_marca = ?
                    WHERE placa = ?
                    """,
                    (
                        veiculo.cor,
                        veiculo.proprietario.cpf,
                        veiculo.marca.id,
                        veiculo.placa,
                    ),
                )

            if cursor.rowcount == 0:
                logger.warning(
                    "Veículo %s não encontrado.",
                    veiculo.placa,
                )
                return

            logger.info(
                "Veículo %s atualizado com sucesso.",
                veiculo.placa,
            )

        except sqlite3.IntegrityError:
            logger.exception(
                "Erro de integridade ao atualizar veículo %s.",
                veiculo.placa,
            )
            raise

        except sqlite3.Error:
            logger.exception(
                "Erro ao atualizar veículo %s.",
                veiculo.placa,
            )
            raise

    def apagar_veiculo(
        self,
        placa: str,
    ) -> None:
        conn = self._obter_conexao()

        try:
            with conn:
                cursor = conn.execute(
                    """
                    DELETE FROM Veiculo
                    WHERE placa = ?
                    """,
                    (placa,),
                )

            if cursor.rowcount == 0:
                logger.warning(
                    "Veículo %s não encontrado.",
                    placa,
                )
                return

            logger.info(
                "Veículo %s removido com sucesso.",
                placa,
            )

        except sqlite3.Error:
            logger.exception(
                "Erro ao apagar veículo %s.",
                placa,
            )
            raise

    def apagar_pessoa(
        self,
        cpf: str,
    ) -> None:
        conn = self._obter_conexao()

        try:
            with conn:
                cursor = conn.execute(
                    """
                    DELETE FROM Pessoa
                    WHERE cpf = ?
                    """,
                    (cpf,),
                )

            if cursor.rowcount == 0:
                logger.warning(
                    "Pessoa %s não encontrada.",
                    cpf,
                )
                return

            logger.info(
                "Pessoa %s removida com sucesso.",
                cpf,
            )

        except sqlite3.IntegrityError:
            logger.exception(
                "Não foi possível apagar a pessoa %s "
                "porque existem registros relacionados.",
                cpf,
            )
            raise

        except sqlite3.Error:
            logger.exception(
                "Erro ao apagar pessoa %s.",
                cpf,
            )
            raise

    def buscar_pessoa_por_cpf(
        self,
        cpf: str,
    ) -> Pessoa | None:
        conn = self._obter_conexao()

        try:
            row = conn.execute(
                """
                SELECT
                    cpf,
                    nome,
                    nascimento,
                    oculos
                FROM Pessoa
                WHERE cpf = ?
                """,
                (cpf,),
            ).fetchone()

            if row is None:
                return None

            return Pessoa(
                cpf=row["cpf"],
                nome=row["nome"],
                nascimento=self._converter_data(
                    row["nascimento"]
                ),
                oculos=bool(row["oculos"]),
            )

        except sqlite3.Error:
            logger.exception(
                "Erro ao buscar pessoa %s.",
                cpf,
            )
            raise

    def buscar_todas_pessoas(
        self,
    ) -> list[Pessoa]:
        conn = self._obter_conexao()

        try:
            rows = conn.execute(
                """
                SELECT
                    cpf,
                    nome,
                    nascimento,
                    oculos
                FROM Pessoa
                ORDER BY nome
                """
            ).fetchall()

            return [
                Pessoa(
                    cpf=row["cpf"],
                    nome=row["nome"],
                    nascimento=self._converter_data(
                        row["nascimento"]
                    ),
                    oculos=bool(row["oculos"]),
                )
                for row in rows
            ]

        except sqlite3.Error:
            logger.exception(
                "Erro ao buscar pessoas."
            )
            raise

    def buscar_marca_por_id(
        self,
        id_marca: int,
    ) -> Marca | None:
        conn = self._obter_conexao()

        try:
            row = conn.execute(
                """
                SELECT
                    id,
                    nome,
                    sigla
                FROM Marca
                WHERE id = ?
                """,
                (id_marca,),
            ).fetchone()

            if row is None:
                return None

            return Marca(
                id=row["id"],
                nome=row["nome"],
                sigla=row["sigla"],
            )

        except sqlite3.Error:
            logger.exception(
                "Erro ao buscar marca %s.",
                id_marca,
            )
            raise

    def buscar_todas_marcas(
        self,
    ) -> list[Marca]:
        conn = self._obter_conexao()

        try:
            rows = conn.execute(
                """
                SELECT
                    id,
                    nome,
                    sigla
                FROM Marca
                ORDER BY nome
                """
            ).fetchall()

            return [
                Marca(
                    id=row["id"],
                    nome=row["nome"],
                    sigla=row["sigla"],
                )
                for row in rows
            ]

        except sqlite3.Error:
            logger.exception(
                "Erro ao buscar marcas."
            )
            raise

    def buscar_veiculo_por_placa(
        self,
        placa: str,
    ) -> Veiculo | None:
        conn = self._obter_conexao()

        try:
            row = conn.execute(
                """
                SELECT
                    v.placa,
                    v.cor,

                    p.cpf AS pessoa_cpf,
                    p.nome AS pessoa_nome,
                    p.nascimento AS pessoa_nascimento,
                    p.oculos AS pessoa_oculos,

                    m.id AS marca_id,
                    m.nome AS marca_nome,
                    m.sigla AS marca_sigla

                FROM Veiculo AS v

                INNER JOIN Pessoa AS p
                    ON p.cpf = v.cpf_proprietario

                INNER JOIN Marca AS m
                    ON m.id = v.id_marca

                WHERE v.placa = ?
                """,
                (placa,),
            ).fetchone()

            if row is None:
                return None

            return self._row_para_veiculo(row)

        except sqlite3.Error:
            logger.exception(
                "Erro ao buscar veículo %s.",
                placa,
            )
            raise

    def buscar_todos_veiculos(
        self,
    ) -> list[Veiculo]:
        conn = self._obter_conexao()

        try:
            rows = conn.execute(
                """
                SELECT
                    v.placa,
                    v.cor,

                    p.cpf AS pessoa_cpf,
                    p.nome AS pessoa_nome,
                    p.nascimento AS pessoa_nascimento,
                    p.oculos AS pessoa_oculos,

                    m.id AS marca_id,
                    m.nome AS marca_nome,
                    m.sigla AS marca_sigla

                FROM Veiculo AS v

                INNER JOIN Pessoa AS p
                    ON p.cpf = v.cpf_proprietario

                INNER JOIN Marca AS m
                    ON m.id = v.id_marca

                ORDER BY v.placa
                """
            ).fetchall()

            return [
                self._row_para_veiculo(row)
                for row in rows
            ]

        except sqlite3.Error:
            logger.exception(
                "Erro ao buscar veículos."
            )
            raise

    def buscar_veiculos_da_pessoa(
        self,
        cpf: str,
    ) -> list[Veiculo]:
        conn = self._obter_conexao()

        try:
            rows = conn.execute(
                """
                SELECT
                    v.placa,
                    v.cor,

                    p.cpf AS pessoa_cpf,
                    p.nome AS pessoa_nome,
                    p.nascimento AS pessoa_nascimento,
                    p.oculos AS pessoa_oculos,

                    m.id AS marca_id,
                    m.nome AS marca_nome,
                    m.sigla AS marca_sigla

                FROM Veiculo AS v

                INNER JOIN Pessoa AS p
                    ON p.cpf = v.cpf_proprietario

                INNER JOIN Marca AS m
                    ON m.id = v.id_marca

                WHERE p.cpf = ?

                ORDER BY v.placa
                """,
                (cpf,),
            ).fetchall()

            return [
                self._row_para_veiculo(row)
                for row in rows
            ]

        except sqlite3.Error:
            logger.exception(
                "Erro ao buscar veículos da pessoa %s.",
                cpf,
            )
            raise


    @staticmethod
    def _converter_data(valor: str):
        from datetime import date

        return date.fromisoformat(valor)

    def _row_para_veiculo(
        self,
        row: sqlite3.Row,
    ) -> Veiculo:
        pessoa = Pessoa(
            cpf=row["pessoa_cpf"],
            nome=row["pessoa_nome"],
            nascimento=self._converter_data(
                row["pessoa_nascimento"]
            ),
            oculos=bool(row["pessoa_oculos"]),
        )

        marca = Marca(
            id=row["marca_id"],
            nome=row["marca_nome"],
            sigla=row["marca_sigla"],
        )

        return Veiculo(
            placa=row["placa"],
            cor=row["cor"],
            proprietario=pessoa,
            marca=marca,
        )

    def fechar_conexao(self) -> None:
        if self.conn is not None:
            self.conn.close()
            self.conn = None

            logger.info(
                "Conexão com o banco encerrada."
            )

    def __enter__(self):
        self.conectar()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.fechar_conexao()