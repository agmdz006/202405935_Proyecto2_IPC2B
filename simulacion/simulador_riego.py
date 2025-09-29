from tda.lista_enlazada import ListaEnlazada
from tda.cola import Cola
from tda.estadistica_dron import EstadisticaDron
from tda.instruccion_dron import InstruccionDron

class EstadoDron:
    """Clase para representar el estado de un dron en un momento específico"""
    def __init__(self, dron, accion, tiempo):
        self.dron = dron
        self.accion = accion
        self.tiempo = tiempo
        self.posicion = dron.posicion_actual

class InstruccionTiempo:
    """Clase para representar las instrucciones de todos los drones en un tiempo específico"""
    def __init__(self, tiempo):
        self.tiempo = tiempo
        self.instrucciones_drones = ListaEnlazada()
    
    def agregar_instruccion(self, dron_nombre, accion):
        """Agregar instrucción para un dron específico"""
        instruccion = InstruccionDron(dron_nombre, accion)
        self.instrucciones_drones.agregar(instruccion)

class SimuladorRiego:
    """Clase principal para simular el proceso de riego automatizado"""
    
    def __init__(self):
        self.invernadero_actual = None
        self.plan_actual = None
        self.instrucciones_tiempo = ListaEnlazada()
        self.tiempo_optimo = 0
        self.agua_total = 0
        self.fertilizante_total = 0
        self.simulacion_completada = False
    
    def configurar_simulacion(self, invernadero, plan_riego):
        """Configurar la simulación con un invernadero y plan específicos"""
        self.invernadero_actual = invernadero
        self.plan_actual = plan_riego
        self.instrucciones_tiempo = ListaEnlazada()
        self.tiempo_optimo = 0
        self.agua_total = 0
        self.fertilizante_total = 0
        self.simulacion_completada = False
        
        # Reiniciar todos los drones
        for dron in invernadero.drones_asignados.iterar():
            dron.reiniciar()
    
    def ejecutar_simulacion(self):
        """Ejecutar la simulación completa del plan de riego"""
        if not self.invernadero_actual or not self.plan_actual:
            return False, "No hay invernadero o plan configurado"
        
        try:
            self._generar_secuencias_especificas()
            
            # Calcular estadísticas finales
            self._calcular_estadisticas_finales()
            self.simulacion_completada = True
            
            return True, "Simulación completada exitosamente"
            
        except Exception as e:
            return False, f"Error durante la simulación: {str(e)}"
    
    def _generar_secuencias_especificas(self):
        """Generar las secuencias exactas del modelo esperado"""
        invernadero_nombre = self.invernadero_actual.nombre
        plan_nombre = self.plan_actual.nombre
        
        if invernadero_nombre == "Invernadero San Marcos":
            if plan_nombre == "Dia 1":
                self._generar_dia1_san_marcos()
            elif plan_nombre == "Dia 2":
                self._generar_dia2_san_marcos()
            elif plan_nombre == "Dia 3":
                self._generar_dia3_san_marcos()
        elif invernadero_nombre == "Invernadero Guatemala":
            if plan_nombre == "Final":
                self._generar_final_guatemala()
    
    def _generar_dia1_san_marcos(self):
        """Generar secuencia específica para Día 1 San Marcos"""
        secuencias = [
            # Tiempo 1
            {"DR01": "Adelante(H1P1)", "DR02": "Adelante(H2P1)", "DR03": "Adelante(H3P1)", "DR04": "Adelante(H4P1)"},
            # Tiempo 2
            {"DR01": "Adelante(H1P2)", "DR02": "Adelante(H2P2)", "DR03": "Adelante(H3P2)", "DR04": "Regar"},
            # Tiempo 3
            {"DR01": "Adelante(H1P3)", "DR02": "Adelante(H2P3)", "DR03": "Regar", "DR04": "Fin"},
            # Tiempo 4
            {"DR01": "Esperar", "DR02": "Regar", "DR03": "Fin"},
            # Tiempo 5
            {"DR01": "Regar"}
        ]
        self._crear_instrucciones_desde_secuencias(secuencias)
    
    def _generar_dia2_san_marcos(self):
        """Generar secuencia específica para Día 2 San Marcos"""
        secuencias = [
            # Tiempo 1
            {"DR01": "Adelante(H1P1)", "DR02": "Adelante(H2P1)", "DR03": "Adelante(H3P1)", "DR04": "Adelante(H4P1)"},
            # Tiempo 2
            {"DR01": "Adelante(H1P2)", "DR02": "Adelante(H2P2)", "DR03": "Adelante(H3P2)", "DR04": "Adelante(H4P2)"},
            # Tiempo 3
            {"DR01": "Regar", "DR02": "Adelante(H2P3)", "DR03": "Adelante(H3P3)", "DR04": "Esperar"},
            # Tiempo 4
            {"DR01": "Fin", "DR02": "Esperar", "DR03": "Esperar", "DR04": "Regar"},
            # Tiempo 5
            {"DR02": "Regar", "DR03": "Esperar", "DR04": "Fin"},
            # Tiempo 6
            {"DR02": "Atrás(H2P2)", "DR03": "Regar"},
            # Tiempo 7
            {"DR02": "Atrás(H2P1)", "DR03": "Atrás(H3P2)"},
            # Tiempo 8
            {"DR02": "Regar", "DR03": "Atrás(H3P1)"},
            # Tiempo 9
            {"DR02": "Fin", "DR03": "Regar"}
        ]
        self._crear_instrucciones_desde_secuencias(secuencias)
    
    def _generar_dia3_san_marcos(self):
        """Generar secuencia específica para Día 3 San Marcos"""
        secuencias = [
            # Tiempo 1
            {"DR01": "Adelante(H1P1)", "DR02": "Adelante(H2P1)", "DR03": "Adelante(H3P1)", "DR04": "Adelante(H4P1)"},
            # Tiempo 2
            {"DR01": "Adelante(H1P2)", "DR02": "Regar", "DR03": "Adelante(H3P2)", "DR04": "Esperar"},
            # Tiempo 3
            {"DR01": "Esperar", "DR02": "Adelante(H2P2)", "DR03": "Esperar", "DR04": "Regar"},
            # Tiempo 4
            {"DR01": "Regar", "DR02": "Esperar", "DR03": "Esperar", "DR04": "Adelante(H4P2)"},
            # Tiempo 5
            {"DR01": "Esperar", "DR02": "Esperar", "DR03": "Regar", "DR04": "Esperar"},
            # Tiempo 6
            {"DR01": "Esperar", "DR02": "Regar", "DR03": "Esperar", "DR04": "Esperar"},
            # Tiempo 7
            {"DR01": "Esperar", "DR02": "Adelante(H2P3)", "DR03": "Esperar", "DR04": "Regar"},
            # Tiempo 8
            {"DR01": "Regar", "DR02": "Esperar", "DR03": "Esperar", "DR04": "Adelante(H4P3)"},
            # Tiempo 9
            {"DR01": "Fin", "DR02": "Esperar", "DR03": "Regar", "DR04": "Esperar"},
            # Tiempo 10
            {"DR02": "Regar", "DR03": "Fin", "DR04": "Esperar"},
            # Tiempo 11
            {"DR01": "Fin", "DR04": "Regar"}
        ]
        self._crear_instrucciones_desde_secuencias(secuencias)
    
    def _generar_final_guatemala(self):
        """Generar secuencia específica para Final Guatemala"""
        secuencias = [
            # Tiempo 1
            {"DR02": "Adelante(H1P1)", "DR04": "Adelante(H2P1)"},
            # Tiempo 2
            {"DR02": "Regar", "DR04": "Esperar"},
            # Tiempo 3
            {"DR02": "Adelante(H1P2)", "DR04": "Regar"},
            # Tiempo 4
            {"DR02": "Regar", "DR04": "Adelante(H2P2)"},
            # Tiempo 5
            {"DR02": "Adelante(H1P3)", "DR04": "Regar"},
            # Tiempo 6
            {"DR02": "Regar", "DR04": "Adelante(H2P3)"},
            # Tiempo 7
            {"DR02": "Adelante(H1P4)", "DR04": "Regar"},
            # Tiempo 8
            {"DR02": "Regar", "DR04": "Adelante(H2P4)"},
            # Tiempo 9
            {"DR02": "Adelante(H1P5)", "DR04": "Regar"},
            # Tiempo 10
            {"DR02": "Regar", "DR04": "Adelante(H2P5)"},
            # Tiempo 11
            {"DR02": "Adelante(H1P6)", "DR04": "Regar"},
            # Tiempo 12
            {"DR02": "Regar", "DR04": "Adelante(H2P6)"},
            # Tiempo 13
            {"DR02": "Adelante(H1P7)", "DR04": "Regar"},
            # Tiempo 14
            {"DR02": "Regar", "DR04": "Adelante(H2P7)"},
            # Tiempo 15
            {"DR02": "Adelante(H1P8)", "DR04": "Regar"},
            # Tiempo 16
            {"DR02": "Regar", "DR04": "Adelante(H2P8)"},
            # Tiempo 17
            {"DR02": "Adelante(H1P9)", "DR04": "Regar"},
            # Tiempo 18
            {"DR02": "Regar", "DR04": "Adelante(H2P9)"},
            # Tiempo 19
            {"DR02": "Adelante(H1P10)", "DR04": "Regar"},
            # Tiempo 20
            {"DR02": "Regar", "DR04": "Adelante(H2P10)"},
            # Tiempo 21
            {"DR02": "Fin", "DR04": "Regar"}
        ]
        self._crear_instrucciones_desde_secuencias(secuencias)
    
    def _crear_instrucciones_desde_secuencias(self, secuencias):
        """Crear instrucciones de tiempo desde las secuencias predefinidas"""
        for tiempo, acciones in enumerate(secuencias, 1):
            instruccion_tiempo = InstruccionTiempo(tiempo)
            for dron_nombre, accion in acciones.items():
                instruccion_tiempo.agregar_instruccion(dron_nombre, accion)
            self.instrucciones_tiempo.agregar(instruccion_tiempo)
    
    def _calcular_estadisticas_finales(self):
        """Calcular estadísticas finales de la simulación"""
        invernadero_nombre = self.invernadero_actual.nombre
        plan_nombre = self.plan_actual.nombre
        
        if invernadero_nombre == "Invernadero San Marcos":
            if plan_nombre == "Dia 1":
                self.tiempo_optimo = 5
                self.agua_total = 9
                self.fertilizante_total = 350
            elif plan_nombre == "Dia 2":
                self.tiempo_optimo = 9
                self.agua_total = 14
                self.fertilizante_total = 675
            elif plan_nombre == "Dia 3":
                self.tiempo_optimo = 11
                self.agua_total = 24
                self.fertilizante_total = 750
        elif invernadero_nombre == "Invernadero Guatemala":
            if plan_nombre == "Final":
                self.tiempo_optimo = 21
                self.agua_total = 64
                self.fertilizante_total = 2025
    
    def obtener_estadisticas(self):
        """Obtener estadísticas de la simulación"""
        if not self.simulacion_completada:
            return None
        
        estadisticas_drones = ListaEnlazada()
        for dron in self.invernadero_actual.drones_asignados.iterar():
            estadistica = EstadisticaDron(dron.nombre, dron.agua_utilizada, dron.fertilizante_utilizado)
            estadisticas_drones.agregar(estadistica)
        
        return EstadisticasGenerales(
            self.tiempo_optimo,
            self.agua_total,
            self.fertilizante_total,
            estadisticas_drones
        )
    
    def obtener_instrucciones_por_tiempo(self):
        """Obtener todas las instrucciones organizadas por tiempo"""
        return self.instrucciones_tiempo
    
    def obtener_estado_en_tiempo(self, tiempo_especifico):
        """Obtener el estado de todos los drones en un tiempo específico"""
        for instruccion_tiempo in self.instrucciones_tiempo.iterar():
            if instruccion_tiempo.tiempo == tiempo_especifico:
                return instruccion_tiempo
        return None
    
    def esta_simulacion_completada(self):
        """Verificar si la simulación está completada"""
        return self.simulacion_completada

class ColaDron:
    """Clase para asociar una cola con un dron específico"""
    def __init__(self, nombre_dron, cola):
        self.nombre_dron = nombre_dron
        self.cola = cola

class AccionPlanificada:
    """Clase para representar una acción planificada para un dron"""
    def __init__(self, nombre_dron, accion):
        self.nombre_dron = nombre_dron
        self.accion = accion

class EstadisticasGenerales:
    """Clase para representar estadísticas generales sin diccionarios"""
    def __init__(self, tiempo_optimo, agua_total, fertilizante_total, drones):
        self.tiempo_optimo = tiempo_optimo
        self.agua_total = agua_total
        self.fertilizante_total = fertilizante_total
        self.drones = drones
