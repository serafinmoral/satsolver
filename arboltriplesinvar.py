# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import math
from SimpleClausulas import * 

def calculavar(lista):
    cuenta = dict()
    for cl in lista:
        vars = map(abs,cl)
        for v in vars:
            if v in cuenta:
                cuenta[v]  += 1
            else:
                cuenta[v] = 1
    return max(cuenta, key=(lambda key: cuenta[key]))


def split(lista,var):
    lista1 = []
    lista2 = []
    for cl in lista:
        if var in cl:
            cl.discard(var)
            lista1.append(cl)
        elif -var in cl:
            cl.discard(-var)
            lista2.append(cl)
        else:
            lista1.append(cl)
            lista2.append(cl.copy())
    return (lista1,lista2)


def split3(lista,var):
    lista1 = []
    lista2 = []
    lista3 = []
    for cl in lista:
        if var in cl:
            cl.discard(var)
            lista1.append(cl)
        elif -var in cl:
            cl.discard(-var)
            lista2.append(cl)
        else:
            lista3.append(cl)
    return (lista1,lista2,lista3)

def computefromLista(x,N):

        result = arboltriple()
        
        if len(x)<= N:
            valor = simpleClausulas()
            for cl in x:
                valor.insertar(cl)

            result.asignaval(valor)
        else:
            var = calculavar(x)    
            (l0,l1) = split(x,var)
            h0 = computefromLista(l0,N)
            h1 = computefromLista(l1,N)
            h2 = arboltriple()

            result.asignavarhijos(var,h0,h1,h2)
        
        return result

def compute3fromLista(x,N):

        result = arboltriple()
        
        if len(x)<= N:
            valor = simpleClausulas()
            for cl in x:
                valor.insertar(cl)

            result.asignaval(valor)
        else:
            var = calculavar(x)    
            (l0,l1,l2) = split3(x,var)
            h0 = computefromLista(l0,N)
            h1 = computefromLista(l1,N)
            h2 = computefromLista(l2,N)

            result.asignavarhijos(var,h0,h1,h2)
        
        return result


class arboltriple:
    def __init__(self):
        self.var = 0
        self.value = simpleClausulas()
        self.hijos = [None,None,None]
        self.contradict = False
    
    def anula(self):
        self.var = 0
        x = simpleClausulas()
        x.insertar(set())
        self.value = x
        self.hijos = [None,None,None]

    def asignavar(self,p):
        self.var = p
        self.value = None

        self.hijos[0] = arboltriple()
        self.hijos[1] = arboltriple()
        self.hijos[2] = arboltriple()

    def asignavarhijos(self,p,h0,h1,h2):
        self.var = p
        self.value = None

        self.hijos[0] = h0
        self.hijos[1] = h1
        self.hijos[2] = h2


        
    def asignaval(self,x):
        self.var = 0
        self.value = x
        self.hijos = [None,None,None]
        
        
    def asignahijo(self,t,i):
        self.hijos[i] = t
        
    def imprime(self):
        if (self.var == 0):
            print("valor " , self.value.listaclaus)
        else:
            print ("variable ",self.var)
            print("hijo 1")
            self.hijos[0].imprime()
            print("hijo 2")
            self.hijos[1].imprime()
            print("hijo 3")
            self.hijos[2].imprime()
        
        
    
        
    def noesta(self,cl):
        if self.var==0:
            return self.value.noesta(cl)
        else:
            v = self.var
            if v in cl:
                return self.hijos[0].noesta(cl - {v}) or self.hijos[2].noesta(cl)
            elif -v in cl:
                return self.hijos[1].noesta(cl - {-v}) or self.hijos[2].noesta(cl)
            else:
                return self.hijos[2].noesta(cl)


    def insertaclau(self,cl,tres = False):
        if self.var == 0:
            self.value.insertar(cl)
        else:
            v = self.var
            if v in cl:
                self.hijos[0].insertaclau(self,cl.discard(v),tres)
            elif -v in cl:
                self.hijos[1].insertaclau(self,cl.discard(-v),tres)
            elif tres:
                self.hijos[2].insertaclau(self,cl,tres)
            else:
                self.hijos[0].insertaclau(self,cl,tres)
                self.hijos[1].insertaclau(self,cl.copy(),tres)

                
        
 
            
    
        
 
            
    
                
            
        
        
        
            
        