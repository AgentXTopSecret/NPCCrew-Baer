# Test: Baer K1 -- Vertrauen neu, Schild folgt der Pose, Zahnrad, Inventar 1000, Beduerfnisse nach Groesse -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen. F1 bis F4, Liegen und der Rezept-Fix sind schon drin.
(Entwurf der Nachbesserung 14.11.2026, `k1/NACHBESSERUNG.md`; vom Gegenpruefer berichtigt, `k1/GEGEN.md` Abschnitt 6.) Spiel ist auf Deutsch:
die Texte unten sind die deutschen.

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (vorher und nachher gesichert). Danach das Spiel **neu starten, mit -debug**.
- Erst einen **alten Spielstand** mit gezaehmtem Baeren laden (Teil A), danach einen **neuen Wegwerf-Spielstand**, Mods: **nur NCBearTest**,
  Sandbox alles auf Vorgabe.
- Befehle tippst du in die Lua-Konsole. Leg dir bereit: 10 Steaks, 1 Honig, 2 volle Wasserflaschen, 1 Flasche ungekochtes Wasser.

**Teil A: alter Spielstand -- Vertrauen umgerechnet**
1. Alten Spielstand laden, Baerenfenster (**E**): Vertrauen steht jetzt zwischen -100 und +100 (alt 44 % -> **-12**, roter Balken, rote Zahl).
   Bei negativem Wert ist der leere Teil des Balkens dunkelrot, in der Mitte ein heller Strich (= 0). Spiel speichern, neu laden: Wert bleibt
   gleich (nur einmal umgerechnet).

**Teil B: neuer Spielstand -- Vertrauen gewinnen und verlieren (Junges)**
2. `NCBear_CubClean()`, `NCBear_CubHere(4)`, hingehen, `NCBear_CubTame(100)`. Fenster: Vertrauen **0**, grau.
3. Streicheln -> Meldung "+0,5 Vertrauen: Es hat das Streicheln genossen.", Zahl gruen "+0.5%" (ueber dem Kopf steht dabei "+1" -- siehe
   Frage in GEGEN.md). Gleich noch einmal streicheln: **kein** +0,5.
4. `NCBear_CubNeeds(10, 10, 10, 0)`, dann Rechtsklick Fuettern: neben jedem Futter steht "Macht ihn fuer etwa x % seines Tagesbedarfs satt"
   (Junges: Steak etwa 48 %). Steak fuettern -> "+0,5 Vertrauen: Du hast es satt gefuettert." (Hunger 0 %). Noch ein Steak: "hat keinen Hunger".
   Wasser geben -> "+0,5 Vertrauen: Du hast es satt getraenkt.". Maus auf Vertrauen: "Heute noch moeglich" bzw. "fuer heute verdient".
5. `NCBear_CubTrustDay()` setzt die Tages-Marken zurueck (zum Wiederholen).
6. `NCBear_CubNeeds(89, 10, 10, 0)` und eine Spielstunde warten: Hunger springt ueber 90 % -> Meldung "... vertraut dir weniger (-5)".
   Am selben Tag nicht noch einmal (`NCBear_CubNeeds(89, ...)` noch einmal + eine Stunde: kein zweites -5).
7. Selbst fressen: 2 Steaks und 1 Honig ins Baeren-Inventar legen, `NCBear_CubNeeds(55, 10, 10, 0)`, etwa 30 Spielminuten warten: er frisst
   ab 50 % selbst (ein Stueck je 10 Spielminuten) bis **0 %**, das letzte Stueck ist das kleinste, das noch reicht. Das gibt **kein** +0,5.
8. Ausgewachsen testen: `NCBear_CubGrow(100)` (bis zu einer Minute warten, bis der grosse Baer da ist), `NCBear_CubTrustDay()`,
   `NCBear_CubNeeds(8, 10, 10, 0)`, zwei Steaks fuettern: das erste bringt ihn auf etwa 2 %, das zweite auf **0 %** und gibt "+0,5 ... satt
   gefuettert" (vorher blieb ein grosser Baer zwischen 0 und 5 % haengen -- Fehler C1). Unter 1 % lehnt er ab ("hat keinen Hunger").
9. `NCBear_FightDown()` -> "ging zu Boden ... (-10)". Aufhelfen (Knopf "Aufhelfen" bzw. Rechtsklick "Dem Baeren aufhelfen"), dann noch einmal
   `NCBear_FightDown()`: wieder -10. (Nur wenn du wach und nah bist -- schlaeft du oder bist du ueber 70 Kacheln weg, kostet es nichts; Frage 2.)
10. `NCBear_CubNeeds(nil, nil, nil, -80)`: er weigert sich zu kaempfen (Meldung, Wort "Misstrauisch"). `NCBear_CubNeeds(nil, nil, nil, 100)`:
    Herz ueber dem Namen. Danach `NCBear_CubNeeds(nil, nil, nil, 0)`.

**Teil C: Schild ueber dem Baeren folgt der Pose**
11. Grosser Baer, Namensschild an: `NCBear_AnimTest("rear")` -> Name, Zustand, Lebensbalken heben sich mit dem Kopf und kommen wieder herunter,
    **nie ueber Kopf oder Maul**. Auch `NCBear_AnimTest("slam")`, `NCBear_AnimTest("bite")`, Sitzen (Befehl Sitz). Von hinten (Baer schaut
    von der Kamera weg) beim Biss besonders hinsehen.
12. `NCBear_AnimTest()` ohne Namen: die Liste nennt die acht Schlaf-Namen (liedown, sleep ...) **nicht**; `NCBear_AnimTest("sleep")` spielt
    nichts und sagt, dass die Schlaf-Clips erst mit F3b kommen.
13. `NCBear_TagPose(false)` schaltet das Heben aus (zum Vergleichen), `NCBear_TagPose(true)` wieder an. Dasselbe am Jungen und mit dem
    Aussehen "Braun" (Look-Knopf).

**Teil D: Zahnrad und Anzeige**
14. Baerenfenster: oben rechts neben dem Kreuz ein **Zahnrad**. Klick: Namensschild, **Lebensbalken** (neu), Schaden zeigen, Wachstumszeile
    (nur solange er waechst), Nasen-Warnung **rot** (= kommt spaeter, Vanillas Farbe). Lebensbalken aus -> roter Balken ueber dem Baeren weg.
    Unten im Fenster bleibt nur **Passiv**.
15. Optionen -> Mods -> Hunger/Durst/Muedigkeit ueber dem Baeren auf **Aus** (Vorgabe). `NCBear_CubNeeds(80, 10, 77, 0)` -> ueber ihm steht
    "Hunger 80%" und "Muede 77%" als Zahl, obwohl Aus. `NCBear_CubNeeds(10, 10, 10, 0)` -> wieder weg.
16. `NCBear_CubNeeds(10, 100, 10, 0)`: im Fenster "Nahkampfschaden" **rot**, Maus drauf: Grund ("Durst 100%: 70% des normalen Schadens"),
    sonst/jetzt und je Angriff "(sonst ...)". Muedigkeit allein macht nichts rot. (Durst 100 kostet dabei richtig -5 Vertrauen und etwas Leben.)
    Danach `NCBear_CubNeeds(10, 10, 10, 0)`.

**Teil E: Inventar 1000 + Zahlenfeld**
17. `NCBear_InvItems("Base.Bullets9mm", 500)`. Baeren-Inventar: bei den Patronen **Geben** -> Zahlenfeld "Wie viele gibst du? (1 - ...)",
    vorbelegt mit dem, was passt; 300 eintippen, OK -> EINE kurze Aktion, 300 sind drueben. Eine zu grosse Zahl -> OK grau mit Hinweis.
    **Nehmen** 120 -> Zahlenfeld, eine Aktion. 1 Stueck geht ohne Feld. **Alle** bewegt den ganzen Stapel. Fusszeile ohne "(bis zu 50)".
    Zaehl nach: nichts fehlt, nichts doppelt. (Liegen die Patronen in einer Tasche, holt das Spiel sie vorher Stueck fuer Stueck ins
    Hauptinventar -- das dauert etwas; Frage K-F10.)

**Teil F: selbst trinken, Einfrieren, Mitschlafen**
18. 2 Wasserflaschen + 1 ungekochtes Wasser ins Baeren-Inventar, `NCBear_CubNeeds(10, 55, 10, 0)`, etwa 40 Spielminuten warten (eine Flasche
    je 10 Spielminuten): er trinkt zuerst die **sauberen**, dann das ungekochte; die Flaschen bleiben **leer im Inventar**. Ein grosser Baer
    braucht 15 l fuer die ganze Leiste -- drei Flaschen senken den Durst nur um etwa 20 Punkte (nicht bis 0; bis 0 sieht man am Jungen, dort
    reicht eine Flasche fuer ~67 %).
19. Schlafen gehen (Bett) **oder** vorspulen (>>): der Baer legt sich hin, auch aus Bleiben/Sitz (ist er naeher als 25 Kacheln, kommt er erst
    zu dir); Hunger/Durst/Muedigkeit bleiben stehen (`NCBear_CubNeedsInfo()` zeigt "needs frozen: owner" bzw. "sleep"). Beim Vorspulen
    `NCBear_FightZed(1)` in die Naehe -> er wacht auf und kaempft.
20. Befehl **Bleiben**, dann 71 bis 75 Kacheln weggehen: Werte bleiben stehen (Maus auf Hunger: "Seine Beduerfnisse ruhen: du bist zu weit
    weg"). Noch weiter weg ist er nicht mehr geladen: dann steht der Satz nicht da, die Werte ruhen trotzdem.

**Teil G: Look-Sperre und Deutsch**
21. Wie dein Fall vom 13.11.: neues Junges (`NCBear_CubClean()`, `NCBear_CubHere(4)`, `NCBear_CubTame(100)`), dann `NCBear_CubGrow(55)`;
    sobald der grosse Koerper da ist, sofort den Look-Knopf -> Meldung mit **Grund und Restzeit** ("Dein Baer ist gerade erst gewachsen oder
    hat sich veraendert -- versuch es in xx s noch einmal"). `NCBear_CubLook("gen")` (Testhilfe) geht trotzdem sofort. (Zweimal hintereinander
    der Look-Knopf zeigt dagegen die gemeinsame Uhr mit Unstuck in Minuten -- das ist die alte, richtige Sperre.)
22. Pflege-Knopf heisst **"Heilen"**, Rechtsklick "Baeren heilen" (beim Jungen "Junges heilen").

**Mehrspieler (ungespielt, erst spaeter):** der Baer schlaeft mit, wenn der SERVER dich schlafen sieht (Bett); Vorspulen gibt es dort nicht.

**Bitte melden:** Fehlerzeilen in console.txt, ob das Schild beim Aufrichten gut sitzt (jetzt naeher am Kopf als vorher), und die Fragen in
`k1/GEGEN.md` (Abschnitt Fragen fuer Kevin).
