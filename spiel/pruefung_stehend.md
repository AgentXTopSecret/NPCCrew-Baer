# Pruefung: stehender Baer (NCBearTest)

Statisch geprueft, nicht gespielt. Stand 07.11.2026, Spiel 42.21, gelesen im Jar und in Vanilla.

**Ergebnis:** Nichts gefunden, was das Ansehen verhindert. Die Zahlen des Bauberichts stimmen bis auf eine harmlose Abweichung. Vier kleine Nachbesserungen in der Lua-Datei, alle schon drin.

## Nachgebessert (`42/media/lua/client/NCBearTest.lua`)

| Fund | Schwere | Was jetzt |
|---|---|---|
| `instanceItem` liefert nil, wenn das Skript nicht geladen ist. `AddWorldInventoryItem` gibt es fuer String, ItemKey und InventoryItem (Jar, `IsoGridSquare`), nil trifft keine eindeutige Fassung. | klein | Klare Konsolenzeile statt Fehler im Menue |
| Der Probelauf `test = true` (Controller) baute das ganze Menue ins Unsichtbare und rief nie `setTest`, obwohl Vanilla genau das verlangt (`ISWorldObjectContextMenu.lua:122-128`). | klein | `if test then return ISWorldObjectContextMenu.setTest() end`, Form aus `DebugContextMenu.lua:350` |
| `NCBear_Spawn()` ohne Figur (Hauptmenue) griff auf nil zu. | klein | Klare Konsolenzeile |
| `% 360` hatte keine Fundstelle. | nur Kommentar | `ISKnob.lua:139` |

Danach alle vier Pruefer: `luacheck.py` ok, `scopecheck.py` ok, `localcount.py` hoechstens 21 Locals, `luacheck_pz.py` 0 Treffer. `--unused` meldet nur das unbenutzte Argument `player`, das die Ereignis-Signatur vorgibt. Datei ASCII, LF.

## Geprueft und in Ordnung

| Punkt | Beleg |
|---|---|
| Skript `nc_bear.txt` | Gleiche Felder wie `NCTurretTest` (im Spiel gesehen) und wie Vanilla: `mesh`, `texture`, `scale` (`models_items.txt:4648`), `ItemType = base:normal` (1099 Treffer), `DisplayCategory = Junk` (`drainable.txt:967`), `Icon`, `WorldStaticModel` (`alarmclock.txt:8-10`). `DisplayName` steht in Vanilla nicht mehr, der Parser kennt es aber (`Item` im Jar, Offset 232-246). |
| Pfade | `models_X/WorldItems/NCBear.fbx`, `textures/WorldItems/NCBear.png`, `textures/Item_NCBear.png`: Schreibweise wie Vanilla und wie das Turret. |
| FBX, in Blender eingelesen | 14.228 Dreiecke, 7.156 Punkte, 8.131 Spielpunkte (Punkt + UV + Normale), 21 Schalen (Rumpf + 20 Krallen), 0 offene Kanten, Volumen positiv wie beim Turret, alles weich schattiert. Masse 1,955 x 0,995 x 1,164, x von -0,798 bis +1,157, Boden bei 0. |
| Exportoptionen | Wortgleich mit `turret_export.py`. |
| Abwicklung | 44 Inseln, Fuellgrad 58,0 %, kein Texel von zwei Dreiecken belegt. |
| Textur | 2048 x 2048, RGB, kein Alpha. 0 Texel mit Gruen- oder Blaustich, also keine Grasfarbe. **Abweichung:** in 0,05 % der Texel steht ein Kanal auf 255, der Bericht nennt 0,01 %. Ohne Folgen. |
| Icon | 32 x 32 mit Alpha, Baer erkennbar. |
| Scale 0,544 | `MaleBody.x` Y 0 bis 0,9798 gemessen, 0,98 / 1,8 = 0,544. Baer 0,633 Mesh-Einheiten, 65 % der Figur. Turret 1,234, also 1,26 Figuren. |
| Gegenprobe, neu | `CowBody.x`: Hoehe 0,9456, Laenge 1,447. Mit 0,544 je Meter sind das 1,74 m und 2,66 m, das passt zu einer Kuh mit erhobenem Kopf. Der Baer ist 73 % so lang wie die Kuh. Ob die Animation die Figur noch skaliert, bleibt ungeprueft. |
| Atlas | Selbst gelesen: `renderMain` 12-24 (Option 3D-Bodengegenstaende), `renderAtlasTexture` 18-26, 27-39, 86-100, 197-208; `RenderJob.render` 88-113 (ueber 512 nach `tooBig`, dann 3D-Weg). Vorgaben im Jar: `WorldItemAtlas.Enable` an, `ItemsInChunkTexture` aus. `Core.scale` = Wurzel(2)/2/10/1,5 = 0,04714, Viewport 1024, Ortho 0,5333, also 135,8 Pixel je Mesh-Einheit. Baer nachgerechnet: 154 x 152 Pixel, gezoomt 385 x 380, bleibt im Atlas. Es wird nicht beschnitten. |
| Drehen | `ItemParams.isStillValid` 12-21 vergleicht `worldZRotation`, `angle.y` kommt direkt daher (Offset 807-814). Wirkt also sofort. |
| Licht | `basicEffect.frag`: Textur x min(Licht, 1), ohne Gamma. Umgebung 0,4 (`renderModel` 413-439). Das 1,95-fache Backen ist damit begruendet. |
| Lua-Fundstellen | Alle Zeilen aus dem Bericht einzeln nachgelesen, Zeilennummer und Argumenttypen stimmen. |
| nil-Faelle | Kein Square im Menue: Ruecksprung. Kein Gegenstand zurueck: Zeile. `getWorldItem` hinter Riegel. Leere Nachbarkacheln: Riegel. Spielstand: die Drehung speichert `InventoryItem.save` (Offset 1282-1322), den Aufraeum-Riegel `IsoWorldInventoryObject.save` (Offset 109), beide werden wieder geladen. |
| Menue | `Events.Add` genau einmal auf Dateiebene, ein Aufruf je Rechtsklick. |
| Entfernen | Nur bei `getFullType() == "NCBear.BearStatic"`, erst sammeln, dann handeln, gleiche fuenf Aufrufe wie `ISGrabItemAction.lua:129-134`. |
| Je Bild | Nichts, kein OnTick, kein OnPlayerUpdate. |
| Beide Modi | Einzelspieler: `isSingleplayer()` wahr, volles Untermenue, das ist der Zweig fuer den Test. Mehrspieler-Client: Eintrag grau mit Hinweis, `NCBear_Spawn()` druckt dasselbe. Dedizierter Server: `client/` laedt dort nicht. Im Mehrspieler spawnt absichtlich nichts. |
| mod.info | An beiden Orten, gleiche Felder wie beim Turret, kein `require`. Leeres `common/media` wie beim Turret. |
| Abgrenzung | `git status` im NPCCrew-Repo leer, keine Treffer auf NCBear unter `42`, `common`, `mod.info`. |

## Sieht es nach Baer aus?

Ja. Aus allen acht Drehrichtungen und auch in echter Spielgroesse (1 m = 74 Pixel) sofort als Braunbaer zu lesen, gerendert aus dem fertigen FBX und PNG mit der Lichtformel des Spiels (`vorschau_acht_richtungen.png`, `vorschau_kopf_ruecken.png`). Keine Loecher, keine fremden Flecken, beide Kopfseiten sauber.

Schwaechen, ehrlich:

* Die Augen sind schmale Schlitze, er wirkt schlaefrig bis finster.
* Das Gesicht ist hell und glatt gegen die dunklen Beine, von nah etwas wie Pluesch.
* Von hinten ist er ein Klumpen mit Hosenbeinen.
* Die Rueckenlinie ist in der Schraegansicht wellig.

Fuer ein erstes Ansehen reicht das. Bei Spielgroesse faellt davon nur der Klumpen von hinten auf.

## Offen, bis Kevin es sieht

1. Helligkeit: gerechnet, nicht gesehen. `vorschau_wie_spiel.png` ist ohne Kachellicht. Das Turret hatte mittlere Texturfarbe 31 und war etwas dunkel, der Baer hat 100.
2. Verdecken an Waenden und Nachbarkacheln: das Turret lag frei, sonst ungeprueft.
3. Groesse: eine Zahl in `nc_bear.txt`, Neustart noetig.
4. Der Menueweg `OnFillWorldObjectContextMenu` ist in dieser Mod neu, das Turret hatte keine Lua. Vanilla und NPC Crew benutzen ihn taeglich.
5. Links und rechts gespiegelt oder nicht ist ungeprueft und beim Baeren ohne Belang.
