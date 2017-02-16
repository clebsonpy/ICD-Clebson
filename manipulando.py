#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:46:00 2017

@author: clebson
"""

import pandas as pd
import arquivoTxt as arq
import os


def manipDados(dadosVazao):
    dadosVazao.sort_index(level='Data', inplace=True)
    nFalhas = dadosVazao.isnull().sum()
    dadosConsistido = dadosVazao.iloc[dadosVazao.index.isin([1], level=1)]
    dadosConsistido.reset_index(level=1, drop=True, inplace=True)
    dadosBruto = dadosVazao.iloc[dadosVazao.index.isin([2], level=1)]
    dadosBruto.reset_index(level=1, drop=True, inplace=True)
    ganttConsistido = dadosConsistido.isnull().resample('M').sum()
    ganttBruto = dadosBruto.isnull().resample('M').sum()

    return nFalhas, ganttConsistido, ganttBruto

if __name__ == "__main__":
    caminho = caminho = os.getcwd()
    dadosVazao = arq.trabaLinhas(caminho)
    mani = manipDados(dadosVazao)