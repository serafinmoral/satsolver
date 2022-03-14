# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 20:13:39 2021

@author: efrai
"""

from operator import index
import time

from numpy import False_
from vartablas import *

from SimpleClausulas import *
from arboltabla import calculadesdePotencial
from tablaClausulas import *


def ordenaycombinaincluidas(lista,rela):
    
    lista.sort(key = lambda x : - len(x.listavar) )

    
    i=0
    while i <len(lista)-1:
        j = i+1
        while j < len(lista):
            if set(lista[j].listavar) <= set(lista[i].listavar):
                print("incluidas " )
                p = lista[i]
                q = lista[j]
                print(p.listavar)
                print(q.listavar)
                rela.borrarpot(p)
                rela.borrarpot(q)
                p.combina(q,inplace= True)
                rela.insertar(p)
                lista.remove(q)
            else:
                j+=1
        
        i+=1
    lista.reverse()




class problemaTrianFactor:
    def __init__(self,info,M=25):
         self.M = M
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
         self.contradict = False

         self.varpar = []
         self.potpar = []



    
        

    def inicia0(self):

            
            self.pinicial.computefromsimple(self.inicial)

    def inicia1(self):

        print(self.orden)
        self.lqueue = []
        
        for i in self.orden:
                
                y = PotencialTabla()
                self.lqueue.append(y)
        y = PotencialTabla()
        self.lqueue.append(y)

        self.inserta(self.pinicial)    



    def previo(self, Q = 2):
        for x in self.pinicial.unit:
            self.varpar.append(abs(x))
            pot = PotencialTabla()
            pot.unit.add(x)
            self.potpar.append(pot)
        self.pinicial.unit = set()


        vars = self.pinicial.getvars()

        

        count = dict()
        pots = dict()

        for v in vars:
            count[v] = 0
        
        for p in self.pinicial.listap:
            for v in p.listavar:
                count[v] +=1
                pots[v] = p
        for v in vars:
            print ("var ", v, "num ", count[v])
            if count[v] == 1:
                    pot = pots[v]
                    pos = self.pinicial.listap.index(pot)
                    print("var ", v ,"encontrada una vez")

                
                    sleep(0.2)
                    print("borrando esta variable")
                    self.varpar.append(v)
                    self.potpar.append(pot)

                    r = p.borra([v],inplace = False)
                    self.pinicial.listap[pos] = r




        sleep(0.1)
        total = 0
        for K in range(2,Q+1):
            varb = []
            potb = []
        
            total = 1
            while total >0:
                total = 0
                i=0
                while i < len(self.pinicial.listap):
                    p = self.pinicial.listap[i]
                    if len(p.listavar) == K:
                        for v in p.listavar:
                                deter = p.checkdetermi(v)
                                if deter:
                                    varb.append(v)
                                    potb.append(p)
                                    # print("variable ", v, " determinada ", p.listavar)
                                    # print(p.tabla)
                                    self.borrad(v,p)
                                    total += 1
                                    break
                    i+= 1
                print(total)

    def borrad(self,v,p):
        bor = []
        tota = set()
        for i in range(len(self.pinicial.listap)):
            q = self.pinicial.listap[i]
            if v in q.listavar:
                # print("var pot", q.listavar)
                if q == p:
                    h = q.borra([v],inplace = False)
                    if h.trivial():
                        bor.append(h)
                    
                else:
                    h = q.combina(p,inplace = False, des= False)
                    h.borra([v], inplace = True)
                    if h.trivial():
                        bor.append(h)
                        print("trivial 2")
                        sleep(1)
                self.pinicial.listap[i] = h
                
        for q in bor:
            self.pinicial.listap.remove(q)



    def anula(self):

        for i in range(len(self.orden)):
            self.lqueue[i].anula()
        self.contradict = True

           
    def insertaunit(self,x):
        xp = abs(x)
        nu = set()
        for pos in range(len(self.clusters)):
            if xp in self.clusters[pos]:
                pot = self.lqueue[pos]  
                pot.insertaunit(x)
    



    

    def insertacolapot(self,p):
        


        
            vcl = p.listavar
            if vcl:
                pos = min(map(lambda h: self.posvar[h], vcl))
            else:
                pos = len(self.orden)
            pot = self.lqueue[pos]
            pot.listap.append(p)
            

    def mejorainicial(self):
        res = []
        for p in self.pinicial.listap:
            old = np.sum(p.tabla)
            oldl = len(p.listavar)
            vcl = set(p.listavar)
            if vcl:
                pos = min(map(lambda h: self.posvar[h], vcl))
            else:
                pos = len(self.orden)

            pot = self.lqueue[pos]
            npot = pot.marginalizas( set(pot.getvars()) - vcl)

            for v in npot.unit:
                p.reduce([v],inplace=True)
            for q in npot.listap:
                p.combina(q, inplace=True)
            new = np.sum(p.tabla)
            if new < old:
                print("mejora ", old, new, len(p.listavar))
                res.append(p)
                # sleep(2)            
        return res

    def borraproi(self):
        
        for i in reversed(range(len(self.orden))):
            if self.inicial.contradict:
                break
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]

           
            if pot.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            
            for j in self.child[i]:
                print (j)
                dif = self.clusters[i]-self.clusters[j]
                
                potn = pot.marginalizapros(dif,self.M, inplace=False)
                
            
            

                  

                    

                    

                self.lqueue[j].insertaa(potn,self.M)

                

        
    def borrai(self):
        

        for i in reversed(range(len(self.orden))):
            if self.inicial.contradict:
                break
            # print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            
            if pot.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            
            for j in self.child[i]:
                # print (j)
                dif = self.clusters[i]-self.clusters[j]
                # print(dif)
                # print("entro en copia")
                # potn = self.lqueue[i].copia()
                # print("salgo de copia") 

                
                potn = pot.marginalizas(dif,inplace=False)
                
            
            

                       

                    

                    

                self.lqueue[j].insertap(potn)

    def pasaarbol(self):
        for i in range(len(self.lqueue)):
            print("arbol ", i)
            print("cluster ", self.clusters[i])

            p = self.lqueue[i]
            ap = calculadesdePotencial(p)
                       
            self.lqueue[i] = ap

    def combinaincluidos(self):
        for i in range(len(self.orden)):
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            pot.combinaincluidos()

    def calculanu(self):
        nu = set()
        for i in range(len(self.orden)):
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            for p in pot.listap:
                nu.update(p.calculaunit())

        return nu

    def limpia(self):
        for i in range(len(self.orden)):
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
            bor =  []
            for p in pot.listap:
                if p.trivial():
                    print("uno trivial", p.listavar)
                    bor.append(p)
                if p.contradict():
                    self.anula()
                    return
            for p in bor:
                pot.listap.remove(p)

        return nu


        

    def borradin(self):
    
        rela = varpot()
        rela.createfrompot(self.pinicial)
        t = len(self.pinicial.getvars())
        if self.inicial.contradict:
            self.anula()
            return
        i = 0
        while rela.tabla:
            var = rela.siguiente()
            print("i= ", i, "de " , t, "var = ", var)
            lista = rela.get(var)

            ordenaycombinaincluidas(lista,rela)

            
            rela.borrarv(var)

            
            pot = PotencialTabla()
            pot.listap = lista

            nuevas = pot.marginalizacond2(var,M=30)
        



            for p in nuevas:
                if p.contradict():
                    print("contradictorio ")
                    sleep(10)
                    break
                rela.insertar(p)


            ordenaycombinaincluidas(nuevas,rela)
            i+= 1
                        
            
    def borra(self):
        print(len(self.orden))

        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
       
            # pot.imprime()
            
            if pot.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            
            
            # potn = pot.marginaliza(var,self.posvar, L=23)

            potn = pot.marginaliza(var)
            print("fin marginaliza")

            pos = self.parent[i]

            poti = self.lqueue[pos]

            poti.inserta(potn)
            print("fin de combina")
            # potn.imprime()
            # if self.parent[i]==-1:
                

            #     if potn.contradict:
            #         print("contradiccion en resultado")
            #     print("Ahora inserto en la cola")
                


            # else:
            #     self.inserta(potn)

    def borrapro(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            pot = self.lqueue[i]
       
            # pot.imprime()

            
            
            if pot.contradict:
                self.inicial.contradict=True #ojo
                print("contradiccion antes de normalizar ")
                break
            
            
            potn = pot.marginalizapro(var,self.M)
            
            # potn.imprime()
            pos = self.parent[i]

            poti = self.lqueue[pos]

            

            
            poti.insertaa(potn,self.M)

            


    def inserta(self,pot):
        for x in pot.unit:
                self.insertaunit(x)

        for p in pot.listap:
                
                self.insertacolapot(p)
       



    


            


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