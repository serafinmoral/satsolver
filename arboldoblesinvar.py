# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import math
from SimpleClausulas import * 

def calculavar(lista):
    # print(    len(lista))
    # print(lista)
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


def split(lista,var):
    lista1 = simpleClausulas()
    lista2 = simpleClausulas()
    unit = set()
    for cl in lista:
        if len(cl)==1:
            v = cl.pop()
            unit.add(v)
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
            var = calculavar(x.listaclaus)    
            (l0,l1,unit) = split(x.listaclaus,var)
            h0 = computefromSimple(l0,N)
            h1 = computefromSimple(l1,N)
            value = simpleClausulas()
            value.unit = x.unit
            value.unit.update(unit)


            result.asignavarhijosv(var,h0,h1,value)
        
        return result

def computefromLista(x,N):

        y = simpleClausulas()
        for cl in x:
            y.insertar(cl)
        
        
        
        return computefromSimple(y,N)


class arboldoble:
    def __init__(self):
        self.var = 0
        self.value = simpleClausulas()
        self.hijos = [None,None]
        self.contradict = False
        self.unit = set()
    
    def anula(self):
        self.var = 0
        x = simpleClausulas()
        x.insertar(set())
        self.value = x
        self.unit = set()
        self.hijos = [None,None]

    def asignavar(self,p):
        self.var = p
        self.value = None

        self.hijos[0] = arboldoble()
        self.hijos[1] = arboldoble()

    def asignavarhijos(self,p,h0,h1):
        self.var = p
        self.value = None

        self.hijos[0] = h0
        self.hijos[1] = h1

    def asignavarhijosv(self,p,h0,h1,v):
        self.var = p
        self.value = None

        self.hijos[0] = h0
        self.hijos[1] = h1
        self.value = v
        self.imprime()



        
    def asignaval(self,x):
        self.var = 0
        self.value = x
        self.hijos = [None,None]
        self.imprime()        
        
    def asignahijo(self,t,i):
        self.hijos[i] = t
        
    def imprime(self):
            print("valor clausulas" , self.value.listaclaus)
            print("valor unit" , self.value.unit)

            print ("variable ",self.var)
            if not self.var == 0:
                print("hijo 1")
                self.hijos[0].imprime()
                print("hijo 2")
                self.hijos[1].imprime()
            
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

    


    def insertaclau(self,cl):
        if self.var == 0:
            self.value.insertar(cl)
            return
        neg = set(map(lambda x:-x,self.unit))
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
                self.hijos[0].insertaclau(self,cl)
                self.hijos[1].insertaclau(self,cl.copy())

    def simplificaunit(self,v):
        self.value.simplificaunit(v)
        if self.value.contradict:
            self.asignaval(self.value)
            return
        if not self.var == 0:
            if self.var == v:
                self.value.hijos[1].combina(self.value)
                self = self.hijos[1]
            
            elif -self.var == v:
                self = self.hijos[0]
                self.value.hijos[0].combina(self.value)
            else:
                self.hijos[0].simplificaunit(v)
                self.hijos[1].simplificaunit(v)


                
                
    def simplifica(self, refarbol, config = set()):
        if self.var == 0:
            if refarbol.var == 0:
                    self.value.simplificaconfig(refarbol.value,config)
            else:
                v = refarbol.var
                if v in config:
                    config.discar(v)
                    self.simplifica(refarbol.hijos[0],config)
                    config.add(v)
                elif -v in config:
                    config.discar(-v)    
                    self.simplifica(refarbol.hijos[1],config)
                    config.add(-v)
                self.simplifica(refarbol.hijos[2],config)
        else:
            v = self.var
            config.add(v)
            self.hijos[0].simplifica(refarbol, config)
            config.discard(v)
            config.add(-v)
            self.hijos[1].simplifica(refarbol, config)
            config.discard(-v)
            self.hijos[2].simplifica(refarbol, config)



    def normaliza(self,N=20):
        if self.var == 0:
            if len(self.value.listaclaus) > N:
                x = self.value.listaclaus
                var = calculavar(x)    
                (l0,l1,unit) = split(x,var)
                ug = simpleClausulas()
                ug.unit = unit
                h0 = computefromSimple(l0,N)
                h1 = computefromSimple(l1,N)

                self.asignavarhijosv(var,h0,h1,ug)
        else:
            self.hijos[0].normaliza(N)   
            self.hijos[1].normaliza(N)
            if self.hijos[0].var == 0 and self.hijos[1].var == 0 and \
                 (self.hijos[0].lon() + self.hijos[1].lon() <=N):
                v = self.var
                self.hijos[0].value.addvalue(v)
                self.hijos[1].value.addvalue(-v)
                s1 = self.hijos[0].value
                s2 = self.hijos[1].value

                self.value.combina(s1).combina(s2)

    


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

    


    def combinaborra(self,t,conf = set()):
        if self.var == 0:
            if t.var == 0:
                if not conf:
                    prod = self.value.combinaborra(t.value)
                    res = arboldoble()
                    res.asignaval(prod)
                    res.normaliza()
                    return res
                else:
                    h = conf.pop()
                    (t0,t1,t2) = t.splitborra(abs(h))
                    r2 = self.combinaborra(t2,conf)
                   
                    res = arboldoble()

                    if h>0:
                        r0 = self.combinaborra(t0,conf)
                        r0.inserta(r2)
                        r1 = arboldoble()
                    elif h<0:
                        r1 = self.combinaborra(t1,conf)
                        r1.inserta(r2)
                        r0 = arboldoble()
             
                
                    
                    res.asignavarhijos(abs(h),r0,r1)
                    conf.add(h)
                    return res

            else:
                v = t.var
                res = arboldoble()
                q0 = t.hijos[0]
                q1 = t.hijos[1]
                q2 = arboldoble()
                q2.asignaval(t.value)

                if v in conf:
                    conf.discard(v)
                    r0 = self.combinaborra(q0,conf)
                    r2 = self.combinaborra(q2,conf)
                    conf.add(v)
                    r0.inserta(r2)
                    r1 = arboldoble()

                elif -v in conf:
                    conf.discard(-v)
                    r1 = self.combinaborra(q1,conf)
                    r2 = self.combinaborra(q2,conf)
                    conf.add(-v)
                    r1.inserta(r2)
                    r0 = arboldoble()
                else: 
                    (t0,t1,t2) = self.splitborra(v)

                    r0 = t0.combinaborra(q0,conf)
                    r01 = t0.combinaborra(q2,conf)
                    r02 = t2.combinaborra(q0,conf)
                    r0.inserta(r01)
                    r0.inserta(r02)
                    r1 = t1.combinaborra(q1,conf)
                    r11 = t1.combinaborra(q2,conf)
                    r12 = t2.combinaborra(q1,conf)
                    r1.inserta(r11)
                    r1.inserta(r12)
                    r2 = t2.combinaborra(q2,conf)
                    r0.inserta(r2.copia()) 
                    r1.inserta(r2)                   
                    
                res.asignavarhijos(v,r0,r1)
                return res
        else:
            v = self.var
            conf.add(v)
            r0 = self.hijos[0].combinaborra(t,conf)
            conf.discard(v)
            conf.add(-v)
            r1 = self.hijos[1].combinaborra(t,conf)
            conf.discard(-v)
            
            t2 = arboldoble()
            t2.asignaval(self.value.copia())
            r2 = t2.combinaborra(t,conf)

            r0.inserta(r1)
            r0.inserta(r2)
            return r0



        
    



    def inserta(self,t,conf= set()):
        if t.var == 0:
            if self.var == 0:
                t.value.adconfig(conf)
                for cl in t.value.listaclaus:
                    self.value.insertar(cl)
                self.normaliza()
            else:
                v = self.var
                if v in conf:
                    conf.discard(v)
                    self.hijos[0].inserta(t,conf)
                    conf.add(v)
                elif -v in conf:
                    conf.discard(-v)
                    self.hijos[1].inserta(t,conf)
                    conf.add(-v)
                else:
                    (l0,l1,l2) = t.splitborra(v)
                    self.hijos[0].inserta(l0,conf)
                    self.hijos[1].inserta(l1,conf)
                    self.hijos[0].inserta(l2.copia(),conf)
                    self.hijos[1].inserta(l2,conf)




        else:
            v = t.var
            conf.add(v)
            self.inserta(t.hijos[0],conf)
            conf.discard(v)
            conf.add(-v)
            self.inserta(t.hijos[1],conf)
            conf.discard(-v)
            nuevo = arboldoble()
            nuevo.asignaval(t.value)
            self.inserta(nuevo,conf)
    
        
 
    
                
            
        
        
        
            
        