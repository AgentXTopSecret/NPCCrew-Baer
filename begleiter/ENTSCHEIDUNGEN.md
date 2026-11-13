# Baer als Begleiter: Kevins Entscheidungen (Stand 08.11.2026 nachts)

Gilt vor PLAN.md, wo beide sich widersprechen. Quelle: Chat mit Kevin 07./08.11.2026.

## Groesse und Stufen (entschieden)
| Stufe | Groesse (setSizeForced) | Kampf |
|---|---|---|
| Jungtier | 0,35 (rund 70 cm lang, 40 cm Schulter) | kaempft nicht, versteckt sich bei Zombies hinter dem Besitzer |
| Halbstark | ab 0,75 | schwacher Prankenhieb gegen EINEN Gegner, wenig Schaden, wirft nicht um; bruellt, richtet sich noch nicht auf |
| Erwachsen | **1,35** (Kevin: "mach den finalen baeren doch auf 1,35"; rund 2,65 m lang, 1,55 m Schulter, aufgerichtet rund 2,7 m) | alles: Aufrichten mit Bruellen, Flaechenhieb, Umwerfen, viel Schaden |

Modell bei 1,0: 1,96 m lang, 1,16 m Schulter. Wachstum etwa 7 Spieltage bis Halbstark, weitere 14 bis Erwachsen, Tempo als Sandbox-Option, Fuettern beschleunigt, Hunger bremst. Leben, Hunger und Durst wachsen fliessend mit. Optional spaeter: eigenes Baby-Modell (groesserer Kopf, kuerzere Beine, flauschiger), Kevins Wort offen.

## Leben, Futter, Wasser (Vorschlag als Vorgabe, Kevin: Level-Idee "gefaellt mir")
| Stufe | Leben | Futter je Spieltag | Wasser je Spieltag |
|---|---|---|---|
| Jungtier | 40 | 1 Mahlzeit | 1 Schale |
| Halbstark | 150 | 2 Mahlzeiten | 2 Schalen |
| Erwachsen | 400 | 4 Mahlzeiten | 3 Schalen |

Level-System: bis +50 % Leben, dazu Ausdauer, Schaden, Tempo, Spuersinn (Vorschlag). Hunger/Durst: erst langsamer und schwaecher, waechst nicht, heilt nicht; lange ohne: verliert Leben.

## Tod
Kann gegen Zombies und Banditen sterben. Sandbox "Baer unsterblich" (Vorgabe AUS): dann statt Tod "downed" wie die NPC-Crew-Figuren, aufhelfen.

## Gegner wehren sich (Kevin: "bisschen doof wenn der alles wegklatscht und die wehren sich nie")
Zombies und feindliche Banditen sollen den Baeren angreifen und verletzen. Weg 1 "echt" (Zombie zielt auf den Baeren) wird zuerst geprueft (Lauf baer-zombie-angriff, `angriff_*.md`, Probe `NCBear_AttackProbe()`), Weg 2 "nachgebaut" nur, wenn 1 nicht geht.

## Inventar und Fischen (Kevin: "ja das klingt gut")
Eigenes Inventar zum Oeffnen. Traglast: Jungtier 10, Halbstark 40, Erwachsen 100 (wie ein grosser Kofferraum), Packtaschen als Ausruestung +50, Sandbox-Faktor fuer mehr (500 abgelehnt: dann braucht niemand ein Auto). Ob ein lebendes Tier ein oeffenbares Inventar haben kann: ungeprueft.
Spaeter: Fischen erst ab kampfbereit (Halbstark ungeschickt, Erwachsen besser), streift an See oder Fluss, faengt Fische, legt sie ins eigene Inventar und frisst sie selbst. Kommt nach Kampf, Wachsen und Fuettern.

## Grundsatz
Jeder Spieler darf einen Baeren als Begleiter haben; wie man ihn bekommt, schlaegt PLAN.md vor (Kevins Wahl offen). Agenten: fuer das Baer-Projekt bis 10 je Lauf ohne erneute Frage (Kevin 07.11.).

## Offen am Modell (Kevin 08.11.: 'der baer muss natuerlich noch schoener werden du weisst die schoenheitsfehler')
Liste fuer den Lauf baer-fell: (1) Umriss 'wie Hubbel' -> viele kleine spitze Zotteln; (2) Koerpertextur 1024 -> 2048, staerkere Haarstraehnen, Schatten in Falten; (3) Augen nur Schlitze -> tief liegendes, dunkles, sichtbares Auge mit Lidrand; (4) Gesicht zu hell; (5) von hinten ein Klumpen; (6) Falten an Ellbogen und Achsel liegend; (7) im Galopp ein Bild mit zu kurzem Hinterbein; (8) pruefen, ob Alpha-Haarkarten am Rand gehen; (9) Junges-Modell: Kevin 08.11. *'vllt auch ein eigenes baby model ;D aber ich weiss nicht ob das wirklich noetig ist koennte man ja testen den unterschied ob man den echt sieht'* -> im Fell-Lauf zuerst ein Vergleichsbild im Spielwinkel und in Spielgroesse (verkleinerter Erwachsener 0,35 gegen Junges mit eigenen Proportionen), Kevin entscheidet danach.
Fell sieht im Spiel "wie Hubbel" aus (Kevin 08.11., Abendlicht): Umriss mit grossen runden Beulen, Koerpertextur nur 1024. Nach dem Lauf baer-kampf: Lauf "baer-fell" (kleine spitze Zotteln statt Beulen, Textur 2048, staerkere Straehnen, pruefen ob Alpha-Haarkarten gehen).

## Antworten auf die Plan-Fragen (Kevin 08.11.)
* **Bekommen:** Weg A (verwaistes Junges im Wald, 3-5 Mal aus der Hand fuettern) plus C (Koederplatz mit Honig oder Fisch). Mutter (B) spaeter.
* **Downed:** Aufhelfen per Rechtsklick (5 s, 45 % Leben) und ohne Hilfe steht er nach 12 Spielstunden mit 15 % allein auf.
* **Mitgehen:** `pathToLocation` am Tier als AUSNAHME erlaubt (Kevins Ja), mit Jar-Beleg, Existenz-Riegel, pcall und Gegenprobe; scheitert es, Rueckfall Hinterherrennen.
* **Artname:** umbenennen in `ncbear` (in B1, nach dem Lauf baer-kampf, der heute noch 'bear' benutzt; Testspielstaende mit Baer werden dann unbrauchbar, Kevin weiss es).
* Ohne eigene Frage, Vorgabe aus dem Plan: Schaden nur von Zombies, Banditen, Hunger, Durst (nicht Spieler, nicht Autos); nach dem Tod neues Junges nach 7 Spieltagen; jede Version in SP und MP, Kampf im MP erst ab B9.

**Reihenfolge:** nach baer-kampf: B1 (Wachsen, Umbenennen, Groessen) und parallel baer-fell (Modell), dann B2a usw. nach PLAN.md.

## Copy-Paste in NPC Crew (Kevin 08.11., 'ganz wichtig')
Alles muss spaeter per Copy-Paste in NPC Crew gehen, wie beim Turret: Lua als `BanditsNPCBear*.lua`, Modul `BanditsNPC.Bear`, Texte `UI_BN_Bear_*` in sieben Sprachen, Sandbox `BanditsNPC.Bear*`, Testhilfen getrennt (`NCBearBench*`, nie kopiert), gleiche Pfade fuer Modelle, Texturen, Toene, AnimSets; Kollisionsprobe; Uebernahme-Skript `_docs/tools/baer_uebernahme.py` mit Trockenlauf und Probe. Der Umbau der heutigen `NCBear*`-Dateien gehoert in B1 (zusammen mit der Umbenennung der Art in `ncbear`).

**FESTE REGEL (Kevin 08.11.): keine Cheat- oder Testmenues nach NPC Crew.** Spawn-Menues, Bank-/Testmodus, Konsolenbefehle (`NCTurret_*`, `NCBear_*`) und Debug-Rechtsklicks leben nur in Bench-Dateien. Das Uebernahme-Skript prueft die kopierten Dateien darauf und bricht sonst ab (beim naechsten Lauf, der das Skript anfasst, einbauen).

## Ergebnis Angriffs-Recherche (08.11. ~01:30, statisch, nicht gespielt; `angriff_*.md`)
* Zombies: von selbst nie. Angestossen (spotted/setTarget) laufen sie hin und beissen SICHTBAR, die Engine macht aber 0 Schaden (AttackState.triggerPlayerReaction 20-33). Schaden rechnen wir selbst (Mittelweg: Engine-Biss als Bild + eigener Abzug; fuer NPC Crew Weg 2 nach Bandits-Muster). Probe `NCBear_AttackProbe()` nach Neustart.
* Banditen: zielen nie auf Tiere; eigene Zielsuche ueber CacheLightB (nur hostile) plus eigene Aufgabe, Schaden selbst rechnen. Crew und Neutrale greifen ihn nie an.
* NEBENFUND, betrifft auch NPC Crew (alle Tiere, nicht nur den Baeren): eine verirrte Banditen-Kugel, die ein Tier trifft, landet im Einzelspieler laut Jar-Lesart beim SPIELER (playerIndex 0). Ungespielt; ein Gegenzug braucht Kevins Wort.

## Probe im Spiel (Kevin 08.11. ~01:20, console.txt Zeilen um [NCBear-ATK])
Weg 1 angestossen (30 Anstoesse in 15 s): der Zombie LAEUFT hin (walktoward, Abstand 1,95 -> 0,81), bleibt dann in idle 0,81 vor dem Baeren stehen, das Ziel steht bei jeder Messung schon wieder auf 'keins', kein einziger Biss-Ansatz (Zustand attack nie), Baer-Leben 1,000 unveraendert. Lesart: das Ziel wird sofort geloescht (Ursache ungeprueft) und die Kollision haelt ihn ausserhalb der Bissweite 0,72. **Also Weg 2: Biss nachbauen** (eigene Biss-Pose/Animation, Ton, Blut, Schaden per eigenem Code) fuer B5a; die Annaeherung ueber spotted/setTarget taugt als 'hinlaufen'.

## Befehle, Sitzen, Fressen (Kevin 08.11. ~01:45)
Woertlich: *'ich will auch eine fressens animation und sitz animation fuer den baeren das man den sagen kann der soll sich hinsetzen z.b oder frei rum wandern aber nie aus der base area geht, aber egal was er tut wenn ein zombies kommt soll der dann immer kaempfen ausser man stellt den auf passiv'*.
* Neue Clips: Hinsetzen, Sitzen (Schleife), Aufstehen, Fressen (Schleife). Das Animset `buck` hat dafuer schon Zustaende (idleSit/sitRandomly, eating): Clips `DeerStag_IdleToSitting`, `DeerStag_SittingIdle`, `DeerStag_SittingToStanding`, `DeerStag_IdleEating01` im eigenen Netz.
* Befehle: Folgen, Bleiben, **Sitz**, **Frei herumlaufen** (nie ausserhalb der Basisflaeche: in NPC Crew die gezeichnete Basisflaeche des Beacons, in der Test-Mod ein vom Spieler gesetzter Bereich), Komm her. Fressen spielt beim Fuettern und wenn er aus dem eigenen Inventar frisst.
* **Kampf hat Vorrang:** egal welcher Befehl, kommt ein Zombie oder feindlicher Bandit, kaempft er (ab Halbstark); danach zurueck zum Befehl. Schalter **Passiv** (je Baer): kaempft nicht, bleibt beim Befehl bzw. zieht sich zum Besitzer zurueck. Jungtier kaempft nie (versteckt sich).
* Gehoert in B2b (Befehle) und eine Clip-Runde (zusammen mit dem Fell-Lauf oder davor).
* **Unstuck-Knopf** (Kevin 08.11.: 'wir brauchen natuerlich wie bei den npcs einen unstuck button fuer den baeren'): im Baeren-Fenster, holt ihn auf eine freie, stehbare Kachel neben dem Spieler (nie auf eine unstehbare, Regel der NPCs), auch wenn er liegt oder nicht geladen ist; nur auf Klick, nie automatisch. Im Mehrspieler versetzt der Server das Tier (Tiere rechnet der Server). Gehoert in B2a/B2b.
* **Sitz-Animation, Massstab (Kevin 08.11.: 'unsere sitz animation muss besser aussehn wie bei denen'):** besser als Knox Wildlife (deren Sitzen hat er im Spiel gesehen: 'bad'). Wie echte Baeren sitzen: Hinterteil am Boden, Hinterbeine nach vorn gestreckt oder angewinkelt, Oberkoerper aufrecht oder leicht nach hinten gelehnt, Vorderpranken zwischen den Beinen oder auf dem Bauch; dazu eine zweite Sitzhaltung (seitlich gelagert). Hinsetzen und Aufstehen fluessig, kein Durchdringen des Bodens, Fell darf nicht zerreissen. Vor dem Bau Referenzbilder echter sitzender Baeren suchen (Websuche, nur ansehen).
  **KEVINS VORLAGE (08.11. ~01:50, `kevin_sitzvorlage.png` hier im Ordner; 'so soll unser baer sitzen laut google bilder sitzen die wohl immer so', dazu 'das sieht auch voll suess aus'):** DAS ist die Haupt-Sitzhaltung, sie geht vor der Beschreibung oben. Aufrecht auf dem Hinterteil, Oberkoerper senkrecht und rund (Bauch nach vorn), Vorderbeine gerade nach unten zwischen den Hinterbeinen, Vorderpranken flach am Boden; Hinterbeine nach vorn und leicht gespreizt, die Fusssohlen zeigen nach vorn/oben (Ballen sichtbar); Kopf aufrecht, leicht zur Seite gedreht. Wirkung: gemuetlich, knuffig. Die seitlich gelagerte Haltung bleibt hoechstens eine zweite. Das Bild (Wasserzeichen pngtree) ist NUR Vorlage zum Ansehen, nichts davon wird in Modell oder Textur uebernommen.

## Kampf-Animationen, Kevins Test (08.11. ~02:30)
Woertlich: *'die animation sieht aus wie von einen schlechten entwickler und damit mein ich beide der knickt so komisch seine arm beim angriff und beim auf 2 beinen stehn das ist ersten zu kurz die animation und 2tens sieht die nicht so huebsch aus also da muste morgen nochmal dran mit agenten damit das schoener aussieht'*. Dazu: 'umwerfen hat geklappt aber die meisten sind sofort tot' (Schaden runter, Wert per `NCBear_Tune("dmg", x)` sucht Kevin aus, dann fest eintragen).
* **Prankenhieb (SwipeL/R):** der Arm knickt unnatuerlich (Ellbogen/Handgelenk falsch herum oder zu stark). Neu nach Vorlage echter Baeren: Schlag aus der Schulter, Arm fast gestreckt, Pranke dreht ein, Gewicht verlagert sich mit, Gegenarm stuetzt.
* **Aufrichten (Rear):** zu kurz und nicht schoen. Laenger (Aufrichten, oben stehen mit Bruellen, zurueck), echte Haltung: Hinterbeine tragen, Ruecken aufrecht, Vorderpranken locker vor der Brust, Kopf hoch, leicht schwankend.
* **Vorgehen morgen (auf sein Wort, mit Agenten):** zuerst Referenz echter Baeren (Websuche/Videos, nur ansehen, Bewegungsablauf je Phase notieren), dann Animator mit Gelenkgrenzen je Knochen (kein Knick gegen das Gelenk), Vorschau-Video, Kritiker vergleicht Einzelbilder gegen die Referenz, hoechstens zehn Runden. Treffermomente danach in NCBearFight.lua nachziehen. Gehoert zusammen mit Sitzen/Fressen (Vorlage `kevin_sitzvorlage.png`) in den Lauf 'baer-anim'.
* **Nachtrag Kevin 08.11. ~02:40** (woertlich: *'ja soll er und wenn er den krallenhieb macht knickt er den arm so komisch teilweise und bewegt den restlichen koerper halt null das sieht bisschen komisch aus, kannst du dir nicht angucken irgentwie wie ein echter baer kaempfen wuerde? abgesehn vom rangeln ich glaub das passt nicht so gegen zombies ;D und er braucht auch eine beiss animation also das er so durch weckselt zwischen angriff mal den angriff und mal den anderen macht ;D und sie kippen um beim angriff aber geht auch umkippen mit ein wenig zurueck fliegen? so knockback? das waere noch realistischer glaub ich weil ein baer ja mega stark zuschlaegt'*):
  - **Schnauben auch ausserhalb des Kampfs:** ab und zu beim Herumlaufen, beim Stehen und wenn der Spieler nah kommt (heute nur beim Losrennen im Kampf, hoechstens alle 6 s, und sehr leise; Huff-Schnitt ist der wackeligste, ggf. neu schneiden).
  - **Ganzer Koerper beim Hieb:** heute bewegt sich nur der Arm und knickt teils komisch. Neu: Schulter, Ruecken, Kopf und Hinterbeine arbeiten mit (Gewicht nach vorn, Vorstoss, Gegenarm stuetzt), Arm knickt nie gegen das Gelenk.
  - **Wie echte Baeren kaempfen** (Referenz zuerst, nur ansehen): Prankenhieb, Biss, Vorstoss/Ansturm, aufgerichteter Schlag. **Kein Rangeln/Ringen** (passt laut Kevin nicht gegen Zombies).
  - **Biss im Wechsel:** heute beisst er nur Liegende (NCBear_Maul). Neu: Biss auch gegen Stehende, und er wechselt die Angriffe ab (Hieb links, Hieb rechts, Biss, Doppelschlag), nicht nur links/rechts im Takt.
  - **Knockback:** Getroffene kippen nicht nur um, sondern fliegen ein Stueck zurueck (Baer schlaegt sehr stark). Morgen erst klaeren, was belegt geht: B42-Ragdoll (`to_staggerback-knockeddown-ragdoll`/`to_falldown-ragdoll` mit usePhysicHitReaction/isRagdollFall/canRagdoll, Setter und Lua-Belege suchen) oder ein eigenes Zurueckschieben ueber mehrere Bilder mit Wand-/Kachelpruefung (nie durch Wand, Tuer, Zaun, nie ins Wasser oder ueber eine Ebenenkante). Ohne Beleg kein Aufruf (CLAUDE.md Abschnitt 3).
* **Nachtrag Kevin 08.11. ~02:45** (woertlich: *'und die sitz animation brauch ich auch noch morgen, will sehn ob das so schoen wie auf den bild aussehn wuerde und der muss natuerlich noch allgemein huebscher werden der baer wobei ich sagen muss das gesicht also der kopf vom baeren passt so nur der rest ist so eckig'*):
  - **Sitz-Animation MORGEN** (Hinsetzen, Sitzen-Schleife, Aufstehen) nach `kevin_sitzvorlage.png`; Kevin will sie sehen und mit dem Bild vergleichen -> Vorschau-Render neben die Vorlage legen.
  - **KOPF BLEIBT SO** (Gesicht passt laut Kevin). Nicht umbauen; nur das Maul/die Kampfteile duerfen dran, die Form des Kopfes nicht.
  - **Rumpf, Beine, Pranken sind zu eckig:** runder machen (mehr Rundung im Umriss, weichere Uebergaenge Schulter/Bauch/Hinterteil, Fell-Volumen), ohne die Knochen/Clips zu brechen; Vergleichsrender alt gegen neu.
* **Nachtrag Kevin 08.11. ~02:50** (woertlich: *'und beim schrei + auf 2 beine stellen die animation soll noch 1sec laenger dauern'*): ~~NCBear_Rear von heute 3,0 s auf 4,0 s~~ **ZURUECKGENOMMEN ~02:52 (Kevin: 'warte mal die 3sec animation reicht schon das ist doch nicht zu kurz'): Dauer bleibt 3,0 s.** Der fruehere Punkt 'zu kurz' ist damit auch erledigt; bleibt nur 'schoener'. Alter Text: (die Sekunde mehr oben im Stehen mit Bruellen, nicht im Hoch-/Runterkommen). Mitziehen: Clip-Dauer und Bruell-Moment in NCBearFight.lua (`rear.dur`), und der Bruellton passt dann nicht mehr -- der Fixer hat NCBear_Roar auf den ersten Stoss gekuerzt (1,18 s), fuer 4 s eher beide Stoesse (2,0 s) oder den Ton so legen, dass er mit dem offenen Maul endet.
* **Nachtrag Kevin 08.11. ~02:55** (woertlich: *'aber diese doppel hieb attacke sieht auch sehr komisch aus von den gelenken'*): **NCBear_Slam (Doppelschlag) neu**, gleiche Regel wie beim Hieb: kein Gelenk knickt gegen seine Richtung (Ellbogen, Handgelenk, Schulter), ganzer Koerper arbeitet mit (Aufrichten, beide Pranken mit dem Koerpergewicht nach unten, Hinterbeine tragen). Damit sind ALLE vier Kampfclips (SwipeL, SwipeR, Slam, Rear) neu zu machen; Biss (Maul) nach Referenz pruefen. Gelenkgrenzen je Knochen als feste Regel im Animator-Skript, Kritiker prueft jeden Clip Bild fuer Bild auf Knicke.
* **Kevin 08.11. ~03:00: KEIN Scheinangriff** (woertlich: *'nein den scheinangrif will ich nicht unser baer soll immer angreifen'*). Kein Losrennen-Stoppen-Schnauben-Bodenschlag vor dem Angriff; er greift immer direkt an. Bewegungsvorbild fuer die Clips (aus allgemeinem Wissen, morgen per Referenz belegen): Hieb = Gewicht nach hinten, Vorderhaelfte hebt leicht, Schlag aus der Schulter im Bogen schraeg nach unten, Landung mit Schritt auf der schlagenden Pranke, Kopf dreht leicht weg; Biss = Vorstoss mit tiefem Kopf und langem Hals, kurzes Kopfschuetteln (Hauptwaffe); Doppelschlag = halb aufrichten, mit beiden Pranken und vollem Gewicht nach unten (Festnageln), danach Biss passend; Aufrichten + Bruellen bleibt als Drohgeste beim ersten Kontakt.
* **Kevin 08.11. ~19:00: knockPush Vorgabe 0,7** (woertlich: *'NCBear_Tune("knockPush", 0.7) soll der standard werden glaub 1 ist schon bisschen too much ;D'*). Im Spiel getestet mit knockBack = 1 (Vorgabe): das eigene Schieben kommt dann nur zu den echten Fluegen von vorn dazu (Flug rund 2,1 Kacheln statt rund 2,9 mit 1,5). In `F.T` von NCBearFight.lua `knockPush = 0.7` setzen (nach dem Lauf baer-laerm, der dieselbe Datei aendert). Offen: Treffer von der Seite und von hinten fallen weiter nur um (Angebot: eigenes Wegschleudern auch dafuer).
* **Kevin 08.11. ~19:10: Pfoten-Sohlen und Unterseite** (woertlich, mit Foto einer echten Baerensohle `kevin_pfotenvorlage.png`, nur ansehen, nicht hochladen: *'so sieht eine baeren pfote aus und unser model hat einfach nix da und wenn der baer auf 2 beine steigt sieht das auch so aus als haette unsere model den koerper den man nur beim aufstehn sieht eher vernachlaessigt'*). Anlass: im Sitzen (Fassung a) wirken die nach vorn zeigenden Sohlen von der Spielkamera wie schwarze Loecher. Befund: in der Textur (NCBear.png 1024) sind die Sohlen nur dunkelbraune Flecken mit Krallen, keine Ballen.
  - **Sohlen wie beim echten Baeren:** grosser querliegender Sohlenballen, fuenf Zehenballen im Bogen darueber, Krallen davor, dunkelgraue lederartige Haut, Fell am Rand; Vorder- und Hinterpfoten (hinten laengere Sohle mit Fersenballen). In Netz UND Textur, sichtbar im Sitzen, Aufrichten, Liegen und Sturz.
  - **Unterseite ausarbeiten:** Bauch, Brust, Achseln, Innenseiten der Beine, Kehle -- was man nur beim Aufrichten und Sitzen sieht (heute vernachlaessigt, dazu die bekannte Hautdehnung Achsel/Brustunterseite). Gehoert in den Lauf **baer-fell** (Kevins Startwort vom 08.11.), vor dem neuen Aufrichten-Clip pruefen.
  - **Nachtrag Kevin 08.11. ~19:20** (woertlich, mit Spielbild `kevin_rear_unterseite.webp` von vorn beim Aufrichten: *'hier guck dir an wie scheisse der baer von unten aussieht wenn der ROAR macht'* -- *'das musst du fixxen noch ubedingt mit den pfoten zusammen'*): **Pflicht im Lauf baer-fell, zusammen mit den Sohlen.** Gesehen im Bild: Brust/Bauch dunkel und verschmiert ohne Fellstruktur; Vorderpranken vor der Brust formlose dunkle Klumpen mit Krallen (dazu der bekannte Kragen ueber den Oberarmen); Hinterbeine Roehren mit hellem Streifen innen, Fuesse ohne Form; Rumpf von vorn ein Ei ohne Schultern und Hals. Ursache (statisch, nicht gemessen): die Textur wird in der Vierbein-Ruhehaltung aus 21 Rumpf-Ansichten gebacken (auch 7 von unten, `baer_export.py` 99-106), aber Achseln, Brust zwischen den Vorderbeinen und Innenschenkel sind dort fast ueberall verdeckt; dazu die Hautdehnung Achsel/Brust. Pruefen im Lauf: Unterseite und Sohlen in Pose Aufrichten, Sitzen und Liegen von vorn und unten rendern und gegen das Spielbild halten.
* **Kevin 08.11. ~19:25: Testbefehle drehen den Baeren zur Kamera** (woertlich: *'wenn man die test befehle eingibt z.b NCBear_AnimTest("rear") dann muss der baer das immer machen in der position wo er zur "kamera" guckt also das ich den von vorne sehn kann weil sonst ist das scheisse ^^'*). Nur in `NCBearBench.lua` (Testhilfe, geht nie nach NPC Crew): NCBear_AnimTest, NCBear_Sit, NCBear_Eat drehen ihn nach erfolgreichem Befehl mit `animal:setDir(IsoDirections.SE)` (Beleg: Vanilla `ButcheringUtil.lua:574` setDir an einem Tier) -- SE = Bildschirm unten, also zur Kamera (statisch, im Spiel pruefen). Einbau nach dem Lauf baer-laerm (der dieselben Dateien kopiert).
* **Kevin 08.11. ~19:30: Sitzen schoener, keine schwarzen Flecken** (woertlich: *'und das sitzen muss noch bisschen schoener werden wie du meintest auch das an der seite so schwarze flecken sind ist da nicht gut ^^'*). "Wie du meintest" = Claudes Vorschlag vorher: Richtung Fassung (b) -- aufrechter Oberkoerper, Kopf hoch, Hinterbeine weniger gespreizt, naeher an `kevin_sitzvorlage.png` -- und die seitlich herausstehenden dunklen Sohlen weg (mit den neuen Ballen-Sohlen aus baer-fell; Sohlen nicht als dunkle Scheiben zur Seite). Damit ist die offene Wahl Sitzen (a)/(b) beantwortet: (b) als Richtung. Gehoert in denselben Gang wie Aufrichten neu (Clips nach dem neuen Netz aus baer-fell); Hinsetzen/Aufstehen nachziehen.
* **Kevin 08.11. ~19:40: Baeren rufen** (woertlich: *'ja das waere auch eine idee mit dem baeren rufen ;D'*), nachdem der Baer beim Rufen mit Q weglief. Idee fuer "Komm her" (Befehle B2b): Q-Ruf des Besitzers holt den Baeren, wie die Engine es bei Akzeptanz >= 40 von selbst tut (Jar IsoAnimal.respondToSound Offset 156-210). Belegt in Vanilla: `animal:getPlayerAcceptance(chr)` (ISAnimalUI.lua:323) und `animal:setDebugAcceptance(playerObj, wert)` (ISAnimalContextMenu.lua:614, nur Debug-Menue "Full Acceptance"; im MP Serverbefehl mit Recht AnimalCheats, ClientCommands.lua:964-971) -- also ein Cheat-Weg, NICHT fuer NPC Crew. Fuer das fertige Spiel einen echten Weg suchen (Akzeptanz wie Vanilla durch Streicheln/Fuettern, oder eigene Ruf-Erkennung); erst pruefen, nicht bauen.
* **Kevin 08.11. ~19:45: Baeren-Fenster mit V** (woertlich: *'und mit V druecken geht die zombie uebersicht auf wie bei den npc's oder? ;D'* -- *'ich meinte die baeren uebersicht nicht zombie'*). Das Baeren-Fenster aus PLAN.md Abschnitt 8 (B6) oeffnet mit derselben Taste wie das NPC-Gespraech in NPC Crew (V = Belegung "Talk to NPC", `BanditsNPCInteract.lua:35/7392/7404`). Naht mit NPC Crew: V gehoert dort `BanditsNPC.Interact.Open`; wer gewinnt, wenn NPC und Baer nah sind (z. B. das Naechste unter der Maus/Figur), im Bau klaeren, Aufsatz in OnGameBoot, keine NPC-Crew-Datei aendern; ohne NPC Crew eigene Belegung. Dazu Rechtsklick "Baer" wie beim NPC.
* **Kevin 08.11. ~19:55: Reihenfolge, Umbenennen, Zaehm-Balken, Namensschild** (woertlich: *'solltest du nicht zuerst bauen das die zombies/bandits gegen den baeren kaempfen? und danach erstmal das baby baeren finden und tamen?'* -- *'das wuerde mehr sinn machen ;D'* -- *'ja mach das ;D und wir brauchen einen taming balken mit vorschrit und so und ueber den baeren noch eine namensanzeige dann die man auch abschalten kann im baeren menue'*):
  - **Reihenfolge** (STAND.md): baer-laerm -> baer-fell -> Clip-Runde -> **B5a Gegenwehr** (Zombies und feindliche Banditen) -> **B1 + Baby finden + zaehmen** -> Befehle und Fenster (V) -> Beduerfnisse, Inventar, Fischen, MP.
  - **Umbenennen ganz am Anfang von B5a** (Kevins Ja): Art `ncbear`, Dateien `BanditsNPCBear*`, Module `BanditsNPC.Bear`, Texte `UI_BN_Bear_*` in sieben Sprachen, Testhilfen nur in `NCBearBench*`.
  - **Zaehm-Balken:** beim Zaehmen des Jungtiers ein Fortschrittsbalken (wie weit er schon vertraut, was ihn voranbringt), sichtbar beim Zaehmen und im Baeren-Fenster.
  - **Namensschild ueber dem Baeren:** Name ueber dem Kopf, im Baeren-Menue/Fenster an- und abschaltbar (je Baer; Vorgabe an). Zeichnen wie NPC Crew/Bandits es fuer Namen tun (Fundstelle im Bau suchen), nichts Teures je Bild.
  - **Nachtrag ~20:00, Zaehmen durch Futter UND Streicheln** (woertlich: *'ich will das man den irgentwie mit futter tamed und den streicheln kann ;D so eine mischung aus beiden soll den fortschritt fuellen ^^'*): beides fuellt den Zaehm-Balken, die Mischung zaehlt (z. B. nur Fuettern oder nur Streicheln kommt langsamer voran als beides im Wechsel -- Zahlen im Bau vorschlagen). Spur: Vanilla-Streicheln ruft `animal:petAnimal(character)` (`ISPetAnimal.lua:70`, Timed Action 400) -- pruefen, ob das die Engine-Akzeptanz hebt (dann kaeme der Baer ab 40 auch auf Q-Ruf); Fuettern ueber eigenen Menuepunkt (Vanilla "Feed" bietet dem Baeren kein Fleisch, PLAN.md Abschnitt 6). Akzeptanz direkt setzen geht in Vanilla nur als Debug-Cheat (`setDebugAcceptance`) -- nicht fuer NPC Crew.
* **Kevin 08.11. ~20:05: Balken ueber dem Baeren** (woertlich: *'und ich will noch das man beim baeren einen hp bar anzeigen lassen kann ueber den baeren so von links nach rechts und bei bedarf noch mehr balken hunger/essen ;D'*): ueber dem Kopf (beim Namensschild) ein waagerechter Lebensbalken, der sich von links nach rechts fuellt; auf Wunsch weitere Balken (Hunger, Durst). Jeder Balken einzeln im Baeren-Menue/Fenster an- und abschaltbar, wie das Namensschild. Gehoert zu Fenster/Namensschild (Befehle und Fenster), die Werte zu Beduerfnisse. Zeichnen ohne Teures je Bild (Fundstelle fuer Bildschirm-Zeichnen im Bau, z. B. wie Bandits/NPC Crew Namen und Balken zeichnen).
  - **Nachtrag ~20:07** (woertlich: *'das kann jeder frei entscheiden im baeren menue was er haben will ;D'*): Namensschild und jeder Balken sind eine Einstellung JE SPIELER (was ich sehe), nicht je Welt; im Mehrspieler entscheidet jeder fuer sich. Gespeichert beim Spieler/Client, nichts davon muss der Server wissen.
* **Kevin 08.11. ~20:10: Immer streichelbar, Vertrauen/Gluecklich-Anzeige** (woertlich: *'und der baer soll immer streichelbar sein mit cooldown ;D da brauchen wir noch ein vertrauens system oder so das waer cool der anzeigt wie happy der baer ist ;D'*):
  - **Streicheln geht immer** (Jungtier und erwachsen, auch nach dem Zaehmen), mit Abklingzeit, damit man es nicht durchklicken kann (Zahl im Bau vorschlagen). Nur der Besitzer bzw. wer darf (MP: im Bau klaeren).
  - **Vertrauen / Gluecklich:** das ist die "Bindung" aus PLAN.md Abschnitt 5 (steigt mit Fuettern und Streicheln, sinkt bei Hunger), ausgebaut zu einer sichtbaren Laune: wie happy der Baer ist (Balken und/oder Gesicht/Wort im Baeren-Fenster, optional als eigener Balken ueber dem Kopf wie Leben/Hunger, je Spieler abschaltbar). Beim Jungtier fuellt dieselbe Mischung den Zaehm-Balken; nach dem Zaehmen geht es als Vertrauen weiter. Was sie senkt (Hunger, Durst, lange allein, verletzt) und was sie bewirkt (gehorcht besser/schlechter, PLAN.md) im Bau vorschlagen.
  - **Nachtrag ~20:12** (woertlich: *'hatte nicht oft grossen hunger oder durst sowas z.b'*): die Laune merkt sich, wie gut er versorgt WAR -- war er selten stark hungrig oder durstig, steigt sie (Zeitspanne, z. B. die letzten Spieltage, im Bau vorschlagen); oft grosser Hunger/Durst drueckt sie. Also nicht nur der Wert von jetzt, sondern der Verlauf.

## Schlafen, Zz, Schlafton, Baerenbett (Kevin 09.11.2026 mittags)
Woertlich: *'ich hab noch vorschlaege ich brauch eine baeren schlaf animation wenn moeglich noch mit so z Z z ueber den baeren wenn er schlaeft und vllt noch mit leisen baeren schlaf sound wenn es sowas gibt zum runterladen im internet, wenn nicht dann ohne ton und dann noch ein baeren bett das so gross ist das der baer da perfekt drauf passt wenn er maximal ausgewachsen ist. als oder muss dann spaeter noch schlafen wie npc's es schon tun'*
* **Schlaf-Animation:** Hinlegen, Schlafen (Schleife, ruhiges Atmen), Aufwachen/Aufstehen. Haltung nach echten Baeren (Referenz nur ansehen), gebaut auf dem neuen Netz aus baer-fell.
* **z Z z ueber dem Baeren**, solange er schlaeft (aufsteigend, klein-gross-klein). Zeichnen wie Namensschild/Balken: nichts Teures je Bild, im Mehrspieler sieht es jeder.
* **Leiser Schlafton** (Atmen/Schnarchen), nur wenn es eine freie Aufnahme gibt. Download wie immer nur mit Dateiname, Quelle, Groesse, Lizenz und Kevins Ja je Datei (Massstab `sound/roh/QUELLEN.txt`: gemeinfrei). Gibt es keine: ohne Ton.
* **Baerenbett:** so gross, dass der ausgewachsene Baer (Groesse 1,35, rund 2,65 m lang) in der Schlafhaltung genau darauf passt. Wie man es bekommt, ist offen (keine Cheat-Menues: echter Weg, z. B. Rezept/Bauen).
* **Schlafen wie die NPCs** in NPC Crew (spaeter): nachts schlafen, am Bett bzw. beim Besitzer; Kampf hat Vorrang (kommt ein Zombie, wacht er auf), Passiv bleibt.
* Reihenfolge im Bau: Kevins Wort offen (Vorschlag in STAND.md, nach dem Forschungslauf baer-schlaf).

## Pfoten: "wie ein abgesaegtes Bein" (Kevin 09.11.2026 nachmittags, nach dem Vorher/Nachher-Bild von baer-fell)
Woertlich: *'also ganz ehrlich du verarschst mich doch jz guck dir mal selbst die bilder an von dem bein das ist wie eine seule/abgesaegtes bein + baeren pfote vorne dran also das ist ja verarsche, das soll natuerlich nur eine richtige baerenpfote sein vllt nochmal rechere treiben und dann richitg machen oder brauchst du von mirn bild?'*
* **Er hat recht** (Ton-Bild `_arbeit/baer_fell/pruef/optik/blaetter/b6_sit_fuss.png`): das Hinterbein endet als runde Saeule mit Kappe, die Sohle ist nur draufgemalt, die Zehen sitzen als Klumpen oben drauf; vorn eine dicke Saeule mit kleinem Zehenwulst. baer-fell hat nur Textur und 8 mm Relief auf diese Kappe gelegt -- das war als "Sohle mit Ballen" zu schoen gemeldet.
* **Pflicht:** vier ECHTE Baerenpfoten -- das Bein geht in einen Fuss ueber (hinten Sohlengaenger mit Ferse, langer Sohle, Zehenreihe, Krallen; vorn breite Pranke mit Handwurzelballen), in jeder Pose als Pfote lesbar (Stehen, Gehen, Sitzen, Aufrichten, Liegen). Erst Recherche (Lauf baer-pfoten-forschung, 3 Agenten, `../_arbeit/baer_pfote/`), dann Bau-Lauf baer-pfoten.
* Regeln fuer den Bau: Kopf bleibt; Clips bleiben bit-gleich, ausser eine Pose ist nachweislich nicht zu retten (dann Vorschlag fuer die Clip-Runde); Krallen-Form bleibt, Lage darf an die neuen Zehen.
* Lehre: Ton-Bild (ohne Textur) jeder Form IMMER neben die Referenz legen, bevor etwas als "fertig" gemeldet wird; Textur darf eine falsche Form nicht verdecken.
* **Kevins Vergleichsbild (09.11. nachmittags, `kevin_baerenfuss_vorlage.png`; Stockfoto mit Wasserzeichen: NUR ansehen, nie hochladen, steht in .gitignore):** *'das ist auch ein vergleichsbild wie ein baerenfuss aussieht'*. Grizzly sitzt auf dem Hinterteil, eine Vorderpranke erhoben (breiter querliegender Handballen, Zehenballen im Bogen, Krallen), ein Hinterfuss erhoben mit der Sohle zur Kamera, der andere liegt auf der Aussenkante. Daran sieht man: der Hinterfuss ist eine lange, flache, ovale Sohlen-PLATTE (Ferse unten rund, fuenf Zehenballen im Bogen am oberen Rand, kurze Krallen), deutlich laenger als breit und laenger als das Bein dick ist; das Fell umschliesst den Sohlenrand; Bein und Fuss sind dick und zottig, aber der Fuss ragt als eigene Form heraus (Ferse hinten, Zehen vorn) -- keine runde Saeule mit Deckel. Gilt als Hauptvorlage fuer den Bau-Lauf baer-pfoten (zusammen mit `kevin_pfotenvorlage.png`).

## Gebiss, Zunge, Beine wie Baumstaemme (Kevin 09.11.2026 ~16:05, waehrend baer-pfoten laeuft)
Woertlich: *'hier guck dir mal die zaehne an wenn er schreit so sollen die auch aussehn die zaehne und zunge sieht auch noch schlecht aus ;D und die beine must du auch noch realistischer machen die sehn aus bei baumstaemme ;D'*
* **Vorlage:** `kevin_bruellen_vorlage.webp` (Bildschirmfoto einer Bildersuche "big brown bear roar", lauter Stockfotos mit Wasserzeichen: NUR ansehen, nie hochladen, nie in Modell/Textur, steht in .gitignore).
* **Was die Fotos zeigen (Gebiss beim Bruellen):** Maul sehr weit offen; vier lange, gebogene, spitze Eckzaehne (oben und unten, elfenbein- bis gelblich, an der Spitze heller), dazwischen oben und unten eine Reihe kleiner Schneidezaehne; dahinter Backenzaehne; Lippen weit zurueckgezogen, Lefzen schwarz, Zahnfleisch dunkel bis rosa sichtbar; Gaumen mit Querrillen.
* **Zunge:** rosa, breit und flach, liegt tief im Unterkiefer, Raender leicht hochgewoelbt, Spitze hinter den unteren Schneidezaehnen -- kein Klumpen, keine Rolle.
* **Beine:** "wie Baumstaemme" = gleich dicke Rohre. Echt: vorn grosser Schulterbuckel, Oberarm im Rumpf, kraeftiger Unterarm, der zum Handgelenk schmaler wird, Fellzotteln hinter dem Ellbogen; hinten breiter Oberschenkel, der in den Hintern uebergeht, nach unten zum Sprunggelenk schmaler, Ferse sichtbar. Fell bricht die Kontur (haengt an Bauch und Beinen).
* **Stand bei Kevins Nachricht:** baer-pfoten (laeuft) baut nur unterhalb ~36 cm Hoehe (Bein verjuengt sich zum Gelenk, eigener Fuss, SPEZ_PFOTEN.md 1.2/1.3); darueber bleibt die Form bewusst gleich. Ganze Beine (Schulter, Ellbogen, Oberschenkel) sowie Gebiss und Zunge sind ein EIGENER naechster Lauf (STAND.md 2c), erst nach Kevins Pause (5-Stunden-Limit).
* Regeln wie bei den Pfoten: Ton-Bild jeder Form neben die Vorlage, bevor "fertig"; Kopf-Aussenform bleibt (nur Maul innen, Lefzen, Zaehne, Zunge); Clips bit-gleich, ausser ein Bein laesst sich nachweislich nur mit neuer Pose retten.

## Gesicht des Baby-Baeren (Kevin 09.11.2026 ~16:09)
Woertlich: *'guck mal das bild sollst du nehmen als vorlage fuer das gesicht vom baby baeren wenn der noch klein ist ;D'*
* **Vorlage:** `kevin_babygesicht_vorlage.webp` (Foto unbekannter Herkunft: NUR ansehen, nie hochladen, nie in Modell/Textur kopieren, steht in .gitignore). Gilt fuer das Gesicht des Jungtiers (Groessenstufe Jungtier 0,35, evtl. auch noch Halbstark).
* **Was das Foto zeigt:** Junges liegt flach, Kinn auf dem Boden zwischen den Vorderpranken (Sphinx-Haltung wie unser geplanter Schlaf, SCHLAF_PLAN.md).
  - **Kopf** gross und rund, Stirn gewoelbt, steigt steil von der Schnauze an (deutlicher Stirnabsatz); Kopf wirkt breiter als lang.
  - **Ohren** gross, rund, weit aussen oben, dick bepelzt, innen etwas heller -- viel groesser im Verhaeltnis als beim Erwachsenen.
  - **Schnauze** kurz und stumpf, hell beige/hellbraun, nach oben ins dunklere Gesicht verlaufend; **Nase** schwarz, gross, feucht glaenzend.
  - **Augen** dunkelbraun, rund, eher gross, weit vorn, mit Glanzpunkt; Fell um die Augen dunkler, ueber den Augen ein Hauch heller.
  - **Fell** dicht, weich, kurz und flauschig, schokoladenbraun mit hellen Spitzen (wirkt gesprenkelt), an Wangen leicht abstehend.
  - **Pranken** dunkel, fuenf helle, gebogene Krallen je Pranke (elfenbein bis grau), Krallen im Verhaeltnis gross.
* **Bezug zum Bestand:** baer-fell hat ein Junges nur durch Knochen-Skalieren probiert (`../_arbeit/baer_fell/baby/bericht.md`: Kopf x1,45, Kopfnetz unveraendert, Pfoten relativ gross) -- Gesicht, Ohren und Schnauze waren dort noch Erwachsenen-Form. Mit dieser Vorlage wird das Baby ein eigenes Gesicht (Kopfnetz und Textur), nicht nur ein groesserer Erwachsenen-Kopf.
* **Wann:** zusammen mit dem eigenen Baby-Modell bzw. B1 (Wachsen, STAND.md Punkt 5) oder als eigener Lauf; Reihenfolge auf Kevins Wort. Bauweg (eigenes GLB fuer das Junge oder Gesichts-Form ueber Knochen + eigene Textur) im Lauf untersuchen. Regeln wie immer: Ton-Bild neben die Vorlage, bevor "fertig".
* **Kevin 09.11. ~16:15: Reihenfolge bleibt** (Antwort auf 'Baby vor die Gegenwehr ziehen?': *'Reihenfolge lassen'*): 2b Pfoten -> 2c Gebiss/Zunge/Beine -> Clip-Runde -> B5a Gegenwehr -> B1 + Baby finden und zaehmen. Dazu (woertlich): *'wenn der worklow durch ist mach direkt weiter'* -- nach baer-pfoten ohne Pause pruefen, einbauen und Lauf 2c starten (vorher Verbrauch pruefen, Agentenzahl nennen). Der Fundort-Vorschlag fuer das Junge (Wald selten ausser Sicht, Koederplatz 1-3 Naechte, Verschwinden nach 1-2 Tagen ohne Kontakt) ist ihm erklaert, aber noch nicht ausdruecklich bestaetigt.

## Sitzen, Hinterfuss, Kopf, Hose in Stiefeln (Kevin 10.11.2026 ~01:00, beim Spieltest von baer-pfoten)
Woertlich: *'siehste das der fuss sieht aus wie vom menschen jz viel zu lang'* -- *'und wenn er da so sitzt sieht das aus als ob sein kopf nicht zum koerper passen wuerde'* -- *'haste mal das bild gesehn wie es aussehn soll? die beine sind jz auch viel zu weit auseinander'* (Link auf seine Sitzvorlage, dasselbe Bild wie `kevin_sitzvorlage.png`) -- *'so sollte er da sitzend aussehn wie auf dem bild'* -- *'und guck dir mal seine fuesse an und guck mal die fuesse die du gemacht hast'* -- *'der baer hat so eine fussform wie menschen xD statt wie von einen braunbaeren'* -- *'die beine sehn jz zwar besser aus also die fuesse unten aber der uebergang ist so als haette der seine hose in stiefeln gesteckt xD komplett krass'*.
* **Spielbild Sitzen:** `kevin_sitzen_fuss_kopf.webp` (nur lokal, .gitignore; zeigt auch ein Steam-Overlay). Gesehen: Rumpf ein Fellball, die Fellhuelle steht als Kragen ringsum ums Gesicht, Kopf heller und glatter (wirkt aufgeklebt, zu klein, kein Hals); Hinterbeine weit gespreizt, Hinterfuesse lange hellgraue Rechteck-Sohlen wie Menschenfuesse. Das Stehbild (Hose in Stiefeln) liegt nicht auf der Platte: duenne kurze Unterschenkel/Unterarme, darueber schlagartig der dicke Rumpf wie ein Sack.
* **Massstab ist seine Sitzvorlage:** aufrecht, Kopf oben auf dem Koerper ohne Kante zum Koerperfell, Vorderbeine gerade zwischen den Hinterbeinen, Hinterbeine eng; Hinterfuss kurz, breit, fast rund, dunkelbraun-ledrig, grosse Zehenballen im Bogen, Fellkranz. Die Literatur-Ziele aus baer-pfoten (spitze Ferse, L/B 1,7-1,9, 29 cm) gelten fuer die FORM nicht mehr.
* **Folgen (Claude):** alles in Lauf 2c aufgenommen (Workflow angehalten und mit Zusatz C1-C5 fortgesetzt, Forschung blieb erhalten): C1 Hinterfuss wie in der Vorlage; C2 Sitzen nach der Vorlage = Richtung (b) vom 08.11. (SitDown/Sit/StandUp neu, Laenge/Ereignisse gleich; das Sprunggelenk tiefer = C3 aus SPEZ_PFOTEN 4.2, mit Kevins Saetzen freigegeben); C3 Kopf passt: Kopfform bleibt, Kragen weg, Hals/Nacken, Farbuebergang ueber Koerper-Texel, ein groesserer Kopf nur als Vorschlag mit Bild; C4 Rumpf schmaler; C5 durchgehender Uebergang Pfote -> Rumpf ohne Hose-in-Stiefeln (Kevins wichtigster Bein-Punkt). Das neue Aufrichten bleibt in der Clip-Runde.

## Baby-Modell hochwertig + Finden und Zaehmen JETZT (Kevin 10.11.2026 nachmittags, neuer Account)
Woertlich, auf die Frage nach dem Entwurf des Jungen: *'hast du den auch angepasst an das neue baeren model? wo die fuesse verbessert worden sind?'* -- *'und die sitz animation ist ja jz auch anders'* -- und auf den Vorschlag, erst seinen 2c-Test abzuwarten: *'ja ich will das du jz das model richtig schoen machst hochwertig wie ein normales braun baer bnaby soll das aussehen und nebenbei will ich das du schonmal den code programmierst das man das baby finden und tamen kann'*.
* **Modell des Jungen jetzt, ohne auf den 2c-Test zu warten:** hochwertig, wie ein normales (echtes) Braunbaeren-Junges; auf dem Stand 2c (Fuesse, Beine, neue Sitz-Clips). Massstab: sein Babyfoto und das echte Tier aus der Spielkamera.
* **Code Finden + Zaehmen jetzt, parallel** (damit ist die Reihenfolge vom 09.11. fuer diese beiden Punkte ueberholt: sie kommen VOR Clip-Runde und B5a Gegenwehr).
* **Von Claude fuer die Laeufe gesetzt (Kevins Wort dazu steht noch aus, er kann es umwerfen):** Augen groesser als im Entwurf, Rumpf kuerzer und runder, Weg je Schritt mit dem Bein-Faktor (Fuesse gleiten nicht), Unterlid dunkel, Ohren gross und flauschig; Tierart des Jungen `ncbearcub` (der Erwachsene bleibt bis B5a `bear`); Finden nach seinen Antworten vom 08.11. (Weg A Wald + Weg C Koederplatz), alle Zahlen als Sandbox-Optionen; Wachsen zum Erwachsenen ist NICHT in dieser Version (B1b danach).

## Bild-zu-3D-Generator, Vorlagebilder aus dem Internet, Stockfoto-Regel (Kevin 10.11.2026 ~20:30)

Anlass: Kevin fragte, ob es bessere Programme als Blender gibt (*"im internet meinte einer opus 5.5 waer der 3d model gott davon hab ich noch ncihts gemerkt haha oder gibs noch besser programme die ich mir runterladen muss als blender"*). Claude: Blender ist nicht der Engpass; Tierformen per Skript sind die Schwaeche; ein Bild-zu-3D-Generator auf der 4090 koennte die Rohform liefern.

* Kevin woertlich: *"das ist nicht meine regel mit dem stockfoto ;D aber das echte problem ist ein bild zu haben wo ein kompletter baer drauf ist ^^ und ja sollst du wenn es das besser macht"*
* Kevin woertlich: *"such das bild zu 3d generatoren raus + bilder im internet von einen schoenen baeren wo der komplett drauf ist von oben bis unten :D"*
* Kevin woertlich: *"du darfst den baerne komplett nachbauen das ist kein problem"*
* **Folge:** Die Zeile in UEBERGABE.md ("Stockfotos: NUR ansehen ... nie in Modell/Textur") ist KEINE Regel von Kevin, sondern stammt aus Claudes Uebergabe-Notizen. Der Baer darf nach einem Vorlagebild komplett nachgebaut werden. (Claudes Auslegung, nicht Kevins Wort: fremde Fotos selbst weiter nicht nach GitHub hochladen, CLAUDE.md Abschnitt 9; fuer neue Vorlagen freie Bilder bevorzugen, z. B. gemeinfreie NPS/USFWS-Fotos.)
* **Auftrag:** Bild-zu-3D-Generatoren heraussuchen (lokal, RTX 4090) und Bilder eines schoenen Baeren suchen, auf denen er ganz zu sehen ist. Downloads weiter nur mit Name, Quelle, Groesse und Kevins Ja je Datei (CLAUDE.md Abschnitt 6).
* Kevin woertlich (zur Lizenz der Bilder): *"ist ja scheiss egal ob die bilder eine lizenz haben du klaust ja nicht das bild und veroeffenlticht es  sondern nur den baeren und der kann keine lizenz haben xD"*
* Kevin zu den sechs Downloads (ComfyUI + TRELLIS.2, 10,24 GB, Liste in `BILD_ZU_3D.md`): *"Ja, alle sechs"*
* Kevin woertlich (Bildwahl): *"dann nimm A fuers baby und E fuer den grossen und mach das bitte richtig schoen von allen seiten das es immer gut aussieht ^^"* -> A = `Bear cub on the beach (53167951257).jpg` fuer das Junge, E = `909's 2 5 Year Old Cub (Fat) (53214356524).jpg` fuer den GROSSEN Baeren (also auch der Erwachsene kommt neu aus dem Generator). Massstab: von ALLEN Seiten gut, nicht nur aus dem Blick des Fotos -> Rundum-Renders aus der Spielkamera pruefen.
* Kevin woertlich (10.11. ~20:45, als Claude die 15 Bewegungen fuer das Generator-Modell aufzaehlte): *"ja und den krallenhieb dann mal in schoener ;D"* -> Wunsch: der Krallenhieb (Hieb-Clips des Erwachsenen) soll schoener werden, wenn das neue Modell seine Bewegungen bekommt. Was genau ihn stoert, ist noch nicht gefragt/beantwortet. Gehoert zur Clip-Runde (STAND.md "Offen").
* Kevin (10.11. ~21:20) auf Claudes Frage, ob der Chat wegen der Fable-Woche (80 %) auf Opus umgestellt werden soll: *"Nein, Fable lassen"*. Als Claude daraufhin schrieb, er halte seine Runden so knapp wie moeglich: *"nichts so knapp wie moeglich so schoen wie moeglich muss das model werden ;D"* -> **Beim Modell geht Schoenheit vor Sparen:** lieber mehr Varianten, mehr Nacharbeit und mehr eigene Blicke auf die Blaetter als ein knapper Durchgang. (Claudes Auslegung: gespart wird an Geplauder und doppelten Schritten, nicht an der Arbeit am Modell; die 98-%-Wochenregel aus UEBERGABE.md gilt weiter, bis Kevin sie aendert.)

## Erster Spieltest B1a Finden und Zaehmen (Kevin 10.11.2026 ~22:20-22:45, Spielstand Apocalypse 2026-11-10_22-12-12, debug)

* *"NCBear_CubHere() eingeeben dann kam no cub:not inworld"* -> Fix 1 (zu fruehe isExistInTheWorld-Pruefung), danach *"ja der baer ist da"*, *"oh es sind jz 2 baeren da"* (Waise des ersten Versuchs, N5), *"und ja das rennt weg"* (ohne Futter, wie geplant).
* *"man kann garkein essen in die hand nehmen?"* (N6: Vanilla hat fuer Essen kein Ausruesten), Fuettern *"ging mit hinterherennen"*, *"vorher bekomtm man das feed fenster jan icht auf wenn man zuweit weg steht"*.
* Frage: *"was passiert wenn ich den baeren aufasammel und wieder hinsetze?"* (nur mit Debug-Gottmodus/unbegrenzter Traglast moeglich).
* Streicheln (Screenshot: Balken "Taming 33% / Food: 50 min / Petting: ready" gut lesbar): *"zuviel abstand beim streicheln aber danach tut der die hand unter den baeren das sah gut aus"* -> N7.
* Kevin zum Streichel-Abstand (N7), nach dem zweiten Streicheln: *"diesmal hat er aber richitg gestreichelt also lass das einfach so das kommt wohl auf den blickwinkel an"* -> N7 NICHT beheben, Streicheln bleibt wie es ist.
* *"wieso macht streicheln keinen sound wie bei tiere streicheln beim tierpfleger?"* -> Fix 3 (Streichel-Ton PetAnimalCalf, im Staging).
* *"und em hab ihn wohl jz getamed? aber kann jz nichtmehr mit dem machen also da steht auch nicht ueber den baeren das es meiner ist etc"* -> Zaehmen klappt; nach dem Zaehmen gibt es in B1a absichtlich nichts mehr (kein Namensschild, kein Folgen, keine Befehle) -- Kevin fragen, was zuerst kommt.
* Kevin zu den Spielnetz-Blaettern (10.11. ~23:05): *"ja hol dir noch ausn internet baeren bilder damit du es bauen kannst wie er grade steht ;D und fix noch den komischen schwanz hinten und das komische dinge auf den kopf und so wie du selbst gesagt hast die punkte"* -> neues Foto fuer das Junge: `vorlage_C_junges_steht.jpg` (Wikimedia Commons "Eurasian brown bear (Ursus arctos arctos) cub 14 months.jpg", CC BY-SA 4.0, 4378x2919, 11,8 MB; steht ruhig auf allen vier Pfoten, Gesicht gut zu sehen). Grosser Baer bleibt E, wird nachgearbeitet (Schwanz-Lappen, Kopf-Wulst, Augen, Krallen, Fell).
* Kevin (~23:15) waehrend der Modell-Lauf startete: *"hol dir auch ein bild vom hintern vom baeren damit du den schwanz hinten fixxen kannst"*, *"und vom stehenden baeren bilder damit das ROAR nicht komplett scheisse wieder aussieht"*, *"du brauchst bilder von jeden winkel ;D"* -> Referenzen aus Wikimedia Commons in `begleiter/ref_*.jpg` (nicht in Git): hinten (Grizzly cub and sow ... PD; Brown Bears Exploring Their Habitat, CC0; Bear ran onto the road ... panoramio, CC BY-SA 3.0), aufrecht (Ursus arctos - Norway, CC BY 2.0; Eurasian brown bear standing on rear legs, Skansen, CC BY-SA 4.0; Standing Grizzly Bear Cub, CC BY-SA 2.0); noch ausstehend wegen Wikimedia-Bremse: Mother and cub (PD), Grizzly bear cub walking (PD). Modell-Lauf mit diesen Referenzen neu gestartet (Workflow wf_ae849387-409); Brust/Bauch/Hinterteil werden zusaetzlich von vorn-unten und hinten geprueft.
* Kevin (11.11. ~00:00): *"ich will das er erst folgt wenn er getamed ist weil sonst ist das bestmmt zu leicht das man den einfach direkt mit nimmt ;D oder anbinden das soll auch nicht gehn"* -> (1) Folgen NUR fuer das eigene, gezaehmte Junge -- so steht es schon in `../_arbeit/baer_zaehmen/PLAN_B1B.md:59/65/212` (st == "tame" und owner). (2) Anleinen mit Seil darf nicht gehen -- ist ohne Cheat schon gesperrt: die Definition des Jungen setzt `canBeAttached` absichtlich nicht (`shared/BanditsNPCBearDefs.lua:97`), Vanilla fragt `animal:getBehavior():canBeAttached()` = `adef.canBeAttached` (Jar BaseAnimalBehavior:1735, Vorgabe false); nur der Debug-"Tier Cheat" zeigt die Option (`ISAnimalContextMenu.lua:173`). Gilt so bleibend, auch fuer das gezaehmte Junge und den grossen Baeren.
* Kevin (11.11. ~00:05) zur Zaehm-Dauer (vorher erklaert: mit Grundwerten gut 4 Spielstunden): *"und das soll standardmaessig laenger dauern als 4 ingame stunden eher so 12 ingame stunden ;D"* -> neue Vorgaben (Claudes Wahl, Kevin kann sie umwerfen): `BearFeedCooldownMinutes` 120 -> 180 und `BearTameMinFeedings` 3 -> 5, also mindestens 4 Pausen x 3 h = 12 Spielstunden (der Balken bleibt bis zur 5. Fuetterung bei hoechstens 99 %). Einbau NACH dem laufenden B1b-Zusammenbau (sonst Schreibkonflikt im Staging); Tooltips mit festen Zahlen mitziehen. Bestehende Spielstaende behalten ihre gespeicherten Sandbox-Werte.
* Kevin (11.11. ~00:08) korrigiert: *"nein nein ich will das streicheln und fuettern immer noch so oft geht nur es soll laenger dauern"* -> Abklingzeiten BLEIBEN (Fuettern 120 min, Streicheln 60 min, MinFeedings 3); stattdessen weniger Punkte je Handlung: `BearTameFeedPoints` 14 -> 4, `BearTamePetPoints` 8 -> 3 (Boni unveraendert). Rechnung (Claude): bestes Spiel = Lieblingsfutter, im Wechsel, jede Gelegenheit genutzt -> 6 + 4,5 + 3, danach je 2 h 9 + 4,5 + 3 = 16,5 -> 100 % nach etwa 12 Spielstunden; mit normalem Futter ~14 h. Der vorige Vorschlag (180 min / 5 Fuetterungen) ist damit VERWORFEN.

## Wachsen und Kampfkraft bis ganz gross (Kevin 11.11.2026 ~00:20) -- ERSETZT die Zeiten vom 08.11. (7 + 14 Spieltage)

* Kevin woertlich: *"das muss laenger dauern standardmaessig bin ich so fuer 100 tage bis max gross damit es sich richtig lohnt und man laengere runs spielen kann mit dem baeren ;D oder waere eine andere zahl passender weil gerade?"*
* Claudes Vorschlag (Kevin: *"ja mach das so als standard und in der sandbox einstellbar und die werte von baeren muessen pro tag steigen"*):

| Groesse | ca. ab Spieltag (nach dem Zaehmen) | neu |
|---|---|---|
| Jungtier 0,35 | 0 | kaempft nicht (versteckt sich) |
| Halbstark 0,75 | 15 | schwacher Prankenhieb gegen EINEN Gegner, wenig Schaden, wirft nicht um |
| 1,0 | 45 | Biss, Umwerfen wird moeglich (Chance waechst weiter) |
| Erwachsen 1,35 | 100 | Aufrichten mit Bruellen, Flaechenhieb, volle Kraft |

* **Fest:** Standard 100 Spieltage bis ausgewachsen; Wachstum vorne schneller, hinten langsamer; als Sandbox-Option einstellbar (Vorschlag "Tage bis ausgewachsen", 10 bis 365); gutes Fuettern beschleunigt etwas, Hunger bremst (aus 08.11.).
* **Fest:** Die Werte des Baeren (Schaden, Leben, Hunger/Durst-Bedarf, Traglast usw.) steigen JEDEN TAG ein Stueck mit der Groesse, ohne Sprung; neue Angriffe werden an den Meilensteinen der Tabelle freigeschaltet.
* Offen (Claudes Hinweis, Kevins Wort fehlt): ein 90-Tage-Baer sollte im Kampf lieber schwer verletzt fliehen als schnell sterben -- gehoert zu B5a Gegenwehr.
## Werte und Faehigkeiten des Baeren (Kevin 11.11.2026 ~00:30)

* Kevin woertlich: *"aber was fuer werte soll es geben und was fuer skills dazu das weiss ich noch nicht , ich weiss nur sowas wie , leben und schaden, und vllt noch ausdauer? und fischen als skill? fischen soll er ja auch koennen ab dann wann der kaempfen kann aber nur schlecht und dann am ende viel besser"* -- auf Claudes Vorschlag: *"genau traglast das stimmt auch noch ;D"*.
* **Werte (wachsen jeden Tag mit der Groesse):** Leben, Schaden, Ausdauer (rennen/kaempfen bis zum Verschnaufen, erholt sich beim Ausruhen), Traglast (10 / 40 / 100 wie 08.11.).
* **Faehigkeit Fischen:** ab Halbstark (Tag ~15), anfangs schlecht, am Ende viel besser -- Fang-Chance und Fischgroesse aus Groesse UND Uebung (Stufe 0-10 durch Benutzen).
* **Noch ohne Kevins Wort (Claudes Vorschlag):** Faehigkeit Kaempfen (durch Uebung: trifft/weicht oefter aus, braucht weniger Ausdauer), Faehigkeit Spuernase (riecht Zombies frueher, warnt mit Brummen).
## Muedigkeit und Schlafen im Kampf-Alltag (Kevin 11.11.2026 ~00:40)

* Kevin woertlich (zur Ausdauer-Erklaerung): *"genau schlafen wollte ich ja auch noch einbauen beim baeren das er auch so muede wird und schlafen muss und dann nichtmehr kaempft nur noch weg rennt bis du ihn schlafen schickst ;D oder erst selbst schlaeft aber wenn ein zombie in der naehe ist wacht er auf und rennt nur weg das ist noch besser!"*
* **Fest (Kevins Wahl "noch besser"):** eigener Wert Muedigkeit (langsam ueber den Tag, getrennt von der kurzen Ausdauer). Sehr muede -> kaempft nicht mehr, rennt nur noch weg. Er legt sich SELBST schlafen, wenn er muede ist; kommt ein Zombie in die Naehe, wacht er auf und rennt weg (kaempft nicht). Gehoert zum Schlaf-Plan `begleiter/SCHLAF_PLAN.md` (Fragen K1-K21) und zum Kampf (B5a).
* Offen (Claude fragt beim Bau): wohin rennt er -- zum Besitzer oder nur weg vom Zombie; ab wann "sehr muede"; schlaeft er bevorzugt auf dem Baerenbett.
* Kevin (11.11. ~00:45): *"und die spuehrnase auch einbauen aber in den einstellungen abschaltbar falls es jemand nervig findet wenn er staendig sagt zombie in der naehe ^^"* -> **Spuernase FEST:** riecht Zombies frueher und warnt mit Brummen; abschaltbar (Vorschlag: Sandbox-Schalter fuer den Server UND ein Schalter je Spieler/Baer, damit jeder sie fuer sich ausmachen kann); Warnung nicht staendig (Abklingzeit, nur bei neuen Zombies). Faehigkeit Kaempfen weiter ohne Kevins Wort.
* Kevin (11.11. ~00:50): *"und ein agilitaets skill wie bei den npc's das erhoeht die ausweichchance vom baeren das er garnicht erst getroffen wird, das levelt pro hit den er kassiert wie das leben das wer skill hoeher geht aber zusetzlich geht das leben auch hoch pro wachstums tage"*
  * **Fest:** Faehigkeit **Agilitaet** (Stufe 0-10): erhoeht die Ausweich-Chance (Treffer geht ganz daneben); steigt mit jedem Treffer, den er einsteckt.
  * **Fest:** **Leben** steigt auf ZWEI Wegen: jeden Wachstumstag mit der Groesse UND als Faehigkeit mit jedem eingesteckten Treffer (Claudes Lesart: Lebens-Bonus aus Uebung obendrauf).
  * Beleg zum Vergleich: bei den NPC-Crew-Figuren ist Ausweichen KEIN Skill, sondern ein fester Sandbox-Wert (`CompanionDodge`, Vorgabe 50 %, Deckel 95 %; NPC Crew `shared/BanditsNPCSkills.lua:966-975`). Beim Baeren wird es ein Skill. Vorschlag Claude: Deckel bei Stufe 10 um 40-50 %, damit er nie unverwundbar ist (Kevins Wort beim Bau).
* Kevin (11.11. ~01:00) auf Claudes Fragen (Kondition durch Rennen/Kaempfen + Wachstum? 40 % Ausweichen auf Stufe 10?): *"ja und kaempfen damit meinst du ja sicher schaden ^^"*
  * **Fest:** Faehigkeit **Kondition** (0-10): steigt durch Rennen, Kaempfen und vor allem Ausser-Puste-Kommen (gemuetliches Hinterherlaufen zaehlt kaum); bringt groessere Ausdauer-Leiste und schnellere Erholung -- zusaetzlich zum taeglichen Wachstum.
  * **Fest:** Agilitaet Stufe 0 = 5 %, Stufe 10 = 40 % Ausweichen (Hoechstwert als Sandbox-Option); Aufsteigen hinten langsamer.
  * **Fest:** Faehigkeit **Kaempfen** = mehr **Schaden**: steigt mit jedem Treffer, den er AUSTEILT -- zusaetzlich zum Schaden aus dem taeglichen Wachstum (gleiches Muster wie Leben und Ausdauer: Wert waechst mit dem Alter, Faehigkeit mit der Uebung).
* **Gesamtbild Werte/Faehigkeiten (Stand 11.11. 01:00):** Werte aus dem Wachstum (taeglich): Leben, Schaden, Ausdauer, Traglast. Faehigkeiten 0-10 aus Uebung: Agilitaet (eingesteckte Treffer -> Ausweichen 5-40 %), Leben-Bonus (eingesteckte Treffer), Kondition (Anstrengung), Kaempfen (ausgeteilte Treffer -> Schaden), Fischen (Fischen, ab Halbstark), Spuernase (Warnung, abschaltbar). Dazu Muedigkeit/Schlafen (eigener Abschnitt oben).
* Kevin (11.11. ~01:25) zum Schaden-Bonus der Faehigkeit Kaempfen: *"mach +70% bei stufe 10 ein baer der dir eine richitg verpasst da sind sogar bett matzreatzen komplett durch das ueberlebt eigtl keiner xD"* -> **Fest: Kaempfen Stufe 10 = +70 % Schaden** (obendrauf auf den Wachstums-Schaden). Grundlage der Entscheidung (Claudes Rechnung aus dem Jar 42.22.2, ungespielt): Zombie-Leben normal 1,8-2,1 (zaeh 3,5-3,8, zerbrechlich 0,5-0,8; `IsoZombie` Zaehigkeit); erwachsener Baer heute Hieb 1,0 / Biss 1,2 / Zerfleischen 1,8 direkt vom Leben (`NCBearFight.lua:92`) -> meist 2 Treffer; Spieler Staerke 5 + Waffe 5 ~ Waffenschaden x 0,4 je Treffer (Baseballschlaeger 5-6, Axt ~4, Machete 2). Mit +70 %: Hieb 1,7, Biss 2,04, Zerfleischen 3,06 -> normale Zombies fallen oft schon beim ersten Biss/Zerfleischen, beim Hieb meist nach 2.
## Anzeige ueber dem Baeren, frei einstellbar (Kevin 11.11.2026 ~01:35)

* Kevin woertlich: *"achso ich brauch noch eine einstellbar anzeige fuer den baeren z,b wie namen ein/ausblenden ueber den baeren dafuer noch HP/ausdauer anzeige (wie bei computer spiel cheats ESP(wallhack) so eine anzeige einblenden lassen quasi mit den werten und jeden wert einzelnd anzeigen lassen erlauben z.b auch noch hunger/durst/muedigkeit das soll dann da stehn im balken oder als zahl frei auswaehlbar und groessen einstellung wie gross die anzeige ist und wenn er ausweicht soll da DODGE stehen wie bei der npc's"*
* **Fest:** Anzeige ueber dem Baeren, je Spieler einstellbar: Name ein/aus; jeder Wert einzeln (Leben, Ausdauer, Hunger, Durst, Muedigkeit; Claudes Ergaenzung: Zaehm-Fortschritt) ein/aus und je Wert **Balken ODER Zahl** frei waehlbar; **Groesse** der Anzeige einstellbar; beim Ausweichen schwebt **"DODGE"** ueber ihm wie bei den NPC-Crew-Figuren (NPC Crew `client/BanditsNPCSkillsHooks.lua:134-141` barkDodge, Text `UI_BN_Skill_Dodge`).
* **Weg (Claudes Vorschlag):** Einstellungen als Mod-Optionen des Spiels je Spieler (wie NPC Crew `client/BanditsNPCModOptions.lua`), nicht Sandbox; billig gezeichnet. Die Werte kommen dazu, sobald es sie gibt (Leben/Ausdauer mit Wachsen/Kampf, Hunger/Durst/Muedigkeit mit Beduerfnissen/Schlafen). Name ein/aus und Groesse koennen gleich nach B1b kommen (B1b baut gerade das Namensschild).
* Kevin zum Zaehm-Fortschritt in den Anzeige-Optionen: *"Zaehm-Fortschritt (mein Zusatz) nein das will jeder wissen das geht ja danach eh weg ;D"* -> der Zaehm-Balken bleibt IMMER sichtbar (keine Einstellung dafuer); er verschwindet von selbst nach dem Zaehmen.
* Kevin: *"den rest wil ich aber ;D"* -> **Fest:** alle uebrigen Anzeige-Einstellungen wie vorgeschlagen (Name ein/aus; Leben, Ausdauer, Hunger, Durst, Muedigkeit je aus/Balken/Zahl; Groesse als Schieberegler; "DODGE" ein/aus), je Spieler unter Optionen -> Mods.
## Mitfahren im Auto und Unstuck (Kevin 11.11.2026 ~00:55)

* Kevin woertlich (auf "steigst du ins Auto ..., bleibt es stehen"): *"warte mal der kann nicht ins auto einsteigen wie die npc's ? das soll der aber koennen wenn er getamed ist und genauso wie unstuck button"*
* **Fest:** der GEZAEHMTE Baer kann wie die NPC-Crew-Figuren mit ins Auto (NPC Crew: `client/BanditsNPCPersistence.lua:7948` P.BeginRide, Fahrzeug-Panel `client/ISUI/BanditsNPCVehiclePanel.lua`) und bekommt einen **Unstuck-Knopf** wie die NPCs (NPC Crew `client/BanditsNPCPersistence.lua:9613` P.Unstuck mit Abklingzeit :9446-9475).
* Offen fuer die Forschung (Claude): Engine-Weg fuer ein Tier im Auto -- Vanilla kennt Tiere im Anhaenger/Fahrzeug (`shared/TimedActions/Animals/ISAddAnimalInTrailer.lua`, Def-Feld `canBeTransported`) -- gegen den NPC-Weg (Figur verschwindet beim Einsteigen und kommt beim Aussteigen wieder); Unstuck = zum Besitzer holen ueber einen belegten Weg (z. B. ins Fahrzeug aufnehmen/absetzen) statt unbelegtem Teleport. Grosser Baer (1,35) passt in kein normales Auto -- Groessen-Regel klaeren (Kevins Wort).
* Nicht mehr in B1b (laeuft schon in der Nachbesserung); kommt in die naechste Code-Version.
* Kevin auf die Frage (jedes Auto wie die NPCs, oder ab einer Groesse nur Transporter/Anhaenger?): *"sowie unser npc crews"* -> **Fest:** der Baer faehrt GENAU WIE die NPC-Crew-Figuren mit -- in jedem Auto, unabhaengig von seiner Groesse (Weg der NPCs: beim Einsteigen verschwinden, beim Aussteigen wieder da; Einzelheiten aus NPC Crew `client/BanditsNPCPersistence.lua` P.BeginRide ff. lernen, nicht kopieren).
## Markierung oben am Bildschirm fuer das wilde Junge (Kevin 11.11.2026 ~01:10)

* Kevin woertlich: *"okay dann mach mir bitte dafuer wie beim npc crew mod diese anzeige oben in den bildschirm mit einen baby baeren wild das du jz zeichnest nebenbei und mir dann vorstellst so 3 versionen und ich entscheide mich und dann so ein pfeil in die richtung also wie beim npc crew wenn ein npc dude spawnt"*
* Weg (Beleg): NPC Crew zeigt den Ueberlebenden-Pfeil ueber Bandits' Markierung `BanditEventMarkerHandler.set(id, icon, dauer, x, y, farbe, text)` mit fester Id, die alle 0,4 s neu gesetzt wird (NPC Crew `client/BanditsNPCSpawn.lua:238-319`, Symbol `media/ui/friend.png`, Farbe Gruen; Bandits `42.22/media/lua/client/BanditEventMarkerHandler.lua:6`, Zeichnen `BanditEventMarkers.lua:160-200`: farbiger Kreis `eventMarkerBase.png` + Pfeil-Ring + Symbol 96x96). Fuer das Junge: eigenes Symbol `media/ui/BanditsNPCBearCub_marker.png` (Name im Stil), Farbe Honig-Braun, Text "Bear cub nearby" (7 Sprachen), nur wenn Bandits geladen ist (Existenz-Riegel).
* Drei Entwuerfe gezeichnet (Skript `../_arbeit/baer_icon/zeichne_icons.py`, Dateien dort): 1 Kopf von vorn, 2 ganzes Junges von der Seite, 3 Kopf mit traurigem Blick + Wimmer-Bogen. Blatt `spiel/icon_auswahl.png`. **Kevins Wahl steht aus.**
* Kevin zu den drei Piktogrammen: *"keins davon das soll schon echter aussehn und suesser ;D"*, dann mit einem Beispielbild (Cartoon: sitzendes braunes Baerenjunges von vorn, grosse Glanzaugen, helle Schnauze, Laecheln, heller herzfoermiger Brustfleck, Pfotenballen, dunkle Umrisslinie): *"ich weiss das ist nicht echt aber suesser ^^"* -> Stil-Vorlage `begleiter/kevin_icon_vorlage.png` (fremdes Bild: NUR ansehen, nicht abzeichnen oder kopieren, nicht in Git). Neue Entwuerfe in diesem suessen Cartoon-Stil, eigene Zeichnung.
* Kevins Wahl fuer das Markierungs-Symbol (zweite Runde, Cartoon-Stil, Blatt `spiel/icon_auswahl_2.png`): *"ich will 1 haben"* -> **Fest: Entwurf 1, Kopf von vorn** (`../_arbeit/baer_icon/BanditsNPCBearCub_marker_W1.png`, als Einbau-Datei kopiert nach `../_arbeit/baer_icon/BanditsNPCBearCub_marker.png`; Ziel im Mod: `42/media/ui/BanditsNPCBearCub_marker.png`). Kreisfarbe wie auf dem Blatt (im Spiel kraeftiges Orange, weil Bandits die Farbe mit sich selbst multipliziert) -- Kevin hat dazu nichts gesagt, bleibt so bis zu seinem Wort. Einbau in der naechsten Code-Version.
## Karten-Markierung und Unstuck-Knopf (Kevin 11.11.2026 ~01:35)

* Kevin (nachdem er sein Junges nach dem Neuladen nicht mehr als gezaehmt sah und nicht fand): *"und wie find ich den ich brauch nen map marker mit unseren baeren icon so klein auf der mini map und der grossen karte ;D und spaeter irgentwo ein icon ingame damit unstuck geht z.b ^^"*
* **Fest:** eigener Baer als kleines Baeren-Symbol (Entwurf 1, Kopf von vorn) auf der Mini-Karte UND der grossen Karte -- Weg wie NPC Crew `client/ISUI/BanditsNPCMiniMap.lua` (Render von ISMiniMapInner und ISWorldMap umwickeln, `mapAPI:worldToUIX/Y(x, y)` belegt in Vanilla ISWorldMapSymbols.lua/ISWorldMap.lua:478), nicht kopieren.
* **Fest (spaeter):** ein Knopf/Symbol im Spiel, ueber das man z. B. Unstuck ausloest (wo genau: Kevins Wort beim Bau; NPC Crew hat Unstuck mit Abklingzeit, `client/BanditsNPCPersistence.lua:9613`).
## B1b gespielt + Baeren-Fenster (Kevin 11.11.2026 ~01:45)

* Kevin nach `NCBear_CubTame(100)`: *"okay klappt jz hab den getamed und der folgt aber ich wll noch spaeter eine richtige UI die aufgeht wenn ich V druecke (einstellbar in den keystings)"* -> **Folgen im SP gespielt: klappt.**
* **Fest (spaeter):** eigenes Baeren-Fenster, das mit **V** aufgeht; Taste in den Tastenbelegungen des Spiels einstellbar (Weg wie NPC Crew `client/BanditsNPCModOptions.lua` crewKey/OnKeyPressed :138-155, lernen, nicht kopieren). Gehoert zu "Befehle + Fenster" (STAND Offen); Inhalt (Befehle, Werte, Faehigkeiten, Name, Unstuck ...) beim Bau mit Kevin klaeren.
## Laerm, Zombies und das Junge (Kevin 11.11.2026 ~01:50, beim Spielen von B1b)

* Kevin: *"kan ndas sein das der baer weg rennt wegen lauten sounds wie der grosse baer das probelm ahtte also wenn ich renne oder so?"* -> JA, belegt: die Engine laesst jedes nicht wilde Tier vor jedem Nicht-Fahrzeug-Laerm `radius + 10` Kacheln wegrennen (`respondToSound`, Jar `dec/IsoAnimal.java:764-806`, Forschung `spiel/b1b_forschung_b1b.md` Befund 4); B1b holt es nur im naechsten Takt zurueck (PLAN_B1B 1.2). **Fix (naechste Version):** wie beim grossen Baeren (Lauf baer-laerm, `NCBearFight.lua:28-38` fleeStop) die Laerm-Flucht des GEZAEHMTEN Jungen sofort abbrechen; wilde/scheue Junge duerfen weiter erschrecken.
* Kevin: *"und da stand direkt ein zombie neben den baeren und der ist nicht weg gelaufen"* -> stimmt: das Junge hat `fleeZombies = false` (`shared/BanditsNPCBearDefs.lua:91`) und noch kein eigenes Verhalten. Kevins Regel vom 08.11. (ENTSCHEIDUNGEN.md:8): **Jungtier kaempft nicht, versteckt sich bei Zombies hinter dem Besitzer** -> naechste Version (wilde Junge: fliehen vor Zombies).
* Kevin: *"aber du must auch noch machen das die zombies baeren angreifen und so"* -> **Fest:** Zombies greifen Baeren an (Engine laesst Zombies nie Tiere angreifen, `AttackState`; muss selbst gebaut werden; stand als "Biss der Zombies" schon in STAND Offen und gehoert zu B5a Gegenwehr). Vorschlag Claude (Kevins Wort fehlt): Zombies greifen jeden GEZAEHMTEN Baeren an, auch das Junge (darum versteckt es sich); wilde Junge nicht (die fliehen).
* Kevin zur Frage, ob Zombies auch das gezaehmte Junge angreifen: *"ja nur ungetamte greifen die nicht an"* -> **Fest:** Zombies greifen JEDEN gezaehmten Baeren an, auch das Junge; ungezaehmte (wilde/scheue/angefuetterte) Junge greifen sie nicht an.
## Heilen (Kevin 11.11.2026 ~01:55)

* Kevin woertlich: *"ja und auto heilung aber langsam und wir koennen den baeren manuel heilen oder auch gut unsere npc's duerfen spaeter auch noch den baeren heilen per schalter 😃 aber erst wenn generel der heiler job kommt ^^"*
* **Fest:** (1) Der Baer heilt sich langsam von selbst. (2) Der Spieler kann ihn von Hand heilen (womit genau -- z. B. Verband/Desinfektion -- im Bau vorschlagen). (3) Spaeter duerfen NPC-Crew-Figuren den Baeren heilen, per Schalter -- aber ERST wenn es in NPC Crew den allgemeinen Heiler-Job gibt (Naht zu NPC Crew).
* Kevin: *"aber heilen soll echt langsam gehn von alleine ohne das man aktiv heilt weil bei den npc's ist das auch schon zu schnell ;D"* -> **Fest:** Selbstheilung ECHT langsam (Vorschlag Claude: etwa 1 % des Lebens je Spielstunde, also rund 4 Spieltage von fast tot bis voll, als Sandbox-Option); aktives Heilen deutlich schneller. Nebenbei Kevins Meinung zu NPC Crew: dort heilen NPCs von selbst zu schnell (gehoert in die NPC-Crew-Sitzung, nicht hierher).
* Kevin: *"ja das klingt gut aber beim schlafen soll er viel schneller geheilt werden das er quasi immer voll ist nach dem er paar ingame std geschlafen hat"* -> **Fest:** wach ~1 %/Spielstunde (Sandbox); **im Schlaf viel schneller**, so dass er nach ein paar Spielstunden Schlaf praktisch voll ist (Vorschlag Claude: ~15 %/Spielstunde -> von fast leer in ~6-7 h Schlaf voll; Sandbox-Option).
## Nachtschicht 11.11.2026 -- Kevins Freigaben (~01:50)

* Auf Claudes Fragenliste (12 Punkte mit Vorschlaegen) antwortete Kevin: *"ja alles so wie du vorgeschlagen hast"*. Damit gilt:
  1. Zuerst Code B1c: Register-Selbstheilung (N9), Laerm-Flucht des gezaehmten Jungen abfangen, Verstecken hinter dem Besitzer bei Zombies (wilde Junge fliehen), Mitfahren wie NPC Crew, Unstuck, Bildschirm-Markierung mit Symbol 1 + Pfeil, Karten-Symbol (Mini + gross), Anzeige-Optionen Name ein/aus + Groesse.
  2. Danach Modell des Jungen: Generator-Junges mit Skelett, Gewichten, allen 15 Clips, Gehen schneller; ersetzt den Platzhalter in NCBearTest, wenn der Gegenpruefer es besser findet.
  3. Grosser Baer bleibt diese Nacht 2c; vom Generator-Baeren nur Blaetter (Kopf-Frage entscheidet Kevin selbst).
  4. Wenn Zeit: Wachsen 100 Tage + taeglich steigende Werte (Plan + Bau); Kampf/Zombie-Angriffe/Heilen erst nach Kevins B1c-Test.
  5. Unstuck vorerst als Rechtsklick am Baeren ("Call to me"), Abklingzeit 5 min; spaeter ins V-Fenster.
  6. Mitfahren nur bei "Follow me" und hoechstens 15 Kacheln Abstand beim Einsteigen; beim Aussteigen neben dem Auto.
  7. **Kevins Wort fuer `animal:setVariable("animalRunning", false)`** (eiserne Regel, Ausnahme je Methode: belegt am Spieler V:ISMilkAnimal.lua:138/ISPetAnimal.lua:37 und am Zombie B:ZAMove.lua:31, am Tier nur in unserer gespielten NCBearFight.lua:457/1064) -- ERLAUBT, damit das Junge gehen kann.
  8. Markierungskreis bleibt orange; Karten-Symbol nur fuer den eigenen Baeren.
  9. B1b-Einzelheiten bleiben: Schild-Zeile 2 nur blasser, Bleiben-Radius 12, MP-abgemeldeter Besitzer -> Junges wartet als follow (A7).
  10. MP-Fragen B1a: Uhren nur online (B2), reifer Koeder verfaellt nach 8 Tagen (B5), A3 entscheidet der MP-Test.
  11. 2c-Fragen G1-G3 bleiben liegen.
  12. Wie immer: sichern, committen, pushen; Test-Mod nur bei geschlossenem Spiel; kein --echt, keine Downloads.
## Neues Junges (Generator) -- Kevins erster Blick auf das Blatt (11.11.2026 ~15:00)

* Kevin: *"da bin ich mal gespannt also perfekt sieht der ja nicht aus auf den bildern von dir ^^"* und *"besonders die gesichtsgroesse sieht zu klein aus also das maul"* -> **naechste Modell-Runde:** Gesicht/Schnauze (Maul) des Jungen deutlich groesser, Kopf in Kevins Kamera nicht so gesenkt (Gesicht sitzt heute klein unten am Umriss, Gegenpruefer `spiel/rig_GEGEN.md`); dazu die bekannten Restpunkte (Ohren von vorn wie Scheiben, Fressen erreicht den Boden nicht, von hinten Ei auf Stelzen). Massstab Foto C und Kevins Babygesicht-Vorlage. Erst nach dem Wochen-Reset (Woche 93 %).
* Kevin (11.11. ~15:05, nach dem Blatt `spiel/rig_KEVIN_junges_spielfertig.png`, noch nicht im Spiel gesehen): *"ich find sogar unser altes baby model sieht besser aus um ehrlich zu sein xD"* -> Lehre: der Generator-Weg liefert nicht von selbst ein schoeneres Junges; Kevins Blick auf das Blatt entscheidet. Rueckweg jederzeit moeglich: alter Entwurf `../_arbeit/baer_baby/entwurf/NCBearCub.glb` (6c3f0a96) + `NCBearCub.png` (2ee25f24), Sicherung `Zomboid/backups/NCBearTest/NCBearTest_vor_junges_neu_2026-11-11_143915.zip` (beim alten Modell geht das Junge wieder nur 0,52 Kacheln/s).
* Kevin: *"ich will das du die 2 baby varianten einbaust zum spawnen und beide grosse!"* -> Testhilfe gebaut (nur NCBearBench*, nie nach NPC Crew), Staging `../_arbeit/baer_vergleich/mod/` (9 Dateien): altes Junges als Vergleichs-Art `ncbearcubalt` (lebend, Modell `NCBearBenchCubAlt`), grosser Generator-Baer E als STANDMODELL in zwei Farben (Gegenstaende `NCBear.BenchGenEBraun` / `NCBear.BenchGenEFototon`, 1,96 m lang wie der 2c-Baer bei 1,0, ohne Knochen/Bewegung). Befehle `NCBear_Vergleich()`, `NCBear_CubAlt()`, `NCBear_GenE()`. Einbau in NCBearTest erst bei geschlossenem Spiel (11.11. ~15:20 lief es).

## Wachsen: Wechsel auf das grosse Modell ab Tag 15 (Kevin 11.11.2026 ~15:20, beantwortet F11)
Anlass (Spieltest B1d, woertlich): *'der wird garnichtmehr groesser ab tag 15 oder so'* -- *'und das model aendert sich auch nicht'* -- *'und was sagt die konsole wegen den hp und so?'*. Konsole (console.txt): Werte wie geplant (Tag 15 Leben 150, Tag 45 Leben 255, Tag 100 Leben 400 / Ausdauer 160 / Traglast 100 / Schaden 1,0), Bild bleibt absichtlich bei 0,75 (`PLAN_B1D.md` 0.10/1.2), keine roten Fehler.
* Frage: 'Ab wann soll das Junge zum grossen Baeren werden?' (Claudes Vorschlag: ab Tag 15 wird das Junge zum grossen Baeren in klein, mit 0,75, und waechst bis Tag 100 auf die volle Groesse 1,35; ein Babygesicht in gross saehe komisch aus, die Fuesse wuerden mehr rutschen). **Kevin: *'Ab Tag 15 (halbstark)'*.**
* Folge: Lauf baer-b1e (Code) schaltet den vorbereiteten Modellwechsel ein: beim Erreichen von Halbstark wird das Junges-Modell gegen das grosse Modell getauscht, das dann bis 1,35 mitwaechst; NICHT die alte Art `bear` (NCBearFight greift sofort an = B5a). Welches grosse Modell (2c oder Generator, Farbe, Kopf) bleibt Kevins offene Frage -- der Wechsel nimmt das jeweils aktuelle grosse Modell.

## Altes Junges ist besser (Kevin 11.11.2026 ~15:25, im Spiel verglichen)
Woertlich: *'wie lass ich das alte model wachsen? vom alten baby baeren'* -- *'ok ich muss wohl neustarten damit das geht'* -- *'der neue baby baer laeuft auch wie eine giraffe oder so xD also das alte ist definitiv besser ^^'*.
* **Entscheidung: das ALTE Junge (Entwurf baer-baby, `../_arbeit/baer_baby/entwurf/NCBearCub.glb` 6c3f0a96 + `NCBearCub.png` 2ee25f24) kommt zurueck** als Modell der Art `ncbearcub` (Stand vor Test-Mod-Commit f10621f; Gehen 0,52 / Rennen 2,47 Kacheln/s, dazu passen die B1c-Folgen-Werte). Einbau automatisch, sobald Kevins Spiel zu ist (Sicherungen `NCBearTest_vor_altes_junges_*`/`_mit_`). Das Generator-Junge bleibt nur als Arbeitsstand (`../_arbeit/baer_gen/`, Sicherung `NCBearTest_mit_junges_neu_2026-11-11_*.zip`).
* Neue Testhilfe `NCBear_CubAltSize(0.35 .. 1.35)` (nur NCBearBench*, seit 15:21 in NCBearTest, e92835b): stellt alte Vergleichs-Junge auf eine Groesse.
* Lauf baer-b1e (Modellwechsel ab Tag 15) misst und plant jetzt mit dem alten Jungen (Skript `../_arbeit/baer_zaehmen/workflow_baer_b1e.js`).

## Markierung oben groesser (Kevin 11.11.2026 ~15:30, nach dem Test mit Bandits)
Woertlich: *'ich dachte in der mitte kommt schon ein symbol wenn ein bear in der naehe ist brauch ich dafuer eine zusatz mod?'* -- *'hab nur die baeren mod aktiv grade ;D'* -- (mit Bandits, Bild 3840x2054) *'okay das geht schonmal aber waer cooler wenn das symbol was groesser waere zumindestens bei 4k aufloesung'*.
* Befund: Bandits zeichnet Kreis, Pfeil und Symbol in fester Groesse 96 Pixel (Bandits 42.22 `client/BanditEventMarkers.lua:7`, `:174`, `:192-193`), daher bei 4K klein; ohne Bandits gibt es die Markierung nicht (Existenz-Riegel).
* Folge: als Punkt 7 in Lauf baer-b1e -- Markierung waechst mit der Bildschirmhoehe (1080 = 1,0 / 4K = 2,0) und ist in den Mod-Optionen einstellbar; Weg (eigenes UI-Element oder belegtes Skalieren) entscheidet die Forschung mit Beleg.

## Grosser Baer sitzt (Kevin 11.11.2026 ~15:40, Stand baer-2c gespielt)
Woertlich: *'sag mir wie ich den grossen baeren zum sitzen bekomme'* -- (NCBear_SpawnLive(), NCBear_Sit(20), Bild aus der Spielkamera) *'okay geil der sitz schonmal viel besser als frueher'*.
* Sitzen nach Vorlage (Lauf baer-2c) im Spiel bestaetigt. Die drei Kopf-Punkte G1-G3 (Buckel hinter dem Kopf, dunkler Ring, Blick nach oben) hat Kevin nicht angesprochen -- weiter offen, bei Gelegenheit fragen.

## Aufrichten + Bruellen sieht schlecht aus (Kevin 11.11.2026 ~15:45, NCBear_AnimTest("rear") im Spiel)
Woertlich: *'wie mach ich das der schreit'* -- (Bild aus der Spielkamera, Baer von vorn aufgerichtet) *'das sieht scheisse aus das must du noch fixxen guck dir unsere bilder an aus dem internet wie echte baeren stehen und bruellen'* -- *'da sieht das model auch komisch aus dabei ;D'*.
* Gesehen (Claude): aufrecht wie eine steife Saeule, Beine kurz und gerade, Vorderbeine stehen seitlich ab wie kleine Arme, Rumpf ein gerades Rohr; Zaehne beim Bruellen sind zu sehen.
* Vorlagen: `begleiter/ref_aufrecht_vorn.jpg`, `ref_aufrecht_seite.jpg`, `ref_aufrecht_schraeg.jpg` (Wikimedia), `kevin_bruellen_vorlage.webp`; dazu Netzbilder nur ansehen.
* Folge: Lauf baer-rear (Modell + Clip): NCBear_Rear neu (Dauer 3,0 s und Ton-Zeitpunkte bleiben) UND die Koerperform beim Aufrichten (Gewichte/Netz), andere Clips bit-gleich, Sitzen darf nicht schlechter werden.

## Arbeitsweise: zwei Spuren immer weiter (Kevin 11.11.2026 ~15:55)
Woertlich: *'kannst du bitte die baeren funktionen weiter bauen + unseren grossen baeren und den neuen grossen baeren machen also fuer alle 3 sachen eigne workflows von mir aus auch 10agenten pro workflow hauptsache es sieht gut aus'* -- *'und ich will jz immer das du das model/animation weiter machst + nebenbei die funktionen einbauchst als odas baeren menue und so du weisst schon was ich meine ^^'*. -- *'weil wenn du nur model machst das hat letzdens 9std gedauert da werden wir niemals fertig'*.
* **Fest:** immer eine Modell-/Animations-Spur UND eine Funktionen-Spur gleichzeitig (je hoechstens 10 Agenten je Workflow, getrennte Dateien). Nach jedem fertigen Lauf: selbst pruefen, einbauen sobald das Spiel zu ist, Commit/Push, dann SOFORT den naechsten Lauf derselben Spur starten (ohne zu fragen; Agentenzahl und Verbrauch kurz nennen). Wochenlimit-Regel bleibt (bis 98 %, dann anhalten + Uebergabe).
* Naechste Funktionen nach baer-b1e: **Baeren-Menue/Fenster** (Kevin nennt es ausdruecklich: V-Taste, Befehle Folgen/Bleiben/Sitz/Frei/Komm her/Passiv, Namensschild, Balken, Rechtsklick), danach B5a Kampf. Naechste Modell-Schritte nach baer-gross/baer-gen-gross: Kevins Wahl grosser Baer (2c oder Generator, Farbe), dann Clip-Runde-Reste (Toe0, Pranke beim Aufrichten, Liegen), Junges (Augen, Rumpf, Aufrichten des Jungen).

## Altes Junges: Baerenfuesse und Sitzen wie der grosse Baer, Gesicht und Gang bleiben (Kevin 11.11.2026 ~16:45)
Woertlich (nach den Bilderreihen `spiel/rig_KEVIN_junges_spielfertig.png` und `spiel/baby_entwurf.png`): *'ja ausser auf dem foto da sieht das noch schlimmer aus haha'* -- *'sieht das aktuell wirkloch noch genau so aus?'* -- *'und das baby hat echt so menschen fuesse noch? wenn ja kannst du das auch noch abaendern das es beim sitzen nicht so scheisse aussieht dann? sondern wie unser grosser baer der schon fast fertig ist? ;D'* -- *'genau das gesicht muss so bleiben das wirkt suess ;D das ist gut so und gang sieht ja auch normal aus ^^'*.
* Ja: das alte Junge (6c3f0a96) stammt aus dem grossen Baeren VOR baer-2c (Menschenfuss, alte Sitzhaltung; `../_arbeit/baer_baby/fix_baby.md`).
* **Fest:** Lauf baer-junges-fuss (8 Agenten, Skript `../_arbeit/baer_junges_fuss/workflow_baer_junges_fuss.js`): Fuesse/Beine wie der 2c-Baer im Junges-Massstab, Sitz-Clips aus den 2c-Clips umgerechnet (wiederholbar), **Gesicht/Kopf bit-gleich, Gang (alle anderen Clips) byte-gleich**.

## Nachtschicht 11./12.11.2026: Freigaben (Kevin 11.11.2026 ~18:25)
Fragen (ueber die Projekte-Sitzung gestellt) und Kevins Antwort woertlich: *'alles wie du gesagt hast aber bei 6 weiss ich das nicht ;D deswegen machst du das am besten selbst'*.
* 1 ja: fertige, selbst gepruefte, UNGESPIELTE Staende nachts in NCBearTest kopieren (nur bei geschlossenem Spiel, Zip vorher/nachher, Commit+Push).
* 2 A: der ueberarbeitete grosse Baer (Lauf baer-gross: Aufrichten/Bruellen, Koerperform, Kopf im Sitzen) ERSETZT den 2c-Baeren im Spiel; alter Stand im Zip.
* 3 ja: der Generator-Baer nur als Vergleich per Testbefehl `NCBear_GenLive()` (braun + Fototon); Kevin waehlt spaeter.
* 4 ja: B1e-Reste in den naechsten Funktionen-Lauf -- Meldungen beim grossen Baeren "bear" statt "cub"; Baer ohne Koerper (Absturz im Wechsel-Bild)
  erscheint von selbst wieder.
* 5 ja: Funktionen-Reihenfolge Baerenfenster (V) -> B5a Kampf (alte NCBear*-Dateien bekommen NPC-Crew-Namen) -> Schlafen; B5a darf nachts starten.
* 6 "machst du das am besten selbst": fuer die Nacht stellt sich die Sitzung EIGENE Wecker (Cron, nur in dieser Sitzung, verfallen mit ihr):
  Start 20:03 nach dem 5-h-Reset, danach alle ~15 min Verbrauch pruefen -- 5 h ab 85 %: laufende Workflows anhalten (TaskStop), nach dem Reset mit
  derselben Lauf-ID fortsetzen; Woche ab 98 %: alles anhalten, Uebergabe schreiben, sichern. Am Morgen auf Kevins Stopp Wecker loeschen.
* Nachtrag ~18:30, woertlich: *'ja arbeite an den baeren models + den code ingame fuer die funktionen damit wir ueberall weiter kommen du siehst ja
  selbst ob der baer schoen aussieht wenn du meinst er ist schoen genug und die anitmtionen passen gut dann kannst du ja erstmal mir das zeigen
  morgen und ich entscheide dann'* -> Modelle nachts selbst beurteilen (Blatt aus der Spielkamera neben die Fotos) und nachbessern, bis sie schoen
  sind; erst dann fuer Kevin morgen zeigen (Blatt + Testweg). Er entscheidet dann; der alte Stand bleibt je Einbau im Zip.
* Nachtrag ~18:35, woertlich: *'du machst beide baeren schoener baby und die grossen okay? also 3 baeren gleichtzeitig wenn das geht ;D ausser du
  sagst jz das ist zu viel und kostet zuviel tokens ^^'* -> ab 20:03 alle drei Modell-Laeufe gleichzeitig (baer-gross, baer-gen-gross,
  baer-junges-fuss) plus der Funktionen-Lauf; parallel kostet nicht mehr Tokens, das 5-h-Fenster ist nur frueher voll (dann Pause bis zum Reset).
* Nachtrag ~18:40, woertlich: *'gut und alle funktionen einbauen noch vom baeren du weisst ja bescheid was ich alels wollte die ganzen skills das
  schoene ui und alles'* -> Funktionen-Spur nachts der Reihe nach durch ALLES (Liste STAND.md oben "Funktionen-Liste"); offene Kleinfragen mit dem
  empfohlenen Weg bauen und morgens als Liste zeigen; das UI soll schoen sein (Kevins Wort).

## Jar-Ausnahme getTextOrNull mit Platzhalter-Argumenten (Kevin 12.11.2026 ~04:25)
Anlass: Turret- und NPC-Crew-Sitzung melden je Bear-Text mit Platzhalter eine Warnung "Missing arguments for UI_BN_Bear_*" (MissingFormatArgumentException
'%1$s', console.txt 12.11. ab 04:09, je Schluessel einmal je Sitzung; Restwarnung aus Fix 2 vom 10.11.). Frage: getTextOrNull mit "%1".."%9" als
Argumenten wie NPC Crew seit v3.11.19 (`shared/BanditsNPC.lua` BanditsNPC.T, ~:2843-2870; Beleg dort: Jar Translator.getTextOrNull(String, Object...)
ruft reportMissingArgumentsFromPastAbuse -> text.formatted(args)) -- in Vanilla- und Bandits-Lua NICHT als Aufruf mit Argumenten belegt (grep 12.11.: 0).
Kevins Antwort woertlich: *'Ja, wie NPC Crew'*.
* **Fest:** `B.T` (shared/BanditsNPCBear.lua) fragt die Existenz eines Schluessels einmal je Sitzung mit `pcall(getTextOrNull, key, "%1", ..., "%9")`;
  eingesetzt wird weiter mit `getText(key, Werte)` (Vanilla-belegt). Gilt NUR fuer diese eine Methode in dieser Form. Eingebaut mit F2 (Staging), nicht
  einzeln in die Test-Mod.

## Baeren-Fenster: E in der Naehe statt V, Fern-Taste selbst setzen (Kevin 12.11.2026 ~04:40)
Woertlich (nach dem ersten F1-Spiel: "neues ui anzeige passt ... das ist top"): *'also folgendes problem das fenster geht auf V auf aber das war
eigtl so gemeint wenn man in der naehe ist wie bei den npc's ich wuerde vorschlagen aber jz weil wenn man mit npc's unterwegs ist die auf v auf gehn
dann ist es schwer das baeren inventar zu oeffnen deswegen schlag ich vor bei E das baeren ui zu oeffnen und wenn man es aus der ferne oeffnen will
dann kann man beim UI den hotkey festelegen um es aus der ferne aufzurufen und em die E taste fuer den baeren wenn man in der naehe ist in sen mod
settings zum aendern eintragen falls jemand nicht E nutzen will sondern einen anderen key'*.
* **Fest (Lauf baer-f1b, `spiel/f1b_workflow.js`):** Nah-Taste Vorgabe **E** (nur neben dem EIGENEN Baeren, Abstand wie NPC Crews V bei NPCs),
  Fern-Taste Vorgabe **keine** -- beide in Optionen > Mods > "NPC Crew: Bear" einstellbar. V gehoert wieder NPC Crew ("Talk to NPC") und Vanilla;
  der Rechtsklick "Bear window" bleibt. Ohne Baer in der Naehe tut E nichts Eigenes (bleibt Vanillas Interact).
* Gewaehlter Weg bei Kleinfragen (Lauf entscheidet mit Beleg, Kevin sieht die Liste danach): E oeffnet nicht im Fahrzeug, beim Tippen im Chat
  oder bei anderem Fenster im Fokus; Vanillas Tier-Radial am eigenen Baeren wieder offen, aber ohne "Kill" (falls belegt moeglich).

## Wachstums-Zeile ueber dem Baeren: Schalter im Fenster, ausgewachsen weg (Kevin 12.11.2026 ~04:50)
Woertlich: *'ich will auch im ui einen schalter haben das die anzeige aus geht wann der waechst und wenn er bei 100% ist soll der knopf ganz
verschwinden aus dem ui weil er dann unnoetig waere wenn das geht ;D'* -- *'also ueber den baeren die anzeige'*.
* **Fest (mit Lauf baer-f1b):** Schalter je Baer im Baeren-Fenster fuer die Zeile "Day 12 - half-grown in 3 day(s)" ueber dem Baeren (gespeichert
  wie der Namensschild-Schalter, nur auf dem eigenen Rechner; die Option in Optionen > Mods bleibt Hauptschalter). Ausgewachsen: Zeile ueber dem
  Baeren UND Schalter im Fenster verschwinden (heute stuende dort dauerhaft "Day N - full-grown").

## "Show damage" und "Melee damage" im Baeren-Fenster (Kevin 12.11.2026 ~05:00)
Woertlich: *'ich will auch noch im ui ein "show damage" button das ueber den kopf der zombies/banditen dann der dmg steht den der dmg austeilt wie
bei der mod show damage die ich auch installiert habe und im ui haett ich gern noch bei COndition ein Meele damage reiter damit man sieht wie viel
schaden er aktuell macht mit seiner aktuellen groesse eventuell auch mit dem skill zsm rechnen?'*
* **Fest (mit F2, Nachtrag `../_arbeit/baer_zaehmen/PLAN_F2.md` Abschnitt 11):** Schalter "Show damage" im Fenster (je Spieler gespeichert, Vorgabe
  an): Schadenszahl schwebt ueber dem Kopf jedes Zombies/Banditen, den der EIGENE Baer trifft, in derselben Einheit wie Kevins Mod CombatText
  (Workshop 2286124931, nur gelesen, nichts kopiert). Zeigt CombatText die Baeren-Treffer schon selbst: Vorgabe aus, Frage an Kevin.
* Zeile "Melee damage" unter Condition: Schaden je Treffer JETZT, aus Groesse UND Kaempfen-Stufe (und Sandbox-Prozent) -- dieselbe Rechnung wie im
  Kampf (`B.MeleeDamage`), Tooltip mit allen freigeschalteten Angriffen; das Junge kaempft nicht ("--").

## Lerntempo der Faehigkeiten langsamer + Sandbox, Kill-Zaehler (Kevin 12.11.2026 ~05:10)
Woertlich: *'und wie haste die level erfahrung berechnet? wie lange es dauert bis der baer lvl 10er skills bekommt , das soll schon etwas dauern
also nicht zu schnell gehen der soll nicht schon alles auf max level haben bevor er ueberhuaot voll ausgewachsen ist am besten mit sandbox
einstellung die das verschnellert und ich brauch noch im baeren ui einen kill counter'* -- dazu sein Befund: *'ich hab schon 24 von 100 punkte ibs
lvl 1 bei endurance dabei bin ich mit dem baeren vllt maximal 5 min rumgelaufen'* (passt zum heutigen Deckel 6 XP/min: 5 min -> hoechstens 30).
* **Fest (mit F2, `../_arbeit/baer_zaehmen/PLAN_F2.md` 11.4/11.5):** Deckel 6 -> 2 XP je Faehigkeit und Minute (Stufe 10 >= ~18 Echtzeit-Stunden
  Dauer-Einsatz); Alters-Deckel Junges 3 / halbstark 6 / kraeftig 8 / ausgewachsen 10; Sandbox "Bear: skill learning speed (%)" 25-1000, Vorgabe 100,
  und "Bear: skills limited by age" an/aus, Vorgabe an. Kill-Zaehler je Baer (Zombies, Banditen) im Fenster.

## Kein Schaden am eigenen Baeren durch Spieler, Turrets, NPCs (Kevin 12.11.2026 ~05:20)
Anlass: Kevin hat seinen halbstarken Baeren aus Versehen getoetet (console.txt f:181960 Note_BearDead, Speer in der Hand). Woertlich: *'und scheinbar
hab ich grad meinen eigenen baeren ausversehn gekillt der darf kein schaden bekommen von mir oder meinen turrets schuessen/raketen und von meinen
npc's nicht'* -- danach *'kann keinen neuen baeren rufen obwohl meiner tot ist'* (Trauer-Sperre; zum Testen `NCBear_CubClean()` loescht sie; die
Meldung zeigte "%1$s" -- Bench-Fehler).
* **Fest (mit F2, `../_arbeit/baer_zaehmen/PLAN_F2.md` 11.6):** gezaehmter Baer fuer die Engine unverwundbar; Leben sinkt NUR durch Zombies/feindliche
  Banditen (`B.BearHurt`); jeder andere Verlust (Spieler -- Empfehlung: alle Spieler --, Auto, Turret, NPC-Crew-Figur, fremde Mod) wird
  zurueckgenommen. Naht Turret <-> Baer in NAEHTE.md; Turret-Sitzung am 12.11. informiert. Bench-Meldung bekommt die Tage-Zahl.

## Kopfnaht am grossen Baeren muss weg (Kevin 12.11.2026 ~05:35)
Bilder (nur lokal): `begleiter/kevin_kopfnaht_1112_a.png` (rote Linie = Bogen hinter Stirn/Ohren) und `_b.png`, Spielkamera von vorn-oben auf seinen
grossen gezaehmten Baeren (2c-Modell). Woertlich: *'guck mal die rote markierung da ist kein sauberer umergang zum kopf das regt mich noch auf da
sieht man richtig so eine spuhr das bis da gerendet wurde und dann der kopf einfach dran gebaut worden ist'* -- *'oder fixxed du das sowieso schon
im worklfow?'* -> nur teilweise: baer-gross hob ein 3-cm-Band an (Farbsprung 18,8 -> 16,5), sein Optik-Pruefer sieht den Rand weiter
(`../_arbeit/baer_gross/pruef_optik.md` Befund 4).
* **Fest:** baer-gross-Gegenpruefer prueft die Kopfnaht ausdruecklich aus Kevins Kamera; danach eigener Modell-Lauf **baer-kopfnaht**
  (`spiel/kopfnaht_workflow.js`, 6 Agenten): Uebergang Kopf -> Stirn/Nacken/Hals/Wangen ohne Rand, Ring, Struktur- oder Farbsprung und ohne Stufe,
  Gesicht unveraendert; geprueft aus Kevins Kamera in 8 Posen; erst zeigen, wenn wirklich weg.
* Nachtrag ~06:25: Kevin zu den Zahlen (Stufe 1 >= 50 min, Stufe 10 >= 18 h reine Aktivitaet, realistisch Tag 100-200): *'okay das klingt gut steht das
  dann auch im ui dasss das level nicht hoeher werden kann wegen dem baeren wachstum?'* -> ja: Hinweis "max for its age" sichtbar an der Faehigkeit,
  Tooltip nennt Stufe und ungefaehren Tag, ab dem es weitergeht (PLAN_F2.md 11.4).
* Nachtrag ~06:30, woertlich: *'oder der balken ist ausgegraut also so dunkler das faend ichn och besser'* -> dann *'zusaetzlich'* -> **Fest:** am Alters-Deckel ist der
  Balken der Faehigkeit ausgegraut (dunkler, Stufe gedimmt) UND daneben steht klein "max for its age"; der Tooltip erklaert Stufe und ungefaehren Tag.

## Fischen: Balance gegen den NPC-Angler (Kevin 12.11.2026 ~06:55)
Vorher die Frage "wer fischt besser, Mensch oder mittelgrosser Baer?" (Antwort: halbstark schlechter, ausgewachsen am flachen Fluss besser). Woertlich:
*'mach einfach sowie du meintest halbstark schlechter als ein npc und ausgewachsen besser als ein npc aber nicht viel besser weil sonst wird der die
ganze base alleine versorgen das waere broken weil der ja keinen koeder/angel braucht ;D also mein vorschlag ich eher angeln 50% so stark wie ein npc
und ausgewachsen fuer die balance genauso stark wie ein npc also wenn beide stufe 0 fischen haben und bei stufe 10 fischen sollen die auch gleich gut
dann sein verstehst du?'*
* **Fest (fuer F5):** Fang-Ertrag des Baeren = Ertrag eines NPC-Anglers von NPC Crew mit GLEICHER Fischen-Stufe x Groessen-Faktor. Faktor **0,5 bei
  halbstark** (Tag ~15), steigt mit dem Wachsen auf **1,0 bei ausgewachsen** (Tag 100), nie darueber. Stufe 0 Baer (ausgewachsen) = NPC Stufe 0,
  Stufe 10 Baer (ausgewachsen) = NPC Stufe 10. Junges fischt nicht.
* Grund (Kevin): der Baer braucht keinen Koeder und keine Angel -- besser als der NPC waere "broken" (versorgt sonst die ganze Basis allein).
* F5 liest die Ertrags-Rechnung des NPC-Anglers in NPC Crew nach (nur lesen: `42/media/lua/.../BanditsNPCFishing.lua`, `BanditsNPCFishNet*.lua`)
  und rechnet mit DERSELBEN Formel x Faktor (keine zweite Wahrheit; fehlt NPC Crew in der Test-Mod: dieselben Zahlen als Kopie mit Fundstelle). Die
  B1d-Platzhalter `fishBase 10 / fishMax 60` werden dadurch ersetzt. Offene F5-Fragen (von selbst/Befehl, Fische bringen, Zusehen) bleiben offen.
* Nachtrag ~07:00, woertlich: *'genau und die fischer funktion vom baeren soll einfach nach wasser gehen nicht extra noch beachten wie tief das
  wasser ist etc, einfach wasser das reicht ;D'* -> **Fest:** jede Wasser-Kachel, an der man in Vanilla angeln kann, reicht; kein Unterschied
  Fluss/See/flach/tief (die Fluss-am-flachen-Wasser-Idee entfaellt).

## Fliehen erst kurz vor dem Tod (Kevin 12.11.2026 ~07:30)
Woertlich: *'merk dir noch auch fuer die uebergabe der getamte waer soll nichtmehr kaempfen und nur noch fliehen wenn er low hp ist sodas er nach 2-3
hits sterben wuerde'* -- Korrektur *'getamter baer*'*.
* **Fest (F2, `../_arbeit/baer_zaehmen/PLAN_F2.md` 11.7):** der gezaehmte Baer kaempft, bis sein Leben nur noch fuer 3 Treffer der aktuellen Gegner
  reicht, dann hoert er auf und flieht. Sandbox "Bear: backs off when this many hits from death" 1-10, Vorgabe 3, 0 = nie. Ersetzt die 20-%-Schwelle.

## Junges liegend/tot: Pfoten stecken ineinander (Kevin 12.11.2026 ~07:40)
Nach dem Vergleichsblatt `../_arbeit/baer_junges_fuss/bilder/KEVIN_junges_liegen.png` (alt | neu | Variante "liegen" 2,2 cm tiefer) woertlich:
*'naja ich denk mal du siehst selbst das es scheisse ist die beine stecken ineinander xD'* -- *'(die fuesse)'*. Zuvor zum Gesamtblatt: *'ja das ist
schonmal besser als vorher'*.
* **Fest (naechster Modell-Lauf am Jungen, nach dem Wochen-Reset):** Clips Dead/Death des Jungen so aendern, dass die Pfoten/Fuesse beim Liegen NICHT
  ineinander oder uebereinander stecken (Beine natuerlich gestaffelt, jede Pfote sichtbar und frei), Koerper liegt auf (Variante liegen_gesenkt
  einrechnen), aus Kevins Kamera UND von der Seite pruefen; dabei auch das Schweben beim Rennen ansehen. Die anderen Clips bleiben byte-gleich.
* Nachtrag ~07:50: der grosse Baer liegt bei Dead/Death ebenso mit uebereinander gestapelten Beinen (Render `../_arbeit/baer_gross/fix1/render/end/p_dead_az50_tex.png`).
  Frage "das Liegen beim grossen Baeren gleich mit?" -> Kevin: *'Ja, beide Baeren'*. **Fest:** die Liegen-Aufgabe gilt fuer Junges UND grossen Baeren.

## Schlaf-Pose nach Fotos, fuer alle Baeren (Kevin 12.11.2026 ~07:50)
Kevin: *'lad dir mal schlafende baer fotos runter und zeig mir die dann welche du nehmen wuerdest zum bauen'* -> 12 freie Fotos auf Wikimedia Commons
(Kategorie "Sleeping bears") nur IM BROWSER angesehen, 5 ausgewaehlt und Kevin gezeigt (*'zeig mir nur die bilder die du nehmen wuerdest'*). Dann
woertlich: *'okay mer kdir das mal so fuer die uebergabe das er darauss eine schlafpose macht fuer unsere baeren geht das dann fuer alle baeren direkt?
also baby und ganz gross?'*
* **Fest:** Die Schlaf-Pose (SCHLAF_PLAN.md: Sphinx, Kopf ~20 Grad seitlich auf der Pranke, Pfoten frei, NICHT die Seitenlage der Tot-Pose) wird nach
  diesen 5 Fotos gebaut, fuer ALLE Baeren: einmal am grossen Baeren (2c-Skelett) entworfen, dann wie beim Sitzen (Umrechner `spiel/baer_sitz_jfuss.py`
  mit IK fuer die kuerzeren Arme) auf das Junge uebertragen -- je ein Clip-Satz im GLB des Jungen und im GLB des grossen Baeren; die Groessen dazwischen
  (0,35 .. 1,35) nutzen denselben Clip.
* **Download noch NICHT erlaubt** (Werkstatt-Regel: Name, Quelle, Groesse und Kevins Ja je Datei). Die naechste Sitzung fragt Kevin mit dieser Liste;
  Ablage dann nur lokal `begleiter/ref_schlafen_<nr>.jpg` (in .gitignore eintragen), nur ansehen, nichts davon in die Mod.
| Nr. | Rolle | Datei (Wikimedia Commons, Beschreibungsseite) | Groesse | Lizenz / Urheber |
|---|---|---|---|---|
| 6 | HAUPTVORLAGE: Bauch, Kopf seitlich auf der Pranke, Pfoten frei, schraeg von oben | https://commons.wikimedia.org/wiki/File:%D0%A1%D1%96%D1%94%D1%81%D1%82%D0%B0.jpg ("Сієста.jpg") | 2048x1536, 0,73 MB | CC BY-SA 4.0, Sirocco74 |
| 3 | ganzer Koerper von der Seite, Kopf auf den Vorderpfoten (Masse) | https://commons.wikimedia.org/wiki/File:OURS_BRUN_0023.JPG | 3008x2000, 2,80 MB | CC BY 2.5, Jm.d (angenommen) |
| 10 | eingerollt, von vorn-oben wie die Spielkamera (Pfoten-Lage) | https://commons.wikimedia.org/wiki/File:Ours_brun_(19612993101).jpg | 3427x2284, 7,04 MB | CC BY 2.0, Sebastien Faillon |
| 4 | Sphinx, Kopf seitlich, Hinterbeine sauber nebeneinander | https://commons.wikimedia.org/wiki/File:Braunbaer_anholter_schweiz.JPG | 2816x2112, 3,13 MB | CC BY-SA 3.0, jpr65 |
| 9 | Schlafgesicht nah, Augen zu | https://commons.wikimedia.org/wiki/File:Orso_bruno_(Ursus_arctos)_-_Brown_bear,_Valbrembo,_Italia,_08.2014_(2).jpg | 4608x3072, 11,12 MB | CC BY-SA 4.0, Chindea Ciprian Emil |
* Nachtrag ~07:55: Kevin schickt ein eigenes Bild (nur lokal `begleiter/kevin_schlafen_vorlage_1112.png`): *'das bild find ich auch noch gut dafuer'* --
  Braunbaer EINGEROLLT auf der Seite, Kopf flach am Boden, Vorderpfote vor dem Bauch, Hintersohle sichtbar, alle Pfoten frei. **Fest:** gilt als
  Vorlage mit Vorrang (Kevins Bild ist der Massstab) fuer eine zweite Schlafhaltung "eingerollt" (Tiefschlaf) neben der Sphinx -- deutlich anders als
  die ausgestreckte Tot-Pose (Beine angezogen, Ruecken rund). Ob beide Haltungen oder nur eine: im F3-Plan vorschlagen, Kevin entscheidet.
* Nachtrag ~08:00, woertlich: *'ja und wenn er schlaeft kommt ja eh ein z Z z ueber den kopf in einer farbe ;D die gut dafuer ist'* -- *'merk dir das
  auch noch'*. Das steigende z Z z ist im SCHLAF_PLAN.md Abschnitt 2 schon geplant (dort noch fast weiss wie die NPC-Crew-Namen). **Fest:** eine Farbe,
  die nach Schlaf aussieht -- Vorschlag sanftes Hellblau (etwa 0,70 / 0,85 / 1,00) mit dunklem Schatten, damit es sich klar vom weissen Namensschild
  abhebt; im F3-Plan als Bild zeigen, Kevin waehlt.
* Kevin (12.11. ~08:15) zum Generator-Baeren (zweites grosses Modell): *"ja mach den eignen model lauf wo du den verbesserst besonders sein gesicht (nase) die ist voll schmall und so"* -> Lauf baer-gen-gross-v2 (7 Agenten).
* Kevin (12.11. ~08:30) auf die Frage, ob man das Modell eines gezaehmten Baeren im Spiel wechseln kann: *"ja fuer spieler als knopf aber was ist der haken den versteh ich nicht"*.
  **Fest:** echte Spieler-Funktion (kein Bench), Knopf "Aussehen" im Baerenfenster; grosser Baer 2c <-> Generator-Baer (braun/Fototon), Junges alt <-> neu.
  Weg: derselbe Koerpertausch wie beim Wachsen (B.BodySwap -- neuer Koerper, Eintrag/Name/Zaehmung/Werte bleiben). Jedes Aussehen = eigene Tierart mit
  ENDGUELTIGEM Namen (steht im Spielstand). Einplanen in der Funktionen-Spur NACH F1b (F1b baut am Baerenfenster).
* Kevin (12.11. ~08:40): *"okay gut dann starte noch einen workflow fuer den anderen baby baeren mach da auch das gesicht besser und vorallem die beine"* -- *"laeuft das
  andere baby anders als das was jz standard ist?"* -> Lauf baer-gen-junges-v2 (8 Agenten) am Generator-Jungen (Foto C): Beine/Gang zuerst, dann Gesicht/Maul; kommt als
  Vergleich per NCBear_CubGen() zurueck (Bench), spaeter waehlbar ueber den Aussehen-Knopf.
* Kevin (12.11. ~10:15) auf die Frage "NPC Crew kann jetzt Deutsch -- soll der Baer auch deutsche Texte bekommen?": *"Ja, auch Deutsch"*.
  **Fest:** der Baer bekommt DE als achte Sprache (wie NPC Crew seit v3.14.75: EN, PTBR, RU, KO, ES, CN, FR, DE; DE nur U+0020-007E und U+00A1-00FF ohne
  U+00A4/U+00AD, typografische Anfuehrungszeichen als " und Gedankenstriche als --, Pruefung NPC Crew `_docs/tools/langcheck.py`). Vorbereitung jetzt am
  F1b-Stand (`../_arbeit/baer_de/`), die F2-Texte kommen nach dem F2-Lauf dazu; dann LANGS im Uebernahme-Skript auf acht und mit F2 einbauen.
* Kevin (12.11. ~10:50) zu den deutschen Begriffen: Ueberschrift **"Faehigkeiten"** (nicht Fertigkeiten), Balken **"Leben"** (nicht Gesundheit), Knopf
  Unstuck = **"Herholen"** (wie NPC Crew DE), mittlere Stufe **"stark"** (Junges -> halbstark -> stark -> ausgewachsen). Die Faehigkeit Vitality heisst "Zaehigkeit"
  (damit sie nicht wie der Balken "Leben" heisst). Eingesetzt in `../_arbeit/baer_de/werkzeug/de_texte.py`, Pruefer 0 Fehler.
* Kevin (12.11. ~13:50) zum Blatt KEVIN_gen_gross_v2.png (Generator-Baer v2): *"variante nase schmaler sieht am besten aus"*. **Fest:** Nase wie die Spalte
  "Variante: Nase schmaler" (= v2/out_vor_fix, ohne den Nasen-Umlauf O2-01). Plan: alle anderen Nachbesserungen behalten (Lippenlinie glatt, Augenring,
  Fototon), nur O2-01 (wrap/unter) aus -> v2/out_schmal/; sieht es von vorn nicht wie seine Wahl aus, out_vor_fix nehmen.
* Kevin (12.11. ~14:00) nach dem Blatt KEVIN_gen_gross_v2.png: *"und bei beiden baeren sieht der mund schonn scheisse aus das muss besser werden  guck dir dazu
  vllt bilder an wie nen baeren maul aussieht wenn er das maul offen hat"* -> Lauf **baer-maul** fuer 2c UND Generator-Baer: erst Forschung + Plan
  (`spiel/maul_plan_workflow.js`), Bau als eigener Lauf, sobald kopfnaht und gen-gross-schmal fertig sind (dieselben Modelle). Vorlage weiter
  kevin_bruellen_vorlage.webp (nur ansehen) + Netzbilder nur ansehen; freie Fotos nur mit Kevins Ja je Datei.
* Kevin (12.11. ~15:00) zu den Maul-Fragen (PLAN_MAUL.md 7): **K2 Mundwinkel weiter nach hinten bis unters Auge: Ja.** **K4 dunkle Lippenlinie auch bei
  geschlossenem Maul: Ja.** **K1 Generator-Baer bekommt das neue Aufrichten/Bruellen: *"erstmal so lassen und angucken"*** (nicht im Maul-Lauf). **K5 Downloads:
  alle drei Ja** -> `begleiter/ref_maul/ref_maul_1.jpg` (Kodiak_brown_bears_FWS_18395.jpg, 1.919.838 B, gemeinfrei Lisa Hupp/USFWS), `ref_maul_2.jpg`
  (Two_bears_fight,_mouths_open_(51101357447).jpg, 12.029.986 B, gemeinfrei Peter Pearsall/USFWS), `ref_maul_3.jpg` (Brown_bear_(Ursus_arctos_arctos)_smiling.jpg,
  9.966.880 B, CC BY-SA Malene Thyssen) -- alle von commons.wikimedia.org, nur ansehen, in .gitignore, nie in Modell/Textur, nie hochladen.
* Kevin (12.11. ~15:15) auf "Was soll der naechste Funktionen-Lauf werden?": *"Aussehen-Knopf"* (vor F3); Start: *"Nach 18:40"* (5-h-Reset). Lauf baer-aussehen
  (8 Agenten, `spiel/aussehen_workflow.js`, Staging `../_arbeit/baer_zaehmen/mod_look/` = Test-Mod 8a22bf9).
* Kevin (12.11., weitergegeben von der NPC-Crew-Sitzung): *"nach dem upload aber unsere turret mod und baeren und modelle mod muss dem auch folgen"* -- Sandbox-Optionen
  in Kategorien (Seiten) wie NPC Crew. Vorschlag fuer die 39 Baeren-Optionen in `NAEHTE.md` "Sandbox-Seiten"; umsetzen, sobald NPC Crew die page-Namen meldet.
* Kevin (12.11. ~17:40) zu den 39 Sandbox-Optionen: *"was wir haben 39 baeren sandbox einstellungen?"* -- *"ja du hast komplett uebertrieben  da muss so einiges
  rausfliegen ;D"* -- zu Claudes 13er-Liste: *"9 ist ja komplett unnoetig klar sollen die zombides und banditen den angriefen ^^"* -> **Fest: 12 bleiben**
  (Junge an/aus, Haeufigkeit, Baeren je Spieler, Koederplatz an/aus, Zaehm-Tempo %, Tage bis ausgewachsen, Lerntempo %, Faehigkeiten nach Alter an/aus,
  kann nicht sterben, Flucht-Schwelle, Schaden des Baeren %, Heil-Tempo %); alle anderen feste Werte (heutige Vorgaben), Zombies/Banditen greifen immer an.
  Umsetzung im Lauf baer-aussehen (CTX "SANDBOX-KUERZUNG"). Nachfrage Kevin: *"was soll denn nummer 12 sein schaden pro % ?"*
  Nach der Erklaerung (Schaden, den der Baer austeilt, 10-300 %, 100 = normal): *"ja okay den rest koennen wir so lassen"* -> die 12er-Liste ist FEST (inkl. Schaden %).
* Kevin (12.11. ~19:30) zum UI-Entwurf (`../_arbeit/baer_zaehmen/ui_entwurf/`, A hoch / B breit): *"B (breit)"* -> **Fest: Baerenfenster Variante B** -- drei Karten
  nebeneinander (Condition | Needs | Skills), Befehle in 5 Spalten (Reihe 1 Befehle, Reihe 2 Handgriffe Fish/Unstuck/Look/Inventory/Bandage, Reihe 3 Schalter).
  Umbau mit F3 (bringt die Needs-Karte); Vorlage `ui_entwurf/proto/`. Der laufende Aussehen-Lauf baut seinen Knopf noch im heutigen Layout.
* Kevin (12.11. ~20:10): *"so keinen neuen workflow mehr starten merk dir den stand schonmal und mach alels fuer die uebergabe an eine nanderen clausde ascocunt
  berreit und wenn die workflows durch sind nochmal alles speichern, stell dir einen waechter ab 95% wochen limit stoppst du alles und machst es berreit fuer die
  uebergabe und mach ein 5h std waechter an falls er beendet wird deswegen"* -> UEBERGABE_ACCOUNT2.md neu, Waechter 3c536c47.

## 13.11.2026 (anderer Account, Sitzung cccbd9d6): Kevins Antworten zu F3, Maul, Modell-Reihenfolge
Kevin: *"so les dir durch wo es weiter geht und dann mach weiter :D"*. Antworten per Auswahl-Dialog, Freitext woertlich:
* **Maul:** Lippenlinie darf 1,3-1,8 cm nach innen ruecken (*"Ja, darf"*) -> Maul-Nachbesserung als Modell-Lauf NACH Liegen/Tot.
* **Modell-Reihenfolge:** zuerst **Liegen/Tot beider Baeren (Pfoten frei)**, dann Maul-Nachbesserung, dann Schlafpose.
* **F3 Frage 1 (Schlafhaltung):** *"Beide"* (Sphinx + eingerollt, 8 Clips).
* **F3 Frage 2 (vom Zombie geweckt):** *"Ersr weg dann kaempfen wie Recommeded nur halt das er nach 5 sec schlaftrunken wieder kaempft aber den rest sowie das steht"*
  -> schlaftrunken wegrennen **5 s** (nicht 20), dann kaempfen wie immer; sehr muede -> rennt weiter weg; Passiv/Junges wie heute.
* **F3 Frage 3 (Muedigkeit beim Folgen):** *"wie recommended nur ich will das er ab 90% sagt das er zu muede ist zum kaempfen und erst bei 100% von selbst einschlaeft"*
  -> Muedigkeit steigt auch beim Folgen; **ab 90 % kaempft er nicht mehr und SAGT es** (Meldung "zu muede zum Kaempfen"); **erst bei 100 % schlaeft er von selbst ein**.
* **F3 Frage 4 (Vertrauen):** *"wie recommended nur mit dem unterschied wenn sein vertrauen zu negativ wird weigert er sich zu kaempfen und das steht dann da auch , ausserdem bei niedrigen vertrauen erhoehen sich seine beduerfnisse im gegenzug"*
  -> Balken + Wort; viel Vertrauen: Hunger/Durst/Muedigkeit bis 20 % langsamer; **wenig Vertrauen: Beduerfnisse steigen schneller** (Gegenstueck); **sehr wenig
  Vertrauen: er weigert sich zu kaempfen, und das steht sichtbar da** (Fenster + Meldung). Andere Befehle gehorcht er weiter. Schwellen/Zahlen im Bau vorschlagen.
* **F3 Frage 5 (z Z z):** *"Hellblau, ueber dem Kopf"* -> Kevins Ja, dass der Code das Spiel fragt, wohin der Baer schaut (Blickrichtung des Tiers; falls nur im Jar
  belegt: das ist Kevins Wort fuer genau diesen Aufruf, Fundstelle/Offset im Kommentar). Buchstabe wechselt weich z -> Z -> z.
* **F3 Frage 6 (a):** *"bei leben und trinken geht sein leben auf 1% runter aber er stirbt nie daran"* -> Hunger/Durst leer: Leben sinkt bis **1 %** (nicht 10), nie Tod.
* **(b):** ein neuer Sandbox-Regler Beduerfnis-Tempo % (0 = aus) -> 13 Regler.
* **(c):** *"schlafen und aufstehen nach seinen mueidgkeitswert wie bei den npc crew's steigt es auf 100% schlaeft er solange bis er auf 0% runter ist ansonsten kann man ihn per folgen wieder aufwecken mitten drinne"*
  -> **KEINE Uhrzeiten** (kein Nachtschlaf 22-7, kein fester Mittagsschlaf des Jungen): Schlaf nur nach Muedigkeit wie die NPC-Crew-Figuren -- bei 100 % schlaeft er,
  bis er bei 0 % ist; mittendrin weckt ihn "Folgen" (bzw. jeder Befehl, siehe e). Lesart Claude: der Mittagsschlaf 13-15 Uhr entfaellt damit (Kevin gesagt, nicht widersprochen = offen bis zum Test).
* **(d):** Ja -- er legt sich neben den Spieler, wenn der schlaeft (das ist die eine Ausnahme vom 100-%-Schlaf).
* **(e):** Kein Schlaf-Knopf; jeder Befehl weckt ihn, Streicheln laesst ihn liegen, Fuettern/Traenken weckt kurz.
* **(f):** Schlafton, Baerenbett, selbst trinken am Wasser: alles spaeter.
* **(g):** Prozent im Balken, Wort im Tooltip.
* **Kevin 13.11. (waehrend des F3-Starts): Herz bei maximalem Vertrauen** (woertlich: *"wenn man bei maximalen vertrauen ist beim baeren soll ein Herz ueber den baeren namen erscheinen das auch abschaltbar wird das herz muessen wir davor noch selbst erstellen damit es huebsch aussieht ;D"*)
  -> **Fest (in F3):** bei maximalem Vertrauen erscheint ein Herz UEBER dem Namensschild des Baeren; je Spieler abschaltbar (Optionen > Mods, wie die Kopf-Balken,
  Vorgabe an). Das Herz ist ein EIGENES, selbst gezeichnetes Bild (nichts kopiert, kein Download), mehrere Entwuerfe auf einem Blatt fuer Kevin, der huebscheste ist eingebaut.
  - Nachtrag gleich danach, woertlich: *"oder das herz wird nur angezeigt wenn die namens anzeige vom baeren an ist eins von beiden"* -> **Gebaut wird diese
    zweite Fassung:** das Herz haengt am Namensschild -- es ist nur zu sehen, wenn die Namensanzeige des Baeren an ist; KEIN eigener Schalter (weniger Optionen).

## 13.11.2026 abends: Kevins Antworten zu F4 (Traglast + eigenes Inventar), per Auswahl-Dialog
Grundlage `../_arbeit/baer_zaehmen/f4/PLAN_F4.md` Abschnitt 23 und FORSCHUNG_F4.md (Weg D: Register-Inventar + Spieler-Kopie als Absturz-Schutz).
* **Frage 1 (was tragen):** woertlich *"alles was es gibt :D und wie hoch wird das slot limit die npc's duerfen nur maixmal 1000 items im inventar tragen z.b"*
  -> **ALLES** (auch Kleidung, Taschen, gekochtes/gefrorenes Essen, Schusswaffen, Schluessel, Zettel/Karten, Elektronik, Klingen).
* **Jar-Ausnahme dafuer:** *"Ja, dieselben wie NPC Crew"* -> der Baer darf JEDE Jar-Methode nutzen, die NPC Crew fuer seine Inventar-Manifeste schon mit
  Kevins Wort nutzt (Liste mit Klasse/Methode/NPC-Crew-Fundstelle im Bau in NAEHTE.md und hier nachtragen). Was selbst NPC Crew nicht verlustfrei kann
  (z. B. Inhalt von Taschen, echte Flicken), wird im Plan genannt und erst nach Kevins Wort gebaut -- bis dahin ehrlich ablehnen statt Werte verlieren.
* **Item-Limit:** *"1000 wie die NPCs"* -> hoechstens 1000 Gegenstaende, zusaetzlich zur Gewichtsgrenze.
* **Frage 2 (oeffnen):** ansehen ueberall (auch Fern-Taste), hineinlegen/herausnehmen nur daneben (3 Kacheln), nicht waehrend er im Auto mitfaehrt.
* **Frage 3 (Tod):** alles faellt an der Stelle auf den Boden (auch die Packtaschen).
* **Frage 4 (Packtaschen):** eigener Gegenstand "Bear Packs"/"Baeren-Packtaschen", selbst naehen (Schneidern 3: Jute oder Stoff, Lederstreifen, Seil,
  Faden; Nadel und Schere bleiben), anlegen ab halbstark, mit F4 nutzbar, Modell/Bild am Ruecken in einem eigenen Modell-Lauf danach.
* **Frage 5 (Sandbox):** neuer Regler "Traglast %" 50-250, Vorgabe 100, Packtaschen immer +50 -> 14 Regler.
* **Frage 6 (selbst fressen):** ja -- ab 50 % Hunger aus dem eigenen Inventar, nur Baerenfutter, nie Verdorbenes, Lieblingsfutter zuerst.
* Ohne Frage (Plan): nicht langsamer bei Last, nur der Besitzer kommt ran, hineinlegen weckt nicht, Absturz-Schutz ueber die Spieler-Kopie.
* **Kevin 13.11. abends (F4 laeuft schon): Packtaschen +150 statt +50** (woertlich: *"okay aber die traglast kann man ja sicher noch leicht erhoehen oder? weil nur +50kg find ich aktuell zu wenig um ehrlich zu sein 😃 ich bin eher so bei +150 das der baer am ende dann bei 250kg ist das waere er doch oder?"*)
  -> **Fest:** Packtaschen geben **+150** (ausgewachsen 100 + 150 = **250 kg** bei Regler 100 %). Der Regler "Traglast %" (50-250) wirkt weiter nur auf die
  Grundlast, nicht auf die Taschen: hoechstens 250 + 150 = 400 kg (unter den 500, die Kevin am 08.11. abgelehnt hat). Halbstark mit Taschen 40 + 150 = 190.
* **Kevin 13.11. ~21:15 zu Liegen/Tot** (woertlich: *"ja okay das ist gut genug dafuer der tot muss nicht so schoen sein haha"*): Liegen/Tot ist **abgenommen, so wie es ist**.
  Die Kleinfragen des Laufs (K1 obere Beine in der Luft, K2 Junges Braun steifer, K3 Plumps-Ton frueh, K5 von hinten verdeckt, K6 Falten, Bein kurz im Bauch beim
  Sturz) werden NICHT weiter verfolgt. Offen bleibt nur die Frage, ob F2 "Am Boden" spaeter die Seitenlage statt Sitzen zeigt (nicht beantwortet).
* **Kevin 13.11. ~21:25: Bauch von unten verbessern** (woertlich: *"aber das baeren model koennen wir jederzeit noch verschoenern ohne das es den posen schadet oder? ^^"* --
  *"weil von unten der bauch von den baer sieht ja noch verbesserungswuerdig aus sag ich mal ;D"*). -> **Auf die Modell-Liste nach der Pause:** Unterseite/Bauch
  des grossen Baeren (beide Aussehen; Junge pruefen) schoener -- Fell/Textur und, wo noetig, Form; danach alle Posen (Sitzen, Aufrichten, Liegen/Tot, spaeter
  Schlafpose) neu rendern und nachmessen (Liegen per `spiel/baer_kern_liegen.py` wiederholbar). Kevins Bild vorher erfragen (was genau stoert).
  Nachtrag, woertlich: *"das hat man bei der todes animation gesehn"* -> gesehen auf dem Blatt `../_arbeit/baer_liegen/bilder/KEVIN_liegen.png`
  (Spalte "nah, Blick 90 Grad (Bauch)" und die TON-Reihe): die Bauchseite des liegenden Baeren ist dort der Massstab.
* **Kevin 13.11. ~21:40: Vertrauen von -100 % bis +100 %, Start bei 0** (woertlich: *"warte mal ich hab gesehn dass das vertrauen vom baeren bei 50% schon ist ist es so eingestellt das unter 50% negativ ist und ueber 0% psotiiv"* -- nach der Erklaerung: *"das ist nicht gut das must du bitte aendern ich will bei 0 starten und dann bis 100% und bis -100%"*).
  -> **Fest (Korrektur an F3):** Vertrauen laeuft von **-100 % bis +100 %**, ein frisch gezaehmter Baer startet bei **0**. 0 = neutral; +100 = Beduerfnisse 20 % langsamer
  und Herz ueber dem Namen; -100 = 20 % schneller; **unter -70 % weigert er sich zu kaempfen** (Kevin: "Unter -70 %", = alte Grenze 15). Anzeige: **normaler Balken mit
  Zahl** (links -100, rechts +100, Zahl daneben, z. B. "-20 %"; Kevin waehlte das, nicht den Mittel-Balken). Alte Spielstaende umrechnen: neu = (alt - 50) x 2.
  Kopf-Balken (TagTrust), Tooltips und Texte in acht Sprachen nachziehen. Einbau NACH F4 (F4-Staging enthaelt dieselben Dateien), als kleiner Lauf.
  Nachtrag, woertlich: *"und bei negativ halt in einer negativen farbe und positiv eine positive = gruen ;D und negativ rot"* -> Balken (Fenster UND Kopf-Balken)
  **gruen bei positivem, rot bei negativem Vertrauen** (bei 0 neutral grau); die Zahl daneben in derselben Farbe.
* **Kevin 13.11. ~21:50, Fehler beim Aufrichten/Bruellen** (Spielbild `kevin_rear_schild_1113.webp`, `NCBear_AnimTest("rear")` am ausgewachsenen Baeren; woertlich: *"hier der erste fehler beim roar geht der text nicht hoeher und versperrt die sicht"*):
  das Namensschild ("Baer von Dee", "folgt", Balken) bleibt beim Aufrichten auf der Steh-Hoehe und liegt dann mitten ueber Kopf/Brust. **Fix (im Korrektur-Lauf nach
  F4, zusammen mit dem Vertrauen):** Schild (samt Herz, z Z z, Kopf-Balken) folgt der Pose -- beim Aufrichten weich mit dem Kopf nach oben und wieder herunter
  (Zeitkurve des Clips bzw. was belegt ist), so dass es nie Kopf oder Gesicht verdeckt; gilt fuer alle Aussehen und Groessen (auch Generator-Baer mit altem Clip).
  Dabei alle hohen/tiefen Posen mitpruefen (Aufrichten, Doppelschlag, Sitzen, Liegen/Tot, spaeter Schlafen). Pruefbild aus dem echten Code ueber Kevins Spielbild.
  - **Nachtrag ~21:55, Spielbild beim Aufrichten von vorn** `kevin_rear_bauch_1113.webp` (woertlich: *"hier siehst du seinen bauch von unten sieht der noch komisch aus"*).
    Claude sieht darin (vergroessert): Bauch und Brust als flache, hellere Platte zwischen den Vorderbeinen (wie ein Brett/Latz, kaum Fell, keine Rundung), unten
    eine waagerechte Kante wie eine Hosennaht, Innenseite der Hinterbeine als Bogen ("Hose"); Rumpf von vorn ein langes Rechteck ohne Bauchwoelbung;
    Vorderbeine haengen wie Aermel seitlich an der Platte; helle Flecken an den Hinterfuessen. **Massstab fuer den Bauch-Lauf** (neben KEVIN_liegen.png Spalte
    Bauch): runder Bauch mit Fell und Struktur, kein Latz, keine Naht, Uebergang Brust-Bauch-Innenschenkel fliessend -- aus Kevins Kamera beim Aufrichten,
    Sitzen und Liegen pruefen.
  - Nachtrag ~22:00 zum Schild-Fehler, woertlich: *"der hp balken geht auch nicht hoeher dabei der stoert also auch"* (im Bild `kevin_rear_bauch_1113.webp` liegt der
    rote Lebensbalken genau unter dem offenen Maul) -> der Fix gilt ausdruecklich fuer ALLES ueber dem Baeren: Name, Zustandszeile, Lebens-/Ausdauer-Balken,
    Beduerfnis-Balken, Herz, z Z z -- alles hebt sich beim Aufrichten mit dem Kopf und verdeckt nie Kopf oder Maul.
* **Kevin 13.11. ~22:05: Lebensbalken per Knopf ausblenden** (woertlich: *"und ich wuerde den hp balken auch gern ausblenden lassen durch einen botton"*). Heute geht das nur
  unter Optionen > Mods > "NPC Crew: Bear" > Health over the bear (Aus / Balken / Zahl, Vorgabe Balken; `client/BanditsNPCBearOptions.lua:99-102`).
  -> **Im Korrektur-Lauf nach F4:** im Baerenfenster in der Schalter-Reihe (neben Namensschild / Schaden zeigen / Wachstumszeile) ein Schalter **"Lebensbalken"**,
  der denselben Wert umschaltet (an = wie in den Optionen gewaehlt, aus = Aus), je Spieler gespeichert wie die anderen Schalter; Texte acht Sprachen.
* **Kevin 13.11. ~22:10, deutsche Uebersetzung "Verbinden" irrefuehrend** (woertlich: *"ausserdem ist die deutsche uebersetzung "Verbinden" ireefuehren das hat mehrere bedeutungen und ist nicht eindeuig wie "Heilen""*).
  -> **Im Korrektur-Lauf nach F4:** DE `UI_BN_Bear_Win_Bandage` "Verbinden" -> **"Heilen"**; Rechtsklick `UI_BN_Bear_Menu_Bandage` "Junges verbinden" -> **"Junges heilen"**,
  `UI_BN_Bear_Menu_BandageBig` "Baeren verbinden" -> **"Baeren heilen"** (Translate/DE/UI.json:87-88, :289). Tooltip/Meldungen, die "verbinden" sagen, ebenso; dass dabei
  ein Verband verbraucht wird, sagt der Tooltip. Andere Sprachen unveraendert (nur DE betroffen). Gilt ab jetzt auch fuer neue DE-Texte: "heilen" statt "verbinden".
* **Kevin 13.11. ~22:20: `NCBear_CubLook("gen")` sagt immer "dein Baer ist beschaeftigt"** (woertlich: *"geht nicht NCBear_CubLook("gen") da steht immer dein baer ist beschaeftigt"*).
  Ursache laut console.txt (f:90955 NCBear_CubGrow(55) -> "body big (swapped)", Look-Bitten f:95000-98322 = rund 28-51 s spaeter bei ~144 Bildern/s) und Code: nach JEDEM
  Koerper-Tausch (auch dem Wachsen) sperrt `B.BodySwapReady` 60 s Echtzeit (`server/BanditsNPCBearGrow.lua:594`, swapMinMs 60000, Grund "cool" -> Meldung LookBusy);
  der Testbefehl setzt nur die gemeinsame Uhr Unstuck/Look zurueck, nicht diese Minute. -> **Im Korrektur-Lauf nach F4:** Meldung nennt den Grund und die Restzeit
  ("gerade erst gewachsen/gewechselt -- noch 40 s"), und `NCBear_CubLook` (Testhilfe) setzt auch diese Minute zurueck.
* **Claude 13.11. ~22:25 (beim Zusammenstellen der Posen fuer Kevin gefunden):** `NCBear_AnimTest()` listet seit F3 auch die acht Schlaf-Schluessel (liedown, sleep,
  wakeup, wakealarm, curlin, sleepcurl, curlout, wakecurl; `shared/BanditsNPCBearFightRules.lua:77-84`), deren Clips/Knoten erst F3b bringt -- abgespielt wuerde der
  Baer stehend erstarren. -> **Im Korrektur-Lauf nach F4:** AnimTest zeigt und spielt diese Schluessel nur, wenn `B.CFG.sleepClips == true`; Kevin vorher gewarnt.
* **Kevin 13.11. ~22:35: Generator-Baer bekommt das neue Bruellen** (woertlich: *"ja uebertrag die version auf den"*; Vergleichsbild `kevin_rear_gen_1113.webp` mit
  `kevin_rear_bauch_1113.webp`). -> Kleiner Modell-Lauf: Clip NCBear_Rear aus dem 2c-GLB in NCBearGen.glb uebernehmen (gleiches Skelett; Weg wie beim Liegen per Clip-Tausch),
  nur Rear aendern, Hals/Brust beim Aufrichten am Generator-Netz pruefen (beim 2c brauchte es die Kopfnaht-Reparatur), Bilder aus Kevins Kamera von vorn.
  Reihenfolge: nach F4 und dem Korrektur-Lauf, vor dem Maul (beruehrt dieselbe Datei NCBearGen.glb).
* **Kevin 13.11. ~22:35, Augen** (woertlich: *"was haelst du von deren augen kann man die noch verbessern oder egal weil eh zu klein zum erkennen?"*). Claudes Einschaetzung
  aus Kevins Spielbildern (4K, vergroessert): Klassisch -- kleine dunkle Augen auf hellem Gesichtsfell, als Augen lesbar; Generator-Baer -- dunkle Augen im dunklen Fell
  verschwinden fast (dazu verdeckt heute das Schild das Gesicht). Vorschlag: kein eigener Lauf; im naechsten Modell-Lauf am Generator-Baeren nur Textur: etwas helleres
  Fell als Ring ums Auge und ein winziger Glanzpunkt (aendert keine Pose); erst nach dem Schild-Fix beurteilen.
  **Kevin, woertlich: *"ne lass die augen so"* -> Augen bleiben bei allen Baeren, wie sie sind (kein Textur-Eingriff).**
* **Kevin 13.11. ~22:45, Bauch-Lauf eingegrenzt** (woertlich: *"beim bauch vom std baeren will ich nur das das fell besser aussieht beim ROAR der rest soll so bleiben okay die textur da sieht nur matschig aus nicht wie richtiges fell beim bauch da"*).
  -> **Fest: NUR TEXTUR** am Klassisch-Baeren (2c, `textures/Body/NCBear.png`): Bauch/Brust/Innenschenkel bekommen echte Fellstruktur statt Matsch (Straehnen, Richtung,
  Tiefe), gesehen beim Aufrichten von vorn (`kevin_rear_bauch_1113.webp`). **Form, Netz, Gewichte, Clips bleiben unveraendert** -- also kein Posen-Risiko; Kopf/Gesicht und
  Augen unveraendert. Die frueheren Punkte "Latz/Platte, Naht, Rechteck" sind damit KEIN Auftrag mehr (Kevin: "der rest soll so bleiben").
* **Kevin 13.11. ~22:55: Prankenhieb (swipeL/swipeR) besser** (woertlich: *"und kannst du noch besser NCBear_AnimTest("swipeR") und swipeL animationen bauen? die sieht nicht so geil aus das geht besser ;D"* --
  *"der muss mehr schwung holen und die pfote drehn der tut die pfote komplett in den winkel lassen wie wenn er laufen wuerde das wirkt sehr unnatuerlich"*).
  -> **Auf die Modell-Liste (Clip-Lauf, alle Koerper):** (1) **mehr Schwung holen** -- deutliches Ausholen (Arm weit zurueck/hoch, Schulter und Rumpf drehen mit), dann schneller
  Schlag mit Wucht und Durchzug; (2) **die Pfote dreht beim Schlag** -- Handflaeche/Krallen zum Ziel (Pranke dreht sich auf, Krallen voraus), NICHT die Lauf-Haltung der Pfote
  (heute bleibt die Pfote im Winkel wie beim Gehen). Massstab: echte Baeren-Prankenhiebe (Referenz nur ansehen), Bilder aus Kevins Kamera von vorn und von der Seite,
  Einzelbilder des Schlags. Trefferzeitpunkt (hitPc 0,40) und Dauer 1,5 s nur aendern, wenn noetig -- dann B.CLIPS und Knoten-XML nachziehen. Gilt fuer Klassisch,
  Generator-Baer und die Jungen (gleicher Clip-Weg wie Liegen/Tot), alle anderen Clips bit-gleich.
  Nachtrag, woertlich: *"normalerweise wuerde man die pfote90grad drehn und dann baeaeaem"* -> beim Ausholen dreht die Pranke um **etwa 90 Grad** (Handflaeche/Krallen
  vom Gehen-Winkel zum Ziel gedreht), DANN der schnelle, harte Schlag.
* **Kevin 13.11. ~23:00, Kampf-Fehler aus seinem Test (Stand F3, Kampf aus F2)**, woertlich:
  1. *"der baer macht nicht den roar wenn ein zombie kommt wieso? der sollte das doch machen bevor er in den kampf stuermt das erste mal"* -- heute: Aufrichten nur als erster
     Angriff, 50 % Zufall, Ziel weiter als 2,5 Kacheln, hoechstens alle 120 s, nur ausgewachsen (`shared/BanditsNPCBearFightRules.lua:215`, `server/BanditsNPCBearFight.lua:274`,
     `shared/BanditsNPCBear.lua:214`). Claudes Vorschlag: IMMER beim ersten Kontakt eines Kampfes (rearChance 100), 120-s-Pause bleibt, steht ein Zombie schon direkt
     dran (< 2,5) greift er sofort an. Kevin, woertlich: *"okay verstanden den punkt mit dem bruellen der macht sinn abeeeeeeeeer der kampf code muss noch verbessert werden"*
     -> Bruellen so bauen (immer beim ersten Kontakt, Pause 120 s, ganz nah sofort Angriff); **der Kampf-Code wird insgesamt verbessert** (eigener Kampf-Lauf).
  2. *"und er hat eben einen zombie der am boden lag nichtmehr angegrifen und gewartet bis er aufgestanden ist"* -- Verdacht (statisch, ungeprueft): die Wahl nimmt nur
     `isProne()` (Fight.lua:631); ein umgeworfener Zombie ist im Fall/Liegen evtl. nicht "prone" -> Biss statt Zerfleischen, oder die Treffer-/Sicht-Pruefung (CanSee,
     "kein Luftschlag" F2 B3) lehnt Liegende ab, bzw. der Liegende ist nach dem Wegfliegen ausserhalb maulReach (1,1 x Groesse). Im Lauf klaeren und beheben: liegende
     Ziele werden zerfleischt (maul), auch nach dem Wegfliegen hinlaufen.
  3. *"ausserdem hat er probleme zombies abzuraeumen die sich bewegen dann rennt er langsam hinterher eher ein folgen und kommt nie zum zug"* -- Verdacht: Anlauf mit
     B.MoveTo/fleeTo alle 750 ms neu auf die JETZIGE Lage minus Ankunftsabstand (Fight.lua:672-676); jeder neue Weg startet die Wegsuche neu (Ruckeln), und waehrend
     des Ausholens (Hieb 1,5 s, Treffer bei 0,6 s) laeuft das Ziel aus der Weite. Im Lauf klaeren und beheben: Vorhalt (wohin der Zombie laeuft), volles Tempo, angreifen,
     sobald in Weite, kurzer Ausfallschritt im Schlag.
  -> Alle drei in den Korrektur-Lauf (nach der Pause), mit Kampf-Log: Kevin testet mit `NCBear_FightLog(true)`, damit die Entscheidungen in console.txt stehen.
  4. Nachtrag, woertlich: *"ausserdem sind braunbaeren schneller also die sollten zombies locker einholen und weg klatschen"* -> **Fest fuer den Kampf-Lauf:** im Kampf ist der
     Baer klar schneller als jeder Zombie (auch Sprinter) und holt ihn locker ein. Heute: Tempo kommt aus dem Renn-Clip (tier_spez.md 2.8; Stellwert runSpeedBig 3,17
     Kacheln/s ist nur die Schaetzung fuer die Wegzeit, `shared/BanditsNPCBear.lua:168`). Im Lauf messen (echtes Tempo im Spiel vs. Zombie-Tempo je Sandbox-Art) und,
     falls zu langsam, nur fuer unsere Baeren schneller machen (belegter Weg: z. B. schnellerer Renn-Clip im GLB oder Tempo-Faktor im eigenen Knoten; nie Vanillas Reh/Hirsch aendern).
     Nachtrag, woertlich: *"der soll jz aber auch nicht permanent rumrennen wie ein geisteskranker das soll schon realtisch wirken ^^"* -> schnell NUR im Angriff (kurzer,
     kraftvoller Sprint zum Ziel), sonst ruhig: Folgen, Bleiben, Frei im normalen Gang, nach dem Kampf ruhig zurueck; kein dauerndes Hin- und Herrennen zwischen Zielen
     (kurze Pausen/Verschnaufen wie heute die Ausdauer, kein Zappeln). Realistisch vor schnell.
  5. **Zombies ignorieren den Baeren** (woertlich: *"zombies ignorieren den scheinbar noch stimms?"* -- nach Claudes Erklaerung "naechster gewinnt, du standest daneben":
     *"das kan nich nciht bestaetigen die sind sehr fixiert auf mich und beissen ihn nur wenn ich genau so laufe das der weg zu mir am baeren vorbei fuehrt ansosnten wird der total ignoriert"*).
     Kevin hat recht (sein Spielbild schlaegt den Code-Plan): gebaut ist ein Lenken (`shared/BanditsNPCBearFoe.lua` lureBody :553-588, Zombies im Umkreis lureR 10, nur wenn der
     Baer naeher ist als jeder Spieler, steerZombie), aber offenbar gewinnt die Engine-Jagd auf den Spieler. -> **Hauptpunkt im Kampf-Lauf:** Zombies, die den Baeren
     sehen bzw. ihm nahe kommen, greifen IHN an (er ist Gefahr und Hindernis), nicht nur, wenn er zufaellig im Weg steht; mit Beleg, wie Bandits Zombies auf seine
     Banditen lenkt (nur lesen, nichts kopieren), Kampf-Log in console.txt als Nachweis. Claudes Vorschlag zusaetzlich: wer bis ~2 Kacheln an den Baeren kommt, greift ihn an.
  6. **Kampf-Log 13.11. ~22:33** (Kevin hat `NCBear_FightLog(true)` eingeschaltet; console.txt ab f:349486): 2 Kaempfe, 4 Zombies getoetet (kZ 16-19), dazwischen
     `[TC-BEAR] guard: b2 hides behind its owner from a zombie at 6` -- der AUSGEWACHSENE Baer versteckt sich hinter dem Besitzer (Verhalten des Jungen aus B1c) statt anzugreifen:
     Verdacht Fehler (`server/BanditsNPCBearGuard.lua`), im Kampf-Lauf pruefen. Ausserdem `calm: b2 noise answered (run, walk)`. Das Log sagt NICHT, warum er einen liegenden
     Zombie auslaesst oder was die Zombies tun -> im Kampf-Lauf genauere Diagnose-Zeilen (Grund je "kein Angriff": liegt/ausser Weite/keine Sicht/gesperrt; Lenk-Zustand
     je Zombie) hinter demselben Schalter.
  7. **Reichweiten** (Kevin zu den Werten "kommt mir was sparsam vor"; Auswahl-Dialog, woertlich): Erkennen *"10 reichen aber er ist bei mir grad nie hingelaufen eher bei wenigern ^^"*
     -> fightRadius bleibt **10 Kacheln**, ABER er reagiert im Spiel erst deutlich naeher -> im Kampf-Lauf messen und beheben, warum er bei 10 nicht losgeht (Sicht/CanSee,
     Leine, guard-Fehler aus Punkt 6, Suchtakt); Leine: **25 Kacheln** (fightLeash 14 -> 25; *"25 Kacheln"*).
     Nachtrag Leine, woertlich: *"er soll dann wenn ich 25 kacheln weg bin in fullspeed zu mir sprinten ;D"* -> bricht er den Kampf wegen der Leine ab (Besitzer > 25 Kacheln),
     SPRINTET er mit vollem Tempo zum Besitzer (nicht gehen/traben), bis er wieder in normaler Folge-Naehe ist; dann wieder ruhiger Gang (Kevin 23:05 "realistisch").
  8. **Sprung-Hieb / "Retter-Move"** (Kevin 13.11. ~23:15, woertlich: *"ja sowas waere auch meine idee gewesen das er das machen darf ab und zu also wenn notwendig wenn sich das ziel von ihn entfernt statt zu ihn zu kommen z.b aber ich denke wenn du es schaffst das die zombeis den baeren soweiso angreifen dann gibs so ein problem viel letzdener ausser vllt der spieler selbst wird verfolgt und der baer kommt zur hilfe , in jeden fall waere so ein angriff cool so als retter move :D"*).
     -> **Fest, neuer Angriff (Modell + Kampf):** ein Sprung-Hieb aus dem Lauf (Anlauf, Sprung 1-2 Kacheln nach vorn, Pranke trifft im Flug/Aufkommen, Umwerfen), nur
     **wenn noetig**: das Ziel entfernt sich bzw. laeuft vor ihm her (vor allem ein Zombie, der den BESITZER verfolgt -> "Retter-Move"), nicht als Standard-Angriff;
     Abklingzeit. Weg: eigener Clip mit Vorwaerts-Bewegung im Clip (Tiere bewegen sich laut Forschung baer-laerm ueber die Bewegung im Clip, `getDeferredMovement` --
     im Lauf erst belegen, dass ein Clip mit Wurzel-Bewegung den Baeren wirklich traegt). Reihenfolge: nach dem Kampf-Lauf (der zuerst Zombies auf den Baeren lenkt).

### 13.11.2026 ~23:45 -- F4 im Spiel: Inventar (Kevins Test nach dem Rezept-Fix)
Woertlich (Bild Baer-Inventar, Fusszeile "bis zu 50 auf einmal"): *"guck mal nur 50 items aufienmal verschieben unsere npc crew mod kann da mehr das bitte noch genauso anpassen wie essen/trinken anzeige ist die genauso wie bei npc crew?"*
-> **Fest fuer den Korrektur-Lauf:** "Alle" verschiebt den GANZEN Stapel wie NPC Crew (NC `client/ISUI/BanditsNPCInventoryWindow.lua:153-164` moveStack: ganze Zeile, haelt beim
   ersten Stueck an, das nicht passt, und sagt es). Grenzen nur noch Traglast und 1000 Stueck, kein 50er-Deckel je Klick. Heute: Nehmen nimmt schon den ganzen Stapel
   (Aktionen zu je invTakeMax 50, T `client/BanditsNPCBearInvClient.lua:460-480`), Geben ist bei 50 gedeckelt (U.InvGiveWhy) und stellt je Stueck EINE Zeitaktion an
   (40 + 8 x kg Ticks, `:436-458`) -> grosse Stapel dauern. Lauf prueft, ob Geben wie Nehmen buendelweise geht -- verlustfrei (rote Linie). Fusszeile ohne "(bis zu 50)", 8 Sprachen.
-> **Frage offen (Claude 23:45 gestellt):** Anzeige der Zeilen wie NPC Crew? NPC Crew zeigt den Vanilla-Namen MIT Zustand in der Zeile ("Frisch, ...", "Verdorben, ...";
   NC `client/ISUI/BanditsNPCItemList.lua:212` item:getName), "x5", Gewicht rechts. Baer heute: Name OHNE Zustand, "x5", kg rechts; frisch/alt/verdorben, gekocht,
   Fuellung, "frisst er selbst" nur im Tooltip (T `client/ISUI/BanditsNPCBearInvWindow.lua:270-290`, `:318-327`), Verdorbenes in Warnfarbe.
Dazu Kevins Frage zum Vertrauen (Bild: 44 % nach dem ersten Tag): erklaert -- Tag mit Hunger UND Durst ueber 50 = -3 -3 (B.TrustDayClose); keine Aenderung verlangt.
Kevin ~23:50, woertlich: *"nur die 1000 items einstellen zum gleichzeitig verschieben"* -> **Anzeige bleibt wie sie ist** (Zustand im Tooltip). **Korrektur-Lauf:** "Alle"
   verschiebt bis zu 1000 Stueck auf einmal (Geben: `GIVE_MAX 50` in T `client/BanditsNPCBearInvClient.lua:41`; Nehmen/Server: `invTakeMax 50` in
   T `shared/BanditsNPCBear.lua:301`, Server `server/BanditsNPCBearInv.lua:648`, `:697`) -> beide 1000 (= invMaxItems); Grenzen nur Traglast und 1000; Fusszeile ohne "(bis zu 50)".
Kevin ~23:50, woertlich: *"aber vertrauen muessen wir rebalancen das geht viel zu schnell hoch und runter"* -> **Korrektur-Lauf: Vertrauen deutlich langsamer hoch UND runter**
   (heute bestenfalls +17 je Tag auf 0..100, schlechter Tag -6, ausgehungert -16, am Boden -5). Zahlen: Kevins Antwort folgt (Fragen 23:50: Tage bis +100, Kosten eines schlechten Tags).
Kevin ~23:55 statt der Auswahl, woertlich: *"ganz anders erst ab 90% trinken/durst soll er vertrauen verlieren wie heute die regel, aber gewinnen soll er immer nur beim streicheln und wenn das essen und trinken 100 erreicht bei den aktionen um 0,5 aber immer nur 1x pro tag darf das passieren genauso wie der verlust  des vertrauens, sag mir wie du das verstanden hast und wie lange man dann braucht im optimal fall auf 100 vertraune zu kommen"*
   Claudes Verstaendnis (an Kevin zur Bestaetigung): Gewinn NUR noch je Spieltag hoechstens einmal je Quelle +0,5: Streicheln; satt gefuettert (Hunger durch Fuettern auf 0 %);
   satt getraenkt (Durst durch Traenken auf 0 %) -> bestenfalls +1,5 am Tag -> 0 bis +100 in ~67 Spieltagen. Weg: Hand-Punkte je Futter, Wechsel-Bonus, "gut versorgt" +3, Schlaf +2.
   Verlust NUR noch, wenn Hunger oder Durst an dem Tag 90 % erreicht, hoechstens einmal am Tag (Betrag offen: Vorschlag -0,5); "am Boden -5" faellt weg (offen).
Kevin ~00:00, woertlich: *"ja ausser das trinken/essen bei 90% direkt - 5 machen und wenn der baer down (todesschutz) geht verliert er -10 und ab 1% hp (durch hunger/durst) auch -10 vertrauen wenn das geht ;D  muesste aber weil er bei downed ja mehr als 1% hp hat und unter 1% waere er ja sowieso tot ^^"*
-> **ENDGUELTIGE VERTRAUENS-REGEL fuer den Korrektur-Lauf** (Skala -100..+100, Start 0, wie 21:40 entschieden):
   GEWINN nur so, je Quelle hoechstens 1x je Spieltag, je +0,5: Streicheln / satt gefuettert (Hunger durch Fuettern auf 0 %) / satt getraenkt (Durst durch Traenken auf 0 %).
     Bestenfalls +1,5 am Tag -> 0 bis +100 in ~67 Spieltagen. Alles andere entfaellt (Punkte je Futter, Wechsel-Bonus, gut versorgt +3, Schlaf +2, Tages-Hand-Deckel).
   VERLUST: Hunger erreicht 90 % -> SOFORT -5; Durst erreicht 90 % -> SOFORT -5 (je Wert hoechstens 1x je Spieltag). Kein Tagesabschluss-Verlust mehr (50/80-Stufen weg).
     Am Boden (Todesschutz) -> -10 (heute trDown -5, T `server/BanditsNPCBearHurt.lua:154-155`), jedes Mal.
     Leben faellt durch Hunger/Durst auf 1 % (needHpFloor, T `server/BanditsNPCBearNeeds.lua:479-494`) -> -10, hoechstens 1x je Spieltag.
     Kevins Begruendung stimmt mit dem Code: der Hunger-Abzug stoppt bei 1 % und laeuft nie, solange er am Boden ist (rec.down == nil, :485); am Boden kommt nur aus Treffern.
   Bleibt: Bedarf bis 20 % langsamer/schneller je Vertrauen, Kampf-Verweigerung unter -70, Herz bei +100, Balken gruen/rot mit Zahl.
Kevin ~00:10 (Bild: .357 Magnum Patrone (94), Knoepfe Geben / Alle), woertlich: *"das musst du auch noch fixxen ich kann nur einen schuss geben oder alles ich will bei geben eine auswahl bkeommen wo ich eine zahl eintippe"*
-> **Korrektur-Lauf:** "Geben" oeffnet bei einem Stapel (mehr als 1 Stueck) ein kleines Zahlenfeld (wie viele?), vorbelegt mit dem ganzen Stapel bzw. dem, was noch passt
   (Traglast, 1000); OK/Abbrechen; bei 1 Stueck sofort geben wie heute. "Alle" bleibt. Beleg Vanilla-Zahlenfeld: `ISTextBox:new(0, 0, 280, 180, text, wert, nil, onClick, playerNum, ...)`
   V:`client/ISUI/Animal/ISAnimalContextMenu.lua:791` (Wolle-Menge), `setOnlyNumbers(true)` V:`client/Entity/ISUI/BuildRecipe/ISWidgetBuildControl.lua`. Ob auch "Nehmen" ein Zahlenfeld bekommt: an Kevin gefragt.
Kevin ~00:15 (Auswahl): *"Ja, auch Nehmen"* -> auch "Nehmen" oeffnet bei einem Stapel das Zahlenfeld (vorbelegt: ganzer Satz bzw. was in deine Tasche passt); 1 Stueck sofort wie heute; "Alle" bleibt.
Kevin ~00:20 (Bild Fenster: Nahkampfschaden "70 je Treffer", Durst 100 %, Tooltip "Von Hunger oder Durst geschwaecht: 70%"), woertlich: *"die damage zahl soll rot werden und echte wert angezeigt werden wenn er durch hunger/muedigkeit etc wenigert dmg verursacht"*
-> **Korrektur-Lauf:** Wert "Nahkampfschaden" (und die Zeilen Prankenhieb/Biss/Zerfleischen im Tooltip) in ROT, solange ein Schwaeche-Faktor wirkt (Sicht mdmgK < 1,
   T `client/BanditsNPCBearWinData.lua:901-903`). Der Wert ist schon heute der echte (mdmg enthaelt den Faktor: normal 100, hungrig 85, Durst 100 % -> 70).
   Muedigkeit senkt den Schaden heute NICHT (B.NeedK: ab 70 nur Ausdauer-Erholung halb, ab 90 kein Kampf) -- an Kevin gefragt, ob sie es soll.
   Nachtrag Kevin ~00:22, woertlich: *"mit info dann im screen"* -> der Tooltip sagt beim roten Wert genau, WARUM und wie viel: normaler Schaden, jetziger Schaden,
   Grund mit Stand (z. B. "Durst 100 %: 70 % des normalen Schadens (normal 100, jetzt 70)"); Prankenhieb/Biss/Zerfleischen je mit normal -> jetzt.
   Kevin ~00:25 (Auswahl "Soll Muedigkeit auch den Schaden senken?"): *"Nein, so lassen"* -> Schaden sinkt nur durch Hunger/Durst wie heute.
Kevin ~00:30 (Frage "ab wie viel % essen/trinken ... aus dem inventar?"; Auswahl "Soll er auch Wasser aus seinem Inventar selbst trinken?"): *"Ja, ab 50 % Durst"*
-> **Korrektur-Lauf:** Selbst trinken aus dem eigenen Inventar wie das Fressen (T `server/BanditsNPCBearInv.lua` ~985-1010: ab needHungry 50 bis unter needPeckish 25,
   hoechstens je invEatGapMin 10 Spielminuten): ab Durst 50 % trinkt er aus Behaeltern mit Wasser. BERICHTIGT 00:45: das Inventar nimmt JEDEN Fluessigkeits-Behaelter mit genau EINEM Stoff an
   (Satz-Felder q/ft, T `shared/BanditsNPCBearInvRules.lua:370-405`: Flasche, Feldflasche, Topf, 10-l-Eimer, Kanister -- auch Benzin, Bleiche, Alkohol). Trinken daher NUR
   aus ft Water / TaintedWater (Namen im Lauf an Vanilla belegen), nie aus anderen Stoffen;
   eine Schale (bowlL 0,5 l) je Schluck, bis Durst unter 25 %; die Flasche bleibt (leer) im Inventar -- nichts verloren, nichts doppelt. Wie beim Traenken aus der Hand (B.DrinkNeedL).
   Vorschlag: sauberes Wasser zuerst, dann ungekochtes (Baeren trinken aus Fluessen). Zaehlt NICHT als "satt getraenkt" fuer das Vertrauen (das gibt es nur beim Traenken aus der Hand).
Kevin ~00:35, woertlich: *"kann der baer auch spaeter auf kisten zugreifen und essen holen und trinken?"* -> gleich danach: *"okay nur wie die tiere das macht mehr sinn haha"*
-> **Spaeter (B-Liste, nicht im Korrektur-Lauf):** der Baer frisst und trinkt selbst WIE VANILLAS NUTZTIERE -- aus Futtertroegen und Wassertroegen (B42-Tiere gehen selbst
   hin), in der Wildnis aus Fluss/See; NICHT aus Kisten. Erst Forschung: wie Vanilla-Tiere Troege finden und nutzen (IsoAnimal, Trog-Objekte; Belege Vanilla-Lua/Jar),
   ob das am Baeren (AnimSet buck, eigene Beduerfnisse statt Vanilla-Werte) mitlaeuft oder nachgebaut werden muss; MP und "nichts verloren/doppelt" am Trog. Passt zu F5 (Fischen/Nase).
Kevin ~00:50, woertlich: *"ich will das er isst + trinkt bis er 0% erreicht also garnichtmehr hunrig oder drustig ist und ab 50% wieder isst/trinkt"*
-> **Korrektur-Lauf:** Selbst fressen UND selbst trinken aus dem Inventar: Start ab 50 %, weiter bis 0 % (heute Fressen bis unter needPeckish 25 -> neu bis 0;
   eigener Wert z. B. invEatStop = 0). Trinken nimmt beim letzten Schluck nur, was bis 0 fehlt (B.DrinkNeedL), der Rest bleibt im Behaelter. Beim Fressen beim letzten
   Stueck das kleinste passende waehlen, damit wenig verfaellt (was unter 0 ginge, verfaellt heute -- B.Feed). Bei Saft/Milch/Limo nicht geantwortet -> nur Wasser.
Kevin ~00:55, woertlich: *"ja der darf natuerlich auch dreckiges wasser trinken weils ein tier ist"* -> bestaetigt: sauberes UND ungekochtes (TaintedWater) Wasser, ohne Krankheit; sauberes zuerst.
Kevin ~01:00, woertlich: *"und ich will noch das hunger system aendern und das trinken 😃 das soll realistisch sein nach groesseeee"*
-> **Neuer Punkt (vor dem Bau erst Zahlen):** Hunger und Durst realistisch nach Groesse. Heute (T `shared/BanditsNPCBear.lua:258-260`): Prozent steigen fuer ALLE Groessen
   gleich (Hunger +50, Durst +75 je Spieltag); nur die Menge waechst: Junges 1 Mahlzeit / 1 Schale, halbstark 2 / 2, ausgewachsen 4 / 3 (Mahlzeit = 20 Vanilla-Hungerpunkte
   = 1 Honig, Schale = 0,5 l -> ausgewachsen 1,5 l am Tag). Plan: zuerst Forschung mit Quellen (Futter- und Wasserbedarf echter Braunbaeren je Koerpergewicht, Jahreszeit;
   Vanilla-Kalorien/Hungerwerte der Spiel-Lebensmittel), dann Kevin zwei Varianten (realistisch / spielbar) mit Tabelle je Groesse zur Wahl, erst dann bauen.
Kevin ~01:05, woertlich: *"so jz hoer zu wichtige regeln beim schlafen/ausgelogt/nicht geladen in der welt weit out of range  duerfen seine beduerfnisse nie steigen"*
-> **FESTE REGEL (Korrektur-Lauf):** Hunger, Durst, Muedigkeit steigen NIE, wenn (a) der Baer schlaeft ODER sein Besitzer schlaeft (Zeitraffer im Bett), (b) der Besitzer
   abgemeldet ist, (c) der Baer nicht geladen ist, (d) der Baer weit weg vom Besitzer ist (Vorschlag: weiter als die Ladeweite, ~70 Kacheln -- im MP haelt sonst ein
   anderer Spieler ihn geladen und die Werte liefen weiter). Heute schon eingefroren (T `server/BanditsNPCBearNeeds.lua:424-430` counts()): abgemeldet, nicht geladen
   (kein Koerper, nicht mitfahrend). NEU: (a) -- heute steigen Hunger/Durst auch im Schlaf (:459-461 "auch im Schlaf"), nur die Muedigkeit sinkt; Schlaf-Abbau der
   Muedigkeit bleibt. NEU: (d). Leben-Abzug bei 100 und Tagesabschluss/Vertrauen folgen derselben Sperre (nur gezaehlte Stunden); kein Nachholen nach dem Laden (maxDtH).
Kevin ~01:10, woertlich: *"wenn ein spieler schlaeft schlaeft der baer immer mit legt sich neben dem spieler und wenn der spieler vorspult das spiel dan legt er sich auch zum schlafen hin ausser gegner sind in der naehe dann kaempft er"*
-> **Korrektur-Lauf:** (1) Besitzer schlaeft -> Baer schlaeft IMMER mit, geht zu ihm und legt sich daneben (heute schon: B._ownSleep, Weg sleepWalkMs 30 s, sleepNear 2,5;
   T `server/BanditsNPCBearSleep.lua:99-135`) -- auch aus Bleiben/Sitz/Frei; ist er zu weit weg zum Hingehen (nicht in der Naehe geladen), schlaeft er, wo er ist (Claudes Annahme).
   (2) NEU: Besitzer spult vor (Spieltempo > 1) -> der Baer legt sich ebenfalls schlafen (neben dem Besitzer wie bei 1). Beleg Vanilla: `UIManager.getSpeedControls():getCurrentGameSpeed()`
   V:`client/Context/ISMenuContextWorld.lua:37`, V:`client/Foraging/ISBaseIcon.lua:63`; der Client meldet es mit der Bitte "Sleep" (heute player:isAsleep(), client/BanditsNPCBearPose.lua).
   Im MP gibt es Vorspulen nur, wenn alle schlafen -> dort zaehlt (1). (3) Gegner in der Naehe (sleepWakeR 8) -> er wacht auf und kaempft (heute: wokeFleeMs 5 s schlaftrunken).
   Zusammen mit der Regel 01:05: solange er schlaeft, steigen seine Beduerfnisse nicht.
Kevin ~01:15, woertlich: *"dann nimm dein vorschlag fuer den mp"* -> (d) BESTAETIGT: weiter als ~70 Kacheln vom Besitzer (Ladeweite) = eingefroren, auch wenn ihn im MP ein
   anderer Spieler geladen haelt; im SP faellt das mit "nicht geladen" zusammen. Wert als B.CFG (z. B. needFreezeR = 70), unter dem Lade-Rand von 76 Kacheln.
Kevin ~01:40 (Auswahl "Welchen Trinkwert soll der Baer bekommen?", Netzsuche `begleiter/bedarf_echte_baeren.md`): *"Mitte, ~6 %"*
-> **Trinkbedarf = 6 % des Koerpergewichts je Spieltag.** Gewicht je Groesse (Claudes Annahme aus den Quellen, Kevin darf aendern): Junges ~25 kg, halbstark ~80 kg,
   ausgewachsen ~250 kg (an statAt 0.35 / 0.75 / 1.35, dazwischen gleitend wie carryAt) -> **1,5 l / 4,8 l / 15 l am Tag** (heute 0,5 / 1 / 1,5 l; bowlsAt {1,2,3}
   wird daraus abgeleitet: Liter / bowlL 0,5 -> 3 / 9,6 / 30 Schalen). Traenken aus der Hand und selbst trinken nehmen je Aktion so viel, wie bis 0 % fehlt (B.DrinkNeedL),
   damit niemand 30 Mal klicken muss. Gilt fuer den Hunger-/Durst-Umbau "realistisch nach Groesse" (01:00); Futter-Zahlen noch offen (Netzsuche Futter folgt).
Kevin ~01:55 (Netzsuche Futter, `begleiter/bedarf_echte_baeren.md`): *"da nehmen wir dann auch die mitte ;D"* und Auswahl "Wie soll das Futter zaehlen?": *"Nach Saettigung"*
-> **Futterbedarf = Mitte ~10 % des Koerpergewichts (Junges ~3 kg / halbstark ~8 kg / ausgewachsen ~25 kg echtes Futter je Tag), gezaehlt NACH SAETTIGUNG:**
   umgerechnet ueber den Menschen (Annahme ~2 kg Essen je Tag) -> Junges ~1,5 x, halbstark ~4 x, ausgewachsen ~12,5 x der Vanilla-Hungerpunkte, die ein SPIELER je
   Spieltag verbraucht (Zahl im Lauf aus Vanilla belegen: Hunger-Anstieg je Stunde des Spielers). Jedes Futter sattigt nach seinem Vanilla-Hungerwert (HungerChange,
   z. B. Steak 40, Wild 80, Honig 20, Apfel 16), wie heute (B.MealsOf). Heute: mealsAt {1,2,4} x 20 Punkte = 20 / 40 / 80 Punkte je Tag. Dazwischen gleitend mit der Groesse.
Kevin ~02:00, woertlich: *"trinken ist ja noch leicht achja waer cool du konntest noch einbauen das der baer in wassernaehe automatisch zum wasser laeuft wenn man ka 10-20 kacheln entfernt ist und er selbst staendig dann eine trink animation abspielt mit sound wenns geht und dann sich komplett voll trinkt aber nicht blitzschnell das soll schon bisschen dauern ;D"*
-> **Neues Paket "Wasser in der Welt" (zusammen mit den Troegen, B-Liste):** durstig (ab 50 %, wie das Selbst-Trinken) und offenes Wasser (Fluss/See) bzw. Wassertrog in
   ~10-20 Kacheln -> er geht SELBST hin (nicht im Kampf, nicht in Bleiben/Sitz? -- im Plan klaeren), spielt eine TRINK-ANIMATION (neuer Clip -> Modell-Lauf; erst pruefen, ob
   Vanillas Tier-AnimSets einen Trink-Knoten haben) mit Ton (Vanilla-Tier-Trinkton belegen), trinkt sich bis 0 % voll, LANGSAM (Vorschlag: ~1 Spielstunde fuer einen
   ausgewachsenen Baeren von 50 auf 0), dann zurueck zum Befehl. Wasser-Kacheln/Trog-Erkennung nur mit Vanilla-Beleg (Angeln/Troege). Gefahr -> bricht ab und kaempft.
Kevin ~02:05, woertlich: *"wie viel muss er nach saettigung fressen? schon heute zeigt die npc crew mod die essenswerte an also fuer jeden sichtbar ;D"*
   Stand: NPC Crew zeigt unter jedem Lebensmittel-Tooltip einen Kasten mit Hunger (z. B. -40), Kalorien usw. fuer alle (NC `client/ISUI/BanditsNPCFoodStats.lua:8`, `:267`).
   Spieler-Tagesbedarf in Hungerpunkten: Konstante gefunden (V `shared/defines.lua:14` HungerIncrease = 0.0000032 * 3, Schlaf :17), Umrechnung je Spieltag noch NICHT
   gemacht (braucht den Jar-Weg Stats/GameTime) -> im Lauf belegen, dann Tabelle "je Tag: x Steaks / y Wild / z Honig" je Groesse.
   **Vorschlag (an Kevin):** im Baeren-Inventar und im Futter-Tooltip zusaetzlich "satt fuer ~x % seines Tagesbedarfs" je Stueck; NPC Crews Kasten nicht kopieren.
