# Test: Baer F4 -- eigenes Inventar, Load, Packtaschen, selbst fressen -- Einzelspieler

Statisch geprueft, nicht gespielt. Ich lasse den Fehlerwaechter mitlaufen. F1 bis F3, Deutsch und der Aussehen-Knopf sind schon drin.
(Entwurf der Nachbesserung 13.11.2026 spaet, vom Gegenpruefer gegen den Code abgeglichen und berichtigt: f4/GEGEN.md.)

**Vorher**
- Ich kopiere erst, wenn dein Spiel zu ist (vorher und nachher gesichert). Danach das Spiel **neu starten, mit -debug**.
- **Neuer Wegwerf-Spielstand**, Mods: **nur NCBearTest**. Sandbox-Seite "NPC Crew": jetzt **14** Baeren-Optionen, neu
  **"Bear: carrying capacity (percent)"** (100). Alles auf Vorgabe lassen.
- Befehle tippst du in die Lua-Konsole. Gegenstaende holst du aus der Debug-Itemliste. Leg dir bereit: 1 Apfel, 5 Naegel, eine **halb
  volle** Wasserflasche, eine Axt, eine **geladene** Pistole mit Rotpunkt-Visier, ein Hemd mit Blut, eine Karte, einen vollen Rucksack,
  einen Fisch, ein Brett, **Bear Packs** (Debug-Itemliste "Bear Packs").

**Teil A: Fenster und Load**
1. `NCBear_CubClean()`, `NCBear_CubHere(4)`, hingehen, `NCBear_CubTame(100)`, `NCBear_CubFood()`.
2. **E**: in der Karte Condition steht jetzt **"Load 0.0 / 10 kg"** (statt "Can carry"; der Wert waechst mit dem Jungen). Maus drauf: Tooltip "What your **cub** carries
   now ..." mit 10 / 40 / 100 kg. Der Knopf **Inventory** ist **scharf**.
3. **Inventory** klicken: Fenster "Inventory: <Name>", links "Your cub carries" ("Nothing in here yet."), rechts "You carry" (dein Inventar
   samt Taschen), oben "Load" mit Balken und "0 / 1000 things". Rechtsklick am Jungen hat auch **"Open its inventory"**.

**Teil B: Geben und Nehmen (daneben stehen)**
4. Gib nacheinander: Apfel, Naegel (**All** = alle 5 in einem Stapel), Wasserflasche, Axt, Pistole, Hemd. Je kurze Handbewegung, Meldung
   "Packed: ...". Links stehen sie **nach Namen geordnet**, Maus auf eine Zeile: Gewicht, Zustand, Fuellung, Frische. Ein Nagel zeigt
   "0.01 kg" (nicht "0.0 kg"). Bekannt: frisches Essen stapelt beim Baeren nicht -- gibst du 3 Aepfel, stehen links 3 Zeilen "Apple"
   (Dosen stapeln). Sag mir, ob dich das stoert.
5. Karte und **voller Rucksack**: grau. Karte: "Your cub cannot carry this without losing something about it."; Rucksack: "Empty it
   first.". Getragenes Hemd: "Take it off first.".
6. Alles einzeln zurueck (**Take**, bei den Naegeln **All**): Axt hat dieselbe Schaerfe, Pistole ist noch geladen und hat das Visier,
   Flasche ist noch halb voll, Hemd hat noch das Blut. Meldung "You took ...".
7. Zu schwer: das Junge traegt etwa 10 kg. Gib schwere Dinge (Brett, Axt ...), bis **Give** grau wird: "Too heavy for your cub: ... kg left.".
8. Weggehen (3 Kacheln oder mehr): Liste bleibt sichtbar, alles grau, unten "Walk to your cub to put things in or take them out.".
   Mausrad ueber einer Spalte blaettert (bei mehr als 10 Zeilen), Umschalt + Pfeil springt 10 Seiten.
   Fern-Taste (falls du in Optionen -> Mods -> "NPC Crew: Bear" eine belegt hast; Vorgabe: keine): aus 20 Kacheln das Baeren-Fenster
   oeffnen, **Inventory** -> die Liste kommt, alles grau.

**Teil C: Packtaschen (+150 kg)**
9. Als Junges, Bear Packs im Inventar: Rechtsklick **"Put packs on the cub"** ist grau mit "A cub is too small for packs."; im Fenster ist
   **Put on** ebenso grau. (Ohne Bear Packs im Inventar gibt es den Rechtsklick-Punkt gar nicht.)
10. `NCBear_CubGrow(15)` (halbstark; bis zu einer Minute warten, bis der grosse Baer da ist). Fenster: "Load ... / 40 kg".
11. Bear Packs im Inventar: Rechtsklick am Baeren **"Put packs on the bear"** (er laeuft hin) oder im Fenster **Put on**. Meldung "Your bear
    wears its packs now.", Kopfzeile **"Packs: on (+150 kg)"**, Load jetzt **/ 190 kg**. (Am Baeren sieht man die Taschen noch nicht.)
12. Naehen: Rezept **"Sew Bear Packs"** (Schneidern 3; Jute oder Stoff, Lederstreifen, Seil, Faden; Nadel und Schere bleiben) -- nur ansehen,
    ob es im Bastel-Menue steht.
13. Mehr als 40 kg hineinlegen, dann **Take off**: grau, "Take some things out first - without the packs your bear cannot carry it all.".
    Etwas herausnehmen, dann geht Take off; die Taschen sind wieder bei dir. Danach die Taschen wieder anlegen (fuer Teil D und G).

**Teil D: Alles bleibt da**
14. Mit vollem Inventar: Fenster **Look** (anderes Aussehen), **Unstuck**, ins Auto steigen und ein Stueck fahren (er faehrt mit; im Fenster
    "Your bear is riding with you.", ansehen geht), aussteigen, `NCBear_CubGrow(60)`: nach jedem Schritt ist alles noch genau so da.
    Spiel speichern und laden: ebenso.

**Teil E: Absturz (T7, der wichtigste Test)** -- erst NACH Teil D (dort hast du gespeichert und geladen; so ist der Baer selbst schon
im Spielstand).
15. Etwas Auffaelliges hineinlegen (z. B. die Axt). **Etwa 1 Minute warten** (nichts speichern). Spiel per **Task-Manager beenden**.
    Laden: die Axt ist **genau einmal** da -- beim Baeren, nicht in deinem Inventar. (In `console.txt` steht dann vielleicht
    "restored from the owner's copy".)
16. Umgekehrt: die Axt **herausnehmen**, 1 Minute warten, Task-Manager, laden: genau einmal da -- bei dir, nicht beim Baeren.
17. Werkbank ohne Absturz: `NCBear_InvSnap()`, etwas hineinlegen, `NCBear_InvRollback()` -> Meldung "register set back like after a crash",
    in `console.txt` "restored from the owner's copy"; `NCBear_InvInfo()`: das Hineingelegte ist da.

**Teil F: Selbst fressen**
18. Fisch hineinlegen, dann `NCBear_CubNeeds(70)` (Hunger 70 %). Hoechstens 10 Spielminuten warten: er frisst den Fisch selbst, kurzes
    Fress-Bild, Meldung "Your bear ate ... it was carrying.". Er frisst nicht, solange er schlaeft, kaempft oder mitfaehrt. Falls du
    verdorbenes Essen hast: das isst er nie, und im Tooltip steht dort auch nicht "eats this by itself".

**Teil G: Tod**
19. Ein paar Dinge + Packtaschen am Baeren, dann `NCBear_CubKill()`: alles liegt an seiner Stelle am Boden, auch die Packtaschen; Meldung
    "Your bear's things lie where it died.". Nichts doppelt, nichts fehlt.

**Mehrspieler (spaeter, F6) -- nur zur Info**
- Im Mehrspieler fehlt der Absturz-Schutz aus Teil E noch: stuerzt der **Server** zwischen zwei Speicherungen ab, kann Gegebenes fehlen
  oder Genommenes doppelt sein (Frage an dich im Bericht). Kleidung und Taschen nimmt er im Mehrspieler vorerst nicht (Farbton -- Frage an dich).
  Wenn du es trotzdem probierst: Rolle user, AntiCheat 2 -- es darf **keinen Kick** geben.

**Rueckmeldung bitte:** je Schritt "ok" oder was anders war (Screenshot mit rotem Kreis hilft). Danach muss das Spiel fuer jede Aenderung
neu gestartet werden (Lua laedt nur beim Spielstart).
