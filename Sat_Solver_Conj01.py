# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 08:25:29 2019

@author: Nizziho
"""
import time
class Clausula:
    def __init__(self,x):
        self.N=0
        self.datos = frozenset(x)

    def contenida(self,x):
        return self.datos.issubset(x)

    def contiene(self,x):
        return self.datos.issuperset(x)

    def pertenece(self, x):
       return x in self.lista
   
    def resuelve(self,varb,clau2):
        result = set(self.datos.union(clau2.datos) - {varb,-varb})
        for i in result:
            if (i>0) and (-i in result):
                result.clear()
                break
        return (Clausula(result))
        
class conjuntoClausulas:
    def __init__(self,x):
        self.lstClausulas=[]
        self.nVar=x
        self.indice=0
        self.varResultado=[-1 for i in range(x+1)]
        self.varOrdElimina=[i for i in range(x+1)]        
        self.posAfirmadas=[set() for i in range(x+1)]
        self.posNegadas=[set() for i in range(x+1)]
         
    def insertar(self,x):
        x.N=len(self.lstClausulas)
        for y in x.datos:
            if y>0:
                self.posAfirmadas[y].add(x.N)
            else:
                self.posNegadas[-y].add(x.N)
        self.lstClausulas.append(x)

    def imprimir_Clausualas(self):
        for clau in self.lstClausulas:
            print(clau.datos)

    def borra(self):
        listaux=set()
        for i in range(1,self.nVar+1):
            varElimina=self.siguiente()
            band=True
            cont=0
            contenidas=0
            noGen=0
            tinicio=time.time()
            if (len(self.posAfirmadas[varElimina])>0):
                for varA in self.posAfirmadas[varElimina]:            
                    self.borraPosicion(self.lstClausulas[varA],varElimina)
                    lstposNegadas=self.posNegadas[varElimina].copy()
                    for varN in lstposNegadas:
                        if band:
                            self.borraPosicion(self.lstClausulas[varN],varElimina)
                        listaux=self.lstClausulas[varA].resuelve(varElimina,self.lstClausulas[varN])                
                        if len(listaux.datos)>0:
                            if not(self.estaContenida(listaux.datos)):
                                self.insertar(listaux)
                                cont=cont+1
                            else:
                                contenidas=contenidas+1
                        else:
                            noGen=noGen+1
                    band=False
            else:
                    for varN in self.posNegadas[varElimina]:
                            self.borraPosicion(self.lstClausulas[varN],varElimina)
            tfin=time.time()
            print(i,"Proceso de Borrado Variable: ",varElimina,", VAfir=",len(self.posAfirmadas[varElimina]),", VNeg=",len(self.posNegadas[varElimina]),", TotalC=",len(self.posAfirmadas[varElimina])*len(self.posNegadas[varElimina]),", CNGPElim=",noGen, ", VR=",cont,", ContBorr=",0,", ContGen=",contenidas, "Tiempo=",tfin-tinicio)

        
    def siguiente(self):
        self.indice = self.indice + 1
        valor = (len(self.posAfirmadas[self.varOrdElimina[self.indice]]) * len(self.posNegadas[self.varOrdElimina[self.indice]])) - len(self.posAfirmadas[self.varOrdElimina[self.indice]]) - len(self.posNegadas[self.varOrdElimina[self.indice]])
        for p in range(self.indice + 1,self.nVar):
            a=len(self.posAfirmadas[self.varOrdElimina[p]])
            b=len(self.posNegadas[self.varOrdElimina[p]])
            if valor > a*b - a - b:
                valor=a*b - a - b
                aux=self.varOrdElimina[self.indice]
                self.varOrdElimina[self.indice] = self.varOrdElimina[p]
                self.varOrdElimina[p] = aux
        return self.varOrdElimina[self.indice]
    
    def borraPosicion(self,inClau, pos):
        for y in inClau.datos-{pos,-pos}:
            if y>0:
                self.posAfirmadas[y].discard(inClau.N)
            else:
                self.posNegadas[-y].discard(inClau.N)  

    def estaContenida(self,conjunto):
        conjLista=set(conjunto)
        aux=conjLista.pop()
        if aux>0:
            conjInters = self.posAfirmadas[aux]
        else:
            conjInters = self.posNegadas[-aux]
        for elem in conjunto:
            if elem>0:
                conjTemp = self.posAfirmadas[elem]
            else:
                conjTemp = self.posNegadas[-elem]
            conjInters = conjInters & conjTemp
            if len(conjInters)==0:
                break
        for elem in conjInters:
            if len(self.lstClausulas[elem].datos)>len(conjunto):
                self.borraPosicion(self.lstClausulas[elem],0)
            else:
                return True
    
        conjUnion=set()
        conjLista=conjunto
        i=0
        for elem in conjunto:
            if elem>0:
                conjSol=self.posAfirmadas[elem]
            else:
                conjSol=self.posNegadas[-elem]
            conjSol=conjSol-conjUnion
            conjUnion=conjUnion|conjSol
            for x in conjSol:
                if len(self.lstClausulas[x].datos)<(len(conjLista)-i):
                    conjX=self.lstClausulas[x].datos
                    conjComp=conjLista & conjX
                    if (len(conjComp)==len(conjX)):
                        return True
            i=i+1
        return False                         
        
def leeArchivo(Archivo):
    reader=open(Archivo,"r")
    cadena = reader.readline()
    while cadena[0]=='c':
        cadena = reader.readline()
    param = cadena.split()
    n = int(param[2])
    infor = conjuntoClausulas(n)
    for cadena in reader:
        if (cadena[0]!='c'):
            cadena.strip()
            listaux=cadena.split()
            clausula= Clausula([int (var) for var in listaux[0:-1]])
            infor.insertar(clausula)
    return infor

info = leeArchivo('SAT_V144C560.cnf')
info.imprimir_Clausualas()
info.borra()