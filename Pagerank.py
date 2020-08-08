#***************************************************#
#**                                               **#
#**   Lucas Rodrigues Giacone   11831901          **#
#**   Exercicio Programa 1: PageRank              **#
#**   Professor: Saulo Rabello Maciel de Barros   **#
#**   Turma: 01                                   **#
#**                                               **#
#***************************************************#
from random import random,sample 
from json import loads as loadList
from math import sqrt
from time import time

def escalona(matriz,alfa):
    t = time()
    tamanho = len(matriz)
    autovetores = []

    #Adição de alfa
    for i in range(tamanho):
        for j in range(tamanho):
            matriz[i][j] = (1-alfa)*matriz[i][j] + alfa*(1/tamanho)

    #Subtração da identidade
    for i in range(tamanho):
        matriz[i][i] -= 1 

    #Escalonamento para baixo com valor mais alto da linha
    for i in range(tamanho):
        coluna = []
        for j in range(i,tamanho):
            coluna.append(matriz[j][i])

        if max(coluna) > -min(coluna):
            indiceColMax = coluna.index(max(coluna))
        else:
            indiceColMax = coluna.index(min(coluna))
        matriz[i][:] , matriz[indiceColMax+i][:] = matriz[indiceColMax+i][:] , matriz[i][:]

        for j in range(i+1,tamanho):
            RazaoLin = matriz[j][i]/matriz[i][i]
            for k in range(tamanho):
                matriz[j][k] -=  RazaoLin * matriz[i][k]
                #Zerar elementos menores que 2*10^(-05)
                matriz[j][k] *= (abs(matriz[j][k])>2e-05)

    #Normalização da linha para que todos os elementos da diagonal princiapal tenham valor 1
    for i in range(tamanho-1):
        if matriz[i][i] != 1:
            for j in reversed(range(tamanho)):
                matriz[i][j] /= matriz[i][i]

    #Escalonamento para baixo tirando a ultima coluna:
    for i in range(1,tamanho-1):
        for j in range(i):
            RazaoLin = matriz[j][i]/matriz[i][i]
            for k in range(i,tamanho):
                matriz[j][k] -= RazaoLin*matriz[i][k]

    #Pega os valores dos autovetores da ultima coluna da matriz
    for i in range(tamanho-1):
        autovetores.append(-1*matriz[i][-1])
    autovetores.append(1)

    #Normaliza oos valores
    soma = sum(autovetores)
    for i in range(tamanho):
        autovetores[i] /= soma

    print('Vetores normalizados, Metodo do escalonamento:')
    for i in autovetores:
            print(f'{i:.5f}')

    return time() - t


def calculaC (matriz):
    c = matriz[0][0]
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] < c:
                c = matriz[i][j]

    c = 1.0 - 2.0 * c

    return c


def iterativo(V,L,C,tamanho,alfa,c):
    t = time()
    Xnovo = [1/tamanho for i in range(tamanho)]
    Xvelho = [0 for i in range(tamanho)]

    #while |Xnovo-Xvelho| > 1e-5:
    while normaVetor(subtracaoVetor(Xnovo,Xvelho,tamanho)) > 1e-5:
        Xvelho = Xnovo[:]
        Y = [0 for i in range(tamanho)]
        for indice in range(len(V)):
            Y[L[indice]] += V[indice]*Xvelho[C[indice]]*(1-alfa)
        somaAlfa = sum(Xvelho)*alfa/tamanho
        for i in range(tamanho):
            Y[i] += somaAlfa
        normY = normaVetor(Y)
        Xnovo = [y/normY for y in Y]

    autovetores = Xnovo
    soma = sum(autovetores)
    for i in range(tamanho):
        autovetores[i] /= soma
    print('Vetores normalizados, Metodo iterativo:')
    for i in autovetores:
            print(f'{i:.5f}')
    return time() - t


def subtracaoVetor(vecA,vecB,tamanho):
    vec = []
    for i in range(tamanho):
        vec.append(vecA[i] - vecB[i])
    return vec


def normaVetor(vec):
    soma = 0
    for valor in vec:
        soma += valor**2
    return sqrt(soma)


def entradaGrafos():
    V = []
    L = []
    C = []
    while True:
        try:
            tamanho = int(input("Digite o numero de paginas:\n>"))
            if tamanho > 1:
                break
            else:
                print("O tamanho deve ser maior que 1")
        except ValueError:
            print("Entre com um numero inteiro para o numero de paginas")
    matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
    print("Como entrar com os grafos\n Ex: A pagina 1 referencia as paginas 2, 4 e 5 entrar 2, 4, 5.")
    for linha in range(tamanho):
        while True:
            colunas = input(f"Entre com a(s) referencia(s) da pagina {linha+1}\n>").split(",")
            if str(linha+1) in colunas:
                print("Grafo invalido, um site não pode apontar pra ele mesmo!")
            else:
                for i in range(len(colunas)):
                    if colunas[i] in colunas[i+1:]:
                        print("Um site não pode apontar duas vezes para o mesmo site")
                        break
                else:
                    valor = 1/len(colunas)
                    for elemento in colunas:
                        try:
                            if int(elemento) > tamanho:
                                print("Grafo invalido, um site não pode apontar pra uma pagina que não existe!")
                                break
                        except Exception:
                            print("Os valores devem ser inteiros!")
                            break
                        V.append(valor)
                        L.append(int(elemento)-1)
                        C.append(linha)
                        #criar a matriz normamente para o escalonamento
                        matriz[int(elemento)-1][linha] = valor
                    else:
                        break
            print("Tente novamente")
    else:
        alfa = float(input("Digite o valor de alfa:\n Ex: 15% = 0.15\n>"))
        tempo = escalona(matriz,alfa)
        print(f"Tempo de escalonamento foi:{tempo}")
        tempo = iterativo(V,L,C,tamanho,alfa)
        print(f"Tempo iterativo foi:{tempo}")


def entradaMatriz():
    matriz = loadList(input("Digite a matriz:\n Ex:\n[[ 0  , 0  , 1, 1/2],\n [ 1/3, 0  , 0, 0  ],\n [ 1/3, 1/2, 0, 1/2],\n [ 1/3, 1/2, 0, 0  ]]\n Seria:\n[[ 0, 0, 1, 0.5],[ 0.33333, 0, 0, 0],[ 0.33333, 0.5, 0, 0.5],[ 0.33333, 0.5, 0, 0]]\nOu seja, entre apenas com numeros decimais.\n>"))
    tamanho = len(matriz)
    V = []
    L = []
    C = []

    for i in range(tamanho):
        if matriz[i][i] != 0:
            print("Matriz invalida")
            return
        soma = 0
        for j in range(tamanho):
            soma += matriz[j][i]

        #Erro de float impede precisao por isso 0.95 envez de 1
        if soma < 0.95 :
            print(f"Erro na coluna {i+1}, Verifique a matriz ou tente usar mais casas decimais")
            return

        for j in range(tamanho):
            if matriz[i][j] !=0:
                V.append(matriz[i][j])
                L.append(i)
                C.append(j)

    else:
        alfa = float(input("Digite o valor de alfa:\n Ex: 15% = 0.15\n>"))
        tempo = escalona(matriz,alfa)
        print(f"Tempo de escalonamento foi:{tempo}")
        tempo = iterativo(V,L,C,tamanho,alfa)
        print(f"Tempo iterativo foi:{tempo}")


def geraMatriz():
    tamanho = int(input("Digite o tamanho da matriz \n>"))
    simetrica  = int(input("Você deseja que a matriz seja simetrica?\n1-Sim\n2-Não\n>"))%2
    matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
    V = []
    L = []
    C = []

    if not simetrica:
        for coluna in range(tamanho):
            numeroDeLigacoes = int(random()*(tamanho-1) % (tamanho-1) +1)
            possiveis = [*range(tamanho)]
            del(possiveis[coluna])
            ligacoes = sample(possiveis,numeroDeLigacoes)
            for linha in ligacoes:
                matriz[linha][coluna] = 1/numeroDeLigacoes

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

    for i in range(tamanho):
        for j in range(tamanho):
                if matriz[i][j] !=0:
                    V.append(matriz[i][j])
                    L.append(i)
                    C.append(j)

    imprime = int(input("Você deseja imprimir a matriz?\n1-Sim\n2-Não\n>"))%2
    if imprime:
        print("A matriz gerada foi:")
        print("[",end = "")
        for i in range(tamanho):
            print("[", end = "")
            for j in range(tamanho):
                if j == tamanho-1:
                    print(f" {matriz[i][j]:.03f}]", end = "")
                else:
                    print(f" {matriz[i][j]:.03f},", end = "")
            if i != tamanho-1:
                print(",\n ",end="")
            else:
                print("]")

    alfa = float(input("Digite o valor de alfa:\n Ex: 15% = 0.15\n>"))
    c = calculaC(matriz)
    tempo = escalona(matriz,alfa)
    print(f"Tempo de escalonamento foi:{tempo}")
    tempo = iterativo(V,L,C,tamanho,alfa,c)
    print(f"Tempo iterativo foi:{tempo}")
    return


if __name__ == "__main__":
    print("Entrar com: \n1-Mapa de grafos \n2-Matriz\n3-Gerar matriz aleatoria valida")
    while True:
        escolha = input('>')
        if escolha in ['1','2','3']:
            break
        else:
            print("Entre com uma opção valida!")
    if escolha == '1':
        entradaGrafos()
    if escolha == '2':
        entradaMatriz()
    if escolha == '3':
        geraMatriz()