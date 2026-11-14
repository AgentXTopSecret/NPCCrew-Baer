--
-- NPC Crew -- Baer, das Baeren-Fenster (F1, PLAN_F1.md 0.1, 0.4, 0.10, 1.1, 1.8; Kevin 11.11.2026: "ich wll noch spaeter eine richtige
-- UI die aufgeht wenn ich V druecke (einstellbar in den keystings)" -- "das schoene ui").
--
-- Ein eigenes ISPanel mit moveWithMouse (Vanilla V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1, :243, :253; Ziehen
-- V:client/ISUI/ISPanel.lua:49-95), NICHT ISCollapsableWindow (dessen Titelleiste nimmt fest UIFont.Small, ISCollapsableWindow.lua:398-399,
-- bei 4K winzig). Alles waechst mit EINEM Faktor f = U.MarkerFactor(Bildschirmhoehe, Option WinSize) (B1e, 1080 -> 1,0, Kevins
-- 2054 -> 2,0); Zeilenhoehen aus der echten Schrifthoehe, Breiten aus MeasureStringX -- so passt es bei jeder Vanilla-Schriftgroesse.
-- Aufbau (PLAN_F1.md 1.1; seit F3 Variante B, siehe unten): Kopf (Kevins Symbol 1, Name + Umbenennen, Koerper/Tag, naechste Stufe,
-- Zustand-Chip, Abstand, Pfeile bei mehreren Baeren, Schliessen), Karten "Condition" | "Needs" | "Skills", Karte "Orders" (Befehle,
-- Handgriffe, Schalter), Fusszeile. Bausteine: client/ISUI/BanditsNPCBearWinParts.lua; Inhalt:
-- client/BanditsNPCBearWinData.lua (U.WinModel).
-- Takt (nichts Teures je Bild, PLAN_F1.md 0.10): das Modell entsteht nur bei neuer Sicht (U.WinOnView) und hoechstens 1 x je Sekunde,
-- nur solange das Fenster offen ist; je Bild wird nur aus fertigen Feldern gezeichnet. Geschlossen: kein Bau, kein Zeichnen.
-- Befehle gehen als Bitte an den Schreiber (B.Ask: Einzelspieler B.Handle direkt, Mehrspieler sendClientCommand, Rolle user genuegt);
-- Besitz, Lage und Abklingzeit prueft der Schreiber. Das Fenster setzt nie einen Wert selbst (kein Cheat).
-- Nur Spieler 0 (wie V:client/ISUI/Hutch/ISHutchUI.lua:884-893). Kein Schliessen wegen Abstand (F-j).
-- F1B (PLAN_F1B.md 0 E8, E11, 1.7, 5.3; Kevin 12.11.2026: "bei E das baeren ui zu oeffnen" und "einen schalter haben das die anzeige
-- aus geht wann der waechst und wenn er bei 100% ist soll der knopf ganz verschwinden"): das Fenster verbraucht nur noch Esc -- Auf/Zu
-- mit der Nah-Taste (E) und der Fern-Taste macht allein client/BanditsNPCBearKey.lua (OnKeyPressed). So bekommen alle anderen
-- Lua-Hoerer ihre Taste auch bei offenem Fenster (NC "Talk to NPC" auf V, Moebel-Cursor und NC-Stationen auf E). Dazu der dritte
-- Schalter "Growth line" (Wachstums-Zeile UEBER diesem Baeren an/aus, je Spieler wie "Name tag", client/BanditsNPCBearTags.lua) in der
-- bisher leeren dritten Zelle der Schalterreihe; ist der Baer ausgewachsen (Sicht ohne nst), verschwindet der Schalter (setVisible) --
-- Breite, Hoehe und alle anderen Kinder haengen nicht daran, die Zelle bleibt leer, nichts springt.
-- F2 = B5a (PLAN_F2.md 3.2, Nachtrag 11.1/11.2/11.5): Karte "Condition" bekommt zwei Wert-Zeilen "Melee damage" und "Kills" (nach "Can
-- carry", gleiche Machart); Karte "Orders" eine vierte Reihe: Zelle 1 der Pflege-Knopf "Bandage" bzw. am Boden "Help up" (U.MendAsk /
-- U.HelpAsk: hingehen, Zeitaktion -- entscheiden tut der Schreiber), Zelle 2 der Schalter "Show damage" (je Spieler, U.DmgSet). ABWEICHUNG
-- vom Plan (schnittstelle_aenderungen.md "F2 OBERFLAECHE"): PLAN_F2.md 3.2 wollte den Knopf in die dritte Zelle der Schalter-Reihe -- die
-- belegt seit F1B "Growth line". Feste Hoehe (beide Zeilen und die Reihe stehen immer, auch beim Jungen mit "--"): nichts springt, wenn er
-- waechst, kaempft oder zu Boden geht.
-- Aussehen (Lauf baer-aussehen, PLAN_AUSSEHEN.md 8.1; Kevin 12.11.2026: "ja fuer spieler als knopf"): Knopf "Look: <Name>" in der bisher
-- freien Zelle 3 der vierten Reihe (Fensterhoehe unveraendert; Breite misst alle Namen und die Uhr). Klick oeffnet Vanillas Kontextmenue
-- am Knopf mit allen Aussehen dieses Koerpers (das jetzige abgehakt, ohne Funktion); die Wahl schickt die Bitte "Look" { id, look } an
-- den Schreiber (B.Ask) -- Besitz, Zustand, Zombies, Platz und die gemeinsame Uhr mit Unstuck prueft der Schreiber (B.HandleLook).
-- Kennt der Kern kein Aussehen (Modell ohne d.look), bleibt die Zelle leer (Knopf unsichtbar).
-- F3 (Lauf baer-f3, PLAN_F3.md 10; Kevin 12./13.11.2026: Variante B FEST): NEUE ANORDNUNG -- drei Karten nebeneinander
--   Condition (Leben, Ausdauer, Can carry, Melee damage, Kills) | Needs (Hunger, Thirst, Tiredness, Trust als Balken mit Prozent) |
--   Skills (6 Faehigkeiten), darunter die Karte "Orders" mit FUENF Spalten in drei Reihen:
--   Reihe 1 Befehle   Follow | Stay | Sit | Roam free | Come here
--   Reihe 2 Handgriffe Fish (grau bis F5) | Unstuck | Look | Inventory (grau bis F4) | Bandage bzw. Help up
--   Reihe 3 Schalter  Passive | Nose alerts (grau bis F5) | Name tag | Show damage | Growth line (verschwindet ausgewachsen: die Luecke
--                     liegt am Reihenende wie seit F1B).
-- Aus dem Prototyp ui_entwurf/proto nur der Zweig "wide" (Masse und Lagen); die Zeile "Coming later", die Trennlinie der linken Karte und
-- die vierte Reihe gibt es nicht mehr. Das Fenster wird breiter und NIEDRIGER als bisher (1080p EN etwa 769 x 615 statt 640 x 682). Die
-- grauen Platzhalter sind gewoehnliche graue Knoepfe / ein grauer Schalter mit Grund im Tooltip: kein Klick, keine Bitte -- F4 / F5
-- schalten sie nur scharf, nichts wandert spaeter. Kein Schlaf-Knopf (Kevin 6e): jeder Befehl weckt. Die Fusszeile zeigt in Warnfarbe,
-- wenn der Baer nicht kaempft (zu muede / kein Vertrauen, client/BanditsNPCBearWinData.lua d.footerCol).
-- F4 (Lauf baer-f4, PLAN_F4.md 7, 8.1): der Knopf "Inventory" (Reihe 2, Zelle 4) ist scharf und oeffnet das Inventar-Fenster dieses Baeren
-- (U.InvOpen, client/ISUI/BanditsNPCBearInvWindow.lua) -- auch von weitem (Kevin Antwort 2: ansehen ueberall). Die Zeile "Can carry" heisst
-- jetzt "Load" (Inhalt aus client/BanditsNPCBearWinData.lua; Lage und Masse unveraendert).
-- K1 (Lauf baer-k1, PLAN_K1.md 1.5, 4 Z; Kevin 14.11.2026 I1 "zahnrad menue einbauen in baeren ui fuer mehr platz im ui fuer unnoetige
-- ausblendungknoepfe"): ZAHNRAD oben rechts neben "Schliessen" -- Vanillas Knopf mit Vanillas Bild media/ui/inventoryPanes/Button_Gear.png (Form
-- des Chat-Zahnrads V:client/Chat/ISChat.lua:130-140), Klick oeffnet Vanillas Kontextmenue am Zahnrad (ISChat.lua:245-272: ISContextMenu.get,
-- addOption, setOptionChecked) mit den Ausblend-Schaltern Name tag / Health bar (NEU) / Show damage / Growth line (nur solange er waechst) /
-- Nose alerts (grau bis F5); Haken = an. Die Punkte kommen fertig aus dem Modell (d.gear, client/BanditsNPCBearWinData.lua). Reihe 3 der
-- Befehle traegt nur noch "Passive" (Zelle 1; der Rest bleibt frei fuer spaeter); Fensterhoehe unveraendert, nichts springt. Pfeile bei
-- mehreren Baeren ruecken um ein Zahnrad nach links.
-- TALENTE (Lauf baer-talente, PLAN_TALENTE.md 5.1; Kevin 14.11.2026 "im skilltree auf einen extra tab kann man die skillpunkte aisgeben",
-- ~10:20 "Freie Wahl"): unter dem Kopf eine REITERLEISTE "Overview" | "Perks" (U.WinBtn Stil "tab", am zweiten ein Honig-Abzeichen mit der Zahl
-- freier Talentpunkte). "Overview" zeigt alles wie bisher; "Perks" zeigt EINE Karte mit 3 x 3 Kacheln, Kopf- und Fusszeile und dem Knopf
-- "Reset" (client/ISUI/BanditsNPCBearTalentTab.lua, Modell client/BanditsNPCBearTalentData.lua). Beide Reiter sind gleich hoch (die
-- Talent-Karte nimmt genau die Flaeche der drei Karten + Befehle), das Fenster wird um eine Reiterzeile hoeher (1080p: 29 px). Wechsel: offene
-- Tooltips abmelden (hideTip), dann setVisible je Kind (V:client/ISUI/ISButton.lua:9). Der gewaehlte Reiter gilt nur in dieser Sitzung.
-- Die Leiste gibt es nur, wenn der Kern die Talente kennt (B.TALENTS / B.TalentCan) und die Kachel-Datei geladen ist -- sonst ist das Fenster
-- genau wie vorher. Lernen / Zuruecksetzen erst nach Vanillas Ja/Nein-Fenster, dann eine Bitte an den Schreiber (U.TalentAsk).
-- Jeder Engine-Aufruf hat eine Vanilla-Fundstelle (Kommentar daneben). Statisch geprueft, nicht gespielt.
--

require "ISUI/ISPanel"
require "ISUI/ISButton"

BanditsNPC = BanditsNPC or {}
BanditsNPC.Bear = BanditsNPC.Bear or {}
local B = BanditsNPC.Bear
B.UI = B.UI or {}
local U = B.UI

-- Klasse bleibt ein Local. ISPanel:derive: V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:1.
local Win = ISPanel:derive("BanditsNPCBearWindow")

local LAYOUT_NAME = "BanditsNPCBearWindow"      -- Name in Vanillas layout.ini (eindeutig, Kollisionsprobe forschung_f1.md 8)
local MODEL_MS = 1000
local FIT = 0.92                                -- passt das Fenster nicht in 92 % der Bildhoehe, wird f eine Stufe kleiner
local ICON_FILE = "media/ui/BanditsNPCBearCub_marker288.png"
local DISC_FILE = "media/ui/BanditsNPCBearMarker_disc.png"
local CLOSE_FILE = "media/ui/inventoryPanes/Button_Close.png"
local GEAR_FILE = "media/ui/inventoryPanes/Button_Gear.png"   -- K1: Vanillas Zahnrad-Bild (V:client/Chat/ISChat.lua:137)
local CMDS = { "follow", "stay", "sit", "roam", "come", "unstuck", "fish", "inv" }     -- F3: + fish (grau bis F5), inv (F4 scharf)
local NEEDS = { "hun", "thr", "tir", "tru" }                                            -- F3: Balken-Zeilen der Karte "Needs"
-- F3 (PLAN_F3.md 10.2): Reihe 1 und die ersten vier Zellen von Reihe 2 der Befehle (Zelle 3 von Reihe 2 = Knopf "Look", Zelle 5 = Pflege)
local ROW1 = { "follow", "stay", "sit", "roam", "come" }
local ROW2 = { "fish", "unstuck", false, "inv" }

-- Alles, was das Fenster sich merkt (nur diese Sitzung): genau EIN Fenster-Objekt je Spielstart.
local W = { win = nil, tex = nil }

local function col(key)
    local c = U.WIN_COL and U.WIN_COL[key]
    return c or { 1, 1, 1, 1 }
end

-- Textbreite. getTextManager():MeasureStringX(Schrift, Text): V:client/ISUI/ISButton.lua:450, :233.
local function tw(font, s)
    if s == nil or s == "" then return 0 end
    return getTextManager():MeasureStringX(font, s)
end

local function screen()
    local core = getCore()
    return core:getScreenWidth(), core:getScreenHeight()   -- V:client/Challenge/WinterIsComing.lua:18
end

-- Optionswert WinSize (Index der Auswahl, client/BanditsNPCBearOptions.lua): 1 = Auto. Fehlt die Seite: Auto.
local function sizeIdx()
    local v = 1
    if U.Opt then v = tonumber(U.Opt("WinSize", 1)) or 1 end
    return math.floor(v)
end

local function factor(h, idx)
    if U.MarkerFactor then return U.MarkerFactor(h, idx) end
    return 1, 1
end

-- ---------------------------------------------------------------------------
-- Masse (PLAN_F1.md 1.1, Pixel bei f = 1, jede Zahl x f gerundet; lb / ls / ln = Zeilenhoehe Text / Klein / Name). Dieselbe Rechnung wie
-- f1_entwurf/zeichne_fenster.py window(). Gibt die Tabelle m mit allen Massen und Lagen; misst die festen Texte (Breite waechst nur,
-- wenn ein Text nicht passt). Nur beim Legen.
-- ---------------------------------------------------------------------------
-- Breite, die die wechselnden Texte brauchen (Name + Umbenennen + Pfeile, Koerper/Stufe neben dem Chip, Hinweis der Befehle,
-- Fusszeile). Mit den Schriften und festen Breiten aus m; im 1-s-Takt nur diese wenigen Messungen (layoutStale).
local function dynNeed(m, d, n)
    local P = m.P
    local need = 0
    local function grow(v) if v > need then need = v end end
    local right = m.R24 + m.R6 + m.R24                  -- K1: Schliessen + Zahnrad
    local countW = 0
    if n > 1 then
        countW = math.max(tw(m.fSmall, d and d.count), m.R28)
        right = right + m.R6 + m.R24 + m.R6 + countW + m.R6 + m.R24
    end
    local nameW = tw(m.fName, d and d.name)
    grow(m.tx + nameW + m.bold + m.R12 + m.renameW + m.R16 + right + P)
    local subW = math.max(tw(m.fBody, d and d.sub), tw(m.fBody, d and d.next))
    grow(m.tx + subW + m.R16 + math.max(m.chipMax, m.distW) + P)
    grow(2 * P + m.R24 + m.ordTitleW + m.R16 + tw(m.fSmall, d and d.ordersInfo))
    grow(2 * P + tw(m.fSmall, d and d.footer))
    return need, nameW, countW
end

local function metrics(f, d, n, sw, sh, idx)
    local m = { f = f, n = n, sw = sw, sh = sh, idx = idx }
    local function R(v) return math.floor(v * f + 0.5) end
    for _, v in ipairs({ 2, 3, 4, 6, 8, 9, 10, 12, 14, 16, 24, 28, 36, 40, 44, 46, 72, 80, 94, 100 }) do m["R" .. v] = R(v) end
    m.t = math.max(1, math.floor(f))
    m.bar = R(4)
    m.bold = math.max(1, math.floor(f / 2))
    m.ox, m.oy = R(8), R(3)
    m.fName, m.fBody, m.fSmall, m.ln, m.lb, m.ls = U.WinFonts(f)
    local P = R(16)
    m.P = P
    local lb, ls, ln = m.lb, m.ls, m.ln
    m.headH = math.max(R(100), R(14) + ln + R(2) + lb + R(2) + lb + R(10))
    m.rowBar = lb + R(4) + R(10) + R(10)
    m.rowVal = lb + R(10)
    m.rowSk = lb + R(4) + R(8) + R(8)
    -- F3 (Variante B): drei Karten gleicher Hoehe -- Condition (2 Balken + 3 Werte) | Needs (4 Balken) | Skills (6 Faehigkeiten)
    local top = R(10) + lb + R(8)                       -- Kartenrand + Titel bis zur ersten Zeile
    local c1 = top + 2 * m.rowBar + 3 * m.rowVal + R(4)
    local c2 = top + 4 * m.rowBar + R(4)
    local c3 = top + 6 * m.rowSk + R(4)
    m.cardH = math.max(c1, c2, c3)
    m.bh = math.max(R(34), lb + R(12))
    m.th = math.max(R(30), lb + R(10))
    -- F3: Befehle in fuenf Spalten -- Reihe Befehle, Reihe Handgriffe, Reihe Schalter
    m.ordH = R(10) + lb + R(8) + m.bh + R(8) + m.bh + R(10) + m.th + R(12)
    -- Lauf baer-talente: Reiterleiste zwischen Kopf und Karten (nur mit Talenten; d.tal setzt das Modell)
    m.tal = (d ~= nil and d.tal ~= nil and U.TalentLayout ~= nil and U.TalentNeedW ~= nil)
    m.tabH = 0
    if m.tal then
        m.tabY = m.headH + R(8)
        m.tabH = lb + R(10)
    end
    m.y1 = m.headH + R(16) + m.tabH
    m.y2 = m.y1 + m.cardH + R(16)
    m.y3 = m.y2 + m.ordH + R(10)
    m.H = m.y3 + ls + R(14)
    m.chipH = lb + R(8)
    m.tx = P + R(94)
    m.ty = R(14)
    m.l2y = m.ty + ln + R(2)
    m.l3y = m.l2y + lb + R(2)
    m.rbh = ls + R(6)
    -- Breite: mindestens 640 x f; mehr nur, wenn ein Text nicht passt (PLAN_F1.md 1.1). Feste Texte hier (einmal je Legen),
    -- wechselnde in dynNeed.
    local s = (d and d.wide) or {}
    local need = R(640)
    local function grow(v) if v > need then need = v end end
    m.renameW = tw(m.fSmall, d and d.rename) + R(16)
    local chipMax = 0
    if type(s.state) == "table" then
        for _, txt in pairs(s.state) do chipMax = math.max(chipMax, tw(m.fBody, txt)) end
    end
    m.chipMax = R(28) + chipMax + R(12)
    m.distW = math.max(tw(m.fSmall, s.wideDist), tw(m.fSmall, s.wideDist2))
    m.ordTitleW = tw(m.fBody, s.tOrders)
    -- Karten: jede Spalte CW >= Etikett + Wert + 36 x f
    local cw = 0
    local function col2(a, b, extra) cw = math.max(cw, a + b + (extra or R(36))) end
    col2(tw(m.fBody, s.tHealth), tw(m.fBody, s.wideVal))
    col2(tw(m.fBody, s.tStamina), tw(m.fBody, s.wideVal))
    col2(tw(m.fBody, s.tCarry), tw(m.fBody, s.wideCarry))
    for _, t in ipairs({ s.tHunger, s.tThirst, s.tTired, s.tTrust }) do     -- F3: die vier Beduerfnis-Zeilen
        col2(tw(m.fBody, t), math.max(tw(m.fBody, s.widePctNeed), tw(m.fBody, s.off)))      -- Nachbesserung P3: "Off" bei Regler 0
    end
    col2(tw(m.fBody, s.tTrust), tw(m.fBody, s.wideTrust))                 -- K1: Vertrauen mit Vorzeichen und Nachkommastelle
    cw = math.max(cw, tw(m.fBody, s.tNeeds) + R(24), tw(m.fBody, s.tSkills) + R(24), tw(m.fBody, s.tCond) + R(24))
    col2(tw(m.fBody, s.tMelee), tw(m.fBody, s.wideMelee))                  -- F2 (11.2)
    col2(tw(m.fBody, s.tKills), tw(m.fBody, s.wideKills))                  -- F2 (11.5)
    local lvW, pctW = tw(m.fBody, s.wideLv), math.max(tw(m.fSmall, s.widePct), tw(m.fSmall, s.max), tw(m.fSmall, s.ageMax))
    if type(s.skName) == "table" then
        for i = 1, #s.skName do col2(tw(m.fBody, s.skName[i]), lvW + R(8) + pctW, R(44)) end
    end
    grow(2 * P + 3 * cw + 2 * R(16))                    -- F3: drei Karten
    -- Befehle: jeder Knopf bw >= laengster Knopftext + 24 x f; Schalter: Kaestchen + Abstaende + Text
    local bwNeed = 0
    if type(s.btn) == "table" then
        for _, txt in pairs(s.btn) do bwNeed = math.max(bwNeed, tw(m.fBody, txt) + R(24)) end
    end
    bwNeed = math.max(bwNeed, tw(m.fBody, s.wideUnstuck) + R(24))
    bwNeed = math.max(bwNeed, tw(m.fBody, s.passive) + R(46))
    -- K1: Name tag, Growth line, Show damage, Nose alerts stehen im Zahnrad-Menue (Vanillas Kontextmenue misst sich selbst)
    -- F2: Pflege-Knopf (beide Texte)
    bwNeed = math.max(bwNeed, tw(m.fBody, s.bandage) + R(24), tw(m.fBody, s.helpUp) + R(24))
    -- Aussehen (PLAN_AUSSEHEN.md 8.1): "Look: <Name>" mit jedem Namen und "Look  9:59" -- immer mitgemessen, damit nichts springt
    bwNeed = math.max(bwNeed, tw(m.fBody, s.wideLook) + R(24))
    if type(s.lookLabels) == "table" then
        for i = 1, #s.lookLabels do bwNeed = math.max(bwNeed, tw(m.fBody, s.lookLabels[i]) + R(24)) end
    end
    -- F3: Fish, Inventory stehen in s.btn (oben gemessen). Fuenf Spalten.
    grow(2 * P + 5 * bwNeed + R(24) + 4 * R(8))
    local footW = 0
    for _, txt in ipairs({ s.hintMissing, s.hintRide, s.hintAway, s.hintEsc, s.hintSleep, s.hintTired, s.hintNoTrust }) do
        footW = math.max(footW, tw(m.fSmall, txt))
    end
    grow(2 * P + footW)
    if m.tal then grow(U.TalentNeedW(m)) end              -- Lauf baer-talente: Kacheln, Kopf- und Fusszeile, Reiter
    m.needStatic = need
    local dyn, nameW, countW = dynNeed(m, d, n)
    m.nameW, m.countW = nameW, countW
    if dyn > need then need = dyn end
    m.need = need
    -- Spaltenbreite ganzzahlig, Fensterbreite exakt daraus (keine Rundungsluecke am rechten Rand)
    m.CW = math.floor((need - 2 * P - 2 * R(16)) / 3 + 0.999)
    m.W = 2 * P + 3 * m.CW + 2 * R(16)
    m.ow = m.W - 2 * P
    m.bw = math.floor((m.ow - R(24) - 4 * R(8)) / 5)
    m.lx, m.mx, m.rx = P, P + m.CW + R(16), P + 2 * (m.CW + R(16))
    if m.tal then
        -- Lauf baer-talente: Lage der Talent-Karte; braucht sie mehr Hoehe, wird die Befehls-Karte hoeher (beide Reiter gleich hoch)
        U.TalentLayout(m)
        m.y3 = m.y2 + m.ordH + R(10)
        m.H = m.y3 + ls + R(14)
    end
    return m
end

-- Lage der Kinder (Knoepfe, Zeilen, Schalter) nach den Massen m. setX/setY/setWidth/setHeight: V:client/ISUI/ISUIElement.lua:195-245
-- (Vanilla ruft sie an Knoepfen, z. B. V:client/ISUI/ISCollapsableWindow.lua; Aufrufer V:client/ISUI/ISToolTip.lua:78-79).
local function put(el, x, y, w, h)
    el:setX(x)
    el:setY(y)
    el:setWidth(w)
    el:setHeight(h)
end

local function place(win, m)
    local P = m.P
    win:setWidth(m.W)
    win:setHeight(m.H)
    -- Kopf
    put(win.closeB, m.W - P - m.R24, m.R12, m.R24, m.R24)
    win.closeB:forceImageSize(m.R24, m.R24)          -- V:client/ISUI/ISInventoryPage.lua:1479
    -- K1: Zahnrad links neben Schliessen, gleiche Masse
    put(win.gearB, m.W - P - m.R24 - m.R6 - m.R24, m.R12, m.R24, m.R24)
    win.gearB:forceImageSize(m.R24, m.R24)           -- ISInventoryPage.lua:1479
    put(win.rename, m.tx + m.nameW + m.bold + m.R12, m.ty + math.floor((m.ln - m.rbh) / 2), m.renameW, m.rbh)
    win.rename.font, win.rename.fh = m.fSmall, m.ls
    local nx = m.W - P - m.R24 - m.R6 - m.R24 - m.R6 - m.R24
    put(win.nextB, nx, m.R12, m.R24, m.R24)
    m.countX = nx - m.R6 - math.floor(m.countW / 2)
    put(win.prevB, nx - m.R6 - m.countW - m.R6 - m.R24, m.R12, m.R24, m.R24)
    win.prevB.font, win.prevB.fh = m.fBody, m.lb
    win.nextB.font, win.nextB.fh = m.fBody, m.lb
    win.prevB:setVisible(m.n > 1)                   -- ISButton:setVisible V:client/ISUI/ISButton.lua:9
    win.nextB:setVisible(m.n > 1)
    -- F3 (Variante B, PLAN_F3.md 10.2): drei Karten -- jede Zeile liegt 4 x f im Kartenrand und 3 x f ueber ihrem Text
    local top = m.y1 + m.R10 + m.lb + m.R8
    local function row(el, x, yy, h) put(el, x + m.R4, yy - m.R3, m.CW - m.R8, h - m.R2) end
    -- Karte 1 "Condition": Leben, Ausdauer, Traglast, Melee damage (F2 11.2), Kills (F2 11.5)
    local yy = top
    row(win.rows.hp, m.lx, yy, m.rowBar)
    yy = yy + m.rowBar
    row(win.rows.sta, m.lx, yy, m.rowBar)
    yy = yy + m.rowBar
    row(win.rows.carry, m.lx, yy, m.rowVal)
    yy = yy + m.rowVal
    row(win.rows.melee, m.lx, yy, m.rowVal)
    yy = yy + m.rowVal
    row(win.rows.kills, m.lx, yy, m.rowVal)
    -- Karte 2 "Needs": Hunger, Durst, Muedigkeit, Vertrauen
    yy = top
    for i = 1, #NEEDS do
        row(win.rows[NEEDS[i]], m.mx, yy, m.rowBar)
        yy = yy + m.rowBar
    end
    -- Karte 3 "Skills": sechs Faehigkeiten
    yy = top
    for i = 1, 6 do
        row(win.rows[i], m.rx, yy, m.rowSk)
        yy = yy + m.rowSk
    end
    -- Befehle in fuenf Spalten: Zelle c (1..5) der Reihe bei y
    local function cell(el, c, y, h)
        put(el, P + m.R12 + (c - 1) * (m.bw + m.R8), y, m.bw, h)
        el.font, el.fh = m.fBody, m.lb
    end
    local by0 = m.y2 + m.R10 + m.lb + m.R8
    local by1 = by0 + m.bh + m.R8
    for c = 1, 5 do cell(win.btn[ROW1[c]], c, by0, m.bh) end                    -- Reihe 1: Befehle
    for c = 1, 4 do
        if ROW2[c] then cell(win.btn[ROW2[c]], c, by1, m.bh) end                -- Reihe 2: Fish, Unstuck, (Look), Inventory
    end
    cell(win.look, 3, by1, m.bh)                                                -- Aussehen (PLAN_AUSSEHEN.md 8.1): neben Unstuck (gemeinsame Uhr)
    cell(win.care, 5, by1, m.bh)                                                -- F2: "Bandage" / am Boden "Help up"
    local ty0 = by1 + m.bh + m.R8 + m.R2
    cell(win.tick.pas, 1, ty0, m.th)                    -- Reihe 3: nur noch "Passive" (K1: die anderen Schalter im Zahnrad-Menue)
    if m.tal and win.talTiles and U.TalentPlace then U.TalentPlace(win, m) end     -- Lauf baer-talente: Reiter, Kacheln, Reset
end

-- Auf den Bildschirm klemmen: mindestens 40 x f px sichtbar, Oberkante nie ueber dem Bild (PLAN_F1.md 1.1 "Lage").
local function clampPos(win)
    local m = win.m
    if not m then return end
    local sw, sh = screen()
    local keep = m.R40
    local x, y = win:getX(), win:getY()             -- V:client/ISUI/ISLayoutManager.lua:55-56
    local nx = math.max(keep - m.W, math.min(x, sw - keep))
    local ny = math.max(0, math.min(y, sh - keep))
    if nx ~= x then win:setX(nx) end
    if ny ~= y then win:setY(ny) end
end

-- ---------------------------------------------------------------------------
-- U.WinLayout(): Faktor, Schrift, Masse, Kinder neu legen (PLAN_F1.md 1.1, 1.7). Passt das Fenster nicht (H > 0,92 x Bildhoehe), eine
-- Stufe kleiner (U.MarkerFactor(h, k): Index k = Stufe k-1, bis 1,0).
-- ---------------------------------------------------------------------------
function U.WinLayout()
    local win = W.win
    if not win then return end
    local sw, sh = screen()
    local idx = sizeIdx()
    local f, k = factor(sh, idx)
    local m = nil
    for _ = 1, 8 do
        m = metrics(f, win.model, win.n or 1, sw, sh, idx)
        if m.H <= FIT * sh or (k or 1) <= 1 then break end
        f, k = factor(sh, k)
    end
    m.disc = W.tex and W.tex.disc
    win.m = m
    place(win, m)
    clampPos(win)
end

-- ---------------------------------------------------------------------------
-- Das Fenster
-- ---------------------------------------------------------------------------

-- ISPanel:new + eigene Felder (Form V:client/ISUI/AdminPanel/ISAdminTicketsUI.lua:243-253); Tasten wie
-- V:client/ISUI/Crafting/ISHandcraftWindow.lua:386 (setWantKeyEvents vor dem Anlegen speichert nur das Feld, ISUIElement.lua:1828-1831).
function Win:new(x, y, w, h)
    local o = ISPanel:new(x, y, w, h)
    setmetatable(o, self)
    self.__index = self
    o.moveWithMouse = true
    o.background = false                            -- eigener Hintergrund (Feld wie ISPanel:noBackground, V:client/ISUI/ISPanel.lua:9-11)
    o:setWantKeyEvents(true)
    o.dirty = true
    o.modelAt = 0
    o.n = 0
    o.idx = 1
    o.isOpen = false
    return o
end

-- Kinder einmal anlegen. ISButton:new(x, y, w, h, Titel, Ziel, Rueckruf) + initialise + addChild: V:client/ISUI/ISCollapsableWindow.lua:55-61
-- (dort auch das Bild am Schliessen-Knopf, setImage :60, Hintergrund-Alpha :57-59). Abgeleitete Klassen erben :new
-- (V:client/ISUI/ISResizeableButton.lua:1; Aufrufer V:client/ISUI/ISInventoryPane.lua:63). Titel immer "" -- die Texte zeichnen die
-- Klassen selbst aus fertigen Feldern.
local function kid(win, cls, cmd, style)
    local b = cls:new(0, 0, 10, 10, "", win, Win.onCmd)
    b:initialise()
    b.win, b.cmd, b.style, b.state = win, cmd, style, "normal"
    win:addChild(b)
    win.kids[#win.kids + 1] = b
    return b
end

function Win:build()
    self.kids = {}
    self.btn = {}
    for i = 1, #CMDS do self.btn[CMDS[i]] = kid(self, U.WinBtn, CMDS[i], "cmd") end
    self.rename = kid(self, U.WinBtn, "rename", "small")
    self.prevB = kid(self, U.WinBtn, "prev", "small")
    self.nextB = kid(self, U.WinBtn, "next", "small")
    self.prevB.label, self.nextB.label = "<", ">"
    self.tick = { pas = kid(self, U.WinTick, "passive") }                          -- K1: die anderen Schalter stehen im Zahnrad-Menue
    self.care = kid(self, U.WinBtn, "care", "cmd")                                  -- F2: "Bandage" / "Help up"
    self.look = kid(self, U.WinBtn, "look", "cmd")                                  -- Aussehen: "Look: <Name>"
    self.rows = {
        hp = kid(self, U.WinRow, nil), sta = kid(self, U.WinRow, nil), carry = kid(self, U.WinRow, nil),
        melee = kid(self, U.WinRow, nil), kills = kid(self, U.WinRow, nil),
    }
    -- F3: vier Balken-Zeilen der Karte "Needs" (derselbe Baustein wie Leben / Ausdauer) statt der Zeile "Coming later"
    for i = 1, #NEEDS do
        local r = kid(self, U.WinRow, nil)
        r.kind, r.key = "bar", NEEDS[i]
        self.rows[NEEDS[i]] = r
    end
    self.rows.hp.kind, self.rows.hp.key = "bar", "hp"
    self.rows.sta.kind, self.rows.sta.key = "bar", "sta"
    self.rows.carry.kind, self.rows.carry.key = "val", "carry"
    self.rows.melee.kind, self.rows.melee.key = "val", "melee"                      -- F2 (11.2)
    self.rows.kills.kind, self.rows.kills.key = "val", "kills"                      -- F2 (11.5)
    for i = 1, 6 do
        local r = kid(self, U.WinRow, nil)
        r.kind, r.key = "skill", i
        self.rows[i] = r
    end
    for _, r in pairs(self.rows) do r.onclick = nil end   -- Zeilen klicken nicht (ISButton.lua:42-44)
    -- Schliessen: Vanillas Knopf mit Vanillas Bild (wie ISCollapsableWindow.lua:55-61)
    local c = ISButton:new(0, 0, 10, 10, "", self, Win.onClose)
    c:initialise()
    c.borderColor.a = 0.0                           -- ISCollapsableWindow.lua:57
    local bg, hv = col("closeBg"), col("closeHover")
    c.backgroundColor = { r = bg[1], g = bg[2], b = bg[3], a = bg[4] }
    c.backgroundColorMouseOver = { r = hv[1], g = hv[2], b = hv[3], a = hv[4] }
    if W.tex and W.tex.close then c:setImage(W.tex.close) end   -- ISCollapsableWindow.lua:60
    self:addChild(c)
    self.kids[#self.kids + 1] = c
    self.closeB = c                                 -- nicht "close": das ist ISPanel:close (V:client/ISUI/ISPanel.lua:14)
    -- K1: Zahnrad wie Vanillas Chat (V:client/Chat/ISChat.lua:130-140: ISButton mit Bild, Rahmen aus) mit den Farben unseres Schliessen-Knopfs
    local g = ISButton:new(0, 0, 10, 10, "", self, Win.onGear)
    g:initialise()
    g.borderColor.a = 0.0                           -- ISChat.lua:134
    g.backgroundColor = { r = bg[1], g = bg[2], b = bg[3], a = bg[4] }
    g.backgroundColorMouseOver = { r = hv[1], g = hv[2], b = hv[3], a = hv[4] }
    if W.tex and W.tex.gear then g:setImage(W.tex.gear) end       -- ISChat.lua:137
    self:addChild(g)
    self.kids[#self.kids + 1] = g
    self.gearB = g
    -- Lauf baer-talente: Reiter, 9 Kacheln (U.WinTalent, client/ISUI/BanditsNPCBearTalentTab.lua) und "Reset" -- nur mit den Regeln des Kerns
    if U.WinTalent and U.TalentOn and U.TalentOn() then
        self.tabMainB = kid(self, U.WinBtn, "tabMain", "tab")
        self.tabTalB = kid(self, U.WinBtn, "tabTal", "tab")
        self.talTiles = {}
        for i = 1, #B.TALENTS do self.talTiles[i] = kid(self, U.WinTalent, "talent", nil) end
        self.talReset = kid(self, U.WinBtn, "talReset", "cmd")
        self.tab = "main"
    end
end

-- Offenen Tooltip EINES Kindes abmelden (wie ISButton:updateTooltip selbst: V:client/ISUI/ISButton.lua:341-343). F1B: auch fuer den
-- Wachstums-Schalter, bevor er unsichtbar wird -- ein unsichtbarer Knopf bekommt kein prerender mehr, sein Tooltip bliebe sonst stehen.
local function hideTip(el)
    local tip = el and el.tooltipUI
    if tip and tip:getIsVisible() then
        tip:setVisible(false)
        tip:removeFromUIManager()
    end
end

-- Offene Tooltips aller Kinder abmelden.
local function hideTips(win)
    if not win.kids then return end
    for i = 1, #win.kids do hideTip(win.kids[i]) end
end

-- Lauf baer-talente: ist der Reiter "Perks" gerade sichtbar?
local function talActive(win)
    return win.talTiles ~= nil and win.tab == "tal" and win.m ~= nil and win.m.tal == true
end

-- Sichtbarkeit nur bei einem Wechsel setzen, den Tooltip vorher abmelden (wie der Knopf "Look"; ISButton:setVisible V:client/ISUI/ISButton.lua:9,
-- getIsVisible :34).
local function setVis(el, want)
    if el and el:getIsVisible() ~= want then
        if not want then hideTip(el) end
        el:setVisible(want)
    end
end

-- Lauf baer-talente: Kinder je Reiter zeigen / verbergen. Ohne Talente (keine Kacheln) tut es nichts.
local function showTab(win)
    if not win.talTiles then return end
    local tal = talActive(win)
    for _, r in pairs(win.rows) do setVis(r, not tal) end
    for _, b in pairs(win.btn) do setVis(b, not tal) end
    setVis(win.tick.pas, not tal)
    setVis(win.care, not tal)
    setVis(win.look, (not tal) and win.model ~= nil and win.model.look ~= nil)
    for i = 1, #win.talTiles do setVis(win.talTiles[i], tal) end
    setVis(win.talReset, tal)
    local on = win.m ~= nil and win.m.tal == true
    setVis(win.tabMainB, on)
    setVis(win.tabTalB, on)
end

-- Modell anwenden: Texte, Zustaende, Tooltips der Kinder; Breiten, die je Sekunde wechseln (Chip, Prozent). Nur im 1-s-Takt.
local function apply(win, d)
    local m = win.m
    if not m then return end
    d.chipW = m.R28 + tw(m.fBody, d.chipText) + m.R12
    for i = 1, #d.skills do
        local s = d.skills[i]
        s.pctW = tw(m.fSmall, s.pctTxt)
        win.rows[i].tooltip = s.tip
    end
    for i = 1, #CMDS do
        local key = CMDS[i]
        local b, e = win.btn[key], d.buttons[key]
        b.label, b.state, b.tooltip = e.label, e.state, e.tip
        b.enable = (e.state ~= "off")               -- ISButton.lua:45; Felder wie V:client/ISUI/Hutch/ISHutchUI.lua:617-623
    end
    win.rename.label = d.rename
    local t = d.toggles
    win.tick.pas.on, win.tick.pas.label, win.tick.pas.tooltip = t.pas, t.pasLabel, t.pasTip
    win.gearB.tooltip = d.gearTip                                   -- K1: Zahnrad (ISButton-Tooltip, V:client/ISUI/ISButton.lua:316-346)
    win.rows.hp.tooltip, win.rows.sta.tooltip = d.tips.hp, d.tips.sta
    win.rows.carry.tooltip = d.tips.carry
    for i = 1, #NEEDS do win.rows[NEEDS[i]].tooltip = d.tips[NEEDS[i]] end         -- F3: Hunger, Durst, Muedigkeit, Vertrauen
    -- F2: Melee damage / Kills, Pflege-Knopf, Show damage; Breite des Leben-Werts fuer das Verband-Zeichen (WinParts drawBar)
    win.rows.melee.tooltip, win.rows.kills.tooltip = d.tips.melee, d.tips.kills
    d.hp.valW = tw(m.fBody, d.hp.val)
    local c = d.care
    if c then
        win.care.label, win.care.state, win.care.tooltip, win.care.kind = c.label, c.state, c.tip, c.kind
        win.care.enable = (c.state ~= "off")                        -- ISButton.lua:45
    end
    -- Aussehen (PLAN_AUSSEHEN.md 8.1): Knopf "Look"; ohne d.look (Kern ohne Aussehen) unsichtbar -- wie der Wachstums-Schalter oben nur bei
    -- einem Wechsel umschalten und den offenen Tooltip vorher abmelden (ISButton:setVisible V:client/ISUI/ISButton.lua:9, getIsVisible :34)
    local lb, le = win.look, d.look
    if le then
        lb.label, lb.state, lb.tooltip = le.label, le.state, le.tip
        lb.enable = (le.state ~= "off")                             -- ISButton.lua:45
    end
    local showLook = (le ~= nil) and not talActive(win)             -- Lauf baer-talente: im Reiter "Perks" verborgen
    if lb:getIsVisible() ~= showLook then
        if not showLook then hideTip(lb) end
        lb:setVisible(showLook)
    end
    -- Lauf baer-talente: Kacheln, Reset, Reiter-Texte; dann Sichtbarkeit je Reiter
    if win.talTiles and U.TalentApply then U.TalentApply(win, d) end
    showTab(win)
end

-- Neu legen noetig? Option, Bildschirm, Zahl der Baeren, Name (Lage des Umbenennen-Knopfs) oder ein Text, der nicht mehr passt.
local function layoutStale(win, d)
    local m = win.m
    if not m then return true end
    local sw, sh = screen()
    if sw ~= m.sw or sh ~= m.sh or sizeIdx() ~= m.idx then return true end
    if (win.n > 1) ~= (m.n > 1) then return true end
    if (d.tal ~= nil) ~= (m.tal == true) then return true end         -- Lauf baer-talente: Reiterleiste kam / ging
    local dyn, nameW, countW = dynNeed(m, d, win.n)
    if nameW ~= m.nameW or countW ~= m.countW then return true end
    return math.max(m.needStatic, dyn) ~= m.need
end

-- Modell neu bauen (bei neuer Sicht oder je MODEL_MS). Gibt false, wenn das Fenster dabei geschlossen wurde.
function Win:refresh(now)
    self.dirty = false
    self.modelAt = now
    local player = getSpecificPlayer(0)             -- V:client/Farming/CFarmingSystem.lua:45
    if not player or player:isDead() then           -- V:client/ISUI/ISUIHandler.lua:42
        U.WinClose()
        return false
    end
    local list = U.WinBears()
    if #list == 0 then
        U.WinClose()
        return false
    end
    local idx = nil
    for i = 1, #list do
        if list[i].id == self.sel then idx = i end
    end
    if idx == nil then idx = math.min(math.max(self.idx or 1, 1), #list) end   -- der gewaehlte ist weg: naechster eigener Baer
    local v = list[idx]
    self.idx, self.sel, self.n, self.v = idx, v.id, #list, v
    local d = U.WinModel(v, player, now)
    if not self.talTiles then d.tal = nil end                       -- Lauf baer-talente: ohne Kacheln keine Reiterleiste
    if #list > 1 then d.count = U.T("UI_BN_Bear_Win_Count", idx, #list) end
    self.model = d
    if layoutStale(self, d) then U.WinLayout() end
    apply(self, d)
    return true
end

-- Aussehen (PLAN_AUSSEHEN.md 8.1): Wahl im Menue des Knopfs. Vanillas Kontextmenue ruft onSelect(Ziel, Wert1, Wert2, ...)
-- (V:client/ISUI/ISContextMenu.lua:66-70, Aufruf :70 mit param1..param10; addOption speichert sie, :873). Rueckruf mit ZWEI Werten wie
-- Vanillas addOption(Name, Ziel, Funktion, Wert1, Wert2) V:client/ISUI/Animal/ISAnimalContextMenu.lua:75 / :377 (Form mit einem Wert:
-- V:client/Chat/ISChat.lua:675). id = Baer, an dem das
-- Menue aufging: gehoert er (laut Sicht) noch mir, geht genau EINE Bitte "Look" an den Schreiber -- der prueft alles noch einmal (Besitz,
-- Zustand, Zombies, Platz, gemeinsame Uhr) und setzt nichts, was er nicht selbst geprueft hat.
function Win.onLookPick(self, k, id)
    if type(k) ~= "string" or id == nil then return end
    local player = getSpecificPlayer(0)                 -- V:client/Farming/CFarmingSystem.lua:45
    if not player then return end
    local list = U.WinBears()
    local mine = false
    for i = 1, #list do
        if list[i].id == id then mine = true end
    end
    if not mine then return end
    B.Ask(player, "Look", { id = id, look = k })
    self.dirty = true
end

-- Aussehen: kleines Menue am Knopf mit allen Aussehen dieses Koerpers (Kevin-Frage K5: Menue statt Weiterschalten -- jeder Wechsel
-- kostet die gemeinsame Uhr). Das jetzige steht abgehakt und ohne Funktion, die anderen schicken die Bitte (Win.onLookPick).
-- ISContextMenu.get(Spieler, x, y) am Knopf: V:client/ISUI/Animal/ISButcherHookUI.lua:668 (Lage aus getAbsoluteX/Y des Knopfs),
-- getHeight eines Knopfs V:client/ISUI/ISButton.lua:338; addOption(Name, Ziel) ohne Funktion V:client/Chat/ISChat.lua:260;
-- addOption(Name, Ziel, Rueckruf, Wert, ...) ISChat.lua:263 / ISButcherHookUI.lua:674; setOptionChecked(Punkt, true) ISChat.lua:267
-- (V:client/ISUI/ISContextMenu.lua:1084). Die Namen sind fertige Texte aus Schluesseln (UI_BN_Bear_Look_*, client/BanditsNPCBearWinData.lua).
-- Nachbesserung Aussehen A1 (PRUEF_A.md): auf geht es, sobald es AUSSER dem jetzigen ein Angebot gibt (e.others, dieselbe Zaehlung wie
-- das Grau "nur ein Aussehen" in client/BanditsNPCBearWinData.lua) -- auch wenn das jetzige mit hide gestrichen ist und fehlt.
local function lookMenu(win, button, v)
    local e = win.model and win.model.look
    if type(e) ~= "table" or type(e.picks) ~= "table" then return end
    local others = tonumber(e.others)
    if others == nil then
        others = 0
        for i = 1, #e.picks do
            if not e.picks[i].cur then others = others + 1 end
        end
    end
    if others < 1 then return end
    local x = button:getAbsoluteX()
    local y = button:getAbsoluteY() + button:getHeight()
    local context = ISContextMenu.get(0, x, y)
    for i = 1, #e.picks do
        local p = e.picks[i]
        if p.cur then
            local opt = context:addOption(p.name, win)
            context:setOptionChecked(opt, true)
        else
            context:addOption(p.name, win, Win.onLookPick, p.k, v.id)
        end
    end
end

-- K1 (PLAN_K1.md 4 Z): Wahl im Zahnrad-Menue. Vanillas Kontextmenue ruft onSelect(Ziel, Wert1, Wert2) (V:client/ISUI/ISContextMenu.lua:66-70).
-- Alles nur je Spieler, was ICH sehe (client/BanditsNPCBearTags.lua) -- kein Server, kein Befehl. id = Baer, an dem das Menue aufging; gehoert er
-- (laut Sicht) nicht mehr mir, passiert nichts.
function Win.onGearPick(self, key, id)
    if type(key) ~= "string" or id == nil then return end
    local v = nil
    local list = U.WinBears()
    for i = 1, #list do
        if list[i].id == id then v = list[i] end
    end
    if v == nil then return end
    if key == "tag" then
        if U.TagSet and U.TagOn then U.TagSet(v, not U.TagOn(v)) end
    elseif key == "hp" then
        if U.HpSet and U.HpOn then U.HpSet(v, not U.HpOn(v)) end
    elseif key == "showdmg" then
        if U.DmgSet and U.DmgOn then U.DmgSet(not U.DmgOn()) end
    elseif key == "growth" then
        if U.AgeSet and U.AgeOn then U.AgeSet(v, not U.AgeOn(v)) end
    end
    -- "nose" ist bis F5 grau (notAvailable) und kommt nie hier an
    self.dirty = true
end

-- K1: das Zahnrad-Menue am Knopf (Form V:client/Chat/ISChat.lua:245-272 und unser lookMenu oben): je Punkt des Modells (d.gear) addOption mit
-- Rueckruf (ISChat.lua:263), Haken = an (setOptionChecked, ISChat.lua:267 / V:client/ISUI/ISContextMenu.lua:1084), grau = notAvailable +
-- Tooltip (V:client/ISUI/Animal/ISAnimalContextMenu.lua:160-163; ISWorldObjectContextMenu.addToolTip, setName). Der Tooltip-Text ist derselbe
-- Rich-Text wie an den Knoepfen (ISToolTip description -> ISRichTextPanel, V:client/ISUI/ISToolTip.lua:191-192).
local function gearMenu(win, button, v)
    local items = win.model and win.model.gear
    if type(items) ~= "table" then return end
    local x = button:getAbsoluteX()                     -- V:client/ISUI/Animal/ISButcherHookUI.lua:668
    local y = button:getAbsoluteY() + button:getHeight()    -- V:client/ISUI/ISButton.lua:338
    local context = ISContextMenu.get(0, x, y)
    for i = 1, #items do
        local e = items[i]
        if e.hide ~= true then
            local opt
            if e.off then
                opt = context:addOption(e.label, win)
                opt.notAvailable = true
            else
                opt = context:addOption(e.label, win, Win.onGearPick, e.key, v.id)
                if e.on then context:setOptionChecked(opt, true) end
            end
            if e.tip then
                local tip = ISWorldObjectContextMenu.addToolTip()
                tip.description = e.tip
                opt.toolTip = tip
            end
        end
    end
end

function Win:onGear(button)
    local v = self.v
    if not v or v.id == nil or not button then return end
    gearMenu(self, button, v)
end

-- Klick auf einen Knopf / Schalter (ISButton ruft onclick(Ziel, Knopf), V:client/ISUI/ISButton.lua:47). Nur Bitten an den Schreiber;
-- nie eine leere Tabelle (S:client/BanditsNPCBearClient.lua sendHello).
function Win:onCmd(button)
    if not button or button.state == "off" then return end
    local cmd = button.cmd
    local player = getSpecificPlayer(0)
    if not player then return end
    if cmd == "prev" or cmd == "next" then
        local n = self.n or 1
        if n > 1 then
            local i = (self.idx or 1) + ((cmd == "next") and 1 or -1)
            if i < 1 then i = n end
            if i > n then i = 1 end
            local list = U.WinBears()
            if list[i] then self.sel, self.idx = list[i].id, i end
            self.dirty = true
        end
        return
    end
    if cmd == "tabMain" or cmd == "tabTal" then
        -- Lauf baer-talente: Reiter wechseln (nur diese Sitzung); offene Tooltips weg, dann Sichtbarkeit je Reiter
        local want = (cmd == "tabTal") and "tal" or "main"
        if self.tab ~= want then
            self.tab = want
            hideTips(self)
            if U.TalentApply then U.TalentApply(self, self.model) end
            showTab(self)
        end
        return
    end
    local v = self.v
    if not v or v.id == nil then return end
    if cmd == "talent" then
        -- Lauf baer-talente: waehlbare Kachel -> Vanillas Ja/Nein-Fenster; die Bitte geht erst nach "Ja" (client/ISUI/BanditsNPCBearTalentTab.lua)
        if U.TalentAsk then U.TalentAsk(self, button) end
        return
    elseif cmd == "talReset" then
        if U.TalentResetAsk then U.TalentResetAsk(self) end
        return
    end
    if cmd == "follow" or cmd == "stay" or cmd == "sit" or cmd == "roam" then
        B.Ask(player, "Mode", { id = v.id, mode = cmd })
    elseif cmd == "come" then
        B.Ask(player, "Come", { id = v.id })
    elseif cmd == "unstuck" then
        B.Ask(player, "Call", { id = v.id })
    elseif cmd == "passive" then
        B.Ask(player, "Passive", { id = v.id, on = not (v.pas == true) })
    elseif cmd == "rename" then
        if U.AskName then self.nameBox = U.AskName(player, v) end
    elseif cmd == "care" then
        -- F2: hingehen + Zeitaktion (client/BanditsNPCBearMenu.lua); ob es gilt, entscheidet der Schreiber in complete()
        if button.kind == "help" then
            if U.HelpAsk then U.HelpAsk(player, v) end
        elseif U.MendAsk then
            U.MendAsk(player, v)
        end
        self.dirty = true
    elseif cmd == "look" then
        -- Aussehen: grau kam oben schon zurueck (state "off"); hier nur das Menue -- die Bitte schickt erst die Wahl
        lookMenu(self, button, v)
    elseif cmd == "inv" then
        -- F4 (PLAN_F4.md 7, 8.1): Inventar-Fenster dieses Baeren (client/ISUI/BanditsNPCBearInvWindow.lua) -- ansehen geht immer, Geben /
        -- Nehmen prueft dort die Vorpruefung, entscheiden tut der Schreiber in complete()
        if U.InvOpen then U.InvOpen(player, v.id) end
    end
    -- F3: "fish" hat bis F5 bewusst keinen Zweig -- grau (state "off", oben schon zurueck), schickt nie eine Bitte; kein Schlaf-Befehl (Kevin 6e).
    -- K1: Name tag / Growth line / Show damage / Health bar / Nose alerts gehen ueber das Zahnrad (Win.onGearPick).
end

function Win:onClose()
    U.WinClose()
end

-- Zeichnen je Bild: nur Rechtecke, Bilder und fertige Texte (PLAN_F1.md 0.10). drawRect / drawRectBorder / drawText / drawTextRight /
-- drawTextCentre / drawTextureScaled wie client/ISUI/BanditsNPCBearWinParts.lua (Belege dort); Bild-Zeichnen V:client/Chat/ISChat.lua:418.
local function drawHead(self, m, d)
    local P = m.P
    local tex = W.tex or {}
    local disc = col("iconDisc")
    if tex.disc then self:drawTextureScaled(tex.disc, P, m.R12, m.R80, m.R80, 1, disc[1], disc[2], disc[3]) end
    if tex.icon then self:drawTextureScaled(tex.icon, P + m.R4, m.R16, m.R72, m.R72, 1, 1, 1, 1) end
    local c = col("name")
    self:drawText(d.name or "", m.tx, m.ty, c[1], c[2], c[3], c[4], m.fName)
    self:drawText(d.name or "", m.tx + m.bold, m.ty, c[1], c[2], c[3], c[4], m.fName)   -- zweimal = "fett" (PLAN_F1.md 1.1)
    c = col("text2")
    self:drawText(d.sub or "", m.tx, m.l2y, c[1], c[2], c[3], c[4], m.fBody)
    if d.next then
        c = col("honeyText")
        self:drawText(d.next, m.tx, m.l3y, c[1], c[2], c[3], c[4], m.fBody)
    end
    if d.count and m.n > 1 then
        c = col("text2")
        self:drawTextCentre(d.count, m.countX, m.R12 + math.floor((m.R24 - m.ls) / 2), c[1], c[2], c[3], c[4], m.fSmall)
    end
    -- Zustand-Chip (rechtsbuendig) und Abstand darunter
    local cw = d.chipW or 0
    local chx, chy = m.W - P - cw, m.R44
    local r, g, b = d.cr or 1, d.cg or 1, d.cb or 1
    self:drawRect(chx, chy, cw, m.chipH, 1, r * 0.2, g * 0.2, b * 0.2)
    for i = 0, m.t - 1 do self:drawRectBorder(chx + i, chy + i, cw - 2 * i, m.chipH - 2 * i, 0.85, r, g, b) end
    if tex.disc then self:drawTextureScaled(tex.disc, chx + m.R10, chy + math.floor((m.chipH - m.R10) / 2), m.R10, m.R10, 1, r, g, b) end
    c = col("text")
    self:drawText(d.chipText or "", chx + m.R28, chy + m.R4, c[1], c[2], c[3], c[4], m.fBody)
    if d.dist then
        c = col("dim")
        self:drawTextRight(d.dist, m.W - P, chy + m.chipH + m.R4, c[1], c[2], c[3], c[4], m.fSmall)
    end
end

local function card(self, m, x, y, w, h, title, info)
    U.WinRect(self, x, y, w, h, col("cardBg"))
    U.WinFrame(self, x, y, w, h, m.t, col("cardBorder"))
    local c = col("title")
    self:drawText(title or "", x + m.R12, y + m.R10, c[1], c[2], c[3], c[4], m.fBody)
    if info and info ~= "" then
        c = col("dim")
        self:drawTextRight(info, x + w - m.R12, y + m.R10, c[1], c[2], c[3], c[4], m.fSmall)
    end
end

function Win:prerender()
    local now = getTimestampMs()                    -- V:client/Foraging/ISBaseIcon.lua:485
    if self.dirty or now - self.modelAt >= MODEL_MS or now < self.modelAt then
        if not self:refresh(now) then return end
    end
    local m, d = self.m, self.model
    if not m or not d then return end
    U.WinRect(self, 0, 0, m.W, m.H, col("winBg"))
    U.WinFrame(self, 0, 0, m.W, m.H, m.t, col("winBorder"))
    U.WinRect(self, 0, 0, m.W, m.R3, col("accent"))
    drawHead(self, m, d)
    U.WinRect(self, m.P, m.headH + m.R4, m.W - 2 * m.P, m.t, col("divider"))
    if talActive(self) and U.TalentDraw then
        U.TalentDraw(self, m, d)                                                    -- Lauf baer-talente: Karte "Perks"
    else
        card(self, m, m.lx, m.y1, m.CW, m.cardH, d.tCond)
        card(self, m, m.mx, m.y1, m.CW, m.cardH, d.tNeeds)                          -- F3 (Variante B): eigene Karte "Needs"
        card(self, m, m.rx, m.y1, m.CW, m.cardH, d.tSkills)
        card(self, m, m.P, m.y2, m.ow, m.ordH, d.tOrders, d.ordersInfo)
    end
    -- Fusszeile; F3: in Warnfarbe, wenn der Baer nicht kaempft (zu muede / kein Vertrauen -- d.footerCol aus dem Modell)
    local c = col(d.footerCol or "dim")
    self:drawText(d.footer or "", m.P, m.y3, c[1], c[2], c[3], c[4], m.fSmall)
end

-- Esc schliesst (V:client/ISUI/Crafting/ISHandcraftWindow.lua:289-297; Esc nur Spieler 0 wie V:client/ISUI/Hutch/ISHutchUI.lua:884-893).
-- Nicht, solange der Spieler tippt: Chat (ISChat.focused, V:client/Chat/ISChat.lua:8) oder das Namensfeld dieses Fensters
-- (isReallyVisible, V:client/ISUI/ISUIElement.lua:690).
local function typing(self)
    if ISChat and ISChat.focused then return true end
    local box = self.nameBox
    return box ~= nil and box:isReallyVisible()
end

-- Schliess-Taste: nur Esc (F1B E8, PLAN_F1B.md 1.7; Form V:client/ISUI/Crafting/ISHandcraftWindow.lua:290). Die einzige Tastenabfrage
-- dieser Datei. Die Nah- und die Fern-Taste verbraucht das Fenster NICHT: ein verbrauchter Druck naehme allen Lua-Hoerern die Taste
-- (NC "Talk to NPC" auf V, Moebel-Cursor, NC-Stationen auf E); sie schliessen ueber client/BanditsNPCBearKey.lua (OnKeyPressed).
local function closeKey(key)
    return key == Keyboard.KEY_ESCAPE
end

function Win:isKeyConsumed(key)
    if typing(self) then return false end
    return closeKey(key)
end

function Win:onKeyRelease(key)
    if typing(self) then return end
    if self:isVisible() and closeKey(key) then
        U.WinClose()
    end
end

-- Lage merken (V:client/ISUI/ISLayoutManager.lua:6-13 RegisterWindow mit eigener Klasse wie V:client/Chat/ISChat.lua:1172; gerufen
-- :103 / :111). NUR x und y -- kein "visible", sonst oeffnete Vanillas DefaultRestoreWindow das Fenster nach dem Laden von selbst
-- (:45-50). Geschrieben in layout.ini beim Spielspeichern (:191-232), je Aufloesung.
function Win:SaveLayout(_name, layout)
    layout.x = self:getX()
    layout.y = self:getY()
    layout.visible, layout.width, layout.height = nil, nil, nil
end

function Win:RestoreLayout(_name, layout)
    local x = tonumber(layout.x)                    -- ISLayoutManager.lua:17-18
    local y = tonumber(layout.y)
    if x ~= nil and y ~= nil then
        self:setX(x)
        self:setY(y)
        clampPos(self)
    end
end

-- ---------------------------------------------------------------------------
-- Oeffnen / Schliessen (PLAN_F1.md 1.8)
-- ---------------------------------------------------------------------------

-- Bilder einmal je Spielstart. getTexture(Pfad): V:client/Chat/ISChat.lua:137; Vanillas Schliessen-Bild:
-- V:client/ISUI/ISCollapsableWindow.lua:386; eigene Bilder wie S:client/ISUI/BanditsNPCBearMarker.lua (288-px-Symbol, Scheibe).
local function textures()
    if W.tex then return W.tex end
    W.tex = { icon = getTexture(ICON_FILE), disc = getTexture(DISC_FILE), close = getTexture(CLOSE_FILE),
        gear = getTexture(GEAR_FILE) }                  -- K1: Zahnrad (V:client/Chat/ISChat.lua:137)
    return W.tex
end

-- Der naechste eigene Baer (Sicht-Lage) -- beim Oeffnen ohne Kennung (Frage F6).
local function nearest(list, player)
    local best, bestD = list[1], nil
    local px, py = player:getX(), player:getY()     -- V:client/Fishing/TensionUI.lua:11
    for i = 1, #list do
        local v = list[i]
        if type(v.x) == "number" and type(v.y) == "number" then
            local dx, dy = v.x + 0.5 - px, v.y + 0.5 - py
            local dd = dx * dx + dy * dy
            if bestD == nil or dd < bestD then best, bestD = v, dd end
        end
    end
    return best
end

-- Hinweis ueber der Figur. HaloTextHelper.addText(Spieler, Text): V:client/Foraging/forageClient.lua:73.
local function halo(player, key)
    HaloTextHelper.addText(player, U.T(key))
end

function U.WinOpen(player, id)
    player = player or getSpecificPlayer(0)
    if not player then return false end
    if not U.Fresh or not U.Fresh() then
        if U.AskHello then U.AskHello(player) end
        halo(player, "UI_BN_Bear_Win_NoData")
        return false
    end
    local list = U.WinBears()
    if #list == 0 then
        halo(player, "UI_BN_Bear_Win_NoBear")
        return false
    end
    local pick = nil
    if id ~= nil then
        for i = 1, #list do
            if list[i].id == id then pick = list[i] end
        end
    end
    if pick == nil then pick = nearest(list, player) end
    local win = W.win
    local first = (win == nil)
    if first then
        textures()
        win = Win:new(0, 0, 640, 480)
        win:initialise()                            -- V:client/ISUI/Animal/ISAnimalContextMenu.lua:746
        win:build()
        W.win = win
    end
    win.sel = pick.id
    win.dirty = true
    if not win:refresh(getTimestampMs()) then return false end
    if first then
        local sw, sh = screen()
        local m = win.m
        win:setX(math.floor((sw - m.W) * 0.62))
        win:setY(math.floor((sh - m.H) * 0.30))
        ISLayoutManager.RegisterWindow(LAYOUT_NAME, Win, win)   -- stellt eine gemerkte Lage sofort her (ISLayoutManager.lua:12)
        clampPos(win)
    end
    win.isOpen = true
    win:addToUIManager()                            -- V:client/ISUI/ISUIElement.lua:1365
    win:setVisible(true)                            -- :657
    win:bringToTop()                                -- :1548
    return true
end

function U.WinClose()
    U.winClosedAt = getTimestampMs()
    local win = W.win
    if not win then return end
    win.isOpen = false
    hideTips(win)
    win:setVisible(false)                           -- wie V:client/ISUI/Crafting/ISHandcraftWindow.lua:295-296 (close + removeFromUIManager)
    win:removeFromUIManager()
end

function U.WinIsOpen()
    return W.win ~= nil and W.win.isOpen == true
end

-- Nachbesserung F1 B10: tippt der Spieler gerade (Chat oder das Namensfeld dieses Fensters ist offen, auch ohne Fokus)? Dann schliesst die
-- Taste das Fenster auch ueber client/BanditsNPCBearKey.lua nicht (isKeyConsumed gibt die Taste dann frei).
function U.WinTyping()
    local win = W.win
    return win ~= nil and win.isOpen == true and typing(win)
end

function U.WinToggle(player)
    if U.WinIsOpen() then
        U.WinClose()
    else
        U.WinOpen(player)
    end
end

-- Naht zur Sicht: B.OnView (client/ISUI/BanditsNPCBearHud.lua) ruft das nach jeder neuen Sicht -> Modell im naechsten Bild neu.
function U.WinOnView()
    if W.win then W.win.dirty = true end
end

-- Je Spielstart ein frisches Fenster: ein altes (Hauptmenue und neu laden) wird geschlossen, abgemeldet und vergessen (wie
-- S:client/ISUI/BanditsNPCBearHud.lua onGameStart).
local function onGameStart()
    if W.win then U.WinClose() end
    W.win = nil
    W.tex = nil
end

-- Bildschirm-Aufloesung geaendert: neu legen und klemmen. Events.OnResolutionChange: V:client/ISUI/PlayerData/ISPlayerData.lua:206.
local function onResolution()
    if W.win then U.WinLayout() end
end

Events.OnGameStart.Add(onGameStart)                 -- V:client/Chat/ISChat.lua:1186
Events.OnResolutionChange.Add(onResolution)
