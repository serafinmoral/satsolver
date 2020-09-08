# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os

import itertools
         
from comunes import *  
              
from GlobalClausulas2 import *

from time import time

 
                
class solveSATBorradoPotential:    
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
#        self.conjuntoclau.satura()
        t1 = time()
        self.conjuntoclau.podaylimpia() 
        t2 = time()
        print("Tiempo " , t2-t1)
#        self.bloqueadas = self.conjuntoclau.calcularbloqueadas()
#        print("fin de calculo de bloqueadas")
        (self.ordenbo,self.varinorder,self.conjuntosvar) = self.conjuntoclau.computeOrder()
        print("fin de calculo de orden")
        self.totaloriginal = self.conjuntoclau.copia()

        self.conjuntopotentials = self.conjuntoclau.extraePotentials(self.ordenbo)
        
        
        
        
        
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
                
            
            
    def borra(self):
        current=1
        print (self.conjuntoclau.listavar)
        nvar = len(self.ordenbo)
        
        total = 0
        
        while current<= nvar  and not self.solved:
            print (current)
           
            varb = self.ordenbo[current-1]
           
            current = current +1
#            print ("Borrando variable ", varb)
            
            # self.listapos[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # self.listaneg[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # print(len(self.listapos[varb]))
            # self.limpiaordennum(self.listapos[varb])
            # print(len(self.listapos[varb]))
            # print(len(self.listaneg[varb]))
            # self.limpiaordennum(self.listaneg[varb])
            # print(len(self.listaneg[varb]))
            
            listapotv = calculapotentials(self.conjuntopotentials,varb)
            
            self.potentialsborrado[varb] = listapotv
            
#            print(len(listapotv))
            
            pot = globalClausulas()
            
            for p2 in listapotv:
                pot.combina(p2)
            
#            pot.podavar2(varb)
            
#            th = 0.05
#            th = 0.000

            
#            (pot1,pot2) = pot.split(varb)
#            print(pot1.listaclaus)
#            print("split ",len(pot1.listaclaus), len(pot2.listaclaus)  )
            self.potentialcombinat[varb] = pot
#            total = total +  len(pot1.listaclaus)
#            print(pot1.listaclaus)
#            unitarias = set()
#            otras = set()
##            potm= globalClausulas()
#            potm = pot1.marginalizaapr(varb,th,self.bloqueadas,unitarias,otras)
            
            
#            potm = globalClausulas()
#            potm.podaylimpia()
#            print(potm.listaclaus)
#            print(len(otras))
#            if (unitarias):
#                print("unitarias")
#                for p in unitarias:
#                    self.totaloriginal.unitprev.add(p)
#                self.original.unitprop()      
#
#            
#            for cl in potm.listaclaus:
#                self.totaloriginal.insertayborra(cl)
            
            

            
#            self.potentialmandado[varb] = potm
            
           
#            if pot1.contradict:
#                self.solved = True
#                self.con = True
            
            
               # for x in nuevas:
            #   print (x.lista)
#            print("tamaño sin limpiar" ,len(potm.listaclaus))
#            print("ordenadas")
#            potm.limpiarec(th)   
#            potm.limpiatama(1)
#            print(potm.listaclaus)
#            potm.limpianum(10)
#            print(potm.listaclaus)

#            potm.limpiarec(th)
#            
#            
#            for cl in potm.listaclaus:
#                self.totaloriginal.insertayborra(cl)
            # solveSATBorrado.limpiarec(nuevas,noborrad,posiciones)
#            print("tamaño después de limpiar" ,len(potm.listaclaus))
            
            # for x in self.listapos[varb]:
            #    print (x, self.claus.conjunto[x].lista)
            
#            nuevas = self.conjuntoclau.borraAprox(varb,self.clausulasborr[varb],self.clausulasborr[-varb],th)
            
#            self.conjuntopotentials.append(potm)
#            self.conjuntopotentials.append(pot2)

           
         
            
#            print(total)
            
            
#            h = list(nuevas.listaclaus)
#            
#            h.sort(key=lambda x: len(x.lista))
          
#            i=0
           
#                if (i==600):
#                    break
                    
  
             
    
    def calculavalor(self,valores,var):
        pot = self.potentialcombinat[abs(var)]
        negativos = set(map(lambda x: -x,valores))
        if var in pot.indices:
            for x in pot.indices[var]:
                if ((x-{var})<=negativos):
                    return [True,x]
        return [False]
                
    
 
    
    
                   
    
    def calculavalor2(self,valores,var):
        pot = self.totaloriginal
        negativos = set(map(lambda x: -x,valores))
        if var in pot.indices:
            for x in pot.indices[var]:
                if ((x-{var})<=negativos):
                    return [True,x]
        return [False]
    
    def busca(self):
        valores = set()
        n = len(self.ordenbo)
        current = n-1
        minc = current
        nnodos = 0
        
        while not (self.solved):
            
            
            nnodos += 1
#            print(current)
#            print(valores)
            if (current < minc):
                print (current)
                minc = current
            var = self.ordenbo[current]
#            print(var)
            varpos = self.calculavalor(valores,var)
            varneg = self.calculavalor(valores,-var)
            if (varpos[0] and varneg[0]):
#                print("Contradiccion ")
                clau1 = varpos[1]
                clau2 = varneg[1]
#                print(valores)
#                print(clau1)
#                print(clau2)
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
                self.potentialcombinat[varmin].insertar(claures)
#                print(claures)
#                if (self.totaloriginal.borraincluidas(claures)):
                self.totaloriginal.insertayborra(claures)
#                self.totaloriginal.podaylimpia()
                for j in range(current+1,imin+1):
                    valores.discard(self.ordenbo[j])
                    valores.discard(-self.ordenbo[j])
                    
                current = imin
                
            elif varpos[0] and not varneg[0]:
#                print ("positivo")
                current -= 1
                valores.add(var)
            elif varneg[0] and not varpos[0]:
#                print ("negativo")

                current -= 1
                valores.add(-var)
            else:
                xpos = 1.0
                xneg = 1.0
                
                    
                    
                pot = self.totaloriginal 
#                    pot = self.potentialcombinat[var2]
                if var in pot.indices:
                        l1=pot.indices[var]
                else:
                        l1 = set()
                if -var in pot.indices:
                        l2=pot.indices[-var]
                else:
                        l2 = set()
#                    print("positivas")
                for z1 in l1:
                        z = reduce(z1,valores)
                        
                        if 0 not in z:
#                            if (len(z) == 1):
#                                print(z)
#                                print(z1)
                            xneg *= (2**(len(z)-1)-1)/2**(len(z)-1)
#                            if(xneg==0):
#                                print("negativo")
                        
#                    print("negativas")
                for z1 in l2:

                        z = reduce(z1,valores)
                        
                        if 0 not in z:
#                            if (len(z) == 1):
#                                print(z)
#                                print(z1)
                            xpos *= (2**(len(z)-1)-1)/2**(len(z)-1)
#                            if(xpos==0):
#                                print("positivo")
#                            xneg += 1       
                current -= 1
#                print(xpos,xneg)
                
#  
                
                if (xpos>xneg):
                    valores.add(var)
                else:
                    valores.add(-var)
                            
            if (current == -1):
                self.solved = True
                self.solucion = True
                self.configura = valores
        print("n. nodos ", nnodos)
    
  
    def busca3(self):
        valores = set()
        n = len(self.ordenbo)
        current = n-1
        minc = current
        
        while not (self.solved):
#            print(valores)
            if (current < minc):
                print (current)
                minc = current
            var = self.ordenbo[current]
#            print(var)
            varpos = self.calculavalor(valores,var)
            varneg = self.calculavalor(valores,-var)
            if (varpos[0] and varneg[0]):
#                print("Contradiccion ")
                clau1 = varpos[1]
                clau2 = varneg[1]
#                print(valores)
#                print(clau1)
#                print(clau2)
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
                self.potentialcombinat[varmin].insertar(claures)
#                print(claures)
                self.totaloriginal.insertar(claures)
                for j in range(current+1,imin+1):
                    valores.discard(self.ordenbo[j])
                    valores.discard(-self.ordenbo[j])
                    
                current = imin
                
            elif varpos[0] and not varneg[0]:
#                print ("positivo")
                current -= 1
                valores.add(var)
            elif varneg[0] and not varpos[0]:
#                print ("negativo")

                current -= 1
                valores.add(-var)
            else:
                valores.add(var)
                current -= 1

                            
            if (current == -1):
                self.solved = True
                self.solucion = True
                self.configura = valores
    
  
 

    def busca2(self):
        valores = set()
        n = len(self.ordenbo)
        current = n-1
        minc = current
        
        while not (self.solved):
#            print(current)
#            print(valores)
            if (current < minc):
                print (current)
                minc = current
            var = self.ordenbo[current]
#            print(var)
            varpos = self.calculavalor2(valores,var)
            varneg = self.calculavalor2(valores,-var)
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
                
                    
                    
                pot = self.totaloriginal 
#                    pot = self.potentialcombinat[var2]
                if var in pot.indices:
                        l1=pot.indices[var]
                else:
                        l1 = set()
                if -var in pot.indices:
                        l2=pot.indices[-var]
                else:
                        l2 = set()
#                    print("positivas")
                for z1 in l1:
                        z = reduce(z1,valores)
                        
                        if 0 not in z:
#                            if (len(z) == 1):
#                                print(z)
#                                print(z1)
                            xneg *= (2**(len(z)-1)-1)/2**(len(z)-1)
                        
#                    print("negativas")
                for z1 in l2:

                        z = reduce(z1,valores)
                        
                        if 0 not in z:
#                            if (len(z) == 1):
#                                print(z)
#                                print(z1)
                            xpos *= (2**(len(z)-1)-1)/2**(len(z)-1)
#                            xneg += 1       
                current -= 1
#                print(xpos,xneg)
                if (xpos>xneg):
                    valores.add(var)
                else:
                    valores.add(-var)
                            
            if (current == -1):
                self.solved = True
                self.solucion = True
                self.configura = valores
               
           
    
  
 




    
#print(SeleccionarArchivo("ArchivosSAT.txt"))
#info = leeArchivoGlobal('SAT_V155C1135.cnf')
# info.satura(4)
#print("fin de satura")
# info.busca()
t1 = time()
#info = leeArchivoGlobal('SAT_V153C408.cnf')

#info = leeArchivoGlobal('SAT_V1168C4675.cnf')

#info = leeArchivoGlobal('SAT_V6498C130997.cnf')


info = leeArchivoGlobal('aes_32_1_keyfind_1.cnf')
t2= time()



#info = leeArchivoSet('SAT_V144C560.cnf')

#print(info.listavar)

problema = solveSATBorradoPotential(info)

#print(problema.conjuntoclau.listavar)


problema.inicia()
t3 = time()



problema.borra()
t4 = time()

#problema.originalpotentials = problema.totaloriginal.extraePotentials(problema.ordenbo,problema.conjuntosvar)

problema.busca()
t5 = time()



problema.compruebasol()
#info2 = leeArchivoGlobal('SAT_V1168C4675.cnf')
info2 = leeArchivoGlobal('aes_32_1_keyfind_1.cnf')
#info2 = leeArchivoGlobal('SAT_V6498C130997.cnf')
#info2 = leeArchivoGlobal('SAT_V153C408.cnf')

info2.compruebasol(problema.configura)

print("tiempo lectura ",t2-t1)
print("tiempo inicio ",t3-t2)
print("tiempo borrado ",t4-t3)
print("tiempo busqueda ",t5-t4)

print("tiempo TOTAL ",t5-t1)


