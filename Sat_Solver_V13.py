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
            if (cadena[0]>="0" and cadena[0]<="9") or cadena[0]=="-":
                listaux=cadena.split()
                listaux.remove("0")
                self.agregarClausula(listaux)
    
    def varEliminar(self):
        self.indice = self.indice + 1
        valor = (len(self.posAfirmadas[self.indice]) * len(self.posNegadas[self.indice])) - len(self.posAfirmadas[self.indice]) - len(self.posNegadas[self.indice])
        for p in range(self.indice + 1,self.nVar):
            if valor > (len(self.posAfirmadas[p]) * len(self.posNegadas[p])) - len(self.posAfirmadas[p]) - len(self.posNegadas[p]):
                valor=(len(self.posAfirmadas[p]) * len(self.posNegadas[p])) - len(self.posAfirmadas[p]) - len(self.posNegadas[p])
                aux=self.varOrdElimina[self.indice]
                self.varOrdElimina[self.indice] = p
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

                
def procesarClausulas(clausulas):
    for i in range(1,clausulas.nVar+1):
        print("Ingresa selección eliminar")
        clausulas.varEliminar()
        print("Sale selección eliminar")
        listafirma=[]
        listniega=[]
        for var in clausulas.posAfirmadas[clausulas.varElimina]:
            clausulas.lstClausulas[var].procesada=True
            #aux=copy.copy(clausulas.lstClausulas[var])
            aux=Clausula()
            aux.num=clausulas.lstClausulas[var].num
            aux.propos=clausulas.lstClausulas[var].propos.copy()
            aux.eliminar(clausulas.varElimina)
            listafirma.append(aux)
            
        for var in clausulas.posNegadas[clausulas.varElimina]:
            clausulas.lstClausulas[var].procesada=True
            #aux=copy.copy(clausulas.lstClausulas[var])
            aux=Clausula()
            aux.num=clausulas.lstClausulas[var].num
            aux.propos=clausulas.lstClausulas[var].propos.copy()
            aux.eliminar(-clausulas.varElimina)
            listniega.append(aux)
            
        clausulas.imprimirPosiciones()       
        print("\n\nVariable a Eliminar: ", clausulas.varOrdElimina[clausulas.indice])
        print("Cláusulas afirmadas:")
        for i in listafirma:
            i.imprimirClausula()
        print("Cláusulas negadas:")
        for i in listniega:
            i.imprimirClausula()
        print("Resultado Eliminación:")
        borraVariable(clausulas,listafirma,listniega)
        #ImprimirListas(ProcesaElimina(Nodo,listafirma,listniega,VarPos,NodoElim))
        print("\n\n----NODO---")
        clausulas.imprimirClausulas()
        print("\n\n----POSICIONES---")
        #clausulas.imprimirPosiciones()     

def borraVariable(clausulas,lstAfirma,lstNiega):
    laux=lstAfirma+lstNiega
    for x in laux:
        for y in x.propos:
            if y>0:
                #print(y,clausulas.posAfirmadas[y],x.num)
                clausulas.posAfirmadas[y].remove(x.num)
            else:
                #print(y,clausulas.posNegadas[-y],x.num)
                clausulas.posNegadas[-y].remove(x.num)
    laux=[]
    for x in lstAfirma:
        for y in lstNiega:
            aux=Clausula()
            aux.propos=x.propos.copy()
            #aux=copy.copy(x)
            for z in y.propos:
                print (z)
                if aux.encontrar(-z):
                    aux.propos=[]
                    break
                elif not(aux.encontrar(z)):
                    aux.agregar(z)
                print(y.propos,z,aux.propos)
            if len(aux.propos)>0:
                if not(estaContenida(clausulas,aux.propos)):
                    clausulas.agregarClausula(aux.propos)
                    print(aux.propos)
    
def estaContenida(clausulas, lista):
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

MenuPrincipal()