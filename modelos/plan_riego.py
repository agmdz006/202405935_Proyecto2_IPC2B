from tda.lista_enlazada import ListaEnlazada

class PlanRiego:
    """Clase que representa un plan de riego"""
    def __init__(self, nombre, secuencia_riego=""):
        self.nombre = nombre
        self.secuencia_riego = secuencia_riego
        self.instrucciones = ListaEnlazada()  # Lista de instrucciones parseadas
        self.tiempo_optimo = 0
        self.agua_total = 0
        self.fertilizante_total = 0
        self.procesado = False
    
    def parsear_secuencia(self):
        """Parsear la secuencia de riego (ej: H1-P2, H2-P1, H2-P2)"""
        if not self.secuencia_riego:
            return
        
        # Limpiar y dividir la secuencia
        secuencia_limpia = self.secuencia_riego.replace(" ", "")
        instrucciones_str = secuencia_limpia.split(",")
        
        for instruccion_str in instrucciones_str:
            if instruccion_str.strip():
                # Parsear formato H#-P#
                partes = instruccion_str.strip().split("-")
                if len(partes) == 2:
                    hilera_str = partes[0].replace("H", "")
                    posicion_str = partes[1].replace("P", "")
                    
                    try:
                        hilera = int(hilera_str)
                        posicion = int(posicion_str)
                        instruccion = InstruccionRiego(hilera, posicion)
                        self.instrucciones.agregar(instruccion)
                    except ValueError:
                        continue
    
    def obtener_instrucciones(self):
        """Obtener lista de instrucciones parseadas"""
        if not self.procesado:
            self.parsear_secuencia()
            self.procesado = True
        return self.instrucciones
    
    def __str__(self):
        return f"Plan {self.nombre}: {self.secuencia_riego}"

class InstruccionRiego:
    """Clase que representa una instrucción individual de riego"""
    def __init__(self, hilera, posicion):
        self.hilera = hilera
        self.posicion = posicion
    
    def obtener_identificador(self):
        """Obtener identificador de la instrucción"""
        return f"H{self.hilera}-P{self.posicion}"
    
    def __str__(self):
        return self.obtener_identificador()
