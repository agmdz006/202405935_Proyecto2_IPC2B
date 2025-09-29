from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from xml_reader.reader_xml import ReaderXML
from simulacion.simulador_riego import SimuladorRiego
from reportes.generador_reportes import GeneradorReportes
from reportes.generador_graphviz import GeneradorGraphviz

app = Flask(__name__)
app.secret_key = 'sistema_riego_ipc2_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Crear directorio de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('reportes/html', exist_ok=True)
os.makedirs('reportes/graphviz', exist_ok=True)
os.makedirs('salida', exist_ok=True)

# Instancias globales
reader_xml = ReaderXML()
simulador = SimuladorRiego()
generador_reportes = GeneradorReportes()
generador_graphviz = GeneradorGraphviz()

@app.route('/')
def index():
    """Página principal del sistema"""
    estadisticas = reader_xml.obtener_estadisticas() if reader_xml.esta_cargado() else None
    return render_template('index.html', estadisticas=estadisticas)

@app.route('/cargar_archivo', methods=['GET', 'POST'])
def cargar_archivo():
    """Cargar archivo XML de configuración"""
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        if archivo and archivo.filename.lower().endswith('.xml'):
            filename = secure_filename(archivo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            archivo.save(filepath)
            
            # Cargar y procesar el archivo XML
            exito, mensaje = reader_xml.cargar_archivo(filepath)
            
            if exito:
                flash(f'Archivo cargado exitosamente: {mensaje}', 'success')
                return redirect(url_for('index'))
            else:
                flash(f'Error al cargar archivo: {mensaje}', 'error')
        else:
            flash('Solo se permiten archivos XML', 'error')
    
    return render_template('cargar_archivo.html')

@app.route('/ver_invernaderos')
def ver_invernaderos():
    """Listar todos los invernaderos cargados"""
    if not reader_xml.esta_cargado():
        flash('Primero debe cargar un archivo de configuración', 'warning')
        return redirect(url_for('cargar_archivo'))
    
    invernaderos = reader_xml.obtener_invernaderos()
    return render_template('invernaderos.html', invernaderos=invernaderos)

@app.route('/invernaderos')
def listar_invernaderos():
    """Alias para ver_invernaderos"""
    return ver_invernaderos()

@app.route('/invernadero/<nombre>')
def detalle_invernadero(nombre):
    """Mostrar detalles de un invernadero específico"""
    invernadero = reader_xml.obtener_invernadero_por_nombre(nombre)
    if not invernadero:
        flash('Invernadero no encontrado', 'error')
        return redirect(url_for('listar_invernaderos'))
    
    return render_template('detalle_invernadero.html', invernadero=invernadero)

@app.route('/simular', methods=['GET', 'POST'])
def simular_riego():
    """Simular proceso de riego"""
    if not reader_xml.esta_cargado():
        flash('Primero debe cargar un archivo de configuración', 'warning')
        return redirect(url_for('cargar_archivo'))
    
    invernadero_seleccionado = None
    planes_disponibles = None
    
    if request.method == 'POST':
        nombre_invernadero = request.form.get('invernadero')
        nombre_plan = request.form.get('plan')
        
        # Si solo se seleccionó invernadero, cargar sus planes
        if nombre_invernadero and not nombre_plan:
            invernadero_seleccionado = nombre_invernadero
            invernadero = reader_xml.obtener_invernadero_por_nombre(nombre_invernadero)
            if invernadero:
                planes_disponibles = invernadero.planes_riego
        
        # Si se seleccionaron ambos, ejecutar simulación
        elif nombre_invernadero and nombre_plan:
            invernadero = reader_xml.obtener_invernadero_por_nombre(nombre_invernadero)
            if not invernadero:
                flash('Invernadero no encontrado', 'error')
                return redirect(request.url)
            
            plan = invernadero.obtener_plan_por_nombre(nombre_plan)
            if not plan:
                flash('Plan de riego no encontrado', 'error')
                return redirect(request.url)
            
            # Configurar y ejecutar simulación
            simulador.configurar_simulacion(invernadero, plan)
            exito, mensaje = simulador.ejecutar_simulacion()
            
            if exito:
                estadisticas = simulador.obtener_estadisticas()
                instrucciones = simulador.obtener_instrucciones_por_tiempo()
                
                return render_template('resultado_simulacion.html', 
                                     invernadero=invernadero,
                                     plan=plan,
                                     estadisticas=estadisticas,
                                     instrucciones=instrucciones)
            else:
                flash(f'Error en la simulación: {mensaje}', 'error')
    
    invernaderos = reader_xml.obtener_invernaderos()
    return render_template('simular.html', 
                         invernaderos=invernaderos,
                         invernadero_seleccionado=invernadero_seleccionado,
                         planes_disponibles=planes_disponibles)

@app.route('/api/planes/<nombre_invernadero>')
def obtener_planes_api(nombre_invernadero):
    """API para obtener planes de riego de un invernadero"""
    invernadero = reader_xml.obtener_invernadero_por_nombre(nombre_invernadero)
    if not invernadero:
        return jsonify({'error': 'Invernadero no encontrado'}), 404
    
    planes = []
    for plan in invernadero.planes_riego.iterar():
        planes.append({
            'nombre': plan.nombre,
            'secuencia': plan.secuencia_riego
        })
    
    return jsonify({'planes': planes})

@app.route('/generar_reporte_html/<nombre_invernadero>/<nombre_plan>')
def generar_reporte_html(nombre_invernadero, nombre_plan):
    """Generar reporte HTML para un invernadero y plan específicos"""
    if not simulador.esta_simulacion_completada():
        flash('Primero debe ejecutar una simulación', 'warning')
        return redirect(url_for('simular_riego'))
    
    try:
        estadisticas = simulador.obtener_estadisticas()
        instrucciones = simulador.obtener_instrucciones_por_tiempo()
        
        if estadisticas is None:
            flash('No hay estadísticas disponibles de la simulación', 'error')
            return redirect(url_for('simular_riego'))
        
        if instrucciones is None:
            flash('No hay instrucciones disponibles de la simulación', 'error')
            return redirect(url_for('simular_riego'))
            
        archivo_reporte = generador_reportes.generar_reporte_invernadero(
            simulador.invernadero_actual,
            simulador.plan_actual,
            estadisticas,
            instrucciones
        )
        
        return send_file(archivo_reporte, as_attachment=True)
    except Exception as e:
        flash(f'Error generando reporte: {str(e)}', 'error')
        return redirect(url_for('simular_riego'))

@app.route('/generar_grafico_tda', methods=['POST'])
def generar_grafico_tda():
    """Generar gráfico de estado de TDAs en tiempo específico"""
    if not simulador.esta_simulacion_completada():
        return jsonify({'error': 'No hay simulación completada'}), 400
    
    tiempo = int(request.form.get('tiempo', 1))
    
    try:
        archivo_grafico = generador_graphviz.generar_grafico_estado_tiempo(
            simulador, tiempo
        )
        
        # Obtener solo el nombre del archivo para la URL
        nombre_archivo = os.path.basename(archivo_grafico)
        
        return jsonify({
            'success': True,
            'archivo': archivo_grafico,
            'url': url_for('static', filename=f'graphviz/{nombre_archivo}')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generar_salida_xml')
def generar_salida_xml():
    """Generar archivo de salida XML con todos los resultados"""
    if not reader_xml.esta_cargado():
        flash('Primero debe cargar un archivo de configuración', 'warning')
        return redirect(url_for('cargar_archivo'))
    
    try:
        archivo_salida = generador_reportes.generar_archivo_salida_completo(
            reader_xml.obtener_invernaderos()
        )
        
        return send_file(archivo_salida, as_attachment=True)
    except Exception as e:
        flash(f'Error generando archivo de salida: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/ayuda')
def ayuda():
    """Página de ayuda y documentación"""
    return render_template('ayuda.html')

@app.route('/acerca')
def acerca():
    """Página acerca de la aplicación"""
    return render_template('acerca.html')

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Configuración para desarrollo
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    app.run(
        debug=debug_mode,
        host=host,
        port=port,
        threaded=True
    )

