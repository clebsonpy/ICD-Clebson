#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:46:00 2017

@author: clebson
"""

import pandas
import arquivoTxt as arq

def manipDados(dadosVazao):
    dadosVazao.sort_index(level='Data', inplace=True)
    nFalhas = dadosVazao.isnull().sum()
    s
    return nFalhas
        
if __name__ == "__main__":
    caminho = caminho = os.getcwd()
    dadosVazao = arq.trabaLinhas(arq.lerTxt(caminho, "4933000"))
    print(manipDados(dadosVazao))