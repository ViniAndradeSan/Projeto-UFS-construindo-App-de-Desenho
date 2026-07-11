from modelo.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono
from modelo.modelo_desenho import Desenho
from tkinter import  colorchooser, filedialog


class Controlador:
    """Controlador da aplicação de desenho que liga modelo e visão.

    Finalidade:
        Gerenciar a criação, atualização e inclusão de figuras no desenho.

    Responsabilidade:
        Receber eventos de mouse e teclado, controlar a figura em construção,
        executar desfazer/limpar e tratar operações de abrir/salvar.

    Uso:
        Instanciar com `Controlador(desenho, area_desenho)` e conectar eventos do
        canvas e da interface gráfica.

    Autor: Constrole Vinicius
    Versão: 1.0
    """

    CLASSES_FIGURA = {
        'Linha': Linha,
        'Retangulo': Retangulo,
        'Oval': Oval,
        'Circulo': Circulo,
    }

    def __init__(self, desenho, area_desenho):
        """Inicializa o controlador da aplicação.

        Objetivo:
            Conectar o modelo de desenho e a área de visualização para utilizar o
            modo de criação de figuras.

        Args:
            desenho (Desenho): Instância do modelo de desenho.
            area_desenho (AreaDesenho): Área gráfica onde as figuras são mostradas.
        """
        self.desenho = desenho
        self.area_desenho = area_desenho
        self.figura_nova = None

    def iniciar_figura_nova(self, event):

        tipo = self.tipo_figura_var.get()

        if tipo == 'Poligono':
            if self.figura_nova is not None and isinstance(self.figura_nova, Poligono):
                self.figura_nova.adicionar_vertice(event.x, event.y)
            else:
                self.figura_nova = Poligono(
                    event.x, event.y,
                    self.cor_borda.get(), self.cor_preenchimento.get()
                )
            self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)
            return

        if tipo == 'Rabisco':
            self.figura_nova = Rabisco(event.x, event.y, self.cor_borda.get())
        else:
            classe = self.CLASSES_FIGURA[tipo]
            if classe is Linha:
                self.figura_nova = classe(event.x, event.y, event.x, event.y, self.cor_borda.get())
            else:
                self.figura_nova = classe(
                    event.x, event.y, event.x, event.y,
                    self.cor_borda.get(), self.cor_preenchimento.get()
                )


    def atualizar_figura_nova(self, event):
        if not self.figura_nova: 
            return
        self.figura_nova.atualizar(event.x, event.y)

        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def mover_mouse(self, event):
        if self.figura_nova is not None and isinstance(self.figura_nova, Poligono):
            self.atualizar_figura_nova(event)


    def incluir_figura_nova(self, event):
        if self.figura_nova is None or isinstance(self.figura_nova, Poligono):
            return

        if not self.figura_nova.esta_incompleta():
            self.desenho.adicionar(self.figura_nova)

        self.figura_nova = None
        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)


    # Duplo clique ou Enter: finaliza o Poligono em construção
    def finalizar_poligono(self, event):
        if self.figura_nova is not None and isinstance(self.figura_nova, Poligono):
            self.figura_nova.finalizar()
            if not self.figura_nova.esta_incompleta():
                self.desenho.adicionar(self.figura_nova)
            self.figura_nova = None
            self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)


    # Esc: cancela o Poligono em construção
    def cancelar_figura_nova(self, event):
        if self.figura_nova is not None:
            self.figura_nova = None
            self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def escolher_cor(self, tipo):
        cor = colorchooser.askcolor()
        if not cor[1]:
            return

        if tipo == 'b':
            self.cor_borda.set(cor[1])
        elif tipo == 'p':
            self.cor_preenchimento.set(cor[1])


    def desfazer_ultimo(self, event=None):
        self.desenho.desfazer()
        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)


    def limpar_tudo(self):
        self.desenho.limpar()
        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def definir_variaveis(self, tipo_figura_var, cor_borda, cor_preenchimento):
        self.tipo_figura_var = tipo_figura_var
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def abrir_para_edicao(self, event=None):
        self.arquivo_dir = filedialog.askopenfilename(
            defaultextension='.json'
        )

        if self.arquivo_dir:
            self.desenho.abrir(diretorio=self.arquivo_dir)
            self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def salvar_para_edicao(self, event=None):
        self.save_dir = filedialog.asksaveasfilename(
            defaultextension='.json'
        )
        
        if self.save_dir:
            self.desenho.salvar(diretorio=self.save_dir)