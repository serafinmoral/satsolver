# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
""" 
import networkx as nx    
from SimpleClausulas import *
from  ProblemaTrianFactor import *
from time import *
from utils import *

from arboltablaglobal import *

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
    
    return infor, nvar, nclaus
    
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
        
        
    i = 0
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
        # print(nnodo)
        orden.append(nnodo)
        veci = set(grafo[nnodo])
        clus = veci.union({nnodo})
        clusters.append(clus)

        posvar[nnodo] = i

        # print( i, clus) 
        i += 1
        grafo.remove_node(nnodo)
        for x in veci:
            for y in veci:
                if not x==y:
                    grafo.add_edge(x,y)

    
    clusters.append(set())

    h = list(map(len,clusters))
    print("maximo: ", max(h), "suma: ", sum(h))
    sleep(1)
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
    return (orden,cnodo,mh)
    
    
def main(prob, Previo=True, Mejora=False): #EDM
        # info.contradict = False
        # info.solved = False
        
        prob.inicial.solved = False         
        print("entro en main")  #EDM

        prob.inicia0()        


        t = varpot(prob.Q, prob.Partir)
        t.createfrompot(prob.pinicial)
        prob.rela = t


        # prob.rela.mejoralocal()           
        if Mejora:  #EDM
            prob.rela.mejoralocal()      #EDM  
        # print("otra vez!")      #EDM  


        lista = prob.rela.extraelista()
        prob.pinicial.listap = lista


        if Previo: #EDM
            prob.previo()

        if prob.contradict:
            print("problema contradictorio")

        else:

            t = varpot(prob.Q, prob.Partir)
            t.createfrompot(prob.pinicial)
            prob.rela = t
               

        # prob.rela.mejoralocal()           
        # if Mejora:  #EDM
        #     prob.rela.mejoralocal()      #EDM  
            
        # arbol = calculaglobal(prob.rela)




        # (prob.orden,prob.clusters,prob.borr,prob.posvar,prob.child,prob.parent) = triangulap(prob.pinicial) 


            prob.borradin()

        print("salgo de borrado")

        if not prob.contradict:
            prob.sol = prob.findsol()
            prob.compruebaSol()
            return True
        else:
            print(" problema contradictorio ")
            return False


def borradocontablas(archivolee, Q=[20],Mejora=[False], Previo=[True], Partir=[True], archivogenera="salida.csv"):
    try:
        reader=open(archivolee,"r")
        writer=open(archivogenera,"w")
        writer.write("Problema;Variable;Claúsulas;Q;MejoraLocal;Previo;PartirVars;TLectura;TBúsqueda;TTotal;SAT\n")
        ttotal = 0
        # i=0
        for linea in reader:
            # i=i+1
            linea = linea.rstrip()
            if len(linea)>0:
                cadena = ""
                param = linea.split()
                nombre = param[0]
                N1 = int(param[1])
                print(nombre)     
                t1 = time()
                (info, nvar, nclaus) = leeArchivoGlobal(nombre)
                t2= time()
                for Qev in Q:
                    for Mej in Mejora:
                        for Pre in Previo:
                            for Part in Partir:
                                try:
                                    t3 = time()
                                    cadena= nombre + ";" + str(nvar) + ";" + str(nclaus) + ";" + str(Qev) + ";" + str(Mej) + ";" + str(Pre) + ";" + str(Part) + ";"
                                    prob = problemaTrianFactor(info,Qin=Qev) #EDM   #Último parámetro es Q
                                    # prob = problemaTrianFactor(info,N1,Qev) #EDM   #Último parámetro es Q
                                    t4 = time()
                                    # main(prob)  #EDM 
                                    bolSAT = main(prob, Qev,Mej) #EDM 
                                    t5 = time()
                                    print("tiempo lectura ",t2-t1)
                                    print("tiempo busqueda ",t5-t4)
                                    print("tiempo TOTAL ",t5-t3+t2-t1)
                                    cadena =  cadena + str(t2-t1) + ";" + str(t5-t4) + ";" + str(t5-t3+t2-t1) + (";SAT" if bolSAT else ";UNSAT") + "\n"
                                except ValueError:
                                    cadena = cadena + "ERROR"
                                writer.write(cadena)
                                # ttotal += t5-t1
                # print(Q)
        # if i>0:
        #     print ("tiempo medio ", ttotal/i)
        #     writer.write("tiempo medio " + str(ttotal/i)+"\n")
        writer.close()
        reader.close()    
    except ValueError:
        print("Error")
borradocontablas("entrada",[15],[False],[True, False],[True,False],"prueba05.txt")