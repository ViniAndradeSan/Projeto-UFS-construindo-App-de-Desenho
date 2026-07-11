import tkinter as tk


class BarraMenu:
    def __init__(self, root, controlador):
        
        self.menu = tk.Menu(root)
        
        self.arquivo = tk.Menu(self.menu, tearoff=0)
        self.arquivo.add_command(label="Abrir", command=controlador.abrir_para_edicao, accelerator="Ctrl + O")
        self.arquivo.add_separator()
        self.arquivo.add_command(label="Salvar para edição", command=controlador.salvar_para_edicao, accelerator="Ctrl + S")

        self.menu.add_cascade(label="Arquivo", menu=self.arquivo)

        root.bind_all("<Control-o>", controlador.abrir_para_edicao)
        root.bind_all("<Control-s>", controlador.salvar_para_edicao)
        root.config(menu=self.menu)