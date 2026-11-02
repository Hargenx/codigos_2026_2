"""Primeiro exemplo: Treeview sem banco de dados."""

import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
janela.title("Primeiro Treeview")
janela.geometry("520x300")

tabela = ttk.Treeview(janela, columns=("nome", "idade"), show="headings")
tabela.heading("nome", text="Nome")
tabela.heading("idade", text="Idade")
tabela.column("nome", width=330)
tabela.column("idade", width=100, anchor="center")
tabela.pack(fill="both", expand=True, padx=20, pady=20)

tabela.insert("", "end", values=("Ana", 23))
tabela.insert("", "end", values=("Bruno", 29))

janela.mainloop()
