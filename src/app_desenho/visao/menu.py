import tkinter as tk


class BarraMenu:
    """Barra de menu para operações de arquivo no aplicativo de desenho.

    Finalidade:
        Expor ações de abrir e salvar desenho por meio de um menu padrão.

    Responsabilidade:
        Criar o menu principal e associar atalhos de teclado às funções do
        controlador.

    Uso:
        Instanciar com `BarraMenu(root, controlador)` depois de criar a janela
        principal (`root`) e o controlador.

    @author Danillo
    @version 1.0
    """

    def __init__(self, root, controlador):
        """Inicializa a barra de menu da aplicação.

        Objetivo:
            Criar o menu de arquivo e vincular atalhos de teclado.

        @param root (tk.Tk): Janela principal da aplicação.
        @param controlador (Controlador): Controlador que trata abrir e salvar.
        """
        
        self.menu = tk.Menu(root)
        
        self.arquivo = tk.Menu(self.menu, tearoff=0)
        self.arquivo.add_command(label="Abrir", command=controlador.abrir_para_edicao, accelerator="Ctrl + O")
        self.arquivo.add_separator()
        self.arquivo.add_command(label="Salvar para edição", command=controlador.salvar_para_edicao, accelerator="Ctrl + S")

        self.menu.add_cascade(label="Arquivo", menu=self.arquivo)

        root.bind_all("<Control-o>", controlador.abrir_para_edicao)
        root.bind_all("<Control-s>", controlador.salvar_para_edicao)
        root.config(menu=self.menu)