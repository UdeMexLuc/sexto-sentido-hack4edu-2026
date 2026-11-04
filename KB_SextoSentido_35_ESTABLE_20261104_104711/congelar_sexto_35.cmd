@echo off
setlocal EnableExtensions
pushd "%~dp0"
if errorlevel 1 (echo [FALLO] No se puede abrir la carpeta del proyecto.& exit /b 1)
echo ================================================
echo  SEXTO SENTIDO 35 - CONGELAR VERSION ESTABLE
echo ================================================
echo Primero: repetir las 25 pruebas reales Python + DLV.
python verificar_sexto_35.py
if errorlevel 1 (
  echo [FALLO] Las pruebas no pasaron. NO se crea respaldo.
  popd
  exit /b 1
)
echo.
echo [OK] Pruebas: ahora se crea copia estable y ZIP.
python congelar_sexto_35.py
set "RET=%errorlevel%"
popd
exit /b %RET%
