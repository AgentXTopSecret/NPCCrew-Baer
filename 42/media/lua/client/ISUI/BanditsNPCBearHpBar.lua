--
-- NPC Crew -- Baer, Lebensanzeige ueber dem Baeren, Vorlage B "Rollenspiel" (Lauf baer-hp-b, 14.11.2026; Kevin 14.11. ~11:15 "die hp anzeige
-- ueber den baeren soll schoener werden", ~12:25 "B rollenspiel ist geil" -- baer/begleiter/ENTSCHEIDUNGEN.md). DER ENTWURF IST DIE VORGABE:
-- _arbeit/baer_hp_entwurf/B/BESCHREIBUNG.md und zeichne.py (Masse, Farben, Zeitverlauf der Effekte stammen von dort, Zeile fuer Zeile).
--
-- Was man sieht (Option "Health above tamed bears" = Bar, wie heute je Baer abschaltbar ueber das Zahnrad, U.HpOn; "Number" bleibt die
-- Zahl-Zeile des Schilds, "Off" nichts):
--   * links eine runde Bronze-Plakette mit Pfote (eigenes Bild), rechts der Balken im Rahmen schwarz / Bronze / schwarz (abgeschraegte Ecken,
--     helle Kante oben), 10 Segmente, Fuellung mit Glanz oben und Schatten unten, in der Mitte die Zahl "352/400" mit dunklem Umriss.
--   * Farbe in STUFEN: gruen ab 61 %, gelb ab 31 %, orange ab 16 %, darunter rot und pulsierend ("fast leer": schneller roter Puls mit Schein).
--   * rechts vom Rahmen Zustands-Bilder: Pflaster (Sicht bnd: Verband wirkt), Keule (Hunger 100: verliert Leben), Tropfen (Durst 100).
--   * Effekte: HEILEN (Leben steigt in der Sicht: neuer Teil leuchtet, Rahmen und Plakette gruen, 8 helle Kreuze steigen auf, gruene "+12"),
--     TREFFER (Fx "hurt" ohne Ausweichen: Wackeln, kurzer weisser Blitz, Rahmen rot, rote "-28" springt hoch, der verlorene Teil bleibt hell
--     stehen und laeuft nach), HUNGER/DURST (kein Wackeln, kein Blitz: Rahmen pulsiert langsam orange mit Schein, das Ende der Fuellung pulsiert
--     dunkel, kleine "-4" sinkt neben den Bildern ab), FAST LEER (<= 15 %: Fuellung, Rahmen, Plakette pulsieren rot, roter Schein).
--     Hungert er UND ist fast leer, hat der rote Schein Vorrang, die Keule bleibt. Schwebende Zahlen stehen RECHTS neben dem Rahmen (nie ueber
--     dem Kopf), Kreuze ueber dem Balken.
--   * Groesse waechst mit der Schrift: u = Hoehe der Zeile-1-Schrift / 19 (Small 1x: u = 1 -> Rahmen 106 x 19; Kevins 4x: u = 2 -> 212 x 38).
--
-- Ausloeser (nur Anzeige; alle Zahlen kommen aus der Sicht bzw. dem Fx-Ereignis des Schreibers, nichts geht zurueck):
--   * U.HpBarPrep (aus dem Listenbau der Anzeige, hoechstens 1 x je Sekunde und sofort nach einer neuen Sicht): vergleicht hp der Sicht mit dem
--     letzten Stand DIESES Baeren -- hoeher = Heilen; niedriger = Treffer bestaetigt (Fx "hurt" mit pts: solange die Sicht zur Vorhersage passt,
--     Rundung +-0,5) bzw. Hunger/Durst (hun / thr 100 in der alten ODER neuen Sicht, nicht am Boden dn, nicht eingefroren nfz;
--     S:server/BanditsNPCBearNeeds.lua:520-522, :566-585) bzw. sonst ein Treffer, dessen Fx diesen Client nicht erreichte (fxDist). War der Baer
--     laenger als Z.SEEN_MS nicht in der Liste, gibt es keinen Effekt (nur neuer Stand). Einzelheiten: onDrop (Nachbesserung C1-C4).
--   * U.HpBarHurt(id, pts) (aus U.FightFx "hurt", client/BanditsNPCBearFx.lua): sofort Wackeln, Blitz, "-pts" und die vorhergesagte Fuellung
--     (Feld pts des Ereignisses, S:server/BanditsNPCBearHurt.lua B.BearHurt); die Sicht mit dem neuen Leben kommt spaeter und loest die Vorhersage
--     ab (wartet bis Z.PRED_MS; aendert der Treffer die ganzen Prozent der Sicht nicht, bleibt die Vorhersage bis zur naechsten anderen Sicht).
--     Ohne pts (alter Schreiber): Wackeln sofort, Zahl und Nachlauf aus der naechsten niedrigeren Sicht.
--
-- Zeichnen je Bild NUR aus fertigen Daten (Eintrag e.hpSt / e.hpM, beim Listenbau gesetzt): Rechnen, keine Suche, kein getText, keine Tabelle
-- je Bild (die Zahl "352/400" wird nur bei neuem Wert gebaut, schwebende Zahlen beim Ausloesen). Bilder einmal je Spielstart (je Groesse).
-- Zeichenaufrufe je Lebens-Rahmen: ruhig 25 (Rahmen 6, Leiste 4, Segmente 9, Zahl 5, Plakette 1) + je Zustands-Bild 1; hoechstens 72 (Schein 2,
-- Rahmen 6, Leiste mit Nachlauf / Glanz / Rinnen / Blitz 8, Segmente 9, Zahl 5, Plakette 1, Bilder 3, 8 Kreuze je 4, 3 Zahlen je 2).
-- Deckel: je Baer hoechstens Z.FLOAT_MAX schwebende Zahlen und Z.CROSS_N Kreuze; Zustand je Kennung, gedeckelt durch die Sicht (U.HpBarForget) und
-- Z.STATE_MAX.
--
-- Engine-Aufrufe (Fundstelle, gleiche Argumenttypen):
--   el:drawRect(x, y, w, h, a, r, g, b): V:client/ISUI/ISUIElement.lua:1191 (wie S:client/ISUI/BanditsNPCBearHud.lua valueBar)
--   el:drawTextCentre(Text, x, y, r, g, b, a, Schrift): V:client/ISUI/ISUIElement.lua:1280; UIFont.Medium V:client/ISUI/ISFitnessUI.lua:204,
--     UIFont.Large V:client/Chat/ISAlert.lua:35, UIFont.Small / NewSmall wie die Anzeige (S:client/ISUI/BanditsNPCBearHud.lua text)
--   el:drawTextureScaled(Bild, x, y, w, h, a, r, g, b): V:client/Chat/ISChat.lua:418; Farbton r/g/b ungleich 1:
--     V:client/XpSystem/ISUI/ISSkillProgressBar.lua:198
--   getTexture("media/textures/<datei>.png"): V:client/Chat/ISChat.lua:424 (wie S:client/ISUI/BanditsNPCBearTalentTab.lua)
--   getTextManager():getFontHeight(UIFont.Medium / UIFont.Large): V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8 / ISAdminTicketsUI.lua:6
--   getTimestampMs(): V:client/Foraging/ISBaseIcon.lua:485
--   getTextManager():MeasureStringX(Schrift, Text): V:client/ISUI/ISButton.lua:450 (Nachbesserung P2; einmal je schwebende Zahl, nicht je Bild)
--   B.Now() = getGameTime():getWorldAgeHours() (Kern S:shared/BanditsNPCBear.lua:714; Client V:client/Challenge/WinterIsComing.lua:8) --
--     nur beim Listenbau, nur fuer fremde Baeren mit Hunger / Durst 100 (Nachbesserung C4)
--   math.cos / math.sin / math.pi (Lua): V:client/RadioCom/ISUIRadio/ISSineWaveDisplay.lua:95, V:client/ISUI/ISEquippedItem.lua:391
-- Bilder (eigene Rechnung des Entwurfs, _arbeit/baer_zaehmen/hp/werkzeug/tex_hp.py): 42/media/textures/BanditsNPCBear_Hp_<art>_<NN>.png,
-- gezeichnet 1:1 (scharf) in der groessten Groesse, die in 24u (Plakette) bzw. 20u (Bilder) passt.
-- Laeuft im Einzelspieler und auf jedem MP-Client gleich (der dedizierte Server laedt client/ nicht). Fehlt diese Datei, zeichnet die Anzeige
-- den alten schmalen Balken (Existenz-Riegel in BanditsNPCBearHud.lua). Statisch geprueft, nicht gespielt.
--

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- ---------------------------------------------------------------------------
-- Farben (r, g, b) wie der Entwurf (zeichne.py Zeile 51-75)
-- ---------------------------------------------------------------------------
local C = {}                -- Farben (eine Tabelle: Lua 5.1 erlaubt hoechstens 60 Upvalues je Funktion)
C.GREEN = { 0.38, 0.80, 0.30 }
C.YELLOW = { 0.95, 0.80, 0.20 }
C.ORANGE = { 0.96, 0.52, 0.14 }
C.RED = { 0.88, 0.17, 0.15 }
C.RED_HI = { 1.00, 0.45, 0.38 }          -- Puls "fast leer" (LEER_HELL)
C.BRONZE = { 0.80, 0.60, 0.29 }
C.BRONZE_HI = { 0.98, 0.84, 0.52 }
C.INNER = { 0.06, 0.045, 0.035 }
C.TRACK = { 0.13, 0.10, 0.085 }
C.SEG = { 0.30, 0.25, 0.21 }
C.NUM = { 1.00, 0.98, 0.93 }
C.HEAL = { 0.55, 1.00, 0.50 }            -- "+12"
C.HEAL_X = { 0.80, 1.00, 0.70 }          -- Kreuze
C.HEAL_X_SH = { 0.03, 0.20, 0.03 }       -- Schatten der Kreuze
C.HEAL_RIM = { 0.45, 0.95, 0.40 }        -- Rahmen beim Heilen
C.HEAL_NEW = { 0.85, 1.00, 0.80 }        -- frisch geheilter Teil
C.HIT = { 1.00, 0.27, 0.20 }             -- "-28" und Rahmen beim Treffer
C.GHOST = { 1.00, 0.88, 0.78 }           -- verlorener Teil, der nachlaeuft
C.HUNGER = { 1.00, 0.55, 0.06 }          -- Rahmen-Puls und Schein bei Hunger/Durst
C.HUNGER_NUM = { 0.98, 0.70, 0.36 }
C.DRAIN = { 0.30, 0.13, 0.03 }           -- Ende der Fuellung "rinnt"
C.LOW_GLOW = { 1.00, 0.18, 0.12 }
C.LOW_RIM = { 0.95, 0.20, 0.15 }
C.TINT_HEAL = { 0.75, 1.00, 0.75 }            -- Farbton der Plakette
C.TINT_HIT = { 1.00, 0.45, 0.42 }
C.TINT_LOW = { 1.00, 0.55, 0.50 }

-- Stufen (ganze Prozent): ab 61 gruen, ab 31 gelb, ab 16 orange, darunter rot und "fast leer"
local Z = {}                -- Stufen, Zeiten (ms), Deckel (eine Tabelle, Grund wie C)
Z.AT_GREEN, Z.AT_YELLOW, Z.AT_ORANGE = 61, 31, 16
Z.LOW_AT = 15

-- Zeiten (ms) wie der Entwurf (fx_heal / fx_hit / fx_hunger / fx_low)
Z.SEEN_MS = 2500        -- war der Baer laenger nicht in der Liste: neuer Stand ohne Effekt
-- Nachbesserung C2 / C3 (hp/NACHBESSERUNG.md): ein Treffer mit pts wartet so lange auf seine Sicht (Vorhersage gezeigt, Zuordnung offen; vorher
-- 3 s / 4 s -- eine spaete Sicht im MP gab einen zweiten Treffer-Effekt). Passt die Sicht schon (Treffer kleiner als ihre Rundung), haelt jeder
-- Listenbau die Vorhersage fuer die Anzeige weiter, bis die Sicht sich aendert.
Z.PRED_MS = 6000
Z.HURT_WIN = 6000       -- ein Treffer OHNE pts (alter Schreiber) wartet so lange auf seine ERSTE niedrigere Sicht
Z.EPS = 0.000001
Z.FADE_IN = 80
Z.HEAL_GLOW = 900
Z.HEAL_RIM_HOLD, Z.HEAL_RIM_FADE = 250, 800
Z.HEAL_FLOAT, Z.HEAL_FLOAT_HOLD = 1500, 800
Z.CROSS_N, Z.CROSS_STEP, Z.CROSS_LIFE, Z.CROSS_HOLD = 8, 100, 1000, 550
Z.CROSS_END = (Z.CROSS_N - 1) * Z.CROSS_STEP + Z.CROSS_LIFE
Z.HIT_SHAKE, Z.HIT_HZ = 320, 22
Z.GHOST_HOLD, Z.GHOST_RUN = 450, 450
Z.HIT_RIM_HOLD, Z.HIT_RIM_FADE = 120, 400
Z.HIT_FLASH = 90
Z.HIT_FLOAT, Z.HIT_FLOAT_HOLD, Z.HIT_JUMP = 1400, 750, 120
Z.HIT_END = 1400
Z.HUN_MS = 1600
Z.DRAIN_FLOAT, Z.DRAIN_FLOAT_HOLD = 1600, 700
Z.LOW_MS = 900
Z.TWO_PI = 2 * math.pi
-- Kreuze: Lage relativ zur Leiste (Anteil der Breite / der Steig-Hoehe), wie der Entwurf -- nie unter dem Zustandstext (Mitte 0,2 .. 0,6)
Z.CROSS_X = { 0.05, 0.68, 0.13, 0.93, 0.80, 0.02, 0.17, 0.74 }
Z.CROSS_Y = { 0.55, 0.20, 0.75, 0.40, 0.30, 0.60, 0.80, 0.45 }

Z.FLOAT_MAX = 3         -- schwebende Zahlen je Baer
Z.STATE_MAX = 32        -- Zustaende insgesamt (mehr: alle vergessen; die Sicht deckelt ohnehin)
Z.K_HEAL, Z.K_HIT, Z.K_DRAIN = 1, 2, 3

-- Bilder (eigene Rechnung, _arbeit/baer_zaehmen/hp/werkzeug/tex_hp.py). Namen ausgeschrieben (Uebernahme-Skript: jedes genannte Bild wird
-- mitkopiert, jedes kopierte genannt).
local BADGE_SIZES = { 24, 32, 40, 48, 56, 64 }
local ICON_SIZES = { 16, 20, 24, 28, 32, 40, 48 }
local FILES = {
    badge = {
        [24] = "media/textures/BanditsNPCBear_Hp_badge_24.png", [32] = "media/textures/BanditsNPCBear_Hp_badge_32.png",
        [40] = "media/textures/BanditsNPCBear_Hp_badge_40.png", [48] = "media/textures/BanditsNPCBear_Hp_badge_48.png",
        [56] = "media/textures/BanditsNPCBear_Hp_badge_56.png", [64] = "media/textures/BanditsNPCBear_Hp_badge_64.png",
    },
    bandage = {
        [16] = "media/textures/BanditsNPCBear_Hp_bandage_16.png", [20] = "media/textures/BanditsNPCBear_Hp_bandage_20.png",
        [24] = "media/textures/BanditsNPCBear_Hp_bandage_24.png", [28] = "media/textures/BanditsNPCBear_Hp_bandage_28.png",
        [32] = "media/textures/BanditsNPCBear_Hp_bandage_32.png", [40] = "media/textures/BanditsNPCBear_Hp_bandage_40.png",
        [48] = "media/textures/BanditsNPCBear_Hp_bandage_48.png",
    },
    hunger = {
        [16] = "media/textures/BanditsNPCBear_Hp_hunger_16.png", [20] = "media/textures/BanditsNPCBear_Hp_hunger_20.png",
        [24] = "media/textures/BanditsNPCBear_Hp_hunger_24.png", [28] = "media/textures/BanditsNPCBear_Hp_hunger_28.png",
        [32] = "media/textures/BanditsNPCBear_Hp_hunger_32.png", [40] = "media/textures/BanditsNPCBear_Hp_hunger_40.png",
        [48] = "media/textures/BanditsNPCBear_Hp_hunger_48.png",
    },
    thirst = {
        [16] = "media/textures/BanditsNPCBear_Hp_thirst_16.png", [20] = "media/textures/BanditsNPCBear_Hp_thirst_20.png",
        [24] = "media/textures/BanditsNPCBear_Hp_thirst_24.png", [28] = "media/textures/BanditsNPCBear_Hp_thirst_28.png",
        [32] = "media/textures/BanditsNPCBear_Hp_thirst_32.png", [40] = "media/textures/BanditsNPCBear_Hp_thirst_40.png",
        [48] = "media/textures/BanditsNPCBear_Hp_thirst_48.png",
    },
}

local texCache = {}         -- Pfad -> Bild oder false (fehlt); gedeckelt durch FILES (27 Pfade)
local texErr = false
local metricsOf = {}        -- Groessenstufe der Anzeige (Tabelle) -> Masse; hoechstens drei Stufen
local states = {}           -- Kennung -> Zustand der Anzeige dieses Baeren
local stateN = 0

local function isNum(v)
    return type(v) == "number" and v == v
end

-- Bild einmal je Spielstart holen; fehlt es: EINE Fehlerzeile, dann ohne dieses Bild.
local function texOf(path)
    if path == nil then return nil end
    local tex = texCache[path]
    if tex == nil then
        tex = getTexture(path)                                   -- V:client/Chat/ISChat.lua:424
        if not tex then
            tex = false
            if not texErr then
                texErr = true
                if B.Err then B.Err("hud: health bar image " .. tostring(path) .. " is missing -- drawn without it") end
            end
        end
        texCache[path] = tex
    end
    if tex == false then return nil end
    return tex
end

-- groesste Groesse aus list, die nicht groesser ist als lim (sonst die kleinste)
local function pickSize(list, lim)
    local best = list[1]
    for i = 1, #list do
        if list[i] <= lim + 0.01 then best = list[i] end
    end
    return best
end

-- Masse einer Groessenstufe t der Anzeige (t.f1 / t.h1 = Zeile-1-Schrift, t.f2 / t.h2 = kleine Schrift; S:client/ISUI/BanditsNPCBearHud.lua
-- tierOf). Einmal je Stufe gerechnet (hoechstens drei), samt Bildern.
local function metrics(t)
    local m = metricsOf[t]
    if m then return m end
    local h1 = tonumber(t.h1) or 19
    local u = h1 / 19
    if u < 1 then u = 1 end
    local function P(v) return math.floor(v * u + 0.5) end
    m = { u = u }
    m.th = math.max(1, math.floor(u + 0.5))                     -- Strichstaerke
    m.W = P(100)                                                -- Leiste innen
    m.H = P(13)
    m.FW = m.W + 6 * m.th                                       -- mit Rahmen (schwarz, Bronze, schwarz)
    m.FH = m.H + 6 * m.th
    m.badge = pickSize(BADGE_SIZES, 24 * u)
    m.icon = pickSize(ICON_SIZES, 20 * u)
    m.ov = P(5)                                                 -- so weit liegt die Plakette ueber dem linken Rahmen
    m.unitW = m.badge + m.FW - m.ov
    m.blockH = math.max(m.badge, m.FH)
    m.p1, m.p2, m.p3, m.p4, m.p6, m.p9, m.p10 = P(1), P(2), P(3), P(4), P(6), P(9), P(10)
    m.p14, m.p16, m.p24 = P(14), P(16), P(24)
    m.crossT = math.max(2, P(2))
    m.gloss = math.max(1, math.floor(m.H * 0.38))
    m.seg = {}
    for k = 1, 9 do m.seg[k] = math.floor(m.W * k / 10 + 0.5) - math.floor(m.th / 2) end
    -- Schriften: Zahl im Balken = kleine Zeile des Schilds (Stufe 1: Small), schwebend = eine Stufe ueber der Zeile 1 (wie client/
    -- BanditsNPCBearFx.lua floatFont), "-4" (Hunger) = kleine Schrift
    m.numFont, m.numH = t.f2 or UIFont.Small, tonumber(t.h2) or h1
    m.floatFont = UIFont.Large
    if t.f1 == UIFont.Small then m.floatFont = UIFont.Medium end
    m.floatH = getTextManager():getFontHeight(m.floatFont)      -- ISAddSafeZoneUI.lua:8 / ISAdminTicketsUI.lua:6
    if not isNum(m.floatH) or m.floatH <= 0 then m.floatH = h1 end
    m.smallFont, m.smallH = m.numFont, m.numH
    m.texBadge = texOf(FILES.badge[m.badge])
    m.texBandage = texOf(FILES.bandage[m.icon])
    m.texHunger = texOf(FILES.hunger[m.icon])
    m.texThirst = texOf(FILES.thirst[m.icon])
    metricsOf[t] = m
    return m
end

local function clamp01(x)
    if x < 0 then return 0 end
    if x > 1 then return 1 end
    return x
end

local function easeOut(x)
    x = clamp01(x)
    local k = 1 - x
    return 1 - k * k * k
end

-- Deckkraft einer Erscheinung: 80 ms ein, bis hold voll, dann bis life aus (ms)
local function fade(tau, life, hold)
    if tau < 0 or tau >= life then return 0 end
    if tau < Z.FADE_IN then return tau / Z.FADE_IN end
    if tau < hold then return 1 end
    local a = 1 - (tau - hold) / (life - hold)
    if a < 0 then return 0 end
    return a
end

-- Punkte wie die Zahl im Balken (ganze Prozent mal Hoechstwert)
local function pts(pct, most)
    return math.floor(pct * most / 100 + 0.5)
end

local function addFloat(st, txt, kind, now)
    local fl = st.fl
    while #fl >= Z.FLOAT_MAX do table.remove(fl, 1) end
    fl[#fl + 1] = { txt = txt, k = kind, t0 = now }
end

-- gerade gezeigtes Leben (Prozent, darf Bruch sein): Sicht, oder die Vorhersage nach einem Treffer, solange sie gilt und tiefer ist
local function shownPct(st, now)
    local v = st.vp
    local p = st.pred
    if p ~= nil and now < st.predUntil and now >= st.predUntil - Z.PRED_MS and p < v then v = p end
    return v
end

-- Ende des Nachlaufs (Prozent) oder nil
local function ghostEnd(st, now)
    if st.gAt == nil then return nil end
    local tau = now - st.gAt
    if tau < 0 or tau >= Z.GHOST_HOLD + Z.GHOST_RUN then return nil end
    if tau < Z.GHOST_HOLD then return st.gFrom end
    return st.gFrom - (st.gFrom - st.gTo) * easeOut((tau - Z.GHOST_HOLD) / Z.GHOST_RUN)
end

local function ghost(st, from, to, now)
    if from <= to then return end
    st.gAt, st.gFrom, st.gTo = now, from, to
end

local function stateOf(id)
    local st = states[id]
    if st == nil then
        if stateN >= Z.STATE_MAX then
            states = {}
            stateN = 0
        end
        st = { fl = {} }
        states[id] = st
        stateN = stateN + 1
    end
    return st
end

-- Heilen: Leben in der Sicht gestiegen
local function onHeal(st, from, to, most, now)
    st.pred = nil
    st.healAt, st.healFrom = now, from
    local n = pts(to, most) - pts(from, most)
    if n > 0 then addFloat(st, "+" .. string.format("%d", n), Z.K_HEAL, now) end   -- string.format: S:shared/BanditsNPCBear.lua argText
end

-- Leben in der Sicht gesunken (from = alte Sicht, to = neue). Reihenfolge (Nachbesserung C1-C3, hp/NACHBESSERUNG.md):
--   1. Treffer mit pts (st.pred, offen bis Z.PRED_MS nach dem letzten Fx): die Sicht BESTAETIGT sie, solange sie nicht tiefer liegt, als die
--      Vorhersage nach der Rundung des Schreibers erlaubt (Sicht = floor(hp x 100 + 0,5), S:server/BanditsNPCBearGrow.lua:976: wahres Leben
--      = Vorhersage +-0,5 -> Sicht >= floor(Vorhersage)) -> kein neuer Effekt. Liegt die Sicht noch ueber der Vorhersage (Fx 2 kam vor Sicht 1),
--      bleibt die Vorhersage stehen; am Boden (dn) gilt die Sicht. Tiefer: der Rest ist ein neuer Verlust ab der Vorhersage.
--   2. ein Treffer OHNE pts (alter Schreiber) wartet Z.HURT_WIN auf seine ERSTE niedrigere Sicht: Nachlauf und Zahl aus der Sicht.
--   3. sonst Hunger / Durst (drain, aus der alten ODER neuen Sicht) -> kleine "-4", kein Wackeln, kein Blitz; sonst ein Treffer, dessen Fx
--      diesen Client nicht erreichte (fxDist) -> Treffer-Effekt aus der Sicht.
-- Rueckgabe true = ein Hunger-/Durst-Verlust wurde gezeigt.
local function onDrop(st, from, to, most, now, drain, dn)
    local p = st.pred
    if p ~= nil and now < (st.predUntil or 0) then
        local open = st.predAt ~= nil and now - st.predAt >= 0 and now - st.predAt <= Z.PRED_MS
        if open and to >= math.floor(p + Z.EPS) then
            if dn or to <= p + 0.5 + Z.EPS then st.pred = nil end
            return false
        end
        if p < from then from = p end                            -- gezeigt war die Vorhersage: der neue Verlust beginnt dort
    end
    st.pred = nil
    local n = pts(from, most) - pts(to, most)
    if st.hitNoPts and st.hitAt ~= nil and now - st.hitAt >= 0 and now - st.hitAt <= Z.HURT_WIN then
        st.hitNoPts = false
        ghost(st, from, to, now)
        if n > 0 then addFloat(st, "-" .. string.format("%d", n), Z.K_HIT, now) end
        return false
    end
    st.hitNoPts = false
    if drain then
        if n > 0 then addFloat(st, "-" .. string.format("%d", n), Z.K_DRAIN, now) end
        return true
    end
    st.hitAt = now
    ghost(st, from, to, now)
    if n > 0 then addFloat(st, "-" .. string.format("%d", n), Z.K_HIT, now) end
    return false
end

-- Weltstunden (B.Now = getGameTime():getWorldAgeHours(), S:shared/BanditsNPCBear.lua:714; auf dem Client wie S:client/BanditsNPCBearMenu.lua:382,
-- Vanilla-Client V:client/Challenge/WinterIsComing.lua:8) oder nil
local function hoursNow()
    if not B.Now then return nil end
    local h = B.Now()
    if isNum(h) then return h end
    return nil
end

local function cfgNum(key, def)
    local c = B.CFG
    local v = c and tonumber(c[key]) or nil
    if v == nil or v ~= v then return def end
    return v
end

-- ---------------------------------------------------------------------------
-- U.HpBarPrep(e, c, t, now, own): beim Listenbau der Anzeige (S:client/ISUI/BanditsNPCBearHud.lua describeValues), nur wenn die Leben-Zeile als
-- Balken steht; own = der Baer gehoert diesem Spieler (wie die Auto-Zeilen, Hud.lua ownOf). Setzt e.hpSt (Zustand) und e.hpM (Masse); gibt die
-- Hoehe der Zeile (Pixel) oder nil (dann der alte Balken).
-- ---------------------------------------------------------------------------
function U.HpBarPrep(e, c, t, now, own)
    if type(e) ~= "table" or type(c) ~= "table" or type(t) ~= "table" or c.id == nil then return nil end
    if not isNum(c.hp) or not isNum(c.hpMax) or not isNum(now) then return nil end
    local m = metrics(t)
    local pct = math.floor(c.hp)
    if pct < 0 then pct = 0 end
    if pct > 100 then pct = 100 end
    local most = math.floor(c.hpMax)
    if most < 0 then most = 0 end
    -- Hunger / Durst 100 kostet Leben, ausser am Boden oder eingefroren (S:server/BanditsNPCBearNeeds.lua:520-522, :566-585)
    local can = c.dn ~= true and c.nfz == nil
    local hunC = can and isNum(c.hun) and c.hun >= 100
    local thrC = can and isNum(c.thr) and c.thr >= 100
    local st = stateOf(c.id)
    st.m = m
    local seen = st.seenAt
    if seen ~= nil and st.vp ~= nil and now - seen >= 0 and now - seen <= Z.SEEN_MS then
        if c.dn == true and st.dn ~= true then
            st.pred = nil       -- geht zu Boden: Leben = downFloor (S:server/BanditsNPCBearHurt.lua:146 B.BearDown), kein Heil-Effekt
        elseif pct > st.vp then
            onHeal(st, shownPct(st, now), pct, most, now)
        elseif pct < st.vp then
            -- Nachbesserung C1: Hunger / Durst nach dem ALTEN oder dem NEUEN Stand (der letzte Schritt endet auf needHpFloor 1 %,
            -- S:server/BanditsNPCBearNeeds.lua:576-585; Abzug und Selbst-Fressen im selben Takt :585 / :613-614 -> eine Sicht mit weniger
            -- Leben und hun < 100) -- nie ein Treffer-Effekt fuer Hunger
            local drain = c.dn ~= true and (st.hunC == true or st.thrC == true or hunC or thrC)
            if onDrop(st, st.vp, pct, most, now, drain, c.dn == true) then st.drH = hoursNow() end
        elseif st.pred ~= nil and now < (st.predUntil or 0) and st.vp - st.pred <= 0.5 + Z.EPS then
            st.predUntil = now + Z.PRED_MS      -- Nachbesserung C2: Treffer kleiner als die Rundung der Sicht -- Vorhersage bleibt stehen
        end
    else
        st.pred, st.gAt, st.healAt, st.hitAt, st.drH = nil, nil, nil, nil, nil
    end
    -- Keule / Tropfen: nicht am Boden-Wert 1 % (dort zieht der Schreiber nichts mehr ab, needHpFloor). Nachbesserung C4: beim FREMDEN Baeren
    -- ruhen die Beduerfnisse auch OHNE Grund in der Sicht (Besitzer nicht im Spiel: S:server/BanditsNPCBearNeeds.lua:254 -> kein Abzug :520-522,
    -- kein nfz :651) -- dort erst nach einem gesehenen Hunger-Sinken und nur, solange das naechste faellig waere (zwei 1-%-Schritte der Sicht bei
    -- needHpHun / needHpThr Prozent je Spielstunde, S:shared/BanditsNPCBear.lua:279, + ein Langsam-Takt von 10 Spielminuten).
    local show = pct > 1
    if show and own ~= true and (hunC or thrC) then
        local rate = 0
        if hunC then rate = rate + cfgNum("needHpHun", 2) end
        if thrC then rate = rate + cfgNum("needHpThr", 3) end
        if rate < 0.1 then rate = 0.1 end
        local h = hoursNow()
        show = st.drH ~= nil and h ~= nil and h - st.drH >= 0 and h - st.drH <= 2 / rate + 1 / 6
    end
    st.vp, st.most, st.seenAt = pct, most, now
    st.hunC, st.thrC, st.dn = hunC, thrC, c.dn == true
    st.hun, st.thr = hunC and show, thrC and show
    st.bnd = isNum(c.bnd) and c.bnd > 0                          -- Verband wirkt (Stunden uebrig, S:server/BanditsNPCBearMend.lua:70)
    e.hpSt, e.hpM = st, m
    return m.blockH
end

-- ---------------------------------------------------------------------------
-- U.HpBarHurt(id, pts): Fx "hurt" ohne Ausweichen (client/BanditsNPCBearFx.lua U.FightFx). Nur ein Baer, dessen Balken gerade steht.
-- ---------------------------------------------------------------------------
function U.HpBarHurt(id, p)
    if id == nil then return false end
    local st = states[id]
    if st == nil or st.seenAt == nil or st.vp == nil then return false end
    local now = getTimestampMs()                                -- ISBaseIcon.lua:485
    if now - st.seenAt < 0 or now - st.seenAt > Z.SEEN_MS then return false end
    local shown = shownPct(st, now)
    local gEnd = ghostEnd(st, now)
    st.hitAt = now
    local v = tonumber(p)
    local most = st.most or 0
    if v ~= nil and v == v and v > 0 and most > 0 then
        local to = shown - v * 100 / most
        if to < 0 then to = 0 end
        st.pred, st.predUntil, st.predAt = to, now + Z.PRED_MS, now
        local from = shown
        if gEnd ~= nil and gEnd > from then from = gEnd end
        ghost(st, from, to, now)
        local n = math.floor(v + 0.5)
        if n >= 1 then addFloat(st, "-" .. string.format("%d", n), Z.K_HIT, now) end
        st.hitNoPts = false
    else
        st.hitNoPts = true
    end
    return true
end

-- Zustaende von Kennungen vergessen, die die Sicht nicht mehr traegt (bei jeder neuen Sicht aus dem Listenbau).
function U.HpBarForget(cubs)
    if type(cubs) ~= "table" then return end
    local gone = nil
    for id, _ in pairs(states) do
        if cubs[id] == nil then
            gone = gone or {}
            gone[#gone + 1] = id
        end
    end
    if gone then
        for i = 1, #gone do states[gone[i]] = nil end
        stateN = stateN - #gone
        if stateN < 0 then stateN = 0 end
    end
end

-- Zum Pruefen (Attrappe, Konsolen-Info): Zustand eines Baeren (nur lesen) und die Masse einer Stufe.
function U.HpBarState(id)
    if id == nil then return nil end
    return states[id]
end

function U.HpBarMetrics(t)
    if type(t) ~= "table" then return nil end
    return metrics(t)
end

-- ---------------------------------------------------------------------------
-- Zeichnen je Bild
-- ---------------------------------------------------------------------------
local function mixInto(r, g, b, c, k)
    return r + (c[1] - r) * k, g + (c[2] - g) * k, b + (c[3] - b) * k
end

-- Glanzkante: Richtung = die Farbe, um 35 % aufgehellt (zeichne.py: fhi = mix(BRONZE_HI, mix(c, weiss, 0.35), k))
local function mixHi(r, g, b, c, k)
    return r + (c[1] * 0.65 + 0.35 - r) * k, g + (c[2] * 0.65 + 0.35 - g) * k, b + (c[3] * 0.65 + 0.35 - b) * k
end

local function shadowText(el, s, x, y, c, a, font, sh)
    el:drawTextCentre(s, x + sh, y + sh, 0, 0, 0, 0.7 * a, font)               -- ISUIElement.lua:1280
    el:drawTextCentre(s, x, y, c[1], c[2], c[3], a, font)
end

local function cross(el, cx, cy, arm, thk, a, sh)
    local half = math.floor(thk / 2)
    local sa = 0.65 * a
    local c = C.HEAL_X_SH
    el:drawRect(cx - arm + sh, cy - half + sh, 2 * arm, thk, sa, c[1], c[2], c[3])
    el:drawRect(cx - half + sh, cy - arm + sh, thk, 2 * arm, sa, c[1], c[2], c[3])
    c = C.HEAL_X
    el:drawRect(cx - arm, cy - half, 2 * arm, thk, a, c[1], c[2], c[3])
    el:drawRect(cx - half, cy - arm, thk, 2 * arm, a, c[1], c[2], c[3])
end

-- U.HpBarDraw(el, e, sx, top, now): der ganze Lebens-Rahmen; sx = Mitte des Schilds, top = Oberkante der Zeile (Bildschirm-Pixel).
function U.HpBarDraw(el, e, sx, top, now)
    local st, m = e.hpSt, e.hpM
    if st == nil or m == nil then return end
    local th = m.th
    local W, H = m.W, m.H
    local pv = shownPct(st, now)
    local ip = math.floor(pv)
    local low = ip <= Z.LOW_AT
    local starving = st.hun == true or st.thr == true
    local pl, ph = 0, 0
    if low then pl = 0.5 - 0.5 * math.cos(Z.TWO_PI * (now % Z.LOW_MS) / Z.LOW_MS) end
    if starving then ph = 0.5 - 0.5 * math.cos(Z.TWO_PI * (now % Z.HUN_MS) / Z.HUN_MS) end
    local hitT, healT = -1, -1
    if st.hitAt ~= nil then
        hitT = now - st.hitAt
        if hitT < 0 or hitT >= Z.HIT_END then hitT = -1 end
    end
    if st.healAt ~= nil then
        healT = now - st.healAt
        if healT < 0 or healT >= Z.CROSS_END then healT = -1 end
    end

    -- Lage (wie zeichne.py draw_tag): Einheit mittig, Wackeln nur seitlich
    local shake = 0
    if hitT >= 0 and hitT < Z.HIT_SHAKE then
        local amp = m.p4 * (1 - hitT / Z.HIT_SHAKE)
        shake = math.floor(amp * math.sin(Z.TWO_PI * Z.HIT_HZ * hitT / 1000 + 0.6) + 0.5)
    end
    local x0 = sx - math.floor(m.unitW / 2) + shake
    local cy = top + m.blockH - math.floor(m.blockH / 2)
    local fx = x0 + m.badge - m.ov
    local fy = cy - math.floor(m.FH / 2)
    local bx, by = fx + 3 * th, fy + 3 * th
    local FW, FH = m.FW, m.FH

    -- Farben dieses Bilds
    local fr, fg, fb = C.BRONZE[1], C.BRONZE[2], C.BRONZE[3]
    local hr, hg, hb = C.BRONZE_HI[1], C.BRONZE_HI[2], C.BRONZE_HI[3]
    local tr, tg, tb = 1, 1, 1
    local glowC, glowA, drainA = nil, 0, 0
    if low then
        local k = 0.75 * pl
        fr, fg, fb = mixInto(fr, fg, fb, C.LOW_RIM, k)
        hr, hg, hb = mixHi(hr, hg, hb, C.LOW_RIM, k)
        glowC, glowA = C.LOW_GLOW, pl
        tr, tg, tb = mixInto(tr, tg, tb, C.TINT_LOW, pl)
    elseif starving then
        local k = 0.90 * ph
        fr, fg, fb = mixInto(fr, fg, fb, C.HUNGER, k)
        hr, hg, hb = mixHi(hr, hg, hb, C.HUNGER, k)
        glowC, glowA = C.HUNGER, 0.55 * ph
        drainA = 0.55 * ph
    end
    if healT >= 0 then
        local k = 1
        if healT >= Z.HEAL_RIM_HOLD then k = clamp01(1 - (healT - Z.HEAL_RIM_HOLD) / Z.HEAL_RIM_FADE) end
        if k > 0 then
            fr, fg, fb = mixInto(fr, fg, fb, C.HEAL_RIM, k)
            hr, hg, hb = mixHi(hr, hg, hb, C.HEAL_RIM, k)
            tr, tg, tb = mixInto(tr, tg, tb, C.TINT_HEAL, k)
        end
    end
    if hitT >= 0 then
        local k = 1
        if hitT >= Z.HIT_RIM_HOLD then k = clamp01(1 - (hitT - Z.HIT_RIM_HOLD) / Z.HIT_RIM_FADE) end
        if k > 0 then
            fr, fg, fb = mixInto(fr, fg, fb, C.HIT, k)
            hr, hg, hb = mixHi(hr, hg, hb, C.HIT, k)
            tr, tg, tb = mixInto(tr, tg, tb, C.TINT_HIT, k)
        end
    end

    -- Schein (fast leer / Hunger): zwei Rechtecke hinter dem Rahmen
    if glowC and glowA > 0 then
        el:drawRect(fx - 3 * th, fy - 3 * th, FW + 6 * th, FH + 6 * th, 0.22 * glowA, glowC[1], glowC[2], glowC[3])   -- ISUIElement.lua:1191
        el:drawRect(fx - 2 * th, fy - 2 * th, FW + 4 * th, FH + 4 * th, 0.45 * glowA, glowC[1], glowC[2], glowC[3])
    end
    -- Rahmen: schwarz (abgeschraegt, 2), Bronze (abgeschraegt, 2), Glanzkante oben (1), schwarz innen (1)
    el:drawRect(fx, fy + th, FW, FH - 2 * th, 0.85, 0, 0, 0)
    el:drawRect(fx + th, fy, FW - 2 * th, FH, 0.85, 0, 0, 0)
    el:drawRect(fx + th, fy + 2 * th, FW - 2 * th, FH - 4 * th, 1, fr, fg, fb)
    el:drawRect(fx + 2 * th, fy + th, FW - 4 * th, FH - 2 * th, 1, fr, fg, fb)
    el:drawRect(fx + 2 * th, fy + th, FW - 4 * th, th, 1, hr, hg, hb)
    local c = C.INNER
    el:drawRect(fx + 2 * th, fy + 2 * th, FW - 4 * th, FH - 4 * th, 1, c[1], c[2], c[3])

    -- Leiste: leer, Fuellung, Nachlauf, frisch geheilt, Rinnen, Glanz, Schatten
    c = C.TRACK
    el:drawRect(bx, by, W, H, 0.95, c[1], c[2], c[3])
    local fill = math.floor(W * pv / 100)
    if fill < 0 then fill = 0 end
    local cr, cg, cb
    if ip >= Z.AT_GREEN then
        c = C.GREEN
    elseif ip >= Z.AT_YELLOW then
        c = C.YELLOW
    elseif ip >= Z.AT_ORANGE then
        c = C.ORANGE
    else
        c = C.RED
    end
    cr, cg, cb = c[1], c[2], c[3]
    if low then cr, cg, cb = mixInto(cr, cg, cb, C.RED_HI, pl) end
    if fill > 0 then el:drawRect(bx, by, fill, H, 1, cr, cg, cb) end
    local wend = fill
    local gEnd = ghostEnd(st, now)
    if gEnd ~= nil then
        local gpx = math.floor(W * gEnd / 100)
        if gpx > fill then
            c = C.GHOST
            el:drawRect(bx + fill, by, gpx - fill, H, 0.95, c[1], c[2], c[3])
            wend = gpx
        end
    end
    if healT >= 0 and healT < Z.HEAL_GLOW and st.healFrom ~= nil then
        local hs = math.floor(W * st.healFrom / 100)
        if fill > hs then
            c = C.HEAL_NEW
            el:drawRect(bx + hs, by, fill - hs, H, 0.95 * (1 - healT / Z.HEAL_GLOW), c[1], c[2], c[3])
        end
    end
    if drainA > 0 and fill > 0 then
        local dw = math.min(fill, m.p10)
        c = C.DRAIN
        el:drawRect(bx + fill - dw, by, dw, H, drainA, c[1], c[2], c[3])
    end
    if wend > 0 then
        el:drawRect(bx, by, wend, m.gloss, 0.26, 1, 1, 1)
        el:drawRect(bx, by + H - m.p3, wend, m.p3, 0.22, 0, 0, 0)
    end
    -- zehn Segmente: neun Striche (auf der Fuellung dunkel, auf der leeren Leiste hell)
    local seg = m.seg
    c = C.SEG
    for k = 1, 9 do
        local xk = bx + seg[k]
        if xk < bx + wend then
            el:drawRect(xk, by, th, H, 0.42, 0, 0, 0)
        else
            el:drawRect(xk, by, th, H, 0.55, c[1], c[2], c[3])
        end
    end
    if hitT >= 0 and hitT < Z.HIT_FLASH then
        el:drawRect(bx, by, W, H, 0.40 * (1 - hitT / Z.HIT_FLASH), 1, 1, 1)
    end

    -- Zahl im Balken "352/400" (Umriss aus vier Schatten, lesbar auf Gelb und auf Dunkel); Text nur bei neuem Wert gebaut
    local most = st.most or 0
    local cur = pts(pv, most)
    if st.numV ~= cur or st.numM ~= most then
        st.numV, st.numM = cur, most
        st.numTxt = string.format("%d", cur) .. "/" .. string.format("%d", most)
    end
    local num = st.numTxt
    local nx = bx + math.floor(W / 2)
    local ny = by + math.floor(H / 2) - math.floor(m.numH / 2)
    local nf = m.numFont
    el:drawTextCentre(num, nx + th, ny, 0, 0, 0, 0.80, nf)
    el:drawTextCentre(num, nx - th, ny, 0, 0, 0, 0.80, nf)
    el:drawTextCentre(num, nx, ny + th, 0, 0, 0, 0.80, nf)
    el:drawTextCentre(num, nx, ny - th, 0, 0, 0, 0.80, nf)
    c = C.NUM
    el:drawTextCentre(num, nx, ny, c[1], c[2], c[3], 1, nf)

    -- Plakette mit Pfote (1:1, Farbton ueber drawTextureScaled)
    if m.texBadge then
        el:drawTextureScaled(m.texBadge, x0, cy - math.floor(m.badge / 2), m.badge, m.badge, 1, tr, tg, tb)   -- ISChat.lua:418
    end

    -- Zustands-Bilder rechts vom Rahmen: Verband, Hunger, Durst
    local icon = m.icon
    local ix = fx + FW + m.p3
    local iy = cy - math.floor(icon / 2)
    local nIcons = 0
    if st.bnd and m.texBandage then
        el:drawTextureScaled(m.texBandage, ix, iy, icon, icon, 1, 1, 1, 1)
        ix = ix + icon + m.p2
        nIcons = nIcons + 1
    end
    local ia = 0.55 + 0.45 * ph
    if st.hun and m.texHunger then
        el:drawTextureScaled(m.texHunger, ix, iy, icon, icon, ia, 1, 1, 1)
        ix = ix + icon + m.p2
        nIcons = nIcons + 1
    end
    if st.thr and m.texThirst then
        el:drawTextureScaled(m.texThirst, ix, iy, icon, icon, ia, 1, 1, 1)
        nIcons = nIcons + 1
    end

    -- Nachbesserung P2: halbe Breite der Zeile direkt ueber dem Block (e.hpAboveW, beim Listenbau gemessen, S:client/ISUI/BanditsNPCBearHud.lua
    -- describeValues) -- ein langer Zustand ("zu muede -- weicht zurueck", "Muede 90%") bekommt keine Kreuze und keine Zahl ueber sich
    local aHalf = math.floor((tonumber(e.hpAboveW) or 0) / 2)

    -- Kreuze (Heilen): steigen ueber der Leiste auf, nacheinander; unter einer breiten Zeile darueber nur bis zur Oberkante des Blocks
    if healT >= 0 then
        local arm, thk = m.p4, m.crossT
        for i = 1, Z.CROSS_N do
            local ti = healT - (i - 1) * Z.CROSS_STEP
            if ti >= 0 and ti < Z.CROSS_LIFE then
                local a = fade(ti, Z.CROSS_LIFE, Z.CROSS_HOLD)
                if a > 0 then
                    local cxx = bx + math.floor(W * Z.CROSS_X[i])
                    local cyy = by - m.p2 - math.floor(m.p6 * Z.CROSS_Y[i]) - math.floor(m.p14 * easeOut(ti / Z.CROSS_LIFE))
                    if aHalf > 0 and cyy < top + arm and math.abs(cxx - sx) <= aHalf + arm then cyy = top + arm end
                    cross(el, cxx, cyy, arm, thk, a, th)
                end
            end
        end
    end

    -- schwebende Zahlen rechts neben dem Rahmen (abgelaufene fallen heraus, in-place; im ersten Bild noch unsichtbar, Einblenden 80 ms).
    -- Nachbesserung P2: ist die Zeile darueber breiter als der Block, steigen "+12" / "-28" rechts von IHR auf (Breite der Zahl einmal je Zahl
    -- gemessen, getTextManager():MeasureStringX(Schrift, Text): V:client/ISUI/ISButton.lua:450 -- nicht je Bild)
    local fl = st.fl
    local keep = 0
    local fxr = fx + FW + m.p14
    for i = 1, #fl do
        local f = fl[i]
        local tau = now - f.t0
        local life = Z.DRAIN_FLOAT
        if f.k == Z.K_HEAL then life = Z.HEAL_FLOAT elseif f.k == Z.K_HIT then life = Z.HIT_FLOAT end
        if tau < life then
            keep = keep + 1
            fl[keep] = f
        end
        local nxr = fxr
        if aHalf > 0 and f.k ~= Z.K_DRAIN then
            if f.w == nil then f.w = tonumber(getTextManager():MeasureStringX(m.floatFont, f.txt)) or 0 end
            local need = sx + aHalf + m.p4 + math.floor(f.w / 2)
            if need > nxr then nxr = need end
        end
        if f.k == Z.K_HEAL then
            local a = fade(tau, Z.HEAL_FLOAT, Z.HEAL_FLOAT_HOLD)
            if a > 0 then
                local rise = math.floor(m.p24 * easeOut(tau / Z.HEAL_FLOAT))
                shadowText(el, f.txt, nxr, by - m.p4 - rise - math.floor(m.floatH / 2), C.HEAL, a, m.floatFont, th)
            end
        elseif f.k == Z.K_HIT then
            local a = fade(tau, Z.HIT_FLOAT, Z.HIT_FLOAT_HOLD)
            if a > 0 then
                local rest = (tau - Z.HIT_JUMP) / (Z.HIT_FLOAT - Z.HIT_JUMP)
                if rest < 0 then rest = 0 end
                local rise = math.floor(m.p10 * easeOut(tau / Z.HIT_JUMP) + m.p16 * rest)
                shadowText(el, f.txt, nxr, by - m.p4 - rise - math.floor(m.floatH / 2), C.HIT, a, m.floatFont, th)
            end
        else
            local a = fade(tau, Z.DRAIN_FLOAT, Z.DRAIN_FLOAT_HOLD)
            if a > 0 then
                local x = fx + FW + m.p3 + nIcons * (icon + m.p2) + m.p9
                local y = by + math.floor(H / 2) + math.floor(m.p10 * tau / Z.DRAIN_FLOAT) - math.floor(m.smallH / 2)
                shadowText(el, f.txt, x, y, C.HUNGER_NUM, 0.9 * a, m.smallFont, th)
            end
        end
    end
    for i = #fl, keep + 1, -1 do fl[i] = nil end
end

-- Je Spielstart leer (Kennungen und Bilder eines alten Spielstands nie anfassen). Events.OnGameStart: V:client/Chat/ISChat.lua:1186.
local function onGameStart()
    states, stateN = {}, 0
    texCache, texErr = {}, false
    metricsOf = {}
end

Events.OnGameStart.Add(onGameStart)
