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
            print(str + "valor clausulas" , self.value.listaclaus)
            print(str +"valor unit" , self.value.unit)

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
        if len(cl)==1:
            v = cl.pop()
            self.value.insertar({v})
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
        if self.checkunit():
            print("problema antes de normalizar")
        if self.var == 0:
            if len(self.value.listaclaus) > N:
                x = self.value.listaclaus
                var = calculavar(x)
                (l0,l1,unit) = split(x,var)

                ug = simpleClausulas()
                for z in unit:
                    ug.insertar({z})
                for z in self.value.unit:
                    ug.insertar({z})

                h0 = computefromSimple(l0,N)
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
            if v==98:
                print(" En split borra arbol t2")
                t2.imprime()
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
        # if self.checkrep():
        #     print ("repeticion self")
        #     time.sleep(50)
        # if t.checkrep():
        #     print ("repeticion t")
        #     print (conf)
        #     t.imprime()
        #     time.sleep(50)
        if self.var == 0:
            if not self.value.nulo():
                res =  t.combinaborrasimple(self.value,N,conf)
                # if res.checkrep():
                #     print("problema en combina borra res 1",self.var, conf)
                #     time.sleep(50)
                #     res.imprime()
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
            # if h0.checkrep():
            #     print("problema en combina borra h0",v, conf)
            #     h0.imprime()
            #     time.sleep(50)

            conf.add(-v)
            h1 = self.hijos[1].combinaborra(t,N,conf)
            conf.discard(-v)
            # if h1.checkrep():
            #     print("problema en combina borra h1",v, conf)
            #     h1.imprime()
            #     time.sleep(50)

            h = simpleClausulas()
            res.asignavarhijosv(v,h0,h1,h)

            # if res.checkrep():
            #     print("problema en combina borra res",v, conf)
            #     res.imprime()
            #     time.sleep(50)

            if not self.value.nulo():
                addi = t.combinaborrasimple(self.value,N,conf)
                # if addi.checkrep():
                #     print("problema en addi")
                #     addi.imprime()
                #     time.sleep(50)

                res.inserta(addi,N, norma= False)
                # if res.checkrep():
                #     print("problema despues de insertar addi",v, conf)
                #     print("addi")
                #     addi.imprime()
                #     print("res")
                #     res.imprime()
                #     time.sleep(50)

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
            # if res.checkrep():
            #     print("problema en combina borra res",v, conf)
            #     res.imprime()
            if not s2.nulo():
                    sc = simple.combinaborra(s2)

                    res2= arboldoble()
                    res2.asignaval(sc)
                    # if res2.checkrep():
                    #     print("poblema en res2")
                    #     s2.imprime()

                    res.inserta(res2,N,norma = False)
        return res

    def combinaborra2(self,t,N,conf = set()):
        # print("entro combina")
            # simple.imprime()
        # print(conf)
            # self.imprime()
        if  t.var == 0:
            # print("entro en combinaborra simple desde combina borra")
            return self.combinaborrasimple(t.value,N,conf)
            # print("salgo de combinaborra ")
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


    def combinaborrasimple2(self,simple,N,conf):
            # print("entro combinasimple" , self.var)
            # simple.imprime()
            print(conf)
            if simple.nulo():
                res = arboldoble()
                return res
            # self.imprime()
            if self.var == 0:

                if not conf:
                    prod = self.value.combinaborra(simple)
                    res = arboldoble()
                    res.asignaval(prod)
                    # print("empiezo a normalizar")
                    res.normaliza(N)
                    # print("termino de normalizar")
                    # res.imprime()
                    return res
                else:
                    prod = self.value.combinaborrac(simple,conf)
                    res = arboldoble()
                    res.asignaval(prod)
                    # print("empiezo a normalizar")

                    res.normaliza(N)
                    # print("termino de normalizar")

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
                # print("empiezo a normalizar")

                res1.normaliza(N)
                # print("termino de normalizar")

                val = simpleClausulas()
                # print("res1")
                # res1.imprime()

                if v in conf:
                    # print("v in conf")
                    conf.discard(v)
                    r0 = self.hijos[0].combinaborrasimple(simple,N,conf)
                    conf.add(v)
                    r1 = arboldoble()


                elif -v in conf:
                    # print("v in conf")
                    conf.discard(-v)
                    r1 = self.hijos[1].combinaborrasimple(simple,N,conf)
                    conf.add(-v)
                    r0 = arboldoble()

                else:
                    # print ("nada de lso dos")
                    r0 = self.hijos[0].combinaborrasimple(simple.sel(v),N,conf)
                    r1 = self.hijos[1].combinaborrasimple(simple.sel(-v),N,conf)


                res.asignavarhijosv(v,r0,r1,val)
                # if (v==226):
                #     self.imprime()
                #     r0.imprime()
                #     r1.imprime()
                #     res.imprime()
                # print("res ")
                # res.imprime()
                # print("inserto en combina borra simple")
                # res1.imprime()
                res.inserta(res1,N)
                # print("termino")
                # res.imprime()
                # print("comienzo a normalizar")
                res.normaliza(N)
                # print ("termino")
                return res




    def insertaunits(self,sunits):
        # print("inserta ", sunits)
        self.simplificaunits(sunits)
        if not self.value.contradict:
            self.value.unit.update(sunits)
            pos = set(map(lambda x: abs(x), sunits))
            self.value.listavar.update(pos)




    def insertasimple(self,simple,N,conf=set(), norma = True):

        if self.value.contradict:
            return
        # if simple.checkvars():
        #     print("problema en inserta simle con simple ")
        # if self.checkrep():
        #     print ("repeticion antes de inserta simple ")
        #     time.sleep(40)

        # poscon = set(map(lambda x: abs(x), conf))

        # if poscon.intersection(simple.listavar):
        #     print("problema " , conf)
        #     simple.imprime()
        #     time.sleep(40)
        if self.value.unit:
            if conf.intersection(self.value.unit):
                return
            else:
                neg= set(map(lambda x: -x, self.value.unit))
                conf2 = conf-neg
            simple.simplificaunits(self.value.unit)

        else:
            conf2 = conf
        if simple.contradict:
            if not conf2:
                self.value.insertar(set())
                self.var = 0
                self.hijos = [None,None]
                return
            elif len(conf2)==1:

                self.insertaunits(conf2)
                # if self.checkrep():
                #     print ("repeticion despues de insertaunits conf2 " , conf2)
                #     self.imprime()
                #     print(" simple ", conf2)
                #     simple.imprime()
                #     time.sleep(40)
                return

        elif not conf2 and simple.unit:
                # print ("entro en poda")
                self.insertaunits(simple.unit)
                if self.value.contradict:
                    return
                simple.unit = set()
                self.insertasimple(simple,N,conf2,norma)
                return
        # if self.checkrep():
        #         print ("repeticion despues de inserta simple  despues de insertar unitarias")
        #         self.imprime()
        #         print(" simple ", conf2)
        #         time.sleep(40)

        if self.var==0:


            simple.adconfig(conf2)
            for v in simple.unit:
                self.value.insertar({v})
            for cl in simple.listaclaus:
                self.value.insertar(cl)
            if norma:
                self.normaliza(N)
            # if self.checkrep():
            #     print ("repeticion despues de inserta simple  con self.var ) = 0")

        else:

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
                # if self.checkrep():
                #     print ("repeticion despues de insertar en hijo1 sin v in conf")
                #     self.imprime()

                #     l0.imprime()
                #     l1.imprime()
                #     l2.imprime()
                #     simple.imprime()
                #     time.sleep(40)

                self.hijos[0].insertasimple(l2.copia(),N,conf2, norma)
                # if self.checkrep():
                #     print ("repeticion despues de insertar en hijo0 parte sin v", v, conf)
                #     l2.imprime()
                #     l0.imprime()
                #     l1.imprime()
                #     l2.imprime()
                #     simple.imprime()
                #     time.sleep(40)

                self.hijos[1].insertasimple(l2,N,conf2, norma)
                # if self.checkrep():
                #     print ("repeticion despues de insertar en hijo1 parte sin v",v, conf )
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
                r = t.value.copia()
                for y in t.value.unit:
                    if not abs(y) in t.value.listavar:
                        print ("problema de variables " )
                        t.value.imprime()
                        time.sleep(49)
                self.insertasimple(t.value,N,conf, norma)
            # if self.checkrep():
            #     print("repeticion despues de inserta simple de insertar ", conf)
            #     self.imprime()

            #     time.sleep(30)
        else:
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
            if not t.value.nulo():
                self.insertasimple(t.value,N,conf,norma)
            # if self.checkrep():
            #     print("repeticion despues de segundo inserta simple ", conf)
            #     print("t value")
            #     t.value.imprime()
            #     self.imprime()
            #     time.sleep(30)










