class Dron:
    """Clase que representa un dron regador"""
    def __init__(self, id_dron, nombre):
        self.id = id_dron
        self.nombre = nombre
        self.hilera_asignada = None
        self.posicion_actual = 0  # Posición en la hilera (0 = inicio)
        self.agua_utilizada = 0
        self.fertilizante_utilizado = 0
        self.activo = True
    
    def asignar_hilera(self, hilera):
        """Asignar dron a una hilera específica"""
        self.hilera_asignada = hilera
        self.posicion_actual = 0
    
    def mover_adelante(self):
        """Mover dron una posición adelante"""
        self.posicion_actual += 1
        return f"Adelante(H{self.hilera_asignada}P{self.posicion_actual})"
    
    def mover_atras(self):
        """Mover dron una posición atrás"""
        if self.posicion_actual > 0:
            self.posicion_actual -= 1
        return f"Atrás(H{self.hilera_asignada}P{self.posicion_actual})"
    
    def regar_planta(self, planta):
        """Regar una planta específica"""
        if planta:
            self.agua_utilizada += planta.litros_agua
            self.fertilizante_utilizado += planta.gramos_fertilizante
            planta.regar()
            return "Regar"
        return "Esperar"
    
    def esperar(self):
        """Acción de esperar"""
        return "Esperar"
    
    def finalizar(self):
        """Finalizar operaciones del dron"""
        self.activo = False
        return "Fin"
    
    def reiniciar(self):
        """Reiniciar dron al estado inicial"""
        self.posicion_actual = 0
        self.agua_utilizada = 0
        self.fertilizante_utilizado = 0
        self.activo = True
    
    def __str__(self):
        return f"Dron {self.nombre} (ID: {self.id}) - Hilera: {self.hilera_asignada}"

