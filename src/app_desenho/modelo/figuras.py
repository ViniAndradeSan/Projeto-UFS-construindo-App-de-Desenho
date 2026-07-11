from abc import ABC, abstractmethod

class Figura(ABC):
    """Base abstrata para figuras geométricas do desenho.

    Finalidade:
        Fornecer atributos comuns de coordenadas e cor de borda, além de uma
        interface unificada para atualização e desenho.

    Responsabilidade:
        Manter a posição inicial e final de uma figura e definir métodos que as
        subclasses devem implementar.

    Uso:
        Estender esta classe e implementar o método `desenhar(canvas,
        tracejado=False)`.

    Autor: Vinicius
    Versão: 1.0
    """

    def __init__(self, x1, y1, x2, y2, cor_borda):
        """Inicializa os atributos básicos de uma figura.

        Objetivo:
            Configurar as coordenadas de início e fim e a cor da borda.

        Args:
            x1 (int): Coordenada x do ponto inicial.
            y1 (int): Coordenada y do ponto inicial.
            x2 (int): Coordenada x do ponto final.
            y2 (int): Coordenada y do ponto final.
            cor_borda (str): Cor da borda para desenho.
        """
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.cor_borda = cor_borda

    def atualizar(self, x, y):
        """Atualiza a coordenada final da figura.

        Descrição:
            Modifica o ponto final (x2, y2) para a nova posição fornecida.

        Args:
            x (int): Coordenada x da nova posição final.
            y (int): Coordenada y da nova posição final.
        """
        self.x2, self.y2 = x, y

    @abstractmethod
    def desenhar(self, canvas, tracejado=False):
        """Renderiza a figura no canvas.

        Descrição:
            Desenha a figura usando o método apropriado do canvas Tkinter.

        Args:
            canvas (tk.Canvas): Canvas onde a figura será desenhada.
            tracejado (bool): Se True, desenha com linha tracejada. Default(tracejado): False.
        """
        pass

    def esta_incompleta(self):
        """Verifica se a figura ainda está em construção.

        Descrição:
            Uma figura está incompleta se o ponto inicial e final são iguais,
            indicando que ainda não foi pelo menos arrastada.

        Returns:
            bool: True se a figura está incompleta, False caso contrário.
        """
        return (self.x1, self.y1) == (self.x2, self.y2)

    def _opcoes_desenho(self, tracejado=False):
        opcoes = {
            "fill": self.cor_borda
        }

        if tracejado:
            opcoes["dash"] = (4,2)
            
        return opcoes

class FiguraPreenchida(Figura):
    """Figura com preenchimento interna usada no desenho.

    Finalidade:
        Adicionar suporte a cor de preenchimento em figuras derivadas.

    Responsabilidade:
        Estender `Figura` com a cor de preenchimento e ajustar as opções de
        desenho para exibir tanto contorno quanto preenchimento.

    Uso:
        Não é instanciada diretamente; serve como base para figuras como
        `Retangulo`, `Oval` e `Circulo`.

    Autor: Vinicius
    Versão: 1.0
    """

    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        """Inicializa uma figura com cor de preenchimento.

        Objetivo:
            Configurar coordenadas, cor de borda e cor de preenchimento.

        Args:
            x1 (int): Coordenada x do ponto inicial.
            y1 (int): Coordenada y do ponto inicial.
            x2 (int): Coordenada x do ponto final.
            y2 (int): Coordenada y do ponto final.
            cor_borda (str): Cor da borda.
            cor_preenchimento (str): Cor de preenchimento interno.
        """
        super().__init__(x1,y1,x2,y2,cor_borda)
        self.cor_preenchimento = cor_preenchimento

    def _opcoes_desenho(self, tracejado=False):
        opcoes = {"outline": self.cor_borda , "fill": self.cor_preenchimento}
        
        if tracejado:
            opcoes["dash"] = (4,2)
            
        return opcoes

class Linha(Figura):
    """Representa uma linha reta desenhável.

    Finalidade:
        Modelar uma linha com duas extremidades e renderizá-la em um canvas.

    Responsabilidade:
        Atualizar as coordenadas finais e desenhar a linha usando a cor de
        borda configurada.

    Uso:
        Instanciar com `Linha(x1, y1, x2, y2, cor_borda)` e chamar
        `desenhar(canvas)` para renderizá-la.

    Autor: Vinicius
    Versão: 1.0
    """

    def desenhar(self, canvas, tracejado=False):
        """Desenha uma linha no canvas.

        Descrição:
            Renderiza uma linha reta entre os pontos inicial e final.

        Args:
            canvas (tk.Canvas): Canvas onde desenhar.
            tracejado (bool): Se True, desenha com linha tracejada. Default(tracejado): False.
        """
        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
         **self._opcoes_desenho(tracejado)
         )

    def to_dict(self):
        """Serializa a linha em dicionário.

        Descrição:
            Converte os atributos da linha em um dicionário para salvamento em JSON.

        Returns:
            dict: Dicionário com os dados da linha.
        """
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
        """Desserializa uma linha a partir de um dicionário.

        Descrição:
            Reconstrói uma instância de Linha a partir de dados serializados.

        Args:
            dicionario (dict): Dicionário contendo dados da linha.

        Returns:
            Linha: Nova instância de Linha.
        """
        return Linha(dicionario['x1'], dicionario['y1'], dicionario['x2'], dicionario['y2'], dicionario['cor_borda'])

class Rabisco(Figura):
    """Representa um traço livre como sequência de pontos.

    Finalidade:
        Permitir desenho solto com múltiplos segmentos conectados.

    Responsabilidade:
        Armazenar uma lista de pontos e renderizar o traço no canvas.

    Uso:
        Instanciar com `Rabisco(x1, y1, cor_borda)`, chamar `atualizar(x, y)`
        para adicionar pontos e `desenhar(canvas)` para renderizar.

    Autor: Vinicius
    Versão: 1.0
    """

    def __init__(self, x1, y1, cor_borda):
        """Inicializa um rabisco livre com o ponto inicial.

        Objetivo:
            Criar um traço em construção armazenando o primeiro ponto.

        Args:
            x1 (int): Coordenada x inicial do rabisco.
            y1 (int): Coordenada y inicial do rabisco.
            cor_borda (str): Cor da linha do rabisco.
        """
        super().__init__(x1, y1, x1, y1, cor_borda)
        self.pontos = [(x1,y1)]

    def atualizar(self, x, y):
        """Adiciona um novo ponto ao rabisco.

        Descrição:
            Anexa as coordenadas fornecidas à lista de pontos do traço livre.

        Args:
            x (int): Coordenada x do novo ponto.
            y (int): Coordenada y do novo ponto.
        """
        self.pontos.append((x, y))    

    def esta_incompleta(self):
        """Verifica se o rabisco tem menos de 2 pontos.

        Descrição:
            Um rabisco está incompleto se possui menos de 2 pontos (sem poder desenhar).

        Returns:
            bool: True se o rabisco tem menos de 2 pontos, False caso contrário.
        """
        return len(self.pontos) < 2

    def desenhar(self, canvas, tracejado=False):
        """Desenha o rabisco como uma sequência de linha conectada.

        Descrição:
            Renderiza todos os pontos conectados no canvas se houver pelo menos 2 pontos.

        Args:
            canvas (tk.Canvas): Canvas onde desenhar.
            tracejado (bool): Se True, desenha com linha tracejada. Default: False.
        """
        if len(self.pontos) < 2:
            return
        canvas.create_line(self.pontos, **self._opcoes_desenho(tracejado))

    def to_dict(self):
        """Serializa o rabisco em dicionário.

        Descrição:
            Converte os atributos do rabisco incluindo a lista de pontos para JSON.

        Returns:
            dict: Dicionário com os dados do rabisco.
        """
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
        """Desserializa um rabisco a partir de um dicionário.

        Descrição:
            Reconstrói uma instância de Rabisco incluindo a lista de pontos.

        Args:
            dicionario (dict): Dicionário contendo dados do rabisco.

        Returns:
            Rabisco: Nova instância de Rabisco.
        """
        r = Rabisco(dicionario['x1'], dicionario['y1'], dicionario['cor_borda'])
        r.pontos = [tuple(p) for p in dicionario['pontos']]
        r.x2 = dicionario['x2']
        r.y2 = dicionario['y2']
        return r

class Retangulo(FiguraPreenchida):
    """Representa um retângulo preenchido no desenho.

    Finalidade:
        Criar e desenhar um retângulo com contorno e preenchimento.

    Responsabilidade:
        Aplicar as coordenadas e opções de estilo no método de desenho.

    Uso:
        Instanciar com `Retangulo(x1, y1, x2, y2, cor_borda,
        cor_preenchimento)` e chamar `desenhar(canvas)` para renderizar.

    Autor: Vinicius
    Versão: 1.0
    """

    def desenhar(self, canvas, tracejado=False):
        """Desenha um retângulo no canvas.

        Descrição:
            Renderiza um retângulo com contorno e preenchimento.

        Args:
            canvas (tk.Canvas): Canvas onde desenhar.
            tracejado (bool): Se True, desenha com linha tracejada. Default(tracejado): False.
        """
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            **self._opcoes_desenho(tracejado)
        )

    def to_dict(self):
        """Serializa o retângulo em dicionário.

        Descrição:
            Converte os atributos do retângulo em dados para salvamento em JSON.

        Returns:
            dict: Dicionário com os dados do retângulo.
        """
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
        """Desserializa um retângulo a partir de um dicionário.

        Descrição:
            Reconstrói uma instância de Retangulo a partir de dados serializados.

        Args:
            dicionario (dict): Dicionário contendo dados do retângulo.

        Returns:
            Retangulo: Nova instância de Retangulo.
        """
        return Retangulo(dicionario['x1'], dicionario['y1'], dicionario['x2'], dicionario['y2'], dicionario['cor_borda'], dicionario['cor_preenchimento'])

class Oval(FiguraPreenchida):
    """Representa uma elipse preenchida no desenho.

    Finalidade:
        Desenhar uma forma oval com contorno e preenchimento.

    Responsabilidade:
        Utilizar as coordenadas de dois cantos opostos para renderizar a oval.

    Uso:
        Instanciar com `Oval(x1, y1, x2, y2, cor_borda,
        cor_preenchimento)` e chamar `desenhar(canvas)`.

    Autor: Vinicius
    Versão: 1.0
    """

    def desenhar(self, canvas, tracejado=False):
        """Desenha uma oval no canvas.

        Descrição:
            Renderiza uma forma oval com contorno e preenchimento.

        Args:
            canvas (tk.Canvas): Canvas onde desenhar.
            tracejado (bool): Se True, desenha com linha tracejada. Default(tracejado): False.
        """
        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            **self._opcoes_desenho(tracejado)
        )

    def to_dict(self):
        """Serializa a oval em dicionário.

        Descrição:
            Converte os atributos da oval em dados para salvamento em JSON.

        Returns:
            dict: Dicionário com os dados da oval.
        """
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
        """Desserializa uma oval a partir de um dicionário.

        Descrição:
            Reconstrói uma instância de Oval a partir de dados serializados.

        Args:
            dicionario (dict): Dicionário contendo dados da oval.

        Returns:
            Oval: Nova instância de Oval.
        """
        return Oval(dicionario['x1'], dicionario['y1'], dicionario['x2'], dicionario['y2'], dicionario['cor_borda'], dicionario['cor_preenchimento'])

class Circulo(FiguraPreenchida):
    """Representa um círculo preenchido no desenho.

    Finalidade:
        Desenhar um círculo baseado em uma área delimitada por dois pontos.

    Responsabilidade:
        Calcular o centro e o raio para renderizar um círculo perfeito.

    Uso:
        Instanciar com `Circulo(x1, y1, x2, y2, cor_borda,
        cor_preenchimento)` e chamar `desenhar(canvas)`.

    Autor: Vinicius
    Versão: 1.0
    """

    def desenhar(self, canvas, tracejado=False):
        """Desenha um círculo no canvas.

        Descrição:
            Renderiza um círculo perfeito calculando o raio a partir da área fornecida.

        Args:
            canvas (tk.Canvas): Canvas onde desenhar.
            tracejado (bool): Se True, desenha com linha tracejada. Default(tracejado): False.
        """
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
        """Serializa o círculo em dicionário.

        Descrição:
            Converte os atributos do círculo em dados para salvamento em JSON.

        Returns:
            dict: Dicionário com os dados do círculo.
        """
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
        """Desserializa um círculo a partir de um dicionário.

        Descrição:
            Reconstrói uma instância de Circulo a partir de dados serializados.

        Args:
            dicionario (dict): Dicionário contendo dados do círculo.

        Returns:
            Circulo: Nova instância de Circulo.
        """
        return Circulo(dicionario['x1'], dicionario['y1'], dicionario['x2'], dicionario['y2'], dicionario['cor_borda'], dicionario['cor_preenchimento'])

class Poligono(FiguraPreenchida):
    """Representa um polígono construído por vértices.

    Finalidade:
        Permitir desenho de formas poligonais com vários vértices.

    Responsabilidade:
        Armazenar vértices, acompanhar se o polígono foi finalizado e
        renderizá-lo corretamente.

    Uso:
        Criar com `Poligono(x, y, cor_borda, cor_preenchimento)`, usar
        `adicionar_vertice(x, y)` para cada novo ponto, e `finalizar()` antes de
        adicionar ao desenho.

    Autor: Vinicius
    Versão: 1.0
    """

    def __init__(self, x, y, cor_borda, cor_preenchimento):
        """Inicializa um polígono em construção com o primeiro vértice.

        Objetivo:
            Criar a estrutura de pontos e configurar cores para o polígono.

        Args:
            x (int): Coordenada x do primeiro vértice.
            y (int): Coordenada y do primeiro vértice.
            cor_borda (str): Cor da borda do polígono.
            cor_preenchimento (str): Cor de preenchimento do polígono.
        """
        self.pontos = [(x, y)]
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x, y
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.finalizado = False

    def adicionar_vertice(self, x, y):
        """Adiciona um novo vértice ao polígono.

        Descrição:
            Anexa as coordenadas como um novo ponto e atualiza a posição final.

        Args:
            x (int): Coordenada x do novo vértice.
            y (int): Coordenada y do novo vértice.
        """
        self.pontos.append((x, y))
        self.x2, self.y2 = x, y

    def atualizar(self, x, y):
        """Atualiza a posição temporária enquanto se desenha.

        Descrição:
            Modifica o último ponto sem adicioná-lo permanentemente (linha de pré-visualização).

        Args:
            x (int): Coordenada x da posição temporária.
            y (int): Coordenada y da posição temporária.
        """
        self.x2, self.y2 = x, y

    def finalizar(self):
        """Marca o polígono como finalizado.

        Descrição:
            Define o polígono como completo e pronto para ser adicionado ao desenho.
        """
        self.finalizado = True

    def esta_incompleta(self):
        """Verifica se o polígono ainda está em construção.

        Descrição:
            Um polígono está incompleto se não foi finalizado ou tem menos de 3 pontos.

        Returns:
            bool: True se incompleto, False se é um polígono válido finalizado.
        """

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
        """Desenha o polígono no canvas.

        Descrição:
            Se finalizado, renderiza como polígono preenchido; caso contrário, como linha tracejada.

        Args:
            canvas (tk.Canvas): Canvas onde desenhar.
            tracejado (bool): Se True, desenha com linha tracejada. Default: False.
        """
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
        """Serializa o polígono em dicionário.

        Descrição:
            Converte todos os atributos do polígono incluindo a lista de vértices.

        Returns:
            dict: Dicionário com os dados do polígono.
        """
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
        """Desserializa um polígono a partir de um dicionário.

        Descrição:
            Reconstrói uma instância de Poligono incluindo todos os vértices e estado.

        Args:
            dicionario (dict): Dicionário contendo dados do polígono.

        Returns:
            Poligono: Nova instância de Poligono.
        """
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
    """Instancia a classe de figura correta a partir de um dicionário.

    Finalidade:
        Reconstruir obejtos feitos de Figura a partir de dados serializados.

    Responsabilidade:
        Identificar a etiqueta de tipo no dicionário e despachar a criação
        para o método estático `from_dict` da subclasse correspondente.

    Uso:
        Chamar `figura_from_dict(dados_da_figura)` ao ler dados de um arquivo.

    Autor: Vinicius
    Versão: 1.0
    """
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
