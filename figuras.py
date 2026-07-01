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

    def _opcoes_desenho(self, tracejado=False):
        # Coloque aqui Danilo sua parte
        pass


class FiguraPreenchida(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        # Coloque aqui Danilo sua parte
        pass

    def _opcoes_desenho(self, tracejado=False):
        # Coloque aqui Danilo sua parte
        pass


class Linha(Figura):
    def desenhar(self, canvas, tracejado=False):
        # Coloque aqui Danilo sua parte
        pass


class Rabisco(Figura):
    def __init__(self, x, y, cor_borda):
        # Coloque aqui Danilo sua parte
        pass

    def atualizar(self, x, y):
        # Coloque aqui Danilo sua parte
        pass

    def esta_incompleta(self):
        # Coloque aqui Danilo sua parte
        pass

    def desenhar(self, canvas, tracejado=False):
        # Coloque aqui Danilo sua parte
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


class Poligono(FiguraPreenchida):

    def __init__(self, x, y, cor_borda, cor_preenchimento):
        self.pontos = [(x, y)]
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x, y
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.finalizado = False

    def adicionar_vertice(self, x, y):
        self.pontos.append((x, y))
        self.x2, self.y2 = x, y

    def atualizar(self, x, y):
        self.x2, self.y2 = x, y

    def finalizar(self):
        self.finalizado = True

    def esta_incompleta(self):

        return not self.finalizado or len(self.pontos) < 3

    def _pontos_para_desenho(self):
        pontos = list(self.pontos)
        if not self.finalizado:
            pontos.append((self.x2, self.y2))
        coords = []
        for px, py in pontos:
            coords.extend([px, py])
        return coords

    def desenhar(self, canvas, tracejado=False):
        coords = self._pontos_para_desenho()
        if len(coords) < 4:
            return

        opcoes = self._opcoes_desenho(tracejado)

        if self.finalizado and len(self.pontos) >= 3:
            canvas.create_polygon(coords, **opcoes)
        else:
            canvas.create_line(
                coords,
                fill=self.cor_borda,
                dash=(4, 2) if tracejado else None
            )