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
