# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import math
from GlobalClausulas import * 

class arbolsinvar:
    def __init__(self):
        self.var = 0
        self.value = SimpleClausulas()
        self.hijos = [None,None,None]
        self.contradict = False
    
        
    def asignavar(self,p):
        self.var = p
        self.value = None

        self.hijos[0] = arbolsinvar()
        self.hijos[1] = arbolsinvar()
        self.hijos[2] = arbolsinvar()

        
        
    def asignaval(self,x):
        self.var = 0
        self.value = x
        self.hijos = [None,None,None]
        
        
    def asignahijo(self,t,i):
        self.hijos[i] = t
        
    def imprime(self):
        if (self.var == 0):
            print("valor " , self.value.listaclaus)
        else:
            print ("variable ",self.var)
            print("hijo 1")
            self.hijos[0].imprime()
            print("hijo 2")
            self.hijos[1].imprime()
            print("hijo 2")
            self.hijos[2].imprime()
        
        
    def computefromSat(self,x):
#        print(self.listavar)
#        print(x.listaclaus)
        if x.contradict:
                self.asignaval(0.0)
                return
        if len(x.listaclaus)== 0:
            self.asignaval(1.0)
        else:
            var = x.computevar()
            self.asignavar(var)
            x1 = x.restringe(-var)
            self.hijos[0].computefromSat(x1)
            x1 = x.restringe(var)
            self.hijos[1].computefromSat(x1)
                
        
    def select(self,x):
        if self.var == 0:
            return self
        elif self.var == abs(x):
            if x<0:
                return self.hijos[0]
            else:
                return self.hijos[1]
        else:
            t = arbolsinvar()
            t.var = self.var
            t.value = 0.0
            t.hijos[0] = self.hijos[0].select(x)
            t.hijos[1] = self.hijos[1].select(x)
        return t
    
    def setvalue(self,c,x):
        if self.var == 0:
            if (len(c)==0):
                self.value = x
            else:
                cval = c.pop()
                oldvalue = self.value
                self.var = abs(cval)
        
                hijo0 = arbolsinvar()
                hijo1 = arbolsinvar()
                hijo0.asignaval(oldvalue)
                hijo1.asignaval(oldvalue)
                if (cval>0):
                    hijo1.setvalue(c,x)
                else:
                    hijo0.setvalue(c,x)
                self.hijos = [hijo0,hijo1]
                
        else:
            if self.var in c:
                c.remove(self.var)
                self.hijos[1].setvalue(c,x)
            elif -self.var  in c:
                c.remove(-self.var)
                self.hijos[0].setvalue(c,x)   
            else:
                cp = c.copy()
                self.hijos[0].setvalue(c,x)
                self.hijos[1].setvalue(cp,x)
    
    def computevalconfig(self,c):
        if self.var == 0:
            return self.value
        elif self.var in c:
            return self.hijos[1].computevalconfig(c)
        elif -self.var in c:
            return self.hijos[0].computevalconfig(c)
        else:
            return -1
    
    def selectconfig(self,c):
        
#        print("entro en select config",c,self.var)
        if self.var == 0:
#            print ("devuelvo vacio",self.var)
            t = arbolsinvar()
            t.var = 0
            t.value = self.value
            return t
        elif self.var in c:
             return self.hijos[1].selectconfig(c)
#            print ("devuelvo positivo",cr1,self.var)
         
        elif -self.var in c:
            return self.hijos[0].selectconfig(c)
#            print ("devuelvo negativo" , cr2,self.var)
        else:
            t = arbolsinvar()
            t.var = self.var
            t.value = 0.0
            v1 = self.hijos[1].selectconfig(c)
            v0 = self.hijos[0].selectconfig(c)
            t.hijos[0] = v0
            t.hijos[1] = v1
#            print("devuelvo dos ",cr0,cr1,self.var)
            
            return t
        
    def multval(self,x):
        t = arbolsinvar()
        if self.var == 0:
           
            t.asignaval(x*self.value)
        else:
            v = self.var
            t.asignavar(v)
            t.hijos[0] = self.hijos[0].multval(x)
            t.hijos[1] = self.hijos[1].multval(x)
        return t
    
    def sumaval(self,x):
        t = arbolsinvar()
        if self.var == 0:
            t.asignaval(x+self.value)
        else:
            v = self.var
            t.asignavar(v)
            t.hijos[0] = self.hijos[0].sumaval(x)
            t.hijos[1] = self.hijos[1].sumaval(x)
        return t
    
    def combina(self,t2):
        
        if (self.var == 0):
            t =  t2.multval(self.value)
        elif (t2.var == 0):
            t =  self.multval(t2.value)
        else:
            h0 = self.hijos[0]
            h1 = self.hijos[1]
            t = arbolsinvar()
            t.asignavar(self.var)
            t.hijos[0] = h0.combina(t2.select(-self.var))
            t.hijos[1] = h1.combina(t2.select(self.var))
         
        return t
    
    def suma(self,t2):
        
        if (self.var == 0):
            t =  t2.sumaval(self.value)
        elif (t2.var == 0):
            t =  self.sumaval(t2.value)
        else:
            h0 = self.hijos[0]
            h1 = self.hijos[1]
            t = arbolsinvar()
            t.asignavar(self.var)
            t.hijos[0] = h0.suma(t2.select(-self.var))
            t.hijos[1] = h1.suma(t2.select(self.var))
        return t
    
    
    
    def marginaliza(self,v):
        if (self.var == 0):
            t = arbolsinvar()
            t.asignaval(self.value*2)
        elif self.var == v:
            t = self.hijos[0].suma(self.hijos[1])
        else:
            t = arbolsinvar()
            t.var = self.var
            t.hijos[0] = self.hijos[0].marginaliza(v)
            t.hijos[1] = self.hijos[1].marginaliza(v)
        return t
            
    
 
            
    def total(self,listavar):
        if (self.var == 0):
            return self.value*2**(len(listavar))
        else:
            return self.hijos[0].total(listavar-{self.var}) + self.hijos[1].total(listavar-{self.var})
        
        
 
            
    def totalv(self,listavar,x):
        if (self.var == 0):
            return self.value*2**(len(listavar-{x}))
        elif self.var == x:
            return self.hijos[1].total(listavar-{self.var})
        elif self.var == -x:
            return self.hijos[0].total(listavar-{self.var})
        else:
            return self.hijos[0].totalv(listavar-{self.var},x) + self.hijos[1].totalv(listavar-{self.var},x)
            
    def poda(self,epsilon,listavar):
        globalsum = self.total(listavar)
        self.podarec(epsilon,globalsum,listavar)
        
    def podarec(self,epsilon,globalsum,listavar):
        if (self.var == 0):
            return True
        else:
            v = self.var
            p1 = self.hijos[0].podarec(epsilon,globalsum,listavar-{v})
            p2 = self.hijos[1].podarec(epsilon,globalsum,listavar-{v})
            if p1 and p2:
                x1 = self.hijos[0].value
                x2 = self.hijos[1].value
                size = 2**len(listavar -{v})
                suma = x1 +x2
                if (x1>0) :
                    e1 = -x1*math.log(x1*size)
                else:
                    e1 = 0.0
                if (x2>0) :
                    e2 = -x2*math.log(x2*size)
                else:
                    e2 = 0.0
                if(suma ==0):
                    info = 0
                else:
                    entropy =size*(e1+e2)
                    info =  suma*size*(math.log(2) - math.log(size* suma)) -  entropy
                    info = info/globalsum
                if (info<=epsilon):
#                    print(info,epsilon,x1,x2)
                    self.asignaval((x1+x2)/2.0)
#                    print("podando")
                    return True
                else:
                    return False
            return False
                
                
            
        
        
        
            
        