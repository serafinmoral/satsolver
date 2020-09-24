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
         self.equiv = set()
         self.unitprev = set()
         self.dobles = set()
         self.dep = dict()
         self.refer = dict()
         self.apren = {0}
         
     
    def tambor(self,v):
        n1 = len(self.indices.get(v,set()))
        n2 = len(self.indices.get(-v,set()))
        return n1*n2-n1-n2
        
    def Conjunto(self):
        result = []
        for c in self.listaclaus:
            result= result + [list(c)]
        return result
         
    def compruebasol(self,config):
        correcto = True
        for y in self.listaclaus:
            t = reduce(y,config)
            if len(t)== 0:
                print("solucion no valida ")
                print(config)
                print("clausula ",y)
                correcto = False
                break
        if correcto:
            print("Solucion Correcta")
       
        
    def compruebasol2(self,config):
        conf = set(config)
        correcto = True
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
    def calculadep(self):
    
        for cl in self.listaclaus:
            lon = len(cl)-1
            for x in cl:
                for y in cl:
                    if not x==y:
                        lo = min(abs(x),abs(y))
                        up = max(abs(x),abs(y))
                        if (lo,up) in self.dep:
                                self.dep[(lo,up)] += 1/2**lon
                        else:
                                self.dep[(lo,up)]= 1/2**lon
                        
    def calculagrafo(self):
            
        grafo = dict()
    
        for cl in self.listaclaus:
            
            for x in cl:
                for y in cl:
                   if not x==y:
                       if not abs(x) in grafo:
                           grafo[abs(x)] = [abs(y)]
                       else:
                           grafo[abs(x)].append(abs(y))
                       if not abs(y) in grafo:
                           grafo[abs(y)] = [abs(x)]
                       else:
                           grafo[abs(y)].append(abs(x))   
        return grafo
     

    def insertacondi(self,cl):
        self.insertaysatura(cl,2)

        if (len(cl))== 1:
                h = set(cl).pop()
                self.unitprev.add(h)
                self.unit.add(h)
        

                                   
            
    def propagacion_unitaria(self):
        self.unitprev= set()
        for c in self.listaclaus:
            if (len(c))== 1:
                h = set(c).pop()
                self.unitprev.add(h)
                self.unit.add(h)
            elif (len(c)==2):
                self.dobles.add(c)
                mclau = frozenset(map(lambda x: -x,c))
                if mclau in self.dobles:
                    par = set(c)
                    l1 = par.pop()
                    l2 = -par.pop()
                    if(abs(l1)<abs(l2)):
                        self.equiv.add((l1,l2))
                    else:
                        self.equiv.add((l2,l1))
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
#                    print("propagacion unitaria")
#                    print(c)
#                    print(p)
#                    print(self.refer.get(c,set()))
#                    print(self.refer.get(frozenset({p}),set()))

                    c2 = frozenset(set(c)-{-p})
                    re = self.refer.get(c,set()).union({-p})
#                    if not c2:
#                       print(re)
                    self.insertarref(c2,re,M=0)

                    if self.contradict:
                        return res
                    
                    
                    if (len(c2)==2):
                        self.dobles.add(c2)
                        mc = frozenset(map(lambda x: -x, c2))
                        if mc in self.dobles:
#                            print(c,mc,"nueva equivalencia")
                            par = set(c2)
                            t1 = par.pop()
                            t2 = -par.pop()
                            
                            if(abs(t1)<abs(t2)):
                                if(not  (-t1,-t2) in self.equiv):    
                                    self.equiv.add((t1,t2))
#                                    print("nueva equivalencia ", t1, t2)
#                                    time.sleep(3)
                            else:
                                if(not (-t2,-t1) in self.equiv):
                                    self.equiv.add((t2,t1)) 
                                    
        return res
                                    
    def unitprop2(self,probs):
        while self.unitprev:
            p = self.unitprev.pop()
            if abs(p) in probs:
                probs.pop(abs(p))
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
#                    self.refer[c2] = self.refer.get(c,set()).union(self.refer.get(frozenset({p}),set()))
                    if(not c2):
                        self.contradict = True
                        self.solved = True
#                            
#                            self.apren = self.refer[c2]
                        return
                    self.insertar(c2)
                    if (len(c2)==1):
                        h = set(c2).pop()
                        self.unitprev.add(h)
                        self.unit.add(h)
            self.listavar.discard(abs(p))
            
                     
                        
    def unitprop3(self):
        while self.unitprev:
            p = self.unitprev.pop()
            self.listavar.discard(abs(p))

            if p in self.indices:
                borrar = set()
                for c in self.indices[p]:
                    if len(c)>1:
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
#                    self.refer[c2] = self.refer.get(c,set()).union(self.refer.get(frozenset({p}),set()))
                    if(not c2):
                        self.contradict = True
                        self.solved = True
#                            
#                            self.apren = self.refer[c2]
                        return
                    self.insertar(c2)
                    if (len(c2)==1):
                        h = set(c2).pop()
                        self.unitprev.add(h)
                        self.unit.add(h)
            
            
                     
                                                               
                        
    def equivprop(self):
        equival = []
        refs = dict()
        while self.equiv:
            (l1,l2) = self.equiv.pop()
            equival.append((l1,l2))
            
#            print("equivalencia " ,l1 ,l2)
            eliminar = set()
            anadir = set()
#            print("quitamos ", l2)
            if l2 in self.indices:
                for c in self.indices[l2]:
                    eliminar.add(c)
                    if not -l1 in c: 
                        h =  frozenset(set(c)-{l2}).union({l1})
                        anadir.add(h)
                        ref2 = self.refer.get(c,set()).union(self.refer.get(frozenset({-l2,l1}),set()))
                        refs[h]= ref2
            if -l2 in self.indices:
                for c in self.indices[-l2]:
                    eliminar.add(c)
                    if not l1 in c: 
                        h =  frozenset(set(c)-{-l2}).union({-l1})
                        anadir.add(h)
                        ref2 = self.refer.get(c,set()).union(self.refer.get(frozenset({l2,-l1}),set()))
                        refs[h]= ref2
            for c in eliminar:
#                    print("borramos ",c)
                    self.eliminar(c)
            self.listavar.discard(abs(l2))

#                    if (len(c)==2):
#                        self.equiv.discard(c)
            for c in anadir:
#                    print("añadimos ", c)
              
                    if (len(c)==2):
                        self.dobles.add(c)
                        mc = frozenset(map(lambda x: -x, c))
                        if mc in self.dobles:
#                            print(c,mc,"nueva equivalencia")
                            par = set(c)
                            t1 = par.pop()
                            t2 = -par.pop()
                            
                            if(abs(t1)<abs(t2)):
                                if(not  (-t1,-t2) in self.equiv):    
                                    self.equiv.add((t1,t2))
#                                    print("nueva equivalencia ", t1, t2)
#                                    time.sleep(3)
                            else:
                                if(not (-t2,-t1) in self.equiv):
                                    self.equiv.add((t2,t1)) 
#                                    print("nueva equivalencia ", t2, t1)
#                                    time.sleep(3)
                    self.insertarref(c,refs[c])
                        

#            self.unitprop()
            
        
        return equival                        
        
         
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
    
    def nextVar(self,noborrad):
        y = noborrad[0]
        (conjunto,k) = self.computeComplV(y)
        best = len(conjunto)*len(self.listaclaus) + k 
        nbest = y
        for y in noborrad[1:]:
            (c2,k) = self.computeComplV(y)
            z = len(c2)*len(self.listaclaus) + k 
            if(z<best) :
                nbest=y
                best = z
                conjunto = c2
        return (nbest,conjunto)
        
    def actualizab(self,var,conjunto):
        conjunto = frozenset(conjunto -{var})
        if (len(conjunto)>0):
            self.insertar(conjunto) 
        if var in self.indices:
            while bool(self.indices[var]):
#                print(self.indices[var])
                c = self.indices[var].pop()
                self.eliminar(c)
            
            
    def computeOrder(self):
        
        ordenbo = []
        varinorder = dict()
        conjuntosvar = dict()
        conjuntos = self.calculaconjuntos()
        noborrad = list(self.listavar)
        current = 1
        while len(noborrad)>0:
            (var,conjunto) = conjuntos.nextVar(noborrad)
            noborrad.remove(var)
            ordenbo.append(var)
#            print(var)
            varinorder[var] = current-1
            conjuntosvar[var] = conjunto
#            print (current)
            current += 1
     
#            print (var)
#            print(conjunto)
            conjuntos.actualizab(var,conjunto)
        return(ordenbo,varinorder,conjuntosvar)
        
        
                  
    def computeOrder2(self):
        
       
        varinorder = dict()
        noborrad = list(self.listavar)
        
        scores = dict()
        
        for x in noborrad:
            scores[x] = 1.0
            scores[-x] = 1.0
        

        for cl in self.listaclaus:
            for x in cl:
                scores[-x] *= ((2**(len(cl)-1)-1)/2**(len(cl)-1))
                
#        print(scores)

                
        for x in noborrad:
            h = scores[x]/(scores[x]+scores[-x])
            scores[x] = max(h,1-h)
            
        
        ordenbo = sorted(noborrad,key = lambda x: scores[x])
        
        print(ordenbo)
        
        for i in range(len(ordenbo)):
            varinorder[ordenbo[i]] = i
        
        return(ordenbo,varinorder)
        
                  
    def computeOrder3(self):
        conjunto = self.copia()
        
        
        ordenbo = []
       
        varinorder = dict()
        noborrad = set(self.listavar)
        
        index = 0
        
        while noborrad:
            
            minv = min(noborrad , key=lambda x: (len(conjunto.indices.get(x,set()))-1)*    (len(conjunto.indices.get(-x,set()))-1))
#            print (minv)
            ordenbo.append(minv)
            varinorder[minv] = index
            index += 1
            conjunto.marginalizaAprox(minv,10)
            noborrad.discard(minv)
        
                
#        print(scores)

        
            
        
        return(ordenbo,varinorder)
        
        
    def marginalizaAprox(self,var,M=200):
        r1 = self.indices.get(var,set())
        r2 = self.indices.get(-var,set())
        
        
        lista =[]
        
        for clau1 in r1:
            for clau2 in r2:
                clau = resolution(var,clau1,clau2)
                if (0 not in clau):
                    lista.append(clau)
                    
        lista.sort(key=len)
        for i in range(min(M,len(lista))):
            clau = lista[i]
            self.insertayborra(clau)
        while r1:
            self.eliminar(r1.pop())
        while r2:
            self.eliminar(r2.pop())

     
    def computeCliques(self):
        
        ordenbo = []
        varinorder = dict()
        conjuntosvar = dict()
        conjuntos = self.calculaconjuntos()
        noborrad = list(self.listavar)
        current = 1
        while len(noborrad)>0:
            (var,conjunto) = conjuntos.nextVar(noborrad)
            noborrad.remove(var)
            ordenbo.append(var)
            varinorder[var] = current-1
            conjuntosvar[var] = conjunto
#            print (current)
            current += 1
     
#            print (var)
#            print(conjunto)
            conjuntos.actualizab(var,conjunto)
        return(ordenbo,varinorder,conjuntosvar)
        
        
    def extraePotentials(self,ordenbo):
            listpot = []
            for v in ordenbo:
                pot = self.extraeBorra(v)
                listpot.append(pot)
            return listpot
        
        
                
    def copia(self):
      nuevo = globalClausulas()
      nuevo.apren = self.apren
      nuevo.listavar = self.listavar.copy()
      
      for x in self.listaclaus:
          nuevo.insertar(x)
          if x in self.refer:
              nuevo.refer[x] = self.refer[x].copy()
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
    
    def calprob(self):
        x = 0.0
        for cl in self.listaclaus:
            x += (2**(len(cl))-1)/2**(len(cl))
        return x
    
    def cuenta(self,config):
        result = 0
        for cl in self.listaclaus:
            if config.intersection(cl):
                result += 1
        return result
    
    
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
        
    def cgrafo(self):
        grafo = nx.Graph()
        
        grafo.add_nodes_from(self.listavar)
        
        for cl in self.listaclaus:
           for u in cl:
                   for v in cl:
                       if not abs(u)==abs(v):
                           grafo.add_edge(abs(u),abs(v))                     
        return grafo
                         
        
    def restringeref(self,x):
    
        
        y = globalClausulas()
        for cl in self.listaclaus:
            if (x not in cl) and (-x not in cl):
                y.insertar(cl)
#                y.refer[cl] = self.refer.get(x,set())
               
                if (len(cl)==2):
                    y.dobles.add(cl)
                    mclau = frozenset(map(lambda x: -x,cl))
                    if mclau in y.dobles:
                        par = set(cl)
                        l1 = par.pop()
                        l2 = -par.pop()
                        if(abs(l1)<abs(l2)):
                            y.equiv.add((l1,l2))
                        else:
                            y.equiv.add((l2,l1))
                if (cl in self.refer):
                    y.refer[cl] = self.refer[cl]
            elif -x in cl:
                cl2 = frozenset(cl-{-x})
                r1 = set(self.refer.get(cl,set()))
                r1.add(-x)
                y.refer[cl2]=r1
                
                if (cl2):
                    y.insertar(cl2)
                    if (len(cl2))== 1:
                        h = set(cl2).pop()
                        y.unitprev.add(h)
                        y.unit.add(h)
                    elif (len(cl)==2):
                        y.dobles.add(cl2)
                        mclau = frozenset(map(lambda x: -x,cl))
                        if mclau in self.dobles:
                            par = set(cl2)
                            l1 = par.pop()
                            l2 = -par.pop()
                            if(abs(l1)<abs(l2)):
                                y.equiv.add((l1,l2))
                            else:
                                y.equiv.add((l2,l1))
                    
                else:
                    y.listaclaus.clear()
                    y.insertar(cl2)
                    y.contradict = True
                    y.solved = True
                    y.apren = y.refer[cl2]
                    print("Aprendo ·al restringir", y.apren)
                    break
                
        return y
        
        
                    
                
    def recomvar(self):
        elimin = set()
        for x in self.listavar:
            if not self.indices.get(x,set()) and not self.indices.get(-x,set()):
                elimin.add(x)
        self.listavar = self.listavar - elimin
         
    def calculascore(self,valores,var):
        score = 1.0
        for x in self.indices[var]:
            z = reduce(x,valores)
            if 0 not in z:
                score *= (2**(len(z)-1)-1)/2**(len(z)-1)
            if score==0.0:
                return [score,x]
        return [score]
    
    
            
        
                    
     
    def eliminaListas(self,lista1,lista2,noborrad):
        
        for y in lista1:
            for z in y:
                if (z in noborrad) or (-z in noborrad):
                        self.indices[z].remove(y)
                        

        for y in lista2:
            for z in y:
                if (z in noborrad) or (-z in noborrad):
                        self.indices[z].remove(y)     

    def busca(self):
        print("Comienza busqueda")
        valores = set()
        variables = []
        restantes = self.listavar.copy()
        n = len(restantes)
        current = 0
        while current< n and not self.solved:
            print(current)
#            print(current)
            bvar = -1
            best = 1.0
            pos = True
            forced = False
            incon = False
            for var in restantes:
                varneg = self.calculascore(valores,var)
                varpos = self.calculascore(valores,-var)
                if ((varpos[0]==0.0) and (varneg[0]==0.0)):
                    print(varpos[0],varneg[0])

                    clau1 = varpos[1]
                    clau2 = varneg[1]
#                   print(clau1.lista)
#                   print(clau2.lista)
#                   print(var)
                    claures = resolution(var,clau1,clau2)
                    if(len(claures)==0):
                        self.solved = True
                        self.contradict = True
                        self.solucion = False
                    
                    imax = 0
#                   print(claures.lista)
                    for y in claures:
                        z = abs(y)
                        posic = variables.index(z)
                        if (posic >imax):
                            imax = posic
#                            varmax = variables[imax]
#                    print(varmax)
                    self.insertar(claures)
                    
#                    print (clau1)
#                    print(clau2)
#                    print ("inserto clausula",claures)
#                    print ("Var",var)
#                    
#                    print (valores)
                
                    for j in range(imax,current):
                        valores.discard(variables[j])
                        valores.discard(-variables[j])
#                    print(imax,current)
#                    print(valores)
#                    print(restantes)
#                    print (variables[imax:current])
                    restantes.update(variables[imax:current])
#                   print(restantes)
                    del variables[imax:current]
#                    print(variables)
                    incon = True  
                    current = imax
                    break
                
                elif (varneg[0]==0 and  varpos[0]>0):
                    forced = True
                    pos = True
                    bvar = var
                
                elif (varpos[0]==0 and  varneg[0]>0):
                    forced = True
                    pos = False
                    bvar = var
                elif not forced:
                    
                    
                    if (varneg[0]>varpos[0]):
                        coef = varneg[0]/varpos[0]
                        if (coef>=best):
                            best = coef
                            pos = False
                            bvar = var
                    else:
                        coef = varpos[0]/varneg[0]
                        if (coef>=best):
                            best = coef
                            pos = True
                            bvar = var
            if not incon:
                if pos:
                    current += 1
                    valores.add(bvar)
                    variables.append(bvar)
                    restantes.discard(bvar)
                else:
                   current += 1
                   valores.add(-bvar)
                   variables.append(bvar)
                   restantes.discard(bvar) 
                
                            
        if not self.solved:
            self.solved = True
            self.solucion = True
            self.configura = valores
        
    def insertarc(self,x,M=2):
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
           self.insertaborraypoda2(x) 
           
           
           
    def insertarref(self,x,r,M=2):
        if self.contradict or (0 in x):
            return
#        print("inserto ",x)
        if not x:
            self.anula()
            self.listaclaus.add(x)
            self.solved=True
            self.contradict=True
            self.apren = r
            return
        if x in self.listaclaus:
            if len(r) < len(self.refer.get(x,set())):
                self.refer[x] = r
            return
        if len(x)==1:
            self.unitprev.add(set(x).pop())
            self.unit.add(set(x).pop())
        elif len(x)==2:
                        self.dobles.add(x)
                        mc = frozenset(map(lambda y: -y, x))
                        if mc in self.dobles:
#                            print(c,mc,"nueva equivalencia")
                            par = set(x)
                            t1 = par.pop()
                            t2 = -par.pop()
                            
                            if(abs(t1)<abs(t2)):
                                if(not  (-t1,-t2) in self.equiv):    
                                    self.equiv.add((t1,t2))
#                                    print("nueva equivalencia ", t1, t2)
#                                    time.sleep(3)
                            else:
                                if(not (-t2,-t1) in self.equiv):
                                    self.equiv.add((t2,t1))
            
        if len(x)>M:
            self.refer[x] = r
            for y in x:
                if y in self.indices:
                    self.indices[y].add(x)
                else:
                    self.indices[y] = {x}
                if(abs(y) not in self.listavar):
                    self.listavar.add(abs(y))
            self.listaclaus.add(x)
            
        else:
           self.insertaborraypoda2r(x,r,M) 
      
    def inserts(self,x):
        
            
        if x not in self.listaclaus:
            for y in x:
                if y in self.indices:
                    self.indices[y].add(x)
                else:
                    self.indices[y] = {x}
                if(abs(y) not in self.listavar):
                    self.listavar.add(abs(y))
            self.listaclaus.add(x)
       
        
         
    def insertar(self,x):
        if self.contradict:
            return
        if not x:
            self.anula()
            self.listaclaus.add(x)
            self.solved=True
            self.contradict=True
            if x in self.refer:
                self.apren = self.refer.get(x,set())
            
        if x not in self.listaclaus:
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
            self.unit.add(set(x).pop())
            
    def insertaycomprueba(self,x):
        if len(x)==0:
            self.anula()
            self.listaclaus.add(x)
            self.solved=True
            self.contradict=True
        if x not in self.listaclaus:
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
                self.insertar(x)

                
            
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
                    
                    
    def insertaborraypoda2(self,x):
        if self.contradict:
            return

        bor = []
        h = []
#        print("inserto x",x) 
        if x not in self.listaclaus:
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
                               h.append(ncl)
                               self.refer[ncl] = self.refer.get(cl,set()).union(self.refer.get(x,set()))
                               if not ncl:
                                   self.solved = True
                                   self.contradict = True
                                   self.apren = self.refer[ncl]
                                   return 
                               
                               
                               
               else:
                   if p in self.indices:
                       for cl in self.indices[p]:
                               bor.append(cl)
                   if -p in self.indices:
                       for cl in self.indices[-p]:
                               bor.append(cl)         
                               ncl = frozenset(cl - {-p})
                               h.append(ncl)
                               self.refer[ncl] = self.refer.get(cl,set()).union(self.refer.get(x,set()))
                               if not ncl:
                                   self.solved = True
                                   self.contradict = True
                                   self.apren = self.refer[ncl]
                                   return             
           for cl in bor:
#                if cl == test:
#                    print("aqui borro",x)
#                print("borro",cl,len(self.listaclaus))
                self.refer.pop(cl,-1)
                self.eliminar(cl)
                
           self.insertar(x)

            
           for cl in h:
                
#                print("ibp2",cl)
                if cl not in self.listaclaus:
                    self.insertarc(cl,2)
                    
                    
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
#                if clr < cl:
#                    borrar.append(cl)
#                    break
#                if clr < cl2:
#                    borrar.append(cl2)
#        for cl2 in borrar:
#            self.eliminar(cl2)
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
            
      

    def insertaborraypoda2r(self,x,r,M=2):
        if self.contradict:
            return

        bor = []
        h = []
        refs = dict()
#        print("inserto x",x) 
        if x not in self.listaclaus:
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
                               h.append(ncl)
                               refs[ncl] = self.refer.get(cl,set()).union(r)
                               if not ncl:
                                   self.solved = True
                                   self.contradict = True
                                   self.apren = self.refer.get(cl,set()).union(r)
                                   return 
                               
                               
                               
               else:
                   if p in self.indices:
                       for cl in self.indices[p]:
                               bor.append(cl)
                   if -p in self.indices:
                       for cl in self.indices[-p]:
                               bor.append(cl)         
                               ncl = frozenset(cl - {-p})
                               h.append(ncl)
                               refs[ncl] = self.refer.get(cl,set()).union(r)
                               if not ncl:
                                   self.solved = True
                                   self.contradict = True
                                   self.apren = self.refer.get(cl,set()).union(r)
                                   return             
           for cl in bor:
#                if cl == test:
#                    print("aqui borro",x)
#                print("borro",cl,len(self.listaclaus))
                self.refer.pop(cl,-1)
                self.eliminar(cl)
                
           self.insertarref(x,r,M=0)

            
           for cl in h:
                
#                print("ibp2",cl)
                if cl not in self.listaclaus:
                    self.insertarref(cl,refs[cl])
  

    def insertaborraypoda2sr(self,x):

        bor = []
        h = []
#        print("inserto x",x) 
        if x not in self.listaclaus:
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
                               h.append(ncl)
                               if not ncl:
                                   self.solved = True
                                   self.contradict = True
                                   return 
                               
                               
                               
               else:
                   if p in self.indices:
                       for cl in self.indices[p]:
                               bor.append(cl)
                   if -p in self.indices:
                       for cl in self.indices[-p]:
                               bor.append(cl)         
                               ncl = frozenset(cl - {-p})
                               h.append(ncl)
                               if not ncl:
                                   self.solved = True
                                   self.contradict = True
                                   return              
           for cl in bor:
#                if cl == test:
#                    print("aqui borro",x)
#                print("borro",cl,len(self.listaclaus))
                self.refer.pop(cl,-1)
                self.eliminar(cl)
                
           self.insertar(x)

            
           for cl in h:
                
#                print("ibp2",cl)
                if cl not in self.listaclaus:
                    self.insertaborraypoda2(cl)
            
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
                

 
                
    def calculaconjunto(self,y):
        valor = set()
        for x in self.indices[y]:
            for z in x.lista:
                valor.add(abs(z))
        for x in self.indices[-y]:
            for z in x.lista:
                valor.add(abs(z))
        return valor
    
    
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


    def computevar(self):
        variables = list(self.listavar)
        valores = []
        for x in variables:
            r1 = self.indices.get(x,[])
            r2 = self.indices.get(-x,[])
            valores.append( len(r1)*len(r2) + len(r1) + len(r2))
#        print (valores)
        nvar = valores.index(max(valores))
        var = variables[nvar]
        return var
                 
    
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
            
    def borraAprox(self,var,listapos,listaneg,th,M=3000):
        
        y = globalClausulas()
        
        r1 = self.limpiacasi(th,listapos)
        r2 = self.limpiacasi(th,listaneg)
        
        
        while len(r1)*len(r2)>M:
            cl1 = r1[-1]
            cl2 = r2[-1]
            if (cl1.lista>cl2.lista):
                r1.pop()
            else:
                r2.pop()
            
       
        
        for clau1 in r1:
            for clau2 in r2:
                clau = clau1.resolution(var,clau2)
                if (len(clau.lista)==0):
                    y.insertar(clau)
                    return y
                if (0 not in clau.lista):
                    y.insertar(clau)
        return y
        
    def marginaliza(self,var):
        
        y = globalClausulas()
        
        
        
        r1 = self.indices.get(var,set())
        r2 = self.indices.get(-var,set())
        
        for cl in self.listaclaus:
            if (not var in cl) and (not -var in cl):
                y.insertar(cl)
        
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    y.insertar(clau)
                    y.contradict=True
                    y.solved=True
                    return y
            if (0 not in clau):
                    y.insertar(clau)
        return y
        
    def marginalizain(self,var,M=3, L =50):
        
        lista = []
        r1 = list(self.indices.get(var,set()))
        r2 = list(self.indices.get(-var,set()))
        
        for x in r1:
                self.eliminar(x)
                
        for x in r2:
                self.eliminar(x)
        
        
        if (len(r1)*len(r2)>L*L):
            
            if (len(r1)>L) and (len(r2)>L):
                r1.sort(key= lambda x: len(x))
                
                r2.sort(key= lambda x: len(x))
        
                r1 = r1[:L]
                r2 = r2[:L]
        
            elif len(r1)>L :
                r1.sort(key= lambda x: len(x))
                
                
                r1 = r1[:int( L*L/len(r2))] 
                
            else:
                
                r2.sort(key= lambda x: len(x))
                
                
                r2 = r2[:int( L*L/len(r1))] 
        
        
        self.listavar.discard(var)
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            if(0 not in clau):
                re = self.refer.get(x[0],set()).union(self.refer.get(x[1],set()))
                self.insertarref(clau,re,M=0)
                if self.contradict:
                    return lista
            
                if len(clau)<= M:
                    lista.append(clau)
            
            
                    

                
        return lista
    
    
    def marginalizain2(self,var,N=4):
        
        lista = []
        borra = []
        r1 = list(self.indices.get(var,set()))
        r2 = list(self.indices.get(-var,set()))
        
        for x in r1:
                self.eliminar(x)
                
        for x in r2:
                self.eliminar(x)
        
        
        
        
        
        self.listavar.discard(var)
        
        for x in  list(itertools.product(r1,r2)):
          if (len(x[0])<=N) and (len(x[1])<=N):
                
            clau = resolution(var,x[0],x[1])
            if(0 not in clau):
                re = self.refer.get(x[0],set()).union(self.refer.get(x[1],set()))
                self.insertarref(clau,re,M=3)
                if self.contradict:
                    return (lista,borra)
            
                
                lista.append(clau)
          elif (x[0]-{var}) <= x[1]-{-var}:
             clau = resolution(var,x[0],x[1])
             if(0 not in clau):
                re = self.refer.get(x[0],set()).union(self.refer.get(x[1],set()))
                self.insertarref(clau,re,M=3)
                if self.contradict:
                    return (lista,borra)
            
                borra.append(x[1])
                lista.append(clau) 
        
          elif (x[1]-{-var}) <= x[0]-{var}:
             clau = resolution(var,x[0],x[1])
             if(0 not in clau):
                re = self.refer.get(x[0],set()).union(self.refer.get(x[1],set()))
                self.insertarref(clau,re,M=0)
                if self.contradict:
                    return (lista,borra)
            
                borra.append(x[0])
                lista.append(clau)   
            
                    

                
        return (lista,borra)
    
    def marginalizaprox(self,var,L=30):
        
        lista = globalClausulas()
        r1 = list(self.indices.get(var,set()))
        r2 = list(self.indices.get(-var,set()))
        
        for cl in self.listaclaus:
            if not var in cl and not -var in cl:
                lista.insertar(cl)
        
        
        if (len(r1)*len(r2)>L*L):
            
            if (len(r1)>L) and (len(r2)>L):
                r1.sort(key= lambda x: len(x))
                
                r2.sort(key= lambda x: len(x))
        
                r1 = r1[:L]
                r2 = r2[:L]
        
            elif len(r1)>L :
                r1.sort(key= lambda x: len(x))
                
                
                r1 = r1[:int( L*L/len(r2))] 
                
            else:
                
                r2.sort(key= lambda x: len(x))
                
                
                r2 = r2[:int( L*L/len(r1))] 
        
        
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    lista.insertar(clau)
                    lista.contradict=True
                    lista.solved=True
                    return lista
            if (0 not in clau):
                    lista.insertar(clau)
                    

                
        return(lista)
    
    
    def marginalizalen(self,var,i=2):
        
        y = globalClausulas()
        
        
        
     
        
        for cl in self.listaclaus:
            if (not var in cl) and (not -var in cl):
                y.insertar(cl)
        
        
        for cl1 in self.indices.get(var,set()):
            if len(cl1)<= i:
                for cl2 in self.indices.get(-var,set()):
                    if len(cl2)<= i:
                        clau = resolution(var,cl1,cl2)
                        if (0 not in clau):
                            y.insertar(clau)
                
                        if (len(clau)==0):
                            y.contradict=True
                            y.solved=True
                            return y
                        elif (len(clau)==1):
                            nu = set(clau).pop()
                            y.unit.add(nu)
                            y.unitprev.add(nu)
                            y.unitprop()
                    
                    
                    
        return y
    
    
    def borraexactolim2(self,listas,M=40):
        variables = set(map(abs,self.indices))
        
        borrar = []
        for v in variables:
            n1 = len(self.indices.get(v,set()))
            n2 = len(self.indices.get(-v,set()))
            if n1==0 and n2==0:
                borrar.append(v)
                
        for v in borrar:
            variables.discard(v)
                
            
        final = []
        pos = True
        while pos and variables:
            vmin = min(variables,key = self.tambor)
            n1 = len(self.indices.get(vmin,set()))
            n2 = len(self.indices.get(-vmin,set())) 
            if  ((n1*n2-n1-n2<=M) or (n1==1) or (n2==1)) and (n1>0 or n2>0):
                listas[vmin] = self.indices.get(vmin,set()).copy()
                listas[-vmin] = self.indices.get(-vmin,set()) .copy()
                for cl in listas[vmin]:
                    self.eliminar(cl)
                for cl in listas[-vmin]:
                    self.eliminar(cl)
                if vmin in self.indices:
                    self.indices.pop(vmin)
                if -vmin in self.indices:
                    self.indices.pop(-vmin)
                self.listavar.discard(vmin)
                variables.discard(vmin)
                
                
                for x in  list(itertools.product(listas[vmin],listas[-vmin])):
                    clau = resolution(vmin,x[0],x[1])
                    if (0 not in clau):
                        self.insertar(clau)
#                        self.refer[clau] = self.refer.get(x[0],set()).union(self.refer.get(x[1],set()))
                        
                        if not clau:
                            self.contradict=True
                            return [vmin]
            
        
                final = [vmin] + final
            else:
                pos = False
        
        return final
                            
                        
                
                
        
    
    
    
    
    def borraexactolim(self,listas,M=20):
        if self.contradict:
            return[]
        variables = set(map(abs,self.indices))
        
        for v in variables:
            l1 = self.indices.get(v,set()) 
            l2 = self.indices.get(-v,set())
            n1 = len(l1)
            n2 = len(l2)
            if ((n1*n2<=M) or (n1==1) or (n2==1)) and (n1>0 or n2>0):
                listas[v] = l1.copy()
                listas[-v] = l2.copy()
                for cl in listas[v]:
                    self.eliminar(cl)
                for cl in listas[-v]:
                    self.eliminar(cl)
                if (n1>0):
                    self.indices.pop(v)
                if (n2>0):
                    self.indices.pop(-v)
                self.listavar.discard(v)
                
                
                
                for x in  list(itertools.product(listas[v],listas[-v])):
                    clau = resolution(v,x[0],x[1])
                    re = self.refer.get(x[0],set()).union(self.refer.get(x[1],set()))
                    self.insertarref(clau,re)
                    if self.contradict:
                        return []
                   
                        
                        
                return [v] + self.borraexactolim(listas,M)   
        return []
                            
                        
                
                
    
    
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
                
            
            
        
    
    def marginalizaapr2(self,var,bloquedas,unitarias,M=3):
        
        y = globalClausulas()
        z = globalClausulas()
        
        anadir = []
        
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            
        
        
           
 
    
        
        
        
        
       

        r1 = self.indices.get(var,set())
        r2 = self.indices.get(-var,set())            
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    y.insertar(clau)
                    y.contradict=True
                    y.solved=True
                    return 
            if (0 not in clau):
                if (len(clau)==1):
                    print("unitaria ", clau)
                    p = set(clau).pop()
                    unitarias.add(p)
                elif (len(clau)<=M):
                    y.insertar(clau)
        return y
    
    
    
    
    def marginalizaapr(self,var,th,bloquedas,unitarias,otras,M=2):
        
        y = globalClausulas()
        z = globalClausulas()
        
        
 
        
        
        
        
        for cl in self.listaclaus:
            if (not var in cl) and (not -var in cl):
                y.insertar(cl)
            else:
                if (not z in bloquedas):
                    z.insertar(cl)

        z.limpiarec(th)

        r1 = z.indices.get(var,set())
        r2 = z.indices.get(-var,set())            
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    y.insertar(clau)
                    y.contradict=True
                    y.solved=True
                    return 
            if (0 not in clau):
                if (len(clau)==1):
                    print("unitaria ", clau)
                    p = set(clau).pop()
                    unitarias.add(p)
                elif (len(clau)<=M):
                    otras.insertar(clau)
                y.insertar(clau)
                
        y.limpiarec(0.0)
        return y
    
    def borraExactoCasi(self,var,listapos,listaneg,th):
        
        y = globalClausulas()
        
        
        
        r1 = self.limpiacasi(th,listapos)
        r2 = self.limpiacasi(th,listaneg)
        
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    y.insertar(clau)
                    return y
            if (0 not in clau):
                    y.insertar(clau)
        return y
        
   
    
    
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
        
        t = h.indices.get(var,set())
        
        if len(t)== 0:
            return True
        else:
            return False
            
        
        
        
        
        
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
#        print("entro en poda")
        
        lista = self.listavar.copy()
        
        for var in lista:
            self.podavar2(var)
#        print("salgo de poda")
    
        
    def podaylimpia(self):
        y = []
        borr = []
#        print("entro en poda 2")
        lista = sorted(self.listaclaus,key = lambda x: len(x))
#        print("ordenadas")
        
        for i in range(len(lista)):
            clau1 = lista[i]
            for j in range(i+1,len(lista)):

                clau2 = lista[j]
                claudif = set(clau1-clau2)
                if (len(claudif) ==0):
                    borr.append(clau2)
                elif (len(claudif) ==1):
                    var = claudif.pop()
                    if -var in clau2:
                        y.append(frozenset(clau2-{var}))
                        borr.append(clau2)
                        
        for clau in borr:
            self.eliminar(clau)
        
        for clau in y:
#            print("original ibp",clau,len(self.listaclaus))
            self.insertaborraypoda(clau)
#            print("original ibp",clau,len(self.listaclaus))

#                
#        print("salgo de poda 2")

    
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
        
    
    def satura(self,M=3,N=50000):
        z = set()
        for var in self.listavar:
            y = self.saturaVar(var,M)
            z.update(y)
        added =0
        while added<N and len(z)>0:
            clau = z.pop()
            self.insertayborra(clau)
            added += 1
            y = self.calculaNuevas(clau,M)
            z.update(y)
            print("total clau", len(self.listaclaus), added)
            print("cola ", len(z))
#        while len(z)>0:
#            clau = z.pop()
#            self.insertayborra(clau)
        print("total clau", len(self.listaclaus))
        
        
    def satura2(self,M=3,T=2,N=5000000):
        nue = self.copia()
        z = set()
        
        for var in self.listavar:
            y = self.saturaVar(var,M)
            z.update(y)
            if len(z)>N:
                break
        total = len(z)
        
        while len(z)>0:
            clau = z.pop()
            nue.insertar(clau)
            if len(clau)<=T:
                self.insertayborra(clau)
                print("Nueva clausula" ,clau)
            if total < N:
                y = nue.calculaNuevas(clau,M)
                total += len(y)
                z.update(y)
            
#        while len(z)>0:
#            clau = z.pop()
#            self.insertayborra(clau)
        print("total clau", len(self.listaclaus))
            
    def calculaNuevas(self,clau1,M=10):
        y = set()
        for var in clau1:
            for clau2 in self.indices[-var]:
                if (len(clau2)<=M+1):
                    clau = resolution(abs(var),clau1,clau2)
                    if 0 not in clau:
                        y.add(clau)
                    if (len(clau)==0):
                        self.solved=True
                        self.contradict=True
                        return y
                    
        return y
    
    def saturaVar(self,var,M=10):
        
        listapos = self.indices[var]
        listaneg = self.indices[-var]
        
        y = set()
        
        for clau1 in listapos:
            for clau2 in listaneg:
                if ((len(clau1)<=(M+1)) and len(clau2)<=(M+1)):
                    clau = resolution(var,clau1,clau2)
                    if (len(clau)==0):
                        y.insertar(clau)
                        self.solved=True
                        self.contradict=True
                        return
                    if (0 not in clau and len(clau)<=M):
                        y.add(clau)
        return y
    
    def insertaysatura(self,clau,M=2):
        if self.contradict:
            return 
        if (len(clau)<=M):
            self.insertayborra(clau)
        else:
            self.insertar(clau)
        
        if (len(clau)<=M):
            lista = self.entorno(clau)
        
            for x in lista:
                for v in clau:
                    if -v in x:
                        res = resolution(v,x,clau)
                        if not res:
                            self.contradict=True
                            self.solved = True
                            return
                        if len(res)<=M and (0 not in res) and (res not in self.listaclaus):
                            self.insertaysatura(res)
        
        
        
        
    
    
    def seleccionaVar(self,x):
        self.listavar.update(x)
       
        
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
                
                
    def limpiacasi(self,th,conjunto):
        
        nuevas = list(conjunto)
        nuevas.sort(key=lambda x: len(x))
        i1 = 0
        i2 = 1
        
       
        while (i1<(len(nuevas)-1)  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if casicontenida(cl1,cl2,th):
                if (cl1<=cl2):
                    conjunto.discard(cl2)
                del nuevas[i2]
                
            i2=i2-1
            if (i2 ==i1):
                i1=i1+1
                i2 = len(nuevas)-1 
         
           
        return nuevas
    
    
    def limpiatama(self,M=150):
        bor=[]
        x = self.listaclaus
        for y in x:
            if len(y)>M:
                bor.append(y)
        for y in bor:
            self.eliminar(y)
#            print("elimino ",len(y.lista))
            
    def limpianum(self,M=1000):
        bor=[]
        x = list(self.listaclaus)
        x.sort(key=lambda z: len(z))
        for y in x[M:]:
            self.eliminar(y)
#            print("elimino ",len(y.lista))
        
    def limpiarec(self,th,M=200):
         
        
        if len(self.listaclaus)<M :
            self.limpia(th)
            return
        
        
        
        valores = dict()
        
        for x in self.listavar:
            if (x in self.indices):
                l1 = len(self.indices[x])
            else:
                l1 = 0
            if (-x in self.indices):
                l2 = len(self.indices[-x])
            else:
                l2 = 0
            
            valores[x] = l1 * l2 -  l1 - l2 + len(self.listaclaus)
           
        
        
        
        var = max(valores.keys(), key=(lambda k: valores[k]))

        listano = globalClausulas()
        listap = globalClausulas()
        listanop = globalClausulas()
        
        if var in self.indices:
            conj1 = self.indices[var]
        else:
            conj1 = set()
        
        if -var in self.indices:
            conj2 = self.indices[-var]
        else:
            conj2 = set()
            
            
        listap.anadirConjunto(conj1)
        listanop.anadirConjunto(conj2)
        listano.anadirConjunto(self.listaclaus- conj1 - conj2 )
        
        if( len(listano.listaclaus) < 0.8 * len(self.listaclaus)):
                listano.limpiarec(th,M)
        else:
                listano.limpia(th)
        if(len(listap.listaclaus) < 0.8 * len(self.listaclaus)):    
                listap.limpiarecdos(listano,th,M)
        else:
                listap.limpia(th)
                listap.limpiacruz(listano,th)
                
        if(len(listanop.listaclaus) < 0.8 * len(self.listaclaus)):    
                listanop.limpiarecdos(listano,th,M)
        else:
                listanop.limpia(th)
                listanop.limpiacruz(listano,th)   
                
        self.anula()
        self.combina(listano)
        self.combina(listap)
        self.combina(listanop)
        
           
 
            
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
                           
    
            
           
    def limpiarecdos(self,aux,th,M):
       
        
        if len(self.listaclaus)<M :
            self.limpia(th)
            self.limpiacruz(aux,th)
            return
        
        valores = dict()
        for x in self.listavar:
            if (x in self.indices):
                l1 = len(self.indices[x])
            else:
                l1 = 0
            if (-x in self.indices):
                l2 = len(self.indices[-x])
            else:
                l2 = 0
            
            valores[x] = l1 * l2 -  l1 - l2 + len(self.listaclaus)
        
        
        
        var = max(valores.keys(), key=(lambda k: valores[k]))

        listano = globalClausulas()
        listap = globalClausulas()
        listanop = globalClausulas()
        
        if var in self.indices:
            conj1 = self.indices[var]
        else:
            conj1 = set()
        
        if -var in self.indices:
            conj2 = self.indices[-var]
        else:
            conj2 = set()
            
            
        listap.anadirConjunto(conj1)
        listanop.anadirConjunto(conj2)
        listano.anadirConjunto(self.listaclaus- conj1 - conj2 )
        
        
        auxno = globalClausulas()
        auxp = globalClausulas()
        auxnop = globalClausulas()
        
        if var in aux.indices:
            conj1 = aux.indices[var]
        else:
            conj1 = set()
        
        if -var in aux.indices:
            conj2 = aux.indices[-var]
        else:
            conj2 = set()
        
        
        auxp.anadirConjunto(conj1)
        auxnop.anadirConjunto(conj1)
        auxno.anadirConjunto(auxno.listavar- conj1 - conj2 )
        
        auxp.combina(auxno)
        auxp.combina(listano)
                    
        auxnop.combina(auxno)
        auxnop.combina(listano)
        
        if( len(listano.listaclaus) < 0.8 * len(self.listaclaus)):
                listano.limpiarecdos(auxno,th,M)
        else:
                listano.limpia(th)
                listano.limpiacruz(auxno,th)
        if(len(listap.listaclaus) < 0.8 * len(self.listaclaus)):    
                listap.limpiarecdos(auxp,th,M)
        else:
                listap.limpia(th)
                listap.limpiacruz(auxp,th)
                
        if(len(listanop.listaclaus) < 0.8 * len(self.listaclaus)):    
                listanop.limpiarecdos(auxnop,th,M)
        else:
                listanop.limpia(th)
                listanop.limpiacruz(auxnop,th)   
                
        self.anula()
        self.combina(listano)
        self.combina(listap)
        self.combina(listanop)
        
        # print(len(clausulas))
       
                    
            
     
    def limpiacruz(self,aux,th):
        
        borra = []
        for x in self.listaclaus:
            for y in aux.listaclaus:
                if casicontenida(y,x,th):
                    borra.append(x)
                    break
        
        self.eliminalista(borra)  
        

    
#print(SeleccionarArchivo("ArchivosSAT.txt"))


# info.satura(4)
#print("fin de satura")
# info.busca()
# info = leeArchivoSet('SAT_V153C408.cnf')



#info = leeArchivoSet('SAT_V144C560.cnf')

