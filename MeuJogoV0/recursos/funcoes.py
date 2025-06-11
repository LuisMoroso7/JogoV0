import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    try:
        banco = open("log.data", "r")
        banco.close()
    except:
        print("Banco de Dados Inexistente. Criando...")
        with open("log.data", "w") as banco:
            banco.write("{}")
    
def escreverDados(nome, pontos):
    try:
        with open("log.data", "r") as banco:
            dados = banco.read()
            dadosDict = json.loads(dados) if dados.strip() else {}
    except (FileNotFoundError, json.JSONDecodeError):
        dadosDict = {}

    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)

    with open("log.data", "w") as banco:
        banco.write(json.dumps(dadosDict))
    
    # END - inserindo no arquivo