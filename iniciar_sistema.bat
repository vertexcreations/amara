@echo off
REM Iniciar el sistema en desarrollo

echo.
echo ========================================
echo Iniciando Vestra - Sistema de POS
echo ========================================
echo.

REM Verificar si existe el virtual environment
if not exist ".venv" (
    echo Creando virtual environment...
    python -m venv .venv
)

REM Activar virtual environment
call .venv\Scripts\activate.bat

REM Instalar/actualizar dependencias
pip install -r requirements.txt

REM Iniciar aplicación
echo.
echo Iniciando aplicación...
python app.py

pause
