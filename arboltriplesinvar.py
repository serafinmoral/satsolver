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
    lista1 = []
    lista2 = []
    lista3 = []
    unit = set()
    for cl in lista:
        if len(cl)==1:
            unit.add(cl.pop())
        elif var in cl:
            cl.discard(var)
            lista1.append(cl)
        elif -var in cl:
            cl.discard(-var)
            lista2.append(cl)
        else:
            lista3.append(cl)
    return (lista1,lista2,lista3,unit)


def computefromLista(x,N):

        result = arboltriple()
        
        if len(x)<= N:
            valor = simpleClausulas()
            for cl in x:
                valor.insertar(cl)

            result.asignaval(valor)
        else:
            var = calculavar(x)    
            (l0,l1,l2,u) = split(x,var)
            su = simpleClausulas()
            su.unit= u.copy()
            su.listavar = set(map(abs,u))
            h0 = computefromLista(l0,N)
            h1 = computefromLista(l1,N)
            h2 = computefromLista(l2,N)

            result.asignavarhijos(var,h0,h1,h2,su)
        
        return result

def computeSimpleSet(x):
    res = simpleClausulas()
    res.listavar = set(map(abs,x))
    res.unit = x.copy()
    return res


class arboltriple:
    def __init__(self):
        self.var = 0
        self.value = simpleClausulas()
        self.hijos = [None,None,None]
        self.contradict = False

    def anula(self):
        self.var = 0
        x = simpleClausulas()
        x.insertar(set())
        self.value = x
        self.hijos = [None,None,None]

    def asignavar(self,p):
        self.var = p
        self.value = simpleClausulas()

        self.hijos[0] = arboltriple()
        self.hijos[1] = arboltriple()
        self.hijos[2] = arboltriple()

    def asignavarhijos(self,p,h0,h1,h2,val = simpleClausulas()):
        self.var = p
        self.value = val

        self.hijos[0] = h0
        self.hijos[1] = h1
        self.hijos[2] = h2


        
    def asignaval(self,x):
        self.var = 0
        self.value = x
        self.hijos = [None,None,None]
        
        
    def asignahijo(self,t,i):
        self.hijos[i] = t
        
    def imprime(self):
       
        print("valor " , self.value.listaclaus)
        print ("unitarias " , self.value.unit)

        if not self.var == 0:
            print ("variable ",self.var)
            print("hijo 1")
            self.hijos[0].imprime()
            print("hijo 2")
            self.hijos[1].imprime()
            print("hijo 3")
            self.hijos[2].imprime()
        
        
    def copia(self):
        res = arboltriple()


        if self.var>0:
            v = self.var
            h0 = self.hijos[0].copia()
            h1 = self.hijos[1].copia()
            h2 = self.hijos[2].copia()
            res.asignavarhijos(v,h0,h1,h2,self.value.copia())
        else:
            res.asignaval(self.value.copia())


        return res

    


    def insertaclau(self,cl,tres = False):
        if self.var == 0:
            self.value.insertar(cl)
        elif len(cl)==1:
            self.value.insertar(cl)
            self.simplificavar(cl.copy().pop())
            self.normaliza()
        else:
            v = self.var
            if v in cl:
                self.hijos[0].insertaclau(self,cl.discard(v),tres)
            elif -v in cl:
                self.hijos[1].insertaclau(self,cl.discard(-v),tres)
            elif tres:
                self.hijos[2].insertaclau(self,cl,tres)
            

  
    def simplificavar(self,v):

        self.value.simplificavar(v)
        if self.value.contradict:
            self.anula()
            return
            
        if self.var == abs(v):
            if v>0:
                base = self.hijos[0]
            elif v<0:
                base = self.hijos[1]
            base.combina(self.hijos[2])
            self = base
        else:
            self.hijos[0].simplificavar(v)
            self.hijos[1].simplificavar(v)
            self.hijos[2].simplificavar(v)           

    def normaliza(self,N=200):
        if self.var == 0:
            if len(self.value.listaclaus) > N:
                x = self.value.listaclaus
                var = calculavar(x)    
                (l0,l1,l2,u) = split(x,var)
                h0 = computefromLista(l0,N)
                h1 = computefromLista(l1,N)
                h2 = computefromLista(l2,N)
                su = computeSimpleSet(u)

                self.asignavarhijos(var,h0,h1,h2,su)
        else:
            self.hijos[0].normaliza(N)
            self.hijos[1].normaliza(N)
            self.hijos[2].normaliza(N)

            if  self.hijos[2].value.contradict or (  self.hijos[1].value.contradict and  self.hijos[2].value.contradict  ):
                h = simpleClausulas()
                h.insertar(set())
                self.asignaval(h)
            elif self.hijos[1].value.contradict:
                self.simplificavar(self.var)
            elif self.hijos[1].value.contradict:
                self.simplificavar(-self.var)
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
        (s0,s1,s2) = self.value.splitborra(v,n)
        if self.var == 0:
            t0 = arboltriple()
            t1 = arboltriple()
            t2 = arboltriple()
            t0.asignaval(s0)
            t1.asignaval(s1)
            t2.asignaval(s2)
        else:
            nv = self.var
            if (nv==v):
                t0 = self.hijos[0].copia()
                t1 = self.hijos[1].copia()
                t2 = self.hijos[2].copia()
                t0.insertasimple(s0,set())
                t1.insertasimple(s1,set())
                t2.insertasimple(s2,set())

            else:
                (t00, t01,t02) = self.hijos[0].splitborra(v,n)
                (t10, t11,t12) = self.hijos[1].splitborra(v,n)
                (t20, t21,t22) = self.hijos[2].splitborra(v,n)
                t0 = arboltriple()
                t1 = arboltriple()
                t2 = arboltriple()
                t0.asignavarhijos(nv,t00,t10,t20,s0)
                t1.asignavarhijos(nv,t01,t11,t21,s1)
                t2.asignavarhijos(nv,t02,t12,t22,s2)
        return(t0,t1,t2)

    def combinaborrasimple(self,g,conf = set()):
        if self.var == 0:
            if not conf:
                prod = g.combinaborra(self.value)
                res = arboltriple()
                res.asignaval(prod)
                res.normaliza()
                return res
            else:
                h = conf.pop()
                (t0,t1,t2) = self.splitborra(abs(h))
                r2 = t2.combinaborrasimple(g,conf)
                
                res = arboltriple()

                if h>0:
                    r0 = t0.combinaborrasimple(g,conf)
                    r0.inserta(r2)
                    r1 = arboltriple()    
                elif h<0:
                    r1 = t1.combinaborrasimple(g,conf)
                    r1.inserta(r2)

                    r0 = arboltriple()  
                conf.add(h)
                r2 = arboltriple()
                res.asignavarhijos(abs(h),r0,r1,r2)
                return res

        else:
            v = self.var                                                                               
            res = arboltriple()
            (s0,s1,s2) = self.value.splitborra(v)
            if v in conf:
                conf.discard(v)
                r0 = self.hijos[0].combinaborrasimple(g,conf)
                r2 = self.hijos[2].combinaborrasimple(g,conf)
                as0 = arboltriple()
                as2 = arboltriple()
                as0.asignaval(s0)
                as2.asignaval(s2)
                r0.inserta(r2)
                r0.inserta(as0.combinaborrasimple(g,conf) )
                r0.inserta(as2.combinaborrasimple(g,conf))
                conf.add(v)

                r1 = arboltriple()
                r2 = arboltriple()

            elif -v in conf:
                conf.discard(-v)
                r1 = self.hijos[1].combinaborrasimple(g,conf)
                r2 = self.hijos[2].combinaborrasimple(g,conf)
                as1 = arboltriple()
                as2 = arboltriple()
                as1.asignaval(s1)
                as2.asignaval(s2)
                r1.inserta(r2)
                r1.inserta(as1.combinaborrasimple(g,conf) )
                r1.inserta(as2.combinaborrasimple(g,conf))
                conf.add(-v)
                r1.inserta(r2)
                r0 = arboltriple()
                r2 = arboltriple()
            else: 
                (g0,g1,g2) = g.splitborra(v)
                as0 = arboltriple()
                as1 = arboltriple()
                as2 = arboltriple()
                as0.asignaval(s0)
                as1.asignaval(s1)
                as2.asignaval(s2)


                r0 = self.hijos[0].combinaborrasimple(g0,conf)
                r01 = self.hijos[2].combinaborrasimple(g0,conf)
                r02 = self.hijos[0].combinaborrasimple(g2,conf)

                r0.inserta(as0.combinaborrasimple(g0,conf))
                r01.inserta(as2.combinaborrasimple(g0,conf)  )
                r02.inserta(as0.combinaborrasimple(g2,conf)  )

                r0.inserta(r01)
                r0.inserta(r02)
                r1 = self.hijos[1].combinaborrasimple(g1,conf.copy())
                r11 = self.hijos[2].combinaborrasimple(g1,conf.copy())
                r12 = self.hijos[1].combinaborrasimple(g2, conf.copy())

                r1.inserta(as1.combinaborrasimple(g1,conf))
                r11.inserta(as2.combinaborrasimple(g1,conf)  )
                r12.inserta(as1.combinaborrasimple(g2,conf)  )


                r1.inserta(r11)
                r1.inserta(r12)
                r2 = self.hijos[2].combinaborrasimple(g2,conf)
                r2.inserta(as2.combinaborrasimple(g2,conf))
                
                
            res.asignavarhijos(v,r0,r1,r2)
            return res


    def combinaborra(self,t,conf = set()):
        h = t.combinaborrasimple(self.value,conf)
        if self.var == 0:
            return h
        else:
            v = self.var
            conf.add(v)
            r0 = self.hijos[0].combinaborra(t,conf)
            conf.discard(v)
            conf.add(-v)
            r1 = self.hijos[1].combinaborra(t,conf)
            conf.discard(-v)
            r2 = self.hijos[2].combinaborra(t,conf)
            r0.inserta(r1)
            r0.inserta(r2)
            r0.inserta(h)
        
            
            return r0

    def insertasimple(self,g,conf= set()):
        if self.var == 0:
            g.adconfig(conf)
            for cl in g.listaclaus:
                self.value.insertar(cl)
            self.normaliza()
        else:
                v = self.var
                if v in conf:
                    conf.discard(v)
                    self.hijos[0].insertasimple(g,conf)
                    conf.add(v)
                elif -v in conf:
                    conf.discard(-v)
                    self.hijos[1].insertasimple(g,conf)
                    conf.add(-v)
                else:
                    (l0,l1,l2) = g.splitborra(v)
                    self.hijos[0].insertasimple(l0,conf)
                    self.hijos[1].insertasimple(l1,conf)
                    self.hijos[2].insertasimple(l2,conf)


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
                    self.hijos[2].inserta(l2,conf)



        else:
            v = t.var
            conf.add(v)
            self.inserta(t.hijos[0],conf)
            conf.discard(v)
            conf.add(-v)
            self.inserta(t.hijos[1],conf)
            conf.discard(-v)
            self.inserta(t.hijos[2],conf)
    
        
 
   
            
    
                
            
        
    # def noesta(self,cl):
    #     if self.var==0:
    #         return self.value.noesta(cl)
    #     else:
    #         v = self.var
    #         if v in cl:
    #             return self.hijos[0].noesta(cl - {v}) or self.hijos[2].noesta(cl)
    #         elif -v in cl:
    #             return self.hijos[1].noesta(cl - {-v}) or self.hijos[2].noesta(cl)
    #         else:
    #             return self.hijos[2].noesta(cl) 
        
            
    # def combinaborra2(self,t,conf = set()):
    #     if self.var == 0:
    #         if t.var == 0:
    #             if not conf:
    #                 prod = self.value.combinaborra(t.value)
    #                 res = arboltriple()
    #                 res.asignaval(prod)
    #                 res.normaliza()
    #                 return res
    #             else:
    #                 h = conf.pop()
    #                 (t0,t1,t2) = t.splitborra(abs(h))
    #                 r2 = self.combinaborra(t2,conf.copy())
                   
    #                 res = arboltriple()

    #                 if h>0:
    #                     r0 = self.combinaborra(t0,conf)
    #                     r0.inserta(r2)
    #                     r1 = arboltriple()    
    #                 elif h<0:
    #                     r1 = self.combinaborra(t1,conf)
    #                     r1.inserta(r2)

    #                     r0 = arboltriple()  
                
    #                 r2 = arboltriple()
    #                 res.asignavarhijos(abs(h),r0,r1,r2)
    #                 return res

    #         else:
    #             v = t.var
    #             res = arboltriple()

    #             if v in conf:
    #                 conf.discard(v)
    #                 r0 = self.combinaborra(t.hijos[0],conf.copy())
    #                 r2 = self.combinaborra(t.hijos[2],conf)
    #                 r0.inserta(r2)
    #                 r1 = arboltriple()
    #                 r2 = arboltriple()

    #             elif -v in conf:
    #                 conf.discard(-v)
    #                 r1 = self.combinaborra(t.hijos[1],conf.copy())
    #                 r2 = self.combinaborra(t.hijos[2],conf)
    #                 r1.inserta(r2)
    #                 r0 = arboltriple()
    #                 r2 = arboltriple()
    #             else: 
    #                 (t0,t1,t2) = self.splitborra(v)

    #                 r0 = t0.combinaborra(t.hijos[0],conf.copy())
    #                 r01 = t0.combinaborra(t.hijos[2],conf.copy())
    #                 r02 = t2.combinaborra(t.hijos[0],conf.copy())
    #                 r0.inserta(r01)
    #                 r0.inserta(r02)
    #                 r1 = t1.combinaborra(t.hijos[1],conf.copy())
    #                 r11 = t1.combinaborra(t.hijos[2],conf.copy())
    #                 r12 = t2.combinaborra(t.hijos[1],conf.copy())
    #                 r1.inserta(r11)
    #                 r1.inserta(r12)
    #                 r2 = t2.combinaborra(t.hijos[2],conf)
                    
                    
    #             res.asignavarhijos(v,r0,r1,r2)
    #             return res
    #     else:
    #         v = self.var
    #         conf.add(v)
    #         r0 = self.hijos[0].combinaborra(t,conf.copy())
    #         conf.discard(v)
    #         conf.add(-v)
    #         r1 = self.hijos[1].combinaborra(t,conf.copy())
    #         conf.discard(-v)
    #         r2 = self.hijos[2].combinaborra(t,conf)
    #         r0.inserta(r1)
    #         r0.inserta(r2)
    #         return r0



        
    
              
    # def simplifica(self, refarbol, config = set()):
    #     if self.var == 0:
    #         if refarbol.var == 0:
    #                 self.value.simplificaconfig(refarbol.value,config)
    #         else:
    #             v = refarbol.var
    #             if v in config:
    #                 config.discar(v)
    #                 self.simplifica(refarbol.hijos[0],config)
    #                 config.add(v)
    #             elif -v in config:
    #                 config.discar(-v)    
    #                 self.simplifica(refarbol.hijos[1],config)
    #                 config.add(-v)
    #             self.simplifica(refarbol.hijos[2],config)
    #     else:
    #         v = self.var
    #         config.add(v)
    #         self.hijos[0].simplifica(refarbol, config)
    #         config.discard(v)
    #         config.add(-v)
    #         self.hijos[1].simplifica(refarbol, config)
    #         config.discard(-v)
    #         self.hijos[2].simplifica(refarbol, config)

