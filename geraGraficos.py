import matplotlib.pyplot
import json

with open(f'dadosIterativo.json', 'r') as dados:
    dadosIterativo = list(json.load(dados))
with open(f'dadosEscalona.json', 'r') as dados:
    dadosEscalonados = list(json.load(dados))
numero = []
tempo1 = []
tempo2 = []
for dadoIterativo,dadoEscalona in zip(dadosIterativo,dadosEscalonados):
    numero.append(dadoIterativo[0])
    tempo1.append(dadoIterativo[1])
    tempo2.append(dadoEscalona[1])
matplotlib.pyplot.plot(numero,tempo1)
matplotlib.pyplot.plot(numero,tempo2)
matplotlib.pyplot.show()