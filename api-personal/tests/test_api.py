from app.models import Personal

# Probar obtener todos los empleados
empleados = Personal.get_all()
print(f'✓ Total de empleados: {len(empleados)}')

if empleados:
    print(f'\nPrimeros 3 empleados:')
    for i, emp in enumerate(empleados[:3], 1):
        print(f'{i}. {emp["nombres"]} {emp["apellidos"]} (CI: {emp["ci"]})')
