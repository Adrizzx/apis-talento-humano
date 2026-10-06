"""
Script simple para verificar que el servidor Flask está respondiendo
Sin usar urllib - usa sockets directo
"""
import socket
import json

def test_http_get(host='localhost', port=5000, path='/'):
    """Hace una petición HTTP GET simple usando sockets"""
    try:
        # Crear socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Conectar
        sock.connect((host, port))
        
        # Enviar petición HTTP
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())
        
        # Recibir respuesta
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        sock.close()
        
        # Separar headers y body
        response_str = response.decode('utf-8', errors='ignore')
        parts = response_str.split('\r\n\r\n', 1)
        
        if len(parts) == 2:
            headers, body = parts
            return True, headers.split('\r\n')[0], body
        else:
            return True, "No headers", response_str
            
    except socket.timeout:
        return False, "TIMEOUT", "El servidor no respondió en 5 segundos"
    except ConnectionRefusedError:
        return False, "REFUSED", "El servidor rechazó la conexión. ¿Está corriendo?"
    except Exception as e:
        return False, "ERROR", str(e)

print("=" * 70)
print("VERIFICACIÓN DEL SERVIDOR FLASK")
print("=" * 70)

# Test 1: Endpoint raíz
print("\n1. Probando GET / ...")
success, status, body = test_http_get(path='/')
if success:
    print(f"   ✓ {status}")
    try:
        data = json.loads(body)
        print(f"   Mensaje: {data.get('message', 'N/A')}")
        print(f"   Versión: {data.get('version', 'N/A')}")
    except:
        print(f"   Body: {body[:200]}")
else:
    print(f"   ✗ {status}: {body}")

# Test 2: Listar empleados
print("\n2. Probando GET /api/personal ...")
success, status, body = test_http_get(path='/api/personal')
if success:
    print(f"   ✓ {status}")
    try:
        data = json.loads(body)
        if data.get('success'):
            print(f"   Total empleados: {data.get('total', 0)}")
            if data.get('data'):
                primer = data['data'][0]
                print(f"   Primer empleado: {primer.get('nombres', '')} {primer.get('apellidos', '')}")
        else:
            print(f"   Error: {data.get('error', 'Unknown')}")
    except Exception as e:
        print(f"   Error parseando JSON: {e}")
        print(f"   Body: {body[:200]}")
else:
    print(f"   ✗ {status}: {body}")

# Test 3: Buscar por nombre
print("\n3. Probando GET /api/personal/search?nombres=ERIKA ...")
success, status, body = test_http_get(path='/api/personal/search?nombres=ERIKA')
if success:
    print(f"   ✓ {status}")
    try:
        data = json.loads(body)
        if data.get('success'):
            print(f"   Encontrados: {data.get('total', 0)} empleados")
            for emp in data.get('data', [])[:3]:
                print(f"   - {emp.get('nombres', '')} {emp.get('apellidos', '')}")
    except Exception as e:
        print(f"   Error parseando JSON: {e}")
else:
    print(f"   ✗ {status}: {body}")

print("\n" + "=" * 70)
print("VERIFICACIÓN COMPLETADA")
print("=" * 70)
print("\nSi ves errores, verifica que:")
print("1. El servidor está corriendo: python run.py")
print("2. El puerto 5000 está disponible")
print("3. No hay firewall bloqueando")
