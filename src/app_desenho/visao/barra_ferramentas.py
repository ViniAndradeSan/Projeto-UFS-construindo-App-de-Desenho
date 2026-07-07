from tkinter import StringVar, Label, E, W, ttk, Button, Frame, LEFT

class BarraFerramentas:
    paddings = {'padx': 5, 'pady': 5}

    def __init__(self, frame, controlador):
        self.frame = frame
        self.controlador = controlador       

        # Ferramentas
        tipo_figura_var = StringVar(frame, 'Linha')
        cor_borda = StringVar(frame, value='#000000')
        cor_preenchimento = StringVar(frame)

        controlador.definir_variaveis(tipo_figura_var, cor_borda, cor_preenchimento)

        self.label = Label(frame, text='Selecione sua ferramenta de desenho: ')
        self.label.grid(column=0, row=0, sticky=E, **self.paddings, rowspan=2)

        option_menu = ttk.OptionMenu(
            frame, tipo_figura_var, 'Linha',
            'Linha', 'Rabisco', 'Retangulo', 'Circulo', 'Oval', 'Poligono'
        )
        option_menu.grid(column=1, row=0, sticky=W, **self.paddings, rowspan=2)

        # Menu de cores
        self.label_cor_borda = Label(frame, text='Cor da borda: ')
        self.label_cor_borda.grid(column=2, row=0, sticky=E, **self.paddings)
        self.caixa_cor_borda = Button(frame, text='Selecionar cor', command=lambda: controlador.escolher_cor('b'))
        self.caixa_cor_borda.grid(column=3, row=0, sticky=E, **self.paddings)

        self.caixa_resetar_borda = Button(frame, text='Resetar borda', command=lambda: cor_borda.set('#000000'))
        self.caixa_resetar_borda.grid(column=4, row=0, sticky=W, **self.paddings)

        self.label_cor_preenchimento = Label(frame, text='Cor do preenchimento: ')
        self.label_cor_preenchimento.grid(column=2, row=1, sticky=E, **self.paddings)
        self.caixa_cor_preenchimento = Button(frame, text='Selecionar cor', command=lambda: controlador.escolher_cor('p'))
        self.caixa_cor_preenchimento.grid(column=3, row=1, sticky=E, **self.paddings)

        self.caixa_resetar_preenchimento = Button(frame, text='Resetar preenchimento', command=lambda: cor_preenchimento.set(''))
        self.caixa_resetar_preenchimento.grid(column=4, row=1, sticky=E, **self.paddings)

        # Controle Global
        self.frame_apagar = Frame(frame)
        self.frame_apagar.grid(column=0, row=2, columnspan=5, sticky=W, **self.paddings)

        self.label_apagar = Label(self.frame_apagar, text='Opção de apagar: ')
        self.label_apagar.pack(side=LEFT, padx=2)

        self.caixa_desfazer = Button(self.frame_apagar, text='Desfazer', command=controlador.desfazer_ultimo)
        self.caixa_desfazer.pack(side=LEFT, padx=5)

        self.caixa_limpar = Button(self.frame_apagar, text='Limpar Tela', command=controlador.limpar_tudo)
        self.caixa_limpar.pack(side=LEFT, padx=5)