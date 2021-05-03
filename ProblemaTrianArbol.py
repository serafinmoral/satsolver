# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:28:21 2020

@author: Serafin
"""
from arboldoblesinvar import *
from SimpleClausulas import *

def filtra(lista,nconfig,pconfig,i):
    result = []
    for cl in lista:
        if not cl.intersection(pconfig):
            if len(cl-nconfig)<=i:
                result.append(cl)
    return result


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
    def __init__(self,info):
         self.N1 = 300
         self.N2 = 3
         self.inicial = info
         self.orden = []
         self.clusters = []
         self.lpot = []
         self.lqueue  = []
         self.posvar = dict()
         
         
    def inicia0(self):

            for i in self.orden:
                x = arboldoble()
                self.lpot.append(x)
                y = arboldoble()
                self.lqueue.append(y)
    
            for cl in self.inicial.listaclaus:
                self.insertacolaclau(set(cl))


            for pot in self.lqueue:
                pot.normaliza()
                
            


    def inicia2(self):
            cola = []
            for i in self.orden:
                x = arboltriple()
                self.lpot.append(x)
                y = arboltriple()
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
                    
                
    def insertapu(self,cl,pot,val):
        borrar = []
        cola = []
        if -val in pot.indices:
            for clau in pot.indices[-val]:
                cl1 = frozenset(clau-{-val})
                if not cl1:
                    self.solved = True
                    self.contradict = True
                    break
                cola.append(cl1)
                borrar.append(clau)
        if val in pot.indices:
            for clau in pot.indices[val]:
                borrar.append(clau)
        pot.inserts(cl)
    
        for clau in borrar:
            pot.eliminar(clau)
            
            
        return cola

    def podau(self,pot,val):
    
        borrar = []
        cola = []
        if -val in pot.indices:
            for clau in pot.indices[-val]:
                cl1 = frozenset(clau-{-val})
                cola.append(cl1)
                if not cl1:
                    self.solved = True
                    self.contradict = True
                    break
                borrar.append(clau)
        if val in pot.indices:
            for clau in pot.indices[val]:
                borrar.append(clau)
                
        
    
        for clau in borrar:
            pot.eliminar(clau)
        
        
        
        
        return cola
            
    def insertacolaclau(self,cl):
        if not cl:
            self.anula()
        else:
            indices = map(lambda x:self.posvar[abs(x)],cl)
            pos = min (indices) 
            pot = self.lqueue[pos]
            pot.insertaclau(cl)

    def insertacola(self,t,conf=set()):
        if t.value.listaclaus  or t.value.unit:
                if t.value.contradict and not conf:
                    self.problemacontradict()
                else:
                    indices = map(lambda x:self.posvar[abs(x)],conf.union(t.value.listavar))
                    # print(set(indices))
                    pos = min (indices) 
                    print(pos,self.clusters[pos])
                    pot = self.lqueue[pos]
                    print("inserto en ", pos)
                    # pot.imprime()

                    pot.inserta(t,conf) 
                    pot.normaliza()        
                    # print("resultado")
                    # pot.imprime() 


        if not t.var ==0:
            v = t.var
            conf.add(v)
            self.insertacola(t.hijos[0],conf)
            conf.discard(v)
            conf.add(-v)
            self.insertacola(t.hijos[1],conf)
            conf.discard(-v)

    def problemacontradict(self):
        print("contradiccion")
        self.inicial.solved = True
        self.inicial.contradict = True
                
    def tinserta(self,cl,pos=-1):
#    print(cl)
        cola = []
        if not cl:
            self.inicial.solved = True
            self.inicial.contradict = True
        elif len(cl)==1:
            val = set(cl).pop()
            var = abs(val)        
            pos = self.posvar[var]
            pot = self.lpot[pos]
            self.inicial.unit.add(val)
            self.inicial = self.inicial.restringe(val)
            cola = cola + self.insertapu(cl,pot,val)
#            print(cola)
            for i in range(pos):
            
                pot = self.lpot[i]
                if var in pot.listavar:
                    cola = cola + self.podau(pot,val)
#                    print(cola)
                pot = self.lqueue[i]
                if var in pot.listavar:
                    cola = cola + self.podau(pot,val)
#                    print(cola)
                    
        elif len(cl)<=self.N1:
        
            if (pos ==-1):
                indices = map(lambda x:self.posvar[abs(x)],cl)
                pos = min (indices)
            pot = self.lpot[pos]
            pot2 = self.lqueue[pos]
            var = self.orden[pos]

            pot.borraincluidas(cl)
            pot2.borraincluidas(cl)
            cola = pot.insertasatura(cl,var)
            
            
                
        else:
            if (pos ==-1):
                indices = map(lambda x:self.posvar[abs(x)],cl)
                pos = min (indices)
            var = self.orden[pos]
            pot = self.lpot[pos]
            cola = pot.insertasatura(cl,var)
    
        return cola
    
    
    
    def borra(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            if self.inicial.contradict:
                break
            var = self.orden[i]
            print("i= ", i, "var = ", self.orden[i], "cluster ", self.clusters[i])
     
            pot = self.lqueue[i]
            # pot2 = self.lpot[i]

            # pot.imprime()            
            # wait = input("Press Enter to continue.")

            # pot.simplifica(pot2)

            pot.normaliza()
            
            if (i>= 0):
                pot.imprime()
            (t0,t1,t2) = pot.splitborra(var)
            print("resultado split")
            t0.imprime()
            t1.imprime()
            t2.imprime()



            # (h0,h1,h2) = pot2.splitborra(var)

            # t0.imprime()
            # t1.imprime()
            # t2.imprime()

            # pot.imprime()
            # t0.imprime()
            # t1.imprime()

            # wait = input("Press Enter to continue.")
            # t0.imprime()
            # t1.imprime()

            res1 = t0.combinaborra(t1)
            print("primera combinacion")

            res1.imprime()


            # res2 = t0.combinaborra(h1)
            # res3 = t1.combinaborra(h0)

            # res1.imprime()
            # res1.imprime()
            # res2.imprime()
            # res3.imprime()

            # res1.inserta3(res2)

            # res1.inserta3(res3)

            # res1.imprime()
            res1.inserta(t2)
            # res1.imprime()
            res1.normaliza()

            print("despues de insertar t2")
            res1.imprime()

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

            self.insertacola(res1)

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
   
                
                
        
        
        
        
        
        