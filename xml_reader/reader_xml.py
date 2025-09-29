import xml.etree.ElementTree as ET
from tda.lista_enlazada import ListaEnlazada
from modelos.planta import Planta
from modelos.dron import Dron
from modelos.invernadero import Invernadero
from modelos.plan_riego import PlanRiego

class ReaderXML:
    """Clase encargada de leer y parsear archivos XML de configuración"""
    
    def __init__(self):
        self.drones_disponibles = ListaEnlazada()
        self.invernaderos = ListaEnlazada()
        self.archivo_cargado = False
    
    def cargar_archivo(self, ruta_archivo):
        """Cargar y procesar archivo XML de configuración"""
        try:
            # Parsear el archivo XML
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            # Limpiar configuraciones previas
            self.drones_disponibles = ListaEnlazada()
            self.invernaderos = ListaEnlazada()
            
            # Procesar drones disponibles
            self._procesar_drones(root)
            
            # Procesar invernaderos
            self._procesar_invernaderos(root)
            
            self.archivo_cargado = True
            return True, "Archivo XML cargado exitosamente"
            
        except ET.ParseError as e:
            return False, f"Error al parsear XML: {str(e)}"
        except FileNotFoundError:
            return False, "Archivo no encontrado"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def _procesar_drones(self, root):
        """Procesar la lista de drones del XML"""
        lista_drones = root.find('listaDrones')
        if lista_drones is not None:
            for dron_element in lista_drones.findall('dron'):
                try:
                    id_dron = int(dron_element.get('id'))
                    nombre = dron_element.get('nombre', f'DR{id_dron:02d}')
                    
                    dron = Dron(id_dron, nombre)
                    self.drones_disponibles.agregar(dron)
                    
                except (ValueError, TypeError) as e:
                    print(f"Error procesando dron: {e}")
                    continue
    
    def _procesar_invernaderos(self, root):
        """Procesar la lista de invernaderos del XML"""
        lista_invernaderos = root.find('listaInvernaderos')
        if lista_invernaderos is not None:
            for invernadero_element in lista_invernaderos.findall('invernadero'):
                try:
                    nombre = invernadero_element.get('nombre', 'Invernadero Sin Nombre')
                    invernadero = Invernadero(nombre)
                    
                    # Procesar dimensiones
                    self._procesar_dimensiones(invernadero_element, invernadero)
                    
                    # Procesar plantas
                    self._procesar_plantas(invernadero_element, invernadero)
                    
                    # Procesar asignación de drones
                    self._procesar_asignacion_drones(invernadero_element, invernadero)
                    
                    # Procesar planes de riego
                    self._procesar_planes_riego(invernadero_element, invernadero)
                    
                    self.invernaderos.agregar(invernadero)
                    
                except Exception as e:
                    print(f"Error procesando invernadero {nombre}: {e}")
                    continue
    
    def _procesar_dimensiones(self, invernadero_element, invernadero):
        """Procesar dimensiones del invernadero"""
        numero_hileras_elem = invernadero_element.find('numeroHileras')
        plantas_hilera_elem = invernadero_element.find('plantasXhilera')
        
        if numero_hileras_elem is not None and plantas_hilera_elem is not None:
            try:
                numero_hileras = int(numero_hileras_elem.text.strip())
                plantas_por_hilera = int(plantas_hilera_elem.text.strip())
                invernadero.configurar_dimensiones(numero_hileras, plantas_por_hilera)
            except (ValueError, AttributeError):
                print("Error procesando dimensiones del invernadero")
    
    def _procesar_plantas(self, invernadero_element, invernadero):
        """Procesar lista de plantas del invernadero"""
        lista_plantas = invernadero_element.find('listaPlantas')
        if lista_plantas is not None:
            for planta_element in lista_plantas.findall('planta'):
                try:
                    hilera = int(planta_element.get('hilera'))
                    posicion = int(planta_element.get('posicion'))
                    litros_agua = float(planta_element.get('litrosAgua', 0))
                    gramos_fertilizante = float(planta_element.get('gramosFertilizante', 0))
                    tipo_planta = planta_element.text.strip() if planta_element.text else ""
                    
                    planta = Planta(hilera, posicion, litros_agua, gramos_fertilizante, tipo_planta)
                    invernadero.agregar_planta(planta)
                    
                except (ValueError, TypeError, AttributeError) as e:
                    print(f"Error procesando planta: {e}")
                    continue
    
    def _procesar_asignacion_drones(self, invernadero_element, invernadero):
        """Procesar asignación de drones a hileras"""
        asignacion_drones = invernadero_element.find('asignacionDrones')
        if asignacion_drones is not None:
            for dron_element in asignacion_drones.findall('dron'):
                try:
                    id_dron = int(dron_element.get('id'))
                    hilera = int(dron_element.get('hilera'))
                    
                    # Buscar el dron en la lista de drones disponibles
                    dron_encontrado = None
                    for dron in self.drones_disponibles.iterar():
                        if dron.id == id_dron:
                            dron_encontrado = dron
                            break
                    
                    if dron_encontrado:
                        # Crear una copia del dron para este invernadero
                        dron_copia = Dron(dron_encontrado.id, dron_encontrado.nombre)
                        invernadero.asignar_dron(dron_copia, hilera)
                    
                except (ValueError, TypeError) as e:
                    print(f"Error procesando asignación de dron: {e}")
                    continue
    
    def _procesar_planes_riego(self, invernadero_element, invernadero):
        """Procesar planes de riego del invernadero"""
        planes_riego = invernadero_element.find('planesRiego')
        if planes_riego is not None:
            for plan_element in planes_riego.findall('plan'):
                try:
                    nombre_plan = plan_element.get('nombre', 'Plan Sin Nombre')
                    secuencia = plan_element.text.strip() if plan_element.text else ""
                    
                    plan = PlanRiego(nombre_plan, secuencia)
                    invernadero.agregar_plan_riego(plan)
                    
                except AttributeError as e:
                    print(f"Error procesando plan de riego: {e}")
                    continue
    
    def obtener_drones(self):
        """Obtener lista de drones disponibles"""
        return self.drones_disponibles
    
    def obtener_invernaderos(self):
        """Obtener lista de invernaderos cargados"""
        return self.invernaderos
    
    def obtener_invernadero_por_nombre(self, nombre):
        """Obtener invernadero específico por nombre"""
        for invernadero in self.invernaderos.iterar():
            if invernadero.nombre == nombre:
                return invernadero
        return None
    
    def esta_cargado(self):
        """Verificar si hay un archivo cargado"""
        return self.archivo_cargado
    
    def obtener_estadisticas(self):
        """Obtener estadísticas de la configuración cargada"""
        if not self.archivo_cargado:
            return None
        
        total_drones = self.drones_disponibles.obtener_tamaño()
        total_invernaderos = self.invernaderos.obtener_tamaño()
        total_plantas = 0
        total_planes = 0
        
        for invernadero in self.invernaderos.iterar():
            total_plantas += invernadero.plantas.obtener_tamaño()
            total_planes += invernadero.planes_riego.obtener_tamaño()
        
        return {
            'drones': total_drones,
            'invernaderos': total_invernaderos,
            'plantas': total_plantas,
            'planes': total_planes
        }
