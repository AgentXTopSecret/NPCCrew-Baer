# Baer-Anim: Pruefung Optik gegen die Referenz (Lauf baer-anim, Pruefer "Optik")

Stand 08.11.2026. Geprueft: `_arbeit/baer_anim/mod/42/media/models_X/Skinned/NCBear.glb` (MD5 `f06d9ec1...`) gegen
`NCBearTest/.../NCBear.glb` (MD5 `2e9a6d17...`, heute gespielt), `anim_referenz.md`, `anim_spez.md`, `anim_clips.md`,
`anim_modell.md`, `kevin_sitzvorlage.png`. **Nur gelesen, gerechnet und gerendert, nichts gespielt, nichts am Stand geaendert.**

Werkzeuge (alle unter `_arbeit/baer_anim/pruef/`): eigener GLB-Leser ohne Blender und ohne Probe.java (`glb.py`, `ana.py`:
Knoten, Clips, Haeutung in numpy), Gelenk- und Hautmessung je Bild (`run1.py`, `geo.py`, `roll.py`, `str.py`, `slide.py`),
Durchdringung ueber die Windungszahl des geschlossenen Netzes (`wind2.py`, Punkte 1,5 mm nach aussen versetzt, Punkte, die
schon in Ruhe innen liegen wie Krallen und Mundsack, abgezogen), Renders mit Cycles auf der RTX 4090 (OptiX + OptiX-Entrauscher,
vor jedem Render `tasklist` geprueft: das Spiel lief nie), Bildblaetter `s*.png`. Massangaben in Modellmetern (GLB-Einheit
E = 0,544 m Modell; Kacheln wie im Bericht = E x 1,5).

---

## Funde

1. **ernst -- NCBear_SwipeL/SwipeR: Bild 17-21 (0,57-0,70 s), also genau im Treffer -- die schlagende Pranke faehrt durch den
   eigenen Unterkiefer.**
   Beleg: Pfotenmitte bei 0,60 s (1,09 vor, -0,04 seitlich, 0,51 hoch), Schnauzenspitze (1,13 / -0,27 / 0,56); kleinster
   Abstand Pfote-Kopf 0,2-0,3 cm in Bild 18-20. Windungszahl: 94 / 181 / 212 Pfoten- und Unterarmpunkte liegen in Bild 18 / 19 / 20
   im Kopf, umgekehrt 105 / 208 / 278 Kopfpunkte im Arm (Gang: 0). Bilder `s4_swl.png` (Kopf rot, Arm blau: blau schneidet rot),
   `s5_tex.png` (Spielwinkel Bild 19: Pranke vor/im Maul), `s_spike.png`. Ursache: der Treffpunkt aus `anim_spez.md` 7
   (0,945 Kacheln vor, 0,03 innen, 0,52 m) liegt auf der Mittellinie genau dort, wo der eigene Kopf ist; der Kopf giert nur
   -14 Grad weg. SwipeR ist exakt gespiegelt (Abweichung der Gelenkorte 0,0003 cm), hat also denselben Fehler.
   Vorschlag: Treffpunkt 0,15-0,25 m nach aussen auf die Schlagseite legen (vor die Schulter, nicht vor die Schnauze), oder Pranke
   unter dem Kinn durchziehen (Hoehe <= 0,30 m ab 0,57 s) und Kopf in 0,50-0,70 s staerker wegdrehen (gieren -25..-30, 6-8 cm
   zurueck); danach Windungszahl Pfote/Kopf je Bild = 0 als feste Pruefung in den Bau.

2. **ernst -- NCBear_Sit (und Ende SitDown / Anfang StandUp): sieht nicht wie Kevins Vorlage aus, und die Beine stecken
   ineinander.**
   Beleg: (a) Rumpflinie Becken->Hals 56 Grad gegen die Senkrechte (Vorlage: senkrecht), Kopf weit vorn-oben (Kopf 0,59 vor, 0,98
   hoch; Hals 0,41 / 0,86) -> von der Seite ein geduckter Buckel mit vorgestrecktem Hals, von vorn ein runder Klumpen
   (`s3_sit.png`, `s1_misc.png`, `anim_sitzen_vergleich.png`). (b) Die Hinterbeine liegen nicht vorn: Ferse 0,10 vor, Zehen 0,27 vor,
   seitlich 0,30-0,34 -- also NEBEN den Vorderpfoten (0,20 vor, +-0,11), nicht davor; die Sohle zeigt zu 82 % nach innen (Normale
   links: -0,82 / -0,06 / +0,56), nicht nach vorn-oben. (c) Durchdringung, dauerhaft in der ganzen Schleife: 406 Punkte der linken
   Hinterpfote liegen im linken Vorderbein, 420 rechts; 88-101 Punkte je Vorderpfote in der anderen Vorderpfote (Pfotenmitten nur
   22 cm auseinander, Spez wollte +-0,12..0,15); 113-121 je Vorderpfote im Hinterbein (`wind_out.txt`; Lauf zum Vergleich nur
   kurz und nur im Sammelbild). Bilder `s4_sit.png` (lila Hinterpfote verschmilzt mit gruenem Vorderbein, gruen und blau ohne
   Spalt). Die Begruendung im Bericht (aufrechter Rumpf und flache Pfoten am Boden gehen mit diesen Proportionen nicht zusammen)
   haelt nach den Gelenkorten: Schulter 0,72 m bei 34 Grad Rumpf, senkrecht waere sie rund 1,0 m, der Arm reicht 0,73 m.
   **(b) und (c) haengen davon aber nicht ab.**
   Vorschlag: Kevin sofort Wahl (b) aus `anim_clips.md` 7 anbieten (aufrecht, Pranken im Schoss bzw. auf den Hinterpfoten), denn nur
   die trifft den Umriss der Vorlage; unabhaengig davon Hinterbeine wirklich nach vorn (Fersen 0,55-0,70 vor der Hueftlinie, Sohle
   nach vorn-oben wie Spez), Vorderpfoten auf +-0,15 m, und Windungszahl zwischen den Gliedmassen = 0 pruefen.

3. **ernst -- NCBear_SitDown Bild 28-32 (0,93-1,07 s) und NCBear_StandUp Bild 0-4 (0,00-0,13 s): die Hinterpfoten klappen
   seitlich um, und im Sitzen sind sie 61 Grad verdreht.**
   Beleg: Rollen der Sohle aus der Beinebene (Drehung der Pfote um ihre eigene Laengsachse, Inversion/Eversion): Sitzen dauerhaft
   61,4 Grad; SitDown -8 -> -22 -> -60 Grad in 0,13 s, StandUp -61 -> -25 -> -8 Grad. Drehung Unterschenkel->Fuss je Bild:
   SitDown 26 Grad, StandUp 36 Grad (Gang 8, Lauf 18,5). Abgenommene Clips: Idle <= 2, Gang <= 6, Lauf <= 4 Grad Rollen
   (`roll.py`). **Messluecke:** `gelenke_messen*.py` erfasst dieses Rollen nicht (Hinterfuss "Drehung" = um die Unterschenkelachse,
   "aus der Ebene" = Richtung der Pfote); deshalb meldet der Bericht "0 Befunde".
   Vorschlag: neue Grenze "Sohle aus der Beinebene" hinten etwa +-20 Grad und Sprung <= 20 Grad je Bild in `GRENZEN` aufnehmen; die
   Sohlenrichtung im Sitzen ueber Hueftdrehung/Spreizung statt ueber das Sprunggelenk herstellen.

4. **ernst -- NCBear_Slam Bild 20-30 (0,67-1,00 s): Pranken neben bzw. vor dem Gesicht, Unterarme im Kopf.**
   Beleg: Pfotenmitte 0,82-0,90 vor, 0,34-0,37 seitlich, 1,01-1,14 hoch; Schnauze 0,93-1,00 vor, 1,07-1,20 hoch: die Pranken
   stehen auf Augen-/Ohrenhoehe seitlich vom Kopf. Windungszahl: bis 43 Unterarmpunkte im Kopf und 67 Kopfpunkte in den Armen
   (Bild 26). Von vorn wirkt das wie "Haende hoch" bzw. Ohren zuhalten, von der Seite liegt der rechte Unterarm vor der offenen
   Schnauze (`s1_misc.png` Slam 28 vorn, `s5_tex.png` Slam 27 Seite, `s4_maul.png` untere Reihe). Referenz 7 B wollte
   "Vorderbeine locker vorn-oben", Oberarm vor +20..+40; gebaut ist vor 22-24 bei Brust -42, Hals und Kopf gehen in denselben Raum.
   Vorschlag: Oberarm vor auf +35..+40 und Pranken 15-20 cm vor die Schnauze (oder Kopf in der Hochphase 8-10 cm tiefer/zurueck),
   Windungszahl Arm/Kopf = 0.

5. **ernst -- SwipeL/R, Slam, Bite: der Rest des Koerpers arbeitet kaum mehr als im heutigen (verworfenen) Clip; die Hinterbeine
   schieben nie.**
   Beleg (`gelenke_heute.txt` gegen `gelenke18.txt`): Hieb Becken gieren -6..+5 (alt -6..+3), Brust gieren -18..+12 (alt
   -18..+8; Referenz 5 wollte 35 Grad), Becken-Versatz seitlich 13 cm (alt 9); Hinterknie Hieb 117..134, Slam 119..134 (alt
   109..134), Biss 124..134. Ruhewinkel ist 133,7 -- das Knie wird also in keinem Angriff gestreckt; Referenz 5 C/D wollte
   140-145 (Schub), 7 C 110 -> 145, Biss 125 -> 150. Hinterpfoten 0 m Weg. Slam: Becken- und Brustnicken gleich dem alten Clip
   (-22..6 / -42..17). Kevins Satz "bewegt den restlichen Koerper halt null" bleibt damit fuer Becken und Hinterbeine bestehen;
   neu ist vor allem die Armbahn (`s_swl_vorn.png`: Brust rollt sichtbar, Becken kaum).
   Vorschlag: Knie in der Schlagphase auf 140-145 strecken (Schub) und Becken-Gieren auf rund 40 % der Brust (14 Grad) wie
   Referenz 5; beim Slam Knie vor dem Aufrichten auf 110 laden und im Niederschlag auf 145 strecken.

6. **ernst -- SwipeL/R Bild 12-21, Slam Bild 22-34, Rear oben: Haut an Achsel/Rippenbogen und Unterarm gedehnt, im Treffer ein
   flacher "Flossen"-Unterarm mit Zipfel am Ellbogen.**
   Beleg (alle Kanten, `str.py`): Kanten ueber 3-fach je Bild: Hieb 116, Slam 207, Biss 88, Rear 100 (Gang 9, Lauf 38); Kanten
   ueber 4-fach im Clip: Hieb 41, Slam 49 (Lauf 6). Orte: `Spine`/`Spine1` (Rippen hinter der Achsel) und `L_Forearm`. Im Bild:
   Unterarm wird bei 0,57-0,73 s zu einer flachen Klinge mit spitzem Zipfel am Ellbogen (`s2_swl_vornL.png` Bild 17-21,
   `s_spike.png` rechts), dunkle Faltlinie Achsel-Brust beim Ausholen (`s5_tex.png` Bild 12), beim Aufrichten ein harter
   "Kragen" ueber den Oberarmen (`s3_rear.png`). Der Bauer hat das Ziel 3-fach selbst als verfehlt gemeldet; bestaetigt.
   Vorschlag: wie Bericht 6 -- Korrekturknochen bzw. Achselfalte im Netz (Lauf baer-fell), oder Armhub weiter zuruecknehmen;
   bis dahin Kevin den Zipfel zeigen, nicht verschweigen.

7. **klein -- NCBear_Maul Bild 20 (0,67 s): Kopf drueckt in die haltende linke Pranke.** 73 Pfotenpunkte im Kopf, nur dieses
   eine Schuettelbild (Bild 16 und 24: 0-3). Vorschlag: Schuetteln dort 3-4 cm weiter nach rechts oder Pranke 5 cm nach aussen.

8. **klein -- NCBear_Bite Bild 9-17: die Vorderpfoten schnellen in 3 Bildern auf 53 cm Hoehe (bis 35 cm je Bild, rund 10 m/s
   Modell), stehen 4 Bilder still und schlagen in 2 Bildern zurueck.** Aenderung der Bildgeschwindigkeit bis 24 cm (Lauf 7,8).
   Wirkt wie Arme-Hochreissen mit Krallen nach oben ("Superman"), Referenz 6 wollte einen kurzen Satz (0,15 m vor). Vorschlag:
   Hubhoehe 20-30 cm, weichere Ein- und Ausfahrt.

9. **klein -- NCBear_SwipeL/R Bild 15-27 (0,50-0,90 s): Stuetzpfote dreht auf dem Boden; Kontaktpunkte wandern bis 4,2 cm.**
   Der Bericht nennt je Bild <= 0,0096 Kacheln -- aufsummiert ueber den Stand sind es 4,2 cm (Pfote dreht 7 Grad, Haelfte der
   Sohle hebt). Im Spielwinkel kaum sichtbar.

10. **klein -- NCBear_Sit: Hinterpfoten schweben 6-9 mm ueber dem Boden** (tiefster Punkt der Pfote, ganze Schleife); Bericht 7
    sagt "Ferse am Boden".

11. **klein -- alte Clips mit neuem Netz:** Bewegung bit-gleich (siehe unten), aber die Haut an der Pranke dehnt sich mehr:
    groesste Kante Gang 3,72 -> 4,82, Lauf 4,18 -> 5,57 (Handgelenk, kurze Kanten 0,6-2,4 cm); Death tiefster Punkt -14,7 ->
    -18,1 mm. Abgenommene Clips also optisch nicht ganz wie heute; im Spiel vermutlich nicht zu sehen, Kevin beim naechsten
    Test auf die Pranke im Gang schauen lassen.

12. **klein -- SwipeL/R Bild 8-14 (0,27-0,47 s): von vorn liest sich das Ausholen wie Winken** (Unterarm senkrecht neben dem
    Kopf, Handflaeche zum Betrachter, `s2_swl_key.png` obere Reihe). Geschmacksfrage, nur Kevins Blick entscheidet.

13. **klein -- `anim_clips.md` 1: "tiefster Hautpunkt hoechstens 2,1 mm drunter"** -- das ist der Wert in E (-0,0021 E), in
    Modellmetern sind es 3,9 mm (eigene Messung SwipeL -3,8 mm, Maul -3,8 mm). Harmlos, aber Einheit nennen.

## Geprueft und in Ordnung

- **Kopf unveraendert:** alle 1.293 Punkte mit Kopf-/Kiefergewicht > 0,99 bit-gleich in Lage und UV, 2.048 Kopfflaechen alt wie
  neu; nur 67 Punkte am Nahtrand (Kopfgewicht 0,51-0,96) verschoben, hoechstens 6,9 mm, Gewichte dort bis 0,012 anders.
- **Idle, Walk, Run, Death, Dead:** alle Abtastzeiten, Werte, Interpolationsarten und alle 78 Kanaele je Clip bit-gleich
  (Abweichung 0), Ruheknoten und Inverse-Bind-Matrizen gleich (eigener Leser, nicht Probe.java).
- **Rumpf und Beine runder:** eigener Render aus beiden GLB (`s6_altneu.png`) zeigt dasselbe wie `anim_modell_vergleich.png`:
  Beulen weg, Umriss rund, Kopf gleich.
- **Kein Gelenk knickt gegen seine Richtung (vorn, Knie, Schulter):** Ellbogen ist in allen Clips ein reines Scharnier
  (Abweichung von der Scharnierachse 0,0 Grad, nie umgeklappt), 84,6..172,8 innen; Vorderpfote Drehung -28..+28, aus der Ebene
  <= 10,8 (geometrisch nachgemessen, gleich `gelenke18.txt`); Oberarmdrehung im Rahmen; Knie nie umgeklappt. Der alte Knick
  (-139/-168 Grad, Ellbogen 27-36) ist weg. Ausnahme: Hinterfuss-Rollen, Fund 3.
- **Naehte und Schleifen:** SitDown-Ende = Sit = StandUp-Anfang (0,0 cm), Sit und Eat schliessen (0,0 cm), alle Kampfclips beginnen
  und enden 0,3 cm am Mittel von Idle01.
- **Boden:** neue Clips hoechstens 3,8 mm unter null (Gang heute 24 mm).
- **Aufrichten:** Arme haengen vor der Brust (Ellbogen 102-108), Kopf hoch mit offenem Maul, Knie 124-163, keine Durchdringung von
  Arm/Kopf; 3,0 s.
- **Fressen:** Kopf am Boden vor den Pfoten, Kauen sichtbar, keine Durchdringung ueber den Ruhezustand hinaus.
- **SwipeR** ist exakt das Spiegelbild von SwipeL.

## Urteil

Der alte Armknick ist wirklich weg, Kopf und alte Clips sind unveraendert und der Rumpf ist rund. **Aber so nicht Kevin zeigen
ohne Nacharbeit:** beim Hieb faehrt die Pranke im Treffer durch den eigenen Kiefer, beim Doppelschlag stehen die Pranken neben
dem Gesicht, die Hinterbeine schieben in keinem Angriff, und das Sitzen ist weder Kevins Vorlage noch sauber (Beine stecken
ineinander, Hinterpfoten klappen um).

Hinweis zum Vorgehen: Der erste Render-Lauf schrieb wegen eines relativen Pfads 594 Bilder nach `C:\r1`; sofort nach
`_arbeit/baer_anim/pruef/r1` verschoben, `C:\r1` existiert nicht mehr.

Statisch geprueft und offline gemessen, nicht gespielt.
