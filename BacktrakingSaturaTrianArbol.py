
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
    borr = []
    child = []
    grafoc = grafo.copy()
    centra = nx.algorithms.centrality.betweenness_centrality(grafoc)
    ma = 0
    mv = 0
    n = len(grafo.nodes)
    parent = [-1]*n
    for i in range(n):
        child.append(set())
    
    i= 0
    total = set()
    while grafo.nodes:

        nnodo = min(grafo.nodes,key = lambda x : grafo.degree[x] - 0.01*centra[x])
        print(nnodo)
        orden.append(nnodo)
        veci = set(grafo[nnodo])
        clus = veci.union({nnodo})
        clusters.append(clus)

        maxim = True
        for j in range(i-1,-1,-1):
            print(j, clusters[j])
            if clus <= (clusters[j]):
                # child[j] = i
                # parent[i] = j
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

    total = clusters[n-1].copy()
    for i  in range(n-2,-1,-1):
        clus = clusters[i]
        for j in range(i+1,n,1):
            if clus.intersection(total) == clus.intersection(clusters[j]):
                parent[i] = j
                child[j].add(i)
                break
        total.update(clus)
            

    # print(orden)
    return (orden,clusters,borr,maximal,child,parent)
    
def main(prob):
        # info.contradict = False
        # info.solved = False
        prob.inicial.contradict = False
        prob.inicial.solved = False         
        print("entro en main")
        
        # grafo = info.cgrafo()
        grafo = prob.inicial.cgrafo()
        (prob.orden,prob.clusters,prob.borr,prob.maximal,prob.child,prob.parent)  = triangula(grafo)
        h = sorted(prob.orden)
        prob.posvar = dict()
        for i in h:
            prob.posvar[i] = prob.orden.index(i)

        prob.inicia0()                          
        prob.borraapro(M=4,T=3)
        prob.reinicia()
        prob.borraaproi(M=4,T=3)
        

        

        



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

