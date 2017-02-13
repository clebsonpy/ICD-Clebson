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
    dadosBruto = dadosVazao.iloc[dadosVazao.index.isin([2], level=1)]
    ganttConsistido = dadosConsistido.isnull().resample('AUG-M', level='Data').sum()
    ganttBruto = dadosBruto.isnull().resample('AUG-M', level='Data').sum()

    return nFalhas, ganttConsistido, ganttBruto

if __name__ == "__main__":
    caminho = caminho = os.getcwd()
    dadosVazao = arq.trabaLinhas(caminho)
    print(manipDados(dadosVazao))