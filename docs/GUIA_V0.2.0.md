# Guía de v0.2.0 para estudiante, docente y jurado

## Recorrido guiado

Inicia `python3 ejecutar.py --interfaz`, abre la dirección local indicada y utiliza un seudónimo ficticio. Pulsa **Empezar el recorrido**.

| Paso | Caso | Comprobación que se practica |
| --- | --- | --- |
| 1 | 25 · La mochila de Lucía | Revisar operaciones y bases porcentuales. |
| 2 | 29 · Aviso escolar | Consultar procedencia y confirmación antes de difundir. |
| 3 | 31 · Lista del grupo | Reconocer datos identificables y usar ejemplos ficticios. |
| 4 | 34 · Ahorro de energía | Pedir datos, explicitar supuestos y reconocer incertidumbre. |

En cada caso:

1. Elige una opción y declara tu confianza entre 0 y 100.
2. Si quieres, escribe **por qué la elegiste antes de recibir ayuda**. La razón se conserva como texto; no se califica automáticamente.
3. Consulta al tutor. DLV aplica las mismas reglas pedagógicas de la versión anterior. Puede mostrar una pista o, ante un acierto con poca confianza, pedir una justificación.
4. Si hay revisión, puedes mantener o cambiar la respuesta y registrar otra razón antes de ver la explicación.
5. Lee la explicación y registra, si quieres, una reflexión final. Esta reflexión ocurre después de conocer la respuesta de referencia.
6. Guarda para continuar. El cuarto cierre abre el resumen del recorrido.

Los aciertos iniciales pasan a la explicación, salvo que el motor pida una justificación. No se crea una respuesta revisada cuando no se ha solicitado revisión.

## Pausa y exploración libre

Puedes volver a Inicio o al banco y usar **Retomar actividad**. La cookie local y el archivo de sesión permiten recuperar esa actividad al recargar el navegador. El resumen puede consultarse durante una actividad sin cerrarla.

Si inicias otra actividad, se conserva lo registrado del intento anterior y se abre un intento distinto. El banco permite elegir las 35 actividades; sus filtros separan los 12 casos sobre IA de los 23 fundamentos de razonamiento.

## Resumen para estudiante y docente

El resumen corresponde al seudónimo de la sesión actual. Muestra los intentos con respuesta, su estado de cierre y las revisiones registradas. Cada intento reúne:

- opción, texto elegido y confianza inicial;
- razón inicial, escrita antes de la intervención;
- ayuda del tutor, motivo y reflexión posterior a la ayuda, cuando existen;
- opción, confianza y razón revisadas, cuando se solicitó revisión;
- reflexión final posterior a la explicación.

**Finalizado** significa que se pulsó el cierre de la actividad. No indica por sí mismo acierto, dominio de una habilidad o aprendizaje duradero. **Registro anterior** identifica datos previos a v0.2.0 cuyo cierre o justificación pueden no estar documentados.

El botón **Descargar registros (CSV)** exporta todos los intentos del seudónimo actual. Utiliza UTF-8 con BOM y separa columnas para razones y momentos distintos. El texto que podría interpretarse como fórmula se exporta como texto. **Imprimir resumen** abre la impresión del navegador; también puede guardarse como PDF desde ese diálogo.

El docente puede comparar la relación entre la razón y la decisión, discutir qué comprobación fue pertinente y proponer un caso nuevo. El software no produce una nota general ni evalúa semánticamente los textos.

## Datos locales

Se mantienen `historial_interfaz.dlv`, `reflexiones_interfaz.jsonl` y los archivos de sesión. Se añade `intentos_interfaz.jsonl`, un diario de las actualizaciones de cada intento. Todos están en `datos_interfaz/`, excluido de Git.

Utiliza únicamente datos ficticios para una demostración pública. Esta versión local conserva los límites y requisitos de instalación descritos en el README.
