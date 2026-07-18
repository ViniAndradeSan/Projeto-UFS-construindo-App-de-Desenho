from modelo.figuras import Poligono
from .estado_ferramenta import EstadoFerramenta


class EstadoPoligono(EstadoFerramenta):
    """Estado de ferramenta para o Polígono (desenho multi-clique).

    Finalidade:
        Encapsular o fluxo clique-a-clique de construção de polígonos,
        onde cada clique adiciona um vértice e o polígono só é finalizado
        por duplo clique ou tecla Enter.

    Responsabilidade:
        Criar o polígono no primeiro clique, adicionar vértices nos cliques
        subsequentes, atualizar a prévia ao mover o mouse, e finalizar
        quando o usuário indica que terminou (duplo clique / Enter).

    Uso:
        Instanciar com `EstadoPoligono()` e registrar no dicionário
        `ESTADOS_FERRAMENTA` do Controlador.

    @author Danillo
    @version 1.0
    @see EstadoFerramenta
    """

    def mouse_pressionado(self, controlador, event):
        """Adiciona um vértice ou cria um novo polígono.

        Descrição:
            Se já existe um polígono em construção, adiciona um novo vértice.
            Caso contrário, cria um polígono novo com o ponto do clique.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento do mouse com as coordenadas do clique.
        """
        if controlador.figura_nova is not None and isinstance(controlador.figura_nova, Poligono):
            controlador.figura_nova.adicionar_vertice(event.x, event.y)
        else:
            controlador.figura_nova = Poligono(
                event.x, event.y,
                controlador.cor_borda.get(), controlador.cor_preenchimento.get()
            )
        controlador.area_desenho.atualizar(controlador.desenho.figuras, controlador.figura_nova)

    def mouse_arrastado(self, controlador, event):
        """Ignorado — polígonos não usam arrasto."""
        pass

    def mouse_solto(self, controlador, event):
        """Ignorado — polígonos não finalizam ao soltar o botão."""
        pass

    def mouse_movido(self, controlador, event):
        """Atualiza a prévia do polígono durante o movimento do mouse.

        Descrição:
            Mantém uma linha de pré-visualização do último vértice até a
            posição atual do cursor, sem adicioná-lo permanentemente.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de movimento do mouse.
        """
        if controlador.figura_nova is not None and isinstance(controlador.figura_nova, Poligono):
            controlador.figura_nova.atualizar(event.x, event.y)
            controlador.area_desenho.atualizar(controlador.desenho.figuras, controlador.figura_nova)

    def duplo_clique(self, controlador, event):
        """Finaliza o polígono em construção via duplo clique.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de duplo clique.
        """
        self._finalizar(controlador)

    def tecla_enter(self, controlador, event):
        """Finaliza o polígono em construção via tecla Enter.

        @param controlador (Controlador): Controlador da aplicação.
        @param event (tk.Event): Evento de tecla pressionada.
        """
        self._finalizar(controlador)

    def _finalizar(self, controlador):
        """Finaliza o polígono e o adiciona ao desenho, se válido.

        Descrição:
            Marca o polígono como finalizado. Se ele tiver 3 ou mais vértices,
            adiciona ao desenho. Caso contrário, descarta.
            Limpa `figura_nova` e redesenha a área.

        @param controlador (Controlador): Controlador da aplicação.
        """
        if controlador.figura_nova is None or not isinstance(controlador.figura_nova, Poligono):
            return

        controlador.figura_nova.finalizar()

        if not controlador.figura_nova.esta_incompleta():
            controlador.desenho.adicionar(controlador.figura_nova)

        controlador.figura_nova = None
        controlador.area_desenho.atualizar(controlador.desenho.figuras, controlador.figura_nova)
