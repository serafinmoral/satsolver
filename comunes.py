#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:55:15 2019

@author: smc
"""
import networkx as nx


def numerotodasfalsas(lclau,n):
    varincl = set()
    for x in lclau:
        varincl.update(set(map(abs,x)))
    total = 2**(n-len(varincl))
    return total





def numeroalgunafalsa (lclau,n):
    
    k = len(lclau)
    
    
    
    if (k == 1):
        return 2**(n-len(lclau[0]))
    
    if(k==0):
        return 0
    
    nlista = lclau.copy()
    clau = nlista.pop()
    
   
    
    p1 = numeroalgunafalsa(nlista,n)
    
    
    
    
    
    p3= numfalsayalguna(clau,nlista,n) 
    
    return p1 + 2**(n-len(clau)) -p3
    
    
def numfalsayalguna(clau,lclau,n):
    
    negclau = set(map(lambda x: -x,clau))
    nlc = []
    for x in lclau:
        if (len(x.intersection(negclau)) == 0):
            y = frozenset(x-clau)
            nlc.append(y)
        
    return numeroalgunafalsa(nlc,n-len(clau))
        
    
    
def probabilidad(lista):
    
    varincl = set()
    for x in lista:
        varincl.update(set(map(abs,x)))
    
    n = len(varincl)
    
    
    
    return (2**n - numeroalgunafalsa(lista,n))/2**n
     
    
    
def condprobabilidad(cl,lista):
    y = probabilidad(lista)
    lista.append(cl)
    z = probabilidad(lista)
    lista.pop()
    if (y!=0):
        return z/y
    else:
        return -1
    
   


def casicontenida(x,y,th,method=4):
        z=0
        

        if method==4:
            z = 1-condprobabilidad(y,[x])
        elif method == 0: 
            z = len(x - y)/len(x)
        elif method == 1:
            z = len(x - y)/len(x |y)
        elif method == 3:
            z = len(x - y)
        
        
        if z <= th:
            return True
        else:
            return False

def resolution (var,clau1,clau2):
    clau = clau1.union(clau2) - {var,-var}
    for x in clau:
        if -x in clau:
            clau = frozenset({0})
            break
    return clau
        
def reduceplus(clau,x):
        h = []
        cont = set()
        for y in clau:
            if y in x:
                h = [0]
                cont = {y}
                break
            elif -y not in x:
                h.append(y)
            else:
                cont.add(y)
                
        return (frozenset(h),cont)
    
def inserta(cl,cola):
       l = len(cl)
#       print(cl)
       if l not in cola:
           cola[l] = set()
#       print(cola[l])    
       cola[l].add(cl) 
     

def reduce(clau,x):
        h = []
        for y in clau:
            if y in x:
                
                h = [0]
                break
            elif -y not in x:
                h.append(y)
        
                
        return frozenset(h)
    
def variables(cl):
    return set(map(lambda x: abs(x), cl))    
    

def calculapotentials(lista,var):
    result = []
    for x in lista:
#        print(x.listavar)
        if var in x.listavar:
            result.append(x)
    for x in result:
        lista.remove(x)
    return result
    



def calculaorden(grafo):
    
    orden = []
    
    grafoc = grafo.copy()
    
    
    centra = nx.algorithms.centrality.degree_centrality(grafoc)

#    print(centra)
    ma = 0
    i= 0
    while grafo.nodes:
        nnodo = min(grafo.nodes,key = lambda x : grafo.degree[x] - 0.1* centra[x])
        orden.append(nnodo)
        
        veci = set(grafo[nnodo])
        
        grafo.remove_node(nnodo)
        for x in veci:
            for y in veci:
                if not x==y:
                    grafo.add_edge(x,y)
                    
                    
    
    

    

    print(orden)
    return orden
        