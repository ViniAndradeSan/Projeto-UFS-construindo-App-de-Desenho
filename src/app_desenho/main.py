from tkinter import *
from src.app_desenho.modelo.figuras import *
from src.app_desenho.controlador.controlador import *


#******* MAIN *******#

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

# Área de desenho
canvas = Canvas(frame, bg='white', width=800, height=600)
canvas.grid(column=0, row=3, columnspan=5, sticky=N, **paddings)

frame.pack()

root.mainloop()