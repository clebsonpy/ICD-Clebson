#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:46:00 2017

@author: clebson
"""

import pandas as pd
import arquivoTxt as arq
import os
import calendar




#def grupoAnoHidro(dados, nPosto = None, grafico = False):
#    mesHidro = mesInicioAnoHidrologico(dadosVazao, nPosto)
#    dias = calendar.monthrange(2000, mesHidro-1)[1]
#    mes = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
#    if nPosto != None:
#        grupo = dados[nPosto].groupby(pd.Grouper(freq='A-%s' % mes[mesHidro]))
#    else:
#        grupo = dados.groupby(pd.Grouper(freq='A-%s' % mes[mesHidro]))
#
#    if grafico and nPosto != None:
#        frame = pd.DataFrame(index=pd.date_range(pd.to_datetime('1999/%s/1' % mesHidro), pd.to_datetime('2000/%s/%s' % (mesHidro-1, dias))))
#        for dado in grupo:
#            index = []
#            for data in dado[1].index:
#                if data.month > (mesHidro-1):
#                    ano = 1999
#                else:
#                    ano = 2000
#                index.append(pd.to_datetime('%s/%s/%s' % (ano, data.month, data.day)))
#
#            aux = dado[1].rename(dado[0].year)
#            frameAux = pd.DataFrame(aux)
#            frameAux.set_index(pd.Index(index), inplace=True)
#            frame = arq.combinaDateFrame(frame, frameAux)
#        frame.plot(legend=False)
#        return grupo, frame
#
#    return grupo

def preparaSerieGrafico(dados, nPosto):
    mesHidro = mesInicioAnoHidrologico(dadosVazao, nPosto)
    mes = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
    grupos = dados[nPosto].groupby(pd.Grouper(freq='A-%s' % mes[mesHidro]))
    keysG = [i[0] for i in grupos] 
    frame = pd.DataFrame()
    for key, dado in grupos:
        if key.year != keysG[0].year and key.year != keysG[-1].year:
            aux = dado.values
            index = dado.index
            
            indexMult = list(zip(*[index.month, index.day]))
            indexN = pd.MultiIndex.from_tuples(indexMult, names=["Mes", "Dia"])
            serie = pd.Series(aux, index=indexN, name=key.year)
            frameAux = pd.DataFrame(serie)
            #frameAux.set_index(pd.Index(indexN), inplace=True)
            frame = arq.combinaDateFrame(frame, frameAux)

    return frame
        
        
def maximaAnual(grupos, nPosto):
    vazaoMax = []
    dataMax = []
    for data, dado in grupos:
        vazaoMax.append(dado.max())
        dataMax.append(dado.idxmax())
    maxAnualSeie =  pd.Series(vazaoMax, dataMax, name=nPosto)
    maxAnual = pd.DataFrame(maxAnualSeie)

    return maxAnual


def mesInicioAnoHidrologico(dados, nPosto):
    grupoMesAno = dados.groupby(pd.Grouper(freq='M')).mean().to_period()
    indexMult = list(zip(*[grupoMesAno.index.month, grupoMesAno.index.year]))
    indexN = pd.MultiIndex.from_tuples(indexMult, names=["Mes", "Ano"])
    grupoMesAno.set_index(indexN, inplace=True)
    grupoMesMedia = grupoMesAno[nPosto].groupby(level='Mes').mean()
    return grupoMesMedia.idxmin()


def separaDadosConsisBruto(dados, tipo, lev):
    dadosSeparado = dados.iloc[dados.index.isin([tipo], level=lev)]
    dadosSeparado.reset_index(level=lev, drop=True, inplace=True)
    return dadosSeparado


def falhas(dadosVazao):
    dadosVazao.sort_index(inplace=True)
    nFalhas = dadosVazao.isnull().sum()
    gantt = dadosVazao.isnull().groupby(pd.Grouper(freq = 'M')).sum().to_period()

    return nFalhas, gantt

if __name__ == "__main__":
    caminho = caminho = os.getcwd()
    dadosVazao = separaDadosConsisBruto(arq.trabaLinhas(caminho), tipo=1,lev=1)
    gantt = falhas(dadosVazao)
    df = preparaSerieGrafico(dadosVazao, '49330000')
    #grupos = grupoAnoHidro(dadosVazao, mes, nPosto='49330000',grafico=True)
    #maxAnual = maximaAnual(grupos, nPosto='49330000')

