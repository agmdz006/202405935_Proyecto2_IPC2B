from .nodo import Nodo

class ListaEnlazada:
    """Lista enlazada simple implementada desde cero"""
    def __init__(self):
        self.cabeza = None
        self.tamaño = 0
    
    def agregar(self, dato):
        """Agregar elemento al final de la lista"""
        nuevo_nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamaño += 1
    
    def agregar_inicio(self, dato):
        """Agregar elemento al inicio de la lista"""
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamaño += 1
    
    def obtener(self, indice):
        """Obtener elemento por índice"""
        if indice < 0 or indice >= self.tamaño:
            return None
        
        actual = self.cabeza
        for i in range(indice):
            actual = actual.siguiente
        return actual.dato
    
    def buscar(self, dato):
        """Buscar elemento en la lista"""
        actual = self.cabeza
        indice = 0
        while actual is not None:
            if actual.dato == dato:
                return indice
            actual = actual.siguiente
            indice += 1
        return -1
    
    def eliminar(self, dato):
        """Eliminar elemento de la lista"""
        if self.cabeza is None:
            return False
        
        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            self.tamaño -= 1
            return True
        
        actual = self.cabeza
        while actual.siguiente is not None:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self.tamaño -= 1
                return True
            actual = actual.siguiente
        return False
    
    def obtener_tamaño(self):
        """Obtener tamaño de la lista"""
        return self.tamaño
    
    def esta_vacia(self):
        """Verificar si la lista está vacía"""
        return self.cabeza is None
    
    def iterar(self):
        """Generador para iterar sobre la lista"""
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
