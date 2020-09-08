# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 07:04:35 2019

@author: Nizziho
"""
import os
import copy

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
                j=k-1
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
        if i<=leni:
            #auxclau=auxclau + self.propos[i:]
            temp=Clausula()
            temp.propos=self.propos[i:].copy()
            temp.eliminar(var)
            auxclau=auxclau + temp.propos              
        if j<=lenj:
            temp=Clausula()
            temp.propos=clau.propos[j:].copy()
            temp.eliminar(-var)
            auxclau=auxclau + temp.propos        
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
        self.varOrdElimina=[i for i in range(Archivo.numVariables+1)]
        self.posAfirmadas=[list() for i in range(Archivo.numVariables+1)]
        self.posNegadas=[list() for i in range(Archivo.numVariables+1)]
        self.nVar=Archivo.numVariables
        self.nClaus=Archivo.numClausulas
        reader=open(Archivo.archivoTrabajo,"r")
        for cadena in reader.readlines():
            listaux=cadena.split()
            if (listaux[0][0:1]>="0" and listaux[0][0:1]<="9") or listaux[0][0:1]=="-":
                listaux.remove("0")
                self.agregarClausula(listaux)
    
    def selVarEliminar(self):
        self.indice = self.indice + 1
        valor = (len(self.posAfirmadas[self.indice]) * len(self.posNegadas[self.indice])) - len(self.posAfirmadas[self.indice]) - len(self.posNegadas[self.indice])
        for p in range(self.indice + 2,self.nVar):
            if valor > (len(self.posAfirmadas[p]) * len(self.posNegadas[p])) - len(self.posAfirmadas[p]) - len(self.posNegadas[p]):
                valor=(len(self.posAfirmadas[p]) * len(self.posNegadas[p])) - len(self.posAfirmadas[p]) - len(self.posNegadas[p])
                aux=self.varOrdElimina[self.indice]
                self.varOrdElimina[self.indice] = self.varOrdElimina[p]
                self.varOrdElimina[p] = aux
        self.varElimina=self.varOrdElimina[self.indice]

    def agregarClausula(self, lista):
        clausula=Clausula()
        for var in lista:
            aux=int(var)
            clausula.agregar(aux)
            if aux>0:
                self.posAfirmadas[aux].append(len(self.lstClausulas))
            else:
                self.posNegadas[-aux].append(len(self.lstClausulas))
        clausula.num=len(self.lstClausulas)
        self.lstClausulas.append(clausula)

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
            print(self.lstClausulas[p].propos)
        print("Clausulas Negadas  de ", var)
        for p in self.posNegadas[var]:
            print(self.lstClausulas[p].num,self.lstClausulas[p].propos)
                
def procesarClausulas(clausulas):
    listaux=[]
    clausulas.imprimirClausulas()
    clausulas.imprimirPosiciones()
    for i in range(1,clausulas.nVar+1):
        clausulas.selVarEliminar()
        band=True
        print("Resultado de Eliminación de: ",clausulas.varElimina)#
        clausulas.imprimirClausulasVar(clausulas.varElimina)#
        if (len(clausulas.posAfirmadas[clausulas.varElimina])>0):
            for varA in clausulas.posAfirmadas[clausulas.varElimina]:            
                borraPosicion(clausulas,clausulas.lstClausulas[varA])
                lstposNegadas=clausulas.posNegadas[clausulas.varElimina].copy()
                for varN in lstposNegadas:
                    if band:
                        borraPosicion(clausulas,clausulas.lstClausulas[varN])
                    listaux=clausulas.lstClausulas[varA].resolver(clausulas.varElimina,clausulas.lstClausulas[varN])
                    if len(listaux)>0:
                        if not(estaContenida(clausulas,listaux)):
                            clausulas.agregarClausula(listaux)
                            print(i,listaux)
                band=False
        else:
                for varN in clausulas.posNegadas[clausulas.varElimina]:
                        borraPosicion(clausulas,clausulas.lstClausulas[varN])

def borraPosicion(clausulas,inClau):
    for y in inClau.propos:
        if abs(y)!=clausulas.varElimina:
            if y>0:
                clausulas.posAfirmadas[y].remove(inClau.num)
            else:
                clausulas.posNegadas[-y].remove(inClau.num)
    
def estaContenida(clausulas, lista):
    for p in lista:
        i=0
        j=0
        band=False
        temp=clausulas.lstClausulas[p].propos
        leni=len(temp)-1
        lenj=len(lista)-1
        while i<=leni and j<=lenj:
            if abs(temp[i])>abs(lista[j]):
                band=False
                break
            elif abs(temp[i])<abs(lista[j]):
                i=i+1
                band=False
            elif temp[i]!=lista[j]:
                band=False
                break
            else:
                i=i+1
                j=j+1
                band=True
        if band:
            if leni>lenj:
                clausulas.lstClausulas[p].procesada=True
                borraPosicion(clausulas,clausulas.lstClausulas[p])
                return False
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
                print(f"\n\nSeleccionó trabajar con el Archivo: ",ListaArchivos[sel - 1][0])
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
    


def ImprimirListas(Lista):
    for l in Lista:
        print(l)


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
            procesarClausulas(lstClau)
            lstClau.imprimirClausulas()
            lstClau.imprimirPosiciones()

MenuPrincipal()