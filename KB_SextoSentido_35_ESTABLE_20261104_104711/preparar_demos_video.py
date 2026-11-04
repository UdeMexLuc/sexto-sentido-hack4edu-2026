#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepare three isolated directories for video demonstration without histories."""
import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUTS = [
    "sexto_35.py", "textos_problemas.json", "Sexto_Sentido_12_actividades_revisadas.json",
    "problemas.dlv", "diagnostico.dlv", "tutor.dlv", "estructura_ia.dlv", "politica_ia.dlv",
    "reproducir_demo.py"
]
NAMES = {1:"01_verificar_calculo", 2:"02_aviso_no_verificado", 3:"03_adaptacion_historial"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ejecutar", action="store_true", help="Run all demos and verify DLV decisions")
    args = parser.parse_args()
    missing = [p for p in INPUTS if not (BASE / p).is_file()]
    if missing:
        raise RuntimeError("Faltan archivos: " + ", ".join(missing))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    root_base = BASE.parent / ("DEMOS_VIDEO_SS35_" + stamp)
    root = root_base
    i = 2
    while root.exists():
        root = Path(str(root_base) + "_" + str(i))
        i += 1
    root.mkdir()
    successes = []
    for n, folder in NAMES.items():
        dst = root / folder
        dst.mkdir()
        for name in INPUTS:
            shutil.copy2(BASE / name, dst / name)
        runner_name = "EJECUTAR_DEMO_{}.cmd".format(n)
        # Use an ordinary batch wrapper without touching other directories.
        cmd = ("@echo off\r\nsetlocal EnableExtensions\r\n" +
               "chcp 65001 >nul\r\n" +
               "set \"PYTHONIOENCODING=utf-8\"\r\n" +
               "set \"PYTHONUTF8=1\"\r\n" +
               "pushd \"%~dp0\"\r\n") + \
              "python reproducir_demo.py {}\r\nset \"RET=%errorlevel%\"\r\npopd\r\nexit /b %RET%\r\n".format(n)
        (dst / runner_name).write_bytes(cmd.encode("ascii"))
        print("[OK] Carpeta preparada:", dst)
        if args.ejecutar:
            p = subprocess.run([sys.executable, "reproducir_demo.py", str(n)],
                               cwd=str(dst), capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=140)
            if p.returncode:
                print("[FALLO] DEMO", n)
                print(p.stderr[-5500:] + p.stdout[-2500:])
                return 1
            successes.append(n)
            print("[OK] Demo {} reproducida con DLV; transcripcion generada.".format(n))
    if args.ejecutar and len(successes) == 3:
        (root / "RESULTADO_DEMOS.txt").write_text(
            "[OK] 3/3 demostraciones con Python + DLV verificadas.\n"
            "Historias generadas y descartadas en carpetas temporales.\n",
            encoding="utf-8")
    print("\nDirectorio de las demostraciones:", root)
    print("Cada demo incluye un CMD independiente y su propia carpeta de datos.")
    print("No se ha tocado el historial_sexto_35.dlv ni el historial_alumno.dlv.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        print("[FALLO]", exc)
        raise SystemExit(1)
