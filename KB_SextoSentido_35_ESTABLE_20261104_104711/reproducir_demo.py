#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three reproducible, isolated REAL Python+DLV demos for Sexto Sentido 35.

This script only records responses from the actual tutor. It does not emulate DLV.
It does not read or change any real student histories.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
CORE_FILES = [
    "sexto_35.py", "textos_problemas.json",
    "Sexto_Sentido_12_actividades_revisadas.json", "problemas.dlv",
    "diagnostico.dlv", "tutor.dlv", "estructura_ia.dlv", "politica_ia.dlv"
]

SCENARIOS = {
    1: {
        "name": "Verificar una respuesta de IA (calculo)",
        "steps": [{
            "pid": 25, "student": "demo_calculo", "answer": "1", "confidence": "90",
            "note": "Revisare las bases de los porcentajes.",
            "revision": "2", "confidence_final": "85",
            "reflection": "El descuento usa el precio aumentado, no el inicial.",
            "expected": ["accion=verificar_operaciones", "modo=contrastar_razones",
                         "accion=pedir_revision", "accion=resumir_revision"]
        }],
    },
    2: {
        "name": "No difundir informacion sin verificar (aviso escolar)",
        "steps": [{
            "pid": 29, "student": "demo_aviso", "answer": "1", "confidence": "95",
            "note": "No tengo confirmacion en el canal oficial.",
            "revision": "3", "confidence_final": "85",
            "reflection": "Verificare el aviso antes de compartirlo.",
            "expected": ["accion=detener_y_verificar", "modo=contrastar_razones",
                         "accion=pedir_revision", "accion=resumir_revision"]
        }],
    },
    3: {
        "name": "Transferencia a partir del historial (dos sesiones)",
        "steps": [
            {"pid": 24, "student": "demo_historial", "answer": "1", "confidence": "90",
             "note": "Una presentacion agradable no demuestra eficacia.",
             "revision": "3", "confidence_final": "80",
             "reflection": "Necesito evidencia sobre resultados.",
             "expected": ["accion=distinguir_impresion_evidencia",
                          "accion=pedir_revision", "accion=resumir_revision"]},
            {"pid": 26, "student": "demo_historial", "answer": "2", "confidence": "90",
             "note": "Este caso se relaciona con la actividad anterior.",
             "revision": "1", "confidence_final": "85",
             "reflection": "Debo pedir resultados verificables y comparaciones.",
             "expected": ["accion=comparar_objetivo_anterior",
                          "motivo=antecedente_en_mismo_objetivo",
                          "modo=transferencia", "Actividad anterior relacionada: 24.",
                          "accion=pedir_revision", "accion=resumir_revision"]}
        ]
    }
}


def decorate(stdout, step):
    """Reinsert typed scripted inputs for readability; substantive output is unmodified."""
    entries = [
        ("Respuesta inicial (1-3, x=salir): ", step["answer"]),
        ("Confianza inicial (0-100, x=salir): ", step["confidence"]),
        ("Tu reflexion (opcional, sin datos personales): ", step["note"]),
        ("Respuesta revisada (1-3, x=salir): ", step["revision"]),
        ("Confianza revisada (0-100, x=salir): ", step["confidence_final"]),
        ("Tu reflexion final (opcional, sin datos personales): ", step["reflection"]),
    ]
    for prompt, value in entries:
        count = stdout.count(prompt)
        if count != 1:
            raise RuntimeError("Se esperaba una aparicion del prompt {!r}; encontradas {}".format(prompt, count))
        stdout = stdout.replace(prompt, prompt + value + "\n", 1)
    return stdout


def execute(n):
    if shutil.which("dlv") is None:
        raise RuntimeError("No se encontro DLV. Abre CMD donde 'dlv' funciona y ejecuta el .cmd.")
    for filename in CORE_FILES:
        if not (BASE / filename).is_file():
            raise FileNotFoundError("Falta " + filename + " en " + str(BASE))
    spec = SCENARIOS[n]
    lines = ["SEXTO SENTIDO 35 | DEMOSTRACION REPRODUCIBLE {}".format(n),
             spec["name"], "=" * 68,
             "EJECUCION REAL de sexto_35.py + DLV en una copia temporal.",
             "Los valores introducidos automaticamente se muestran despues de cada prompt.",
             "No hay respuestas ni decisiones pedagogicas inventadas en la transcripcion.",
             "No se ha leido ni modificado el historial real.", ""]
    with tempfile.TemporaryDirectory(prefix="SS35_EJEC_", dir=str(BASE)) as td:
        work = Path(td)
        for filename in CORE_FILES:
            shutil.copy2(BASE / filename, work / filename)
        for index, step in enumerate(spec["steps"], 1):
            inputs = "\n".join([step["answer"], step["confidence"], step["note"],
                                step["revision"], step["confidence_final"],
                                step["reflection"], ""])
            process = subprocess.run(
                [sys.executable, "sexto_35.py", "--alumno", step["student"],
                 "--problema", str(step["pid"]), "--una"],
                input=inputs, text=True, encoding="utf-8", errors="replace",
                capture_output=True, cwd=str(work), timeout=60)
            if process.returncode:
                raise RuntimeError("Ejecucion {} fallida (exit {}).\n{}\n{}".format(
                    index, process.returncode, process.stdout, process.stderr))
            for expected in step["expected"]:
                if expected not in process.stdout:
                    raise RuntimeError("En ejecucion {} falta {!r}.\n{}".format(
                        index, expected, process.stdout[-5500:]))
            annotated = decorate(process.stdout, step)
            lines += ["\n" + "-"*68,
                      "EJECUCION {} / {} : actividad {}".format(index, len(spec["steps"]), step["pid"]),
                      "Comando: python sexto_35.py --alumno {} --problema {} --una".format(
                          step["student"], step["pid"]), "-"*68, annotated,
                      "[OK] Acciones DLV verificadas contra los resultados esperados."]
            (BASE / "SALIDA_BRUTA_{}.txt".format(index)).write_text(
                process.stdout, encoding="utf-8")
        hist = work / "historial_sexto_35.dlv"
        if not hist.is_file():
            raise RuntimeError("No se genero historial en el sandbox.")
        facts = [ln for ln in hist.read_text(encoding="utf-8").splitlines()
                 if re.match(r"^(respuesta|evaluacion|confianza|observacion_error|intervencion_hecha)\(", ln)]
        lines += ["\nHECHOS REGISTRADOS (solo datos ficticios en sandbox):"]
        lines.extend(facts)
        lines += ["", "[OK] DEMO {} COMPLETADA Y VALIDADA".format(n)]
    transcript = "\n".join(lines) + "\n"
    (BASE / "TRANSCRIPCION_DEMO_{}.txt".format(n)).write_text(transcript, encoding="utf-8")
    try:
        print(transcript)
    except UnicodeError:
        print(transcript.encode("ascii", "replace").decode("ascii"))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reproduce una demo con datos ficticios y DLV real.")
    parser.add_argument("numero", type=int, choices=sorted(SCENARIOS))
    args = parser.parse_args()
    try:
        raise SystemExit(execute(args.numero))
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print("[FALLO]", exc, file=sys.stderr)
        raise SystemExit(1)
