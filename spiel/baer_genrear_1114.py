# -*- coding: utf-8 -*-
# Lauf baer-gen-rear-bauch (14.11.2026), Rolle BAUER A: der Generator-Baer (NCBearGen.glb, Aussehen "Brown" und "Natural") bekommt das neue
# Aufrichten/Bruellen NCBear_Rear des Klassisch-Baeren (NCBear.glb). Kevin 13.11. ~22:35, woertlich: "ja uebertrag die version auf den".
# NEU (kein Original geaendert). Reines Python/numpy, kein Blender. Importiert den Kern baer_kern_liegen.py (Lauf baer-liegen, im selben
# Ordner, wird NICHT geaendert): GLB lesen, Rig/FK/Haut, teile(), paar() (Windungszahl), Drehungen.
#
# Was passiert (PLAN.md 2.4, _arbeit/baer_modell_1114/):
#   1. Pruefen: Skelett beider GLB gleich (Knotennamen ausser dem Netz-Knoten, Eltern, Ruhe-TRS, Skin-Liste, inverse Bind byte-gleich);
#      in NCBear_Rear gleiche Kanaele, Zeit-Bytes und Interpolation, gleich lange Ausgaben; die Rear-Ausgaben des Generator-GLB werden
#      von KEINEM anderen Clip, Netz oder Skin benutzt und haben keinen byteStride. Sonst REAR_GEN_FEHLER, Code 2, nichts geschrieben.
#   2. Rear-Werte des Klassisch-GLB AN ORT UND STELLE ins BIN des Generator-GLB (JSON bleibt byte-gleich, alle anderen Bytes auch).
#   3. --arm VOR,AUS: nur die Rotation von Bip01_L/R_UpperArm neu -- Oberarm an der Schulter um die Welt-Querachse VOR Grad nach vorn und
#      um die Welt-Laengsachse AUS Grad nach aussen (L/R gespiegelt), weich ein 0,30-0,55 s, aus 2,25-2,45 s; ausserhalb (Bild 0..8 und
#      74..90) bleiben die Bytes die des Klassisch-Clips. Grund: am dickeren Generator-Netz stecken die Unterarme im 1:1-Clip bis 10,0 cm
#      in der Brust (Klassisch 2,9 cm). Vorgabe PLAN 12,8; der Bau hat ueber ALLE 91 Bilder 12..20 / 8..14 gerastert (--scan) und die
#      kleinste Drehung genommen, die A3 erfuellt -> VORGABE_ARM unten (14,8).
# (Der PLAN nannte das Skript baer_rear_gen_1114.py; der Bau-Auftrag baer_genrear_1114.py -- es gibt nur diese Datei.)
#   4. Selbstpruefung: JSON byte-gleich zum Generator-Eingang; BIN ausserhalb der Rear-Ausgaben byte-gleich; Rear-Ausgaben = Klassisch-Rear
#      bis auf UpperArm L/R-Rotation, diese nur in Bildern mit Gewicht > 0 anders; Bild 0 und 90 gleich.
#   5. Abnahme A3/A4 (PLAN 2.5) an ALLEN 91 Bildern auf dem Generator-Netz (Groesse 1; im Spiel x1,35), sonst Code 2 und nichts geschrieben.
#   6. Schreiben ueber AUS.tmp -> AUS. Ende "REAR_GEN_OK MD5 <md5> <AUS>". Zweimal gebaut (auch auf dem eigenen Ergebnis) = gleiche MD5.
#
# Aufruf (Pfade frei; EIN = Ordner der geltenden GLB, wird nur gelesen):
#   python baer_genrear_1114.py EIN/NCBear.glb EIN/NCBearGen.glb AUS/NCBearGen.glb [--arm VOR,AUS] [--bericht B.json] [--jobs N]
#   python baer_genrear_1114.py --scan EIN/NCBear.glb EIN/NCBearGen.glb VOR1,VOR2,.. AUS1,AUS2,..   (nur messen, schreibt nichts)
#   python baer_genrear_1114.py --mess GLB [B.json]   (A3/A4-Messung von NCBear_Rear eines GLB an seinem eigenen Netz, schreibt nur B.json)
#   python baer_genrear_1114.py --pruefe KLASSISCH.glb GENERATOR_ALT.glb NEU.glb   (Beweis "nur Rear, nur UpperArm anders als Klassisch")
# SCHREIBSCHUTZ: schreibt nie auf einen Eingang und nie in einen Mod-/Spielordner (.../Zomboid/mods/..., .../steamapps/...).
# Statisch gerechnet, nicht gespielt.
import hashlib
import json
import math
import multiprocessing as mp
import os
import struct
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baer_kern_liegen as K  # noqa: E402

CLIP = "NCBear_Rear"
ARME = ("Bip01_L_UpperArm", "Bip01_R_UpperArm")
VORGABE_ARM = (14.0, 8.0)          # Grad vor / aus; Bau-Scan 14.11. ueber ALLE 91 Bilder (gen_rear/mess/scan1.txt): 12/8 aus dem PLAN
#                                    verfehlt A3 in Bild 64-66 (3,40 cm, 37 Punkte); kleinste Drehung mit A3 im Raster 12..20 / 8..14 = 14/8
EIN_AUS = (0.30, 0.55, 2.25, 2.45)  # weich ein (s) / weich aus (s), wie PLAN 2.3
QUER = np.array((1.0, 0.0, 0.0))   # glTF +x = Tier links (Querachse)
LANG = np.array((0.0, 0.0, 1.0))   # glTF +z = Tier vorn (Laengsachse)
# Abnahme (PLAN 2.5), Netz-Masse Groesse 1, cm
A3 = dict(arm_tiefe_cm=3.0, arm_punkte_je_seite=30, boden_cm=-0.5)
A4 = dict(hals995=1.80, halsmax=2.10, dehn995=2.20, riss_cm=0.50, riss_hals_cm=0.0)
NULL_PAARE = (("kopf", "rumpf"), ("pfote_VL", "kopf"), ("pfote_VR", "kopf"), ("pfote_VL", "pfote_VR"), ("bein_VL", "bein_HL"),
              ("bein_VR", "bein_HR"))


# ------------------------------------------------------------------ Hilfen
def md5b(b):
    return hashlib.md5(b).hexdigest()


def _norm(p):
    return os.path.normcase(os.path.abspath(p)).replace("\\", "/")


def schreibschutz(eingaenge, *ziele):
    f = []
    for z in ziele:
        if not z:
            continue
        zn = _norm(z)
        for e in eingaenge:
            gleich = zn == _norm(e)
            if not gleich and os.path.exists(z) and os.path.exists(e):
                try:
                    gleich = os.path.samefile(z, e)
                except OSError:
                    gleich = False
            if gleich:
                f.append("AUS %s ist ein Eingang -- Eingaenge werden nur gelesen" % z)
        if "/zomboid/mods/" in zn + "/" or "/steamapps/" in zn + "/":
            f.append("AUS %s liegt in einem Mod-/Spielordner -- dieses Skript schreibt nie dorthin (Einbau macht der Integrator)" % z)
    return f


def bin_start(raw):
    n = struct.unpack("<I", raw[12:16])[0]
    return 20 + n + 8


def anim(J, name):
    for a in J["animations"]:
        if a.get("name") == name:
            return a
    raise KeyError(name)


def nutzer(J):
    """Accessor -> Menge der Benutzer (Clip-Namen, NETZ, SKIN)."""
    u = {}
    for an in J["animations"]:
        for s in an["samplers"]:
            for k in ("input", "output"):
                u.setdefault(s[k], set()).add(an["name"])
    for m in J["meshes"]:
        for p in m["primitives"]:
            for v in list(p["attributes"].values()) + ([p["indices"]] if "indices" in p else []):
                u.setdefault(v, set()).add("NETZ")
    for sk in J.get("skins", []):
        if "inverseBindMatrices" in sk:
            u.setdefault(sk["inverseBindMatrices"], set()).add("SKIN")
    return u


def acc_lage(J, i):
    """(Byte-Anfang im BIN, Laenge) eines dicht gepackten Accessors."""
    a = J["accessors"][i]
    v = J["bufferViews"][a["bufferView"]]
    k = K.NC[a["type"]]
    sz = np.dtype(K.CT[a["componentType"]]).itemsize
    return v.get("byteOffset", 0) + a.get("byteOffset", 0), a["count"] * k * sz, ("byteStride" in v and v["byteStride"] != k * sz)


# ------------------------------------------------------------------ 1. Pruefen
def pruefe_eingang(JA, BA, JG, BG):
    f = []
    na, ng = JA["nodes"], JG["nodes"]
    if len(na) != len(ng):
        return ["Knotenzahl %d / %d" % (len(na), len(ng))]
    netz_a = {i for i, n in enumerate(na) if "mesh" in n}
    for i, (x, y) in enumerate(zip(na, ng)):
        for k in ("translation", "rotation", "scale", "children", "matrix", "skin", "mesh"):
            if x.get(k) != y.get(k):
                f.append("Knoten %d %s: %s verschieden" % (i, x.get("name"), k))
        if i not in netz_a and x.get("name") != y.get("name"):
            f.append("Knoten %d Name %s / %s" % (i, x.get("name"), y.get("name")))
    if JA["skins"][0]["joints"] != JG["skins"][0]["joints"]:
        f.append("Skin-Liste verschieden")
    if K.acc_bytes(JA, BA, JA["skins"][0]["inverseBindMatrices"]) != K.acc_bytes(JG, BG, JG["skins"][0]["inverseBindMatrices"]):
        f.append("inverse Bind nicht byte-gleich")
    ra, rg = anim(JA, CLIP), anim(JG, CLIP)
    if ra["channels"] != rg["channels"]:
        f.append("Rear: Kanal-Liste verschieden")
        return f
    u = nutzer(JG)
    for ch in rg["channels"]:
        sa, sg = ra["samplers"][ch["sampler"]], rg["samplers"][ch["sampler"]]
        if K.acc_bytes(JA, BA, sa["input"]) != K.acc_bytes(JG, BG, sg["input"]):
            f.append("Rear: Zeit-Bytes verschieden (Knoten %d %s)" % (ch["target"]["node"], ch["target"]["path"]))
        if sa.get("interpolation") != sg.get("interpolation"):
            f.append("Rear: Interpolation verschieden (Knoten %d %s)" % (ch["target"]["node"], ch["target"]["path"]))
        aa, ag = JA["accessors"][sa["output"]], JG["accessors"][sg["output"]]
        if (aa["count"], aa["type"], aa["componentType"]) != (ag["count"], ag["type"], ag["componentType"]):
            f.append("Rear: Ausgabe-Form verschieden (Knoten %d %s)" % (ch["target"]["node"], ch["target"]["path"]))
            continue
        if K.acc_bytes(JA, BA, sa["output"]) != K.acc_bytes(JG, BG, sg["output"]) or \
                (ch["target"]["path"] == "rotation" and JG["nodes"][ch["target"]["node"]].get("name") in ARME):
            if u.get(sg["output"]) != {CLIP}:
                f.append("Rear-Ausgabe %d (Knoten %d %s) wird mitbenutzt von %s" % (sg["output"], ch["target"]["node"], ch["target"]["path"],
                                                                                   sorted(u.get(sg["output"], ()))))
            if acc_lage(JG, sg["output"])[2]:
                f.append("Rear-Ausgabe %d hat byteStride" % sg["output"])
    return f


# ------------------------------------------------------------------ 3. Arm-Umrechnung
def gewicht_zeit(t):
    a0, a1, b0, b1 = EIN_AUS
    return K.ssf(a0, a1, t) * (1.0 - K.ssf(b0, b1, t))


def rot(ax, g):
    ax = np.asarray(ax, float) / np.linalg.norm(ax)
    g = math.radians(g)
    Kx = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(g) * Kx + (1 - math.cos(g)) * Kx @ Kx


def arm_umrechnen(rig, c, vor, aus):
    """c = rig.clip(CLIP) (Klassisch-Werte). Liefert {Knotenindex: (n,4) float32 neue Quaternionen} und je Bild das Gewicht.
    Oberarm-Weltdrehung neu = Rw x alt (Rw um die Schulter, Welt-Achsen glTF), lokal: Rp^T Rw Rp q. Bilder mit Gewicht 0 behalten die
    Klassisch-Werte bit-gleich; Vorzeichen jeder neuen Quaternion wie die alte (kein Sprung fuer die lineare Abtastung)."""
    n = len(c["T"])
    w = np.array([gewicht_zeit(float(t)) for t in c["T"]])
    neu = {}
    for i_name, sg in zip(ARME, (1.0, -1.0)):
        i = rig.ix[i_name]
        neu[i] = c["q"][:, i].astype(np.float32).copy()
    if vor == 0 and aus == 0:
        return neu, w
    for f in range(n):
        if w[f] <= 0.0:
            continue
        W = rig.welt(c["t"][f], c["q"][f], c["s"][f])
        for i_name, sg in zip(ARME, (1.0, -1.0)):
            i = rig.ix[i_name]
            p = rig.par[i]
            Rp = W[p][:3, :3] / np.linalg.norm(W[p][:3, :3], axis=0)
            Rw = rot(QUER, -vor * w[f]) @ rot(LANG, sg * aus * w[f])
            q0 = c["q"][f, i]
            q = K.mat_q(Rp.T @ Rw @ Rp @ K.q_mat(q0))
            if float(q @ q0) < 0:
                q = -q
            neu[i][f] = q.astype(np.float32)
    return neu, w


# ------------------------------------------------------------------ 2.+3. bauen (nur Bytes, ohne Abnahme)
def baue_bytes(pfad_k, pfad_g, vor, aus):
    JA, BA = K.lade_glb(pfad_k)
    raw = bytearray(open(pfad_g, "rb").read())
    JG, BG = K.lade_glb(pfad_g)
    fehler = pruefe_eingang(JA, BA, JG, BG)
    if fehler:
        return None, fehler, None
    b0 = bin_start(raw)
    ra, rg = anim(JA, CLIP), anim(JG, CLIP)
    info = dict(kanaele=len(rg["channels"]), anders_als_generator=[], arm=[vor, aus])
    for ch in rg["channels"]:
        sa, sg = ra["samplers"][ch["sampler"]], rg["samplers"][ch["sampler"]]
        a_out = K.acc_bytes(JA, BA, sa["output"])
        if a_out == K.acc_bytes(JG, BG, sg["output"]):
            continue
        o, ln, _ = acc_lage(JG, sg["output"])
        assert ln == len(a_out)
        raw[b0 + o:b0 + o + ln] = a_out
        info["anders_als_generator"].append("%s.%s" % (JG["nodes"][ch["target"]["node"]]["name"], ch["target"]["path"]))
    rig = K.Rig(pfad_k)
    c = rig.clip(CLIP)
    neu, w = arm_umrechnen(rig, c, vor, aus)
    for ch in rg["channels"]:
        node, path = ch["target"]["node"], ch["target"]["path"]
        if path != "rotation" or node not in neu:
            continue
        sg = rg["samplers"][ch["sampler"]]
        assert JG["accessors"][sg["output"]]["count"] == len(c["T"]), "UpperArm-Rotation nicht dicht abgetastet"
        assert K.acc_bytes(JG, BG, sg["input"]) == K.acc_bytes(JA, BA, ra["samplers"][ch["sampler"]]["input"])
        o, ln, _ = acc_lage(JG, sg["output"])
        b = np.ascontiguousarray(neu[node].astype("<f4")).tobytes()
        assert len(b) == ln
        raw[b0 + o:b0 + o + ln] = b
    info["bilder_mit_arm"] = [int(f) for f in np.nonzero(w > 0)[0]]
    info["zeit"] = [float(c["T"][0]), float(c["T"][-1]), int(len(c["T"]))]
    return bytes(raw), [], info


# ------------------------------------------------------------------ 4. Selbstpruefung
def pruefe_nur_rear(pfad_k, pfad_g, neu_bytes):
    """Beweis: JSON byte-gleich zum Generator-Eingang; jedes BIN-Byte ausserhalb der Rear-Ausgaben byte-gleich; Rear-Ausgaben = Klassisch,
    ausser UpperArm L/R-Rotation; diese nur in Bildern mit Gewicht > 0 anders, Bild 0 und letztes Bild gleich."""
    f = []
    rawg = open(pfad_g, "rb").read()
    JA, BA = K.lade_glb(pfad_k)
    JG, BG = K.lade_glb(pfad_g)
    n = struct.unpack("<I", rawg[12:16])[0]
    if neu_bytes[:20 + n + 8] != rawg[:20 + n + 8] or len(neu_bytes) != len(rawg):
        f.append("Kopf/JSON/Laenge nicht byte-gleich zum Generator-Eingang")
        return f, {}
    JN, BN = _lade(neu_bytes)
    ra, rg = anim(JA, CLIP), anim(JG, CLIP)
    maske = np.zeros(len(BG), dtype=bool)
    arm_anders = {}
    for ch in rg["channels"]:
        sg = rg["samplers"][ch["sampler"]]
        o, ln, _ = acc_lage(JG, sg["output"])
        maske[o:o + ln] = True
        nm = JG["nodes"][ch["target"]["node"]]["name"]
        a_k = K.acc_bytes(JA, BA, ra["samplers"][ch["sampler"]]["output"])
        a_n = K.acc_bytes(JN, BN, sg["output"])
        if ch["target"]["path"] == "rotation" and nm in ARME:
            vk = np.frombuffer(a_k, "<f4").reshape(-1, 4)
            vn = np.frombuffer(a_n, "<f4").reshape(-1, 4)
            anders = np.nonzero((vk != vn).any(1))[0]
            arm_anders[nm] = [int(x) for x in anders]
            T = K.acc_arr(JA, BA, ra["samplers"][ch["sampler"]]["input"])[:, 0]
            for fr in anders:
                if gewicht_zeit(float(T[fr])) <= 0.0:
                    f.append("%s Bild %d anders, obwohl Gewicht 0" % (nm, fr))
            if 0 in anders or len(vk) - 1 in anders:
                f.append("%s: Bild 0 oder letztes Bild anders" % nm)
        elif a_k != a_n:
            f.append("Rear %s.%s nicht byte-gleich zum Klassisch-Clip" % (nm, ch["target"]["path"]))
        if K.acc_bytes(JN, BN, sg["input"]) != K.acc_bytes(JG, BG, sg["input"]):
            f.append("Rear %s.%s Zeit-Bytes geaendert" % (nm, ch["target"]["path"]))
    BNa, BGa = np.frombuffer(BN, np.uint8), np.frombuffer(BG, np.uint8)
    aussen = int((BNa[~maske] != BGa[~maske]).sum())
    if aussen:
        f.append("%d Bytes ausserhalb der Rear-Ausgaben geaendert" % aussen)
    # andere Clips je Sampler byte-gleich (folgt aus aussen == 0 und JSON gleich; zur Sicherheit gezaehlt)
    gleich = alle = 0
    for a1, a2 in zip(JG["animations"], JN["animations"]):
        if a1["name"] == CLIP:
            continue
        for s1, s2 in zip(a1["samplers"], a2["samplers"]):
            alle += 2
            gleich += K.acc_bytes(JG, BG, s1["input"]) == K.acc_bytes(JN, BN, s2["input"])
            gleich += K.acc_bytes(JG, BG, s1["output"]) == K.acc_bytes(JN, BN, s2["output"])
    if gleich != alle:
        f.append("andere Clips: %d/%d Sampler-Puffer gleich" % (gleich, alle))
    return f, dict(json_gleich=True, bytes_aussen_geaendert=aussen, rear_bytes=int(maske.sum()), andere_clips=[gleich, alle], arm_bilder_anders=arm_anders)


def _lade(b):
    n = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + n])
    o = 20 + n
    bl = struct.unpack("<I", b[o:o + 4])[0]
    return J, b[o + 8:o + 8 + bl]


# ------------------------------------------------------------------ 5. Messen (alle Bilder, mehrere Prozesse)
_W = {}


def _init(pfad_netz):
    rig = K.Rig(pfad_netz)
    T = K.teile(rig)
    G = rig.gewichte()
    F = rig.F
    E = np.unique(np.sort(np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]], 1), axis=0)
    R0 = K.g2t(rig.P)
    L0 = np.linalg.norm(R0[E[:, 0]] - R0[E[:, 1]], axis=1)
    ok = (L0 > 0.004) & ~(T["kopf"][E[:, 0]] | T["kopf"][E[:, 1]])
    kh = T["kopf"] | T["hals"]
    band = (L0 > 0.002) & ((kh[E[:, 0]] & T["rumpf"][E[:, 1]]) | (kh[E[:, 1]] & T["rumpf"][E[:, 0]]) | (T["kopf"][E[:, 0]] ^ T["kopf"][E[:, 1]]))
    key = np.round(rig.P / 1e-5).astype(np.int64)
    _, inv, cnt = np.unique(key, axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    pp = np.array([(g[0], k) for g in (np.nonzero(inv == q)[0] for q in np.nonzero(cnt > 1)[0]) for k in g[1:]], dtype=int).reshape(-1, 2)
    jaw = G[:, rig.ix["Bip01_Jaw"]]
    neck = G[:, rig.ix["Bip01_Neck"]]
    maul = np.abs(jaw[pp[:, 0]] - jaw[pp[:, 1]]) > 0.05 if len(pp) else np.zeros(0, bool)
    hals = (~maul) & ((neck[pp[:, 0]] > 0.01) | (neck[pp[:, 1]] > 0.01)) if len(pp) else np.zeros(0, bool)
    _W.update(rig=rig, T=T, E=E, L0=L0, ok=ok, band=band, pp=pp, maul=maul, hals=hals)


def _bild(arg):
    f, t, q, s, voll = arg
    rig, T = _W["rig"], _W["T"]
    P = rig.haut_tier(rig.welt(t, q, s))
    r = dict(bild=int(f))
    for sd in ("VL", "VR"):
        p = K.paar(P, rig.F, T["unten_" + sd] | T["pfote_" + sd], T["rumpf"])
        r["arm_" + sd] = [p["a_in_b"] + p["b_in_a"], p["tiefe_cm"]]
    if not voll:
        return r
    for a, b in NULL_PAARE:
        p = K.paar(P, rig.F, T[a], T[b])
        r[a + "|" + b] = p["a_in_b"] + p["b_in_a"]
    E, L0 = _W["E"], _W["L0"]
    L1 = np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1) / np.maximum(L0, 1e-9)
    r["dehn"] = [round(float(np.percentile(L1[_W["ok"]], 99.5)), 3), round(float(L1[_W["ok"]].max()), 3)]
    r["hals"] = [round(float(np.percentile(L1[_W["band"]], 99.5)), 3), round(float(L1[_W["band"]].max()), 3)]
    pp = _W["pp"]
    if len(pp):
        d = np.linalg.norm(P[pp[:, 0]] - P[pp[:, 1]], axis=1)
        r["riss_ohne_maul_cm"] = round(100 * float(d[~_W["maul"]].max()), 3) if (~_W["maul"]).any() else 0.0
        r["riss_hals_cm"] = round(100 * float(d[_W["hals"]].max()), 3) if _W["hals"].any() else 0.0
    r["boden_cm"] = round(100 * float(P[:, 2].min()), 2)
    return r


def messe(pfad_netz, c, q=None, voll=True, jobs=None, pool=None):
    """Misst alle Bilder des Clips c (Rig.clip) am Netz von pfad_netz; q ersetzt die Drehungen (n, nn, 4), falls gegeben."""
    q = c["q"] if q is None else q
    args = [(f, c["t"][f], q[f], c["s"][f], voll) for f in range(len(c["T"]))]
    eigen = pool is None
    if eigen:
        pool = mp.Pool(jobs or min(24, mp.cpu_count()), initializer=_init, initargs=(pfad_netz,))
    try:
        out = pool.map(_bild, args)
    finally:
        if eigen:
            pool.close()
            pool.join()
    return out


def zusammen(m):
    z = dict(arm_tiefe_cm=max(max(r["arm_VL"][1], r["arm_VR"][1]) for r in m),
             arm_punkte=[max(r["arm_VL"][0] for r in m), max(r["arm_VR"][0] for r in m)],
             arm_bild_tiefst=max(m, key=lambda r: max(r["arm_VL"][1], r["arm_VR"][1]))["bild"])
    if "dehn" in m[0]:
        for a, b in NULL_PAARE:
            z[a + "|" + b] = max(r[a + "|" + b] for r in m)
        z["dehn995"] = max(r["dehn"][0] for r in m)
        z["dehnmax"] = max(r["dehn"][1] for r in m)
        z["hals995"] = max(r["hals"][0] for r in m)
        z["halsmax"] = max(r["hals"][1] for r in m)
        z["riss_ohne_maul_cm"] = max(r.get("riss_ohne_maul_cm", 0.0) for r in m)
        z["riss_hals_cm"] = max(r.get("riss_hals_cm", 0.0) for r in m)
        z["boden_cm"] = min(r["boden_cm"] for r in m)
    return z


def abnahme(z):
    f = []
    if z["arm_tiefe_cm"] > A3["arm_tiefe_cm"]:
        f.append("A3 Unterarm/Pfote in Rumpf %.2f cm > %.1f" % (z["arm_tiefe_cm"], A3["arm_tiefe_cm"]))
    if max(z["arm_punkte"]) > A3["arm_punkte_je_seite"]:
        f.append("A3 Unterarm/Pfote in Rumpf %s Punkte je Seite > %d" % (z["arm_punkte"], A3["arm_punkte_je_seite"]))
    for a, b in NULL_PAARE:
        if z[a + "|" + b] > 0:
            f.append("A3 %s gegen %s: %d Punkte" % (a, b, z[a + "|" + b]))
    if z["boden_cm"] < A3["boden_cm"]:
        f.append("A3 tiefster Hautpunkt %.2f cm" % z["boden_cm"])
    if z["hals995"] > A4["hals995"] or z["halsmax"] > A4["halsmax"]:
        f.append("A4 Halsband %.2f / %.2f" % (z["hals995"], z["halsmax"]))
    if z["dehn995"] > A4["dehn995"]:
        f.append("A4 Dehnung ohne Kopf 99,5 %% %.2f" % z["dehn995"])
    if z["riss_ohne_maul_cm"] > A4["riss_cm"]:
        f.append("A4 Riss ohne Maul %.2f cm" % z["riss_ohne_maul_cm"])
    if z["riss_hals_cm"] > A4["riss_hals_cm"]:
        f.append("A4 Riss am Hals %.3f cm" % z["riss_hals_cm"])
    return f


# ------------------------------------------------------------------ Befehle
def _arg(a, k, d=None):
    if k in a:
        i = a.index(k)
        v = a[i + 1]
        del a[i:i + 2]
        return v
    return d


def bauen(pfad_k, pfad_g, aus, vor, aus_g, bericht=None, jobs=None):
    sperre = schreibschutz([pfad_k, pfad_g], aus, bericht, aus + ".tmp")
    if sperre:
        for x in sperre:
            print("REAR_GEN_FEHLER", x)
        raise SystemExit(2)
    neu, fehler, info = baue_bytes(pfad_k, pfad_g, vor, aus_g)
    if fehler:
        for x in fehler:
            print("REAR_GEN_FEHLER", x)
        raise SystemExit(2)
    f2, beweis = pruefe_nur_rear(pfad_k, pfad_g, neu)
    if f2:
        for x in f2:
            print("REAR_GEN_FEHLER Selbstpruefung:", x)
        raise SystemExit(2)
    os.makedirs(os.path.dirname(os.path.abspath(aus)), exist_ok=True)
    tmp = aus + ".tmp"
    open(tmp, "wb").write(neu)
    rig = K.Rig(tmp)
    m = messe(tmp, rig.clip(CLIP), jobs=jobs)
    z = zusammen(m)
    fa = abnahme(z)
    print("REAR_GEN Abnahme (alle %d Bilder, Groesse 1): Unterarm/Pfote in Rumpf %.2f cm (Bild %d), Punkte L/R %s; Kopf-Rumpf %d, Pfote-Kopf %d/%d, "
          "Pfote-Pfote %d, Bein V-H %d/%d; Halsband %.2f / %.2f; Dehnung ohne Kopf %.2f; Riss ohne Maul %.2f cm, am Hals %.3f cm; Boden %.2f cm"
          % (len(m), z["arm_tiefe_cm"], z["arm_bild_tiefst"], z["arm_punkte"], z["kopf|rumpf"], z["pfote_VL|kopf"], z["pfote_VR|kopf"],
             z["pfote_VL|pfote_VR"], z["bein_VL|bein_HL"], z["bein_VR|bein_HR"], z["hals995"], z["halsmax"], z["dehn995"], z["riss_ohne_maul_cm"],
             z["riss_hals_cm"], z["boden_cm"]))
    if fa:
        os.remove(tmp)
        for x in fa:
            print("REAR_GEN_FEHLER Abnahme:", x)
        raise SystemExit(2)
    os.replace(tmp, aus)
    h = md5b(neu)
    if bericht:
        json.dump(dict(klassisch=pfad_k, klassisch_md5=md5b(open(pfad_k, "rb").read()), generator=pfad_g,
                       generator_md5=md5b(open(pfad_g, "rb").read()), aus=aus, md5=h, bytes=len(neu), info=info, beweis=beweis,
                       abnahme=z, schwellen=dict(A3=A3, A4=A4), bilder=m), open(bericht, "w"), indent=1)
    print("REAR_GEN beweis: JSON byte-gleich, %d Bytes ausserhalb Rear geaendert, andere Clips %d/%d Sampler-Puffer gleich, Rear = Klassisch bis auf "
          "UpperArm (anders in Bild %s)" % (beweis["bytes_aussen_geaendert"], beweis["andere_clips"][0], beweis["andere_clips"][1],
                                           {k: "%d..%d (%d)" % (min(v), max(v), len(v)) if v else "-" for k, v in beweis["arm_bilder_anders"].items()}))
    print("REAR_GEN_OK MD5 %s %s" % (h, aus))
    return h


def scan(pfad_k, pfad_g, vors, auss, jobs=None):
    JA, BA = K.lade_glb(pfad_k)
    JG, BG = K.lade_glb(pfad_g)
    fehler = pruefe_eingang(JA, BA, JG, BG)
    if fehler:
        for x in fehler:
            print("REAR_GEN_FEHLER", x)
        raise SystemExit(2)
    rig = K.Rig(pfad_k)
    c = rig.clip(CLIP)
    pool = mp.Pool(jobs or min(24, mp.cpu_count()), initializer=_init, initargs=(pfad_g,))
    erg = []
    try:
        for v in vors:
            for a in auss:
                neu, w = arm_umrechnen(rig, c, v, a)
                q = c["q"].copy()
                for i, arr in neu.items():
                    q[:, i] = arr.astype(float)
                m = messe(pfad_g, c, q=q, voll=False, pool=pool)
                z = zusammen(m)
                ok = z["arm_tiefe_cm"] <= A3["arm_tiefe_cm"] and max(z["arm_punkte"]) <= A3["arm_punkte_je_seite"]
                erg.append((v, a, z, ok))
                print("SCAN vor %5.1f aus %5.1f | Tiefe %.2f cm (Bild %d) | Punkte L/R %s | A3-Arm %s | je Bild L/R: %s" % (
                    v, a, z["arm_tiefe_cm"], z["arm_bild_tiefst"], z["arm_punkte"], "ok" if ok else "NEIN",
                    " ".join("%d:%d/%d/%.1f" % (r["bild"], r["arm_VL"][0], r["arm_VR"][0], max(r["arm_VL"][1], r["arm_VR"][1]))
                             for r in m if r["arm_VL"][0] + r["arm_VR"][0] > 0)), flush=True)
    finally:
        pool.close()
        pool.join()
    gut = [e for e in erg if e[3]]
    if gut:
        b = min(gut, key=lambda e: (math.hypot(e[0], e[1]), e[2]["arm_tiefe_cm"]))
        print("SCAN kleinste Drehung mit A3-Arm: vor %.1f aus %.1f (Tiefe %.2f cm, Punkte %s)" % (b[0], b[1], b[2]["arm_tiefe_cm"], b[2]["arm_punkte"]))
    else:
        print("SCAN keine Drehung erfuellt A3-Arm")


def mess_glb(pfad, bericht=None, jobs=None):
    rig = K.Rig(pfad)
    m = messe(pfad, rig.clip(CLIP), jobs=jobs)
    z = zusammen(m)
    print("MESS %s: %s" % (pfad, json.dumps(z)))
    print("MESS Abnahme A3/A4:", abnahme(z) or "erfuellt")
    if bericht:
        json.dump(dict(glb=pfad, md5=md5b(open(pfad, "rb").read()), abnahme=z, bilder=m), open(bericht, "w"), indent=1)


def main():
    a = sys.argv[1:]
    jobs = _arg(a, "--jobs")
    jobs = int(jobs) if jobs else None
    if a and a[0] == "--scan":
        scan(a[1], a[2], [float(x) for x in a[3].split(",")], [float(x) for x in a[4].split(",")], jobs)
        return
    if a and a[0] == "--mess":
        mess_glb(a[1], a[2] if len(a) > 2 else None, jobs)
        return
    if a and a[0] == "--pruefe":
        neu = open(a[3], "rb").read()
        f, b = pruefe_nur_rear(a[1], a[2], neu)
        print("PRUEFE", "ok" if not f else "FEHLER", json.dumps(b), f)
        raise SystemExit(2 if f else 0)
    arm = _arg(a, "--arm")
    bericht = _arg(a, "--bericht")
    if len(a) != 3:
        print(__doc__ or "", "Aufruf: python baer_genrear_1114.py KLASSISCH.glb GENERATOR.glb AUS.glb [--arm VOR,AUS] [--bericht B.json] [--jobs N]")
        raise SystemExit(1)
    vor, aus_g = (float(x) for x in arm.split(",")) if arm else VORGABE_ARM
    bauen(a[0], a[1], a[2], vor, aus_g, bericht, jobs)


if __name__ == "__main__":
    main()
