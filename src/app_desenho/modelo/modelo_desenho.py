from .figuras import figura_from_dict
import json

class Desenho:
    """Modelo de desenho que agrupa figuras e manipula seu estado.

    Finalidade:
        Manter a lista de figuras criadas, permitir desfazer, limpar e gerenciar
        carregamento/salvamento.

    Responsabilidade:
        Ser o repositório de dados do desenho e converter figuras para/desde
        representação JSON.

    Uso:
        Instanciar com `Desenho()`, utilizar `adicionar(figura)`, `desfazer()`,
        `limpar()`, `abrir(diretorio)` e `salvar(diretorio)`.

    @author Danillo
    @version 1.0
    """

    def __init__(self):
        """Inicializa o modelo de desenho com sua lista interna vazia.

        Objetivo:
            Preparar o estado inicial do desenho para receber figuras.

        """
        self._figuras = []
        self._figura_atual = []
        self._cor_borda = []
        self._cor_preenchimento = []
        self._tipo_ferramenta = []

    @property
    def figuras(self):
        """Retorna uma cópia da lista de figuras.

        Descrição:
            Fornece acesso à lista de figuras sem permitir modificações diretas.

        @return list: Cópia da lista de figuras atuais.
        """
        return list(self._figuras)
    
    def adicionar(self, figura):
        """Adiciona uma figura ao desenho.

        Descrição:
            Anexa uma figura completada à lista de figuras do desenho.

        @param figura (Figura): Instância de uma figura completa para adicionar.
        """
        self._figuras.append(figura)

    def desfazer(self):
        """Remove e retorna a última figura adicionada.

        Descrição:
            Executa uma operação de desfazer removendo a figura do topo da pilha.

        @return Figura ou None: A última figura adicionada, ou None se a lista está vazia.
        """
        if self._figuras:
            return self._figuras.pop()

    def limpar(self):
        """Remove todas as figuras do desenho.

        Descrição:
            Limpa completamente a lista de figuras.
        """
        self._figuras.clear()

    def criar(self):
        """Método para criar novo desenho.

        Descrição:
            Atualiza o estado do desenho para um novo estado vazio.
        """
        self.limpar()

    def esta_vazio(self):
        """Verifica se o desenho não possui figuras.

        Descrição:
            Retorna verdadeiro se a lista de figuras está vazia.

        @return bool: True se não há figuras, False caso contrário.
        """
        return len(self._figuras) == 0

    def to_dict(self):
        """Serializa o desenho em dicionário.

        Descrição:
            Converte todas as figuras em dicionários para salvamento em JSON.

        @return dict: Dicionário com lista de figuras serializadas.
        """
        return {
            'figuras': [f.to_dict() for f in self._figuras],
        }

    @staticmethod
    def from_dict(dicionario: dict):
        """Desserializa um desenho a partir de um dicionário.

        Descrição:
            Reconstrói uma instância de Desenho com todas as figuras armazenadas.

        @param dicionario (dict): Dicionário contendo dados de figuras serializadas.
        @return Desenho: Nova instância de Desenho com as figuras restauradas.
        """
        modelo = Desenho()
        for figuradata in dicionario['figuras']:
            modelo._figuras.append(figura_from_dict(figuradata))
        return modelo

    def abrir(self, diretorio):
        """Carrega um desenho a partir de um arquivo JSON.

        Descrição:
            Lê um arquivo JSON e reconstrói todas as figuras, limpando o estado atual.

        @param diretorio (str): Caminho do arquivo JSON a ser carregado.
        @throws FileNotFoundError: Se o arquivo não existir.
        @throws json.JSONDecodeError: Se o arquivo não for um JSON válido.
        """
        with open(diretorio, 'r') as file:
            self.arquivo = json.load(file) 
        self.limpar()
        for figura_dict in self.arquivo["figuras"]:
            figura = figura_from_dict(figura_dict)
            self._figuras.append(figura)


    def salvar(self, diretorio):
        """Salva o desenho em um arquivo JSON.

        Descrição:
            Serializa todas as figuras e escreve em um arquivo JSON.

        @param diretorio (str): Caminho do arquivo JSON onde salvar.
        @throws IOError: Se não for possível escrever no arquivo.
        """
        self.figuras_serializadas = self.to_dict()
        with open(diretorio, "w") as file:
            json.dump(self.figuras_serializadas, file, indent=4)