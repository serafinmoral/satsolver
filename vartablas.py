# -*- coding: utf-8 -*-
"""
Created on 31 Enero 2022

@author: Serafin
"""
from utils import *


class varpot:

        def __init__(self):

            self.tabla = dict()
            self.unit = set()
            self.contradict = False

        def anula(self):
            self.tabla = dict()
            self.unit = dict()
            self.contradict = True


        def insertar(self,p):
            if self.unit:
                varsu = set(map(abs,self.unit))
                if varsu.intersection(set(p.listavar)):
                    varr = filter(self.unit, key = lambda x: abs(x) in varsu)
                    for x in varr:
                        p = p.reduce(x,inplace=False)
            for v in p.listavar:
                if v in self.tabla:
                    self.tabla[v].append(p)
                else:
                    self.tabla[v] = [p]

        def reduce(self,v,inplace=True):
            res = self if inplace else  self.copia()

            if v in self.unit:
                self.unit.discard(v)
            elif -v in self.unit:
                self.unit.anula()
            elif v in self.tabla:
                
                res.borrarv(v)



        def copia(self):
            res = varpot()
            res.unit = self.copy()
            res.contradict = self.contradict
            for x in self.keys():
                res.tabla[x] = self.tabla[x].copy()
            return res




        def createfrompot(self,pot):
            self.contradict = self.contradict
            self.unit = pot.unit.copy()
            for p in pot.listap:
                self.insertar(p)


        def borrarpot(self,p):
            for v in p.listavar:
                self.tabla[v].remove(p)

        def borrarv(self,v):
            if v in self.tabla:
                for p in self.tabla[v].copy():
                    self.borrarpot(p)
                del self.tabla[v]

        def siguiente(self):

            if self.unit:
                x = self.unit.pop()
                self.unit.add(x)
                return abs(x)
            miv = min(self.tabla,key = lambda x: len(self.tabla.get(x)))
            mav = max(self.tabla,key = lambda x: len(self.tabla.get(x)))

            print(miv,mav,len(self.tabla.get(miv)),len(self.tabla.get(mav)))

            if len(self.tabla.get(miv)) == 1:
                print("un solo potencial !!!!!!!!!!!!!!!!")
                return (miv)
                


            miv = min(self.tabla,key = lambda x: tam(self.tabla.get(x)))
            mav = max(self.tabla,key = lambda x: tam(self.tabla.get(x)))
            print (miv,mav,tam(self.tabla.get(miv)),tam(self.tabla.get(mav)))
            return miv

        def siguientep(self,pos):

            if self.unit:
                varu = set(map(abs,self.unit))
                if varu.intersection(pos):
                    x = varu.pop()
                
                    return x

            miv = min(pos,key = lambda x: tam(self.tabla.get(x)))
            mav = max(pos,key = lambda x: tam(self.tabla.get(x)))
            print (miv,mav,tam(self.tabla.get(miv)),tam(self.tabla.get(mav)))
            return miv

        def get(self,i):
            return self.tabla.get(i,[]).copy()




                    
                

