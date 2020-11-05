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

    infor = globalClausulas()
    infor.nvar = nvar
    for cadena in reader:
#        print (cadena)
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= frozenset(listaux)
            infor.insertar(clausula)
            if(len(clausula)==1):
                h = set(clausula).pop()
                infor.unitprev.add(h)
            elif (len(clausula)==2):
                infor.dobles.add(clausula)
                mclau = frozenset(map(lambda x: -x,clausula))
                if mclau in infor.dobles:
                    par = set(clausula)
                    l1 = par.pop()
                    l2 = -par.pop()
                    if(abs(l1)<abs(l2)):
                        infor.equiv.add((l1,l2))
                    else:
                        infor.equiv.add((l2,l1))



#    print("paso a limpiar")
#    infor.limpiarec(0.0)
#    print("termino de limpiar")
    return infor  

 
    
class globalClausulas:
    def __init__(self):
         self.nvar = 0
         self.listaclaus = set()
         self.indices = dict()
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
        res = []
        while self.unitprev:
            p = self.unitprev.pop()

            res.append(p)
            
            self.listavar.discard(abs(p))

            if p in self.indices:
                borrar = set()
                for c in self.indices[p]:
                    
                        borrar.add(c)
                self.indices.pop(p)
                for c in borrar:
                    self.eliminar(c)
            if -p in self.indices:
                borrar = set()
                for c in self.indices[-p]:
                    borrar.add(c)
                self.indices.pop(-p)

                for c in borrar:
                    self.eliminar(c)


                    c2 = frozenset(set(c)-{-p})

                    self.insertar(c2)

                    if self.contradict:
                        return res
                    
                    
                    
                                    
        return res

   
         
    def calculaconjuntos(self):
        z = globalClausulas()
        for cla in self.listaclaus:
            posclau = frozenset(map(abs,cla))
            z.insertar(posclau)
        return z
    
    def computeComplV(self,y):
        conjunto = set({y})
        l=0
        if y in self.indices:
            l = len(self.indices[y])
            for z in self.indices[y]:
                conjunto.update(z)
#        print (y, conjunto)
        return (conjunto,l)
    
    
        
    def actualizab(self,var,conjunto):
        conjunto = frozenset(conjunto -{var})
        if (len(conjunto)>0):
            self.insertar(conjunto) 
        if var in self.indices:
            while bool(self.indices[var]):
#                print(self.indices[var])
                c = self.indices[var].pop()
                self.eliminar(c)
            

            
        
        return(ordenbo,varinorder)
        
        
    

     
   
        
    def extraePotentials(self,ordenbo):
            listpot = []
            for v in ordenbo:
                pot = self.extraeBorra(v)
                listpot.append(pot)
            return listpot
        
        
                
    def copia(self):
      nuevo = globalClausulas()
      nuevo.listavar = self.listavar.copy()
      
      for x in self.listaclaus:
          nuevo.insertar(x)
          
      return nuevo

    def divide(self,x):
        y1 = globalClausulas()
        y2 = globalClausulas()
       
        for cl in self.listaclaus:
            if (x not in cl) and (-x not in cl):
                y1.insertar(cl)
                y2.insertar(cl)
#                if (cl in self.re1er):
#                    y.refer[cl] = self.refer[cl]
            elif x in cl and not y2.contradict:
                cl2 = frozenset(cl-{x})
#                r1 = self.refer.get(cl,set())
#                r1.add(-x)
#                if not cl2 in self.refer:
#                    y.refer[cl2]=r1
#                else:
#                    r2 = self.refer[cl2]
#                
#                    if len(r1) < len(r2):
#                        y.refer[cl2]=r1
                
                y2.insertar(cl2)
                if not cl2:
                    y2.contradict = True
                elif len(cl2)==1:
                    y2.unitprev.add(set(cl2).pop())
#             
            elif -x in cl and not y1.contradict:
                cl2 = frozenset(cl-{-x})
#                r1 = self.refer.get(cl,set())
#                r1.add(-x)
#                if not cl2 in self.refer:
#                    y.refer[cl2]=r1
#                else:
#                    r2 = self.refer[cl2]
#                
#                    if len(r1) < len(r2):
#                        y.refer[cl2]=r1
                
                y1.insertar(cl2)
                if not cl2:
                    y1.contradict = True
                elif len(cl2)==1:
                    y1.unitprev.add(set(cl2).pop())
        
        
        y1.unitprop3()
        y2.unitprop3()
        return (y1,y2)

                
        
    def restringe(self,x):
        y = globalClausulas()
        y.listavar = self.listavar-{abs(x)}
        for cl in self.listaclaus:
            if (x not in cl) and (-x not in cl):
                y.insertar(cl)
#                if (cl in self.refer):
#                    y.refer[cl] = self.refer[cl]
            elif -x in cl:
                cl2 = frozenset(cl-{-x})
#                r1 = self.refer.get(cl,set())
#                r1.add(-x)
#                if not cl2 in self.refer:
#                    y.refer[cl2]=r1
#                else:
#                    r2 = self.refer[cl2]
#                
#                    if len(r1) < len(r2):
#                        y.refer[cl2]=r1
                if (cl2):
                    y.insertar(cl2)

                else:
                    y.listaclaus.clear()
                    y.insertar(cl2)
                    y.contradict = True
#                    y.apren = y.refer[cl2]
#                    print("Aprendo ·", y.apren)
                    break
                
        return y
    
    
    
    def restringeyparte(self,x):
        grafo = dict()
        for z in self.listavar:
            grafo[z] = set()
        
        y = globalClausulas()
        for cl in self.listaclaus:
            if (x not in cl) and (-x not in cl):
                y.insertar(cl)
#                y.refer[cl] = self.refer.get(x,set())
                for u in cl:
                   for v in cl:
                       if not abs(u)==abs(v):
                           grafo[abs(u)].add(abs(v))
                           grafo[abs(v)].add(abs(u))

                if (cl in self.refer):
                    y.refer[cl] = self.refer[cl]
            elif -x in cl:
                cl2 = frozenset(cl-{-x})
                r1 = set(self.refer.get(cl,set()).copy())
                r1.add(-x)
                y.refer[cl2]=r1
                
                if (cl2):
                    y.insertar(cl2)
                    for u in cl2:
                        for v in cl2:
                            if not abs(u)==abs(v):
                                grafo[abs(u)].add(abs(v))
                                grafo[abs(v)].add(abs(u))
#                    if(len(cl2) ==1):
#                         h = set(cl2).pop()
#                         y.unitprev.add(h)
#                         y.unit.add(h)
                else:
                    y.listaclaus.clear()
                    y.insertar(cl2)
                    y.contradict = True
                    y.solved = True
                    y.apren = y.refer[cl2]
#                    print("Aprendo ·", y.apren)
                    break
                
        if y.contradict or not y.listaclaus:
            return [y]
        
        lista = []
        total = y.listavar.copy()
        while y.listaclaus:
#            print(y.listaclaus)
#            print(v)
            v = total.pop()
            tosee = {v}
            seen = {v}
            while tosee:
                w = tosee.pop()
                vec = grafo[w]-seen
                seen.update(vec)
                tosee.update(vec)
            total.add(v)
            if seen == total:
                y.recomvar()
                lista.append(y)
                return lista
            else:
                h = globalClausulas()
                for cl in y.listaclaus:
                    posv = set(map(abs,cl))
                    if posv.intersection(seen):
                        h.insertar(cl)
                        h.refer[cl] = y.refer.get(cl,set())
                for cl in h.listaclaus:
                    y.eliminar(cl)
                total  = total - h.listavar
                lista.append(h)
        return lista             
                    
    
    def restringe2(self,x):
        y = globalClausulas()
        pos = 0
        y.listavar = self.listavar-{abs(x)}
        for cl in self.listaclaus:
            if (x not in cl) and (-x not in cl):
                y.insertar(cl)
#                if (cl in self.refer):
#                    y.refer[cl] = self.refer[cl]
            elif -x in cl:
                cl2 = frozenset(cl-{-x})
#                r1 = self.refer.get(cl,set())
#                r1.add(-x)
#                if not cl2 in self.refer:
#                    y.refer[cl2]=r1
#                else:
#                    r2 = self.refer[cl2]
#                
#                    if len(r1) < len(r2):
#                        y.refer[cl2]=r1
                if (cl2):
                    y.insertar(cl2)
            else:
                pos += 1
                
        return (y,pos)   
        
    
        
 
        
                    
  
        
     
  

        
    def insertar(self,x,M=3):
        if self.contradict or (0 in x):
            return
#        print("inserto ",x)
        if not x:
            self.anula()
            self.listaclaus.add(x)
            self.solved=True
            self.contradict=True
            return
        if x in self.listaclaus:
            return
        if len(x)==1:
            self.unitprev.add(set(x).pop())
            self.unit.add(set(x).pop())
            self.insertaborraypodarec(x)

        if len(x)>M:
            for y in x:
                if y in self.indices:
                    self.indices[y].add(x)
                else:
                    self.indices[y] = {x}
                if(abs(y) not in self.listavar):
                    self.listavar.add(abs(y))
            self.listaclaus.add(x)
            
        else:
           self.insertaborraypoda(x) 
           
           
           
  
    def inserts(self,x):
        if self.contradict or (0 in x) or x in self.listaclaus:
            return
#        print("inserto ",x)
        if not x:
            self.anula()
            self.listaclaus.add(x)
            self.solved=True
            self.contradict=True
            return
        
        if len(x)==1:
            self.unitprev.add(set(x).pop())
            self.unit.add(set(x).pop())
            
        for y in x:
            if y in self.indices:
                self.indices[y].add(x)
            else:
                self.indices[y] = {x}
            if(abs(y) not in self.listavar):
                self.listavar.add(abs(y))
        self.listaclaus.add(x)
       
        
         
 
            
  
            
    def insertayborra(self,x):
        if x not in self.listaclaus:
            h = self.borraincluidas(x)
            for y in x:
                if y in self.indices:
                    self.indices[y].add(x)
                else:
                    self.indices[y] = {x}

                if(abs(y) not in self.listavar):
                    self.listavar.add(abs(y))
            
            self.listaclaus.add(x)
            if len(x)==1:
                self.unitprev.add(set(x).pop())
            
            
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
                

 
                
   
    
    
    def extraeBorra(self,y):
        resultado = globalClausulas()
        for x in self.indices.get(y,[]):
            resultado.insertar(x)
        for x in self.indices.get(-y,[]):
            resultado.insertar(x)
        for x in resultado.listaclaus:
            self.eliminar(x)
        return resultado
    
    
    def split(self,y):
        con = globalClausulas()
        sin = globalClausulas()
        for cl in self.listaclaus:
            if (y not in cl) and (-y not in cl):
                sin.insertar(cl)
            else:
                con.insertar(cl)
        return (con,sin)
            
        
        
    def anadirConjunto(self,z):
        for y in z:
            self.insertar(y)
            
    def anula(self):
        self.listaclaus.clear()
        self.listavar.clear()
        self.indices.clear()
        self.unitprev.clear()


         
    
    def eliminar(self,x):
        self.listaclaus.discard(x)
        for y in x:
            if y in self.indices:
                self.indices[y].discard(x)
                
    def eliminalista(self,x):
        for y in x:
            self.eliminar(y)
            
            
    def entorno(self,clau):
        total = set()
        for x in clau:
            if -x in self.indices:
                for h in self.indices[-x]:
                    total.add(h)
        return total


    
        
            
    
    
    
    
    
                
                
    
    
    def eliminavar(self,var):
        l1 = self.indices.get(var,set())
        l2 = self.indices.get(-var,set())
        anadir = []
        
        for x in  list(itertools.product(l1,l2)):
            clau = resolution(var,x[0],x[1])
            if (0 not in clau):
                anadir.append(clau)
                
        lista = l1.union(l2)
        
        for cl in lista:
            self.eliminar(cl)
        for cl in anadir:
            self.insertar(cl)
                
            
            
        
    
    
    
    def bloqueo(self,c):
        hl = set(map(lambda x: -x,c))
        for x in c:
            bloque = True
            if (-x in self.indices):
                for y in self.indices[-x]:
                    if len( y  & hl)==1:
                        bloque = False 
                        break
            if bloque:
                break
        return bloque
    
 
        
    
    def bloqueogen(self,c,M=100):
        
        h = globalClausulas()
        
        ent = self.entorno(c)
        
        h.anadirConjunto(ent)
        var = len(self.listavar)+2
        
        lista = set(map(abs,c))
        
        cl = frozenset(c | {var})
        
        h.insertar(cl)
        
#        print(len(h.listaclaus))
        
        for v in lista:
            h.eliminavar(v)
            t = h.indices.get(var,set())
        
            if len(t)== 0:
                return True
            if len(h.listaclaus)>M:
                return False
            
        h.limpia(0.0)
        h.poda()
        
        t = h.indices.get(var,set())
        
        if len(t)== 0:
            return True
        else:
            return False
            
        
        
        
        
        
       
    

    def eliminarbloqueadas(self):
        bloqueadas = set()
        for c in self.listaclaus:
            if self.bloqueo(c):
                bloqueadas.add(c)
                print ("bloqueada ",c)
        for h in bloqueadas:
            self.eliminar(h)
            print ("eliminada ",h)
        if (len(bloqueadas)>1):
            return bloqueadas | self.eliminarbloqueadas()
        else:
            return bloqueadas
        
    def calcularbloqueadas(self):
        bloqueadas = set()
        for c in self.listaclaus:
            if self.bloqueo(c):
                bloqueadas.add(c)
                print ("bloqueada ",c)
        if (bloqueadas):
            for h in bloqueadas:
                self.eliminar(h)
                print ("eliminada ",h)
            bloqueadas = bloqueadas | self.eliminarbloqueadas()
            for h in bloqueadas:
                self.insertar(h)
            return bloqueadas
        else:
            return bloqueadas
        
    def calculartodasbloqueadas(self):
        bloqueadas = set()
        for c in self.listaclaus:
#            print (c)
            if self.bloqueogen(c):
                bloqueadas.add(c)
                print ("bloqueada ",c)
        return bloqueadas
                

    def poda(self):
        print("entro en poda")
        
        lista = self.listavar.copy()
        
        for var in lista:
            self.podavar2(var)
        print("salgo de poda")
    
        
    def podaylimpia(self):
        inicial = len(self.listaclaus)
        y = []
        borr = []
        # print("entro en poda 2", len(self.listaclaus))
        lista = sorted(self.listaclaus,key = lambda x: len(x))
        # print("ordenadas")
        
        for i in range(len(lista)):
            clau1 = lista[i]
            for j in range(i+1,len(lista)):

                clau2 = lista[j]
                if clau2 in borr:
                    break
                claudif = set(clau1-clau2)
                if (len(claudif) ==0):
 #                   print("borro", clau2)
                    borr.append(clau2)
                elif (len(claudif) ==1):
#                    print("poda", clau2)
                    var = claudif.pop()
                    if -var in clau2:
                        y.append(frozenset(clau2-{-var}))
                        borr.append(clau2)
        if(len(y) >len(borr)):
            print("añado mas que borro")

        for clau in borr:
            self.eliminar(clau)
        
        for clau in y:
#            print("original ibp",clau,len(self.listaclaus))
            self.insertaborraypodarec(clau)
#            print("original ibp",clau,len(self.listaclaus))

        if len(self.listaclaus)>inicial:
            print("warningggggggggggggggggggggg ")
        # print("salgo de poda 2")

    
    def podavar(self,var):
#        print("podando",var)
        y = []
        if(var in self.indices and -var in self.indices):
            listapos = self.indices[var]
            listaneg = self.indices[-var]
            for clau1 in listapos:
                for clau2 in listaneg:
                    if (clau1 - {var} <= clau2 -{-var}):
                        y.append(frozenset(clau2-{-var}))
#                        print ("podo con", clau2-{-var})
                    elif  (clau2 - {-var} <= clau1 -{var}): 
                        y.append(frozenset(clau1-{var}))
#                        print ("podo con", clau1-{var})
        for clau in y:
#            print("original ibp",clau,len(self.listaclaus))
            if (len(clau)>1):
                self.insertaborraypoda(clau)
            elif len(clau)==1:
                self.unit.add(set(clau).pop())
                self.unitprev.add(set(clau).pop())
                self.unitprop()
#                self.insertar(clau)
            else:
                self.solved=True
                self.contradict=True
#                self.insertar(clau)

            
    def podavar2(self,var):
#        print("podando",var)
        y = []
        borra = []
        if(var in self.indices and -var in self.indices):
            listapos = self.indices[var]
            listaneg = self.indices[-var]
            for clau1 in listapos:
                for clau2 in listaneg:
                    if (clau1 - {var} <= clau2 -{-var}):
                        borra.append(clau2)
                        y.append(clau2-{-var})
#                        print ("podo con", clau2-{-var})
                    elif  (clau2 - {-var} <= clau1 -{var}): 
                        y.append(clau1-{var})
                        borra.append(clau1)
#                        print ("podo con", clau1-{var})
        for clau in borra:
            self.eliminar(clau)
        
        for clau in y:
            if not clau:
                self.solved=True
                self.contradict=True
            self.insertar(clau)
        
    
    
    
    
    
    
        
    def limpia2(self):
        if(len(self.listaclaus)<2):
            return
        
        nuevas = list(self.listaclaus)
        nuevas.sort(key=lambda x: len(x))
        i1 = 0
        i2 = len(nuevas)-1 
        
        while (i1<(len(nuevas)-1)  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if cl1<=cl2:
                del nuevas[i2]
                self.eliminar(cl2)
            i2=i2-1
            if (i2 ==i1):
                i1=i1+1
                i2 = len(nuevas)-1 
                        
        
    def limpia(self,th):
        if(len(self.listaclaus)<2):
            return
        
        nuevas = list(self.listaclaus)
        nuevas.sort(key=lambda x: len(x))
        i1 = 0
        i2 = len(nuevas)-1 
        
        while (i1<(len(nuevas)-1)  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if casicontenida(cl1,cl2,th):
                del nuevas[i2]
                self.eliminar(cl2)
            i2=i2-1
            if (i2 ==i1):
                i1=i1+1
                i2 = len(nuevas)-1 
                
                
    
        
    
 
            
    def combina(self,conjunto):
#        self.listavar.update(conjunto.listavar)
#        self.listaclaus.update(conjunto.listaclaus)
#        for x in conjunto.indices:
#            if x in self.indices:
#                self.indices[x].update(conjunto.indices[x])
#            else:
#                self.indices[x] = conjunto.indices[x].copy()
        for x in conjunto.listaclaus:
            self.insertar(x)
#            self.limpiarec(0.0)
                           
    
    def podaylimpiarec(self,M=4000):
        if len(self.listaclaus)<=M:
            self.podaylimpia()
        else:
            var = max(self.listavar, key=lambda x: len(self.indices.get(x,set()))* len(self.indices.get(-x,set())) )      

            listano = globalClausulas()
            listap = globalClausulas()
            listanop = globalClausulas()  

            conp =  self.indices.get(var,set()) 
            connop =  self.indices.get(-var,set())
            conno = self.listaclaus - conp - connop 

            listap.anadirConjunto(conp)
            listanop.anadirConjunto(connop)
            listano.anadirConjunto(conno)

            listap.podaylimpiarec()
            listanop.podaylimpiarec()
            listano.podaylimpiarec()

            self.anula()
            self.combina(listap)
            self.combina(listanop)
            self.combina(listano)
