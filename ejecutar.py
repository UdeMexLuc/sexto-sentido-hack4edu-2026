#!/usr/bin/env python3
"""Lanzador multiplataforma para la entrega al jurado."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STABLE = ROOT / 'KB_SextoSentido_35_ESTABLE_20261104_104711'


def main():
    args = sys.argv[1:]
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    configured = env.get('DLV_BIN')
    if configured:
        binary = Path(configured).expanduser().resolve()
        if binary.name not in ('dlv', 'dlv.exe') or not binary.is_file():
            sys.exit('DLV_BIN debe apuntar a un archivo existente llamado dlv o dlv.exe.')
        env['PATH'] = str(binary.parent) + os.pathsep + env.get('PATH', '')
    else:
        local = ROOT / 'herramientas' / 'dlv' / 'bin'
        env['PATH'] = str(local) + os.pathsep + env.get('PATH', '')
    binary = shutil.which('dlv', path=env['PATH'])
    if '--listar' not in args:
        if not binary:
            sys.exit('Falta DLV clásico. Consulta docs/INSTALACION.md; no hay que instalar paquetes Python.')
        try:
            check = subprocess.run([binary, '-help'], capture_output=True, text=True,
                                   errors='replace', timeout=10, env=env)
        except (OSError, subprocess.TimeoutExpired) as error:
            sys.exit('No se pudo ejecutar DLV: ' + str(error))
        banner = check.stdout + check.stderr
        if 'DLV' not in banner:
            sys.exit('El comando dlv no parece ser el motor ASP esperado. Revisa docs/INSTALACION.md.')
    if args == ['--comprobar']:
        print('Python:', sys.version.split()[0])
        print('Ejecutable DLV:', binary)
        print(banner.splitlines()[0:5])
        return 0
    mode = args.pop(0) if args and args[0] in ('--interfaz', '--pruebas', '--pruebas-interfaz', '--demos', '--consola') else None
    if mode == '--pruebas':
        script = STABLE / 'verificar_sexto_35.py'
    elif mode == '--pruebas-interfaz':
        script = ROOT / 'interfaz' / 'verificar_interfaz.py'
    elif mode == '--demos':
        script = STABLE / 'preparar_demos_video.py'
        args.insert(0, '--ejecutar')
    elif mode == '--consola' or (mode is None and args):
        script = STABLE / 'sexto_35.py'
    else:
        script = ROOT / 'interfaz' / 'servidor.py'
    try:
        return subprocess.call([sys.executable, '-B', str(script), *args], env=env, cwd=ROOT)
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
