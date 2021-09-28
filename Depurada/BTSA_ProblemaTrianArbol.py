# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 20:02:59 2021

@author: efraín
"""
from BTSA_ArbolDoblesinvar import *

class problemaTrianArbol:
    def __init__(self,info,N=100):
         self.N = N
         self.inicial = info
         self.orden = []
         self.clusters = []
         self.lpot = []
         self.lqueue  = []
         self.posvar = dict()

    def inicia0(self):
            for i in self.orden:
                x = arboldoble()
                self.lpot.append(x)
                y = arboldoble()
                self.lqueue.append(y)
            
            for cl in self.inicial.listaclaus:
                self.insertacolaclau(set(cl))

            for pot in self.lqueue:
                pot.normaliza(self.N)

    def borra(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
    
            pot = self.lqueue[i]
            pot.normaliza(self.N)
            (t0,t1,t2) = pot.splitborra(var)
            res1 = t0.combinaborra(t1,self.N)
            res1.inserta(t2,self.N)
            res1.normaliza(self.N)
            pot.void()
            self.insertacola(res1)

    def insertacolaclau(self,cl):
        if not cl:
            self.anula()
        else:
            indices = map(lambda x:self.posvar[abs(x)],cl)
            pos = min (indices)
            pot = self.lqueue[pos]
            pot.insertaclau(cl)
            
    def insertacola(self,t,conf=set()):
        if t.value.listaclaus  or t.value.unit:
                if t.value.contradict and not conf:
                    self.problemacontradict()
                else:
                    indices = map(lambda x:self.posvar[abs(x)],conf.union(t.value.listavar))
                    # print(set(indices))
                    pos = min (indices) 
                    # print(pos,self.clusters[pos])
                    pot = self.lqueue[pos]
                    pot.inserta(t,self.N,conf) 
                    pot.normaliza(self.N)     

        if not t.var ==0:
            v = t.var
            conf.add(v)
            self.insertacola(t.hijos[0],conf)
            conf.discard(v)
            conf.add(-v)
            self.insertacola(t.hijos[1],conf)
            conf.discard(-v)

    def problemacontradict(self):
        print("contradiccion")
        self.inicial.solved = True
        self.inicial.contradict = True