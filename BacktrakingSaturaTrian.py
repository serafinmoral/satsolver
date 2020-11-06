# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os
import sys

import itertools
import networkx as nx    


from random import *
              
from GlobalClausulasSimple import *
from ProblemaTrian import *
from comunes import *

from queue import PriorityQueue

#from arbolpot import *
#
#x = 3434
#for i in range(60):
#    x = x*1.2
#    print(x)

from time import time



def leeArchivoGlobal(Archivo):
    reader=open(Archivo,"r")
    cadena = reader.readline()
    
    while cadena[0]=='c':
        cadena = reader.readline()
    
    cadena.strip()
    listaaux = cadena.split()
    print(listaaux)
    nvar = int(listaaux[2])
    nclaus = int(listaaux[3])
    print(nvar)
#    print(cadena)
    while cadena[0]=='c':
        cadena = reader.readline()
#    param = cadena.split()

    infor = globalClausulas()
    infor.nvar = nvar
    
    for cadena in reader:
#        print (cadena)
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= frozenset(listaux)
            infor.insertar(clausula)
            if(len(clausula)==1):
                h = set(clausula).pop()
                infor.unitprev.add(h)
                infor.unit.add(h)
            



#    print("paso a limpiar")
#    infor.limpiarec(0.0)
#    print("termino de limpiar")
    return infor  

  




    
 
def triangula(grafo):
    
    orden = []
    
    grafoc = grafo.copy()
    
    
    centra = nx.algorithms.centrality.betweenness_centrality(grafoc)

#    print(centra)
    ma = 0
    mv = 0
    i= 0
    while grafo.nodes:
        nnodo = min(grafo.nodes,key = lambda x : grafo.degree[x] - 0.01*centra[x])
        print(nnodo)
        orden.append(nnodo)
        
        veci = set(grafo[nnodo])
        if len(veci)> mv:
            mv = len(veci)
            ma = i
            
        i += 1
        grafo.remove_node(nnodo)
        for x in veci:
            for y in veci:
                if not x==y:
                    grafo.add_edge(x,y)
                    
                    
    

    # rem = orden[(ma+1):]
    
    # orden = orden[:(ma+1)]
    
    
    
    
    
    # orden2 = []
    # while rem:
    #         centra = nx.algorithms.centrality.betweenness_centrality(grafoc)
    #         pr = max(rem,key = centra.get)
    #         print(pr)
    #         orden2.append(pr)
    #         grafoc.remove_node(pr)
    #         rem.remove(pr)
    
    # orden2.reverse()
    # orden = orden + orden2    

    print(orden)
    return orden


    
    

       

    



    



    
def main(prob):
        
        info.unitprop()
        info.contradict = False
        info.solved = False

        print("entro en main")


        grafo = info.cgrafo()
        prob.orden = triangula(grafo)
        

        h = sorted(prob.orden)
        prob.posvar = dict()
        for i in h:
            prob.posvar[i] = prob.orden.index(i)
            

  
        
        listapot = prob.inicia2()     

        prob.borra4(listapot)

        # prob.inicia()
        
        print("salgo de inicio")
        # prob.borra()

        # config = prob.busca()
                     
        print(prob.inicial.solved, prob.inicial.contradict, config)
                        
        prob.inicial.compruebasol2(config)
        
        
        

       
#     

#
#reader=open(sys.argv[1],"r")
#
#writer=open(sys.argv[2],"w")

reader=open('entrada',"r")

writer=open('salida',"w")
ttotal = 0

while reader:
    linea = reader.readline().rstrip()  
    param = linea.split()
    nombre = param[0]
    N1 = int(param[1])
    N2 = int(param[2])
    N3 = int(param[3])
#    I = int(param[4])
    print(nombre)     
    t1 = time()
    info = leeArchivoGlobal(nombre)
    t2= time()

    prob = problemaTrian(info)
    prob.N1 = N1
    prob.N2 = N2
    prob.N3 = N3
#    prob.I = I

#info = leeArchivoSet('SAT_V144C560.cnf')

#print(info.listavar)

    

#print(problema.conjuntoclau.listavar)


    



#    problema.explora()

    t4 = time()
    

#problema.originalpotentials = problema.totaloriginal.extraePotentials(problema.ordenbo,problema.conjuntosvar)

    main(prob)
    
    t5 = time()



#info2 = leeArchivoGlobal('SAT_V1168C4675.cnf')
#info2 = leeArchivoGlobal('aes_32_1_keyfind_1.cnf')
#    info2 = leeArchivoGlobal(nombre)
#info2 = leeArchivoGlobal('SAT_V153C408.cnf')

#    info2.compruebasol(problema.configura)

    print("tiempo lectura ",t2-t1)
#    print("tiempo inicio ",t3-t2)
#    print("tiempo borrado ",t4-t3)
    print("tiempo busqueda ",t5-t4)

    print("tiempo TOTAL ",t5-t1)
    writer.write(linea+"\n")
    writer.write("tiempo TOTAL" + str(t5-t1)+"\n")
    ttotal += t5-t1

print ("tiempo medio ", ttotal/i)
writer.write("tiempo medio " + str(ttotal/i)+"\n")
writer.close()
reader.close()

