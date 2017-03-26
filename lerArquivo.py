import os
import calendar as ca
import pandas as pd
import numpy as np

def listaArq(caminho, tipo):
    listaDir = os.listdir(caminho)
    listaArquivo = []
    for arquivo in listaDir:
        if os.path.isfile(os.path.join(caminho, arquivo)):
            nome, ext = arquivo.split('.')
            if ext == tipo:
                listaArquivo.append(nome)
    return listaArquivo


def renomearTxt(caminho, listaTxt):
    for txt in listaTxt:
        if txt == "VAZOES":
            with open(os.path.join(caminho, txt+'.TXT'), encoding="Latin-1") as arquivo:
                for linha in arquivo.readlines():
                    if linha.split(":")[0] == "//   Código da Estação":
                        nome = linha.split(":")[1][1:-1]
                        print(nome)
                        os.rename(txt+'.TXT', nome+".TXT")


def lerTxt(caminho, nomeArquivo):
    listaLinhas = []
    with open(os.path.join(caminho, nomeArquivo+'.TXT'), encoding="Latin-1") as arquivo:
        for linha in arquivo.readlines():
            if linha[:3] != "// " and linha[:3] != "//-" and linha != "\n" and linha !="//\n":
                listaLinhas.append(linha.strip("//").split(";"))
    return listaLinhas


def multIndex(data, dias, consistencia):
    if data.day == 1:
        dias = dias
    else:
        dias = dias - data.day

    listaData = pd.date_range(data, periods=dias, freq="D")
    listaCons = [int(consistencia)]*dias
    indexMult = list(zip(*[listaData, listaCons]))
    return pd.MultiIndex.from_tuples(indexMult, names=["Data", "Consistencia"])


def combinaDateFrame(dataframe1, dataframe2):
    if len(dataframe1) > 0:
        dataframe1 = dataframe1.combine_first(dataframe2)
    else:
        dataframe1 = dataframe2
    return dataframe1

def trabaLinhas(caminho):
    nomeArquivos = listaArq(caminho, 'TXT')
    dadosV = pd.DataFrame()
    for nomeArquivo in nomeArquivos:
        print('Arquivo: ', nomeArquivo)
        listaLinhas = lerTxt(caminho, nomeArquivo)
        dadosVazao = []
        count = 0
        for linha in listaLinhas:
            count += 1
            if count == 1:
                #indiceCodigo = linha.index("EstacaoCodigo")
                inicioVa = linha.index("Vazao01")
                indiceData = linha.index("Data")
                indiceCons = linha.index("NivelConsistencia")
            elif count >= 2:
                #codigoEst = linha[indiceCodigo]
                data = pd.to_datetime(linha[indiceData], dayfirst=True)
                dias = ca.monthrange(data.year, data.month)[1]
                consistencia = linha[indiceCons]
                index = multIndex(data, dias, consistencia)
                indiceVa = [i for i in range(inicioVa, inicioVa+dias)]
                listaVazao = [np.NaN if linha[i] == "" else float(linha[i].replace(",",".")) for i in indiceVa]
                dadosVazao.append(pd.Series(listaVazao, index=index, name=nomeArquivo))

        dados = pd.DataFrame(pd.concat(dadosVazao))
        dadosV = combinaDateFrame(dadosV, dados)

    return dadosV

def lerXlsx(caminho, nomeArquivo, planilha):
    arq = os.path.join(caminho, nomeArquivo[0]+'.xls')
    dadosV = pd.read_excel(arq, shettname=planilha, header=0, skiprows=5, index_col=0)
    dadosV.drop(np.NaN, inplace=True)
    aux = []
    dic = {'jan':'1', 'fev':'2', 'mar':'3', 'abr':'4', 'mai':'5', 'jun':'6', 'jul':'7', 'ago':'8', 'set':'9', 'out':'10', 'nov':'11', 'dez':'12'}
    for i in dadosV.index:
        aux.append(i.replace(i[-8:-5], dic[i[-8:-5]]))
    
    dadosV.index = pd.to_datetime(aux, dayfirst=True)
    codiColuna = [i.split(' ')[-1][1:-1] for i in dadosV.axes[1]]
    dadosV.columns = codiColuna
    
    return dadosV

if __name__ == "__main__":
    caminho = os.getcwd()
    nomeArquivo = listaArq(caminho, 'xls')
    dados = lerXlsx(caminho, nomeArquivo, 'Total')
#    dadox = pd.DataFrame.add(dados)
#    print(dados)