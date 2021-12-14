
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
""" 
import networkx as nx    
from ProblemaTrianArbol import *
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
    while cadena[0]=='c':
        cadena = reader.readline()

    infor = simpleClausulas()
    for cadena in reader:
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= set(listaux)
            infor.listaclausOriginal.append(clausula.copy())
            infor.insertar(clausula)
    
    return infor  
    
 
def triangula(grafo):
    orden = []
    clusters = []
    maximal = []
    child = []
    borr = []
    grafoc = grafo.copy()
    centra = nx.algorithms.centrality.betweenness_centrality(grafoc)
    ma = 0
    mv = 0
    child = [-1]*len(grafo.nodes)
    
    i= 0
    total = set()
    while grafo.nodes:
        nnodo = min(grafo.nodes,key = lambda x : grafo.degree[x] - 0.01*centra[x])
        print(nnodo)
        orden.append(nnodo)
        veci = set(grafo[nnodo])
        clus = veci.union({nnodo})
        clusters.append(clus)
        borr.append(clus-total)
        total.update(clus)
        print(clus)

        maxim = True
        for j in range(i-1,-1,-1):
            print(j, clusters[j])
            if clus == (clusters[j]-{orden[j]}):
                child[j] = i
                maxim = False
                print("no maximal")
                break
        if maxim:
            maximal.append(i)


        


        print( i, clus) 
        i += 1
        grafo.remove_node(nnodo)
        for x in veci:
            for y in veci:
                if not x==y:
                    grafo.add_edge(x,y)

    # print(orden)
    return (orden,clusters,borr,maximal,child)
    
def main(prob):
        # info.contradict = False
        # info.solved = False
        prob.inicial.contradict = False
        prob.inicial.solved = False         
        print("entro en main")
        
        # grafo = info.cgrafo()
        grafo = prob.inicial.cgrafo()
        (prob.orden,prob.clusters,prob.borr,prob.maximal,prob.child)  = triangula(grafo)
        h = sorted(prob.orden)
        prob.posvar = dict()
        for i in h:
            prob.posvar[i] = prob.orden.index(i)

        prob.inicia0()      
        prob.borraapro(M=3,T=2)

        prob.reinicia()
        prob.borraapro(M=3,T=3)
        prob.reinicia()


        prob.borra()
        if not prob.inicial.contradict:
            prob.findsol()

        print("salgo de inicio")
       
#     
# ********** Control de Aplicación ****************
#

reader=open('entrada',"r")
writer=open('salida',"w")
ttotal = 0

while reader:
    linea = reader.readline().rstrip()  
    param = linea.split()
    nombre = param[0]
    N1 = int(param[1])
    print(nombre)     
    t1 = time()
    info = leeArchivoGlobal(nombre)
    t2= time()
    prob = problemaTrianArbol(info,N1)
    t4 = time()

    main(prob)
    # print("Conjunto solución: ",prob.sol)
    if prob.inicial.contradict==False:
        prob.compruebaSol()
    else:
        print("Problema no satisfactible")
    t5 = time()
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

