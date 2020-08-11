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

class pageRank():
    def __init__(self,tamanho,simetrica,alfa,vezesEscalonado = 0,vezesIterativo = 0,display = False):
        self.tamanho = tamanho
        self.simetrica = simetrica
        self.alfa = alfa
        self.display = display
        self.vezesEscalonado = vezesEscalonado
        self.vezesIterativo =  vezesIterativo


    def escalona(self):
        t = time()
        alfa = self.alfa
        print(len(self.matriz))
        for i in range(self.vezesEscalonado):
            matriz = self.matriz[:]
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
        if self.vezesEscalonado:
            return (time() - t)/self.vezesEscalonado
        else:
            return 0


    def iterativo(self):
        alfa = self.alfa
        tamanho = self.tamanho
        t = time()
        print(tamanho)
        for i in range(self.vezesIterativo):
            V = self.V[:]
            L = self.L[:]
            C = self.C[:]

            c = (1 - 2 * min(V))*(1-alfa)+ alfa/tamanho
            c = c/(1-c)
            Xnovo = [1/tamanho for i in range(tamanho)]
            Xvelho = [0 for i in range(tamanho)]

            #while |Xnovo-Xvelho| > 1e-5:
            while c*self.normaVetor(self.subtracaoVetor(Xnovo,Xvelho)) > 1e-5:
                Xvelho = Xnovo[:]
                Y = [0 for i in range(tamanho)]
                for indice in range(len(V)):
                    Y[L[indice]] += V[indice]*Xvelho[C[indice]] * (1-alfa)
                somaAlfa = sum(Xvelho)*alfa/tamanho
                for i in range(tamanho):
                    Y[i] += somaAlfa
                normY = self.normaVetor(Y)
                Xnovo = [y/normY for y in Y]

            autovetores = Xnovo
            soma = sum(autovetores)
            for i in range(tamanho):
                autovetores[i] /= soma

        if self.vezesIterativo:
            return (time() - t)/self.vezesIterativo
        else:
            return 0


    def subtracaoVetor(self,vecA,vecB):
        vec = []
        for i in range(self.tamanho):
            vec.append(vecA[i] - vecB[i])
        return vec


    def normaVetor(self,vec):
        soma = 0
        for valor in vec:
            soma += valor**2
        return sqrt(soma)


    def geraMatriz(self):
        tamanho = self.tamanho

        matriz = [[0 for i in range(tamanho)] for j in range(tamanho)]
        V = []
        L = []
        C = []

        if not self.simetrica:
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
            for coluna in range(tamanho-1):
                # numeroDeLigacoes = int(random()*(tamanho-1-coluna) % (tamanho-1-coluna) +1)
                numeroDeLigacoes = (coluna > 11)*int(random()*10 % 10 +1) + (coluna<11)*int(random()*(tamanho-1-coluna) % (tamanho-1-coluna) +1)
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
        
        if self.display:
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

        self.matriz = matriz
        self.V = V
        self.L = L
        self.C = C

        tempo = [0,0]
        tempo[0] = self.escalona()
        tempo[1] = self.iterativo()
        return tempo
