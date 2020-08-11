import PagerankClasses
import json
from multiprocessing import Pool

simetrica = False
multiplicadorIterativo = 15
multiplicadorEscalonamento = 0

def pegaTempo(lista):
    dados = []
    for numero in lista:
        P = PagerankClasses.pageRank(numero,simetrica,0.15,multiplicadorEscalonamento,multiplicadorIterativo)
        tempos = [0,0]
        tempos = P.geraMatriz()
        dados.append([numero]+tempos)
    return dados


if __name__ == "__main__":
    #Threads define quantos nucleos ele vai usar
    threads = 1

    p = Pool(threads)
    lista = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 57, 58, 60, 61, 62, 64, 66, 67, 69, 71, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 97, 99, 101, 104, 106, 109, 112, 115, 117, 120, 123, 126, 129, 132, 136, 139, 142, 146, 150, 153, 157, 161, 165, 169, 173, 177, 182, 186, 191, 195, 200, 205, 210, 215, 220, 226, 231, 237, 243, 249, 255, 261, 268, 274, 281, 288, 295, 302, 309, 317, 325, 333, 341, 349, 358, 367, 376, 385, 394, 404, 414, 424, 434, 445, 456, 467, 479, 490, 502, 515, 527, 540, 554, 567, 581, 595, 610, 625, 640, 656, 672, 688, 705, 723, 740, 759, 777, 796, 816, 836, 856, 877, 899, 921, 943, 967, 990, 1015, 1039, 1065, 1091, 1118, 1145, 1173, 1202, 1232, 1262, 1293, 1325, 1357, 1390, 1424, 1459, 1495, 1532, 1570, 1608, 1647, 1688, 1729, 1772, 1815, 1860, 1905, 1952, 2000]
    # lista = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 57, 58, 60, 61, 62, 64, 66, 67, 69, 71, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 97, 99, 101, 104, 106, 109, 112, 115, 117, 120, 123, 126, 129, 132, 136, 139, 142, 146, 150, 153, 157, 161, 165, 169, 173, 177, 182, 186, 191, 195, 200]
    listaDividida = [list(lista[i::threads]) for i in range(threads)]

    tempos = []
    temposSeparados = p.map(pegaTempo, listaDividida)
    for i in temposSeparados:
        tempos = tempos + i
    tempos = sorted(tempos)

    dadosEscalona = []
    dadosIterativo  = []
    for i in tempos:
        dadosEscalona.append([i[0],i[1]])
        dadosIterativo.append([i[0],i[2]])

    with open(f'dadosEscalona.json', 'w') as outfile:
        json.dump(dadosEscalona, outfile)
    with open(f'dadosIterativo.json', 'w') as outfile:
        json.dump(dadosIterativo, outfile)