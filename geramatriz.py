import random
def geramatriz(tamanho,simetrica):
    matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
    if not simetrica:
        for i in range(tamanho):
            numerodeligacoes = random.randrange(tamanho-1)+1
            possiveis = [*range(tamanho)]
            del(possiveis[i])
            Ligacoes = random.sample(possiveis,numerodeligacoes)
            for k in Ligacoes:
                matriz[k][i] += 1/numerodeligacoes
        return matriz
    else:
        for i in range(tamanho-1):
            numerodeligacoes = random.randrange(tamanho-1-i)+1
            possiveis = [*range(i+1,tamanho)]
            Ligacoes = random.sample(possiveis,numerodeligacoes)
            for k in Ligacoes:
                matriz[k][i] += 1
                matriz[i][k] += 1
        for i in range(tamanho):
            divisor = 0
            for j in range(tamanho):
                divisor += matriz[j][i]
            for j in range(tamanho):
                matriz[j][i] /= divisor
        return matriz


def salva(matriz):
    arq = open("matriz.txt", "w")
    arq.write("[")
    for i in range(tamanho):
        arq.write("[")
        for j in range(tamanho):
            if j != tamanho-1: arq.write(f" {matriz[i][j]:.3f},")
            else: arq.write(f" {matriz[i][j]:.3f}")
        if i != tamanho-1: arq.write("],\n ")
        else: arq.write("]")
    arq.write("]")
    arq.close


tamanho = int(input("Digite o tamanho da matriz:"))
simetrica = int(input("Simetrica(1/0):"))
matriz = geramatriz(tamanho,simetrica)
print("gerado")
salva(matriz)
print("salvo")