from app.database import get_db_connection, close_db_connection

class Personal:
    """Modelo para gestionar empleados/personal"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los empleados ordenados por apellido"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT ci, id_a, id_t, id_b, id_ba, 
                       nombres, apellidos, direccion, telefonos, 
                       correo, fecha_nacimiento, fecha_ingreso, 
                       fecha_contrato, salario 
                FROM empleado 
                ORDER BY apellidos
            """)
            empleados = cursor.fetchall()
            return empleados
        finally:
            cursor.close()
            close_db_connection(conn)
    
    @staticmethod
    def get_by_ci(ci):
        """Obtiene un empleado por su CI"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT ci, id_a, id_t, id_b, id_ba, 
                       nombres, apellidos, direccion, telefonos, 
                       correo, fecha_nacimiento, fecha_ingreso, 
                       fecha_contrato, salario 
                FROM empleado 
                WHERE ci = %s
            """, (ci,))
            empleado = cursor.fetchone()
            return empleado
        finally:
            cursor.close()
            close_db_connection(conn)
    
    @staticmethod
    def search_by_name(nombres=None, apellidos=None):
        """Busca empleados por nombre o apellido"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Construir query dinámicamente según los parámetros proporcionados
            conditions = []
            params = []
            
            if nombres:
                conditions.append("nombres ILIKE %s")
                params.append(f'%{nombres}%')
            
            if apellidos:
                conditions.append("apellidos ILIKE %s")
                params.append(f'%{apellidos}%')
            
            # Unir condiciones con OR (si no hay condiciones, no devolver nada)
            where_clause = " OR ".join(conditions) if conditions else "1=0"
            
            query = f"""
                SELECT ci, id_a, id_t, id_b, id_ba, 
                       nombres, apellidos, direccion, telefonos, 
                       correo, fecha_nacimiento, fecha_ingreso, 
                       fecha_contrato, salario 
                FROM empleado 
                WHERE {where_clause}
                ORDER BY apellidos
            """
            cursor.execute(query, params)
            empleados = cursor.fetchall()
            return empleados
        finally:
            cursor.close()
            close_db_connection(conn)
    
    @staticmethod
    def create(data):
        """Crea un nuevo empleado"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO empleado 
                (ci, id_a, id_t, id_b, id_ba, nombres, apellidos, 
                 direccion, telefonos, correo, fecha_nacimiento, 
                 fecha_ingreso, fecha_contrato, salario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING ci
            """, (
                data['ci'], data['id_a'], data['id_t'], data['id_b'], 
                data['id_ba'], data['nombres'], data['apellidos'],
                data['direccion'], data['telefonos'], data['correo'],
                data['fecha_nacimiento'], data['fecha_ingreso'],
                data['fecha_contrato'], data['salario']
            ))
            conn.commit()
            new_ci = cursor.fetchone()['ci']
            return new_ci
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            close_db_connection(conn)
    
    @staticmethod
    def update(ci, data):
        """Actualiza un empleado existente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE empleado 
                SET id_a = %s, id_t = %s, id_b = %s, id_ba = %s,
                    nombres = %s, apellidos = %s, direccion = %s,
                    telefonos = %s, correo = %s, fecha_nacimiento = %s,
                    fecha_ingreso = %s, fecha_contrato = %s, salario = %s
                WHERE ci = %s
            """, (
                data['id_a'], data['id_t'], data['id_b'], data['id_ba'],
                data['nombres'], data['apellidos'], data['direccion'],
                data['telefonos'], data['correo'], data['fecha_nacimiento'],
                data['fecha_ingreso'], data['fecha_contrato'], data['salario'],
                ci
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            close_db_connection(conn)
    
    @staticmethod
    def delete(ci):
        """Elimina un empleado"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM empleado WHERE ci = %s", (ci,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            close_db_connection(conn)