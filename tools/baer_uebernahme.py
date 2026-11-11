# -*- coding: utf-8 -*-
"""baer_uebernahme.py -- den Baeren (heute B1a: Junges finden und zaehmen; B1b: Folgen/Bleiben, Namensschild, Umbenennen, Futter
hinhalten, Waisen raeumen; B1c: Register-Selbstheilung, Laerm- und Zombie-Wache, Mitfahren, Call to me, Gehen, Bildschirm-Markierung,
Karten-Symbol, Anzeige-Optionen; B1d: Wachsen in BearGrowDays Spieltagen, taeglich steigende Werte, Faehigkeiten als Daten, Leben am
Tier, Werte-Zeilen ueber dem Baeren) aus der Test-Mod NCBearTest nach NPC Crew uebernehmen.

Grundregel (Werkstatt-CLAUDE.md Abschnitt 0, Kevin 08.11.2026): alles wird FUER NPC Crew gebaut und soll am Ende "einfach copy paste"
hinueber; keine Cheat- oder Testmenues kommen mit. Plan: _arbeit/baer_zaehmen/PLAN_ZAEHMEN.md Abschnitt 12 (B1b: PLAN_B1B.md 7),
Naehte: baer/NAEHTE.md.
Vorbild (gelesen, nicht blind kopiert): turret/tools/turret_uebernahme.py.

Aufruf (aus C:/Users/Kevin/NPCCrew-Nebenprojekte):
  python baer/tools/baer_uebernahme.py                     Trockenlauf: liest alles, schreibt NICHTS, sagt, was passieren wuerde.
  python baer/tools/baer_uebernahme.py --probe <ordner>    baut <ordner>/quelle (Kopie der Test-Mod ohne .git, darueber --staging, falls
                                                           angegeben) und <ordner>/NPCCrew (Kopie der noetigen Teile von NPC Crew), spielt
                                                           die Uebernahme dort echt durch, danach die vier Lua-Pruefer.
  python baer/tools/baer_uebernahme.py --echt --ja-kevin-hat-es-gesagt
                                                           schreibt in NPC Crew. NUR auf Kevins Wort, nie waehrend das Spiel laeuft.
  Zusatz: --staging <ordner>  Staging ueber die Test-Mod legen (Trockenlauf: nur gedanklich, Probe: in <probe>/quelle kopiert);
                              Form wie _arbeit/baer_zaehmen/mod (spiegelt die Wurzel der Test-Mod). Mit --echt verboten.
          --vor-b5a           Altlasten (die alten, noch nicht umbenannten NCBear*-Dateien und die Art "bear") nur als Warnung.
                              Nur Trockenlauf/Probe; mit --echt verboten: bis B5a ist die echte Uebernahme deshalb immer rot.
          --erneut            eine Datei aus einer frueheren Uebernahme darf ueberschrieben werden (sonst ist jede vorhandene Kollision).

Was es tut (erst wenn ALLES geprueft ist, wird geschrieben; sonst Abbruch ohne Schreiben):
  1. Einordnen: Lua (42|common)/media/lua/(shared|client|server)/(ISUI/|TimedActions/)?BanditsNPCBear*.lua kopieren; jede Datei mit
     Basisnamen NCBearBench* (jede Endung, jeder Ordner) NICHT (Testhilfe); mod.info, .git, .gitattributes, .gitignore nie;
     Translate/<L>/*.json zusammenfuehren; sandbox-options.txt anhaengen (Naht); Modell/Textur/Skript des Jungen (NCBearCub*,
     nc_bear_cub*) und den Animations-Knoten 42/media/AnimSets/buck/idle/NCBear_Eat.xml kopieren (die 9 Knoten des Erwachsenen
     bleiben bis B5a in der Test-Mod). B1c: Bilder 42/media/ui/BanditsNPCBear*.png kopieren (Kevins Symbol fuer Markierung und Karte;
     PNG-Kopf geprueft, Name gegen NPC Crew, Vanilla und Bandits). Die ALTEN Dateien (NCBear*.lua
     ausser Bench, Modelle/Texturen/Skripte/Toene des Erwachsenen und des Test-Gegenstands, die drei Test-Tiernamen in EN/IG_UI.json)
     sind "noch umzubenennen (B5a)": Fehler, mit --vor-b5a Warnung, werden nie kopiert. Erwartet sind genau die in ALT_EXPECTED
     (NAEHTE.md 'Erlaubte Fundstellen des Trockenlaufs'); eine neue Altlast ist immer ein Fehler. Alles andere: Fehler.
  2. Form: Lua LF, reines ASCII, keine Zeile endet mit Backslash; JSON der Quelle UTF-8 ohne BOM, Round-Trip
     json.dumps(indent=4, ensure_ascii=False)+"\\n"; Animations-Knoten wohlgeformt, genau eine Bedingung NCBearAct (STRING) -- sonst
     spielte der Knoten fuer jedes Tier mit Animset buck, auch Vanillas Hirsche --, jeder Clip im GLB des Jungen; Clip-Namen der
     GLB-Datei gegen Vanillas buck-Animset (fehlende nur Warnung, der gespielte Erwachsene hat dieselben 15).
  3. Texte: neue Schluessel sortiert einfuegen, nie die ganze Datei neu sortieren; NPC Crews Datei muss den Round-Trip bestehen;
     Paritaet ueber sieben Sprachen; CN nur Zeichen, die Vanilla-CN benutzt; EN 'singleplayer'/'multiplayer' zusammen; %1/%2 gleich
     in allen Sprachen; Namensraum je Datei (UI_BN_Bear_*, Sandbox_BanditsNPC_Bear*, die drei Tiernamen); IG_UI.json hat NPC Crew
     nicht: wird sortiert neu angelegt (bzw. zusammengefuehrt, falls es sie inzwischen gibt); gleicher Schluessel mit gleichem Wert
     (Sandbox_BanditsNPC = "NPC Crew") ist kein Fehler. B1b: kein '<' oder '>' in einem UI.json-Text (Tooltips sind Rich-Text).
  4. Sandbox (Naht 4): die option BanditsNPC.Bear*-Bloecke an NPC Crews 42/media/sandbox-options.txt anhaengen (Zeilenenden der
     Zieldatei, nur C-Kommentare, VERSION nicht doppelt); Abbruch bei vorhandenem Namen; je Option page, translation, Grenzen gegen
     B.OPTS in shared/BanditsNPCBear.lua und die Texte in Sandbox.json.
  5. Kollisionen gegen NPC Crew und Vanilla: eigene Namen (OWN_NAME_RES) im Code von NPC Crew (Kommentar = Warnung), Dateien im
     eigenen Namensraum, gleiche Dateinamen in models_X/textures/scripts/AnimSets (NPC Crew UND Vanilla: gleicher Pfad verdeckte
     Vanillas Datei), Modell-/Skriptnamen in Vanilla-Skripten, BanditsNPC.Bear als Funktion UND Tabelle (v3.8.38), Texte aus der Lua
     fehlen in EN, englische Ersatztexte (U.EN) wortgleich mit EN/UI.json, mesh/Textur des Jungen liegt auf der Platte.
  6. Cheat-Pruefung (Kevin 08.11.2026, fest): kein Testbefehl (NC<Name>_*), keine Testhilfe/Bank/Cheat, kein 'debug' im Code, kein
     Admin-Recht, keine Taste/Maus, kein Engine-Cheat, kein _G, keine globale Funktion/Zuweisung (ausser BanditsNPC = ..., den drei
     Aktionsklassen = ISBaseTimedAction:derive(...) und AnimalDefinitions = AnimalDefinitions or {}), kein Gegenstand aus dem Nichts,
     kein fester Menuetext, kein Fingerabdruck der Werkbank (Texte, Funktionsnamen der NCBearBench*-Dateien). Tier-Regel (Plan 12.1
     Punkt 7): addAnimal( und :addToWorld( nur in B.CreateCub, B.CreateCub( nur aus B.AppearFor, B.AppearFor( nur aus forestRolls und
     baitAppear in server/BanditsNPCBearServer.lua, :remove() am Tier nur in B.RemoveCub. B1b: kein B.ScanAnimals(..., force) im
     kopierten Code (Waisen ohne Alters-Frist entfernen kann nur die Werkbank). B1c (PLAN_B1C.md 10): B.CreateCub( auch aus B.PlaceCub
     (server/BanditsNPCBearRide.lua: Aussteigen, Call to me); setVariable("animalRunning" und :pathToLocation( (Kevins Wort je Methode)
     nur in B.MoveTo (server/BanditsNPCBearWorld.lua) -- seit der Nachbesserung B1c A4 zaehlt JEDES Vorkommen der beiden Namen im
     Code-Teil (auch als String, ueber einen Namen oder ein Tabellenfeld); animalRunning darf zusaetzlich in der Laerm-Wache gelesen
     werden (calmTickBody); B._callAt (Abklingzeit von Call to me) nur in server/BanditsNPCBearRide.lua -- zuruecksetzen kann nur die
     Werkbank; die Seite unter Optionen -> Mods (PZAPI.ModOptions) nennt nur Textschluessel (kein anderes Literal, keine Verkettung,
     kein getText(...) als Argument: mo_text_hits).
     B1d (PLAN_B1D.md 10): Groesse am Tier (setSizeForced, getData) nur in B.ApplySize (shared/BanditsNPCBearStats.lua), Leben am Tier
     (setHealth, getHealth) nur in B.BodyHp (server/BanditsNPCBearGrow.lua) -- jedes Vorkommen des Namens im Code-Teil; die
     Probe-Wege B.GrowSetG / B.GrowSetHp / B.SkillSet (Vorspulen, Leben und Erfahrung setzen) ruft im kopierten Code NIEMAND (nur die
     Definition; aufrufen darf sie nur die Werkbank, spaeter ein Baeren-Fenster mit eigener begruendeter Ausnahme). Die neuen Dateien
     deckt LUA_BEAR, die fuenf neuen Optionen (zwei als double) plan_sandbox (Text der Zahlen gegen B.OPTS).
     Ausnahmen nur einzeln mit Grund (CHEAT_ALLOWED).
  7. (Probe/echt) schreiben, zuruecklesen, dann luacheck.py, scopecheck.py, localcount.py je kopierter Lua-Datei und luacheck_pz.py
     (W113 nur die einzeln erlaubten: die drei Aktionsklassen, die eine andere kopierte Datei setzt).

Statisch geprueft, nicht gespielt. Das Skript startet kein Spiel und keinen Server, schreibt nie in die Test-Mod, nie in Vanilla/Bandits,
committet nichts.
"""
import collections
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
NC_LIVE = os.path.normpath(r"C:/Users/Kevin/Zomboid/mods/NPCCrew")
TOOLS = os.path.join(NC_LIVE, "_docs", "tools")                     # Pruefwerkzeuge von NPC Crew (nur aufrufen)
ZOMBOID = os.path.normpath(os.path.join(NC_LIVE, "..", ".."))        # C:/Users/Kevin/Zomboid
TEST = os.path.join(ZOMBOID, "mods", "NCBearTest")
NAEHTE = os.path.normpath(os.path.join(HERE, "..", "NAEHTE.md"))
VANILLA_MEDIA = r"C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media"
VANILLA_CN = os.path.join(VANILLA_MEDIA, "lua", "shared", "Translate", "CN")
VANILLA_EN = os.path.join(VANILLA_MEDIA, "lua", "shared", "Translate", "EN")
VANILLA_BUCK = os.path.join(VANILLA_MEDIA, "AnimSets", "buck")
LUAC = r"C:/Users/Kevin/Tools/lua51/luac5.1.exe"
LANGS = ["EN", "PTBR", "RU", "KO", "ES", "CN", "FR"]
PROBE_MARK = ".baer_probe"

# ---------------------------------------------------------------------------------------------------------------------------------
# Namen (Plan 12.1 Punkt 4). Alles davon in NPC Crew (ausser erlaubten Fundstellen) ist eine Kollision.
# UI_BN_Bear_ MIT Unterstrich (UI_BN_Beard_None ist NPC Crews), tcBear mit Wortgrenze (nicht tcBeardColor).
# ---------------------------------------------------------------------------------------------------------------------------------
OWN_NAME_RES = [r"BanditsNPC\.Bear\b", r"BanditsNPCBear", r"TrueCompanionsBears", r"TC-BEAR", r"UI_BN_Bear_", r"\btcBear\b",
                r"ncbear", r"NCBear", r"nc_bear"]
LUA_BEAR = re.compile(r"^(42|common)/media/lua/(shared|client|server)/(ISUI/|TimedActions/)?BanditsNPCBear[A-Za-z0-9_]*\.lua$")
BENCH_ANY = re.compile(r"^NCBearBench", re.I)                    # jede Testhilfe, gleich welche Endung und welcher Ordner
TRANSLATE = re.compile(r"^42/media/lua/shared/Translate/([A-Za-z]+)/([^/]+\.json)$")
SANDBOX = "42/media/sandbox-options.txt"
# Neue Teile des Jungen (B1a) und der EINE Animations-Knoten, den das Junge braucht (NCBear_Eat, Plan 12.1 P. 10). Die uebrigen
# Knoten des Erwachsenen (Bite, Maul, Slam, Swipe ...) bleiben bis B5a in der Test-Mod (Nachbesserung A10): nie Kampf-Knoten vor
# dem Kampf nach NPC Crew, und was B5a umbenennt, muesste dort sonst geloescht werden.
CUB_ASSET = re.compile(r"^42/media/(models_X/Skinned/NCBearCub\.glb|textures/Body/NCBearCub\.png|scripts/nc_bear_cub\.txt)$")
# B1c (PLAN_B1C.md 10c): Bilder der Oberflaeche (Kevins Baeren-Symbol fuer Bildschirm-Markierung und Karte), nur im eigenen Namensraum
UI_ASSET = re.compile(r"^42/media/ui/BanditsNPCBear[A-Za-z0-9_]*\.png$")
UI_MAX_PX = 512                                                    # Deckel fuer ein Oberflaechen-Bild (Kevins Symbol: 96 x 96)
BANDITS_MEDIA = [os.path.normpath(r"C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3268487204/mods/Bandits/" + v
                                  + "/media") for v in ("42.22", "common")]   # nur lesen: gleicher ui-Dateiname verdeckte Bandits' Bild
ANIMSET_OK = re.compile(r"^42/media/AnimSets/buck/idle/NCBear_Eat\.xml$")
ANIMSET_ADULT = re.compile(r"^42/media/AnimSets/buck/idle/NCBear_[A-Za-z0-9]+\.xml$")
ANIMSET_ANY = re.compile(r"^(42|common)/media/AnimSets/")
CUB_GLB = "42/media/models_X/Skinned/NCBearCub.glb"
GIT_ROOT_FILES = (".git", ".gitattributes", ".gitignore")
ANIM_VAR = "NCBearAct"                                             # B.ACT

# Namensraum der Texte je Datei.
TEXT_NS = {
    "UI.json": (re.compile(r"^UI_BN_Bear_[A-Za-z0-9_]+$"), set()),
    "Sandbox.json": (re.compile(r"^Sandbox_BanditsNPC_Bear[A-Za-z0-9_]+$"), {"Sandbox_BanditsNPC"}),
    "IG_UI.json": (re.compile(r"^$"), {"IGUI_AnimalType_ncbearcub", "IGUI_Animal_Group_ncbear", "IGUI_Breed_brown"}),
}

# ---------------------------------------------------------------------------------------------------------------------------------
# Altlasten bis B5a (Plan 12.1 Punkt 8; Kevin: Umbenennen zu Beginn von B5a). "Erlaubte Fundstellen des Trockenlaufs" (NAEHTE.md):
# genau diese machen den Trockenlauf ohne --vor-b5a absichtlich rot. Je Eintrag Pfad (bzw. "text:<datei>:<schluessel>") und Grund.
# ---------------------------------------------------------------------------------------------------------------------------------
ALT_EXPECTED = collections.OrderedDict([
    ("42/media/lua/shared/NCBearDefs.lua", "Art 'bear' des Erwachsenen (Altname, B5a: Umbenennen in BanditsNPCBear*, Art/Gruppe entscheiden)"),
    ("42/media/lua/shared/NCBearFight.lua", "Kampf des Erwachsenen im SP (Altname; Kampf ist B5a)"),
    ("42/media/lua/client/NCBearAttackProbe.lua", "Angriffs-Sonde (Testwerkzeug: B5a streicht oder schiebt nach NCBearBench*)"),
    ("42/media/lua/client/NCBearSize.lua", "Groessen-Testhilfe (B5a: nach NCBearBench* oder streichen)"),
    ("42/media/lua/client/NCBearSpawn.lua", "Spawn-Testhilfe des Erwachsenen (B5a: nach NCBearBench*)"),
    ("42/media/lua/client/NCBearTest.lua", "Testbefehle NCBear_Sit/Stand/Eat (B5a: nach NCBearBench*)"),
    ("42/media/models_X/Skinned/NCBear.glb", "Modell des Erwachsenen (geht mit der Art 'bear', B5a)"),
    ("42/media/models_X/Skinned/NCBearDeer.glb", "Test-Modell 'bearstag' mit Hirsch-Bewegung (B5a: streichen)"),
    ("42/media/models_X/WorldItems/NCBear.fbx", "Test-Gegenstand 'Test Bear (model)' (B5a: streichen)"),
    ("42/media/textures/Body/NCBear.png", "Textur des Erwachsenen (B5a)"),
    ("42/media/textures/Item_NCBear.png", "Icon des Test-Gegenstands (B5a: streichen)"),
    ("42/media/textures/WorldItems/NCBear.png", "Textur des Test-Gegenstands (B5a: streichen)"),
    ("42/media/scripts/nc_bear.txt", "module NCBear mit Test-Gegenstand BearStatic, DisplayName 'Test Bear (model)' (B5a: streichen)"),
    ("42/media/scripts/nc_bear_tier.txt", "Modelle NCBear_Body und NCBearStag_Body des Erwachsenen (B5a)"),
    ("42/media/scripts/nc_bear_sounds.txt", "Toene des Erwachsenen (B5a, mit dem Kampf)"),
    ("42/media/sound/NCBear_Growl1.wav", "Ton des Erwachsenen (B5a)"),
    ("42/media/sound/NCBear_Growl2.wav", "Ton des Erwachsenen (B5a)"),
    ("42/media/sound/NCBear_Growl3.wav", "Ton des Erwachsenen (B5a)"),
    ("42/media/sound/NCBear_Huff.wav", "Ton des Erwachsenen (B5a)"),
    ("42/media/sound/NCBear_Pain.wav", "Ton des Erwachsenen (B5a)"),
    ("42/media/sound/NCBear_Roar.wav", "Ton des Erwachsenen (B5a)"),
    ("text:IG_UI.json:IGUI_AnimalType_bear", "Tiername der Test-Art 'bear' ('Brown bear (test)', B5a)"),
    ("text:IG_UI.json:IGUI_AnimalType_bearstag", "Tiername der Test-Art 'bearstag' (B5a: streichen)"),
    ("text:IG_UI.json:IGUI_Animal_Group_bear", "Gruppenname der Test-Gruppe 'bear' ('Bear (NC test)', B5a)"),
])
OLD_ASSET = re.compile(r"^(NCBear|nc_bear|Item_NCBear)", re.I)
OLD_TEXT_KEYS = {"IG_UI.json": {"IGUI_AnimalType_bear", "IGUI_AnimalType_bearstag", "IGUI_Animal_Group_bear"}}

# Erlaubte Fundstellen in NPC Crew (NPC Crew nennt den Baeren SELBST im Code). Heute keine: der Baer beruehrt NPC Crew nur zur Laufzeit
# (NAEHTE.md). NPC Crew nennt 'NCBear' heute nur in einem Changelog-KOMMENTAR (shared/BanditsNPC.lua, v3.14.58): Warnung, keine Kollision.
NC_ALLOWED = []

# ---------------------------------------------------------------------------------------------------------------------------------
# Cheat-Pruefung (Kevin 08.11.2026: "achte darauf das keine cheat menues davon rueber kommen am ende"). Geprueft wird der CODE-Teil jeder
# kopierten Lua-Zeile (Strings zaehlen zum Code, Kommentare nicht). (Kennung, Muster, Grund)
# ---------------------------------------------------------------------------------------------------------------------------------
CHEAT_RULES = [
    ("befehl", r"\bNC[A-Z][A-Za-z]*_[A-Za-z]\w*", "Testbefehl der Werkbank (NCBear_*, NCTurret_* ...)"),
    ("testhilfe", r"(?i)\w*(bench|cheat|godmode|testmod[eu]s?|testhilfe|testmenue?)\w*", "Bank-, Test- oder Cheat-Name"),
    ("bank", r"(?i)\bbank\b", "Bank-Modus (gehoert in NCBearBench*)"),
    ("debug", r"\bisDebugEnabled\b|\bgetDebug\s*\(|\bgetDebugOptions\b|\bDebugOptions\b|\baddDebugOption\b|\bDebugContextMenu\b"
              r"|\bISDebugMenu\b|(?i:debug)", "Debug-Schalter, Debug-Menue oder 'debug' im Code"),
    ("admin", r"\bCapability\.\w+|\bisAdmin\b|\bgetAccessLevel\b|\bIsStaff\b|\bhasAdminPower\b|\bhasAdminTool\b"
              r"|:getRole\s*\(\s*\)\s*:\s*getName\s*\(|\bisCoopHost\b|(?i:[\"']admin)", "Admin-/Staff-Recht (ein Admin-Weg ist ein Spawn-Weg)"),
    ("taste", r"\bEvents\.(OnKeyPressed|OnKeyStartPressed|OnKeyKeepPressed|OnCustomUIKey\w*|OnContextKey|OnMouseDown|OnMouseUp"
              r"|OnRightMouseDown|OnRightMouseUp|OnMouseWheel|OnObject(?:Left|Right)MouseButton(?:Down|Up)|OnJoypad\w*|OnGamepad\w*"
              r"|OnPressReloadButton|OnPressRackButton)\b|\bisKeyDown\s*\(|\bisKeyPressed\s*\(|\bGameKeyboard\.|\bKeyboard\.KEY_\w+",
     "Taste oder Maus abgefragt (Debug-Taste? Die V-Taste kommt erst mit dem Baeren-Fenster und dann ueber NAEHTE.md)"),
    ("engine", r"\b(setGodMod|setGhostMode|setInvisible|setInvincible|setIsInvincible|setNoClip|setUnlimitedCarry|setUnlimitedEndurance"
               r"|setUnlimitedAmmo|setBuildCheat|setFarmingCheat|setHealthCheat|setMechanicsCheat|setMovablesCheat"
               r"|setTimedActionInstantCheat|setFastMoveCheat|setCanSeeAll|setCanHearAll|setZombiesDontAttack|setKnowAllRecipes"
               r"|setSeeNonPvpZone|setCanUseBrushTool|setDebug\w*|addAcceptance|setWild)\b", "Cheat-Aufruf der Engine (Plan 0.8: nicht benutzt)"),
    ("_G", r"(?<!rawget\()\b_G\b", "Zugriff auf _G (Konsolenbefehl?)"),
    ("erzeugen", r"\binstanceItem\s*\(|\bInventoryItemFactory\.CreateItem\s*\(|:AddItems?\s*\(|\bsendAddItemToContainer\s*\(",
     "Gegenstand erzeugen (aus dem Nichts = Spawn; jede Stelle einzeln mit Grund freigeben)"),
    ("bankspur", r"\[NCBear\]|(?i:[\"'][^\"'\n]*\busage:)", "Fingerabdruck der Werkbank (Praefix [NCBear] oder 'usage:'-Hilfe)"),
    ("altmenue", r"\bNCBearMenu\b|\bNCBearBench\w*", "Haken ins alte Testmenue der Test-Mod (NCBearMenu.extra) oder in die Testhilfe"),
    # B1b (PLAN_B1B.md 4.3): B.ScanAnimals(players, force) -- force ueberspringt die Alters-Frist der Waisen (Riegel 3). Nur die Werkbank
    # (NCBear_CubSweep) darf das. Seit der Nachbesserung B1b A5 keine Zeilen-Regex mehr, sondern scan_force_hits (zerlegt die Klammer).
]
SCAN_NAME = re.compile(r"\bScanAnimals\b")
SCAN_DEF = re.compile(r"\bfunction\s+(?:[\w.]+[.:])?ScanAnimals\s*\(")
SCAN_WHY = "Waisen-Suchlauf mit force (ohne Alters-Frist) gibt es nur in der Werkbank"


def scan_force_hits(code_text):
    """Nachbesserung B1b A5: jede Erwaehnung von ScanAnimals im Code-Teil einer Datei (Zeilen mit "\\n" verbunden, Kommentare schon
    weg, Strings noch da). Erlaubt sind nur die Definition und Aufrufe mit hoechstens EINEM Argument auf oberster Ebene (mit
    ':' zaehlt das versteckte self mit). Fund: ein zweites Argument in jeder Form (true, not false, 1 == 1, B.Players(), ...), ein
    Aufruf ueber mehrere Zeilen eingeschlossen, und ScanAnimals ohne folgende Klammer (Zuweisung an einen Namen, Tabellenfeld,
    Text "ScanAnimals"). Rueckgabe: Liste (Zeichen-Offset, Kurztext)."""
    defs = set()
    for d in SCAN_DEF.finditer(code_text):
        defs.add(d.start() + d.group(0).index("ScanAnimals"))
    hits = []
    for m in SCAN_NAME.finditer(code_text):
        if m.start() in defs:
            continue
        j = m.end()
        while j < len(code_text) and code_text[j] in " \t\r\n":
            j += 1
        if j >= len(code_text) or code_text[j] != "(":
            hits.append((m.start(), "ScanAnimals ohne Aufruf-Klammer (an einen Namen gebunden?)"))
            continue
        k = m.start() - 1
        while k >= 0 and code_text[k] in " \t":
            k -= 1
        args = call_args(code_text, j + 1)
        n = len(args)
        if n == 1 and not args[0].strip():
            n = 0
        if k >= 0 and code_text[k] == ":":
            n += 1
        if n > 1:
            hits.append((m.start(), "Aufruf mit %d Argumenten" % n))
    return hits
CHEAT_GLOBAL_FN = re.compile(r"(?<![\w.:])function\s+([A-Za-z_]\w*)\s*\(")
CHEAT_GLOBAL_SET = re.compile(r"^([A-Za-z_]\w*)\s*=(?!=)")
CHEAT_STRING = re.compile(r"(?i)(?<!de)spawn|debug")
CHEAT_NAME = re.compile(r"(?i:bench|cheat|debug|spawn)|Dbg|Test|TEST|(?<![A-Za-z])test")
CHEAT_FILE_REST = re.compile(r"(?i:dev|tools|admin|console|tweak|tune)(?![a-z])")
CHEAT_TEXT = re.compile(r"(?i)\b(bench|cheat|debug|spawn|test)")
XML_CHEAT = re.compile(r"(?i)bench|cheat|debug|test|NCBear_Cub")
LUA_STRING = re.compile(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'')
LONG_STRING = re.compile(r"\[(=*)\[(.*?)\]\1\]", re.S)
BTN_CALL = re.compile(r"\bISButton\s*:\s*new\s*\(|[:.]addSlice\s*\(")
MENU_CALL = re.compile(r"[:.](addOption|addOptionOnTop|addGetUpOption|addColorBoxOption|addActionsOption|insertOptionAfter"
                       r"|insertOptionBefore)\s*\(")
_TS = r'"(?:[^"\\\n]|\\.)*"|' + r"'(?:[^'\\\n]|\\.)*'"
_TL0 = r"(?:%s|[^()\"'])*" % _TS
_TL1 = r"(?:%s|[^()\"']|\(%s\))*" % (_TS, _TL0)
_TL2 = r"(?:%s|[^()\"']|\(%s\))*" % (_TS, _TL1)
TEXT_CALL = re.compile(r"\b(?:getText|getTextOrNull)\s*\(%s\)|\b[\w.:]+\s*\(\s*([\"'])UI_[^\"']*\1%s\)" % (_TL2, _TL2))
FN_HEAD = re.compile(r"^(?:local\s+)?function\s+([\w.:]+)\s*\(|^(?:local\s+)?([\w.:]+)\s*=\s*function\b")
# Erlaubte Globale (Plan 12.1 Punkt 6): Aktionsklassen sind in Vanilla und NPC Crew global (die Engine baut Netz-Aktionen ueber den Namen).
GLOBAL_OK = {"BanditsNPC"}
GLOBAL_SAME = {"AnimalDefinitions"}                                # nur die Form "X = X or {}" (Vanillas Tabelle, DeerDefinitions.lua:1)
# Tier-Regel (Plan 12.1 Punkt 7): Muster -> erlaubte (Datei, Funktion). Die Definition selbst zaehlt nicht.
TIER_RULES = [
    ("addAnimal", re.compile(r"(?<![\w.:])addAnimal\s*\("), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.CreateCub")},
     "Tier erzeugen nur in B.CreateCub"),
    ("addToWorld", re.compile(r":addToWorld\s*\("), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.CreateCub")},
     "Tier in die Welt setzen nur in B.CreateCub"),
    ("CreateCub", re.compile(r"\bB\.CreateCub\s*\("), {("42/media/lua/server/BanditsNPCBearServer.lua", "B.AppearFor"),
                                                         ("42/media/lua/server/BanditsNPCBearRide.lua", "B.PlaceCub")},
     "B.CreateCub nur aus B.AppearFor und (B1c) B.PlaceCub (Aussteigen, Call to me)"),
    ("AppearFor", re.compile(r"\bB\.AppearFor\s*\("), {("42/media/lua/server/BanditsNPCBearServer.lua", "forestRolls"),
                                                         ("42/media/lua/server/BanditsNPCBearServer.lua", "baitAppear")},
     "B.AppearFor (der EINE Weg, ein Junges in die Welt zu setzen) nur aus Wald-Wurf und Koeder"),
    ("remove", re.compile(r":remove\s*\(\s*\)"), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.RemoveCub")},
     "Tier entfernen nur in B.RemoveCub"),
    ("removeAnimal", re.compile(r"(?<![\w.:])removeAnimal\s*\("), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.RemoveCub")},
     "Tier bei den Clients entfernen (Server) nur in B.RemoveCub"),
    # B1c (PLAN_B1C.md 10b): die zwei Engine-Aufrufe mit Kevins Wort (pathToLocation 08.11.2026, setVariable("animalRunning", false)
    # 11.11.2026) an genau EINER Stelle. Nachbesserung B1c A4: nicht mehr nur die Aufruf-Form, sondern JEDES Vorkommen des Namens im
    # Code-Teil (Strings zaehlen mit, Gross/Klein egal) -- so fallen auch local V = "animalRunning"; a.setVariable(a, V, false),
    # a["setVariable"](...), a.pathToLocation(a, ...), a["pathToLocation"](...) und local f = a.pathToLocation auf. Zweite erlaubte
    # Stelle fuer den Namen animalRunning: das LESEN in der Laerm-Wache (getVariableBoolean, calmTickBody, nur Einzelspieler).
    ("animalRunning", re.compile(r"(?i)\banimalRunning\b"),
     {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.MoveTo"), ("42/media/lua/server/BanditsNPCBearGuard.lua", "calmTickBody")},
     "Name animalRunning (Gehen setzen nur in B.MoveTo, lesen nur in der Laerm-Wache)"),
    ("pathToLocation", re.compile(r"(?i)\bpathToLocation\b"), {("42/media/lua/server/BanditsNPCBearWorld.lua", "B.MoveTo")},
     "pathToLocation (jede Form) nur in B.MoveTo"),
    # B1c: die Abklingzeit von "Call to me" lebt nur in Ride.lua (Dateiebene, B.CallLeft, callMark); sie zuruecksetzen kann nur die
    # Werkbank (NCBear_CubCallReset)
    ("callAt", re.compile(r"\bB\._callAt\b"), {("42/media/lua/server/BanditsNPCBearRide.lua", None),
                                              ("42/media/lua/server/BanditsNPCBearRide.lua", "B.CallLeft"),
                                              ("42/media/lua/server/BanditsNPCBearRide.lua", "callMark")},
     "Abklingzeit von Call to me (B._callAt) nur in server/BanditsNPCBearRide.lua"),
    # B1d (PLAN_B1D.md 10, 7.1 Nr. 18): Groesse und Leben am Tier je an EINER Stelle -- jedes Vorkommen des Namens im Code-Teil (auch als
    # String oder Tabellenfeld), wie die B1c-Regeln animalRunning/pathToLocation. Belege der Aufrufe stehen dort im Kommentar
    # (setSizeForced: Vanilla ButcheringUtil.lua:569/:571/:586; getHealth: ISAnimalUI.lua:15; setHealth: ISAnimalContextMenu.lua:545).
    ("setSizeForced", re.compile(r"(?i)\bsetSizeForced\b"), {("42/media/lua/shared/BanditsNPCBearStats.lua", "B.ApplySize")},
     "Groesse am Tier setzen (setSizeForced) nur in B.ApplySize"),
    ("getData", re.compile(r"\bgetData\b"), {("42/media/lua/shared/BanditsNPCBearStats.lua", "B.ApplySize")},
     "Datenteil des Tiers (getData) nur in B.ApplySize"),
    ("setHealth", re.compile(r"(?i)\bsetHealth\b"), {("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyHp")},
     "Leben am Tier setzen (setHealth) nur in B.BodyHp"),
    ("getHealth", re.compile(r"(?i)\bgetHealth\b"), {("42/media/lua/server/BanditsNPCBearGrow.lua", "B.BodyHp")},
     "Leben am Tier lesen (getHealth) nur in B.BodyHp"),
    # B1d: Vorspulen / Leben / Erfahrung von Hand setzen -- im kopierten Code gibt es keinen erlaubten Aufrufer (leere Menge); die
    # Definitionen zaehlen nicht (TIER_DEF). Ein Aufrufer waere ein Spieler-Weg ohne Spielmechanik (Cheat-Pfad).
    ("probeweg", re.compile(r"\bGrowSetG\b|\bGrowSetHp\b|\bSkillSet\b"), set(),
     "B.GrowSetG / B.GrowSetHp / B.SkillSet nur aus der Werkbank (im kopierten Code nur die Definition)"),
]
# B1c (PLAN_B1C.md 6.8): die Seite unter Optionen -> Mods bekommt nur Textschluessel (Vanilla ruft getText,
# client/OptionScreens/MainOptions.lua:2801-2812). Methode -> Stellen der Text-Argumente (0 = erstes Argument).
MO_CALL = re.compile(r"\bModOptions\s*:\s*create\s*\(|[:.](addTitle|addDescription|addTickBox|addSlider|addComboBox|addItem|addTextEntry"
                     r"|addButton|addKeyBind|addMultipleTickBox|addColorPicker)\s*\(")
MO_TEXT_ARGS = {None: (1,), "addTitle": (0,), "addDescription": (0,), "addTickBox": (1, 3), "addSlider": (1, 6), "addComboBox": (1, 2),
                "addItem": (0,), "addTextEntry": (1, 3), "addButton": (1, 2), "addKeyBind": (1, 3), "addMultipleTickBox": (1, 2),
                "addColorPicker": (1, 6)}
# (Vanilla client/PZAPI/ModOptions.lua :28-247; option:addTickBox(name, value) einer Mehrfach-Auswahl :96 hat den Text vorn -- mit
# hoechstens zwei Argumenten zaehlt deshalb das erste)
MO_KEY = re.compile(r"^UI_BN_Bear_[A-Za-z0-9_]+$")
MO_NAME = re.compile(r"^[A-Za-z_]\w*$")


def mo_text_hits(code_text):
    """Nachbesserung B1c A4: Text-Argumente der Optionen-Seite (PZAPI.ModOptions) im Code-Teil einer Datei (Zeilen mit "\\n"
    verbunden, Kommentare weg). Erlaubt: genau EIN String-Literal, das ein Schluessel UI_BN_Bear_* ist, oder ein blosser Name, hinter
    dem kein lokaler Satz steht (local x = "..."). Alles andere ist ein Fund: ein anderes Literal, ein Literal in einer Verkettung
    ("Text" .. x), ein Aufruf als Argument (getText(...), U.T(...) -- schon uebersetzt statt Schluessel), jeder andere Ausdruck.
    Rueckgabe: Liste (Zeilennummer, Kurztext, Grund)."""
    local_str = set(m.group(1) for m in re.finditer(r"\blocal\s+(\w+)\s*=\s*[\"'][^\"'\n]*[A-Za-z][^\"'\n]*[A-Za-z]", code_text))
    hits = []
    for m in MO_CALL.finditer(code_text):
        args = call_args(code_text, m.end())
        idx = MO_TEXT_ARGS.get(m.group(1), ())
        if m.group(1) == "addTickBox" and len(args) <= 2:
            idx = (0,)
        no = code_text.count("\n", 0, m.start()) + 1
        for i in idx:
            if i >= len(args):
                continue
            a = args[i].strip()
            if a in ("", "nil"):
                continue
            lit = re.match(r"^([\"'])([^\"'\n]*)\1$", a)
            if lit:
                if not MO_KEY.match(lit.group(2)):
                    hits.append((no, a[:40], "Optionen-Seite mit festem Text statt Textschluessel"))
            elif MO_NAME.match(a):
                if a in local_str:
                    hits.append((no, a[:40], "Optionen-Seite mit festem Text (lokaler Satz) statt Textschluessel"))
            else:
                hits.append((no, a[:40], "Optionen-Seite mit einem Ausdruck (Verkettung, Aufruf ...) statt eines Textschluessels"))
    return hits


TIER_DEF = re.compile(r"^function\s+B\.(CreateCub|AppearFor|RemoveCub|GrowSetG|GrowSetHp|SkillSet)\s*\(")   # B1d: + die drei Probe-Wege
# Ausnahmen einzeln mit Grund: Datei, Regel, ein Text im Code-Teil der Zeile. Greift eine nicht mehr, warnt das Skript.
CHEAT_ALLOWED = [
    {"file": "42/media/lua/shared/BanditsNPCBearDefs.lua", "rule": "befehl", "code": 'bodyModel = "NCBearCub_Body"',
     "why": "Name des model-Skripts (scripts/nc_bear_cub.txt), kein Befehl (Plan 12.1 Punkt 5)"},
]
# luacheck_pz W113, die eine ANDERE kopierte Datei setzt (luacheck_pz liest je Datei, nicht ueber Dateien): (Datei, Name).
PZ_ALLOWED = {
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearFeedAction"),
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearPetAction"),
    ("BanditsNPCBearMenu.lua", "BanditsNPCBearBaitAction"),
}

ARGS = {"erneut": False, "vor_b5a": False, "echt": False}


class Report:
    def __init__(self):
        self.errors, self.warns, self.lines = [], [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warns.append(msg)

    def say(self, msg=""):
        self.lines.append(msg)
        print(msg)


def rd(path):
    with open(path, "rb") as f:
        return f.read()


def rel_of(root, full):
    return os.path.relpath(full, root).replace(os.sep, "/")


def md5(data):
    return hashlib.md5(data).hexdigest()


_LONG_OPEN = re.compile(r"\[(=*)\[")


def lua_split_lines(text):
    """Je Zeile (Code, Kommentar). Kennt "..." und '...' mit Escapes, [[...]] und --[[...]] auch ueber Zeilen. Nur zum Pruefen.
    Was es nicht erkennt, zaehlt als Code (die strengere Seite). Form wie turret_uebernahme.py."""
    out = []
    state = None
    for raw in text.split("\n"):
        line = raw[:-1] if raw.endswith("\r") else raw
        code, com = [], []
        i, n = 0, len(line)
        while i < n:
            if state is not None:
                close = "]" + "=" * state[0] + "]"
                j = line.find(close, i)
                end = n if j < 0 else j + len(close)
                (com if state[1] else code).append(line[i:end])
                if j >= 0:
                    if state[1] and "".join(code).strip():
                        code.append(" ")
                    state = None
                i = end
                continue
            c = line[i]
            if c == "-" and line.startswith("--", i):
                m = _LONG_OPEN.match(line, i + 2)
                if m:
                    state = (len(m.group(1)), True)
                    com.append(line[i:m.end()])
                    i = m.end()
                    continue
                com.append(line[i:])
                break
            if c == "[":
                m = _LONG_OPEN.match(line, i)
                if m:
                    state = (len(m.group(1)), False)
                    code.append(line[i:m.end()])
                    i = m.end()
                    continue
            if c == '"' or c == "'":
                j = i + 1
                while j < n and line[j] != c:
                    j += 2 if line[j] == "\\" else 1
                code.append(line[i:j + 1])
                i = j + 1
                continue
            code.append(c)
            i += 1
        out.append(("".join(code), "".join(com)))
    return out


def eol_of(data, label, rep):
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    if crlf and lf:
        rep.err("%s: gemischte Zeilenenden (%d CRLF, %d LF) -- nicht anfassen, von Hand klaeren" % (label, crlf, lf))
    return b"\r\n" if crlf > lf else b"\n"


# ---------------------------------------------------------------------------------------------------------------------------------
# 0. Quelle: Test-Mod (ohne .git), wahlweise mit Staging darueber
# ---------------------------------------------------------------------------------------------------------------------------------
def source_map(base, staging, rep):
    """{rel: absoluter Pfad} und Liste der uebersprungenen Git-Teile. Staging gewinnt (gleicher Pfad)."""
    files, skipped = {}, []
    for root, tag in ((base, "test"), (staging, "staging")):
        if not root:
            continue
        if not os.path.isdir(root):
            rep.err("Quelle fehlt: %s" % root)
            continue
        for dirpath, dirs, fs in os.walk(root):
            if os.path.normcase(dirpath) == os.path.normcase(root) and ".git" in dirs:
                dirs.remove(".git")
                skipped.append((".git/", "Git-Sicherung der Test-Mod (Ordner), wird nicht kopiert"))
            for fn in fs:
                full = os.path.join(dirpath, fn)
                rel = rel_of(root, full)
                if tag == "staging" and rel in ("mod.info", "42/mod.info"):
                    rep.err("Staging enthaelt %s -- mod.info gehoert nicht ins Staging (Vorschlag als eigene Datei)" % rel)
                    continue
                files[rel] = full
    return files, skipped


# ---------------------------------------------------------------------------------------------------------------------------------
# 1. Einordnen
# ---------------------------------------------------------------------------------------------------------------------------------
def collect_source(src, rep):
    copy_lua, copy_asset, merge, skipped, alt, sandbox = [], [], [], [], [], None
    for rel in sorted(src):
        base = os.path.basename(rel)
        if rel in ("mod.info", "42/mod.info"):
            skipped.append((rel, "mod.info der Test-Mod"))
        elif rel in GIT_ROOT_FILES:
            skipped.append((rel, "Git-Sicherung der Test-Mod, wird nicht kopiert"))
        elif BENCH_ANY.match(base):
            skipped.append((rel, "Testhilfe NCBearBench*, wird nie kopiert"))
        elif TRANSLATE.match(rel):
            merge.append(rel)
        elif LUA_BEAR.match(rel):
            copy_lua.append(rel)
        elif rel == SANDBOX:
            sandbox = rel
        elif CUB_ASSET.match(rel) or ANIMSET_OK.match(rel) or UI_ASSET.match(rel):
            copy_asset.append(rel)
        elif ANIMSET_ADULT.match(rel):
            skipped.append((rel, "Animations-Knoten des Erwachsenen, bleibt bis B5a in der Test-Mod (NAEHTE.md Naht 9)"))
        elif rel.endswith(".lua") and re.match(r"BanditsNPCBear", base):
            rep.err("%s: Unterordner nicht freigegeben (bekannt: shared|client|server, darin ISUI/ oder TimedActions/)" % rel)
        elif rel in ALT_EXPECTED or (rel.endswith(".lua") and base.startswith("NCBear")) or (
                rel.startswith(("42/media/", "common/media/")) and OLD_ASSET.match(base)):
            alt.append(rel)
        elif ANIMSET_ANY.match(rel):
            rep.err("%s: Animations-Datei nur als 42/media/AnimSets/buck/idle/NCBear_*.xml" % rel)
        elif rel.endswith(".lua"):
            rep.err("%s: Lua-Datei ohne den Namen BanditsNPCBear* (Kopierregel a) -- umbenennen; Testhilfe nach NCBearBench*" % rel)
        else:
            rep.err("%s: Datei ohne Baeren-Namen -- wuerde eine NPC-Crew-Datei treffen koennen" % rel)
    return copy_lua, copy_asset, merge, skipped, alt, sandbox


def alt_report(alt, text_alt, rep):
    """Altlasten bis B5a melden. Ohne --vor-b5a Fehler (erwartet rot), mit Warnung; eine nicht erwartete ist immer ein Fehler."""
    rep.say("")
    rep.say("== Altlasten bis B5a (noch umzubenennen; Erlaubte Fundstellen des Trockenlaufs, NAEHTE.md)")
    found = list(alt) + list(text_alt)
    for item in found:
        why = ALT_EXPECTED.get(item)
        if why is None:
            rep.err("unbekannte Altlast %s -- nicht in ALT_EXPECTED: umbenennen (BanditsNPCBear*/NCBearCub*) oder nach NCBearBench*" % item)
            continue
        msg = "noch umzubenennen (B5a): %s -- %s" % (item, why)
        rep.say("  " + msg)
        if ARGS["vor_b5a"]:
            rep.warn(msg)
        else:
            rep.err(msg)
    for item in ALT_EXPECTED:
        if item not in found:
            rep.warn("Altlast %s ist weg (in B5a erledigt?) -- aus ALT_EXPECTED und NAEHTE.md streichen" % item)
    rep.say("  %d Altlasten (%s)" % (len(found), "--vor-b5a: nur Warnung" if ARGS["vor_b5a"] else "Fehler: Trockenlauf absichtlich rot"))
    return len(found)


# ---------------------------------------------------------------------------------------------------------------------------------
# 2. Form: Lua, Animations-Knoten, GLB
# ---------------------------------------------------------------------------------------------------------------------------------
def glb_json(data, label, rep):
    if len(data) < 20 or data[:4] != b"glTF":
        rep.err("%s: keine GLB-Datei (Kopf)" % label)
        return None
    _magic, ver, length = struct.unpack("<4sII", data[:12])
    clen, ctype = struct.unpack("<I4s", data[12:20])
    if ver != 2 or ctype != b"JSON" or length != len(data):
        rep.err("%s: GLB-Kopf unstimmig (Version %s, Laenge %s/%s)" % (label, ver, length, len(data)))
        return None
    try:
        return json.loads(data[20:20 + clen].decode("utf-8"))
    except ValueError as ex:
        rep.err("%s: GLB-JSON unlesbar (%s)" % (label, ex))
        return None


def vanilla_buck_clips():
    clips = set()
    for dp, _d, fs in os.walk(VANILLA_BUCK):
        for fn in fs:
            if fn.endswith(".xml"):
                try:
                    t = rd(os.path.join(dp, fn)).decode("utf-8", errors="ignore")
                except OSError:
                    continue
                clips.update(re.findall(r"<m_AnimName>\s*([^<\s]+)\s*</m_AnimName>", t))
    return clips


def form_check(final, copy_lua, copy_asset, rep):
    for rel in copy_lua:
        data = final[rel]
        if b"\r" in data:
            rep.err("%s: CR in einer neuen Datei (Regel: LF)" % rel)
        if any(c > 126 or (c < 32 and c not in (9, 10)) for c in data):
            rep.err("%s: nicht reines ASCII oder Steuerzeichen" % rel)
        if data.startswith(b"\xef\xbb\xbf"):
            rep.err("%s: BOM" % rel)
        if not data.endswith(b"\n"):
            rep.warn("%s: kein Zeilenende am Schluss" % rel)
        for no, ln in enumerate(data.split(b"\n"), 1):
            if ln.endswith(b"\\"):
                rep.err("%s:%d: Zeile endet mit Backslash (String ueber das Zeilenende)" % (rel, no))
        code = "\n".join(c for c, _ in lua_split_lines(data.decode("latin-1")))
        if re.search(r"(?<![\w.:])next\s*\(", code):
            rep.err("%s: next( -- Kahlua kennt kein next" % rel)
    # GLB des Jungen
    rep.say("")
    rep.say("== Modell und Animations-Knoten")
    glb = final.get(CUB_GLB)
    cub_clips = set()
    if glb is None:
        rep.err("%s fehlt in der Quelle (Platzhalter aus _arbeit/baer_baby/entwurf/ oder Modell aus baer-junges)" % CUB_GLB)
    else:
        j = glb_json(glb, CUB_GLB, rep)
        if j is not None:
            cub_clips = set(a.get("name") for a in j.get("animations", []))
            nm, ns = len(j.get("meshes", [])), len(j.get("skins", []))
            joints = len(j["skins"][0].get("joints", [])) if ns else 0
            rep.say("  %s: MD5 %s, %d KB, %d Netz(e), %d Haut, %d Knochen, %d Clips" % (CUB_GLB, md5(glb), len(glb) // 1024, nm, ns,
                                                                                          joints, len(cub_clips)))
            if nm != 1 or ns != 1:
                rep.err("%s: erwartet genau ein Netz und eine Haut (Werkstatt-CLAUDE.md 8)" % CUB_GLB)
            miss = sorted(vanilla_buck_clips() - cub_clips)
            if miss:
                rep.warn("%s: %d Clips aus Vanillas Animset buck fehlen im GLB (%s) -- der gespielte Erwachsene hat dieselben 15 "
                         "Clips; ob ein Zustand mit fehlendem Clip einfriert, ist ungespielt" % (CUB_GLB, len(miss), ", ".join(miss)))
    used_values = set()
    for rel in copy_asset:
        if not ANIMSET_OK.match(rel):
            continue
        data = final[rel]
        if data.startswith(b"\xef\xbb\xbf"):
            rep.err("%s: BOM" % rel)
            continue
        eol_of(data, rel, rep)
        try:
            root = ET.fromstring(data)
        except ET.ParseError as ex:
            rep.err("%s: kein wohlgeformtes XML (%s)" % (rel, ex))
            continue
        if root.tag != "animNode":
            rep.err("%s: Wurzel <%s>, erwartet <animNode>" % (rel, root.tag))
        anims = [(a.text or "").strip() for a in root.iter("m_AnimName")]
        if not anims or not all(anims):
            rep.err("%s: kein m_AnimName" % rel)
        for a in anims:
            if cub_clips and a not in cub_clips:
                rep.err("%s: Clip '%s' fehlt im GLB des Jungen -- ein Name ohne Clip friert das Tier ein" % (rel, a))
        conds = list(root.iter("m_Conditions"))
        mine = [c for c in conds if (c.findtext("m_Name") or "").strip() == ANIM_VAR]
        if len(conds) != 1 or len(mine) != 1:
            rep.err("%s: genau eine Bedingung %s erwartet (%d Bedingungen) -- sonst spielte der Knoten fuer jedes Tier mit Animset "
                    "buck, auch Vanillas Hirsche" % (rel, ANIM_VAR, len(conds)))
        for c in mine:
            if (c.findtext("m_Type") or "").strip() != "STRING":
                rep.err("%s: Bedingung %s nicht vom Typ STRING" % (rel, ANIM_VAR))
            used_values.add((c.findtext("m_Value") or "").strip())
        for no, ln in enumerate(data.decode("latin-1").split("\n"), 1):
            m = XML_CHEAT.search(ln)
            if m:
                rep.err("%s:%d: Wort einer Testhilfe/Debug/Cheat im Animations-Knoten (%s)" % (rel, no, m.group(0)))
    # Jeder Wert, den die Lua an B.ACT setzt, hat einen Knoten.
    for rel in copy_lua:
        code = "\n".join(c for c, _ in lua_split_lines(final[rel].decode("latin-1")))
        for m in re.finditer(r"setVariable\s*\(\s*B\.ACT\s*,\s*\"(\w+)\"", code):
            if m.group(1) not in used_values:
                rep.err("%s: setzt %s = '%s', dafuer gibt es keinen kopierten Animations-Knoten" % (rel, ANIM_VAR, m.group(1)))
            else:
                rep.say("  %s = '%s' (%s) hat seinen Knoten" % (ANIM_VAR, m.group(1), os.path.basename(rel)))
    rep.say("  Animations-Knoten: %d, Werte %s" % (len([r for r in copy_asset if ANIMSET_OK.match(r)]), ", ".join(sorted(used_values))))
    # B1c: Bilder der Oberflaeche (PNG-Kopf, IHDR-Groesse, gedeckelt); jedes Bild, das die kopierte Lua als media/ui/... nennt, wird
    # mitkopiert -- und jedes kopierte Bild nennt die Lua auch (sonst toter Ballast)
    rep.say("")
    rep.say("== Bilder der Oberflaeche (B1c)")
    named = set()
    for rel in copy_lua:
        code = "\n".join(c for c, _ in lua_split_lines(final[rel].decode("latin-1")))
        named.update("42/" + m for m in re.findall(r"[\"'](media/ui/BanditsNPCBear[A-Za-z0-9_]*\.png)[\"']", code))
    ui = [r for r in copy_asset if UI_ASSET.match(r)]
    for rel in ui:
        data = final[rel]
        if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            rep.err("%s: kein PNG (Kopf/IHDR)" % rel)
            continue
        w, h = struct.unpack(">II", data[16:24])
        rep.say("  %s: %d x %d, %d Bytes, MD5 %s" % (rel, w, h, len(data), md5(data)))
        if not (0 < w <= UI_MAX_PX and 0 < h <= UI_MAX_PX):
            rep.err("%s: %d x %d -- erwartet hoechstens %d x %d" % (rel, w, h, UI_MAX_PX, UI_MAX_PX))
        if rel not in named:
            rep.warn("%s wird kopiert, aber keine kopierte Lua-Datei nennt es" % rel)
    for rel in sorted(named - set(ui)):
        rep.err("die Lua nennt %s, das Bild ist nicht in der Uebernahme (fehlt in Test-Mod/Staging)" % rel[3:])
    if not ui and not named:
        rep.say("  keine")


# ---------------------------------------------------------------------------------------------------------------------------------
# 3. Texte
# ---------------------------------------------------------------------------------------------------------------------------------
_cn_chars = None


def vanilla_cn_chars(rep):
    global _cn_chars
    if _cn_chars is not None:
        return _cn_chars
    chars = set()
    if not os.path.isdir(VANILLA_CN):
        rep.err("Vanilla-CN fehlt (%s)" % VANILLA_CN)
    else:
        for fn in os.listdir(VANILLA_CN):
            p = os.path.join(VANILLA_CN, fn)
            if os.path.isfile(p):
                chars.update(rd(p).decode("utf-8", errors="ignore"))
    _cn_chars = chars
    return chars


def dump_json(d):
    return (json.dumps(d, indent=4, ensure_ascii=False) + "\n").encode("utf-8")


def load_json(data, label, rep):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        rep.err("%s: kein UTF-8" % label)
        return None
    if text.startswith("\ufeff"):
        rep.err("%s: BOM am Anfang" % label)
        return None
    try:
        return json.loads(text, object_pairs_hook=collections.OrderedDict)
    except ValueError as ex:
        rep.err("%s: kein gueltiges JSON (%s)" % (label, ex))
        return None


PLACE = re.compile(r"%\d|<LINE>|<BR>")


def plan_texts(tgt, src, merge, rep):
    """{rel_ziel: neue bytes}, Zusammenfassung, by_file (ohne Altschluessel), Altschluessel. Schreibt nichts."""
    out, summary, text_alt = {}, [], []
    by_file = collections.defaultdict(dict)
    for rel in merge:
        lang, fname = TRANSLATE.match(rel).groups()
        raw = rd(src[rel])
        d = load_json(raw, "Quelle " + rel, rep)
        if d is None:
            continue
        if dump_json(d) != raw:
            rep.err("Quelle %s: nicht im Round-Trip-Format (json.dumps(indent=4, ensure_ascii=False)+'\\n')" % rel)
        ks = list(d)
        if any(a > b for a, b in zip(ks, ks[1:])):
            rep.warn("Quelle %s: nicht sortiert" % rel)
        old = OLD_TEXT_KEYS.get(fname, set())
        for k in list(d):
            if k in old:
                if lang == "EN":
                    text_alt.append("text:%s:%s" % (fname, k))
                del d[k]
        by_file[fname][lang] = d
    tdir = os.path.join(tgt, "42", "media", "lua", "shared", "Translate")
    if os.path.isdir(tdir):
        other = [x for x in os.listdir(tdir) if os.path.isdir(os.path.join(tdir, x)) and x not in LANGS]
        if other:
            rep.err("NPC Crew hat Sprachen, die das Skript nicht kennt: %s -- LANGS erweitern" % ", ".join(other))
    cn = None
    for fname, langs in sorted(by_file.items()):
        ns = TEXT_NS.get(fname)
        if ns is None:
            rep.err("Texte %s: unbekannte Datei (erlaubt: %s)" % (fname, ", ".join(sorted(TEXT_NS))))
            continue
        missing = [l for l in LANGS if l not in langs]
        if missing:
            rep.err("Texte %s: es fehlen Sprachen %s (alle sieben, immer)" % (fname, ",".join(missing)))
        keyset = None
        for l in LANGS:
            if l in langs:
                ks = set(langs[l])
                if keyset is None:
                    keyset = ks
                elif ks != keyset:
                    rep.err("Texte %s: Sprache %s hat andere Schluessel als EN (%s)" % (fname, l, ", ".join(sorted(ks ^ keyset))[:200]))
        en = langs.get("EN", {})
        for k, v in en.items():
            if not (ns[0].match(k) or k in ns[1]):
                rep.err("Texte %s: Schluessel %s liegt nicht im Baeren-Namensraum" % (fname, k))
            if re.search(r"single[ -]player|multi[ -]player", str(v), re.I):
                rep.err("Texte %s %s: EN schreibt 'singleplayer'/'multiplayer' zusammen" % (fname, k))
            # B1b (schnittstelle_aenderungen.md, B1b OBERFLAECHE 1): Tooltips sind Rich-Text (Vanilla client/ISUI/ISButton.lua:317-334 ->
            # ISToolTip.lua:192, :358) -- ein "<" oder ">" in einem UI-Text wuerde dort als Formatbefehl verschluckt.
            if fname == "UI.json":
                for l in LANGS:
                    lv = langs.get(l, {}).get(k)
                    if lv is not None and re.search(r"[<>]", PLACE.sub("", str(lv))):
                        rep.err("Texte UI.json %s %s: '<' oder '>' im Text (Tooltip ist Rich-Text)" % (l, k))
            want = sorted(PLACE.findall(str(v)))
            for l in LANGS:
                if l in langs and k in langs[l] and sorted(PLACE.findall(str(langs[l][k]))) != want:
                    rep.err("Texte %s %s: Platzhalter in %s weichen von EN ab" % (fname, k, l))
        if "CN" in langs:
            cn = cn or vanilla_cn_chars(rep)
            for k, v in langs["CN"].items():
                bad = sorted(set(c for c in str(v) if ord(c) > 127 and c not in cn))
                if bad:
                    rep.err("Texte %s %s: CN-Zeichen, die Vanilla-CN nicht benutzt: %s" % (fname, k, " ".join("U+%04X" % ord(c) for c in bad)))
        # Vanilla verdecken? (gleicher Schluessel in Vanillas gleichnamiger Datei)
        vp = os.path.join(VANILLA_EN, fname)
        if os.path.isfile(vp):
            try:
                van = json.loads(rd(vp).decode("utf-8", errors="replace"))
            except ValueError:
                van = {}
            for k in en:
                if k in van:
                    rep.err("Texte %s: Schluessel %s gibt es in Vanilla -- unser Text verdeckte Vanillas" % (fname, k))
        counts = {}
        for l in LANGS:
            if l not in langs:
                continue
            rel_t = "42/media/lua/shared/Translate/%s/%s" % (l, fname)
            full_t = os.path.join(tgt, rel_t)
            new = langs[l]
            if os.path.isfile(full_t):
                raw = rd(full_t)
                old = load_json(raw, "NPC Crew " + rel_t, rep)
                if old is None:
                    continue
                if dump_json(old) != raw:
                    rep.err("NPC Crew %s: Round-Trip stimmt nicht -- Abbruch, sonst wuerde die ganze Datei umformatiert" % rel_t)
                    continue
                ks = list(old)
                if any(a > b for a, b in zip(ks, ks[1:])):
                    rep.warn("NPC Crew %s: nicht sortiert, neue Schluessel kommen vor den ersten groesseren" % rel_t)
                add = []
                for k in sorted(new):
                    if k in old:
                        if old[k] != new[k]:
                            rep.err("Texte %s: Schluessel %s gibt es in NPC Crew schon mit anderem Wert -- Kollision" % (rel_t, k))
                    else:
                        add.append(k)
                merged = collections.OrderedDict()
                i = 0
                for k in ks:
                    while i < len(add) and add[i] < k:
                        merged[add[i]] = new[add[i]]
                        i += 1
                    merged[k] = old[k]
                while i < len(add):
                    merged[add[i]] = new[add[i]]
                    i += 1
                data = dump_json(merged)
                again = json.loads(data.decode("utf-8"), object_pairs_hook=collections.OrderedDict)
                if dump_json(again) != data or list(again) != list(merged):
                    rep.err("Texte %s: Round-Trip nach dem Einfuegen stimmt nicht" % rel_t)
                if add:
                    out[rel_t] = data
                counts[l] = (len(old), len(merged), len(add))
            else:
                merged = collections.OrderedDict((k, new[k]) for k in sorted(new))
                out[rel_t] = dump_json(merged)
                counts[l] = (0, len(merged), len(merged))
        totals = set(c[1] for c in counts.values())
        if len(totals) > 1:
            rep.err("Texte %s: nach dem Zusammenfuehren ungleich viele Schluessel je Sprache: %s" % (fname, counts))
        else:
            ref = None
            for l in LANGS:
                rel_t = "42/media/lua/shared/Translate/%s/%s" % (l, fname)
                data = out.get(rel_t)
                if data is None and os.path.isfile(os.path.join(tgt, rel_t)):
                    data = rd(os.path.join(tgt, rel_t))
                if data is None:
                    continue
                ks = set(json.loads(data.decode("utf-8")))
                if ref is None:
                    ref = ks
                elif ks != ref:
                    rep.err("Texte %s: Sprache %s hat nach dem Zusammenfuehren andere Schluessel als EN" % (fname, l))
        if counts:
            c = counts.get("EN") or list(counts.values())[0]
            summary.append("%s: %d neu, %d -> %d je Sprache, %d Sprachen%s" % (fname, c[2], c[0], c[1], len(counts),
                                                                             "" if c[0] else " (Datei neu)"))
    return out, summary, by_file, text_alt


# ---------------------------------------------------------------------------------------------------------------------------------
# 4. Sandbox (Naht 4)
# ---------------------------------------------------------------------------------------------------------------------------------
OPT_BLOCK = re.compile(r"^option\s+(BanditsNPC\.\w+)\s*\{(.*?)^\}", re.M | re.S)


def opts_of_lua(final):
    """B.OPTS aus shared/BanditsNPCBear.lua: Name -> (def, min, max) als Text."""
    data = final.get("42/media/lua/shared/BanditsNPCBear.lua")
    out = {}
    if data is None:
        return out
    for m in re.finditer(r"^\s*(Bear\w+)\s*=\s*\{\s*def\s*=\s*([^,}\s]+)\s*(?:,\s*min\s*=\s*([-\d.]+)\s*,\s*max\s*=\s*([-\d.]+))?\s*\}",
                         data.decode("latin-1"), re.M):
        out[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return out


def plan_sandbox(tgt, src, rel, final, en_sandbox, rep):
    """{rel: neue bytes} fuer NPC Crews sandbox-options.txt, Zahl der Optionen. Schreibt nichts."""
    rep.say("")
    rep.say("== Sandbox-Optionen (Naht 4: an NPC Crews 42/media/sandbox-options.txt anhaengen)")
    if rel is None:
        rep.say("  keine sandbox-options.txt in der Quelle")
        return {}, 0
    raw = rd(src[rel])
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        rep.err("%s: nicht reines ASCII" % rel)
        return {}, 0
    if "\r" in text:
        rep.err("%s: CR (Regel: LF)" % rel)
    lines = text.split("\n")
    if not lines or lines[0].strip() != "VERSION = 1,":
        rep.err("%s: erste Zeile ist nicht 'VERSION = 1,'" % rel)
        return {}, 0
    body = "\n".join(lines[1:]).strip("\n") + "\n"
    if "VERSION" in body:
        rep.err("%s: VERSION steht noch einmal im Anhang" % rel)
    if re.search(r"^\s*--", body, re.M):
        rep.err("%s: '--'-Kommentar (nur C-Kommentare: ein unlesbarer Kommentar kostet die ganze Seite)" % rel)
    blocks = OPT_BLOCK.findall(body)
    stripped = re.sub(r"/\*.*?\*/", "", OPT_BLOCK.sub("", body), flags=re.S).strip()
    if stripped:
        rep.err("%s: ausser Optionen und C-Kommentaren steht noch etwas da: %r" % (rel, stripped[:80]))
    lua_opts = opts_of_lua(final)
    names = []
    for name, inner in blocks:
        names.append(name)
        short = name[len("BanditsNPC."):]
        if not short.startswith("Bear"):
            rep.err("Sandbox %s: nicht im Namensraum BanditsNPC.Bear*" % name)
        kv = dict((k.strip(), v.strip()) for k, v in re.findall(r"(\w+)\s*=\s*([^,\n]+)", inner))
        if kv.get("page") != "BanditsNPC":
            rep.err("Sandbox %s: page ist nicht BanditsNPC" % name)
        if kv.get("translation") != "BanditsNPC_" + short:
            rep.err("Sandbox %s: translation ist nicht BanditsNPC_%s" % (name, short))
        for key in ("Sandbox_BanditsNPC_" + short, "Sandbox_BanditsNPC_" + short + "_tooltip"):
            if key not in en_sandbox:
                rep.err("Sandbox %s: Text %s fehlt in EN/Sandbox.json" % (name, key))
        if kv.get("type") == "enum":
            n = int(kv.get("numValues", "0"))
            vt = kv.get("valueTranslation", "")
            for i in range(1, n + 1):
                if "Sandbox_%s_option%d" % (vt, i) not in en_sandbox:
                    rep.err("Sandbox %s: Text Sandbox_%s_option%d fehlt" % (name, vt, i))
        lo = lua_opts.get(short)
        if lo is None:
            rep.err("Sandbox %s: fehlt in B.OPTS (shared/BanditsNPCBear.lua)" % name)
        else:
            d, mn, mx = lo
            if kv.get("default") != d:
                rep.err("Sandbox %s: default %s, B.OPTS %s" % (name, kv.get("default"), d))
            if kv.get("type") == "enum":
                # enum: Werte 1..numValues (Vanilla-Form); B.OPTS klemmt auf min..max
                if mn is not None and (mn != "1" or kv.get("numValues") != mx):
                    rep.err("Sandbox %s: enum 1..%s, B.OPTS %s..%s" % (name, kv.get("numValues"), mn, mx))
            elif mn is not None and (kv.get("min") != mn or kv.get("max") != mx):
                rep.err("Sandbox %s: Bereich %s..%s, B.OPTS %s..%s" % (name, kv.get("min"), kv.get("max"), mn, mx))
    for short in lua_opts:
        if "BanditsNPC." + short not in names:
            rep.err("B.OPTS %s hat keine Sandbox-Option" % short)
    tfull = os.path.join(tgt, SANDBOX)
    if not os.path.isfile(tfull):
        rep.err("NPC Crew hat keine %s" % SANDBOX)
        return {}, len(names)
    traw = rd(tfull)
    eol = eol_of(traw, "NPC Crew " + SANDBOX, rep)
    ttext = traw.decode("latin-1").replace("\r\n", "\n")
    nc_names = set(re.findall(r"^option\s+(BanditsNPC\.\w+)", ttext, re.M))
    if body.strip() in ttext:
        if ARGS["erneut"]:
            rep.say("  %d Optionen stehen schon da (--erneut), uebersprungen" % len(names))
            return {}, len(names)
    for name in names:
        if name in nc_names:
            rep.err("Sandbox %s gibt es in NPC Crew schon -- Kollision" % name)
    new = ttext.rstrip("\n") + "\n\n" + body
    data = new.replace("\n", "\r\n").encode("ascii") if eol == b"\r\n" else new.encode("ascii")
    rep.say("  %d Optionen (%s ... %s), NPC Crew vorher %d Optionen, Zeilenenden %s" % (
        len(names), names[0] if names else "-", names[-1] if names else "-", len(nc_names), "CRLF" if eol == b"\r\n" else "LF"))
    return {SANDBOX: data}, len(names)


# ---------------------------------------------------------------------------------------------------------------------------------
# 5. Kollisionen
# ---------------------------------------------------------------------------------------------------------------------------------
def walk_rel(root, sub):
    out = []
    for top in ("42", "common"):
        base = os.path.join(root, top, "media", sub)
        for dp, _d, fs in os.walk(base):
            for fn in fs:
                out.append(rel_of(root, os.path.join(dp, fn)))
    return out


def is_own(rel):
    b = os.path.basename(rel)
    return bool(LUA_BEAR.match(rel) or UI_ASSET.match(rel) or re.match(r"^(NCBear|nc_bear|Item_NCBear)", b, re.I))


def collisions(tgt, final, copy_lua, copy_asset, rep):
    rep.say("")
    rep.say("== Kollisionsbericht (NPC Crew vor der Uebernahme, Vanilla)")
    nc_lua = [r for r in walk_rel(tgt, "lua") if r.endswith(".lua") and not is_own(r)]
    nc_scripts = [r for r in walk_rel(tgt, "scripts") if not is_own(r)]
    nc_anims = [r for r in walk_rel(tgt, "AnimSets") if not is_own(r)]
    pat = re.compile("|".join(OWN_NAME_RES))
    hard, in_comment = [], []
    for rel in nc_lua + nc_scripts + nc_anims:
        try:
            text = rd(os.path.join(tgt, rel)).decode("latin-1")
        except OSError:
            continue
        parts = lua_split_lines(text) if rel.endswith(".lua") else [(ln.rstrip("\r"), "") for ln in text.split("\n")]
        for no, (code, com) in enumerate(parts, 1):
            if pat.search(code):
                if not any(a["file"] == rel and a["line"] == code.strip() for a in NC_ALLOWED):
                    hard.append("%s:%d: %s" % (rel, no, (code + com).strip()[:100]))
            elif pat.search(com):
                in_comment.append("%s:%d" % (rel, no))
    rep.say("Baeren-Namen in NPC Crew (%d Muster): %d im Code, %d nur im Kommentar" % (len(OWN_NAME_RES), len(hard), len(in_comment)))
    for h in hard[:20]:
        rep.err("Kollision: " + h)
    if in_comment:
        rep.warn("Baeren-Namen nur in NPC-Crew-Kommentaren (keine Kollision): %s" % ", ".join(in_comment[:10]))
    for r in sorted(set(walk_rel(tgt, "lua")) | set(walk_rel(tgt, "scripts")) | set(walk_rel(tgt, "AnimSets"))
                    | set(walk_rel(tgt, "models_X")) | set(walk_rel(tgt, "textures")) | set(walk_rel(tgt, "ui"))):
        if is_own(r) and not ARGS["erneut"]:
            rep.err("Kollision: NPC Crew hat schon eine Datei im Baeren-Namensraum: %s" % r)
    for rel in sorted(final):
        if rel.startswith("42/media/lua/shared/Translate/") or rel == SANDBOX:
            continue
        full = os.path.join(tgt, rel)
        if os.path.exists(full) and rd(full) != final[rel] and not ARGS["erneut"]:
            rep.err("Kollision: %s gibt es in NPC Crew schon mit anderem Inhalt" % rel)
    # Gleicher Dateiname: NPC Crew (Ziel und echter Baum) und Vanilla (gleicher relativer Pfad verdeckte Vanillas Datei).
    names = collections.defaultdict(list)
    for root in sorted(set([tgt, NC_LIVE])):
        for sub in ("models_X", "textures", "scripts", "AnimSets", "sound", "ui"):      # B1c: + ui
            for rel in walk_rel(root, sub):
                names[os.path.basename(rel).lower()].append(rel)
    n_van = 0
    n_ban = 0
    for rel in sorted(copy_asset):
        b = os.path.basename(rel).lower()
        others = [o for o in names.get(b, []) if o != rel]
        if others:
            rep.err("Kollision: %s, gleicher Dateiname liegt in NPC Crew unter %s" % (rel, ", ".join(sorted(set(others)))))
        vp = os.path.join(VANILLA_MEDIA, rel[len("42/media/"):])
        if os.path.exists(vp):
            n_van += 1
            rep.err("Kollision: %s verdeckte Vanillas Datei %s" % (rel, vp))
        # B1c: Bandits ist Pflicht-Mod von NPC Crew; ein gleicher media/ui-Pfad verdeckte Bandits' Bild (oder umgekehrt)
        if UI_ASSET.match(rel):
            for bm in BANDITS_MEDIA:
                bp = os.path.join(bm, rel[len("42/media/"):])
                if os.path.exists(bp):
                    n_ban += 1
                    rep.err("Kollision: %s liegt auch in Bandits (%s)" % (rel, bp))
    rep.say("Dateinamen gegen NPC Crew, Vanilla und Bandits (media/ui): %d Vanilla-Treffer, %d Bandits-Treffer" % (n_van, n_ban))
    # Modell-/Skriptnamen und Tierart gegen Vanilla.
    van_scripts = os.path.join(VANILLA_MEDIA, "scripts")
    own_models = set()
    for rel in [r for r in final if r.startswith("42/media/scripts/")]:
        own_models.update(re.findall(r"^\s*(?:model|animationsMesh|item|sound)\s+(\w+)", final[rel].decode("latin-1"), re.M))
    hits = []
    for dp, _d, fs in os.walk(van_scripts):
        for fn in fs:
            t = rd(os.path.join(dp, fn)).decode("latin-1")
            for nm in own_models:
                if re.search(r"^\s*(?:model|animationsMesh|item|sound)\s+%s\b" % re.escape(nm), t, re.M):
                    hits.append("%s in %s" % (nm, fn))
    for nc in nc_scripts:
        t = rd(os.path.join(tgt, nc)).decode("latin-1")
        for nm in own_models:
            if re.search(r"^\s*(?:model|animationsMesh|item|sound)\s+%s\b" % re.escape(nm), t, re.M):
                hits.append("%s in NPC Crew %s" % (nm, nc))
    for h in hits:
        rep.err("Kollision Skriptname: " + h)
    rep.say("Skriptnamen %s gegen Vanilla und NPC Crew: %d Treffer" % (", ".join(sorted(own_models)) or "-", len(hits)))
    van_lua = os.path.join(VANILLA_MEDIA, "lua")
    vhits = 0
    for dp, _d, fs in os.walk(van_lua):
        for fn in fs:
            if fn.endswith(".lua") and re.search(r"ncbear|NCBear|BanditsNPCBear", rd(os.path.join(dp, fn)).decode("latin-1")):
                vhits += 1
                rep.err("Kollision: Vanilla %s nennt einen Baeren-Namen" % os.path.join(dp, fn))
    rep.say("Baeren-Namen in Vanilla-Lua: %d" % vhits)
    # Globale der kopierten Dateien gegen NPC Crew; v3.8.38 (Funktion gegen Modultabelle).
    own_globals = set()
    for rel in copy_lua:
        text = final[rel].decode("latin-1")
        for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=(?!=)", text, re.M):
            if m.group(1) not in GLOBAL_OK and m.group(1) not in GLOBAL_SAME:
                own_globals.add(m.group(1))
    for g in sorted(own_globals):
        for rel in nc_lua:
            t = rd(os.path.join(tgt, rel)).decode("latin-1")
            if re.search(r"(^|[^.\w])%s\s*=|function %s\s*\(" % (re.escape(g), re.escape(g)), t, re.M):
                rep.err("Kollision: Global %s wird auch in NPC Crew %s gesetzt" % (g, rel))
                break
    fn, mod = set(), set()
    for rel in set(nc_lua) | set(copy_lua):
        text = final[rel].decode("latin-1") if rel in final else rd(os.path.join(tgt, rel)).decode("latin-1")
        fn.update(re.findall(r"^function BanditsNPC\.([A-Za-z_]*)\(", text, re.M))
        mod.update(m.group(1) for m in re.finditer(r"BanditsNPC\.([A-Za-z_]*) = BanditsNPC\.\1 or \{\}", text))
    both = sorted(fn & mod)
    rep.say("Globale der Baeren-Dateien: %s; v3.8.38-Probe: %d Funktionen gegen %d Modultabellen, Kollision: %s" % (
        ", ".join(sorted(own_globals)) or "-", len(fn), len(mod), ", ".join(both) or "keine"))
    for b in both:
        rep.err("Kollision v3.8.38: BanditsNPC.%s ist Funktion UND Modultabelle" % b)
    # Skript des Jungen: mesh liegt auf der Platte, Textur der Rasse liegt auf der Platte.
    for rel in [r for r in final if r.startswith("42/media/scripts/")]:
        text = final[rel].decode("latin-1")
        for kind, val in re.findall(r"^\s*(mesh|meshFile)\s*=\s*([^,\s]+)", text, re.M):
            p = "42/media/models_X/" + val
            if p not in final:
                rep.err("%s: %s = %s liegt nicht in der Uebernahme (%s)" % (rel, kind, val, p))
        rep.say("Skript %s: Module %s, Namen %s" % (rel, ", ".join(re.findall(r"^\s*module\s+(\w+)", text, re.M)),
                                                  ", ".join(re.findall(r"^\s*(?:model|animationsMesh)\s+(\w+)", text, re.M))))
    defs = final.get("42/media/lua/shared/BanditsNPCBearDefs.lua")
    if defs:
        dtext = defs.decode("latin-1")
        for val in sorted(set(re.findall(r"\btexture(?:Male|Baby)?\s*=\s*\"(\w+)\"", dtext))):
            if "42/media/textures/Body/%s.png" % val not in final:
                rep.err("Defs: Rassen-Textur %s liegt nicht als 42/media/textures/Body/%s.png in der Uebernahme" % (val, val))
        for val in re.findall(r"\bbodyModel\s*=\s*\"(\w+)\"", dtext):
            if not any(re.search(r"^\s*model\s+%s\b" % re.escape(val), final[r].decode("latin-1"), re.M)
                       for r in final if r.startswith("42/media/scripts/")):
                rep.err("Defs: bodyModel %s hat kein model-Skript in der Uebernahme" % val)
    # Texte: jeder Schluessel aus der Lua steht in EN; englische Ersatztexte (U.EN) wortgleich.
    rel_en = "42/media/lua/shared/Translate/EN/UI.json"
    data = final.get(rel_en)
    if data is None and os.path.isfile(os.path.join(tgt, rel_en)):
        data = rd(os.path.join(tgt, rel_en))
    en_final = json.loads(data.decode("utf-8")) if data else {}
    used = set()
    fallback = {}
    for rel in copy_lua:
        t = "\n".join(c for c, _ in lua_split_lines(final[rel].decode("latin-1")))
        for k in re.findall(r'"(UI_BN_[A-Za-z0-9_]+)"', t):
            if not k.endswith("_"):
                used.add(k)
        # englische Ersatztexte: nur der Block "U.EN = { ... }" (client/BanditsNPCBearClient.lua); andere Tabellen mit
        # Textschluesseln als Feldnamen (WHY_T im Server) sind keine Ersatztexte
        blk = re.search(r"^U\.EN\s*=\s*\{\s*$(.*?)^\}", t, re.M | re.S)
        if blk:
            for k, v in re.findall(r'^\s*(UI_BN_Bear_[A-Za-z0-9_]+)\s*=\s*"((?:[^"\\]|\\.)*)"\s*,', blk.group(1), re.M):
                fallback[k] = v
    miss = sorted(k for k in used if k not in en_final)
    for k in miss:
        rep.err("Text %s wird in der Baeren-Lua benutzt, steht aber nicht in EN/UI.json" % k)
    own_en = dict((k, v) for k, v in en_final.items() if k.startswith("UI_BN_Bear_"))
    for k, v in sorted(fallback.items()):
        if own_en.get(k) != v:
            rep.err("Ersatztext %s weicht von EN/UI.json ab" % k)
    for k in sorted(set(own_en) - set(fallback)):
        rep.warn("EN-Schluessel %s hat keinen englischen Ersatztext im Code" % k)
    rep.say("Texte aus der Lua: %d benutzt, fehlen in EN: %d; Ersatztexte %d, wortgleich: %s" % (
        len(used), len(miss), len(fallback), "ja" if all(own_en.get(k) == v for k, v in fallback.items()) else "NEIN"))


# ---------------------------------------------------------------------------------------------------------------------------------
# 6. Cheat-Pruefung und Tier-Regel
# ---------------------------------------------------------------------------------------------------------------------------------
def call_args(text, start):
    args, cur, depth, i, n = [], [], 0, start, len(text)
    while i < n:
        c = text[i]
        if c == '"' or c == "'":
            j = i + 1
            while j < n and text[j] != c and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            cur.append(text[i:j + 1])
            i = j + 1
            continue
        if c in "({[":
            depth += 1
        elif c in ")}]":
            if depth == 0:
                args.append("".join(cur))
                return args
            depth -= 1
        elif c == "," and depth == 0:
            args.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    args.append("".join(cur))
    return args


def lua_setglobals(data):
    if not os.path.isfile(LUAC):
        return None
    fd, tmp = tempfile.mkstemp(suffix=".lua", prefix="baer_luac_")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        p = subprocess.run([LUAC, "-p", "-l", tmp], capture_output=True, text=True, errors="replace")
        if p.returncode != 0:
            return None
        return [(int(m.group(1)), m.group(2)) for m in re.finditer(r"\[(\d+)\]\s+SETGLOBAL\s+[^;\n]*;\s*([A-Za-z_]\w*)", p.stdout)]
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


def global_ok(name, code):
    if name in GLOBAL_OK:
        return True
    if name in GLOBAL_SAME:
        return re.match(r"^\s*%s\s*=\s*%s\s+or\s+\{\s*\}\s*$" % (re.escape(name), re.escape(name)), code) is not None
    # Aktionsklassen: BanditsNPCBear*Action = ISBaseTimedAction:derive("gleicher Name")
    return name.startswith("BanditsNPCBear") and re.match(
        r"^\s*%s\s*=\s*ISBaseTimedAction:derive\s*\(\s*[\"']%s[\"']\s*\)\s*;?\s*$" % (re.escape(name), re.escape(name)), code) is not None


def _strings_of(code):
    out = [s.group(1) if s.group(1) is not None else s.group(2) for s in LUA_STRING.finditer(code)]
    out += [s.group(2) for s in LONG_STRING.finditer(code)]
    return out


def _norm_text(s):
    return s.strip().rstrip(".").strip().casefold()


def bench_marks(plan, src, copy_fn_names):
    """Texte (addOption/say/print-Helfer) und Funktionsnamen der NCBearBench*-Dateien. Namen, die auch eine kopierte Datei als
    Funktion definiert, zaehlen nicht als Fingerabdruck (sonst meldete die Pruefung den Kern)."""
    texts, funcs, shared = set(), set(), set()
    for rel, _why in plan["skipped"]:
        if not (rel.endswith(".lua") and BENCH_ANY.match(os.path.basename(rel))):
            continue
        for code, _com in lua_split_lines(rd(src[rel]).decode("latin-1")):
            m = re.match(r"^\s*(?:local\s+)?function\s+([A-Za-z_]\w*)\s*\(", code)
            if m:
                (shared if m.group(1) in copy_fn_names else funcs).add(m.group(1))
            plain = re.search(r"\baddOption\w*\s*\(|\bsay\s*\(", code)
            helper = (not plain) and re.search(r"\b\w*[Ss]ay\s*\(|\bline\s*\(", code)
            if plain or helper:
                for s in _strings_of(code):
                    t = _norm_text(s)
                    # nur Saetze und Menuetexte (zwei Woerter oder lang): einzelne Woerter wie "bait", "cub", "bear" sind
                    # Fachwoerter, die der echte Code auch braucht (sonst meldete die Pruefung den Kern)
                    if re.search(r"[a-z].*[a-z]", t) and (" " in t or len(t) >= 10):
                        texts.add(t)
    return texts, funcs, shared


def cheat_check(plan, src, rep):
    rep.say("")
    rep.say("== Cheat-Pruefung (Kevin 08.11.: keine Cheat- oder Testmenues nach NPC Crew) und Tier-Regel (Plan 12.1 Punkt 7)")
    final = plan["final"]
    rules = [(rid, re.compile(rx), why) for rid, rx, why in CHEAT_RULES]
    found, comments, seen = [], [], set()
    used = [[] for _ in CHEAT_ALLOWED]
    tier_used = collections.defaultdict(list)
    copy_fn = set()
    for rel in plan["copy_lua"]:
        copy_fn.update(re.findall(r"^\s*(?:local\s+)?function\s+(?:[\w.:]*[.:])?([A-Za-z_]\w*)\s*\(", final[rel].decode("latin-1"), re.M))
    prints, bfuncs, bshared = bench_marks(plan, src, copy_fn)

    def add(rel, no, rid, code, why, what):
        key = (rel, no, rid, what)
        if key in seen:
            return
        seen.add(key)
        for i, a in enumerate(CHEAT_ALLOWED):
            if a["file"] == rel and a["rule"] == rid and a["code"] in code:
                used[i].append("%s:%s" % (rel, no) if no else rel)
                return
        found.append("%s: %s [%s: %s]" % ("%s:%d" % (rel, no) if no else rel, why, rid, what))

    def check_code(rel, no, code):
        for rid, rx, why in rules:
            m = rx.search(code)
            if m:
                add(rel, no, rid, code, why, m.group(0))
        for body in _strings_of(code):
            m = CHEAT_STRING.search(body)
            if m:
                add(rel, no, "wort", code, "Cheat-/Spawn-/Debug-Wort in einem String im Code", body[:40])
            if _norm_text(body) in prints:
                add(rel, no, "bankspur", code, "Text aus dem Werkbank-Menue", body[:40])
        for m in CHEAT_GLOBAL_FN.finditer(code):
            if not re.search(r"\blocal\s+$", code[:m.start()]):
                add(rel, no, "global", code, "globale Funktion (in der Konsole aufrufbar: Konsolenbefehl)", m.group(1))
        m = CHEAT_GLOBAL_SET.match(code)
        if m and not global_ok(m.group(1), code):
            add(rel, no, "global", code, "globale Zuweisung (in der Konsole aufrufbar)", m.group(1))
        m = re.match(r"^\s*(?:local\s+)?function\s+(\w+)\s*\(", code)
        if m and m.group(1) in bfuncs:
            add(rel, no, "bankspur", code, "Funktionsname aus der Werkbank", m.group(1))

    def menu_check(rel, codes):
        code_text = "\n".join(codes)
        local_str = set(m.group(1) for m in re.finditer(r"\blocal\s+(\w+)\s*=\s*[\"'][^\"'\n]*[A-Za-z][^\"'\n]*[A-Za-z]", code_text))
        for rx in (MENU_CALL, BTN_CALL):
            for m in rx.finditer(code_text):
                args = call_args(code_text, m.end())
                if rx is BTN_CALL:
                    texts = args[4:5] if "ISButton" in m.group(0) else args[:1]
                else:
                    texts = args[:2] if m.group(1).startswith("insert") else args[:1]
                no = code_text.count("\n", 0, m.start()) + 1
                for a in texts:
                    lits = _strings_of(TEXT_CALL.sub("", a))
                    if any(re.search(r"[A-Za-z].*[A-Za-z]", x) for x in lits) or a.strip() in local_str:
                        add(rel, no, "menue", codes[no - 1], "Menue-Eintrag mit festem Text statt Textschluessel (Testmenue?)", a.strip()[:40])
        # B1c: Optionen-Seite (PZAPI.ModOptions) -- jedes Text-Argument ist ein Schluessel UI_BN_Bear_* (Vanilla ruft getText), nie
        # ein fester Satz, nie ein Ausdruck (Nachbesserung B1c A4: mo_text_hits)
        for no, what, why in mo_text_hits(code_text):
            add(rel, no, "menue", codes[no - 1], why, what)

    n_lines = 0
    for rel in plan["copy_lua"]:
        rest = os.path.basename(rel)[len("BanditsNPCBear"):]
        if CHEAT_NAME.search(rest) or CHEAT_FILE_REST.match(rest):
            add(rel, 0, "dateiname", os.path.basename(rel), "Dateiname nach Testhilfe/Debug/Cheat/Werkzeug", os.path.basename(rel))
        parts = lua_split_lines(final[rel].decode("latin-1"))
        cur_fn = None
        for no, (code, com) in enumerate(parts, 1):
            head = FN_HEAD.match(code)
            if head:
                cur_fn = head.group(1) or head.group(2)
            elif code[:1] not in ("", " ", "\t"):
                cur_fn = None
            if code.strip():
                n_lines += 1
                check_code(rel, no, code)
                if not TIER_DEF.match(code):
                    for tid, rx, allowed, why in TIER_RULES:
                        if rx.search(code):
                            if (rel, cur_fn) in allowed:
                                tier_used[tid].append("%s:%d (%s)" % (os.path.basename(rel), no, cur_fn or "Dateiebene"))
                            else:
                                add(rel, no, "tier", code, "%s -- Aufruf aus %s" % (why, cur_fn or "Dateiebene"), tid)
            if re.search(r"\bNC[A-Z][A-Za-z]*_[A-Za-z]|\bNC[A-Za-z]*Bench|(?i:\btesthilfe\b|\bwerkbank\b)", com):
                comments.append("%s:%d" % (rel, no))
        code_lines = [c for c, _ in parts]
        menu_check(rel, code_lines)
        code_text = "\n".join(code_lines)
        for off, what in scan_force_hits(code_text):
            no = code_text.count("\n", 0, off) + 1
            add(rel, no, "force", code_lines[no - 1], SCAN_WHY, what)
        sg = lua_setglobals(final[rel])
        if sg is None:
            rep.warn("%s: luac5.1 lief nicht (%s) -- globale Zuweisungen nur per Regex geprueft" % (rel, LUAC))
        else:
            for ln, name in sg:
                gcode = parts[ln - 1][0] if 0 < ln <= len(parts) else ""
                if not global_ok(name, gcode):
                    add(rel, ln, "global", gcode, "globale Zuweisung laut luac", name)
    for rel in plan["copy_asset"]:
        b = os.path.basename(rel)
        if CHEAT_NAME.search(b):
            add(rel, 0, "dateiname", b, "Dateiname nach Testhilfe/Debug/Cheat/Spawn", b)
    n_text = 0
    for fname, langs in sorted(plan["by_file"].items()):
        for l, d in sorted(langs.items()):
            for k, v in d.items():
                n_text += 1
                kk = k[len("UI_BN_"):] if k.startswith("UI_BN_") else k
                if CHEAT_NAME.search(kk):
                    add("Translate/" + fname, 0, "text", k, "Textschluessel nach Testhilfe/Debug/Cheat/Spawn", k)
                if l == "EN":
                    if CHEAT_TEXT.search(str(v)):
                        add("Translate/" + fname, 0, "text", k, "EN-Text klingt nach Test-/Cheat-Menue", "%s = '%s'" % (k, str(v)[:50]))
                    if _norm_text(str(v)) in prints:
                        add("Translate/" + fname, 0, "bankspur", k, "EN-Text aus dem Werkbank-Menue", k)
    for rel in [r for r in final if r.startswith("42/media/scripts/")]:
        text = final[rel].decode("latin-1")
        for m in re.finditer(r"^\s*(?:item|model|animationsMesh)\s+(\w+)", text, re.M):
            if re.search(r"(?i)bench|cheat|debug|spawn|test", m.group(1)):
                add(rel, 0, "skript", m.group(1), "Skriptname nach Testhilfe/Debug/Cheat/Spawn", m.group(1))
    if SANDBOX in final:
        for name in re.findall(r"^option\s+(BanditsNPC\.\w+)", plan["sandbox_body"], re.M):
            if CHEAT_NAME.search(name):
                add(SANDBOX, 0, "sandbox", name, "Sandbox-Option nach Testhilfe/Debug/Cheat/Spawn", name)
    rep.say("geprueft: %d Lua-Dateien (%d Codezeilen), %d Texte, %d Dateinamen; %d Zeilenregeln + wort, global, menue, tier, force, "
            "bankspur (%d Werkbank-Texte, %d Werkbank-Funktionsnamen; %d gemeinsame Namen nicht gewertet: %s); %d Ausnahmen" % (
                len(plan["copy_lua"]), n_lines, n_text, len(plan["copy_lua"]) + len(plan["copy_asset"]), len(CHEAT_RULES),
                len(prints), len(bfuncs), len(bshared), ", ".join(sorted(bshared)) or "-", len(CHEAT_ALLOWED)))
    for a, hits in zip(CHEAT_ALLOWED, used):
        if hits:
            rep.say("  erlaubt %s [%s] (%s)" % (", ".join(hits), a["rule"], a["why"]))
        else:
            rep.warn("Cheat-Ausnahme greift nicht mehr (streichen?): %s [%s] %s" % (a["file"], a["rule"], a["code"]))
    for tid, _rx, allowed, why in TIER_RULES:
        hits = tier_used.get(tid, [])
        rep.say("  Tier-Regel %s: %s -- %s" % (tid, ", ".join(hits) or ("kein Aufruf" if allowed else "kein Aufruf (erlaubt: nirgends)"), why))
        if not hits and allowed:              # B1d: eine Regel ohne erlaubten Aufrufer (probeweg) erwartet keinen
            rep.warn("Tier-Regel %s: kein erlaubter Aufruf gefunden (Code umgebaut? TIER_RULES nachziehen)" % tid)
    if comments:
        rep.warn("Kommentare in Baeren-Dateien nennen Testbefehle oder die Testhilfe (kein Cheat): %s" % ", ".join(comments[:12]))
    rep.say("Funde: %d" % len(found))
    for f in found:
        rep.err("Cheat-Pruefung: " + f)
    return len(found)


# ---------------------------------------------------------------------------------------------------------------------------------
# 7. Pruefer
# ---------------------------------------------------------------------------------------------------------------------------------
def run_tool(args):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=NC_LIVE)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def checkers(root, lua_rels, final, rep):
    rep.say("")
    rep.say("== Pruefer auf dem geschriebenen Stand (%s)" % root)
    bad = 0
    for rel in lua_rels:
        p = os.path.join(root, rel)
        res = []
        for tool in ("luacheck.py", "scopecheck.py", "localcount.py"):
            rc, out = run_tool([os.path.join(TOOLS, tool), p])
            if rc != 0:
                bad += 1
                rep.err("%s: %s meldet einen Fehler:\n%s" % (rel, tool, "\n".join(out.strip().splitlines()[-6:])))
                res.append(tool + " FEHLER")
            else:
                if tool == "localcount.py":
                    nums = [int(x) for x in re.findall(r"^\s*(\d+) (?:locals|declared in total)", out, re.M)]
                    if nums and max(nums) >= 180:
                        rep.err("%s: localcount %d (ab 180 aufteilen)" % (rel, max(nums)))
                    res.append("localcount ok (hoechstens %d)" % (max(nums) if nums else 0))
                else:
                    res.append(tool.replace(".py", "") + " ok")
        rep.say("  %s: %s" % (rel, ", ".join(res)))
    rc, out = run_tool([os.path.join(TOOLS, "luacheck_pz.py")] + [os.path.join(root, r) for r in lua_rels])
    if "luacheck_pz:" not in out:
        rep.err("luacheck_pz lief nicht:\n" + out[-400:])
        return bad
    hits, allowed = [], []
    classes = set()
    for rel in lua_rels:
        classes.update(re.findall(r"^(BanditsNPCBear\w+)\s*=\s*ISBaseTimedAction:derive", final[rel].decode("latin-1"), re.M))
    for ln in out.splitlines():
        m = re.match(r"^(.*?):(\d+): \((\w\d+)\) .*'(\w+)'", ln)
        if not m:
            continue
        key = (os.path.basename(m.group(1)), m.group(4))
        if m.group(3) == "W113" and key in PZ_ALLOWED and m.group(4) in classes:
            allowed.append("%s:%s %s" % (key[0], m.group(2), key[1]))
        else:
            hits.append(ln.strip())
    for h in hits:
        rep.err("luacheck_pz: " + h)
    rep.say("  luacheck_pz auf %d kopierten Dateien: %d Treffer, %d erlaubt (Aktionsklasse aus einer anderen kopierten Datei: %s)"
            % (len(lua_rels), len(hits), len(allowed), ", ".join(allowed) or "-"))
    return bad


# ---------------------------------------------------------------------------------------------------------------------------------
# Ablauf
# ---------------------------------------------------------------------------------------------------------------------------------
def build_plan(tgt, src, rep):
    copy_lua, copy_asset, merge, skipped, alt, sandbox = collect_source(src, rep)
    final = {}
    for rel in copy_lua + copy_asset:
        final[rel] = rd(src[rel])
    form_check(final, copy_lua, copy_asset, rep)
    texts, tsum, by_file, text_alt = plan_texts(tgt, src, merge, rep)
    final.update(texts)
    en_sb = {}
    rel_sb = "42/media/lua/shared/Translate/EN/Sandbox.json"
    data = final.get(rel_sb)
    if data is None and os.path.isfile(os.path.join(tgt, rel_sb)):
        data = rd(os.path.join(tgt, rel_sb))
    if data:
        en_sb = json.loads(data.decode("utf-8"))
    sb, n_opt = plan_sandbox(tgt, src, sandbox, final, en_sb, rep)
    final.update(sb)
    body = ""
    if sandbox:
        body = "\n".join(rd(src[sandbox]).decode("latin-1").split("\n")[1:])
    return {"copy_lua": copy_lua, "copy_asset": copy_asset, "merge": merge, "skipped": skipped, "alt": alt, "text_alt": text_alt,
            "final": final, "texts": tsum, "by_file": by_file, "n_opt": n_opt, "sandbox_body": body}


def print_plan(plan, rep):
    rep.say("")
    rep.say("== Dateien")
    size = sum(len(plan["final"][r]) for r in plan["copy_lua"] + plan["copy_asset"])
    rep.say("kopieren: %d Lua, %d Modell/Textur/Skript/Animations-Knoten, zusammen %.1f MB" % (
        len(plan["copy_lua"]), len(plan["copy_asset"]), size / 1048576.0))
    for rel in plan["copy_lua"]:
        rep.say("  lua    %s" % rel)
    for rel in plan["copy_asset"]:
        rep.say("  datei  %s (%d KB, MD5 %s)" % (rel, len(plan["final"][rel]) // 1024, md5(plan["final"][rel])))
    for rel, why in plan["skipped"]:
        rep.say("  NICHT  %s (%s)" % (rel, why))
    for rel in plan["alt"]:
        rep.say("  ALT    %s (noch umzubenennen, B5a)" % rel)
    rep.say("")
    rep.say("== Texte")
    for s in plan["texts"]:
        rep.say("  " + s)
    rep.say("")
    rep.say("== Naehte (NAEHTE.md): keine Zeile in einer NPC-Crew-Lua-Datei. Laufzeit-Aufsaetze auf NPC Crew in OnGameBoot stehen in den "
            "kopierten Dateien (B1c: dazu ein Aufsatz auf VANILLAS Kartenklassen, Datei-Ende + OnGameStart, NAEHTE.md Zeile 18; B1d: "
            "keine neue Naht, NAEHTE.md Zeile 25); geaendert werden nur NPC Crews Texte (zusammenfuehren) und sandbox-options.txt (anhaengen).")


def write_all(root, final, rep):
    n = 0
    for rel, data in sorted(final.items()):
        full = os.path.join(root, rel)
        if os.path.isfile(full) and rd(full) == data:
            continue
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
        if rd(full) != data:
            rep.err("%s: nach dem Schreiben nicht gleich -- Platte pruefen" % rel)
        n += 1
    return n


def game_running():
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True, errors="replace").stdout
    except OSError:
        return None
    return "projectzomboid" in out.lower()


def under(path, bad):
    a, b = os.path.abspath(path).lower(), os.path.abspath(bad).lower()
    return a == b or a.startswith(b + os.sep)


def make_probe(probe_dir, staging, rep):
    probe_dir = os.path.abspath(probe_dir)
    for bad in (ZOMBOID, NC_LIVE, TEST):
        if under(probe_dir, bad):
            rep.err("Probe-Ordner liegt unter %s -- dort laedt das Spiel Kopien als Mod oder es traefe echte Dateien" % bad)
            return None, None
    if os.path.exists(probe_dir) and os.listdir(probe_dir) and not os.path.isfile(os.path.join(probe_dir, PROBE_MARK)):
        rep.err("%s ist nicht leer und keine Probe dieses Skripts (Marke %s fehlt) -- nichts geloescht, Abbruch" % (probe_dir, PROBE_MARK))
        return None, None
    for sub in ("quelle", "NPCCrew"):
        p = os.path.join(probe_dir, sub)
        if os.path.exists(p):
            shutil.rmtree(p)
    os.makedirs(probe_dir, exist_ok=True)
    with open(os.path.join(probe_dir, PROBE_MARK), "w", encoding="ascii") as f:
        f.write("Probe von baer_uebernahme.py, darf geloescht werden.\n")
    # Quelle: Kopie der Test-Mod ohne Git-Teile, darueber das Staging.
    qroot = os.path.join(probe_dir, "quelle")
    src, _sk = source_map(TEST, staging, rep)
    for rel, full in sorted(src.items()):
        if rel in GIT_ROOT_FILES:
            continue
        dst = os.path.join(qroot, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(full, dst)
        if rd(dst) != rd(full):
            rep.err("Probe-Quelle %s: Kopie nicht byte-gleich" % rel)
    # Ziel: nur die noetigen Teile von NPC Crew (Lua, Skripte, AnimSets, Sandbox, mod.info); Texturen/Modelle liest das Skript im echten Baum.
    root = os.path.join(probe_dir, "NPCCrew")
    os.makedirs(root)
    for sub in ("42/media/lua", "42/media/scripts", "common/media/AnimSets", "42/media/AnimSets"):
        s = os.path.join(NC_LIVE, sub)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(root, sub))
    for one in (SANDBOX, "42/mod.info", "mod.info"):
        s = os.path.join(NC_LIVE, one)
        if os.path.isfile(s):
            os.makedirs(os.path.dirname(os.path.join(root, one)), exist_ok=True)
            shutil.copy2(s, os.path.join(root, one))
    return qroot, root


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    rep = Report()
    probe, staging = None, None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--probe", "--staging"):
            if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                print("%s braucht einen Ordner" % a)
                return 2
            if a == "--probe":
                probe = argv[i + 1]
            else:
                staging = os.path.abspath(argv[i + 1])
            i += 1
        elif a == "--echt":
            ARGS["echt"] = True
        elif a == "--ja-kevin-hat-es-gesagt":
            pass
        elif a == "--erneut":
            ARGS["erneut"] = True
        elif a == "--vor-b5a":
            ARGS["vor_b5a"] = True
        else:
            print("unbekannt: %s (Hilfe: -h)" % a)
            return 2
        i += 1
    echt = ARGS["echt"]
    if probe and echt:
        print("--probe und --echt zusammen geht nicht")
        return 2
    if echt and "--ja-kevin-hat-es-gesagt" not in argv:
        print("--echt schreibt in NPC Crew und verlangt ausdruecklich --ja-kevin-hat-es-gesagt (nur auf Kevins Wort).")
        return 2
    if echt and (ARGS["vor_b5a"] or staging):
        print("--echt geht nicht mit --vor-b5a oder --staging: die echte Uebernahme liest nur die Test-Mod und prueft streng.")
        return 2
    if not os.path.isdir(TEST):
        print("Test-Mod fehlt: %s" % TEST)
        return 1
    if staging:
        for bad in (NC_LIVE, TEST):
            if under(staging, bad):
                print("--staging darf nicht in %s liegen" % bad)
                return 2

    if probe:
        mode = "PROBE"
        qroot, tgt = make_probe(probe, staging, rep)
        if tgt is None:
            for e in rep.errors:
                print("FEHLER: " + e)
            return 1
        src, git_sk = source_map(qroot, None, rep)
        src_label = "%s (Kopie der Test-Mod ohne .git%s)" % (qroot, ", darueber " + staging if staging else "")
    else:
        src, git_sk = source_map(TEST, staging, rep)
        src_label = TEST + ("  +  Staging " + staging if staging else "")
        if echt:
            mode, tgt = "ECHT", NC_LIVE
            running = game_running()
            if running is None:
                rep.err("tasklist lief nicht: ob das Spiel laeuft, ist unbekannt -- Abbruch")
            elif running:
                rep.err("Project Zomboid laeuft: erst das Spiel beenden.")
        else:
            mode, tgt = "TROCKENLAUF", NC_LIVE

    rep.say("baer_uebernahme.py -- %s%s" % (mode, " --vor-b5a" if ARGS["vor_b5a"] else ""))
    rep.say("Quelle: %s" % src_label)
    rep.say("Ziel:   %s%s" % (tgt, "  (nur lesen)" if mode == "TROCKENLAUF" else ""))
    plan = build_plan(tgt, src, rep)
    plan["skipped"] = sorted(set(git_sk)) + plan["skipped"]
    print_plan(plan, rep)
    alt_report(plan["alt"], plan["text_alt"], rep)
    collisions(tgt, plan["final"], plan["copy_lua"], plan["copy_asset"], rep)
    cheat_check(plan, src, rep)

    if rep.errors:
        rep.say("")
        rep.say("NICHT geschrieben: %d Fehler." % len(rep.errors))
    elif mode == "TROCKENLAUF":
        rep.say("")
        rep.say("Trockenlauf: nichts geschrieben. Wuerde %d Datei(en) schreiben." % len(plan["final"]))
    else:
        written = write_all(tgt, plan["final"], rep)
        rep.say("")
        rep.say("geschrieben: %d Datei(en) nach %s" % (written, tgt))
        checkers(tgt, plan["copy_lua"], plan["final"], rep)

    rep.say("")
    for w in rep.warns:
        rep.say("WARNUNG: " + w)
    for e in rep.errors:
        rep.say("FEHLER: " + e)
    rep.say("")
    rep.say("ERGEBNIS: %s -- %d Fehler, %d Warnungen (%s). Statisch geprueft, nicht gespielt." % (
        "OK" if not rep.errors else "NICHT OK", len(rep.errors), len(rep.warns), mode))
    n_alt = len(plan["alt"]) + len(plan["text_alt"])
    if not ARGS["vor_b5a"] and n_alt and len(rep.errors) == n_alt and all(e.startswith("noch umzubenennen (B5a)") for e in rep.errors):
        rep.say("Erwartet rot: genau die %d Altlasten aus ALT_EXPECTED (NAEHTE.md 'Erlaubte Fundstellen des Trockenlaufs'), sonst nichts." % n_alt)
    if mode == "ECHT" and not rep.errors:
        rep.say("Danach von Hand: Version + Changelog in NPC Crew, Test-Mod aus Kevins Liste UND ihre Lua leeren (zwei Mods mit denselben "
                "Pfaden), Spiel neu starten.")
    if mode == "PROBE":
        try:
            with open(os.path.join(tgt, "bericht.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(rep.lines) + "\n")
        except OSError:
            pass
    return 0 if not rep.errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
