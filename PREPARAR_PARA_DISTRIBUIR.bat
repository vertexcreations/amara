@echo off
title Preparar para Distribuir
echo ===================================================
echo      Limpiando archivos para distribucion
echo ===================================================
echo.
echo Este script borrara el entorno virtual y archivos temporales
echo para que la carpeta sea mas liviana y facil de copiar.
echo.
echo [ADVERTENCIA] Esto borrara la carpeta 'venv'.
echo La proxima vez que inicies el sistema, se volvera a crear.
echo.
pause

echo.
echo 1. Borrando entorno virtual (venv)...
if exist venv rmdir /s /q venv

echo 2. Borrando caches de Python...
if exist __pycache__ rmdir /s /q __pycache__
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist instance\pos.db (
    echo.
    echo [NOTA] Se encontro una base de datos existente en 'instance\pos.db'.
    echo No se borrara para no perder datos.
    echo Si quieres una instalacion limpia, borra la carpeta 'instance' manualmente.
)

echo.
echo ===================================================
echo      LISTO PARA COPIAR
echo ===================================================
echo Ahora puedes copiar toda la carpeta "AppPoS" a la otra computadora.
echo.
pause
