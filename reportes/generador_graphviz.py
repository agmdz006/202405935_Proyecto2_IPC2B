import os
import graphviz
from datetime import datetime
from tda.planta_regada import PlantaRegada
from tda.lista_enlazada import ListaEnlazada
from tda.instruccion_dron import InstruccionDron

class GeneradorGraphviz:
    """Clase para generar gráficos con Graphviz mostrando el estado de los TDAs"""
    
    def __init__(self):
        self.directorio_graficos = 'static/graphviz'
        os.makedirs(self.directorio_graficos, exist_ok=True)
    
    def generar_grafico_estado_tiempo(self, simulador, tiempo_especifico):
        """Generar gráfico mostrando SOLO las plantas regadas como lista enlazada simple"""
        if not simulador.esta_simulacion_completada():
            raise Exception("No hay simulación completada")
        
        # Crear grafo dirigido horizontal para lista enlazada
        dot = graphviz.Digraph(comment=f'Plantas Regadas - Tiempo {tiempo_especifico}s')
        dot.attr(rankdir='LR', size='12,8')
        dot.attr('node', shape='record', style='filled', fillcolor='lightgreen')
        
        # Configurar estilos simples
        dot.attr('graph', bgcolor='white', fontname='Arial', fontsize='12')
        dot.attr('node', fontname='Arial', fontsize='11')
        dot.attr('edge', fontname='Arial', fontsize='10', color='blue', penwidth='2')
        
        plantas_regadas = self._obtener_plantas_regadas_hasta_tiempo(simulador, tiempo_especifico)
        
        if plantas_regadas.obtener_tamaño() > 0:
            # Crear lista enlazada de plantas regadas
            contador = 0
            for planta_info in plantas_regadas.iterar():
                nodo_id = f"planta_{contador}"
                
                planta_texto = f"H{planta_info.obtener_hilera()}-P{planta_info.obtener_posicion()}"
                
                # Color diferente si tiene fertilizante
                color = 'lightcoral' if planta_info.obtener_fertilizante() > 0 else 'lightblue'
                
                dot.node(nodo_id, planta_texto, fillcolor=color, fontsize='12')
                
                # Conectar con el nodo anterior (lista enlazada)
                if contador > 0:
                    dot.edge(f"planta_{contador-1}", nodo_id, label='→')
                
                contador += 1
            
            # Nodo final NULL
            dot.node('null', 'NULL', shape='ellipse', fillcolor='lightgray', fontsize='10')
            if contador > 0:
                dot.edge(f"planta_{contador-1}", 'null', label='→')
        else:
            # Lista vacía
            dot.node('vacia', 'Lista Vacía\\nNo hay plantas regadas', 
                    shape='box', fillcolor='lightgray', fontsize='12')
        
        # Generar archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"plantas_regadas_t{tiempo_especifico}_{timestamp}"
        
        try:
            # Renderizar el gráfico
            ruta_archivo = dot.render(
                os.path.join(self.directorio_graficos, nombre_archivo),
                format='png',
                cleanup=True
            )
            return ruta_archivo
        except Exception as e:
            raise Exception(f"Error generando gráfico: {str(e)}")
    
    def _obtener_plantas_regadas_hasta_tiempo(self, simulador, tiempo_limite):
        """Obtener lista de plantas que han sido regadas hasta un tiempo específico"""
        plantas_regadas = ListaEnlazada()
        
        plantas_regadas_set = set()  # Para evitar duplicados
        
        posiciones_drones = {}  # {nombre_dron: posicion}
        
        # Inicializar posiciones de drones
        for dron in simulador.invernadero_actual.drones_asignados.iterar():
            posiciones_drones[dron.nombre] = 0
        
        # Revisar las instrucciones por tiempo hasta el límite especificado
        for instruccion_tiempo in simulador.obtener_instrucciones_por_tiempo().iterar():
            if instruccion_tiempo.tiempo > tiempo_limite:
                break
                
            # Procesar cada instrucción en este tiempo
            for instruccion in instruccion_tiempo.instrucciones_drones.iterar():
                dron_nombre = instruccion.obtener_dron_nombre()
                accion = instruccion.obtener_accion()
                
                if accion == "Regar":
                    # Obtener la posición actual del dron para el riego
                    dron = self._obtener_dron_por_nombre(simulador.invernadero_actual, dron_nombre)
                    if dron:
                        hilera = dron.hilera_asignada
                        posicion = posiciones_drones[dron_nombre]
                        planta_id = f"H{hilera}-P{posicion}"
                        
                        # Agregar solo si no está duplicada
                        if planta_id not in plantas_regadas_set:
                            fertilizante = 25 if self._requiere_fertilizante(hilera, posicion) else 0
                            
                            planta_info = PlantaRegada(
                                hilera,
                                posicion,
                                dron_nombre,
                                instruccion_tiempo.tiempo,
                                50,  # Agua estándar por planta
                                fertilizante
                            )
                            plantas_regadas.agregar(planta_info)
                            plantas_regadas_set.add(planta_id)
                
                elif accion.startswith("Adelante"):
                    # Actualizar posición del dron
                    posiciones_drones[dron_nombre] += 1
                elif accion.startswith("Atrás"):
                    # Actualizar posición del dron hacia atrás
                    if posiciones_drones[dron_nombre] > 0:
                        posiciones_drones[dron_nombre] -= 1
        
        return plantas_regadas
    
    def _encontrar_planta_regada_en_posicion(self, invernadero, hilera, posicion):
        """Encontrar una planta regada en una posición específica"""
        planta = invernadero.obtener_planta(hilera, posicion)
        if planta and planta.regada:
            return planta
        return None
    
    def _requiere_fertilizante(self, hilera, posicion):
        """Determinar si una planta requiere fertilizante (plantas en posiciones pares)"""
        return posicion % 2 == 0
    
    def _obtener_dron_por_nombre(self, invernadero, nombre_dron):
        """Obtener dron por nombre"""
        for dron in invernadero.drones_asignados.iterar():
            if dron.nombre == nombre_dron:
                return dron
        return None
    
    def _encontrar_tiempo_riego(self, simulador, hilera, posicion, tiempo_limite):
        """Encontrar el tiempo en que se regó una planta específica"""
        for instruccion_tiempo in simulador.obtener_instrucciones_por_tiempo().iterar():
            if instruccion_tiempo.tiempo > tiempo_limite:
                break
                
            for instruccion in instruccion_tiempo.instrucciones_drones.iterar():
                if instruccion.obtener_accion() == "Regar":
                    dron = self._obtener_dron_por_nombre(simulador.invernadero_actual, instruccion.obtener_dron_nombre())
                    if (dron and dron.hilera_asignada == hilera and 
                        dron.posicion_actual == posicion):
                        return instruccion_tiempo.tiempo
        return None










