# Lauf baer-2c: Bau-Spezifikation Beine, Rumpf, Hinterfuss, Sitzen, Kopf-Passung, Gebiss (10.11.2026)

Grundlage: `forschung_beine.md`, `forschung_gebiss.md` (beide ganz gelesen), `_arbeit/baer_pfote/SPEZ_PFOTEN.md`, ENTSCHEIDUNGEN.md
(Abschnitte Sitzen, Gebiss/Beine), Kevins Saetze vom 10.11. ~01:00, eigene Messung und eigene Renders am heutigen GLB (NCBearTest =
Stand baer-pfoten, Dump `forschung/beine/dump/heute.txt`). Kevins Bilder angesehen: `baer/begleiter/kevin_sitzvorlage.png`,
`kevin_sitzen_fuss_kopf.webp` (Ausschnitte vergroessert, `referenz/`, `spez/referenz/`), dazu `kevin_bruellen_vorlage` ueber die
Forschung. **Statisch/offline gemessen und gerendert, nichts gebaut, nichts gespielt.** Nichts in Test-Mod, NPC Crew oder fremde
`_arbeit/baer_*` geschrieben, nichts committet.

Masse in Spielmetern bei Groesse 1,0, Tier-Rahmen x vorn, y links, z oben, linke Seite (rechts = y gespiegelt), Ruhe = Bind-Pose
des GLB. **Alle Soll-Zahlen maschinenlesbar in `spez/soll_2c.json`** -- Bauer und Pruefer lesen die Zahlen dort, nicht aus dem Text.
Kameras wie `render_optik.py` (az 0 = von vorn, +90 = von seiner linken Seite, el ueber dem Boden).

-------------------------------------------------------------------------------------------------------------------------------

## 0. Kurz (Entscheidungen)

1. **Kevins Spielkamera ist nachgestellt:** az 0, el 30, Clip `NCBear_Sit` Bild 60 (2,0 s) deckt sein Spielbild (Kopfdrehung,
   Fellball, Fuesse, Krallen) -- `spez/blaetter/b1_sitzen_spielkamera.png`. Das ist die Abnahmekamera fuer C2/C3.
2. **C1 Hinterfuss:** heute 43,4 cm Haut (46,2 mit Krallen) x 18,7 cm, im Sitzen sichtbar 2,1-2,4 mal so lang wie breit, Sohle
   hellgrau (Texel RGB 128/118/104). **Soll 29 +-1 cm** (Ferse x -0,555, Zehen vorn x -0,265), breit 19-21 cm mit Fell, runde breite
   Ferse, fuenf grosse Zehenballen dicht im Bogen, Fellkranz, Sohle dunkelbraun (Median RGB 62/42/30). **Hinterkrallen 7,0 cm nach
   hinten** (Form/UV/Gewichte gleich). Probe: damit stecken sie in Walk/Run NICHT mehr im Boden (-2,23 -> +0,66 cm, -2,58 -> +0,70).
3. **C2 Sitzen:** Kevins Vorlage woertlich (Brust senkrecht) geht mit dem festen Skelett NICHT: die Vorderbeine (63,9 cm) reichen
   dann 22-25 cm nicht bis zum Boden (Gegenprobe K3). Gemessen ueber 1.440 Posen: **aufrechteste Brust mit flachen Pfoten = -40
   Grad** (heute -14). Soll-Pose = Kandidat **K2**: Becken -35, Lende -25, Brust -40, Hals -77, Kopf geradeaus; Hinterbeine eng
   (Fuss-Mitten 62-72 cm statt 118), Ferse auf dem Boden, Vorderpfoten flach zwischen den Hinterbeinen.
4. **K2 braucht eine Sitz-Ausnahme der Gelenkgrenze Kopf gegen Hals: nick bis +60 statt +-35** (nur in SitDown/Sit/StandUp; Beugung
   in Gelenkrichtung, kein Knick gegen das Gelenk). Ohne sie bleibt K1 (alle Grenzen wie heute) -- dann sitzt der Kopf sichtbar
   schlechter (Kragen hinter dem Kopf +14,5 statt +4,1 cm). **Entscheidung Orchestrator/Kevin; Vorgabe der Spez: K2.**
5. **C3 Kopf-Passung:** der "Kragen" ist vor allem der Schulterbuckel HINTER dem Kopf (Spielkamera: Koerper 21-24 cm ueber der
   Kopf-Oberkante, an den Kopfseiten bis +14 cm). Haltung K2 senkt das auf +4 / -7 bis -14 cm; schmalere Schultern (C4) und ein
   flacherer Nacken (x 0,40-0,60 um 3-5 cm) sollen den Rest bringen. Soll: Koerper hinter dem Kopf <= +2 cm, an den Seiten <= -10 cm.
6. **C3 Farbe:** an der Naht selbst ist kein Sprung (Bild 1,02); der Kopf wirkt aufgeklebt, weil sein Inneres heller und glatter ist
   als der Fellring darum (Helligkeit 0,83, Feinkontrast 1,32 im Spielbild). Soll Ring/Kopf >= 0,92 und Kontrast <= 1,20 -- nur ueber
   Koerper-Texel (Hals, Nacken, Kehle, Schulterbuckel). Kopf-Texel und groesserer Kopf (x 1,10-1,15) **nur als Vorschlag-Datei**.
7. **C4 Rumpf:** 0,93 m breit, die Breite sitzt ueber Schultern (halbe 0,467) und Huefte (0,458); Bauchmitte ist schon 0,68-0,70.
   **Soll Gesamtbreite <= 0,82 m (Ideal 0,78)**, Schultern/Huefte halbe Breite <= 0,40.
8. **C5/Ziel A Beine:** Profiltabellen aus der Forschung (4.1) uebernommen, Hinterbein unten an den neuen Fuss angepasst; **keine
   Stufe**: Zunahme je 5 cm Hoehe vorn <= 3,0 cm, hinten <= 3,5 cm, kein Schritt > 1,6 x Mittel.
9. **Ziel B Gebiss:** Vorschlag der Forschung (874 Dreiecke, Sparfassung 700) wird Soll; Eckzaehne 2,1-3,1 cm innen (feste
   Aussenform), Lefzen-Hochziehen bleibt fuer die Clip-Runde, schwarzer Lippensaum aussen nur als Vorschlag.
10. **Haushalt:** 19.426 heute; Gebiss +544, Behang +250, Ruecken -280, kuerzere Hinterfuesse -300 -> **rund 19.640** (Grenze
    20.000, Ziel <= 19.850).
11. **Reihenfolge:** (1) Bau Koerper -> (2) Bau Sitzen; (3) Bau Gebiss parallel in eigener Datei `baer_maul_2c.py`; (4) Textur + 5
    Dateien. 12 Clips bleiben bit-gleich, neu sind nur SitDown/Sit/StandUp (Dauer, Proben, Schleife, Ereignisse wie heute).

-------------------------------------------------------------------------------------------------------------------------------

## 1. Messung heute gegen Vorlage und Spielbild

Werkzeuge `spez/werkzeug/`: `mess_sitz.py` (Posen, Masse je Kamera; Log `spez/log/mess_sitz_heute.txt`), `mess_brustband.py`,
`mess_naht.py` (Bild), `mess_texel_naht.py` (Texel), `sitz_fk.py` + `sitz_fk_suche.py` + `sitz_kand.py` (Vorwaertskinematik der
Sitzpose, Kontrolle gegen den heutigen Clip: Schulter 0,729 statt 0,720, Kopf oben 1,180 statt 1,191, Kragen-Masse gleich),
`krallen_probe.py`, `raster.py`, `blatt.py`, `render_optik.py` (Kopie, neu: Feld `punkte`), `gpu_render.sh`.

| Mass | Vorlage (px, 3/4-Sicht az ~-30) | Kevins Spielbild (px) | heute Modell | Soll |
|---|---|---|---|---|
| Kopfbreite / Brust 5-25 cm unter dem Kinn | 240 / 305 = **0,79** | 76 / 142 = 0,54 | vorn el 0: 44-47 / 92 cm = **0,48-0,51** | >= 0,55 (Netz), Vorschlag Kopf x1,12 -> ~0,62 |
| Kopf / Silhouette gesamt (Spielkamera) | 240 / 525 = 0,46 | 76 / 207 = 0,37 | 0,33-0,35 (Bild 0,35) | >= 0,45 |
| Kopfhoehe / Sitzhoehe | 228 / 578 = 0,39 | -- | 0,37 / 1,19 m = 0,31 | (Haltung + Vorschlag) |
| Koerper HINTER dem Kopf ueber Kopf-Oberkante, Spielkamera | -- | +36 px = **+0,65 Kopfhoehen** | **+21,4 bis +24,0 cm** (= +0,61 Kopfhoehen) | <= +2 cm |
| Koerperkante 3 cm neben dem Kopf, Spielkamera | -- | ~+16 px (~+0,3 Kopfh.) | +12,2 / +4,5 (Bild 0); Bild-Mass +14,0 / -0,9 (Bild 60) | <= -10 cm |
| Schulterlinie neben dem Kopf, von vorn | nahe Seite auf Kinnhoehe (-0,95 Kopfh.), ferne Seite (Buckel) -0,35 | -- | -15,9 / -26,3 cm (Kopfhoehe 37) | <= -28 cm |
| Koerper hinter dem Kopf, von vorn | -- | -- | -4,6 / -5,6 cm | <= -8 cm |
| Oberkoerper (Brust gegen Waagerechte) | ~80-90 Grad | -- | **14 Grad** (Becken 47,5, Lende 37,5) | 40 Grad (5.1) |
| Hinterfuss-Mitten Abstand | 285 px = 1,19 Kopfbreiten | 190 px = 2,5 Kopfbreiten | **118,1 cm** = 2,7 Kopfbreiten (Sprunggelenke 113,3) | 62-72 cm (1,4-1,6) |
| Vorderpfoten-Mitten Abstand | 55 px, beruehren sich | 52 px | 33,0 cm | 22-26 cm |
| Hinterfuss sichtbar Laenge/Breite (Sitzen) | ~1,2-1,35 | 57/23 px = **2,5** | Spielkamera 2,12-2,14, vorn 2,40-2,44 | 1,1-1,4 / 1,2-1,5 |
| Hinterfuss in Ruhe | -- | -- | 43,4 cm Haut (x -0,629..-0,1955), mit Krallen 46,2; breit 18,7 | 29 x 19-21 cm |
| Sohle Farbe | Median RGB 58/32/22 (Mittel 61/37/27 bzw. 81/51/38) | Bild 89/81/71 | Texel 128/118/104 (Median 131/122/107) | Median 62/42/30 +-12 |
| Rumpf gesamt breit (Ruhe) | -- | -- | **0,930 m** = 0,80 x Schulterhoehe | <= 0,82 (Ideal 0,78) |
| Bild-Naht Ring 0-4 cm / Kopf innen: Helligkeit, Feinkontrast | -- | Kopf heller, glatter | **0,83 / 1,32** (Naht selbst 1,02 / 1,09) | >= 0,92 / <= 1,20 |

Texel um den Kopf (`spez/log/mess_texel_naht_heute.txt`, UV-gerastert): Kopf L 111,3, Koerper 0-4 cm 112,4, 4-8 cm 106,7, 8-12 cm
101,6, 12-20 cm 99,9, **20-35 cm 84,2, 35-60 cm 73,7**. Lesart: die Textur laeuft am Hals schon aus; im Sitzen liegen aber Schulter und
Buckel (20-60 cm vom Kopf) im Bild direkt neben dem Kopf -- die sind 24-34 % dunkler. Deshalb Haltung + Rumpf zuerst, Texel danach.

Bilder (alle nur unter `_arbeit/baer_2c`, Blaetter mit Vorlage/Spielbild nie weitergeben), alle angesehen:
`spez/blaetter/b1_sitzen_spielkamera.png` (Spielbild | heute Textur/Ton/Zonen; Vorlage | heute az -30 Ton/Textur | vorn),
`b2_kandidaten.png` (heute, K1, K2, K3), `b3_hinterfuss.png` (Vorlagen-Fuesse | Spielbild | heute nah Ton/Textur),
`b4_stehen_seite_spiel.png` (Stehen az +-90 el 30, die "Hose im Stiefel" alt), `b5_sitzen_soll.png` (Spielbild | heute | K2 | K2 + Kopf
x1,12; Vorlage | heute | K2 | K2 + Kopf). Einzelbilder `spez/render/`.

Was ich sehe: im Spielbild-Nachbau ist der Kopf ein Gesicht in einer Kapuze aus Rumpf (Zonenbild: grau = Rumpf rundum, gelb =
Halsfell links/unter dem Kopf), die Hinterfuesse stehen als lange helle Platten senkrecht an den Seiten, die Vorderbeine sind zwei
Saeulen in der Mitte. K2 (gleiches Netz, neue Haltung) setzt den Kopf sichtbar oben auf den Koerper (von vorn und az -30), die Beine
ruecken zusammen; der Rumpf bleibt ein breiter Kasten und die alten Fuesse bleiben lange graue Platten -- das loesen C4 und C1.

-------------------------------------------------------------------------------------------------------------------------------

## 2. A BEINE und RUMPF (Ziel A, C4, C5)

Gilt fuer die Ruhe des fertigen GLB (Huelle inkl.), Toleranz +-1,5 cm, wo nicht anders genannt. Messart wie
`werkzeug/beine/beine_mass.py` (waagerechte Schnitte, freie Schleife bzw. Fenster). Die Pfoten unter z 0,115 bleiben vorn wie
baer-pfoten (hoechstens Nahtrand); hinten gilt C1 (Abschnitt 4).

### 2.1 Vorderbein (Handgelenk 0,32/0,23/0,10, Ellbogen 0,23/0,24/0,41, Schulter 0,29/0,225/0,72 -- fest)
| z | 0,12 | 0,15 | 0,20 | 0,25 | 0,30 | 0,35 | 0,40 | heute z 0,25 / 0,30 / 0,35 |
|---|---|---|---|---|---|---|---|---|
| Breite Seite (cm) | 18,8 (fest) | 19,5 | 21,5 | 24,4 | 27,0 | 29,3 | 31,5 | 27,0 / 35,7 / 39,1 |
| Breite vorn (cm) | 18,4 | 19,0 | 21,0 | 23,2 | 25,8 | 29,0 | 33,0 | 27,9 / 36,8 / 40,6 |
| Vorderkante x | 0,412 | 0,406 | 0,405 | 0,404 | 0,405 | 0,408 | 0,415 | 0,441 / 0,485 / 0,501 (Wulst) |
| Hinterkante x | 0,224 | 0,211 | 0,190 | 0,160 | 0,135 | 0,115 | 0,100 | 0,171 / 0,128 / 0,110 |
| aussen y | 0,312 | 0,318 | 0,330 | 0,344 | 0,358 | 0,372 | 0,386 | 0,370 / 0,420 / 0,440 |
| innen y | 0,128 | 0,128 | 0,120 | 0,112 | 0,100 | 0,082 | 0,055 | 0,091 / 0,052 / 0,034 |

Darueber aussen y hoechstens 0,392 / 0,398 / 0,400 / 0,400 bei z 0,45 / 0,50 / 0,55-0,60 / 0,70 (C4). Der Wulst vor dem Unterarm
faellt weg, Verjuengung gleichmaessig Ellbogen -> Handgelenk (oben : Handgelenk 1,6-1,7; echt 1,5-2,0). **Schulter/Oberarm:** sichtbare
Muskelmasse ueber dem Ellbogen, schraeg nach hinten-oben zum Buckel; der Buckel selbst bleibt (Ruecken z 1,159 +-1,5 cm bei x 0,20).
Brust zwischen den Vorderbeinen von z 0,302 auf 0,34-0,36 heben (echt etwa Ellbogenhoehe).

### 2.2 Hinterbein (Huefte -0,46/0,25/0,69, Knie -0,35/0,262/0,41, Sprunggelenk -0,48/0,247/0,10 -- fest)
| z | 0,04 | 0,08 | 0,12 | 0,16 | 0,20 | 0,25 | 0,30 | 0,35 | 0,40 | 0,50 | 0,60 | 0,70 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Hinterkante x (Soll) | -0,555 Ferse | -0,555 | -0,560 | -0,580 | -0,600 | -0,605 | -0,607 | -0,610 | -0,615 | -0,660 | -0,710 | -0,750 |
| heute | ~-0,627 | ~-0,634 | ~-0,632 | ~-0,629 | -0,609 | -0,608 | -0,607 | -0,604 | -0,601 | -0,667 | -0,738 | -0,750 |

| z | 0,20 | 0,25 | 0,30 | 0,35 | 0,40 |
|---|---|---|---|---|---|
| Vorderkante x | -0,390 | -0,364 | -0,340 | -0,317 | -0,288, darueber Kniefalte |
| Breite Seite (cm) | 21,0 | 24,1 | 26,7 | 29,3 | 32,7 (heute 21,7 / 29,4 / 39,0 / 42,7 / --) |
| aussen y | 0,348 | 0,361 | 0,375 | 0,388 | 0,398; darueber <= 0,400 / 0,405 / 0,405 bei z 0,50 / 0,60 / 0,70 |
| innen y | 0,146 | 0,135 | 0,120 | 0,100 | 0,070 |

- Hinterkante bis z 0,40 hart (+-1,0 cm); **z 0,50-0,70 Ziel**: der Schenkel geht stetig nach hinten in den Hintern ueber (>= 2,5 cm
  je 10 cm von z 0,40 bis 0,60, kein senkrechtes Stueck > 10 cm, heute senkrecht z 0,20-0,45 und dann Stufe -0,614 -> -0,667). Weil
  die Sitz-Clips neu gebaut werden, begrenzen nur noch die 12 uebrigen Clips: **Bau Koerper misst zuerst den Bodenspielraum der
  Schenkel-Hinterkante ohne SitDown/Sit/StandUp** (Kopie von `werkzeug/beine/attrappe.py`, Abschnitt Spielraum) und kappt dort
  minus 0,5 cm; reicht der Raum nicht, so weit wie moeglich, ohne Stufe, und melden.
- Kniefalte: hohles Hautsegel Knie -> Bauch statt Fleisch 14-17 cm vor dem Kniegelenk.

### 2.3 Keine Glocke (C5, Kevins wichtigster Bein-Punkt)
Je Bein, Ruhe UND Idle Bild 0, Walk Bild 2 und 20 (Schnitte senkrecht zum Knochen wie `beine_mass.py`), Breite von der Seite und
von vorn in 5-cm-Schritten im Band z 0,12-0,40 (freie Schleife); darueber bis z 0,60 die Aussenkante (monoton, ohne Stufe):
- Zunahme je 5 cm: **vorn <= 3,0 cm, hinten <= 3,5 cm** (heute +7,2 bis +9,6), nie < -0,5 cm (keine Taille ueber dem Gelenk),
- **kein Schritt groesser als 1,6 x der Mittelwert der Schritte** im Band (Gleichmaessigkeit),
- im Spielwinkel seitlich (az +-90, el 30) ist der Uebergang Pfote -> Unterarm/Unterschenkel -> Ellbogen/Knie -> Schulter/Schenkel ->
  Rumpf eine Linie ohne Kante (Bild-Pruefung 8.3, Zelle "Hose im Stiefel" = Nein).

### 2.4 Rumpfbreite (C4) und Nacken/Kragen (C3)
Halbe Breite je x-Scheibe (Ruhe, an der breitesten Hoehe; heute aus `forschung/beine/log/beine_mass.txt` 507-524):
| x | -0,60 | -0,50 | -0,40 | -0,30 | -0,20 | -0,10 | 0,00 | 0,10 | 0,20 | 0,30 | 0,40 | 0,50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| heute | 0,418 | 0,458 | 0,454 | 0,434 | 0,352 | 0,337 | 0,352 | 0,409 | 0,454 | 0,467 | 0,441 | 0,324 |
| Soll | 0,34-0,38 | 0,37-0,405 | 0,37-0,405 | 0,36-0,395 | 0,33-0,36 | 0,32-0,345 | 0,33-0,355 | 0,35-0,38 | 0,365-0,395 | 0,365-0,40 | 0,345-0,38 | 0,255-0,29 |

- Gesamtbreite **<= 0,82 m, Ideal 0,78** (heute 0,93). Grenze nach innen: Schultergelenk |y| 0,225 und Huefte 0,25 sind fest, die
  Bein-Aussenkanten aus 2.1/2.2 sind das Minimum. Die Aussenwand laeuft schraeg statt senkrecht ("Kasten" weg).
- Ei-Form, helle Unterseite, Straehnen, Gesaessfalte, Falten bleiben (Grenzwerte 8.2).
- **Nacken (kein Kragen):** Ruecken z bei x 0,40 / 0,50 / 0,60 von 1,087 / 1,016 / 0,938 auf **1,05-1,07 / 0,96-0,99 / 0,90-0,92**;
  Buckel bei x 0,10-0,30 bleibt (1,139 / 1,159 / 1,142 +-1,5 cm). Hals direkt hinter dem Kopf: halbe Breite bei x 0,50 0,255-0,29
  (heute 0,324 = 1,5 Kopfbreiten). Die Kopfpunkte (Maske 3.5) bleiben bit-gleich; geaendert wird nur, was dahinter liegt.
- Gemessen wird der Kragen in der Sitzpose (Abschnitt 6) -- die Ruhezahlen hier sind Richtwerte fuer das Netz.

### 2.5 Fellbehang (Weg A + B der Forschung, Abschnitt 3)
- **Umriss-Kanten als Teil der Huelle** (vor dem Verringern geformt, nicht als Zotteln): Ellbogenbehang hinter dem Unterarm 4-6 cm tief
  bei z 0,30-0,45, laeuft bis z 0,15 auf 0 aus (Bodenspielraum mind. 5,4 cm); Bauchkante 3-4 cm (Spielraum 15,2 cm); an der
  Schenkel-Hinterkante hoechstens 1-2 cm. Kosten +200 bis +300 Dreiecke (Kantenschleifen), aus dem glatten Ruecken holen.
- **Textur:** haengende Straehnen-Buendel 3-6 Texel quer ueber die Behang-Kanten, darunter ein dunkles Schattenband; Beine unten
  dunkler als der Rumpf.
- Keine Netz-Zotteln (baer-fell: Noppen, `_arbeit/baer_fell/bau_netz.md:121-126`), keine Alpha-Karten, keine Lappen-Probe in diesem Lauf.

### 2.6 Bau-Orte (Kopien, Originale nicht aendern)
- `baer_quelle_2c.py`: Bein-Ketten `:1130`/`:1138` an die Knochen (Schulter -> Ellbogen -> Handgelenk, Huefte -> Knie -> Hock statt
  gerader Saeule), Hinterfuss-Feld neu (C1), Rumpf-Metaballs der Schultern/Huefte schmaler, Buckel `:1123` bleibt, Nacken flacher.
- `baer_export_2c.py`: `huelle_bauen` `:723` (Felldicke gleitend ueber z 0,15-0,45 statt Wechsel in `PF_UEB` `:69`), `form_fell`
  `:844` (Masken Schulter/Flanke an die schmalere Form, neue Behang-Kanten), `fix1_form` `:1473` ersetzen (die Regel "ueber z 0,36
  wie baer-fell" faellt fuer Beine, Rumpfseiten und Nacken), `PF_HINTEN_HEUTE` `:72` an 2.2, `SPERR_FLECKEN` `:141` = Flecken aus 3.4,
  Ziele `PF_ZIEL`/`PF_RUMPF_REST`/`RUMPF_ZIEL` `:77-78`, `:139` nach Abschnitt 7.1.
- `baer_kampf_2c.py` `gewichte_eigen` `:1722`: Oberarm/Oberschenkel bekommen mehr Haut (heute dominant nur 13/16 bzw. 97/100
  Dreiecke; Einblendung `:1733-1734` z 0,32-0,50 -> etwa 0,22-0,45); `baer_gewichte_2c.py` optimiert danach wie heute.

-------------------------------------------------------------------------------------------------------------------------------

## 3. B GEBISS und ZUNGE (Ziel B)

Kopfrahmen a/b/c wie `baer_kampf_pfote.py:107-141` (a vorn, b seitlich, c oben; fuer a > 0,32 ist 1 a-Einheit = 68,44 cm, sonst
87,75 cm; Lippenlinie `k_lippe` :164). Alle Teile **starr, Gewicht 1,0**: oben an `Bip01_Head`, unten an `Bip01_Jaw`. Keine
Knochen- oder Clip-Aenderung; die Kieferspuren der Clips (Rear 38 Grad, Bite 34, Maul 33,7, Slam 26, Swipe 22, Eat 24, Sit 5) wirken.

### 3.1 Zaehne einzeln (Soll; Masse = sichtbare Krone, Massstab Natur x 1,15)
| Teil | Anzahl | Knochen | Lage | Krone (cm) | Basis (cm) | Form |
|---|---|---|---|---|---|---|
| Eckzahn oben | 2 | Head | a 0,440-0,450, \|b\| 4,4-5,0, Basis 0,6 cm ueber der Lippenlinie | **4,6** (4,2-5,0) | Oval 2,3 x 1,7 | 35 Grad Bogen nach hinten, 10 Grad nach vorn, **10 Grad nach innen**; 6-seitig, 4 Ringe + Spitze, 42 Dreiecke |
| Eckzahn unten | 2 | Jaw | a 0,462, \|b\| 3,4-4,0, Basis 0,6 cm unter der Lippenlinie; 0,8-1,5 cm VOR und ~1 cm innen vom oberen | **4,0** (3,6-4,8) | Oval 2,1 x 1,6 | 45 Grad Bogen nach hinten, 15 Grad vorn, 8 Grad aussen |
| Schneidezaehne oben | 6 | Head | Bogen zwischen den Eckzaehnen, Vorderkante >= 1,3 cm hinter der Vorderlippe | 1,1-1,6 hoch, 0,9-1,3 breit, I3 am groessten | -- | Zinnen-Leiste, 6 Dreiecke je Zahn |
| Schneidezaehne unten | 6 | Jaw | Bogen, >= 0,5 cm hinter der Unterlippe | 0,9-1,1 hoch, 0,8-1,0 breit | -- | dito |
| Backenzaehne | je Kiefer und Seite 1 Leiste | Head / Jaw | nach 2,5-3,0 cm Luecke hinter dem Eckzahn, >= 1,0 cm von der Lippenlinie | 1,0-1,2 hoch, Leiste 6-8 cm lang (gekuerzt "angedeutet": das Maul ist nur 13,0 cm lang) | -- | Hoecker-Leiste 24 Dreiecke |

Heute zum Vergleich: vier gerade Kegel 3,0 / 2,8 cm, untere HINTER den oberen, alle Zahn-Dreiecke auf einem Texel.

### 3.2 Luft und Durchstich (hart)
- **Maul zu** (jeder Clip, jedes Bild mit Kiefer < 6 Grad: Idle, Walk, Run, Death, Dead, SitDown, StandUp, Sit, Halten von Bite/Maul):
  0 Zahnpunkte ausserhalb der Aussenhaut, Luft >= 2 mm (Windungszahl `abs(w) > 0,5`, `tier()` spiegelt).
- **Kleine Winkel 3-14 Grad** (Bite/Maul 3, Sit 5, Eat 4-14): kein Eckzahn durch Gaumen, Maulboden oder Zunge -> Taschen/Rinnen
  seitlich der Zunge fuer die oberen Eckzaehne; Probe je Clip und Bild (Kopie `werkzeug/gebiss/probe_gebiss.py`, erweitert um alle
  Clipbilder und um Gaumen/Boden/Zunge als Gegenflaechen).
- Zaehne einer Reihe stechen nicht ineinander; obere und untere Zaehne beim Schliessen hoechstens 2 mm Ueberlappung im Bild 0-3 Grad.

### 3.3 Zunge, Gaumen, Zahnfleisch, Lefzen, Wange
- **Zunge** (Jaw): eigener Koerper, hinten 7-8 cm breit, Spitze 5-6 cm, 1,2-1,5 cm dick, Raender 0,3-0,5 cm hochgewoelbt (flache
  Mulde), Spitze rund, 1,5-2,0 cm hinter den unteren Schneidezaehnen; liegt tief im Unterkiefer (Oberseite >= 0,5 cm unter den
  unteren Zahnspitzen); kein Klumpen, keine Rolle, kein Dach-Knick. Farbe rosa-mauve RGB 175-205 / 98-125 / 110-135, Mittelrinne
  leicht dunkler.
- **Gaumen** (Head): gewoelbt 1,5-2 cm, 7-8 Querrillen nur gemalt, RGB 135-165 / 80-100 / 92-112; **Rachen** dunkel (40/20/22).
- **Zahnfleisch**: Wall 1,0-1,5 cm um die Zahnreihen oben und unten, dunkel bis rosa (110/62/68 -> 140/85/90).
- **Lefzen**: innerer Lippenstreifen 1,2-1,5 cm breit direkt hinter der Lippenkante, schwarz (28/24/24) -> rosa; beim Oeffnen wirkt er
  wie die zurueckgezogene schwarze Lefze, geschlossen unsichtbar. Echtes Hochziehen der Oberlippe = Clip-Runde (8.4).
- **Wangenhaut** (Weg b der Forschung 4.5): innere Haut an beiden Mundwinkeln, verdeckt Kasten-Ecke und "Zipfel" (gespannte Wange,
  Dehnung x3,9). Gehoert in M1. Weg a (Kiefergewichte der unteren Lippenzwillinge) nur, wenn b den Zipfel im Ton-Bild Rear Bild 48
  nicht verdeckt -- dann nur die 64 unteren Zwillinge (M2), Liste der geaenderten Gewichte, Dehnung neu.

### 3.4 Dreiecke und Texel
- Maul-Inneres **874 Dreiecke (Soll), >= 700 (Untergrenze)**, heute 330: Eckzaehne 168, Schneidezaehne 72, Backenzaehne 96, Gaumen +
  oberer Wall 150, Boden + unterer Wall 110, Zunge 110, innerer Lippenstreifen 120, Wangenhaut 32, Rachen 16.
- Flecken in der 1024er Body-Textur (Pixel x, y von oben, Breite, Hoehe; im freien Rechteck 196 x 108 bei (269,0) und 210 x 29 bei
  (465,0), `forschung/gebiss/mess/texturplatz.png`): **Gaumen (271, 2, 94, 104), Zunge (369, 2, 94, 104), Zahn/Zahnfleisch/Lippe als
  Streifen (467, 2, 206, 25)** (Zahn-Verlauf Zahnfleisch dunkel -> Hals 190/170/120 -> Spitze 235/228/210; Lippen-Verlauf schwarz ->
  rosa). Vor dem Bau gegen die Karte pruefen (3 px Saum zu jeder Insel), sonst verkleinern -- keine Insel wandert.
  `SPERR_FLECKEN` (Kopie von `baer_export_pfote.py:141`) und die Pruefung (Kopie `baer_textur_pfote.py:1495-1499`) nennen dieselben
  drei Rechtecke. Flecken gibt es nur in der 1024er Body-Textur (wie heute).

### 3.5 Maske "Kopf-Aussenform bleibt" (wie geprueft)
| Zone | Inhalt | darf sich aendern | Pruefung |
|---|---|---|---|
| M1 Innen | alles, was `maul_bauen` erzeugt (Punkte mit UV in den drei Flecken) | alles (Punkte, Dreiecke, UV, Gewichte, Flecken-Texel) | nur Grenzen 3.2, <= 4 Einfluesse, nur Head/Jaw, Dreiecke 3.4 |
| M2 Lippenkante | die 31 Lagen der Schnittlinie (64 obere + 64 untere Dump-Punkte) | Lage und UV **bit-gleich**; neue Nachbarn nach innen; Kiefergewicht der 64 UNTEREN Zwillinge nur nach 3.3 Weg a | Lage/UV bit-gleich, Gewichtsliste |
| M3 Lippenband aussen | Aussenhaut vor a = 0,245 mit \|c - k_lippe\| < 7 mm (112 Punkte / 180 Dreiecke) | **in diesem Lauf nichts**; schwarzer Saum aussen nur als Vorschlag-Datei | Texel-Vergleich |
| Kopf Rest | alle 1.333 Kopfpunkte von `kopf.py` ausser M2 | nichts | `kopf.py` (Lage, UV, Gewichte bit-gleich), `textur_pruef_pfote.py` (Kopf-Texel Body 1024 und WorldItems 2048 bit-gleich ausser den Flecken + 4 px) |

### 3.6 Bau-Ort
Neue Datei **`baer/spiel/baer_maul_2c.py`** (Kopie von `maul_bauen` `baer_kampf_pfote.py:1898-2134`, `fleck_malen` :2455 und den
Farben :2443-2487), von `baer_kampf_2c.py` aufgerufen (Schnittstelle: `maul_bauen(V, T, UVc, W, namen)` und `flecken_malen(bild)` wie
heute). So arbeitet der Gebiss-Bauer nie in derselben Datei wie der Sitz-Bauer. Netz und Gewichte des Rumpfs muessen dafuer nicht neu
laufen; `glb` + `deer` + Pruefer schon. Das Hochmodell-Gebiss (`baer_quelle_pfote.py:1675-1716`) ist nur fuer Schau-Renders; Masse aus 3.1.

-------------------------------------------------------------------------------------------------------------------------------

## 4. C HINTERFUSS (C1, Massstab ist Kevins Vorlage; die Literatur-Ziele aus baer-pfoten gelten nicht mehr)

Ruhe, linker Fuss, Sprunggelenk (-0,48/0,247/0,10) und Ballen-Knochen (-0,25/0,24/0,045) fest. Bild: `spez/blaetter/b3_hinterfuss.png`.

| Mass | heute | Soll |
|---|---|---|
| Laenge Haut Ferse -> Zehenstirn (ohne Krallen) | 43,4 cm (-0,629..-0,1955) | **29 +-1 cm: Ferse x -0,555, Zehenstirn x -0,265** |
| Ferse | 15 cm hinter dem Gelenk, schmal (11-12), Kante | 7,5 cm hinter dem Gelenk, **rund und breit**: Breite bei x -0,50 15-17 cm mit Fell (Haut 13-15), Rundungsradius von der Seite >= 4 cm |
| Breite | Platte 16,5-17,5, mit Fell 20-21 an den Zehen | Zehenreihe mit Fell 19-21, Platte bei x -0,33 17-18 |
| Sichtbares L/B | Ruhe straight 2,0 (Platte+Zehen 34,6/17) | Sohle von unten (Fell inkl.) 1,35-1,55; im Sitzen Spielkamera **1,1-1,4**, von vorn 1,2-1,5 |
| Krallen | Wurzeln x -0,240/-0,213/-0,203/-0,212/-0,239, Spitzen -0,175 | **alle 10 Hinterkrallen um dx = -0,070 verschoben** (nur Lage; Form, UV, Gewichte bit-gleich, Gewicht 1,0 Foot), y/z wie heute |
| Zehenballen | 5, Halbachsen 1,65 x 1,9 cm, Zeh 1 x 0,85 | 5 **grosse, runde** Ballen 3,4-3,8 cm, dicht im Bogen am vorderen Rand (Luecke <= 0,6 cm), Mitte 3,0 +-0,5 cm hinter der Krallenwurzel, aeussere 2,5-3 cm weiter hinten; Relief 8-12 mm |
| Sohlenballen | lange Platte mit Fersenhochzug | ein grosser Ballen x -0,54..-0,315, vorn 14-16 cm, an der Ferse 11-13 cm breit, Furche 1,0-1,5 cm zu den Zehenballen |
| Fellkranz | 1,5-2 cm (Textur) | 1,5-2,5 cm breit, ueberdeckt den Sohlenrand 0,5-1,0 cm -> Umriss rund/oval, keine geraden Kanten |
| Rist / Hoehe | Zehen 5,0-5,5 cm | Zehenoberkanten 4,5-5,5 cm, Rist faellt vom Schienbein-Vorderrand (x -0,40, z ~0,15) zu den Zehen (x -0,29, z ~0,06), Zehenhoecker sichtbar |
| Fuss : Bein | 2,0 gefordert | Fusslaenge / Bein-Tiefe z 0,20 = 1,3-1,6 |
| Sohlen-Texel | 128/118/104 (grau-beige) | **Median 62/42/30 +-12 je Kanal**, keine Grautoene (R - B >= 20), Ballenmitte +10..+15 L heller (ledrig, leichter Glanz), Furchen L <= 45 |
| Krallen-Texel | elfenbein | dunkler erlaubt und empfohlen (hinten "kurze dunkle Krallen"): Wurzel <= 70/55/45, Spitze <= 150/135/115; vorn hoechstens dunkler, sonst wie heute |

- **Boden:** Probe `spez/log/krallen_probe.txt` (Krallen + Zehenhaut starr um -0,07 verschoben): kein Clip tiefer, Walk -2,23 ->
  +0,66 cm, Run -2,58 -> +0,70, Death -1,01 -> +0,39 (Kralle). Die neue Ferse liegt vor der Grenzkurve von `SPEZ_PFOTEN.md` 1.4.
  Trotzdem je Clip messen (8.2).
- Im neuen Sitzen liegt die Ferse auf (Sprunggelenk ~0,08 statt 0,156 hoch, Abschnitt 5).
- Die Vorderpranken bleiben wie baer-pfoten (Krallen hoechstens dunkler).
- Bau: Hinterfuss-Feld in `baer_quelle_2c.py` und Plan `spez/soll_2c.json` -> `C_hinterfuss` (ersetzt fuer hinten `pfoten_plan.json`);
  `sohlen_bauen`/`ballen_plan` in `baer_export_2c.py` (`:1065`, `:984`); Krallen-Verschiebung dort, wo heute K1 vorn liegt
  (`stufe_kopfprobe` `:2673`: hinten "Form/UV/Gewichte bit-gleich, Lage = alt + (-0,070, 0, 0) +-0,1 mm").

-------------------------------------------------------------------------------------------------------------------------------

## 5. D SITZEN (C2, Richtung (b) aus ENTSCHEIDUNGEN.md:70/96)

### 5.1 Machbarkeit (gemessen, `spez/log/sitz_fk.txt`, `sitz_fk_suche.txt`, `sitz_kand.txt`)
- Vorderbein Schulter -> Handgelenk hoechstens 63,7 cm (Ellbogen innen <= 173); flache Pranke = Handgelenk z 0,10 -> **Schulter
  hoechstens ~0,737 m**. Mit dem festen Rumpf liegt sie bei senkrechter Brust (Vorlage) bei 0,955-1,106 -> Pfote 22-37 cm in der Luft
  (K3, `spez/render/K3_*`): geht nicht, sieht auch falsch aus (Kopf schaut nach oben, Koerper ein Turm).
- Suche 2 x 720 Posen (Becken -35..-85, Lende/Brust gegen Eltern in den Grenzen, Schulterblatt -25..+20, Pfote x 0,36/0,44):
  **aufrechteste Brust mit flachen Pfoten -40 Grad**; dafuer Lende gegen Becken +10 (nach vorn gebeugt), Brust gegen Lende -15
  (Grenze), Schulterblatt +20 (Grenze) -- die Schulter sinkt so auf 0,72-0,73.
- **K1** (alle Grenzen wie heute, Kopf gegen Hals +34): Kopf oben 1,190, Kragen Spielkamera hinter +14,5 / Seiten +4,1 / -3,7 cm,
  von vorn Seiten -20,8 / -23,8. **K2** (Hals steil, Kopf geradeaus, Kopf gegen Hals +54): Kopf oben 1,282, Spielkamera hinter
  **+4,1**, Seiten **-7,5 / -14,1**, von vorn Seiten **-31,3 / -33,1**, hinter -11,0. Beide mit dem heutigen Netz (breit, langer Fuss).
- K1/K2 sind mit Sprunggelenk z 0,155 gerechnet (der heutige lange Fuss liegt sonst im Boden): Huefte 0,286, Schulter 0,676, Ellbogen
  133 (gebeugt). In der Suche mit tiefem Sprunggelenk (z 0,075, wie fuer den kurzen Fuss C1) liegen die Schenkel tiefer am Boden:
  Huefte 0,342, Schulter 0,732, Arm 0,998 (gerade). Die Sitzflaeche haengt also an der Schenkellage -- der Bau Sitzen loest die Pose
  am fertigen Netz aus (1) neu und misst die Haut (nicht schaetzen).

### 5.2 Soll-Pose S_neu (Ende SitDown, Anfang/Ende Sit, Anfang StandUp; Weltdrehungen wie `euler()`, nick + = Nase runter)
| Teil | Soll (Toleranz +-5 Grad) | heute (POSE_S, `baer_kampf_pfote.py:1262`) |
|---|---|---|
| Becken `r_pel` | (0, **-35**, 0); Ursprung x -0,32..-0,26, z 0,33-0,42 (Huefte 0,27-0,35); tiefster Haut-Punkt Sitzflaeche 0,0 cm | (0, -42, 0), z 0,384 (Huefte 0,301) |
| Lende `r_sp` | (0, **-25**, 0) = +10 gegen Becken | (0, -28, 0) |
| Brust `r_ch` | (0, **-40**, 0) = -15 gegen Lende (Grenze) | (0, -14, 0) |
| Schulterblatt `klav` | nick **+15..+20** | -8 |
| Hals `r_ne` | (5, **-77**, 2) = -35..-40 gegen Brust | (3,5, -58, 2) |
| Kopf `r_he` | (15, **-24**, 5), nick -25..-15 (Kopfknochen 0..+10 Grad ueber der Waagerechten = geradeaus, Ruhe -14,7), Kopf gegen Hals +50..+60 (Sitz-Ausnahme 5.4); Schleife gier 10 -> 28 -> 10 wie heute | (10, -24, 5) an Hals -58: Kopf gegen Hals +34 |
| Schulter (UpperArm) z | **0,69-0,74** | 0,720 |
| Vorderpfoten | flach (Ballen z 0,045, tiefste Haut -0,05..+0,3 cm), Ballen x **0,34-0,40**, \|y\| **0,11-0,13** (Pfoten fast beruehrend, >= 1 cm Luecke), gier 0..+6; Ellbogen innen **150-172** (Vorderbeine "gerade nach unten"), Abstand/Armlaenge <= 0,998 | x 0,40, \|y\| 0,18, Ellbogen 159-163 |
| Hinterbeine | Huefte fest am Becken; Knie innen 115-145, Knie vorn-aussen (Pol), \|y\| Knie 0,32-0,40; **Sprunggelenk x 0,16-0,24, \|y\| 0,33-0,36, z so, dass die neue Ferse aufliegt (tiefste Fersenhaut 0,0-0,5 cm; mit Fuss nach C1 etwa z 0,07-0,09)** | Sprunggelenk (0,147, 0,566, 0,156) |
| Hinterfuss welt | gier **+15..+25** (Zehen nach aussen), nick **-95..-110** (Sohle nach vorn, leicht nach oben), roll 0..+10; Sohlen-Normale 10-25 Grad ueber der Waagerechten und 15-30 Grad nach aussen | (34, -95, 0) |
| Fussabstand | Mitten der Hinterfuss-Haut **62-72 cm** (Sprunggelenke 66-72); Hinterfuss-Innenkante >= 2 cm neben der Vorderpfoten-Aussenkante | 118,1 / 113,3 cm |
| Kopf-Oberkante z | 1,20-1,32 | 1,191-1,201 |
| Kiefer, Schwanz | zu (Schleife 5 Grad bei 2,6-3,3 s wie heute); Schwanz `r_ta` = Becken, am Boden, nicht im Boden | |

Kopf-Masse in dieser Pose: Abschnitt 6. Ist K2 nicht erlaubt (5.4), gilt K1 (`spez/log/sitz_kand.json`) mit den Ersatz-Grenzwerten 6.1.

### 5.3 Clips (Vertrag mit `NCBearFight.lua:54-56` und den Knoten `AnimSets/buck/idle/NCBear_*.xml` -- nichts davon aendert sich)
| Clip | Dauer / Proben (30/s) | Schleife / Ereignis (XML) | Anfang -> Ende |
|---|---|---|---|
| NCBear_SitDown | 1,60 s / 49 | nein; SetVariable NCBearDone=true am Ende | `grund()` (= Idle) -> S_neu exakt |
| NCBear_Sit | 4,00 s / 121 | ja; erstes = letztes Bild bit-gleich | S_neu -> S_neu |
| NCBear_StandUp | 1,30 s / 40 | nein; Ereignis am Ende | S_neu -> `grund()` exakt |

- Gleiche Namen, gleiche Knochen/Eltern/Offsets/Bind, keine Wurzelbewegung (Bip01, Translation_Data wie heute), gleiche Abtastzeiten.
- **SitDown** (Lehren des Fixers baer-anim behalten: erst Hinterbeine, dann Vorderpfoten; Fuss bis zur Schrittmitte flach,
  `_fuss_flach_bis`): 0-0,30 Gewicht nach hinten, Hinterknie beugen; 0,25-0,64 Hinterpfoten je ein halber Schritt (links 0,25-0,47,
  rechts 0,42-0,64); 0,68-0,94 Hinterbeine nach vorn in die ENGE Lage, Ferse auf, Sohle nach vorn; Hinterteil am Boden ~1,00;
  0,95-1,40 Oberkoerper richtet sich auf (Brust -14 -> -40, Hals -> -77, Kopf geradeaus); 1,02-1,30 Vorderpfoten je ein Schritt
  ZURUECK zwischen die Hinterbeine (links 1,02-1,18, rechts 1,14-1,30); 1,40-1,60 Setzen, Kopf dreht zur Seite.
- **Sit**: Atmen (Brust nick +-1,5..2, zwei Zuege), Kopf schaut um (gier 10 -> 28 -> 10, Hals mit 35 %), Kiefer 5 Grad bei 2,9 s;
  Pfoten gleiten 0 (alle vier Ballen <= 1 mm Weg).
- **StandUp** (Spiegel): 0-0,25 Vorderpfoten auf den Ruheplatz (links 0-0,15, rechts 0,10-0,25), Oberkoerper nach vorn; 0,14-0,52
  Hinterbeine halb unter den Koerper; Hinterteil hebt; 0,55-0,92 Hinterpfoten ganz zurueck; ab 0,92 in die Grundhaltung.
- `NCBear_SitB` gibt es im GLB nicht (nur Vorschau-Variable `NCB_VORSCHAU_SITZ_B`, `baer_kampf_pfote.py:1443-1463`) -- bleibt aus.
- Alle anderen 12 Clips **bit-gleich** gegen das heutige GLB (Dump-Textbloecke + Animations-Puffer). Ist einer nachweislich nur per Clip
  zu retten, nicht aendern, sondern in 8.4 melden.

### 5.4 Gelenkgrenzen
- Alle Grenzen aus `baer_kampf_pfote.py:566-582` (GRENZEN, GRENZEN_RUMPF, GRENZE_KLAV, SPRUNG, SOHLE_*) gelten fuer jede Taste.
- **Einzige Ausnahme, nur SitDown/Sit/StandUp:** `he_ne` nick bis **+60** (statt +-35). Grund: senkrechter Hals bei geradeaus
  blickendem Kopf braucht Beugung im Kopfgelenk in seiner eigenen Richtung (wie beim sitzenden Hund); die Grenze +-35 ist ein
  Arbeitswert aus Hunde-Goniometrie (`anim_referenz.md` 2), kein Baer-Mass. Gegenmittel fuer die Haut: Dehnung Hals/Nacken je Bild
  berichten (8.2). Wird die Ausnahme abgelehnt: K1.
- Sprung je Bild: Pfotendrehung/Oberarmdrehung <= 20 Grad, Pfotenbeugung <= 35 Grad, Beckenweg <= 3 cm je Bild, kein Bild-Sprung an
  der Schleifennaht Sit.

### 5.5 Harte Regeln Sitzen
Kein Bild tiefer im Boden als heute (Sit/SitDown -0,05 cm, StandUp -0,06; ganzes Netz und je Pfote Haut/Kralle); keine Durchdringung:
0 Punkte von Hinterfuss/Unterschenkel im Unterarm und umgekehrt, Vorderpfoten nicht ineinander (Mess-Art wie die Fixer-Messung
baer-anim "59 Fusspunkte im Unterarm"; Probe-Vorlage `_arbeit/baer_anim/anim/pose_probe.py`, oder schneller `spez/werkzeug/sitz_fk.py`
fuer Posen ohne Blender); Dehnung je Clip wie 8.2.

-------------------------------------------------------------------------------------------------------------------------------

## 6. E KOPF-PASSUNG (C3)

### 6.1 Messgroessen und Soll (Sitzen, Bilder 0/30/60/90 von NCBear_Sit, jedes Bild einzeln)
| Mass | Werkzeug | heute | K2 (heutiges Netz) | **Soll** | Ersatz bei K1 |
|---|---|---|---|---|---|
| Spielkamera: hoechste Koerperkante in den Kopfspalten minus Kopf-Oberkante | `mess_naht.py` (Zonenbild) / `mess_sitz.py` | +21,5 cm (Bild 60) / +24,0 (Bild 0) | +4,2 | **<= +2 cm** | <= +8 |
| Spielkamera: Koerperkante 3 cm neben dem Kopf (beide Seiten) | dito | +14,0 / -0,9 (Bild 60); +12,2 / +4,5 (Bild 0) | -7,0 / -14,0 | **<= -10 cm** | <= -4 |
| Spielkamera: Kopfbreite / Silhouette gesamt | `mess_naht.py` | 0,35 | 0,43 | **>= 0,45** | >= 0,42 |
| Von vorn (az 0 el 0): Koerperkante 3 cm neben dem Kopf | `mess_sitz.py` | -15,9 / -26,3 | -31,3 / -33,1 | **<= -28 cm** | <= -22 |
| Von vorn: Koerper hinter dem Kopf | dito | -5,6 | -11,0 | **<= -8 cm** | <= -6 |
| Von vorn: Kopfbreite / Brustband 5-25 cm unter dem Kinn | `mess_brustband.py` | 0,48-0,51 | 0,47 | **>= 0,55** | >= 0,55 |
| Spielbild-Naht: Helligkeit Ring 0-4 cm / Kopf innen | `mess_naht.py` (Licht B, Band 20 px = 3,7 cm; Logs `spez/log/mess_naht_*.txt`) | 0,83 | 0,81 | **>= 0,92** | >= 0,92 |
| Ring 4-12 cm / Kopf innen | `mess_naht.py ... 20 0.001838 65` (Ring 20-65 px) | 0,77 | 0,78 | **>= 0,85** | >= 0,85 |
| Feinkontrast Ring 0-4 cm / Kopf innen | dito | 1,32 | 1,27 | **<= 1,20** | <= 1,20 |

Kragenhoehe = erste Zeile. Ein Kopf, der "oben auf dem Koerper" sitzt, erfuellt Zeilen 1, 2 und 4 zugleich.

### 6.2 Wie (Reihenfolge)
1. Haltung K2 (Abschnitt 5) -- traegt den groessten Teil (hinter +24 -> +4).
2. Schmalere Schultern (2.4, C4) -- senkt die Kanten neben dem Kopf.
3. Nacken flacher, Hals hinter dem Kopf schmaler (2.4) -- nimmt den Rest hinter dem Kopf; Kopfpunkte bleiben.
4. **Koerper-Texel** an Hals, Nacken, Kehle UND an Schulterbuckel/Schultern (die im Sitzen neben dem Kopf liegen): Helligkeit und Farbe
   gleiten zum Kopfmittel (Texel L 111, RGB 139/104/75) -- 0-12 cm um die Kopfnaht L >= 0,95 x Kopf, Schulter/Buckel bis ~35 cm L >=
   0,85 x Kopf (heute 0,76), danach Koerperfarbe; Straehnen dort feiner/schwaecher (Feinkontrast <= 1,1 x Kopf). Die Rueckenstraehnen
   (8.2) und die helle Unterseite bleiben; Mass am Texel: `mess_texel_naht.py` (heute: 1,01 / 0,96 / 0,91 / 0,90 / 0,76 / 0,66 je Band).

### 6.3 Nur als Vorschlag (eigene Dateien unter `_arbeit/baer_2c/vorschlag/`, nie in den 5 Mod-Dateien)
- **Kopf-Texel** (z. B. Kopf 6-10 % dunkler, Straehnen staerker): `vorschlag/NCBear_kopftexel.png` + Vorher/Nachher-Blatt Spielkamera.
- **Kopf gleichmaessig groesser x1,10-1,15** (Form gleich, um den Kopf-Gelenkpunkt, gleitend mit dem Kopfgewicht): `vorschlag/NCBear_kopf112.glb`
  + Blatt. Vorschau mit K2 heute (`spez/render/K2_kopf112_*`, Blatt `b5`): Kopf 44,1 -> 48,1 cm, sichtbar etwas besser, kein Ersatz
  fuer 6.2. Risiko: Kiefergelenk sitzt dann 1-1,5 cm neben der Maulecke (Knochen fest).
- **Schwarzer Lippensaum aussen** (M3, 7 mm): `vorschlag/NCBear_lippensaum.png` + Blatt Bruellen.

-------------------------------------------------------------------------------------------------------------------------------

## 7. F HAUSHALT und REIHENFOLGE

### 7.1 Dreiecke (nach dem Importer; Grenze 20.000)
Die Regionszahlen der Forschung (`forschung_beine.md` 4.4) ueberlappen sich (Summe 20.076 statt 19.426), deshalb als Aenderung gegen
heute; die Verteilung laeuft ueber die Dezimier-Ziele (`PF_ZIEL` `:77`, `PF_RUMPF_REST` `:78`, `RUMPF_ZIEL` `:139`), eine reine
Formaenderung kostet 0. Kopf aussen 2.295 und Krallen 832 bleiben.
| Posten | Dreiecke |
|---|---|
| heute | 19.426 |
| Maul innen 330 -> 874 (Sparfassung 700) | +544 (+370) |
| Behang-Kanten Ellbogen/Bauch/Kniefalte | +200 .. +300 |
| glatter Ruecken/Hinterteil | -250 .. -300 |
| kuerzere Hinterfuesse (Sohle ~30 % kleiner; `PF_ZIEL` 4.300 -> ~3.950) | -250 .. -350 |
| schmalerer Rumpf, Beinform, Nacken | 0 |
| **Summe** | **~19.590 .. 19.720; Ziel <= 19.850, hart <= 20.000.** Bei Ueberlauf zuerst Sparfassung Maul, dann Behang kleiner |

### 7.2 Kette und Zustaendigkeit (Kopien in `baer/spiel/`: `baer_quelle_2c.py`, `baer_export_2c.py`, `baer_kampf_2c.py`,
`baer_gewichte_2c.py`, `baer_textur_2c.py` aus den `*_pfote.py`; neu `baer_maul_2c.py`; Ausgaben nur `_arbeit/baer_2c/`; Werkzeuge
kopieren nach `_arbeit/baer_2c/werkzeug/`; Kette `lauf_2c.sh` als Kopie von `_arbeit/baer_pfote/werkzeug/lauf_pfote.sh`)
| Schritt | Bauer | Dateien (nur diese) | Inhalt | fertig, wenn |
|---|---|---|---|---|
| (1) Bau Koerper | Bauer Koerper | `baer_quelle_2c.py`, `baer_export_2c.py`, `baer_gewichte_2c.py`, in `baer_kampf_2c.py` NUR `gewichte_eigen` | Abschnitte 2 und 4 (Beine, Rumpf, Nacken, Hinterfuss, Krallen-Lage), Form-Runden mit Formel-Gewichten + Ton-Bildern (~5 min), dann netz -> fbx -> kopfprobe -> formel -> gewichte -> glb mit den ALTEN 15 Clips | 8.2 Teil Koerper gruen fuer die 12 Nicht-Sitz-Clips; die alten Sitz-Clips duerfen schweben/stecken (werden ersetzt) |
| (2) Bau Sitzen | Bauer Sitzen | `baer_kampf_2c.py` ausser `gewichte_eigen` | Abschnitt 5 auf dem Netz von (1): `_pose_s`, `sp_setzen`, `sp_sitzen`, `sp_aufstehen`, Sitz-Grenze 5.4; Vorschau-Video | 8.2 Teil Sitzen + Kopf (6.1 Zeilen 1-6) gruen |
| (3) Bau Gebiss | Bauer Gebiss | `baer_maul_2c.py` (neu), Konstanten der Flecken nur wie 3.4 | Abschnitt 3; arbeitet gegen das heutige GLB/Kopfrahmen, kann parallel zu (1)/(2) laufen | 8.2 Teil Gebiss gruen |
| (4) Textur + Mod | Bauer Textur | `baer_textur_2c.py` | Textur-Ansichten (GPU) -> backen -> Body 1024 + Flecken -> GLB -> deer -> WorldItems FBX/PNG; Sohlen/Krallen/Naht-Texel (4, 6.2); genau 5 Dateien unter `_arbeit/baer_2c/mod/42/media/` | 8.1-8.3 komplett |

Ganze Kette ~35-40 min, GPU-Teile ueber `gpu_render.sh` (Sperre `_arbeit/baer_2c/gpu.lock`, nicht auf das Spiel pruefen). Workflow
<= 10 Agenten, z. B. 4 Bauer + Pruefer Technik + Pruefer Optik + Nachbesserung + Gegenpruefer + Integrator = 9.

-------------------------------------------------------------------------------------------------------------------------------

## 8. G ABNAHME

### 8.1 Feste Regeln (hart; Werkzeuge in `_arbeit/baer_pfote/werkzeug/` und `pruef/technik/` kopieren)
- 12 Clips bit-gleich (`regeln.py`, `glb_datei.py`, `glb_pruef.py`); SitDown/Sit/StandUp: Namen, Dauer, Probenzahl, Zeiten gleich;
  Knochen/Namen/Eltern/Offset/Bind bit-gleich.
- <= 20.000 Dreiecke (Ziel <= 19.850), <= 4 Einfluesse, Summe 1, keine negativen, 1 Netz / 1 Primitiv / 0 Materialien.
- Kopf: Maske 3.5 (`kopf.py`, `textur_pruef_pfote.py` mit den neuen Flecken); Krallen: Form/UV/Gewichte bit-gleich, vorn Lage wie
  baer-pfoten, hinten Lage + (-0,070, 0, 0) +-0,1 mm; Krallen-Texel bit-gleich oder dunkler nach 4.
- Boden: je Clip tiefster Punkt (Netz, je Pfote Haut und Kralle) >= Grundlinie heute - 0,05 cm (Grundlinie neu am heutigen GLB mit
  Kopie von `_arbeit/baer_pfote/spez/heute_tiefst.py`); Sitz-Clips 5.5; **Liegehoehe Dead/Death tiefster Punkt in [heute - 0,05;
  heute + 1,0 cm]** -- schwebt der schmalere Rumpf liegend hoeher, melden (8.4).
- Dehnung (`dehnung.py`, `regionen.py`): je Clip 99,5 % <= 2,6, Hoechstwert <= 4,0, Achsel/Brust <= 3,5; neu berichtet: Hals/Nacken in
  den Sitz-Clips, Region Bein-Uebergang z 0,12-0,50.
- Falten liegend (Dead): Achsel+Ellbogen sigma2 < 0,5 <= 136 (heute, Ziel 120), sigma2 < 0,3 <= 200.
- baer-fell/pfoten bleibt: Ei (Rear 1,3 s, `ei.py`) >= 0,95 (heute 1,032); Unterseite (`mess_textur.py`) >= 0,40 je Region;
  Straehnen Ruecken (`mess_bild.py`) Kontrast >= 0,063, Kohaerenz >= 0,60; Gesaessfalte im Ton von hinten sichtbar; Vorderpfoten wie
  baer-pfoten (Ja/Nein-Tabelle `SPEZ_PFOTEN.md` 3.4 vorn).
- Deer: 40 Knochen, Offset/Bind gleich, UV passt zum neuen Netz. Genau die 5 Dateien, gleiche Pfade, PNG-Typ/-Groesse gleich.

### 8.2 Messungen mit Grenzwerten (alle Zahlen `spez/soll_2c.json`)
| Teil | Mass | Grenze |
|---|---|---|
| Beine | Tabellen 2.1 / 2.2 | +-1,5 cm (Hinterkante bis z 0,40 +-1,0) |
| Beine | keine Glocke 2.3 (Ruhe, Idle 0, Walk 2/20) | Zunahme/5 cm vorn <= 3,0, hinten <= 3,5, >= -0,5, Schritt <= 1,6 x Mittel |
| Rumpf | Tabelle 2.4, Gesamtbreite | <= 0,82 m |
| Nacken | Ruecken z bei x 0,40/0,50/0,60 | 1,05-1,07 / 0,96-0,99 / 0,90-0,92; Buckel x 0,10-0,30 +-1,5 cm |
| Hinterfuss | Tabelle 4 (Laenge, Breiten, Ferse, Ballen, L/B, Texel) | wie Tabelle |
| Sitzen | Tabelle 5.2 je Bild 0/30/60/90 | wie Tabelle |
| Sitzen | Fussabstand, Luecke Fuss/Pfote, Pfoten gleiten | 62-72 cm, >= 2 cm, <= 1 mm |
| Kopf | Tabelle 6.1 | Spalte Soll (bzw. K1-Ersatz) |
| Gebiss | 3.1 Masse je Zahn, 3.2 Luft, 3.4 Dreiecke | Krone oben 4,2-5,0, unten 3,6-4,8; Luft >= 2 mm; 700-874 |
| Gebiss Spielgroesse | pxu 560, el 30, Rear Bild 48 | obere Eckzaehne je >= 5 px hoch, Helligkeit Zahn minus Rachen >= 80 |

### 8.3 Pflichtbilder (Ton = ohne Textur UND Textur Licht B; nah UND Spielgroesse; alt NEBEN neu; jedes Bild ansehen)
1. **Sitzen aus Kevins Spielkamera** (az 0, el 30, Sit Bild 0/30/60/90, Ausschnitt wie `spez/log/auftrag_heute.json`): Kevins
   Spielbild | alt | neu | Vorlage; dazu dieselbe Ansicht in Spielgroesse (Baer ~260 px breit wie im Spielbild).
2. Sitzen von vorn (az 0 el 0) und im Vorlagen-Blick (az -30 el 8): alt | neu | Vorlage; Zonenbild alt | neu (Kopf rot).
3. **Hinterfuss nah** im Sitzen (az 0 el 10) neben den Vorlagen-Fuessen (`b3`-Ausschnitte); Ruhe Sohle von unten (el -90), Seite, vorn.
4. **Vorschau-Video** Hinsetzen -> eine Sitz-Schleife -> Aufstehen, Spielkamera, Textur (mp4 unter `_arbeit/baer_2c/`).
5. **Stehen seitlich aus der Spielkamera** (az +90, el 30, Idle Bild 0; Baer schaut nach links wie in Kevins Bild): alt (`b4`) | neu;
   dazu Walk Bild 2/20 und Run, Seite el 0 und Spielwinkel az 50/130 el 30.
6. Beine Ruhe Seite/vorn/hinten Ton: alt | neu | Skizze (`forschung/beine/skizze_*.png`).
7. **Gebiss neben der Bruell-Vorlage**: Rear Bild 48 (1,60 s) mit den Kameras der Forschung (`forschung/gebiss/mess/kameras.json`, a1-a6),
   Bite 13, Maul 13, Eat 15 und ein Kau-Bild, Maul zu (Idle) nah, Spielgroesse (pxu 560, el 30) -- alt | neu | Vorlage.
8. Vorschlaege (6.3) als eigene Blaetter, klar beschriftet "nur Vorschlag".
9. Ja/Nein je Bild (Pruefer Optik UND Gegenpruefer, Bildpfad + Satz): "Hose im Stiefel?", "Kopf in der Kapuze?", "Menschenfuss?",
   "Zaehne/Zunge wie die Vorlage?" -- im Ton genauso wie mit Textur. Endgueltig urteilt Kevin im Spiel ("statisch geprueft, nicht gespielt").

### 8.4 Ausdruecklich Clip-Runde (in diesem Lauf nicht machen, nur melden)
1. Lefzen hochziehen / Unterlippe haengen (Bruellen) -- braucht Lippenknochen oder Spuren.
2. Liegehoehe Dead/Death, falls der schmalere Rumpf liegend schwebt (8.1).
3. Schmalerer Stand und Hinterfuesse 10-15 cm weiter unter den Koerper im Stehen/Gehen (forschung_beine 4.2).
4. Schenkel-Hinterkante weiter nach hinten, wo die 12 Clips es heute verbieten (2.2).
5. Toe0 abrollen im Gang (SPEZ_PFOTEN 4.2 C1).
6. Aufrichten neu (Kevin 08.11.) -- bleibt fuer die Clip-Runde.
7. Senkrechter Oberkoerper wie die Vorlage: nur mit laengeren Vorderbeinen (Knochen) -- Information, kein Auftrag.

-------------------------------------------------------------------------------------------------------------------------------

## 9. Risiken
| # | Risiko | Gegenmittel / Messung |
|---|---|---|
| R1 | Dehnung steht schon bei 2,59/2,6; schmalere Achsel +0,2 (Forschung) | `gewichte`-Optimierung mit, Achsel zuerst; Rueckfall Schulter-Halbbreite 0,40 -> 0,42 |
| R2 | Ei-Form sinkt (Attrappe 1,032 -> 0,999) | Wand erst unter z 0,50 schraeg, `FORM_SCHULTER` nachziehen; Grenze 0,95 |
| R3 | Dead schwebt nach dem Verschmaelern | 8.1 Band +1,0 cm, sonst Clip-Runde |
| R4 | Sitz-Ausnahme Kopf/Hals: Halshaut knittert (K2 zeigt Ringe am Hals im Ton) | Hals-Gewichte (nicht Kopf) nachziehen, Dehnung Hals; Rueckfall K1 |
| R5 | Sitzflaeche/Huefte haengt an der Kontaktlage der Schenkel (Huefte 0,286-0,342 je nach Sprunggelenk) | Pose mit dem fertigen Netz aus (1) neu loesen (Haut messen, nicht schaetzen) |
| R6 | Zwei Bauer in `baer_kampf_2c.py` | Aufteilung 7.2: Koerper nur `gewichte_eigen`, Gebiss eigene Datei |
| R7 | Kragen bleibt trotz K2 + C4 ueber +2 cm | Nacken 2.4 tiefer (bis -5 cm), Vorschlag Kopf x1,12; melden |
| R8 | Hellere Schulter-Texel schwaechen die Straehnen | nur im Band 6.2, Straehnen-Mass 8.1 |
| R9 | Budget Beine/Gebiss | 7.1; Sparfassung Maul 700 |
| R10 | Vorlage ist ein stilisiertes Stockbild (kleine Pfoten, langer Arm) | Masse sind Verhaeltnisse, Ziel ist K2, nicht die Vorlage woertlich |
| R11 | Hinterfuss-Kontakt im neuen Sitzen: kurze Ferse + Fell muss aufliegen, nicht stecken | Ferse tiefste Haut 0,0-0,5 cm je Bild |

## 10. Dateien dieser Spez (`_arbeit/baer_2c/`)
- `SPEZ_2C.md` (dieses), **`spez/soll_2c.json`** (alle Soll-Zahlen)
- Werkzeuge `spez/werkzeug/`: `mess_sitz.py`, `mess_brustband.py`, `mess_naht.py`, `mess_texel_naht.py`, `sitz_fk.py`, `sitz_fk_suche.py`,
  `sitz_fk_dbg.py`, `sitz_kand.py`, `kopf_skala.py`, `krallen_probe.py`, `raster.py`, `blatt.py`, `render_optik.py`, `gpu_render.sh`, `dumpread.py`
- Logs `spez/log/`: `mess_sitz_heute.txt|json`, `mess_brustband.txt`, `mess_texel_naht_heute.txt`, `sitz_fk.txt|json`, `sitz_fk_suche.txt|json`,
  `sitz_kand.txt|json`, `kand_K1|K2|K3|K2_kopf112.npy`, `krallen_probe.txt`, `zonen_sitz.npz`, `auftrag_heute.json`, `auftrag_kopf.json`, `render_*.log`
- Bilder `spez/render/` (31 Einzelbilder), Blaetter `spez/blaetter/b1-b5` (mit Vorlage/Spielbild: nur lokal), Ansehkopien `referenz/`,
  `spez/referenz/` (Raster)
