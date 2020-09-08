# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""

import itertools
         
from comunes import *  
             

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

    infor = globalClausulas()
    infor.nvar = nvar
    for cadena in reader:
#        print (cadena)
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= frozenset(listaux)
            infor.insertar(clausula)
            if(len(clausula)==1):
                h = set(clausula).pop()
                infor.unitprev.add(h)
            elif (len(clausula)==2):
                infor.dobles.add(clausula)
                mclau = frozenset(map(lambda x: -x,clausula))
                if mclau in infor.dobles:
                    par = set(clausula)
                    l1 = par.pop()
                    l2 = -par.pop()
                    if(abs(l1)<abs(l2)):
                        infor.equiv.add((l1,l2))
                    else:
                        infor.equiv.add((l2,l1))



#    print("paso a limpiar")
#    infor.limpiarec(0.0)
#    print("termino de limpiar")
    return infor  

  
    
class globalClausulas:
    def __init__(self):
         self.nvar = 0
         self.listaclaus = set()
         self.indices = dict()
         self.contradict = False
         self.listavar = set()    
         self.solved = False
         self.solution = set()
         self.unit = set()
         self.equiv = set()
         self.unitprev = set()
         self.dobles = set()
         self.refer = dict()
         self.apren = set()
         self.totalapren = set()
         
         
    def Conjunto(self):
        result = []
        for c in self.listaclaus:
            result= result + [list(c)]
        return result
         
    def compruebasol(self,config):
        correcto = True
        for y in self.listaclaus:
            t = reduce(y,config)
            if len(t)== 0:
                print("solucion no valida ")
                print(config)
                print("clausula ",y)
                correcto = False
                break
        if correcto:
            print("Solucion Correcta")
           
            
    def propagacion_unitaria(self):
        self.unitprev= set()
        for c in self.listaclaus:
            if (len(c))== 1:
                h = set(c).pop()
                self.unitprev.add(h)
                self.unit.add(h)
        self.unitprop()        
                
            
    def unitprop(self):
        while self.unitprev:
            p = self.unitprev.pop()
            if p in self.indices:
                borrar = set()
                for c in self.indices[p]:
                    
                        borrar.add(c)
                for c in borrar:
                    self.eliminar(c)
            if -p in self.indices:
                borrar = set()
                for c in self.indices[-p]:
                    borrar.add(c)
                for c in borrar:
                    c2 = frozenset(set(c)-{-p})

                    self.refer[c2] = self.refer.get(c,set()).union(self.refer.get(frozenset({p}),set()))
#                    if   not c2.union(self.refer[c2]).intersection(x):
#                        print(c2,self.refer[c2])
#                        print(c,self.refer.get(c,set()))
#                        print(p,self.refer.get(frozenset({p}),set()))
#                        print("problema 1")
#                        
                    self.eliminar(c)
                    if(not c2):
                        self.contradict = True
                        self.apren = self.refer[c2]
                        self.totalapren.add(frozenset(self.refer[c2]))
#                        print("aprendo ",self.refer[c2] )
#                        print(self.refer.get(frozenset({p}),set()))
#                        print(self.refer.get(c,set()))
                        return
                    self.insertar(c2)
                    if (len(c2)==1):
                        h = set(c2).pop()
                        self.unitprev.add(h)
                        self.unit.add(h)
                    elif (len(c2)==2):
                        self.dobles.add(c2)
                        mc = frozenset(map(lambda x: -x, c2))
                        if mc in self.dobles:
#                            print(c,mc,"nueva equivalencia")
                            par = set(c2)
                            t1 = par.pop()
                            t2 = -par.pop()
                            
                            if(abs(t1)<abs(t2)):
                                if(not  (-t1,-t2) in self.equiv):    
                                    self.equiv.add((t1,t2))
#                                    print("nueva equivalencia ", t1, t2)
#                                    time.sleep(3)
                            else:
                                if(not (-t2,-t1) in self.equiv):
                                    self.equiv.add((t2,t1)) 
                        
                        
    def equivprop(self):

        equival = []
        while self.equiv:
            (l1,l2) = self.equiv.pop()
            equival.append((l1,l2))
            
#            print("equivalencia " ,l1 ,l2)
            eliminar = set()
            anadir = set()
#            print("quitamos ", l2)
            if l2 in self.indices:
                for c in self.indices[l2]:
                    eliminar.add(c)
                    if not -l1 in c: 
                        h =  frozenset(set(c)-{l2}).union({l1})
                        anadir.add(h)
                        
                        ref2 = self.refer.get(c,set()).union(self.refer.get(frozenset({-l2,l1}),set()))
                        
                        self.refer[h]= ref2
#                        if   not h.union(self.refer[h]).intersection(x):
#                            print(h,self.refer[h])
#                            print(c,self.refer.get(c,set()))
#                            
#                            print("problema 2")
            if -l2 in self.indices:
                for c in self.indices[-l2]:
                    eliminar.add(c)
                    if not l1 in c: 
                        h =  frozenset(set(c)-{-l2}).union({-l1})
                        anadir.add(h)
                        
                        ref2 = self.refer.get(c,set()).union(self.refer.get(frozenset({l2,-l1}),set()))
                       
                        self.refer[h]= ref2
#                        if   not h.union(self.refer[h]).intersection(x):
#                            print(h,self.refer[h])
#                            print(c,self.refer.get(c,set()))
#                            
#                            print("problema 3")
            for c in eliminar:
#                    print("borramos ",c)
                    self.eliminar(c)
#                    if (len(c)==2):
#                        self.equiv.discard(c)
            for c in anadir:
#                    print("añadimos ", c)
                    self.insertayborra(c)
                    if (len(c)==1):
                        w = set(c).pop()
                        self.unit.add(w)
                        self.unitprev.add(w)
                    if (len(c)==2):
                        self.dobles.add(c)
                        mc = frozenset(map(lambda x: -x, c))
                        if mc in self.dobles:
#                            print(c,mc,"nueva equivalencia")
                            par = set(c)
                            t1 = par.pop()
                            t2 = -par.pop()
                            
                            if(abs(t1)<abs(t2)):
                                if(not  (-t1,-t2) in self.equiv):    
                                    self.equiv.add((t1,t2))
#                                    print("nueva equivalencia ", t1, t2)
#                                    time.sleep(3)
                            else:
                                if(not (-t2,-t1) in self.equiv):
                                    self.equiv.add((t2,t1)) 
#                                    print("nueva equivalencia ", t2, t1)
#                                    time.sleep(3)

            self.listavar.discard(abs(l2))
            self.unitprop()

            
        return equival                        
        
         
    def calculaconjuntos(self):
        z = globalClausulas()
        for cla in self.listaclaus:
            posclau = frozenset(map(abs,cla))
            z.insertar(posclau)
        return z
    
    def computeComplV(self,y):
        conjunto = set({y})
        l=0
        if y in self.indices:
            l = len(self.indices[y])
            for z in self.indices[y]:
                conjunto.update(z)
#        print (y, conjunto)
        return (conjunto,l)
    
    def nextVar(self,noborrad):
        y = noborrad[0]
        (conjunto,k) = self.computeComplV(y)
        best = len(conjunto)*len(self.listaclaus) + k 
        nbest = y
        for y in noborrad[1:]:
            (c2,k) = self.computeComplV(y)
            z = len(c2)*len(self.listaclaus) + k 
            if(z<best) :
                nbest=y
                best = z
                conjunto = c2
        return (nbest,conjunto)
        
    def actualizab(self,var,conjunto):
        conjunto = frozenset(conjunto -{var})
        if (len(conjunto)>0):
            self.insertar(conjunto) 
        if var in self.indices:
            while bool(self.indices[var]):
#                print(self.indices[var])
                c = self.indices[var].pop()
                self.eliminar(c)
            
            
    def computeOrder(self):
        
        ordenbo = []
        varinorder = dict()
        conjuntosvar = dict()
        conjuntos = self.calculaconjuntos()
        noborrad = list(self.listavar)
        current = 1
        while len(noborrad)>0:
            (var,conjunto) = conjuntos.nextVar(noborrad)
            noborrad.remove(var)
            ordenbo.append(var)
#            print(var)
            varinorder[var] = current-1
            conjuntosvar[var] = conjunto
#            print (current)
            current += 1
     
#            print (var)
#            print(conjunto)
            conjuntos.actualizab(var,conjunto)
        return(ordenbo,varinorder,conjuntosvar)
        
        
                  
    def computeOrder2(self):
        
       
        varinorder = dict()
        noborrad = list(self.listavar)
        
        scores = dict()
        
        for x in noborrad:
            scores[x] = 1.0
            scores[-x] = 1.0
        

        for cl in self.listaclaus:
            for x in cl:
                scores[-x] *= ((2**(len(cl)-1)-1)/2**(len(cl)-1))
                
#        print(scores)

                
        for x in noborrad:
            h = scores[x]/(scores[x]+scores[-x])
            scores[x] = max(h,1-h)
            
        
        ordenbo = sorted(noborrad,key = lambda x: scores[x])
        
        print(ordenbo)
        
        for i in range(len(ordenbo)):
            varinorder[ordenbo[i]] = i
        
        return(ordenbo,varinorder)
        
                  
    def computeOrder3(self):
        conjunto = self.copia()
        
        
        ordenbo = []
       
        varinorder = dict()
        noborrad = set(self.listavar)
        
        index = 0
        
        while noborrad:
            
            minv = min(noborrad , key=lambda x: (len(conjunto.indices.get(x,set()))-1)*    (len(conjunto.indices.get(-x,set()))-1))
#            print (minv)
            ordenbo.append(minv)
            varinorder[minv] = index
            index += 1
            conjunto.marginalizaAprox(minv,10)
            noborrad.discard(minv)
        
                
#        print(scores)

        
            
        
        return(ordenbo,varinorder)
        
        
    def marginalizaAprox(self,var,M=200):
        r1 = self.indices.get(var,set())
        r2 = self.indices.get(-var,set())
        
        
        lista =[]
        
        for clau1 in r1:
            for clau2 in r2:
                clau = resolution(var,clau1,clau2)
                if (0 not in clau):
                    lista.append(clau)
                    
        lista.sort(key=len)
        for i in range(min(M,len(lista))):
            clau = lista[i]
            self.insertayborra(clau)
        while r1:
            self.eliminar(r1.pop())
        while r2:
            self.eliminar(r2.pop())

     
    def computeCliques(self):
        
        ordenbo = []
        varinorder = dict()
        conjuntosvar = dict()
        conjuntos = self.calculaconjuntos()
        noborrad = list(self.listavar)
        current = 1
        while len(noborrad)>0:
            (var,conjunto) = conjuntos.nextVar(noborrad)
            noborrad.remove(var)
            ordenbo.append(var)
            varinorder[var] = current-1
            conjuntosvar[var] = conjunto
#            print (current)
            current += 1
     
#            print (var)
#            print(conjunto)
            conjuntos.actualizab(var,conjunto)
        return(ordenbo,varinorder,conjuntosvar)
        
        
    def extraePotentials(self,ordenbo):
            listpot = []
            for v in ordenbo:
                pot = self.extraeBorra(v)
                listpot.append(pot)
            return listpot
        
        
                
    def copia(self):
      nuevo = globalClausulas()
      for x in self.listaclaus:
          nuevo.insertar(x)
      return nuevo
        
        
        
    def incorpora(self,conjunto,valores):
        y = globalClausulas()
        for cl in conjunto:
            y.insertar(cl)
        for v in valores:
            y = y.restringe(v)
            if y.contradict:
                break
        if y.contradict:
            self.contradict=True
            self.apren = y.apren
#            print("incorpora", y.totalapren)
            self.totalapren.update(y.totalapren)
        else:
            for cl in y.listaclaus:
                    self.insertar(cl)
                    self.refer[cl] = y.refer.get(cl,set())
                
                


                
  
    
    def restringe(self,x):

        y = globalClausulas()
        y.listavar = self.listavar-{abs(x)}
        if self.contradict:
            y.contradict= True
            y.apren = self.apren
            y.totalapren = self.totalapren.copy()
        for cl in self.listaclaus:
            if (x not in cl) and (-x not in cl):
                y.insertar(cl)
                if (cl in self.refer):
                    y.refer[cl] = self.refer[cl]
            elif -x in cl:
                cl2 = frozenset(cl-{-x})
                if cl in self.refer:
                    y.refer[cl2]=self.refer[cl].union({-x})
                else:
                    y.refer[cl2]= {-x}
#                if not sol.intersection(cl2.union(y.refer[cl2])):
#                    print("problema 5")
                if (cl2):
                    y.insertar(cl2)
                else:
                    y.listaclaus.clear()
                    y.insertar(cl2)
                    y.contradict = True
                    y.apren = y.refer[cl2]
                    y.totalapren.add(frozenset(y.refer[cl2]))

#                    print("Aprendo ·", y.apren)
                    break
        return y
        
         
    def calculascore(self,valores,var):
        score = 1.0
        for x in self.indices[var]:
            z = reduce(x,valores)
            if 0 not in z:
                score *= (2**(len(z)-1)-1)/2**(len(z)-1)
            if score==0.0:
                return [score,x]
        return [score]
    
    
            
        
                    
     
    def eliminaListas(self,lista1,lista2,noborrad):
        
        for y in lista1:
            for z in y:
                if (z in noborrad) or (-z in noborrad):
                        self.indices[z].remove(y)
                        

        for y in lista2:
            for z in y:
                if (z in noborrad) or (-z in noborrad):
                        self.indices[z].remove(y)     

    def busca(self):
        print("Comienza busqueda")
        valores = set()
        variables = []
        restantes = self.listavar.copy()
        n = len(restantes)
        current = 0
        while current< n and not self.solved:
            print(current)
#            print(current)
            bvar = -1
            best = 1.0
            pos = True
            forced = False
            incon = False
            for var in restantes:
                varneg = self.calculascore(valores,var)
                varpos = self.calculascore(valores,-var)
                if ((varpos[0]==0.0) and (varneg[0]==0.0)):
                    print(varpos[0],varneg[0])

                    clau1 = varpos[1]
                    clau2 = varneg[1]
#                   print(clau1.lista)
#                   print(clau2.lista)
#                   print(var)
                    claures = resolution(var,clau1,clau2)
                    if(len(claures)==0):
                        self.solved = True
                        self.contradict = True
                        self.solucion = False
                    
                    imax = 0
#                   print(claures.lista)
                    for y in claures:
                        z = abs(y)
                        posic = variables.index(z)
                        if (posic >imax):
                            imax = posic
#                            varmax = variables[imax]
#                    print(varmax)
                    self.insertar(claures)
                    
#                    print (clau1)
#                    print(clau2)
#                    print ("inserto clausula",claures)
#                    print ("Var",var)
#                    
#                    print (valores)
                
                    for j in range(imax,current):
                        valores.discard(variables[j])
                        valores.discard(-variables[j])
#                    print(imax,current)
#                    print(valores)
#                    print(restantes)
#                    print (variables[imax:current])
                    restantes.update(variables[imax:current])
#                   print(restantes)
                    del variables[imax:current]
#                    print(variables)
                    incon = True  
                    current = imax
                    break
                
                elif (varneg[0]==0 and  varpos[0]>0):
                    forced = True
                    pos = True
                    bvar = var
                
                elif (varpos[0]==0 and  varneg[0]>0):
                    forced = True
                    pos = False
                    bvar = var
                elif not forced:
                    
                    
                    if (varneg[0]>varpos[0]):
                        coef = varneg[0]/varpos[0]
                        if (coef>=best):
                            best = coef
                            pos = False
                            bvar = var
                    else:
                        coef = varpos[0]/varneg[0]
                        if (coef>=best):
                            best = coef
                            pos = True
                            bvar = var
            if not incon:
                if pos:
                    current += 1
                    valores.add(bvar)
                    variables.append(bvar)
                    restantes.discard(bvar)
                else:
                   current += 1
                   valores.add(-bvar)
                   variables.append(bvar)
                   restantes.discard(bvar) 
                
                            
        if not self.solved:
            self.solved = True
            self.solucion = True
            self.configura = valores
        
        
         
    def insertar(self,x):
        if len(x)==0:
            self.anula()
            self.listaclaus.add(x)
            self.solved=True
            self.contradict=True
        if x not in self.listaclaus:
            for y in x:
                if y in self.indices:
                    self.indices[y].add(x)
                else:
                    self.indices[y] = {x}
                if(abs(y) not in self.listavar):
                    self.listavar.add(abs(y))
            self.listaclaus.add(x)
            
    def insertaycomprueba(self,x):
        if len(x)==0:
            self.anula()
            self.listaclaus.add(x)
            self.solved=True
            self.contradict=True
        if x not in self.listaclaus:
            for y in x:
                if y in self.indices:
                    self.indices[y].add(x)
                else:
                    self.indices[y] = {x}
                if(abs(y) not in self.listavar):
                    self.listavar.add(abs(y))
            self.listaclaus.add(x)
            
    def insertayborra(self,x):
        if x not in self.listaclaus:
            h = self.borraincluidas(x)
            for y in x:
                if y in self.indices:
                    self.indices[y].add(x)
                else:
                    self.indices[y] = {x}

                if(abs(y) not in self.listavar):
                    self.listavar.add(abs(y))
            
            self.listaclaus.add(x)
            
            
    def insertaborraypoda(self,x):
        bor = []
        h = []
        insertar = True
        
        if x not in self.listaclaus:
            for z in self.listaclaus:
                if x <= z:
                    bor.append(z)
                elif z <= x:
                    return
                else:
                    for var in x:
                        if (-var in z) and (x-{var} <= z - {-var}):
                            h.append(frozenset(z-{-var}))
                            if len(z-{-var})==0:
#                                print("calusula Contradictoria ",z,x)
                                self.contradict= True
                                self.solved = True
#                                time.sleep(30)
                            elif len(z-{-var})==1:
#                                print("calusula Unitaria ",z,x)
                                self.unit.add((set(z-{-var})).pop())
                                self.unitprev.add(set((z-{-var})).pop())
                            bor.append(z)
                        elif (-var in z) and    (z - {-var} <= x-{var}):
                            h.append(frozenset(x-{var}))
                            if len(x-{-var})==0:
#                                print("calusula Contradictoria ",z,x)
                                self.contradict= True
                                self.solved = True
#                                time.sleep(30)
                            elif len(x-{-var})==1:
#                                print("calusula Unitaria ",z,x)
                                self.unit.add((x-{-var}).pop())
                                self.unitprev.add((x-{-var}).pop())
                            insertar = False
        
            if insertar:
#                print("inserto ", x)
                self.insertar(x)

                
            
            for cl in bor:
#                print("borro",cl,len(self.listaclaus))
                self.eliminar(cl)
            
            self.unitprop()
            
            for cl in h:
                
#                print("ibp",cl)
                if cl not in self.listaclaus:
#                    print("insertaar ", cl, len(self.listaclaus))
                    self.insertaborraypoda(cl)
#                    print("insertaar ", cl, len(self.listaclaus))
                    
                    
    def insertaborraypoda2(self,x):
        bor = []
        h = []
        if x not in self.listaclaus:
           for p in x:
               y = x-{p}
               lista = set()
               for q in y:
                   if q in self.indices and len(lista)>0:
                       lista.intersection_update(self.indices[q])
                   if (len(lista)>0) and p in self.indices:
                       lista1 = lista.intersection(self.indices[p])
                       for cl in lista1:
                           bor.append(cl)
                   if (len(lista)>0) and -p in self.indices:
                       lista1 = lista.intersection(self.indices[-p])
                       for cl in lista1:
                           bor.append(cl) 
                           h.append(frozenset(cl - {-p}))
                        
           for cl in bor:
                print("borro",cl,len(self.listaclaus))
                self.eliminar(cl)
            
           for cl in h:
                
                print("ibp",cl)
                if cl not in self.listaclaus:
                    self.insertaborraypoda2(cl)


            
    def borraincluidas(self,x):
        if len(x)==0:
            self.listaclaus = set()
            self.indices = dict()
            self.contradict = True
            return True
        else:
            y = list(x)
            z = y[0]
            if z in self.indices:
                inter = self.indices[z].copy()
                for i in range(1,len(y)):
                    z = y[i]
                    if z in self.indices:
                        inter.intersection_update( self.indices[z] )
                    else:
                        return False
            else:
                return False
            if (len(inter)>0):
                for z in inter:
#                    print ("borrando", z)
                    self.eliminar(z)
                    return True
            else:
                return False
                

 
                
    def calculaconjunto(self,y):
        valor = set()
        for x in self.indices[y]:
            for z in x.lista:
                valor.add(abs(z))
        for x in self.indices[-y]:
            for z in x.lista:
                valor.add(abs(z))
        return valor
    
    
    def extraeBorra(self,y):
        resultado = globalClausulas()
        for x in self.indices.get(y,[]):
            resultado.insertar(x)
        for x in self.indices.get(-y,[]):
            resultado.insertar(x)
        for x in resultado.listaclaus:
            self.eliminar(x)
        return resultado
    
    
    def split(self,y):
        con = globalClausulas()
        sin = globalClausulas()
        for cl in self.listaclaus:
            if (y not in cl) and (-y not in cl):
                sin.insertar(cl)
            else:
                con.insertar(cl)
        return (con,sin)
            
        
        
    def anadirConjunto(self,z):
        for y in z:
            self.insertar(y)
            
    def anula(self):
        self.listaclaus.clear()
        self.listavar.clear()
        self.indices.clear()


    def computevar(self):
        variables = list(self.listavar)
        valores = []
        for x in variables:
            r1 = self.indices.get(x,[])
            r2 = self.indices.get(-x,[])
            valores.append( len(r1)*len(r2) + len(r1) + len(r2))
#        print (valores)
        nvar = valores.index(max(valores))
        var = variables[nvar]
        return var
                 
    
    def eliminar(self,x):
        self.listaclaus.discard(x)
        for y in x:
            if y in self.indices:
                self.indices[y].discard(x)
                
    def eliminalista(self,x):
        for y in x:
            self.eliminar(y)
            
            
    def entorno(self,clau):
        total = set()
        for x in clau:
            if -x in self.indices:
                for h in self.indices[-x]:
                    total.add(h)
        return total
            
    def borraAprox(self,var,listapos,listaneg,th,M=3000):
        
        y = globalClausulas()
        
        r1 = self.limpiacasi(th,listapos)
        r2 = self.limpiacasi(th,listaneg)
        
        
        while len(r1)*len(r2)>M:
            cl1 = r1[-1]
            cl2 = r2[-1]
            if (cl1.lista>cl2.lista):
                r1.pop()
            else:
                r2.pop()
            
       
        
        for clau1 in r1:
            for clau2 in r2:
                clau = clau1.resolution(var,clau2)
                if (len(clau.lista)==0):
                    y.insertar(clau)
                    return y
                if (0 not in clau.lista):
                    y.insertar(clau)
        return y
        
    def marginaliza(self,var):
        
        y = globalClausulas()
        
        
        
        r1 = self.indices.get(var,set())
        r2 = self.indices.get(-var,set())
        
        for cl in self.listaclaus:
            if (not var in cl) and (not -var in cl):
                y.insertar(cl)
        
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    y.insertar(clau)
                    y.contradict=True
                    y.solved=True
                    return y
            if (0 not in clau):
                    y.insertar(clau)
        return y
    
    
    def marginalizalen(self,var,i=2):
        
        y = globalClausulas()
        
        
        
     
        
        for cl in self.listaclaus:
            if (not var in cl) and (not -var in cl):
                y.insertar(cl)
        
        
        for cl1 in self.indices.get(var,set()):
            if len(cl1)<= i:
                for cl2 in self.indices.get(-var,set()):
                    if len(cl2)<= i:
                        clau = resolution(var,cl1,cl2)
                        if (0 not in clau):
                            y.insertar(clau)
                
                        if (len(clau)==0):
                            y.contradict=True
                            y.solved=True
                            return y
                        elif (len(clau)==1):
                            nu = set(clau).pop()
                            y.unit.add(nu)
                            y.unitprev.add(nu)
                            y.unitprop()
                    
                    
                    
        return y
    
    def borraexactolim(self,listas,M=20):
        variables = set(map(abs,self.indices))
        for v in variables:
            l1 = self.indices.get(v,set())
            l2 = self.indices.get(-v,set())
            n1 = len(l1)
            n2 = len(l2)
            if ((n1*n2<=M) or (n1==1) or (n2==1)) and ((n1>0) or (n2>0)):
                listas[v] = l1.copy()
                listas[-v] = l2.copy()
                for cl in listas[v]:
                    self.eliminar(cl)
                for cl in listas[-v]:
                    self.eliminar(cl)
                if (n1>0):
                    self.indices.pop(v)
                if (n2>0):
                    self.indices.pop(-v)
                
                
                
                for x in  list(itertools.product(listas[v],listas[-v])):
                    clau = resolution(v,x[0],x[1])
                    if (0 not in clau):
                        self.insertar(clau)
                        self.refer[clau] = self.refer.get(x[0],set()).union(self.refer.get(x[1],set()))
#                        if not sol.intersection(clau.union(self.refer[clau])):
#                            print("problema 6")
                        if not clau:
                            self.contradict=True
                            self.apren = self.refer[clau]
                            self.totalapren.add(frozenset(self.refer[clau]))

                            return [v]
                return [v] + self.borraexactolim(listas,M)   
        return []
                            
                        
                
                
    
    
    def eliminavar(self,var):
        l1 = self.indices.get(var,set())
        l2 = self.indices.get(-var,set())
        anadir = []
        
        for x in  list(itertools.product(l1,l2)):
            clau = resolution(var,x[0],x[1])
            if (0 not in clau):
                anadir.append(clau)
                
        lista = l1.union(l2)
        
        for cl in lista:
            self.eliminar(cl)
        for cl in anadir:
            self.insertar(cl)
                
            
            
        
    
    def marginalizaapr2(self,var,bloquedas,unitarias,M=3):
        
        y = globalClausulas()
        z = globalClausulas()
        
        anadir = []
        
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            
        
        
           
 
    
        
        
        
        
       

        r1 = self.indices.get(var,set())
        r2 = self.indices.get(-var,set())            
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    y.insertar(clau)
                    y.contradict=True
                    y.solved=True
                    return 
            if (0 not in clau):
                if (len(clau)==1):
                    print("unitaria ", clau)
                    p = set(clau).pop()
                    unitarias.add(p)
                elif (len(clau)<=M):
                    y.insertar(clau)
        return y
    
    
    
    
    def marginalizaapr(self,var,th,bloquedas,unitarias,otras,M=2):
        
        y = globalClausulas()
        z = globalClausulas()
        
        
 
        
        
        
        
        for cl in self.listaclaus:
            if (not var in cl) and (not -var in cl):
                y.insertar(cl)
            else:
                if (not z in bloquedas):
                    z.insertar(cl)

        z.limpiarec(th)

        r1 = z.indices.get(var,set())
        r2 = z.indices.get(-var,set())            
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    y.insertar(clau)
                    y.contradict=True
                    y.solved=True
                    return 
            if (0 not in clau):
                if (len(clau)==1):
                    print("unitaria ", clau)
                    p = set(clau).pop()
                    unitarias.add(p)
                elif (len(clau)<=M):
                    otras.insertar(clau)
                y.insertar(clau)
                
        y.limpiarec(0.0)
        return y
    
    def borraExactoCasi(self,var,listapos,listaneg,th):
        
        y = globalClausulas()
        
        
        
        r1 = self.limpiacasi(th,listapos)
        r2 = self.limpiacasi(th,listaneg)
        
        
        for x in  list(itertools.product(r1,r2)):
            clau = resolution(var,x[0],x[1])
            
                
            if (len(clau)==0):
                    y.insertar(clau)
                    return y
            if (0 not in clau):
                    y.insertar(clau)
        return y
        
   
    
    
    def bloqueo(self,c):
        hl = set(map(lambda x: -x,c))
        for x in c:
            bloque = True
            if (-x in self.indices):
                for y in self.indices[-x]:
                    if len( y  & hl)==1:
                        bloque = False 
                        break
            if bloque:
                break
        return bloque
    
 
        
    
    def bloqueogen(self,c,M=100):
        
        h = globalClausulas()
        
        ent = self.entorno(c)
        
        h.anadirConjunto(ent)
        var = len(self.listavar)+2
        
        lista = set(map(abs,c))
        
        cl = frozenset(c | {var})
        
        h.insertar(cl)
        
#        print(len(h.listaclaus))
        
        for v in lista:
            h.eliminavar(v)
            t = h.indices.get(var,set())
        
            if len(t)== 0:
                return True
            if len(h.listaclaus)>M:
                return False
            
        h.limpia(0.0)
        
        t = h.indices.get(var,set())
        
        if len(t)== 0:
            return True
        else:
            return False
            
        
        
        
        
        
        for x in c:
            bloque = True
            if (-x in self.indices):
                for y in self.indices[-x]:
                    if len( y  & hl)==1:
                        bloque = False 
                        break
            if bloque:
                break
        return bloque
    

    def eliminarbloqueadas(self):
        bloqueadas = set()
        for c in self.listaclaus:
            if self.bloqueo(c):
                bloqueadas.add(c)
                print ("bloqueada ",c)
        for h in bloqueadas:
            self.eliminar(h)
            print ("eliminada ",h)
        if (len(bloqueadas)>1):
            return bloqueadas | self.eliminarbloqueadas()
        else:
            return bloqueadas
        
    def calcularbloqueadas(self):
        bloqueadas = set()
        for c in self.listaclaus:
            if self.bloqueo(c):
                bloqueadas.add(c)
                print ("bloqueada ",c)
        if (bloqueadas):
            for h in bloqueadas:
                self.eliminar(h)
                print ("eliminada ",h)
            bloqueadas = bloqueadas | self.eliminarbloqueadas()
            for h in bloqueadas:
                self.insertar(h)
            return bloqueadas
        else:
            return bloqueadas
        
    def calculartodasbloqueadas(self):
        bloqueadas = set()
        for c in self.listaclaus:
#            print (c)
            if self.bloqueogen(c):
                bloqueadas.add(c)
                print ("bloqueada ",c)
        return bloqueadas
                
    def poda(self):
#        print("entro en poda")
        
        lista = self.listavar.copy()
        
        for var in lista:
            self.podavar(var)
#        print("salgo de poda")
    
        
    def podaylimpia(self):
        y = []
        borr = []
#        print("entro en poda 2")
        lista = sorted(self.listaclaus,key = lambda x: len(x))
#        print("ordenadas")
        
        for i in range(len(lista)):
            clau1 = lista[i]
            for j in range(i+1,len(lista)):

                clau2 = lista[j]
                claudif = set(clau1-clau2)
                if (len(claudif) ==0):
                    borr.append(clau2)
                elif (len(claudif) ==1):
                    var = claudif.pop()
                    if -var in clau2:
                        y.append(frozenset(clau2-{var}))
                        borr.append(clau2)
                        
        for clau in borr:
            self.eliminar(clau)
        
        for clau in y:
#            print("original ibp",clau,len(self.listaclaus))
            self.insertaborraypoda(clau)
#            print("original ibp",clau,len(self.listaclaus))

#                
#        print("salgo de poda 2")

    
    def podavar(self,var):
#        print("podando",var)
        y = []
        if(var in self.indices and -var in self.indices):
            listapos = self.indices[var]
            listaneg = self.indices[-var]
            for clau1 in listapos:
                for clau2 in listaneg:
                    if (clau1 - {var} <= clau2 -{-var}):
                        y.append(frozenset(clau2-{-var}))
#                        print ("podo con", clau2-{-var})
                    elif  (clau2 - {-var} <= clau1 -{var}): 
                        y.append(frozenset(clau1-{var}))
#                        print ("podo con", clau1-{var})
        for clau in y:
            print("original ibp",clau,len(self.listaclaus))
            if (len(clau)>1):
                self.insertaborraypoda(clau)
            elif len(clau)==1:
                self.unit.add(set(clau).pop())
                self.unitprev.add(set(clau).pop())
                self.unitprop()
#                self.insertar(clau)
            else:
                self.solved=True
                self.contradict=True
#                self.insertar(clau)

            
    def podavar2(self,var):
        print("podando",var)
        y = []
        borra = []
        if(var in self.indices and -var in self.indices):
            listapos = self.indices[var]
            listaneg = self.indices[-var]
            for clau1 in listapos:
                for clau2 in listaneg:
                    if (clau1 - {var} <= clau2 -{-var}):
                        borra.append(clau2)
                        y.append(clau2-{-var})
#                        print ("podo con", clau2-{-var})
                    elif  (clau2 - {-var} <= clau1 -{var}): 
                        y.append(clau1-{var})
                        borra.append(clau1)
#                        print ("podo con", clau1-{var})
        for clau in y:
            self.insertar(clau)
        for clau in borra:
            self.eliminar(clau)
    
    def satura(self,M=3,N=500000):
        z = set()
        for var in self.listavar:
            y = self.saturaVar(var,M)
            z.update(y)
        added =0
        while added<N and len(z)>0:
            clau = z.pop()
            self.insertayborra(clau)
            added += 1
            y = self.calculaNuevas(clau,M)
            z.update(y)
            print("total clau", len(self.listaclaus), added)
            print("cola ", len(z))
#        while len(z)>0:
#            clau = z.pop()
#            self.insertayborra(clau)
        print("total clau", len(self.listaclaus))
            
    def calculaNuevas(self,clau1,M=10):
        y = set()
        for var in clau1:
            for clau2 in self.indices[-var]:
                if (len(clau2)<=M+1):
                    clau = resolution(abs(var),clau1,clau2)
                    y.add(clau)
                    if (len(clau)==0):
                        self.solved=True
                        self.contradict=True
                        return y
                    
        return y
    
    def saturaVar(self,var,M=10):
        
        listapos = self.indices[var]
        listaneg = self.indices[-var]
        
        y = set()
        
        for clau1 in listapos:
            for clau2 in listaneg:
                if ((len(clau1)<=(M+1)) and len(clau2)<=(M+1)):
                    clau = resolution(var,clau1,clau2)
                    if (len(clau)==0):
                        y.insertar(clau)
                        self.solved=True
                        self.contradict=True
                        return
                    if (0 not in clau and len(clau)<=M):
                        y.add(clau)
        return y
    
    def seleccionaVar(self,x):
        self.listavar.update(x)
        
        
    def limpia(self,th):
        if(len(self.listaclaus)<2):
            return
        
        nuevas = list(self.listaclaus)
        nuevas.sort(key=lambda x: len(x))
        i1 = 0
        i2 = len(nuevas)-1 
        
        while (i1<(len(nuevas)-1)  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if casicontenida(cl1,cl2,th):
                del nuevas[i2]
                self.eliminar(cl2)
            i2=i2-1
            if (i2 ==i1):
                i1=i1+1
                i2 = len(nuevas)-1 
                
                
    def limpiacasi(self,th,conjunto):
        
        nuevas = list(conjunto)
        nuevas.sort(key=lambda x: len(x))
        i1 = 0
        i2 = 1
        
       
        while (i1<(len(nuevas)-1)  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if casicontenida(cl1,cl2,th):
                if (cl1<=cl2):
                    conjunto.discard(cl2)
                del nuevas[i2]
                
            i2=i2-1
            if (i2 ==i1):
                i1=i1+1
                i2 = len(nuevas)-1 
         
           
        return nuevas
    
    
    def limpiatama(self,M=150):
        bor=[]
        x = self.listaclaus
        for y in x:
            if len(y)>M:
                bor.append(y)
        for y in bor:
            self.eliminar(y)
#            print("elimino ",len(y.lista))
            
    def limpianum(self,M=1000):
        bor=[]
        x = list(self.listaclaus)
        x.sort(key=lambda z: len(z))
        for y in x[M:]:
            self.eliminar(y)
#            print("elimino ",len(y.lista))
        
    def limpiarec(self,th,M=200):
         
        
        if len(self.listaclaus)<M :
            self.limpia(th)
            return
        
        
        
        valores = dict()
        
        for x in self.listavar:
            if (x in self.indices):
                l1 = len(self.indices[x])
            else:
                l1 = 0
            if (-x in self.indices):
                l2 = len(self.indices[-x])
            else:
                l2 = 0
            
            valores[x] = l1 * l2 -  l1 - l2 + len(self.listaclaus)
           
        
        
        
        var = max(valores.keys(), key=(lambda k: valores[k]))

        listano = globalClausulas()
        listap = globalClausulas()
        listanop = globalClausulas()
        
        if var in self.indices:
            conj1 = self.indices[var]
        else:
            conj1 = set()
        
        if -var in self.indices:
            conj2 = self.indices[-var]
        else:
            conj2 = set()
            
            
        listap.anadirConjunto(conj1)
        listanop.anadirConjunto(conj2)
        listano.anadirConjunto(self.listaclaus- conj1 - conj2 )
        
        if( len(listano.listaclaus) < 0.8 * len(self.listaclaus)):
                listano.limpiarec(th,M)
        else:
                listano.limpia(th)
        if(len(listap.listaclaus) < 0.8 * len(self.listaclaus)):    
                listap.limpiarecdos(listano,th,M)
        else:
                listap.limpia(th)
                listap.limpiacruz(listano,th)
                
        if(len(listanop.listaclaus) < 0.8 * len(self.listaclaus)):    
                listanop.limpiarecdos(listano,th,M)
        else:
                listanop.limpia(th)
                listanop.limpiacruz(listano,th)   
                
        self.anula()
        self.combina(listano)
        self.combina(listap)
        self.combina(listanop)
        
           
 
            
    def combina(self,conjunto):
#        self.listavar.update(conjunto.listavar)
#        self.listaclaus.update(conjunto.listaclaus)
#        for x in conjunto.indices:
#            if x in self.indices:
#                self.indices[x].update(conjunto.indices[x])
#            else:
#                self.indices[x] = conjunto.indices[x].copy()
        for x in conjunto.listaclaus:
            self.insertar(x)
            self.limpiarec(0.0)
                           
    
            
           
    def limpiarecdos(self,aux,th,M):
       
        
        if len(self.listaclaus)<M :
            self.limpia(th)
            self.limpiacruz(aux,th)
            return
        
        valores = dict()
        for x in self.listavar:
            if (x in self.indices):
                l1 = len(self.indices[x])
            else:
                l1 = 0
            if (-x in self.indices):
                l2 = len(self.indices[-x])
            else:
                l2 = 0
            
            valores[x] = l1 * l2 -  l1 - l2 + len(self.listaclaus)
        
        
        
        var = max(valores.keys(), key=(lambda k: valores[k]))

        listano = globalClausulas()
        listap = globalClausulas()
        listanop = globalClausulas()
        
        if var in self.indices:
            conj1 = self.indices[var]
        else:
            conj1 = set()
        
        if -var in self.indices:
            conj2 = self.indices[-var]
        else:
            conj2 = set()
            
            
        listap.anadirConjunto(conj1)
        listanop.anadirConjunto(conj2)
        listano.anadirConjunto(self.listaclaus- conj1 - conj2 )
        
        
        auxno = globalClausulas()
        auxp = globalClausulas()
        auxnop = globalClausulas()
        
        if var in aux.indices:
            conj1 = aux.indices[var]
        else:
            conj1 = set()
        
        if -var in aux.indices:
            conj2 = aux.indices[-var]
        else:
            conj2 = set()
        
        
        auxp.anadirConjunto(conj1)
        auxnop.anadirConjunto(conj1)
        auxno.anadirConjunto(auxno.listavar- conj1 - conj2 )
        
        auxp.combina(auxno)
        auxp.combina(listano)
                    
        auxnop.combina(auxno)
        auxnop.combina(listano)
        
        if( len(listano.listaclaus) < 0.8 * len(self.listaclaus)):
                listano.limpiarecdos(auxno,th,M)
        else:
                listano.limpia(th)
                listano.limpiacruz(auxno,th)
        if(len(listap.listaclaus) < 0.8 * len(self.listaclaus)):    
                listap.limpiarecdos(auxp,th,M)
        else:
                listap.limpia(th)
                listap.limpiacruz(auxp,th)
                
        if(len(listanop.listaclaus) < 0.8 * len(self.listaclaus)):    
                listanop.limpiarecdos(auxnop,th,M)
        else:
                listanop.limpia(th)
                listanop.limpiacruz(auxnop,th)   
                
        self.anula()
        self.combina(listano)
        self.combina(listap)
        self.combina(listanop)
        
        # print(len(clausulas))
       
                    
            
     
    def limpiacruz(self,aux,th):
        
        borra = []
        for x in self.listaclaus:
            for y in aux.listaclaus:
                if casicontenida(y,x,th):
                    borra.append(x)
                    break
        
        self.eliminalista(borra)  
        

    
#print(SeleccionarArchivo("ArchivosSAT.txt"))


# info.satura(4)
#print("fin de satura")
# info.busca()
# info = leeArchivoSet('SAT_V153C408.cnf')



#info = leeArchivoSet('SAT_V144C560.cnf')

