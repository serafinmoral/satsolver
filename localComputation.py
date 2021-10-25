#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:15:59 2019

@author: smc
"""


class localComputation:
    def __init__(self):
        self.var = 0
        self.ordenbo = []
        self.listacliques = []
        self.listapadres = []
        self.listahijos = []
        self.mensajes = dict()
    
        
    def inicia(self,x):
         (self.ordenbo,varinorder,self.listacliques,self.listapadres,self.listahijos) = x.computeCliques()
         conjuntopotentials = x.extraePotentials(self.ordenbo,self.listacliques)
         
        
        
        