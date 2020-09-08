# -*- coding: utf-8 -*-
"""
Clase: Archivo

@author: Nizziho
"""

class Archivo(object):
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

nodox = Nodo()
prepo = Proposicion()
prepo.Agregar(3)
prepo.Agregar(4)
prepo.Agregar(-5)
control = ControlVariable([nodox,prepo,5])
print(control.Num)

filex = Archivo()
filex.Escribir("hola ")
filex.Escribir("mundo")
filex.EscribirNL(" Ejemplo")
filex.Escribir("Nueva Linea")