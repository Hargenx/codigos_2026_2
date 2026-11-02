import tkinter as tk
from tkinter import ttk


class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

class ArvorePessoas:
    def __init__(self):
        self.pessoas = []

    def adicionar_pessoa(self, pessoa):
        self.pessoas.append(pessoa)

    def listar_pessoas(self):
        return self.pessoas

class Aplicativo:
    def __init__(self, master):
        self.master = master
        self.master.title("Primeiro Treeview")
        self.master.geometry("520x300")

        self.tabela = ttk.Treeview(master, columns=("nome", "idade"), show="headings")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("idade", text="Idade")
        self.tabela.column("nome", width=330)
        self.tabela.column("idade", width=100, anchor="center")
        self.tabela.pack(fill="both", expand=True, padx=20, pady=20)

        self.arvore = ArvorePessoas()
        self.arvore.adicionar_pessoa(Pessoa("Ana", 23))
        self.arvore.adicionar_pessoa(Pessoa("Bruno", 29))

        for pessoa in self.arvore.listar_pessoas():
            self.tabela.insert("", "end", values=(pessoa.nome, pessoa.idade))

if __name__ == "__main__":
    janela = tk.Tk()
    janela.title("Primeiro Treeview")
    janela.geometry("520x300")

    aplicativo = Aplicativo(janela)
    janela.mainloop()
