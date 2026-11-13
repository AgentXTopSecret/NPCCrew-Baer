---
name: cpu-voll-nutzen-ok
description: "Kevin erlaubt, dass Laeufe die CPU voll auslasten (z. B. 26 Python-Rechenprozesse); nicht deckeln, nicht nachfragen"
metadata:
  node_type: memory
  type: feedback
  originSessionId: cccbd9d6-dd89-4eba-8fad-b3beed093bcb
  modified: 2026-11-13T18:15:17.884Z
---

Kevin fragte am 13.11.2026, ob der Workflow seine CPU "auseinandernimmt" (Liegen-Lauf: Posen-Suche mit 26 Python-Prozessen, CPU 100 %). Auf den Vorschlag, Rechnungen kuenftig auf die halbe CPU und niedrige Prioritaet zu begrenzen: *"nein mach so weiter"*.

**Why:** Ihm ist Tempo der Laeufe wichtiger; die volle CPU-Last stoert ihn nicht (sein PC: Ryzen 9 7950X3D, 32 Threads, RTX 4090).

**How to apply:** Agenten-Auftraege nicht auf weniger Worker deckeln. Fragt er wieder nach Last: erklaeren, was rechnet; niedrige Prioritaet setzen ist harmlos, aber nicht noetig. Renders bleiben auf der GPU. Verwandt: [[zwei-spuren-immer-weiter]].
