"""
AUDITORÍA DE PRODUCCIÓN - Revisar antes de subir
"""

issues = [
    ("[CRITICO]", "app.py:36", "debug=True en produccion", "Cambiar a debug=False"),

    ("[IMPORTANTE]", "app.py:16-18", "Inconsistencia BD path", "dist/pos.db vs instance/pos.db"),

    ("[IMPORTANTE]", "backup_routes.py:97, 104, 127", "Path traversal vulnerability", "Sanitizar filenames en backup operations"),

    ("[IMPORTANTE]", "routes.py:39, 73, 87", "Sin validacion de datos POST", "Agregar try-catch en add/update endpoints"),

    ("[IMPORTANTE]", "routes.py:155, 214", "Custom price sin validacion", "Validar que price >= 0"),

    ("[MODERADO]", "routes.py:145", "Acceso directo a dict sin validacion", "Validar item['id'] existe"),

    ("[MODERADO]", "models.py:43", "default=datetime.now deberia ser callable", "Cambiar a default=datetime.now"),

    ("[MODERADO]", "routes.py:140", "Sale.total_amount=0 luego se actualiza", "Puede causar race conditions"),
]

print("\n" + "="*70)
print("AUDITORIA PRE-PRODUCCION")
print("="*70)

for severity, location, problem, fix in issues:
    print(f"\n{severity}")
    print(f"  {location}")
    print(f"  Problema: {problem}")
    print(f"  Solucion: {fix}")

print("\n" + "="*70)
print(f"TOTAL: {len(issues)} issues encontrados")
print("="*70 + "\n")
