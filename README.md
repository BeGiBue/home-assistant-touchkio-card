<p align="center">
  <img src="https://raw.githubusercontent.com/BeGiBue/home-assistant-touchkio-card/main/images/touchkio-card-logo-160.png" alt="TouchKio Card" width="160">
</p>

# TouchKio Card

**English** | [Deutsch](https://github.com/BeGiBue/home-assistant-touchkio-card#deutsch)

## English

Home Assistant card for [TouchKio](https://github.com/leukipp/touchkio): control and status of a Raspberry Pi kiosk.

<img src="https://raw.githubusercontent.com/BeGiBue/home-assistant-touchkio-card/main/screenshots/touchkio-normal-350-light.png" width="350" alt="TouchKio Card in normal operation, 350 px wide, light theme">

### Features

- Display brightness slider; tapping the icon turns the display on or off
- On-screen keyboard, kiosk mode and theme as tiles
- Page selection from all Home Assistant dashboards and their views
- Processor temperature, CPU, RAM and package updates with warning colors; tap **Packages** to list available system updates
- Network address and uptime
- App update row with an **Install** button when supported
- Refresh, reboot and shutdown; reboot and shutdown need a second tap
- Compact view for small portrait displays such as a Raspberry Pi 7" in portrait
- Follows your theme; empty entity fields hide their section

The card is shown in German when Home Assistant is set to German, and in English otherwise.

### Requirements

- Home Assistant with custom card support and the TouchKio entities; the card does not set up the device integration itself.
- Actions run with the signed-in user's permissions. Page selection only shows dashboards the session may read. App installation, reboot and shutdown need matching device entities and services.

Independent community project, not affiliated with TouchKio or Home Assistant. License: [AGPL-3.0-only](https://github.com/BeGiBue/home-assistant-touchkio-card/blob/main/LICENSE).

## Deutsch

[English](https://github.com/BeGiBue/home-assistant-touchkio-card#english) | **Deutsch**

Home-Assistant-Karte für [TouchKio](https://github.com/leukipp/touchkio): Steuerung und Status eines Raspberry-Pi-Kiosks.

<img src="https://raw.githubusercontent.com/BeGiBue/home-assistant-touchkio-card/main/screenshots/touchkio-normal-350-light.png" width="350" alt="TouchKio Card im Normalbetrieb, 350 px breit, helles Theme">

### Funktionen

- Display-Helligkeit per Slider; Tippen auf das Symbol schaltet das Display ein oder aus
- Bildschirmtastatur, Kiosk-Modus und Theme als Kacheln
- Seitenauswahl aus allen Home-Assistant-Dashboards und deren Ansichten
- Prozessor-Temperatur, CPU, RAM und Paket-Updates mit Warnfarben; Tippen auf **Pakete** listet die verfügbaren System-Updates
- Netzwerkadresse und Laufzeit
- App-Update-Zeile mit Button **Installieren**, wenn unterstützt
- Aktualisieren, Neustart und Herunterfahren; Neustart und Herunterfahren verlangen ein zweites Tippen
- Kompakte Darstellung für kleine Hochformat-Displays wie den Raspberry Pi 7" hochkant
- Folgt dem Theme; leere Entitätsfelder blenden ihren Bereich aus

Die Karte erscheint auf Deutsch, wenn Home Assistant auf Deutsch eingestellt ist, sonst auf Englisch.

### Voraussetzungen

- Home Assistant mit Custom-Card-Unterstützung und die TouchKio-Entitäten; die Karte richtet die Geräteintegration nicht selbst ein.
- Aktionen laufen mit den Rechten des angemeldeten Benutzers. Die Seitenauswahl zeigt nur Dashboards, die die Sitzung lesen darf. App-Installation, Neustart und Herunterfahren benötigen passende Geräteentitäten und Dienste.

Unabhängiges Community-Projekt, ohne Verbindung zu TouchKio oder Home Assistant. Lizenz: [AGPL-3.0-only](https://github.com/BeGiBue/home-assistant-touchkio-card/blob/main/LICENSE).
