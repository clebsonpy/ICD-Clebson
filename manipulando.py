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
    gant = dados.iloc[dados.index.isin([1], level=1)].isnull().resample('M', level='Data').sum()
    gant2 = dados.iloc[dados.index.isin([2], level=1)].isnull().resample('M', level='Data').sum()
    
    return nFalhas
        
if __name__ == "__main__":
    caminho = caminho = os.getcwd()
    dadosVazao = arq.trabaLinhas(arq.lerTxt(caminho, "4933000"))
    print(manipDados(dadosVazao))