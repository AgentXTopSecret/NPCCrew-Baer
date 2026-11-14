# GEGENPRUEFER -- Lauf baer-gen-rear-bauch (14.11.2026)

**Statisch geprueft und selbst gerendert, nicht gespielt.** Geschrieben nur `gegen/` (Werkzeuge, Dumps, Auftraege, Renders, Messungen, Nachbau),
`bilder/KEVIN_gen_rear_bauch.png` und diese Datei. Test-Mod, NPC Crew, Spiel, `out/` nur gelesen; Eingaenge vorher und nachher gleich
(NCBear.glb dc50d350, NCBearGen.glb 867b558b, NCBear.png 5a841f0c, NCBearGen.png 1fe9c54b, NCBearGenFoto.png 29c3c7d7, TagPose.lua bd95570b).
Kein git, kein Download. Renders nur RTX 4090 (OptiX, Log `BILD Geraete ['NVIDIA GeForce RTX 4090']`) ueber `werkzeug/gpu_render.sh`; `gpu.lock` frei.

## Urteil

**Einbaubar, kein Blocker, kein Major. Schoen genug fuer Kevin: ja.**
- **A Generator-Bruellen:** Der Generator-Baer richtet sich jetzt so auf wie der braune Baer in Kevins rechtem Bild (aufrecht, Kopf hoch, Maul
  weit offen, Pranken vor der Brust statt "Fluegel"), in Brown und Natural, aus allen fuenf Blickrichtungen. Hals/Kehle heil, kein Durchstossen
  zu sehen, Kopf/Gesicht/Augen gleich. Einziger Unterschied zum braunen Baeren: Arme 14 Grad weiter vor (F1).
- **B Bauch-Fell:** Brust, Bauch und Innenschenkel zeigen Straehnen statt der glatten, verwaschenen Platte -- beim Aufrichten von vorn und im
  Liegen deutlich. Keine Naht, keine Kante, Farbe passt; Kopf/Gesicht/Augen, Ruecken, Pfoten unveraendert. In Kevins normaler Spielgroesse
  (1080p) ist der Unterschied klein, nah und in 4K klar.

## 1. Eigene Pruefungen (eigene Werkzeuge in `gegen/werkzeug/`, Ergebnisse `gegen/mess/`)

| Pruefung | Weg | Ergebnis |
|---|---|---|
| out/md5.txt | `md5sum -c` | beide OK (8fe40125 / 3493a5e6) |
| A nur Rear (Importer) | eigene Dumps mit `werkzeug/dump.sh` (Dump.java), `glb_pruef.py` ALT gegen NEU (`glb_pruef_alt_neu.txt`) | 26 Knochen, Namen/Eltern gleich, Offset/Bind max 0,0; **14 Clips Abweichung 0**; NCBear_Rear 3,0000 s, 91/91 Abtastungen gleich. Dumps byte-gleich mit denen des Optik-Pruefers |
| A nur Rear (Bytes) | **eigenes** `g_glb_bytes.py` (`g_glb_bytes.txt`, `g_interp.txt`) | JSON byte-gleich; 24 104 BIN-Bytes anders, **alle in den 22 Ausgabe-Accessoren von NCBear_Rear**, keiner davon mit anderem Clip/Netz geteilt; Netz/Skin-Accessoren und 708 Accessoren anderer Clips byte-gleich; Rear-Zeiten NEU = ALT = Klassisch bit-gleich, Interpolation und Bildzahl je Kanal = Klassisch; gegen Klassisch nur `Bip01_L/R_UpperArm` anders, Bild 9..73, max 16,11 Grad (= 14/8) |
| A Name/Dauer | Test-Mod `AnimSets/buck/idle/NCBear_Rear.xml` (`m_AnimName NCBear_Rear`), `shared/BanditsNPCBearFightRules.lua:65` (`rear = { dur = 3.00 }`) | passen (Name und 3,0 s unveraendert) |
| A Kopfhoehe | `k1/werkzeug_plan/kopfhoehe.py` (`kopfhoehe_g.txt`) | Generator gross Rear **1,750 -> 1,832** (bei 1,27 s); Klassisch 1,881 |
| A Schild-Tabelle | `tagpose_schirm.py` mit dem WIEDERHOLEN-Befehl nach `gegen/mess/tagpose_g.lua` | MD5 0a8c61e7 = `gen_rear/mess/tagpose_v1.lua`; diff zur Test-Mod nur **Zeile 62** `biggen.rear` (max 1,56 -> 1,61) |
| B nur Bauch (Texel) | **eigenes** `g_png_diff.py` + `g_png_kopf.py` (UV-Dreiecke aus dem Dump, fuehrender Knochen je Dreieck) | PNG-Bloecke ausser IDAT byte-gleich, 1024x1024 RGB 8 bit; 164 354 Texel anders (116 405 Netz + 47 949 Polster), 79,7 % mit Normale nach unten, Ruecken (Normale oben) 229 von 214 331; **Head+Jaw-Dreiecke: 0 Texel anders**, kein geaenderter Texel direkt neben einem Kopf-Texel (Abstand 1: 0); Pfote/Schwanz > 0,6: 0 (> 0,4: die 204 Texel aus T7, max 41) |
| B Kopf im Bild | Render Kopf ALT/NEU-Textur ohne Entrauscher, gleicher Samen, Kopf-Maske als Feld (`g_kopf_render.txt`) | Kopf innen 2 bzw. 4 Pixel um 1 Stufe anders (Rauschen), Rand max 6/17 (Nachbar-Pixel der Brust) -> **Gesicht/Augen gleich** |
| Wiederholbar | beide WIEDERHOLEN-Befehle nach `gegen/wdh/` | **8fe40125 und 3493a5e6 byte-gleich** (27 s / 91 s); B auf dem eigenen Ergebnis -> `BAUCHFELL_SCHON`, Code 0, gleiche MD5 |
| Durchstossen (Versuch) | eigene Strahl-Paritaet `g_durch.py` (`g_durch_*.txt`) | **nicht aussagekraeftig**: das Netz ist nicht geschlossen, auch der alte Generator (Arme weit vom Rumpf) hat 3-49 Kandidaten je Seite; NEU liegt im selben Bereich wie ALT und Klassisch. Beleg fuer A3 bleiben die Messungen der Bauer/des Technik-Pruefers und meine TON-Bilder |

## 2. Eigene Bilder (alle selbst angesehen)

Renders `gegen/render/{gen_alt,gen_neu,klass,x_*}/` (Auftraege `gegen/auftrag/`, Erzeuger `g_auftrag.py`), Seh-Blaetter `gegen/bilder/_sicht_*.png`.
- **Generator, Kevins Kamera** (az 0/50/90/180/270, Hoehe 30, Spielgroesse neben 1,8-m-Figur, Bild 38 und 64, Brown + Natural): NEU = Pose des
  braunen Baeren; ALT hatte die waagerechten "Fluegel".
- **Generator von vorn nah** (Hoehe 30 und 8, Bild 21/38/64/77): Pranken haengen vor Brust/Bauch, verschmelzen farblich mit dem dunklen Fell.
- **TON** (vorn/az 40/Seite, Bild 21-77; Hals ganz nah Bild 30/36/38/46): kein Riss am Hals, keine Pranke im Rumpf; Faltenlinien an Schulter,
  Ellbogen und ein duenner Ring am Unterarm (auch ALT/Klassisch haben solche Falten) -- mit Textur in keinem Blick zu sehen (`_sicht_x_zoom.png`).
- **Klassisch-Bauch** ALT/NEU 1024 und 256: Aufrichten 4K-Massstab, ganz nah (Hoehe 8, az 30), Liegen az 90/50/270 und von unten, ganz nah;
  Sitzen/Stehen praktisch gleich (Sitzen: Brust etwas felliger, F3); Ruecken/Kopf gleich.
- Massstab: meine Renders sind heller als Kevins Spielbild des Generators (Licht-Nachbau), fuer ALT und NEU gleich -- kein Modellfehler.

**Blatt fuer Kevin:** `bilder/KEVIN_gen_rear_bauch.png` (2700 x 3941): oben A -- Kevins zwei Spielbilder, Generator ALT/NEU von vorn (Brown,
Natural, fast Bodenhoehe), Kevins Kamera 5 Blicke ALT/NEU mit Figur, Bildfolge 0-3 s ALT/NEU; unten B -- Kevins Bauch-Bild, Bruellen 4K ALT/NEU,
Brust/Bauch ganz nah ALT/NEU, Liegen ALT/NEU (ganz und nah), Sitzen/Stehen/Kopf/Kamera 50 Grad ALT/NEU; Zahlen unten. Erzeuger `gegen/werkzeug/g_blatt.py`.

## 3. Befunde (alle minor, keiner verlangt eine Nachbesserung vor dem Einbau)

- **G1 (A, = F1):** Arme 14/8 statt Klassisch-Werten -> Unterarme von vorn leicht V-foermig, von der Seite etwas weiter vorn. Wirkt natuerlich.
- **G2 (A):** TON-Falten an Schulter/Ellbogen/Unterarm (wie ALT und Klassisch, Befunde O3/T4); mit Textur unsichtbar.
- **G3 (A):** Eigene Durchstoss-Probe ohne Aussage (s. 1); kein Widerspruch zu A3, aber auch kein unabhaengiger Zahlenbeweis.
- **G4 (B):** Straehnen etwas laenger/welliger als am Ruecken, im oberen Bauch teils quer; der hellere Laengsstreifen ("Latz") bleibt (Kevin: "der rest soll so bleiben", O4).
- **G5 (B):** B4b nicht jeder Nahtpunkt <= 3 (92,9 %, ALT 90,7 %); im Bild keine Naht.
- **G6 (B):** Bei normaler Spielgroesse 1080p ist der Gewinn klein (Bauch nur beim Aufrichten/Liegen sichtbar); nah/4K deutlich.
- **G7 (Doku):** `bilder/KEVIN_gen_rear_bauch.png` zeigt Brown; Natural nur in Reihe 1 (Generator NEU Natural) -- beide gleich gut.

## 4. Fuer den Integrator

- Einbau nur auf Kevins Wort und nur wenn NCBearTest nicht geladen ist: `out/42/media/models_X/Skinned/NCBearGen.glb` (8fe40125) und
  `out/42/media/textures/Body/NCBear.png` (3493a5e6); **dazu Zeile 62 von `shared/BanditsNPCBearTagPose.lua`** aus `gen_rear/mess/tagpose_v1.lua`
  (F6, Vorgabe ja) -- NCBearGen.glb und diese Zeile nur zusammen. Nichts sonst.
- Git: `baer/spiel/baer_genrear_1114.py` (1cb07ba0) und `baer_bauch_1114.py` (7725e38e) sind seit db1b171 geaendert -> neu committen;
  `NAEHTE.md` im Arbeitsbaum ist von einem anderen Lauf -> nicht ungesehen mitcommitten.
- Kevin zeigen: `bilder/KEVIN_gen_rear_bauch.png`. Nach dem Einbau Spiel neu starten.

## 5. Fragen fuer Kevin (Vorgabe gilt bis zur Antwort)

- F1: Generator-Arme 14 Grad weiter vor als beim braunen Baeren (sonst stecken die Pranken in der dickeren Brust) -- ok?
- F6: Namensschild-Tabelle beim Einbau mitziehen (Generator Bruellen 1,56 -> 1,61)? Vorgabe ja.
- F2: Kehle direkt unter dem Maul bleibt altes Fell (gehoert zum Kopf) -- auch neu machen?
- B-F6: Fell-Staerke wie am Ruecken -- zu unruhig oder zu schwach?
- (F3 Brust im Sitzen etwas felliger, F4 Krallen bei 256, F5 Bodenmodell alt: Vorgaben so lassen.)

## 6. Kevins Test (nach dem Einbau, Spiel neu starten, -debug, Einzelspieler)

1. Gezaehmten grossen Baeren holen, `NCBear_CubLook("gen")`, dann `NCBear_AnimTest("rear")`: bruellt wie der braune, Pranken vor der Brust.
2. `NCBear_CubLook("foto")`, wieder `NCBear_AnimTest("rear")`.
3. `NCBear_CubLook("std")`, `NCBear_AnimTest("rear")`: Brust/Bauch Fell statt Matsch, Kopf/Augen wie vorher.
4. Schild steht beim Bruellen ueber dem Kopf (nur mit Zeile 62).
5. Faellt was auf: Bild mit rotem Kreis.
