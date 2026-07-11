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

    @author Vinicius
    @version 1.0
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

        @param desenho (Desenho): Instância do modelo de desenho.
        @param area_desenho (AreaDesenho): Área gráfica onde as figuras são mostradas.
        """
        self.desenho = desenho
        self.area_desenho = area_desenho
        self.figura_nova = None

    def iniciar_figura_nova(self, event):
        """Inicia a criação de uma nova figura baseada na seleção.

        Descrição:
            Cria uma instância da figura selecionada com o ponto inicial do evento.
            Para polígonos, adiciona novos vértices; para outras formas, inicia.

        @param event (tk.Event): Evento do mouse contendo as coordenadas x e y.
        """

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
        """Atualiza a posição final da figura em construção.

        Descrição:
            Modifica o ponto final da figura corrente durante o arrasto do mouse.

        @param event (tk.Event): Evento do mouse com coordenadas x e y.
        """
        if not self.figura_nova: 
            return
        self.figura_nova.atualizar(event.x, event.y)

        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def mover_mouse(self, event):
        """Evento de movimento do mouse para atualização de polígonos.

        Descrição:
            Atualiza a visão de pré-visualização para polígonos enquanto o mouse se move.

        @param event (tk.Event): Evento de movimento do mouse.
        """
        if self.figura_nova is not None and isinstance(self.figura_nova, Poligono):
            self.atualizar_figura_nova(event)


    def incluir_figura_nova(self, event):
        """Finaliza a criação e adiciona a figura ao desenho.

        Descrição:
            Se a figura não está incompleta, adiciona-a ao desenho completado.
            Ignora polígonos que precisam de finalização explícita.

        @param event (tk.Event): Evento de liberação do botão do mouse.
        """
        if self.figura_nova is None or isinstance(self.figura_nova, Poligono):
            return

        if not self.figura_nova.esta_incompleta():
            self.desenho.adicionar(self.figura_nova)

        self.figura_nova = None
        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)


    # Duplo clique ou Enter: finaliza o Poligono em construção
    def finalizar_poligono(self, event):
        """Finaliza a construção de um polígono e o adiciona ao desenho.

        Descrição:
            Marca o polígono como finalizado e adiciona-o ao desenho. Acionado
            por duplo clique ou Press Enter.

        @param event (tk.Event): Evento de duplo clique ou tecla de enter.
        """
        if self.figura_nova is not None and isinstance(self.figura_nova, Poligono):
            self.figura_nova.finalizar()
            if not self.figura_nova.esta_incompleta():
                self.desenho.adicionar(self.figura_nova)
            self.figura_nova = None
            self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)


    # Esc: cancela o Poligono em construção
    def cancelar_figura_nova(self, event):
        """Cancela a criação da figura atual.

        Descrição:
            Descarta a figura em construção sem adicioná-la ao desenho.
            Acionado pela tecla Escape.

        @param event (tk.Event): Evento de pressa da tecla Escape.
        """
        if self.figura_nova is not None:
            self.figura_nova = None
            self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def escolher_cor(self, tipo):
        """Abre o diálogo de seleção de cor.

        Descrição:
            Exibe um diálogo do sistema para escolher cor de borda ou preenchimento.

        @param tipo (str): 'b' para cor de borda ou 'p' para cor de preenchimento.
        """
        cor = colorchooser.askcolor()
        if not cor[1]:
            return

        if tipo == 'b':
            self.cor_borda.set(cor[1])
        elif tipo == 'p':
            self.cor_preenchimento.set(cor[1])


    def desfazer_ultimo(self, event=None):
        """Desfaz a última figura adicionada ao desenho.

        Descrição:
            Remove e descarta a figura mais recente do desenho.

        @param event (tk.Event, optional): Evento de teclado (Ctrl+Z). Default: None.
        """
        self.desenho.desfazer()
        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)


    def limpar_tudo(self):
        """Remove todas as figuras do desenho.

        Descrição:
            Limpa completamente a área de desenho removendo todas as figuras.
        """
        self.desenho.limpar()
        self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def definir_variaveis(self, tipo_figura_var, cor_borda, cor_preenchimento):
        """Define as variáveis de controle da barra de ferramentas.

        Descrição:
            Armazena referências às variáveis Tkinter de seleção de figura e cores.

        @param tipo_figura_var (tk.StringVar): Variável de tipo de figura selecionado.
        @param cor_borda (tk.StringVar): Variável de cor da borda.
        @param cor_preenchimento (tk.StringVar): Variável de cor de preenchimento.
        """
        self.tipo_figura_var = tipo_figura_var
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def abrir_para_edicao(self, event=None):
        """Abre um diálogo para carregar um desenho de um arquivo.

        Descrição:
            Exibe o diálogo de arquivo do sistema para seleção de um JSON a carregar.

        @param event (tk.Event, optional): Evento de teclado (Ctrl+O). Default(event): None.
        """
        self.arquivo_dir = filedialog.askopenfilename(
            defaultextension='.json'
        )

        if self.arquivo_dir:
            self.desenho.abrir(diretorio=self.arquivo_dir)
            self.area_desenho.atualizar(self.desenho.figuras, self.figura_nova)

    def salvar_para_edicao(self, event=None):
        """Abre um diálogo para salvar o desenho em um arquivo.

        Descrição:
            Exibe o diálogo de arquivo do sistema para seleção do local de salvamento.

        @param event (tk.Event, optional): Evento de teclado (Ctrl+S). Default(event): None.
        """
        self.save_dir = filedialog.asksaveasfilename(
            defaultextension='.json'
        )
        
        if self.save_dir:
            self.desenho.salvar(diretorio=self.save_dir)