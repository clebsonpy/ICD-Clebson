#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:46:00 2017

@author: clebson
"""

import pandas as pd
import arquivoTxt as arq
import os
import calendar as cal

#plotly
#Cufflinks

def preparaGrupoSerie(dados, nPosto, mesHidro):
    grupos = dados[nPosto].groupby(pd.Grouper(freq='A-%s' % mesHidro[1]))
    keysG = [i[0] for i in grupos]
    frameGrafico = pd.DataFrame()
    for key, dado in grupos:
        if key.year != keysG[0].year and key.year != keysG[-1].year:
            aux = dado.values
            index = dado.index
            indexMult = list(zip(*[index.month, index.day]))
            indexN = pd.MultiIndex.from_tuples(indexMult, names=["Mes", "Dia"])
            serie = pd.Series(aux, index=indexN, name=key.year)
            frameAux = pd.DataFrame(serie)
            frameGrafico = arq.combinaDateFrame(frameGrafico, frameAux)
    frameGrafico.drop_duplicates(keep='last', inplace=True)
    return grupos, frameGrafico

def periodoSemFalhas(gantt, nPosto):
    aux = []
    listaInicio = []
    listaFim = []
    for i in gantt[nPosto].index:
        if gantt[nPosto].loc[i] == 0:
            aux.append(i)
        else:
            if len(aux) > 2:
                listaInicio.append(aux[0])
                listaFim.append(aux[-1])
            aux = []

    listaInicio.append(aux[0])
    listaFim.append(aux[-1])
    dic = {'Inicio': listaInicio, 'Fim': listaFim}
    return pd.DataFrame(dic)

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
    mesHidro = grupoMesMedia.idxmin()
    mesHidroAbr = cal.month_abbr[mesHidro].upper()
    return mesHidro, mesHidroAbr


def separaDadosConsisBruto(dados, tipo, lev):
    dadosSeparado = dados.iloc[dados.index.isin([tipo], level=lev)]
    dadosSeparado.reset_index(level=lev, drop=True, inplace=True)
    return dadosSeparado


def falhas(dadosVazao):
    dadosVazao.sort_index(inplace=True)
    nFalhas = dadosVazao.isnull().sum()
    gantt = dadosVazao.isnull().groupby(pd.Grouper(freq = 'M')).sum()
    for i in gantt.index:
        if gantt.loc[i].isnull().all():
            gantt.set_value(index = i, col = gantt.axes[1], value = i.day)
    
    return nFalhas, gantt.to_period()

if __name__ == "__main__":
    caminho = os.getcwd()
    dadosVazao = separaDadosConsisBruto(arq.trabaLinhas(caminho), tipo=2,lev=1)
    falhas, gantt = falhas(dadosVazao)
    periodoSemFalhas = periodoSemFalhas(gantt, nPosto = '49330000')
    #mesHidro = mesInicioAnoHidrologico(dadosVazao, '49330000')
    #grupos, fg = preparaGrupoSerie(dadosVazao, '49330000')
    #grupos = grupoAnoHidro(dadosVazao, nPosto='49330000', mesHidro = mesHidro, grafico=True)
    #maxAnual = maximaAnual(grupos, nPosto='49330000')

