# Lauf baer-junges-fuss (11.11.2026 nachts), Bauer CLIPS: Sitz-Clips des ALTEN Jungen (NCBearCub.glb 6c3f0a96) aus den Sitz-Clips des
# grossen Baeren umrechnen -- wiederholbar, reines numpy (kein Blender), deterministisch. Kevin 11.11.: "das es beim sitzen nicht so
# scheisse aussieht ... sondern wie unser grosser baer" (ENTSCHEIDUNGEN.md, ganz unten). Weg (PLAN_JFUSS.md 5.1/5.2):
#   1. Grund: Drehungen der Quelle (2c) auf dem Skelett des Jungen; Lagen = Ruhe des Jungen, Becken-Lage = Quelle x diag(S_eltern).
#   2. w(t) "wie weit sitzt die Quelle" (Brust-Neigung + Beckenhoehe der Quelle, monoton in SitDown/StandUp, 1 in Sit).
#   3. Vorbeugen: Becken w*dB, Lende w*dL (Welt-Querachse), Brust gegen Lende wie Quelle.
#   4. Kopf: Weltdrehung = Quelle (Blick wie der grosse Baer); Hals nimmt das Vorbeugen zurueck, so weit die Grenze Hals/Brust laesst.
#   5. Vorderbein: 2-Knochen-IK, Pfote mit der Weltdrehung der Quelle (flach); Ziel = Pfotenweg der Quelle auf das Junge abgebildet.
#   6. Hinterbein: 2-Knochen-IK, Fuss mit der Weltdrehung der Quelle, Sprunggelenk wie im Grund, Ferse/Sohle auf den Boden.
#   7. Boden je Bild exakt (tiefster Hautpunkt 0; sitzt die Quelle auf, sitzt auch das Junge auf). SitDown Bild 0 und StandUp Bild 39 = heute.
# Rechnet alles im glTF-Raum der GLB (Tier-Rahmen: x vorn = glTF z, y links = glTF x, z oben = glTF y; Meter = Einheiten / 0,544).
# Aufruf:
#   python baer_sitz_jfuss.py [--quelle Q.glb] [--junges J.glb] [--netz N.npz] [--gewichte G.npz] --aus A.npz [--clips a,b,c] [--rear]
#                             [--par JSON] [--bericht B.json]
#   --quelle: Vorgabe quelle/2c/NCBear.glb (08ec7806). Spaeter mit EINEM Befehl die Sitz-Clips von baer-gross: --quelle <Endstand>/NCBear.glb
#   --rear  : NCBear_Rear vorbereitet (Drehungs-Kopie + Hinterfuss-IK + Boden); wird in diesem Lauf NICHT ausgeliefert.
# Ausgabe A.npz: je Clip <clip>__T (Zeiten), <clip>__t (Bilder x 26 x 3, glTF-lokal), <clip>__q (Bilder x 26 x 4, x y z w), <clip>__w;
#   Bericht (JSON) mit Kontakten, Grenzen, Spruengen je Bild. Statisch/offline gerechnet, nicht gespielt. Schreibt nur --aus/--bericht.
import argparse
import json
import math
import struct
import sys

import numpy as np

ARB = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges_fuss/"
QUELLE_STD = ARB + "quelle/2c/NCBear.glb"
JUNGES_STD = ARB + "quelle/cub/NCBearCub.glb"
NETZ_STD = ARB + "form/jfuss.npz"
SITZ = ("NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp")
M2U = 0.544
CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
B_T = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])     # glTF-Richtung -> Tier-Richtung (det +1)

# Parameter der Korrektur-Schicht (Grad / Meter, Tier-Rahmen). Startwerte aus PLAN 2.3 (probe_suche), Endwerte aus der Suche (CLIPS.md).
# fix1 (Nachbesserung 12.11.2026, Pruefer Optik M1 blocker "kauert wie eine Katze"): aufrecht wie der 2c statt flach vorgebeugt.
#   Vorher dB -20 / dL +6 (Becken-Welt 20,5, Becken->Hals 26 Grad, Laenge/Hoehe 1,44). Suche fix1/log/suche_m1_*.txt: mit flacher Sohle
#   erreichen die kurzen Arme des Jungen den Boden nur bei Becken <= ~-18 (runder Ruecken ueber Lende/Brust senkt die Schulter kaum);
#   daher Becken -5 (Becken-Welt 35,5, wie heute 37 / 2c 39) und die Vorderpfoten im Sitzen Zehen nach unten gekippt (v_kipp 45):
#   Becken->Hals 37,2 Grad, Kopfgelenk 52,5 (E x 100), Laenge/Hoehe 1,18; Arme gerade, Zehenballen am Boden.
#   Alte Haltung (byte-gleich 7f1be7bf): --par '{"dB": -20, "dL": 6, "v_kipp": 0, "glatt_ziel": 0}'.
PAR = dict(
    dB=-5.0,             # Becken: Welt-Nicken (+ = vorn hoch) bei w = 1 (fix1; vorher -20)
    dL=0.0,              # Lende zusaetzlich (+ = Lende wieder auf) (fix1; vorher +6)
    dC=0.0,              # fix1: Brust zusaetzlich gegen die Lende (+ = auf, - = runder Ruecken)
    v_kipp=45.0,         # fix1: Vorderpfote im Sitzen Zehen nach unten (Grad bei w = 1); 0 = flache Sohle wie vorher
    hals=0.0,            # Anteil des Vorbeugens, den der Hals zuruecknimmt (bis zur Grenze Hals gegen Brust)
    hals_k=0.5,          # Hals gegen Brust: Anteil der Quell-Drehung bei w = 1 (1 = wie Quelle). Abwaegung (clips/log/suche_hals.txt):
                         # 1,0 Hals-Loft dehnt 6,3-6,6, Kragen -1,8/-3,9 cm; 0,3: 2,5-2,7 / +2,7/+0,5; 0,5: 3,6-3,8 (heute 3,5-3,7) / +1,4/-0,7
    h_dy=0.02,           # Hinterfuesse im Sitzen je Seite so viel weiter aussen (Luecke Hinterfuss/Vorderpfote >= 2 cm, Fussabstand <= 64)
    hals_extra=0.0,      # Hals zusaetzlich steiler (Grad, + = Kopf hoch) bei w = 1
    klav=0.0,            # Schulterblatt zusaetzlich nicken (kampf-Masse, + = Schulter tiefer) bei w = 1
    v_dx=0.01,           # Vorderpfote im Sitzen: Handgelenk x = Schultergelenk x + v_dx
    v_y=0.111,           # Vorderpfote im Sitzen: Ballen |y| (Luecke Pfote/Pfote >= 1 cm)
    kontakt=0.005,       # Quelle: Sohle/Ferse/Sitzflaeche tiefer als 0,5 cm = Bodenkontakt
    schwung=0.74,        # Schwung-Hoehe Quelle -> Junges (Beine 0,74)
    w_glatt=1,           # Glaettung von w (+-Bilder)
    anschluss=3,         # SitDown/StandUp: weicher Anschluss an das feste Bild 0/39 (Bilder)
    rand=0.3,            # Abstand zu den Gelenkgrenzen (Grad)
    knie_max=138.0,      # Hinterbein: Knie hoechstens so weit gestreckt (Innenwinkel); sonst rueckt das Sprunggelenk zur Huefte
    fuss_kipp=5.0,       # Hinterfuss darf gegen die Quelle hoechstens so weit kippen (Grad), nur um die Grenze dors zu halten
    glatt_ziel=2,        # fix1 (T4): Pfoten-Zielweg in SitDown/StandUp +- so viele Bilder glaetten (0 = aus wie vor fix1)
)
# Gelenkgrenzen wie baer_kampf_2c.py (GRENZEN, GRENZEN_RUMPF_SITZ, GRENZE_KLAV, SPRUNG): Messgroessen dort, hier in numpy nachgebaut.
GRENZEN = {
    "V": dict(prot=(-70, 60), abd=(-20, 45), tw=(-35, 20), inner=(55, 173), dors=(-115, 75), seitab=(-15, 15), sup=(-20, 35)),
    "H": dict(prot=(-60, 80), abd=(-15, 35), tw=(-25, 15), inner=(55, 174), dors=(-125, -45), seitab=(-12, 12), sup=(-20, 20)),
}
GRENZEN_RUMPF = {"sp_pel": ((-12, 12), (-20, 20), (-12, 12)), "ch_sp": ((-15, 15), (-15, 15), (-15, 15)),
                 "ne_ch": ((-35, 35), (-45, 50), (-15, 15)), "he_ne": ((-30, 30), (-35, 35), (-25, 25))}
GRENZEN_RUMPF_SITZ = dict(GRENZEN_RUMPF, he_ne=((-30, 30), (-35, 60), (-25, 25)))
GRENZE_KLAV = ((-25.0, 20.0), (-15.0, 15.0))
SPRUNG = dict(sup=20.0, tw=20.0, dors=35.0, inner=20.0)    # fix1 (T4): + Ellbogen-/Kniebeugung je Bild
# Ballen in der Ruhe des grossen Baeren (baer_kampf_2c.py BALLEN_V/BALLEN_H, HAND/FERSE) -> beim Jungen relativ zum Gelenk x 0,9402
BALLEN = {"V": ((0.48, 0.22, 0.045), (0.32, 0.23, 0.10)), "H": ((-0.25, 0.24, 0.045), (-0.48, 0.247, 0.10))}
PFOTE_F = 0.9402


# ---------------------------------------------------------------- GLB lesen
def lade_glb(pfad):
    b = open(pfad, "rb").read()
    assert b[:4] == b"glTF"
    n = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + n])
    o = 20 + n
    bl = struct.unpack("<I", b[o:o + 4])[0]
    return J, b[o + 8:o + 8 + bl]


def acc_bytes(J, B, i):
    a = J["accessors"][i]
    v = J["bufferViews"][a["bufferView"]]
    k = NC[a["type"]]
    sz = np.dtype(CT[a["componentType"]]).itemsize
    s = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    st = v.get("byteStride", k * sz)
    if st == k * sz:
        return B[s:s + a["count"] * k * sz]
    return b"".join(B[s + j * st: s + j * st + k * sz] for j in range(a["count"]))


def acc_np(J, B, i):
    a = J["accessors"][i]
    return np.frombuffer(acc_bytes(J, B, i), dtype=CT[a["componentType"]]).reshape(a["count"], NC[a["type"]])


# ---------------------------------------------------------------- Drehungen
def q2m(q):
    q = np.asarray(q, float)
    x, y, z, w = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    n = x * x + y * y + z * z + w * w
    s = np.where(n > 0, 2.0 / n, 0.0)
    R = np.empty(q.shape[:-1] + (3, 3))
    R[..., 0, 0] = 1 - s * (y * y + z * z)
    R[..., 0, 1] = s * (x * y - z * w)
    R[..., 0, 2] = s * (x * z + y * w)
    R[..., 1, 0] = s * (x * y + z * w)
    R[..., 1, 1] = 1 - s * (x * x + z * z)
    R[..., 1, 2] = s * (y * z - x * w)
    R[..., 2, 0] = s * (x * z - y * w)
    R[..., 2, 1] = s * (y * z + x * w)
    R[..., 2, 2] = 1 - s * (x * x + y * y)
    return R


def m2q(R):
    """Drehmatrix -> Quaternion (x, y, z, w), w >= 0 (Shepperd)."""
    m = np.asarray(R, float)
    t = np.trace(m)
    if t > 0:
        s = math.sqrt(t + 1.0) * 2
        q = np.array([(m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s, (m[1, 0] - m[0, 1]) / s, 0.25 * s])
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        q = np.array([0.25 * s, (m[0, 1] + m[1, 0]) / s, (m[0, 2] + m[2, 0]) / s, (m[2, 1] - m[1, 2]) / s])
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        q = np.array([(m[0, 1] + m[1, 0]) / s, 0.25 * s, (m[1, 2] + m[2, 1]) / s, (m[0, 2] - m[2, 0]) / s])
    else:
        s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        q = np.array([(m[0, 2] + m[2, 0]) / s, (m[1, 2] + m[2, 1]) / s, 0.25 * s, (m[1, 0] - m[0, 1]) / s])
    q /= np.linalg.norm(q)
    return q if q[3] >= 0 else -q


def achse_dreh(ax, grad):
    ax = np.asarray(ax, float) / np.linalg.norm(ax)
    a = math.radians(grad)
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K


def orth(R):
    """naechste Drehmatrix (polar, SVD): Weltmatrizen tragen die Skalier-Schluessel (~1 +- 3e-5) mit."""
    U, _, Vt = np.linalg.svd(R)
    M = U @ Vt
    if np.linalg.det(M) < 0:
        U[:, -1] *= -1
        M = U @ Vt
    return M


def lok(Wpar3, Rwelt):
    """lokale 3x3 so, dass Wpar3 @ lokal = orth(Rwelt) genau gilt (Inverse statt Transponierte: die Weltmatrix ist nicht exakt orthonormal)."""
    return np.linalg.inv(Wpar3) @ orth(Rwelt)


def zwischen(a, b):
    """kleinste Drehung, die Richtung a auf b dreht."""
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    v = np.cross(a, b)
    c = float(a @ b)
    s = np.linalg.norm(v)
    if s < 1e-12:
        return np.eye(3)
    return achse_dreh(v, math.degrees(math.atan2(s, c)))


# Tier-Querachse (y, links) in glTF = +x. Nicken um +Grad (+ = vorn hoch) = Drehung um die Tier-y-Achse um -Grad.
QUER_G = np.array([1.0, 0.0, 0.0])


def nick_dreh(grad):
    return achse_dreh(QUER_G, -grad)


def tier(Pg):
    return np.asarray(Pg, float) @ B_T.T / M2U


def gltf(T):
    return (np.asarray(T, float) * M2U) @ B_T


def ypr(Rt):
    """Gieren/Nicken/Rollen wie baer_kampf_2c.ypr (Blender to_euler XYZ: R = Rz Ry Rx, Nicken + = Nase runter), Tier-Rahmen."""
    p = math.degrees(math.asin(max(-1.0, min(1.0, -Rt[2, 0]))))
    y = math.degrees(math.atan2(Rt[1, 0], Rt[0, 0]))
    r = math.degrees(math.atan2(Rt[2, 1], Rt[2, 2]))
    return y, p, r


# ---------------------------------------------------------------- Skelett / Clips / Haut
class Gerippe:
    def __init__(self, pfad):
        self.pfad = pfad
        self.J, self.B = lade_glb(pfad)
        J = self.J
        joints = J["skins"][0]["joints"]
        self.knoten = list(joints)
        self.names = [J["nodes"][k]["name"] for k in joints]
        self.idx = {n: i for i, n in enumerate(self.names)}
        npar = {}
        for i, n in enumerate(J["nodes"]):
            for c in n.get("children", []):
                npar[c] = i
        jix = {k: i for i, k in enumerate(joints)}
        self.par = []
        for k in joints:
            p = npar.get(k, -1)
            while p >= 0 and p not in jix:      # Vorfahren ohne Gelenk (Rig) duerfen keine Lage/Drehung haben
                nd = J["nodes"][p]
                assert not any(x in nd for x in ("translation", "rotation", "scale", "matrix")), nd
                p = npar.get(p, -1)
            self.par.append(jix[p] if p >= 0 else -1)
        nb = len(joints)
        self.t0 = np.zeros((nb, 3))
        self.q0 = np.zeros((nb, 4))
        self.s0 = np.ones((nb, 3))
        for b, k in enumerate(joints):
            n = J["nodes"][k]
            self.t0[b] = n.get("translation", [0, 0, 0])
            self.q0[b] = n.get("rotation", [0, 0, 0, 1])
            self.s0[b] = n.get("scale", [1, 1, 1])
        ibm = acc_np(J, self.B, J["skins"][0]["inverseBindMatrices"]).astype(np.float64)
        self.ibm = np.array([m.reshape(4, 4).T for m in ibm])
        self.W0 = self.fk(self.t0, self.q0, self.s0)
        self.anim = {a["name"]: a for a in J["animations"]}

    def fk(self, t, q, s=None):
        nb = len(self.names)
        L = np.zeros((nb, 4, 4))
        R = q2m(q)
        if s is not None:
            R = R * np.asarray(s)[:, None, :]
        L[:, :3, :3] = R
        L[:, :3, 3] = t
        L[:, 3, 3] = 1.0
        W = np.zeros_like(L)
        for b in range(nb):
            p = self.par[b]
            W[b] = L[b] if p < 0 else W[p] @ L[b]
        return W

    def kanaele(self, clip):
        a = self.anim[clip]
        out = {}
        for ch in a["channels"]:
            nm = self.J["nodes"][ch["target"]["node"]]["name"]
            if nm not in self.idx:
                continue
            smp = a["samplers"][ch["sampler"]]
            out[(nm, ch["target"]["path"])] = (smp["input"], smp["output"], smp.get("interpolation", "LINEAR"), ch["sampler"])
        return out

    def zeiten(self, clip):
        ins = sorted({v[0] for v in self.kanaele(clip).values()}, key=lambda i: -self.J["accessors"][i]["count"])
        return acc_np(self.J, self.B, ins[0]).ravel().astype(np.float64), ins[0]

    def werte(self, clip, T=None):
        """Lokale TRS je Bild (Zeiten T, Vorgabe: die Schluesselzeiten des Clips): t (n,26,3), q (n,26,4), s (n,26,3)."""
        if T is None:
            T, _ = self.zeiten(clip)
        n = len(T)
        nb = len(self.names)
        t = np.repeat(self.t0[None], n, 0)
        q = np.repeat(self.q0[None], n, 0)
        s = np.repeat(self.s0[None], n, 0)
        for (nm, path), (ia, oa, interp, _) in self.kanaele(clip).items():
            b = self.idx[nm]
            ti = acc_np(self.J, self.B, ia).ravel().astype(np.float64)
            vo = acc_np(self.J, self.B, oa).astype(np.float64)
            if len(ti) == n and np.array_equal(ti.astype(np.float32), np.asarray(T).astype(np.float32)):
                v = vo
            else:
                k = np.clip(np.searchsorted(ti, np.asarray(T) + 1e-6, side="right") - 1, 0, len(ti) - 1)
                if interp == "STEP":
                    v = vo[k]
                else:
                    k1 = np.minimum(k + 1, len(ti) - 1)
                    u = np.where(k1 > k, (np.asarray(T) - ti[k]) / np.maximum(ti[k1] - ti[k], 1e-12), 0.0)[:, None]
                    v0, v1 = vo[k], vo[k1]
                    if path == "rotation":
                        v1 = np.where(((v0 * v1).sum(1) < 0)[:, None], -v1, v1)
                        v = v0 * (1 - u) + v1 * u
                        v /= np.linalg.norm(v, axis=1, keepdims=True)
                    else:
                        v = v0 * (1 - u) + v1 * u
            {"translation": t, "rotation": q, "scale": s}[path][:, b] = v
        return t, q, s


def haut(W, ibm, P, Wt, Bi):
    Sk = np.einsum("bij,bjk->bik", W, ibm)
    h = np.c_[P, np.ones(len(P))]
    out = np.zeros((len(P), 3))
    for k in range(Wt.shape[1]):
        out += Wt[:, k:k + 1] * np.einsum("nij,nj->ni", Sk[Bi[:, k]], h)[:, :3]
    return out


def netz_aus_glb(G):
    J, B = G.J, G.B
    pr = J["meshes"][0]["primitives"][0]
    P = acc_np(J, B, pr["attributes"]["POSITION"]).astype(np.float64)
    Bi = acc_np(J, B, pr["attributes"]["JOINTS_0"]).astype(int)
    Wt = acc_np(J, B, pr["attributes"]["WEIGHTS_0"]).astype(np.float64)
    return P, Wt, Bi


def masken(names, P_ruhe_t, Wt, Bi):
    """Zonen aus Gewichten (dominanter Knochen) und Ruhe-Lage (Tier): Pfoten, Fuesse, Ferse, Sitzflaeche."""
    dom = Bi[np.arange(len(Bi)), Wt.argmax(1)]
    ix = {n: i for i, n in enumerate(names)}

    def d(*nn):
        return np.isin(dom, [ix[n] for n in nn])
    M = {"sitz": d("Bip01_Pelvis", "Bip01_Tail", "Bip01_Spine", "Bip01_L_Thigh", "Bip01_R_Thigh")}
    M["kopf"] = d("Bip01_Head", "Bip01_Jaw")
    for s in "LR":
        M["hand_" + s] = d("Bip01_%s_Hand" % s)
        M["fuss_" + s] = d("Bip01_%s_Foot" % s, "Bip01_%s_Toe0" % s)
        fx = P_ruhe_t[M["fuss_" + s], 0]
        M["ferse_" + s] = M["fuss_" + s] & (P_ruhe_t[:, 0] < fx.min() + 0.07)
        M["unterarm_" + s] = d("Bip01_%s_Forearm" % s, "Bip01_%s_Hand" % s)
        M["hbein_" + s] = d("Bip01_%s_Calf" % s, "Bip01_%s_Foot" % s, "Bip01_%s_Toe0" % s)
    return M, dom


# ---------------------------------------------------------------- Messgroessen wie baer_kampf_2c (bein_mass, rumpf_mass)
def twist_swing(R, axis):
    """R = swing @ twist (twist um axis). Rueckgabe Twistwinkel (Grad), swing."""
    q = m2q(R)
    v = q[:3]
    proj = axis * float(v @ axis)
    tw = np.array([proj[0], proj[1], proj[2], q[3]])
    nrm = np.linalg.norm(tw)
    if nrm < 1e-9:
        tw = np.array([0, 0, 0, 1.0])
    else:
        tw /= nrm
    ang = 2.0 * math.atan2(float(tw[:3] @ axis), tw[3])
    ang = (ang + math.pi) % (2 * math.pi) - math.pi
    return math.degrees(ang), R @ q2m(tw).T


def _sag(d):
    return math.degrees(math.atan2(d[0], -d[2]))


def _asin(x):
    return math.degrees(math.asin(max(-1.0, min(1.0, x))))


def _winkel(a, b):
    return math.degrees(math.acos(max(-1.0, min(1.0, float(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))))))


class Messung:
    """Messgroessen der Beine (prot/abd/tw/inner/dors/seitab/sup) und des Rumpfs (ypr gegen Eltern) am Jungen (Tier-Rahmen, Ruhe = Junges)."""

    def __init__(self, G):
        self.G = G
        ix = G.idx
        self.Rw0 = G.W0[:, :3, :3]
        Jt = {n: tier(G.W0[ix[n]][:3, 3]) for n in G.names}
        self.Jt = Jt
        self.ruhe = {}
        for key in ("VL", "VR", "HL", "HR"):
            v, s = key[0], key[1]
            sg = 1 if s == "L" else -1
            oben, unten, fuss = ["Bip01_%s_%s" % (s, k) for k in (("UpperArm", "Forearm", "Hand") if v == "V" else ("Thigh", "Calf", "Foot"))]
            hip0, K0, A0 = Jt[oben], Jt[unten], Jt[fuss]
            ball_a, gel_a = (np.array(x, float) for x in BALLEN[v])
            off = (ball_a - gel_a) * np.array((1, sg, 1))
            off[1] = (ball_a[1] - gel_a[1]) * sg
            ball0 = A0 + off * PFOTE_F
            lat = np.array((0, sg, 0.0))
            d_up0 = (K0 - hip0) / np.linalg.norm(K0 - hip0)
            d_lo0 = (A0 - K0) / np.linalg.norm(A0 - K0)
            d_ft0 = (ball0 - A0) / np.linalg.norm(ball0 - A0)
            n0 = np.cross(d_up0, d_lo0)
            n0 /= np.linalg.norm(n0)
            l_ = (A0 - hip0) / np.linalg.norm(A0 - hip0)
            e0 = K0 - (hip0 + l_ * float((K0 - hip0) @ l_))
            e0 /= np.linalg.norm(e0)
            r = dict(oben=oben, unten=unten, fuss=fuss, lat=lat, d_up0=d_up0, d_lo0=d_lo0, d_ft0=d_ft0, n0=n0, ball0=ball0,
                     tw_sgn=1.0 if float(np.cross(d_up0, e0) @ lat) > 0 else -1.0,
                     sup_sgn=1.0 if float(np.cross(d_lo0, np.array((0, 0, -1.0))) @ (-lat)) > 0 else -1.0,
                     par=G.names[G.par[ix[oben]]])
            self.ruhe[key] = r

    def delta(self, W):
        """Weltdrehung gegen die Ruhe je Knochen, Tier-Rahmen."""
        D = np.einsum("bij,bkj->bik", W[:, :3, :3], self.Rw0)
        return np.einsum("ij,bjk,lk->bil", B_T, D, B_T)

    def bein(self, W, D, key):
        r = self.ruhe[key]
        ix = self.G.idx
        q_par, q_up, q_lo, q_ft = (D[ix[n]] for n in (r["par"], r["oben"], r["unten"], r["fuss"]))
        hip, K, A = (tier(W[ix[n]][:3, 3]) for n in (r["oben"], r["unten"], r["fuss"]))
        tw, sw = twist_swing(q_par.T @ q_up, r["d_up0"])
        d1 = sw @ r["d_up0"]
        prot = _sag(d1) - _sag(r["d_up0"])
        abd = _asin(float(d1 @ r["lat"])) - _asin(float(r["d_up0"] @ r["lat"]))
        l_ft = q_lo.T @ q_ft
        sup, _ = twist_swing(l_ft, r["d_lo0"])
        d_ft = l_ft @ r["d_ft0"]
        dors = math.degrees(math.atan2(float(np.cross(r["d_lo0"], d_ft) @ r["n0"]), float(r["d_lo0"] @ d_ft)))
        seitab = _asin(float(d_ft @ r["n0"]))
        ball = A + q_ft @ (r["ball0"] - self.Jt[r["fuss"]])
        return dict(prot=prot, abd=abd, tw=tw * r["tw_sgn"], inner=_winkel(hip - K, A - K), dors=dors, seitab=seitab,
                    sup=sup * r["sup_sgn"], ball=ball)

    def rumpf(self, D):
        ix = self.G.idx
        q = {k: D[ix[k]] for k in ("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Head")}
        r = dict(sp_pel=ypr(q["Bip01_Pelvis"].T @ q["Bip01_Spine"]), ch_sp=ypr(q["Bip01_Spine"].T @ q["Bip01_Spine1"]),
                 ne_ch=ypr(q["Bip01_Spine1"].T @ q["Bip01_Neck"]), he_ne=ypr(q["Bip01_Neck"].T @ q["Bip01_Head"]),
                 pel_welt=ypr(q["Bip01_Pelvis"]), brust_welt=ypr(q["Bip01_Spine1"]), kopf_welt=ypr(q["Bip01_Head"]))
        r["kiefer"] = ypr(q["Bip01_Head"].T @ D[ix["Bip01_Jaw"]])[1]
        for n in "LR":
            r["klav_" + n] = ypr(q["Bip01_Spine1"].T @ D[ix["Bip01_%s_Clavicle" % n]])
        return r


def nick_knochen(W, b):
    """Welt-Neigung der Knochen-Y-Achse ueber der Waagerechten (+ = vorn hoch), wie plan/werkzeug/probe_suche.nick."""
    y = B_T @ W[b][:3, 1]
    return math.degrees(math.atan2(y[2], math.hypot(y[0], y[1])))


# ---------------------------------------------------------------- 2-Knochen-IK (Weltlagen, glTF)
def ik_zwei(W, G, oben, unten, fuss, ziel, pol, R_fuss_welt, inner_max=179.0):
    """Setzt die Weltdrehungen von oben/unten so, dass das Gelenk 'fuss' auf ziel liegt (Ellbogen/Knie zur Polrichtung pol);
    Weltdrehung von 'fuss' = R_fuss_welt. Gibt die neuen lokalen Drehungen (3x3) von oben, unten, fuss und den Innenwinkel zurueck.
    Die Verdrehung je Knochen bleibt wie im Grund (Rahmen aus Knochenrichtung und Beugeebene)."""
    io, iu, iff = G.idx[oben], G.idx[unten], G.idx[fuss]
    S, K0, A0 = W[io][:3, 3], W[iu][:3, 3], W[iff][:3, 3]
    a = np.linalg.norm(K0 - S)
    b = np.linalg.norm(A0 - K0)
    d = ziel - S
    ln = np.linalg.norm(d)
    fehl = 0.0
    lmax = min((a + b) * 0.9995, math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(inner_max))))
    lmin = abs(a - b) * 1.001 + 1e-6
    if ln > lmax:
        fehl = ln - lmax
        ln = lmax
    if ln < lmin:
        fehl = lmin - ln
        ln = lmin
    e = d / np.linalg.norm(d)
    along = (a * a - b * b + ln * ln) / (2.0 * ln)
    h = math.sqrt(max(a * a - along * along, 0.0))
    p = pol - e * float(pol @ e)
    p /= np.linalg.norm(p)
    K = S + e * along + p * h
    A = S + e * ln

    def rahmen(y1, y2):
        y1 = y1 / np.linalg.norm(y1)
        n = np.cross(y1, y2)
        nn = np.linalg.norm(n)
        n = n / nn if nn > 1e-9 else np.cross(y1, p) / np.linalg.norm(np.cross(y1, p))
        return np.stack((y1, n, np.cross(y1, n)), 1)
    F1b = rahmen(K0 - S, A0 - K0)
    F1n = rahmen(K - S, A - K)
    # Unterknochen: Rahmen (Richtung, gleiche Beugenormale wie oben)
    n_b = F1b[:, 1]
    n_n = F1n[:, 1]
    y2b = (A0 - K0) / b
    y2n = (A - K) / np.linalg.norm(A - K)
    F2b = np.stack((y2b, n_b, np.cross(y2b, n_b)), 1)
    F2n = np.stack((y2n, n_n, np.cross(y2n, n_n)), 1)
    Rup = F1n @ F1b.T @ W[io][:3, :3]
    Rlo = F2n @ F2b.T @ W[iu][:3, :3]
    Rpar = W[G.par[io]][:3, :3]
    inner = _winkel(S - K, A - K)
    Rup = orth(Rup)
    Rlo = orth(Rlo)
    return lok(Rpar, Rup), lok(Rup, Rlo), lok(Rlo, R_fuss_welt), inner, fehl


def lokal_setzen(L, b, R3):
    L[b][:3, :3] = R3


class Rechner:
    """Haelt Quelle, Junges, Netz und die Grund-Daten; rechnet die Sitz-Clips."""

    def __init__(self, quelle, junges, netz, gewichte=None, par=None):
        self.P = dict(PAR, **(par or {}))
        self.Q = Gerippe(quelle)
        self.G = Gerippe(junges)
        assert self.Q.names == self.G.names and self.Q.par == self.G.par, "Knochen Quelle != Junges"
        N = np.load(netz)
        self.N = N
        self.S = N["S"].astype(np.float64)                 # Form-Skalierung je Knochen (Dump-Achsen = glTF-Achsen bis aufs Vorzeichen)
        self.Pg = N["P"].astype(np.float64) * np.array((1.0, 1.0, -1.0))
        if gewichte:
            Gz = np.load(gewichte)
            Wt, Bi = Gz["Wt"].astype(np.float64), Gz["Bi"].astype(int)
        else:
            Wt, Bi = N["Wt"].astype(np.float64), N["Bi"].astype(int)
        Wt = np.where(Wt < 1e-6, 0.0, Wt)
        Wt /= Wt.sum(1, keepdims=True)
        self.Wt, self.Bi = Wt, Bi
        self.Tr = tier(self.Pg)
        self.M, self.dom = masken(self.G.names, self.Tr, Wt, Bi)
        # Haut-Ruhe muss stimmen (IBM des Jungen)
        r0 = haut(self.G.W0, self.G.ibm, self.Pg, Wt, Bi)
        assert np.abs(r0 - self.Pg).max() < 1e-4, np.abs(r0 - self.Pg).max()
        # Quelle: Netz und Zonen
        self.QP, self.QWt, self.QBi = netz_aus_glb(self.Q)
        self.QM, _ = masken(self.Q.names, tier(self.QP), self.QWt, self.QBi)
        self.mess = Messung(self.G)
        self.ix = self.G.idx
        # Pfoten-Geometrie relativ zum Gelenk (Ruhe, glTF): fuer Ballen und tiefsten Punkt
        self.bericht = {}

    # -------------------------------------------- Grund-Pose (Quell-Drehungen auf dem Jungen)
    def grund_lokal(self, tQ, qQ, sJ, tJ):
        """Lokale 4x4 des Grunds: Drehung Quelle, Lage Junges (Ruhe), Becken/Bip01/Translation_Data = Quelle x S_eltern."""
        nb = len(self.G.names)
        L = np.zeros((nb, 4, 4))
        R = q2m(qQ) * sJ[:, None, :]
        L[:, :3, :3] = R
        L[:, :3, 3] = tJ
        for nm in ("Bip01_Pelvis", "Bip01", "Translation_Data"):
            b = self.ix[nm]
            p = self.G.par[b]
            s = self.S[p] if p >= 0 else np.ones(3)
            L[b][:3, 3] = s * tQ[b]
        L[:, 3, 3] = 1.0
        return L

    def fk_L(self, L):
        W = np.zeros_like(L)
        for b, p in enumerate(self.G.par):
            W[b] = L[b] if p < 0 else W[p] @ L[b]
        return W

    def haut_t(self, W):
        return tier(haut(W, self.G.ibm, self.Pg, self.Wt, self.Bi))

    def quelle_haut_t(self, W):
        return tier(haut(W, self.Q.ibm, self.QP, self.QWt, self.QBi))

    # -------------------------------------------- Pfoten: Ballen und tiefster Punkt relativ zum Gelenk
    def pfote_rel(self, W, s, v):
        """tiefster Sohlenpunkt (Tier-z) relativ zum Gelenk Hand/Fuss im Bild W (Haut nur der Pfote)."""
        m = self.M[("hand_" if v == "V" else "fuss_") + s]
        Pw = tier(haut(W, self.G.ibm, self.Pg[m], self.Wt[m], self.Bi[m]))
        g = tier(W[self.ix["Bip01_%s_%s" % (s, "Hand" if v == "V" else "Foot")]][:3, 3])
        return Pw[:, 2].min() - g[2]

    # -------------------------------------------- ein Clip
    def clip(self, name, rear=False):
        P = self.P
        G, Q = self.G, self.Q
        T, _ = G.zeiten(name)
        TQ, _ = Q.zeiten(name)
        assert len(T) == len(TQ) and np.abs(T - TQ).max() < 1e-6, ("Zeiten Quelle != Junges", name)
        tQ, qQ, sQ = Q.werte(name, T)
        tJ, qJ, sJ = G.werte(name, T)            # heutiges Junges: Lagen (konstant), Skalier-Schluessel, Anschlussbilder
        n = len(T)
        ix = self.ix
        nb = len(G.names)
        # Quelle: Welt je Bild, Kontakte, Ballen, Neigungen
        WQ = np.array([Q.fk(tQ[f], qQ[f], sQ[f]) for f in range(n)])
        qk = []
        for f in range(n):
            Tq = self.quelle_haut_t(WQ[f])
            z0 = 0.0
            k = {}
            for s in "LR":
                k["V" + s] = Tq[self.QM["hand_" + s], 2].min() - z0
                k["H" + s] = Tq[self.QM["fuss_" + s], 2].min() - z0
                k["F" + s] = Tq[self.QM["ferse_" + s], 2].min() - z0
            k["sitz"] = Tq[self.QM["sitz"], 2].min() - z0
            k["boden"] = Tq[:, 2].min()
            k["brust"] = nick_knochen(WQ[f], ix["Bip01_Spine1"])
            k["becken_z"] = tier(WQ[f][ix["Bip01_Pelvis"]][:3, 3])[2]
            qk.append(k)
        # w(t): Brust-Neigung und Beckenhoehe der Quelle, normiert zwischen Stand (SitDown 0 / StandUp Ende) und Sitz (Sit 0)
        ref = self._quelle_ref()
        if name == "NCBear_Sit" or rear:
            w = np.ones(n) if not rear else np.zeros(n)
        else:
            u1 = np.array([(k["brust"] - ref["brust_stand"]) / (ref["brust_sitz"] - ref["brust_stand"]) for k in qk])
            u2 = np.array([(k["becken_z"] - ref["becken_stand"]) / (ref["becken_sitz"] - ref["becken_stand"]) for k in qk])
            w = np.clip(0.5 * (u1 + u2), 0, 1)
            g = int(P["w_glatt"])
            if g > 0:
                wp = np.r_[np.full(g, w[0]), w, np.full(g, w[-1])]
                w = np.convolve(wp, np.ones(2 * g + 1) / (2 * g + 1), mode="valid")
            if name == "NCBear_SitDown":
                w = np.maximum.accumulate(w)
                w = (w - w[0]) / max(w[-1] - w[0], 1e-9)
            else:
                w = np.minimum.accumulate(w)
                w = (w - w[-1]) / max(w[0] - w[-1], 1e-9)
            w = w * w * (3 - 2 * w)
        # Ziele der Pfoten: Start (heutiges Junges, festes Anschlussbild) und Sitz
        sitz = self.sitz_ziele()
        dz_sitz = self.sitz_hoehe()
        if name == "NCBear_SitDown":
            f_fest = 0
        elif name == "NCBear_StandUp":
            f_fest = n - 1
        else:
            f_fest = None
        if f_fest is not None:
            Lf = self._lokal_heute(tJ[f_fest], qJ[f_fest], sJ[f_fest])
            Wf = self.fk_L(Lf)
            start = {}
            for s in "LR":
                start["V" + s] = self.mess.bein(Wf, self.mess.delta(Wf), "V" + s)["ball"]
            qf = qk[f_fest]
            Wqf = WQ[f_fest]
            Tf = self.haut_t(Wf)
            z0f = Tf[:, 2].min()
            # Bezugshoehe des Beckens: im festen Bild = heute, im Sitz = Sitzflaeche auf dem Boden (Sit Bild 0), dazwischen mit w
            Lb = self.grund_lokal(tQ[f_fest], qQ[f_fest], sJ[f_fest], tJ[f_fest])
            dz_stand = float(tier(Wf[ix["Bip01_Pelvis"]][:3, 3])[2] - tier(self.fk_L(Lb)[ix["Bip01_Pelvis"]][:3, 3])[2] - z0f)
            for s in "LR":
                start["sV" + s] = float(Tf[self.M["hand_" + s], 2].min() - z0f)      # heute: Vorderpfoten im Stand ~4 cm ueber dem Boden
                start["sH" + s] = float(Tf[self.M["fuss_" + s], 2].min() - z0f)
        out_t = np.zeros((n, nb, 3))
        out_q = np.zeros((n, nb, 4))
        info = []
        ziele = []
        for f in range(n):
            L0 = self.grund_lokal(tQ[f], qQ[f], sJ[f], tJ[f])
            W0 = self.fk_L(L0)
            # Ziel Vorderpfoten (Ballen, Tier) aus dem Quellweg
            zV = {}
            zH = {}
            Dq = self.mess.delta(WQ[f])
            for s in "LR":
                bq = self._ball_quelle(WQ[f], s)
                if rear:
                    zV[s] = None
                elif name == "NCBear_Sit" or f_fest is None:
                    zV[s] = sitz["V" + s].copy()
                else:
                    bq0 = self._ball_quelle(Wqf, s)
                    bqs = sitz["Vq" + s]
                    b0 = start["V" + s]
                    bs = sitz["V" + s]
                    z_ = np.zeros(3)
                    for a in (0, 1):
                        den = bqs[a] - bq0[a]
                        if abs(den) > 0.01:
                            z_[a] = b0[a] + (bq[a] - bq0[a]) * (bs[a] - b0[a]) / den
                        else:
                            z_[a] = b0[a] + (bq[a] - bq0[a]) * P["schwung"] + (bs[a] - b0[a]) * w[f]
                    zV[s] = z_
                # Sohlenhoehe: Kontakt der Quelle -> Boden; Schwung -> Quelle x 0,74; dazu im Stand die Hoehe des festen Anschlussbilds
                # (heute schweben die Vorderpfoten im Stand ~4 cm, Gang byte-gleich), ausgeblendet mit w
                wv = min(1.0, w[f] / 0.35)
                wv = wv * wv * (3 - 2 * wv)
                aV = (1.0 - wv) * start["sV" + s] if f_fest is not None else 0.0
                aH = (1.0 - w[f]) * start["sH" + s] if f_fest is not None else 0.0
                hq = qk[f]["V" + s]
                zV[s + "_kontakt"] = bool(hq < P["kontakt"])
                zV[s + "_sohle"] = aV + (0.0 if hq < P["kontakt"] else hq * P["schwung"])
                hq = min(qk[f]["H" + s], qk[f]["F" + s])
                zH[s + "_kontakt"] = bool(hq < P["kontakt"])
                zH[s + "_sohle"] = aH + (0.0 if hq < P["kontakt"] else hq * P["schwung"])
            if f_fest is not None:
                dz_ref = dz_stand + (dz_sitz - dz_stand) * w[f]
            elif name == "NCBear_Sit":
                dz_ref = dz_sitz
            else:
                dz_ref = None
            ziele.append((L0, W0, zV, zH, dz_ref))
        # fix1 (Pruefer Technik T4): Pfoten-Zielweg in SitDown/StandUp ueber +-glatt_ziel Bilder glaetten (Lage und Sohlenhoehe), damit
        # kurze Schritte den Ellbogen nicht um 25-31 Grad je Bild knicken; Sit und Rear unveraendert. glatt_ziel 0 = wie vor fix1.
        g_ = int(P.get("glatt_ziel", 0))
        if g_ > 0 and f_fest is not None and not rear:
            roh_sohle = [{(d_, s + "_sohle"): z_[d_][s + "_sohle"] for d_ in (2, 3) for s in "LR" if s + "_sohle" in z_[d_]} for z_ in ziele]
            kern = np.array([g_ + 1 - abs(j) for j in range(-g_, g_ + 1)], float)
            kern /= kern.sum()

            def glatt(a):
                a = np.asarray(a, float)
                pad = np.concatenate([np.repeat(a[:1], g_, 0), a, np.repeat(a[-1:], g_, 0)], 0)
                return np.array([(kern[:, None] * pad[f_:f_ + 2 * g_ + 1].reshape(2 * g_ + 1, -1)).sum(0) for f_ in range(n)]).reshape(a.shape)
            for s in "LR":
                if ziele[0][2].get(s) is not None:
                    pv = glatt([z_[2][s] for z_ in ziele])
                    for f_, z_ in enumerate(ziele):
                        z_[2][s] = pv[f_]
                for d_, k_ in ((2, s + "_sohle"), (3, s + "_sohle")):
                    hv = glatt([z_[d_][k_] for z_ in ziele])
                    for f_, z_ in enumerate(ziele):
                        z_[d_][k_] = float(hv[f_])
            # Bodenkontakt bleibt: je Bild steht die tiefste der laut Quelle aufstehenden Pfoten wieder auf ihrer Hoehe vor dem Glaetten
            # (das Glaetten hebt sonst Kontaktbilder neben einem Schritt an und das Junge schwebt bis 0,9 cm)
            for f_, z_ in enumerate(ziele):
                kont = [(d_, s + "_sohle") for d_ in (2, 3) for s in "LR" if z_[d_].get(s + "_kontakt") and (d_ == 3 or z_[2].get(s) is not None)]
                if kont:
                    roh = roh_sohle[f_]
                    r_min = min(roh[k] for k in kont)
                    kont = [k for k in kont if roh[k] <= r_min + 1e-6]      # nur die wirklich tiefsten (Boden-)Kontakte
                    d_min = min(z_[d_][k_] - roh[(d_, k_)] for d_, k_ in kont)
                    if d_min > 0:
                        for d_ in (2, 3):
                            for s in "LR":
                                k_ = s + "_sohle"
                                if k_ in z_[d_]:
                                    z_[d_][k_] = max(roh[(d_, k_)], z_[d_][k_] - d_min)
        for f in range(n):
            L0, W0, zV, zH, dz_ref = ziele[f]
            r = self.pose(name, f, L0, W0, WQ[f], w[f], zV, zH, qk[f], rear, dz_ref)
            Lr, Wr, m = r
            m["w"] = float(w[f])
            info.append(m)
            for b in range(nb):
                out_t[f, b] = Lr[b][:3, 3]
                Rb = Lr[b][:3, :3] / sJ[f][b][None, :]
                out_q[f, b] = m2q(Rb)
        # feste Anschlussbilder + weicher Anschluss
        if f_fest is not None:
            k = int(P["anschluss"])
            for b in range(nb):
                tf, qf_ = tJ[f_fest][b], qJ[f_fest][b]
                for j in range(0, k + 1):
                    f = f_fest + j if f_fest == 0 else f_fest - j
                    u = j / (k + 1.0)
                    u = u * u * (3 - 2 * u)
                    qa = qf_ / np.linalg.norm(qf_)
                    qb = out_q[f, b] if float(out_q[f, b] @ qa) >= 0 else -out_q[f, b]
                    qm = qa * (1 - u) + qb * u
                    out_q[f, b] = qm / np.linalg.norm(qm)
                    out_t[f, b] = tf * (1 - u) + out_t[f, b] * u
            out_q[f_fest] = qJ[f_fest]
            out_t[f_fest] = tJ[f_fest]
        # Vorzeichen stetig
        for b in range(nb):
            if f_fest == n - 1:
                rng = range(n - 2, -1, -1)
                for f in rng:
                    if float(out_q[f, b] @ out_q[f + 1, b]) < 0:
                        out_q[f, b] = -out_q[f, b]
            else:
                for f in range(1, n):
                    if float(out_q[f, b] @ out_q[f - 1, b]) < 0:
                        out_q[f, b] = -out_q[f, b]
        # Messung an den fertigen Schluesseln (float32 wie im GLB), Fehlbetraege der IK aus der Rechnung dazu
        info2 = self.auswerten(out_t, out_q, sJ)
        for f in range(n):
            for k_ in ("VL_fehl", "VR_fehl", "HL_fehl", "HR_fehl", "iter", "sitzt_quelle", "zug_H", "kipp_H", "knie_H", "dz"):
                if k_ in info[f]:
                    info2[f][k_] = info[f][k_]
            info2[f]["w"] = float(w[f])
        return dict(T=T, t=out_t, q=out_q, w=w, info=info2, sJ=sJ)

    def auswerten(self, out_t, out_q, sJ):
        res = []
        for f in range(len(out_t)):
            t32 = out_t[f].astype(np.float32).astype(np.float64)
            q32 = out_q[f].astype(np.float32).astype(np.float64)
            W = self.G.fk(t32, q32, sJ[f])
            T_ = self.haut_t(W)
            res.append(self.kennzahlen(W, self.mess.delta(W), T_))
        return res

    def _lokal_heute(self, t, q, s):
        nb = len(self.G.names)
        L = np.zeros((nb, 4, 4))
        L[:, :3, :3] = q2m(q) * s[:, None, :]
        L[:, :3, 3] = t
        L[:, 3, 3] = 1.0
        return L

    def _ball_quelle(self, WQ, s):
        """Ballen der Quelle (Tier, Meter): Gelenk Hand + Drehung x (Ballen - Hand) in der Ruhe des grossen Baeren."""
        ix = self.ix
        b = ix["Bip01_%s_Hand" % s]
        sg = 1 if s == "L" else -1
        ball_a, gel_a = (np.array(x, float) for x in BALLEN["V"])
        off = (ball_a - gel_a) * np.array((1, sg, 1))
        D = B_T @ (WQ[b][:3, :3] @ self.Q.W0[b][:3, :3].T) @ B_T.T
        return tier(WQ[b][:3, 3]) + D @ off

    def _quelle_ref(self):
        if hasattr(self, "_qref"):
            return self._qref
        Q = self.Q
        ix = self.ix
        r = {}
        for nm, f, tag in (("NCBear_SitDown", 0, "stand"), ("NCBear_Sit", 0, "sitz")):
            T, _ = Q.zeiten(nm)
            t, q, s = Q.werte(nm, T)
            W = Q.fk(t[f], q[f], s[f])
            r["brust_" + tag] = nick_knochen(W, ix["Bip01_Spine1"])
            r["becken_" + tag] = tier(W[ix["Bip01_Pelvis"]][:3, 3])[2]
        self._qref = r
        return r

    def sitz_ziele(self):
        """Sitzlage der Vorderpfoten (Ballen, Tier) aus dem Sit-Bild 0 mit Vorbeugen: Handgelenk x = Schultergelenk x + v_dx (Unterarm
        fast senkrecht), Ballen |y| = v_y; Ballen = Handgelenk + Pfote (Weltdrehung der Quelle)."""
        if hasattr(self, "_sitz"):
            return self._sitz
        G, Q = self.G, self.Q
        nm = "NCBear_Sit"
        T, _ = G.zeiten(nm)
        tQ, qQ, sQ = Q.werte(nm, T)
        tJ, qJ, sJ = G.werte(nm, T)
        L0 = self.grund_lokal(tQ[0], qQ[0], sJ[0], tJ[0])
        W0 = self.fk_L(L0)
        L = self.vorbeugen(L0, 1.0)
        W = self.fk_L(L)
        WQ = Q.fk(tQ[0], qQ[0], sQ[0])
        z = {}
        for s in "LR":
            sg = 1 if s == "L" else -1
            sh = tier(W[self.ix["Bip01_%s_UpperArm" % s]][:3, 3])
            br = self._ball_rel(self._pfote_kipp(W0[self.ix["Bip01_%s_Hand" % s]][:3, :3], 1.0), s)
            z["V" + s] = np.array((sh[0] + self.P["v_dx"] + br[0], sg * self.P["v_y"], 0.0))
            z["Vq" + s] = self._ball_quelle(WQ, s)
        self._sitz = z
        return z

    def sitz_hoehe(self):
        """Beckenhoehe im Sitzen (Sit Bild 0, Sitzflaeche auf dem Boden) als Versatz gegen den Grund (Tier-z, Meter)."""
        if hasattr(self, "_dz_sitz"):
            return self._dz_sitz
        G, Q = self.G, self.Q
        nm = "NCBear_Sit"
        T, _ = G.zeiten(nm)
        tQ, qQ, sQ = Q.werte(nm, T)
        tJ, qJ, sJ = G.werte(nm, T)
        L0 = self.grund_lokal(tQ[0], qQ[0], sJ[0], tJ[0])
        W0 = self.fk_L(L0)
        sz = self.sitz_ziele()
        zV = {"L": sz["VL"].copy(), "R": sz["VR"].copy(), "L_sohle": 0.0, "R_sohle": 0.0, "L_kontakt": True, "R_kontakt": True}
        zH = {"L_sohle": 0.0, "R_sohle": 0.0, "L_kontakt": True, "R_kontakt": True}
        _, _, m = self.pose(nm, 0, L0, W0, Q.fk(tQ[0], qQ[0], sQ[0]), 1.0, zV, zH, {"sitz": 0.0}, False)
        self._dz_sitz = m["dz"]
        return self._dz_sitz

    # -------------------------------------------- Korrektur-Schicht
    def vorbeugen(self, L0, w):
        """Becken/Lende vorbeugen (Welt-Querachse), Hals nimmt es zurueck (bis Grenze), Kopf-Weltdrehung = Grund."""
        P = self.P
        ix = self.ix
        L = L0.copy()
        W0 = self.fk_L(L0)
        ip, isp, ich, ine, ihe = (ix[n] for n in ("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Neck", "Bip01_Head"))
        if w <= 0 and P["klav"] == 0:
            return L
        Rb = nick_dreh(w * P["dB"])
        Wp = W0[ip].copy()
        Rp_w = Rb @ Wp[:3, :3]
        L[ip][:3, :3] = lok(W0[self.G.par[ip]][:3, :3], Rp_w)
        W1 = self.fk_L(L)
        Rs_w = nick_dreh(w * P["dL"]) @ W1[isp][:3, :3]
        L[isp][:3, :3] = lok(W1[ip][:3, :3], Rs_w)
        if P.get("dC", 0.0) != 0.0:
            # fix1 (Nachbesserung M1): Brust zusaetzlich gegen die Lende (Welt-Querachse, + = Brust wieder auf) -> runder Ruecken
            W1c = self.fk_L(L)
            Rc_w = nick_dreh(w * P["dC"]) @ W1c[ich][:3, :3]
            L[ich][:3, :3] = lok(W1c[isp][:3, :3], Rc_w)
        # Hals gegen die Brust: Drehung der Quelle (gegen die Ruhe) nur zum Anteil 1 - w*(1 - hals_k) -- kuerzerer Nackenbogen, der Kopf
        # (Weltdrehung = Quelle) gleicht aus; der kurze Hals-Loft des Jungen dehnt sich sonst (Kopf rutscht gegen die Brust)
        if P["hals_k"] != 1.0 and w > 0:
            k_ = 1.0 - w * (1.0 - P["hals_k"])
            R0n = q2m(self.G.q0[ine])
            Dl = R0n.T @ L[ine][:3, :3]
            qd = m2q(Dl)
            ang = 2 * math.degrees(math.atan2(np.linalg.norm(qd[:3]), qd[3]))
            if ang > 1e-9:
                L[ine][:3, :3] = R0n @ achse_dreh(qd[:3], ang * k_)
        W2 = self.fk_L(L)
        # Hals: Weltdrehung zurueck Richtung Grund (Anteil 'hals'), dazu hals_extra; Grenze ne_ch nicken (-45, 50) mit Rand
        lean = w * (P["dB"] + P["dL"] + P.get("dC", 0.0))
        lo = GRENZEN_RUMPF_SITZ["ne_ch"][1][0] + P["rand"] + 1.0
        Rn_lean = W2[ine][:3, :3]
        best = None
        for a in np.linspace(0.0, 1.0, 41)[::-1]:
            ang = -lean * P["hals"] * a + w * P["hals_extra"] * a
            Rn = nick_dreh(ang) @ Rn_lean
            Lt = L.copy()
            Lt[ine][:3, :3] = lok(W2[ich][:3, :3], Rn)
            Wt_ = self.fk_L(Lt)
            Dn = self.mess.delta(Wt_)
            ne = ypr(Dn[ich].T @ Dn[ine])
            if ne[1] >= lo or a == 0.0:
                best = Rn
                break
        L[ine][:3, :3] = lok(W2[ich][:3, :3], best)
        W3 = self.fk_L(L)
        # Kopf: Weltdrehung = Grund (Quelle); Kiefer folgt lokal
        L[ihe][:3, :3] = lok(W3[ine][:3, :3], W0[ihe][:3, :3])
        # Schulterblatt zusaetzlich (kampf: euler(0, kp, kr) gegen die Brust; + nicken = Schulter tiefer)
        if P["klav"] != 0:
            for s in "LR":
                ic = ix["Bip01_%s_Clavicle" % s]
                W4 = self.fk_L(L)
                Rc = W4[ic][:3, :3]
                ax = W4[ich][:3, :3] @ (W0[ich][:3, :3].T @ np.array((1.0, 0, 0)))   # Brust-Querachse (glTF x in Ruhe)
                Rc2 = achse_dreh(QUER_G, -w * P["klav"]) @ Rc
                L[ic][:3, :3] = lok(W4[ich][:3, :3], Rc2)
        return L

    def pose(self, name, f, L0, W0, WQ, w, zV, zH, qk, rear, dz_ref=None):
        P = self.P
        ix = self.ix
        G = self.G
        L = self.vorbeugen(L0, w)
        # Startlage Becken: Grund mit Bodenausgleich (tiefster Hautpunkt 0), dann Iteration
        T0 = self.haut_t(W0)
        dz = -T0[:, 2].min() if dz_ref is None else float(dz_ref)
        ip = ix["Bip01_Pelvis"]
        Rbip = W0[G.par[ip]][:3, :3]
        t_pel0 = L[ip][:3, 3].copy()
        # Hinterbein-Ziel (Tier): Sprunggelenk wie im Grund (x, y), z aus dem Boden; Knie hoechstens knie_max gestreckt
        anke = {s: tier(W0[ix["Bip01_%s_Foot" % s]][:3, 3]) for s in "LR"}
        sitzt = qk["sitz"] < P["kontakt"]
        relV = {s: self._sohle_rel(self._pfote_kipp(W0[ix["Bip01_%s_Hand" % s]][:3, :3], w), s, "V") for s in "LR"}
        relH = {s: self._sohle_rel(W0[ix["Bip01_%s_Foot" % s]][:3, :3], s, "H") for s in "LR"}
        frei = ~(self.M["sitz"] | self.M["hand_L"] | self.M["hand_R"] | self.M["fuss_L"] | self.M["fuss_R"])
        m = {}
        zug = {}
        kipp = {"L": 0.0, "R": 0.0}                     # Hinterfuss kippen (Grad um die Beugeachse), nur gegen die Grenze dors
        knie = {"L": P["knie_max"], "R": P["knie_max"]}   # reicht das Kippen nicht: Knie in diesem Bild etwas mehr strecken
        lo_dors = GRENZEN["H"]["dors"][0] + P["rand"] + 0.2
        for it in range(60):
            L[ip][:3, 3] = t_pel0 + Rbip.T @ gltf(np.array((0.0, 0.0, dz)))
            W = self.fk_L(L)
            Lk = L.copy()
            for s in "LR":
                if zV.get(s) is None:
                    continue
                iH = ix["Bip01_%s_Hand" % s]
                Rh = self._pfote_kipp(W0[iH][:3, :3], w)     # Weltdrehung Pfote = Grund (Quelle), fix1: im Sitzen Zehen nach unten (v_kipp)
                z_ = zV[s] - self._ball_rel(Rh, s)           # Handgelenk (Tier) aus dem Ballen
                z_[2] = zV[s + "_sohle"] - relV[s]           # Hoehe aus der tiefsten Sohlenhaut
                ru, rl, rf, inner, fehl = ik_zwei(W, G, "Bip01_%s_UpperArm" % s, "Bip01_%s_Forearm" % s, "Bip01_%s_Hand" % s, gltf(z_),
                                                  self._pol(W0, "V", s, W), Rh, GRENZEN["V"]["inner"][1] - P["rand"] - 0.2)
                Lk[ix["Bip01_%s_UpperArm" % s]][:3, :3] = ru
                Lk[ix["Bip01_%s_Forearm" % s]][:3, :3] = rl
                Lk[iH][:3, :3] = rf
                m["V%s_fehl" % s] = fehl / M2U
            for s in "LR":
                iF = ix["Bip01_%s_Foot" % s]
                Rf = W0[iF][:3, :3]
                if kipp[s] != 0.0:
                    n_c = W[ix["Bip01_%s_Calf" % s]][:3, :3] @ G.W0[ix["Bip01_%s_Calf" % s]][:3, :3].T @ gltf(self.mess.ruhe["H" + s]["n0"])
                    Rf = achse_dreh(n_c, kipp[s]) @ Rf
                z_ = anke[s].copy()
                z_[1] += (1.0 if s == "L" else -1.0) * w * P["h_dy"]      # Hinterfuesse im Sitzen etwas weiter aussen (Luecke zur Vorderpfote)
                z_[2] = zH[s + "_sohle"] - relH[s]
                hip = tier(W[ix["Bip01_%s_Thigh" % s]][:3, 3])
                a_ = np.linalg.norm(W[ix["Bip01_%s_Calf" % s]][:3, 3] - W[ix["Bip01_%s_Thigh" % s]][:3, 3]) / M2U
                b_ = np.linalg.norm(W[iF][:3, 3] - W[ix["Bip01_%s_Calf" % s]][:3, 3]) / M2U
                dmax = math.sqrt(a_ * a_ + b_ * b_ - 2 * a_ * b_ * math.cos(math.radians(knie[s])))
                d_ = z_ - hip
                if np.linalg.norm(d_) > dmax:
                    rest = dmax * dmax - d_[1] ** 2 - d_[2] ** 2
                    if rest > 0:
                        zug[s] = float(z_[0] - (hip[0] + math.copysign(math.sqrt(rest), d_[0])))
                        z_[0] = hip[0] + math.copysign(math.sqrt(rest), d_[0])
                ru, rl, rf, inner, fehl = ik_zwei(W, G, "Bip01_%s_Thigh" % s, "Bip01_%s_Calf" % s, "Bip01_%s_Foot" % s, gltf(z_),
                                                  self._pol(W0, "H", s, W), Rf, GRENZEN["H"]["inner"][1] - P["rand"] - 0.2)
                Lk[ix["Bip01_%s_Thigh" % s]][:3, :3] = ru
                Lk[ix["Bip01_%s_Calf" % s]][:3, :3] = rl
                Lk[iF][:3, :3] = rf
                m["H%s_fehl" % s] = fehl / M2U
            Wk = self.fk_L(Lk)
            Dk = self.mess.delta(Wk)
            for s in "LR":
                dors = self.mess.bein(Wk, Dk, "H" + s)["dors"]
                if dors < lo_dors or kipp[s] != 0.0:
                    # Vorzeichen numerisch: wie aendert +1 Grad Kippen dors?
                    iF = ix["Bip01_%s_Foot" % s]
                    n_c = Wk[ix["Bip01_%s_Calf" % s]][:3, :3] @ G.W0[ix["Bip01_%s_Calf" % s]][:3, :3].T @ gltf(self.mess.ruhe["H" + s]["n0"])
                    Wt_ = Wk.copy()
                    Wt_[iF][:3, :3] = achse_dreh(n_c, 1.0) @ Wk[iF][:3, :3]
                    g_ = self.mess.bein(Wt_, self.mess.delta(Wt_), "H" + s)["dors"] - dors
                    if abs(g_) > 1e-6:
                        voll = abs(kipp[s]) >= P["fuss_kipp"] - 1e-9     # schon am Kipp-Anschlag (vorige Runde)
                        need = (lo_dors - dors) / g_
                        if dors < lo_dors:
                            neu = kipp[s] + need
                        else:                                   # zu weit gekippt: zurueck Richtung 0, nie darueber hinaus
                            neu = kipp[s] + need
                            if neu * kipp[s] < 0 or abs(neu) > abs(kipp[s]):
                                neu = 0.0 if neu * kipp[s] < 0 else kipp[s]
                        kipp[s] = float(np.clip(neu, -P["fuss_kipp"], P["fuss_kipp"]))
                        if voll and dors < lo_dors - 0.1 and abs(neu) > P["fuss_kipp"]:
                            knie[s] = min(knie[s] + min(lo_dors - dors, 4.0), 165.0)    # Knie strecken: Unterschenkel flacher, Fuss weniger gebeugt
            Tk = self.haut_t(Wk)
            # Sohlen-Abstand zum Gelenk aus der Haut (nicht aufsummiert)
            for s in "LR":
                if zV.get(s) is not None:
                    relV[s] = Tk[self.M["hand_" + s], 2].min() - tier(Wk[ix["Bip01_%s_Hand" % s]][:3, 3])[2]
                relH[s] = Tk[self.M["fuss_" + s], 2].min() - tier(Wk[ix["Bip01_%s_Foot" % s]][:3, 3])[2]
            m_all = Tk[:, 2].min()
            m_sitz = Tk[self.M["sitz"], 2].min()
            m_frei = Tk[frei, 2].min()
            if sitzt:
                delta = -m_sitz                              # Quelle sitzt auf: Sitzflaeche auf den Boden
                delta = max(delta, -m_frei)
            elif dz_ref is not None:
                # Hoehe folgt dem Bezugsweg. Steht eine Pfote laut Quelle auf, erreicht den Boden aber nicht (Arm/Bein am Anschlag):
                # Koerper senken, bis alle aufstehenden Pfoten den Boden beruehren (die anderen Beine beugen sich per IK); Sitzflaeche und
                # Rumpf nie in den Boden (dann anheben). Pfoten selbst liegen per IK auf ihrem Ziel.
                kont = [Tk[self.M["hand_" + s], 2].min() - zV[s + "_sohle"] for s in "LR" if zV.get(s) is not None and zV[s + "_kontakt"]]
                kont += [Tk[self.M["fuss_" + s], 2].min() - zH[s + "_sohle"] for s in "LR" if zH[s + "_kontakt"]]
                delta = -max(max(kont), 0.0) if kont else 0.0
                delta = max(delta, -m_sitz, -m_frei)
            else:
                delta = -m_all if m_all > 0 else 0.0
                delta = max(delta, -m_sitz, -m_frei)
            dz += delta
            L = Lk
            res = 0.0                                        # Sohlen-Rest gegen das Ziel (Haut), muss mit konvergieren (nur erreichbare Pfoten)
            for s in "LR":
                if zV.get(s) is not None and m.get("V%s_fehl" % s, 0.0) < 1e-6:
                    res = max(res, abs(Tk[self.M["hand_" + s], 2].min() - zV[s + "_sohle"]))
                if m.get("H%s_fehl" % s, 0.0) < 1e-6:
                    res = max(res, abs(Tk[self.M["fuss_" + s], 2].min() - zH[s + "_sohle"]))
            if self.P.get("debug"):
                print("  it %2d dz %.5f delta %+.6f res %.6f m_all %+.5f m_sitz %+.5f m_frei %+.5f kipp %s knie %s" % (
                    it, dz, delta, res, m_all, m_sitz, m_frei, {k_: round(v_, 3) for k_, v_ in kipp.items()}, {k_: round(v_, 2) for k_, v_ in knie.items()}))
            if abs(delta) < 1e-7 and it > 3 and res < 2e-5:
                break
        L[ip][:3, 3] = t_pel0 + Rbip.T @ gltf(np.array((0.0, 0.0, dz)))
        m["iter"] = it
        m["dz"] = float(dz)
        m["sitzt_quelle"] = bool(sitzt)
        m["zug_H"] = zug
        m["kipp_H"] = dict(kipp)
        m["knie_H"] = dict(knie)
        return L, None, m

    def _pfote_kipp(self, Rh, w):
        """fix1 (Nachbesserung M1): Vorderpfote im Sitzen um die Welt-Querachse nach vorn unten kippen (v_kipp Grad bei w = 1,
        + = Zehen runter). Das aufrechte Junge erreicht mit geraden kurzen Armen den Boden mit den Zehenballen statt der ganzen Sohle."""
        k = float(self.P.get("v_kipp", 0.0)) * float(w)
        if k == 0.0:
            return Rh
        return nick_dreh(-k) @ Rh

    def _ball_rel(self, Rh, s):
        """Ballen relativ zum Handgelenk (Tier) bei Weltdrehung Rh (glTF) der Pfote."""
        r = self.mess.ruhe["V" + s]
        D = B_T @ (Rh @ self.G.W0[self.ix["Bip01_%s_Hand" % s]][:3, :3].T) @ B_T.T
        return D @ (r["ball0"] - self.mess.Jt[r["fuss"]])

    def _sohle_rel(self, Rh, s, v, W0=None):
        """tiefster Pfotenpunkt relativ zum Gelenk (Tier-z) bei Weltdrehung Rh (starr: Punkte der Pfote mit dem Pfotenknochen)."""
        nm = "Bip01_%s_%s" % (s, "Hand" if v == "V" else "Foot")
        b = self.ix[nm]
        m = self.M[("hand_" if v == "V" else "fuss_") + s]
        D = Rh @ self.G.W0[b][:3, :3].T
        rel = (self.Pg[m] - self.G.W0[b][:3, 3]) @ D.T
        return tier(rel)[:, 2].min()

    def _pol(self, W0, v, s, W):
        """Polrichtung (glTF): Ellbogen/Knie im Grund relativ zur Linie Schulter/Huefte -> Hand/Fuss, mit dem Rumpf mitgedreht."""
        ix = self.ix
        o, u, ff = (("UpperArm", "Forearm", "Hand") if v == "V" else ("Thigh", "Calf", "Foot"))
        S0, K0, A0 = (W0[ix["Bip01_%s_%s" % (s, k)]][:3, 3] for k in (o, u, ff))
        e = (A0 - S0) / np.linalg.norm(A0 - S0)
        p = (K0 - S0) - e * float((K0 - S0) @ e)
        par = self.G.par[ix["Bip01_%s_%s" % (s, o)]]
        R = W[par][:3, :3] @ W0[par][:3, :3].T
        return R @ p

    def kennzahlen(self, W, D, T_):
        M = self.M
        ix = self.ix
        k = {}
        z0 = T_[:, 2].min()
        k["boden_cm"] = 100 * z0
        for s in "LR":
            k["vpfote_%s_cm" % s] = 100 * (T_[M["hand_" + s], 2].min() - z0)
            k["ferse_%s_cm" % s] = 100 * (T_[M["ferse_" + s], 2].min() - z0)
            k["hfuss_%s_cm" % s] = 100 * (T_[M["fuss_" + s], 2].min() - z0)
        k["sitz_cm"] = 100 * (T_[M["sitz"], 2].min() - z0)
        fL = T_[M["fuss_L"]].mean(0)
        fR = T_[M["fuss_R"]].mean(0)
        k["fussabstand_cm"] = 100 * abs(fL[1] - fR[1])
        k["kopf_oben_m"] = float(T_[:, 2].max() - z0)
        k["kopf_ist_oben"] = bool(T_[M["kopf"], 2].max() >= T_[~M["kopf"], 2].max())
        k["kopf_minus_rest_cm"] = 100 * float(T_[M["kopf"], 2].max() - T_[~M["kopf"], 2].max())
        for nm, tag in (("Bip01_Pelvis", "becken"), ("Bip01_Spine", "lende"), ("Bip01_Spine1", "brust"), ("Bip01_Neck", "hals"), ("Bip01_Head", "kopf")):
            k["nick_" + tag] = nick_knochen(W, ix[nm])
        LM = LANDMARKE_KOPF
        d = D[ix["Bip01_Head"]] @ LM
        k["blick"] = math.degrees(math.atan2(d[2], math.hypot(d[0], d[1])))
        k["bein"] = {}
        for key in ("VL", "VR", "HL", "HR"):
            b = self.mess.bein(W, D, key)
            k["bein"][key] = {kk: (float(vv) if not isinstance(vv, np.ndarray) else [float(x) for x in vv]) for kk, vv in b.items()}
        k["rumpf"] = self.mess.rumpf(D)
        k["schulter_z"] = float(tier(W[ix["Bip01_L_UpperArm"]][:3, 3])[2] - z0)
        k["becken_t"] = [float(x) for x in tier(W[ix["Bip01_Pelvis"]][:3, 3])]
        return k


# Kopf-Rahmen x (Ruhe, Tier) aus _arbeit/baer_baby/landmarken.json "kopfachse_x_y_z"[0] (Blick, Ruhe -14,7 Grad)
LANDMARKE_KOPF = np.array([0.9670745526730832, 4.193595284130907e-15, -0.2544932172285179])


def grenzen_pruefen(info, sitz=True):
    """Zaehlt Bilder ausserhalb der Gelenkgrenzen (baer_kampf_2c GRENZEN, GRENZEN_RUMPF(_SITZ), GRENZE_KLAV) und Spruenge je Bild."""
    aus = {}
    GR = GRENZEN_RUMPF_SITZ if sitz else GRENZEN_RUMPF
    spannen = {}
    for f, m in enumerate(info):
        for key, b in m["bein"].items():
            G = GRENZEN[key[0]]
            for g, (lo, hi) in G.items():
                v = b[g]
                spannen.setdefault("%s_%s" % (key, g), [1e9, -1e9])
                spannen["%s_%s" % (key, g)] = [min(spannen["%s_%s" % (key, g)][0], v), max(spannen["%s_%s" % (key, g)][1], v)]
                if not (lo - 0.01 <= v <= hi + 0.01):
                    aus.setdefault("%s_%s" % (key, g), []).append(f)
        for g, gr in GR.items():
            for a, nm in enumerate(("gier", "nick", "roll")):
                v = m["rumpf"][g][a]
                kk = "%s_%s" % (g, nm)
                spannen.setdefault(kk, [1e9, -1e9])
                spannen[kk] = [min(spannen[kk][0], v), max(spannen[kk][1], v)]
                if not (gr[a][0] - 0.01 <= v <= gr[a][1] + 0.01):
                    aus.setdefault(kk, []).append(f)
        for s in "LR":
            y, p, r = m["rumpf"]["klav_" + s]
            kk = "klav_" + s
            spannen.setdefault(kk + "_nick", [1e9, -1e9])
            spannen[kk + "_nick"] = [min(spannen[kk + "_nick"][0], p), max(spannen[kk + "_nick"][1], p)]
            if not (GRENZE_KLAV[0][0] - 0.01 <= p <= GRENZE_KLAV[0][1] + 0.01) or not (GRENZE_KLAV[1][0] - 0.01 <= r <= GRENZE_KLAV[1][1] + 0.01):
                aus.setdefault(kk, []).append(f)
    spr = {}
    for f in range(1, len(info)):
        a, b = info[f - 1], info[f]
        for key in ("VL", "VR", "HL", "HR"):
            for g in ("sup", "tw", "dors", "inner"):
                d = abs(b["bein"][key][g] - a["bein"][key][g])
                spr["%s_%s" % (key, g)] = max(spr.get("%s_%s" % (key, g), 0.0), d)
        d = 100 * np.linalg.norm(np.array(b["becken_t"]) - np.array(a["becken_t"]))
        spr["becken_cm"] = max(spr.get("becken_cm", 0.0), float(d))
    sprung_aus = {k: v for k, v in spr.items() if (k.endswith("_sup") and v > SPRUNG["sup"]) or (k.endswith("_tw") and v > SPRUNG["tw"])
                  or (k.endswith("_dors") and v > SPRUNG["dors"]) or (k.endswith("_inner") and v > SPRUNG["inner"]) or (k == "becken_cm" and v > 3.0)}
    return dict(aus={k: [len(v), v[:6]] for k, v in aus.items()}, spannen={k: [round(a, 1), round(b, 1)] for k, (a, b) in spannen.items()},
                sprung={k: round(v, 2) for k, v in spr.items()}, sprung_aus=sprung_aus)


def zusammenfassung(name, r):
    I = r["info"]

    def sp(k, sub=None):
        vs = [m[k] if sub is None else m[k][sub] for m in I]
        return [round(float(min(vs)), 2), round(float(max(vs)), 2)]
    z = dict(bilder=len(I), w=[round(float(x), 3) for x in r["w"][::6]])
    for k in ("boden_cm", "vpfote_L_cm", "vpfote_R_cm", "ferse_L_cm", "ferse_R_cm", "hfuss_L_cm", "hfuss_R_cm", "sitz_cm", "fussabstand_cm",
              "kopf_oben_m", "kopf_minus_rest_cm", "nick_becken", "nick_lende", "nick_brust", "nick_hals", "nick_kopf", "blick", "schulter_z",
              "VL_fehl", "VR_fehl", "HL_fehl", "HR_fehl"):
        if k in I[0]:
            z[k] = sp(k)
    for key in ("VL", "VR", "HL", "HR"):
        z[key + "_inner"] = [round(min(m["bein"][key]["inner"] for m in I), 1), round(max(m["bein"][key]["inner"] for m in I), 1)]
        z[key + "_ball"] = [[round(v, 3) for v in I[0]["bein"][key]["ball"]], [round(v, 3) for v in I[-1]["bein"][key]["ball"]]]
    z["grenzen"] = grenzen_pruefen(I)
    return z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quelle", default=QUELLE_STD)
    ap.add_argument("--junges", default=JUNGES_STD)
    ap.add_argument("--netz", default=NETZ_STD)
    ap.add_argument("--gewichte", default=None)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--bericht", default=None)
    ap.add_argument("--clips", default=",".join(SITZ))
    ap.add_argument("--rear", action="store_true")
    ap.add_argument("--par", default=None, help="JSON mit Parametern (ueberschreibt PAR)")
    a = ap.parse_args()
    par = json.loads(open(a.par).read()) if a.par and a.par.endswith(".json") else (json.loads(a.par) if a.par else None)
    R = Rechner(a.quelle, a.junges, a.netz, a.gewichte, par)
    clips = [c for c in a.clips.split(",") if c]
    if a.rear and "NCBear_Rear" not in clips:
        clips.append("NCBear_Rear")
    aus = {}
    ber = dict(quelle=a.quelle, junges=a.junges, netz=a.netz, gewichte=a.gewichte, par=R.P, clips={})
    for c in clips:
        r = R.clip(c, rear=(c == "NCBear_Rear"))
        aus[c + "__T"] = r["T"]
        aus[c + "__t"] = r["t"]
        aus[c + "__q"] = r["q"]
        aus[c + "__w"] = r["w"]
        ber["clips"][c] = zusammenfassung(c, r)
        print("SITZ", c, json.dumps({k: v for k, v in ber["clips"][c].items() if k not in ("grenzen",)}), flush=True)
        print("SITZ", c, "Grenzen aus:", ber["clips"][c]["grenzen"]["aus"], "Spruenge aus:", ber["clips"][c]["grenzen"]["sprung_aus"], flush=True)
    np.savez(a.aus, names=np.array(R.G.names), **aus)
    if a.bericht:
        json.dump(ber, open(a.bericht, "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
