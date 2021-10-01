# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import math
from SimpleClausulasD import *

def calculavar(lista):
    # print(    len(lista))
    # print(lista)
    cuenta = dict()
    for cl in lista:
        if (len(cl))>1:
            vars = map(abs,cl)
            for v in vars:
                if v in cuenta:
                    cuenta[v]  += 1/len(cl)
                else:
                    cuenta[v] = 1/len(cl)
    return max(cuenta, key=(lambda key: cuenta[key]))


def calculavar2(lista):
    # print(    len(lista))
    # print(lista)
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
            lista2.insertar(cl.copy())
            lista1.insertar(cl)
    return (lista1,lista2,unit)




def computefromSimple(x,N):

        result = arboldoble()

        if len(x.listaclaus)<= N:


            result.asignaval(x)
        else:
            lista = x.calculalistatotal()
            var = calculavar2(lista)
            (l0,l1,unit) = split(lista,var)
            h0 = computefromSimple(l0,N)
            h1 = computefromSimple(l1,N)
            value = simpleClausulas()
            for z in x.unit:
                value.insertar({z})
            for z in unit:
                value.insertar({z})


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

    def void(self):
        self.var = 0
        self.value = simpleClausulas()
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

        self.hijos[0] = h0
        self.hijos[1] = h1
        self.value = v




    def asignaval(self,x):
        self.var = 0
        self.value = x
        self.hijos = [None,None]

    def asignahijo(self,t,i):
        self.hijos[i] = t

    def imprime(self, str = ''):
            self.value.imprime()

            print (str +"variable ",self.var)
            if not self.var == 0:
                print(str +"hijo 1")
                self.hijos[0].imprime(str  + '   ')
                print(str +"hijo 2")
                self.hijos[1].imprime(str  + '   ')

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
        
        neg = set(map(lambda x:-x,self.value.unit))
        cl.difference_update(neg)
        if not cl:
            self.anula()
        if len(cl)==1:
            v = cl.pop()
            self.value.insertar({v})
            self.hijos[0].simplificaunit(v)
            self.hijos[1].simplificaunit(v)
            self.normaliza()
        else:

            v = self.var
            if v in cl:
                cl.discard(v)
                self.hijos[0].insertaclau(cl)
            elif -v in cl:
                cl.discard(-v)
                self.hijos[1].insertaclau(cl)
            else:
                self.hijos[0].insertaclau(cl.copy())
                self.hijos[1].insertaclau(cl)

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
                self.value.hijos[0].combina(self.value)
                self = self.hijos[0]
            else:
                self.hijos[0].simplificaunit(v)
                self.hijos[1].simplificaunit(v)


    def simplificaunits(self,s):
        # print("simplifica units " , s)

        self.value.simplificaunits(s)
        if self.value.contradict:
            self.asignaval(self.value)
            return
        if not self.var == 0:
            if self.var in s:
                self.hijos[1].simplificaunits(s)
                self.hijos[1].value.combina(self.value)
                self.value = self.hijos[1].value
                self.var = self.hijos[1].var
                self.hijos = self.hijos[1].hijos
            elif -self.var in s:
                self.hijos[0].simplificaunits(s)
                self.hijos[0].value.combina(self.value)
                self.value = self.hijos[0].value
                self.var = self.hijos[0].var
                self.hijos = self.hijos[0].hijos
            else:
                self.hijos[0].simplificaunits(s)
                self.hijos[1].simplificaunits(s)

                if self.hijos[0].value.contradict or self.hijos[1].value.contradict:
                    self.normaliza()




   

    def tosimple(self):
        res = simpleClausulas()
        res.combina(self.value.copia())
        if not self.var == 0:
            res1 = self.hijos[0].tosimple()
            res2 = self.hijos[1].tosimple()
            res1.advalue(self.var)
            res2.advalue(-self.var)
            res.combina(res1)
            res.combina(res2)
        return res

    def checkrep(self, vars = set()):
        if self.value.listavar.intersection(vars):
            print( "Intersecio ", self.value.listavar.intersection(vars))
            self.imprime()
            print (vars)
            return True
        if self.var == 0:
            return False
        elif self.var in vars:
            print ("var ",self.var)
            return True
        else:

            varn = vars.union({self.var}).union(set(map(lambda x : abs(x), self.value.unit)))
            return self.hijos[0].checkrep(varn) or self.hijos[1].checkrep(varn)

    def checkunit(self):
        for x in self.value.unit:
            if abs(x) not in self.value.listavar:
                print("problema de unidades ",x , self.value.listavar)
                return True
        if self.var == 0:
            return False
        return self.hijos[0].checkunit() or self.hijos[1].checkunit()


    def normaliza(self,N=100):
        # if self.checkunit():
        #     print("problema antes de normalizar")
        if self.var == 0:
            if len(self.value.listaclaus) > N:
                x = self.value.calculalistatotal()
                var = calculavar(x)
                (l0,l1,unit) = split(x,var)

                ug = simpleClausulas()
                for z in unit:
                    ug.insertar({z})
                for z in self.value.unit:
                    ug.insertar({z})

                h0 =computefromSimple(l0,N)
                h1 = computefromSimple(l1,N)

                self.asignavarhijosv(var,h0,h1,ug)
                # if self.checkunit():
                #     print("problema despues de normalizar con var 0")
                #     ug.imprime()
                #     h0.imprime()
                #     h1.imprime()
        else:
            self.hijos[0].normaliza(N)
            self.hijos[1].normaliza(N)
            if self.checkunit():
                    print("problema despues de normalizar los hijos")
            v = self.var
            if self.hijos[0].value.contradict:
                self.value.insertar({v})
                self.hijos[1].value.combina(self.value)
                self.value = self.hijos[1].value
                self.var = self.hijos[1].var

                self.hijos = self.hijos[1].hijos

                # if self.checkunit():
                #     print("problema despues de contradiccion en hijos 0")

            elif self.hijos[1].value.contradict:
                self.value.insertar({-v})
                self.hijos[0].value.combina(self.value)
                self.value = self.hijos[0].value
                self.var = self.hijos[0].var

                self.hijos = self.hijos[0].hijos
                # if self.checkunit():
                #     print("problema despues de contradiccion en hijos 1")

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
                # if self.checkunit():
                #     print("problema despues de reunificar")



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

    def combinaborra(self,t,N,conf=set()):
      
        if self.var == 0:
            if not self.value.nulo():
                res =  t.combinaborrasimple(self.value,N,conf)
                return res
            else:
                res = arboldoble()
                return res
        else:
            res = arboldoble()
            v = self.var
            conf.add(v)
            h0 = self.hijos[0].combinaborra(t,N,conf)
            conf.discard(v)
           

            conf.add(-v)
            h1 = self.hijos[1].combinaborra(t,N,conf)
            conf.discard(-v)
            

            h = simpleClausulas()
            res.asignavarhijosv(v,h0,h1,h)

            

            if not self.value.nulo():
                addi = t.combinaborrasimple(self.value,N,conf)
                res.inserta(addi,N, norma= False)
            

            return res

    def combinaborrasimple(self,simple,N,conf):
        v = self.var
        if v== 0:
            s2 = self.value.selconf(conf)
            sc = simple.combinaborra(s2)
            res = arboldoble()
            res.asignaval(sc)
        else:
            if v in conf:
                res = self.hijos[0].combinaborrasimple(simple,N,conf)
            elif -v in conf:
                res = self.hijos[1].combinaborrasimple(simple,N,conf)
            else:
                s0 = simple.sel(v)
                h0 = self.hijos[0].combinaborrasimple(s0,N,conf)
                s1 = simple.sel(-v)
                h1 = self.hijos[1].combinaborrasimple(s1,N,conf)
                t = simpleClausulas()
                res = arboldoble()
                res.asignavarhijosv(v,h0,h1,t)

            s2  = self.value.selconf(conf)
         
            if not s2.nulo():
                    sc = simple.combinaborra(s2)

                    res2= arboldoble()
                    res2.asignaval(sc)
        

                    res.inserta(res2,N,norma = False)
        return res

    
   
    def insertaunits(self,sunits):
        # print("inserta ", sunits)
        self.simplificaunits(sunits)
        if not self.value.contradict:
            self.value.unit.update(sunits)
            pos = set(map(lambda x: abs(x), sunits))
            self.value.listavar.update(pos)




    def insertasimple(self,simple,N,conf=set(), norma = True):

        # if self.checkrep():
        #     print("repeticion antes")
        #     time.sleep(40)

        conf2 = conf.copy()
        if self.value.contradict:
            return
        if simple.contradict:
                    self.insertaclau(conf2)
                    return
    
        if self.value.unit:
            simple.simplificaunits(self.value.unit)
            
            if conf2.intersection(self.value.unit):
                return
            else:
                neg= set(map(lambda x: -x, self.value.unit))
                conf2 = conf2-neg
            if simple.contradict:
                    self.insertaclau(conf2)
                    return

            
            


       
        

        if self.var==0:


            simple.adconfig(conf2)
            self.value.combina(simple)
            if norma:
                self.normaliza(N)
            if self.checkrep():
                print ("repeticion despues de inserta simple  con self.var ) = 0")

        else:
            if not conf2:
                while  simple.unit:
                    # if 97 in simple.unit:
                    #     print("posible causa")
                    self.simplificaunits(simple.unit)
                    self.value.unit.update(simple.unit)
                    self.value.listavar.update( set(map(abs,simple.unit)))
                    simple.unit = set()
                    if self.value.unit:
                        simple.simplificaunits(self.value.unit)
                        if simple.contradict:
                            self.insertaclau(conf2)
                            return

                
                if self.var==0:
                    self.value.combina(simple)
                    if norma:
                        self.normaliza(N)
                    if self.checkrep():
                        print ("repeticion despues de inserta simple  con self.var ) = 0")
                        time.sleep(4)
                    return 
                


            v = self.var

            
            if v in conf2:


                conf2.discard(v)
                self.hijos[0].insertasimple(simple,N,conf2, norma)
                conf2.add(v)
                # if self.checkrep():
                #     print ("repeticion despues de insertar en hijo0 con v en conf" , conf2, v)
                #     self.hijos[0].imprime()
                #     simple.imprime()
                #     time.sleep(40)


            elif -v in conf2:
                conf2.discard(-v)
                self.hijos[1].insertasimple(simple,N,conf2, norma)
                conf2.add(-v)
                # if self.checkrep():
                #     print ("repeticion despues de insertar en hijo1 con -v en conf", conf2)
                #     time.sleep(40)

            else:

                (l0,l1,l2) = simple.splitborra(v)


                # print(" v", v , "hijos ", self.hijos)
                self.hijos[0].insertasimple(l0,N,conf2, norma)
                # if self.checkrep():
                #     print ("repeticion despues de insertar en hijo0 sin v in conf", v, conf2)
                #     self.imprime()
                #     l0.imprime()
                #     l1.imprime()
                #     l2.imprime()
                #     simple.imprime()
                #     time.sleep(40)

                self.hijos[1].insertasimple(l1,N,conf2, norma)
                if self.checkrep():
                    print ("repeticion despues de insertar en hijo1 sin v in conf", v, conf2)
                    self.imprime()

                    print("l1 "     )                    
                    l1.imprime()
                    time.sleep(40)

                self.hijos[0].insertasimple(l2.copia(),N,conf2, norma)
                # if self.checkrep():
                #     print ("repeticion despues de insertar en hijo0 parte sin v", v, conf2)
                #     simple.imprime()
                #     l0.imprime()
                #     l1.imprime()
                #     l2.imprime()
                #     self.imprime()
                #     time.sleep(40)

                self.hijos[1].insertasimple(l2,N,conf2, norma)
                # if self.checkrep():
                #     print ("repeticion despues de insertar en hijo1 parte sin v",v, conf2 )
                #     l0.imprime()
                #     l1.imprime()
                #     l2.imprime()
                #     simple.imprime()
                #     time.sleep(40)


    def inserta(self,t,N,conf= set(), norma = True):
        # if self.checkrep():
        #     print("repeticion antes de insertar ")
        #     time.sleep(30)
        # if t.checkrep():
        #     print("repeticion antes de insertar en t")
        #     t.imprime()
        #     time.sleep(30)
        # if t.checkunit():
        #     print("problema en lo insertado ")
        #     print(conf)
        #     t.imprime()
        #     time.sleep(30)



        if t.var == 0:

            if not t.value.nulo():
                # r = t.value.copia()
                # for y in t.value.unit:
                #     if not abs(y) in t.value.listavar:
                #         print ("problema de variables " )
                #         t.value.imprime()
                #         time.sleep(49)
                self.insertasimple(t.value,N,conf, norma)
            # if self.checkrep():
            #     print("repeticion despues de inserta simple de insertar ", conf)
            #     self.imprime()

            #     time.sleep(30)
        else:
            if not t.value.nulo():
                self.insertasimple(t.value,N,conf,norma)
            v = t.var
            conf.add(v)
            self.inserta(t.hijos[0],N,conf,norma)
            # if self.checkrep():
            #     print("repeticion despues de inserta el primer hijo de t ")
            #     time.sleep(30)
            conf.discard(v)
            conf.add(-v)
            self.inserta(t.hijos[1],N,conf,norma)
            # if self.checkrep():
            #     print("repeticion despues de inserta el segundo hijo de t ")
            #     time.sleep(30)
            conf.discard(-v)
            
            # if self.checkrep():
            #     print("repeticion despues de segundo inserta simple ", conf)
            #     print("t value")
            #     t.value.imprime()
            #     self.imprime()
            #     time.sleep(30)










