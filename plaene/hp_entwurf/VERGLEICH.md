# Lebensanzeige über dem Bären: Vorlagen A / B / C im Vergleich (ENTWURF)

Lauf `baer-hp-entwurf`, 14.11.2026. Nur Entwurfsbilder, kein Mod-Code. Alles ist statisch gezeichnet und wurde nicht gespielt.
Vergleichsbilder: `KEVIN_hp_vorlagen.png` (1080p, Schrift 1x), `KEVIN_hp_vorlagen_4k.png` (4K, Schrift 4x, wie bei Kevin),
`KEVIN_hp_vorlagen.gif` (alle drei nebeneinander: Heilen, Treffer, Hunger, 4K-Pixel 1:1, 8,8 s).
Gezeichnet hat sie `vergleich.py`. Das Skript nutzt die `zeichne.py` der drei Vorlagen selbst. Alle drei stehen an derselben Stelle über
den Ohren, im selben Maßstab und mit denselben Zustandszeilen, über Kevins Bild `kevin_rear_bauch_1113.webp`.

## A „Schlicht-Klar“
- **Stärke:** am ruhigsten und am klarsten lesbar, stört das Bild am wenigsten. Die Farbe läuft fließend. Treffer (weißer Blitz, dann ein heller Nachlauf), Hunger (langsames Rot mit Keule bzw. Tropfen) und fast leer (Herzschlag-Glut) sind gut auseinanderzuhalten. Die Zahl ist optional.
- **Schwäche:** am wenigsten besonders, wirkt wie ein normaler Spielbalken. Symbole (14 px bei 1080p) und Heil-Schimmer sind klein und leise. Heilen sieht man vor allem am Plus.
- **Aufwand:** kleinster Bau, eine eigene Client-Datei (~200-250 Zeilen). Ein Skript erzeugt die kleinen PNGs. Neu ist die Option „Balken + Zahl“ (Text in 8 Sprachen), am Server optional ~6 Zeilen. Ruhig 18 Aufrufe je Schild, höchstens 31; der Deckel steigt von 25 auf 49.

## B „Rollenspiel“
- **Stärke:** am meisten Spielgefühl. Die Bronze-Plakette mit Pfote und 10 Teilen, die Zahl „352/400“ ist immer sichtbar, und die schwebenden „+12“ / „-28“ / „-4“ zeigen genau, was gerade passiert. Die vier Farbstufen passen zu den Teilen.
- **Schwäche:** der größte Block (bei Kevin ~250 × 48 px, mit Name ~250 × 125). Er wirkt unruhiger, und bei mehreren Bären wird es voll. Die Zahl liegt über den Teil-Strichen und ist auf Gelb schwächer im Kontrast. Die genaue „-28“ geht erst mit einem neuen Server-Feld.
- **Aufwand:** mittlerer Bau mit einer neuen Datei (~250-350 Zeilen) und 22 Bildern. Am Server 1 Zeile (`fx.pts`), optional ~10 (`hpR`). Die meisten Zeichenaufrufe: ruhig 29, im Effekt bis 58, der Deckel steigt von 25 auf ~60.

## C „Modern-Rund“
- **Stärke:** am schönsten und modernsten. Kapsel mit Leuchtrand, Herz-Medaillon und fließender Farbe. Die Effekte fallen am meisten auf: grüner Glow mit „+“, Splitter mit Wackeln, dunkles „Ausfließen“ mit dem echten Vanilla-Symbol für Hunger bzw. Durst, und das Herz schlägt doppelt.
- **Schwäche:** keine Zahl, und die Füllung wächst von der Mitte aus. Unter ~20 % sieht man nur noch Stummel neben dem Herz, der genaue Wert ist schwer abzulesen. Das Lebens-Herz ähnelt dem Vertrauens-Herz. Das Hunger-Symbol ist im ruhigen Takt klein und dunkel.
- **Aufwand:** mittlerer Bau, nur Client (~200-250 Zeilen) und 26 kleine PNGs je Größenstufe. Der Server braucht nichts (optional `hp` im Ereignis „hurt“). Ruhig 29 Aufrufe, bis 41; der Deckel steigt von 25 auf ~45. Die Größe sollte an der Schrifthöhe hängen wie bei A und B, nicht an der Bildschirmhöhe.

## Geprüft, behoben, für alle gleich
- **Behoben (C):** Das 4K-Bild, die Effekt-Tafel und die GIFs waren mit Schrift 2x gezeichnet. Kevin spielt aber mit 4x: „Bär von Dee“ misst in seinem Bild 138-140 px, 4x Small hat 143 px (gemessen von A und B). Ich habe `C/zeichne.py` auf 4x umgestellt und neu gezeichnet. Die alte Fassung liegt in `C/_alt_schrift2x/`.
- **Korrigiert (C):** C behauptet, der Client merke das Einfrieren nicht. Das stimmt nicht, die Sicht trägt `nfz` (`server/BanditsNPCBearNeeds.lua:647`). Das Feld `stv` ist darum unnötig; das steht jetzt in `C/BESCHREIBUNG.md`.
- **Spiel-machbar sind alle drei:** Sie brauchen nur `drawRect`, `drawTextureScaled` und `drawText`/`drawTextCentre`, also keinen Shader. Nachgelesen: Vanilla `ISUIElement.lua:1191` / `:1280` und `ISChat.lua:418`. Heute steht der Deckel bei 25 Aufrufen je Schild (`BanditsNPCBearHud.lua:53`). Der Balken ist fest 64 × 7 px (`BAR_W`/`BAR_H`) und darum bei Kevin in 4K so winzig. `hpMax` ist in der Sicht (`server/BanditsNPCBearGrow.lua:969`).
- **Treffer:** Der Zeitpunkt kommt sofort über das Ereignis „hurt“, aber ohne Lebenswert (`server/BanditsNPCBearHurt.lua:104-105`). Das neue Leben kommt erst mit der nächsten Sicht, im Kampf nach bis zu ~2 s. Alle drei wollen dafür ein Feld im Ereignis „hurt“ (A `fx.hp`, B `fx.pts`, C `hp`). Jede Vorlage braucht nur dieses eine Feld. B will die Punkte; aus dem Prozentwert ginge es nur auf ~1 % genau.
- **Hunger/Durst** geht bei allen ohne neues Feld: `hun` oder `thr` = 100, dazu kein `nfz`, kein `dn` und `hp` > 1. **Heilen** kommt als Schub, weil das Leben höchstens einmal je Spielstunde festgeschrieben wird. Verband (`bnd`) und Schlaf (`slp`) sieht der Client sofort.
- Die Bilder habe ich angesehen, abgeschnittene Schrift gibt es keine. Ins GIF habe ich jedes Bild zurückgelesen und gegengeprüft: 0 Abweichungen.

**Kurz:** A ist am ruhigsten und hat das geringste Risiko, B zeigt die meisten Infos, C ist am schönsten. Eine Mischung geht auch, z. B. die
Kapsel von C mit Füllung von links und Zahl wie bei A. Die Wahl trifft Kevin.
