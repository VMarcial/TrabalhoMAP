from random import random,sample 
from time import time

def geramatriz(tamanho,simetrica):
    matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
    if not simetrica:
        for coluna in range(tamanho):
            numeroDeLigacoes = int(random()*(tamanho-1) % (tamanho-1) +1)
            possiveis = [*range(tamanho)]
            del(possiveis[coluna])
            ligacoes = sample(possiveis,numeroDeLigacoes)
            for linha in ligacoes:
                matriz[linha][coluna] = 1/numeroDeLigacoes
        return matriz
    else:
        for coluna in range(tamanho-1):
            numeroDeLigacoes = int(random()*(tamanho-1-coluna) % (tamanho-1-coluna) +1)
            possiveis = [*range(coluna+1,tamanho)]
            ligacoes = sample(possiveis,numeroDeLigacoes)
            for linha in ligacoes:
                matriz[linha][coluna] = 1
                matriz[coluna][linha] = 1
        for coluna in range(tamanho):
            divisor = 0
            for linha in range(tamanho):
                divisor += matriz[linha][coluna]
            for linha in range(tamanho):
                matriz[linha][coluna] /= divisor
        return matriz


def salva(matriz,tamanho):
    arq = open("matriz.txt", "w")
    arq.write("[")
    for i in range(tamanho):
        arq.write("[")
        for j in range(tamanho):
            if j != tamanho-1: arq.write(f" {matriz[i][j]:.{precisao}f},")
            else: arq.write(f" {matriz[i][j]:.{precisao}f}")
        if i != tamanho-1: arq.write("],\n ")
        else: arq.write("]")
    arq.write("]")
    arq.close


tamanho = int(input("Digite o tamanho da matriz:"))
simetrica = int(input("Simetrica(1/0):"))
precisao = int(input("Casas depois da virgula:"))
t = time()
matriz = geramatriz(tamanho,simetrica)
print(f"gerado , tempo = {time() - t}")
t = time()
salva(matriz,tamanho)
print(f"salvo , tempo = {time() - t}")