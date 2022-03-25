#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:55:15 2019

@author: smc
"""

"""
Calculates the size of the union of the variables of all the tables in a list
"""

from tablaClausulas import *
from vartablas import *

def tam(l):
    tot = set()
    if l:
        for h in l:
            tot.update(set(h.listavar))
        return len(tot)
    else:
        return 0    

def valord(p):
    if not len(p.listavar)==1:
        print("llamada impropia")
    else:
        v = p.listavar[0]
        if not p.tabla[0]:
            return v
        else:
            return -v

def contenida(nodo, listanodos):
    if (len(listanodos)>0):
        nodoaux = nodoTabla([])
        for x in range(len(listanodos)):
            nodoaux.combina(listanodos[x], inplace=True)
        listaBorra = list(set(nodoaux.listavar)-set(nodo.listavar))
        nodoaux.borra(listaBorra, inplace=True)
        nodoaux.tabla = np.logical_not(nodoaux.tabla)
        nodoaux=nodoaux.suma(nodo)
        return nodoaux.trivial()
    else:
        return False

def partev(lista,v):
    bor = []
    nl = []
    for p in lista:
        
        if v in p.listavar:
            l = p.descomponev(v)
            if len(l)>1:
                nl = nl +l 
                bor.append(p)
                print("descomposicion ", len(p.listavar))
                print([len(q.listavar) for q in l])
                # sleep(1)
            
    for p in bor:
        lista.remove(p)
    lista = lista.extend(nl)



def potdev(v):
    res = nodoTabla([abs(v)])
    if v>0:
        res.tabla[0] = False
    else:
        res.tabla[1] = False
    return res


def calculaclusters1(lista,p,var):
    li = [set(q.listavar).union(p.listavar) - {var} for q in lista]
    borraincluidos(li)
    return li

def calculaclusters2(lista,var):
    li = []
    for p in lista:
        s = set(p.listavar)
        for q in lista:
            li.append(s.union(q.listavar)- {var})
    borraincluidos(li)
    return li

def borraincluidos(lista):
    
    lista.sort(key = lambda x : - len(x) )

    
    i=0
    while i <len(lista)-1:
        j = i+1
        while j < len(lista):
            con1 = lista[i]
            con2 = lista[j]
            if con2 <= con1:
                lista.remove(con2)
            else:
                j+=1
        i += 1


def ordenaycombinaincluidas(lista,rela):
    
    lista.sort(key = lambda x : - len(x.listavar) )

    
    i=0
    while i <len(lista)-1:
        j = i+1
        while j < len(lista):
            if set(lista[j].listavar) <= set(lista[i].listavar):
                p = lista[i]
                q = lista[j]
                
                rela.borrarpot(p)
                rela.borrarpot(q)
                p.combina(q,inplace= True)
                rela.insertar(p)
                lista.remove(q)
            else:
                j+=1
        
        i+=1
    lista.reverse()



def createclusters (lista):
    listasets = []
    for cl in lista:
        va = set(map(abs,cl))
        encontrado = False
        for x in listasets:
            if va <= x:
                encontrado = True
                break
            
        if not encontrado:
            listasets.append(va)

    i = 0
    j = 1
    while (i<len(listasets)-1):
        if listasets[i] <= listasets[j]:
            del listasets[i]
            j = i+1
        elif listasets[j] <= listasets[i]:
            del listasets[j]
            if j >= len(listasets):
                i += 1
                j = i+1
        else:
            j += 1
            if j >= len(listasets):
                i += 1
                j = i+1
    listaclaus = []
    for i in range(len(listasets)):
        listaclaus.append([])


    for cl in lista:
        va = set(map(abs,cl))
        for i in range(len(listasets)):
            if va <= listasets[i]:
                listaclaus[i].append(cl)
                break

    return(listasets,listaclaus)



def marginaliza(lista,var, M=30, Q=20):

    

    if not lista:
        
        return (True,[],[])

    partev(lista,var)

   
    res = []
    si = []
    vars = set()
    deter = False
    for p in lista:
        if var in p.listavar:

            vars.update(p.listavar)
            si.append(p)
            if not deter:
                deter = p.checkdetermi(var)
                if deter: 
                    nv = set()
                    keyp = p.minimizadep(var,nv)
                    setkey = set(keyp.listavar)
                    # if len(keyp.listavar) < len(p.listavar):
                        # print("minimizo ",len(keyp.listavar) ,  len(p.listavar))
        else:
            print("warning: variable no en tabla")
            res.append(p)

                                    
        
    if not si:
        return (True,res,[nodoTabla([var])])
    
    exact = True

    if deter:
        vars.discard(var)

        listp = [keyp]
        if len(vars) <= Q:
            # print("global ")
            r = nodoTabla([])
            lc = calculaclusters1(si,keyp,var)
            while si:
                q = si.pop()
                r.combina(q,inplace=True)
            r.borra([var],inplace=True)
            if r.contradict():
                con = nodoTabla([])
                con.anula()
                return (True,[con],[keyp])
                    

            for h in lc:
                rh = r.borra(list(vars-h)) 
                        
                if not rh.trivial():
                    res.append(rh)
                        
        else:
            while si:
                q = si.pop() 
                if q == keyp:
                    r = q.borra([var],inplace = False)
                else:
                    if len(setkey.union(set(q.listavar))) < M+1:
                        r = q.combina(keyp,inplace = False, des = False)
                        r.borra([var],inplace = True)

                        if r.contradict():
                            con = nodoTabla([])
                            con.anula()
                            return (True,[con],[])
                        if not r.trivial():
                            res.append(r)
                    else:
                        exact = False

    else:
            si.sort(key = lambda h: - len(h.listavar) )
            # print("borrada " , var, "metodo 2, n potenciales", len(si))
        
            lista = []
            if len(vars)<= Q:
                # print("global ")
                vars.discard(var)

                r = nodoTabla([])
                lc = calculaclusters2(si,var)
                while si:
                    q = si.pop()
                    r.combina(q,inplace=True)
                listp = [r.copia()]
                
                r.borra([var],inplace=True)
                if r.contradict():
                    con = nodoTabla([])
                    con.anula()
                    return (True,[con],[])
                

                for h in lc:
                    rh = r.borra(list(vars-h)) 
                    
                    if not rh.trivial():
                        res.append(rh)
            else:
                si2 = si.copy()
                listp = si2
                while si:
                    
                    q = si.pop()
                    
                    for p in si2:
                        if len(set(q.listavar).union(set(p.listavar))) >M+1:
                            print( "no exacto")
                            exact = False
                        else:
                            r = p.combina(q)
                            r.borra([var], inplace = True)


                            if r.contradict():
                                con = nodoTabla([])
                                con.anula()
                                r = nodoTabla([var])
                                r.tabla[0] = False
                                r.tabla[1] = False
                                return (True, [con],listp)
                    
                            if not r.trivial():
                
                                res.append(r)

                        
            
            
    return (exact,res,listp)
                
def calculamethod(lista,var):

        
        
            
            si = []    

            deter = False
            vars = set()

            if len(lista)<=2:
                return 1

            for p in lista:
        
            
                if var in p.listavar:
                        vars.update(p.listavar)
                        si.append(p)
                        if not deter:
                            deter = p.checkdetermi(var)
                            if deter: 
                                return 1
            return 2              
                    
def triangulaconorden(pot,orden):

    n = len(orden)
    clusters = []
    
    child = []
    posvar = dict()
    parent = [-1]*(n+1)

    indexvar = dict()
    for v in orden:
        indexvar[v] = []

    for i in range(n+1):
        child.append(set())
    

    for p in pot.listap:
        con = set(p.listavar)
        for v in con:
            indexvar[v].append(con)
    for v in pot.unit:
        indexvar[v].append({abs(v)})

    i=0
    for nnodo in orden:
        lista = indexvar[nnodo]
        cluster = set()
        for y in lista:
            cluster.update(y)
        clusters.append(cluster)
        posvar[nnodo] = i
        print( i, cluster)
        i+=1
        clustersin = cluster-{nnodo}

        for y in clustersin:
            indexvar[y] = list(filter( lambda h: nnodo not in h  ,indexvar[y] ))
            indexvar[y].append(clustersin)
           
        




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
    return (clusters,posvar,child,parent)     