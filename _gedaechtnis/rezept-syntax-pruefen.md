---
name: rezept-syntax-pruefen
description: "B42-craftRecipe-Eingaben immer in [ ] (item 4 [Base.X]); ein Syntaxfehler in einer scripts/*.txt laesst das ganze Spiel nicht laden -- vor jedem Einbau neuer Rezepte gegen Vanilla pruefen"
metadata:
  node_type: memory
  type: feedback
  originSessionId: cccbd9d6-dd89-4eba-8fad-b3beed093bcb
  modified: 2026-11-13T21:56:49.864Z
---

13.11.2026: Nach dem F4-Einbau lud Kevins Spiel nicht ("das spiel laesst sich nicht laden kommt immer error"). console.txt: `unknown recipe param: Base.LeatherStrips at InputScript.Load`, danach `ScriptManager.Load: Script load errors` -- ein einziges falsch geschriebenes Rezept (`item 4 Base.LeatherStrips` statt `item 4 [Base.LeatherStrips]`) bricht das Laden ALLER Skripte ab. Weder Lua-Pruefer noch Attrappen noch Gegenpruefer haben es gesehen, weil niemand die Skript-Syntax prueft.

**Why:** Kevin kann nicht testen, wenn das Spiel nicht laedt; ein Ein-Zeichen-Fehler kostet einen ganzen Testabend.

**How to apply:** Bei jedem neuen oder geaenderten `scripts/*.txt` (Rezepte, Items, Modelle): jede Zeile gegen eine Vanilla-Fundstelle derselben Form legen (Eingaben `item N [A;B]` bzw. `tags[...]`, Ausgaben `item N Modul.Typ` ohne Klammern). In Lauf-Auftraege fuer Bauer/Pruefer die Pflicht "Skript-Syntax Zeile fuer Zeile gegen Vanilla" schreiben. Nach dem Einbau console.txt auf `ScriptBucket`/`InputScript` pruefen, sobald Kevin startet.
