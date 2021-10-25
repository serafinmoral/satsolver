# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""

import itertools
         
import networkx as nx    
import random
import time


def leeArchivoGlobal(Archivo):
    reader=open(Archivo,"r")
    cadena = reader.readline()
    
    while cadena[0]=='c':
        cadena = reader.readline()
    
    cadena.strip()
    listaaux = cadena.split()
    print(listaaux)
    nvar = int(listaaux[2])
    nclaus = int(listaaux[3])
    print(nvar)
#    print(cadena)
    while cadena[0]=='c':
        cadena = reader.readline()
#    param = cadena.split()

    infor = simpleClausulas()
    infor.nvar = nvar
    for cadena in reader:
#        print (cadena)
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= set(listaux)
            infor.insertar(clausula)
            
           



#    print("paso a limpiar")
#    infor.limpiarec(0.0)
#    print("termino de limpiar")
    return infor  

 
    
class simpleClausulas:
    def __init__(self):
        self.unit = set()
        self.contradict = False
        self.listavar = set()    
        self.claus = dict()
        self.root = True
   
    def imprime(self,space =  " "):
        print(space+"v",self.listavar)
        print(space+"contrad ", self.contradict)

        print(space+"u",self.unit)
        print(space+"clausulas")
        space2 = space + "   "
        for x in self.claus:
            print (space,x, ":  ")
            
            self.claus[x].imprime(space2)

    
        
                
    def copia(self):
      nuevo = simpleClausulas()
      nuevo.listavar = self.listavar.copy()
      nuevo.unit = self.unit.copy()
      nuevo.contradict = self.contradict
      nuevo.root = self.root
      for x in self.claus:
          nuevo.claus[x] = self.claus[x].copia()
          
      
      return nuevo

    def combina(self,otro,conf= set()):
        if otro.contradict:
            self.insertar(conf)
            return 
        aux = otro.getlista()
        if conf:
            for cl in aux:
                cl.update(conf)
        for cl in aux:
            self.insertar(cl)


    def poda(self,x):
        if x in self.claus:
            if self.claus[x].contradict:
                self.insertar({x})
            elif self.claus[x].nulo():
                self.claus.pop(x)

    def simplificaunit(self,v):
        self.simplifica(v)


    def simplifica(self,v):
        self.unit.discard(v)
        self.claus.pop(v,None)

        if -v in self.unit:
            self.anula()
        
        lista = list(self.claus.keys())
        for x in lista:
            if abs(x) < abs(v):
                if x in self.claus:
                    self.claus[x].simplifica(v)
                    self.poda(x)

        if -v in self.claus:     
            self.combina(self.claus[-v])
            self.claus.pop(-v,None)


    def simplificacl(self,cl):
         
        
        clx = cl-set(map(lambda h: -h,self.unit))
        if not clx:
            self.anula()
            return
        v = min(clx,key=lambda z: abs(z))  
        if len(clx)== 1:
            self.simplifica(v)
            return
        if clx.intersection(self.unit):
            return
        lista = self.claus.keys()
        for l in lista:
            if abs(l) < abs(v) and l in self.claus:
                self.claus[l].simplificacl(clx)
                self.poda(l)
        if v in self.claus:
            clx.discard(v)
            self.claus[v].simplificacl(clx)
            clx.add(v)
            self.poda(v)
        if -v in self.claus:
            clx.discard(-v)
            sin = self.claus[-v].calculaimplicadas(clx)
            clx.add(-v)
            self.combina(sin)

                
            
    def insertars(self,cl):
        if not cl:
            self.anula()
            return
        
        v = min(cl,key=lambda z: abs(z))

        if len(cl) == 1:
            self.unit.add(v)
            return
        
        if v not in self.claus:
            self.claus[v] = simpleClausulas()
            self.claus[v].root = False
        
        cl.discard(v)
        self.claus[v].insertars(cl)
        cl.add(v)



        
        
    
    
    
    def insertar(self,x, comprob=True):
        if self.contradict:
            return False

        if x.intersection(self.unit):
                return False
        neg = set(map(lambda x: -x, self.unit))

        xc = x-neg
        
        if not xc:
            self.anula()
            self.contradict= True
            return True
        

        if len(xc) ==1:
            v = xc.pop()
            
            self.simplifica(v)
            self.unit.add(v)
            if self.root:
                self.listavar.add(v)
            return True
        else:
            v = min(xc,key=lambda z: abs(z))
            
            gra = []
            peq = []
    
        
            for l in self.claus:
                if abs(l)> abs(v):
                    peq.append(l)
                elif abs(l)<abs(v):
                    gra.append(l)
            
            if comprob:
                print(xc)
                lo = len(xc)
                for l in peq:
                    if l in xc:
                        xc.discard(l)
                        implied = self.claus[l].compruebayreduce(xc)
                        xc.add(l)
                        if implied:
                            return False
                        if len(xc)< lo:
                            return self.insertar(xc)
                    elif -l in xc:
                        xc.discard(-l)
                        implied = self.claus[l].comprueba(xc)
                        if implied:
                            return self.insertar(xc)
                if -v in self.claus:
                    xc.discard(v)
                    implied = self.claus[-v].comprueba(xc)
                    if implied:
                        return self.insertar(xc,False)
                        
                
            if v not in self.claus:
                self.claus[v] = simpleClausulas()
                self.claus[v].root = False
                
            xc.discard(v)
            insertada =  self.claus[v].insertar(xc)
            xc.add(v)

            if not insertada:
                return False
            if self.claus[v].contradict:
                self.insertar({v})
            else:
                if self.root:
                    self.listavar.update(set(map(abs,xc)))
        

            

            if -v in self.claus:
                xc.discard(v)
                sci = self.claus[-v].calculaimplicadas(xc)
                xc.add(v)
                self.combina(sci)
            for l in gra:
                
                if l in self.claus:
                    self.claus[l].simplificacl(xc)
                    if self.claus[l].contradict:
                        self.insertar({l})
                    if self.claus[l].nulo():
                        self.claus.pop(l)
                    
                
                   
                    

            return True
                
                    
                    
                    
              
            
    def calculaimplicadas(self,cl):
        if not cl:
            return self.copia()
    
       

        v = min(cl,key=lambda z: abs(z))  

        result = simpleClausulas()
        if v in self.unit and len(cl) == 1:
            self.unit.discard(v)
            result.unit.add(v)
            return
        for l in self.claus:
            if abs(l) < abs(v):
                result.claus[l] = self.claus[l].calculaimplicadas(cl)
                if self.claus[l].nulo():
                    self.claus.pop(l)
        if v in self.claus:
            cl.discard(v)
            result.claus[v] = self.claus[v].calculaimplicadas(cl)
            if result.claus[v].nulo():
                    result.claus.pop(v)
            cl.add(v)

        return result



 
    def compruebayreduce(self,cl):
        if cl.intersection(self.unit):
            return True
        else:
            lo = len(cl)
            cl.difference_update(set(map(lambda x:-x ,self.unit  )))
            if len(cl) < lo:
                return False
        v = min(cl,key=lambda z: abs(z))
        lo = len(cl)
        for l in self.claus:
            if abs(l)>= abs(v):
                if l in cl:
                    cl.discard(l)
                    implied = self.claus[l].compruebayreduce(cl)
                    if implied:
                        return True
                    else:
                        cl.add(l)
                    if len(cl)< lo:
                        return False
                elif -l in cl:
                    cl.discard(-l)
                    implied = self.claus[l].comprueba(cl)
                    if implied:
                        return False


    def comprueba(self,cl):
        if cl.intersection(self.unit):
            return True
        else:
            v = min(cl,key=lambda z: abs(z))
            for l in self.claus:
                if abs(l)>= abs(v):
                    if l in cl:
                        cl.discard(l)
                        implied = self.claus[l].comprueba(cl)
                        cl.add(l)
                        if implied:
                            return True
                        



           
        
            
        

    def anula(self):
        self.listavar.clear()
        self.unit.clear()
        self.claus.clear()
        self.contradict = False


    def nulo(self):
        if not self.unit and not self.claus and not self.contradict:
            return True
        else:
            return False 
   

    def splitborra(self,v,n=True):
        s1 = simpleClausulas()
        s2 = simpleClausulas()
        s3 = simpleClausulas()
        
        if v in self.unit:
            s1.insertar(set())
            for x in self.unit:
                if not x == v and not x==-v:
                    s3.insertars({x})
            

        elif -v in self.unit:
            s2.insertar(set())
            for x in self.unit:
                if  not x == v and not x==-v:
                    s3.insertars({x})

            
        else:

            s3.unit = self.unit.copy()
            if s3.root:
                s3.listavar = set(map(lambda x: abs(x),s3.unit))


            for l in self.claus:
                if abs(l)> abs(v):
                    s3.claus[l] = self.claus[l].copia()
                elif abs(l)<abs(v):
                    (r1,r2,r3) = self.claus[l].splitborra(v)
                    if r1.contradict:
                        s1.insertar({l})
                        s1.listavar.add(abs(l))
                    elif not r1.nulo():
                        s1.claus[l] = r1
                        s1.listavar.update(r1.listavar)
                        s1.listavar.add(l)
                        s1.claus[l].root = False
                        s1.claus[l].listavar = set()
                    if r2.contradict:
                        s2.insertar({l})
                        s2.listavar.add(abs(l))
                    elif not r2.nulo():
                        s2.claus[l] = r2
                        s2.claus[l] = r2
                        s2.listavar.update(r2.listavar)
                        s2.listavar.add(l)
                        s2.claus[l].root = False
                        s2.claus[l].listavar = set()
                    if not r3.nulo():
                        s3.claus[l] = r3
                        s3.listavar.update(r3.listavar)
                        s3.listavar.add(l)
                        s3.claus[l].root = False
                        s3.claus[l].listavar = set()
                elif l == v:
                    s1.combina(self.claus[v])
                else:
                    s2.combina(self.claus[-v])

        
        return (s1,s2,s3)

    def addsinu(self,x):
        result = simpleClausulas()
        result.claus[x] = simpleClausulas()
        for l in self.claus:
            if abs(l) < abs(x):
                aux = self.claus[l].add(x)
                result.claus[l] = aux
            elif abs(l)> abs(x):
                aux = simpleClausulas()
                aux.claus[l] = self.claus[l]
                result.claus[x].combina(aux)
            elif l == x:
                result.claus[x].combina(self.claus[l])
        return result

    def add(self,x):
        result = self.addsinu(x)

        for y in self.unit:
            if not y == -x:
                result.insertar({x,y})

        return result

    def getlista(self):
        res = []
        if self.contradict:
            res.append(set())
        for x in self.unit:
            res.append({x})
        for z in self.claus:
            aux = self.claus[z].getlista()
            self.imprime()
            print("z" ,z, aux)
        
            for cl in aux:
                cl.add(z)
                res = res.append(cl)
        return res

    def size(self):
        res = len(self.unit)
        for x in self.claus:
            res += len(self.claus[x])


    def combinaborra(self,otro):
        
        if self.contradict:
            return otro.copia()
        if otro.contradict:
            return self.copia()
        
        result = simpleClausulas()
        if self.nulo() or otro.nulo():
            return result
        for x in self.unit:
            for y in otro.unit:
                if not x == -y:
                    result.insertar({x,y})

            if otro.claus:
                aux = otro.addsinu(x)
                result.combina(aux)
        for y in otro.unit:
            if self.claus:
                aux = self.addsinu(y)
                result.combina(aux)
        
        aux1 = list(self.claus.keys())
        aux2 = list(otro.claus.keys())

        for l1 in aux1:
            for l2 in aux2:
                if not l1==-l2:
                    rt = self.claus[l1].combinaborra(otro.claus[l2])
                    if l1== l2:
                        if l1 in result.claus:
                            result.claus[l1].combina(rt)
                    else:
                        if abs(l1)<abs(l2):
                            p1 = l1
                            p2 = l2
                        else:
                            p1 = l2
                            p2 = l1
                        rta = rt.add(p2)
                        result.claus[p1].combina(rta)

        
        
        return result     

    
pot = simpleClausulas()
pot.imprime()
pot.insertar({1,2,3})
pot.imprime()  
pot.insertar({-1,3,5})
pot.imprime()  
pot.insertar({1,2,-3})
pot.imprime()
pot.insertar({1,2,3})
pot.imprime()
pot.insertar({1,3,5})
pot.imprime()
pot.insertar({5,-3,9})
pot.imprime()
pot.insertar({-9,2,5})
pot.imprime()
(s1,s2,s3) = pot.splitborra(5)
s1.imprime()
s2.imprime()
s3.imprime()
t = s1.combinaborra(s3)
t.imprime()
