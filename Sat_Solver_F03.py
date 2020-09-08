# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 07:04:35 2019
Versión con proceso de buscar contenidas entre en cláusulas que apuntan al primer elemento de la lista
@author: Nizziho
"""
import os
import time

class Clausula:
    def __init__(self):
        self.num = -1
        self.procesada = False
        self.propos = []

    def agregar(self, x):
         j = len(self.propos)-1
         i = 0 
         if ((j<0) or (abs(self.propos[0])>abs(x))):
             self.propos.insert(0,x)
             return
         if(abs(self.propos[j])<abs(x)):
             self.propos.append(x)
             return
         end = False
         while (not end) :
            k = (i+j)//2
            if (self.propos[k] == x) :
                return
            elif (self.propos[k] == -x) :
                self.makeTrue()
                return
            elif (abs(x) >  abs(self.propos[k])):
               i=k+1
            else:
                j=k
            if (i==j):
                end = True
         self.propos.insert(i,x)

    def encontrar(self, x):
         j = len(self.propos)-1
         i = 0 
         if ((j<0) or (abs(self.propos[0])>abs(x))):
             return False
         if(abs(self.propos[j])<abs(x)):
             return False

         end = False
         while (not end) :
            k = (i+j)//2
            if (self.propos[k] == x) :
                return True
            elif (self.propos[k] == -x) :
                return False
            elif (abs(x) >  abs(self.propos[k])):
               i=k+1
            else:
                j=k-1
            if (i>j):
                return False
            
    def resolver(self, var, clau):
        auxclau = []
        leni = len(self.propos)-1
        lenj = len(clau.propos)-1
        i=0
        j=0
        self.procesada=True
        clau.procesada=True
        while i<=leni and j<=lenj:
            if self.propos[i]==var:
                i=i+1
                continue
            if clau.propos[j]==-var:
                j=j+1
            elif self.propos[i]==-clau.propos[j]:
                auxclau=[]
                return auxclau
            elif self.propos[i]==clau.propos[j]:
                auxclau.append(self.propos[i])
                i=i+1
                j=j+1
            elif abs(self.propos[i])<abs(clau.propos[j]):
                auxclau.append(self.propos[i])
                i=i+1
            else:
                auxclau.append(clau.propos[j])
                j=j+1                
        temp=self.propos[i:]+clau.propos[j:]
        for i in temp:
            if abs(i)!=var:
                auxclau.append(i)
        return auxclau
                

    def eliminar(self, x):
         j = len(self.propos)-1
         i = 0 
         if ((j<0) or (abs(self.propos[0])>abs(x))):
             return False
         if(abs(self.propos[j])<abs(x)):
             return False
         end = False

         while (not end) :
            k = (i+j)//2
            if (self.propos[k] == x) :
                del(self.propos[k])
                return True
            elif (self.propos[k] == -x) :
                return False
            elif (abs(x) >  abs(self.propos[k])):
               i=k+1
            else:
                j=k-1
            if (i>j):
                return False
            
    def retornar(self, posicion):
        return self.propos[posicion]

    def imprimirClausula(self):
        print(self.num, self.propos, self.procesada)


class ListaClausulas:
    def __init__(self, Archivo):
        self.lstClausulas=[]
        self.nVar=0
        self.nClaus=0
        self.indice=0
        self.varElimina=0
        self.varResultado=[-1 for i in range(Archivo.numVariables+1)]
        self.varOrdElimina=[i for i in range(Archivo.numVariables+1)]
        self.posAfirmadas=[list() for i in range(Archivo.numVariables+1)]
        self.posNegadas=[list() for i in range(Archivo.numVariables+1)]
        self.nVar=Archivo.numVariables
        self.nClaus=Archivo.numClausulas
        reader=open(Archivo.archivoTrabajo,"r")
        for cadena in reader.readlines():
            listaux=cadena.split()
            if (listaux[0][0:1]>="0" and listaux[0][0:1]<="9") or listaux[0][0:1]=="-":
                clausAux=Clausula()
                for x in listaux[0:-1]:
                    clausAux.agregar(int(x))
                if not(estaContenida(self,clausAux.propos)):
                     self.agregarClausula(clausAux)
    
    def selVarEliminar(self):
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
        self.varElimina=self.varOrdElimina[self.indice]

    def agregarClausula(self, clausula):
        for var in clausula.propos:
            if var>0:
                self.posAfirmadas[var].append(len(self.lstClausulas))
            else:
                self.posNegadas[-var].append(len(self.lstClausulas))
        clausula.num=len(self.lstClausulas)
        self.lstClausulas.append(clausula)

    def eliminarPosicion(self, pos, x):
         if pos>0:
             prop=self.posAfirmadas[pos]
         else:
             prop=self.posNegadas[-pos]        
         j = len(prop)-1
         i = 0 
         if ((j<0) or (abs(prop[0])>abs(x))):
             return False
         if(abs(prop[j])<abs(x)):
             return False
         end = False

         while (not end) :
            k = (i+j)//2
            if (prop[k] == x) :
                del(prop[k])
                return True
            elif (prop[k] == -x) :
                return False
            elif (abs(x) >  abs(prop[k])):
               i=k+1
            else:
                j=k-1
            if (i>j):
                return False        

    def imprimirClausulas(self):
        for objClaus in self.lstClausulas:
            objClaus.imprimirClausula()
    
    def imprimirPosiciones(self):
        print("Posiciones Afirmadas")
        for objPos in self.posAfirmadas:
            print(objPos)
        print("Posiciones Negadas")
        for objPos in self.posNegadas:
            print(objPos)
    
    def imprimirClausulasVar(self,var):
        print("Clausulas Afirmadas  de ", var)
        for p in self.posAfirmadas[var]:
            print(self.lstClausulas[p].num,self.lstClausulas[p].propos) 
        print("Clausulas Negadas  de ", var)
        for p in self.posNegadas[var]:
            print(self.lstClausulas[p].num,self.lstClausulas[p].propos) 
    
    def imprimirResultados(self):
        print("\n\nRESULTADOS")
        for i in range(1,self.nVar+1):
            print("Var ",i," = ",self.varResultado[i])
            
                
def procesarClausulas(clausulas):
    listaux=[]
    for i in range(1,clausulas.nVar+1):
        clausulas.selVarEliminar()
        band=True
        cont=0
        contenidas=0
        noGen=0
        tinicio=time.time()
        if (len(clausulas.posAfirmadas[clausulas.varElimina])>0):
            for varA in clausulas.posAfirmadas[clausulas.varElimina]:            
                Posicion(clausulas,clausulas.lstClausulas[varA],clausulas.varElimina)
                lstposNegadas=clausulas.posNegadas[clausulas.varElimina].copy()
                for varN in lstposNegadas:
                    if band:
                        borraPosicion(clausulas,clausulas.lstClausulas[varN],clausulas.varElimina)
                    listaux=clausulas.lstClausulas[varA].resolver(clausulas.varElimina,clausulas.lstClausulas[varN])                
                    if len(listaux)>0:
                        if not(estaContenida(clausulas,listaux)):
                            TempClau=Clausula()
                            TempClau.propos=listaux
                            clausulas.agregarClausula(TempClau)
                            cont=cont+1
                        else:
                            contenidas=contenidas+1
                    else:
                        noGen=noGen+1
                band=False
        else:
                for varN in clausulas.posNegadas[clausulas.varElimina]:
                        borraPosicion(clausulas,clausulas.lstClausulas[varN],clausulas.varElimina)
        tfin=time.time()
        print(i,"Proceso de Borrado Variable: ",clausulas.varElimina,", VAfir=",len(clausulas.posAfirmadas[clausulas.varElimina]),", VNeg=",len(clausulas.posNegadas[clausulas.varElimina]),", TotalC=",len(clausulas.posAfirmadas[clausulas.varElimina])*len(clausulas.posNegadas[clausulas.varElimina]),", CNGPElim=",noGen, ", VR=",cont,", ContBorr=",0,", ContGen=",contenidas, "Tiempo=",tfin-tinicio)

def borraPosicion(clausulas,inClau, pos):
    for y in inClau.propos:
        if abs(y)!=pos:
            clausulas.eliminarPosicion(y,inClau.num)
    
def estaContenida(clausulas,lista):
    if lista[0]>0:
        conjInters = set(clausulas.posAfirmadas[lista[0]])
    else:
        conjInters = set(clausulas.posNegadas[-lista[0]])
    for elem in lista[1:]:
        if elem>0:
            conjTemp = set(clausulas.posAfirmadas[elem])
        else:
            conjTemp = set(clausulas.posNegadas[-elem])
        conjInters = conjInters & conjTemp
        if len(conjInters)==0:
            break
    for elem in conjInters:
        if len(clausulas.lstClausulas[elem].propos)>len(lista):
            borraPosicion(clausulas,clausulas.lstClausulas[elem],0)
        else:
            return True
    
    conjUnion=set()
    conjLista=set(lista)
    i=0
    for elem in lista:
        if elem>0:
            conjSol=set(clausulas.posAfirmadas[elem])
        else:
            conjSol=set(clausulas.posNegadas[-elem])
        conjSol=conjSol-conjUnion
        conjUnion=conjUnion|conjSol
        for x in conjSol:
            if len(clausulas.lstClausulas[x].propos)<(len(conjLista)-i):
                conjX=set(clausulas.lstClausulas[x].propos)
                conjComp=conjLista & conjX
                if (len(conjComp)==len(conjX)):
                    return True
        i=i+1
    return False
    
    
def estaContenidaX(clausulas,lista):
    if lista[0]>0:
        pos=clausulas.posAfirmadas[lista[0]]
    else:
        pos=clausulas.posNegadas[-lista[0]]
    for p in pos:
        lstTemp=clausulas.lstClausulas[p].propos
        if len(lstTemp)>len(lista):
            lstMayor=lstTemp
            lstMenor=lista
        else:
            lstMayor=lista
            lstMenor=lstTemp
        i=0
        j=0
        leni=len(lstMayor)-1
        lenj=len(lstMenor)-1
        while i<=leni and j<=lenj:
            if lstMayor[i]==lstMenor[j]:
                i=i+1
                j=j+1
            elif abs(lstMayor[i])<abs(lstMenor[j]):
                i=i+1
            else:
                break
        if j>lenj:
            if len(lstTemp)>len(lista):
                clausulas.lstClausulas[p].procesada=True
                borraPosicion(clausulas,clausulas.lstClausulas[p],0)
                i=1
            else:
                return True
    return False

def estaContenidaBorrado(lstBorrado,lista):
    for p in lstBorrado:
        if len(p)>len(lista):
            lstMayor=p
            lstMenor=lista
        else:
            lstMayor=lista
            lstMenor=p
        i=0
        j=0
        leni=len(lstMayor)-1
        lenj=len(lstMenor)-1
        while i<=leni and j<=lenj:
            if lstMayor[i]==lstMenor[j]:
                i=i+1
                j=j+1
            elif abs(lstMayor[i])<abs(lstMenor[j]):
                i=i+1
            else:
                break
        if j>lenj:
            if len(lstBorrado)>len(lista):
                lstBorrado.remove(p)
                i=1
            else:
                return True
    return False


class FuenteDatos:
    def __init__(self, file):
        self.nombre=file
        self.numVariables=0
        self.numClausulas=0
        self.archivoTrabajo=""

    def seleccionarArchivo(self):
        ListaArchivos=[]
        contador=0
        print("{0:3} {1:25} {2:5} {3:5}".format("Num","Nombre de Archivo","#Var","#Cláusulas"))
        reader=open(self.nombre,"r")
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
                print("\n\nSeleccionó trabajar con el Archivo: ",ListaArchivos[sel - 1][0])
                self.archivoTrabajo=ListaArchivos[sel - 1][0]
                self.numVariables=int(ListaArchivos[sel - 1][1])
                self.numClausulas=int(ListaArchivos[sel - 1][2])
            else:
                print("\n\nNo se encuentra información en Archivo")

    def registrarArchivo(self):
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
                writer=open(self.nombre,"a")
                writer.write(nombreArchivo+";"+str(NVar)+";"+str(NProp)+"\n")
                writer.close()
                print("\nSe grabó información correctamente!!")
            print("\n\nArchivo tiene", NVar,"variables con",NProp,"proposiciones")
        else:
            print("\n\nNO SE ENCUENTRA ARCHIVO !!!!!\n\nFavor copiar archivo en directorio donde se encuentra Archivo Ejecutable de esta aplicación..")

def busqueda(clausulas):
    for i in range(len(clausulas.varOrdElimina)-1,0,-1):
        listaR=clausulas.posAfirmadas[clausulas.varOrdElimina[i]] + clausulas.posNegadas[clausulas.varOrdElimina[i]]
        tempPos=len(clausulas.posAfirmadas[clausulas.varOrdElimina[i]])-1
        tempi=-1
        if len(listaR)==0:
            clausulas.varResultado[clausulas.varOrdElimina[i]]=0
        else:
            for pos in listaR:
                tempi=tempi+1
                proaux=clausulas.lstClausulas[pos].propos
                if len(proaux)==0:
                    clausulas.varResultado[clausulas.varOrdElimina[i]]=0
                    break
                if len(proaux)==1:
                    if proaux[0]>0:
                        clausulas.varResultado[clausulas.varOrdElimina[i]]=1
                    else:
                        clausulas.varResultado[clausulas.varOrdElimina[i]]=0
                    break
                else:
                    band=True
                    clausulas.varResultado[clausulas.varOrdElimina[i]]=0
                    for var in proaux:
                        if abs(var)!=clausulas.varOrdElimina[i]:
                            if (clausulas.varResultado[abs(var)]==1 and var>0) or (clausulas.varResultado[abs(var)]==0 and var<0):
                                band=False
                                break
                    if band:
                        if tempi<=tempPos:
                            clausulas.varResultado[clausulas.varOrdElimina[i]]=1
                        else:
                            clausulas.varResultado[clausulas.varOrdElimina[i]]=0
                        break

def MenuPrincipal():
    archivo = FuenteDatos("ArchivosSAT.txt")
    
    while True:
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
            archivo.seleccionarArchivo()
            lstClau = ListaClausulas(archivo)
        elif opc==2:
            archivo.registrarArchivo()
        elif opc==3:
            lstClau.imprimirClausulas()
            input("Presione Enter")
            procesarClausulas(lstClau)
        elif opc==4:
            busqueda(lstClau)
            lstClau.imprimirResultados()

MenuPrincipal()