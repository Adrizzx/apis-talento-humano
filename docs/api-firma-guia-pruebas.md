# GUÍA DE PRUEBAS COMPLETA - API REST DE FIRMAS

## TABLA DE CONTENIDOS

1. [Configuración Inicial](#configuración-inicial)
2. [Orden de Pruebas](#orden-de-pruebas)
3. [Pruebas de Verificación](#pruebas-de-verificación)
4. [Prueba Completa: Jornada Laboral](#prueba-completa-jornada-laboral)
5. [Pruebas de Consulta](#pruebas-de-consulta)
6. [Pruebas de Actualización](#pruebas-de-actualización)
7. [Pruebas de Autocompletado](#pruebas-de-autocompletado)
8. [Pruebas de Eliminación](#pruebas-de-eliminación)
9. [Verificación en Base de Datos](#verificación-en-base-de-datos)
10. [Limpieza de Datos](#limpieza-de-datos)

---

## CONFIGURACIÓN INICIAL

### Requisitos Previos

- API REST ejecutándose en `http://localhost:5001`
- PostgreSQL activo con la base de datos `personal_postgres`
- Postman instalado
- Colección de API Firma importada en Postman

### Iniciar la API

Si la API no está en ejecución, ejecutar el siguiente comando en terminal:

```bash
cd c:/Users/adria/api_firma
venv/bin/python.exe run.py
```

Debe aparecer el mensaje:

```
============================================================
Iniciando API de Firmas - Sistema de Asistencia
============================================================
Servidor: http://localhost:5001
```

---

## ORDEN DE PRUEBAS

Se recomienda seguir el siguiente orden para una evaluación completa del sistema:

1. Verificación del estado de la API (Health Check)
2. Consulta de firmas existentes
3. Registro completo de jornada laboral (6 eventos)
4. Consultas específicas por diferentes criterios
5. Actualización manual de registros
6. Autocompletado de registros incompletos
7. Eliminación de registros
8. Validación de errores y excepciones

---

## PRUEBAS DE VERIFICACIÓN

### PRUEBA 1: Health Check

**Objetivo:** Verificar que la API está funcionando correctamente y tiene conexión con la base de datos.

**Configuración en Postman:**
- Método: `GET`
- URL: `http://localhost:5001/api/health`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "API de Firmas funcionando correctamente",
    "status": "healthy",
    "timestamp": "2026-02-03T10:30:00.123456"
}

```

**Código de Estado HTTP:** `200 OK`

**Validación:** Si recibe esta respuesta, la API está operativa y la conexión a la base de datos es correcta.

---

### PRUEBA 2: Consultar Todas las Firmas

**Objetivo:** Obtener el listado completo de registros de asistencia en el sistema.

**Configuración en Postman:**
- Método: `GET`
- URL: `http://localhost:5001/api/firmas`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "data": [
        {
            "id_f": 1,
            "fecha_firma": "2026-02-03",
            "h_i_jornada": "08:00:00",
            "ci": "1700000001",
            "empleado": {
                "ci": "1700000001",
                "nombres": "EMPLEADO DEMO",
                "apellidos": "EMPLEADO DEMO"
            }
        }
    ],
    "total": 1,
    "message": "Se encontraron 1 firmas"
}
```

**Verificación en Base de Datos:**

```sql
SELECT * FROM firma ORDER BY fecha_firma DESC, id_f DESC;
```

---

### PRUEBA 3: Consultar Firmas del Día Actual

**Objetivo:** Obtener únicamente los registros de asistencia del día actual.

**Configuración en Postman:**
- Método: `GET`
- URL: `http://localhost:5001/api/firmas/hoy`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "data": [],
    "total": 0,
    "fecha": "2026-02-03",
    "message": "Se encontraron 0 firmas para hoy"
}
```

---

### PRUEBA 4: Consultar Firmas Incompletas

**Objetivo:** Identificar registros de empleados que no finalizaron su jornada laboral.

**Configuración en Postman:**
- Método: `GET`
- URL: `http://localhost:5001/api/firmas/incompletas`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "data": [],
    "total": 0,
    "message": "Se encontraron 0 firmas incompletas"
}
```

**Verificación en Base de Datos:**

```sql
SELECT * FROM firma WHERE h_f_jornada IS NULL ORDER BY fecha_firma DESC;
```

---

## PRUEBA COMPLETA: JORNADA LABORAL

Esta sección simula el registro completo de asistencia de un empleado durante una jornada laboral normal, desde el inicio hasta la finalización.

**Datos del Empleado:**
- CI: `1700000001`
- Nombre: EMPLEADO DEMO EMPLEADO DEMO
- Fecha: `2026-02-03`

### EVENTO 1: Inicio de Jornada

**Hora:** 08:00:00

**Objetivo:** Registrar el momento en que el empleado inicia su jornada laboral.

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:5001/api/firmas/procesar`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "hora_actual": "08:00:00"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Inicio de jornada registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "INICIO_JORNADA",
    "data": {
        "id_f": 1,
        "fecha_firma": "2026-02-03",
        "h_i_jornada": "08:00:00",
        "a_i_jornada": "00:00:00",
        "ci": "1700000001",
        "id_t": 3,
        "id_b": 8,
        "id_ba": 18
    },
    "detalles": {
        "hora_registro": "08:00:00",
        "hora_esperada": "08:00:00",
        "atraso": "00:00:00"
    }
}
```

**Código de Estado HTTP:** `201 Created`

**Operación Realizada:** INSERT en tabla firma

**Verificación en Base de Datos:**

```sql
SELECT 
    id_f, fecha_firma, h_i_jornada, a_i_jornada, ci,
    h_i_break, h_f_break, h_i_almuerzo, h_f_almuerzo, h_f_jornada
FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';
```

**Resultado Esperado:**
- h_i_jornada: 08:00:00
- a_i_jornada: 00:00:00
- h_i_break: NULL
- h_f_break: NULL
- h_i_almuerzo: NULL
- h_f_almuerzo: NULL
- h_f_jornada: NULL

---

### EVENTO 2: Salida a Break

**Hora:** 10:30:00

**Objetivo:** Registrar el momento en que el empleado sale a su receso.

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:5001/api/firmas/procesar`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "hora_actual": "10:30:00"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Salida Break registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "SALIDA_BREAK",
    "data": {
        "id_f": 1,
        "h_i_break": "10:30:00"
    },
    "detalles": {
        "hora_salida_break": "10:30:00"
    }
}
```

**Código de Estado HTTP:** `200 OK`

**Operación Realizada:** UPDATE en tabla firma (mismo registro)

**Verificación en Base de Datos:**

```sql
SELECT h_i_jornada, h_i_break, h_f_break 
FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';
```

**Resultado Esperado:**
- h_i_jornada: 08:00:00
- h_i_break: 10:30:00
- h_f_break: NULL

---

### EVENTO 3: Regreso de Break

**Hora:** 10:47:00

**Objetivo:** Registrar el regreso del empleado después del receso y calcular el atraso si existe.

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:5001/api/firmas/procesar`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "hora_actual": "10:47:00"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Regreso Break registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "REGRESO_BREAK",
    "data": {
        "id_f": 1,
        "h_f_break": "10:47:00",
        "a_f_break": "00:02:00"
    },
    "detalles": {
        "hora_regreso_break": "10:47:00",
        "hora_esperada_regreso": "10:45:00",
        "atraso": "00:02:00"
    }
}
```

**Código de Estado HTTP:** `200 OK`

**Operación Realizada:** UPDATE en tabla firma

**Cálculo de Atraso:** El sistema calcula automáticamente la diferencia entre la hora esperada de regreso y la hora real. En este caso: 10:47:00 - 10:45:00 = 00:02:00

**Verificación en Base de Datos:**

```sql
SELECT h_i_break, h_f_break, a_f_break 
FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';
```

**Resultado Esperado:**
- h_i_break: 10:30:00
- h_f_break: 10:47:00
- a_f_break: 00:02:00

---

### EVENTO 4: Salida a Almuerzo

**Hora:** 13:00:00

**Objetivo:** Registrar el momento en que el empleado sale a su hora de almuerzo.

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:5001/api/firmas/procesar`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "hora_actual": "13:00:00"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Salida Almuerzo registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "SALIDA_ALMUERZO",
    "data": {
        "id_f": 1,
        "h_i_almuerzo": "13:00:00"
    },
    "detalles": {
        "hora_salida_almuerzo": "13:00:00"
    }
}
```

**Código de Estado HTTP:** `200 OK`

**Operación Realizada:** UPDATE en tabla firma

**Verificación en Base de Datos:**

```sql
SELECT h_i_almuerzo, h_f_almuerzo 
FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';
```

**Resultado Esperado:**
- h_i_almuerzo: 13:00:00
- h_f_almuerzo: NULL

---

### EVENTO 5: Regreso de Almuerzo

**Hora:** 14:05:00

**Objetivo:** Registrar el regreso del empleado después del almuerzo y calcular el atraso si existe.

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:5001/api/firmas/procesar`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "hora_actual": "14:05:00"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Regreso Almuerzo registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "REGRESO_ALMUERZO",
    "data": {
        "id_f": 1,
        "h_f_almuerzo": "14:05:00",
        "a_f_almuerzo": "00:05:00"
    },
    "detalles": {
        "hora_regreso_almuerzo": "14:05:00",
        "hora_esperada_regreso": "14:00:00",
        "atraso": "00:05:00"
    }
}
```

**Código de Estado HTTP:** `200 OK`

**Operación Realizada:** UPDATE en tabla firma

**Cálculo de Atraso:** 14:05:00 - 14:00:00 = 00:05:00

**Verificación en Base de Datos:**

```sql
SELECT h_i_almuerzo, h_f_almuerzo, a_f_almuerzo 
FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';
```

**Resultado Esperado:**
- h_i_almuerzo: 13:00:00
- h_f_almuerzo: 14:05:00
- a_f_almuerzo: 00:05:00

---

### EVENTO 6: Fin de Jornada

**Hora:** 16:00:00

**Objetivo:** Registrar la finalización de la jornada laboral del empleado.

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:5001/api/firmas/procesar`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "hora_actual": "16:00:00"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Fin de jornada registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "FIN_JORNADA",
    "data": {
        "id_f": 1,
        "h_f_jornada": "16:00:00"
    },
    "detalles": {
        "hora_fin_jornada": "16:00:00"
    }
}
```

**Código de Estado HTTP:** `200 OK`

**Operación Realizada:** UPDATE en tabla firma

**Estado Final:** Jornada completa registrada exitosamente.

**Verificación Completa en Base de Datos:**

```sql
SELECT 
    id_f,
    fecha_firma,
    h_i_jornada,
    a_i_jornada,
    h_i_break,
    h_f_break,
    a_f_break,
    h_i_almuerzo,
    h_f_almuerzo,
    a_f_almuerzo,
    h_f_jornada,
    ci
FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';
```

**Resultado Esperado (Registro Completo):**

| Campo | Valor |
|-------|-------|
| id_f | 1 |
| fecha_firma | 2026-02-03 |
| h_i_jornada | 08:00:00 |
| a_i_jornada | 00:00:00 |
| h_i_break | 10:30:00 |
| h_f_break | 10:47:00 |
| a_f_break | 00:02:00 |
| h_i_almuerzo | 13:00:00 |
| h_f_almuerzo | 14:05:00 |
| a_f_almuerzo | 00:05:00 |
| h_f_jornada | 16:00:00 |
| ci | 1700000001 |

---

### VALIDACIÓN: Intento de Registro Adicional

**Objetivo:** Verificar que el sistema no permita registrar eventos adicionales cuando la jornada ya está completa.

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:5001/api/firmas/procesar`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "hora_actual": "17:00:00"
}
```

**Respuesta Esperada (Error):**

```json
{
    "success": false,
    "error": "La jornada ya ha sido completada para este empleado en esta fecha"
}
```

**Código de Estado HTTP:** `400 Bad Request`

**Validación:** El sistema correctamente rechaza el intento de registrar eventos adicionales cuando todos los campos de la jornada están completos.

---

## PRUEBAS DE CONSULTA

### CONSULTA 1: Firma por ID

**Objetivo:** Recuperar un registro específico mediante su identificador único.

**Configuración en Postman:**
- Método: `GET`
- URL: `http://localhost:5001/api/firmas/1`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "data": {
        "id_f": 1,
        "fecha_firma": "2026-02-03",
        "h_i_jornada": "08:00:00",
        "a_i_jornada": "00:00:00",
        "h_i_break": "10:30:00",
        "h_f_break": "10:47:00",
        "a_f_break": "00:02:00",
        "h_i_almuerzo": "13:00:00",
        "h_f_almuerzo": "14:05:00",
        "a_f_almuerzo": "00:05:00",
        "h_f_jornada": "16:00:00",
        "ci": "1700000001",
        "empleado": {
            "ci": "1700000001",
            "nombres": "EMPLEADO DEMO",
            "apellidos": "EMPLEADO DEMO"
        }
    },
    "message": "Firma encontrada"
}
```

---

### CONSULTA 2: Todas las Firmas de un Empleado

**Objetivo:** Obtener el historial completo de asistencia de un empleado específico.

**Configuración en Postman:**
- Método: `GET`
- URL: `http://localhost:5001/api/firmas/empleado/1700000001`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "data": [
        {
            "id_f": 1,
            "fecha_firma": "2026-02-03",
            "h_i_jornada": "08:00:00",
            "ci": "1700000001"
        }
    ],
    "total": 1,
    "empleado": {
        "ci": "1700000001",
        "nombre_completo": "EMPLEADO DEMO EMPLEADO DEMO"
    },
    "message": "Se encontraron 1 firmas para EMPLEADO DEMO EMPLEADO DEMO"
}
```

**Verificación en Base de Datos:**

```sql
SELECT * FROM firma 
WHERE ci = '1700000001' 
ORDER BY fecha_firma DESC;
```

---

### CONSULTA 3: Firma por Empleado y Fecha

**Objetivo:** Obtener el registro de asistencia de un empleado en una fecha específica.

**Configuración en Postman:**
- Método: `GET`
- URL: `http://localhost:5001/api/firmas/empleado/1700000001/fecha/2026-02-03`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "data": {
        "id_f": 1,
        "fecha_firma": "2026-02-03",
        "h_i_jornada": "08:00:00",
        "h_f_jornada": "16:00:00",
        "ci": "1700000001",
        "empleado": {
            "ci": "1700000001",
            "nombres": "EMPLEADO DEMO",
            "apellidos": "EMPLEADO DEMO"
        }
    },
    "message": "Firma encontrada"
}
```

---

### CONSULTA 4: Todas las Firmas de una Fecha

**Objetivo:** Obtener todos los registros de asistencia de todos los empleados en una fecha específica.

**Configuración en Postman:**
- Método: `GET`
- URL: `http://localhost:5001/api/firmas/fecha/2026-02-03`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "data": [
        {
            "id_f": 1,
            "fecha_firma": "2026-02-03",
            "ci": "1700000001",
            "empleado": {
                "nombres": "EMPLEADO DEMO",
                "apellidos": "EMPLEADO DEMO"
            }
        }
    ],
    "total": 1,
    "fecha": "2026-02-03",
    "message": "Se encontraron 1 firmas para la fecha 2026-02-03"
}
```

**Verificación en Base de Datos:**

```sql
SELECT f.*, e.nombres, e.apellidos
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
WHERE f.fecha_firma = '2026-02-03'
ORDER BY f.ci;
```

---

## PRUEBAS DE ACTUALIZACIÓN

### ACTUALIZACIÓN 1: Agregar Observación

**Objetivo:** Añadir o modificar el campo de observaciones en un registro existente.

**Configuración en Postman:**
- Método: `PUT`
- URL: `http://localhost:5001/api/firmas/1`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "observacion": "Empleado presento certificado medico por cita con especialista"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Firma actualizada correctamente. Campos actualizados: Observación",
    "data": {
        "id_f": 1,
        "observacion": "Empleado presento certificado medico por cita con especialista",
        "fecha_firma": "2026-02-03",
        "ci": "1700000001"
    }
}
```

**Código de Estado HTTP:** `200 OK`

**Verificación en Base de Datos:**

```sql
SELECT id_f, ci, fecha_firma, observacion 
FROM firma 
WHERE id_f = 1;
```

---

### ACTUALIZACIÓN 2: Modificar Hora de Fin de Jornada

**Objetivo:** Actualizar la hora de finalización de jornada y agregar justificación.

**Configuración en Postman:**
- Método: `PUT`
- URL: `http://localhost:5001/api/firmas/1`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "h_f_jornada": "17:30:00",
    "observacion": "Hora extra aprobada por supervisor para culminar proyecto urgente"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Firma actualizada correctamente. Campos actualizados: Hora fin jornada, Observación",
    "data": {
        "id_f": 1,
        "h_f_jornada": "17:30:00",
        "observacion": "Hora extra aprobada por supervisor para culminar proyecto urgente",
        "fecha_firma": "2026-02-03",
        "ci": "1700000001"
    }
}
```

**Código de Estado HTTP:** `200 OK`

**Verificación en Base de Datos:**

```sql
SELECT id_f, h_f_jornada, observacion 
FROM firma 
WHERE id_f = 1;
```

---

## PRUEBAS DE AUTOCOMPLETADO

El autocompletado es una funcionalidad administrativa que permite completar automáticamente registros de jornadas laborales incompletas de días anteriores.

### PREPARACIÓN: Crear Registro Incompleto

**Objetivo:** Crear un registro de jornada del día anterior que no fue completado.

**Configuración en Postman:**
- Método: `POST`
- URL: `http://localhost:5001/api/firmas/procesar`
- Headers: `Content-Type: application/json`
- Body (raw - JSON):

```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-02",
    "hora_actual": "08:30:00"
}
```

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Inicio de jornada registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "INICIO_JORNADA",
    "data": {
        "id_f": 2,
        "fecha_firma": "2026-02-02",
        "h_i_jornada": "08:30:00",
        "ci": "1700000001"
    }
}
```

**Verificación en Base de Datos:**

```sql
SELECT * FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-02';
```

**Estado Esperado:** Solo h_i_jornada tiene valor, los demás campos están en NULL.

---

### EJECUCIÓN: Autocompletar Firmas Incompletas

**Objetivo:** Completar automáticamente las jornadas incompletas de días anteriores.

**Configuración en Postman:**
- Método: `PUT`
- URL: `http://localhost:5001/api/firmas/autocompletar`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "1 firmas autocompletadas correctamente",
    "total": 1,
    "firmas_completadas": [
        {
            "id_f": 2,
            "ci": "1700000001",
            "fecha": "2026-02-02",
            "observacion": "NO FIRMASTE DESDE EL INICIO DE TU BREAK EN ADELANTE. AUTO COMPLETADO"
        }
    ]
}
```

**Código de Estado HTTP:** `200 OK`

**Lógica del Autocompletado:**
1. Detecta el primer campo NULL después de h_i_jornada
2. Completa todos los campos faltantes con 00:00:00
3. Establece h_f_jornada con la hora de fin del turno del empleado
4. Genera una observación explicativa

**Verificación en Base de Datos:**

```sql
SELECT 
    h_i_jornada, h_i_break, h_f_break, 
    h_i_almuerzo, h_f_almuerzo, h_f_jornada,
    observacion
FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-02';
```

**Resultado Esperado:**
- h_i_jornada: 08:30:00 (original)
- h_i_break: 00:00:00 (autocompletado)
- h_f_break: 00:00:00 (autocompletado)
- h_i_almuerzo: 00:00:00 (autocompletado)
- h_f_almuerzo: 00:00:00 (autocompletado)
- h_f_jornada: 17:00:00 (hora del turno)
- observacion: "NO FIRMASTE DESDE EL INICIO DE TU BREAK EN ADELANTE. AUTO COMPLETADO"

---

## PRUEBAS DE ELIMINACIÓN

### ELIMINACIÓN 1: Eliminar Registro Autocompletado

**Objetivo:** Eliminar permanentemente un registro de la base de datos.

**ADVERTENCIA:** Esta operación es irreversible.

**Configuración en Postman:**
- Método: `DELETE`
- URL: `http://localhost:5001/api/firmas/2`
- Body: Ninguno

**Respuesta Esperada:**

```json
{
    "success": true,
    "message": "Firma ID 2 eliminada correctamente (CI: 1700000001, Fecha: 2026-02-02)"
}
```

**Código de Estado HTTP:** `200 OK`

**Verificación en Base de Datos:**

```sql
SELECT * FROM firma WHERE id_f = 2;
```

**Resultado Esperado:** 0 registros (el registro fue eliminado)

---

### ELIMINACIÓN 2: Intentar Eliminar Registro Inexistente

**Objetivo:** Validar el manejo de errores al intentar eliminar un registro que no existe.

**Configuración en Postman:**
- Método: `DELETE`
- URL: `http://localhost:5001/api/firmas/999`
- Body: Ninguno

**Respuesta Esperada (Error):**

```json
{
    "success": false,
    "error": "Firma no encontrada"
}
```

**Código de Estado HTTP:** `404 Not Found`

**Validación:** El sistema maneja correctamente los intentos de eliminar registros inexistentes.

---

## VERIFICACIÓN EN BASE DE DATOS

### Consulta General de Firmas

```sql
SELECT 
    f.id_f,
    f.fecha_firma,
    f.ci,
    e.nombres || ' ' || e.apellidos as nombre_completo,
    f.h_i_jornada,
    f.h_f_jornada,
    CASE 
        WHEN f.h_f_jornada IS NOT NULL THEN 'COMPLETA'
        ELSE 'INCOMPLETA'
    END as estado
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
ORDER BY f.fecha_firma DESC, f.id_f DESC;
```

### Detalle Completo de un Registro

```sql
SELECT 
    f.*,
    e.nombres,
    e.apellidos,
    t.nombre_t as turno,
    t.hora_inicio_t,
    t.hora_fin_t
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
INNER JOIN turno t ON f.id_t = t.id_t
WHERE f.ci = '1700000001' AND f.fecha_firma = '2026-02-03';
```

### Estadísticas de Asistencia

```sql
SELECT 
    e.ci,
    e.nombres || ' ' || e.apellidos as nombre_completo,
    COUNT(*) as total_firmas,
    SUM(CASE WHEN f.h_f_jornada IS NOT NULL THEN 1 ELSE 0 END) as firmas_completas,
    SUM(CASE WHEN f.a_i_jornada > '00:00:00' THEN 1 ELSE 0 END) as dias_con_atraso
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
GROUP BY e.ci, e.nombres, e.apellidos
ORDER BY total_firmas DESC;
```

---

## LIMPIEZA DE DATOS

### Eliminar Registros de Prueba

Después de completar todas las pruebas, se recomienda eliminar los registros de prueba:

```sql
-- Eliminar firmas de fechas específicas
DELETE FROM firma WHERE fecha_firma = '2026-02-03';

-- Eliminar firmas de empleados específicos
DELETE FROM firma WHERE ci IN ('1700000001', '1700000001');

-- Verificar registros restantes
SELECT COUNT(*) as total_registros FROM firma;
```

### Reiniciar Secuencia de ID (Opcional)

Si se eliminaron todos los registros y se desea reiniciar la numeración:

```sql
-- Verificar que no hay registros
SELECT COUNT(*) FROM firma;

-- Si el resultado es 0, reiniciar secuencia
ALTER SEQUENCE firma_id_f_seq RESTART WITH 1;
```

---

## RESUMEN DE PRUEBAS

### Checklist de Validación

#### Pruebas Básicas
- [ ] Health Check exitoso
- [ ] Consulta de todas las firmas
- [ ] Consulta de firmas del día
- [ ] Consulta de firmas incompletas

#### Jornada Completa (6 eventos)
- [ ] Inicio de jornada registrado correctamente
- [ ] Salida a break registrada correctamente
- [ ] Regreso de break con cálculo de atraso
- [ ] Salida a almuerzo registrada correctamente
- [ ] Regreso de almuerzo con cálculo de atraso
- [ ] Fin de jornada registrado correctamente
- [ ] Validación de jornada completa (rechazo de eventos adicionales)

#### Consultas Específicas
- [ ] Consulta por ID funciona correctamente
- [ ] Consulta por empleado (historial completo)
- [ ] Consulta por empleado y fecha específica
- [ ] Consulta por fecha (todos los empleados)

#### Actualizaciones
- [ ] Agregar observación a registro existente
- [ ] Modificar hora de fin de jornada

#### Autocompletado
- [ ] Crear registro incompleto
- [ ] Ejecutar autocompletado exitosamente
- [ ] Verificar generación automática de observación

#### Eliminaciones
- [ ] Eliminar registro existente
- [ ] Validar error al eliminar registro inexistente

#### Validaciones de Error
- [ ] Empleado no encontrado
- [ ] Campo requerido faltante
- [ ] Formato de fecha inválido
- [ ] Actualización de registro inexistente

---

## CONCLUSIONES

Al completar exitosamente todas las pruebas de esta guía, se habrá validado:

1. **Funcionalidad Completa:** Todos los endpoints de la API funcionan correctamente.
2. **Integridad de Datos:** Las operaciones CRUD se ejecutan correctamente en la base de datos.
3. **Lógica de Negocio:** El sistema de registro en cascada funciona como se esperaba.
4. **Cálculos Automáticos:** Los atrasos se calculan correctamente de forma automática.
5. **Validaciones:** El sistema rechaza adecuadamente operaciones inválidas.
6. **Manejo de Errores:** Los mensajes de error son claros y apropiados.

El sistema está listo para su implementación en ambiente de producción.

---

## INFORMACIÓN ADICIONAL

### Empleados Disponibles para Pruebas

| CI | Nombres | Apellidos | Turno |
|----|---------|-----------|-------|
| 1700000001 | EMPLEADO DEMO | EMPLEADO DEMO | 1 |
| 1700000001 | EMPLEADO DEMO | EMPLEADO DEMO | 3 |
| 1700000001 | EMPLEADO DEMO | EMPLEADO DEMO | 1 |
| 1700000001 | EMPLEADO DEMO | EMPLEADO DEMO | 2 |
| 1700000005 | EMPLEADO DEMO | EMPLEADO DEMO | 1 |

### Códigos de Estado HTTP Utilizados

- **200 OK:** Operación exitosa (GET, PUT, DELETE)
- **201 Created:** Recurso creado exitosamente (POST - primer registro)
- **400 Bad Request:** Error en los datos enviados
- **404 Not Found:** Recurso no encontrado
- **500 Internal Server Error:** Error del servidor

### Contacto y Soporte

Para reportar problemas o solicitar asistencia con la API, contactar al equipo de desarrollo.

---

**Fecha de Documento:** 03 de Febrero de 2026  
**Versión de API:** 1.0  
**Base de Datos:** PostgreSQL - personal_postgres  
**Puerto:** 5001
