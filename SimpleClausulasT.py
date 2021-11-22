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

        for u in self.two:
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
            print (x, y ":", self.c3[x][y])
    
        print("c",self.listaclaus)  
        
                
    def copia(self):
      nuevo = simpleClausulas()
      nuevo.listavar = self.listavar.copy()
      nuevo.unit = self.unit.copy()
      nuevo.contradict = self.contradict
      
      for x in self.two:
          nuevo.two[x] = self.two[x].copy()

      for x in self.c3:
          for y in self.c3[x]:
            nuevo.c3[x][y] = self.c3[x][y].copy()
      
      for x in self.listaclaus:
          nuevo.insertar(x.copy())
          
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

                ]
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
        if self.contradict:
            return 
        nvar = set(map(abs,x))
        self.listavar.update(nvar)
        if len(x)==1:
            self.unit.add(x.copy().pop())
        elif len(x) == 2:
            xc = x.copy()
            t1 = xc.pop()
            t2 = xc.pop()
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
        elif len(x) == 3:
            ol = list(x).order(key h: abs(h))
            t1 = ol[0]
            t2 = ol[1]
            t3 = ol[3]
            if t1 in self.c3:
                if t2 in self.c3[t1]:
                    self.c3[t1][t2].add(t3)
                else:
                    self.c3[t1][t2] = {t3}
            else:
                self.c3[t1] = dict()
                self.c3[t1][t2] = {t3}
        else:
            self.listaclaus.append(x)
    
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

    
    def insertar(self,x, check = True):
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
            if -v in self.unit:
                self.insertar(set())
                return []
            elif v not in self.unit:
                self.listavar.add(abs(v))
                self.unit.add(v)
                if v in self.two and self.two[v]:
                    self.two.pop(v)
                if -v in self.two and self.two[-v]:
                    listau = self.two.pop(-v)
                    for r in listau:
                        y.append({r})
                for z in self.two:
                    if v in self.two[z]:
                        self.two[z].discard(v)
                    elif -v in self.two[z]:
                        self.two[z] = set()
                        y.append({z})
                if v in self.c3:
                    self.c3.pop(v)
                if -v in self.c3:
                    aux = self.c3.pop(-v)
                for w in aux:
                    for z in aux[w]:
                        y.append({w,z})
                for z in self.c3:
                    if v in self.c3[z]:
                        self.c3[z].pop(v)
                    if -v in self.c3[z]:
                        aux = self.c3[z].pop(-v)
                        for h in aux:
                            y.append({z,h})
                    for w in self.c3[z]:
                        self.c3[z][w].discard(v)
                        if -v in self.c3[z][w]:
                            y.append({z,w})
                            self.c3[z].pop(w)
                            if not self.c3[z]:
                                self.c3.pop(z)


                    


                for cl in self.listaclaus:
                    if v in cl:
                        borr.append(cl)
                    if -v in cl:
                        borr.append(cl)
                        cl1 = cl.copy()
                        cl1.discard(-v)
                        y.append(cl1)
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
                        
                    
                    if r1 in self.two:
                        self.two[r1].add(r2)
                    else:
                        self.two[r1] = {r2}

                    self.listavar.update({abs(r1),abs(r2)})
    
                    

                    for cl in borr:
                        self.eliminar(cl)
        
                    for cl in y:
                        self.insertar(cl)

                    if -r1 in self.two and -r2 in self.two[-r1]:
                        self.equiv(r1,-r2)


                    return []

                    
                


                

            
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
        for x in self.two:
            for y in self.two[x]:
                cl = {x,y,v}
                self.listaclaus.append(cl)
            self.two[x] = set()
        for x in self.unit:
                if abs(v) <= abs(x):
                        r1 = v
                        r2 = x
                else:
                        r1 = x
                        r2 = v
                if r1 in self.two:
                    self.two[r1].add(r2)
                else:
                    self.two[r1] = {r2}
        
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
            
            
            for x in self.unit:
                    cl = conf.union({x})
                    
                    self.listaclaus.append(cl)
            self.unit = set()

            for x in self.two:
                for y in self.two[x]:
                    cl = conf.union({x,y})
                    self.listaclaus.append(cl)
                self.two[x] = set()


    def combina(self,simple, check = False):
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
        
            for cl in simple.listaclaus:
                self.insertar(cl,check)
   
   

    def nulo(self):
        if self.unit or self.listaclaus:
            return False
        for x in self.two:
            if self.two[x]:
                return False
        return True


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



        for x in conj.two:
            for y in  conj.two[x]:
                for cl in self.listaclaus:
                    if -x not in cl and not -y  in cl:
                        r = cl.union({x,y})
                        res.insertar(r)


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

            

        confn= set(map(lambda x: -x, conf))
        for cl in self.listaclaus:
            if not cl.intersection(confn):
                x = cl - conf
                res.insertar(x)
        return res
    
    def simplificaunit(self,v):
        if -v in self.unit:
            self.insertar(set())
            return 
        self.listavar.discard(abs(v))

        if v in self.unit:
            self.unit.discard(v)
        else:
            ins = []
            borr = []
            for x in self.two:
                if -v == x:
                    for y in self.two[x]:
                        ins.append({y})
                    self.two[x] = set()

                elif v == x:
                    self.two[x] = set()

                else:
                    
                    for y in self.two[x]:
                        if -v == y:
                            ins.append({x})
                            break
                    
                    self.two[x].discard(v)    
                            


            for cl in self.listaclaus:
                if -v in cl:
                    borr.append(cl)
                    clc = cl-{-v}
                    ins.append(clc)
                elif v in cl:
                    borr.append(cl)
            for cl in borr:
                self.eliminars(cl)
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


# def splitinserta(self,v,n=True):
#         s1 = simpleClausulas()
#         s2 = simpleClausulas()
#         if not v in self.listavar:
#             s1 = self.copia() 
#             s2 = self
#         else:
#             if v in self.unit:
#                 s1.insertar(set())
#                 for x in self.unit:
#                     if not x == v and not x==-v:
#                         s2.insertars({x})
#                 for cl in self.listaclaus:
#                     s2.insertars(cl)
#             elif -v in self.unit:
#                 s2.insertar(set())
#                 for x in self.unit:
#                     if  not x == v and not x==-v:
#                         s1.insertars({x})

#                 for cl in self.listaclaus:
#                     s1.insertars(cl)
#             else:

#                 s1.unit = self.unit.copy()
#                 s2.unit = self.unit.copy()
#                 s1.listavar = set(map(lambda x: abs(x),s3.unit))
#                 s2.listavar = set(map(lambda x: abs(x),s3.unit))
#                 for cl in self.listaclaus:
#                     if v in cl:
#                         if n:
#                             cl1 = cl - {v}
#                             s1.insertars(cl1)
#                         else:
#                             cl.discard(v)
#                             s1.insertars(cl)
#                     elif -v in cl:
#                         if n:
#                             cl1 = cl - {-v}
#                             s2.insertars(cl1)
#                         else:
#                             cl.discard(-v)
#                             s2.insertars(cl)
#                     else: 
#                         if n:
#                             cl1 = cl.copy()
#                             s1.insertars(cl1)
#                             s2.insertars(cl1.copy())
#                         else:
#                             s1.insertars(cl.copy())
#                             s2.insertars(cl)
#         return (s1,s2)

        
#   def podaylimpia(self):
#         y = []
#         borr = []
#         # print("entro en poda 2", len(self.listaclaus))
#         self.listaclaus.sort(key = lambda x: len(x))
#         # print("ordenadas")
        
#         lista = self.listaclaus

#         for i in range(len(lista)):
#             clau1 = lista[i]
#             for j in range(i+1,len(lista)):

#                 clau2 = lista[j]
#                 if clau2 in borr:
#                     break
#                 claudif = (clau1-clau2)
#                 if (len(claudif) ==0):
#                     borr.append(clau2)
#                 elif (len(claudif) ==1):
# #                    print("poda", clau2)
#                     var = claudif.pop()
#                     if -var in clau2:
#                         clau2.dicard(-var)
#                         y.append(clau2)
        
#         for clau in borr:
#             self.eliminar(clau)
        
#         while y:
# #            print("original ibp",clau,len(self.listaclaus))
#             clau = y.pop()
#             y = self.podacola(clau)
# #            print("original ibp",clau,len(self.listaclaus))
    # def propagacion_unitaria(self):
    #     self.unitprev= set()
    #     for c in self.listaclaus:
    #         if (len(c))== 1:
    #             h = set(c).pop()
    #             self.unitprev.add(h)
    #             self.unit.add(h)
            
    #     self.unitprop()        
                
            
    # def unitprop(self):
    #     res = set()
    #     while self.unitprev:
    #         p = self.unitprev.pop()

    #         res.add(p)
            
    #         self.listavar.discard(abs(p))
    #         borrar = []

    #         for cl in self.listaclaus:
    #             if p in cl:
    #                 borrar.append(cl)
    #             elif -p in cl:
    #                 cl.discard(cl)
    #                 if len(cl) == 1:
    #                     nv = next(iter(cl))
    #                     self.unitprev.add(nv)
    #                 elif not cl:
    #                     self.contradict = True
    #                     break
   
                                    
    #     return res


    #  def podacola(self,x):
    #     y = []
    #     borr = []
    #     for cl in self.listaclaus:
    #         if not x == cl:
    #             if len(x) < len(cl):
    #                 claudif = x-cl
    #                 if not claudif:
    #                     borr.append(cl)
    #                 elif len(claudif) == 1:
    #                     var = claudif.pop()
    #                     if -var in cl:
    #                         cl.discard(-var)
    #                         y.append(cl)
    #             else:
    #                 claudif = cl-x
    #                 if not claudif:
    #                     return []
    #                 elif len(claudif) == 1:
    #                     var = claudif.pop()
    #                     if -var in x:
    #                         x.discard(-var)
    #                         for cl in borr:
    #                             self.eliminar(cl)
    #                         return self.podacola(x)
    #     for cl in borr:
    #         self.eliminar(cl)
    #     return y
    # def simplificaconfig(self,ref,config):
    #     borrar = []
    #     for cl1 in self.listaclaus:
    #         cl = config.union(cl1)
    #         for cl2 in ref.listaclaus:
    #             if len(cl2) <= len(cl):
    #                 claudif = cl2-cl
    #                 if not claudif:
    #                     borrar.append(cl1)
    #                     break
    #                 elif len(claudif)==1:
    #                     var = claudif.pop()
    #                     if -var in cl1:
    #                         cl1.discard(-var)
    #                         if not cl1:
    #                             self.insertar(set())
    #                             break
    #     for cl in borrar:
    #         self.eliminar(cl)