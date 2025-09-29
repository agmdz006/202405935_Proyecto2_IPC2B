class EstadisticaDron:
    """Clase para representar estadísticas de un dron sin usar diccionarios"""
    
    def __init__(self, nombre, agua, fertilizante):
        self.nombre = nombre
        self.agua = agua
        self.fertilizante = fertilizante
    
    def obtener_nombre(self):
        return self.nombre
    
    def obtener_agua(self):
        return self.agua
    
    def obtener_fertilizante(self):
        return self.fertilizante
