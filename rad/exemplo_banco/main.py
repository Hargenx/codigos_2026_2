import tkinter as tk

from exemplo_treeview import Aplicativo

root = tk.Tk()
app = Aplicativo(root)

app.tabela.insert("", "end", iid="42", values=(42, "Ana", "ana@example.com"))

itens = app.tabela.selection()
if itens:
    usuario_id = int(itens[0])
    print("Registro selecionado:", usuario_id)

root.mainloop()