from tkinter import *

class AreaDesenho:
    """Área de desenho responsável por exibir as figuras no canvas.

    Finalidade:
        Renderizar figuras existentes e a figura em construção dentro da área do
        aplicativo.

    Responsabilidade:
        Criar o canvas, atualizar sua exibição e redesenhar todas as figuras
        conforme o estado atual do desenho.

    Uso:
        Instanciar com `AreaDesenho(frame)` e chamar `atualizar(figuras,
        figura_em_processo)` quando o estado do desenho mudar.

    Autor: Danillo
    Versão: 1.0
    """

    def __init__(self, frame):
        self.frame = frame
        self.canvas = Canvas(frame, bg='white', width=800, height=600)

        self.canvas.grid(column=0, row=3, columnspan=5, sticky=N, padx=5, pady=5)

    def atualizar(self, figuras, figura_em_processo=None):
        self.canvas.delete("all")
        for fig in figuras:
            fig.desenhar(self.canvas)

        if not figura_em_processo:
            return 
        figura_em_processo.desenhar(self.canvas, tracejado=True )
