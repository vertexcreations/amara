@echo off
REM Crear ejecutable con PyInstaller
REM Este script compila la aplicación Flask en un ejecutable Windows

echo.
echo ========================================
echo Compilando Vestra en archivo .exe
echo ========================================
echo.

REM Verificar si existe el virtual environment
if not exist ".venv" (
    echo Error: Virtual environment no encontrado
    echo Por favor ejecuta: python -m venv .venv
    pause
    exit /b 1
)

REM Activar virtual environment
call .venv\Scripts\activate.bat

REM Verificar si PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

REM Crear directorio dist si no existe
if not exist "dist" mkdir dist

REM Compilar con PyInstaller
echo.
echo Compilando aplicación...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "Vestra" ^
    --icon=icon.ico ^
    --add-data "templates:templates" ^
    --add-data "static:static" ^
    --hidden-import=flask ^
    --hidden-import=flask_sqlalchemy ^
    --hidden-import=werkzeug ^
    desktop_app.py

if errorlevel 1 (
    echo.
    echo Error durante la compilación
    pause
    exit /b 1
)

echo.
echo ========================================
echo Compilación completada exitosamente
echo.
echo Ejecutable creado en: dist\Vestra.exe
echo ========================================
echo.

pause
