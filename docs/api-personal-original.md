# API REST - Sistema de Personal

API REST desarrollada con Flask y PostgreSQL para la gestión de empleados.

## ✅ Estado del Proyecto

- ✅ Conexión a PostgreSQL establecida
- ✅ Base de datos: `personal_postgres`
- ✅ 11 empleados cargados en la base de datos
- ✅ Todos los endpoints funcionando
- ✅ Servidor corriendo en: http://localhost:5000

## 🚀 Inicio Rápido

### Iniciar el servidor
```bash
python run.py
```

El servidor estará disponible en:
- http://localhost:5000
- http://localhost:5000

## 📡 Endpoints Disponibles

### 1. Información de la API
```
GET /
```
Respuesta:
```json
{
  "message": "API de Personal - Sistema de Gestión de Empleados",
  "version": "1.0",
  "endpoints": { ... }
}
```

### 2. Listar todos los empleados
```
GET /api/personal
```
Respuesta:
```json
{
  "success": true,
  "data": [...],
  "total": 11
}
```

### 3. Obtener empleado por CI
```
GET /api/personal/<ci>
```
Ejemplo: `GET /api/personal/1700000008`

### 4. Buscar empleados
```
GET /api/personal/search?nombres=<nombre>&apellidos=<apellido>
```
Ejemplo: `GET /api/personal/search?nombres=ERIKA`

### 5. Crear empleado
```
POST /api/personal
Content-Type: application/json

{
  "ci": "1700000001",
  "id_a": 1,
  "id_t": 3,
  "nombres": "JUAN",
  "apellidos": "PEREZ",
  "direccion": "QUITO",
  "telefonos": "1700000001",
  "correo": "juan@example.com",
  "fecha_nacimiento": "1990-01-01",
  "fecha_ingreso": "2024-01-01",
  "fecha_contrato": "2024-01-01",
  "salario": 500.00
}
```

### 6. Actualizar empleado
```
PUT /api/personal/<ci>
Content-Type: application/json

{
  "id_a": 1,
  "id_t": 3,
  "nombres": "JUAN CARLOS",
  "apellidos": "PEREZ LOPEZ",
  ...
}
```

### 7. Eliminar empleado
```
DELETE /api/personal/<ci>
```

## 🗃️ Configuración de Base de Datos

Archivo `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=personal_postgres
DB_USER=postgres
DB_PASSWORD=adrizzx
PORT=5000
```

## 📦 Dependencias

- Flask 3.0.0
- flask-cors 4.0.0
- psycopg2-binary >= 2.9.9
- python-dotenv 1.0.0

## 🧪 Pruebas

Ejecutar script de pruebas:
```bash
python test_endpoints.py
```

## 📊 Empleados en la Base de Datos

Actualmente hay **11 empleados** registrados:
1. EMPLEADO DEMO EMPLEADO DEMO
2. EMPLEADO DEMO EMPLEADO DEMO
3. EMPLEADO DEMO EMPLEADO DEMO
4. Y más...

## 🔧 Estructura del Proyecto

```
api-personal/
├── app/
│   ├── __init__.py          # Configuración de Flask
│   ├── database.py          # Conexión a PostgreSQL
│   ├── models.py            # Modelos (Personal)
│   └── routes.py            # Endpoints de la API
├── config.py                # Configuración general
├── run.py                   # Archivo principal
├── requirements.txt         # Dependencias
├── .env                     # Variables de entorno
└── test_endpoints.py        # Script de pruebas
```

## 📝 Notas

- La API está configurada para desarrollo (debug=True)
- CORS está habilitado para permitir peticiones desde cualquier origen
- Las fechas se devuelven en formato ISO (YYYY-MM-DD)
- Los salarios se devuelven como números decimales
