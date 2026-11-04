# Historial de cambios

## v0.1.1 — 4 de noviembre de 2026

Corrige la configuración de UTF-8 al preparar y ejecutar las demostraciones en Windows CMD.

- Se incorporan `preparar_demos_video.py` y `preparar_demos_video.cmd` de la carpeta de trabajo `KB_SextoSentido_23`, posteriores al respaldo publicado inicialmente.
- El CMD de preparación y los tres CMD generados configuran `chcp 65001`, `PYTHONIOENCODING=utf-8` y `PYTHONUTF8=1`.
- Se actualizan VERSION, el estado de versión y las huellas de los dos archivos modificados en el manifiesto SHA-256.
- El tutor de 35 actividades, las reglas DLV, los bancos JSON y la interfaz conservan el mismo comportamiento que v0.1.0.

La carpeta `KB_SextoSentido_35_ESTABLE_20261104_104711` conserva su nombre por compatibilidad con el lanzador. Dentro de esta entrega contiene la revisión v0.1.1; la etiqueta v0.1.0 conserva la copia anterior.

## v0.1.0 — 4 de noviembre de 2026

Primera entrega pública para Hack4Edu 2026: tutor de 35 actividades, interfaz local, consola, pruebas de integración y documentación para el jurado.
