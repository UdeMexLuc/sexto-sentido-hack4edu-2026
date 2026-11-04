# Sexto Sentido 35 — Matriz de cobertura del Reto 07

**Fecha de revisión:** 4 de noviembre de 2026. **Estado:** prototipo de consola verificado técnicamente en los escenarios probados (25/25, según la ejecución comunicada por el equipo). No es un estudio de eficacia educativa ni una certificación de cumplimiento formal.

## Fuentes y alcance de la verificación

- **Enunciado de trabajo facilitado por el equipo:** Reto 07, *«Una IA que también explique sus límites»*; pregunta orientadora: *«¿Cómo enseñar a niños y jóvenes a utilizar la inteligencia artificial de forma crítica, segura y responsable?»*.
- **Fuente oficial pública disponible:** [ProFuturo — Hack4Edu](https://profuturo.education/hack4edu/) y [anuncio Hack4Edu 2026](https://profuturo.education/noticias/hack4edu-2026-vuelve-el-hackathon-internacional-de-innovacion-educativa-con-tecnologia-de-fundacion-telefonica-y-fundacion-la-caixa/): confirma el propósito de desarrollar prototipos para desafíos educativos reales, con áreas como IA, inclusión y accesibilidad.
- **Limitación de la verificación oficial:** no se localizó una rúbrica detallada y accesible del **Reto 07** con requisitos ponderados o límites de duración del video. Esta matriz **no atribuye criterios numerados ni puntuaciones oficiales** a la organización. Los puntos de abajo son una operacionalización interna de la pregunta facilitada por el equipo.
- **Orientación pedagógica complementaria, NO bases del concurso:** [INTEF, guía de IA educativa 2026](https://intef.es/Noticias/nueva-version-de-la-guia-sobre-el-uso-de-la-inteligencia-artificial-en-el-ambito-educativo/) y [INTEF, pensamiento crítico mediante IA](https://formacion.intef.es/aulaenabierto/mod/book/tool/print/index.php?id=9256).

## Matriz de capacidades observables

| Objetivo educativo operacionalizado | Evidencia en Sexto Sentido 35 | Estado técnico | Qué NO se puede afirmar |
|---|---|---|---|
| Cuestionar respuestas convincentes pero incorrectas | Actividades 24, 25, 26, 27, 34; comparar argumentos y verificar operaciones | **Demostrable**: demo 1 y tests T05–T08 | No prueba que la habilidad se generalice a nuevas situaciones reales |
| Contrastar fuentes y no propagar información no verificada | Actividades 28 y 29; `pedir_verificacion_fuente`, `detener_y_verificar` | **Demostrable**: demo 2 | No navega ni autentica referencias, redes o noticias en tiempo real |
| Distinguir suplantación o medios sintéticos de evidencia verificada | Actividad 32; `verificar_procedencia_multimedia` | **Cobertura didáctica** | No inspecciona ni detecta técnicamente audios falsos |
| Pensar en equidad y sesgos | Actividad 30; `examinar_criterios_pertinentes` | **Cobertura didáctica** | No mide ni certifica ausencia de sesgos en modelos reales |
| Protección de datos personales | Actividad 31; `revisar_privacidad_y_consentimiento` | **Cobertura didáctica** | La consola acepta reflexiones libres: no filtra datos sensibles, no cifra archivos locales |
| Reconocer cuándo hace falta intervención humana | Actividad 33; `reconocer_limites_y_derivar` | **Cobertura didáctica** | No reemplaza profesionales ni ofrece consejo médico personalizado |
| Integridad académica y responsabilidad | Actividad 35; `distinguir_apoyo_y_sustitucion` | **Cobertura didáctica** | No verifica plagio ni autoría de trabajos reales |
| Explicar por qué interviene el tutor | DLV entrega `accion`, `motivo` y a veces `modo_ayuda`; Python muestra trazas | **Demostrable** en las 3 demos | Transparencia de la política no equivale a explicar el funcionamiento interno de un LLM |
| Adaptar ayuda según respuestas e historial | `observacion_error`, confianza, sesiones previas y `comparar_objetivo_anterior` | **Demostrable**: demo 3 y T21 | No demuestra un perfil psicológico ni una mejoría sostenida |
| Explicar los límites de la propia herramienta | Avisos de pseudónimo y clasificación no psicológica; campo editorial `limite_ia_que_ensena` tras cada caso | **Parcial** | Falta una pantalla inicial completa «Qué hace y qué no hace»; el usuario podría creer que se verifican fuentes reales |
| Prototipo simple, reproducible y ejecutable localmente | Python + DLV clásico, datos JSON, 35 actividades, tests automatizados, respaldos con SHA-256 | **Demostrable**: 25/25 pruebas informadas por el equipo | Las pruebas funcionales no son pruebas de accesibilidad, robustez ante todos los fallos o validez externa |

## Arquitectura y significado de «IA»

El prototipo utiliza **IA simbólica**: reglas explícitas y programación lógica ASP ejecutada mediante DLV, más un banco editorial revisable. No contiene un chatbot generativo ni pretende reconocer emociones o mecanismos mentales. Python determina la categoría observable **a partir de la opción elegida y la clave editorial**. DLV utiliza esa categoría, la confianza y los antecedentes para elegir una intervención. La separación es valiosa porque permite auditar las decisiones y evita que las reglas inventen respuestas correctas.

## Límites que deben decirse expresamente en el video

1. **No hay verificación externa en directo.** Los ejemplos simulan afirmaciones de IA; el tutor propone cómo contrastarlas, pero no comprueba noticias, artículos, páginas ni voces.
2. **No hay diagnóstico psicológico.** Una elección errónea no revela qué «sistema» de Kahneman utilizó un alumno.
3. **No hay evidencia de eficacia pedagógica aún.** 25/25 son pruebas de software y de decisiones previstas; no miden aprendizaje real, retención o transferencia en población escolar.
4. **Los datos son locales y deben tratarse con cuidado.** Utilizar pseudónimos y datos ficticios; evitar almacenar información sensible de menores. El sistema todavía no incluye cifrado, control de acceso ni filtrado automático de datos personales.
5. **La duración del video no está verificada como requisito oficial.** El guion de 10 minutos es una guía para el equipo, sujeta a los límites que establezca la organización.

## Siguiente mínimo ajuste recomendado (FUERA del respaldo congelado)

Agregar una pantalla inicial o comando `--limites` con cuatro frases: «Este tutor usa situaciones ficticias y reglas ASP», «No verifica información en Internet», «No diagnostica tu mente», y «No reemplaza al docente ni a los profesionales». Esto cerraría una laguna concreta respecto al título del reto sin necesidad de un modelo generativo ni una interfaz gráfica. **No debe introducirse silenciosamente en la versión congelada:** crearía una versión posterior sometida a nuevas pruebas.

## Dictamen para el equipo

**Cobertura conceptual sólida y demostración técnica viable.** El prototipo permite enseñar de forma operativa verificación, prudencia, equidad, privacidad y agencia humana. El cumplimiento **formal** de las bases específicas del Reto 07 permanece **pendiente de contraste con el documento oficial del reto**, y la eficacia educativa debe someterse a evaluación con usuarios y docentes.
