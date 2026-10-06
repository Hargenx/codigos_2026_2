# main.py

from datetime import date

from banco import BancoDeDados
from marca import Marca
from pessoa import Pessoa
from veiculo import Veiculo


def main() -> None:
    pessoa1 = Pessoa(
        cpf="12345678900",
        nome="Raphael",
        nascimento=date(1984, 7, 26),
        oculos=True,
    )

    marca1 = Marca(
        id=1,
        nome="Fiat",
        sigla="FIA",
    )

    veiculo1 = Veiculo(
        placa="RMS2264",
        cor="Cinza",
        proprietario=pessoa1,
        marca=marca1,
    )

    with BancoDeDados() as banco:
        banco.criar_tabelas()

        # -----------------------------------------------------
        # INSERT
        # -----------------------------------------------------

        if banco.buscar_pessoa_por_cpf(
            pessoa1.cpf
        ) is None:
            banco.inserir_pessoa(pessoa1)

        if banco.buscar_marca_por_id(
            marca1.id
        ) is None:
            banco.inserir_marca(marca1)

        if banco.buscar_veiculo_por_placa(
            veiculo1.placa
        ) is None:
            banco.inserir_veiculo(veiculo1)

        # -----------------------------------------------------
        # SELECT
        # -----------------------------------------------------

        print("\nPESSOAS")
        print("-" * 50)

        for pessoa in banco.buscar_todas_pessoas():
            print(
                f"CPF: {pessoa.cpf} | "
                f"Nome: {pessoa.nome} | "
                f"Nascimento: {pessoa.nascimento} | "
                f"Óculos: {pessoa.oculos}"
            )

        print("\nMARCAS")
        print("-" * 50)

        for marca in banco.buscar_todas_marcas():
            print(
                f"ID: {marca.id} | "
                f"Nome: {marca.nome} | "
                f"Sigla: {marca.sigla}"
            )

        print("\nVEÍCULOS")
        print("-" * 50)

        for veiculo in banco.buscar_todos_veiculos():
            print(
                f"Placa: {veiculo.placa} | "
                f"Cor: {veiculo.cor}"
            )

            print(
                f"  Proprietário: "
                f"{veiculo.proprietario.nome}"
            )

            print(
                f"  Marca: "
                f"{veiculo.marca.nome}"
            )

        # -----------------------------------------------------
        # BUSCA POR CPF
        # -----------------------------------------------------

        print("\nBUSCA POR CPF")
        print("-" * 50)

        pessoa = banco.buscar_pessoa_por_cpf(
            "12345678900"
        )

        if pessoa:
            print(pessoa)

        # -----------------------------------------------------
        # VEÍCULOS DE UMA PESSOA
        # -----------------------------------------------------

        print("\nVEÍCULOS DA PESSOA")
        print("-" * 50)

        veiculos = banco.buscar_veiculos_da_pessoa(
            "12345678900"
        )

        for veiculo in veiculos:
            print(
                f"{veiculo.placa} - "
                f"{veiculo.cor} - "
                f"{veiculo.marca.nome}"
            )

        # -----------------------------------------------------
        # UPDATE COMPLETO
        # -----------------------------------------------------

        pessoa_atualizada = Pessoa(
            cpf="12345678900",
            nome="Raphael Mauricio",
            nascimento=date(1984, 7, 26),
            oculos=False,
        )

        banco.atualizar_pessoa(
            pessoa_atualizada
        )

        # -----------------------------------------------------
        # UPDATE DINÂMICO E SEGURO
        # -----------------------------------------------------

        banco.atualizar_pessoa_campos(
            "12345678900",
            nome="Raphael M. S. de Jesus",
            oculos=True,
        )

        # -----------------------------------------------------
        # UPDATE VEÍCULO
        # -----------------------------------------------------

        veiculo_atualizado = Veiculo(
            placa="LRW1I27",
            cor="Preto",
            proprietario=pessoa_atualizada,
            marca=marca1,
        )

        banco.atualizar_veiculo(
            veiculo_atualizado
        )

        # -----------------------------------------------------
        # ALTER TABLE
        # -----------------------------------------------------

        banco.adicionar_coluna_motor()

        # -----------------------------------------------------
        # DELETE
        #
        # Descomente caso queira testar.
        #
        # É necessário apagar primeiro o veículo, pois ele
        # possui uma chave estrangeira apontando para Pessoa.
        # -----------------------------------------------------

        # banco.apagar_veiculo("LRW1I27")
        # banco.apagar_pessoa("12345678900")


if __name__ == "__main__":
    main()