# Lauf baer-pfoten: Bau-Spezifikation "vier echte Baerenpfoten" (09.11.2026)

Grundlage: `forschung_referenz.md`, `forschung_bestand.md` (beide ganz gelesen, alle ihre Bilder und Kevins drei Vorlagen angesehen),
eigene Nachmessung am heutigen GLB (Dump `bestand/dump_heute.txt`, MD5 GLB 2a4837f6...). Skripte/Ausgaben der Spez in `spez/`.
**Statisch/offline gemessen und gezeichnet, nichts gebaut, nichts gerendert, nicht gespielt.** Nichts in Test-Mod, NPC Crew oder
`baer_fell` geschrieben, nichts committet. Masse in **Spielmetern** (Tier-Rahmen: x vorn, y links, z oben; Ruhe = Bind-Pose des GLB),
immer fuer das **fertige GLB mit Huelle**, linke Pfoten; rechte = y gespiegelt. Umrechnung ins Hochmodell: `x_h = x/0,75 - 0,0811`,
`y_h = y/0,75`, `z_h = z/0,75 + 0,0013` (`baer_export_fell.py:59`, `:292`, `:490-495`).

Skizze (selbst gezeichnet, aus Messungen): **`_arbeit/baer_pfote/spez_skizze.png`** (Seite, vorn, Abdruck je Hinter-/Vorderpfote; rot =
heute gemessen, gruen = Soll, orange = Clip-Verbot). Alle Soll-Zahlen maschinenlesbar: **`spez/pfoten_plan.json`** (eine Quelle fuer
Pfotenfeld, `ballen_plan` und Textur; erzeugt von `spez/spez_skizze.py`).

---------------------------------------------------------------------------------------------------------------------------------

## 0. Kurz (Entscheidungen)

1. **Ursache bestaetigt** (beide Berichte, eigene Schnitte `spez/heute_kontur.json`): Fellhuelle +7 cm je Seite bis zum Boden, flach
   abgeklemmt; Bein 34-36 cm dick, Zehen 4-7 cm vor der Saeule, Sohle = Stirnflaeche. Kevin hat recht.
2. **Neu:** das Bein **verjuengt sich ab 36 cm Hoehe** auf ~19-20 cm am Gelenk, darunter ein **eigener Fuss**: hinten Ferse (rund),
   Rist, flache Sohlenplatte, fuenf einzelne Zehen, Zehen ragen **20 cm** vor das Schienbein (heute 6,6); vorn breite Pranke, querliegender
   Handballen, fuenf Zehen, angehobener Handwurzelballen, Zehen **12 cm** vor dem Unterarm (heute 4,2).
3. **Laenge des Hinterfusses bleibt gross (gesamt 43 cm, Sohlenplatte+Zehen 34,6 cm) statt 29 cm der Referenz.** Grund gemessen: fester
   Fussknochen (22,5 cm Gelenk -> Ballen) und die Sitz-Pose (Sprunggelenk im Sit 15,7 cm hoch): eine Ferse bei x -0,52 schwebte im Sitzen
   **12,5 cm** ueber dem Boden (`spez/grenzkurve.txt`). Die Pfoten werden damit ~1,15-1,2 x so gross wie bei einem echten grossen Maennchen
   (Referenz-Verhaeltnisse bleiben: Platte deutlich laenger als breit, Fuss laenger als das Bein dick).
4. **Krallen:** hinten **bit-gleich** (K0). Vorn **K1**: nur in y zur Mittelkralle geschoben (Teilung 4,6 -> 4,1 cm, Form/UV/Gewichte gleich),
   damit die Pranke "breiter als tief" wie Kevins Sohlenfoto wird (L/B 1,1); gemessen in keinem Clip tiefer (`spez/k1_probe.txt`).
5. **Clips bleiben bit-gleich.** Was nur mit Clips geht (Ferse liegt im Sitzen auf, Zehen rollen ab), steht in 4.2 fuer die Clip-Runde.

## 0.1 Gegenpruefung der beiden Berichte (Widersprueche, selbst nachgemessen)

| # | Punkt | Referenz | Bestand | eigene Messung (Beleg) | gilt |
|---|---|---|---|---|---|
| 1 | Ferse flach am Boden | - | "nicht weiter als x -0,58" | flach (z = 0) nur bis **x -0,550**: bei -0,56/-0,58 ginge die Ferse im Walk 1,8/2,0 cm (HL, heute 1,72) bzw. 1,5/1,7 cm (HR, heute **1,41**) in den Boden. Die heutige Ferse bei -0,56..-0,60 liegt in Ruhe 0,4 cm ueber dem Boden, deshalb "nur" -1,7 (`spez/nachmessen.txt`, `spez/grenzkurve.txt`, `spez/heute_tiefst.txt`). Bestand hat nur die linke Seite gerechnet. | **-0,550**, dahinter Grenzkurve 1.4 |
| 2 | Hinterfuss-Laenge | 29 (28-31) cm | Ferse bis ~-0,63, Zehen nicht weiter vor | Sitz-Auflage braucht Hinterkante **-0,629** (Sit 60: 1,2-1,9 cm Luft); Ferse -0,52 -> 12,5 cm Luft; Zehen sind durch die Krallen bei -0,175..-0,24 festgelegt | gesamt 43 cm, Platte+Zehen 34,6 |
| 3 | Hinterfuss-Breite | 15 (+Fell 17-18) | - | Krallen hinten Teilung 3,7 cm, Mitten y 0,166..0,315 (`spez/krallen_lage.txt`) -> Zehenreihe 18 cm | Platte 16,5-17,5, mit Fell 20-21 |
| 4 | Vorderpfote Breite | 16 (+Fell 18-19) | - | Krallen vorn Teilung 4,6 (Reihe 22,5 cm) -> mit K1 4,1 (Reihe 20,4) | Handballen 17-18 |
| 5 | Zehen vorn am Boden | - | "nicht weiter vor als heute (-0,19 / 0,52)" | stimmt, genauer: Auflage bis **-0,210 / 0,500**, davor Anstieg nach Tabelle 1.4 | Grenzkurve |
| 6 | Unterschenkel/Handgelenk | 15-18 / 16-20 (Schaetzung) | duenner, 2-3 cm Huelle | Hochmodell-Haut in 20 cm heute schon 21 x 20 cm (`bestand/schnitt_mass.txt`) | 19-20,5 (x1,15 der Referenz) |
| 7 | Gewichte | - | "muessen am Gelenk trennen" | das heutige Hoehenband 5,5-17,5 cm liegt am Gelenk (z 0,10); mit der neuen Form genuegt eine Korrektur fuer den Fussruecken vor dem Gelenk (2.3). Heute haengt die Sitz-Auflage an Mischgewichten der Hock-Rueckseite (x -0,636, z 0,109: Fuss 0,58 / Wade 0,40, `spez/nachmessen.txt`) | 2.3 |
| 8 | uebereinstimmend | 22,5 cm Gelenk->Ballen; Abdruck 41,0 x 22,9-23,1; Bein 34-36; Zehen-Ueberstand 6,5-6,7 / 4,3-4,4; Sit Fuss +81,4 Grad, Sohlen-Normale 5 Grad; Toe0 dreht nie; 18.930 Dreiecke | | eigene Schnitte gleich | - |

---------------------------------------------------------------------------------------------------------------------------------

## 1. Zielform je Pfote (fertiges GLB, Ruhe, Spielmeter; Toleranz in Klammern, Clip-Grenzen 1.4 sind hart)

### 1.1 Ueberall
- Oberhalb **z 0,36** bleibt die Form wie heute (Rumpf, Ei-Form, Gesaessfalte, Schultern): Abstand neu->baer-fell dort p95 <= 0,5 cm,
  max <= 1,5 cm (ohne Kopf, der ist bit-gleich). Zwischen z 0,36 und 0,25 weicher Uebergang (kein Absatz > 1 cm je 2 cm Hoehe).
- **Fell an der Pfote** (Huelle) duenn: Zehen 0,3-0,6 cm, Fuss/Pranke 0,6-1,0 cm, Gelenk 1,0-1,5 cm, z 0,20 ~2 cm, z 0,30 ~4-5 cm,
  ab z 0,36 wie heute (7,1 cm). Die Huelle verdeckt nie Zehenrillen, Rist oder Ferse.
- **Sohlenrand rund**, kein Kantenknick: Knick zwischen flachem Abdruck und Seitenwand Mittel <= 20 Grad, p90 <= 35, max <= 55 (heute
  HL 20,8 / 49,5 / **84,7**, VL 20,1 / 46,8 / 68,0; `spez/heute_kontur.py`). Fellkranz 1,5-2 cm um die Ballen (Textur), Fell faellt
  ueber den Rist, schluckt aber nie die Zehen.
- Der flache Abdruck (z <= 0,5 cm) ist je Pfote **eine** zusammenhaengende Flaeche (Voraussetzung fuer `sohlen_bauen`, das die groesste
  Komponente nimmt, `baer_export_fell.py:927-930`).

### 1.2 Hinterfuss (HL; Sprunggelenk -0,48/0,247/0,10, Ballen -0,25/0,24/0,045, Knie -0,35/0,41)

Seitenumriss (Mittellinie, Schnitte quer; heute aus `spez/heute_kontur.json`):

| z (cm) | Hinterkante x (+-0,5 cm) | Vorderkante x | Tiefe | heute Hinter / Vorder |
|---|---|---|---|---|
| 0 (flach) | -0,550 | -0,212 | 33,8 | -0,563 / -0,226 |
| 0,5 | -0,567 | -0,206 | | -0,591 / -0,200 |
| 1,0 | -0,600 | -0,200 | | -0,606 / -0,195 |
| 2,6 | -0,624 | -0,1955 (Zehenfront) | | -0,613 / -0,191 |
| 5 | -0,629 | -0,208 (Zehenoberkante 5,0-5,5) | | -0,622 / -0,202 |
| 10 | -0,629 | -0,363 (Rist) | 26,6 | -0,634 / -0,246 |
| 15 | -0,620 | -0,397 | 22,3 | -0,635 / -0,263 |
| 20 | -0,605 | -0,402 (Schienbein) | **20,3 (19-21,5)** | -0,621 / -0,257 (36,4) |
| 25 | -0,606 | -0,375 | 23 | -0,612 / -0,228 |
| 30 | -0,610 | -0,30 (Uebergang) | ~31 | -0,610 / -0,200 |
| 36 | wie heute -0,605 | wie heute -0,172 | | |

- **Ferse**: rund; Hinterkante -0,629 (+0/-0,3 cm) von z 4 bis 11 cm (Sitz-Auflage, nicht weiter hinten: Clip-Verbot), darueber eine
  flache Kehle (-0,605 in 20 cm, Ferse ragt >= 2 cm hinter die Kehle). Fersenunterseite steigt von x -0,550 (z 0) flach an (Tabelle 1.4).
- **Rist**: Fussruecken faellt vom Schienbein (z ~0,16 bei x -0,40) gleichmaessig zu den Zehen: z_oben 12 cm bei x -0,375, 9 bei -0,33,
  7,7 bei -0,30, 6,0 bei -0,25 (+-1 cm). Kein senkrechtes Stueck vor dem Gelenk.
- **Breite** (von vorn, Mitte y 0,242, +-1,5 cm bis z 25): z 0 (Abdruck an der Zehenreihe) 18; z 1 19,5; z 3 20,5 (Zehen mit Fell);
  z 6 20; **z 10 19 (heute 31,1); z 15 19 (33,6); z 20 20,5 (34,7)**; z 25 23,5; z 30 27; z 33 31; z 36 wie heute 36. Regel: Bein in
  10-15 cm hoechstens so breit wie der Fuss an den Zehen (mit Fell) minus 0,5 cm.
- **Zehen** (5): je ein runder Hoecker um die Krallenwurzel; Krallen **bit-gleich**, Mitten y 0,166 / 0,204 / 0,240 / 0,277 / 0,315,
  Wurzeln x -0,240 / -0,213 / -0,203 / -0,212 / -0,239, z 0,040-0,045 (`spez/krallen_lage.txt`). Zehenhoehe (Haut oben) mittlere drei
  5,0-5,5 cm, aeussere 4,5-5,0, Zeh 1 (innen, y 0,166) 15 % kleiner. Breite je Zeh = Teilung 3,7 cm (an der Basis beruehrend).
  **Rillen** zwischen den Zehen oben >= 1,2 cm tief und >= 1,2 cm offen (V-Form), an der Stirn >= 0,8 cm. Krallenwurzel liegt 0,2-0,8 cm
  in der Haut (kein Spalt, keine freistehende Kralle). Krallen ragen 2-2,5 cm vor die Zehenstirn (Spitze -0,175 bleibt).
- **Sohle** (Abdruck x -0,550..-0,212, y 0,150..0,335 an den Zehen, Ferse 11-12 breit): eine lange **Sohlenplatte** (Ballenhaut) vorn im
  Bogen hinter den Zehenballen (x -0,268 Mitte, -0,305 aussen; Fell-Luecke 1,2-1,5 cm), Breite bei x -0,33 16,5-17,5, bei -0,42 14-15,
  bei -0,48 11-12, bei -0,525 8,5-9,5, hinten rund bis -0,562 (zieht 0,5 cm an der Ferse hoch). **Zehenballen**: Mitte x = Krallenwurzel
  -3,2 cm (+-0,5), y = Krallenmitte, Halbachsen y 1,65 x 1,9 cm (Zeh 1 x 0,85). Platte+Zehen 34,6 cm lang, L/B ~2,0 (Referenz 1,7-1,9;
  Grund 0.3). Zehenanteil (Bogen der Zehenballen) ~24 % der Laenge (Referenz 25-30 %).

### 1.3 Vorderpfote (VL; Handgelenk 0,32/0,23/0,10, Ballen 0,48/0,22/0,045, Ellbogen 0,23/0,41)

| z (cm) | Hinterkante x (+-0,5) | Vorderkante x | Tiefe | heute Hinter / Vorder |
|---|---|---|---|---|
| 0 (flach) | 0,300 | 0,500 | 20 | 0,262 / 0,489 |
| 0,5 | 0,296 | 0,5055 | | 0,240 / 0,504 |
| 1,0 | 0,286 | 0,516 | | 0,229 / 0,520 |
| 1,75 | 0,26-0,272 (Handwurzelballen unten) | 0,521 | | |
| 2,6 | 0,246 | 0,5235 (Zehenfront) | | 0,210 / 0,526 |
| 4,5 | 0,237 | 0,522 | | (z 5) 0,190 / 0,523 |
| 6,6 | 0,234 | 0,503 (Zehenoberkante 6,0-6,6) | | |
| 10 | 0,228 | 0,415 (Pranken-Ruecken) | 18,7 | 0,164 / 0,471 |
| 15 | 0,218 | 0,401 | 18,3 | 0,149 / 0,474 |
| 20 | 0,205 | 0,400 (Unterarm) | **19,5 (18,5-21)** | 0,143 / 0,484 (34,2) |
| 25 | 0,190 | 0,405 | 21,5 | 0,132 / 0,495 |
| 30 | 0,160 | 0,430 (Uebergang) | 27 | 0,121 / 0,501 |
| 36 | wie heute 0,109 | wie heute 0,501 | | |

- **Breite** (von vorn, Mitte y 0,213): z 0 18,5; z 1 20,5; z 3 21,5 (Zehen mit Fell); z 6 20,5; **z 10 19 (heute 29,0); z 15 19 (33,1);
  z 20 20,5 (34,3)**; z 25 23; z 30 27; z 33 32; z 36 wie heute 37,6. Regel: Handgelenk (z 10-15) mindestens 1,5 cm schmaler als die
  Zehenreihe mit Fell.
- **Zehen** (5): Krallen **K1**: Mitten y 0,131 / 0,172 / 0,213 / 0,254 / 0,295 (Verschiebung +1,0 / +0,5 / 0 / -0,5 / -1,0 cm, nur y;
  x/z, Form, UV, Gewichte unveraendert), Wurzeln x 0,467 / 0,500 / 0,513 / 0,502 / 0,468, z 0,053-0,058. Zehenhoehe mittlere drei
  6,0-6,6 cm, aeussere 5,5-6,0; Breite je Zeh = Teilung 4,1; Rillen wie hinten (>= 1,2 oben, >= 0,8 Stirn); Krallen ragen 4,5-5,5 cm vor
  die Zehenstirn (Spitzen bleiben bei 0,507-0,561).
- **Handballen** quer: x 0,325..0,440 in der Mitte (Tiefe 11,5), aussen 0,334..0,398 (Vorderkante nach vorn gewoelbt), Breite 17-18
  (y 0,124..0,303), Luecke zu den Zehenballen 0,8-1,5 cm. **Zehenballen**: Mitte x = Krallenwurzel -3,6 cm (+-0,5), Halbachsen y 1,9 x 2,3
  (Zeh 1 x 0,92). Laenge Zehenstirn bis Handballen-Hinterkante 19,9 = **1,1 x Breite** (Kevins Sohlenfoto 1,13).
- **Handwurzelballen**: rund, Durchmesser 5,8 (5,5-6,5), Mitte x 0,265, **aussen** (y 0,258 = 4,5 cm neben der Mittelkralle), unterster
  Punkt **z 1,5-2,0 cm** (steht im Stand nicht auf; Clip-Grenze 1.4), hebt sich >= 0,8 cm aus der Fellflaeche, >= 2,5 cm Fell zum
  Handballen. Laenge bis Handwurzelballen-Ende 0,5235-0,236 = 28,8 = 1,6 x Breite (Referenz 1,7-1,8).

### 1.4 Clip-Grenzen der Unterseite (hart; `spez/grenzkurve.txt`, L und R getrennt, das Strengere)
Fuer jeden Punkt mit vollem Hand-/Fuss-Gewicht: kleinste erlaubte Hoehe ueber dem Boden in Ruhe, damit er in **keinem** Clip tiefer in den
Boden geht als die heutige Haut dieser Pfote in diesem Clip (Grenze je Clip `min(heute, 0) - 0,05 cm`). Empfohlen +0,25 cm Abstand.

| Hinterfuss Ferse x | -0,550 | -0,555..-0,575 | -0,58..-0,595 | -0,60..-0,615 | -0,620 | -0,625 | -0,630 | < -0,630 |
|---|---|---|---|---|---|---|---|---|
| z min (cm) | 0 | 0,25 | 0,5 | 0,75 | 1,0 | 1,25 | 3,75 | verboten bis z 15 |
| Sit Bild 60 Luft (cm) | 9,5 | 9,0-7,0 | 6,5-5,0 | 4,5-3,0 | 2,4 | 1,9 | 1,2 | - |

| Hinterfuss Zehen x | <= -0,210 | -0,205 | -0,200 | -0,195 | -0,190 | -0,185 | -0,180 | -0,175 |
|---|---|---|---|---|---|---|---|---|
| z min (cm) | 0 | 0,25 | 0,5 | 0,75 | 1,25 | 1,5 | 1,75 | 2,0 |

| Vorderpfote hinten x | >= 0,27 | 0,25-0,26 | 0,22-0,24 | 0,20-0,21 | | Vorderpfote Zehen x | <= 0,500 | 0,505-0,51 | 0,515 | 0,52 | 0,525 | 0,53 | 0,535 | 0,54 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| z min (cm) | 0 | 0,25 | 0,5 | 0,75 | | z min (cm) | 0 | 0,25 | 0,5 | 0,75 | 1,0 | 1,25 | 1,75 | 2,0 |

Punkte mit Wadengewicht (Hock-Rueckseite z 8-15) verhalten sich anders; sie werden am fertigen Netz gemessen (3.1). Grundlinie heute je Clip,
je Pfote Haut/Kralle und ganzes Netz: `spez/heute_tiefst.txt|json` (z. B. Walk Haut VL -0,68, VR -0,58, HL -1,72, HR -1,41; Run
-0,77 / -0,51 / -1,53 / -1,26; Death ganzes Netz -1,81 (HR); Dead 0,01; Sit hinten Haut 0,16/0,10).

---------------------------------------------------------------------------------------------------------------------------------

## 2. Bau-Weg

### 2.1 Dateien (Kopien, Originale `*_anim.py`/`*_fell.py` bleiben unveraendert; Ausgaben nur unter `_arbeit/baer_pfote/`)
| Kopie (`baer/spiel/`) | aus | Pfade/Umgebung |
|---|---|---|
| `baer_quelle_pfote.py` | `baer_quelle_anim.py` | `OUT` -> `_arbeit/baer_pfote/hoch/` |
| `baer_export_pfote.py` | `baer_export_fell.py` | `QUELLE` -> `baer_quelle_pfote.py`; `BAER_PFOTE_NETZ` (Vorgabe `_arbeit/baer_pfote/netz/`), `BAER_PFOTE_ANS` (Fell-Ansichten, Vorgabe `_arbeit/baer_pfote/ansichten/`, fuer Form-Runden alt `_arbeit/baer_spiel/ansichten/` nur lesen), `MOD_FELL` -> `_arbeit/baer_pfote/mod/42/media/`; Kopf/Krallen weiter aus `baer_anim/modell/alt/` (nur lesen) |
| `baer_kampf_pfote.py` | `baer_kampf_fell.py` | GLB-Ziel/Quelle per Argument wie heute, `NCB_PFOTE_GEWICHTE` |
| `baer_gewichte_pfote.py` | `baer_gewichte_fell.py` | Argumente wie heute |
| `baer_textur_pfote.py` | `baer_textur_fell.py` | `BAER_TX_DIR`/`BAER_TX_ANS`/`BAER_FELL_NETZ` mit Vorgaben unter `_arbeit/baer_pfote/textur/` |
| Kette `werkzeug/lauf_pfote.sh` | `baer_fell/fix/lauf_fix.sh` | alle Pfade nach `_arbeit/baer_pfote/`; Deer weiter mit dem Original `baer_tier_anim.py` (unveraendert aufgerufen) |
| Werkzeug-Kopien nach `_arbeit/baer_pfote/werkzeug/` | `baer_fell/netz/` (messen, glb_pruef, pruef_netz, lowpoly_npz, karten, falten_fell), `baer_fell/pruef/gegen/werkzeug/` (regeln, dehnung(+_lib), gewichte, glb_datei, textur, deer, klein), `baer_fell/fix/werkzeug/` (ei, fremd, mess_bild, dehn_tab), `baer_fell/textur/werkzeug/` (mess_textur, body1024), `render_optik.py`, `gpu_render.sh` (schon da) | nur kopieren |
| neu `werkzeug/pfote_abnahme.py` | aus `spez/heute_kontur.py`, `grenzkurve.py`, `heute_tiefst.py`, `k1_probe.py` | Masse von Abschnitt 3.2 am Dump |

### 2.2 Was sich aendert (Funktionen, Zeilen der Originale)
**`baer_quelle_pfote.py` (Hochmodell)**
- `:897-905` Beine: Fuss-/Pranken-Ketten `:901` und `:905` **weg**; Unterschenkel/Unterarm `:900`, `:904` unten duenner (Endradius heute
  0,205/0,20 Hochmodell, Richtwert 0,14-0,15; einstellen bis die Haut-Schnitte = Soll minus Huelle aus 1.1 sind). Oberhalb z_spiel 0,36
  nichts aendern (Rumpf-Voxelgitter, Risiko R8).
- `:1482-1568` `PFOTEN`, `zehen_lage`, `zehen_feld_fn`, `pfote_bauen` -> **`pfote_feld_fn(pfote)`** aus `spez/pfoten_plan.json`
  (Spiel -> Hochmodell umgerechnet, Soll minus Huelle): Gelenk-Manschette (ueberlappt das Metaball-Bein bis z_spiel ~0,18, gleicher Radius am
  Treffpunkt), Fersenbein + Hock-Polster bis zur Hinterkante 1.2, Rist, flache Sohlenplatte mit runder Kante (Radius >= 1,5 cm Spiel),
  fuenf Zehen-Kapseln (Radius = halbe Teilung, enden 0,2-0,8 cm vor der Krallenwurzel), vorn Handwurzelballen-Kugel; weiche Vereinigung
  (`smin`), Boden wie heute `smax(d, 0.003 - z)`. Netz `pfote_<bn>` wie heute starr am Hochmodell-Knochen (`on_bone`, `:1265`).
- Hochmodell-Krallen (`krallenpfad`/`rohr`, `:1533-1558`) an die neuen Lagen (vorn K1), Form gleich (nur fuer Ansichten/Textur).
- `zehen_abstand` (`:1571`) -> `pfoten_abstand` (Abstand zum Pfotenfeld); Fell `:1589-1610` (d_bein, l_bein: am Fuss kurz 1-2,5 cm Spiel,
  keins auf Ballen/Sohle/Handwurzelballen), Zehenhaar `:1720-1741` auf die neuen Zehen.

**`baer_export_pfote.py` (Spielnetz)**
- neue Stufe **`ansichten`** (aus `baer_export.py:160` `stufe_ansichten` samt `kamera_daten`, `kopf_kameras`, `gpu`, `neutrale_welt`),
  Ausgabe `BAER_PFOTE_ANS` (die alten Ansichten kennen den neuen Fuss nicht).
- `huelle_bauen` (`:658`): Teile `pfote_*` statt `zehen_*` (`:674`); `dlim` (`:695-702`) neu nach 1.1 (Pfotenabstand + Hoehe statt
  ueberall 0,112-0,022 Hochmodell = 7,1 cm Spiel); Bodenklemme `:724`, `:1172`, `:1178`, `:1385` bleibt (schneidet nur noch ~1 cm der
  eigenen Sohle).
- `stufe_netz_anim` (`:1139`): Taubin-Gewicht an der Pfote 0,10 (`:1159`, heute Zehen 0,25), `falten_fuellen` bleibt unter z_h 0,30 aus
  (`:1163`), `form_fell` auf Pfotenmasken pruefen; Verringern (`:1323` Gruppe `frei`): Pfoten Gewicht ~0,3 (weniger verringert), `RUMPF_ZIEL`
  (`:74`) nach Budget 2.5.
- `sohlen_bauen` (`:897`): `RASTER` 0,015 -> 0,020 (`:805`), `BALLEN_HUB` 0,008 -> 0,012 (`:802`, bau_netz.md 8.3), `ballen_plan`
  (`:848`) liest `pfoten_plan.json` statt fester Abstaende zu den Krallen (Handwurzelballen gehoert nicht in den flachen Abdruck).
- Krallen (`:1392-1398`, alte Schalen): vorn je Kralle die K1-Verschiebung in y; `stufe_kopfprobe` (`:2082`): Kopf bit-gleich wie heute,
  Krallen hinten bit-gleich, vorn "Form/UV/Gewichte bit-gleich, Lage = alt + Plan (+-0,1 mm)".

**`baer_kampf_pfote.py` (Gewichte-Formel, GLB)**: `:1734` `w_fu = 1 - sst(0.055, 0.175, z)` bleibt als Grund (Band am Gelenk z 0,10), dazu
**Fussruecken-Korrektur**: `w_fu = max(w_fu, sst(0.04, 0.09, sx*(x - x_gelenk)) * (1 - sst(0.10, 0.16, z)))` (sx = +1 vorn/Fuss vor dem
Gelenk; x_gelenk -0,48 hinten / 0,32 vorn). Krallen starr (`:1741-1746`) bleibt.
**`baer_gewichte_pfote.py`**: `:96` frei = ausserdem nicht in der Pfote (Formel-Fussgewicht >= 0,95 bleibt Formel); Rest wie baer-fell.
**`baer_textur_pfote.py`**: Ansichten neu (Hochmodell neu); `sohlen_malen` (`:627`) nach `pfoten_plan.json`; Ballen, die nicht im flachen
Abdruck liegen (Fersen-Hochzug, Handwurzelballen), ueber eine 3D-Maske aus dem Plan malen; Zehenrillen dunkler (Geometrie/AO). Alles
andere wie baer-fell (helle Unterseite, Straehnen, Kopf-/Krallen-Texel).

### 2.3 Reihenfolge und Laufzeiten (Zeiten aus `forschung_bestand.md` 4 bzw. `baer_fell/fix/log`)
| Schritt | was | Zeit | GPU |
|---|---|---|---|
| 0 | Kopien, Pfade, `pfoten_plan.json` einlesen, `lauf_pfote.sh` | ~20 min Arbeit | - |
| 1 | **Form-Runden**: quelle (form) + netz mit ALTEN Ansichten + fbx + kopfprobe + formel + glb + Dump + `pfote_abnahme.py` + 16 Ton-Bilder (4 Pfoten x Seite/vorn/Abdruck/Sitz) | ~6-8 min je Runde, erwartet 3-6 Runden | ~1 min je Runde |
| 2 | Fell-Ansichten des neuen Hochmodells (`ansichten`) | ~6 min | ja |
| 3 | netz (neue Ansichten) -> fbx + kopfprobe -> formel -> **gewichte** -> messen/Dehnung -> glb + Dump + glb_pruef -> lowpoly/karten | 2,5 + 0,2 + 0,6 + **12-15** + 1 + 1 + 1 min | - |
| 4 | Textur-Ansichten (Ruhe + Posen) -> backen -> body + GLB -> deer | 5 + 2 + 1,2 + 0,7 + 1 min | 7 min |
| 5 | Pflichtbilder (3.3, ~180 Bilder) + Blaetter + alle Messungen | ~6 min Render + 5 min | ja |
Ganze Kette nach den Form-Runden ~40-45 min Maschine (GPU ~19 min); mit Form-Runden ~1,5 h. Vor jedem Render: `tasklist | grep -i
ProjectZomboid`, Sperre `gpu.lock`, fremdes Blender pruefen (`werkzeug/gpu_render.sh` macht alles drei); laeuft das Spiel: CPU-Schritte
weiter, Render spaeter (hoechstens 30 min warten, dann "Render offen").

### 2.4 Lauf-Vorschlag (Workflow, <= 10 Agenten)
Bauer Netz (Schritte 0-3, Form-Runden) -> Bauer Textur (4) -> Pruefer Technik + Pruefer Optik (parallel, 3) -> Nachbesserung ->
Gegenpruefer -> Integrator: 7 Agenten. Zwei Bauer nur nacheinander (Textur braucht das fertige Netz).

### 2.5 Dreiecks-Budget (nach dem Importer; heute 18.930 = Rumpf 14.499 + Sohlen netto 890 + Kopf 2.295 + Krallen 832 + Maul 414)
| Teil | heute | Ziel |
|---|---|---|
| Kopf + Krallen + Maul (fest) | 3.541 | 3.541 |
| 4 Pfoten (Haut mit Hand/Foot-Gewicht > 0,5, samt Sohle) | ~3.870 (943-992 je Pfote, Sohle 374-461) | **4 x 1.100-1.250** (Zehen ~500, Sohle ~250 bei Raster 20 mm, Ferse/Rist/Seiten ~400) |
| Rumpf ohne Pfoten | ~11.520 | 10.600-11.200 (duennere Unterschenkel; ggf. `RUMPF_ZIEL` 14.000) |
| **Summe** | 18.930 | **19.300-19.700** (hart <= 20.000, Reserve >= 300) |

---------------------------------------------------------------------------------------------------------------------------------

## 3. Abnahme

### 3.1 Feste Regeln (hart, Werkzeuge wie im Gegenbericht baer-fell Abschnitt 1)
- 15 Clips bit-gleich (Dump-Textbloecke + Animations-Puffer der Datei byteweise), Knochen/Namen/Eltern, Offset- und Bind-Matrizen gleich
  (`regeln.py`, `glb_datei.py`, `glb_pruef.py`).
- <= 20.000 Dreiecke nach dem Importer; <= 4 Einfluesse, Summe 1, keine negativen; 1 Netz, 1 Primitiv, 0 Materialien.
- **Kopf bleibt so**: 1.333 Kopfpunkte Lage+UV+Gewichte bit-gleich (hoechstens Nahtrand wie baer-fell), Kopf-Texel Body 1024 und
  WorldItems 2048 bit-gleich, Maul-Flecken frei.
- Krallen: hinten 2 x 5 alle 16 Werte bit-gleich; vorn 2 x 5 Form/UV/Gewichte bit-gleich, Lage = alt + K1-Plan (+-0,1 mm); Gewicht 1,0 an
  Hand/Foot; Krallen-Texel bit-gleich.
- **Kein Clip tiefer im Boden als heute**: je Clip tiefster Punkt des ganzen Netzes >= heute - 0,05 cm; je Pfote tiefste Haut >=
  min(heute, 0) - 0,05 cm; je Pfote tiefste Kralle >= heute - 0,05 cm (Grundlinie `spez/heute_tiefst.json`). Liegehoehe Dead >= 0,01 cm,
  Death >= -1,81 cm wie heute.
- Dehnung (`dehnung.py`, Regionen `regionen.py`): 99,5 % je Clip <= 2,6, Hoechstwert <= 4,0, Achsel/Brust <= 3,5; Ziel nicht schlechter als
  baer-fell + 0,10 (2,45 / 3,16 / 3,02). Neu getrennt berichtet: **Region Pfote/Gelenk** (Hand/Foot oder Forearm/Calf > 0,2, z < 0,36)
  99,5 % <= 2,6, max <= 4,0. Falten liegend (Dead, sigma2 < 0,5 Achsel+Ellbogen) <= 120 (baer-fell 88), sigma2 < 0,3 <= 200 (121).
- Fremde Gewichte (`fremd.py`): keine (Regeln baer-fell). Fussgewicht >= 0,95 unter z 6 cm und im Fussruecken vor dem Gelenk bis z 10;
  Wade/Unterarm >= 0,95 ab z 0,20 im Bein.
- Nur die 5 Dateien mit gleichen Pfaden, PNG-Typ/-Groesse gleich; Deer 40 Knochen, Offset/Bind gleich, UV passt zum neuen Netz.
- **Was baer-fell erreicht hat bleibt**: Rumpf oberhalb z 0,36 p95 <= 0,5 cm / max <= 1,5 cm Abstand zum baer-fell-Netz (Ruhe); Ei
  (Rear 1,3 s, `ei.py`) >= 0,95 (baer-fell 1,033); Unterseite (`mess_textur.py`) >= 0,40 je Region; Straehnen (`mess_bild.py`, Spielgroesse
  Licht B) Kontrast Ruecken >= 0,063, Kohaerenz Ruecken >= 0,60 (baer-fell 0,070 / 0,66); Gesaessfalte im Ton von hinten wie baer-fell.

### 3.2 Form-Masse (`werkzeug/pfote_abnahme.py` am Dump, alle vier Pfoten; heute in Klammern)
| Mass | Soll hinten | Soll vorn |
|---|---|---|
| Schnitte Hinter-/Vorderkante, Breiten | Tabellen 1.2/1.3 (+-0,5 bzw. +-1,5 cm) | dito |
| Bein am Gelenk schmaler als der Fuss: Breite z 15 vs. Breite z 3 | <= z3 - 0,5 (33,6 vs 25,2) | <= z3 - 1,5 (33,1 vs 24,0) |
| Fuss laenger als Bein dick: (Vorderkante z 2,6 minus hinterste Hinterkante z 0-12) / Tiefe z 20 | >= 2,0 (1,22) | >= 1,4 (1,06) |
| Abdruck (flach) / Tiefe z 20 | >= 1,6 (1,13) | >= 1,0 (0,83) |
| Zehen-Ueberstand: Vorderkante z 2,6 minus Vorderkante z 20 | >= 18 cm (6,6) | >= 10 cm (4,2) |
| Ferse ragt hinter die Kehle: Hinterkante z 5-11 minus z 20 | >= 2,0 cm (1,3) | - |
| Rist: Hautoberkante in der Fussmitte (hinten x -0,30, vorn x 0,46) | 6,5-9,0 cm (heute Saeule, kein Rist) | 6,5-8,5 cm |
| 5 Zehen: Hoehenprofil 1 cm unter den Zehenkuppen quer | 5 Maxima, 4 Rillen >= 1,2 cm | dito |
| Zehenstirn bei z 2,5 cm, Profil quer | 5 Vorspruenge, Einzuege >= 0,8 cm | dito |
| Krallenwurzel in der Haut | 0,2-0,8 cm | dito |
| flacher Abdruck: Lage, eine Flaeche | x -0,550..-0,212, 1 Komponente | x 0,300..0,500, 1 Komponente |
| Sohlenrand-Knick Mittel/p90/max | <= 20 / 35 / 55 Grad (20,8/49,5/84,7) | dito (20,1/46,8/68,0) |
| Ballen-Relief (Furchen) | 10-14 mm (8) | dito |
| Handwurzelballen unterster Punkt / Vorsprung | - | 1,5-2,0 cm / >= 0,8 cm |
| Sit Bild 60: Luft unter dem Hinterfuss (tiefste Haut HL/HR) | <= 2,0 cm (0,16/0,10), berichten | - |
| Dreiecke je Pfote | 1.050-1.300 | dito |

### 3.3 Pflichtbilder (Spiel-Licht B, `render_optik.py`; TON = ohne Textur; jedes Bild ansehen)
1. **Gleiche Kameras wie heute** (`bestand/auftrag_bestand.json`, 90 Bilder: Stehen, Gehen Walk Bild 22, Sitzen Sit 2,0 s, Aufrichten
   Rear 1,3 s, Liegen Dead; je Gesamtbild Spielwinkel, Seite el 0 Ton, je Pfote nah und Spielwinkel el 30, Ton + Textur) fuer **neu**; alt
   liegt in `bestand/render/`.
2. Dazu neu: **Rennen** (Run, Bild mit am besten sichtbarer Hintersohle) und **Gehen Schwungphase** (Walk, Hintersohle nach hinten, Kamera
   az 180 +-30, el 10); **SitDown Mitte**; **Swipe** (Vordersohle sichtbar); **Aufrichten von hinten** (Ferse sichtbar); **Sitzen von vorn**
   (az 0, el 10, beide Hinterfuesse, wie Kevins Hauptvorlage) und Sitzen in 8 Spiel-Azimuten (el 30, Textur); Ruhe je Pfote **Seite el 0,
   vorn el 0, unten el -90** (Ton + Textur, gleicher Ausschnitt wie die Skizze); **Spielgroesse** (Baer so klein wie im Spiel) fuer
   Stehen/Gehen/Sitzen.
3. **Blaetter je Pose**: Kevins Vorlage (nur zum Ansehen, nur lokal) | alt | neu, oben Ton, unten Textur, nah und Spielwinkel; ein Blatt
   "Ruhe neu gegen Skizze" (Seite/vorn/unten). Kevins Vorlagen nie in Mod oder Textur.

### 3.4 Ja/Nein: "abgesaegtes Bein?" (Pruefer Optik UND Gegenpruefer, je Zelle Bildpfad + Satz)
Je Pfote (VL, VR, HL, HR) x Pose (Stehen, Gehen, Rennen, Sitzen, Aufrichten, Liegen) = 24 Zellen, jede im **Ton-Bild** und im
**Textur-Bild**. "Nein" (= echte Pfote) nur, wenn alle fuenf gelten: (1) der Fuss ist eine eigene Form, die aus dem Bein ragt (hinten
Ferse + Zehen, vorn Zehen); (2) kein Rand/Ueberhang, wo Bein auf Sohle trifft, Bein schmaler als der Fuss; (3) fuenf einzelne Zehen;
(4) wo die Sohle sichtbar ist: Platte mit Ballen (hinten lang mit Ferse, vorn Handballen quer + Handwurzelballen); (5) im Ton genauso
lesbar wie mit Textur. Eine Zelle "Ja" = nicht abgenommen; "nicht sichtbar" nur mit Bildbeleg. Endgueltig entscheidet Kevin im Spiel
(bis dahin "statisch geprueft, nicht gespielt").

---------------------------------------------------------------------------------------------------------------------------------

## 4. Risiken und Clip-Runde

### 4.1 Risiken
| # | Risiko | Gegenmittel / Messung |
|---|---|---|
| R1 | Naht Metaball-Bein / Pfotenfeld (harte Vereinigung im Voxel-Remesh) gibt Absatz | Manschette mit gleichem Radius am Treffpunkt; Knick-Mass `pruef_netz.py` im Band z 0,12-0,25 |
| R2 | Duenneres Gelenk dehnt sich im Walk/Run staerker (Knick 69-110 / 55-105 Grad) | Formel-Band breit lassen, `gewichte` laufen lassen; Rueckfall: Gelenk 1-2 cm dicker (Toleranz der Tabellen) |
| R3 | Sitzen: Hinterfuss 1,2-1,9 cm ueber dem Boden (heute 0,16) | ohne Clip nicht zu schliessen; berichten, Clip-Runde C2 |
| R4 | Zehen/Krallen stecken im Walk/Run 1,3-3,0 cm im Boden (heute schon) | bleibt (Grenzkurve haelt es nicht schlechter); Clip-Runde C1 |
| R5 | Hinterfuss 1,15-1,2 x real, L/B ~2,0 | Folge der festen Knochen/Sitz-Pose (0.1 Nr. 2); kuerzer nur mit Clip C3 |
| R6 | Voxel 9,5 mm (0,71 cm Spiel) + Huelle fuellen Zehenrillen | Rillen >= 1,2 cm offen, Huelle auf Zehen <= 0,6 cm, Taubin 0,10; Mass 3.2 |
| R7 | `sohlen_bauen` nimmt nur die groesste flache Komponente | Abdruck eine Flaeche (1.1); Mass 3.2 |
| R8 | Geaendertes Metaball-Bein verschiebt das Voxelgitter des Rumpfs (ungeprueft, Bestand 6) | nur `:900/:901/:904/:905` aendern; Rumpf-Abstand z >= 0,36 (3.1) |
| R9 | K1 vorn | gemessen: kein Clip tiefer, Dead/Death/Swipe hoeher (`spez/k1_probe.txt`); Rueckfall K0 (dann Handballen 19-20 breit) |
| R10 | Gehobene Ballen (Ferse, Handwurzel) liegen nicht in der Sohlen-UV-Insel | 3D-Maske in `baer_textur_pfote.py` (2.2) |
| R11 | Form-Runden mit alten Fell-Ansichten | nur fuer die Form; Endlauf zwingend mit neuen Ansichten (Schritt 2) |
| R12 | Von vorn sind Hinterbein und -fuss fast gleich breit | Regel "Bein z 15 <= Fuss z 3 - 0,5", Zehenhoecker, Rist; Zelle "von vorn" in 3.4 |
| R13 | Andere Sitzungen auf der GPU, Spiel laeuft | `gpu_render.sh` wartet; sonst "Render offen" |

### 4.2 Nur mit Clip-Aenderung (Vorschlag fuer die Clip-Runde, NICHT in diesem Lauf)
- **C1 Gehen/Rennen: `Toe0` abrollen lassen** (Zehen biegen beim Abdruck hoch). Heute dreht Toe0 nie (Abweichung <= 3e-7,
  `bestand/spielraum2.txt`); Zehenhaut steckt im Walk bis 1,7 cm, Krallen bis 3,0 cm im Boden. Braucht danach Zehen-Gewichte an Toe0.
- **C2 Sitzen (Sit, Ende SitDown, Anfang StandUp): Unterschenkel ~2 cm tiefer** oder Fuss so drehen, dass die Ferse aufliegt (heute
  Gelenk im Sit 15,7 cm hoch, Ferse dann 1,2-1,9 cm Luft).
- **C3 (gross, nur auf Kevins Wort): Sprunggelenk im Sit 8-10 cm tiefer**; erst dann kann die Ferse auf echte 29-31 cm Fusslaenge
  zurueck (heute schwebte sie 12,5 cm).
- **C4 (Kosmetik)**: Fuesse im Gehen leicht einwaerts, Vorderpfote setzt mit der Aussenkante auf (Referenz 2, Q1/Q11).

---------------------------------------------------------------------------------------------------------------------------------

## 5. Dateien dieser Spez (`_arbeit/baer_pfote/`)
- `SPEZ_PFOTEN.md` (dieses), `spez_skizze.png` (MD5 9cab8818...), `spez/pfoten_plan.json` (Soll-Zahlen)
- `spez/heute_tiefst.py|.txt|.json` (Grundlinie je Clip/Pfote), `spez/grenzkurve.py|.txt|.json` (Clip-Grenzen 1.4),
  `spez/heute_kontur.py|.json` (Schnitte heute, Sohlenrand-Knick), `spez/krallen_lage.py|.txt`, `spez/k1_probe.py|.txt`,
  `spez/nachmessen.py|.txt` (Gewichte/Tiefe der heutigen Ferse), `spez/ferse_raster.py|.txt`, `spez/hand_raster.py|.txt`,
  `spez/grenzen_lr.py|.txt` (Raster L/R), `spez/spez_skizze.py`
- Alles aus dem Dump `bestand/dump_heute.txt` (Importer `Dump.java`, byte-gleich zu einem frischen Lauf laut Bestand) mit `bestand/lade.py`.
