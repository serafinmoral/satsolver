# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 12:02:58 2021

@author: efraín
"""
from time import time
from BTSA_SimpleClausulas import *
from BTSA_ProblemaTrianArbol import *
import networkx as nx   

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
    infor = simpleClausulas()
    
    for cadena in reader:
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= set(listaux)
            infor.insertar(clausula)
    return infor  


def main(prob):
        info.contradict = False
        info.solved = False
        print("entro en main")
        
        grafo = info.cgrafo()
        (prob.orden,prob.clusters)  = triangula(grafo)
        
        h = sorted(prob.orden)
        prob.posvar = dict()
        for i in h:
            prob.posvar[i] = prob.orden.index(i)
        
        prob.inicia0()     
        prob.borra()
        
        print("salgo de inicio")

def triangula(grafo):
    orden = []
    clusters = []
    
    grafoc = grafo.copy()
    centra = nx.algorithms.centrality.betweenness_centrality(grafoc)
    i= 0
    while grafo.nodes:
        nnodo = min(grafo.nodes,key = lambda x : grafo.degree[x] - 0.01*centra[x])
        # print(nnodo)
        orden.append(nnodo)
        veci = set(grafo[nnodo])
        clus = veci.union({nnodo})
        clusters.append(clus)
        # print( i, clus) 
        i += 1
        grafo.remove_node(nnodo)
        for x in veci:
            for y in veci:
                if not x==y:
                    grafo.add_edge(x,y)
    return (orden,clusters)

# **************
# ****MAIN******

reader=open('entrada',"r")
writer=open('salida',"w")
ttotal = 0

for linea in reader: 
    param = linea.rstrip().split()
    nombre = param[0]
    N1 = int(param[1])
    print(nombre)     
    t1 = time()
    info = leeArchivoGlobal(nombre)
    # print(info.listaclaus)
    # print(info.listavar)
    # print(info.unit)
    t2= time()
    # info.imprime()
    prob = problemaTrianArbol(info,N1)
    t4 = time()
    
    main(prob)
    t5 = time()
    print("tiempo lectura ",t2-t1)
    print("tiempo busqueda ",t5-t4)
    print("tiempo TOTAL ",t5-t1)
    writer.write(linea+"\n")
    writer.write("tiempo TOTAL" + str(t5-t1)+"\n")
    ttotal += t5-t1
# print ("tiempo medio ", ttotal/i)
# writer.write("tiempo medio " + str(ttotal/i)+"\n")
writer.close()
reader.close()
