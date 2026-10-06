from flask import Blueprint, request, jsonify
from app.models import Personal
from datetime import datetime

personal_bp = Blueprint('personal', __name__)

# GET - Obtener todos los empleados
@personal_bp.route('/personal', methods=['GET'])
def obtener_empleados():
    try:
        empleados = Personal.get_all()
        empleados_list = [dict(emp) for emp in empleados]
        
        # Convertir fechas a string
        for emp in empleados_list:
            if emp.get('fecha_nacimiento'):
                emp['fecha_nacimiento'] = emp['fecha_nacimiento'].strftime('%Y-%m-%d')
            if emp.get('fecha_ingreso'):
                emp['fecha_ingreso'] = emp['fecha_ingreso'].strftime('%Y-%m-%d')
            if emp.get('fecha_contrato'):
                emp['fecha_contrato'] = emp['fecha_contrato'].strftime('%Y-%m-%d')
            if emp.get('salario'):
                emp['salario'] = float(emp['salario'])
        
        return jsonify({
            'success': True,
            'data': empleados_list,
            'total': len(empleados_list)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# GET - Obtener empleado por CI
@personal_bp.route('/personal/<string:ci>', methods=['GET'])
def obtener_empleado(ci):
    try:
        empleado = Personal.get_by_ci(ci)
        if empleado:
            empleado_dict = dict(empleado)
            
            # Convertir fechas a string
            if empleado_dict.get('fecha_nacimiento'):
                empleado_dict['fecha_nacimiento'] = empleado_dict['fecha_nacimiento'].strftime('%Y-%m-%d')
            if empleado_dict.get('fecha_ingreso'):
                empleado_dict['fecha_ingreso'] = empleado_dict['fecha_ingreso'].strftime('%Y-%m-%d')
            if empleado_dict.get('fecha_contrato'):
                empleado_dict['fecha_contrato'] = empleado_dict['fecha_contrato'].strftime('%Y-%m-%d')
            if empleado_dict.get('salario'):
                empleado_dict['salario'] = float(empleado_dict['salario'])
            
            return jsonify({
                'success': True,
                'data': empleado_dict
            }), 200
        return jsonify({
            'success': False,
            'error': 'Empleado no encontrado'
        }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# GET - Buscar empleados por nombre o apellido
@personal_bp.route('/personal/search', methods=['GET'])
def buscar_empleados():
    try:
        nombres = request.args.get('nombres', '')
        apellidos = request.args.get('apellidos', '')
        
        if not nombres and not apellidos:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar al menos un criterio de búsqueda (nombres o apellidos)'
            }), 400
        
        empleados = Personal.search_by_name(nombres, apellidos)
        empleados_list = [dict(emp) for emp in empleados]
        
        # Convertir fechas a string
        for emp in empleados_list:
            if emp.get('fecha_nacimiento'):
                emp['fecha_nacimiento'] = emp['fecha_nacimiento'].strftime('%Y-%m-%d')
            if emp.get('fecha_ingreso'):
                emp['fecha_ingreso'] = emp['fecha_ingreso'].strftime('%Y-%m-%d')
            if emp.get('fecha_contrato'):
                emp['fecha_contrato'] = emp['fecha_contrato'].strftime('%Y-%m-%d')
            if emp.get('salario'):
                emp['salario'] = float(emp['salario'])
        
        return jsonify({
            'success': True,
            'data': empleados_list,
            'total': len(empleados_list)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# POST - Crear nuevo empleado
@personal_bp.route('/personal', methods=['POST'])
def crear_empleado():
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        campos_requeridos = [
            'ci', 'id_a', 'id_t', 'nombres', 'apellidos',
            'direccion', 'telefonos', 'correo', 'fecha_nacimiento',
            'fecha_ingreso', 'fecha_contrato', 'salario'
        ]
        
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Verificar si ya existe
        empleado_existente = Personal.get_by_ci(data['ci'])
        if empleado_existente:
            return jsonify({
                'success': False,
                'error': 'Ya existe un empleado con esa cédula'
            }), 400
        
        # Establecer valores por defecto para campos opcionales
        if 'id_b' not in data:
            data['id_b'] = None
        if 'id_ba' not in data:
            data['id_ba'] = None
        
        # Crear empleado
        new_ci = Personal.create(data)
        
        # Obtener el empleado creado
        nuevo_empleado = Personal.get_by_ci(new_ci)
        empleado_dict = dict(nuevo_empleado)
        
        # Convertir fechas a string
        if empleado_dict.get('fecha_nacimiento'):
            empleado_dict['fecha_nacimiento'] = empleado_dict['fecha_nacimiento'].strftime('%Y-%m-%d')
        if empleado_dict.get('fecha_ingreso'):
            empleado_dict['fecha_ingreso'] = empleado_dict['fecha_ingreso'].strftime('%Y-%m-%d')
        if empleado_dict.get('fecha_contrato'):
            empleado_dict['fecha_contrato'] = empleado_dict['fecha_contrato'].strftime('%Y-%m-%d')
        if empleado_dict.get('salario'):
            empleado_dict['salario'] = float(empleado_dict['salario'])
        
        return jsonify({
            'success': True,
            'message': 'Empleado creado exitosamente',
            'data': empleado_dict
        }), 201
        
    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f'Campo requerido faltante: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# PUT - Actualizar empleado existente
@personal_bp.route('/personal/<string:ci>', methods=['PUT'])
def actualizar_empleado(ci):
    try:
        # Verificar si existe
        empleado = Personal.get_by_ci(ci)
        if not empleado:
            return jsonify({
                'success': False,
                'error': 'Empleado no encontrado'
            }), 404
        
        data = request.get_json()
        
        # Validar campos requeridos
        campos_requeridos = [
            'id_a', 'id_t', 'nombres', 'apellidos',
            'direccion', 'telefonos', 'correo', 'fecha_nacimiento',
            'fecha_ingreso', 'fecha_contrato', 'salario'
        ]
        
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Establecer valores por defecto para campos opcionales
        if 'id_b' not in data:
            data['id_b'] = None
        if 'id_ba' not in data:
            data['id_ba'] = None
        
        # Actualizar empleado
        actualizado = Personal.update(ci, data)
        
        if actualizado:
            # Obtener el empleado actualizado
            empleado_actualizado = Personal.get_by_ci(ci)
            empleado_dict = dict(empleado_actualizado)
            
            # Convertir fechas a string
            if empleado_dict.get('fecha_nacimiento'):
                empleado_dict['fecha_nacimiento'] = empleado_dict['fecha_nacimiento'].strftime('%Y-%m-%d')
            if empleado_dict.get('fecha_ingreso'):
                empleado_dict['fecha_ingreso'] = empleado_dict['fecha_ingreso'].strftime('%Y-%m-%d')
            if empleado_dict.get('fecha_contrato'):
                empleado_dict['fecha_contrato'] = empleado_dict['fecha_contrato'].strftime('%Y-%m-%d')
            if empleado_dict.get('salario'):
                empleado_dict['salario'] = float(empleado_dict['salario'])
            
            return jsonify({
                'success': True,
                'message': 'Empleado actualizado exitosamente',
                'data': empleado_dict
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el empleado'
            }), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# DELETE - Eliminar empleado
@personal_bp.route('/personal/<string:ci>', methods=['DELETE'])
def eliminar_empleado(ci):
    try:
        # Verificar si existe
        empleado = Personal.get_by_ci(ci)
        if not empleado:
            return jsonify({
                'success': False,
                'error': 'Empleado no encontrado'
            }), 404
        
        # Eliminar empleado
        eliminado = Personal.delete(ci)
        
        if eliminado:
            return jsonify({
                'success': True,
                'message': 'Empleado eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el empleado'
            }), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
