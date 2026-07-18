from abc import ABC, abstractmethod


class EstadoFerramenta(ABC):
    """Contrato base para os estados de ferramenta do Controlador.

    Finalidade:
        Definir a interface comum que toda ferramenta de desenho (Linha,
        Retangulo, Rabisco, Poligono, ...) precisa cumprir para reagir a
        eventos de mouse e teclado.

    Responsabilidade:
        Declarar os eventos possíveis (mouse pressionado/arrastado/solto/
        movido, duplo clique, Enter, Esc) e fornecer o comportamento padrão
        de Esc, igual para qualquer ferramenta.

    Uso:
        Estender esta classe e implementar `mouse_pressionado`. Sobrescrever
        os demais métodos só quando a ferramenta precisar reagir a esses
        eventos (o padrão de todos, exceto Esc, é não fazer nada).

    @author Danillo
    @version 1.0
    """

    @abstractmethod
    def mouse_pressionado(self, controlador, event):
        """Reage ao clique inicial do mouse (obrigatório para toda ferramenta).

        @param controlador (Controlador): Controlador que guarda o estado da
            interação (figura_nova, desenho, area_desenho, cores).
        @param event (tk.Event): Evento do mouse com as coordenadas do clique.
        """
        pass

    def mouse_arrastado(self, controlador, event):
        """Reage ao arrastar do mouse com o botão pressionado.

        Descrição:
            Não faz nada por padrão; ferramentas que precisam atualizar uma
            prévia durante o arrasto sobrescrevem este método.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento do mouse durante o arrasto.
        """
        pass

    def mouse_solto(self, controlador, event):
        """Reage à liberação do botão do mouse.

        Descrição:
            Não faz nada por padrão; ferramentas que finalizam a figura ao
            soltar o botão sobrescrevem este método.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de liberação do botão do mouse.
        """
        pass

    def mouse_movido(self, controlador, event):
        """Reage ao movimento do mouse, mesmo sem o botão pressionado.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de movimento do mouse.
        """
        pass

    def duplo_clique(self, controlador, event):
        """Reage ao duplo clique do mouse.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de duplo clique.
        """
        pass

    def tecla_enter(self, controlador, event):
        """Reage à tecla Enter.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de tecla pressionada.
        """
        pass

    def tecla_esc(self, controlador, event):
        """Cancela a figura em construção (comportamento igual para todas).

        Descrição:
            Descarta `controlador.figura_nova`, se existir, e manda a área de
            desenho redesenhar sem nenhuma prévia. Igual para toda
            ferramenta, por isso já vem implementado aqui na base.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de tecla Escape.
        """
        if controlador.figura_nova is not None:
            controlador.figura_nova = None
            controlador.area_desenho.atualizar(controlador.desenho.figuras, controlador.figura_nova)
