# Validación de las entregas

## v0.2.0 — recorrido, justificaciones y resumen

Fecha: **4 de noviembre de 2026**. Pruebas ejecutadas desde una copia temporal de entrega con Python 3.9.6, macOS Apple Silicon y DLV clásico build BEN/Mar 29 2023.

- **25/25 comprobaciones del motor aprobadas.**
- **14 grupos de pruebas de la interfaz aprobados.**
- **3/3 demostraciones reproducidas con DLV.**
- Los 19 archivos del motor conservan las huellas del manifiesto de v0.1.1.
- Las pruebas nuevas verifican la escritura de la razón antes de consultar DLV, razones iniciales y revisadas independientes, recorrido completo, pausa y reanudación, sesiones entre pestañas, recuperación de registros anteriores y reversión ante fallos.
- La exportación CSV se verificó con Unicode, comas, saltos de línea y texto que podría interpretarse como fórmula.

En el navegador se completó el recorrido **25 → 29 → 31 → 34** con un seudónimo ficticio, combinando errores con revisión, aciertos con baja confianza y aciertos directos. Se comprobó la pausa, recarga y reanudación, y se descargó un CSV real con las cuatro actividades y sus razones. El resumen mostró cuatro intentos finalizados y dos revisiones. También se revisaron las vistas de escritorio y de 390 píxeles, sin desbordamiento horizontal.

[Registro completo de v0.2.0](PRUEBAS_V0.2.0_20261104.txt). [Guía del recorrido y resumen](GUIA_V0.2.0.md).

Estas pruebas verifican funcionamiento; no demuestran aprendizaje ni validan una calificación del pensamiento crítico. No se ha realizado una nueva ejecución independiente en Windows. Las capturas usan exclusivamente datos ficticios y la entrega excluye historiales y el binario DLV.

## v0.1.1 — ajuste UTF-8 para demos de Windows

Fecha: **4 de noviembre de 2026**. Se ejecutó la copia de entrega en una carpeta temporal con Python 3.9.6, macOS Apple Silicon y DLV clásico build BEN/Mar 29 2023.

- **25/25 comprobaciones del motor aprobadas.**
- **6 grupos de pruebas de la interfaz aprobados.**
- **3/3 demostraciones reproducidas y verificadas con DLV.**
- Los tres CMD generados incluyen `chcp 65001`, `PYTHONIOENCODING=utf-8` y `PYTHONUTF8=1`.
- Las huellas de los 19 archivos coinciden con el manifiesto actualizado. Solo cambian las dos huellas de los preparadores de demos, además de la cabecera del manifiesto.
- Los dos preparadores coinciden byte a byte con los de la carpeta de trabajo `KB_SextoSentido_23`.

[Registro completo de v0.1.1](PRUEBAS_V0.1.1_20261104.txt).

Esta revisión verifica la ejecución en Mac y la configuración de los CMD generados; no incluye una nueva ejecución independiente de esos CMD en Windows. Se conservan el motor, las reglas, el banco y la interfaz de v0.1.0, así como la etiqueta pública de esa entrega.

## v0.1.0 — registro histórico

Fecha: **4 de noviembre de 2026**. Entorno de ejecución: **macOS 15.6.1, Apple Silicon arm64, Python 3.9.6 y DLV clásico build BEN/Mar 29 2023**.

### Ejecución desde la copia de entrega

| Comando | Resultado | Registro |
| --- | --- | --- |
| `python3 ejecutar.py --comprobar` | Python y DLV identificados | [Entorno](ENTORNO_20261104.txt) |
| `python3 ejecutar.py --pruebas` | 25/25 comprobaciones | [Pruebas del motor](PRUEBAS_ENTREGA_20261104.txt) |
| `python3 ejecutar.py --pruebas-interfaz` | 6 grupos de pruebas aprobados | [Pruebas de la interfaz](PRUEBAS_INTERFAZ_20261104.txt) |

Los grupos de la interfaz incluyen aciertos iniciales con baja confianza y errores con revisión correcta para las **35 actividades**; también cubren los segundos distractores de los 12 casos nuevos, revisión incorrecta, transferencia 24→26, prioridad de precaución 28→29, entradas no válidas, rechazo de envíos duplicados, recuperación de sesión y reversión de una respuesta si falla DLV. Los recorridos se ejecutan contra el motor real; solo se simula un fallo en el caso específico de recuperación.

### Integridad y comprobación visual

- Los 19 archivos declarados en el manifiesto SHA-256 del motor conservan sus huellas originales.
- La interfaz original se comprobó en navegador: caso 25 completo, ayuda, revisión, resultado, retorno al banco, 35 tarjetas, ventana de límites y recuperación del progreso al recargar.
- Se revisó el diseño a 1440 y 390 píxeles de ancho. No hubo desbordamiento horizontal en la vista de inicio de 390 píxeles.
- La captura incluida en el README procede de una sesión ficticia de prueba.
- Antes de preparar esta entrega, las tres demos reproducibles pasaron 3/3 con DLV en este Mac.

### Límites de esta evidencia

Estas verificaciones demuestran funcionamiento en los escenarios probados. No constituyen un estudio de aprendizaje, una evaluación de accesibilidad completa, una validación independiente en todos los sistemas operativos ni una certificación de cumplimiento de la rúbrica del hackatón.

La entrega excluye historiales de uso, reflexiones, cookies de sesión, respaldos redundantes y el ejecutable de DLV. Para reproducir las pruebas se necesita instalar externamente una versión compatible del motor.
