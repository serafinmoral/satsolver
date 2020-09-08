# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import math
from GlobalClausulas import *
from arbolsinvar import * 

class arbolpot:
    def __init__(self):
        self.arbol = arbolsinvar()
        self.listavar = set()
    
        
    def asignavar(self,p):
        self.arbol.asignavar(p)
        
    def asignaval(self,x):
        self.arbol.asignaval(x)
        
        
    def asignahijo(self,t,i):
        self.arbol.hijos[i] = t
        
    def imprime(self):
        print(self.listavar)
        self.arbol.imprime()
        
        
    def computefromSat(self,x):
#        print(self.listavar)
        self.listavar = x.listavar.copy()
        self.arbol.computefromSat(x)
     
                
        
    def select(self,x):
        t = arbolpot()
        t.listavar = self.listavar-{abs(x)}
        t.arbol = self.arbol.select(x)
        return t
    
    def setvalue(self,c,x):
        self.arbol.setvalue(c,x)
    
    def computevalconfig(self,c):
        return self.arbol.computevalconfig(c)    
    
    def selectconfig(self,c):
        t = arbolpot()
        t.listavar = self.listavar - set(map(abs,c))
        
        ar = self.arbol.selectconfig(c)
        
        t.arbol = ar
        return t
     
        
    def multval(self,x):
        t = arbolpot()
        t.listavar = self.listavar.copy()
        t.arbol = self.arbol.multval(x)
        return t
    
    
    def sumaval(self,x):
        t = arbolpot()
        t.listavar = self.listavar.copy()
        t.arbol = self.arbol.sumval(x)
        return t
            
    def combina(self,t2):
        t = arbolpot()
        t.listavar = self.listavar.union(t2.listavar)
        t.arbol = self.arbol.combina(t2.arbol)
     
        return t
    
    def suma(self,t2):
        t = arbolpot()
        t.listavar = self.listavar.union(t2.listavar)
        t.arbol = self.arbol.suma(t2.arbol)

    
        return t
    
    
    
    def marginaliza(self,v):
        t = arbolpot()
        t.listavar = self.listavar-{v}
        t.arbol = self.arbol.marginaliza(v)
       
        return t
            
    
 
            
    def total(self):
        return self.arbol.total(self.listavar)
    
    
            
    def totalv(self,var):
        return self.arbol.totalv(self.listavar,var)
       
            
    def poda(self,epsilon):
        
        
        globalsum = self.total()
        self.arbol.podarec(epsilon,globalsum,self.listavar)
        
  
        
        
        
            
        