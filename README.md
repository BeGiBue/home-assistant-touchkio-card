<p align="center">
  <img src="https://raw.githubusercontent.com/BeGiBue/home-assistant-touchkio-card/main/images/touchkio-card-logo-160.png" alt="TouchKio Card" width="160">
</p>

<h1 align="center">TouchKio Card</h1>

<p align="center">
  Custom-Card für <a href="https://github.com/leukipp/touchkio">TouchKio</a> – Steuerung und Status eines Raspberry-Pi-Kiosks.
</p>

## Vorschau

**Normalbetrieb – schmal (350 px)**

<img src="https://raw.githubusercontent.com/BeGiBue/home-assistant-touchkio-card/main/screenshots/touchkio-normal-350-light.png" width="350" alt="TouchKio Card im Normalbetrieb, 350 px Kartenbreite, helles Theme">

**Normalbetrieb – breit (800 px)**

<img src="https://raw.githubusercontent.com/BeGiBue/home-assistant-touchkio-card/main/screenshots/touchkio-normal-800-light.png" width="800" alt="TouchKio Card im Normalbetrieb, 800 px Kartenbreite, helles Theme">

<p align="center">
  <strong>Version 2.0.0</strong><br>
  <a href="https://github.com/BeGiBue/home-assistant-touchkio-card/actions/workflows/validate.yml"><img src="https://github.com/BeGiBue/home-assistant-touchkio-card/actions/workflows/validate.yml/badge.svg" alt="HACS validation"></a>
</p>

## Funktionen

- Theme-sensitive Darstellung für Light Mode, Dark Mode und benutzerdefinierte Home-Assistant-Themes
- Freigestelltes TouchKio-Gerätebild direkt in der JavaScript-Komponente eingebettet – groß im Hintergrund; optional eigene Bild-URL oder ausblendbar
- Display-Helligkeit per Slider; Tippen auf das Symbol schaltet das Display ein oder aus
- Bildschirmtastatur als Schalter-Kachel
- Kiosk-Modus und Theme als Auswahl-Kacheln (nativer Picker)
- Seitenauswahl: Picker mit allen vorhandenen Home-Assistant-Dashboards und deren Ansichten; die Auswahl wird in die Seiten-URL-Entität geschrieben. Der Stift öffnet die Detailansicht zum manuellen Bearbeiten der URL
- Prozessor-Temperatur, CPU, RAM und Paket-Updates; Warnfarben (CPU orange ab 75 %, RAM ab 80 %, Temperatur ab 70 °C, rot ab 90 % / 90 % / 80 °C)
- Netzwerkadresse und Laufzeit (Einheit wird automatisch gewählt: Minuten, Stunden, Tage oder Wochen)
- App-Update-Zeile mit installierter und ggf. neuer Version; bei verfügbarem Update und unterstützter Installation erscheint der Button **Installieren** (mit zweitem Tippen zur Bestätigung), während der Installation der Fortschritt in Prozent
- Tippen auf die Kachel **Pakete** klappt die Liste der verfügbaren System-Updates (Paketname und neue Version) auf und wieder zu
- Aktualisieren, Neustart und Herunterfahren; Neustart und Herunterfahren verlangen ein zweites Tippen
- Alle Entitäten über native Home-Assistant-Entity-Picker wählbar; nicht gesetzte Bereiche werden ausgeblendet
- Breite im Sections-Dashboard frei von 4 bis 12 Spalten, Höhe automatisch
- Optimiert für Hochformat und Touch – iPhone, iPad und Raspberry-Pi-Kiosk: Schrift wächst mit der Kartenbreite
- Kompakte Darstellung für kleine Hochformat-Displays (Raspberry Pi 7" hochkant): alles auf einer Bildschirmhöhe, ohne Scrollen

## Standard-Entitäten

```text
light.touchkio_touchkio_display
switch.touchkio_touchkio_keyboard
select.touchkio_touchkio_kiosk
select.touchkio_touchkio_theme
text.touchkio_touchkio_page_url
sensor.touchkio_touchkio_processor_temperature
sensor.touchkio_touchkio_processor_usage
sensor.touchkio_touchkio_memory_usage
sensor.touchkio_touchkio_package_upgrades
sensor.touchkio_touchkio_network_address
sensor.touchkio_touchkio_up_time
update.touchkio_touchkio_app
button.touchkio_touchkio_refresh
button.touchkio_touchkio_reboot
button.touchkio_touchkio_shutdown
```

Alle Entitäten können im grafischen Karteneditor geändert oder geleert werden. Ein leeres Feld blendet den zugehörigen Bereich aus.

## Installation über HACS

Das Projekt ist im offiziellen HACS-Katalog verfügbar.

1. HACS öffnen und nach **TouchKio Card** suchen.
2. Die Karte auswählen und herunterladen.
3. Browser vollständig neu laden; in der Companion-App gegebenenfalls den Frontend-Cache zurücksetzen.

[![In HACS öffnen](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=BeGiBue&repository=home-assistant-touchkio-card&category=plugin)

### Bestehende Custom-Repository-Installation migrieren

1. Zuerst prüfen, ob **TouchKio Card** im offiziellen HACS-Katalog gefunden wird. Falls nicht, HACS aktualisieren und den bisherigen Eintrag vorerst behalten.
2. Unter **HACS → ⋮ → Benutzerdefinierte Repositories** nur den Eintrag für dieses Repository entfernen.
3. **Die bestehende Installation nicht deinstallieren.** Installation, Dashboard-Ressource und Kartenkonfigurationen beibehalten.
4. HACS neu laden bzw. **Informationen aktualisieren**, anschließend die weiterhin installierte Karte und angebotene Updates prüfen.
5. Nach einem Update das Frontend vollständig neu laden und die vorhandenen Dashboard-Karten prüfen.

Für den Wechsel in den Katalog müssen Karten und YAML-Konfigurationen nicht neu angelegt werden. Die Major-Version kennzeichnet diesen Meilenstein und bedeutet nicht automatisch Breaking Changes; vorhandene Konfigurationsschlüssel bleiben erhalten.

## Card hinzufügen

Minimal:

```yaml
type: custom:touchkio-card
```

Vollständiges Beispiel:

```yaml
type: custom:touchkio-card
title: TouchKio
subtitle: Kiosk-Steuerung
display_entity: light.touchkio_touchkio_display
keyboard_entity: switch.touchkio_touchkio_keyboard
kiosk_entity: select.touchkio_touchkio_kiosk
theme_entity: select.touchkio_touchkio_theme
url_entity: text.touchkio_touchkio_page_url
temperature_entity: sensor.touchkio_touchkio_processor_temperature
cpu_entity: sensor.touchkio_touchkio_processor_usage
memory_entity: sensor.touchkio_touchkio_memory_usage
packages_entity: sensor.touchkio_touchkio_package_upgrades
network_entity: sensor.touchkio_touchkio_network_address
uptime_entity: sensor.touchkio_touchkio_up_time
update_title: App-Update
update_entity: update.touchkio_touchkio_app
refresh_entity: button.touchkio_touchkio_refresh
reboot_entity: button.touchkio_touchkio_reboot
shutdown_entity: button.touchkio_touchkio_shutdown
```

## Optionen

| Option | Werte | Standard | Beschreibung |
|---|---|---|---|
| `show_image` | `true` \| `false` | `true` | Gerätebild im Hintergrund anzeigen. |
| `image_url` | URL | leer | Eigenes Gerätebild, z. B. `/local/images/touchkio.png`. Leer = eingebettetes Standardbild. |
| `scale` | `0.8` – `1.8` | `1` | Skaliert die gesamte Card, z. B. für Kiosk-Displays. |
| `compact`         | `auto` \| `on` \| `off` | `auto` | Kompakte Darstellung für kleine Hochformat-Displays. `auto`: im TouchKio-Kiosk (Electron) bei schmalem Hochformat (Breite ≤ 520, Höhe ≤ 760 CSS-Pixel). |
| `confirm_actions` | `true` \| `false` | `true` | Neustart und Herunterfahren erst nach einem zweiten Tippen auslösen. |

## Updates

**App-Update (TouchKio selbst):** Die Update-Entität zeigt installierte und neue Version. Unterstützt TouchKio auf dem Gerät die Installation (Installation per `.deb` mit Dienst), erscheint in der Zeile der Button **Installieren**. Er ruft `update.install` auf; TouchKio führt dann sein Update-Skript aus und meldet den Fortschritt zurück. Unterstützt die Entität keine Installation, zeigt die Zeile nur den Status – das Update muss dann auf dem Gerät erfolgen.

**System-Updates (apt):** TouchKio prüft stündlich per `apt list --upgradable` und meldet Anzahl und Liste (Attribut `packages` des Sensors „Package Upgrades"). Die Card zeigt die Liste an. Installieren lässt sich das aus Home Assistant nicht, weil TouchKio dafür keinen Dienst bereitstellt; auf dem Gerät: `sudo apt update && sudo apt upgrade`.

## Layout / Größe

Im Home-Assistant-Sections-Dashboard ist die Breite frei einstellbar (4 bis 12 Spalten). Die Höhe ist fest: Die Card meldet genau die Zeilenzahl, die ihr Inhalt bei der aktuellen Breite braucht, und im Layout-Editor lässt sie sich nicht verändern. Die aufgeklappte Paketliste ändert die Höhe nicht, sondern scrollt innerhalb der Card; am Listenende wird die Wischgeste an die Seite weitergereicht. Ansonsten scrollt die Card nie selbst, damit das Dashboard auf Touch-Displays immer scrollbar bleibt.

### Raspberry Pi 7" hochkant

Das alte Raspberry-Pi-Display hat 800 × 480 Pixel; hochkant sind das 480 × 800. TouchKio rendert standardmäßig mit Web-Zoom 1,25, die Seite sieht dann nur 384 × 640 CSS-Pixel. Dafür schaltet `compact: auto` im Kiosk die kompakte Darstellung ein (ca. 500 Pixel Höhe statt 700, passt mit Kopfzeile ohne Scrollen). Bei Web-Zoom 1,0 (480 × 800) reicht die normale Darstellung. Mit `compact: on` oder `off` lässt sich das erzwingen.

## Seitenauswahl

Der Picker liest über die Home-Assistant-Schnittstelle die Dashboards (`lovelace/dashboards/list`) und deren Ansichten (`lovelace/config`) und bietet sie gruppiert nach Dashboard an. Bei der Auswahl wird die komplette URL per `text.set_value` in `url_entity` geschrieben.

- Der Adressanfang (z. B. `http://homeassistant.local:8123`) wird aus der aktuell gesetzten Seiten-URL übernommen, weil TouchKio die Adresse so erreicht, wie sie dort steht. Ist noch keine URL gesetzt, wird die Adresse der Home-Assistant-Oberfläche verwendet.
- Eine URL, die in keiner Ansicht vorkommt, wird als „Eigene URL" angezeigt und bleibt unverändert, bis eine andere Seite gewählt wird.
- Dashboards im automatisch generierten Modus liefern keine Konfiguration und erscheinen mit einer einzelnen Startseite.
- Die Auswahl wird einmal beim Laden der Card gelesen; nach neuen Dashboards oder Ansichten die Seite neu laden.

## Bild

Das freigestellte TouchKio-Gerätebild ist direkt in der JavaScript-Komponente eingebettet und wird nicht aus einem Ordner geladen. Mit `show_image: false` wird es ausgeblendet, mit `image_url` durch ein eigenes Bild ersetzt.

## Voraussetzungen und Grenzen

Benötigt werden Home Assistant mit Custom-Card-Unterstützung und die in der Konfiguration zugeordneten Entitäten. Die Karte richtet die Geräteintegration nicht selbst ein. Nicht verfügbare Messwerte werden als solche angezeigt; Gerätestatus und Aktualität hängen von der zugrunde liegenden Integration ab.

Aktionen laufen über die angemeldete Home-Assistant-Sitzung und deren Berechtigungen. Die Bestätigung per zweitem Tippen verhindert versehentliche Bedienung; sie ersetzt keine Berechtigungsprüfung. Eigene Bild-URLs werden vom Browser geladen und können dessen IP-Adresse und Metadaten an den Bildanbieter übertragen. Für lokale Bilder `/local/…` verwenden und keine Zugangsdaten in URLs eintragen.

Die Seitenauswahl schreibt die gewählte URL in die TouchKio-Textentität. Es werden nur Dashboards angezeigt, die die Home-Assistant-Sitzung lesen darf. App-Installation, Neustart und Abschalten benötigen passende Geräteentitäten und Dienste.

## Hinweise zu Marken

Dieses Projekt ist ein unabhängiges Community-Projekt und steht in keiner Verbindung zu TouchKio oder Home Assistant.

## Lizenz

GNU Affero General Public License v3.0 only (**AGPL-3.0-only**).

Nutzung, Änderungen und Weitergabe sind unter den Bedingungen der AGPL erlaubt; abgeleitete Werke müssen unter derselben Lizenz stehen. Bei modifizierten Versionen, die über ein Netzwerk genutzt werden, muss der entsprechende Quellcode den Nutzern zugänglich gemacht werden.

Details stehen in [`LICENSE`](LICENSE).
