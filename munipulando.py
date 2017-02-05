#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:46:00 2017

@author: clebson
"""

import pandas
import arquivoTxt as arq

def nfalhas(dicVazoes):
    falhas = {}
    for i in dicVazoes:
        
            
        print(dicVazoes[i])
        

caminho = caminho = os.getcwd()
dicVazoes = arq.trabaLinhas(arq.lerTxt(caminho, "4933000"))

nfalhas(dicVazoes)