@echo off
title Creando Ejecutable (EXE)...
echo ===================================================
echo      Creando Aplicacion de Escritorio (.exe)
echo ===================================================
echo.

:: 1. Verificar entorno virtual
if not exist ".venv" (
    echo [INFO] Creando entorno virtual...
    python -m venv .venv
)
call .venv\Scripts\activate

:: 2. Instalar dependencias
echo [INFO] Instalando librerias necesarias (esto puede tardar)...
pip install -r requirements.txt >nul
pip install pyinstaller pywebview >nul

:: 3. Limpiar builds anteriores
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "MiTiendaPoS.spec" del "MiTiendaPoS.spec"

:: 4. Crear el ejecutable
echo.
echo [INFO] Generando el archivo .exe...
echo Por favor espere, esto puede tomar unos minutos.
echo.

pyinstaller --noconsole --onefile ^
    --name "MiTiendaPoS" ^
    --icon "static/icon.ico" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    desktop_app.py

:: Nota: Si no tienes favicon.ico, pyinstaller mostrará una advertencia pero continuará. 
:: Puedes quitar la linea --icon si falla.

echo.
echo ===================================================
echo      PROCESO TERMINADO
echo ===================================================
echo.
if exist "dist\MiTiendaPoS.exe" (
    echo [EXITO] El ejecutable se creo correctamente.
    echo Lo encontraras en la carpeta: dist\MiTiendaPoS.exe
    echo.
    echo Puedes copiar ese archivo unico a cualquier computadora
    echo y funcionara sin instalar nada mas.
) else (
    echo [ERROR] Algo salio mal. Revisa los mensajes de arriba.
)
echo.
pause

