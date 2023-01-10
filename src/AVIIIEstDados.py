'''UFRJ - Universidade Federal do Rio de Janeiro
MAE015 - Tóp. Especiais em Engenharia de dados A: Estrutura de dados
Autores:
Nome: Rhuan Justo
DRE: 118043398

Nome: Davi Richards
DRE: 119022078

Nome: Sebastião Rodrigo
DRE: 117099621

Nome: Yuri Ferreira Melo
DRE: 120081378'''

import matplotlib.pyplot as plt
import numpy as np
import os

class Ponto(): #Cria a classe ponto dadas as suas coordenadas x,y

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        "Permite representar o objeto ponto como uma string (x,y)"
        return 'P({:.2f}, {:.2f})'.format(self.x, self.y)


class Rect(): #Cria a classe retângulo

    def __init__(self, x0, y0, w, h):
        """(x0,y0) é o ponto inicial, w é a largura e h é a altura.
        (Se quisermos dar o ponto superior esquerdo e o inferior direito, o (x0,y0) é o ponto superior esquerdo,
        w é a norma da diferença entre o x final e o inicial, o h é a diferença entre o y final e inicial com sinal)"""
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self.coord_0 = Ponto(x0,y0)
        self.coord_1 = Ponto(x0+w,y0+h)
        self.coord_centro = Ponto(x0+w/2, y0+h/2)


  
    def contem(self,pt):
        """Essa função define se um dado ponto está contido no retângulo"""
        if self.coord_0.x <= pt.x <= self.coord_1.x and self.coord_0.y <= pt.y <= self.coord_1.y:
            return True
        else:
            return False

    def printar(self, ax, c='k', lw=1, **kwargs):
        """Desenha o retângulo no matplotlib"""
        x1, y1 = self.x0, self.coord_1.y
        x2, y2 = self.coord_1.x, self.y0
        ax.plot([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1], c=c, lw=lw, **kwargs)

    def intersect(self, other):
        """Define se um dado retângulo insercta outro"""
        return not (other.x0 > self.coord_1.x or
                other.coord_1.x < self.x0 or
                other.y0 > self.coord_1.y or
                other.coord_1.y < self.y0)
    
class Quad_Tree(): #Cria a classe quad-tree
    def __init__(self, rect_inicial, prof = 0, max_points = 1):
        """Rect_inicial: o retângulo principal, os limites da quad-tree
        prof: a profundidade da quad-tree, 0 é a raiz, a cada nível aumenta a profundidade em 1.
        max_points: o número limite de pontos por nó"""
        self.rect_inicial = rect_inicial
        self.prof = prof
        self.max_points = max_points
        self.pontos = []
        self.dividido = False #determina se a quad-tree possui filhos ou não

    def divide(self):
        """Essa função divide uma quad-tree em seus 4 filhos: noroeste, nordeste,sudoeste e sudeste"""
        centro_x, centro_y = self.rect_inicial.coord_centro.x, self.rect_inicial.coord_centro.y
        w,h = self.rect_inicial.w, self.rect_inicial.h

        self.NO = Quad_Tree(Rect(centro_x-w/2,centro_y,w/2,h/2), self.prof + 1, self.max_points)
        self.NE = Quad_Tree(Rect(centro_x,centro_y,w/2,h/2), self.prof + 1, self.max_points)
        self.SO = Quad_Tree(Rect(centro_x-w/2,centro_y-h/2,w/2,h/2), self.prof + 1, self.max_points)
        self.SE = Quad_Tree(Rect(centro_x,centro_y-h/2,w/2,h/2), self.prof + 1, self.max_points)

        self.dividido = True #a quad-tree principal passa a ser reconhecida como um nó "pai"

    def consulta(self, pt):
        """Dado um ponto, define se o ponto está na quad-tree ou não"""
        if pt in self.pontos: #verificamos diretamente nos pontos da quad-tree inicial
            return True
        elif self.dividido == False:#se a quad-tree não possuir filhos e falhou no teste anterior, o ponto não está.
            return False
        else: #se a quad-tree possuir filhos, recursivamente teste nos filhos
            if pt.x <= self.rect_inicial.coord_centro.x and pt.y <= self.rect_inicial.coord_centro.y:
                return self.SO.consulta(pt)
            elif pt.x <= self.rect_inicial.coord_centro.x and pt.y > self.rect_inicial.coord_centro.y:
                return self.NO.consulta(pt)
            elif pt.x > self.rect_inicial.coord_centro.x and pt.y <= self.rect_inicial.coord_centro.y:
                return self.SE.consulta(pt)
            elif pt.x > self.rect_inicial.coord_centro.x and pt.y > self.rect_inicial.coord_centro.y:
                return self.NE.consulta(pt)

    def consulta_janela(self, pt_sup_esq, pt_inf_dir, pts_encontrados):
        """Dado o ponto superior esquerdo e o inferior direito de uma janela (retângulo),
        retorna os pontos da quad-tree que estão dentro dessa janela"""
        x0 = pt_sup_esq.x
        y0 = pt_inf_dir.y
        
        w = np.abs(pt_inf_dir.x - pt_sup_esq.x)
        h = np.abs(pt_sup_esq.y - pt_inf_dir.y)
        
        rect = Rect(x0,y0,w,h)
    
        if self.rect_inicial.intersect(rect) == False:
            # Se a janela desejada não intersectar os limites da quad-tree, não faz sentido procurar pelos pontos
            return False
    
        for pt in self.pontos: #para cada ponto direto da quad-tree, testa se a janela contém o ponto
            if rect.contem(pt):
                pts_encontrados.append(pt)


        if self.dividido: #se a quad-tree possuir filhos, recursivamente procura os pontos na janela
            pt_0 = Ponto(rect.x0,rect.y0+h)
            pt_1 = Ponto(rect.x0+w,rect.y0)
            self.NO.consulta_janela(pt_0,pt_1, pts_encontrados)
            self.NE.consulta_janela(pt_0,pt_1, pts_encontrados)
            self.SO.consulta_janela(pt_0,pt_1, pts_encontrados)
            self.SE.consulta_janela(pt_0,pt_1, pts_encontrados)
        return pts_encontrados

    def consulta_cardeal(self, pt, dire, pts_encontrados):
        """Dado um ponto de referência (x,y) e uma direção cardeal (N,S,L,O), retorna os
        pontos interiores do semiplano formado de (x,y) na direção desejada."""
        #dependendo da direção, tome o semiplano formado
        if dire == "N":
            rect = Rect(self.rect_inicial.x0, pt.y, self.rect_inicial.w, self.rect_inicial.coord_1.y - pt.y)
        elif dire == "S":
            rect = Rect(self.rect_inicial.x0, self.rect_inicial.y0, self.rect_inicial.w, pt.y)
        elif dire == "L":
            rect = Rect(pt.x, self.rect_inicial.y0, self.rect_inicial.coord_1.x, self.rect_inicial.coord_1.y)
        elif dire == "O":
            rect = Rect(self.rect_inicial.x0, self.rect_inicial.y0, pt.x, self.rect_inicial.coord_1.y)

        #consulte se o ponto está no semiplano
        pt_0 = Ponto(rect.x0,rect.y0+rect.h)
        pt_1 = Ponto(rect.x0+rect.w,rect.y0)
        return self.consulta_janela(pt_0, pt_1, pts_encontrados)

    def insere(self, pt):
        """Dado um ponto, insere esse ponto na quad-tree, criando os nós de maior profundidade, se necessário"""
        if self.rect_inicial.contem(pt) == False:
            return False
    
        if len(self.pontos) < self.max_points:
            # Se o nó ainda possui espaço para acrescentar um ponto, acrescente.
            self.pontos.append(pt)
            return True
      
        if self.dividido == False: #Se o nó está preenchido e ainda não possui filhos, divida o nó
            self.divide()

        return (self.NO.insere(pt) or #Recursivamente tente inserir nas sub-árvores formadas.
                self.NE.insere(pt) or
                self.SO.insere(pt) or
                self.SE.insere(pt))


    def printar(self, ax):
        """Printa a quad-tree"""
        self.rect_inicial.printar(ax)
        if self.dividido: #se possuir filhos, printa todos os filhos
            self.NO.printar(ax)
            self.NE.printar(ax)
            self.SO.printar(ax)
            self.SE.printar(ax)

#Vamos abrir a base de dados
f = open("pts_qt.txt")

#45 linhas e 100 colunas
m = 45
n = 135

#criando o retângulo inicial da quad-tree e a própria quad-tree
r1 = Rect(0,0,n,m)
q1 = Quad_Tree(r1)
pts = []

#inserindo os pontos do BD na quad-tree
for s in f.readlines():
    aux = s.split(",", 1)

    x = int(aux[0][1:])
    y = int(aux[1][:-2])
        
    pt = Ponto(x,y)
    pts.append(pt)
    q1.insere(pt)
    
#printando a quad-tree
fig, ax = plt.subplots(1,1, figsize = (12,8))


q1.printar(ax)

#printando os pontos inseridos
ax.scatter([p.x for p in pts], [p.y for p in pts],
           facecolors='none', edgecolors='r', s=22)


def print_tela(qt,pt_sup_esq,pt_inf_dir,m,n):
    """Essa função printa no console todos os pontos encontrados
na janela dada pelo ponto superior esquerdo e o ponto inferior direito."""
    linha = "-"*n
    tela = ''
    for _ in range(m):
        tela += linha + "\n"
    
    strings = tela.split()

    found = qt.consulta_janela(pt_sup_esq,pt_inf_dir,[])

    for p in found:
        x,y = p.x, p.y
    
        strings[m-y] = strings[m-y][:x-1] + 'x' + strings[m-y][x:]
    
    tela = '\n'.join(strings)
    print(tela)


def main():
    """Função main para permitir a interação com o usuário pelo console"""
    f = open("pts_qt.txt")

    m = 45
    n = 135


    r1 = Rect(0,0,n,m)
    q1 = Quad_Tree(r1)
    pts = []
    
    for s in f.readlines():
        aux = s.split(",", 1)

        x = int(aux[0][1:])
        y = int(aux[1][:-2])

        pt = Ponto(x,y)
        pts.append(pt)
        q1.insere(pt)
        
    
    print("Bem-vindo ao guia de localização de Postos de Combustíveis!")
    res = input("Você gostaria de pesquisar a localização de um posto? (s/n) ")
    
    while res == 's': 
        os.system('cls')
        coords_0 = input("Digite as coordenadas do canto superior esquerdo da janela de visão: 'x1,y1'")
        coords_1 = input("Digite as coordenadas do canto inferior direito da janela de visão: 'x2,y2'")

        aux_0 = coords_0.split(',')
        aux_1 = coords_1.split(',')
    
        x0 = int(aux_0[0])
        y0 = int(aux_0[1])
    
        x1 = int(aux_1[0])
        y1 = int(aux_1[1])
    
        pt_sup_esq = Ponto(x0,y0)
        pt_inf_dir = Ponto(x1,y1)
    
        print_tela(q1,pt_sup_esq,pt_inf_dir,m,n)
        res = input("Você gostaria de pesquisar a localização de um posto? (s/n) ")

if __name__ == '__main__':
    main()

plt.show()
  
