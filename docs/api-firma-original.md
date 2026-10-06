# 📝 API de Firmas - Sistema de Asistencia

API REST desarrollada con Flask y PostgreSQL para gestionar el sistema de firmas y asistencia de empleados.

## 🚀 Características

- ✅ Registro automático de firmas (inicio jornada, breaks, almuerzo, fin jornada)
- ✅ Cálculo automático de atrasos
- ✅ Verificación en cascada de NULL
- ✅ Autocompletado de firmas incompletas
- ✅ Validaciones completas de datos
- ✅ Manejo de errores robusto
- ✅ Documentación completa
- ✅ Compatible con base de datos existente

## 📁 Estructura del Proyecto

```
api_firma/
├── app/
│   ├── __init__.py          # Factory de la aplicación
│   ├── config.py            # Configuración
│   ├── models/              # Modelos de base de datos
│   │   ├── __init__.py
│   │   ├── firma.py
│   │   ├── empleado.py
│   │   ├── turno.py
│   │   ├── receso.py
│   │   └── area.py
│   ├── routes/              # Rutas y endpoints
│   │   ├── __init__.py
│   │   └── firmas.py
│   └── schemas/             # Schemas de serialización
│       ├── __init__.py
│       └── firma_schema.py
├── requirements.txt         # Dependencias
├── run.py                  # Punto de entrada
├── .env                    # Variables de entorno
├── .gitignore
├── README.md
└── GUIA_PRUEBAS_POSTMAN.md # Guía de pruebas
```

## 🔧 Instalación Rápida

### 1. Clonar o descargar el proyecto

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar .env

Editar `.env` con tus credenciales:

```env
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/personal
SECRET_KEY=tu_clave_secreta
FLASK_ENV=development
FLASK_DEBUG=1
```

### 4. Ejecutar

```bash
python run.py
```

La API estará en: `http://localhost:5000`

## 📚 Documentación

Ver [GUIA_PRUEBAS_POSTMAN.md](GUIA_PRUEBAS_POSTMAN.md) para:
- Guía completa de instalación
- Pruebas paso a paso en Postman
- Casos de uso completos
- Ejemplos de requests y responses

## 🎯 Endpoints Principales

### Consultas (GET)
- `GET /api/health` - Health check
- `GET /api/firmas` - Todas las firmas
- `GET /api/firmas/hoy` - Firmas de hoy
- `GET /api/firmas/empleado/<ci>` - Firmas de un empleado
- `GET /api/firmas/incompletas` - Firmas sin completar

### Operaciones (POST/PUT/DELETE)
- `POST /api/firmas/procesar` - **Procesar firma automática** ⭐
- `POST /api/firmas/iniciar-jornada` - Iniciar jornada manual
- `PUT /api/firmas/<id>` - Actualizar firma
- `PUT /api/firmas/autocompletar` - Autocompletar pendientes
- `DELETE /api/firmas/<id>` - Eliminar firma

## 💡 Uso Principal

El endpoint principal es `/api/firmas/procesar` que detecta automáticamente qué acción realizar:

```json
POST /api/firmas/procesar
{
    "ci": "1700000004",
    "hora_actual": "08:35:00"
}
```

La API detecta automáticamente:
1. ✅ Primera firma → Inicio de jornada
2. ✅ Segunda firma → Salida a break
3. ✅ Tercera firma → Regreso de break
4. ✅ Cuarta firma → Salida a almuerzo
5. ✅ Quinta firma → Regreso de almuerzo
6. ✅ Sexta firma → Fin de jornada

## 🔐 Base de Datos

La API usa la base de datos `personal` existente con estas tablas:
- `firma` - Registros de asistencia
- `empleado` - Información del personal
- `turno` - Horarios de trabajo
- `break` - Recesos (breaks y almuerzos)
- `area` - Áreas de trabajo

## 🛠️ Tecnologías

- **Flask** 3.0.0 - Framework web
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de datos
- **Marshmallow** - Serialización
- **Flask-CORS** - CORS support

## 📝 Licencia

Proyecto privado - Sistema de Asistencia

## 👨‍💻 Autor

Desarrollado para el sistema de gestión de asistencia de personal.

## 📞 Soporte

Para problemas o preguntas, revisar:
1. [GUIA_PRUEBAS_POSTMAN.md](GUIA_PRUEBAS_POSTMAN.md)
2. [API_Firma_Flask_PostgreSQL.md](API_Firma_Flask_PostgreSQL.md)
3. Logs de la aplicación
