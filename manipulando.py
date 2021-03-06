#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:46:00 2017

@author: clebson
"""
import timeit
import pandas as pd
import lerArquivo as arq
import os
import calendar as cal
import plotly.tools as tls
import plotly.figure_factory as FF
import plotly.offline as py
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

def dataFrameGantt(aux):
    df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Description', 'IndexCol'])
    cont = 0
    for i in aux:
        color = 0
        n = 1
        psf = aux[i]
        for j in psf.index:
            df.set_value(index = cont, col = 'Task', value = i)
            df.set_value(index = cont, col = 'Description', value = i + ' - %s' % j)
            df.set_value(index = cont, col = 'Col', value = color)
            df.set_value(index = cont, col = 'Start', value = psf['Inicio'].loc[j])
            df.set_value(index = cont, col = 'Finish', value = psf['Fim'].loc[j])
            cont += 1
            color += (100*n)
            n *= -1

    return df

def periodoSemFalhas(ganttBool, nPosto):
    aux = []
    listaInicio = []
    listaFim = []
    for i in ganttBool[nPosto].index:
        if ~ganttBool[nPosto].loc[i]:
            aux.append(i)
        elif len(aux) > 2 and ganttBool[nPosto].loc[i]:
            listaInicio.append(aux[0])
            listaFim.append(aux[-1])
            aux = []

    if len(aux) > 0:
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
    ganttSoma = dadosVazao.isnull().groupby(pd.Grouper(freq = 'M')).sum()
    ganttBool = dadosVazao.isnull()
    #nomeIndex = getattr(dadosVazao.index, 'names', getattr(dadosVazao.index, 'name', 'index'))[0]
    #ganttBool = ganttBool.reset_index().drop_duplicates(subset=nomeIndex, keep='last').set_index(nomeIndex)
    for i in ganttSoma.index:
        if ganttSoma.loc[i].isnull().all():
            ganttSoma.set_value(index = i, col = ganttSoma.axes[1], value = i.day)

    return nFalhas, ganttBool, ganttSoma.to_period()

def plotlyCredenciais(username, apiKey):
    tls.set_credentials_file(username=username, api_key= apiKey)
    tls.set_config_file(world_readable=True, sharing='public')

def plotGantt(dfGantt, filename):
    fig = FF.create_gantt(dfGantt, colors = ['#000000', '#858585'], group_tasks=True, bar_width=0.475)
    py.plot(fig, filename=filename)

if __name__ == "__main__":
    ini = timeit.default_timer()
    caminho = os.getcwd()
    nomeArquivo = arq.listaArq(caminho, 'xls')
    #dadosVazao = separaDadosConsisBruto(arq.trabaLinhas(caminho), tipo=2,lev=1)
    dadosVazao = arq.lerXlsx(caminho, nomeArquivo, 'Total')
    falhas, ganttBool, ganttSoma = falhas(dadosVazao)
    
    #aux = {}
    #listaText = arq.listaArq(caminho, 'xls')
    #for i in dadosVazao:
    #    aux[i] = periodoSemFalhas(ganttBool, nPosto = i)

    #dfGantt = dataFrameGantt(aux)
    #plotlyCredenciais(username='clebsonpy', apiKey='Dtk2N7biK0BjJZHEJ5uf')
    #plotGantt(dfGantt, filename='ganttChart')
    mesHidro = mesInicioAnoHidrologico(dadosVazao, '178')
    #grupos, fg = preparaGrupoSerie(dadosVazao, '49330000', mesHidro)
    #maxAnual = maximaAnual(grupos, nPosto='49330000')0
    fim = timeit.default_timer()
    print('Duração: %s' % (fim-ini))

