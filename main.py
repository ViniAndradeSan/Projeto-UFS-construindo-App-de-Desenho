from tkinter import *
from tkinter import ttk

#__MAIN__

root = Tk()
root.title('Exemplo de aplicação')
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
label = ttk.Label(frame,  text='Escolha sua ferramenta de desenho: ')
label.grid(column=0, row=0, sticky=E, **paddings)

# option menu
tipo_figura_var = StringVar(root)
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Retangulo', 'Retangulo', 'Circulo', 'Oval')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=2, sticky=W, **paddings)

frame.pack()

root.mainloop()
