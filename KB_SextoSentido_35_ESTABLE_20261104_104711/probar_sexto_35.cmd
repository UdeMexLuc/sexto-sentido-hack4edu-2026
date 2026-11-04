@echo off
setlocal EnableExtensions
pushd "%~dp0"
if errorlevel 1 (echo [FALLO] No se puede abrir la carpeta del CMD.& exit /b 1)
python verificar_sexto_35.py
set "RESULTADO=%errorlevel%"
popd
exit /b %RESULTADO%
