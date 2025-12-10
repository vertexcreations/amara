@echo off
title Mi Tienda PoS - Iniciando...
echo ===================================================
echo      Iniciando Sistema de Punto de Venta
echo ===================================================
echo.

:: 1. Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no fue encontrado en su sistema.
    echo.
    echo Por favor, siga estos pasos:
    echo 1. Vaya a https://www.python.org/downloads/
    echo 2. Descargue e instale la ultima version de Python.
    echo 3. IMPORTANTE: Al instalar, marque la casilla "Add Python to PATH".
    echo.
    echo Una vez instalado, vuelva a ejecutar este archivo.
    echo.
    pause
    exit /b
)

:: 2. Crear entorno virtual si no existe (para aislar las librerias)
if not exist "venv" (
    echo [INFO] Configurando el entorno por primera vez...
    python -m venv venv
)

:: 3. Activar entorno virtual
call venv\Scripts\activate

:: 4. Instalar librerias necesarias
echo [INFO] Verificando librerias necesarias...
pip install -r requirements.txt >nul

:: 5. Programar apertura del navegador (en 5 segundos)
echo [INFO] El navegador se abrira automaticamente en unos segundos...
start /min cmd /c "timeout /t 5 >nul && start http://127.0.0.1:5000"

:: 6. Ejecutar la aplicacion
echo.
echo [EXITO] El sistema esta funcionando.
echo NO CIERRE ESTA VENTANA mientras use el sistema.
echo Para salir, puede cerrar esta ventana.
echo.
python app.py
pause
