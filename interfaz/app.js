'use strict';
let state, view = 'inicio', filter = 'ia', busy = false;
const app = document.querySelector('#app');
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const themes = {24:'Impresión y evidencia',25:'Verificación de cálculos',26:'Evidencia de aprendizaje',27:'Comparar procedimientos',28:'Fuentes y referencias',29:'Información sin verificar',30:'Sesgos y equidad',31:'Privacidad y datos',32:'Medios sintéticos',33:'Supervisión humana',34:'Incertidumbre',35:'Integridad académica'};
const descriptions = {25:'¿Una explicación amable también puede equivocarse?',29:'Un mensaje urgente. Una decisión antes de compartir.',24:'¿Una buena presentación demuestra buenos resultados?'};
function notify(message) { const n=document.querySelector('#notice'); n.textContent=message; n.hidden=false; clearTimeout(notify.timer); notify.timer=setTimeout(()=>n.hidden=true,8000); }
async function request(route, body) {
  const response = await fetch(route,{credentials:'same-origin',headers:body?{'Content-Type':'application/json'}:{},method:body?'POST':'GET',body:body?JSON.stringify(body):undefined});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'No se pudo completar la solicitud.');
  return data;
}
async function perform(route,body,after) {
  if (busy) return;
  busy=true; app.setAttribute('aria-busy','true');
  app.querySelectorAll('button').forEach(b=>b.disabled=true);
  try { state=await request(route,body); if(state.stage==='resumen') view='resumen'; else if(state.stage!=='catalogo') view='actividad'; if(after) after(); render(); app.focus({preventScroll:true}); window.scrollTo({top:0,behavior:'instant'}); }
  catch(error) { notify(error.message || 'No se pudo conectar. Comprueba que la terminal siga abierta.'); }
  finally { busy=false; app.removeAttribute('aria-busy'); app.querySelectorAll('button').forEach(b=>b.disabled=false); }
}
function studentField(){return `<div class="student-row"><label for="student">Tu seudónimo</label><input id="student" value="${esc(state.student)}" maxlength="40" required pattern="[a-z][a-z0-9_]*" spellcheck="false" autocomplete="off"><span>Sin nombres ni datos personales.</span></div>`;}
function card(id, detailed=false) {
 const p=state.catalog.find(p=>p.id===id), done=state.completed.includes(id);
 return `<button class="case-card" data-start="${id}"><span class="badge ${id===29?'orange':id===24?'blue':''}">${esc(themes[id] || 'Razonamiento lógico')}</span><h3>${esc(p.title)}</h3>${detailed?'':`<p>${esc(descriptions[id] || '')}</p>`}<span class="card-bottom"><span>CASO ${String(id).padStart(2,'0')}${done?' · Completado':''}</span><span aria-hidden="true">↗</span></span></button>`;
}
function home(){return `${resumeBanner()}<section class="hero"><div class="hero-copy"><span class="eyebrow">PIENSA · CONTRASTA · DECIDE</span><h1>Antes de creer,<br>aprende a <em>comprobar.</em></h1><p>Una respuesta convincente no siempre es una respuesta correcta. Pon a prueba tu criterio, descubre qué falta verificar y vuelve a decidir.</p><div class="hero-actions"><button class="primary" data-journey>Empezar el recorrido <span aria-hidden="true">→</span></button><button class="secondary" data-go="banco">Explorar el banco</button></div><span class="small-note">Casos ficticios. Decisiones tuyas. Ayuda que puedes entender.</span></div><div class="illustration" aria-hidden="true"><div class="orbit"></div><div class="center-symbol">?</div><span class="float-tag tag1"><b>01</b> Cuestiona la respuesta</span><span class="float-tag tag2"><b>02</b> Busca la evidencia</span><span class="float-tag tag3"><b>03</b> Revisa tu decisión</span><span class="spark">✳</span></div></section><section class="process" aria-label="Cómo funciona"><div class="process-item"><span class="process-number">01</span><div><strong>Elige y explica tu primera razón</strong><p>Tu primera respuesta es el punto de partida.</p></div></div><div class="process-item"><span class="process-number">02</span><div><strong>Recibe una pista explicable</strong><p>Conoce por qué el tutor te propone esa ayuda.</p></div></div><div class="process-item"><span class="process-number">03</span><div><strong>Revisa y descubre el porqué</strong><p>Compara tus decisiones y su explicación.</p></div></div></section><section><div class="section-heading"><h2>Tres formas de empezar</h2><p>También puedes elegir un caso libre</p></div>${studentField()}${journeyIntro()}<div class="cards">${[25,29,24].map(id=>card(id)).join('')}</div></section>`;}
function catalog(){const items=state.catalog.filter(p=>filter==='todos'||(filter==='ia'?p.new:!p.new));return `${resumeBanner()}<section class="catalog"><div class="catalog-title"><span class="eyebrow">BANCO DE ACTIVIDADES</span><h1>Un caso. Otra forma de pensar.</h1><p>Explora situaciones de uso de IA o profundiza en los fundamentos del razonamiento.</p></div>${studentField()}<div class="filters" role="group" aria-label="Filtrar actividades">${[['ia','IA y vida escolar · 12'],['logica','Fundamentos · 23'],['todos','Todas · 35']].map(([id,text])=>`<button class="filter ${filter===id?'active':''}" aria-pressed="${filter===id}" data-filter="${id}">${text}</button>`).join('')}</div><div class="cards">${items.map(p=>card(p.id,true)).join('')}</div></section>`;}
function heading(){const a=state.activity,n=['inicial'].includes(state.stage)?1:['ayuda','justificacion','revision'].includes(state.stage)?2:3;return `${journeyProgress()}<button class="back-link" id="back">← Volver al banco</button><div class="activity-heading"><div><span class="eyebrow">CASO ${String(a.id).padStart(2,'0')} · ${esc(themes[a.id] || 'RAZONAMIENTO')}</span><h1>${esc(a.title)}</h1></div><div class="steps" aria-label="Progreso de la actividad">${['Tu decisión','Una nueva mirada','Reflexión'].map((t,i)=>`<span class="step ${n===i+1?'active':''}" ${n===i+1?'aria-current="step"':''}><i>${i+1}</i>${t}</span>`).join('')}</div></div>`;}
function trace(){const d=state.decision;return `<details class="trace"><summary>¿Cómo tomó esta decisión el tutor?</summary><p>${esc(d.explanation)}</p><code>Motor: ASP / DLV\nAcción: ${esc(d.action)}\nMotivo: ${esc(d.reason)}${d.mode?'\nModo de ayuda: '+esc(d.mode):''}</code></details>`;}
function exercise(){const revision=state.stage==='revision',a=state.activity;return `${heading()}<form id="answer-form"><div class="exercise"><article class="scenario"><span class="eyebrow">LEE EL ESCENARIO</span><p class="scenario-text">${esc(a.text)}</p>${a.question?`<p class="question">${esc(a.question)}</p>`:''}</article><section class="answer-panel"><h2>${revision?'Míralo de nuevo.':'¿Qué piensas tú?'}</h2><p>${revision?'Puedes mantener o cambiar tu elección después de la pista.':'Elige la opción que consideres mejor justificada.'}</p><fieldset class="options"><legend class="sr-only">Selecciona tu respuesta</legend>${a.options.map(o=>`<label class="option"><input type="radio" name="option" value="${o.id}" required ${revision&&state.inicial.option===Number(o.id)?'checked':''}><span>${esc(o.texto)}</span></label>`).join('')}</fieldset><div class="confidence"><label for="confidence">¿Cuánta confianza tienes en esta elección?<output id="confidence-value" for="confidence">${revision?state.inicial.confidence:50}%</output></label><input type="range" id="confidence" min="0" max="100" step="1" value="${revision?state.inicial.confidence:50}"><div class="range-labels"><span>0 · Ninguna</span><span>100 · Total</span></div></div><div class="reason-field"><label for="reason">${revision?'¿Qué razón sostiene ahora tu elección?':'¿Por qué elegiste esa respuesta?'} <span>Opcional · Antes de recibir ${revision?'la explicación':'cualquier ayuda'}</span></label><textarea id="reason" maxlength="3000" placeholder="Escribe tu razón, aunque todavía tengas dudas…"></textarea></div><button class="primary" type="submit">${revision?'Registrar mi revisión':'Consultar al tutor'} <span aria-hidden="true">→</span></button><p class="privacy">Tu confianza se registra; no determina si una respuesta es correcta.</p></section></div></form>`;}
function help(){const justification=state.stage==='justificacion';return `${heading()}<section class="tutor-layout"><article class="tutor-card"><span class="eyebrow">UNA PAUSA PARA PENSAR</span><h2>${esc(state.decision.message)}</h2><p>${esc(state.decision.explanation)}</p>${state.previous?`<p><strong>Conecta con tu experiencia:</strong> ${esc(state.previous)}. ¿Qué comprobación necesitabas en ambos casos?</p>`:''}${justification?'':`<div class="hint"><span class="eyebrow">TU PISTA</span><p>${esc(state.hint)}</p></div>`}</article>${trace()}<form id="reflection-form" class="reflection-panel"><label for="reflection">${justification?'¿Cómo justificarías tu elección?':'¿Qué necesitas comprobar antes de volver a decidir?'} <span class="small-note">Reflexión opcional · Sin datos personales</span></label><textarea id="reflection" maxlength="3000" placeholder="Escribe aquí tu reflexión…"></textarea><div class="bottom-actions"><button class="primary" type="submit">${justification?'Ver la explicación':'Revisar mi respuesta'} <span aria-hidden="true">→</span></button></div></form></section>`;}
function responseSummary(record,title){const o=state.activity.options.find(o=>Number(o.id)===record.option);return `<div><span class="eyebrow">${title}</span><p>${esc(o.texto)}</p><strong>Confianza declarada: ${record.confidence}%</strong><div class="reason-quote"><span>Tu razón ${title.includes('INICIAL')?'antes de la ayuda':'antes de la explicación'}</span><p>${esc(record.reason || 'Sin justificación registrada.')}</p></div></div>`;}
function result(){const sol=state.solution,last=state.final||state.inicial,ok=last.option===sol.option;return `${heading()}<section class="tutor-layout"><div class="result-banner"><span class="result-icon" aria-hidden="true">${ok?'✓':'◎'}</span><div><h3>${ok?(state.final?'Revisaste tu decisión. Ahora mira por qué.':'Tu elección coincide con la respuesta de referencia.'):'Hay algo más que revisar.'}</h3><p>${state.final?'Tus dos respuestas se conservaron para compararlas.':'Consulta las razones que respaldan esta conclusión.'}</p></div></div><div class="comparison">${responseSummary(state.inicial,'TU DECISIÓN INICIAL')}${state.final?responseSummary(state.final,'TU DECISIÓN REVISADA'):`<div><span class="eyebrow">TU RECORRIDO</span><p>Acertaste en la primera elección. El siguiente paso es examinar la explicación y sus límites.</p><strong>Comprobar también importa cuando aciertas.</strong></div>`}</div><article class="solution"><h2>La explicación, paso a paso.</h2><p>${esc(sol.explanation)}</p>${sol.limit?`<div class="limit-note"><strong>El límite que ilustra este caso</strong><br>${esc(sol.limit)}</div>`:''}</article>${trace()}<form id="reflection-form" class="reflection-panel"><label for="reflection">${esc(sol.reflection)}<span class="small-note">Reflexión final opcional · Tu texto queda guardado, sin evaluación automática.</span></label><textarea id="reflection" maxlength="3000" placeholder="¿Qué te llevas de este caso?"></textarea><div class="bottom-actions"><button class="primary" type="submit">${finishLabel()} <span aria-hidden="true">→</span></button></div></form></section>`;}
function resumeBanner() {
  if (!state.paused) return '';
  return `<aside class="resume-banner"><div><strong>Tienes una actividad pausada</strong><p>${esc(state.paused.title)}${state.paused.journey ? ' · Recorrido guiado' : ''}</p></div><button class="secondary" id="resume">Retomar actividad →</button></aside>`;
}
function journeyIntro() {
  return `<section class="journey-intro"><div><span class="eyebrow">RECORRIDO GUIADO · 4 CASOS</span><h3>Cuatro decisiones para usar la IA con criterio.</h3><p>Cálculo → información sin verificar → privacidad → incertidumbre.</p></div><span class="journey-note">Al terminar recibirás un resumen de tus decisiones y razones.</span></section>`;
}
function journeyProgress() {
  if (!state.journey || state.journey.completed) return '';
  return `<div class="journey-progress"><span>Recorrido guiado · Caso ${state.journey.index + 1} de 4</span><div>${state.journey.pids.map((pid,i)=>`<span class="journey-dot ${i<=state.journey.index?'reached':''}" aria-label="Caso ${i+1}${i===state.journey.index?', actual':''}"></span>`).join('')}</div></div>`;
}
function finishLabel() {
  if (!state.journey) return 'Guardar y explorar otro caso';
  return state.journey.index < 3 ? 'Guardar y continuar al siguiente caso' : 'Terminar y ver mi resumen';
}
function summaryChoice(choice, label) {
  if (!choice) return `<div><h3>${label}</h3><p class="muted">Sin revisión registrada.</p></div>`;
  return `<div><h3>${label}</h3><p>${esc(choice.text)}</p><strong>Confianza: ${choice.confidence ?? 'Sin dato'}${choice.confidence===null?'':'%'}</strong><blockquote>${esc(choice.reason || 'Sin justificación registrada.')}</blockquote></div>`;
}
function summary() {
  const rows = state.report || [];
  const finished = rows.filter(r=>r.finished).length;
  const revised = rows.filter(r=>r.final).length;
  return `<section class="report"><div class="catalog-title"><span class="eyebrow">RESUMEN PARA ESTUDIANTE Y DOCENTE · V0.2.0</span><h1>Así cambió tu decisión.</h1><p>Registro de <strong>${esc(state.student)}</strong>. Un cierre de actividad documenta el recorrido; no demuestra por sí solo aprendizaje.</p></div>
  ${state.journey?.completed?'<div class="result-banner"><span class="result-icon">✓</span><div><h3>Terminaste los cuatro casos del recorrido.</h3><p>Revisa tus razones iniciales, las ayudas y tus decisiones finales.</p></div></div>':''}
  <div class="report-stats"><div><strong>${rows.length}</strong><span>Intentos con respuesta</span></div><div><strong>${finished}</strong><span>Intentos finalizados</span></div><div><strong>${revised}</strong><span>Revisiones registradas</span></div></div>
  <div class="report-tools"><a class="primary" href="/api/export.csv" download>Descargar registros (CSV) ↓</a><button class="secondary" id="print-report">Imprimir resumen</button><span>Incluye todos los intentos de este seudónimo. Las razones se conservan para revisión humana.</span></div>
  ${rows.length ? rows.map(r=>`<article class="report-attempt"><div class="report-attempt-heading"><div><span class="eyebrow">CASO ${r.pid} · INTENTO ${r.session}${r.journey?' · RECORRIDO GUIADO':''}</span><h2>${esc(r.title)}</h2></div><span class="badge">${r.finished?'Finalizado':r.legacy?'Registro anterior':'En curso'}</span></div>
  <div class="report-choices">${summaryChoice(r.inicial,'Decisión inicial · antes de la ayuda')}${summaryChoice(r.final,'Decisión revisada · antes de la explicación')}</div>
  <div class="report-help"><strong>Ayuda recibida</strong>${r.interventions?.length?r.interventions.map(i=>`<p>${esc(i.message)}${i.explanation?`<br><span>${esc(i.explanation)}</span>`:''}</p>`).join(''):'<p>Sin intervención de ayuda registrada.</p>'}${r.help_reflection?`<p><strong>Reflexión después de la ayuda:</strong> ${esc(r.help_reflection)}</p>`:''}</div>
  <div class="report-final"><strong>Reflexión final · después de la explicación</strong><p>${esc(r.final_reflection || 'Sin reflexión final registrada.')}</p></div>${r.legacy?'<p class="privacy">Registro anterior a v0.2.0. Puede no contener justificación previa ni constancia de cierre.</p>':''}</article>`).join(''):'<div class="solution"><h2>Tu recorrido empieza con una decisión.</h2><p>Aún no hay respuestas registradas para este seudónimo.</p><button class="secondary" data-go="inicio">Volver al inicio</button></div>'}
  </section>`;
}

function render(){
 const active=!['catalogo','resumen'].includes(state.stage);
 const reportVisible=view==='resumen'||state.stage==='resumen';
 app.innerHTML=reportVisible?summary():active?(['inicial','revision'].includes(state.stage)?exercise():['ayuda','justificacion'].includes(state.stage)?help():result()):(view==='banco'?catalog():home());
 document.querySelector('#breadcrumb').textContent=reportVisible?'Resumen de decisiones':active?'Actividad en curso':view==='banco'?'Banco de actividades':'Elige cómo empezar';
 document.querySelector('#progress-count').textContent=`${state.completed.length} / 35`;
 document.querySelector('#progress-bar').style.width=`${state.completed.length/35*100}%`;
 document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===(reportVisible?'resumen':active?'actividad':view)));
 app.querySelectorAll('[data-start]').forEach(b=>b.addEventListener('click',()=>{const input=document.querySelector('#student');if(!input.reportValidity())return;perform('/api/start',{pid:Number(b.dataset.start),student:input.value.trim()});}));
 app.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>{view=b.dataset.go;render();}));
 app.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{filter=b.dataset.filter;render();}));
 app.querySelectorAll('[data-journey]').forEach(b=>b.addEventListener('click',()=>{
   const input=document.querySelector('#student'); if(!input.reportValidity())return;
   perform('/api/journey',{student:input.value.trim()});
 }));
 document.querySelector('#resume')?.addEventListener('click',()=>perform('/api/resume',{}));
 document.querySelector('#print-report')?.addEventListener('click',()=>window.print());
 document.querySelector('#back')?.addEventListener('click',()=>perform('/api/catalog',{},()=>view='banco'));
 document.querySelector('#confidence')?.addEventListener('input',e=>document.querySelector('#confidence-value').textContent=e.target.value+'%');
 document.querySelector('#answer-form')?.addEventListener('submit',e=>{e.preventDefault();perform('/api/answer',{option:Number(new FormData(e.target).get('option')),confidence:Number(document.querySelector('#confidence').value),reason:document.querySelector('#reason').value});});
 document.querySelector('#reflection-form')?.addEventListener('submit',e=>{e.preventDefault();perform(state.stage==='resultado'?'/api/finish':'/api/continue',{reflection:document.querySelector('#reflection').value},()=>{if(state.stage==='catalogo')view='banco';});});
}
function navigate(target) {
  if (busy || !state) return;
  if (target === 'resumen' || ['catalogo', 'resumen'].includes(state.stage)) {
    view = target;
    if (state.stage === 'resumen' && target !== 'resumen') {
      perform('/api/catalog', {}, () => view = target);
    } else render();
  } else perform('/api/catalog', {}, () => view = target);
}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>navigate(b.dataset.view)));
document.querySelector('#brand').addEventListener('click',e=>{e.preventDefault();if(state)navigate('inicio');});
document.querySelector('#limits-button').addEventListener('click',()=>document.querySelector('#limits').showModal());
document.querySelectorAll('.dialog-close').forEach(b=>b.addEventListener('click',()=>document.querySelector('#limits').close()));
document.querySelector('#fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{notify('Usa la opción de pantalla completa de tu navegador.');}});
request('/api/state').then(data=>{state=data;if(state.stage==='resumen')view='resumen';render();}).catch(()=>{app.innerHTML='<h1>No pudimos conectar.</h1><p>Comprueba que el servidor siga abierto en la terminal y recarga esta ventana.</p>';document.querySelector('.local-status').textContent='Sin conexión al motor';});
