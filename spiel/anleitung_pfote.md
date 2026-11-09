# Test fuer Kevin: Lauf baer-pfoten (09./10.11.2026)

Statisch und offline geprueft (Renders auf der 4090), **nicht gespielt**. Neu in NCBearTest seit 10.11. 00:04: Netz, Hautgewichte und
Texturen des Baeren (5 Dateien). Alle 15 Bewegungen und der Kopf sind unveraendert. Vorher/Nachher: `pfote_vorher_nachher.png`.

1. Spiel neu starten (Modelle und Texturen laden nur beim Start), dann `NCBear_SpawnLive()` eingeben.
2. Einmal um den Baeren laufen: Pfoten von der Seite, von vorn, von hinten -- echte Pfote oder noch Saeule?
3. `NCBear_Sit(20)`: Der Hinterfuss zeigt eine lange Sohle, Ferse unten, Zehen oben.
4. `NCBear_AnimTest("rear")`: Er steht auf den ganzen Hinterfuessen.
5. Gehen und Rennen: Sieht der Fussaufsatz richtig aus?
6. Gab es rote Fehler (ja/nein)?

Bekannte Schwaeche (Bild `pfote_kegel.png`): Ueber dem Gelenk wird das Bein auf kurzer Strecke wieder dick ("Glocke", von hinten wie
Hose im Stiefel). Der Lauf durfte das Bein nur unter 36 cm aendern; die ganzen Beine kommen im naechsten Lauf (2c: Gebiss, Zunge, Beine).
Nur per Clip-Runde zu beheben: Pranke beim Aufrichten von vorn klotzig, Hinterfuss im Renn-Rueckschwung schmal.
Berichte: `pfote_*.md` hier im Ordner.
