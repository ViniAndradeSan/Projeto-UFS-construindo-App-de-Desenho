from tkinter import *
<<<<<<< HEAD
from controlador import *
from modelo import *
from visao import *
=======
from tkinter import ttk
from tkinter import colorchooser

from src.app_desenho.modelo.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono

CLASSES_FIGURA = {
    'Linha': Linha,
    'Retangulo': Retangulo,
    'Oval': Oval,
    'Circulo': Circulo,
}

print("")

def iniciar_figura_nova(event):
    global figura_nova

    tipo = tipo_figura_var.get()

    if tipo == 'Poligono':
        if figura_nova is not None and isinstance(figura_nova, Poligono):
            figura_nova.adicionar_vertice(event.x, event.y)
        else:
            figura_nova = Poligono(
                event.x, event.y,
                cor_borda.get(), cor_preenchimento.get()
            )
        desenhar_figuras()
        desenhar_figura_nova()
        return

    if tipo == 'Rabisco':
        figura_nova = Rabisco(event.x, event.y, cor_borda.get())
    else:
        classe = CLASSES_FIGURA[tipo]
        if classe is Linha:
            figura_nova = classe(event.x, event.y, event.x, event.y, cor_borda.get())
        else:
            figura_nova = classe(
                event.x, event.y, event.x, event.y,
                cor_borda.get(), cor_preenchimento.get()
            )


def atualizar_figura_nova(event):
    global figura_nova
    if not figura_nova: 
        return

    if isinstance(figura_nova, Rabisco):
        figura_nova.atualizar(event.x, event.y)
    else:
        figura_nova.atualizar(event.x, event.y)

    desenhar_figuras()
    desenhar_figura_nova()

def mover_mouse(event):
    if figura_nova is not None and isinstance(figura_nova, Poligono):
        atualizar_figura_nova(event)


def incluir_figura_nova(event):
    global figura_nova
    if figura_nova is None:
        return

    if isinstance(figura_nova, Poligono):
        return

    if not figura_nova.esta_incompleta():
        figuras.append(figura_nova)

    figura_nova = None
    desenhar_figuras()


# Duplo clique ou Enter: finaliza o Poligono em construção
def finalizar_poligono(event=None):
    global figura_nova
    if figura_nova is not None and isinstance(figura_nova, Poligono):
        figura_nova.finalizar()
        if not figura_nova.esta_incompleta():
            figuras.append(figura_nova)
        figura_nova = None
        desenhar_figuras()


# Esc: cancela o Poligono em construção
def cancelar_figura_nova(event=None):
    global figura_nova
    if figura_nova is not None:
        figura_nova = None
        desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")
    for fig in figuras:
        fig.desenhar(canvas)


def desenhar_figura_nova():
    if not figura_nova:
        return
    figura_nova.desenhar(canvas, tracejado=True)


def escolher_cor(tipo):
    cor = colorchooser.askcolor()
    if not cor[1]:
        return

    if tipo == 'b':
        cor_borda.set(cor[1])
    elif tipo == 'p':
        cor_preenchimento.set(cor[1])


def desfazer_ultimo():
    if figuras:
        figuras.pop()
        desenhar_figuras()


def limpar_tudo():
    global figuras
    figuras = []
    canvas.delete("all")
>>>>>>> b0b575f (feat(model): adicionando serialização das figura)


#******* MAIN *******#

root = Tk()
root.title('Exemplo de aplicação')
frame = Frame(root)
desenho = Desenho()
area = AreaDesenho(frame)
controlador = Controlador(desenho, area)
barra = BarraFerramentas(frame, controlador)

# Eventos de mouse associados ao canvas
area.canvas.bind('<ButtonPress-1>', controlador.iniciar_figura_nova)
area.canvas.bind('<B1-Motion>', controlador.atualizar_figura_nova)
area.canvas.bind('<ButtonRelease-1>', controlador.incluir_figura_nova)
area.canvas.bind('<Motion>', controlador.mover_mouse)
area.canvas.bind('<Double-Button-1>', controlador.finalizar_poligono)

# Eventos de teclado para finalizar/cancelar o Poligono
root.bind('<Return>', controlador.finalizar_poligono)
root.bind('<Escape>', controlador.cancelar_figura_nova)

frame.pack()
root.mainloop()