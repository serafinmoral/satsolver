# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 19:23:34 2019

@author: Nizziho
"""

# -*- coding: utf-8 -*-
"""
Clase: Archivo

@author: Nizziho
"""

class Archivo:
	def __init__(self):
		self.RutaEscribe = "Proceso.txt"
		self.Escribe = open(self.RutaEscribe,"w")
		self.Escribe.close()

	def Escribir(self, cadena):
		self.Escribe = open(self.RutaEscribe,"a")
		self.Escribe.write(cadena)
		self.Escribe.close()

	def EscribirNL(self, cadena):
		self.Escribe = open(self.RutaEscribe,"a")
		self.Escribe.write(cadena + "\n")
		self.Escribe.close()

"""
Clase: Proposición

@author: Nizziho
"""
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
			z += 1
		self.VarLista.insert(z, x)
        
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

"""
Clase: ControlVariable

@author: Nizziho
"""
class ControlVariable:
	def __init__(self, data=None):
		_data = []      
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
				_data[0].Fin.Siguiente = self
			self.Original = False
			self._data[0].Fin = self 
			self._data[0].Fin.Num = self._data[2] 
			self._data[0].Fin.Apunta = self._data[1]
			self._data[0].Fin.Siguiente = None  

"""
Clase: Control_Nodo

@author: Nizziho
"""
class Control_Nodo:
	def __init__(self, Ruta):
		self._NumVar = 0
		self._NumProp = 0
		self._archivoProceso = Archivo()
		stream = FileStream(Ruta, FileMode.Open, FileAccess.Read)
		reader = StreamReader(stream)
		self._Preprocesa = List[Proposicion]()
		self._PreOriginal = List[Proposicion]()
		self._nodo = Array.CreateInstance(Nodo, 0)
		self._vector = Array.CreateInstance(int, 0)
		while reader.Peek() > -1:
			cadena = reader.ReadLine()
			if cadena.Trim().Substring(0, 1) == "p":
				cadaux = cadena.Substring(1).Trim()
				aux = cadaux.IndexOf(" ")
				if cadaux.Substring(0, cadaux.IndexOf(" ")) == "cnf":
					cadaux = cadaux.Substring(aux + 1)
					aux = cadaux.IndexOf(" ")
					self._NumVar = int.Parse(cadaux.Substring(0, aux))
					self._NumProp = int.Parse(cadaux.Trim().Substring(aux + 1))
					self._maxPrepo = self._NumVar
					self._nodo = Array.CreateInstance(Nodo, self._NumVar + 1)
					self._vector = Array.CreateInstance(int, self._NumVar + 1)
					i = 1
					while i < self._NumVar + 1:
						self._nodo[i] = Nodo()
						self._nodo[i].N = i
						self._vector[i] = i
						i += 1
				Console.WriteLine("Ejemplo de resolución SAT, con {0} variables y {1} proposiciones", self._NumVar, self._NumProp)
				self._archivoProceso.EscribirNL("Ejemplo de resolución SAT, con " + self._NumVar + " variables y " + self._NumProp + " proposiciones")
			elif cadena.Trim().Substring(0, 1) == "1" or cadena.Trim().Substring(0, 1) == "2" or cadena.Trim().Substring(0, 1) == "3" or cadena.Trim().Substring(0, 1) == "4" or cadena.Trim().Substring(0, 1) == "5" or cadena.Trim().Substring(0, 1) == "6" or cadena.Trim().Substring(0, 1) == "7" or cadena.Trim().Substring(0, 1) == "8" or cadena.Trim().Substring(0, 1) == "9" or cadena.Trim().Substring(0, 1) == "0" or cadena.Trim().Substring(0, 1) == "-":
				cadaux = cadena.Trim()
				numaux = int.Parse(cadaux.Substring(0, cadaux.IndexOf(" ")))
				p = Proposicion()
				o = Proposicion()
				cadPropo = ""
				while numaux != 0:
					p.Agregar(numaux)
					o.Agregar(numaux)
					cadaux = cadaux.Substring(cadaux.IndexOf(" ") + 1).Trim()
					if cadPropo.Length > 0:
						cadPropo += " v "
					if numaux < 0:
						cadPropo += ("┐x" + Math.Abs(numaux).ToString())
					else:
						cadPropo += ("x" + numaux.ToString())
					if cadaux == "0":
						numaux = 0
						self._archivoProceso.EscribirNL(cadPropo)
						cadPropo = ""
					else:
						numaux = int.Parse(cadaux.Substring(0, cadaux.IndexOf(" ")))
				p.varElim = 0
				o.varElim = 0
				#Respaldo proposiciones originales para evaluación
				self._PreOriginal.Add(o)
				#Preprocesamiento, verifica si existen proposiciones repetidas
				self.EliminaPropoContenida(self._Preprocesa, p)
		#Proposicion pp  = PreOriginal[6376];
		reader.Close()
		pro = 0
		while pro < self._Preprocesa.Count():
			pPrepocesa = Proposicion()
			pPrepocesa = self._Preprocesa[pro]
			self.actualizaTamañoSuma(pPrepocesa)
			#ImprimirLista(pPrepocesa);
			if pPrepocesa.numVar == 1:
				self._nodo[self._vector[Math.Abs(pPrepocesa.Retornar(0))]].Valor = (1 + pPrepocesa.Lista[0] / Math.Abs(pPrepocesa.Lista[0])) / 2 #----------
			var = 0
			while var < pPrepocesa.numVar:
				cvEvalua = ControlVariable(self._nodo[self._vector[Math.Abs(pPrepocesa.Retornar(var))]], pPrepocesa, pPrepocesa.Retornar(var))
				cvEvalua.Original = True
				var += 1
			pro += 1
		#Ordena nodos en función de na * nn - na -nn
		self.OrdenarVar(1)
		y = 2
		while y <= self._NumVar:
			self._nodo[y].Inicio = self._nodo[y].Fin = None
			y += 1

	def actualizaTamañoSuma(self, p):
		i = 0
		while i < p.numVar:
			variable = p.Retornar(i)
			if variable > 0:
				self._nodo[self._vector[variable]].PAfir += p.numVar
			else:
				self._nodo[self._vector[-variable]].PNega += p.numVar
			i += 1

	def actualizaTamañoResta(self, p):
		i = 0
		while i < p.numVar:
			variable = p.Retornar(i)
			if variable > 0:
				self._nodo[self._vector[variable]].PAfir -= p.numVar
			else:
				self._nodo[self._vector[-variable]].PNega -= p.numVar
			i += 1

	def Eliminacion(self):
		PropoTempAfirma = List[Proposicion]()
		PropoTempNiega = List[Proposicion]()
		#int varElimina;
		p = 1
		while p <= self._NumVar:
			x = 0
			while x < self._Preprocesa.Count() and self._Preprocesa[x].Lista[0] <= self._nodo[p].N:
				if self._Preprocesa[x].Encontrar(self._nodo[p].N) or self._Preprocesa[x].Encontrar(-self._nodo[p].N):
					self._Preprocesa.RemoveAt(x)
				x += 1
			Console.WriteLine("Elimina {0}, de total de {1}", p, self._NumVar)
			#varElimina = NodoEvaluar();
			#nodo[varElimina].Eliminado = true;
			self._archivoProceso.EscribirNL("")
			self._archivoProceso.EscribirNL("")
			self._archivoProceso.EscribirNL("Variable a Eliminar: x" + self._nodo[p].N.ToString())
			self._archivoProceso.EscribirNL("")
			self._archivoProceso.EscribirNL("Lista de Proposiciones")
			PropoTempAfirma.Clear()
			PropoTempNiega.Clear()
			cvTemp = self._nodo[p].Inicio
			PropoResultado = List[Proposicion]()
			while cvTemp != None:
				if not cvTemp.Apunta.procesada:
					cvTemp.Apunta.procesada = True
					cvTemp.Apunta.varElim = self._nodo[p].N
					self.actualizaTamañoResta(cvTemp.Apunta)
					if cvTemp.Num > 0:
						self.EliminaPropoContenida(PropoTempAfirma, cvTemp.Apunta)
					else:
						#PropoTempAfirma.Add(cvTemp.Apunta);
						self.EliminaPropoContenida(PropoTempNiega, cvTemp.Apunta)
				#PropoTempNiega.Add(cvTemp.Apunta);
				cvTemp = cvTemp.Siguiente
			#Imprime Listas de Proposiciones resultantes que intervienen en eliminación
			self._archivoProceso.EscribirNL("")
			#archivoProceso.EscribirNL("Lista de Proposiciones Resultantes");
			self.ImprimirLista(PropoTempAfirma)
			self.ImprimirLista(PropoTempNiega)
			self._archivoProceso.EscribirNL("")
			self._archivoProceso.EscribirNL("Resultado:")
			#Evalúa que exista presencia de variables tanto afirmadas como negadas
			if PropoTempAfirma.Count * PropoTempNiega.Count != 0:
				PropoResultado = List[Proposicion]()
				a = 0
				while a < PropoTempAfirma.Count:
					b = 0
					while b < PropoTempNiega.Count:
						pAux = Proposicion()
						pAux = self.EvaluaProposiciones(PropoTempAfirma[a], PropoTempNiega[b], self._nodo[p].N)
						if pAux != None:
							if pAux.numVar == 1:
								self._nodo[self._vector[Math.Abs(pAux.Lista[0])]].Valor = (1 + pAux.Lista[0] / Math.Abs(pAux.Lista[0])) / 2
							self.EliminaPropoContenida2(PropoResultado, pAux)
						b += 1
					a += 1
				if PropoResultado.Count > self._maxPrepo:
					limite = self._maxPrepo
				else:
					limite = PropoResultado.Count
				w = 0
				while w < limite:
					z = 0
					while z < self._Preprocesa.Count():
						if Math.Abs(self._Preprocesa[z].Lista[0]) >= Math.Abs(PropoResultado[w].Lista[0]):
							break
						z += 1
					self.ImprimirLista(PropoResultado[w])
					self._Preprocesa.Insert(z, PropoResultado[w])
					self.actualizaTamañoSuma(PropoResultado[w])
					w += 1
			if p < self._NumVar:
				self.OrdenarVar(p + 1)
				pro = 0
				while pro < self._Preprocesa.Count():
					if self._Preprocesa[pro].Encontrar(self._nodo[p + 1].N):
						cvEvalua = ControlVariable(self._nodo[p + 1], self._Preprocesa[pro], self._nodo[p + 1].N)
					if self._Preprocesa[pro].Encontrar(-self._nodo[p + 1].N):
						cvEvalua = ControlVariable(self._nodo[p + 1], self._Preprocesa[pro], -self._nodo[p + 1].N)
					pro += 1
			p += 1

	def EliminaPropoContenida2(self, Lista, p, actualiza):
		ingresa = True
		if Lista.Count == 0:
			Lista.Add(p)
		else:
			i = 0
			while i < Lista.Count():
				if (Math.Abs(Lista[i].Lista[0]) > Math.Abs(p.Lista[0])) or (Math.Abs(Lista[i].numVar - p.numVar) < 3 and (Lista[i].numVar - p.numVar) > 13):
					break
				if p.numVar <= Lista[i].numVar:
					if p.numVar == 1:
						Lista[i].Eliminar(-p.Lista[0]) #Elimina negado de variable, si cláusula tiene 1 sola variable
					j = 0
					while j < p.numVar:
						if not Lista[i].Encontrar(p.Retornar(j)):
							break
						j += 1
					if j == p.numVar:
						if actualiza:
							self.actualizaTamañoResta(Lista[i])
						Lista.RemoveAt(i)
						i -= 1
				else: #Elimino cláusula con mayor cantidad de variable
					j = 0
					while j < Lista[i].numVar:
						if not p.Encontrar(Lista[i].Retornar(j)):
							break
						j += 1
					if j == Lista[i].numVar:
						ingresa = False
						break
				i += 1
			if ingresa:
				z = 0
				while z < Lista.Count():
					if Lista[z].numVar >= p.numVar:
						break
					z += 1
				Lista.Insert(z, p)
		return ingresa

	def EliminaPropoContenida(self, Lista, p, actualiza):
		ingresa = True
		if Lista.Count == 0:
			Lista.Add(p)
		else:
			i = 0
			while i < Lista.Count():
				if (Math.Abs(Lista[i].Lista[0]) > Math.Abs(p.Lista[0])) or (Math.Abs(Lista[i].numVar - p.numVar) < 3 and (Lista[i].numVar - p.numVar) > 13):
					break
				if p.numVar <= Lista[i].numVar:
					if p.numVar == 1:
						Lista[i].Eliminar(-p.Lista[0]) #Elimina negado de variable, si cláusula tiene 1 sola variable
					j = 0
					while j < p.numVar:
						if not Lista[i].Encontrar(p.Retornar(j)):
							break
						j += 1
					if j == p.numVar:
						if actualiza:
							self.actualizaTamañoResta(Lista[i])
						Lista.RemoveAt(i)
						i -= 1
				else: #Elimino cláusula con mayor cantidad de variable
					j = 0
					while j < Lista[i].numVar:
						if not p.Encontrar(Lista[i].Retornar(j)):
							break
						j += 1
					if j == Lista[i].numVar:
						ingresa = False
						break
				i += 1
			if ingresa:
				z = 0
				while z < Lista.Count():
					if Math.Abs(Lista[z].Lista[0]) >= Math.Abs(p.Lista[0]):
						break
					z += 1
				Lista.Insert(z, p)
		return ingresa

	def EvaluaProposiciones(self, p1, p2, e):
		cuenta = 0
		pos = -1
		pAux = Proposicion()
		vVar = Array.CreateInstance(int, p1.numVar + p2.numVar)
		p1.Lista.CopyTo(vVar)
		p2.Lista.CopyTo(vVar, p1.numVar)
		enumerator = vVar.GetEnumerator()
		while enumerator.MoveNext():
			valor = enumerator.Current
			vVar[cuenta] = 0
			if Math.Abs(valor) != e and valor != 0:
				pos = Array.IndexOf(vVar, valor)
				if pos == -1:
					pos = Array.IndexOf(vVar, -valor)
					if pos == -1:
						pAux.Agregar(valor)
					else:
						vVar[pos] = 0
						pAux = None
						break
				else:
					pAux.Agregar(valor)
					vVar[pos] = 0
			cuenta += 1
		return pAux

	def OrdenarVar(self, pInicio):
		posicion = pInicio
		valNodo = self._nodo[pInicio].PAfir * self._nodo[pInicio].PNega - self._nodo[pInicio].PAfir - self._nodo[pInicio].PNega
		i = pInicio + 1
		while i <= self._NumVar:
			if self._nodo[i].Valor != -1:
				posicion = i
				break
			#if (valNodo > nodo[i].PAfir * nodo[i].PNega)
			#{
			#    valNodo = nodo[i].PAfir * nodo[i].PNega;
			#    posicion = i;
			#}
			if valNodo > self._nodo[i].PAfir * self._nodo[i].PNega - self._nodo[i].PAfir - self._nodo[i].PNega:
				valNodo = self._nodo[i].PAfir * self._nodo[i].PNega - self._nodo[i].PAfir - self._nodo[i].PNega
				posicion = i
			i += 1
		if posicion != pInicio:
			self._vector[self._nodo[posicion].N] = pInicio
			self._vector[self._nodo[pInicio].N] = posicion
			self._nodo[0] = self._nodo[posicion]
			self._nodo[posicion] = self._nodo[pInicio]
			self._nodo[pInicio] = self._nodo[0]
			self._nodo[0] = None

	def ImprimirLista(self, Lista):
		i = 0
		while i < Lista.Count():
			linea = ""
			j = 0
			while j < Lista[i].numVar:
				if Lista[i].Retornar(j) < 0:
					linea = linea + " v ┐x" + (-Lista[i].Retornar(j)).ToString()
				else:
					linea = linea + " v x" + Lista[i].Retornar(j).ToString()
				j += 1
			self._archivoProceso.EscribirNL(linea.Substring(3))
			i += 1

	def ImprimirLista(self, Lista):
		linea = ""
		j = 0
		while j < Lista.numVar:
			if Lista.Retornar(j) < 0:
				linea = linea + " v ┐x" + (-Lista.Retornar(j)).ToString()
			else:
				linea = linea + " v x" + Lista.Retornar(j).ToString()
			j += 1
		if linea.Length > 0:
			self._archivoProceso.EscribirNL(linea.Substring(3))

	def ImprimirListaConsola(self, Lista):
		linea = ""
		j = 0
		while j < Lista.numVar:
			if Lista.Retornar(j) < 0:
				linea = linea + " v ┐x" + (-Lista.Retornar(j)).ToString()
			else:
				linea = linea + " v x" + Lista.Retornar(j).ToString()
			j += 1
		if linea.Length > 0:
			Console.WriteLine(linea.Substring(3))

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
						while j < cvAux.Apunta.numVar:
							valVar = cvAux.Apunta.Retornar(j)
							if valVar < 0:
								if self._nodo[self._vector[-valVar]].Valor == 0 or self._nodo[self._vector[-valVar]].Valor == -1:
									suma = 1
									break
							else:
								if self._nodo[self._vector[valVar]].Valor == 1 or self._nodo[self._vector[valVar]].Valor == -1:
									suma = 1
									break
							j += 1
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
			pAuxAfirma = List[Proposicion]()
			pAuxNiega = List[Proposicion]()
			cvAux = self._nodo[i].Inicio
			while cvAux != None:
				if cvAux.Apunta.varElim == self._nodo[i].N:
					nEvalua = cvAux.Num
					self._nodo[i].Valor = (1 - nEvalua / Math.Abs(nEvalua)) / 2
					j = 0
					while j < cvAux.Apunta.numVar:
						if self._nodo[self._vector[Math.Abs(cvAux.Apunta.Lista[j])]].Valor == 1:
							if cvAux.Apunta.Lista[j] > 0:
								break
						else:
							if cvAux.Apunta.Lista[j] < 0:
								break
						j += 1
					if j == cvAux.Apunta.numVar:
						if nEvalua > 0:
							pAuxAfirma.Add(cvAux.Apunta)
						else:
							pAuxNiega.Add(cvAux.Apunta)
				cvAux = cvAux.Siguiente
			if pAuxAfirma.Count * pAuxNiega.Count == 0:
				if pAuxAfirma.Count > 0:
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
					x += 1
				pAux.varElim = self._nodo[x].N
				cv = ControlVariable(self._nodo[x], pAux, valVar)
				self._nodo[x].Valor = -1
				i = x + 1
			i -= 1

	def ImprimirResultados(self):
		Console.WriteLine("\nTabla de Verdad de Variables\n\n")
		self._archivoProceso.EscribirNL("")
		self._archivoProceso.EscribirNL("****************************")
		self._archivoProceso.EscribirNL("Tabla de Verdad de Variables\n\n")
		i = 1
		while i <= self._NumVar:
			Console.WriteLine("x" + i.ToString() + " = " + self._nodo[self._vector[i]].Valor)
			self._archivoProceso.EscribirNL("x" + i.ToString() + " = " + self._nodo[self._vector[i]].Valor)
			i += 1

	def ValidarResultado(self):
		contador = 0
		Console.WriteLine("\nProposiciones que no cumplen: ")
		self._archivoProceso.EscribirNL("")
		self._archivoProceso.EscribirNL("Proposiciones que no cumplen: ")
		i = 0
		while i < self._PreOriginal.Count():
			k = 0
			while k < self._PreOriginal[i].numVar:
				valVar = self._PreOriginal[i].Retornar(k)
				if (valVar < 0 and self._nodo[self._vector[Math.Abs(valVar)]].Valor == 0) or (valVar > 0 and self._nodo[self._vector[valVar]].Valor == 1):
					break
				k += 1
			if k == self._PreOriginal[i].numVar:
				print((contador += 1) + " CNum" + i + ".- ")
				self._archivoProceso.Escribir((contador).ToString() + " CNum" + i.ToString() + ".- ")
				self.ImprimirLista(self._PreOriginal[i])
				self.ImprimirListaConsola(self._PreOriginal[i])
			i += 1

"""
Clase: Nodo

@author: Nizziho
"""



class Nodo(object):
	def __init__(self):
		self.Inicio = None
		self.Fin = None
		self.Valor = -1
		self.N = -1
		self.Pnega = 0
		self.Pafir = 0
		self.Eliminado = False

"""
Clase: Programa

@author: Nizziho
"""


