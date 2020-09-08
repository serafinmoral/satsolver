# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os

import itertools
import networkx as nx    
import matplotlib.pyplot as plt

from random import *
              
from GlobalClausulas import *
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
    

def cuenta(i,var,poten,trian):
    child=trian[2]
    hyp = trian[0]
    if var not in hyp[i]:
        return (0,0)
    np = len(poten[i].indices.get(var,set()))
    nn = len(poten[i].indices.get(-var,set()))
    if (np>0) or (nn>0):
        return (np,nn)
    
    np = 0
    nn = 0
    hijos = child.get(i,[])
    for j in hijos:
        (p,n) = cuenta(j,var,poten,trian)
        np += p
        nn+= n
    return (np,nn)
    
def obtenerVariable(poten,trian):
    orden = trian[3]
    i = len(orden)-1
    var = orden[i]
    
    (pos,neg) = cuenta(i,var,poten,trian)
    if neg > pos:
        var = -var
    return var

def cdesc(j,child):
    result = [j]
    if j in child:
        for k in child[j]:
            result =  cdesc(k,child) + result
    return result

def update(poten,trian,valores):
    orden = trian[3]
    child = trian[2]
    hyp = trian[0].copy()
    par = trian[1]
    pvalores = set(map(abs,valores))
    
    result = []
    for i in range(len(hyp)):
        hyp[i] = hyp[i]-pvalores
        if not hyp[i]:
            tdesc = [i]
            hijos = child.get(i,set())
            for j in hijos:
                l=0
                potenj = []
                ordenj=[]
                hypj = []
                childj = dict()
                parj = dict()
        
                desc = cdesc(j,child)
                tdesc= tdesc+desc
        
                if desc:
                  for k in desc:
                    ordenj.append(orden[k])
                    potenj.append(poten[k])
                    
                
                    hypj.append(hyp[k])
                    if not k == j:
                        np = desc.index(par[k])
                        parj[l] = np
                        if np in childj:
                            childj[np].append(l)
                        else:
                            childj[np] = [l]
                    l+= 1
                  result.append((potenj,(hypj,parj,childj,ordenj)))
            l=0
            potenj = []
            ordenj=[]
            hypj = []
            childj = dict()
            parj = dict()
            desc = []
            for x in range(len(orden)):
                    if not x in tdesc:
                        desc.append(x)
            
            if desc:
                for k in desc:
                    ordenj.append(orden[k])
                    potenj.append(poten[k])
                    
                
                    hypj.append(hyp[k])
                    if k in par:
                        np = desc.index(par[k])
                        parj[l] = np
                        if np in childj:
                            childj[np].append(l)
                        else:
                            childj[np] = [l]
                    l+= 1
                return result +  update(potenj,(hypj,parj,childj,ordenj),valores)
            else:
                return result
    return [(poten,(hyp,par,child,orden))]
        
       
    
    

def restringeyparte(variable,contra,poten,trian):
    orden = trian[3]
    child=trian[2]
    hyp = trian[0]
    par = trian[1]
    
    i = len(orden)-1
    
    npot = poten[i].restringe(variable)
    
    if npot.contradict:
        contra[0] = True
        return []
    result = []
    for j in child[i]:
        l=0
        potenj = []
        ordenj=[]
        hypj = []
        childj = dict()
        parj = dict()
        
        desc = cdesc(j,child)
        
        
        
        for k in desc:
            ordenj.append(orden[k])
            npot = poten[k].restringe(variable)
            potenj.append(npot)
            if npot.contradict:
                contra[0] = True
                return []
                
            hypj.append(hyp[k]-{abs(variable)})
            if not k == j:
                np = desc.index(par[k])
                parj[l] = np
                if np in childj:
                    childj[np].append(l)
                else:
                    childj[np] = [l]
            l+= 1
        result.append((potenj,(hypj,parj,childj,ordenj)))
    
    return result
 
def backtracking(contra,poten,trian, unit=True):
    
        if contra[0]:
            return []
        hyp = trian[0]
        par = trian[1]
        chil = trian[2]
        orden = trian[3]
    
        print("bct",len(orden))
#        print(hyp)
#        print(par)
        
        if unit:
            valores = propagaunit(trian,poten,contra)
            solucion = list(valores)
            if contra[0]:
                
                return []
            contra1 = [False]
            if valores:
                print(valores)
                formulas = update(poten,trian,valores)
                print(len(formulas))
                for x in formulas:
                    poten1 = x[0]
                    trian1 = x[1]
                    contra1 = [False]
        
                    solucion1 = backtracking(contra1,poten1,trian1,False)
                    if contra1[0]:

                        break
                    else:
                        solucion = solucion + solucion1
            
        
                if not contra1[0]:
                    return solucion 
                else:
                    contra[0] = True
                    return []
         
#            if valores:
#                print("units", valores)
        

#        propagaprox(trian,poten,contra)
         
#        print(listae)
#        formula.poda()
        if contra[0]:
            return []
        
        if len(orden)==1:
            var = orden[0]
            if  not frozenset({-var}) in poten[0].listaclaus:
                return [var]
            elif not frozenset({var}) in poten[0].listaclaus:
                return [-var]
            else:
                contra = [True]
                return []
        
        variable = obtenerVariable(poten,trian)
    
    
#        formula.limpia(0.0)
        
        
        formulas = restringeyparte(variable,contra,poten,trian)
        solucion = [variable]
        if contra[0]:
            return []
        for x in formulas:
            poten1 = x[0]
            trian1 = x[1]
            contra1 = [False]
        
            solucion1 = backtracking(contra1,poten1,trian1,True)
            if contra1[0]:

                break
            else:
                solucion = solucion + solucion1
            
        
        if not contra1[0]:
            return solucion
        
        formulas = restringeyparte(-variable,contra,poten,trian)
        solucion = [-variable]
        if contra[0]:
            return []
        for x in formulas:
            poten1 = x[0]
            trian1 = x[1]
            contra1 = [False]
        
            solucion1 = backtracking(contra1,poten1,trian1,True)
            if contra1[0]:

                break
            else:
                solucion = solucion + solucion1
            
            
         
        if not contra1[0]:  
            return solucion
        else:
            contra[0] = True
            return []
    

    
  
    

                   
def propagaunit(trian,poten,contra):
    unitsg= set()
    unitst = set()
    for pot in poten:
        unitsg.update(pot.unitprev)
    while unitsg:
        p = unitsg.pop()
        unitst.add(p)
        for pot in poten:
            if abs(p) in pot.listavar:
                pot.unitprev.discard(p)
                if p in pot.indices:
                    borrar = set()
                    for c in pot.indices[p]:
                    
                        borrar.add(c)
                
                    pot.indices.pop(p)
                        
                    for c in borrar:
                        pot.eliminar(c)
            if -p in pot.indices:
                borrar = set()
                for c in pot.indices[-p]:
                    borrar.add(c)
                            
                pot.indices.pop(-p)

                for c in borrar:
                    pot.eliminar(c)
                    c2 = frozenset(set(c)-{-p})
#                    self.refer[c2] = self.refer.get(c,set()).union(self.refer.get(frozenset({p}),set()))
                    if(not c2):
                        pot.contradict = True
                        pot.solved = True
                        contra[0] = True     
#                            self.apren = self.refer[c2]
                        return unitst
                    pot.insertar(c2)
                    if (len(c2)==1):
                        h = set(c2).pop()
                        unitsg.add(h)
                        pot.unit.add(h)
            pot.listavar.discard(abs(p))
        
    return unitst
                         
        
               
              
      
 
def triangula(grafo):
    
    hypernodes = []
    parents = dict()
    children = dict()
    orden = []
    
    
    while grafo.nodes:
        nnodo = min(grafo.nodes,key = grafo.degree)
        orden.append(nnodo)
        
        veci = set(grafo[nnodo])
        hnodo = (veci.union({nnodo}))
        hypernodes.append(hnodo)
        
        grafo.remove_node(nnodo)
        for x in veci:
            for y in veci:
                if not x==y:
                    grafo.add_edge(x,y)
                    
                    
    for i in range(len(orden)-1):
        x = orden[i]
        y = hypernodes[i]
        z = y-{x}
        for j in range(i+1,len(orden)):
            if z <= hypernodes[j]:
                parents[i]= j
                if j in children:
                    children[j].append(i)
                else:
                    children[j] = [i]
                break
            
                    
    return (hypernodes,parents,children,orden)
        

def inicializa(formula,trian):
    
    hyp = trian[0]
    par = trian[1]
    chil = trian[2]
    orden = trian[3]
    
    poten = []
    
    for i in range(len(orden)):
        var = orden[i]
        poten.append(globalClausulas())
        borrar=[]
        pos = formula.indices.get(var,set())
        for cl in pos:
            poten[i].insertar(cl)
            borrar.append(cl)
        neg = formula.indices.get(-var,set())
        for cl in neg:
            poten[i].insertar(cl)
            borrar.append(cl)
        for cl in borrar:
            formula.eliminar(cl)
    return poten

def propagaprox(trian,poten,contra,L=4):
    
#    print("comienzo propagacion arriba")
    propagaup(trian,poten,contra,L)
#    print("comienzo propagacion abajo")
    propagadown(trian,poten,contra,L)
    
    
def propagaup(trian,poten,contra,L=6):
    hyp = trian[0]
    par = trian[1]
    chil = trian[2]
    orden = trian[3]
    
    
    for i in range(len(orden)-1):
        var = orden[i]
        total = poten[i]
        if var in hyp[i]:
            margin = total.marginalizaprox(var,L)
        else:
            margin = total
        if margin.contradict:
#            print("contradiccion")
            contra[0] = True
            return
        destino = poten[par[i]]
        
        for cl in margin.listaclaus:
            destino.insertar(cl)
            
def limpia(poten):
    for i in poten:
        print("l " ,len(poten[i].listaclaus))

        poten[i].poda()
        print("dl " ,len(poten[i].listaclaus))

        print(i)
#        poten[i].limpia2()
        
    
        
def propagadown(trian,poten,contra,L=20):
    hyp = trian[0]
    par = trian[1]
    chil = trian[2]
    orden = trian[3]
    
    
    for i in range(len(orden)-1,1,-1):
        
        total = poten[i]
        hijos = chil.get(i,[])
        origen = hyp[i]
        margin = total
        for j in hijos:
            destino = hyp[j]
            dif = origen-destino
            for v in dif:
                margin = margin.marginalizaprox(v,L)
                if margin.contradict:
                    contra[0] = True
                    return
        
    
            
        
        
            for cl in margin.listaclaus:
                poten[j].insertar(cl)
        
        
        

def main(info):
        
        info.unitprop()
#        info.calculadep()
#        print("salgo de explora")
#        info.equivprop()degrr
        
#        self.conjuntoclau.satura()
#        info.satura2()
#        print(info.unit)      
        

        solucion = list(info.unit)

#        lista = info.equivprop()   
        
        if info.contradict:
                        configura = []
                        print("Inconsistente")
                        return
        
#        explora(info)

        info.poda()

        grafo = info.cgrafo()
        trian = triangula(grafo)
        
        poten = inicializa(info,trian)
        
        
#        print(lista)
       
#        todas = info.calculartodasbloqueadas()
#        print ("bloqueadas",todas)
        
        contra = [False]
        
#        propagaprox(trian,poten,contra)
            
        if contra[0]:
            configura = []
            print("Inconsistente")
        else:

            configura = backtracking(contra,poten,trian)
        
        if contra[0]:
            configura = []
            print("Inconsistente")
            
        else:
            
#            for (l1,l2) in lista:
#                if l1 in configura:
#                    configura.append(l2)
#                elif -l1 in configura:
#                    configura.append(-l2)
            configura = solucion + configura
            print("Consistente", len(configura),configura)
        
  
ttotal = 0
i = 0
reader=open('entrada',"r")

while reader:
    nombre = reader.readline().rstrip()             
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

    main(info)
    
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
    ttotal += t2-t1

print ("tiempo medio ", ttotal/i)