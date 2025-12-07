@echo off
echo ============================================
echo ExpertResizer - Instalador de Dependencias
echo ============================================
echo.
echo Instalando las dependencias necesarias...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias
    echo Asegurate de tener Python instalado y agregado al PATH
    pause
    exit /b 1
)

echo.
echo ============================================
echo Instalacion completada exitosamente!
echo.
echo Para ejecutar la aplicacion usa:
echo     python main.py
echo.
echo Para crear el ejecutable usa:
echo     build.bat
echo ============================================
pause
