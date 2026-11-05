#!/usr/bin/env python3
"""Pruebas del adaptador gráfico con DLV real y datos temporales."""
import json
import csv
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import servidor as gui


class FlujosInterfaz(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='sexto_gui_test_')
        self.addCleanup(self.tmp.cleanup)
        os.environ['PATH'] = str(gui.ROOT / 'herramientas/dlv/bin') + os.pathsep + os.environ['PATH']
        self.tutor = gui.Tutor(Path(self.tmp.name))
        self.token = 'a' * 32

    def start(self, pid, student='prueba_visual'):
        return self.tutor.act(self.token, '/api/start', {'pid': pid, 'student': student})

    def answer(self, option, confidence=90):
        return self.tutor.act(self.token, '/api/answer', {'option': option, 'confidence': confidence})

    def continue_(self):
        return self.tutor.act(self.token, '/api/continue', {'reflection': 'Reflexión ficticia de prueba.'})

    def finish(self):
        return self.tutor.act(self.token, '/api/finish', {'reflection': 'Cierre ficticio.'})

    def test_35_aciertos_iniciales_y_justificacion(self):
        for pid, p in self.tutor.bank.items():
            with self.subTest(pid=pid):
                s = self.start(pid)
                self.assertNotIn('solution', s)
                self.assertNotIn('clave_docente', json.dumps(s))
                s = self.answer(int(p['clave_docente']['correcta_id']), 20)
                self.assertEqual(s['stage'], 'justificacion')
                self.assertNotIn('solution', s)
                s = self.continue_()
                self.assertEqual(s['stage'], 'resultado')
                self.assertEqual(s['solution']['option'], p['clave_docente']['correcta_id'])
                s = self.finish()
                self.assertEqual(s['student'], 'prueba_visual')
        self.assertEqual(len(s['completed']), 35)

    def test_35_errores_ayuda_y_revision_correcta(self):
        for pid, p in self.tutor.bank.items():
            with self.subTest(pid=pid):
                self.start(pid, 'prueba_' + str(pid))
                s = self.answer(int(p['clave_docente']['intuitiva_s1_id']))
                self.assertEqual(s['stage'], 'ayuda')
                self.assertTrue(s['hint'])
                self.assertNotIn('solution', s)
                s = self.continue_()
                self.assertEqual(s['stage'], 'revision')
                s = self.answer(int(p['clave_docente']['correcta_id']), 80)
                self.assertEqual(s['decision']['action'], 'resumir_revision')
                self.assertNotEqual(s['inicial']['option'], s['final']['option'])
                self.finish()

    def test_segundos_distractores_y_revision_incorrecta(self):
        for pid in range(24, 36):
            p = self.tutor.bank[pid]
            self.start(pid, 'otra_' + str(pid))
            wrong = int(p['errores_previsibles'][1]['opcion_id'])
            s = self.answer(wrong, 20)
            self.assertEqual(s['decision']['mode'], 'pista_breve')
            self.continue_()
            s = self.answer(wrong, 30)
            self.assertEqual(s['decision']['action'], 'reexaminar_error')
            self.finish()

    def test_transferencia_y_prioridad_de_precaucion(self):
        for first, second, action in [(24, 26, 'comparar_objetivo_anterior'), (28, 29, 'detener_y_verificar')]:
            student = 'transferencia_' + str(first)
            self.start(first, student)
            self.answer(int(self.tutor.bank[first]['clave_docente']['intuitiva_s1_id']))
            self.continue_()
            self.answer(int(self.tutor.bank[first]['clave_docente']['correcta_id']))
            self.finish()
            self.start(second, student)
            s = self.answer(int(self.tutor.bank[second]['clave_docente']['intuitiva_s1_id']))
            self.assertEqual(s['decision']['action'], action)
            if second == 26:
                self.assertIn('24', s['previous'])
            self.continue_()
            self.answer(int(self.tutor.bank[second]['clave_docente']['correcta_id']))
            self.finish()

    def test_validacion_duplicados_y_recuperacion(self):
        self.start(25)
        for option, confidence in [(False, 90), (9, 90), (1, -1), (1, 101)]:
            with self.assertRaises(ValueError):
                self.answer(option, confidence)
        self.assertEqual(self.tutor.public(self.token)['stage'], 'inicial')
        self.answer(1)
        history = gui.ss.HIST.read_bytes()
        with self.assertRaises(ValueError):
            self.answer(2)
        self.assertEqual(gui.ss.HIST.read_bytes(), history)
        self.tutor = gui.Tutor(Path(self.tmp.name))
        self.assertEqual(self.tutor.public(self.token)['stage'], 'ayuda')
        self.continue_()
        self.answer(2)
        self.finish()

    def test_fallo_dlv_no_guarda_respuesta_parcial(self):
        self.start(25)
        history = gui.ss.HIST.read_bytes()
        with patch.object(self.tutor, 'decision', side_effect=RuntimeError('Fallo DLV de prueba')):
            with self.assertRaises(RuntimeError):
                self.answer(1)
        self.assertEqual(gui.ss.HIST.read_bytes(), history)
        self.assertEqual(self.tutor.public(self.token)['stage'], 'inicial')
        self.assertEqual(self.answer(1)['stage'], 'ayuda')

    def test_razon_inicial_precede_dlv_y_se_conserva(self):
        self.start(25)
        original = self.tutor.decision
        def observing(state):
            reflections = [json.loads(l) for l in gui.ss.REFLEX.read_text().splitlines()]
            self.assertEqual(reflections[-1]['etapa'], 'justificacion_inicial')
            self.assertEqual(reflections[-1]['texto'], 'Los porcentajes se cancelan.')
            return original(state)
        with patch.object(self.tutor, 'decision', side_effect=observing):
            self.tutor.act(self.token, '/api/answer', {
                'option': 1, 'confidence': 90, 'reason': 'Los porcentajes se cancelan.'})
        self.continue_()
        s = self.tutor.act(self.token, '/api/answer', {
            'option': 2, 'confidence': 75, 'reason': 'El descuento usa el precio aumentado.'})
        self.assertEqual(s['inicial']['reason'], 'Los porcentajes se cancelan.')
        self.finish()
        row = self.tutor.report('prueba_visual')[0]
        self.assertEqual(row['inicial']['reason'], 'Los porcentajes se cancelan.')
        self.assertEqual(row['final']['reason'], 'El descuento usa el precio aumentado.')
        self.assertEqual(row['final_reflection'], 'Cierre ficticio.')
        self.assertEqual(row['interventions'][0]['action'], 'verificar_operaciones')
        self.assertTrue(row['finished'])

    def test_recorrido_completo_cuatro_casos_y_resumen(self):
        s = self.tutor.act(self.token, '/api/journey', {'student': 'recorrido_demo'})
        route_id = s['journey']['id']
        for index, pid in enumerate([25, 29, 31, 34]):
            self.assertEqual(s['pid'], pid)
            self.assertEqual(s['journey']['index'], index)
            self.assertEqual(s['journey']['id'], route_id)
            p = self.tutor.bank[pid]
            # Incluye un acierto inicial con duda y tres revisiones.
            choice = p['clave_docente']['correcta_id'] if pid == 31 else p['clave_docente']['intuitiva_s1_id']
            s = self.answer(int(choice), 20 if pid == 31 else 90)
            s = self.continue_()
            if pid != 31:
                s = self.answer(int(p['clave_docente']['correcta_id']))
            self.assertEqual(s['stage'], 'resultado')
            s = self.finish()
        self.assertEqual(s['stage'], 'resumen')
        self.assertTrue(s['journey']['completed'])
        self.assertEqual([r['pid'] for r in s['report']], [25, 29, 31, 34])
        self.assertTrue(all(r['finished'] for r in s['report']))
        self.assertEqual(len(self.tutor.bank), 35)
        with self.assertRaises(ValueError):
            self.finish()

    def test_pausa_recarga_y_reanudacion_del_recorrido(self):
        self.tutor.act(self.token, '/api/journey', {'student': 'pausa_demo'})
        self.tutor.act(self.token, '/api/answer', {'option': 1, 'confidence': 90, 'reason': 'Mi razón inicial.'})
        s = self.tutor.act(self.token, '/api/catalog', {})
        self.assertEqual(s['stage'], 'catalogo')
        self.assertEqual(s['paused']['pid'], 25)
        self.assertNotIn('inicial', s['paused'])
        self.tutor = gui.Tutor(Path(self.tmp.name))
        s = self.tutor.act(self.token, '/api/resume', {})
        self.assertEqual(s['stage'], 'ayuda')
        self.assertEqual(s['inicial']['reason'], 'Mi razón inicial.')
        self.continue_()
        self.answer(2)
        s = self.finish()
        self.assertEqual(s['pid'], 29)

    def test_reserva_intentos_sin_colision_entre_pestanas(self):
        a = self.start(25)
        b = self.tutor.act('b' * 32, '/api/start', {'student': 'prueba_visual', 'pid': 25})
        self.assertNotEqual(a['session'], b['session'])
        self.answer(1)
        self.tutor.act('b' * 32, '/api/answer', {'option': 2, 'confidence': 90, 'reason': ''})
        self.assertEqual(len(self.tutor.report('prueba_visual')), 2)

    def test_csv_unicode_campos_y_formulas_como_texto(self):
        self.start(25)
        malicious = '=HYPERLINK("https://ejemplo.test","hola")\nCon coma, y acento: cálculo.'
        self.tutor.act(self.token, '/api/answer', {'option': 2, 'confidence': 90, 'reason': malicious})
        self.finish()
        binary = self.tutor.csv_report(self.token)
        self.assertTrue(binary.startswith(b'\xef\xbb\xbf'))
        rows = list(csv.DictReader(io.StringIO(binary.decode('utf-8-sig'))))
        self.assertEqual(rows[0]['razon_inicial'], "'" + malicious)
        self.assertEqual(rows[0]['estado'], 'Finalizado')
        self.assertEqual(rows[0]['confianza_inicial'], '90')
        self.assertEqual(rows[0]['respuesta_inicial'], self.tutor.bank[25]['opciones'][1]['texto'])
        self.assertEqual(rows[0]['opcion_revisada'], '')

    def test_reporte_filtra_seudonimos_y_no_califica_razones(self):
        self.start(25, 'primero')
        s1 = self.tutor.act(self.token, '/api/answer', {'option': 1, 'confidence': 90, 'reason': 'Una razón.'})
        self.continue_()
        self.answer(2)
        self.finish()
        self.start(25, 'segundo')
        s2 = self.tutor.act(self.token, '/api/answer', {'option': 1, 'confidence': 90, 'reason': 'Otra razón.'})
        self.assertEqual(s1['decision'], s2['decision'])
        self.assertEqual(len(s2['report']), 1)
        self.assertEqual(s2['report'][0]['student'], 'segundo')
        self.assertNotIn('primero', self.tutor.csv_report(self.token).decode('utf-8-sig'))

    def test_razon_invalida_y_fallo_dlv_revierten_todos_los_registros(self):
        self.start(25)
        before = {p.name: p.read_bytes() for p in Path(self.tmp.name).iterdir()}
        for reason in [None, 45, 'x' * 3001]:
            with self.assertRaises(ValueError):
                self.tutor.act(self.token, '/api/answer', {'option': 1, 'confidence': 90, 'reason': reason})
        with patch.object(self.tutor, 'decision', side_effect=RuntimeError('Fallo simulado')):
            with self.assertRaises(RuntimeError):
                self.tutor.act(self.token, '/api/answer', {'option': 1, 'confidence': 90, 'reason': 'No debe quedar guardada.'})
        after = {p.name: p.read_bytes() for p in Path(self.tmp.name).iterdir()}
        self.assertEqual(before, after)
        self.assertEqual(self.tutor.report('prueba_visual'), [])

    def test_datos_anteriores_se_recuperan_sin_inventar_razones(self):
        p = self.tutor.bank[25]
        gui.ss.actualizar(['alumno(anterior).'], contexto=('anterior', 1, 25))
        gui.ss.guardar_respuesta('anterior', 1, p, 'inicial', 1, 90)
        gui.ss.guardar_respuesta('anterior', 1, p, 'final', 2, 80)
        row = self.tutor.report('anterior')[0]
        self.assertTrue(row['legacy'])
        self.assertFalse(row['finished'])
        self.assertEqual(row['inicial']['reason'], '')
        self.assertEqual(row['final']['confidence'], 80)


if __name__ == '__main__':
    unittest.main(verbosity=2)
