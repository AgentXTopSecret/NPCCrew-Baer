# Baer schlaeft: Referenz echter Baeren, Schlafhaltung, Clip-Liste, Bettmass (Lauf baer-schlaf, Forscher "Referenz")

Stand 09.11.2026. **Nur gelesen, im Netz gesucht (Seiten gelesen, nichts heruntergeladen) und offline gemessen (Blender im
Hintergrund, nur CPU, kein Render, keine GPU). Nichts gebaut, keine Mod-Datei geaendert, nichts gespielt.** Der parallele Lauf
baer-fell (`_arbeit/baer_fell`) wurde nur gelesen (Netz-FBX und `gewichte_fell.npz` als Eingang der Messung).

Eigene Dateien: `_arbeit/baer_schlaf/referenz/` -- `schlaf_probe.py` + `probe.log` + `umriss.json` (Messung 1),
`schlaf_probe2.py` (= Kopf von `schlaf_probe.py` + `schlaf_probe2_teil.py`) + `probe2.log` + `umriss2.json` (Messung 2),
`umriss2_*_haut.npy` (Hautpunkte der gemessenen Posen).

Schreibweise: `Datei:Zeile`; Masse in Modellmetern (Modell bei Groesse 1,0; ein Mensch MaleBody = 1,8 m), "bei 1,35" = mal 1,35
(Erwachsener). Kacheln = Meter x 0,544 x 1,5 = Meter x 0,816 (0,544 E je Meter, 1,5 Kacheln je E: `baer/spiel/bau_lebend.md:48`).

---

## 0. Ergebnis in zehn Saetzen

1. Echte Braunbaeren schlafen in **Seitenlage** (im Zoo der groesste Teil des Schlafs, verbunden mit REM-Schlaf, Quelle 2), auf dem
   **Bauch** (auch mit nach hinten gestreckten Hinterbeinen, Schnauze am Boden), auf dem **Ruecken** und **eingerollt** (im Winterlager,
   Quellen 1, 7, 8). Eisbaeren nehmen die Pranke als Kissen (Quelle 4).
2. **Vorschlag Haupt-Schlafhaltung: "Sphinx" -- Bauchlage, Ellbogen unter der Schulter, Unterarme flach nach vorn, Kinn zwischen bzw.
   Wange auf den Pranken, Hinterbeine untergeschlagen**, Kopf in der Schleife leicht zur Seite. Knuffig (Teddy-Form wie Kevins
   Sitzvorlage), aus der Iso-Kamera klar lesbar (Ruecken, Kopf, beide Pranken nach vorn, Platz fuer z Z z ueber dem Kopf).
3. **Nicht die Seitenlage als Hauptpose:** unsere Tot-Pose `DeerStag_Dead` liegt schon auf der rechten Flanke mit gestreckten Beinen
   (`baer_kampf_fell.py:470-492`); ein schlafender Baer in Seitenlage sieht von oben aus wie ein toter.
4. Hoechstens eine zweite Haltung: **halb eingerollt auf der Seite** (Nase zum Bauch, Beine angezogen) als "Tiefschlaf", spaeter und nur
   auf Kevins Wort -- die grobe Probe zeigt, dass die Beine viel Arbeit brauchen (22 Klemmungen).
5. Clips: **NCBear_LieDown 2,4 s**, **NCBear_Sleep 12,0 s Schleife** (zwei Atemzuege, ~10 je Minute), **NCBear_WakeUp 2,2 s**;
   optional **NCBear_WakeAlarm 1,1 s** (Kampf hat Vorrang) -- Muster wie SitDown/Sit/StandUp, neue Grundpose `POSE_L` wie `POSE_S`.
6. Die Sphinx ist mit unserem Skelett und den festen Gelenkgrenzen **erreichbar** (gemessen: Vorderbein ohne Klemmung, Ellbogen 107,
   Schulter vor 30; Hinterbein Knie 65, Huefte vor 78). Offen fuer den Animator: Ellbogenunterseite 5 cm und Hinterfuss 4 cm im Boden.
7. Gebaut wird in der juengsten Clip-Quelle (heute `baer/spiel/baer_kampf_fell.py`, erst nach dem Ende von baer-fell anfassen), mit
   allen Regeln von baer-anim (Grenzen, Klemmen, Bericht je Clip, Kritiker Bild fuer Bild, nichts im Boden, `liege_alt.json` nur fuer
   Death/Dead). Danach `baer_gewichte_fell.py` neu (Gewichte sind gegen genau 15 Clips optimiert, `bau_netz.md:162`), Dehnung und
   **Falten liegend** messen (heute schon die Schwachstelle: 154 statt Ziel 120, `bau_netz.md:164`).
8. **Umriss Sphinx beim Erwachsenen (1,35): 2,57 x 1,50 m (2,10 x 1,23 Kacheln)**, Seitenlage (= Dead) 2,54 x 1,45 m, Stehen
   2,63 x 1,30 m (Gegenprobe gegen `anim_modell.md` 3 stimmt). Gemessen an der Haut, nicht geschaetzt.
9. **Bett-Empfehlung: flach. Liegeflaeche 4 cm hoch (hoechstens 5 cm), Innenmass mindestens 2,8 x 1,65 m (2,3 x 1,35 Kacheln)**,
   Rand nur ausserhalb des Umrisses und niedrig. Zwei Kacheln Laenge reichen NICHT (gebraucht 2,10 Kacheln).
10. Statisch und offline gemessen, nicht gespielt. Alle Verhaltens-Fragen (wann schlafen, Laerm weckt, MP) gehoeren anderen Forschern.

---

## 1. Wie echte Braunbaeren schlafen (Quellen in Abschnitt 8)

| Thema | Befund | Quelle |
|---|---|---|
| Haltungen (Freiland) | Mutter und Junges lagen beim Ruhen in vielen Lagen: auf der Seite, auf dem Bauch mit nach hinten gestreckten Hinterbeinen, auf dem Ruecken; eine Mutter lag auf dem Bauch mit der Schnauze am Boden; das Junge lehnte mit dem Ruecken an der Mutter, ein Fruehjahrsjunges lag zwischen ihren Pranken | 1 (Murie, Denali) |
| Haltung im Tiefschlaf | Ein Zoo-Braunbaer verbrachte den groessten Teil seines Schlafs in Seitenlage (von den Autoren mit REM-Schlaf verbunden); Anteil 36 % -> 15 % nach dem Tod der Schwester, dafuer mehr Stehen | 2 (Mattiello et al. 2014) |
| Kopf ablegen | Eisbaeren nehmen ihre Pranke, Eis oder einen Stein als Kissen | 4 (Polar Bears International) |
| Bett graben | Eisbaeren graben auf weichem Grund flache Liegemulden ("day beds"), gemessen rund **1,5 m** quer und bis 0,5 m tief | 4 |
| Bett-Material | Schwarzbaeren liegen im Sommer direkt auf kuehlem, feuchtem, moosigem Boden; zum Polstern beissen sie Nadelzweige ab oder schaelen Zedernrinde | 5 (North American Bear Center) |
| Winterlager | Braunbaeren verbringen 4-6 Monate eingerollt im Lager; die Kammer ist gerade gross genug zum Einrollen | 7 (San Diego Zoo), 8 (Kodiak) |
| Bettenstudie | 119 Sommerbetten europaeischer Braunbaeren in Norwegen (Typ und Groesse gemessen) -- **Masse nicht gelesen** (nur die Kurzfassung erreichbar) | 6 (Mysterud 1983) |
| Wann, wie lange | Skandinavische Braunbaeren: aktiv frueh morgens und nachmittags, ruhen mittags und nachts; rund 12 h Ruhe am Tag, davon ~9 h tagsueber und ~3 h nachts (**nur Suchauszug**, Ordiz et al. 2011 nach Moe et al. 2007, Volltext nicht gelesen). Eisbaeren: lange Schlafphasen 7-8 h, Nickerchen 1-2 h, oft nach dem Fressen | 9, 10, 4 |
| Aufwachen / Aufstehen | Morgens blieb eine Mutter rund 15 min still liegen, hob mehrmals kurz den Kopf zum Schauen, stand dann auf, ging ein paar Schritte und schaute sich um | 1 |
| Hinlegen | **Keine baerenspezifische Beschreibung gefunden** (zwei Suchen). Die Phasen in Abschnitt 3 sind aus Mechanik und unseren Clips abgeleitet -- ungeprueft | - |
| Atmung wach in Ruhe | 6-10 Atemzuege je Minute, Herz 40-50 je Minute (NPS Yellowstone; **nur Suchauszug**, die archivierte Seite kam leer zurueck). Herz im Sommer 40-50 auch bei Yellowstone Forever (gelesen) | 11, 12 |
| Atmung im Winterlager | rund 4 je Minute eingerollt im Lager (Kodiak, gelesen); im tiefen Winterschlaf rund 1 je Minute bzw. alle 45 s, Herz 8-10 bzw. 8-12 | 8, 13, 12 |
| Atmung im Sommerschlaf | **keine Messung gefunden**. Vorschlag: 8-10 je Minute (zwischen Ruhe wach und Winterlager), im Spiel gut sichtbar | - |
| Schnarchen | nicht gesucht (Thema des Ton-Forschers) | - |

Was man daraus fuer das Spiel nimmt:
- Bauchlage mit Kopf am Boden/auf der Pranke ist echt (1, 4) und die Haltung, die von oben am "suessesten" wirkt.
- Seitenlage ist die echte Tiefschlaf-Haltung (2), kollidiert aber im Bild mit unserer Tot-Pose (Abschnitt 2).
- Ein kurzes "Bett zurechtscharren" vor dem Hinlegen ist echt (4, 5) -- als optionaler Clip denkbar, Kevins Wort.
- Aufwachen: erst Kopf hoch und schauen, dann aufstehen (1) -- genau so ist `NCBear_WakeUp` unten gebaut.

## 2. Haltungen fuer unseren Baeren

Kevins Geschmack: "knuffig/suess", runde Teddy-Form, sichtbare Ballen (`begleiter/kevin_sitzvorlage.png`, nur angesehen;
`begleiter/ENTSCHEIDUNGEN.md` Abschnitt Sitz-Animation). Die Spielkamera schaut schraeg von oben.

| Haltung | echt? | von oben lesbar | knuffig | mit unserem Skelett (gemessen, Abschnitt 6) | Urteil |
|---|---|---|---|---|---|
| **Sphinx: Bauchlage, Kinn zwischen / Wange auf den Pranken, Hinterbeine untergeschlagen** | ja (1, 4) | sehr gut: Ruecken, Kopf vorn, beide Pranken; z Z z ueber dem Kopf frei | ja (Hund/Teddy "Kopf auf den Pfoten") | Vorderbein ohne Klemmung, Hinterbein in den Grenzen (Fuss geklemmt), Rumpf 0 Klemmungen | **Haupthaltung** |
| Seitenlage gestreckt | ja, Tiefschlaf (2) | Flanke und Beine | mittel | geht (= `DeerStag_Dead`) | **nein: sieht aus wie tot** (`baer_kampf_fell.py:470-492`, LIEGE "auf die rechte Flanke gerollt") |
| Halb eingerollt auf der Seite (Nase zum Bauch, Beine angezogen) | ja, eingerollt im Lager (7, 8) | mittel (Knaeuel, Kopf seitlich) | ja | Rumpfbeugung geht (Lende 12, Brust 10, Hals 35, Kopf 25 Grad gegen die Eltern), **Beine in der groben Probe falsch** (22 Klemmungen, Pranke 0,5 m in der Luft) | hoechstens zweite, spaeter |
| Froschlage (Bauch, Hinterbeine flach nach hinten, Sohlen oben) | ja (1) | gut, Sohlen sichtbar | sehr | **nicht in den Grenzen**: Huefte vor -60 und Sprunggelenk dors -45 (`baer_kampf_fell.py:562-565`) halten die Fuesse 31 cm im Boden (`umriss.json`) | nur mit gelockerten Grenzen (Kevins Wort, Begruendung Hund Quelle 4 in `anim_referenz.md`: Huefte bis 180, Tarsus bis 188 Grad) |
| Rueckenlage | ja (1) | Bauch nach oben | sehr | ungemessen; Bauchseite ist gerade erst in baer-fell in Arbeit | nein: "Beine in die Luft" liest sich ebenfalls wie tot |

**Empfehlung:** Sphinx als Haupthaltung; in der Schlafschleife den Kopf langsam etwa 20-25 Grad zur Seite sinken lassen (Wange auf der
linken Pranke) -- das wirkt am knuffigsten und ist gemessen (Abschnitt 6, "Kopf 25 Grad zur Seite": keine Rumpfklemmung). Zweite
Haltung (halb eingerollt) nur, wenn Kevin nach dem ersten Test mehr will; sie wuerde ueber die Sphinx erreicht (Sphinx -> Einrollen ->
Schlafen eingerollt -> Ausrollen -> Sphinx), damit es nur EINEN Aufwach-Clip gibt.

Startwerte der Sphinx aus der Messung (Spuren-Schreibweise von `baer_kampf_fell.py`, Tier-Rahmen x vorn, y links, z oben; **Probe,
kein fertiger Clip**):

| Spur | Wert | gemessen |
|---|---|---|
| `pel` | (0, 0, -0,31) | tiefster Rumpfpunkt +6 mm (Becken-Gelenk 0,41 m hoch) |
| `r_pel / r_sp / r_ch` | (0,0,0) / (0,1,0) / (0,2,0) | Rumpf flach am Boden |
| `r_ne / r_he` | (0, 20, 0) / (0, 10, 0); Seitenvariante gier 10 / 25 | Kinn 7,7 cm hoch, Pfotenoberkante 15,9 cm: das Kinn liegt zwischen den Pranken |
| `ball_V`, `rot_V`, `pole_V` | (0,86, +-0,17, 0,045), (-5 s, 0, 0), (-0,4, 0,15 s, -1) | Schulter vor 30,2, abd -0,2, Ellbogen 106,9, dors -18,6, sup -0,7: **keine Klemmung**; Ellbogenunterseite 5,2 cm im Boden |
| `ball_H`, `rot_H`, `pole_H` | (-0,06, +-0,40, 0,045), (15 s, 0, 0), (0,7, 0,6 s, 0,5) | Huefte vor 77,8 (Grenze 80), abd 26,7, Knie 65,1, Fuss dors -92,7; Fuss geklemmt ("pfote", "schwenk"), Fuss 3,9 cm im Boden |

## 3. Clip-Liste (Vorschlag)

Muster: genau wie Hinsetzen/Sitzen/Aufstehen (`baer_kampf_fell.py:1247-1400`, Liste `KAMPF_CLIPS` 1422-1433, `SCHLEIFE` 1464):
eine Grundpose `POSE_L` (wie `POSE_S` 1275), Hinlegen endet in L, Schlafen beginnt und endet in L, Aufwachen beginnt in L und endet in
der Grundhaltung (Mittel von `DeerStag_Idle01`). 30 Bilder/s, alle 26 Knochen mit Schluesseln, `Translation_Data` 0, Bip01 still.

| Clip | Dauer | Bilder | Schleife | Anfang -> Ende | Ablauf |
|---|---|---|---|---|---|
| **NCBear_LieDown** | 2,4 s | 72 | nein | Grund -> L | A 0-0,5: Kopf senkt sich, Gewicht nach hinten, Hinterknie beugen (wie SitDown 0-0,30). B 0,4-1,2: Hinterteil sinkt, jede Hinterpfote einen halben Schritt nach aussen-vorn (L 0,40-0,70, R 0,60-0,90), Knie nach aussen. C 1,0-1,8: Vorderpfoten nacheinander einen Schritt vor (L 1,00-1,30, R 1,20-1,50), Ellbogen knicken unter die Schulter, Brust kommt bei ~1,7 auf. D 1,8-2,4: Hinterbeine fertig untergeschlagen, Kopf legt sich zwischen die Pranken, ein **Seufzer** (Ruecken hebt 1,8-2,0, sinkt 2,0-2,4). Reihenfolge Hinterbeine vor Vorderbeinen wie beim Hinsetzen (Fixer-Lehre: sonst faehrt der Unterschenkel durch den Unterarm, `baer_kampf_fell.py` Doku von `sp_setzen`) |
| **NCBear_Sleep** | 12,0 s | 360 | ja (erstes = letztes Bild = L) | L -> L | Zwei Atemzuege (Einatmen 0-2,4 / 6,0-8,6, Ausatmen 2,4-5,4 / 8,6-11,4, kurze Pause): Becken z +8..+10 mm, Lende/Brust nicken je -1..-1,5 Grad (Ruecken hebt sich), Schulterblatt mit; ~10 Atemzuege je Minute. Kopf: bleibt liegen, kleines Traumzucken bei ~7,5 s (rollen 2 Grad, 0,3 s), Kiefer beim Ausatmen 0 -> 2-3 Grad -> 0 (Lippen "blubbern", passt zu einem Schnarchton). Schwanz zuckt bei ~9,5 s. Pfoten fest (Gleiten 0). Ton-Momente fuer einen Schlafton: Beginn Ausatmen 2,4 s und 8,6 s |
| **NCBear_WakeUp** | 2,2 s | 66 | nein | L -> Grund | A 0-0,5: Kopf hebt sich (Quelle 1: erst Kopf hoch und schauen). B 0,5-1,0: kurz umschauen (gieren +-15). C 0,8-1,4: Vorderbeine strecken (Ellbogen 107 -> 150), Brust hebt, Vorderpfoten einen halben Schritt zurueck. D 1,2-1,9: Hinterbeine unter den Koerper, Hinterteil hebt. E 1,9-2,2: Grundhaltung |
| NCBear_WakeAlarm (optional) | 1,1 s | 33 | nein | L -> Grund | Kopf ruckt hoch (0-0,2), dann C-E im Schnellgang. Fuer "Kampf hat Vorrang" (Zombie kommt): 2,2 s ruhiges Aufwachen ist zu lang, um sich zu wehren |
| NCBear_LieIdle (optional) | 6,0 s | 180 | ja | L -> L | Wach liegen, Kopf hoch, schaut langsam umher -- vor dem Einschlafen / nach Laerm, ohne gleich aufzustehen. Kevins Wort |
| NCBear_Scrape (optional) | 2,0 s | 60 | nein | Grund -> Grund | Bett zurechtscharren mit einer Vorderpranke vor dem Hinlegen (Quellen 4, 5). Kevins Wort |

Vergleich der Dauern: Vanillas Reh `DeerStag_IdleToSitting` 2,67 s und `DeerStag_SittingToStanding` 2,40 s (das Reh "sitzt" dabei in
Bauchlage; Zahlen aus `anim_referenz.md` Abschnitt 9); unser SitDown 1,6 s, StandUp 1,3 s, Sit-Schleife 4,0 s (`anim_clips.md` 3).

Was die vorhandenen Clips beitragen:
- **SitDown/StandUp**: Hinterbein-Schritte, Reihenfolge und `_fuss_flach_bis` (Zehen erst nach der Schrittmitte hoch) wiederverwenden.
- **Sit**: Atem-Muster (Brust nicken, zwei Zuege, `sp_sitzen` 1357) -- fuer die Bauchlage zusaetzlich das Becken heben.
- **Death/Dead**: NICHT als Schlaf verwenden (tot-gleich, ausserhalb des Spuren-Systems gebaut, haengt an `liege_alt.json`).
- **Eat**: Kopf-am-Boden-Haltung und Kiefer-Spur als Vorbild fuer "Kopf liegt".

Skelett (26 Knochen, `anim_referenz.md` Abschnitt 1): Atmen geht nur ueber Becken-Position und Lende/Brust (keine Rippen-Knochen,
Knochen werden nicht skaliert -- jede Taste setzt Scale 1, `baer_kampf_fell.py` `schluessel`); Kopf, Hals, Kiefer, Schwanz fuer die
kleinen Bewegungen; Schulterblatt traegt keine Gewichte. **Es gibt keine Ohr-Knochen**: Ohrzucken ginge nur mit einem neuen Knochen,
der Gewichte und alle Clips beruehrt -- nicht empfohlen.

## 4. Wie die Blender-Kette die Clips baut, und was danach nachzuziehen ist

**Welche Datei:** die juengste Clip-Quelle. Heute ist das `baer/spiel/baer_kampf_fell.py` (Kopie von `baer_kampf_anim.py`, Clips Zeile
fuer Zeile gleich, Netz/Gewichte aus baer-fell, `bau_netz.md` Abschnitt 2). **Erst anfassen, wenn baer-fell fertig ist** (der Lauf
arbeitet noch an Netz und Textur). Neu hinein: `_pose_l()` / `POSE_L`, `sp_hinlegen()`, `sp_schlafen()`, `sp_aufwachen()` (und
optional Alarm), drei Zeilen in `KAMPF_CLIPS` (Anfang/Ende `None`/`POSE_L` usw.), `"NCBear_Sleep"` in `SCHLEIFE`.

**Regeln aus baer-anim, die gelten (alle schon im Skript):**
1. Gelenkgrenzen als feste Regel: `GRENZEN` (562), `GRENZEN_RUMPF` (566), `GRENZE_KLAV` (572), Kiefer 0-40, Spruenge je Bild `SPRUNG`
   (574), Hinterfuss-Rollen `SOHLE_GRENZE` (577); jede Taste wird nach dem Loesen geklemmt (`bein_kampf`, `rumpf_bei`), die Zahl der
   Klemmungen steht je Clip im Bericht (`bericht` 1467). Ziel wie baer-anim: unabhaengige Gegenmessung mit
   `_arbeit/baer_anim/anim/gelenke_messen_anim.py` ohne Befund (`anim_clips.md` 1).
2. Kein Knick gegen das Gelenk; Pfote in der Luft relativ zum Unterarm (`welt_`=0), am Boden flach in Welt (`welt_`=1).
3. Boden: tiefster Hautpunkt hoechstens ~2 mm unter 0 (`anim_clips.md` 5), gemessen mit `haut_bericht` (2293) und verbindlich mit dem
   Importer des Spiels (`Dump.java`/`Probe.java`, `_arbeit/baer_anim/anim/pruef_anim.py`); Fussgleiten aufgesetzter Pfoten unter 0,01 Kacheln.
   **Gerade die Liegepose braucht das:** in meiner Probe stecken Ellbogenunterseite (5 cm) und Hinterfuss (4 cm) im Boden.
4. Kritiker Bild fuer Bild (Vorbild `baer/spiel/anim_review_optik.md`: Durchdringung ueber Windungszahl `wind2.py`, Gleiten, Rollen,
   Bildblaetter; Werkzeuge in `_arbeit/baer_anim/pruef/`), Vorschau im Spielwinkel und von der Seite, hoechstens zehn Runden.
5. **Liegehoehe:** `liege_alt.json` (Argument 3, `baer_kampf_fell.py:48`) ist NUR fuer Death/Dead und muss weiter uebergeben werden, sonst
   bewegen sich die alten Clips (`anim_modell.md` 5/6). Die Hoehe der neuen Pose L kommt aus der Haut (wie `_pose_s`: tiefster Rumpfpunkt
   ~0-6 mm) und sollte **als feste Zahl im Skript** stehen (wie `POSE_S` pel = (0,075, 0, -0,336)), nicht zur Bauzeit gerechnet --
   sonst wandert die Pose, sobald `baer_gewichte_fell.py` die Gewichte neu rechnet (dieselbe Lehre wie bei `liege_alt.json`).
6. Alle anderen 15 Clips muessen bit-gleich bleiben (`glb_pruef.py`, wie `bau_netz.md` 3.3).

**Danach nachziehen:**
1. `baer/spiel/baer_gewichte_fell.py` neu laufen lassen: die Gewichte sind gegen genau diese 15 Clips optimiert (`bau_netz.md:162`);
   die drei neuen Clips gehoeren in die Energie (jedes 5. Bild) und in die Bedingung "kein freier Punkt unter dem Boden".
2. Dehnung messen (`_arbeit/baer_fell/netz/messen.py`, Ziele 99,5 % <= 2,6 und max <= 4,0 je Clip, `bau_netz.md` 3.4) und
   **Falten liegend** (`falten_fell.py`; Achsel+Ellbogen heute 154 statt Ziel 120, `bau_netz.md:164`) -- die Sphinx knickt den Ellbogen
   auf ~107 Grad und drueckt die Achsel zusammen, also genau die Schwachstelle.
3. GLB: Dreiecke unveraendert (18.870), Groesse waechst um grob einige hundert KB (Schaetzung, 360-Bilder-Schleife; im Bau messen).
4. Knoten-XML in `42/media/AnimSets/buck/idle/` nach Muster `NCBear_SitDown.xml` / `NCBear_Sit.xml` (Variable `NCBearAct`, Ende-Ereignis
   `NCBearDone=true`, Schleife `m_Looped true`) -- Vanilla `buck` hat KEINEN Schlafknoten (grep "sleep" in `media/AnimSets`: nur
   `player/onbed`), also eigene Knoten wie beim Sitzen.
5. Lua (anderer Forscher/Bauer): `F.ACTS` in `NCBearFight.lua:47-56` (Dauern), Unterzustaende wie sitdown/sit/standup (`calmStart` 1500,
   Kampf weckt: Muster "aus sit erst standup" 1617-1621), kein Schnauben im Schlaf (`HUFF_SIT_MUL` 163 gilt heute fuer Sitzen),
   Engine-Fluchtbefehle bei Laerm (Lauf baer-laerm) waehrend des Schlafs abfangen. Testbefehl nur in `NCBearBench.lua`.

## 5. Bett und Hoehe -- Empfehlung an den Bett-Forscher

Das Tier steht immer auf der Bodenhoehe seiner Kachel; der Clip legt die Haut auf z = 0. Liegt ein Bett-Modell darunter, ist alles
unterhalb der Liegeflaeche im Bett versteckt.

| Weg | Befund | Urteil |
|---|---|---|
| **a) Bett flach (Matte, Strohlager, Fellnest)** | Mit Liegeflaeche h sinkt der Baer h tief ein. Im Sphinx-Bild bei 1,35 liegen Kinn 0,10 m und Pfotenoberkante 0,21 m hoch (aus 0,077 / 0,159 m bei 1,0); bei h = 4-5 cm bleiben Kinn und Pranken sichtbar, der Bauch "sinkt ins Stroh" | **empfohlen** |
| b) Hoehe im Clip | Braucht einen zweiten Satz Liege-Clips (Kevin will auch "beim Besitzer" schlafen, also auf dem Boden), dazu einen Schritt hinauf beim Hinlegen und hinunter beim Aufstehen. Vanilla-Spieler: `ISGetOnBedAction.lua` setzt nur Variablen (Zeilen 22-170, z. B. `OnBedDirection`), kein `setZ` -- die Bett-Hoehe muss dort also aus Clips/Engine kommen (welches von beiden: ungeprueft) | nein (doppelte Clips) |
| c) Hoehe per Code | `animal:setZ(animal:getZ() + 0.66)` ist in Vanilla belegt, aber nur fuer ein Tier am Schlachthaken mit `setOnHook(true)` (`ButcheringUtil.lua:577-578`, Werte `AnimalAvatarDefinition.lua:23`); `ClientCommands.lua:847` setzt ganze Ebenen. Ob ein lebendes, freies Tier eine Bruchteil-Hoehe behaelt oder zurueckfaellt: **ungeprueft**; im MP muesste der Server es setzen | nein (ungeprueft, MP-Risiko) |

**Klare Empfehlung:**
- **Liegeflaeche 4 cm ueber dem Boden (hoechstens 5 cm)**, Masse in Spielmetern (Mensch 1,8 m).
- **Innenmass mindestens 2,8 m x 1,65 m (2,3 x 1,35 Kacheln)** fuer den Erwachsenen = gemessener Umriss Sphinx 2,57 x 1,50 m plus ~10 %
  (Atmen, Kopf zur Seite, Blende beim Hinlegen, Ungenauigkeit der Probe +-5 cm). Zwei Kacheln Laenge (2,45 m) sind zu kurz; drei
  Kacheln lang und zwei breit passt.
- Rand/Wulst nur ausserhalb des Umrisses (mindestens 10 cm Abstand), hoechstens ~12 cm hoch und an der Kopfseite bzw. zur Kamera hin
  niedrig oder offen, sonst verdeckt er Kopf, Pranken und die z Z z-Stelle.
- Der Baer liegt laengs zum Bett (Ausrichtung des Tiers an der Bett-Richtung). **Die Mitte seines Umrisses liegt 0,15 m (bei 1,35:
  0,20 m = 0,16 Kacheln) VOR seinem Wurzelpunkt Bip01** (Umriss x -0,806..+1,098 bei 1,0) -- beim Hinstellen auf das Bett zu beachten.
- Jungtier (0,35) und Halbstark (0,75) liegen im selben Bett deutlich kleiner (0,67 x 0,39 m bzw. 1,43 x 0,83 m).

## 6. Umriss der Haltungen (Messung)

**Methode:** `schlaf_probe.py` / `schlaf_probe2.py` fuehren `baer_kampf_fell.py` nur bis vor den Abschnitt "Armature" aus (Fell-Netz
`_arbeit/baer_fell/mod/42/media/models_X/WorldItems/NCBear.fbx`, 9.270 Punkte mit Krallen, ohne Mundbeutel; Gewichte
`_arbeit/baer_fell/netz/gewichte_fell.npz`; Liegepose `liege_alt.json`), bauen die Pose mit den Funktionen des Skripts
(`spuren_bauen`, `kampf_pose` samt Klemmen gegen die Gelenkgrenzen; Seitenlage = `pose_dead`) und haeuten wie die Engine
(`haut_tier`, lineares Haeuten). Gemessen: Ausdehnung aller Hautpunkte in x (vorn) und y (seitlich), hoechster Punkt, Draufsicht-Flaeche
(4-cm-Raster). Hoehe des Beckens so, dass der tiefste Rumpfpunkt +6 mm liegt (wie `boden_liege`). Umrechnung auf 1,35 linear
(Annahme: `setSizeForced` skaliert gleichmaessig; passt zu ENTSCHEIDUNGEN 1,96 m -> 2,65 m). Gegenprobe Stehen: 1,945 x 0,962 m
gegen 1,96 x 0,97 m in `anim_modell.md` 3 (Fell-Netz minimal anders).

| Haltung | bei 1,0: L x B (m) | Hoehe | bei 1,35: L x B (m) | in Kacheln bei 1,35 | Draufsicht bei 1,0 | Bemerkung |
|---|---|---|---|---|---|---|
| Stehen (Gegenprobe) | 1,945 x 0,962 | 1,155 | 2,63 x 1,30 | 2,14 x 1,06 | 1,34 m2 | stimmt mit Bestand |
| **Sphinx, Kopf gerade** | **1,905 x 1,112** | 0,846 | **2,57 x 1,50** | **2,10 x 1,23** | 1,54 m2 | Vorderbein 0 Klemmungen, 4 am Hinterfuss; Ellbogen 5,2 cm, Hinterfuss 3,9 cm im Boden |
| Sphinx, Kopf 25 Grad zur Seite | 1,870 x 1,112 | 0,846 | 2,52 x 1,50 | 2,06 x 1,23 | 1,53 m2 | Rumpf 0 Klemmungen |
| Seitenlage = DeerStag_Dead | 1,880 x 1,077 | 0,961 | 2,54 x 1,45 | 2,07 x 1,19 | 1,38 m2 | Bestand, tot-gleich |
| Halb eingerollt (grob) | 1,481 x 1,182 | 1,004 | 2,00 x 1,60 | 1,63 x 1,30 | 1,38 m2 | Beine nicht sauber (22 Klemmungen, Pfoten bis 9,6 cm im Boden bzw. 0,5 m in der Luft) -- nur Groessenordnung |
| Froschlage (Grenzen verletzt) | 2,091 x 0,968 | 0,877 | 2,82 x 1,31 | 2,30 x 1,07 | 1,62 m2 | Fuesse 31 cm im Boden; echte Froschlage waere noch ~0,2 m laenger |
| Sitzen (NCBear_Sit, Vergleich) | 1,701 x 1,419 | 1,191 | 2,30 x 1,92 | 1,87 x 1,56 | 1,46 m2 | |

Fuer z Z z (Zeichnen ueber dem Kopf): in der Sphinx liegt der Hinterkopf oben bei x ~0,70 m, z ~0,50 m (bei 1,35: ~0,95 m vor Bip01,
0,67 m hoch), der hoechste Punkt ist der Buckel bei x 0,23, z 0,85 (bei 1,35: 1,14 m) (`umriss2_sphinx_haut.npy`).

## 7. Einzelspieler, Mehrspieler, Copy-Paste

- Clips und Knoten-XML sind fuer SP und MP gleich (dieselbe GLB, dieselben Knoten). Wer im MP die Variable `NCBearAct` setzt und ob alle
  Zuschauer den Schlaf-Clip sehen, ist dieselbe offene Frage wie beim Sitzen (MP ist heute im Test aus, `STAND.md` Punkt 10) -- **MP offen**.
- Pfade wie in NPC Crew: `42/media/models_X/Skinned/NCBear.glb`, `42/media/AnimSets/buck/idle/*.xml`. Clip-Namen hier `NCBear_*` wie die
  vorhandenen; ob sie bei der Umbenennung in B5a mitwandern, entscheidet B5a -- **vor dem Bau festlegen**, sonst muss die GLB spaeter neu.
- Keine Testteile in den Clip-Dateien; ein Test wie `NCBear_AnimTest("sleep")` nur in `NCBearBench.lua` (geht nie nach NPC Crew).

## 8. Quellen (gelesen am 09.11.2026; nichts heruntergeladen, Bilder/Videos nicht abgerufen)

1. https://npshistory.com/series/science/14/chap4.htm -- A. Murie, The Grizzlies of Mount McKinley, Kapitel 4 "The Family" (NPS Scientific Monograph 14; der Autorname steht im gelesenen Teil nicht, bekannt aus dem Werk): Ruhelagen (Seite, Bauch mit Hinterbeinen nach hinten, Ruecken, Schnauze am Boden), Betten auf Simsen, Aufwachen (Kopf mehrmals heben, dann aufstehen und schauen). Gelesen: erste 100.000 Zeichen der Seite.
2. https://faunalytics.org/effect-of-the-change-of-social-environment-on-the-behavior-of-a-captive-brown-bear-ursus-arctos/ -- Zusammenfassung von Mattiello et al. 2014, J. Vet. Behav. 9(3):119-123, doi 10.1016/j.jveb.2014.01.002: Seitenlage im Schlaf, REM, Anteile.
3. https://pmc.ncbi.nlm.nih.gov/articles/PMC8614411/table/animals-11-03214-t001 -- (nur Suchauszug) Ethogramm-Begriffe "sternal" (Brust, Kopf hoch oder Nase am Boden, Beine unter/neben dem Koerper) und "lateral recumbency" (Seite, Beine gestreckt); Tierart nicht genannt.
4. https://polarbearsinternational.org/news-media/articles/polar-bear-sleep-patterns -- Pranke als Kissen, Liegemulden ~1,5 m quer bis 0,5 m tief, 7-8 h Schlaf und Nickerchen 1-2 h.
5. https://bear.org/summer-beds/ -- North American Bear Center: Sommerbetten auf kuehlem Moosboden, Polster aus abgebissenen Zweigen/Rinde.
6. https://www.bearbiology.org/download/characteristics-of-summer-beds-of-european-brown-bears-in-norway/ -- Mysterud 1983, Ursus 5:208-222: 119 Sommerbetten (nur Kurzfassung, keine Masse gelesen).
7. https://sdzwildlifeexplorers.org/animals/brown-bear -- San Diego Zoo: 4-6 Monate eingerollt im Lager.
8. https://kodiakbearcenter.com/?p=4902 -- Kodiak: Kammer gerade gross genug zum Einrollen, Atmung im Lager etwa 4 je Minute, Herz ~50 -> 8-12.
9. https://link.springer.com/article/10.1007/s00442-011-1920-5 -- Ordiz et al. 2011, Oecologia: Tagesbetten mit mehr Deckung; Ruhe ~12 h/Tag (~9 h Tag, ~3 h Nacht) nach Moe et al. 2007 -- **nur Suchauszug**.
10. https://openpolar.no/Record/crcansciencepubl:10.1139%2Fz07-034 -- Moe et al. 2007, Can. J. Zool. 85:518-525: Tagesrhythmus (aktiv morgens/nachmittags, Ruhe mittags/nachts) -- **nur Suchauszug**.
11. https://webarchive.library.unt.edu/web/20120927065533/http://www.nps.gov/yell/forkids/upload/YELL710.pdf -- NPS Yellowstone: Atmung 6-10 je Minute normal, im Winterschlaf 1 je 45 s; Herz 40-50 -> 8-19 -- **nur Suchauszug** (Abruf lieferte leere Seite).
12. https://www.yellowstone.org/naturalist-notes-hibernation/ -- Yellowstone Forever: 1 Atemzug je 45 s im Winterschlaf, Herz Sommer 40-50 -> 8-12.
13. https://www.nps.gov/katm/blogs/Hibernation-in-Bears.htm -- NPS Katmai: im Winterschlaf ~1 Atemzug je Minute, Herz 8-10.
14. Lokal: Vanilla `media/AnimSets/buck/idle/idleSit.xml` (Reh-"Sitzen" = Bauchlage, Clips `DeerStag_SittingIdle`/`_SittingToStanding`), `media/AnimSets/player/onbed/OnBedAsleep.xml`, `media/lua/shared/TimedActions/ISGetOnBedAction.lua`, `media/lua/shared/Definitions/animal/ButcheringUtil.lua:569-578`, `media/lua/server/ClientCommands.lua:847`.

Schwache oder nicht verwendete Treffer: Matratzen-Blogs ("eingerollt oder ausgestreckt auf dem Bauch"), Hunde-Seiten zu Schlafhaltungen
-- nicht als Beleg genommen.

## 9. Unsicher

- **Nicht gespielt, nicht gerendert.** Die Posen der Messung sind Proben fuer den Umriss, keine fertigen Clips; wie knuffig die Sphinx im
  Spiel wirkt, zeigt erst ein Vorschaubild im Spielwinkel und Kevins Blick.
- Atemtakt im Sommerschlaf ist nicht gemessen gefunden; 10 je Minute ist ein Spiel-Vorschlag. Ob 1-1,5 cm Ruecken-Hub aus der Spielkamera
  sichtbar ist, ungeprueft (im Bau gegen ein Vorschaubild pruefen, notfalls staerker).
- Hinlege-Ablauf echter Baeren: keine Quelle gefunden; die Phasen sind aus Mechanik und unseren Clips abgeleitet.
- Umriss +-5 cm (Probe mit Bodendurchdringung an Ellbogen/Hinterfuss); halb eingerollt nur Groessenordnung.
- `setSizeForced` gleichmaessig skaliert: Annahme (stimmt mit den bisherigen Zahlen ueberein, hier nicht am Jar geprueft).
- Bett-Hoehe per Code: `setZ` an einem freien lebenden Tier ungeprueft.

## 10. Fragen an Kevin

1. Haupt-Schlafhaltung **Sphinx** (Bauch, Kopf auf/zwischen den Pranken, im Schlaf leicht zur Seite) -- ja? Seitenlage nicht, weil sie
   wie die Tot-Pose aussieht.
2. Zweite Haltung "halb eingerollt" spaeter dazu, oder erst mal nur eine?
3. Kurz "Bett zurechtscharren" vor dem Hinlegen (echt bei Baeren) -- ja/nein? Und "wach liegen und umschauen" (LieIdle)?
4. Schnelles Aufwachen bei Zombies (WakeAlarm 1,1 s) zusaetzlich zum ruhigen Aufwachen (2,2 s) -- ja?
5. Bett flach wie ein Strohlager/Fellnest (4 cm, Innenmass ~2,8 x 1,65 m, drei Kacheln lang) statt eines hohen Bettgestells -- ok?

Statisch geprueft und offline gemessen, nicht gespielt.
