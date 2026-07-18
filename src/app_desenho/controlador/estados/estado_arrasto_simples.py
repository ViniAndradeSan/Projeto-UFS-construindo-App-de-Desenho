from modelo.figuras import Rabisco
from .estado_ferramenta import EstadoFerramenta


class EstadoArrastoSimples(EstadoFerramenta):
    """Estado de ferramenta para figuras do tipo clique-arrasta-solta.

    Finalidade:
        Cobrir, com uma única classe, as ferramentas Linha, Retangulo, Oval e
        Circulo — todas seguem o mesmo fluxo de interação (clique inicia,
        arrasto atualiza, soltar o botão finaliza), diferindo apenas em qual
        classe de Figura instanciar e se ela usa cor de preenchimento.

    Responsabilidade:
        Criar a figura certa no clique (sem condicional: a classe vem por
        parâmetro do construtor), atualizar sua posição durante o arrasto e
        adicioná-la ao desenho ao soltar o botão, se estiver completa.

    Uso:
        Instanciar uma vez por ferramenta, por exemplo
        `EstadoArrastoSimples(Retangulo)` ou `EstadoArrastoSimples(Linha,
        usa_preenchimento=False)`, e reaproveitar essa mesma instância para
        todas as figuras desse tipo desenhadas durante a sessão.

    @author Danillo
    @version 1.0
    @see EstadoFerramenta
    """

    def __init__(self, classe_figura, usa_preenchimento=True):
        """Configura qual classe de Figura este estado cria.

        @param classe_figura (type): Classe de Figura a instanciar (ex:
            Retangulo, Oval, Circulo, Linha).
        @param usa_preenchimento (bool): Se True, a figura recebe cor de
            preenchimento além da cor de borda. Default: True.
        """
        self.classe_figura = classe_figura
        self.usa_preenchimento = usa_preenchimento

    def mouse_pressionado(self, controlador, event):
        """Cria uma figura nova no ponto do clique.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento do mouse com as coordenadas do clique.
        """
        if self.usa_preenchimento:
            controlador.figura_nova = self.classe_figura(
                event.x, event.y, event.x, event.y,
                controlador.cor_borda.get(), controlador.cor_preenchimento.get()
            )
        else:
            controlador.figura_nova = self.classe_figura(
                event.x, event.y, event.x, event.y,
                controlador.cor_borda.get()
            )
        controlador.area_desenho.atualizar(controlador.desenho.figuras, controlador.figura_nova)

    def mouse_arrastado(self, controlador, event):
        """Atualiza o ponto final da figura em construção.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento do mouse durante o arrasto.
        """
        if controlador.figura_nova is None:
            return
        controlador.figura_nova.atualizar(event.x, event.y)
        controlador.area_desenho.atualizar(controlador.desenho.figuras, controlador.figura_nova)

    def mouse_solto(self, controlador, event):
        """Finaliza a figura e a adiciona ao desenho, se estiver completa.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de liberação do botão do mouse.
        """
        if controlador.figura_nova is None:
            return
        if not controlador.figura_nova.esta_incompleta():
            controlador.desenho.adicionar(controlador.figura_nova)
        controlador.figura_nova = None
        controlador.area_desenho.atualizar(controlador.desenho.figuras, controlador.figura_nova)


class EstadoRabisco(EstadoArrastoSimples):
    """Estado de ferramenta para o Rabisco (traço livre).

    Finalidade:
        Reaproveitar o arrasto/soltura de `EstadoArrastoSimples`, mudando só
        como a figura nasce, já que o construtor de `Rabisco` não tem x2/y2
        nem cor de preenchimento.

    Responsabilidade:
        Criar o `Rabisco` no clique inicial; o resto do comportamento (mover
        e soltar) é herdado sem alteração, porque `Rabisco.atualizar` e
        `Rabisco.esta_incompleta` já sabem se comportar de forma diferente
        por polimorfismo.

    Uso:
        Instanciar com `EstadoRabisco()` (sem argumentos).

    @author Danillo
    @version 1.0
    @see EstadoArrastoSimples
    """

    def __init__(self):
        """Configura este estado para sempre criar um Rabisco."""
        super().__init__(Rabisco, usa_preenchimento=False)

    def mouse_pressionado(self, controlador, event):
        """Cria um Rabisco novo no ponto do clique.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento do mouse com as coordenadas do clique.
        """
        controlador.figura_nova = Rabisco(event.x, event.y, controlador.cor_borda.get())
        controlador.area_desenho.atualizar(controlador.desenho.figuras, controlador.figura_nova)
