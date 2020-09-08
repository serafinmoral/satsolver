# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os


class Clausulafs:
    def __init__(self,x):
        self.lista = frozenset(x)

    def incompatible(self,x):
        if len(self.lista) <= len(x.lista):
            x1 = self
            x2 = x
        else:
            x1 = x
            x2 = self
        for y in x1.lista:
            if -y in x2.lista:
                return True
        return False
    
         
    def pertenece(self, x):
       return x in self.lista
    
    
    def reduce(self,x):
        h = []
        for y in self.lista:
            if y in x:
                h = [0]
                break
            elif -y not in x:
                h.append(y)
        return Clausulafs(h)
            
    def contenida(self,x):
        return self.lista.issubset(x.lista)
    
    
    def casicontenida(self,x,th,method=1):
        z=0
        
        if self.incompatible(x):
            return False
        
        if method == 0: 
            z = len(self.lista - x.lista)/len(self.lista)
        elif method == 1:
            z = len(self.lista - x.lista)/len(self.lista |x.lista)
        elif method == 3:
            z = len(self.lista - x.lista)
        
        if z <= th:
            return True
        else:
            return False
        
       
            
    def resolution(self,varb,clau2):
        
        result = self.lista.union(clau2.lista) - {varb,-varb}
        
        for i in result:
            if (i>0) and (-i in result):
                result = {0}
                
        return (Clausulafs(result))
                
        
        
class conjuntoClausulas:
    def __init__(self):
         self.listavar = set()
         self.listaclaus = set()
         self.indices = dict()
         self.contradict = False
         
         
    def restringe(self,x):
        y = conjuntoClausulas()
        for cl in self.listaclaus:
            if (x not in cl.lista) and (-x not in cl.lista):
                y.insertar(cl)
            elif -x in cl.lista:
                cl2 = Clausulafs(cl.lista-{-x})
                if (len(cl2.lista)>0):
                    y.insertar(cl2)
                else:
                    y.listaclaus.clear()
                    y.insertar(cl2)
                    y.contradict = True
        return y
        
         
    def insertar(self,x):
            for y in x.lista:
                if y in self.indices:
                    self.indices[y].add(x)
                else:
                    self.indices[y] = set([x])
                if(abs(y) not in self.listavar):
                    self.listavar.add(abs(y))
            self.listaclaus.add(x)
            
    def combina(self,conjunto):
        self.listavar.update(conjunto.listavar)
        self.listaclaus.update(conjunto.listaclaus)
        for x in conjunto.indices:
            if x in self.indices:
                self.indices[x].update(conjunto.indices[x])
            else:
                self.indices[x] = conjunto.indices[x].copy()
        
        
    def anadirConjunto(self,z):
        for y in z:
            self.insertar(y)
            
    def anula(self):
        self.listaclaus.clear()
        self.listavar.clear()
        self.indices.clear()


    def computevar(self):
        valores = [0]*len(self.listavar)
        for x in self.listavar:
            valores[x-1] = len(self.indices[x])*len(self.indices[-x]) + len(self.indices[x]) + len(self.indices[-x])
        var = index(max(valores))+1
        return var
                 
    
    def eliminar(self,x):
        self.listaclaus.discard(x)
        for y in x.lista:
                self.indices[y].discard(x)
                
    def eliminalista(self,x):
        for y in x:
            self.eliminar(y)
            
    def borraAprox(self,var,listapos,listaneg,th,M=3000):
        
        y = conjuntoClausulas()
        
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
        
    def borraExactoCasi(self,var,listapos,listaneg,th):
        
        y = conjuntoClausulas()
        
        r1 = self.limpiacasi(th,listapos)
        r2 = self.limpiacasi(th,listaneg)
        
        for clau1 in r1:
            for clau2 in r2:
                clau = clau1.resolution(var,clau2)
                if (len(clau.lista)==0):
                    y.insertar(clau)
                    return y
                if (0 not in clau.lista):
                    y.insertar(clau)
        return y
        
        
    def borraExacto(self,var,listapos,listaneg):
        
        y = conjuntoClausulas()
        
        for clau1 in listapos:
            for clau2 in listaneg:
                clau = clau1.resolution(var,clau2)
                if (len(clau.lista)==0):
                    y.insertar(clau)
                    return y
                if (0 not in clau.lista):
                    y.insertar(clau)
        return y
    
    def seleccionaVar(self,x):
        self.listavar.update(x)
        
        
    def limpia(self,th):
        if(len(self.listaclaus)<2):
            return
        
        nuevas = list(self.listaclaus)
        nuevas.sort(key=lambda x: len(x.lista))
        i1 = 0
        i2 = 1
        
        while (i1<(len(nuevas)-1)  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if cl1.casicontenida(cl2,th):
                del nuevas[i2]
                self.eliminar(cl2)
            i2=i2-1
            if (i2 ==i1):
                i1=i1+1
                i2 = len(nuevas)-1 
                
                
    def limpiacasi(self,th,conjunto):
        
        
        nuevas = list(conjunto)
        nuevas.sort(key=lambda x: len(x.lista))
        i1 = 0
        i2 = 1
        
       
        while (i1<(len(nuevas)-1)  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if cl1.casicontenida(cl2,th):
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
            if len(y.lista)>M:
                bor.append(y)
        for y in bor:
            self.eliminar(y)
#            print("elimino ",len(y.lista))
            
    def limpianum(self,M=1000):
        x = list(self.listaclaus)
        x.sort(key=lambda z: len(z.lista))
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

        listano = conjuntoClausulas()
        listap = conjuntoClausulas()
        listanop = conjuntoClausulas()
        
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

        listano = conjuntoClausulas()
        listap = conjuntoClausulas()
        listanop = conjuntoClausulas()
        
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
        
        
        auxno = conjuntoClausulas()
        auxp = conjuntoClausulas()
        auxnop = conjuntoClausulas()
        
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
                if y.casicontenida(x,th):
                    borra.append(x)
                    break
        
        self.eliminalista(borra)  
        
         
        
            
        
class listaClausulas:
    def __init__(self,n):
        self.conjunto = []
        self.positivas = []
        self.negativas = []
        self.nvar = n
        for i in range(n):
            self.positivas.append([])
            self.negativas.append([])
        
    def insertar(self,x):
        self.conjunto.append(x)
        n = len(self.conjunto)-1
        for y in x.lista:
            if (y>0):
                self.positivas[y-1].append(n)
            else:
                self.negativas[-y-1].append(n)
        return n
    
                
class solveSATBorradoSet:    
    def __init__(self,x):
        self.listOriginal=[]
        self.method = 0
        self.limit = 0
        self.solucion = False
        self.solved = False    
        self.varinorder = dict()
        self.posorder = dict()
        self.clausulasborr = dict()
        self.conjuntoclau = x
        self.ordenbo = []
        self.configura = []
        self.resultado=set()
    
        for z in x.listaclaus:
           self.listOriginal.append(z.lista)
            
        for y in x.listavar:
            self.clausulasborr[y] = {}
            self.clausulasborr[-y] = {}
        
         
    def computeCompl(self,y,i):
        c = 0
        if (i==0):
            x1 = len(self.conjuntoclau.indices[y])
            x2  = len(self.conjuntoclau.indices[-y])
            c= x1*x2 - x1 -x2
        return c
    
    def siguiente(self,i,noborrad):
        y = noborrad[0]
        best = self.computeCompl(y,i)
        nbest = y
        for y in noborrad[1:]:
            z = self.computeCompl(y,i)
            if(z<best) :
                nbest=y
                best=z
        return nbest
    
    @staticmethod
    def calculavalor(valores,conjunto):
        for x in conjunto:
            if len(valores.intersection(x.lista))==0:
                return [True,x]
        return [False]
                
    
    def busca(self):
        valores = set()
        n = len(self.ordenbo)
        current = n-1
        
        while not (self.solved):
            print(current)
#            print(current)
            var = self.ordenbo[current]
            varpos = solveSATBorradoSet.calculavalor(valores,self.clausulasborr[var])
            varneg = solveSATBorradoSet.calculavalor(valores,self.clausulasborr[-var])
#            print("Valores:",valores)
#            print("Variable:",var)
#            print("Afirmadas:")
#            for i in self.clausulasborr[var]:
#                print(i.lista)
#            print("Negadas:")
#            for i in self.clausulasborr[-var]:
#                print(i.lista)
#            print(varpos)
#            print(varneg)
#            r=int(input("Hola Mundo"))
            if (varpos[0] and varneg[0]):
                clau1 = varpos[1]
                clau2 = varneg[1]
#                print(clau1.lista)
#                print(clau2.lista)
#                print(var)
                claures = clau1.resolution(var,clau2)
                if(len(claures.lista)==0):
                    self.solved = True
                    
                imin = n-1
#                print(claures.lista)
                for y in claures.lista:
                    z = abs(y)
                    pos = self.varinorder[z]
                    if (pos>imin):
                        imin = pos
                varmin = self.ordenbo[imin]
                if (varmin in claures.lista):
                    self.clausulasborr[varmin].add(claures)
                else:
                    self.clausulasborr[-varmin].add(claures)
                for j in range(imin,current+1):
                    valores.discard(self.ordenbo[j])
                    valores.discard(-self.ordenbo[j])
                    
                current = imin
                
            elif varpos[0] and not varneg[0]:
                current -= 1
                valores.add(var)
            elif varneg[0] and not varpos[0]:
                current -= 1
                valores.add(-var)
            else:
                valores.add(var)
                current -= 1
#                xpos = 1.0
#                xneg = 1.0
#                p=int(input("Nada--> "))
#                for i in range(current-1):
#                    var2 = self.ordenbo[i]
#                    l1 = self.clausulasborr[var2]
#                    l2 = self.clausulasborr[-var2]
#                    for z in l1:
#                        z = z.reduce(valores)
#                        if var in z.lista:
##                            xpos += 1
#                            xneg = xneg*(2**(len(z.lista)-1)-1)/2**(len(z.lista)-1)
#                        elif -var in z.lista:
#                            xpos = xpos*(2**(len(z.lista)-1)-1)/2**(len(z.lista)-1)
##                            xneg += 1
#                    for z in l2:
#                        z = z.reduce(valores)
#                        if var in z.lista:
##                            xpos += 1
#                            xneg = xneg*(2**(len(z.lista)-1)-1)/2**(len(z.lista)-1)
#                        elif -var in z.lista:
#                            xpos =xpos* (2**(len(z.lista)-1)-1)/2**(len(z.lista)-1)
##                            xneg += 1       
#                current -= 1
#                print(xpos,xneg)
#                if (xpos>xneg):
#                    valores.add(var)
#                else:
#                    valores.add(-var)
                            
            if (current == -1):
                self.solved = True
                self.solucion = True
                self.configura = valores
        self.resultado=valores
        i = 0
        for c in self.listOriginal:
            i = i + 1
            if len(c & valores)==0:
                print ("ERRRORORORORORORRRRRRRRRRRRRRR",i,c)
            else:
                print(i,c & valores)
        print(valores)
                
    def eliminaListas(self,lista1,lista2,noborrad):
        
        for y in lista1:
            for z in y.lista:
                if (z in noborrad) or (-z in noborrad):
                        self.conjuntoclau.indices[z].remove(y)
                        

        for y in lista2:
            for z in y.lista:
                if (z in noborrad) or (-z in noborrad):
                        self.conjuntoclau.indices[z].remove(y)     
                
    def borra(self):
        current=1
        noborrad = list(self.conjuntoclau.listavar)
        while len(noborrad)>0 and not self.solved:
            print (current)
            varb = self.siguiente(0,noborrad)
            print ("Borrando variable ", varb)
            self.ordenbo.append(varb)
            self.varinorder[varb] = current-1
            current = current +1
            noborrad.remove(varb)
            
            # self.listapos[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # self.listaneg[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # print(len(self.listapos[varb]))
            # self.limpiaordennum(self.listapos[varb])
            # print(len(self.listapos[varb]))
            # print(len(self.listaneg[varb]))
            # self.limpiaordennum(self.listaneg[varb])
            # print(len(self.listaneg[varb]))

            self.clausulasborr[varb] = self.conjuntoclau.indices[varb]
            self.clausulasborr[-varb] = self.conjuntoclau.indices[-varb]
            
            th = 0.09

            
            # for x in self.listapos[varb]:
            #    print (x, self.claus.conjunto[x].lista)
            
#            nuevas = self.conjuntoclau.borraAprox(varb,self.clausulasborr[varb],self.clausulasborr[-varb],th)
            nuevas = self.conjuntoclau.borraExactoCasi(varb,self.clausulasborr[varb],self.clausulasborr[-varb],th)

            # for x in nuevas:
            #   print (x.lista)
            print("tamaño sin limpiar" ,len(nuevas.listaclaus))
            print("ordenadas")
                
#            nuevas.limpiatama(18)
            nuevas.limpianum(5000)
            nuevas.limpiarec(th)
            # solveSATBorrado.limpiarec(nuevas,noborrad,posiciones)
            print("tamaño después de limpiar" ,len(nuevas.listaclaus))
            
            
            
            self.eliminaListas(self.clausulasborr[varb],self.clausulasborr[-varb],noborrad)
            
            
#            h = list(nuevas.listaclaus)
#            
#            h.sort(key=lambda x: len(x.lista))
          
#            i=0
            for x in nuevas.listaclaus:
#                i+=1
                if (len(x.lista)==0):
                    self.solved = True
                    self.solution = False
                elif (0 not in x.lista):
                    self.conjuntoclau.insertar(x)
#                if (i==600):
#                    break
                    
  
             
            
class solveSATBorrado:
    def __init__(self,x):
        self.nvar = x.nvar
        self.ordenbo = []
        self.varinorder = [0]*x.nvar
        self.posorder = []
        self.negorder = []
        self.claus = x
        
        self.listapos = []
        self.listaneg = []
        self.method = 0
        self.limit = 0
        self.solucion = 0
        self.solved = False
        
        
        for i in range(self.nvar):
            self.listapos.append(x.positivas[i].copy())
            self.listaneg.append(x.negativas[i].copy())
        
        
    def siguiente(self,i,noborrad):
        y = noborrad[0]
        best = self.computeCompl(y,i)
        nbest = y
        for y in noborrad[1:]:
            z = self.computeCompl(y,i)
            if(z<best) :
                nbest=y
                best=z
        return nbest
               

    def borraExacto(self,varb,listapos,listaneg):
        result = []
        
        for i1 in listapos:
            for i2 in listaneg:
                clau1 = self.claus.conjunto[i1]
                clau2 = self.claus.conjunto[i2]
                clau = clau1.resolution(varb,clau2)
                if (len(clau.lista)==0):
                    result.append(clau)
                    return result
                if (clau.lista[0]!=0):
                    result.append(clau)
                
                
        return result
        
    def computeCompl(self,y,i):
        c = 0
        if (i==0):
            x1 = len(self.listapos[y])
            x2  = len(self.listaneg[y])
            c= x1*x2 - x1 -x2
        return c
    
    
    def eliminaListas(self,varb,lista1,lista2):
        for y in lista1:
            cl = self.claus.conjunto[y]
            for z in cl.lista:
                if z != varb:
                    if (z>0):
                        self.elimina(y,self.listapos[z-1])
                    else:
                        self.elimina(y,self.listaneg[-z-1])
                
                        
                        
        for y in lista2:
            cl = self.claus.conjunto[y]
            for z in cl.lista:
                if z != -varb:
                    if (z>0):
                        self.elimina(y,self.listapos[z-1])
                    elif (z<0):
                        self.elimina(y,self.listaneg[-z-1])
               
                        
    
    
    
    @staticmethod                   
    def elimina(x,lista):
        j = len(lista)-1
        i = 0 
         
        if ((j<0) or (lista[0])>x):
             return False
        if(lista[j]<x):
             return False
        
        end = False
        while (not end) :
            k = (i+j)//2
            if (lista[k] == x) :
                del lista[k]
                return True
            elif (x >  lista[k]):
               i=k+1
            else:
                j=k
            if (i>j):
                return False
        
                    
    @staticmethod
    def limpia(nuevas):
        if(len(nuevas)<2):
            return
        
        i1= 0
        i2 =1
        
        while((i1<(len(nuevas)-1)) and (i2<(len(nuevas)))  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if cl1.contenida(cl2):
                del nuevas[i2]
            elif cl2.contenida(cl1):
                del nuevas[i1]
                i2 = i1+1
            else:
                i2 = i2+1
            if (i2 >= len(nuevas)):
                i1=i1+1
                i2 = i1+1
        
    @staticmethod
    def limpiaorden(nuevas):
        if(len(nuevas)<2):
            return
        
        i1=  0
        i2 = 1
        
        while (i1<(len(nuevas)-1)  ):
            cl1 = nuevas[i1]
            cl2 = nuevas[i2]
            if cl1.contenida(cl2):
                del nuevas[i2]
            i2=i2-1
            if (i2 ==i1):
                i1=i1+1
                i2 = len(nuevas)-1 
                
                
    @staticmethod
    def limpiacruz(nuevas,aux):
        
        i1=  0
        i2 = 0
        
        while (i1< len(nuevas) and i2 < len(aux)  ):
            cl1 = nuevas[i1]
            cl2 = aux[i2]
            if cl2.contenida(cl1):
                del nuevas[i1]
                i2=0
            else:
                i2 = i2+1
                if(i2==len(aux)):
                    i1=i1+1
                    i2=0
                
                
                
    @staticmethod           
    def limpiarec(clausulas,noborra,posiciones,M=500):
       
        
        if len(clausulas)<M :
            solveSATBorrado.limpiaorden(clausulas)
            return
        
        totalpos = [0]*len(noborra)
        totalneg = [0]*len(noborra)
        
        for x in clausulas:
            
            y = x.lista
            for z in y:
                if(z>0):
                    totalpos[posiciones[z-1]] = totalpos[posiciones[z-1]] +1 
                elif (z<0):
                    totalneg[posiciones[-z-1]]  = totalneg[posiciones[-z-1]] +1 
        
        maxv = totalpos[0]*totalneg[0] - totalpos[0] - totalneg[0] + len(clausulas)
        imax = 0
        
        for i in range(1,len(totalpos)):
            if (totalpos[i]*totalneg[i] - totalpos[i] - totalneg[i] + len(clausulas))> maxv:
                maxv = totalpos[i]*totalneg[i] - totalpos[i] - totalneg[i] + len(clausulas)
                imax = i
        
        var = noborra[imax]
        
        if (maxv == 0):
            solveSATBorrado.limpiaorden(clausulas)
            return
        else:
            listap = []
            listanop = []
            listano = []
            for x in clausulas:
                if (var+1) in x.lista:
                    listap.append(x)
                elif (-var-1) in x.lista:
                    listanop.append(x)
                else:
                    listano.append(x)
            if( len(listano) < 0.8 * len(clausulas)):
                solveSATBorrado.limpiarec(listano,noborra,posiciones)
            else:
                solveSATBorrado.limpiaorden(listano)
            if( len(listap) < 0.8 * len(clausulas)):    
                solveSATBorrado.limpiarecdos(listap,listano,noborra,posiciones)
            else:
                solveSATBorrado.limpiaorden(listap)
                solveSATBorrado.limpiacruz(listap,listano)
                
            if( len(listanop) < 0.8 * len(clausulas)):    
                solveSATBorrado.limpiarecdos(listanop,listano,noborra,posiciones)
            else:
                solveSATBorrado.limpiaorden(listanop)
                solveSATBorrado.limpiacruz(listanop,listano)            
            clausulas.clear()
            clausulas.extend(listano)
            clausulas.extend(listap)
            clausulas.extend(listanop)
 
            
            
    
            
    @staticmethod           
    def limpiarecdos(clausulas,aux,noborra,posiciones,M=500):
       
        
        if len(clausulas)<M :
            solveSATBorrado.limpiaorden(clausulas)
            solveSATBorrado.limpiacruz(clausulas,aux)
            return
        
        totalpos = [0]*len(noborra)
        totalneg = [0]*len(noborra)
        for x in clausulas:  
            y = x.lista
            for z in y:
                if(z>0):
                    totalpos[posiciones[z-1]] = totalpos[posiciones[z-1]] +1 
                elif (z<0):
                    totalneg[posiciones[-z-1]]  = totalneg[posiciones[-z-1]] +1 
        
        maxv = totalpos[0]*totalneg[0]- totalpos[0] - totalneg[0] + len(clausulas)
        imax = 0
        
        for i in range(1,len(totalpos)):
            if (totalpos[i]*totalneg[i] - totalpos[i] - totalneg[i] + len(clausulas)) > maxv:
                maxv = totalpos[i]*totalneg[i]- totalpos[i] - totalneg[i] + len(clausulas)
                imax = i
            
        
        var = noborra[imax]
        
        # print(len(clausulas))
        if (maxv == 0):
            # print ("no recursion")
            solveSATBorrado.limpiaorden(clausulas)
            solveSATBorrado.limpiacruz(clausulas,aux)
            return
        else:
            # print ("si recursion")
            listap = []
            listanop = []
            listano = []
            for x in clausulas:
                if var+1 in x.lista:
                    listap.append(x)
                elif -var-1 in x.lista:
                    listanop.append(x)
                else:
                    listano.append(x)
            auxp = []
            auxnop = []
            auxno = []
            for x in aux:
                if (var+1) in x.lista:
                    auxp.append(x)
                elif (-var-1) in x.lista:
                    auxnop.append(x)
                else:
                    auxno.append(x)   
                    
            auxp.extend(auxno)
            auxp.extend(listano)
                    
            auxnop.extend(auxno)
            auxnop.extend(listano)
                    
            
            if( len(listano) < 0.8 * len(clausulas)):
                solveSATBorrado.limpiarecdos(listano,auxno,noborra,posiciones)
            else:
                solveSATBorrado.limpiaorden(listano)
            if( len(listap) < 0.8 * len(clausulas)):    
                solveSATBorrado.limpiarecdos(listap,auxp,noborra,posiciones)
            else:
                solveSATBorrado.limpiaorden(listap)
                solveSATBorrado.limpiacruz(listap,auxp)
                
            if( len(listanop) < 0.8 * len(clausulas)):    
                solveSATBorrado.limpiarecdos(listanop,auxnop,noborra,posiciones)
            else:
                solveSATBorrado.limpiaorden(listanop)
                solveSATBorrado.limpiacruz(listanop,auxnop)  
                
                
            clausulas.clear()
            clausulas.extend(listano)
            clausulas.extend(listap)
            clausulas.extend(listanop)
        
        
        
                
    
    def limpiaordennum(self,antiguas):
        
        if(len(antiguas)<2):
            return
        
        i1=  0
        i2 = 1
        
        while (i1<(len(antiguas)-1)  ):
            cl1 = self.claus.conjunto[antiguas[i1]]
            cl2 = self.claus.conjunto[antiguas[i2]]
            if cl1.contenida(cl2):
                del antiguas[i2]
            i2=i2-1
            if (i2 ==i1):
                i1=i1+1
                i2 = len(antiguas)-1  
        
    @staticmethod
    def calculapos(x):
        y = dict()
        n = range(len(x))
        for z in n:
            y[x[z]] = z 
        return y
    

    def borra(self):
        current=0
        noborrad = list(range(self.nvar))
        while len(noborrad)>0 and not self.solved:
            print (current)
            varb = self.siguiente(0,noborrad)
            print ("Borrando variable ", varb)
            self.ordenbo.append(varb)
            self.varinorder[varb] = current
            current = current +1
            noborrad.remove(varb)
            # self.listapos[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # self.listaneg[varb].sort(key=lambda x: len(self.claus.conjunto[x].lista))
            # print(len(self.listapos[varb]))
            # self.limpiaordennum(self.listapos[varb])
            # print(len(self.listapos[varb]))
            # print(len(self.listaneg[varb]))
            # self.limpiaordennum(self.listaneg[varb])
            # print(len(self.listaneg[varb]))

            self.posorder.append(self.listapos[varb])
            self.negorder.append(self.listaneg[varb])
            
            # for x in self.listapos[varb]:
            #    print (x, self.claus.conjunto[x].lista)
            
            nuevas = self.borraExacto(varb+1,self.listapos[varb],self.listaneg[varb])
            # for x in nuevas:
            #   print (x.lista)
            print("tamaño sin limpiar" ,len(nuevas))
            nuevas.sort(key=lambda x: len(x.lista))
            posiciones = solveSATBorrado.calculapos(noborrad)
            print("ordenadas")
            # solveSATBorrado.limpiaorden(nuevas)
            solveSATBorrado.limpiarec(nuevas,noborrad,posiciones)
            print("tamaño después de limpiar" ,len(nuevas))
            
            
            
            self.eliminaListas(varb+1,self.listapos[varb],self.listaneg[varb])
            
            
            
            
            print(len(nuevas))
            for x in nuevas:
                if (len(x.lista)==0):
                    self.solved = True
                    self.solution = 0
                elif (abs(x.lista[0])>0):
                    k = self.claus.insertar(x)
                    self.actualizaListas(x,k)
                    
  
            
                    
           
    def actualizaListas(self,x,k):
         if(len(x.lista)>0 and abs(x.lista[0])>0):
             
             for y in x.lista:
                if (y>0):
                    self.inserta(k,self.listapos[y-1])
                else:
                    self.inserta(k,self.listaneg[-y-1])  
             
    @staticmethod  
    def inserta(x,lista):
        j = len(lista)-1
        i = 0 
        end = False
        
        if ((j<0) or (lista[0])>x):
             lista.insert(0,x)
             end = True
             
        if(lista[j]<x):
             lista.append(x)
             end = True
        
       
        while (not end) :
            k = (i+j)//2
            if (lista[k] == x) :
                end = True
            elif (x >  lista[k]):
               i=k+1
            else:
                j=k
            if (i>j):
               lista.insert(i,x)  
               end = True
        
        

def leeArchivoSet(Archivo):
    reader=open(Archivo,"r")
    cadena = reader.readline()
    while cadena[0]=='c':
        cadena = reader.readline()
    param = cadena.split()
    n = int(param[2])
    infor = conjuntoClausulas()
    for cadena in reader:
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            listaux.pop()
            listaux = map(int,listaux)
            clausula= Clausulafs(listaux)
            infor.insertar(clausula)
    return infor


def RegistrarArchivo(nombre):
    print("\nRegistro de nuevo archivo!!!")
    print("\nNota: El archivo debe estar previamente grabado en directorio donde se encuentra Archivo Ejecutable de esta aplicación!!!")
    nombreArchivo=input("\n\nIngrese nombre de archivo (incluya extensión) --> ")
    if os.path.exists(nombreArchivo):
        reader=open(nombreArchivo,"r")
        for cadena in reader.readlines():
            cadena=cadena.strip()
            if cadena[0] == "p":
                cadena=cadena[1:].strip()
                if cadena[:cadena.index(" ")]=="cnf":
                    cadena=cadena[cadena.index(" ")+1:]
                    NVar=int(cadena[:cadena.index(" ")])
                    NProp=int(cadena[cadena.index(" ")+1:])
                    break
        reader.close()
        if NVar>0 and NProp>0:
            writer=open(nombre,"a")
            writer.write(nombreArchivo+";"+str(NVar)+";"+str(NProp)+"\n")
            writer.close()
            print("\nSe grabó información correctamente!!")
        print("\n\nArchivo tiene", NVar,"variables con",NProp,"proposiciones")
    else:
        print("\n\nNO SE ENCUENTRA ARCHIVO !!!!!\n\nFavor copiar archivo en directorio donde se encuentra Archivo Ejecutable de esta aplicación..")
    
def SeleccionarArchivo(nombre):
    ListaArchivos=[]
    contador=0
    print("{0:3} {1:25} {2:5} {3:5}".format("Num","Nombre de Archivo","#Var","#Prop"))
    reader=open(nombre,"r")
    for cadena in reader.readlines():
        if len(cadena.strip())>0:
            ListaArchivos.append((''.join(cadena.split())).split(";"))
            contador=contador+1
            print("{0:3d} {1:25}{2:5d} {3:6d}".format(contador,ListaArchivos[contador-1][0],int(ListaArchivos[contador-1][1]),int(ListaArchivos[contador-1][2])))
    reader.close()
    sel=0
    while (sel<=0 or sel>contador) and contador>0:
        sel=int(input("\n\n Seleccione el Archivo a trabajar --> "))
    if sel>0:
        print(f"\n\nSeleccionó trabajar con el Archivo: ",ListaArchivos[sel - 1][0])
        return(ListaArchivos[sel - 1])
    else:
        print("\n\nNo se encuentra información en Archivo")
        return("")

def PreparaInformacion(Archivo, Nodo, VarPos):
    reader=open(Archivo,"r")
    for cadena in reader.readlines():
        if (cadena[0]>="0" and cadena[0]<="9") or cadena[0]=="-":
            listaux=cadena.split()
            listaux.remove("0")
            clausula=[]
            for var in listaux:
                aux=int(var)
                clausula.append(aux)
                VarPos[abs(aux)].append(len(Nodo))
            Nodo.append(clausula)

def ImprimirListas(Lista):
    for l in Lista:
        print(l)


def MenuPrincipal():
    Nodo=[]
    VarPos=[]
    VarElim=[]
    
    
    while True:
        #os.system("cls") limpiar pantalla
        print("\n\nMENU DE APLICACION")
        print("\n1.- Seleccionar Archivo a procesar")
        print("2.- Registrar nuevo archivo")
        print("3.- Procesar")
        print("4.- Ver resultados")
        print("5.- Salir")
        opc=int(input("\nSeleccione opción --> "))
        if opc==5:
            break
        if opc==1:
            listaAux=SeleccionarArchivo("ArchivosSAT.txt")
            #fileName=listaAux[0]
        elif opc==2:
            RegistrarArchivo("ArchivosSAT.txt")
        elif opc==3:
            info = leeArchivo(listaAux[0])
            satcase = solveSATBorrado(info)
            satcase.borra()
        elif opc==4:
            input("Presione ENTER para regresar al Menú principal!!")

def ProcesaElimina(Nod,lafirma,lniega,VPos):
    laux=[]
    for x in range(len(lafirma)):
        aux1=lafirma[x].copy()
        aux1.remove(0)
        for z in range(0,len(aux1)):
            (VPos[abs(aux1[z])]).remove(lafirma[x][0])
        for y in range(len(lniega)):
            aux2=aux1.copy()
            for z in range(1,len(lniega[y])):
                (VPos[abs(lniega[y][z])]).remove(lniega[y][0])
                if (-lniega[y][z]) in aux2:
                    aux2=[]
                    break
                elif not((lniega[y][z]) in aux2):
                    aux2.append(lniega[y][z])
            if len(aux2)>0:
                laux.append(aux2)
    AgregarClausula(Nod,laux,VPos)
    return laux
    
def AgregarClausula(Nod,lclau,VPos):
    for listaux in lclau:
        for var in listaux:
            VPos[abs(var)].append(len(Nod))
        Nod.append(listaux)
    
#print(SeleccionarArchivo("ArchivosSAT.txt"))
#info = leeArchivoSet('SAT_V64C254.cnf')
info = leeArchivoSet('SAT_V153C408.cnf')


#info = leeArchivoSet('SAT_V144C560.cnf')
problema = solveSATBorradoSet(info)
problema.borra()
problema.busca()
