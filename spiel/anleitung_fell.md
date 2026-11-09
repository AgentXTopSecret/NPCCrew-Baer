# Test fuer Kevin: Lauf baer-fell (09.11.2026)

Statisch und offline geprueft (Renders auf der 4090), **nicht gespielt**. Neu in NCBearTest: Netz, Hautgewichte und Texturen des Baeren
(5 Dateien). Bewegungen (alle 15 Clips) und Kopf sind unveraendert. Vorher/Nachher: `fell_vorher_nachher.png`.

1. Spiel neu starten (Modelle und Texturen laden nur beim Start), dann `NCBear_SpawnLive()` eingeben.
2. `NCBear_AnimTest("rear")`: Brust und Bauch hell, keine Hautlappen, kein heller Streifen innen an den Beinen?
3. `NCBear_Sit()`: Die Hinterpfote zeigt eine graue Sohle mit Ballen statt eines schwarzen Lochs. Ist dir das Grau zu hell?
4. `NCBear_AnimTest("swipeR")` und `NCBear_AnimTest("slam")`: reisst oder knickt es an Achsel, Brust oder Knie?
5. Von hinten ansehen: Ist das Fell kraeftiger und gut so, oder wirkt das Hinterteil fleckig oder grau?
6. `NCBear_SpawnLive("bearstag")` (Rueckfall mit Reh-Bewegung): Sitzt das Fell richtig? Gab es rote Fehler (ja/nein)?

Noch offen (dein Wort): Zotteln am Umriss (als Netz verworfen: sahen aus wie Noppen), Form der Vorderpranken (Schaufel), Gesaessfalte nur
schwach, Kopf-Variante mit sichtbaren Augen (`_arbeit/baer_fell/textur/NCBear_kopf_variante*.png`), eigenes Baby-Modell
(`_arbeit/baer_fell/baby/baby_vergleich.png`). Berichte: `fell_*.md` hier im Ordner.
