class AccionDron:
    """Clase para representar la acción de un dron en un tiempo específico sin usar diccionarios"""
    
    def __init__(self, nombre_dron, accion):
        self.nombre_dron = nombre_dron
        self.accion = accion
    
    def obtener_nombre_dron(self):
        return self.nombre_dron
    
    def obtener_accion(self):
        return self.accion
