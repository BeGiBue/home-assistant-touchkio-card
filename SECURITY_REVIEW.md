# Security-Review – home-assistant-touchkio-card

Prüfdatum: 2026-10-24. Geprüfte Ausgangsbasis: `1f6875041f47236e70887efc166590c752dbd66a`; Zielversion **2.0.0**.
Zeilenangaben der Befunde beziehen sich auf diese Ausgangsbasis.

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

| ID | Datei / Zeile | Risiko | Schweregrad | Korrektur / Status |
|---|---|---|---|---|
| TOUCH-01 | `touchkio-card.js:282` | Frei konfigurierte Bild-URL überträgt Browser-Metadaten an den Bildanbieter; HTTP ohne Transportschutz. URL wird als `img.src` escaped. | Niedrig / Konfigurationsrisiko | Lokale `/local/…`-Bilder empfohlen, keine Credentials in URLs; im README dokumentiert. |
| TOUCH-02 | `touchkio-card.js:100–147`, 230 | Dashboard-Liste und Seitenwahl verwenden die Rechte der angemeldeten HA-Sitzung; die gewählte URL wird in die Textentität geschrieben. Fremde Ziel-Origin kann bewusst konfiguriert sein. | Informativ / Vertrauensgrenze | Nur vertrauenswürdige HA-/TouchKio-Konfiguration verwenden. Keine direkte Navigation oder Credential-Übermittlung durch diese Karte. |

Entity-Zustände, Einheiten, Paketnamen/-versionen, Optionswerte und Dashboard-Titel/-Pfade
werden für Text-/Attributkontexte escaped. Helligkeit, Fortschritt und Skalierung
werden numerisch konvertiert; der Live-Slider verwendet ausschließlich `Number(sl.value)`.
Es gibt keine im HTML erzeugten Inline-Event-Handler. Dienste nutzen die HA-Sitzung;
Neustart/Abschalten und unterstützte App-Installation verlangen standardmäßig ein
zweites Tippen. Die Frontend-Bestätigung ersetzt keine Backend-Autorisierung.

## Verifikation

- `node --check touchkio-card.js`: bestanden.
- `node tests/security.test.mjs`: **3 Tests bestanden** (Entity/Config/Update/Bildattribute,
  Paketliste, Optionswerte und Dashboard-API-Daten).
- `git diff --check`: bestanden.
- CI führt Syntax- und Regressionstests neben bestehender HACS-Prüfung aus.

## Release-Einschätzung

Keine offenen kritischen oder hohen Befunde im geprüften Umfang. Vor Veröffentlichung
HACS-CI sowie Bedienung, grafischen Editor und bestehende Dashboard-Konfigurationen
in einer echten HA-Instanz prüfen. Keine Releases oder Tags durch diesen Auftrag.
Die Major-Version markiert die Aufnahme in den offiziellen HACS-Katalog; sie bedeutet
nicht automatisch Breaking Changes.
