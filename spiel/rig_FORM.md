# FORM -- Lauf baer-rig-junges, Rolle FORM (11.11.2026)

**Statisch geprueft, nicht gespielt.** Kein Skelett, keine Gewichte, keine Clips (das machen SKELETT und CLIPS). Nichts in Test-Mods,
NPC Crew, Spiel oder `_arbeit/baer_zaehmen/mod/` geschrieben; kein git, kein Download. Originale per MD5 vorher/nachher gleich
(`rig/form/eingang/md5*.txt`: form2.py, textur2.py, C_s01_wdh.glb, C_gen_eingang.png, aus/C_schoen*, NCBearTest NCBearCub.glb/.png).
Ablauf: erster Anlauf dieser Rolle 05:43-06:26 (F1 fertig, F2 Version 1 angefangen, dann abgebrochen); fortgesetzt ab 08:11.

## 0. Ergebnis kurz
- Abgabe (massgeblich): `rig/form/C_rig_basis.npz`; zum Ansehen `rig/form/C_rig_basis.glb` + `C_rig_basis.png`; `rig/form/landmarken_rig.json`,
  Messungen `rig/form/pruef_form.json`; Blatt `rig/bilder/form.png` (selbst angesehen).
- Das Generator-Junge steht jetzt in der **Ruhelage des Erwachsenen-Skeletts**: Kopf gerade (Gier 49 Grad weg, Rollen weg, Nicken wie im
  Foto), Rumpf gerade (C-Bogen weg), Unterarm 16,2 Grad vor, Unterschenkel 22,8 Grad zurueck, Spur symmetrisch, Koerper links = Spiegelbild
  von rechts (Symmetrie <= 0,17 cm in 181 Schnitten).
- Ohren: runde, dicke Baerenohren von allen Seiten, von hinten keine Pilze, von vorn ragen beide 12,5 cm (bei 1,0) ueber den Kopfumriss.
- Neues Spielnetz (19.418 Dreiecke, 11.811 GLB-Punkte, 0 Loecher), neue UV, **neue Textur 1024x1024 RGB** (frisch gemalt in Ruhelage).
- Urteil: siehe Abschnitt 6. Kurz: von allen Seiten ein sauberes Teddy-Baerenjunges; Rest-Maengel klein (Abschnitt 6.2).

## 1. F1 -- Fotopose (RIG_PLAN 2.1), erster Anlauf, unveraendert uebernommen
Parameter `rig/form/C_form_rig.json`, `C_tex_rig.json` (Abweichungen gegen `C_form_v17.json` / `C_tex_final.json`):
| Punkt | vorher -> nachher | Wirkung |
|---|---|---|
| Ohren Groesse | r_breit 0,05 -> 0,062, r_hoch 0,047 -> 0,06, dicke 0,034 -> 0,04 (+24..28 %, Plan sagte +12..18 %) | wie im Foto gross; in Spielgroesse 18 px breit |
| Ohren Basis | k 0,014 -> 0,04, heraus 0,006 -> -0,008 | Basis breit, kein Hals -> keine Pilze von hinten (`render/vgl_r3.png`, Ton 135/180/225) |
| Ohren Lage | kipp 30 -> 18 Grad, aussen 15 -> 22, seitlich 0,09 -> 0,12, neigung 10 -> 15, Mulde breiter/tiefer | ragen bei geradem Kopf von vorn ueber den Umriss |
| Kopf-Oberseite | neu `spiegel_ende` (form2_rig.py e3): Schaedeldecke hinter den Augen noch einmal gespiegelt | rechte Ohrbasis lag 0,6-2,6 cm tiefer -> Ohren gleich hoch |
| Ohr-Textur | ohr_fell_staerke 0,6 -> 0,3 nur in der Muschel, Rueckseite volles Fell, Saum nur vorn, Rueckseite x 0,85 | keine Holzmaserung innen, Rueckseite nicht heller als die Stirn |
| Stirn-Kratzer | `flecken_fuellen` Kopfrahmen (-0,07, 0,065, 0,14) | Kratzer am rechten Ohr weg |
| Sohlen | sohle_h 0,022 -> 0,032, sohle_breite 0,95, k_bein 0,025, boden_k 0,016, `glaetten_je_bein` (Knoechel/Sohle, aus E_form_v9) | Unterkante rund |
Ergebnis F1 `rig/form/f1/C_f1.glb` (19.528 Dreiecke). F1 ist nur noch Messgrundlage fuer F2 (Achsen, Kopfrahmen, Kopf-Gewichte).

## 2. F2 -- Ruhelage (RIG_PLAN 2.2), **anderer Weg als im Plan-Wortlaut**
Plan: "nur Punkte des F1-Netzes verschieben, UV und Textur bleiben". Erster Versuch so (`render/f2_t1.png`): Brust und Schulter falten,
weil VL im Schritt steht und VR 17 Grad schraeg nach innen. Darum **(Begruendung):** das **Rohmodell** (TRELLIS, 580.888 Punkte) wird
glatt verformt und die bewaehrte Kette `form2_rig.py` + `textur2_rig.py` laeuft in der Ruhelage neu -> Form, UV, Fell und Malerei frisch,
keine verzerrten Fellstriche.
- Version 1 (erster Anlauf): Beine im Abstandsfeld als Saeule ausgetauscht -> Stufen an Knie/Ellbogen, Fersen-Sporn (`render/ruhe_r1.png`).
  Verworfen.
- **Version 2 (Abgabe):** `werkzeug/bein_trafo.py` (numpy, von beiden Skripten benutzt) + `werkzeug/raw_ruhe2.py` (Blender, CPU 15 s):
  1. **Rumpf gerade:** seitliche Scherung dy(x) (Polynom Grad 3 durch die Rumpfmitte z 0,45-0,75 roh): C-Bogen 6,45 cm roh weg
     (vorn +3,2 cm, hinten -2,2 cm roh).
  2. **Kopf gerade:** Gier 49,1 Grad um einen Drehpunkt auf der Hals-Mittellinie, Rest (Rollen -3,4 Grad) um den Atlas; Gewichte harmonisch
     auf dem F1-Netz (Kopf starr, Rumpf fest), per 6 Nachbarn aufs Rohmodell. Nicken bleibt.
  3. **Beine glatt (VR, HR):** Drehung um Ellbogen/Knie mit Winkel-Mischung (keine lineare Matrizen-Mischung), Streckung entlang der
     Fotoachse, Pfote nur verschoben (nicht gekippt), Querverschiebung in einem breiteren Band; seitliche Maske (Abstand zur Fotoachse,
     Teilungslinie zur linken Partnerbein-Luecke). VR: 26,1 Grad (Unterarm -4 -> +16,2 Grad vor, Seitenneigung 17 Grad weg),
     Streckung 0,994, Hand 7,6 cm nach aussen. HR: 14,8 Grad (Unterschenkel -> 22,8 Grad zurueck), Streckung 1,074, 6,2 cm nach aussen.
     Riss im Netz: 0 (verschweisste Punkte bleiben zusammen).
  4. **Links = Spiegelbild von rechts** im Abstandsfeld (`form2_rig.py` e5, Naht 0,02); Pfoten neu gebaut (Abdruck links = gespiegelter
     Abdruck rechts, neu `fuss_spiegel`), Knoechel-Radius je Art (vorn 0,068, hinten 0,09 roh; Hinterlauf am Sprung vorn-hinten breiter ->
     keine Kante mehr, `render/pfote_r2..r4.png`), weichere Sohle (knoechel_k 0,05, sohle_breite 0,88, boden_k 0,02).
  5. **Farbquelle** `f2/raw_ruhe_tex.glb`: unter z 0,44 roh links = Spiegelbild von rechts (dort lag der Riss der Bein-Umstellung), oben
     links bleibt die Fotoseite. Helle Risse der Rohtextur (Generator-UV-Naehte) an 9 Stellen glatt gefuellt und neu befellt (gefunden mit
     `werkzeug/texel_flecken*.py` und `werkzeug/pixel_3d.py`, Nahbilder `render/flecken_probe.png` vorher, `flecken_probe_nach.png` nachher).
- Warum die Spur nicht wie im Foto: im Foto stehen die Vorderpfoten nach innen (VR 17 Grad schraeg). Das Skelett hat gerade Unterarme ->
  die Pfoten stehen jetzt unter den Ellbogen. Spur halb vorn 12,5 cm / hinten 14,7 cm bei 1,0 (RIG_PLAN erwartete 12,4 / 14,7).

## 3. Messungen (eigene, `rig/form/pruef_form.json`; tier-Meter bei Groesse 1,0; Spiel x 0,35)
| Mass | Wert | Grenze / Ziel |
|---|---|---|
| Dreiecke / GLB-Punkte / verschweisst | 19.418 / 11.811 / 9.711 | <= 20.000 (Importer zaehlt), < 65.536 |
| offene / nicht-mannigfaltige Kanten / entartete Dreiecke | 0 / 0 / 0 | 0 |
| Netze / Materialien / UV | 1 / 1 / 1 | 1 |
| Textur | 1024 x 1024, RGB 8 Bit, kein Alpha | wie verlangt |
| Augen-Nase-Linie | -42,0 Grad | -41 +- 3 (Foto) |
| Augenhoehe links/rechts, Augenmitte y, Nase y, Blick-Gier | 0,06 cm / 0,01 cm / -0,04 cm / -0,34 Grad | <= 0,3 cm, <= 0,5 cm |
| Symmetrie (Halbbreiten links/rechts, 181 exakte Schnitte z 0,3-0,8 m) | max 0,17 cm, p95 0,05 cm | <= 1,5 cm |
| Luecke linkes/rechtes Bein z 0,03-0,29 m | vorn >= 5,5 cm, hinten >= 5,1 cm | >= 4 cm |
| Luecke im Uebergang Achsel/Schritt z 0,31-0,35 m | vorn 5,3 -> 3,3 cm, hinten 3,9 -> 1,9 cm | **unter 4 cm** (Beine laufen dort in den Rumpf; Abschnitt 6.2) |
| Ohren von vorn ueber dem Kopfumriss | je 12,5 cm = 0,28 W; Spielgroesse 13,8 px hoch, 18,2/18,8 px breit | >= 0,10 W, >= 4 px, >= 15 px |
| Widerrist / Kruppe / Bauch tiefster Punkt | 1,176 / 1,078 / 0,418 m (bei 0,35: 41,2 / 37,7 / 14,6 cm) | RIG_PLAN 1,146 / 1,086 / 0,406 |
| Rumpf-Halbbreite max / Laenge Nase-Heck / Hoehe mit Ohren | 0,308 / 1,431 / 1,254 m | |
| tiefster Punkt | -0,03 cm | Boden 0 |
| Kopfbreite W (Wangen auf Augenhoehe) | 0,446 m | |
| Verzerrung der Hals-Umstellung im **Rohmodell** (sigma1/sigma2 je Rohdreieck im Halsband) | p50 1,27, p90 2,02, p99 4,0 | Plan p99 <= 1,35 -- **formal verfehlt**; Fell und Malerei werden auf dem Ruhenetz neu gezeichnet, nur die weichgezeichnete Grundfarbe kommt von dort; im Bild keine verschmierten Striche (Kopf rundum `render/kopf_tex_r2.png`, Blatt) |
| V_foto Abstand zum naechsten verformten Rohpunkt | Median 0,4 cm, p99 6 cm (neu gebaute Ohren/Pfoten) roh | |

## 4. Abgabe fuer SKELETT+GEWICHTE (Inhalt `C_rig_basis.npz`)
Rahmen **tier-Meter bei Groesse 1,0**: x vorn, y links, z oben, Boden z 0, y 0 = Mittelebene, **x 0 = Mitte zwischen Vorder- und
Hinterpfoten (vorlaeufig, SKELETT verschiebt)**; `ursprung_roh` (Lage dieses Ursprungs in roh), `skala_m_je_roh` 1,31, `y_mitte_roh` -0,05.
- `V` (9.711 x 3) verschweisste Punkte, `T` (19.418 x 3) Dreiecke in verschweissten Indizes, `T_glb` Dreiecke in GLB-Punkt-Indizes,
  `glb_punkt` (11.811) GLB-Punkt -> verschweisster Punkt, `UV` je GLB-Punkt **glTF-Konvention (v von oben) -- beim Export NICHT spiegeln**
  (Probe: `C_rig_basis.glb` mit genau diesen UV und `C_rig_basis.png` rendert richtig, Blatt Reihe 2).
- `V_foto`: Lage in der Fotopose nach Rumpf-Scherung (tier-Meter, gleicher Ursprung); linke Seite = Spiegelbild der rechten (wie die Form).
- Masken je Punkt: `kopf` (1.993; vor der Ebene Atlas-Kehle minus 3 cm, Ohren immer dabei), `ohr_l` 244, `ohr_r` 236, `hals` 319,
  `pfote_VR/VL/HR/HL` 473/473/504/498, `kralle` 334, `sohle` 344, `stummel` 53.
- `landmarken_rig.json`: Augen (0,676 / +-0,068 / 0,955), Nasenspitze (0,770 / 0 / 0,870), Ohrspitzen/-basen, Krone, Nacken ueber dem
  Atlas, Kinn, Kehle, Kopf-Grenz-Normale, **Atlas-Schaetzung (0,441 / 0 / 0,922), C7-Schaetzung (0,268 / 0 / 0,904)**, W, Widerrist,
  Kruppe, Bauch, Bug, Rumpfende, Stummel; je Bein: Achsenpunkte (exakte Schnitt-Mitten z 0,03-0,35 m), Ellbogen/Knie wie gedreht
  (vorn 0,283 / +-0,125 / 0,41, hinten -0,244 / +-0,147 / 0,41), Hand/Sprung (0,373 / -0,374, z 0,10), Pfoten-Mitte, Ferse, Ballen,
  Zehenspitze, Sohlenrand (x/y-Spanne). Vorderpfote 21,6 cm lang, Hinterpfote 28,1 cm (Ferse bis Zehe) bei 1,0.
- Hinweise: die Beinachsen des Netzes stehen bis auf die Pfote genau in Knochenrichtung (Drehung in Rohmodell-Koordinaten; SKELETT bitte
  mit eigener Achsmessung gegenpruefen). Der Kopf traegt sich hoch wie im Foto; der Hals ist kurz und dick (Kopf geht ohne Stufe in den
  Nacken, darum "Nacken ueber dem Atlas" statt "Hinterkopf").

## 5. Dateien
| Datei | Inhalt |
|---|---|
| `baer/spiel/baer_form_rig.py` | `plan` (Messung am F1-Netz, Umstell-Plan, Parameter fuer raw_ruhe2/form2_rig/textur2_rig) und `abgabe` (npz, glb, png, Landmarken, Messungen) |
| `rig/form/werkzeug/bein_trafo.py`, `raw_ruhe2.py` | glatte Bein-Umstellung; Rohmodell -> Ruhelage (+ Farbquelle, `raw_paare.npz`) |
| `rig/form/werkzeug/form2_rig.py`, `textur2_rig.py` | Kopien (Originale unveraendert); neu: L_fest, spiegel.normale_fest, e3 spiegel_ende, e4 (V1, unbenutzt), e5 koerper_spiegel, Pfoten radien/fuss_kreis/fuss_spiegel/r_max je Art; textur: hoch_glb, Ohr-Optionen |
| `rig/form/C_form_ruhe.json`, `C_tex_ruhe.json` | erzeugte Parameter der Ruhelage (aus `plan`) |
| `rig/form/f2/form_ruhe/` (dichte Form), `f2/C_ruhe.glb` (+ `_textur.png`, `_messung.json`, `einzel/`) | Kette in Ruhelage |
| `rig/form/werkzeug/rblick.py`, `cfg_ruhe.py`, `blatt_form.py`, `montage.py`, `texel_flecken*.py`, `pixel_3d.py`, `komp_probe.py`, `bein_probe.py`, `raw_dump.py` | Renders, Blatt, Proben |
| `rig/form/v1/` | Stand Version 1 und Zwischenstaende der Textur (tex_a/b/c) |
Wiederholen (unter `_arbeit/baer_gen/rig/form`, B = blender.exe, Pfade absolut):
`python baer_form_rig.py plan` -> `B -b --factory-startup --python werkzeug/raw_ruhe2.py -- f2/plan.json f2/plan.npz f2` ->
`B ... werkzeug/form2_rig.py -- C_form_ruhe.json` -> `sh ../../werkzeug/gpu_lauf.sh log/x.log B ... werkzeug/textur2_rig.py -- C_tex_ruhe.json`
-> `python baer_form_rig.py abgabe`.

## 6. Urteil (Bild-Fragen 6.5 soweit FORM; Blatt `rig/bilder/form.png`, selbst angesehen)
### 6.1 Ja
1. Ton ohne Textur von 8 Seiten: ein Baerenjunges, Beine glatt (keine Stufen mehr an Knie/Ellbogen), Rumpf rund, Heck rund. **Ja.**
2. Kopf gerade, Gesicht von vorn (Kevins Spielkamera 0/30 zeigt jetzt das Gesicht), Hals ohne Naht/Stufe in Ton und Textur. **Ja.**
3. Ohren von allen Seiten rund und dick, von hinten zwei runde Lappen ohne Hals (keine Pilze), von vorn beide ueber dem Umriss mit
   dunkler Muschel oben drauf -- kein dunkler Fleck im Kopfumriss mehr. **Ja.**
4. Pfoten von der Seite (el 0) rund, keine Platte, keine Kante am Sprung. **Ja** (Rest 6.2).
5. Textur: Fellstriche, dunkle Beine, helle Schnauze, schwarze Nase, braune Augen; Spielgroesse auf Grau/Gras ruhig. Farbe wie in C_FEIN
   geeicht (gleiche Kette; Belichtung 1,035 -> 1,0).
### 6.2 Rest (ehrlich)
- **Ruhelage sieht ungewohnt aus**: Vorderbeine 16 Grad nach vorn, Hinterbeine 23 Grad nach hinten (das ist die Ruhe des Erwachsenen-Skeletts;
  im Spiel stellt Idle01 die Beine, nicht diese Pose). Das Blatt zeigt deshalb einen "gestreckten" Stand.
- Von unten (el -10) ist die flache Sohle als Band sichtbar; von hinten wirkt die Pfote kastenfoermig. In Spielgroesse unsichtbar.
- Beinluecke im Achsel-/Schritt-Uebergang (z 0,31-0,35 m) nur 1,9-3,3 cm; dort sitzt Fell an Fell. Bei Trab/Galopp (SKELETT/CLIPS) die
  Leiste pruefen (C4).
- Hals-Umstellung im Rohmodell stark geschert (p99 4,0); wirkt nur auf die Grundfarbe, im Bild unauffaellig.
- Von hinten (180) wirkt das Junge schmal und hoch ("Ei auf Beinen", wie GEGEN_OPTIK) -- Form des Generators, nicht veraendert.
- Die linke untere Koerperhaelfte traegt die gespiegelte Farbe der rechten Seite (Fotoseite nur oben links).
- Platzhalter-Vergleich (R8) und Harness-Dump gehoeren zum fertigen, geriggten GLB (CLIPS); `C_rig_basis.glb` ist nur zum Ansehen
  (kein Skin) und wurde nicht durch Dump.java geschickt.

MD5 der Abgabe (`rig/form/md5_abgabe.txt`): C_rig_basis.npz 7a0ce03a..., C_rig_basis.glb 3740290b..., C_rig_basis.png 8ce68838...,
f2/C_ruhe.glb 66ed0f41..., f2/C_ruhe_textur.png 69609dc9... Letzte Nahbilder: `render/flecken_probe_nach.png`, `render/kopf_final.png`.

## 7. Fragen fuer Kevin
1. **Ohren** sind etwas groesser als im Foto-Vergleich vorgeschlagen (+24..28 % statt +12..18 %), damit sie aus deiner Kamera von vorn klar
   ueber dem Kopf stehen. So lassen?
2. **Spur:** im Foto stehen die Vorderpfoten nach innen; das Junge steht jetzt mit geraden Unterarmen (Pfoten unter den Schultern). So lassen?
3. Aus RIG_PLAN 8.2 weiter offen: Laenge (kompakt, L/H 1,2), Maul (bleibt zu), Kopfhaltung hoch, kuerzere Hinterpfoten (hier 28 cm bei 1,0).
