# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os

import itertools

from comunes import *
from GlobalClausulas import  *      
   

           
    
                
class solveSATBorradoSet:    
    def __init__(self,x):
        self.method = 0
        self.limit = 0
        self.solucion = False
        self.solved = False    
        self.varinorder = dict()
        self.posorder = dict()
        self.clausulasborr = dict()
        self.conjuntoclau = x
        self.ordenbo = []
        self.configura = []
        self.conjuntopotentials = []
        
        for y in x.listavar:
            self.clausulasborr[y] = {}
            self.clausulasborr[-y] = {}
            
    def computeOrder(self):
        
        self.ordenbo.clear()
        conjuntos = self.conjuntoclau.calculaconjuntos()
        noborrad = list(self.conjuntoclau.listavar)
        self.varinorder.clear()
        current = 1
        while len(noborrad)>0:
            (var,conjunto) = conjuntos.nextVar(noborrad)
            noborrad.remove(var)
            self.ordenbo.append(var)
            self.varinorder[var] = current-1
#            print (current)
            current += 1
     
#            print (var)
#            print(conjunto)
            conjuntos.actualizab(var,conjunto)
            
            
    def computeCliques(self):
        
        self.ordenbo.clear()
        conjuntos = self.conjuntoclau.calculaconjuntos()
        noborrad = list(self.conjuntoclau.listavar)
        self.varinorder.clear()
        current = 1
        while len(noborrad)>0:
            (var,conjunto) = conjuntos.nextVar(noborrad)
            noborrad.remove(var)
            self.ordenbo.append(var)
            self.varinorder[var] = current-1
#            print (current)
            current += 1
     
#            print (var)
#            print(conjunto)
            conjuntos.actualizab(var,conjunto)
  
            
    
         
    def computeCompl(self,y,i):
        c = 0
        if (i==0):
            x1 = len(self.conjuntoclau.indices[y])
            x2  = len(self.conjuntoclau.indices[-y])
            c= x1*x2 - x1 -x2
        return c
    

    
    
    
    def siguiente(self,i,noborrad):
        y = noborrad[0]
        best = self.computeCompl(y,i)
        nbest = y
        for y in noborrad[1:]:
            z = self.computeCompl(y,i)
            if(z<best) :
                nbest=y
                best=z
        return nbest
    
    @staticmethod
    def calculavalor(valores,conjunto):
        for x in conjunto:
            if len(valores.intersection(x))==0:
                return [True,x]
        return [False]
                
    
    def busca(self):
        valores = set()
        n = len(self.ordenbo)
        current = n-1
        
        while not (self.solved):
            print(current)
#            print(current)
            var = self.ordenbo[current]
            varpos = solveSATBorradoSet.calculavalor(valores,self.clausulasborr[var])
            varneg = solveSATBorradoSet.calculavalor(valores,self.clausulasborr[-var])
            if (varpos[0] and varneg[0]):
                clau1 = varpos[1]
                clau2 = varneg[1]
#                print(clau1.lista)
#                print(clau2.lista)
#                print(var)
                claures = resolution(var,clau1,clau2)
                if(len(claures)==0):
                    self.solved = True
                    self.solucion = False

                    
                imin = n-1
#                print(claures.lista)
                for y in claures:
                    z = abs(y)
                    pos = self.varinorder[z]
                    if (pos<imin):
                        imin = pos
                varmin = self.ordenbo[imin]
                if (varmin in claures):
                    self.clausulasborr[varmin].add(claures)
                else:
                    self.clausulasborr[-varmin].add(claures)
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
                for i in range(current-1):
                    var2 = self.ordenbo[i]
                    l1 = self.clausulasborr[var2]
                    l2 = self.clausulasborr[-var2]
                    for z in l1:
                        z = reduce(z,valores)
                        if var in z:
#                            xpos += 1
                            xneg *= (2**(len(z)-1)-1)/2**(len(z)-1)
                        elif -var in z:
                            xpos *= (2**(len(z)-1)-1)/2**(len(z)-1)
#                            xneg += 1
                    for z in l2:
                        z = reduce(z,valores)
                        if var in z:
#                            xpos += 1
                            xneg *= (2**(len(z)-1)-1)/2**(len(z)-1)
                        elif -var in z:
                            xpos *= (2**(len(z)-1)-1)/2**(len(z)-1)
#                            xneg += 1       
                current -= 1
                print(xpos,xneg)
                if (xpos>xneg):
                    valores.add(var)
                else:
                    valores.add(-var)
                            
            if (current == -1):
                self.solved = True
                self.solucion = True
                self.configura = valores
        
                
    def eliminaListas(self,lista1,lista2,noborrad):
        
        for y in lista1:
            for z in y:
                if (z in noborrad) or (-z in noborrad):
                        self.conjuntoclau.indices[z].remove(y)
                        

        for y in lista2:
            for z in y:
                if (z in noborrad) or (-z in noborrad):
                        self.conjuntoclau.indices[z].remove(y)     
                
    def borra(self,previo=False):
        current=1
        noborrad = list(self.conjuntoclau.listavar)
        while len(noborrad)>0 and not self.solved:
            print (current)
            if previo:
                varb = self.ordenbo[current-1]
            else:
                varb = self.siguiente(0,noborrad)
                self.ordenbo.append(varb)
                self.varinorder[varb] = current-1
            current = current +1
            noborrad.remove(varb)
            print ("Borrando variable ", varb)
            
            # self.listapos[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # self.listaneg[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # print(len(self.listapos[varb]))
            # self.limpiaordennum(self.listapos[varb])
            # print(len(self.listapos[varb]))
            # print(len(self.listaneg[varb]))
            # self.limpiaordennum(self.listaneg[varb])
            # print(len(self.listaneg[varb]))

            self.clausulasborr[varb] = self.conjuntoclau.indices[varb]
            self.clausulasborr[-varb] = self.conjuntoclau.indices[-varb]
            
            th = 0.02

            
            # for x in self.listapos[varb]:
            #    print (x, self.claus.conjunto[x].lista)
            
#            nuevas = self.conjuntoclau.borraAprox(varb,self.clausulasborr[varb],self.clausulasborr[-varb],th)
            
            print("eliminando")
            self.eliminaListas(self.clausulasborr[varb],self.clausulasborr[-varb],noborrad)

            print("borrando")
            nuevas = self.conjuntoclau.borraExactoCasi(varb,self.clausulasborr[varb],self.clausulasborr[-varb],th)

            # for x in nuevas:
            #   print (x.lista)
            print("tamaño sin limpiar" ,len(nuevas.listaclaus))
            print("ordenadas")
                
#            nuevas.limpiatama(18)
            nuevas.limpianum(10000)
            nuevas.limpiarec(th)
            # solveSATBorrado.limpiarec(nuevas,noborrad,posiciones)
            print("tamaño después de limpiar" ,len(nuevas.listaclaus))
            
            
            
            
            
#            h = list(nuevas.listaclaus)
#            
#            h.sort(key=lambda x: len(x.lista))
          
#            i=0
            for x in nuevas.listaclaus:
#                i+=1
                if (len(x)==0):
                    self.solved = True
                    self.solution = False
                elif (0 not in x):
                    self.conjuntoclau.insertar(x)
#                if (i==600):
#                    break
                    
  
             
  






    
#print(SeleccionarArchivo("ArchivosSAT.txt"))
info = leeArchivoGlobal('SAT_V153C408.cnf')
# info.satura(4)
print("fin de satura")
# info.busca()
# info = leeArchivoSet('SAT_V153C408.cnf')



#info = leeArchivoSet('SAT_V144C560.cnf')
problema = solveSATBorradoPotential(info)
problema.computeOrder()

problema.borra(previo=True)
problema.busca()
