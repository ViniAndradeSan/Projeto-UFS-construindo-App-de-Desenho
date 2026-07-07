
class Desenho:
    def __init__(self):
        self._figuras = []

    @property
    def figuras(self):
        return list(self._figuras)

    def adicionar(self, figura):
        self._figuras.append(figura)

    def desfazer(self):
        if self._figuras:
            return self._figuras.pop()

    def limpar(self):
        self._figuras.clear()

    def esta_vazio(self):
        return len(self._figuras) == 0