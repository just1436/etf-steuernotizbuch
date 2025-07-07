# etf-steuernotizbuch
Kleine Software mit GUI zum Verwalten und Simulieren der Steuerzahlungen auf Gewinne und Vorabpauschalen von Fonds und ETFs unter deutschem Steuerrecht. Besonders geeignet für Auslandsdepots und zur Simulation der anfallenden Steuern bei einem beabsichtigten Verkauf von Anteilen. 

## Kurzanleitung
### Anlegen eines Wertpapiers
Nach dem Start kann über `Datei` - `Öffnen` die Demo-Datei `demo.csv` im Ordner `savefiles` geöffnet werden um die Software auszuprobieren. Alternativ kann mit `Datei` - `Neu` ein neues, leeres Dokument für ein Wertpapier erstellt werden.

Eine Datei stellt immer ein bestimmtes Wertpapier in einem bestimmten Depot dar. Wenn man mehrere Wertpapiere in einem Depot oder mehrere Depots mit dem gleichen Wertpapier hat, ist also für jede Depot-Wertpapier-Kombination eine Datei anzulegen. Dies entspricht der deutschen Steuergesetzgebung die genau eine solche Einzelbetrachtung verlangt.

### Transaktionen eintragen
Ist die Datei angelegt oder geöffnet, können mit `Kauf eintragen` und `Verkauf eintragen` Transaktionen eingetragen werden (es werden nur ganze Anteile unterstützt). Mit `Transaktion löschen` kann eine fehlerhaft eingetragene Transaktion gelöscht werden. 

Wenn Transaktionen eingetragen sind, wird im Diagrammbereich `Vorhandene Chargen` dargestellt, wie die Chargen **heute** aufgebaut sind. Das heißt, bei Verkäufen wurden nach dem Prinzip *First-In-First-Out (FIFO)* (steuergesetzlich vorgegeben) Anteile entnommen. Es verbleibt ein gestapeltes Säulendiagramm das die Anteils-Chargen nach Kaufzeitpunkt, Anzahl der Anteile und Einstandskurs darstellt. 

### Steuersimulation

Sobald alle im Depot vorhandenen Transaktionen zu dem Wertpapier eingetragen sind,  kann mit dem Button `Verkauf simulieren` eine Simulation eines Verkaufs und dessen steuerlichen Auswirkungen angestoßen werden.
