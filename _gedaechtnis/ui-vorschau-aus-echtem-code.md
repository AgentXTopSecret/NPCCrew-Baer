---
name: ui-vorschau-aus-echtem-code
description: "UI-Vorschaubilder fuer Kevin immer aus dem echten Lua-Code zeichnen (Zeichen-Mitschrift + echte Spielschriften), nie frei malen"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d5933cc7-7f9d-46b2-a3a8-0929595b654b
  modified: 2026-11-12T15:31:20.857Z
---

Kevin (12.11.2026) lobte das Baerenfenster-Bild, weil es "exakt aus wie ingame" aussah; fruehere UI-Entwuerfe (frei gemalt) sahen "immer komplett anders aus wie in der realitaet ingame".

**Why:** Nur ein Bild, das aus dem echten Code entsteht, zeigt Kevin, was er wirklich bekommt; frei gemalte Entwuerfe enttaeuschen ihn.

**How to apply:** Fuer jede neue UI: den echten Fenster-Code unter Lua 5.1 mit Attrappen von Vanillas ISPanel/ISButton laufen lassen, jeden drawRect/drawText/drawTextureScaled mitschreiben (Vorbild `_arbeit/baer_zaehmen/attrappe/f1_ober/zeichne_dump.lua`) und mit Python/PIL mit den echten Spielschriften (Vanilla media/fonts BMFont) und echten UI-Bildern ueber Kevins Spielbild malen (`_arbeit/baer_zaehmen/f1_entwurf/zeichne_gebaut.py`). Vor dem Bau darf ein Entwurf frei sein, muss aber dieselben Schriften/Masse nutzen und als Entwurf markiert sein. Siehe [[kevin-vorlage-ist-massstab]].
