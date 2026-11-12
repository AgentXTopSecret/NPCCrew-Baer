# Lauf baer-junges (10.11.2026), Bau Koerper: Skelett und Koerper-Form des Baeren-Jungen NCBearCub (SPEZ_JUNGES.md A.2, B).
# Nur numpy. Geruest (Raeume, FK, Klassen) aus baer_form_baby.py, Feld-Idee form_2c (baer_export_2c.py:1772). Bauweg A+:
#   das fertige Spielnetz 2c (eingang/lp_2c.npz, 9.330 Punkte / 18.576 Dreiecke) wird mit EINEM Feld form_junges zum Jungen:
#   Stufe 1 (Knochen): je Punkt die gewichtete Abbildung Ruhe Erwachsener -> Ruhe Junges (Beine starr verschoben, Rumpf x 0,85
#                      entlang und quer, Platzhalter-Kopf = Kopf des Erwachsenen um das Kopfgelenk gestreckt 1,25 / 1,29 / 1,39)
#   Stufe 2 (Form):    Pfoten breiter, Krallen x 0,75, Beine dicker (Soll-Tabellen B.3), Rumpf auf Ruecken-/Bauchlinie und halbe
#                      Breite (B.2), Hintern rund, danach die Verschiebung geglaettet
#   Dasselbe Feld gilt fuer die dichte Huelle eingang/form2c_feld_2c.npz S (Gewichte aus den 8 naechsten Spielnetz-Punkten).
# Alle Eingaenge NUR aus _arbeit/baer_junges/eingang/ (MD5 in eingang/md5.txt). Topologie, Punkt-Nummern, UV, Sohlen bleiben 2c.
# Aufruf: python baer_form_junges.py bauen [AUS_ORDNER]      -> koerper/lp_junges.npz, huelle_junges.npz, skelett.json, mass.json
#         python baer_form_junges.py mass  NPZ               -> Masse B.1-B.4 eines lp_junges.npz
# Statisch/offline, nicht gespielt. Weder Test-Mod noch NPC Crew werden gelesen oder beschrieben.
#
# Raeume: dump = Modellraum des Importers (0,544 E je Meter); tier = Meter, x vorn, y links, z oben: tier = (-z_d, x_d, y_d) / 0,544
import json
import os
import pickle
import struct
import sys

import numpy as np

M2U = 0.544
ARB = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges/"
EIN = ARB + "eingang/"
DUMP_ERW = EIN + "erw_2c.txt.pkl"
GLB_ERW = EIN + "NCBear.glb"
FZ = np.diag([1.0, 1.0, -1.0])

# ---------------------------------------------------------------- Skelett-Faktoren (SPEZ B.5) ------------------------------------
F_RUMPF, F_BEIN, F_PFOTE, F_HALS, F_KIEFER = 0.85, 1.0, 1.0, 1.0, 1.20
DX = 0.05625                       # Hinterbeine +DX, Vorderbeine -DX in tier x (die Mitte zwischen den Pfoten bleibt)
FAKTOR = {"Spine": F_RUMPF, "Spine1": F_RUMPF, "Neck": F_RUMPF, "Tail": F_RUMPF, "Head": F_HALS, "Jaw": F_KIEFER}
for _s in "LR":
    FAKTOR.update({_s + "_Thigh": F_RUMPF, _s + "_Clavicle": F_RUMPF, _s + "_UpperArm": F_RUMPF, _s + "_Calf": F_BEIN,
                   _s + "_Foot": F_BEIN, _s + "_Forearm": F_BEIN, _s + "_Hand": F_BEIN, _s + "_Toe0": F_PFOTE})
# Platzhalter-Kopf (SPEZ G (1)): Kopf des Erwachsenen um das Kopfgelenk gestreckt, Knochen-Lokal X quer / Y laengs / Z hoch
S_KOPF = (1.29, 1.09, 1.39)   # laengs 1,09 statt 1,25: Nasenspitze bei x 1,11 (B.1), siehe bau_koerper.md
S_RUMPF = (0.85, 0.85, 1.0)        # Stufe 1: Rumpf quer wie das Skelett (Hueften/Schultern), laengs 0,85, hoch 1,0; Stufe 2 formt nach
S_SCHWANZ = (0.6, 0.6, 0.6)        # B.4: Schwanz-Punkte zum Schwanzgelenk hin


def lade_json_glb(pfad=GLB_ERW):
    b = open(pfad, "rb").read()
    assert b[:4] == b"glTF"
    n = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + n])
    o = 20 + n
    bl = struct.unpack("<I", b[o:o + 4])[0]
    return J, b[o + 8:o + 8 + bl]


def quat_m(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def m_quat(R):
    """Drehmatrix -> Quaternion (x, y, z, w)."""
    t = np.trace(R)
    if t > 0:
        s = np.sqrt(t + 1.0) * 2
        q = ((R[2, 1] - R[1, 2]) / s, (R[0, 2] - R[2, 0]) / s, (R[1, 0] - R[0, 1]) / s, 0.25 * s)
    else:
        i = int(np.argmax(np.diag(R)))
        j, k = (i + 1) % 3, (i + 2) % 3
        s = np.sqrt(1.0 + R[i, i] - R[j, j] - R[k, k]) * 2
        q = [0.0, 0.0, 0.0, 0.0]
        q[i] = 0.25 * s
        q[j] = (R[j, i] + R[i, j]) / s
        q[k] = (R[k, i] + R[i, k]) / s
        q[3] = (R[k, j] - R[j, k]) / s
    q = np.array(q)
    return q / np.linalg.norm(q)


def tier(P):
    P = np.asarray(P, float)
    return np.stack((-P[..., 2], P[..., 0], P[..., 1]), -1) / M2U


def dump(T):
    T = np.asarray(T, float)
    return np.stack((T[..., 1], T[..., 2], -T[..., 0]), -1) * M2U


A_TD = np.array([[0, 0, -1.0], [1, 0, 0], [0, 1, 0]])      # Richtung dump -> tier (ohne Massstab)


class Skelett:
    """Erwachsener 2c (Ruhe aus den GLB-Knoten, Dump-Raum) und Junges (gleiche Ruhe-Drehungen, Lagen mal Faktor, SPEZ B.5)."""

    def __init__(self, dump_pkl=DUMP_ERW):
        D = pickle.load(open(dump_pkl, "rb"))
        self.D = D
        self.names, self.par, self.idx = D["names"], D["par"], D["idx"]
        self.nb = len(self.names)
        J, _ = lade_json_glb()
        nodes = {n["name"]: n for n in J["nodes"]}
        self.t_e = np.zeros((self.nb, 3))
        self.R_loc = np.zeros((self.nb, 3, 3))
        for b, nm in enumerate(self.names):
            n = nodes[nm]
            self.t_e[b] = FZ @ np.array(n.get("translation", [0, 0, 0]), float)
            self.R_loc[b] = FZ @ quat_m(n.get("rotation", [0, 0, 0, 1])) @ FZ
        self.BW_e = self.fk(self.t_e, self.R_loc)
        # Junges: Lage = Faktor x Lage des Erwachsenen; Becken so, dass die Mitte der Hueftgelenke um DX nach vorn rueckt
        self.t_j = self.t_e.copy()
        for b, nm in enumerate(self.names):
            self.t_j[b] = FAKTOR.get(nm.replace("Bip01_", ""), 1.0) * self.t_e[b]
        ip, ih = self.idx["Bip01_Pelvis"], self.idx["Bip01_L_Thigh"]
        ib = self.idx["Bip01"]
        t_mitte = self.t_e[ih] * np.array((0.0, 1.0, 1.0))             # Mitte der Hueftgelenke im Becken-Raum (E)
        self.t_mitte = t_mitte
        R_pel = self.BW_e[ip][:3, :3]
        hm_e = self.BW_e[ip][:3, 3] + R_pel @ t_mitte                  # Hueftmitte Erwachsener (dump-Welt)
        p_j = hm_e + dump(np.array((DX, 0.0, 0.0))) - R_pel @ (F_RUMPF * t_mitte)
        self.t_j[ip] = np.linalg.inv(self.BW_e[ib][:3, :3]) @ (p_j - self.BW_e[ib][:3, 3])
        self.BW_j = self.fk(self.t_j, self.R_loc)
        self.inv_e = np.array([np.linalg.inv(m) for m in self.BW_e])
        self.inv_j = np.array([np.linalg.inv(m) for m in self.BW_j])

    def fk(self, t_loc, R_loc):
        W = np.zeros((self.nb, 4, 4))
        for b in range(self.nb):
            T = np.eye(4)
            T[:3, :3] = R_loc[b]
            T[:3, 3] = t_loc[b]
            W[b] = T if self.par[b] < 0 else W[self.par[b]] @ T
        return W

    def gelenk_e(self, nm):
        return tier(self.BW_e[self.idx["Bip01_" + nm if not nm.startswith(("Bip", "Dum", "Tra")) else nm]][:3, 3])

    def gelenk_j(self, nm):
        return tier(self.BW_j[self.idx["Bip01_" + nm if not nm.startswith(("Bip", "Dum", "Tra")) else nm]][:3, 3])

    def clip_lokal_erw(self, clip, bild):
        """Lokale Schluessel des Erwachsenen (Dump-Raum): Lage, Drehmatrix."""
        Lk = self.D["clips"][clip]["L"][bild]
        t = self.t_e.copy()
        R = self.R_loc.copy()
        for b in range(self.nb):
            if b in Lk:
                t[b] = Lk[b][:3]
                R[b] = quat_m(Lk[b][3:7])
        return t, R

    def becken_regel(self, R_welt_pel_erw, hm_erw, R_welt_bip, p_bip, dz=0.0):
        """SPEZ D.2: Becken-Lage (lokal im Bip01-Raum, E) so, dass die Hueftmitte = Hueftmitte des Erwachsenen + (DX, 0, dz)."""
        p = hm_erw + dump(np.array((DX, 0.0, dz))) - R_welt_pel_erw @ (F_RUMPF * self.t_mitte)
        return np.linalg.inv(R_welt_bip) @ (p - p_bip)

    def lokal_junges(self, clip, bild, dz=0.0):
        """Lokale Schluessel des Jungen fuer ein Bild eines Clips des ERWACHSENEN (Drehungen gleich, Lagen B.5, Becken-Regel D.2)."""
        t, R = self.clip_lokal_erw(clip, bild)
        Me = self.fk(t, R)
        ip, ib = self.idx["Bip01_Pelvis"], self.idx["Bip01"]
        hm = Me[ip][:3, 3] + Me[ip][:3, :3] @ self.t_mitte
        tj = self.t_j.copy()
        tj[ib] = t[ib]
        tj[self.idx["Translation_Data"]] = t[self.idx["Translation_Data"]]
        tj[ip] = self.becken_regel(Me[ip][:3, :3], hm, Me[ib][:3, :3], Me[ib][:3, 3], dz)
        return tj, R

    def welt_junges(self, clip, bild, dz=0.0):
        tj, R = self.lokal_junges(clip, bild, dz)
        return self.fk(tj, R)


def haut(Mw, inv_bind, P_d, W, bi):
    """Linear Blend Skinning (Dump-Raum). W: n x k Gewichte, bi: Knochenindex je Spalte."""
    h = np.c_[P_d, np.ones(len(P_d))]
    out = np.zeros((len(P_d), 3))
    for k, b in enumerate(bi):
        w = W[:, k]
        m = w > 0
        if m.any():
            out[m] += w[m, None] * (h[m] @ (Mw[b] @ inv_bind[b]).T)[:, :3]
    return out


# ---------------------------------------------------------------- Netz-Helfer -----------------------------------------------------
def nachbarn(T, n):
    nb = [[] for _ in range(n)]
    for a, b, c in T:
        nb[a] += [b, c]
        nb[b] += [a, c]
        nb[c] += [a, b]
    return [np.unique(x) for x in nb]


def laplace_matrix(T, n):
    """Zeilen-normierte Nachbar-Mittelung als (Index, Zeiger)-Felder fuer schnelles Glaetten."""
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]], T[:, [1, 0]], T[:, [2, 1]], T[:, [0, 2]]))
    E = np.unique(E, axis=0)
    cnt = np.bincount(E[:, 0], minlength=n).astype(float)
    return E, np.maximum(cnt, 1.0)


def glaetten(X, E, cnt, runden, lam=0.5, fest=None):
    """Glaettet ein Feld X (n x k) ueber die Netzkanten; fest: Maske der Punkte, die bleiben."""
    X = X.copy()
    for _ in range(runden):
        acc = np.zeros_like(X)
        np.add.at(acc, E[:, 0], X[E[:, 1]])
        neu = X + lam * (acc / cnt[:, None] - X)
        if fest is not None:
            neu[fest] = X[fest]
        X = neu
    return X


def sst(a, b, x):
    t = np.clip((np.asarray(x, float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def schalen(T, n):
    """Zusammenhangs-Komponenten (Punkt -> Nummer)."""
    p = np.arange(n)

    def w(i):
        while p[i] != i:
            p[i] = p[p[i]]
            i = p[i]
        return i
    for a, b, c in T:
        ra = w(a)
        p[w(b)] = ra
        p[w(c)] = ra
    return np.array([w(i) for i in range(n)])


# ---------------------------------------------------------------- Soll-Tabellen (SPEZ B.2, B.3) -----------------------------------
# Ruecken- und Bauchlinie in der Mittelebene, halbe Breite je x (Meter, Ruhe)
X_RUE = np.array((-0.74, -0.70, -0.60, -0.50, -0.42, -0.30, -0.20, -0.10, 0.00, 0.10, 0.23, 0.30, 0.40, 0.47))
Z_RUE = np.array((0.66, 0.84, 1.03, 1.115, 1.143, 1.150, 1.150, 1.150, 1.150, 1.148, 1.143, 1.125, 1.07, 1.00))
X_BAU = np.array((-0.50, -0.42, -0.30, -0.20, -0.10, 0.00, 0.10, 0.23, 0.30, 0.40))
Z_BAU = np.array((0.50, 0.45, 0.415, 0.402, 0.400, 0.402, 0.410, 0.425, 0.45, 0.52))
X_BRE = np.array((-0.70, -0.60, -0.50, -0.40, -0.20, 0.00, 0.20, 0.30, 0.40, 0.47))
Y_BRE = np.array((0.20, 0.30, 0.335, 0.335, 0.325, 0.32, 0.318, 0.30, 0.255, 0.225))
# Beine: Breite von der Seite / von vorn (m) je Hoehe z
Z_BEIN = np.array((0.15, 0.20, 0.25, 0.30, 0.35, 0.40))
V_SEITE = np.array((0.220, 0.235, 0.255, 0.275, 0.295, 0.315))
V_VORN = np.array((0.210, 0.220, 0.230, 0.245, 0.260, np.nan))
H_SEITE = np.array((0.230, 0.240, 0.265, 0.290, 0.315, 0.340))
H_VORN = np.array((0.205, 0.220, 0.240, 0.260, 0.275, np.nan))
V_AUSSEN = np.array((0.300, 0.304, 0.308, 0.312, 0.316, 0.318))      # Aussenkante |y| je Hoehe (B.3)
H_AUSSEN = np.array((0.312, 0.320, 0.327, 0.332, 0.336, 0.338))
H_HINTEN = np.array((-0.528, -0.545, -0.550, -0.554, -0.557, -0.560))  # Hinterkante x des Hinterbeins je Hoehe (B.3)
PFOTE_V_BREIT, PFOTE_H_BREIT = 1.15, 1.08
KRALLE_F = 0.75
X_ENDE = -0.74                     # Rumpfende (B.1)


SIGMA_W = 0.03                     # Gauss-Breite (m) der raeumlich geglaetteten Gewichte


def raum_glatt(X, werte, sigma, block=400):
    """Raeumliches Gauss-Mittel von werte (n x k) ueber die Punkte X (n x 3)."""
    out = np.zeros_like(werte, dtype=float)
    x2 = (X ** 2).sum(1)
    for a in range(0, len(X), block):
        Q = X[a:a + block]
        d2 = (Q ** 2).sum(1)[:, None] - 2.0 * Q @ X.T + x2[None, :]
        g = np.exp(-np.maximum(d2, 0.0) / (2.0 * sigma * sigma))
        out[a:a + block] = (g @ werte) / g.sum(1)[:, None]
    return out


class Netz:
    """Spielnetz 2c + Gewichte; Masken und Helfer."""

    def __init__(self):
        L = np.load(EIN + "lp_2c.npz")
        G = np.load(EIN + "gewichte_2c.npz")
        assert np.abs(L["V"] - G["V"]).max() == 0 and (L["T"] == G["T"]).all()
        self.V, self.T, self.UVT, self.gegend, self.sohle = L["V"], L["T"], L["UVT"], L["gegend"], L["sohle"]
        self.W = G["W"]
        self.namen = [str(n) for n in G["namen"]]
        self.kralle = G["kralle"]
        self.n = len(self.V)
        self.E, self.cnt = laplace_matrix(self.T, self.n)
        # Gewichte RAEUMLICH geglaettet (Gauss ueber die Lage im Urbild, 3 cm): Grundlage des Form-Felds. Die Haut-Gewichte selbst sind
        # nur entlang der Netzkanten glatt; in Achsel und Leiste liegen Splitter-Dreiecke (Hoehe ~1 mm), die ein Feld aus solchen
        # Gewichten umkippt (Runden 1-3: 8-30 umgekippte Dreiecke). Ein raeumlich glattes Feld ist oertlich fast starr.
        haut_ = ~self.kralle
        self.Ws = self.W.copy()
        self.Ws[haut_] = raum_glatt(self.V[haut_], self.W[haut_], SIGMA_W)
        self.Ws /= self.Ws.sum(1)[:, None]

    def w(self, *namen, W=None):
        W = self.W if W is None else W
        out = np.zeros(self.n)
        for nm in namen:
            for k, n in enumerate(self.namen):
                if n == "Bip01_" + nm or (nm.startswith("*") and n.endswith(nm[1:])):
                    out += W[:, k]
        return out

    def ws(self, *namen):
        return self.w(*namen, W=self.Ws)


def stufe1(sk, V, W, namen, kopf=S_KOPF):
    """Knochen-Stufe: v' = Summe w_k B'_k diag(S_k) B_k^-1 v (tier-Meter -> tier-Meter)."""
    Pd = dump(V)
    h = np.c_[Pd, np.ones(len(Pd))]
    out = np.zeros((len(Pd), 3))
    for k, nm in enumerate(namen):
        b = sk.idx[nm]
        kurz = nm.replace("Bip01_", "")
        if kurz in ("Pelvis", "Spine", "Spine1"):
            s = S_RUMPF
        elif kurz == "Tail":
            s = S_SCHWANZ
        elif kurz == "Head":
            s = kopf
        else:
            s = (1.0, 1.0, 1.0)
        M = sk.BW_j[b] @ np.diag((s[0], s[1], s[2], 1.0)) @ sk.inv_e[b]
        w = W[:, k]
        m = w > 0
        out[m] += w[m, None] * (h[m] @ M.T)[:, :3]
    return tier(out)


def schnitt(V, T, achse, wert, maske_t=None):
    """Schnitt des Netzes mit der Ebene V[:, achse] == wert: Strecken (n x 2 x 3). maske_t: nur diese Dreiecke."""
    Tm = T if maske_t is None else T[maske_t]
    d = V[Tm, achse] - wert
    s = d > 0
    gem = s.any(1) & ~s.all(1)
    Tm, d = Tm[gem], d[gem]
    out = []
    for a, b in ((0, 1), (1, 2), (2, 0)):
        kreuzt = (d[:, a] > 0) != (d[:, b] > 0)
        t = np.where(kreuzt, d[:, a] / np.where(kreuzt, d[:, a] - d[:, b], 1.0), np.nan)
        out.append(V[Tm[:, a]] + (V[Tm[:, b]] - V[Tm[:, a]]) * t[:, None])
    Pk = np.stack(out, 1)                                   # n x 3 x 3, je Dreieck zwei gueltige Punkte
    ok = ~np.isnan(Pk[:, :, 0])
    seg = np.zeros((len(Pk), 2, 3))
    for i in range(len(Pk)):
        seg[i] = Pk[i][ok[i]][:2]
    return seg


def linie(V, x, T=None, z_min=0.45, seg_mitte=None):
    """Ruecken (max z) und Bauch (min z) in der Mittelebene bei x; halbe Breite (max |y| ueber z_min) im Querschnitt x."""
    oben = unten = breit = np.nan
    if seg_mitte is not None and len(seg_mitte):
        a, b = seg_mitte[:, 0], seg_mitte[:, 1]
        m = ((a[:, 0] - x) * (b[:, 0] - x) <= 0) & (np.abs(a[:, 0] - b[:, 0]) > 1e-9)
        if m.any():
            t = (x - a[m, 0]) / (b[m, 0] - a[m, 0])
            z = a[m, 2] + (b[m, 2] - a[m, 2]) * t
            oben, unten = float(z.max()), float(z.min())
    if T is not None:
        sq = schnitt(V, T, 0, x)
        if len(sq):
            pts = sq.reshape(-1, 3)
            pts = pts[pts[:, 2] > z_min]
            if len(pts):
                breit = float(np.abs(pts[:, 1]).max())
    return oben, unten, breit


def profil(V, T, xs, maske_t=None, z_min=0.45):
    """Ruecken-, Bauchlinie (Mittelebene y = 0) und halbe Breite je x. maske_t: Dreiecke fuer die Mittelebene (z. B. nur Rumpf)."""
    seg = schnitt(V, T, 1, 0.0, maske_t)
    out = np.array([linie(V, x, T, z_min, seg) for x in xs])
    return out[:, 0], out[:, 1], out[:, 2]


def bein_breiten(V, T, wb, seite, zs):
    """Breite eines Beins von der Seite (x-Ausdehnung) und von vorn (y-Ausdehnung), Aussenkante |y| je Hoehe z (Schnitt z = const).
    wb: Gewicht der Beinkette je Punkt; gezaehlt werden Dreiecke mit mittlerem Gewicht >= 0,5 auf der Seite 'seite' (+1 links)."""
    mt = (wb[T].mean(1) >= 0.5) & (V[T, 1].mean(1) * seite > 0)
    out = []
    for z in zs:
        sq = schnitt(V, T, 2, z, mt)
        if len(sq) < 4:
            out.append((np.nan, np.nan, np.nan, np.nan, np.nan))
            continue
        pts = sq.reshape(-1, 3)
        out.append((float(np.ptp(pts[:, 0])), float(np.ptp(pts[:, 1])), float(np.abs(pts[:, 1]).max()), float(pts[:, 0].min()), float(pts[:, 0].max())))
    return np.array(out)


# Hintern im Seitenriss (B.2): hinterster Punkt x je Hoehe z
Z_HIN = np.array((0.42, 0.50, 0.58, 0.66, 0.75, 0.84, 0.94, 1.03, 1.08, 1.115))
X_HIN = np.array((-0.62, -0.70, -0.730, -0.74, -0.732, -0.70, -0.655, -0.60, -0.555, -0.50))

PARAM = dict(
    glatt=12,            # Glaett-Runden der Verschiebung (Stufe 2)
    hintern_x0=-0.36,    # ab hier nach hinten wird der Hintern in x gestreckt (auf X_HIN je Hoehe)
    zc=0.74,             # Hoehe der Rumpf-Mittellinie fuer die Hoehen-Abbildung (bleibt fest)
    bein_aussen=1.0,     # Anteil der Aussenkanten-Korrektur der Beine (B.3)
    geo=(30, 15),        # Geometrie-Glaetten des Rumpfs: Taubin-Runden je Durchgang (danach jeweils neu auf die Tabellen)
    geo_lam=0.6, geo_plain=6,
    glatt_z0=0.34, glatt_z1=0.50,   # Oberbeine: ab hier nimmt das Geometrie-Glaetten zu (Ellbogen-/Bauch-Behang des Erwachsenen weich)
    bein_glatt=0.35,     # leichtes Glaetten der Unterbeine ab z 0,20 (Ring der Fellhuelle bei z ~0,33)
    bein_nach=2,         # Durchgaenge Bein-Tabellen nach dem Rumpf-Glaetten
    nach_runden=2,
    schwanz_glatt=40, schwanz_z=0.70, schwanz_h=0.045, schwanz_sigma=0.055,   # Schwanz-Knubbel (B.4)
)


def stufe2(nz, sk, P1, par=PARAM, info=None):
    """Form-Stufe auf dem Spielnetz. Alle Masken aus den RAEUMLICH geglaetteten Gewichten. Rueckgabe: P2 (tier-Meter)."""
    info = info if info is not None else {}
    P = P1.copy()
    V0 = nz.V
    wV = {s: nz.ws(s + "_Forearm", s + "_Hand") for s in "LR"}
    wVo = {s: nz.ws(s + "_UpperArm") for s in "LR"}
    wH = {s: nz.ws(s + "_Calf", s + "_Foot") for s in "LR"}
    wHo = {s: nz.ws(s + "_Thigh") for s in "LR"}
    w_rumpf = nz.ws("Pelvis", "Spine", "Spine1", "Tail")
    w_kopf = nz.ws("Head", "Neck")
    D = np.zeros_like(P)
    # ---- (a) Pfoten breiter: unter z 0,10 um die Pfoten-Mittellinie in y, Uebergang bis z 0,18; x und z unveraendert (B.4)
    for s, sg in (("L", 1.0), ("R", -1.0)):
        for art, wb, wo, f in (("V", wV[s], wVo[s], PFOTE_V_BREIT), ("H", wH[s], wHo[s], PFOTE_H_BREIT)):
            m = (wb + wo >= 0.5) & (P[:, 1] * sg > 0) & ~nz.kralle
            sohle = m & (P[:, 2] < 0.03)
            ym = float((P[sohle, 1].max() + P[sohle, 1].min()) / 2)
            g = 1.0 - sst(0.10, 0.18, P[:, 2])
            D[m, 1] += ((P[m, 1] - ym) * (f - 1.0) * g[m])
    # ---- (b) Krallen: starr mit ihrer Wurzel mit, dann x 0,75 um die Wurzel (B.4)
    sch = schalen(nz.T, nz.n)
    haupt = np.bincount(sch).argmax()
    n_kr = 0
    for c in np.unique(sch):
        if c == haupt:
            continue
        idx = np.where(sch == c)[0]
        ordn = idx[np.argsort(P[idx, 0])]
        wz = ordn[:max(3, len(ordn) // 4)]              # Wurzel = hinteres Viertel (die Krallen zeigen in der Ruhe nach vorn-unten)
        wurzel = P[wz].mean(0)
        haut_idx = np.where((sch == haupt) & (np.abs(P[:, 0] - wurzel[0]) < 0.06) & (np.abs(P[:, 1] - wurzel[1]) < 0.06) & (P[:, 2] < 0.12))[0]
        j = haut_idx[np.argmin(np.linalg.norm(P[haut_idx] - wurzel, axis=1))]
        D[idx] = D[j] + (P[idx] - wurzel) * (KRALLE_F - 1.0)
        n_kr += 1
    info["krallen"] = n_kr
    P = P + D
    fest_kralle = sch != haupt
    # ---- Masken
    m_bein = np.zeros(nz.n)
    for s in "LR":
        m_bein += (wV[s] + wVo[s] + wH[s] + wHo[s])
    # Beine machen den Bauch-Hub nach der HOEHE mit (z 0,24..0,42), nicht nach dem Gewicht: sonst reisst der Hub die Kehle zwischen
    # Brustboden (voll gehoben) und Bein-Innenwand (nicht gehoben) auf
    mk = np.clip(w_rumpf + m_bein * sst(0.24, 0.42, P[:, 2]) + w_kopf * (1.0 - sst(0.47, 0.60, P[:, 0])), 0.0, 1.0)
    mk[fest_kralle] = 0.0
    mg = np.clip(3.0 * w_rumpf, 0.0, 1.0) + nz.ws("Neck") * (1.0 - sst(0.50, 0.62, P[:, 0])) + m_bein * sst(par["glatt_z0"], par["glatt_z1"], P[:, 2])
    mg = np.maximum(mg, par["bein_glatt"] * m_bein * sst(0.18, 0.24, P[:, 2]))
    mg = np.clip(mg, 0.0, 1.0)
    mg[nz.ws("Head") > 0.5] = 0.0
    mg[fest_kralle] = 0.0
    info["rumpf"] = []
    # ---- (c) Schwanz einschmelzen (der Hoecker kommt am Ende), Beine und Rumpf auf die Tabellen, dazwischen Geometrie glaetten
    P = schwanz_schmelzen(P, nz, par)
    P = bein_fit(P, nz, sk, par, info, wV, wVo, wH, wHo, fest_kralle)
    P = rumpf_fit(P, nz, mk, par, info)
    for r, n_gl in enumerate(par["geo"]):
        for _ in range(par["geo_plain"]):        # ein paar einfache Laplace-Schritte (nehmen auch lange Wellen), dann Taubin
            acc = np.zeros_like(P)
            np.add.at(acc, nz.E[:, 0], P[nz.E[:, 1]])
            P = P + (0.5 * mg)[:, None] * (acc / nz.cnt[:, None] - P)
        P = geo_glatt(P, nz, mg, n_gl, par["geo_lam"])
        P = rumpf_fit(P, nz, mk, par, info)
        for _ in range(par["bein_nach"]):
            P = bein_fit(P, nz, sk, par, info, wV, wVo, wH, wHo, fest_kralle)
    for _ in range(par["nach_runden"]):
        P = rumpf_fit(P, nz, mk, par, info)
        P = bein_fit(P, nz, sk, par, info, wV, wVo, wH, wHo, fest_kralle)
    # ---- (d) Schwanz-Hoecker
    P = schwanz_hoecker(P, nz, par, info)
    # ---- (e) umgekippte Dreiecke lokal entspannen (sollte nach dem raeumlich glatten Feld kaum noch etwas finden)
    P, n_vor, n_nach = entkippen(P, V0, nz, fest_kralle)
    info["umgekippt_vor"] = n_vor
    info["entkippen_frei"] = getattr(entkippen, "frei", 0)
    info["entkippen_splitter"] = getattr(entkippen, "splitter", 0)
    info["umgekippt"] = n_nach
    return P


def bein_fit(P, nz, sk, par, info, wV, wVo, wH, wHo, fest_kralle):
    """Bein-Dicke (von der Seite / von vorn) und Aussenkante auf die Tabellen B.3; ein Durchgang."""
    D = np.zeros_like(P)
    for s, sg in (("L", 1.0), ("R", -1.0)):
        for art, wb, wo, soll_s, soll_v, soll_a, a_nm, b_nm in (
                ("V", wV[s], wVo[s], V_SEITE, V_VORN, V_AUSSEN, s + "_Hand", s + "_Forearm"),
                ("H", wH[s], wHo[s], H_SEITE, H_VORN, H_AUSSEN, s + "_Foot", s + "_Calf")):
            wk = wb + wo
            ist = bein_breiten(P, nz.T, wk, sg, Z_BEIN)
            fs = np.clip(np.where(np.isnan(ist[:, 0]), 1.0, soll_s / ist[:, 0]), 0.85, 1.30)
            fv = np.clip(np.where(np.isnan(ist[:, 1]) | np.isnan(soll_v), 1.0, soll_v / ist[:, 1]), 0.85, 1.30)
            zk = np.concatenate(((0.0, 0.09), Z_BEIN, (0.56, 2.0)))
            fsk = np.concatenate(((1.0, 1.0), fs, (1.0, 1.0)))
            fvk = np.concatenate(((1.0, 1.0), fv, (1.0, 1.0)))
            pa, pb = sk.gelenk_j(a_nm), sk.gelenk_j(b_nm)
            t = np.clip((P[:, 2] - pa[2]) / (pb[2] - pa[2]), 0.0, 1.0)
            # Mittellinie des Beins = Mitte des gemessenen Schnitts waere genauer; die Knochenlinie reicht (Bein sitzt mittig um den Knochen)
            cx = pa[0] + (pb[0] - pa[0]) * t
            cy = pa[1] + (pb[1] - pa[1]) * t
            m = (wk > 0) & (P[:, 1] * sg > 0) & ~fest_kralle
            gx = np.interp(P[:, 2], zk, fsk) - 1.0
            gy = np.interp(P[:, 2], zk, fvk) - 1.0
            D[m, 0] += (P[m, 0] - cx[m]) * gx[m] * wk[m]
            D[m, 1] += (P[m, 1] - cy[m]) * gy[m] * wk[m]
            # Aussenkante nach dem Skalieren: aussen' = cy + (aussen - cy) * fv
            cyz = np.interp(Z_BEIN, [pa[2], pb[2]], [abs(pa[1]), abs(pb[1])])
            aus_neu = cyz + (ist[:, 2] - cyz) * fv
            dy = np.where(np.isnan(ist[:, 2]), 0.0, soll_a - aus_neu) * par["bein_aussen"]
            zk2 = np.concatenate(((0.0, 0.10), Z_BEIN, (0.50, 0.62, 2.0)))
            dk = np.concatenate(((0.0, 0.0), dy, (dy[-1], 0.0, 0.0)))
            D[m, 1] += sg * np.interp(P[m, 2], zk2, dk) * wk[m]
            if art == "H":
                # Hinterkante des Hinterbeins (B.3: z 0,20-0,40 bei x -0,545..-0,56): nach dem Skalieren um die Knochenlinie verschieben
                cxz = np.interp(Z_BEIN, [pa[2], pb[2]], [pa[0], pb[0]])
                hin_neu = cxz + (ist[:, 3] - cxz) * fs
                dx = np.where(np.isnan(ist[:, 3]), 0.0, H_HINTEN - hin_neu)
                dkx = np.concatenate(((0.0, 0.0), dx, (dx[-1] * 0.5, 0.0, 0.0)))
                D[m, 0] += np.interp(P[m, 2], zk2, dkx) * wk[m]
    D = glaetten(D, nz.E, nz.cnt, 5, 0.5, fest=fest_kralle)
    return P + D


def schwanz_schmelzen(P, nz, par):
    wt = nz.ws("Tail")
    m = np.clip(wt * 3.0, 0.0, 1.0)
    m[nz.kralle] = 0.0
    P = P.copy()
    for _ in range(par["schwanz_glatt"]):
        acc = np.zeros_like(P)
        np.add.at(acc, nz.E[:, 0], P[nz.E[:, 1]])
        P = P + (0.6 * m)[:, None] * (acc / nz.cnt[:, None] - P)
    return P


def schwanz_hoecker(P, nz, par, info):
    """Weicher Hoecker (Gauss) an der hintersten Stelle der Mittelebene bei z = schwanz_z, entlang -x."""
    P = P.copy()
    zc_, h, sig = par["schwanz_z"], par["schwanz_h"], par["schwanz_sigma"]
    nahe = (np.abs(P[:, 1]) < 0.04) & (np.abs(P[:, 2] - zc_) < 0.04) & (P[:, 0] < -0.5)
    c = np.array((float(P[nahe, 0].min()), 0.0, zc_))
    d2 = ((P[:, 1] - c[1]) ** 2 + (P[:, 2] - c[2]) ** 2)
    g = np.exp(-d2 / (sig * sig)) * (P[:, 0] < -0.5)
    P[:, 0] -= h * g
    info["schwanz"] = dict(mitte=[round(float(v), 4) for v in c], hoehe=h, sigma=sig)
    return P


def entkippen(P, V_erw, nz, fest, runden=40, radius=0.05):
    """Umgekippte Dreiecke (Normale gegen das Urbild um > 90 Grad) beseitigen: um jedes umgekippte Dreieck wird die VERSCHIEBUNG
    gegen das Urbild RAEUMLICH geglaettet (Gauss-Mittel ueber die Lage im Urbild, Breite 'radius'), bis nichts mehr umgekippt ist.
    Raeumlich glatt = oertlich fast starr = die Stelle behaelt die Form des Erwachsenen (dort: die Kehle zwischen Brustboden und
    Vorderbein, lauter Dreiecke von 0,4-1,3 cm2). Ein Glaetten ueber die Netzkanten hilft dort nicht: Netz-Nachbarn liegen in der Kehle
    ~1 mm auseinander und duerfen sich kaum gegeneinander verschieben."""
    T = nz.T
    na = np.cross(V_erw[T[:, 1]] - V_erw[T[:, 0]], V_erw[T[:, 2]] - V_erw[T[:, 0]])

    def schlecht(X):
        nj = np.cross(X[T[:, 1]] - X[T[:, 0]], X[T[:, 2]] - X[T[:, 0]])
        return (na * nj).sum(1) < 0
    D = P - V_erw
    n_vor = int(schlecht(P).sum())
    quelle = np.where(~fest)[0]
    Q = V_erw[quelle]
    q2 = (Q ** 2).sum(1)
    k_ges = np.zeros(nz.n)
    r_ = 0
    for r_ in range(runden):
        b = np.where(schlecht(V_erw + D))[0]
        if not len(b):
            break
        C = V_erw[T[b]].mean(1)                                  # Mitten der umgekippten Dreiecke (Urbild)
        d2 = ((Q[:, None, :] - C[None, :, :]) ** 2).sum(2).min(1)
        k = np.exp(-d2 / (2.0 * (1.6 * radius) ** 2))
        nah = k > 0.02
        X = Q[nah]
        dd = (X ** 2).sum(1)[:, None] - 2.0 * X @ Q.T + q2[None, :]
        g = np.exp(-np.maximum(dd, 0.0) / (2.0 * radius * radius))
        Ds = (g @ D[quelle]) / g.sum(1)[:, None]
        i = quelle[nah]
        D[i] = D[i] + k[nah, None] * (Ds - D[i])
        k_ges[i] = np.maximum(k_ges[i], k[nah])
    entkippen.frei = int((k_ges > 0.5).sum())
    entkippen.splitter = r_
    return V_erw + D, n_vor, int(schlecht(V_erw + D).sum())


def geo_glatt(P, nz, m, runden, lam=0.5):
    """Glaettet die GEOMETRIE (nicht nur die Verschiebung) dort, wo m > 0 (Taubin: abwechselnd +lam / -mu, schrumpft kaum)."""
    P = P.copy()
    mu = -lam * 1.02
    for i in range(runden * 2):
        acc = np.zeros_like(P)
        np.add.at(acc, nz.E[:, 0], P[nz.E[:, 1]])
        f = lam if i % 2 == 0 else mu
        P = P + (f * m)[:, None] * (acc / nz.cnt[:, None] - P)
    return P


def rumpf_fit(P, nz, mk, par, info, hintern=True):
    """Rumpf auf die Soll-Tabellen B.2: Hintern (hinterster Punkt x je Hoehe z), Ruecken z, Bauch z, halbe Breite je x."""
    fest_kralle = nz.kralle
    D = np.zeros_like(P)
    x0 = par["hintern_x0"]
    zs = np.linspace(0.40, 1.13, 24)
    xe = np.full(len(zs), np.nan)
    sel0 = (mk > 0.5) & (P[:, 0] < x0)
    for i, z_ in enumerate(zs):
        m_ = sel0 & (np.abs(P[:, 2] - z_) < 0.03)
        if m_.sum() >= 3:
            xe[i] = P[m_, 0].min()
    ok = ~np.isnan(xe)
    xe = np.interp(zs, zs[ok], xe[ok])
    kz = np.clip((np.interp(zs, Z_HIN, X_HIN) - x0) / (xe - x0), 0.6, 1.6)
    kz = np.convolve(np.pad(kz, 2, mode="edge"), np.array((1, 2, 3, 2, 1.0)) / 9.0, mode="valid")
    hin = P[:, 0] < x0
    D[hin, 0] = (P[hin, 0] - x0) * (np.interp(P[hin, 2], zs, kz) - 1.0) * mk[hin] * sst(0.36, 0.46, P[hin, 2])   # nur ueber der Gesaessfalte
    x_end, k = float(xe.min()), float(kz.mean())
    Pm = P + D
    xs = np.linspace(-0.76, 0.62, 70)
    zt, zb, yh = profil(Pm, nz.T, xs)
    zc = par["zc"]

    def fuell(a):
        a = np.array(a, float)
        ok = ~np.isnan(a)
        return np.interp(xs, xs[ok], a[ok])
    zt, zb2, yh = fuell(zt), fuell(zb), fuell(yh)
    kern = np.array((1, 2, 3, 2, 1.0))
    kern /= kern.sum()

    def gl(a):
        return np.convolve(np.pad(a, 2, mode="edge"), kern, mode="valid")
    zt, zb2, yh = gl(zt), gl(zb2), gl(yh)
    zt_s = np.interp(xs, X_RUE, Z_RUE)
    zb_s = np.interp(xs, X_BAU, Z_BAU)
    yh_s = np.interp(xs, X_BRE, Y_BRE)
    g_o = sst(-0.64, -0.52, xs) * (1.0 - sst(0.47, 0.60, xs))      # hinter x -0,52 formt der Hintern-Riss (X_HIN je Hoehe)
    g_u = sst(-0.56, -0.44, xs) * (1.0 - sst(0.38, 0.50, xs))
    g_b = sst(-0.70, -0.58, xs) * (1.0 - sst(0.47, 0.60, xs))
    s_o = np.clip(1.0 + ((zt_s - zc) / np.maximum(zt - zc, 0.05) - 1.0) * g_o, 0.3, 1.8)
    s_u = np.clip(1.0 + ((zc - zb_s) / np.maximum(zc - zb2, 0.05) - 1.0) * g_u, 0.3, 1.8)
    s_y = np.clip(1.0 + (yh_s / np.maximum(yh, 0.05) - 1.0) * g_b, 0.5, 1.6)
    info["rumpf"].append(dict(x_ende_vor=round(float(x_end), 4), k=round(float(k), 4), s_oben=[round(float(s_o.min()), 3), round(float(s_o.max()), 3)],
                              s_unten=[round(float(s_u.min()), 3), round(float(s_u.max()), 3)], s_breite=[round(float(s_y.min()), 3), round(float(s_y.max()), 3)]))
    so = np.interp(Pm[:, 0], xs, s_o)
    su = np.interp(Pm[:, 0], xs, s_u)
    sy = np.interp(Pm[:, 0], xs, s_y)
    dzc = Pm[:, 2] - zc
    zz = np.linspace(-0.6, 0.6, 241)
    uu = sst(-0.10, 0.10, zz)
    iu = np.concatenate(((0.0,), np.cumsum((uu[1:] + uu[:-1]) / 2 * np.diff(zz))))
    iu -= np.interp(0.0, zz, iu)
    Iu = np.interp(dzc, zz, iu)
    neu_dz = su * (dzc - Iu) + so * Iu
    D[:, 2] += (neu_dz - dzc) * mk
    D[:, 1] += Pm[:, 1] * (sy - 1.0) * mk
    D = glaetten(D, nz.E, nz.cnt, par["glatt"], 0.5, fest=fest_kralle)
    return P + D


def umgekippt(V_erw, V, T):
    na = np.cross(V_erw[T[:, 1]] - V_erw[T[:, 0]], V_erw[T[:, 2]] - V_erw[T[:, 0]])
    nj = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    return ((na * nj).sum(1) < 0).sum()


def mass(V, nz, sk):
    """Masse B.1-B.3 (Meter)."""
    out = {}
    koerper = nz.w("Head") < 0.5
    # Rumpfende ohne den Schwanz-Hoecker: der Hoecker ist ein bekannter Gauss entlang -x (schwanz_hoecker), er wird herausgerechnet
    g_h = np.exp(-(V[:, 1] ** 2 + (V[:, 2] - PARAM["schwanz_z"]) ** 2) / PARAM["schwanz_sigma"] ** 2) * (V[:, 0] < -0.5)
    x_ohne = V[:, 0] + PARAM["schwanz_h"] * g_h
    out["L"] = float(V[:, 0].max() - x_ohne.min())
    out["nase_x"] = float(V[:, 0].max())
    out["rumpfende_x"] = float(x_ohne.min())
    out["rumpfende_z"] = float(V[int(np.argmin(x_ohne)), 2])
    out["schwanz_sichtbar"] = float(x_ohne.min() - V[:, 0].min())
    zt, zb, yh = profil(V, nz.T, X_RUE)
    out["ruecken"] = dict(x=X_RUE.tolist(), ist=np.round(zt, 3).tolist(), soll=Z_RUE.tolist())
    zt2, zb2, _ = profil(V, nz.T, X_BAU)
    out["bauch"] = dict(x=X_BAU.tolist(), ist=np.round(zb2, 3).tolist(), soll=Z_BAU.tolist())
    _, _, yb = profil(V, nz.T, X_BRE)
    out["halbe_breite"] = dict(x=X_BRE.tolist(), ist=np.round(yb, 3).tolist(), soll=Y_BRE.tolist())
    _sm = schnitt(V, nz.T, 1, 0.0)
    out["H_schulter"] = linie(V, 0.23, None, 0.45, _sm)[0]
    out["kruppe"] = linie(V, -0.42, None, 0.45, _sm)[0]
    out["ruecken_mitte"] = max(linie(V, x_, None, 0.45, _sm)[0] for x_ in (-0.10, -0.05, 0.0))
    out["bauch_tief"] = float(np.nanmin(zb2))
    out["rumpftiefe_mitte"] = linie(V, -0.05, None, 0.45, _sm)[0] - linie(V, -0.05, None, 0.45, _sm)[1]
    for nm, x0, x1 in (("breite_hueften", -0.55, -0.30), ("breite_bauch", -0.15, 0.05), ("breite_schultern", 0.12, 0.34)):
        m = (V[:, 0] > x0) & (V[:, 0] < x1) & (V[:, 2] > 0.45)
        out[nm] = float(V[m, 1].max() - V[m, 1].min())
    m = (np.abs(V[:, 0] - 0.47) < 0.03) & (V[:, 2] > 0.5)
    out["hals_breite_x047"] = float(V[m, 1].max() - V[m, 1].min())
    m = nz.w("Head") >= 0.5
    out["kopf_breite"] = float(V[m, 1].max() - V[m, 1].min())
    out["kopf_oben"] = float(V[m, 2].max())
    out["hoehe_gesamt"] = float(V[koerper, 2].max())
    for s, sg in (("L", 1.0),):
        wv = nz.w(s + "_Forearm", s + "_Hand", s + "_UpperArm")
        wh = nz.w(s + "_Calf", s + "_Foot", s + "_Thigh")
        bv, bh = bein_breiten(V, nz.T, wv, sg, Z_BEIN), bein_breiten(V, nz.T, wh, sg, Z_BEIN)
        out["bein_vorn"] = dict(z=Z_BEIN.tolist(), seite=bv[:, 0].round(3).tolist(), vorn=bv[:, 1].round(3).tolist(), aussen=bv[:, 2].round(3).tolist(),
                                soll_seite=V_SEITE.tolist(), soll_vorn=[None if np.isnan(v) else v for v in V_VORN])
        out["bein_hinten"] = dict(z=Z_BEIN.tolist(), seite=bh[:, 0].round(3).tolist(), vorn=bh[:, 1].round(3).tolist(), aussen=bh[:, 2].round(3).tolist(), hinten=bh[:, 3].round(3).tolist(),
                                  soll_seite=H_SEITE.tolist(), soll_vorn=[None if np.isnan(v) else v for v in H_VORN])
        mv = (nz.w(s + "_Hand") >= 0.5) & ~nz.kralle & (V[:, 2] < 0.10)
        mh = (nz.w(s + "_Foot") >= 0.5) & ~nz.kralle & (V[:, 2] < 0.10)
        out["pranke_vorn_breite"] = float(np.ptp(V[mv, 1]))
        out["fuss_hinten_breite"] = float(np.ptp(V[mh, 1]))
        out["fuss_hinten_laenge"] = float(np.ptp(V[mh, 0]))
        out["pfote_tiefst"] = dict(vorn=float(V[mv, 2].min()), hinten=float(V[mh, 2].min()))
    return out


def huelle_gewichte(S_erw, nz, k=8, block=4000):
    """Gewichte der dichten Huelle aus den k naechsten Spielnetz-Punkten (wie feld_zurueck, baer_textur_2c.py:1009); ohne scipy."""
    Vn = nz.V
    idx = np.zeros((len(S_erw), k), int)
    gew = np.zeros((len(S_erw), k))
    v2 = (Vn ** 2).sum(1)
    for a in range(0, len(S_erw), block):
        Q = S_erw[a:a + block]
        d2 = (Q ** 2).sum(1)[:, None] - 2.0 * Q @ Vn.T + v2[None, :]
        i = np.argpartition(d2, k, axis=1)[:, :k]
        d = np.sqrt(np.maximum(np.take_along_axis(d2, i, 1), 1e-12))
        g = 1.0 / np.maximum(d, 1e-6) ** 2
        idx[a:a + block] = i
        gew[a:a + block] = g / g.sum(1)[:, None]
    return idx, gew


def bauen(aus=ARB + "koerper/", par=PARAM):
    os.makedirs(aus, exist_ok=True)
    sk = Skelett()
    nz = Netz()
    info = {}
    P1 = stufe1(sk, nz.V, nz.Ws, nz.namen)
    P2 = stufe2(nz, sk, P1, par, info)
    # Boden: Sohlen bleiben, wo sie sind (x, z unveraendert unter z 0,10); nichts unter z = 0
    info["z_min"] = float(P2[:, 2].min())
    np.savez(aus + "lp_junges.npz", V=P2, T=nz.T, UVT=nz.UVT, gegend=nz.gegend, sohle=nz.sohle, V_erw=nz.V, V_stufe1=P1)
    # dichte Huelle: Verschiebung der 8 naechsten Spielnetz-Punkte (Verschiebungsfeld des Spielnetzes ist glatt)
    Z = np.load(EIN + "form2c_feld_2c.npz")
    S_erw = Z["S"].astype(np.float64)
    if os.environ.get("NCB_JUNGES_HUELLE", "1") != "0":
        i, g = huelle_gewichte(S_erw, nz)
        dS = ((P2 - nz.V)[i] * g[:, :, None]).sum(1)
        np.savez(aus + "huelle_junges.npz", S_junges=(S_erw + dS).astype(np.float32), S_erw=Z["S"], T=Z["T"])
        info["huelle"] = dict(punkte=int(len(S_erw)), verschiebung_max=float(np.linalg.norm(dS, axis=1).max()))
    ms = mass(P2, nz, sk)
    json.dump(dict(info=info, mass=ms), open(aus + "mass.json", "w"), indent=1)
    skj = dict(faktoren=dict(rumpf=F_RUMPF, beine=F_BEIN, pfoten=F_PFOTE, hals=F_HALS, kiefergelenk=F_KIEFER, dx_m=DX),
               namen=sk.names, eltern=sk.par,
               lage_E={nm: sk.t_j[b].round(6).tolist() for b, nm in enumerate(sk.names)},
               lage_E_erw={nm: sk.t_e[b].round(6).tolist() for b, nm in enumerate(sk.names)},
               ruhe_m={nm: tier(sk.BW_j[b][:3, 3]).round(4).tolist() for b, nm in enumerate(sk.names)},
               ruhe_m_erw={nm: tier(sk.BW_e[b][:3, 3]).round(4).tolist() for b, nm in enumerate(sk.names)})
    json.dump(skj, open(aus + "skelett.json", "w"), indent=1)
    return sk, nz, P1, P2, info, ms


def drucke(ms, info=None):
    if info:
        print("FORM umgekippt", info.get("umgekippt"), "(vor dem Entspannen", info.get("umgekippt_vor"), ", frei", info.get("entkippen_frei"), "Punkte, Runden", info.get("entkippen_splitter"), ") | Schwanz", info.get("schwanz"), "| Krallen", info.get("krallen"), "| z_min %.4f" % info.get("z_min", 0),
              "| Huelle", info.get("huelle"))
    print("MASS L %.3f (Soll 1,85) | Nase x %.3f (1,10) | Rumpfende x %.3f (-0,74) | Schwanz sichtbar %.3f (<= 0,06)" % (ms["L"], ms["nase_x"], ms["rumpfende_x"], ms["schwanz_sichtbar"]))
    print("MASS H Schulter %.3f (1,143) | Kruppe %.3f (1,143) | Ruecken Mitte %.3f (1,150) | Bauch tief %.3f (0,400) | Rumpftiefe %.3f (0,750)" % (
        ms["H_schulter"], ms["kruppe"], ms["ruecken_mitte"], ms["bauch_tief"], ms["rumpftiefe_mitte"]))
    print("MASS Breite Hueften %.3f (0,67) | Bauch %.3f (0,64) | Schultern %.3f (0,635) | Hals x0,47 %.3f (0,45) | Kopf %.3f (0,56) | Kopf oben %.3f (0,955)" % (
        ms["breite_hueften"], ms["breite_bauch"], ms["breite_schultern"], ms["hals_breite_x047"], ms["kopf_breite"], ms["kopf_oben"]))
    for k in ("ruecken", "bauch", "halbe_breite"):
        print("MASS %-12s x   " % k, " ".join("%6.2f" % v for v in ms[k]["x"]))
        print("MASS %-12s ist " % k, " ".join("%6.3f" % v for v in ms[k]["ist"]))
        print("MASS %-12s soll" % k, " ".join("%6.3f" % v for v in ms[k]["soll"]))
    for k in ("bein_vorn", "bein_hinten"):
        b = ms[k]
        print("MASS %-11s z     " % k, " ".join("%6.2f" % v for v in b["z"]))
        print("MASS %-11s Seite " % k, " ".join("%6.3f" % v for v in b["seite"]), "| Soll", " ".join("%.3f" % v for v in b["soll_seite"]))
        print("MASS %-11s vorn  " % k, " ".join("%6.3f" % v for v in b["vorn"]), "| Soll", " ".join("%s" % v for v in b["soll_vorn"]))
        print("MASS %-11s aussen" % k, " ".join("%6.3f" % v for v in b["aussen"]), ("| Hinterkante x " + " ".join("%6.3f" % v for v in b["hinten"]) + " (Soll -0,545..-0,56 bei z 0,20-0,40)") if "hinten" in b else "")
    print("MASS Pranke vorn breit %.3f (0,228) | Hinterfuss breit %.3f (0,212) lang %.3f (0,29) | Pfote tiefst %s" % (
        ms["pranke_vorn_breite"], ms["fuss_hinten_breite"], ms["fuss_hinten_laenge"], ms["pfote_tiefst"]))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "bauen":
        _sk, _nz, _P1, _P2, _info, _ms = bauen(sys.argv[2] if len(sys.argv) > 2 else ARB + "koerper/")
        print("SKELETT Ruhe Junges (m):", {k.replace("Bip01_", ""): [round(float(v), 3) for v in tier(_sk.BW_j[b][:3, 3])] for b, k in enumerate(_sk.names) if "R_" not in k})
        print("STUFE1:")
        drucke(mass(_P1, _nz, _sk))
        print("STUFE2:")
        drucke(_ms, _info)
    elif len(sys.argv) > 2 and sys.argv[1] == "mass":
        _sk, _nz = Skelett(), Netz()
        drucke(mass(np.load(sys.argv[2])["V"], _nz, _sk))
