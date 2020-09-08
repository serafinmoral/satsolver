# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:30:14 2019

@author: Nizziho
"""
import os

import itertools
         
from comunes import *  

from random import *
              
from GlobalClausulas import *
from arbolpot import *
#
#x = 3434
#for i in range(60):
#    x = x*1.2
#    print(x)

from time import time

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
                infor.unit.add(h)
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

  



def pure_literal(formula):
        counter = get_counter(formula)
        assignment = []
        pures = []
        for literal, times in counter.items():
            if -literal not in counter: 
                pures.append(literal)
        for pure in pures:
            formula = bcp(formula, pure)
        assignment += pures
        return formula, assignment
#%%
def get_counter(formula):
        counter = {}
        for clause in formula:
            for literal in clause:
                if literal in counter:
                    counter[literal] += 1
                else:
                    counter[literal] = 1
        return counter


def bcp(formula, VarUnica):
        modificado = []
        for clausula in formula:
            if VarUnica in clausula:
                continue
            if -VarUnica in clausula:
                nueva_clause=[]
                for x in clausula:
                    if x !=-VarUnica:
                        nueva_clause=nueva_clause+[x]
                if not nueva_clause:
                    return -1
                modificado.append(nueva_clause)
            else:
                modificado.append(clausula)
        return modificado

def marginaliza(fv,v,probs,lista):

    if not fv.listaclaus:
        return (1.0,1.0)
    
    if fv.contradict:
        return (0.0,0.0)
    
    
    if lista:
        vp = max(lista, key = lambda x: len(fv.indices.get(x,set())) +  len(fv.indices.get(-x,set()))  )
        
        (fv1,fv2) = fv.divide(vp)
        lista1 = fv1.listavar-{v}
        lista2 = fv2.listavar-{v}
        
        
        (x1,x2) = marginaliza(fv1,v,probs,lista1)
        (y1,y2) = marginaliza(fv2,v,probs,lista2)
        
        
        x = (probs[vp]*x1+(1-probs[vp])*y1)
        y = (probs[vp]*x2+(1-probs[vp])*y2)
        
#        if x==0.0 and probs[vp]>0 and x1>0:
#            print("problema redondeo")
#            
#        if x==0.0 and (1-probs[vp])>0 and y1>0:
#            print("problema redondeo")    
#            
#        if y==0.0 and (probs[vp])>0 and x2>0:
#            print("problema redondeo")
##        if (x==0.0) and (y==0.0):
##            print("does ceros")
#            
#        if y==0.0 and (1-probs[vp])>0 and y2>0:
#            print("problema redondeo")    
##            
       
        
        return (x,y)
    
    else:
        n1 = 1.0
        n2=  1.0
        
        if frozenset({v}) in fv.listaclaus:
            n2 = 0.0
            
        if frozenset({-v}) in fv.listaclaus:
            n1 = 0.0     
        
        return (n1,n2)
            
        
        
        
def propaga(formula,probs,N=1,eps=0.1):
    
    minv = 0.0000001
    i = 1
    cambio = True
    while i<= N and cambio:
#        print(i)
#        print(probs)
        i+=1
        cambio = False
        for v in probs:
#            print(v)
            old = probs[v]
            fv = globalClausulas()
            if v in formula.indices:
                for cl in formula.indices[v]:
                    fv.insertar(cl)
            if -v in formula.indices:
                for cl in formula.indices[-v]:
                    fv.insertar(cl)
            
            
#            print(fv.listaclaus)
#            print(fv.listavar)
            lista = fv.listavar-{v}
            (pos,neg) = marginaliza(fv,v,probs,lista)
            if pos==0.0 and neg==0.0:
#                print("dos ceros")
                formula.contradict=True
                return
            else:
                new =pos/(pos+neg)
#                if (new == 0.0) and (pos>0):
#                    new = minv
#                if (new ==1.0) and (neg>0):
#                    new = 1-minv
                probs[v] = 0.8*new + 0.2*old
            if abs(new -old)>eps:

                cambio = True
            if fv.contradict:
                formula.contradict=True
                return
            
    
    
    
 
def backtracking(formula, asignaciones, probs):
   
#        print(len(asignaciones))
#        explora(formula)insertar
#        formula, pure_assignment = pure_literal(formula)
        formula.unitprop2(probs)
#        print(listae)
#        formula.poda()
        if formula.contradict:
            return []
        asignaciones = asignaciones+ list(formula.unit)
       
        if not formula.listaclaus:
            return asignaciones
            

        propaga(formula,probs)
        
        if formula.contradict:
            return []
        

        variable = obtenerVariable(probs)
        
#        print('v ', variable)
        if variable == 0:
            return []
        formula1 = formula.restringe(variable)
        probs1 = probs.copy()
        probs1.pop(abs(variable))
        solucion = backtracking(formula1, asignaciones+ [variable],probs1)
        
        if not formula1.contradict:
            
            return solucion
        
        
        probs1 = probs.copy()
        probs1.pop(abs(variable))   
        formula2 = formula.restringe(-variable)
        solucion = backtracking(formula2, asignaciones + [-variable],probs1)
        if not formula2.contradict:   
            
            return solucion
        formula.contradict=True
        return []
    

    
    

    
def obtenerVariable(probs):
        
        vmin = min(probs.keys(),key = lambda x: min(probs[x],1-probs[x]))
        
        if (probs[vmin]>0.5):
            return vmin
        else:
            return -vmin
    
    
                   
     
def inicia(formula):    

    probs = dict()
    for v in formula.listavar:
        probs[v] = 0.5


    return probs    
                   
                       

        
    
    


        
    
def main(info):
        
#        info.calculadep()
#        print("salgo de explodefra")
#        info.equivprop()
        
#        self.conjuntoclau.satura()
#        info.satura2()
#        print(info.unit)      
        



        info.unitprop()
             
        
        
#        print(lista)
       
#        todas = info.calculartodasbloqueadas()
#        print ("bloqueadas",todas)
        probs = inicia(info)
        propaga(info,probs,N=1)
        lista = [2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 16, 17, 18, 21, 23, 24, 25, 30, 32, 33, 34, 36, 37, 39, 46, 49, 51, 52, 54, 55, 56, 58, 61, 65, 66, 67, 68, 69, 71, 74, 79, 84, 85, 86, 87, 88, 94, 97, 102, 104, 105, 107, 108, 109, 110, 112, 114, 115, 116, 117, 118, 121, 122, 125, 126, 128, 130, 132, 133, 138, 140, 141, 142, 145, 146, 147, 149, 151, 152, 153, 155, 159, 160, 161, 163, 167, 172, 173, 174, 175, 177, 178, 179, 180, 182, 185, 187, 190, 191, 192, 193, 196, 200, 201, 202, 207, 208, 209, 211, -300, -298, -297, 216, -295, -294, 219, 220, 221, 222, 223, -291, -287, -290, -285, 227, 228, -289, 232, -280, 235, -277, -275, -274, -273, 237, -271, 242, 244, 245, -266, 247, 248, -265, 250, 251, -261, -268, 254, -257, 255, -258, 256, 259, -253, 260, -252, 263, -249, 264, 262, 267, -246, 269, -243, -241, 272, -239, -240, 270, 276, -238, 278, 279, -233, -231, -230, 283, 284, 282, 286, -225, 288, -224, -226, -229, 292, 293, -218, -217, 296, -215, -214, -213, 299, -212, -210, -206, -205, -204, -203, -199, -198, -197, -195, -194, -189, -188, -186, -184, -183, -181, -176, -171, -170, -169, -168, -166, -165, -164, -236, -162, -158, -157, -156, -154, -234, -150, -148, -144, -143, -139, -137, -136, -135, -134, -131, -129, -127, -124, -123, 281, -120, -119, -113, -111, -106, -103, -101, -100, -99, -98, -96, -95, -93, -92, -91, -90, -89, -83, -82, -81, -80, -78, -77, -76, -75, -73, -72, -70, -64, -63, -62, -60, -59, -57, -53, -50, -48, -47, -45, -44, -43, -42, -41, -40, -38, -35, -31, -29, -28, -27, -26, -22, -20, -19, -15, -14, -10, -3, -1]
        
        
        for x in lista:
            if abs(x) in probs:
                print(x,probs[abs(x)])
                
        lista1 = []
        lista2 = []
        for x in lista:
            if abs(x) in probs:
                if x>0:
                    lista1.append(probs[abs(x)])
                else:
                    lista2.append(probs[abs(x)])
        print("pos",sum(lista1)/len(lista1))
        print("neg",sum(lista2)/len(lista2))
        
        configura = backtracking(info,[],probs)
        
        if info.contradict:
            configura = []
            print("Inconsistente")
            
        else:
            print("Consistente", len(configura),configura)
        
  
ttotal = 0
i = 0
reader=open('entrada',"r")

while reader:
    nombre = reader.readline().rstrip()             
    t1 = time()
    i +=1
    info = leeArchivoGlobal(nombre)
    t2= time()



#info = leeArchivoSet('SAT_V144C560.cnf')

#print(info.listavar)

    

#print(problema.conjuntoclau.listavar)


    



    
#    problema.explora()

    t4 = time()
    

#problema.originalpotentials = problema.totaloriginal.extraePotentials(problema.ordenbo,problema.conjuntosvar)

    main(info)
    
    t5 = time()



#info2 = leeArchivoGlobal('SAT_V1168C4675.cnf')
#info2 = leeArchivoGlobal('aes_32_1_keyfind_1.cnf')
#    info2 = leeArchivoGlobal(nombre)
#info2 = leeArchivoGlobal('SAT_V153C408.cnf')

#    info2.compruebasol(problema.configura)

    print("tiempo lectura ",t2-t1)
#    print("tiempo inicio ",t3-t2)
#    print("tiempo borrado ",t4-t3)
    print("tiempo busqueda ",t5-t4)

    print("tiempo TOTAL ",t5-t1)
    ttotal += t2-t1

print ("tiempo medio ", ttotal/i)