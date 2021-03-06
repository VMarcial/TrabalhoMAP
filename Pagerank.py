#***************************************************#
#**                                               **#
#**   Lucas Rodrigues Giacone   11831901          **#
#**   Exercicio Programa 1: PageRank              **#
#**   Professor: Saulo Rabello Maciel de Barros   **#
#**   Turma: 01                                   **#
#**                                               **#
#***************************************************#
from random import random,sample 
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

    t = time() - t
    imprime = int(input("Você deseja imprimir o autovetor do metodo escalonamento?\n1-Sim\n2-Não\n>"))%2
    if imprime:
        print('Vetor normalizado, Metodo iterativo:')
        for i in autovetores:
            print(i)
        # ranking = []
        # for i in range(len(autovetores)):
        #     ranking.append([i, autovetores[i]])
        # ranking = sorted(ranking, key = lambda k: k[1], reverse=True)
        # print('Vetor normalizados, Metodo escalonamento:')
        # for i in ranking:
        #     print(i[0]+1, f'{i[1]:.5f}')

    return t,autovetores


def iterativo(V,L,C,tamanho,alfa):
    t = time()
    c = (1 - 2 * min(V))*(1-alfa)+ alfa/tamanho
    c = c/(1-c)
    Xnovo = [1/tamanho for i in range(tamanho)]
    Xvelho = [0 for i in range(tamanho)]

    #while |Xnovo-Xvelho| > 1e-5:
    while c*normaVetor(subtracaoVetor(Xnovo,Xvelho,tamanho)) > 1e-5:
        Xvelho = Xnovo[:]
        Y = [0 for i in range(tamanho)]
        for indice in range(len(V)):
            Y[L[indice]] += V[indice]*Xvelho[C[indice]] * (1-alfa)
        somaAlfa = sum(Xvelho)*alfa/tamanho
        for i in range(tamanho):
            Y[i] += somaAlfa
        normY = normaVetor(Y)
        Xnovo = [y/normY for y in Y]

    autovetores = Xnovo
    soma = sum(autovetores)
    for i in range(tamanho):
        autovetores[i] /= soma
    t = time() - t
    imprime = int(input("Você deseja imprimir o autovetor do metodo iterativo?\n1-Sim\n2-Não\n>"))%2
    if imprime:
        print('Vetor normalizado, Metodo iterativo:')
        for i in autovetores:
            print(i)
        # ranking = []
        # for i in range(len(autovetores)):
        #     ranking.append([i, autovetores[i]])
        # ranking = sorted(ranking, key = lambda k: k[1], reverse=True)
        # print('Vetor normalizados, Metodo iterativo:')
        # for i in ranking:
        #     print(i[0]+1, f'{i[1]:.5f}')
    return t,autovetores


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


def printRanking(vecA,vecB):
    ranking = []
    for i in range(len(vecA)):
        ranking.append([i, vecA[i], vecB[i]])
    ranking = sorted(ranking, key = lambda k: k[1], reverse=True)
    print('Rank das paginas:')
    print('Pagina\tValor Escalonado  Valor Iterativo')
    for i in ranking:
        print(f'  {i[0]+1}\t    {i[1]:.5f}\t      {i[2]:.5f}')


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
                        except ValueError:
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
        tempo,vecA = escalona(matriz,alfa)
        print(f"Tempo de escalonamento foi:{tempo}")
        tempo,vecB = iterativo(V,L,C,tamanho,alfa)
        print(f"Tempo iterativo foi:{tempo}")
    imprime = int(input('Deseja imprimir o ranking das paginas?\n1-Sim\n2-Não\n>'))%2
    if imprime:
        printRanking(vecA,vecB) 


def entradaMatriz():
    matriz = input("Digite a matriz:\n Ex:\n[[ 0  , 0  , 1, 1/2],\n [ 1/3, 0  , 0, 0  ],\n [ 1/3, 1/2, 0, 1/2],\n [ 1/3, 1/2, 0, 0  ]]\n Seria:\n[[ 0, 0, 1, 1/2],[ 1/3, 0, 0, 0],[ 1/3, 1/2, 0, 1/2],[ 1/3, 1/2, 0, 0]]\nOu\n[[ 0, 0, 1, 0.5],[ 0.33333, 0, 0, 0],[ 0.33333, 0.5, 0, 0.5],[ 0.33333, 0.5, 0, 0]]\nOu seja, entre apenas com numeros decimais ou frações.\n>")
    matriz = matriz.replace(" ", "")
    matriz = [I+']' for I in matriz.split(']')[:-2]]
    tamanho = len(matriz)
    matrizFinal = [[0 for i in range(tamanho)] for j in range(tamanho)]
    for i in range(len(matriz)):
        matriz[i] = matriz[i][2:-1]
    for indiceLin,linha in enumerate(matriz):
        linha = linha.split(",")
        for indiceCol,elemento in enumerate(linha):
            if "/" in elemento:
                elemento = elemento.split("/")
                matrizFinal[indiceLin][indiceCol] = int(elemento[0])/int(elemento[1])
            else:
                matrizFinal[indiceLin][indiceCol] = float(elemento)
    matriz = matrizFinal

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
        tempo,vecA = escalona(matriz,alfa)
        print(f"Tempo de escalonamento foi:{tempo}")
        tempo,vecB = iterativo(V,L,C,tamanho,alfa)
        print(f"Tempo iterativo foi:{tempo}")
    imprime = int(input('Deseja imprimir o ranking das paginas?\n1-Sim\n2-Não\n>'))%2
    if imprime:
        printRanking(vecA,vecB) 

def geraMatriz():
    caciqueTribo = int(input("Você deseja que a matriz seja cacique-tribo da tarefa 2?\n1-Sim\n2-Não\n>"))%2
    if caciqueTribo:
        ordem = int(input("Digite a ordem da cacique-tribo \n>"))
        t = time()
        tamanho = int(ordem*(ordem+3)/2)
        matriz = [([0]*tamanho) for i in range(tamanho)]
    else:
        tamanho = int(input("Digite o tamanho da matriz \n>"))
        t = time()
        matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
    # simetrica  = int(input("Você deseja que a matriz seja simetrica?\n1-Sim\n2-Não\n>"))%2
    V = []
    L = []
    C = []

    if not caciqueTribo:
        if tamanho > 10:
            for coluna in range(tamanho):
                # numeroDeLigacoes = int(random()*(tamanho-1) % (tamanho-1) +1)
                numeroDeLigacoes = int(random()*10 % 10 +1)
                possiveis = [*range(tamanho)]
                del(possiveis[coluna])
                ligacoes = sample(possiveis,numeroDeLigacoes)
                for linha in ligacoes:
                    matriz[linha][coluna] = 1/numeroDeLigacoes
        else:
            for coluna in range(tamanho):
                numeroDeLigacoes = int(random()*(tamanho-1) % (tamanho-1) +1)
                possiveis = [*range(tamanho)]
                del(possiveis[coluna])
                ligacoes = sample(possiveis,numeroDeLigacoes)
                for linha in ligacoes:
                    matriz[linha][coluna] = 1/numeroDeLigacoes

    else:
        cont = 0
        cacique = []
        for i in range(ordem):
            cacique.append(cont)
            for j in range(i+1):
                matriz[cont][cont+j+1]=1
                matriz[cont+j+1][cont]=1
                for k in range(j):
                    matriz[cont+k+1][cont+j+1]=1
                    matriz[cont+j+1][cont+k+1]=1
            cont+=i+2
        for i in cacique:
            for j in cacique:
                matriz[i][j]=int(i!=j)
                matriz[j][i]=int(i!=j)
        for i in range(tamanho):
            soma = 0
            for j in range (tamanho):
                soma += matriz[j][i]
            for j in range (tamanho):
                matriz[j][i]/=soma

    for i in range(tamanho):
        for j in range(tamanho):
                if matriz[i][j] !=0:
                    V.append(matriz[i][j])
                    L.append(i)
                    C.append(j)
    print(f"\nTempo para gerar a matriz foi:{time()-t}\n")
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
    tempo,vecA = escalona(matriz,alfa)
    print(f"Tempo de escalonamento foi:{tempo}")
    tempo,vecB = iterativo(V,L,C,tamanho,alfa)
    print(f"Tempo iterativo foi:{tempo}")
    imprime = int(input('Deseja imprimir o ranking das paginas?\n1-Sim\n2-Não\n>'))%2
    if imprime:
        printRanking(vecA,vecB) 
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