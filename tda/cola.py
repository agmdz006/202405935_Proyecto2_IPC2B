from .nodo import Nodo

class Cola:
    """Cola (FIFO) implementada desde cero"""
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamaño = 0
    
    def encolar(self, dato):
        """Agregar elemento al final de la cola"""
        nuevo_nodo = Nodo(dato)
        if self.final is None:
            self.frente = self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.tamaño += 1
    
    def desencolar(self):
        """Remover y retornar elemento del frente de la cola"""
        if self.frente is None:
            return None
        
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamaño -= 1
        return dato
    
    def ver_frente(self):
        """Ver elemento del frente sin removerlo"""
        if self.frente is None:
            return None
        return self.frente.dato
    
    def esta_vacia(self):
        """Verificar si la cola está vacía"""
        return self.frente is None
    
    def obtener_tamaño(self):
        """Obtener tamaño de la cola"""
        return self.tamaño
    
    def iterar(self):
        """Generador para iterar sobre la cola"""
        actual = self.frente
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
