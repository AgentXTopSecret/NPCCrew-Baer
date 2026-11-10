# Pruefung Lauf baer-baby (Entwurf Baer-Junges) -- Pruefer, 10.11.2026 nachts

**Statisch/offline geprueft, gemessen und selbst gerendert (RTX 4090, OptiX + Entrauscher, Sperre `gpu.lock`), NICHT gespielt.**
Am Bau nichts geaendert. Eigene Dateien nur unter `_arbeit/baer_baby/pruef/` (Skripte `pruef_technik.py`, `ort_dehnung.py`,
`szene_bauen.py`, `auftrag_bauen.py`, `auftrag2_bauen.py`, `render_pruef.py`; Ergebnisse `technik.json`, `dump_pruef.txt`,
`dump_erw.txt`, Bilder `pruef/bilder/`). Eigene Renders kommen aus MEINEM Dump (Dump.java, JAssImp wie das Spiel), nicht aus den
Render-Skripten des Bauers. **`pruef/bilder/intern_vergleich_foto_p1.png` zeigt die Vorlage: nur intern, nie weitergeben.**

## 0. Urteil kurz

- **Ist es ein Baerenjunges wie im Foto?** Von der FORM her ja: runder, breiter Kopf, Stirnabsatz, Ohren oben weit aussen, kurze
  Schnauze, grosse Nase; kein Fellkragen; neben dem Erwachsenen x0,35 klar ein Junges, kein verkleinerter Erwachsener (R5,
  `pruef/bilder/p7_spiel_stehend_tex.png`). In Spielgroesse lesbar.
- **Aber deutlich sichtbar (major):** der Kopf wirkt **aufgesteckt** (eigene Kugel-Schale mit Kerbe zum Hals + harter Bruch der
  Fellstruktur), das **Kopffell ist fleckig wie Kork statt flauschig**, die **Augen** bekommen einen hellen Unterlid-Halbmond
  (starrer Blick, im Foto kein Weiss), beim **Fressen klappt eine 0,92 W breite Kiefer-Platte** auf (Spalt ueber die ganze Wange),
  und der Bericht sagt **`Translation_Data` unveraendert -- im GLB ist der Weg aber x0,777**. Hautdehnung in den Clips verfehlt die SPEZ
  (vom Bauer offen gesagt, von mir bestaetigt).
- **Technik und Regeln gruen:** Importer laedt, 26 Knochen gleich, 19.938 Dreiecke, <= 4 Einfluesse, Summe 1, ein Netz, keine offenen
  Kanten, Naehte bleiben in allen Posen zu, Boden <= 0,28 cm, Textur 1024 RGB, keine Foto-Pixel, Namen kollisionsfrei, Test-Mod/NPC Crew/
  2c/Originale unberuehrt. Kein Blocker.

## 1. Technik (selbst gemessen)

| Pruefung | Ergebnis | Beleg |
|---|---|---|
| GLB-MD5 | 129cfc23db342d66c3a0030181725335 (= Bericht); Textur 07abcf75... | `md5sum` |
| Importer (Dump.java, JAssImp) | laedt, 26 Knochen, 15 Clips; mein Dump byte-gleich mit `entwurf/dump_final.txt` | `pruef/dump_pruef.txt` |
| Knochen Name/Eltern/Reihenfolge | = Erwachsener (NCBearTest-GLB selbst gedumpt, = `baer_pfote/fix1/bau4/dump_final.txt`) | `pruef/technik.json` |
| Dreiecke | 19.938 (Erwachsener 19.426) | dito |
| Einfluesse / Summe / negativ | max 4 / 0,99999985..1,00000018 / 0 | dito |
| GLB-Aufbau | 1 Netz, 1 Primitiv, 0 Material, 0 Bild, 1 Skin 26 Joints, 15 Animationen, 28 Knoten -- identisch zum Erwachsenen | GLB-JSON gelesen |
| NaN | keins | dito |
| Offene / nicht-mannigfaltige Kanten (geschweisst 1e-5) | 0 / 0 (Erwachsener 0 / 41) | dito |
| Schalen | Koerper+Hals 9.476 Punkte, Kopf 1.532 (nur Head), Kiefer 284 (nur Jaw), 2 Ohren je 142, 20 Krallen | eigene Komponenten-Zaehlung |
| Naehte (2.017 zusammenfallende Punktpaare) in Idle/Walk/Run/Sit/Eat/Maul/SitDown/SwipeL, alle Bilder | max 1e-15 E auseinander -> keine Risse | `pruef/technik.json` |
| Boden (tiefster Punkt Junges minus Erwachsener, alle Bilder) | 0,00 cm, Eat -0,28 cm | dito |
| Textur | 1024 x 1024 RGB | PIL |
| Foto-Pixel | `baer_textur_baby.py` liest nur Netz + Erwachsenen-Textur (`baer_form_baby.py:26`); die Vorlage lesen nur `werkzeug/raster.py`, `farben.py`, `blatt_ton_foto.py`, `blatt_foto_baby.py` (Mess-/Blatt-Skripte). Bilder fuer Kevin (`bilder/`) zeigen kein Foto | grep |
| Namen | `bearcub|NCBearCub|BanditsNPCBearCub`: NPC Crew `42/media/lua` 0, Vanilla `media/lua`+`media/scripts` 0, NCBearTest 0 | grep |
| Regeln | NCBearTest-GLB 5066fa67 unveraendert (mtime 10.11. 00:04, vor dem Lauf); `*_pfote.py` MD5 = Log; in `_arbeit/baer_fell|baer_pfote|baer_spiel` und `baer/begleiter` keine Datei neuer als der Laufstart; kein Commit (HEAD 99971a4) | find/md5sum/git |

**Hautdehnung** (sigma1 je Dreieck gegen die Ruhe, Dreiecke mit kleinster Kante > 0,004 E wie `dehnung_lib.py`, alle Bilder zusammen;
Koerper ohne Kopf/Hals):

| Clip | Junges p99,5 / max | Erwachsener p99,5 / max | Anteil sigma > 2 Junges / Erw. |
|---|---|---|---|
| Idle | 1,25 / 3,7 | 1,15 / 1,6 | 0,01 % / 0,00 % |
| Walk | 2,05 / 16,1 | 1,55 / 7,6 | 0,57 % / 0,03 % |
| Run | 2,59 / 21,7 | 1,82 / 9,4 | 1,50 % / 0,16 % |
| Sit | 2,57 / 16,5 | 1,96 / 6,9 | 2,35 % / 0,44 % |
| SwipeL | 2,92 / 24,3 | 1,95 / 8,3 | 1,53 % / 0,43 % |

Ort (`pruef/ort_dehnung.py`): in Run sitzen 84 der 124 Dreiecke mit sigma > 3 auf Spine1 (Brust/Bauch unten, ~24 cm ueber Boden bei
Groesse 1), 14 an den Unterarmen (Achsel). Bild `pruef/bilder/p8_bauch_unten_rennen_ton.png`: zerknitterte Manschetten an Achsel und
Leiste. SPEZ 4.7.6 (<= Erwachsener + 10 %) **verfehlt** -- deckt sich mit `bau_baby.md` 3.8.

## 2. Optik (eigene Renders, Ton UND Textur)

Bilder: `pruef/bilder/p0_foto30_ganz_paar.png`, `p1_foto30_kopf_paar.png`, `p2_dreiviertel_paar.png`, `p3_seite_paar.png`,
`p4_nacken_nah_paar.png`, `p5_sitzen_paar.png`, `p6_maul_offen_paar.png`, `q1_augen.png`, `q2_maul.png`, `q3_spiel.png`,
`p7_spiel_stehend_tex.png`, `p7_spiel_sitzend_tex.png`, Ausschnitte `z_*.png`; intern `intern_vergleich_foto_p1.png`. Dazu alle
Bilder des Bauers angesehen (R1-R6, R5 in voller Groesse, C).

### Gesicht gegen das Foto (je Merkmal)
| Merkmal (Foto) | Ton | Textur | Urteil |
|---|---|---|---|
| Kopf gross, rund, breiter als lang | ja (p1, R6) | ja | erfuellt |
| Stirn gewoelbt, deutlicher Absatz | ja (R6 Seite, Stufe Schnauze -> Stirn) | ja | erfuellt |
| Ohren gross, rund, weit aussen oben, dick bepelzt, innen heller | Lage trifft die Fotolinien (intern_vergleich); wirken als glatte duenne Scheiben | Ring hell / Mulde dunkel = Teddy-Spielzeug | teils |
| Schnauze kurz, stumpf, hell, nach oben verlaufend | ja | ja, gut | erfuellt |
| Nase gross, schwarz, glaenzend | ja | ja, Glanz gemalt | erfuellt |
| Augen gross, rund, dunkelbraun, Glanzpunkt, dunkler Ring | nur flache Delle mit gezackten Kerben (q1) | rundes Auge + Glanz, aber heller Unterlid-Halbmond rundherum unten, polygonaler Rand | **verfehlt im Ausdruck** |
| Fell dicht, kurz, flauschig, schokobraun mit hellen Spitzen | -- | grobe schwarze Flecken (Kork/Schwamm), anders als Koerperfell | **verfehlt** |
| Wangen leicht abstehend | glatter Umriss, keine Fellzacken | -- | fehlt |
| Kopf oben auf dem Koerper, kein Kragen | kein Kragen ja; Kerbe Kopf/Hals rundum | harter Struktur-/Farbbruch an der Kopfgrenze | **teils** |

### Gruselig / plump / verzogen?
- Nicht gruselig in der Gesamtform; die Front (p0, R1) liest sich als niedliches Junges.
- Leicht unheimlich wirken: der helle Halbmond unter der Iris (wie sichtbares Augenweiss), die rote Lippenlinie beim Fressen
  (q2, wie Lippenstift/Blut), der fleckige dunkle Kopf ("schorfig").
- Plump: Rumpf als langes Fass mit "Hose in Stiefeln" und Menschen-Sohle im Sitzen (p3, p5, R4) -- bekannte Baustelle 2c, nicht
  diesem Lauf angelastet, bleibt aber im Bild.
- In Spielgroesse (577 px/E, R5, p7, q3): klar lesbar als Junges; Kopf wirkt grauer/kuehler als der warme Koerper.

## 3. Befunde

### major

**M1 Kopf wirkt aufgesteckt (Geometrie-Kerbe + Struktur-Bruch).**
Beleg:
- Der Kopf ist eine eigene geschlossene Schale (1.532 Punkte, nur Head), die den Hals-Schlauch durchdringt; Kopf und Hals sind
  nicht verbunden.
- Folge ist eine scharfe Kerbe rundum: `pruef/bilder/p4_nacken_nah_paar.png`, `p3_seite_paar.png`, R3 "Ton az 90" (Kerbe am Nacken),
  R4/p5 (Kugel auf dem Rumpf).
- Textur: Hochpass-Kontrast (|L - 9x9-Mittel|) Kopf 16,0 gegen Koerper 6,3, dunkle Texel (L < 35) 9,2 % gegen 3,2 %. Die Kopfgrenze
  ist eine harte Linie (p2, p4 Textur).
- In Spielgroesse wirkt der Kopf grauer (R5).
- Das ist Kevins Kritik am Erwachsenen ("wirkt aufgeklebt"); SPEZ 4.2 verlangt "ohne Kante".
Vorschlag:
- Hals-Loft am Kopf tangential auslaufen lassen oder die Kopfschale mit dem Loft verschweissen. Den Rand mit einem Fellwulst
  ausrunden: Neck/Head-Mischgewichte ueber ~0,1 W statt einer Durchdringung.
- Textur: Uebergangsband ~0,1 W, das Kopf- und Koerperfell mischt, und beide Fellstrukturen angleichen (siehe M2).

**M2 Kopffell fleckig statt flauschig.**
Beleg:
- p1/R6/R1 Textur: grobe schwarze Kleckse ohne Haarrichtung auf der Stirn.
- Im Foto feine kurze Haare mit hellen Spitzen. Der Kontrast passt in Zahlen (Kopf 16,0, Foto-Stirn 18,1 bei gleicher Texeldichte,
  nur gemessen), das MUSTER aber nicht: Klumpen statt Haare.
- Der Bauer nennt es selbst "wollig".
Vorschlag:
- Feine Straehnen (2-4 Texel breit, 8-15 lang) in Haarstrich-Richtung mit hellen Spitzen von 10-15 %, die dunklen Klumpen weg.
- Das Koerperfell auf dieselbe Kornung bringen oder umgekehrt.

**M3 Augen: heller Unterlid-Halbmond, im Ton nur gezackte Delle.**
Beleg:
- `pruef/bilder/q1_augen.png` und `z_augen.png`: weiss-blauer Halbmond unter der Iris, ~0,01 W breit, im Licht fast weiss.
  SPEZ verlangt 0,004-0,006 W hellgrau; das Foto zeigt kein Weiss.
- Der Ring um das Auge ist ein sichtbares Sechs-/Achteck.
- Im Ton nur eine flache Delle mit dunklen Zacken-Kerben (rechtes Auge). Die Textur traegt das runde Auge.
Vorschlag:
- Unterlid dunkel-graubraun (~(90,80,75)), <= 0,005 W, nur unten-aussen.
- Augenrand im Netz feiner (>= 16 Segmente) und Augapfel/Lid ohne Durchdringung.
- Leichter dunkler Augenring statt hellem Rand.

**M4 Kiefer als 0,92 W breite starre Platte.**
Beleg:
- Die Kiefer-Schale ist 0,922 W breit, 0,542 W lang, nur Jaw, keine Mischzone (0 Punkte mit Jaw-Gewicht 0,05-0,95).
- Die Mundwinkel liegen bei +-0,124 W. Beim Fressen (15 Grad) oeffnet ein Spalt ueber ~0,65 W, also quer durch die Wangen
  ("Entenschnabel").
- Innen zeigt sich eine rote Lippenlinie: `pruef/bilder/q2_maul.png`, `z_maul.png`, auch C "Eat Ton" des Bauers.
Vorschlag:
- Die Kiefer-Schale hinter den Mundwinkeln schmal machen (<= 0,35 W an der Lippe) und die Wangen auf Head lassen.
- Ab dem Mundwinkel Mischgewichte Head/Jaw, damit die Haut sich dehnt statt aufzuklappen.
- Lippenkante dunkelbraun statt rot.

**M5 `Translation_Data` (Weg) ist NICHT unveraendert -- Bericht widerspricht dem GLB.**
Beleg: Lage-Schluessel `Translation_Data` im Dump:

| Clip | Junges | Erwachsener | Faktor |
|---|---|---|---|
| Walk | 0,294 E | 0,378 E | 0,777 |
| Run | 0,822 E | 1,058 E | 0,777 |

- `baer_export_baby.py:6` skaliert den Weg absichtlich (`bewegt` :93), `bau_baby.md:35` sagt das auch.
- `bau_baby.md:25, :122, :161, :193` und die Kurzfassung sagen dagegen "unveraendert = Erwachsenen-Weg".
- Damit ist eine Spielentscheidung schon getroffen (das Junge laeuft bei gleicher Groesse 22 % weniger Weg je Zyklus), die nach
  SPEZ 3.3 Punkt 4 Kevins Wort braucht.
Vorschlag:
- Bericht berichtigen und den Faktor als Schalter im Export fuehren (1,0 / 0,777 / Kevins Wert).
- In B1 Kevin fragen.

**M6 Hautdehnung in den Clips (bestaetigt, SPEZ 4.7.6 verfehlt).**
Beleg: Tabelle in Abschnitt 1. p99,5 liegt bis +50 % ueber dem Erwachsenen, max 16-24 gegen 6-9. Sitz an Bauch, Achsel und Leiste
(`p8_bauch_unten_rennen_ton.png`).
Vorschlag (wie der Bauer): Bein- und Rumpf-Faktoren angleichen oder die Gewichte an Achsel und Leiste neu setzen. Zusammen mit 2c/B1.

### minor

**m1 Nacken: Falte mit dunklem Schlitz.**
- Sichtbar in Idle Bild 0 (`p4_nacken_nah_paar.png`, `z_nacken_ausschnitt.png`) und mit gesenktem Kopf (Maul Bild 24,
  `p6_maul_offen_paar.png`, `q2_maul.png`).
- Es gibt 0 offene Kanten; es ist ein Umklappen bzw. eine Selbstdurchdringung.
- `bau_baby.md:51/:137` sagt "kein schwarzer Spalt mehr".
- In Spielgroesse kaum sichtbar.
- Vorschlag: zusammen mit M1 loesen.

**m2 Wangen-Fellzacken fehlen.**
- SPEZ 4.2 fordert 0,015-0,03 W; der Umriss ist glatt.
- Sie sind nicht als offen gemeldet.
- Vorschlag: kurze Zacken im Umriss zwischen z +0,18 und -0,24 W.

**m3 Beleg "Skalier-Schluessel wirken nicht" (SPEZ 3.3.1) ist ungenau.**
- javap `updateBoneAnimationTransform_Internal`: `getTrackTransform` (202) liefert auch scale, und `boneTransforms.set(position,
  rotation, scale)` (622) setzt es.
- Die Folgerung (eigenes GLB mit eigenen Lage-Schluesseln) bleibt richtig, weil die Skalier-Schluessel 1,0 sind.
- Vorschlag: Satz abschwaechen.

**m4 Skript-Vorschlag `mesh = Skinned/NCBearCub` passt nicht zum Erwachsenen.**
- `bau_baby.md:156` setzt den Pfad ohne `.glb`, beim Erwachsenen steht `mesh = Skinned/NCBear.glb` (`nc_bear_tier.txt:11`).
- "Felder wie beim Erwachsenen" stimmt damit nicht.
- Vorschlag: `.glb` mitschreiben.

**m5 Becken-Hub beim Gehen groesser als beim Erwachsenen.**
- Spannweite des Lage-Schluessels 0,0219 gegen 0,0146 E, verursacht durch den Bodenausgleich je Bild.
- Bei kuerzeren Beinen kann das als Huepfen wirken. Ungeprueft in Bewegung.
- Vorschlag: Bodenausgleich glaetten oder je Stuetzpfote rechnen.

**m6 Koerper (bekannt, Lauf 2c).**
- Langer Fass-Rumpf, "Hose in Stiefeln" (p3) und Menschen-Sohle im Sitzen (p5, R4) bleiben im Bild.
- Die Pfoten wirken gross.
- Nicht diesem Lauf angelastet; bei der Uebernahme von 2c erneut pruefen.

**m7 Zone "ueber dem Auge" 16 Stufen zu dunkel; Ohren wirken als Teddy-Ring.**
- Die Zone ueber dem Auge hat der Bauer selbst gemeldet.
- Die Ohren haben einen hellen Rand und eine dunkle Mulde, statt dick bepelzt zu sein.
- Vorschlag: Fellrand an den Ohren, Zone angleichen.

## 4. Weg ins Spiel (Urteil)

Die Empfehlung A (eigene Art `bearcub` mit eigenem GLB, Stufe -> `bear`, `animset = "buck"`, Clips per Skript) ist **belegt und
machbar**. Nachgesehen:
- Vanilla:
  - `DeerDefinitions.lua:7-11` (fawn -> doe/buck) und `:58-64` (bodyModel `DeerFawn` :59, animset `fawn` :64, eigenes Modell);
    `textureBaby :43`;
  - `models_animals.txt:232-238` (model DeerFawn, animationsMesh Deer_Fawn);
  - `animations_meshes.txt:30-35`;
  - Maus mit gleichem Modell: `MouseDefinitions.lua:87-99`.
- dec `IsoAnimal.java`:
  - `:1525-1537` textureBaby, solange `nextStage` gesetzt ist;
  - `:1779-1781` `isBaby`.
- dec `AnimalData.java`:
  - `:120-133` checkStages -> grow;
  - `:218-234` growUp.
- javap `AnimalData.grow`:
  - Offsets 58/92 (neues IsoAnimal), 268 (Name), 304 (AnimalID), 340-392 (Sprung > 0,7), 540/545 (delete/addToWorld);
  - im ganzen Methodenbereich (javap-Zeilen 4298-4556) **kein getModData** -> Naht modData in B1 belegt.
- NCBearTest: `NCBearDefs.lua:62-102`, `nc_bear_tier.txt:3-15`.

Technik des Entwurfs:
- Das GLB laedt im Spiel-Importer.
- Knochen und Aufbau sind gleich dem Erwachsenen.
- Clip-Drehungen gleich, Boden haelt.

Nutzbar, aber offen:
- Hautdehnung (M6).
- Weg x0,777 schon eingebaut (M5).
- Kiefer-Platte beim Fressen (M4).
- Mehrspieler, `isBaby`-Nebenwirkungen und die modData-Uebergabe sind ungeprueft.

Nicht gespielt.

## 5. Was der Bauer richtig gemeldet hat (bestaetigt)
- Technik-Werte (3.7).
- Bodenausgleich.
- Dehnung nicht erreicht.
- Kopf-Fotolinien: im eigenen Blatt treffen Ohr oben, Krone, Ohrmitte, Auge und Nase (intern).
- Kopf-Masse plausibel.
- Keine Schreibzugriffe ausserhalb.
- Keine Foto-Pixel.
