@echo off
setlocal EnableExtensions
chcp 65001 >nul
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
pushd "%~dp0"
if errorlevel 1 (echo [FALLO] No se puede abrir la carpeta del proyecto.& exit /b 1)
python preparar_demos_video.py --ejecutar
set "RET=%errorlevel%"
popd
exit /b %RET%
