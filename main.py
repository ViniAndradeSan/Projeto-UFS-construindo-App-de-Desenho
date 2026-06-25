from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
import tkinter as tk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("Linha", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Oval':
        figura_nova = ("Oval", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Retangulo':
         figura_nova = ("Retangulo", (event.x, event.y, event.x, event.y))
    else:
        figura_nova = ("Rabisco", [(event.x, event.y)])

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if not figura_nova:  # Proteção caso o evento de movimento dispare sem o clique inicial
        return
        
    if figura_nova[0] == "Rabisco":
        figura_nova[1].append((event.x, event.y))
    elif figura_nova[0] == "Linha": 
        figura_nova = ("Linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "Retangulo":
        figura_nova = ('Retangulo', (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "Oval":
        figura_nova = ("Oval", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    global figura_nova
    if figura_nova and not incompleta(figura_nova): 
        figuras.append(figura_nova) 
    
    figura_nova = None  # Reseta a figura nova após soltar o mouse
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values in figuras:
        if fig == "Linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor_preenchimento.get())
        elif fig == "Oval":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor_borda.get(), fill=cor_preenchimento.get())
        elif fig == "Retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor_borda.get(), fill=cor_preenchimento.get())
        else: # fig == "rabisco"
            canvas.create_line(values, fill=cor_preenchimento.get())

def desenhar_figura_nova():
    if not figura_nova:
        return
    fig, values = figura_nova
    if fig == "Linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill=cor_preenchimento.get())
    elif fig == "Oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline=cor_borda.get(), fill=cor_preenchimento.get())
    elif fig == "Retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline=cor_borda.get(), fill=cor_preenchimento.get())
    else: # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2), fill=cor_preenchimento.get())

def incompleta(figura):
    fig, values = figura
    if fig in ["Linha", "Oval"]:
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "Rabisco":
        return len(values) <= 1
    elif fig == "Retangulo":
        return (values[0], values[1]) == (values[2], values[3])

def escolher_cor(tipo):
    cor = colorchooser.askcolor()
    # Só continua a função se o usuário escolher uma cor.
    if not cor[1]:
        return
    
    if tipo == 'b':
        cor_borda.set(cor[1])
    elif tipo == 'p':
        cor_preenchimento.set(cor[1])

#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada

root = Tk()
root.title('Exemplo de aplicação')
frame = Frame(root)

paddings = {'padx': 5, 'pady': 5} 

# label
label = tk.Label(frame, text='Selecione sua ferramenta de desenho: ')
label.grid(column=0, row=0, sticky=E, **paddings, rowspan=2)

# option menu
tipo_figura_var = StringVar(root)
option_menu = ttk.OptionMenu(frame, tipo_figura_var, 'Linha', 'Rabisco', 'Retangulo', 'Circulo', 'Oval')
option_menu.grid(column=1, row=0, sticky=W, **paddings, rowspan=2)

# menu de cores
cor_borda = StringVar(root, value='#000000')
cor_preenchimento = StringVar(root, value='#000000')


label_cor_borda = tk.Label(frame, text='Cor da borda: ')
label_cor_borda.grid(column=2, row=0, sticky=E, **paddings)
caixa_cor_borda = tk.Button(frame, text='Selecionar cor', command=lambda: escolher_cor('b'))
caixa_cor_borda.grid(column=3, row=0, sticky=E, **paddings)

label_cor_preenchimento = tk.Label(frame, text='Cor do preenchimento: ')
label_cor_preenchimento.grid(column=2, row=1, sticky=E, **paddings)
caixa_cor_preenchimento = tk.Button(frame, text='Selecionar cor', command=lambda: escolher_cor('p'))
caixa_cor_preenchimento.grid(column=3, row=1, sticky=E, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=2, columnspan=4, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()
