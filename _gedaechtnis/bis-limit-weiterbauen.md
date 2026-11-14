---
name: bis-limit-weiterbauen
description: "Kevin 14.11.: ohne Pause weiterbauen bis das Limit den Lauf abbricht; schreibt er danach, abgebrochenen Workflow verlustfrei fortsetzen (resumeFromRunId) und weiter"
metadata:
  type: feedback
---

Kevin 14.11.2026 ~10:55, woertlich: *"bau noch weiter ohne pause und ganz normal wie immer einfach bis es abbricht und du merkst dir dann immer wenn ich was schreibe und der workflow ist abgebrochen stellst du ihn wieder her ohne verlust und es geht weiter okay?"*

**Why:** Er will das Wochenlimit voll ausnutzen statt bei 98 % zu stoppen (die 98-%-Regel mit Herunterfahren galt nur fuer die Nacht 13./14.11.).

**How to apply:** Laeufe normal weiterfuehren (zwei Spuren, [[zwei-spuren-immer-weiter]]), keinen 98-%-Waechter mehr. Bricht ein Workflow wegen des Limits ab: Run-ID und Skriptpfad in baer/STAND.md oben notieren. Sobald Kevin wieder schreibt, zuerst pruefen, ob ein Lauf abgebrochen ist, und ihn mit `Workflow({scriptPath, resumeFromRunId})` fortsetzen (fertige Agenten kommen aus dem Cache) -- nur in derselben Sitzung moeglich; in einer neuen Sitzung ein Fortsetzungs-Skript nach dem Vorbild baer/spiel/f2_fortsetzung.js. Danach seine Nachricht beantworten.
