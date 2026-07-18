from modelo.figuras import Linha, Retangulo, Oval, Circulo
from controlador.estados import EstadoArrastoSimples, EstadoRabisco, EstadoPoligono
from tkinter import colorchooser, filedialog


ESTADOS_FERRAMENTA = {
    'Linha': EstadoArrastoSimples(Linha, False),
    'Retangulo': EstadoArrastoSimples(Retangulo),
    'Oval': EstadoArrastoSimples(Oval),
    'Circulo': EstadoArrastoSimples(Circulo),
    'Rabisco': EstadoRabisco(),
    'Poligono': EstadoPoligono(),
}


class Controlador:
    """Controlador da aplicação de desenho que liga modelo e visão.

    Finalidade:
        Gerenciar a criação, atualização e inclusão de figuras no desenho.

    Responsabilidade:
        Receber eventos de mouse e teclado, controlar a figura em construção,
        executar desfazer/limpar e tratar operações de abrir/salvar.
        Delega toda lógica de criação de figuras ao estado de ferramenta atual.

    Uso:
        Instanciar com `Controlador(desenho, area_desenho)` e conectar eventos do
        canvas e da interface gráfica.

    @author Vinicius
    @version 2.0
    """

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
        self.estado = None

    def selecionar_ferramenta(self, tipo):
        """Troca o estado de ferramenta atual.

        Descrição:
            Busca o estado correspondente ao tipo no dicionário
            ESTADOS_FERRAMENTA e o define como estado ativo.

        @param tipo (str): Nome da ferramenta (ex: 'Linha', 'Poligono').
        """
        if tipo in ESTADOS_FERRAMENTA:
            self.estado = ESTADOS_FERRAMENTA[tipo]

    def iniciar_figura_nova(self, event):
        """Delega o clique inicial ao estado de ferramenta atual.

        @param event (tk.Event): Evento do mouse contendo as coordenadas x e y.
        """
        if self.estado:
            self.estado.mouse_pressionado(self, event)

    def atualizar_figura_nova(self, event):
        """Delega o arrasto do mouse ao estado de ferramenta atual.

        @param event (tk.Event): Evento do mouse com coordenadas x e y.
        """
        if self.estado:
            self.estado.mouse_arrastado(self, event)

    def mover_mouse(self, event):
        """Delega o movimento do mouse ao estado de ferramenta atual.

        @param event (tk.Event): Evento de movimento do mouse.
        """
        if self.estado:
            self.estado.mouse_movido(self, event)

    def incluir_figura_nova(self, event):
        """Delega a soltura do botão ao estado de ferramenta atual.

        @param event (tk.Event): Evento de liberação do botão do mouse.
        """
        if self.estado:
            self.estado.mouse_solto(self, event)

    def finalizar_poligono(self, event):
        """Delega o duplo clique ao estado de ferramenta atual.

        @param event (tk.Event): Evento de duplo clique ou tecla de enter.
        """
        if self.estado:
            self.estado.duplo_clique(self, event)

    def cancelar_figura_nova(self, event):
        """Delega a tecla Esc ao estado de ferramenta atual.

        @param event (tk.Event): Evento de pressa da tecla Escape.
        """
        if self.estado:
            self.estado.tecla_esc(self, event)

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
            Inicializa o estado com a ferramenta padrão.

        @param tipo_figura_var (tk.StringVar): Variável de tipo de figura selecionado.
        @param cor_borda (tk.StringVar): Variável de cor da borda.
        @param cor_preenchimento (tk.StringVar): Variável de cor de preenchimento.
        """
        self.tipo_figura_var = tipo_figura_var
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.selecionar_ferramenta(tipo_figura_var.get())

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

        @param event (tk.Event, optional): Evento de teclado (Ctrl+S). Default: None.
        """
        self.save_dir = filedialog.asksaveasfilename(
            defaultextension='.json'
        )

        if self.save_dir:
            self.desenho.salvar(diretorio=self.save_dir)
