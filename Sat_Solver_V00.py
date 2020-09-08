1# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 10:14:57 2019

@author: Nizziho
"""
import os

class Archivo:
	def __init__(self):
		self.RutaEscribe = "Proceso.txt"
		self.Escribe = open(self.RutaEscribe,mode="w",encoding="utf-8")
		self.Escribe.close()

	def Escribir(self, cadena):
		self.Escribe = open(self.RutaEscribe,mode="a",encoding="utf-8")
		self.Escribe.write(cadena)
		self.Escribe.close()

	def EscribirNL(self, cadena):
		self.Escribe = open(self.RutaEscribe,mode="a+",encoding="utf-8")
		self.Escribe.write(cadena+"\n")
		self.Escribe.close()

class Proposicion:
	def __init__(self):
		self.NumVar = 0
		self.VarElim = -1
		self.Procesada = False
		self.VarLista = []

	def Agregar(self, x):
		z = 0
		while z < self.NumVar:
			if abs(self.VarLista[z]) > abs(x):
				break
			z = z + 1
		self.VarLista.insert(z, x)
		self.NumVar=self.NumVar+1
        
	def Encontrar(self, y):
		if y in self.VarLista: return True
		return False

	def Retornar(self, posicion):
		return self.VarLista[posicion]

	def Eliminar(self, e):
		self.VarLista.remove(e)

	def Ordenar(self):
		self.VarLista.sort()
		return self

class ControlVariable:
	def __init__(self, data=None):
		self._data = []      
		if not data:
			self.Original = False
			self.Num = 0
			self.Original = False
			self.Apunta = None
			self.Siguiente = None            
		else:
			self._data = list(data)            
			if self._data[0].Inicio == None:
				self._data[0].Inicio = self
			else:
				self._data[0].Fin.Siguiente = self
			self.Original = False
			self._data[0].Fin = self 
			self._data[0].Fin.Num = self._data[2] 
			self._data[0].Fin.Apunta = self._data[1]
			self._data[0].Fin.Siguiente = None  

class Nodo(object):
	def __init__(self):
		self.Inicio = None
		self.Fin = None
		self.Valor = -1
		self.N = -1
		self.Pnega = 0
		self.Pafir = 0
		self.Eliminado = False

class Control_Nodo:
	def __init__(self, Ruta):
		self._NumVar = 0
		self._NumProp = 0
		self._archivoProceso = Archivo()
		self.reader = open(Ruta, "r")
		self._Preprocesa = []
		self._PreOriginal = []
		for cadena in self.reader.readlines():            
			cadena=cadena.strip()
			if cadena[0] == "p":
				cadaux = cadena[1:].strip()
				aux = cadaux.index(" ")
				if cadaux[:cadaux.index(" ")] == "cnf":
					cadaux = cadaux[aux + 1:]
					aux = cadaux.index(" ")
					self._NumVar = int(cadaux[:aux])
					self._NumProp = int(cadaux[aux + 1:])
					self._maxPrepo = self._NumVar
					self._nodo = []
					self._vector = []
					self._nodo.append(Nodo())
					self._vector.append(0)
					i = 1
					while i < self._NumVar + 1:
						self._nodo.append(Nodo())
						self._nodo[i].N = i
						self._vector.append(i)
						i = i + 1
				print("Ejemplo de resolución SAT, con {0} variables y {1} proposiciones", self._NumVar, self._NumProp)
				self._archivoProceso.EscribirNL("Ejemplo de resolución SAT, con " + str(self._NumVar) + " variables y " + str(self._NumProp) + " proposiciones")
			elif cadena[0] == "1" or cadena[0] == "2" or cadena[0] == "3" or cadena[0] == "4" or cadena[0] == "5" or cadena[0] == "6" or cadena[0] == "7" or cadena[0] == "8" or cadena[0] == "9" or cadena[0] == "0" or cadena[0] == "-":
				cadaux = cadena.strip()
				numaux = int(cadaux[:cadaux.index(" ")])
				p = Proposicion()
				o = Proposicion()
				cadPropo = ""
				while numaux != 0:
					p.Agregar(numaux)
					o.Agregar(numaux)
					cadaux = cadaux[cadaux.index(" ") + 1:].strip()
					if len(cadPropo) > 0:
						cadPropo += " v "
					if numaux < 0:
						cadPropo += ("┐x" + str(abs(numaux)))
					else:
						cadPropo += ("x" + str(numaux))
					if cadaux == "0":
						numaux = 0
						self._archivoProceso.EscribirNL(cadPropo)
						cadPropo = ""
					else:
						numaux = int(cadaux[:cadaux.index(" ")])
				p.varElim = 0
				o.varElim = 0
				#Respaldo proposiciones originales para evaluación
				self._PreOriginal.append(o)
				#Preprocesamiento, verifica si existen proposiciones repetidas
				self.EliminaPropoContenida(self._Preprocesa, p, False)
		#print("PreOriginal={0}, PreProcesa={1}".format(len(self._PreOriginal),len(self._Preprocesa)))
		self.reader.close()
		pro = 0
		#print("Longitud de Preprocesa",self._Preprocesa[0].VarLista)
		while pro < len(self._Preprocesa):
			pPrepocesa = Proposicion()
			pPrepocesa = self._Preprocesa[pro]
			self.actualizaTamañoSuma(pPrepocesa)
			#ImprimirLista(pPrepocesa);
			if pPrepocesa.NumVar == 1:
				self._nodo[self._vector[abs(pPrepocesa.Retornar(0))]].Valor = (1 + pPrepocesa.VarLista[0] / abs(pPrepocesa.VarLista[0])) / 2 #----------
			var = 0
			while var < pPrepocesa.NumVar:
				cvEvalua = ControlVariable([self._nodo[self._vector[abs(pPrepocesa.Retornar(var))]], pPrepocesa, pPrepocesa.Retornar(var)])
				cvEvalua.Original = True
				var = var + 1
			pro = pro + 1
		#Ordena nodos en función de na * nn - na -nn
		self.OrdenarVar(1)
		y = 2
		while y <= self._NumVar:
			self._nodo[y].Inicio = self._nodo[y].Fin = None
			y = y + 1

	def actualizaTamañoSuma(self, p):
		i = 0
		while i < p.NumVar:
			variable = p.Retornar(i)
			if variable > 0:
				self._nodo[self._vector[variable]].Pafir = self._nodo[self._vector[variable]].Pafir + p.NumVar
			else:
				self._nodo[self._vector[-variable]].Pnega = self._nodo[self._vector[-variable]].Pnega + p.NumVar
			i = i + 1

	def actualizaTamañoResta(self, p):
		i = 0
		while i < p.NumVar:
			variable = p.Retornar(i)
			if variable > 0:
				self._nodo[self._vector[variable]].Pafir -= p.NumVar
			else:
				self._nodo[self._vector[-variable]].Pnega -= p.NumVar
			i = i + 1

	def Eliminacion(self):
		PropoTempAfirma = []
		PropoTempNiega = []
		#int varElimina;
		p = 1
		while p <= self._NumVar:
			x = 0
			while x < len(self._Preprocesa) and self._Preprocesa[x].VarLista[0] <= self._nodo[p].N:
				if self._Preprocesa[x].Encontrar(self._nodo[p].N) or self._Preprocesa[x].Encontrar(-self._nodo[p].N):
					self._Preprocesa.pop(x)
				x = x + 1
			print(("Elimina {0}, de total de {1}").format(p, self._NumVar))
			#varElimina = NodoEvaluar();
			#nodo[varElimina].Eliminado = true;
			self._archivoProceso.EscribirNL("\n\nVariable a Eliminar: x" + str(self._nodo[p].N))
			self._archivoProceso.EscribirNL("\nLista de Proposiciones")
			PropoTempAfirma=[]
			PropoTempNiega=[]
			cvTemp = self._nodo[p].Inicio
			PropoResultado = []
			while cvTemp != None:
				if not cvTemp.Apunta.Procesada:
					cvTemp.Apunta.Procesada = True
					cvTemp.Apunta.varElim = self._nodo[p].N
					self.actualizaTamañoResta(cvTemp.Apunta)
					if cvTemp.Num > 0:
						self.EliminaPropoContenida(PropoTempAfirma, cvTemp.Apunta, False)
					else:
						#PropoTempAfirma.Add(cvTemp.Apunta);
						self.EliminaPropoContenida(PropoTempNiega, cvTemp.Apunta, False)
				#PropoTempNiega.Add(cvTemp.Apunta);
				cvTemp = cvTemp.Siguiente
			#Imprime Listas de Proposiciones resultantes que intervienen en eliminación
			self._archivoProceso.EscribirNL("")
			#archivoProceso.EscribirNL("Lista de Proposiciones Resultantes");
			self.ImprimirLista(PropoTempAfirma,1)
			self.ImprimirLista(PropoTempNiega,1)
			self._archivoProceso.EscribirNL("")
			self._archivoProceso.EscribirNL("Resultado:")
			#Evalúa que exista presencia de variables tanto afirmadas como negadas
			if len(PropoTempAfirma) * len(PropoTempNiega) != 0:
				PropoResultado = []
				a = 0
				while a < len(PropoTempAfirma):
					b = 0
					while b < len(PropoTempNiega):
						pAux = Proposicion()
						pAux = self.EvaluaProposiciones(PropoTempAfirma[a], PropoTempNiega[b], self._nodo[p].N)
						if pAux != None:
							if pAux.NumVar == 1:
								self._nodo[self._vector[abs(pAux.VarLista[0])]].Valor = (1 + pAux.VarLista[0] / abs(pAux.VarLista[0])) / 2
							self.EliminaPropoContenida2(PropoResultado, pAux, False)
						b = b + 1
					a = a + 1
				if len(PropoResultado) > self._maxPrepo:
					limite = self._maxPrepo
				else:
					limite = len(PropoResultado)
				w = 0
				while w < limite:
					z = 0
					while z < len(self._Preprocesa):
						if abs(self._Preprocesa[z].VarLista[0]) >= abs(PropoResultado[w].VarLista[0]):
							break
						z = z + 1
					self.ImprimirLista(PropoResultado[w],2)
					self._Preprocesa.insert(z, PropoResultado[w])
					self.actualizaTamañoSuma(PropoResultado[w])
					w = w + 1
			if p < self._NumVar:
				self.OrdenarVar(p + 1)
				pro = 0
				while pro < len(self._Preprocesa):
					if self._Preprocesa[pro].Encontrar(self._nodo[p + 1].N):
						cvEvalua = ControlVariable([self._nodo[p + 1], self._Preprocesa[pro], self._nodo[p + 1].N])
					if self._Preprocesa[pro].Encontrar(-self._nodo[p + 1].N):
						cvEvalua = ControlVariable([self._nodo[p + 1], self._Preprocesa[pro], -self._nodo[p + 1].N])
					pro = pro + 1
			p = p + 1

	def EliminaPropoContenida2(self, Lista, p, actualiza):
		ingresa = True
		if len(Lista) == 0:
			Lista.append(p)
		else:
			i = 0
			while i < len(Lista):
				if (abs(Lista[i].VarLista[0]) > abs(p.VarLista[0])) or (abs(Lista[i].NumVar - p.NumVar) < 3 and (Lista[i].NumVar - p.NumVar) > 13):
					break
				if p.NumVar <= Lista[i].NumVar:
					if p.NumVar == 1:
						Lista[i].Eliminar(-p.VarLista[0]) #Elimina negado de variable, si cláusula tiene 1 sola variable
					j = 0
					while j < p.NumVar:
						if not Lista[i].Encontrar(p.Retornar(j)):
							break
						j = j + 1
					if j == p.NumVar:
						if actualiza:
							self.actualizaTamañoResta(Lista[i])
						Lista.pop(i)
						i -= 1
				else: #Elimino cláusula con mayor cantidad de variable
					j = 0
					while j < Lista[i].NumVar:
						if not p.Encontrar(Lista[i].Retornar(j)):
							break
						j = j + 1
					if j == Lista[i].NumVar:
						ingresa = False
						break
				i = i + 1
			if ingresa:
				z = 0
				while z < len(Lista):
					if Lista[z].NumVar >= p.NumVar:
						break
					z = z + 1
				Lista.insert(z, p)
		return ingresa

	def EliminaPropoContenida(self, Lista, p, actualiza):
		ingresa = True
		if len(Lista) == 0:
			Lista.append(p)
		else:
			i = 0
			while i < len(Lista):
				if (abs(Lista[i].VarLista[0]) > abs(p.VarLista[0])) or (abs(Lista[i].NumVar - p.NumVar) < 3 and (Lista[i].NumVar - p.NumVar) > 13):
					break
				if p.NumVar <= Lista[i].NumVar:
					if p.NumVar == 1:
						Lista[i].Eliminar(-p.VarLista[0]) #Elimina negado de variable, si cláusula tiene 1 sola variable
					j = 0
					while j < p.NumVar:
						if not Lista[i].Encontrar(p.Retornar(j)):
							break
						j = j + 1
					if j == p.NumVar:
						if actualiza:
							self.actualizaTamañoResta(Lista[i])
						Lista.pop(i)
						i -= 1
				else: #Elimino cláusula con mayor cantidad de variable
					j = 0
					while j < Lista[i].NumVar:
						if not p.Encontrar(Lista[i].Retornar(j)):
							break
						j = j + 1
					if j == Lista[i].NumVar:
						ingresa = False
						break
				i = i + 1
			if ingresa:
				z = 0
				while z < len(Lista):
					if abs(Lista[z].VarLista[0]) >= abs(p.VarLista[0]):
						break
					z = z + 1
				Lista.insert(z, p)
		#print("Lista de EliminaPropoContenida",Lista[0].VarLista)
		return ingresa

	def EvaluaProposiciones(self, p1, p2, e):
		cuenta = 0
		pos = -1
		pAux = Proposicion()
		vVar = p1.VarLista + p2.VarLista
		for valor in vVar:
			vVar[cuenta] = 0
			if abs(valor) != e and valor != 0:
				if not(valor in vVar):
					if not(-valor in vVar):
						pAux.Agregar(valor)
					else:
						pos = vVar.index(-valor)
						vVar[pos] = 0
						pAux = None
						break
				else:
					pos = vVar.index(valor)
					pAux.Agregar(valor)
					vVar[pos] = 0
			cuenta = cuenta + 1
		return pAux

	def OrdenarVar(self, pInicio):
		posicion = pInicio
		valNodo = self._nodo[pInicio].Pafir * self._nodo[pInicio].Pnega - self._nodo[pInicio].Pafir - self._nodo[pInicio].Pnega
		i = pInicio + 1
		while i <= self._NumVar:
			if self._nodo[i].Valor != -1:
				posicion = i
				break
			if valNodo > self._nodo[i].Pafir * self._nodo[i].Pnega - self._nodo[i].Pafir - self._nodo[i].Pnega:
				valNodo = self._nodo[i].Pafir * self._nodo[i].Pnega - self._nodo[i].Pafir - self._nodo[i].Pnega
				posicion = i
			i = i + 1
		if posicion != pInicio:
			self._vector[self._nodo[posicion].N] = pInicio
			self._vector[self._nodo[pInicio].N] = posicion
			self._nodo[0] = self._nodo[posicion]
			self._nodo[posicion] = self._nodo[pInicio]
			self._nodo[pInicio] = self._nodo[0]
			self._nodo[0] = None

	def ImprimirLista(self, Lista, band):
		if band == 1:
			i = 0
			#print(Lista,len(Lista))
			while i < len(Lista):
				linea = ""
				j = 0
				while j < Lista[i].NumVar:
					if Lista[i].Retornar(j) < 0:
						linea = linea + " v ┐x" + str(-Lista[i].Retornar(j))
					else:
						linea = linea + " v x" + str(Lista[i].Retornar(j))
					j = j + 1
				#print(linea)
				self._archivoProceso.EscribirNL(linea[3:])                
				i = i + 1
		else:
			linea = ""
			j = 0
			while j < Lista.NumVar:
				if Lista.Retornar(j) < 0:
					linea = linea + " v ┐x" + str(-Lista.Retornar(j))
				else:
					linea = linea + " v x" + str(Lista.Retornar(j))
				j = j + 1
			if len(linea) > 0:
				self._archivoProceso.EscribirNL(linea[3:])            


	def ImprimirListaConsola(self, Lista):
		linea = ""
		j = 0
		while j < Lista.NumVar:
			if Lista.Retornar(j) < 0:
				linea = linea + " v ┐x" + str(-Lista.Retornar(j))
			else:
				linea = linea + " v x" + str(Lista.Retornar(j))
			j = j + 1
		if len(linea) > 0:
			print(linea[3:])

	def Resultados(self):
		i = self._NumVar
		while i > 0:
			if self._nodo[i].Valor == -1:
				self._nodo[i].Valor = 0
				cvAux = self._nodo[i].Inicio
				while cvAux != None:
					if cvAux.Apunta.varElim == self._nodo[i].N:
						suma = 0
						j = 0
						while j < cvAux.Apunta.NumVar:
							valVar = cvAux.Apunta.Retornar(j)
							if valVar < 0:
								if self._nodo[self._vector[-valVar]].Valor == 0 or self._nodo[self._vector[-valVar]].Valor == -1:
									suma = 1
									break
							else:
								if self._nodo[self._vector[valVar]].Valor == 1 or self._nodo[self._vector[valVar]].Valor == -1:
									suma = 1
									break
							j = j + 1
						if suma == 0:
							self._nodo[i].Valor = 1
							break
					cvAux = cvAux.Siguiente
			i -= 1

	def Resultados2(self):
		valVar = 0
		#int band1, band2;
		i = self._NumVar
		while i > 0:
			#band1 = band2 = 0;
			pAuxAfirma = []
			pAuxNiega = []
			cvAux = self._nodo[i].Inicio
			while cvAux != None:
				if cvAux.Apunta.varElim == self._nodo[i].N:
					nEvalua = cvAux.Num
					self._nodo[i].Valor = (1 - nEvalua / abs(nEvalua)) / 2
					j = 0
					while j < cvAux.Apunta.NumVar:
						if self._nodo[self._vector[abs(cvAux.Apunta.VarLista[j])]].Valor == 1:
							if cvAux.Apunta.VarLista[j] > 0:
								break
						else:
							if cvAux.Apunta.VarLista[j] < 0:
								break
						j = j + 1
					if j == cvAux.Apunta.NumVar:
						if nEvalua > 0:
							pAuxAfirma.append(cvAux.Apunta)
						else:
							pAuxNiega.append(cvAux.Apunta)
				cvAux = cvAux.Siguiente
			if len(pAuxAfirma) * len(pAuxNiega) == 0:
				if len(pAuxAfirma) > 0:
					self._nodo[i].Valor = 1
				else:
					self._nodo[i].Valor = 0
			else:
				pAux = Proposicion()
				pAux = self.EvaluaProposiciones(pAuxAfirma[0], pAuxNiega[0], self._nodo[i].N)
				x = i
				while x < self._NumVar:
					if pAux.Encontrar(self._nodo[x].N):
						valVar = self._nodo[x].N
						break
					if pAux.Encontrar(-self._nodo[x].N):
						valVar = -self._nodo[x].N
						break
					x = x + 1
				pAux.varElim = self._nodo[x].N
				cv = ControlVariable([self._nodo[x], pAux, valVar])
				self._nodo[x].Valor = -1
				i = x + 1
			i -= 1

	def ImprimirResultados(self):
		print("\nTabla de Verdad de Variables\n\n")
		self._archivoProceso.EscribirNL("")
		self._archivoProceso.EscribirNL("****************************")
		self._archivoProceso.EscribirNL("Tabla de Verdad de Variables\n\n")
		i = 1
		while i <= self._NumVar:
			print("x" + str(i) + " = " + str(self._nodo[self._vector[i]].Valor))
			self._archivoProceso.EscribirNL("x" + str(i) + " = " + str(self._nodo[self._vector[i]].Valor))
			i = i + 1

	def ValidarResultado(self):
		contador = 0
		print("\nProposiciones que no cumplen: ")
		self._archivoProceso.EscribirNL("")
		self._archivoProceso.EscribirNL("Proposiciones que no cumplen: ")
		i = 0
		while i < len(self._PreOriginal):
			k = 0
			while k < self._PreOriginal[i].NumVar:
				valVar = self._PreOriginal[i].Retornar(k)
				if (valVar < 0 and self._nodo[self._vector[abs(valVar)]].Valor == 0) or (valVar > 0 and self._nodo[self._vector[valVar]].Valor == 1):
					break
				k = k + 1
			if k == self._PreOriginal[i].NumVar:
				contador = contador + 1
				print(str(contador) + " CNum" + str(i) + ".- ")
				self._archivoProceso.Escribir(str(contador) + " CNum" + str(i) + ".- ")
				self.ImprimirLista(self._PreOriginal[i],2)
				self.ImprimirListaConsola(self._PreOriginal[i])
			i = i + 1

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

def DevolverDatos(cadena):
    lista=[]
    i=cadena.index(";")
    lista.append(cadena[0:i])
    cadena=cadena[i+1:]  
    i=cadena.index(";")
    lista.append(cadena[0:i])
    cadena=cadena[i+1:]
    lista.append(cadena)
    return(lista)
    
def SeleccionarArchivo(nombre):
    ListaArchivos=[]
    contador=0
    #os.system("cls") limpiar pantalla
    print("{0:3} {1:25} {2:5} {3:5}".format("Num","Nombre de Archivo","#Var","#Prop"))
    reader=open(nombre,"r")
    for cadena in reader.readlines():
        if len(cadena.strip())>0:
            ListaArchivos.append(DevolverDatos(''.join(cadena.split())))
            contador=contador+1
            print("{0:3d} {1:25}{2:5d} {3:6d}".format(contador,ListaArchivos[contador-1][0],int(ListaArchivos[contador-1][1]),int(ListaArchivos[contador-1][2])))
    reader.close()
    sel=0
    while (sel<=0 or sel>contador) and contador>0:
        sel=int(input("\n\n Seleccione el Archivo a trabajar --> "))
    if sel>0:
        print(f"\n\nSeleccionó trabajar con el Archivo: {0}",ListaArchivos[sel - 1])
        return(ListaArchivos[sel - 1])
    else:
        print("\n\nNo se encuentra información en Archivo")
        return("")
def MenuPrincipal():
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
            fileName=SeleccionarArchivo("ArchivosSAT.txt")[0]
        elif opc==2:
            RegistrarArchivo("ArchivosSAT.txt")
        elif opc==3:
            if len(fileName)>0:
                nControl=Control_Nodo(fileName)
                nControl.Eliminacion()
                nControl.Resultados2();
        elif opc==4:
            nControl.ImprimirResultados()
            nControl.ValidarResultado()
            input("Presione ENTER para regresar al Menú principal!!")

MenuPrincipal()
#print(SeleccionarArchivo("ArchivosSAT.txt"))
