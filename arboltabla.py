"""
Spyder Editor

This is a temporary script file.
"""
import networkx as nx    

import os
import math
from pickle import FALSE
from tablaClausulas  import *
from time import * 


def triangulacond(pot):
    orden = []
    clusters = []
    
    borr = []
   

    grafo = pot.cgrafo()

    ma = 0
    mv = 0
    n = len(grafo.nodes)
    

    i= 0
    total = set()
    cnodo = max(grafo.nodes,key = lambda x : grafo.degree[x])

    while grafo.nodes:

        nnodo = min(grafo.nodes,key = lambda x : grafo.degree[x])
        # print(nnodo)
        orden.append(nnodo)
        veci = set(grafo[nnodo])
        clus = veci.union({nnodo})
        clusters.append(clus)


        # print( i, clus) 
        i += 1
        grafo.remove_node(nnodo)
        for x in veci:
            for y in veci:
                if not x==y:
                    grafo.add_edge(x,y)

    
    clusters.append(set())

    h = list(map(len,clusters))
    mh = max(h)
    sh = sum(h)
    print("maximo: ", mh, "suma: ", sh)
    
    



    
    
    
    return (orden,cnodo,mh)
    

def calculadesdePotencial(pot,posvar, L=30):

        result = arbol()
        vars = set()
        for p in pot.listap:
            vars.update(p.listavar)
        
        if len(vars)<=L:
            result.asignaval(pot)
            return result
        else:
            result.value.unit = pot.unit.copy()
            pot.unit = set()
            
            var = max(vars, key = lambda x: posvar[x])
        
            p0 = pot.reduce([var], inplace = False)
            p1 = pot.reduce([-var], inplace = False)
            p0.simplifica()
            p1.simplifica()

            if p0.contradict and p1.contradict:
                result.anula()
                return result

            if p0.trivial() and p1.trivial():
                return result


            h0 = calculadesdePotencial(p0,posvar,L)
            h1 = calculadesdePotencial(p1,posvar,L)

            if h0.value.contradict and h1.value.contradict:
                result.anula()
                return result

            if h0.trivial() and h1.trivial():
                return result
            
            result.asignavarhijos(var,h0,h1)

            

        return result

def calculaglobal(pot, conf = [], L=30, M=5):

        result = arbol()
        vars = pot.getvars()
        if len(vars)<= L:
            result.value = pot
            return result
        print(conf) 
        (orden,cnodo,maxp) = triangulacond(pot)
        
        cnodo = pot.calculavarcond()

        if maxp <= L:
            result.value = pot
        else:
            pot.combinafacil(orden,M=6)
            l0 = []
            l1 = []
            p0 = pot.reducenv(cnodo, l0, inplace = False)
            p1 = pot.reducenv(-cnodo, l1, inplace = False)
            p0.simplifica(l0,M)
            p1.simplifica(l1,M)

            if p0.contradict and p1.contradict:
                result.anula()
                return result

            if p0.trivial() and p1.trivial():
                return result

            conf.append(-cnodo)
            h0 = calculaglobal(p0,conf,L)
            conf.pop()

            conf.append(cnodo)

            h1 = calculaglobal(p1,conf,L)
            conf.pop()
            
            
            


            if h0.value.contradict and h1.value.contradict:
                result.anula()

                return result

            if h0.trivial() and h1.trivial():
                return result
            
            result.asignavarhijos(cnodo,h0,h1)

            

        return result

def createft(nt):
    ar = arbol()
    
    if len(nt.listavar)==0:
        if ar.contradict:
            ar.anula()
        return ar
    elif len(nt.listavar) == 1:
        if nt.tabla.trivial:
            return ar
        elif nt.tabla.contradict:
            ar.anula()
            return ar
        elif not nt.tabla[0]:
            ar.unit.add(nt.listavar[0])
        elif not nt.tabla[1]:
            ar.unit.add(-nt.listavar[0])
    else:
        ar.value = nt
    return ar



class arbol:
    def __init__(self):
        self.var = 0
        self.value = PotencialTabla()
        self.hijos = [None,None]

    def anula(self):
        self.var = 0
        self.value.anula()
        self.hijos = [None,None]



            



    def void(self):
        self.var = 0
        self.value = simpleClausulas()
        self.unit = set()
        self.hijos = [None,None]

    def trivial(self):
        if self.value.trivial() and self.var == 0:
            return True
        else:
            return False


    def asignavar(self,p):
        self.var = p
        self.value = None

        self.hijos[0] = arbol()
        self.hijos[1] = arbol()

    def asignavarhijos(self,p,h0,h1):
        self.var = p

        self.hijos[0] = h0
        self.hijos[1] = h1





    def asignaval(self,x):
        self.var = 0
        self.value = x
        self.hijos = [None,None]

    def asignahijo(self,t,i):
        self.hijos[i] = t

    def imprime(self, str = ''):

            print (str +"variable ",self.var)
            if self.var==0:
                self.value.imprime()
            else:
                print(str +"hijo 1")
                self.hijos[0].imprime(str  + '   ')
                print(str +"hijo 2")
                self.hijos[1].imprime(str  + '   ')

    def getvars(self):
        vars = set(self.value.listavar)
        vu = { (abs(x)) for x in self.unit}
        vars.update(vu)
        if not self.var == 0:
            vars.update(self.hijos[0].getvars())
            vars.update(self.hijos[1].getvars())
        return vars



    def lon(self):
        return (len(self.value.unit) + len(self.value.listaclaus))

    def nulo(self):
        if self.var == 0 and not self.unit and self.value.trivial():
            return True
        else:
            return False

    def copia(self):
        res = arbol()

        if self.var == 0:
            res.asignaval(self.value.copia())
            res.unit = self.unit.copia()

        else:
            v = self.var
            h0 = self.hijos[0].copia()
            h1 = self.hijos[1].copia()
            u = self.unit.copia()
            res.asignavarhijosv(v,h0,h1,u)

        return res




    


    def reduce(self,v, inplace = False):
        res = self if inplace else self.copia()
        if v in res.unit:
            res.unit.discard(v)
        if -v in res.unit:
            res.anula
            res.contradict = True
            return res
    
        res.value.reduce([v], inplace=True)
        if res.value.contradict:
            res.anula()
            return res 

        if len(res.value.listvar)==1:
            if res.value.trivial():
                res.value = nodoTabla()

            elif not res.value.tabla[0]:
                nv = res.value.listavar[0]
                res.insertau({nv})
            elif not res.value.tabla[1]:
                nv = -res.value.listavar[0]
                res.insertau({-nv})
            if inplace:
                return res
            else:
                return

        if not res.var == 0:
            if res.var == v:
                res.hijos[1].value.combina(res.value, inplace=True)
                res.value = res.hijos[1].value
                res.var = res.hijos[1].var
                res.hijos = res.hijos[1].hijos

            elif -res.var == v:
                res.hijos[0].value.combina(res.value, inplace=True)
                res.value = res.hijos[0].value
                res.var = res.hijos[0].var
                res.hijos = res.hijos[0].hijos
            else:
                res.hijos[0].reduce(v,inplace=True)
                res.hijos[1].reduce(v, inplace=True)

        if not inplace:
            return res

            


    def reduces(self,s, inplace=False):
        
        v = set(s)

        res = self if inplace else self.copia()
        
        res.unit.difference_update(v)
        mv = set(map(lambda x:-x,v))
        if mv.intersection(res.unit):
            res.anula
            res.contradict = True
            return res
        res.value.reduce(list(v), inplace=True)
        if res.value.contradict:
            res.asignaval(res.value,set())
            return res
        if not res.var == 0:
            if res.var in v:
                res.hijos[1].reduces(s,inplace=True)
                res.hijos[1].value.combina(res.value)
                res.value = res.hijos[1].value
                res.var = res.hijos[1].var
                res.hijos = res.hijos[1].hijos

            elif -res.var in v:
                res.hijos[0].reduces(s,inplace=True)
                res.hijos[0].value.combina(res.value)
                res.value = res.hijos[0].value
                res.var = res.hijos[0].var
                res.hijos = res.hijos[0].hijos
            else:
                res.hijos[0].reduces(v, inplace=True)
                res.hijos[1].reduces(v, inplace=True)

        if not inplace:
            return res



    


                            

        

   

    

    

    def normaliza(self,N, inplace = True):
      
        if self.var == 0:
            return
        else:
            self.hijos[0].normaliza(N)
            self.hijos[1].normaliza(N)
            v = self.var
            if self.hijos[0].contradict:
                self.unit.add(v)
                self.hijos[1].union_update(self.unit)
                self.value = self.hijos[1].value
                self.var = self.hijos[1].var
                self.hijos = self.hijos[1].hijos

            elif self.hijos[1].contradict:
                self.unit.add(-v)
                self.hijos[0].union_update(self.unit)
                self.value = self.hijos[0].value
                self.var = self.hijos[0].var
                self.hijos = self.hijos[0].hijos
            
            else:
                vars = self.hijos[0].unit.intersection(self.hijos[1].unit)
                if vars:
                    self.unit.update(vars)
                    self.hijos[0].unit.difference_update(vars)
                    self.hijos[1].unit.difference_update(vars)

            if  self.hijos[0].var == 0 and self.hijos[1].var == 0:
                vars = set(self.hijos[0].value.listavar).union(set(self.hijos[1].value.listavar))
                varsunit0 = set(map(abs,self.hijos[0].value.unit))
                varsunit1 = set(map(abs,self.hijos[1].value.unit))
                vars.update(varsunit0.union(varsunit1))
                if len(vars) < N:
                    l0 = self.hijos[0].value
                    l1 = self.hijos[1].value
                    self.hijos[0].unit.add(-v)
                    self.hijos[1].unit.add(v)
                    l0.extendunits(self.hijos[0].unit)
                    l1.extendunits(self.hijos[1].unit)
                    l0.suma(l1, inplace=True)
                    self.value = l0
                    self.var = 0

            


            

    def insertau(self,units,conf,N, posvar):
        if self.unit.intersection(conf):
                return
        else:
            neg = set(map(lambda x: -x, self.unit))
            conf.difference_update(neg)
            
        if not conf:
            self.reduces(units)
            self.unit.update(units)
        elif self.var==0:
            
            va = max (conf, key = lambda x: posvar[abs(x)])
            v = abs(va)
            tab0 = self.value.reduce(-v, inplace=False)
            tab1 = self.value.reduce(v, inplace=False)
            ar0 = createft(tab0)
            ar1 = createft(tab1)

            self.asignavarhijosv(v,ar0,ar1,self.unit)

            if self.hijos[0].contradict:
                self.unit.add(v)
                self.hijos[1].union_update(self.unit)
                self.value = self.hijos[1].value
                self.var = self.hijos[1].var
                self.hijos = self.hijos[1].hijos
                conf.discard(va)
                self.insertaunit(units,conf,N,posvar)
                return



            elif self.hijos[1].contradict:
                self.unit.add(-v)
                self.hijos[0].union_update(self.unit)
                self.value = self.hijos[0].value
                self.var = self.hijos[0].var
                self.hijos = self.hijos[0].hijos
                self.insertaunit(units,conf,N,posvar)
                return

            conf.discard(va)
            if v == -va:
                self.hijos[0].insertaunit(units,conf,N,posvar)
            else:
                self.hijos[1].insertaunit(units,conf,N,posvar)
        else:
            v = self.var
            if -v in conf:
                conf.discard(-v)
                self.hijos[0].insertaunit(units,conf,N,posvar)
            elif v in conf:
                conf.discard(v)
                self.hijos[1].insertaunit(units,conf,N,posvar)
            elif -v in units:
                r = min(conf,key= lambda x: posvar[abs(x)])
                conf.discard(r)
                self.hijos[0].insertaunit({r},conf,N,posvar)
            elif v in units:
                r = min(conf,key= lambda x: posvar[abs(x)])
                conf.discard(r)
                self.hijos[1].insertaunit({r},conf,N,posvar)
            else:
                self.hijos[1].insertaunit(units,conf.copy(),N,posvar)
                self.hijos[0].insertaunit(units,conf,N,posvar)


    def insertatabla(self,tab,conf,N, posvar):
        if self.unit.intersection(conf):
                return
        else:
            neg = set(map(lambda x: -x, self.unit))
            conf.difference_update(neg)
        tab.reduce(self.unit,inplace =True )
        if tab.tabla.contradict:
            self.anula()
            self.contradict = True
            return

        if tab.tabla.ndim==1:
            if not tab.tabla[0]:
                h = {tab.listavar[0]}
                self.insertaunits(h,conf,N,posvar)
            elif not tab.tabla[1]:
                h = {-tab.listavar[0]}
                self.insertaunits(h,conf,N,posvar)
            return




        if not conf:
            if self.var == 0:
                arb = createft(tab)
                if arb.var ==0:
                    self.asignaval(arb.value,arb.unit)
                else:
                    self.asignavarhijosv(arb.var,arb.hijos[0],arb.hijos[1],arb.unit)
            else:
                v = self.var
                t0 = tab.reduce(-v,inplace = False)
                t1 = tab.reduce(v,inplace = False)
                self.hijos[0].insertatabla(t0,conf,N,posvar)
                self.hijos[1].insertatabla(t1,conf,N,posvar)
        elif self.var==0:
            va = max (conf, key = lambda x: posvar[abs(x)])
            v = abs(va)
            tab0 = self.value.reduce(-v, inplace=False)
            tab1 = self.value.reduce(v, inplace=False)
            ar0 = createft(tab0)
            ar1 = createft(tab1)

            self.asignavarhijosv(v,ar0,ar1,self.unit)

            if self.hijos[0].contradict:
                self.unit.add(v)
                self.hijos[1].union_update(self.unit)
                self.value = self.hijos[1].value
                self.var = self.hijos[1].var
                self.hijos = self.hijos[1].hijos
                conf.discard(va)
                self.insertatabla(tab,conf,N,posvar)
                return



            elif self.hijos[1].contradict:
                self.unit.add(-v)
                self.hijos[0].union_update(self.unit)
                self.value = self.hijos[0].value
                self.var = self.hijos[0].var
                self.hijos = self.hijos[0].hijos
                self.insertatabla(tab,conf,N,posvar)
                return

            conf.discard(va)
            if v == -va:
                self.hijos[0].insertatabla(tab,conf,N,posvar)
            else:
                self.hijos[1].insertatabla(tab,conf,N,posvar)


        else:
            v = self.var
            if v in conf:
                conf.discard(v)
                self.hijos[1].insertatabla(tab,conf,N,posvar)
            elif -v in conf:
                conf.discard(-v)
                self.hijos[0].insertatabla(tab,conf,N,posvar)
            else:
                self.hijos[0].insertatabla(tab,conf.copy(),N,posvar)
                self.hijos[1].insertatabla(tab,conf.copy(),N,posvar)





        return
    
    def inserta(self, p, conf):
        return

    def combina(self,t,N,varpos,inplace=True,des=True):
        res = self if inplace else self.copia()

        t.reduce(res.units, inplace=True)
        res.reduce(t.units, inplace = True)
        if res.contradict:
            return

        res.units.update(t.units)
        t.units = ()

        if res.var == 0:
            if t.var == 0:
                vars = set(res.value.listavars).union(t.value.listavars)
                if len(vars) <=N:
                    res.value.combina(t.value,inplace = True)
                else:
                    pot = PotencialTabla()
                    pot.listap.append(res.value)
                    pot.listap.append(t.value)
                    ar = calculadesdePotencial(pot,varpos)
                    res.hijos = ar.hijos
                    res.value  = ar.value
                    res.var = ar.var
                    res.contradict = ar.contradict
            else:
                res.hijos = t.hijos
                res.value  = t.value
                res.var = t.var
                res.unit = t.unit
                res.contradict = t.contradict

        else:
            v = res.var
            r0 = t.reduce(v, inplace=False)
            r1 = t.reduce(-v, inplace=False)
            res.hijos[0].combina(r0,N, varpos)
            res.hijos[1].combina(r1,N, varpos)


        if not inplace:
            return res        
               









