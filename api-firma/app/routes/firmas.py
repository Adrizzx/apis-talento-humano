from flask import Blueprint, request, jsonify
from app.models import db
from app.models.firma import Firma
from app.models.empleado import Empleado
from app.models.turno import Turno
from app.models.receso import Receso
from app.schemas.firma_schema import firma_schema, firmas_schema
from datetime import datetime, date, time, timedelta
from sqlalchemy import and_, or_

firmas_bp = Blueprint('firmas', __name__)

# ========================================
# FUNCIONES AUXILIARES
# ========================================

def calcular_diferencia_tiempo(hora_esperada, hora_real):
    """
    Calcula la diferencia entre dos horas y retorna un objeto time
    """
    if not hora_esperada or not hora_real:
        return time(0, 0, 0)
    
    # Convertir a datetime para poder restar
    fecha_base = datetime(2000, 1, 1)
    dt_esperada = datetime.combine(fecha_base, hora_esperada)
    dt_real = datetime.combine(fecha_base, hora_real)
    
    diferencia = dt_real - dt_esperada
    
    # Si la diferencia es negativa, retornar 00:00:00
    if diferencia.total_seconds() < 0:
        return time(0, 0, 0)
    
    # Convertir segundos a horas, minutos, segundos
    segundos_totales = int(diferencia.total_seconds())
    horas = segundos_totales // 3600
    minutos = (segundos_totales % 3600) // 60
    segundos = segundos_totales % 60
    
    return time(horas, minutos, segundos)

def validar_datos_requeridos(data, campos_requeridos):
    """
    Valida que los campos requeridos estén presentes en el request
    """
    campos_faltantes = []
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or data[campo] == '':
            campos_faltantes.append(campo)
    
    if campos_faltantes:
        return False, f"Faltan campos requeridos: {', '.join(campos_faltantes)}"
    
    return True, None

def parsear_fecha(fecha_str):
    """
    Convierte string a objeto date con validación
    """
    try:
        return datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError('Formato de fecha inválido. Use YYYY-MM-DD')

def parsear_hora(hora_str):
    """
    Convierte string a objeto time con validación
    """
    try:
        return datetime.strptime(hora_str, '%H:%M:%S').time()
    except ValueError:
        raise ValueError('Formato de hora inválido. Use HH:MM:SS')

# ========================================
# GET - Obtener todas las firmas
# ========================================
@firmas_bp.route('/firmas', methods=['GET'])
def obtener_firmas():
    """
    Obtener todas las firmas registradas ordenadas por fecha descendente
    """
    try:
        firmas = Firma.query.order_by(Firma.fecha_firma.desc(), Firma.id_f.desc()).all()
        return jsonify({
            'success': True,
            'data': firmas_schema.dump(firmas),
            'total': len(firmas),
            'message': f'Se encontraron {len(firmas)} firmas'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener firmas: {str(e)}'
        }), 500

# ========================================
# GET - Obtener firma por ID
# ========================================
@firmas_bp.route('/firmas/<int:id_f>', methods=['GET'])
def obtener_firma(id_f):
    """
    Obtener una firma específica por ID
    """
    try:
        firma = Firma.query.get(id_f)
        if not firma:
            return jsonify({
                'success': False,
                'error': f'Firma con ID {id_f} no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': firma_schema.dump(firma),
            'message': 'Firma encontrada'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener firma: {str(e)}'
        }), 500

# ========================================
# GET - Obtener firma por CI y fecha
# ========================================
@firmas_bp.route('/firmas/empleado/<string:ci>/fecha/<string:fecha>', methods=['GET'])
def obtener_firma_por_ci_fecha(ci, fecha):
    """
    Obtener firma de un empleado en una fecha específica
    
    Parámetros:
    - ci: Cédula del empleado
    - fecha: Fecha en formato YYYY-MM-DD
    """
    try:
        # Validar empleado
        empleado = Empleado.query.get(ci)
        if not empleado:
            return jsonify({
                'success': False,
                'error': f'Empleado con CI {ci} no encontrado'
            }), 404
        
        # Convertir string a date
        fecha_obj = parsear_fecha(fecha)
        
        # Buscar firma
        firma = Firma.query.filter(
            and_(
                Firma.ci == ci,
                Firma.fecha_firma == fecha_obj
            )
        ).first()
        
        if not firma:
            return jsonify({
                'success': False,
                'error': f'No se encontró firma para el empleado {empleado.nombres} {empleado.apellidos} en la fecha {fecha}'
            }), 404
        
        return jsonify({
            'success': True,
            'data': firma_schema.dump(firma),
            'message': 'Firma encontrada'
        }), 200
        
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener firma: {str(e)}'
        }), 500

# ========================================
# GET - Obtener firmas de un empleado
# ========================================
@firmas_bp.route('/firmas/empleado/<string:ci>', methods=['GET'])
def obtener_firmas_empleado(ci):
    """
    Obtener todas las firmas de un empleado específico
    """
    try:
        # Validar empleado
        empleado = Empleado.query.get(ci)
        if not empleado:
            return jsonify({
                'success': False,
                'error': f'Empleado con CI {ci} no encontrado'
            }), 404
        
        # Obtener firmas
        firmas = Firma.query.filter_by(ci=ci).order_by(Firma.fecha_firma.desc()).all()
        
        return jsonify({
            'success': True,
            'data': firmas_schema.dump(firmas),
            'total': len(firmas),
            'empleado': {
                'ci': empleado.ci,
                'nombre_completo': f'{empleado.nombres} {empleado.apellidos}'
            },
            'message': f'Se encontraron {len(firmas)} firmas para {empleado.nombres} {empleado.apellidos}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener firmas del empleado: {str(e)}'
        }), 500

# ========================================
# GET - Obtener firmas por fecha
# ========================================
@firmas_bp.route('/firmas/fecha/<string:fecha>', methods=['GET'])
def obtener_firmas_por_fecha(fecha):
    """
    Obtener todas las firmas de una fecha específica
    
    Parámetros:
    - fecha: Fecha en formato YYYY-MM-DD
    """
    try:
        fecha_obj = parsear_fecha(fecha)
        firmas = Firma.query.filter_by(fecha_firma=fecha_obj).order_by(Firma.ci).all()
        
        return jsonify({
            'success': True,
            'data': firmas_schema.dump(firmas),
            'total': len(firmas),
            'fecha': fecha,
            'message': f'Se encontraron {len(firmas)} firmas para la fecha {fecha}'
        }), 200
        
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener firmas por fecha: {str(e)}'
        }), 500

# ========================================
# GET - Obtener firmas incompletas
# ========================================
@firmas_bp.route('/firmas/incompletas', methods=['GET'])
def obtener_firmas_incompletas():
    """
    Obtener firmas que no han completado la jornada (h_f_jornada es NULL)
    """
    try:
        firmas = Firma.query.filter(Firma.h_f_jornada == None).order_by(Firma.fecha_firma.desc()).all()
        
        return jsonify({
            'success': True,
            'data': firmas_schema.dump(firmas),
            'total': len(firmas),
            'message': f'Se encontraron {len(firmas)} firmas incompletas'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener firmas incompletas: {str(e)}'
        }), 500

# ========================================
# GET - Obtener firmas de hoy
# ========================================
@firmas_bp.route('/firmas/hoy', methods=['GET'])
def obtener_firmas_hoy():
    """
    Obtener todas las firmas del día actual
    """
    try:
        hoy = date.today()
        firmas = Firma.query.filter_by(fecha_firma=hoy).order_by(Firma.h_i_jornada).all()
        
        return jsonify({
            'success': True,
            'data': firmas_schema.dump(firmas),
            'total': len(firmas),
            'fecha': hoy.isoformat(),
            'message': f'Se encontraron {len(firmas)} firmas para hoy'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener firmas de hoy: {str(e)}'
        }), 500

# ========================================
# POST - Registrar inicio de jornada (INSERT)
# ========================================
@firmas_bp.route('/firmas/iniciar-jornada', methods=['POST'])
def iniciar_jornada():
    """
    Registrar inicio de jornada de un empleado (INSERT)
    
    Body JSON:
    {
        "ci": "1234567890",
        "fecha_firma": "2026-02-02",
        "h_i_jornada": "08:35:00",
        "a_i_jornada": "00:05:00"  (opcional)
    }
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        es_valido, mensaje_error = validar_datos_requeridos(data, ['ci', 'fecha_firma', 'h_i_jornada'])
        if not es_valido:
            return jsonify({
                'success': False,
                'error': mensaje_error
            }), 400
        
        # Validar empleado existe
        empleado = Empleado.query.get(data.get('ci'))
        if not empleado:
            return jsonify({
                'success': False,
                'error': f'Empleado con CI {data.get("ci")} no encontrado'
            }), 404
        
        # Validar que tenga turno asignado
        if not empleado.id_t:
            return jsonify({
                'success': False,
                'error': f'El empleado {empleado.nombres} {empleado.apellidos} no tiene un turno asignado'
            }), 400
        
        # Convertir fecha y hora
        fecha_obj = parsear_fecha(data.get('fecha_firma'))
        hora_inicio = parsear_hora(data.get('h_i_jornada'))
        
        # Verificar si ya existe firma para este empleado en esta fecha
        firma_existente = Firma.query.filter(
            and_(
                Firma.ci == data.get('ci'),
                Firma.fecha_firma == fecha_obj
            )
        ).first()
        
        if firma_existente:
            return jsonify({
                'success': False,
                'error': f'Ya existe un registro de firma para {empleado.nombres} {empleado.apellidos} en la fecha {fecha_obj.isoformat()}. ID: {firma_existente.id_f}'
            }), 400
        
        # Calcular atraso si se proporciona
        atraso = None
        if data.get('a_i_jornada'):
            atraso = parsear_hora(data.get('a_i_jornada'))
        else:
            # Calcular atraso automáticamente
            turno = Turno.query.get(empleado.id_t)
            if turno:
                atraso = calcular_diferencia_tiempo(turno.hora_inicio_t, hora_inicio)
        
        # Crear nueva firma
        nueva_firma = Firma(
            fecha_firma=fecha_obj,
            h_i_jornada=hora_inicio,
            a_i_jornada=atraso,
            ci=data.get('ci'),
            id_t=empleado.id_t,
            id_b=empleado.id_b if empleado.id_b else 0,
            id_ba=empleado.id_ba if empleado.id_ba else 0
        )
        
        db.session.add(nueva_firma)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Jornada iniciada correctamente para {empleado.nombres} {empleado.apellidos}',
            'data': firma_schema.dump(nueva_firma)
        }), 201
        
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al iniciar jornada: {str(e)}'
        }), 500

# ========================================
# PUT - Actualizar firma (UPDATE)
# ========================================
@firmas_bp.route('/firmas/<int:id_f>', methods=['PUT'])
def actualizar_firma(id_f):
    """
    Actualizar una firma existente (UPDATE)
    Usado para registrar eventos: salida/regreso break, salida/regreso almuerzo, fin jornada
    
    Body JSON:
    {
        "h_i_break": "10:30:00",
        "h_f_break": "10:45:00",
        "a_f_break": "00:02:00",
        "h_i_almuerzo": "13:00:00",
        "h_f_almuerzo": "14:00:00",
        "a_f_almuerzo": "00:05:00",
        "h_f_jornada": "17:30:00",
        "observacion": "Jornada completada"
    }
    """
    try:
        firma = Firma.query.get(id_f)
        if not firma:
            return jsonify({
                'success': False,
                'error': f'Firma con ID {id_f} no encontrada'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        campos_actualizados = []
        
        # Actualizar campos de tiempo si vienen en el request
        campos_hora = {
            'h_i_break': 'Hora inicio break',
            'h_f_break': 'Hora fin break',
            'a_f_break': 'Atraso fin break',
            'h_i_almuerzo': 'Hora inicio almuerzo',
            'h_f_almuerzo': 'Hora fin almuerzo',
            'a_f_almuerzo': 'Atraso fin almuerzo',
            'h_f_jornada': 'Hora fin jornada'
        }
        
        for campo, descripcion in campos_hora.items():
            if campo in data and data[campo]:
                try:
                    hora_obj = parsear_hora(data[campo])
                    setattr(firma, campo, hora_obj)
                    campos_actualizados.append(descripcion)
                except ValueError as ve:
                    return jsonify({
                        'success': False,
                        'error': f'Error en {descripcion}: {str(ve)}'
                    }), 400
        
        # Actualizar observación
        if 'observacion' in data:
            firma.observacion = data['observacion']
            campos_actualizados.append('Observación')
        
        if not campos_actualizados:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron campos válidos para actualizar'
            }), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Firma actualizada correctamente. Campos actualizados: {", ".join(campos_actualizados)}',
            'data': firma_schema.dump(firma)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al actualizar firma: {str(e)}'
        }), 500

# ========================================
# POST - Procesar firma (Lógica completa)
# ========================================
@firmas_bp.route('/firmas/procesar', methods=['POST'])
def procesar_firma():
    """
    Procesar firma automáticamente según verificación en cascada de NULL
    
    Body JSON:
    {
        "ci": "1234567890",
        "fecha_firma": "2026-02-02",  (opcional, por defecto usa fecha actual)
        "hora_actual": "10:30:00"      (opcional, por defecto usa hora actual)
    }
    
    Este endpoint implementa la lógica:
    1. Busca firma existente por CI y fecha
    2. Si no existe -> INSERT (inicio jornada)
    3. Si existe -> Verifica en cascada NULL y hace UPDATE
    """
    try:
        data = request.get_json()
        
        # Validar CI
        es_valido, mensaje_error = validar_datos_requeridos(data, ['ci'])
        if not es_valido:
            return jsonify({
                'success': False,
                'error': mensaje_error
            }), 400
        
        ci = data.get('ci')
        
        # Usar fecha actual si no se proporciona
        fecha_str = data.get('fecha_firma', date.today().isoformat())
        fecha_obj = parsear_fecha(fecha_str)
        
        # Usar hora actual si no se proporciona
        hora_str = data.get('hora_actual', datetime.now().strftime('%H:%M:%S'))
        hora_obj = parsear_hora(hora_str)
        
        # Validar empleado
        empleado = Empleado.query.get(ci)
        if not empleado:
            return jsonify({
                'success': False,
                'error': f'Empleado con CI {ci} no encontrado'
            }), 404
        
        # Validar que tenga turno asignado
        if not empleado.id_t:
            return jsonify({
                'success': False,
                'error': f'El empleado {empleado.nombres} {empleado.apellidos} no tiene un turno asignado'
            }), 400
        
        # Obtener turno
        turno = Turno.query.get(empleado.id_t)
        if not turno:
            return jsonify({
                'success': False,
                'error': f'El turno ID {empleado.id_t} no existe'
            }), 404
        
        # Buscar firma existente
        firma = Firma.query.filter(
            and_(
                Firma.ci == ci,
                Firma.fecha_firma == fecha_obj
            )
        ).first()
        
        # ===============================================
        # CASO 1: NO EXISTE FIRMA -> INICIO DE JORNADA
        # ===============================================
        if not firma:
            # Calcular atraso de inicio
            atraso_inicio = calcular_diferencia_tiempo(turno.hora_inicio_t, hora_obj)
            
            nueva_firma = Firma(
                fecha_firma=fecha_obj,
                h_i_jornada=hora_obj,
                a_i_jornada=atraso_inicio,
                ci=ci,
                id_t=empleado.id_t,
                id_b=empleado.id_b if empleado.id_b else 0,
                id_ba=empleado.id_ba if empleado.id_ba else 0
            )
            db.session.add(nueva_firma)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'✅ Inicio de jornada registrado para {empleado.nombres} {empleado.apellidos}',
                'evento': 'INICIO_JORNADA',
                'data': firma_schema.dump(nueva_firma),
                'detalles': {
                    'hora_registro': hora_obj.isoformat(),
                    'hora_esperada': turno.hora_inicio_t.isoformat(),
                    'atraso': atraso_inicio.isoformat()
                }
            }), 201
        
        # ===============================================
        # CASO 2: EXISTE FIRMA -> VERIFICACIÓN CASCADA
        # ===============================================
        
        evento = None
        detalles = {}
        
        # Caso 2.1: Salida a break
        if firma.h_i_break is None:
            firma.h_i_break = hora_obj
            evento = 'SALIDA_BREAK'
            detalles = {
                'hora_salida_break': hora_obj.isoformat(),
                'descripcion': 'Salida a break registrada'
            }
        
        # Caso 2.2: Regreso de break
        elif firma.h_f_break is None:
            firma.h_f_break = hora_obj
            
            # Obtener datos del break
            if empleado.id_b:
                receso_break = Receso.query.get(empleado.id_b)
                if receso_break:
                    # Calcular hora esperada de regreso
                    fecha_base = datetime(2000, 1, 1)
                    dt_inicio_break = datetime.combine(fecha_base, firma.h_i_break)
                    dt_duracion_break = datetime.combine(fecha_base, receso_break.tiempo_receso_b)
                    duracion_segundos = (dt_duracion_break - fecha_base).total_seconds()
                    dt_esperado = dt_inicio_break + timedelta(seconds=duracion_segundos)
                    hora_esperada_regreso = dt_esperado.time()
                    
                    # Calcular atraso
                    atraso_break = calcular_diferencia_tiempo(hora_esperada_regreso, hora_obj)
                    firma.a_f_break = atraso_break
                    
                    detalles = {
                        'hora_regreso_break': hora_obj.isoformat(),
                        'hora_esperada_regreso': hora_esperada_regreso.isoformat(),
                        'atraso': atraso_break.isoformat()
                    }
                else:
                    firma.a_f_break = time(0, 0, 0)
                    detalles = {
                        'hora_regreso_break': hora_obj.isoformat(),
                        'nota': 'No se pudo calcular atraso (receso no encontrado)'
                    }
            else:
                firma.a_f_break = time(0, 0, 0)
                detalles = {
                    'hora_regreso_break': hora_obj.isoformat(),
                    'nota': 'Empleado sin break asignado'
                }
            
            evento = 'REGRESO_BREAK'
        
        # Caso 2.3: Salida a almuerzo
        elif firma.h_i_almuerzo is None:
            firma.h_i_almuerzo = hora_obj
            evento = 'SALIDA_ALMUERZO'
            detalles = {
                'hora_salida_almuerzo': hora_obj.isoformat(),
                'descripcion': 'Salida a almuerzo registrada'
            }
        
        # Caso 2.4: Regreso de almuerzo
        elif firma.h_f_almuerzo is None:
            firma.h_f_almuerzo = hora_obj
            
            # Obtener datos del almuerzo
            if empleado.id_ba:
                receso_almuerzo = Receso.query.get(empleado.id_ba)
                if receso_almuerzo:
                    # Calcular hora esperada de regreso
                    fecha_base = datetime(2000, 1, 1)
                    dt_inicio_almuerzo = datetime.combine(fecha_base, firma.h_i_almuerzo)
                    dt_duracion_almuerzo = datetime.combine(fecha_base, receso_almuerzo.tiempo_receso_b)
                    duracion_segundos = (dt_duracion_almuerzo - fecha_base).total_seconds()
                    dt_esperado = dt_inicio_almuerzo + timedelta(seconds=duracion_segundos)
                    hora_esperada_regreso = dt_esperado.time()
                    
                    # Calcular atraso
                    atraso_almuerzo = calcular_diferencia_tiempo(hora_esperada_regreso, hora_obj)
                    firma.a_f_almuerzo = atraso_almuerzo
                    
                    detalles = {
                        'hora_regreso_almuerzo': hora_obj.isoformat(),
                        'hora_esperada_regreso': hora_esperada_regreso.isoformat(),
                        'atraso': atraso_almuerzo.isoformat()
                    }
                else:
                    firma.a_f_almuerzo = time(0, 0, 0)
                    detalles = {
                        'hora_regreso_almuerzo': hora_obj.isoformat(),
                        'nota': 'No se pudo calcular atraso (receso no encontrado)'
                    }
            else:
                firma.a_f_almuerzo = time(0, 0, 0)
                detalles = {
                    'hora_regreso_almuerzo': hora_obj.isoformat(),
                    'nota': 'Empleado sin almuerzo asignado'
                }
            
            evento = 'REGRESO_ALMUERZO'
        
        # Caso 2.5: Fin de jornada
        elif firma.h_f_jornada is None:
            firma.h_f_jornada = hora_obj
            evento = 'FIN_JORNADA'
            detalles = {
                'hora_fin_jornada': hora_obj.isoformat(),
                'hora_esperada_fin': turno.hora_fin_t.isoformat(),
                'descripcion': 'Jornada completada'
            }
        
        # Caso 2.6: Jornada ya completada
        else:
            return jsonify({
                'success': False,
                'error': f'La jornada de {empleado.nombres} {empleado.apellidos} para la fecha {fecha_obj.isoformat()} ya ha sido completada',
                'data': firma_schema.dump(firma)
            }), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'✅ {evento.replace("_", " ").title()} registrado para {empleado.nombres} {empleado.apellidos}',
            'evento': evento,
            'data': firma_schema.dump(firma),
            'detalles': detalles
        }), 200
        
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al procesar firma: {str(e)}'
        }), 500

# ========================================
# PUT - Autocompletar firmas incompletas
# ========================================
@firmas_bp.route('/firmas/autocompletar', methods=['PUT'])
def autocompletar_firmas():
    """
    Autocompletar firmas incompletas de fechas anteriores
    con hora de fin de turno y observaciones
    """
    try:
        # Obtener fecha actual
        hoy = date.today()
        
        # Buscar firmas incompletas (h_f_jornada es NULL y fecha != hoy)
        firmas_incompletas = Firma.query.filter(
            and_(
                Firma.h_f_jornada == None,
                Firma.fecha_firma < hoy
            )
        ).all()
        
        if not firmas_incompletas:
            return jsonify({
                'success': True,
                'message': 'No hay firmas incompletas para autocompletar',
                'total': 0
            }), 200
        
        completadas = []
        
        for firma in firmas_incompletas:
            # Obtener hora de fin de turno
            turno = Turno.query.get(firma.id_t)
            hora_fin_turno = turno.hora_fin_t if turno else time(18, 0, 0)
            
            # Determinar qué campo está NULL y establecer observación
            if firma.h_i_break is None:
                observacion = "NO FIRMASTE DESDE EL INICIO DE TU BREAK EN ADELANTE. AUTO COMPLETADO"
                firma.h_i_break = time(0, 0, 0)
                firma.h_f_break = time(0, 0, 0)
                firma.a_f_break = time(0, 0, 0)
                firma.h_i_almuerzo = time(0, 0, 0)
                firma.h_f_almuerzo = time(0, 0, 0)
                firma.a_f_almuerzo = time(0, 0, 0)
            elif firma.h_f_break is None:
                observacion = "NO FIRMASTE DESDE EL FIN DE TU BREAK EN ADELANTE. AUTO COMPLETADO"
                firma.h_f_break = time(0, 0, 0)
                firma.a_f_break = time(0, 0, 0)
                firma.h_i_almuerzo = time(0, 0, 0)
                firma.h_f_almuerzo = time(0, 0, 0)
                firma.a_f_almuerzo = time(0, 0, 0)
            elif firma.h_i_almuerzo is None:
                observacion = "NO FIRMASTE DESDE EL INICIO DE TU ALMUERZO EN ADELANTE. AUTO COMPLETADO"
                firma.h_i_almuerzo = time(0, 0, 0)
                firma.h_f_almuerzo = time(0, 0, 0)
                firma.a_f_almuerzo = time(0, 0, 0)
            elif firma.h_f_almuerzo is None:
                observacion = "NO FIRMASTE DESDE EL FIN DE TU ALMUERZO EN ADELANTE. AUTO COMPLETADO"
                firma.h_f_almuerzo = time(0, 0, 0)
                firma.a_f_almuerzo = time(0, 0, 0)
            else:
                observacion = "NO FIRMASTE LA SALIDA DE TU JORNADA. AUTO COMPLETADO"
            
            firma.h_f_jornada = hora_fin_turno
            firma.observacion = observacion
            
            completadas.append({
                'id_f': firma.id_f,
                'ci': firma.ci,
                'fecha': firma.fecha_firma.isoformat(),
                'observacion': observacion
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'✅ {len(completadas)} firmas autocompletadas correctamente',
            'total': len(completadas),
            'firmas_completadas': completadas
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al autocompletar firmas: {str(e)}'
        }), 500

# ========================================
# DELETE - Eliminar firma
# ========================================
@firmas_bp.route('/firmas/<int:id_f>', methods=['DELETE'])
def eliminar_firma(id_f):
    """
    Eliminar una firma específica
    """
    try:
        firma = Firma.query.get(id_f)
        if not firma:
            return jsonify({
                'success': False,
                'error': f'Firma con ID {id_f} no encontrada'
            }), 404
        
        # Guardar datos para el mensaje
        ci = firma.ci
        fecha = firma.fecha_firma.isoformat() if firma.fecha_firma else 'N/A'
        
        db.session.delete(firma)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'✅ Firma ID {id_f} eliminada correctamente (CI: {ci}, Fecha: {fecha})'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al eliminar firma: {str(e)}'
        }), 500

# ========================================
# GET - Health Check
# ========================================
@firmas_bp.route('/health', methods=['GET'])
def health_check():
    """
    Verificar el estado de la API
    """
    try:
        # Verificar conexión a base de datos
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        
        return jsonify({
            'success': True,
            'message': 'API de Firmas funcionando correctamente',
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error en la API',
            'status': 'unhealthy',
            'error': str(e)
        }), 500
