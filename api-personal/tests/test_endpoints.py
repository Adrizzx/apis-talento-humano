import json
from urllib import request, parse
from urllib.error import HTTPError

BASE_URL = "http://localhost:5000/api"

def test_endpoint(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            with request.urlopen(url) as response:
                result = json.loads(response.read().decode())
                return True, result
        elif method == "POST":
            req = request.Request(url, 
                                data=json.dumps(data).encode(),
                                headers={'Content-Type': 'application/json'},
                                method='POST')
            with request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                return True, result
    except HTTPError as e:
        result = json.loads(e.read().decode())
        return False, result
    except Exception as e:
        return False, {"error": str(e)}

print("=" * 60)
print("PRUEBAS DE LA API REST - PERSONAL")
print("=" * 60)

# Test 1: Obtener todos los empleados
print("\n1. GET /api/personal - Obtener todos los empleados")
success, result = test_endpoint("GET", "/personal")
if success:
    print(f"   ✓ Éxito: {result['total']} empleados encontrados")
    if result['data']:
        emp = result['data'][0]
        print(f"   Ejemplo: {emp['nombres']} {emp['apellidos']}")
else:
    print(f"   ✗ Error: {result.get('error', 'Unknown')}")

# Test 2: Obtener empleado por CI (usando el primero de la lista)
if success and result['data']:
    ci = result['data'][0]['ci'].strip()
    print(f"\n2. GET /api/personal/{ci} - Obtener empleado por CI")
    success2, result2 = test_endpoint("GET", f"/personal/{ci}")
    if success2:
        emp = result2['data']
        print(f"   ✓ Éxito: {emp['nombres']} {emp['apellidos']}")
        print(f"   Área: {emp['id_a']}, Turno: {emp['id_t']}")
    else:
        print(f"   ✗ Error: {result2.get('error', 'Unknown')}")

# Test 3: Buscar empleados por nombre
print("\n3. GET /api/personal/search?nombres=ERIKA - Buscar por nombre")
success3, result3 = test_endpoint("GET", "/personal/search?nombres=ERIKA")
if success3:
    print(f"   ✓ Éxito: {result3['total']} empleados encontrados")
    for emp in result3['data']:
        print(f"   - {emp['nombres']} {emp['apellidos']}")
else:
    print(f"   ✗ Error: {result3.get('error', 'Unknown')}")

# Test 4: Endpoint raíz
print("\n4. GET / - Información de la API")
try:
    with request.urlopen("http://localhost:5000/") as response:
        result4 = json.loads(response.read().decode())
        print(f"   ✓ Éxito: {result4['message']}")
        print(f"   Versión: {result4['version']}")
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

print("\n" + "=" * 60)
print("TODAS LAS PRUEBAS COMPLETADAS")
print("=" * 60)
