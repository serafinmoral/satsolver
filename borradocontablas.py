
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
""" 
import networkx as nx    
from SimpleClausulas import *
from ProblemaTrianFactor import *
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
            infor.insertar(clausula, test=False)
    
    return infor  
    
def triangulap(pot):
    orden = []
    clusters = []
    borr = []
    child = []
    posvar = dict()
    total = set()
    dvar = dict()

    for p in pot.listap:
        con = set(p.listavar)
        print(con)
        total.update(con)
        for v in con:
            if v in dvar:
                dvar[v].append(con)
            else:
                dvar[v] = [con]
    n = len(total.union(pot.unit))
    
    
    parent = [-1]*(n+1)
    for i in range(n+1):
        child.append(set())
    
    i= 0
    units = pot.unit.copy()




    while units:

        nnodo = abs(units.pop())
        orden.append(nnodo)
        clus = {nnodo}
        clusters.append(clus)
        posvar[nnodo] = i
        print( i, clus) 

        i+=1

   
    
    
    value = dict()
    totvar = dict()


    for x in dvar:
        totvar[x] = set()
        for h in dvar[x]:
            totvar[x].update(h)
        value[x] = 2**(len(totvar[x])-1) - sum([2**len(y) for y in dvar[x]])
        
        

    while total:
        nnodo = min(value, key = value.get )
        orden.append(nnodo)

        clus = set()
        for x in dvar[nnodo]:
            clus.update(x)
        clusters.append(clus)
        posvar[nnodo] = i
        print( i, clus) 

        i+=1
        clustersin = clus-{nnodo}

        for y in clustersin:
            dvar[y] = list(filter( lambda h: nnodo not in h  ,dvar[y] ))
            dvar[y].append(clustersin)
            totvar[y] = set()
            for h in dvar[y]:
                totvar[y].update(h)
            value[y] = 2**(len(totvar[y])-1) - sum([2**len(z) for z in dvar[y]])
        


        del value[nnodo]
        del dvar[nnodo]
        del totvar[nnodo]
        total.discard(nnodo)


    clusters.append(set())


    for i in range(n):
            con = clusters[i]
            cons = con - {orden[i]}
            if not cons:
                parent[i] = n
                child[n].add(i)
            else:
                pos = min(map(lambda h: posvar[h], cons))
                parent[i] = pos
                child[pos].add(i)



        
            

        
       

            

    # print(orden)
    return (orden,clusters,borr,posvar,child,parent) 


def triangula(grafo):
    orden = []
    clusters = []
    
    borr = []
    child = []
    posvar = dict()
    grafoc = grafo.copy()
    centra = nx.algorithms.centrality.betweenness_centrality(grafoc)
    ma = 0
    mv = 0
    n = len(grafo.nodes)
    parent = [-1]*(n+1)
    for i in range(n+1):
        child.append(set())
    
    i= 0
    total = set()
    while grafo.nodes:

        nnodo = min(grafo.nodes,key = lambda x : grafo.degree[x] + 2*centra[x])
        print(nnodo)
        orden.append(nnodo)
        veci = set(grafo[nnodo])
        clus = veci.union({nnodo})
        clusters.append(clus)

        posvar[nnodo] = i

        print( i, clus) 
        i += 1
        grafo.remove_node(nnodo)
        for x in veci:
            for y in veci:
                if not x==y:
                    grafo.add_edge(x,y)

    
    clusters.append(set())


    for i in range(n):
            con = clusters[i]
            cons = con - {orden[i]}
            if not cons:
                parent[i] = n
                child[n].add(i)
            else:
                pos = min(map(lambda h: posvar[h], cons))
                parent[i] = pos
                child[pos].add(i)



    
    
    # total = clusters[n-1].copy()
    # for i  in range(n-2,-1,-1):
    #     clus = clusters[i]
    #     for j in range(i+1,n,1):
    #         if clus.intersection(total) == clus.intersection(clusters[j]):
    #             parent[i] = j
    #             child[j].add(i)
    #             break
    #     total.update(clus)
            

    # print(orden)
    return (orden,clusters,borr,posvar,child,parent)
    
def main(prob):
        # info.contradict = False
        # info.solved = False
        prob.inicial.contradict = False
        prob.inicial.solved = False         
        print("entro en main")
        prob.inicia0()                          

        grafo = prob.inicial.cgrafo()
        (prob.orden,prob.clusters,prob.borr,prob.posvar,prob.child,prob.parent)  = triangula(grafo)
       

        # prob.borraapro(M=4,T=3)
        # prob.reinicia()
        # prob.borraaproi(M=4,T=3)
        

        

        


        # # prob.randomsol()
        # prob.reinicia()

        prob.inicia1()
        prob.borrapro()
        prob.borraproi()

        prob.pasaarbol()
  
        
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
    prob = problemaTrianFactor(info,N1)
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

