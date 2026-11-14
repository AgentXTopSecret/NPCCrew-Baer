if isClient() then return end      -- Vanilla server/Traps/STrapSystem.lua:1: laeuft im Einzelspieler und auf dem Server

--
-- NPC Crew -- Baer, Talente beim Schreiber (Lauf baer-talente, baer/plaene/PLAN_TALENTE.md 4, 8; Kevins Antworten 14.11.2026 ~10:20,
-- baer/begleiter/ENTSCHEIDUNGEN.md -- sie gehen vor dem Plan).
--
-- Kevin 14.11.2026: "im skilltree auf einen extra tab kann man die skillpunkte aisgeben und per knopf altivieten dann leuchtet der skill hell und
-- ist permanent altiv" -- "skills vergeben muss bestaetigt werden beim klicken" -- "skill reset ist erlaubt pro sandbox setting, nur 1x taeglich
-- auch per sandbox einstellbar" -- "standardmaessig aber nicht erlaubt"; ~10:20 "Freie Wahl", Reset "Alle auf einmal".
--
-- Nur der Schreiber entscheidet (Einzelspieler: dasselbe Programm; Mehrspieler: der Server). Der Client fragt erst im Vanilla-Ja/Nein-Fenster
-- und bittet dann B.Ask(player, "Talent", { id, k }) bzw. "TalentReset" { id } -- geglaubt wird nur die Benennung (Eintrag, Schluessel), nie
-- eine Punktzahl oder ein Zustand. Rolle "user" genuegt (sendClientCommand wie jede Baeren-Bitte) -> kein Kick, kein Admin-Weg.
-- Die Regeln (verdiente Punkte, darf er lernen, Reset-Uhr) stehen REIN in shared/BanditsNPCBearTalentRules.lua -- der Client rechnet mit
-- denselben Funktionen auf seinem Sicht-Eintrag.
-- Gespeichert: rec.tal (Text "alert,paw"), rec.talR (Spieltag des letzten Resets), rec.talN (zuletzt gemeldete Punktzahl: jede Meldung genau
-- einmal, auch nach Laden/Absturz). Alle drei auch im Spiegel am Tier (server/BanditsNPCBearHeal.lua MARK_FIELDS) -- B.TalentFromMark kuerzt
-- beim Wiederherstellen auf die verdienten Punkte (im Mehrspieler ist g dort schon gedeckelt, server/BanditsNPCBearGrow.lua B.GrowFromMark).
-- Kein Talent beruehrt einen Gegenstand (Lasttier-Reset bei voller Last: nichts faellt heraus, er nimmt nur nichts mehr an).
--
-- Kein neuer Engine-Aufruf: getTimestampMs (Vanilla server/Foraging/forageServer.lua:456); alles andere ueber vorhandene Baeren-Funktionen
-- (B.Reg, B.PlayerKey, B.AskOk, B.Commit, B.Tell, B.PushView, B.FlushViews, B.PlayerByKey, B.Opt, B.Now, B.NoteBd, B.Touch, B.Ses).
-- Ladefolge: server/ alphabetisch nach ...Sleep, vor ...World -- fremde Funktionen nur zur Laufzeit. Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear

local function note(k, t, v, tone)
    return { k = k, t = t, v = v, tone = tone }
end

local function num(v)
    local n = tonumber(v)
    if n == nil or n ~= n then return nil end
    return n
end

-- Regeln geladen? (shared/BanditsNPCBearTalentRules.lua; fehlt sie -- Teilkopie --, tut jeder Weg hier nichts)
local function rulesOk()
    return type(B.TALENT_IX) == "table" and B.TalentCan ~= nil and B.TalentFix ~= nil and B.TalentList ~= nil and B.TalentEarned ~= nil
        and B.TalentResetLeft ~= nil
end

local function isTame(st)
    return st == "tame" or st == "missing"
end

-- Ablehnung: Drossel je "Spieler|<Befehl>|no" (B.AskOk, server/BanditsNPCBearFollow.lua), dann Meldung und frische Sicht (die Kacheln stimmen
-- danach wieder mit dem Schreiber ueberein).
local function refuse(player, pkey, cmd, ms, n)
    if B.AskOk(pkey .. "|" .. cmd .. "|no", ms) then
        B.Tell(player, n)
        B.PushView(player)
    end
end

-- Grund aus B.TalentCan -> Meldung
local WHY = {
    max = "UI_BN_Bear_Why_TalentMax", have = "UI_BN_Bear_Why_TalentHave", soon = "UI_BN_Bear_Why_TalentSoon",
    point = "UI_BN_Bear_Why_TalentPoint",
}

-- Eintrag des Bittenden: rec oder nil (nach einer Ablehnung). Gemeinsam fuer beide Bitten.
local function ownRec(player, pkey, args, cmd, ms)
    local reg = B.Reg()
    if not reg then return nil end
    local rec = reg.cubs[args.id]
    if rec == nil then
        refuse(player, pkey, cmd, ms, note("UI_BN_Bear_Why_Gone", nil, nil, "bad"))
        return nil
    end
    if rec.owner ~= pkey or not isTame(rec.st) then
        refuse(player, pkey, cmd, ms, note("UI_BN_Bear_Why_NotOwner", nil, nil, "bad"))
        return nil
    end
    return rec
end

-- ---------------------------------------------------------------------------
-- Bitte "Talent" { id = <Text>, k = <Schluessel> }. Unsinn (kein Text, unbekanntes Talent) wird still verworfen. Ein vermisster Baer darf lernen
-- (es braucht keinen Koerper). Zwei schnelle Klicks: die zweite Pruefung von B.TalentCan ("have" / "point" / "max") -- der Schreiber arbeitet jede
-- Bitte ganz ab (rec.tal ist schon geschrieben, wenn die naechste kommt). Nachbesserung C2: KEINE Drossel "|Talent|ok" mehr -- sie verwarf eine
-- zweite GUELTIGE Bitte (anderes Talent, freier Punkt) innerhalb von askMs still (im Mehrspieler mit Verzoegerung moeglich: zwei Ja kurz
-- nacheinander). Jedes Lernen verbraucht einen verdienten Punkt, mehr als talMax (3) geht nie -- Spam ist so von selbst gedeckelt; Ablehnungen
-- bleiben ueber refuse gedrosselt ("|Talent|no").
-- ---------------------------------------------------------------------------
function B.HandleTalent(player, args)
    if not player or not B.IsWriter() or not rulesOk() then return end
    if type(args) ~= "table" or type(args.id) ~= "string" then return end
    local k = args.k
    if type(k) ~= "string" or B.TALENT_IX[k] == nil then return end
    local pkey = B.PlayerKey(player)
    if pkey == nil then return end
    local ms = getTimestampMs()
    local rec = ownRec(player, pkey, args, "Talent", ms)
    if rec == nil then return end
    B.TalentFix(rec)
    local ok, why = B.TalentCan(rec, k)
    if not ok then
        refuse(player, pkey, "Talent", ms, note(WHY[why] or "UI_BN_Bear_Why_TalentPoint", nil, nil, "bad"))
        return
    end
    local list = B.TalentList(rec)
    list[#list + 1] = k
    rec.tal = table.concat(list, ",")
    B.TalentFix(rec)
    B.Commit(rec)
    B.Tell(player, note("UI_BN_Bear_Note_TalentLearned", "talent", k, "good"))
    B.Log("talent: " .. tostring(rec.id) .. " learned " .. k .. " (" .. tostring(rec.tal) .. ", earned " .. tostring(B.TalentEarned(rec))
        .. ") for " .. tostring(pkey))
    B.FlushViews()
end

-- ---------------------------------------------------------------------------
-- Bitte "TalentReset" { id = <Text> }: nur, wenn die Sandbox es erlaubt (BearTalentReset, Vorgabe AUS), etwas gelernt ist und der Abstand
-- BearTalentResetDays (Spieltage, 0 = jederzeit) um ist. Setzt ALLE zurueck (Kevin ~10:20), merkt den Spieltag. Beruehrt nichts anderes: Leben-
-- und Ausdauer-Anteil, Inventar, Erfahrung bleiben (Dickes Fell weg: 325/650 -> 200/400; Lasttier weg bei voller Last: nur "zu schwer").
-- ---------------------------------------------------------------------------
function B.HandleTalentReset(player, args)
    if not player or not B.IsWriter() or not rulesOk() then return end
    if type(args) ~= "table" or type(args.id) ~= "string" then return end
    local pkey = B.PlayerKey(player)
    if pkey == nil then return end
    local ms = getTimestampMs()
    local rec = ownRec(player, pkey, args, "TalentReset", ms)
    if rec == nil then return end
    if B.Opt("BearTalentReset") ~= true then
        refuse(player, pkey, "TalentReset", ms, note("UI_BN_Bear_Why_TalentResetOff", nil, nil, "bad"))
        return
    end
    B.TalentFix(rec)
    if #B.TalentList(rec) == 0 then
        refuse(player, pkey, "TalentReset", ms, note("UI_BN_Bear_Why_TalentNone", nil, nil, "bad"))
        return
    end
    local now = B.Now()
    local left = B.TalentResetLeft(rec, now, B.Opt("BearTalentResetDays"))
    if left > 0 then
        refuse(player, pkey, "TalentReset", ms, note("UI_BN_Bear_Why_TalentResetWait", "wait", left, "bad"))
        return
    end
    if not B.AskOk(pkey .. "|TalentReset|ok", ms) then return end
    local was = rec.tal
    rec.tal = nil
    rec.talR = math.floor(now / 24)
    B.TalentFix(rec)
    B.Commit(rec)
    B.Tell(player, note("UI_BN_Bear_Note_TalentReset", "num", B.TalentFree(rec), "good"))
    B.Log("talent: " .. tostring(rec.id) .. " reset (" .. tostring(was) .. ") on day " .. tostring(rec.talR) .. " for " .. tostring(pkey))
    B.FlushViews()
end

-- ---------------------------------------------------------------------------
-- Langsam-Takt (aus slowTickBody, eigene Schleife NACH B.NeedsSlow, server/BanditsNPCBearServer.lua): nur gezaehmt, Besitzer im Spiel.
-- Mehr verdiente Punkte als rec.talN -> EINE Meldung "Talentpunkt" (nur, wenn wirklich einer frei ist), talN merken, Commit. talN ist ein
-- Hoechststand: es sinkt nie (g sinkt im Spiel nie; nur ein Probeweg setzt g) -- so kommt jede Meldung genau einmal, auch nach g runter / rauf, Laden und
-- Absturz (talN steht im Spiegel). Dazu: laeuft eine Reset-Wartezeit, geht je volle Stunde Rest eine frische Sicht hinaus (sonst bliebe der
-- Knopf "Zuruecksetzen" grau, bis zufaellig etwas anderes die Sicht erneuert).
-- ---------------------------------------------------------------------------
function B.TalentSlow(rec, now, players)
    if type(rec) ~= "table" or rec.st ~= "tame" or rec.owner == nil or not rulesOk() then return end
    local p = B.PlayerByKey(rec.owner, players)
    if p == nil then return end
    now = num(now) or B.Now()
    local n = B.TalentEarned(rec)
    local was = num(rec.talN) or 0
    if n > was then
        rec.talN = n
        local free = B.TalentFree(rec)
        if free > 0 then
            B.Tell(p, B.NoteBd(note("UI_BN_Bear_Note_TalentPoint", "num", free, "good"), rec))
            B.Log("talent: " .. tostring(rec.id) .. " earned perk point " .. tostring(n) .. " (" .. tostring(free) .. " free)")
        end
        B.Commit(rec)
    end
    if rec.talR ~= nil and B.Opt("BearTalentReset") == true then
        local left = B.TalentResetLeft(rec, now, B.Opt("BearTalentResetDays"))
        local s = B.Ses(rec.id)
        local h = math.ceil(left - 0.000001)
        if h < 0 then h = 0 end
        if s.talWh ~= nil and s.talWh ~= h then B.Touch(rec) end
        if h > 0 then s.talWh = h else s.talWh = nil end
    end
end

-- ---------------------------------------------------------------------------
-- Sicht (aus viewEntry, server/BanditsNPCBearRegistry.lua): NUR fuer den Besitzer, nur tame/missing. Schreibt nur in t (flach):
-- tal (Text, fehlt = nichts gelernt), talE (verdient 0..3), talNx (Spieltage bis zum naechsten Punkt, fehlt bei 3), talRo (Reset laut
-- Server-Sandbox erlaubt), talRw (Stunden bis Reset wieder geht, eine Nachkommastelle, nur > 0), talRd (Tage zwischen zwei Resets).
-- Der Eintrag wird hier NICHT veraendert (B.TalentList bereinigt nur die Kopie).
-- ---------------------------------------------------------------------------
function B.TalentView(rec, t, pkey, now)
    if type(rec) ~= "table" or type(t) ~= "table" or not rulesOk() then return end
    if pkey == nil or rec.owner ~= pkey or not isTame(rec.st) then return end
    local list = B.TalentList(rec)
    if #list > 0 then t.tal = table.concat(list, ",") end
    t.talE = B.TalentEarned(rec)
    if B.TalentNextDays then t.talNx = B.TalentNextDays(rec) end
    local days = B.Opt("BearTalentResetDays")
    t.talRd = days
    if B.Opt("BearTalentReset") == true then
        t.talRo = true
        local left = B.TalentResetLeft(rec, num(now) or B.Now(), days)
        if left > 0 then
            local r = math.ceil(left * 10 - 0.000001) / 10
            if r < 0.1 then r = 0.1 end
            t.talRw = r
        end
    end
end

-- Text der Talente ohne den Schluessel k (Nachbesserung C3): Teile durch Komma, zeichenweise ohne Muster wie parse in
-- shared/BanditsNPCBearTalentRules.lua (Kahlua ist kein echtes Lua 5.1), hoechstens 200 Zeichen. Rueckgabe: Text, ob k darin war.
local function dropKey(text, k)
    if type(text) ~= "string" then return text, false end
    local n = string.len(text)
    if n > 200 then n = 200 end
    local keep, start, hit = {}, 1, false
    for i = 1, n + 1 do
        local ch = ""
        if i <= n then ch = string.sub(text, i, i) end
        if i > n or ch == "," then
            local part = string.sub(text, start, i - 1)
            start = i + 1
            if part == k then
                hit = true
            elseif part ~= "" then
                keep[#keep + 1] = part
            end
        end
    end
    if not hit then return text, false end
    return table.concat(keep, ","), true
end

-- ---------------------------------------------------------------------------
-- Aus dem Spiegel (server/BanditsNPCBearHeal.lua, nur fuer einen gezaehmten Eintrag, NACH B.GrowFromMark -- g ist dann schon geklemmt bzw. im
-- Mehrspieler gedeckelt). how "restore" (B.Restore) und "newer" (B.TakeNewerMark, nur Einzelspieler: der neuere Spiegel ist die Wahrheit) --
-- beide: tal / talR / talN aus dem Spiegel, bereinigt (B.TalentFix), auf die verdienten Punkte gekuerzt (B.TalentCut, R2), talR hoechstens
-- heute, talN hoechstens verdient.
-- ---------------------------------------------------------------------------
function B.TalentFromMark(rec, mark, how)
    if type(rec) ~= "table" or type(mark) ~= "table" or not rulesOk() then return end
    if how ~= "restore" and how ~= "newer" then return end
    rec.tal = nil
    if type(mark.tal) == "string" then rec.tal = mark.tal end
    -- Nachbesserung C3: ein Spiegel bringt kein gesperrtes Talent mit -- der Angler ist bis F5 "kommt spaeter" (B.TalentCan "soon",
    -- B.CFG.talFishOn ~= true); im Mehrspieler kann ein Client die ModData eines Tiers schreiben (server/BanditsNPCBearHeal.lua B.TakeNewerMark).
    -- VOR dem Bereinigen gestrichen (wie ein unbekannter Schluessel), damit er keinen der 3 Plaetze belegt.
    local dropped = false
    if not (B.CFG and B.CFG.talFishOn == true) then rec.tal, dropped = dropKey(rec.tal, "fisher") end
    rec.talR = num(mark.talR)
    rec.talN = num(mark.talN)
    B.TalentFix(rec)
    if dropped then
        B.Err("heal: " .. tostring(rec.id) .. " -- the locked perk fisher from the mark dropped (comes with a later version)")
    end
    local today = math.floor(B.Now() / 24)
    if rec.talR ~= nil and rec.talR > today then rec.talR = today end
    local cut = B.TalentCut(rec)
    if cut > 0 then
        B.Err("heal: " .. tostring(rec.id) .. " -- " .. tostring(cut) .. " perk(s) from the mark dropped (more than its growth earned)")
    end
    local earned = B.TalentEarned(rec)
    if rec.talN ~= nil and rec.talN > earned then rec.talN = earned end
end

-- ---------------------------------------------------------------------------
-- PROBEWEGE (nur die Probe-Datei der Test-Mod ruft sie; im kopierten Code ruft sie niemand -- Tier-Regel "probeweg" des
-- Uebernahme-Skripts). B.TalentForce: Talente ohne Punkte setzen (bereinigt, hoechstens talMax). B.TalentWipe: Reset ohne Sandbox und Uhr.
-- ---------------------------------------------------------------------------
function B.TalentForce(rec, text)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return nil end
    rec.tal = nil
    if type(text) == "string" then rec.tal = text end
    B.TalentFix(rec)
    B.Commit(rec)
    return rec.tal
end

function B.TalentWipe(rec)
    if type(rec) ~= "table" or not isTame(rec.st) or not rulesOk() then return end
    rec.tal, rec.talR = nil, nil
    B.Commit(rec)
end
