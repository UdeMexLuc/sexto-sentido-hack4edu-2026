#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Immutable-ish source snapshot with SHA256 manifest, no personal histories.

This script must be called only after the local integration suite succeeds.
Creates a fresh sibling folder and its ZIP; never overwrites existing backups.
"""
import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
FILES = [
    "sexto_35.py", "textos_problemas.json", "Sexto_Sentido_12_actividades_revisadas.json",
    "problemas.dlv", "diagnostico.dlv", "tutor.dlv", "estructura_ia.dlv", "politica_ia.dlv",
    "verificar_sexto_35.py", "probar_sexto_35.cmd",
    "congelar_sexto_35.py", "congelar_sexto_35.cmd",
    "preparar_demos_video.py", "preparar_demos_video.cmd", "reproducir_demo.py",
    "GUIA_DEMOS_VIDEO.md", "GUION_VIDEO_10MIN_EN.md", "MATRIZ_RETO07.md",
    "LEEME_PASO_FINAL.txt"
]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(128*1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    missing = [name for name in FILES if not (BASE / name).is_file()]
    if missing:
        raise RuntimeError("Faltan archivos del prototipo: " + ", ".join(missing))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = "KB_SextoSentido_35_ESTABLE_" + stamp
    dst = BASE.parent / name
    k = 2
    while dst.exists() or dst.with_suffix(".zip").exists():
        dst = BASE.parent / (name + "_" + str(k))
        k += 1
    dst.mkdir()
    try:
        entries = {}
        for name in FILES:
            shutil.copy2(BASE / name, dst / name)
            source_hash, copy_hash = sha256(BASE / name), sha256(dst / name)
            if source_hash != copy_hash:
                raise RuntimeError("La copia no coincide en " + name)
            entries[name] = source_hash
        manifest = "# SHA256 | Sexto Sentido 35 | respaldado despues de 25 tests\n" + \
                   "\n".join(entries[n] + "  " + n for n in FILES) + "\n"
        (dst / "MANIFIESTO_SHA256.txt").write_text(manifest, encoding="utf-8")
        status = {
            "version": "sexto_35_v1_verificada_por_usuario_25_de_25",
            "fecha_respaldo_local": datetime.now().isoformat(timespec="seconds"),
            "pruebas_esperadas": "verificar_sexto_35.py: 25/25 antes del respaldo",
            "documentos_y_codigo": len(FILES),
            "archivos_incluidos": FILES,
            "excluidos": ["historial_alumno.dlv", "historial_sexto_35.dlv",
                          "reflexiones_alumno.jsonl", "reflexiones_sexto_35.jsonl"],
            "nota": "Version tecnica reproducible; la eficacia educativa requiere evaluacion humana"
        }
        (dst / "ESTADO_VERSION.json").write_text(
            json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        zip_path = dst.with_suffix(".zip")
        with zipfile.ZipFile(zip_path, "x", compression=zipfile.ZIP_DEFLATED) as z:
            for f in sorted(dst.iterdir()):
                if f.is_file():
                    z.write(f, arcname=dst.name + "/" + f.name)
        with zipfile.ZipFile(zip_path) as z:
            bad = z.testzip()
            if bad:
                raise RuntimeError("ZIP corrupto: " + bad)
        print("[OK] Respaldo estable:", dst)
        print("[OK] ZIP:", zip_path)
        print("[OK] Copias verificadas SHA256 de {} archivos.".format(len(FILES)))
        print("[OK] Historias y reflexiones personales excluidas.")
        return 0
    except Exception:
        print("[AVISO] Hubo un fallo; revise el directorio parcial:", dst, file=sys.stderr)
        raise


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, zipfile.BadZipFile) as exc:
        print("[FALLO]", exc, file=sys.stderr)
        raise SystemExit(1)
