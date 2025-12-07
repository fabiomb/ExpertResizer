@echo off
setlocal enabledelayedexpansion

echo ============================================
echo ExpertResizer - Build Script
echo ============================================
echo.

REM Verificar que Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)

REM Verificar que las dependencias estan instaladas
echo [1/3] Verificando dependencias...
pip show Pillow >nul 2>&1
if errorlevel 1 (
    echo Pillow no esta instalado. Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no esta instalado. Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo [OK] Dependencias verificadas
echo.

REM Limpiar compilaciones anteriores
echo [2/3] Limpiando compilaciones anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ExpertResizer.spec del /q ExpertResizer.spec
echo [OK] Limpieza completada
echo.

REM Compilar con PyInstaller
echo [3/3] Compilando ejecutable...
echo Este proceso puede tardar varios minutos...
echo.

python -m PyInstaller --onefile ^
    --windowed ^
    --name=ExpertResizer ^
    --clean ^
    --noconfirm ^
    ExpertResizer.py

if errorlevel 1 (
    echo.
    echo ERROR: Fallo la compilacion
    pause
    exit /b 1
)

echo.
echo ============================================
echo     COMPILACION EXITOSA
echo ============================================
echo.
echo El ejecutable ha sido creado en:
echo     %CD%\dist\ExpertResizer.exe
echo.
echo Tamano del ejecutable:
for %%A in (dist\ExpertResizer.exe) do echo     %%~zA bytes
echo.
echo Puedes distribuir este archivo .exe sin necesidad
echo de instalar Python en otras computadoras.
echo ============================================
pause
