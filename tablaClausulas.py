# -*- coding: utf-8 -*-
"""
Created on 31 Enero 2022

@author: Serafin
"""
 
from xmlrpc.client import boolean
import networkx as nx
import numpy as np
from SimpleClausulas import * 


class nodoTabla:

    
    def __init__(self, lista):
        
        self.listavar = lista
        n = len(lista)
        t = (2,)*n
        self.tabla = np.ones( dtype = boolean, shape = t)
    
    def copia(self):
        result = nodoTabla(self.listavar.copy())
        result.tabla = self.tabla.copy()
        return result
    

    def combina(self,op,inplace = False, des= False):
        result = self if inplace else self.copia()
        if isinstance(op,boolean):
            if op:
                return result
            else:
                result.tabla = result.tabla & op
                return result

        if not des:
            op = op.copia()
        extra = set(op.listavar) - set(result.listavar)
        if extra:
                slice_ = [slice(None)] * len(result.listavar)
                slice_.extend([np.newaxis] * len(extra))

                result.tabla = result.tabla[tuple(slice_)]

                result.listavar.extend(extra)

        extra = set(result.listavar) - set(op.listavar)
        if extra:
                slice_ = [slice(None)] * len(op.listavar)
                slice_.extend([np.newaxis] * len(extra))

                op.tabla = op.tabla[tuple(slice_)]

                op.listavar.extend(extra)
                # No need to modify cardinality as we don't need it.

            # rearranging the axes of phi1 to match phi
        for axis in range(result.tabla.ndim):
            exchange_index = op.listavar.index(result.listavar[axis])
            op.listavar[axis], op.listavar[exchange_index] = (
                op.listavar[exchange_index],
                op.listavar[axis],
            )
            op.tabla = op.tabla.swapaxes(axis, exchange_index)

        result.tabla = result.tabla & op.tabla    
        if not inplace:
            return result

    def reduce(self, val, inplace=False):
        
        values = filter(lambda x: abs(x) in  self.listavar, val)
        phi = self if inplace else self.copia()

        values = [
                (abs(var), 0 if var<0 else 1) for var in values
            ]

        var_index_to_del = []
        slice_ = [slice(None)] * len(self.listavar)
        for var, state in values:
            var_index = phi.listavar.index(var)
            slice_[var_index] = state
            var_index_to_del.append(var_index)

        var_index_to_keep = sorted(
            set(range(len(phi.listavar))) - set(var_index_to_del)
        )
        # set difference is not guaranteed to maintain ordering
        phi.listavar = [phi.listavar[index] for index in var_index_to_keep]
        

        phi.tabla= phi.tabla[tuple(slice_)]

        if not inplace:
            return phi

    
    def introducelista(self,lista):
        for cl in lista:
            self.introduceclau(cl)
    
    def introduceclau(self, values):
        for var in values:
            if abs(var) not in self.listavar:
                raise ValueError(f"La variable: {abs(var)} no está en el potencial")


        values = [
                (abs(var), 1 if var<0 else 0) for var in values
            ]

        slice_ = [slice(None)] * len(self.listavar)
        for var, state in values:
            var_index = self.listavar.index(var)
            slice_[var_index] = state

        
        # set difference is not guaranteed to maintain ordering
        

        self.tabla[tuple(slice_)] = False

        

    

    def borra(self,variables, inplace=False):

        phi = self if inplace else self.copia()   
        for var in variables:
            if var not in phi.listavar:
                raise ValueError(f"{var} no está en la lista.")

        var_indexes = [phi.listavar.index(var) for var in variables]

        index_to_keep = sorted(set(range(len(self.listavar))) - set(var_indexes))
        phi.listavar = [phi.listavar[index] for index in index_to_keep]

        phi.tabla = np.amax(phi.tabla, axis=tuple(var_indexes))

        if not inplace:
            return phi

    def contradict(self):
        return not np.amax(self.tabla)

    def calculaunit(self):
        result = set()
        n = len(self.listavar)
        total = set(range(n))
        for i in range(n):
            
            borra = tuple(total-{i})
            marg = np.amax(self.tabla,axis = borra)
            
            if not marg[0]:
                if not marg[1]:
                    result.add(0)
                    return result
                else:
                    result.add(self.listavar[i])
            elif  not marg[1]:    
                    result.add(-self.listavar[i])
        return result
          
    

def createclusters (lista):
    listasets = []
    for cl in lista:
        va = set(map(abs,cl))
        encontrado = False
        for x in listasets:
            if va <= x:
                encontrado = True
                break
            
        if not encontrado:
            listasets.append(va)

    i = 0
    j = 1
    while (i<len(listasets)-1):
        if listasets[i] <= listasets[j]:
            del listasets[i]
            j = i+1
        elif listasets[j] <= listasets[i]:
            del listasets[j]
            if j >= len(listasets):
                i += 1
                j = i+1
        else:
            j += 1
            if j >= len(listasets):
                i += 1
                j = i+1
    listaclaus = []
    for i in range(len(listasets)):
        listaclaus.append([])


    for cl in lista:
        va = set(map(abs,cl))
        for i in range(len(listasets)):
            if va <= listasets[i]:
                listaclaus[i].append(cl)
                break

    return(listasets,listaclaus)



class PotencialTabla:
        def __init__(self):
            self.unit = set()
            self.listap = []
            self.contradict = False

        def imprime(self):
            print("unit: ", self.unit)
            print("tablas ")
            for x in self.listap:
                print("vars" , x.listavar)
                print(x.tabla)

        def copia(self):
            res = PotencialTabla()
            res.unit = self.unit.copy()

            for p in self.listap:
                print(p)
                res.listap.append(p.copia())
            return res

        def computefromsimple(self,simple):
            self.unit = simple.unit.copy()
            (sets,clusters) = createclusters(simple.listaclaus)
            for i in range(len(sets)):
                x = nodoTabla(list(sets[i]))
                x.introducelista(clusters[i])
                self.listap.append(x)

        def inserta(self,p):
            self.listap.append(p)

        def insertap(self,p):
            for x in p.unit:
                self.insertaunit(x)
            for q in p.listap:
                if self.listap:
                    self.listap[0].combina(q, inplace=True, des= True)
                else: 
                    self.listap = [q]
        
        def insertaunit(self,x):
            if -x in self.unit:
                self.contradict = True
            else:
                self.unit.add(x)
            
            xp = abs(x)
            for p in self.listap:
                if xp in p.listavars:
                    p.reduce({xp}, inplace = True)

        def reduceycombina(self, val, inplace = False):
            res = PotencialTabla()
            for x in self.unit:
                if -x in val:
                    res.contradict = True
                    return res
                elif not x in val:
                    res.unit.add(x)
            t = nodoTabla([])
            for p in self.listap:
                q = p.reduce(val,inplace = False)
                t.combina(q, inplace=True)
            res.listap.append(t)
            return res



        def marginaliza(self,var, inplace = False):

            if not inplace:
                res = PotencialTabla()

                if self.contradict:
                    res.contradict = True
                    return res
                for x in self.unit:
                    if x == var:
                        res.unit = self.unit-{var}
                        res.listap = self.listap.copy()
                        return res
                    elif x== -var:
                        res.unit = self.unit-{-var}
                        res.listap = self.listap.copy()
                        return res
                    else:
                        res.unit.add(x)
                si = []
                i = 0
                
                si = self.listap.copy()

                if si:
                        si.sort(key = lambda h: - len(h.listavar) )
                        
                        p = si.pop()
                        self.listap.remove(p)
 
                        
                        while si:
                            
                            q = si.pop()
                            self.listap.remove(q)
                            p.combina(q,inplace = True, des =True)
                    
                            
                        r = p.borra([var], inplace=False)
                        
                        self.listap.append(p)
                        res.listap.append(r)
                        

                        

                return res

        def marginalizas(self,vars, inplace = False):

            if not inplace:
                res = PotencialTabla()

                if self.contradict:
                    res.contradict = True
                    return res
                uv = self.unit.intersection(set(vars))
                nvars = set(map(lambda x: -x, vars))
                nuv = self.unit.intersection(nvars)

                if uv:
                    res.unit = self.unit - uv
                    vars = vars - uv
                else:
                    res.unit = self.unit.copy()
                if nuv:
                    res.unit = res.unit - nuv
                    puv = set(map(lambda x: -x, nuv)) 
                    vars = vars - puv

                
                si = []
                
                si = self.listap.copy()

                if si:
                        si.sort(key = lambda h: - len(h.listavar) )
                        
                        p = si.pop()
                        self.listap.remove(p)
 
                        
                        while si:
                            
                            q = si.pop()
                            self.listap.remove(q)
                            p.combina(q,inplace = True, des =True)
                    
                        if vars:   
                            r = p.borra(vars, inplace=False)
                        else:
                            r = p.copia()
                        
                        self.listap.append(p)
                        res.listap.append(r)
                        
                

                        

                return res
        
        def marginalizapro(self,var, L,inplace = False):

            if not inplace:
                res = PotencialTabla()

                if self.contradict:
                    res.contradict = True
                    return res
                for x in self.unit:
                    if x == var:
                        res.unit = self.unit-{var}
                        res.listap = self.listap.copy()
                        return res
                    elif x== -var:
                        res.unit = self.unit-{-var}
                        res.listap = self.listap.copy()
                        return res
                    else:
                        res.unit.add(x)
                si = []
                for p in self.listap:
            
                
                    if var in p.listavar:
                            si.append(p)
                    else:
                            res.listap.append(p)
        
                if si:
                        p = si.pop()
                        

                        
                        for q in si:
                            
                            if len(set(p.listavar).union(set(q.listavar)))<=L:                    
                                p.combina(q,inplace = True)
                            else:
                                r = p.borra([var], inplace=False)
                                res.listap.append(r)
                                p = q
                                print("aproximo")

                            
                        r = p.borra([var], inplace=False)
                        
                        
                        res.listap.append(r)
                        

                        

                return res




            



            

    








