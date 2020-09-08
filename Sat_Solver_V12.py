# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 07:04:35 2019

@author: Nizziho
"""
import os

class ListaClausulas:
    def __init__(self):
        self.lstClausulas=[]
        self.nVar=0
        self.nClaus=0
        
    def agregarClausula(self, lista):
        self.lstClausulas.append(lista)

    def preparaInformacion(self, Archivo, VarPos):
        self.nVar=Archivo.numVariables
        self.nClaus=Archivo.numClausulas
        reader=open(Archivo.archivoTrabajo,"r")
        for cadena in reader.readlines():
            if (cadena[0]>="0" and cadena[0]<="9") or cadena[0]=="-":
                listaux=cadena.split()
                listaux.remove("0")
                clausula=Clausula()
                for var in listaux:
                    aux=int(var)
                    clausula.propos.append(aux)
                    clausula.num=len(self.lstClausulas)
                    VarPos[abs(aux)].posiciones.append(len(self.lstClausulas))
                    VarPos[abs(aux)].variable=aux
                self.agregarClausula(clausula)
        
    def procesarClausulas(self, VarPos):
        for i in range(1,self.nVar+1):
            listafirma=[]
            listniega=[]
            VarPos[i].eliminada=True
            for var in VarPos[i].posiciones:
                self.lstClausulas[var].procesada=True
                aux=self.lstClausulas[var].propos.copy()
                if i in aux:
                    aux.remove(i)
                    listafirma.append(aux)
                else:
                    aux.remove(-i)
                    listniega.append(aux)
                aux.insert(0,var)        
            print("\n\nVariable a Eliminar: ",i)
            print("Cláusulas afirmadas:")
            ImprimirListas(listafirma)
            print("Cláusulas negadas:")
            ImprimirListas(listniega)
            print("Resultado Eliminación:")
            #ImprimirListas(ProcesaElimina(Nodo,listafirma,listniega,VarPos,NodoElim))
            print("\n\n----NODO---")
            self.imprimirClausulas()
            print("\n\n----POSICIONES---")
            self.imprimirPosiciones(VarPos) 
                
    def imprimirClausulas(self):
        for objClaus in self.lstClausulas:
            objClaus.imprimirClausula()
    
    def imprimirPosiciones(self, VarPos):
        for objPos in VarPos:
            objPos.imprimirPosicion()
            
class PosicionVar:
    def __init__(self):
        self.variable=0
        self.posiciones=[]
        self.eliminada=False
    
    def imprimirPosicion(self):
        print(self.variable,self.posiciones,self.eliminada)
        
class Clausula:
    def __init__(self):
        self.num = -1
        self.procesada = False
        self.propos = []
        
    def imprimirClausula(self):
        print(self.num, self.propos, self.procesada)
    
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
    lstClau = ListaClausulas()
    pVar=[]
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
            pVar=[PosicionVar() for i in range(archivo.numVariables+1)]
            lstClau.preparaInformacion(archivo, pVar)
        elif opc==2:
            archivo.registrarArchivo()
        elif opc==3:
            lstClau.procesarClausulas(pVar)

MenuPrincipal()