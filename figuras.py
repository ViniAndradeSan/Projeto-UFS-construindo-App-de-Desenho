from abc import ABC, abstractmethod

class Figura(ABC):
    def __init__(self, x1, y1, x2, y2, cor_borda):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.cor_borda = cor_borda

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y

    @abstractmethod
    def desenhar(self, canvas, tracejado=False):
        pass

    def esta_incompleta(self):
        return (self.x1, self.y1) == (self.x2, self.y2)


class FiguraPreenchida(Figura):
    pass


class Retangulo(FiguraPreenchida):
    def desenhar(self, canvas, tracejado=False):
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            **self._opcoes_desenho(tracejado)
        )


class Oval(FiguraPreenchida):
    def desenhar(self, canvas, tracejado=False):
        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            **self._opcoes_desenho(tracejado)
        )


class Circulo(FiguraPreenchida):
    def desenhar(self, canvas, tracejado=False):
        x1, x2 = min(self.x1, self.x2), max(self.x1, self.x2)
        y1, y2 = min(self.y1, self.y2), max(self.y1, self.y2)
        largura = x2 - x1
        altura = y2 - y1
        lado = min(largura, altura)
        centrox = (x1 + x2) // 2
        centroy = (y1 + y2) // 2
        raio = lado // 2

        canvas.create_oval(
            centrox - raio, centroy - raio,
            centrox + raio, centroy + raio,
            **self._opcoes_desenho(tracejado)
        )