# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import itertools
import os
import sys
from random import *
from time import time

import networkx as nx

from GlobalClausulas import *

# import matplotlib.pyplot as plt

              
#from arbolpot import *
#
#x = 3434
#for i in range(60):
#    x = x*1.2
#    print(x)


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
            elif (len(clausula)==2):
                infor.dobles.add(clausula)
                mclau = frozenset(map(lambda x: -x,clausula))
                if mclau in infor.dobles:
                    par = set(clausula)
                    l1 = par.pop()
                    l2 = -par.pop()
                    if(abs(l1)<abs(l2)):
                        infor.equiv.add((l1,l2))
                    else:
                        infor.equiv.add((l2,l1))



#    print("paso a limpiar")
#    infor.limpiarec(0.0)
#    print("termino de limpiar")
    return infor  

  



def pure_literal(formula):
        counter = get_counter(formula)
        assignment = []
        pures = []
        for literal, times in counter.items():
            if -literal not in counter: 
                pures.append(literal)
        for pure in pures:
            formula = bcp(formula, pure)
        assignment += pures
        return formula, assignment
#%%
def get_counter(formula):
        counter = {}
        for clause in formula:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 1
        return counter


def bcp(formula, VarUnica):
        modificado = []
        for clausula in formula:
            if VarUnica in clausula:
                continue
            if -VarUnica in clausula:
                nueva_clause=[]
                for x in clausula:
                    if x !=-VarUnica:
                        nueva_clause=nueva_clause+[x]
                if not nueva_clause:
                    return -1
                modificado.append(nueva_clause)
            else:
                modificado.append(clausula)
        return modificado
    
def expandesol(sol,nuevas,listas,listae):
    while nuevas:
        v = nuevas.pop()
        encuentravalor(v,listas,sol)
    for (l1,l2) in reversed(listae):
        if l1 in sol and l2 not in sol:
            sol.append(l2)
        elif -l1 in sol and -l2 not in sol:
            sol.append(-l2)       
            
            

def backtracking2(formula,tapren,path, tunit, N1,N2,N3,NI,  R = False):
        
    NI[0] -= 1
#    print(NI[0],path)
    if NI[0]%2000 == 0:
        print(path)
    if formula.contradict:
#        print("contradiccion primaria")
        return []
    if path:
        variable = path[-1]
        listauni = [variable]
    else:
        listauni = []

    listapar = []
    while True:
#        print("ciclo", path)
#        print("entro en unit prop")
        
        while True:


    
            uni = formula.unitprop()
#        print("salgo", uni)
            listauni = listauni  + uni
            if formula.contradict:
                break
            listae = formula.equivprop()
            
            listas = dict()
            nuevas = []
#            nuevas = formula.borraexactolim(listas, M=N3)

 
            listapar.append((nuevas, listas,listae))
            
            if (not nuevas) and (not listae):
                break

        if formula.contradict:
#                print("contradiccion")
                apren = formula.apren
#                print(apren)
                negapren = set(map(lambda x: -x,apren))
                inter = negapren.intersection(set(listauni))
                
                while len(inter)>1:
                    for i in reversed(listauni):
                        if i in negapren:
                            break
                        
                    
                    apren.discard(-i)
                    apren.update(formula.refer.get(frozenset({i}),set()))
                    negapren = set(map(lambda x: -x,apren))
                    inter = negapren.intersection(set(listauni))
                    
                formula.apren = apren
                
                tapren.insertar(frozenset(apren))
                return []
                       
      
                    
                    
                    
                
        if not formula.listaclaus:
                for v in formula.listavar:
                    listauni.append(v)
                    print("añado ", v , " a solucion por no clausulas ")
                
                solucion = listauni
                for x in reversed(listapar):
                     expandesol(solucion,x[0],x[1],x[2])
                formula.compruebasol2(solucion)

                
                formula.solved = True
                formula.contradict = False
#            print("resuelto devuelvo ",asignaciones)
                return listauni
            
        napren = globalClausulas()
        variable = obtenerVariable3e(formula)
        path.append(variable)
        formulan = formula.restringeref(variable)
        formulan.refer[variable] = {-variable}

        if not formulan.contradict:

            ntunit = listauni + tunit
            solucion = backtracking2(formulan,napren,path,ntunit,N1,N2,N3,NI)
            tapren.combina(napren)
        else:
            tapren.insertar(frozenset(formulan.apren))
        path.pop()
            
        if formulan.solved and not formulan.contradict:
            
                solucion = listauni + solucion 
                for x in reversed(listapar):
                     expandesol(solucion,x[0],x[1],x[2])
                formula.compruebasol2(solucion)
                formula.solved = True
                return solucion
        
        
        
        
        else:
                posclau = set(map(abs,formulan.apren))
                posuni = set(map(abs,listauni))
                if not (posclau.intersection(posuni)) or NI[0]<0:
                    formula.apren = formulan.apren
                    formula.solved = False
                    return []
                else:
                    ntunit = listauni + tunit
                    tunitn = set(map(lambda x: -x, ntunit))
                    for cl in napren.listaclaus:
                      if -variable not in cl:
                       cln =  reduce(cl,ntunit)
#                       print("introduzco" ,cln)
                      
                       if 0 not in cln:
                          if cln:
                             formula.refer[cln] = set(cl.intersection(tunitn))
#                             print (formula.refer[cln])
                             formula.insertarref(cln,set(cl.intersection(tunitn)),M=0)
                          else:
                            formula.solved = True
                            formula.contradict = True
                            formula.apren = frozenset(cl.intersection(tunitn))
#                            print(formula.apren)
                            tapren.insertar(formula.apren)
                            return []
                    cl = formulan.apren
                    cln =  reduce(cl,ntunit)
                    if 0 not in cln:
                          if cln:
                             formula.refer[cln] = set(cl.intersection(tunitn))
#                             print (formula.refer[cln])
                             formula.insertarref(cln,set(cl.intersection(tunitn)),M=0)
                          else:
                            formula.solved = True
                            formula.contradict = True
                            formula.apren = frozenset(cl.intersection(tunitn))
#                            print(formula.apren)
                            tapren.insertar(formula.apren)
                            return []

                    
     

#        formulan = formula.restringeref(variable)

 

def asignarandom(formula):
    
    
    configura = set()

    lista = formula.listavar.copy()
    
    
    
    while lista:
        v = lista.pop()        
        ve = choice([v,-v])
#        print(ve)
        configura.add(ve)
        
    return configura
        
def asignagreedy(formula):
    
    
    configura = set()

    lista = formula.listavar.copy()
    
    
    
    while lista:
        v = max(lista,key = lambda x: abs(len(formula.indices.get(x,set()))-len(formula.indices.get(-x,set()))))
        
        (setv,pos) = formula.restringe2(v)
        (setf,neg) = formula.restringe2(-v)
        probp = pos + setv.calprob()
        probn = neg + setf.calprob()
        if probp >= probn:
                ve = v
                fmax = setv
        else:
                ve = -v
                fmax = setf
        lista.discard(v)
#        print(ve)
        configura.add(ve)
        formula = fmax
        
            
        
       
    return configura              
      

        
def asignagreedyr(formula):
    
    
    configura = set()

    lista = formula.listavar.copy()
    
    
    
    while lista:
        v = choice(tuple(lista))
        
        (setv,pos) = formula.restringe2(v)
        (setf,neg) = formula.restringe2(-v)
        probp = pos + setv.calprob()
        probn = neg + setf.calprob()
        if probp >= probn:
                ve = v
                fmax = setv
        else:
                ve = -v
                fmax = setf
        lista.discard(v)
#        print(ve)
        configura.add(ve)
        formula = fmax
        
            
        
       
    return configura                   
         
        
def explora(formula):
    
    
    configura = set()

    mejora = True
    total = len(formula.listaclaus)
    actual = 0
    
    nuevas = set()
    
    while mejora:
        mejora = False
        for v in formula.listavar:
            if v in configura:
                old =v
                configura = configura - {v}
            elif -v in configura:
                old = -v
                configura = configura - {-v}
            else:
                old=0
                
            npos = 0 
            nneg = 0
            cl1 = {0}
            cl2 = {0}
            if v in formula.indices:
                
                for cl in formula.indices[v]:
                    if not cl.intersection(configura):
                        npos+=1
                        if 0 in cl1:
                             cl1 = cl
                        elif len(cl.union(cl2))<len(cl1.union(cl2)):
                             cl1 = cl
                        
            if -v in formula.indices:
                
                for cl in formula.indices[-v]:
                    if not cl.intersection(configura):
                        nneg+=1
                        if 0 in cl2:
                             cl2 = cl
                        elif len(cl.union(cl2))<len(cl1.union(cl2)):
                             cl2 = cl
                        
            if npos >= nneg:
                new = v
            else:
                new = -v
            configura.add(new)    
    
            if (0 not in cl1) and (0 not in cl2) and (len(configura) == len(formula.listavar)):
                newcl = resolution(v,cl1,cl2)
                
                if 0 not in newcl and len(cl)<=3:
                    nuevas.add(newcl)
            if old==0:
                mejor = max([npos,nneg])
                if mejor >0:
                    actual += mejor
                    mejora = True
            elif abs(npos-nneg)>0 and not(old==new):
                actual += abs(npos-nneg)
                mejora = True
    print(len(nuevas))
    
    for cl in nuevas:     
        if len(cl)<= 2:
            formula.insertaborraypoda2(cl)
        else:
            formula.insertar(cl)
 




def explorai(formula,configura):
    
    
    mejora = True
    total = len(formula.listaclaus)
    actual = formula.cuenta(configura)
    
    nuevas = set()
    
    while mejora and actual<total:
        print(actual,total)
        mejora = False
        for v in formula.listavar:
            if v in configura:
                old =v
                configura.discard(v)
            elif -v in configura:
                old = -v
                configura.discard(-v)
            else:
                old=0
                
            npos = 0 
            nneg = 0
            cl1 = {0}
            cl2 = {0}
            if v in formula.indices:
                
                for cl in formula.indices[v]:
                    if not cl.intersection(configura):
                        npos+=1
                        if 0 in cl1:
                             cl1 = cl
                        elif len(cl) <len(cl1):
                             cl1 = cl
                        
            if -v in formula.indices:
                
                for cl in formula.indices[-v]:
                    if not cl.intersection(configura):
                        nneg+=1
                        if 0 in cl2:
                             cl2 = cl
                        elif  len(cl.union(cl1))<len(cl2.union(cl1)):
                             cl2 = cl
                        
            if npos >= nneg:
                new = v
            else:
                new = -v
            configura.add(new)    
    
            if (0 not in cl1) and (0 not in cl2):
                newcl = resolution(v,cl1,cl2)
                
                if 0 not in newcl and len(cl)<=3:
                    nuevas.add(newcl)
            if old==0:
                mejor = max([npos,nneg])
                if mejor >0:
                    actual += mejor
                    mejora = True
            elif abs(npos-nneg)>0 and not(old==new):
                actual += abs(npos-nneg)
                mejora = True
    print(len(nuevas))
           
    return nuevas
                   
    


def explorai2(formula,configura):
    
    
    mejora = True
    total = len(formula.listaclaus)
    actual = formula.cuenta(configura)
    
    nuevas = set()
    
    while mejora and actual<total:
        print(actual,total)
        mejora = False
        for v in formula.listavar:
            if v in configura:
                old =v
                configura.discard(v)
            elif -v in configura:
                old = -v
                configura.discard(-v)
            else:
                old=0
                
            npos = 0 
            nneg = 0
            cl1 = {0}
            cl2 = {0}
            if v in formula.indices:
                
                for cl in formula.indices[v]:
                    if not cl.intersection(configura):
                        npos+=1
                        if 0 in cl1:
                             cl1 = cl
                        elif len(cl)<len(cl1):
                             cl1 = cl
                        
            if -v in formula.indices:
                
                for cl in formula.indices[-v]:
                    if not cl.intersection(configura):
                        nneg+=1
                        if 0 in cl2:
                             cl2 = cl
                        elif len(cl.union(cl1))<len(cl2.union(cl1)):
                             cl2 = cl
                        
               
    
            if (0 not in cl1) and (0 not in cl2):
                newcl = resolution(v,cl1,cl2)
                
                if 0 not in newcl and len(cl)<=3:
                    nuevas.add(newcl)
                
                v1 = set(newcl).pop()
                if v1 in configura:
                    old1 = v1
                else:
                    old1 = -v1
                configura.discard(old1)
                
                y = globalClausulas()
                for cl in formula.indices.get(v,set()).union(formula.indices.get(-v,set())).union(formula.indices.get(v1,set())).union(formula.indices.get(-v1,set())):
                    y.insertar(cl)
                
                configurap = configura.union({v,v1})
                nvv = y.cuenta(configurap)
                configurap = configura.union({v,-v1})
                nvf = y.cuenta(configurap)
                configurap = configura.union({-v,v1})
                nfv = y.cuenta(configurap)
                configurap = configura.union({-v,-v1})
                nff = y.cuenta(configurap)
                if old == v and old1 == v1:
                    nold =nvv
                elif old == v and old1 == -v1:
                    nold = nvf
                elif old1==v1:
                    nold = nfv
                else:
                    nold = nff
                nnew = max ((nvv,nvf,nfv,nff))
                
                if nnew == nvv:
                    configura.add(v)
                    configura.add(v1)
                elif nnew == nvf:
                    configura.add(v)
                    configura.add(-v1)
                elif nnew == nfv:
                    configura.add(-v)
                    configura.add(v1)
                else:
                    configura.add(-v)
                    configura.add(-v1)
                    
                if nnew>nold:
                    mejora = True
                    actual += (nnew-nold)
                
                
            
            else:
                
                if npos>nneg:
                    new = v
                else:
                    new = -v
                configura.add(new)
                if not new == old:
                    actual += abs(npos-nneg)
                
    print(len(nuevas))
           
    return nuevas

def explorain(formula,l,N5 = 3, N4 = 3):

    grafo = formula.cgrafo()
    configura = l.pop()

    mejora = True
    total = len(formula.listaclaus)
    actual = formula.cuenta(configura)

    nuevas = set()
    
    print("inicial ", len(configura))

    while mejora and actual<total:
        print(actual,total)
        mejora = False
        for v in formula.listavar:
            


            if v in configura:
                old =v
                configura = configura - {v}
            elif -v in configura:
                old = -v
                configura = configura - {-v}
            else:
                print("no está")
                old=0
                
            npos = 0 
            nneg = 0
            cl1 = {0}
            cl2 = {0}
            if v in formula.indices:
                
                for cl in formula.indices[v]:
                    if not cl.intersection(configura):
                        npos+=1
                        if 0 in cl1:
                             cl1 = cl
                        elif len(cl.union(cl2)) < len(cl1.union(cl2)):
                            cl1 = cl
                        
            if -v in formula.indices:
                
                for cl in formula.indices[-v]:
                    if not cl.intersection(configura):
                        nneg+=1
                        if 0 in cl2:
                             cl2 = cl
                        elif len(cl.union(cl1))<len(cl2.union(cl1)):
                             cl2 = cl
                        
            
    
            if (0 not in cl1) and (0 not in cl2):
                newcl = resolution(v,cl1,cl2)
                
                if 0 not in newcl and len(cl)<=N4:
                    nuevas.add(newcl)
                
                cand = [v]
                cando = [old]
                conj = set(grafo[v])
                while conj and len(cand)< N5: 
                    v1 = conj.pop()
                    if v1 in configura:
                        old1 = v1
                    else:
                        old1 = -v1
                    configura.discard(old1)
                    cando.append(old1)
                    cand.append(abs(old1))

                # print(len(configura), len(cand))

                y = globalClausulas()
                lista = set()
                for v in cand:
                    lista.update(formula.indices.get(v,set()))
                    lista.update(formula.indices.get(-v,set()))
                
                for cl in lista:
                    if not cl.intersection(configura):
                        y.insertar(cl)
                
                options = itertools.product([0,1],repeat = len(cand))
                
                numeros = dict()
                for o in options:
                    configurap = configura.copy()
                    for i in range(len(o)):
                        if o[i]==0:
                            configurap.add(cand[i])
                        else:
                            configurap.add(-cand[i])
                    numeros[frozenset(configurap)] = y.cuenta(configurap)

                  
                
                configurap = configura.copy()
                for x in cando:
                    configurap.add(x)
                nold = numeros[frozenset(configurap)]
                
                valores = list(numeros.values())
                llaves = list(numeros.keys())

                nnew = max(valores)

                mcon = llaves[valores.index(nnew)]
                
                
                    
                if nnew>nold:
                    mejora = True
                    actual += (nnew-nold)
                    # print(actual)

                configura = set(mcon)
                
                
            
            else:
                
                if npos>nneg:
                    new = v
                elif npos==nneg:
                    new = old
                else:    
                    new = -v
                configura.add(new)
                if not new == old:
                    actual += abs(npos-nneg)
                    # print(actual)
                    mejora = True
                
    print(len(nuevas))
    l.append(configura)     

    if (actual==total):
        info.solved=True
        info.solucion = configura
        return set()
    return nuevas

                          
        
def explora3(formula, N=10000):
    
    gr = formula.calculagrafo()
    
    configura = set()
    conta = dict()

    total = len(formula.listaclaus)
    actual = 0
    
    nuevas = set()
    v = choice([*gr])
    conta[v] = 1
    for i in range(N):
#            print("v",v)   
#            print(configura)
            if v in configura:
                old =v
                configura = configura - {v}
            elif -v in configura:
                old = -v
                configura = configura - {-v}
            else:
                old=0
                
            npos = 0 
            nneg = 0
            cl1 = {0}
            cl2 = {0}
            if v in formula.indices:
                
                for cl in formula.indices[v]:
                    if not cl.intersection(configura):
                        npos+=1
                        if 0 in cl1:
                             cl1 = cl
                        elif len(cl.union(cl2))<len(cl1.union(cl2)):
                             cl1 = cl
                        
            if -v in formula.indices:
                
                for cl in formula.indices[-v]:
                    if not cl.intersection(configura):
                        nneg+=1
                        if 0 in cl2:
                             cl2 = cl
                        elif len(cl.union(cl2))<len(cl1.union(cl2)):
                             cl2 = cl
                        
            if npos >= nneg:
                new = v
            else:
                new = -v
            configura.add(new)    
    
            if (0 not in cl1) and (0 not in cl2) and (len(configura) == len(formula.listavar)):
                newcl = resolution(v,cl1,cl2)
                
                if 0 not in newcl and len(cl)<=5:
                    formula.insertar(newcl)
            v= siguiente(gr,v,conta)
                    
                                
def siguiente(gr,v,cont):
    
    if v in gr:
        lista = gr[v]
    else:
       return  choice([*gr])
    minv = -1
    for v in lista:
        if v not in cont:
            cont[v]=0
            minv = 0
        elif minv==-1:
            minv = cont[v]
        else:
            minv = min(minv,cont[v])
    
    minor = []
    for v in lista:
        if v not in cont:
            minor.append(v)
        elif cont[v]==minv:
            minor.append(v)
    
    vn = choice(minor)
    if not vn in cont:
        cont[vn]=1
    else:
        cont[vn] += 1

    return vn
    
    
    
    
    
      
def explora2(formula, M=50):
    
    configura = set()

    total = len(formula.listaclaus)
    actual = 0
    
    nuevas = set()
    
    for i in range(50):
        for v in formula.listavar:
            if v in configura:
                old =v
                configura = configura - {v}
            elif -v in configura:
                old = -v
                configura = configura - {-v}
            else:
                old=0
                
            npos = 0 
            nneg = 0
            cl1 = {0}
            cl2 = {0}
            if v in formula.indices:
                
                for cl in formula.indices[v]:
                    if not cl.intersection(configura):
                        npos+=1
                        if 0 in cl1:
                             cl1 = cl
                        elif len(cl.union(cl2))<len(cl1.union(cl2)):
                             cl1 = cl
                        
            if -v in formula.indices:
                
                for cl in formula.indices[-v]:
                    if not cl.intersection(configura):
                        nneg+=1
                        if 0 in cl2:
                             cl2 = cl
                        elif len(cl.union(cl2))<len(cl1.union(cl2)):
                             cl2 = cl
                        
            if npos >= nneg:
                new = v
            else:
                new = -v
            configura.add(new)    
    
            if (0 not in cl1) and (0 not in cl2) and (len(configura) == len(formula.listavar)):
                newcl = resolution(v,cl1,cl2)
                
                if 0 not in newcl:
                    formula.insertar(newcl)
            
                                
    
            
    
    
def encuentravalor(v,listas,solucion):
    forp = False
    forn = False
    if v in solucion or -v in solucion:
        print(v , "ya en solucion")
        return
    neg = set(map(lambda x: -x, solucion))
    if -v in listas:
        for x in listas[-v]:
            if ((x-{-v})<=neg):
                   forn = True
                   break
    if not forn:
        if v in solucion:
            print("repetido", v)
        solucion.append(v)
        return
    
    if v in listas:
        for x in listas[v]:
            if ((x-{v})<=neg):
                   forp = True
                   break
               
    if not forp:
        if -v in solucion:
            print("repetido ", v)
        solucion.append(-v)
        return 
    print("problema", v)
    return -1
                   
    
               
              
                   
     
    


    
    
def obtenerVariable(g):
        formula = g.listaclaus
        z = dict()
        nc = len(formula)
        for cla in formula:
            posclau = frozenset(map(abs,cla))
            for x in posclau:
                if x in z:
                    z[x].add(posclau)
                else:
                    z[x]={posclau}          
        best=len(formula)**3
        nbest=-1
        for i in z:
            conjunto = set({i})
            l=len(z[i])
            for x in z[i]:
                conjunto.update(x)
                aux = len(conjunto)*nc+l
            if(aux<best) :
                nbest = i
                best = aux          
        return nbest   
                
def obtenerVariable2(formula):
        z = dict()
        for cla in formula.listaclaus:
            
            for x in cla:
                if x in z:
                    z[-x] *= (2**(len(cla)-1)-1)/2**(len(cla)-1)
#                    z[x] += 1/2**(len(cla)-1)
#                    z[-x] -= 1/2**(len(cla)-1)
                else:
                     z[-x] = (2**(len(cla)-1)-1)/2**(len(cla)-1)
                     z[x] = 1.0
#                    z[x] =  1/2**(len(cla)-1) 
#                    z[-x] = - 1/2**(len(cla)-1)
        
        
        best=1
        nbest=0
        for i in z:
            if z[-i]==0.0:
               nbest = i
               break
            elif z[i]/z[-i]>= best:
                    nbest = i
                    best = z[i]/z[-i]
        return nbest   
        
def obtenerVariable4(formula):
        z = dict()
        for cla in formula.listaclaus:
            
            for x1 in cla:
                for x2 in cla-{x1}:
                    if x1 in z:
                        z[x1].add(x2)
                    else:
                        z[x1]= {x2}
                    if x2 in z:
                        z[x2].add(x1)
                    else:
                        z[x2]= {x1}
                    
        best = 0
        nbest = 1    
        for v in z:
            if len(z[v])>best:
                best = len(z[v])
                nbest = v
            
        
        return nbest   
    
    
def obtenerVariable5(formula):
        vmax = 0
        best = 0
        centr = dict()
        for v in formula.listavar:
            centr[v] =0.0
            for vp in formula.listavar:
                if (v,vp) in formula.dep:
                    centr[v] += formula.dep[(v,vp)]
                elif (vp,v) in formula.dep:
                    centr[v] += formula.dep[(vp,v)]
               
#        print (vmax,len(formula.indices.get(vmax,set())),len(formula.indices.get(-vmax,set())))
        vmax = max(formula.listavar, key = lambda x: centr[x])
        if len(formula.indices.get(-vmax ,set()))>len(formula.indices.get(vmax,set())):
              vmax = -vmax
        return vmax
    
    
def obtenerVariable3(formula):
        vmax = 0
        best = 0
        for v in formula.listavar:
            l1 = len(formula.indices.get(v,set()))
            l2 = len(formula.indices.get(-v,set()))
            if l1*l2 >= best:
                best = l1*l2
                if(l1>l2):
                    vmax = v
                    
                else:
                    vmax = -v
#        print (vmax,len(formula.indices.get(vmax,set())),len(formula.indices.get(-vmax,set())))
        
            
    
    
        
        
        
        return vmax   
        
     
                   
                       

    
                   
        
                   
                       
               
               

      
        
    
def auxtam(v,r):
    l1 = len(r.indices.get(v,set()))
    l2 = len(r.indices.get(-v,set()))
#    if len(l1)==0 or len(l2)==0:
#        return 0
#    con = set()
#    for cl in l1:
#        con= con.union(cl)
#        
#    for cl in l2:
#        con= con.union(cl)
        
    return l1*l2
    

def obtenerVariablegraph(formula):
#        print("inicio")
        grafo = formula.cgrafo()
#        plt.subplot(122)
#        
#        nx.draw(grafo)
#        print("computing centrality")
        centra = nx.algorithms.centrality.betweenness_centrality(grafo)
#        print("fin centrality")

        vmax = max(centra.keys(),key = lambda x: centra[x] )

#                formula
        
        r = formula.copia()

        
       
        
        
        
        apren = []
        
        while len(r.listavar) > 1:
            
            v = min(r.listavar-{vmax}, key = lambda x: auxtam(x,r) )
            

            apren = apren + r.marginalizain(v,3,25)
            if r.contradict:
#                    print("contra")
                    formula.contradict=True
                    formula.solved=True
                    return vmax
            
#        print("fin ", vmax, len(apren))
        if frozenset({vmax}) in r.listaclaus and frozenset({-vmax}) in r.listaclaus:
#                    print("contra")
                    formula.contradict=True
                    formula.solved=True
                    return vmax

        
#        print(len(apren))
                
        for cl in apren:
                
                formula.insertarref(cl,r.refer.get(cl,set()) )
        
#        formula.poda()
            
        
        if frozenset({-vmax}) in r.listaclaus:
#            print("fneg")
            return -vmax
        
        if frozenset({vmax}) in r.listaclaus:
#            print("pos")
            return vmax
        
            
#        print (vmax ,ar.computevalconfig({vmax}),ar.computevalconfig({-vmax}) )
            
    
                           
                   
                       
               
               

               
                
            
              
                
         
#        print (vmax,len(formula.indices.get(vmax,set())),len(formula.indices.get(-vmax,set())))
        if len(formula.indices.get(vmax,set()))> len(formula.indices.get(-vmax,set())):
            return vmax  
        else:
            return -vmax                
               

               
def obtenerVariablecuenta(formula,cuenta):
   
        vmax = 0
        best = 0
        for v in formula.listavar:
            l1 = len(formula.indices.get(v,set()))
            l2 = len(formula.indices.get(-v,set()))
            if l1+l2 > best:
                best = l1+l2
                vmax = v

        if cuenta[vmax]>= 0:
            return vmax
        else:
            return -vmax
def obtenerVariable3e(formula,N1=3,N2=3):
#        print("inicio")
    neg = set(map(lambda x: -x, formula.listavar))
    candidates = formula.listavar.union(neg)
    return max (candidates, key = lambda x: len(formula.indices.get(x,set())))
#                

def obtenerVariable3d(formula,N1=3,N2=3):
#        print("inicio")
        vmax = 0
        best = 0
        for v in formula.listavar:
            l1 = len(formula.indices.get(v,set()))
            l2 = len(formula.indices.get(-v,set()))
            if l1*l2 > best:
                best = l1*l2
                vmax = v
#                
        
#        r = formula.copia()
#
#        
#    
#        
#        
#        apren = []
#        
#        while len(r.listavar) > 1:
#            
#            v = min(r.listavar-{vmax}, key = lambda x: auxtam(x,r) )
#            
#
#            apren = apren + r.marginalizain(v,N1,N2)
#            if r.contradict:
##                    print("contra")
#                    formula.contradict=True
#                    formula.solved=True
#                    formula.apren = r.apren
#                    if not formula.apren:
#                        print ("aprendo ",formula.apren)
#                    return vmax
#            
##        print("fin ", vmax, len(apren))
#        if frozenset({vmax}) in r.listaclaus and frozenset({-vmax}) in r.listaclaus:
##                    print("contra")
                    # formula.contradict=True
                    # formula.solved=True
                    # formula.apren = r.refer.get(frozenset({vmax}),set()).union( r.refer.get( frozenset({-vmax}),set()))
                    # if (not formula.apren):
                    #     print("vamx ", vmax, r.refer.get(frozenset({vmax}),set()),r.refer.get( frozenset({-vmax}),set())   )
                    # return vmax
#
#        
##        print("aprendidas ", len(apren))
#                
#         for cl in apren:
# ##                print("inserto ", cl,r.refer.get(cl,set()) )
#                 formula.insertarref(cl,r.refer.get(cl,set()))
#                 if formula.contradict:
#                     return vmax
#        
#        
##        formula.poda()
#            
#        
#         if frozenset({-vmax}) in r.listaclaus:
# ##            print("fneg")
#             return -vmax
# #        
#         if frozenset({vmax}) in r.listaclaus:
# ##            print("pos")
#             return vmax
        
        if len(formula.indices.get(vmax,set()))> len(formula.indices.get(-vmax,set())):
            return vmax  
        else:
            return -vmax                
                   
#        print (vmax ,ar.computevalconfig({vmax}),ar.computevalconfig({-vmax}) )
            
    
    
def obtenerVariable3c(formula,N1,N2):
#        print("inicio")
        vmax = 0
        best = 0
        for v in formula.listavar:
            l1 =formula.indices.get(v,set())
            l2 = formula.indices.get(-v,set())
            im = 0.0
            for cl in l1:
                im += (len(cl)-1)/2**(len(cl)-1)
            for cl in l2:
                im += (len(cl)-1)/2**(len(cl)-1)
            
            if im > best:
                best = im
                vmax = v
#                
        
        r = formula.copia()

        
      
        
        
        apren = []
        
        while len(r.listavar) > 1:
            
            v = min(r.listavar-{vmax}, key = lambda x: auxtam(x,r) )
            

            apren = apren + r.marginalizain(v,N1,N2)
            if r.contradict:
#                    print("contra")
                    formula.contradict=True
                    formula.solved=True
                    formula.apren = r.apren
                    if not formula.apren:
                        print ("aprendo ",formula.apren)
                    return vmax
            
#        print("fin ", vmax, len(apren))
        if frozenset({vmax}) in r.listaclaus and frozenset({-vmax}) in r.listaclaus:
#                    print("contra")
                    formula.contradict=True
                    formula.solved=True
                    formula.apren = r.refer.get(frozenset({vmax}),set()).union( r.refer.get( frozenset({-vmax}),set()))
                    if (not formula.apren):
                        print("vamx ", vmax, r.refer.get(frozenset({vmax}),set()),r.refer.get( frozenset({-vmax}),set())   )
                    return vmax

        
#        print("aprendidas ", len(apren))
                
        for cl in apren:
#                print("inserto ", cl,r.refer.get(cl,set()) )
                formula.insertarref(cl,r.refer.get(cl,set()))
                if formula.contradict:
                    return vmax
        
        
#        formula.poda()
            
        
        if frozenset({-vmax}) in formula.listaclaus:
#            print("fneg")
            return -vmax
        
        if frozenset({vmax}) in formula.listaclaus:
#            print("pos")
            return vmax                           
                   
                       
               
               

               
                
        l1 =formula.indices.get(vmax,set())
        l2 = formula.indices.get(-vmax,set())
              
        v1 = 1.0
        for  cl in l2:
            x = 2**(len(cl)-1)
            v1 *= (x-1)/x
            
        v2 = 1.0
        for  cl in l1:
            x = 2**(len(cl)-1)
            v2 *= (x-1)/x
#        print (vmax,len(formula.indices.get(vmax,set())),len(formula.indices.get(-vmax,set())))
        if v1>v2:
            return vmax  
        else:
            return -vmax                
               

               

        
class solveSATBack:    
    def __init__(self):
        self.method = 0
        self.limit = 0
        self.solucion = False
        self.solved = False    
        
        self.conjuntoclau = []
 
        self.configura = []
        self.nvar = 0
 

        
    
def main(info,N1,N2,N3,I):
        
        # cuenta = dict()
        # for x in info.listavar:
        #     cuenta[x]= 0
        #     cuenta[-x] = 0

        # totalclau = info.listaclaus.copy()
        # for cl in totalclau:
        #     if info.bloqueogen(cl,M=1000):
        #         print(cl, " bloqueada ")
        #         info.eliminar(cl)

        solvedexplore = False
        configura = asignagreedy(info)
        nuevas = (explorai(info,configura))
        # for x in configura:
        #     cuenta[x] += 1
            
        if not info.solved:
             for cl in nuevas:
                info.insertaborraypoda2(cl)
        l = [configura]
        nuevas = ( explorain(info,l,N5=2,N4=3))

        configura = l[0]
        
        # for x in configura:
        #     cuenta[x] += 1


        

        if not info.solved:
            print(len(nuevas))
  

       

            for cl in nuevas:
                info.insertaborraypoda2(cl)

        
        
        
        # nuevas = ( explorain(info,l,N5=10,N4=3))
        # configura = l[0] 
        
        # # for x in configura:
        # #     cuenta[x] += 1


        # solvedexplore = info.solved
        
        # if not info.solved:
        #     print(len(nuevas))
  

       

        #     for cl in nuevas:
        #         info.insertaborraypoda2(cl)

        for i in range(0):
        
            configura = asignarandom(info)
            l = [configura]
            nuevas = ( explorain(info,l,N5=8,N4=3))
            # configura = l[0]
            # if info.solved:
            #     break
            # for x in configura:
            #     cuenta[x] += 1
            for cl in nuevas:
                info.insertaborraypoda2(cl)
        
        solvedexplore = info.solved
        
        
        # for x in info.listavar:
        #     print(x,cuenta[x] - cuenta[-x])

        print(info.solved,info.contradict)
        tuni = []

        # if not info.solved:
        #     grafo = info.cgrafo()
        #     orden = calculaorden(grafo)
            
        #     info.saturaborra(orden,N=0)



        if not info.solved:
            info.poda()

            print(info.solved,info.contradict)

            tapren = globalClausulas()
            path = []
        
        # else:
        #     configura = list(configura)

        listas = dict()
        elimina = []
        while not info.solved:
            NI = [I]
            tuni = tuni + info.unitprop()

            elimina = elimina + info.borraexactolim2(listas,M=0)
            print(elimina)

#            print(info.unit)
            formula = info.copia()
            configura = backtracking2(formula,tapren,path,tuni,N1,N2,N3,NI)   
            info.solved = formula.solved
            info.contradict = formula.contradict
            print("antes clausu ",len(tapren.listaclaus))
            
#            tapren.poda()
            if tapren.contradict:
                info.solved = True
                info.contracit = True
            
            print("despues clausu ",len(tapren.listaclaus))   

            for cl in tapren.listaclaus:
                info.insertarc(frozenset(cl))
            tapren.anula()

            
        
        if info.contradict:
            configura = []
            print("Inconsistente")
            
        elif not solvedexplore:
            configura = configura+tuni
            expandesol(configura,elimina,listas,[])
#            for (l1,l2) in lista:
#                if l1 in configura:
#                    configura.append(l2)
#                elif -l1 in configura:
#                    configura.append(-l2)
            info.compruebasol2(configura)
            print("Consistente", len(configura),configura)

        else:
            configura = l.pop()
            info.compruebasol2(configura)
            print("Consistente", len(configura),configura)
        
  
ttotal = 0
i = 0

#
#reader=open(sys.argv[1],"r")
#
#writer=open(sys.argv[2],"w")


reader=open('entrada',"r")

writer=open('salida',"w")

while reader:
    linea = reader.readline().rstrip()  
    if not linea:
        break
    param = linea.split()
    nombre = param[0]
    N1 = int(param[1])
    N2 = int(param[2])
    N3 = int(param[3])
    I = int(param[4])
    print(nombre)     
    t1 = time()
    i +=1
    info = leeArchivoGlobal(nombre)
    t2= time()



#info = leeArchivoSet('SAT_V144C560.cnf')

#print(info.listavar)

    

#print(problema.conjuntoclau.listavar)


    



#    problema.explora()

    t4 = time()
    

#problema.originalpotentials = problema.totaloriginal.extraePotentials(problema.ordenbo,problema.conjuntosvar)

    main(info,N1,N2,N3,I)
    
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
