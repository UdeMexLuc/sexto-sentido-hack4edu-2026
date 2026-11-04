# Sexto Sentido — Suggested 10-minute demonstration video

**Video production draft (English).** Use real terminal footage from the reproducible demo scripts. All test students are fictional. The ten-minute duration is a **team planning estimate, not a verified competition rule**. Confirm the allowed submission length.

## 0:00–0:50 — The educational challenge

**On screen:** Title, one question, and a simple subtitle: *Can a convincing AI answer still be wrong?*

**Suggested narration:**

> Generative AI can be fluent, helpful, and persuasive. But fluent language is not evidence of correctness. Students need to learn when to verify an answer, protect private information, question stereotypes, and keep human judgment in control. Sexto Sentido is a small educational tutor designed to practice precisely those decisions.

## 0:50–2:05 — How the prototype works

**On screen:** A simple graphic or terminal listing: **35 activities → Python checks an editorial answer key → ASP/DLV selects an intervention → student revises → history is stored**. Show `python sexto_35.py --listar` briefly.

**Suggested narration:**

> The prototype is deliberately simple. The front end is a Python console. The content bank contains 23 reasoning exercises and 12 activities about the responsible use of AI. The editorial keys determine which answer is correct. The reasoning engine, written in Answer Set Programming and executed by DLV, does not invent correct answers. Instead, it considers the student's selected option, declared confidence, and earlier attempts to choose an understandable pedagogical intervention. The interface displays both the chosen action and its reason.

## 2:05–4:05 — Demonstration 1: A convincing mathematical mistake

**On screen:** Run `EJECUTAR_DEMO_1.cmd` from `01_verificar_calculo`, or show its verified `TRANSCRIPCION_DEMO_1.txt`. Highlight the activity 25, initial answer `1` with confidence `90`, then:

```text
[DLV: accion=verificar_operaciones; motivo=aceptacion_por_personalizacion; modo=contrastar_razones]
```

**Suggested narration:**

> The first scenario presents an AI answer about a percentage increase followed by a discount. The response sounds supportive and personalized, but it uses a faulty rule. Our fictional student accepts the intuitive answer with high confidence. The tutor identifies the type of argument selected; it does not infer the student's mental state. DLV asks for a check of the arithmetic and the percentage bases. The student revises the choice, and the tutor explains the correct reasoning. We can see the action and its explanation in the terminal.

## 4:05–5:50 — Demonstration 2: An unverified school announcement

**On screen:** Run `EJECUTAR_DEMO_2.cmd`. Highlight activity 29 and:

```text
[DLV: accion=detener_y_verificar; motivo=difusion_precipitada; modo=contrastar_razones]
```

**Suggested narration:**

> Our second example is an urgent announcement circulating in a school chat. The student initially chooses to share it immediately. This time the tutor prioritizes a precautionary action: stop and verify. It asks the student to look for trustworthy confirmation, rather than treating urgency or repeated messages as proof. Importantly, the program does not connect to social networks and cannot tell whether a real message is true. It teaches a verification habit through a fictional scenario.

## 5:50–8:05 — Demonstration 3: Adaptation from earlier responses

**On screen:** Run `EJECUTAR_DEMO_3.cmd`. Show two consecutive activities under the same pseudonym. In the second activity, highlight:

```text
[DLV: accion=comparar_objetivo_anterior; motivo=antecedente_en_mismo_objetivo; modo=transferencia]
Actividad anterior relacionada: 24.
```

**Suggested narration:**

> The third demonstration shows that the tutor has a memory of observable learning events. In the first activity, the student mistakes an appealing presentation for evidence of educational effectiveness. A later activity addresses the same general skill. DLV recognizes that an earlier answer in this family of tasks was incorrect, and changes its strategy: instead of merely supplying another hint, it invites comparison with the previous case. This is interpretable adaptation based on recorded decisions, not a psychological label or an opaque prediction of student ability.

## 8:05–9:15 — Explain the limits of the AI tutor itself

**On screen:** Four plain limitations, matching `MATRIZ_RETO07.md`.

**Suggested narration:**

> Sexto Sentido is an example of symbolic artificial intelligence, not a generative chatbot. It operates on curated teaching scenarios. It cannot verify live web sources, detect manipulated audio, or make sensitive decisions for students. It does not diagnose cognition, and it is not intended to replace teachers or professionals. Our 25 integration checks establish that selected software scenarios work as intended; they do not establish improved learning outcomes in real classrooms. That would require a separate educational evaluation.

## 9:15–10:00 — Closing

**On screen:** Architecture summary, three green demonstration checks, and *AI should support judgment, not replace it.*

**Suggested narration:**

> A responsible AI learning tool should make reasoning visible. Sexto Sentido gives students a safe place to practice checking claims, reconsidering first impressions, and deciding when human verification matters. Its strength is not a spectacular interface. It is a small, transparent backend where the intervention can be traced to explicit pedagogical rules. The next step is to evaluate how well this practice supports students and teachers.

## Production checklist

- Record **real** `sexto_35.py + DLV` outputs. Scripted inputs are not evidence from real pupils.
- Never claim that a simulated school message was independently checked online.
- Show `accion`, `motivo`, and where present `modo_ayuda`.
- Mention that the 35 activities include 23 foundational reasoning cases and 12 AI-literacy cases.
- Do not present the 25 software tests as an educational impact study.
- Use large terminal typography and subtitles; blur any personal data accidentally visible.
- Check the official time limit and submission requirements before editing the final cut.
