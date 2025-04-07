# Raumklimamonitor

Der **Raumklimamonitor** ist eine Home Assistant-Integration zur Überwachung und Analyse des Raumklimas in Echtzeit. Diese Integration nutzt Temperatur- und Luftfeuchtigkeitssensoren, um das Raumklima zu bewerten und gibt Empfehlungen zur Lüftung basierend auf diesen Werten.

## Funktionen

- **Überwachung des Raumklimas**: Anzeigen der aktuellen Temperatur und Luftfeuchtigkeit im Raum.
- **Raumklimastatus**: Berechnung und Anzeige des Raumklimastatus, z. B. „optimales Klima“, „akzeptables Klima“ oder „ungünstiges Klima“.
- **Lüftungsempfehlungen**: Automatische Empfehlungen zum Lüften basierend auf Temperatur und Luftfeuchtigkeit.
- **Anpassbare Icons und Texte**: Du kannst Icons und Texte für jeden Raumklima-Status über das UI ändern.
- **Automatisierungen**: Die Lüftungsempfehlungen können eine Automatisierung starten, um beispielsweise ein Fenster zu öffnen.

## Installation

### Installation über HACS (Home Assistant Community Store)

1. **Füge das Repository zu HACS hinzu**:
   - Öffne **Home Assistant** und gehe zu **HACS**.
   - Gehe zu **"Integrationen"** und klicke auf **"Repositories verwalten"** (drei Punkte oben rechts).
   - Füge die URL dieses Repositories hinzu:
     ```
     https://github.com/dein-benutzername/raumklimamonitor
     ```
   - Setze die **Kategorie** auf **Integration**.

2. **Installiere das Plugin**:
   - Nachdem das Repository hinzugefügt wurde, suche nach **Raumklimamonitor** in der HACS-Integrationen-Seite.
   - Klicke auf **Installieren** und starte Home Assistant neu.

### Manuelle Installation

1. **Kopiere das Repository** in das Verzeichnis `custom_components` deines Home Assistant:

2. **Füge die Konfiguration hinzu**:
- Öffne deine **`configuration.yaml`** und füge die folgende Zeile hinzu:
  ```yaml
  raumsensor:
    name: "Wohnzimmer"
    device_id: "wohnzimmer_1"
  ```

3. **Starte Home Assistant neu**, um die Integration zu aktivieren.

## Verwendung

### Konfiguration

- **Temperatur- und Luftfeuchtigkeitssensoren**: Wähle die Sensoren für Innen- und Außentemperatur sowie Luftfeuchtigkeit aus, um das Raumklima zu berechnen.
- **Raumklima-Status**: Der Raumklima-Status wird auf Basis der aktuellen Werte berechnet:
- **Optimales Klima**: Der Raum hat ein angenehmes Klima (gute Temperatur und Luftfeuchtigkeit).
- **Akzeptables Klima**: Das Klima ist akzeptabel, aber nicht optimal.
- **Ungünstiges Klima**: Das Raumklima ist nicht ideal, es wird empfohlen zu lüften.

### Automatisierung

Du kannst eine Automatisierung erstellen, die basierend auf den Lüftungsempfehlungen des Raumklimamonitors Aktionen ausführt, wie z. B. das Öffnen eines Fensters.

Beispiel einer Automatisierung:

```yaml
automation:
- alias: 'Lüften bei ungünstigem Raumklima'
 trigger:
   platform: state
   entity_id: sensor.raumklimamonitor_wohnzimmer_ventilation_recommendation
   to: 'Lüften dringend empfohlen'
 action:
   service: script.open_window

