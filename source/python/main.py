import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showerror
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.backend_bases import key_press_handler
from tkcalendar import DateEntry
import time
import platform
import numpy as np

aktuellePositionenInvalide = False

filetypes = [
        ('CSV Dateien', '*.csv')
]

def speichern():
    dateiname = fd.asksaveasfilename(title='Datei Speichern',defaultextension=".csv", initialdir='*', filetypes=filetypes)
    if dateiname =="":
        return
    zeilenT = 0
    stammdaten = []
    stammdaten.append(fonds.name)
    stammdaten.append(fonds.depot)
    stammdaten.append(fonds.isin)
    stammdaten.append(fonds.teilfreistellung)
    
    tDatum = []
    tAnzahl = []
    tKurs = []
    tIstKauf = []
    tKosten = []
    for transaktion in transaktionen:
        tDatum.append(transaktion.datum)
        tAnzahl.append(transaktion.anzahl)
        tKurs.append(transaktion.kurs)
        tIstKauf.append(transaktion.istKauf)
        tKosten.append(transaktion.transaktionskosten)
        zeilenT+=1
    vJahr = []
    vHoehe = []
    zeilenV = 0
    for vorabpauschale in vorabpauschalen:
        vJahr.append(vorabpauschale.jahr)
        vHoehe.append(vorabpauschale.hoehe)
        zeilenV += 1

    zeilen = max(4,max(zeilenV, zeilenT))
    stammdaten.extend([""]*(zeilen-3))
    tDatum.extend([""]*(zeilen-zeilenT))
    tAnzahl.extend([""]*(zeilen-zeilenT))
    tKurs.extend([""]*(zeilen-zeilenT))
    tIstKauf.extend([""]*(zeilen-zeilenT))
    tKosten.extend([""]*(zeilen-zeilenT))
    vJahr.extend([""]*(zeilen-zeilenV))
    vHoehe.extend([""]*(zeilen-zeilenV))
    
    np.savetxt((dateiname), [p for p in zip(stammdaten, tDatum, tAnzahl, tKurs, tIstKauf, tKosten, vJahr, vHoehe)], delimiter=',', fmt='%s')

def str2bool(v):
    return v.lower() in ("true", "1")

def laden():
    dateiname = fd.askopenfilename(title='Datei Öffnen', initialdir='*', filetypes=filetypes)
    if dateiname =="":
        return
    daten = np.loadtxt(dateiname, delimiter=',', dtype='str')
    transaktionen.clear()
    vorabpauschalen.clear()
    fonds.name=daten[0][0]
    fonds.depot=daten[1][0]
    fonds.isin=daten[2][0]
    fonds.teilfreistellung=float(daten[3][0])

    for reihe in daten:
        if reihe[1] != '':
            transaktionen.append(Transaktion(int(reihe[2]),float(reihe[3]),reihe[1],float(reihe[5]),str2bool(reihe[4])))
        if len(reihe) > 6:
            if reihe[6]!='':
                vorabpauschalen.append(Vorabpauschale(float(reihe[7]), int(reihe[6])))
    buttonsAktivieren()
    update()

def neu():
    transaktionen.clear()
    vorabpauschalen.clear()
    NeuFenster()
    
def onClosingHauptFenster():
    root.quit()

def berechneAktuellePositionen():
    global aktuellePositionenInvalide 
    aktuellePositionenInvalide = False
    aktuellePositionen = []
    for transaktion in transaktionen:
        if transaktion.istKauf:
            aktuellePositionen.append(Position(transaktion.anzahl, transaktion.kurs, transaktion.datum, transaktion.transaktionskosten))
        else:
            anzahl = transaktion.anzahl
            while anzahl > 0:
                if len(aktuellePositionen) == 0:
                    aktuellePositionenInvalide = True
                    return aktuellePositionen
                anzahl = aktuellePositionen[0].verkaufeUndGibRest(anzahl)
                if aktuellePositionen[0].anzahl == 0:
                    aktuellePositionen = aktuellePositionen[1:]
    return aktuellePositionen

def berechnePositionenZuDatum(datum):
    aktuellePositionen = []
    for transaktion in transaktionen:
        if transaktion.datumWert < datum:
            if transaktion.istKauf:
                aktuellePositionen.append(Position(transaktion.anzahl, transaktion.kurs, transaktion.datum, transaktion.transaktionskosten))
            else:
                anzahl = transaktion.anzahl
                while anzahl > 0:
                    if len(aktuellePositionen) == 0:
                        return aktuellePositionen
                    anzahl = aktuellePositionen[0].verkaufeUndGibRest(anzahl)
                    if aktuellePositionen[0].anzahl == 0:
                        aktuellePositionen = aktuellePositionen[1:]
    return aktuellePositionen

def update():
    widthBar = 0.1
    bottom = 0

    aktuellePositionen = berechneAktuellePositionen()
    if aktuellePositionenInvalide:
        transaktionenInvalideLabel.config(text='Aktuelle Transaktionen invalide (mehr verkauft als gekauft)')
    else: 
        transaktionenInvalideLabel.config(text=' ')
    fondsnameLabel.config(text=fonds.name+'\n'+fonds.depot+'\n'+str(fonds.isin), font=('Helvetica', 18, 'bold'))

    fig, ax = plt.subplots()
    for position in aktuellePositionen:
        p = ax.bar(fonds.name, position.anzahl, width=widthBar, label=""+position.kaufdatum +": "+str(position.anzahl)+ " @ " + str(position.kaufkurs) + "€", bottom=bottom)
        bottom += position.anzahl
    canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=2,columnspan=3, rowspan=10, **options)
    ax.set_title("Vorhandene Chargen")
    #plt.legend(title="Line", loc='upper left', reverse=True)

    transaktionenListBox.delete(0,"end")
    
    for transaktion in transaktionen:
        if transaktion.istKauf:
            transaktionenListBox.insert("end", "Kauf "+str(transaktion.datum)+": "+str(transaktion.anzahl)+" Anteile @ "+str(transaktion.kurs)+"€, Kosten: "+str(round(transaktion.transaktionskosten*transaktion.anzahl,2))+"€")
        else:
            transaktionenListBox.insert("end", "Verkauf "+str(transaktion.datum)+": "+str(transaktion.anzahl)+" Anteile @ "+str(transaktion.kurs)+"€, Kosten: "+str(round(transaktion.transaktionskosten*transaktion.anzahl,2))+"€")
            
    vorabpauschalenListBox.delete(0,"end")
    for vorabpauschale in vorabpauschalen:
        if gibAnzahlAnteileZuDatum(vorabpauschale.datumFaelligkeit)<=0:
            vorabpauschalenListBox.insert("end", str(vorabpauschale.jahr)+": "+str(vorabpauschale.hoehe)+"€ (pro Anteil: ERROR)")
            break
        vorabpauschalenListBox.insert("end", str(vorabpauschale.jahr)+": "+str(vorabpauschale.hoehe)+"€ (pro Anteil: "+str(round(vorabpauschale.hoehe/gibAnzahlAnteileZuDatum(vorabpauschale.datumFaelligkeit),2))+"€)")

def kauf():
    KaufFenster()

def verkauf():
    VerkaufFenster()

def transaktionLoeschen(transaktionIndex):
    if len(transaktionIndex)==0: 
        return
    del transaktionen[transaktionIndex[0]]
    update()

def vorabpauschaleLoeschen(vorabpauschaleIndex):
    if len(vorabpauschaleIndex)==0: 
        return
    del vorabpauschalen[vorabpauschaleIndex[0]]
    update()

def steuerberichtErstellen():
    SteuerberichtErstellenFenster()

def verkaufSimulieren():
    VerkaufSimulationFenster()
    
def vorabpauschaleEintragen():
    VorabpauschaleEintragenFenster()

def gibAnzahlAnteile():
    anzahl = 0
    for position in berechneAktuellePositionen():
        anzahl += position.anzahl
    return anzahl

def gibAnzahlAnteileZuDatum(datum):
    anzahl = 0
    for transaktion in transaktionen:
        if transaktion.datumWert<datum:
            if transaktion.istKauf:
                anzahl += transaktion.anzahl
            else:
                anzahl -= transaktion.anzahl
    return anzahl          

def buttonsDeaktivieren():
    vorabpauschaleEintragenButton.config(state="disabled")
    kaufenButton.config(state="disabled")
    verkaufenButton.config(state="disabled")
    verkaufSimulierenButton.config(state="disabled")
    transaktionLoeschenButton.config(state="disabled")
    vorabpauschaleLoeschenButton.config(state="disabled")
    steuerberichtButton.config(state="disabled")

def buttonsAktivieren():
    vorabpauschaleEintragenButton.config(state="active")
    kaufenButton.config(state="active")
    verkaufenButton.config(state="active")
    verkaufSimulierenButton.config(state="active")
    transaktionLoeschenButton.config(state="active")
    vorabpauschaleLoeschenButton.config(state="active")
    steuerberichtButton.config(state="active")

def gibVorabpauschaleImJahr(jahr):
    for vorabpauschale in vorabpauschalen:
        if vorabpauschale.jahr==jahr:
                return vorabpauschale.hoehe
    return 0


def gibAnzahlVorjahresmonateEinerVorabpauschale(vorabpauschale): #berechnet die Anzahl der  Vorjahresmonate die für die Vorabpauschale zählen. Die Anteile, die im Vorjahr erst gekauft werden zählen nur die investierten Monate inkl Kaufmonat, sonst 12
    positionen = berechnePositionenZuDatum(vorabpauschale.datumFaelligkeit)
    monate=0
    for position in positionen:
        if position.kaufdatumWert.tm_year < vorabpauschale.datumFaelligkeit.tm_year - 1: #nicht im Vorjahr gekauft?
            monate += 12 # ganzes Vorjahr gehalten
        else: #im Vorjahr gekauft
            monate += 13 - position.kaufdatumWert.tm_mon #Anzahl angebrochener Monate gehalten
    return monate

def gibSpezielleVorabpauschaleProAnteilEinerPosition(vorabpauschale, position):
    vorabpauschaleHoeheProVorjahresmonate = vorabpauschale.hoehe/gibAnzahlVorjahresmonateEinerVorabpauschale(vorabpauschale)
    vorabpauschaleHoeheProVorjahresmonateProAnteil = vorabpauschaleHoeheProVorjahresmonate / gibAnzahlAnteileZuDatum(vorabpauschale.datumFaelligkeit)

    if position.kaufdatumWert.tm_year < vorabpauschale.datumFaelligkeit.tm_year - 1: #nicht im Vorjahr gekauft?
        return vorabpauschaleHoeheProVorjahresmonateProAnteil * 12 * len(berechnePositionenZuDatum(vorabpauschale.datumFaelligkeit)) # Wert pro Vorjahresmonate * 1 Jahr * Anzahl der Positionen
    else: #im Vorjahr gekauft
        return vorabpauschaleHoeheProVorjahresmonateProAnteil * (13 - position.kaufdatumWert.tm_mon) * len(berechnePositionenZuDatum(vorabpauschale.datumFaelligkeit)) # Wert pro Vorjahresmonate * Monate gehalte * Anzahl der Positionen

def gibVorabpauschalenBisHeuteProAnteil(position):
        summe = 0
        for vorabpauschale in vorabpauschalen:
            if position.kaufdatumWert < vorabpauschale.datumFaelligkeit:
                summe +=  gibSpezielleVorabpauschaleProAnteilEinerPosition(vorabpauschale, position)
        return summe

def gibVorabpauschalenBisDatumProAnteil(position, datum):
        summe = 0
        for vorabpauschale in vorabpauschalen:
            if vorabpauschale.datumFaelligkeit < datum:
                if position.kaufdatumWert < vorabpauschale.datumFaelligkeit:
                    summe += gibSpezielleVorabpauschaleProAnteilEinerPosition(vorabpauschale, position)
        return summe

class Vorabpauschale:
    hoehe = 0
    jahr = 0
    datumFaelligkeit = 0
    def __init__(self, hoehe, jahr):
        self.hoehe = float(hoehe)
        self.jahr = int(jahr)
        self.datumFaelligkeit = time.strptime(str(jahr)+"-01-01", "%Y-%m-%d")

class Transaktion:
    anzahl = 0
    kurs = 0
    datum = ""
    datumWert = 0
    transaktionskosten = 0
    istKauf = True
    def __init__(self, anzahl, kurs, datum, transaktionskosten, istKauf):
        self.anzahl = anzahl
        self.kurs = kurs
        self.datum = datum
        self.datumWert = time.strptime(datum, "%Y-%m-%d")
        self.transaktionskosten = transaktionskosten
        self.istKauf = istKauf
        self.bezahlteVorabpauschalen = []

class Position:
    anzahl = 0
    kaufkurs = 0
    kaufdatum = ""
    kaufdatumWert = 0
    kaufkosten = 0
    def __init__(self, anzahl, kaufkurs, kaufdatum, kaufkosten):
        self.anzahl = anzahl
        self.kaufkurs = float(kaufkurs)
        self.kaufkosten = float(kaufkosten)
        self.kaufdatum = kaufdatum
        self.kaufdatumWert = time.strptime(kaufdatum, "%Y-%m-%d")
        self.bezahlteVorabpauschalen = []
    
    def verkaufeUndGibRest(self, anzahl):
        if self.anzahl < anzahl:
            anzahl -= self.anzahl
            self.anzahl = 0
            return anzahl
        else:
            self.anzahl -= anzahl
            return 0

class Fonds:
    name = "leer"
    depot = "leer"
    isin = ""
    teilfreistellung = 0.3
    def __init__(self, name, depot, isin):
        self.name=name
        self.depot=depot
        self.isin=isin
        self.teilfreistellung = 0.3

class NeuFenster:
    fenster = 0

    nameEingabefeld = 0
    depotEingabefeld = 0
    isinEingabefeld = 0
    teilfreistellungCombo = 0
    

    def onClosingKaufFenster(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()
        
    def bestaetigung(self):
        try:
            fonds.name = self.nameEingabefeld.get()
            fonds.depot = self.depotEingabefeld.get()
            fonds.isin = self.isinEingabefeld.get()
            strTeilfreistellung = self.teilfreistellungCombo.get()
            if strTeilfreistellung == "30%":
                fonds.teilfreistellung=0.3
            if strTeilfreistellung == "0%":
                fonds.teilfreistellung=0
            if strTeilfreistellung == "15%":
                fonds.teilfreistellung=0.15
            if strTeilfreistellung == "60%":
                fonds.teilfreistellung=0.6
            if strTeilfreistellung == "80%":
                fonds.teilfreistellung=0.8
            
        
            update()
            buttonsAktivieren()
            if platform.system() == 'Windows':
                root.attributes('-disabled', 0)
            self.fenster.destroy()
        except:
            tk.messagebox.showwarning(title="Fehler", message="Fehler in den Eingabefeldern, bitte erneut versuchen")
            self.fenster.lift()


    def __init__(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 1)
        self.fenster = tk.Toplevel(root)
    
        # sets the title of the
        # Toplevel widget
        self.fenster.title("Neuen Fonds/ETF anlegen")
    
        # sets the geometry of toplevel
        self.fenster.geometry("400x400")
        self.fenster.protocol("WM_DELETE_WINDOW", self.onClosingKaufFenster)

        # A Label widget to show in toplevel
        tk.Label(self.fenster, text = "Fondsdaten eintragen").pack()

        
        tk.Label(self.fenster, text = "Fonds/ETF Name:").pack()
        self.nameEingabefeld = tk.Entry(self.fenster)
        self.nameEingabefeld.pack(padx=10, pady=10)
        tk.Label(self.fenster, text = "Depot Name:").pack()
        self.depotEingabefeld = tk.Entry(self.fenster)
        self.depotEingabefeld.pack(padx=10, pady=10)
        tk.Label(self.fenster, text = "ISIN: ").pack()
        self.isinEingabefeld = tk.Entry(self.fenster)
        self.isinEingabefeld.pack(padx=10, pady=10)
        tk.Label(self.fenster, text = "Teilfreistellung (Aktienfonds: 30%): ").pack()
        self.teilfreistellungCombo = ttk.Combobox(self.fenster, state="readonly", values=["30%", "0%", "15%", "60%", "80%"])
        self.teilfreistellungCombo.set("30%")
        self.teilfreistellungCombo.pack(padx=10, pady=10)

        bestaetigenButton = tk.Button(self.fenster, text="Fonds/ETF erstellen", command=self.bestaetigung)
        bestaetigenButton.pack(padx=10, pady=10)

class KaufFenster:
    
    fenster = 0
    anzahl = 0
    preis = 0
    datum = ""

    preisEingabefeld = 0
    anzahlEingabefeld = 0
    datumEingabefeld = 0
    kostenEingabefeld = 0


    def onClosingKaufFenster(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()
        
    def bestaetigung(self):
        try:
            datum = str(self.datumEingabefeld.get_date())
            datumWert = time.strptime(datum, "%Y-%m-%d")
            eingetragen = False
            for i, transaktion in enumerate(transaktionen):
                if transaktion.datumWert > datumWert:
                    transaktionen.insert(i, Transaktion(int(self.anzahlEingabefeld.get()), float(self.preisEingabefeld.get().replace(',','.')), datum, float(self.kostenEingabefeld.get().replace(',','.'))/int(self.anzahlEingabefeld.get()), True))
                    eingetragen = True
                    break
            if not eingetragen:
                transaktionen.append(Transaktion(int(self.anzahlEingabefeld.get()), float(self.preisEingabefeld.get().replace(',','.')), datum, float(self.kostenEingabefeld.get().replace(',','.'))/int(self.anzahlEingabefeld.get()), True))
            update()
            if platform.system() == 'Windows':
                root.attributes('-disabled', 0)
            self.fenster.destroy()
        except:
            tk.messagebox.showwarning(title="Fehler", message="Fehler in den Eingabefeldern, bitte erneut versuchen")
            self.fenster.lift()

    def __init__(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 1)
        self.fenster = tk.Toplevel(root)
    
        # sets the title of the
        # Toplevel widget
        self.fenster.title("Neuen Kauf eintragen")
    
        # sets the geometry of toplevel
        self.fenster.geometry("400x400")
        self.fenster.protocol("WM_DELETE_WINDOW", self.onClosingKaufFenster)

        # A Label widget to show in toplevel
        tk.Label(self.fenster, text = "Neuen Kauf eintragen").pack()
        tk.Label(self.fenster, text = fonds.name).pack()
        tk.Label(self.fenster, text = fonds.isin).pack()
        tk.Label(self.fenster, text = "Kaufdatum:").pack()
        self.datumEingabefeld = DateEntry(self.fenster, width=12, background='darkblue',
                        foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd")
        self.datumEingabefeld.pack(padx=10, pady=10)
        tk.Label(self.fenster, text = "Anzahl Anteile:").pack()
        self.anzahlEingabefeld = tk.Entry(self.fenster)
        self.anzahlEingabefeld.pack(padx=10, pady=10)

        tk.Label(self.fenster, text = "Preise pro Anteil in €:").pack()
        self.preisEingabefeld = tk.Entry(self.fenster)
        self.preisEingabefeld.pack(padx=10, pady=10)

        tk.Label(self.fenster, text = "Transaktionskosten (gesamt) in €:").pack()
        self.kostenEingabefeld = tk.Entry(self.fenster)
        self.kostenEingabefeld.pack(padx=10, pady=10)

        bestaetigenButton = tk.Button(self.fenster, text="Kauf eintragen", command=self.bestaetigung)
        bestaetigenButton.pack(padx=10, pady=10)

class VerkaufFenster:
    
    fenster = 0
    anzahl = 0
    preis = 0
    datum = ""

    preisEingabefeld = 0
    anzahlEingabefeld = 0
    datumEingabefeld = 0


    def onClosingKaufFenster(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()
        
    def bestaetigung(self):
        try:
            datum = str(self.datumEingabefeld.get_date())
            datumWert = time.strptime(datum, "%Y-%m-%d")
            eingetragen = False
            for i, transaktion in enumerate(transaktionen):
                if transaktion.datumWert > datumWert:
                    transaktionen.insert(i, Transaktion(int(self.anzahlEingabefeld.get()), float(self.preisEingabefeld.get().replace(',','.'))/int(self.anzahlEingabefeld.get()), datum,float(self.kostenEingabefeld.get().replace(',','.')), False))
                    eingetragen = True
                    break
            if not eingetragen:
                transaktionen.append(Transaktion(int(self.anzahlEingabefeld.get()), float(self.preisEingabefeld.get().replace(',','.')), datum, float(self.kostenEingabefeld.get().replace(',','.'))/int(self.anzahlEingabefeld.get()), False))
            if platform.system() == 'Windows':
                root.attributes('-disabled', 0)
            self.fenster.destroy()
            update()
        except:
            tk.messagebox.showwarning(title="Fehler", message="Fehler in den Eingabefeldern, bitte erneut versuchen")
            self.fenster.lift()


    def __init__(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 1)
        self.fenster = tk.Toplevel(root)
    
        # sets the title of the
        # Toplevel widget
        self.fenster.title("Neuen Verkauf eintragen")
    
        # sets the geometry of toplevel
        self.fenster.geometry("400x400")
        self.fenster.protocol("WM_DELETE_WINDOW", self.onClosingKaufFenster)

        # A Label widget to show in toplevel
        tk.Label(self.fenster, text = "Neuen Verkauf eintragen").pack()
        tk.Label(self.fenster, text = fonds.name).pack()
        tk.Label(self.fenster, text = fonds.isin).pack()

        tk.Label(self.fenster, text = "Verkaufsdatum:").pack()
        self.datumEingabefeld = DateEntry(self.fenster, width=12, background='darkblue',
                        foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd")
        self.datumEingabefeld.pack(padx=10, pady=10)

        tk.Label(self.fenster, text = "Anzahl Anteile:").pack()
        self.anzahlEingabefeld = tk.Entry(self.fenster)
        self.anzahlEingabefeld.pack(padx=10, pady=10)

        tk.Label(self.fenster, text = "Preise pro Anteil in €:").pack()
        self.preisEingabefeld = tk.Entry(self.fenster)
        self.preisEingabefeld.pack(padx=10, pady=10)
        
        tk.Label(self.fenster, text = "Transaktionskosten (gesamt) in €:").pack()
        self.kostenEingabefeld = tk.Entry(self.fenster)
        self.kostenEingabefeld.pack(padx=10, pady=10)

        bestaetigenButton = tk.Button(self.fenster, text="Verkauf eintragen", command=self.bestaetigung)
        bestaetigenButton.pack(padx=10, pady=10)

class VerkaufSimulationErgebnisFenster:
    fenster = 0
    def onClosingKaufFenster(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()
    
    def __init__(self, anzahl, preis):
        self.fenster = tk.Toplevel(root)
        # sets the title of the
        # Toplevel widget
        self.fenster.title("Ergebnis Steuersimulation Verkauf")
        
        tk.Label(self.fenster, text = "Anzahl Anteile die verkauft werden sollen: "+str(anzahl)+" von "+str(gibAnzahlAnteile())).pack()
        tk.Label(self.fenster, text = "Voraussichtlicher Verkaufspreis pro Anteil: "+str(preis)+"€").pack()
        tk.Label(self.fenster, text = "Gesamter Verkaufserlöß: "+str(preis*anzahl)+"€").pack()

        
        tk.Label(self.fenster, text = "Verkaufte Anteilschargen:").pack()
        chargenListboxFrame = tk.Frame (self.fenster)
        chargenListboxFrame.pack()
        chargenListBox=tk.Listbox(chargenListboxFrame, width=140)  
        chargenListBox.pack(side="left")
        scrollbar = tk.Scrollbar(chargenListboxFrame,orient="vertical",command=chargenListBox.yview)
        scrollbar.pack(side ="right", fill = "y" )
        chargenListBox.configure(yscrollcommand=scrollbar.set)
        aktuellePositionen = berechneAktuellePositionen()

        verkaufAnzahl = anzahl
        gewinn = 0
        for position in aktuellePositionen:
            summeVorabpauschalenProAnteil = gibVorabpauschalenBisHeuteProAnteil(position)
            if position.anzahl <= verkaufAnzahl:
                anzahlZuVerkaufen = position.anzahl
                verkaufAnzahl -= position.anzahl
            else:
                anzahlZuVerkaufen = verkaufAnzahl
                verkaufAnzahl = 0
            gewinn += (preis-position.kaufkurs-summeVorabpauschalenProAnteil-position.kaufkosten)*anzahlZuVerkaufen
            chargenListBox.insert("end","["+str(position.kaufdatum)+"] "+str(anzahlZuVerkaufen)+" Anteile @ "+str(position.kaufkurs)+"€ - Gewinn: "+str(round((preis - position.kaufkurs - summeVorabpauschalenProAnteil - position.kaufkosten)*anzahlZuVerkaufen, 2))+"€ - Gewinn pro Anteil: "+str(round(preis - position.kaufkurs - summeVorabpauschalenProAnteil - position.kaufkosten, 2)) + "€ (berücksichtigt: Vorabpauschale pro Anteil " + str(round(summeVorabpauschalenProAnteil,2))+ "€ - Kaufkosten: "+str(float(round(position.kaufkosten*anzahlZuVerkaufen,2)))+"€)")

            if verkaufAnzahl == 0:
                break
        tk.Label(self.fenster, text = "Realisierter Gewinn nach Abzug bezahlter Vorabpauschalen und Kaufkosten vor Teilfreistellung: "+str(round(gewinn,2))+"€").pack()
        tk.Label(self.fenster, text = "Realisierter Gewinn nach Teilfreistellung ("+str(fonds.teilfreistellung*100)+"%): "+str(round(gewinn*(1-fonds.teilfreistellung),2))+"€", font='Helvetica 12 bold').pack()
        tk.Label(self.fenster, text = "Erwartete Kapitalertragssteuer inkl. Soli (26,375%): " + str(round(gewinn*(1-fonds.teilfreistellung)*0.26375,2))+"€", font='Helvetica 12 bold').pack()

        # sets the geometry of toplevel
        self.fenster.geometry("800x400")
        self.fenster.protocol("WM_DELETE_WINDOW", self.onClosingKaufFenster)

class VerkaufSimulationFenster:
    
    fenster = 0
    anzahl = 0
    preis = 0

    preisEingabefeld = 0
    anzahlEingabefeld = 0


    def onClosingKaufFenster(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()
        
    def bestaetigung(self):
        try:
            self.anzahl = int(self.anzahlEingabefeld.get())
            self.preis = float(self.preisEingabefeld.get().replace(",","."))
            VerkaufSimulationErgebnisFenster(self.anzahl, self.preis)
        except:
            tk.messagebox.showwarning(title="Fehler", message="Fehler in den Eingabefeldern, bitte erneut versuchen")
            self.fenster.lift()
    
    def __init__(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 1)
        self.fenster = tk.Toplevel(root)
    
        # sets the title of the
        # Toplevel widget
        self.fenster.title("Steuersimulation Verkauf")
        
        tk.Label(self.fenster, text = "Anzahl Anteile die verkauft werden sollen ("+str(gibAnzahlAnteile())+" verfügbar):").pack()
        self.anzahlEingabefeld = tk.Entry(self.fenster)
        self.anzahlEingabefeld.pack(padx=10, pady=10)

        tk.Label(self.fenster, text = "Voraussichtlicher Verkaufspreis pro Anteil in €:").pack()
        self.preisEingabefeld = tk.Entry(self.fenster)
        self.preisEingabefeld.pack(padx=10, pady=10)

        bestaetigenButton = tk.Button(self.fenster, text="Verkauf simulieren", command=self.bestaetigung)
        bestaetigenButton.pack(padx=10, pady=10)

        # sets the geometry of toplevel
        self.fenster.geometry("400x400")
        self.fenster.protocol("WM_DELETE_WINDOW", self.onClosingKaufFenster)

class SteuerberichtErstellenFenster:
    
    fenster = 0
    jahr = 0

    jahrEingabefeld = 0

    def onClosingKaufFenster(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()
        
    def bestaetigung(self):
        try:
            self.jahr = int(self.jahrEingabefeld.get())
            if self.jahr < 1000 or self.jahr > 9999:
                raise
            SteuerberichtErgebnisFenster(self.jahr)
        except:
            tk.messagebox.showwarning(title="Fehler", message="Fehler in den Eingabefeldern, bitte erneut versuchen")
            self.fenster.lift()
    
    def __init__(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 1)
        self.fenster = tk.Toplevel(root)
    
        # sets the title of the
        # Toplevel widget
        self.fenster.title("Steuerbericht")
        
        tk.Label(self.fenster, text = "Für welches Jahr soll der Steuerbericht erstellt werden? (YYYY)").pack()
        self.jahrEingabefeld = tk.Entry(self.fenster)
        self.jahrEingabefeld.pack(padx=10, pady=10)

        bestaetigenButton = tk.Button(self.fenster, text="Steuerbericht erstellen", command=self.bestaetigung)
        bestaetigenButton.pack(padx=10, pady=10)

        # sets the geometry of toplevel
        self.fenster.geometry("400x400")
        self.fenster.protocol("WM_DELETE_WINDOW", self.onClosingKaufFenster)

class SteuerberichtErgebnisFenster:
    fenster = 0
    def onClosingKaufFenster(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()

    def __init__(self, jahr):
        self.fenster = tk.Toplevel(root)
        self.fenster.title("Steuerbericht "+str(jahr))
      
        tk.Label(self.fenster, text = "Im Jahr verkaufte Anteilschargen:").pack()
        
        chargenListboxFrame = tk.Frame (self.fenster)
        chargenListboxFrame.pack()

        chargenListBox=tk.Listbox(chargenListboxFrame, width=230)  
        chargenListBox.pack(side="left")

        scrollbar = tk.Scrollbar(chargenListboxFrame,orient="vertical",command=chargenListBox.yview)
        scrollbar.pack(side ="right", fill = "y" )
        chargenListBox.configure(yscrollcommand=scrollbar.set)
        gewinn = 0
        for transaktion in transaktionen:
            if not transaktion.istKauf:
                if transaktion.datumWert.tm_year == jahr:
                    positionen = berechnePositionenZuDatum(transaktion.datumWert)
                    verkaufAnzahl = transaktion.anzahl
                    verkaufPreis = transaktion.kurs
                    for position in positionen:
                        
                        summeVorabpauschalenProAnteil = gibVorabpauschalenBisDatumProAnteil(position, transaktion.datumWert)
                        if position.anzahl <= verkaufAnzahl:
                            anzahlZuVerkaufen = position.anzahl
                            verkaufAnzahl -= position.anzahl
                        else:
                            anzahlZuVerkaufen = verkaufAnzahl
                            verkaufAnzahl = 0
                        aktGewinn = (verkaufPreis - position.kaufkurs - summeVorabpauschalenProAnteil - position.kaufkosten - transaktion.transaktionskosten)*anzahlZuVerkaufen
                        gewinn += aktGewinn
                        chargenListBox.insert("end","Verkauft "+str(anzahlZuVerkaufen)+" Anteile am " + transaktion.datum + " zu " + str(transaktion.kurs)+ "€ (Verkaufskosten: "+str(float(round(transaktion.transaktionskosten*anzahlZuVerkaufen,2)))+"€) | gekauft am "+position.kaufdatum+" zu "+str(position.kaufkurs)+"€ (Kaufkosten: "+str(float(round(position.kaufkosten*anzahlZuVerkaufen,2)))+"€) | bezahlte Vorabpauschalen (gesamt): " + str(round(summeVorabpauschalenProAnteil * anzahlZuVerkaufen,2)) + "€ | bezahlte Vorabpauschalen pro Anteil: "+str(round(summeVorabpauschalenProAnteil,4))+"€ | Gewinn: "+str(round(aktGewinn,2))+"€")
                        if verkaufAnzahl == 0:
                            break
        
        tk.Label(self.fenster, text = "Gewinn aus Verkäufen "+str(jahr)+" vor Teilfreistellung: "+str(round(gewinn,2))+"€").pack()
        vorabpauschale = gibVorabpauschaleImJahr(jahr)
        tk.Label(self.fenster, text = "Vorabpauschale "+str(jahr)+" vor Teilfreistellung: " + str(vorabpauschale)+"€").pack()
        gewinnVorTeilfreistellung = gewinn+vorabpauschale
        tk.Label(self.fenster, text = "Gewinn "+str(jahr)+" vor Teilfreistellung: "+str(round(gewinnVorTeilfreistellung,2))+"€").pack()
        gewinnNachTeilfreistellung = gewinnVorTeilfreistellung*(1-fonds.teilfreistellung)
        tk.Label(self.fenster, text = "Gewinn "+str(jahr)+" nach Teilfreistellung "+str(fonds.teilfreistellung*100)+"%: "+str(round(gewinnNachTeilfreistellung,2))+"€").pack()
        tk.Label(self.fenster, text = "Erwartete Kapitalertragssteuer "+str(jahr)+" inkl. Soli (26,375%): " + str(round(gewinnNachTeilfreistellung * 0.26375,2))+"€").pack()
        
        # sets the geometry of toplevel
        self.fenster.geometry("1500x400")
        self.fenster.protocol("WM_DELETE_WINDOW", self.onClosingKaufFenster)

class VorabpauschaleEintragenFenster:
    jahr = 0
    hoehe = 0
    fenster = 0

    jahrEingabefeld = 0
    hoeheEingabefeld = 0
    def onClosingKaufFenster(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()
        
    def bestaetigung(self):
        try:
            jahr = int(self.jahrEingabefeld.get())
            if jahr < 1000 or jahr > 9999:
                raise
            float(self.hoeheEingabefeld.get())
        except: 
            tk.messagebox.showwarning(title="Fehler", message="Fehler in den Eingabefeldern, bitte erneut versuchen")
            self.fenster.lift()
            return
        eingetragen = False
        for i, vorabpauschale in enumerate(vorabpauschalen):
            if vorabpauschale.jahr==jahr:
                tk.messagebox.showwarning(title="Fehler", message="Vorabpauschale für dieses Jahr ist bereits eingetragen, bei  Korrektur bitte alte Eintragung zuerst löschen")
                self.fenster.lift()
                return
            if vorabpauschale.jahr > jahr:
                vorabpauschalen.insert(i, Vorabpauschale(self.hoeheEingabefeld.get(), jahr))
                eingetragen = True
                break
        if not eingetragen:
            vorabpauschalen.append(Vorabpauschale(self.hoeheEingabefeld.get(), jahr))
        update()
        if platform.system() == 'Windows':
            root.attributes('-disabled', 0)
        self.fenster.destroy()

    def __init__(self):
        if platform.system() == 'Windows':
            root.attributes('-disabled', 1)
        self.fenster = tk.Toplevel(root)
    
        # sets the title of the
        # Toplevel widget
        self.fenster.title("Vorabpauschale eintragen")
        tk.Label(self.fenster, text = "Jahr der Vorabpauschale (YYYY):").pack()
        self.jahrEingabefeld = tk.Entry(self.fenster)
        self.jahrEingabefeld.pack(padx=10, pady=10)
        tk.Label(self.fenster, text = "[bitte Jahr eintragen, zu dessen Beginn die Vorabpauschale fällig war]").pack()

        tk.Label(self.fenster, text = "Gezahlte Vorabpauschale:").pack()
        self.hoeheEingabefeld = tk.Entry(self.fenster)
        self.hoeheEingabefeld.pack(padx=10, pady=10)
        tk.Label(self.fenster, text = "[idealerweise mit Steuersoftware ermittelt]").pack()

        bestaetigenButton = tk.Button(self.fenster, text="Vorabpauschale eintragen", command=self.bestaetigung)
        bestaetigenButton.pack(padx=10, pady=10)

        # sets the geometry of toplevel
        self.fenster.geometry("400x400")
        self.fenster.protocol("WM_DELETE_WINDOW", self.onClosingKaufFenster)     


if __name__ == '__main__': #Start des Programms
    fonds = Fonds("Bitte Datei", "erstellen oder öffnen", "")

    vorabpauschalen = []
    transaktionen = []

    # root window
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', onClosingHauptFenster)

    # frame
    frame = ttk.Frame(root) 
    root.title('Steuernotebook ETF-/Fondsanteile')
    root.geometry('1400x800')
    root.resizable(True, True)

    # field options
    options = {'padx': 5, 'pady': 2}

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Neu", command=neu)
    filemenu.add_command(label="Öffnen", command=laden)
    filemenu.add_command(label="Speichern", command=speichern)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Datei", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    #helpmenu.add_command(label="Hilfe Index", command=donothing)
    #helpmenu.add_command(label="Über...", command=donothing)
    menubar.add_cascade(label="Hilfe", menu=helpmenu)

    root.config(menu=menubar)

    fondsnameLabel = ttk.Label(frame, text=fonds.name+'\n'+fonds.depot+'\n'+str(fonds.isin), font=('Helvetica', 18, 'bold'))
    fondsnameLabel.grid(row=0, column=0)

    transaktionenLabel = ttk.Label(frame, text='Transaktionen:')
    transaktionenLabel.grid(row=0, column=5, **options)

    transaktionenListboxFrame = tk.Frame (frame)
    transaktionenListboxFrame.grid(row=1, column=5)

    transaktionenListBox=tk.Listbox(transaktionenListboxFrame, width=60, height=13)  
    transaktionenListBox.pack(side="left")

    scrollbar = tk.Scrollbar(transaktionenListboxFrame,orient="vertical",command=transaktionenListBox.yview)
    scrollbar.pack(side ="right", fill = "y" )
    transaktionenListBox.configure(yscrollcommand=scrollbar.set)

    transaktionenInvalideLabel = ttk.Label(frame, text='')
    transaktionenInvalideLabel.grid(row=2, column=5, **options)

    kaufenButton = tk.Button(frame, text="Kauf eintragen", command=kauf)
    kaufenButton.grid(row=3, column=5, **options)

    verkaufenButton = tk.Button(frame, text="Verkauf eintragen", command=verkauf)
    verkaufenButton.grid(row=4, column=5, **options)

    verkaufSimulierenButton = tk.Button(frame, text="Verkauf simulieren", command=verkaufSimulieren)
    verkaufSimulierenButton.grid(row=5, column=5, **options)

    transaktionLoeschenButton = tk.Button(frame, text="Transaktion löschen", command=lambda: transaktionLoeschen(transaktionenListBox.curselection()))
    transaktionLoeschenButton.grid(row=6, column=5, **options)

    steuerberichtButton = tk.Button(frame, text="Jahressteuerbericht erstellen", command=steuerberichtErstellen)
    steuerberichtButton.grid(row=1, column=0, **options)

    vorabpauschalenLabel = ttk.Label(frame, text='Gezahlte Vorabpauschalen:')
    vorabpauschalenLabel.grid(row=7, column=5)

    vorabpauschalenListboxFrame = tk.Frame (frame)
    vorabpauschalenListboxFrame.grid(row=8, column=5)

    vorabpauschalenListBox=tk.Listbox(vorabpauschalenListboxFrame, width=60)  
    vorabpauschalenListBox.pack(side="left")

    scrollbar = tk.Scrollbar(vorabpauschalenListboxFrame,orient="vertical",command=vorabpauschalenListBox.yview)
    scrollbar.pack(side ="right", fill = "y" )
    vorabpauschalenListBox.configure(yscrollcommand=scrollbar.set)

    vorabpauschaleEintragenButton = tk.Button(frame, text="Vorabpauschale eintragen", command=vorabpauschaleEintragen)
    vorabpauschaleEintragenButton.grid(row=9, column=5, **options)

    vorabpauschaleLoeschenButton = tk.Button(frame, text="Vorabpauschale löschen", command=lambda: vorabpauschaleLoeschen(vorabpauschalenListBox.curselection()))
    vorabpauschaleLoeschenButton.grid(row=10, column=5, **options)

    buttonsDeaktivieren()

    update()

    # add padding to the frame and show it
    frame.grid(padx=10, pady=10)

    # start the app
    root.mainloop()
