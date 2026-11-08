# Baer kaempft - Pruefung Animation und Technik (adversarisch)

Stand 08.11.2026. Geprueft: `_arbeit/baer_kampf/mod/42` (Bau), Berichte `kampf_spez.md`, `kampf_anim.md`, `kampf_lua.md`,
`sound/schnitt.md`. Nur gelesen, eigene Laeufe: Probe.java (`_arbeit/baer_spiel/harness`) auf neuem und altem GLB, GLB-Kanaele
und Gewichte mit Python, Textur gegen UV, wav-Messung, Kiefer gegen Tonhuelle, die vier Lua-Pruefer, Attrappe, javap.
Ausgaben: `_arbeit/baer_kampf/pruef_probe_technik.txt`, `pruef_probe_alt_technik.txt`, `_arbeit/baer_kampf/pruef_technik/`.
Spiel lief nicht (tasklist leer), gerendert wurde nichts. **Statisch geprueft, nicht gespielt.**

## Funde

1. **ernst** -- `NCBearFight.lua:36-39` (arrive 1.5, swipeReach 1.8, slamReach 2.0, maulReach 1.7), dazu `:472` (Nachruecken erst ab
   1,5 x 1,15 = 1,73) -- Die Spielregel trifft weiter, als der Clip reicht. Im Treffermoment ist die Pranke 0,82 Kacheln vor der
   Tiermitte, die Schnauze beim Biss 0,78, beide Pranken beim Doppelschlag 0,60 (`kampf_anim.md:37-45`, Clips laut Probe ohne Weg).
   Zombies laufen nicht auf den Baeren zu (sie zielen auf Spieler, Spez 3.6), also steht das Hauptziel beim Hieb typisch 1,0-1,7
   Kacheln weg: die Pranke schlaegt 0,2-0,9 Kacheln (bis ~1,1 m) davor in die Luft, und der Zombie faellt trotzdem; der Biss geht
   0,7-0,9 Kacheln vor dem Liegenden in den Boden. Bei Kevins "realistisch" sichtbar bei jedem Angriff. Der Animator hat es
   gemeldet (`kampf_anim.md:43-45`), die Lua-Seite hat es nicht uebernommen (der Biss wurde sogar von 1,4 auf 1,7 erweitert, weil
   er bei 1,5 ankommt). -- Vorschlag: `arrive` 1,05-1,1 (Koerperkreis `collisionSize` 0,42 laesst das zu), `swipeReach` ~1,4 fuer
   Nebenziele, `maulReach` ~1,2, `slamReach` ~1,5; alles bleibt per `NCBear_Tune` nachstellbar. Im Test pruefen, ob er bei 1,1
   haengen bleibt (Zeile "stuck on the way"). Groesse aendert nichts: Regel und Modell wachsen beide mit `getSize`.

2. **klein** -- `NCBearFight.lua:53` (`pause = { 0, 5 }`) mit `m_BlendTime` 0,15-0,25 der Knoten -- Die Engine nimmt einen noch
   ausblendenden Knoten wieder, statt ihn neu zu starten: `AnimLayer.findLiveNode` 36-59 liefert jeden Live-Knoten, der nicht
   `transitioningOut` ist, `getOrCreateLiveNode` 6-15 ruft dann nur `setActive(true)`, kein `startLiveNodeTracks`. Ausgeblendet
   wird ueber die eigene `m_BlendTime` (`LiveAnimNode.getBlendOutTime` 0-14 -> `AnimNode.getBlendOutTime`, Vorgabe `blendOutTime`
   -1,0 im Konstruktor 90-93 -> `blendTime`), entfernt bei Gewicht <= 0,01 (`removeFadedOutNodes`). Mit der Vorgabe 0,35 s ist
   das sicher. Mit `NCBear_Tune("pause", <0,25)` und zweimal demselben Angriff (Biss, dann Biss auf den naechsten Liegenden) steht
   der Clip schon am Ende: kein `NCBearHit`, kein `NCBearDone`, Frist, Treffer verworfen, nach drei Mal "fight clips probably
   missing" und 60 s Ruhe -- ein Fehlalarm, der die Suche zum GLB schickt. -- Vorschlag: Untergrenze `pause` 0,3, Grund als
   Kommentar dazu.

3. **klein** -- `NCBear_Rear.xml:14-18` (Roar bei `m_TimePc` 0,27) mit `NCBear_Roar.wav` -- Der zweite Stoss der Datei (1,20-1,92 s)
   faellt im Clip auf 2,0-2,74 s; der Kiefer ist nur 0,83-2,07 s ueber 15 Grad offen (aus dem GLB). Gemessen: 0,60 s der 1,95 s
   lauten Tons (> -24 dBFS, 50-ms-Fenster) liegen bei Kiefer < 8 Grad (2,18-2,74 s), genau waehrend er auf alle vier zurueckgeht.
   Klingt wie Bruellen mit geschlossenem Maul. Biss und Doppelschlag sind unauffaellig (Knurren beim Schuetteln passt). --
   Vorschlag: Roar auf den ersten Stoss kuerzen (Datei ~0,05-0,95 s, `schnitt.py`) oder den Kiefer im Clip bis ~2,7 s offen halten.

4. **klein** -- `NCBearFight.lua:473` und `:515` mit `:346-349` -- `F.ChooseAct(B)` wird als Argument VOR `beginAct` ausgewertet;
   `countFoes(..., frontOnly)` fuer die Doppelschlag-Wahl nimmt `B.fx/B.fy` vom letzten `face()` (vor dem Anrennen, Startwert {1,0}).
   Nach dem Anrennen zeigt der "vordere Halbkreis" in die alte Richtung. Die Treffer selbst stimmen (`beginAct` dreht vor dem
   Setzen, `:253`, und bis zum Treffer, `:481`). -- Vorschlag: in `decide` und `updateApproach` erst `face(B, B.target)`, dann
   `ChooseAct`.

5. **klein** -- `NCBearFight.lua:580-591`, `:601-605` -- `scanBears` wirft einen verschwundenen Baeren ohne `clearAct` aus der Liste,
   `register` loescht nichts. Kaeme dasselbe Objekt mit gesetztem `NCBearAct` zurueck, gewinnt der Knoten (Prioritaet 10) und
   niemand loescht ihn: er steht im letzten Clipbild ohne Atmen. Ob ein Tierobjekt so zurueckkommen kann: ungeprueft (Neuladen
   eines Chunks baut vermutlich neu). -- Vorschlag: in `register` die drei `clearVariable` (ISPetAnimal.lua:48), einmal je Baer.

6. **klein** -- Abschluss-Kopie -- Der Bau hat 16 Dateien; `NCBearTest/42` hat daneben `client/NCBearSpawn.lua`, `NCBearTest.lua`,
   `NCBearSize.lua` (00:14), `NCBearAttackProbe.lua` (01:04, gehoert zu `begleiter/angriff_fazit.md`, nicht zu diesem Lauf),
   `Translate/EN/IG_UI.json`, `scripts/nc_bear.txt`, `nc_bear_tier.txt`, `NCBearDeer.glb`, `WorldItems/*`, beide `mod.info`. Die
   Kopie darf nur hinzufuegen und ueberschreiben, nie spiegeln oder loeschen. `NCBearDefs.lua` unterscheidet sich vom Stand in
   NCBearTest nur im Tonblock (diff). `mod.info` sagt noch "friedlich" (`kampf_lua.md:26`).

7. **klein** -- Netz, bekannt (`kampf_anim.md:79-82`) -- Bestaetigt im Video: Hieb links Bild 131-137 dunkler Schmier an
   Brust/Achsel (Dehnung 6-7-fach); Nahbild `anim/stand2/maul_zu.png` zeigt bei fast geschlossenem Kiefer einen Spalt mit
   Fangzahn und einen kantigen Unterkiefer. Aus Spielhoehe kaum zu sehen. Nur notiert.

## Geprueft und in Ordnung

- **Clipnamen gleich in Lua, XML, GLB:** Probe.java selbst gelaufen: `NCBear_Rear/SwipeL/SwipeR/Slam/Maul` = `m_AnimName` =
  `F.ACTS` (`:23-27`); Dauern 3,0 / 1,1 / 1,1 / 2,2 / 1,6 s = `F.ACTS`. 10 Clips, 26 Knochen, `Bip01_Jaw` Kind von `Bip01_Head`,
  "ohne_keys" in jedem Clip leer. `Translation_Data`, `Bip01`, `Dummy01` in allen Kampfclips ueber den ganzen Clip 0 (GLB-Kanaele).
- **Alte Clips unveraendert:** Probe-Ausgabe der fuenf `DeerStag_*` alt/neu zeilengleich (Weltlagen, Weg, gehaeutete bbox);
  Schluessel je Clip genau +2/+2/+2 (Kiefer, steht still).
- **Netz:** ein Netz (Name jetzt `NCBear.001`, egal: `ProcessedAiScene.findMesh` 9-56 nimmt ohne meshName das erste gehaeutete),
  kein Material wie vorher, je Punkt hoechstens 4 Gewichte, Summe 1,000, 625 Punkte am Kiefer, 8.439 Punkte = Importer. Mit
  Positions-Schweissung genau 41 Kanten mit vier Flaechen = der Lippenschnitt, sonst geschlossen, keine entarteten Dreiecke.
  Kieferwinkel aus dem GLB 38 / 22 / 22 / 26 / 34 Grad = Bericht.
- **Textur:** 16.512 Pixel geaendert (x 276-499, y 12-99); Ueberlappung mit der UV von `NCBearDeer.glb` und vom alten Netz 0, auch
  mit 8 px Rand (Mip-Bluten). Das neue Netz nutzt die Flecken. MD5 GLB/PNG = `kampf_anim.md`.
- **Knoten nur fuer den Baeren:** Bedingung `NCBearAct` setzt nur `NCBearFight.lua`, nur an `getAnimalType() == "bear"` (`:612`);
  echte Hirsche und `bearstag` bekommen sie nie. Vanilla-Form: `m_Looped false` (521x), `m_ConditionPriority 10` (14x), STRING mit
  `m_Value` wie `buck/idle/idle2.xml`, SetVariable `End` wie `player/bumped/bumpFall.xml`; XML wohlgeformt, Dateinamen und
  `m_Name` eindeutig. Kein Uebergang in `actiongroups/buck/idle/*.xml` haengt an einem unserer Ereignisnamen.
- **Ausgang aus jedem Knoten:** nur ueber `NCBearAct`, und Lua loescht es bei Done, Frist (Dauer + 1 s), Kampfende, Treffer am
  Baeren, Lua-Fehler (`releaseAll`), `NCBear_Fight(false)`. Ausnahme Fund 5.
- **Ereigniszeiten = Clip:** Treffer 0,462 / 1,254 / 0,544 s gegen Kontakt 0,46 / 1,25 / 0,544; Wusch 0,297 gegen Schlagbeginn 0,30;
  Stampfen 1,21 gegen Aufsetzen 1,22; Roar 0,81 bei offenem Maul (Rest Fund 3).
- **Jar:** `AnimEventSetVariable` teilt "Name=Wert" (9-38), `OnAnimEvent_SetVariable` setzt am Charakter (21-27). OnTick laeuft
  in der Pause nicht (IngameState hat dafuer `OnTickEvenPaused`), die Frist zaehlt also keine Pause. Unsichtbare Tiere
  ueberspringen Bilder mit hochgerechneter Zeit (`IsoGameCharacter.updateAnimationTimeDelta` 58-95), Ereignisse kommen trotzdem.
  Lua-Uhr `getMultiplier()/48` = `GameTime.getTimeDeltaFromMultiplier` (/0,8/bias/60) bei bias 1; `animationTimeScale` setzt nur
  IsoGameCharacter selbst.
- **Argumenttypen der Engine-Aufrufe:** `faceThisObject(IsoObject)`, `CanSee(IsoMovingObject|IsoObject)`, `fleeTo(IsoGridSquare)`
  (ISMilkAnimal.lua:38 mit `getSquare(...)`), `knockDown(boolean)` (DebugContextMenu.lua:562-563 -> :668), `playBreedSound(String)`,
  `setVariable/clearVariable/getVariableString(String..)`: IsoAnimal erbt von IsoPlayer, also dieselbe Klassenlinie wie die
  Fundstellen am Spieler. `addSound(IsoObject,int x5)` nur bei `noise > 0` (Vorgabe 0).
- **Toene:** sechs wav vorhanden, mono 44,1 kHz 16 bit PCM, Spitze -1,3 bis -8,1 dBFS, rms95 -12 bis -13 (Huff -21,7; meine
  festen 50-ms-Fenster liegen 1-2 dB unter `schnitt.md`), DC < 0,4 LSB, erstes/letztes Sample 0. Namen Skript = Datei = XML =
  Rassentabelle. Vanilla-Namen belegt: SledgehammerSwing/Hit, MacheteHit, ZombieBite, HeadSmash, AttackStomp,
  AnimalFoleyBuckBodyfall. `GameSound.is3d` Vorgabe true (Konstruktor 11-12), also 3D ohne `is3D`-Zeile. MD5 = `ton/md5_1.txt`.
- **Lua-Pruefer:** luacheck und scopecheck 0; localcount hoechstens 52 insgesamt; luacheck_pz nur 2x W113 auf den eigenen Global
  `NCBearFight`. LF, ASCII, ohne BOM. Keine Namensgleichheit mit den Globalen von NCBearTest.
- **Attrappe:** `test_fight.lua` laedt die echte Datei per `dofile` (`:138`); mit Pfad gelaufen 79/79 gruen (ohne Pfad bricht sie
  bei `:141` ab, der Aufruf steht im Kopf). Ihr Motor startet den Clip bei jedem Wechsel neu - Fund 2 kann sie nicht sehen.
- **Kosten und Deckel:** je Bild nur kaempfende Baeren (zwei Variablen, ein Abstand, eine Frist, Drehen bis zum Treffer);
  Zombieliste ohne Kopie alle 0,5 s je ruhendem Baeren, `getObjectListForLua` alle 5 s; Deckel 8 / 4 / 32; Sortierer streng.
- **Bilder:** 330 Einzelbilder (`anim/video`, Quelle des mp4; mp4 selbst nicht dekodiert, kein ffmpeg) als Kontaktbogen und
  Ausschnitte angesehen: Aufrichten mit offenem Maul, Hieb links mit der linken (nahen) Pranke, rechts mit der rechten,
  Doppelschlag, Biss mit Schuetteln; kein Riss, kein Gleiten sichtbar. L/R wie beim Vanilla-Hirsch (Probe `DeerStag_Walk.x`:
  `Bip01_L_Foot` x +0,065, Baer +0,134). `kampf_bilder.png` angesehen.
- **Mehrspieler:** nichts angemeldet (`isSP`), Knoten und Rassentoene liegen mit, Schaden nur im Einzelspieler - wie verlangt
  als offen markiert.

## Urteil

Technisch sauber und spielbar, kein toedlicher Fund; ernst ist nur, dass die Schlagweite der Regel sichtbar groesser ist als die
Pranke im Clip (Fund 1), der Rest ist klein.

Statisch geprueft und offline gemessen, nicht gespielt.
