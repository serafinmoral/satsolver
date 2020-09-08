# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os
import sys

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
    
def expandesol(sol,nuevas,listas,listae):
    while nuevas:
        v = nuevas.pop()
        encuentravalor(v,listas,sol)
    for (l1,l2) in reversed(listae):
        if l1 in sol and l2 not in sol:
            sol.append(l2)
        elif -l1 in sol and -l2 not in sol:
            sol.append(-l2)       
 
def backtracking(formula,tapren,path,N1,N2,N3,NI):
    
    
#        test = frozenset({-100, -143, -110, -140, -107, -36})    
#        if test in formula.listaclaus:
#            print("formula test !")
#        print("ba",len(formula.listavar))
        
        NI[0] -=1
        if NI[0]==0:
            return []
    
        if formula.contradict:
#            print("inconsistencia primaria")
#            if 0 in formula.apren:
#                print("no aprendo")
#                sys.exit()

            return []
#        print(formula.listaclaus)
        if (NI[0]%200==0):
            print(path)
#        formulac = formula.copia()
#        old = len(formula.listavar)
#        explora(formula)
#        print(len(asignaciones))
#        explora(formula)
#        formula, pure_assignment = pure_literal(formula)
#        print("backtracking ", len(formula.listavar)"bcormula.contradict)
#        if len(formula.listavar)==0:
#            if formula.contradict:
#                print("OKOKOKOKOKOKOKOKOOK")
#            else:
#                print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        formula.propagacion_unitaria()
#        print(formula.unit)
        if formula.contradict:
            tapren.insertar(frozenset(formula.apren))
#            print("primera unitaria ",formula.apren)
            if not formula.apren:
                    print("unitaria primaria ")
#            papren =set( map(abs,formula.apren))
#            ppath = set( map(abs,path))
#            if  not papren <=ppath :
#                print("Aprendida no valida " )
#                sys.exit()
            return []
#        print("unitarias " ,len(formula.unit))
#        if (test in formula.listaclaus):
#            print("formula test ! despues de propagacion unitaria")
        listae = formula.equivprop()
#        print("equivalencias ", len(listae))
#        if (test in formula.listaclaus):
#            print("formula test ! despues de equivalencias")
#        print(listae)
#        formula.poda()
        if formula.contradict:
            tapren.insertar(frozenset(formula.apren))
            if not formula.apren:
                    print("inconsistencia equivalencia ")

#            print(" equivalencias ",formula.apren)
#            papren =set( map(abs,formula.apren))
#            ppath = set( map(abs,path))
#            if  not papren <=ppath :
#                print("Aprendida no valida " )
#                sys.exit()
            return []
#            print("inconsistencia equivalencia", tapren)
#            if 0 in formula.apren:
#                print("no aprendo")
#                sys.exit()

        asignaciones = list(formula.unit)
#        print("unitarias", len (asignaciones))
        listas = dict()
        nuevas = formula.borraexactolim(listas,M=N3)
        
#        print("borradas ", nuevas)
        
        if formula.contradict:
#            print("inconsistencia borrado", tapren)
#            if 0 in formula.apren:
#                print("no aprendo")
#                sys.exit()
            
#            print("borrar ", formula.apren)
#            papren =set( map(abs,formula.apren))
#            ppath = set( map(abs,path))
#            if  not papren <=ppath :
#                print("Aprendida no valida " )
#                sys.exit()
            if not formula.apren:
                    print("inconsistencia borrado exacto")
            tapren.insertar(frozenset(formula.apren))
            return [] 
#        if (test in formula.listaclaus):
#            print("formula test ! despues de borrado")
#        print("borradas ", len(nuevas))
        
        if not formula.listaclaus:
            for v in formula.listavar:
                asignaciones.append(v)
#                print("añado ", v , " a solucion por no clausulas ")
            expandesol(asignaciones,nuevas,listas,listae)
#            print("solucion ", asignaciones)
            formula.compruebasol2(asignaciones)

                
            formula.solved = True
            formula.contradict = False
#            print("resuelto devuelvo ",asignaciones)
            return asignaciones
            
        
        variable = obtenerVariable3d(formula,N1,N2)
        if formula.contradict:
            tapren.insertar(frozenset(formula.apren))

            if not formula.apren:
                print("inconsistencia al obtener variable ")
#            papren =set( map(abs,formula.apren))
#            ppath = set( map(abs,path))
#            if  not papren <=ppath :
#                print("Aprendida no valida " , variable)
#                sys.exit()
            return []
        asignaciones = list(formula.unit)

        
        while formula.unitprev:
            formula.unitprop()
            if formula.contradict:
                tapren.insertar(frozenset(formula.apren))
                if not formula.apren:
                    print("inconsistencia propagacion unitaria ")
#            print(" obtener variable ", formula.apren)
#
#            papren =set( map(abs,formula.apren))
#            ppath = set( map(abs,path))
#            if  not papren <=ppath :
#                print("Aprendida no valida " , variable)
#                sys.exit()
                return []
            asignaciones = list(formula.unit)
            if not formula.listaclaus:
                for v in formula.listavar:
                    asignaciones.append(v)
#                    print("añado ", v , " a solucion por no clausulas ")
                expandesol(asignaciones,nuevas,listas,listae)
#                print("solucion ", asignaciones)
                formula.compruebasol2(asignaciones)

                
                formula.solved = True
#            print("resuelto devuelvo ",asignaciones)
                return asignaciones
            
            
            variable = obtenerVariable3d(formula,N1,N2)
            if formula.contradict:
                tapren.insertar(frozenset(formula.apren))
                if not formula.apren:
                    print("inconsistencia obtener variable ", formula.apren)
#            print(" obtener variable ", formula.apren)
#
#            papren =set( map(abs,formula.apren))
#            ppath = set( map(abs,path))
#            if  not papren <=ppath :
#                print("Aprendida no valida " , variable)
#                sys.exit()
                return []

        
#        print(variable)
#        if (test in formula.listaclaus):
#            print("formula test ! despues de obtener variable")
#        formula.poda()
#        formula.limpia(0.0)
        
#        if formula.contradict:
#            tapren.append(formula.apren)
##            print("segunda contradiccion ", formula.apren)
##            papren =set( map(abs,formula.apren))
##            ppath = set( map(abs,path))
##            if  not papren <=ppath :
##                print("Aprendida no valida " )
##                sys.exit()
#
##            print("inconsistencia obtener variable", tapren)
##            if 0 in formula.apren:
##                print("no aprendo")
##                sys.exit()
#
#            return []
#        clau1 = 0
#        print('v ', variable)
#        if variable == 0:
#            return []
        formulas = formula.restringeyparte(variable)
        if(len(formulas)>1):
            print("particion",len(formula.listavar),len(formula.listaclaus))
        solucion = asignaciones + [variable]
        
        for formula1 in formulas:
            
            path.append(variable)
            solucion1 = backtracking(formula1,tapren,path,N1,N2,N3,NI)
            path.pop()
            
            
            if formula1.contradict or not formula1.solved:

                break
            elif formula1.solved:
#                if not formula1.compruebasol2(solucion1):
#                    print("problema en solucion")
##                    print(formula.listaclaus)
#                    print("var ",variable)
##                    print(formula1.listaclaus)
#                    sys.exit()
                solucion = solucion + solucion1
            
                
#        print("formula1 ", path, formula1.contradict, formula1.solved, formula1.apren)    
        
        if not formula1.contradict and formula1.solved:
#            print("solucion antes de expandir 1", solucion)
            expandesol(solucion,nuevas,listas,listae)
#            print("solucion despues de expandir 1", solucion)
            formula.compruebasol2(solucion)

#            print("solucion ",len(solucion),old,solucion)
#            if not formulac.compruebasol2(solucion):
#                    print("problema en solucion in situ",variable)
#            print("resuelto devuelvo 1", solucion)

            formula.solved = True
            return solucion
        else:
            posclau = set(map(abs,formula1.apren))
            if abs(variable) in posclau and NI[0]>0:
#                print("encuentro en nivel")
                npath = set(map( lambda x: -x, path))
                for cl in tapren.listaclaus:
                    cln =  reduce(cl,path)
                    clch = set(map(lambda x:-x,cl))
                    if 0 not in cln:
                        if cln:
                            formula.refer[cln] = cl.intersection(npath)
                            if len(cln) <= 2:
                                formula.insertaborraypoda2(cln)
                            else:
                                formula.insertar(cln)
                            if formula.contradict:
                                tapren.insertar(frozenset(formula.apren))
                                return []    
                        else:
                            formula.solved = True
                            formula.contradict = True
                            formula.apren = cl.intersection(npath)
                            tapren.insertar(formula.apren)
                            return []
                
                napren =globalClausulas()
                formula1 = formula.copia()
                solucion.pop()
#                print("llamo a backtracking" )
                sp = backtracking(formula1,napren,path,N1,N2,N3,NI)
                solucion = solucion + sp
                tapren.combina(napren)
                if not formula1.contradict and formula1.solved:
                    formula.solved = True
                    formula.contradict = False
#                    print("solucion antes de expandir 2 ", solucion)
                    expandesol(solucion,nuevas,listas,listae)
#                    print("solucion despues de expandir 2", solucion)

                    formula.compruebasol2(solucion)

#            print("solucion ",len(solucion),old,solucion)
#            if not formulac.compruebasol2(solucion):
#                    print("problema en solucion in situ",variable)
#                    print("resuelto devuelvo 2", solucion)
                    

                    return solucion
                else:
#                    print("primera llamada ",formula1.apren)

                    formula.apren = formula1.apren
                    formula.contradict = formula1.contradict
                    formula.solved = formula1.solved
#                    print("Salgo ",formula.contradict)

                    return []
            else:
#            tapren.append(formula1.apren)
                formula.solved = False
                formula.contradict = False
                formula.apren = formula1.apren
#                print("primera llamada no resuelto",formula.apren)

#                print("hacia atrás sin resolver aprendida 1", formula.apren, tapren)
#                if 0 in formula.apren:
#                    print("no aprendo")
#                    sys.exit()
                return []
#        else:
#           formula.solved = False
#           formula.contradict = False
#           formula.apren = formula1.apren
#           print("no variable ",formula.apren)

#           print("hacia atrás sin resolver 2",formula.apren, tapren)
#           if 0 in formula.apren:
#                print("no aprendo")
#                sys.exit()

#           return [] 
                        
                
            
            
#        
#        
#        
#        formulas = formula.restringeyparte(-variable)
#        if(len(formulas)>1):
#            print("particion",len(formula.listavar),len(formula.listaclaus))
#        solucion = asignaciones+ [-variable]
#        
#        for formula2 in formulas:
#            path.append(-variable)
#
#            solucion2 = backtracking(formula2,tapren,path)
#            path.pop()
#            if formula2.contradict:
#
#                break
#            else:
##                if not formula2.compruebasol2(solucion2):
##                    print("problema en solucion")
###                    print(formula.listaclaus)
##                    print("var ",-variable)
###                    print(formula2.listaclaus)
##                    sys.exit()
#
#                solucion = solucion + solucion2
#            
#            
#         
#        if not formula2.contradict:  
#            while nuevas:
#                v = nuevas.pop()
#                encuentravalor(v,listas,solucion)
#            for (l1,l2) in reversed(listae):
#                if l1 in solucion and l2 not in solucion:
#                   
#                    solucion.append(l2)
#                elif -l1 in solucion and -l2 not in solucion:
#                   
#                    solucion.append(-l2)
#            
##            print("solucion ",len(solucion),old,solucion)  
#           
##            if not formulac.compruebasol2(solucion):
##                    print("problema en solucion in situ", -variable)
#            return solucion
#        formula.contradict=True
#        return []
#    

 
        
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
      
def asignarandom(formula):
        configura = set()
        for v in formula.listavar:
            x = choice((v,-v))
            configura.add(x)
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
         
    



def explorai(formula,configura,ins = False):
    
    
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
    
    if ins:      
       for cl in nuevas:
        if not cl:
            formula.solved = True
            formula.contradict = True
            return
        if len(cl)<= 2:
            formula.insertaborraypoda2(cl)
        else:
            formula.insertar(cl)


def explorai2(formula,configura,ins=False):
    
    
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
    if ins:      
      for cl in nuevas:
        if not cl:
            formula.solved = True
            formula.contradict = True
            return
        
        if len(cl)<= 2:
            formula.insertaborraypoda2(cl)
        else:
            formula.insertar(cl)
                   

                    
                                
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
  
               
    
    
    
def obtenerVariable3d(formula,N1,N2):
#        print("inicio")
        vmax = 0
        best = 0
        listaarbol = []
        for v in formula.listavar:
            l1 = len(formula.indices.get(v,set()))
            l2 = len(formula.indices.get(-v,set()))
            if l1*l2 > best:
                best = l1*l2
                vmax = v
#                
        
        r = formula.copia()

        
        lista1 = formula.indices.get(v,set())
        lista2 = formula.indices.get(-v,set())
        
        
        
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
               

  
def computedep(formula):
    lista = list(formula.listavar)
    dep = dict()
    for i in range(len(lista)):
        for j in range(i+1,len(lista)):
            dep[(i,j)] = 0.0
            v1 = lista[i]
            v2 = lista[j]
            l1 = formula.indices.get(v1,set()).union(formula.indices.get(v1,set()))
            l2 = formula.indices.get(v1,set()).union(formula.indices.get(v1,set()))
            lf = l1.intersection(l2)
            for cl in lf:
                dep[(i,j)] += 1/2**(len(cl)-1)
                
    return dep
        
def computeest(formula, ins = True  , T = 100):
    
    count = dict()
    for v in formula.listavar:
        count[v] = 0
    for i in range(T):
        config = asignarandom(formula)
        explorai(formula,config,ins)
        explorai2(formula,config,ins)
        for v in config:
            if v>0:
                    count[v]  += 1
              
    for v in count:
        count[v] = count[v]/T
        
    return count
         
    
def main(info,N1,N2,N3,I):
        

    
    
    #        info.calculadep()
#        print("salgo de explora")
#        info.equivprop()
        
#        self.conjuntoclau.satura()
# mbmb mbmbmbbbbbbhjjguy
#       info.satura2()
#        print(info.unit)      
        
        info.unitprop()

        dep = computedep(info)
        
        tdep = dict()
        for i in range(len(info.listavar)):
            tdep[i] = 0.0
            for j in range(i):
                tdep[i] += dep[(j,i)]
            for j in range(i+1,len(info.listavar)):
                tdep[i] += dep[(i,j)]
            print(i,tdep[i])
            

        
        
#        print("fs ", info.cuenta(config))
        
#        print(config)


#        configr = asignagreedyr(info)
#        
#        print("fs ", info.cuenta(configr))
#        explorai(info,config)
#        explorai2(info,config)

#        explorai(info,config)
#        explorai2(info,config)
#        
# 
#        explorai(info,config)
#        explorai2(info,config)
        



#        print(config)
#        explorai(info,config)
#        explorai2(info,config)

#        explorai(info,configr)
#        explorai2(info,configr)
#        
 
        
  

#        explora(info)

        info.poda()

        lista = [2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 16, 17, 18, 21, 23, 24, 25, 30, 32, 33, 34, 36, 37, 39, 46, 49, 51, 52, 54, 55, 56, 58, 61, 65, 66, 67, 68, 69, 71, 74, 79, 84, 85, 86, 87, 88, 94, 97, 102, 104, 105, 107, 108, 109, 110, 112, 114, 115, 116, 117, 118, 121, 122, 125, 126, 128, 130, 132, 133, 138, 140, 141, 142, 145, 146, 147, 149, 151, 152, 153, 155, 159, 160, 161, 163, 167, 172, 173, 174, 175, 177, 178, 179, 180, 182, 185, 187, 190, 191, 192, 193, 196, 200, 201, 202, 207, 208, 209, 211, -300, -298, -297, 216, -295, -294, 219, 220, 221, 222, 223, -291, -287, -290, -285, 227, 228, -289, 232, -280, 235, -277, -275, -274, -273, 237, -271, 242, 244, 245, -266, 247, 248, -265, 250, 251, -261, -268, 254, -257, 255, -258, 256, 259, -253, 260, -252, 263, -249, 264, 262, 267, -246, 269, -243, -241, 272, -239, -240, 270, 276, -238, 278, 279, -233, -231, -230, 283, 284, 282, 286, -225, 288, -224, -226, -229, 292, 293, -218, -217, 296, -215, -214, -213, 299, -212, -210, -206, -205, -204, -203, -199, -198, -197, -195, -194, -189, -188, -186, -184, -183, -181, -176, -171, -170, -169, -168, -166, -165, -164, -236, -162, -158, -157, -156, -154, -234, -150, -148, -144, -143, -139, -137, -136, -135, -134, -131, -129, -127, -124, -123, 281, -120, -119, -113, -111, -106, -103, -101, -100, -99, -98, -96, -95, -93, -92, -91, -90, -89, -83, -82, -81, -80, -78, -77, -76, -75, -73, -72, -70, -64, -63, -62, -60, -59, -57, -53, -50, -48, -47, -45, -44, -43, -42, -41, -40, -38, -35, -31, -29, -28, -27, -26, -22, -20, -19, -15, -14, -10, -3, -1]
        
        
        for x in lista:
            if abs(x) in estadis:
                print(x,estadis[abs(x)])
                
        lista1 = []
        lista2 = []
        for x in lista:
            if abs(x) in estadis:
                if x>0:
                    lista1.append(estadis[abs(x)])
                else:
                    lista2.append(estadis[abs(x)])
        print("pos",sum(lista1)/len(lista1))
        print("neg",sum(lista2)/len(lista2))


#        print(lista)
       
#        todas = info.calculartodasbloqueadas()
#        print ("bloqueadas",todas)
        tapren = globalClausulas()
        path = []
        
        
        while not info.solved:
            NI = [I]
            info.unitprop()
#            print(info.unit)
            formula = info.copia()
            configura = backtracking(formula,tapren,path,N1,N2,N3,NI)   
            info.solved = formula.solved
            info.contradict = formula.contradict
            print("antes clausu ",len(tapren.listaclaus))

            tapren.poda()
            print("despues clausu ",len(tapren.listaclaus))   

            for cl in tapren.listaclaus:
                info.insertarc(frozenset(cl))
            tapren.anula()

            
        
        if info.contradict:
            configura = []
            print("Inconsistente")
            
        else:
            configura = configura+list(info.unit)
#            for (l1,l2) in lista:
#                if l1 in configura:
#                    configura.append(l2)
#                elif -l1 in configura:
#                    configura.append(-l2)
            info.compruebasol2(configura)
            print("Consistente", len(configura),configura)
        
  
ttotal = 0
i = 0



reader=open('entrada',"r")

writer=open('salida',"w")


#
#
#reader=open(sys.argv[1],"r")
#
#writer=open(sys.argv[2],"w")


while reader:
    linea = reader.readline().rstrip()  
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
    ttotal += t2-t1

print ("tiempo medio ", ttotal/i)
writer.write("tiempo medio " + str(ttotal/i)+"\n")
writer.close()
reader.close()

