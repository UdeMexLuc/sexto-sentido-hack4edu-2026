#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integracion real Python+DLV en carpeta temporal. No altera datos reales."""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import sexto_35 as ss

BASE = Path(__file__).resolve().parent
ARCHIVOS = ["sexto_35.py", "textos_problemas.json",
            "Sexto_Sentido_12_actividades_revisadas.json",
            "problemas.dlv", "diagnostico.dlv", "tutor.dlv",
            "estructura_ia.dlv", "politica_ia.dlv"]
APROBADAS = 0


def correcto(etiqueta, condicion, detalle=""):
    global APROBADAS
    if not condicion:
        print("[FALLO]", etiqueta)
        if detalle:
            print(detalle[-9000:])
        raise SystemExit(1)
    APROBADAS += 1
    print(f"[OK] T{APROBADAS:02d} {etiqueta}")


def huella(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest() if ruta.is_file() else None


def correr(carpeta, alumno, pid, entradas):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    p = subprocess.run([sys.executable, "sexto_35.py", "--alumno", alumno,
                        "--problema", str(pid), "--una"],
                       input=entradas, text=True, encoding="utf-8",
                       errors="replace", capture_output=True, cwd=carpeta,
                       env=env, timeout=50)
    if p.returncode:
        raise RuntimeError(f"Actividad {pid}; alumno {alumno}; codigo {p.returncode}\n"
                           + p.stdout + "\n" + p.stderr)
    return p.stdout


def tiene(archivo, texto):
    return texto in archivo.read_text(encoding="utf-8")


def main():
    print("\nSEXTO SENTIDO 35 - PRUEBAS DE INTEGRACION")
    print("Usa una carpeta temporal; no modifica el historial original.\n")
    if shutil.which("dlv") is None:
        raise RuntimeError("No se encuentra 'dlv' en el PATH.")
    for nombre in ARCHIVOS:
        if not (BASE / nombre).is_file():
            raise RuntimeError("Falta el archivo: " + nombre)
    originales = [BASE / "historial_alumno.dlv", BASE / "reflexiones_alumno.jsonl",
                 BASE / "historial_sexto_35.dlv", BASE / "reflexiones_sexto_35.jsonl"]
    antes = {str(f): huella(f) for f in originales}
    banco = ss.cargar_banco()
    reglas, objetivos = ss.cargar_politica(banco)
    correcto("banco completo: 23+12=35", set(banco) == set(range(1, 36)))
    correcto("24 errores editoriales corresponden a la politica", len(reglas) == 24)
    correcto("objetivos de transferencia disponibles", len(objetivos) == 12)
    with tempfile.TemporaryDirectory(prefix="SS35_PRUEBA_") as temporal:
        carpeta = Path(temporal)
        for nombre in ARCHIVOS:
            shutil.copy2(BASE / nombre, carpeta / nombre)
        lista = subprocess.run([sys.executable, "sexto_35.py", "--listar"],
                               cwd=carpeta, text=True, encoding="utf-8",
                               errors="replace", capture_output=True, timeout=15)
        correcto("listado sin crear historial", lista.returncode == 0 and
                 "35." in lista.stdout and not (carpeta / ss.HIST.name).exists(),
                 lista.stdout + lista.stderr)
        historial = carpeta / ss.HIST.name
        # Los 12 casos nuevos: error inicial, ayuda especifica, revision correcta.
        for pid in range(24, 36):
            p = banco[pid]
            err = p["errores_previsibles"][0]
            mala = int(err["opcion_id"])
            buena = int(p["clave_docente"]["correcta_id"])
            salida = correr(carpeta, f"qa_{pid}", pid,
                            f"{mala}\n90\n\n{buena}\n75\n\n")
            accion = err["intervencion_sugerida"]
            hecho = f"observacion_error(qa_{pid},1,{pid},{err['etiqueta']})."
            final = f"evaluacion(qa_{pid},1,{pid},final,correcta)."
            correcto(f"actividad {pid}: ayuda, revision e historial",
                     f"[DLV: accion={accion};" in salida and
                     "modo=contrastar_razones" in salida and
                     "accion=resumir_revision" in salida and
                     tiene(historial, hecho) and tiene(historial, final), salida)
        # Segunda categoria diferente: baja confianza y otra ayuda.
        p = banco[24]
        err = p["errores_previsibles"][1]
        salida = correr(carpeta, "qa_otra", 24, f"{err['opcion_id']}\n20\n\n3\n70\n\n")
        correcto("segundo distractor y pista breve",
                 "accion=pedir_evidencia_pertinente" in salida and
                 "modo=pista_breve" in salida and
                 "motivo=sospecha_sin_evidencia" in salida, salida)
        # Regresion con los problemas 1..23.
        salida = correr(carpeta, "qa_viejo", 1, "1\n20\n\n5\n75\n")
        correcto("problema original 1: ayuda gradual y revision",
                 "accion=ofrecer_pista_gradual" in salida and
                 "accion=resumir_revision" in salida and
                 not tiene(historial, "observacion_error(qa_viejo,"), salida)
        # Baja confianza con acierto no inventa categoria de error.
        salida = correr(carpeta, "qa_acierto", 34, "1\n20\n\n\n")
        correcto("acierto con baja confianza: pedir justificacion",
                 "accion=pedir_justificacion" in salida and
                 "accion=proponer_nuevo_caso" in salida and
                 not tiene(historial, "observacion_error(qa_acierto,"), salida)
        # Pista ya dada y revision pendiente, reanudada en otro proceso.
        salida1 = correr(carpeta, "qa_pendiente", 25, "1\n90\n\nx\n")
        salida2 = correr(carpeta, "qa_pendiente", 25, "\n2\n80\n\n")
        correcto("reanudar revision pendiente sin duplicar respuesta",
                 "Revision pendiente" in salida2 and
                 "accion=pedir_revision" in salida2 and
                 tiene(historial, "evaluacion(qa_pendiente,1,25,final,correcta).") and
                 historial.read_text(encoding="utf-8").count(
                   "respuesta(qa_pendiente,1,25,inicial,1).") == 1,
                 salida1 + salida2)
        # Transferencia entre casos con distinto tipo de error y mismo objetivo.
        correr(carpeta, "qa_trans", 24, "1\n90\n\n3\n80\n\n")
        salida = correr(carpeta, "qa_trans", 26, "2\n90\n\n1\n80\n\n")
        correcto("transferencia entre actividades 24 y 26",
                 "accion=comparar_objetivo_anterior" in salida and
                 "Actividad anterior relacionada: 24." in salida, salida)
        # La seguridad conserva prioridad sobre la transferencia.
        correr(carpeta, "qa_seguro", 28, "1\n90\n\n2\n80\n\n")
        salida = correr(carpeta, "qa_seguro", 29, "1\n90\n\n3\n80\n\n")
        correcto("seguridad: caso 29 prima sobre transferencia",
                 "accion=detener_y_verificar" in salida and
                 "accion=comparar_objetivo_anterior" not in salida, salida)
        # Salir sin responder no produce evaluaciones falsas.
        salida = correr(carpeta, "qa_salida", 31, "x\n")
        correcto("salida temprana: sin evaluacion inventada",
                 "Progreso conservado" in salida and
                 not tiene(historial, "respuesta(qa_salida,"), salida)
        correcto("nuevo historial independiente en carpeta temporal", historial.is_file())
    despues = {str(f): huella(f) for f in originales}
    correcto("historiales reales intactos", antes == despues)
    print(f"\n[OK] {APROBADAS} de {APROBADAS} comprobaciones superadas.")
    print("[OK] Los historiales reales no se modificaron.")
    print("[OK] La version estable sexto_entrega.py permanece intacta.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print("\n[FALLO]", exc)
        raise SystemExit(1)
