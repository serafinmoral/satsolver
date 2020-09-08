# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os

import itertools
         
from comunes import *  
              
from GlobalClausulas import *


from time import time

class grupo:
    def __init__(self):
        self.incon = False
        self.vars = set()
        self.clausulas = set()
        
    def imprime(self):
        print(self.clausulas)
        
    def computefromSat(self,eleme):
        self.vars = eleme.listavar
        self.clausulas = eleme.listaclaus
        
    def selectconfig(self,config):
        h = grupo()
        h.vars = self.vars - set(map(lambda x: abs(x),config))
        for x in self.clausulas:
            z = reduce(x,config)
            if not 0 in z:
                h.clausulas.add(z)
            if len(z) == 0:
                h.clausulas = {z}
                return h
                self.incon = True
        return h
            
    def calculaprobv(self,z):
        if self.incon:
            return 0
        nct = 2**(len(self.vars)-1)
        exclu = 0
        for x in self.clausulas:
            
            if not z in x:
                if -z in x:
                    exclu += 2**(len(self.vars)-len(x))
                else:
                    exclu += 2**(len(self.vars)-len(x)-1)
#            elif z in x:
#                exclu += 0
#            else:
#                exclu += 2**(len(self.vars)-len(x)-1)
        prob = (nct-exclu)/nct
        
#        if (prob==0):
#            print (self.clausulas,z)
        
        return prob
    
    def calculaprob(self):
        if self.incon:
            return 0
        nct = 2**(len(self.vars))
        exclu = 0
        for x in self.clausulas:
            exclu +=  2**(len(self.vars)-len(x))
           
        prob = (nct-exclu)/nct
        
        return prob
    
    def eliminar(self,cl):
        self.clausulas.discard(cl)
    
    def anadir(self,cl):
        clneg = set(map(lambda x: -x,cl))
        quitar = set()
        for cl2 in self.clausulas:
            if cl2 <= cl:
                return
            elif cl<= cl2:
                quitar.add(cl2)
            else:
                if not clneg.intersection(cl2):
                    h = cl2-cl
                    t = set(h).pop()
                    for x in quitar:
                        self.clausulas.discard(x)
                    self.anadir(cl.union({t}))
                    self.anadir(cl.union({-t}))
                    
                    return
        for x in quitar:
            self.clausulas.discard(x)
        self.vars.update(set(map(lambda x: abs(x), cl)))
        self.clausulas.add(cl)


    def copia(self):
        nuevo = grupo()
        nuevo.incon = self.incon 
        nuevo.vars = self.vars.copy() 
        nuevo.clausulas = self.clausulas.copy()
        return nuevo


    def combina(self,gr):
        if len(self.clausulas) <= len(gr.clausulas):
            gr1 = gr.copia()
            gr2 = self
        else:                           
            gr1 = self.copia()
            gr2 = gr
            
        for cl in gr2.clausulas:
            gr1.anadir(cl)
            
        return gr1
    
    def combinarest(self,gr,valores):
        result = grupo()
        for cl in self.clausulas:
            if (not cl.intersection(valores)):
                result.anadir(cl)
        for cl in gr.clausulas:
            if (not cl.intersection(valores)):
                result.anadir(cl)
        
        return result
        
    def parcialcombina(self,gr,valores):
    
        eli = []   
        
        neg = map(lambda x: -x,valores)
            
        for cl in gr.clausulas:
            if (not cl.intersection(valores)):
                self.anadir(cl)
#                eli.append(cl)
#        for cl in eli:
#            gr.eliminar(cl)
            
       
    def combinayborra(self,gr2,valores):
        gr1 = self
        varinval = set(map(lambda x: abs(x),valores))
        neg = map(lambda x: -x,valores)
        gr = grupo()
        for cl in gr1.clausulas:
            if (cl.intersection(neg)):
                gr.anadir(cl)
        for cl in gr2.clausulas:
            if (cl.intersection(neg)):
                gr.anadir(cl)
    
        lista = gr.vars - varinval
        for v in lista:
            gr = gr.borra(v)
    
        return gr
    
    def borra(self,v):
        gr = grupo()
        lista1 = []
        lista2 = []
        for c in self.clausulas:
                if v in c:
                    lista1.append(c)
                elif -v in c:
                    lista2.append(c)
                else:
                    gr.anadir(c)
        for c1 in lista1:
            for c2 in lista2:
                c = resolution(v,c1,c2)
                if (0 not in c):
                    gr.anadir(c)
        return gr
        
        
        
        
                
class solveSATGrupos:    
    def __init__(self,x):
        self.method = 0
        self.limit = 0
        self.solucion = False
        self.solved = False    
        self.varinorder = dict()
        self.posorder = dict()
#        self.clausulasborr = dict()
        self.conjuntoclau = x
        self.ordenbo = []
        self.configura = []
        self.conjuntopotentials = []
        self.conjuntogrupos = []
        self.indicesgrupos = dict()
        self.potentialsborrado = dict() 
        self.potentialcombinat = dict()
#        self.potentialmandado = dict()
        self.originalpotentials = []
        self.bloqueadas = set()
        self.totaloriginal = x
        self.nvar = x.nvar

        
#        for y in x.listavar:
#            self.clausulasborr[y] = {}
#            self.clausulasborr[-y] = {}
#                     
    def inicia(self):
        print(len(self.conjuntoclau.listaclaus))
        self.conjuntoclau.unitprop()
#        self.conjuntoclau.satura()
        t1 = time()
        self.conjuntoclau.podaylimpia() 
        t2 = time()
        print("Tiempo " , t2-t1)
        self.solved = self.conjuntoclau.solved
        self.solucion = self.conjuntoclau.solution
        
#        self.bloqueadas = self.conjuntoclau.calcularbloqueadas()
#        print("fin de calculo de bloqueadas")
        (self.ordenbo,self.varinorder,self.conjuntosvar) = self.conjuntoclau.computeOrder()
        print("fin de calculo de orden")
        self.totaloriginal = self.conjuntoclau.copia()
        
        self.extraegrupos()
        
        self.combinagrupos2()

        self.conjuntopotentials = self.conjuntoclau.extraePotentials(self.ordenbo)
        
        
        
        
        
#        print("potenciales calculados")
  
    def combinagrupos2(self,M=4):
     i=0
     j=i+1
     
     while j < len(self.conjuntogrupos):
         gr1 = self.conjuntogrupos[i]
         gr2 = self.conjuntogrupos[j]
         co1 = gr1.vars
         co2 = gr2.vars
         inter = co1.intersection(co2)
         union = co1.union(co2)
         if (inter and len(gr1.clausulas)<=M and len(gr2.clausulas)<=M):
             if (len(union-co1)<=3) or (len(union-co2)<=3):
                 gr = gr1.combina(gr2)
                 self.borragrupo(gr1)
                 self.borragrupo(gr2)
                 self.insertagrupo(gr)
             else:
                 j+=1
                 if(j>=len(self.conjuntogrupos)):
                     i+=1
                     j = i+1
         else:
          j+=1
          if(j>=len(self.conjuntogrupos)):
              i+=1
              j = i+1  
             
     def combinagrupos3(self,M=4):
            
         lista = list(sorted(list(filter(lambda x: len(x.clausulas)<=M,self.listagrupos) ,key = lambda x: len(x.clausulas))))
            
         final = []
         anadir = []
         eliminar = []
            
         i=0
         j=i+1
     
         while j < len(lista):
             gr1 = self.conjuntogrupos[i]
             gr2 = self.conjuntogrupos[j]
             co1 = gr1.vars
             co2 = gr2.vars
             inter = co1.intersection(co2)
             union = co1.union(co2)
             if (inter):
                 gr = gr1.combina(gr2)
                 self.borragrupo(gr1)
                 self.borragrupo(gr2)
                 self.insertagrupo(gr)
                 lista.remove(gr1)
                 lista.remove(gr2)
                 
             else:
                 j+=1
                 if(j>=len(lista)):
                     i+=1
                     j = i+1
         else:
          j+=1
          if(j>=len(self.conjuntogrupos)):
              i+=1
              j = i+1  
            
     
     
     while j < len(self.conjuntogrupos):
         gr1 = self.conjuntogrupos[i]
         gr2 = self.conjuntogrupos[j]
         co1 = gr1.vars
         co2 = gr2.vars
         inter = co1.intersection(co2)
         union = co1.union(co2)
         if (inter and len(gr1.vars)<=M and len(gr2.vars)<=M):
             if (len(union-co1)<=3) or (len(union-co2)<=3):
                 gr = gr1.combina(gr2)
                 self.borragrupo(gr1)
                 self.borragrupo(gr2)
                 self.insertagrupo(gr)
             else:
                 j+=1
                 if(j>=len(self.conjuntogrupos)):
                     i+=1
                     j = i+1
         else:
          j+=1
          if(j>=len(self.conjuntogrupos)):
              i+=1
              j = i+1                     
                    
        
  
    def combinagrupos(self,M=4):
        for var in self.totaloriginal.listavar:
            l1 = self.indicesgrupos.get(var,set())
            lista = list(sorted(l1,key = lambda x: len(x.clausulas)))
            
            final = []
            anadir = []
            eliminar = []
            
            i = 0
            
            if (len(lista)==1):
                end = True
            else:
                end = False
            while not end:
                gr1 = lista[i]
                gr2 = lista[i+1]
                
                i += 2
                if i >= len(lista)-1:
                    end = True
                if len(gr2.clausulas)>M:
                    end = True
                else:
                    eliminar.append(gr1)
                    eliminar.append(gr2)
                    gr = gr1.combina(gr2)
                    if len(gr.clausulas)>M:
                        anadir.append(gr)
                    else:
                        final.append(gr)

            while final:
                gr1 = final.pop()
                
                if final:
                    gr2 = final.pop()
                    gr = gr1.combina(gr2)
                    if len(gr.clausulas)>M:
                        anadir.append(gr)
                    else:
                        final.append(gr)
                else:
                    anadir.append(gr1)
                    
                    
            for gr in anadir:
                self.insertagrupo(gr)
            
            for gr in eliminar:
                self.borragrupo(gr)
                    
                    
        


    def extraegrupos(self):
        while (len(self.totaloriginal.listaclaus)>0):
            g = grupo()
            eleme = globalClausulas()
            claus = next(iter(self.totaloriginal.listaclaus))
            eleme.insertar(claus)
            self.totaloriginal.eliminar(claus)
            lista = self.totaloriginal.entorno(claus)
#            print (lista)
            while lista:
                h = lista.pop()
                eleme.insertar(h)
                self.totaloriginal.eliminar(h)
                lista.intersection_update(self.totaloriginal.entorno(h))
#            print (len(eleme.listaclaus))
            g.computefromSat(eleme)
            if (g.calculaprob==0.0):
                self.solved = True 
                self.solucion = False
#            t.imprime()
            self.insertagrupo(g)
                 
            
                  


    def extraegrupos2(self,M=0):
        while (len(self.totaloriginal.listaclaus)>0):
            g = grupo()
            claus = next(iter(self.totaloriginal.listaclaus))
            g.anadir(claus)
            self.totaloriginal.eliminar(claus)
            lista = self.totaloriginal.entorno(claus)
#            print (lista)
            while lista:
                h = max(lista,key = lambda x: len(g.vars.intersection(  variables(x))))
                g.anadir(h)
                self.totaloriginal.eliminar(h)
                lista.discard(h)
                if (M==0 or len(lista)>M):
                    lista.intersection_update(self.totaloriginal.entorno(h))
#            print (len(eleme.listaclaus))
#            t.imprime()
            self.insertagrupo(g)
                 
    
    
    def extraearboles2(self):
        while (len(self.totaloriginal.listaclaus)>0):
            t = arbolpot()
            eleme = globalClausulas()
            claus = next(iter(self.totaloriginal.listaclaus))
            eleme.insertar(claus)
            self.totaloriginal.eliminar(claus)
          
#            print (len(eleme.listaclaus))
            t.computefromSat(eleme)
#            t.imprime()
            self.insertaarbol(t)
            
    def insertagrupo(self,t):
        self.conjuntogrupos.append(t)
        for var in t.vars:
            if var in self.indicesgrupos:
                self.indicesgrupos[var].add(t)
            else:
                self.indicesgrupos[var] = {t}

    def borragrupo(self,t):
        self.conjuntogrupos.remove(t)
        for var in t.vars:
            self.indicesgrupos[var].discard(t)
        



    def compruebasol(self):
        correcto = True
        if self.solved and self.solucion:
            for h in self.originalpotentials:
                for y in h.listaclaus:
                    t = reduce(y,self.configura)
                    if len(t)== 0:
                        print("solucion no valida ")
                        print(self.configura)
                        print("clausula ",y)
                        correcto = False
                        break
        if correcto:
            print("Solucion Correcta")
                
            
            
    def borra(self):
        current=1
        print (self.conjuntoclau.listavar)
        nvar = len(self.ordenbo)
        
        total = 0
        
        while current<= nvar  and not self.solved:
#            print (current)
           
            varb = self.ordenbo[current-1]
           
            current = current +1
#            print ("Borrando variable ", varb)
            
            # self.listapos[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # self.listaneg[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # print(len(self.listapos[varb]))
            # self.limpiaordennum(self.listapos[varb])
            # print(len(self.listapos[varb]))
            # print(len(self.listaneg[varb]))
            # self.limpiaordennum(self.listaneg[varb])
            # print(len(self.listaneg[varb]))
            
            listapotv = calculapotentials(self.conjuntopotentials,varb)
            
            self.potentialsborrado[varb] = listapotv
            
#            print(len(listapotv))
            
            pot = globalClausulas()
            
            for p2 in listapotv:
                pot.combina(p2)
            
#            pot.podavar2(varb)
            
#            th = 0.05
#            th = 0.000

            
#            (pot1,pot2) = pot.split(varb)
#            print(pot1.listaclaus)
#            print("split ",len(pot1.listaclaus), len(pot2.listaclaus)  )
            self.potentialcombinat[varb] = pot
#            total = total +  len(pot1.listaclaus)
#            print(pot1.listaclaus)
#            unitarias = set()
#            otras = set()
#            potm= globalClausulas()
#            potm = pot1.marginalizaapr(varb,th,self.bloqueadas,unitarias,otras)
#            potm = globalClausulas()
#            potm.podaylimpia()
#            print(potm.listaclaus)
#            print(len(otras))
#            if (unitarias):
#                print("unitarias")
#                for p in unitarias:
#                    self.original.unitprev.add(p)
#                self.original.unitprop()      

            
            
            
            

            
#            self.potentialmandado[varb] = potm
            
           
#            if pot1.contradict:
#                self.solved = True
#                self.con = True
            
            
               # for x in nuevas:
            #   print (x.lista)
#            print("tamaño sin limpiar" ,len(potm.listaclaus))
#            print("ordenadas")
#            potm.limpiarec(th)   
#            potm.limpiatama(1)
#            print(potm.listaclaus)
#            potm.limpianum(10)
#            print(potm.listaclaus)

#            potm.limpiarec(th)
            # solveSATBorrado.limpiarec(nuevas,noborrad,posiciones)
#            print("tamaño después de limpiar" ,len(potm.listaclaus))
            
            # for x in self.listapos[varb]:
            #    print (x, self.claus.conjunto[x].lista)
            
#            nuevas = self.conjuntoclau.borraAprox(varb,self.clausulasborr[varb],self.clausulasborr[-varb],th)
            
#            self.conjuntopotentials.append(potm)
#            self.conjuntopotentials.append(pot2)

           
         
            
#            print(total)
            
            
#            h = list(nuevas.listaclaus)
#            
#            h.sort(key=lambda x: len(x.lista))
          
#            i=0
           
#                if (i==600):
#                    break
                    
  
             
    
    def calculavalor(self,valores,var):
        pot = self.potentialcombinat[abs(var)]
        negativos = set(map(lambda x: -x,valores))
        if var in pot.indices:
            for x in pot.indices[var]:
                if ((x-{var})<=negativos):
                    return [True,x]
        return [False]
                
    
 
    
    
                   
    
    def calculavalor2(self,valores,var):
        pot = self.totaloriginal
        negativos = set(map(lambda x: -x,valores))
        if var in pot.indices:
            for x in pot.indices[var]:
                if ((x-{var})<=negativos):
                    return [True,x]
        return [False]
    
    def buscadinamico(self):
        valores = set()
        nnodos = 0
        variables = set()
        quedan = set()
        
        while not (self.solved):
            nnodos +=1
            
    def buscayborra(self):
        valores = set()
        n = len(self.ordenbo)
        current = 0
        maxc = current
        nnodos = 0
        
        while not (self.solved):
            nnodos += 1
            var = self.solved
    
    def back(self):
        valores = set()
        self.varinorder = dict()
#        print(self.nvar)
        n = self.nvar
        nnodos = 0
        active = set(range(1,n+1))
        level = dict()
        current = 1
        ordenvar = []
        while not (self.solved):
            print(current)
#            print(valores)
#            print(active)
#            print(active)
            nnodos += 1
            if not current in level:
                xpos = dict()
                xneg = dict()
                rompe = False
                forced = False
                for gr in self.conjuntogrupos:
                    grupo = gr.selectconfig(valores)
                    if rompe:
                        
                            self.solved=True
                            self.solucion = False
                        
#                        else:
#                            imax = 0
#                            for y in gr.vars:
#                        
#                                pos = self.varinorder.get(y,n)
#                                if (pos>imax) and (pos<current):
#                                    imax = pos
#                            print("vuelta atrás uno***************************************************")
#                            
#                            for j in range(imax+1,current):
#                                      del level[j]
#                                      l = ordenvar.pop()
#                                      valores.discard(l)
#                                      valores.discard(-l)
#                                      active.add(l)
#                            current = imax
#                            if (current == 0):
#                                    self.solved=True
#                                    self.solucion = False
#                            
##                            print("Vuelta atras")
##                            print(current)
##                            print(valores)
#                            rompe = True
#                            break                        
                    else:
                            
                            for var in grupo.vars:
                                t1 = grupo.calculaprobv(var)
                                t2 = grupo.calculaprobv(-var)
                                if not var in xpos:
                                    xpos[var]=t1
                                
                                else:
                                    xpos[var]*=t1
                                if not var in xneg:
                                    xneg[var] = t2
                                else:
                                    xneg[var]*=t2   
                                if t1 == 0.0:
                                    vars1 = gr.vars
                                    forced = True
                                    varf = -var

                                if t2 == 0.0:
                                    vars2 = gr.vars
                                    forced = True
                                    varf = var
                                    
                                if xpos[var] == 0.0 and xneg[var] == 0.0:
                                    imax = 0
                                    totalvars = vars1.union(vars2)
                                    for y in totalvars:
                        
                                        pos = self.varinorder.get(y,n)
                                        if (pos>imax) and (pos<current):
                                            imax = pos
                                    print("vuelta atrás dos")
                                    for j in range(imax+1,current):
                                            del level[j]
                                            l = ordenvar.pop()
                                            valores.discard(l)
                                            valores.discard(-l)
                                            active.add(l)
                    
                                    current = imax
                                    if (current == 0):
                                        self.solved=True
                                        self.solucion = False
                                    rompe=True
                                    break
                            if rompe:
                                break
                if forced and not rompe:
                        valores.add(varf)
                        level[current] = 0
                        ordenvar.append(abs(varf))
                        self.varinorder[abs(varf)] = current
                        current +=1  
                        active.discard(abs(varf))
#                        print("avance")
#                        print(current)
#                        print(valores, len(valores))
                elif not rompe:
                        vmax = 1
                        
                        for var in active:
                            if not var in xpos:
                                if (1.0 >= vmax):
                                    varf = var
                            else:
                                if xpos[var] >= xneg[var]:
                                    h = xpos[var] / xneg[var]
                                    if h>= vmax:
                                        vmax = h
                                        varf = var
                                else:
                                    h = xneg[var] / xpos[var]
                                    if h>= vmax:
                                        vmax = h
                                        varf = -var  
                        print(varf,vmax)
                        valores.add(varf)
                        level[current] = varf
                        ordenvar.append(abs(varf))
                        self.varinorder[abs(varf)] = current
                        current +=1  
                        active.discard(abs(varf))
#                        print("avance")
#                        print(current)
#                        print(valores, len(valores))
                    
                    
                if current == (n+1):
                            self.solved = True
                            self.solucion = True
                            self.configura = valores
                        
            elif  not level[current]   ==0:
                    varf = -level[current]
                    level[current] = 0
                    valores.discard(-varf)
                    valores.add(varf)
                    current+=1
            else:
                    del level[current]
                    l = ordenvar.pop()
                    valores.discard(l)
                    valores.discard(-l)
                    active.add(l)
                    current -= 1
                    if (current == 0):
                         self.solved=True
                         self.solucion = False
                    
                        
                    
                        
                            
                                                        
                            
                        
                        
            
 
    
    
    def busca(self):
        valores = set()
        print(self.ordenbo)
        n = len(self.ordenbo)
        current = n-1
        minc = current
        nnodos = 0
        
        while not (self.solved):
            print(current)
#            print(valores)
#            print(valores)
            nnodos += 1
            var = self.ordenbo[current]
#            print(var)
 
            
            if (current < minc):
                print (current)
                minc = current
#                print(var)
#            print(var)

            xpos = 1.0
            xneg = 1.0
                
            bneg = False
            bpos = False
            vuelta = False
                
            for x in self.indicesgrupos[var]:
#                    x.imprime()
                    grupo = x.selectconfig(valores)
                    
                    
                    if (grupo.calculaprob()==0):
                        imin = n-1
#                print(claures)
                        for y in x.vars:
                    
                                pos = self.varinorder[y]
                                if (pos<imin) and (pos>current):
                                    imin = pos
                        print("vuelta atrás")
#                print(claures)
                     
                
#                print(claures)
                
        
                        for j in range(current+1,imin+1):
                                valores.discard(self.ordenbo[j])
                                valores.discard(-self.ordenbo[j])
                    
                        current = imin
                        xpos = 0.0
                        xneg = 0.0
                        vuelta = True
                        break
                    
#                    x.imprime()
                    if(xpos>0):
                        t1 = grupo.calculaprobv(var)
                    
                    if(xneg>0):
                        t2 = grupo.calculaprobv(-var)
                    
                    if (t1==0) and not bpos:
                        gr1 = x
                        bpos = True
                    if (t2==0) and not bneg:
                        gr2 = x
                        bneg = True
                    
                    xpos *= t1
                    xneg *= t2    
                    
                    if (xpos==0) and (xneg==0):
                        break
            
            if (xpos==0) and (xneg==0) and not (gr1==gr2) and not vuelta:
                    
 
                    
                        gr = gr1.combinarest(gr2,valores)
                    
                        self.insertagrupo(gr)
        
                        grp = gr.selectconfig(valores)
                        
                        
                        print("dos negativos",grp.calculaprob())
                        if(gr.calculaprob()==0):
                            self.solved = True
                            self.solucion = False
                        else:
                            imin = n-1
#                print(claures)
                            for y in gr.vars:
                    
                                pos = self.varinorder[y]
                                if (pos<imin) and (pos>current):
                                    imin = pos
                
#                print(claures)
                
        
                            for j in range(current+1,imin+1):
                                    valores.discard(self.ordenbo[j])
                                    valores.discard(-self.ordenbo[j])
                    
                            current = imin

           
#                    
            elif not vuelta:    
                    current-= 1
#                    print(xpos,xneg)
                    if (xpos>xneg):
                         valores.add(var)
                    else:
                        valores.add(-var)
                            
            if (current == -1):
                self.solved = True
                self.solucion = True
                self.configura = valores
        print("N. nodos ", nnodos)

  
 

 
 




    
#print(SeleccionarArchivo("ArchivosSAT.txt"))
#info = leeArchivoGlobal('SAT_V155C1135.cnf')
# info.satura(4)
#print("fin de satura")
# info.busca()
t1 = time()
#info = leeArchivoGlobal('SAT_V153C408.cnf')

#info = leeArchivoGlobal('SAT_V1168C4675.cnf')

#info = leeArchivoGlobal('SAT_V6498C130997.cnf')
ttotal = 0
i = 0
reader=open('entrada',"r")



for cad in reader:
    nombre = cad.rstrip()             
    t1 = time()
    i +=1
    info = leeArchivoGlobal(nombre)
    t2= time()



#info = leeArchivoSet('SAT_V144C560.cnf')

#print(info.listavar)

    problema = solveSATGrupos(info)
    

#print(problema.conjuntoclau.listavar)


    problema.inicia()
    t3 = time()



    problema.borra()
#    problema.explora()

    t4 = time()
    

#problema.originalpotentials = problema.totaloriginal.extraePotentials(problema.ordenbo,problema.conjuntosvar)

    problema.busca()
    t5 = time()



    problema.compruebasol()
#info2 = leeArchivoGlobal('SAT_V1168C4675.cnf')
#info2 = leeArchivoGlobal('aes_32_1_keyfind_1.cnf')
    info2 = leeArchivoGlobal(nombre)
#info2 = leeArchivoGlobal('SAT_V153C408.cnf')

    info2.compruebasol(problema.configura)
    

    print(problema.configura)
    print(problema.solucion)
    print("tiempo lectura ",t2-t1)
    print("tiempo inicio ",t3-t2)
    print("tiempo borrado ",t4-t3)
    print("tiempo busqueda ",t5-t4)

    print("tiempo TOTAL ",t5-t1)
    ttotal += t5-t1

print ("tiempo medio ", ttotal/i)