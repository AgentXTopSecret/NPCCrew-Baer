# Forschung baer-schlaf: LEISER SCHLAFTON (09.11.2026)

Nur Forschung: nichts gebaut, keine Mod-Datei geaendert, nichts heruntergeladen (nur Webseiten gelesen, keine Audiodatei abgerufen),
keine Renders. Eigene Hilfsdateien nur in `_arbeit/baer_schlaf/ton/` (Messskripte, Messtabellen, Spektrogramme, `jar/` mit
javap-Auszuegen). **Statisch geprueft, nichts gehoert, nichts gespielt.**

Kevins Wunsch (ENTSCHEIDUNGEN.md:113-116): *"vllt noch mit leisen baeren schlaf sound wenn es sowas gibt zum runterladen im internet,
wenn nicht dann ohne ton"*; Massstab `baer/sound/roh/QUELLEN.txt`: bisher nur gemeinfreie Aufnahmen von US-Behoerden, jeder Download
einzeln von Kevin freigegeben.

## 0. Ergebnis in Kuerze

1. **Eine freie (gemeinfreie oder CC0) Aufnahme eines schlafenden, schnarchenden oder ruhig atmenden Baeren gibt es nach dieser Suche
   nicht.** Durchsucht: soundbible.com, freesound.org (auch mit CC0-Filter), Wikimedia Commons, NPS (Baeren-Seite, Yellowstone-
   Tonbibliothek, NPGallery), FWS-Tonarchiv, Acoustic Atlas (MSU), Pixabay, earth.fm, Tierstimmenarchiv; Zapsplat und BBC liessen sich
   nicht lesen (403 bzw. gesperrt).
2. Die **einzige echte Aufnahme eines ruhenden Baeren** ("Grizzly Bear breathing", Acoustic Atlas 2191, 1:05) steht unter **CC BY-NC 4.0
   -> ungeeignet** (NC). Alles Freie ist Fressen, Trinken, Warn-Schnauben, Knurren oder Jungtier-Laute.
3. **Vanilla hat keinen Schlaf-, Schnarch- oder Atemton fuer Tiere.** Die einzigen "Sleep"-Toene sind menschliche Stimmen
   (`VoiceMaleSleep`/`VoiceFemaleSleep`), dazu `FishBreath` (Fisch). Bandits hat nur menschliches Keuchen (`ZSBreath_*`).
4. **In den drei vorhandenen Rohaufnahmen gibt es keine ruhige Atemstelle** (Messung Abschnitt 3: null Treffer). Einziges atemartiges
   Stueck ist das schon geschnittene `NCBear_Huff.wav` (0,21 s Atemstoss).
5. **Empfehlung: ohne Ton bauen (Kevins eigener Rueckfall)**, aber den Weg schon anlegen (Rassen-Schluessel `sleep`, Abschnitt 4), damit
   ein Ton spaeter nur eine Datei und eine Zeile ist. Wahlweise, nur auf Kevins Wort: (a) als Test den vorhandenen Huff sehr leise und
   selten im Schlaf (kein Download), oder (b) einen der Kandidaten aus Abschnitt 1 einzeln freigeben.

## 1. Internet-Kandidaten (hoechstens 8; zuerst die rechtlich brauchbaren)

Ehrlich vorweg: **keiner davon ist ein schlafender Baer.** "Geeignet" heisst hier nur: Lizenz erlaubt das Weitergeben in einer kostenlosen
Workshop-Mod. Freesound-Dateien kann nur ein angemeldetes Konto herunterladen (FAQ https://freesound.org/help/faq/ : *"To download a
sound, first make sure you are logged into your registered account."*) -- das muesste Kevin selbst tun, wir legen kein Konto an.

| # | Seite / Titel | Datei, Groesse, Dauer, Format | Urheber | Lizenz (Link) | Workshop? Namensnennung? | Inhalt laut Beschreibung, Qualitaet | Schlaf? |
|---|---|---|---|---|---|---|---|
| 1 | https://npgallery.nps.gov/AssetDetail/e82a43bb-d16e-46d9-84d0-27794962bf16 "bear_cub_feeding.wav" | WAV 5,3 MB (Byte nicht angegeben), 31 s; MP3 489,6 KB; Abtastrate nicht angegeben | NPS, Sequoia & Kings Canyon (Kontakt Joshua Flickinger), 10.07.2019 | Seite: *"Constraints Information: Public domain"*, *"Digital assets without any copyright restrictions are public domain."* | ja; Nennung nicht Pflicht (wie QUELLEN.txt: "National Park Service" nennen) | "Audio recording of a Black Bear cub feeding, recorded at Crystal Cave Road in SEKI" -- Rauschen/Fremdtoene nicht beschrieben | **nein** (Jungtier frisst/saeugt). Saeugende Jungtiere "summen" als Wohlfuehllaut (Peters, Owen, Rogers 2007, *Humming in bears*, https://link.springer.com/article/10.1007/BF03194236; Bear Center https://bear.org/?p=236) -- ob das hier zu hoeren ist: **ungehoert** |
| 2 | https://freesound.org/people/YleArkisto/sounds/249443/ "Karhut heraeaevaet, kurlutus / A group of bears waking up in a zoological park, gurgle ..." | WAV 48 kHz/24 Bit Stereo, 5:16,454, 86,9 MB | Yle Arkisto (Finnischer Rundfunk), Nagra-Band, Aehtaeri (Tierpark), 06.05.1975 | CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ | ja, **Namensnennung Pflicht**; nicht gemeinfrei (weicht vom Massstab QUELLEN.txt ab) | Braunbaeren wachen auf, durchgehendes Gurgeln nah am Mikrofon bis 3:50, dann etwas Bewegung; **Voegel im Hintergrund**; altes Analogband | **nein** (Aufwachen/Gurgeln, nicht Atmen) |
| 3 | https://freesound.org/people/YleArkisto/sounds/249440/ "Karhut syoevaet ja murisevat / Bears eating and growling ..." | WAV 48 kHz/24 Bit Stereo, 2:19,969, 38,4 MB | Yle Arkisto, Nagra-Band, Aehtaeri, 22.04.1975 | CC BY 4.0 (wie 2) | ja, Namensnennung Pflicht | Fressen mit "tuhinaa" (Schnauben/Schnaufen) und Schmatzen, Tapsen im Schnee; ab ~40 s lautes Heulen/Knurren; **Voegel und leiser Verkehr** im Hintergrund | **nein** (Schnaufen beim Fressen) |
| 4 | https://freesound.org/people/Nivatius/sounds/519597/ "huf grizzly bear" und .../519598/ "huf grizzly" | MP3 44,1 kHz Mono, 0,487 s / 7,0 KB bzw. 0,358 s / 5,4 KB | Nivatius, aus NPS-Yellowstone-Material ("slightly edited audio provided as public domain by the yellowstone national park service") | CC0 http://creativecommons.org/publicdomain/zero/1.0/ | ja, keine Nennung noetig | einzelne Schnauber ("breathing an vocalizing"), MP3, sehr kurz | **nein** -- vermutlich Ausschnitte aus #5 (Warn-Schnauben eines gefangenen Baeren; Herkunft nicht bewiesen) |
| 5 | https://commons.wikimedia.org/wiki/File:Yellowstone_sound_library_-_Grizzly_Bear_vocalizations_-_001.mp3 | MP3 192 kbit/s, 65,14 s, 1.569.578 Byte | NPS & MSU Acoustic Atlas / Dan Bergum (Handy), 20.05.2016 | gemeinfrei (US-Bundeswerk, CC-PD-Mark auf der Seite); Quelle https://www.nps.gov/yell/learn/photosmultimedia/grizzlysounds.htm , dort Tonbibliothek: *"in the public domain"*, *"please credit the National Park Service"* (https://www.nps.gov/yell/learn/photosmultimedia/soundlibrary.htm) | ja | Warn-Schnauben, Kieferklappen (0:35, 0:57), tiefes Knurren eines Baeren in der Kastenfalle; Handyaufnahme | **nein** (Stress) |
| 6 | https://freesound.org/people/selsel/sounds/824784/ "Bear slurping from mud puddle" | WAV 48 kHz/24 Bit Stereo, 0:51,094, 14,1 MB | selsel, Silver Salmon Creek, Lake Clark NP, Alaska | CC0 (Link wie 4) | ja | Kuestenbraunbaer schluerft aus einer Pfuetze | **nein** (Trinken; ob zwischen den Schlucken Atem zu hoeren ist: ungehoert) |
| 7 | https://commons.wikimedia.org/wiki/File:Grizzly_bear_sound_effect.wav | WAV ~2:04, 21.817.934 Byte | Zagzav12, "Own work" (2012) | *"Creative Commons CC0 1.0 Universal Public Domain Dedication"* | ja | Seite beschreibt den Inhalt nicht ("Grizzly bear sound effect"); Herkunft ungeklaert | **unbekannt** |
| 8 | https://acousticatlas.org/item.php?id=2191 "Grizzly Bear breathing" (Blog: https://www.lib.montana.edu/acoustic-atlas/acoustic-atlas-blog/posts/what-is-the-sound-of-one-bear-sleeping.html) | MP3 254 KB, 1:05 (Original 48 kHz/24 Bit), Telinga-Parabolmikrofon, Sound Devices 702 | Jennifer Jerrett, Blacktail Ponds, Yellowstone, 15.03.2015 23:23 | *"Audio Rights: https://creativecommons.org/licenses/by-nc/4.0/"* | **UNGEEIGNET (NC)** | "Grizzly bear at rest breathing"; Blog: *"the slow, steady, breaths of a resting bear"*, aus dem Auto heraus aufgenommen | **ja, ruhend** -- die einzige echte; Lizenz verbietet sie nach Projektregel |

Ausserdem gesehen und **ungeeignet** (nicht als Kandidat gezaehlt):
- earth.fm "Dreams of Bears" (Vladimir Arkhipov, Kamtschatka; *"a mother bear and her two cubs breathing gently as they take a nap"*,
  https://earth.fm/recordings/dreams-of-bears): **keine Lizenz, kein Download, nur Stream** -> ungeeignet. Inhaltlich genau das Gesuchte.
- tbsounddesigns "BEARBreath_09.wav" (https://freesound.org/people/tbsounddesigns/sounds/416857/): *"Bear breath, emulated using human
  voice and vocal transformer"*, CC BY 4.0, 1,269 s, 110,0 KB -- **kein Baer** (Mensch mit Effekt).
- BBC Sound Effects: RemArc-Lizenz nur *"personal, educational or research purposes"* (Sekundaerquellen, z. B.
  https://www.prsformusic.com/m-magazine/news/bbc-releases-sample-library-with-thousands-of-sound-effects ; Lizenzseite selbst nicht abrufbar)
  -> ungeeignet. Ob es dort einen schlafenden Baeren gibt: ungeprueft (Seite gesperrt).
- Zapsplat: Seiten antworten 403, nicht geprueft. Pixabay: unter "bear sleeping"/"bear breathing" nur Menschen, Hunde, Knurren, unklare
  Herkunft (z. B. "Bear sound mks0127", Beschreibung nur *"Free for use"*) -> kein Kandidat.
- soundbible.com (Suche "bear"): kein Schlaf; Baeren dort entweder *Personal Use Only* (ungeeignet) oder die schon benutzten FWS/NPS-Rufe
  (241, 242, 868) und "3 Baby Cubs Grunt And Growl" (FWS, Jungtiere knurren).
- Tierstimmenarchiv Berlin (Ursus arctos "Prusten und Ruf", Zoo Hannover 1960): CC BY-NC-SA 4.0 (Suchtreffer Deutsche Digitale
  Bibliothek) -> ungeeignet.
- Western Soundscape Archive (NPS-Yosemite-Baeren): laut Suchtreffer CC BY-NC-ND -> ungeeignet (Seite nicht selbst gelesen).
- NPS-Baerenseite https://www.nps.gov/subjects/bears/sounds.htm und Yellowstone-Grizzlyseite: nur Warnlaute, Fressen, Bruellen, Mutter mit
  Jungen -- kein Schlaf.

Fazit Internet: Wer einen echten Schlafton will, muesste entweder (a) eine Ausnahme vom Massstab "gemeinfrei" machen (CC BY mit
Namensnennung, #2/#3 -- aber auch die sind kein Schlaf) oder (b) bei der Yellowstone-Tonbibliothek nachfragen, ob "Grizzly Bear breathing"
(#8) dort wie die anderen Jerrett-Aufnahmen gemeinfrei erscheinen kann (die NPS-Seite nennt ihre Dateien gemeinfrei; #8 steht dort aber
nicht -- **offen, nur Kevin kann fragen**).

## 2. Vanilla- und Bandits-Toene (per Namen abspielbar, liegen im Spiel)

Gesucht in `media/scripts/**/*.txt` nach sleep/snor/breath/yawn/sigh/purr/pant/rest und in der Jar nach den Namen.

| Name | Fundstelle | Ereignis, Reichweite | Passt? |
|---|---|---|---|
| `VoiceMaleSleep` | `scripts/generated/sounds/player/sounds_player_voice_male.txt:303-311` (doppelt :323-331) | `event = Character/Voice/Male/Sleep`, `category = Player`, `distanceMax = 150` | **nein**: menschliche Stimme. Kein Aufrufer in Vanilla-Lua; in der Jar nur in `zombie/scripting/objects/SoundKey` und `generation/SoundScriptGenerator` (eigene Suche `ton/jar_grep.py`). Inhalt liegt in der FMOD-Bank: **ungehoert** |
| `VoiceFemaleSleep` | `.../sounds_player_voice_female.txt:283-291` (doppelt :303-311) | wie oben, Female | nein (Mensch) |
| `VoiceMaleSighReliefed` u. a. | `sounds_player_voice_male.txt:353`, female `:333` | Seufzer | nein (Mensch) |
| `FishBreath` | `scripts/generated/sounds/sounds_ambience.txt:301-309` | `event = World/Fish/Breath`, `master = Ambient`; benutzt von Jar `zombie/iso/FishSplashSoundManager` | nein (Fisch) |
| Tier-Toene | `scripts/generated/sounds/animals/*.txt` (22 Dateien) | je Art nur Idle, Stressed, Pain, Death, Schritte, Bodyfall, dazu `AnimalFoleyEatGrass` usw. | **kein Schlaf-/Atemton fuer irgendein Tier** |
| Bandits `ZSBreath_Male`/`_Female` | Bandits `42.21/media/scripts/zs_sounds.txt:531-541`, Datei `male_breath.ogg` | `is3D = true`, `distanceMin = 1`, `distanceMax = 4`, `volume = 0.6`; gespielt beim Rennen (`BanditUpdate.lua:443-463`) | nein (Mensch keucht); aber **gutes Vorbild fuer die Werte eines leisen Nah-Tons** |

Ergebnis: **Kein vorhandener Spielton taugt als Baeren-Schlafton.**

### 2.1 Wie NCBearTest heute seine Toene spielt (Ist-Stand)

- **Tonskript** `NCBearTest/42/media/scripts/nc_bear_sounds.txt`: `module Base`, je Ton `category = Animals` und ein `clip { file =
  media/sound/NCBear_*.wav, distanceMax = ... }` (Roar 150, Growl 80, Huff 30, HuffSoft 20 bei :53-61, Pain 80). Form wie Vanilla
  `sounds_zombie_voice_tutorial.txt:3-11`. Dateien Mono, 44,1 kHz, 16 Bit (`baer/sound/schnitt.md`).
- **Rassen-Toene** `NCBearDefs.lua:48-57`: `sounds = { pain = {...priority 50}, huff = {...10}, huffsoft = {... priority = 5}, growl1..3
  = {...20} }`, alle `slot = "voice"` (Form `CowDefinitions.lua:315-330`).
- **Abspielen ueber die Rasse**: `a:playBreedSound("huffsoft")` (`NCBearFight.lua:1481`), `"huff"` (:557), `"growl"..n` (:543); Beleg
  Vanilla `animal:playBreedSound("pick_up")` (`shared/TimedActions/Animals/ISHutchGrabAnimal.lua:31`). Die Engine selbst spielt `pain`
  (`AnimSets/buck/hitreaction/hitreaction1.xml:8-12` PlayBreedSound) und `fallover` (`buck/falldown/falldown.xml:15-19`).
- **Ueber Animationsereignisse**: `PlaySound NCBear_Roar` bei 0,27 im Knoten `NCBear_Rear.xml:14-18`, aehnlich Bite/Maul/Slam/Swipe.
- **Alltags-Schnauben (das Vorbild fuer den Schlafton)** `NCBearFight.lua:1458-1488` `dailyHuff`: im 0,5-s-Suchtakt je Baer ein Termin
  `huffMin + ZombRand(huffSpread+1)` s (90-240 s, :99, ZombRand-Beleg `ISMilkAnimal.lua:25`), im Sitzen mal 3 (:163), dazu einmal, wenn
  der Spieler unter 3 Kacheln kommt (:164), mindestens 60 s Abstand (:162), nach Kampf 20 s still (:166, :576).
- **Treffer- und Weltlaerm** (nicht fuer den Schlaf): `z:playSound(...)` am Zombie (:918, :924), `addSound(...)` als Weltgeraeusch (:1006).
- **Nur Einzelspieler**: `NCBearFight.lua:4-5` ("Diese Datei tut im Mehrspieler nichts").

### 2.2 Was die Engine dabei tut (Jar 42.21, javap-Auszuege in `ton/jar/`)

- `IsoAnimal.playBreedSound(String)` (Offset 0-128): holt `AnimalBreed.getSound(key)`; mit `slot` geht es in den Stimm-Slot: laeuft dort
  ein Ton **hoeherer Prioritaet**, kommt nichts (Offset 40-61), sonst `AnimalSoundState.start(name, prio)` (Offset 106-116). Ohne `slot`:
  `playSoundLocal` (Offset 120-125).
- `AnimalSoundState.start` (Offset 1-139): stoppt zuerst den alten Slot-Ton (`stop()`, Offset 1), spielt ueber
  `getEmitter().playVocals(name)` (Offset 20-27). **Ein Weltgeraeusch (lockt Zombies) gibt es nur, wenn die Sandbox
  `AnimalSoundAttractZombies` an ist UND die Tierdefinition `idleSoundRadius > 0` und `idleSoundVolume > 0` hat** (Offset 33-112).
  NCBearDefs setzt beides nicht (grep: kein Treffer), und die Felder sind ohne Eintrag 0 (Jar `AnimalDefinitions`: nur bei vorhandenem
  Schluessel gesetzt, Offset 412-449). -> **Ein Schlafton lockt keine Zombies und weckt den Baeren nicht ueber respondToSound.**
  Diese Felder darum auch spaeter NIE fuer den Baeren setzen.
- `IsoAnimal.updateVocalProperties` kehrt auf dem Server sofort zurueck (Offset 0-6, `GameServer.server`): Tierstimmen sind **Sache jedes
  Clients**. Dazu `kampf_spez.md:260`: "Animation, Anim-Ereignisse, Toene: jeder Client fuer seine Kopie; der Server spielt keine Ereignisse".
- Die Engine waehlt von selbst nur `idle`, `stressed`, `idle_walk` (`IsoAnimal.chooseIdleSound`, Offset 64-185); der Baer hat keinen davon.
  **Der Schluessel `sleep` ist frei** (in IsoAnimal kein String "sleep"/"snore" im Ton-Zusammenhang). `forceNextIdleSound` ist privat
  und ohne Lua-Setter -> nicht nutzbar.
- `IsoAnimal.onPlayBreedSoundEvent(String)` (Offset 0-59): Animationsereignis `PlayBreedSound` mit einem Wert ausser run/walk/walkFront/
  walkBack geht direkt an `playBreedSound`. Vanilla nutzt es in **Schleifen-Knoten** fuer wiederholte Toene je Zyklus:
  `AnimSets/buck/walk/defaultWalk.xml:6-25` (vier Schritt-Toene je Gang-Zyklus; der Knoten hat kein `m_Looped`, Vorgabe `true` laut Jar
  `AnimNode.<init>` Offset 85-87).
- Tonskript-Felder (Jar `GameSoundScript`, Konstruktor/`LoadClip`): Ton-Ebene `category, clip, is3D, loop, master,
  maxInstancesPerEmitter`; Clip-Ebene `distanceMax, distanceMin, event, file, pitch, reverbFactor, reverbMaxRange, stopImmediate, volume`.
  **Vorgaben ohne Eintrag** (Jar `GameSoundClip.<init>` Offset 5-23, `GameSound.<init>` Offset 11-12): `volume 1`, `pitch 1`,
  **`distanceMin 10`**, `distanceMax 10`, `is3d true`. Folge: ein leiser Nah-Ton braucht ausdruecklich `distanceMin = 1` (sonst volle
  Lautstaerke bis 10 Kacheln; heute hat z. B. HuffSoft keinen distanceMin). `volume`/`distanceMin` neben `file` belegt in Bandits
  `zs_sounds.txt:537-539`; `pitch` ist nur in der Jar gesehen, in keinem Skript -> **nur Jar, braucht Kevins Wort**.

## 3. Rueckfall ohne Download: die drei Rohaufnahmen

Messung `ton/ruhe_messung.py` (nur lesen; 50-ms-Fenster, Pegel ueber dem Grundrauschen, Baender, spektrale Flachheit als "Atem-artig",
Tonalitaet), Tabellen `ton/messung_soundbible_*.txt`, Spektrogramme `ton/spek_soundbible_*.png` (angesehen), Liste
`ton/ruhe_kandidaten.txt`. Gesucht: mind. 0,30 s am Stueck, 6-20 dB ueber Grundrauschen, rauschartig (Flachheit > 0,15), nicht tonal,
tiefes Band nicht schwaecher als die Mitte. **Ergebnis: KEINE Stelle.**

- **241** (FWS, 15,5 s, Spitze -17,8 dBFS, Grund -42,4 dBFS): Fenster nur "Boden" (57) oder "leise-tonal" (98) -- eine Reihe
  rhythmischer Klagerufe mit Obertoenen alle ~1,3 s (Spektrogramm); dazwischen nur Rauschen.
- **242** (FWS, 20,8 s, Grund -35,6 dBFS): die "leisen rauschartigen" Fenster liegen alle bei 0,1-3,7 s = Wind am Mikrofon (schnitt.md:
  0-10,8 s Wind). Bei 3,5-10,5 s gibt es tiefe Brummstapel 120-380 Hz, aber nur wenige dB ueber dem Wind, und das 40-110-Hz-Band springt
  um bis zu 27 dB (14-41 dB, `ton/tiefband_242.py`) -- Windstoesse. Inhaltlich tiefes Knurren einer Baerin, die Junge verteidigt
  (QUELLEN.txt), kein Schlaf.
- **868** (NPS, 6,2 s): fast nur tonale Jungtier-Laute 380-450 Hz mit Obertonreihe, teils stark wellig (0-1,2 s, 5,3-5,9 s) --
  nach dem Bild eher Wimmern/Rufen als Summen (die NPS-Seite zur Aufnahme "Bear with cubs" nennt *"mewling and crying noises"*,
  https://www.nps.gov/subjects/bears/sounds.htm). Ein weinendes Jungtier als Schlafton waere falsch. Der einzige Atemstoss 3,16-3,31 s
  ist schon `NCBear_Huff.wav`; das Ende 5,93-6,2 s ist zu schwach (schnitt.md).

Also bleibt ohne Download nur:
- **R1 ohne Ton** (Kevins Rueckfall).
- **R2 Huff wiederverwenden** (kein neuer Schnitt, keine neue Datei): ein eigener Skript-Eintrag mit derselben Datei, sehr leise und nah,
  z. B. `sound NCBear_HuffSleep { category = Animals, clip { file = media/sound/NCBear_Huff.wav, distanceMin = 1, distanceMax = 6,
  volume = 0.4, } }` und alle 8-15 s einmal im Schlaf. Ehrlich: ein 0,21-s-Atemstoss ist kein ruhiges Schlafatmen und kein Schnarchen,
  Kevin nannte den Huff schon "sehr leise; Huff-Schnitt ist der wackeligste" (ENTSCHEIDUNGEN.md:78). Nur als Hoertest.
- (Nicht empfohlen, nur der Vollstaendigkeit halber: Atemrauschen per Python selbst erzeugen -- urheberrechtlich frei, klingt aber leicht
  kuenstlich; Kevin sagte "wenn nicht dann ohne ton", also nur auf sein ausdrueckliches Wort.)

## 4. Der Weg fuer einen Schlafton (gleich, welcher Ton es wird -- oder spaeter)

Alles nach dem heutigen, schon gespielten Muster (huffsoft). Namen wie die sechs vorhandenen Toene (`NCBear_*`); die Umbenennung aller
NCBear-Dateien gehoert gesammelt in B1 (ENTSCHEIDUNGEN.md:50). Kollisionsprobe: `NCBear_Sleep`, Rassen-Schluessel `sleep` -- kein Treffer
in NPC Crew `42/media`, Vanilla-Skripten, Bandits-Skripten. **Achtung beim spaeteren Greppen:** `UI_BN_Bear` trifft auch
`UI_BN_Beard_*` (NPC Crew `BanditsNPCAppearance.lua:244`, `Translate/EN/UI.json:290`) -- immer mit Unterstrich `UI_BN_Bear_` suchen.

1. **Tonskript** (in `nc_bear_sounds.txt`):
   `sound NCBear_Sleep { category = Animals, clip { file = media/sound/NCBear_Sleep.wav, distanceMin = 1, distanceMax = 8, volume = 0.6, } }`
   -- kein `loop` (Einzelton, nichts muss gestoppt werden), `is3d` ist Vorgabe. Werte nach Bandits `zs_sounds.txt:531-541` (Atem: 1/4/0,6);
   8 statt 4 Kacheln, weil der Baer groesser ist -- **Vorschlag, nach Gehoer einstellen**.
2. **Rasse** (`NCBearDefs.lua` `rassen().sounds`): `sleep = { name = "NCBear_Sleep", slot = "voice", priority = 1 }` -- niedrigste Stufe:
   Schmerz (50), Knurren (20), Huff (10), HuffSoft (5) gehen vor und brechen ihn ab (Jar playBreedSound Offset 40-61, start Offset 1);
   er bricht nie einen von ihnen ab.
3. **Ausloesen**, zwei belegte Wege:
   - **A (empfohlen, auch fuer MP): Animationsereignis im Schlaf-Schleifenknoten** (z. B. `AnimSets/buck/idle/NCBear_Sleep.xml`, Form
     wie `NCBear_Sit.xml`): `<m_Events><m_EventName>PlayBreedSound</m_EventName><m_TimePc>0.xx</m_TimePc><m_ParameterValue>sleep
     </m_ParameterValue></m_Events>` am Ausatmen des Clips. Vorbild `buck/walk/defaultWalk.xml:6-25`. Ton sitzt genau auf der
     Brustbewegung, kein Lua je Bild; jeder Client spielt ihn fuer seine Kopie. Folge: ein Ton je Schleifendurchlauf -- ist das zu oft,
     den Schleifenclip mit 2-3 Atemzuegen bauen und nur EIN Ereignis setzen (Absprache mit dem Lauf Schlaf-Animation).
   - **B (nur Einzelspieler, wie dailyHuff):** im 0,5-s-Suchtakt, solange der Baer schlaeft: Spieler (`getSpecificPlayer(0)`, belegt
     `client/DebugUIs/DebugContextMenu.lua:900`) naeher als ~10 Kacheln und gleiche Ebene, Termin `clock + 6 + ZombRand(7)`:
     `a:playBreedSound("sleep")` (`ISHutchGrabAnimal.lua:31`). Mehrere Varianten wie `growl1..3` ueber eigene Schluessel
     (`NCBearFight.lua:543`); mehrere `clip` in einem Ton gibt es in der Jar (`GameSound.getRandomClip`), aber in keinem gesehenen Skript ->
     nicht benutzen.
4. **Aufwachen:** nichts zu stoppen (Einzeltoene <= 2 s); ein Knurren/Huff beim Aufwachen beendet ihn sowieso. Ein Schleifenton (`loop =
   true`) braeuchte ein Stoppen am Tier-Emitter -- dafuer gibt es keinen gesehenen Vanilla-/Bandits-Aufruf am Tier -> **nicht** so bauen.
5. **Zombies:** kein `addSound`, kein `idleSoundRadius` -> der Schlafton lockt nichts und laesst den Baeren nicht fliehen (2.2).
6. **SP/MP:** SP geht ueber beide Wege. MP: der Ton selbst braucht keinen Server und kein Paket (Client-lokal, 2.2), also kein Kick-Risiko;
   **offen** ist nur, ob der Zustand "schlaeft" (Animationsvariable bzw. ModData) bei jedem Client ankommt -- das gilt fuer die ganze
   Baer-KI, die heute nur im SP laeuft (`NCBearFight.lua:4-5`, `kampf_spez.md:265`). Weg A braucht dafuer nichts Zusaetzliches, Weg B
   eine Client-Pruefung im OnTick.
7. **NPC Crew / Copy-Paste:** Tonskript, `media/sound/...wav` und die Zeile in der Rasse wandern 1:1; kein Menue, kein Testbefehl. Ein
   An/Aus fuer den Schlafton, falls gewuenscht, als Spieler-Einstellung wie Namensschild/Balken (ENTSCHEIDUNGEN.md:106: "Einstellung JE
   SPIELER"), nicht als Cheat. Bei CC-BY-Toenen gehoert die Namensnennung in die Mod-Beschreibung und eine Quellen-Datei
   (wie QUELLEN.txt).

## 5. Empfehlung mit Begruendung

**Ohne Ton bauen, Weg A vorbereiten.** Begruendung: Kevins Bedingung ("wenn es sowas gibt ... wenn nicht dann ohne ton") ist nicht
erfuellt -- es gibt keine freie Aufnahme eines schlafenden Baeren; die einzige echte (Acoustic Atlas 2191) ist NC. Alles Freie wuerde
einen fressenden, knurrenden, gefangenen oder weinenden Baeren als "Schlaf" ausgeben, und Vanilla hat nichts Passendes. Weg A
(PlayBreedSound im Schlafknoten, Rassen-Schluessel `sleep`) kostet nichts, ist Vanilla-belegt, MP-tauglich und laesst spaeter einen Ton
mit EINER Datei und EINER Zeile nachruesten. Bis dahin bleibt das Ereignis einfach weg (ein fehlender Schluessel spielt nichts:
`playBreedSound` gibt bei `getSound == null` 0 zurueck, Offset 11-22).

Wenn Kevin trotzdem etwas hoeren moechte, in dieser Reihenfolge: (1) **R2 Huff leise im Schlaf** als Hoertest (kein Download, sofort
wieder raus); (2) Kandidat **#1 NPGallery bear_cub_feeding.wav** (gemeinfrei, kein Konto noetig, 5,3 MB) -- hoechstens fuer das Jungtier,
falls darin Summen ist; (3) **#2/#3 Yle (CC BY 4.0)** nur mit Ausnahme vom Massstab "gemeinfrei" und Kevins eigenem Freesound-Login.

## 6. Offene Fragen an Kevin

1. Ohne Ton (Empfehlung) -- oder als Hoertest den vorhandenen Schnauber sehr leise im Schlaf?
2. Soll eine CC-BY-Aufnahme mit Namensnennung erlaubt sein (Ausnahme vom bisherigen "nur gemeinfrei")?
3. Moechtest du selbst bei der Yellowstone-Tonbibliothek (NPS) fragen, ob "Grizzly Bear breathing" (Jerrett 2015) gemeinfrei
   freigegeben werden kann? Das waere der einzige echte Schlafatem.
4. Soll der Schlafton (wenn es einen gibt) pro Spieler abschaltbar sein?

## 7. Eigene Dateien dieses Laufs

- `_arbeit/baer_schlaf/forschung_ton.md` (dieser Bericht)
- `_arbeit/baer_schlaf/ton/ruhe_messung.py`, `tiefband_242.py`, `jar_grep.py` (nur lesend)
- `_arbeit/baer_schlaf/ton/messung_soundbible_{241,242,868}.txt`, `ruhe_kandidaten.txt`, `spek_soundbible_{241,242,868}.png`
- `_arbeit/baer_schlaf/ton/jar/` (aus projectzomboid.jar gezogene Klassen und javap-Text: IsoAnimal, AnimalBreed(+$Sound), AnimalSoundState,
  AnimalVocalsManager, AnimalDefinitions, GameSoundScript, GameSound, GameSoundClip, AnimNode, SoundKey, FishSplashSoundManager)
