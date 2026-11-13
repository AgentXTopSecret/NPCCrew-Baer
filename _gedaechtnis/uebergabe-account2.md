---
name: uebergabe-account2
description: Kontowechsel Baer -- zuerst baer/STAND.md (oberster Block) und baer/UEBERGABE_ACCOUNT2.md lesen; seit 13.11. laufen baer-f3 und baer-liegen in Sitzung cccbd9d6
metadata:
  node_type: memory
  type: project
  originSessionId: cccbd9d6-dd89-4eba-8fad-b3beed093bcb
  modified: 2026-11-13T14:05:44.131Z
---

Kevin wechselt zwischen zwei Claude-Accounts. Die Uebergabe steht in `C:\Users\Kevin\NPCCrew-Nebenprojekte\baer\UEBERGABE_ACCOUNT2.md` (FINAL 13.11.2026 ~01:00 aus Sitzung d5933cc7, mit Nachtrag 13.11. ~15:20); der neueste Stand steht immer im obersten Block von `baer\STAND.md`.

Stand 13.11.2026 ~15:20 (Sitzung cccbd9d6, erster Account, Woche frisch): Kevin hat die F3-Fragen einzeln beantwortet (woertlich in `baer\begleiter\ENTSCHEIDUNGEN.md` unten und `_arbeit\baer_zaehmen\f3\KEVIN_ANTWORTEN.md`), Maul "Lippenlinie darf rein", Modell-Reihenfolge Liegen/Tot -> Maul-Nachbesserung -> Schlafpose. Gestartet: `baer-f3` (wf_36e98ba8-469, `baer\spiel\f3_workflow.js`) und `baer-liegen` (wf_c0a986cb-3dd, `baer\spiel\liegen_workflow.js`).

**Why:** `resumeFromRunId` gilt nur in der Sitzung, die den Lauf gestartet hat; ein neuer Account muss mit Fortsetzungs-Skripten weitermachen (Vorbild `baer/spiel/f2_fortsetzung.js`).

**How to apply:** Neue Sitzung: zuerst STAND.md oben, dann UEBERGABE_ACCOUNT2.md, dann ENTSCHEIDUNGEN.md unten. Kevins "mach weiter" (13.11.) hat den Halt vom 12.11. aufgehoben; es gilt wieder [[zwei-spuren-immer-weiter]]. Fragen an Kevin einzeln per Auswahl-Dialog stellen (er aendert Empfehlungen gern im Freitext). Siehe [[ui-vorschau-aus-echtem-code]].
