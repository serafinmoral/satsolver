# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 20:13:39 2021

@author: efrai
"""

import time

from arboldoblesinvar import *
from SimpleClausulas import *

class problemaTrianArbol:
    def __init__(self,info,N=100):
         self.N = N
         self.inicial = info
         self.orden = []
         self.clusters = []
         self.lpot = []
         self.lqueue  = []
         self.lqp = []
         self.lqn = []
         self.posvar = dict()
         self.sol = set()

    def inicia0(self):
            for i in self.orden:
                x = arboldoble()
                self.lpot.append(x)
                y = arboldoble()
                self.lqueue.append(y)
    
            for v in self.inicial.unit:
                self.insertacolaclau2({v})
            for cl in self.inicial.listaclaus:
                self.insertacolaclau2(cl)
            for pot in self.lqueue:
                pot.normaliza(self.N)
                
    def insertacolaclau2(self,cl):
        if not cl:
            self.anula()
        else:
            vars = set(map(lambda x:abs(x),cl))
            for pos in range(len(self.clusters)):
                if vars <= self.clusters[pos]:
                    break
            pot = self.lqueue[pos]
            pot.insertaclau(cl)

    def borra(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            if i==1336:
                print("parada")
            if pot.value.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            print("entro en normaliza")
            # if pot.checkrep():
            #     print("proeblma de repeticion antes de normalizar")
            pot.normaliza(self.N) 
            if pot.value.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion después de normalizar ")
                break
            print("entro en split")
            # if pot.checkrep():
            #     print("proeblma de repeticion")
            (t0,t1,t2) = pot.splitborra(var)
            
            

            self.lqp.append(t1)
            self.lqn.append(t0)
            print("ntro en combinaborra")
            res1 = t0.combinaborra(t1,self.N)

            print("inserto t2")
            self.insertacola(t2,i)
            res1.normaliza(self.N)

            if res1.value.contradict:
                print("contradiccion en resultado")
            pot.void()
            print("Ahora inserto en la cola")
            self.insertacola(res1,i)
            
    def findsol(self):
        sol = set()
        for i in reversed(range(len(self.orden))):
            pos = self.lqp[i].copia()
            neg = self.lqn[i].copia()
            neg.simplificaunits(sol)
            pos.simplificaunits(sol)
            
            pos.normaliza(N=1000)
            neg.normaliza(N=1000)

            poss = pos.tosimple()
            negg = neg.tosimple()
            var = self.orden[i]
            print("i= ",i)
            if not poss.contradict:
                sol.add(var)
                print(var)
            elif not negg.contradict:
                sol.add(-var)
                print(-var)
            else:
                print("contradiccion buscando solucion" , sol )
                self.lqp[i].imprime()
                self.lqn[i].imprime()
                break
        self.sol = sol
        return sol
    
    def compruebaSol(self):
        aux = 0
        for clau in self.inicial.listaclausOriginal:
            aux = aux + 1
            if len(clau.intersection(self.sol))==0:
                print("Error en cláusula: ", clau)
                return False
        print("Cumple solución satisfactoriamente, Número de cláusulas validadas: ", aux)
        return True
    
    def insertacola(self,t,i,conf=set()):
        if not t.value.nulo():
                if t.value.contradict and not conf:
                    self.problemacontradict()
                else:
                    j = i+1
                    vars = set(map(lambda x: abs(x),conf.union(t.value.listavar)) )
                    while not vars <= self.clusters[j]:
                        j += 1
                        if j == len(self.clusters):
                            print(vars)
                    
                    pot = self.lqueue[j]
                    # if pot.checkrep():
                    #     print("problema de repecion antes de insertar")
                    #     time.sleep(30)
                    if pot.value.contradict:
                        print("contradiccion antes")

                    pot.insertasimple(t.value,self.N,conf) 
                    # if pot.checkrep():
                    #     print("problema de repecion despyes de insertar",conf)
                    #     time.sleep(30)

                    pot.normaliza(self.N) 
        if not t.var ==0:
            v = t.var
            conf.add(v)
            self.insertacola(t.hijos[0],i,conf)
            conf.discard(v)
            conf.add(-v)
            self.insertacola(t.hijos[1],i,conf)
            conf.discard(-v)
            
    def problemacontradict(self):
        print("contradiccion")
        self.inicial.solved = True
        self.inicial.contradict = True
        
    def anula(self):
        self.inicial.solved = True
        self.inicial.contradict = True
        for pot in self.lpot:
            pot.anula()
        for por in self.lqueue:
            pot.anula()