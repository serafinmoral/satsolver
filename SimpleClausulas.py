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

    
    
    
                    
    
        
 
        
                    
  
        
     
  

        
    def insertar(self,x):
        if self.contradict or (0 in x):
            return
#        print("inserto ",x)
        if not x:
            self.anula()
            self.listaclaus.append(x)
            self.contradict=True
            return
        
        

        for y in x:
            if y in self.indices:
                self.indices[y].append(x)
            else:
                self.indices[y] = [x]
            if(abs(y) not in self.listavar):
                self.listavar.add(abs(y))
        self.listaclaus.append(x)
        
        if len(x)==1:
            p = next(iter(x))
            self.unitprev.add(p)
            self.unit.add(p)
            self.unitprop()  
           
           
  
   
 
            
  
            
    
            
            
    def insertaborraypoda(self,x):
        bor = []
        h = []
        insertar = True
        
        if x not in self.listaclaus:
            for z in self.listaclaus:
                if x <= z:
                    bor.append(z)
                elif z <= x:
                    return
                else:
                    for var in x:
                        if (-var in z) and (x-{var} <= z - {-var}):
                            h.append(frozenset(z-{-var}))
                            if len(z-{-var})==0:
#                                print("calusula Contradictoria ",z,x)
                                self.contradict= True
                                self.solved = True
#                                time.sleep(30)
                            elif len(z-{-var})==1:
#                                print("calusula Unitaria ",z,x)
                                self.unit.add((set(z-{-var})).pop())
                                self.unitprev.add(set((z-{-var})).pop())
                            bor.append(z)
                        elif (-var in z) and    (z - {-var} <= x-{var}):
                            h.append(frozenset(x-{var}))
                            if len(x-{-var})==0:
#                                print("calusula Contradictoria ",z,x)
                                self.contradict= True
                                self.solved = True
#                                time.sleep(30)
                            elif len(x-{-var})==1:
#                                print("calusula Unitaria ",z,x)
                                self.unit.add((x-{-var}).pop())
                                self.unitprev.add((x-{-var}).pop())
                            insertar = False
        
            if insertar:
#                print("inserto ", x)
                self.inserts(x)

                
            
            for cl in bor:
#                print("borro",cl,len(self.listaclaus))
                self.eliminar(cl)
            
            self.unitprop()
            
            for cl in h:
                
#                print("ibp",cl)
                if cl not in self.listaclaus:
#                    print("insertaar ", cl, len(self.listaclaus))
                    self.insertaborraypoda(cl)
#                    print("insertaar ", cl, len(self.listaclaus))
    
                               
                    
    def insertaborraypodarecnoin(self,x, insert=True, M=3, N=100):
        if self.contradict:
            return []

        bor = []
        h = []
#        print("inserto x",x) 
        if x not in self.listaclaus:
            if len(self.listaclaus)<= N:
                lista = self.listaclaus.copy()
            else: 
                z = set(x)

                if len(z)>M:
                    lar = max(z,key = lambda u: len(self.indices.get(u,set())))
                    lista = self.indices.get(lar,set()).copy()
                    z.discard(lar)
                else:
                    lista = self.listaclaus.copy()
            while len(lista)>N and len(z)>M :
                lar = max(z,key = lambda u: len(self.indices.get(u,set())))
                lista.intersection_update(self.indices.get(lar,set()))
                z.discard(lar)
            if len(lista)<=N:
                    for cl in lista:
                        if(len(cl) < len(x)):
                            cl1 = cl
                            cl2 = x
                        else:
                            cl1 = x
                            cl2 = cl
                            dif = set(cl1 - cl2)
                            if not dif:
                                if cl2 == x:
                                    insert = False
                                    break
                                else:
                                    bor.append(cl)
                            elif len(dif)==1:
                                var = dif.pop()
                                if -var in cl2:
                                    ncl = frozenset(cl2 - {-var})
                                    h.append(ncl)
                                    if not ncl:
                                        self.solved = True
                                        self.contradict = True
                                    if cl2 == x:
                                        insert = False
                                        break
                                    else:
                                        bor.append(cl2)
                                
            else:
                for p in z:
                    y = set(z)-{p}
                    if y:
                        lista2 = lista.copy()
                        for q in y:
                            if q in self.indices and len(lista2)>0:
                                lista2.intersection_update(self.indices[q])
                            else:
                                lista2 = set()
                                break

                        if (len(lista2)>0) and p in self.indices:
                           lista1 = lista2.intersection(self.indices[p])
                           for cl in lista1:
                               bor.append(cl)
#                               if cl == test:
#                                   print("aqui borro incluido",x,p)
                        if (len(lista)>0) and -p in self.indices:
                           lista1 = lista2.intersection(self.indices[-p])
                           for cl in lista1:
                               bor.append(cl) 
#                               if cl == test:
#                                   print("aqui borro",p,x, "añado " ,frozenset(cl - {-p}))
                               ncl = frozenset(cl - {-p})
                               h.append(ncl)
                               if not ncl:
                                   self.solved = True
                                   self.contradict = True
                                   self.inserts(x)

                                   return []
                        
                               
                               
                               
               
            for cl in bor:
#                if cl == test:
#                    print("aqui borro",x)
#                print("borro",cl,len(self.listaclaus))
                self.eliminar(cl)
                
            if insert:
                self.inserts(x)

            return h
        else:
            return []
                    
                    
    def insertaborraypodarec(self,x,  insert=True , M=3, N=10):
        if self.contradict:
            return []

        bor = []
        h = []
#        print("inserto x",x) 
        if x not in self.listaclaus:
            if len(self.listaclaus)<= N:
                lista = self.listaclaus.copy()
            else: 
                z = set(x)

                if len(z)>M:
                    lar = max(z,key = lambda u: len(self.indices.get(u,set())))
                    lista = self.indices.get(lar,set()).copy()
                    z.discard(lar)
                else:
                    lista = self.listaclaus.copy()
            while len(lista)>N and len(z)>M :
                lar = max(z,key = lambda u: len(self.indices.get(u,set())))
                lista.intersection_update(self.indices.get(lar,set()))
                z.discard(lar)
            if len(lista)<=N:
                    for cl in lista:
                        if(len(cl) < len(x)):
                            cl1 = cl
                            cl2 = x
                        else:
                            cl1 = x
                            cl2 = cl
                            dif = set(cl1 - cl2)
                            if not dif:
                                if cl2 == x:
                                    insert = False
                                    break
                                else:
                                    bor.append(cl)
                            elif len(dif)==1:
                                var = dif.pop()
                                if -var in cl2:
                                    ncl = frozenset(cl2 - {-var})
                                    h.append(ncl)
                                    if not ncl:
                                        self.solved = True
                                        self.contradict = True
                                    if cl2 == x:
                                        insert = False
                                        break
                                    else:
                                        bor.append(cl2)
                                
            else:
                for p in z:
                    y = set(z)-{p}
                    if y:
                        lista2 = lista.copy()
                        for q in y:
                            if q in self.indices and len(lista2)>0:
                                lista2.intersection_update(self.indices[q])
                            else:
                                lista2 = set()
                                break

                        if (len(lista2)>0) and p in self.indices:
                           lista1 = lista2.intersection(self.indices[p])
                           for cl in lista1:
                               bor.append(cl)
#                               if cl == test:
#                                   print("aqui borro incluido",x,p)
                        if (len(lista)>0) and -p in self.indices:
                           lista1 = lista2.intersection(self.indices[-p])
                           for cl in lista1:
                               bor.append(cl) 
#                               if cl == test:
#                                   print("aqui borro",p,x, "añado " ,frozenset(cl - {-p}))
                               ncl = frozenset(cl - {-p})
                               h.append(ncl)
                               if not ncl:
                                   self.solved = True
                                   self.contradict = True
                                   self.inserts(x)

                                   return []
                        
                               
                               
                               
               
            for cl in bor:
#                if cl == test:
#                    print("aqui borro",x)
#                print("borro",cl,len(self.listaclaus))
                self.eliminar(cl)
                
            if insert:
                self.inserts(x)

            for cl in h:
                self.insertaborraypodarec(cl)
        else:
            return []
                                    
    def insertasatura(self,cl,var):
        if cl in self.listaclaus:
            return []
        cola = []
        self.inserts(cl)
        if -var in cl:
            ivar = var
        else:
            ivar = -var
        
        borrar = []
        if ivar in self.indices:
            for cl2 in self.indices[ivar]:
                clr = resolution(var,cl,cl2)
                if 0 not in clr:
                    cola.append(clr)

        return cola


    

    def podacola(self,x):
        if self.contradict:
            return
        cola = []
        bor = []
#        print("inserto x",x) 
        for p in x:
               y = set(x)-{p}
               if y:
                   l = y.pop()
                   lista = self.indices.get(l,set()).copy()
                   for q in y:
                       if q in self.indices and len(lista)>0:
                           lista.intersection_update(self.indices[q])
                       else:
                           lista = set()
                           break

                   if (len(lista)>0) and p in self.indices:
                           lista1 = lista.intersection(self.indices[p])
                           for cl in lista1:
                               bor.append(cl)
#                               if cl == test:
#                                   print("aqui borro incluido",x,p)
                   if (len(lista)>0) and -p in self.indices:
                           lista1 = lista.intersection(self.indices[-p])
                           for cl in lista1:
                               bor.append(cl) 
#                               if cl == test:
#                                   print("aqui borro",p,x, "añado " ,frozenset(cl - {-p}))
                               ncl = frozenset(cl - {-p})
                               cola.append(ncl)
 
                               
                               
                               
 
        for cl in bor:
#                if cl == test:
#                    print("aqui borro",x)
#                print("borro",cl,len(self.listaclaus))
                self.eliminar(cl)
                
        return cola
            
      

   
    
            
    def borraincluidas(self,x):
        if len(x)==0:
            self.listaclaus = set()
            self.indices = dict()
            self.contradict = True
            self.solved = True
            return True
        else:
            y = list(x)
            z = y[0]
            if z in self.indices:
                inter = self.indices[z].copy()
                for i in range(1,len(y)):
                    z = y[i]
                    if z in self.indices:
                        inter.intersection_update( self.indices[z] )
                    else:
                        return False
            else:
                return False
            if (len(inter)>0):
                for z in inter:
#                    print ("borrando", z)
                    self.eliminar(z)
                    return True
            else:
                return False
                

 
                
   
            
        
        
    def anadirConjunto(self,z):
        for y in z:
            self.insertar(y)
            
    def anula(self):
        self.listaclaus.clear()
        self.listavar.clear()
        self.indices.clear()
        self.unitprev.clear()


         
    
    def eliminar(self,x):
        self.listaclaus.remove(x)
        for y in x:
            if y in self.indices:
                self.indices[y].discard(x)
                
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
                        self.indices[-var].discard(clau2)
        
        for clau in borr:
            self.eliminar(clau)
        
        for clau in y:
#            print("original ibp",clau,len(self.listaclaus))
            self.insertaborraypodarec(clau)
#            print("original ibp",clau,len(self.listaclaus))

       

    
   
    
    
    
    
  