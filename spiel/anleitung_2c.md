# Test fuer Kevin: Lauf baer-2c (10.11.2026)

Statisch und offline geprueft (Renders auf der 4090), **nicht gespielt**. Neu in NCBearTest seit 10.11. 10:37: Netz, Hautgewichte, Texturen und die
drei Sitz-Bewegungen (Hinsetzen, Sitzen, Aufstehen) des Baeren (5 Dateien). Die anderen 12 Bewegungen und der Kopf von aussen sind unveraendert.
Vorher/Nachher: `2c_vorher_nachher.png`. Der Gegenpruefer sagt: in jedem Bild klar besser, aber noch NICHT fertig (drei Punkte am Kopf, unten).

1. Spiel neu starten (Modelle und Texturen laden nur beim Start), dann `NCBear_SpawnLive()`.
2. `NCBear_Sit(20)` aus der normalen Spielkamera: Sitzt er wie auf deiner Vorlage? Kopf oben statt in einer Kapuze? Beine eng?
   Hinterfuesse kurze dunkle Ovale statt Badelatschen? Schaut der Kopf zu sehr nach oben?
3. Hinsetzen und Aufstehen einmal ganz ansehen: fluessig, nichts im Boden?
4. Einmal um den stehenden Baeren laufen (seitlich, hinten): Ist die "Hose in Stiefeln" weg?
5. Gehen und Rennen: Kerbe oder Knick am Knie?
6. `NCBear_AnimTest("rear")`: Zaehne und Zunge beim Bruellen; danach nah an das geschlossene Maul: blitzt unten vorn ein Zahn durch die Lippe?
7. Gab es rote Fehler (ja/nein)?

## Offen -- braucht deine Entscheidung (Belege `2c_gegen_bericht.md`)
- **G1 Buckel hinter dem Kopf:** Der Kragen ringsum ist weg, aber im Sitzen woelbt sich der Buckel noch 2,6-4,2 cm hinter dem Kopf ueber die
  Ohren. 1,5-3 cm tiefer machen oder so lassen?
- **G2 Ring um den Kopf:** Das Fell direkt um den Kopf ist 12 % dunkler als der Kopf, dadurch wirkt der Kopf leicht aufgeklebt. Beheben geht nur,
  wenn die Kopf-Farbe am Rand angepasst werden darf (Kopf-Form bleibt).
- **G3 Blick im Sitzen:** Der Kopf schaut beim Sitzen nach oben; deine Vorlage schaut geradeaus. Kopf im Sitzen geradeaus drehen?
- Kleinkram (nur nah sichtbar): Zahnwurzeln unten vorn sehr knapp unter der Kinnhaut, Knitter am Hinterknie im Gehen, Splitter-Dreiecke in der
  Achsel (fast ganz verdeckt), Maul-Oeffnung kastig mit braunen Lefzen (Lefzen hochziehen geht nur mit der Clip-Runde).
