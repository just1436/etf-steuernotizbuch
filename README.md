# ETF-Steuernotizbuch
Kleine Software mit GUI zum Verwalten und Simulieren der Steuerzahlungen auf Gewinne und Vorabpauschalen von Fonds und ETFs unter deutschem Steuerrecht. Besonders geeignet für Auslandsdepots und zur Simulation der anfallenden Steuern bei einem beabsichtigten Verkauf von Anteilen. 

## Wozu dieses Tool gedacht ist - Motivation
Im deutschen Steuerrecht ist seit 2018 die so genannte "Vorabpauschale" für (insb. idR thesaurierende) ETFs und Fonds vorgesehen. Dies führt zu einer komplizierten steuerlichen Situation bei einer Buy-and-Hold-Strategie dieser Produkte, da in der Regel jährlich Vorabpauschalen zu versteuern sind. Die Berechnung dieser ist bereits nicht trivial, jedoch ist es besonders unübersichtlich, wenn die Anteile wieder verkauft werden sollen. Hier ist nämlich für **jeden einzelnen Anteil** nachzuvollziehen, wie viel Vorabpauschale für diesen bereits abgeführt wurde, was sehr kompliziert wird, wenn über die Jahre mehrere Male der gleiche ETF gekauft wurde. Ebenso muss nachvollzogen werden wie viel Gewinn auf jeden einzelnen Anteil besteht, da nur dieser bei Verkauf versteuert werden muss. Hierbei ist insbesondere das FIFO (First-In-First-Out) anzuwenden, es sind also nicht alle Anteile gleich. So lange man einen Broker mit deutschem Sitz nutzt, ist das es dessen Aufgabe diese Informationen zu tracken und für die Steuer bei Verkauf aus- und gegenzurechnen. Hat man jedoch ein Depot im Ausland muss dies als Anleger selbst gemacht werden. 

Diese Informationen nachzuhalten ist schwierig und erscheint auch bei Nutzung eines Tabellenkalkulationsprogramms sehr unübersichtlich. Für mich persönlich war das langfristig nicht parktikabel, ich wollte aber auch nicht auf ein Auslandsdepot (aus verschiedenen Gründen) verzichten. Eine andere Software, die diese steuerlichen Daten nachhalten kann konnte ich trotz längerer Recherche nicht finden, weder Steuersoftware wie WISO noch Portfoliotracker scheinen diese Funktionen anzubieten. 
Zusätzlich bietet diese Software auch die Möglichkeit einer "Steuersimulation", also einer Berechnung der voraussichtlichen Steuer bei Verkauf unter beachtung der vorgenannten Regeln. Dieses Feature war mir bisher nur bei der Comdirect bekannt. Daher kann das Tool auch für Konten im Inland hilfreich sein wenn diese Funktion nicht verfügbar ist, auch um allein einen Überblick über die steuerliche Struktur des Bestands zu haben. 

**Ich freue mich über jede Rückmeldung oder Verbesserungsvorschläge zu diesem kleinen Projekt! Es ist aktuell noch in einer frühen Phase, dennoch war es für mich persönlich bereits nützlich und ich würde mich freuen wenn es auch anderen hilft.**

## Installation

### Per Paketmanager unter Linux
TODO

### Als ausführbare Datei unter Windows
TODO

### Per `pip` (Pypi) (für Windows und Linux mit Python möglich, MacOS nicht getestet)
Das Projekt ist auf Pypi unter https://pypi.org/project/etf-steuernotizbuch/. Eine Installation kann per 

```
pip install etf-steuernotizbuch
```

erfolgen, hierzu sind grundlegende Kenntnisse mit Python bzw. pip erforderlich (muss beides installiert und eine "virtuelle Umgebung" erzeugt werden). Nach Installation kann das Programm einfach mit 
```
etf-steuernotizbuch
```

gestartet werden. Die Demo-CSV-Dateien müssen zusätzlich von Github (https://github.com/just1436/etf-steuernotizbuch) geladen werden. 

### Per Download von Github und Ausführung mit Python (für Windows und Linux mit Python möglich, MacOS nicht getestet)
Das ganze Archiv kann geladen werden (https://github.com/just1436/etf-steuernotizbuch) und dann die `main.py` per Python gestartet werden. Hierfür müssen die Bibliotheken `matplotlib`, `numpy` und `tkcalendar` installiert sein.

```
pip3 install matplotlib numpy tkcalendar
python3 etf_steuernotizbuch/main.py
```


Diese Methode ist geeignet für fortgeschrittene Benutzer da so der Quellcode leicht angepasst werden kann. Ich freue mich auch über Verbesserungsvorschläge im Code auf Github.




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

**Es ist jedoch eine ausführliche Prüfung der Ergebnisse erforderlich, dieses Tool kann keine Steuerbeartung durchführen. Es ist ebenfalls möglich, dass Fehler in der Berechnung vorhanden sind, ebenso können persönliche Rahmenbedingungen zu einer abweichenden Steuerlast führen. Eine individuelle Steuerberatung erfolgt nicht, der Entwickler des Tools ist nicht in steuerberatenden Berufen tätig. Jegliche Ergebnisse sind als experimentell zu betrachten**

Bevor der Button genutzt wird, ist es unbedingt erforderlich alle Transaktionen und Vorabpauschalen sorgfältig einzutragen. Kleine Fehler können große Auswirkungen haben. Es ist zu beachten, dass auch im Jahr des Verkaufs am 1.1. eine Vorabpauschale anfällt, diese sollte vorab berechnet werden, zB mit einer Steuersoftware. 

Wenn alles eingetragen ist, kann ein Steuerbericht erstellt werden. Hierzu ist das Jahr einzutragen, für das man die Steuererklärung erstellen will. 

Es öffnet sich ein Ergebnisfenster mit den folgenden Daten: 
- Im oberen Bereich ist ein scrollbarer Bereich mit den einzelnen verkauften Chargen (ein Teil der vorhandenen Chargen) inklusive Gewinn pro Anteil und der ganzen Charge. Die bereits bezahlte Steuer auf Vorabpauschalen vor dem Verkauf sind hier berücksichtigt und werden als Summe und pro Anteil angegeben. In einer möglichen Steuererklärung für das Jahr sind die Chargen einzeln einzutragen. In WISO-Steuer heißt die Tabelle (Anlage KAP-INV, Bereich "Investmentfonds, die nicht dem inländischen Steuerabzug unterlegen haben") "Verkauf von Investmentanteilen"
- Unten steht noch eine (informatorische) Zusammenfassung der steuerlichen Beträge bezogen auf das Jahr inkl. Gesamtgewinn des Jahres vor und nach Teilfreistellung sowie eine Berechnung der voraussichtlichen Kapitalertragssteuer. 

### Speichern/exportieren
Mit `Datei` - `Speichern` können die Angaben, die bezüglich des Wertpapiers gemacht werden als CSV im Klartext gespeichert werden und mit einem Tabellenkalkulationsprogramm gelesen und manipuliert werden. Es handelt sich bei den gespeicherten Daten lediglich um folgende Informationen:
- Metadaten (A1-A4: Name, Depot, ISIN, Teilfreistellung) 
- Transaktionen: Datum (Spalte B), Anzahl Anteile (Spalte C), Preis eines Anteils (Spalte D), Transaktionstyp (Spalte E, Kauf=True, Verkauf=False), Transaktionskosten (Spalte F)
- Vorabpauschalen: Jahr (Spalte G), Höhe (Spalte H)

**Nicht** enthalten sind aktuell explizit Daten zu den einzelnen Chargen, Steuerdaten usw. da diese durch das Programm jederzeit "on-the-fly" durch das Programm aus den obigen Daten berechnet werden. Eventuell kann bei Bedarf in Zukunft eine Exportfunktion für diese Daten bzw. Steuerberichte hinzugefügt werden. 

