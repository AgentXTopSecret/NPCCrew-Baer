# Tonschnitt Baer (NC Bear Test) - Stand 08.11.2026

**Statisch geprueft, nicht gehoert.** Die Stuecke sind ueber Lautstaerke-Huellkurve und Spektrum gewaehlt (je Datei ein
Spektrogramm `schnitt_<Name>.png` hier im Ordner, alle angesehen). Ob sie im Spiel wie ein Baer klingen, entscheidet erst Kevins Ohr.

Erzeugt von `schnitt.py` (wiederholbar: zweiter Lauf byte-gleich, Dither mit festem Samen je Datei).
Ausgabe: `...\_arbeit\baer_kampf\mod\42\media\sound\` (Vorgabe im Skript), anderer Ordner mit `--out ORDNER`.

## Liste

| Datei | Quelle | Sekunde von - bis | Laenge | Spitze | rms95 | Was es ist |
|---|---|---|---|---|---|---|
| NCBear_Roar.wav   | soundbible_242.wav | 11,08 - 12,26 | 1,18 s | -4,5 dBFS | -11,0 dBFS | lautester Ruf der Aufnahme: Stoss 11,13-11,92 mit Ausklang; seit 08.11. (Fixer) ohne den zweiten Stoss 12,28-13,00, der im Clip bei geschlossenem Maul lag (`spiel/kampf_fix.md`) |
| NCBear_Growl1.wav | soundbible_242.wav | 14,86 - 15,92 | 1,06 s | -3,7 dBFS | -12,0 dBFS | einzelner Stoss 14,90-15,85, endet natuerlich |
| NCBear_Growl2.wav | soundbible_242.wav | 16,29 - 17,28 | 0,99 s | -3,8 dBFS | -12,0 dBFS | einzelner Stoss 16,32-17,18, harter Einsatz |
| NCBear_Growl3.wav | soundbible_242.wav | 19,37 - 20,42 | 1,05 s | -1,3 dBFS | -12,0 dBFS | einzelner Stoss 19,41-20,37, hellster der drei |
| NCBear_Pain.wav   | soundbible_241.wav | 2,91 - 3,56   | 0,65 s | -8,1 dBFS | -13,0 dBFS | tonaler Klagelaut um 490 Hz (kein Knurren), als Schmerzlaut gedacht |
| NCBear_Huff.wav   | soundbible_868.wav | 3,165 - 3,37  | 0,21 s | -7,8 dBFS | -20,0 dBFS | Atemstoss 3,16-3,31, leise gepegelt - **Kandidat, siehe unten** |

Alle: Mono, 44,1 kHz, 16 Bit (wie Vanillas `media/sound/fzombierand5.wav`), keine Vollaussteuerung (Spitze <= -1 dBFS),
Gleichanteil unter 1 LSB, erster und letzter Abtastwert 0 bzw. 1 LSB (Ein-/Ausblenden als Kosinus: 10-20 ms ein, 60-100 ms aus).

Herkunft und Lizenz: `roh/QUELLEN.txt` - soundbible.com, Public Domain (fws.gov: 241, 242; nps.gov: 868), mit Kevins Freigabe am 07.11.

## Bearbeitung (je Datei, in dieser Reihenfolge)

1. Mono: 241 und 242 sind Doppel-Mono (beide Kanaele identisch, Korrelation 1,000), 868 ist Mono.
2. Nur Huff: Vollaussteuerung reparieren (868 hat 9 Abtastwerte bei 3,288 s an 0,99-1,00; ersetzt durch ein kubisches Polynom aus
   je 8 Nachbarn) und Obertonsperre: je STFT-Fenster wird der Grundton des Jungtier-Summens (gesucht 380-520 Hz) gefunden und jede
   Obertonlinie k*f0 (bis 10.) in +-32 Hz um 20 dB gedaempft; Fenster ohne deutliche Linie bleiben unberuehrt (117 von 147 Fenstern gesperrt).
3. Filter nullphasig ueber die FFT (Butterworth-Betrag): 241/242 Hochpass 110 Hz 4. Ordnung, Tiefpass 7 kHz 2. Ordnung;
   Huff Hochpass 120 Hz 2. Ordnung, Tiefpass 6 kHz 2. Ordnung.
4. 241/242 von 48 kHz auf 44,1 kHz umgetastet (FFT, bandbegrenzt).
5. Ein-/Ausblenden, Pegel auf rms95 (95. Perzentil der 50-ms-Fenster) angeglichen, Spitze auf -1 dBFS gedeckelt (griff bei keiner Datei),
   TPDF-Dither +-1 LSB, 16 Bit.

Pegel-Bezug Vanilla (gemessen): fzombiehit1-5 und fzombierand1, PZ_DogBark1/2, PZ_DogBark_Whimper1 haben Spitze -0,2 bis -2,6 dBFS und
rms95 -8 bis -13 dBFS. Bruellen -11, Knurren -12, Schmerz -13 liegen darin; das Schnauben ist mit -20 bewusst leise.

## Warum diese Stellen - und was NICHT genommen wurde

- **242, 0 - 10,8 s nicht benutzt:** durchgehend breitbandiges Rauschen 40 Hz - 5 kHz mit starken Stoessen unter 200 Hz (Wind am
  Mikrofon). Ab 10,8 s ist die Pause zwischen den Rufen ueber 250 Hz dunkel (-40 bis -48 dBFS), die Rufe stehen dort 15-20 dB darueber.
- **Hochpass 110 Hz:** Bandvergleich Ruf gegen Pause in 242: unter 100 Hz nur 8-11 dB Abstand (Wind), 125-200 Hz 9-17 dB (Koerper des
  Rufs, bleibt), 400-1000 Hz 17-22 dB. In 241 genauso (50-63 Hz 0-5 dB, 500 Hz 27 dB).
- **241** ist leiser (Spitze der Rohdatei 0,13) und hat mehr Grundrauschen; sein sauberster Ruf (2,95-3,50, fast reiner Ton um 490 Hz mit
  Obertonen) klingt nach Klage, nicht nach Knurren - deshalb Schmerzlaut.
- **868 ("Bear And Bear Cubs") hat kein sauberes Schnauben einer Baerin.** Darin sind fast nur tonale Summ-Laute von Jungtieren
  (Grundton 410-480 Hz mit Obertonreihe) und kurze Klicks (5-ms-Spitzen bei 4,00 / 4,34-4,44 / 4,65 s, Schmatzen oder Kiefer).
  Der einzige kraeftige Atemstoss ist 3,16-3,31 s: Hauptenergie 60-150 Hz, dazu breitbandiges Rauschen 300-1500 Hz, das zwischen den
  Obertonlinien 17 dB ueber dem Summen allein liegt. Genau dort setzt aber auch ein Jungtier-Summen ein - daher die Obertonsperre.
  Nach der Sperre springt der Stoss in rund 10 ms auf -23 dBFS und erreicht seine Spitze nach weiteren 40 ms, dann klingt er ueber
  rund 100 ms ab. Ob es ein Ausatmen der Baerin oder ein Stoss ans Mikrofon ist, laesst sich aus Bildern nicht sicher sagen (das
  breitbandige Rauschen ueber 100 ms spricht eher fuer Atem). **Beim Hoeren pruefen; taugt es nicht, Huff weglassen.**
- Die leisen Rauschstellen am Ende von 868 (5,93-6,2 s) liegen nur wenige dB ueber dem Grundrauschen - zu schwach.

## Was Kevin hoeren soll

- Klingt Roar (jetzt nur der erste Stoss, 1,18 s) kraeftig genug, und endet er nicht zu abrupt?
- Klingt Growl1-3 nach Knurren/Angriff, oder zu "bloekend"? (Alle drei aus derselben Rufserie, aehnliche Formanten 500 / 1000-1200 / 1600 Hz.)
- Pain: Klage oder eher Muh?
- Huff: Schnauben oder dumpfer Stoss? Hoert man noch das Summen des Jungtiers?

## Einbinden (nicht Teil dieses Schnitts)

Vanillas Form fuer eine lose wav: `sound <Name> { category = ..., clip { file = media/sound/<datei>.wav, distanceMax = 100, } }`
(`media/scripts/generated/sounds/zombies/sounds_zombie_voice_tutorial.txt:3-11`). Prankenhieb-Wusch und Treffer kommen laut Auftrag
aus vorhandenen Spieltoenen, nicht aus diesem Schnitt.
