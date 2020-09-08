# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""

         
from comunes import *  

from random import *
              

from time import time

from GlobalClausulas import *



def calculaprobv(grupo,z):
    
        lvar = set()
        if not grupo:
            return 1
        for x in grupo:
            va = set(map(abs,x))
            lvar.update(va)
        
   
        nct = 2**(len(lvar)-1)
        exclu = 0
        for x in grupo:
            
            if not z in x:
                if -z in x:
                    exclu += 2**(len(lvar)-len(x))
                else:
                    exclu += 2**(len(lvar)-len(x)-1)
#            elif z in x:
#                exclu += 0
#            else:
#                exclu += 2**(len(self.vars)-len(x)-1)
        prob = (nct-exclu)/nct
        
#        if (prob==0):
#            print (self.clausulas,z)
        
        return prob
    
def calculaprobdos(grupo,z,lvar):
    
  
   
        nct = 2**(len(lvar)-1)
        exclupos = 0
        excluneg = 0
        for x in grupo:
            
            if not z in x and not -z in x:
                exclupos += 2**(len(lvar)-len(x)-1)
                excluneg += 2**(len(lvar)-len(x)-1) 
            elif -z in x:
                exclupos += 2**(len(lvar)-len(x))
            else:
                excluneg += 2**(len(lvar)-len(x))
                
               
#                exclu += 0
#            else:
#                exclu += 2**(len(self.vars)-len(x)-1)
        probpos = (nct-exclupos)/nct
        probneg = (nct-excluneg)/nct

#        if (prob==0):
#            print (self.clausulas,z)
        
        return probpos,probneg   
    
def calculaprob(grupo):
        
        lvar = set()
        if not grupo:
            return 1
        for x in grupo:
            va = set(map(abs,x))
            lvar.update(va)
        
        nct = 2**(len(lvar))
        exclu = 0
        for x in grupo:
            exclu +=  2**(len(lvar)-len(x))
           
        prob = (nct-exclu)/nct
        
        return prob      

  
    
  
def propagacion_unitaria(formula):
    asignaciones = []
    clausula_unica=[]
    for grupo in formula:
#        print(grupo)
        lvar = set()
        for x in grupo:
            va = set(map(abs,x))
            lvar.update(va)
        for va in lvar:
            xpos,xneg = calculaprobdos(grupo,va,lvar)
            if xpos==0.0 and xneg==0.0:
                return -1, []
            elif xneg==0.0:
                clausula_unica=clausula_unica+[va]
                break
            elif xpos==0.0:
                clausula_unica=clausula_unica+[-va]
                break
            
    while clausula_unica:
        varUnica = clausula_unica[0]
#        if formula==-1:
#            print(formula)
        formula = bcp(formula, varUnica)
        asignaciones += [varUnica]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, asignaciones
        for grupo in formula:
 
            clausula_unica = []
            lvar = set()
            for x in grupo:
                va = set(map(abs,x))
                lvar.update(va)
            for va in lvar:
                xpos,xneg = calculaprobdos(grupo,va,lvar)
                if xpos==0.0 and xneg==0.0:
                    return -1, []
                elif xneg==0.0:
                    clausula_unica=clausula_unica+[va]
                    break
                elif xpos==0.0:
                    clausula_unica=clausula_unica+[-va]
                    break
            if clausula_unica:
                break
    return formula, asignaciones 


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
        for grupo in formula:
            ngrupo = []
            for clausula in grupo:
                if VarUnica in clausula:
                    continue
                if -VarUnica in clausula:
                    nueva_clause=[]
                    for x in clausula:
                        if x !=-VarUnica:
                            nueva_clause=nueva_clause+[x]
                    if not nueva_clause:
#                        print(grupo,VarUnica)
                        return -1
                    ngrupo.append(nueva_clause)
                else:
                    ngrupo.append(clausula)
            if ngrupo:
                modificado.append(ngrupo)
        return modificado
 
def backtracking(formula, asignaciones):
   
        print(len(asignaciones))
        
        formula, unit_assignment = propagacion_unitaria(formula)
        asignaciones = asignaciones+ unit_assignment
        if formula == - 1:
            return []
        if not formula:
            return asignaciones
        
        variable = obtenerVariable2(formula)
          
        
        
        solucion = backtracking(bcp(formula, variable), asignaciones+ [variable])
        if not solucion:
#            print("v",variable)
#            if (variable == -100):
#                print (formula)
#                print(bcp(formula, -variable))
            solucion = backtracking(bcp(formula, -variable), asignaciones + [-variable])
        return solucion
   
    
    
    
def obtenerVariable(formula):
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
        for grupo in formula:
            lvar = set()
            for x in grupo:
                va = set(map(abs,x))
                lvar.update(va)    
            for va in lvar:
                xpos,xneg = calculaprobdos(grupo,va,lvar)  
            if va in z:
                z[va]*= xpos
            else:
                z[va] = xpos
            if -va in z:
                z[-va]*= xneg
            else:
                z[-va] = xneg
                
        best=0
        nbest=0
        for i in z:
           if z[i]/z[-i]> best:
                    nbest = i
                    best = z[i]/z[-i]
        return nbest   
    
def extraegrupos(formula):
        result = []
        while (formula.listaclaus):
            eleme = []
            claus = next(iter(formula.listaclaus))
            formula.eliminar(claus)
            eleme.append(list(claus))
            formula.eliminar(claus)
            lista = formula.entorno(claus)
#            print (lista)
            while lista:
                h = lista.pop()
                eleme.append(list(h))
                formula.eliminar(h)
                lista.intersection_update(formula.entorno(h))
#            print (len(eleme.listaclaus))
            result.append(eleme)
        return result       
                    
    
class solveSATBackGrupos:    
    def __init__(self,x):
        self.method = 0
        self.solucion = False
        self.solved = False    
        
 
        self.configura = []
        self.nvar = 0
        self.formula = x
        self.grupos = []

        
    
    def main(self):
        
        self.grupos = extraegrupos(self.formula)
        self.configura = backtracking(self.grupos,[])
        print(self.configura)
        
  
ttotal = 0
i = 0
reader=open('entrada',"r")



while reader:
    nombre = reader.readline().rstrip()             
    i +=1
    t1 = time()
    info = leeArchivoGlobal(nombre)
    problema = solveSATBackGrupos(info)
    t2= time()



#info = leeArchivoSet('SAT_V144C560.cnf')

#print(info.listavar)

    

#print(problema.conjuntoclau.listavar)


    


    
#    problema.explora()

    t4 = time()
    

#problema.originalpotentials = problema.totaloriginal.extraePotentials(problema.ordenbo,problema.conjuntosvar)

    problema.main()
    
    t5 = time()



#info2 = leeArchivoGlobal('SAT_V1168C4675.cnf')
#info2 = leeArchivoGlobal('aes_32_1_keyfind_1.cnf')
#    info2 = leeArchivoGlobal(nombre)
#info2 = leeArchivoGlobal('SAT_V153C408.cnf')

#    info2.compruebasol(problema.configura)

    print("tiempo lectura ",t2-t1)
 
    print("tiempo busqueda ",t5-t4)

    print("tiempo TOTAL ",t5-t1)
    ttotal += t2-t1

print ("tiempo medio ", ttotal/i)