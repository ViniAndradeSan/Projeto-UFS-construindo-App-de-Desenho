from tkinter import *
from controlador import *
from modelo import *
from visao import *

#******* MAIN *******#

root = Tk()
root.title('Exemplo de aplicação')
frame = Frame(root)
desenho = Desenho()
area = AreaDesenho(frame)
controlador = Controlador(desenho, area)
barra = BarraFerramentas(frame, controlador)
menu = BarraMenu(root, controlador)

# Eventos de mouse associados ao canvas
area.canvas.bind('<ButtonPress-1>', controlador.iniciar_figura_nova)
area.canvas.bind('<B1-Motion>', controlador.atualizar_figura_nova)
area.canvas.bind('<ButtonRelease-1>', controlador.incluir_figura_nova)
area.canvas.bind('<Motion>', controlador.mover_mouse)
area.canvas.bind('<Double-Button-1>', controlador.finalizar_poligono)

# Eventos de teclado para finalizar/cancelar o Poligono
root.bind('<Return>', controlador.finalizar_poligono)
root.bind('<Escape>', controlador.cancelar_figura_nova)
root.bind('<Control-z>', controlador.desfazer_ultimo)

frame.pack()
root.mainloop()