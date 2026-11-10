# Lauf baer-2c: Bau Gebiss + Zunge (10.11.2026, 05:50-07:25)

Blender 5.2.3, JDK 25, PZ 42.21. **Statisch/offline gebaut, gemessen und gerendert, nicht gespielt.**
- Nichts in die Test-Mod NCBearTest geschrieben (GLB dort weiter 5066fa67), nichts nach NPC Crew, nichts committet, nichts hochgeladen.
- Originale `*_pfote.py` unveraendert (MD5 9ae68692 / 402f9f5b / 14fceba9 / 380f259f / a14a4e1b).
- Geaendert bzw. neu in `baer/spiel/`: **`baer_maul_2c.py` (neu, MD5 be09fe8e)**, `baer_kampf_2c.py` (nur zwei Aufrufstellen + Kopfzeile, MD5
  b1575c19; vorher cf5e18af, Kopie `_arbeit/baer_2c/log/baer_kampf_2c_vor_gebiss_cf5e18af.py`), `baer_export_2c.py` (nur die Flecken-
  Konstanten, MD5 85eb1f11; vorher a44ad5c3, Kopie `gebiss/werkzeug/baer_export_2c_vor_gebiss_a44ad5c3.py`). quelle/gewichte/textur_2c
  unveraendert (72230dae / 8bdd899a / fbd67ac7).
- Fremde `_arbeit/baer_*`-Ordner nur gelesen. Renders nur RTX 4090/OptiX + OptiX-Entrauscher ueber `gebiss/werkzeug/gpu_render.sh`
  (Sperre `gpu.lock`, nicht auf das Spiel geprueft). Alle Bilder unten habe ich angesehen.
- Kevins Bruell-Vorlage nur angesehen (Ansehkopie der Forschung `referenz/`); sie steckt in keinem Modell/keiner Textur. Blaetter mit
  Vorlage: nur `bilder/gebiss_vorlage_ton.png` (nur lokal, nie weitergeben).

## 0. Kurz

| Ziel (SPEZ 3 / 8) | neu (Endstand `glb_2c`, GLB 0ce2661e) | heute (baer-pfoten) | Soll | ok |
|---|---|---|---|---|
| Eckzahn oben: Krone unter der Lippenlinie | **4,36 cm**, 35 Grad Bogen nach hinten, 10 vorn, 10 nach innen, 6-seitig, kraeftig | 3,0 cm gerader Kegel, 1,5-2 sichtbar | 4,6 (4,2-5,0) | ja |
| Eckzahn oben: Lage / Basis | a 0,439, \|b\| 4,8 cm / Oval 2,1 x 1,6 cm | a 0,430, 4,4 / r 0,75 | a 0,440-0,450, \|b\| 4,4-5,0 / 2,3 x 1,7 | a 1 mm vor dem Band, Basis 2 mm schmaler (Platz zum unteren Eckzahn, 4.2) |
| Eckzahn unten: Krone ueber der Lippe / Lage | **3,84 cm**, 45 Grad Bogen, 15 vorn, 8 aussen / a 0,462, \|b\| 3,5; steht VOR und innen vom oberen | 2,8 cm, hinter dem oberen | 4,0 (3,6-4,8) / a 0,462, 3,4-4,0 | ja |
| Schneidezaehne 6 + 6 | oben 1,20/1,30/1,45 hoch, 0,90-1,00 breit, Vorderkante 1,37 cm hinter der Lippe; unten 0,95-1,10 / 0,82-0,90, 0,6 cm | keine | oben >= 1,3, unten >= 0,5 cm | ja |
| Backenzaehne angedeutet | je Kiefer/Seite eine Hoecker-Leiste, 24 Dreiecke, 1,1/1,0 cm hoch, oben 5,3 / unten 5,9 cm lang | keine | 1,0-1,2 hoch, 6-8 cm | Laenge knapp darunter (Mundwinkel, 7.4) |
| Zunge | eigener geschlossener Koerper am Kiefer, 10 cm lang, hinten 7,2 / vorn 4,2-5,4 cm breit, 1,4 cm dick, Raender 0,25-0,4 hoeher, Spitze rund 1,6 cm hinter den unteren Schneidezaehnen, Oberseite 1,1 cm unter deren Spitzen | flaches Blatt 20,7 cm breit | 7-8 / 5-6 / 1,2-1,5 / 0,3-0,5 / 1,5-2,0 / >= 0,5 | ja |
| Gaumen, Zahnfleisch, Lefzen, Rachen | Gaumen gewoelbt 1,7-1,85 cm ueber dem Zahnfleisch, 8 gemalte Querrillen + Naht; Zahnfleischwall ~1 cm um beide Reihen; innerer Lippenstreifen schwarz (28/24/24) die ersten 1,3 cm, bis 2,3 cm rosa; Rachen dunkel 40/20/22 | flache Blaetter | wie 3.3 | ja (Lefze aussen nur Vorschlag, 6) |
| Maul zu: Zahn ausserhalb der Haut / Luft zur Haut | **0** / Kronen >= **8,1 mm** (Eckzaehne 8,3-9,8), Zahnfuesse alle im Fleisch | 0 / 18 mm | 0 / >= 2 mm | ja |
| Jede Kieferlage aller 15 Clips (124 Winkel 0-38 Grad): Krone durch Gaumen/Boden/Zunge | **0**; kleinste Luft 2,1 mm (oberer Eckzahn, Idle 0), sonst >= 2,4 | nicht geprueft | 0 Durchstich | ja |
| Oben gegen unten beim Schliessen (0-3 Grad) | 0 Punkte im anderen Zahn | | <= 2 mm Ueberlappung | ja |
| Spielgroesse (pxu 560, el 30, Rear 48) | obere Eckzaehne je **11-13 px hoch** (heute 4-6); Zahn minus Rachen **89-95** (heute 44-83) | | >= 5 px / >= 80 | ja |
| Dreiecke Maul innen | **1.146** (Waende oben 233 + Gaumen 96, unten 289 + Boden 96, Zaehne 336, Zunge 96) | 330 | 874 Soll, >= 700 | ueber Soll (+272), im Haushalt |
| Dreiecke GLB | **19.806** | 19.426 | <= 19.850 (Ziel), 20.000 hart | ja |
| Maske M2/Kopf: alle Punkte ausser Mundhoehle | **11.294/11.294 mit allen 16 Werten bit-gleich** zu Bau Sitzen (Lage, Gewichte, Knochen, UV, Normale); Lippenkante 34/34 Lagen; Kopf 1.333/1.333 Lage+UV+Gewichte (kopf.py) | | bit-gleich | ja |
| Kopf-Texel | Body-PNG: geaendert nur x 272-506, y 0-109 (neue Flecken + 4 px), 0 Texel ausserhalb | | bit-gleich ausser Flecken + 4 px | ja |
| Clips / Skelett | 15/15 bit-gleich zu Bau Sitzen; gegen heute 12 bit-gleich, SitDown/Sit/StandUp = Bau Sitzen | | | ja |
| Einfluesse / Summe / negative | max 4 / 1,000000 / 0 | | | ja |
| Bau Koerper/Sitzen-Messungen | Rumpf 0,794, Ei 0,993, Dehnung 99,5 % 2,49 / max 3,68 / Achsel 3,51, Falten 688 (Achsel+Ellbogen 254), Boden wie Bau Sitzen, Liegehoehe 1,12 cm | | | unveraendert (offen aus Bau Koerper bleibt offen) |

Im Ton und mit Textur (`bilder/gebiss_bruellen_ton.png`): beim Bruellen vier lange gebogene Eckzaehne an den Maulecken, oben und unten
eine Reihe Schneidezaehne, seitlich Hoecker-Leisten, rosa-mauve Schleimhaut, dunkler Rachen, Gaumen mit Querrillen; von oben liegt die
Zunge flach und tief im Unterkiefer. Maul zu: kein Zahn sichtbar. **Die Maul-Oeffnung selbst bleibt der Kasten** (Aussenform fest) und die
Lefzen sind aussen fellbraun -- dazu 6 und 7.

## 1. Wie gebaut (`baer/spiel/baer_maul_2c.py`, 898 Zeilen, reines numpy)

- **Auslagerung zuerst als Null-Probe:** v0 = woertliche Kopie von `maul_bauen`/Flecken aus `baer_kampf_2c.py`; damit gebaut ergab das GLB
  genau 1427f367 (= `glb_sitzen`), Body-PNG und Dump byte-gleich (`gebiss/bau_v0/`). Erst danach der neue Innenraum.
- `baer_kampf_2c.py` :2380-2390 importiert `baer_maul_2c`, prueft vor dem Bau, dass dessen Kopfrahmen-Formeln **bit-gleich** rechnen
  (500 Zufallspunkte, `assert`), kann die Eingabe als npz ablegen (`NCB_MAUL_EINGABE`) und ruft `MAUL.maul_bauen`; :2704 `MAUL.flecken_malen(kl)`.
- **Woertlich behalten** (`baer_maul_2c.py` :1-120, :475-582): Kopfrahmen, `fleck_uv`, `kiefer_anteil`, der Schnitt an der Lippenlinie
  (Zwillinge, UV-Versatz der Unterlippe), die Gewichtsrechnung der Aussenhaut (:762-781). Deshalb bleiben M2 und der ganze Kopf bit-gleich.
- **Neu ab :583:**
  - Rachennaht mit 7 statt 5 Punkten (Gewicht 0,5 wie bisher).
  - Je Kiefer eine Mundhoehle aus Ringen um die Mitte a = 0,37, beschrieben als Tabellen (X, \|Y\|, h) im Plan in cm (`RING_O` :238,
    `RING_U` :262).
    - Oben: Vorhof aussen / innen -> Zahnfleisch aussen -> Zahnreihe -> Zahnfleisch innen -> Gaumenrand -> Gaumendach.
    - Unten zusaetzlich eine Wand halb zwischen Haut und oberem Eckzahn.
    - Zwischen den Ringen wird nach dem Winkel verzahnt (`zip_ringe` :211), mit dichteren Punkten bei theta 20-55 Grad (`_dichte` :195).
  - **Taschen:** oben 4,4 cm hoch fuer den unteren Eckzahn (Luecke zwischen I3 und C), unten 4,7-4,75 cm tief fuer den oberen Eckzahn.
    Ihre Waende sind nach gemessenem Raum gesetzt (`gebiss/werkzeug/raum_tasche.py`: Haut- und Zahn-Radius je Winkel und Hoehe).
  - Gewichte der neuen Punkte ueber `kiefer_anteil` mit der echten Hoehe ueber der Lippe: vor a 0,325 starr (oben Kopf, unten Kiefer),
    zu den Mundwinkeln weich wie die Haut.
  - **Zaehne** (`ZAEHNE` :296, `zahn_netz` :319) und **Zunge** (`ZUNGE` :309, `zungen_netz` :413) als eigene Schalen, Gewicht 1,0 (oben
    Kopf, unten Kiefer). Zaehne sind unten offen, die Zunge ist geschlossen.
    - Zahnfuesse werden nach dem Bau senkrecht mindestens 0,35 cm hinter die eigene Mundhoehle geschoben (:703, `FUSS_TIEF`).
    - Damit ist nie ein offener Zahnboden zu sehen.
  - Ausrichtung der Schalen per Volumen-Vorzeichen wie der Koerper.
  - Pruefungen im Bau: Koerper geschlossen und gleich ausgerichtet (wie bisher); jede Schale ohne doppelte Kante, offen nur am Fussring.
  - Feste Reihenfolge der Teile (anfangs per `set()` -> Dreiecks-Reihenfolge je Python-Lauf anders; behoben, zwei Laeufe jetzt byte-gleich).
- **UV / Flecken** (:93-95, `uv_dreieck` :450, `flecken_malen` :850):
  - Gaumen-Fleck (276,4,92,102): oben Waende nach (Winkel, Weg von der Lippe), darunter der Gaumen eben (X, Y).
  - Zungen-Fleck (372,4,82,102): unten Waende + Boden, darunter die Zunge eben.
  - Zahn-Fleck (458,4,45,102): je Zahnart eine Spalte, Verlauf Zahnfleisch -> Hals 190/170/120 -> Spitze 235/228/210.
  - Farben nach SPEZ 3.3.
- **Abweichung von SPEZ 3.4 (Flecken):** Die Spez-Rechtecke wurden am ALTEN UV gemessen. Bau Koerper hat das UV neu gepackt; im neuen UV
  liegt im Zahn/Lippe-Streifen (467,2,206,25) eine Insel: 689 Texel, mit 3-px-Saum 1.174 (`gebiss/werkzeug/texturplatz_2c.py`,
  `gebiss/texturplatz_2c.png`).
  - Frei ist dort 235 x 110 px bei (272,0) mit 3 px Saum. Darin liegen die drei Flecken oben samt 4 px Malsaum (x 272-506, y 0-109).
  - Keine Insel wandert.
- **`baer_export_2c.py` :144-150, :2705:** `SPERR_FLECKEN` = die drei neuen Rechtecke. Damit prueft :3010, und `baer_textur_2c.py:1497`
  liest sie ueber `E["SPERR_FLECKEN"]`, also keine Aenderung dort.
  - Das Packen sperrt weiter die alten Rechtecke (`SPERR_PACKEN`), damit die Stufe `netz` dasselbe UV liefert.
  - **Nachgewiesen:** `netz`+`fbx` neu laufen lassen -> `netz_2c.npz` gleich (7fa4c262), Assert der neuen Flecken bestanden. Das GLB daraus
    hat dieselben 12.026 Punkte (alle 16 Werte) und dieselben 19.806 gerichteten Dreiecke; nur die Speicher-Reihenfolge ist anders
    (`gebiss/bau_netz`, `gebiss/bau_netzglb`).
  - Die FBX-Datei selbst hat eine andere MD5 (Kopf-Zeitstempel, Versatz 16 Byte).

## 2. Runden (Bilder angesehen)

| Runde | Was | Befund |
|---|---|---|
| v1 | erste Ringe, Zaehne, Zunge | Schnitte (`gebiss/schnitt/v1_zu.png`): riesige Dreiecke quer durchs Maul -> Fehler: kleine Rueckschritte der unregelmaessigen Lippenlinie wurden als Umlauf (+360) gezaehlt; `np.unwrap` + monoton (v1b) |
| v2-v5 | Probe-Runden | Unterer Vorhof vorn ausserhalb der Haut (Kinn hinter der Lippe nur 0,2-0,7 cm tief) -> flacher; Zahnfuesse sichtbar -> automatisch ins Fleisch; Eckzahn oben nur 0,6-1,4 mm Luft |
| v6-v7 | untere Tasche | eine gerade Wand von der Lippe zum Taschenboden lag zwischen Haut und Zahn eng (`v6_eck.png`); Raum je Winkel gemessen, neue Wand L05 halb dazwischen -> 0 Stich |
| v8-v9 | erstes GLB + Renders | Eckzaehne, Reihen, Gaumen, dunkler Rachen lesbar (`gebiss/blatt_v8_a.png`, `blatt_v9_a.png`); Schneidezaehne zu blockig, Lefze kaum schwarz |
| v10-v11 | Eckzahn-Krone kraeftiger ((1-t)^0,6), Schneiden spitzer, Lefzen-Schwarz 1,3 cm; obere Backenleiste hinten aus der Mundwinkel-Mischzone (bei 33,5 Grad 1 Punkt im Koerper) | volle Probe 0 Stich; `gebiss/blatt_v11_a.png` |
| Ende | feste Reihenfolge, `glb_2c` | GLB 0ce2661e zweimal byte-gleich gebaut; Geometrie = v11 (Mengenvergleich) |

## 3. Messungen Endstand

### 3.1 Durchstich-Probe (`gebiss/werkzeug/probe_gebiss_2c.py`, Ausgabe `gebiss/probe_end.txt`)
- Grundlage wie die Probe der Forschung (Windungszahl, `abs(w) > 0,5`).
- Kieferlagen: aus jedem Bild jedes Clips die Lage des Kiefers zum Kopf (S_kopf^-1 S_kiefer), auf 0,25 Grad gerundet (124 Lagen,
  0-38 Grad). Punkte mit Kopf/Kiefer-Gewicht werden gemischt.
- Kronen-Stichproben = Ecken + 7 Flaechenpunkte je Dreieck jenseits der Lippenebene.
- **Maul zu:**
  - Mundhoehle 0 Punkte / 0 von 2.240 Flaechen-Stichproben ausserhalb der Haut.
  - 12 Punkte naeher als 1 mm an der Haut (min 0,2 mm, unten vorn hinter der Lippe), alle innen.
  - Zunge 0 aussen.
  - Kronen 0 aussen, Luft zur Haut 8,1-31,3 mm.
  - Kein Fussring sichtbar.
- **Alle Lagen:** 0 Stich-Punkte bei allen 20 Zaehnen. Kleinste Luft zu Gaumen/Boden/Zunge des anderen Kiefers:
  - Eckzahn oben 2,1 (R) / 2,4 mm (L), unten 3,2 / 5,2.
  - I3 oben 2,7, I1-I2 oben 6,3-6,7, unten 3,4-4,3.
  - Backenleisten 4,7 / 10,9.
- **Zahn in Zahn (0-3 Grad):** keine.
- Schnittbilder: `bilder/gebiss_schnitte_ton.png` (zu / 5 / 14 Grad).

### 3.2 Feste Regeln (`gebiss/werkzeug/maske_2c.py` -> `glb_2c/log/maske_2c.txt`; `werkzeug/kette/glb_pruef.py` -> `glb_2c/log/glb_pruef.txt`)
- Siehe Tabelle 0.
- Bau-Koerper-Pruefer komplett auf dem neuen Dump (`werkzeug/pruef/messen_2c.sh` -> `pruef_koerper/g11/`, Log `gebiss/log/messen_g11.txt`):
  - kopf 1.333/1.333 (9 Normalen am Nahtrand wie in allen frueheren Laeufen).
  - Boden-Tabelle gleich Bau Sitzen (die 2 "Verstoesse" = Hinterkrallen im Sitzen ueber dem Boden, Bau Sitzen 4.3).
  - Regionen-Tabelle 2,49 / 3,68 / Achsel 3,51.
  - Falten, Ei 0,993, Beine, Rumpf 0,794, Hinterfuss 29,3 cm: alles wie Bau Koerper/Sitzen.
  - Sitz-Masse: nicht neu gemessen, weil Haut, Gewichte und Clips bit-gleich sind (3.2 Zeile 1).
- **Dehnung der Mundhoehle selbst:** Die amtliche Regel laesst den Kopf aus.
  - Eigene Rechnung (`gebiss/werkzeug/dehnung_maul.py`, Log `gebiss/log/dehnung_maul.txt`): alt (Beutel) Rear 99,5 % 10,5 / max 14,4 / 22 Dreiecke > 3.
  - Neu: 3,9 / 6,6 / 21 Dreiecke > 3 (Biss 3,6 / 6,0; Fressen 2,8 / 4,6).
  - Ort: Rachen-/Mundwinkelflaechen zwischen Ober- und Unterkiefer (Gewicht 0,5).
  - Die Rohzeile "Kopf (fest)" im Regionen-Log steigt deshalb leicht: Rear max 6,46 -> 6,61; > 3: 25 -> 38.

### 3.3 Spielgroesse (`gebiss/werkzeug/spielgroesse_2c.py`, `gebiss/spiel/end/spielgroesse.txt`)
- Maskenbild je Dreieck (aus UV-Fleck + Kiefergewicht) + Textur Licht B, Rear Bild 48, pxu 560, el 30, az 0 / 45 / 300.
- Obere Eckzaehne je 11-13 px hoch, 3-6 px breit; Helligkeit Eckzahn 136-138, Mundhoehle 42-47, Unterschied 89-95.
- Heute: 4-6 px, Unterschied 44-83.

## 4. Bilder (`bilder/`, Ton UND Textur, alt neben neu, Engine-Normalen; Rumpf-Textur = Platzhalter von Bau Koerper, Kopf-UV/Texel unveraendert)
- `gebiss_bruellen_ton.png` -- Rear 48 mit den Kameras der Forschung a1-a6: vorn, Foto-Blick, schraeg, Seite, von oben (Zunge), von unten
  (Gaumen); je alt Ton | neu Ton | alt Textur | neu Textur.
- `gebiss_halboffen_ton.png` -- Biss 13, Maul 13, Fressen 15, Kauen (Eat 50), Maul 3 Grad, Fressen 14 Grad.
- `gebiss_zu_ton.png` -- Maul zu (Idle 0) Seite/schraeg/vorn/unten: kein Zahn sichtbar.
  - An den Mundwinkeln ein haarfeiner dunkler ">"-Span, gibt es heute auch (Aussenhaut, 6.2).
- `gebiss_spielgroesse_ton.png` -- Spielgroesse alt | neu.
- `gebiss_schnitte_ton.png` -- Schnitte (technisch).
- `gebiss_vorlage_ton.png` -- **mit Kevins Vorlage, nur lokal**: Vorlage oben, darunter neu Ton und neu Textur.
- Einzelbilder `gebiss/render/end_neu`, `end_alt` (1000 px), Arbeitsblaetter `gebiss/blatt_v8_a|v9_a|v9_b|v11_a.png`, `gebiss/blatt_dn.png`.
- **Neue Option `dump_normalen`** in der Kopie `gebiss/werkzeug/render_gebiss.py`:
  - Normalen wie die Engine (aus dem Dump, mit den Knochen gedreht), statt sie am an UV-Naehten getrennten Netz neu zu rechnen.
  - Vorher zeigten die Ton-Bilder Knicke an UV-Naehten, die es im Spiel nicht gibt (Vergleich `gebiss/blatt_dn.png`).

## 5. Gegen Kevins Vorlage (ehrlich)
- **Wie die Vorlage:**
  - Vier lange, gebogene, spitze Eckzaehne an den Maulecken, unten vor und innen von oben.
  - Reihe kleiner Schneidezaehne oben und unten, Backenzaehne angedeutet.
  - Rosa-mauve Mundhoehle mit dunklem Rachen, Gaumen mit Querrillen.
  - Zunge breit, flach, tief im Unterkiefer, Raender leicht hoch (sichtbar von oben, beim Fressen/Kauen).
  - Maul zu sauber.
- **Nicht wie die Vorlage:**
  1. **Oeffnung bleibt ein Kasten** (Lippenlinie und Aussenhaut fest, Kevin: Kopf-Aussenform bleibt). Die Fotos zeigen ein hohes Oval.
  2. **Lefzen aussen fellbraun.** Im Maul ist der Lippenstreifen schwarz. Der schwarze Saum aussen aendert Kopf-Texel (M3) und ist nur
     Vorschlag (6).
  3. Lefzen nicht hochgezogen (Clip-Runde).
  4. Im Ton wirkt das Innere etwas kantig (Ringe mit 20-28 Punkten; mit Textur unauffaellig).
  5. Die Zunge sieht man von vorn kaum (sie liegt tief, wie gewuenscht); von oben/beim Fressen gut.

## 6. Offen / fuer die naechsten
1. **Vorschlag schwarzer Lippensaum aussen (Zone M3)**, nur Vorschlag-Datei, NICHT in den 5 Mod-Dateien:
   - Datei `vorschlag/NCBear_lippensaum.png` = Body-PNG des Endstands + 2.467 Texel.
   - Inhalt: vor dem Mundwinkel (a > 0,265, Auslauf bis 0,30), |c - Lippe| bis 3 mm schwarz, bis 7 mm weich.
   - Blatt `vorschlag/blatt_lippensaum.png`: Endstand | Vorschlag, offen und zu. Ergebnis: deutlich naeher an der Vorlage; zu eine dunkle
     Lippenlinie.
   - Werkzeug `gebiss/werkzeug/vorschlag_lippensaum.py`.
   - Fuer die 2048er WorldItems-Textur muesste der Textur-Bauer es nachziehen. **Entscheidung Kevin/Orchestrator.**
2. **Zipfel/Kasten-Ecke an den Mundwinkeln** (SPEZ 3.3 Wangenhaut):
   - Der dunkle ">"-Span ist Aussenhaut hinter dem Mundwinkel (Forschung 4.5). Er liegt AUSSERHALB der Mundhoehle; eine innere Wangenhaut
     (Weg b) kann ihn nicht verdecken. Deshalb nicht gebaut (0 von 32 Dreiecken).
   - Weg a (Kiefergewichte der 64 unteren Zwillinge) wuerde nach Forschung auch "die Reihe hinter dem Winkel" brauchen. Das ist Kopf-Rest
     (bit-gleich) -> nicht ohne Freigabe; Dehnung neu. Vorschlag fuer die Clip-Runde bzw. Entscheidung.
3. **Dreiecke 1.146 statt 874 (Soll).** Gesamt 19.806 liegt im Ziel <= 19.850 (44 Reserve).
   - Einsparung moeglich, z. B. Ringe oben 28/28/24/24/22/14 -> 26/26/22/22/20/12 (~-50); kostet Rundung der Taschen.
4. **Eckzahn-Basis 2,1 x 1,6 statt 2,3 x 1,7 cm, oben a 0,439 statt >= 0,440.** Mit Spez-Massen beruehren sich oberer und unterer Eckzahn
   am Hals (gerechnet 0-1 mm Abstand), dazwischen muss aber Zahnfleisch und Taschenwand.
5. **Backenleisten 5,3 / 5,9 cm statt 6-8**, obere Luecke hinter dem Eckzahn 2,1 statt 2,5-3,0 cm: Das Maul ist 13 cm lang; hinter
   a 0,32 mischt der Mundwinkel Kopf und Kiefer, dort stach die Leiste bei 33,5 Grad in die Mundhoehle (v10).
6. **Luft unterer Vorhof vorn zur Haut** nur 0,2-1 mm (12 Punkte, innen): das Kinn ist hinter der Unterlippe 0,2-0,7 cm duenn. Kein
   Durchstich, im Spiel ansehen.
7. **Textur:** Body-PNG in `glb_2c` = Platzhalter von Bau Koerper (UV neu) + meine Flecken.
   - Der Textur-Bauer backt neu.
   - `kampf` malt die Flecken danach wieder (`MAUL.flecken_malen`). Die Flecken stehen in `SPERR_FLECKEN` und werden von
     `baer_textur_2c.py:1497` geprueft.
8. **Deer:** `glb_2c/tier/.../NCBearDeer.glb` (7a9f8778, mit dem ORIGINAL `baer_tier_anim.py` aus der FBX b440d693, 18.576 Dreiecke, wie
   bisher ohne Maul-Inneres) nur als Lauf-Beleg; die 5 Mod-Dateien macht der Textur-Bauer.
9. Clip-Runde (nur melden): Lefzen hochziehen / Unterlippe haengen; Zipfel (2).
10. **Nicht gespielt.**

## 7. Wiederholen
```
cd C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c
bash gebiss/werkzeug/glb_bau.sh $PWD/glb_2c/bau                       # GLB-Stufe (~10 s), Netz/Gewichte von Bau Koerper
NCB_MAUL_EINGABE=gebiss/maul_eingabe.npz bash gebiss/werkzeug/glb_bau.sh $PWD/X   # dazu Eingabe fuer Offline-Proben
python gebiss/werkzeug/maul_lauf.py gebiss/maul_eingabe.npz gebiss/X.npz             # maul_bauen ohne Blender (~2 s)
python gebiss/werkzeug/probe_gebiss_2c.py gebiss/X.npz glb_2c/dump_2c.txt AUS.txt [schnell|ab20]   # voll ~4 min
python gebiss/werkzeug/maske_2c.py glb_sitzen/dump_sitzen.txt glb_2c/dump_2c.txt glb_sitzen/42/media/textures/Body/NCBear.png glb_2c/42/media/textures/Body/NCBear.png
SCHNITT_S=42 python gebiss/werkzeug/schnitt_bild.py gebiss/X.npz glb_2c/dump_2c.txt AUS.png 0 r0 r30 r44 r90
python gebiss/werkzeug/auftrag_2c.py DUMP TEXTUR AUSORDNER AUFTRAG.json 1000 alle; bash gebiss/werkzeug/gpu_render.sh gebiss/werkzeug/render_gebiss.py AUFTRAG.json LOG
```

## 8. Dateien (`_arbeit/baer_2c/`)
- **Endstand `glb_2c/`:**
  - `42/media/models_X/Skinned/NCBear.glb` (MD5 0ce2661e76fcc8781d9fb3192eb16721).
  - `42/media/models_X/WorldItems/NCBear.fbx` (b440d693 = Bau Koerper).
  - `42/media/textures/Body/NCBear.png` (7ce60f79, Platzhalter + Flecken).
  - `dump_2c.txt`; `log/` (kampf.log, bericht.json, glb_pruef.txt, maske_2c.txt, Skript-Staende); `tier/` (Deer-Beleg); `bau/`, `bau2/`
    (zwei identische Laeufe).
- **Skripte:** `baer/spiel/baer_maul_2c.py` (neu), `baer_kampf_2c.py`, `baer_export_2c.py` (siehe oben).
- **Bilder:** `bilder/gebiss_*_ton.png` (6 Blaetter, `gebiss_vorlage_ton.png` nur lokal).
- **Vorschlag:** `vorschlag/NCBear_lippensaum.png`, `vorschlag/blatt_lippensaum.png`.
- **Werkzeuge:** `gebiss/werkzeug/`
  - Kopien der Forschung + glb_bau.sh.
  - Neu: maul_lauf.py, probe_gebiss_2c.py, schnitt_bild.py, raum_tasche.py, maul_lage.py, rand_probe.py, texturplatz_2c.py,
    maske_2c.py, spielgroesse_2c.py, auftrag_2c.py, auftrag_extra.py, vorschlag_lippensaum.py, dehnung_maul.py.
  - render_gebiss.py mit `dump_normalen`.
- **Messungen/Logs:** `gebiss/probe_end.txt` (+ probe_v1..v11), `gebiss/spiel/end/spielgroesse.txt`, `pruef_koerper/g11/`, `gebiss/log/`.
- **Bau-Ordner:** `gebiss/bau_v0` (Null-Probe), `bau_v8`, `bau_v9`, `bau_v11`, `bau_netz` + `bau_netzglb` (Reproduzierbarkeit), `gebiss/v*.npz`.
