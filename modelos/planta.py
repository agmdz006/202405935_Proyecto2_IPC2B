class Planta:
    """Clase que representa una planta en el invernadero"""
    def __init__(self, hilera, posicion, litros_agua, gramos_fertilizante, tipo_planta=""):
        self.hilera = hilera
        self.posicion = posicion
        self.litros_agua = litros_agua
        self.gramos_fertilizante = gramos_fertilizante
        self.tipo_planta = tipo_planta
        self.regada = False
    
    def obtener_identificador(self):
        """Obtener identificador único de la planta (H#-P#)"""
        return f"H{self.hilera}-P{self.posicion}"
    
    def regar(self):
        """Marcar la planta como regada"""
        self.regada = True
    
    def __str__(self):
        return f"Planta {self.obtener_identificador()}: {self.tipo_planta} - {self.litros_agua}L, {self.gramos_fertilizante}g"
