#!/usr/bin/env python3
"""Pruebas del adaptador gráfico con DLV real y datos temporales."""
import json
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
