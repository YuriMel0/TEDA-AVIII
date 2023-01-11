![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Avaliação III - Point Quad-Tree

### Descrição de implementação Point Quad-Tree:

Desenvolver um módulo, em C++ ou Python, que implementa parcialmente uma árvore Point Quad-tree, para dados pontuais de coordenadas (x,y), e utilizá-la na resolução do problema descrito abaixo.

Esta árvore não é balanceada e os seus dados (os pares de coordenadas de cada ponto) encontram-se nos seus nós folhas. Os nós internos possuem um array de quatro ponteiros para as quatros sub-árvores que contém as regiões colaterais (NO, NE, SE, SO). Os nós internos podem, ou não, conter um dado “Point2D”, com as coordenadas do centro de sua subdivisão, apesar de ser algo que se pode calcular apenas sabendo em que nível da árvore o nó se encontra (o que pode ser passado como parâmetro da chamada recursiva).

Os nós folhas, contendo os pontos (x,y), pode ser implementados tanto utilizando a mesma classe dos nós internos, como também como uma sub-classe especializada dos nós internos, ou mesmo como uma classe Folha independente. No caso de se reutilizar a classe dos nós internos, o seu array de ponteiros para os nós folhas devem todos estar nulos, e necessariamente ter o campo de dados “Point2D”, para hora armazenar as coordenadas do centro de sua subdivisão, quando for nó interno, e hora armazenar as coordenados do ponto (x,y), quando for utilizado como nó folha. As opções aqui sugeridas têm vantagens e desvantagens durante a codificação.

No caso da árvore Point Quad-Tree, esta deve ser projetada como uma classe OO que apresenta os seguintes métodos em sua interface:

- Criação da árvore
- Inserção de ponto p(x,y) na Point Quad-tree
- Consultas:
  - De ponto p(x,y). A resposta aqui é True caso o ponto esteja na árvore, e False, caso não esteja
  - Janela: dado um retângulo de canto superior esquerdo nas coordenadas (x1,y1), e canto inferior direito nas coordenadas (x1,y2), retornar uma lista dos pontos pertencentes ao retângulo (pontos interiores e pontos na borda).
  - Orientação cardeais: dado um ponto p(x,y) e um dos quatro pontos cardeais (N,S,L,O), ou um dos quatro pontos colaterais (NO, NE, SE, SO), recupera a lista de pontos que residem no respectivo semi-plano na direção cardeal, ou no respectivo quadrante nas direções colaterais.



### Descrição do Problema a ser solucionado utilizando um Point Quad-tree:

Imaginando uma interface via celular para visualizar um mapa de pontos (que podem representar, por exemplos, Farmácias, Postos de Abastecimentos etc.) através  de uma “janela de visão” (window view) sobre o mapa de pontos dado, em escala, pelas dimensões da tela do celular, onde a interface com o usuário, baseada em “toques na tela” (touch screen), permite realizar movimentos da “janela de visão” para as quatro direções cardeais, além de comandar um “zoom in” e “zoom out” (diminuição/aumento das dimensões das janela de visão).

Sendo assim, o exercício é tão somente “recuperar e apresentar” uma lista de pontos, armazenados em uma Point Quad-Tree, que residem em uma “janela de visão dada”, a qual é especificada através do seu “retângulo envolvente”, de canto superior esquerdo nas coordenadas (x1,y1), e canto inferior direito nas coordenadas (x1,y2). O programa deve permitir a alteração das coordenadas da janela a fim de simular os quatros movimentos nas direções cardeais (N,S,L,O), bem como a ampliação e diminuição proporcional das dimensões da janela, simulando o “zoom in, zoom out”.

O mapa de pontos deve ser armazenado em uma Point Quad-Tree criada de uma única vez, a partir de uma lista de pontos fornecida em um arquivo texto comum (contendo apenas uma lista de pares (x,y), coordenadas em números inteiros positivos para simplificar a CG.

A apresentação do resultado, ou seja, a visualização da lista de pontos dentro da “janela de visão” especificada, deve ser feita na tela do console, codificada através de uma matriz de pontos “m x n”, onde “m” é o número de linhas da tela do console, e “n” o número de colunas. Por exemplo, em uma tela WideScreen, com fonte padrão, a tela do console tem entre 40 a 45 linhas x 100 a 180 colunas. Lembre-se que se deseja uma janela proporcional a de um celular, onde se tem uma dimensão bem maior que a outra (a depender se o celular está “em pé” ou “deitado”. Note que há um problema de escala quando se resolve o “zoom in” e “zoom out”. É opcional ao grupo implementar a saída do programa utilizando CG (computação gráfica e telas gráficas). Sugiro, para os teste, criar figuras padrão, como cruzes e quadrado com pontos adjacentes, a fim de testar as funcionalidade do programa.




