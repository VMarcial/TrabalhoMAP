import random
def geramatriz(tamanho):
    matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
    for i in range(tamanho):
        numerodeligacoes = random.randrange(tamanho-1)+1
        Ligacoes = []
        contador = numerodeligacoes
        while contador > 0:
            numLigação = random.randrange(tamanho)+1
            comparador = (numLigação not in Ligacoes) and (numLigação != (i+1))
            Ligacoes.append( (comparador)*numLigação )
            contador -= comparador
        while 0 in Ligacoes:
            Ligacoes.remove(0)
        for k in Ligacoes:
            matriz[k-1][i] += 1/numerodeligacoes
    return matriz



tamanho = int(input("Digite o tamanho da matriz:"))
matriz = geramatriz(tamanho)
m = open("matriz.txt", "w")
m.write("[")
for i in range(tamanho):
    m.write("[")
    for j in range(tamanho):
        if j != tamanho-1: m.write(f" {matriz[i][j]:.2f},")
        else: m.write(f" {matriz[i][j]:.2f}")
    if i != tamanho-1: m.write("],")
    else: m.write("]")
m.write("]")
m.close
print("gerado")
