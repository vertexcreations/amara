@echo off
REM Script para preparar la aplicación para distribución
REM Limpia archivos temporales, compila ejecutable y prepara paquete de distribución

echo.
echo ========================================
echo Preparando Vestra para distribución
echo ========================================
echo.

REM Limpiar directorios temporales
echo Limpiando archivos temporales...
if exist "__pycache__" rmdir /s /q __pycache__
if exist "build" rmdir /s /q build
if exist "*.pyc" del /q *.pyc
if exist ".pytest_cache" rmdir /s /q .pytest_cache

REM Compilar ejecutable
echo.
echo Compilando ejecutable...
call crear_ejecutable.bat

if errorlevel 1 (
    echo Error durante la compilación
    pause
    exit /b 1
)

REM Crear carpeta de distribución
echo.
echo Preparando paquete de distribución...
if not exist "release" mkdir release
if exist "release\Vestra.exe" del /q release\Vestra.exe

REM Copiar ejecutable
if exist "dist\Vestra.exe" (
    copy dist\Vestra.exe release\Vestra.exe
    echo Ejecutable copiado a: release\Vestra.exe
) else (
    echo Error: No se encontró el ejecutable compilado
    pause
    exit /b 1
)

REM Crear archivo info
echo. > release\README.txt
echo Vestra - Sistema de Punto de Venta >> release\README.txt
echo. >> release\README.txt
echo Para ejecutar: Simplemente haz doble clic en Vestra.exe >> release\README.txt
echo. >> release\README.txt
echo Requisitos: Windows Vista o superior >> release\README.txt

echo.
echo ========================================
echo Distribución preparada exitosamente
echo Archivo listo en: release\Vestra.exe
echo ========================================
echo.

pause
