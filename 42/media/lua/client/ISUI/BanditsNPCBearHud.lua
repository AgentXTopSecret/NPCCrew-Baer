--
-- NPC Crew -- Baer, Anzeige ueber der Welt (B1a, PLAN_ZAEHMEN.md 5.6, 6.8, 7): Zaehm-Balken ueber dem Jungen und das Schild
-- ueber dem eigenen Koederplatz. B1b (PLAN_B1B.md 2): Namensschild ueber jedem gezaehmten Jungen (Zeile 1 Name, Zeile 2 klein
-- der Zustand bzw. bei fremden Jungen der Besitzer); Balken und Schild haengen am selben Anker B.CFG.tagZ dicht ueber dem Kopf.
-- Dazu U.CubsNear (die Jungen mit Objekt in der Naehe, fuer "Futter hinhalten" im Welt-Menue).
-- B1c (PLAN_B1C.md 1.9, 6.4): Anzeige-Optionen je Spieler ueber U.Opt (client/BanditsNPCBearOptions.lua) -- "TagShow" aus blendet
-- die Namensschilder ALLER gezaehmten Baeren aus (der Zaehm-Balken bleibt immer), "TagSize" 100 / 150 / 200 waehlt die Schrift
-- Small / Medium / Large fuer Schild UND Balken (Balken und Abstaende wachsen mit dem Verhaeltnis der Schrifthoehen). Gelesen nur
-- beim Listenbau (hoechstens 1 x je Sekunde). Ein mitfahrendes Junges (Sicht "ride") hat keinen Koerper: kein Suchlauf seinetwegen.
-- U.CubObj / U.CubPos geben anderen Anzeigen (Markierung, Karte) die lebende Client-Kopie aus derselben Tabelle -- ohne eigenen Suchlauf.
-- B1d (PLAN_B1D.md 1.6, 4, 6.6): ueber jedem gezaehmten Jungen bis zu fuenf Zeilen, jede einzeln waehlbar (Kevin 11.11.2026: "jeden
-- wert einzelnd ... im balken oder als zahl"). Der Block waechst vom Anker nach oben, von unten: Ausdauer -> Leben -> Alter-Zeile ->
-- Zustand -> Name. Name + Zustand an "TagShow" (B1c), Leben an "TagHealth" (1 Aus / 2 Balken / 3 Zahl), Ausdauer an "TagStamina",
-- Alter an "TagAge". Die Zahlen kommen fertig aus der Sicht (sz hp hpMax sta staMax day nst nxt, der Kern rechnet); fehlt ein Wert,
-- faellt seine Zeile weg; ist ALLES aus, bekommt das zahme Junge keinen Eintrag (zaehlt nicht gegen hudMax). Der Anker waechst mit
-- der gezeigten Groesse (tagZ x sz / tagBase). Nur auf dem MP-Client: im Listenbau die Groesse der Client-Kopie aus der Sicht
-- nachsetzen (B.ApplySize, Kern) -- das laufende Tierpaket der Engine traegt keine Groesse (PLAN_B1D.md 0.4).
-- B1e (PLAN_B1E.md 1.2.4, 1.2.5, 3.2 Nr. 13 und 20): ab Halbstark traegt der Eintrag den grossen Koerper (Art B.BIG). Der Suchlauf
-- bindet beide Koerper (nur B.BodyKind des Kerns fragt die Art); das Schild sitzt beim grossen Koerper (Sicht bd == "big") um
-- B.CFG.tagBigK (1,06 = Oberkante Buckel / Kopf des Jungen bei gleicher Groesse, gemessen) hoeher; die MP-Groessen-Probe setzt nur
-- an einer Kopie der passenden Art (im Tauschfenster kann die alte Kopie noch da sein). Vorgabe-Name "<Spieler>'s bear" (U.CubName).
-- F1 (PLAN_F1.md 2.9, 7.1): Zeile 2 kennt die Modi "sitting" / "roaming"; das Namensschild ist je Baer abschaltbar (U.TagOn,
-- client/BanditsNPCBearTags.lua -- je Spieler, was ICH sehe; "TagShow" bleibt der Hauptschalter): bei aus keine Name-/Zustand-Zeilen
-- fuer diesen Baeren, die Werte-Zeilen folgen weiter ihren Optionen. B.OnView meldet jede neue Sicht zusaetzlich dem Baeren-Fenster
-- (U.WinOnView) und dem Sitz-Treiber (U.PoseOnView), je hinter einem Existenz-Riegel.
-- F1B (PLAN_F1B.md 5.2, 5.5; Kevin 12.11.2026: "einen schalter haben das die anzeige aus geht wann der waechst und wenn er bei 100% ist
-- soll der knopf ganz verschwinden ... also ueber den baeren die anzeige"): die Alter-/Wachstums-Zeile steht nur noch, solange der Baer
-- waechst (Sicht mit nst; ausgewachsen fehlt nst) UND sein Schalter "Growth line" an ist (U.AgeOn, je Spieler,
-- client/BanditsNPCBearTags.lua; "TagAge" bleibt der Hauptschalter). Die Zeile "Day N - full-grown" gibt es nicht mehr -- fuer jeden
-- gezaehmten Baeren, den dieser Spieler sieht. Nebenbefund FB 5.3 (a): wechselt ein Eintrag in einer neuen Sicht auf "geladen" (ld),
-- sucht die Anzeige sofort (sonst bis 30 s ohne Objekt -- auch fuer die Nah-Taste E, client/BanditsNPCBearKey.lua). Reine Lua-Rechnung.
-- F2 = B5a (PLAN_F2.md 3.2, 4.6): Zeile 2 des EIGENEN Baeren nennt den Kampfzustand -- "down" (Sicht dn, rot) vor "fighting" (fst fight,
-- orange) vor "backing off" / "catching its breath" (fst retreat / rest, gelb) vor dem Modus. U.TagLift(c) gibt die Hoehe des Schild-
-- Ankers ueber den Fuessen (dieselbe Rechnung wie das Schild), damit "DODGE" / "down" (client/BanditsNPCBearFx.lua) darueber schweben.
-- Die schwebenden Zeilen und Schadenszahlen (Nachtrag 11.1) zeichnet U.FloatDraw aus derselben prerender -- je Bild nur aus fertigen
-- Listen, auch wenn gerade kein Schild steht.
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 8.2): die Hoehe des Schilds nimmt den Faktor tagK des Aussehens (Sicht lk, B.LookNum des
-- Kerns), wenn es einen hat; sonst wie bisher. Die Groessen-Probe vergleicht weiter nur den Koerper (erster Wert von B.BodyKind).
-- F3 (Lauf baer-f3, PLAN_F3.md 8, 9; Kevin 13.11.2026, f3/KEVIN_ANTWORTEN.md):
--   * Vier neue Werte-Zeilen Hunger / Durst / Muedigkeit / Vertrauen (Sicht hun thr tir tru, 0..100), jede einzeln Aus (Vorgabe) / Balken /
--     Zahl ueber "TagHunger" / "TagThirst" / "TagTired" / "TagTrust" (Optionen -> Mods). Der Block waechst von unten: Ausdauer -> Leben ->
--     Hunger -> Durst -> Muedigkeit -> Vertrauen -> Alter -> Zustand -> Name. Die Balken fuellen sich mit dem Druck (Vertrauen mit dem
--     Guten). Fehlt ein Wert in der Sicht, faellt seine Zeile weg.
--   * Zeile 2 des EIGENEN Baeren: "sleeping" in der EINEN Schlaf-Farbe (U.SleepColor) mit Vorrang am Boden > Kampf > Schlaf > Modus; ein
--     Rueckzug mit Grund (Sicht fsy) heisst "too tired - backing off" bzw. "won't fight - backing off" (Kevin Antworten 3 und 4).
--   * HERZ (Kevin Antwort 7: "bei maximalen vertrauen ... ein Herz ueber den baeren namen", Nachtrag "oder das herz wird nur angezeigt wenn
--     die namens anzeige vom baeren an ist"): meldet die Sicht maximales Vertrauen (trM, sonst tru >= B.CFG.trHeart, Rueckfall 100), steht
--     ein eigenes Bild media/ui/BanditsNPCBearHeart<NN>.png mittig UEBER dem Namen. Es haengt am Namensschild -- KEIN eigener Schalter:
--     ohne Name-Zeile (TagShow aus oder "Name tag" dieses Baeren aus) kein Herz. Gezeichnet 1:1 (scharf): je Groessenstufe die groesste
--     Datei, die nicht hoeher ist als die Namens-Schrift; ein Aufruf drawTextureScaled je Herz.
--   * U.TagTop(id) = Hoehe des ganzen Schild-Stapels ueber seinem Anker (Pixel, 0 ohne Schild) -- darueber beginnt das z Z z
--     (client/ISUI/BanditsNPCBearZz.lua, gerufen aus prerender nach U.FloatDraw, hinter Existenz-Riegel).
--   * Deckel: je Schild jetzt hoechstens 25 Zeichenaufrufe (12 wie B1d + 4 Werte je hoechstens 3 + 1 Herz), bei hudMax 6 also 150 je Bild.
--   * Mit Schlaf-Clips (B.CFG.sleepClips, erst F3b) sitzt der Anker eines schlafenden Baeren um B.CFG.tagSleepK (0,65) tiefer; mit dem
--     Ersatzbild (Sitzen) bleibt er oben.
--
-- Reine Anzeige: liest nur B.View (die Sicht, die der Schreiber diesem Spieler geschickt hat) und fragt nie den Server.
-- Einzelspieler und Mehrspieler laufen gleich; im Mehrspieler stammen alle Zahlen vom Server. Der dedizierte Server laedt client/ nicht.
--
-- Bauart (Vorbild: ein kleines Element, das weit daneben zeichnet; Vanilla ISButtonPrompt.lua:1244 haelt genauso ein 1 x 1-Element):
--   * EIN ISPanel, 1 x 1 Pixel in der Ecke oben links, angelegt bei OnGameStart. Es bleibt 1 x 1 (ein grosses Element frisst jeden
--     Weltklick) und wird NIE unsichtbar geschaltet (ein unsichtbares Element erreicht prerender nie wieder); Ein/Aus sitzt im
--     Zeichencode. Die drei Maus-Funktionen geben false zurueck.
--   * Die Liste der Balken wird hoechstens einmal je Sekunde neu gebaut (und sofort nach einer neuen Sicht): hoechstens
--     B.CFG.hudMax Junge in B.CFG.hudDist Kacheln, dazu fertige Texte. Die Objektliste der Zelle wird nur durchsucht, wenn ein
--     Junges aus der Sicht noch kein Objekt hat, und dann hoechstens einmal je Sekunde (nach fuenf vergeblichen Laeufen alle 5 s).
--   * Je Bild wird nur aus der fertigen Liste gezeichnet: je Balken zwei Umrechnungen, zwei Rechtecke, ein Rahmen, zwei Texte
--     (jeder mit Schatten); je Namensschild zwei Umrechnungen und zwei Texte (mit Schatten: vier drawTextCentre). B1d: je Schild
--     hoechstens 12 Zeichenaufrufe (Name, Zustand, Alter je 2 Texte, Leben und Ausdauer je Balken mit 3 oder Zahl mit 2) -- bei
--     hudMax 6 also hoechstens 72 je Bild; Zeilen-Lagen, Fuellbreiten und Texte stehen schon fertig im Eintrag. Keine Suche,
--     kein getText, keine Tabelle je Bild. Kein Sichtfeld-Test: ein folgendes Junges laeuft HINTER dem Spieler (Plan 2.3).
--   * Bei mehr als einem lokalen Spieler (geteilter Bildschirm) wird nichts gezeichnet; auf dem MP-Client wird die Liste trotzdem
--     gebaut (Groessen-Probe, Nachbesserung B1d B6). Grenzen (ehrlich): ein Junges ausserhalb der Sicht (fremde ab tellDist 60 Kacheln)
--     und eine ausgeblendete Oberflaeche (ob prerender dann laeuft: ungeprueft) bekommen keine Probe -- die Kopie behaelt ihre Groesse.
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

require "ISUI/ISPanel"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Die Klasse bleibt ein Local: sie muss nicht global sein (nur Zeitaktionen muessen das).
local Hud = ISPanel:derive("BanditsNPCBearHud")

local LIST_MS = 1000        -- Liste hoechstens so oft neu
local SCAN_FAST_MS = 1000   -- Suchlauf, solange ein Junges ohne Objekt ist
local SCAN_SLOW_MS = 5000   -- ... nach SCAN_FAST_N vergeblichen Laeufen
local SCAN_FAST_N = 5
-- Nach SCAN_SLOW_N vergeblichen Laeufen nur noch je SCAN_IDLE_MS (das eigene Junge steht in der Sicht, ist aber weit weg und
-- nicht geladen). Kommt der Spieler in seine Naehe, schickt der Schreiber eine neue Sicht (Server pushNewSights) und es geht
-- wieder schnell (S.scanMiss = 0 bei jeder neuen Sicht). Nachbesserung B6.
local SCAN_SLOW_N = 17
local SCAN_IDLE_MS = 30000
local FLASH_MS = 5000       -- so lange steht "Gezaehmt!"
local BAR_W = 64
local BAR_H = 7
local BAIT_DIST = 25        -- Kacheln: so nah steht das Schild ueber dem eigenen Koederplatz
local BAIT_Z = 0.3
local TAG_Z = 0.18          -- Rueckfall fuer B.CFG.tagZ (Anker von Balken und Schild ueber dem Boden des Tiers, Plan 2.2)
local TAG_BASE = 0.35       -- B1d: Rueckfall fuer B.CFG.tagBase (die Groesse, fuer die tagZ gemessen ist, PLAN_B1D.md 1.2 Punkt 2)
local ZK_MAX = 5            -- B1d: Deckel fuer den Anker-Faktor sz / tagBase (gegen Unsinn in der Sicht; 1,35 / 0,35 = 3,9)
local TAG_BIG_K = 1.06      -- B1e: Rueckfall fuer B.CFG.tagBigK (grosser Koerper; Tag 100: 1,35 / 0,35 x 1,06 = 4,09 < ZK_MAX)
-- B1d: Anzeige-Arten der Werte (U.Opt "TagHealth" / "TagStamina", Index der Auswahl, V:client/PZAPI/ModOptions.lua:137)
local SHOW_OFF, SHOW_BAR, SHOW_NUM = 1, 2, 3
-- F3 (PLAN_F3.md 9): die vier Beduerfnis-Zeilen von unten nach oben. Je Zeile: Options-Id (U.Opt), Sicht-Feld, Schluessel der Zahl-Form,
-- Farbe des Balkens, Farbe des Zahl-Texts. Feste Tabelle (nie je Bild oder je Liste neu).
local NEED_ROWS = {
    { opt = "TagHunger", f = "hun", key = "UI_BN_Bear_Tag_Hunger", r = 0.90, g = 0.55, b = 0.20, tr = 0.98, tg = 0.78, tb = 0.55 },
    { opt = "TagThirst", f = "thr", key = "UI_BN_Bear_Tag_Thirst", r = 0.35, g = 0.60, b = 0.95, tr = 0.66, tg = 0.80, tb = 0.98 },
    { opt = "TagTired", f = "tir", key = "UI_BN_Bear_Tag_Tired", r = 0.65, g = 0.55, b = 0.90, tr = 0.82, tg = 0.76, tb = 0.96 },
    { opt = "TagTrust", f = "tru", key = "UI_BN_Bear_Tag_Trust", r = 1.00, g = 0.78, b = 0.30, tr = 1.00, tg = 0.88, tb = 0.58 },
}
-- F3 (Kevin Antwort 7): das Herz ueber dem Namen. Eigene Bilder (Quelle _arbeit/baer_zaehmen/f3/herz/herz_zeichne.py), je Kantenlaenge
-- eine Datei media/ui/BanditsNPCBearHeart<NN>.png -- gezeichnet wird 1:1 mit der groessten, die nicht hoeher ist als die Namens-Schrift.
local HEART_SIZES = { 16, 20, 24, 28, 32, 40, 48, 64 }
local HEART_FILES = {
    [16] = "media/ui/BanditsNPCBearHeart16.png", [20] = "media/ui/BanditsNPCBearHeart20.png",
    [24] = "media/ui/BanditsNPCBearHeart24.png", [28] = "media/ui/BanditsNPCBearHeart28.png",
    [32] = "media/ui/BanditsNPCBearHeart32.png", [40] = "media/ui/BanditsNPCBearHeart40.png",
    [48] = "media/ui/BanditsNPCBearHeart48.png", [64] = "media/ui/BanditsNPCBearHeart64.png",
}
local HEART_GAP = 1         -- Pixel zwischen Herz und Oberkante der Namens-Zeile
local TR_HEART = 100        -- Rueckfall fuer B.CFG.trHeart (ab diesem Vertrauen gilt "maximal", wenn die Sicht kein trM traegt)
local TAG_SLEEP_K = 0.65    -- Rueckfall fuer B.CFG.tagSleepK (Anker eines liegenden Baeren, nur mit Schlaf-Clips)

local panel = nil
local fontH = nil           -- Hoehe UIFont.Small (Zeile 1, Balken-Texte)
local font2 = nil           -- Schrift der kleinen Zeile 2 des Namensschilds: UIFont.NewSmall, wenn sie niedriger ist, sonst Small
local fontH2 = nil

-- B1c: Groessenstufen der Anzeige (U.Opt "TagSize"). Je Stufe: f1/h1 = Schrift und Hoehe von Zeile 1 und den Balken-Texten, f2/h2 =
-- die kleinere Zeile 2 des Schilds, barW/barH/gap = Balkenmasse (Stufe 1 = genau der Stand B1b). Die Hoehe jeder Schrift wird nur
-- einmal geholt, wenn die Stufe zum ersten Mal gebraucht wird. Hoechstens drei Eintraege.
local tiers = {}
local SIZE_MID = 125        -- TagSize unter 125 -> Stufe 1 (Small), unter 175 -> Stufe 2 (Medium), sonst Stufe 3 (Large)
local SIZE_BIG = 175

-- Alles, was die Anzeige sich merkt. Nichts davon wird gespeichert oder gesendet; die Tabellen sind durch die Sicht gedeckelt
-- (hoechstens so viele Kennungen, wie B.View.cubs traegt; verschwundene Kennungen fallen bei jeder neuen Sicht heraus).
local S = {
    dirty = true,   -- neue Sicht: Liste sofort neu
    listAt = 0,     -- ms, letzte Liste
    scanAt = 0,     -- ms, fruehestens naechster Suchlauf
    scanMiss = 0,   -- vergebliche Suchlaeufe in Folge
    list = {},      -- fertige Eintraege fuer den Zeichner
    n = 0,
    bait = nil,     -- fertiger Eintrag fuer das Koeder-Schild
    objs = {},      -- id -> IsoAnimal (nur in dieser Sitzung, jedes Mal gegengeprueft)
    prev = {},      -- id -> letzter gesehener Zustand (fuer "gerade gezaehmt")
    flash = {},     -- id -> ms, bis wann "Gezaehmt!" steht
    ldPrev = {},    -- F1B: id -> war der Eintrag in der letzten Sicht geladen (ld)? Gedeckelt wie prev (forget bei neuer Sicht)
    tier = nil,     -- B1c: Groessenstufe der aktuellen Liste (tiers[1..3]); nil = noch keine Liste
    -- B1d: Anzeige-Optionen der aktuellen Liste (einmal je Liste gelesen; EINE Tabelle, nie neu angelegt). F3: nd[i] = Anzeige-Art der
    -- i-ten Zeile aus NEED_ROWS (Vorgabe Aus)
    md = { tags = true, hp = SHOW_BAR, sta = SHOW_OFF, age = true, nd = { SHOW_OFF, SHOW_OFF, SHOW_OFF, SHOW_OFF } },
    heart = {},     -- F3: Kantenlaenge -> Bild des Herzens (false = fehlt); gedeckelt durch HEART_SIZES
    heartErr = false,
}

local function reset()
    S.dirty = true
    S.listAt = 0
    S.scanAt = 0
    S.scanMiss = 0
    S.list = {}
    S.n = 0
    S.bait = nil
    S.objs = {}
    S.prev = {}
    S.flash = {}
    S.ldPrev = {}
    S.tier = nil
    S.heart = {}
    S.heartErr = false
end

-- Stufe k (1..3) mit Schriften und Massen. Stufe 1 braucht fontH/font2/fontH2 (in prerender einmal geholt).
-- getFontHeight(UIFont.Medium): V:client/ISUI/AdminPanel/ISAddSafeZoneUI.lua:8; getFontHeight(UIFont.Large):
-- V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:6.
local function tierOf(k)
    local t = tiers[k]
    if t then return t end
    local h1, f1, h2, f2 = fontH, UIFont.Small, fontH2, font2
    if k == 2 or k == 3 then
        local tm = getTextManager()
        local hMed = tm:getFontHeight(UIFont.Medium)
        if k == 2 then
            f1, h1 = UIFont.Medium, hMed
            f2, h2 = UIFont.Small, fontH
        else
            f1, h1 = UIFont.Large, tm:getFontHeight(UIFont.Large)
            f2, h2 = UIFont.Medium, hMed
        end
        if type(h1) ~= "number" or h1 <= 0 then h1 = fontH end
        if type(h2) ~= "number" or h2 <= 0 then h2 = fontH end
    end
    local ratio = 1
    if k ~= 1 and fontH and fontH > 0 then ratio = h1 / fontH end
    if ratio < 1 then ratio = 1 end
    t = {
        f1 = f1, h1 = h1, f2 = f2, h2 = h2,
        barW = math.floor(BAR_W * ratio + 0.5), barH = math.floor(BAR_H * ratio + 0.5),
        gap = math.floor(4 * ratio + 0.5), gap2 = math.floor(2 * ratio + 0.5),
    }
    -- F3: Kantenlaenge des Herzens fuer diese Stufe = groesste Bildgroesse, die nicht hoeher ist als die Namens-Schrift (1:1, scharf)
    t.heart = HEART_SIZES[1]
    for i = 1, #HEART_SIZES do
        if HEART_SIZES[i] <= h1 then t.heart = HEART_SIZES[i] end
    end
    tiers[k] = t
    return t
end

-- F3: Bild des Herzens in der Kantenlaenge size, einmal je Spielstart geholt (S.heart). getTexture("media/ui/<datei>.png"):
-- V:client/Chat/ISChat.lua:921 (wie S:client/ISUI/BanditsNPCBearMarker.lua). Fehlt die Datei: EINE Fehlerzeile, kein Herz.
local function heartTex(size)
    local tex = S.heart[size]
    if tex == nil then
        local file = HEART_FILES[size]
        if file then tex = getTexture(file) end
        if not tex then
            tex = false
            if not S.heartErr then
                S.heartErr = true
                B.Err("hud: heart image " .. tostring(file) .. " is missing -- no heart above name tags")
            end
        end
        S.heart[size] = tex
    end
    if tex == false then return nil end
    return tex
end

-- Gewaehlte Stufe aus der Anzeige-Option (fehlt client/BanditsNPCBearOptions.lua: Vorgabe 100 = Stufe 1).
local function tierWanted()
    local size = 100
    local opt = U.Opt
    if opt then size = tonumber(opt("TagSize", 100)) or 100 end
    if size < SIZE_MID then return 1 end
    if size < SIZE_BIG then return 2 end
    return 3
end

-- Namensschilder zeigen? (fehlt die Options-Datei: ja)
local function tagsWanted()
    local opt = U.Opt
    if not opt then return true end
    return opt("TagShow", true) ~= false
end

-- B1d: Anzeige-Art eines Werts (1 Aus / 2 Balken / 3 Zahl). Fehlt die Options-Datei oder steht Unsinn in ModOptions.ini (Vanilla
-- laedt jede Zahl, V:client/PZAPI/ModOptions.lua:319-320): die Vorgabe.
local function showMode(id, def)
    local opt = U.Opt
    if not opt then return def end
    local v = tonumber(opt(id, def))
    if v == nil then return def end
    v = math.floor(v)
    if v < SHOW_OFF or v > SHOW_NUM then return def end
    return v
end

-- B1d: Alter-Zeile zeigen? (fehlt die Options-Datei: ja)
local function ageWanted()
    local opt = U.Opt
    if not opt then return true end
    return opt("TagAge", true) ~= false
end

-- B1d: traegt die Sicht die Zahlen fuer eine Zeile? (Zahl und nicht NaN; der Kern schickt ganze Zahlen)
local function isNum(v)
    return type(v) == "number" and v == v
end

local function hasHp(c)
    return isNum(c.hp) and isNum(c.hpMax)
end

local function hasSta(c)
    return isNum(c.sta) and isNum(c.staMax)
end

local function hasAge(c)
    return isNum(c.day)
end

-- F1: Namensschild dieses Baeren an? (U.TagOn, client/BanditsNPCBearTags.lua; fehlt die Datei: an)
local function tagOn(c)
    local f = U.TagOn
    if not f then return true end
    return f(c) ~= false
end

-- F1B: Wachstums-Zeile dieses Baeren an? (U.AgeOn, client/BanditsNPCBearTags.lua; fehlt die Datei: an)
local function ageOn(c)
    local f = U.AgeOn
    if not f then return true end
    return f(c) ~= false
end

-- F1B: nur solange er noch waechst -- ausgewachsen fehlt nst (S:server/BanditsNPCBearGrow.lua:758, :786-787)
local function growShown(c)
    return hasAge(c) and c.nst ~= nil and ageOn(c)
end

-- B1d: hat ein gezaehmtes Junges mit den Optionen dieser Liste (md) ueberhaupt eine Zeile? Sonst bekommt es keinen Eintrag.
-- F1: das Namensschild zaehlt nur, wenn es fuer DIESEN Baeren an ist. F1B: die Alter-Zeile nur, solange er waechst und ihr Schalter
-- an ist (ein ausgewachsener Baer ohne andere Zeile bekommt keinen leeren Eintrag).
local function tameShown(c, md)
    if md.tags and tagOn(c) then return true end
    if md.hp ~= SHOW_OFF and hasHp(c) then return true end
    if md.sta ~= SHOW_OFF and hasSta(c) then return true end
    if md.age and growShown(c) then return true end
    -- F3: eine der vier Beduerfnis-Zeilen ist an und die Sicht traegt ihren Wert
    for i = 1, #NEED_ROWS do
        if md.nd[i] ~= SHOW_OFF and isNum(c[NEED_ROWS[i].f]) then return true end
    end
    return false
end

-- F3 (Kevin Antwort 7): meldet die Sicht maximales Vertrauen? Wahrheit ist das Sicht-Feld trM des Schreibers: ein Kern mit F3 (erkennbar
-- an B.TrustK, shared/BanditsNPCBearNeedRules.lua) meldet es selbst -- fehlt trM dann, ist es nicht maximal (kein Nachrechnen aus der
-- gerundeten Sicht-Zahl). Nur ohne einen solchen Kern gilt tru >= B.CFG.trHeart (Rueckfall 100). Beim Listenbau (hoechstens 1 x je
-- Sekunde), nie je Bild.
local function trustMax(c)
    if c.trM ~= nil then return c.trM == true end
    if B.TrustK ~= nil then return false end
    local need = tonumber(B.CFG.trHeart) or TR_HEART
    return isNum(c.tru) and c.tru >= need
end

-- ---------------------------------------------------------------------------
-- Liste bauen (hoechstens einmal je Sekunde)
-- ---------------------------------------------------------------------------

-- Objekt noch da und lebendig? isExistInTheWorld: client/ISUI/Animal/ISAnimalUI.lua:15; isDead: client/ISUI/Hutch/ISHutchUI.lua:427.
local function alive(a)
    return a ~= nil and a:isExistInTheWorld() and not a:isDead()
end

-- Bekommt dieses Junge eine Anzeige? B1b: jedes Junge der Sicht, das ein Objekt haben kann -- ungezaehmte den Balken, gezaehmte
-- (eigene und fremde) das Namensschild. "missing" hat kein Objekt (Plan 2.1). B1c: ein mitfahrendes Junges ("ride") auch nicht.
local function wanted(c)
    if c.ride == true then return false end
    local st = c.st
    return st == "new" or st == "shy" or st == "fed" or st == "tame"
end

-- Kennungen vergessen, die die Sicht nicht mehr traegt. Erst sammeln, dann loeschen (nie waehrend des Durchlaufs).
local function forget(t, cubs)
    local gone = nil
    for id, _ in pairs(t) do
        if cubs[id] == nil then
            gone = gone or {}
            gone[#gone + 1] = id
        end
    end
    if gone then
        for i = 1, #gone do t[gone[i]] = nil end
    end
end

-- Suchlauf: alle geladenen Jungen einmal ihrem Sicht-Eintrag zuordnen. Die Liste ist eine Kopie der Engine, deshalb selten.
-- getCell():getObjectListForLua(), size(), get(i): Vanilla FenrisScenario.lua:505-507; instanceof(o, "IsoAnimal"):
-- shared/TimedActions/Animals/ISAddAnimalInTrailer.lua:29. B1e: beide Koerper ueber B.BodyKind (Kern; darin getAnimalType(),
-- client/ISUI/Animal/ISAnimalUI.lua:65) -- fehlt der Helfer (Kern ohne B1e), kein Suchlauf.
local function scan()
    local kind = B.BodyKind
    if not kind then return end
    local objects = getCell():getObjectListForLua()
    for i = 0, objects:size() - 1 do
        local o = objects:get(i)
        if instanceof(o, "IsoAnimal") and kind(o) ~= nil then
            local v = B.ViewOf(o)
            if v and v.id ~= nil then S.objs[v.id] = o end
        end
    end
end

-- "bereit" oder die Restzeit als Text.
local function waitWord(c, kind, nowH)
    local left = B.WaitLeft(c, kind, nowH)
    if type(left) ~= "number" or left <= 0 then return U.T("UI_BN_Bear_Hud_Ready") end
    return U.WaitText(left)
end

-- Zustand eines gezaehmten Jungen. B.ModeOf ist die Regel des Kerns (shared, Plan 5.3: nil und alles andere = "stay"; F1: follow /
-- stay / sit / roam); fehlt die Kern-Datei, gilt dieselbe Regel hier.
local function modeOf(c)
    local f = B.ModeOf
    if f then return f(c) end
    local m = c.mode
    if m == "follow" or m == "sit" or m == "roam" then return m end
    return "stay"
end

-- F1 (PLAN_F1.md 7.1): Zeile 2 je Modus. Schluessel ausgeschrieben.
local MODE_TAG = { follow = "UI_BN_Bear_Tag_Follow", stay = "UI_BN_Bear_Tag_Stay", sit = "UI_BN_Bear_Tag_Sit",
    roam = "UI_BN_Bear_Tag_Roam" }
-- F2 (PLAN_F2.md 3.2): Zeile 2 im Kampf (Sicht fst) und am Boden (dn) mit eigener Farbe { Schluessel, r, g, b }. Schluessel ausgeschrieben.
local FIGHT_TAG = { fight = { "UI_BN_Bear_Tag_Fight", 1.00, 0.55, 0.25 }, retreat = { "UI_BN_Bear_Tag_Retreat", 0.95, 0.78, 0.40 },
    rest = { "UI_BN_Bear_Tag_Rest", 0.95, 0.78, 0.40 }, down = { "UI_BN_Bear_Tag_Down", 0.95, 0.40, 0.35 } }
-- F3 (PLAN_F3.md 9; Kevin Antworten 3 und 4): Rueckzug MIT Grund (Sicht fsy "tired" / "trust") und "sleeping" in der EINEN Schlaf-Farbe
-- (U.SleepColor, client/BanditsNPCBearClient.lua -- einmal beim Laden dieser Datei; fehlt der Helfer: derselbe Wert).
local BACK_TAG = { tired = { "UI_BN_Bear_Tag_TiredBack", 0.95, 0.78, 0.40 }, trust = { "UI_BN_Bear_Tag_TrustBack", 0.95, 0.78, 0.40 } }
local SLEEP_TAG = { "UI_BN_Bear_Tag_Sleep", 0.70, 0.85, 1.00 }
if U.SleepColor then
    local sr, sg, sb = U.SleepColor()
    SLEEP_TAG[2], SLEEP_TAG[3], SLEEP_TAG[4] = sr, sg, sb
end

-- Namensschild (Plan 2.1): Zeile 1 der Name (U.CubName), Zeile 2 beim eigenen Jungen der Zustand, beim fremden der Besitzer.
-- Gerade gezaehmt: Zeile 2 blinkt FLASH_MS lang gruen "Tamed!", danach der Zustand. Eigen ist ein Junges, wenn der Besitzer mein
-- Schluessel ist -- oder im Einzelspieler der feste Einzelspieler-Schluessel (dann gibt es keinen anderen Besitzer). Im
-- Mehrspieler zaehlt "__sp" nie als eigen und erscheint nie als Text (Nachbesserung B1b B8: Junge eines frueheren
-- Einzelspieler-Stands auf einem Server zeigen "belongs to ?").
local function describeTag(e, meKey)
    local c = e.c
    e.tag = true
    e.line1 = U.CubName(c, meKey)
    local own = (c.owner ~= nil) and (c.owner == meKey or (c.owner == B.SP_KEY and B.IsSP ~= nil and B.IsSP()))
    e.l2 = nil
    if own then
        e.r, e.g, e.b = 0.96, 0.96, 0.90
        e.line2 = U.T(MODE_TAG[modeOf(c)] or "UI_BN_Bear_Tag_Stay")
        -- F2: am Boden vor Kampf vor Modus (feste Tabelle, keine neue je Liste)
        local ft = nil
        if c.dn == true then ft = FIGHT_TAG.down elseif c.fst ~= nil then ft = FIGHT_TAG[c.fst] end
        -- F3: ein Rueckzug nennt seinen Grund (zu muede / weigert sich); schlafend steht "sleeping" (nach Boden und Kampf, vor dem Modus)
        if c.dn ~= true and c.fst == "retreat" and c.fsy ~= nil and BACK_TAG[c.fsy] then ft = BACK_TAG[c.fsy] end
        if ft == nil and c.slp == true then ft = SLEEP_TAG end
        if ft then
            e.line2 = U.T(ft[1])
            e.l2 = ft
        end
        e.till = S.flash[c.id] or 0
        e.flashLine = U.T("UI_BN_Bear_Hud_Tamed")
    else
        e.r, e.g, e.b = 0.80, 0.88, 1.00
        local who = c.owner
        if who == nil or who == B.SP_KEY then who = "?" end
        e.line2 = U.T("UI_BN_Bear_Tag_Owner", tostring(who))
        e.till = 0
    end
end

-- B1d: Wert-Zeile (Leben oder Ausdauer) aus Prozent (0..100) und Hoechstwert (Punkte) -- als Fuellbreite des Balkens oder als Text
-- "<jetzt>/<hoechst>". Gibt fill, text (eins davon nil).
local function valueLine(mode, pct, most, key, barW)
    pct = math.floor(pct)
    if pct < 0 then pct = 0 end
    if pct > 100 then pct = 100 end
    if mode == SHOW_BAR then
        return math.floor(barW * pct / 100), nil
    end
    most = math.floor(most)
    if most < 0 then most = 0 end
    return nil, U.T(key, math.floor(pct * most / 100 + 0.5), most)
end

-- B1d (PLAN_B1D.md 1.6, 6.6): die Werte-Zeilen eines gezaehmten Jungen und die Lage JEDER Zeile als Abstand ihrer Oberkante ueber
-- dem Anker (Pixel), von unten nach oben: Ausdauer, Leben, Alter, Zustand (darueber der Name). Zeilenhoehe Balken t.barH + t.gap2,
-- Textzeile t.h2 + 1. Ohne Werte-Zeilen sitzt der Zustand wie in B1b/B1c mit der Unterkante am Anker.
local function describeValues(e, c, md, t)
    e.showName = md.tags and tagOn(c)
    e.hpFill, e.hpText, e.staFill, e.staText, e.ageLine = nil, nil, nil, nil, nil
    if md.hp ~= SHOW_OFF and hasHp(c) then
        e.hpFill, e.hpText = valueLine(md.hp, c.hp, c.hpMax, "UI_BN_Bear_Tag_Health", t.barW)
    end
    if md.sta ~= SHOW_OFF and hasSta(c) then
        e.staFill, e.staText = valueLine(md.sta, c.sta, c.staMax, "UI_BN_Bear_Tag_Stamina", t.barW)
    end
    -- F1B: nur solange er waechst und sein Schalter an ist (growShown); die "full-grown"-Zeile entfaellt
    if md.age and growShown(c) then
        local day = math.floor(c.day)
        local left = math.floor(tonumber(c.nxt) or 1)
        if left < 1 then left = 1 end
        e.ageLine = U.T("UI_BN_Bear_Tag_Age", day, U.StageName(c.nst), left)
    end
    local up = 0
    if e.staFill then
        e.ySta = up + t.barH
        up = up + t.barH + t.gap2
    elseif e.staText then
        e.ySta = up + t.h2
        up = up + t.h2 + 1
    end
    if e.hpFill then
        e.yHp = up + t.barH
        up = up + t.barH + t.gap2
    elseif e.hpText then
        e.yHp = up + t.h2
        up = up + t.h2 + 1
    end
    -- F3 (PLAN_F3.md 9): Hunger, Durst, Muedigkeit, Vertrauen ueber Leben -- je Zeile { Zeilen-Daten, Fuellbreite ODER Text, Oberkante }.
    -- Die Liste entsteht je Eintrag beim Listenbau (hoechstens 1 x je Sekunde), nie je Bild; ohne Zeile bleibt e.ndN = 0.
    local n = 0
    for i = 1, #NEED_ROWS do
        local row = NEED_ROWS[i]
        local mode = md.nd[i]
        local val = c[row.f]
        if mode ~= SHOW_OFF and isNum(val) then
            local pct = math.floor(val + 0.5)
            if pct < 0 then pct = 0 end
            if pct > 100 then pct = 100 end
            n = n + 1
            e.nd = e.nd or {}
            local line = { row = row }
            if mode == SHOW_BAR then
                line.fill = math.floor(t.barW * pct / 100)
                line.y = up + t.barH
                up = up + t.barH + t.gap2
            else
                line.text = U.T(row.key, pct)
                line.y = up + t.h2
                up = up + t.h2 + 1
            end
            e.nd[n] = line
        end
    end
    e.ndN = n
    if e.ageLine then
        e.yAge = up + t.h2
        up = up + t.h2 + 1
    end
    e.yState = up + t.h2
    -- F3 (Kevin Antwort 7): Herz ueber dem Namen -- nur MIT Name-Zeile (kein eigener Schalter) und nur bei maximalem Vertrauen
    e.heart, e.heartS = nil, 0
    e.top = up
    if e.showName then
        e.top = e.yState + 1 + t.h1
        if trustMax(c) then
            e.heart = heartTex(t.heart)
            if e.heart then
                e.heartS = t.heart
                e.top = e.top + HEART_GAP + t.heart
            end
        end
    end
end

-- B1d: Anker waechst mit der gezeigten Groesse (PLAN_B1D.md 1.2 Punkt 2); fehlt sz (Kern ohne B1d): 1. B1e (PLAN_B1E.md 1.2.5): der
-- grosse Koerper ist bei gleicher Groesse um tagBigK hoeher (Buckel statt Kopf). F2: als eigene Funktion, damit U.TagLift dasselbe rechnet.
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 8.2): traegt das Aussehen des Koerpers (Sicht lk) einen eigenen Faktor tagK in B.LOOKS
-- (B.LookNum des Kerns; Generator-Junges 1,11, Generator gross 1,08 -- aus der Bindepose, ungespielt), gilt er statt tagBigK / 1;
-- sonst wie bisher. Gerufen beim Listenbau (hoechstens 1 x je Sekunde) und von U.TagLift, nie je Bild.
local function lookK(c)
    if c.lk == nil or not B.LookNum then return nil end
    local body = (c.bd == "big") and "big" or "cub"
    local k = tonumber(B.LookNum(body, c.lk, "tagK", nil))
    if k == nil or k ~= k or k <= 0 then return nil end
    return k
end

local function zkOf(c)
    local base = tonumber(B.CFG.tagBase) or TAG_BASE
    if base <= 0 then base = TAG_BASE end
    local sz = c.sz
    if not isNum(sz) or sz <= 0 then return 1 end
    local zk = sz / base
    local lk = lookK(c)
    if lk ~= nil then
        zk = zk * lk
    elseif c.bd == "big" then
        local k = tonumber(B.CFG.tagBigK) or TAG_BIG_K
        if k <= 0 then k = TAG_BIG_K end
        zk = zk * k
    end
    if zk > ZK_MAX then zk = ZK_MAX end
    -- F3 (PLAN_F3.md 9): ein LIEGENDER Baer ist niedriger -- nur mit den Schlaf-Clips (B.CFG.sleepClips, erst F3b); mit dem Ersatzbild
    -- (Sitzen) bleibt der Anker oben.
    if c.slp == true and B.CFG.sleepClips == true then
        local k = tonumber(B.CFG.tagSleepK) or TAG_SLEEP_K
        if k > 0 and k <= 1 then zk = zk * k end
    end
    return zk
end

-- F2 (PLAN_F2.md 3.2): Hoehe des Schild-Ankers ueber den Fuessen (Ebenen) fuer einen Sicht-Eintrag -- fuer "DODGE" / "down"
-- (client/BanditsNPCBearFx.lua). Ohne Eintrag: wie ein Junges ohne Groesse.
function U.TagLift(c)
    local lift = tonumber(B.CFG and B.CFG.tagZ) or TAG_Z
    if type(c) ~= "table" then return lift end
    return lift * zkOf(c)
end

-- Die fertigen Texte eines Eintrags (einmal je Liste, nie je Bild).
local function describe(e, meKey, nowH)
    local c = e.c
    e.zk = 1
    if c.st == "tame" then
        describeTag(e, meKey)
        describeValues(e, c, S.md, S.tier or tierOf(1))
        e.zk = zkOf(c)
        return
    end
    local pct = math.floor(tonumber(c.tame) or 0)
    if pct < 0 then pct = 0 end
    if pct > 100 then pct = 100 end
    local barW = BAR_W
    if S.tier then barW = S.tier.barW end
    e.fill = math.floor(barW * pct / 100)
    local unfed = (c.st == "new" or c.st == "shy")
    e.unfed = unfed
    local line1 = U.T("UI_BN_Bear_Hud_Taming", pct)
    if unfed then line1 = line1 .. " - " .. U.T("UI_BN_Bear_Hud_Shy") end
    e.line1 = line1
    if c.bond ~= nil and c.bond ~= meKey then
        -- an jemand anderen gebunden
        e.line2 = U.T("UI_BN_Bear_Hud_Other", tostring(c.bond))
    elseif unfed then
        -- noch nie gefuettert: Streicheln geht noch nicht, also nur die Futter-Zeile
        e.line2 = U.T("UI_BN_Bear_Hud_Feed", waitWord(c, "feed", nowH))
    else
        e.line2 = U.T("UI_BN_Bear_Hud_Feed", waitWord(c, "feed", nowH)) .. "   "
            .. U.T("UI_BN_Bear_Hud_Pet", waitWord(c, "pet", nowH))
    end
end

local function byDist(a, b)
    return a.d2 < b.d2
end

-- Koeder-Schild: nur der eigene Platz (mehr traegt die Sicht nicht), nur in BAIT_DIST Kacheln.
local function baitEntry(view, px, py)
    local bait = view.bait
    if type(bait) ~= "table" or type(bait.x) ~= "number" or type(bait.y) ~= "number" then return nil end
    local dx = bait.x + 0.5 - px
    local dy = bait.y + 0.5 - py
    if dx * dx + dy * dy > BAIT_DIST * BAIT_DIST then return nil end
    local kindKey = "UI_BN_Bear_Bait_Fish"
    if bait.kind == "honey" then kindKey = "UI_BN_Bear_Bait_Honey" end
    local e = { x = bait.x + 0.5, y = bait.y + 0.5, z = (tonumber(bait.z) or 0) + BAIT_Z }
    e.line1 = U.T("UI_BN_Bear_Hud_Bait", U.T(kindKey))
    if bait.ready == true then
        e.line2 = U.T("UI_BN_Bear_Hud_BaitReady")
    else
        e.line2 = U.T("UI_BN_Bear_Hud_BaitNight", tonumber(bait.nights) or 0, tonumber(bait.max) or 0)
    end
    return e
end

local function rebuild(now)
    local wasDirty = S.dirty
    S.dirty = false
    S.listAt = now
    S.n = 0
    S.bait = nil
    -- Nur eine Sicht von DIESEM Spiel zeigen (B.UI.Fresh, client/BanditsNPCBearClient.lua).
    if not U.Fresh or not U.Fresh() then return end
    local view = B.View
    local cubs = view.cubs
    if type(cubs) ~= "table" then return end

    if wasDirty then
        forget(S.objs, cubs)
        forget(S.prev, cubs)
        forget(S.flash, cubs)
        forget(S.ldPrev, cubs)
        S.scanMiss = 0
    end

    -- 1. Zustandswechsel merken; fehlt einem gewuenschten Jungen das Objekt?
    -- B1d (PLAN_B1D.md 0.4, 6.6): nur auf dem MP-Client die Groesse jeder lebenden Kopie eines zahmen Jungen aus der Sicht nachsetzen
    -- (B.ApplySize, Kern: schreibt nur bei einer Abweichung). Im Einzelspieler ist die Kopie das Objekt des Schreibers -> nie.
    -- isClient(): V:client/ISUI/ISWorldObjectContextMenu.lua:1435. Fehlt B.ApplySize (Kern ohne B1d): keine Probe.
    -- B1e (PLAN_B1E.md 1.2.4): nur an einer Kopie der Art, die die Sicht nennt (bd fehlt = Junges) -- im Tauschfenster bekommt nie ein
    -- Junges-Koerper die Groesse des grossen oder umgekehrt. Fehlt B.BodyKind (Kern ohne B1e): keine Probe.
    local probe = isClient() and B.ApplySize ~= nil and B.BodyKind ~= nil
    local need = false
    local any = false
    for id, c in pairs(cubs) do
        any = true
        local was = S.prev[id]
        if c.st == "tame" and (was == "fed" or was == "shy" or was == "new") then
            S.flash[id] = now + FLASH_MS
        end
        S.prev[id] = c.st
        -- F1B (FB 5.3 a): nur bei neuer Sicht -- wechselt der Eintrag auf "geladen", gleich suchen statt bis zu SCAN_IDLE_MS zu warten
        if wasDirty then
            local ldNow = (c.ld == true)
            if ldNow and S.ldPrev[id] ~= true then S.scanAt = 0 end
            S.ldPrev[id] = ldNow
        end
        if wanted(c) then
            local obj = S.objs[id]
            if not alive(obj) then
                S.objs[id] = nil
                need = true
            elseif probe and c.st == "tame" and isNum(c.sz) and B.BodyKind(obj) == (c.bd or "cub") then
                B.ApplySize(obj, c.sz)
            end
        end
    end
    -- Die Sicht kennt weder ein Junges noch einen Koederplatz: nichts zu tun, kein Engine-Aufruf.
    if not any and view.bait == nil then return end

    local player = getSpecificPlayer(0)                 -- client/Farming/CFarmingSystem.lua:45
    if not player then return end
    local px = player:getX()                            -- client/Fishing/TensionUI.lua:11
    local py = player:getY()

    -- 2. Suchlauf, nur bei Bedarf und gedrosselt (now < scanAt - SCAN_IDLE_MS: die Uhr lief rueckwaerts).
    if need and (now >= S.scanAt or now < S.scanAt - SCAN_IDLE_MS) then
        scan()
        local still = false
        for id, c in pairs(cubs) do
            if wanted(c) and S.objs[id] == nil then still = true end
        end
        if still then
            S.scanMiss = S.scanMiss + 1
            local wait = SCAN_IDLE_MS
            if S.scanMiss <= SCAN_FAST_N then
                wait = SCAN_FAST_MS
            elseif S.scanMiss <= SCAN_SLOW_N then
                wait = SCAN_SLOW_MS
            end
            S.scanAt = now + wait
        else
            S.scanMiss = 0
            S.scanAt = now + SCAN_FAST_MS
        end
    end

    -- 3. Eintraege: die naechsten hudMax in hudDist Kacheln. B1c: Anzeige-Optionen einmal je Liste lesen (U.Opt, je Wert
    -- hoechstens 1 x je Sekunde); "Namensschilder aus" laesst gezaehmte Junge weg (sie zaehlen dann auch nicht gegen hudMax).
    -- B1d: dazu Leben / Ausdauer / Alter; ein gezaehmtes Junges bekommt nur dann einen Eintrag, wenn mindestens EINE seiner Zeilen
    -- gezeigt wird (tameShown) -- Name aus, Leben als Balken: nur der Balken.
    S.tier = tierOf(tierWanted())
    local md = S.md
    md.tags = tagsWanted()
    md.hp = showMode("TagHealth", SHOW_BAR)
    md.sta = showMode("TagStamina", SHOW_OFF)
    md.age = ageWanted()
    for i = 1, #NEED_ROWS do md.nd[i] = showMode(NEED_ROWS[i].opt, SHOW_OFF) end      -- F3: Hunger, Durst, Muedigkeit, Vertrauen
    local cfg = B.CFG
    local reach = cfg.hudDist or 20
    local max = cfg.hudMax or 6
    local found = {}
    for id, c in pairs(cubs) do
        local a = S.objs[id]
        if a ~= nil and wanted(c) and (c.st ~= "tame" or tameShown(c, md)) and alive(a) then
            local dx = a:getX() - px                    -- client/TimedActions/ISContextualActions.lua:100
            local dy = a:getY() - py
            local d2 = dx * dx + dy * dy
            if d2 <= reach * reach then
                found[#found + 1] = { a = a, c = c, d2 = d2 }
            end
        end
    end
    if #found > 1 then table.sort(found, byDist) end
    local n = #found
    if n > max then n = max end
    if n > 0 then
        local meKey = view.me and view.me.key
        local nowH = B.Now()
        for i = 1, n do
            describe(found[i], meKey, nowH)
        end
    end
    S.list = found
    S.n = n

    -- 4. Koeder-Schild
    S.bait = baitEntry(view, px, py)
end

-- ---------------------------------------------------------------------------
-- Zeichnen (je Bild, nur aus der fertigen Liste)
-- ---------------------------------------------------------------------------

-- Text mit Schatten, sonst ist heller Text auf Sand oder Beton unlesbar. drawTextCentre(text, x, y, r, g, b, a, Schrift):
-- client/ISUI/ISUIElement.lua:1280 (UIFont.Small); mit UIFont.NewSmall: client/Foraging/ISSearchManager.lua:148.
local function text(self, str, x, y, r, g, b, a, font)
    self:drawTextCentre(str, x + 1, y + 1, 0, 0, 0, 0.7, font)
    self:drawTextCentre(str, x, y, r, g, b, a, font)
end

-- Namensschild: der Block waechst vom Anker nach OBEN -- Zeile 2 (klein, blasser) sitzt mit ihrer Unterkante am Anker, Zeile 1
-- 1 px darueber (Plan 2.2). Gerade gezaehmt: Zeile 2 blinkt gruen "Tamed!" (450 von 700 ms an), danach der Zustand.
-- B1c: Schriften und Hoehen aus der Groessenstufe t (Stufe 1 = Small / NewSmall wie B1b). drawTextCentre mit UIFont.Medium:
-- V:client/ISUI/ISFitnessUI.lua:204; mit UIFont.Large: V:client/Chat/ISAlert.lua:35.
-- B1d: Wert-Balken (Leben rot, Ausdauer gelb) mit der Oberkante bei top; Masse der Groessenstufe t, Hintergrund und Rahmen wie der
-- Zaehm-Balken (drawRect / drawRectBorder (x, y, w, h, a, r, g, b): V:client/ISUI/ISUIElement.lua:1191 / :1219). Ohne Text.
local function valueBar(self, sx, top, fill, t, r, g, b)
    local bw, bh = t.barW, t.barH
    local bx = sx - bw / 2
    self:drawRect(bx - 1, top - 1, bw + 2, bh + 2, 0.65, 0, 0, 0)
    if fill > 0 then
        self:drawRect(bx, top, fill, bh, 0.95, r, g, b)
    end
    self:drawRectBorder(bx - 1, top - 1, bw + 2, bh + 2, 0.9, 0.85, 0.85, 0.80)
end

-- B1d: das ganze Schild eines gezaehmten Jungen. Die Lagen (e.yState, e.yAge, e.yHp, e.ySta = Oberkante ueber dem Anker) stehen
-- fertig im Eintrag (describeValues); gezeichnet wird von oben nach unten, damit Name und Zustand wie in B1b/B1c zuerst kommen.
-- Ohne Werte-Zeilen ist e.yState = t.h2: genau das Schild von B1c.
local function drawTag(self, e, sx, sy, now, t)
    if e.showName then
        local y2 = sy - e.yState
        -- F3: das Herz mittig ueber dem Namen, 1:1 (Kantenlaenge = Bildgroesse, gerade Zahl -> ganze Pixel). drawTextureScaled(tex, x, y,
        -- w, h, a, r, g, b): V:client/Chat/ISChat.lua:418 (wie S:client/ISUI/BanditsNPCBearMarker.lua)
        if e.heart then
            local hs = e.heartS
            self:drawTextureScaled(e.heart, sx - hs / 2, y2 - 1 - t.h1 - HEART_GAP - hs, hs, hs, 1, 1, 1, 1)
        end
        text(self, e.line1, sx, y2 - 1 - t.h1, e.r, e.g, e.b, 0.95, t.f1)
        if now < e.till then
            if (now % 700) < 450 then
                text(self, e.flashLine, sx, y2, 0.55, 1.0, 0.55, 1.0, t.f2)
            end
        elseif e.l2 then
            text(self, e.line2, sx, y2, e.l2[2], e.l2[3], e.l2[4], 0.90, t.f2)       -- F2: Kampfzustand / am Boden
        else
            text(self, e.line2, sx, y2, 0.78, 0.78, 0.74, 0.80, t.f2)
        end
    end
    if e.ageLine then
        text(self, e.ageLine, sx, sy - e.yAge, 0.78, 0.78, 0.74, 0.80, t.f2)
    end
    -- F3: Vertrauen, Muedigkeit, Durst, Hunger (von oben nach unten; die Liste steht von unten nach oben)
    for i = e.ndN or 0, 1, -1 do
        local line = e.nd[i]
        local row = line.row
        if line.fill then
            valueBar(self, sx, sy - line.y, line.fill, t, row.r, row.g, row.b)
        else
            text(self, line.text, sx, sy - line.y, row.tr, row.tg, row.tb, 0.90, t.f2)
        end
    end
    if e.hpFill then
        valueBar(self, sx, sy - e.yHp, e.hpFill, t, 0.85, 0.20, 0.20)
    elseif e.hpText then
        text(self, e.hpText, sx, sy - e.yHp, 0.96, 0.64, 0.62, 0.90, t.f2)
    end
    if e.staFill then
        valueBar(self, sx, sy - e.ySta, e.staFill, t, 0.95, 0.80, 0.25)
    elseif e.staText then
        text(self, e.staText, sx, sy - e.ySta, 0.96, 0.88, 0.56, 0.90, t.f2)
    end
end

-- Zaehm-Balken wie B1a (Zeile 2 unten am Anker, darueber der Balken, darueber Zeile 1); nur der Anker ist neu.
-- B1c: Balkenbreite, -hoehe und Abstaende aus der Groessenstufe t (Stufe 1: 64 x 7, 4 und 2 px wie B1b).
local function drawBar(self, e, sx, sy, t)
    local fh = t.h1
    local bw, bh = t.barW, t.barH
    local bx = sx - bw / 2
    local by = sy - fh - bh - t.gap
    text(self, e.line1, sx, by - fh - t.gap2, 0.96, 0.96, 0.90, 0.95, t.f1)
    self:drawRect(bx - 1, by - 1, bw + 2, bh + 2, 0.65, 0, 0, 0)
    if e.fill > 0 then
        if e.unfed then
            self:drawRect(bx, by, e.fill, bh, 0.95, 0.95, 0.70, 0.25)
        else
            self:drawRect(bx, by, e.fill, bh, 0.95, 0.45, 0.85, 0.35)
        end
    end
    self:drawRectBorder(bx - 1, by - 1, bw + 2, bh + 2, 0.9, 0.85, 0.85, 0.80)
    text(self, e.line2, sx, sy - fh, 0.90, 0.90, 0.85, 0.80, t.f1)
end

-- Das Element liegt bei 0,0 und wird nie verschoben: seine Koordinaten sind Bildschirm-Koordinaten.
-- isoToScreenX/Y(Spielernummer, x, y, z): client/Fishing/TensionUI.lua:11-12 (erstes Argument eine Zahl).
-- drawRect / drawRectBorder (x, y, w, h, a, r, g, b): client/ISUI/ISUIElement.lua:1191 / :1219.
-- Anker fuer Balken UND Schild: a:getZ() + B.CFG.tagZ (Plan 2.2; je Bild gelesen, damit ein geaenderter Stellwert sofort wirkt).
-- B1d: beim gezaehmten Jungen mal e.zk = gezeigte Groesse / tagBase (im Listenbau gerechnet; wilde Junge 1).
local function draw(self, now)
    local cfg = B.CFG
    local lift = tonumber(cfg.tagZ) or TAG_Z
    local small = UIFont.Small
    local t = S.tier or tierOf(1)
    for i = 1, S.n do
        local e = S.list[i]
        local a = e.a
        if a:isExistInTheWorld() then
            local x = a:getX()
            local y = a:getY()
            local z = a:getZ() + lift * (e.zk or 1)
            local sx = math.floor(isoToScreenX(0, x, y, z))
            local sy = math.floor(isoToScreenY(0, x, y, z))
            if e.tag then
                drawTag(self, e, sx, sy, now, t)
            else
                drawBar(self, e, sx, sy, t)
            end
        end
    end
    local bait = S.bait
    if bait then
        local fh = fontH
        local sx = math.floor(isoToScreenX(0, bait.x, bait.y, bait.z))
        local sy = math.floor(isoToScreenY(0, bait.x, bait.y, bait.z))
        text(self, bait.line1, sx, sy - fh * 2 - 2, 0.98, 0.85, 0.45, 0.95, small)
        text(self, bait.line2, sx, sy - fh, 0.90, 0.90, 0.85, 0.80, small)
    end
end

-- Ein Panel sagt zu jedem Klick ja, wenn man es laesst: ausdruecklich nein.
function Hud:onMouseDown() return false end
function Hud:onMouseUp() return false end
function Hud:onRightMouseDown() return false end

function Hud:prerender()
    ISPanel.prerender(self)
    if not B.View or not B.CFG or not B.T then return end
    -- Geteilter Bildschirm: lieber nichts als auf der falschen Haelfte. getNumActivePlayers: client/Fishing/FishingHandler.lua:6.
    -- Nachbesserung B1d B6: auf dem MP-Client wird die Liste trotzdem gebaut (nur nicht gezeichnet) -- sie traegt die Groessen-Probe
    -- der Client-Kopien (rebuild Schritt 1). isClient(): V:client/ISUI/ISWorldObjectContextMenu.lua:1435 (nur bei geteiltem Bildschirm).
    local split = getNumActivePlayers() > 1
    if split and not isClient() then return end
    local now = getTimestampMs()                        -- client/Foraging/ISBaseIcon.lua:485
    if S.dirty or now - S.listAt >= LIST_MS or now < S.listAt then
        if not fontH then
            -- Schrifthoehen einmal holen. getFontHeight(UIFont.Small): client/ISUI/Animal/ISAnimalUI.lua:4;
            -- getFontHeight(UIFont.NewSmall): client/Entity/ISUI/Controls/ISWidgetTitleHeader.lua:4. Statisch entschieden
            -- (Nachbesserung B1b A3): in JEDER Vanilla-Sprache laden "font NewSmall" und "font Small" dieselbe Datei
            -- (media/fonts/EN/fonts.txt:75-79 und :93-97, ebenso CN, CH, JP, KO, PL, RU, TH) -- Zeile 2 ist also gleich gross, nur
            -- blasser. Der Vergleich bleibt (schadet nicht, greift, falls ein Schriftsatz NewSmall einmal kleiner macht); kleiner
            -- zeichnen ginge nur mit drawTextZoomed, das Vanilla nirgends aufruft (braucht Kevins Wort).
            local tm = getTextManager()
            fontH = tm:getFontHeight(UIFont.Small)
            local hNew = tm:getFontHeight(UIFont.NewSmall)
            if type(hNew) == "number" and hNew > 0 and hNew < fontH then
                font2 = UIFont.NewSmall
                fontH2 = hNew
            else
                font2 = UIFont.Small
                fontH2 = fontH
            end
        end
        rebuild(now)
    end
    if split then return end
    if S.n > 0 or S.bait then
        draw(self, now)
    end
    -- F2 (PLAN_F2.md 3.2, Nachtrag 11.1): "DODGE" / "down" und Schadenszahlen (client/BanditsNPCBearFx.lua), nur aus fertigen Listen
    if U.FloatDraw then U.FloatDraw(self, now) end
    -- F3 (PLAN_F3.md 8): z Z z ueber schlafenden Baeren (client/ISUI/BanditsNPCBearZz.lua), nur aus seiner fertigen Liste
    if U.ZzDraw then U.ZzDraw(self, now) end
end

-- F3 (PLAN_F3.md 8): Hoehe des ganzen Schild-Stapels eines Baeren ueber seinem Anker in Pixeln (Werte-Zeilen, Zustand, Name, Herz) --
-- 0, wenn er gerade kein Schild hat. Fuer das z Z z, das darueber beginnt. Nur aus der fertigen Liste (hoechstens hudMax Eintraege);
-- gerufen vom 1-s-Sammler des z Z z, nie je Bild.
function U.TagTop(id)
    if id == nil then return 0 end
    for i = 1, S.n do
        local e = S.list[i]
        if e.tag and e.c and e.c.id == id then return e.top or 0 end
    end
    return 0
end

-- ---------------------------------------------------------------------------
-- Junge mit Objekt in der Naehe (B1b, Plan 3.2 / 5.4): fuer "Futter hinhalten" im Welt-Menue. Quelle sind die Objekte, die der
-- Balken ohnehin kennt (S.objs) -- kein Suchlauf, kein Server-Weg. Liste { id, c, a, d }, naechste zuerst. Laeuft nur auf
-- Rechtsklick. getX/getY am Tier: client/TimedActions/ISContextualActions.lua:100; isExistInTheWorld/isDead siehe alive().
-- ---------------------------------------------------------------------------
local function byD(a, b)
    return a.d < b.d
end

function U.CubsNear(playerObj, radius)
    local out = {}
    if not playerObj or not U.Fresh or not U.Fresh() then return out end
    local cubs = B.View and B.View.cubs
    if type(cubs) ~= "table" then return out end
    local r = tonumber(radius) or 0
    if r <= 0 then return out end
    local px = playerObj:getX()                         -- client/Fishing/TensionUI.lua:11
    local py = playerObj:getY()
    for id, c in pairs(cubs) do
        local a = S.objs[id]
        if a ~= nil and alive(a) then
            local dx = a:getX() - px
            local dy = a:getY() - py
            local d = math.sqrt(dx * dx + dy * dy)
            if d <= r then
                out[#out + 1] = { id = id, c = c, a = a, d = d }
            end
        end
    end
    if #out > 1 then table.sort(out, byD) end
    return out
end

-- ---------------------------------------------------------------------------
-- B1c (PLAN_B1C.md 6.4): die lebende Client-Kopie eines Jungen fuer Markierung und Karte -- aus derselben Tabelle wie der
-- Balken (S.objs), ohne eigenen Suchlauf. Nur auf Abruf (Markierung je 400 ms, Karte je 500 ms), nie je Bild.
-- U.CubObj(id): das Objekt, wenn es lebt UND sein Sicht-Eintrag noch diese Kennung ist (B.ViewOf: Spiegel bzw. OnlineID), sonst
-- nil -- schuetzt davor, einer anderen Figur zu folgen, falls die Engine ein Objekt weiterreicht.
-- U.CubPos(id): x, y, z dieser Kopie oder nil. getX/getY/getZ am Tier: client/TimedActions/ISContextualActions.lua:100.
-- ---------------------------------------------------------------------------
function U.CubObj(id)
    if id == nil then return nil end
    local a = S.objs[id]
    if a == nil or not alive(a) then return nil end
    local v = B.ViewOf and B.ViewOf(a)
    if not v or v.id ~= id then return nil end
    return a
end

function U.CubPos(id)
    local a = U.CubObj(id)
    if a == nil then return nil end
    return a:getX(), a:getY(), a:getZ()
end

-- ---------------------------------------------------------------------------
-- Naht zum Kern (Plan 6.2.4): B.ApplySync ruft das nach jeder neuen Sicht.
-- ---------------------------------------------------------------------------
function B.OnView()
    S.dirty = true
    if U.NoteSync then U.NoteSync() end
    if U.WinOnView then U.WinOnView() end           -- F1: Baeren-Fenster (client/ISUI/BanditsNPCBearWindow.lua)
    if U.PoseOnView then U.PoseOnView() end         -- F1: Sitz-Treiber (client/BanditsNPCBearPose.lua)
end

-- Je Spielstart ein frisches Element. Ein altes (Hauptmenue und neu laden) wird vorher abgemeldet und vergessen:
-- removeFromUIManager ist Vanillas eigenes Lua (client/ISUI/ISUIElement.lua:1373) und tut nichts, wenn es schon weg ist.
local function onGameStart()
    if panel then panel:removeFromUIManager() end
    reset()
    panel = Hud:new(0, 0, 1, 1)
    panel:initialise()                                  -- client/ISUI/Animal/ISAnimalContextMenu.lua:746
    panel:noBackground()                                -- client/ISUI/ISPanel.lua:9
    panel:addToUIManager()                              -- client/ISUI/Animal/ISAnimalContextMenu.lua:747
end

Events.OnGameStart.Add(onGameStart)                     -- client/Chat/ISChat.lua:1186
