from .figuras import figura_from_dict
import json

class Desenho:
    def __init__(self):
        self._figuras = []
        self._figura_atual = []
        self._cor_borda = []
        self._cor_preenchimento = []
        self._tipo_ferramenta = []

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
        modelo = Desenho()
        for figuradata in dicionario['figuras']:
            modelo._figuras.append(figura_from_dict(figuradata))
        return modelo

    def abrir(self, diretorio):
        with open(diretorio, 'r') as file:
            self.arquivo = json.load(file) 
        self.limpar()
        for figura_dict in self.arquivo["figuras"]:
            figura = figura_from_dict(figura_dict)
            self._figuras.append(figura)


    def salvar(self, diretorio):
        self.figuras_serializadas = self.to_dict()
        with open(diretorio, "w") as file:
            json.dump(self.figuras_serializadas, file, indent=4)