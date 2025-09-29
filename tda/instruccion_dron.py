class InstruccionDron:
    """Clase para representar una instrucción de dron sin usar diccionarios"""
    
    def __init__(self, dron_nombre, accion):
        self.dron_nombre = dron_nombre
        self.accion = accion
    
    def obtener_dron_nombre(self):
        return self.dron_nombre
    
    def obtener_accion(self):
        return self.accion