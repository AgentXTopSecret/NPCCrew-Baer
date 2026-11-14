--
-- NPC Crew -- Baer, "z Z z" ueber dem schlafenden Baeren (F3, Lauf baer-f3, PLAN_F3.md 8; Kevin 08.11.2026: "ein aufsteigendes zZz ...
-- klein-gross-klein", "im Mehrspieler sieht es jeder"; Kevin 13.11.2026, f3/KEVIN_ANTWORTEN.md Antwort 5: "Hellblau, ueber dem Kopf").
--
-- Reine Anzeige auf jedem Client (Einzelspieler und Mehrspieler gleich; der dedizierte Server laedt client/ nicht): gezeichnet wird ueber
-- jedem gezaehmten Baeren, dessen Sicht-Eintrag schlaeft (slp, vom Schreiber) UND dessen Schlaf-Schleife an der lebenden Kopie DIESES
-- Clients schon laeuft (U.PoseSleeping, client/BanditsNPCBearPose.lua) -- eigene und fremde Baeren. Nichts wird gesendet oder gespeichert.
--   * Kein eigenes Element: U.ZzDraw(self, now) wird aus der vorhandenen prerender der Anzeige gerufen (client/ISUI/BanditsNPCBearHud.lua,
--     direkt nach U.FloatDraw, hinter Existenz-Riegel) -- gezeichnet wird mit DEREN 1 x 1-Element in Bildschirm-Koordinaten. Bei
--     geteiltem Bildschirm kommt der Aufruf nie (die Anzeige zeichnet dann nichts).
--   * Liste hoechstens 1 x je Sekunde (und sofort, wenn der Schlaf-Treiber eine Schleife beginnt oder beendet: U.ZzPoke): Sicht-Eintraege
--     mit slp, lebende Kopie aus U.CubObj (kein eigener Suchlauf), gleiche Ebene wie der Spieler, in B.CFG.hudDist Kacheln, Deckel
--     B.CFG.hudMax. Dort wird EINMAL je Sammlung gefragt, wohin der Baer schaut (siehe JAR-AUSNAHME), und die Hoehe des Schild-Stapels
--     geholt (U.TagTop) -- waehrend er schlaeft, dreht er sich nicht.
--   * Je Bild und Baer: drei Umrechnungen (Kopf waagerecht und senkrecht, Tiermitte senkrecht), drei Buchstaben mit Schatten
--     (6 Textaufrufe), waehrend EINES Glyphen-Wechsels 2 mehr (8). Keine Tabelle, kein getText, keine Suche je Bild.
--   * Bild: drei Buchstaben gleichzeitig, jeder lebt 2,4 s, versetzt um 0,8 s; sie steigen schraeg nach rechts (2,4 x Schrifthoehe hoch,
--     0,5 x seitlich, leichtes Pendeln) und werden weich ein- und ausgeblendet (Kurve aus _arbeit/baer_schlaf/zz/zz_kurve.lua).
--     "klein-gross-klein" OHNE drawTextZoomed (kein Vanilla-Aufrufer, Kevin Antwort 5: nicht noetig): jeder Buchstabe ist unten ein "z" in
--     Schrift A, in der Mitte ein "Z" in Schrift B (eine Stufe groesser), oben wieder "z" -- an den zwei Uebergaengen 0,2 s Ueberblenden
--     (beide Glyphen mit gegenlaeufiger Deckkraft). Schriften nach der Anzeige-Option "TagSize": 100 -> Small / Medium, 150 -> Medium /
--     Large, 200 -> Large / Large. Weil die drei Buchstaben um ein Drittel ihres Lebens versetzt sind UND das grosse "Z" samt beider
--     Uebergaenge genau das mittlere Drittel fuellt (UP_AT 0,375 / DOWN_AT 0,625, Nachbesserung P1), steht immer nur EIN grosses "Z" in
--     der Saeule: sie liest sich von unten nach oben wie "z Z z" (mit 0,28 / 0,72 standen in einem Drittel der Bilder zwei grosse Z).
--   * Anker: waagerecht ueber dem KOPF (Tiermitte + Blickrichtung x Kopf-Vorlage, auf Kopfhoehe = Schild-Anker U.TagLift); senkrecht
--     dort -- oder hoeher, naemlich ueber dem Schild-Stapel dieses Baeren (U.TagTop: Werte-Zeilen, Zustand, Name, Herz ueber der
--     Tiermitte), damit die Buchstaben nie durch Name und Zustand laufen (schaut er zur Kamera, liegt der Kopf im Bild UNTER dem
--     Schild). Regler zur Laufzeit:
--     U.ZZ.lift (Pixel) und U.ZZ.head (Kopf-Vorlage in Modell-Einheiten; nil = B.CFG.zzHeadE, Rueckfall 0,30 fuer das Ersatzbild
--     Sitzen -- den Liege-Wert misst der Modell-Lauf F3b). Im Spiel stellt sie niemand; diese Datei bietet keinen Befehl dafuer an.
--   * Farbe: die EINE Schlaf-Farbe (U.SleepColor = B.CFG.sleepCol, Hellblau), dunkler Schatten wie das Namensschild.
--   * Wann: 0,5 s nach Beginn der Schlaf-Schleife beginnt der erste Buchstabe; beim Wecken entstehen keine neuen, alles blendet in 0,6 s
--     aus. Eigene Uhr, die in der Pause steht (isGamePaused). Schalter je Spieler "TagSleep" (Optionen -> Mods, Vorgabe an).
--
-- JAR-AUSNAHME (Kevins Wort 13.11.2026, Antwort 5 -- genau dieser EINE Aufruf, nur hier): animal:getForwardDirection() am Tier.
--   Klasse.Methode: zombie.characters.IsoGameCharacter.getForwardDirection() -> zombie.iso.Vector2 (javap -c, Spiel 42.22: Offset 0
--   aload_0, 1 getfield forwardDirection, 4 areturn); zombie.characters.animals.IsoAnimal extends IsoPlayer extends IsoLivingCharacter
--   extends IsoGameCharacter und ueberschreibt sie nicht. In Vanilla-Lua nur am Spieler belegt (V:client/Foraging/ISBaseIcon.lua:216,
--   V:shared/Fishing/FishingRod.lua:286), in Bandits am Zombie (B:shared/ZombieActions/ZAPush.lua:37) -- am Tier ohne Lua-Fundstelle.
--   Die Rueckgabe wird mit :getX() / :getY() gelesen (belegt: B:shared/ZombieActions/ZAPush.lua:38, B:shared/Bandit.lua:1454-1455).
--   Ob die Vorwaertsrichtung eines ruhenden Tiers der Blickrichtung des Modells entspricht, ist ungespielt (Regler U.ZZ.head = 0 setzt das
--   z Z z ueber die Tiermitte).
-- K1 (PLAN_K1.md 3, 6): das z Z z hebt sich mit derselben Pose wie das Schild (U.PoseLift); U.SleepReport meldet im Einzelspieler auch das
--   VORSPULEN (Spieltempo > 1) als Schlaf des Besitzers -- dann legt sich der Baer ebenfalls hin (Kevin 14.11. ~01:10).
-- Dazu, ohne Zeichnen (PLAN_F3.md 6.7; Kevin 13.11.2026 Antwort 6d "er legt sich neben den Spieler, wenn der schlaeft"): U.SleepReport(now)
--   meldet dem Schreiber, wenn der Besitzer einschlaeft bzw. aufwacht -- Bitte "Sleep" { on } ueber B.Ask (Einzelspieler B.Handle direkt,
--   Mehrspieler sendClientCommand, Rolle user genuegt). Einen belegten Lua-Weg, auf dem der Server den Schlaf eines Spielers erfaehrt,
--   hat Vanilla nur fuer das Schlafen im FAHRZEUG ("onVehicleSleep", V:client/ISUI/ISWorldObjectContextMenu.lua:1098 ->
--   V:server/ClientCommands.lua:658-661). Gerufen aus U.PoseTick (client/BanditsNPCBearPose.lua, hinter Existenz-Riegel), selbst auf 1 x je
--   Sekunde gedrosselt; gesendet nur bei Wechsel und je 30 s waehrend des Schlafs (der Schreiber vergisst die Meldung nach 90 s) und nur,
--   wenn die Sicht einen eigenen gezaehmten Baeren traegt. Eine falsche Meldung legte hoechstens den EIGENEN Baeren hin.
-- Alle anderen Engine-Aufrufe haben eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

local LIST_MS = 1000        -- Liste hoechstens so oft neu (ausser U.ZzPoke)
local LIFE_MS = 2400        -- Leben eines Buchstabens
local STEP_MS = 800         -- Versatz der drei Buchstaben (= ein Drittel des Lebens)
local LETTERS = 3
local IN_MS = 500           -- so lange nach Beginn der Schlaf-Schleife beginnt der erste Buchstabe
local OUT_MS = 600          -- so schnell blendet alles aus, wenn er aufwacht
local FADE_IN = 0.15        -- Anteil des Lebens: weich ein
local FADE_OUT = 0.35       -- Anteil des Lebens: weich aus
-- Nachbesserung P1: das grosse "Z" fuellt mit seinen zwei Uebergaengen (je 2 x BLEND = 1/12 des Lebens) genau das mittlere Drittel
-- 1/3 .. 2/3 -- bei drei um 1/3 versetzten Buchstaben steht so immer hoechstens EIN "Z", und nie wechseln zwei Buchstaben zugleich.
local UP_AT = 0.375         -- Anteil des Lebens: Mitte des Uebergangs "z" -> "Z" (beginnt bei 1/3)
local DOWN_AT = 0.625       -- Anteil des Lebens: Mitte des Uebergangs "Z" -> "z" (endet bei 2/3)
local BLEND = 0.2 * 1000 / LIFE_MS / 2      -- halbe Breite eines Uebergangs (0,2 s) als Anteil des Lebens
local RISE_K = 2.4          -- Aufstieg in Schrifthoehen (der grossen Schrift)
local SIDE_K = 0.5          -- Drift nach rechts in Schrifthoehen
local SWAY_K = 0.12         -- Pendeln in Schrifthoehen
local MAX_DT = 100          -- die eigene Uhr laeuft je Bild hoechstens so viele ms weiter (kein Sprung nach einem Haenger)
local HEAD_E = 0.30         -- Rueckfall fuer B.CFG.zzHeadE (Kopf-Vorlage vor der Tiermitte in Modell-Einheiten, Ersatzbild Sitzen)
local E_TILES = 1.5         -- Modell-Einheiten x Groesse -> Kacheln (_arbeit/baer_schlaf/forschung_zz.md 3.3)
local HUD_DIST, HUD_MAX = 20, 6
local SIZE_MID, SIZE_BIG = 125, 175     -- Stufen von "TagSize" wie client/ISUI/BanditsNPCBearHud.lua
local SMALL, BIG = "z", "Z"

-- Regler zur Laufzeit (PLAN_F3.md 8, 13; Lehre NPC Crew "Regler gleich mitbauen"): lift = Pixel ueber dem Schild-Stapel, head =
-- Kopf-Vorlage in Modell-Einheiten (nil = Wert des Kerns bzw. Rueckfall). Im Spiel setzt sie niemand; nicht gespeichert.
U.ZZ = U.ZZ or { lift = 4, head = nil }

-- Alles, was das z Z z sich merkt (nur diese Sitzung). st: Kennung -> Zustand eines schlafenden Baeren; gedeckelt durch die Sicht
-- (Kennungen ohne Schlaf fallen nach dem Ausblenden heraus) und HUD_MAX gezeichnete.
local Z = { at = 0, poke = true, clock = 0, last = nil, st = {}, list = {}, n = 0, fa = nil, ha = 0, fb = nil, hb = 0,
    r = 0.70, g = 0.85, b = 1.00 }

-- Schalter je Spieler (fehlt client/BanditsNPCBearOptions.lua: an).
local function wanted()
    local opt = U.Opt
    if not opt then return true end
    return opt("TagSleep", true) ~= false
end

-- Schriften A (kleines "z") und B (grosses "Z") nach "TagSize" und ihre Hoehen -- einmal je Sammlung, nie je Bild.
-- getFontHeight(UIFont.Small): V:client/ISUI/Animal/ISAnimalUI.lua:4; UIFont.Medium: V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8;
-- UIFont.Large: V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6.
local function fonts()
    local size = 100
    if U.Opt then size = tonumber(U.Opt("TagSize", 100)) or 100 end
    local fa, fb = UIFont.Small, UIFont.Medium
    if size >= SIZE_BIG then
        fa, fb = UIFont.Large, UIFont.Large
    elseif size >= SIZE_MID then
        fa, fb = UIFont.Medium, UIFont.Large
    end
    local tm = getTextManager()
    local ha, hb = tm:getFontHeight(fa), tm:getFontHeight(fb)
    if type(ha) ~= "number" or ha <= 0 then ha = 19 end
    if type(hb) ~= "number" or hb <= 0 then hb = 29 end
    Z.fa, Z.ha, Z.fb, Z.hb = fa, ha, fb, hb
end

-- Lage eines schlafenden Baeren fuer die naechste Sekunde: Kopf-Versatz in Kacheln (Blickrichtung x Kopf-Vorlage x Groesse), Hoehe des
-- Schild-Ankers (U.TagLift, dieselbe Rechnung wie das Schild) und Hoehe des Schild-Stapels in Pixeln (U.TagTop) + Regler.
local function aim(e, a, c, id, headE)
    -- JAR-AUSNAHME (Kevins Wort 13.11.2026, Antwort 5; Kopf dieser Datei): zombie.characters.IsoGameCharacter.getForwardDirection(),
    -- javap -c Offset 0-4 (getfield forwardDirection, areturn); getX / getY der Rueckgabe: B:shared/ZombieActions/ZAPush.lua:38.
    local fd = a:getForwardDirection()
    local fx, fy = fd:getX(), fd:getY()
    local len = math.sqrt(fx * fx + fy * fy)
    local sz = tonumber(c.sz) or 1
    if sz ~= sz or sz <= 0 then sz = 1 end
    if sz > 2 then sz = 2 end
    local k = 0
    if len > 0.001 then k = headE * E_TILES * sz / len end
    e.hx, e.hy = fx * k, fy * k
    local lift = 0.18
    if U.TagLift then lift = tonumber(U.TagLift(c)) or lift end
    e.lift = lift
    local top = 0
    if U.TagTop then top = tonumber(U.TagTop(id)) or 0 end
    e.top = top
    e.gap = tonumber(U.ZZ.lift) or 0
end

-- Liste bauen (hoechstens 1 x je Sekunde). getSpecificPlayer(0): V:client/Farming/CFarmingSystem.lua:45; getX / getY / getZ am Spieler:
-- V:client/Fishing/TensionUI.lua:11-12; am Tier: V:client/TimedActions/ISContextualActions.lua:100.
local function collect(now)
    Z.at = now
    Z.poke = false
    local st = Z.st
    for _, e in pairs(st) do e.seen = false end
    local cfg = B.CFG or {}
    local cubs = B.View and B.View.cubs
    local player = getSpecificPlayer(0)
    if wanted() and U.Fresh and U.Fresh() and U.CubObj and U.PoseSleeping and type(cubs) == "table" and player then
        local reach = tonumber(cfg.hudDist) or HUD_DIST
        local px, py, pz = player:getX(), player:getY(), math.floor(player:getZ())
        local headE = tonumber(U.ZZ.head) or tonumber(cfg.zzHeadE) or HEAD_E
        for id, c in pairs(cubs) do
            if type(c) == "table" and c.st == "tame" and c.slp == true and c.ride ~= true and U.PoseSleeping(id) then
                local a = U.CubObj(id)
                if a ~= nil then
                    local dx, dy = a:getX() - px, a:getY() - py
                    if math.floor(a:getZ()) == pz and dx * dx + dy * dy <= reach * reach then
                        local e = st[id]
                        if e == nil then
                            e = { t0 = Z.clock + IN_MS }
                            st[id] = e
                        elseif e.endAt ~= nil then
                            e.t0, e.endAt = Z.clock + IN_MS, nil        -- wieder eingeschlafen: von vorn
                        end
                        e.seen, e.a, e.id = true, a, id             -- K1: id fuer U.PoseLift je Bild
                        aim(e, a, c, id, headE)
                    end
                end
            end
        end
    end
    -- Nicht mehr gesehen: ausblenden (keine neuen Buchstaben); fertig ausgeblendet: vergessen. Erst sammeln, dann loeschen.
    local max = tonumber(cfg.hudMax) or HUD_MAX
    local gone = nil
    local n = 0
    for id, e in pairs(st) do
        if not e.seen and e.endAt == nil then e.endAt = Z.clock end
        if e.endAt ~= nil and Z.clock - e.endAt >= OUT_MS then
            gone = gone or {}
            gone[#gone + 1] = id
        elseif n < max then
            n = n + 1
            Z.list[n] = e
        end
    end
    if gone then
        for i = 1, #gone do st[gone[i]] = nil end
    end
    for i = n + 1, #Z.list do Z.list[i] = nil end
    Z.n = n
    if n > 0 then
        fonts()
        if U.SleepColor then
            local r, g, b = U.SleepColor()          -- Mehrfachrueckgabe erst in Locals
            Z.r, Z.g, Z.b = r, g, b
        end
    end
end

-- Ein Glyph mit Schatten (wie das Namensschild: schwarz, 1 px versetzt). drawTextCentre(text, x, y, r, g, b, a, Schrift):
-- V:client/ISUI/ISUIElement.lua:1280; mit UIFont.Medium V:client/ISUI/ISFitnessUI.lua:204, mit UIFont.Large V:client/Chat/ISAlert.lua:35.
local function glyph(self, str, x, y, a, font)
    self:drawTextCentre(str, x + 1, y + 1, 0, 0, 0, 0.7 * a, font)
    self:drawTextCentre(str, x, y, Z.r, Z.g, Z.b, 0.95 * a, font)
end

-- Ein Buchstabe an der Stelle u (0..1) seines Lebens: Weg, Deckkraft, "z" oder "Z" (an den zwei Uebergaengen beide ueberblendet).
local function letter(self, sx, sy, u, fade)
    local a = fade
    if u < FADE_IN then a = a * (u / FADE_IN) end
    if 1 - u < FADE_OUT then a = a * ((1 - u) / FADE_OUT) end
    if a <= 0.01 then return end
    local hb = Z.hb
    local x = sx + math.floor(hb * (SIDE_K * u + SWAY_K * math.sin(2 * math.pi * u)) + 0.5)
    local y = sy - math.floor(hb * RISE_K * u + 0.5)
    local w = 0                                     -- Anteil des grossen "Z" (0 = nur "z", 1 = nur "Z")
    if u >= UP_AT + BLEND and u <= DOWN_AT - BLEND then
        w = 1
    elseif u > UP_AT - BLEND and u < UP_AT + BLEND then
        w = (u - (UP_AT - BLEND)) / (2 * BLEND)
    elseif u > DOWN_AT - BLEND and u < DOWN_AT + BLEND then
        w = 1 - (u - (DOWN_AT - BLEND)) / (2 * BLEND)
    end
    -- (x, y) ist die Unterkante der kleinen Zeile: der Buchstabe beginnt UEBER dem Anker; beide Glyphen haben dieselbe Mitte
    local ha = Z.ha
    if w < 1 then glyph(self, SMALL, x, y - ha, a * (1 - w), Z.fa) end
    if w > 0 then glyph(self, BIG, x, y - ha - math.floor((hb - ha) / 2), a * w, Z.fb) end
end

-- ---------------------------------------------------------------------------
-- U.ZzDraw(self, now): aus Hud:prerender (client/ISUI/BanditsNPCBearHud.lua). self = das 1 x 1-Element der Anzeige bei 0,0 (seine
-- Koordinaten sind Bildschirm-Koordinaten), now = getTimestampMs() dieses Bildes. Ohne schlafenden Baeren: ein Zeitvergleich, sonst nichts.
-- isoToScreenX/Y(Spielernummer, x, y, z): V:client/Fishing/TensionUI.lua:11-12; isExistInTheWorld: V:client/ISUI/Animal/ISAnimalUI.lua:15;
-- isGamePaused(): V:client/Foraging/ISSearchManager.lua:1462 (die eigene Uhr steht in der Pause).
-- ---------------------------------------------------------------------------
function U.ZzDraw(self, now)
    if Z.poke or now - Z.at >= LIST_MS or now < Z.at then collect(now) end
    if Z.n == 0 then
        Z.last = nil
        return
    end
    local last = Z.last
    Z.last = now
    if last ~= nil and now > last and not isGamePaused() then
        local dt = now - last
        if dt > MAX_DT then dt = MAX_DT end
        Z.clock = Z.clock + dt
    end
    local clock = Z.clock
    for i = 1, Z.n do
        local e = Z.list[i]
        local a = e.a
        if a ~= nil and a:isExistInTheWorld() then
            local fade = 1
            if e.endAt ~= nil then fade = 1 - (clock - e.endAt) / OUT_MS end
            if fade > 0 then
                -- K1 (PLAN_K1.md 3): derselbe Pose-Faktor wie das Schild (U.PoseLift, client/BanditsNPCBearPose.lua) -- ueber dem Schild bleiben
                local pk = 1
                if U.PoseLift then pk = tonumber(U.PoseLift(e.id, now)) or 1 end
                local ax, ay, z = a:getX(), a:getY(), a:getZ() + e.lift * pk
                local x, y = ax + e.hx, ay + e.hy
                local sx = math.floor(isoToScreenX(0, x, y, z))
                -- senkrecht: am Kopf, aber nie tiefer als die Oberkante des Schild-Stapels (der haengt ueber der Tiermitte)
                local sy = math.floor(isoToScreenY(0, x, y, z))
                local ty = math.floor(isoToScreenY(0, ax, ay, z)) - e.top
                if ty < sy then sy = ty end
                sy = sy - e.gap
                for k = 0, LETTERS - 1 do
                    local age = clock - e.t0 - k * STEP_MS
                    if age >= 0 then
                        local cyc = math.floor(age / LIFE_MS)
                        -- nach dem Wecken entstehen keine neuen Buchstaben: dieser Durchlauf muss vorher begonnen haben
                        if e.endAt == nil or e.t0 + k * STEP_MS + cyc * LIFE_MS <= e.endAt then
                            letter(self, sx, sy, (age - cyc * LIFE_MS) / LIFE_MS, fade)
                        end
                    end
                end
            end
        end
    end
end

-- Der Schlaf-Treiber (client/BanditsNPCBearPose.lua) meldet, dass eine Schlaf-Schleife begonnen oder geendet hat: Liste im naechsten Bild
-- neu (sonst bis zu 1 s Verzug). Reines Lua.
function U.ZzPoke()
    Z.poke = true
end

-- Zum Nachsehen (nur lesen): Zahl der gezeichneten Baeren und die eigene Uhr.
function U.ZzInfo()
    return Z.n, Z.clock
end

-- ---------------------------------------------------------------------------
-- Besitzer schlaeft (PLAN_F3.md 6.7; Kevin Antwort 6d). O.told = der Schreiber glaubt gerade, dass ich schlafe.
-- ---------------------------------------------------------------------------
local OWN_MS = 1000             -- so oft wird der eigene Schlaf gefragt
local OWN_RESEND_MS = 30000     -- im Schlaf so oft auffrischen
local O = { at = 0, told = false, sentAt = 0 }

-- Traegt die Sicht dieses Spiels einen eigenen gezaehmten Baeren? (U.WinMine, client/BanditsNPCBearWinData.lua)
local function ownBear()
    if not U.Fresh or not U.Fresh() or not U.WinMine then return false end
    local cubs = B.View and B.View.cubs
    if type(cubs) ~= "table" then return false end
    for _, c in pairs(cubs) do
        if type(c) == "table" and c.st == "tame" and U.WinMine(c) then return true end
    end
    return false
end

-- K1 (Lauf baer-k1, PLAN_K1.md 1.3, 6; Kevin 14.11.2026 ~01:10: "wenn der spieler vorspult das spiel dan legt er sich auch zum schlafen hin"):
-- im EINZELSPIELER zaehlt auch das Vorspulen (Spieltempo > 1) als Schlaf des Besitzers -- dieselbe Bitte "Sleep" { on }, kein neues Netzfeld.
-- Der Vergleich genau wie V:client/TimedActions/ISTimedActionQueue.lua:302 (UIManager.getSpeedControls():getCurrentGameSpeed() > 1, mit dem
-- Riegel UIManager.getSpeedControls wie V:client/Foraging/ISBaseIcon.lua:62-63; Aufruf auch V:client/Context/ISMenuContextWorld.lua:37). Im
-- Mehrspieler gibt es Vorspulen nur, wenn alle schlafen (dann zaehlt isAsleep) -- dort wird das Tempo nicht gefragt.
local function fastForward()
    if not (B.IsSP and B.IsSP()) then return false end
    if not (UIManager and UIManager.getSpeedControls) then return false end
    local sc = UIManager.getSpeedControls()
    if not sc then return false end
    return (tonumber(sc:getCurrentGameSpeed()) or 1) > 1
end
U.SleepFastForward = fastForward

-- getSpecificPlayer(0): V:client/Farming/CFarmingSystem.lua:45; playerObj:isAsleep(): V:client/ISUI/ISButtonPrompt.lua:440. Die Tabelle
-- der Bitte ist nie leer (eine leere kaeme als nil an, S:client/BanditsNPCBearClient.lua sendHello).
function U.SleepReport(now)
    if now - O.at < OWN_MS and now >= O.at then return end
    O.at = now
    local p = getSpecificPlayer(0)
    if not p or not B.Ask then return end
    if p:isAsleep() == true or fastForward() then
        if (not O.told or now - O.sentAt >= OWN_RESEND_MS or now < O.sentAt) and ownBear() then
            O.told, O.sentAt = true, now
            B.Ask(p, "Sleep", { on = true })
        end
    elseif O.told then
        O.told = false
        B.Ask(p, "Sleep", { on = false })
    end
end

local function onGameStart()
    Z.at, Z.poke, Z.clock, Z.last, Z.st, Z.list, Z.n = 0, true, 0, nil, {}, {}, 0
    O.at, O.told, O.sentAt = 0, false, 0
end

Events.OnGameStart.Add(onGameStart)                 -- V:client/Chat/ISChat.lua:1186
