# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import math
from SimpleClausulas import * 

def calculavar(lista):
    # print(len(lista))
    # print(lista)
    cuenta = dict()
    for cl in lista:
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
    for cl in lista:
        if var in cl:
            cl.discard(var)
            lista1.insertar(cl)
        elif -var in cl:
            cl.discard(-var)
            lista2.insertar(cl)
        else:
            lista1.insertar(cl)
            lista2.insertar(cl.copy())
    return (lista1,lista2)




def computefromSimple(x,N):

        result = arboldoble()
        
        if len(x.listaclaus)<= N:
            

            result.asignaval(x)
        else:
            var = calculavar(x.listaclaus)    
            (l0,l1) = split(x.listaclaus,var)
            h0 = computefromSimple(l0,N)
            h1 = computefromSimple(l1,N)
        

            result.asignavarhijos(var,h0,h1)
        
        return result

def compute3fromLista(x,N):

        result = arboldoble()
        
        if len(x)<= N:
            valor = simpleClausulas()
            for cl in x:
                valor.insertar(cl)

            result.asignaval(valor)
        else:
            var = calculavar(x)    
            (l0,l1,l2) = split3(x,var)
            h0 = compute3fromLista(l0,N)
            h1 = compute3fromLista(l1,N)
            h2 = compute3fromLista(l2,N)

            result.asignavarhijos(var,h0,h1,h2)
        
        return result


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


        
    def asignaval(self,x):
        self.var = 0
        self.value = x
        self.hijos = [None,None]
        
        
    def asignahijo(self,t,i):
        self.hijos[i] = t
        
    def imprime(self):
        if (self.var == 0):
            print("valor " , self.value.listaclaus)
        else:
            print ("variable ",self.var)
            print("hijo 1")
            self.hijos[0].imprime()
            print("hijo 2")
            self.hijos[1].imprime()
            print("hijo 3")
            self.hijos[2].imprime()
        
        
    def copia(self):
        res = arboltriple()

        if self.var == 0:
            res.asignaval(self.value.copia())

        else:
            v = self.var
            h0 = self.hijos[0].copia()
            h1 = self.hijos[1].copia()
            h2 = self.hijos[2].copia()
            res.asignavarhijos(v,h0,h1,h2)

        return res
    def noesta(self,cl):
        if self.var==0:
            return self.value.noesta(cl)
        else:
            v = self.var
            if v in cl:
                return self.hijos[0].noesta(cl - {v}) or self.hijos[2].noesta(cl)
            elif -v in cl:
                return self.hijos[1].noesta(cl - {-v}) or self.hijos[2].noesta(cl)
            else:
                return self.hijos[2].noesta(cl)


    def insertaclau(self,cl,tres = False):
        if self.var == 0:
            self.value.insertar(cl)
        else:
            v = self.var
            if v in cl:
                self.hijos[0].insertaclau(self,cl.discard(v),tres)
            elif -v in cl:
                self.hijos[1].insertaclau(self,cl.discard(-v),tres)
            elif tres:
                self.hijos[2].insertaclau(self,cl,tres)
            else:
                self.hijos[0].insertaclau(self,cl,tres)
                self.hijos[1].insertaclau(self,cl.copy(),tres)

                
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



    def normaliza2(self,N=300):
        if self.var == 0:
            if len(self.value.listaclaus) > N:
                x = self.value.listaclaus
                var = calculavar(x)    
                (l0,l1) = split(x,var)
                h0 = computefromSimple(l0,N)
                h1 = computefromSimple(l1,N)
                h2 = arboltriple()

                self.asignavarhijos(var,h0,h1,h2)
        else:
            self.hijos[0].normaliza2(N)   
            self.hijos[1].normaliza2(N)
            if self.hijos[0].var == 0 and self.hijos[1].var == 0 and \
                 (len(self.hijos[0].value.listaclaus) + len(self.hijos[1].value.listaclaus))<=N:
                v = self.var
                self.hijos[0].value.add(v)
                self.hijos[1].value.add(v)
                s1 = self.hijos[0]
                s2 = self.hijos[1]

                self.asignaval(  s1.combina(s2)  )

    def normaliza3(self,N=200):
        if self.var == 0:
            if len(self.value.listaclaus) > N:
                x = self.value.listaclaus
                var = calculavar(x)    
                (l0,l1,l2) = split3(x,var)
                h0 = compute3fromLista(l0,N)
                h1 = compute3fromLista(l1,N)
                h2 = compute3fromLista(l2,N)

                self.asignavarhijos(var,h0,h1,h2)
        else:
            self.hijos[0].normaliza3(N)
            self.hijos[1].normaliza3(N)
            self.hijos[2].normaliza3(N)

            if self.hijos[2].var == 0 and self.hijos[2].value.contradict:
                h = simpleClausulas()
                h.insertar(set())
                self.asignaval(h)

            elif self.hijos[0].var == 0 and self.hijos[1].var == 0 and \
                self.hijos[2].var == 0 and (len(self.hijos[0].value.listaclaus) + 
                len(self.hijos[1].value.listaclaus) +  len(self.hijos[2].value.listaclaus)  )<=N:
                v = self.var
                s1 = self.hijos[0].value
                s2 = self.hijos[1].value
                s1.advalue(v)
                s2.advalue(-v)
                
                s1.combina(s2)
                s1.combina(self.hijos[2].value)
                self.asignaval(  s1 )


    def splitborra(self,v,n=True):
        if self.var == 0:
            (s0,s1,s2) = self.value.splitborra(v,n)
            t0 = arboltriple()
            t1 = arboltriple()
            t2 = arboltriple()
            t0.asignaval(s0)
            t1.asignaval(s1)
            t2.asignaval(s2)
            return(t0,t1,t2)
        else:
            nv = self.var
            if (nv==v):
                return (self.hijos[0].copia(),self.hijos[1].copia(),self.hijos[2].copia()   )
            else:
                (t00, t01,t02) = self.hijos[0].splitborra(v,n)
                (t10, t11,t12) = self.hijos[1].splitborra(v,n)
                (t20, t21,t22) = self.hijos[2].splitborra(v,n)
                t0 = arboltriple()
                t1 = arboltriple()
                t2 = arboltriple()
                t0.asignavarhijos(nv,t00,t10,t20)
                t1.asignavarhijos(nv,t01,t11,t21)
                t2.asignavarhijos(nv,t02,t12,t22)
                return(t0,t1,t2)

    


    def combinaborra(self,t,conf = set()):
        if self.var == 0:
            if t.var == 0:
                if not conf:
                    prod = self.value.combinaborra(t.value)
                    res = arboltriple()
                    res.asignaval(prod)
                    res.normaliza3()
                    return res
                else:
                    h = conf.pop()
                    (t0,t1,t2) = t.splitborra(abs(h))
                    r2 = self.combinaborra(t2,conf.copy())
                   
                    res = arboltriple()

                    if h>0:
                        r0 = self.combinaborra(t0,conf)
                        r0.inserta3(r2)
                        r1 = arboltriple()    
                    elif h<0:
                        r1 = self.combinaborra(t1,conf)
                        r1.inserta3(r2)

                        r0 = arboltriple()  
                
                    r2 = arboltriple()
                    res.asignavarhijos(abs(h),r0,r1,r2)
                    return res

            else:
                v = t.var
                res = arboltriple()

                if v in conf:
                    conf.discard(v)
                    r0 = self.combinaborra(t.hijos[0],conf.copy())
                    r2 = self.combinaborra(t.hijos[2],conf)
                    r0.inserta3(r2)
                    r1 = arboltriple()
                    r2 = arboltriple()

                elif -v in conf:
                    conf.discard(-v)
                    r1 = self.combinaborra(t.hijos[1],conf.copy())
                    r2 = self.combinaborra(t.hijos[2],conf)
                    r1.inserta3(r2)
                    r0 = arboltriple()
                    r2 = arboltriple()
                else: 
                    (t0,t1,t2) = self.splitborra(v)

                    r0 = t0.combinaborra(t.hijos[0],conf.copy())
                    r01 = t0.combinaborra(t.hijos[2],conf.copy())
                    r02 = t2.combinaborra(t.hijos[0],conf.copy())
                    r0.inserta3(r01)
                    r0.inserta3(r02)
                    r1 = t1.combinaborra(t.hijos[1],conf.copy())
                    r11 = t1.combinaborra(t.hijos[2],conf.copy())
                    r12 = t2.combinaborra(t.hijos[1],conf.copy())
                    r1.inserta3(r11)
                    r1.inserta3(r12)
                    r2 = t2.combinaborra(t.hijos[2],conf)
                    
                    
                res.asignavarhijos(v,r0,r1,r2)
                return res
        else:
            v = self.var
            conf.add(v)
            r0 = self.hijos[0].combinaborra(t,conf.copy())
            conf.discard(v)
            conf.add(-v)
            r1 = self.hijos[1].combinaborra(t,conf.copy())
            conf.discard(-v)
            r2 = self.hijos[2].combinaborra(t,conf)
            r0.inserta3(r1)
            r0.inserta3(r2)
            return r0



        
    



    def inserta3(self,t,conf= set()):
        if t.var == 0:
            if self.var == 0:
                t.value.adconfig(conf)
                for cl in t.value.listaclaus:
                    self.value.insertar(cl)
                self.normaliza3()
            else:
                v = self.var
                if v in conf:
                    conf.discard(v)
                    self.hijos[0].inserta3(t,conf)
                    conf.add(v)
                elif -v in conf:
                    conf.discard(-v)
                    self.hijos[1].inserta3(t,conf)
                    conf.add(-v)
                else:
                    (l0,l1,l2) = t.splitborra(v)
                    self.hijos[0].inserta3(l0,conf)
                    self.hijos[1].inserta3(l1,conf)
                    self.hijos[2].inserta3(l2,conf)



        else:
            v = t.var
            conf.add(v)
            self.inserta3(t.hijos[0],conf)
            conf.discard(v)
            conf.add(-v)
            self.inserta3(t.hijos[1],conf)
            conf.discard(-v)
            self.inserta3(t.hijos[2],conf)
    
        
 
    def inserta2(self,t,conf= set()):
        if t.var == 0:
            if self.var == 0:
                t.value.adconfig(conf)
                for cl in t.value.listaclaus:
                    self.value.insertar(cl)
                self.normaliza2()
            else:
                v = self.var
                if v in conf:
                    conf.discard(v)
                    self.hijos[0].inserta2(t,conf)
                elif -v in conf:
                    conf.discard(-v)
                    self.hijos[1].inserta2(t,conf)
                else:
                    (l0,l1,l2) = t.splitborra(v)
                    self.hijos[0].inserta2(l0,conf)
                    self.hijos[1].inserta2(l1,conf)
                    self.hijos[0].inserta2(l2,conf)
                    self.hijos[1].inserta2(l2.copia(),conf)




        else:
            v = t.var
            conf.add(v)
            self.inserta2(t.hijos[0],conf)
            conf.discard(v)
            conf.add(-v)
            self.inserta2(t.hijos[1],conf)
            conf.discard(-v)
            self.inserta2(t.hijos[2],conf)
            
    
                
            
        
        
        
            
        