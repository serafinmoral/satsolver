# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os
import itertools   
from comunes import *
from GlobalClausulas import *
from time import time


class grupo:
    def __init__(self):
        self.incon = False
        self.vars = set()
        self.clausulas = set()
        
    def computefromSat(self,eleme):
        self.vars = eleme.listavar
        self.clausulas = eleme.listaclaus
    
    def selectconfig(self,config):
        h = grupo()
        h.vars = self.vars - set(map(lambda x: abs(x),config))
        for x in self.clausulas:
            z = reduce(x,config)
            if not 0 in z:
                h.clausulas.add(z)
            if len(z) == 0:
                h.clausulas = {z}
                return h
                self.incon = True
        return h
    
    def calculaprobv(self,z):
        if self.incon:
            return 0
        nct = 2**(len(self.vars)-1)
        exclu = 0
        for x in self.clausulas:
            if not z in x:
                if -z in x:
                    exclu += 2**(len(self.vars)-len(x))
                else:
                    exclu += 2**(len(self.vars)-len(x)-1)
        prob = (nct-exclu)/nct
        return prob
    
    def calculaprob(self):
        nct = 2**(len(self.vars))
        exclu = 0
        for x in self.clausulas:
            exclu +=  2**(len(self.vars)-len(x))
        prob = (nct-exclu)/nct
        return prob
    
    def eliminar(self,cl):
        self.clausulas.discard(cl)
    
    def anadir(self,cl):
        clneg = set(map(lambda x: -x,cl))
        quitar = set()
        for cl2 in self.clausulas:
            if cl2 <= cl:
                return
            elif cl<= cl2:
                quitar.add(cl2)
            else:
                if not clneg.intersection(cl2):
                    h = cl2-cl
                    t = set(h).pop()
                    for x in quitar:
                        self.clausulas.discard(x)
                    self.anadir(cl.union({t}))
                    self.anadir(cl.union({-t}))
                    
                    return
        for x in quitar:
            self.clausulas.discard(x)
        self.vars.update(set(map(lambda x: abs(x), cl)))
        self.clausulas.add(cl)
    
    def copia(self):
        nuevo = grupo()
        nuevo.incon = self.incon 
        nuevo.vars = self.vars.copy() 
        nuevo.clausulas = self.clausulas.copy()
        return nuevo
    
    def combina(self,gr):
        if len(self.clausulas) <= len(gr.clausulas):
            gr1 = gr.copia()
            gr2 = self
        else:                           
            gr1 = self.copia()
            gr2 = gr
        for cl in gr2.clausulas:
            gr1.anadir(cl)
        return gr1
    
    def parcialcombina(self,gr,valores):
        eli = []   
        for cl in gr.clausulas:
            if (not cl.intersection(valores)):
                self.anadir(cl)
                eli.append(cl)
        for cl in eli:
            gr.eliminar(cl)
                
class solveSATGrupos:    
    def __init__(self,x):
        self.method = 0
        self.limit = 0
        self.solucion = False
        self.solved = False    
        self.varinorder = dict()
        self.posorder = dict()
        self.conjuntoclau = x
        self.ordenbo = []
        self.configura = []
        self.conjuntopotentials = []
        self.conjuntogrupos = []
        self.indicesgrupos = dict()
        self.potentialsborrado = dict() 
        self.potentialcombinat = dict()
        self.originalpotentials = []
        self.bloqueadas = set()
        self.totaloriginal = x
    
    def inicia(self):
        print(len(self.conjuntoclau.listaclaus))
        self.conjuntoclau.unitprop()
        t1 = time()
        self.conjuntoclau.podaylimpia() 
        t2 = time()
        print("Tiempo " , t2-t1)
        self.solved = self.conjuntoclau.solved
        self.solucion = self.conjuntoclau.solution
        (self.ordenbo,self.varinorder,self.conjuntosvar) = self.conjuntoclau.computeOrder()
        print("fin de calculo de orden")
        self.totaloriginal = self.conjuntoclau.copia()
        self.extraegrupos()
        self.combinagrupos2()
        self.conjuntopotentials = self.conjuntoclau.extraePotentials(self.ordenbo)
        
    def combinagrupos2(self,M=4):
     i=0
     j=i+1
     while j < len(self.conjuntogrupos):
         gr1 = self.conjuntogrupos[i]
         gr2 = self.conjuntogrupos[j]
         co1 = gr1.vars
         co2 = gr2.vars
         inter = co1.intersection(co2)
         union = co1.union(co2)
         if (inter and len(gr1.clausulas)<=M and len(gr2.clausulas)<=M):
             if (len(union-co1)<=3) or (len(union-co2)<=3):
                 gr = gr1.combina(gr2)
                 self.borragrupo(gr1)
                 self.borragrupo(gr2)
                 self.insertagrupo(gr)
             else:
                 j+=1
                 if(j>=len(self.conjuntogrupos)):
                     i+=1
                     j = i+1
         else:
          j+=1
          if(j>=len(self.conjuntogrupos)):
              i+=1
              j = i+1  

    def extraegrupos(self):
        while (len(self.totaloriginal.listaclaus)>0):
            g = grupo()
            eleme = globalClausulas()
            claus = next(iter(self.totaloriginal.listaclaus))
            eleme.insertar(claus)
            self.totaloriginal.eliminar(claus)
            lista = self.totaloriginal.entorno(claus)
            while lista:
                h = lista.pop()
                eleme.insertar(h)
                self.totaloriginal.eliminar(h)
                lista.intersection_update(self.totaloriginal.entorno(h))
            g.computefromSat(eleme)
            self.insertagrupo(g)
            
    def insertagrupo(self,t):
        self.conjuntogrupos.append(t)
        for var in t.vars:
            if var in self.indicesgrupos:
                self.indicesgrupos[var].add(t)
            else:
                self.indicesgrupos[var] = {t}

    def borragrupo(self,t):
        self.conjuntogrupos.remove(t)
        for var in t.vars:
            self.indicesgrupos[var].discard(t)

    def compruebasol(self):
        correcto = True
        if self.solved and self.solucion:
            for h in self.originalpotentials:
                for y in h.listaclaus:
                    t = reduce(y,self.configura)
                    if len(t)== 0:
                        print("solucion no valida ")
                        print(self.configura)
                        print("clausula ",y)
                        correcto = False
                        break
        if correcto:
            print("Solucion Correcta")
    
    def borra(self):
        current=1
        print (self.conjuntoclau.listavar)
        nvar = len(self.ordenbo)
        total = 0
        while current<= nvar  and not self.solved:
            varb = self.ordenbo[current-1]
            current = current +1
            listapotv = calculapotentials(self.conjuntopotentials,varb)
            self.potentialsborrado[varb] = listapotv
            pot = globalClausulas()
            for p2 in listapotv:
                pot.combina(p2)
            self.potentialcombinat[varb] = pot

    def calculavalor(self,valores,var):
        pot = self.potentialcombinat[abs(var)]
        negativos = set(map(lambda x: -x,valores))
        if var in pot.indices:
            for x in pot.indices[var]:
                if ((x-{var})<=negativos):
                    return [True,x]
        return [False]
    
    def busca(self):
        valores = set()
        print(self.ordenbo)
        n = len(self.ordenbo)
        current = n-1
        minc = current
        nnodos = 0
        while not (self.solved):
            nnodos += 1
            var = self.ordenbo[current]
            if (current < minc):
                print (current)
                minc = current
            varpos = self.calculavalor(valores,var)
            varneg = self.calculavalor(valores,-var)
            if (varpos[0] and varneg[0]):
                clau1 = varpos[1]
                clau2 = varneg[1]
                claures = resolution(var,clau1,clau2)
                if(len(claures)==0):
                    self.solved = True
                    self.solucion = False
                imin = n-1
                for y in claures:
                    z = abs(y)
                    pos = self.varinorder[z]
                    if (pos<imin):
                        imin = pos
                varmin = self.ordenbo[imin]
                self.potentialcombinat[varmin].insertar(claures)
                self.totaloriginal.insertar(claures)
                for j in range(current+1,imin+1):
                    valores.discard(self.ordenbo[j])
                    valores.discard(-self.ordenbo[j])
                current = imin
                
            elif varpos[0] and not varneg[0]:
                current -= 1
                valores.add(var)
            elif varneg[0] and not varpos[0]:
                current -= 1
                valores.add(-var)
            else:
                xpos = 1.0
                xneg = 1.0
                bneg = False
                bpos = False
                
                for x in self.indicesgrupos[var]:
                    grupo = x.selectconfig(valores)
                    if(xpos>0):
                        t1 = grupo.calculaprobv(var)
                    if(xneg>0):
                        t2 = grupo.calculaprobv(-var)
                    if (t1==0) and not bpos:
                        gr1 = x
                        bpos = True
                    if (t2==0) and not bneg:
                        gr2 = x
                        bneg = True
                    xpos *= t1
                    xneg *= t2    
                    if (xpos==0) and (xneg==0):
                        break
                    
                if (xpos==0) and (xneg==0) and not (gr1==gr2):
                    self.borragrupo(gr1)
                    self.borragrupo(gr2)
                    gr1.parcialcombina(gr2,valores)
                    self.insertagrupo(gr1)
                    self.insertagrupo(gr2)
                    print("dos negativos")
                    if(gr1.calculaprob()==0):
                        self.solved = True
                        self.solucion = False
                    else:
                        imin = n-1
                    for y in gr1.vars:
                    
                        pos = self.varinorder[z]
                        if (pos<imin):
                            imin = pos
                    for j in range(current+1,imin+1):
                            valores.discard(self.ordenbo[j])
                            valores.discard(-self.ordenbo[j])
                    current = imin
                else:    
                    current-= 1
                    if (xpos>xneg):
                         valores.add(var)
                    else:
                        valores.add(-var)
            if (current == -1):
                self.solved = True
                self.solucion = True
                self.configura = valores
        print("N. nodos ", nnodos)
    
#Instrucciones iniciales
t1 = time()
ttotal = 0
i = 0
reader=open('entrada',"r")
for cad in reader:
    nombre = cad.rstrip()             
    t1 = time()
    i +=1
    info = leeArchivoGlobal(nombre)
    t2= time()
    problema = solveSATGrupos(info)
    problema.inicia()
    t3 = time()
    problema.borra()
    t4 = time()
    problema.busca()
    t5 = time()
    problema.compruebasol()
    info2 = leeArchivoGlobal(nombre)
    info2.compruebasol(problema.configura)
    print(problema.configura)
    print("tiempo lectura ",t2-t1)
    print("tiempo inicio ",t3-t2)
    print("tiempo borrado ",t4-t3)
    print("tiempo busqueda ",t5-t4)
    print("tiempo TOTAL ",t5-t1)
    ttotal += t5-t1

print ("tiempo medio ", ttotal/i)
