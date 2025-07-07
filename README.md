# etf-steuernotizbuch
Kleine Software mit GUI zum Verwalten und Simulieren der Steuerzahlungen auf Gewinne und Vorabpauschalen von Fonds und ETFs unter deutschem Steuerrecht. Besonders geeignet für Auslandsdepots und zur Simulation der anfallenden Steuern bei einem beabsichtigten Verkauf von Anteilen. 

## Kurzanleitung
### Anlegen eines Wertpapiers
Nach dem Start kann über `Datei` - `Öffnen` die Demo-Datei `demo.csv` im Ordner `savefiles` geöffnet werden um die Software auszuprobieren. Alternativ kann mit `Datei` - `Neu` ein neues, leeres Dokument für ein Wertpapier erstellt werden.

Eine Datei stellt immer ein bestimmtes Wertpapier in einem bestimmten Depot dar. Wenn man mehrere Wertpapiere in einem Depot oder mehrere Depots mit dem gleichen Wertpapier hat, ist also für jede Depot-Wertpapier-Kombination eine Datei anzulegen. Dies entspricht der deutschen Steuergesetzgebung die genau eine solche Einzelbetrachtung verlangt.

### Transaktionen eintragen
Ist die Datei angelegt oder geöffnet, können mit `Kauf eintragen` und `Verkauf eintragen` Transaktionen eingetragen werden (es werden nur ganze Anteile unterstützt). Mit `Transaktion löschen` kann eine fehlerhaft eingetragene Transaktion gelöscht werden. 

Wenn Transaktionen eingetragen sind, wird im Diagrammbereich `Vorhandene Chargen` dargestellt, wie die Chargen **heute** aufgebaut sind. Das heißt, bei Verkäufen wurden nach dem Prinzip *First-In-First-Out (FIFO)* (steuergesetzlich vorgegeben) Anteile entnommen. Es verbleibt ein gestapeltes Säulendiagramm das die Anteils-Chargen nach Kaufzeitpunkt, Anzahl der Anteile und Einstandskurs darstellt. 

### Vorabpauschale eintragen
Mit dem Button `Vorabpauschale eintragen` können für einzelne Kalenderjahre Vorabpauschalen eingetragen werden. Es sind die Werte für die *Vorabpauschale* einzutragen, nicht etwa der Wert der bezahlten Steuer darauf. Pro Kalenderjahr ist natürlich nur eine Vorabpauschale erlaubt. Wie bei den Transaktionen können Vorabpauschalen auch mit dem entsprechenden Button gelöscht werden. 
**Bitte beachten: **Dieses Tool beinhaltet absichtlich keinen Rechner um die Vorabpauschale zu berechnen. Es soll die in der Steuererklärung berücksichtigte Vorabpauschale eingetragen werden. Steuersoftware (ich nutze WISO-Steuer) kann die Vorabpauschale für die Steuer berechnen.

### Steuersimulation

Sobald alle im Depot vorhandenen Transaktionen zu dem Wertpapier eingetragen sind, kann mit dem Button `Verkauf simulieren` eine Simulation eines Verkaufs und dessen steuerlichen Auswirkungen angestoßen werden. Für die Richtigkeit des Ergebnisses ist es essenziell, dass alle vorhergehenden Transaktionen ab dem ersten Kauf eingetragen sind. Ebenso sollten alle vorher angefallenen (also versteuerten) Vorabpauschalen inkl. des aktuellen Jahres (fehlen Vorabpauschalen wird der Wert des Gewinns  und damit die simulierte Steuer etwas zu hoch sein).

Einzutragen sind die Anzahl der Anteile, die beabsichtigt werden zu verkaufen sowie eine Schätzung des Verkaufskurses (idR aktueller Kurs).

Im Ergebnisfenster werden einige berechnete Werte dargstellt:
- Oben die trivial berechneten Rahmendaten des Verkaufs. 
- In der Mitte ein scrollbarer Bereich mit den einzelnen verkauften Chargen (ein Teil der vorhandenen Chargen) inklusive Gewinn pro Anteil und der ganzen Charge.
- Im unteren Bereich finden sich dann Gesamtgewinn vor und nach Teilfreistellung sowie die zu erwartende Kapitalertragsteuer (dieser Wert berücksichtigt natürlich nicht Rahmenfaktoren auf der Gesamtebene wie Sparerpauschbetrag oder Günstigerprüfung)

### Jahresssteuerbericht erstellen

Mit dem Button `Jahressteuerbericht erstellen` können Auswertungen für einzelne Kalenderjahre generiert werden. Das ist das Kernfeature dieses Tools da so Werte für eine mögliche Steuererklärung eines Kalenderjahres erhalten werden können. 

**Es ist jedoch eine ausführliche Prüfung der Ergebnisse erforderlich, dieses Tool kann keine Steuerbeartung durchführen. Es ist ebenfalls möglich, dass Fehler in der Berechnung vorhanden sind, ebenso können persönliche Rahmenbedingungen zu einer abweichenden Steuerlast führen**

Bevor der Button genutzt wird, ist es unbedingt erforderlich alle Transaktionen und Vorabpauschalen sorgfältig einzutragen. Kleine Fehler können große Auswirkungen haben. Es ist zu beachten, dass auch im Jahr des Verkaufs am 1.1. eine Vorabpauschale anfällt, diese sollte vorab berechnet werden, zB mit einer Steuersoftware. 

Wenn alles eingetragen ist, kann ein Steuerbericht erstellt werden. Hierzu ist das Jahr einzutragen, für das man die Steuererklärung erstellen will. 

Es öffnet sich ein Ergebnisfenster mit den folgenden Daten: 
- Im oberen Bereich ist ein scrollbarer Bereich mit den einzelnen verkauften Chargen (ein Teil der vorhandenen Chargen) inklusive Gewinn pro Anteil und der ganzen Charge.



