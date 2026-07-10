from .figuras import figura_from_dict

class ModeloDesenho:
    def __init__(self):
        self._figuras = []
        self._figura_atual = []
        self._cor_borda = []
        self._cor_preenchimento = []
        self._tipo_ferramenta = []

    @property
    def figuras(self):
        return list(self._figuras)
<<<<<<< HEAD

    def adicionar(self, figura):
        self._figuras.append(figura)

    def desfazer(self):
        if self._figuras:
            return self._figuras.pop()

    def limpar(self):
        self._figuras.clear()

    def esta_vazio(self):
        return len(self._figuras) == 0
=======
    
    def adicionar(self, figura):
        self._figuras.append(figura)

    def desfazer(self):
        if self._figuras:
            return self._figuras.pop()

    def limpar(self):
        self._figras.clear()

    def criar(self):
        pass

    def esta_vazio(self):
        return len(self._figuras) == 0

    def to_dict(self):
        return {
            'figuras': [f.to_dict() for f in self._figuras],
        }

    @staticmethod
    def from_dict(dicionario: dict):
        modelo = ModeloDesenho()
        for figuradata in dicionario['figuras']:
            modelo._figuras.append(figura_from_dict(figuradata))
        return modelo
>>>>>>> b0b575f (feat(model): adicionando serialização das figura)
