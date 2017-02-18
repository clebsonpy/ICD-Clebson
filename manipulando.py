#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:46:00 2017

@author: clebson
"""

import pandas as pd
import arquivoTxt as arq
import os

def mesInicioAnoHidrologico(dados):
    grupoMesAno = dados.groupby(pd.Grouper(freq='M')).mean().to_period()
    indexMult = list(zip(*[grupoMesAno.index.month, grupoMesAno.index.year]))
    indexN = pd.MultiIndex.from_tuples(indexMult, names=["Mes", "Ano"])
    grupoMesAno.set_index(indexN, inplace=True)
    grupoMes = grupoMesAno.groupby(level='Mes').mean()
    return grupoMes.idxmin()


def separaDadosConsisBruto(dados, tipo, lev):
    dadosSeparado = dados.iloc[dados.index.isin([tipo], level=lev)]
    dadosSeparado.reset_index(level=lev, drop=True, inplace=True)
    return dadosSeparado


def manipDados(dadosVazao):
    dadosVazao.sort_index(level='Data', inplace=True)
    nFalhas = dadosVazao.isnull().sum()
    dadosConsistido = separaDadosConsisBruto(dadosVazao, tipo = 1, lev = 1)
    dadosBruto = separaDadosConsisBruto(dadosVazao, tipo = 2, lev = 1)
    ganttConsistido = dadosConsistido.isnull().groupby(pd.Grouper(freq = 'M')).sum().to_period()
    ganttBruto = dadosBruto.isnull().groupby(pd.Grouper(freq = 'M')).sum()
    #grupoBruto = dadosBruto.groupby(pd.Grouper(freq = 'A-AUG'))
    return nFalhas, ganttConsistido, ganttBruto

if __name__ == "__main__":
    caminho = caminho = os.getcwd()
    dadosVazao = arq.trabaLinhas(caminho)
    mes = mesInicioAnoHidrologico(separaDadosConsisBruto(dadosVazao, tipo=2,lev=1))
    print(mes)