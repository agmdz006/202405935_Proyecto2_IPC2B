class Nodo:
    """Nodo básico para estructuras de datos enlazadas"""
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None
        self.anterior = None  # Para listas doblemente enlazadas
