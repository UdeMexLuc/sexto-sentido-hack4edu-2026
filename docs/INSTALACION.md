# Instalación de la primera versión

## Dependencias

- Python **3.9 o posterior**; [descargas oficiales](https://www.python.org/downloads/).
- Un navegador moderno.
- **DLV clásico**, ejecutable `dlv` en macOS/Linux o `dlv.exe` en Windows.

No uses `brew install delve`: instala el depurador de Go, que también se llama `dlv`, y no es el motor ASP. Esta versión fue validada con DLV clásico **build BEN/Mar 29 2023**, macOS arm64. No se ha validado con DLV 2; no se promete compatibilidad intercambiable.

## Obtener y configurar DLV

El ejecutable no se redistribuye en este repositorio. Consulta al proveedor en [DLVSystem](https://www.dlvsystem.it/dlvsite/dlv/) y revisa sus condiciones de uso. Su [página actual de descargas](https://www.dlvsystem.it/dlvsite/dlv-download/) ofrece DLV 2, por lo que debes comprobar la versión que descargues.

Para reproducir el entorno probado en **Mac con Apple Silicon**, el archivo del proveedor es [dlv-mac-m1-2023-03.zip](https://www.dlvsystem.it/files/dlv-mac-m1-2023-03.zip). Descomprímelo y utiliza el ejecutable clásico llamado `dlv`. Para otras arquitecturas, obtén el ejecutable clásico correspondiente del proveedor; esta publicación no contiene un motor alternativo.

Puedes colocarlo en `herramientas/dlv/bin/` dentro del repositorio (crea la carpeta si no existe). Esa carpeta está excluida de Git. En macOS/Linux, concede permiso de ejecución al archivo:

```sh
chmod +x herramientas/dlv/bin/dlv
python3 ejecutar.py --comprobar
```

También puedes mantener DLV en otra ubicación y definir su ruta **absoluta**. El archivo debe llamarse `dlv` o `dlv.exe`:

```sh
export DLV_BIN="/ruta/absoluta/al/ejecutable/dlv"
python3 ejecutar.py --comprobar
```

En PowerShell de Windows:

```powershell
$env:DLV_BIN = 'C:\ruta\al\ejecutable\dlv.exe'
py -3 ejecutar.py --comprobar
py -3 ejecutar.py --interfaz
```

Si `dlv` ya está en el PATH del sistema, el lanzador también lo encuentra. No se necesitan `pip install` ni herramientas de Node.js.

## Iniciar la interfaz

```sh
python3 ejecutar.py --interfaz
```

Abre [http://127.0.0.1:8765](http://127.0.0.1:8765) y conserva la terminal abierta. Ctrl+C detiene el servidor.

Para otra dirección de puerto o datos de demostración separados:

```sh
python3 ejecutar.py --interfaz --port 8766 --datos /tmp/sexto_jurado
```

En Windows elige una carpeta temporal de tu equipo en lugar de `/tmp/sexto_jurado`.

## Comprobar la instalación

```sh
python3 ejecutar.py --pruebas
python3 ejecutar.py --pruebas-interfaz
```

Las pruebas deben terminar con **25 comprobaciones superadas** y **OK (6 tests)**, respectivamente. Si falla el motor, comprueba primero la versión y arquitectura del ejecutable con `--comprobar`.

Las instrucciones de Windows se proporcionan para el lanzador multiplataforma; la validación de esta entrega se realizó en macOS Apple Silicon, y no constituye una nueva validación independiente en Windows o Linux.
