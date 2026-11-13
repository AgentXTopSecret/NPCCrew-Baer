# -*- coding: utf-8 -*-
# Lauf baer-liegen (13.11.2026), Rolle PLAN: gemeinsamer numpy-Kern fuer "Baer liegt tot" (Clips DeerStag_Death / DeerStag_Dead).
# NEU (kein Original geaendert). Reines Python/numpy, kein Blender. Beide Bauer (GROSS, JUNGE) IMPORTIEREN diese Datei und aendern sie
# NICHT (getrennte Dateien); braucht ein Bauer eine Abweichung, ueberschreibt er die Funktion in SEINER Datei und meldet es im Bericht.
#   Rig        GLB lesen (Knoten, Ruhe, Skin, Netz), Clips abtasten, FK, Haut (wie glTF; gegen den Importer-Dump geprueft)
#   Loeser     Liegepose aus Zielen (Sprache wie LIEGE in baer_kampf_gross.py: Becken-Lage, Weltdrehungen yaw/pitch/roll gegen die Ruhe,
#              je Bein Gelenk-Ziel + Pfoten-Weltdrehung + Pol; Zwei-Knochen-IK wie bein()) -> lokale Drehungen je Knoten
#   sturz      Death neu = heutige Death-Spur, im Gelenkraum weich auf die neue Endpose ueberblendet (Bild 0 bleibt, letztes Bild = Dead);
#              boden_je_bild haelt den Sturz am Boden (nichts tiefer als 1,2 cm, kein Schweben)
#   aufloesen  relative Ziel-Tabelle (POSE.md: s, vor, boden/senk, Pfote beuge) -> absolute Ziele mit Boden-Regeln fuer Rumpf, Beine, Kopf
#   baue       EIN Schritt: Tabelle + Gerippe-GLB -> GLB mit neuem Death/Dead + Kurz-Messung (auch als Befehl, siehe unten)
#   schreibe   GLB neu packen: NUR die Kanaele von Death/Dead bekommen neue Accessoren; alle anderen Accessoren byte-gleich kopiert;
#              Selbstpruefung (13 andere Clips, Knoten, Skin, inverse Bind, Netz-Puffer byte-gleich; Zeiten/Dauer von Death/Dead gleich)
# Rahmen "tier": Meter, x vorn, y links, z oben, Boden z 0.  glTF (x, y, z) = tier (y, z, x) * 0,544  (wie baer_export_gengross.py).
# Statisch/offline gerechnet, nicht gespielt. Schreibt nur die Datei, die der Aufrufer nennt.
import hashlib
import json
import math
import struct

import numpy as np

M2U = 0.544
CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8, 5120: np.int8, 5122: np.int16}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
CLIPS_LIEGEN = ("DeerStag_Death", "DeerStag_Dead")
C_GT = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])     # tier = C_GT @ glTF / M2U


# ------------------------------------------------------------------ GLB lesen
def lade_glb(pfad):
    b = open(pfad, "rb").read()
    assert b[:4] == b"glTF", pfad
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


def acc_arr(J, B, i):
    a = J["accessors"][i]
    return np.frombuffer(acc_bytes(J, B, i), dtype=CT[a["componentType"]]).reshape(a["count"], NC[a["type"]])


# ------------------------------------------------------------------ Drehungen (Matrizen 3x3; Quaternion x, y, z, w wie glTF)
def rx(g):
    c, s = math.cos(math.radians(g)), math.sin(math.radians(g))
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float)


def ry(g):  # +g: Nase bzw. Zehe nach unten
    c, s = math.cos(math.radians(g)), math.sin(math.radians(g))
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float)


def rz(g):  # +g: Nase nach links
    c, s = math.cos(math.radians(g)), math.sin(math.radians(g))
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def euler(yaw=0.0, pitch=0.0, roll=0.0):
    """wie baer_kampf_gross.euler: rz(yaw) @ ry(pitch) @ rx(roll), Achsen des Tier-Rahmens."""
    return rz(yaw) @ ry(pitch) @ rx(roll)


def euler_von(R):
    """Umkehrung von euler(): (yaw, pitch, roll) in Grad."""
    pitch = -math.degrees(math.asin(max(-1.0, min(1.0, R[2, 0]))))
    yaw = math.degrees(math.atan2(R[1, 0], R[0, 0]))
    roll = math.degrees(math.atan2(R[2, 1], R[2, 2]))
    return yaw, pitch, roll


def q_mat(q):
    x, y, z, w = (float(v) for v in q)
    n = math.sqrt(x * x + y * y + z * z + w * w)
    x, y, z, w = x / n, y / n, z / n, w / n
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def mat_q(R):
    m = R
    tr = m[0, 0] + m[1, 1] + m[2, 2]
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2
        q = ((m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s, (m[1, 0] - m[0, 1]) / s, 0.25 * s)
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        q = (0.25 * s, (m[0, 1] + m[1, 0]) / s, (m[0, 2] + m[2, 0]) / s, (m[2, 1] - m[1, 2]) / s)
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        q = ((m[0, 1] + m[1, 0]) / s, 0.25 * s, (m[1, 2] + m[2, 1]) / s, (m[0, 2] - m[2, 0]) / s)
    else:
        s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        q = ((m[0, 2] + m[2, 0]) / s, (m[1, 2] + m[2, 1]) / s, 0.25 * s, (m[1, 0] - m[0, 1]) / s)
    q = np.array(q, dtype=float)
    return q / np.linalg.norm(q)


def q_slerp(a, b, t):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = float(a @ b)
    if d < 0:
        b, d = -b, -d
    if d > 0.9995:
        q = a + t * (b - a)
    else:
        w = math.acos(d)
        q = (math.sin((1 - t) * w) * a + math.sin(t * w) * b) / math.sin(w)
    return q / np.linalg.norm(q)


def winkel(Ra, Rb):
    """Drehwinkel zwischen zwei Drehungen in Grad."""
    c = (np.trace(Ra.T @ Rb) - 1.0) / 2.0
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def g2t(P):
    P = np.asarray(P, float)
    return P[..., [2, 0, 1]] / M2U


def t2g(P):
    P = np.asarray(P, float)
    return P[..., [1, 2, 0]] * M2U


def ssf(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


def _rein(M):
    """Drehanteil einer 3x3 ohne Skalierung."""
    return M / np.linalg.norm(M, axis=0)[None, :]


# ------------------------------------------------------------------ Rig: GLB als Skelett + Netz
class Rig:
    def __init__(self, pfad):
        self.pfad = pfad
        self.J, self.B = lade_glb(pfad)
        nodes = self.J["nodes"]
        self.nn = len(nodes)
        self.name = [n.get("name", "?") for n in nodes]
        self.ix = {n: i for i, n in enumerate(self.name)}
        self.par = [-1] * self.nn
        for i, n in enumerate(nodes):
            for c in n.get("children", []):
                self.par[c] = i
        self.ord = []
        while len(self.ord) < self.nn:
            for i in range(self.nn):
                if i not in self.ord and (self.par[i] < 0 or self.par[i] in self.ord):
                    self.ord.append(i)
        self.t0 = np.array([n.get("translation", (0, 0, 0)) for n in nodes], dtype=float)
        self.q0 = np.array([n.get("rotation", (0, 0, 0, 1)) for n in nodes], dtype=float)
        self.s0 = np.array([n.get("scale", (1, 1, 1)) for n in nodes], dtype=float)
        sk = self.J["skins"][0]
        self.joints = list(sk["joints"])
        self.jname = [self.name[k] for k in self.joints]
        self.ibm = acc_arr(self.J, self.B, sk["inverseBindMatrices"]).astype(float).reshape(-1, 4, 4).transpose(0, 2, 1)
        pr = self.J["meshes"][0]["primitives"][0]
        self.P = acc_arr(self.J, self.B, pr["attributes"]["POSITION"]).astype(float)
        self.JN = acc_arr(self.J, self.B, pr["attributes"]["JOINTS_0"]).astype(int)
        self.WT = acc_arr(self.J, self.B, pr["attributes"]["WEIGHTS_0"]).astype(float)
        self.F = acc_arr(self.J, self.B, pr["indices"]).astype(int).reshape(-1, 3)
        self.W0 = self.welt(self.t0, self.q0)

    def welt(self, t, q, s=None):
        """FK im glTF-Raum: lokale Lage/Drehung je Knoten -> Weltmatrizen (Skalierung = Ruhe, wenn s fehlt)."""
        s = self.s0 if s is None else s
        W = np.zeros((self.nn, 4, 4))
        for i in self.ord:
            L = np.eye(4)
            L[:3, :3] = q_mat(q[i]) * s[i][None, :]
            L[:3, 3] = t[i]
            W[i] = L if self.par[i] < 0 else W[self.par[i]] @ L
        return W

    def haut(self, W):
        """Hautpunkte im glTF-Raum fuer Weltmatrizen W (Summe Gewicht x Welt x inverseBind)."""
        S = np.einsum("jab,jbc->jac", W[self.joints], self.ibm)
        Ph = np.c_[self.P, np.ones(len(self.P))]
        out = np.zeros((len(self.P), 3))
        for k in range(4):
            out += self.WT[:, k:k + 1] * np.einsum("nab,nb->na", S[self.JN[:, k]], Ph)[:, :3]
        return out

    def haut_tier(self, W):
        return g2t(self.haut(W))

    def gewichte(self):
        """n x Knoten Gewichtsmatrix (Spalte = Knoten-Index)."""
        G = np.zeros((len(self.P), self.nn))
        jn = np.array(self.joints)
        for k in range(4):
            np.add.at(G, (np.arange(len(self.P)), jn[self.JN[:, k]]), self.WT[:, k])
        return G

    def anim(self, name):
        for a in self.J["animations"]:
            if a.get("name") == name:
                return a
        raise KeyError(name)

    def clip(self, name):
        """Tastet einen Clip an seinen dichten Zeiten ab: T (n), t (n, nn, 3), q (n, nn, 4), s (n, nn, 3); ia = Accessor der dichten Zeiten."""
        an = self.anim(name)
        best, ia = None, None
        for smp in an["samplers"]:
            T = acc_arr(self.J, self.B, smp["input"])[:, 0]
            if best is None or len(T) > len(best):
                best, ia = T, smp["input"]
        T = best.astype(np.float32)
        n = len(T)
        t = np.repeat(self.t0[None], n, 0)
        q = np.repeat(self.q0[None], n, 0)
        s = np.repeat(self.s0[None], n, 0)
        for ch in an["channels"]:
            smp = an["samplers"][ch["sampler"]]
            ti = acc_arr(self.J, self.B, smp["input"])[:, 0]
            v = acc_arr(self.J, self.B, smp["output"]).astype(float)
            node, path = ch["target"]["node"], ch["target"]["path"]
            if len(ti) == n and np.array_equal(ti, T):
                w = v
            else:
                w = np.zeros((n, v.shape[1]))
                for f in range(n):
                    k = int(np.searchsorted(ti, T[f] + 1e-6) - 1)
                    k = max(0, min(len(ti) - 1, k))
                    if smp.get("interpolation", "LINEAR") == "STEP" or k == len(ti) - 1:
                        w[f] = v[k]
                    else:
                        u = (T[f] - ti[k]) / (ti[k + 1] - ti[k])
                        w[f] = q_slerp(v[k], v[k + 1], u) if path == "rotation" else (1 - u) * v[k] + u * v[k + 1]
            if path == "translation":
                t[:, node] = w
            elif path == "rotation":
                q[:, node] = w
            else:
                s[:, node] = w
        return dict(T=T, t=t, q=q, s=s, ia=ia)


# ------------------------------------------------------------------ Loeser: Liegepose aus Zielen
BEINE = (("VL", "L", "UpperArm", "Forearm", "Hand"), ("VR", "R", "UpperArm", "Forearm", "Hand"),
         ("HL", "L", "Thigh", "Calf", "Foot"), ("HR", "R", "Thigh", "Calf", "Foot"))
RUMPF = (("q_pel", "Bip01_Pelvis"), ("q_sp", "Bip01_Spine"), ("q_ch", "Bip01_Spine1"), ("q_ne", "Bip01_Neck"), ("q_he", "Bip01_Head"),
         ("q_ta", "Bip01_Tail"))


def _E(v):
    v = np.asarray(v, float)
    return v if v.shape == (3, 3) else euler(*v)


class Loeser:
    """Sprache wie baer_kampf_gross.py: je Knochen eine WELT-Drehung gegen die Ruhe (Q) und die Lage des Knochenkopfs (tier-Meter).
    Ziel-Tabelle Z (POSE.md): pel (x, y, z), q_pel/q_sp/q_ch/q_ne/q_he/q_ta = (yaw, pitch, roll) Grad, klav {L, R} Grad, kiefer Grad,
    bein {VL, VR, HL, HR}: ziel = Hand-/Sprunggelenk (x, y, z), q = Weltdrehung der Pfote (yaw, pitch, roll), pole = Richtung von
    Ellbogen/Knie (x, y, z), hinten wahlweise zehe (Grad gegen den Fuss)."""

    def __init__(self, rig):
        self.rig = rig
        R = rig
        self.Jp = {n: g2t(R.W0[i][:3, 3]) for i, n in enumerate(R.name)}
        self.R0 = {n: C_GT @ _rein(R.W0[i][:3, :3]) @ C_GT.T for i, n in enumerate(R.name)}
        self.eltern = {n: (R.name[R.par[i]] if R.par[i] >= 0 else None) for i, n in enumerate(R.name)}
        self.LEG = {}
        for key, sn, a_, b_, c_ in BEINE:
            oben, unten, fuss = "Bip01_%s_%s" % (sn, a_), "Bip01_%s_%s" % (sn, b_), "Bip01_%s_%s" % (sn, c_)
            ja, jb, jc = self.Jp[oben], self.Jp[unten], self.Jp[fuss]
            y_r = (jb - ja) / np.linalg.norm(jb - ja)
            y2_r = (jc - jb) / np.linalg.norm(jc - jb)
            n_r = np.cross(y_r, y2_r)
            n_r /= np.linalg.norm(n_r)
            self.LEG[key] = dict(oben=oben, unten=unten, fuss=fuss, s=1 if sn == "L" else -1, vorn=key[0] == "V",
                                 a=float(np.linalg.norm(jb - ja)), b=float(np.linalg.norm(jc - jb)),
                                 F1=np.stack((y_r, n_r, np.cross(y_r, n_r)), 1), F2=np.stack((y2_r, n_r, np.cross(y2_r, n_r)), 1),
                                 knick0=math.degrees(math.acos(max(-1, min(1, float(y_r @ y2_r))))))

    def _kette(self, pose, name, Q):
        par = self.eltern[name]
        Qp, pp = pose[par]
        pose[name] = (Q, pp + Qp @ (self.Jp[name] - self.Jp[par]))

    def _bein(self, pose, key, ank, Qf, pole, stat):
        """Zwei-Knochen-IK wie bein() in baer_kampf_gross.py:224 (gleiche Formeln, numpy)."""
        L = self.LEG[key]
        par = self.eltern[L["oben"]]
        Qp, pp = pose[par]
        hip = pp + Qp @ (self.Jp[L["oben"]] - self.Jp[par])
        a, b = L["a"], L["b"]
        d = ank - hip
        ln = float(np.linalg.norm(d))
        maxd = (a + b) * 0.998
        stat.setdefault("streckung", {})[key] = round(ln / (a + b), 4)
        if ln > maxd:
            stat.setdefault("ueber", {})[key] = round(ln - maxd, 4)
            ln = maxd
        e = d / np.linalg.norm(d)
        along = (a * a - b * b + ln * ln) / (2.0 * ln)
        h = math.sqrt(max(a * a - along * along, 0.0))
        p = pole - e * float(pole @ e)
        p /= np.linalg.norm(p)
        K = hip + e * along + p * h
        A = hip + e * ln
        y1 = (K - hip) / np.linalg.norm(K - hip)
        y2 = (A - K) / np.linalg.norm(A - K)
        n = np.cross(y1, y2)
        if np.linalg.norm(n) < 1e-6:
            n = np.cross(p, e)
        n /= np.linalg.norm(n)
        F1 = np.stack((y1, n, np.cross(y1, n)), 1)
        F2 = np.stack((y2, n, np.cross(y2, n)), 1)
        stat.setdefault("knick", {})[key] = round(math.degrees(math.acos(max(-1, min(1, float(y1 @ y2))))) - L["knick0"], 2)
        pose[L["oben"]] = (F1 @ L["F1"].T, hip)
        pose[L["unten"]] = (F2 @ L["F2"].T, K)
        pose[L["fuss"]] = (Qf, A)

    def welt_pose(self, Z, stat=None):
        """Z -> pose[name] = (Q Weltdrehung gegen Ruhe 3x3, Kopf-Lage tier)."""
        stat = {} if stat is None else stat
        pose = {"Dummy01": (np.eye(3), self.Jp["Dummy01"].copy()), "Bip01": (np.eye(3), self.Jp["Bip01"].copy())}
        pose["Bip01_Pelvis"] = (_E(Z["q_pel"]), np.array(Z["pel"], float))
        self._kette(pose, "Bip01_Spine", _E(Z["q_sp"]))
        self._kette(pose, "Bip01_Spine1", _E(Z["q_ch"]))
        self._kette(pose, "Bip01_Neck", _E(Z["q_ne"]))
        self._kette(pose, "Bip01_Head", _E(Z["q_he"]))
        self._kette(pose, "Bip01_Jaw", pose["Bip01_Head"][0] @ ry(Z.get("kiefer", 0.0)))
        self._kette(pose, "Bip01_Tail", _E(Z["q_ta"]))
        for sn in "LR":
            self._kette(pose, "Bip01_%s_Clavicle" % sn, pose["Bip01_Spine1"][0] @ ry(Z["klav"][sn]))
        for key, sn, a_, b_, c_ in BEINE:
            bz = Z["bein"][key]
            self._bein(pose, key, np.array(bz["ziel"], float), _E(bz["q"]), np.array(bz["pole"], float), stat)
            if a_ == "Thigh":
                self._kette(pose, "Bip01_%s_Toe0" % sn, pose["Bip01_%s_Foot" % sn][0] @ ry(bz.get("zehe", 0.0)))
        return pose

    def lokal(self, pose):
        """pose -> lokale Lage/Drehung je Knoten im glTF-Raum (t nn x 3, q nn x 4). Nicht genannte Knoten bleiben in Ruhe."""
        R = self.rig
        t, q = R.t0.copy(), R.q0.copy()
        Rw = {}
        for i in R.ord:
            n = R.name[i]
            Rp = Rw[R.par[i]] if R.par[i] >= 0 else np.eye(3)
            if n in pose:
                Rw[i] = (C_GT.T @ pose[n][0] @ C_GT) @ _rein(R.W0[i][:3, :3])
                q[i] = mat_q(Rp.T @ Rw[i])
            else:
                Rw[i] = Rp @ q_mat(R.q0[i])
        ip = R.ix["Bip01_Pelvis"]
        Wp = R.welt(t, q)[R.par[ip]]
        t[ip] = (np.linalg.inv(Wp) @ np.r_[t2g(pose["Bip01_Pelvis"][1]), 1.0])[:3]
        return t, q

    def loese(self, Z, stat=None):
        return self.lokal(self.welt_pose(Z, stat))

    def lesen(self, t, q):
        """Umkehrung fuer die Analyse: lokale Pose -> pose[name] = (Q, Lage tier) fuer alle Knoten."""
        R = self.rig
        W = R.welt(t, q)
        return {n: ((C_GT @ _rein(W[i][:3, :3]) @ C_GT.T) @ self.R0[n].T, g2t(W[i][:3, 3])) for i, n in enumerate(R.name)}

    def ziele_von(self, t, q):
        """Liest aus einer lokalen Pose die Ziel-Sprache zurueck (fuer Tabellen und als Startwert): dict wie Z."""
        p = self.lesen(t, q)
        Z = dict(pel=[round(float(v), 4) for v in p["Bip01_Pelvis"][1]])
        for k, n in RUMPF:
            Z[k] = [round(v, 2) for v in euler_von(p[n][0])]
        Z["klav"] = {sn: round(euler_von(p["Bip01_Spine1"][0].T @ p["Bip01_%s_Clavicle" % sn][0])[1], 2) for sn in "LR"}
        Z["kiefer"] = round(euler_von(p["Bip01_Head"][0].T @ p["Bip01_Jaw"][0])[1], 2)
        Z["bein"] = {}
        for key, sn, a_, b_, c_ in BEINE:
            L = self.LEG[key]
            hip, K, A = p[L["oben"]][1], p[L["unten"]][1], p[L["fuss"]][1]
            e = (A - hip) / np.linalg.norm(A - hip)
            pol = (K - hip) - e * float((K - hip) @ e)
            pol = pol / max(np.linalg.norm(pol), 1e-9)
            Z["bein"][key] = dict(ziel=[round(float(v), 4) for v in A], q=[round(v, 2) for v in euler_von(p[L["fuss"]][0])],
                                  pole=[round(float(v), 3) for v in pol])
            if a_ == "Thigh":
                Z["bein"][key]["zehe"] = round(euler_von(p[L["fuss"]][0].T @ p["Bip01_%s_Toe0" % sn][0])[1], 2)
        return Z

    def gelenke(self, t, q):
        """Lesbare Gelenk-Tabelle: je Knochen Drehung gegen die Ruhe-Lokaldrehung (Grad) und Innenwinkel Ellbogen/Knie/Hand-/Sprunggelenk."""
        R = self.rig
        p = self.lesen(t, q)
        out = {}
        for i, n in enumerate(R.name):
            if n.startswith("Bip01_"):
                out[n] = dict(lokal_grad=round(winkel(q_mat(R.q0[i]), q_mat(q[i])), 1), welt=[round(v, 1) for v in euler_von(p[n][0])],
                              kopf=[round(float(v), 3) for v in p[n][1]])
        for key, sn, a_, b_, c_ in BEINE:
            L = self.LEG[key]
            hip, K, A = p[L["oben"]][1], p[L["unten"]][1], p[L["fuss"]][1]
            u, v = hip - K, A - K
            out["innen_" + key] = round(math.degrees(math.acos(max(-1, min(1, float(u @ v) / np.linalg.norm(u) / np.linalg.norm(v))))), 1)
        return out


# ------------------------------------------------------------------ Sturz: heutige Death-Spur auf die neue Endpose ueberblenden
def sturz_gewichte(n):
    """Fortschritt je Bild wie pose_death (baer_kampf_gross.py:512): k Rumpf, kR/kL je Beinseite, kopf. Nur die Zeitform, keine Pose."""
    out = []
    for f in range(n):
        t = f / (n - 1)
        kipp = ssf(0.20, 0.60, t) ** 1.6
        feder = 0.040 * math.sin(max(0.0, min(1.0, (t - 0.60) / 0.20)) * math.pi) * (1.0 if t > 0.60 else 0.0)
        k = max(0.0, min(1.0, kipp - feder))
        kopf = ssf(0.55, 0.92, t)
        out.append(dict(k=k, kR=ssf(0.30 * 0.6, 1.0, k), kL=ssf(0.05 * 0.6, 1.0, k), kopf=k * kopf))
    out[-1] = dict(k=1.0, kR=1.0, kL=1.0, kopf=1.0)
    return out


def gruppe(name):
    if name in ("Bip01_Neck", "Bip01_Head", "Bip01_Jaw"):
        return "kopf"
    if "_L_" in name and "Clavicle" not in name:
        return "kL"
    if "_R_" in name and "Clavicle" not in name:
        return "kR"
    return "k"


def sturz(rig, alt, t_end, q_end, gewicht=None):
    """alt = rig.clip('DeerStag_Death'). Neu je Bild: q = q_alt(f) * slerp(1, q_alt(ende)^-1 * q_neu(ende), w(f)); Becken-Lage additiv.
    Bild 0 bleibt (w = 0), das letzte Bild ist genau die neue Endpose (w = 1). gewicht: Liste je Bild {k, kR, kL, kopf} (sturz_gewichte)."""
    n = len(alt["T"])
    G = sturz_gewichte(n) if gewicht is None else gewicht
    t = alt["t"].copy()
    q = alt["q"].copy()
    ip = rig.ix["Bip01_Pelvis"]
    for i, name in enumerate(rig.name):
        D = q_mat(alt["q"][-1, i]).T @ q_mat(q_end[i])
        if winkel(np.eye(3), D) < 1e-4:
            continue
        qd = mat_q(D)
        g = gruppe(name)
        for f in range(n):
            if G[f][g] <= 0.0:
                continue                                           # Gewicht 0: Schluessel genau wie heute (Anschluss an Idle)
            qq = mat_q(q_mat(alt["q"][f, i]) @ q_mat(q_slerp((0, 0, 0, 1), qd, G[f][g])))
            if f and float(qq @ q[f - 1, i]) < 0:
                qq = -qq
            q[f, i] = qq
        qe = np.asarray(q_end[i], float)
        q[-1, i] = qe if float(qe @ q[-2, i]) >= 0 else -qe
    for f in range(n):
        t[f, ip] = alt["t"][f, ip] + G[f]["k"] * (np.asarray(t_end[ip]) - alt["t"][-1, ip])
    t[-1, ip] = t_end[ip]
    return t, q


def boden_je_bild(rig, t, q, s=None, unten=-0.012, oben=0.005, fest=4, glatt=2):
    """Sturz am Boden halten: je Bild den tiefsten Hautpunkt messen; liegt er tiefer als 'unten' (m), das Becken heben, schwebt alles
    hoeher als 'oben', das Becken senken. Die ersten 'fest' Bilder und das letzte Bild bleiben, wie sie sind (Anschluss an Idle und an
    Dead). Die Korrektur wird ueber die Zeit geglaettet und danach noch einmal geklemmt. Liefert (t neu, Liste tiefster Punkt cm vorher,
    nachher, Korrektur cm)."""
    n = t.shape[0]
    ip = rig.ix["Bip01_Pelvis"]

    def zmin(tt, f):
        return float(rig.haut_tier(rig.welt(tt[f], q[f], None if s is None else s[f]))[:, 2].min())
    z0 = [zmin(t, f) for f in range(n)]
    lo = min(unten, z0[-1])
    hi = max(oben, z0[-1])

    def bedarf(z):
        return [(lo - v) if v < lo else ((hi - v) if v > hi else 0.0) for v in z]
    c = np.array(bedarf(z0))
    c[:fest] = 0.0
    c[-1] = 0.0
    need = c.copy()
    for _ in range(glatt):
        g = c.copy()
        g[1:-1] = 0.25 * c[:-2] + 0.5 * c[1:-1] + 0.25 * c[2:]
        c = np.where(need > 0, np.maximum(g, need), np.where(need < 0, np.minimum(g, need), g))
        c[:fest] = 0.0
        c[-1] = 0.0
    Rp = _rein(rig.welt(rig.t0, rig.q0)[rig.par[ip]][:3, :3])
    t2 = t.copy()
    for f in range(n):
        t2[f, ip] = t[f, ip] + Rp.T @ t2g(np.array([0.0, 0.0, c[f]]))
    z1 = [zmin(t2, f) for f in range(n)]
    return t2, [round(100 * v, 2) for v in z0], [round(100 * v, 2) for v in z1], [round(100 * float(v), 2) for v in c]


def spuren(rig, t_end, q_end, gewicht=None, boden=True, unten=-0.012, oben=0.005):
    """Beide Clips aus einer Endpose (lokal, Loeser.loese): Death = heutige Spur auf die Endpose ueberblendet und am Boden gehalten,
    Dead = genau das letzte Death-Bild (nur die Bip01_*-Drehungen und die Becken-Lage; alle anderen Schluessel bleiben die heutigen).
    Liefert ({clip: dict(t, q)}, info) fuer schreibe()."""
    death, dead = rig.clip("DeerStag_Death"), rig.clip("DeerStag_Dead")
    t2, q2 = sturz(rig, death, t_end, q_end, gewicht)
    info = {}
    if boden:
        t2, z0, z1, c = boden_je_bild(rig, t2, q2, death["s"], unten, oben)
        info = dict(sturz_tief_vor_cm=z0, sturz_tief_cm=z1, becken_korrektur_cm=c)
    td, qd = dead["t"].copy(), dead["q"].copy()
    ip = rig.ix["Bip01_Pelvis"]
    for i, name in enumerate(rig.name):
        if name.startswith("Bip01_"):
            qd[:, i] = q2[-1, i]
    td[:, ip] = t2[-1, ip]
    return {"DeerStag_Death": dict(t=t2, q=q2), "DeerStag_Dead": dict(t=td, q=qd)}, info


# ------------------------------------------------------------------ Messen an der Haut (tier-Meter)
def teile(rig):
    """Punkt-Masken nach dem staerksten Knochen: rumpf, hals, kopf, je Bein oben_/unten_/pfote_/bein_ (= unten + pfote)."""
    G = rig.gewichte()
    dom = np.argmax(G, 1)

    def m(*namen):
        return np.isin(dom, [rig.ix[x] for x in namen if x in rig.ix])
    T = dict(kopf=m("Bip01_Head", "Bip01_Jaw"), hals=m("Bip01_Neck"),
             rumpf=m("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Tail", "Bip01_L_Clavicle", "Bip01_R_Clavicle"))
    for key, sn, a_, b_, c_ in BEINE:
        T["oben_" + key] = m("Bip01_%s_%s" % (sn, a_))
        T["unten_" + key] = m("Bip01_%s_%s" % (sn, b_))
        T["pfote_" + key] = m("Bip01_%s_%s" % (sn, c_), "Bip01_%s_Toe0" % sn) if a_ == "Thigh" else m("Bip01_%s_%s" % (sn, c_))
        T["bein_" + key] = T["unten_" + key] | T["pfote_" + key]
    return T


def _solid(Q, A, B, C):
    a = A[None] - Q[:, None]
    b = B[None] - Q[:, None]
    c = C[None] - Q[:, None]
    la, lb, lc = (np.linalg.norm(x, axis=2) for x in (a, b, c))
    det = np.einsum("qtk,qtk->qt", a, np.cross(b, c))
    den = la * lb * lc + np.einsum("qtk,qtk->qt", a, b) * lc + np.einsum("qtk,qtk->qt", b, c) * la + np.einsum("qtk,qtk->qt", c, a) * lb
    return 2.0 * np.arctan2(det, den) / (4 * np.pi)


def windung(Q, P, tt, block=300):
    """Windungszahl der Punkte Q gegen die Dreiecke tt (Messart baer-2c sitzmess.py: |w| > 0,5 = innen)."""
    if len(tt) == 0 or len(Q) == 0:
        return np.zeros(len(Q))
    A, B, C = P[tt[:, 0]], P[tt[:, 1]], P[tt[:, 2]]
    w = np.zeros(len(Q))
    for i in range(0, len(Q), block):
        w[i:i + block] = _solid(Q[i:i + block], A, B, C).sum(1)
    return w


def paar(P, F, ma, mb):
    """Durchdringung Teil a gegen Teil b: Punkte von a IN b und b IN a (Windungszahl), groesste Eindringtiefe in cm (Abstand des tiefsten
    Innenpunkts zur Haut des anderen Teils, ueber dessen Punkte genaehert) und kleinster Abstand der beiden Haeute in cm (Punkt-Punkt)."""
    ia, ib = np.nonzero(ma)[0], np.nonzero(mb)[0]
    fa, fb = F[ma[F].all(1)], F[mb[F].all(1)]
    r = dict(a_in_b=0, b_in_a=0, tiefe_cm=0.0)
    lo, hi = P[ib].min(0) - 0.02, P[ib].max(0) + 0.02
    qa = ia[((P[ia] >= lo) & (P[ia] <= hi)).all(1)]
    lo, hi = P[ia].min(0) - 0.02, P[ia].max(0) + 0.02
    qb = ib[((P[ib] >= lo) & (P[ib] <= hi)).all(1)]
    tief = 0.0
    if len(qa):
        inn = qa[np.abs(windung(P[qa], P, fb)) > 0.5]
        r["a_in_b"] = int(len(inn))
        if len(inn):
            tief = max(tief, float(np.linalg.norm(P[inn][:, None] - P[ib][None], axis=2).min(1).max()))
    if len(qb):
        inn = qb[np.abs(windung(P[qb], P, fa)) > 0.5]
        r["b_in_a"] = int(len(inn))
        if len(inn):
            tief = max(tief, float(np.linalg.norm(P[inn][:, None] - P[ia][None], axis=2).min(1).max()))
    r["tiefe_cm"] = round(100 * tief, 2)
    dmin = 9.0
    for i in range(0, len(ia), 400):
        dmin = min(dmin, float(np.linalg.norm(P[ia[i:i + 400]][:, None] - P[ib][None], axis=2).min()))
    r["abstand_cm"] = round(100 * dmin, 2)
    return r


def auflage(P, F, hoehe=0.01):
    """Auflageflaeche in cm2: Dreiecke, deren drei Ecken tiefer als hoehe (m) liegen, auf den Boden projiziert."""
    m = (P[F, 2] < hoehe).all(1)
    a, b, c = P[F[m, 0]], P[F[m, 1]], P[F[m, 2]]
    fl = 0.5 * np.abs((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]))
    return float(fl.sum() * 1e4)


def dehnung(rig, P, T=None):
    """Kanten-Dehnung gegen die Ruhe (ohne Kopf, wenn T gegeben): 99,5 %-Wert und max."""
    F = rig.F
    E = np.unique(np.sort(np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]], 1), axis=0)
    R0 = g2t(rig.P)
    L0 = np.linalg.norm(R0[E[:, 0]] - R0[E[:, 1]], axis=1)
    ok = L0 > 0.004
    if T is not None:
        ok &= ~(T["kopf"][E[:, 0]] | T["kopf"][E[:, 1]])
    L1 = np.linalg.norm(P[E[ok, 0]] - P[E[ok, 1]], axis=1) / L0[ok]
    return float(np.percentile(L1, 99.5)), float(L1.max())


# ------------------------------------------------------------------ Relative Ziel-Tabelle (POSE.md) -> absolute Ziele
# Tabelle Z_rel: pel_xy [x, y], boden_rumpf (m, tiefster Punkt von Rumpf+Hals+Oberarmen/Oberschenkeln), q_pel/q_sp/q_ch/q_ne/q_he/q_ta,
# klav {L, R}, kiefer, kopf_boden (m, wahlfrei: Hals und Kopf nicken, bis der Kopf so tief liegt), bein[key]:
#   s      Abstand Schulter/Huefte -> Hand-/Sprunggelenk als Anteil der Beinlaenge
#   vor    Grad in der Bodenebene von der Bauchseite (+y) zum Kopf (+x) hin (negativ = zum Schwanz)
#   boden  tiefster Hautpunkt von Unterbein + Pfote (m): das Bein liegt auf   ODER   senk  Grad unter der Waagerechten: Bein in der Luft
#   pole   Richtung von Ellbogen/Knie (Vorgabe vorn -x, hinten +x: Beuge-Ebene liegt flach)
#   pfote  beuge = Grad um die Gelenkachse gegen die Ruhe-Stellung der Pfote am Unterbein, + = zur Geraden hin und darueber hinaus
#          (schlaffe Pfote: vorn palmar, hinten plantar); dreh = um die Unterbein-Achse; kipp = seitlich
RUMPF_TEILE = ("rumpf", "hals", "oben_VL", "oben_VR", "oben_HL", "oben_HR")


def achse(a, g):
    a = np.asarray(a, float) / np.linalg.norm(a)
    c, s = math.cos(math.radians(g)), math.sin(math.radians(g))
    x, y, z = a
    return np.array([[c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
                     [y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s],
                     [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)]])


def pfoten_richtung(rig, L, T):
    """Ruhe-Richtung Gelenk -> Pfotenmitte (Schwerpunkt der vorderen Haelfte der Pfotenpunkte), je Bein, tier."""
    P0 = rig.haut_tier(rig.W0)
    out = {}
    for key in ("VL", "VR", "HL", "HR"):
        Q = P0[T["pfote_" + key]]
        vorn = Q[Q[:, 0] > np.median(Q[:, 0])]
        d = vorn.mean(0) - L.Jp[L.LEG[key]["fuss"]]
        out[key] = d / np.linalg.norm(d)
    return out


def innen_winkel(A, K_, d):
    u = (K_ - A) / np.linalg.norm(K_ - A)
    return math.degrees(math.acos(max(-1, min(1, float(u @ d)))))


def aufloesen(rig, L, T, Z, runden=5):
    """Relative Tabelle -> absolute Ziele (Sprache des Kerns: pel, q_*, bein[key] = ziel/q/pole). Liefert (Z_abs, info)."""
    PR = pfoten_richtung(rig, L, T)
    Za = dict(pel=[Z["pel_xy"][0], Z["pel_xy"][1], Z.get("pel_z0", 0.45)], klav=dict(Z["klav"]), kiefer=Z.get("kiefer", 0.0), bein={})
    for k in ("q_pel", "q_sp", "q_ch", "q_ne", "q_he", "q_ta"):
        Za[k] = list(Z[k])
    for key in L.LEG:
        Za["bein"][key] = dict(ziel=list(L.Jp[L.LEG[key]["fuss"]]), q=[0, 0, 0], pole=list(Z["bein"][key].get("pole", [-1, 0, 0] if key[0] == "V" else [1, 0, 0])))
        if "zehe" in Z["bein"][key]:
            Za["bein"][key]["zehe"] = Z["bein"][key]["zehe"]
    m_rumpf = np.zeros(len(rig.P), bool)
    for k in RUMPF_TEILE:
        m_rumpf |= T[k]
    info = {}

    def haut():
        t, q = L.loese(Za)
        return rig.haut_tier(rig.welt(t, q))

    def setze_bein(key, zz):
        bz, L_ = Z["bein"][key], L.LEG[key]
        pose = L.welt_pose(Za)
        par = L.eltern[L_["oben"]]
        hip = pose[par][1] + pose[par][0] @ (L.Jp[L_["oben"]] - L.Jp[par])
        ln = (L_["a"] + L_["b"]) * bz["s"]
        dz = zz - hip[2]
        dz = max(-ln * 0.98, min(ln * 0.98, dz))
        h = math.sqrt(ln * ln - dz * dz)
        v = math.radians(bz["vor"])
        ziel = hip + np.array([h * math.sin(v), h * math.cos(v), dz])
        Za["bein"][key]["ziel"] = [float(x) for x in ziel]
        # Pfote: an das Unterbein gehaengt, dann um die Gelenkachse auf den Innenwinkel gedreht
        st = {}
        L._bein(pose, key, ziel, np.eye(3), np.array(Za["bein"][key]["pole"], float), st)
        Qlo, Kp = pose[L_["unten"]]
        n = Qlo @ L_["F2"][:, 1]
        pf = bz.get("pfote", {})
        Q = Qlo
        if pf.get("beuge"):
            # + = die Pfote klappt von der Ruhe-Stellung aus zur Geraden hin und darueber hinaus (vorn palmar, hinten plantar: schlaffe Pfote)
            w0 = innen_winkel(ziel, Kp, Qlo @ PR[key])
            w1 = innen_winkel(ziel, Kp, achse(n, 1.0) @ Qlo @ PR[key])
            Q = achse(n, (1.0 if w1 > w0 else -1.0) * pf["beuge"]) @ Qlo
        y2 = (ziel - Kp) / np.linalg.norm(ziel - Kp)
        if pf.get("kipp"):
            Q = achse(np.cross(n, y2), pf["kipp"]) @ Q
        if pf.get("dreh"):
            Q = achse(y2, pf["dreh"]) @ Q
        Za["bein"][key]["q"] = [float(v_) for v_ in euler_von(Q)]
        return hip

    def bein_z(key):
        bz, L_ = Z["bein"][key], L.LEG[key]
        pose = L.welt_pose(Za)
        par = L.eltern[L_["oben"]]
        hip = pose[par][1] + pose[par][0] @ (L.Jp[L_["oben"]] - L.Jp[par])
        ln = (L_["a"] + L_["b"]) * bz["s"]
        if "senk" in bz:
            setze_bein(key, hip[2] - ln * math.sin(math.radians(bz["senk"])))
            return
        lo, hi = hip[2] - ln * 0.9, hip[2] + ln * 0.9
        for _ in range(18):
            mid = 0.5 * (lo + hi)
            setze_bein(key, mid)
            zmin = float(haut()[T["bein_" + key], 2].min())
            if zmin > bz["boden"]:
                hi = mid
            else:
                lo = mid
        setze_bein(key, 0.5 * (lo + hi))

    for _ in range(runden):
        for key in ("VR", "HR", "VL", "HL"):
            bein_z(key)
        P = haut()
        Za["pel"][2] += Z.get("boden_rumpf", -0.010) - float(P[m_rumpf, 2].min())
    for key in ("VR", "HR", "VL", "HL"):
        bein_z(key)
    Za["pel"][2] += Z.get("boden_rumpf", -0.010) - float(haut()[m_rumpf, 2].min())
    if "kopf_boden" in Z:
        base_ne, base_he = list(Z["q_ne"]), list(Z["q_he"])
        lo, hi = -40.0, 40.0
        for _ in range(16):
            mid = 0.5 * (lo + hi)
            Za["q_ne"] = [base_ne[0], base_ne[1] + mid * Z.get("kopf_anteil_hals", 0.5), base_ne[2]]
            Za["q_he"] = [base_he[0], base_he[1] + mid, base_he[2]]
            zmin = float(haut()[T["kopf"], 2].min())
            if zmin > Z["kopf_boden"]:
                lo = mid
            else:
                hi = mid
        info["kopf_nick_zusatz"] = round(0.5 * (lo + hi), 2)
    return Za, info


def bein_winkel(L, pose, key):
    """prot (vor/zurueck) und abd (seitlich, + = vom Koerper weg) des Oberarms/Oberschenkels gegen den Elternknochen, relativ zur Ruhe;
    inner = Innenwinkel Ellbogen/Knie; pfote = Innenwinkel Unterbein gegen Pfotenknochen-Richtung (Ruhe-Wert dazu)."""
    L_ = L.LEG[key]
    par = L.eltern[L_["oben"]]
    Qp = pose[par][0]
    hip, Kp, A = pose[L_["oben"]][1], pose[L_["unten"]][1], pose[L_["fuss"]][1]
    d = Qp.T @ ((Kp - hip) / np.linalg.norm(Kp - hip))
    d0 = L.Jp[L_["unten"]] - L.Jp[L_["oben"]]
    d0 = d0 / np.linalg.norm(d0)
    sag = lambda v: math.degrees(math.atan2(v[0], -v[2]))  # noqa: E731
    lat = L_["s"]
    asin = lambda x: math.degrees(math.asin(max(-1, min(1, x))))  # noqa: E731
    u, v = hip - Kp, A - Kp
    inner = math.degrees(math.acos(max(-1, min(1, float(u @ v) / np.linalg.norm(u) / np.linalg.norm(v)))))
    return dict(prot=round(sag(d) - sag(d0), 1), abd=round(asin(d[1] * lat) - asin(d0[1] * lat), 1), inner=round(inner, 1))


def rumpf_winkel(pose):
    r = {}
    for nm, a, b in (("sp_pel", "Bip01_Pelvis", "Bip01_Spine"), ("ch_sp", "Bip01_Spine", "Bip01_Spine1"), ("ne_ch", "Bip01_Spine1", "Bip01_Neck"),
                     ("he_ne", "Bip01_Neck", "Bip01_Head")):
        r[nm] = [round(v, 1) for v in euler_von(pose[a][0].T @ pose[b][0])]
    return r


# ------------------------------------------------------------------ GLB schreiben: nur Death/Dead neu
def schreibe(gerippe, aus, neu, generator="baer_kern_liegen.py (Lauf baer-liegen)", still=False):
    """neu = {clipname: dict(t=(n, nn, 3), q=(n, nn, 4))} an den dichten Zeiten des Clips (Rig.clip). Fuer jeden Dreh-/Lage-Kanal dieser
    Clips, dessen Werte sich aendern, ein NEUER Accessor; Zeit-Accessoren, Skalier-Schluessel und alle anderen Clips bleiben, wie sie sind.
    Kanaele mit nur 2 Schluesseln (konstant), die jetzt laufen, bekommen die dichte Zeitreihe DESSELBEN Clips (gleiche Abtastzeiten)."""
    rig = Rig(gerippe)
    J, B = rig.J, rig.B
    J2 = json.loads(json.dumps(J))
    n_acc = len(J["accessors"])
    anh, info = [], {}
    for an in J2["animations"]:
        nm = an["name"]
        if nm not in neu:
            continue
        assert nm in CLIPS_LIEGEN, "nur Death/Dead duerfen neu sein: %s" % nm
        alt = rig.clip(nm)
        T, ia = alt["T"], alt["ia"]
        n = len(T)
        assert neu[nm]["q"].shape[0] == n and neu[nm]["t"].shape[0] == n, (nm, n)
        cnt = {}
        for ch in an["channels"]:
            cnt[ch["sampler"]] = cnt.get(ch["sampler"], 0) + 1
        assert max(cnt.values()) == 1, "Sampler zwischen Kanaelen geteilt"
        ni = dict(rotation=0, translation=0, gleich=0, dicht=0)
        for ch in an["channels"]:
            path, node = ch["target"]["path"], ch["target"]["node"]
            if path not in ("rotation", "translation"):
                continue
            v = (neu[nm]["q"] if path == "rotation" else neu[nm]["t"])[:, node].astype(np.float32)
            a_ = (alt["q"] if path == "rotation" else alt["t"])[:, node].astype(np.float32)
            if np.array_equal(v, a_):
                ni["gleich"] += 1
                continue
            smp = an["samplers"][ch["sampler"]]
            ti = acc_arr(J, B, smp["input"])[:, 0]
            if len(ti) == n:
                w = v
            elif np.abs(v - v[0]).max() < 1e-7:
                w = np.repeat(v[:1], len(ti), 0)                     # bleibt konstant: Schluesselzahl wie heute
            else:
                w = v                                              # laeuft jetzt: dichte Zeiten desselben Clips
                smp["input"] = int(ia)
                smp["interpolation"] = "LINEAR"
                ni["dicht"] += 1
            anh.append(({"componentType": 5126, "count": int(len(w)), "type": "VEC4" if path == "rotation" else "VEC3"},
                        np.ascontiguousarray(w)))
            smp["output"] = n_acc + len(anh) - 1
            ni[path] += 1
        info[nm] = ni
    J2["accessors"].extend(a for a, _ in anh)
    daten = {n_acc + k: d for k, (_, d) in enumerate(anh)}
    benutzt = set()
    for m in J2["meshes"]:
        for pr in m["primitives"]:
            benutzt |= set(pr["attributes"].values())
            if "indices" in pr:
                benutzt.add(pr["indices"])
    for sk in J2.get("skins", []):
        if "inverseBindMatrices" in sk:
            benutzt.add(sk["inverseBindMatrices"])
    for an in J2["animations"]:
        for smp in an["samplers"]:
            benutzt |= {smp["input"], smp["output"]}
    behalten = [i for i in range(len(J2["accessors"])) if i in benutzt]
    nix = {i: k for k, i in enumerate(behalten)}
    J2["accessors"] = [J2["accessors"][i] for i in behalten]
    for m in J2["meshes"]:
        for pr in m["primitives"]:
            pr["attributes"] = {k: nix[v] for k, v in pr["attributes"].items()}
            if "indices" in pr:
                pr["indices"] = nix[pr["indices"]]
    for sk in J2.get("skins", []):
        if "inverseBindMatrices" in sk:
            sk["inverseBindMatrices"] = nix[sk["inverseBindMatrices"]]
    for an in J2["animations"]:
        for smp in an["samplers"]:
            smp["input"], smp["output"] = nix[smp["input"]], nix[smp["output"]]
    bin_, views = bytearray(), []
    for k, i in enumerate(behalten):
        ac = J2["accessors"][k]
        data = np.ascontiguousarray(daten[i].astype(np.float32)).tobytes() if i in daten else acc_bytes(J, B, i)
        while len(bin_) % 4:
            bin_ += b"\0"
        v = {"buffer": 0, "byteOffset": len(bin_), "byteLength": len(data)}
        if i < n_acc:
            va = J["bufferViews"][J["accessors"][i]["bufferView"]]
            if "target" in va:
                v["target"] = va["target"]
            if "byteStride" in va:
                v["byteStride"] = va["byteStride"]
        views.append(v)
        ac["bufferView"] = k
        ac.pop("byteOffset", None)
        bin_ += data
    while len(bin_) % 4:
        bin_ += b"\0"
    J2["bufferViews"] = views
    J2["buffers"] = [{"byteLength": len(bin_)}]
    J2["asset"]["generator"] = generator
    js = json.dumps(J2, separators=(",", ":")).encode()
    while len(js) % 4:
        js += b" "
    out = b"glTF" + struct.pack("<II", 2, 12 + 8 + len(js) + 8 + len(bin_))
    out += struct.pack("<I", len(js)) + b"JSON" + js + struct.pack("<I", len(bin_)) + b"BIN\0" + bytes(bin_)
    open(aus, "wb").write(out)
    r = pruefe_nur_liegen(gerippe, aus)
    r["neu"] = info
    r["weggelassen"] = n_acc + len(anh) - len(behalten)
    r["md5"] = hashlib.md5(out).hexdigest()
    if not still:
        print("LIEGEN", aus, "MD5", r["md5"], "Bytes", len(out))
        print("LIEGEN andere Clips byte-gleich %d/%d Sampler-Puffer; Netz/Skin/Knoten byte-gleich: %s; neue Kanaele %s; unbenutzte Accessoren weg %d"
              % (r["gleich"], r["alle"], r["rest_gleich"], json.dumps(info), r["weggelassen"]))
    return r


def pruefe_nur_liegen(alt_pfad, neu_pfad):
    """Beweis 'nur Death/Dead': alle anderen Clips (Kanaele, Zeiten, Werte, Interpolation), Knoten, Skin, inverse Bind und die Netz-Puffer
    byte-gleich; in Death/Dead gleiche Kanaele, gleiche Menge an Abtastzeiten (also Dauer und Bildzahl), Skalier-Schluessel byte-gleich."""
    J, B = lade_glb(alt_pfad)
    J3, B3 = lade_glb(neu_pfad)
    gleich = alle = 0
    assert [a["name"] for a in J["animations"]] == [a["name"] for a in J3["animations"]]
    for a1, a2 in zip(J["animations"], J3["animations"]):
        assert a1["channels"] == a2["channels"], a1["name"]
        if a1["name"] in CLIPS_LIEGEN:
            z1 = sorted(set(np.concatenate([acc_arr(J, B, s["input"])[:, 0] for s in a1["samplers"]]).tolist()))
            z2 = sorted(set(np.concatenate([acc_arr(J3, B3, s["input"])[:, 0] for s in a2["samplers"]]).tolist()))
            assert z1 == z2, "Abtastzeiten geaendert: %s" % a1["name"]
            for ch in a1["channels"]:
                s1, s2 = a1["samplers"][ch["sampler"]], a2["samplers"][ch["sampler"]]
                if ch["target"]["path"] == "scale":
                    assert acc_bytes(J, B, s1["output"]) == acc_bytes(J3, B3, s2["output"])
                    assert acc_bytes(J, B, s1["input"]) == acc_bytes(J3, B3, s2["input"])
            continue
        for s1, s2 in zip(a1["samplers"], a2["samplers"]):
            alle += 2
            gleich += acc_bytes(J, B, s1["input"]) == acc_bytes(J3, B3, s2["input"])
            gleich += acc_bytes(J, B, s1["output"]) == acc_bytes(J3, B3, s2["output"])
            assert s1.get("interpolation") == s2.get("interpolation")
    assert gleich == alle, (gleich, alle)
    assert J["nodes"] == J3["nodes"] and J["skins"] == J3["skins"] and J["scenes"] == J3["scenes"]
    assert acc_bytes(J, B, J["skins"][0]["inverseBindMatrices"]) == acc_bytes(J3, B3, J3["skins"][0]["inverseBindMatrices"])
    p1, p3 = J["meshes"][0]["primitives"][0], J3["meshes"][0]["primitives"][0]
    assert set(p1["attributes"]) == set(p3["attributes"])
    for k in p1["attributes"]:
        assert acc_bytes(J, B, p1["attributes"][k]) == acc_bytes(J3, B3, p3["attributes"][k]), k
        a1, a3 = J["accessors"][p1["attributes"][k]], J3["accessors"][p3["attributes"][k]]
        assert {x: a1[x] for x in a1 if x not in ("bufferView", "byteOffset")} == {x: a3[x] for x in a3 if x not in ("bufferView", "byteOffset")}
    assert acc_bytes(J, B, p1["indices"]) == acc_bytes(J3, B3, p3["indices"])
    assert {k: v for k, v in J["meshes"][0].items() if k != "primitives"} == {k: v for k, v in J3["meshes"][0].items() if k != "primitives"}
    assert J.get("materials") == J3.get("materials") and J.get("images") == J3.get("images") and J.get("textures") == J3.get("textures")
    return dict(gleich=gleich, alle=alle, rest_gleich=True)


# ------------------------------------------------------------------ Ein Befehl: Tabelle + Gerippe -> GLB mit neuem Death/Dead
def abnahme(rig, T, P):
    """Kurz-Messung der Endpose (tier-Meter): Boden, Auflage, Durchdringung/Abstand je Pfoten- und Beinpaar und Bein gegen Rumpf, Dehnung.
    (Sichtbarkeit aus Kevins Kamera: _arbeit/baer_liegen/werkzeug/mess_liegen.py.)"""
    F = rig.F
    keys = [b[0] for b in BEINE]
    r = dict(tief_cm=round(100 * float(P[:, 2].min()), 2), rumpf_tief_cm=round(100 * min(float(P[T[k], 2].min()) for k in RUMPF_TEILE), 2),
             kopf_tief_cm=round(100 * float(P[T["kopf"], 2].min()), 2), auflage_cm2=round(auflage(P, F, 0.01), 0),
             bein_tief_cm={k: round(100 * float(P[T["bein_" + k], 2].min()), 2) for k in keys})
    paare = {}
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            paare["pfote_%s-pfote_%s" % (a, b)] = paar(P, F, T["pfote_" + a], T["pfote_" + b])
            paare["bein_%s-bein_%s" % (a, b)] = paar(P, F, T["bein_" + a], T["bein_" + b])
    koerper = T["rumpf"] | T["hals"] | T["kopf"]
    for a in keys:
        paare["bein_%s-rumpf" % a] = paar(P, F, T["bein_" + a], koerper)
    r["paare"] = paare
    r["pfote_bein_punkte"] = int(sum(v["a_in_b"] + v["b_in_a"] for k, v in paare.items() if not k.endswith("-rumpf")))
    r["rumpf_punkte"] = int(sum(v["a_in_b"] + v["b_in_a"] for k, v in paare.items() if k.endswith("-rumpf")))
    r["pfoten_abstand_min_cm"] = min(v["abstand_cm"] for k, v in paare.items() if k.startswith("pfote_"))
    d99, dmax = dehnung(rig, P, T)
    r["dehnung"] = [round(d99, 2), round(dmax, 2)]
    return r


def baue(gerippe, Z, aus, generator=None, still=False, gewicht=None):
    """EIN Schritt je Koerper: relative Tabelle Z (POSE.md T1) auf dem Skelett/Netz von 'gerippe' aufloesen, Death/Dead rechnen, GLB nach
    'aus' schreiben (nur diese zwei Clips neu, Selbstpruefung), Endpose messen. 'gerippe' wird nur gelesen."""
    rig = Rig(gerippe)
    L = Loeser(rig)
    T = teile(rig)
    Za, info = aufloesen(rig, L, T, Z)
    stat = {}
    pose = L.welt_pose(Za, stat)
    t, q = L.lokal(pose)
    neu, si = spuren(rig, t, q, gewicht)
    r = schreibe(gerippe, aus, neu, generator or "baer_kern_liegen.py baue (Lauf baer-liegen)", still)
    m = abnahme(rig, T, rig.haut_tier(rig.welt(t, q)))
    out = dict(md5=r["md5"], neu=r["neu"], ziele_abs=Za, stat=stat, mess=m, sturz=si, bein_winkel={k: bein_winkel(L, pose, k) for k in L.LEG},
               rumpf_winkel=rumpf_winkel(pose))
    out.update(info)
    if not still:
        print("LIEGEN Endpose: tief %+.2f cm, Rumpf %+.2f, Kopf %+.2f, Auflage %d cm2, Pfote/Bein-Paare %d Punkte, Bein-Rumpf %d Punkte, "
              "Pfotenabstand min %.2f cm, Dehnung %s; Sturz tief %.2f..%.2f cm"
              % (m["tief_cm"], m["rumpf_tief_cm"], m["kopf_tief_cm"], m["auflage_cm2"], m["pfote_bein_punkte"], m["rumpf_punkte"],
                 m["pfoten_abstand_min_cm"], m["dehnung"], min(si["sturz_tief_cm"]), max(si["sturz_tief_cm"])))
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4 and sys.argv[1] == "pruefe":
        print("NUR_LIEGEN_OK", json.dumps(pruefe_nur_liegen(sys.argv[2], sys.argv[3])))
    elif len(sys.argv) >= 5 and sys.argv[1] == "baue":
        _r = baue(sys.argv[2], json.load(open(sys.argv[3])), sys.argv[4])
        if len(sys.argv) > 5:
            json.dump(_r, open(sys.argv[5], "w"), indent=1)
    else:
        print("Aufruf: python baer_kern_liegen.py pruefe ALT.glb NEU.glb")
        print("        python baer_kern_liegen.py baue GERIPPE.glb POSE.json AUS.glb [BERICHT.json]   (POSE.json = relative Tabelle, POSE.md T1)")
