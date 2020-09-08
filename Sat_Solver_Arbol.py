# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""

         
from comunes import *  
              
from GlobalClausulas import *
    
from arbol import *
 
                
class solveSATBorradoArbol:    
    def __init__(self,x):
        self.method = 0
        self.limit = 0
        self.solucion = False
        self.solved = False    
        self.varinorder = dict()
        self.posorder = dict()
        self.conjuntosvar = dict()
        self.clausulasborr = dict()
        self.conjuntoclau = x
        self.ordenbo = []
        self.configura = []
        self.conjuntopotentials = []
        
    
        self.potentialsborrado = dict() 
        self.potentialcombinat = dict()
        self.potentialmandado = dict()

        
        for y in x.listavar:
            self.clausulasborr[y] = {}
            self.clausulasborr[-y] = {}
                     
    def inicia(self):
        (self.ordenbo,self.varinorder,self.conjuntosvar) = self.conjuntoclau.computeOrder()
        self.conjuntopotentials = self.conjuntoclau.extraePotentials(self.ordenbo,self.conjuntosvar)
        self.pasapotarbol()
#        for x in self.conjuntopotentials:
#            print (x.listavar)
        
    def pasapotarbol(self):
        lista = []
        for pot in self.conjuntopotentials:
                    
            potarb = arbol()

#            print(pot.listavar)
            potarb.computefromSat(pot)
#            potarb.imprime()
#            if(potarb.total()==0.0):
#                print("0 inicial")
#                potarb.imprime()
#            print(potarb.listavar)
            lista.append(potarb)
        self.conjuntopotentials = lista
        

    def borra(self):
        current=1
        nvar = len(self.ordenbo)
        
        
        while current<= nvar  and not self.solved:
            print (current)
           
            varb = self.ordenbo[current-1]
           
            current = current +1
            print ("Borrando variable ", varb)
            
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
            
            pot = arbol()
            
#            print("potencial incial")
#            pot.imprime()
            
            for p2 in listapotv:
#                print ("multiplicando por")
#                p2.imprime()
               p3 = pot
               pot = pot.combina(p2)
#               if (pot.total() == 0.0):
#                   print("primero")
#                   p3.imprime()
#                   print("segundo")
#                   p2.imprime()
#                print("resultado")
#                pot.imprime()
            
            self.potentialcombinat[varb] = pot
            
            potm = pot.marginaliza(varb)

#            if (potm.total() ==  0.0):
#                print("0 por marginalizacion")
#                potm.imprime()
           
            th = 0.001

            potm.poda(th)
            
            self.potentialmandado[varb] = potm 
            
#            if (potm.total() == 0.0):
#                print("0 por poda")
#                potm.imprime()
                
            if (potm.var == 0 and potm.value == 0.0):
                self.solved = True
                self.con = True
            
            
               # for x in nuevas:
            #   print (x.lista)
     
            #    print (x, self.claus.conjunto[x].lista)
            
#            nuevas = self.conjuntoclau.borraAprox(varb,self.clausulasborr[varb],self.clausulasborr[-varb],th)
            
            self.conjuntopotentials.append(potm)

           
         
            
            
            
            
#            h = list(nuevas.listaclaus)
#            
#            h.sort(key=lambda x: len(x.lista))
          
#            i=0
           
#                if (i==600):
#                    break
                    
  
             
    
    def calculavalor(self,valores,var):
        pot = self.potentialcombinat[abs(var)]
        (potr,confreal) = pot.selectconfig(valores)
        c1 = {var}
        x1 = potr.computevalconfig(c1)
        c2 = {-var}
        x2 = potr.computevalconfig(c2)
        return (x1,x2,confreal)        
    
    def busca(self):
        valores = set()
        n = len(self.ordenbo)
        current = n-1
        
        while not (self.solved):
            print(current)
#            print(valores)
            var = self.ordenbo[current]
#            print(var)
            (varpos,varneg,config) = self.calculavalor(valores,var)
            print (varpos,varneg)
            if (varpos==0 and varneg==0):
                if (current == (n-1)):
                    self.solved = True
                    self.con = True
                imin = n-1
                for y in config:
                    z = abs(y)
                    pos = self.varinorder[z]
                    if (pos<imin):
                        imin = pos
                varmin = self.ordenbo[imin]
                self.potentialcombinat[varmin].setvalue(config,0.0)
                for j in range(current+1,imin+1):
                    valores.discard(self.ordenbo[j])
                    valores.discard(-self.ordenbo[j])
                    
                current = imin
                
            elif varneg==0:
                current -= 1
                valores.add(var)
            elif varpos==0:
                current -= 1
                valores.add(-var)
            elif (varpos>varneg):
               
#                            xneg += 1       
                current -= 1
                
                valores.add(var)
            else:
#                print (varpos,varneg)
#                            xneg += 1       
                current -= 1
                
                valores.add(- var)
            if (current == -1):
                self.solved = True
                self.solucion = True
                self.configura = valores
               
           
    
  
 




    
#print(SeleccionarArchivo("ArchivosSAT.txt"))
info = leeArchivoGlobal('SAT_V153C408.cnf')
#info = leeArchivoGlobal('SAT_V155C1135.cnf')
# info = leeArchivoGlobal('uf20-01.cnf')
# info.satura(4)
#print("fin de satura")
# info.busca()
# info = leeArchivoGlobal('SAT_V153C408.cnf')



#info = leeArchivoSet('SAT_V144C560.cnf')

print(info.listavar)

problema = solveSATBorradoArbol(info)

print(problema.conjuntoclau.listavar)

problema.inicia()

problema.borra()
problema.busca()
