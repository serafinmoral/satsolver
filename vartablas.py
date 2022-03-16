# -*- coding: utf-8 -*-
"""
Created on 31 Enero 2022

@author: Serafin
"""
from utils import *


class varpot:

        def __init__(self):

            self.tabla = dict()

        def anula(self):
            self.tabla = dict()


        def insertar(self,p):
            for v in p.listavar:
                if v in self.tabla:
                    self.tabla[v].append(p)
                else:
                    self.tabla[v] = [p]

        def createfrompot(self,pot):
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
            miv = min(self.tabla,key = lambda x: len(self.tabla.get(x)))
            mav = max(self.tabla,key = lambda x: len(self.tabla.get(x)))

            print(len(self.tabla.get(miv)),len(self.tabla.get(mav)))

            if len(self.tabla.get(miv)) == 1:
                print("un solo potencial !!!!!!!!!!!!!!!!")
                return (miv)
                


            miv = min(self.tabla,key = lambda x: tam(self.tabla.get(x)))
            mav = max(self.tabla,key = lambda x: tam(self.tabla.get(x)))
            print (tam(self.tabla.get(miv)),tam(self.tabla.get(mav)))
            return miv

        def siguientep(self,pos):
            miv = min(pos,key = lambda x: tam(self.tabla.get(x)))
            mav = max(pos,key = lambda x: tam(self.tabla.get(x)))
            print (tam(self.tabla.get(miv)),tam(self.tabla.get(mav)))
            return miv

        def get(self,i):
            return self.tabla.get(i,[]).copy()




                    
                

