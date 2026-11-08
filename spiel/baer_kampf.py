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
QUELLE = r"C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/"
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


# ------------------------------------------------------------------ Kampfclips (kampf_spez.md 5.5)
# Jede Spur hat eigene Schluessel (Zeit in s, Wert); dazwischen monotone kubische Kurve (Fritsch-Carlson): kein Ueberschwingen,
# Tempo 0 an Umkehrpunkten und an Clipanfang und -ende. Anfang und Ende sind die Grundhaltung des Stehens (Mittel von
# DeerStag_Idle01), damit die Blende aus und in idle1 nicht springt. Gliedmassen: Ballen der Pfote in Welt, Weltdrehung der
# Pfote, Pol des Ellbogens bzw. Knies. ("S", d): Schulter bzw. Huefte zur Schluesselzeit plus d (Welt, Meter).
# Drehungen (Gieren, Nicken, Rollen) in Grad wie euler(): Nicken + = Nase runter, Gieren + = Nase links, Rollen + = linke Seite hoch.
T_REAR, T_HIEB, T_SLAM, T_MAUL = 3.0, 1.1, 2.2, 1.6   # 90, 33, 66, 48 Bilder
R0 = (0.0, 0.0, 0.0)


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


def grund():
    N = dict(pel=(0.0, 0.0, -0.004), r_pel=R0, r_sp=R0, r_ch=R0, r_ne=(0.0, 4.0, 0.0), r_he=(0.0, 4.0, 0.0), r_ta=R0,
             kiefer=(0.0,), klav_L=(0.0, 0.0), klav_R=(0.0, 0.0))
    for key, L in LEG.items():
        N["ball_" + key] = tuple(L["ball"])
        N["rot_" + key] = R0
        N["pole_" + key] = tuple(L["pole"])
    return N


def NB(key, dx=0.0, dy=0.0, dz=0.0):
    b = LEG[key]["ball"]
    return (b.x + dx, b.y + dy, b.z + dz)


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
    return v


def spiegeln(sp):
    """Hieb rechts aus Hieb links: Seite, Gieren und Rollen spiegeln, L und R tauschen. Das Skelett ist symmetrisch gebaut."""
    return {_tausche(k): [(t, _spiegel_wert(k, v)) for t, v in ks] for k, ks in sp.items()}


def wert(sp, k, t):
    ts, ys = sp[k]
    return pchip(ts, ys, t)


def rumpf_bei(sp, t):
    pel = J["Bip01_Pelvis"] + Vector(wert(sp, "pel", t))
    q = [euler(*[float(x) for x in wert(sp, k, t)]) for k in ("r_pel", "r_sp", "r_ch", "r_ne", "r_he", "r_ta")]
    pose = {}
    rumpf(pose, pel, *q, kiefer=float(wert(sp, "kiefer", t)[0]))
    for n in "LR":
        kp, kr = (float(x) for x in wert(sp, "klav_" + n, t))
        kette(pose, "Bip01_%s_Clavicle" % n, pose["Bip01_Spine1"][0] @ euler(0.0, kp, kr))
    return pose


def spuren_bauen(roh, T):
    """Fuellt fehlende Spuren mit der Grundhaltung, setzt Anfang und Ende, loest Schulterbezuege auf."""
    N = grund()
    unbekannt = set(roh) - set(N)
    assert not unbekannt, unbekannt
    tab = {}
    for k, v0 in N.items():
        ks = [(float(t), v) for t, v in roh.get(k, [])]
        assert all(ks[i][0] < ks[i + 1][0] for i in range(len(ks) - 1)), k
        if not ks or ks[0][0] > 1e-9:
            ks.insert(0, (0.0, v0))
        if ks[-1][0] < T - 1e-9:
            ks.append((T, v0))
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


def kampf_pose(sp, t, stat):
    pose = rumpf_bei(sp, t)
    for key in ("VL", "VR", "HL", "HR"):
        L = LEG[key]
        ball = Vector(wert(sp, "ball_" + key, t))
        q = euler(*[float(x) for x in wert(sp, "rot_" + key, t)])
        pose["_pole_" + key] = Vector(wert(sp, "pole_" + key, t)).normalized()
        ank = ball + q @ (J[L["fuss"]] - L["ball"])
        st = stat.setdefault(key, {})
        u0 = st.get("ueber", 0)
        bein(pose, key, hueftpunkt(pose, key), ank, q, st)
        if st.get("ueber", 0) > u0:
            st.setdefault("zeiten", []).append(round(t, 3))
    toe(pose)
    return pose


SCHNAUZE = Vector(BONES["Bip01_Head"][1])


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


def sp_rear():
    """Aufrichten auf die Hinterbeine und Bruellen. 0-0,8 s hoch, 0,8-2,2 s stehen (Bruellen ab 0,81 s), 2,2-3,0 s zurueck."""
    sp = {}
    sp["pel"] = [(0.18, (-0.03, 0, -0.035)), (0.40, (-0.07, 0, -0.045)), (0.80, (-0.09, 0, -0.035)), (1.00, (-0.09, 0, -0.025)),
                 (2.00, (-0.09, 0, -0.03)), (2.25, (-0.08, 0, -0.035)), (2.55, (-0.03, 0, -0.035)), (2.78, (0.01, 0, -0.03))]
    sp["r_pel"] = [(0.18, (0, 3, 0)), (0.40, (0, -16, 0)), (0.80, (0, -48, 0)), (1.00, (0, -52, 0)), (1.60, (1, -50, -1.5)),
                   (2.00, (0, -48, 1)), (2.25, (0, -40, 0)), (2.55, (0, -14, 0)), (2.78, (0, 3, 0))]
    sp["r_sp"] = [(0.18, (0, 4, 0)), (0.40, (0, -24, 0)), (0.80, (0, -64, 0)), (1.00, (0, -70, 0)), (1.60, (2, -68, -2)),
                  (2.00, (0, -66, 1.5)), (2.25, (0, -56, 0)), (2.55, (0, -20, 0)), (2.78, (0, 4, 0))]
    sp["r_ch"] = [(0.18, (0, 6, 0)), (0.40, (0, -30, 0)), (0.80, (0, -74, 0)), (1.00, (0, -80, 0)), (1.60, (3, -78, -3)),
                  (2.00, (0, -76, 2)), (2.25, (0, -64, 0)), (2.55, (0, -24, 0)), (2.78, (0, 7, 0))]
    sp["r_ne"] = [(0.18, (0, 12, 0)), (0.40, (0, -10, 0)), (0.80, (0, -46, 0)), (0.95, (0, -58, 0)), (1.30, (-4, -60, 2)),
                  (1.60, (5, -58, -2)), (1.90, (-3, -56, 1)), (2.10, (0, -44, 0)), (2.40, (0, -6, 0)), (2.78, (0, 10, 0))]
    sp["r_he"] = [(0.18, (0, 12, 0)), (0.40, (0, -4, 0)), (0.80, (0, -30, 0)), (0.95, (0, -44, 0)), (1.15, (-6, -46, 4)),
                  (1.40, (6, -44, -4)), (1.65, (-5, -45, 3)), (1.90, (3, -40, -2)), (2.10, (0, -28, 0)), (2.40, (0, 0, 0)),
                  (2.78, (0, 8, 0))]
    sp["r_ta"] = [(0.40, (0, -12, 0)), (0.80, (0, -40, 0)), (2.10, (0, -40, 0)), (2.55, (0, -10, 0))]
    sp["kiefer"] = [(0.60, (0.0,)), (0.80, (14.0,)), (0.95, (38.0,)), (1.30, (35.0,)), (1.60, (38.0,)), (1.85, (34.0,)),
                    (2.00, (30.0,)), (2.15, (8.0,)), (2.30, (0.0,))]
    for n, s in (("L", 1), ("R", -1)):
        sp["klav_" + n] = [(0.40, (-8.0, 0.0)), (0.90, (-14.0, 6.0 * s)), (2.10, (-14.0, 6.0 * s)), (2.60, (-6.0, 0.0))]
        k = "V" + n
        sp["ball_" + k] = [(0.22, NB(k)), (0.40, NB(k, -0.08, 0, 0.17)), (0.80, ("S", (0.26, -0.05 * s, -0.32))),
                           (1.60, ("S", (0.28, -0.06 * s, -0.30))), (2.10, ("S", (0.30, -0.04 * s, -0.30))),
                           (2.55, NB(k, 0.08, 0, 0.15)), (2.75, NB(k))]
        sp["rot_" + k] = [(0.22, R0), (0.40, (0, 30, 0)), (0.80, (-8 * s, 55, 0)), (1.60, (-10 * s, 57, 0)), (2.10, (-6 * s, 50, 0)),
                          (2.55, (0, 20, 0)), (2.75, R0)]
        sp["pole_" + k] = [(0.22, (-1.0, 0.0, 0.0)), (0.80, (-0.3, 0.25 * s, -1.0)), (2.10, (-0.3, 0.25 * s, -1.0)), (2.60, (-1.0, 0.0, 0.0))]
    return sp


def sp_hieb_l():
    """Prankenhieb links: Gewicht auf rechts und hinten, linke Pranke vorn-aussen hoch, schneller Schlag schraeg nach
    innen-unten vor dem Gesicht vorbei (Treffer 0,46 s), der Kopf weicht nach rechts-unten aus, die Pranke zieht bis zum
    Boden durch, zurueck. Rechts vorn und beide hinten bleiben stehen."""
    sp = {}
    sp["pel"] = [(0.12, (-0.02, -0.025, -0.01)), (0.30, (-0.04, -0.035, -0.015)), (0.46, (0.05, -0.01, -0.035)),
                 (0.62, (0.05, 0.005, -0.035)), (0.85, (0.01, 0.0, -0.015))]
    sp["r_pel"] = [(0.30, (3, -2, 2)), (0.46, (-4, 2, -1)), (0.62, (-6, 2, -2)), (0.85, (-2, 1, 0))]
    sp["r_sp"] = [(0.30, (5, -3, 5)), (0.46, (-8, 3, 0)), (0.62, (-12, 4, -2)), (0.85, (-3, 1, 0))]
    sp["r_ch"] = [(0.12, (3, -1, 6)), (0.30, (8, -5, 14)), (0.46, (-14, 6, 3)), (0.62, (-18, 8, -2)), (0.85, (-5, 2, 0))]
    sp["r_ne"] = [(0.30, (2, 2, 4)), (0.46, (-14, 12, 0)), (0.62, (-14, 12, -2)), (0.85, (-3, 6, 0))]
    sp["r_he"] = [(0.30, (-6, 4, 6)), (0.46, (-18, 16, -6)), (0.62, (-12, 14, -3)), (0.85, (-3, 6, 0))]
    sp["kiefer"] = [(0.15, (6.0,)), (0.32, (16.0,)), (0.46, (22.0,)), (0.62, (18.0,)), (0.85, (4.0,)), (1.0, (0.0,))]
    sp["klav_L"] = [(0.30, (-6.0, 14.0)), (0.46, (-16.0, 6.0)), (0.62, (-12.0, 0.0)), (0.85, (-2.0, 0.0))]
    sp["klav_R"] = [(0.30, (0.0, -4.0)), (0.46, (4.0, -2.0)), (0.85, (0.0, 0.0))]
    sp["ball_VL"] = [(0.06, NB("VL")), (0.16, NB("VL", 0.02, 0.05, 0.14)), (0.30, ("S", (0.26, 0.30, 0.14))),
                     (0.40, ("S", (0.52, 0.14, 0.04))), (0.46, (1.00, 0.05, 0.55)), (0.62, (0.78, -0.20, 0.10)),
                     (0.80, (0.60, 0.06, 0.15)), (0.95, NB("VL"))]
    sp["rot_VL"] = [(0.06, R0), (0.16, (8, 25, 10)), (0.30, (25, -20, 45)), (0.40, (5, 0, 60)), (0.46, (-40, 30, 70)),
                    (0.62, (-55, 65, 40)), (0.80, (-10, 25, 5)), (0.95, R0)]
    sp["pole_VL"] = [(0.06, (-1.0, 0.0, 0.0)), (0.30, (-0.6, 0.3, -0.7)), (0.46, (-0.8, 0.5, -0.2)), (0.62, (-1.0, 0.3, -0.3)),
                     (0.95, (-1.0, 0.0, 0.0))]
    return sp


def sp_slam():
    """Doppelschlag: halb aufrichten (0-0,9 s), beide Pranken mit Wucht nach vorn-unten (Aufschlag 1,22 s, Treffer 1,25 s),
    Rumpf faellt nach vorn, federt, dann tritt erst links, dann rechts zurueck an den alten Platz."""
    sp = {}
    sp["pel"] = [(0.15, (-0.03, 0, -0.035)), (0.40, (-0.07, 0, -0.04)), (0.85, (-0.09, 0, -0.04)), (1.10, (0.00, 0, -0.03)),
                 (1.25, (0.07, 0, -0.05)), (1.38, (0.07, 0, -0.07)), (1.62, (0.06, 0, -0.05)), (1.82, (0.04, 0, -0.035)),
                 (2.05, (0.0, 0, -0.01))]
    sp["r_pel"] = [(0.15, (0, 3, 0)), (0.40, (0, -10, 0)), (0.85, (0, -24, 0)), (1.10, (0, -4, 0)), (1.25, (0, 4, 0)),
                   (1.38, (0, 6, 0)), (1.70, (0, 4, 0)), (1.95, (0, 1, 0))]
    sp["r_sp"] = [(0.15, (0, 4, 0)), (0.40, (0, -16, 0)), (0.85, (0, -34, 0)), (1.10, (0, -6, 0)), (1.25, (0, 8, 0)),
                  (1.38, (0, 10, 0)), (1.70, (0, 7, 0)), (1.95, (0, 2, 0))]
    sp["r_ch"] = [(0.15, (0, 6, 0)), (0.40, (0, -20, 0)), (0.85, (0, -42, 0)), (1.10, (0, -8, 0)), (1.25, (0, 13, 0)),
                  (1.38, (0, 17, 0)), (1.70, (0, 11, 0)), (1.95, (0, 3, 0))]
    sp["r_ne"] = [(0.15, (0, 12, 0)), (0.40, (0, -4, 0)), (0.85, (0, -14, 0)), (1.10, (0, 10, 0)), (1.25, (0, 24, 0)),
                  (1.38, (0, 26, 0)), (1.60, (0, 10, 0))]
    sp["r_he"] = [(0.15, (0, 14, 0)), (0.40, (0, 4, 0)), (0.85, (0, 0, 0)), (1.10, (0, 14, 0)), (1.25, (0, 28, 0)),
                  (1.38, (0, 30, 0)), (1.60, (0, 10, 0))]
    sp["r_ta"] = [(0.85, (0, -18, 0)), (1.25, (0, 4, 0))]
    sp["kiefer"] = [(0.10, (4.0,)), (0.30, (18.0,)), (0.85, (24.0,)), (1.10, (26.0,)), (1.25, (14.0,)), (1.45, (6.0,)), (1.70, (0.0,))]
    for n, s in (("L", 1), ("R", -1)):
        sp["klav_" + n] = [(0.85, (-10.0, 6.0 * s)), (1.25, (-12.0, 0.0)), (1.60, (0.0, 0.0))]
        k = "V" + n
        lauf = (1.42, 1.52, 1.62) if n == "L" else (1.62, 1.72, 1.82)
        sp["ball_" + k] = [(0.20, NB(k)), (0.40, NB(k, -0.04, 0, 0.22)), (0.85, ("S", (0.30, 0.0, 0.10))),
                           (1.05, NB(k, 0.22, -0.01 * s, 0.40)), (1.20, NB(k, 0.26, -0.01 * s, 0.015)),
                           (1.22, NB(k, 0.26, -0.01 * s, 0.0)), (lauf[0], NB(k, 0.26, -0.01 * s, 0.0)),
                           (lauf[1], NB(k, 0.13, 0.005 * s, 0.07)), (lauf[2], NB(k))]
        sp["rot_" + k] = [(0.20, R0), (0.40, (0, 40, 0)), (0.85, (0, 10, 0)), (1.05, (0, 10, 0)), (1.20, (0, 2, 0)), (1.22, R0),
                          (lauf[0], R0), (lauf[1], (0, 15, 0)), (lauf[2], R0)]
        sp["pole_" + k] = [(0.20, (-1.0, 0.0, 0.0)), (0.85, (-0.5, 0.2 * s, -1.0)), (1.22, (-1.0, 0.0, 0.0))]
    return sp


def sp_maul():
    """Biss am Boden: Kopf tief und vor, Maul auf, Stoss nach unten-vorn, Maul zu beim Treffer (0,54 s), zweimal
    Schuetteln (zerren), hoch. Die Schnauze bleibt ueber dem Boden; die Vorderpfoten stehen."""
    sp = {}
    sp["pel"] = [(0.16, (0.01, 0, -0.01)), (0.32, (0.07, 0, -0.03)), (0.48, (0.11, 0, -0.045)), (0.56, (0.115, 0, -0.05)),
                 (0.70, (0.08, 0.01, -0.045)), (0.85, (0.07, -0.01, -0.045)), (1.00, (0.07, 0.01, -0.045)), (1.12, (0.06, 0, -0.04)),
                 (1.30, (0.02, 0, -0.02))]
    sp["r_pel"] = [(0.32, (0, 3, 0)), (0.48, (0, 5, 0)), (1.12, (0, 5, 0)), (1.30, (0, 2, 0))]
    sp["r_sp"] = [(0.32, (0, 6, 0)), (0.48, (0, 8, 0)), (0.70, (-3, 8, 2)), (0.85, (3, 8, -2)), (1.00, (-3, 8, 2)),
                  (1.12, (2, 8, -1)), (1.30, (0, 4, 0))]
    sp["r_ch"] = [(0.16, (0, 3, 0)), (0.32, (0, 10, 0)), (0.48, (0, 14, 0)), (0.70, (-5, 14, 4)), (0.85, (5, 14, -4)),
                  (1.00, (-5, 14, 4)), (1.12, (3, 14, -2)), (1.30, (0, 6, 0))]
    sp["r_ne"] = [(0.16, (0, 8, 0)), (0.32, (0, 20, 0)), (0.48, (0, 26, 0)), (0.56, (0, 28, 0)), (0.70, (12, 27, 8)),
                  (0.85, (-12, 27, -8)), (1.00, (11, 27, 7)), (1.12, (-8, 26, -5)), (1.30, (0, 16, 0))]
    sp["r_he"] = [(0.16, (0, 12, 0)), (0.32, (0, 30, 0)), (0.48, (0, 42, 0)), (0.56, (0, 45, 0)), (0.70, (20, 44, 14)),
                  (0.85, (-20, 44, -14)), (1.00, (18, 44, 12)), (1.12, (-14, 42, -9)), (1.30, (0, 20, 0))]
    sp["kiefer"] = [(0.10, (4.0,)), (0.30, (28.0,)), (0.46, (34.0,)), (0.52, (10.0,)), (0.56, (3.0,)), (1.12, (3.0,)), (1.30, (0.0,))]
    sp["klav_L"] = [(0.48, (-12.0, 0.0)), (1.12, (-12.0, 0.0))]
    sp["klav_R"] = [(0.48, (-12.0, 0.0)), (1.12, (-12.0, 0.0))]
    return sp


KAMPF_CLIPS = (
    ("NCBear_Rear", sp_rear, T_REAR, (0.0, 0.40, 0.80, 1.00, 1.60, 2.20, 2.75)),
    ("NCBear_SwipeL", sp_hieb_l, T_HIEB, (0.0, 0.30, 0.40, 0.46, 0.62, 0.95)),
    ("NCBear_SwipeR", lambda: spiegeln(sp_hieb_l()), T_HIEB, (0.30, 0.46, 0.62)),
    ("NCBear_Slam", sp_slam, T_SLAM, (0.85, 1.05, 1.22, 1.254, 1.38, 1.80, 2.12)),
    ("NCBear_Maul", sp_maul, T_MAUL, (0.30, 0.46, 0.544, 0.70, 0.85)),
)


# ------------------------------------------------------------------ Netz
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = FPS
scene.render.fps_base = 1.0
bpy.ops.import_scene.fbx(filepath=QUELLE + "models_X/WorldItems/NCBear.fbx", use_custom_normals=False, use_image_search=False)
mo = [o for o in bpy.context.selected_objects if o.type == "MESH"][0]
for o in list(bpy.data.objects):
    if o is not mo:
        bpy.data.objects.remove(o, do_unlink=True)
mo.name = "NCBear"
me = mo.data
me.name = "NCBear"
n_v = len(me.vertices)
Vm = np.empty(n_v * 3, dtype=np.float64)
me.vertices.foreach_get("co", Vm)
Vm = Vm.reshape(n_v, 3)     # Meter, Tier-Rahmen
me.calc_loop_triangles()
n_t = len(me.loop_triangles)
Tri = np.empty(n_t * 3, dtype=np.int64)
me.loop_triangles.foreach_get("vertices", Tri)
Tri = Tri.reshape(n_t, 3)
Vb = np.stack((Vm[:, 1], -Vm[:, 0], Vm[:, 2]), 1) * M2U
me.vertices.foreach_set("co", Vb.ravel())
me.update()
me.shade_smooth()
me.materials.clear()
mat = bpy.data.materials.new("NCBear")
me.materials.append(mat)
log("Netz", n_v, "Punkte", n_t, "Dreiecke", "Ausmass", Vb.min(0).round(3), Vb.max(0).round(3))

# Schalen: Hauptnetz gegen Krallen
_p = np.arange(n_v)


def _w(i):
    while _p[i] != i:
        _p[i] = _p[_p[i]]
        i = _p[i]
    return i


for _t in Tri:
    _a = _w(_t[0])
    _p[_w(_t[1])] = _a
    _p[_w(_t[2])] = _a
_r = np.array([_w(i) for i in range(n_v)])
_u, _cnt = np.unique(_r, return_counts=True)
KRALLE = _r != _u[_cnt.argmax()]
log("Krallen-Schalen", len(_u) - 1, "Punkte", int(KRALLE.sum()))
KANTEN = np.unique(np.sort(np.concatenate((Tri[:, [0, 1]], Tri[:, [1, 2]], Tri[:, [2, 0]]), 0), axis=1), axis=0)


# ------------------------------------------------------------------ Gewichte
def glaette(W, runden=2, lam=0.5):
    """W: Punkte x Knochen. Mittelung ueber die Netzkanten; ueber die Beinzwischenraeume geht keine Kante."""
    W = W.copy()
    cnt = np.bincount(KANTEN[:, 0], minlength=n_v) + np.bincount(KANTEN[:, 1], minlength=n_v)
    for _ in range(runden):
        for k in range(W.shape[1]):
            s = np.bincount(KANTEN[:, 0], weights=W[KANTEN[:, 1], k], minlength=n_v) + np.bincount(KANTEN[:, 1], weights=W[KANTEN[:, 0], k], minlength=n_v)
            W[:, k] += (s / np.maximum(cnt, 1) - W[:, k]) * lam
    return W


x, y, z = Vm[:, 0], Vm[:, 1], Vm[:, 2]
Y = np.abs(y)


def achse_x(punkte, zz):
    """x der Beinachse auf Hoehe zz (punkte von oben nach unten)."""
    zs = np.array([p[2] for p in punkte])[::-1]
    xs = np.array([p[0] for p in punkte])[::-1]
    return np.interp(zz, zs, xs)


def bein_anteil():
    """Wie sehr gehoert der Punkt zum Bein statt zum Rumpf (0..1), je vorn und hinten.
    Im Rumpf zaehlt der Abstand zur Beinachse (vorn/hinten UND seitlich), damit Bauch und Brust zwischen den Beinen Rumpf bleiben.
    Unter z = 0,30 liegt zwischen den Beinen kein Punkt (Querschnitte), dort gehoert alles zum Bein."""
    ax_v = achse_x((SCHULTER, ELLE, HAND), z)
    ax_h = achse_x((HUEFTE, KNIE, FERSE), z)
    # Abstand zur Beinachse, zur Bauchseite hin (innen, zwischen den Beinen) strenger als nach aussen
    dxv = x - ax_v
    dxv = dxv * np.where(dxv < 0, 1.5, 1.0)
    dyv = Y - 0.235
    dyv = dyv * np.where(dyv < 0, 1.5, 0.75)
    dxh = x - ax_h
    dxh = dxh * np.where(dxh > 0, 1.5, 0.9)
    dyh = Y - 0.25
    dyh = dyh * np.where(dyh < 0, 1.5, 0.75)
    r_v = np.sqrt(dxv ** 2 + dyv ** 2)
    r_h = np.sqrt(dxh ** 2 + dyh ** 2)
    # Weicher Uebergang am Bauchrand: weiche Vereinigung statt Maximum, sonst liegt dort ein Ring mit starker Scherung
    unten = (1.0 - sst(0.17, 0.41, z)) * sst(0.03, 0.08, Y)
    v = (1.0 - sst(0.40, 0.78, z)) * (1.0 - sst(0.12, 0.25, r_v))
    h = (1.0 - sst(0.44, 0.84, z)) * (1.0 - sst(0.13, 0.27, r_h))
    uv = unten * sst(0.02, 0.08, x)
    uh = unten * (1.0 - sst(-0.14, -0.08, x))
    v = 1.0 - (1.0 - v) * (1.0 - uv)
    h = 1.0 - (1.0 - h) * (1.0 - uh)
    v = np.where(z < 0.17, np.maximum(v, sst(0.02, 0.08, x)), v)
    h = np.where(z < 0.17, np.maximum(h, 1.0 - sst(-0.14, -0.08, x)), h)
    return v, h


L_V, L_H = bein_anteil()
L_ALL = L_V + L_H


def rumpf_anteile():
    """Anteile der Rumpfknochen entlang x, Summe 1."""
    p_sp = sst(-0.20, -0.02, x)
    p_ch = sst(0.05, 0.22, x)
    p_ne = sst(0.40, 0.58, x)
    p_he = sst(0.62, 0.76, x)
    a = dict(
        Pelvis=1.0 - p_sp,
        Spine=p_sp * (1.0 - p_ch),
        Spine1=p_ch * (1.0 - p_ne),
        Neck=p_ne * (1.0 - p_he),
        Head=p_he,
    )
    t = sst(-0.69, -0.76, x) * (1.0 - sst(0.05, 0.13, Y)) * (1.0 - sst(0.72, 0.80, z)) * sst(0.56, 0.62, z)
    a["Tail"] = t
    a["Pelvis"] = a["Pelvis"] * (1.0 - t)
    return a


def setze_gewichte(ob, W, namen, unten_rein):
    """Glaettet, haelt den Unterlauf der Beine frei vom Rumpf, schneidet auf 4 Einfluesse, normiert, schreibt Vertexgruppen."""
    W = glaette(W, 2, 0.5)
    rumpf_idx = [i for i, n in enumerate(namen) if n in unten_rein]
    # Unterlauf der Beine rein: unter z = 0,17 kein Rumpfanteil (dort liegt zwischen den Beinen nichts), darueber weich
    W[:, rumpf_idx] *= sst(0.15, 0.24, z)[:, None]
    W[W < 1e-3] = 0.0
    s = np.argsort(-W, axis=1)
    keep = np.zeros_like(W, dtype=bool)
    np.put_along_axis(keep, s[:, :4], True, axis=1)
    W[~keep] = 0.0
    su = W.sum(1, keepdims=True)
    assert (su > 0).all()
    W /= su
    for k, nm in enumerate(namen):
        vg = ob.vertex_groups.get(nm) or ob.vertex_groups.new(name=nm)
        idx = np.nonzero(W[:, k] > 0)[0]
        for i in idx:
            vg.add([int(i)], float(W[i, k]), "REPLACE")
    log("Gewichte", ob.name, "Knochen mit Gewicht", int((W.sum(0) > 0).sum()), "Einfluesse je Punkt max", int((W > 0).sum(1).max()), "Summe min/max %.4f %.4f" % (W.sum(1).min(), W.sum(1).max()))
    return W


def gewichte_eigen():
    a = rumpf_anteile()
    namen = []
    W = []

    def dazu(n, w):
        namen.append(n)
        W.append(w)

    for k in ("Pelvis", "Spine", "Spine1", "Neck", "Head", "Tail"):
        dazu("Bip01_" + k, a[k] * (1.0 - L_ALL))
    w_ob_v = sst(0.32, 0.50, z)
    w_ob_h = sst(0.33, 0.50, z)
    w_fu = 1.0 - sst(0.055, 0.175, z)
    for n, ss in (("L", y > 0), ("R", y <= 0)):
        ss = ss.astype(float)
        dazu("Bip01_%s_UpperArm" % n, L_V * ss * w_ob_v)
        dazu("Bip01_%s_Forearm" % n, L_V * ss * (1.0 - w_ob_v) * (1.0 - w_fu))
        dazu("Bip01_%s_Hand" % n, L_V * ss * (1.0 - w_ob_v) * w_fu)
        dazu("Bip01_%s_Thigh" % n, L_H * ss * w_ob_h)
        dazu("Bip01_%s_Calf" % n, L_H * ss * (1.0 - w_ob_h) * (1.0 - w_fu))
        dazu("Bip01_%s_Foot" % n, L_H * ss * (1.0 - w_ob_h) * w_fu)
    W = np.stack(W, 1)
    # Krallen starr an der Pfote
    for n, ss in (("L", y > 0), ("R", y <= 0)):
        for nm, cond in (("Hand", x > 0), ("Foot", x <= 0)):
            k = namen.index("Bip01_%s_%s" % (n, nm))
            m = KRALLE & ss & cond
            W[m, :] = 0.0
            W[m, k] = 1.0
    return W, namen


WE, NAMEN_E = gewichte_eigen()
WE2 = setze_gewichte(mo, WE, NAMEN_E, {"Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Head", "Bip01_Tail"})
# Krallen nach dem Glaetten nachpruefen: ihre Schalen haben nur eigene Kanten, bleiben also rein
assert (WE2[KRALLE] > 0).sum(1).max() == 1


# ------------------------------------------------------------------ Haut im Tier-Rahmen (Meter): fuer die Liegehoehe
W_TIER = WE2
J_NAMEN = NAMEN_E


def haut_tier(pose):
    """Lineares Haeuten wie die Engine: v' = Summe w (P + Q (v - J))."""
    out = np.zeros((n_v, 3))
    for k, nm in enumerate(J_NAMEN):
        w = W_TIER[:, k]
        m = w > 0
        if not m.any():
            continue
        q, p = pose[nm]
        R = np.array(q.to_matrix())
        out[m] += w[m, None] * (np.asarray(p) + (Vm[m] - np.asarray(J[nm])) @ R.T)
    return out


def boden_liege():
    """Setzt die Liegepose auf den Boden: der Rumpf (ohne Beine) so tief, dass sein tiefster Punkt aufliegt,
    jede Pfote so hoch, dass sie nicht im Boden steckt. Mehrmals, weil Rumpf und Beine einander verschieben."""
    haupt = np.argmax(W_TIER, 1)
    bein_von = {}
    for key, L in LEG.items():
        for nm in (L["oben"], L["unten"], L["fuss"]):
            bein_von[J_NAMEN.index(nm)] = key
    rumpf_m = np.array([bein_von.get(int(k)) is None for k in haupt])
    pfote = {key: np.array([J_NAMEN[int(k)] == L["fuss"] for k in haupt]) for key, L in LEG.items()}
    for _ in range(6):
        P = haut_tier(pose_dead(0, {}))
        LIEGE["pel"].z += 0.006 - float(P[rumpf_m, 2].min())
        for key, m in pfote.items():
            tief = float(P[m, 2].min())
            if tief < 0.004:
                ank, q = LIEGE["fuss"][key]
                LIEGE["fuss"][key] = (ank + vec(0, 0, 0.004 - tief), q)
    P = haut_tier(pose_dead(0, {}))
    teile = {}
    for k, nm in enumerate(J_NAMEN):
        m = haupt == k
        if m.any():
            teile[nm.replace("Bip01_", "")] = round(float(P[m, 2].min()), 3)
    log("Liegepose: Becken z %.3f m, tiefster Punkt %.3f m; je Teil tiefster Punkt" % (LIEGE["pel"].z, P[:, 2].min()), teile,
        "Fersen", {k: tuple(round(v, 3) for v in LIEGE["fuss"][k][0]) for k in LEG})


# ------------------------------------------------------------------ Maul: Schnitt an der Lippenlinie, Mundhoehle, Fangzaehne
# Das Spielnetz hat ein geschlossenes Maul (bau_stehend.md). Hier wird es entlang c = lippe(a, |b|) vor dem Mundwinkel
# aufgeschnitten (Dreiecke an der Linie geteilt, Punkte auf der Linie verdoppelt: oben folgt dem Kopf, unten dem Kiefer).
# In den Schlitz kommt ein geschlossener Beutel: Gaumen oben, Zunge unten, hinten an einer Linie quer durch die Mundwinkel
# verbunden. Zu liegt er flach in der Lippenebene im Kopf und ist unsichtbar, offen ist er die dunkle Mundhoehle. Dazu vier
# Fangzaehne als eigene Schalen. Alles bleibt EIN Netz mit EINEM Material; Gaumen, Zunge und Zaehne zeigen auf drei Flecken
# der Textur, die die UV-Belegung frei laesst (gemessen: 58,6 % belegt, Flecken mit 16 px Abstand zu jeder Insel).
FLECK_GAUMEN = (280, 16, 80, 80)    # Bildpixel x, y (von oben), Breite, Hoehe in der 1024er Textur
FLECK_ZUNGE = (376, 16, 80, 80)
FLECK_ZAHN = (472, 16, 24, 24)
TEX_R = 1024
GEWOELBE, MULDE = 0.012, 0.008      # Gaumen nach oben, Zunge nach unten gewoelbt (Kopfeinheiten), damit sie offen Tiefe hat


def fleck_uv(fl, s, t):
    x0, y0, w, h = fl
    px = x0 + 2.0 + np.clip(s, 0.0, 1.0) * (w - 4.0)
    py = y0 + 2.0 + np.clip(t, 0.0, 1.0) * (h - 4.0)
    return np.stack((px / TEX_R, 1.0 - py / TEX_R), -1)


def kiefer_anteil(a, f, seite):
    """Anteil des Unterkiefers am Kopfgewicht. f = c - lippe (oben positiv). Vor dem Mundwinkel trennt der Schnitt scharf,
    am Winkel je die Haelfte, dahinter laeuft es weich ueber die Wange aus (wie kiefer_gewicht in baer_quelle.py)."""
    s = 0.025 + np.maximum(K_ECKE - a, 0.0) * 0.5
    g = 1.0 - sst(-s, s, f)
    r = sst(K_ECKE, K_ECKE + 0.05, a)
    oben = (1.0 - r) * g
    unten = 1.0 - (1.0 - r) * (1.0 - g)
    return np.where(seite > 0, oben, unten) * sst(0.06, K_ECKE - 0.012, a)


def maul_bauen(V, T, UVc, W, namen):
    n0 = len(V)
    LC = fbx2l(V)
    a, b, c = LC[:, 0], LC[:, 1], LC[:, 2]
    f = c - k_lippe(a, np.abs(b))
    f = np.where(np.abs(f) < 1e-7, 1e-7, f)
    # Der Schnitt reicht 3 cm (Kopfeinheiten) hinter den Mundwinkel: dort sind oben und unten noch gleich gewichtet (je die
    # Haelfte), die Enden des Schnitts und die hintere Naht des Beutels liegen also sicher dort, wo der Spalt zu bleibt.
    reg = (a > K_ECKE - 0.03) & (V[:, 0] > 0.80)
    neu_p, neu_w, kante = [], [], {}

    def teil(p, q):
        k = (min(p, q), max(p, q))
        if k not in kante:
            i0, i1 = k
            if reg[i0] and reg[i1] and f[i0] * f[i1] < 0:
                t = f[i0] / (f[i0] - f[i1])
                kante[k] = (n0 + len(neu_p), i0, t)
                neu_p.append(V[i0] + (V[i1] - V[i0]) * t)
                neu_w.append(W[i0] + (W[i1] - W[i0]) * t)
            else:
                kante[k] = None
        return kante[k]

    def uv_auf(s, uv_p, uv_q, p):
        _n, i0, t = s
        u0, u1 = (uv_p, uv_q) if p == i0 else (uv_q, uv_p)
        return u0 + (u1 - u0) * t

    T2, UV2, SEITE, segs, eins = [], [], [], [], []
    for ti in range(len(T)):
        tri = [int(v) for v in T[ti]]
        uvs = [UVc[ti, k].copy() for k in range(3)]
        st = [teil(tri[m], tri[(m + 1) % 3]) for m in range(3)]
        cnt = sum(s is not None for s in st)
        if cnt == 0:
            T2.append(tri)
            UV2.append(uvs)
            SEITE.append(0)
        elif cnt == 1:
            m = [i for i in range(3) if st[i] is not None][0]
            p, q, r = tri[m], tri[(m + 1) % 3], tri[(m + 2) % 3]
            up, uq, ur = uvs[m], uvs[(m + 1) % 3], uvs[(m + 2) % 3]
            un = uv_auf(st[m], up, uq, p)
            n = st[m][0]
            T2 += [[p, n, r], [n, q, r]]
            UV2 += [[up, un, ur], [un, uq, ur]]
            SEITE += [0, 0]
            eins.append(n)
        elif cnt == 2:
            u = [i for i in range(3) if st[i] is None][0]
            ia, ib, ic = (u + 2) % 3, u, (u + 1) % 3
            a0, b0, c0 = tri[ia], tri[ib], tri[ic]
            ua, ub, uc = uvs[ia], uvs[ib], uvs[ic]
            s1, s2 = st[ia], st[ic]
            n1, n2 = s1[0], s2[0]
            u1 = uv_auf(s1, ua, ub, a0)
            u2 = uv_auf(s2, uc, ua, c0)
            sa = 1 if f[a0] > 0 else -1
            sb = 1 if f[b0] > 0 else -1
            assert sa != sb
            T2 += [[a0, n1, n2], [n1, b0, c0], [n1, c0, n2]]
            UV2 += [[ua, u1, u2], [u1, ub, uc], [u1, uc, u2]]
            SEITE += [sa, sb, sb]
            segs.append((n1, n2))
        else:
            raise RuntimeError("Dreieck mit drei Schnittkanten")
    nb = {}
    for x_, y_ in segs:
        nb.setdefault(x_, []).append(y_)
        nb.setdefault(y_, []).append(x_)
    enden = [v for v, l in nb.items() if len(l) == 1]
    assert len(enden) == 2 and all(len(l) <= 2 for l in nb.values()), ("Schnitt ist keine einfache Linie", len(enden))
    assert set(enden) <= set(eins)
    P_neu = np.array(neu_p)
    enden.sort(key=lambda v: fbx2l(P_neu[v - n0])[1])          # rechts (b < 0) zuerst
    kette_ = [enden[0]]
    vor = None
    while True:
        nx = [v for v in nb[kette_[-1]] if v != vor]
        if not nx:
            break
        vor = kette_[-1]
        kette_.append(nx[0])
    assert kette_[-1] == enden[1] and len(kette_) == len(nb), "Schnitt nicht zusammenhaengend"
    innen = kette_[1:-1]
    V1 = np.vstack((V, P_neu))
    W1 = np.vstack((W, np.array(neu_w)))
    n1_ = len(V1)
    unten_id = {v: n1_ + k for k, v in enumerate(innen)}
    V1 = np.vstack((V1, V1[innen]))
    W1 = np.vstack((W1, W1[innen]))
    for i, tri in enumerate(T2):
        if SEITE[i] < 0:
            T2[i] = [unten_id.get(v, v) for v in tri]
            # Unterlippe: UV um 0,2 Texel versetzt, sonst legt Assimp (JOIN_IDENTICAL_VERTICES) Ober- und Unterlippe an
            # Stellen mit gleicher Normale wieder zu einem Punkt zusammen (gemessen: 2 Paare)
            for k_ in range(3):
                if tri[k_] in unten_id:
                    UV2[i][k_] = UV2[i][k_] + np.array((2.0e-4, 0.0))
        elif SEITE[i] == 0:
            assert not any(v in unten_id for v in tri), "Dreieck ohne Seite an der Schnittlinie"
    n_ken = len(V1)
    f1 = np.concatenate((f, np.zeros(n_ken - n0)))
    seite1 = np.concatenate((np.where(f > 0, 1, -1), np.ones(len(neu_p)), -np.ones(len(innen))))
    lo_ = [kette_[0]] + [unten_id[v] for v in innen] + [kette_[-1]]
    log("Maul: Schnitt %d Kanten, %d Punkte auf der Linie (davon %d verdoppelt), lose Teilpunkte %d" % (len(segs), len(kette_), len(innen), len(set(eins) - set(enden))))

    # ---- Beutel
    VS, WS, SS, FS, US = [], [], [], [], []      # Lage (Spielnetz), Kieferanteil fest, -, -, -
    ih = namen.index("Bip01_Head")

    def dazu(p_fbx, wj):
        VS.append(np.asarray(p_fbx, dtype=float))
        WS.append(wj)
        return n_ken + len(VS) - 1

    LCk = fbx2l(V1)
    pa, pb = LCk[kette_[0]], LCk[kette_[-1]]
    n_hinten = 5
    hinten = []
    for k in range(1, n_hinten + 1):
        q = pb + (pa - pb) * (k / (n_hinten + 1.0))      # von der linken Ecke (Kettenende) zur rechten (Kettenanfang)
        q = np.array((q[0], q[1], float(K_LIP(q[0]))))
        hinten.append(dazu(l2fbx(q), 0.5))
    rand_lok = [LCk[v] for v in kette_] + [fbx2l(VS[i - n_ken]) for i in hinten]
    a_m = float(np.mean([LCk[v][0] for v in kette_]))
    M = np.array((a_m, 0.0, float(K_LIP(a_m))))

    def blatt(rand_ids, oben):
        vz = 1.0 if oben else -1.0
        tiefe = GEWOELBE if oben else MULDE
        ring = []
        for p in rand_lok:
            q = M + (np.asarray(p) - M) * 0.55
            q = np.array((q[0], q[1], float(K_LIP(q[0])) + vz * tiefe * 0.55))
            wj = float(kiefer_anteil(np.array([q[0]]), np.array([0.0]), np.array([1 if oben else -1]))[0])
            ring.append(dazu(l2fbx(q), wj))
        mq = np.array((M[0], 0.0, M[2] + vz * tiefe))
        mid = dazu(l2fbx(mq), float(kiefer_anteil(np.array([M[0]]), np.array([0.0]), np.array([1 if oben else -1]))[0]))
        tris = []
        n = len(rand_ids)
        for j in range(n):
            k = (j + 1) % n
            tris += [[rand_ids[j], rand_ids[k], ring[k]], [rand_ids[j], ring[k], ring[j]], [ring[j], ring[k], mid]]
        return tris

    gaumen = blatt(kette_ + hinten, True)
    zunge = blatt(lo_ + hinten, False)
    aussen = {(t[m], t[(m + 1) % 3]) for t in T2 for m in range(3)}

    def ausrichten(tris, x, y):
        d = {(t[m], t[(m + 1) % 3]) for t in tris for m in range(3)}
        if (x, y) in aussen:
            dreh = (x, y) in d
        else:
            assert (y, x) in aussen
            dreh = (y, x) in d
        return [[t[0], t[2], t[1]] for t in tris] if dreh else tris

    gaumen = ausrichten(gaumen, kette_[1], kette_[2])
    zunge = ausrichten(zunge, lo_[1], lo_[2])

    # ---- Fangzaehne: Kegel, oben am Kopf, unten am Kiefer (Lage wie fang_o/fang_u in baer_quelle.py, in die Huelle gerueckt)
    zaehne = []
    for s in (1.0, -1.0):
        for basis, spitze, r, unten in (((0.430, 0.050 * s, -0.036), (0.428, 0.052 * s, -0.070), 0.0085, False),
                                         ((0.415, 0.044 * s, -0.052), (0.418, 0.046 * s, -0.020), 0.0080, True)):
            B0, S0 = l2fbx(basis), l2fbx(spitze)
            ax = (S0 - B0) / np.linalg.norm(S0 - B0)
            e1 = np.cross(ax, (0.0, 1.0, 0.0))
            e1 /= np.linalg.norm(e1)
            e2 = np.cross(ax, e1)
            wj = 1.0 if unten else 0.0
            ring = [dazu(B0 + (e1 * math.cos(2 * math.pi * k / 6) + e2 * math.sin(2 * math.pi * k / 6)) * r * K_FAKTOR, wj) for k in range(6)]
            sp_ = dazu(S0, wj)
            mi = dazu(B0, wj)
            tr = []
            for k in range(6):
                tr += [[ring[k], ring[(k + 1) % 6], sp_], [mi, ring[(k + 1) % 6], ring[k]]]
            # nach aussen: Normale der ersten Seitenflaeche gegen die Achse
            p0, p1, p2 = (np.asarray(VS[i - n_ken]) for i in tr[0])
            nrm = np.cross(p1 - p0, p2 - p0)
            if np.dot(nrm, (p0 + p1) * 0.5 - B0) < 0:
                tr = [[t[0], t[2], t[1]] for t in tr]
            zaehne += tr
    VB = np.array(VS)
    V2 = np.vstack((V1, VB))
    n2 = len(V2)
    # ---- Gewichte: der Kopfanteil teilt sich in Kopf und Kiefer
    W2 = np.zeros((n2, len(namen) + 1))
    W2[:n_ken, :len(namen)] = W1
    W2[n_ken:, ih] = 1.0
    LC2 = fbx2l(V2)
    wj = np.zeros(n2)
    wj[:n_ken] = kiefer_anteil(LC2[:n_ken, 0], f1, seite1)
    wj[n_ken:] = np.array(WS)
    W2[:, -1] = W2[:, ih] * wj
    W2[:, ih] *= (1.0 - wj)
    W2[W2 < 1e-4] = 0.0
    o = np.argsort(-W2, axis=1)
    keep = np.zeros_like(W2, dtype=bool)
    np.put_along_axis(keep, o[:, :4], True, axis=1)
    W2[~keep] = 0.0
    W2 /= W2.sum(1, keepdims=True)
    # ---- Flaechen und UV
    T_all = [list(t) for t in T2] + gaumen + zunge + zaehne
    UVm = [np.array(u) for u in UV2]

    def uv_blatt(tris, fl):
        out = []
        for t in tris:
            L_ = LC2[t]
            out.append(fleck_uv(fl, (L_[:, 1] + 0.11) / 0.22, (L_[:, 0] - 0.25) / 0.27))
        return out

    UVm += uv_blatt(gaumen, FLECK_GAUMEN) + uv_blatt(zunge, FLECK_ZUNGE)
    zuv = fleck_uv(FLECK_ZAHN, np.array(0.5), np.array(0.5))
    UVm += [np.tile(zuv, (3, 1)) for _ in zaehne]
    T_all = np.array(T_all, dtype=np.int64)
    UVm = np.array(UVm)
    # ---- Pruefung: geschlossen und gleich ausgerichtet (jede gerichtete Kante genau einmal, ihre Gegenkante genau einmal)
    gk = {}
    for t in T_all:
        for m in range(3):
            e = (int(t[m]), int(t[(m + 1) % 3]))
            gk[e] = gk.get(e, 0) + 1
    doppelt = sum(1 for v in gk.values() if v > 1)
    offen = sum(1 for e in gk if (e[1], e[0]) not in gk)
    assert doppelt == 0 and offen == 0, ("Netz offen oder verdreht", doppelt, offen)
    scharf = [(kette_[i], kette_[i + 1]) for i in range(len(kette_) - 1)] + [(lo_[i], lo_[i + 1]) for i in range(len(lo_) - 1)]
    hk = [kette_[-1]] + hinten + [kette_[0]]
    scharf += [(hk[i], hk[i + 1]) for i in range(len(hk) - 1)]
    info = dict(kette=len(kette_), beutel=len(gaumen) + len(zunge), zaehne=len(zaehne), punkte=n2, dreiecke=len(T_all),
                kiefer_punkte=int((W2[:, -1] > 0.5).sum()))
    log("Maul:", info)
    return V2, T_all, UVm, W2, namen + ["Bip01_Jaw"], scharf


def netz_ersetzen(V, T, UVm, W, namen, scharf):
    me2 = bpy.data.meshes.new("NCBear")
    Vb_ = np.stack((V[:, 1], -V[:, 0], V[:, 2]), 1) * M2U
    me2.from_pydata(Vb_.tolist(), [], T.tolist())
    me2.update()
    uvl = me2.uv_layers.new(name="UVMap")
    uvl.data.foreach_set("uv", UVm.reshape(-1).astype(np.float32))
    me2.shade_smooth()
    ev = np.empty(len(me2.edges) * 2, dtype=np.int64)
    me2.edges.foreach_get("vertices", ev)
    ev = ev.reshape(-1, 2)
    such = {(min(int(p), int(q)), max(int(p), int(q))): i for i, (p, q) in enumerate(ev)}
    sh = np.zeros(len(ev), dtype=bool)
    for p, q in scharf:
        sh[such[(min(p, q), max(p, q))]] = True
    at = me2.attributes.get("sharp_edge") or me2.attributes.new("sharp_edge", "BOOLEAN", "EDGE")
    at.data.foreach_set("value", sh)
    me2.materials.append(mat)
    me2.update()
    mo.data = me2
    mo.vertex_groups.clear()
    for k, nm in enumerate(namen):
        vg = mo.vertex_groups.new(name=nm)
        for i in np.nonzero(W[:, k] > 0)[0]:
            vg.add([int(i)], float(W[i, k]), "REPLACE")
    log("Netz mit Maul:", len(V), "Punkte", len(T), "Dreiecke, scharfe Kanten", int(sh.sum()), "Knochen mit Gewicht", int((W.sum(0) > 0).sum()))


me.calc_loop_triangles()
_lt_uv = np.empty(len(me.loops) * 2, dtype=np.float64)
me.uv_layers.active.data.foreach_get("uv", _lt_uv)
_lt_uv = _lt_uv.reshape(-1, 2)
_lt_lo = np.empty(n_t * 3, dtype=np.int64)
me.loop_triangles.foreach_get("loops", _lt_lo)
UV_ECKEN = _lt_uv[_lt_lo.reshape(n_t, 3)]
netz_ersetzen(*maul_bauen(Vm, Tri, UV_ECKEN, WE2, NAMEN_E))


# ------------------------------------------------------------------ Armature
def baue_rig():
    arm = bpy.data.armatures.new("Rig")
    ao = bpy.data.objects.new("Rig", arm)
    scene.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao
    ao.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    EB = arm.edit_bones
    d = EB.new("Dummy01")
    d.head = (0, 0, 0)
    d.tail = (0, -0.1, 0)
    d.roll = math.pi
    b = EB.new("Bip01")
    b.head = t2b(J["Bip01"])
    b.tail = t2b(J["Bip01"] + vec(0.18, 0, 0))
    b.roll = 0
    b.parent = d
    for nm in ORDER[2:]:
        h, t, p = BONES[nm]
        e = EB.new(nm)
        e.head = t2b(h)
        e.tail = t2b(t)
        e.roll = 0
        e.parent = EB[p]
    td = EB.new("Translation_Data")
    td.head = (0, 0, 0)
    td.tail = (0, 0, 0.1)
    td.roll = 0
    bpy.ops.object.mode_set(mode="OBJECT")
    return ao


ao = baue_rig()
log("Knochen", len(ao.data.bones))
for _nm in ("Dummy01", "Bip01", "Bip01_Pelvis", "Bip01_L_Thigh"):
    log("RUHE", _nm, [round(v, 6) for row in ao.data.bones[_nm].matrix_local for v in row])
assert len(ao.data.bones) <= 60
mo.parent = ao
mod = mo.modifiers.new("skelett", "ARMATURE")
mod.object = ao
ao.animation_data_create()
for pb in ao.pose.bones:
    pb.rotation_mode = "QUATERNION"
bpy.context.view_layer.update()


# ------------------------------------------------------------------ Pose in Schluessel
def schluessel(pose, f, prev, weg):
    M_pose = {}
    pbs = ao.pose.bones
    for nm in ORDER:
        bone = ao.data.bones[nm]
        q, p = pose[nm]
        rest = bone.matrix_local
        rot = (qb(q).to_matrix().to_4x4() @ rest.to_quaternion().to_matrix().to_4x4())
        M = Matrix.Translation(t2b(p)) @ rot
        M_pose[nm] = M
        par = PARENT[nm]
        if par is None:
            B = rest.inverted() @ M
        else:
            L_rest = ao.data.bones[par].matrix_local.inverted() @ rest
            B = L_rest.inverted() @ M_pose[par].inverted() @ M
        loc, qq, _s = B.decompose()
        qv = prev.get(nm)
        if qv is not None and qv.dot(qq) < 0:
            qq = -qq
        prev[nm] = qq.copy()
        pb = pbs[nm]
        pb.location = loc
        pb.rotation_quaternion = qq
        pb.scale = (1, 1, 1)
        pb.keyframe_insert("location", frame=f)
        pb.keyframe_insert("rotation_quaternion", frame=f)
        pb.keyframe_insert("scale", frame=f)
    td = pbs["Translation_Data"]
    td.location = (0, 0, weg)
    td.rotation_quaternion = (1, 0, 0, 0)
    td.scale = (1, 1, 1)
    td.keyframe_insert("location", frame=f)
    td.keyframe_insert("rotation_quaternion", frame=f)
    td.keyframe_insert("scale", frame=f)


def clip(name, fn, n, weg_ende):
    """n Abschnitte: Bilder 1..n+1, Bild n+1 ist bei Schleifen gleich Bild 1 (ausser dem Weg)."""
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    ao.animation_data.action = act
    prev = {}
    stat = {}
    for i in range(n + 1):
        pose = fn(i, stat)
        schluessel(pose, i + 1, prev, weg_ende * i / max(n, 1))
    ao.animation_data.action = None
    if stat.get("wo"):
        log("Clip", name, "ueberstreckt (Bein: Laenge/Reichweite je Bild)", stat["wo"])
    log("Clip", name, "Bilder", n + 1, "Dauer %.3f s" % (n / FPS), "Weg %.4f" % weg_ende, "Tempo %.3f E/s = %.2f Kacheln/s" % (weg_ende / (n / FPS), weg_ende / (n / FPS) * 1.6),
        "Bein max %.3f der Laenge, ueber Grenze %d Mal, Fehl %.4f m, Knie/Ellbogen weiter gebeugt bis %.1f Grad, Oberschenkel geschwenkt bis %.1f Grad, Rumpf gesenkt bis %.3f m, Brust geneigt bis %.1f Grad" % (stat.get("max", 0), stat.get("ueber", 0), stat.get("fehl", 0), stat.get("knick", 0), stat.get("schwung", 0), stat.get("absenk", 0), stat.get("neig", 0)))
    return act


def weg_gang(G):
    # Stuetzpfote laeuft S/duty je Zyklus (Meter) rueckwaerts. Der Spieler sieht sie mit 1,5 je Einheit, das Tier laeuft mit 1,6 je Einheit.
    return G["S"]["H"] / G["duty"] * M2U / K_WELT


boden_liege()
clip("DeerStag_Idle01", pose_idle, IDLE_T, 0.0)
clip("DeerStag_Walk", pose_walk, WALK["T"], weg_gang(WALK))
clip("DeerStag_Run", pose_run, RUN["T"], weg_gang(RUN))
clip("DeerStag_Death", pose_death, DEATH_N - 1, 0.0)
clip("DeerStag_Dead", pose_dead, 1, 0.0)
for _nm, _fn, _T, _zeiten in KAMPF_CLIPS:
    _sp = spuren_bauen(_fn(), _T)
    _st = {}
    clip(_nm, lambda i, stat, S=_sp, st=_st: kampf_pose(S, i / FPS, st), int(round(_T * FPS)), 0.0)
    for _k in ("VL", "VR", "HL", "HR"):
        _s = _st.get(_k, {})
        log("Clip", _nm, _k, "Bein max %.3f der Laenge, ueber Grenze %d Bilder, Fehl %.4f m, bei t =" % (_s.get("max", 0.0), _s.get("ueber", 0), _s.get("fehl", 0.0)), _s.get("zeiten", []))
    kampf_diag(_nm, _sp, _zeiten)
ao.animation_data.action = None
for pb in ao.pose.bones:
    pb.location = (0, 0, 0)
    pb.rotation_quaternion = (1, 0, 0, 0)
    pb.scale = (1, 1, 1)
bpy.context.view_layer.update()

# ------------------------------------------------------------------ Export
os.makedirs(ZIEL + "models_X/Skinned", exist_ok=True)
os.makedirs(ZIEL + "textures/Body", exist_ok=True)


def exportiere(pfad, ob_a, ob_m, anim):
    bpy.ops.object.select_all(action="DESELECT")
    ob_a.select_set(True)
    ob_m.select_set(True)
    bpy.context.view_layer.objects.active = ob_a
    bpy.ops.export_scene.gltf(
        filepath=pfad, export_format="GLB", use_selection=True, export_yup=True, export_skins=True, export_animations=anim,
        export_animation_mode="ACTIONS", export_anim_slide_to_zero=True, export_apply=False, export_morph=False,
        export_cameras=False, export_lights=False, export_materials="PLACEHOLDER", export_texcoords=True, export_normals=True,
        export_tangents=False, export_vertex_color="NONE",
    )
    log("Export", pfad, os.path.getsize(pfad), "Byte")


exportiere(ZIEL + "models_X/Skinned/NCBear.glb", ao, mo, True)

# ------------------------------------------------------------------ Rueckfall: dasselbe Netz, Knochen und Ruhehaltung genau wie das Reh
if DEER:
    sys.path.insert(0, os.path.dirname(os.path.abspath(DEER)))
    from dumpread import lese

    D = lese(DEER)
    names, par_d = D["names"], D["par"]
    T_S = np.array(((1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 0), (0, 0, 0, 1)), dtype=float)   # Blender (x,y,z) <-> Modell (x,z,y)
    C_F = np.diag((1.0, 1.0, -1.0, 1.0))                                                    # Assimp MAKE_LEFT_HANDED
    clip0 = next(iter(D["clips"].values()))
    arm2 = bpy.data.armatures.new("Rig")
    ao2 = bpy.data.objects.new("RigDeer", arm2)
    scene.collection.objects.link(ao2)
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = ao2
    ao2.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    EB2 = arm2.edit_bones
    for i, nm in enumerate(names):
        off = D["off"][i]
        if np.allclose(off, np.eye(4)):
            W_ = clip0["M"][0][i]          # Knochen ohne Haut beim Reh: nur als Knoten da
        else:
            W_ = np.linalg.inv(off)
        B_ = T_S @ W_ @ C_F
        e = EB2.new(nm)
        e.head = (0, 0, 0)
        e.tail = (0, 0.03, 0)
        e.matrix = Matrix(B_.tolist())
        e.length = 0.03
    for i, nm in enumerate(names):
        if par_d[i] >= 0 and nm != "Translation_Data":
            EB2[nm].parent = EB2[names[par_d[i]]]
    bpy.ops.object.mode_set(mode="OBJECT")
    me2 = me.copy()
    me2.name = "NCBear"
    mo2 = bpy.data.objects.new("NCBearDeer", me2)
    scene.collection.objects.link(mo2)
    mo2.parent = ao2
    m2 = mo2.modifiers.new("skelett", "ARMATURE")
    m2.object = ao2

    # Rumpf wie beim eigenen Skelett. Beine nach der Hoehe ueber dem Boden auf die langen Rehknochen:
    # die Haut des kurzen Baerenbeins liegt dort, wo beim Reh Mittelfuss und Zehe laufen, und bleibt so am Boden.
    h = z * M2U
    a = rumpf_anteile()
    namen2, W2 = [], []

    def dazu2(n, w):
        namen2.append(n)
        W2.append(w)

    # Der Stummelschwanz geht hier mit dem Becken: der Rehschwanz stellt sich auf und waere ein Stachel
    a["Pelvis"] = a["Pelvis"] + a["Tail"]
    for k in ("Pelvis", "Spine", "Spine1", "Neck", "Head"):
        dazu2("Bip01_" + k, a[k] * (1.0 - L_ALL))
    w_toe = 1.0 - sst(0.03, 0.07, h)
    w_hock = sst(0.26, 0.33, h)
    w_th = sst(0.36, 0.44, h)
    w_fin = 1.0 - sst(0.06, 0.11, h)
    w_ha = sst(0.20, 0.25, h)
    w_ua = sst(0.37, 0.43, h)
    for n, ss in (("L", y > 0), ("R", y <= 0)):
        ss = ss.astype(float)
        dazu2("Bip01_%s_Thigh" % n, L_H * ss * w_th)
        dazu2("Bip01_%s_Calf" % n, L_H * ss * (w_hock - w_th))
        dazu2("Bip01_%s_Foot" % n, L_H * ss * ((1.0 - w_hock) - w_toe))
        dazu2("Bip01_%s_Toe0" % n, L_H * ss * w_toe)
        dazu2("Bip01_%s_UpperArm" % n, L_V * ss * w_ua)
        dazu2("Bip01_%s_Forearm" % n, L_V * ss * (w_ha - w_ua))
        dazu2("Bip01_%s_Hand" % n, L_V * ss * ((1.0 - w_ha) - w_fin))
        dazu2("Bip01_%s_Finger0" % n, L_V * ss * w_fin)
    W2 = np.stack(W2, 1)
    for n, ss in (("L", y > 0), ("R", y <= 0)):
        for nm, cond in (("Finger0", x > 0), ("Toe0", x <= 0)):
            k = namen2.index("Bip01_%s_%s" % (n, nm))
            m = KRALLE & ss & cond
            W2[m, :] = 0.0
            W2[m, k] = 1.0
    for vg in list(mo2.vertex_groups):
        mo2.vertex_groups.remove(vg)
    setze_gewichte(mo2, W2, namen2, {"Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Head"})
    bpy.context.view_layer.update()
    exportiere(ZIEL + "models_X/Skinned/NCBearDeer.glb", ao2, mo2, False)

# ------------------------------------------------------------------ Textur
img = bpy.data.images.load(QUELLE + "textures/WorldItems/NCBear.png")
img.colorspace_settings.name = "Non-Color"
w0, h0 = img.size
a = np.empty(w0 * h0 * 4, dtype=np.float32)
img.pixels.foreach_get(a)
a = a.reshape(h0, w0, 4)
assert w0 == 2048 and h0 == 2048
kl = (a[0::2, 0::2] + a[1::2, 0::2] + a[0::2, 1::2] + a[1::2, 1::2]) * 0.25
kl[..., 3] = 1.0


def fleck_malen(fl, farbe):
    """Malt einen Fleck (Bildpixel von oben) samt 4 px Saum in kl; farbe(s, t) -> (h, w, 3) sRGB 0..1."""
    x0, y0, w, h = fl
    ys = np.arange(y0 - 4, y0 + h + 4)
    xs = np.arange(x0 - 4, x0 + w + 4)
    s = (xs + 0.5 - (x0 + 2.0)) / (w - 4.0)
    t = (ys + 0.5 - (y0 + 2.0)) / (h - 4.0)
    S_, T_ = np.meshgrid(np.clip(s, 0, 1), np.clip(t, 0, 1))
    kl[(TEX_R - 1 - ys)[:, None], xs[None, :], :3] = farbe(S_, T_)


def gaumen_farbe(s, t):
    rand = 1.0 - np.abs(2.0 * s - 1.0)
    rippen = 1.0 + 0.30 * np.maximum(np.cos(2 * math.pi * t * 7.0), 0.0) * sst(0.15, 0.45, rand)
    hell = (0.62 + 0.38 * sst(0.0, 0.6, rand)) * rippen
    return np.stack((0.20 * hell, 0.085 * hell, 0.085 * hell), -1)


def zungen_farbe(s, t):
    m = np.abs(s - 0.5)
    zunge = 1.0 - sst(0.20, 0.34, m)
    rille = 1.0 - 0.25 * np.exp(-((s - 0.5) / 0.035) ** 2)
    tief = 0.65 + 0.35 * sst(0.0, 0.7, t)
    rot = np.array((0.62, 0.30, 0.31))
    dunkel = np.array((0.21, 0.085, 0.085))
    c_ = dunkel + (rot - dunkel) * (zunge * rille * tief)[..., None]
    return c_


fleck_malen(FLECK_GAUMEN, gaumen_farbe)
fleck_malen(FLECK_ZUNGE, zungen_farbe)
fleck_malen(FLECK_ZAHN, lambda s, t: np.broadcast_to(np.array((0.86, 0.81, 0.69)), s.shape + (3,)).copy())
log("Textur: Flecken fuer Gaumen, Zunge, Zaehne gemalt", FLECK_GAUMEN, FLECK_ZUNGE, FLECK_ZAHN)
i2 = bpy.data.images.new("NCBearBody", 1024, 1024, alpha=False)
i2.colorspace_settings.name = "Non-Color"
i2.pixels.foreach_set(kl.ravel())
i2.filepath_raw = ZIEL + "textures/Body/NCBear.png"
i2.file_format = "PNG"
i2.save()
log("Textur", ZIEL + "textures/Body/NCBear.png", os.path.getsize(ZIEL + "textures/Body/NCBear.png"), "Byte")
log("TIER_OK")
log("KAMPF_OK")
