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

import random

file = open("pts_qt.txt", 'w')

n = 8
for _ in range(n):
    linha = f"({random.randint(1,135)},{random.randint(1,45)})"
    file.write(linha + "\n")
    
n = 3
for i in range(n):
    linha = f'({60},{10+3*i})'
    file.write(linha + "\n")
    
n = 3
for i in range(n):
    linha = f'({69},{10+3*i})'
    file.write(linha + "\n")

#cria a cruz para testar o programa
file.write('(78,16)' + '\n')
file.write('(51,16)' + '\n')
file.write('(78,19)' + '\n')
file.write('(51,19)' + '\n')
file.write('(60,19)' + '\n')
file.write('(60,22)' + '\n')
file.write('(69,22)' + '\n')
file.write('(69,19)' + '\n')

file.close()
