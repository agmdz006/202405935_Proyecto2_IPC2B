class PlantaRegada:
    """Clase para representar información de una planta regada sin usar diccionarios"""
    
    def __init__(self, hilera, posicion, dron, tiempo, agua, fertilizante):
        self.hilera = hilera
        self.posicion = posicion
        self.dron = dron
        self.tiempo = tiempo
        self.agua = agua
        self.fertilizante = fertilizante
    
    def obtener_hilera(self):
        return self.hilera
    
    def obtener_posicion(self):
        return self.posicion
    
    def obtener_dron(self):
        return self.dron
    
    def obtener_tiempo(self):
        return self.tiempo
    
    def obtener_agua(self):
        return self.agua
    
    def obtener_fertilizante(self):
        return self.fertilizante
