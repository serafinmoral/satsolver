# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:28:21 2020

@author: Serafin
"""
from GlobalClausulasSimple import *

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

class problemaTrian:
    def __init__(self,info):
         self.N1 = 3
         self.N2 = 1
         self.N3 = 2
         self.inicial = info
         self.orden = []
         self.lpot = []
         self.lqueue  = []
         self.peq = []
         self.posvar = dict()
         
         
    def inicia(self):
            cola = []
            for i in self.orden:
                x = globalClausulas()
                self.lpot.append(x)
                y = globalClausulas()
                self.lqueue.append(y)
    
            for cl in self.inicial.listaclaus:
#                print("inserto " ,cl)
                if len(cl)<=self.N1:
                    cola = cola + self.tinserta(cl)
                else:
                    self.insertaypodacola(cl)
                
            while cola:
                cl = cola.pop()
                if not cl:
                    self.inicial.solved = True
                    self.inicial.contradict = True
                elif len(cl)<= self.N1:
                    cola = cola + self.tinserta(cl)
                else:
                    self.insertacola(cl)
            for i in range(len(self.orden)):
                print(self.orden[i])
                print(len(self.lpot[i].listaclaus),len(self.lqueue[i].listaclaus))
                print (self.lpot[i].listaclaus)
                print (self.lqueue[i].listaclaus)


    def inicia2(self):
            cola = []
            for i in self.orden:
                x = globalClausulas()
                self.lpot.append(x)
                y = globalClausulas()
                self.lqueue.append(y)
                z = globalClausulas()
                self.peq.append(z)
            
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
            
    def insertacola(self,cl):
          indices = map(lambda x:self.posvar[abs(x)],cl)
          pos = min (indices) 
          pot = self.lqueue[pos]
          pot.inserts(cl)

    def insertaypodacola(self,x):
        cola = [x]
        while cola:
          cl = cola.pop()
          indices = map(lambda y:self.posvar[abs(y)],cl)
          pos = min (indices) 
          pot = self.lqueue[pos]
          cola = cola + pot.insertaborraypodarecnoin(cl)

          if len(cl) <= self.N1:
            varscl = set(map(abs,cl))
            pot = self.lpot[pos]
            if varscl <= pot.listavar:
                cola = cola + pot.podacola(cl)
                self.peq[pos].insertar(cl)
            for i in range(pos):
                pot = self.lpot[i]
                self.peq[i].insertar(cl)
                if varscl <= pot.listavar:
                    cola = cola + pot.podacola(cl)
                pot = self.lqueue[i]
                if varscl <= pot.listavar:
                    cola = cola + pot.podacola(cl)

          
          if pot.contradict:
              break
                
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
    
    def tinsertarec(self,cl,pos=-1):
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
            for i in range(pos):
                pot = self.lpot[i]
                if varscl <= pot.listavar:
                    cola = cola + pot.podacola(cl)
                pot = self.lqueue[i]
                if varscl <= pot.listavar:
                    cola = cola + pot.podacola(cl)
            
                
        else:
            if (pos ==-1):
                indices = map(lambda x:self.posvar[abs(x)],cl)
                pos = min (indices)
            var = self.orden[pos]
            pot = self.lpot[pos]
            cola = pot.insertasatura(cl,var)
    
        for cl2 in cola:
            indices = map(lambda x:self.posvar[abs(x)],cl2)
            pos2 = min (indices)
            if pos2 >= pos:
                self.tinsertarec(cl2)
            else:
                self.insertacola(cl)
    
    def borra(self):
        print(len(self.orden))
        for i in range(len(self.orden)):
            var = self.orden[i]
            # print("i= ", i, "var = ", self.orden[i], " n. peq. ", len(self.peq[i].listaclaus),self.peq[i].listaclaus)
            if i==140:
                print("parada")
            pot = self.lqueue[i]
            pot2 = self.lpot[i]
            l1 = pot.indices.get(var,set())
            l2 = pot.indices.get(-var,set())

            lp1 = pot2.indices.get(var,set())
            lp2 = pot2.indices.get(-var,set())
            

            npot = globalClausulas()
            for cl1 in l1:
                for cl2 in l2:
                    cl = resolution(var,cl1,cl2)
                    if 0 not in cl:
                        npot.insertar(cl)
            for cl1 in l1:
                for cl2 in lp2:
                    cl = resolution(var,cl1,cl2)
                    if 0 not in cl:
                        npot.insertar(cl)

            for cl1 in lp1:
                for cl2 in l2:
                    cl = resolution(var,cl1,cl2)
                    if 0 not in cl:
                        npot.insertar(cl)

            for cl1 in l1:
                pot2.insertar(cl1)
            for cl2 in l2:
                pot2.insertar(cl2)

                
            pot.anula()
            if npot.solved:
                self.inicial.solved = True
                self.inicial.contradict = self.inicial.contradict
                break
            if len(npot.listaclaus)>0 :
                print("longitud ", len(npot.listaclaus), npot.listavar , len(npot.listavar))
 
            npot.podaylimpiarec()
            if len(npot.listaclaus)>0 :
                print("longitud ", len(npot.listaclaus))

            for cl in npot.listaclaus:
                self.insertaypodacola(cl)

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
       
    
    def busca(self):
        
        config = []
        nconfig = set()
        pconfig = set()
        n = len(self.orden)

        i=n-1

        
        while not self.inicial.solved:
            print("i=",i)
            print(config)
            back = False
            maxpos = i
            if i<0:
                self.inicial.solved = True
                self.inicial.solution = set(config)
            else:
                pot = self.lqueue[i]
                var = self.orden[i]
#                print(var)
                
                l1 = filtra(pot.indices.get(var,set()),nconfig,pconfig,1)
                l2 = filtra(pot.indices.get(-var,set()),nconfig,pconfig,1)
                
                # print(var,len(l1),len(l2))
#                pot = self.lpot[i]
#
#                l1p = filtra(pot.indices.get(var,set()),nconfig,pconfig,1)
#                l2p = filtra(pot.indices.get(-var,set()),nconfig,pconfig,1)
#                print(len(l1p),len(l2p))
                
                lista = set(l1+l2)
                
                for cl in lista:
                    pot.eliminar(cl)
                
#                print(lista)

                for j in range(0,i):
                    pot = self.lqueue[j]
                    lista2 = filtra(pot.listaclaus,nconfig,pconfig,self.N2)
                    for cl in lista2:
                        pot.eliminar(cl)
                    lista.update(set(lista2))
                
                # print(len(lista))
                while lista and not self.inicial.solved:
                    cl = lista.pop()
                    # print(len(lista))
                    # print(cl)
                    if cl <= nconfig:
                        back = True
                        indices = map(lambda x:self.posvar[abs(x)],cl)
                        maxpos = min (indices)
                        nuevas = self.tinserta(cl)
#                    print(nuevas)
                        if self.inicial.solved:
                            break
                    
                        lista.update(set(nuevas))
            
                        # print(len(lista))
                        while lista:
                            cl = lista.pop()
                            if (cl <= nconfig):
                                indices = map(lambda x:self.posvar[abs(x)],cl)
                                maxpos = max(min (indices),maxpos)
                                nuevas = self.tinserta(cl)
                                lista.update(set(nuevas))
                            else:
                                self.insertacola(cl)
                        break

#                    if (len(n1)>0):
#                        print(config)
#                        print(n1)
                    nuevas = self.tinserta(cl)
#                    print(nuevas)
                    if self.inicial.solved:
                            break
                    
                    (n1,n2) = filtrasplit(nuevas,nconfig,pconfig,self.N2)
                    lista.update(set(n1))
                    for cl1 in n2:
                        self.insertacola(cl1)
                        
                            
                    
                    
                    
                if back:
                    for j in range(i,maxpos):
                        x = config.pop()
                        pconfig.remove(x)
                        nconfig.remove(-x)
                    i = maxpos
                else:
                    if l1:
                        nvalue = var
                    elif l2:
                        nvalue = -var
                    else:
                        pot = self.lpot[i]

                        l1 = filtra(pot.indices.get(var,set()),nconfig,pconfig,1)
                        l2 = filtra(pot.indices.get(-var,set()),nconfig,pconfig,1)
                        print(len(l1),len(l2))

                        if(var == 83):
                            print(l1)
                            print(l2)

                        if l1:
                            nvalue = var
                        elif l2:
                            nvalue = -var
                        else:
                            nvalue = self.selectval(i,var,config)
                            
                            
                    config.append(nvalue)
                    pconfig.add(nvalue)
                    nconfig.add(-nvalue)
                    i-=1
                    
        return config
                    
                            
                
                
                
        
        
        
        
        
        