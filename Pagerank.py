from random import random,sample 
from json import loads as loadList
from math import sqrt
from time import time
def escalona(matriz):
    t = time()
    tamanho = len(matriz)
    autovetores = []
    alfa = 0.15

    for i in matriz:
        print(i)
    print()

    #Adição de alfa
    for i in range(tamanho):
        for j in range(tamanho):
            
            matriz[i][j] = (1-alfa)*matriz[i][j] + alfa*(1/tamanho)



    #Subtração da identidade
    for i in range(tamanho):
        matriz[i][i] -= 1 

    for i in matriz:
        print(i)
    print()



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
    print('Autovetores:')
    for i in range(tamanho-1):
        autovetores.append(-1*matriz[i][-1])
    autovetores.append(1)
    for i in autovetores:
            print(f'{i:.3f}')

    #Normaliza oos valores
    soma = sum(autovetores)
    for i in range(tamanho):
        autovetores[i] /= soma
    print('Normalizados:')
    for i in autovetores:
            print(f'{i:.3f}')

    return time() - t


def iterativo(V,L,C,tamanho):
    t = time()
    Xnovo = [1/tamanho for i in range(tamanho)]
    Xvelho = [0 for i in range(tamanho)]

    
    #while |Xnovo-Xvelho| > 1e-5:
    while normaVetor(subtracaoVetor(Xnovo,Xvelho)) > 1e-5:
        Xvelho = Xnovo[:]
        Y = [0 for i in range(tamanho)]
        for indice in range(len(V)):
            Y[L[indice]] += V[indice]*Xvelho[C[indice]]
        normY = normaVetor(Y)
        Xnovo = [Y[i]/normY for i in range(tamanho)]


    autovetores = Xnovo
    soma = sum(autovetores)
    for i in range(tamanho):
        autovetores[i] /= soma
    print('Normalizados:')
    for i in autovetores:
            print(f'{i:.3f}')
    return time() - t



def subtracaoVetor(vecA,vecB):
    vec = []
    for i in range(len(vecA)):
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
    tamanho = int(input("Digite o numero de paginas:\n>"))
    matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
    print("Como entrar com os grafos\n Ex: A pagina 1 referencia as paginas 2, 4 e 5 entrar 2, 4, 5.")
    for linha in range(tamanho):
        colunas = input(f"Entre com a(s) referencia(s) da pagina {linha+1}\n>").split(",")
        valor = 1/len(colunas)

        for elemento in colunas:
            V.append(valor)
            L.append(int(elemento)-1)
            C.append(linha)
            #criar a matriz normamente para o escalonamento
            matriz[int(elemento)-1][linha] = valor


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
    else:
        tempo = escalona(matriz)
        print(f"Tempo de escalonamento foi:{tempo}")
        #Falta implementar o alfa no iterativo
        tempo = iterativo(V,L,C,tamanho)
        print(f"Tempo iterativo foi:{tempo}")

def entradaMatriz():
    matriz = loadList(input("Digite a matriz:\n Ex:\n[[ 0  , 0  , 1, 1/2],\n [ 1/3, 0  , 0, 0  ],\n [ 1/3, 1/2, 0, 1/2],\n [ 1/3, 1/2, 0, 0  ]]\n Seria:\n[[ 0, 0, 1, 0.5],[ 0.33333, 0, 0, 0],[ 0.33333, 0.5, 0, 0.5],[ 0.33333, 0.5, 0, 0]]\nOu seja, entre apenas com numeros decimais.\n>"))
    tamanho = len(matriz)

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
    else:
        return escalona(matriz)


def geraMatriz():
    tamanho = int(input("Digite o tamanho da matriz \n>"))
    simetrica  = int(input("Você deseja que a matriz seja simetrica?\n1-Sim\n2-Não\n>"))%2
    matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
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
    return escalona(matriz)


if __name__ == "__main__":
    print("Entrar com: \n1-Mapa de grafos \n2-Matriz\n3-Gerar matriz aleatoria valida")
    escolha = int(input('>'))
    if escolha == 1:
        entradaGrafos()
    if escolha == 2:
        entradaMatriz()
    if escolha == 3:
        geraMatriz()