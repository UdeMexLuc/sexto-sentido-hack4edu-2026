# Sexto Sentido 35 — Guía para tres demostraciones reproducibles

**Propósito.** Mostrar a colegas y evaluadores cómo el tutor, con una interfaz de consola mínima y un motor de reglas ASP/DLV, ofrece ayuda explicable para un uso crítico de la IA. Todos los estudiantes y escenarios de la demostración son ficticios.

**Prerrequisitos:** Windows, Python 3, `dlv` en `PATH`; versión `sexto_35.py` con las 35 actividades; ejecución previa de `probar_sexto_35.cmd` con 25/25 verificaciones.

## Preparación segura

En la carpeta del proyecto, ejecutar **en este orden**:

```cmd
congelar_sexto_35.cmd
preparar_demos_video.cmd
```

El primer comando vuelve a ejecutar las 25 pruebas y crea una copia de código y datos en la carpeta superior, con `MANIFIESTO_SHA256.txt`. El segundo crea una carpeta `DEMOS_VIDEO_SS35_...` con tres subcarpetas aisladas, ejecuta cada caso con DLV y guarda las transcripciones para el equipo de video.

No se copian los historiales ni reflexiones personales. **No grabar** la carpeta real de historiales o los nombres del equipo; usar solamente los pseudónimos de las demostraciones. Los ejecutables `EJECUTAR_DEMO_N.cmd` se pueden volver a ejecutar cuantas veces se quiera sin alterar datos del proyecto.

## Demostración 1: Verificar una respuesta aparentemente convincente

- **Actividad:** 25, *La mochila de Lucía*.
- **Pseudónimo:** `demo_calculo`.
- **Entrada inicial:** opción `1`, confianza `90`.
- **Intervención esperada:** `verificar_operaciones`, modo `contrastar_razones`.
- **Revisión:** opción `2`, confianza `85`.
- **Cierre esperado:** `resumir_revision`.
- **Mensaje educativo:** amabilidad y personalización no garantizan corrección; el estudiante comprueba las bases porcentuales.

## Demostración 2: Información falsa o no comprobada

- **Actividad:** 29, *El aviso escolar que circula en el chat*.
- **Pseudónimo:** `demo_aviso`.
- **Entrada inicial:** opción `1`, confianza `95`.
- **Intervención esperada:** `detener_y_verificar`, modo `contrastar_razones`.
- **Revisión:** opción `3`, confianza `85`.
- **Cierre esperado:** `resumir_revision`.
- **Mensaje educativo:** antes de compartir una noticia urgente, identificar la fuente, la fecha y la vía oficial de confirmación. **El programa NO verifica noticias reales ni consulta páginas web.**

## Demostración 3: Adaptación mediante historial

Dos ejecuciones consecutivas, **mismo pseudónimo `demo_historial`**, pero sesiones diferentes:

1. **Actividad 24:** opción inicial `1`, confianza `90`; intervención `distinguir_impresion_evidencia`; opción revisada `3`, confianza `80`.
2. **Actividad 26:** opción inicial `2`, confianza `90`; esta vez DLV usa el error anterior en una actividad relacionada y selecciona `comparar_objetivo_anterior` con motivo `antecedente_en_mismo_objetivo`; opción revisada `1`, confianza `85`.

El transcript mostrará `Actividad anterior relacionada: 24.` como comprobación de que se utilizó el historial.

## Para la grabación

1. Abrir una de las tres subcarpetas dentro de `DEMOS_VIDEO_SS35_...`.
2. Ejecutar su `EJECUTAR_DEMO_N.cmd` **desde CMD** (o volver a generar las tres con `preparar_demos_video.cmd`).
3. Observar `[OK] DEMO N COMPLETADA Y VALIDADA` y mostrar las líneas `[DLV: accion=...; motivo=...; modo=...]`.
4. Si se necesita detener o ampliar la imagen durante la edición, abrir `TRANSCRIPCION_DEMO_N.txt` en un editor con letra grande. La transcripción procede de **ejecuciones reales** de Python + DLV; los valores introducidos automáticamente se reinsertan junto a los prompts para facilitar su lectura.
5. No interpretar un acierto corregido en una única sesión como evidencia de aprendizaje duradero; es solo una demostración del flujo de intervención.

## Señales de fallo

Si una acción DLV ya no coincide con lo esperado, el reproductor devuelve `[FALLO]` y **no debe usarse la grabación** como demostración validada. No modificar la salida manualmente. Corregir primero el software o actualizar explícitamente el guion para que represente lo que ocurre.

## Archivos esperados

- `TRANSCRIPCION_DEMO_1.txt`, `TRANSCRIPCION_DEMO_2.txt`, `TRANSCRIPCION_DEMO_3.txt`;
- `SALIDA_BRUTA_1.txt` (en la demo 3 también `SALIDA_BRUTA_2.txt`);
- `RESULTADO_DEMOS.txt` con `[OK] 3/3` en la carpeta superior de las demostraciones.
