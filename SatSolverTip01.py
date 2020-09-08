from time import time
import copy

def extraerDatos(filename):
    ltclausulas = []
    for cadena in open(filename):
        if cadena.startswith('c'):
            continue
        if cadena.startswith('p'):
            n_vars = cadena.split()[2]
            continue
        clausula = [int(x) for x in cadena[:-2].split()]
        ltclausulas.append(clausula)

    return ltclausulas, int(n_vars)

  #%%          
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



#%%
def propagacion_unitaria(formula):
    asignaciones = []
    clausula_unica=[]
    for c in formula:
        if len(c)==1:
            clausula_unica=clausula_unica+[c]
            break
    while clausula_unica:
        varUnica = clausula_unica[0]
        formula = bcp(formula, varUnica[0])
        asignaciones += [varUnica[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, asignaciones
        for c in formula:
            clausula_unica=[]
            if len(c)==1:
                clausula_unica=clausula_unica+[c]
                break
    return formula, asignaciones
#%%
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

#%%
def backtracking(formula, asignaciones):
    formula, pure_assignment = pure_literal(formula)
    formula, unit_assignment = propagacion_unitaria(formula)
    asignaciones = asignaciones+ pure_assignment+ unit_assignment
    if formula == - 1:
        return []
    if not formula:
        return asignaciones
    variable = obtenerVariable(formula)
    solucion = backtracking(bcp(formula, variable), asignaciones+ [variable])
    if not solucion:
        solucion = backtracking(bcp(formula, -variable), asignaciones + [-variable])
    return solucion

#%%
def simplificarClausula(formula):
    solucionInicial=[]
    print("Numero de clausulas inicial",len(formula))
    var=varUnitarias(formula)
    while(not var==0):
        solucionInicial=solucionInicial+[var]
        formula=bcp(formula,var)
        if formula==-1:
            return formula,solucionInicial
        var=varUnitarias(formula)
    print("Numero de clausulas final",len(formula))
    return formula,solucionInicial

#%%       
def varUnitarias(formula):
#    print(formula)
    for i in formula:
        if len(i)==1:
            return i[0]
    return 0
        
#%%        
def obtenerVariable(formula):
     apariciones = aparicionesTotal(formula)
     return max(apariciones, key=apariciones.get)

#%% 
def comprobarSolucion(formula,solucion):
    if solucion:
        solucion.sort(key=abs)
        for i in formula:
            if not esVerdadera(solucion,i):
                print("UNSAT")
                break
        print("SAT")
        print(solucion)
    else:
        print ("UNSAT")
        
def esVerdadera(solucion,clausula):
    for lit in clausula:
        if lit in solucion:
            return True
    return False
    
#%% 
def aparicionesTotal(formula):
    apariciones = {}
    for clausula in formula:
        for literal in clausula:
            if abs(literal) in apariciones:
                apariciones[abs(literal)] +=2** -len(clausula)
            else:
                apariciones[abs(literal)] = 2**-len(clausula)
    return apariciones


#%% 

ti=time()
ltclausulas, n_vars = extraerDatos(r"SAT_V300C1016.cnf")
tf=time()
print("Tiempo de lectura",tf-ti)

ti=time()
formula=copy.deepcopy(ltclausulas)
ltclausulas,solucionInicial=simplificarClausula(ltclausulas)

if ltclausulas==-1:
    print("UNSAT")
else:
    tf=time()
    print("Tiempo de pre-procesamiento",tf-ti)
    
    
    
    ti=time()
    ltclausulas.sort(key=len,reverse=True)
    solucion = backtracking(ltclausulas, [])
    tf=time()
    print("Tiempo de procesamiento",tf-ti)
    
    
    if solucion:
        solucion=solucion+solucionInicial
    ti=time()
    comprobarSolucion(formula,solucion)
    tf=time()
    print("Tiempo de comprobacion",tf-ti)



