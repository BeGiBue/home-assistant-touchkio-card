# Security-Review – home-assistant-touchkio-card

## Umfang und Grenzen

Manuelle Prüfung der gesamten JavaScript-Komponente: HTML-/Attributausgaben,
Konfigurationswerte, Entity-Zustände und Attribute, numerische Styles,
URL-Kontexte, Event-Handler, Home-Assistant-Dienste und WebSocket-Aufrufe.
Keine Fremdbibliotheken, Paketverwaltung oder eigenen Zugangsdaten im Laufzeitcode.
Die Karte verwendet die angemeldete HA-Sitzung; Backend-Berechtigungen bleiben die
Sicherheitsgrenze. Keine direkte Geräte-API und kein eigener WebSocket-Client.
Keine vollständige Prüfung des HA-Core oder der zugrunde liegenden Geräteintegration.

## Befunde

Keine bestätigte Sicherheitslücke im geprüften Laufzeitcode.

| ID | Risiko | Schweregrad | Korrektur / Status |
|---|---|---|---|
| TOUCH-01 | Frei konfigurierte Bild-URL überträgt Browser-Metadaten an den Bildanbieter; HTTP ohne Transportschutz. URL wird als `img.src` escaped. | Niedrig / Konfigurationsrisiko | Lokale `/local/…`-Bilder empfohlen, keine Credentials in URLs; in der README dokumentiert. |
| TOUCH-02 | Dashboard-Liste und Seitenwahl verwenden die Rechte der angemeldeten HA-Sitzung; die gewählte URL wird in die Textentität geschrieben. Fremde Ziel-Origin kann bewusst konfiguriert sein. | Informativ / Vertrauensgrenze | Nur vertrauenswürdige HA-/TouchKio-Konfiguration verwenden. Keine direkte Navigation oder Credential-Übermittlung durch diese Karte. |

## Vertrauensgrenzen

Entity-Zustände, Einheiten, Paketnamen/-versionen, Optionswerte und Dashboard-Titel/-Pfade
werden für Text-/Attributkontexte escaped. Helligkeit, Fortschritt und Skalierung
werden numerisch konvertiert. Es gibt keine im HTML erzeugten Inline-Event-Handler.
Dienste nutzen die HA-Sitzung; Neustart/Abschalten und unterstützte App-Installation
verlangen standardmäßig ein zweites Tippen. Die Frontend-Bestätigung ersetzt keine
Backend-Autorisierung.

## Automatische Prüfungen

Der Workflow „Validate“ (`.github/workflows/validate.yml`) führt bei Push auf `main`,
Pull Requests und manuell aus:

- HACS-Validierung (`hacs/action`, Kategorie `plugin`)
- Syntaxprüfung: `node --check touchkio-card.js`
- Regressionstests: `node --test tests/*.test.mjs` (Entity-Zustände, Konfigurationswerte,
  Bildattribute, Paketliste, Optionswerte, Dashboard-API-Daten)

## Restrisiken

Keine offenen kritischen oder hohen Befunde im geprüften Umfang. Nicht automatisch
geprüft wird das Verhalten in einer echten Home-Assistant-Instanz (Bedienung,
grafischer Editor, bestehende Dashboard-Konfigurationen).
