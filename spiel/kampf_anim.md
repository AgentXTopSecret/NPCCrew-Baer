# Baer: Kampfclips und Maul (NCBearTest) - Animationsbericht

Stand 08.11.2026, PZ 42.21, Blender 5.2.3. **Statisch geprueft und offline gemessen, nicht gespielt.** Gemessen mit dem
Importer des Spiels (`jassimp64.dll`, `ProcessedAiScene`, `tier_werkzeug/Probe.java` und `Dump.java`). Das Spiel lief beim
Start dieses Laufs; gebaut und geprueft wurde ohne GPU, gerendert erst, als `tasklist` es nicht mehr zeigte (vor jedem Render
geprueft).

## Was entstanden ist

| Datei | Inhalt |
|---|---|
| `NPCCrew-Nebenprojekte/baer/spiel/baer_kampf.py` | Kopie von `baer_tier.py` (Original unveraendert) plus Kiefer, Maul, fuenf Kampfclips |
| `_arbeit/baer_kampf/mod/42/media/models_X/Skinned/NCBear.glb` | ein Netz, ein Material, 26 Knochen, 10 Clips (846.128 Byte) |
| `_arbeit/baer_kampf/mod/42/media/textures/Body/NCBear.png` | wie bisher, plus drei Flecken fuer Gaumen, Zunge, Zaehne (16.512 Pixel, alle in freier UV-Flaeche; ausserhalb 0 Pixel geaendert) |
| `NPCCrew-Nebenprojekte/baer/spiel/kampf_vorschau.mp4` | 330 Bilder, 30 Bilder/s, Spielwinkel: Aufrichten+Bruellen, Hieb links, Hieb rechts, Doppelschlag, Biss |
| `NPCCrew-Nebenprojekte/baer/spiel/kampf_bilder.png` | Nahaufnahmen (Bruellen vorn/seitlich, Maul zu, Biss, Hieb, Aufschlag) |

`NCBearDeer.glb` (Rueckfall) wird nicht neu gebaut; die in NCBearTest bleibt. Die Textur-Flecken liegen ausserhalb ihrer UV.
Zweimal gebaut: GLB und PNG byte-gleich (MD5 `2e9a6d17...`, `58a4ea41...`).
Neu bauen: `blender --background --factory-startup --python baer_kampf.py -- <Ordner, unter dem 42/media liegt>`.

## Clips

Zeiten in Sekunden; `m_TimePc` = Zeit / Dauer. Alle Kampfclips stehen auf der Stelle (Translation_Data ueber den ganzen Clip
0,00000, Bip01 bewegt sich nicht), beginnen und enden in der Grundhaltung des Stehens (Mittel von DeerStag_Idle01).

| Clip (`m_AnimName`) | Dauer | Bilder | Treffer | Toene laut Spez | Ablauf |
|---|---|---|---|---|---|
| `NCBear_Rear` | 3,00 | 90 | - (Bruellen ab 0,81 = 0,27) | `NCBearRoar1` 0,27 | 0-0,8 hoch auf die Hinterbeine (Becken 52 Grad, Brust 80 Grad), Vorderpranken vor die Brust; Maul ab 0,6 auf, 38 Grad bei 0,95-1,85, Kopf hoch, schuettelt leicht; ab 2,0 Maul zu, 2,2-2,75 nach vorn auf alle vier, Aufsetzen 2,75 |
| `NCBear_SwipeL` | 1,10 | 33 | **0,46** (0,42) | Wusch 0,27 (0,30) | 0-0,3 Gewicht nach rechts-hinten, linke Pranke aussen hoch (0,98 m); 0,30-0,46 schneller Schlag schraeg nach innen-unten vor dem Gesicht vorbei, Kopf weicht nach rechts-unten aus, Maul 22 Grad (Knurren); 0,46-0,62 zieht bis zum Boden rechts durch; 0,95 Pfote wieder am Platz |
| `NCBear_SwipeR` | 1,10 | 33 | **0,46** (0,42) | gespiegelt | genau gespiegelt aus SwipeL (Skelett symmetrisch) |
| `NCBear_Slam` | 2,20 | 66 | **1,25** (0,57) | Knurren 0,05 (0,11), Aufschlag 0,55 (1,21) | 0,2-0,85 halb aufrichten, Pranken bis Kopfhoehe; 0,85-1,22 beide Pranken mit Wucht nach vorn-unten (Aufsetzen 1,22, Pfote kommt mit Tempo an), Rumpf faellt nach vorn, federt bis 1,38; links tritt 1,42-1,62 zurueck, rechts 1,62-1,82, Rumpf zurueck bis 2,2 |
| `NCBear_Maul` | 1,60 | 48 | **0,544** (0,34) | Knurren 0,10 (0,16) | Kopf tief und vor, Maul auf (34 Grad bei 0,46), Stoss nach unten, Maul schnappt 0,46-0,56 zu; 0,56-1,12 zweimal Schuetteln (Kopf 20 Grad, Rollen 14 Grad); hoch bis 1,6 |

Wo der Treffer sitzt (Pfotenballen bzw. Schnauze zum Treffermoment, Kacheln vor Bip01 = Tiermitte; 1 m = 0,816 Kacheln):

| Clip | Stelle | vor der Mitte | seitlich | Hoehe |
|---|---|---|---|---|
| SwipeL / SwipeR | Pranke | 0,82 Kacheln | 0,04 links bzw. rechts | 0,55 m |
| Slam | beide Pranken am Boden | 0,60 Kacheln | je 0,17 | Boden |
| Maul | Schnauze | 0,78 Kacheln | 0 | 0,12 m |

Hinweis fuer die Lua-Seite: die Spez nennt 1,8 Kacheln Reichweite fuer den Hieb (Spielregel); sichtbar trifft die Pranke
bei rund 0,8 Kacheln. Ein Ziel bei 1,0-1,3 Kacheln sieht getroffen aus, bei 1,8 schlaegt er sichtbar in die Luft. Biss:
die Schnauze erreicht den Boden 0,78 Kacheln vor der Mitte.

## Kiefer und Maul

* Neuer Knochen `Bip01_Jaw`, Kind von `Bip01_Head`, Gelenk unter dem Ohr (Hochmodell `kiefer`, Kopfrahmen (0,075 0 -0,060)),
  Spitze am Kinn. Gewichte: der Kopfanteil teilt sich nach `kiefer_anteil` (vor dem Mundwinkel scharf getrennt, am Winkel je
  die Haelfte, dahinter weich ueber die Wange wie `kiefer_gewicht` in `baer_quelle.py`). 26 Knochen (Grenze 60).
* Das Spielnetz hatte ein geschlossenes Maul. Es wird an der Lippenlinie `c = lippe(a, |b|)` aufgeschnitten (dieselbe Linie,
  an der die Textur die Mundrille malt): 41 Schnittkanten, 40 Punkte verdoppelt. In den Schlitz kommt ein geschlossener
  Beutel (Gaumen oben am Kopf, Zunge unten am Kiefer, hinten quer durch die Mundwinkel verbunden, leicht gewoelbt), dazu vier
  Fangzaehne. Zu liegt alles im Kopf (Nahaufnahme Maul zu: unsichtbar); offen ist es dunkler Gaumen und rote Zunge.
* Netz geschlossen und gleich ausgerichtet (geprueft: jede gerichtete Kante einmal, Gegenkante einmal). 14.642 Dreiecke,
  8.439 Punkte nach dem Importer (vorher 14.228). Lippennaehte und Beutelrand sind scharfe Kanten.
* **Gefundene Falle:** Assimp (`JOIN_IDENTICAL_VERTICES`) hat an zwei Stellen Ober- und Unterlippe wieder zu einem Punkt
  zusammengelegt (gleiche Lage, Normale, UV, nur andere Gewichte) - dort riss die Lippe beim Oeffnen 21-fach. Die
  Unterlippe bekommt jetzt einen UV-Versatz von 0,2 Texel; GLB und Importer haben danach gleich viele Punkte (8.439).
* Kieferwinkel: Rear 38, Hieb 22, Slam 26, Biss 34 Grad; in den alten Clips zu.

## Pruefung (Importer des Spiels)

* **Alte Clips bit-gleich:** DeerStag_Idle01, _Walk, _Run, _Death, _Dead - alle Abtastzeiten gleich, Modellmatrizen und
  Schluessel jedes alten Knochens Abweichung 0,00e+00; der Kiefer steht in ihnen relativ zum Kopf fest (1e-7).
* Weg 0 in allen Kampfclips, Bip01 still. Kein Bein ueberstreckt (Reichweite hoechstens 0,986).
* Haut ueber den Clip (E, ohne Mundhoehle): Rear bis 1,049 hoch (rund 1,9 m stehend), Slam bis 0,767, sonst wie Idle.
  Tiefster Punkt in allen Kampfclips 0,000 (nichts im Boden).
* Fussgleiten: Hinterpfoten in allen Kampfclips 0; stehende Vorderpfote 0; aufgesetzte Pfoten hoechstens 0,007 Kacheln.
* Dehnung (99,5 %-Wert / Maximum; zum Vergleich Death 2,10 / 4,59): Maul 1,39 / 2,07, Rear 2,50 / 4,79 (Handgelenk),
  Slam 2,91 / 6,17, Hieb 2,92 / 7,32. Lippe und Wange 2,5-3,5 / bis 4,1.
* Angesehen (Skizzen ohne GPU, dann Cycles): Knie beim Stehen gebeugt, Fuesse flach; Schulter hebt beim Ausholen; Kiefer
  oeffnet sauber, Mundwinkel ohne Riss; Maul zu ohne sichtbaren Beutel; keine Pfote gleitet.

## Was unsicher bleibt

1. **Nicht gespielt.** Ob die Knoten spielen und die Blende sauber ist, entscheidet nur Kevins Test.
2. Brust zwischen den Vorderbeinen: das alte Netz gibt ihr Unterarmgewicht; beim Hieb und Slam dehnt sie sich bis 6-7-fach
   (Unterseite, von oben kaum zu sehen). Nicht geaendert, weil sonst Gang und Lauf anders aussaehen.
3. Die Innenseite des gehobenen Arms ist dunkel (gebackene Textur der Achsel), beim Ausholen gut zu sehen.
4. Kurz nach dem Biss (Kiefer 3 Grad) blitzen die Fangzaehne an der Lippe; zu (0 Grad) sind sie verdeckt.
5. Mehrspieler: die Clips sind dieselben; was im MP gespielt wird, entscheidet die Lua-Seite (Spez 3.5).

Statisch geprueft und offline gemessen, nicht gespielt.
