# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:28:21 2020

@author: Serafin
"""
from GlobalClausulas import *

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

class problemaTrian:
    def __init__(self,info):
         self.N1 = 3
         self.N2 = 1
         self.N3 = 2
         self.inicial = info
         self.orden = []
         self.lpot = []
         self.lqueue  = []
         self.posvar = dict()
         
         
    def inicia(self):
            cola = []
            for i in self.orden:
                x = globalClausulas()
                self.lpot.append(x)
                y = globalClausulas()
                self.lqueue.append(y)
    
            for cl in self.inicial.listaclaus:
#                print("inserto " ,cl)
                cola = cola + self.tinserta(cl)
                
            while cola:
                cl = cola.pop()
                if not cl:
                    self.inicial.solved = True
                    self.inicial.contradict = True
                elif len(cl)<= self.N1:
                    cola = cola + self.tinserta(cl)
                else:
                    self.insertacola(cl)
                    
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
            
    def insertacola(self,cl):
          indices = map(lambda x:self.posvar[abs(x)],cl)
          pos = min (indices) 
          pot = self.lqueue[pos]
          pot.inserts(cl)
                
    def tinserta(self,cl):
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
        
        
            indices = map(lambda x:self.posvar[abs(x)],cl)
            pos = min (indices)
            pot = self.lpot[pos]
            pot2 = self.lqueue[pos]
            var = self.orden[pos]

            pot.borraincluidas(cl)
            pot2.borraincluidas(cl)
            cola = pot.insertasatura(cl,var)

            for i in range(pos):
                pot = self.lpot[i]
                if cl <= pot.listavar:
                    cola = cola + pot.podacola(cl)
                
        else:
            indices = map(lambda x:self.posvar[abs(x)],cl)
            pos = min (indices) 
            var = self.orden[pos]
            pot = self.lpot[pos]
            cola = pot.insertasatura(cl,var)
    
        return cola
    
    
    
    
    def busca(self):
        
        config = []
        nconfig = set()
        pconfig = set()
        n = len(self.orden)

        i=n-1

        
        while not self.inicial.solved:
            print("i=",i)
            print(config)
            back = False
            maxpos = i
            if i<0:
                self.inicial.solved = True
                self.inicial.solution = set(config)
            else:
                pot = self.lqueue[i]
                var = self.orden[i]
#                print(var)
                
                l1 = filtra(pot.indices.get(var,set()),nconfig,pconfig,1)
                l2 = filtra(pot.indices.get(-var,set()),nconfig,pconfig,1)
                
#                print(len(l1),len(l2))
#                pot = self.lpot[i]
#
#                l1p = filtra(pot.indices.get(var,set()),nconfig,pconfig,1)
#                l2p = filtra(pot.indices.get(-var,set()),nconfig,pconfig,1)
#                print(len(l1p),len(l2p))
                
                lista = set(l1+l2)
                
                for cl in lista:
                    pot.eliminar(cl)
                
#                print(lista)

                for j in range(0,i):
                    pot = self.lqueue[j]
                    lista2 = filtra(pot.listaclaus,nconfig,pconfig,self.N2)
                    for cl in lista2:
                        pot.eliminar(cl)
                    lista.update(set(lista2))
                
                print(len(lista))
                while lista and not self.inicial.solved:
                    cl = lista.pop()
                    print(len(lista))
#                    print(cl)
                    if cl <= nconfig:
                        back = True
                        indices = map(lambda x:self.posvar[abs(x)],cl)
                        maxpos = min (indices)
                        nuevas = self.tinserta(cl)
#                    print(nuevas)
                        if self.inicial.solved:
                            break
                    
                        (n1,n2) = filtrasplit(nuevas,nconfig,pconfig,self.N2)
                        lista.update(set(n1))
                        lista.update(set(n2))
                        print(len(lista))
                        while lista:
                            cl = lista.pop()
                            self.insertacola(cl)
                        break

#                    if (len(n1)>0):
#                        print(config)
#                        print(n1)
                    nuevas = self.tinserta(cl)
#                    print(nuevas)
                    if self.inicial.solved:
                            break
                    
                    (n1,n2) = filtrasplit(nuevas,nconfig,pconfig,self.N2)
                    lista.update(set(n1))
                    for cl1 in n2:
                        self.insertacola(cl1)
                        
                            
                    nuevas = self.tinserta(cl)
#                    print(nuevas)
                    if self.inicial.solved:
                        break
                    
                    (n1,n2) = filtrasplit(nuevas,nconfig,pconfig,self.N2)
                    
                    

#                    if (len(n1)>0):
#                        print(config)
#                        print(n1)
                    lista.update(set(n1))
                    for cl1 in n2:
                        self.insertacola(cl1)
                    
                    
                if back:
                    for j in range(i,maxpos):
                        x = config.pop()
                        pconfig.remove(x)
                        nconfig.remove(-x)
                    i = maxpos
                else:
                    if l1:
                        nvalue = var
                    elif l2:
                        nvalue = -var
                    else:
                        pot = self.lpot[i]

                        l1 = filtra(pot.indices.get(var,set()),nconfig,pconfig,1)
                        l2 = filtra(pot.indices.get(-var,set()),nconfig,pconfig,1)
#                        print(len(l1),len(l2))

                        if l1:
                            nvalue = var
                        elif l2:
                            nvalue = -var
                        else:
                            nvalue = self.selectval(i,var,config)
                            
                            
                    config.append(nvalue)
                    pconfig.add(nvalue)
                    nconfig.add(-nvalue)
                    i-=1
                    
        return config
                    
                            
                
                
                
        
        
        
        
        
        