# Lauf baer-rig-junges (11.11.2026), Rolle CLIPS+EXPORT: Kopie von baer_kampf_junges.py (Original unveraendert; Zeilen 1-1702 von dort,
# geaenderte Stellen tragen "RIG"). Quelle der FUENF neuen Clips des Generator-Jungen NCBearCub (RIG_PLAN.md 5.2-5.4):
#   DeerStag_Walk = Trab (3 Zyklen in 0,9 s), DeerStag_Run = Galopp (2 Zyklen in 0,5333 s), NCBear_SitDown/_Sit/_StandUp = S_J.
# Gelenke aus rig/skelett/skelett_rig.json (ruhe_m, Skelettrahmen). Ausgabe nur Posen (kein Netz, kein Rig, kein Export):
#   NCB_RIG_AUS=clips_neu_posen.npz [NCB_JUNGES_SITZ=sitz_par.json] [NCB_RIG_GANG=gang_par.json]
#   blender --background --factory-startup --python baer_clips_rig.py -- x
# Je Clip <Clip>_Q (Bilder x Knochen x 4, Weltdrehung gegen die Ruhe w x y z), <Clip>_P (Gelenklage, tier-Meter), dazu fuer Walk/Run
# <Clip>_u (Bilder x 4 Phase je Bein VL VR HL HR, Stuetze wenn u < duty) und <Clip>_weg (Translation_Data-Ende in E). Statisch gerechnet,
# nicht gespielt. Weder Test-Mod noch NPC Crew werden gelesen oder beschrieben.
#
# Lauf baer-junges (10.11.2026), Bau Koerper: Kopie von baer_kampf_2c.py (Original unveraendert), erzeugt von
# _arbeit/baer_junges/werkzeug/patch/mache_kampf_junges.py. NUR Quelle der drei Sitz-Clips des Baeren-Jungen NCBearCub (SPEZ_JUNGES D.4):
# die parametrischen Sitz-Spuren von 2c (_pose_s2c, sp_setzen_2c, sp_sitzen_2c, sp_aufstehen_2c) laufen mit den Gelenken des Jungen
# (BONES aus koerper/skelett.json) und der Soll-Pose S_J; abgetastet an denselben Zeiten. Geaenderte Stellen tragen "JUNGES".
# Aufruf: NCB_JUNGES_AUS=posen.npz [NCB_JUNGES_SITZ=par.json] [NCB_JUNGES_SKELETT=skelett.json] [NCB_JUNGES_ERW=1]
#         blender --background --factory-startup --python baer_kampf_junges.py -- x
# Ohne NCB_JUNGES_AUS liefe der Rest des Erwachsenen-Skripts (Netz, Rig, Export) -- dafuer ist diese Kopie NICHT gedacht.
# Lauf baer-2c (10.11.2026): Kopie von baer_kampf_pfote.py (Original unveraendert). Bau Koerper aendert NUR gewichte_eigen (mit "2c"
# kommentiert); Vorgabe-Quelle _arbeit/baer_2c/mod/42/media/, Gewichte _arbeit/baer_2c/netz/gewichte_2c.npz. Bau Sitzen (Bericht
# _arbeit/baer_2c/bau_sitzen.md): nur NCBear_SitDown/_Sit/_StandUp neu (SITZ_2C, sp_*_2c, _ferse_weg, Sitz-Grenze Kopf gegen Hals +60);
# die 12 anderen Clips, Knochen, Bind und Netz bit-gleich. Bau Gebiss: Maul-Inneres und Flecken aus baer_maul_2c.py (Aufruf bei
# netz_ersetzen und flecken_malen), sonst nichts geaendert.
# Lauf baer-pfoten (09.11.2026): Kopie von baer_kampf_fell.py (Original bleibt). Clips, Knochen, Bind Zeile fuer Zeile gleich.
# Neu: Vorgabe-Quelle _arbeit/baer_pfote/mod/42/media/; Gewichte aus NCB_PFOTE_GEWICHTE (sonst NCB_FELL_GEWICHTE, Vorgabe
# _arbeit/baer_pfote/netz/gewichte_pfote.npz, 'formel' = Formel); Formel mit Fussruecken-Korrektur (SPEZ_PFOTEN.md 2.2): vor dem
# Sprung-/Handgelenk gehoert der Fussruecken bis z 0,10-0,16 dem Fuss/der Hand (vorher nur nach Hoehe 5,5-17,5 cm).
# Vorgaenger (baer-fell): Kopie von baer_kampf_anim.py fuer den Lauf baer-fell (Original bleibt): Netz und Gewichte neu, Clips Zeile fuer Zeile gleich.
# Quelle der Figur (Argument 2) als Vorgabe: _arbeit/baer_fell/mod/42/media/ (WorldItems/NCBear.fbx + WorldItems/NCBear.png).
# Kopie von baer_kampf.py fuer den Lauf baer-anim (Original bleibt): liest das runde Spielnetz aus baer_export_anim.py.
# Aenderungen: (1) Quelle der Figur waehlbar (Argument 2, Ordner unter dem models_X/WorldItems/NCBear.fbx und
# textures/WorldItems/NCBear.png liegen; ohne Argument das runde Netz aus dem Lauf baer-anim). (2) Die Liegehoehe der
# Sterbe-Clips (boden_liege) haengt am Netz; damit sich die alten Clips nicht bewegen, wird sie aus einer Datei gelesen
# (Argument 3), die ein Lauf mit dem ALTEN Netz geschrieben hat. Knochen und Formeln sind unveraendert, nur die Gewichte
# kommen neu aus dem neuen Netz.
# Aufruf: blender --background --factory-startup --python baer_kampf_anim.py -- ZIELORDNER [QUELLE_MEDIA] [LIEGE.json] [BERICHT.json]
# Lauf baer-anim, Animator (08.11.2026): alle Kampfclips neu (Hieb L/R, Doppelschlag, Aufrichten, Biss am Boden) und neu der
# Biss gegen Stehende, Hinsetzen, Sitzen (Schleife), Aufstehen, Fressen (Schleife); Dauern nach anim_spez.md 7. Jede Taste wird
# gegen feste Gelenkgrenzen geklemmt und gemessen (GRENZEN), Pfote in der Luft relativ zum Unterarm, Arme in der Luft im
# Gelenkraum (fk_). Gewichte: Brust unter dem Hals gehoert der Brust (rumpf_anteile), Brustunterseite zwischen den Vorderbeinen
# mehr geglaettet (BRISKET). Idle/Walk/Run/Death/Dead unveraendert (Abweichung 0). Bericht: anim_clips.md.
# Fixer (08.11.2026, anim_review_optik.md / anim_review_technik.md, Bericht anim_fix.md): Hieb trifft vor der Schulter statt
# durch den eigenen Kiefer, Kopf dreht weg, Rumpf und Hinterbeine schieben; Doppelschlag mit Pranken vor der Brust statt neben dem
# Gesicht, Hinterbeine laden und schieben; Biss mit flachem Satz statt Arme hochreissen; Bodenbiss mit Pranke weiter aussen;
# Sitzen mit Hinterbeinen wirklich vorn und gespreizt, Hinterfuss in Welt (kein Rollen der Sohle), neue Reihenfolge beim Hinsetzen
# und Aufstehen; neue feste Pruefung "Sohle rollt" (SOHLE_GRENZE); Vorschau-Pose (b) nur mit NCB_VORSCHAU_SITZ_B.
# Baer als lebendes Tier mit Kampfclips (Project Zomboid B42.21): Kopie von baer_tier.py, das Original bleibt.
# Dazu: Unterkiefer (Bip01_Jaw), das Maul aufgeschnitten mit dunkler Mundhoehle und Fangzaehnen (ein Netz, ein Material),
# fuenf Kampfclips nach kampf_spez.md 5.5 (NCBear_Rear, _SwipeL, _SwipeR, _Slam, _Maul). Die fuenf alten Clips werden mit
# genau denselben Formeln gerechnet wie in baer_tier.py; der Kiefer steht in ihnen zu. NCBearDeer.glb wird hier nicht gebaut.
# Aufruf: blender --background --factory-startup --python baer_kampf.py -- ZIELORDNER
#   schreibt ZIELORDNER/42/media/models_X/Skinned/NCBear.glb und .../textures/Body/NCBear.png (mit drei Flecken fuer das Maul)
#
# Herkunft: baer_tier.py baut aus dem fertigen Spielnetz die zwei GLB-Dateien und die Koerpertextur.
#   NCBear.glb      eigenes Skelett mit fuenf Clips (DeerStag_Idle01, _Walk, _Run, _Death, _Dead), Weg auf Translation_Data
#   NCBearDeer.glb  dasselbe Netz auf den Knochen des Rehs (Rueckfall, tier_spez.md 6.5), ohne Clips
#   Body/NCBear.png 1024er Verkleinerung der gebackenen 2048er
# Aufruf: blender --background --factory-startup --python baer_tier.py -- ZIELORDNER [deer_walk.txt]
#   ZIELORDNER ist das Verzeichnis, unter dem 42/media liegt. deer_walk.txt kommt von Dump.java (Knochen des Rehs).
# Quelle der Figur: models_X/WorldItems/NCBear.fbx (Meter, Kopf +X, Boden z=0) und textures/WorldItems/NCBear.png aus NCBearTest.
# Alle Masse unten sind Meter im Tier-Rahmen: x vorn, y links, z oben. Massstab im Netz: 0,544 Einheiten je Meter, Tier schaut nach -Y.
# Statisch geprueft und offline gemessen, nicht gespielt.
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ZIEL = ARGS[0].replace("\\", "/").rstrip("/") + "/42/media/"
DEER = None   # Rueckfall NCBearDeer.glb wird hier nicht neu gebaut (der in NCBearTest bleibt)
QUELLE = (ARGS[1].replace("\\", "/").rstrip("/") + "/") if len(ARGS) > 1 and ARGS[1] else r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/mod/42/media/"
LIEGE_DATEI = ARGS[2] if len(ARGS) > 2 else None
M2U = 0.544                # Modelleinheiten je Meter (bau_stehend.md)
FPS = 30
K_WELT = 1.6 / 1.5         # MotionScale 1,6 (Defaults.xml) gegen Modellmassstab 1,5 (Core.DoPushIsoStuff 413-422)


def log(*a):
    print("TIER", *a, flush=True)


def sst(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ------------------------------------------------------------------ Rahmen
Q_C = Quaternion((0, 0, 1), math.radians(-90))     # Tier -> Armature: Kopf von +X nach -Y


def t2b(p):
    return Vector((p[1], -p[0], p[2])) * M2U


def qb(q):
    return Q_C @ q @ Q_C.inverted()


def vec(*a):
    return Vector(a)


# ------------------------------------------------------------------ Skelett (Meter, Tier-Rahmen)
# Name: (Kopf, Spitze, Eltern). Von den Querschnitten des Netzes abgelesen: Beine sitzen mittig im Bein,
# das Ellbogengelenk liegt hinter der Linie Schulter-Handgelenk, das Knie davor.
BONES = {
    "Bip01_Pelvis": ((-0.37, 0, 0.72), (-0.06, 0, 0.75), "Bip01"),
    "Bip01_Spine": ((-0.06, 0, 0.75), (0.24, 0, 0.80), "Bip01_Pelvis"),
    "Bip01_Spine1": ((0.24, 0, 0.80), (0.50, 0, 0.80), "Bip01_Spine"),
    "Bip01_Neck": ((0.50, 0, 0.80), (0.70, 0, 0.72), "Bip01_Spine1"),
    "Bip01_Head": ((0.70, 0, 0.72), (1.08, 0, 0.62), "Bip01_Neck"),
    "Bip01_Tail": ((-0.70, 0, 0.70), (-0.80, 0, 0.68), "Bip01_Pelvis"),
}
HUEFTE, KNIE, FERSE, BALLEN_H, ZEHE = (-0.46, 0.25, 0.69), (-0.35, 0.262, 0.41), (-0.48, 0.247, 0.10), (-0.25, 0.24, 0.045), (-0.19, 0.24, 0.03)
KLAV, SCHULTER, ELLE, HAND, BALLEN_V = (0.30, 0.10, 0.92), (0.29, 0.225, 0.72), (0.23, 0.24, 0.41), (0.32, 0.23, 0.10), (0.48, 0.22, 0.045)
for _n, _s in (("L", 1), ("R", -1)):
    def _m(p, s=_s):
        return (p[0], p[1] * s, p[2])
    BONES["Bip01_%s_Clavicle" % _n] = (_m(KLAV), _m(SCHULTER), "Bip01_Spine1")
    BONES["Bip01_%s_UpperArm" % _n] = (_m(SCHULTER), _m(ELLE), "Bip01_%s_Clavicle" % _n)
    BONES["Bip01_%s_Forearm" % _n] = (_m(ELLE), _m(HAND), "Bip01_%s_UpperArm" % _n)
    BONES["Bip01_%s_Hand" % _n] = (_m(HAND), _m(BALLEN_V), "Bip01_%s_Forearm" % _n)
    BONES["Bip01_%s_Thigh" % _n] = (_m(HUEFTE), _m(KNIE), "Bip01_Pelvis")
    BONES["Bip01_%s_Calf" % _n] = (_m(KNIE), _m(FERSE), "Bip01_%s_Thigh" % _n)
    BONES["Bip01_%s_Foot" % _n] = (_m(FERSE), _m(BALLEN_H), "Bip01_%s_Calf" % _n)
    BONES["Bip01_%s_Toe0" % _n] = (_m(BALLEN_H), _m(ZEHE), "Bip01_%s_Foot" % _n)
# ==== JUNGES (A): Ruhe-Gelenke des Jungen (SPEZ_JUNGES B.5) aus koerper/skelett.json; Knochen-Richtungen wie beim Erwachsenen
JUNGES = os.environ.get("NCB_JUNGES_ERW") != "1"
if JUNGES:
    import json as _json
    _SKJ = _json.load(open(os.environ.get("NCB_JUNGES_SKELETT", r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/skelett/skelett_rig.json")))   # RIG: Skelett des Generator-Jungen
    _RJ = _SKJ["ruhe_m"]
    _HAND_J, _HAND_E = _RJ["Bip01_L_Hand"], HAND
    BALLEN_V = tuple(_HAND_J[i] + (BALLEN_V[i] - _HAND_E[i]) for i in range(3))     # Vorderpranke: Ballen starr am Handgelenk
    BALLEN_H = tuple(_RJ["Bip01_L_Toe0"])
    for _k in list(BONES):
        _h, _t, _p = BONES[_k]
        _hj = tuple(float(v) for v in _RJ[_k])
        if _k.endswith("_Foot"):
            _tj = tuple(float(v) for v in _RJ[_k.replace("_Foot", "_Toe0")])
        elif _k.endswith("_Hand"):
            _tj = (BALLEN_V[0], BALLEN_V[1] * (1 if "_L_" in _k else -1), BALLEN_V[2])
        else:
            _tj = tuple(_hj[i] + (_t[i] - _h[i]) for i in range(3))
        BONES[_k] = (_hj, _tj, _p)
# ------------------------------------------------------------------ Kopfrahmen des Hochmodells (fuer Maul und Kiefer)
# Aus baer_quelle.py (HO, HA, HB, HC, KOPF_SK, Schnauzenstauchung SN_*, LIP, lippe, ECKE, Kiefergelenk) und baer_export.py:
# Spielnetz = (Hochmodell - (x0, 0, zmin)) * GROESSE mit GROESSE 0,75, x0 = -0,081 (backen.log), zmin = Bodenklemme 0,004.
# Gemessen: die Lippenlinie des Spielnetzes liegt bei c = lippe(a, |b|); dort malt gesicht_nacharbeit auch die Mundrille.
K_PITCH = math.radians(15.0)
K_HO = np.array((0.925, 0.0, 1.085 - (0.33 - 0.20)))
K_HA = np.array((math.cos(K_PITCH), 0.0, -math.sin(K_PITCH)))
K_HB = np.array((0.0, 1.0, 0.0))
K_HC = np.array((math.sin(K_PITCH), 0.0, math.cos(K_PITCH)))
K_SK = 1.17
_K_X = np.linspace(-1.0, 1.0, 4001)
_K_G = np.where(_K_X < 0.23, 0.0, np.where(_K_X < 0.32, (_K_X - 0.23) ** 2 / (2 * 0.09), _K_X - 0.23 - 0.045))
_K_Y = _K_X - 0.22 * _K_G
K_GROESSE, K_X0, K_ZMIN = 0.75, -0.081, 0.004
K_ECKE = 0.275              # Mundwinkel unter dem Auge (baer_quelle.py ECKE)
K_FAKTOR = K_SK * K_GROESSE  # Meter im Spielnetz je Kopfeinheit


def k_l2w(P):
    P = np.asarray(P, dtype=float)
    return (K_HO + (np.interp(P[..., 0], _K_X, _K_Y) * K_SK)[..., None] * K_HA + (P[..., 1] * K_SK)[..., None] * K_HB
            + (P[..., 2] * K_SK)[..., None] * K_HC)


def k_w2l(W):
    D = np.asarray(W, dtype=float) - K_HO
    return np.stack((np.interp((D @ K_HA) / K_SK, _K_Y, _K_X), (D @ K_HB) / K_SK, (D @ K_HC) / K_SK), -1)


def fbx2l(P):
    return k_w2l(np.asarray(P, dtype=float) / K_GROESSE + np.array((K_X0, 0.0, K_ZMIN)))


def l2fbx(P):
    return (k_l2w(P) - np.array((K_X0, 0.0, K_ZMIN))) * K_GROESSE


class _KKurve:
    """Glatte Tabelle wie Kurve in baer_quelle.py."""

    def __init__(self, xs, ys, n=400):
        xs, ys = np.array(xs, dtype=float), np.array(ys, dtype=float)
        m = np.gradient(ys, xs)
        X = np.linspace(xs[0], xs[-1], n)
        i = np.clip(np.searchsorted(xs, X) - 1, 0, len(xs) - 2)
        h = xs[i + 1] - xs[i]
        t = (X - xs[i]) / h
        self.X = X
        self.Y = (2 * t**3 - 3 * t**2 + 1) * ys[i] + (t**3 - 2 * t**2 + t) * h * m[i] + (-2 * t**3 + 3 * t**2) * ys[i + 1] + (t**3 - t**2) * h * m[i + 1]

    def __call__(self, a):
        return np.interp(a, self.X, self.Y)


K_LIP = _KKurve([0.20, 0.25, 0.29, 0.34, 0.42, 0.50], [-0.044, -0.046, -0.047, -0.047, -0.044, -0.040])


def k_lippe(a, B):
    return K_LIP(a) + 0.0055 * np.exp(-((B / 0.011) ** 2))


# Unterkiefer: Gelenk unter dem Ohr, Knochen laeuft die Kinnlinie entlang (baer_quelle.py "kiefer"), Kind des Kopfes
BONES["Bip01_Jaw"] = (tuple(float(v) for v in l2fbx((0.075, 0.0, -0.060))), tuple(float(v) for v in l2fbx((0.45, 0.0, -0.070))), "Bip01_Head")
if JUNGES:     # ==== JUNGES (B): Kiefergelenk des Jungen, Richtung wie beim Erwachsenen
    _h, _t, _p = BONES["Bip01_Jaw"]
    _hj = tuple(float(v) for v in _RJ["Bip01_Jaw"])
    BONES["Bip01_Jaw"] = (_hj, tuple(_hj[i] + (_t[i] - _h[i]) for i in range(3)), _p)
BIP01_Z = 0.72
J = {k: Vector(v[0]) for k, v in BONES.items()}
J["Bip01"] = Vector((0, 0, BIP01_Z))
J["Dummy01"] = Vector((0, 0, 0))
PARENT = {k: v[2] for k, v in BONES.items()}
PARENT["Bip01"] = "Dummy01"
PARENT["Dummy01"] = None
# Reihenfolge: Eltern vor Kindern
ORDER = ["Dummy01", "Bip01"]
while len(ORDER) < len(PARENT):
    for k, p in PARENT.items():
        if k not in ORDER and p in ORDER:
            ORDER.append(k)

LEG = {}
for _n, _s in (("L", 1), ("R", -1)):
    for _v, _a, _b, _c, _ball in (("V", "UpperArm", "Forearm", "Hand", BALLEN_V), ("H", "Thigh", "Calf", "Foot", BALLEN_H)):
        oben, unten, fuss = "Bip01_%s_%s" % (_n, _a), "Bip01_%s_%s" % (_n, _b), "Bip01_%s_%s" % (_n, _c)
        ja, jb, jc = J[oben], J[unten], J[fuss]
        y_r = (jb - ja).normalized()
        n_r = y_r.cross((jc - jb).normalized()).normalized()
        y2_r = (jc - jb).normalized()
        LEG[_v + _n] = dict(
            oben=oben, unten=unten, fuss=fuss, s=_s, vorn=_v == "V",
            a=(jb - ja).length, b=(jc - jb).length,
            ball=Vector((_ball[0], _ball[1] * _s, _ball[2])),
            pole=Vector((-1, 0, 0)) if _v == "V" else Vector((1, 0, 0)),
            F1=Matrix((y_r, n_r, y_r.cross(n_r))).transposed(),
            F2=Matrix((y2_r, n_r, y2_r.cross(n_r))).transposed(),
            knick0=math.degrees(y_r.angle(y2_r)),
        )


# ------------------------------------------------------------------ Pose: je Knochen Weltdrehung (gegen die Ruhe) und Kopfposition
def rx(g):
    return Quaternion((1, 0, 0), math.radians(g))


def ry(g):  # +g: Nase bzw. Zehe nach unten
    return Quaternion((0, 1, 0), math.radians(g))


def rz(g):  # +g: Nase nach links
    return Quaternion((0, 0, 1), math.radians(g))


def euler(yaw=0.0, pitch=0.0, roll=0.0):
    return rz(yaw) @ ry(pitch) @ rx(roll)


STAT = {}


def bein(pose, key, hip, ank, foot_q, stat):
    """Zwei-Knochen-IK: setzt oben, unten, fuss. hip und ank in Welt. foot_q ist die Weltdrehung der Pfote."""
    L = LEG[key]
    a, b = L["a"], L["b"]
    d = ank - hip
    ln = d.length
    maxd = (a + b) * 0.998
    stat["max"] = max(stat.get("max", 0.0), ln / (a + b))
    if ln > maxd:
        stat["ueber"] = stat.get("ueber", 0) + 1
        stat.setdefault("wo", {}).setdefault(key, []).append(round(ln / (a + b), 3))
        stat["fehl"] = max(stat.get("fehl", 0.0), ln - maxd)
        ln = maxd
    e = d.normalized()
    along = (a * a - b * b + ln * ln) / (2.0 * ln)
    h = math.sqrt(max(a * a - along * along, 0.0))
    pole = pose.get("_pole_" + key, L["pole"])
    p = pole - e * pole.dot(e)
    p.normalize()
    K = hip + e * along + p * h
    A = hip + e * ln
    y1 = (K - hip).normalized()
    y2 = (A - K).normalized()
    n = y1.cross(y2)
    if n.length < 1e-6:
        n = p.cross(e)
    n.normalize()
    F1 = Matrix((y1, n, y1.cross(n))).transposed()
    F2 = Matrix((y2, n, y2.cross(n))).transposed()
    knick = math.degrees(y1.angle(y2)) - L["knick0"]
    stat["knick"] = max(stat.get("knick", 0.0), abs(knick))
    stat["schwung"] = max(stat.get("schwung", 0.0), math.degrees(y1.angle(Vector(L["F1"].col[0]))))
    pose[L["oben"]] = ((F1 @ L["F1"].transposed()).to_quaternion(), hip.copy())
    pose[L["unten"]] = ((F2 @ L["F2"].transposed()).to_quaternion(), K.copy())
    pose[L["fuss"]] = (foot_q.copy(), A.copy())


def kette(pose, name, q):
    """Weltdrehung q fuer name; Position aus dem Elternteil."""
    par = PARENT[name]
    qp, pp = pose[par]
    pose[name] = (q.copy(), pp + qp @ (J[name] - J[par]))


def hueftpunkt(pose, key):
    L = LEG[key]
    par = PARENT[L["oben"]]
    qp, pp = pose[par]
    return pp + qp @ (J[L["oben"]] - J[par])


def rumpf(pose, pel_p, q_pel, q_sp, q_ch, q_ne, q_he, q_ta, kiefer=0.0):
    pose["Dummy01"] = (Quaternion(), J["Dummy01"].copy())
    pose["Bip01"] = (Quaternion(), J["Bip01"].copy())
    pose["Bip01_Pelvis"] = (q_pel.copy(), pel_p.copy())
    kette(pose, "Bip01_Spine", q_sp)
    kette(pose, "Bip01_Spine1", q_ch)
    kette(pose, "Bip01_Neck", q_ne)
    kette(pose, "Bip01_Head", q_he)
    kette(pose, "Bip01_Jaw", q_he @ ry(kiefer))     # zu: Kiefer in Ruhe zum Kopf
    kette(pose, "Bip01_Tail", q_ta)


def schluesselbein(pose, n, g):
    """Schulterblatt: dreht um die Querachse, schiebt damit die Schulter vor und zurueck. Der Knochen traegt keine Gewichte."""
    name = "Bip01_%s_Clavicle" % n
    kette(pose, name, pose["Bip01_Spine1"][0] @ ry(g))


def toe(pose):
    for n in "LR":
        kette(pose, "Bip01_%s_Toe0" % n, pose["Bip01_%s_Foot" % n][0])


def ballen_zu_ferse(key, ball, pitch):
    L = LEG[key]
    q = ry(pitch)
    return ball + q @ (J[L["fuss"]] - L["ball"]), q


def hermite(s, p0, p1, m0, m1):
    s2, s3 = s * s, s * s * s
    return (2 * s3 - 3 * s2 + 1) * p0 + (s3 - 2 * s2 + s) * m0 + (-2 * s3 + 3 * s2) * p1 + (s3 - s2) * m1


def ssf(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


# ------------------------------------------------------------------ Gang
WALK = dict(
    name="DeerStag_Walk", T=27, duty=0.62,
    # Passgang: die Beine einer Seite gehen fast zusammen
    kontakt=dict(HL=0.00, VL=0.10, HR=0.50, VR=0.60),
    S=dict(H=0.46, V=0.46), mitte=dict(H=0.03, V=-0.03), hub=dict(H=0.075, V=0.095),
    ab=dict(H=26.0, V=24.0), spitze=dict(H=40.0, V=55.0), aussen=0.018, senk=0.004, streck=dict(H=0.97, V=0.988),
)
RUN = dict(
    name="DeerStag_Run", T=16, duty=0.27,
    kontakt=dict(HL=0.00, HR=0.08, VL=0.42, VR=0.52),
    S=dict(H=0.56, V=0.56), mitte=dict(H=0.08, V=-0.04), hub=dict(H=0.12, V=0.15),
    ab=dict(H=34.0, V=30.0), spitze=dict(H=58.0, V=72.0), aussen=0.012, senk=0.010, streck=dict(H=0.97, V=0.985),
)


def fuss_bahn(G, key, phi):
    """Ballenposition und Pfotenneigung fuer Phase phi. Stuetze: Ballen steht in der Welt, also rueckwaerts im Tier."""
    L = LEG[key]
    art = key[0]
    u = (phi - G["kontakt"][key]) % 1.0
    duty, S, c = G["duty"], G["S"][art], G["mitte"][art]
    x0 = L["ball"].x + c
    if u < duty:
        w = u / duty
        x = x0 + S * 0.5 - S * w
        z = L["ball"].z
        y = L["ball"].y
        pit = G["ab"][art] * ssf(0.60, 1.0, w)
    else:
        s = (u - duty) / (1.0 - duty)
        # Anfangs- und Endtempo des Schwungs wie in der Stuetze, im Galopp gedeckelt: sonst schiesst die Pfote weit nach hinten
        m = -S * min((1.0 - duty) / duty, 1.0)
        x = hermite(s, x0 - S * 0.5, x0 + S * 0.5, m, m)
        z = L["ball"].z + G["hub"][art] * math.sin(math.pi * s ** 0.85)
        y = L["ball"].y + L["s"] * G["aussen"] * math.sin(math.pi * s)
        if s < 0.30:
            pit = G["ab"][art] + (G["spitze"][art] - G["ab"][art]) * ssf(0.0, 0.30, s)
        else:
            pit = G["spitze"][art] * (1.0 - ssf(0.30, 0.88, s)) - 7.0 * ssf(0.70, 0.90, s) * (1.0 - ssf(0.92, 1.0, s))
    return Vector((x, y, z)), pit


def c(x):
    return math.cos(2.0 * math.pi * x)


def gang(G, phi, stat, koerper):
    """Beine nach der Fussbahn; der Rumpf sinkt nur so weit, wie die stuetzenden Beine es verlangen (gestreckte Saeulen,
    der Rumpf schwingt darueber wie ein umgekehrtes Pendel). koerper(dz, dp) liefert den Rumpf mit Absenkung dz (Meter)
    und zusaetzlicher Neigung dp der Brust (Grad, Nase nach unten)."""
    ziele = {}
    for key in ("VL", "VR", "HL", "HR"):
        ball, pit = fuss_bahn(G, key, phi)
        ank, q = ballen_zu_ferse(key, ball, pit)
        u = (phi - G["kontakt"][key]) % 1.0
        ziele[key] = (ank, q, u < G["duty"] + 0.05 or u > 0.96)
    dz, dp = 0.0, 0.0
    for _ in range(6):
        pose = koerper(dz, dp)
        bed = dict(V=0.0, H=0.0)
        for key, (ank, q, st) in ziele.items():
            if not st:
                continue
            L = LEG[key]
            hip = hueftpunkt(pose, key)
            dmax = G["streck"][key[0]] * (L["a"] + L["b"])
            dxy2 = (hip.x - ank.x) ** 2 + (hip.y - ank.y) ** 2
            zreq = ank.z + math.sqrt(max(dmax * dmax - dxy2, 0.0))
            bed[key[0]] = min(bed[key[0]], zreq - hip.z)
        if bed["H"] > -2e-4 and bed["V"] > -2e-4:
            break
        dz += bed["H"]
        dp += math.degrees(math.atan2(-bed["V"], 0.37))
    stat["absenk"] = min(stat.get("absenk", 0.0), dz)
    stat["neig"] = max(stat.get("neig", 0.0), dp)
    for key, (ank, q, st) in ziele.items():
        bein(pose, key, hueftpunkt(pose, key), ank, q, stat)
    toe(pose)
    return pose


def pose_walk(f, stat):
    G = WALK
    phi = f / G["T"]
    # Linke Seite schwingt um 0,81, rechte um 0,31; das Gewicht geht auf die Stuetzseite, die schwingende Seite hebt sich
    wieg = c(phi - 0.81)

    def koerper(dz, dp):
        pel = J["Bip01_Pelvis"] + vec(0.008 * c(phi * 2), -0.020 * wieg, -G["senk"] + dz)
        q_pel = euler(yaw=-3.0 * c(phi), pitch=1.0 * c(2 * (phi - 0.10)), roll=3.6 * wieg)
        q_sp = ry(dp * 0.6) @ euler(yaw=-1.0 * c(phi - 0.05), pitch=0.6 * c(2 * (phi - 0.14)), roll=3.0 * c(phi - 0.85))
        # Die Schulterpartie rollt spaeter und staerker als die Kruppe: das ist der schwere Gang
        q_ch = ry(dp) @ euler(yaw=-4.2 * c(phi - 0.10), pitch=-0.8 * c(2 * (phi - 0.20)), roll=5.2 * c(phi - 0.91))
        q_ne = euler(yaw=1.0 * c(phi - 0.14), pitch=7.0 + 1.5 * c(2 * (phi - 0.28)), roll=2.2 * c(phi - 0.95))
        # Kopf tief, pendelt gegen die Schultern
        q_he = euler(yaw=5.0 * c(phi - 0.20), pitch=7.0 + 2.2 * c(2 * (phi - 0.34)), roll=-1.2 * c(phi - 0.20))
        q_ta = euler(yaw=7.0 * c(phi - 0.30), pitch=-2.0 * c(2 * phi))
        pose = {}
        rumpf(pose, pel, q_pel, q_sp, q_ch, q_ne, q_he, q_ta)
        # Schulterblatt: Pfote vorn -> Schulter vorn (Kontakt vorn links bei 0,10)
        for n, ph in (("L", 0.10), ("R", 0.60)):
            schluesselbein(pose, n, -12.0 * math.cos(2.0 * math.pi * (phi - ph)))
        return pose

    return gang(G, phi, stat, koerper)


def pose_run(f, stat):
    G = RUN
    phi = f / G["T"]
    # Gestreckt am Ende des Schubs, zusammengezogen bevor die Hinterbeine fassen
    beug = c(phi - 0.97)          # 1: Rumpf rund, Huefte unter dem Bauch
    kipp = c(phi - 0.18)          # 1: Nase oben

    def koerper(dz, dp):
        pel = J["Bip01_Pelvis"] + vec(0.045 * beug, 0.008 * c(phi - 0.2), -G["senk"] + 0.020 * c(phi - 0.86) + dz)
        q_pel = euler(yaw=2.0 * c(phi - 0.1), pitch=-8.0 * beug - 3.0 * kipp, roll=2.5 * c(phi - 0.05))
        q_sp = ry(dp * 0.6) @ euler(yaw=0.5 * c(phi - 0.15), pitch=-2.0 * beug - 3.0 * kipp, roll=1.2 * c(phi - 0.1))
        q_ch = ry(dp) @ euler(yaw=-2.0 * c(phi - 0.45), pitch=5.0 * beug - 3.0 * kipp, roll=-2.5 * c(phi - 0.50))
        q_ne = euler(yaw=1.0 * c(phi - 0.5), pitch=6.0 + 2.0 * beug + 3.0 * kipp, roll=-1.0 * c(phi - 0.5))
        q_he = euler(yaw=1.5 * c(phi - 0.55), pitch=5.0 + 4.0 * kipp, roll=0.0)
        q_ta = euler(yaw=5.0 * c(phi - 0.3), pitch=-10.0 * c(phi - 0.1))
        pose = {}
        rumpf(pose, pel, q_pel, q_sp, q_ch, q_ne, q_he, q_ta)
        for n, ph in (("L", 0.42), ("R", 0.52)):
            schluesselbein(pose, n, -14.0 * math.cos(2.0 * math.pi * (phi - ph)))
        return pose

    return gang(G, phi, stat, koerper)


def beine_stehen(pose, stat, senk=None):
    for key in ("VL", "VR", "HL", "HR"):
        ank, q = ballen_zu_ferse(key, LEG[key]["ball"], 0.0)
        bein(pose, key, hueftpunkt(pose, key), ank, q, stat)
    toe(pose)


IDLE_T = 96


def pose_idle(f, stat):
    x = f / IDLE_T
    pel = J["Bip01_Pelvis"] + vec(0.004 * c(x + 0.1), 0.010 * c(x - 0.2), -0.004 + 0.0045 * c(x * 2 + 0.05))
    q_pel = euler(yaw=0.6 * c(x - 0.2), pitch=0.5 * c(x * 2), roll=0.8 * c(x - 0.2))
    q_sp = euler(yaw=0.4 * c(x - 0.25), pitch=-0.7 * c(x * 2 - 0.05), roll=0.9 * c(x - 0.25))
    # Atmen: die Brust hebt sich
    q_ch = euler(yaw=0.8 * c(x - 0.3), pitch=-1.5 * c(x * 2 - 0.1), roll=1.0 * c(x - 0.3))
    q_ne = euler(yaw=3.0 * c(x - 0.42), pitch=4.0 + 1.0 * c(x * 2 - 0.2))
    # Kopf sieht sich langsam um
    q_he = euler(yaw=7.5 * c(x - 0.48), pitch=4.0 + 2.6 * c(x * 2 + 0.3), roll=-1.4 * c(x - 0.48))
    q_ta = euler(yaw=3.0 * c(x * 2 + 0.1))
    rumpf(pose_neu := {}, pel, q_pel, q_sp, q_ch, q_ne, q_he, q_ta)
    for n in "LR":
        schluesselbein(pose_neu, n, 0.0)
    beine_stehen(pose_neu, stat)
    return pose_neu


# ------------------------------------------------------------------ Sturz
DEATH_N = 78
# Liegepose: auf die rechte Flanke gerollt, Ruecken nach rechts, Beine nach links. Zahlen an der Haut abgelesen (tier_pruef.py).
LIEGE = dict(
    # Liegt auf der rechten Flanke, etwas zum Bauch gedreht: die Beine zeigen zur Seite und ein wenig nach unten.
    # Die Hoehe pel.z setzt boden_liege() nach der Haut, damit nichts im Boden steckt.
    pel=vec(-0.37, -0.24, 0.47),
    q_pel=euler(yaw=2.0, pitch=0.0, roll=80.0),
    q_sp=euler(yaw=-1.0, pitch=0.0, roll=80.0),
    q_ch=euler(yaw=-4.0, pitch=3.0, roll=78.0),
    q_ne=euler(yaw=-4.0, pitch=28.0, roll=72.0),
    q_he=euler(yaw=0.0, pitch=22.0, roll=68.0),
    q_ta=euler(yaw=-12.0, pitch=0.0, roll=75.0),
    klav=dict(L=-8.0, R=6.0),
    # Ferse bzw. Handgelenk liegend und die Weltdrehung der Pfote. Unten liegende Beine auf dem Boden,
    # die oberen sinken auf sie, Vorderbein etwas nach vorn, Hinterbein etwas nach hinten.
    fuss=dict(
        VR=(vec(0.50, 0.22, 0.10), euler(yaw=-18.0, pitch=30.0, roll=56.0)),
        HR=(vec(-0.44, 0.24, 0.10), euler(yaw=10.0, pitch=20.0, roll=56.0)),
        VL=(vec(0.42, 0.05, 0.27), euler(yaw=-20.0, pitch=42.0, roll=70.0)),
        HL=(vec(-0.44, 0.08, 0.28), euler(yaw=12.0, pitch=30.0, roll=70.0)),
    ),
)
LIEGE["pole"] = dict(VL=vec(-1, 0.0, 0.25), VR=vec(-1, 0.0, 0.30), HL=vec(1, 0, 0.25), HR=vec(1, 0, 0.30))


def pose_death(f, stat):
    t = (f - 0) / (DEATH_N - 1)
    # 0..0,24 wankt und sackt, 0,24..0,66 kippt immer schneller, dann Aufschlag mit kleinem Nachfedern, Kopf zuletzt
    kipp = ssf(0.20, 0.60, t) ** 1.6
    feder = 0.040 * math.sin(max(0.0, min(1.0, (t - 0.60) / 0.20)) * math.pi) * (1.0 if t > 0.60 else 0.0)
    wank = math.sin(min(t / 0.24, 1.0) * math.pi)           # zuerst kurz zur Gegenseite
    k = min(1.0, kipp - feder)
    sack = ssf(0.02, 0.26, t)
    p_st = J["Bip01_Pelvis"] + vec(0.0, 0.03 * wank, -0.022 - 0.075 * sack)
    pel = p_st.lerp(LIEGE["pel"], k)
    pel.z += 0.018 * math.sin(max(0.0, min(1.0, (t - 0.60) / 0.16)) * math.pi)

    def mische(q_ziel, verz=0.0, wanken=0.0, nick=0.0):
        k2 = max(0.0, min(1.0, k - verz * (1.0 - k) * 0.5))
        q0 = euler(pitch=nick * sack, roll=-wanken * wank)
        return q0.slerp(q_ziel, k2)

    q_pel = mische(LIEGE["q_pel"], 0.0, 3.0)
    q_sp = mische(LIEGE["q_sp"], 0.0, 3.0)
    q_ch = mische(LIEGE["q_ch"], 0.05, 3.5, 2.0)
    # Kopf sinkt schon im Wanken und kommt zuletzt auf dem Boden an
    kopf = ssf(0.55, 0.92, t)
    q_ne0 = mische(LIEGE["q_ne"], 0.25, 2.0, 12.0)
    q_he0 = mische(LIEGE["q_he"], 0.45, 1.0, 16.0)
    q_ne = q_ne0.slerp(LIEGE["q_ne"], kopf)
    q_he = q_he0.slerp(LIEGE["q_he"], kopf)
    q_ta = mische(LIEGE["q_ta"])
    rumpf(pose_neu := {}, pel, q_pel, q_sp, q_ch, q_ne, q_he, q_ta)
    for n in "LR":
        schluesselbein(pose_neu, n, LIEGE["klav"][n] * k)
    # Rechte Beine bleiben stehen, bis er zu weit hinten liegt; linke heben ab
    for key in ("VL", "VR", "HL", "HR"):
        ank0, q0 = ballen_zu_ferse(key, LEG[key]["ball"], 0.0)
        ank1, q1 = LIEGE["fuss"][key]
        verz = 0.30 if key[1] == "R" else 0.05
        kb = ssf(verz * 0.6, 1.0, k)
        ank = ank0.lerp(ank1, kb)
        if key[1] == "L":
            ank.z += 0.10 * math.sin(kb * math.pi)
        pose_neu["_pole_" + key] = LEG[key]["pole"].lerp(LIEGE["pole"][key], kb)
        bein(pose_neu, key, hueftpunkt(pose_neu, key), ank, q0.slerp(q1, kb), stat)
    toe(pose_neu)
    return pose_neu


def pose_dead(f, stat):
    return pose_death(DEATH_N - 1, stat)


# ------------------------------------------------------------------ Kampf- und Ruheclips (Lauf baer-anim, anim_spez.md 7)
# Neu gebaut nach anim_referenz.md (Bewegung echter Baeren, Gelenkgrenzen) und Kevins Test vom 08.11.: der Arm knickt nie
# gegen das Gelenk, der ganze Koerper arbeitet mit (Becken, Ruecken, Schulterblatt, Hinterbeine, Kopf), die Pfote dreht in der
# Luft RELATIV ZUM UNTERARM (die alten Clips gaben eine Weltdrehung vor, daher Pfote -139/-168 Grad verdreht), und jede Taste
# wird gegen feste Gelenkgrenzen geklemmt und gemessen (GRENZEN unten, Messgroessen wie _arbeit/baer_anim/ref/gelenke_messen.py).
# Spuren: Zeit in s, Wert; dazwischen monotone kubische Kurve (Fritsch-Carlson). Anfang und Ende sind die Grundhaltung des
# Stehens (Mittel von DeerStag_Idle01), ausser bei Sitzen/Fressen (eigene Grundpose S bzw. E).
# Gliedmassen je Bein: ball_X (Ballen in Welt, ("S", d) = Schulter bzw. Huefte zur Schluesselzeit plus d), welt_X (1 = Pfote
# mit Weltdrehung rot_X, fuer den Boden; 0 = Pfote relativ zum Unterarm mit rel_X = (dors, aus, sup) in den Messgroessen),
# pole_X (Pol des Ellbogens im Rahmen der Brust bzw. des Knies im Rahmen des Beckens).
# Drehungen (Gieren, Nicken, Rollen) in Grad wie euler(): Nicken + = Nase runter, Gieren + = Nase links, Rollen + = linke Seite hoch.
# Dauern und Treffer: Vertrag mit NCBearFight.lua (F.ACTS) und den Knoten (anim_spez.md 7, anim_lua.md).
T_REAR, T_HIEB, T_SLAM, T_MAUL, T_BISS = 3.0, 1.5, 2.4, 1.6, 1.3          # 90, 45, 72, 48, 39 Bilder
T_SETZEN, T_SITZEN, T_AUFSTEHEN, T_FRESSEN = 1.6, 4.0, 1.3, 3.2          # 48, 120 (Schleife), 39, 96 (Schleife)
R0 = (0.0, 0.0, 0.0)

# ---- Gelenkgrenzen (feste Regel, anim_referenz.md Abschnitt 2). Beine: Messgroessen von bein_mass; Rumpf: (Gieren, Nicken,
# Rollen) gegen den Elternknochen. Jede Taste jedes Clips aus dieser Liste wird nach dem Loesen dagegen geklemmt.
GRENZEN = {
    "V": dict(prot=(-70, 60), abd=(-20, 45), tw=(-35, 20), inner=(55, 173), dors=(-115, 75), seitab=(-15, 15), sup=(-20, 35)),
    "H": dict(prot=(-60, 80), abd=(-15, 35), tw=(-25, 15), inner=(55, 174), dors=(-125, -45), seitab=(-12, 12), sup=(-20, 20)),
}
GRENZEN_RUMPF = {
    "sp_pel": ((-12, 12), (-20, 20), (-12, 12)),
    "ch_sp": ((-15, 15), (-15, 15), (-15, 15)),
    "ne_ch": ((-35, 35), (-45, 50), (-15, 15)),
    "he_ne": ((-30, 30), (-35, 35), (-25, 25)),
}
# Lauf baer-2c, Bau Sitzen: EINZIGE Ausnahme (SPEZ_2C.md 5.4), nur in NCBear_SitDown/_Sit/_StandUp: Kopf gegen Hals nicken bis +60 statt
# +35 (Beugung in Gelenkrichtung: senkrechter Hals, Kopf blickt geradeaus wie beim sitzenden Hund). Alle anderen Clips klemmen wie bisher.
GRENZEN_RUMPF_SITZ = dict(GRENZEN_RUMPF, he_ne=((-30, 30), (-35, 60), (-25, 25)))
if JUNGES:     # ==== JUNGES (C): Sitz-Ausnahmen des Jungen (SPEZ_JUNGES D.4): Brust gegen Lende nicken bis -22, Kopf gegen Hals bis +68
    GRENZEN_RUMPF_SITZ = dict(GRENZEN_RUMPF, ch_sp=((-15, 15), (-22, 15), (-15, 15)), he_ne=((-30, 30), (-35, 68), (-25, 25)))
SITZ_CLIPS = ("NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp")
GR_AKTIV = {"rumpf": GRENZEN_RUMPF}               # beim Bau eines Sitz-Clips GRENZEN_RUMPF_SITZ (Schleife unten), sonst GRENZEN_RUMPF
GRENZE_KLAV = ((-25.0, 20.0), (-15.0, 15.0))     # Schulterblatt Nicken, Rollen gegen die Brust (Gieren 0)
GRENZE_KIEFER = (0.0, 40.0)
SPRUNG = dict(sup=20.0, tw=20.0, dors=35.0)       # Grad je Bild hoechstens (Gang/Lauf bleiben darunter)
# Hinterfuss: Rollen der Sohle aus der Beinebene (Fixer 08.11., anim_review_optik.md Fund 3). Die Messgroessen dors/seitab/sup sehen
# es nicht, wenn der Fuss quer zum Unterschenkel steht; deshalb eigene Grenze und eigener Sprung je Bild (Gang <= 6, Lauf <= 4).
SOHLE_GRENZE, SOHLE_SPRUNG = 20.0, 20.0
RAND = 0.05                                       # klemmen auf Grenze minus 0,05 Grad (Rechengenauigkeit)


def _deg(x):
    return math.degrees(x)


def twist_swing(q, axis):
    """q = swing @ twist, twist um axis (Einheitsvektor). Rueckgabe: Twistwinkel (Grad, rechte Hand um axis), swing."""
    v = Vector((q.x, q.y, q.z))
    proj = axis * v.dot(axis)
    tw = Quaternion((q.w, proj.x, proj.y, proj.z))
    if tw.magnitude < 1e-9:
        tw = Quaternion()
    else:
        tw.normalize()
    ang = 2.0 * math.atan2(Vector((tw.x, tw.y, tw.z)).dot(axis), tw.w)
    ang = (ang + math.pi) % (2 * math.pi) - math.pi
    return _deg(ang), q @ tw.inverted()


def rotvec(q):
    q = q.copy()
    if q.w < 0:
        q = -q
    s = math.sqrt(max(1e-18, q.x * q.x + q.y * q.y + q.z * q.z))
    ang = 2.0 * math.atan2(s, q.w)
    return Vector((q.x, q.y, q.z)) / s * ang if s > 1e-9 else Vector((0, 0, 0))


def ypr(q):
    e = q.to_euler("XYZ")
    return _deg(e.z), _deg(e.y), _deg(e.x)   # Gieren, Nicken, Rollen


def _sag(d):
    return _deg(math.atan2(d.x, -d.z))


def _asin(x):
    return _deg(math.asin(max(-1.0, min(1.0, x))))


def _kl(v, gr):
    lo, hi = gr
    return min(max(v, lo + RAND), hi - RAND)


# Ruhe-Geometrie je Bein (genau wie gelenke_messen.py)
RUHE = {}
for _key, _L in LEG.items():
    _lat = Vector((0, _L["s"], 0))
    _hip0, _K0, _A0 = J[_L["oben"]], J[_L["unten"]], J[_L["fuss"]]
    _d_up0 = (_K0 - _hip0).normalized()
    _d_lo0 = (_A0 - _K0).normalized()
    _d_ft0 = (_L["ball"] - _A0).normalized()
    _n0 = _d_up0.cross(_d_lo0).normalized()
    _l = (_A0 - _hip0).normalized()
    _e0 = (_K0 - (_hip0 + _l * (_K0 - _hip0).dot(_l))).normalized()
    RUHE[_key] = dict(lat=_lat, d_up0=_d_up0, d_lo0=_d_lo0, d_ft0=_d_ft0, n0=_n0, m0=_d_lo0.cross(_n0).normalized(),
                      tw_sgn=1.0 if _d_up0.cross(_e0).dot(_lat) > 0 else -1.0,
                      sup_sgn=1.0 if _d_lo0.cross(Vector((0, 0, -1))).dot(-_lat) > 0 else -1.0,
                      inner0=_deg((_hip0 - _K0).angle(_A0 - _K0)))
    # Vorzeichen der Ellbogen-/Kniedrehung um n0: Innenwinkel wird kleiner, wenn el_sgn * Winkel waechst
    _q = Quaternion(_n0, math.radians(5.0))
    _inn = _deg((-_d_up0).angle(_q @ _d_lo0))
    RUHE[_key]["el_sgn"] = 1.0 if _inn < RUHE[_key]["inner0"] else -1.0


def schulter_mass(key, l_up):
    """(prot, abd, tw) des Oberarms/Oberschenkels gegen Schluesselbein bzw. Becken (lokale Drehung l_up)."""
    R = RUHE[key]
    tw, sw = twist_swing(l_up, R["d_up0"])
    d1 = sw @ R["d_up0"]
    return (_sag(d1) - _sag(R["d_up0"]), _asin(d1.dot(R["lat"])) - _asin(R["d_up0"].dot(R["lat"])), tw * R["tw_sgn"])


def schulter_bauen(key, prot, abd, tw):
    R = RUHE[key]
    sg = math.radians(_sag(R["d_up0"]) + prot)
    la = math.radians(_asin(R["d_up0"].dot(R["lat"])) + abd)
    d1 = Vector((math.cos(la) * math.sin(sg), LEG[key]["s"] * math.sin(la), -math.cos(la) * math.cos(sg)))
    return R["d_up0"].rotation_difference(d1) @ Quaternion(R["d_up0"], math.radians(tw * R["tw_sgn"]))


def ellbogen_mass(key, l_lo):
    R = RUHE[key]
    return _deg((-R["d_up0"]).angle(l_lo @ R["d_lo0"]))


def ellbogen_bauen(key, inner):
    R = RUHE[key]
    return Quaternion(R["n0"], math.radians((R["inner0"] - inner) * R["el_sgn"]))


def pfote_mass(key, l_ft):
    """(dors, seitab, sup) der Pfote gegen den Unterarm bzw. des Fusses gegen den Unterschenkel (lokal l_ft)."""
    R = RUHE[key]
    sup, _sw = twist_swing(l_ft, R["d_lo0"])
    d_ft = l_ft @ R["d_ft0"]
    d_lo, n_c = R["d_lo0"], R["n0"]
    return (_deg(math.atan2(d_lo.cross(d_ft).dot(n_c), d_lo.dot(d_ft))), _asin(d_ft.dot(n_c)), sup * R["sup_sgn"])


def pfote_param(key, l_ft):
    R = RUHE[key]
    s_deg, sw = twist_swing(l_ft, R["d_lo0"])
    rv = rotvec(sw)
    return [rv.dot(R["n0"]), rv.dot(R["m0"]), math.radians(s_deg)]


def pfote_aus_param(key, p):
    R = RUHE[key]
    v = R["n0"] * p[0] + R["m0"] * p[1]
    sw = Quaternion(v.normalized(), v.length) if v.length > 1e-12 else Quaternion()
    return sw @ Quaternion(R["d_lo0"], p[2])


def pfote_loesen(key, ziel, p0=None):
    """Lokale Pfotendrehung mit den Messgroessen ziel = (dors, seitab, sup); Newton mit numerischer Ableitung."""
    R = RUHE[key]
    if p0 is None:
        p = [0.0, 0.0, math.radians(ziel[2] * R["sup_sgn"])]
        d0 = pfote_mass(key, Quaternion())[0]
        p[0] = math.radians(ziel[0] - d0) * (1.0 if pfote_mass(key, pfote_aus_param(key, [0.05, 0, 0]))[0] > d0 else -1.0)
    else:
        p = list(p0)
    fehl = 99.0
    for _ in range(14):
        m = pfote_mass(key, pfote_aus_param(key, p))
        f = np.array([m[0] - ziel[0], m[1] - ziel[1], ((m[2] - ziel[2] + 180.0) % 360.0) - 180.0])
        fehl = float(np.abs(f).max())
        if fehl < 0.005:
            break
        Jm = np.zeros((3, 3))
        for j in range(3):
            p2 = list(p)
            p2[j] += 1e-4
            m2 = pfote_mass(key, pfote_aus_param(key, p2))
            Jm[:, j] = (np.array(m2) - np.array(m)) / 1e-4
        dp = np.linalg.lstsq(Jm, -f, rcond=None)[0]
        n = float(np.abs(dp).max())
        if n > 0.3:
            dp *= 0.3 / n
        p = [p[k] + float(dp[k]) for k in range(3)]
    return pfote_aus_param(key, p), p, fehl


def bein_mass(pose, key):
    """Messgroessen eines Beins aus der fertigen Pose (wie gelenke_messen.py bein_mass)."""
    L = LEG[key]
    q_par = pose[PARENT[L["oben"]]][0]
    q_up, hip = pose[L["oben"]]
    q_lo, K = pose[L["unten"]]
    q_ft, A = pose[L["fuss"]]
    prot, abd, tw = schulter_mass(key, q_par.inverted() @ q_up)
    dors, seitab, sup = pfote_mass(key, q_lo.inverted() @ q_ft)
    ball = A + q_ft @ (L["ball"] - J[L["fuss"]])
    return dict(prot=prot, abd=abd, tw=tw, inner=_deg((hip - K).angle(A - K)), dors=dors, seitab=seitab, sup=sup,
                ball=(ball.x, ball.y, ball.z))


def rumpf_mass(pose):
    q = {k: pose[k][0] for k in ("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Head")}
    r = dict(sp_pel=ypr(q["Bip01_Pelvis"].inverted() @ q["Bip01_Spine"]), ch_sp=ypr(q["Bip01_Spine"].inverted() @ q["Bip01_Spine1"]),
             ne_ch=ypr(q["Bip01_Spine1"].inverted() @ q["Bip01_Neck"]), he_ne=ypr(q["Bip01_Neck"].inverted() @ q["Bip01_Head"]),
             pel_welt=ypr(q["Bip01_Pelvis"]), brust_welt=ypr(q["Bip01_Spine1"]), kopf_welt=ypr(q["Bip01_Head"]))
    r["kiefer"] = ypr(q["Bip01_Head"].inverted() @ pose["Bip01_Jaw"][0])[1]
    for n in "LR":
        r["klav_" + n] = ypr(pose["Bip01_Spine1"][0].inverted() @ pose["Bip01_%s_Clavicle" % n][0])
    return r


def _zaehle(st, was, t):
    st.setdefault("klemm", {}).setdefault(was, []).append(round(t, 3))


def ik_zwei(hip, ank, pole, key, q_par, st, t):
    """Zwei-Knochen-IK wie bein(); Abstand Schulter-Handgelenk in den Grenzen des Ellbogens, und liegt die Drehung des Oberarms
    ausserhalb ihrer Grenze, wird der Ellbogen um die Achse Schulter-Handgelenk geschwenkt (das Handgelenk bleibt, wo es ist)."""
    L = LEG[key]
    G = GRENZEN[key[0]]
    a, b = L["a"], L["b"]
    lo, hi = G["inner"]
    dmin = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(lo + 2 * RAND)))
    dmax = min(math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(hi - 2 * RAND))), (a + b) * 0.998)
    d = ank - hip
    ln = d.length
    st["max"] = max(st.get("max", 0.0), ln / (a + b))
    if ln > dmax or ln < dmin:
        _zaehle(st, "abstand", t)
        st["fehl"] = max(st.get("fehl", 0.0), ln - dmax, dmin - ln)
        ln = min(max(ln, dmin), dmax)
    e = d.normalized()
    along = (a * a - b * b + ln * ln) / (2.0 * ln)
    h = math.sqrt(max(a * a - along * along, 0.0))
    p = pole - e * pole.dot(e)
    if p.length < 1e-6:
        p = L["pole"] - e * L["pole"].dot(e)
    p.normalize()

    def bau(pp):
        K = hip + e * along + pp * h
        A = hip + e * ln
        y1 = (K - hip).normalized()
        y2 = (A - K).normalized()
        n = y1.cross(y2)
        if n.length < 1e-6:
            n = pp.cross(e)
        n.normalize()
        F1 = Matrix((y1, n, y1.cross(n))).transposed()
        F2 = Matrix((y2, n, y2.cross(n))).transposed()
        return (F1 @ L["F1"].transposed()).to_quaternion(), (F2 @ L["F2"].transposed()).to_quaternion()

    def drehung(pp):
        q_up, _ = bau(pp)
        return schulter_mass(key, q_par.inverted() @ q_up)[2]

    q_up, q_lo = bau(p)
    t_lo, t_hi = G["tw"]
    tw0 = drehung(p)
    if not (t_lo <= tw0 <= t_hi):
        _zaehle(st, "schwenk", t)
        gef = None
        for k in range(1, 73):
            for sg in (1.0, -1.0):
                psi = math.radians(2.5 * k) * sg
                if t_lo + RAND <= drehung(Quaternion(e, psi) @ p) <= t_hi - RAND:
                    gef = psi
                    break
            if gef is not None:
                break
        if gef is not None:
            a0, a1 = gef - math.copysign(math.radians(2.5), gef), gef
            for _ in range(12):
                am = 0.5 * (a0 + a1)
                if t_lo + RAND <= drehung(Quaternion(e, am) @ p) <= t_hi - RAND:
                    a1 = am
                else:
                    a0 = am
            q_up, q_lo = bau(Quaternion(e, a1) @ p)
    return q_up, q_lo


def bein_kampf(pose, key, ziel, q_welt, rel, welt, pole_w, st, t, ik=1.0, fk=None):
    """Loest ein Bein. ik 1: Ballen nach ziel (IK), Pfote in Welt (welt 1) oder relativ zum Unterarm (welt 0). ik 0: Vorwaerts-
    kette aus den Messgroessen fk = (prot, abd, tw, inner) und rel (Bogen im Gelenkraum, fuer die Luft). Dazwischen je Gelenk
    gemischt. Danach jede Messgroesse gegen GRENZEN klemmen (Schulter, Ellbogen, Pfote). Setzt pose, gibt den Ballen zurueck."""
    L = LEG[key]
    hip = hueftpunkt(pose, key)
    q_par = pose[PARENT[L["oben"]]][0]
    vf = J[L["fuss"]] - L["ball"]
    l_rel = None
    if welt < 0.999 or ik < 0.999:
        l_rel, _p, fehl = pfote_loesen(key, rel)
        st["pfote_fehl"] = max(st.get("pfote_fehl", 0.0), fehl)
    if ik > 1e-3:
        q_ft = q_welt
        for _ in range(1 if welt >= 0.999 else 5):
            ank = ziel + q_ft @ vf
            q_up, q_lo = ik_zwei(hip, ank, pole_w, key, q_par, st, t)
            if welt < 0.999:
                q_r = q_lo @ l_rel
                q_ft = q_r.slerp(q_welt, welt) if welt > 1e-3 else q_r
        l_up = q_par.inverted() @ q_up
        l_lo = q_up.inverted() @ q_lo
        l_ft = q_lo.inverted() @ q_ft
    if ik < 0.999:
        f_up = schulter_bauen(key, fk[0], fk[1], fk[2])
        f_lo = ellbogen_bauen(key, fk[3])
        if ik > 1e-3:
            l_up, l_lo, l_ft = f_up.slerp(l_up, ik), f_lo.slerp(l_lo, ik), l_rel.slerp(l_ft, ik)
        else:
            l_up, l_lo, l_ft = f_up, f_lo, l_rel
    G = GRENZEN[key[0]]
    # Schulter / Huefte
    pr, ab, tw = schulter_mass(key, l_up)
    k3 = (_kl(pr, G["prot"]), _kl(ab, G["abd"]), _kl(tw, G["tw"]))
    if max(abs(k3[0] - pr), abs(k3[1] - ab), abs(k3[2] - tw)) > 1e-6:
        _zaehle(st, "schulter", t)
        l_up = schulter_bauen(key, *k3)
    # Ellbogen / Knie (reines Scharnier)
    inn = ellbogen_mass(key, l_lo)
    k1 = _kl(inn, G["inner"])
    if abs(k1 - inn) > 1e-6:
        _zaehle(st, "ellbogen", t)
        l_lo = ellbogen_bauen(key, k1)
    # Pfote / Fuss
    dm = pfote_mass(key, l_ft)
    kd = (_kl(dm[0], G["dors"]), _kl(dm[1], G["seitab"]), _kl(dm[2], G["sup"]))
    if max(abs(kd[i] - dm[i]) for i in range(3)) > 1e-6:
        _zaehle(st, "pfote", t)
        l_ft, _p, fehl = pfote_loesen(key, kd, pfote_param(key, l_ft))
        st["pfote_fehl"] = max(st.get("pfote_fehl", 0.0), fehl)
    q_up = q_par @ l_up
    K = hip + q_up @ (J[L["unten"]] - J[L["oben"]])
    q_lo = q_up @ l_lo
    A = K + q_lo @ (J[L["fuss"]] - J[L["unten"]])
    q_ft = q_lo @ l_ft
    pose[L["oben"]] = (q_up, hip.copy())
    pose[L["unten"]] = (q_lo, K)
    pose[L["fuss"]] = (q_ft, A)
    return A + q_ft @ (L["ball"] - J[L["fuss"]])


def pchip(ts, ys, t):
    ts = np.asarray(ts, dtype=float)
    ys = np.asarray(ys, dtype=float).reshape(len(ts), -1)
    if len(ts) == 1 or t <= ts[0]:
        return ys[0].copy()
    if t >= ts[-1]:
        return ys[-1].copy()
    h = np.diff(ts)
    dl = np.diff(ys, axis=0) / h[:, None]
    m = np.zeros_like(ys)
    for k in range(1, len(ts) - 1):
        w1 = 2.0 * h[k] + h[k - 1]
        w2 = h[k] + 2.0 * h[k - 1]
        gl = dl[k - 1] * dl[k] > 0
        q1 = np.where(gl, dl[k - 1], 1.0)
        q2 = np.where(gl, dl[k], 1.0)
        m[k] = np.where(gl, (w1 + w2) / (w1 / q1 + w2 / q2), 0.0)
    i = int(np.searchsorted(ts, t, side="right")) - 1
    i = min(max(i, 0), len(ts) - 2)
    s = (t - ts[i]) / h[i]
    return hermite(s, ys[i], ys[i + 1], m[i] * h[i], m[i + 1] * h[i])


def NB(key, dx=0.0, dy=0.0, dz=0.0):
    b = LEG[key]["ball"]
    return (b.x + dx, b.y + dy, b.z + dz)


def _stand_rel():
    """Messgroessen der Pfoten in der Grundhaltung (Startwert der rel-Spuren, damit eine Blende nicht springt)."""
    pose = {}
    rumpf(pose, J["Bip01_Pelvis"] + vec(0, 0, -0.004), Quaternion(), Quaternion(), Quaternion(), ry(4.0), ry(4.0), Quaternion())
    for n in "LR":
        schluesselbein(pose, n, 0.0)
    beine_stehen(pose, {})
    rel = {k: tuple(round(v, 3) for v in pfote_mass(k, pose[LEG[k]["unten"]][0].inverted() @ pose[LEG[k]["fuss"]][0])) for k in LEG}
    fk = {}
    for k in LEG:
        m = bein_mass(pose, k)
        fk[k] = tuple(round(m[f], 3) for f in ("prot", "abd", "tw", "inner"))
    return rel, fk


REL0, FK0 = _stand_rel()


def grund():
    N = dict(pel=(0.0, 0.0, -0.004), r_pel=R0, r_sp=R0, r_ch=R0, r_ne=(0.0, 4.0, 0.0), r_he=(0.0, 4.0, 0.0), r_ta=R0,
             kiefer=(0.0,), klav_L=(0.0, 0.0), klav_R=(0.0, 0.0))
    for key, L in LEG.items():
        N["ball_" + key] = tuple(L["ball"])
        N["rot_" + key] = R0
        N["pole_" + key] = tuple(L["pole"])
        N["welt_" + key] = (1.0,)
        N["rel_" + key] = REL0[key]
        N["ik_" + key] = (1.0,)
        N["fk_" + key] = FK0[key]
    return N


def _tausche(k):
    for a_, b_ in (("VL", "VR"), ("VR", "VL"), ("HL", "HR"), ("HR", "HL")):
        if k.endswith("_" + a_):
            return k[:-2] + b_
    return {"klav_L": "klav_R", "klav_R": "klav_L"}.get(k, k)


def _spiegel_wert(k, v):
    if k.startswith(("ball_", "pole_")) or k == "pel":
        if isinstance(v[0], str):
            return (v[0], (v[1][0], -v[1][1], v[1][2]))
        return (v[0], -v[1], v[2])
    if k.startswith(("r_", "rot_")):
        return (-v[0], v[1], -v[2])
    if k.startswith("klav_"):
        return (v[0], -v[1])
    if k.startswith("rel_"):
        return (v[0], -v[1], v[2])     # seitab wechselt mit der Seite das Vorzeichen (n0 gespiegelt), dors und sup nicht
    return v


def spiegeln(sp):
    """Hieb rechts aus Hieb links: Seite, Gieren und Rollen spiegeln, L und R tauschen. Das Skelett ist symmetrisch gebaut."""
    return {_tausche(k): [(t, _spiegel_wert(k, v)) for t, v in ks] for k, ks in sp.items()}


def wert(sp, k, t):
    ts, ys = sp[k]
    return pchip(ts, ys, t)


def rumpf_bei(sp, t, st=None):
    """Rumpf aus den Spuren; Lende, Brust, Hals und Kopf werden gegen ihren Elternknochen auf GRENZEN_RUMPF geklemmt."""
    pel = J["Bip01_Pelvis"] + Vector(wert(sp, "pel", t))
    qs = [euler(*[float(x) for x in wert(sp, k, t)]) for k in ("r_pel", "r_sp", "r_ch", "r_ne", "r_he", "r_ta")]
    for i, nm in ((1, "sp_pel"), (2, "ch_sp"), (3, "ne_ch"), (4, "he_ne")):
        y, p, r = ypr(qs[i - 1].inverted() @ qs[i])
        gr = GR_AKTIV["rumpf"][nm]     # 2c: Sitz-Ausnahme nur waehrend der drei Sitz-Clips (sonst GRENZEN_RUMPF wie bisher)
        k3 = (_kl(y, gr[0]), _kl(p, gr[1]), _kl(r, gr[2]))
        if max(abs(k3[0] - y), abs(k3[1] - p), abs(k3[2] - r)) > 1e-6:
            if st is not None:
                _zaehle(st.setdefault("rumpf", {}), nm, t)
            qs[i] = qs[i - 1] @ euler(*k3)
    kf = float(wert(sp, "kiefer", t)[0])
    kf2 = min(max(kf, GRENZE_KIEFER[0]), GRENZE_KIEFER[1])
    if st is not None and abs(kf2 - kf) > 1e-6:
        _zaehle(st.setdefault("rumpf", {}), "kiefer", t)
    pose = {}
    rumpf(pose, pel, *qs, kiefer=kf2)
    for n in "LR":
        kp, kr = (float(x) for x in wert(sp, "klav_" + n, t))
        kp2, kr2 = _kl(kp, GRENZE_KLAV[0]), _kl(kr, GRENZE_KLAV[1])
        if st is not None and max(abs(kp2 - kp), abs(kr2 - kr)) > 1e-6:
            _zaehle(st.setdefault("rumpf", {}), "klav_" + n, t)
        kette(pose, "Bip01_%s_Clavicle" % n, pose["Bip01_Spine1"][0] @ euler(0.0, kp2, kr2))
    return pose


def spuren_bauen(roh, T, anfang=None, ende=None):
    """Fuellt fehlende Spuren, setzt Anfang und Ende (Vorgabe: Grundhaltung), loest Schulterbezuege auf."""
    N = grund()
    A0 = dict(N, **(anfang or {}))
    E0 = dict(N, **(ende or {}))
    unbekannt = set(roh) - set(N)
    assert not unbekannt, unbekannt
    tab = {}
    for k in N:
        ks = [(float(t), v) for t, v in roh.get(k, [])]
        assert all(ks[i][0] < ks[i + 1][0] for i in range(len(ks) - 1)), k
        if not ks or ks[0][0] > 1e-9:
            ks.insert(0, (0.0, A0[k]))
        if ks[-1][0] < T - 1e-9:
            ks.append((T, E0[k]))
        tab[k] = ks
    roh_sp = {k: (np.array([q[0] for q in ks]), [q[1] for q in ks]) for k, ks in tab.items()}
    for key in LEG:
        ts, ys = roh_sp["ball_" + key]
        for i, v in enumerate(ys):
            if isinstance(v[0], str):
                assert v[0] == "S"
                h = hueftpunkt(rumpf_bei(roh_sp, float(ts[i])), key)
                ys[i] = (h.x + v[1][0], h.y + v[1][1], h.z + v[1][2])
    return {k: (ts, np.array(ys, dtype=float)) for k, (ts, ys) in roh_sp.items()}


SCHNAUZE = Vector(BONES["Bip01_Head"][1])


def kampf_pose(sp, t, stat):
    pose = rumpf_bei(sp, t, stat)
    for key in ("VL", "VR", "HL", "HR"):
        L = LEG[key]
        welt = min(1.0, max(0.0, float(wert(sp, "welt_" + key, t)[0])))
        rahmen = pose["Bip01_Spine1" if L["vorn"] else "Bip01_Pelvis"][0]
        ik = min(1.0, max(0.0, float(wert(sp, "ik_" + key, t)[0])))
        bein_kampf(pose, key, Vector(wert(sp, "ball_" + key, t)), euler(*[float(x) for x in wert(sp, "rot_" + key, t)]),
                   [float(x) for x in wert(sp, "rel_" + key, t)], welt, rahmen @ Vector(wert(sp, "pole_" + key, t)).normalized(),
                   stat.setdefault(key, {}), t, ik, [float(x) for x in wert(sp, "fk_" + key, t)])
    toe(pose)
    if stat is not None:
        qh, ph = pose["Bip01_Head"]
        nase = ph + qh @ (SCHNAUZE - J["Bip01_Head"])
        bild = dict(t=round(t, 4), rumpf=rumpf_mass(pose), nase=(nase.x, nase.y, nase.z), **{k: bein_mass(pose, k) for k in LEG})
        for k in LEG:
            L = LEG[k]
            n_b = (pose[L["fuss"]][1] - pose[L["unten"]][1]).cross(pose[L["oben"]][1] - pose[L["unten"]][1])
            s_b = pose[L["fuss"]][0] @ Vector((0, 0, -1))
            bild[k]["rollen"] = _asin(s_b.dot(n_b.normalized())) if n_b.length > 1e-9 else 0.0
            bild[k]["ziel"] = tuple(float(v) for v in wert(sp, "ball_" + k, t))
            bild[k]["halt"] = float(wert(sp, "ik_" + k, t)[0]) > 0.999
        stat.setdefault("bilder", []).append(bild)
    return pose


def kampf_diag(name, sp, zeiten):
    for t in zeiten:
        p = kampf_pose(sp, t, {})
        qh, ph = p["Bip01_Head"]
        nase = ph + qh @ (SCHNAUZE - J["Bip01_Head"])
        zeile = ["t=%.3f" % t, "Schnauze (%.2f %+.2f %.2f)" % tuple(nase), "Kopfgelenk z %.2f" % ph.z]
        for key in ("VL", "VR"):
            qf, pf = p[LEG[key]["fuss"]]
            ball = pf + qf @ (LEG[key]["ball"] - J[LEG[key]["fuss"]])
            zeile.append("%s Ballen (%.2f %+.2f %.2f) = %.2f Kacheln vor Bip01" % (key, ball.x, ball.y, ball.z, ball.x * M2U * 1.5))
        zeile.append("Kiefer %.0f Grad" % float(wert(sp, "kiefer", t)[0]))
        log("DIAG", name, *zeile)


# ------------------------------------------------------------------ die Spuren je Clip
def sp_hieb_l():
    """Prankenhieb links, 1,50 s, Treffer 0,60 s. Fixer 08.11.: Treffpunkt vor der linken Schulter statt vor der Schnauze und
    tiefer (Pranke nie durch den eigenen Kiefer), Kopf dreht im Schlag deutlich weg und hebt sich; Rumpf dreht weiter
    (Brust +16 -> -20, Becken rund 40 % davon), die Hinterbeine laden beim Ausholen und schieben im Schlag (Knie streckt)."""
    sp = {}
    sp["pel"] = [(0.20, (-0.04, -0.035, -0.03)), (0.44, (-0.07, -0.045, -0.045)), (0.58, (0.035, -0.015, 0.004)),
                 (0.66, (0.055, -0.005, 0.0)), (0.82, (0.06, 0.01, -0.02)), (1.05, (0.045, 0.005, -0.02)), (1.40, (0.0, 0.0, -0.004))]
    sp["r_pel"] = [(0.20, (3, -2, 3)), (0.44, (7, -4, 4)), (0.60, (-6, 0, -2)), (0.80, (-9, 2, -3)), (1.10, (-4, 1, -1)), (1.40, R0)]
    sp["r_sp"] = [(0.20, (6, -4, 6)), (0.44, (11, -7, 8)), (0.60, (-11, 1, -1)), (0.80, (-13, 5, -3)), (1.10, (-7, 2, -2)), (1.40, R0)]
    sp["r_ch"] = [(0.20, (10, -8, 10)), (0.44, (16, -10, 12)), (0.60, (-17, 4, -2)), (0.80, (-19, 7, -3)), (1.10, (-9, 3, -2)),
                  (1.40, R0)]
    sp["r_ne"] = [(0.20, (4, -2, 5)), (0.44, (6, -6, 6)), (0.56, (-10, -8, -3)), (0.66, (-20, -6, -4)), (0.84, (-17, 4, -3)),
                  (1.10, (-6, 6, 0)), (1.40, (0, 4, 0))]
    sp["r_he"] = [(0.20, (0, 2, 2)), (0.44, (2, -2, 2)), (0.56, (-16, -10, -6)), (0.66, (-27, -8, -8)), (0.84, (-23, 6, -6)),
                  (1.10, (-8, 6, 0)), (1.40, (0, 4, 0))]
    sp["r_ta"] = [(0.44, (6, -4, 0)), (0.80, (-8, 4, 0)), (1.30, R0)]
    sp["kiefer"] = [(0.12, (6.0,)), (0.40, (18.0,)), (0.60, (22.0,)), (0.80, (16.0,)), (1.10, (4.0,)), (1.30, (0.0,))]
    sp["klav_L"] = [(0.20, (4.0, 6.0)), (0.44, (8.0, 12.0)), (0.60, (-14.0, 4.0)), (0.80, (-10.0, -2.0)), (1.20, (-3.0, 0.0)),
                    (1.40, (0.0, 0.0))]
    sp["klav_R"] = [(0.44, (0.0, 3.0)), (0.80, (2.0, 2.0)), (1.30, (0.0, 0.0))]
    land = NB("VL", 0.30, -0.04, 0.0)
    sp["ball_VL"] = [(0.08, NB("VL")), (0.18, NB("VL", 0.02, 0.02, 0.05)), (0.72, (0.86, 0.25, 0.18)), (0.80, land), (1.08, land),
                     (1.19, NB("VL", 0.15, -0.02, 0.09)), (1.30, NB("VL"))]
    sp["welt_VL"] = [(0.14, (1.0,)), (0.22, (0.0,)), (0.72, (0.0,)), (0.78, (1.0,))]
    sp["rot_VL"] = [(0.08, R0), (0.79, (-10, 0, 0)), (1.08, (-10, 0, 0)), (1.29, R0)]
    sp["ik_VL"] = [(0.12, (1.0,)), (0.20, (0.0,)), (0.66, (0.0,)), (0.77, (1.0,))]
    sp["fk_VL"] = [(0.12, FK0["VL"]), (0.30, (20, 25, -10, 100)), (0.44, (25, 42, -5, 95)), (0.52, (30, 30, -10, 112)),
                   (0.60, (33, 24, -12, 136)), (0.68, (26, 12, -12, 136))]
    sp["rel_VL"] = [(0.08, REL0["VL"]), (0.20, (20, 0, 5)), (0.44, (-35, 0, 15)), (0.52, (-15, 0, 25)), (0.60, (0, 0, 28)),
                    (0.68, (28, 0, 15)), (0.76, (55, 0, 5)), (1.12, (50, 0, 5)), (1.19, (15, 0, 5)), (1.27, REL0["VL"])]
    sp["pole_VL"] = [(0.08, (-1.0, 0.0, 0.0)), (0.80, (-1.0, 0.1, -0.3)), (1.30, (-1.0, 0.0, 0.0))]
    sp["rot_VR"] = [(0.44, R0), (0.62, (-7, 0, 0)), (1.05, (-7, 0, 0)), (1.35, R0)]
    sp["ball_VR"] = [(0.50, NB("VR")), (0.66, NB("VR", 0, 0, 0.005)), (1.05, NB("VR", 0, 0, 0.005)), (1.25, NB("VR"))]
    return sp


def sp_slam():
    """Doppelschlag, 2,40 s, Treffer 1,30 s (anim_referenz.md 7): Hinterbeine laden 0-0,25 (Knie rund 120), halb aufrichten
    0,22-0,90, die Pranken halten vor der Brust UNTER dem Kopf (Ellbogen 104-112; Fixer 08.11.: vorher neben dem Gesicht auf
    Augenhoehe, Unterarme im Kopf, anim_review_optik.md Fund 4), Kopf hoch; dann faellt das ganze Gewicht nach vorn, die
    Hinterbeine schieben (Knie bis rund 150, Fund 5), die Arme strecken sich und landen flach 1,27 (Pfoten erst kurz davor flach),
    Ellbogen federn nach; links tritt 1,55-1,75 zurueck, rechts 1,75-1,95. In der Luft laufen die Arme im Gelenkraum (fk_)."""
    sp = {}
    sp["pel"] = [(0.22, (-0.05, 0, -0.045)), (0.55, (-0.07, 0, 0.0)), (0.90, (-0.08, 0, 0.025)), (1.12, (0.04, 0, 0.03)),
                 (1.25, (0.11, 0, 0.0)), (1.32, (0.12, 0, -0.025)), (1.45, (0.10, 0, -0.05)), (1.75, (0.06, 0, -0.045)),
                 (1.95, (0.03, 0, -0.03)), (2.30, (0.0, 0, -0.004))]
    sp["r_pel"] = [(0.22, (0, 3, 0)), (0.55, (0, -12, 0)), (0.90, (0, -22, 0)), (1.15, (0, -4, 0)), (1.30, (0, 4, 0)),
                   (1.45, (0, 6, 0)), (1.80, (0, 3, 0)), (2.30, R0)]
    sp["r_sp"] = [(0.22, (0, 4, 0)), (0.55, (0, -18, 0)), (0.90, (0, -31, 0)), (1.15, (0, -6, 0)), (1.30, (0, 8, 0)),
                  (1.45, (0, 10, 0)), (1.80, (0, 6, 0)), (2.30, R0)]
    sp["r_ch"] = [(0.22, (0, 4, 0)), (0.55, (0, -26, 0)), (0.90, (0, -42, 0)), (1.15, (0, -8, 0)), (1.30, (0, 14, 0)),
                  (1.45, (0, 17, 0)), (1.80, (0, 10, 0)), (2.30, R0)]
    sp["r_ne"] = [(0.22, (0, 8, 0)), (0.55, (0, -16, 0)), (0.90, (0, -28, 0)), (1.15, (0, 4, 0)), (1.30, (0, 22, 0)),
                  (1.45, (0, 24, 0)), (1.80, (0, 12, 0)), (2.30, (0, 4, 0))]
    sp["r_he"] = [(0.22, (0, 8, 0)), (0.55, (0, -14, 0)), (0.90, (0, -22, 0)), (1.15, (0, 10, 0)), (1.30, (0, 28, 0)),
                  (1.45, (0, 30, 0)), (1.80, (0, 12, 0)), (2.30, (0, 4, 0))]
    sp["r_ta"] = [(0.90, (0, -18, 0)), (1.30, (0, 4, 0)), (2.0, R0)]
    sp["kiefer"] = [(0.10, (4.0,)), (0.40, (18.0,)), (0.90, (24.0,)), (1.15, (26.0,)), (1.30, (14.0,)), (1.50, (6.0,)), (1.80, (0.0,))]
    for n, s in (("L", 1), ("R", -1)):
        k = "V" + n
        sp["klav_" + n] = [(0.55, (-10.0, 3.0 * s)), (0.90, (-16.0, 5.0 * s)), (1.15, (-8.0, 0.0)), (1.30, (-10.0, 0.0)), (1.70, (0.0, 0.0))]
        lauf = (1.55, 1.65, 1.75) if n == "L" else (1.75, 1.85, 1.95)
        land = NB(k, 0.23, -0.01 * s, 0.0)
        sp["ball_" + k] = [(0.24, NB(k)), (0.34, NB(k, -0.02, 0, 0.10)), (1.20, NB(k, 0.23, -0.01 * s, 0.03)), (1.27, land),
                           (lauf[0], land), (lauf[1], NB(k, 0.14, -0.005 * s, 0.08)), (lauf[2], NB(k))]
        sp["welt_" + k] = [(0.34, (1.0,)), (0.44, (0.0,)), (1.18, (0.0,)), (1.25, (1.0,))]
        sp["rot_" + k] = [(0.24, R0), (1.26, R0), (lauf[2], R0)]
        sp["ik_" + k] = [(0.30, (1.0,)), (0.42, (0.0,)), (1.08, (0.0,)), (1.20, (1.0,))]
        sp["fk_" + k] = [(0.30, FK0[k]), (0.55, (6, 8, -8, 112)), (0.90, (-4, 12, -6, 104)), (1.00, (8, 9, -8, 120)), (1.08, (20, 4, -9, 138))]
        sp["rel_" + k] = [(0.24, REL0[k]), (0.44, (20, 0, 5)), (0.90, (-45, 0, 10)), (1.00, (-30, 0, 8)), (1.10, (5, 0, 3)),
                          (1.21, (50, 0, 0)), (lauf[0] + 0.03, (50, 0, 0)), (lauf[1], (15, 0, 0)), (lauf[2] - 0.03, REL0[k])]
        sp["pole_" + k] = [(0.24, (-1.0, 0.0, 0.0)), (1.20, (-1.0, 0.1 * s, -0.3)), (1.40, (-1.0, 0.0, 0.0))]
    return sp


def sp_rear():
    """Aufrichten mit Bruellen, 3,00 s (bleibt): Hochkommen 0,25-0,85 (Becken dreht, Lende fast gerade, Gewicht ueber den
    Hinterpfoten, Hinterbeine stabil), oben 0,85-2,05 mit Bruellen (Maul 0,95-1,85), Ruecken aufrecht, Vorderpranken haengen
    locker vor der Brust (Ellbogen 100-110, Arme im Gelenkraum), Kopf hoch, leichtes Schwanken; herunter 2,05-2,72,
    Aufsetzen am Ruheplatz."""
    sp = {}
    sp["pel"] = [(0.25, (-0.03, 0, -0.03)), (0.55, (-0.05, 0, 0.035)), (0.85, (-0.06, 0, 0.09)), (1.45, (-0.06, 0.01, 0.09)),
                 (2.05, (-0.06, -0.005, 0.09)), (2.40, (-0.04, 0, 0.035)), (2.72, (0.0, 0, -0.03)), (2.88, (0.0, 0, -0.012))]
    sp["r_pel"] = [(0.25, (0, 2, 0)), (0.55, (0, -24, 0)), (0.85, (0, -46, 0)), (1.45, (2, -48, -2)), (2.05, (-1, -46, 2)),
                   (2.40, (0, -28, 0)), (2.72, (0, 2, 0)), (2.88, (0, 1, 0))]
    sp["r_sp"] = [(0.25, (0, 3, 0)), (0.55, (0, -36, 0)), (0.85, (0, -65, 0)), (1.45, (3, -67, -3)), (2.05, (-2, -65, 3)),
                  (2.40, (0, -38, 0)), (2.72, (0, 3, 0))]
    sp["r_ch"] = [(0.25, (0, 4, 0)), (0.55, (0, -44, 0)), (0.85, (0, -78, 0)), (1.25, (4, -80, -3)), (1.85, (-4, -79, 3)),
                  (2.05, (0, -78, 0)), (2.40, (0, -42, 0)), (2.72, (0, 4, 0))]
    sp["r_ne"] = [(0.25, (0, -6, 0)), (0.55, (0, -26, 0)), (0.85, (0, -50, 0)), (1.25, (3, -54, -2)), (1.85, (-3, -53, 2)),
                  (2.05, (0, -50, 0)), (2.40, (0, -14, 0)), (2.72, (0, 6, 0))]
    sp["r_he"] = [(0.25, (0, -2, 0)), (0.55, (0, -18, 0)), (0.85, (0, -36, 0)), (1.05, (-5, -42, 3)), (1.30, (6, -44, -4)),
                  (1.55, (-5, -43, 3)), (1.80, (4, -40, -2)), (2.05, (0, -34, 0)), (2.40, (0, -6, 0)), (2.72, (0, 6, 0))]
    sp["r_ta"] = [(0.55, (0, -15, 0)), (0.85, (0, -35, 0)), (2.05, (0, -35, 0)), (2.50, (0, -8, 0))]
    sp["kiefer"] = [(0.60, (0.0,)), (0.80, (12.0,)), (0.95, (37.0,)), (1.30, (35.0,)), (1.60, (38.0,)), (1.85, (34.0,)),
                    (2.00, (28.0,)), (2.15, (8.0,)), (2.30, (0.0,))]
    for n, s in (("L", 1), ("R", -1)):
        k = "V" + n
        sp["klav_" + n] = [(0.40, (-8.0, 0.0)), (0.85, (-20.0, 3.0 * s)), (2.05, (-20.0, 3.0 * s)), (2.55, (-6.0, 0.0)), (2.80, (0.0, 0.0))]
        sp["ball_" + k] = [(0.28, NB(k)), (0.36, NB(k, -0.02, 0, 0.07)), (2.58, NB(k, 0.02, 0, 0.09)), (2.72, NB(k))]
        sp["welt_" + k] = [(0.28, (1.0,)), (0.36, (0.0,)), (2.64, (0.0,)), (2.71, (1.0,))]
        sp["rot_" + k] = [(0.28, R0), (2.71, R0)]
        sp["ik_" + k] = [(0.32, (1.0,)), (0.42, (0.0,)), (2.48, (0.0,)), (2.60, (1.0,))]
        sp["fk_" + k] = [(0.32, FK0[k]), (0.55, (-22, 6, -8, 118)), (0.85, (-52, 10, -6, 108)), (1.25, (-56, 12, -6, 102)),
                         (1.85, (-50, 10, -6, 110)), (2.05, (-48, 9, -6, 108)), (2.30, (-28, 5, -8, 128)), (2.42, (-12, 2, -9, 138))]
        sp["rel_" + k] = [(0.28, REL0[k]), (0.45, (0, 0, 5)), (0.85, (-38, 0, 10)), (1.25, (-46, 0, 12)), (1.85, (-34, 0, 9)),
                          (2.05, (-38, 0, 10)), (2.35, (5, 0, 5)), (2.56, (45, 0, 0)), (2.70, REL0[k])]
    return sp


def sp_biss():
    """Biss gegen ein stehendes Ziel, 1,30 s, Treffer 0,52 s (anim_referenz.md 6): Ansatz 0-0,17 (duckt, Hinterbeine laden,
    Knie rund 122), Vorstoss 0,17-0,48 mit halbem Aufrichten und langem Hals, die Hinterbeine schieben (Knie bis rund 147,
    Fixer 08.11., anim_review_optik.md Fund 5); die Vorderpfoten machen einen flachen Satz (hoechstens rund 0,24 m, per IK statt
    Arme hochreissen, Fund 8) und setzen 0,07 weiter vorn wieder auf (0,60); Zubeissen und Ruck 0,48-0,58, zweimal Schuetteln
    0,58-0,95 (Brust rollt mit), zurueck mit je einem Schritt."""
    sp = {}
    sp["pel"] = [(0.17, (-0.05, 0, -0.035)), (0.40, (0.08, 0, 0.022)), (0.52, (0.10, 0, 0.008)), (0.62, (0.09, 0, -0.02)),
                 (0.95, (0.06, 0, -0.03)), (1.20, (0.0, 0, -0.004))]
    sp["r_pel"] = [(0.17, (0, 2, 0)), (0.40, (0, -6, 0)), (0.52, (0, -6, 0)), (0.62, (0, -2, 0)), (0.95, (0, 0, 0)), (1.20, R0)]
    sp["r_sp"] = [(0.17, (0, 3, 0)), (0.40, (0, -9, 0)), (0.52, (0, -7, 0)), (0.62, (0, -3, 0)), (0.95, (0, -1, 0)), (1.20, R0)]
    sp["r_ch"] = [(0.17, (0, 4, 0)), (0.40, (0, -15, 0)), (0.52, (0, -10, 0)), (0.58, (0, -3, 0)), (0.66, (4, -2, 4)),
                  (0.76, (-4, -1, -4)), (0.86, (4, 0, 4)), (0.95, (-2, 0, -2)), (1.20, R0)]
    sp["r_ne"] = [(0.17, (0, 10, 0)), (0.40, (0, -36, 0)), (0.52, (0, -32, 0)), (0.58, (0, -20, 0)), (0.66, (14, -16, 6)),
                  (0.76, (-14, -14, -6)), (0.86, (12, -10, 5)), (0.95, (-4, -4, -2)), (1.20, (0, 4, 0))]
    sp["r_he"] = [(0.17, (0, 14, 0)), (0.40, (0, -16, 0)), (0.52, (0, -10, 0)), (0.58, (0, 4, 0)), (0.66, (24, 4, 14)),
                  (0.76, (-24, 6, -14)), (0.86, (20, 6, 12)), (0.95, (-6, 5, -4)), (1.20, (0, 4, 0))]
    sp["r_ta"] = [(0.40, (0, -10, 0)), (0.95, (0, -2, 0))]
    sp["kiefer"] = [(0.08, (4.0,)), (0.30, (24.0,)), (0.44, (34.0,)), (0.52, (6.0,)), (0.56, (3.0,)), (0.95, (3.0,)), (1.10, (0.0,))]
    for n, s in (("L", 1), ("R", -1)):
        k = "V" + n
        sp["klav_" + n] = [(0.17, (2.0, 0.0)), (0.40, (-12.0, 2.0 * s)), (0.60, (-6.0, 0.0)), (1.10, (0.0, 0.0))]
        vor = NB(k, 0.07, -0.01 * s, 0.0)
        lauf = (0.96, 1.05, 1.13) if n == "L" else (1.07, 1.16, 1.24)
        # Satz nach vorn statt Arme hochreissen (Fixer 08.11., anim_review_optik.md Fund 8): die Pfoten bleiben per IK an einem
        # flachen Bogen, hoechstens rund 0,22 m hoch, und landen 0,07 weiter vorn
        sp["ball_" + k] = [(0.18, NB(k)), (0.28, NB(k, 0.02, 0, 0.09)), (0.40, NB(k, 0.06, -0.01 * s, 0.20)),
                           (0.50, NB(k, 0.09, -0.01 * s, 0.14)), (0.58, NB(k, 0.08, -0.01 * s, 0.025)), (0.62, vor),
                           (lauf[0], vor), (lauf[1], NB(k, 0.05, 0, 0.07)), (lauf[2], NB(k))]
        sp["welt_" + k] = [(0.20, (1.0,)), (0.28, (0.0,)), (0.52, (0.0,)), (0.60, (1.0,))]
        sp["rot_" + k] = [(0.18, R0), (0.62, R0), (lauf[2], R0)]
        sp["rel_" + k] = [(0.18, REL0[k]), (0.28, (5, 0, 5)), (0.40, (-20, 0, 5)), (0.52, (15, 0, 3)), (0.61, (48, 0, 0)),
                          (lauf[0] + 0.03, (48, 0, 0)), (lauf[1], (10, 0, 0)), (lauf[2] - 0.03, REL0[k])]
    return sp


def sp_maul():
    """Biss am Boden, 1,60 s, Treffer 0,544 s (anim_referenz.md 6): Kopf und Hals gehen tief (nicht die Vorderbeine), die linke
    Pranke tritt vor und drueckt das Opfer nieder, Biss, zweimal Schuetteln mit rollenden Schultern, zurueck mit Schritt.
    Fixer 08.11.: die haltende Pranke 5 cm weiter aussen und das Schuetteln zur linken Seite kleiner (17 statt 30 Grad), sonst
    drueckt der Kopf in die Pranke (anim_review_optik.md Fund 7)."""
    sp = {}
    sp["pel"] = [(0.20, (0.04, 0, -0.01)), (0.46, (0.12, 0, -0.03)), (0.56, (0.13, 0, -0.035)), (1.12, (0.10, 0, -0.035)),
                 (1.45, (0.02, 0, -0.015))]
    sp["r_pel"] = [(0.20, (0, 2, 0)), (0.46, (0, 4, 0)), (1.12, (0, 4, 0)), (1.45, (0, 1, 0))]
    sp["r_sp"] = [(0.20, (0, 4, 0)), (0.46, (0, 8, 0)), (1.12, (0, 8, 0)), (1.45, (0, 2, 0))]
    sp["r_ch"] = [(0.20, (0, 6, 0)), (0.46, (0, 12, 0)), (0.56, (0, 14, 0)), (0.70, (6, 14, 7)), (0.84, (-6, 14, -7)),
                  (0.98, (6, 14, 7)), (1.12, (-2, 12, -2)), (1.45, (0, 2, 0))]
    sp["r_ne"] = [(0.20, (0, 18, 0)), (0.46, (0, 36, 0)), (0.56, (0, 38, 0)), (0.70, (11, 37, 6)), (0.84, (-16, 37, -9)),
                  (0.98, (10, 36, 5)), (1.12, (-4, 33, -2)), (1.45, (0, 10, 0))]
    sp["r_he"] = [(0.20, (0, 31, 0)), (0.46, (0, 58, 0)), (0.56, (0, 61, 0)), (0.70, (17, 58, 11)), (0.84, (-30, 58, -20)),
                  (0.98, (15, 58, 10)), (1.12, (-6, 50, -3)), (1.45, (0, 12, 0))]
    sp["kiefer"] = [(0.08, (4.0,)), (0.20, (18.0,)), (0.46, (34.0,)), (0.52, (10.0,)), (0.56, (3.0,)), (1.12, (3.0,)), (1.30, (0.0,))]
    sp["klav_L"] = [(0.20, (-4.0, 0.0)), (0.46, (-14.0, -2.0)), (1.12, (-12.0, -2.0)), (1.45, (0.0, 0.0))]
    sp["klav_R"] = [(0.46, (-6.0, 0.0)), (1.12, (-6.0, 0.0)), (1.45, (0.0, 0.0))]
    druck = NB("VL", 0.25, 0.05, 0.0)
    sp["ball_VL"] = [(0.18, NB("VL")), (0.30, NB("VL", 0.13, 0.03, 0.09)), (0.40, druck), (1.25, druck),
                     (1.36, NB("VL", 0.12, 0.03, 0.08)), (1.46, NB("VL"))]
    sp["rot_VL"] = [(0.18, R0), (0.40, (-6, 0, 0)), (1.25, (-6, 0, 0)), (1.46, R0)]
    sp["rel_VL"] = [(0.18, REL0["VL"]), (0.30, (10, 0, 5)), (0.38, (50, 0, 5)), (1.28, (50, 0, 5)), (1.36, (10, 0, 0)),
                    (1.43, REL0["VL"])]
    return sp


# ---- Sitzen und Fressen: Grundposen S (Sitzen nach kevin_sitzvorlage.png) und E (Kopf unten am Futter)
def _pose_s(kopf_gier=10.0):
    """Sitzpose nach kevin_sitzvorlage.png: Hinterteil am Boden (Becken dreht -42, Ruecken rund), Vorderbeine gerade zwischen den
    Hinterbeinen, Pranken flach, Hinterbeine vorn und gespreizt, Sohlen nach vorn-oben, Kopf hoch und leicht zu seiner linken
    Seite. Gemessen an der Haut (pose_probe): mit diesem Skelett reichen die Vorderpfoten nur bis zum Boden, wenn die Schulter
    hoechstens rund 0,72 m hoch ist; deshalb ist die Brust nur -14 Grad aufgerichtet und der Hals traegt den Kopf hoch.
    Fixer 08.11. (anim_review_optik.md Fund 2/3/10): Hinterbeine wirklich nach vorn (Ferse 0,49 vor der Hueftlinie, Knie rund
    141, Fersengelenk 0,16 ueber dem Boden, denn mit hochgestellten Zehen liegt das Fersenpolster 0,15 unter dem Gelenk) und gespreizt (Fersen +-0,57): das runde Netz hat dicke Glieder (Unterarm und
    Unterschenkel je rund 0,17 m Radius um den Knochen, radius.py), enger stecken sie im Vorderbein; Vorderpfoten auf +-0,18
    (vorher 0,12, die Pfoten steckten ineinander). Der Hinterfuss steht jetzt IN WELT (welt 1, Gieren 34 mit dem Bein,
    Nicken -95 = Zehen hoch, Sohle nach vorn): die alte relative Vorgabe rel (-100, -6, 10) lag im toten Winkel der Messgroessen
    -- steht der Fuss quer zum Unterschenkel, sehen dors/seitab/sup das Rollen um die Fusslaengsachse nicht, und der Loeser rollte
    die Sohle 61 Grad nach innen, um 2 Grad seitab zu erfuellen. Hals etwas steiler (-58), Kopf hoeher (-24)."""
    S = dict(pel=(0.075, 0.0, -0.336), r_pel=(0, -42, 0), r_sp=(0, -28, 0), r_ch=(0, -14, 0), r_ne=(kopf_gier * 0.35, -58, 2),
             r_he=(kopf_gier, -24, 5), r_ta=(0, -45, 0), kiefer=(0.0,), klav_L=(-8.0, -12.0), klav_R=(-8.0, 12.0))
    for n, s in (("L", 1), ("R", -1)):
        S["ball_V" + n] = (0.40, 0.18 * s, 0.045)
        S["rot_V" + n] = (8 * s, 0, 0)
        S["welt_V" + n] = (1.0,)
        S["rel_V" + n] = REL0["V" + n]
        S["pole_V" + n] = (-1.0, 0.0, 0.0)
        S["ball_H" + n] = (0.18, 0.58 * s, 0.39)
        S["rot_H" + n] = (34.0 * s, -95.0, 0.0)
        S["welt_H" + n] = (1.0,)
        S["rel_H" + n] = REL0["H" + n]
        S["pole_H" + n] = (0.67, 0.15 * s, 0.74)
    return S


POSE_S = _pose_s()

# ---- Lauf baer-2c, Bau Sitzen (10.11.2026): neue Sitzpose S_neu nach Kevins Sitzvorlage (SPEZ_2C.md 5.2, Kandidat K2) auf dem Netz von
# Bau Koerper (schmaler Rumpf, kurzer Hinterfuss). Rumpf aufgerichtet (Brust bis -40 moeglich: SPEZ 5.1; gewaehlt -37, s. u.), Hals
# steil, Kopf geradeaus OBEN auf dem Koerper; Hinterbeine eng nach vorn, Ferse liegt auf, Sohle nach vorn-oben; Vorderbeine gerade
# zwischen den Hinterbeinen, Pranken flach. Becken- und Sprunggelenkhoehe am fertigen Netz geloest (Haut: Sitzflaeche und Ferse auf dem
# Boden; Probe _arbeit/baer_2c/sitzen/werkzeug/pose_probe_2c.py, Bericht bau_sitzen.md). Die alte Pose oben (_pose_s) bleibt nur fuer die
# Vorschau-Variante (b).
# Neustart Bau Sitzen (Probe p25-p29, Bilder sitzen/blatt/p25.png, p28.png): mit Brust -40 / Lende -25 (Brust gegen Lende -15, Grenze)
# zieht die Haut zwischen den Schulterblaettern eine scharfe Querfalte (85 Dreiecke sigma2 < 0,55, min 0,06; von hinten sichtbar), und
# Kopf -24 an Hals -82 schaut deutlich nach oben (von vorn sieht man unter das Kinn). Jetzt: Brust -37, Lende -27 (Brust gegen Lende -10:
# Falte weich, 46 Dreiecke, min 0,24), Schulterblatt nicken 16 (Schulter tiefer, Pranken bleiben flach), Hals -78, Kopf -20 (Kopf gegen
# Hals +57,5, Sitz-Ausnahme). Gemessen p29: Sitzflaeche +0,2, Ferse +0,15, Pranken 0,0; Schulter 0,725, Ellbogen innen 163; Huefte 0,33;
# Fussmitten 71,3 cm; Kopf oben 1,31; Achsel 3,09, Leiste 2,56. Hinterfuss-Nicken -91 statt -95..-110 der Spez: steiler stoesst der Fuss
# gegen den Unterschenkel (Grenze dors -125, das Klemmen rollte die Sohle bis 50 Grad; Probe des ersten Bauers).
SITZ_2C = dict(
    becken=(-0.29, 0.40572),               # Ursprung Bip01_Pelvis x, z (Welt, Tier-Rahmen); z geloest: Sitzflaeche/Unterschenkel auf dem Boden
    # fix1 2c (Pruefbericht M1, Kragen hinter/neben dem Kopf = Buckel, fix1/log/kragen_ort.txt): Brust -37 -> -40 (Spez 5.2), Hals -78 ->
    # -77,5 (Kopf-Oberkante <= ~1,32), Schulterblatt 16 -> 18 (Schulter tiefer, Pranken bleiben flach). Probe fix1/probe/pe.py + pf.py:
    # Kragen Spielkamera hinter +5,3 -> +3,8 cm, seitlich -9,2 -> -10,9 (Bild 0, f4-Netz), Pfoten 0,00, Ferse 0,09, keine Klemmung
    r_pel=(0.0, -35.0, 0.0), r_sp=(0.0, -27.0, 0.0), r_ch=(0.0, -40.0, 0.0), r_ne=(4.2, -77.5, 2.0), r_he=(12.0, -20.0, 5.0),
    r_ta=(0.0, -35.0, 0.0),
    klav=(18.0, -3.0),                     # Schulterblatt nicken, rollen (links; rechts gespiegelt); fix1 2c 16 -> 18
    vpf=(0.40, 0.12, 0.045), vgier=4.0,    # Vorderpfote: Ballen x, |y|, z; Gieren (Zehen leicht nach aussen)
    sprung=(0.18, 0.335, 0.08111),         # Hinterbein: Sprunggelenk x, |y|, z (Welt); z geloest: Ferse 1,5 mm ueber dem Boden
    fuss=(20.0, -91.0, 5.0),               # Hinterfuss in Welt: Gieren (Zehen nach aussen), Nicken (- = Zehen hoch), Rollen
    hpole=(0.67, 0.15, 0.74),              # Kniepol im Becken-Rahmen (Knie vorn-aussen)
)

if JUNGES:     # ==== JUNGES (D): Soll-Pose S_J (SPEZ_JUNGES D.4); Vorgabe = am Netz des Jungen geloest (bau_koerper.md), Datei ueberschreibt
    # RIG: S_J des GENERATOR-Jungen, am Netz rig/skelett/netz_rig.npz geloest (rig/werkzeug/sitz_loesen.py s1-s4, Uebergaenge td, 11.11.):
    # Sitzflaeche +0,15 cm, Ferse +0,10 cm, Pranken 0,0 cm, Hueftmitte x -0,29, Handgelenk 1,5 cm vor der Schulter. Kurzer Hals mit C7 senkrecht
    # ueber Spine1: Hals nur -25 (der Erwachsenen-Wert -66,8 zog den Kopf 11 cm hinter die Schulter), Kopf -7 (Blick Augen-Nase -34,9,
    # Kopf oben 1,28 m, Atlas 1,5 cm hinter dem Schultergelenk; Varianten k1-k3).
    # NACHBESSERUNG 11.11. (PRUEF_TECHNIK M2: Unterschenkel steckte 6-16 Punkte / bis 3,3 cm im Unterarm derselben Seite, Strahl-Test):
    # Kniepol nach aussen (hpole y 0,15 -> 0,30: das Knie geht bis an die Drehgrenze des Oberschenkels, "schwenk" im Log), Sprunggelenk
    # |y| 0,345 -> 0,37 (Hinterfuss-Mitten 0,742), Hinterfuss-Gieren 20 -> 8 (der Fuss wird an der Pfotengrenze geklemmt; Zehen zeigen
    # 34 statt 18 Grad nach aussen), Vorderpranken |y| 0,098 -> 0,095 (Luecke 1,0 cm), Zwischenplatz (0,40 / 0,095) -> (0,40 / 0,09).
    # Geloest mit rig/fix/werkzeug/sitz_loesen_fix.py (Variante s6) und gemessen mit den ENDgewichten (clips/gewichte_end.npz):
    # Strahl-Test 0 Punkte in SitDown/Sit/StandUp, Dehnung max 3,79 (Leiste). Neu waehlbar: ferse_dy_auf (Aufstehen), Vorgabe = ferse_dy.
    SITZ_2C = dict(
        becken=(-0.2453, 0.3939),              # Ursprung Bip01_Pelvis x, z; z am Netz geloest (Sitzflaeche auf dem Boden)
        r_pel=(0.0, -40.0, 0.0), r_sp=(0.0, -35.0, 0.0), r_ch=(0.0, -47.0, 0.0), r_ne=(4.2, -25.0, 2.0), r_he=(12.0, -7.0, 5.0),
        r_ta=(0.0, -45.0, 0.0),
        klav=(19.5, -3.0),                     # Schulterblatt-Grenze 20 (GRENZE_KLAV)
        vpf=(0.356, 0.095, 0.042), vgier=4.0,  # Ballen x, |y|, z (Ruhe-Ballen z 0,042: Pranke flach)
        sprung=(0.235, 0.37, 0.1392),          # Sprunggelenk x, |y|, z; z am Netz geloest (Ferse liegt auf; Sprunggelenk mitten ueber der Sohle)
        fuss=(8.0, -91.0, 5.0),
        hpole=(0.67, 0.30, 0.74),
        ferse_dy=0.09,                         # Hinterbein-Schritt in die Sitzlage: Sprunggelenk 9 cm nach aussen ausweichen
    )
    V_ZW_J = (0.40, 0.09)
    if os.environ.get("NCB_JUNGES_SITZ"):
        _par = _json.load(open(os.environ["NCB_JUNGES_SITZ"]))
        V_ZW_J = tuple(_par.pop("v_zw", V_ZW_J))
        SITZ_2C.update({k: (tuple(v) if isinstance(v, list) else v) for k, v in _par.items()})


def _pose_s2c(par=None):
    p = dict(SITZ_2C, **(par or {}))
    S = dict(pel=(p["becken"][0] - J["Bip01_Pelvis"].x, 0.0, p["becken"][1] - J["Bip01_Pelvis"].z), kiefer=(0.0,),
             klav_L=(p["klav"][0], p["klav"][1]), klav_R=(p["klav"][0], -p["klav"][1]))
    for k in ("r_pel", "r_sp", "r_ch", "r_ne", "r_he", "r_ta"):
        S[k] = tuple(float(v) for v in p[k])
    for n, s in (("L", 1), ("R", -1)):
        S["ball_V" + n] = (p["vpf"][0], p["vpf"][1] * s, p["vpf"][2])
        S["rot_V" + n] = (p["vgier"] * s, 0.0, 0.0)
        S["welt_V" + n] = (1.0,)
        S["rel_V" + n] = REL0["V" + n]
        S["pole_V" + n] = (-1.0, 0.0, 0.0)
        L = LEG["H" + n]
        rot = (p["fuss"][0] * s, p["fuss"][1], p["fuss"][2] * s)
        A = Vector((p["sprung"][0], p["sprung"][1] * s, p["sprung"][2]))
        S["ball_H" + n] = tuple(float(v) for v in A + euler(*rot) @ (L["ball"] - J[L["fuss"]]))
        S["rot_H" + n] = rot
        S["welt_H" + n] = (1.0,)
        S["rel_H" + n] = REL0["H" + n]
        S["pole_H" + n] = (p["hpole"][0], p["hpole"][1] * s, p["hpole"][2])
    return S


def _pose_e(kopf=0.0):
    """Fresspose: steht, Kopf unten am Futter vor den Pfoten, linke Pranke etwas vor auf dem Futter."""
    E = dict(pel=(0.05, 0.0, -0.03), r_pel=(0, 4, 0), r_sp=(0, 8, 0), r_ch=(0, 10, 0), r_ne=(0, 50 - kopf, 0), r_he=(0, 62 - kopf, 0),
             r_ta=(0, 0, 0), kiefer=(18.0,), klav_L=(-8.0, 0.0), klav_R=(-4.0, 0.0))
    E["ball_VL"] = NB("VL", 0.06, -0.02, 0.0)
    E["rot_VL"] = (-6, 0, 0)
    return E


POSE_E = _pose_e()


def _abschnitt(sp, k, ks):
    sp.setdefault(k, []).extend(ks)


def _schritt(sp, key, t0, t1, von, nach, rot_von, rot_nach, hub=0.06, rel_mitte=None, pol=None, welt=(1.0, 1.0), rel=(None, None)):
    """Ein Schritt eines Beins von t0 bis t1: Ballen von 'von' nach 'nach' mit Hub, Pfote in der Luft relativ zum Unterarm.
    welt/rel: Art der Pfote am Anfang und am Ende (1 = flach in Welt, 0 = relativ mit rel)."""
    m = tuple(0.5 * (von[i] + nach[i]) for i in range(3))
    r0, r1 = rel[0] or REL0[key], rel[1] or REL0[key]
    sp.setdefault("ball_" + key, []).extend([(t0, von), (0.5 * (t0 + t1), (m[0], m[1], m[2] + hub)), (t1, nach)])
    # Pfote bleibt im Schritt flach in Welt (sonst tauchen beim Abheben und Aufsetzen die Zehen in den Boden), nur wo Anfang
    # oder Ende relativ ist, wird ueber den Schritt umgeblendet
    sp.setdefault("welt_" + key, []).extend([(t0, (welt[0],)), (t1, (welt[1],))])
    sp.setdefault("rot_" + key, []).extend([(t0, rot_von), (t1, rot_nach)])
    sp.setdefault("rel_" + key, []).extend([(t0, r0), (0.5 * (t0 + t1), rel_mitte or tuple(0.5 * (r0[i] + r1[i]) for i in range(3))), (t1, r1)])
    if pol:
        sp.setdefault("pole_" + key, []).extend([(t0, pol[0]), (t1, pol[1])])


def _fuss_flach_bis(sp, key, tm, rot):
    """Fixer 08.11.: im Schritt in die Sitzpose bzw. aus ihr heraus steht der Hinterfuss bis zur Mitte (tm) flach (rot), erst
    dann drehen sich die Zehen hoch bzw. kommen herunter -- sonst stehen die Zehen mitten im Schritt hoch und stechen in den
    Unterarm (Messung Aufstehen 0,27 s: 59 Fusspunkte im Unterarm)."""
    ks = sp["rot_" + key]
    i = max(j for j, (tt, _v) in enumerate(ks) if tt < tm)
    ks.insert(i + 1, (tm, rot))


def _misch(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(len(a)))


def sp_setzen():
    """Hinsetzen, 1,60 s (Grundhaltung -> S): die Hinterknie beugen, Gewicht nach hinten (0-0,30); jede Hinterpfote geht einen
    halben Schritt nach vorn und leicht nach aussen (links 0,25-0,47, rechts 0,42-0,64), damit das Becken absinken kann; dann
    strecken sich die Hinterbeine gespreizt nach vorn, Ferse auf, Sohle nach vorn (beide 0,68-0,94), Hinterteil
    am Boden bei rund 1,00; ERST DANACH ruecken die Vorderpfoten zwischen die Hinterbeine (1,02-1,18 / 1,14-1,30; Fixer 08.11.:
    in der alten Reihenfolge fuhr der Unterschenkel durch den Unterarm); Kopf dreht zur Seite."""
    S = POSE_S
    g = grund()
    sp = {}
    sp["pel"] = [(0.30, (-0.01, 0, -0.08)), (0.60, _misch(g["pel"], S["pel"], 0.50)), (0.85, _misch(g["pel"], S["pel"], 0.80)),
                 (1.00, _misch(g["pel"], S["pel"], 0.93)), (1.20, _misch(g["pel"], S["pel"], 0.995)), (1.35, S["pel"])]
    for k, u in (("r_pel", (0.15, 0.50, 0.85, 0.97)), ("r_sp", (0.12, 0.45, 0.80, 0.95)), ("r_ch", (0.05, 0.30, 0.65, 0.88)),
                 ("r_ne", (0.05, 0.25, 0.55, 0.80)), ("r_he", (0.02, 0.15, 0.40, 0.70)), ("r_ta", (0.1, 0.4, 0.8, 1.0))):
        sp[k] = [(0.30, _misch(g[k], S[k], u[0])), (0.60, _misch(g[k], S[k], u[1])), (0.85, _misch(g[k], S[k], u[2])),
                 (1.00, _misch(g[k], S[k], u[3])), (1.40, S[k])]
    for n in "LR":
        sp["klav_" + n] = [(0.70, _misch(g["klav_" + n], S["klav_" + n], 0.3)), (1.00, S["klav_" + n])]
    for n, s in (("L", 1), ("R", -1)):
        h, v = "H" + n, "V" + n
        halb = NB(h, 0.32, 0.10 * s, 0.0)
        t1 = (0.25, 0.47) if n == "L" else (0.42, 0.64)
        # Fixer 08.11.: erst die Hinterbeine nach vorn, DANN die Vorderpfoten nach innen -- umgekehrt fuhr der Unterschenkel durch
        # den schon eingeruekten Unterarm (das runde Netz hat dicke Glieder, Messung 83 Punkte bei 0,93 s)
        t2 = (0.68, 0.94)                       # beide zugleich (spaeter rechts: Sohle springt bis 37 Grad je Bild)
        tV = (1.02, 1.18) if n == "L" else (1.14, 1.30)
        hr = (14.0 * s, 0.0, 0.0)               # halber Schritt leicht nach aussen gedreht (sonst klemmt das Fussgelenk)
        _schritt(sp, h, t1[0], t1[1], NB(h), halb, R0, hr, 0.06)
        # Hub 0,06: der Fuss bleibt bis 40 % flach (_fuss_flach_bis), mit mehr Hub stoesst der Oberschenkel an seine Grenze
        _schritt(sp, h, t2[0], t2[1], halb, S["ball_" + h], hr, S["rot_" + h], 0.06, None, ((1.0, 0.0, 0.0), S["pole_" + h]),
                 (1.0, S["welt_" + h][0]), (REL0[h], S["rel_" + h]))
        _fuss_flach_bis(sp, h, t2[0] + 0.40 * (t2[1] - t2[0]), hr)
        _schritt(sp, v, tV[0], tV[1], NB(v), S["ball_" + v], R0, S["rot_" + v], 0.06, (25, 0, 5))
    return sp


def sp_sitzen():
    """Sitzen-Schleife, 4,00 s, erstes = letztes Bild = S: Atmen (Brust nicken +-1,5, zwei Zuege), der Kopf schaut langsam
    um (gieren 10 -> 28 -> 10); Pfoten fest."""
    sp = {}
    b = POSE_S["r_ch"]
    sp["r_ch"] = [(0.0, b), (1.0, (b[0], b[1] - 2.0, b[2])), (2.0, b), (3.0, (b[0], b[1] - 2.0, b[2])), (4.0, b)]
    ne, he = POSE_S["r_ne"], POSE_S["r_he"]
    sp["r_ne"] = [(0.0, ne), (2.0, (ne[0] + 7.0, ne[1] + 0.5, ne[2] + 1.0)), (4.0, ne)]
    sp["r_he"] = [(0.0, he), (2.0, (he[0] + 18.0, he[1] - 3.0, he[2] + 3.0)), (4.0, he)]
    sp["kiefer"] = [(0.0, (0.0,)), (2.6, (0.0,)), (2.9, (5.0,)), (3.3, (0.0,)), (4.0, (0.0,))]
    return sp


def sp_aufstehen():
    """Aufstehen, 1,30 s (S -> Grundhaltung), Spiegel von sp_setzen (Fixer 08.11.): zuerst gehen die Vorderpfoten auf den
    Ruheplatz (links 0-0,15, rechts 0,10-0,25), dann ziehen sich die Hinterbeine halb unter den Koerper (0,14-0,40 / 0,26-0,52),
    der Oberkoerper legt sich nach vorn und das Hinterteil hebt; dann die Hinterpfoten ganz zurueck (0,55-0,75 / 0,72-0,92), ab
    0,92 in die Grundhaltung."""
    S = POSE_S
    g = grund()
    sp = {}
    sp["pel"] = [(0.25, _misch(S["pel"], g["pel"], 0.10)), (0.45, _misch(S["pel"], g["pel"], 0.45)), (0.70, _misch(S["pel"], g["pel"], 0.80)),
                 (0.95, _misch(S["pel"], g["pel"], 0.98))]
    for k, u in (("r_pel", (0.25, 0.55, 0.85, 0.98)), ("r_sp", (0.30, 0.60, 0.88, 0.98)), ("r_ch", (0.35, 0.65, 0.90, 0.98)),
                 ("r_ne", (0.35, 0.65, 0.92, 1.0)), ("r_he", (0.30, 0.60, 0.92, 1.0)), ("r_ta", (0.3, 0.6, 0.9, 1.0))):
        sp[k] = [(0.25, _misch(S[k], g[k], u[0])), (0.45, _misch(S[k], g[k], u[1])), (0.70, _misch(S[k], g[k], u[2])),
                 (0.95, _misch(S[k], g[k], u[3]))]
    for n in "LR":
        sp["klav_" + n] = [(0.25, S["klav_" + n]), (0.60, g["klav_" + n])]
    for n, s in (("L", 1), ("R", -1)):
        h, v = "H" + n, "V" + n
        halb = NB(h, 0.32, 0.10 * s, 0.0)
        # Fixer 08.11.: erst die Vorderpfoten nach aussen-vorn, dann die Hinterbeine unter den Koerper (Spiegel von sp_setzen)
        tV = (0.00, 0.15) if n == "L" else (0.10, 0.25)
        t1 = (0.14, 0.40) if n == "L" else (0.26, 0.52)
        t2 = (0.55, 0.75) if n == "L" else (0.72, 0.92)
        hr = (14.0 * s, 0.0, 0.0)
        _schritt(sp, h, t1[0], t1[1], S["ball_" + h], halb, S["rot_" + h], hr, 0.06, None, (S["pole_" + h], (1.0, 0.0, 0.0)),
                 (S["welt_" + h][0], 1.0), (S["rel_" + h], REL0[h]))
        _fuss_flach_bis(sp, h, t1[0] + 0.60 * (t1[1] - t1[0]), hr)
        _schritt(sp, h, t2[0], t2[1], halb, NB(h), hr, R0, 0.06)
        _schritt(sp, v, tV[0] + 1e-3, tV[1], S["ball_" + v], NB(v), S["rot_" + v], R0, 0.06, (25, 0, 5))
    return sp


# ---- Lauf baer-2c, Bau Sitzen: die drei Sitz-Clips neu auf S_neu (SITZ_2C). Dauer, Bilderzahl, Schleife und Ereignisse wie bisher
# (T_SETZEN 1,6 / T_SITZEN 4,0 Schleife / T_AUFSTEHEN 1,3; NCBearDone setzt die XML am Ende, der Clip traegt keine Ereignisse). Die alten
# sp_setzen/sp_sitzen/sp_aufstehen oben werden nicht mehr gebaut (nur noch Vorlage). Neu gegen baer-anim: die Hinterbeine gehen in die ENGE
# Lage (Sprunggelenke +-0,335 statt +-0,57) und kommen damit dorthin, wo die Vorderpfoten im Stand stehen; deshalb ruecken die Vorderpfoten
# ZUERST einen kleinen Schritt nach innen (Zwischenplatz V_ZW), dann kommen die Hinterbeine nach vorn, zuletzt gehen die Vorderpfoten den
# Schritt zurueck zwischen die Hinterbeine (beim Aufstehen umgekehrt). Lehre des Fixers baer-anim bleibt: Fuss bis zur Schrittmitte flach.
POSE_S2C = _pose_s2c()
V_ZW = (0.43, 0.125)                       # Zwischenplatz der Vorderpfoten (Ballen x, |y|): eng, noch vorn; fix1 2c: x 0,44 -> 0,43
if JUNGES:     # ==== JUNGES (E): Zwischenplatz der Vorderpfoten des Jungen (Ruhe-Ballen x 0,424 statt 0,48)
    V_ZW = V_ZW_J
#   (mit Brust -40 und dem breiteren Hinterfuss stach in SitDown Bild 29-30 eine Hinterzehe 1 Punkt in den Unterarm; Probe fix1/probe/pi.py: 0)


def _ausweichen(sp, key, tm, dy):
    """Verschiebt den Mittel-Schluessel eines Schritts (Zeit tm) seitlich um dy."""
    ks = sp["ball_" + key]
    i = [j for j, (tt, _v) in enumerate(ks) if abs(tt - tm) < 1e-9][0]
    v = ks[i][1]
    ks[i] = (tm, (v[0], v[1] + dy, v[2]))


def _vzw(n):
    s = 1 if n == "L" else -1
    return (V_ZW[0], V_ZW[1] * s, 0.045)


FERSE_WEG = True     # Neustart Bau Sitzen: Hinterbein-Schritt in die Sitzlage/aus ihr ueber den Weg des Sprunggelenks (p34), sonst wie zuvor


def _ferse_weg(sp, key, t0, t1, hub=0.025, dy=0.0, n=5):
    """Neustart Bau Sitzen (Probe p34): Schritt des Hinterbeins zwischen flachem Fuss und Sitzlage (Sohle nach vorn). Bisher lief der
    BALLEN mit 6 cm Hub von der Schrittmitte in die Sitzlage; weil der Ballen dort ~31 cm hoch steht (Fuss senkrecht), hob das das
    Sprunggelenk bis 0,27 m und faltete das Knie bis 59-62 Grad (Bild 24, scharfe Knitter an Knie und Schenkel). Jetzt laeuft das
    SPRUNGGELENK flach (Hub 'hub', seitlich 'dy' in der Mitte) und der Fuss dreht dabei um die Ferse (Drehung glatt von Anfang zu Ende);
    der Ballen folgt aus Sprunggelenk + Drehung. Ersetzt die Ballen- und Drehungs-Schluessel innerhalb (t0, t1) durch n Zwischenschluessel."""
    L = LEG[key]
    fv = L["ball"] - J[L["fuss"]]
    kb, kr = sp["ball_" + key], sp["rot_" + key]
    b0 = [v for t, v in kb if abs(t - t0) < 1e-9][0]
    b1 = [v for t, v in kb if abs(t - t1) < 1e-9][0]
    r0 = [v for t, v in kr if abs(t - t0) < 1e-9][0]
    r1 = [v for t, v in kr if abs(t - t1) < 1e-9][0]
    h0 = Vector(b0) - euler(*r0) @ fv
    h1 = Vector(b1) - euler(*r1) @ fv
    nb, nr = [], []
    for k in range(1, n + 1):
        u = k / (n + 1.0)
        w = u * u * (3.0 - 2.0 * u)
        t = t0 + u * (t1 - t0)
        r = tuple(r0[i] + (r1[i] - r0[i]) * w for i in range(3))
        hk = h0 + (h1 - h0) * w + Vector((0.0, dy * math.sin(math.pi * u), hub * math.sin(math.pi * u)))
        nb.append((t, tuple(float(x) for x in hk + euler(*r) @ fv)))
        nr.append((t, r))
    sp["ball_" + key] = sorted([(t, v) for t, v in kb if not (t0 + 1e-9 < t < t1 - 1e-9)] + nb, key=lambda q: q[0])
    sp["rot_" + key] = sorted([(t, v) for t, v in kr if not (t0 + 1e-9 < t < t1 - 1e-9)] + nr, key=lambda q: q[0])


def sp_setzen_2c():
    """Hinsetzen, 1,60 s (Grundhaltung -> S_neu): 0-0,30 Gewicht nach hinten, Hinterknie beugen; 0,15-0,43 Vorderpfoten je ein kleiner
    Schritt nach innen (links 0,15-0,31, rechts 0,27-0,43); 0,25-0,64 Hinterpfoten je ein halber Schritt nach vorn (links 0,25-0,47,
    rechts 0,42-0,64); 0,45-0,80 Schulterblatt rollt ein; 0,68-0,94 beide Hinterbeine nach vorn in die enge Lage (Sprunggelenk flach,
    Schrittmitte 3 cm aussen, Fuss dreht um die Ferse: _ferse_weg), Ferse auf, Sohle nach vorn; Hinterteil am Boden ab ~1,00;
    0,95-1,40 Oberkoerper richtet sich auf (Brust -> -37, Hals -> -78, Kopf geradeaus); 1,02-1,30 Vorderpfoten je ein Schritt zurueck
    zwischen die Hinterbeine (links 1,02-1,18, rechts 1,14-1,30); 1,40-1,60 Setzen, Kopf zur Seite."""
    S = POSE_S2C
    g = grund()
    sp = {}
    sp["pel"] = [(0.30, (-0.01, 0, -0.08)), (0.60, _misch(g["pel"], S["pel"], 0.50)), (0.85, _misch(g["pel"], S["pel"], 0.80)),
                 (1.00, _misch(g["pel"], S["pel"], 0.95)), (1.20, _misch(g["pel"], S["pel"], 0.995)), (1.35, S["pel"])]
    for k, u in (("r_pel", (0.15, 0.50, 0.85, 0.97)), ("r_sp", (0.10, 0.35, 0.65, 0.85)), ("r_ch", (0.03, 0.15, 0.35, 0.60)),
                 ("r_ne", (0.03, 0.15, 0.35, 0.60)), ("r_he", (0.02, 0.15, 0.35, 0.60)), ("r_ta", (0.1, 0.4, 0.8, 1.0))):
        sp[k] = [(0.30, _misch(g[k], S[k], u[0])), (0.60, _misch(g[k], S[k], u[1])), (0.85, _misch(g[k], S[k], u[2])),
                 (1.00, _misch(g[k], S[k], u[3])), (1.40, S[k])]
    for n in "LR":
        # Schulterblatt frueh einrollen (Ellbogen naeher an den Koerper), bevor die Hinterfuesse neben dem Unterarm hochkommen (Probe p18)
        sp["klav_" + n] = [(0.45, _misch(g["klav_" + n], S["klav_" + n], 0.5)), (0.80, S["klav_" + n])]
    for n, s in (("L", 1), ("R", -1)):
        h, v = "H" + n, "V" + n
        halb = NB(h, 0.31, 0.10 * s, 0.0)
        tV1 = (0.15, 0.31) if n == "L" else (0.27, 0.43)
        t1 = (0.25, 0.47) if n == "L" else (0.42, 0.64)
        t2 = (0.68, 0.94)
        tV2 = (1.02, 1.18) if n == "L" else (1.14, 1.30)
        hr = (14.0 * s, 0.0, 0.0)
        _schritt(sp, v, tV1[0], tV1[1], NB(v), _vzw(n), R0, R0, 0.05, (25, 0, 5))
        _schritt(sp, h, t1[0], t1[1], NB(h), halb, R0, hr, 0.06)
        _schritt(sp, h, t2[0], t2[1], halb, S["ball_" + h], hr, S["rot_" + h], 0.06, None, ((1.0, 0.0, 0.0), S["pole_" + h]),
                 (1.0, S["welt_" + h][0]), (REL0[h], S["rel_" + h]))
        if FERSE_WEG:
            _ferse_weg(sp, h, t2[0], t2[1], 0.025, SITZ_2C.get("ferse_dy", 0.03) * s)     # RIG: Ausweichen waehlbar (p34)
        else:
            _fuss_flach_bis(sp, h, t2[0] + 0.40 * (t2[1] - t2[0]), hr)
            _ausweichen(sp, h, 0.5 * (t2[0] + t2[1]), 0.03 * s)     # Schrittmitte 3 cm weiter aussen: Zehen am Unterarm vorbei (Probe p18)
        _schritt(sp, v, tV2[0], tV2[1], _vzw(n), S["ball_" + v], R0, S["rot_" + v], 0.05, (25, 0, 5))
    return sp


def sp_sitzen_2c():
    """Sitzen-Schleife, 4,00 s, erstes = letztes Bild = S_neu: Atmen (Brust nicken +1,8, zwei Zuege; nach vorn: Brust gegen
    Lende bleibt so zwischen -10 und -8, die Rueckenfalte waechst nicht), der Kopf schaut langsam um (gieren 12 -> 27 -> 12, Hals mit 50 %), Kiefer 5 Grad bei 2,9 s;
    Pfoten fest."""
    S = POSE_S2C
    sp = {}
    b = S["r_ch"]
    sp["r_ch"] = [(0.0, b), (1.0, (b[0], b[1] + 1.8, b[2])), (2.0, b), (3.0, (b[0], b[1] + 1.8, b[2])), (4.0, b)]
    ne, he = S["r_ne"], S["r_he"]
    # Hals traegt 50 % des Umschauens, der Kopf rollt beim Umschauen 3 Grad zurueck: bei steilem Hals wird Gieren des Kopfes gegen den
    # Hals zu Rollen; so bleibt Kopf gegen Hals rollen <= 25 und nicken <= 58 (Sitz-Grenze 60) ohne Klemmen (Probe p19/p21)
    sp["r_ne"] = [(0.0, ne), (2.0, (ne[0] + 7.5, ne[1] + 0.5, ne[2] + 1.0)), (4.0, ne)]
    sp["r_he"] = [(0.0, he), (2.0, (he[0] + 15.0, he[1] - 1.0, he[2] - 3.0)), (4.0, he)]
    sp["kiefer"] = [(0.0, (0.0,)), (2.6, (0.0,)), (2.9, (5.0,)), (3.3, (0.0,)), (4.0, (0.0,))]
    return sp


def sp_aufstehen_2c():
    """Aufstehen, 1,30 s (S_neu -> Grundhaltung). Gemessen (Probe p13-p15, Windungszahl und Haut): die Hinterbeine muessen ZUERST unter
    den Koerper (links 0,06-0,34, rechts 0,16-0,44, halber Schritt nach x -0,25+0,25), solange das Becken noch steht -- hebt oder dreht
    sich das Becken vorher, streckt sich das Bein gegen den festen Fuss und der Unterschenkel drueckt bis 2 cm in den Boden; die
    Vorderpfoten gehen erst danach auf den Zwischenplatz (links 0,40-0,54, rechts 0,52-0,66; vorher stach die Zehe des Hinterfusses in
    den nach vorn geneigten Unterarm, 19-20 Punkte). 0,20-0,95 Hinterteil hebt, Oberkoerper nach vorn; 0,55-0,92 Hinterpfoten ganz
    zurueck (links 0,55-0,75, rechts 0,72-0,92); 0,92-1,18 Vorderpfoten nach aussen auf den Ruheplatz (links 0,92-1,06, rechts
    1,04-1,18); danach Grundhaltung."""
    S = POSE_S2C
    g = grund()
    sp = {}
    sp["pel"] = [(0.20, S["pel"]), (0.35, _misch(S["pel"], g["pel"], 0.15)), (0.50, _misch(S["pel"], g["pel"], 0.45)),
                 (0.70, _misch(S["pel"], g["pel"], 0.80)), (0.95, _misch(S["pel"], g["pel"], 0.98))]
    for k, u in (("r_pel", (0.10, 0.45, 0.80, 0.98)), ("r_sp", (0.15, 0.50, 0.85, 0.98)), ("r_ch", (0.35, 0.65, 0.90, 0.98)),
                 ("r_ne", (0.35, 0.65, 0.90, 0.98)), ("r_he", (0.35, 0.65, 0.90, 0.98)), ("r_ta", (0.3, 0.6, 0.9, 1.0))):
        sp[k] = [(0.25, _misch(S[k], g[k], u[0])), (0.45, _misch(S[k], g[k], u[1])), (0.70, _misch(S[k], g[k], u[2])),
                 (0.95, _misch(S[k], g[k], u[3]))]
    for n in "LR":
        sp["klav_" + n] = [(0.25, _misch(S["klav_" + n], g["klav_" + n], 0.3)), (0.60, g["klav_" + n])]
    for n, s in (("L", 1), ("R", -1)):
        h, v = "H" + n, "V" + n
        halb = NB(h, 0.25, 0.08 * s, 0.0)
        t1 = (0.06, 0.34) if n == "L" else (0.16, 0.44)
        tV1 = (0.40, 0.54) if n == "L" else (0.52, 0.66)
        t2 = (0.55, 0.75) if n == "L" else (0.72, 0.92)
        tV2 = (0.92, 1.06) if n == "L" else (1.04, 1.18)
        hr = (14.0 * s, 0.0, 0.0)
        _schritt(sp, h, t1[0], t1[1], S["ball_" + h], halb, S["rot_" + h], hr, 0.06, None, (S["pole_" + h], (1.0, 0.0, 0.0)),
                 (S["welt_" + h][0], 1.0), (S["rel_" + h], REL0[h]))
        if FERSE_WEG:
            # NACHBESSERUNG: Aufstehen mit eigenem Ausweichen (ferse_dy_auf), sonst wie Hinsetzen
            _ferse_weg(sp, h, t1[0], t1[1], 0.025, SITZ_2C.get("ferse_dy_auf", SITZ_2C.get("ferse_dy", 0.03)) * s)
        else:
            _fuss_flach_bis(sp, h, t1[0] + 0.60 * (t1[1] - t1[0]), hr)
            _ausweichen(sp, h, 0.5 * (t1[0] + t1[1]), 0.03 * s)     # Neustart: Schrittmitte 3 cm aussen, sonst streift der Fuss den Unterarm (p31)
        _schritt(sp, v, tV1[0], tV1[1], S["ball_" + v], _vzw(n), S["rot_" + v], R0, 0.05, (25, 0, 5))
        _schritt(sp, h, t2[0], t2[1], halb, NB(h), hr, R0, 0.06)
        _schritt(sp, v, tV2[0], tV2[1], _vzw(n), NB(v), R0, R0, 0.05, (25, 0, 5))
    return sp


def sp_fressen():
    """Fressen am Boden, Schleife 3,20 s, erstes = letztes Bild = E: Zubeissen 0,50-0,72, Reissen 0,72-1,20 (Kopf ruckt hoch und
    zurueck, die linke Pranke drueckt), Kauen 1,20-2,70 (Kopf halb hoch, Kiefer 2,5 Hz), Kopf wieder runter 2,70-3,20."""
    E = POSE_E
    sp = {}
    ne, he = E["r_ne"], E["r_he"]
    sp["r_ne"] = [(0.0, ne), (0.50, (0, ne[1] + 2, 0)), (0.72, (0, ne[1] + 3, 0)), (0.85, (8, ne[1] - 14, 3)), (1.00, (-8, ne[1] - 18, -3)),
                  (1.20, (0, ne[1] - 22, 0)), (1.95, (3, ne[1] - 22, 1)), (2.70, (-2, ne[1] - 20, 0)), (3.20, ne)]
    sp["r_he"] = [(0.0, he), (0.50, (0, he[1] + 3, 0)), (0.72, (0, he[1] + 4, 0)), (0.85, (14, he[1] - 22, 6)), (1.00, (-12, he[1] - 30, -5)),
                  (1.20, (0, he[1] - 36, 0)), (1.60, (5, he[1] - 36, 2)), (2.00, (-5, he[1] - 35, -2)), (2.40, (4, he[1] - 34, 1)),
                  (2.70, (0, he[1] - 30, 0)), (3.20, he)]
    ch = E["r_ch"]
    sp["r_ch"] = [(0.0, ch), (0.72, (0, ch[1] + 1, 0)), (1.00, (0, ch[1] - 4, 0)), (1.20, (0, ch[1] - 5, 0)), (2.70, (0, ch[1] - 4, 0)), (3.20, ch)]
    sp["kiefer"] = [(0.0, E["kiefer"]), (0.50, (24.0,)), (0.65, (3.0,)), (0.72, (3.0,)), (1.20, (4.0,)), (1.40, (14.0,)), (1.60, (4.0,)),
                    (1.80, (14.0,)), (2.00, (4.0,)), (2.20, (14.0,)), (2.40, (4.0,)), (2.60, (12.0,)), (2.85, (6.0,)), (3.20, E["kiefer"])]
    sp["klav_L"] = [(0.0, E["klav_L"]), (0.72, (-8.0, 0.0)), (1.00, (-14.0, -3.0)), (1.30, (-10.0, -1.0)), (3.20, E["klav_L"])]
    return sp


# (Name, Spurfunktion, Dauer, Zeiten fuer die Diagnose, Anfangspose, Endpose)
KAMPF_CLIPS = (
    ("NCBear_Rear", sp_rear, T_REAR, (0.0, 0.40, 0.85, 1.45, 2.05, 2.40, 2.72), None, None),
    ("NCBear_SwipeL", sp_hieb_l, T_HIEB, (0.20, 0.44, 0.52, 0.60, 0.70, 0.80, 1.20), None, None),
    ("NCBear_SwipeR", lambda: spiegeln(sp_hieb_l()), T_HIEB, (0.44, 0.60, 0.80), None, None),
    ("NCBear_Slam", sp_slam, T_SLAM, (0.90, 1.10, 1.27, 1.30, 1.45, 1.85, 2.30), None, None),
    ("NCBear_Bite", sp_biss, T_BISS, (0.17, 0.40, 0.52, 0.66, 0.95), None, None),
    ("NCBear_Maul", sp_maul, T_MAUL, (0.30, 0.46, 0.544, 0.70, 0.85), None, None),
    ("NCBear_SitDown", sp_setzen_2c, T_SETZEN, (0.30, 0.65, 0.95, 1.30, 1.60), None, POSE_S2C),      # 2c Bau Sitzen: S_neu
    ("NCBear_Sit", sp_sitzen_2c, T_SITZEN, (0.0, 1.0, 2.0), POSE_S2C, POSE_S2C),
    ("NCBear_StandUp", sp_aufstehen_2c, T_AUFSTEHEN, (0.0, 0.25, 0.55, 0.80), POSE_S2C, None),
    ("NCBear_Eat", sp_fressen, T_FRESSEN, (0.0, 0.65, 1.0, 2.0), POSE_E, POSE_E),
)




# ==== RIG (G): Gang des Generator-Jungen (RIG_PLAN 5.3, Kevins Freigabe 11.11. "Gehen schneller"). Walk = Trab (diagonale Paare),
# Run = Galopp (Kopie RUN mit weniger Bildern je Zyklus). Das Spiel nimmt das Tempo nur aus Translation_Data (x MotionScale 1,6) und
# skaliert das Bild mit 1,5 x Groesse (Belege RIG_PLAN 5.3); ohne Gleiten muss gelten Weg je Zyklus = S/duty x M2U / K_WELT x 0,35.
# Abrollpunkt (RIG): die Generator-Pfoten sind starre Koerper, das Sprung-/Handgelenk steht mitten ueber der Sohle (SKELETT.md 8.5).
# Rollt die Pfote um Toe0 (8 cm hoch), taucht die Sohlenspitze in den Boden; deshalb rollt sie hier um die Vorderkante unten
# (Netz rig/skelett/netz_rig.npz, gemessen 11.11.: Sohle ohne Krallen steigt vorn von z 0,2 cm bei x 0,357 auf 0,6 cm bei 0,391, die
# Krallen liegen dort bei 0,8 cm; hinten Sohle bis x -0,33 (0,7 cm), Krallen -0,33..-0,29). Abrollpunkt = Zehenansatz unten.
ABROLL = {}
for _n, _s in (("L", 1), ("R", -1)):
    ABROLL["V" + _n] = Vector((0.395, J["Bip01_%s_Hand" % _n].y, 0.006))
    ABROLL["H" + _n] = Vector((-0.330, J["Bip01_%s_Foot" % _n].y, 0.007))
WEG_GROESSE = 0.35          # Bezugsgroesse des Jungen (BanditsNPCBearDefs.lua minSize = maxSize = 0,35)
# Festgelegt nach der Suche rig/clips/suche (v1-v5, Messung werkzeug/gang_pruef.py an der Haut, 11.11.): Plan-Werte S 0,64 / duty 0,38
# ueberstrecken 6 Bilder, Becken wippt 4,3 cm und der Hinterfuss faehrt durch Unterarm und Pranke derselben Seite (185 Punkte; kurzer
# Rumpf L/H 1,2). Gleiches Tempo (S/duty gleich) mit kleinerem Stuetzweg und kuerzerer Stuetzzeit (fliegender Trab): S 0,53 / duty
# 0,3148 -> 0 ueberstreckt, 0 Durchdringung, Becken 0,8 cm, Pfoten in der Stuetze 0..+0,7 cm. Vorderpfote hebt steil ab (m0 0,3, hexp 0,6).
TRAB = dict(
    name="DeerStag_Walk", T=9, N=3, duty=0.3148,
    kontakt=dict(HL=0.00, VR=0.02, HR=0.50, VL=0.52),       # Trab: diagonale Paare HL+VR, HR+VL
    S=dict(H=0.53, V=0.53), mitte=dict(H=0.0, V=0.0), hub=dict(H=0.10, V=0.12),
    ab=dict(H=22.0, V=22.0), spitze=dict(H=35.0, V=40.0), aussen=0.02, senk=0.03, streck=dict(H=0.97, V=0.985),   # spitze: die runde
    # Generator-Pfote sah mit 45/60 Grad im Schwung wie ein Haken aus (Diag-Render 11.11.); 35/40 wirkt weicher, Messung gleich (Suche v6)
    m0=dict(V=0.3, H=1.0), hexp=dict(V=0.6, H=0.85),
    roll=1.5, nick=1.5, klav=14.0, kopf=4.0,
)
# Galopp: Plan S 0,61 / duty 0,25 ueberstreckt 2 Bilder, Becken 6,5 cm, Durchdringung 147 Punkte; gleiches Tempo mit S 0,56 / duty 0,2295,
# Hinterpfote im Schwung 4 cm weiter aussen, Spur hinten +1 / vorn -0,5 cm, Abrollen 22/20 Grad -> 0 / 0, Becken 4,0 cm (Suche r_c2).
RUN_J = dict(RUN, name="DeerStag_Run", T=8, N=2, S=dict(H=0.56, V=0.56), duty=0.2295, m0=dict(V=0.3, H=1.0), hexp=dict(V=0.6, H=0.85),
             ab=dict(H=22.0, V=20.0), aussen=0.04, spur=dict(H=0.01, V=-0.005), mitte=dict(H=0.04, V=-0.02), spitze=dict(H=45.0, V=50.0))
if os.environ.get("NCB_RIG_GANG"):
    _gp = _json.load(open(os.environ["NCB_RIG_GANG"]))
    for _k, _v in _gp.get("TRAB", {}).items():
        TRAB[_k] = _v
    for _k, _v in _gp.get("RUN_J", {}).items():
        RUN_J[_k] = _v


def weg_j(G):
    """Translation_Data am Clip-Ende (E): N Zyklen, Stuetzweg S/duty (m bei Groesse 1,0) x M2U / K_WELT x WEG_GROESSE."""
    return G["N"] * G["S"]["H"] / G["duty"] * M2U / K_WELT * WEG_GROESSE


def ballen_zu_ferse_j(key, ball, pitch):
    q = ry(pitch)
    return ball + q @ (J[LEG[key]["fuss"]] - ABROLL[key]), q


def fuss_bahn_j(G, key, phi):
    """Wie fuss_bahn, aber Bahn des Abrollpunkts (Vorderkante der Sohle am Boden) statt Toe0."""
    L = LEG[key]
    art = key[0]
    u = (phi - G["kontakt"][key]) % 1.0
    duty, S, cc = G["duty"], G["S"][art], G["mitte"][art]
    b = ABROLL[key]
    x0 = b.x + cc
    spur = G.get("spur", {}).get(art, 0.0)           # RIG: Stuetz-Spur quer (+ = nach aussen)
    if u < duty:
        w = u / duty
        x = x0 + S * 0.5 - S * w
        z = b.z
        y = b.y + L["s"] * spur
        pit = G["ab"][art] * ssf(0.60, 1.0, w)
    else:
        s = (u - duty) / (1.0 - duty)
        m = -S * min((1.0 - duty) / duty, 1.0)
        # RIG: Anfangstempo des Schwungs je Beinpaar waehlbar (m0 < 1: die Pfote laeuft nach dem Abheben nicht weiter nach hinten
        # in die Bahn des anderen Beins derselben Seite), Hub-Verlauf (hexp < 0,85: frueher hoch)
        x = hermite(s, x0 - S * 0.5, x0 + S * 0.5, m * G.get("m0", {}).get(art, 1.0), m * G.get("m1", {}).get(art, 1.0))
        z = b.z + G["hub"][art] * math.sin(math.pi * s ** G.get("hexp", {}).get(art, 0.85))
        y = b.y + L["s"] * (spur + G["aussen"] * math.sin(math.pi * s))
        if s < 0.30:
            pit = G["ab"][art] + (G["spitze"][art] - G["ab"][art]) * ssf(0.0, 0.30, s)
        else:
            pit = G["spitze"][art] * (1.0 - ssf(0.30, 0.88, s)) - 7.0 * ssf(0.70, 0.90, s) * (1.0 - ssf(0.92, 1.0, s))
    return Vector((x, y, z)), pit, u


def gang_j(G, phi, stat, koerper):
    """Wie gang(): Beine nach der Bahn des Abrollpunkts, der Rumpf sinkt nur so weit, wie die stuetzenden Beine es verlangen."""
    ziele = {}
    for key in ("VL", "VR", "HL", "HR"):
        ball, pit, u = fuss_bahn_j(G, key, phi)
        ank, q = ballen_zu_ferse_j(key, ball, pit)
        ziele[key] = (ank, q, u < G["duty"] + 0.05 or u > 0.96)
    dz, dp = 0.0, 0.0
    for _ in range(6):
        pose = koerper(dz, dp)
        bed = dict(V=0.0, H=0.0)
        for key, (ank, q, st) in ziele.items():
            if not st:
                continue
            L = LEG[key]
            hip = hueftpunkt(pose, key)
            dmax = G["streck"][key[0]] * (L["a"] + L["b"])
            dxy2 = (hip.x - ank.x) ** 2 + (hip.y - ank.y) ** 2
            zreq = ank.z + math.sqrt(max(dmax * dmax - dxy2, 0.0))
            bed[key[0]] = min(bed[key[0]], zreq - hip.z)
        if bed["H"] > -2e-4 and bed["V"] > -2e-4:
            break
        dz += bed["H"]
        dp += math.degrees(math.atan2(-bed["V"], 0.37))
    stat["absenk"] = min(stat.get("absenk", 0.0), dz)
    stat["neig"] = max(stat.get("neig", 0.0), dp)
    stat.setdefault("dz", []).append(dz)
    stat.setdefault("dp", []).append(dp)
    for key, (ank, q, st) in ziele.items():
        bein(pose, key, hueftpunkt(pose, key), ank, q, stat)
    toe(pose)
    return pose


def pose_trab(f, stat):
    """Trab: diagonale Paare (HL+VR, HR+VL), 3 Zyklen je Clip. Rumpf ruhig (Rollen +-roll, Nicken +-nick doppelt je Zyklus: jedes
    diagonale Paar federt einmal), Kopf ruhig gegen die Schultern, Schulterblatt +-klav mit der Vorderpfote, Schwanz klein."""
    G = TRAB
    phi = f / G["T"]

    def koerper(dz, dp):
        pel = J["Bip01_Pelvis"] + vec(0.004 * c(2 * phi), -0.004 * c(phi - 0.25), -G["senk"] + 0.004 * c(2 * (phi - 0.15)) + dz)
        q_pel = euler(yaw=-1.5 * c(phi), pitch=G["nick"] * c(2 * (phi - 0.10)), roll=G["roll"] * c(phi - 0.25))
        q_sp = ry(dp * 0.6) @ euler(yaw=-0.5 * c(phi - 0.05), pitch=-0.4 * G["nick"] * c(2 * (phi - 0.14)), roll=0.6 * G["roll"] * c(phi - 0.30))
        q_ch = ry(dp) @ euler(yaw=1.5 * c(phi - 0.10), pitch=-G["nick"] * c(2 * (phi - 0.20)), roll=-G["roll"] * c(phi - 0.30))
        # Kopf ruhig: Hals und Kopf (Weltdrehung) pendeln nur wenig, gegen die Schultern
        q_ne = euler(yaw=-0.8 * c(phi - 0.10), pitch=G["kopf"] + 0.6 * c(2 * (phi - 0.25)), roll=0.6 * c(phi - 0.30))
        q_he = euler(yaw=-0.8 * c(phi - 0.10), pitch=G["kopf"] + 0.5 * c(2 * (phi - 0.30)), roll=0.4 * c(phi - 0.30))
        q_ta = euler(yaw=4.0 * c(phi - 0.30), pitch=-2.0 * c(2 * phi))
        pose = {}
        rumpf(pose, pel, q_pel, q_sp, q_ch, q_ne, q_he, q_ta)
        for n, ph in (("L", G["kontakt"]["VL"]), ("R", G["kontakt"]["VR"])):
            schluesselbein(pose, n, -G["klav"] * math.cos(2.0 * math.pi * (phi - ph)))
        return pose

    return gang_j(G, phi, stat, koerper)


def pose_galopp(f, stat):
    """Galopp: wie pose_run (Erwachsener), Parameter RUN_J, 2 Zyklen je Clip."""
    G = RUN_J
    phi = f / G["T"]
    beug = c(phi - 0.97)
    kipp = c(phi - 0.18)

    def koerper(dz, dp):
        pel = J["Bip01_Pelvis"] + vec(0.045 * beug, 0.008 * c(phi - 0.2), -G["senk"] + 0.020 * c(phi - 0.86) + dz)
        q_pel = euler(yaw=2.0 * c(phi - 0.1), pitch=-8.0 * beug - 3.0 * kipp, roll=2.5 * c(phi - 0.05))
        q_sp = ry(dp * 0.6) @ euler(yaw=0.5 * c(phi - 0.15), pitch=-2.0 * beug - 3.0 * kipp, roll=1.2 * c(phi - 0.1))
        q_ch = ry(dp) @ euler(yaw=-2.0 * c(phi - 0.45), pitch=5.0 * beug - 3.0 * kipp, roll=-2.5 * c(phi - 0.50))
        q_ne = euler(yaw=1.0 * c(phi - 0.5), pitch=6.0 + 2.0 * beug + 3.0 * kipp, roll=-1.0 * c(phi - 0.5))
        q_he = euler(yaw=1.5 * c(phi - 0.55), pitch=5.0 + 4.0 * kipp, roll=0.0)
        q_ta = euler(yaw=5.0 * c(phi - 0.3), pitch=-10.0 * c(phi - 0.1))
        pose = {}
        rumpf(pose, pel, q_pel, q_sp, q_ch, q_ne, q_he, q_ta)
        for n, ph in (("L", G["kontakt"]["VL"]), ("R", G["kontakt"]["VR"])):
            schluesselbein(pose, n, -14.0 * math.cos(2.0 * math.pi * (phi - ph)))
        return pose

    return gang_j(G, phi, stat, koerper)


# ==== RIG (H): die fuenf neuen Clips als Posen schreiben (kein Netz, kein Rig, kein Export), dann Ende
if os.environ.get("NCB_RIG_AUS"):
    _aus = {"namen": np.array(ORDER), "ruhe": np.array([tuple(J[_b]) for _b in ORDER])}
    _nur = os.environ.get("NCB_RIG_NUR", "")
    for _nm, _fn, _n, _G in (("DeerStag_Walk", pose_trab, 27, TRAB), ("DeerStag_Run", pose_galopp, 16, RUN_J)):
        if _nur and _nur != "gang":
            continue
        assert _n == _G["T"] * _G["N"], (_nm, _n, _G["T"], _G["N"])
        _st = {}
        _Q = np.zeros((_n + 1, len(ORDER), 4))
        _P = np.zeros((_n + 1, len(ORDER), 3))
        _U = np.zeros((_n + 1, 4))
        for _i in range(_n + 1):
            _pose = _fn(_i, _st)
            for _k, _b in enumerate(ORDER):
                _q, _p = _pose[_b]
                _Q[_i, _k] = (_q.w, _q.x, _q.y, _q.z)
                _P[_i, _k] = tuple(_p)
            _U[_i] = [(_i / _G["T"] - _G["kontakt"][_k]) % 1.0 for _k in ("VL", "VR", "HL", "HR")]
        _aus[_nm + "_Q"], _aus[_nm + "_P"], _aus[_nm + "_u"] = _Q, _P, _U
        _aus[_nm + "_weg"] = np.array(weg_j(_G))
        _aus[_nm + "_duty"] = np.array(_G["duty"])
        _ip = ORDER.index("Bip01_Pelvis")
        log("RIG_GANG", _nm, "Bilder", _n + 1, "Zyklen", _G["N"], "S", _G["S"], "duty", _G["duty"], "Weg %.5f E" % weg_j(_G),
            "Tempo %.3f Kacheln/s" % (weg_j(_G) * 1.6 / (_n / FPS)), "| ueberstreckt", _st.get("ueber", 0), "max %.3f" % _st.get("max", 0),
            "| Rumpf gesenkt min %.3f m, Brust geneigt max %.2f Grad" % (_st.get("absenk", 0), _st.get("neig", 0)),
            "| Becken z Spitze-Spitze %.2f cm" % (100 * (_P[:, _ip, 2].max() - _P[:, _ip, 2].min())), "| wo", _st.get("wo"))
    for _nm, _fn, _T, _zeiten, _anf, _end in KAMPF_CLIPS:
        if _nm not in SITZ_CLIPS or (_nur and _nur != "sitz"):
            continue
        GR_AKTIV["rumpf"] = GRENZEN_RUMPF_SITZ
        _sp = spuren_bauen(_fn(), _T, _anf, _end)
        _n = int(round(_T * FPS))
        _st = {}
        _Q = np.zeros((_n + 1, len(ORDER), 4))
        _P = np.zeros((_n + 1, len(ORDER), 3))
        for _i in range(_n + 1):
            _pose = kampf_pose(_sp, _i / FPS, _st)
            for _k, _b in enumerate(ORDER):
                _q, _p = _pose[_b]
                _Q[_i, _k] = (_q.w, _q.x, _q.y, _q.z)
                _P[_i, _k] = tuple(_p)
        _aus[_nm + "_Q"] = _Q
        _aus[_nm + "_P"] = _P
        _jkl = {k: {w: len(v) for w, v in _st.get(k, {}).get("klemm", {}).items()} for k in LEG}
        _jkr = {w: len(v) for w, v in _st.get("rumpf", {}).get("klemm", {}).items()}
        _jue = {k: (_st.get(k, {}).get("ueber"), round(_st.get(k, {}).get("max", 0.0), 4)) for k in LEG}
        log("RIG_SITZ", _nm, "Bilder", _n + 1, "| geklemmt Beine", {k: v for k, v in _jkl.items() if v}, "| geklemmt Rumpf", _jkr,
            "| Bein-Laenge/Reichweite (ueber, max)", _jue)
    GR_AKTIV["rumpf"] = GRENZEN_RUMPF
    np.savez(os.environ["NCB_RIG_AUS"], **_aus)
    log("RIG_AUS", os.environ["NCB_RIG_AUS"], "SITZ", SITZ_2C, "V_ZW", V_ZW, "TRAB", TRAB, "RUN_J", {k: v for k, v in RUN_J.items() if k != "kontakt"})
    sys.exit(0)
