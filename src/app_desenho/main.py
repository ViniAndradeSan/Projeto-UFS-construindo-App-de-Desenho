from tkinter import *
import tkinter as ttk
from src.app_desenho.modelo.figuras import *
from src.app_desenho.controlador.controlador import *


#******* MAIN *******#

root = Tk()
root.title('Exemplo de aplicação')
frame = Frame(root)

# menu de cores
cor_borda = StringVar(root, value='#000000')
cor_preenchimento = StringVar(root)

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