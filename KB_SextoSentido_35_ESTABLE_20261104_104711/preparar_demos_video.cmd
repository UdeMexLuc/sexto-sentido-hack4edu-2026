@echo off
setlocal EnableExtensions
pushd "%~dp0"
if errorlevel 1 (echo [FALLO] No se puede abrir la carpeta del proyecto.& exit /b 1)
python preparar_demos_video.py --ejecutar
set "RET=%errorlevel%"
popd
exit /b %RET%
