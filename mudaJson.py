import json
jsonEscalona = []
jsonIterativo = []
with open(f'dadosC.json', 'r') as dados:
    dado = json.load(dados)
    for linha in dado:
        jsonEscalona.append([linha['field2'],linha['field3']])
        jsonIterativo.append([linha['field2'],linha['field7']])
    with open(f'dadosCEscalonado.json', 'w') as outfile:
        json.dump(jsonEscalona, outfile)
    with open(f'dadosCIterativo.json', 'w') as outfile:
        json.dump(jsonIterativo, outfile)