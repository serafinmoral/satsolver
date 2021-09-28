# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 12:22:12 2021

@author: efraín
"""
import networkx as nx

class simpleClausulas:
    def __init__(self):
         self.listaclaus = []
         self.contradict = False
         self.listavar = set()    
         self.solved = False
         # self.solution = set()
         self.unit = set()


    def imprime(self):
        print("v",self.listavar)
        print("u",self.unit)
        print("c",self.listaclaus)  

    def insertars(self,x):

        nvar = set(map(abs,x))
        self.listavar.update(nvar)
        if len(x)==1:
            self.unit.add(x.pop())
        else:
            self.listaclaus.append(x)

    def eliminars(self,x):
        
        try:
            self.listaclaus.remove(x)
        except:
            ValueError

    def insertar(self,x):
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
            else:
                self.listavar.add(abs(v))
                self.unit.add(v)
                for cl in self.listaclaus:
                    if v in cl:
                        borr.append(cl)
                    if -v in cl:
                        borr.append(cl)
                        cl.discard(-v)
                        y.append(cl)
        else:

            if x.intersection(self.unit):
                return []
            else:
                neg = set(map(lambda x: -x, self.unit))
                x = x-neg
                if len(x) <= 1:
                    self.insertar(x)
                    return 

            for cl in self.listaclaus:
                if len(x) < len(cl):
                    claudif = x-cl
                    if not claudif:
                        borr.append(cl)
                    elif len(claudif) == 1:
                        var = claudif.pop()
                        if -var in cl:
                            cl.discard(-var)
                            borr.append(cl)
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
            nvar = set(map(abs,x))
            self.listavar.update(nvar)
            self.listaclaus.append(x)
        for cl in borr:
            self.eliminars(cl)
        
        for cl in y:
            self.insertar(cl)
        # print("Lista Cláusulas: ",self.listaclaus)
        # print("Variables: ",self.listavar)
        # print("Unitarias: ",self.unit)
        # time.sleep(3)

    def eliminar(self,x):
        if len(x)==1:
            v = x.pop()
            self.unit.discard(v)
            return
        try:
            self.listaclaus.remove(x)
        except:
            ValueError

    def anula(self):
        self.listaclaus.clear()
        self.listavar.clear()
        self.unit.clear()

    def cgrafo(self):
        grafo = nx.Graph()
        grafo.add_nodes_from(self.listavar)
        # print("grafos:", grafo)
        for cl in self.listaclaus:
           for u in cl:
                   for v in cl:
                       if not abs(u)==abs(v):
                           grafo.add_edge(abs(u),abs(v))                     
        return grafo

    def copia(self):
      nuevo = simpleClausulas()
      nuevo.listavar = self.listavar.copy()
      nuevo.unit = self.unit.copy()
      nuevo.contradict = self.contradict
      for x in self.listaclaus:
          nuevo.insertar(x.copy())
          
      return nuevo

    def simplificaunits(self,s):
        neg = set(map (lambda x: -x,s))

        if self.unit.intersection(s) in self.unit:
            self.insertar(set())
        else:
            y = []
            borr = []
            for cl in self.listaclaus:
    
                if cl.intersection(neg):
                    borr.append(cl)
                    cl.difference_update(neg)
                    y.append(cl)
            for cl in borr:
                self.eliminars(cl)
            for cl in y:
                self.insertar(cl)

    def splitborra(self,v,n=True):
        s1 = simpleClausulas()
        s2 = simpleClausulas()
        s3 = simpleClausulas()
        if not v in self.listavar:
            for cl in self.listaclaus:
                s3.insertars(cl)
            s3.unit = self.unit.copy()
        else:
            if v in self.unit:
                s1.insertar(set())
                for x in self.unit:
                    if not x == v and not x==-v:
                        s3.unit.add(x)
                for cl in self.listaclaus:
                    s3.insertars(cl)
            elif -v in self.unit:
                s2.insertar(set())
                for x in self.unit:
                    if  not x == v and not x==-v:
                        s3.unit.add(x)
                for cl in self.listaclaus:
                    s3.insertars(cl)
            else:

                s3.unit = self.unit.copy()

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

    def combinaborra(self,conj):
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
            for cl in conj.listaclaus:
                if -v not in cl:
                    r = cl.union({v})
                    res.insertar(r)
        for x in conj.unit:
            for cl in self.listaclaus:
                if -x not in cl:
                    r = cl.union({x})
                    res.insertar(r)
        for cl in self.listaclaus:
            for cl2 in conj.listaclaus:
                cpn = set(map(lambda x: -x, cl))
                if not cpn.intersection(cl2):
                    r = cl.union(cl2)
                    res.insertar(r)
        return res

    def combinaborrac(self,conj,conf):
        res = simpleClausulas()
        if self.contradict:
            h = conj.copia()
            h.adconfig(conf)
            return h
        if conj.contradict:
            h = self.copiac(conf) 
            return h
        confn = set(map(lambda x: -x, conf))
        for v in self.unit:
            if -v not in conf:
                for x in conj.unit:
                    if not v == -x:
                        cl = conf.union({v,x})
                        res.insertar(cl)
                for cl in conj.listaclaus:
                    if -v not in cl:
                        r = cl.union({v}).union(conf)
                        res.insertar(r)
        for x in conj.unit:
            for cl in self.listaclaus:
                if not confn.intersection(cl):
                    if -x not in cl:
                        r = cl.union({x}).union(conf)
                        res.insertar(r)
        for cl in self.listaclaus:
            if not confn.intersection(cl):
                cpn = set(map(lambda x: -x, cl))
                for cl2 in conj.listaclaus:
                    if not cpn.intersection(cl2):
                        r = cl.union(cl2).union(conf)
                        res.insertar(r)
        return res

    def combina(self,simple):
        neg = set(map(lambda x: -x, simple.unit))
        if neg.intersection(self.unit):
            self.insertar(set())
        else:
            for v in simple.unit:
                self.simplificaunit(v)
            self.unit.update(simple.unit)
        
            for cl in simple.listaclaus:
                self.insertar(cl)

    def adconfig(self,conf):
        
        if conf:
            for x in conf:
                self.listavar.add(abs(x))
            for cl in self.listaclaus:
                cl.update(conf)
            for x in self.unit:
                cl = conf.union({x})
                self.listaclaus.append(cl)
            self.unit = set()

    def advalue(self,v):
        self.listavar.add(v)
        for cl in self.listaclaus:
            cl.add(v)
        for x in self.unit:
            cl = {x,v}
            self.listaclaus.append(cl)
        self.unit = set()

    def nulo(self):
        if self.unit or self.listaclaus:
            return False
        else:
            return True

    def sel(self,v):
        result = simpleClausulas()
        if v in self.unit:
            result.insertar(set())
            return result
        result.unit = self.unit.copy()
        result.unit.discard(-v)
        for cl in self.listaclaus:
            if v in  cl:
                result.insertar(cl-{v})
            elif not -v in cl:
                result.insertar(cl)
        return result

    def simplificaunit(self,v):
        if -v in self.unit:
            self.insertar(set())
        else:
            y = []
            borr = []
            for cl in self.listaclaus:
                if -v in cl:
                    borr.append(cl)
                    cl.discard(-v)
                    y.append(cl)
            for cl in borr:
                self.eliminars(cl)
            for cl in y:
                self.insertar(cl)

    def copiac(self,conf):
      confn= set(map(lambda x: -x ,conf))
      varn = set(map(lambda x: abs(x) ,conf))
      nuevo = simpleClausulas()
      nuevo.listavar = self.listavar.union(varn)
      for x in self.unit:
          if -x not in conf:
              cl = conf.union({x})
              nuevo.insertar(cl)
      
      
      for x in self.listaclaus:
        if not confn.intersection(x):
            cl = conf.union(x)
            nuevo.listaclaus.append(cl)
          
      return nuevo
