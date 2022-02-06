# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 20:13:39 2021

@author: efrai
"""

import time

from SimpleClausulas import *
from tablaClausulas import *
class problemaTrianFactor:
    def __init__(self,info,N=100):
         self.N = N
         self.inicial = info
         self.pinicial = PotencialTabla()
         self.orden = []
         self.clusters = []
         self.lpot = []
         self.lqueue  = []
         self.lqp = []
         self.lqn = []
         self.cortas = []
         self.posvar = dict()
         self.sol = set()
         self.borr = []
         self.maximal = []
         self.child = []
         self.parent = []

    def reinicia(self):
        for x in self.lpot:
                x = arboldoble()
        for y in self.lqueue:
                y = arboldoble()

        for v in self.inicial.unit:
                self.insertacolaclau2({v})
        # for x in self.inicial.two:
        #     for y in self.inicial.two[x]:
        #         self.insertacolaclau2({x,y})
        for cl in self.inicial.listaclaus:
                self.insertacolaclau2(cl)
        for pot in self.lqueue:
                pot.normaliza(self.N)      

    def reinicia2(self):
        for x in self.lpot:
                x = arboldoble()
        for y in self.lqueue:
                y = arboldoble()

        for v in self.inicial.unit:
                self.insertacolaclau3({v})
        # for x in self.inicial.two:
        #     for y in self.inicial.two[x]:
        #         self.insertacolaclau2({x,y})
        for cl in self.inicial.listaclaus:
                self.insertacolaclau3(cl)
        # for pot in self.lqueue:
        #         pot.normaliza(self.N)         

    def inicia0(self):

            for i in self.orden:
                x = PotencialTabla()
                self.lpot.append(x)
                y = PotencialTabla()
                self.lqueue.append(y)
            self.pinicial.computefromsimple(self.inicial)

            for x in self.pinicial.unit:
                self.insertaunit(x)

            for p in self.pinicial.listap:
                
                self.insertacolapot(p)
    
            
           
    def insertaunit(self,x):
        xp = abs(x)
        for pos in range(len(self.clusters)):
            if xp in self.clusters[pos]:
                pot = self.lqueue[pos]  
                pot.insertaunit(x)



    

    def insertacolapot(self,p):
        


        
            vcl = p.listavar
            pos = min(map(lambda h: self.posvar[h], vcl))
            
            pot = self.lqueue[pos]
            pot.inserta(p)


    def introducecorclau(self,cl):
        vars = set(map(lambda x:abs(x),cl))
        for pos in range(len(self.clusters)):
            if vars <= self.clusters[pos]:
                simple = self.cortas[pos]
                simple.insertar(cl)


    def introducecortas(self,simple):
        for x in simple.unit:
            self.introducecorclau({x})

        for x in simple.two:
            for y in simple.two[x]:
                self.introducecorclau({x,y})

        for cl in simple.listaclaus:
            self.introducecorclau(cl)

    def borraapro(self,M=10,T=4):
        print(len(self.orden))
        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            
            if pot.value.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            print("entro en normaliza")
            # if pot.checkrep():
            #     print("proeblma de repeticion antes de normalizar")
            pot.normaliza(self.N) 
            if pot.value.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion después de normalizar ")
                break
            print("entro en split")
            # if pot.checkrep():
            #     print("proeblma de repeticion")
            (t0,t1,t2) = pot.splitborra(var)
            
            

                       

            print("ntro en combinaborra")
            res1 = t0.combinaborra(t1,self.N)

            c1 = res1.extraecortas(M)
            # c2 = t2.extraecortas(M)

            lista = c1.extraecortas(T).calculalistatotal()
            # lista2 = c2.extraecortas(T).calculalistatotal()

            for cl in lista:
                print(cl)
                self.inicial.insertar(cl)


            # for cl in lista2:
            #     print("lista 2",cl)
            #     self.inicial.insertar(cl)

            print("inserto t2")
            self.insertacola(t2,i)
            
            ad = arboldoble()
            ad.asignaval(c1)

            if res1.value.contradict:
                print("contradiccion en resultado")
            print("Ahora inserto en la cola")
            self.insertacola(ad,i)


    def borraaproi(self,M=4,T=3):
        print(len(self.orden))
        for i in reversed(range(len(self.orden))):
            if self.inicial.contradict:
                break
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            
            if pot.value.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            print("entro en normaliza")
            # if pot.checkrep():
            #     print("proeblma de repeticion antes de normalizar")
            pot.normaliza(self.N) 
            if pot.value.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion después de normalizar ")
                break
            print("entro en split")
            # if pot.checkrep():
            #     print("proeblma de repeticion")
            
            for j in self.child[i]:
                dif = self.clusters[i]-self.clusters[j]
                pot = self.lqueue[i]

                for var in dif:
                    (t0,t1,t2) = pot.splitborra(var)
            
            

                       

                    print("ntro en combinaborra")
                    res1 = t0.combinaborra(t1,self.N)

                    c1 = res1.extraecortas(M)

                    lista = c1.extraecortas(T).calculalistatotal()

                    for cl in lista:
                        print(cl)
                        self.inicial.insertar(cl)

                    res1.inserta(t2,self.N)
                    pot = arboldoble()
                    pot.asignaval(c1)

                self.lqueue[j].inserta(pot,self.N)

        

                

    def borra(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            if i==213:
                print("posible problema")
            # pot.imprime()
            
            if pot.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            
            
            potn = pot.marginaliza(var)
            
            # potn.imprime()
            if self.parent[i]==-1:
                

                if potn.contradict:
                    print("contradiccion en resultado")
                print("Ahora inserto en la cola")
                


            else:
                self.inserta(potn)


    def inserta(self,pot):
        for x in pot.unit:
                self.insertaunit(x)

        for p in pot.listap:
                self.insertacolapot(p)
       



    def borra2(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
                t0 = arboldoble()
                t1 = arboldoble()
                self.lqp.append(t1)
                self.lqn.append(t0)
                c = simpleClausulas()
                self.cortas.append(c)
        for j in range(len(self.orden),0,-1):
            print("j= ", j)
            if self.inicial.contradict:
                    break
            for i in range(j,len(self.orden)):
            
                if self.inicial.contradict:
                    break
                var = self.orden[i]
                print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
                pot = self.lqueue[i]
                
                if pot.value.contradict:
                    self.inicial.contradict=True #ojo
                    print("contradiccion antes de normalizar ")
                    break
                print("entro en normaliza")
                # if pot.checkrep():
                #     print("proeblma de repeticion antes de normalizar")
                pot.normaliza(self.N) 
                if pot.value.contradict:
                    self.inicial.contradict=True #ojo
                    print("contradiccion después de normalizar ")
                    break
                print("entro en split")
                # if pot.checkrep():
                #     print("proeblma de repeticion")
                (t0,t1,t2) = pot.splitborra(var)
                
                r0 = self.lqn[i]
                r1 = self.lqp[i]

                
                print("ntro en combinaborra")
                res1 = t0.combinaborra(t1,self.N)
                res2 = t0.combinaborra(r1,self.N)
                res3 = t1.combinaborra(r0,self.N)

                r0.inserta(t0,self.N)
                r1.inserta(t1,self.N)

                c1 = res1.extraecortas()
                c2 = res2.extraecortas()
                c3 = res3.extraecortas()


                if not c1.nulo():
                    
                    self.introducecortas(c1)

                    c1.imprime()
                    time.sleep(3)
                
                if not c2.nulo():
                    self.introducecortas(c2)

                    c2.imprime()
                    time.sleep(3)

                if not c3.nulo():
                    self.introducecortas(c3)

                    c3.imprime()
                    time.sleep(3)



                print("inserto t2")
                self.insertacola(t2,i)
                res1.normaliza(self.N)

                if res1.value.contradict:
                    print("contradiccion en resultado")
                pot.void()
                print("Ahora inserto en la cola")
                self.insertacola(res1,i)
                self.insertacola(res2,i)
                self.insertacola(res3,i)


            


    def findsol(self):
        sol = set()
        for i in reversed(range(len(self.orden))):
            pot = self.lqueue[i]
            

            r = pot.reduceycombina(sol)
            
            
            var = self.orden[i]
            print(var)
            
            if r.contradict:
                print("contradiccion buscando solucion" , sol )
                break

            if var in r.unit:
                sol.add(var)
                print(var)
            elif -var in r.unit:
                sol.add(-var)
                print(-var)
            elif not r.listap:
                sol.add(var)
                print(var)
            elif not r.listap[0].tabla[0] and  not r.listap[0].tabla[1]:
                print("contradiccion buscando solucion" , sol )
                break
            elif  r.listap[0].tabla[0]:
                sol.add(-var)
                print(-var)
            else:
               sol.add(var)
               print(var) 

            
            
        self.sol = sol
        return sol
    
    def randomsol(self,T=40000):
        sol = []
        i = len(self.orden)-1
        k = 0
        while i >0 and k<T:
            k+=1
            # print(i,k,sol)
            pot = self.lqueue[i].copia()
            
            pot.simplificaunits(sol)
            pot.normaliza(N=1000)

            pots = pot.tosimple()
            
            var = self.orden[i]
            
            if pots.contradict:
                pot = self.lqueue[i].copia()
                cl = pot.extraeclaus(sol,var)
                # print(cl)
                vcl = map(abs,cl)
               
                j = min(map(lambda h: self.posvar[h], vcl))
                self.lqueue[j].insertaclau(cl)
                t = j-i

                i = j

                del sol[-t:]

                if len(cl)<=3:
                     print("buena", cl)
                     self.inicial.insertar(cl)
            else:


                i=i-1
                pots.simplificaunit(var)
                if pots.contradict:
                    sol.append(-var)
                else:
                    sol.append(var)
            
            
        if i<0:
            self.sol = sol
        print(sol)
        return sol

    def compruebaSol(self):
        aux = 0
        for clau in self.inicial.listaclausOriginal:
            aux = aux + 1
            if len(clau.intersection(self.sol))==0:
                print("Error en cláusula: ", clau)
                return False
        print("Cumple solución satisfactoriamente, Número de cláusulas validadas: ", aux)
        return True
    
    def insertacola(self,t,i,conf=set()):
        if not t.value.nulo():
                if t.value.contradict and not conf:
                    self.problemacontradict()
                else:
                    j = i+1
                    vars = set(map(lambda x: abs(x),conf.union(t.value.listavar)) )
                    # j = min(map(lambda h: self.posvar[h],vars))
                    while not vars <= self.clusters[j]:
                        j += 1
                        if j == len(self.clusters):
                            print(vars)
                    
                    pot = self.lqueue[j]
                    # if pot.checkrep():
                    #     print("problema de repecion antes de insertar")
                    #     time.sleep(30)
                    if pot.value.contradict:
                        print("contradiccion antes")

                    
                    pot.insertasimple(t.value,self.N,conf) 
                    # if pot.checkrep():
                    #     print("problema de repecion despyes de insertar",conf)
                    #     time.sleep(30)

                    pot.normaliza(self.N) 
        if not t.var ==0:
            v = t.var
            conf.add(v)
            self.insertacola(t.hijos[0],i,conf)
            conf.discard(v)
            conf.add(-v)
            self.insertacola(t.hijos[1],i,conf)
            conf.discard(-v)

    def insertacolai(self,t,i,conf=set()):
        if not t.value.nulo():
                if t.value.contradict and not conf:
                    self.problemacontradict()
                else:
                    j = i-1
                    vars = set(map(lambda x: abs(x),conf.union(t.value.listavar)) )
                    # j = min(map(lambda h: self.posvar[h],vars))
                    while not vars <= self.clusters[self.maximal[j]]:
                        j -= 1
                        if j == -1:
                            print(vars)
                    
                    pot = self.lqueue[self.maximal[j]]
                    # if pot.checkrep():
                    #     print("problema de repecion antes de insertar")
                    #     time.sleep(30)
                    if pot.value.contradict:
                        print("contradiccion antes")

                    
                    pot.insertasimple(t.value,self.N,conf) 
                    # if pot.checkrep():
                    #     print("problema de repecion despyes de insertar",conf)
                    #     time.sleep(30)

                    pot.normaliza(self.N) 
        if not t.var ==0:
            v = t.var
            conf.add(v)
            self.insertacola(t.hijos[0],i,conf)
            conf.discard(v)
            conf.add(-v)
            self.insertacola(t.hijos[1],i,conf)
            conf.discard(-v)
            
    def problemacontradict(self):
        print("contradiccion")
        self.inicial.solved = True
        self.inicial.contradict = True
        
    def anula(self):
        self.inicial.solved = True
        self.inicial.contradict = True
        for pot in self.lpot:
            pot.anula()
        for por in self.lqueue:
            pot.anula()