import matplotlib.pyplot
import json

with open(f'dadosIterativoSinglethread(Varias Matrizes x50).json', 'r') as dados:
    dadosIterativo = list(json.load(dados))
with open(f'dadosEscalonamentoSingleThreadComMultiplicadorInverso.json', 'r') as dados:
    dadosEscalonados = list(json.load(dados))
numero = []
tempo1 = []
tempo2 = []

for dadoIterativo,dadoEscalona in zip(dadosIterativo,dadosEscalonados):
    numero.append(int(dadoIterativo[0]))
    tempo1.append(float(dadoIterativo[1]))
    tempo2.append(float(dadoEscalona[1]))
    if int(dadoIterativo[0])>30:
        break
matplotlib.pyplot.ylabel('tempo (s)')
matplotlib.pyplot.xlabel('tamanho da matriz')
matplotlib.pyplot.title('Iterativo e Escalonamento N=30')
matplotlib.pyplot.grid(True)
matplotlib.pyplot.plot(numero,tempo1,label = 'Iterativo')
matplotlib.pyplot.plot(numero,tempo2,label = 'Escalonamento')
matplotlib.pyplot.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1,loc='upper left',prop={'size': 12})
matplotlib.pyplot.savefig("Grafico Iterativo e escalonamento 30.png",dpi=1000)
# matplotlib.pyplot.show()