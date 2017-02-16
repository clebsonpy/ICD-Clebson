import os
import extraindoZip
import calendar as ca
import pandas as pd
import numpy as np

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
						nome = linha.split(":")[1][1:-1]
						os.rename(txt, nome+".TXT")


def lerTxt(caminho, codigoArq):
    listaLinhas = []
    with open(os.path.join(caminho, codigoArq+".TXT"), encoding="Latin-1") as arquivo:
        for linha in arquivo.readlines():
            if linha[:3] != "// " and linha[:3] != "//-" and linha != "\n" and linha !="//\n":
                listaLinhas.append(linha.strip("//").split(";"))
    return listaLinhas


def trabaLinhas(caminho):
    colunas = extraindoZip.listaArq(caminho)[1]
    dadosV = pd.DataFrame(columns=colunas)
    for coluna in colunas:
        listaLinhas = lerTxt(caminho, coluna)
        dadosVazao = []
        count = 0
        for linha in listaLinhas:
            count += 1
            if count == 1:
                indiceCodigo = linha.index("EstacaoCodigo")
                inicioVa = linha.index("Vazao01")
                indiceData = linha.index("Data")
                indiceCons = linha.index("NivelConsistencia")
            elif count >= 2:
                #codigoEst = linha[indiceCodigo]
                data = pd.to_datetime(linha[indiceData], dayfirst=True)
                dias = ca.monthrange(data.year, data.month)[1]
                listaData = pd.date_range(data, periods=dias, freq="D")
                listaCons = [int(linha[indiceCons])]*dias
                indexMult = list(zip(*[listaData, listaCons]))
                index = pd.MultiIndex.from_tuples(indexMult, names=["Data", "Consistencia"])
                indiceVa = [i for i in range(inicioVa, inicioVa+dias)]
                listaVazao = [np.NaN if linha[i] == "" else float(linha[i].replace(",",".")) for i in indiceVa]
                dadosVazao.append(pd.Series(listaVazao, index=index))

        dadosV[coluna] = pd.concat(dadosVazao)

    return dadosV


if __name__ == "__main__":
    caminho = os.getcwd()
    dados = trabaLinhas(caminho)
    print(dados)









