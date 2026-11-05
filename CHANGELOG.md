# Historial de cambios

## v0.2.0 — 4 de noviembre de 2026

- Captura una justificación inicial breve y opcional antes de consultar a DLV. Conserva por separado la razón de la revisión y la reflexión posterior a la explicación.
- Añade el recorrido guiado 25 → 29 → 31 → 34, con avance explícito, pausa y reanudación tras recargar.
- Añade un resumen para estudiante y docente con decisiones, confianza, ayudas y razones, impresión y descarga CSV UTF-8.
- Conserva las 35 actividades para exploración libre. Las reflexiones se registran para revisión humana, sin calificación automática ni nota general de pensamiento crítico.
- El diario de intentos permite recuperar los datos y reservar sesiones distintas entre pestañas. Los registros anteriores se muestran con sus campos disponibles.
- Amplía a 14 los grupos de pruebas de la interfaz, incluidas captura previa a la ayuda, conservación de razones, recorrido, recuperación, datos anteriores y CSV con texto libre.
- Mantiene el motor, las reglas y los bancos de v0.1.1. Las entregas anteriores conservan sus etiquetas.

## v0.1.1 — 4 de noviembre de 2026

Corrige la configuración de UTF-8 al preparar y ejecutar las demostraciones en Windows CMD.

- Se incorporan `preparar_demos_video.py` y `preparar_demos_video.cmd` de la carpeta de trabajo `KB_SextoSentido_23`, posteriores al respaldo publicado inicialmente.
- El CMD de preparación y los tres CMD generados configuran `chcp 65001`, `PYTHONIOENCODING=utf-8` y `PYTHONUTF8=1`.
- Se actualizan VERSION, el estado de versión y las huellas de los dos archivos modificados en el manifiesto SHA-256.
- El tutor de 35 actividades, las reglas DLV, los bancos JSON y la interfaz conservan el mismo comportamiento que v0.1.0.

La carpeta `KB_SextoSentido_35_ESTABLE_20261104_104711` conserva su nombre por compatibilidad con el lanzador. Dentro de esta entrega contiene la revisión v0.1.1; la etiqueta v0.1.0 conserva la copia anterior.

## v0.1.0 — 4 de noviembre de 2026

Primera entrega pública para Hack4Edu 2026: tutor de 35 actividades, interfaz local, consola, pruebas de integración y documentación para el jurado.
