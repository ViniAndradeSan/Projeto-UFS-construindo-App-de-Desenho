from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

from figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono

CLASSES_FIGURA = {
    'Linha': Linha,
    'Retangulo': Retangulo,
    'Oval': Oval,
    'Circulo': Circulo,
}


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


#******* MAIN *******#

figuras = []   
figura_nova = None 

root = Tk()
root.title('Exemplo de aplicação')
frame = Frame(root)

paddings = {'padx': 5, 'pady': 5}

# label
label = Label(frame, text='Selecione sua ferramenta de desenho: ')
label.grid(column=0, row=0, sticky=E, **paddings, rowspan=2)

tipo_figura_var = StringVar(root)
option_menu = ttk.OptionMenu(
    frame, tipo_figura_var, 'Linha',
    'Linha', 'Rabisco', 'Retangulo', 'Circulo', 'Oval', 'Poligono'
)
option_menu.grid(column=1, row=0, sticky=W, **paddings, rowspan=2)

# menu de cores
cor_borda = StringVar(root, value='#000000')
cor_preenchimento = StringVar(root)

label_cor_borda = Label(frame, text='Cor da borda: ')
label_cor_borda.grid(column=2, row=0, sticky=E, **paddings)
caixa_cor_borda = Button(frame, text='Selecionar cor', command=lambda: escolher_cor('b'))
caixa_cor_borda.grid(column=3, row=0, sticky=E, **paddings)

caixa_resetar_borda = Button(frame, text='Resetar borda', command=lambda: cor_borda.set('#000000'))
caixa_resetar_borda.grid(column=4, row=0, sticky=W, **paddings)

label_cor_preenchimento = Label(frame, text='Cor do preenchimento: ')
label_cor_preenchimento.grid(column=2, row=1, sticky=E, **paddings)
caixa_cor_preenchimento = Button(frame, text='Selecionar cor', command=lambda: escolher_cor('p'))
caixa_cor_preenchimento.grid(column=3, row=1, sticky=E, **paddings)

caixa_resetar_preenchimento = Button(frame, text='Resetar preenchimento', command=lambda: cor_preenchimento.set(''))
caixa_resetar_preenchimento.grid(column=4, row=1, sticky=E, **paddings)

# controle global
frame_apagar = Frame(frame)
frame_apagar.grid(column=0, row=2, columnspan=5, sticky=W, **paddings)

label_apagar = Label(frame_apagar, text='Opção de apagar: ')
label_apagar.pack(side=LEFT, padx=2)

caixa_desfazer = Button(frame_apagar, text='Desfazer', command=desfazer_ultimo)
caixa_desfazer.pack(side=LEFT, padx=5)

caixa_limpar = Button(frame_apagar, text='Limpar Tela', command=limpar_tudo)
caixa_limpar.pack(side=LEFT, padx=5)

# dica de uso do Poligono
label_dica = Label(
    frame_apagar,
    text='(Poligono: clique para cada vértice, duplo clique/Enter finaliza, Esc cancela)'
)
label_dica.pack(side=LEFT, padx=10)

# Área de desenho
canvas = Canvas(frame, bg='white', width=800, height=600)
canvas.grid(column=0, row=3, columnspan=5, sticky=N, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)
canvas.bind('<Motion>', mover_mouse)          # prévia do Poligono
canvas.bind('<Double-Button-1>', finalizar_poligono)

# Eventos de teclado para finalizar/cancelar o Poligono
root.bind('<Return>', finalizar_poligono)
root.bind('<Escape>', cancelar_figura_nova)

root.mainloop()