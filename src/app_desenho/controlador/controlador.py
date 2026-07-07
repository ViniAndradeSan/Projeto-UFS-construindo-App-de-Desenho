from modelo.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono
from tkinter import  colorchooser


class Controlador:
    CLASSES_FIGURA = {
        'Linha': Linha,
        'Retangulo': Retangulo,
        'Oval': Oval,
        'Circulo': Circulo,
    }

    def __init__(self, desenho, area_desenho):
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


    def desfazer_ultimo(self):
        self.desenho.desfazer()
        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)


    def limpar_tudo(self):
        self.desenho.limpar()
        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def definir_variaveis(self, tipo_figura_var, cor_borda, cor_preenchimento):
        self.tipo_figura_var = tipo_figura_var
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        
'''''

# Eventos de mouse associados ao canvas
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)
canvas.bind('<Motion>', mover_mouse)          # prévia do Poligono
canvas.bind('<Double-Button-1>', finalizar_poligono)

# Eventos de teclado para finalizar/cancelar o Poligono
root.bind('<Return>', finalizar_poligono)
root.bind('<Escape>', cancelar_figura_nova)
'''''