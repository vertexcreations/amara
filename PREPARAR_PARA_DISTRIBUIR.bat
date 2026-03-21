@echo off
setlocal enabledelayedexpansion
title Preparar AppPoS para Distribuir
color 0A

echo ===================================================
echo      PREPARANDO APPPOS PARA DISTRIBUCION v3.0
echo ===================================================
echo.

REM Detectar arquitectura
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set ARCH=x64
) else (
    set ARCH=x86
)

echo [INFO] Arquitectura detectada: %ARCH%
echo [INFO] Verificando archivos necesarios...
echo.

REM Verificar archivos criticos
if not exist "app.py" (
    color 0C
    echo [ERROR] No se encontro app.py. Ejecuta este script en la raiz del proyecto.
    pause
    exit /b 1
)

if not exist "models.py" (
    color 0C
    echo [ERROR] No se encontro models.py
    pause
    exit /b 1
)

if not exist "MiTiendaPoS.spec" (
    color 0C
    echo [ERROR] No se encontro MiTiendaPoS.spec
    pause
    exit /b 1
)

echo [OK] Archivos criticos encontrados
echo.
echo ===================================================
echo      PASO 1: BACKUP DE DATOS ACTUAL
echo ===================================================
echo.

REM Crear carpeta de backups si no existe
if not exist "dist\backups" mkdir dist\backups

if exist "dist\pos.db" (
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
    for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
    set TIMESTAMP=!mydate!_!mytime!

    echo Haciendo backup de BD actual...
    copy "dist\pos.db" "dist\backups\backup_!TIMESTAMP!.db" >nul
    echo [OK] Backup creado en dist\backups\backup_!TIMESTAMP!.db
) else (
    echo [INFO] Sin BD existente para respaldar
)

echo.
echo ===================================================
echo      PASO 2: LIMPIAR ENTORNO VIRTUAL Y CACHE
echo ===================================================
echo.

echo [1/5] Manteniendo .venv (requerido para PyInstaller)...
REM if exist ".venv" rmdir /s /q ".venv" 2>nul
REM if exist ".venv311" rmdir /s /q ".venv311" 2>nul

echo [2/5] Eliminando __pycache__...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul

echo [3/5] Eliminando .pytest_cache...
if exist ".pytest_cache" rmdir /s /q ".pytest_cache" 2>nul

echo [4/5] Limpiando carpeta build...
if exist "build" rmdir /s /q "build" 2>nul

echo [5/5] Limpiando archivos compilados (.pyc)...
for /r . %%f in (*.pyc) do del /q "%%f" 2>nul

echo [OK] Limpieza completada

echo.
echo ===================================================
echo      PASO 3: GENERAR EJECUTABLE
echo ===================================================
echo.

if not exist "dist\MiTiendaPoS.exe" (
    echo [INFO] Generando ejecutable con PyInstaller...
    echo Esto puede tomar 2-5 minutos...
    echo.
    call .venv_build\Scripts\pyinstaller.exe MiTiendaPoS.spec

    if errorlevel 1 (
        color 0C
        echo [ERROR] Fallo al generar ejecutable
        echo Asegurate que:
        echo - .venv_build\Scripts\pyinstaller.exe existe
        echo - Todas las dependencias estan instaladas
        pause
        exit /b 1
    )

    echo [OK] Ejecutable creado en dist\MiTiendaPoS.exe
) else (
    echo [OK] dist\MiTiendaPoS.exe ya existe
)

echo.
echo ===================================================
echo      PASO 4: LIMPIAR ARCHIVOS INNECESARIOS
echo ===================================================
echo.

echo Eliminando archivos temporales de distribucion...
if exist "instance\pos.db" (
    echo [INFO] Preservando BD en instance\ para el cliente
) else (
    echo [INFO] Sin BD en instance\ - se creara automaticamente
)

REM Limpiar archivos .db temporales en raiz
if exist "pos.db" del /q "pos.db" 2>nul
if exist "pos.db.safety" del /q "pos.db.safety" 2>nul

echo [OK] Limpieza completada

echo.
echo ===================================================
echo      RESUMEN FINAL
echo ===================================================
echo.
echo ARCHIVOS PARA DISTRIBUIR:
echo.
if exist "dist\MiTiendaPoS.exe" (
    for /f %%Z in ('dir /b "dist\MiTiendaPoS.exe" ^| find /c /v ""') do if not "%%Z"=="0" (
        echo [OK] dist\MiTiendaPoS.exe - LISTO
    )
) else (
    echo [ERROR] dist\MiTiendaPoS.exe - NO ENCONTRADO
)

if exist "dist\backups" (
    echo [OK] dist\backups\ - Respaldos de BD
)

if exist "templates" (
    echo [OK] templates\ - Plantillas HTML
)

if exist "static" (
    echo [OK] static\ - Archivos estaticos
)

echo.
echo INSTRUCCIONES PARA CLIENTE:
echo.
echo 1. Copiar carpeta "AppPoS_2" completa a destino
echo 2. Ejecutar: dist\MiTiendaPoS.exe
echo 3. Primera ejecucion creara BD en instance\pos.db
echo 4. Los respaldos anteriores estan en dist\backups\
echo.

color 0B
echo ===================================================
echo      LISTO PARA DISTRIBUCION
echo ===================================================
echo.
pause
