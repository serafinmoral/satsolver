# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""

import itertools
         
from comunes import *  
import networkx as nx    

class simpleClausulas:
    def __init__(self):
         self.listaclaus = []
         self.contradict = False
         self.listavar = set()    
         self.solved = False
         self.solution = set()
         self.unit = set()
         self.two = dict()
         self.c3 = dict()


         
     
    
    def cgrafo(self):
        grafo = nx.Graph()
        
        grafo.add_nodes_from(self.listavar)
        
        for cl in self.listaclaus:
           for u in cl:
                   for v in cl:
                       if not abs(u)==abs(v):
                           grafo.add_edge(abs(u),abs(v))     

        for u in self.two:
            for v in self.two[u]:
               grafo.add_edge(abs(u),abs(v))      


        for u in self.two:
            for v in self.c3[u]:
                for w in self.c3[u][v]:
                   grafo.add_edge(abs(u),abs(v)) 
                   grafo.add_edge(abs(u),abs(w))    
                   grafo.add_edge(abs(w),abs(v))          
        return grafo  


    def calculalistatotal(self):
        
        lista = self.listaclaus.copy()
        for x in self.two:
             for y in self.two[x]:
                 lista.append({x,y})

        for u in self.c3:
            for v in self.c3[u]:
                for w in self.c3[u][v]:
                   lista.append({u,v,w})   
        return lista
    
        
    def compruebasol2(self,config):
        conf = set(config)
        if not self.unit <= conf:
            print("Solucion no valida")
            print(config)
            print("unitarias", self.unit)
            return False

        for x in self.two:
            if not x in conf:
                if not self.two[x] <= conf:
                    print("Solucion no valida")
                    print(config)
                    print("dobles", x, ":", self.two[x])
                    return False

        for x in self.c3:
            if not x in conf:
                for y in self.c3[x]:
                    if not y in conf:
                        if not self.c3[x][y] <= conf:
                            print("Solucion no valida")
                            print(config)
                            print("triples ", x, y, ":", self.c3[x][y])
                            return False


        for y in self.listaclaus:
            inte = conf.intersection(y)
            if not inte:
                print("solucion no valida ")
                print(config)
                print("clausula ",y)
                return False
        print ("correcto")
        return True  
                        
            
   
    def imprime(self):
        print("v",self.listavar)
        print("u",self.unit)
        print("d")
        for x in self.two:
            print (x, ":", self.two[x])
        print("t")
        for x in self.c3:
            for y in self.c3[x]:
                print (x, y ,":", self.c3[x][y])
    
        print("c",self.listaclaus)  
        
                
    def copia(self):
      nuevo = simpleClausulas()
      nuevo.listavar = self.listavar.copy()
      nuevo.unit = self.unit.copy()
      nuevo.contradict = self.contradict
      
      for x in self.two:
          nuevo.two[x] = self.two[x].copy()

      for x in self.c3:
          nuevo.c3[x] = dict()
          for y in self.c3[x]:
            nuevo.c3[x][y] = self.c3[x][y].copy()
      
      for x in self.listaclaus:
          nuevo.listaclaus.append(x.copy())
          
      return nuevo

    def checkvars(self):
        for x in self.unit:
            if abs(x) not in self.listavar:
                print("problema " , x , self.listavar)
                return True

        for x in self.two:
            if (abs(x) not in self.listavar) and self.two[x]:
                print("problema doble" , x , self.two[x], self.listavar)
                return True    
            for y in self.two[x]:
                if (abs(y) not in self.listavar):
                    print("problema doble" , x , self.two[x], self.listavar)
                    return True

        for x in self.c3:
            isx = abs(x)  in self.listavar
            for y in self.c3[x]:
                if self.c3[x][y] and (not isx or not abs(y) in self.listavar):
                    print("problema triple" , x ,y, self.c3[x][y], self.listavar)
                    return True 
                for z in self.c3[x][y]:
                    if not abs(z) in self.listavar:
                        print("problema triple" , x ,y, self.c3[x][y], self.listavar) 

        
        for cl in self.listaclaus:
            for x in cl:
              if abs(x) not in self.listavar:
                print("problema " , cl , self.listavar)
                return True  
        return False

    def copiac(self,conf):
        confn= set(map(lambda x: -x ,conf))
        varn = set(map(lambda x: abs(x) ,conf))
        nuevo = simpleClausulas()
        nuevo.listavar = self.listavar.union(varn)
        for x in self.unit:
          if -x not in conf:
              cl = conf.union({x})
              nuevo.insertar(cl)
        for x in self.two:
          if -x not in conf:
              for y in self.two[x]:
                  if -y not in conf:
                      cl = conf.union({x,y})
                      nuevo.insertars(cl)

        for x in self.c3:
          if -x not in conf:
              for y in self.c3[x]:
                  if -y not in conf:
                      for z in self.c3[x][y]:
                          if -z not in conf:
                              cl  = conf.union({x,y,z})
                              nuevo.insertars(cl) 
      
        for x in self.listaclaus:
            if not confn.intersection(x):
                cl = conf.union(x)
                nuevo.listaclaus.append(cl)
          
        return nuevo

    
    
    

    
 
            
  
            
    
            
            
   
   
            
        
        
    def anadirConjunto(self,z):
        for y in z:
            self.insertar(y)
            
    def anula(self):
        self.listaclaus.clear()
        self.listavar.clear()
        self.unit.clear()
        self.two.clear()
        self.c3.clear()
        self.contradict = False


    
    def eliminars(self,x):
        
        try:
            self.listaclaus.remove(x)
        except:
            ValueError


             
    
    def eliminar(self,x):
        if len(x) == 1:
            v = x.pop()
            self.unit.discard(v)
            return
        if len(x) == 2:
            t1 = x.pop()
            t2 = x.pop()
            if abs(t1) <= abs(t2):
                r1 = t1
                r2 = t2
            else:
                r1 = t2
                r2 = t1
            if r1 in self.two:
                self.two[r1].discard(r2)
            return
        if len(x) == 3:
            t1 = min (x, key = lambda h: abs(h))
            x.discard(t1)
            if t1 in self.c3:
                t2 = min (x, key = lambda h: abs(h))
                x.discard(t2)
                if t2 in self.c3[t1]:
                    t3 = x.pop()
                    self.c3[t1][t2].discard(t3)
                    if not self.c3[t1][t2]:
                        self.c3[t1].pop(t2)
                        if not self.c3[t1]:
                            self.c3.pop(t1)
            return



            
        try:
            self.listaclaus.remove(x)
        except:
            ValueError


        
                
    def eliminalista(self,x):
        for y in x:
            self.eliminar(y)
            
            
    def insertars(self,x):
        return self.insertar(x,check=False)
    
    # def equiv(self,r1,r2):
    #     ins = []
    #     borr = []
    #     for x in self.two:
    #         if not x == r1 and not x == -r1:
    #             if r2 in self.two[x]:
    #                 ins.append({x,r1})
    #                 self.two[x].discard(r2)
    #             if -r2 in self.two[x]:
    #                 ins.append({x,-r1})
    #                 self.two[x].discard(-r2)
    #     if r2 in self.two:
    #         for x in self.two[r2]:
    #                 ins.append({x,r1})
    #         self.two.pop(r2)
    #     if -r2 in self.two:
    #         for x in self.two[-r2]:
    #                 ins.append({x,-r1})
    #         self.two.pop(-r2)   


    #     for cl in self.listaclaus:
    #         if r2 in cl:
    #             borr.append(cl)
    #             if not -r1 in cl:
    #                 cln = cl-{r2}
    #                 cln.add(r1)
    #                 ins.append(cln)
    #         if -r2 in cl:
    #             borr.append(cl)
    #             if not r1 in cl:
    #                 cln = cl-{-r2}
    #                 cln.add(-r1)
    #                 ins.append(cln)



    #     for cl in borr:
    #         self.eliminar(cl)
        
    #     for cl in ins:
    #         self.insertar(cl)


    def reduce3(self,xc):
        for x in self.c3.keys():
            if x in xc:
                for y in self.c3[x]:
                    if y in xc:
                        for z in self.c3[x][y]:
                            if z in xc:
                                return True
                            elif -z in xc:
                                xc.discard(-z)
                                return False
                    elif -y in xc:
                        if  self.c3[x][y].intersection(xc):
                                xc.discard(-y)
                                return False
            elif -x in xc:
               for y in self.c3[x]:
                    if y in xc:
                        if  self.c3[x][y].intersection(xc):
                            xc.discard(-x)
                            return False
        return False   


    def insertar3(self,xc):
        
        lo = list(xc)
        lo.sort(key = lambda h: abs(h))
        t0 = lo[0]
        t1 = lo[1]
        t2 = lo[2]
        self.listavar.update({abs(t0),abs(t1),abs(t2)})

        if t0 in self.c3:
            if t1 in self.c3[t0]:
                self.c3[t0][t1].add(t2)
            else:
                self.c3[t0][t1] = {t2}
        else:
            self.c3[t0] = dict()
            self.c3[t0][t1] = {t2}
        borra = []
        inserta = []
        for cl in self.listaclaus:
            if t0 in cl:
                if t1 in cl:
                    if t2 in cl:
                        borra.append(cl)
                    elif -t2 in cl:
                        borra.append(cl)
                        cln = cl-{-t2}
                        inserta.append(cln)
                elif -t1 in cl and t2 in cl:
                    borra.append(cl)
                    cln = cl-{-t1}
                    inserta.append(cln)
            elif {-t0,t1,t2} <= cl:
                borra.append(cl)
                cln = cl-{-t0}
                inserta.append(cln)
            
        for cl in borra:
            self.eliminar(cl)
        for cl in inserta:
            self.insertar(cl)


    def insertau(self,v):
        
        self.simplificaunit(v)
        if not self.contradict:
            self.unit.add(v)
            self.listavar.add(abs(v))

    def simplificaunit(self,v):
        if -v in self.unit:
            self.insertar(set())
            return []
        elif v in self.unit:
            self.unit.discard(v)
            self.listavar.discard(abs(v))

        else:
            ins = []
            borr = []
            self.listavar.discard(abs(v))

            
            if v in self.two and self.two[v]:
                self.two.pop(v)
            if -v in self.two and self.two[-v]:
                listau = self.two.pop(-v)
                for r in listau:
                    ins.append({r})
            for z in self.two:
                if v in self.two[z]:
                    self.two[z].discard(v)
                elif -v in self.two[z]:
                    self.two[z] = set()
                    ins.append({z})
            if v in self.c3:
                self.c3.pop(v)
            if -v in self.c3:
                aux = self.c3.pop(-v)
                for w in aux:
                    for z in aux[w]:
                        ins.append({w,z})
            for z in self.c3:
                if v in self.c3[z]:
                    self.c3[z].pop(v)
                if -v in self.c3[z]:
                    aux = self.c3[z].pop(-v)
                    for h in aux:
                        ins.append({z,h})
                for w in self.c3[z]:
                    self.c3[z][w].discard(v)
                    if -v in self.c3[z][w]:
                        ins.append({z,w})
                        self.c3[z][w] = set()



                


            for cl in self.listaclaus:
                if v in cl:
                    borr.append(cl)
                if -v in cl:
                    borr.append(cl)
                    cl1 = cl.copy()
                    cl1.discard(-v)
                    ins.append(cl1)
            for cl in borr:
                self.eliminar(cl)
            
            for cl in ins:
                self.insertar(cl)

    def simplificaunits(self,s):
        neg = set(map (lambda x: -x,s))

        if self.unit.intersection(neg):
            self.insertar(set())
        else:
            absv = set(map (lambda x: abs(x),s))

            self.unit.difference_update(s)

            self.listavar.difference_update(absv)
            ins = []
            borr = []


            for x in self.c3:
                if -x in s:
                    for y in self.c3[x]:
                        if -y in s:
                            for z in self.c3[x][y]:
                                if -z in s:
                                    self.insertar(set())
                                    return
                                elif z not in s:
                                    ins.append({z})
                        elif not y in s:
                            for z in self.c3[x][y]:
                                if -z in s:
                                    ins.append({y})
                                    break
                                elif not z in s:
                                    ins.append({y,z})
                    self.c3[x] = dict()
                elif x in s:
                    self.c3[x] = dict()

                else: 
                    for y in self.c3[x]:
                        if -y in s:
                            for z in self.c3[x][y]:
                                if -z in s:
                                    ins.append({x})
                                    break
                                elif not z in s:
                                    ins.append({x,z})
                            self.c3[x][y] = set()
                        elif y in s:
                            self.c3[x][y] = set()
                        else:
                            if neg.intersection( self.c3[x][y]):
                                ins.append({x,y})
        
                            self.c3[x][y].difference_update(s)



                
                            
            for x in self.two:
                if -x in s:
                    for y in self.two[x]:
                        if -y in s:
                            self.insertar(set())
                            return
                        elif y not in s:
                            ins.append({y})
                    self.two[x] = set()

                elif x in s:
                    self.two[x] = set()


                else: 
    
                    for y in self.two[x]:
                        if -y in s:
                            self.two[x] = set()
                            ins.append({x})
                            break
                    self.two[x].difference_update(s)

            for cl in self.listaclaus:
    
                if cl.intersection(s):
                    borr.append(cl)
                elif cl.intersection(neg):
                    borr.append(cl)
                    cl2 = cl-neg
                    ins.append(cl2)
         

            for cl in borr:
                self.eliminars(cl)
            for cl in ins:
                self.insertar(cl)

        
    def insertar(self,x, check = True):

        # neg = set(map(lambda h: -h, x))
        # if neg.intersection(x):
        #     print("problema insercion" , x)
        #     time.sleep(30)

        if self.contradict:
            return []
        if not x:
            self.anula()
            self.contradict= True
            self.listaclaus.append(set())
            return []
        y = []
        borr = []
        if len(x) ==1:
            v = x.pop()
            if v in self.unit:
                return []
            self.insertau(v)
            
        else:

            if x.intersection(self.unit):
                return []
            else:
                neg = set(map(lambda x: -x, self.unit))

                xc = x-neg

                if len(xc) <= 1:
                    self.insertar(xc)
                    return []

                ox = list(xc)
                ox.sort(key = lambda h: abs(h))

                for i in range(len(ox)):
                    for j in range(i+1,len(ox)):
                        r1 = ox[i]
                        r2 = ox[j]
                        if r2 in self.two.get(r1,set()):
                            return[]
                        if r2 in self.two.get(-r1,set()):
                            xc.discard(r1)
                            self.insertar(xc)
                            return []   
                        if -r2 in self.two.get(r1,set()):
                            xc.discard(r2)
                            self.insertar(xc)
                            return []  

                            
                if len(xc) >= 3:
                    ol = len(xc)
                    implicado = self.reduce3(xc)
                    if implicado:
                        return
                    elif len(xc)< ol:
                        return self.insertar(xc)



                          
                
                
                

                if len(xc) == 2:
                   
                    t1 = xc.pop()
                    t2 = xc.pop()
                    if abs(t1) <= abs(t2):
                        r1 = t1
                        r2 = t2
                    else:
                        r1 = t2
                        r2 = t1
                    
                    

                    for cl in self.listaclaus:
                        if r1 in  cl:
                            if r2 in cl:
                                borr.append(cl)
                            elif -r2 in cl:
                                clc = cl.copy()
                                clc.discard(-r2)
                                
                                y.append(clc)
                                borr.append(cl)
                        if -r1 in cl and r2 in cl:
                                clc = cl.copy()
                                clc.discard(-r1)
                                
                                y.append(clc)
                                borr.append(cl)
                        

                    if r1 in self.c3:
                        if r2 in self.c3[r1]:
                            self.c3[r1].pop(r2)
                        if -r2 in self.c3[r1]:
                            aux = self.c3[r1].pop(-r2)
                            for w in aux:
                                y.append({r1,w})
                        for v in self.c3[r1]:
                            if abs(v) < abs(r2):
                                self.c3[r1][v].discard(r2)
                                if -r2 in self.c3[r1][v]:
                                    y.append({r1,v})
                                    self.c3[r1][v] = set()
                            
                            
                        

                    for u in self.c3:
                        if abs(u)<abs(r1):
                            if r1 in self.c3[u]:
                               
                                   self.c3[u][r1].discard(r2)
                                   if -r2 in self.c3[u][r1]:
                                       self.c3[u].pop(r1) 
                                       y.append({u,r1})
                            elif -r1 in self.c3[u] and r2 in self.c3[u][-r1]:
                                        self.c3[u][-r1].discard(r2)
                                        y.append({u,r2})
                                
                    

                            
                        


                    if r1 in self.two:
                        self.two[r1].add(r2)
                    else:
                        self.two[r1] = {r2}

                    self.listavar.update({abs(r1),abs(r2)})
    
                    

                    for cl in borr:
                        self.eliminar(cl)
        
                    for cl in y:
                        self.insertar(cl)

                    # if -r1 in self.two and -r2 in self.two[-r1]:
                    #     self.equiv(r1,-r2)


                    return []

                    
                if len(xc) == 3:
                    return self.insertar3(xc)



                

            
            if check:

                for cl in self.listaclaus:
                    if len(xc) <= len(cl):
                        claudif = xc-cl
                        if not claudif:
                            borr.append(cl)
                        elif len(claudif) == 1:
                            var = claudif.pop()
                            if -var in cl:
                                clc = cl.copy()
                                clc.discard(-var)
                                borr.append(cl)
                                y.append(clc)
                    if len(cl) <= len(xc):
                        claudif = cl-xc
                        if not claudif:
                            return []
                        elif len(claudif) == 1:
                            var = claudif.pop()
                            if -var in xc:
                                xc.discard(-var)
                                self.insertar(xc)
                                return []
            nvar = set(map(abs,xc))
            self.listavar.update(nvar)
            self.listaclaus.append(xc)

        for cl in borr:
            self.eliminar(cl)
        
        for cl in y:
            self.insertar(cl)
            
    def insertars3(self,cl):
        lo = list(cl)
        lo.sort(key = lambda h: abs(h))
        t0 = lo[0]
        t1 = lo[1]
        t2 = lo[2]
        if t0 in self.c3:
            if t1 in self.c3[t0]:
                self.c3[t0][t1].add(t2)
            else:
                self.c3[t0][t1] = {t2}
        else:
            self.c3[t0] = dict()
            self.c3[t0][t1] = {t2}

    def insertars2(self,cl):
        t1 = cl.pop()
        t2 = cl.pop()
        if abs(t1) <= abs(t2):
            r1 = t1
            r2 = t2
        else:
            r1 = t2
            r2 = t1
        if r1 in self.two:
            self.two[r1].add(r2)
        else:
            self.two[r1] = {r2}

    def advalue(self,v):
        self.listavar.add(abs(v))
        if self.contradict:
            self.contradict = False
            self.unit = {v}
            self.listaclaus = []
            self.two = dict()
            return
        for cl in self.listaclaus:
            cl.add(v)

        

        for x in self.c3:
            for y in self.c3[x]:
                for z in self.c3[x][y]:
                    self.listaclaus.append({x,y,z,v})
        self.c3 = dict()
        
        for x in self.two:
            for y in self.two[x]:
                cl = {x,y,v}
                self.insertars3(cl)
        self.two = dict()
        for x in self.unit:
            self.insertars2({x,v})
        self.unit = set()

    def adconfig(self,conf):
        if self.contradict and conf:
            self.contradict = False
            self.anula()
            self.insertar(conf.copy())
            return
        
        if conf:
            if len(conf) == 1:
                v = conf.copy().pop()
                self.advalue(v)
                return
            for x in conf:
                self.listavar.add(abs(x))
            
            for cl in self.listaclaus:
                cl.update(conf)

            for x in self.c3:
                for y in self.c3[x]:
                    for z in self.c3[x][y]:
                        self.listaclaus.append({x,y,z}.union(conf))
            self.c3= dict()

        
            for x in self.two:
                for y in self.two[x]:
                    cl = conf.union({x,y})
                    self.listaclaus.append(cl)
            self.two = dict()
            if len(conf)==2:
                for x in self.unit:
                        cl = conf.union({x})
                        self.insertars3(cl)
            else:
                for x in self.unit:
                        cl = conf.union({x})
                        self.listaclaus.append(cl)
            self.unit = set()

           


    def combina(self,simple, check = True):
        if self.contradict:
            return
        if simple.contradict:
            self.insertar(set())
            return

        neg = set(map(lambda x: -x, simple.unit))
        if neg.intersection(self.unit):
            self.insertar(set())
        else:
            for v in simple.unit:
                self.insertar({v},check)
            for x in simple.two:
                for y in simple.two[x]:
                    self.insertar({x,y},check)

            for x in simple.c3:
                for y in simple.c3[x]:
                    for z in simple.c3[x][y]:
                        self.insertar({x,y,z},check)
        
            for cl in simple.listaclaus:
                self.insertar(cl,check)
   
   

    def nulo(self):
        if self.unit or self.listaclaus:
            return False
        for x in self.two:
            if self.two[x]:
                return False
        for x in self.c3:
            for y in self.c3[x]:
                if self.c3[x][y]:
                    return False
        return True

    def normaliza(self):
        aux = []
        for x in self.two:
            if not self.two[x]:
                aux.append(x)
        for x in aux:
            self.two.pop(x)

        aux = []
        for x in self.c3:
            aux2 = []
            for y in self.c3[x]:
                if not self.c3[x][y]:
                    aux2.append(y)
            for y in aux2:
                self.c3[x].pop(y)
            if not self.c3[x]:
                aux.append(x)
        for x in aux:
            self.c3.pop(x)




    def combinaborra(self,conj):
        # print("combina borra" , len(self.listaclaus), len(conj.listaclaus))
        res = simpleClausulas()
        if self.contradict:
            return conj.copia()
        if conj.contradict:
            return self.copia()

        for v in self.unit:
            for x in conj.unit:
                if not v == -x:
                    cl = {v,x}
                    res.insertar(cl)
            for x in conj.two:
                if not v == -x:
                    for y in conj.two[x]:
                        if not v == -y:
                            cl = {v,x,y}
                            res.insertar(cl)
            for x in conj.c3:
                if not v==-x:
                    for y in conj.c3[x]:
                        if not v == -y:
                            for z in conj.c3[x][y]:
                                if not v == -z:
                                    res.insertar({x,y,z,v})
            for cl in conj.listaclaus:
                if -v not in cl:
                    r = cl.union({v})
                    res.insertar(r)

        for x in self.two:
            for y in self.two[x]:
                for u in conj.two:
                    if not (u==-x) and not (u == -y):
                        for v in conj.two[u]:
                            if not (v==-x) and not (v == -y):
                                # print(u,v)
                                cl = {u,v,x,y}
                                # print(cl)
                                res.insertar(cl)
                                # res.imprime()
                for cl in conj.listaclaus:
                    if -x not in cl and -y not in cl:
                        r = cl.union({x,y})
                        res.insertar(r)
                for u in conj.c3:
                    if not (u==-x) and not (u == -y):
                        for v in conj.c3[u]:
                            if not (v==-x) and not (v == -y):
                                for w in conj.c3[u][v]:
                                    if not (w==-x) and not (w == -y):
                                        res.insertar({u,v,w,x,y})
        
        for x in self.c3:
            for y in self.c3[x]:
                for z in self.c3[x][y]:
                    for u in conj.c3:
                        if not -u == x and not -u == y and not -u == z:
                            for v in conj.c3[u]:
                               if not -v == x and not -v == y and not -v == z: 
                                    for w in conj.c3[u][v]:
                                        if not -w == x and not -w == y and not -w == z:
                                            res.insertar({x,y,z,u,v,w})
                    for cl in conj.listaclaus:
                        if not -x in cl and not -y in cl and not -z in cl:
                            res.insertar(cl.union({x,y,z})) 

        for x in conj.unit:
            for v in self.two:
                if not v == -x:
                    for y in self.two[v]:
                        if not x == -y:
                            cl = {v,x,y}
                            res.insertar(cl)
            for cl in self.listaclaus:
                if not -x in cl:
                    r = cl.union({x})
                    res.insertar(r)
            for u in self.c3:
                if not u == -x:
                    for v in self.c3[u]:
                        if not v == -x:
                            for w in self.c3[u][v]:
                                if not w == -x:
                                    res.insertar({u,v,w,x})



        for x in conj.two:
            for y in  conj.two[x]:
                for u in self.c3:
                    if not -x == u and not -y == u:
                        for v in self.c3[u]:
                            if not -x == v and not -y == v:
                               for w in self.c3[u][v]:
                                    if not -x == w and not -y == w:
                                        if x==-388 and y == -638:
                                            print("la inserto")
                                        res.insertar({u,v,w,x,y})



                for cl in self.listaclaus:
                    if -x not in cl and not -y  in cl:
                        r = cl.union({x,y})
                        res.insertar(r)

        for x in conj.c3:
            for y in conj.c3[x]:
                for z in conj.c3[x][y]:
                    for cl in self.listaclaus:
                        if not -x in cl and not -y in cl and not -z in cl:
                            res.insertar(cl.union({x,y,z})) 

        for cl in self.listaclaus:
            cpn = set(map(lambda x: -x, cl))
            for cl2 in conj.listaclaus:
                if not cpn.intersection(cl2):
                    r = cl.union(cl2)
                    res.insertar(r)
        # print("Salgo ") 


        return res


    def combinaborrac(self,conj,conf):
        # print("combina borra conf" , conf, len(self.listaclaus), len(conj.listaclaus))

        if not conf:
            return self.combinaborra(conj)
        else:
            r1 = self.copiac(conf)
            return r1.combinaborra(conj)
        

        


    def sel(self,v):
        result = simpleClausulas()
        if v in self.unit:
            result.insertar(set())
            return result
        for x in self.unit:
            if not x == -v:
                result.insertar({x}) 

        for x in self.two:
            if x== v:
                for y in self.two[x]:
                    result.insertar({y})
            elif not x == -v:
                for y in self.two[x]:
                    if y == v:
                        result.insertar({x})
                        break
                    if not y == -v:
                       result.insertar({x,y})
            
        for x in self.c3:
            if x==v:
                for y in self.c3[x]:
                    for z in self.c3[x][y]:
                        result.insertar({y,z})
            elif not x==-v:
                for y in self.c3[x]:
                    if y == v:
                        for z in self.c3[x][y]:
                            result.insertar({x,z})
                    elif not y == -v:
                        for z in self.c3[x][y]:
                            if z == v:
                                result.insertar({x,y})
                            elif not z == -v:
                                result.insertar({x,y,z})

                     
        for cl in self.listaclaus:
            if v in  cl:
                result.insertar(cl-{v})
            elif not -v in cl:
                result.insertar(cl.copy())
        return result

    def selconf(self,conf):
        res = simpleClausulas()
        if conf.intersection(self.unit):
            res.insertar(set())
            return res
        for z in self.unit:
            if -z not in conf:
                res.insertars({z})

        for x in self.two:
            if x in conf:
                for y in self.two[x]:
                    if y in conf:
                        res.insertar((set()))
                        return res
                    if not -y in conf:
                        res.insertar({y})
            elif not -x in conf:
                for y in self.two[x]:
                    if y in conf:
                        res.insertar({x})
                        break
                    elif not -y in conf:
                        res.insertar({x,y})

        for x in self.c3:
            if x in conf:
                for y in self.c3[x]:
                    if y in conf:
                        for z in self.c3[x][y]:
                            if z in conf:
                                res.insertar((set()))
                                return res
                            elif not -z in conf:
                                res.insertar({z})
                    elif -y not in conf:
                        for z in self.c3[x][y]:
                            if z in conf:
                                res.insertar({y})
                            elif not -z in conf:
                                res.insertar({y,z})
            elif not -x in conf:
                for y in self.c3[x]:
                    if y in conf:
                        for z in self.c3[x][y]:
                            if z in conf:
                                res.insertar({x})
                            elif not -z in conf:
                                res.insertar({x,z})
                    elif -y not in conf:
                        for z in self.c3[x][y]:
                            if z in conf:
                                res.insertar({x,y})
                            elif not -z in conf:
                                res.insertar({x,y,z})


        confn= set(map(lambda x: -x, conf))
        for cl in self.listaclaus:
            if not cl.intersection(confn):
                x = cl - conf
                res.insertar(x)
        return res
    
    
    

    def splitborra(self,v,n=True):
        s1 = simpleClausulas()
        s2 = simpleClausulas()
        s3 = simpleClausulas()
        
        if v in self.unit:
            s1.insertar(set())
            for x in self.unit:
                if not x == v and not x==-v:
                    s3.insertars({x})
            

        elif -v in self.unit:
            s2.insertar(set())
            for x in self.unit:
                if  not x == v and not x==-v:
                    s3.insertars({x})

            
        else:

            s3.unit = self.unit.copy()
            s3.listavar = set(map(lambda x: abs(x),s3.unit))


        for x in self.two:
            if x == v:
                for y in self.two[x]:
                    s1.insertars({y})
            elif x == -v:
                for y in self.two[x]:
                    s2.insertars({y})
            else:
                for y in self.two[x]:
                    if y == v:
                        s1.insertars({x})
                    elif y == -v:
                        s2.insertars({x})
                    else:
                        s3.insertars({x,y})

        for x in self.c3:
            if x == v:
                for y in self.c3[x]:
                    for z in self.c3[x][y]:
                        s1.insertars({y,z})
            elif x == -v:
                for y in self.c3[x]:
                    for z in self.c3[x][y]:
                        s2.insertars({y,z})
            else:
                for y in self.c3[x]:
                    if y == v:
                        for z in self.c3[x][y]:
                            s1.insertars({x,z})
                    elif y == -v:
                        for z in self.c3[x][y]:
                            s2.insertars({x,z})
                    else:
                        for z in self.c3[x][y]:
                            if z == v:
                                s1.insertars({x,y})
                            elif z == -v:
                                s2.insertars({x,y})
                            else:
                                s3.insertars({x,y,z})


        for cl in self.listaclaus:
                if v in cl:
                    if n:
                        cl1 = cl - {v}
                        s1.insertars(cl1)
                    else:
                        cl.discard(v)
                        s1.insertars(cl)
                elif -v in cl:
                    if n:
                        cl1 = cl - {-v}
                        s2.insertars(cl1)
                    else:
                        cl.discard(-v)
                        s2.insertars(cl)
                else: 
                    if n:
                        cl1 = cl.copy()
                        s3.insertars(cl1)
                    else:
                        s3.insertars(cl)
        
        return (s1,s2,s3)

