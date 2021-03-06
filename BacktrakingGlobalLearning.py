# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os

import itertools
         
from comunes import *  

from random import *
              
from GlobalClausulasLearning import *
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
 
def backtracking(formula, asignaciones):
   
#        print(len(asignaciones))
        
#        formula, pure_assignment = pure_literal(formula)
        formula.propagacion_unitaria()
        listae = formula.equivprop()

#        formula.poda()
        if formula.contradict:
            return []
        asignaciones = asignaciones+ list(formula.unit)
        listas = dict()
        nuevas = formula.borraexactolim(listas)
        if formula.contradict:
#            print("vuelta atras")
            return []
        if not formula.listaclaus:
            while nuevas:
                v = nuevas.pop()
                encuentravalor(v,listas,asignaciones)
            for (l1,l2) in reversed(listae):
                    if l1 in asignaciones and l2 not in asignaciones:
 
                        asignaciones.append(l2)
                    elif -l1 in asignaciones and -l2 not in asignaciones:
  
                        asignaciones.append(-l2)  
            return asignaciones
        
        variable = obtenerVariable3(formula)
        clau1 = 0
#        print('v ', variable)
        if variable == 0:
            return []
#        print("elijo ",variable)
        formula1 = formula.restringe(variable)
        solucion = backtracking(formula1, asignaciones+ [variable])
        formula.totalapren.update(formula1.totalapren)
        for cl in formula1.totalapren:
            formula.insertar(cl)
            
            
        if not formula1.contradict:
            while nuevas:
                v = nuevas.pop()
                encuentravalor(v,listas,solucion)
            for (l1,l2) in reversed(listae):
                if l1 in solucion and l2 not in solucion:
           
                    solucion.append(l2)
                elif -l1 in solucion and -l2 not in solucion:
                  
                    solucion.append(-l2)    
            return solucion
        elif not formula1.apren == 0:
#            print("formula aprendida",formula1.apren)
            clau1 = formula1.apren-{-variable}
            if -variable not in formula1.apren:
                formula.contradict=True
                formula.apren = formula1.apren

                return
            
            
#            print("Voy con ", -variable)
            formula2 = formula.restringe(-variable)
            formula2.incorpora(formula.totalapren, asignaciones + [-variable])
            solucion = backtracking(formula2, asignaciones + [-variable])
            formula.totalapren.update(formula2.totalapren)
            
        if not formula2.contradict:   
            while nuevas:
                v = nuevas.pop()
                encuentravalor(v,listas,solucion)
            for (l1,l2) in reversed(listae):
                if l1 in solucion and l2 not in solucion:
           
                    solucion.append(l2)
                elif -l1 in solucion and -l2 not in solucion:
                  
                    solucion.append(-l2)    
            return solucion
        formula.contradict=True
        if not formula2.apren == 0:
#            print("formula aprendida",formula2.apren)

            if variable not in formula2.apren:
                formula.apren=formula2.apren
            elif not clau1 == 0:
                nclau = clau1.union(formula2.apren)-{variable}
                formula.apren = nclau
                
#                print("formula aprendida",formula.apren)

        
   
    
def encuentravalor(v,listas,solucion):
    forp = False
    forn = False
    neg = set(map(lambda x: -x, solucion))
    if -v in listas:
        for x in listas[-v]:
            if ((x-{-v})<=neg):
                   forn = True
                   break
    if not forn:
        solucion.append(v)
        return
    
    if v in listas:
        for x in listas[v]:
            if ((x-{v})<=neg):
                   forp = True
                   break
               
    if not forp:
        solucion.append(-v)
        return 
    print("problema")
    return -1
                   
    
               
              
                   
     
       
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
        
    

                
def obtenerVariable3(formula):
        z = dict()
        for cla in formula.listaclaus:
            
            for x in cla:
                if x in z:
#                    z[-x] *= (2**(len(cla)-1)-1)/2**(len(cla)-1)
                    z[x] += 1
                    z[-x] -= (2**(len(cla)-1)-1)/2**(len(cla)-1)
                else:
#                     z[-x] = (2**(len(cla)-1)-1)/2**(len(cla)-1)
#                     z[x] = 1.0
                    z[x] =  1
                    z[-x] = - (2**(len(cla)-1)-1)/2**(len(cla)-1)
        
        
        best=1
        nbest=z[x]-z[-x]
        for i in z:
            
            if z[i] - z[-i]>= best:
                    nbest = i
                    best = z[i]-z[-i]
        return nbest   
        
    
    
class solveSATBack:    
    def __init__(self):
        self.method = 0
        self.limit = 0
        self.solucion = False
        self.solved = False    
        
        self.conjuntoclau = []
 
        self.configura = []
        self.nvar = 0
 

        
    
def main(info):
        
        info.unitprop()
#        info.equivprop()
        
#        self.conjuntoclau.satura()
        info.poda()
#        print(info.unit)         
        solucion = list(info.unit)
        
        lista = info.equivprop()
        explora(info)

#        print(lista)
       
#        todas = info.calculartodasbloqueadas()
#        print ("bloqueadas",todas)
        configura = backtracking(info,[])
        
        if info.contradict:
            configura = []
            print("Inconsistente")
            
        else:
            
            for (l1,l2) in lista:
                if l1 in configura:
                    configura.append(l2)
                elif -l1 in configura:
                    configura.append(-l2)
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