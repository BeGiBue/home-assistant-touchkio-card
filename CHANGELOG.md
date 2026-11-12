# Changelog

## 2.1.1 - 2026-11-12

- New values no longer rebuild the card: only changed texts and attributes are set. Keyboard focus, an open selection list and the loaded image stay in place, and the kiosk has less to redraw. / Neue Werte bauen die Karte nicht mehr neu auf: Es werden nur geänderte Texte und Attribute gesetzt. Tastaturfokus, eine geöffnete Auswahlliste und das geladene Bild bleiben erhalten, und der Kiosk muss weniger neu zeichnen.
- Fixed: the "Tap again" confirmation of Reboot, Shut down and Install disappeared when a sensor value changed in between. It now stays until confirmed or timed out; taps while a command is being sent are ignored. / Behoben: Die Nachfrage „Nochmal tippen“ bei Neustart, Ausschalten und Installieren verschwand, wenn sich zwischendurch ein Messwert änderte. Sie bleibt jetzt bis zur Bestätigung oder zum Ablauf stehen; Tippen während des Sendens wird ignoriert.
- The column changes at 340 px and 560 px card width now use the same ±12 px tolerance as the font size, so the layout does not flip when a scrollbar appears. / Die Spaltenwechsel bei 340 px und 560 px Kartenbreite nutzen jetzt dieselbe Toleranz von ±12 px wie die Schriftgröße; die Aufteilung kippt nicht mehr, wenn eine Scrollleiste erscheint.
- A custom image that cannot be loaded is remembered and replaced by the built-in image without retrying on every update; an invalid image setting no longer breaks the card. / Ein nicht ladbares eigenes Bild wird gemerkt und durch das eingebaute ersetzt, ohne bei jeder Aktualisierung neu zu laden; eine ungültige Bildeinstellung bringt die Karte nicht mehr zum Absturz.
- Height is measured in the next frame (no "ResizeObserver loop" messages) and measuring continues after the card was moved in the dashboard. / Die Höhe wird im nächsten Bild gemessen (keine „ResizeObserver loop“-Meldungen), und nach dem Verschieben der Karte im Dashboard wird weiter gemessen.
- Browser tests for layout, controls and updates added. / Browser-Tests für Layout, Bedienung und Aktualisierung ergänzt.

## 2.1.0 - 2026-11-07

- The card and its editor now appear in English by default and in German when Home Assistant is set to German. / Karte und Editor erscheinen jetzt standardmäßig auf Englisch und auf Deutsch, wenn Home Assistant auf Deutsch eingestellt ist.
- The default subtitle and update title follow the Home Assistant language; titles already saved in a card stay unchanged. / Standard-Untertitel und Update-Titel folgen der Sprache von Home Assistant; bereits gespeicherte Titel bleiben unverändert.
- README shortened and available in English and German. / README gekürzt und auf Englisch und Deutsch verfügbar.

## 2.0.2 - 2026-11-04

- Behoben: Die Card zappelte (Schrift und Höhe wechselten schnell hin und her), wenn ihre Breite knapp an einer Schriftstufe lag (z. B. 400 px) und die Scrollleiste der Seite dadurch ein- und ausgeblendet wurde. Die Schriftstufe wird jetzt mit ±12 px Hysterese gewählt und kippt bei kleinen Breitenänderungen nicht mehr.

## 2.0.1 - 2026-10-28

- Aufräumarbeiten ohne Funktionsänderung: Begrenzung der Kartengröße an einer Stelle zusammengeführt, nie zutreffende Prüfungen, doppelte Gestaltungsregeln und eine Zwischenliste bei der Seitenauswahl entfernt. Aussehen, Konfiguration und Verhalten bleiben unverändert.
- Repository verschlankt: nicht benötigte Logo-Dateien, interne Release-Checkliste und die Pflicht-Dateien `RELEASE_NOTES_<Version>.md` entfernt (der Release-Text kommt jetzt aus diesem Changelog), doppelten Bild-Abschnitt aus der README genommen.

## 2.0.0 - 2026-10-24

- Aufnahme in den offiziellen HACS-Katalog; reguläre Installation über die HACS-Suche.
- Migration bestehender Custom Repositories dokumentiert: nur den benutzerdefinierten Eintrag entfernen, bestehende Installation und Dashboard-Konfigurationen behalten.
- Major-Version als HACS-Meilenstein: bedeutet nicht automatisch Breaking Changes. Bestehende Konfigurationsschlüssel bleiben erhalten.
- README auf Funktionen, Einrichtung, Bedienung, Voraussetzungen und Grenzen ausgerichtet.
- Regressionstests für Entity-Zustände, Paketdaten, Auswahlwerte, Dashboard-Titel und Konfigurationswerte ergänzt.

## 1.0.5

- Neue, im Browser erstellte Vorschauen aus dem unveränderten Original-Code in der README.
- Vorschau-Bilder über absolute Raw-URLs für die Anzeige in GitHub und HACS eingebunden.
- Versionsangaben für das Patch-Release aktualisiert.

Keine Änderungen an der Funktionsweise der Karte oder Integration.

## 1.0.4 - 2026-10-15

### Behoben

- **Scrollen im TouchKio-Kiosk:** Die Card war selbst ein Scroll-Container mit `overscroll-behavior: contain`. Schon wenige Pixel Überstand (z. B. nach Zeilenumbruch oder nachgeladener Schrift) reichten, damit jede Wischgeste auf der Card von ihr „geschluckt“ wurde und das Dashboard nicht mehr scrollte – auf dem schmalen Kiosk-Display liegt die Card auf der ganzen Breite. Die Card scrollt jetzt nicht mehr selbst; nur die aufgeklappte Paketliste scrollt und gibt am Ende die Geste an die Seite weiter.
- Die Card wächst bei Überstand mit dem Inhalt, statt ihn abzuschneiden. Die gemeldete Zeilenzahl wird auch bei Änderungen der Inhaltshöhe und nach dem Laden der Schrift neu gemessen.
- Display-Slider: Bricht der Browser die Geste ab (`touchcancel`), bleibt die Card nicht mehr im Ziehen-Zustand hängen.

### Neu

- **Kompakte Darstellung** für kleine Hochformat-Displays (z. B. Raspberry Pi 7" hochkant, 480 × 800 Pixel, TouchKio-Web-Zoom 1,25 → 384 × 640 CSS-Pixel). Die Card braucht dort etwa 500 statt 700 Pixel Höhe, sodass alles ohne Scrollen sichtbar ist. Neue Option `compact`: `auto` (Standard: im TouchKio/Electron bei schmalem Hochformat), `on` oder `off`.

## 1.0.3 - 2026-10-08

### Geändert

- Aufräumen im Code: nicht mehr benötigter Programmcode für Number-Slider (Überbleibsel des entfernten Seiten-Zooms) entfernt. Keine funktionalen Änderungen.

## 1.0.2 - 2026-10-08

### Geändert

- Die Höhe der Card ist fest: Im Layout-Editor lässt sie sich nicht mehr verändern (`rows`, `min_rows` und `max_rows` sind gleich), die Breite bleibt frei einstellbar.
- Die aufgeklappte Paketliste ändert die Höhe nicht mehr, sondern scrollt innerhalb der Card.

## 1.0.1 - 2026-10-07

### Geändert

- Laufzeit: Die Einheit wird automatisch gewählt (Min, Std, Tage, ab 7 Tagen Wochen), z. B. „5 Std 12 Min“, „2 Tage 4 Std“, „3 Wochen 2 Tage“. TouchKio meldet die Laufzeit in Minuten.
- Lizenzhinweis: SPDX-Kennung und Copyright im Code-Kopf, ausführlicherer Lizenzabschnitt in der README.
- README: Button zum automatischen Hinzufügen in HACS; aktualisierter Screenshot.

### Entfernt

- Box **Seiten-Zoom** und die Option `zoom_entity`. Steht `zoom_entity` noch in einer bestehenden Konfiguration, wird der Eintrag ignoriert.

## 1.0.0 - 2026-10-07

- Erste Version der TouchKio Card im Stil der NAS Card.
- Display-Helligkeit als Slider; Tippen auf das Symbol schaltet das Display ein oder aus.
- Seiten-Zoom als Slider (Number-Entität, Min/Max/Schritt aus der Entität).
- Kacheln für Bildschirmtastatur (Schalter) sowie Kiosk-Modus und Theme (Auswahl).
- Seitenauswahl: Picker mit allen vorhandenen Home-Assistant-Dashboards und Ansichten; schreibt die gewählte URL in die Text-Entität. Der Stift öffnet die Detailansicht zum manuellen Bearbeiten.
- Freigestelltes TouchKio-Gerätebild eingebettet und groß im Hintergrund; Optionen `show_image` und `image_url`.
- Prozessor-Temperatur, CPU, RAM und Paket-Updates mit Warnfarben (CPU orange ab 75 %, RAM ab 80 %, Temperatur ab 70 °C; rot ab 90 %, 90 % bzw. 80 °C).
- Netzwerkadresse und Laufzeit als Textkacheln.
- App-Update-Zeile mit installierter und ggf. neuer Version. Unterstützt die Entität die Installation, erscheint der Button **Installieren** (zweites Tippen zur Bestätigung, danach Fortschrittsanzeige).
- Die Kachel **Pakete** klappt die Liste der verfügbaren System-Updates (Attribut `packages`) auf.
- Aktionen Aktualisieren, Neustart und Herunterfahren; Neustart und Herunterfahren verlangen ein zweites Tippen.
- Alle Entitäten sind im grafischen Editor wählbar; nicht gesetzte Bereiche werden ausgeblendet.
- Glas-Look: Hintergrund, Rand und Blur kommen vom Theme. Schrift wächst mit der Kartenbreite, Option `scale` für Kiosk-Displays.
- HACS-Metadaten und Validierung über GitHub Actions.
