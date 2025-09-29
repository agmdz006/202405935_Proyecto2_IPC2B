from tda.lista_enlazada import ListaEnlazada

class Invernadero:
    """Clase que representa un invernadero completo"""
    def __init__(self, nombre):
        self.nombre = nombre
        self.numero_hileras = 0
        self.plantas_por_hilera = 0
        self.plantas = ListaEnlazada()  # Lista de todas las plantas
        self.drones_asignados = ListaEnlazada()  # Lista de drones asignados
        self.planes_riego = ListaEnlazada()  # Lista de planes de riego
    
    def configurar_dimensiones(self, numero_hileras, plantas_por_hilera):
        """Configurar dimensiones del invernadero"""
        self.numero_hileras = numero_hileras
        self.plantas_por_hilera = plantas_por_hilera
    
    def agregar_planta(self, planta):
        """Agregar una planta al invernadero"""
        self.plantas.agregar(planta)
    
    def asignar_dron(self, dron, hilera):
        """Asignar un dron a una hilera específica"""
        dron.asignar_hilera(hilera)
        self.drones_asignados.agregar(dron)
    
    def agregar_plan_riego(self, plan):
        """Agregar un plan de riego al invernadero"""
        self.planes_riego.agregar(plan)
    
    def obtener_planta(self, hilera, posicion):
        """Obtener planta específica por hilera y posición"""
        for planta in self.plantas.iterar():
            if planta.hilera == hilera and planta.posicion == posicion:
                return planta
        return None
    
    def obtener_dron_por_hilera(self, hilera):
        """Obtener dron asignado a una hilera específica"""
        for dron in self.drones_asignados.iterar():
            if dron.hilera_asignada == hilera:
                return dron
        return None
    
    def obtener_plan_por_nombre(self, nombre_plan):
        """Obtener plan de riego por nombre"""
        for plan in self.planes_riego.iterar():
            if plan.nombre == nombre_plan:
                return plan
        return None
    
    def __str__(self):
        return f"Invernadero {self.nombre}: {self.numero_hileras} hileras x {self.plantas_por_hilera} plantas"
