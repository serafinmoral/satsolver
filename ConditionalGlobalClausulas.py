# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""

import itertools
import time
         
from comunes import *  
from GlobalClausulas import *
             


  
    
class conditionalGlobalClausulas:
    def __init__(self,gclau,valores):
         self.clausulas = globalClausulas()
         self.cond = valores
         self.refer = dict()
         self.aprende = {0}
         self.contra = False
         
         for cl in gclau.listaclaus:
            (clr,cont) = reduceplus(cl,valores)
            if 0 not in clr:
                self.clausulas.insertar(clr)
                self.refer[clr] = set(cl-clr)
                if (len(clr)==0):
                    self.contra = True
                    self.aprende  = refer[clr]
                    break 
                if(len(clr)==1):
                
                    h = set(clr).pop()
                    self.clausulas.unitprev.add(h)
                    self.clausulas.unit.add(h)
                    
                    if -h in self.clausulas.unit:
                        cl2 = frozenset({-h})
                        self.aprende = self.refer[clr].union(self.refer[cl2])
                        self.contra = True
                        break
                    
         self.unitprop()
                    
    def unitprop(self):

        
        while self.clausulas.unitprev and not self.contra:
            p = self.clausulas.unitprev.pop()
            if p in self.clausulas.indices:
                borrar = set()
                for c in self.clausulas.indices[p]:
                    if (len(c)>1):
                        borrar.add(c)
                for c in borrar:
                    self.clausulas.eliminar(c)
            if -p in self.clausulas.indices:
                borrar = set()
                for c in self.clausulas.indices[-p]:
                    borrar.add(c)
                for c in borrar:
                    self.clausulas.eliminar(c)
                    c2 = frozenset(set(c)-{-p})
                    self.refer[c2] = self.refer[c].union(self.refer[frozenset({p})])

                    self.clausulas.insertar(c2)
                    if (len(c2)==1):
                        h = set(c2).pop()
                        self.clausulas.unitprev.add(h)
                        self.clausulas.unit.add(h)
                        if -h in self.clausulas.unit:
                            cl2 = frozenset({-h})
                            self.aprende = self.refer[c2].union(self.refer[cl2])
                            self.contra = True
                            break
                            

            
 

    def addvalor(self,p):
         self.cond.add(p)
         borrar = set()
         anadir = set()
         for cl in self.clausulas.listaclaus:
            if p in cl:
                borrar.add(cl)
            elif -p in cl:
                borrar.add(cl)
                clr = frozenset(cl-{-p}) 
                anadir.add(clr)
                
                self.refer[clr] = self.refer[cl].union({-p})
                
                if(self.refer[clr]==None):
                    print (cl,self.refer[cl],clr,p)
                
                if (len(clr)==0):
                    self.contra = True
                    self.aprende  = self.refer[clr]
                    break
                if(len(clr)==1):
                
                    h = set(clr).pop()
                    self.clausulas.unitprev.add(h)
                    self.clausulas.unit.add(h)
                    
                    if -h in self.clausulas.unit:
                        cl2 = frozenset({-h})
                        self.aprende = self.refer[clr].union(self.refer[cl2])
                        self.contra = True
                        break
                    
         for c in borrar:
                    self.clausulas.eliminar(c)
         for c in anadir:
             self.clausulas.insertayborra(c)
         self.unitprop()     
         
        
    def complV(self,var):
        l1 = self.clausulas.indices.get(var,set())
        l2 = self.clausulas.indices.get(-var,set())
        return (len(l1)*len(l2))
        
    def nextvar(self,variables):
        
        return min(variables,key = lambda x: self.complV(x))
        
         
        

    
#print(SeleccionarArchivo("ArchivosSAT.txt"))


# info.satura(4)
#print("fin de satura")
# info.busca()
# info = leeArchivoSet('SAT_V153C408.cnf')



#info = leeArchivoSet('SAT_V144C560.cnf')

