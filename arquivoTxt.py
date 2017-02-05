import os
import collections

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
    dicVazoes = collections.OrderedDict()
    for linha in listaLinhas:
        count = 0
        vazoes = []
        for i in linha:
            count += 1
            if count == 3:
                mes = int(i.split("/")[1])
                ano = int(i.split("/")[2]) 
                dias = diasDoMes(mes, ano)
            if count >= 17 and count < 17+dias:
                if i != '':
                    vazoes.append(float(i.replace(',','.')))
                else:
                    vazoes.append(-9999.9)
        
        dicVazoes[linha[2], linha[1]] = vazoes
    return dicVazoes


def diasDoMes(mes, ano):
	"""
	:param mes:
	:param ano:
	:return: Quantidades de dias do mês
	"""
	if mes <= 7:
		if mes == 2:
			if (ano % 4) == 0 and (ano % 100) != 0 or (ano % 400) == 0:
				dias = 29
			else:
				dias = 28
		else:
			if (mes%2) == 0:
				dias = 30
			else:
				dias = 31
	else:
		if (mes%2) == 0:
			dias = 31
		else:
			dias = 30
	return dias
