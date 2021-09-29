# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 11:34:37 2021

@author: efraín
"""
from BTSA_SimpleClausulas import * 
class arboldoble:
    def __init__(self):
        self.var = 0
        self.value = simpleClausulas()
        self.hijos = [None,None]
        self.contradict = False
        self.unit = set()

    def void(self):
        self.var = 0
        self.value = simpleClausulas()
        self.unit = set()
        self.hijos = [None,None]

    def asignaval(self,x):
        self.var = 0
        self.value = x
        self.hijos = [None,None]

    def asignavarhijosv(self,p,h0,h1,v):
        self.var = p
        self.hijos[0] = h0
        self.hijos[1] = h1
        self.value = v

    def lon(self):
        return (len(self.value.unit) + len(self.value.listaclaus))  

    def copia(self):
        res = arboldoble()
        if self.var == 0:
            res.asignaval(self.value.copia())
        else:
            v = self.var
            h0 = self.hijos[0].copia()
            h1 = self.hijos[1].copia()
            value = self.value.copia()
            res.asignavarhijosv(v,h0,h1,value)
        return res

    def insertaunits(self,sunits):
        self.simplificaunits(sunits)
        if not self.value.contradict:
            self.value.unit.update(sunits)

    def insertaclau(self,cl):
        if self.var == 0:
            self.value.insertar(cl)
            return
        neg = set(map(lambda x:-x,self.value.unit))
        cl.difference_update(neg)
        if len(cl)==1:
            v = cl.pop()
            self.value.insertaunit(v)
            self.hijos[0].simplificaunit(v)
            self.hijos[1].simplificaunit(v)
        else:
            
            v = self.var
            if v in cl:
                self.hijos[0].insertaclau(self,cl.discard(v))
            elif -v in cl:
                self.hijos[1].insertaclau(self,cl.discard(-v))
            else:
                self.hijos[0].insertaclau(self,cl.copy())
                self.hijos[1].insertaclau(self,cl)

    def normaliza(self,N=100):
        if self.var == 0:
            if len(self.value.listaclaus) > N:
                x = self.value.listaclaus
                var = calculavar(x)    
                (l0,l1,unit) = split(x,var)
                
                ug = simpleClausulas()
                ug.unit = unit.copy()
                ug.unit.update(self.unit)
                h0 = computefromSimple(l0,N)
                h1 = computefromSimple(l1,N)

                self.asignavarhijosv(var,h0,h1,ug)
        else:
            self.hijos[0].normaliza(N)   
            self.hijos[1].normaliza(N)
            v = self.var
            if self.hijos[0].value.contradict:
                self.value.insertar({v})
                self.hijos[1].value.combina(self.value)
                self.value = self.hijos[1].value
                self.var = self.hijos[1].var

                self.hijos = self.hijos[1].hijos
                 
            elif self.hijos[1].value.contradict:
                self.value.insertar({-v})
                self.hijos[0].value.combina(self.value)
                self.value = self.hijos[0].value
                self.var = self.hijos[0].var

                self.hijos = self.hijos[0].hijos

            elif self.hijos[0].var == 0 and self.hijos[1].var == 0 and \
                 (self.hijos[0].lon() + self.hijos[1].lon() <=N):
                v = self.var
                self.hijos[0].value.advalue(v)
                self.hijos[1].value.advalue(-v)
                s1 = self.hijos[0].value
                s2 = self.hijos[1].value

                self.value.combina(s1)
                self.value.combina(s2)
                self.var = 0

    def splitborra(self,v,n=True):
        # self.value.imprime()
        (s0,s1,s2) = self.value.splitborra(v,n)
        if v in self.value.unit or -v in self.value.unit:
            t0 = arboldoble()
            t1 = arboldoble()
            t2 = self.copia()
            t2.value = s2
            t0.asignaval(s0)
            t1.asignaval(s1)
        else:
            nv = self.var
            if nv == 0:
                t0 = arboldoble()
                t1 = arboldoble()
                t2 = arboldoble()
                t0.asignaval(s0)
                t1.asignaval(s1)
                t2.asignaval(s2)
            elif (nv==v):
                t0 = self.hijos[0].copia()
                t1 = self.hijos[1].copia()
                t2 = arboldoble()
                t2.asignaval(s2)
                t0.value.combina(s0)
                t1.value.combina(s1)
            else:
                (t00, t01,t02) = self.hijos[0].splitborra(v,n)
                (t10, t11,t12) = self.hijos[1].splitborra(v,n)
                t0 = arboldoble()
                t1 = arboldoble()
                t2 = arboldoble()
                t0.asignavarhijosv(nv,t00,t10,s0)
                t1.asignavarhijosv(nv,t01,t11,s1)
                t2.asignavarhijosv(nv,t02,t12,s2)

        return(t0,t1,t2)

    def combinaborra(self,t,N,conf = set()):
        if  t.var == 0:
            return self.combinaborrasimple(t.value,N,conf)
        else:
            v = t.var
            conf.add(v)
            r0 = self.combinaborra(t.hijos[0],N,conf)
            conf.discard(v)
            
            conf.add(-v)
            r1 = self.combinaborra(t.hijos[1],N,conf)
            conf.discard(-v)
        
            r2 = self.combinaborrasimple(t.value,N,conf)

            r0.inserta(r1,N)
            r0.inserta(r2,N)
            return r0

    def combinaborrasimple(self,simple,N,conf):
            if self.var == 0:
                if not conf:
                    prod = self.value.combinaborra(simple)
                    res = arboldoble()
                    res.asignaval(prod)
                    res.normaliza(N)
                    # res.imprime()
                    return res
                else:
                    prod = self.value.combinaborrac(simple,conf)
                    res = arboldoble()
                    res.asignaval(prod)
                    res.normaliza(N)
                    # res.imprime()
                    return res
            else:
                v = self.var
                res = arboldoble()
                if not conf:
                    prod = self.value.combinaborra(simple)
                else:
                    prod = self.value.combinaborrac(simple,conf)
                res1 = arboldoble()
                res1.asignaval(prod)
                res1.normaliza(N)
                val = simpleClausulas()
                if v in conf:
                    conf.discard(v)
                    r0 = self.hijos[0].combinaborrasimple(simple,N,conf)
                    conf.add(v)
                    r1 = arboldoble()
                elif -v in conf:
                    conf.discard(-v)
                    r1 = self.hijos[1].combinaborrasimple(simple,N,conf)
                    conf.add(-v)
                    r0 = arboldoble()
                else: 
                    r0 = self.hijos[0].combinaborrasimple(simple.sel(v),N,conf)
                    r1 = self.hijos[1].combinaborrasimple(simple.sel(-v),N,conf)
                res.asignavarhijosv(v,r0,r1,val)
                res.inserta(res1,N)
                res.normaliza(N)
                return res

    def inserta(self,t,N,conf= set()):
        if t.var == 0:
            self.insertasimple(t.value,N,conf)
        else:
            v = t.var
            conf.add(v)
            self.inserta(t.hijos[0],N,conf)
            conf.discard(v)
            conf.add(-v)
            self.inserta(t.hijos[1],N,conf)
            conf.discard(-v)
            if not t.value.nulo():
                self.insertasimple(t.value,N,conf)

    def insertasimple(self,simple,N,conf=set()):
        if self.var==0:
            simple.adconfig(conf)
            for v in simple.unit:
                self.value.insertar({v})
            for cl in simple.listaclaus:
                self.value.insertar(cl)
            self.normaliza(N)
        else:
            simple.simplificaunits(self.value.unit)
            if not conf and simple.unit:
                # print ("entro en poda")
                self.insertaunits(simple.unit)
                simple.unit = set()

            v = self.var
            if v==0:
                simple.adconfig(conf)
                for v in simple.unit:
                    self.value.insertar({v})
                for cl in simple.listaclaus:
                    self.value.insertar(cl)
                self.normaliza(N)
            else:
                if v in conf:
                    conf.discard(v)
                    self.hijos[0].insertasimple(simple,N,conf)
                    conf.add(v)
                elif -v in conf:
                    conf.discard(-v)
                    self.hijos[1].insertasimple(simple,N,conf)
                    conf.add(-v)
                else:
                    (l0,l1,l2) = simple.splitborra(v)
                    self.hijos[0].insertasimple(l0,N,conf)
                    self.hijos[1].insertasimple(l1,N,conf)
                    self.hijos[0].insertasimple(l2.copia(),N,conf)
                    self.hijos[1].insertasimple(l2,N,conf)

    def simplificaunits(self,s):
        self.value.simplificaunits(s)
        if self.value.contradict:
            self.asignaval(self.value)
            return
        if not self.var == 0:
            self.hijos[0].simplificaunits(s)
            self.hijos[1].simplificaunits(s)
            if self.hijos[0].value.contradict or self.hijos[1].value.contradict:
                self.normaliza()
            elif self.var in s:
                self.hijos[1].value.combina(self.value)
                self.value = self.hijos[1].value
                self.var = self.hijos[1].var
                self.hijos = self.hijos[1].hijos
            
            elif -self.var in s:
                self.hijos[0].value.combina(self.value)
                self.value = self.hijos[0].value
                self.var = self.hijos[0].var
                self.hijos = self.hijos[0].hijos

def calculavar(lista):
    cuenta = dict()
    for cl in lista:
        if (len(cl))>1:
            vars = map(abs,cl)
            for v in vars:
                if v in cuenta:
                    cuenta[v]  += 1
                else:
                    cuenta[v] = 1
    return max(cuenta, key=(lambda key: cuenta[key]))

def calculavar2(lista):
    cuenta = dict()
    for cl in lista:
        if (len(cl))>1:
            vars = map(abs,cl)
            for v in vars:
                if v in cuenta:
                    cuenta[v]  = min(len(cl),cuenta[v])
                else:
                    cuenta[v] = len(cl)
    return min(cuenta, key=(lambda key: cuenta[key]))

def split(lista,var):
    lista1 = simpleClausulas()
    lista2 = simpleClausulas()
    unit = set()
    for cl in lista:
        if len(cl)==1:
            v = cl.pop()
            unit.add(v)
            if v == var:
                lista1.insertar({})
            if v == -var:
                lista2.insertar({})
        elif var in cl:
            cl.discard(var)
            lista1.insertar(cl)
        elif -var in cl:
            cl.discard(-var)
            lista2.insertar(cl)
        else:
            lista1.insertar(cl)
            lista2.insertar(cl.copy())
    return (lista1,lista2,unit)

def computefromSimple(x,N):
        result = arboldoble()
        if len(x.listaclaus)<= N:
            result.asignaval(x)
        else:
            var = calculavar2(x.listaclaus)    
            (l0,l1,unit) = split(x.listaclaus,var)
            h0 = computefromSimple(l0,N)
            h1 = computefromSimple(l1,N)
            value = simpleClausulas()
            value.unit = x.unit
            value.unit.update(unit)
            result.asignavarhijosv(var,h0,h1,value)
        return result