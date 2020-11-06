# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:28:21 2020

@author: Serafin
"""
from arboltriplesinvar import *
from SimpleClausulas import *

def filtra(lista,nconfig,pconfig,i):
    result = []
    for cl in lista:
        if not cl.intersection(pconfig):
            if len(cl-nconfig)<=i:
                result.append(cl)
    return result


def filtrasplit(lista,nconfig,pconfig,i):
    result1 = []
    result2 = []
    for cl in lista:
            if len(cl-nconfig)<=i:
                result1.append(cl)
            else:
                result2.append(cl)
                
    return (result1,result2)

class problemaTrianArbol:
    def __init__(self,info):
         self.N1 = 300
         self.N2 = 3
         self.inicial = info
         self.orden = []
         self.lpot = []
         self.lqueue  = []
         self.posvar = dict()
         
         
    def inicia0(self):

            for i in self.orden:
                x = arboltriple()
                self.lpot.append(x)
                y = arboltriple()
                self.lqueue.append(y)
    
            for cl in self.inicial.listaclaus:
                self.insertacolaclau(set(cl))
                
            


    def inicia2(self):
            cola = []
            for i in self.orden:
                x = arboltriple()
                self.lpot.append(x)
                y = arboltriple()
                self.lqueue.append(y)
                
            
            listaorden = []


            copia = self.inicial.copia()
            for i in reversed(range(len(self.orden))):
                var = self.orden[i]
                potsin = []
                if len(copia.indices.get(var,set())) < len(copia.indices.get(-var,set())):
                    value = -var
                else:
                    value = var
                lista = copia.indices.get(value,set()).copy()
                for cl in lista:
                    copia.eliminar(cl)
                    potsin.append(cl)
                print("var ", var, len(potsin))
                listaorden.append(potsin)                                
                
            print(len(listaorden))
            return listaorden
     
                

                    
    def selectval(self,i,var,config):
        return var
                    
                
    def insertapu(self,cl,pot,val):
        borrar = []
        cola = []
        if -val in pot.indices:
            for clau in pot.indices[-val]:
                cl1 = frozenset(clau-{-val})
                if not cl1:
                    self.solved = True
                    self.contradict = True
                    break
                cola.append(cl1)
                borrar.append(clau)
        if val in pot.indices:
            for clau in pot.indices[val]:
                borrar.append(clau)
        pot.inserts(cl)
    
        for clau in borrar:
            pot.eliminar(clau)
            
            
        return cola

    def podau(self,pot,val):
    
        borrar = []
        cola = []
        if -val in pot.indices:
            for clau in pot.indices[-val]:
                cl1 = frozenset(clau-{-val})
                cola.append(cl1)
                if not cl1:
                    self.solved = True
                    self.contradict = True
                    break
                borrar.append(clau)
        if val in pot.indices:
            for clau in pot.indices[val]:
                borrar.append(clau)
                
        
    
        for clau in borrar:
            pot.eliminar(clau)
        
        
        
        
        return cola
            
    def insertacolaclau(self,cl):
        if not cl:
            self.anula()
        else:
            indices = map(lambda x:self.posvar[abs(x)],cl)
            pos = min (indices) 
            pot = self.lqueue[pos]
            pot.insertaclau(cl)


    
                
    def tinserta(self,cl,pos=-1):
#    print(cl)
        cola = []
        if not cl:
            self.inicial.solved = True
            self.inicial.contradict = True
        elif len(cl)==1:
            val = set(cl).pop()
            var = abs(val)        
            pos = self.posvar[var]
            pot = self.lpot[pos]
            self.inicial.unit.add(val)
            self.inicial = self.inicial.restringe(val)
            cola = cola + self.insertapu(cl,pot,val)
#            print(cola)
            for i in range(pos):
            
                pot = self.lpot[i]
                if var in pot.listavar:
                    cola = cola + self.podau(pot,val)
#                    print(cola)
                pot = self.lqueue[i]
                if var in pot.listavar:
                    cola = cola + self.podau(pot,val)
#                    print(cola)
                    
        elif len(cl)<=self.N1:
        
            if (pos ==-1):
                indices = map(lambda x:self.posvar[abs(x)],cl)
                pos = min (indices)
            pot = self.lpot[pos]
            pot2 = self.lqueue[pos]
            var = self.orden[pos]

            pot.borraincluidas(cl)
            pot2.borraincluidas(cl)
            cola = pot.insertasatura(cl,var)
            
            
                
        else:
            if (pos ==-1):
                indices = map(lambda x:self.posvar[abs(x)],cl)
                pos = min (indices)
            var = self.orden[pos]
            pot = self.lpot[pos]
            cola = pot.insertasatura(cl,var)
    
        return cola
    
    
    
    def borra(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            var = self.orden[i]
            # print("i= ", i, "var = ", self.orden[i], " n. peq. ", len(self.peq[i].listaclaus),self.peq[i].listaclaus)
     
            pot = self.lqueue[i]
            pot2 = self.lpot[i]

            # pot.imprime()            

            pot.simplifica(pot2)


            l1 = pot.indices.get(var,set())
            l2 = pot.indices.get(-var,set())

            lp1 = pot2.indices.get(var,set())
            lp2 = pot2.indices.get(-var,set())
            

            npot = arboltriple()
            for cl1 in l1:
                for cl2 in l2:
                    cl = resolution(var,cl1,cl2)
                    if 0 not in cl:
                        npot.insertar(cl)
            for cl1 in l1:
                for cl2 in lp2:
                    cl = resolution(var,cl1,cl2)
                    if 0 not in cl:
                        npot.insertar(cl)

            for cl1 in lp1:
                for cl2 in l2:
                    cl = resolution(var,cl1,cl2)
                    if 0 not in cl:
                        npot.insertar(cl)

            for cl1 in l1:
                pot2.insertar(cl1)
            for cl2 in l2:
                pot2.insertar(cl2)

                
            pot.anula()
            if npot.solved:
                self.inicial.solved = True
                self.inicial.contradict = self.inicial.contradict
                break
            if len(npot.listaclaus)>0 :
                print("longitud ", len(npot.listaclaus), npot.listavar , len(npot.listavar))
 
            npot.podaylimpiarec()
            if len(npot.listaclaus)>0 :
                print("longitud ", len(npot.listaclaus))

            for cl in npot.listaclaus:
                self.insertaypodacola(cl)

    def borra2(self):

        nuevas = True
        while nuevas and not self.inicial.solved:
            
            print("nueva vuelta")
            cola = []
            for i in range(len(self.orden)):
                
                pot = self.lqueue[i]
                while pot.listaclaus:
                    cl = pot.listaclaus.pop()
                    pot.eliminar(cl)
                    cola = cola + self.tinserta(cl,pos=i)

            if not cola:
                nuevas = False
            else:
                print(len(cola))
                for cl in cola:
                    self.insertaypodacola(cl)

                

                

                

                

    def borra4(self,listapot):

        while listapot:
            
            print (len(listapot))
            nclau = listapot.pop()
            print(len((nclau)))
            for cl in nclau:
                self.insertacola(cl)
            self.borra()

        for i in range(len(self.orden)):
            print(self.lpot[i].listaclaus)
       
    
    def anula(self):
        self.inicial.solved = True
        self.inicial.contradict = True
        for pot in self.lpot:
            pot.anula()
        for por in self.lqueue:
            pot.anula()
   
                
                
        
        
        
        
        
        