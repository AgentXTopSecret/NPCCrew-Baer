# Baer als lebendes Tier (Project Zomboid B42.21): baut aus dem fertigen Spielnetz die zwei GLB-Dateien und die Koerpertextur.
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
DEER = ARGS[1] if len(ARGS) > 1 else None
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


def rumpf(pose, pel_p, q_pel, q_sp, q_ch, q_ne, q_he, q_ta):
    pose["Dummy01"] = (Quaternion(), J["Dummy01"].copy())
    pose["Bip01"] = (Quaternion(), J["Bip01"].copy())
    pose["Bip01_Pelvis"] = (q_pel.copy(), pel_p.copy())
    kette(pose, "Bip01_Spine", q_sp)
    kette(pose, "Bip01_Spine1", q_ch)
    kette(pose, "Bip01_Neck", q_ne)
    kette(pose, "Bip01_Head", q_he)
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
i2 = bpy.data.images.new("NCBearBody", 1024, 1024, alpha=False)
i2.colorspace_settings.name = "Non-Color"
i2.pixels.foreach_set(kl.ravel())
i2.filepath_raw = ZIEL + "textures/Body/NCBear.png"
i2.file_format = "PNG"
i2.save()
log("Textur", ZIEL + "textures/Body/NCBear.png", os.path.getsize(ZIEL + "textures/Body/NCBear.png"), "Byte")
log("TIER_OK")
