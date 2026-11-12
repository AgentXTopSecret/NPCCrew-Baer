# Lauf baer-gross (11.11.2026), Bau Clips: Kopie von baer_textur_2c.py (Original unveraendert, MD5 670fe492). Kopie-Schritt: nur Pfade/Namen
# auf _arbeit/baer_gross bzw. *_gross.py umgestellt (ARB -> _arbeit/baer_gross/, EXPORT baer_export_gross.py). Statisch/offline, nicht gespielt.
# Bau Textur (11./12.11.2026): G2 (dunkler Ring um den Kopf, Spez 5.1) als Stufen "GROSS G2 Koerper" / "GROSS G2 Kopfrand" (BAER_TX_G2=0 = wie 2c);
# Vorgaben G2_ZIEL 110, G2_K0/K1 0,04/0,09, SCHAERFE 0,97 (2c 0,85). Kette: _arbeit/baer_gross/werkzeug/textur/lauf_textur_gross.sh.
# Nachbesserung fix1 (12.11.2026, _arbeit/baer_gross/fix1_bericht.md): Zeilenenden LF wie das Original (vorher CRLF); neue Stufe "FIX1 FRONT"
# (BAER_TX_FRONT=0 = wie vorher): Oberarm bis Unterarm-Mitte und Bauchmitte im geglaetteten Feld angehoben (keine drei dunklen
# Laengsstreifen beim Aufrichten). Kette: _arbeit/baer_gross/fix1/werkzeug/lauf_textur_fix1.sh (BAER_TX_GEW = Gewichte).
# Lauf baer-2c (10.11.2026): Kopie von baer_textur_pfote.py (Original unveraendert). Bau Koerper hat NUR die Pfade umgelenkt
# (ARB _arbeit/baer_2c/, EXPORT baer_export_2c.py, Name 2c); alles Weitere macht der Textur-Bauer.
# Bauer Textur 2c (10.11.2026, SPEZ_2C.md 2.5 / 4 / 6.2; Schalter BAER_TX_2C=0 = Rechnung wie baer-pfoten bis auf die Pfade):
#   - Projektion der Ansichten am Netz VOR form_2c (BAER_TX_FELD = netz/form2c_feld_2c.npz, dichte Huelle S0 -> S): je Spielnetz-Punkt
#     die Verschiebung zurueck (8 Nachbarn der Huelle), so treffen Schulter/Knie/Hals (bis 14 cm verschoben) das Hochmodell, das am Rumpf
#     nicht verschmaelert ist; Buesche, Masken, Hoehen und Haarrichtung der Buesche bleiben am neuen Netz (die Straehnen folgen der Form).
#   - Hinterfuss-Sohle dunkelbraun-ledern (Median sRGB 62/42/30, Kuppe heller, Furchen dunkel), Fellkranz breiter und ueber dem Rand.
#   - Krallen dunkler (hinten Wurzel <= 70/55/45, Spitze <= 150/135/115; vorn hoechstens dunkler), nur das Lesefeld der Krallen-UV.
#   - Kopf-Passung (C3): Hals, Nacken, Kehle, Schultern, Buckel gleiten in Helligkeit/Farbe zum Kopfmittel, Straehnen nahe am Kopf
#     feiner; nur Koerper-Texel, ab ~4 cm von der Kopfnaht (die Naht selbst bleibt am alten Fell).
#   - Fellbehang (SPEZ 2.5): haengende Straehnen ueber den Behang-Kanten (Ellbogen, Bauch), darunter ein Schattenband.
#   - BAER_TX_NUR_TEXEL=1: nur Texel-Lagen (P neu, P0 vor form_2c) nach mess/texel_<NAME>.npz (fuer den Bezug), dann Ende.
# Lauf baer-pfoten, Bauer Textur (09.11.2026): Kopie von baer_textur_fell.py (Original unveraendert). Aenderungen:
#   - Hochmodell/Hilfen aus baer_export_pfote.py (-> baer_quelle_pfote.py, neue Pfoten), Netz netz/lowpoly_pfote.blend, Zwischenstand
#     netz/zwischen_pfote, Ordner unter _arbeit/baer_pfote/ (BAER_TX_DIR, BAER_FELL_NETZ, BAER_TX_ANS wie bisher umlenkbar).
#   - Haarrichtung an der Pfote wie das Pfotenhaar des Hochmodells (baer_quelle_pfote.py:2018-2020: unter Spiel-z 0,10 nach vorn/unten).
#   - sohlen_malen nach dem neuen Ballenplan (netz/sohle_layout.json: Sohlenplatte hinten bzw. Handballen vorn als Vieleck, fuenf
#     Zehenballen), dazu ueber eine 3D-Maske aus spez/pfoten_plan.json: Handwurzelballen (vorn, angehoben) und Fersen-Hochzug (hinten),
#     die nicht in der Sohlen-Insel liegen; Zehenrillen dunkler (Verdeckung im Kleinen am Spielnetz); Buesche an der Pfote kleiner.
#   - Bezug fuer Farbabgleich/Hals-Naht: fertige baer-fell-Textur auf die neue UV uebertragen (BAER_TX_ZWISCHEN, textur/zw_fell_2048.png),
#     weil der Zwischenstand des Netz-Bauers 15 % dunkler ist; Pfoten-Helligkeit je Hoehenband an baer-fell (PF_ABGLEICH), Uebergang
#     Rumpf/Bein (Spiel-z 0,27-0,50) oertlich an baer-fell, waagerechte Baender am neuen Wulst eingeebnet, dort kaum nachgeschaerft.
#   - Pruefbild ohne Sohlen: BAER_TX_VOR_SOHLE=1. Kette: _arbeit/baer_pfote/textur/werkzeug/lauf_textur.sh NAME backen glb deer.
#   - Alles andere wie baer-fell (Ausgleich Blickrichtung, Farbabgleich, Back-Pose, Glaetten, 3D-Buesche, Deckel, Kopf/Krallen alt).
# --- Kopf des Originals (baer_textur_fell.py) ---
# Lauf baer-fell, Bauer Textur (08.11.2026). Neue Koerpertextur fuer das Netz aus baer_export_fell.py (netz/lowpoly_fell.blend).
# Liest nur: baer_quelle_anim.py (Hochmodell, Fell), baer_export_fell.py (Hilfsfunktionen der Stufe backen), die alten Ansichten
# (_arbeit/baer_spiel/ansichten), die Uebergabe des Netz-Bauers (_arbeit/baer_fell/netz/). Schreibt nur nach _arbeit/baer_fell/textur/
# und _arbeit/baer_fell/mod/42/media/textures/. Kopf- und Krallen-Texel kommen unveraendert aus der alten 2048er.
# Stufen (blender --background --factory-startup --python baer_textur_fell.py -- STUFE|AUFTRAG.json):
#   AUFTRAG.json {"stufe": "ansichten", ...}  [GPU, nur ueber _arbeit/baer_fell/werkzeug/gpu_render.sh]: Hochmodell mit Fell, Fell nur
#                fuer den Bake geaendert (Variante: Beine weniger Melanin, Haar rauer), 22 Koerper-Ansichten wie baer_export.py
#                kamera_daten + 4 steile Unterseiten-Ansichten -> textur/ansichten; mit "pose": true Back-Pose (Beine gespreizt,
#                back_pose_setzen) und 9 Ansichten von unten -> textur/ansichten_pose. Auftraege: textur/ansichten*_auftrag.json
#   backen     Ansichten auf das neue Netz (Back-Pose-Ansichten auf das gleich posierte Netz), Ausgleich der Blickrichtung zum Haar,
#              Farbabgleich ans alte Fell, Unterseite heller, Haarbuesche, Faltenschatten, Hals-Naht, Sohlen aus dem Ballen-Plan,
#              Kopf/Krallen alt -> textur/NCBear_<BAER_TX_NAME>_2048.png und textur/NCBear_kopf_variante.png (nur Vergleich).
#              BAER_TX_NUR_NEU=1: Gegenprobe mit alten Ansichten und alter Nacharbeit (= Zwischenstand des Netz-Bauers, +-1 sRGB).
# Nachbesserung 09.11.2026 (_arbeit/baer_fell/fix_bericht.md): Ordner per Umgebung (BAER_TX_DIR, BAER_FELL_NETZ, BAER_TX_ANS), weiche
#   Uebergaenge der Back-Pose-/Innenbein-Gewichte (keine scharfkantigen Flecken), Gesprenkel an Beinen/Hinterteil vor der Nacharbeit
#   inselweise geglaettet, breitere/laengere Haarbuesche mit stabiler Haarrichtung (kein Wirbel am Schwanzansatz), Leiste/Unterseite
#   hoechstens so hell wie der Ruecken (CAP_*), Pfoten/zu satte Fellfarbe entsaettigt, Sohle mit groesseren Ballen, glatterer Haut und
#   Fellkranz aus Straehnen, Krallen-Lesefeld (2x2 bilinear, 2048 und 1024) mit den alten Texeln.
# Statisch/offline gebaut und geprueft, nicht gespielt.
import json
import math
import os
import sys
import time

import bpy
import numpy as np
from mathutils import Vector

HIER = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/"
ARB = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gross/"
ARB_FELL = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_fell/"   # nur lesen (bestand/NCBear_2048.png: Krallen-Lesefeld wie baer-fell)
TX = os.environ.get("BAER_TX_DIR", ARB + "textur/")            # Ausgabe (Nachbesserung: umlenkbar, sonst ueberschreibt ein Nachbau die Lieferung)
NETZ = os.environ.get("BAER_FELL_NETZ", ARB + "netz/")         # Netz, Karten, Sohlen-Plan, Zwischenstand
ANS_DIR = os.environ.get("BAER_TX_ANS", ARB + "textur/")       # GPU-Ansichten (ansichten/, ansichten_pose/)
EXPORT = HIER + "baer_export_gross.py"
NETZ_NAME = os.environ.get("BAER_FELL_NAME", "2c")          # netz/lowpoly_<NAME>.blend, netz/zwischen_<NAME>/
PLAN_PFOTE = os.environ.get("BAER_TX_PLAN", r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote/spez/pfoten_plan.json")   # 2c: Vorderpfoten
#   wie baer-pfoten (nur gelesen; _arbeit/baer_2c/spez hat keinen Pfoten-Plan, hinten gilt sohle_layout.json)
ANS_ALT = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/ansichten/"
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["backen"]
T0 = time.time()


def log(*a):
    print("TEXTUR %.1fs" % (time.time() - T0), *a, flush=True)


def lade_export():
    """Hilfsfunktionen aus baer_export_pfote.py (nur lesen): alles vor der Stufenwahl am Dateiende."""
    src = open(EXPORT, encoding="utf-8").read()
    marke = '\nif STUFE == "ansichten":'    # baer_export_pfote.py: Stufenwahl beginnt mit "ansichten" (baer_export_fell.py: "diagnose")
    assert src.count(marke) == 1
    alt = sys.argv
    sys.argv = [alt[0], "--", "keine"]
    E = {"__name__": "baer_export_pfote", "__file__": EXPORT}
    exec(compile(src.split(marke)[0], EXPORT, "exec"), E)
    sys.argv = alt
    return E


# ------------------------------------------------------------------ Kameras (wie baer_export.py kamera_daten, dazu Unterseite)
C_B = (0.14, 0.0, 0.80)


def _view(name, c, az, el, ortho, res, clip=None):
    a, e = math.radians(az), math.radians(el)
    d = (math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))
    v = dict(name=name, c=[float(x) for x in c], d=[float(x) for x in d], ortho=ortho, res=res)
    if clip is not None:
        v["clip"] = float(clip)       # Abstand (Hochmodell-m) vor dem Mittelpunkt c, ab dem die Kamera sieht (Schnitt-Ansicht)
    return v


def kamera_koerper(res=2048):
    """Genau die 22 Koerperkameras von baer_export.py:91-107."""
    views = []
    for az in range(0, 360, 45):
        views.append(_view("k_h%03d" % az, C_B, az, 0, 3.5, res))
    for az in range(0, 360, 60):
        views.append(_view("k_o%03d" % az, C_B, az, 42, 3.5, res))
    views.append(_view("k_top", C_B, 0.0, 89.5, 3.5, res))
    for az in range(30, 390, 60):
        views.append(_view("k_u%03d" % az, C_B, az, -38, 3.5, res))
    views.append(_view("k_bot", C_B, 0.0, -89.5, 3.5, res))
    return views


POSE_HINTEN = float(os.environ.get("BAER_TX_POSE_HINTEN", "28"))   # Back-Pose: Oberschenkel so viele Grad nach aussen
POSE_VORN = float(os.environ.get("BAER_TX_POSE_VORN", "22"))       # Back-Pose: Oberarme so viele Grad nach aussen


def kamera_pose(res=2048):
    """Ansichten der Back-Pose (Beine gespreizt): von unten auf Innenbeine, Achsel, Leiste, Bauch."""
    views = []
    for az in (0, 90, 180, 270):
        views.append(dict(_view("p_s%03d" % az, C_B, az, -64, 3.5, res), pose=True))
    for az in (60, 120, 240, 300):
        views.append(dict(_view("p_u%03d" % az, C_B, az, -36, 3.5, res), pose=True))
    views.append(dict(_view("p_bot", C_B, 0.0, -89.5, 3.5, res), pose=True))
    return views


def back_pose_setzen():
    """Hochmodell-Skelett (baer_quelle_anim.py:1146-1189, ohne IK): Oberschenkel und Oberarme um die Laengsachse (x) nach aussen
    drehen, Kinder folgen. Haut, Fell (Partikel nach dem Armature-Modifier) und an Knochen gehaengte Teile folgen."""
    from mathutils import Matrix
    ao = bpy.data.objects["skelett"]
    assert np.abs(np.array(ao.matrix_world) - np.eye(4)).max() < 1e-9
    for n, sg in (("L", 1.0), ("R", -1.0)):
        for bname, winkel in (("schenkel" + n, POSE_HINTEN), ("oberarm" + n, POSE_VORN)):
            pb = ao.pose.bones[bname]
            H = ao.data.bones[bname].head_local
            R = Matrix.Rotation(math.radians(winkel * sg), 4, "X")
            pb.matrix = Matrix.Translation(H) @ R @ Matrix.Translation(-H) @ pb.matrix
            bpy.context.view_layer.update()


def pose_matrizen():
    """Verformung je Knochen in der Back-Pose (Armature-Raum = Welt): pose.matrix @ bone.matrix_local^-1, dazu die Haut des
    Hochmodells (Ruhe, Welt) und ihre Knochengewichte. Muss vor open_mainfile laufen (das Hochmodell verschwindet dann)."""
    ao = bpy.data.objects["skelett"]
    body = bpy.data.objects["baer_koerper"]
    back_pose_setzen()
    namen = [b.name for b in ao.data.bones]
    D = np.stack([np.array(ao.pose.bones[n].matrix @ ao.data.bones[n].matrix_local.inverted()) for n in namen])
    gi = {vg.index: namen.index(vg.name) for vg in body.vertex_groups if vg.name in namen}
    nb = len(body.data.vertices)
    W = np.zeros((nb, len(namen)))
    for v in body.data.vertices:
        for g in v.groups:
            if g.group in gi:
                W[v.index, gi[g.group]] = g.weight
    W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
    M = np.array(body.matrix_world)
    Vb = np.array([tuple(v.co) for v in body.data.vertices]) @ M[:3, :3].T + M[:3, 3]
    return dict(D=D, W=W, Vb=Vb, namen=namen)


def pose_netz(PM, V):
    """Spielnetz (Hochmodell-Masse) in die Back-Pose: Gewichte des naechsten Hautpunkts, lineares Skinning. Gibt Punkte und 3x3 je Punkt."""
    from mathutils.kdtree import KDTree
    kd = KDTree(len(PM["Vb"]))
    for i, p in enumerate(PM["Vb"]):
        kd.insert(p, i)
    kd.balance()
    nah = np.array([kd.find(p)[1] for p in V])
    Wv = PM["W"][nah]
    Mv = np.einsum("nb,bij->nij", Wv, PM["D"])
    Vp = np.einsum("nij,nj->ni", Mv[:, :3, :3], V) + Mv[:, :3, 3]
    return Vp, Mv[:, :3, :3]


def kamera_unterseite(res=2048, schnitt=False):
    """Zusatz fuer die Unterseite: steile Blicke von unten (64 Grad) in Achsel, Leiste, Bauch und Innenbeine aus vier Richtungen.
    schnitt=True: Schnitt-Ansichten (Kamera-Clip an der Mittelebene) - probiert (probe/p2) und verworfen: der Schnitt geht durch
    das dichte Fell zwischen den Beinen, das Bild ist dort schwarz."""
    views = []
    for az in (0, 90, 180, 270):
        views.append(_view("u_s%03d" % az, C_B, az, -64, 3.5, res))
    if schnitt:
        for az, el in ((90, -12), (270, -12), (90, -40), (270, -40)):
            views.append(_view("u_c%03d_e%+03d" % (az, el), C_B, az, el, 3.5, res, clip=0.0))
    return views


# ------------------------------------------------------------------ Fellfarbe nur fuer den Bake
GRUND = {}


def fell_merken():
    hm = bpy.data.materials["haar"]
    for n in hm.node_tree.nodes:
        if n.type == "MAP_RANGE":
            GRUND[("haar", n.name)] = (n.inputs["To Min"].default_value, n.inputs["To Max"].default_value)
        if n.type == "BSDF_HAIR_PRINCIPLED":
            GRUND[("haar_bsdf", n.name)] = (n.inputs["Roughness"].default_value, n.inputs["Radial Roughness"].default_value)
    fm = bpy.data.materials["fell"]
    for n in fm.node_tree.nodes:
        if n.type == "MAP_RANGE":
            GRUND[("fell", n.name)] = (n.inputs["To Min"].default_value, n.inputs["To Max"].default_value)


def _diffus_zweig(nt, mel_out, rand_out, bsdf):
    """Diffuse Farbe aus Melanin wie Cycles: sigma = q*(Eu*(1-r)+Pheo*r), q = -ln(1-m), r = 0,25; Albedo = exp(-sqrt(sigma)*f(beta))
    mit f(0,8) = 4,286 (Chiang). Ergebnis: Faser ohne Blickrichtungs-Abhaengigkeit, gemischt per Faktor mit der Haar-BSDF."""
    N, L = nt.nodes, nt.links
    eins = N.new("ShaderNodeMath")
    eins.operation = "SUBTRACT"
    eins.inputs[0].default_value = 1.0
    L.new(mel_out, eins.inputs[1])
    mx = N.new("ShaderNodeMath")
    mx.operation = "MAXIMUM"
    mx.inputs[1].default_value = 0.0001
    L.new(eins.outputs[0], mx.inputs[0])
    lg = N.new("ShaderNodeMath")
    lg.operation = "LOGARITHM"
    lg.inputs[1].default_value = math.e
    L.new(mx.outputs[0], lg.inputs[0])
    ng = N.new("ShaderNodeMath")
    ng.operation = "MULTIPLY"
    ng.inputs[1].default_value = -1.0
    L.new(lg.outputs[0], ng.inputs[0])
    sq = N.new("ShaderNodeMath")
    sq.operation = "SQRT"
    L.new(ng.outputs[0], sq.inputs[0])
    cc = N.new("ShaderNodeCombineColor")
    for i, a in enumerate((2.923, 3.867, 5.622)):
        m1 = N.new("ShaderNodeMath")
        m1.operation = "MULTIPLY"
        m1.inputs[1].default_value = -a
        L.new(sq.outputs[0], m1.inputs[0])
        ex = N.new("ShaderNodeMath")
        ex.operation = "EXPONENT"
        L.new(m1.outputs[0], ex.inputs[0])
        L.new(ex.outputs[0], cc.inputs[i])
    zf = N.new("ShaderNodeMapRange")
    zf.inputs["To Min"].default_value = 0.88
    zf.inputs["To Max"].default_value = 1.12
    L.new(rand_out, zf.inputs["Value"])
    mu = N.new("ShaderNodeMix")
    mu.data_type = "RGBA"
    mu.blend_type = "MULTIPLY"
    [i for i in mu.inputs if i.name == "Factor" and i.type == "VALUE"][0].default_value = 1.0
    L.new(cc.outputs[0], [i for i in mu.inputs if i.name == "A" and i.type == "RGBA"][0])
    L.new(zf.outputs[0], [i for i in mu.inputs if i.name == "B" and i.type == "RGBA"][0])
    df = N.new("ShaderNodeBsdfDiffuse")
    L.new([o for o in mu.outputs if o.type == "RGBA"][0], df.inputs["Color"])
    ms = N.new("ShaderNodeMixShader")
    ms.name = "bake_mix"
    L.new(bsdf.outputs[0], ms.inputs[1])
    L.new(df.outputs[0], ms.inputs[2])
    L.new(ms.outputs[0], N["Material Output"].inputs["Surface"])
    return ms


def fell_vorbereiten():
    """Einmal je Sitzung: Werte merken, Diffus-Zweig einbauen (Faktor 0 = wie vorher), Zehenhaar eigenes Material."""
    fell_merken()
    hm = bpy.data.materials["haar"]
    nt = hm.node_tree
    hb = [n for n in nt.nodes if n.type == "BSDF_HAIR_PRINCIPLED"][0]
    mel_out = hb.inputs["Melanin"].links[0].from_socket
    hi = [n for n in nt.nodes if n.type == "HAIR_INFO"][0]
    ms = _diffus_zweig(nt, mel_out, hi.outputs["Random"], hb)
    ms.inputs[0].default_value = 0.0
    # Zehenhaar (Kopfhaar-Material hk) bekommt eine Kopie, damit Kopf und Hals unveraendert bleiben
    hk = bpy.data.materials["haar_kopf"]
    hz = hk.copy()
    hz.name = "haar_zeh"
    ntz = hz.node_tree
    hbz = [n for n in ntz.nodes if n.type == "BSDF_HAIR_PRINCIPLED"][0]
    src = hbz.inputs["Melanin"].links[0].from_socket
    sub = ntz.nodes.new("ShaderNodeMath")
    sub.operation = "SUBTRACT"
    sub.use_clamp = True
    sub.name = "zeh_hell"
    sub.inputs[1].default_value = 0.0
    ntz.links.new(src, sub.inputs[0])
    ntz.links.new(sub.outputs[0], hbz.inputs["Melanin"])
    hiz = [n for n in ntz.nodes if n.type == "HAIR_INFO"][0]
    msz = _diffus_zweig(ntz, sub.outputs[0], hiz.outputs["Random"], hbz)
    msz.inputs[0].default_value = 0.0
    n_z = 0
    for o in bpy.data.objects:
        if o.type == "CURVES" and o.name.startswith("haar_") and not (o.name.startswith("haar_kopf") or o.name.startswith("haar_kiefer")):
            o.data.materials.clear()
            o.data.materials.append(hz)
            n_z += 1
    log("Zehenhaar-Objekte mit eigenem Material:", n_z)


def fell_variante(var):
    """Variante relativ zu den gemerkten Werten. Schluessel: bein_mel (0,13), ruecken_mel (0,12), spitze_mel (0,20), rough (0,34),
    radial (0,80), haut_bein (0,62), diffus (0 = Haar-BSDF wie vorher, 1 = nur diffus), zeh_hell (0)."""
    hm = bpy.data.materials["haar"]
    for n in hm.node_tree.nodes:
        if n.type == "MAP_RANGE" and ("haar", n.name) in GRUND:
            c, d = GRUND[("haar", n.name)]
            if abs(c - 0.13) < 1e-6 and abs(d) < 1e-9:
                n.inputs["To Min"].default_value = var.get("bein_mel", 0.13)
            elif abs(c) < 1e-9 and abs(d - 0.12) < 1e-6:
                n.inputs["To Max"].default_value = var.get("ruecken_mel", 0.12)
            elif abs(c) < 1e-9 and abs(d - 0.2) < 1e-6:
                n.inputs["To Max"].default_value = var.get("spitze_mel", 0.2)
            elif abs(c - 0.74) < 1e-6 and abs(d - 0.90) < 1e-6:
                o = var.get("mel_off", 0.0)
                n.inputs["To Min"].default_value = 0.74 + o
                n.inputs["To Max"].default_value = 0.90 + o
        if n.type == "BSDF_HAIR_PRINCIPLED":
            n.inputs["Roughness"].default_value = var.get("rough", 0.34)
            n.inputs["Radial Roughness"].default_value = var.get("radial", 0.8)
        if n.name == "bake_mix":
            n.inputs[0].default_value = var.get("diffus", 0.0)
    fm = bpy.data.materials["fell"]
    for n in fm.node_tree.nodes:
        if n.type == "MAP_RANGE" and ("fell", n.name) in GRUND:
            c, d = GRUND[("fell", n.name)]
            if abs(c - 0.62) < 1e-6:
                n.inputs["To Min"].default_value = var.get("haut_bein", 0.62)
    hz = bpy.data.materials["haar_zeh"]
    hz.node_tree.nodes["zeh_hell"].inputs[1].default_value = var.get("zeh_hell", 0.0)
    for n in hz.node_tree.nodes:
        if n.type == "MIX_SHADER":
            n.inputs[0].default_value = var.get("diffus", 0.0)


def neutrale_welt(scene, oben=1.05, unten=0.72):
    """Wie baer_export.py:69-87 (Licht der alten Ansichten)."""
    w = bpy.data.worlds.new("backlicht")
    w.use_nodes = True
    nt = w.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.clamp = True
    mr.inputs["From Min"].default_value = -1.0
    mr.inputs["From Max"].default_value = 1.0
    mr.inputs["To Min"].default_value = unten
    mr.inputs["To Max"].default_value = oben
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    nt.links.new(sp.outputs[2], mr.inputs["Value"])
    nt.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    nt.links.new(mr.outputs[0], nt.nodes["Background"].inputs[1])
    scene.world = w


def stufe_ansichten(auf):
    E = lade_export()
    Q = E["quelle"]("spiel")
    log("Hochmodell steht")
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = d.type == "OPTIX"
    assert any(d.use and "4090" in d.name for d in prefs.devices), "keine RTX 4090 mit OptiX"
    print("BILD Geraete", [d.name for d in prefs.devices if d.use], flush=True)
    scene.cycles.device = "GPU"
    scene.cycles.samples = auf.get("samples", 96)
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = "OPTIX"
    scene.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.max_bounces = 8
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    neutrale_welt(scene)
    scene.render.film_transparent = True
    scene.render.use_persistent_data = True
    im = scene.render.image_settings
    im.file_format = "OPEN_EXR"
    im.color_mode = "RGBA"
    im.color_depth = "32"
    im.exr_codec = "ZIP"
    fell_vorbereiten()
    if auf.get("pose"):
        back_pose_setzen()
        log("Back-Pose gesetzt: hinten %.0f, vorn %.0f Grad" % (POSE_HINTEN, POSE_VORN))
    res = auf.get("res", 2048)
    alle = {v["name"]: v for v in kamera_koerper(res) + kamera_unterseite(res, auf.get("schnitt", False)) + kamera_pose(res)}
    namen = auf.get("views") or list(alle)
    cam_d = bpy.data.cameras.new("bake")
    cam_d.type = "ORTHO"
    cam = bpy.data.objects.new("bake", cam_d)
    scene.collection.objects.link(cam)
    scene.camera = cam
    erg = {}
    for vname, var in auf["varianten"].items():
        fell_variante(var)
        aus = auf["aus"] if len(auf["varianten"]) == 1 else os.path.join(auf["aus"], vname)
        os.makedirs(aus, exist_ok=True)
        kam = []
        for nm in namen:
            v = alle[nm]
            kam.append(v)
            out = os.path.join(aus, nm + ".exr")
            if os.path.exists(out) and not auf.get("neu", False):
                continue
            cam_d.ortho_scale = v["ortho"]
            c, d = Vector(v["c"]), Vector(v["d"])
            cam.location = c + d * 12.0
            cam.rotation_mode = "QUATERNION"
            cam.rotation_quaternion = (-d).to_track_quat("-Z", "Y")
            cam_d.clip_start = 0.1 if "clip" not in v else 12.0 - v["clip"]
            cam_d.clip_end = 40.0
            scene.render.resolution_x = scene.render.resolution_y = v["res"]
            scene.render.filepath = out
            t = time.time()
            bpy.ops.render.render(write_still=True)
            img = bpy.data.images.load(out)
            img.colorspace_settings.name = "Non-Color"
            w_, h_ = img.size
            a = np.empty(w_ * h_ * 4, dtype=np.float32)
            img.pixels.foreach_get(a)
            bpy.data.images.remove(img)
            a = a.reshape(h_, w_, 4)
            al = a[..., 3]
            m = al > 0.45
            lum = float(((a[..., :3][m] / al[m][:, None]) @ np.array((0.2126, 0.7152, 0.0722))).mean()) if m.any() else 0.0
            erg["%s/%s" % (vname, nm)] = lum
            print("BILD", vname, nm, "Helligkeit linear %.4f" % lum, "%.1fs" % (time.time() - t), flush=True)
        json.dump(kam, open(os.path.join(aus, "kameras.json"), "w"), indent=1)
        json.dump(var, open(os.path.join(aus, "variante.json"), "w"), indent=1)
    json.dump(erg, open(os.path.join(auf["aus"], "helligkeit_%s.json" % auf.get("name", "lauf")), "w"), indent=1)
    print("BILD_OK", len(erg), flush=True)


# ------------------------------------------------------------------ Stufe backen
# Stellschrauben (alle ueber die Umgebung BAER_TX_<NAME> aenderbar, Vorgabe = gebaute Fassung)
def _par(n, v):
    return float(os.environ.get("BAER_TX_" + n, v))


P_EXP = _par("EXP", 10.0)         # Gewicht cos^P_EXP (bisher 7; schaerfer = weniger Mischung, weniger Schmiere)
A_REF = _par("A_REF", 0.5)        # Bezugs-Blickwinkel zur Haarrichtung fuer den Ausgleich (0,5 = Ruecken von oben)
UNTEN_LIFT = _par("UNTEN", 0.45)  # Unterseite (Normale nach unten, Innenbein, Achsel, Leiste, Bauch) heller
BEIN_LIFT = _par("BEIN", 0.20)    # Unterbeine heller (gegen schwarze Pranken im Spiel-Licht)
STR_AMP = _par("STRAEHNE", 0.30)  # Haarbuesche: Helligkeitshub (Nachbesserung 09.11.: 0,15 -> 0,30, Buesche breiter und laenger)
RUHIG_K = _par("RUHIG", 0.80)     # Nachbesserung: Gesprenkel an Beinen/Hinterteil/gegen die Haarspitzen so stark glaetten (0 = aus)
CAP_L = _par("CAP_LEISTE", 0.95)  # Nachbesserung: Leiste/Innenbein hinten hoechstens so hell (x Ruecken, Mittel ueber wenige cm)
CAP_U = _par("CAP_UNTEN", 1.08)   # Nachbesserung: uebrige Unterseite (Kehle, Achsel, Innenbein vorn, Brust, Bauch) hoechstens so hell
SAT_MAX = _par("SAT_MAX", 0.56)   # Nachbesserung: Saettigung (max-min)/max des Fells hoechstens so hoch (rostorange Pfoten)
AO_K = _par("AO", 0.38)           # Faltenschatten: so viel dunkler in tiefen Falten (offene Flaeche 0)
SCHAERFE = _par("SCHAERFE", 0.97) # Unschaerfemaske (2c 0,85; baer-gross Bau Textur 12.11.: 0,97, Straehnen Ruecken im neuen Netz wieder >= 0,063)
KONTRAST_D = _par("KONTRAST", 0.55)  # Gesprenkel daempfen, wo nur Ansichten gegen die Haarspitzen sehen
NUR_NEU = os.environ.get("BAER_TX_NUR_NEU", "") == "1"   # Gegenprobe: 1 = alte Ansichten, kein Ausgleich (wie baer-anim)
AUSNAME = os.environ.get("BAER_TX_NAME", "fell")
ANS_NEU = ANS_DIR + "ansichten/"
ANS_POSE = ANS_DIR + "ansichten_pose/"
POSE_W = _par("POSE_W", 2.0)          # Gewicht der Back-Pose-Ansichten (0 = aus)
KARTEN = NETZ + "karten/karten_2048.npz"
BESTAND_PNG = ARB_FELL + "bestand/NCBear_2048.png"   # Nachbesserung: 2048er des Stands vor baer-fell (Krallen-Lesefeld, wie baer-fell)
SOHLE_JSON = NETZ + "sohle_layout.json"
ZWISCHEN_PNG = NETZ + "zwischen_%s/42/media/textures/WorldItems/NCBear.png" % NETZ_NAME
# Lauf baer-pfoten: Bezug fuer Farbabgleich und Hals-Naht. Der Zwischenstand des Netz-Bauers ist auf dem Ruecken ~15 % dunkler als baer-fell
# (andere Fell-Ansichten); Vorgabe deshalb die fertige baer-fell-Textur, per 3D-Naechster auf die neue UV uebertragen
# (textur/werkzeug/fell_uebertrag.py -> textur/zw_fell_2048.png; unter Spiel-z 0,30 Zwischenstand, dort ungenutzt)
ZWISCHEN_PNG = os.environ.get("BAER_TX_ZWISCHEN", ZWISCHEN_PNG)
NAHT_A, NAHT_B, NAHT_C = _par("NAHT_A", 0.035), _par("NAHT_B", 0.07), _par("NAHT_C", 0.20)   # Hals (Abstand zur Kopfhuelle,
#   Hochmodell-m): bis A altes Fell, A..B Uebergang, bis C Farbe grob an das alte Fell angeglichen
INNEN_TOL = _par("INNEN_TOL", 0.010)   # Innenbeine: Tiefen-Toleranz der waagerechten Ansichten (sonst 0,030)
INNEN_W = _par("INNEN_W", 0.15)        # Innenbeine: Gewicht der waagerechten Ansichten
K_SEITE = _par("K_SEITE", 3.0)         # Gewicht exp(-K (a - 0,55)): Haar von der Seite gesehen bevorzugen
INNENBEIN = (6, 7)                # Regionen ohne waagerechte Ansichten (Bauchluecke, W5)
RILLE_K = _par("RILLE", 0.45)     # Lauf baer-pfoten: Zehenrillen so viel dunkler (volle Verdeckung im Kleinen)
PF_ABGLEICH = os.environ.get("BAER_TX_PF_ABGLEICH", "1") == "1"   # Pfoten-Helligkeit je Hoehe an baer-fell (siehe stufe_backen)
BAND_K = _par("BAND", 1.00)       # Uebergang Rumpf/Bein: waagerechte Helligkeits-Baender so stark einebnen (v9)
PF_ZIEL = tuple(v / 255.0 for v in (62.0, 59.0, 50.0, 60.0, 61.0))   # Luma-Ziel je Band 0-4-8-12-20-30 cm (baer-fell texel_fix.npz)
RILLE_A, RILLE_B = _par("RILLE_A", 0.16), _par("RILLE_B", 0.42)   # Verdeckung (Reichweite 3 cm) von .. bis voll
RAND_K = _par("RAND_K", 1.15)     # v12: Fell unter 5 cm hoechstens so viel heller als das Fell 4-8 cm desselben Beins (heller Sohlenring)


def sst(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def srgb_inv(s):
    s = np.clip(s, 0.0, 1.0)
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def png_laden(pfad):
    img = bpy.data.images.load(pfad)
    img.colorspace_settings.name = "Non-Color"
    w, h = img.size
    a = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(a)
    bpy.data.images.remove(img)
    return a.reshape(h, w, 4)[..., :3]


def png_schreiben(pfad, col):
    H, W = col.shape[:2]
    img = bpy.data.images.new(os.path.basename(pfad), W, H, alpha=False)
    img.colorspace_settings.name = "Non-Color"
    rgba = np.ones((H, W, 4), dtype=np.float32)
    rgba[..., :3] = np.clip(col, 0.0, 1.0)
    img.pixels.foreach_set(rgba.ravel())
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    img.filepath_raw = pfad
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)


def wachsen(m, n):
    m = m.copy()
    for _ in range(n):
        g = m.copy()
        g[1:] |= m[:-1]
        g[:-1] |= m[1:]
        g[:, 1:] |= m[:, :-1]
        g[:, :-1] |= m[:, 1:]
        m = g
    return m


def abstand_innen(m, n):
    """Texel-Abstand (4er-Nachbarschaft) vom Rand der Maske nach innen, bis n."""
    d = np.zeros(m.shape, dtype=np.float32)
    cur = m.copy()
    for k in range(1, n + 1):
        e = cur.copy()
        e[1:] &= cur[:-1]
        e[:-1] &= cur[1:]
        e[:, 1:] &= cur[:, :-1]
        e[:, :-1] &= cur[:, 1:]
        d[cur & ~e] = k - 0.5
        cur = e
        if not cur.any():
            break
    d[cur] = n
    return d


def haarrichtung(Q, P, Nn):
    """Haarrichtung des Hochmodells (Partikel: Normale x normal_factor + object_align, baer_quelle_anim.py:1692-1694):
    Deckhaar am Rumpf, Beinfell an den Beinen (Gruppe d_bein wie :1591-1595)."""
    z, x = P[:, 2], P[:, 0]
    bein = 1.0 - sst(Q["lz"](0.22), Q["lz"](0.56), z)
    bein = np.where((x > -0.25) & (x < 0.12), bein * 0.15, bein)
    hr = Nn * 0.066 + np.array((-0.052, 0.0, -0.036))
    hb = Nn * 0.046 + np.array((-0.012, 0.0, -0.028))
    h = hr * (1.0 - bein)[:, None] + hb * bein[:, None]
    h = h / np.maximum(np.linalg.norm(h, axis=1, keepdims=True), 1e-9)
    if PF_SPIEL is not None:
        # Lauf baer-pfoten: Pfotenhaar des Hochmodells (baer_quelle_pfote.py:2018-2022, Richtung wie wachse :702-725): Zielrichtung F =
        # (0,9 unter Spiel-z 0,10 | -0,15 darueber, 0, -1) in die Flaeche gelegt, Anteil Normale lift 0,22. Gilt am Unterschenkel/Fuss
        # (Spiel-z < 0,30, weich bis 0,36, nur wo 'bein'); darueber wie baer-fell.
        zs = PF_SPIEL[:, 2]
        fx = 0.9 - 1.05 * sst(0.08, 0.12, zs)
        F = np.stack((fx, np.zeros_like(fx), -np.ones_like(fx)), 1)
        t = F - Nn * np.einsum("ij,ij->i", F, Nn)[:, None]
        t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
        hp = Nn * 0.22 + t * 0.78
        hp /= np.maximum(np.linalg.norm(hp, axis=1, keepdims=True), 1e-9)
        wp = ((1.0 - sst(0.28, 0.36, zs)) * sst(0.3, 0.6, bein))[:, None]
        h = h * (1.0 - wp) + hp * wp
        h = h / np.maximum(np.linalg.norm(h, axis=1, keepdims=True), 1e-9)
    return h, bein


PF_SPIEL = None    # Lauf baer-pfoten: Texel in Spielmetern (stufe_backen setzt es vor haarrichtung)


def haar_tangente(h, Nn):
    """Nachbesserung 09.11.: Haarrichtung in der Flaeche fuer die gemalten Buesche. Wo das Haar fast senkrecht aus der Flaeche steht
    (Schwanzansatz, Hinterteil), ist die projizierte Richtung instabil (Wirbel); dort weich auf 'abwaerts in der Flaeche' ueberblenden."""
    ht = h - np.einsum("ij,ij->i", h, Nn)[:, None] * Nn
    lh = np.linalg.norm(ht, axis=1)
    ab = np.array((0.0, 0.0, -1.0))
    dt = ab[None, :] - Nn[:, 2:3] * Nn
    ld = np.linalg.norm(dt, axis=1)
    hinten = np.array((-1.0, 0.0, 0.0))
    dh = hinten[None, :] - Nn[:, 0:1] * Nn
    dt = np.where((ld < 0.2)[:, None], dh, dt)
    ld = np.linalg.norm(dt, axis=1)
    b = sst(0.25, 0.60, lh)
    d = b[:, None] * ht / np.maximum(lh, 1e-9)[:, None] + (1.0 - b)[:, None] * dt / np.maximum(ld, 1e-9)[:, None]
    return d / np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-9)


def glaetten_insel(img, pos, inn, runden, d_max):
    """Nachbesserung 09.11.: Weichzeichnen im Texturraum nur zwischen Texeln derselben Insel (3D-Abstand der Nachbarn < d_max,
    Hochmodell-m); 5-Punkt-Stern, Mitte doppelt. runden 18 ~ sigma 2,5 Texel (2048)."""
    c = img.astype(np.float32).copy()
    ok_n = []
    for ax, sh in ((0, 1), (0, -1), (1, 1), (1, -1)):
        pn = np.roll(pos, sh, ax)
        mn = np.roll(inn, sh, ax)
        ok_n.append((mn & inn & (((pn - pos) ** 2).sum(-1) < d_max * d_max)).astype(np.float32))
    wsum = 2.0 + sum(ok_n)
    for _ in range(runden):
        acc = c * 2.0
        for (ax, sh), o in zip(((0, 1), (0, -1), (1, 1), (1, -1)), ok_n):
            acc += np.roll(c, sh, ax) * o[..., None]
        c = np.where(inn[..., None], acc / wsum[..., None], c)
    return c


def buesche_3d(P, Nn, h_t, zelle=0.030, sig_l=0.045, sig_q=0.0075, n_max=0.03, saat=23, block=200000):
    """Nachbesserung 09.11.: Haarbuesche als Summe einzelner gestreckter Flecken um zufaellige Mittelpunkte eines 3D-Gitters (Zelle
    'zelle', Hochmodell-m, je Zelle ein Busch mit Zufallslage). Je Texel die Buesche der 27 Nachbarzellen: Abstand in der Flaeche
    laengs der eigenen Haarrichtung (sig_l) und quer (sig_q); Buesche hinter einer duennen Stelle (Abstand laengs der Normale > n_max)
    zaehlen nicht. Ergebnis busch 0..1 (Maximum) und spitze (vorderes Ende des Busches)."""
    n = len(P)
    busch = np.zeros(n, dtype=np.float32)
    spitze = np.zeros(n, dtype=np.float32)
    t_q = np.cross(Nn, h_t)
    t_q /= np.maximum(np.linalg.norm(t_q, axis=1, keepdims=True), 1e-9)

    def zh(ix, iy, iz, k):
        return np.mod(np.sin(ix * 12.9898 + iy * 78.233 + iz * 37.719 + k * 4.581) * 43758.5453, 1.0)

    for s0 in range(0, n, block):
        sl = slice(s0, min(s0 + block, n))
        Pb, Hb, Qb, Nb = P[sl], h_t[sl], t_q[sl], Nn[sl]
        g = np.floor(Pb / zelle)
        bb = np.zeros(len(Pb), dtype=np.float32)
        sp = np.zeros(len(Pb), dtype=np.float32)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    ix, iy, iz = g[:, 0] + dx, g[:, 1] + dy, g[:, 2] + dz
                    C = np.stack(((ix + zh(ix, iy, iz, 1)) * zelle, (iy + zh(ix, iy, iz, 2)) * zelle, (iz + zh(ix, iy, iz, 3)) * zelle), 1)
                    d = Pb - C
                    dn = np.abs(np.einsum("ij,ij->i", d, Nb))
                    dl = np.einsum("ij,ij->i", d, Hb)
                    dq = np.einsum("ij,ij->i", d, Qb)
                    st = 0.65 + 0.35 * zh(ix, iy, iz, 4)
                    sl_ = sig_l * (0.75 + 0.5 * zh(ix, iy, iz, 5))
                    w = np.exp(-(dl / sl_) ** 2 - (dq / sig_q) ** 2) * st * (dn < n_max) * (zh(ix, iy, iz, 6) > 0.12)
                    w = w.astype(np.float32)
                    bb = np.maximum(bb, w)
                    sp = np.maximum(sp, w * sst(0.2, 1.0, dl / sl_).astype(np.float32))
        busch[sl] = bb
        spitze[sl] = sp
    return busch, spitze


def merkmale(a, dz, c, bein):
    return np.stack((a, a * a, dz, c, a * bein, dz * bein), 1)


def ao_punkte(V, T, Nv, n_strahl=64, weit=0.26, nur=None):
    """Umgebungsverdeckung je Punkt am Spielnetz (Hochmodell-Masse), nur nahe Flaechen (Falten), mathutils-BVH.
    Lauf baer-pfoten: nur = Punktnummern (nur diese rechnen, Rest 0)."""
    from mathutils.bvhtree import BVHTree
    bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in V], [tuple(map(int, t)) for t in T])
    rng = np.random.default_rng(5)
    # kosinusgewichtete Halbkugel, feste Richtungen je Punkt (gedreht)
    u1, u2 = rng.random(n_strahl), rng.random(n_strahl)
    r_, ph = np.sqrt(u1), 2 * math.pi * u2
    L = np.stack((r_ * np.cos(ph), r_ * np.sin(ph), np.sqrt(1 - u1)), 1)
    occ = np.zeros(len(V))
    for i in (range(len(V)) if nur is None else nur):
        n = Nv[i]
        a = np.array((1.0, 0, 0)) if abs(n[0]) < 0.9 else np.array((0, 1.0, 0))
        t1 = np.cross(n, a)
        t1 /= np.linalg.norm(t1)
        t2 = np.cross(n, t1)
        D = L[:, 0:1] * t1 + L[:, 1:2] * t2 + L[:, 2:3] * n
        o = Vector(V[i] + n * 0.004)
        s = 0.0
        for d in D:
            hit = bvh.ray_cast(o, Vector(d), weit)
            if hit[0] is not None:
                s += 1.0 - (hit[3] / weit) ** 2
        occ[i] = s / n_strahl
    return occ


SOHLE_Q = _par("SOHLE_Q", 0.95)   # Lauf baer-pfoten: Zehenballen so viel groesser gemalt (baer-fell 0,87; der neue Plan hat die Ballen schon gross)
LEDER_L = _par("LEDER_L", 0.50)   # Lauf baer-pfoten: Ballen-Kuppe sRGB 0-1 (Kevins Fotos: hell-grau-ledern, deutlich heller als das Fell)
FURCHE_L = _par("FURCHE_L", 0.17) # Furche/Haut zwischen Ballen und Fell
FERSE_X = _par("FERSE_X", -0.535) # Hinterfuss: hinter diesem x zieht die Sohlenplatte an der Ferse hoch (Spielmeter; v4 -0,546 gab einen
#                                   Flaschenhals vor der Ferse, weil die Platte dort schon schmaler ist)
FERSE_Z = (_par("FERSE_Z0", 0.006), _par("FERSE_Z1", 0.011))   # ... bis zu dieser Hoehe (Spielmeter, weich; v11: vorher 1,1-1,7 cm,
#                                   die Grenze lag dann am groben Inselrand und war im Liegen gezackt zu sehen)
PAD_Z = (0.005, 0.010)            # sonst liegen Ballen unten (Abdruck + Relief 1 cm)
ZEH_Z = (0.010, 0.016)            # Zehenballen ausserhalb der Insel bis zu dieser Hoehe (Zehen vorn gerundet)
PAD_FARBE = np.array((1.08, 1.0, 0.88))   # warmes Grau (Kevins Sohlenfoto, nur angesehen; v3 waermer als v2 1,05/1/0,93)
RISS_K = _par("RISS", 0.06)        # Lederrisse so viel dunkler (v2 0,14 wirkte wie Pflaster)
FALTE_K = _par("FALTE", 0.035)     # Querfalten auf Platte/Handballen (v3 0,09 mit Welle: sichtbare Wellenlinien, weg)
# Nachbesserung 1 (fix1, 09.11.2026 abends; _arbeit/baer_pfote/fix1_bericht.md): Ferse abgerollt (ballen_q3), Leder unruhiger (Flecken
# 3-5 cm), Furche schmaler, Fell zwischen den Ballen heller, Handwurzelballen nur unten und dunkler, Uebergang Bein (neuer Kegel
# Spiel-z 0,14-0,34) in die Band-Glaettung, an den Unterschenkeln wieder etwas Straehnen. BAER_TX_FIX1=0 = Stand vorher.
FIX1 = os.environ.get("BAER_TX_FIX1", "1") == "1"
FIX1_ROLL = _par("ROLL", 1.0)      # Ferse: x_u = x - ROLL * z hinter FIX1_ROLL_X
FIX1_ROLL_X = _par("ROLL_X", -0.545)
FIX1_FLECK = _par("FLECK", 0.08)   # Leder: grosse Flecken (3-6 cm) +-8 %
FIX1_HW_DUNKEL = _par("HW_DUNKEL", 0.72)   # Handwurzelballen so viel dunkler als die Sohle
FIX1_ZEH_Q = _par("ZEH_Q", 0.86)  # hinten: Zehenballen so viel groesser (q x 0,86; vorher SOHLE_Q 0,95)
FIX1_ZEH_Z = (_par("ZEH_Z0", 0.016), _par("ZEH_Z1", 0.024))   # hinten: Zehenballen an den Zehen bis zu dieser Hoehe
# Lauf baer-2c, Bauer Textur (SPEZ_2C.md 4 / 6.2 / 2.5, soll_2c.json C_hinterfuss / E_kopf)
C2C = os.environ.get("BAER_TX_2C", "1") == "1"
FELD = os.environ.get("BAER_TX_FELD", "") if C2C else ""      # dichte Huelle vor/nach form_2c (Spielmeter): Projektion am Netz vor form_2c
NUR_TEXEL = os.environ.get("BAER_TX_NUR_TEXEL", "") == "1"
# Hinterfuss-Sohle (Kevins Sitzvorlage, nur angesehen): dunkelbraun bis schwarz, ledrig; Median sRGB 62/42/30 +-12, R - B >= 20,
# Ballenkuppe +10..+15 heller, Furchen Luma <= 45
H_LEDER_L = _par("H_LEDER_L", 0.250)        # Kuppe (sRGB 0-1, Luma); Rand H_LEDER_L x H_DOM0 (v1 0,235/0,66: im Licht B terrakotta-rot;
H_DOM0 = _par("H_DOM0", 0.50)               #   v2-v5 0,200/0,62: Kuppe nur +3 ueber dem Median, v6 0,215/0,55 +6, v7 0,235/0,46 +8; Soll +10..+15)
H_DOM_EXP = _par("H_DOM_EXP", 1.4)          # Woelbung hinten: Exponent (vorn 0,6): heller Glanz nur in der Ballenmitte
H_FARBE = np.array((1.30, 0.94, 0.76))      # Farbton des Leders (Luma 1,0): ~52/38/30, weniger rot als v1 (1,37/0,92/0,66)
H_FURCHE_L = _par("H_FURCHE_L", 0.100)      # Furche zwischen den Ballen (Luma ~26)
H_FURCHE_FARBE = np.array((1.25, 0.95, 0.80))
H_PLATTE_EX = _par("H_PLATTE_EX", 2.3)      # Sohlenballen hinten in der Textur runder (Super-Oval-Exponent 3,4 des Netzes -> 2,3): Ecken = Fellkranz
H_ZEH_Q = _par("H_ZEH_Q", 0.80)             # Zehenballen hinten so viel groesser gemalt (fix1 0,86)
H_KRANZ = (_par("H_KRANZ0", 4.0), _par("H_KRANZ1", 8.5))   # Fellkranz hinten: voll bis .. weich bis .. Texel (2048) vom Inselrand
H_KRANZ_LANG = (_par("H_KRANZ_L0", 7.0), _par("H_KRANZ_L1", 9.0))   # Straehnen des Kranzes: 7..16 Texel lang (vorher 4..11)
H_FERSE_FREI = _par("H_FERSE_FREI", -0.530)   # hinter diesem x (Ferse) kein Pflicht-Kranz auf der Insel (Leder laeuft um die Ferse)
H_ROLL_ZMAX = _par("H_ROLL_ZMAX", 0.022)      # 2c: Leder an der Fersen-Hinterkante nur bis 2,2 cm hoch (fix1 ~3,5), darueber Fellkranz
# Krallen dunkler (soll_2c.json C_hinterfuss krallen_rgb; vorn hoechstens dunkler)
KRALLE_H = (np.array((60.0, 47.0, 38.0)) / 255.0, np.array((66.0, 52.0, 42.0)) / 255.0)   # Wurzel, Spitze (sRGB); v5 58/46/37 -> 128/112/94
#   gab im Lesefeld gemittelt einfarbig 97/83/69 (die UV einer Kralle liegen in 1-2 Texeln): Wurzel-Grenze 70/55/45 verfehlt -> hinten
#   einfarbig dunkel ("kurze dunkle Krallen" der Vorlage)
KRALLE_V = (np.array((66.0, 54.0, 44.0)) / 255.0, np.array((112.0, 98.0, 82.0)) / 255.0)   # fix1 2c (Pruefbericht m4 "Vorderkrallen noch
#   hell", Kevin: weisse Krallen): vorn 72/59/48 -> 150/134/113 (Mittel 108/93/76) -> 66/54/44 -> 112/98/82
# Kopf-Passung (SPEZ 6.2 Punkt 4): Ziel-Helligkeit je Abstand zum Kopf (Spielmeter) als Anteil am Kopfmittel (Texel-Luma, ohne Maul-Flecken)
HALS_D = (0.00, 0.05, 0.12, 0.20, 0.30, 0.40, 0.50, 0.62)
HALS_F = (1.00, 1.03, 1.03, 1.02, 0.97, 0.90, 0.82, 0.00)   # v2 (v1: 0,97/0,96/0,94/0,88/0,80 -> Bild-Ring 0,78 statt 0,76)
HALS_FARBE = _par("HALS_FARBE", 0.55)       # so viel zum Farbton des Kopfes (bis 35 cm, dann aus)
HALS_FEIN = _par("HALS_FEIN", 0.60)         # Buesche nahe am Kopf (bis 20-32 cm) so viel schwaecher, Nachschaerfen halb
# Fellbehang (SPEZ 2.5): Straehnen-Hub ueber den Behang-Kanten, Schattenband darunter
BEHANG_HUB = _par("BEHANG_HUB", 0.55)
BEHANG_SCHATTEN = _par("BEHANG_SCHATTEN", 0.16)
BRUST_K = _par("BRUST_K", 0.85)            # Brust-Glaettung (Stufe quer ueber die Brust) so stark
# Lauf baer-gross, Bau Textur (11.11.2026, SPEZ_GROSS.md 5.1 G2 "dunkler Ring um den Kopf"; BAER_TX_G2=0 = Rechnung wie 2c):
# Koerper-Texel nahe am Kopf (dk bis G2_K1) und das Kopfrand-Band (Kopf-Texel bis G2_H1 <= 3 cm von der Kopfnaht, ohne Gesicht, Augen, Nase,
# Schnauze, Lippen, Ohren und Maul-Inneres) im geglaetteten Log-Luma-Feld (Rec. 709) auf G2_ZIEL anheben: nur heller, Straehnen und
# Farbton bleiben (Faktor je Texel auf alle Kanaele). Kopf-Texel weiter als G2_H1 von der Naht bleiben bit-gleich (Faktor genau 1 = nicht
# geschrieben). Der Rand (UV-Polster) der Kopf-Inseln folgt dem Faktor der Nachbar-Texel (sonst dunkler Saum ueber das 2x2-Mittel/bilinear).
G2 = os.environ.get("BAER_TX_G2", "1") == "1"
G2_ZIEL = _par("G2_ZIEL", 110.0) / 255.0                    # Ziel-Luma (sRGB 0-1) des geglaetteten Feldes (erster Agent 106; 12.11.: 110 = Kopf-Rand)
G2_K0, G2_K1 = _par("G2_K0", 0.040), _par("G2_K1", 0.090)   # Koerper: voll bis K0, aus ab K1 (Abstand zum Kopf, Spielmeter; vorher 0,035/0,075)
G2_H0, G2_H1 = _par("G2_H0", 0.012), _par("G2_H1", 0.030)   # Kopf: voll bis H0, aus ab H1 (Abstand zur Kopfnaht, Spielmeter; Spez <= 0,03)
G2_MAX = _par("G2_MAX", 1.45)                               # hoechstens so viel heller
G2_RUNDEN = int(_par("G2_RUNDEN", 4))                       # Glaettung des Luma-Feldes (Runden ueber das Netz)
G2_OHR = _par("G2_OHR", 0.025)                              # Abstand zur Ohrschale (Hochmodell-m), ab dem das Band wieder darf
# Lauf baer-gross fix1 (12.11.2026, pruef_optik Befund 2, pruef_technik M1; BAER_TX_FRONT=0 = Rechnung wie Bau Textur): Front beim Aufrichten
# ohne drei dunkle Laengsstreifen. (1) Oberarm: im geglaetteten Log-Luma-Feld auf FR_ARM_K x Flanke/Schulter (gleiche Seite, Mittel) anheben,
# voll ab Ellbogen + FR_ARM_B, aus unter Ellbogen + FR_ARM_A (Ruhe-z, Spielmeter; Ellbogen z 0,41): das Arm-Dunkel beginnt erst am Unterarm,
# mit ~10 cm Verlauf statt einer Kante an der Schulter. (2) Bauchmitte (Unterseite zwischen den Beinen) auf FR_BAUCH_K x Flanke auf
# Bauchhoehe anheben, weich zur Seite und zu den Beinen. Nur heller, Straehnen/Farbton bleiben (Faktor je Texel auf alle Kanaele); Kopf,
# Sohlen und Krallen unberuehrt (rumpf_t, sohle 0, Kopf-Abstand). Arm-Anteil je Texel aus den Hautgewichten (FR_GEW, Netz-Reihenfolge).
FRONT = os.environ.get("BAER_TX_FRONT", "1") == "1"
FR_GEW = os.environ.get("BAER_TX_GEW", ARB + "glb_netz/gewichte_netz.npz")
FR_ARM_K = _par("FR_ARM_K", 0.92)       # Oberarm-Ziel: Anteil am Flanken-/Schulter-Luma
FR_ARM_A, FR_ARM_B = _par("FR_ARM_A", -0.16), _par("FR_ARM_B", -0.04)  # Verlauf relativ zur Ellbogenhoehe (m): voll bis 4 cm unter dem
#                                                                          Ellbogen, aus 16 cm darunter (Unterarm-Mitte; Handgelenk z 0,10)
FR_ELL_Z = _par("FR_ELL_Z", 0.41)       # Ellbogen in Ruhe (J Forearm z; Schulter 0,72, Oberarm 0,316 m)
FR_BAUCH_K = _par("FR_BAUCH_K", 0.95)   # Bauchmitte-Ziel: Anteil am Flanken-Luma auf Bauchhoehe (Varianten fa 0,88 / fb, fc 0,95)
FR_MAX = _par("FR_MAX", 1.7)            # hoechstens so viel heller


def fell_2d(X, Y, cx, cy, zelle=0.006, saat=0):
    """Fell auf der Sohlen-Insel (Spielmeter, flach): kurze Straehnen um zufaellige Punkte eines 2D-Gitters, Richtung vom Ballen-
    Mittelpunkt (cx, cy) nach aussen (Haar am Sohlenrand zeigt vom Ballen weg), ~1,2 cm lang, ~0,15 cm breit. Gibt 0..1 zurueck."""
    gx, gy = np.floor(X / zelle), np.floor(Y / zelle)
    r = np.stack((X - cx, Y - cy), 1)
    r /= np.maximum(np.linalg.norm(r, axis=1, keepdims=True), 1e-9)
    out = np.zeros(len(X))
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            ix, iy = gx + dx, gy + dy
            h1 = np.mod(np.sin(ix * 12.9898 + iy * 78.233 + saat * 3.1) * 43758.5453, 1.0)
            h2 = np.mod(np.sin(ix * 39.3468 + iy * 11.135 + saat * 1.7) * 24634.6345, 1.0)
            h3 = np.mod(np.sin(ix * 73.156 + iy * 52.235 + saat * 0.9) * 31415.9265, 1.0)
            ddx, ddy = X - (ix + h1) * zelle, Y - (iy + h2) * zelle
            dl = ddx * r[:, 0] + ddy * r[:, 1]
            dq = -ddx * r[:, 1] + ddy * r[:, 0]
            w = np.exp(-(dl / (0.006 * (0.7 + 0.6 * h3))) ** 2 - (dq / 0.0011) ** 2) * (0.6 + 0.4 * h3)
            out = np.maximum(out, w)
    return out


def _voronoi(X, Y, zelle, saat):
    """2D-Zellmuster (Spielmeter): Abstand zur naechsten und zweitnaechsten Zellmitte (Lederrisse dort, wo beide fast gleich sind)."""
    gx, gy = np.floor(X / zelle), np.floor(Y / zelle)
    d1 = np.full(len(X), 9.0)
    d2 = np.full(len(X), 9.0)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            ix, iy = gx + dx, gy + dy
            hx = np.mod(np.sin(ix * 12.9898 + iy * 78.233 + saat * 1.37) * 43758.5453, 1.0)
            hy = np.mod(np.sin(ix * 39.3468 + iy * 11.135 + saat * 2.71) * 24634.6345, 1.0)
            d = np.hypot(X - (ix + hx) * zelle, Y - (iy + hy) * zelle)
            d2 = np.where(d < d1, d1, np.minimum(d2, d))
            d1 = np.minimum(d1, d)
    return d1, d2


def pfoten_ballen(pn):
    """Ballen einer Pfote aus netz/sohle_layout.json (Spielmeter): Zehenballen als Ellipsen (Name, cx, cy, ax, ay, Biegung),
    Sohlenplatte (hinten) bzw. Handballen (vorn) als Vieleck (Name, cx, cy, 0, 0, 0, Vieleck) - Form wie ballen_q in baer_export_pfote.py."""
    E_ = lade_export_cache()
    pl = []
    for b in json.load(open(SOHLE_JSON))["pfoten"][pn]["ballen"]:
        if "vieleck" in b:
            assert abs(b["vieleck_skala"] - E_["VIELECK_SKALA"]) < 1e-12
            pl.append((b["name"], b["cx"], b["cy"], 0.0, 0.0, 0.0, np.array(b["vieleck"], dtype=float)))
        else:
            pl.append((b["name"], b["cx"], b["cy"], b["ax"], b["ay"], b["biegung"]))
    return pl


def ballen_q3(pl, pn, X, Y, Z, insel=False):
    """Normierter Ballen-Abstand q (< 1 im Ballen) in 3D: Zehenballen (q x SOHLE_Q) und Platte/Handballen in (x, y) wie der Netz-Plan,
    dazu die Hoehe (Ballen nur unten; hinten zieht die Platte hinter FERSE_X bis FERSE_Z hoch: die Ferse ist 'abgerollt').
    Gibt q und Platte ja/nein zurueck."""
    E_ = lade_export_cache()
    zeh = [b for b in pl if len(b) == 6]
    pla = [b for b in pl if len(b) > 6]
    if C2C and pn[0] == "H":
        # 2c: Sohlenballen in der Textur runder als das Netz (Kevins Vorlage: ovale Sohle, Fellkranz rundum); Masse wie C2C_PLAN_H
        pla = [(b[0], b[1], b[2], 0.0, 0.0, 0.0, np.array(E_["_2c_platte"](cx=b[1], cy=b[2], ex=H_PLATTE_EX, n=128), dtype=float)) for b in pla]
    q_e, _ = E_["ballen_q"](zeh, X, Y)
    # Auf der Sohlen-Insel keine Hoehen-Strafe (das Netz ist dort grob, 2 cm Raster: die Furchen-Hoehe wuerde die Ballen entlang der
    # Dreiecke abschneiden - gezackte Kanten in v2); ausserhalb der Insel liegen Zehenballen bis ZEH_Z (wickeln vorn etwas hoch)
    if FIX1 and pn[0] == "H":
        # fix1: Zehenballen hinten groesser und an den (kuerzeren, dickeren) Zehen hoeher hinauf (Pruefer Optik M2 "Zehenballen klein")
        q_e = q_e * (H_ZEH_Q if C2C else FIX1_ZEH_Q) + (0.0 if insel else 6.0 * sst(FIX1_ZEH_Z[0], FIX1_ZEH_Z[1], Z))
    else:
        q_e = q_e * SOHLE_Q + (0.0 if insel else 6.0 * sst(ZEH_Z[0], ZEH_Z[1], Z))
    if pn[0] == "H" and FIX1:
        # Nachbesserung 1 (Pruefer Optik M2 "Schild statt ovaler Platte, Ferse ist Fell"): die Platte (fix1-Plan, hinten rund bis
        # x -0,667) gilt an der Ferse in abgerollten Koordinaten x_u = x - FIX1_ROLL * z: unten (z ~ 0) wie bisher, an der Rundung und
        # der Fersen-Hinterkante laeuft das Leder um die Kante hoch (bis ~3,5 cm) und schliesst dort rund - auf und neben der Insel
        # dieselbe Rechnung, also keine Grenze am groben Inselrand.
        hinten = sst(FIX1_ROLL_X + 0.010, FIX1_ROLL_X - 0.010, X)
        xu = X - FIX1_ROLL * np.maximum(Z, 0.0) * hinten
        q_p, _ = E_["ballen_q"](pla, xu, Y)
        q_p = q_p + (1.0 - hinten) * (0.0 if insel else 6.0 * sst(PAD_Z[0], PAD_Z[1], Z))
        if C2C and not insel:
            # 2c: an der kurzen runden Ferse das Leder nur bis H_ROLL_ZMAX hoch, darueber Fell (Fellkranz rundum wie in Kevins Vorlage)
            q_p = q_p + 6.0 * sst(H_ROLL_ZMAX - 0.008, H_ROLL_ZMAX, Z)
    elif pn[0] == "H":
        q_p, _ = E_["ballen_q"](pla, np.maximum(X, FERSE_X), Y)
        fz = sst(FERSE_X + 0.006, FERSE_X - 0.002, X)          # 1 hinter der Fersenkante
        z0 = PAD_Z[0] + (FERSE_Z[0] - PAD_Z[0]) * fz
        z1 = PAD_Z[1] + (FERSE_Z[1] - PAD_Z[1]) * fz
        q_p = q_p + 6.0 * np.clip((Z - z0) / np.maximum(z1 - z0, 1e-6), 0.0, 1.0) ** 2
        if insel:
            q_p = np.where(fz > 0, q_p, E_["ballen_q"](pla, X, Y)[0])
    else:
        q_p, _ = E_["ballen_q"](pla, X, Y)
        q_p = q_p + (0.0 if insel else 6.0 * sst(PAD_Z[0], PAD_Z[1], Z))
    return np.minimum(q_e, q_p), q_p < q_e


def handwurzel_q(pn, Pf, Nn):
    """Vorn: Handwurzelballen (spez/pfoten_plan.json handwurzelballen_x_y_r, angehoben, nicht im Abdruck) als Kappe der Kugel, die aus
    dem Fell ragt: Punkte nahe der Kugelflaeche, deren Normale von der Mitte weg zeigt, untere/hintere Haelfte. q wie bei den Ballen."""
    PL = json.load(open(PLAN_PFOTE))["VL"]
    if FIX1:
        PL = dict(PL)
        PL.update(lade_export_cache()["FIX1_PLAN"]["V"])   # gleiche Lage wie im Hochmodell/Netz (fix1)
    cx, cy, r = PL["handwurzelballen_x_y_r"]
    zu = np.mean(PL["handwurzelballen_z_unten_cm"]) / 100.0
    c = np.array((cx, cy if pn[1] == "L" else -cy, zu + r - 0.0015))     # Mitte ~ 0,0475 wie netz/uebergabe.md
    d_ = Pf - c
    d = np.linalg.norm(d_, axis=1)
    u = d_ / np.maximum(d, 1e-9)[:, None]
    nu = np.einsum("ij,ij->i", Nn, u)
    kappe = sst(0.84, 0.94, nu) * (1.0 - sst(r + 0.0015, r + 0.0050, d)) * (1.0 - sst(0.15, 0.40, u[:, 2]))
    if FIX1:
        # nur die untere Kappe (Pruefer Optik minor 2 "von der Seite wie ein angeklebter Kiesel"): Normale nach unten
        kappe = kappe * sst(-0.25, -0.55, Nn[:, 2])
    return 1.30 - 1.10 * kappe


def leder_farbe(q, platte, X, Y, pid, pn=None):
    """Ballenhaut nach Kevins Fotos (nur angesehen, nichts kopiert): grau-ledern, gewoelbt (Mitte heller, zum Rand dunkler), schmale
    dunkle Randlinie, Furche dunkel; Flecken in zwei Groessen, feine unregelmaessige Lederrisse (Zellen 5-9 mm, schwach), auf
    Platte/Handballen drei, vier leicht wellige Querfalten. Gibt Farbe (n,3) und Anteil Leder (0 = Fell) zurueck.
    v3: weniger Pflaster (Risse 0,14 -> 0,06), Woelbung ueber ~3 cm statt flacher Flaeche, Farbe waermer.
    2c: hinten (pn 'H*') dunkelbraun-ledern nach Kevins Sitzvorlage (H_LEDER_L, H_FARBE), Kuppe deutlich heller als der Rand."""
    hinten = C2C and pn is not None and pn[0] == "H"
    t = np.where(platte > 0.5, np.clip((1.0 - q) / 2.6, 0.0, 1.0), np.clip((1.0 - q) / 0.85, 0.0, 1.0))
    if hinten:
        # Zehenballen (nicht Platte) mit breiterer heller Kuppe (Exponent 0,7): sie heben sich gegen die dunkle Furche ab (Vorlage: pralle,
        # glaenzende Zehenballen); die Platte hat den Glanz nur in der Mitte (H_DOM_EXP)
        L = H_LEDER_L * (H_DOM0 + (1.0 - H_DOM0) * t ** np.where(platte > 0.5, H_DOM_EXP, 0.7))
    else:
        L = LEDER_L * (0.74 + 0.26 * t ** 0.6)
    L = L * (1.0 - 0.16 * np.exp(-((q - 0.97) / 0.07) ** 2))
    d1, d2 = _voronoi(X, Y, 0.0068, pid)
    e1, e2 = _voronoi(X + 0.0031, Y - 0.0017, 0.0093, pid + 7)
    riss = np.maximum(np.exp(-((d2 - d1) / 0.0007) ** 2), 0.7 * np.exp(-((e2 - e1) / 0.0007) ** 2))
    L = L * (1.0 - RISS_K * riss)
    rg = np.random.default_rng(31 + pid)
    n1 = np.zeros(len(X))
    n2 = np.zeros(len(X))
    for _ in range(6):
        w_ = rg.uniform(0, math.pi)
        n1 += np.cos((X * math.cos(w_) + Y * math.sin(w_)) * rg.uniform(35, 70) + rg.uniform(0, 6.3))
        w_ = rg.uniform(0, math.pi)
        n2 += np.cos((X * math.cos(w_) + Y * math.sin(w_)) * rg.uniform(160, 300) + rg.uniform(0, 6.3))
    L = L * (1.0 + 0.022 * n1 + 0.014 * n2)
    if FIX1:
        # grosse Flecken (Pruefer Optik M2 "glatt und einfarbig, wie eine Einlegesohle"): Wellen 3-6 cm, +-FIX1_FLECK
        n3 = np.zeros(len(X))
        for _ in range(5):
            w_ = rg.uniform(0, math.pi)
            n3 += np.cos((X * math.cos(w_) + Y * math.sin(w_)) * rg.uniform(110, 210) + rg.uniform(0, 6.3))
        L = L * (1.0 + FIX1_FLECK * np.tanh(0.6 * n3) + 0.02 * n1)
    falte = np.exp(-((np.sin(X * 150.0 + 6.0 * Y * Y / 0.04 + pid)) / 0.25) ** 2) * platte * sst(0.0, 0.5, t)
    L = L * (1.0 - FALTE_K * falte)
    furche = sst(0.96, 1.05, q) if FIX1 else sst(0.93, 1.06, q)
    if hinten:
        L = L * (1.0 - furche) + H_FURCHE_L * furche
        farbe = L[:, None] * H_FARBE[None, :]
        farbe = farbe * (1.0 - furche[:, None]) + (L[:, None] * H_FURCHE_FARBE[None, :]) * furche[:, None]
        leder = 1.0 - sst(1.15, 1.50, q)
        return farbe, leder
    L = L * (1.0 - furche) + (FURCHE_L * 1.4 if FIX1 else FURCHE_L) * furche
    farbe = L[:, None] * PAD_FARBE[None, :]
    farbe = farbe * (1.0 - furche[:, None]) + (L[:, None] * np.array((1.0, 0.93, 0.86))[None, :]) * furche[:, None]
    leder = 1.0 - sst(1.15, 1.50, q)
    return farbe, leder


def sohlen_malen(col, maske, my, mx, K, plan_json, S_fell, fell_pfote=None, Pf=None, Nn=None, tex_frei=None):
    """Lauf baer-pfoten: (1) Sohlen-Texel (karten sohle_pfote > 0) nach dem neuen Ballen-Plan (Platte/Handballen als Vieleck, fuenf
    Zehenballen): Leder hell, Furche dunkel, dazwischen und am Inselrand Fell (Straehnen in Pfotenfarbe). (2) 3D-Fortsetzung auf die
    Texel ausserhalb der Sohlen-Insel (tex_frei: Rumpf, nicht Sohle): Ballen, die ueber die Insel hinaus reichen (Fersen-Hochzug hinten,
    Ballenkanten), und vorn der Handwurzelballen; dort Leder ueber die gebackene Farbe, Fell bleibt gebacken."""
    pf = K["sohle_pfote"][::-1]                # Kartenzeile 0 = oben -> Rasterzeile 0 = unten
    xyz = K["sohle_xyz"][::-1]
    namen = {1: "VL", 2: "VR", 3: "HL", 4: "HR"}
    inner = abstand_innen(pf > 0, 40)
    for pid, pn in namen.items():
        m = pf == pid
        if not m.any():
            continue
        X, Y, Z = xyz[m, 0].astype(np.float64), xyz[m, 1].astype(np.float64), xyz[m, 2].astype(np.float64)
        pl = pfoten_ballen(pn)
        q, platte = ballen_q3(pl, pn, X, Y, Z, insel=True)
        farbe, leder = leder_farbe(q, platte.astype(np.float64), X, Y, pid, pn)
        # Fell: am Inselrand Straehnen nach innen (Fellkranz), zwischen den Ballen dunkleres Fell
        di = inner[m]
        th = np.arctan2(Y - Y.mean(), X - X.mean())
        nstr = 64.0
        kw = (th + math.pi) / (2.0 * math.pi) * nstr
        kk = np.floor(kw)
        fr = kw - kk
        hk = np.mod(np.sin(kk * 12.9898 + pid * 78.233) * 43758.5453, 1.0)
        lang = 4.0 + 7.0 * hk                  # v4: Fellkranz-Straehnen kuerzer (v2: 6-18 Texel = 1,2-3,6 cm)
        quer = np.exp(-((fr - 0.5) / (0.30 + 0.12 * hk)) ** 2)
        strahl = (1.0 - sst(0.55 * lang, lang, di)) * quer
        rand = np.maximum(1.0 - sst(2.0, 5.0, di), strahl) * sst(0.90, 1.12, q)
        if C2C and pn[0] == "H":
            # 2c (SPEZ 4: Fellkranz 1,5-2,5 cm, ueberdeckt den Sohlenrand 0,5-1,0 cm -> Umriss rund/oval): breiterer Kranz, laengere
            # Straehnen, am Inselrand auch ueber dem Leder (nicht an der Ferse, dort laeuft das Leder um die Kante)
            lang_h = H_KRANZ_LANG[0] + H_KRANZ_LANG[1] * hk
            strahl_h = (1.0 - sst(0.55 * lang_h, lang_h, di)) * quer
            pflicht = (1.0 - sst(H_KRANZ[0], H_KRANZ[1], di)) * sst(H_FERSE_FREI - 0.012, H_FERSE_FREI + 0.004, X)
            rand = np.maximum(np.maximum(1.0 - sst(H_KRANZ[0], H_KRANZ[1], di), strahl_h) * sst(0.80, 1.05, q), pflicht)
        fell = np.maximum(1.0 - leder, rand)
        if fell_pfote is not None and pid in fell_pfote:
            fp = fell_pfote[pid][None, :]
        else:
            fp = np.median(S_fell[m], 0)[None, :]
        # v4: Fell auf der Insel als kurze Straehnen (fell_2d) statt Sinus-Wellen; zum Ballen hin dunkler (Schatten zwischen den Ballen)
        st2 = fell_2d(X, Y, X.mean(), Y.mean(), saat=pid)
        schatten = (0.84 + 0.12 * sst(1.2, 2.2, q)) if FIX1 else (0.70 + 0.22 * sst(1.2, 2.2, q))
        S_rand = fp * (schatten * (0.86 + 0.30 * st2))[:, None]
        # v5: am Inselrand weich in die gebackene Farbe (dort Fell des Hochmodells, so passt der Rand zur Seitenwand)
        w_b = (1.0 - sst(3.0, 10.0, di))[:, None]
        # v13: die gebackene Farbe am Inselrand ist hell (Ansichten sehen dort die helle Sohle des Hochmodells) -> heller Strich um die
        # Sohle/Ferse; Helligkeit hier hoechstens Pfotenfell x RAND_K (Farbton und dunklere Straehnen bleiben)
        Sb = S_fell[m].astype(np.float64)
        lw_ = np.array((0.2126, 0.7152, 0.0722))
        Sb = Sb * np.minimum(1.0, float(fp[0] @ lw_) * RAND_K / np.maximum(Sb @ lw_, 1e-4))[:, None]
        S_rand = S_rand * (1.0 - w_b) + Sb * w_b
        out = farbe * (1.0 - fell[:, None]) + S_rand * fell[:, None]
        col[m] = out.astype(np.float32)
        if C2C:
            ys_m, xs_m = np.nonzero(m)
            SOHLE_MESS[pn] = dict(y=ys_m.astype(np.int16), x=xs_m.astype(np.int16), q=q.astype(np.float32), leder=leder.astype(np.float32),
                                  fell=fell.astype(np.float32))
        Lp = farbe @ np.array((0.2126, 0.7152, 0.0722))
        log("SOHLE %s: Texel %d, Leder %d, Ballen-Luma Median %.0f, Furchen-Luma Median %.0f, Fell %d (sRGB 0-255)" % (
            pn, int(m.sum()), int((leder > 0.5).sum()), np.median(Lp[q < 0.6]) * 255 if (q < 0.6).any() else -1,
            np.median(Lp[(q > 1.0) & (q < 1.12)]) * 255 if ((q > 1.0) & (q < 1.12)).any() else -1, int((fell > 0.5).sum())))
    if Pf is not None:
        # (2) 3D-Fortsetzung ausserhalb der Insel
        for pid, pn in namen.items():
            vorn = pn[0] == "V"
            sy = 1.0 if pn[1] == "L" else -1.0
            sel = tex_frei & ((Pf[:, 0] > 0.0) == vorn) & (Pf[:, 1] * sy > 0.0) & (Pf[:, 2] < (0.09 if vorn else (0.05 if FIX1 else 0.03)))
            sel &= (Pf[:, 0] > 0.15) if vorn else (Pf[:, 0] < -0.10)
            if not sel.any():
                continue
            ix = np.nonzero(sel)[0]
            X, Y, Z = Pf[ix, 0], Pf[ix, 1], Pf[ix, 2]
            pl = pfoten_ballen(pn)
            q, platte = ballen_q3(pl, pn, X, Y, Z)
            unten = sst(-0.15, -0.45, Nn[ix, 2])
            if FIX1 and not vorn:
                # Zehen hinten: auch die schraeg nach vorn/unten gewandte Zehenkuppe (dort sitzt der Zehenballen)
                unten = np.maximum(unten, sst(-0.0, -0.30, Nn[ix, 2]) * sst(-0.30, -0.26, X))
            if not vorn:
                # v6: an der Ferse (hinter FERSE_X) entscheidet nur die Hoehe (wie auf der Insel), sonst gezackter Inselrand (v5)
                unten = np.maximum(unten, sst(FERSE_X + 0.006, FERSE_X - 0.002, X))
            q = np.where(unten > 0, q, 9.0)
            w_unten = unten
            n_hw = 0
            if vorn:
                q_hw = handwurzel_q(pn, Pf[ix], Nn[ix])
                n_hw = int((q_hw < 1.0).sum())
                platte = np.where(q_hw < q, True, platte)
                w_unten = np.where(q_hw < q, 1.0, unten)
                q = np.minimum(q, q_hw)
            farbe, leder = leder_farbe(q, platte.astype(np.float64), X, Y, pid, pn)
            if vorn and FIX1:
                farbe = np.where((q_hw <= q + 1e-9)[:, None], farbe * FIX1_HW_DUNKEL, farbe)
            w = (1.0 - sst(1.0, 1.25, q)) * w_unten      # nur Leder und Furche, Fell bleibt gebacken
            yy, xx = my[ix], mx[ix]
            alt_ = col[yy, xx].astype(np.float64)
            col[yy, xx] = (alt_ * (1.0 - w[:, None]) + farbe * w[:, None]).astype(np.float32)
            log("PFOTE %s 3D-Fortsetzung: Texel %d, davon Leder (q < 1) %d, Handwurzelballen %d" % (pn, len(ix), int((q < 1.0).sum()), n_hw))
    return pf > 0


def feld_zurueck(E, V, pfad, k=8):
    """2c: Spielnetz-Punkte (Hochmodell-Masse) an die Lage VOR form_2c zurueckschieben. Feld = dichte Huelle S0 (vorher) und S (nachher,
    Spielmeter, baer_export_2c.py:1996); je Punkt die Verschiebung S0 - S der k naechsten Huellenpunkte (Gewicht 1/d^2). Kopf (ab der
    Schutzzone) und Pfoten unter z 0,115 hat form_2c nicht bewegt -> dort 0. Gibt V0 (Hochmodell-Masse) und Kennzahlen zurueck."""
    from mathutils.kdtree import KDTree
    F = np.load(pfad)
    S0, S = F["S0"].astype(np.float64), F["S"].astype(np.float64)
    D = S0 - S
    kd = KDTree(len(S))
    for i, p in enumerate(S):
        kd.insert(p, i)
    kd.balance()
    VF = E["h2f"](V)
    off = np.zeros_like(VF)
    dmin = np.zeros(len(VF))
    for i, p in enumerate(VF):
        r = kd.find_n(p, k)
        idx = np.array([x[1] for x in r])
        d = np.array([x[2] for x in r])
        w = 1.0 / (d * d + 1e-8)
        off[i] = (D[idx] * w[:, None]).sum(0) / w.sum()
        dmin[i] = d.min()
    kz = dict(verschiebung_cm_p50=float(np.median(np.linalg.norm(off, axis=1)) * 100),
              verschiebung_cm_p95=float(np.percentile(np.linalg.norm(off, axis=1), 95) * 100),
              verschiebung_cm_max=float(np.linalg.norm(off, axis=1).max() * 100),
              abstand_huelle_mm_p50=float(np.median(dmin) * 1000), abstand_huelle_mm_p95=float(np.percentile(dmin, 95) * 1000))
    return E["f2h"](VF + off), kz


def abstand_kopf(V, kopf_v, block=4000):
    """2c: je Punkt der 3D-Abstand (Spielmeter-Eingabe) zum naechsten Kopfpunkt (wie spez/werkzeug/mess_texel_naht.py)."""
    from mathutils.kdtree import KDTree
    K = V[kopf_v]
    kd = KDTree(len(K))
    for i, p in enumerate(K):
        kd.insert(p, i)
    kd.balance()
    return np.array([kd.find(p)[2] for p in V])


_E_CACHE = {}
SOHLE_MESS = {}     # 2c: Sohlen-Texel je Pfote (Raster-Zeile 0 = unten) mit q, Leder- und Fell-Anteil fuer die Messung


def lade_export_cache():
    if "E" not in _E_CACHE:
        _E_CACHE["E"] = lade_export()
    return _E_CACHE["E"]


def stufe_backen():
    E = lade_export_cache()
    Q = E["quelle"]("form")
    TEX = E["TEX"]
    mit_pose = (not NUR_NEU) and POSE_W > 0 and os.path.exists(ANS_POSE + "kameras.json")
    PM = pose_matrizen() if mit_pose else None          # vor open_mainfile: braucht Skelett und Haut des Hochmodells
    bpy.ops.wm.open_mainfile(filepath=NETZ + "lowpoly_%s.blend" % NETZ_NAME)
    ob = bpy.data.objects["NCBear"]
    me = ob.data
    VF, T = E["netz_arrays"](me)
    V = E["f2h"](VF)
    m_ = len(T)
    LT = np.empty(m_ * 3, dtype=np.int64)
    me.loop_triangles.foreach_get("loops", LT)
    LT = LT.reshape(m_, 3)
    PT = np.empty(m_, dtype=np.int64)
    me.loop_triangles.foreach_get("polygon_index", PT)
    gp = np.empty(len(me.polygons), dtype=np.int32)
    me.attributes["gegend"].data.foreach_get("value", gp)
    gegend = gp[PT]
    sp_ = np.empty(len(me.polygons), dtype=np.int32)
    me.attributes["sohle"].data.foreach_get("value", sp_)
    sohle_t = sp_[PT]
    uv = np.empty(len(me.loops) * 2, dtype=np.float64)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    Ed = E["kanten"](T)
    Vg = E["glatt_feld"](V, Ed, len(V), 8, 0.6)
    N = E["v_normalen"](Vg, T)
    if FELD:
        # 2c: Lage vor form_2c (dort passt das Hochmodell der Ansichten); nur fuer Projektion, Sichtbarkeit und Back-Pose
        V0, kz_feld = feld_zurueck(E, V, FELD)
        N0 = E["v_normalen"](E["glatt_feld"](V0, Ed, len(V), 8, 0.6), T)
        log("2C Projektion am Netz vor form_2c: Verschiebung cm p50 %.2f / p95 %.2f / max %.2f, Abstand zur Huelle mm p50 %.2f / p95 %.2f" % (
            kz_feld["verschiebung_cm_p50"], kz_feld["verschiebung_cm_p95"], kz_feld["verschiebung_cm_max"], kz_feld["abstand_huelle_mm_p50"],
            kz_feld["abstand_huelle_mm_p95"]))
    else:
        V0, N0, kz_feld = V, N, {}
    pos, nrm, tri = E["raster_uv"](uv[LT], T, V, N, TEX)
    maske = tri >= 0
    my, mx = np.nonzero(maske)
    tt = tri[maske]
    P = pos[maske].astype(np.float64)
    Nn = nrm[maske].astype(np.float64)
    Nn /= np.maximum(np.linalg.norm(Nn, axis=1, keepdims=True), 1e-9)
    n_t = len(P)
    log("UV gerastert, Texel", n_t)
    K = np.load(KARTEN)
    region = K["region"][::-1][maske]
    rumpf_t = gegend[tt] == 0
    L_ = Q["w2l"](P)
    hb = Q["huelle_basis"](L_[:, 0], L_[:, 1], L_[:, 2])
    kopf_maske = 1.0 - sst(0.02, 0.20, hb)
    global PF_SPIEL
    PF_SPIEL = E["h2f"](P)
    h_dir, bein = haarrichtung(Q, P, Nn)
    # ---------------------------------------------------------- Ansichten sammeln
    if NUR_NEU:
        views = [dict(v, pfad=ANS_ALT + v["name"] + ".exr") for v in json.load(open(ANS_ALT + "kameras.json"))]
    else:
        views = [dict(v, pfad=ANS_NEU + v["name"] + ".exr") for v in json.load(open(ANS_NEU + "kameras.json"))]
        views += [dict(v, pfad=ANS_ALT + v["name"] + ".exr") for v in json.load(open(ANS_ALT + "kameras.json")) if v["name"].startswith("h_")]
        if mit_pose:
            views += [dict(v, pfad=ANS_POSE + v["name"] + ".exr", pose=True) for v in json.load(open(ANS_POSE + "kameras.json"))]
    innenbein = np.isin(region, INNENBEIN)
    # Baryzentrische Lage je Texel (fuer glatte Felder ueber das Netz: Regionen, Verdeckung, Naht-Farbabgleich)
    A0, A1, A2 = V[T[tt, 0]], V[T[tt, 1]], V[T[tt, 2]]
    v0, v1, v2 = A1 - A0, A2 - A0, P - A0
    d00, d01, d11 = (v0 * v0).sum(1), (v0 * v1).sum(1), (v1 * v1).sum(1)
    d20, d21 = (v2 * v0).sum(1), (v2 * v1).sum(1)
    den = np.maximum(d00 * d11 - d01 * d01, 1e-18)
    bv = np.clip((d11 * d20 - d01 * d21) / den, 0, 1)
    bw = np.clip((d00 * d21 - d01 * d20) / den, 0, 1)
    bu = np.clip(1.0 - bv - bw, 0, 1)
    bs = np.maximum(bu + bv + bw, 1e-9)
    BARY = np.stack((bu / bs, bv / bs, bw / bs), 1)
    del A0, A1, A2, v0, v1, v2, d00, d01, d11, d20, d21, den, bv, bw, bu, bs

    def feld_texel(werte_p):
        """Punktfeld (n,) oder (n,k) -> je Texel baryzentrisch."""
        w = werte_p[T[tt]]
        if w.ndim == 2:
            return (w * BARY).sum(1)
        return (w * BARY[:, :, None]).sum(1)

    def feld_glatt(werte_texel, runden, nur=None):
        """Texelwerte -> Mittel je Dreieck -> je Punkt -> ueber Kanten geglaettet -> je Texel (stetig ueber UV-Naehte)."""
        wt = np.ones(n_t) if nur is None else nur.astype(np.float64)
        x = werte_texel if werte_texel.ndim == 2 else werte_texel[:, None]
        cnt = np.bincount(tt, weights=wt, minlength=len(T))
        tri_m = np.stack([np.bincount(tt, weights=wt * x[:, k], minlength=len(T)) for k in range(x.shape[1])], 1)
        vc = np.zeros(len(V))
        vs = np.zeros((len(V), x.shape[1]))
        for j in range(3):
            vc += np.bincount(T[:, j], weights=cnt, minlength=len(V))
            for k in range(x.shape[1]):
                vs[:, k] += np.bincount(T[:, j], weights=tri_m[:, k], minlength=len(V))
        vp = vs / np.maximum(vc, 1e-9)[:, None]
        hat = vc > 1e-9
        # leere Punkte aus den Nachbarn fuellen, dann glaetten
        for _ in range(80):
            if hat.all():
                break
            nb = np.zeros_like(vp)
            nc = np.zeros(len(V))
            for e0, e1 in ((Ed[:, 0], Ed[:, 1]), (Ed[:, 1], Ed[:, 0])):
                h_ = hat[e1]
                for k in range(vp.shape[1]):
                    nb[:, k] += np.bincount(e0[h_], weights=vp[e1[h_], k], minlength=len(V))
                nc += np.bincount(e0[h_], minlength=len(V))
            neu_ = (~hat) & (nc > 0)
            if not neu_.any():
                break
            vp[neu_] = nb[neu_] / nc[neu_][:, None]
            hat = hat | neu_
        if runden:
            vp = E["glatt_feld"](vp, Ed, len(V), runden, 0.5)
        out = feld_texel(vp)
        return out if werte_texel.ndim == 2 else out[:, 0]

    if FELD:
        P0 = (V0[T[tt]] * BARY[:, :, None]).sum(1)
        Nn0 = (N0[T[tt]] * BARY[:, :, None]).sum(1)
        Nn0 /= np.maximum(np.linalg.norm(Nn0, axis=1, keepdims=True), 1e-9)
        # Haarrichtung des Hochmodells an der alten Lage (fuer den Ausgleich der Blickrichtung); die Buesche nehmen die neue (h_dir)
        PF_SPIEL = E["h2f"](P0)
        h_dir0, bein0 = haarrichtung(Q, P0, Nn0)
        PF_SPIEL = E["h2f"](P)
    else:
        P0, Nn0, h_dir0, bein0 = P, Nn, h_dir, bein
    if C2C:
        # 2c: Abstand je Texel zum naechsten Kopfpunkt (Spielmeter, Ruhe; wie spez/werkzeug/mess_texel_naht.py)
        kopf_vm = np.zeros(len(V), dtype=bool)
        kopf_vm[np.unique(T[gegend == 1].ravel())] = True
        dk = feld_texel(abstand_kopf(E["h2f"](V), kopf_vm))
        log("2C Abstand zum Kopf: Texel unter 12 / 35 / 60 cm: %d / %d / %d" % (int((dk < 0.12).sum()), int((dk < 0.35).sum()), int((dk < 0.60).sum())))
    else:
        dk = np.full(n_t, 9.0)
    if NUR_TEXEL:
        os.makedirs(TX + "mess", exist_ok=True)
        np.savez_compressed(TX + "mess/texel_%s.npz" % AUSNAME, my=my.astype(np.int16), mx=mx.astype(np.int16), gegend=gegend[tt].astype(np.int8),
                            sohle=sohle_t[tt].astype(np.int8), P=E["h2f"](P).astype(np.float32), P0=E["h2f"](P0).astype(np.float32))
        log("NUR_TEXEL", TX + "mess/texel_%s.npz" % AUSNAME, "Texel", n_t, "Abstand P0-P cm p95 %.2f" % (
            np.percentile(np.linalg.norm(E["h2f"](P0) - E["h2f"](P), axis=1), 95) * 100))
        log("BACKEN_OK")
        return
    # Back-Pose: Spielnetz mit den Hautgewichten des Hochmodells in dieselbe Pose (Beine gespreizt), Texel, Normalen, Haarrichtung
    if mit_pose:
        V_p, M3 = pose_netz(PM, V0)     # 2c: Lage vor form_2c (= Hochmodell)
        Np_v = E["v_normalen"](E["glatt_feld"](V_p, Ed, len(V), 8, 0.6), T)
        P_p = feld_texel(V_p)
        Nn_p = feld_texel(Np_v)
        Nn_p /= np.maximum(np.linalg.norm(Nn_p, axis=1, keepdims=True), 1e-9)
        h_p = np.zeros_like(h_dir)
        for i_ in range(3):
            h_p += BARY[:, i_:i_ + 1] * np.einsum("nij,nj->ni", M3[T[tt, i_]], h_dir0)
        h_p /= np.maximum(np.linalg.norm(h_p, axis=1, keepdims=True), 1e-9)
        # nur fuer die Unterseite: Achsel, Leiste, Innenbeine, Bauch, Normale nach unten; nicht Kopf, nicht Sohle
        pose_ok = rumpf_t & (sohle_t[tt] == 0) & (np.isin(region, (4, 5, 6, 7, 9)) | (Nn[:, 2] < -0.3)) & (kopf_maske < 0.05)
        log("Back-Pose: Punkte bewegt im Mittel %.1f cm, max %.1f cm (Hochmodell); Texel fuer Pose-Ansichten %d" % (
            np.linalg.norm(V_p - V, axis=1).mean() * 100, np.linalg.norm(V_p - V, axis=1).max() * 100, int(pose_ok.sum())))
    # Nachbesserung 09.11.: weiche Gewichte statt harter Grenzen je Dreieck (die Region der Karte gilt je Dreieck; harte Schalter gaben
    # scharfkantige helle Flecken, Pruefer Optik minor 4)
    if NUR_NEU:
        inn_w = innenbein.astype(np.float64)
    else:
        inn_w = np.clip(feld_glatt(innenbein.astype(np.float64), 8, nur=rumpf_t), 0.0, 1.0) * rumpf_t
        if mit_pose:
            reg_p = np.clip(feld_glatt(np.isin(region, (4, 5, 6, 7, 9)).astype(np.float64), 8, nur=rumpf_t), 0.0, 1.0)
            pose_w = (np.maximum(reg_p, sst(-0.15, -0.45, Nn[:, 2])) * rumpf_t * (sohle_t[tt] == 0)
                      * (1.0 - sst(0.0, 0.05, kopf_maske)))
            pose_ok = pose_w > 0.02
    S_idx, S_c, S_b, S_cs, S_v = [], [], [], [], []
    t0 = time.time()
    for vi, v in enumerate(views):
        av = E["Ansicht"](v)
        kopf = av.name.startswith("h_")
        ist_p = bool(v.get("pose"))
        Vv, Pv, Nv = (V_p, P_p, Nn_p) if ist_p else (V0, P0, Nn0)   # 2c: V0 = V ohne Feld
        Z = E["minfilter"](E["zbuffer"](av, Vv, T, 1024))
        rgba = E["lade_exr"](v["pfad"])
        u, vv, dep = av.pix(Pv)
        k = 1024.0 / av.res
        iu = np.clip(np.floor(u * k).astype(np.int64), 0, 1023)
        iv = np.clip(np.floor(vv * k).astype(np.int64), 0, 1023)
        tol = np.full(n_t, 0.014 if kopf else 0.030)
        waag = (not NUR_NEU) and av.name.startswith("k_h")
        if waag:
            tol = tol - (0.030 - INNEN_TOL) * inn_w   # W5: waagerechte Ansichten sehen an den Innenbeinen durch die Bauchluecke (weich)
        sicht = dep <= Z[iv, iu] + tol
        cs = np.clip(Nv @ av.d, 0.0, 1.0)
        ok = sicht & (cs >= 0.2)
        if ist_p:
            ok &= pose_ok
        if kopf:
            ok &= kopf_maske > 1e-4
            if not NUR_NEU:
                ok &= ~rumpf_t    # alte Kopfansichten (alter Shader) nur noch fuer Kopf-Texel; den Hals macht die Naht-Mischung
        idx = np.nonzero(ok)[0]
        col, inn = E["bilinear"](rgba, u[idx], vv[idx])
        al = col[:, 3]
        base = inn * (al > 0.45) * al * al
        if kopf:
            base = base * kopf_maske[idx] * 7.0
        if waag:
            base = base * (1.0 - (1.0 - INNEN_W) * inn_w[idx])
        if ist_p:
            base = base * POSE_W * pose_w[idx]
        g = base > 1e-6
        idx = idx[g]
        S_idx.append(idx.astype(np.int32))
        S_c.append((col[g, :3] / np.maximum(al[g], 1e-3)[:, None]).astype(np.float32))
        S_b.append(base[g].astype(np.float32))
        S_cs.append(cs[idx].astype(np.float32))
        S_v.append(np.full(len(idx), vi, dtype=np.int16))
        del rgba
    log("Ansichten gesammelt: %d, Proben %d, %.1fs" % (len(views), sum(len(a) for a in S_idx), time.time() - t0))
    I_ = np.concatenate(S_idx)
    C_ = np.concatenate(S_c)
    B_ = np.concatenate(S_b)
    CS = np.concatenate(S_cs)
    VI = np.concatenate(S_v)
    del S_idx, S_c, S_b, S_cs, S_v
    D_ = np.array([v["d"] for v in views])[VI]
    ist_kopfsicht = np.array([v["name"].startswith("h_") for v in views])[VI]
    G = B_ * CS ** P_EXP
    lum = C_ @ np.array((0.2126, 0.7152, 0.0722), dtype=np.float32)
    a_ = np.einsum("ij,ij->i", D_, h_dir0[I_]).astype(np.float32)
    ist_pose = np.array([bool(v.get("pose")) for v in views])[VI]
    if ist_pose.any():
        a_[ist_pose] = np.einsum("ij,ij->i", D_[ist_pose], h_p[I_[ist_pose]]).astype(np.float32)
        log("Back-Pose: Proben %d (%.1f %% des Gewichts an den Pose-Texeln)" % (int(ist_pose.sum()), 100.0 * float(
            (B_ * CS ** P_EXP)[ist_pose].sum() / max((B_ * CS ** P_EXP)[pose_ok[I_]].sum(), 1e-9))))
    # ---------------------------------------------------------- Ausgleich Blickrichtung zum Haar (nur neue Koerperansichten)
    gain = np.ones(len(I_), dtype=np.float32)
    fit = {}
    if not NUR_NEU:
        X = merkmale(a_, D_[:, 2].astype(np.float32), CS, bein0[I_].astype(np.float32))
        sel = (~ist_kopfsicht) & rumpf_t[I_] & (kopf_maske[I_] < 0.05) & (sohle_t[tt[I_]] == 0) & (lum > 2e-4) & (G > 1e-3)
        sel &= (I_ % 3) == 0
        Xs, ys, ws, ts = X[sel].astype(np.float64), np.log(lum[sel]).astype(np.float64), G[sel].astype(np.float64), I_[sel]
        uniq, ti = np.unique(ts, return_inverse=True)
        sw = np.bincount(ti, weights=ws)
        alpha = np.bincount(ti, weights=ws * ys) / np.maximum(sw, 1e-12)
        beta = np.zeros(X.shape[1])
        for it in range(12):
            r = ys - alpha[ti]
            A = (Xs * ws[:, None]).T @ Xs + np.eye(X.shape[1]) * 1e-3 * ws.sum()
            beta = np.linalg.solve(A, (Xs * ws[:, None]).T @ r)
            alpha = np.bincount(ti, weights=ws * (ys - Xs @ beta)) / np.maximum(sw, 1e-12)
        res0 = ys - np.bincount(ti, weights=ws * ys)[ti] / sw[ti]
        res1 = ys - alpha[ti] - Xs @ beta
        fit = dict(beta=beta.round(4).tolist(), proben=int(len(ys)), texel=int(len(uniq)),
                   streu_vorher=float(np.sqrt((ws * res0 ** 2).sum() / ws.sum())), streu_nachher=float(np.sqrt((ws * res1 ** 2).sum() / ws.sum())))
        log("AUSGLEICH beta [a, a2, dz, cos, a*bein, dz*bein] =", fit["beta"], "log-Streuung %.3f -> %.3f" % (fit["streu_vorher"], fit["streu_nachher"]))
        Xr = merkmale(np.full(len(I_), A_REF, np.float32), np.zeros(len(I_), np.float32), np.ones(len(I_), np.float32), bein0[I_].astype(np.float32))
        gain = np.exp(np.clip((Xr - X) @ beta.astype(np.float32), math.log(0.33), math.log(3.0))).astype(np.float32)
        gain[ist_kopfsicht] = 1.0
        # Ansichten bevorzugen, die das Haar von der Seite sehen (gegen die Haarspitzen = dunkle Luecken zwischen den Bueschen)
        G = G * np.where(ist_kopfsicht, 1.0, np.exp(-K_SEITE * np.maximum(a_ - 0.55, 0.0))).astype(np.float32)

    def mischen(fak_neu):
        f = np.where(ist_kopfsicht[:, None], 1.0, fak_neu[None, :]).astype(np.float32) * gain[:, None]
        cc = C_ * f
        sw = np.bincount(I_, weights=G, minlength=n_t)
        lin = np.stack([np.bincount(I_, weights=G * cc[:, k], minlength=n_t) for k in range(3)], 1) / np.maximum(sw, 1e-12)[:, None]
        lu = cc @ np.array((0.2126, 0.7152, 0.0722), dtype=np.float32)
        m1 = np.bincount(I_, weights=G * lu, minlength=n_t) / np.maximum(sw, 1e-12)
        m2 = np.bincount(I_, weights=G * lu * lu, minlength=n_t) / np.maximum(sw, 1e-12)
        streu = np.sqrt(np.maximum(m2 - m1 * m1, 0.0)) / np.maximum(m1, 1e-5)
        return lin, sw > 1e-5, m1, streu

    HELL, GAMMA = E["HELL"], E["GAMMA"]
    fak = np.ones(3, dtype=np.float32)
    zw = png_laden(ZWISCHEN_PNG)[my, mx]
    ref = (region == 11) & (P[:, 2] > 0.75) & (kopf_maske < 0.02)
    if not NUR_NEU:
        # Belichtung/Farbe der neuen Ansichten an das alte Fell anpassen (Ruecken/Flanke oben, ohne Nacharbeit-Zonen)
        lin0, ges0, _, _ = mischen(fak)
        lin_zw = srgb_inv(np.power(np.clip(zw / HELL, 0, 1), 1.0 / GAMMA))
        fak = (np.median(lin_zw[ref], 0) / np.maximum(np.median(lin0[ref], 0), 1e-6)).astype(np.float32)
        log("Farbabgleich an das alte Fell (linear, je Kanal):", fak.round(3), "Texel", int(ref.sum()))
    lin, gesehen, lum_t, streu_t = mischen(fak)
    gut = np.bincount(I_[(CS >= 0.8) & (G > 1e-6)], minlength=n_t) > 0     # bester Blickwinkel < 37 Grad
    sw_ = np.bincount(I_, weights=G, minlength=n_t)
    a_eff = np.bincount(I_, weights=G * a_, minlength=n_t) / np.maximum(sw_, 1e-12)
    log("Projektion fertig, gesehen %.4f der Texel" % gesehen.mean())
    S = E["srgb"](lin)
    S = np.power(np.clip(S, 0.0, 1.0), GAMMA) * HELL
    # ---------------------------------------------------------- Nacharbeit Rumpf
    kopfm = 1.0 - sst(0.0, 0.14, hb)
    ring = sst(0.15, -0.05, L_[:, 0]) * (1.0 - sst(0.015, 0.11, hb))
    kontrast = np.zeros(n_t)
    if NUR_NEU:
        kralle = (gegend == 2)[tt].astype(np.float64)
        S = E["gesicht_nacharbeit"](Q, S, P, kralle)
    else:
        # Nachbesserung 09.11.: Gesprenkel (helle Haarschlaufen aus Ansichten gegen die Haarspitzen, 'Frottee') an Beinen, Hinterteil und
        # gegen die Haarspitzen gesehenen Flaechen VOR der Nacharbeit inselweise glaetten; die gemalten Buesche kommen danach
        hint_w = np.clip(feld_glatt((region == 10).astype(np.float64), 8, nur=rumpf_t), 0.0, 1.0)
        # (Pfoten unten um die Sohle: voll glaetten, dort war der Fellkranz ein gepunkteter Ring)
        ruhig = (np.maximum(np.maximum(sst(0.62, 0.86, a_eff), 0.85 * np.maximum(bein, hint_w)), 1.0 - sst(0.04, 0.12, P[:, 2]))
                 * rumpf_t * (sohle_t[tt] == 0) * (1.0 - kopfm))
        if RUHIG_K > 0:
            t1 = time.time()
            img = np.zeros((TEX, TEX, 3), dtype=np.float32)
            img[my, mx] = S
            bl = glaetten_insel(img, pos, maske, 18, 0.012)[my, mx].astype(np.float64)
            del img
            k_r = (RUHIG_K * ruhig)[:, None]
            S = S * (1.0 - k_r) + bl * k_r
            del bl
            log("NACHBESSERUNG Gesprenkel geglaettet: Texel mit Anteil > 0,5: %.3f, %.1fs" % (float((RUHIG_K * ruhig > 0.5).mean()), time.time() - t1))
        # Hals wie gesicht_nacharbeit (baer_export_fell.py:422-430), damit die Naht zum alten Kopf passt
        S = S * (1.0 - 0.10 * kopfm[:, None])
        S = S * (1.0 + (0.20 * ring)[:, None] * np.array((1.12, 1.0, 0.82)))
        weg_kopf = 1.0 - kopfm
        rumpf_f = rumpf_t.astype(np.float64)
        # Unterseite: Normale nach unten, dazu Achsel/Leiste/Innenbeine/Bauch (Regionen des Netzes, ueber das Netz geglaettet)
        reg_u = feld_glatt(np.isin(region, (4, 5, 6, 7, 9)).astype(np.float64), 12, nur=rumpf_t)
        unten = np.maximum(sst(-0.10, -0.70, Nn[:, 2]), reg_u * 0.8)
        # Unterbeine (wie baer-anim x1,30/x1,42, jetzt sanfter, weil das Fell dort schon heller gerendert ist)
        tief = 1.0 - sst(0.04, 0.45, P[:, 2])
        S = S * (1.0 + (UNTEN_LIFT * unten + BEIN_LIFT * tief) * weg_kopf)[:, None]
        # Nachbesserung 09.11.: weiche Felder Leiste/Innenbein hinten (k57) und uebrige Unterseite (kU) fuer Deckel und Farbton
        k57 = np.clip(feld_glatt(np.isin(region, (5, 7)).astype(np.float64), 10, nur=rumpf_t), 0.0, 1.0) * weg_kopf * rumpf_f
        kU = np.clip(feld_glatt(np.isin(region, (3, 4, 6, 8, 9)).astype(np.float64), 10, nur=rumpf_t), 0.0, 1.0) * weg_kopf * rumpf_f
        # Haarbuesche laengs der Haarrichtung: Wurzel dunkel, Spitze heller. Nachbesserung 09.11.: einzelne Buesche um zufaellige 3D-Punkte
        # (buesche_3d; vorher ein Gitter in projizierten Koordinaten -> Ringe um den Schwanzansatz), ~1,3 cm breit und ~8 cm lang (Spielmass),
        # also 3-6 Texel breit in der 1024er; Richtung stabil (haar_tangente, ueber das Netz geglaettet); ueberall etwa gleich stark statt an
        # Unterseite/Hinterteil staerker; keine hellen Spitzen an Unterseite/Leiste
        h_t = haar_tangente(h_dir, Nn)
        h_t = feld_glatt(h_t, 4)
        h_t = h_t - np.einsum("ij,ij->i", h_t, Nn)[:, None] * Nn
        h_t /= np.maximum(np.linalg.norm(h_t, axis=1, keepdims=True), 1e-9)
        w_beh = np.zeros(n_t)
        w_schatten = np.zeros(n_t)
        if C2C:
            # 2c (SPEZ 2.5): Fellbehang. Masken wie form_2c (f) (baer_export_2c.py:1858-1866, Spielmeter, am neuen Netz): Ellbogenbehang
            # hinter dem Unterarm z 0,36-0,54, Bauchkante seitlich x -0,24..0,07. Dort haengen die Straehnen (Haarrichtung abwaerts in der
            # Flaeche, laengere Buesche, mehr Hub); darunter ein Schattenband (Unterarm hinten z 0,26-0,38, Bauch innen der Kante).
            xs_, ys_, zs_ = PF_SPIEL[:, 0], np.abs(PF_SPIEL[:, 1]), PF_SPIEL[:, 2]
            hk_ = np.interp(zs_, E["_2C_ZT"], np.array(E["_2C_BEIN"]["V"]["xr_s"], dtype=np.float64))
            hinter_ = sst(-0.15, -0.55, Nn[:, 0]) * (1.0 - sst(0.04, 0.10, np.abs(xs_ - hk_ + 0.01))) * np.exp(-((ys_ - 0.255) / 0.07) ** 2)
            ell_ = sst(0.34, 0.41, zs_) * (1.0 - sst(0.50, 0.56, zs_)) * hinter_
            fen_ = sst(-0.26, -0.15, xs_) * (1.0 - sst(-0.01, 0.09, xs_))
            bauch_ = fen_ * np.exp(-((ys_ - 0.255) / 0.065) ** 2) * sst(-0.2, -0.6, Nn[:, 2]) * sst(0.29, 0.35, zs_) * (1.0 - sst(0.52, 0.58, zs_))
            frei_ = rumpf_f * (sohle_t[tt] == 0) * weg_kopf
            w_beh = np.clip(feld_glatt(np.clip(np.maximum(ell_, bauch_), 0.0, 1.0) * frei_, 3, nur=rumpf_t), 0.0, 1.0) * frei_
            sch_e = sst(0.26, 0.30, zs_) * (1.0 - sst(0.34, 0.38, zs_)) * hinter_
            sch_b = fen_ * np.exp(-((ys_ - 0.19) / 0.035) ** 2) * sst(-0.55, -0.85, Nn[:, 2]) * sst(0.28, 0.33, zs_) * (1.0 - sst(0.50, 0.56, zs_))
            w_schatten = np.clip(feld_glatt(np.clip(np.maximum(sch_e, sch_b), 0.0, 1.0) * frei_, 3, nur=rumpf_t), 0.0, 1.0) * frei_
            ab_ = np.array((0.0, 0.0, -1.0))[None, :] - Nn[:, 2:3] * Nn
            lab_ = np.linalg.norm(ab_, axis=1)
            wh_ = (w_beh * sst(0.2, 0.5, lab_))[:, None]
            h_t = h_t * (1.0 - wh_) + ab_ / np.maximum(lab_, 1e-9)[:, None] * wh_
            h_t = h_t - np.einsum("ij,ij->i", h_t, Nn)[:, None] * Nn
            h_t /= np.maximum(np.linalg.norm(h_t, axis=1, keepdims=True), 1e-9)
            log("2C Behang: Texel Behang > 0,5 %d, Schattenband > 0,5 %d" % (int((w_beh > 0.5).sum()), int((w_schatten > 0.5).sum())))
        t1 = time.time()
        busch, spitze = buesche_3d(P, Nn, h_t)
        busch = busch.astype(np.float64)
        spitze = spitze.astype(np.float64)
        # Lauf baer-pfoten: an der Pfote (Spiel-z < 0,14) kleinere Buesche (Pfotenhaar 1-2 cm statt Beinfell; ~1,2 cm lang, 0,3 cm breit
        # Spielmass), sonst waere ein Busch so lang wie ein Zeh
        pfk = (1.0 - sst(0.06, 0.14, PF_SPIEL[:, 2])) * rumpf_f
        sel_k = pfk > 0
        if sel_k.any():
            bk, sk = buesche_3d(P[sel_k], Nn[sel_k], h_t[sel_k], zelle=0.012, sig_l=0.016, sig_q=0.004, n_max=0.012, saat=29)
            w_k = pfk[sel_k]
            busch[sel_k] = busch[sel_k] * (1.0 - w_k) + bk * w_k
            spitze[sel_k] = spitze[sel_k] * (1.0 - w_k) + sk * w_k
            log("PFOTE kleine Buesche: Texel %d" % int(sel_k.sum()))
        if C2C:
            sel_b = w_beh > 0.02
            if sel_b.any():
                # haengende Buendel: laenger (sig_l 6,5 statt 4,5 cm Hochmodell), etwas schmaler
                bb_, sb_ = buesche_3d(P[sel_b], Nn[sel_b], h_t[sel_b], zelle=0.026, sig_l=0.065, sig_q=0.0065, n_max=0.03, saat=37)
                w_b_ = w_beh[sel_b]
                busch[sel_b] = busch[sel_b] * (1.0 - w_b_) + bb_ * w_b_
                spitze[sel_b] = spitze[sel_b] * (1.0 - w_b_) + sb_ * w_b_
        str_k = STR_AMP * (1.0 - 0.15 * ruhig) * weg_kopf * rumpf_f * (sohle_t[tt] == 0)
        if C2C:
            # Kopf-Passung: nahe am Kopf feinere/schwaechere Straehnen (SPEZ 6.2 Punkt 4: Feinkontrast <= 1,1 x Kopf); Behang mehr Hub
            w_fein = 1.0 - sst(0.20, 0.32, dk)
            str_k = str_k * (1.0 - HALS_FEIN * w_fein) * (1.0 + BEHANG_HUB * w_beh)
        S = S * (1.0 + str_k * (busch - busch.mean()) * 1.6)[:, None]
        S = S + (str_k * 0.30 * spitze * (1.0 - unten) * (1.0 - k57))[:, None] * np.array((0.20, 0.14, 0.075))
        if C2C:
            S = S * (1.0 - BEHANG_SCHATTEN * w_schatten)[:, None]
        log("NACHBESSERUNG Buesche: Hub %.2f, Anteil Busch > 0,5: %.3f, %.1fs" % (STR_AMP, float((busch > 0.5).mean()), time.time() - t1))
        # Faltenschatten aus der Verdeckung des Spielnetzes (nur nahe Flaechen): offene Flaeche bleibt, tiefe Falte bis -AO_K
        t1 = time.time()
        occ_v = ao_punkte(V, T, N)
        occ_v = E["glatt_feld"](occ_v[:, None], Ed, len(V), 2, 0.5)[:, 0]
        occ = feld_texel(occ_v)
        falte = sst(0.22, 0.62, occ) * weg_kopf * rumpf_f
        S = S * (1.0 - AO_K * falte)[:, None]
        log("Faltenschatten: Verdeckung je Punkt %.1fs, Texel mit Falte > 0,5: %.4f" % (time.time() - t1, (falte > 0.5).mean()))
        # Lauf baer-pfoten: Zehenrillen und Kerben an der Pfote dunkler - Verdeckung im Kleinen (Reichweite 3 cm Spielmass) nur an den
        # Pfotenpunkten (Spiel-z < 9 cm); die Rillen sind Geometrie des Spielnetzes (0,6-2,4 cm tief, log/abnahme_final.txt)
        t1 = time.time()
        Vf_ = E["h2f"](V)
        nur_p = np.nonzero(Vf_[:, 2] < 0.09)[0]
        occ_k = ao_punkte(V, T, N, n_strahl=48, weit=0.04, nur=nur_p)
        occ_k = E["glatt_feld"](occ_k[:, None], Ed, len(V), 1, 0.5)[:, 0]
        rille = sst(RILLE_A, RILLE_B, feld_texel(occ_k)) * (1.0 - sst(0.07, 0.09, PF_SPIEL[:, 2])) * rumpf_f * (sohle_t[tt] == 0)
        S = S * (1.0 - RILLE_K * rille)[:, None]
        log("PFOTE Zehenrillen: Punkte %d, %.1fs, Texel mit Rille > 0,5: %d" % (len(nur_p), time.time() - t1, int((rille > 0.5).sum())))
        # Nachbesserung 09.11.: Unterseite hoechstens so hell wie der Ruecken (Mittel ueber wenige cm; die Struktur bleibt). Die Aufhellung
        # war fuer die Ruhehaltung gerechnet; beim Aufrichten/Sitzen dreht die Leiste zur Kamera und leuchtete als goldenes "V" (major 1)
        lumw = np.array((0.2126, 0.7152, 0.0722))
        Lt = S @ lumw
        ref_l = float(np.median(Lt[ref]))
        cb = np.median(S[ref] / np.maximum(Lt[ref], 1e-4)[:, None], 0)
        cb = cb / float(cb @ lumw)
        Llow = feld_glatt(Lt, 3, nur=rumpf_t)
        l57_vor = float(np.median(Lt[k57 > 0.8])) if (k57 > 0.8).any() else -1.0
        f57 = np.minimum(1.0, CAP_L * ref_l / np.maximum(Llow, 1e-4))
        fU = np.minimum(1.0, CAP_U * ref_l / np.maximum(Llow, 1e-4))
        S = S * ((1.0 - k57 * (1.0 - f57)) * (1.0 - (1.0 - k57) * kU * (1.0 - fU)))[:, None]
        # Farbton: Leiste wie der Ruecken (kein Gold), Pfoten grau-braun (nicht rostorange), zu satte Texel begrenzen
        Lt = S @ lumw
        S = S * (1.0 - 0.5 * k57)[:, None] + (Lt[:, None] * cb[None, :]) * (0.5 * k57)[:, None]
        pfote = (1.0 - sst(0.10, 0.30, P[:, 2])) * weg_kopf * rumpf_f
        cp = np.array((1.10, 1.0, 0.86))
        cp = cp / float(cp @ lumw)
        S = S * (1.0 - 0.6 * pfote)[:, None] + (Lt[:, None] * cp[None, :]) * (0.6 * pfote)[:, None]
        Lt = S @ lumw
        mxv = S.max(1)
        sat = (mxv - S.min(1)) / np.maximum(mxv, 1e-4)
        zu = np.clip((sat - SAT_MAX) / np.maximum(sat, 1e-4), 0.0, 1.0) * rumpf_f * weg_kopf * sst(0.22, 0.32, mxv)   # dunkle Texel bleiben
        S = S * (1.0 - zu)[:, None] + (Lt[:, None] * cb[None, :]) * zu[:, None]
        log("NACHBESSERUNG Unterseite: Ruecken-Luma %.3f; Leiste (k57 > 0,8) Median %.3f -> %.3f; Texel mit Saettigung gedeckelt %d" % (
            ref_l, l57_vor, float(np.median((S @ lumw)[k57 > 0.8])) if (k57 > 0.8).any() else -1.0, int((zu > 0).sum())))
        # Lauf baer-pfoten: Pfoten-/Unterbein-Helligkeit je Hoehe an baer-fell angleichen. Das Pfotenhaar des neuen Hochmodells deckt die
        # ganze Pfote bis 30 cm (vorher nur Zehenbuesche) und bekommt fuer den Bake das hellere Zehenhaar-Material (zeh_hell): Fuss 4-12 cm
        # Luma 71-72 statt 50-59, Unterschenkel 20-30 cm 51 statt 61 (v5, gemessen 19:35 an texel_v5.npz gegen baer-fell texel_fix.npz).
        # Ziel = Median-Luma (sRGB) der fertigen baer-fell-Textur je Hoehenband (Rumpf, ohne Sohle), unten 0-4 cm 62 statt 72 (dort lag in
        # baer-fell der helle Fellkranz der Saeule). Weiche Kurve ueber die Bandmitten, Faktor 0,70..1,25, ab 30-40 cm aus.
        if PF_ABGLEICH:
            zs_ = PF_SPIEL[:, 2]
            lumw_ = np.array((0.2126, 0.7152, 0.0722))
            fell_t = rumpf_t & (sohle_t[tt] == 0) & (kopf_maske < 0.02)
            kanten_z = (0.0, 0.04, 0.08, 0.12, 0.20, 0.30)
            mitte_z, gain_z = [], []
            Lt_ = S @ lumw_
            for i_ in range(len(kanten_z) - 1):
                mb = fell_t & (zs_ >= kanten_z[i_]) & (zs_ < kanten_z[i_ + 1])
                ist = float(np.median(Lt_[mb])) if mb.sum() > 100 else PF_ZIEL[i_]
                mitte_z.append(0.5 * (kanten_z[i_] + kanten_z[i_ + 1]))
                gain_z.append(float(np.clip(PF_ZIEL[i_] / max(ist, 1e-3), 0.70, 1.25)))
            g_ = np.interp(zs_, mitte_z, gain_z)
            w_g = (1.0 - sst(0.27, 0.31, zs_)) * fell_t
            S = S * (1.0 + (g_ - 1.0) * w_g)[:, None]
            log("PFOTE Helligkeit je Hoehe (Bandmitte cm: Faktor):", {round(m_ * 100): round(g2, 3) for m_, g2 in zip(mitte_z, gain_z)})
            # v7: Uebergang Knie/Ellbogen (Spiel-z 0,27-0,50) oertlich an baer-fell (zw = fertige baer-fell-Textur, uebertragen; nur ueber
            # 0,30 gueltig): v6 hatte dort ein helles Band (0,30-0,34: Luma 70-80) und darueber ein dunkles (0,35-0,39: 49-53) gegen
            # baer-fell 53-62 -> im Bild eine dunkle Querlinie am Bein. Glatte Felder (log-Luma, 10 Runden ueber das Netz), Detail bleibt.
            ub = fell_t & (zs_ > 0.25) & (zs_ < 0.52)
            lm_ = feld_glatt(np.log(np.maximum(S @ lumw_, 1e-3)), 10, nur=ub)
            lz_ = feld_glatt(np.log(np.maximum(zw @ lumw_, 1e-3)), 10, nur=ub & (zs_ > 0.30))
            w_u = sst(0.27, 0.31, zs_) * (1.0 - sst(0.44, 0.50, zs_)) * fell_t
            if C2C:
                # 2c: nur an den Beinen (|y| > 5-11 cm) und oben weich (z 0,42-0,58): an der Brust zwischen den Vorderbeinen gab die Kante
                # z 0,44-0,50 im Sitzen eine waagerechte Linie quer ueber die Brust (v3, auch im NCBearTest-Stand)
                bein_y = sst(0.05, 0.11, np.abs(PF_SPIEL[:, 1]))
                w_u = sst(0.27, 0.31, zs_) * (1.0 - sst(0.42, 0.58, zs_)) * fell_t * bein_y
            S = S * np.exp(np.clip(lz_ - lm_, -0.5, 0.4) * w_u)[:, None]
            log("PFOTE Uebergang 27-50 cm an baer-fell: Faktor p5/p50/p95 %.2f/%.2f/%.2f" % tuple(
                np.percentile(np.exp(np.clip(lz_ - lm_, -0.5, 0.4))[w_u > 0.5], (5, 50, 95))))
            # v8/v9: Unter dem Wulst, wo der dicke Rumpf in das duenne Bein uebergeht (neu, Netz baer-pfoten), zeigen die Ansichten am
            # Rand des Wulstes ein ~1,5 cm breites dunkles Band (Ansichten-Helligkeit -30 %, Spiel-z 0,35-0,365 vorn) -> im Bild eine harte
            # dunkle Linie um das Bein. Das Band ist waagerecht: je Bein und je 45-Grad-Sektor der Normalen die Median-Log-Luma je 0,5 cm
            # Hoehe, gegen ihre Glaettung (sigma 2,5 cm) zu BAND_K eingeebnet. Straehnen (Abweichungen innerhalb eines Hoehenschritts) bleiben.
            lg_ = np.log(np.maximum(S @ lumw_, 1e-3))
            w_b = sst(0.27, 0.31, zs_) * (1.0 - sst(0.46, 0.50, zs_)) * fell_t
            z_b0 = 0.24
            if FIX1:
                # Kegel statt Wulst (Netz fix1, Spiel-z 0,14-0,34): waagerechte Baender dort ebenso einebnen (Pruefer Optik M1 "dunkle Ringlinie")
                w_b = sst(0.13, 0.16, zs_) * (1.0 - sst(0.46, 0.50, zs_)) * fell_t
                if C2C:
                    w_b = sst(0.13, 0.16, zs_) * (1.0 - sst(0.42, 0.58, zs_)) * fell_t * sst(0.05, 0.11, np.abs(PF_SPIEL[:, 1]))
                z_b0 = 0.11
            korr = np.zeros(n_t)
            bins = np.arange(z_b0, 0.525, 0.005)
            sek = np.floor((np.arctan2(Nn[:, 1], Nn[:, 0]) + math.pi) / (math.pi / 4.0)).astype(np.int64) % 8
            n_k = 0
            for bx_ in ((0.0, 9.0), (-9.0, 0.0)):
                for by_ in ((0.0, 9.0), (-9.0, 0.0)):
                    bein_ = fell_t & (PF_SPIEL[:, 0] > bx_[0]) & (PF_SPIEL[:, 0] < bx_[1]) & (PF_SPIEL[:, 1] > by_[0]) & (PF_SPIEL[:, 1] < by_[1]) & (zs_ > z_b0) & (zs_ < 0.52)
                    for k_ in range(8):
                        m_ = bein_ & (sek == k_)
                        if m_.sum() < 500:
                            continue
                        ib = np.clip(np.digitize(zs_[m_], bins) - 1, 0, len(bins) - 2)
                        med = np.full(len(bins) - 1, np.nan)
                        for j_ in np.unique(ib):
                            vv = lg_[m_][ib == j_]
                            if len(vv) >= 15:
                                med[j_] = np.median(vv)
                        ok_ = ~np.isnan(med)
                        if ok_.sum() < 10:
                            continue
                        zc = 0.5 * (bins[:-1] + bins[1:])
                        medf = np.interp(zc, zc[ok_], med[ok_])
                        ker = np.exp(-0.5 * (np.arange(-10, 11) * 0.005 / 0.025) ** 2)
                        glatt_ = np.convolve(np.pad(medf, 10, mode="edge"), ker / ker.sum(), mode="valid")
                        korr[m_] = np.interp(zs_[m_], zc, medf - glatt_)
                        n_k += 1
            S = S * np.exp(-BAND_K * np.clip(korr, -0.5, 0.5) * w_b)[:, None]
            log("PFOTE Band-Glaettung Uebergang: Bein-Sektoren %d, Texel %d, Korrektur p5/p95 %.2f/%.2f" % (n_k, int((w_b > 0.5).sum()),
                *np.percentile(korr[w_b > 0.5], (5, 95))))
            # v12 (zweiter Anlauf, 09.11. ~20:30): heller Fellring unten um die Sohle. Die Ansichten sehen am Sohlenrand helles Haar bzw.
            # die helle Sohle des Hochmodells: Rumpf-Fell (Ruhepose) 0-1 cm Luma 102, 1-3 cm 70-83 gegen 49-64 bei 3-12 cm (v11). Im Bild
            # ein heller Ring/Doppelstrich um die Ferse (Sitzen nah) und um die Sohle (von unten) - wie eine Schnittkante. Deckel: geglaettete
            # Log-Luma unter 5 cm (Rumpf UND Sohlen-Insel, deren Rand sohlen_malen weich in die gebackene Farbe mischt) hoechstens Bezug je
            # Bein (Median Fell 4-8 cm) x RAND_K; nur abdunkeln, Straehnen (Abweichung vom geglaetteten Feld) bleiben.
            fuss_ = rumpf_t & (kopf_maske < 0.02) & (zs_ < 0.065)
            lr_ = feld_glatt(np.log(np.maximum(S @ lumw_, 1e-3)), 6, nur=fuss_)
            deckel = np.full(n_t, 9.0)
            for bx_ in ((0.0, 9.0), (-9.0, 0.0)):
                for by_ in ((0.0, 9.0), (-9.0, 0.0)):
                    bein_ = (PF_SPIEL[:, 0] > bx_[0]) & (PF_SPIEL[:, 0] < bx_[1]) & (PF_SPIEL[:, 1] > by_[0]) & (PF_SPIEL[:, 1] < by_[1])
                    mb = fell_t & bein_ & (zs_ >= 0.04) & (zs_ < 0.08)
                    if mb.sum() > 100:
                        deckel[bein_] = math.log(float(np.median((S @ lumw_)[mb])) * RAND_K)
            w_r = (1.0 - sst(0.035, 0.05, zs_)) * fuss_
            k_r = np.minimum(0.0, deckel - lr_) * w_r
            S = S * np.exp(k_r)[:, None]
            log("PFOTE Sohlenrand-Deckel (RAND_K %.2f): Texel %d, Faktor p5/p50 %.2f/%.2f" % (RAND_K, int((k_r < -0.01).sum()),
                *np.exp(np.percentile(k_r[w_r > 0.5], (5, 50)))))
        if C2C:
            # 2c Brust-Glaettung: an Brust/Kehle/Achsel vorn eine waagerechte Helligkeitsstufe (im Sitzen von vorn eine Linie quer ueber
            # die Brust, auch im NCBearTest-Stand; nicht in der Form: Ton glatt). Mittlere Stufen (Feld 3 gegen 30 Runden ueber das Netz)
            # zu BRUST_K einebnen; Feinstruktur (Straehnen) und das grosse Feld (helle Unterseite) bleiben.
            lw_b = np.array((0.2126, 0.7152, 0.0722))
            xs_b, ys_b, zs_b = PF_SPIEL[:, 0], np.abs(PF_SPIEL[:, 1]), PF_SPIEL[:, 2]
            m_b = (rumpf_t & (sohle_t[tt] == 0) & (xs_b > 0.10) & (zs_b > 0.22) & (zs_b < 0.80) & (ys_b < 0.30) & (dk > 0.02))
            lg_b = np.log(np.maximum(S @ lw_b, 1e-3))
            l_f = feld_glatt(lg_b, 3, nur=m_b)
            l_c = feld_glatt(lg_b, 30, nur=m_b)
            w_bb = (sst(0.10, 0.18, xs_b) * sst(0.22, 0.30, zs_b) * (1.0 - sst(0.70, 0.80, zs_b)) * (1.0 - sst(0.24, 0.30, ys_b))
                    * sst(0.02, 0.06, dk) * m_b)
            S = S * np.exp(-BRUST_K * np.clip(l_f - l_c, -0.4, 0.4) * w_bb)[:, None]
            log("2C Brust-Glaettung: Texel %d, Stufe p5/p95 %.2f/%.2f" % (int((w_bb > 0.5).sum()), *np.percentile((l_f - l_c)[w_bb > 0.5], (5, 95))))
        # Wo nur Ansichten gegen die Haarspitzen sehen (Hinterteil, Hinterseite der Beine): feines Gesprenkel daempfen
        kontrast = ruhig     # Nachbesserung: dieselbe Maske wie die Glaettung oben (dort weniger nachschaerfen)
        # Naht zum alten Kopf: (1) Farbe des Halses grob an das alte Fell (geglaettete Felder, Verhaeltnis je Kanal), (2) direkt an
        # der Naht weich ins alte Fell (gleiche UV, alte Ansichten = Zwischenstand des Netz-Bauers)
        hals = rumpf_t & (hb < NAHT_C + 0.05)
        Sg = feld_glatt(np.log(np.maximum(S, 1e-3)), 6, nur=hals)
        Zg = feld_glatt(np.log(np.maximum(zw, 1e-3)), 6, nur=hals)
        w_far = (1.0 - sst(NAHT_B, NAHT_C, hb)) * rumpf_f
        S = S * np.exp(np.clip(Zg - Sg, -0.7, 0.7) * w_far[:, None])
        w_naht = (1.0 - sst(NAHT_A, NAHT_B, hb)) * rumpf_f
        S = S * (1.0 - w_naht[:, None]) + zw * w_naht[:, None]
        if C2C:
            # 2c Kopf-Passung (SPEZ 6.2 Punkt 4, C3): Hals, Nacken, Kehle, Schultern und Buckel gleiten in Helligkeit und Farbe zum
            # Kopfmittel (Kopf-Texel des Bezugs = alte Kopf-Texel, gleiche UV). Ziel je Abstand zum Kopf HALS_D/HALS_F (Anteil am Kopfmittel,
            # Luma 0,299/0,587/0,114 wie mess_texel_naht.py); nur anheben (geglaettetes Log-Feld, Straehnen bleiben), ab 3-7 cm von der
            # Kopfnaht (dort bleibt die Naht-Mischung), nur ueber Spiel-z 0,42-0,55 (Beine bleiben dunkler), Farbton bis 30-45 cm.
            lw3 = np.array((0.299, 0.587, 0.114))
            kopf_tex = gegend[tt] == 1
            Lk = float((zw[kopf_tex] @ lw3).mean())
            ck = zw[kopf_tex].mean(0)
            ck = ck / float(ck @ lw3)
            r_ = np.interp(dk, HALS_D, HALS_F)
            w_on = sst(0.005, 0.05, dk) * sst(0.30, 0.62, PF_SPIEL[:, 2]) * rumpf_f * (sohle_t[tt] == 0)   # v1: 3-7 cm, z 0,42-0,55 (Kante Brust)
            hals_m = rumpf_t & (dk < 0.65) & (sohle_t[tt] == 0)
            Lg = feld_glatt(np.log(np.maximum(S @ lw3, 1e-3)), 10, nur=hals_m)
            g_ = np.clip(np.log(np.maximum(r_ * Lk, 1e-3)) - Lg, 0.0, math.log(1.6)) * w_on
            S = S * np.exp(g_)[:, None]
            c_w = HALS_FARBE * w_on * (1.0 - sst(0.30, 0.45, dk))
            Lt3 = S @ lw3
            S = S * (1.0 - c_w)[:, None] + (Lt3[:, None] * ck[None, :]) * c_w[:, None]
            band_ = {}
            for a_b, b_b in ((0, 0.04), (0.04, 0.08), (0.08, 0.12), (0.12, 0.20), (0.20, 0.35), (0.35, 0.60)):
                mb_ = rumpf_t & (sohle_t[tt] == 0) & (dk >= a_b) & (dk < b_b)
                band_["%d-%d" % (a_b * 100, b_b * 100)] = round(float((S[mb_] @ lw3).mean() / Lk), 3) if mb_.any() else None
            log("2C Kopf-Passung: Kopfmittel Luma %.1f RGB %s, Anhebung p50/p95/max %.2f/%.2f/%.2f (Texel w > 0,5: %d); Baender/Kopf %s" % (
                Lk * 255, (zw[kopf_tex].mean(0) * 255).round(0).tolist(), *(np.exp(np.percentile(g_[w_on > 0.5], (50, 95, 100))) if (w_on > 0.5).any() else (1, 1, 1)),
                int((w_on > 0.5).sum()), band_))
            if G2:
                # baer-gross G2 (Koerper-Seite): Hals/Kehle/Seiten 0-G2_K1 vom Kopf im geglaetteten Feld auf G2_ZIEL (nur anheben)
                lw7 = np.array((0.2126, 0.7152, 0.0722))
                nah2 = rumpf_t & (sohle_t[tt] == 0) & (dk < 0.15)
                Lg2 = feld_glatt(np.log(np.maximum(S @ lw7, 1e-3)), G2_RUNDEN, nur=nah2)
                w2 = (1.0 - sst(G2_K0, G2_K1, dk)) * rumpf_f * (sohle_t[tt] == 0)
                g2 = np.clip(math.log(G2_ZIEL) - Lg2, 0.0, math.log(G2_MAX)) * w2
                vor2 = {}
                for a_b, b_b in ((0, 0.02), (0.02, 0.04), (0.04, 0.08)):
                    mb_ = rumpf_t & (sohle_t[tt] == 0) & (dk >= a_b) & (dk < b_b)
                    vor2["%d-%d" % (a_b * 100, b_b * 100)] = round(float((S[mb_] @ lw7).mean() * 255), 1) if mb_.any() else None
                S = S * np.exp(g2)[:, None]
                nach2 = {}
                for a_b, b_b in ((0, 0.02), (0.02, 0.04), (0.04, 0.08)):
                    mb_ = rumpf_t & (sohle_t[tt] == 0) & (dk >= a_b) & (dk < b_b)
                    nach2["%d-%d" % (a_b * 100, b_b * 100)] = round(float((S[mb_] @ lw7).mean() * 255), 1) if mb_.any() else None
                log("GROSS G2 Koerper: Ziel Luma %.0f, Texel angehoben %d, Faktor p50/p95/max %.2f/%.2f/%.2f; Luma je Band vorher %s nachher %s" % (
                    G2_ZIEL * 255, int((g2 > 1e-4).sum()), *(np.exp(np.percentile(g2[g2 > 1e-4], (50, 95, 100))) if (g2 > 1e-4).any() else (1, 1, 1)),
                    vor2, nach2))
            if FRONT:
                # baer-gross fix1: Oberarm und Bauchmitte (siehe FRONT oben)
                lwf = np.array((0.2126, 0.7152, 0.0722))
                Gf = np.load(FR_GEW)
                Vf_g, Wf_g = np.asarray(Gf["V"], dtype=np.float64), np.asarray(Gf["W"], dtype=np.float64)
                namf = [str(n) for n in Gf["namen"]]
                if Vf_g.shape == VF.shape and np.abs(Vf_g - VF).max() < 1e-4:
                    zu_g = np.arange(len(VF))
                else:
                    import mathutils.kdtree
                    kd_f = mathutils.kdtree.KDTree(len(Vf_g))
                    for i_f, p_f in enumerate(Vf_g):
                        kd_f.insert(p_f, i_f)
                    kd_f.balance()
                    zu_g = np.array([kd_f.find(p)[1] for p in VF])
                    log("FIX1 FRONT: Gewichte ueber naechsten Punkt zugeordnet, Abstand max %.2e" % float(np.abs(Vf_g[zu_g] - VF).max()))
                arm_v = Wf_g[:, [i for i, n in enumerate(namf) if any(s in n for s in ("UpperArm", "Forearm", "Hand"))]].sum(1)[zu_g]
                wa = feld_texel(arm_v)
                xs_f, ys_f, zs_f = PF_SPIEL[:, 0], np.abs(PF_SPIEL[:, 1]), PF_SPIEL[:, 2]
                frei_f = rumpf_t & (sohle_t[tt] == 0) & (kopf_maske < 0.02)
                Lsm = feld_glatt(np.log(np.maximum(S @ lwf, 1e-3)), 6, nur=frei_f)
                m_sch = frei_f & (xs_f > 0.10) & (xs_f < 0.45) & (zs_f > 0.55) & (zs_f < 0.80) & (ys_f > 0.18) & (wa < 0.15)
                ref_sch = float(np.median(Lsm[m_sch]))
                w_arm = (np.clip((wa - 0.15) / 0.35, 0.0, 1.0) * sst(FR_ELL_Z + FR_ARM_A, FR_ELL_Z + FR_ARM_B, zs_f) * sst(-0.10, 0.0, xs_f)
                         * frei_f)
                g_arm = np.clip(math.log(FR_ARM_K) + ref_sch - Lsm, 0.0, math.log(FR_MAX)) * w_arm
                m_fl = frei_f & (xs_f > -0.30) & (xs_f < 0.10) & (zs_f > 0.40) & (zs_f < 0.65) & (ys_f > 0.25) & (wa < 0.1)
                ref_fl = float(np.median(Lsm[m_fl]))
                w_bau = ((1.0 - sst(0.12, 0.24, ys_f)) * sst(-0.38, -0.26, xs_f) * (1.0 - sst(0.22, 0.34, xs_f)) * sst(0.15, 0.45, -Nn[:, 2])
                         * (1.0 - np.clip((wa - 0.2) / 0.3, 0.0, 1.0)) * frei_f)
                g_bau = np.clip(math.log(FR_BAUCH_K) + ref_fl - Lsm, 0.0, math.log(FR_MAX)) * w_bau
                vor_f = dict(arm=round(float(np.exp(Lsm[w_arm > 0.5]).mean() * 255), 1) if (w_arm > 0.5).any() else None,
                             bauch=round(float(np.exp(Lsm[w_bau > 0.5]).mean() * 255), 1) if (w_bau > 0.5).any() else None)
                S = S * np.exp(g_arm + g_bau)[:, None]
                Lsm2 = np.log(np.maximum(S @ lwf, 1e-3))
                log("FIX1 FRONT: Schulter/Flanke Luma %.1f, Flanke Bauchhoehe %.1f; Oberarm Texel %d (Faktor p50/p95 %.2f/%.2f), Bauch Texel %d "
                    "(Faktor p50/p95 %.2f/%.2f); geglaettet vorher %s, nachher Mittel Arm %.1f Bauch %.1f" % (
                        math.exp(ref_sch) * 255, math.exp(ref_fl) * 255, int((w_arm > 0.5).sum()),
                        *np.exp(np.percentile(g_arm[w_arm > 0.5], (50, 95))), int((w_bau > 0.5).sum()),
                        *np.exp(np.percentile(g_bau[w_bau > 0.5], (50, 95))), vor_f,
                        float(np.exp(Lsm2[w_arm > 0.5]).mean() * 255), float(np.exp(Lsm2[w_bau > 0.5]).mean() * 255)))
    S = np.clip(S, 0.0, 1.0)
    col = np.zeros((TEX, TEX, 3), dtype=np.float32)
    frei = np.ones((TEX, TEX), dtype=bool)
    col[my[gesehen], mx[gesehen]] = S[gesehen].astype(np.float32)
    frei[my[gesehen], mx[gesehen]] = False
    r_ = E["fuellen"](col, frei, maske, 400)
    if (frei & maske).any():
        col[frei & maske] = S[gesehen].mean(0)
        frei[frei & maske] = False
    E["fuellen"](col, frei, np.ones_like(maske), 14)
    col[frei] = S[gesehen].mean(0)
    if not NUR_NEU and RUHIG_K <= 0:
        km = np.zeros((TEX, TEX), dtype=np.float32)
        km[my, mx] = (KONTRAST_D * kontrast).astype(np.float32)
        weich = col.copy()
        for _ in range(2):
            weich = (np.roll(weich, 1, 0) + np.roll(weich, -1, 0) + np.roll(weich, 1, 1) + np.roll(weich, -1, 1) + weich * 2.0) / 6.0
        col = col - (col - weich) * km[..., None]
    kmap = np.full((TEX, TEX), SCHAERFE, dtype=np.float32)
    # v10: im Uebergang Rumpf/Bein (Wulst, Spiel-z 0,30-0,42) kaum nachschaerfen - die Unschaerfemaske machte aus dem flachen dunklen Band
    # am Wulstrand eine scharfe Linie
    w_sch = sst(0.28, 0.31, PF_SPIEL[:, 2]) * (1.0 - sst(0.42, 0.46, PF_SPIEL[:, 2])) * rumpf_t
    if C2C:
        w_sch = w_sch * 0.0      # 2c: kein Wulst mehr (form_2c); die Schaerfe-Kante z 0,42-0,46 gab unten an der Brust eine flache Zone
    k_d = 0.7 * kontrast
    if FIX1:
        # Pruefer Optik minor 5 "Unterbein glatter, weniger Straehnen": unter 30 cm (nicht an der Pfote unter 5 cm) halb so viel daempfen
        k_d = k_d * (1.0 - 0.5 * (1.0 - sst(0.27, 0.31, PF_SPIEL[:, 2])) * sst(0.05, 0.08, PF_SPIEL[:, 2]) * rumpf_t)
    if C2C:
        k_d = 1.0 - (1.0 - k_d) * (1.0 - 0.5 * (1.0 - sst(0.20, 0.32, dk)) * rumpf_t)    # 2c: nahe am Kopf halb so viel nachschaerfen
    kmap[my, mx] = (SCHAERFE * (1.0 - 0.9 * ring) * (1.0 - k_d) * (1.0 - 0.8 * w_sch)).astype(np.float32)
    col = E["unscharf"](col, kmap)
    # ---------------------------------------------------------- Sohlen
    sohle_m = np.zeros((TEX, TEX), dtype=bool)
    if not NUR_NEU:
        S_fell = col.copy()
        if os.environ.get("BAER_TX_VOR_SOHLE", "") == "1":
            png_schreiben(TX + "NCBear_%s_vor_sohle_2048.png" % AUSNAME, col)     # Lauf baer-pfoten: Pruefbild (gebacken, ohne Sohlen)
        # Nachbesserung: Fellfarbe je Pfote = Median des Rumpf-Fells unten an dieser Pfote (Spielmass z < 7 cm, 16 cm um die Sohle)
        Pf = E["h2f"](P)
        pf_k = K["sohle_pfote"][::-1]
        xyz_k = K["sohle_xyz"][::-1]
        fell_pfote = {}
        for pid_ in (1, 2, 3, 4):
            mk = pf_k == pid_
            if not mk.any():
                continue
            c_ = np.nanmean(xyz_k[mk], 0)
            sel_ = rumpf_t & (sohle_t[tt] == 0) & (Pf[:, 2] < 0.07) & (np.hypot(Pf[:, 0] - c_[0], Pf[:, 1] - c_[1]) < 0.16)
            if sel_.sum() > 50:
                fell_pfote[pid_] = np.median(col[my[sel_], mx[sel_]], 0).astype(np.float32)
        log("NACHBESSERUNG Pfotenfell je Pfote (sRGB):", {k: (v * 255).round(0).tolist() for k, v in fell_pfote.items()})
        sohle_m = sohlen_malen(col, maske, my, mx, K, SOHLE_JSON, S_fell, fell_pfote, Pf=Pf, Nn=Nn,
                               tex_frei=rumpf_t & (sohle_t[tt] == 0))
        # v13: UV-Polster (Texel ohne Netz) um die Sohlen-Inseln neu aus den gemalten Insel-Texeln fuellen. Das Polster stammt aus dem
        # Fuellen VOR dem Sohlenmalen (helle gebackene Farbe) und wirkt ueber das 2x2-Mittel der 1024er und bilinear als heller Rand.
        nah_ = wachsen(sohle_m, 10) & ~maske
        frei_ = nah_.copy()
        E["fuellen"](col, frei_, nah_, 10)
        log("PFOTE Sohlen-Polster neu gefuellt: Texel %d" % int(nah_.sum()))
    # ---------------------------------------------------------- Kopf und Krallen: alte Texel (wie baer_export_anim.py)
    A = png_laden(E["ALT_PNG"])
    behalte = maske & (gegend[np.maximum(tri, 0)] != 0)
    rumpf_m = maske & (gegend[np.maximum(tri, 0)] == 0)
    setzen = wachsen(behalte, 6) & ~wachsen(rumpf_m, 2)
    if FIX1:
        # fix1: Kopf-Texel selbst immer alt, auch wenn eine Rumpf-Insel naeher als 2 px liegt (neue UV-Packung: sonst 3 Kopf-Texel anders)
        setzen |= behalte & ~rumpf_m
    col[setzen] = A[setzen]
    log("Alte Texel fuer Kopf und Krallen: %d, Ueberlappung Kopf/Rumpf-Inseln %d" % (int(setzen.sum()), int((behalte & rumpf_m).sum())))
    if C2C and G2 and not NUR_NEU:
        # baer-gross G2 (Kopf-Seite): Kopfrand-Band = Kopf-Texel bis G2_H1 von der Kopfnaht (3D-Abstand des Kopfpunkts zum naechsten
        # Rumpfpunkt, Spielmeter, baryzentrisch je Texel), ohne Gesicht (Auge, Nase, Schnauze, Lippe/Unterkiefer-Vorderteil, Ohr + G2_OHR
        # Abstand zur Ohrschale) und ohne Maul-Inneres (UV-Rechteck wie r_naht/g_mess). Geglaettetes Log-Luma der alten Kopf-Texel auf
        # G2_ZIEL (nur heller); ausserhalb des Bands Faktor 0 -> Texel nicht geschrieben (bit-gleich).
        from mathutils.kdtree import KDTree
        lw7 = np.array((0.2126, 0.7152, 0.0722))
        Vs2 = E["h2f"](V)
        rv2 = np.unique(T[gegend == 0].ravel())
        kv2 = np.unique(T[gegend == 1].ravel())
        kd2 = KDTree(len(rv2))
        for i_, p_ in enumerate(Vs2[rv2]):
            kd2.insert(p_, i_)
        kd2.balance()
        dv2 = np.zeros(len(V))
        for i_ in kv2:
            dv2[i_] = kd2.find(Vs2[i_])[2]
        kopf_t2 = gegend[tt] == 1
        dn_t = feld_texel(dv2)
        cand = np.nonzero(kopf_t2 & (dn_t < G2_H1 + 0.012))[0]
        # genauer Abstand je Kandidaten-Texel (Lage im Texel, nicht baryzentrisch gemittelt): Band streng < G2_H1
        dex = np.array([kd2.find(p_)[2] for p_ in E["h2f"](P[cand])])
        cand, dex = cand[dex < G2_H1], dex[dex < G2_H1]
        dn_t = np.full(n_t, 9.0)
        dn_t[cand] = dex
        a2_, b2_, c2_ = L_[cand, 0], L_[cand, 1], L_[cand, 2]
        R2 = Q["regionen"](a2_, b2_, c2_)
        oa2, _os2 = Q["ohr_teile"](a2_, np.abs(b2_), c2_)
        ges2 = np.maximum.reduce([R2["aug"], R2["nah"], R2["schf"], R2["unter"], R2["ohr"], R2["innen"], 1.0 - sst(0.0, G2_OHR, oa2)])
        zeile2 = (TEX - 1) - my[cand]
        maul2 = (mx[cand] >= 2 * 255) & (mx[cand] <= 2 * 695) & (zeile2 <= 2 * 115)
        wk2 = (1.0 - sst(G2_H0, G2_H1, dn_t[cand])) * (1.0 - sst(0.0, 0.02, ges2)) * (~maul2)
        alt2 = col[my, mx].astype(np.float64)
        Lh2 = feld_glatt(np.log(np.maximum(alt2 @ lw7, 1e-3)), G2_RUNDEN, nur=kopf_t2)
        gk2 = np.clip(math.log(G2_ZIEL) - Lh2[cand], 0.0, math.log(G2_MAX)) * wk2
        an2 = gk2 > 0.0
        ci = cand[an2]
        neu2 = np.clip(alt2[ci] * np.exp(gk2[an2])[:, None], 0.0, 1.0).astype(np.float32)
        Rr = np.ones_like(col)
        Rr[my[ci], mx[ci]] = neu2 / np.maximum(col[my[ci], mx[ci]], 1e-4)
        col[my[ci], mx[ci]] = neu2
        # UV-Polster der Kopf-Inseln (6 px, nicht naeher als 2 px an anderen Inseln) mit dem Faktor der Nachbar-Texel
        insel2 = np.zeros(maske.shape, dtype=bool)
        insel2[my[kopf_t2], mx[kopf_t2]] = True
        rand2 = wachsen(insel2, 6) & ~insel2 & ~wachsen(maske & ~insel2, 2)
        frei2 = rand2.copy()
        E["fuellen"](Rr, frei2, rand2, 8)
        r2m = rand2 & (np.abs(Rr - 1.0).max(2) > 1e-6)
        col[r2m] = np.clip(col[r2m] * Rr[r2m], 0.0, 1.0)
        band2 = np.zeros(n_t, dtype=bool)
        band2[ci] = True
        os.makedirs(TX + "mess", exist_ok=True)
        np.savez_compressed(TX + "mess/g2_band_%s.npz" % AUSNAME, band=band2, d_naht=dn_t.astype(np.float32))
        Lv2 = alt2[ci] @ lw7
        Ln2 = neu2.astype(np.float64) @ lw7
        log("GROSS G2 Kopfrand: Kandidaten (< %.0f cm) %d, davon Gesicht/Ohr/Maul gesperrt %d, angehoben %d (Faktor p50/p95/max %.2f/%.2f/%.2f), "
            "Luma Band %.1f -> %.1f, Polster-Texel %d; Band a %.3f..%.3f" % (
                G2_H1 * 100, len(cand), int((wk2 <= 0).sum()), len(ci), *(np.exp(np.percentile(gk2[an2], (50, 95, 100))) if an2.any() else (1, 1, 1)),
                Lv2.mean() * 255 if len(ci) else 0, Ln2.mean() * 255 if len(ci) else 0, int(r2m.sum()),
                a2_[an2].min() if an2.any() else 0, a2_[an2].max() if an2.any() else 0))
    if not NUR_NEU:
        # Nachbesserung 09.11. (Pruefer Technik m3): Krallen-UV sind fast Punkte; das Spiel liest bilinear 2x2 Texel. Liegt dieses Lesefeld
        # (in der 2048er und in der 1024er = 2x2-Mittel der 2048er, baer_kampf_fell.py) in einer Rumpf-Insel, dort die alten Texel,
        # damit die Krallen genau wie vorher aussehen. Zeile = v x Aufloesung (Zeile 0 unten wie col).
        uvk = uv[LT[gegend == 2].ravel()]
        fp = np.zeros((TEX, TEX), dtype=bool)
        for res in (TEX, TEX // 2):
            f_ = TEX // res
            x0 = np.floor(uvk[:, 0] * res - 0.5).astype(np.int64)
            y0 = np.floor(uvk[:, 1] * res - 0.5).astype(np.int64)
            for dx in (0, 1):
                for dy in (0, 1):
                    xx = np.clip(x0 + dx, 0, res - 1)
                    yy = np.clip(y0 + dy, 0, res - 1)
                    for ex in range(f_):
                        for ey in range(f_):
                            fp[yy * f_ + ey, xx * f_ + ex] = True
        # Bezug = die Textur, die heute im Spiel ist (NCBearTest, eb717769 = bestand/NCBear_2048.png); ALT_PNG ist der Stand vor baer-anim
        # (Kopf-/Krallen-Inseln gleich, Rumpf anders)
        Bst = png_laden(BESTAND_PNG)
        zus = fp & ~setzen
        col[fp] = Bst[fp]
        log("NACHBESSERUNG Krallen-Lesefeld: Texel %d, davon zusaetzlich alt %d (davon in Rumpf-Inseln %d)" % (
            int(fp.sum()), int(zus.sum()), int((zus & rumpf_m).sum())))
        if C2C:
            # 2c (SPEZ 4, Kevins Vorlage "kurze dunkle Krallen"): Krallen dunkler. Je Krallen-Schale t = 0 an der Wurzel (naechster
            # Abstand zum Rumpf klein) bis 1 an der Spitze; Zielfarbe Wurzel -> Spitze (hinten KRALLE_H, vorn KRALLE_V); in das 2x2-Lesefeld
            # jeder Ecke (2048 und 1024 = 2x2-Mittel) gemittelt; je Kanal hoechstens so hell wie vorher (nur dunkler).
            from mathutils.kdtree import KDTree
            kt_ = np.nonzero(gegend == 2)[0]
            par_ = np.arange(len(V))

            def wurzel_(a):
                while par_[a] != a:
                    par_[a] = par_[par_[a]]
                    a = par_[a]
                return a
            for t_ in T[kt_]:
                r0 = wurzel_(t_[0])
                for v_ in t_[1:]:
                    r1 = wurzel_(v_)
                    if r1 != r0:
                        par_[r1] = r0
            kv_ = np.unique(T[kt_].ravel())
            schale_ = np.array([wurzel_(v_) for v_ in kv_])
            Vf_k = E["h2f"](V)
            rv_ = np.unique(T[gegend == 0].ravel())
            kd_ = KDTree(len(rv_))
            for i_, p_ in enumerate(Vf_k[rv_]):
                kd_.insert(p_, i_)
            kd_.balance()
            dr_ = np.array([kd_.find(p_)[2] for p_ in Vf_k[kv_]])
            t_k = np.zeros(len(V))
            for sc_ in np.unique(schale_):
                m_ = schale_ == sc_
                d_ = dr_[m_]
                t_k[kv_[m_]] = np.clip((d_ - d_.min()) / max(d_.max() - d_.min(), 1e-6), 0.0, 1.0)
            ziel_ = np.zeros((len(V), 3))
            vorn_k = Vf_k[:, 0] > 0.0
            for vk_, (cw_, cs_) in ((True, KRALLE_V), (False, KRALLE_H)):
                m_ = vorn_k == vk_
                tt_ = t_k[m_][:, None] ** 0.8
                ziel_[m_] = cw_[None, :] * (1.0 - tt_) + cs_[None, :] * tt_
            ecken_ = LT[kt_].ravel()
            ev_ = T[kt_].ravel()
            uve_ = uv[ecken_]
            acc_ = np.zeros((TEX, TEX, 3))
            cnt_ = np.zeros((TEX, TEX))
            seite_ = np.zeros((TEX, TEX), dtype=np.int8)   # 1 vorn, 2 hinten, 3 beide
            for res in (TEX, TEX // 2):
                f_ = TEX // res
                x0 = np.floor(uve_[:, 0] * res - 0.5).astype(np.int64)
                y0 = np.floor(uve_[:, 1] * res - 0.5).astype(np.int64)
                for dx in (0, 1):
                    for dy in (0, 1):
                        xx = np.clip(x0 + dx, 0, res - 1)
                        yy = np.clip(y0 + dy, 0, res - 1)
                        for ex in range(f_):
                            for ey in range(f_):
                                np.add.at(acc_, (yy * f_ + ey, xx * f_ + ex), ziel_[ev_])
                                np.add.at(cnt_, (yy * f_ + ey, xx * f_ + ex), 1.0)
                                np.bitwise_or.at(seite_, (yy * f_ + ey, xx * f_ + ex), np.where(vorn_k[ev_], 1, 2).astype(np.int8))
            km_ = cnt_ > 0
            vor_ = col[km_].copy()
            col[km_] = np.minimum(col[km_], (acc_[km_] / cnt_[km_][:, None]).astype(np.float32))
            log("2C Krallen dunkler: Schalen %d, Texel %d (vorn+hinten gemischt %d), Mittel sRGB vorher %s -> nachher %s" % (
                len(np.unique(schale_)), int(km_.sum()), int((seite_ == 3).sum()), (vor_.mean(0) * 255).round(0).tolist(),
                (col[km_].mean(0) * 255).round(0).tolist()))
    for x0, y0, w_, h_ in E["SPERR_FLECKEN"]:
        ys = slice(TEX - 2 * (y0 + h_), TEX - 2 * y0)
        xs = slice(2 * x0, 2 * (x0 + w_))
        assert int(maske[ys, xs].sum()) == 0
    log("Flecken Gaumen/Zunge/Zahn frei")
    log("Textur Mittel sRGB", (col[maske].mean(0) * 255).round(1))
    aus = TX + "NCBear_%s_2048.png" % AUSNAME
    png_schreiben(aus, col)
    log("Textur", aus)
    # ---------------------------------------------------------- Messdaten fuer mess_textur.py
    np.savez_compressed(TX + "mess/texel_%s.npz" % AUSNAME, my=my.astype(np.int16), mx=mx.astype(np.int16), region=region, gegend=gegend[tt].astype(np.int8),
                        sohle=sohle_t[tt].astype(np.int8), N=Nn.astype(np.float32), P=E["h2f"](P).astype(np.float32), lum=lum_t.astype(np.float32),
                        streu=streu_t.astype(np.float32), gesehen=gesehen, gut=gut, kopf_maske=kopf_maske.astype(np.float32),
                        zw=zw.astype(np.float32), P0=E["h2f"](P0).astype(np.float32), dk=dk.astype(np.float32),
                        **{"sohle_%s_%s" % (pn_, k_): v_ for pn_, d_ in SOHLE_MESS.items() for k_, v_ in d_.items()})
    json.dump(dict(fit=fit, farbabgleich=fak.tolist(), param=dict(P_EXP=P_EXP, A_REF=A_REF, UNTEN=UNTEN_LIFT, BEIN=BEIN_LIFT, STRAEHNE=STR_AMP,
                                                                  AO=AO_K, SCHAERFE=SCHAERFE, NUR_NEU=NUR_NEU, KONTRAST=KONTRAST_D,
                                                                  K_SEITE=K_SEITE, INNEN_TOL=INNEN_TOL, INNEN_W=INNEN_W, POSE_W=POSE_W,
                                                                  POSE_HINTEN=POSE_HINTEN, POSE_VORN=POSE_VORN, NAHT=(NAHT_A, NAHT_B, NAHT_C),
                                                                  C2C=C2C, FELD=FELD, feld=kz_feld, H_LEDER_L=H_LEDER_L, H_DOM0=H_DOM0,
                                                                  H_FURCHE_L=H_FURCHE_L, HALS_F=HALS_F, HALS_FARBE=HALS_FARBE, HALS_FEIN=HALS_FEIN,
                                                                  BEHANG_HUB=BEHANG_HUB, BEHANG_SCHATTEN=BEHANG_SCHATTEN),
                   ansichten=[v["pfad"] for v in views]), open(TX + "mess/backen_%s.json" % AUSNAME, "w"), indent=1)
    if not NUR_NEU:
        kopf_variante(E, Q, col, maske, my, mx, tt, gegend, P)
    log("BACKEN_OK")


def kopf_variante(E, Q, col, maske, my, mx, tt, gegend, P):
    """Nur zum Vergleich (Kevin waehlt): Augen sichtbar (dunkle Mandel statt Schlitz, Lidrand, leichter Hoehlenschatten) und Gesicht
    etwas dunkler. Gleiche Textur, nur Kopf-Texel geaendert; die Vorgabe bleibt die alte Kopf-Textur."""
    TEX = E["TEX"]
    kopf_t = gegend[tt] == 1
    Pk = P[kopf_t]
    L = Q["w2l"](Pk)
    a, b, c = L[:, 0], L[:, 1], L[:, 2]
    B = np.abs(b)
    hb = Q["huelle_basis"](a, b, c)
    kopf = (hb < 0.03).astype(np.float64)
    x, y, z = Q["_acht"](a, B, c, Q["AUGE"], Q["AU"], Q["AV"], Q["AW"])
    sp = Q["spalt2d"](y * 0.92, z * 0.80)          # Spalte groesser: offenes Auge statt Schlitz
    vorn = sst(-0.022, -0.005, x) * kopf
    auge = (1.0 - sst(0.0010, 0.0042, sp)) * vorn
    lid = (1.0 - sst(0.0042, 0.0105, sp)) * vorn * (1.0 - auge)
    hoehle = (1.0 - sst(0.008, 0.034, np.sqrt(y * y + z * z))) * vorn
    R = Q["regionen"](a, b, c)
    gesicht = sst(0.02, 0.22, a) * kopf * (1.0 - R["innen"])
    S = col[my[kopf_t], mx[kopf_t]].astype(np.float64)
    S = S * (1.0 - 0.13 * gesicht)[:, None]
    S = S * (1.0 - 0.22 * hoehle)[:, None]
    S = S * (1.0 - 0.55 * lid)[:, None]
    iris = np.array((0.055, 0.034, 0.022)) * (1.0 + 0.6 * sst(0.0035, 0.0005, -sp))[:, None]
    S = S * (1.0 - auge[:, None]) + iris * auge[:, None]
    neu = col.copy()
    neu[my[kopf_t], mx[kopf_t]] = np.clip(S, 0, 1).astype(np.float32)
    # Rand der Kopf-Inseln (6 px, dort liegen in der Vorgabe dieselben alten Texel): Verhaeltnis neu/alt der Nachbarn mitnehmen,
    # sonst bleibt an den UV-Naehten des Kopfes ein heller Saum
    R = np.ones_like(col)
    insel = np.zeros(maske.shape, dtype=bool)
    insel[my[kopf_t], mx[kopf_t]] = True
    R[insel] = neu[insel] / np.maximum(col[insel], 1e-4)
    rand = wachsen(insel, 6) & ~insel & ~wachsen(maske & ~insel, 2)
    frei = rand.copy()
    E["fuellen"](R, frei, rand, 8)
    neu[rand] = np.clip(col[rand] * R[rand], 0, 1)
    png_schreiben(TX + "NCBear_kopf_variante.png", neu)
    log("Kopf-Variante: Texel geaendert %d (Auge %d, Lidrand %d)" % (int((np.abs(neu - col).sum(2) > 1e-4).sum()), int((auge > 0.5).sum()), int((lid > 0.5).sum())))


if ARGS[0].endswith(".json"):
    AUF = json.load(open(ARGS[0]))
    if AUF["stufe"] == "ansichten":
        stufe_ansichten(AUF)
    else:
        raise SystemExit("Stufe %r unbekannt" % AUF["stufe"])
elif ARGS[0] == "backen":
    stufe_backen()
else:
    raise SystemExit("Stufe %r gibt es hier nicht" % ARGS[0])
