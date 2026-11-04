#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sexto Sentido 35: tutor local de consola, Python + DLV clasico.

Preserva los archivos de la version estable: utiliza su propio historial
historial_sexto_35.dlv y sus propias reflexiones_sexto_35.jsonl.
La clave correcta y las categorias de error proceden del JSON editorial.
DLV selecciona acciones didacticas, no calcula respuestas correctas.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
HIST = BASE / "historial_sexto_35.dlv"
REFLEX = BASE / "reflexiones_sexto_35.jsonl"
JSON_ORIGINAL = BASE / "textos_problemas.json"
JSON_NUEVO = BASE / "Sexto_Sentido_12_actividades_revisadas.json"
DLV_INPUTS = ["problemas.dlv", "estructura_ia.dlv", HIST.name,
              "diagnostico.dlv", "tutor.dlv", "politica_ia.dlv"]
ID_ALUMNO = re.compile(r"[a-z][a-z0-9_]*\Z")
RESP = re.compile(r"respuesta\(([a-z][a-z0-9_]*),(\d+),(\d+),(inicial|final),(\d+)\)\.\Z")
OBS = re.compile(r"observacion_error\(([a-z][a-z0-9_]*),(\d+),(\d+),([a-z][a-z0-9_]*)\)\.\Z")
CTX = re.compile(r"contexto_actual\([a-z][a-z0-9_]*,\d+,\d+\)\.\Z")
ATOM = re.compile(r"\b(accion|motivo|modo_ayuda)\(\s*([a-z][a-z0-9_]*)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([a-z][a-z0-9_]*)\s*\)")
ESTRATEGIA = re.compile(r"^estrategia_error\((\d+),([a-z][a-z0-9_]*),([a-z][a-z0-9_]*)\)\.$", re.M)
OBJETIVO = re.compile(r"^objetivo_formativo\((\d+),([a-z][a-z0-9_]*)\)\.$", re.M)

MENSAJES = {
    "presentar_pregunta": "Vamos con una nueva pregunta.",
    "comparar_caso_anterior": "Compara con un problema anterior de la misma familia.",
    "pedir_contraejemplo": "Busca un caso con premisas verdaderas y conclusion falsa.",
    "comparar_eventos": "Compara el evento simple con la conjuncion.",
    "distinguir_evidencia_y_conclusion": "Distingue los datos de la conclusion.",
    "aclarar_sistema_logico": "Revisa cual es el sistema logico supuesto.",
    "ofrecer_pista_gradual": "Examina una pista antes de revisar.",
    "examinar_razones": "Examina las razones de tu respuesta.",
    "pedir_revision": "Ahora puedes revisar tu respuesta.",
    "pedir_justificacion": "Tu respuesta es correcta. Explica brevemente por que.",
    "proponer_nuevo_caso": "Podemos continuar con otro problema.",
    "resumir_revision": "Tu revision corrigio la respuesta; revisemos la explicacion.",
    "reexaminar_error": "La revision aun no es correcta; revisemos la explicacion.",
    "continuar_tras_acierto": "Puedes continuar con otro problema.",
    "comparar_objetivo_anterior": "Compara la comprobacion necesaria con otra actividad anterior.",
    "distinguir_impresion_evidencia": "Distingue una buena impresion de los datos que la sostienen.",
    "pedir_evidencia_pertinente": "No conviertas una sospecha en un hecho: pide pruebas.",
    "verificar_operaciones": "Comprueba las operaciones, no el tono de la respuesta.",
    "formular_preguntas_de_verificacion": "Formula dos preguntas concretas sobre los resultados.",
    "separar_incentivos_de_resultados_de_aprendizaje": "Separa las cifras comerciales de la evidencia educativa.",
    "verificar_bases_porcentuales": "Identifica la base sobre la que se calcula cada porcentaje.",
    "comparar_procedimientos": "Compara los pasos del procedimiento, no solo el resultado.",
    "pedir_verificacion_fuente": "Comprueba si la referencia puede localizarse en una fuente fiable.",
    "distinguir_no_verificado_de_falso": "No verificable todavia no significa demostrado falso.",
    "detener_y_verificar": "No difundas el aviso antes de verificarlo.",
    "contrastar_con_fuente_primaria": "Busca una confirmacion independiente y oficial.",
    "examinar_criterios_pertinentes": "Evalua habilidades y criterios relevantes, no estereotipos.",
    "comparar_equidad_y_evidencia": "Revisa si tus criterios son justos y estan respaldados.",
    "revisar_privacidad_y_consentimiento": "Revisa que datos personales compartes y con que permiso.",
    "identificar_datos_personales_restantes": "Identifica datos que siguen permitiendo reconocer personas.",
    "verificar_procedencia_multimedia": "Verifica la procedencia del audio por otra via.",
    "distinguir_posibilidad_y_prueba": "Que algo pueda ser falso no prueba que lo sea.",
    "reconocer_limites_y_derivar": "No delegues una decision medica en una respuesta de IA.",
    "distinguir_consenso_de_evidencia": "Varias respuestas parecidas no sustituyen evidencia profesional.",
    "identificar_datos_faltantes": "Identifica que datos faltan para estimar el resultado.",
    "formular_estimacion_condicional": "Una estimacion puede ser util si explicita sus condiciones.",
    "distinguir_apoyo_y_sustitucion": "Distingue usar IA como apoyo de entregar trabajo ajeno.",
    "distinguir_transparencia_y_autoria": "Declarar el uso de IA no sustituye el trabajo propio.",
}
MOTIVOS = {
    "esperando_primera_respuesta": "Aun no hay respuesta inicial.",
    "historial_errores_misma_familia": "Hay respuestas iniciales equivocadas previas en esta familia.",
    "antecedente_en_mismo_objetivo": "Hay una respuesta inicial incorrecta en otra actividad relacionada.",
    "error_con_confianza_alta": "Respuesta incorrecta con confianza declarada alta.",
    "error_con_confianza_moderada_o_baja": "Respuesta incorrecta con confianza no alta.",
    "error_sin_intervencion_previa": "Aun no se habia ofrecido una ayuda.",
    "ya_recibio_ayuda": "Ya se ofrecio una intervencion en este caso.",
    "cambio_a_respuesta_correcta": "La revision corrigio la respuesta inicial.",
    "revision_no_resuelve_error": "La revision no corrigio la respuesta.",
    "acierto_inicial_con_duda": "La respuesta es correcta, pero se declaro poca confianza.",
    "acierto_y_puede_continuar": "La respuesta inicial es correcta.",
    "acierto_y_revision_completada": "El caso se ha completado.",
}
AYUDAS_ANTIGUAS = {
    "comparar_caso_anterior", "pedir_contraejemplo", "comparar_eventos",
    "distinguir_evidencia_y_conclusion", "aclarar_sistema_logico",
    "ofrecer_pista_gradual", "examinar_razones"
}


def leer_json(ruta):
    return json.loads(ruta.read_text(encoding="utf-8-sig"))


def cargar_banco():
    originales = leer_json(JSON_ORIGINAL)["problemas"]
    nuevos = leer_json(JSON_NUEVO)["actividades"]
    if len(originales) != 23 or len(nuevos) != 12:
        raise ValueError("Se requieren 23 problemas originales y 12 actividades nuevas.")
    banco = {}
    for p in originales:
        n = int(p["id"])
        if n in banco or n not in range(1, 24):
            raise ValueError("IDs invalidos en el banco original.")
        banco[n] = dict(p, nuevo=False)
    for p in nuevos:
        n = int(p["numero"])
        if n in banco or n not in range(24, 36) or p["id"] != f"SS-{n:03d}":
            raise ValueError("IDs invalidos en el banco nuevo.")
        banco[n] = dict(p, id=n, familia=p["area"],
                        pregunta="", pistas=[p["pista_gradual"]],
                        explicacion=p["explicacion_editorial"], nuevo=True)
    if set(banco) != set(range(1, 36)):
        raise ValueError("El banco no contiene exactamente los IDs 1..35.")
    for n, p in banco.items():
        opciones = {int(o["id"]) for o in p["opciones"]}
        permitidas = set(range(1, 4)) if p["nuevo"] else set(range(1, 6))
        clave = p["clave_docente"]
        if opciones != permitidas or int(clave["correcta_id"]) not in opciones:
            raise ValueError(f"Opciones o clave incorrectas en {n}.")
        if int(clave["intuitiva_s1_id"]) not in opciones - {int(clave["correcta_id"])}:
            raise ValueError(f"Error previsto invalido en {n}.")
        if p["nuevo"]:
            etiquetas = {int(e["opcion_id"]): e for e in p["errores_previsibles"]}
            if set(etiquetas) != opciones - {int(clave["correcta_id"])}:
                raise ValueError(f"Cada distractor debe tener una categoria en {n}.")
            p["errores_por_opcion"] = etiquetas
    return banco


def cargar_politica(banco):
    texto = (BASE / "politica_ia.dlv").read_text(encoding="utf-8")
    reglas = {(int(n), categoria): accion
              for n, categoria, accion in ESTRATEGIA.findall(texto)}
    objetivos = {int(n): nombre for n, nombre in OBJETIVO.findall(texto)}
    esperadas = {(n, e["etiqueta"]): e["intervencion_sugerida"]
                 for n, p in banco.items() if p["nuevo"]
                 for e in p["errores_previsibles"]}
    if reglas != esperadas or set(objetivos) != set(range(24, 36)):
        raise ValueError("La politica DLV no coincide con las 24 categorias del JSON.")
    estructura = (BASE / "estructura_ia.dlv").read_text(encoding="utf-8")
    actividades = {int(n) for n in re.findall(r"^actividad_ia\((\d+)\)\.$", estructura, re.M)}
    if actividades != set(range(24, 36)):
        raise ValueError("estructura_ia.dlv no define los casos 24..35.")
    sin_mensaje = {accion for accion in reglas.values() if accion not in MENSAJES}
    if sin_mensaje:
        raise ValueError("Faltan mensajes para algunas intervenciones: " + str(sin_mensaje))
    return reglas, objetivos


def clasificar(p, n):
    clave = p["clave_docente"]
    if n == int(clave["correcta_id"]):
        return "correcta"
    if n == int(clave["intuitiva_s1_id"]):
        return "intuitiva"
    return "otra"


def lineas_historial():
    if not HIST.exists():
        return []
    return HIST.read_text(encoding="utf-8-sig").splitlines()


def actualizar(hechos=(), contexto=None):
    lineas = lineas_historial()
    if contexto is not None:
        lineas = [l for l in lineas if not CTX.fullmatch(l.strip())]
    presentes = {linea.strip() for linea in lineas}
    for hecho in hechos:
        if hecho not in presentes:
            lineas.append(hecho)
            presentes.add(hecho)
    if contexto is not None:
        linea = "contexto_actual({},{},{}).".format(*contexto)
        if linea not in presentes:
            lineas.append(linea)
    tmp = HIST.with_name(HIST.name + ".tmp")
    tmp.write_text("\n".join(lineas).rstrip() + "\n", encoding="utf-8")
    os.replace(tmp, HIST)


def registros(alumno):
    resultado = []
    for linea in lineas_historial():
        m = RESP.fullmatch(linea.strip())
        if m and m[1] == alumno:
            resultado.append((int(m[2]), int(m[3]), m[4], int(m[5])))
    return resultado


def errores_previos(alumno):
    resultado = []
    for linea in lineas_historial():
        m = OBS.fullmatch(linea.strip())
        if m and m[1] == alumno:
            resultado.append((int(m[2]), int(m[3]), m[4]))
    return resultado


def guardar_respuesta(alumno, sesion, p, fase, opcion, confianza):
    clase = clasificar(p, opcion)
    hechos = [f"respuesta({alumno},{sesion},{p['id']},{fase},{opcion}).",
              f"evaluacion({alumno},{sesion},{p['id']},{fase},{clase}).",
              f"confianza({alumno},{sesion},{p['id']},{fase},{confianza})."]
    if fase == "inicial" and p["nuevo"] and clase != "correcta":
        etiqueta = p["errores_por_opcion"][opcion]["etiqueta"]
        hechos.append(f"observacion_error({alumno},{sesion},{p['id']},{etiqueta}).")
    actualizar(hechos)


def reflexionar(alumno, sesion, pid, etapa="antes_revision"):
    mensaje = "Tu reflexion final (opcional, sin datos personales): " if etapa == "final" else \
              "Tu reflexion (opcional, sin datos personales): "
    texto = input(mensaje).strip()
    if texto:
        with REFLEX.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"alumno": alumno, "sesion": sesion,
                                "problema": pid, "etapa": etapa,
                                "texto": texto}, ensure_ascii=False) + "\n")


def decidir(alumno, sesion, pid, banco):
    proceso = subprocess.run(["dlv", *DLV_INPUTS, "-filter=accion,motivo,modo_ayuda"],
                             cwd=BASE, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=30)
    if proceso.returncode != 0 or "{" not in proceso.stdout:
        raise RuntimeError("DLV no produjo un modelo.\n" + proceso.stdout + proceso.stderr)
    atomos = [(tipo, valor) for tipo, a, s, p, valor in ATOM.findall(proceso.stdout)
             if a == alumno and int(s) == sesion and int(p) == pid]
    acciones = {v for tipo, v in atomos if tipo == "accion"}
    motivos = {v for tipo, v in atomos if tipo == "motivo"}
    modos = {v for tipo, v in atomos if tipo == "modo_ayuda"}
    if len(acciones) != 1 or len(motivos) != 1 or len(modos) > 1:
        raise RuntimeError("DLV no devolvio una decision univoca.\n" + proceso.stdout)
    accion, motivo = next(iter(acciones)), next(iter(motivos))
    modo = next(iter(modos)) if modos else None
    print("\nTutor:", MENSAJES.get(accion, accion))
    observacion = next((e for e in banco[pid].get("errores_previsibles", [])
                        if e["etiqueta"] == motivo), None)
    if observacion:
        print("Motivo observado en la opcion:", observacion["descripcion"])
    else:
        print("Motivo:", MOTIVOS.get(motivo, motivo))
    if modo:
        print("Tipo de ayuda:", {"pista_breve": "pista breve",
                                  "contrastar_razones": "contrastar razones",
                                  "transferencia": "comparar experiencias"}.get(modo, modo))
    print(f"[DLV: accion={accion}; motivo={motivo}" +
          (f"; modo={modo}]" if modo else "]"))
    return accion, motivo, modo


def mostrar_problema(p):
    print("\n" + "=" * 65)
    print(f"Problema {p['id']}: {p['titulo']}")
    print(p["enunciado"])
    if p.get("pregunta"):
        print(p["pregunta"])
    for opcion in sorted(p["opciones"], key=lambda x: int(x["id"])):
        print(f"  {opcion['id']}. {opcion['texto']}")
    print("=" * 65)


def leer_numero(mensaje, minimo, maximo):
    while True:
        valor = input(mensaje).strip().lower()
        if valor in ("x", "salir"):
            return None
        if valor.isdecimal() and minimo <= int(valor) <= maximo:
            return int(valor)
        print(f"Escribe un numero entre {minimo} y {maximo}, o x para salir.")


def mostrar_solucion(p, alumno, sesion):
    correcta = int(p["clave_docente"]["correcta_id"])
    descripcion = next(o["texto"] for o in p["opciones"] if int(o["id"]) == correcta)
    print(f"\nRespuesta editorial: opcion {correcta}. {descripcion}")
    print("Explicacion:", p["explicacion"])
    if p["nuevo"]:
        print("Limite que ilustra:", p["limite_ia_que_ensena"])
        print("Para reflexionar:", p["reflexion_final"])
        reflexionar(alumno, sesion, p["id"], "final")


def mostrar_antecedente(alumno, sesion, pid, banco, objetivos):
    objetivo = objetivos.get(pid)
    coinciden = [(s, p) for s, p, _ in errores_previos(alumno)
                 if s < sesion and p != pid and objetivos.get(p) == objetivo]
    if coinciden:
        anterior = banco[max(coinciden)[1]]
        print(f"Actividad anterior relacionada: {anterior['id']}. {anterior['titulo']}")
    print("Que tipo de comprobacion era necesaria en ambos casos?")


def dar_ayuda(accion, modo, alumno, sesion, pid, banco, objetivos):
    p = banco[pid]
    if accion == "comparar_objetivo_anterior":
        mostrar_antecedente(alumno, sesion, pid, banco, objetivos)
    elif accion == "comparar_caso_anterior":
        previos = [(s, pp) for s, pp, fase, _ in registros(alumno)
                   if fase == "inicial" and (s, pp) != (sesion, pid)
                   and pp in banco and banco[pp]["familia"] == p["familia"]]
        if previos:
            anterior = banco[max(previos)[1]]
            print("Actividad relacionada:", anterior["titulo"])
        print("En que se parece su estructura a este problema?")
    if modo == "contrastar_razones":
        print("Antes de revisar: contrasta tu argumento con un dato o contraejemplo.")
    elif modo == "pista_breve":
        print("Pista breve:")
    pista = (p.get("pistas") or ["Examina que evidencia respalda la conclusion."])[0]
    print("Pista:", pista)
    reflexionar(alumno, sesion, pid)
    actualizar([f"intervencion_hecha({alumno},{sesion},{pid},{accion})."])


def revisar(alumno, sesion, pid, banco, objetivos, ayudas):
    accion, _, modo = decidir(alumno, sesion, pid, banco)
    if accion in ayudas:
        dar_ayuda(accion, modo, alumno, sesion, pid, banco, objetivos)
        accion, _, _ = decidir(alumno, sesion, pid, banco)
    if accion != "pedir_revision":
        raise RuntimeError("Se esperaba pedir_revision; DLV eligio " + accion)
    p = banco[pid]
    mostrar_problema(p)
    maximo = len(p["opciones"])
    n = leer_numero(f"Respuesta revisada (1-{maximo}, x=salir): ", 1, maximo)
    if n is None:
        return False
    confianza = leer_numero("Confianza revisada (0-100, x=salir): ", 0, 100)
    if confianza is None:
        return False
    guardar_respuesta(alumno, sesion, p, "final", n, confianza)
    accion, _, _ = decidir(alumno, sesion, pid, banco)
    if accion not in ("resumir_revision", "reexaminar_error"):
        raise RuntimeError("Accion inesperada tras revisar: " + accion)
    mostrar_solucion(p, alumno, sesion)
    return True


def realizar(alumno, sesion, pid, banco, objetivos, ayudas):
    actualizar(contexto=(alumno, sesion, pid))
    accion, _, _ = decidir(alumno, sesion, pid, banco)
    if accion != "presentar_pregunta":
        raise RuntimeError("Ya hay respuesta inicial en esta sesion: " + accion)
    p = banco[pid]
    mostrar_problema(p)
    maximo = len(p["opciones"])
    n = leer_numero(f"Respuesta inicial (1-{maximo}, x=salir): ", 1, maximo)
    if n is None:
        return False
    confianza = leer_numero("Confianza inicial (0-100, x=salir): ", 0, 100)
    if confianza is None:
        return False
    guardar_respuesta(alumno, sesion, p, "inicial", n, confianza)
    if clasificar(p, n) != "correcta":
        return revisar(alumno, sesion, pid, banco, objetivos, ayudas)
    accion, _, _ = decidir(alumno, sesion, pid, banco)
    if accion == "pedir_justificacion":
        reflexionar(alumno, sesion, pid)
        actualizar([f"intervencion_hecha({alumno},{sesion},{pid},pedir_justificacion)."])
        accion, _, _ = decidir(alumno, sesion, pid, banco)
    if accion != "proponer_nuevo_caso":
        raise RuntimeError("Accion inesperada tras acierto: " + accion)
    mostrar_solucion(p, alumno, sesion)
    return True


def main():
    ap = argparse.ArgumentParser(description="Sexto Sentido: 35 actividades + DLV")
    ap.add_argument("--alumno", default="alumno1", help="Seudonimo: letras minusculas, digitos y _")
    ap.add_argument("--problema", type=int, help="ID de actividad (1-35)")
    ap.add_argument("--una", action="store_true", help="Realizar una sola actividad")
    ap.add_argument("--listar", action="store_true", help="Listar las 35 actividades sin iniciarlas")
    args = ap.parse_args()
    if not ID_ALUMNO.fullmatch(args.alumno):
        ap.error("--alumno debe comenzar con minuscula y usar solo a-z, 0-9 o _")
    for nombre in [JSON_ORIGINAL.name, JSON_NUEVO.name, *DLV_INPUTS]:
        if nombre == HIST.name:
            continue
        if not (BASE / nombre).is_file():
            ap.error("Falta archivo junto al script: " + nombre)
    banco = cargar_banco()
    reglas, objetivos = cargar_politica(banco)
    ayudas = AYUDAS_ANTIGUAS | set(reglas.values()) | {"comparar_objetivo_anterior"}
    if args.problema is not None and args.problema not in banco:
        ap.error("--problema debe estar entre 1 y 35")
    if args.listar:
        for n, p in sorted(banco.items()):
            print(f"{n:2d}. {p['titulo']}")
        return
    if shutil.which("dlv") is None:
        raise RuntimeError("DLV no esta en el PATH: comprueba 'dlv' en CMD.")
    if not HIST.exists():
        HIST.write_text("% Sexto Sentido 35: historial separado de la version estable.\n",
                        encoding="utf-8")
    elif not HIST.with_suffix(HIST.suffix + ".bak").exists():
        shutil.copy2(HIST, HIST.with_suffix(HIST.suffix + ".bak"))
    actualizar([f"alumno({args.alumno})."])
    print("\nSEXTO SENTIDO: 35 actividades | Python + DLV")
    print("Usa un seudonimo y no escribas datos personales.")
    print("Las categorias describen opciones, no diagnostican tu mente.")
    anteriores = registros(args.alumno)
    finales = {(s, p) for s, p, fase, _ in anteriores if fase == "final"}
    pendientes = [(s, p) for s, p, fase, n in anteriores
                  if fase == "inicial" and (s, p) not in finales
                  and p in banco and clasificar(banco[p], n) != "correcta"]
    if pendientes:
        s, p = max(pendientes)
        pregunta = f"Revision pendiente: sesion {s}, actividad {p}. Retomar? [S/n]: "
        if input(pregunta).strip().lower() not in ("n", "no"):
            actualizar(contexto=(args.alumno, s, p))
            if not revisar(args.alumno, s, p, banco, objetivos, ayudas) or args.una:
                print("Historial conservado en", HIST.name)
                return
    sesion = max((s for s, _, _, _ in registros(args.alumno)), default=0) + 1
    primero = args.problema
    while True:
        usados = {p for _, p, fase, _ in registros(args.alumno) if fase == "inicial"}
        siguiente = next((p for p in sorted(banco) if p not in usados), None)
        if primero is not None:
            pid, primero = primero, None
        else:
            texto = str(siguiente) if siguiente is not None else "ninguna sin usar"
            valor = input(f"Actividad (1-35, Enter={texto}, x=salir): ").strip().lower()
            if valor in ("x", "salir"):
                break
            pid = siguiente if not valor else int(valor) if valor.isdecimal() else None
        if pid not in banco:
            print("Selecciona una actividad valida entre 1 y 35.")
            continue
        if not realizar(args.alumno, sesion, pid, banco, objetivos, ayudas):
            print("Progreso conservado en", HIST.name)
            break
        if args.una or input("\nOtra actividad? [s/N]: ").strip().lower() != "s":
            break
        sesion += 1
    print("Historial conservado en", HIST.name)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSesion terminada. Se conservan los datos ya registrados.")
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print("\nERROR:", exc)
        raise SystemExit(1)
