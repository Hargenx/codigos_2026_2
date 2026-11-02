import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from banco import Banco
from negocio import ErroNegocio, Loja, preco_em_centavos, reais


class TestVendaCerta(unittest.TestCase):
    def setUp(self) -> None:
        self.pasta = tempfile.TemporaryDirectory()
        self.loja = Loja(Banco(Path(self.pasta.name) / "teste.db"))
        self.mouse = self.loja.cadastrar_produto("MOU-01", "Mouse", 4990, 5, 2)
        self.teclado = self.loja.cadastrar_produto("TEC-01", "Teclado", 8990, 1, 1)

    def tearDown(self) -> None:
        self.pasta.cleanup()

    def estoque(self, produto_id: int) -> int:
        return next(p["estoque"] for p in self.loja.produtos() if p["id"] == produto_id)

    def test_preco_brasileiro_e_formatacao(self):
        self.assertEqual(preco_em_centavos("12,50"), 1250)
        self.assertEqual(preco_em_centavos("12.5"), 1250)
        self.assertEqual(reais(123456), "R$ 1.234,56")

    def test_preco_invalido_e_centavos_extras(self):
        for valor in ["", "1,234", "-20", "0", "1.234,56", "abc"]:
            with self.subTest(valor=valor), self.assertRaises(ErroNegocio):
                preco_em_centavos(valor)

    def test_sku_nao_pode_repetir(self):
        with self.assertRaisesRegex(ErroNegocio, "SKU"):
            self.loja.cadastrar_produto("mou-01", "Outra coisa", 100, 0, 0)

    def test_cadastro_valida_estoque(self):
        with self.assertRaises(ErroNegocio):
            self.loja.cadastrar_produto("XXX", "Incorreto", 999, -1, 0)

    def test_entrada_estoque(self):
        self.loja.receber_estoque(self.teclado, 4)
        self.assertEqual(self.estoque(self.teclado), 5)

    def test_recebimento_nega_quantidade_zero(self):
        with self.assertRaises(ErroNegocio):
            self.loja.receber_estoque(self.mouse, 0)

    def test_venda_multiplos_itens_total_e_estoque(self):
        venda_id = self.loja.vender("Maria", [(self.mouse, 2), (self.teclado, 1)])
        venda = self.loja.vendas()[0]
        self.assertEqual(venda["id"], venda_id)
        self.assertEqual(venda["total_centavos"], 18970)
        self.assertEqual(venda["cliente"], "Maria")
        self.assertEqual(self.estoque(self.mouse), 3)
        self.assertEqual(self.estoque(self.teclado), 0)
        self.assertEqual(len(self.loja.itens_da_venda(venda_id)), 2)

    def test_venda_agrega_linhas_iguais(self):
        venda_id = self.loja.vender("", [(self.mouse, 1), (self.mouse, 2)])
        self.assertEqual(self.loja.vendas()[0]["cliente"], "Consumidor final")
        self.assertEqual(self.loja.vendas()[0]["total_centavos"], 14970)
        self.assertEqual(len(self.loja.itens_da_venda(venda_id)), 1)
        self.assertEqual(self.estoque(self.mouse), 2)

    def test_falta_estoque_reverte_toda_a_venda(self):
        with self.assertRaisesRegex(ErroNegocio, "Estoque insuficiente"):
            self.loja.vender("Ana", [(self.mouse, 2), (self.teclado, 3)])
        self.assertEqual(self.estoque(self.mouse), 5)
        self.assertEqual(self.estoque(self.teclado), 1)
        self.assertEqual(len(self.loja.vendas()), 0)

    def test_nao_permite_carrinho_vazio(self):
        with self.assertRaises(ErroNegocio):
            self.loja.vender("Ana", [])

    def test_cancelamento_restitui_estoque_apenas_uma_vez(self):
        venda_id = self.loja.vender("Ana", [(self.mouse, 2)])
        self.loja.cancelar_venda(venda_id)
        self.assertEqual(self.estoque(self.mouse), 5)
        self.assertEqual(self.loja.vendas()[0]["status"], "CANCELADA")
        with self.assertRaises(ErroNegocio):
            self.loja.cancelar_venda(venda_id)
        self.assertEqual(self.estoque(self.mouse), 5)

    def test_venda_preserva_preco_historico_apos_edicao(self):
        venda_id = self.loja.vender("", [(self.mouse, 1)])
        self.loja.atualizar_produto(self.mouse, "MOU-01", "Mouse atualizado", 6990, 3)
        item = self.loja.itens_da_venda(venda_id)[0]
        self.assertEqual(item["preco_centavos"], 4990)
        self.assertEqual(item["nome"], "Mouse")
        self.assertEqual(self.estoque(self.mouse), 4)

    def test_resumo_exclui_canceladas(self):
        v1 = self.loja.vender("A", [(self.mouse, 1)])
        self.loja.vender("B", [(self.teclado, 1)])
        self.loja.cancelar_venda(v1)
        self.assertEqual(self.loja.resumo(), (8990, 1, 1))

    def test_demo_somente_em_loja_vazia(self):
        with tempfile.TemporaryDirectory() as pasta:
            loja = Loja(Banco(Path(pasta) / "nova.db"))
            self.assertEqual(loja.carregar_demonstracao(), 5)
            with self.assertRaises(ErroNegocio):
                loja.carregar_demonstracao()


if __name__ == "__main__":
    unittest.main()
