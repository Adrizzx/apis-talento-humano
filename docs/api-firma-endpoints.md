# 📚 Explicación Completa de Cada Endpoint de la API de Firmas

## 🗃️ SQL para ver las tablas afectadas

```sql
-- Ver la tabla FIRMA (la principal que se afecta)
SELECT * FROM firma ORDER BY fecha_firma DESC, id_f DESC;

-- Ver empleados disponibles (para usar sus CIs)
SELECT ci, nombres, apellidos, id_t, id_b, id_ba FROM empleado ORDER BY ci ASC;

-- Ver turnos
SELECT * FROM turno;

-- Ver breaks/recesos
SELECT * FROM break;

-- Ver firma completa con datos del empleado
SELECT 
    f.id_f,
    f.fecha_firma,
    f.h_i_jornada,
    f.a_i_jornada,
    f.h_i_break,
    f.h_f_break,
    f.a_f_break,
    f.h_i_almuerzo,
    f.h_f_almuerzo,
    f.a_f_almuerzo,
    f.h_f_jornada,
    f.ci,
    e.nombres,
    e.apellidos,
    f.observacion
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
ORDER BY f.fecha_firma DESC;

-- Ver firmas incompletas (no terminaron la jornada)
SELECT 
    f.id_f,
    f.fecha_firma,
    f.ci,
    e.nombres,
    e.apellidos,
    f.h_i_jornada,
    f.h_f_jornada
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
WHERE f.h_f_jornada IS NULL
ORDER BY f.fecha_firma DESC;

-- Ver última firma de cada empleado
SELECT 
    f.ci,
    e.nombres,
    e.apellidos,
    MAX(f.fecha_firma) as ultima_firma
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
GROUP BY f.ci, e.nombres, e.apellidos
ORDER BY ultima_firma DESC;

-- Contar firmas por empleado
SELECT 
    f.ci,
    e.nombres,
    e.apellidos,
    COUNT(*) as total_firmas
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
GROUP BY f.ci, e.nombres, e.apellidos
ORDER BY total_firmas DESC;
```

---

## 📋 Estructura de la Tabla FIRMA

```sql
CREATE TABLE firma (
    id_f SERIAL PRIMARY KEY,              -- ID único de la firma
    fecha_firma DATE,                      -- Fecha del registro
    h_i_jornada TIME,                      -- Hora Inicio Jornada
    a_i_jornada TIME,                      -- Atraso Inicio Jornada
    h_i_break TIME,                        -- Hora Inicio Break
    h_f_break TIME,                        -- Hora Fin Break
    a_f_break TIME,                        -- Atraso Fin Break
    h_i_almuerzo TIME,                     -- Hora Inicio Almuerzo
    h_f_almuerzo TIME,                     -- Hora Fin Almuerzo
    a_f_almuerzo TIME,                     -- Atraso Fin Almuerzo
    h_f_jornada TIME,                      -- Hora Fin Jornada
    ci VARCHAR(40) NOT NULL,               -- Cédula del empleado
    id_t INTEGER NOT NULL,                 -- ID del turno
    id_b INTEGER NOT NULL,                 -- ID del break
    id_ba INTEGER NOT NULL,                -- ID del almuerzo
    observacion VARCHAR(254),              -- Observaciones
    FOREIGN KEY (ci) REFERENCES empleado(ci),
    FOREIGN KEY (id_t) REFERENCES turno(id_t)
);
```

---

## 📋 Endpoints y sus Funciones Detalladas

---

### 🟢 1. **GET /api/health** - Health Check

**URL Completa:** `http://localhost:5001/api/health`

#### ¿Qué hace?
- Verifica que la API está funcionando correctamente
- Comprueba la conexión a la base de datos
- No afecta ninguna tabla, solo responde si el servidor está vivo

#### Cuándo usarlo:
- Al iniciar la API
- Para verificar que todo está funcionando
- Para troubleshooting
- En monitoreo automático

#### SQL afectado:
```sql
SELECT 1;  -- Solo verifica conexión
```

#### Response ejemplo:
```json
{
    "success": true,
    "message": "API de Firmas funcionando correctamente",
    "status": "healthy",
    "timestamp": "2026-02-03T10:30:00.123456"
}
```

---

### 🟢 2. **GET /api/firmas** - Obtener Todas las Firmas

**URL Completa:** `http://localhost:5001/api/firmas`

#### ¿Qué hace?
- Consulta TODAS las firmas registradas en la base de datos
- Trae información del empleado y turno (con JOIN)
- Ordena por fecha descendente (más recientes primero)
- Incluye nested data de empleado y turno

#### Cuándo usarlo:
- Ver historial completo de asistencia
- Generar reportes generales
- Dashboard administrativo
- Exportar datos a Excel

#### SQL ejecutado:
```sql
SELECT * FROM firma 
ORDER BY fecha_firma DESC, id_f DESC;

-- Con JOINs para nested data:
SELECT f.*, e.nombres, e.apellidos, t.nombre_t
FROM firma f
LEFT JOIN empleado e ON f.ci = e.ci
LEFT JOIN turno t ON f.id_t = t.id_t
ORDER BY f.fecha_firma DESC, f.id_f DESC;
```

#### Response ejemplo:
```json
{
    "success": true,
    "data": [
        {
            "id_f": 1,
            "fecha_firma": "2026-02-03",
            "h_i_jornada": "08:35:00",
            "ci": "1700000001",
            "empleado": {
                "ci": "1700000001",
                "nombres": "EMPLEADO DEMO",
                "apellidos": "EMPLEADO DEMO"
            },
            "turno": {
                "id_t": 2,
                "nombre_t": "Matutino"
            }
        }
    ],
    "total": 1,
    "message": "Se encontraron 1 firmas"
}
```

---

### 🟢 3. **GET /api/firmas/hoy** - Firmas de Hoy

**URL Completa:** `http://localhost:5001/api/firmas/hoy`

#### ¿Qué hace?
- Trae solo las firmas del día actual (2026-02-03)
- Lista quién ha firmado hoy
- Útil para control diario

#### Cuándo usarlo:
- Control diario de asistencia
- Ver quién está trabajando hoy
- Reporte del día
- Dashboard en tiempo real

#### SQL ejecutado:
```sql
SELECT * FROM firma 
WHERE fecha_firma = CURRENT_DATE
ORDER BY h_i_jornada;
```

#### Response ejemplo:
```json
{
    "success": true,
    "data": [...],
    "total": 8,
    "fecha": "2026-02-03",
    "message": "Se encontraron 8 firmas para hoy"
}
```

---

### 🟢 4. **GET /api/firmas/{id_f}** - Obtener Firma por ID

**URL Ejemplo:** `http://localhost:5001/api/firmas/1`

#### ¿Qué hace?
- Busca UNA firma específica por su ID único
- Trae todos los detalles de esa firma
- Incluye información del empleado y turno

#### Cuándo usarlo:
- Ver detalles de una firma específica
- Después de crear una firma para verificarla
- En actualizaciones para confirmar cambios
- Auditoría de registro específico

#### SQL ejecutado:
```sql
SELECT * FROM firma WHERE id_f = 1;
```

#### Response ejemplo:
```json
{
    "success": true,
    "data": {
        "id_f": 1,
        "fecha_firma": "2026-02-03",
        "h_i_jornada": "08:35:00",
        "a_i_jornada": "00:05:00",
        "h_i_break": "10:30:00",
        "h_f_break": "10:47:00",
        "a_f_break": "00:02:00",
        "h_i_almuerzo": "13:00:00",
        "h_f_almuerzo": "14:05:00",
        "a_f_almuerzo": "00:05:00",
        "h_f_jornada": "17:30:00",
        "ci": "1700000001",
        "id_t": 2,
        "id_b": 7,
        "id_ba": 15,
        "observacion": null
    },
    "message": "Firma encontrada"
}
```

---

### 🟢 5. **GET /api/firmas/empleado/{ci}** - Firmas de un Empleado

**URL Ejemplo:** `http://localhost:5001/api/firmas/empleado/1700000001`

#### ¿Qué hace?
- Trae TODAS las firmas históricas de un empleado específico
- Ordena por fecha descendente (más recientes primero)
- Muestra el nombre completo del empleado

#### Cuándo usarlo:
- Ver historial de asistencia de un empleado
- Auditoría de asistencia individual
- Reporte de horas trabajadas por persona
- Verificar atrasos recurrentes

#### SQL ejecutado:
```sql
SELECT * FROM firma 
WHERE ci = '1700000001'
ORDER BY fecha_firma DESC;
```

#### Response ejemplo:
```json
{
    "success": true,
    "data": [...],
    "total": 15,
    "empleado": {
        "ci": "1700000001",
        "nombre_completo": "EMPLEADO DEMO EMPLEADO DEMO"
    },
    "message": "Se encontraron 15 firmas para EMPLEADO DEMO EMPLEADO DEMO"
}
```

---

### 🟢 6. **GET /api/firmas/empleado/{ci}/fecha/{fecha}** - Firma Específica

**URL Ejemplo:** `http://localhost:5001/api/firmas/empleado/1700000001/fecha/2026-02-03`

#### ¿Qué hace?
- Busca la firma de un empleado en una fecha específica
- Solo devuelve UNA firma (la del día solicitado)
- Combinación de búsqueda por CI y fecha

#### Cuándo usarlo:
- Verificar si un empleado firmó un día específico
- Ver detalles de asistencia de un día concreto
- Auditoría puntual
- Resolver consultas específicas

#### SQL ejecutado:
```sql
SELECT * FROM firma 
WHERE ci = '1700000001' 
AND fecha_firma = '2026-02-03';
```

#### Response ejemplo:
```json
{
    "success": true,
    "data": {
        "id_f": 1,
        "fecha_firma": "2026-02-03",
        "h_i_jornada": "08:35:00",
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

### 🟢 7. **GET /api/firmas/fecha/{fecha}** - Todas las Firmas de una Fecha

**URL Ejemplo:** `http://localhost:5001/api/firmas/fecha/2026-02-03`

#### ¿Qué hace?
- Trae todas las firmas de TODOS los empleados en una fecha específica
- Lista de asistencia completa del día
- Útil para reportes diarios

#### Cuándo usarlo:
- Reporte diario de asistencia
- Ver quiénes trabajaron un día específico
- Estadísticas del día
- Control de asistencia masivo

#### SQL ejecutado:
```sql
SELECT * FROM firma 
WHERE fecha_firma = '2026-02-03'
ORDER BY ci;
```

#### Response ejemplo:
```json
{
    "success": true,
    "data": [...],
    "total": 12,
    "fecha": "2026-02-03",
    "message": "Se encontraron 12 firmas para la fecha 2026-02-03"
}
```

---

### 🟢 8. **GET /api/firmas/incompletas** - Firmas Sin Terminar

**URL Completa:** `http://localhost:5001/api/firmas/incompletas`

#### ¿Qué hace?
- Busca firmas donde el empleado NO terminó su jornada
- Detecta cuando `h_f_jornada` es NULL
- Identifica empleados que no firmaron la salida

#### Cuándo usarlo:
- Control de fin de día
- Detectar empleados que olvidaron firmar
- Antes de ejecutar autocompletar
- Alertas de asistencia

#### SQL ejecutado:
```sql
SELECT * FROM firma 
WHERE h_f_jornada IS NULL
ORDER BY fecha_firma DESC;
```

#### Response ejemplo:
```json
{
    "success": true,
    "data": [
        {
            "id_f": 5,
            "fecha_firma": "2026-02-02",
            "h_i_jornada": "08:30:00",
            "h_f_jornada": null,
            "ci": "1700000001",
            "empleado": {
                "nombres": "EMPLEADO DEMO",
                "apellidos": "EMPLEADO DEMO"
            }
        }
    ],
    "total": 3,
    "message": "Se encontraron 3 firmas incompletas"
}
```

---

### 🔵 9. **POST /api/firmas/iniciar-jornada** - Inicio Manual de Jornada

**URL Completa:** `http://localhost:5001/api/firmas/iniciar-jornada`

#### ¿Qué hace?
- **INSERTA** un nuevo registro en la tabla firma
- Registra el inicio de jornada de un empleado
- Calcula el atraso automáticamente comparando con hora de turno
- Valida que no exista otra firma del mismo empleado en la misma fecha

#### Cuándo usarlo:
- Cuando un empleado llega y marca su entrada
- Primera firma del día
- Registro manual administrativo
- Sistema de entrada controlado

#### Body necesario:
```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "h_i_jornada": "08:35:00",
    "a_i_jornada": "00:05:00"
}
```

#### SQL ejecutado:
```sql
-- 1. Validar que el empleado existe
SELECT * FROM empleado WHERE ci = '1700000001';

-- 2. Verificar que no exista firma
SELECT * FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';

-- 3. Obtener datos del empleado (turno, breaks)
SELECT id_t, id_b, id_ba FROM empleado WHERE ci = '1700000001';

-- 4. Insertar la nueva firma
INSERT INTO firma (
    fecha_firma, h_i_jornada, a_i_jornada, 
    ci, id_t, id_b, id_ba
) VALUES (
    '2026-02-03', '08:35:00', '00:05:00', 
    '1700000001', 2, 7, 15
);
```

#### Response ejemplo:
```json
{
    "success": true,
    "message": "Jornada iniciada correctamente para EMPLEADO DEMO EMPLEADO DEMO",
    "data": {
        "id_f": 1,
        "fecha_firma": "2026-02-03",
        "h_i_jornada": "08:35:00",
        "a_i_jornada": "00:05:00",
        "h_i_break": null,
        "h_f_break": null,
        "ci": "1700000001",
        "id_t": 2,
        "id_b": 7,
        "id_ba": 15
    }
}
```

---

### 🔵 10. **POST /api/firmas/procesar** - Procesar Firma AUTOMÁTICA ⭐

**URL Completa:** `http://localhost:5001/api/firmas/procesar`

#### ¿Qué hace?
- **EL MÁS IMPORTANTE Y PODEROSO DEL SISTEMA**
- Detecta automáticamente qué evento registrar según el estado actual
- Puede hacer **INSERT** (si no existe) o **UPDATE** (si existe)
- Implementa la lógica de verificación en cascada de NULL
- Calcula atrasos automáticamente

#### Lógica en cascada (verificación de NULL):
1. **Si NO existe firma** → **INSERT** inicio de jornada
2. **Si existe y `h_i_break = NULL`** → **UPDATE** salida a break
3. **Si existe y `h_f_break = NULL`** → **UPDATE** regreso de break + calcula atraso
4. **Si existe y `h_i_almuerzo = NULL`** → **UPDATE** salida a almuerzo
5. **Si existe y `h_f_almuerzo = NULL`** → **UPDATE** regreso de almuerzo + calcula atraso
6. **Si existe y `h_f_jornada = NULL`** → **UPDATE** fin de jornada
7. **Si todos están completos** → Error: jornada ya completada

#### Cuándo usarlo:
- **TODO EL TIEMPO** - Es el endpoint principal
- Cuando un empleado firma (no importa en qué momento del día)
- Sistema de reloj checador automático
- App móvil de asistencia
- Terminales de registro biométrico

#### Body necesario:
```json
{
    "ci": "1700000001",
    "fecha_firma": "2026-02-03",
    "hora_actual": "08:35:00"
}
```

**Nota:** Si no se envía `fecha_firma`, usa la fecha actual. Si no se envía `hora_actual`, usa la hora actual del servidor.

#### SQL ejecutado:
```sql
-- 1. Validar empleado
SELECT * FROM empleado WHERE ci = '1700000001';

-- 2. Buscar firma existente
SELECT * FROM firma 
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';

-- 3a. Si NO existe, INSERT:
INSERT INTO firma (
    fecha_firma, h_i_jornada, a_i_jornada, 
    ci, id_t, id_b, id_ba
) VALUES (
    '2026-02-03', '08:35:00', '00:05:00', 
    '1700000001', 2, 7, 15
);

-- 3b. Si existe, UPDATE según campo NULL:

-- Ejemplo: Salida a break
UPDATE firma 
SET h_i_break = '10:30:00'
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';

-- Ejemplo: Regreso de break
UPDATE firma 
SET h_f_break = '10:47:00',
    a_f_break = '00:02:00'
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';

-- Ejemplo: Fin de jornada
UPDATE firma 
SET h_f_jornada = '17:30:00'
WHERE ci = '1700000001' AND fecha_firma = '2026-02-03';
```

#### Response ejemplo (Inicio de jornada):
```json
{
    "success": true,
    "message": "✅ Inicio de jornada registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "INICIO_JORNADA",
    "data": {
        "id_f": 1,
        "fecha_firma": "2026-02-03",
        "h_i_jornada": "08:35:00",
        "a_i_jornada": "00:05:00",
        "ci": "1700000001"
    },
    "detalles": {
        "hora_registro": "08:35:00",
        "hora_esperada": "08:30:00",
        "atraso": "00:05:00"
    }
}
```

#### Response ejemplo (Regreso de break):
```json
{
    "success": true,
    "message": "✅ Regreso Break registrado para EMPLEADO DEMO EMPLEADO DEMO",
    "evento": "REGRESO_BREAK",
    "data": {
        "id_f": 1,
        "h_i_break": "10:30:00",
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

---

### 🟡 11. **PUT /api/firmas/{id_f}** - Actualizar Firma Manual

**URL Ejemplo:** `http://localhost:5001/api/firmas/1`

#### ¿Qué hace?
- **ACTUALIZA** campos específicos de una firma existente
- Permite modificar horas, atrasos, observaciones
- Control manual administrativo
- Correcciones puntuales

#### Cuándo usarlo:
- Correcciones administrativas
- Ajustes por permisos especiales
- Modificar observaciones
- Corregir errores de registro
- Ajustes manuales por recursos humanos

#### Body necesario:
```json
{
    "h_f_jornada": "18:00:00",
    "observacion": "Empleado llegó tarde por cita médica"
}
```

**Nota:** Solo envías los campos que quieres actualizar.

#### SQL ejecutado:
```sql
-- 1. Verificar que la firma existe
SELECT * FROM firma WHERE id_f = 1;

-- 2. Actualizar campos específicos
UPDATE firma 
SET h_f_jornada = '18:00:00',
    observacion = 'Empleado llegó tarde por cita médica'
WHERE id_f = 1;
```

#### Response ejemplo:
```json
{
    "success": true,
    "message": "Firma actualizada correctamente. Campos actualizados: Hora fin jornada, Observación",
    "data": {
        "id_f": 1,
        "fecha_firma": "2026-02-03",
        "h_f_jornada": "18:00:00",
        "observacion": "Empleado llegó tarde por cita médica"
    }
}
```

---

### 🟡 12. **PUT /api/firmas/autocompletar** - Autocompletar Pendientes

**URL Completa:** `http://localhost:5001/api/firmas/autocompletar`

#### ¿Qué hace?
- Busca firmas INCOMPLETAS de días anteriores (no de hoy)
- Las completa automáticamente con:
  - Campos NULL → `00:00:00`
  - `h_f_jornada` → Hora de fin del turno del empleado
  - Observación explicando qué paso olvidó

#### Observaciones que genera:
- "NO FIRMASTE DESDE EL INICIO DE TU BREAK EN ADELANTE. AUTO COMPLETADO"
- "NO FIRMASTE DESDE EL FIN DE TU BREAK EN ADELANTE. AUTO COMPLETADO"
- "NO FIRMASTE DESDE EL INICIO DE TU ALMUERZO EN ADELANTE. AUTO COMPLETADO"
- "NO FIRMASTE DESDE EL FIN DE TU ALMUERZO EN ADELANTE. AUTO COMPLETADO"
- "NO FIRMASTE LA SALIDA DE TU JORNADA. AUTO COMPLETADO"

#### Cuándo usarlo:
- Fin de mes (cierre de planillas)
- Limpiar registros incompletos
- Automatización nocturna (cron job)
- Antes de generar reportes
- Control de calidad de datos

#### SQL ejecutado:
```sql
-- 1. Buscar firmas incompletas de días anteriores
SELECT * FROM firma 
WHERE h_f_jornada IS NULL 
AND fecha_firma < CURRENT_DATE;

-- 2. Para cada firma encontrada, obtener turno
SELECT hora_fin_t FROM turno 
WHERE id_t = (SELECT id_t FROM firma WHERE id_f = X);

-- 3. Actualizar cada firma según el primer NULL encontrado
UPDATE firma 
SET h_i_break = '00:00:00',
    h_f_break = '00:00:00',
    h_i_almuerzo = '00:00:00',
    h_f_almuerzo = '00:00:00',
    h_f_jornada = '17:00:00',  -- hora_fin_t del turno
    observacion = 'NO FIRMASTE DESDE EL INICIO DE TU BREAK EN ADELANTE. AUTO COMPLETADO'
WHERE id_f = X;
```

#### Response ejemplo:
```json
{
    "success": true,
    "message": "✅ 3 firmas autocompletadas correctamente",
    "total": 3,
    "firmas_completadas": [
        {
            "id_f": 5,
            "ci": "1700000001",
            "fecha": "2026-02-01",
            "observacion": "NO FIRMASTE LA SALIDA DE TU JORNADA. AUTO COMPLETADO"
        },
        {
            "id_f": 8,
            "ci": "1700000001",
            "fecha": "2026-02-01",
            "observacion": "NO FIRMASTE DESDE EL INICIO DE TU ALMUERZO EN ADELANTE. AUTO COMPLETADO"
        },
        {
            "id_f": 12,
            "ci": "1700000001",
            "fecha": "2026-02-02",
            "observacion": "NO FIRMASTE DESDE EL FIN DE TU BREAK EN ADELANTE. AUTO COMPLETADO"
        }
    ]
}
```

---

### 🔴 13. **DELETE /api/firmas/{id_f}** - Eliminar Firma

**URL Ejemplo:** `http://localhost:5001/api/firmas/1`

#### ¿Qué hace?
- **ELIMINA** permanentemente una firma de la base de datos
- No se puede recuperar (eliminación física)
- Acción irreversible

#### Cuándo usarlo:
- Corregir errores graves
- Eliminar registros duplicados
- Pruebas/testing
- Limpieza de datos erróneos
- **⚠️ USAR CON PRECAUCIÓN**

#### SQL ejecutado:
```sql
-- 1. Verificar que existe
SELECT * FROM firma WHERE id_f = 1;

-- 2. Eliminar
DELETE FROM firma WHERE id_f = 1;
```

#### Response ejemplo:
```json
{
    "success": true,
    "message": "✅ Firma ID 1 eliminada correctamente (CI: 1700000001, Fecha: 2026-02-03)"
}
```

---

## 🎯 Flujo Típico de Uso - Día Completo

### **Jornada Normal de un Empleado:**

```
8:35 AM - LLEGADA
┌─────────────────────────────────────────┐
│ POST /api/firmas/procesar               │
│ {                                       │
│   "ci": "1700000001",                   │
│   "hora_actual": "08:35:00"             │
│ }                                       │
│ → INSERT nueva firma                    │
│ → h_i_jornada = "08:35:00"             │
│ → a_i_jornada = "00:05:00" (calculado) │
└─────────────────────────────────────────┘

10:30 AM - SALE A BREAK
┌─────────────────────────────────────────┐
│ POST /api/firmas/procesar               │
│ {                                       │
│   "ci": "1700000001",                   │
│   "hora_actual": "10:30:00"             │
│ }                                       │
│ → UPDATE h_i_break = "10:30:00"        │
└─────────────────────────────────────────┘

10:47 AM - REGRESA DE BREAK
┌─────────────────────────────────────────┐
│ POST /api/firmas/procesar               │
│ {                                       │
│   "ci": "1700000001",                   │
│   "hora_actual": "10:47:00"             │
│ }                                       │
│ → UPDATE h_f_break = "10:47:00"        │
│ → UPDATE a_f_break = "00:02:00"        │
└─────────────────────────────────────────┘

1:00 PM - SALE A ALMUERZO
┌─────────────────────────────────────────┐
│ POST /api/firmas/procesar               │
│ {                                       │
│   "ci": "1700000001",                   │
│   "hora_actual": "13:00:00"             │
│ }                                       │
│ → UPDATE h_i_almuerzo = "13:00:00"     │
└─────────────────────────────────────────┘

2:05 PM - REGRESA DE ALMUERZO
┌─────────────────────────────────────────┐
│ POST /api/firmas/procesar               │
│ {                                       │
│   "ci": "1700000001",                   │
│   "hora_actual": "14:05:00"             │
│ }                                       │
│ → UPDATE h_f_almuerzo = "14:05:00"     │
│ → UPDATE a_f_almuerzo = "00:05:00"     │
└─────────────────────────────────────────┘

5:30 PM - TERMINA JORNADA
┌─────────────────────────────────────────┐
│ POST /api/firmas/procesar               │
│ {                                       │
│   "ci": "1700000001",                   │
│   "hora_actual": "17:30:00"             │
│ }                                       │
│ → UPDATE h_f_jornada = "17:30:00"      │
└─────────────────────────────────────────┘
```

---

## 📊 CIs de Ejemplo (Basado en tu Base de Datos)

Puedes usar estos CIs para tus pruebas:

| CI | Nombres | Apellidos | Turno | Break | Almuerzo |
|----|---------|-----------|-------|-------|----------|
| `1700000001` | EMPLEADO DEMO | EMPLEADO DEMO | 1 | 1 | 1 |
| `1700000001` | EMPLEADO DEMO | EMPLEADO DEMO | 3 | 8 | 18 |
| `1700000001` | EMPLEADO DEMO | EMPLEADO DEMO | 1 | 5 | 9 |
| `1700000001` | EMPLEADO DEMO | EMPLEADO DEMO | 2 | 7 | 15 |
| `1700000005` | EMPLEADO DEMO | EMPLEADO DEMO | 1 | 1 | 1 |

**Recomendado para pruebas:** `1700000001` (EMPLEADO DEMO)

---

## ✅ Resumen Rápido de Endpoints

| Endpoint | Método | Acción SQL | Tabla Afectada | Uso Principal |
|----------|--------|------------|----------------|---------------|
| `/health` | GET | SELECT | - | Verificar estado |
| `/firmas` | GET | SELECT | firma | Ver todas las firmas |
| `/firmas/hoy` | GET | SELECT | firma | Firmas del día |
| `/firmas/{id}` | GET | SELECT | firma | Ver una firma |
| `/firmas/empleado/{ci}` | GET | SELECT | firma | Historial empleado |
| `/firmas/empleado/{ci}/fecha/{fecha}` | GET | SELECT | firma | Firma específica |
| `/firmas/fecha/{fecha}` | GET | SELECT | firma | Firmas de un día |
| `/firmas/incompletas` | GET | SELECT | firma | Sin terminar |
| `/firmas/iniciar-jornada` | POST | **INSERT** | **firma** | Registro manual |
| `/firmas/procesar` ⭐ | POST | **INSERT/UPDATE** | **firma** | **Registro automático** |
| `/firmas/{id}` | PUT | **UPDATE** | **firma** | Corrección manual |
| `/firmas/autocompletar` | PUT | **UPDATE** | **firma** | Completar pendientes |
| `/firmas/{id}` | DELETE | **DELETE** | **firma** | Eliminar registro |

---

## 🚨 Errores Comunes y Soluciones

### Error: "Empleado no encontrado"
```json
{
    "success": false,
    "error": "Empleado con CI 12345 no encontrado"
}
```
**Solución:** Usa un CI que existe en tu tabla `empleado`.

### Error: "Ya existe un registro de firma"
```json
{
    "success": false,
    "error": "Ya existe un registro de firma para este empleado en esta fecha"
}
```
**Solución:** 
- Usa `/firmas/procesar` en lugar de `/firmas/iniciar-jornada`
- O elimina la firma existente primero
- O usa otra fecha

### Error: "La jornada ya ha sido completada"
```json
{
    "success": false,
    "error": "La jornada ya ha sido completada"
}
```
**Solución:** Todos los campos ya están llenos. No se puede registrar más eventos para ese día.

### Error: "El empleado no tiene un turno asignado"
```json
{
    "success": false,
    "error": "El empleado no tiene un turno asignado"
}
```
**Solución:** Asignar un turno al empleado en la tabla `empleado`:
```sql
UPDATE empleado SET id_t = 2 WHERE ci = '1700000001';
```

---

## 💡 Tips y Mejores Prácticas

### Para Desarrollo:
1. Usa siempre el endpoint **`/firmas/procesar`** - es el más inteligente
2. Prueba con un solo empleado primero
3. Verifica los datos en pgAdmin4 después de cada operación
4. Usa el Health Check antes de cualquier prueba

### Para Producción:
1. Implementa autenticación (JWT, OAuth)
2. Configura rate limiting
3. Programa `/firmas/autocompletar` como cron job nocturno
4. Haz backups regulares de la tabla `firma`
5. Monitorea firmas incompletas diariamente

### Para Testing:
1. Crea un empleado de prueba específico
2. Usa fechas pasadas para no contaminar datos actuales
3. Limpia datos de prueba después de testear
4. Documenta los CIs de prueba

---

## 📈 Casos de Uso Avanzados

### Reportes Mensuales:
```sql
-- Firmas completas del mes
SELECT 
    e.ci,
    e.nombres,
    e.apellidos,
    COUNT(*) as dias_trabajados,
    SUM(CASE WHEN f.a_i_jornada > '00:00:00' THEN 1 ELSE 0 END) as dias_con_atraso
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
WHERE EXTRACT(MONTH FROM f.fecha_firma) = 2
  AND EXTRACT(YEAR FROM f.fecha_firma) = 2026
GROUP BY e.ci, e.nombres, e.apellidos;
```

### Empleados con más atrasos:
```sql
SELECT 
    e.ci,
    e.nombres,
    e.apellidos,
    COUNT(*) as total_atrasos,
    AVG(EXTRACT(EPOCH FROM f.a_i_jornada)) as promedio_segundos
FROM firma f
INNER JOIN empleado e ON f.ci = e.ci
WHERE f.a_i_jornada > '00:00:00'
GROUP BY e.ci, e.nombres, e.apellidos
ORDER BY total_atrasos DESC
LIMIT 10;
```

---

¡Listo! Ahora tienes una guía completa de todos los endpoints de la API de Firmas. 🚀
