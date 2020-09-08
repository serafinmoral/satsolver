# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os

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

def PreparaInformacion(Archivo, Nodo, VarPos, NodoElim):
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
            NodoElim.append(False)

def ImprimirListas(Lista):
    for l in Lista:
        print(l)


def MenuPrincipal():
    Nodo=[]
    NodoElim=[]
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
            VarPos=[list() for i in range(int(listaAux[1])+1)]
            VarElim=[False for i in range(int(listaAux[1])+1)]
            PreparaInformacion(listaAux[0], Nodo, VarPos, NodoElim)
        elif opc==2:
            RegistrarArchivo("ArchivosSAT.txt")
        elif opc==3:
            for i in range(1,int(listaAux[1])+1):#int(listaAux[1])+1):
                listafirma=[]
                listniega=[]
                VarElim[i]=True
                for var in VarPos[i]:
                    NodoElim[var]=True
                    aux=Nodo[var].copy()
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
                ImprimirListas(ProcesaElimina(Nodo,listafirma,listniega,VarPos,NodoElim))
                print("\n\n----NODO---")
                ImprimirListas(Nodo)
                print("\n\n----POSICIONES---")
                ImprimirListas(VarPos)                
        elif opc==4:
            input("Presione ENTER para regresar al Menú principal!!")

def ProcesaElimina(Nod,lafirma,lniega,VPos,NodElim):
    laux=[]
    print("Problema")
    ImprimirListas(lafirma)
    ImprimirListas(lniega)
    for x in range(len(lafirma)):
        for y in range(1,len(lafirma[x])):
            (VPos[abs(lafirma[x][y])]).remove(lafirma[x][0])
    for x in range(len(lniega)):
        for y in range(1,len(lniega[x])):
            (VPos[abs(lniega[x][y])]).remove(lniega[x][0])
            
    for x in range(len(lafirma)):
        for y in range(len(lniega)):
            aux2=lafirma[x].copy()
            aux2.pop(0)
            for z in range(1,len(lniega[y])):
                if (-lniega[y][z]) in aux2:#Probar con aux1
                    aux2=[]
                    break
                elif not((lniega[y][z]) in aux2):
                    aux2.append(lniega[y][z])
            if len(aux2)>0:
                if (VerificaContenida(Nod,aux2,NodElim,VPos)):
                    laux.append(aux2)
    AgregarClausula(Nod,laux,VPos,NodElim)
    return laux
    
def AgregarClausula(Nod,lclau,VPos,NodElim):
    for listaux in lclau:
        for var in listaux:
            VPos[abs(var)].append(len(Nod))
        Nod.append(listaux)
        NodElim.append(False)

def VerificaContenida(Nod,lista,NodElim,VPos):
    for i in range(0,len(Nod)):
        contenida=True
        if not(NodElim[i]):
            if len(Nod[i])>=len(lista):
                l1=Nod[i]
                l2=lista
                NodoMay=True
            else:
                l1=lista
                l2=Nod[i]
                NodoMay=False
            for x in l2:
                if not(x in l1):
                    contenida=False
                    break
            if contenida:
                if NodoMay:
                    NodElim[i]=True
                    for y in l1:
                        (VPos[abs(y)]).remove(i)                    
                    return True
                else:
                    return False
            else:
                return True
MenuPrincipal()
#print(SeleccionarArchivo("ArchivosSAT.txt"))
