#!/usr/bin/env python3
"""Interfaz local para el tutor estable. Sin dependencias externas."""
import argparse
import copy
import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STABLE = ROOT / 'KB_SextoSentido_35_ESTABLE_20261104_104711'
spec = importlib.util.spec_from_file_location('sexto_motor', STABLE / 'sexto_35.py')
ss = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ss)
DLV_FILES = tuple(ss.DLV_INPUTS)


class Tutor:
    def __init__(self, data):
        self.data = data.resolve()
        self.data.mkdir(parents=True, exist_ok=True)
        ss.HIST = self.data / 'historial_interfaz.dlv'
        ss.REFLEX = self.data / 'reflexiones_interfaz.jsonl'
        ss.DLV_INPUTS = [str(ss.HIST) if f == 'historial_sexto_35.dlv'
                         else str(STABLE / f) for f in DLV_FILES]
        self.bank = ss.cargar_banco()
        self.rules, self.goals = ss.cargar_politica(self.bank)
        self.states = {}

    def state(self, token):
        if token not in self.states:
            path = self.data / (token + '.json')
            self.states[token] = json.loads(path.read_text()) if path.exists() else {
                'stage': 'catalogo', 'student': 'demo_presentacion'}
        return self.states[token]

    def save(self, token):
        path = self.data / (token + '.json')
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(self.states[token], ensure_ascii=False), encoding='utf-8')
        os.replace(tmp, path)

    def decision(self, state):
        p = self.bank[state['pid']]
        # La función original llama al ejecutable DLV; no se simula su salida.
        ss.actualizar(contexto=(state['student'], state['session'], state['pid']))
        with contextlib.redirect_stdout(io.StringIO()):
            action, reason, mode = ss.decidir(state['student'], state['session'], state['pid'], self.bank)
        observed = next((e for e in p.get('errores_previsibles', []) if e['etiqueta'] == reason), None)
        return {'action': action, 'reason': reason, 'mode': mode,
                'message': ss.MENSAJES.get(action, action),
                'explanation': observed['descripcion'] if observed else ss.MOTIVOS.get(reason, reason)}

    def reflection(self, s, text, stage):
        if not isinstance(text, str) or len(text) > 3000:
            raise ValueError('La reflexión admite hasta 3000 caracteres.')
        if text.strip():
            with ss.REFLEX.open('a', encoding='utf-8') as f:
                f.write(json.dumps({'alumno': s['student'], 'sesion': s['session'],
                    'problema': s['pid'], 'etapa': stage, 'texto': text.strip()}, ensure_ascii=False) + '\n')

    def act(self, token, route, body):
        # Si DLV falla, no dejar una transición a medias. El servidor atiende
        # solicitudes en serie; el alumno puede volver a enviar su respuesta.
        before = copy.deepcopy(self.state(token))
        paths = (ss.HIST, ss.REFLEX, self.data / (token + '.json'))
        snapshots = {p: p.read_bytes() if p.exists() else None for p in paths}
        try:
            return self._act(token, route, body)
        except Exception:
            self.states[token] = before
            for path, content in snapshots.items():
                if content is None:
                    if path.exists():
                        path.unlink()
                else:
                    path.write_bytes(content)
            raise

    def _act(self, token, route, body):
        s = self.state(token)
        if route == '/api/start':
            student, pid = body.get('student', ''), body.get('pid')
            if not isinstance(student, str) or not ss.ID_ALUMNO.fullmatch(student) or len(student) > 40:
                raise ValueError('Usa un seudónimo de hasta 40 caracteres: minúsculas, números y _. Empieza con una letra.')
            if type(pid) is not int or pid not in self.bank:
                raise ValueError('Selecciona una actividad válida.')
            if s['stage'] not in ('catalogo', 'resultado'):
                raise ValueError('Termina o vuelve al banco antes de iniciar otra actividad.')
            session = max((r[0] for r in ss.registros(student)), default=0) + 1
            s.clear()
            s.update(stage='inicial', student=student, pid=pid, session=session)
            ss.actualizar([f'alumno({student}).'], contexto=(student, session, pid))
            s['decision'] = self.decision(s)
        elif route == '/api/answer':
            if s['stage'] not in ('inicial', 'revision'):
                raise ValueError('Esta respuesta ya fue registrada.')
            option, confidence = body.get('option'), body.get('confidence')
            p = self.bank[s['pid']]
            if type(option) is not int or option not in [int(o['id']) for o in p['opciones']]:
                raise ValueError('Selecciona una opción.')
            if type(confidence) is not int or not 0 <= confidence <= 100:
                raise ValueError('La confianza debe estar entre 0 y 100.')
            phase = 'inicial' if s['stage'] == 'inicial' else 'final'
            ss.guardar_respuesta(s['student'], s['session'], p, phase, option, confidence)
            s[phase] = {'option': option, 'confidence': confidence}
            s['decision'] = self.decision(s)
            if phase == 'final':
                s['stage'] = 'resultado'
            elif ss.clasificar(p, option) != 'correcta':
                s['stage'] = 'ayuda'
            elif s['decision']['action'] == 'pedir_justificacion':
                s['stage'] = 'justificacion'
            else:
                s['stage'] = 'resultado'
        elif route == '/api/continue':
            if s['stage'] not in ('ayuda', 'justificacion'):
                raise ValueError('No hay una ayuda pendiente.')
            self.reflection(s, body.get('reflection', ''), 'antes_revision')
            action = s['decision']['action']
            ss.actualizar([f"intervencion_hecha({s['student']},{s['session']},{s['pid']},{action})."])
            previous = s['stage']
            s['decision'] = self.decision(s)
            expected = 'pedir_revision' if previous == 'ayuda' else 'proponer_nuevo_caso'
            if s['decision']['action'] != expected:
                raise RuntimeError('El motor devolvió una acción inesperada.')
            s['stage'] = 'revision' if previous == 'ayuda' else 'resultado'
        elif route == '/api/finish':
            if s['stage'] != 'resultado':
                raise ValueError('Primero completa la actividad.')
            self.reflection(s, body.get('reflection', ''), 'final')
            student = s['student']
            s.clear()
            s.update(stage='catalogo', student=student)
        elif route == '/api/catalog':
            # Volver al banco conserva los hechos ya registrados.
            student = s['student']
            s.clear()
            s.update(stage='catalogo', student=student)
        else:
            raise ValueError('Acción desconocida.')
        self.save(token)
        return self.public(token)

    def public(self, token):
        s = dict(self.state(token))
        student = s['student']
        records = ss.registros(student)
        s['completed'] = sorted({p for se, p, phase, op in records
                                if phase == 'final' or (phase == 'inicial' and ss.clasificar(self.bank[p], op) == 'correcta')})
        s['catalog'] = [{'id': n, 'title': p['titulo'], 'family': p['familia'],
                         'new': p['nuevo']} for n, p in self.bank.items()]
        if 'pid' in s:
            p = self.bank[s['pid']]
            s['activity'] = {'id': p['id'], 'title': p['titulo'], 'text': p['enunciado'],
                             'question': p.get('pregunta', ''), 'options': p['opciones']}
            if s['stage'] == 'ayuda':
                s['hint'] = p['pistas'][0]
                if s['decision']['action'] == 'comparar_objetivo_anterior':
                    matches = [(se, pid) for se, pid, _ in ss.errores_previos(student)
                               if se < s['session'] and pid != s['pid'] and self.goals.get(pid) == self.goals.get(s['pid'])]
                    if matches:
                        pid = max(matches)[1]
                        s['previous'] = f"Actividad {pid}: {self.bank[pid]['titulo']}"
            if s['stage'] == 'resultado':
                s['solution'] = {'option': int(p['clave_docente']['correcta_id']), 'explanation': p['explicacion'],
                                 'limit': p.get('limite_ia_que_ensena', ''),
                                 'reflection': p.get('reflexion_final', '¿Qué comprobación te ayudó a decidir?')}
        return s


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if args and str(args[0]).startswith('POST'):
            print(fmt % args, flush=True)

    def reply(self, status, payload, content_type='application/json; charset=utf-8'):
        data = json.dumps(payload, ensure_ascii=False).encode() if not isinstance(payload, bytes) else payload
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
        if getattr(self, 'new_cookie', False):
            self.send_header('Set-Cookie', f'sexto_session={self.token}; HttpOnly; SameSite=Strict; Path=/')
        self.end_headers()
        self.wfile.write(data)

    def identify(self):
        if self.headers.get('Host') not in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'):
            raise ValueError('Dirección local no válida.')
        cookie = SimpleCookie(self.headers.get('Cookie', ''))
        token = cookie['sexto_session'].value if 'sexto_session' in cookie else ''
        self.new_cookie = not bool(re.fullmatch('[a-f0-9]{32}', token))
        self.token = uuid.uuid4().hex if self.new_cookie else token

    def do_GET(self):
        try:
            self.identify()
            if self.path == '/api/state':
                return self.reply(200, self.server.tutor.public(self.token))
            files = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'application/javascript'),
                     '/style.css': ('style.css', 'text/css')}
            if self.path not in files:
                return self.reply(404, {'error': 'No encontrado.'})
            name, mime = files[self.path]
            self.reply(200, (HERE / name).read_bytes(), mime + '; charset=utf-8')
        except ValueError as e:
            self.reply(400, {'error': str(e)})

    def do_POST(self):
        try:
            self.identify()
            origin = self.headers.get('Origin')
            if origin and origin not in (f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'):
                raise ValueError('Origen no permitido.')
            length = int(self.headers.get('Content-Length', '0'))
            if length < 0 or length > 16000:
                raise ValueError('Solicitud demasiado larga.')
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError('Solicitud no válida.')
            self.reply(200, self.server.tutor.act(self.token, self.path, body))
        except (ValueError, KeyError) as e:
            self.reply(400, {'error': str(e)})
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as e:
            print('Error del motor:', e, file=sys.stderr)
            self.reply(503, {'error': 'No se pudo consultar DLV. La respuesta no se guardó. Revisa la terminal y vuelve a intentarlo.'})


def main():
    parser = argparse.ArgumentParser(description='Ventana local de Sexto Sentido')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--datos', type=Path, default=ROOT / 'datos_interfaz')
    args = parser.parse_args()
    os.environ['PATH'] = str(ROOT / 'herramientas/dlv/bin') + os.pathsep + os.environ.get('PATH', '')
    if not shutil.which('dlv'):
        parser.error('No se encontró DLV.')
    try:
        server = HTTPServer(('127.0.0.1', args.port), Handler)
    except OSError as e:
        parser.exit(1, f'No se pudo abrir el puerto {args.port}: {e}. Prueba --port 8766.\n')
    server.tutor = Tutor(args.datos)
    print(f'\nSexto Sentido · Interfaz local\nAbre http://127.0.0.1:{server.server_port}\nCtrl+C para cerrar.\n', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nInterfaz cerrada. Progreso conservado.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
