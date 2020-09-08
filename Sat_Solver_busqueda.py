# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os

import itertools
         
from comunes import *  

from random import *
              
from GlobalClausulas import *

from ConditionalGlobalClausulas import *

from time import time

 
                
class solveSATBusqueda:    
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
        self.potentialsborrado = dict() 
        self.potentialcombinat = dict()
        self.potentialmandado = dict()
        self.originalpotentials = []
        self.bloqueadas = set()
        self.totaloriginal = x

        
        for y in x.listavar:
            self.clausulasborr[y] = {}
            self.clausulasborr[-y] = {}
                     
    def inicia(self):
        print(len(self.conjuntoclau.listaclaus))
        self.conjuntoclau.unitprop()
        self.conjuntoclau.equivprop()
        
#        self.conjuntoclau.satura()
        t1 = time()
        self.conjuntoclau.poda() 
        if self.conjuntoclau.contradict:
            self.solucion = False
            self.solved = True
        t2 = time()
        print("Tiempo " , t2-t1)
#        self.bloqueadas = self.conjuntoclau.calculartodasbloqueadas()
#        print("fin de calculo de bloqueadas")
       
        
#        self.totaloriginal.eliminalista(self.bloqueadas)
        
        
        
#        for cl in self.bloqueadas:
#            self.totaloriginal.eliminar(cl)
        
        
        
#        print("potenciales calculados")

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
                
  
#            i=0
           
#                if (i==600):
#                    break
                    
  
    
  
     
        
    
 
    
    
          
    
    def busca(self):
        valores = set()
        n = len(self.conjuntoclau.listavar)
        current = 0
        minc = current
        nnodos = 0
        noborrad = set(self.conjuntoclau.listavar)
      
            
        curset = conditionalGlobalClausulas(self.conjuntoclau,valores)  
        
        if curset.contra:
            self.solved = True
            self.solucion = False
        
        while not (self.solved):
            
            
            
            nnodos += 1
#            print(current)
#            print(valores)
            if (current > minc):
                print (current)
                minc = current
            
#            print(var)
                
            var = curset.nextvar(noborrad)
            noborrad.remove(var)
            self.varinorder[var] = current
            self.ordenbo.append(var)

            xpos = 0.0
            xneg = 0.0
                
#            if (var==255):
#                print("hola")
#                
                    
            pot = curset.clausulas
#                    pot = self.potentialcombinat[var2]
            
            l1=pot.indices.get(var,set())
            l2=pot.indices.get(-var,set())


            for z in l1:
                xpos +=1/2**(len(z)-1)
#                            if(xneg==0):
#                                print("negativo")
                        
            for z in l2:

                     
                xneg +=1/2**(len(z)-1)

#                            if(xpos==0):
#                                print("positivo")
#                            xneg += 1       
          
#                print(xpos,xneg)
                
#  
                
            if (xpos>xneg):
                    curset.addvalor(var)
                    valores.add(var)
            else:
                    curset.addvalor(-var)
                    valores.add(-var)

            current +=1
            

           
            while (curset.contra):
#                
                claures = curset.aprende
#                print(len(claures))
                if(len(claures)==0):
                    self.solved = True
                    self.solucion = False
#                elif (len(claures)==2):
#                    print("nueva de dos ",claures)

                    
                imax = 0
#                print(claures.lista)
                for y in claures:
                    z = abs(y)
                    pos = self.varinorder[z]
                    if (pos>imax):
                        imax = pos
                varmax = self.ordenbo[imax]
                
#                print(claures)
#                if (self.totaloriginal.borraincluidas(claures)):
                self.conjuntoclau.insertayborra(frozenset(claures))
                
               
#                self.totaloriginal.podaylimpia()
                for j in range(current,imax,-1):
#                    print(j)
                    valores.discard(self.ordenbo[j-1])
                    valores.discard(-self.ordenbo[j-1])
                    var = self.ordenbo.pop()
                    noborrad.add(var)
                    
                    
                    
                curset = conditionalGlobalClausulas(self.conjuntoclau,valores)  
                    
                current = imax
         
                
                  

#               
                            
            if (current == n):
                self.solved = True
                self.solucion = True
                self.configura = valores
        print("n. nodos ", nnodos)
        
        
  
               
           
    
  
 




    
#print(SeleccionarArchivo("ArchivosSAT.txt"))
#info = leeArchivoGlobal('SAT_V155C1135.cnf')
# info.satura(4)
#print("fin de satura")
# info.busca()
#info = leeArchivoGlobal('SAT_V153C408.cnf')
#
#info = leeArchivoGlobal('SAT_V1168C4675.cnf')

#info = leeArchivoGlobal('SAT_V6498C130997.cnf')
#info = leeArchivoGlobal('SAT_V686C6816.cnf')
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

    problema = solveSATBusqueda(info)

#print(problema.conjuntoclau.listavar)


    problema.inicia()
    t3 = time()



   

    t4 = time()
    

#problema.originalpotentials = problema.totaloriginal.extraePotentials(problema.ordenbo,problema.conjuntosvar)

    problema.busca()
    t5 = time()



    problema.compruebasol()
#info2 = leeArchivoGlobal('SAT_V1168C4675.cnf')
#info2 = leeArchivoGlobal('aes_32_1_keyfind_1.cnf')
#    info2 = leeArchivoGlobal(nombre)
#info2 = leeArchivoGlobal('SAT_V153C408.cnf')

#    info2.compruebasol(problema.configura)

    print("tiempo lectura ",t2-t1)
    print("tiempo inicio ",t3-t2)
    print("tiempo borrado ",t4-t3)
    print("tiempo busqueda ",t5-t4)

    print("tiempo TOTAL ",t5-t1)
    ttotal += t2-t1

print ("tiempo medio ", ttotal/i)