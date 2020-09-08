# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 15:57:38 2020

@author: efrai
"""
#%%
import os
import pycosat
from time import time

#%%
def leerArchivoCNF(archivo):
    Lista=list()
    vfile= open(archivo, "r")
    for i in vfile:
        listaAux=i.split()
        if(listaAux[0].islower() == False):
            listaAux.pop()        
            Lista.append(list(map(int,listaAux)))
    return Lista

def clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")
#%%
clear()
l= list()
ttotal = 0
i = 0
reader=open('entrada',"r")
for cad in reader:
    nombre = cad.rstrip()
    i +=1
    t1 = time()
    l=leerArchivoCNF(nombre)
    t2 = time()
    print("\n\n" + nombre)
    print(pycosat.solve(l))
    t3 = time()
    print("Tiempo de lectura",t2-t1)
    print("tiempo resolución ",t3-t2)
    print("tiempo TOTAL ",t3-t1)
    ttotal += t3-t1

print ("tiempo medio ", ttotal/i)
