# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""

import itertools
         
from comunes import *  
import networkx as nx    



def leeArchivoGlobal(Archivo):
    reader=open(Archivo,"r")
    cadena = reader.readline()
    
    while cadena[0]=='c':
        cadena = reader.readline()
    
    cadena.strip()
    listaaux = cadena.split()
    print(listaaux)
    nvar = int(listaaux[2])
    nclaus = int(listaaux[3])
    print(nvar)
#    print(cadena)
    while cadena[0]=='c':
        cadena = reader.readline()
#    param = cadena.split()

    infor = simpleClausulas()
    infor.nvar = nvar
    for cadena in reader:
#        print (cadena)
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= set(listaux)
            infor.insertar(clausula)
            if(len(clausula)==1):
                h = set(clausula).pop()
                infor.unitprev.add(h)
           



#    print("paso a limpiar")
#    infor.limpiarec(0.0)
#    print("termino de limpiar")
    return infor  

 
    
class simpleClausulas:
    def __init__(self):
         self.listaclaus = []
         self.contradict = False
         self.listavar = set()    
         self.solved = False
         self.solution = set()
         self.unit = set()
         self.unitprev = set()
         
     
    
    def cgrafo(self):
        grafo = nx.Graph()
        
        grafo.add_nodes_from(self.listavar)
        
        for cl in self.listaclaus:
           for u in cl:
                   for v in cl:
                       if not abs(u)==abs(v):
                           grafo.add_edge(abs(u),abs(v))                     
        return grafo  
    
        
    def compruebasol2(self,config):
        conf = set(config)
        for y in self.listaclaus:
            inte = conf.intersection(y)
            if not inte:
                print("solucion no valida ")
                print(config)
                print("clausula ",y)
                return False
                break
        print ("correcto")
        return True  
                        
            
    def propagacion_unitaria(self):
        self.unitprev= set()
        for c in self.listaclaus:
            if (len(c))== 1:
                h = set(c).pop()
                self.unitprev.add(h)
                self.unit.add(h)
            
        self.unitprop()        
                
            
    def unitprop(self):
        res = set()
        while self.unitprev:
            p = self.unitprev.pop()

            res.add(p)
            
            self.listavar.discard(abs(p))
            borrar = []

            for cl in self.listaclaus:
                if p in cl:
                    borrar.append(cl)
                elif -p in cl:
                    cl.discard(cl)
                    if len(cl) == 1:
                        nv = next(iter(cl))
                        self.unitprev.add(nv)
                    elif not cl:
                        self.contradict = True
                        break
   
                                    
        return res


 
        
        
                
    def copia(self):
      nuevo = simpleClausulas()
      nuevo.listavar = self.listavar.copy()
      nuevo.unit = self.unit.copy()
      nuevo.contradict = self.contradict
      
      
      for x in self.listaclaus:
          nuevo.insertar(x)
          
      return nuevo

    
    
    

    
 
            
  
            
    
            
            
   
   
            
        
        
    def anadirConjunto(self,z):
        for y in z:
            self.insertar(y)
            
    def anula(self):
        self.listaclaus.clear()
        self.listavar.clear()
        self.unitprev.clear()


         
    
    def eliminar(self,x):
        try:
            self.listaclaus.remove(x)
        except:
            ValueError


        
                
    def eliminalista(self,x):
        for y in x:
            self.eliminar(y)
            
            
   

        
    def podaylimpia(self):
        inicial = len(self.listaclaus)
        y = []
        borr = []
        # print("entro en poda 2", len(self.listaclaus))
        self.listaclaus.sort(key = lambda x: len(x))
        # print("ordenadas")
        
        lista = self.listaclaus

        for i in range(len(lista)):
            clau1 = lista[i]
            for j in range(i+1,len(lista)):

                clau2 = lista[j]
                if clau2 in borr:
                    break
                claudif = (clau1-clau2)
                if (len(claudif) ==0):
                    borr.append(clau2)
                elif (len(claudif) ==1):
#                    print("poda", clau2)
                    var = claudif.pop()
                    if -var in clau2:
                        clau2.dicard(-var)
                        y.append(clau2)
        
        for clau in borr:
            self.eliminar(clau)
        
        while y:
#            print("original ibp",clau,len(self.listaclaus))
            clau = y.pop()
            y = self.podacola(clau)
#            print("original ibp",clau,len(self.listaclaus))

       
    def insertar(self,x):
        if not x:
            self.anula
            self.contradict= True
            self.listaclaus.append(set())
            return []
        y = []
        borr = []
        for cl in self.listaclaus:
            if not x == cl:
                if len(x) < len(cl):
                    claudif = x-cl
                    if not claudif:
                        borr.append(cl)
                    elif len(claudif) == 1:
                        var = claudif.pop()
                        if -var in cl:
                            cl.discard(-var)
                            y.append(cl)
                else:
                    claudif = cl-x
                    if not claudif:
                        return []
                    elif len(claudif) == 1:
                        var = claudif.pop()
                        if -var in x:
                            x.discard(-var)
                            for cl in borr:
                                self.eliminar(cl)
                            self.insertar(x)
                            return []
        for cl in borr:
            self.eliminar(cl)
        nvar = set(map(abs,x))
        self.listavar.update(nvar)
        self.listaclaus.append(x)
        while y:
            cl = y.pop()
            y = y + self.podacola(cl)

    def combina(self,conj):
        for cl in conj.listaclaus:
            self.insertar(cl)
   
    def podacola(self,x):
        y = []
        borr = []
        for cl in self.listaclaus:
            if not x == cl:
                if len(x) < len(cl):
                    claudif = x-cl
                    if not claudif:
                        borr.append(cl)
                    elif len(claudif) == 1:
                        var = claudif.pop()
                        if -var in cl:
                            cl.discard(-var)
                            y.append(cl)
                else:
                    claudif = cl-x
                    if not claudif:
                        return []
                    elif len(claudif) == 1:
                        var = claudif.pop()
                        if -var in x:
                            x.discard(-var)
                            for cl in borr:
                                self.eliminar(cl)
                            return self.podacola(x)
        for cl in borr:
            self.eliminar(cl)
        return y
    
    
    def noesta(self,x):
        y = []
        borr = []
        for cl in self.listaclaus:
            if not x == cl:
                if len(x) < len(cl):
                    claudif = x-cl
                    if not claudif:
                        borr.append(cl)
                    elif len(claudif) == 1:
                        var = claudif.pop()
                        if -var in cl:
                            cl.discard(-var)
                            y.append(cl)
                else:
                    claudif = cl-x
                    if not claudif:
                        return []
                    elif len(claudif) == 1:
                        var = claudif.pop()
                        if -var in x:
                            x.discard(-var)
                            for cl in borr:
                                self.eliminar(cl)
                            self.insertar(x)
                            return []
        
  