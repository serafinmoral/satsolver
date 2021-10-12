# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:28:21 2020

@author: Serafin
"""

import time

from arboldoblesinvar import *
from SimpleClausulas import *

def filtra(lista,nconfig,pconfig,i):
    result = []
    for cl in lista:
        if not cl.intersection(pconfig):
            if len(cl-nconfig)<=i:
                result.append(cl)
    return result

def compruebasolsimple(pot,sol):
    for v in pot.value.unit:
        if -v in sol:
            return False
    for cl in pot.value.listaclaus:
        if not cl.intersection(sol):
            return False
    return True

def filtrasplit(lista,nconfig,pconfig,i):
    result1 = []
    result2 = []
    for cl in lista:
            if len(cl-nconfig)<=i:
                result1.append(cl)
            else:
                result2.append(cl)
                
    return (result1,result2)


class problemaTrianArbol:
    def __init__(self,info,N=100):
         self.N = N
         self.inicial = info
         self.orden = []
         self.clusters = []
         self.lpot = []
         self.lqueue  = []
         self.lqp = []
         self.lqn = []
         self.posvar = dict()
         
         
    def inicia0(self):

            for i in self.orden:
                x = arboldoble()
                self.lpot.append(x)
                y = arboldoble()
                self.lqueue.append(y)
    

            for v in self.inicial.unit:
                self.insertacolaclau2({v})
            for cl in self.inicial.listaclaus:
                self.insertacolaclau2(cl)
     



            for pot in self.lqueue:
                pot.normaliza(self.N)
                
            



    def inicia2(self):
            cola = []
            for i in self.orden:
                x = arboldoble()
                self.lpot.append(x)
                y = arboldoble()
                self.lqueue.append(y)
                
            
            listaorden = []


            copia = self.inicial.copia()
            for i in reversed(range(len(self.orden))):
                var = self.orden[i]
                potsin = []
                if len(copia.indices.get(var,set())) < len(copia.indices.get(-var,set())):
                    value = -var
                else:
                    value = var
                lista = copia.indices.get(value,set()).copy()
                for cl in lista:
                    copia.eliminar(cl)
                    potsin.append(cl)
                print("var ", var, len(potsin))
                listaorden.append(potsin)                                
                
            print(len(listaorden))
            return listaorden
     
                
                

                    
    def selectval(self,i,var,config):
        return var
                    

            
    def insertacolaclau(self,cl):
        if not cl:
            self.anula()
        else:
            indices = map(lambda x:self.posvar[abs(x)],cl)
            pos = min (indices) 
            pot = self.lqueue[pos]
            pot.insertaclau(cl)

    def insertacolaclau2(self,cl):
        if not cl:
            self.anula()
        else:
            
            vars = set(map(lambda x:abs(x),cl))
            for pos in range(len(self.clusters)):
                if vars <= self.clusters[pos]:
                    break

            pot = self.lqueue[pos]
            pot.insertaclau(cl)

    def insertacola(self,t,i,conf=set()):
        if not t.value.nulo():
                if t.value.contradict and not conf:
                    # print("contradiccion c", conf)
                    # t.imprime()
                    
                    self.problemacontradict()
                else:
                    # indices = map(lambda x:self.posvar[abs(x)],conf.union(t.value.listavar))
                    # # print(set(indices))
                    # pos = min (indices) 
                    # print(pos,self.clusters[pos])
                    j = i+1
                    vars = set(map(lambda x: abs(x),conf.union(t.value.listavar)) )
                    while not vars <= self.clusters[j]:
                        
                        j += 1


                    pot = self.lqueue[j]
                    if pot.value.contradict:
                        print("contradiccion antes")
                    # print("inserto en ", pos)
                    # pot.imprime()

                    # if pot.checkunit():
                    #     print("problema unidades antes de insertar en colar")
                    #     time.sleep(50)

                    # if pot.checkrep():
                    #     print("repeticion antes de insertar en colar")
                    #     time.sleep(50)
                    
                   

                    # print("llamo inserta simple" , conf)
                    pot.insertasimple(t.value,self.N,conf) 

                   
                    # if pot.checkrep():
                    #     print("repeticion despues de insertar en colar ", conf)
                    #     t.value.imprime()
                    #     pot.imprime()

                    #     time.sleep(500)
                    # if pot.value.contradict:
                    #     print("contradiccion despues")
                    #     pot.value.imprime()
                    #     pot.imprime()

                    # if pot.checkunit():
                    #     print("problema unidades despues de insertar en colar")
                        
                    #     t.value.imprime()

                    #     pot.imprime()

                    #     time.sleep(50)
                    pot.normaliza(self.N) 
                      
                    # if pot.checkrep():
                    #     print("repeticion despues de normalizar en colar")
                    #     time.sleep(50)
                    # if pot.checkunit():
                    #     print("problema unidades despues de normalizar en colar")
                    #     time.sleep(50)


                    
                    # print("resultado")
                    # pot.imprime() 


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
                
#     def tinserta(self,cl,pos=-1):
# #    print(cl)
#         cola = []
#         if not cl:
#             self.inicial.solved = True
#             self.inicial.contradict = True
#         elif len(cl)==1:
#             val = set(cl).pop()
#             var = abs(val)        
#             pos = self.posvar[var]
#             pot = self.lpot[pos]
#             self.inicial.unit.add(val)
#             self.inicial = self.inicial.restringe(val)
#             cola = cola + self.insertapu(cl,pot,val)
# #            print(cola)
#             for i in range(pos):
            
#                 pot = self.lpot[i]
#                 if var in pot.listavar:
#                     cola = cola + self.podau(pot,val)
# #                    print(cola)
#                 pot = self.lqueue[i]
#                 if var in pot.listavar:
#                     cola = cola + self.podau(pot,val)
# #                    print(cola)
                    
#         elif len(cl)<=self.N1:
        
#             if (pos ==-1):
#                 indices = map(lambda x:self.posvar[abs(x)],cl)
#                 pos = min (indices)
#             pot = self.lpot[pos]
#             pot2 = self.lqueue[pos]
#             var = self.orden[pos]

#             pot.borraincluidas(cl)
#             pot2.borraincluidas(cl)
#             cola = pot.insertasatura(cl,var)
            
            
                
#         else:
#             if (pos ==-1):
#                 indices = map(lambda x:self.posvar[abs(x)],cl)
#                 pos = min (indices)
#             var = self.orden[pos]
#             pot = self.lpot[pos]
#             cola = pot.insertasatura(cl,var)
    
#         return cola
    
    def findsol(self):
        
        sol = set()
        for i in reversed(range(len(self.orden))):
            pos = self.lqp[i].copia()
            neg = self.lqn[i].copia()
            neg.simplificaunits(sol)
            pos.simplificaunits(sol)
            pos.normaliza()
            neg.normaliza()
            var = self.orden[i]
            print("i= ",i)
            if not pos.value.contradict:
                sol.add(var)
                print(var)
            elif not neg.value.contradict:
                sol.add(-var)
                print(-var)
            else:
                print("contradiccion buscando solucion" , sol )
                self.lqp[i].imprime()
                self.lqn[i].imprime()
                break
            
        return sol
        self.sol = sol
    def compruebaSol(self):
        aux = 0
        for clau in self.inicial.listaclausOriginal:
            aux = aux + 1
            if len(clau.intersection(self.sol))==0:
                print("Error en cláusula: ", clau)
                return False
        print("Cumple solución satisfactoriamente, Número de cláusulas validadas: ", aux)
        return True
    
    def borra(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
            
            pot = self.lqueue[i]
            if pot.value.contradict:
                print("contradiccion antes de normalizar ")
                break
            print("entro en normaliza")
            pot.normaliza(self.N)

            
            if pot.value.contradict:
                print("contradiccion después de normalizar ")
                break
            # print("saldo de normaliza")
            # pot2 = self.lpot[i]
            # pot.normaliza(N= 400)

            # pot.imprime()            
            # wait = input("Press Enter to continue.")

            # pot.simplifica(pot2)

            # if i==235:
            #     pot.imprime()

            #     wait = input("Press Enter to continue.")

            

            # if pot.checkrep():
            #     print("repeticion antes")
            #     time.sleep(50)
            
            # if pot.checkunit():
            #     print("problema unidades antes")
            #     time.sleep(50)

            print("entro en split")
            (t0,t1,t2) = pot.splitborra(var)

            self.lqp.append(t1)

            self.lqn.append(t0)


            
            # (t0c,t1c,t2c) = potcopia.splitborra(var)

            # print("resultado split")
            
            



            # (h0,h1,h2) = pot2.splitborra(var)

          

            # pot.imprime()
            # t0.imprime()
            # t1.imprime()

            # wait = input("Press Enter to continue.")
            # t0.imprime()
            # t1.imprime()
            # if t0.checkunit():
            #     print("problema en t0")
            #     t0.imprime()
            #     time.sleep(50)

            # if t1.checkunit():
            #     print("problema en t1")
            #     t1.imprime()
            #     time.sleep(50)

            # if t0.checkrep():
            #     print("problema en t0")
            #     t0.imprime()
            #     time.sleep(50)

            # if t1.checkrep():
            #     print("problema en t1")
            #     t1.imprime()
            #     time.sleep(50)

            # if t2.checkrep():
            #     print("problema en t2")
            #     t2.imprime()
            #     time.sleep(50)



       
            print("ntro en combinaborra")
            res1 = t0.combinaborra(t1,self.N)

            # if res1.checkrep():
            #     print("repeticion en combinar")
            #     time.sleep(50)
            
            # if res1.checkunit():
            #     print("problema unidades en combinar ")
            #     time.sleep(50)
            # res1c = t0c.combinaborra(t1c)
            # s = res1.tosimple()
            # sc = res1c.tosimple()

            # if not s.equal(sc):
            #     print("no iguales")
                
            #     pot.imprime()
            #     t0.imprime()
            #     t1.imprime()
            #     res1.imprime()
            #     s.imprime()


            # res2 = t0.combinaborra(h1)
            # res3 = t1.combinaborra(h0)

            # res1.imprime()
            # res1.imprime()
            # res2.imprime()
            # res3.imprime()

            # res1.inserta3(res2)

            # res1.inserta3(res3)

            # res1.imprime()
            print("inserto t2")
            
            self.insertacola(t2,i)
            
            res1.normaliza(self.N)

            if res1.value.contradict:
                print("contradiccion en resultado")

            # res1.imprime()

           
            # if res1.checkrep():
            #     print("repeticion despues normalizar")
            #     time.sleep(50)

            # if res1.checkunit():
            #     print("problema unidades despues de normalizar")
            #     time.sleep(50)
            

            # arb0 = t0.copia()
            # arb1 = arboltriple()
            # arb2 = arboltriple()

            # nuevo = arboltriple()
            # nuevo.asignavarhijos(var,arb0,arb1,arb2)

            # # pot2.imprime()

            # pot2.inserta2(nuevo)
            
            # # pot2.imprime()
            # arb0 = arboltriple() 
            # arb1 = t1.copia()
            # arb2 = arboltriple()

            # nuevo = arboltriple()
            # nuevo.asignavarhijos(var,arb0,arb1,arb2)

            # pot2.inserta2(nuevo)

            # pot2.imprime()

            # print("resultado")
            # res1.imprime()
            # wait = input("Press Enter to continue.")

            
            pot.void()
            print("Ahora inserto en la cola")
            self.insertacola(res1,i)

    def test(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            # wait = input("Press Enter to continue.")

            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i])
     
            pot = self.lqueue[i]
            pot2 = self.lpot[i]
            potc = pot.copia()
            potc.imprime()            

            # pot.simplifica(pot2)

            pot.normaliza3(N=3)
            pot.normaliza3(N=1000)
            pot.imprime()
            
            pot.normaliza3(N=3)
            pot.imprime()
            
            if (i>= 220):
                pot.imprime()
            (t0,t1,t2) = pot.splitborra(var)
            (t0c,t1c,t2c) = potc.splitborra(var)
            # (h0,h1,h2) = pot2.splitborra(var)

            t0.imprime()
            t0c.imprime()

            wait = input("Press Enter to continue.")

            t1.imprime()
            t1c.imprime()

            wait = input("Press Enter to continue.")

            t2.imprime()
            t2c.imprime()

            wait = input("Press Enter to continue.")

            # t0.imprime()
            # t1.imprime()
            # t2.imprime()

            # pot.imprime()
            
            res1 = t0.combinaborra(t1)
            res1c = t0c.combinaborra(t1c)

            res1.imprime()
            res1c.imprime()

            # res2 = t0.combinaborra(h1)
            # res3 = t1.combinaborra(h0)

            # res1.imprime()
            # res1.imprime()
            # res2.imprime()
            # res3.imprime()

            # res1.inserta3(res2)

            # res1.inserta3(res3)

            # res1.imprime()
            res1.inserta3(t2)
            res1c.inserta3(t2c)

            res1.imprime()
            res1c.imprime()
            # res1.imprime()


            # res1.imprime()

            # arb0 = t0.copia()
            # arb1 = arboltriple()
            # arb2 = arboltriple()

            # nuevo = arboltriple()
            # nuevo.asignavarhijos(var,arb0,arb1,arb2)

            # # pot2.imprime()

            # pot2.inserta2(nuevo)
            
            # # pot2.imprime()
            # arb0 = arboltriple() 
            # arb1 = t1.copia()
            # arb2 = arboltriple()

            # nuevo = arboltriple()
            # nuevo.asignavarhijos(var,arb0,arb1,arb2)

            # pot2.inserta2(nuevo)

            # pot2.imprime()

            res1.normaliza3()
            # print("resultado")
            res1.imprime()

            
            pot.anula()

            self.insertacola(res1)    

    def borra2(self):

        nuevas = True
        while nuevas and not self.inicial.solved:
            
            print("nueva vuelta")
            cola = []
            for i in range(len(self.orden)):
                
                pot = self.lqueue[i]
                while pot.listaclaus:
                    cl = pot.listaclaus.pop()
                    pot.eliminar(cl)
                    cola = cola + self.tinserta(cl,pos=i)

            if not cola:
                nuevas = False
            else:
                print(len(cola))
                for cl in cola:
                    self.insertaypodacola(cl)

                

                

                

                

    def borra4(self,listapot):

        while listapot:
            
            print (len(listapot))
            nclau = listapot.pop()
            print(len((nclau)))
            for cl in nclau:
                self.insertacola(cl)
            self.borra()

        for i in range(len(self.orden)):
            print(self.lpot[i].listaclaus)
       
    
    def anula(self):
        self.inicial.solved = True
        self.inicial.contradict = True
        for pot in self.lpot:
            pot.anula()
        for por in self.lqueue:
            pot.anula()
   
                
                
        
        
        
        
        
        