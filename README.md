# Aplicativo de desenho

## Equipe: Guerreiros do Clean Code

Este projeto foi feito por essa magestosa equipe composta por:

- Danillo Matos Garcez
- Vinicius Andrade Santos
- Julyana Azevedo Lima

## Sobre o sistema

O **Aplicativo de desenho** é um app feita em Python, utilizando a biblioteca Tkinter para a interface gráfica. Ele funciona como uma espécie de "paint".
O projeto foi estruturado seguindo o padrão de arquitetura **MVC (Model-View-Controller)**:

- **Modelo** (`modelo/`): representa as figuras geométricas e o desenho como um todo, incluindo lógica de criação, desfazer, salvar e abrir arquivos.
- **Visão** (`visao/`): responsavel da interface gráfica: área de desenho, barra de ferramentas e menu.
- **Controlador** (`controlador/`): faz a ligação entre o modelo e a visão, tratando os eventos de mouse e teclado do usuário.

## Documentação gerada

Toda a documentação foi produzida a partir dos pydoc/docstrings presentes diretamente no código-fonte. Nós ao todo documentamos:

- **13 classes**
- **63 métodos e funções**

## Como visualizar a documentação

A documentação está disponível em formato HTML, dentro da pasta `docs/`. Para consultá-la, basta:

1. Baixar o zip, ou clonar este repositório.
2. Acessar a pasta `docs/`.
3. Abrir qualquer um dos arquivos `.html` (por exemplo, `app_desenho.main.html`) diretamente no seu navegador de preferência, não é necessário nenhum servidor ou instalação adicional, mas se
preferir pode usar extenções como o `live Server` do proprio `VScode`.

A partir da página inicial da documentação, graças ao pydoc, é possível navegar entre os módulos do sistema (`modelo`, `visao` e `controlador`) e consultar as classes, métodos e suas respectivas descrições.

---

Atenciosamente, **Guerreiros do Clean Code**
