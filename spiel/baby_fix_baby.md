# Lauf baer-baby: Nachbesserung fix1 (10.11.2026, ~03:45-04:35)

**Statisch/offline gebaut, gemessen und gerendert (RTX 4090, OptiX + Entrauscher, Sperre `gpu.lock`), NICHT gespielt. Nichts eingebaut.**
Grundlage: `pruef_baby.md` (6 major, 7 minor, kein Blocker). Sicherung VORHER: `fix1/vorher/` (alle `*_baby.py`, GLB 129cfc23, PNG
07abcf75, `netz/final.*`, `werkzeug/`, Berichte; MD5 `fix1/vorher/md5.txt`).

**Blatt fuer Kevin (ohne Foto):** `bilder/kevin_baby_entwurf.png` (2300 x 3268; selbst angesehen). Einzelbilder `bilder/fix1/`,
Vorher/Nachher je Befund `bilder/fix1/vorher_nachher.png`. **Nur intern (zeigt die Vorlage, nie weitergeben):**
`referenz/fix1_vergleich_foto_R6.png`, `referenz/fix1_vergleich_foto_R1.png`.

## 0. Kurz

- **Kopf aufgesteckt (M1) behoben:** Kopfschale und Hals sind jetzt EINE verschweisste Flaeche (Loch in der Kopfschale + Naht-Streifen),
  Hals-Ende laeuft tangential in den Kopf, Koerperrand geglaettet; Textur ohne Bruch (gleiches Fell, Hals-Ende = Kopffarbe).
- **Kork-Fell (M2) behoben:** Straehnen jetzt als 3D-Strang-Rauschen (kartenunabhaengig), Koernung nahe am Koerperfell.
- **Augen (M3) behoben:** runder Rand im Ton (Zwangsringe, Kegelwand), kein heller Halbmond mehr, Glanzpunkt sichtbar.
- **Kiefer-Platte (M4) behoben:** nur die Mitte (0,30 W) oeffnet; Lippe dunkel; dazu der vorher unbemerkte gezackte Kinnrand von unten.
- **Translation_Data (M5) behoben:** Berichte berichtigt, Schalter `WEG_FAKTOR` im Export; Wert bleibt x0,777 bis Kevins Wort.
- **Hautdehnung (M6) teilweise:** Ursache mit Gegenprobe belegt (Faktor-Unterschied Rumpf/Beine), Behebung gehoert in 2c/B1.
- Technik weiter gruen: Importer laedt, 26 Knochen gleich, **19.806 Dreiecke**, <= 4 Einfluesse, Summe 1, 0 offene / 0 nicht-mannigfaltige
  Kanten, Boden <= 1,04 cm, Textur 1024 RGB, SPEZ-Masse Kopf/Koerper/Kragen in Toleranz.

## 1. Befunde einzeln

| # | Befund (pruef_baby.md) | Urteil | Was, wo (Datei:Zeile) | Beleg |
|---|---|---|---|---|
| M1 | Kopf aufgesteckt: Kerbe + Fellbruch | **behoben** | `baer_netz_baby.py`: `rand_glaetten` :405 (Koerperrand 6 Runden geglaettet, max 3,3 cm, Nachbarring halb), `hals_loft` :451 (Ende AUF der Kopfflaeche, 0,10 W hinter dem alten Eintritt, Ende-Tangente entlang der Kopfflaeche; Start-Tangente aus der echten Koerper-Normalen; 9 Zeilen statt 5), `schweissen` :654 (198 Kopf-Dreiecke im Hals entfernt, Lochrand 40 Punkte, 72 Naht-Dreiecke, Kopien der Randpunkte mit gleicher Lage -> gemeinsame Normale), Deckel entfaellt. Textur: Hals-Ende = Kopffarbe (`baer_textur_baby.py`:449), gleiches Fell an Kopf/Hals/Koerperrand, Hals-UV-Streifen groesser (ATLAS `baer_netz_baby.py`:763) | Knick Koerper/Hals p90 59,8 -> 23,6 Grad, Median 13,3 -> 10,1 (`fix1/naht.py`); Bilder `bilder/fix1/vorher_nachher.png` Zeilen 1-2, `bilder/fix1/N_nacken_*.png`, Zwischenstand ohne Schweissen `bilder/fix1/beleg_hals_loft_ohne_schweissen.png` (Ringlinie blieb) gegen `beleg_hals_verschweisst.png`; in Eat/Run/Sit ohne Naht (`fix1/r_a8/k_nacken*_ton.png`, `k_sit_ton.png`) |
| M2 | Kopffell fleckig wie Kork | **behoben** | `baer_textur_baby.py`: `straehnen` :186 (47.069 Straehnen auf der Kopfflaeche, Laenge 0,05 W, Breite 0,0028 W, Haarstrich von der Nase weg / Hals zum Koerper / Ohren radial, 13 % helle Spitzen nur am Straehnen-Ende), `fell()` Kontrast 0,45..1,6 -> 1 +- 0,16 x z (:37 FELL_AMP), Kopfgrund waermer (82,62,52) | Hochpass Kopf 8,9 / Koerper 6,6 (vorher 16,0 / 6,3), dunkle Texel L<35 Kopf 0,1 % / Koerper 4,1 % (vorher 9,2 / 3,2) (`fix1/textur_mess.py`, `log/textur_zonen_fix1.txt`); Bild `vorher_nachher.png` letzte Zeile. Zwischenweg LIC im UV verworfen: Naehte an den Kartenraendern |
| M3 | Augen: heller Halbmond, Ton nur gezackte Delle | **behoben** | `baer_netz_baby.py` `augen_ringe` :280 (je Auge 2 geschlossene Zwangsringe a 20 Segmente, rho 0,72 auf dem Augapfel und 1,0 am Rand); `baer_form_baby.py` `augen_loch` :763 Kegelwand 35 Grad (`au_kegel`), Rand weicher (`au_mulde_k` 0,006); Textur: Unterlid (78,68,63) statt (150,150,155), nur unten, <= 0,005 W; Iris (27,22,21); Glanzpunkt in die sichtbare Kappe (:394) | `vorher_nachher.png` Zeile "Auge", `bilder/fix1/A_auge_ton.png` (runde weiche Mulde ohne Zacken-Kerben; der Schattenrand oben ist noch leicht unruhig) und `A_auge_textur.png` (rund, dunkel, Glanzpunkt); Iris-Zone (24,19,17) in Toleranz |
| M4 | Kiefer 0,92 W breite Platte, Entenschnabel | **behoben** (Rest: beim Oeffnen kleine Zacken an der Lippenkante im Ton, `bilder/fix1/E_fressen_ton.png`; in Spielgroesse nicht zu sehen, ungeprueft im Spiel) | `gewichte_kiefer` `baer_netz_baby.py`:883: Jaw-Anteil 1 fuer abs(y) <= 0,11 W, 0 ab 0,20 W (Wangen/Unterkopf bleiben Head), nach hinten ebenso -> Jaw-Gewicht > 0,5 nur auf 0,296 W Breite (132 Punkte voll Jaw, 88 gemischt, 44 Head). Lippe/Unterkiefer-Vorderkante dunkel statt rot, Zunge nur hinten (`baer_textur_baby.py`:383). Dabei gefunden und mit behoben: Kiefer- und Kopfschale lagen ueberall nur 0,002 W auseinander und durchstachen sich -> gezackter Kinnrand von unten (auch vorher, `fix1/r_unten_alt/u_ton.png`): Kiefer jetzt dort 0,012 W tiefer, wo der Kopf nicht geschnitten ist (`kiefer_feld` `baer_form_baby.py`:404, `ki_einzug_verdeckt`), Kinn-Kante als Zwangskante (`kinn_kante` :625) | `vorher_nachher.png` Zeilen "Kinn von unten", "Fressen Ton/Textur"; Schnitte `bilder/fix1/beleg_kiefer_schnitt_vorher.png` / `_fix1.png`; Versuch "Schnitt seitlich begrenzen" verworfen (gezackte Seitenwaende, `fix1/r_a2/`) |
| M5 | Translation_Data x0,777, Bericht sagt unveraendert | **behoben (Wert = Kevins Wort)** | `baer_export_baby.py`:30 `WEG_FAKTOR = "eltern"` (x diag(S_eltern) = 0,777 auf der Laufachse) oder Zahl (1.0 = Weg des Erwachsenen); Log je Clip. `bau_baby.md` :25/:122/:193 berichtigt | `log/export_fix1.log`: Walk 0,378 -> 0,294 E, Run 1,058 -> 0,822 E |
| M6 | Hautdehnung in den Clips | **teilweise** (Ursache belegt, Behebung 2c/B1) | Gegenprobe `fix1/dehnung_faktoren.py` (nur Koerpernetz, gleiche Clips): heute Run p99,5 3,67 / SwipeL 4,41; Beine 0,82 laengs / 0,90 quer -> 2,87 / 3,66; alles gleich 0,88 -> 2,09 / 2,61 = Erwachsener (2,07 / 2,60). Die Dehnung kommt also NUR vom Unterschied Rumpf- zu Bein-Faktor (LBS-Mischterm w_a w_b (T_a-T_b)(A_b-A_a)). Abhilfe heisst: kuerzere Beine aufgeben (gegen Kevins "kurze Beine") ODER Gewichte an Achsel/Leiste neu -- das baut 2c am Koerper ohnehin neu. Nicht angewendet | `log/dehnung_faktoren_fix1.txt`; Clips fix1 `log/clips_fix1.txt` (Koerper wie vorher: Walk 2,90, Run 3,64, Sit 2,69, SwipeL 4,41) |
| m1 | Nacken: Falte mit dunklem Schlitz | **behoben** (mit M1) | erster Hals-Streifen klappte am gezackten Koerperrand um (Knick bis 175 Grad) -> Rand geglaettet, Start exakt am Rand, Glaettung erst nach innen | `naht.py` p90 23,6; Rest: 2 Kanten unten an der Kehle (tier z 0,41 m, von oben nicht sichtbar) |
| m2 | Wangen-Fellzacken fehlen | **abgelehnt (mit Beleg)** | Versuch `wangen_zacken` (`baer_form_baby.py`:371, 3 Zacken, 0,022 W): von vorn kaum sichtbar, von der Seite Querrippen wie Falten, +~250 Dreiecke (Grenze 20.000) -> `wz_amp = 0` | `bilder/fix1/beleg_wangenzacken_a3_ton.png` (oben Mitte: Rippen an der Wange). Lieber spaeter als Textur-Fellkante oder in B1 mit mehr Dreiecken |
| m3 | Beleg Skalier-Schluessel ungenau | **behoben** | `SPEZ_BABY.md` 3.3 Punkt 1 berichtigt (Skalierung wuerde wirken, ist aber 1,0) | -- |
| m4 | Skript-Vorschlag ohne .glb | **behoben** | `bau_baby.md`:156 `mesh = Skinned/NCBearCub.glb` wie `nc_bear_tier.txt:11` | -- |
| m5 | Becken-Hub beim Gehen | **behoben** | `baer_export_baby.py`:25 `BODEN_GLATT = 2` (Bodenausgleich zyklisch geglaettet, nur Schleifen-Clips) | Spannweite Becken-Lage Walk 0,0219 -> 0,0165 E (Erw. 0,0146); Bodenfehler Walk 1,02 / Run 1,04 cm (<= 1,5) |
| m6 | Koerper-Baustellen sichtbar | **offen (Lauf 2c)** | siehe 4. | -- |
| m7 | Ueber dem Auge zu dunkel, Ohren Teddy-Ring | **behoben** | Zone (72,54,46) gegen Soll (73,54,46); Ohren: Rand = Kopffell (nur 35 % Randfarbe), Mulde nur in der Mitte dunkel, Innenhaare hell, Dicke 0,10 W | `log/textur_zonen_fix1.txt`; Bilder R6 |

**Bewusste Abweichungen von SPEZ 4.3 (Kevin bitte bestaetigen):** Unterlid (80,69,64) statt hellgrau (150,150,155) -- sonst wirkt es wie
Augenweiss (Pruefer M3); Ohrrand Fell statt heller Gegenlicht-Rand (146,113,93) -- das Spiel hat kein Gegenlicht. Helle Spitzen weicher
(13 % der Straehnen, Mischung 45 %; Anteil L > 115 nur 2,9 %), weil hellere Spitzen als Sprenkel wirkten (Zwischenstand `fix1/r_b1`).

## 2. Messungen fix1 (alle aus `netz/fix1.npz` bzw. dem Importer-Dump `entwurf/dump_fix1.txt`)

- GLB `entwurf/NCBearCub.glb` MD5 6c3f0a96ba9a2aaf3a06eabc184cdbc3, Textur `entwurf/NCBearCub.png` MD5 2ee25f24c4f0f05bfbb955d4d4b17aea
  (1024 x 1024 RGB). Netz und Textur reproduzierbar (zweiter Lauf bit-gleich).
- Importer (Dump.java): laedt, 26 Knochen, 15 Clips (`log/dump_fix1.log`); `log/pruef_glb_fix1.txt`: Namen/Eltern/Reihenfolge gleich,
  19.806 Dreiecke, 11.970 Punkte, max 4 Einfluesse, Summe 0,99999985..1,00000018, kein NaN, Drehschluessel = Erwachsener (Abw. 0),
  Modellmatrizen Importer/eigene Rechnung 2,6e-5, Lage-Schluessel konstant ausser Becken/Translation_Data. 0 offene, 0 nicht-mannigfaltige
  Kanten (geschweisst 1e-5).
- Dreiecke: Koerper 15.860, Kopf+Hals 3.946 (Kopfschale 1.522+796+270 abzgl. 198, Kiefer 436, Ohren 504, Hals+Naht 616).
- SPEZ 4.1 Foto-Kamera unveraendert in Toleranz (Umriss 0,477, Ohr 0,508, Ohrmitte 0,385, Nase -0,256, Kinn -0,363, W/H 1,200, ...);
  3D: Krone (-0,311/0,340), Nase 0,282, Hinterkopf -0,620, Kopflaenge 0,902, Profil oben 0,014, **Profil unten vorn (x >= -0,2) 0,026**;
  hinter x -0,2 bildet jetzt der verschweisste Hals die Kehle (x -0,4: 0,198 W tiefer als die alte Kugel -- gewollt, kein Hals-Absatz);
  sichtbarer Hals 0,037 L (<= 0,08). Kragen: Stufe 0,0011 L Seite und 3/4 (<= 0,01). Landmarken <= 1,8 mm (`landmarken.json` neu).
  `mess/mess_fix1.json`.
- Koerper 4.4 unveraendert in Toleranz (L 1,857 m, W/L 0,348, Ruecken 0,527, Bauch 0,103, Rumpf B/H 1,02).
- Clips (`log/clips_fix1.txt`): Boden Junges minus Erwachsener alle Clips <= 1,04 cm (Walk/Run durch die Glaettung, sonst 0,0);
  Kopf/Kiefer max sigma 3,5 (Rear/Bite/Maul: Mischzone des Kiefers dehnt sich beim Oeffnen -- gewollt, statt Spalt quer ueber die Wangen).
- Textur-Zonen (`log/textur_zonen_fix1.txt`): alle in Toleranz ausser Unterlid (bewusst, s. o.).

## 3. Weg ins Spiel (empfohlen, NICHT eingebaut)

Wie Vanilla beim Reh (`DeerDefinitions.lua`:7-11, :59, :64) bekommt das Junge eine eigene Art `bearcub` mit eigenem Netz `NCBearCub.glb`
(gleiche 26 Knochen wie `NCBear.glb`) und `animset = "buck"`, Stufe `bearcub` -> `bear`. Die 15 Clips erzeugt `baer_export_baby.py`
per Skript aus den Clips des Erwachsenen (Drehungen byte-gleich, Lagen des Jungen, Boden je Bild), der Spiel-Importer liest sie fehlerfrei.
Dateien wie beim Erwachsenen: `models_X/Skinned/NCBearCub.glb`, `textures/Body/NCBearCub.png`, `animationsMesh`/`model` mit
`mesh = Skinned/NCBearCub.glb` (module Base), spaeter in NPC Crew als `BanditsNPCBearCub*` (Namensprobe 0 Treffer). Beim Wachsen baut
`AnimalData.grow` ein neues `IsoAnimal` ohne `getModData`-Uebergabe (javap 4298-4556), also braucht B1 eine eigene Lua-Naht fuer unsere
Daten. Offen bleiben Kevins Wort zum Weg je Schritt (`WEG_FAKTOR`), die Halbstark-Stufe, `isBaby`-Nebenwirkungen und MP.

## 4. Was am Koerper noch vom Erwachsenen kommt (Lauf 2c behebt es, NICHT dieser Lauf)

1. Hinterfuss wie ein Menschenfuss, im Sitzen Menschen-Sohle (R4, `bilder/fix1/R4_sitzen_*.png`).
2. "Hose in Stiefeln" ueber dem Gelenk (R3 Seite).
3. Rumpf als langes Fass, Rumpf breit.
4. Sitzhaltung (Clip NCBear_Sit des Erwachsenen).
5. Pranken = Erwachsenen-Pfoten x 0,94 (wirken beim Jungen gross), Krallen-Form des Erwachsenen.
6. Koerperfell = Erwachsenen-Textur, auf den Soll-Ton umgefaerbt (Koernung passt jetzt zum Kopf, Muster bleibt das des Erwachsenen).
7. Hautdehnung in schnellen Clips (Run, Swipe, Slam) an Achsel/Leiste/Bauch, siehe M6.
Bei der Uebernahme von 2c: Koerperrand-Schnitt, `rand_glaetten`, `hals_loft` und `schweissen` gegen den neuen Koerper neu laufen lassen.

## 5. Offene Fragen an Kevin

1. Weg je Schritt: 0,777 x Erwachsener (passt zu den kurzen Beinen) oder 1,0 (Weg des Erwachsenen, Fuesse gleiten)?
2. Gesicht: passt der Blick (Augen kleiner als im Foto, dunkler Augenring dezent)? Fell mit hellen Spitzen so oder flauschiger/dunkler?
3. Unterlid dunkel und Ohrrand als Fell (Abweichung von der SPEZ) -- einverstanden?
4. Kurze Beine kosten Hautdehnung: in 2c/B1 Gewichte neu (empfohlen) oder Beine etwas laenger (0,82)?
5. Halbstark (Stufe bis 0,75): Junges- oder Erwachsenen-Modell?

## 6. Dateien, Regeln

- Geaendert: `baer/spiel/baer_form_baby.py`, `baer_netz_baby.py`, `baer_textur_baby.py`, `baer_export_baby.py`; Werkzeuge
  `werkzeug/render_vorbereiten.py` (Kamera "frei", `mitte_y`), `werkzeug/mess_baby.py` (verschweissten Hals mitzaehlen, Profil vorn);
  neu `werkzeug/blatt_kevin_fix1.py`, `fix1/*.py` (Patches, `naht.py`, `schnitt.py`, `teil_blick.py`, `textur_mess.py`,
  `dehnung_schnell.py`, `dehnung_faktoren.py`, `ein_schnell.py`, `kachel.py`). Ungenutzt mitgefuehrt (Schalter aus): LIC (`lic`),
  Kiefer-Seitenschnitt (`ma_breite`), Wangen-Zacken (`wz_amp` 0), Hals-Deckel (nur ohne Schweissen).
- Ergebnis: `netz/fix1.npz` + `netz/fix1.json`, `entwurf/NCBearCub.glb/.png`, `entwurf/dump_fix1.txt(.pkl)`, `render/fix1/` (41 Bilder,
  Posen aus dem NEUEN Importer-Dump). Achtung Lehre: `render/final/ein.json` zeigt mit `dump_jung` auf den alten Dump -- wer sie kopiert,
  rendert in Clip-Posen das ALTE Netz (ist mir passiert, `fix1/r_b1` ungueltig).
- Befehle wie `bau_baby.md` 5, mit `netz/fix1.json`, `netz/fix1.npz`, `dump_fix1.txt`, `render/fix1/ein.json`, dann
  `python werkzeug/blatt_kevin_fix1.py`.
- Regeln: NCBearTest unberuehrt (NCBear.glb weiter 5066fa67, keine neuere Datei), NPC Crew nicht beruehrt, `_arbeit/baer_2c` und
  `*_2c.py` nicht beschrieben (dort neue Dateien stammen vom parallel laufenden Lauf 2c), `*_pfote.py` MD5 gleich
  (`log/md5_fix1.txt`), Vorlage nur von den Blatt-/Mess-Skripten gelesen, kein Commit.
