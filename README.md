# Sexto Sentido: antes de creer

**Laboratorio de pensamiento crítico con IA · Hack4Edu 2026 · Versión `v0.2.0` — razones previas, recorrido guiado y resumen de decisiones.**

Una respuesta convincente puede estar equivocada. Sexto Sentido propone casos breves para practicar cómo comprobar una afirmación, identificar información insuficiente y revisar una decisión. Utiliza **IA simbólica (ASP/DLV)** para elegir ayudas pedagógicas con un motivo explícito.

![Resumen de decisiones de Sexto Sentido v0.2.0](interfaz/vista_resumen_v020.png)

Esta versión añade una justificación opcional antes de la ayuda, un recorrido de cuatro casos y un resumen imprimible y descargable en CSV. Conserva el ajuste UTF-8 de v0.1.1. Consulta el [historial de cambios](CHANGELOG.md).

## Para el jurado: empezar aquí

1. Descarga el repositorio con **Code → Download ZIP** y descomprímelo, o clónalo con Git.
2. Instala Python 3.9 o posterior y configura **DLV clásico** siguiendo [la guía de instalación](docs/INSTALACION.md). No se requieren paquetes Python de terceros. El ejecutable DLV es una dependencia externa y no está incluido.
3. Abre una terminal en la carpeta del repositorio y ejecuta:

```sh
python3 ejecutar.py --interfaz
```

En Windows usa `py -3 ejecutar.py --interfaz`. Abre **http://127.0.0.1:8765** en tu navegador y conserva la terminal abierta. Para cerrar, presiona **Ctrl+C**. Si el puerto está ocupado, añade `--port 8766` y abre la dirección que se indique.

El repositorio contiene el código de una aplicación local: visitar GitHub permite inspeccionarlo o descargarlo, pero no ejecuta el tutor en línea. Una vez configuradas las dependencias, la actividad no requiere Internet.

## Qué probar

Usa un seudónimo ficticio, por ejemplo `jurado_demo`, y pulsa **Empezar el recorrido**. La secuencia es **25 → 29 → 31 → 34**: cálculo, información sin verificar, privacidad e incertidumbre. Al terminar cada caso, guarda la reflexión para pasar al siguiente; el cuarto conduce al resumen.

Antes de consultar al tutor puedes registrar por qué elegiste una opción. La razón inicial se conserva tal como se envió. Si revisas la elección, puedes añadir otra razón **antes de ver la explicación**. La reflexión final se solicita después de la explicación y se distingue de ambas razones.

Puedes ir al banco y pulsar **Retomar actividad** para continuar el mismo intento. La pantalla se recupera tras recargar el navegador. Si empiezas otro caso desde el banco, se conserva lo registrado del intento anterior, pero ese intento deja de ser la actividad pausada.

En **Resumen de decisiones** puedes consultar respuestas, confianza, ayudas y razones, imprimir la vista o descargar **todos los intentos del seudónimo actual** en CSV. No se asigna una nota de pensamiento crítico ni se califican automáticamente los textos. Las actividades libres siguen disponibles en **Explorar actividades**.

Para inspeccionar ayudas concretas puedes usar estos recorridos adicionales desde el banco:

| Recorrido | Pasos sugeridos | Qué permite observar |
| --- | --- | --- |
| Caso 25: La mochila de Lucía | Opción inicial 1, confianza 90; después de la pista, opción 2 | Una explicación amable puede contener un error de cálculo; ayuda para verificar las bases porcentuales. |
| Caso 29: Aviso escolar | Opción inicial 1, confianza 95; después, opción 3 | El tutor prioriza detenerse y verificar la información antes de difundirla. |
| Adaptación por antecedentes | Con el mismo seudónimo: caso 24, opción 1 y revisión 3; luego caso 26, opción inicial 2 | La ayuda remite a una actividad previa con el mismo objetivo formativo. |

Las respuestas sugeridas son entradas ficticias para recorrer las funciones del software; no representan observaciones de estudiantes. También puedes responder libremente. Si aciertas inicialmente, pasarás a la explicación; con baja confianza, el tutor puede pedir una justificación.

En cada caso puedes desplegar **«¿Cómo tomó esta decisión el tutor?»** para inspeccionar la acción y el motivo producidos por DLV. La interfaz dispone de pantalla completa para la presentación.

## Qué incluye esta versión

- **35 actividades:** 23 ejercicios de razonamiento y 12 casos sobre uso crítico y responsable de IA.
- Interfaz en navegador y versión de consola.
- Respuesta, confianza y justificación opcional antes de la ayuda; revisión con razón opcional y reflexión final posterior a la explicación.
- Recorrido guiado de cuatro casos y pausa con reanudación.
- Resumen para estudiante y docente, impresión y exportación CSV.
- Registro local de las decisiones y sus revisiones.
- Intervenciones explicables a partir de opciones elegidas, confianza e historial.
- Pruebas de integración y demostraciones reproducibles.

## Cómo funciona

```text
Caso editorial → elección y confianza del estudiante
              → Python clasifica la opción usando la clave docente
              → ASP/DLV selecciona una acción y explica su motivo
              → pista / revisión → explicación y reflexión
```

Las claves de respuesta proceden de un banco editorial. DLV selecciona la intervención; no inventa las respuestas correctas. Las reflexiones se guardan para consulta humana y no se evalúan semánticamente de forma automática.

## Verificación técnica

```sh
python3 ejecutar.py --comprobar
python3 ejecutar.py --pruebas
python3 ejecutar.py --pruebas-interfaz
```

La suite original contiene **25 comprobaciones**. La suite de interfaz contiene **14 grupos**, con recorridos de acierto y error para las 35 actividades, segundos distractores, transferencia, prioridad de precaución, recuperación de sesión y manejo de fallos de DLV. También verifica el orden de captura de la razón inicial, el recorrido de cuatro casos, pausa y recuperación, separación de seudónimos, compatibilidad de registros anteriores y exportación CSV. Ambas utilizan historiales temporales. Consulta [el registro de validación](docs/VALIDACION.md).

Para listar las actividades o usar la consola:

```sh
python3 ejecutar.py --listar
python3 ejecutar.py --consola --alumno demo --problema 25 --una
```

`python3 ejecutar.py --demos` genera tres demostraciones con transcripciones y verifica sus acciones contra DLV. Crea una nueva carpeta local; sus archivos no forman parte del código fuente versionado.

## Alcance y límites

- Trabaja con escenarios preparados: no verifica noticias ni fuentes de Internet en tiempo real.
- No detecta técnicamente imágenes o audios manipulados.
- No diagnostica mecanismos mentales ni sustituye al docente o a profesionales.
- La ayuda considera antecedentes; la elección de la siguiente actividad es manual.
- La opción elegida se evalúa con una clave: el programa todavía no exige introducir cálculos propios. Las razones se registran, pero no se evalúa automáticamente su calidad.
- Las pruebas funcionales no demuestran mejora del aprendizaje ni cumplimiento formal de una rúbrica del concurso.

## Datos y privacidad de la demostración

Utiliza datos ficticios. La interfaz guarda respuestas, confianza, reflexiones y sesiones en `datos_interfaz/`, excluida de Git. La consola utiliza archivos de historial propios dentro del banco estable, también excluidos. Los intentos de la interfaz se guardan también en `datos_interfaz/intentos_interfaz.jsonl`; cada actualización conserva las razones iniciales y las revisiones como eventos. Los registros anteriores pueden mostrarse con campos ausentes identificados y sin inventar justificaciones. Los archivos son locales y no están cifrados; esta versión no tiene autenticación y escucha únicamente en `127.0.0.1`.

## Organización

```text
ejecutar.py                            Lanzador de la entrega
interfaz/                              Ventana local y pruebas de integración
KB_SextoSentido_35_ESTABLE_20261104_104711/  Motor, reglas y banco original
docs/                                  Instalación y evidencia técnica
```

La versión del producto está en `VERSION`. La interfaz de v0.2.0 conserva el motor de v0.1.1. La carpeta del motor conserva su nombre histórico. En v0.1.1 se actualizaron los dos preparadores de demos y sus metadatos; el manifiesto SHA-256 corresponde a esta revisión. El motor, las reglas y los bancos permanecen iguales a v0.1.0. Sus guías históricas describen el empaquetado previo; para ejecutar esta entrega sigue este README. El guion de diez minutos es material interno de producción y no establece la duración oficial de entrega del hackatón.

DLV es software de terceros y mantiene sus condiciones de licencia. Consulta [la documentación de DLVSystem](https://www.dlvsystem.it/dlvsite/dlv/). Esta publicación no incorpora el ejecutable ni asigna una nueva licencia al trabajo previo del equipo.
