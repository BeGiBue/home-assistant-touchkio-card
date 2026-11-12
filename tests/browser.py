#!/usr/bin/env python3
"""Chromium-Tests mit lokalen Home-Assistant-Attrappen; keine realen Geräteaufrufe.

  python tests/browser.py             # Prüfungen
  python tests/browser.py --preview   # zusätzlich Vorschaubilder nach tests/out/

Benötigt: pip install -r requirements-dev.txt  und  playwright install chromium
(oder PLAYWRIGHT_CHROMIUM_EXECUTABLE auf einen vorhandenen Chromium/Chrome setzen).
"""
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

PAGE = """<!doctype html><meta charset="utf-8"><style>
body{margin:0;padding:14px;background:#e9edf1;font-family:Roboto,Inter,sans-serif;font-size:14px;
--primary-text-color:#141414;--secondary-text-color:#6b6f76;--primary-color:#009ac7;--success-color:#43a047;
--warning-color:#ff9800;--error-color:#e53935;--card-background-color:#fff}
</style><div id="w"></div><script>
window.__errors = [];
window.addEventListener('error', (e) => window.__errors.push(String(e.message || e)));
window.addEventListener('unhandledrejection', (e) => window.__errors.push('rejection: ' + e.reason));
customElements.define('ha-card',class extends HTMLElement{constructor(){super();this.attachShadow({mode:'open'}).innerHTML=
  '<style>:host{display:block;background:#fff;border-radius:16px;border:1px solid #dfe3e8;box-sizing:border-box;padding:0}</style><slot></slot>'}});
customElements.define('ha-icon',class extends HTMLElement{connectedCallback(){(this.shadowRoot||this.attachShadow({mode:'open'})).innerHTML=
  '<style>:host{display:inline-flex;width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}i{flex:1;border-radius:30%;background:currentColor;opacity:.55}</style><i></i>'}});
window.st = (state, unit, extra) => ({state: String(state), attributes: {...(unit ? {unit_of_measurement: unit} : {}), ...(extra || {})}});
// Zustände passend zu den Standard-Entitäten der Card (aus ihrer eigenen Standard-Konfiguration abgeleitet)
window.baseStates = () => {
  const c = document.createElement('touchkio-card'); c.setConfig({});
  const cfg = c._config, s = {};
  for (const [k, id] of Object.entries(cfg)) {
    if (!k.endsWith('_entity') || !id) continue;
    if (k === 'display_entity') s[id] = st('on', '', {brightness: 153});
    else if (k === 'keyboard_entity') s[id] = st('off');
    else if (k === 'kiosk_entity') s[id] = st('Fullscreen', '', {options: ['Framed', 'Fullscreen', 'Maximized']});
    else if (k === 'theme_entity') s[id] = st('Dark', '', {options: ['Light', 'Dark']});
    else if (k === 'url_entity') s[id] = st('https://ha.example/lovelace/wohnen');
    else if (k === 'temperature_entity') s[id] = st('48.2', '°C');
    else if (k === 'cpu_entity') s[id] = st('12', '%');
    else if (k === 'memory_entity') s[id] = st('41', '%');
    else if (k === 'packages_entity') s[id] = st('2', '', {packages: [{libc6: '2.36-9'}, {curl: '7.88.1'}]});
    else if (k === 'network_entity') s[id] = st('192.168.1.40');
    else if (k === 'uptime_entity') s[id] = st('3125', 'min');
    else if (k === 'update_entity') s[id] = st('on', '', {installed_version: '1.4.0', latest_version: '1.5.0', supported_features: 1});
    else s[id] = st('unknown');
  }
  return s;
};
window.fixture = ({width = 400, config = {}, language = 'de', states = window.baseStates(), fail = false, hold = false} = {}) => {
  const w = document.getElementById('w');
  w.replaceChildren();
  w.style.width = width + 'px';
  const card = document.createElement('touchkio-card'), events = [], calls = [], pending = [];
  card.addEventListener('hass-more-info', (e) => events.push(e.detail.entityId));
  const mk = (s) => ({states: s, language, locale: {language},
    callService: (...a) => { calls.push(a); if (hold) return new Promise((res) => pending.push(res)); return fail ? Promise.reject(new Error('x')) : Promise.resolve(); },
    callWS: (m) => Promise.resolve(m.type === 'lovelace/dashboards/list' ? [] : {views: [{title: 'Wohnen', path: 'wohnen'}, {title: 'Technik', path: 'technik'}]})});
  card.setConfig(config);
  w.appendChild(card);
  card.hass = mk(states);
  return {card, events, calls, pending, cfg: card._config, set: (s) => { card.hass = mk(s); }};
};
</script>"""

TEST_JS = r"""
async () => {
  const results = [], check = (name, pass) => results.push({name, pass: !!pass});
  const turn = (ms = 0) => new Promise((r) => setTimeout(r, ms));
  const frames = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  const {fixture, baseStates, st} = window;
  const q = (card, sel) => card.shadowRoot.querySelector(sel);
  const qa = (card, sel) => [...card.shadowRoot.querySelectorAll(sel)];
  const text = (el) => el?.textContent.replace(/\s+/g, ' ').trim();
  const hc = (card) => q(card, 'ha-card');
  const H = (card) => hc(card).getBoundingClientRect().height;
  const setW = (w) => { document.getElementById('w').style.width = w + 'px'; };

  // --- Aufbau und Aktualisieren ohne Neuaufbau ---
  {
    const f = fixture(), c = f.cfg;
    await turn(20);
    const card = hc(f.card), main = q(f.card, 'main'), img = q(f.card, '.bgimg');
    const cpuTile = q(f.card, `[data-more="${c.cpu_entity}"]`), slider = q(f.card, 'input[data-slider]');
    check('Aufbau: Kopf, Update-Zeile, drei Aktionen, vier Kacheln, Regler', text(q(f.card, 'h1')) === 'TouchKio' && qa(f.card, '.act').length === 3 && qa(f.card, '.tiles .tile').length === 4 && slider && q(f.card, '.upd'));
    check('Aufbau: kein Leerraum-Text zwischen den Elementen', [...main.childNodes].every((n) => n.nodeType === 1));
    check('Regler zeigt die gemeldete Helligkeit', slider.value === '60' && text(q(f.card, '.slv')) === '60%');
    cpuTile.focus();
    const s = baseStates();
    s[c.cpu_entity] = st('93', '%');
    s[c.temperature_entity] = st('71.5', '°C');
    s[c.display_entity] = st('on', '', {brightness: 51});
    s[c.theme_entity] = st('Light', '', {options: ['Light', 'Dark']});
    f.set(s);
    check('neue Werte: Karte, Inhalt, Bild, Kachel und Regler bleiben dieselben Elemente',
      hc(f.card) === card && q(f.card, 'main') === main && q(f.card, '.bgimg') === img && q(f.card, `[data-more="${c.cpu_entity}"]`) === cpuTile && q(f.card, 'input[data-slider]') === slider);
    check('neue Werte: Text, Farbe und Balken folgen', /93/.test(text(cpuTile)) && cpuTile.classList.contains('tone-error') && cpuTile.querySelector('.bar u').style.width === '93%'
      && q(f.card, `[data-more="${c.temperature_entity}"]`).classList.contains('tone-warning'));
    check('neue Werte: Tastaturfokus bleibt', f.card.shadowRoot.activeElement === cpuTile);
    check('neue Werte: Regler und Auswahl folgen dem gemeldeten Stand', slider.value === '20' && text(q(f.card, '.slv')) === '20%' && q(f.card, `select[data-select="${c.theme_entity}"]`).value === 'Light');
    // angeglichen == frisch aufgebaut
    const morphed = hc(f.card).innerHTML, cls = hc(f.card).className;
    f.card._built = false; f.card._sig = ''; f.card._update();
    check('angeglichener Inhalt entspricht einem frischen Aufbau', hc(f.card).innerHTML === morphed && hc(f.card).className === cls && hc(f.card) !== card);
    const before = hc(f.card);
    f.set(s);
    check('gleiche Werte: nichts wird angefasst', hc(f.card) === before);
  }

  // --- Klicks ---
  {
    const f = fixture(), c = f.cfg;
    await turn(20);
    q(f.card, `[data-more="${c.cpu_entity}"] .val b`).click();
    q(f.card, '.upd .rm').click();
    q(f.card, '.pick .edit').click();
    check('Tippen auf Kachel, Update-Zeile und Stift öffnet die Entität', JSON.stringify(f.events) === JSON.stringify([c.cpu_entity, c.update_entity, c.url_entity]));
    q(f.card, `.ctl [data-toggle="${c.keyboard_entity}"]`).click();
    q(f.card, `.sl [data-toggle="${c.display_entity}"] ha-icon`).click();
    check('Schalter rufen toggle der passenden Domäne', f.calls.length === 2 && f.calls[0][0] === 'switch' && f.calls[0][1] === 'toggle' && f.calls[1][0] === 'light' && f.calls[1][2].entity_id === c.display_entity);
    const sel = q(f.card, `select[data-select="${c.kiosk_entity}"]`);
    sel.value = 'Framed'; sel.dispatchEvent(new Event('change', {bubbles: true}));
    check('Auswahl ruft select_option', f.calls[2][0] === 'select' && f.calls[2][2].option === 'Framed');
    // Die Auswahl springt zurück, solange Home Assistant den alten Stand meldet
    const s = baseStates(); s[c.cpu_entity] = st('13', '%'); f.set(s);
    check('Auswahl zeigt wieder den gemeldeten Stand, wenn Home Assistant ihn nicht übernimmt', sel.isConnected && sel.value === 'Fullscreen');
    await turn(30);
    const page = q(f.card, 'select[data-page]');
    check('Seitenauswahl: Ansichten geladen, aktuelle Seite markiert', page.options.length === 2 && page.value === 'https://ha.example/lovelace/wohnen' && /Wohnen/.test(text(q(f.card, '.pick small'))));
    page.value = 'https://ha.example/lovelace/technik'; page.dispatchEvent(new Event('change', {bubbles: true}));
    check('Seitenauswahl setzt die Adresse', f.calls[3][0] === 'text' && f.calls[3][1] === 'set_value' && f.calls[3][2].value === 'https://ha.example/lovelace/technik');
    // Paketliste
    const rows = f.card.getGridOptions().rows;
    q(f.card, '[data-pkgs]').click();
    check('Paketliste klappt auf, Karte scrollt selbst', qa(f.card, '.prow').length === 2 && hc(f.card).classList.contains('scroll') && q(f.card, '[data-pkgs]').getAttribute('aria-expanded') === 'true');
    await frames();
    check('Paketliste ändert die gemeldete Zeilenzahl nicht', f.card.getGridOptions().rows === rows);
    q(f.card, '[data-pkgs]').click();
    check('Paketliste klappt wieder zu', qa(f.card, '.prow').length === 0 && !hc(f.card).classList.contains('scroll'));
  }

  // --- Aktionen mit Bestätigung ---
  {
    const f = fixture(), c = f.cfg;
    await turn(20);
    const btn = (id) => q(f.card, `[data-press="${id}"]`);
    btn(c.refresh_entity).click();
    await turn();
    check('Neu laden ohne Bestätigung: sofort gesendet', f.calls.length === 1 && f.calls[0][0] === 'button' && f.calls[0][1] === 'press' && btn(c.refresh_entity).classList.contains('sent') && text(btn(c.refresh_entity).querySelector('b')) === 'Gesendet');
    btn(c.refresh_entity).click();
    await turn();
    check('Tippen während „Gesendet“ löst nicht erneut aus', f.calls.length === 1);
    btn(c.reboot_entity).click();
    check('Neustart: erster Tipp fragt nach', f.calls.length === 1 && btn(c.reboot_entity).classList.contains('arm') && text(btn(c.reboot_entity)) === 'Nochmal tippenzum Bestätigen');
    const s = baseStates(); s[c.cpu_entity] = st('55', '%'); f.set(s);
    check('Nachfrage übersteht neue Werte', btn(c.reboot_entity).classList.contains('arm') && text(btn(c.reboot_entity).querySelector('b')) === 'Nochmal tippen');
    btn(c.reboot_entity).click();
    await turn();
    check('Neustart: zweiter Tipp sendet', f.calls.length === 2 && f.calls[1][2].entity_id === c.reboot_entity && btn(c.reboot_entity).classList.contains('sent'));
    // Installieren
    const inst = () => q(f.card, '[data-install]');
    inst().click();
    check('Installieren: erster Tipp fragt nach', f.calls.length === 2 && inst().classList.contains('arm') && text(inst()) === 'Nochmal tippen');
    s[c.memory_entity] = st('44', '%'); f.set(s);
    check('Installieren: Nachfrage übersteht neue Werte', inst().classList.contains('arm'));
    inst().click();
    await turn();
    check('Installieren: zweiter Tipp sendet', f.calls.length === 3 && f.calls[2][0] === 'update' && f.calls[2][1] === 'install' && text(inst()) === 'Gesendet' && !inst().classList.contains('arm'));
    inst().click();
    await turn();
    check('Installieren: Tippen während „Gesendet“ löst nicht erneut aus', f.calls.length === 3);
    s[c.update_entity] = st('on', '', {installed_version: '1.4.0', latest_version: '1.5.0', supported_features: 1, in_progress: true, update_percentage: 40});
    f.set(s);
    check('laufendes Update zeigt den Fortschritt statt der Schaltfläche', !inst() && /40 %/.test(text(q(f.card, '.upd .pill'))));
  }
  {
    const f = fixture({config: {confirm_actions: false}}), c = f.cfg;
    q(f.card, `[data-press="${c.shutdown_entity}"]`).click();
    await turn();
    check('ohne Bestätigung: Herunterfahren sendet beim ersten Tipp', f.calls.length === 1 && f.calls[0][2].entity_id === c.shutdown_entity);
  }
  {
    const f = fixture({fail: true}), c = f.cfg;
    const b = () => q(f.card, `[data-press="${c.refresh_entity}"]`);
    b().click();
    await turn(10);
    check('Fehler beim Senden: Schaltfläche kehrt zurück', !b().classList.contains('sent') && !b().classList.contains('arm') && text(b().querySelector('b')) !== 'Gesendet');
    b().click();
    await turn(10);
    check('Fehler beim Senden: erneuter Versuch möglich', f.calls.length === 2);
  }
  {
    const f = fixture({hold: true}), c = f.cfg;
    const b = () => q(f.card, `[data-press="${c.refresh_entity}"]`);
    b().click(); b().click(); b().click();
    await turn();
    check('schnelles Mehrfachtippen sendet nur einmal', f.calls.length === 1);
    f.pending.forEach((r) => r());
  }

  // --- Regler ---
  {
    const f = fixture(), c = f.cfg;
    await turn(20);
    const sl = q(f.card, 'input[data-slider]'), main = q(f.card, 'main');
    sl.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true, composed: true}));
    sl.value = '35'; sl.dispatchEvent(new Event('input', {bubbles: true}));
    check('Ziehen: Anzeige folgt sofort', text(q(f.card, '.slv')) === '35%' && sl.style.getPropertyValue('--p') === '35%');
    const s = baseStates(); s[c.cpu_entity] = st('77', '%'); f.set(s);
    check('Ziehen: neue Werte warten, der Regler springt nicht', sl.value === '35' && !/77/.test(text(q(f.card, `[data-more="${c.cpu_entity}"]`))));
    sl.dispatchEvent(new Event('change', {bubbles: true}));
    await turn();
    check('Loslassen setzt die Helligkeit', f.calls.length === 1 && f.calls[0][0] === 'light' && f.calls[0][1] === 'turn_on' && f.calls[0][2].brightness_pct === 35);
    s[c.display_entity] = st('on', '', {brightness: 89}); f.set(s);
    await turn(700);
    check('nach dem Loslassen: wartende Werte erscheinen, Regler ist derselbe und zeigt den gemeldeten Stand',
      q(f.card, 'input[data-slider]') === sl && q(f.card, 'main') === main && sl.value === '35' && /77/.test(text(q(f.card, `[data-more="${c.cpu_entity}"]`))));
    sl.value = '0'; sl.dispatchEvent(new Event('input', {bubbles: true})); sl.dispatchEvent(new Event('change', {bubbles: true}));
    await turn();
    check('Regler auf 0 schaltet aus', f.calls[1][1] === 'turn_off' && text(q(f.card, '.slv')) === 'Aus');
    // nach vielen Aktualisierungen genau eine Meldung pro Bedienung
    await turn(700);
    for (let i = 0; i < 5; i++) { s[c.cpu_entity] = st(String(20 + i), '%'); f.set(s); }
    const n = f.calls.length;
    sl.value = '50'; sl.dispatchEvent(new Event('change', {bubbles: true}));
    await turn();
    check('nach mehreren Aktualisierungen löst eine Bedienung genau einen Aufruf aus', f.calls.length === n + 1);
    await turn(700);
  }

  // --- Zusammenspiel Regler und Aktionen ---
  {
    const f = fixture(), c = f.cfg;
    await turn(20);
    const sl = q(f.card, 'input[data-slider]'), btn = () => q(f.card, `[data-press="${c.reboot_entity}"]`);
    sl.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true, composed: true}));
    sl.value = '35'; sl.dispatchEvent(new Event('input', {bubbles: true}));
    sl.dispatchEvent(new Event('change', {bubbles: true})); sl.dispatchEvent(new PointerEvent('pointerup', {bubbles: true, composed: true}));
    await turn(50);
    btn().click();
    check('direkt nach dem Regler: Nachfrage erscheint sofort, Regler behält seinen Stand', btn().classList.contains('arm') && sl.value === '35' && text(q(f.card, '.slv')) === '35%' && f.calls.filter((x) => x[0] === 'button').length === 0);
    q(f.card, '[data-pkgs]').click();
    check('direkt nach dem Regler: Paketliste klappt sofort auf', qa(f.card, '.prow').length === 2 && sl.value === '35');
    await turn(700);
    const g = fixture();
    const s2 = q(g.card, 'input[data-slider]');
    s2.value = '70'; s2.dispatchEvent(new Event('input', {bubbles: true}));
    check('Reglerbewegung ohne Abschluss: Sicherung läuft', g.card._drag === true && !!g.card._dt);
    clearTimeout(g.card._dt); g.card._drag = false;
  }
  {
    const f = fixture({config: {refresh_entity: 'button.same', reboot_entity: 'button.same', shutdown_entity: 'button.same'}});
    qa(f.card, '.act')[1].click();
    check('gleiche Entität an mehreren Schaltflächen: nur die getippte fragt nach', qa(f.card, '.act.arm').length === 1 && qa(f.card, '.act')[1].classList.contains('arm'));
  }
  {
    const f = fixture({hold: true}), c = f.cfg;
    const b = () => q(f.card, `[data-press="${c.refresh_entity}"]`);
    b().click();
    await turn();
    check('laufender Aufruf: Schaltfläche zeigt, dass gesendet wird', b().classList.contains('busy'));
    f.pending.forEach((r) => r());
    await turn();
    check('Aufruf fertig: „Gesendet“', b().classList.contains('sent') && !b().classList.contains('busy'));
  }
  {
    const f = fixture(), c = f.cfg, s = baseStates();
    s[c.update_entity] = st('on', '', {installed_version: '1.4.9', latest_version: '1.5.0', supported_features: 1}); f.set(s);
    check('nur die installierte Version ändert sich: Anzeige folgt', /1\.4\.9/.test(text(q(f.card, '.upd small'))));
    q(f.card, '[data-pkgs]').click();
    s[c.packages_entity] = st('2', '', {packages: [{zlib: '1.3'}, {bash: '5.2'}]}); f.set(s);
    check('Paketnamen ändern sich bei gleicher Anzahl: Liste folgt', /zlib/.test(text(q(f.card, '.plist'))));
  }

  // --- Bild ---
  {
    const f = fixture({config: {image_url: 'http://127.0.0.1:9/kaputt.png'}});
    for (let i = 0; i < 60 && !f.card._badImg?.size; i++) await turn(50);
    const img = q(f.card, '.bgimg');
    check('eigenes Bild nicht ladbar: eingebautes Bild erscheint', img && img.getAttribute('src').startsWith('data:image/'));
    const s = baseStates(); s[f.cfg.cpu_entity] = st('31', '%'); f.set(s);
    f.card.setConfig({image_url: 'http://127.0.0.1:9/kaputt.png', title: 'Neu'}); f.set(s);
    check('nicht ladbare Adresse bleibt gemerkt (kein erneuter Ladeversuch)', q(f.card, '.bgimg').getAttribute('src').startsWith('data:image/') && text(q(f.card, 'h1')) === 'Neu');
    const g = fixture({config: {show_image: false}});
    check('Bild abschaltbar', !q(g.card, '.bgimg'));
    const h = fixture({config: {image_url: 42}});
    check('Bildadresse, die kein Text ist, stört nicht', q(h.card, '.bgimg').getAttribute('src').startsWith('data:image/'));
  }

  // --- Zustände, Sprache, Konfiguration ---
  {
    const s = baseStates(), f = fixture({states: s}), c = f.cfg;
    for (const k of Object.keys(s)) s[k] = st('unavailable');
    f.set(s);
    check('alles nicht verfügbar: Karte bleibt stehen, Werte zeigen Striche', qa(f.card, '.tiles .tile').length === 4 && qa(f.card, '.tiles .val b').every((b) => text(b) === '—'));
    f.set({});
    check('fehlende Entitäten: kein Absturz', !!q(f.card, 'main'));
    f.set(baseStates());
    check('Entitäten kehren zurück: Werte erscheinen wieder', /12/.test(text(q(f.card, `[data-more="${c.cpu_entity}"]`))) && !!q(f.card, '[data-install]'));
    const e = fixture({language: 'en'});
    check('Englisch: Texte folgen der Sprache', /Reboot|Restart/.test(text(q(e.card, `[data-press="${e.cfg.reboot_entity}"]`))) && text(q(e.card, '[data-install]')) === 'Install');
    const m = fixture({config: {reboot_entity: '', shutdown_entity: '', update_entity: '', url_entity: '', display_entity: '', kiosk_entity: '', theme_entity: '', keyboard_entity: ''}});
    check('abgewählte Entitäten: Bereiche entfallen', qa(m.card, '.act').length === 1 && !q(m.card, '.upd') && !q(m.card, '.pick') && !q(m.card, '.sl') && !q(m.card, '.ctl'));
    const k = fixture({config: {compact: 'on'}});
    check('Kompakt-Modus per Einstellung', hc(k.card).classList.contains('compact'));
    k.card.setConfig({compact: 'off'}); k.set(baseStates());
    check('Kompakt-Modus abschaltbar', !hc(k.card).classList.contains('compact'));
  }

  // --- Breiten, Schriftstufen, Spalten ---
  {
    for (const w of [260, 300, 340, 400, 560, 800, 1100]) {
      const f = fixture({width: w});
      await frames();
      const over = qa(f.card, 'main *').filter((el) => { const r = el.getBoundingClientRect(), m = q(f.card, 'main').getBoundingClientRect(); return r.width > 0 && (r.right > m.right + 1 || r.left < m.left - 1); });
      check(`${w} px: nichts ragt aus der Karte`, over.length === 0);
    }
    const cols = (card, sel) => getComputedStyle(q(card, sel)).gridTemplateColumns.split(' ').length;
    const f = fixture({width: 300});
    await frames();
    check('300 px: zwei Kacheln je Zeile, Aktionen untereinander', cols(f.card, '.tiles') === 2 && cols(f.card, '.foot') === 1 && hc(f.card).classList.contains('slim'));
    setW(345); await frames();
    check('345 px (innerhalb der Hysterese): Aufteilung bleibt', cols(f.card, '.tiles') === 2);
    setW(360); await frames();
    check('360 px: vier Kacheln je Zeile', cols(f.card, '.tiles') === 4 && cols(f.card, '.foot') === 2);
    setW(332); await frames();
    check('332 px (innerhalb der Hysterese): bleibt bei vier Kacheln', cols(f.card, '.tiles') === 4);
    setW(320); await frames();
    check('320 px: wieder zwei Kacheln', cols(f.card, '.tiles') === 2);
    setW(580); await frames();
    check('580 px: drei Aktionen nebeneinander', cols(f.card, '.foot') === 3);
    setW(552); await frames();
    check('552 px (innerhalb der Hysterese): bleibt bei drei', cols(f.card, '.foot') === 3);
    setW(540); await frames();
    check('540 px: zwei Spalten, erste Aktion über die ganze Breite', cols(f.card, '.foot') === 2);
    // Schriftstufe mit Hysterese
    const g = fixture({width: 395});
    await frames();
    const fs = () => hc(g.card).style.getPropertyValue('--fs');
    check('395 px: Schrift 14 px', fs() === '14px');
    setW(408); await frames();
    check('408 px (innerhalb der Hysterese): Schrift bleibt', fs() === '14px');
    setW(414); await frames();
    check('414 px: Schrift 15 px', fs() === '15px');
    setW(392); await frames();
    check('392 px (innerhalb der Hysterese): Schrift bleibt', fs() === '15px');
    // Klassen überstehen neue Werte
    const s = baseStates(); s[g.cfg.cpu_entity] = st('66', '%');
    setW(300); await frames(); g.set(s);
    check('Spalten-Klasse übersteht neue Werte', hc(g.card).classList.contains('slim') && hc(g.card).style.getPropertyValue('--fs') === '14px');
  }

  // --- Höhe und Scrollleiste ---
  {
    const f = fixture({width: 400});
    await frames();
    const o = f.card.getGridOptions();
    check('Zeilenzahl aus der gemessenen Höhe, fest', o.rows === o.min_rows && o.rows === o.max_rows && Math.abs(o.rows * 64 - 8 - H(f.card)) < 64);
    // Scrollleiste: Karte darf bei 15 px weniger Breite nicht niedriger werden als bei voller Breite … und umgekehrt nicht pendeln
    let swing = [];
    for (let W = 250; W <= 1100; W += 10) {
      const a = fixture({width: W}); await frames(); const h1 = H(a.card);
      setW(W - 15); await frames(); const h2 = H(a.card);
      if (h1 <= h2 + .3) continue;
      const mid = (h1 + h2) / 2; let n = 0, cur = W - 15;
      for (let i = 0; i < 12; i++) { const want = H(a.card) > mid ? W - 15 : W; if (want !== cur) { cur = want; setW(cur); n++; } await frames(); }
      if (n > 4) swing.push(W);
    }
    check('Scrollleiste: Höhe pendelt bei keiner Breite' + (swing.length ? ' (' + swing.join(',') + ')' : ''), swing.length === 0);
  }

  // --- Abbau ---
  {
    const f = fixture();
    await frames();
    const host = f.card.parentNode;
    f.card.remove();
    host.appendChild(f.card);
    host.style.width = '620px';
    await frames(); await frames();
    check('nach Aus- und Einhängen wird weiter gemessen', hc(f.card).style.getPropertyValue('--fs') === '17px');
  }
  await turn(50);
  check('keine Fehler-Ereignisse (auch kein „ResizeObserver loop“)', window.__errors.length === 0);
  if (window.__errors.length) results.push({name: 'Fehler: ' + window.__errors.join(' | '), pass: false});
  return results;
}
"""


def launch(p):
    executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    return p.chromium.launch(**({"executable_path": executable, "args": ["--no-sandbox"]} if executable else {}))


def main():
    source = (ROOT / "touchkio-card.js").read_text(encoding="utf8")
    errors = []
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": 1200, "height": 1000})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.set_content(PAGE)
        page.add_script_tag(content=source)
        results = page.evaluate(TEST_JS)
        results.append({"name": "keine JavaScript-Fehler", "pass": not errors})
        if "--preview" in sys.argv:
            out = ROOT / "tests" / "out"
            out.mkdir(exist_ok=True)
            for width in (300, 400, 600, 800):
                shot = browser.new_page(viewport={"width": width + 28, "height": 400}, device_scale_factor=2)
                shot.set_content(PAGE)
                shot.add_script_tag(content=source)
                shot.evaluate("(width) => { window.fixture({width}); }", width)
                shot.wait_for_timeout(300)
                shot.screenshot(path=str(out / f"touchkio-{width}.png"), full_page=True)
                shot.close()
        browser.close()
    for result in results:
        print(("PASS " if result["pass"] else "FAIL ") + result["name"])
    failures = sum(not result["pass"] for result in results)
    print(f"\n{len(results)} Prüfungen, {failures} Fehler")
    if errors:
        print(errors)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
