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
from utils import *





class problemaTrianFactor:
    def __init__(self,info,M=25):
         self.M = M
         self.inicial = info
         self.pinicial = PotencialTabla()
         self.rela = varpot()
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

    def mejoradespues(self):
        for p in self.pinicial.listap:
            old = np.sum(p.tabla)
            pos = min(map(lambda h: self.posvar[h],p.listavar))
            pot = self.lqueue[pos]
            potn = pot.marginalizaset(pot.getvars() - set(p.listavar), ver=False, inplace=False)
            tablan = potn.atabla()
            p.combina(tablan, inplace=True)    
            nu =  np.sum(p.tabla)
            print(nu,old)
            if nu<old:
                print("mejoro", old,nu)
        
    def borrai(self):
        

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
                # print (j)
                dif = self.clusters[i]-self.clusters[j]
                # print(dif)
                # print("entro en copia")
                # potn = self.lqueue[i].copia()
                # print("salgo de copia") 

                
                potn = pot.marginalizaset(dif,ver = False,inplace=False)
                self.lqueue[j].combina(potn)

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

        return 


        

    def borradin(self):
    
        if self.rela.contradict:
                print("contradictorio")
                self.anula()
                return

        (e,orden,nuevas,antiguas)= self.rela.marginalizaset(self.pinicial.getvars())
        self.orden = orden
        i=0
        for x in antiguas:
            print(i, x)
            i+=1
            y = varpot()
            y.createfromlista(x)
            self.lqueue.append(y)

        (self.clusters,self.posvar,self.child,self.parent) = triangulaconorden(self.pinicial,orden) 


        
        



        return e
        
           

    def borra12(self,x,l,rela, M= 20):
            print("total ", len(l))
            i = x[0]
            while l:

                p= l.pop()
                sp = p.extraesimple()
                if not sp.trivial():

                    if len(sp.listavar) == 1:
                        var = sp.listavar[0]
                        areducir = rela.get(var)
                        print(" i " , i , "var ", var, "reduccion unitaria ")
                        i +=1
                        sleep(1)
                        rela.borrarv(var)
                        for q in areducir:
                            
                            if q in l:
                                l.remove(q)
                            r = q.combina(sp)
                            r.borra([var],inplace=True)
                            if r.contradict():
                                rela.anula()
                                print("contradiction ")
                                return
                            elif not r.trivial():
                                l.append(r)
                                rela.insertar(r)


                    elif len(sp.listavar) == 2:
                        v1 = sp.listavar[0]
                        v2 = sp.listavar[1]
                        
                        det1 = sp.checkdetermi(v2)
                        if not det1:
                            det2 = sp.checkdetermi(v1)
                        if not det1 and not det2:
                            continue
                        if not det1 and det2:
                            v1,v2 = v2,v1
                        var = v2
                        print(" i " , i, "var ", var, "doble ")
                        sleep(1)
                        i+=1
                        areducir = rela.get(var)
                        rela.borrarv(var)
                        for q in areducir:
                            if q in l:
                                l.remove(q)
                            r = q.combina(sp)
                            r.borra([var],inplace=True)
                            if r.contradict():
                                rela.anula()
                                print("contradiction ")
                                return
                            elif not r.trivial():
                                l.append(r)
                                rela.insertar(r)
                else:
                    print("extraigo trivial ")

            x[0] = i
        


                        
            
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