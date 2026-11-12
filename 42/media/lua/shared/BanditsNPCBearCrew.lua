--
-- NPC Crew -- Baer, Naht-Datei (PLAN_ZAEHMEN.md 12.2). Die EINZIGE Stelle, an der der Baer NPC Crew beruehrt.
--
-- Regel: alles zur Laufzeit, in Events.OnGameBoot, hinter Existenz-Riegel, genau einmal; keine NPC-Crew-Datei wird geaendert.
-- Grund fuer OnGameBoot: NPC Crew setzt seine Tabellen auf Dateiebene; ein Eintrag davor ginge verloren, und nach der
-- Uebernahme laden die Baer-Dateien VOR BanditsNPCLivestock*.lua (alphabetisch).
--
-- Naht 1, Tierpflege: NPC Crews Tierpflege behandelt jedes Tier in einer ihrer Tierzonen als Vieh (zaehlen, Schlachtplan),
-- dessen GRUPPE nicht in BanditsNPC.Livestock.NOT_TENDED steht (NPC Crew shared/BanditsNPCLivestock.lua:5152, Schluessel =
-- Gruppe; "grep -rn NOT_TENDED 42/media/lua" am 10.11.2026: 24 Treffer in 9 Dateien, davon 14 Code-Zeilen in 8 Dateien, der Rest
-- Kommentare; alle Leser fragen zur Laufzeit). Ein Baer ist kein Vieh: die Gruppe "ncbear" eintragen.
-- F2 (PLAN_F2.md 1.4): die alte Gruppe "bear" des frueheren Test-Baeren gehoert nicht zu NPC Crew; die Test-Mod traegt sie bei sich
-- selbst ein.
--
-- Ohne NPC Crew tut diese Datei nichts. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local installed = false

local function install()
    if installed then return end
    installed = true
    local crew = BanditsNPC.Livestock
    if crew == nil then return end                    -- NPC Crew ist nicht da: nichts zu tun
    if type(crew.NOT_TENDED) ~= "table" then
        -- NPC Crew ist da, aber das Feld fehlt: laut melden, sonst zaehlt die Tierpflege Baeren still als Vieh.
        if B.Err then B.Err("seam 1: BanditsNPC.Livestock.NOT_TENDED is missing, bears would count as livestock") end
        return
    end
    crew.NOT_TENDED[B.GROUP or "ncbear"] = true
    if B.Log then B.Log("seam 1: the bear group is not tended livestock") end
end

-- Events.OnGameBoot.Add: Vanilla client/Foraging/ISSearchManager.lua:1481.
Events.OnGameBoot.Add(install)
