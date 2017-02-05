import os
import collections
import calendar as ca
import pandas as pd
import numpy as np
from datetime import datetime as dt

def listaTxt(caminho):
	listaDir = os.listdir(caminho)
	listaArquivo = []
	for arquivo in listaDir:
		if os.path.isfile(os.path.join(caminho,arquivo)) and arquivo[-3:] == 'TXT':
				listaArquivo.append(arquivo)
	return listaArquivo


def renomearTxt(caminho, listaTxt):
	for txt in listaTxt:
		if txt[:-4] == "VAZOES":
			with open(os.path.join(caminho, txt), encoding="Latin-1") as arquivo:
				for linha in arquivo.readlines():
					if linha.split(":")[0] == "//   Código da Estação":
						nome = linha.split(":")[1][1:-2]
						os.rename(txt, nome+".TXT")


def lerTxt(caminho, codigoArq):
	listaLinhas = []
	with open(os.path.join(caminho, codigoArq+".TXT"), encoding="Latin-1") as arquivo:
		for linha in arquivo.readlines():
			if linha != "\n" and linha[0] != "/":
				listaLinhas.append(linha.split(";"))
	return listaLinhas


def trabaLinhas(listaLinhas):
    dadosVazao = []
    for linha in listaLinhas:
        count = 0
        listaVazao = []
        for i in linha:
            count += 1
            if count == 3:
                dia, mes, ano = (int(x) for x in i.split("/"))
                dias = ca.monthrange(ano, mes)[1]
                inicio = dt(ano, mes, dia)
                fim = dt(ano, mes, dias)
                listaDatas = pd.date_range(inicio, fim)
                listaCons = [int(linha[1])]*dias
                indexMult = list(zip(*[listaDatas,listaCons]))
                index = pd.MultiIndex.from_tuples(indexMult, names=['Data', 'Consistência'])
            elif count >= 17 and count < 17+dias:
                if i != "":
                    listaVazao.append(float(i.replace(",",".")))
                else:
                    listaVazao.append(np.NaN)
        dadosVazao.append(pd.Series(listaVazao, index=index))
        
    return pd.concat(dadosVazao)

if __name__ == "__main__":
    caminho = os.getcwd()
    s = (trabaLinhas(lerTxt(caminho, "4933000")))