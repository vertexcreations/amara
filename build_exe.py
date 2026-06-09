#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Verificar archivos necesarios
print("Verificando archivos necesarios...")
for item in [".venv", "desktop_app.py", "templates", "static", "icon.ico"]:
    if not os.path.exists(item):
        print(f"ERROR: {item} no encontrado")
        sys.exit(1)

# Limpiar compilaciones anteriores
print("Limpiando compilaciones anteriores...")
for item in ["build", "dist", "Vestra.spec", "amara.spec"]:
    if os.path.exists(item):
        if os.path.isdir(item):
            shutil.rmtree(item, ignore_errors=True)
        else:
            os.remove(item)

# Activar venv y compilar
print("Compilando amara.exe...")
activate_script = r".venv\Scripts\activate.bat"
compile_cmd = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--name", "amara",
    "--icon=icon.ico",
    "--add-data", r"templates;templates",
    "--add-data", r"static;static",
    "--hidden-import=flask",
    "--hidden-import=flask_sqlalchemy",
    "--hidden-import=flask_cors",
    "--hidden-import=werkzeug",
    "--hidden-import=sqlalchemy",
    "--hidden-import=jinja2",
    "--hidden-import=pywebview",
    "--collect-all=pywebview",
    "desktop_app.py"
]

# Ejecutar con venv activado
result = subprocess.run(
    f'"{activate_script}" && {" ".join(compile_cmd)}',
    shell=True
)

if result.returncode == 0:
    print("\n✓ Compilación completada exitosamente")
    print(f"✓ Ejecutable creado en: dist/amara.exe")
    exe_path = r"dist\amara.exe"
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✓ Tamaño: {size_mb:.2f} MB")
else:
    print("\n✗ Error durante la compilación")
    sys.exit(1)
