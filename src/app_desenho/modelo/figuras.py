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
        opcoes = {
            "fill": self.cor_borda
        }

        if tracejado:
            opcoes["dash"] = (4,2)
            
        return opcoes

class FiguraPreenchida(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(x1,y1,x2,y2,cor_borda)
        self.cor_preenchimento = cor_preenchimento

    def _opcoes_desenho(self, tracejado=False):
        opcoes = {"outline": self.cor_borda , "fill": self.cor_preenchimento}
        
        if tracejado:
            opcoes["dash"] = (4,2)
            
        return opcoes

class Linha(Figura):
    def desenhar(self, canvas, tracejado=False):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
         **self._opcoes_desenho(tracejado)
         )

    def to_dict(self):
        return {
            'tipo': 'Linha',
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'cor_borda': self.cor_borda,
        }

    @staticmethod
    def from_dict(dicionario: dict):
        return Linha(dicionario['x1'], dicionario['y1'], dicionario['x2'], dicionario['y2'], dicionario['cor_borda'])

class Rabisco(Figura):
    def __init__(self, x1, y1, cor_borda):
        super().__init__(x1, y1, x1, y1, cor_borda)
        self.pontos = [(x1,y1)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))    

    def esta_incompleta(self):
        return len(self.pontos) < 2

    def desenhar(self, canvas, tracejado=False):
        if len(self.pontos) < 2:
            return
        canvas.create_line(self.pontos, **self._opcoes_desenho(tracejado))

    def to_dict(self):
        return {
            'tipo': 'Rabisco',
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'cor_borda': self.cor_borda,
            'pontos': [list(p) for p in self.pontos],
        }

    @staticmethod
    def from_dict(dicionario: dict):
        r = Rabisco(dicionario['x1'], dicionario['y1'], dicionario['cor_borda'])
        r.pontos = [tuple(p) for p in dicionario['pontos']]
        r.x2 = dicionario['x2']
        r.y2 = dicionario['y2']
        return r

class Retangulo(FiguraPreenchida):
    def desenhar(self, canvas, tracejado=False):
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            **self._opcoes_desenho(tracejado)
        )

    def to_dict(self):
        return {
            'tipo': 'Retangulo',
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'cor_borda': self.cor_borda,
            'cor_preenchimento': self.cor_preenchimento,
        }

    @staticmethod
    def from_dict(dicionario: dict):
        return Retangulo(dicionario['x1'], dicionario['y1'], dicionario['x2'], dicionario['y2'], dicionario['cor_borda'], dicionario['cor_preenchimento'])

class Oval(FiguraPreenchida):
    def desenhar(self, canvas, tracejado=False):
        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            **self._opcoes_desenho(tracejado)
        )

    def to_dict(self):
        return {
            'tipo': 'Oval',
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'cor_borda': self.cor_borda,
            'cor_preenchimento': self.cor_preenchimento,
        }

    @staticmethod
    def from_dict(dicionario: dict):
        return Oval(dicionario['x1'], dicionario['y1'], dicionario['x2'], dicionario['y2'], dicionario['cor_borda'], dicionario['cor_preenchimento'])

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

    def to_dict(self):
        return {
            'tipo': 'Circulo',
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'cor_borda': self.cor_borda,
            'cor_preenchimento': self.cor_preenchimento,
        }

    @staticmethod
    def from_dict(dicionario: dict):
        return Circulo(dicionario['x1'], dicionario['y1'], dicionario['x2'], dicionario['y2'], dicionario['cor_borda'], dicionario['cor_preenchimento'])

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

    def to_dict(self):
        return {
            'tipo': 'Poligono',
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'cor_borda': self.cor_borda,
            'cor_preenchimento': self.cor_preenchimento,
            'pontos': [list(p) for p in self.pontos],
            'finalizado': self.finalizado,
        }

    @staticmethod
    def from_dict(dicionario: dict):
        p = Poligono(dicionario['x1'], dicionario['y1'], dicionario['cor_borda'], dicionario['cor_preenchimento'])
        p.pontos = [tuple(pt) for pt in dicionario['pontos']]
        p.x2 = dicionario['x2']
        p.y2 = dicionario['y2']
        p.finalizado = dicionario['finalizado']
        return p

CLASSES_FIGURA = {
    'Linha': Linha,
    'Retangulo': Retangulo,
    'Oval': Oval,
    'Circulo': Circulo,
}

def figura_from_dict(dicionario: dict):
    mapa = {
        'Linha': Linha,
        'Rabisco': Rabisco,
        'Retangulo': Retangulo,
        'Oval': Oval,
        'Circulo': Circulo,
        'Poligono': Poligono,
    }
    tipo = dicionario['tipo']
    if tipo not in mapa:
        raise ValueError(f'Tipo de figura desconhecido: {tipo}')
    return mapa[tipo].from_dict(dicionario)