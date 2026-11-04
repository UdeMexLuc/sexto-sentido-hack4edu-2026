# Validación de v0.1.0

Fecha: **4 de noviembre de 2026**. Entorno de ejecución: **macOS 15.6.1, Apple Silicon arm64, Python 3.9.6 y DLV clásico build BEN/Mar 29 2023**.

## Ejecución desde la copia de entrega

| Comando | Resultado | Registro |
| --- | --- | --- |
| `python3 ejecutar.py --comprobar` | Python y DLV identificados | [Entorno](ENTORNO_20261104.txt) |
| `python3 ejecutar.py --pruebas` | 25/25 comprobaciones | [Pruebas del motor](PRUEBAS_ENTREGA_20261104.txt) |
| `python3 ejecutar.py --pruebas-interfaz` | 6 grupos de pruebas aprobados | [Pruebas de la interfaz](PRUEBAS_INTERFAZ_20261104.txt) |

Los grupos de la interfaz incluyen aciertos iniciales con baja confianza y errores con revisión correcta para las **35 actividades**; también cubren los segundos distractores de los 12 casos nuevos, revisión incorrecta, transferencia 24→26, prioridad de precaución 28→29, entradas no válidas, rechazo de envíos duplicados, recuperación de sesión y reversión de una respuesta si falla DLV. Los recorridos se ejecutan contra el motor real; solo se simula un fallo en el caso específico de recuperación.

## Integridad y comprobación visual

- Los 19 archivos declarados en el manifiesto SHA-256 del motor conservan sus huellas originales.
- La interfaz original se comprobó en navegador: caso 25 completo, ayuda, revisión, resultado, retorno al banco, 35 tarjetas, ventana de límites y recuperación del progreso al recargar.
- Se revisó el diseño a 1440 y 390 píxeles de ancho. No hubo desbordamiento horizontal en la vista de inicio de 390 píxeles.
- La captura incluida en el README procede de una sesión ficticia de prueba.
- Antes de preparar esta entrega, las tres demos reproducibles pasaron 3/3 con DLV en este Mac.

## Límites de esta evidencia

Estas verificaciones demuestran funcionamiento en los escenarios probados. No constituyen un estudio de aprendizaje, una evaluación de accesibilidad completa, una validación independiente en todos los sistemas operativos ni una certificación de cumplimiento de la rúbrica del hackatón.

La entrega excluye historiales de uso, reflexiones, cookies de sesión, respaldos redundantes y el ejecutable de DLV. Para reproducir las pruebas se necesita instalar externamente una versión compatible del motor.
