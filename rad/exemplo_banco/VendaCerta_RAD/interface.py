import csv
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from negocio import ErroNegocio, Loja, preco_em_centavos, reais


class VendaCertaApp(tk.Tk):
    def __init__(self, loja: Loja):
        super().__init__()
        self.loja = loja
        self.title("VendaCerta | Vendas e Estoque")
        self.geometry("1180x760")
        self.minsize(980, 640)
        self.configure(bg="#eef3f9")
        self.produto_selecionado: int | None = None
        self.carrinho: dict[int, int] = {}
        self.produtos_atuais: dict[int, sqlite3.Row] = {}
        self.opcoes_venda: list[int] = []
        self._estilo()
        self._construir()
        self.atualizar_tudo()

    def _estilo(self) -> None:
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background="#eef3f9")
        s.configure("TLabel", background="#eef3f9", foreground="#243247", font=("Segoe UI", 11))
        s.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#163d70")
        s.configure("Sub.TLabel", font=("Segoe UI", 10), foreground="#536780")
        s.configure("TButton", font=("Segoe UI", 10), padding=(12, 7))
        s.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8),
                    background="#1465a3", foreground="white")
        s.map("Primary.TButton", background=[("active", "#0f4d80")])
        s.configure("TEntry", padding=5)
        s.configure("TCombobox", padding=5)
        s.configure("TNotebook", background="#eef3f9", borderwidth=0)
        s.configure("TNotebook.Tab", padding=(18, 11), font=("Segoe UI", 11))
        s.configure("Treeview", font=("Segoe UI", 10), rowheight=30,
                    background="white", fieldbackground="white", foreground="#263548")
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                    background="#dce9f7", foreground="#163d70", padding=8)
        s.configure("TLabelframe", background="#eef3f9", padding=12)
        s.configure("TLabelframe.Label", background="#eef3f9", foreground="#173e6e",
                    font=("Segoe UI", 11, "bold"))

    def _construir(self) -> None:
        topo = ttk.Frame(self, padding=(22, 18, 22, 8))
        topo.pack(fill="x")
        ttk.Label(topo, text="VendaCerta", style="Title.TLabel").pack(anchor="w")
        ttk.Label(topo, text="Operações de uma loja: cadastro, estoque e vendas com SQLite",
                  style="Sub.TLabel").pack(anchor="w", pady=(2, 12))
        self.indicadores = ttk.Label(topo, text="", font=("Segoe UI", 11, "bold"))
        self.indicadores.pack(anchor="w", pady=(0, 9))

        self.abas = ttk.Notebook(self)
        self.abas.pack(fill="both", expand=True, padx=22, pady=(0, 14))
        self.aba_produtos = ttk.Frame(self.abas, padding=12)
        self.aba_vendas = ttk.Frame(self.abas, padding=12)
        self.aba_historico = ttk.Frame(self.abas, padding=12)
        self.abas.add(self.aba_produtos, text="01  Produtos e estoque")
        self.abas.add(self.aba_vendas, text="02  Nova venda")
        self.abas.add(self.aba_historico, text="03  Histórico")

        self._aba_produtos()
        self._aba_vendas()
        self._aba_historico()
        ttk.Label(self, text="Protótipo didático offline • valores e vendas de demonstração • sem emissão fiscal",
                  style="Sub.TLabel").pack(anchor="w", padx=24, pady=(0, 12))

    def _campo(self, pai: ttk.Frame, rotulo: str, variavel: tk.StringVar, linha: int) -> None:
        ttk.Label(pai, text=rotulo).grid(row=linha, column=0, sticky="w", pady=(8, 2))
        ttk.Entry(pai, textvariable=variavel).grid(row=linha + 1, column=0, sticky="ew")

    def _tabela(self, pai: ttk.Frame, colunas: list[tuple[str, str, int]]) -> ttk.Treeview:
        holder = ttk.Frame(pai)
        holder.pack(fill="both", expand=True)
        tabela = ttk.Treeview(holder, columns=[c[0] for c in colunas], show="headings", selectmode="browse", height=4)
        for chave, titulo, largura in colunas:
            tabela.heading(chave, text=titulo)
            tabela.column(chave, width=largura, minwidth=70, anchor="w" if chave in ("sku", "nome", "cliente", "data", "status") else "center")
        barra = ttk.Scrollbar(holder, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=barra.set)
        tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabela

    def _aba_produtos(self) -> None:
        conteudo = self.aba_produtos
        conteudo.columnconfigure(1, weight=1)
        conteudo.rowconfigure(0, weight=1)
        formulario = ttk.LabelFrame(conteudo, text="Cadastro / edição", padding=14)
        formulario.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        formulario.columnconfigure(0, weight=1)
        self.sku = tk.StringVar()
        self.nome = tk.StringVar()
        self.preco = tk.StringVar()
        self.estoque = tk.StringVar(value="0")
        self.minimo = tk.StringVar(value="0")
        self._campo(formulario, "SKU (código único)", self.sku, 0)
        self._campo(formulario, "Descrição do produto", self.nome, 2)
        self._campo(formulario, "Preço de venda (ex.: 89,90)", self.preco, 4)
        self._campo(formulario, "Estoque inicial (apenas novo)", self.estoque, 6)
        self._campo(formulario, "Estoque mínimo para alerta", self.minimo, 8)
        ttk.Button(formulario, text="Cadastrar produto", style="Primary.TButton",
                   command=self.cadastrar).grid(row=10, column=0, sticky="ew", pady=(18, 6))
        ttk.Button(formulario, text="Salvar edição (sem mexer no saldo)",
                   command=self.atualizar_cadastro).grid(row=11, column=0, sticky="ew", pady=4)
        ttk.Button(formulario, text="Limpar formulário", command=self.limpar_formulario).grid(
            row=12, column=0, sticky="ew", pady=4)

        direita = ttk.Frame(conteudo)
        direita.grid(row=0, column=1, sticky="nsew")
        ttk.Label(direita, text="Selecione um produto para editar ou receber estoque.",
                  style="Sub.TLabel").pack(anchor="w", pady=(0, 10))
        self.tabela_produtos = self._tabela(direita, [
            ("sku", "SKU", 110), ("nome", "Produto", 240), ("preco", "Preço", 105),
            ("saldo", "Saldo", 75), ("minimo", "Mínimo", 75), ("situacao", "Estoque", 100)])
        self.tabela_produtos.bind("<<TreeviewSelect>>", self.selecionar_produto)
        botoes = ttk.Frame(direita)
        botoes.pack(fill="x", pady=(9, 0))
        ttk.Button(botoes, text="Carregar catálogo demonstrativo", command=self.demo).pack(side="left")
        ttk.Button(botoes, text="Atualizar", command=self.atualizar_tudo).pack(side="right")
        ttk.Button(botoes, text="Receber estoque", command=self.receber).pack(side="right", padx=7)
        self.entrada_estoque = tk.StringVar(value="1")
        ttk.Entry(botoes, textvariable=self.entrada_estoque, width=7).pack(side="right")
        ttk.Label(botoes, text="Qtd. recebida:").pack(side="right", padx=7)

    def _aba_vendas(self) -> None:
        conteudo = self.aba_vendas
        topo = ttk.LabelFrame(conteudo, text="Adicionar produto ao carrinho")
        topo.pack(fill="x", pady=(0, 12))
        topo.columnconfigure(0, weight=1)
        self.combo_produto = ttk.Combobox(topo, state="readonly", width=72)
        self.combo_produto.grid(row=1, column=0, sticky="ew", padx=(0, 12), pady=(0, 8))
        ttk.Label(topo, text="Produto disponível").grid(row=0, column=0, sticky="w")
        ttk.Label(topo, text="Quantidade").grid(row=0, column=1, sticky="w")
        self.qtd_venda = tk.StringVar(value="1")
        ttk.Spinbox(topo, from_=1, to=100000, textvariable=self.qtd_venda, width=8).grid(
            row=1, column=1, padx=(0, 12), sticky="w", pady=(0, 8))
        ttk.Button(topo, text="Adicionar", style="Primary.TButton",
                   command=self.adicionar_carrinho).grid(row=1, column=2, sticky="ew", pady=(0, 8))
        meio = ttk.LabelFrame(conteudo, text="Itens desta venda")
        meio.pack(fill="both", expand=True)
        self.tabela_carrinho = self._tabela(meio, [
            ("sku", "SKU", 130), ("nome", "Produto", 320), ("qtd", "Qtd", 90),
            ("unit", "Unitário", 130), ("subtotal", "Subtotal", 145)])
        rodape = ttk.Frame(conteudo)
        rodape.pack(fill="x", pady=(15, 0))
        ttk.Button(rodape, text="Remover item selecionado", command=self.remover_carrinho).grid(
            row=0, column=0, sticky="w", pady=(0, 12))
        ttk.Label(rodape, text="Cliente (opcional)").grid(row=1, column=0, sticky="w")
        self.cliente = tk.StringVar()
        ttk.Entry(rodape, textvariable=self.cliente, width=40).grid(row=2, column=0, sticky="w")
        rodape.columnconfigure(1, weight=1)
        self.total_carrinho = ttk.Label(rodape, text="Total: R$ 0,00",
                                         font=("Segoe UI", 17, "bold"))
        self.total_carrinho.grid(row=1, column=1, rowspan=2, sticky="e", padx=15)
        ttk.Button(rodape, text="Finalizar venda", style="Primary.TButton",
                   command=self.finalizar_venda).grid(row=1, column=2, rowspan=2, sticky="e")

    def _aba_historico(self) -> None:
        conteudo = self.aba_historico
        ttk.Label(conteudo, text="Vendas concluídas ou canceladas permanecem no histórico.",
                  style="Sub.TLabel").pack(anchor="w", pady=(0, 10))
        superior = ttk.LabelFrame(conteudo, text="Vendas", padding=9)
        superior.pack(fill="both", expand=True)
        self.tabela_vendas = self._tabela(superior, [
            ("id", "Venda", 75), ("data", "Data e hora", 235),
            ("cliente", "Cliente", 240), ("total", "Total", 135),
            ("status", "Situação", 145)])
        self.tabela_vendas.bind("<<TreeviewSelect>>", self.selecionar_venda)
        inferior = ttk.LabelFrame(conteudo, text="Itens da venda selecionada", padding=9)
        inferior.pack(fill="both", expand=True, pady=(12, 0))
        self.tabela_itens = self._tabela(inferior, [
            ("sku", "SKU na venda", 130), ("nome", "Descrição na venda", 300),
            ("qtd", "Qtd", 90), ("unit", "Preço na venda", 140),
            ("total", "Subtotal", 130)])
        acoes = ttk.Frame(conteudo)
        acoes.pack(fill="x", pady=(10, 0))
        ttk.Button(acoes, text="Cancelar venda selecionada",
                   command=self.cancelar_venda).pack(side="left")
        ttk.Button(acoes, text="Exportar histórico CSV", command=self.exportar_csv).pack(side="right")

    def _executar(self, acao) -> None:
        try:
            acao()
        except (ErroNegocio, ValueError, sqlite3.Error) as erro:
            messagebox.showerror("Operação não realizada", str(erro), parent=self)

    def _campos_produto(self) -> tuple[str, str, int, int, int]:
        return (self.sku.get(), self.nome.get(), preco_em_centavos(self.preco.get()),
                int(self.estoque.get()), int(self.minimo.get()))

    def cadastrar(self) -> None:
        def acao():
            self.loja.cadastrar_produto(*self._campos_produto())
            self.limpar_formulario()
            self.atualizar_tudo()
        self._executar(acao)

    def atualizar_cadastro(self) -> None:
        def acao():
            if self.produto_selecionado is None:
                raise ErroNegocio("Selecione um produto na tabela.")
            sku, nome, preco, _, minimo = self._campos_produto()
            self.loja.atualizar_produto(self.produto_selecionado, sku, nome, preco, minimo)
            self.atualizar_tudo()
            messagebox.showinfo("Salvo", "Dados do produto atualizados.", parent=self)
        self._executar(acao)

    def receber(self) -> None:
        def acao():
            if self.produto_selecionado is None:
                raise ErroNegocio("Selecione um produto para receber mercadoria.")
            self.loja.receber_estoque(self.produto_selecionado, int(self.entrada_estoque.get()))
            self.atualizar_tudo()
        self._executar(acao)

    def demo(self) -> None:
        def acao():
            quantidade = self.loja.carregar_demonstracao()
            self.atualizar_tudo()
            messagebox.showinfo("Catálogo de exemplo", f"{quantidade} produtos fictícios adicionados.", parent=self)
        self._executar(acao)

    def limpar_formulario(self) -> None:
        self.produto_selecionado = None
        for campo in (self.sku, self.nome, self.preco):
            campo.set("")
        self.estoque.set("0")
        self.minimo.set("0")
        for iid in self.tabela_produtos.selection():
            self.tabela_produtos.selection_remove(iid)

    def selecionar_produto(self, _evento=None) -> None:
        selecionado = self.tabela_produtos.selection()
        if not selecionado:
            return
        pid = int(selecionado[0])
        produto = self.produtos_atuais.get(pid)
        if produto is None:
            return
        self.produto_selecionado = pid
        self.sku.set(produto["sku"])
        self.nome.set(produto["nome"])
        centavos = produto["preco_centavos"]
        self.preco.set(f"{centavos // 100},{centavos % 100:02d}")
        self.estoque.set("0")  # Não altera o saldo durante uma edição cadastral.
        self.minimo.set(str(produto["minimo"]))

    def atualizar_tudo(self) -> None:
        produtos = self.loja.produtos()
        self.produtos_atuais = {p["id"]: p for p in produtos}
        selecionado = self.produto_selecionado
        self.tabela_produtos.delete(*self.tabela_produtos.get_children())
        for p in produtos:
            situacao = "REPOR" if p["estoque"] <= p["minimo"] else "OK"
            self.tabela_produtos.insert("", "end", iid=str(p["id"]),
                values=(p["sku"], p["nome"], reais(p["preco_centavos"]),
                        p["estoque"], p["minimo"], situacao))
        if selecionado in self.produtos_atuais:
            self.tabela_produtos.selection_set(str(selecionado))
        self.opcoes_venda = [p["id"] for p in produtos if p["estoque"] > 0]
        self.combo_produto["values"] = [
            f"{p['sku']}  |  {p['nome']}  |  {reais(p['preco_centavos'])}  |  saldo {p['estoque']}"
            for p in produtos if p["estoque"] > 0]
        if self.opcoes_venda:
            self.combo_produto.current(0)
        else:
            self.combo_produto.set("")
        self._mostrar_carrinho()
        self._mostrar_historico()
        faturamento, qtd, alertas = self.loja.resumo()
        self.indicadores.configure(text=(
            f"Faturamento registrado: {reais(faturamento)}    •    "
            f"Vendas concluídas: {qtd}    •    Produtos para repor: {alertas}"))

    def adicionar_carrinho(self) -> None:
        def acao():
            indice = self.combo_produto.current()
            if indice < 0:
                raise ErroNegocio("Cadastre um produto com saldo disponível.")
            quantidade = int(self.qtd_venda.get())
            if quantidade <= 0:
                raise ErroNegocio("Quantidade deve ser positiva.")
            produto_id = self.opcoes_venda[indice]
            total = self.carrinho.get(produto_id, 0) + quantidade
            if total > self.produtos_atuais[produto_id]["estoque"]:
                raise ErroNegocio("Quantidade no carrinho maior que o estoque disponível.")
            self.carrinho[produto_id] = total
            self._mostrar_carrinho()
        self._executar(acao)

    def remover_carrinho(self) -> None:
        selecionado = self.tabela_carrinho.selection()
        if selecionado:
            self.carrinho.pop(int(selecionado[0]), None)
            self._mostrar_carrinho()

    def _mostrar_carrinho(self) -> None:
        self.tabela_carrinho.delete(*self.tabela_carrinho.get_children())
        total = 0
        for pid, quantidade in self.carrinho.items():
            p = self.produtos_atuais.get(pid)
            if p is None:
                continue
            subtotal = quantidade * p["preco_centavos"]
            total += subtotal
            self.tabela_carrinho.insert("", "end", iid=str(pid), values=(
                p["sku"], p["nome"], quantidade, reais(p["preco_centavos"]), reais(subtotal)))
        self.total_carrinho.configure(text=f"Total: {reais(total)}")

    def finalizar_venda(self) -> None:
        def acao():
            venda_id = self.loja.vender(self.cliente.get(), list(self.carrinho.items()))
            self.carrinho.clear()
            self.cliente.set("")
            self.atualizar_tudo()
            self.abas.select(self.aba_historico)
            self.tabela_vendas.selection_set(str(venda_id))
            self.tabela_vendas.see(str(venda_id))
            self.selecionar_venda()
            messagebox.showinfo("Venda concluída", f"Venda #{venda_id} registrada e estoque atualizado.", parent=self)
        self._executar(acao)

    def _mostrar_historico(self) -> None:
        self.tabela_vendas.delete(*self.tabela_vendas.get_children())
        self.tabela_itens.delete(*self.tabela_itens.get_children())
        for v in self.loja.vendas():
            data = v["criada_em"].replace("T", " ")[:19]
            self.tabela_vendas.insert("", "end", iid=str(v["id"]), values=(
                v["id"], data, v["cliente"], reais(v["total_centavos"]), v["status"]))

    def selecionar_venda(self, _evento=None) -> None:
        self.tabela_itens.delete(*self.tabela_itens.get_children())
        selecionado = self.tabela_vendas.selection()
        if not selecionado:
            return
        for item in self.loja.itens_da_venda(int(selecionado[0])):
            self.tabela_itens.insert("", "end", values=(
                item["sku"], item["nome"], item["quantidade"],
                reais(item["preco_centavos"]), reais(item["subtotal_centavos"])))

    def cancelar_venda(self) -> None:
        selecionado = self.tabela_vendas.selection()
        if not selecionado:
            messagebox.showwarning("Seleção necessária", "Selecione uma venda.", parent=self)
            return
        venda_id = int(selecionado[0])
        if not messagebox.askyesno("Confirme o cancelamento",
                 f"Cancelar a venda #{venda_id} e devolver os produtos ao estoque?", parent=self):
            return
        def acao():
            self.loja.cancelar_venda(venda_id)
            self.atualizar_tudo()
            messagebox.showinfo("Cancelada", f"Venda #{venda_id} cancelada. Estoque reposto.", parent=self)
        self._executar(acao)

    @staticmethod
    def _celula_csv(texto: str) -> str:
        """Evita que campos informados pelo usuário sejam fórmulas na planilha."""
        if texto.lstrip().startswith(("=", "+", "-", "@")):
            return "'" + texto
        return texto

    def exportar_csv(self) -> None:
        caminho = filedialog.asksaveasfilename(
            parent=self, title="Exportar histórico de vendas",
            defaultextension=".csv", filetypes=[("CSV", "*.csv")],
            initialfile="historico_vendas.csv")
        if not caminho:
            return
        try:
            with Path(caminho).open("w", encoding="utf-8-sig", newline="") as arquivo:
                gravador = csv.writer(arquivo, delimiter=";")
                gravador.writerow(["Venda", "Data/hora", "Cliente", "Status", "Total (R$)"])
                for venda in self.loja.vendas():
                    gravador.writerow([venda["id"], venda["criada_em"], self._celula_csv(venda["cliente"]),
                                      venda["status"],
                                      f"{venda['total_centavos'] // 100},{venda['total_centavos'] % 100:02d}"])
            messagebox.showinfo("Exportado", "Histórico CSV salvo com sucesso.", parent=self)
        except OSError as erro:
            messagebox.showerror("Não foi possível exportar", str(erro), parent=self)
