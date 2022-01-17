# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 22:52:53 2021

@author: efrai
"""

def tranformaArchivoCNF(Archivo):
    lista = list()
    archivo=""
    contarClaus=0
    (contarClaus,archivo)=leerArchivoEvid(Archivo+".evid")
    reader=open(Archivo,"r") 
    reader.readline()
    reader.readline()
    reader.readline()
    numFactor = int(reader.readline())
    for i in range(numFactor):
        cadena = reader.readline()
        lista.append(cadena.split())
        print(i+1,cadena)
    # print (lista)
    for l in lista:
        reader.readline()
        reader.readline()
        n=0
        for x in range(pow(2,int(l[0])-1)):
            laux=reader.readline().split()
            cadClaus=""
            if (float(laux[0]) in {0.0, 1.0}):
                cadAux= ("0"*int(l[0]))[len(bin(2*n+int(float(laux[0])))[2:]):int(l[0])] + bin(2*n+int(float(laux[0])))[2:]
                for r in range(int(l[0])):
                    if (cadAux[r]=="0"):
                        cadClaus = cadClaus + str(-1*(int(l[r+1])+1)) + "  "
                    else:
                        cadClaus = cadClaus + str((int(l[r+1])+1)) + "  "
                cadClaus = cadClaus + "0"
                contarClaus = contarClaus + 1
                archivo = archivo + cadClaus + "\n"
                print(l[0],laux, cadAux, cadClaus)
            n=n+1
    # print (archivo)
    nFileOut = Archivo.split('.')
    archivo = "c\nc SAT instance in Bayes nets CNF input format.\nc\np cnf " + str(numFactor) + " " + str(contarClaus) + "\n" + archivo
    f = open (nFileOut[0] + '.cnf','w')
    f.write(archivo)
    f.close()

def leerArchivoEvid(Archivo):
    cadClaus=""
    reader=open(Archivo,"r")
    lista=reader.readline().split()
    for x in range(int(lista[0])):
        if (lista[2*x+2]=="0"):
            cadClaus = cadClaus + str((int(lista[2*x+1])+1)) + "  0\n"
        else:
            cadClaus = cadClaus + str(-1*(int(lista[2*x+1])+1)) + "  0\n"
    return int(lista[0]), cadClaus


tranformaArchivoCNF("BN_134.uai")