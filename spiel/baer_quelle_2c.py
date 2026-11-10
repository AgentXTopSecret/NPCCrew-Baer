# Lauf baer-2c (10.11.2026, Bau Koerper): Kopie von baer_quelle_pfote.py (Original unveraendert). Ausgaben nach _arbeit/baer_2c/hoch/.
# Aenderungen mit "2c" kommentiert: Hinterfuss kurz und rund (SPEZ_2C.md 4), Hinterkrallen -0,070 in x. Statisch gebaut, nicht gespielt.
# Lauf baer-pfoten (09.11.2026): Kopie von baer_quelle_anim.py (Original bleibt). Kevin: "das soll natuerlich nur eine richtige
# baerenpfote sein". Neu: (1) Unterschenkel/Unterarm der Metaballs unten duenner und nach hinten (nur die unteren drei Kugeln je
# Bein, darueber unveraendert), Fuss-/Pranken-Ketten weg; (2) je Pfote EIN Abstandsfeld (pf_feld_s: Bein, Fuss mit Ferse/Rist/
# flacher Sohle, fuenf Zehen, vorn Handwurzelballen) als Netz 'pfote_<Knochen>' statt 'zehen_<Knochen>'; (3) Krallen wie bisher,
# vorn nach K1 in y zur Mittelkralle; (4) Fell: Pfotenhaar auf dem Fuss, Sohle/Ballen nackt; pfoten_abstand statt zehen_abstand.
# Kopf unveraendert. Ausgaben nach _arbeit/baer_pfote/hoch/. Statisch gebaut, nicht gespielt.
# Vorgaenger: Kopie von baer_quelle.py fuer den Lauf baer-anim (Original bleibt). Einzige Aenderung: eine geglaettete Fassung der
# Rumpfhaut ('baer_koerper_rund' = 'baer_koerper' mit zwei Stufen Catmull-Clark, unsichtbar im Render) fuer das Spielnetz
# in baer_export_anim.py. Das Hochmodell (Fell, Rig, Kopf, Pfoten) ist unveraendert.
# Baer, Bauweise C: Koerper aus Metabaellen, Kopf/Nase/Lider/Zehen aus eigenem Abstandsfeld, Krallen als Rohre,
# Kopffell als Haar-Curves mit Strich aus dem Feld. Skelett, Gehzyklus, Hieb wie im Ausgangsskript.
# Aufruf: blender --background --factory-startup --python baer_c.py -- form|kopf|ende|still|anim
import math
import os
import random
import sys
import time

import bmesh
import bpy
import numpy as np
from mathutils import Euler, Matrix, Quaternion, Vector

OUT = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_2c/hoch/"
MODE = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "still"
random.seed(3)
RNG = np.random.default_rng(7)
T_START = time.time()

# ------------------------------------------------------------------ Kopf als Abstandsfeld (numpy, ohne bpy)
PITCH = math.radians(15.0)
LZ_HUB = 0.20  # Spielmodell: Beine kuerzer als im Entwurf (0.33), Schulter sonst zu hoch
HO = np.array((0.925, 0.0, 1.085 - (0.33 - LZ_HUB)))
HA = np.array((math.cos(PITCH), 0.0, -math.sin(PITCH)))
HB = np.array((0.0, 1.0, 0.0))
HC = np.array((math.sin(PITCH), 0.0, math.cos(PITCH)))


KOPF_SK = 1.17


SN_X0, SN_W, SN_S = 0.23, 0.09, 0.22  # Schnauze: ab x0 weich um den Anteil s gestaucht
_SN_X = np.linspace(-1.0, 1.0, 4001)
_SN_G = np.where(_SN_X < SN_X0, 0.0, np.where(_SN_X < SN_X0 + SN_W, (_SN_X - SN_X0) ** 2 / (2 * SN_W), _SN_X - SN_X0 - SN_W / 2))
_SN_Y = _SN_X - SN_S * _SN_G


def _sn(x):
    return np.interp(x, _SN_X, _SN_Y)


def _sn_inv(y):
    return np.interp(y, _SN_Y, _SN_X)


def l2w(P):
    P = np.asarray(P, dtype=float)
    return HO + (_sn(P[..., 0]) * KOPF_SK)[..., None] * HA + (P[..., 1] * KOPF_SK)[..., None] * HB + (P[..., 2] * KOPF_SK)[..., None] * HC


def w2l(W):
    D = np.asarray(W, dtype=float) - HO
    return np.stack((_sn_inv((D @ HA) / KOPF_SK), (D @ HB) / KOPF_SK, (D @ HC) / KOPF_SK), -1)


# ------------------------------------------------------------------ Grundformen
def sst(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def mixf(a, b, t):
    return a + (b - a) * t


def smin(d1, d2, k):
    h = np.clip(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0)
    return d2 + (d1 - d2) * h - k * h * (1.0 - h)


def smax(d1, d2, k):
    return -smin(-d1, -d2, k)


def ell(a, b, c, C, R):
    x, y, z = (a - C[0]) / R[0], (b - C[1]) / R[1], (c - C[2]) / R[2]
    k0 = np.sqrt(x * x + y * y + z * z)
    k1 = np.sqrt((x / R[0]) ** 2 + (y / R[1]) ** 2 + (z / R[2]) ** 2)
    return np.where(k0 < 1e-3, -min(R), k0 * (k0 - 1.0) / np.maximum(k1, 1e-5))


def cap(a, b, c, P0, P1, r0, r1=None):
    r1 = r0 if r1 is None else r1
    bx, by, bz = P1[0] - P0[0], P1[1] - P0[1], P1[2] - P0[2]
    px, py, pz = a - P0[0], b - P0[1], c - P0[2]
    h = np.clip((px * bx + py * by + pz * bz) / (bx * bx + by * by + bz * bz), 0.0, 1.0)
    dx, dy, dz = px - bx * h, py - by * h, pz - bz * h
    return np.sqrt(dx * dx + dy * dy + dz * dz) - (r0 + (r1 - r0) * h)


class Kurve:
    """Glatte Tabelle (kubisch) als schnelles np.interp."""

    def __init__(self, xs, ys, n=400):
        xs, ys = np.array(xs, dtype=float), np.array(ys, dtype=float)
        m = np.gradient(ys, xs)
        X = np.linspace(xs[0], xs[-1], n)
        i = np.clip(np.searchsorted(xs, X) - 1, 0, len(xs) - 2)
        h = xs[i + 1] - xs[i]
        t = (X - xs[i]) / h
        Y = (2 * t**3 - 3 * t**2 + 1) * ys[i] + (t**3 - 2 * t**2 + t) * h * m[i] + (-2 * t**3 + 3 * t**2) * ys[i + 1] + (t**3 - t**2) * h * m[i + 1]
        self.X, self.Y = X, Y

    def __call__(self, a):
        return np.interp(a, self.X, self.Y)


class Loft:
    """Gestreckter Koerper mit Superellipsen-Querschnitt; jede Station hat oben, unten, Breite, Exponent."""

    def __init__(self, A, top, bot, wid, ex, k0=0.03, k1=0.03):
        self.top, self.bot, self.w, self.n = Kurve(A, top), Kurve(A, bot), Kurve(A, wid), Kurve(A, ex)
        self.a0, self.a1, self.k0, self.k1 = A[0], A[-1], k0, k1

    def __call__(self, a, B, c):
        t, bo, w, ex = self.top(a), self.bot(a), self.w(a), self.n(a)
        cm = 0.5 * (t + bo)
        hh = np.maximum(0.5 * (t - bo), 1e-3)
        w = np.maximum(w, 1e-3)
        u = np.maximum(B / w, 1e-5)
        v = np.maximum(np.abs(c - cm) / hh, 1e-5)
        rr = (u**ex + v**ex) ** (1.0 / ex)
        d = (rr - 1.0) * np.minimum(w, hh)
        d = smax(d, self.a0 - a, self.k0)
        d = smax(d, a - self.a1, self.k1)
        return d


# ------------------------------------------------------------------ Masstabellen (Haut, ohne Fell)
# Oberseite: Schaedel fast flach, klare Stirnkerbe, dann gerader Nasenruecken
OBEN = Loft(
    [-0.18, -0.10, -0.02, 0.06, 0.13, 0.19, 0.24, 0.275, 0.305, 0.34, 0.40, 0.45, 0.489],
    [0.085, 0.108, 0.137, 0.160, 0.171, 0.171, 0.160, 0.124, 0.086, 0.073, 0.069, 0.067, 0.065],
    [-0.125, -0.125, -0.125, -0.12, -0.10, -0.075, -0.060, -0.072, -0.076, -0.076, -0.075, -0.073, -0.070],
    [0.128, 0.140, 0.152, 0.160, 0.155, 0.133, 0.113, 0.100, 0.094, 0.089, 0.083, 0.079, 0.076],
    [2.3, 2.3, 2.3, 2.3, 2.3, 2.4, 2.5, 2.6, 2.8, 3.0, 3.1, 3.1, 3.1],
    k0=0.05,
    k1=0.022,
)
# Unterkiefer: tief, rueckwaerts in den Hals
UNTEN = Loft(
    [0.00, 0.08, 0.16, 0.24, 0.32, 0.39, 0.44, 0.475],
    [-0.02, -0.02, -0.02, -0.025, -0.028, -0.03, -0.03, -0.03],
    [-0.135, -0.142, -0.140, -0.134, -0.126, -0.118, -0.111, -0.098],
    [0.135, 0.128, 0.108, 0.092, 0.082, 0.074, 0.067, 0.058],
    [2.4, 2.4, 2.4, 2.5, 2.6, 2.6, 2.6, 2.6],
    k0=0.03,
    k1=0.03,
)
LIP = Kurve([0.20, 0.25, 0.29, 0.34, 0.42, 0.50], [-0.044, -0.046, -0.047, -0.047, -0.044, -0.040])
ECKE = 0.275  # Mundwinkel unter dem Auge

# Auge: Lage, Blickachse, Achsen der Lidspalte
SOCK = np.array((0.268, 0.074, 0.088))
AUGE = SOCK.copy()
_u = np.array((0.84, 0.47, 0.27))
_u = _u / np.linalg.norm(_u)
_w0 = np.array((0.0, 0.0, 1.0)) - _u * _u[2]
_w0 = _w0 / np.linalg.norm(_w0)
_v0 = np.cross(_w0, _u)
_tilt = math.radians(14.0)  # aeusserer Winkel hoeher
AU = _u
# _v0 zeigt fuer +b nach hinten-aussen (aeusserer Winkel)
if _v0[0] > 0:
    _v0 = -_v0
AV = _v0 * math.cos(_tilt) + _w0 * math.sin(_tilt)
AW = np.cross(AU, AV)
if AW[2] < 0:
    AW = -AW
R_LID = 0.0232
R_BALL = 0.0208
SPALT_L, SPALT_O, SPALT_U = 0.0150, 0.0058, 0.0042
LID_UEBER = 0.0028  # so weit steht die Lidkappe aus der Haut
LOCH_RAND = 0.0030  # um so viel ist die Hautoeffnung groesser als die Lidspalte


def _acht(a, b, c, Cn, U, V, W):
    x, y, z = a - Cn[0], b - Cn[1], c - Cn[2]
    return x * U[0] + y * U[1] + z * U[2], x * V[0] + y * V[1] + z * V[2], x * W[0] + y * W[1] + z * W[2]


def _kreis_r(L, h):
    return (L * L + h * h) / (2.0 * h)


_RO, _RU = _kreis_r(SPALT_L, SPALT_O), _kreis_r(SPALT_L, SPALT_U)


def spalt2d(v, w):
    """Mandel: Schnitt zweier grosser Kreise. Negativ = in der Spalte."""
    d1 = np.sqrt(v * v + (w - (SPALT_O - _RO)) ** 2) - _RO
    d2 = np.sqrt(v * v + (w - (-SPALT_U + _RU)) ** 2) - _RU
    return np.maximum(d1, d2)


# Ohr: Schale, Oeffnung nach vorn-aussen
OHR_C = np.array((0.012, 0.148, 0.128))
_on = np.array((0.74, 0.60, 0.30))
OHR_N = _on / np.linalg.norm(_on)
_ot = np.cross(OHR_N, np.array((0.0, 0.0, 1.0)))
OHR_T = _ot / np.linalg.norm(_ot)
OHR_S = np.cross(OHR_N, OHR_T)
if OHR_S[2] < 0:
    OHR_S = -OHR_S


def ohr_teile(a, B, c):
    n, t, s = _acht(a, B, c, OHR_C, OHR_N, OHR_T, OHR_S)
    aussen = ell(n, t, s, (0, 0, 0), (0.021, 0.050, 0.055))
    schale = ell(n, t, s, (0.018, 0, 0.004), (0.022, 0.040, 0.044))
    return aussen, schale


def feld_huelle(a, b, c):
    """Die aeussere Form samt Lidoeffnung, aber noch ohne Mundspalte."""
    d = huelle_basis(a, b, c)
    B = np.abs(b)
    x, y, z = _acht(a, B, c, AUGE, AU, AV, AW)
    loch = smax(spalt2d(y, z) - LOCH_RAND, -x, 0.001)
    return smax(d, -loch, 0.0018)


def huelle_basis(a, b, c):
    """Die aeussere Form: Lippe, Augenhoehle, Nasenfurche."""
    B = np.abs(b)
    # Der Oberkiefer endet flach an der Lippe; davor faellt der Schnitt weich weg
    u_ = OBEN(a, B, c)
    u_ = smax(u_, (LIP(a) - 0.001 - 0.2 * sst(0.31, 0.235, a)) - c, 0.004)
    d = smin(u_, UNTEN(a, B, c), 0.012 + 0.02 * sst(0.30, 0.20, a))
    # Wangen und Jochbein: weich, keine Falte zum Schaedel
    d = smin(d, ell(a, B, c, (0.085, 0.114, -0.058), (0.125, 0.056, 0.088)), 0.06)
    d = smin(d, cap(a, B, c, (0.05, 0.138, -0.018), (0.205, 0.108, 0.018), 0.024, 0.016), 0.03)
    # Nackenstopfen, der im Koerper verschwindet
    d = smin(d, cap(a, B, c, (-0.02, 0.0, -0.030), (-0.15, 0.0, -0.045), 0.158, 0.192), 0.06)
    # Stirnkerbe: quer ueber den Nasenruecken
    d = smax(d, -cap(a, B, c, (0.300, 0.0, 0.118), (0.300, 0.050, 0.118), 0.032), 0.02)
    # Augenhoehle: Nische, die unter dem Brauenwulst nach vorn schaut
    x, y, z = _acht(a, B, c, SOCK, AU, AV, AW)
    d = smax(d, -ell(x, y, z, (0.020, 0.0, -0.002), (0.022, 0.034, 0.019)), 0.012)
    # Brauenwulst: weich, kein aufgelegter Balken
    d = smin(d, cap(a, B, c, (0.222, 0.106, 0.122), (0.272, 0.064, 0.110), 0.012, 0.010), 0.030)
    # Ohren
    oa, os_ = ohr_teile(a, B, c)
    d = smin(d, smax(oa, -os_, 0.006), 0.012)
    # Oberlippe (Lefze) haengt ueber die Unterlippe
    d = smin(d, cap(a, B, c, (0.29, 0.088, -0.039), (0.47, 0.073, -0.036), 0.0065, 0.0062), 0.010)
    d = smin(d, cap(a, B, c, (0.468, 0.073, -0.036), (0.484, 0.012, -0.034), 0.0062, 0.0060), 0.010)
    # Unterlippe und Kinn
    d = smin(d, cap(a, B, c, (0.285, 0.073, -0.056), (0.452, 0.054, -0.053), 0.0070, 0.0065), 0.008)
    d = smin(d, cap(a, B, c, (0.452, 0.054, -0.053), (0.470, 0.0, -0.053), 0.0065, 0.0065), 0.008)
    # Nasenfurche in die Oberlippe
    d = smax(d, -cap(a, B, c, (0.497, 0.0, 0.010), (0.486, 0.0, -0.046), 0.0052, 0.0048), 0.0045)
    return d


_CAV_O = Loft(
    [0.13, 0.18, 0.25, 0.35, 0.42, 0.452, 0.474],
    [-0.012] * 7,
    [-0.050, -0.050, -0.050, -0.050, -0.048, -0.046, -0.044],
    [0.020, 0.040, 0.054, 0.056, 0.052, 0.044, 0.014],
    [2.6] * 7,
    k0=0.015,
    k1=0.010,
)
_CAV_U = Loft(
    [0.13, 0.20, 0.30, 0.38, 0.43, 0.450],
    [-0.044] * 6,
    [-0.096, -0.096, -0.096, -0.094, -0.090, -0.084],
    [0.020, 0.040, 0.052, 0.050, 0.040, 0.020],
    [2.6] * 6,
    k0=0.015,
    k1=0.010,
)


def lippe(a, B):
    return LIP(a) + 0.0055 * np.exp(-((B / 0.011) ** 2))


def feld_kopf(a, b, c, spalt=0.0032):
    """Huelle minus Mundspalte minus Mundhoehle, plus Zahnfleisch. Das ist die Haut des Kopfes."""
    B = np.abs(b)
    d = feld_huelle(a, b, c)
    s = np.abs(c - lippe(a, B)) - spalt * (0.45 + 0.55 * sst(ECKE, ECKE + 0.055, a))
    s = smax(s, ECKE - a, 0.005)
    d = smax(d, -s, 0.0022)
    cav = np.minimum(_CAV_O(a, B, c), _CAV_U(a, B, c))
    d = smax(d, -cav, 0.004)
    # Gaumenfalten
    # Zahnfleisch oben und unten
    d = smin(d, cap(a, B, c, (0.27, 0.052, -0.012), (0.445, 0.043, -0.012), 0.0115, 0.010), 0.004)
    d = smin(d, cap(a, B, c, (0.445, 0.043, -0.012), (0.462, 0.0, -0.012), 0.010, 0.0095), 0.004)
    d = smin(d, cap(a, B, c, (0.25, 0.049, -0.088), (0.428, 0.042, -0.082), 0.0115, 0.010), 0.004)
    d = smin(d, cap(a, B, c, (0.428, 0.042, -0.082), (0.446, 0.0, -0.079), 0.010, 0.0095), 0.004)
    return d


def _auge_setzen():
    """Die Lidkappe soll nur LID_UEBER aus der Haut stehen: entlang der Blickachse die Flaeche suchen."""
    global AUGE
    ts = np.linspace(-0.05, 0.05, 401)
    P = SOCK[None, :] + AU[None, :] * ts[:, None]
    d = huelle_basis(P[:, 0], P[:, 1], P[:, 2])
    i = np.nonzero((d[:-1] < 0) & (d[1:] >= 0))[0]
    t0 = ts[i[-1]] if len(i) else 0.0
    AUGE = SOCK + AU * (t0 - (R_LID - LID_UEBER))


_auge_setzen()


# ------------------------------------------------------------------ Eigene feine Felder
def feld_lid(a, b, c):
    """Lid als Kugelkappe mit Mandelfenster und Lidrand. Nur fuer b>0 aufrufen."""
    x, y, z = _acht(a, b, c, AUGE, AU, AV, AW)
    r = np.sqrt(x * x + y * y + z * z)
    win = spalt2d(y, z)
    fenster = smax(win, -x, 0.001)
    d = smax(r - R_LID, -fenster, 0.0014)
    # Lidrand: Wulst um die Spalte
    rand = np.sqrt(np.maximum(win, -win) ** 2 + (r - R_LID + 0.0002) ** 2) - 0.0017
    rand = np.where(x > 0, rand, 1.0)
    d = smin(d, rand, 0.0014)
    # Hinten geschlossen halten: nur die Vorderkappe
    d = smax(d, -x - 0.012, 0.002)
    return d


NASE_C = np.array((0.489, 0.0, 0.0345))
NASE_HW, NASE_HH = 0.0425, 0.0275


def nasenfront(y, z):
    """Lage der Vorderflaeche der Nase in Koordinaten um NASE_C (nach vorn)."""
    return 0.0255 - 0.012 * (y / NASE_HW) ** 2 - 0.006 * (z / NASE_HH) ** 2 + 0.05 * z


def nasenloch(x, y, z):
    xf = nasenfront(y, z)
    # Kopf des Kommas: tiefes, rundes Loch nahe der Mitte
    tief = ell(x, y, z, (0.012, 0.0200, -0.0045), (0.022, 0.0082, 0.0070))
    # Schwanz des Kommas: laeuft nach aussen und oben aus
    sch = cap(x - xf, y, z, (-0.001, 0.0215, -0.0025), (-0.0015, 0.0390, 0.0105), 0.0044, 0.0012)
    return smin(tief, sch, 0.0025)


def feld_nase(a, b, c):
    B = np.abs(b)
    x, y, z = a - NASE_C[0], B, c - NASE_C[2]
    # Breites Polster, unten schmaler, oben flach
    w = NASE_HW * (0.70 + 0.30 * sst(-NASE_HH, 0.012, z))
    xf = nasenfront(y, z)
    qx = x - (xf - 0.034)
    q1 = np.abs(qx) - 0.034 + 0.012
    q2 = y - w + 0.012
    q3 = np.abs(z + 0.0020) - (NASE_HH - 0.0020) + 0.012
    o = np.sqrt(np.maximum(q1, 0) ** 2 + np.maximum(q2, 0) ** 2 + np.maximum(q3, 0) ** 2)
    d = o + np.minimum(np.maximum(np.maximum(q1, q2), q3), 0) - 0.012
    # Nasenfluegel ueber dem Loch
    d = smin(d, ell(x - xf, y, z, (-0.006, 0.0305, 0.0115), (0.0085, 0.0115, 0.0085)), 0.005)
    # Mittelfurche, unten tief, oben flach
    fur = cap(x - xf, y, z, (0.0015, 0.0, -0.032), (0.0015, 0.0, 0.009), 0.0036, 0.0020)
    d = smax(d, -fur, 0.003)
    d = smax(d, -nasenloch(x, y, z), 0.0022)
    return d


def feld_zunge(a, b, c):
    B = np.abs(b)
    d = ell(a, B, c, (0.30, 0.0, -0.0785), (0.130, 0.041, 0.0125))
    d = smax(d, -cap(a, B, c, (0.20, 0.0, -0.065), (0.42, 0.0, -0.065), 0.0035), 0.008)
    return d


def feld_kamm(a, b, c):
    """Unteres Zahnfleisch als Wulst: ragt ueber die Spaltebene, damit man seitlich nie durchs Maul sieht."""
    B = np.abs(b)
    d = cap(a, B, c, (0.268, 0.046, -0.054), (0.425, 0.043, -0.050), 0.0098)
    d = smin(d, cap(a, B, c, (0.425, 0.043, -0.050), (0.456, 0.028, -0.048), 0.0098), 0.004)
    d = smin(d, cap(a, B, c, (0.456, 0.028, -0.048), (0.461, 0.0, -0.048), 0.0098), 0.004)
    d = smin(d, cap(a, B, c, (0.26, 0.047, -0.064), (0.425, 0.043, -0.062), 0.0105), 0.004)
    return d


# ------------------------------------------------------------------ Vom Feld zum Netz (Surface Nets)
def netz_aus_feld(feld, lo, hi, h, grob=4, rand=2.4, schritte=2):
    lo, hi = np.asarray(lo, dtype=float), np.asarray(hi, dtype=float)
    n = (np.ceil((hi - lo) / h).astype(int) + 1).tolist()
    ax = [(lo[i] + h * np.arange(n[i])).astype(np.float32) for i in range(3)]
    # Grob rechnen, dann nur das Band um die Flaeche fein
    gx = [(lo[i] + h * np.arange(0, n[i] + grob, grob)).astype(np.float32) for i in range(3)]
    G = np.meshgrid(*gx, indexing="ij")
    D0 = np.asarray(feld(G[0], G[1], G[2]), dtype=np.float32)
    del G
    ix = [(np.arange(n[i]) + grob // 2) // grob for i in range(3)]
    F = D0[np.ix_(ix[0], ix[1], ix[2])]
    mask = np.abs(F) < rand * h * grob
    idx = np.nonzero(mask)
    F[idx] = np.asarray(feld(ax[0][idx[0]], ax[1][idx[1]], ax[2][idx[2]]), dtype=np.float32)
    del idx, mask, D0
    ins = F < 0
    ny, nz = n[1], n[2]
    pos_all, cid_all, flip_all = [], [], []
    for axis in range(3):
        s0, s1 = [slice(None)] * 3, [slice(None)] * 3
        s0[axis], s1[axis] = slice(0, -1), slice(1, None)
        s0, s1 = tuple(s0), tuple(s1)
        E = ins[s0] != ins[s1]
        I = [x.astype(np.int64) for x in np.nonzero(E)]
        d0, d1 = F[s0][E], F[s1][E]
        st = ins[s0][E]
        u, v = (axis + 1) % 3, (axis + 2) % 3
        ok = (I[u] > 0) & (I[v] > 0) & (I[u] < n[u] - 1) & (I[v] < n[v] - 1)
        I = [x[ok] for x in I]
        d0, d1, st = d0[ok], d1[ok], st[ok]
        t = d0 / (d0 - d1)
        pos = np.stack([I[0].astype(np.float32), I[1].astype(np.float32), I[2].astype(np.float32)], 1)
        pos[:, axis] += t
        cells = []
        for du, dv in ((-1, -1), (0, -1), (0, 0), (-1, 0)):
            C = [I[0].copy(), I[1].copy(), I[2].copy()]
            C[u] += du
            C[v] += dv
            cells.append(C[0] * ny * nz + C[1] * nz + C[2])
        cid_all.append(np.stack(cells, 1))
        pos_all.append(pos)
        flip_all.append(~st)
    del F, ins
    cid = np.concatenate(cid_all, 0)
    pos = np.concatenate(pos_all, 0)
    flip = np.concatenate(flip_all, 0)
    uq, inv = np.unique(cid.ravel(), return_inverse=True)
    inv = inv.reshape(cid.shape)
    cnt = np.bincount(inv.ravel(), minlength=len(uq)).astype(float)
    V = np.zeros((len(uq), 3))
    for i in range(3):
        w = np.repeat(pos[:, i], 4)
        V[:, i] = np.bincount(inv.ravel(), weights=w, minlength=len(uq)) / cnt
    V = lo + h * (V + 0.0)
    Q = inv.copy()
    Q[flip] = Q[flip][:, ::-1]
    # Auf die echte Nullflaeche ziehen
    e = h * 0.4
    for _ in range(schritte):
        d = feld(V[:, 0], V[:, 1], V[:, 2])
        g = np.stack(
            (
                feld(V[:, 0] + e, V[:, 1], V[:, 2]) - feld(V[:, 0] - e, V[:, 1], V[:, 2]),
                feld(V[:, 0], V[:, 1] + e, V[:, 2]) - feld(V[:, 0], V[:, 1] - e, V[:, 2]),
                feld(V[:, 0], V[:, 1], V[:, 2] + e) - feld(V[:, 0], V[:, 1], V[:, 2] - e),
            ),
            1,
        ) / (2 * e)
        l2 = np.maximum((g * g).sum(1), 1e-4)
        sv = g * (d / l2)[:, None]
        ln = np.sqrt((sv * sv).sum(1))
        sv *= (np.minimum(ln, h) / np.maximum(ln, 1e-9))[:, None]
        V = V - sv
    return V, Q


def glaette(V, Q, faktor=0.4, runden=1, maske=None):
    """Laplace-Glaettung ueber die Kanten; nimmt Treppen, die Surface Nets laesst."""
    for _ in range(runden):
        S = np.zeros_like(V)
        C = np.zeros(len(V))
        for i, j in ((0, 1), (1, 2), (2, 3), (3, 0)):
            a, b = Q[:, i], Q[:, j]
            for ax in range(3):
                S[:, ax] += np.bincount(a, weights=V[b, ax], minlength=len(V)) + np.bincount(b, weights=V[a, ax], minlength=len(V))
            C += np.bincount(a, minlength=len(V)) + np.bincount(b, minlength=len(V))
        M = S / np.maximum(C, 1)[:, None]
        f = faktor if maske is None else faktor * maske[:, None]
        V = V + (M - V) * f
    return V


def punkt_normalen(V, Q):
    n = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]])
    N = np.zeros_like(V)
    for i in range(4):
        for ax in range(3):
            N[:, ax] += np.bincount(Q[:, i], weights=n[:, ax], minlength=len(V))
    return N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)


# ------------------------------------------------------------------ Faerbung und Haarwerte
def mel2rgb(m):
    return np.stack((0.58 * np.exp(-3.6 * m), 0.42 * np.exp(-4.3 * m), 0.28 * np.exp(-5.2 * m)), -1)


def rauschen(a, b, c, f, seed=0.0):
    """Billiges Wolkenrauschen, -1..1."""
    return (
        np.sin(a * f + 1.3 + seed) * np.sin(b * f * 1.17 + 0.7 + seed * 2) * np.sin(c * f * 0.91 + 2.1)
        + 0.5 * np.sin(a * f * 2.3 + 4.1) * np.sin(b * f * 2.11 + seed) * np.sin(c * f * 1.87 + 0.3)
    )


def regionen(a, b, c):
    B = np.abs(b)
    dn = np.sqrt((a - NASE_C[0]) ** 2 + b * b + (c - NASE_C[2]) ** 2)
    dn2 = np.sqrt((a - NASE_C[0]) ** 2 + (b * 1.22) ** 2 + (np.where(c > NASE_C[2], (c - NASE_C[2]) * 0.85, (c - NASE_C[2]) * 1.35)) ** 2)
    nah = 1.0 - sst(0.047, 0.086, dn2)
    schn = sst(0.262, 0.350, a)
    schf = sst(0.185, 0.405, a)
    stirn = sst(-0.01, 0.20, a) * (1.0 - sst(0.275, 0.325, a)) * sst(0.01, 0.06, c)
    dE = np.sqrt((a - AUGE[0]) ** 2 + (B - AUGE[1]) ** 2 + (c - AUGE[2]) ** 2)
    aug = 1.0 - sst(0.022, 0.050, dE)
    wan = (1.0 - sst(0.10, 0.30, a)) * (1.0 - sst(-0.07, 0.10, c)) * sst(0.03, 0.09, B)
    dv = lippe(a, B) - c
    unter = sst(0.0, 0.012, dv) * sst(0.15, 0.30, a)
    oa, os_ = ohr_teile(a, B, c)
    # Nur was wirklich aus dem Schaedel ragt, ist Ohr: sonst liegt ein dunkler Fleck darunter
    ohr = (1.0 - sst(-0.002, 0.010, oa)) * sst(0.002, 0.014, OBEN(a, B, c))
    innen = (1.0 - sst(-0.004, 0.004, os_)) * ohr
    return dict(B=B, dn=dn, nah=nah, schn=schn, schf=schf, stirn=stirn, dE=dE, aug=aug, wan=wan, dv=dv, unter=unter, ohr=ohr, innen=innen)


def haar_werte(a, b, c):
    """Laenge, Melanin, Roetung je Stelle. Laenge in Metern."""
    R = regionen(a, b, c)
    n1 = rauschen(a, b, c, 34.0)
    n2 = rauschen(a, b, c, 90.0, 1.7)
    # Laenge
    # Von hinten nach vorn immer kuerzer: keine Stufe zwischen Wange und Schnauze
    L = 0.018 + 0.078 * sst(0.34, 0.04, a)
    L = mixf(L, L * 1.18, R["wan"])
    L = mixf(L, 0.036, R["stirn"])
    L = mixf(L, 0.0155, R["schn"] ** 1.5)
    L = mixf(L, 0.017, np.exp(-(((a - 0.292) / 0.034) ** 2)) * sst(0.02, 0.07, c))
    L = mixf(L, 0.022, R["unter"] * (1 - 0.35 * R["schn"]) * sst(0.22, 0.30, a))
    L = mixf(L, 0.0195, R["schn"] * sst(0.030, 0.006, -R["dv"]) * (R["dv"] < 0))
    L = mixf(L, 0.0055, R["nah"] ** 1.5)
    L = mixf(L, 0.012, R["aug"])
    _oa, _ = ohr_teile(a, R["B"], c)
    L = mixf(L, 0.034, (1.0 - sst(0.0, 0.045, _oa)) * sst(-0.015, 0.035, a))
    L = mixf(L, 0.022, R["ohr"])
    L = mixf(L, 0.030, R["innen"])
    # Melanin: 0 hell, 1 schwarz
    m = 0.70 + 0.05 * n1 + 0.15 * sst(0.16, -0.12, a)
    m = mixf(m, 0.68 + 0.05 * n1 + 0.12 * sst(0.12, -0.08, a), R["wan"] * 0.8)
    m = mixf(m, 0.62 + 0.06 * n1, R["stirn"])
    # Schnauze fawn, zur Nase hin dunkler, Nasenruecken eine Spur dunkler als die Seiten
    fawn = 0.47 + 0.05 * n2 + 0.035 * n1 + 0.08 * sst(0.022, 0.058, c) * (1.0 - sst(0.03, 0.078, R["B"]))
    m = mixf(m, fawn, R["schf"])
    m = mixf(m, 0.56 + 0.03 * n2, R["unter"] * 0.9)
    # Entlang der Lippe etwas dunkler
    m = mixf(m, m + 0.10, (1.0 - sst(0.008, 0.024, np.abs(R["dv"]))) * R["schn"])
    m = mixf(m, 0.60, R["nah"] ** 1.8)
    m = mixf(m, 0.70, R["aug"] * 0.45)
    m = mixf(m, 0.86, R["ohr"])
    m = mixf(m, 0.40, R["innen"])
    rot = mixf(0.26, 0.32, R["schn"])
    rot = mixf(rot, 0.30, R["stirn"])
    return L, m, rot, R


def haut_attribute(V):
    """Hautfarbe und Feuchte je Punkt des Kopfnetzes."""
    a, b, c = V[:, 0], V[:, 1], V[:, 2]
    L, m, rot, R = haar_werte(a, b, c)
    rgb = mel2rgb(np.clip(m + 0.08, 0, 1))
    B = R["B"]
    h = feld_huelle(a, b, c)
    tief = sst(-0.0035, -0.009, h)
    # Mundinneres
    roh = np.stack((0.105 + 0 * a, 0.017 + 0 * a, 0.021 + 0 * a), -1)
    gum = np.stack((0.21 + 0 * a, 0.050 + 0 * a, 0.056 + 0 * a), -1)
    gt = sst(0.026, 0.038, B) * sst(0.24, 0.30, a)
    inn = roh + (gum - roh) * gt[:, None]
    rachen = sst(0.27, 0.20, a)
    inn = inn * (1.0 - 0.9 * rachen)[:, None]
    rgb = rgb + (inn - rgb) * tief[:, None]
    # Lippen: schwarzer Streifen, Unterlippe breiter
    dv = R["dv"]
    vorn = sst(ECKE - 0.006, ECKE + 0.030, a)
    obenb = 1.0 - sst(0.0032, 0.0072, -dv)
    untenb = 1.0 - sst(0.0042, 0.0095, dv)
    lip = np.where(dv < 0, obenb, untenb) * vorn
    lip = lip * (1.0 - tief * 0.75)
    # Mittelfurche
    fur = cap(a, B, c, (0.497, 0.0, 0.010), (0.486, 0.0, -0.046), 0.0)
    lip = np.maximum(lip, 1.0 - sst(0.006, 0.012, fur))
    # Um die Nase
    dunkel = np.array((0.012, 0.010, 0.010))
    rgb = rgb + (dunkel - rgb) * lip[:, None]
    # Augenrand
    _x, _y, _z = _acht(a, B, c, AUGE, AU, AV, AW)
    aug = (1.0 - sst(0.004, 0.011, spalt2d(_y, _z))) * (_x > 0)
    rgb = rgb + (dunkel - rgb) * aug[:, None]
    # Dehnzone hinter dem Mundwinkel: dunkel, wie die Innenseite der Backe
    dehn = (1.0 - sst(0.012, 0.050, np.abs(dv))) * sst(0.12, 0.19, a) * (1.0 - sst(ECKE - 0.01, ECKE + 0.01, a))
    rgb = rgb + (np.array((0.010, 0.006, 0.005)) - rgb) * dehn[:, None]
    feucht = np.clip(tief * (1.0 - 0.85 * sst(ECKE + 0.03, ECKE - 0.03, a)) + 0.45 * lip + 0.4 * aug, 0, 1)
    return rgb, feucht


def haar_dichte(C):
    """Straehnen je Quadratmeter auf der Kopfhaut."""
    a, b, c = C[:, 0], C[:, 1], C[:, 2]
    R = regionen(a, b, c)
    d = 270000.0 + 0 * a
    d = mixf(d, 210000.0, R["wan"])
    d = mixf(d, 300000.0, R["stirn"])
    d = mixf(d, 520000.0, R["schn"])
    d = mixf(d, 760000.0, R["nah"] ** 1.3)
    d = mixf(d, 300000.0, R["ohr"])
    d = mixf(d, 340000.0, R["aug"])
    # Nur aussen auf der Huelle
    h = feld_huelle(a, b, c)
    d = d * sst(-0.0030, -0.0012, h)
    # Nicht auf Lippe, Mittelfurche, Lid, Nase, Nackenstopfen tief im Koerper
    dv = R["dv"]
    vorn = sst(ECKE - 0.022, ECKE + 0.002, a)
    frei = 1.0 - (1.0 - sst(0.0026, 0.0058, np.abs(dv))) * vorn
    fur = cap(a, R["B"], c, (0.497, 0.0, 0.010), (0.486, 0.0, -0.046), 0.0)
    frei = frei * sst(0.0035, 0.0075, fur)
    _x, _y, _z = _acht(a, R["B"], c, AUGE, AU, AV, AW)
    frei = frei * np.where(_x > 0, sst(LOCH_RAND + 0.0008, LOCH_RAND + 0.0034, spalt2d(_y, _z)), 1.0)
    frei = frei * sst(-0.0005, 0.0030, feld_nase(a, b, c))
    frei = frei * sst(-0.25, -0.12, a)
    return d * frei


def haar_fluss(a, b, c):
    """Strich des Fells: von der Nase nach hinten, Wange nach hinten-unten, weg vom Auge."""
    R = regionen(a, b, c)
    s = np.sign(b)
    F = np.zeros((len(a), 3))
    F[:, 0] = -1.0
    # Um die Nase strahlenfoermig
    rx, ry, rz = a - (NASE_C[0] + 0.02), b, c - NASE_C[2]
    rl = np.maximum(np.sqrt(rx * rx + ry * ry + rz * rz), 1e-4)
    k = (1.0 - sst(0.05, 0.13, rl)) * 1.4
    F[:, 0] += k * rx / rl
    F[:, 1] += k * ry / rl
    F[:, 2] += k * rz / rl
    # Wange nach unten und aussen, Stirn leicht aussen
    F[:, 2] += -0.34 * R["wan"] - 0.25 * R["schn"] * sst(0.02, -0.03, c)
    F[:, 1] += s * sst(0.0, 0.05, R["B"]) * (0.28 * R["wan"] + 0.16 * R["stirn"])
    # Unterkiefer nach hinten-unten
    F[:, 2] += -0.42 * R["unter"]
    F[:, 2] += -0.60 * R["schn"] * sst(0.032, 0.004, -R["dv"]) * (R["dv"] < 0)
    # Weg vom Auge, aber oberhalb liegt das Haar von der Stirn her ueber dem Lid
    ex, ey, ez = a - AUGE[0], R["B"] - AUGE[1], c - AUGE[2]
    el = np.maximum(R["dE"], 1e-4)
    ke = 1.1 * R["aug"]
    F[:, 0] += ke * ex / el
    F[:, 1] += ke * s * ey / el
    F[:, 2] += ke * ez / el
    # Ohr: von der Basis zum Rand
    ox, oy, oz = a - OHR_C[0], R["B"] - (OHR_C[1] - 0.02), c - (OHR_C[2] - 0.06)
    ol = np.maximum(np.sqrt(ox * ox + oy * oy + oz * oz), 1e-4)
    ko = R["ohr"]
    F[:, 0] = mixf(F[:, 0], ox / ol, ko)
    F[:, 1] = mixf(F[:, 1], s * oy / ol, ko)
    F[:, 2] = mixf(F[:, 2], oz / ol, ko)
    return F


def kiefer_gewicht(a, b, c, spalt):
    """1 = folgt dem Unterkiefer, 0 = dem Schaedel. Hinter dem Mundwinkel laeuft es weich aus."""
    B = np.abs(b)
    dv = lippe(a, B) - c
    delta = spalt * 1.1 + np.clip(ECKE - a, 0, 1) * 0.55
    below = sst(-delta, delta, dv)
    front = sst(0.06, ECKE - 0.012, a)
    return below * front


# ------------------------------------------------------------------ Straehnen wachsen lassen
def wachse(V, Q, dichte_fn, werte_fn, rng, faktor=1.0, np_pts=5, schutz_fn=None, schutz=0.0012, nachbes_fn=None):
    """Liefert Punkte (N,np_pts,3), Radius, und Attribute. werte_fn(P, n) -> dict."""
    T = np.concatenate((Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]), 0)
    e1, e2 = V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]
    area = 0.5 * np.linalg.norm(np.cross(e1, e2), axis=1)
    cen = V[T].mean(1)
    p = area * np.maximum(dichte_fn(cen), 0.0) * faktor
    tot = p.sum()
    N = int(tot)
    idx = rng.choice(len(T), N, p=p / tot)
    r1, r2 = rng.random(N), rng.random(N)
    su = np.sqrt(r1)
    w0, w1, w2 = 1 - su, su * (1 - r2), su * r2
    tv = T[idx]
    P = V[tv[:, 0]] * w0[:, None] + V[tv[:, 1]] * w1[:, None] + V[tv[:, 2]] * w2[:, None]
    VN = punkt_normalen(V, Q)
    n = VN[tv[:, 0]] * w0[:, None] + VN[tv[:, 1]] * w1[:, None] + VN[tv[:, 2]] * w2[:, None]
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
    W = werte_fn(P, n)
    L, F, lift, r0, kl = W["L"], W["F"], W["lift"], W["r0"], W["kl"]
    # Tangente aus dem Strich
    t = F - n * (F * n).sum(1, keepdims=True)
    tl = np.linalg.norm(t, axis=1, keepdims=True)
    fallback = np.cross(n, np.array((0.0, 1.0, 0.0)))
    t = np.where(tl > 1e-3, t / np.maximum(tl, 1e-9), fallback)
    t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
    side = np.cross(n, t)
    # Straehnen: gemeinsame Abweichung je Zelle
    groesse = W.get("zelle", 0.022)
    cell = np.floor(P / groesse).astype(np.int64)
    key = cell[:, 0] * 73856093 ^ cell[:, 1] * 19349663 ^ cell[:, 2] * 83492791
    uq, inv = np.unique(key, return_inverse=True)
    ang_c = rng.normal(0.0, 0.24, len(uq))
    lf_c = rng.normal(1.0, 0.16, len(uq))
    C = np.stack([np.bincount(inv, weights=P[:, i], minlength=len(uq)) / np.maximum(np.bincount(inv, minlength=len(uq)), 1) for i in range(3)], 1)
    ang = ang_c[inv] * kl + rng.normal(0.0, 0.13, N)
    t = t + side * ang[:, None]
    t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
    # Deckhaare: wenige laengere
    gross = rng.random(N) < 0.035
    L = L * (1.0 + (lf_c[inv] - 1.0) * kl) * rng.normal(1.0, 0.13, N) * np.where(gross, 1.22, 1.0)
    g = W.get("g", np.zeros(N))
    d0 = n * lift[:, None] + t * (1 - lift)[:, None]
    d0 /= np.maximum(np.linalg.norm(d0, axis=1, keepdims=True), 1e-9)
    d1 = t + side * rng.normal(0.0, 0.24, N)[:, None] + n * (lift * 0.10)[:, None] + np.array((0.0, 0.0, -1.0)) * g[:, None]
    d1 /= np.maximum(np.linalg.norm(d1, axis=1, keepdims=True), 1e-9)
    rv = rng.normal(0.0, 1.0, (N, 3))
    pts = np.zeros((N, np_pts, 3))
    pts[:, 0] = P
    # Spitzen zur Straehnenmitte ziehen
    zug = (C[inv] - P) * (kl * 0.55)[:, None]
    for i in range(1, np_pts):
        s = (i - 1) / (np_pts - 2)
        di = d0 * (1 - s) + d1 * s + rv * 0.10 * s
        di /= np.maximum(np.linalg.norm(di, axis=1, keepdims=True), 1e-9)
        pts[:, i] = pts[:, i - 1] + di * (L / (np_pts - 1))[:, None]
    for i in range(1, np_pts):
        s = i / (np_pts - 1)
        pts[:, i] += zug * s**1.6
    # Kein Haar in die Haut
    if schutz_fn is not None:
        for i in range(1, np_pts):
            q = pts[:, i]
            dd = schutz_fn(q[:, 0], q[:, 1], q[:, 2])
            # Die Straehne steigt mit der Laenge: sie kriecht nie an der Haut entlang (in Kerben waere sie sonst unter der Haut)
            push = np.maximum(schutz + L * 0.13 * (i / (np_pts - 1)) - dd, 0.0)
            pts[:, i:] += (n * push[:, None])[:, None, :]
    if nachbes_fn is not None:
        pts = nachbes_fn(pts)
    rad = np.zeros((N, np_pts))
    for i in range(np_pts):
        s = i / (np_pts - 1)
        rad[:, i] = r0 * (1.0 - s) ** 0.8 * 0.92 + r0 * 0.08
    rad *= np.where(gross, 0.85, 1.0)[:, None]
    return pts, rad, W, np.where(gross, 1.0, 0.0), n


def kopf_haar_werte(P, n):
    a, b, c = P[:, 0], P[:, 1], P[:, 2]
    L, m, rot, R = haar_werte(a, b, c)
    F = haar_fluss(a, b, c)
    lift = 0.40 - 0.20 * R["schn"] - 0.12 * R["stirn"]
    lift = mixf(lift, 0.46, R["wan"] * (1 - R["schn"]))
    lift = mixf(lift, 0.26, R["nah"])
    lift = mixf(lift, 0.42, R["ohr"])
    lift = mixf(lift, 0.55, R["innen"])
    r0 = 0.00098 + 0.0 * a
    r0 = mixf(r0, 0.00125, R["wan"])
    r0 = mixf(r0, 0.00085, R["stirn"])
    r0 = mixf(r0, 0.00066, R["schn"])
    r0 = mixf(r0, 0.00056, R["nah"])
    kl = np.clip((L - 0.018) / 0.05, 0.0, 1.0)
    g = 0.22 * R["wan"]
    return dict(L=L, F=F, lift=lift, r0=r0, kl=kl, g=g, mel=m, rot=rot)


def eye_ausschluss(pts):
    """Straehnen, die ueber das Lidfenster liegen wuerden, werden gekuerzt."""
    for _ in range(3):
        for sgn in (1.0,):
            q = pts.copy()
            q[..., 1] = np.abs(q[..., 1])
            x, y, z = _acht(q[..., 0], q[..., 1], q[..., 2], AUGE, AU, AV, AW)
            r = np.sqrt(x * x + y * y + z * z)
            win = spalt2d(y, z)
            nah = (r < R_LID + 0.012) & (x > -0.002) & (win < 0.0030)
            bad = nah.any(1)
            if not bad.any():
                break
            pts[bad] = pts[bad, :1] + (pts[bad] - pts[bad, :1]) * 0.55
    return pts


# ------------------------------------------------------------------ Rohre: Kralle, Zahn
def rohr(pfad, rw, rh, oben, seg=14):
    """Rohr entlang pfad (M,3) mit Halbachsen rw (seitlich), rh (Hoehe). Liefert V, Flaechenliste, t je Punkt."""
    pfad = np.asarray(pfad, dtype=float)
    M = len(pfad)
    T = np.gradient(pfad, axis=0)
    T /= np.maximum(np.linalg.norm(T, axis=1, keepdims=True), 1e-9)
    S = np.cross(T, np.asarray(oben, dtype=float))
    S /= np.maximum(np.linalg.norm(S, axis=1, keepdims=True), 1e-9)
    U = np.cross(S, T)
    ang = np.linspace(0, 2 * math.pi, seg, endpoint=False)
    V = []
    tt = []
    for i in range(M):
        for an in ang:
            # Rueckengrat: oben etwas spitzer als unten
            ca, sa = math.cos(an), math.sin(an)
            kante = 1.0 + 0.10 * max(0.0, sa) ** 3
            V.append(pfad[i] + S[i] * rw[i] * ca + U[i] * rh[i] * sa * kante)
            tt.append(i / (M - 1))
    F = []
    for i in range(M - 1):
        for j in range(seg):
            a, b = i * seg + j, i * seg + (j + 1) % seg
            F.append((a, a + seg, b + seg, b))
    # Kappen
    c0 = len(V)
    V.append(pfad[0])
    tt.append(0.0)
    c1 = len(V)
    V.append(pfad[-1])
    tt.append(1.0)
    for j in range(seg):
        F.append((c0, j, (j + 1) % seg))
        F.append((c1, (M - 1) * seg + (j + 1) % seg, (M - 1) * seg + j))
    return np.array(V), F, np.array(tt)


def krallenpfad(S, richtung, L, th0, dth, M=26):
    """Bogen: faengt fast waagerecht an, kruemmt sich zum Boden."""
    S = np.asarray(S, dtype=float)
    f = np.array((math.cos(richtung), math.sin(richtung), 0.0))
    ds = L / (M - 1)
    P = [S.copy()]
    for i in range(1, M):
        t = (i - 0.5) / (M - 1)
        th = th0 + dth * t**1.15
        P.append(P[-1] + (f * math.cos(th) + np.array((0, 0, -1.0)) * math.sin(th)) * ds)
    return np.array(P)


# ------------------------------------------------------------------ Lauf baer-pfoten: ein Feld je Pfote (Bein + Fuss + Zehen)
# Kevin 09.11.2026: "das soll natuerlich nur eine richtige baerenpfote sein" (SPEZ_PFOTEN.md). Bisher: Bein als Metaball-Saeule bis
# zum Boden, Zehen als eigene kleine Objekte angesetzt. Jetzt je Pfote EIN Abstandsfeld in Spielmetern (Tier-Rahmen x vorn, y links,
# z oben, linke Pfote; rechts = y gespiegelt): Unterschenkel/Unterarm (Loft ueber z) verjuengt sich zum Gelenk, Fuss (Loft ueber x)
# mit Ferse, Rist, flacher Sohle mit runder Kante, fuenf Zehen um die festen Krallenwurzeln (spez/krallen_lage.txt, vorn K1),
# vorn ein Handwurzelballen. Die Tabellen sind das SOLL des fertigen Spielnetzes (mit Fellhuelle, SPEZ 1.2/1.3,
# spez/pfoten_plan.json); die Haut hier ist Soll minus PF_HUELLE (so dick legt baer_export_pfote.py die Huelle darueber).
PF_X0, PF_ZMIN, PF_G = -0.081113065901304876, 0.001335123204626143, 0.75   # Hochmodell -> Spielmeter (baer_export_fell.py:59, :292)
PF_HUELLE = (np.array([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.36, 0.60]),
             np.array([0.007, 0.008, 0.010, 0.015, 0.020, 0.030, 0.045, 0.071, 0.071]))   # Fellhuelle je Hoehe (Spielmeter)
PF_HUELLE_ZEHE = 0.004      # Zehen: kurzes Fell
PF_HUELLE_BALLEN = 0.003    # nackte Ballen (Handwurzelballen)
PF_BODEN = 0.0010           # Sohle liegt hier auf (Spielmeter; alt 0,003 Hochmodell)


def pf_huelle(z):
    return np.interp(z, PF_HUELLE[0], PF_HUELLE[1])


def pf_h2s(x, y, z):
    return (x - PF_X0) * PF_G, y * PF_G, (z - PF_ZMIN) * PF_G


class PfBein:
    """Unterschenkel/Unterarm: Superellipse in (x, y) je Hoehe z (Hinterkante xb, Vorderkante xf, halbe Breite hw, Mitte yc),
    Soll-Tabellen; die Haut ist um die Huelle der jeweiligen Hoehe kleiner."""

    def __init__(self, Z, xb, xf, hw, yc, n, z0, z1, k=0.012):
        Z = np.asarray(Z, dtype=float)
        h = pf_huelle(Z)
        self.xb, self.xf = Kurve(Z, np.asarray(xb) + h), Kurve(Z, np.asarray(xf) - h)
        self.hw, self.yc = Kurve(Z, np.asarray(hw) - h), Kurve(Z, yc)
        self.soll = (Kurve(Z, xb), Kurve(Z, xf), Kurve(Z, hw))
        self.n, self.z0, self.z1, self.k = n, z0, z1, k

    def __call__(self, x, y, z, soll=False):
        xb, xf, hw, yc = self.xb(z), self.xf(z), self.hw(z), self.yc(z)
        if soll:
            xb, xf, hw = self.soll[0](z), self.soll[1](z), self.soll[2](z)
        a = np.maximum(0.5 * (xf - xb), 1e-3)
        hw = np.maximum(hw, 1e-3)
        u = np.maximum(np.abs(x - 0.5 * (xf + xb)) / a, 1e-6)
        v = np.maximum(np.abs(y - yc) / hw, 1e-6)
        d = ((u ** self.n + v ** self.n) ** (1.0 / self.n) - 1.0) * np.minimum(a, hw)
        d = smax(d, self.z0 - z, self.k)
        return smax(d, z - self.z1, self.k)


class PfFuss:
    """Fuss/Pranke: Loft ueber x, Querschnitt eine Kuppel ueber flacher Sohle: (|y-yc|/w)^n + ((z-zb)/(zt-zb))^n <= 1, z >= zb.
    w halbe Breite an der Sohle, zb Sohle (0 = liegt auf; hinten an der Ferse angehoben), zt Oberkante (Rist), Soll-Tabellen;
    kb rundet die Sohlenkante, k0/k1 die Enden (Ferse hinten, Zehenansatz vorn)."""

    def __init__(self, X, w, zb, zt, yc, n, x0, x1, kb, k0, k1, hf, hf_w=0.002):
        X = np.asarray(X, dtype=float)
        zb, zt = np.asarray(zb, dtype=float), np.asarray(zt, dtype=float)
        self.w = Kurve(X, np.asarray(w) - hf_w)   # Runde 8: Seiten nur 2 mm unter dem Soll (gemessen: die Huelle legt dort kaum zu)
        self.zb = Kurve(X, np.where(zb > 0.002, zb + hf, zb))
        self.zt = Kurve(X, zt - np.maximum(pf_huelle(zt), hf))
        self.yc = Kurve(X, yc)
        self.soll = (Kurve(X, w), Kurve(X, zb), Kurve(X, zt), x0, x1)
        self.n, self.x0, self.x1 = n, x0 + hf, x1 - hf
        self.kb, self.k0, self.k1 = kb, k0, k1

    def __call__(self, x, y, z, soll=False):
        w, zb, zt, yc = np.maximum(self.w(x), 1e-3), self.zb(x), self.zt(x), self.yc(x)
        x0, x1 = self.x0, self.x1
        if soll:
            w, zb, zt, x0, x1 = np.maximum(self.soll[0](x), 1e-3), self.soll[1](x), self.soll[2](x), self.soll[3], self.soll[4]
        hh = np.maximum(zt - zb, 1e-3)
        u = np.maximum(np.abs(y - yc) / w, 1e-6)
        v = np.maximum(np.maximum(z - zb, 0.0) / hh, 1e-6)
        d = ((u ** self.n + v ** self.n) ** (1.0 / self.n) - 1.0) * np.minimum(w, hh)
        d = smax(d, zb - z, self.kb)
        d = smax(d, x0 - x, self.k0)
        return smax(d, x - x1, self.k1)


# Krallen (Spielnetz, fest): Schwerpunkt-y und Wurzel (x, z) je Zehe, innen -> aussen; vorn nach K1 (nur y zur Mitte, Teilung 4,1 cm)
PF_KRALLEN = {
    # 2c (SPEZ_2C.md 4): alle zehn Hinterkrallen um dx -0,070 nach hinten (Form/UV/Gewichte gleich) -> Wurzeln hier ebenso
    "H": dict(y=(0.166, 0.204, 0.240, 0.277, 0.315), x=tuple(round(v - 0.070, 4) for v in (-0.240, -0.213, -0.203, -0.212, -0.239)),
              z=(0.045, 0.043, 0.040, 0.042, 0.044),
              wy=(0.170, 0.202, 0.237, 0.271, 0.305)),
    "V": dict(y=(0.131, 0.172, 0.213, 0.254, 0.295), x=(0.467, 0.500, 0.513, 0.502, 0.468), z=(0.058, 0.053, 0.053, 0.053, 0.058),
              wy=(0.133, 0.166, 0.217, 0.243, 0.287)),   # wy: Wurzel-y (vorn nach K1)
}
K1_FAKTOR = 4.1 / 4.6 - 1.0   # vorn: dy = (y_kralle - y_mitte) * K1_FAKTOR (SPEZ 0 Nr. 4)
# Zehen (Soll): Stirn vor der Krallenwurzel, Oberkante, halbe Breite/Laenge; Zeh 1 (innen) kleiner
# Runde 2: Zehen laenger (Wurst, hinten im Fuss verankert), schmaler (Rillen bleiben nach Huelle/Voxeln offen), nach hinten 9 Grad
# angehoben; der Fuss-Loft endet hinter den Zehen
PF_ZEHE = {
    # Nachbesserung 1 (fix1, Pruefer Optik M2 "Zehen wie Finger"): hinten kuerzer (ax -16 %) und dicker (ay +12 %), Rillen oben flacher;
    # Stirn 2 mm weiter vor (Krallenwurzeln 2-5 mm in der Haut statt an der Oberflaeche, Pruefer Technik m7)
    # 2c (Kevins Vorlage: grosse runde Zehen dicht im Bogen): hinten kuerzer und runder (ax 0,027-0,031 -> 0,021-0,024), etwas breiter
    "H": dict(stirn=0.0095, oben=(0.0440, 0.0525, 0.0530, 0.0525, 0.0480), ay=(0.0152, 0.0166, 0.0169, 0.0166, 0.0161),
              ax=(0.0215, 0.0232, 0.0238, 0.0232, 0.0220), kipp=math.radians(9.0)),
    "V": dict(stirn=0.0125, oben=(0.0615, 0.0630, 0.0640, 0.0630, 0.0615), ay=(0.0150, 0.0168, 0.0170, 0.0168, 0.0152),
              ax=(0.036, 0.040, 0.041, 0.040, 0.037), kipp=math.radians(9.0)),
}
PF_TEILE = {
    # 2c (SPEZ_2C.md 4, Kevin 10.11.: "fussform wie menschen"): Hinterfuss 29 cm statt 43 (Soll mit Fell: Ferse x -0,555, Zehenstirn
    # -0,265), Ferse rund und breit (von oben Superellipse, von der Seite Radius ~4 cm), Platte bei x -0,33 18 cm, Ferse x -0,50 15,6 cm,
    # Rist faellt vom Schienbein (x -0,40, z 0,15) zu den Zehen (x -0,30, z 0,064). Bein: Hinterkante unten an die neue Ferse
    # (-0,548..-0,560 bis z 0,12, dann zur Hacke -0,600 bei z 0,20), unten etwas schmaler (Ferse 15-17 cm). Oben wie baer-pfoten (fix1-Kegel
    # und form_2c formen darueber).
    "H": dict(
        bein=PfBein(Z=[0.03, 0.06, 0.10, 0.12, 0.14, 0.165, 0.20, 0.25, 0.30, 0.33, 0.37],
                    xb=[-0.548, -0.553, -0.560, -0.566, -0.574, -0.584, -0.598, -0.606, -0.610, -0.610, -0.605],   # f7: Hacke stetiger
                    xf=[-0.40, -0.40, -0.40, -0.40, -0.395, -0.398, -0.402, -0.375, -0.30, -0.24, -0.172],
                    hw=[0.066, 0.075, 0.084, 0.088, 0.090, 0.092, 0.1025, 0.1175, 0.137, 0.168, 0.185],   # f14: Ferse von hinten rund (unten schmaler)
                    yc=[0.242, 0.242, 0.242, 0.243, 0.244, 0.245, 0.247, 0.250, 0.253, 0.255, 0.257],
                    n=2.2, z0=0.03, z1=0.37),
        # fix1 2c: Fersenlaenge bleibt (Probe fix1/probe/pc.py: 7 mm kuerzere Ferse -> im Sitzen muss das Sprunggelenk tiefer, dann
        # liegt der Unterschenkel im Boden und die Beckenloesung laeuft weg)
        fuss=PfFuss(X=[-0.555, -0.553, -0.550, -0.546, -0.540, -0.532, -0.522, -0.510, -0.495, -0.480, -0.460, -0.430, -0.400, -0.375,
                       -0.355, -0.335, -0.320, -0.310, -0.302],
                    # f14: von unten oval statt Rechteck (Ferse schmaler, vorn breit)
                    # fix1 2c (Pruefbericht M2 "im Ton eine laengliche Platte mit geraden Seiten"): Umriss als Ei - Ferse runder und
                    # breiter, Mitte 1 cm je Seite breiter als die Zehenreihe vorn (Fellkranz als Form, nicht nur Textur); Laenge gleich
                    w=[0.038, 0.050, 0.058, 0.065, 0.071, 0.076, 0.079, 0.082, 0.086, 0.090, 0.094, 0.097, 0.099, 0.101,
                       0.101, 0.100, 0.099, 0.098, 0.097],
                    zb=[0.040, 0.030, 0.022, 0.015, 0.009, 0.005, 0.002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0],
                    # f15: Fersen-Oberkante tiefer (0,115 -> 0,085), sonst stand sie als Kante/Ring ueber das Bein (Ansicht von hinten)
                    zt=[0.085, 0.090, 0.095, 0.100, 0.106, 0.112, 0.118, 0.124, 0.130, 0.137, 0.145, 0.155, 0.152, 0.128,
                        0.105, 0.085, 0.073, 0.067, 0.064],
                    yc=[0.242] * 19, n=2.4, x0=-0.555, x1=-0.302, kb=0.040, k0=0.020, k1=0.02, hf=0.007),   # f14: n 2,8 -> 2,4 (Querschnitt runder, kein Klotz von hinten)
    ),
    "V": dict(
        bein=PfBein(Z=[0.03, 0.06, 0.08, 0.11, 0.15, 0.20, 0.25, 0.30, 0.33, 0.37],
                    xb=[0.237, 0.235, 0.231, 0.226, 0.218, 0.205, 0.190, 0.160, 0.130, 0.105],
                    xf=[0.395, 0.398, 0.400, 0.400, 0.401, 0.400, 0.405, 0.430, 0.470, 0.505],
                    hw=[0.093, 0.092, 0.091, 0.091, 0.092, 0.1025, 0.115, 0.137, 0.165, 0.190],
                    yc=[0.213, 0.215, 0.217, 0.220, 0.223, 0.226, 0.229, 0.232, 0.234, 0.236],
                    n=2.2, z0=0.03, z1=0.37),
        fuss=PfFuss(X=[0.240, 0.250, 0.260, 0.272, 0.282, 0.290, 0.296, 0.300, 0.330, 0.360, 0.380, 0.395, 0.405, 0.415, 0.428, 0.440,
                       0.448, 0.456, 0.462],
                    # fix1 (Pruefer Technik M3 "Pranke von unten ein Kasten"): hinten schmaler und weicher aufgesetzt -> Umriss von unten oval
                    w=[0.056, 0.061, 0.066, 0.071, 0.075, 0.078, 0.080, 0.082, 0.090, 0.096, 0.100, 0.102, 0.103, 0.103, 0.103, 0.102,
                       0.101, 0.100, 0.099],
                    zb=[0.048, 0.042, 0.036, 0.029, 0.019, 0.011, 0.0065, 0.004, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0],
                    zt=[0.160, 0.160, 0.160, 0.160, 0.160, 0.160, 0.160, 0.160, 0.160, 0.163, 0.163, 0.150, 0.124, 0.104, 0.090, 0.081,
                        0.079, 0.077, 0.076],
                    yc=[0.220, 0.218, 0.216, 0.215, 0.214, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213,
                        0.213, 0.213, 0.213], n=2.4, x0=0.240, x1=0.462, kb=0.040, k0=0.016, k1=0.02, hf=0.007),
        ballen=dict(c=(0.262, 0.238, 0.0490), r=0.033),   # fix1: Handwurzelballen groesser, tiefer (unten 1,6 cm), mehr zur Mitte
    ),
}
PF_K = dict(bein_fuss=0.022, zehen=0.006, ballen=0.010, bett=0.006)
PF_BETT = dict(R=(0.0132, 0.0102, 0.0137), dx=-0.0035, dz=-0.0035)   # fix1: etwas groesser/hoeher (Krallenwurzeln in die Haut)
_PF_BETT_ALT = dict(R=(0.0120, 0.0095, 0.0125), dx=-0.0040, dz=-0.0045)   # Krallenbett (Soll): Ellipsoid, Mitte = Wurzel + (dx, 0, dz); klein, sonst fuellen sich die Zehenrillen


def pf_zehen_ell(vh, soll=False):
    """Fuenf Zehen als laengliche, nach hinten um 'kipp' angehobene Ellipsoide (Haut; soll=True: Soll mit Huelle):
    (Mitte, Halbachsen, Kippwinkel); Stirn = Krallenwurzel + stirn, Unterseite 1,5 mm unter dem Boden (flacher Abdruck), Oberkante = oben."""
    K, Z = PF_KRALLEN[vh], PF_ZEHE[vh]
    hz = 0.0 if soll else PF_HUELLE_ZEHE
    a = Z["kipp"]
    out = []
    for i in range(5):
        stirn = K["x"][i] + Z["stirn"] - hz
        oben = Z["oben"][i] - hz
        ax = Z["ax"][i] - hz
        h_off = 0.5 * (oben - PF_BODEN + 0.0015)
        az = math.sqrt(max(h_off ** 2 - (ax * math.sin(a)) ** 2, 1e-8)) / math.cos(a)
        f_off = math.sqrt((ax * math.cos(a)) ** 2 + (az * math.sin(a)) ** 2)
        out.append(((stirn - f_off, K["y"][i], PF_BODEN - 0.0015 + h_off), (ax, Z["ay"][i] - hz, az), a))
    return out


def pf_ell_kipp(x, y, z, C, R, a):
    """Ellipsoid um die y-Achse durch C gekippt (a > 0: hinteres Ende hoeher); Drehung erhaelt Abstaende."""
    dx, dz = x - C[0], z - C[2]
    ca, sa = math.cos(a), math.sin(a)
    return ell(C[0] + dx * ca - dz * sa, y, C[2] + dx * sa + dz * ca, C, R)


def pf_feld_s(vh, x, y, z, teil="alle", soll=False):
    """Abstandsfeld der Haut einer linken Pfote in Spielmetern (vh 'V' oder 'H'). teil='fuss': ohne Bein (Taubin/Huelle).
    soll=True: das Soll des fertigen Spielnetzes (Haut + Huelle); daraus rechnet baer_export_pfote.py die Huellendicke."""
    T = PF_TEILE[vh]
    d = T["fuss"](x, y, z, soll)
    if teil != "fuss":
        d = smin(d, T["bein"](x, y, z, soll), PF_K["bein_fuss"])
    for C, R, a in pf_zehen_ell(vh, soll):
        d = smin(d, pf_ell_kipp(x, y, z, C, R, a), PF_K["zehen"])
    K = PF_KRALLEN[vh]
    hz = 0.0 if soll else PF_HUELLE_ZEHE
    Rb = tuple(r - hz for r in PF_BETT["R"])
    for i in range(5):
        Cb = (K["x"][i] + PF_BETT["dx"], K["wy"][i], K["z"][i] + PF_BETT["dz"])
        d = smin(d, ell(x, y, z, Cb, Rb), PF_K["bett"])
    if "ballen" in T:
        b = T["ballen"]
        rb = b["r"] - (0.0 if soll else PF_HUELLE_BALLEN)
        d = smin(d, np.sqrt((x - b["c"][0]) ** 2 + (y - b["c"][1]) ** 2 + (z - b["c"][2]) ** 2) - rb, PF_K["ballen"])
    return smax(d, PF_BODEN - z, 0.003)


def pfote_feld_fn(vh, s, teil="alle", soll=False):
    """Feld im Hochmodell (Welt, Meter des Hochmodells) fuer die Pfote vh ('V'/'H') der Seite s (+1 links, -1 rechts)."""

    def fn(a, b, c):
        xs, ys, zs = pf_h2s(a, b, c)
        return pf_feld_s(vh, xs, ys * s, zs, teil, soll) / PF_G

    return fn
# ------------------------------------------------------------------ Ende des Abstandsfelds

# Stufen: form = nur Haut, kopf = schnelle Nahbilder, sonst volle Qualitaet
QUAL = {"form": 0, "kopf": 1, "nah": 1}.get(MODE, 2)
H_KOPF = {0: 0.0034, 1: 0.0034, 2: 0.0024}[QUAL] if MODE != "nah" else 0.0024
SPALT = max(0.0025, H_KOPF * 1.05)
H_FEIN = {0: 0.0011, 1: 0.0011, 2: 0.0007}[QUAL]
H_ZEH = {0: 0.0052, 1: 0.0042, 2: 0.0030}[QUAL]
FELL_KOERPER = {0: 0.0, 1: 0.5, 2: 1.0}[QUAL]
HAAR_FAKTOR = {0: 0.0, 1: 0.55, 2: 1.35}[QUAL] if MODE != "nah" else 1.35
GRAS = {0: 0.0, 1: 0.35, 2: 1.0}[QUAL]


def dbg(*a):
    print("BAER_ZEIT %.1f" % (time.time() - T_START), *a, flush=True)


bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = scene.collection
FPS = 30
scene.render.fps = FPS

# ------------------------------------------------------------------ Koerper aus Metabaellen
mb = bpy.data.metaballs.new("baer")
mb.resolution = 0.024
mb.render_resolution = 0.024
mb.threshold = 0.62
mo = bpy.data.objects.new("baer", mb)
col.objects.link(mo)


def lz(z):
    t = max(0.0, min(1.0, (z - 0.13) / 0.33))
    return z + LZ_HUB * t * t * (3 - 2 * t)


def ball(x, y, z, r):
    e = mb.elements.new(type="BALL")
    e.co = (x, y, lz(z))
    e.radius = r


# Lauf baer-pfoten: untere Beinkugeln in Spielmetern (x, y links, z, Radius Hochmodell); lz wird hier rueckwaerts gerechnet
# vorn bleiben die oberen drei Kugeln der alten Kette, hinten zwei (die dritte stand bei Spiel-z 0,31 zu weit vorn: Schienbein in
# 25 cm Hoehe sonst 3,5 cm vor dem Soll); gemessen mit _arbeit/baer_pfote/hoch/probe_hoch.py (Rumpfhaut ueber z 0,36 p95 0,1 cm)
PF_KUGELN = {
    "V": ((0.298, 0.230, 0.225, 0.180), (0.296, 0.227, 0.170, 0.150), (0.296, 0.224, 0.120, 0.120)),
    "H": ((-0.460, 0.255, 0.300, 0.210), (-0.488, 0.252, 0.245, 0.180), (-0.503, 0.249, 0.190, 0.150), (-0.508, 0.246, 0.140, 0.120)),
}
PF_KETTE_ALT = {k: int(v) for k, v in (t.split(":") for t in os.environ.get("BAER_PF_KETTE", "V:3,H:2").split(","))}   # so viele Kugeln der alten Unterschenkel-/Unterarm-Kette bleiben genau
if os.environ.get("BAER_PF_KUGELN"):
    import json as _json
    PF_KUGELN = {k: tuple(tuple(v) for v in w) for k, w in _json.loads(os.environ["BAER_PF_KUGELN"]).items()}
_LZ_Z = np.linspace(-0.1, 1.6, 17001)
_LZ_W = np.array([lz(float(_z)) for _z in _LZ_Z])


def ball_s(xs, ys, zs, r):
    zh = zs / PF_G + PF_ZMIN
    ball(xs / PF_G + PF_X0, ys / PF_G, float(np.interp(zh, _LZ_W, _LZ_Z)), r)


def chain(p0, p1, r0, r1, n):
    for i in range(n):
        t = i / max(1, n - 1)
        ball(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t, p0[2] + (p1[2] - p0[2]) * t, r0 + (r1 - r0) * t)


def chain_teil(p0, p1, r0, r1, n, m):
    """Lauf baer-pfoten: nur die ersten m Kugeln einer Kette chain(p0, p1, r0, r1, n), genau dieselbe Rechnung."""
    for i in range(m):
        t = i / max(1, n - 1)
        ball(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t, p0[2] + (p1[2] - p0[2]) * t, r0 + (r1 - r0) * t)


# Rumpf: Kruppe tiefer als der Schulterbuckel, tiefe Brust
chain((-0.78, 0, 0.75), (-0.52, 0, 0.77), 0.42, 0.50, 3)
chain((-0.40, 0, 0.74), (0.12, 0, 0.74), 0.50, 0.53, 4)
chain((0.20, 0, 0.73), (0.46, 0, 0.74), 0.48, 0.38, 3)
ball(0.33, 0, 1.03, 0.34)    # Buckel
ball(0.15, 0, 1.02, 0.36)
ball(-0.05, 0, 0.95, 0.28)
# Dicker Hals, der nach vorn abfaellt; der Kopf kommt aus dem Abstandsfeld
chain((0.52, 0, 0.86), (0.84, 0, 0.73), 0.40, 0.25, 3)
for s in (-1, 1):
    # Vorderbein: lang und saeulig, Pranken leicht einwaerts
    chain((0.30, s * 0.29, 0.78), (0.33, s * 0.32, 0.40), 0.30, 0.235, 3)
    # Lauf baer-pfoten: von der alten Kette (0.33, 0.32, 0.40) -> (0.35, 0.31, 0.14), r 0.25 -> 0.205, 6 Kugeln bleiben die oberen drei
    # (bis Spiel-z 0,30) genau; die unteren drei duenner und nach hinten (PF_KUGELN, Spielmeter); die Pranken-Kette (alt :901) ist weg,
    # die Pranke kommt aus dem Pfotenfeld
    chain_teil((0.33, s * 0.32, 0.40), (0.35, s * 0.31, 0.14), 0.25, 0.205, 6, PF_KETTE_ALT["V"])
    for _xs, _ys, _zs, _r in PF_KUGELN["V"]:
        ball_s(_xs, s * _ys, _zs, _r)
    # Hinterbein: maechtige Keule, Sohlengaenger mit langem Fuss
    chain((-0.72, s * 0.33, 0.72), (-0.57, s * 0.36, 0.42), 0.35, 0.26, 3)
    # Lauf baer-pfoten: alte Kette (-0.58, 0.35, 0.40) -> (-0.71, 0.33, 0.16), r 0.26 -> 0.20, 6 Kugeln: obere drei genau, untere drei
    # neu (PF_KUGELN); die Fuss-Kette (alt :905) ist weg
    chain_teil((-0.58, s * 0.35, 0.40), (-0.71, s * 0.33, 0.16), 0.26, 0.20, 6, PF_KETTE_ALT["H"])
    for _xs, _ys, _zs, _r in PF_KUGELN["H"]:
        ball_s(_xs, s * _ys, _zs, _r)
# Stummelschwanz
chain((-1.06, 0, 0.70), (-1.15, 0, 0.68), 0.11, 0.08, 2)

depsgraph = bpy.context.evaluated_depsgraph_get()
bpy.context.view_layer.objects.active = mo
mo.select_set(True)
bpy.ops.object.convert(target="MESH")
body = bpy.context.active_object
body.name = "baer_koerper"

# Gleichmaessiges Netz: keine Splitter-Dreiecke, die beim Biegen reissen
start_tris = sum(len(p.vertices) - 2 for p in body.data.polygons)
rm = body.modifiers.new("gleich", "REMESH")
rm.mode = "VOXEL"
rm.voxel_size = 0.052
rm.use_smooth_shade = True
bpy.ops.object.modifier_apply(modifier=rm.name)
sm = body.modifiers.new("glatt", "SMOOTH")
sm.factor = 0.6
sm.iterations = 8
bpy.ops.object.modifier_apply(modifier=sm.name)
for p in body.data.polygons:
    p.use_smooth = True
body_tris = sum(len(p.vertices) - 2 for p in body.data.polygons)
dbg("Koerper fertig", body_tris)
# _anim: dieselbe Haut, zwei Stufen Catmull-Clark: gleiche Form, aber ohne die Kanten der 5,2-cm-Voxel (Kantenlaenge rund
# 4,5 cm, Knick im Mittel 7,8 Grad). Im Hochmodell verdeckt das Fell sie; im Spielnetz schoben die Fellhuelle sie entlang der
# Normalen bis in den Umriss (anim_modell.md). Nur das Spielnetz liest dieses Objekt.
rund = body.copy()
rund.data = body.data.copy()
rund.name = "baer_koerper_rund"
col.objects.link(rund)
_sub = rund.modifiers.new("rund", "SUBSURF")
_sub.levels = 2
_sub.render_levels = 2
_dg = bpy.context.evaluated_depsgraph_get()
_me_r = bpy.data.meshes.new_from_object(rund.evaluated_get(_dg))
rund.modifiers.clear()
rund.data = _me_r
rund.hide_render = True
rund.hide_set(True)
dbg("Rundhaut fertig", len(rund.data.vertices), "Punkte")


# ------------------------------------------------------------------ Materialien
def mix_rgba(N, L, fac, a, b):
    m = N.new("ShaderNodeMix")
    m.data_type = "RGBA"
    fi = [i for i in m.inputs if i.type == "VALUE" and i.name == "Factor"][0]
    ai = [i for i in m.inputs if i.type == "RGBA" and i.name == "A"][0]
    bi = [i for i in m.inputs if i.type == "RGBA" and i.name == "B"][0]
    out = [o for o in m.outputs if o.type == "RGBA"][0]
    if hasattr(fac, "links"):
        L.new(fac, fi)
    else:
        fi.default_value = fac
    for sock, val in ((ai, a), (bi, b)):
        if hasattr(val, "links"):
            L.new(val, sock)
        else:
            sock.default_value = (val[0], val[1], val[2], 1)
    return out


def maprange(N, L, v, a, b, c, d):
    m = N.new("ShaderNodeMapRange")
    m.clamp = True
    L.new(v, m.inputs["Value"])
    m.inputs["From Min"].default_value = a
    m.inputs["From Max"].default_value = b
    m.inputs["To Min"].default_value = c
    m.inputs["To Max"].default_value = d
    return m.outputs[0]


fur = bpy.data.materials.new("fell")
fur.use_nodes = True
N, L = fur.node_tree.nodes, fur.node_tree.links
b = N["Principled BSDF"]
tc = N.new("ShaderNodeTexCoord")
sep = N.new("ShaderNodeSeparateXYZ")
L.new(tc.outputs["Generated"], sep.inputs[0])
# Grob: Fleckung im Fell. Fein: Haarstriche, gestaucht entlang des Koerpers.
mapg = N.new("ShaderNodeMapping")
mapg.inputs["Scale"].default_value = (24, 118, 118)
L.new(tc.outputs["Generated"], mapg.inputs["Vector"])
hair = N.new("ShaderNodeTexNoise")
hair.inputs["Scale"].default_value = 3.6
hair.inputs["Detail"].default_value = 11
hair.inputs["Roughness"].default_value = 0.72
L.new(mapg.outputs["Vector"], hair.inputs["Vector"])
big = N.new("ShaderNodeTexNoise")
big.inputs["Scale"].default_value = 11
big.inputs["Detail"].default_value = 7
L.new(tc.outputs["Generated"], big.inputs["Vector"])
base = mix_rgba(N, L, maprange(N, L, big.outputs["Fac"], 0.32, 0.68, 0, 1), (0.035, 0.018, 0.008), (0.06, 0.03, 0.013))
tips = mix_rgba(N, L, maprange(N, L, hair.outputs["Fac"], 0.42, 0.64, 0, 1), (0.02, 0.011, 0.005), (0.09, 0.05, 0.022))
col1 = mix_rgba(N, L, 0.56, base, tips)
# Beine und Bauch dunkler, Oberseite heller
legs = maprange(N, L, sep.outputs[2], 0.12, 0.36, 0.62, 0.0)
col2 = mix_rgba(N, L, legs, col1, (0.02, 0.011, 0.007))
top = maprange(N, L, sep.outputs[2], 0.68, 0.98, 0.0, 0.42)
col3 = mix_rgba(N, L, top, col2, (0.07, 0.038, 0.016))
L.new(col3, b.inputs["Base Color"])
L.new(maprange(N, L, hair.outputs["Fac"], 0.3, 0.7, 0.86, 0.66), b.inputs["Roughness"])
b.inputs["Sheen Weight"].default_value = 0.0
bp = N.new("ShaderNodeBump")
bp.inputs["Strength"].default_value = 1.0
bp.inputs["Distance"].default_value = 0.05
L.new(hair.outputs["Fac"], bp.inputs["Height"])
L.new(bp.outputs["Normal"], b.inputs["Normal"])
body.data.materials.append(fur)


def plain(name, rgb, rough=0.5, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes["Principled BSDF"]
    n.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1)
    n.inputs["Roughness"].default_value = rough
    return m


def attr_node(N, name):
    a = N.new("ShaderNodeAttribute")
    a.attribute_type = "GEOMETRY"
    a.attribute_name = name
    return a


# Haut des Kopfes: Farbe und Feuchte kommen je Punkt aus dem Feld
SKIN = bpy.data.materials.new("kopfhaut")
SKIN.use_nodes = True
_N, _L = SKIN.node_tree.nodes, SKIN.node_tree.links
_b = _N["Principled BSDF"]
_L.new(attr_node(_N, "haut").outputs["Color"], _b.inputs["Base Color"])
_f = attr_node(_N, "feucht")
_L.new(maprange(_N, _L, _f.outputs["Fac"], 0.0, 1.0, 0.78, 0.26), _b.inputs["Roughness"])
_L.new(maprange(_N, _L, _f.outputs["Fac"], 0.0, 0.5, 0.10, 0.5), _b.inputs["Specular IOR Level"])
_tc = _N.new("ShaderNodeTexCoord")
_nz = _N.new("ShaderNodeTexNoise")
_nz.inputs["Scale"].default_value = 700
_nz.inputs["Detail"].default_value = 3
_L.new(_tc.outputs["Object"], _nz.inputs["Vector"])
_bp = _N.new("ShaderNodeBump")
_bp.inputs["Strength"].default_value = 0.5
_bp.inputs["Distance"].default_value = 0.0012
_L.new(_nz.outputs["Fac"], _bp.inputs["Height"])
_L.new(_bp.outputs["Normal"], _b.inputs["Normal"])

# Nase: anthrazit, ledrig-feuchte Koernung aus kleinen Zellen
NASEM = bpy.data.materials.new("nase")
NASEM.use_nodes = True
_N, _L = NASEM.node_tree.nodes, NASEM.node_tree.links
_b = _N["Principled BSDF"]
_L.new(attr_node(_N, "haut").outputs["Color"], _b.inputs["Base Color"])
_tc = _N.new("ShaderNodeTexCoord")
_vo = _N.new("ShaderNodeTexVoronoi")
_vo.feature = "F1"
_vo.inputs["Scale"].default_value = 620
_L.new(_tc.outputs["Object"], _vo.inputs["Vector"])
_nz = _N.new("ShaderNodeTexNoise")
_nz.inputs["Scale"].default_value = 230
_nz.inputs["Detail"].default_value = 4
_L.new(_tc.outputs["Object"], _nz.inputs["Vector"])
_L.new(maprange(_N, _L, _nz.outputs["Fac"], 0.32, 0.68, 0.30, 0.52), _b.inputs["Roughness"])
_b.inputs["Specular IOR Level"].default_value = 0.30
_bp = _N.new("ShaderNodeBump")
_bp.inputs["Strength"].default_value = 0.85
_bp.inputs["Distance"].default_value = 0.0016
_L.new(_vo.outputs["Distance"], _bp.inputs["Height"])
_L.new(_bp.outputs["Normal"], _b.inputs["Normal"])

# Auge: Iris und Pupille um die lokale z-Achse
EYEM = bpy.data.materials.new("auge")
EYEM.use_nodes = True
_N, _L = EYEM.node_tree.nodes, EYEM.node_tree.links
_b = _N["Principled BSDF"]
_tc = _N.new("ShaderNodeTexCoord")
_sp = _N.new("ShaderNodeSeparateXYZ")
_L.new(_tc.outputs["Object"], _sp.inputs[0])
_xy1 = _N.new("ShaderNodeMath")
_xy1.operation = "MULTIPLY"
_L.new(_sp.outputs[0], _xy1.inputs[0])
_L.new(_sp.outputs[0], _xy1.inputs[1])
_xy2 = _N.new("ShaderNodeMath")
_xy2.operation = "MULTIPLY"
_L.new(_sp.outputs[1], _xy2.inputs[0])
_L.new(_sp.outputs[1], _xy2.inputs[1])
_xy3 = _N.new("ShaderNodeMath")
_xy3.operation = "ADD"
_L.new(_xy1.outputs[0], _xy3.inputs[0])
_L.new(_xy2.outputs[0], _xy3.inputs[1])
_rr = _N.new("ShaderNodeMath")
_rr.operation = "SQRT"
_L.new(_xy3.outputs[0], _rr.inputs[0])
_nz = _N.new("ShaderNodeTexNoise")
_nz.inputs["Scale"].default_value = 520
_nz.inputs["Detail"].default_value = 3
_L.new(_tc.outputs["Object"], _nz.inputs["Vector"])
_iris = mix_rgba(_N, _L, maprange(_N, _L, _nz.outputs["Fac"], 0.35, 0.65, 0, 1), (0.085, 0.034, 0.007), (0.20, 0.095, 0.022))
_iris2 = mix_rgba(_N, _L, maprange(_N, _L, _rr.outputs[0], 0.0120, 0.0165, 0, 1), _iris, (0.012, 0.006, 0.003))
_col = mix_rgba(_N, _L, maprange(_N, _L, _rr.outputs[0], 0.0048, 0.0058, 1, 0), _iris2, (0.002, 0.002, 0.002))
_L.new(_col, _b.inputs["Base Color"])
_b.inputs["Roughness"].default_value = 0.09
_b.inputs["IOR"].default_value = 1.38

# Kralle: Horn mit dunkler Wurzel und heller Spitze
CLAWM = bpy.data.materials.new("kralle")
CLAWM.use_nodes = True
_N, _L = CLAWM.node_tree.nodes, CLAWM.node_tree.links
_b = _N["Principled BSDF"]
_tt = attr_node(_N, "krallet")
_rp = _N.new("ShaderNodeValToRGB")
_rp.color_ramp.elements[0].position = 0.16
_rp.color_ramp.elements[0].color = (0.020, 0.013, 0.009, 1)
_rp.color_ramp.elements[1].position = 0.98
_rp.color_ramp.elements[1].color = (0.30, 0.255, 0.20, 1)
_e = _rp.color_ramp.elements.new(0.58)
_e.color = (0.085, 0.060, 0.042, 1)
_L.new(_tt.outputs["Fac"], _rp.inputs["Fac"])
_tc = _N.new("ShaderNodeTexCoord")
_nz = _N.new("ShaderNodeTexNoise")
_nz.inputs["Scale"].default_value = 90
_nz.inputs["Detail"].default_value = 5
_L.new(_tc.outputs["Object"], _nz.inputs["Vector"])
_L.new(mix_rgba(_N, _L, maprange(_N, _L, _nz.outputs["Fac"], 0.35, 0.65, 0.0, 0.22), _rp.outputs["Color"], (0.018, 0.012, 0.008)), _b.inputs["Base Color"])
_b.inputs["Roughness"].default_value = 0.56
_bp = _N.new("ShaderNodeBump")
_bp.inputs["Strength"].default_value = 0.35
_bp.inputs["Distance"].default_value = 0.0015
_L.new(_nz.outputs["Fac"], _bp.inputs["Height"])
_L.new(_bp.outputs["Normal"], _b.inputs["Normal"])

MOUTH = plain("maul", (0.115, 0.020, 0.026), 0.42)
GUM = plain("gum", (0.13, 0.026, 0.032), 0.38)
TOOTH = plain("zahn", (0.62, 0.55, 0.40), 0.36)


# ------------------------------------------------------------------ Skelett
arm = bpy.data.armatures.new("skelett")
ao = bpy.data.objects.new("skelett", arm)
col.objects.link(ao)
bpy.context.view_layer.objects.active = ao
bpy.ops.object.mode_set(mode="EDIT")
EB = arm.edit_bones
BONES = {}


def bone(name, head, tail, parent=None, connect=False):
    e = EB.new(name)
    e.head = (head[0], head[1], lz(head[2]))
    e.tail = (tail[0], tail[1], lz(tail[2]))
    e.roll = 0
    if parent:
        e.parent = EB[parent]
        e.use_connect = connect
    BONES[name] = e
    return e


bone("wurzel", (-0.58, 0, 0.66), (-0.16, 0, 0.66))
bone("ruecken", (-0.16, 0, 0.66), (0.26, 0, 0.78), "wurzel", True)
bone("brust", (0.26, 0, 0.78), (0.58, 0, 0.84), "ruecken", True)
bone("hals", (0.58, 0, 0.84), (0.86, 0, 0.80), "brust", True)
bone("kopf", (0.86, 0, 0.80), (1.38, 0, 0.66), "hals", True)
# Kiefergelenk unter dem Ohr, der Knochen laeuft die Kinnlinie entlang
_kk = EB.new("kiefer")
_kk.head = tuple(l2w((0.075, 0.0, -0.060)))
_kk.tail = tuple(l2w((0.45, 0.0, -0.070)))
_kk.roll = 0
_kk.parent = EB["kopf"]
KIEFER_STUFEN = (1, 2, 3, 4, 5, 6, 7)
for _n in KIEFER_STUFEN:
    _kh = EB.new("kiefer_%d" % _n)
    _kh.head = _kk.head.copy()
    _kh.tail = _kk.tail.copy()
    _kh.roll = 0
    _kh.parent = EB["kopf"]
bone("schwanz", (-1.02, 0, 0.72), (-1.26, 0, 0.72), "wurzel")
for s, n in ((-1, "R"), (1, "L")):
    bone("oberarm" + n, (0.30, s * 0.30, 0.76), (0.33, s * 0.32, 0.38), "brust")
    bone("unterarm" + n, (0.33, s * 0.32, 0.38), (0.35, s * 0.31, 0.13), "oberarm" + n, True)
    bone("pranke" + n, (0.35, s * 0.31, 0.13), (0.56, s * 0.29, 0.06), "unterarm" + n, True)
    bone("schenkel" + n, (-0.70, s * 0.335, 0.72), (-0.55, s * 0.35, 0.38), "wurzel")
    bone("wade" + n, (-0.55, s * 0.35, 0.38), (-0.72, s * 0.33, 0.13), "schenkel" + n, True)
    bone("fuss" + n, (-0.72, s * 0.33, 0.13), (-0.42, s * 0.32, 0.06), "wade" + n, True)
bpy.ops.object.mode_set(mode="OBJECT")

# ------------------------------------------------------------------ Gewichte: nah am Knochen zaehlt
NAMES = [b.name for b in arm.bones if not b.name.startswith("kiefer")]
SEG = {b.name: (b.head_local.copy(), b.tail_local.copy()) for b in arm.bones}
for nm in NAMES:
    body.vertex_groups.new(name=nm)


def seg_dist(p, a, c):
    ac = c - a
    t = max(0.0, min(1.0, (p - a).dot(ac) / ac.length_squared))
    return (p - (a + ac * t)).length


def side_of(nm):
    return {"R": -1, "L": 1}.get(nm[-1]) if nm not in ("kopf", "hals", "brust", "ruecken", "wurzel", "schwanz") else 0


WEIGHTS = []
for v in body.data.vertices:
    p = v.co
    cand = []
    for nm in NAMES:
        sd = side_of(nm)
        if sd and p.y * sd < -0.05:
            continue
        d = seg_dist(p, *SEG[nm])
        if sd:
            d *= 1.1
        cand.append((d, nm))
    cand.sort()
    cand = cand[:3]
    w = [1.0 / max(d, 0.03) ** 3 for d, _ in cand]
    tot = sum(w)
    WEIGHTS.append({nm: wt / tot for (d, nm), wt in zip(cand, w)})

nb = [[] for _ in body.data.vertices]
for e in body.data.edges:
    a, c = e.vertices
    nb[a].append(c)
    nb[c].append(a)
for _ in range(7):
    new = []
    for i, wmap in enumerate(WEIGHTS):
        out = {k: v * 0.45 for k, v in wmap.items()}
        n = nb[i]
        if n:
            f = 0.55 / len(n)
            for j in n:
                for k, v in WEIGHTS[j].items():
                    out[k] = out.get(k, 0.0) + v * f
        new.append(out)
    WEIGHTS = new
for i, wmap in enumerate(WEIGHTS):
    top = sorted(wmap.items(), key=lambda kv: -kv[1])[:4]
    tot = sum(v for _, v in top)
    for k, v in top:
        body.vertex_groups[k].add([i], v / tot, "REPLACE")

mod = body.modifiers.new("skelett", "ARMATURE")
mod.object = ao
body.parent = ao
dbg("Gewichte Koerper fertig")


def sstep(a, c, x):
    t = max(0.0, min(1.0, (x - a) / (c - a)))
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ Teile, die am Knochen haengen
def on_bone(o, bname):
    bpy.context.view_layer.update()
    bn = arm.bones[bname]
    mw = o.matrix_world.copy()
    o.parent = ao
    o.parent_type = "BONE"
    o.parent_bone = bname
    tail_world = ao.matrix_world @ bn.matrix_local @ Matrix.Translation((0, bn.length, 0))
    o.matrix_parent_inverse = tail_world.inverted()
    o.matrix_basis = mw


def netz_objekt(name, V, F, mat, attr_rgb=None, attr_f=None, smooth=True):
    """Netz aus Weltkoordinaten; attr_rgb/attr_f sind Attribute je Punkt."""
    me = bpy.data.meshes.new(name)
    fl = F.tolist() if hasattr(F, "tolist") else F
    me.from_pydata(np.asarray(V, dtype=float).tolist(), [], fl)
    me.update()
    if smooth:
        me.shade_smooth()
    if attr_rgb is not None:
        for key, rgb in attr_rgb.items():
            ca = me.color_attributes.new(key, "FLOAT_COLOR", "POINT")
            rgba = np.ones((len(V), 4), dtype=np.float32)
            rgba[:, :3] = rgb
            ca.data.foreach_set("color", rgba.ravel())
    if attr_f is not None:
        for key, val in attr_f.items():
            at = me.attributes.new(key, "FLOAT", "POINT")
            at.data.foreach_set("value", np.asarray(val, dtype=np.float32))
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    col.objects.link(o)
    return o


def spiegel(V, Q):
    W = np.array(V)
    W[:, 1] *= -1
    return W, np.asarray(Q)[:, ::-1]


# Haarmaterial des Kopfes: Melanin und Roetung kommen je Straehne aus dem Feld
hk = bpy.data.materials.new("haar_kopf")
hk.use_nodes = True
Nk, Lk = hk.node_tree.nodes, hk.node_tree.links
Nk.remove(Nk["Principled BSDF"])
hbk = Nk.new("ShaderNodeBsdfHairPrincipled")
hbk.parametrization = "MELANIN"
hbk.inputs["Roughness"].default_value = 0.46
hbk.inputs["Radial Roughness"].default_value = 0.72
hbk.inputs["Coat"].default_value = 0.0
hbk.inputs["Random Color"].default_value = 0.08
hik = Nk.new("ShaderNodeHairInfo")
ml = Nk.new("ShaderNodeMath")
ml.operation = "ADD"
Lk.new(attr_node(Nk, "mel").outputs["Fac"], ml.inputs[0])
Lk.new(maprange(Nk, Lk, hik.outputs["Random"], 0.0, 1.0, -0.055, 0.055), ml.inputs[1])
ml2 = Nk.new("ShaderNodeMath")
ml2.operation = "SUBTRACT"
ml2.use_clamp = True
Lk.new(ml.outputs[0], ml2.inputs[0])
Lk.new(maprange(Nk, Lk, hik.outputs["Intercept"], 0.35, 1.0, 0.0, 0.17), ml2.inputs[1])
Lk.new(ml2.outputs[0], hbk.inputs["Melanin"])
Lk.new(attr_node(Nk, "rot").outputs["Fac"], hbk.inputs["Melanin Redness"])
Lk.new(hbk.outputs[0], Nk["Material Output"].inputs["Surface"])


def haar_objekt(name, pts, rad, attrs, bone_name, mat=hk):
    """Haar-Curves in Weltkoordinaten, hart am Knochen."""
    N_, M_ = pts.shape[0], pts.shape[1]
    cv = bpy.data.hair_curves.new(name)
    cv.add_curves([M_] * N_)
    cv.position_data.foreach_set("vector", pts.astype(np.float32).ravel())
    ra = cv.attributes.get("radius") or cv.attributes.new("radius", "FLOAT", "POINT")
    ra.data.foreach_set("value", rad.astype(np.float32).ravel())
    for key, val in attrs.items():
        at = cv.attributes.new(key, "FLOAT", "CURVE")
        at.data.foreach_set("value", np.asarray(val, dtype=np.float32))
    cv.materials.append(mat)
    o = bpy.data.objects.new(name, cv)
    col.objects.link(o)
    on_bone(o, bone_name)
    return o


# ------------------------------------------------------------------ Kopf aus dem Feld
t0 = time.time()
_fk = lambda a, b, c: feld_kopf(a, b, c, SPALT)
KV, KQ = netz_aus_feld(_fk, (-0.42, -0.27, -0.28), (0.535, 0.27, 0.235), H_KOPF, grob=4)
dbg("Kopfnetz", len(KV), "Punkte", len(KQ), "Flaechen", "%.1fs" % (time.time() - t0))
# Treppen weg; Lippen und Ohr duerfen scharf bleiben, deshalb nur schwach
KV = glaette(KV, KQ, 0.35, 2)
rgb, feucht = haut_attribute(KV)
kopf = netz_objekt("kopf", l2w(KV), KQ, SKIN, {"haut": rgb}, {"feucht": feucht})
wk = kiefer_gewicht(KV[:, 0], KV[:, 1], KV[:, 2], SPALT)
wh = 1.0 - sst(-0.13, 0.0, KV[:, 0])
wkp = np.clip(1.0 - wk, 0.0, 1.0) * (1.0 - wh)
wbr = 1.0 - sst(-0.36, -0.19, KV[:, 0])
whl = np.clip(wh - wbr, 0.0, 1.0)


def gewichte_setzen(ob, name, w):
    vg = ob.vertex_groups.get(name) or ob.vertex_groups.new(name=name)
    q = np.round(np.clip(w, 0, 1) * 96).astype(int)
    for val in np.unique(q):
        if val > 0:
            vg.add(np.nonzero(q == val)[0].tolist(), float(val) / 96.0, "REPLACE")


gewichte_setzen(kopf, "kopf", wkp)
gewichte_setzen(kopf, "kiefer", wk * (1.0 - wh))
gewichte_setzen(kopf, "hals", whl)
gewichte_setzen(kopf, "brust", wbr)
_m = kopf.modifiers.new("skelett", "ARMATURE")
_m.object = ao
kopf.parent = ao
dbg("Kopf gewichtet")

# Lider (je Seite ein feines Netz) und Augaepfel
_lo = AUGE - 0.034
_hi = AUGE + 0.034
_lo[1] = max(_lo[1], 0.0)
LV, LQ = netz_aus_feld(feld_lid, _lo, _hi, H_FEIN, grob=4, rand=3.0)
LV = glaette(LV, LQ, 0.3, 1)
dbg("Lid", len(LV), "Punkte")
_lr = np.tile(np.array((0.0055, 0.0045, 0.0045)), (len(LV), 1))
_lf = np.full(len(LV), 0.15)
_lx, _ly, _lz = LV[:, 0] - AUGE[0], LV[:, 1] - AUGE[1], LV[:, 2] - AUGE[2]
for sgn, sn in ((1, "l"), (-1, "r")):
    if sgn > 0:
        _o = netz_objekt("lid_" + sn, l2w(LV), LQ, SKIN, {"haut": _lr}, {"feucht": _lf})
    else:
        _w, _q = spiegel(l2w(LV), LQ)
        _o = netz_objekt("lid_" + sn, _w, _q, SKIN, {"haut": _lr}, {"feucht": _lf})
    on_bone(_o, "kopf")
    # Augapfel: Pole auf der Blickachse, damit die Iris einfach zu zeichnen ist
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=32, radius=R_BALL)
    me = bpy.data.meshes.new("auge_" + sn)
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    me.materials.append(EYEM)
    eo = bpy.data.objects.new("auge_" + sn, me)
    col.objects.link(eo)
    _e = np.array(AUGE)
    _au = np.array(AU)
    _e[1] *= sgn
    _au[1] *= sgn
    wp = l2w(_e)
    wd = _au[0] * HA + _au[1] * HB + _au[2] * HC
    eo.rotation_mode = "QUATERNION"
    eo.rotation_quaternion = Vector(wd.tolist()).to_track_quat("Z", "Y")
    eo.location = wp.tolist()
    eo.scale = (KOPF_SK, KOPF_SK, KOPF_SK)
    on_bone(eo, "kopf")

# Nase: eigenes, feines Feld
_nlo = NASE_C + np.array((-0.058, -0.056, -0.042))
_nhi = NASE_C + np.array((0.038, 0.056, 0.044))
NV, NQ = netz_aus_feld(feld_nase, _nlo, _nhi, H_FEIN, grob=4, rand=3.0)
NV = glaette(NV, NQ, 0.25, 1)
dbg("Nase", len(NV), "Punkte")
_x, _y, _z = NV[:, 0] - NASE_C[0], np.abs(NV[:, 1]), NV[:, 2] - NASE_C[2]
_nl = nasenloch(_x, _y, _z)
_tief = 1.0 - sst(0.0005, 0.0048, _nl)
_nr = np.tile(np.array((0.024, 0.0215, 0.021)), (len(NV), 1))
_nr = _nr + (np.array((0.0015, 0.0012, 0.0012)) - _nr) * _tief[:, None]
nase = netz_objekt("nase", l2w(NV), NQ, NASEM, {"haut": _nr})
on_bone(nase, "kopf")

# Zunge, Zaehne
ZV, ZQ = netz_aus_feld(feld_zunge, (0.15, -0.055, -0.09), (0.45, 0.055, -0.04), H_KOPF, grob=4)
ZV = glaette(ZV, ZQ, 0.4, 2)
zunge = netz_objekt("zunge", l2w(ZV), ZQ, MOUTH)
on_bone(zunge, "kiefer")
KV2, KQ2 = netz_aus_feld(feld_kamm, (0.24, -0.075, -0.09), (0.46, 0.075, -0.03), H_KOPF, grob=4)
KV2 = glaette(KV2, KQ2, 0.4, 2)
kamm = netz_objekt("kamm", l2w(KV2), KQ2, GUM)
on_bone(kamm, "kiefer")


def zahn(name, a0, b0, c0, a1, b1, c1, r, bn, kurve=0.0):
    M = 10
    ts = np.linspace(0, 1, M)
    P0, P1 = np.array((a0, b0, c0)), np.array((a1, b1, c1))
    pf = np.array([P0 + (P1 - P0) * t + np.array((-kurve, 0, 0)) * math.sin(math.pi * t) for t in ts])
    rw = r * 0.85 * (1 - ts) ** 0.65 + 0.0005
    rh = r * 1.0 * (1 - ts) ** 0.65 + 0.0005
    V, F, _t = rohr(pf, rw, rh, (0.0, 1.0, 0.0), 10)
    o = netz_objekt(name, l2w(V), F, TOOTH)
    on_bone(o, bn)
    return o


def zaehne():
    for s in (-1.0, 1.0):
        # Eckzaehne
        zahn("fang_o", 0.430, s * 0.047, -0.008, 0.424, s * 0.049, -0.072, 0.0135, "kopf", 0.008)
        zahn("fang_u", 0.418, s * 0.041, -0.086, 0.424, s * 0.044, -0.022, 0.0125, "kiefer", -0.007)
        # Schneidezaehne
        for k, by in enumerate((0.008, 0.021, 0.033)):
            zahn("sz_o", 0.463 - 0.004 * k, s * by, -0.012, 0.463 - 0.004 * k, s * by, -0.034, 0.0048 + 0.0008 * k, "kopf")
            zahn("sz_u", 0.450 - 0.005 * k, s * by * 0.85, -0.074, 0.452 - 0.005 * k, s * by * 0.85, -0.039, 0.0042 + 0.0006 * k, "kiefer")
        # Backenzaehne: stumpf
        for k in range(5):
            aa = 0.285 + 0.024 * k
            bb = 0.052 - 0.0016 * k
            zahn("bz_o", aa, s * bb, -0.012, aa, s * bb, -0.031, 0.0090 - 0.0007 * k, "kopf")
            zahn("bz_u", aa - 0.010, s * (bb - 0.006), -0.082, aa - 0.010, s * (bb - 0.006), -0.037, 0.0085 - 0.0007 * k, "kiefer")


zaehne()
dbg("Mund fertig")

# ------------------------------------------------------------------ Zehen und Krallen
PFOTEN = []
for s, n in ((-1, "R"), (1, "L")):
    PFOTEN.append(("pranke" + n, s, 0.578, s * 0.283, 0.092, 0.058, 1.0))
    PFOTEN.append(("fuss" + n, s, -0.372, s * 0.320, 0.056, 0.044, 0.82))


def zehen_lage(xc, yc, s, g):
    """Fuenf Zehen im Bogen: Ansatz, Spitze, Blickrichtung."""
    Z = []
    for k in (-2, -1, 0, 1, 2):
        # Der Bogen: Mitte am weitesten vorn
        bx = xc - 0.060 * g - 0.013 * k * k * g
        by = yc + s * k * 0.046 * g
        tx = xc + 0.012 * g - 0.015 * k * k * g
        ty = yc + s * k * 0.058 * g
        Z.append(((bx, by, 0.078 * g), (tx, ty, 0.050 * g)))
    return Z


def zehen_feld_fn(xc, yc, s, g):
    Z = zehen_lage(xc, yc, s, g)

    def fn(x, y, z):
        d = ell(x, y, z, (xc - 0.125 * g, yc, 0.066 * g), (0.145 * g, 0.132 * g, 0.066 * g))
        for b0, t0 in Z:
            d = smin(d, cap(x, y, z, b0, t0, 0.0310 * g, 0.0265 * g), 0.0055 * g)
            # Zehenballen
            d = smin(d, ell(x, y, z, (t0[0] - 0.004 * g, t0[1], 0.024 * g), (0.027 * g, 0.024 * g, 0.021 * g)), 0.007 * g)
        # Grosser Sohlenballen
        d = smin(d, ell(x, y, z, (xc - 0.085 * g, yc, 0.018 * g), (0.070 * g, 0.100 * g, 0.018 * g)), 0.012 * g)
        # Boden: oberhalb bleiben
        d = smax(d, 0.003 - z, 0.006)
        return d

    return fn


H_PF = {0: 0.0034, 1: 0.0030, 2: 0.0026}[QUAL]   # Lauf baer-pfoten: Gitter des Pfotenfelds (Hochmodell; Spiel 2,6 / 2,3 / 2,0 mm)
# Kasten je Pfote in Spielmetern (linke Seite): x, y, z
PF_KASTEN = {"H": ((-0.675, 0.105, -0.004), (-0.150, 0.385, 0.385)), "V": ((0.185, 0.075, -0.004), (0.570, 0.355, 0.385))}


def pf_kasten_h(vh, s):
    lo, hi = np.array(PF_KASTEN[vh][0]), np.array(PF_KASTEN[vh][1])
    if s < 0:
        lo[1], hi[1] = -hi[1], -lo[1]
    return lo / PF_G + np.array((PF_X0, 0.0, PF_ZMIN)), hi / PF_G + np.array((PF_X0, 0.0, PF_ZMIN))


def pfote_bauen(bn, s, xc, yc, L_front, S_z, g):
    """Lauf baer-pfoten: Pfote samt Unterschenkel/Unterarm aus EINEM Feld (pfote_feld_fn), Netz 'pfote_<bn>' starr am Knochen
    (Ruhe zaehlt fuer Spielnetz und Ansichten); Krallen wie bisher (zehen_lage), vorn um K1 in y zur Mittelkralle."""
    vh = "V" if bn.startswith("pranke") else "H"
    fn = pfote_feld_fn(vh, s)
    lo, hi = pf_kasten_h(vh, s)
    V, Q = netz_aus_feld(fn, lo, hi, H_PF, grob=4)
    V = glaette(V, Q, 0.25, 1)
    xs, ys, zs = pf_h2s(V[:, 0], V[:, 1], V[:, 2])
    VN = punkt_normalen(V, Q)
    # Sohle, Ballen, Zehenballen dunkel (nackte Haut); oben Fellfarbe
    unten = (1.0 - sst(0.010, 0.022, zs)) * sst(-0.2, -0.6, VN[:, 2])
    if "ballen" in PF_TEILE[vh]:
        b = PF_TEILE[vh]["ballen"]
        db = np.sqrt((xs - b["c"][0]) ** 2 + (ys * s - b["c"][1]) ** 2 + (zs - b["c"][2]) ** 2) - b["r"]
        unten = np.maximum(unten, 1.0 - sst(-0.002, 0.004, db))
    rgb = mel2rgb(np.full(len(V), 0.86))
    rgb = rgb + (np.array((0.014, 0.011, 0.010)) - rgb) * unten[:, None]
    o = netz_objekt("pfote_" + bn, V, Q, SKIN, {"haut": rgb}, {"feucht": unten * 0.25})
    on_bone(o, bn)
    Z = zehen_lage(xc, yc, s, g)
    # Krallen (Form wie bisher); vorn K1: jede Kralle in y zur Mittelkralle (Teilung 4,6 -> 4,1 cm im Spielnetz)
    CV, CF, CT = [], [], []
    off = 0
    for i, (b0, t0) in enumerate(Z):
        k = i - 2
        rich = s * math.radians(k * 6.5)
        Lk_ = L_front * (1.0 - 0.055 * abs(k)) * (0.97 + 0.03 * math.sin(i * 7.3 + s))
        Sx = t0[0] + 0.011 * g + (-0.070 / PF_G if vh == "H" else 0.0)   # 2c: Hinterkrallen 7 cm nach hinten (Spielmass)
        Sy = t0[1] + ((t0[1] - yc) * K1_FAKTOR if vh == "V" else 0.0)
        Sz = S_z + 0.004 * abs(k)
        P = krallenpfad((Sx, Sy, Sz), rich, Lk_, math.radians(6.0), math.radians(72.0))
        # Spitze nie unter den Boden
        low = P[:, 2].min()
        if low < 0.008:
            P[:, 2] += 0.008 - low
        ts = np.linspace(0, 1, len(P))
        prof = (1.0 - ts**1.5) ** 0.72
        rh = (0.0150 * g) * prof + 0.0007
        rw = (0.0150 * g) * 0.74 * prof + 0.0006
        v_, f_, t_ = rohr(P, rw, rh, (0.0, 1.0, 0.0), 16)
        CV.append(v_)
        CT.append(t_)
        CF.extend([tuple(j + off for j in fc) for fc in f_])
        off += len(v_)
    co = netz_objekt("krallen_" + bn, np.concatenate(CV, 0), CF, CLAWM, None, {"krallet": np.concatenate(CT)})
    on_bone(co, bn)
    return V, Q, fn


PF_FN = []
PF_NETZE = []
for bn, s, xc, yc, Lf, Sz, g in PFOTEN:
    V_, Q_, fn_ = pfote_bauen(bn, s, xc, yc, Lf, Sz, g)
    vh_ = "V" if bn.startswith("pranke") else "H"
    PF_NETZE.append((bn, s, vh_, V_, Q_, fn_))
    PF_FN.append((vh_, s) + pf_kasten_h(vh_, s) + (fn_, pfote_feld_fn(vh_, s, "fuss"), pfote_feld_fn(vh_, s, "alle", True)))
    print("BAER_PFOTE", bn, "Punkte", len(V_), "Flaechen", len(Q_), "z_h", round(float(V_[:, 2].min()), 4), round(float(V_[:, 2].max()), 4))
dbg("Pfoten fertig")


def pfoten_abstand(P, teil="alle"):
    """Lauf baer-pfoten: kleinster Abstand (Hochmodell-Meter) zum Pfotenfeld (Welt, Ruhe); teil='fuss': ohne Unterschenkel/Unterarm,
    teil='soll': zum Soll des Spielnetzes (Haut + Huelle; negativ = so weit darf die Huelle noch wachsen)."""
    P = np.asarray(P, dtype=float)
    d = np.full(len(P), 9.0)
    for vh, s, lo, hi, fn, fn_fuss, fn_soll in PF_FN:
        near = np.all((P > lo - 0.08) & (P < hi + 0.08), axis=1)
        if near.any():
            f = {"alle": fn, "fuss": fn_fuss, "soll": fn_soll}[teil]
            d[near] = np.minimum(d[near], f(P[near, 0], P[near, 1], P[near, 2]))
    return d


zehen_abstand = pfoten_abstand   # alter Name (baer_export_*: Zehen-Abstand)


# ------------------------------------------------------------------ Fellgruppen am Koerper
_bv = np.array([v.co for v in body.data.vertices])
_bl = w2l(_bv)
_ka = feld_huelle(_bl[:, 0], _bl[:, 1], _bl[:, 2])
_ze = pfoten_abstand(_bv)
print("BAER_PFOTE vorn x max", round(float(_bv[(_bv[:, 2] < 0.2) & (_bv[:, 1] > 0)][:, 0].max()), 3), "hinten", round(float(_bv[(_bv[:, 2] < 0.2) & (_bv[:, 0] < 0)][:, 0].max()), 3))
print("BAER_HALS x max", round(float(_bv[:, 0].max()), 3), "y bei 0.85", round(float(_bv[np.abs(_bv[:, 0] - 0.85) < 0.03][:, 1].max()), 3), "z", round(float(_bv[np.abs(_bv[:, 0] - 0.85) < 0.03][:, 2].min()), 3), round(float(_bv[np.abs(_bv[:, 0] - 0.85) < 0.03][:, 2].max()), 3))

G = {n: body.vertex_groups.new(name=n) for n in ("d_koerper", "d_bein", "l_koerper", "l_bein")}
for v, kd, zd in zip(body.data.vertices, _ka, _ze):
    c = v.co
    # Wo der Kopf den Hals schluckt, waechst kein Koerperfell mehr
    frei = sstep(-0.012, 0.022, float(kd))
    leg = 1.0 - sstep(lz(0.22), lz(0.56), c.z)
    # Die Bauchlinie zwischen den Beinen bleibt Koerperfell
    if -0.25 < c.x < 0.12:
        leg *= 0.15
    rest = max(0.0, 1.0 - leg)
    G["d_koerper"].add([v.index], rest * frei, "REPLACE")
    # Lauf baer-pfoten: wo die Koerperhaut im Pfotenfeld steckt, waechst kein Beinfell (das Pfotenfeld hat eigenes Haar)
    zf = sstep(-0.004, 0.010, float(zd))
    G["d_bein"].add([v.index], leg * zf, "REPLACE")
    # Laengen: Nackenmaehne und Bauchfransen lang, Ruecken mittel
    lk = 0.72
    lk += 0.28 * sstep(0.1, 0.45, c.x) * sstep(lz(0.62), lz(0.95), c.z) * (1 - sstep(0.75, 0.95, c.x))
    lk += 0.28 * (1 - sstep(lz(0.34), lz(0.48), c.z)) * (1 - sstep(0.12, 0.3, abs(c.x + 0.1)))
    # Am Kopf kuerzer, sonst steckt er in einer Kapuze
    lk *= 1.0 - 0.62 * sstep(0.55, 0.92, c.x)
    G["l_koerper"].add([v.index], min(1.0, lk), "REPLACE")
    G["l_bein"].add([v.index], 0.26 + 0.74 * sstep(0.09, lz(0.34), c.z), "REPLACE")

hm = bpy.data.materials.new("haar")
hm.use_nodes = True
N, L = hm.node_tree.nodes, hm.node_tree.links
N.remove(N["Principled BSDF"])
hb = N.new("ShaderNodeBsdfHairPrincipled")
hb.parametrization = "MELANIN"
hb.inputs["Melanin Redness"].default_value = 0.25
hb.inputs["Roughness"].default_value = 0.34
hb.inputs["Radial Roughness"].default_value = 0.8
hb.inputs["Coat"].default_value = 0.0
hi = N.new("ShaderNodeHairInfo")
tc = N.new("ShaderNodeTexCoord")
sep = N.new("ShaderNodeSeparateXYZ")
L.new(tc.outputs["Generated"], sep.inputs[0])
nz = N.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 9
nz.inputs["Detail"].default_value = 6
L.new(tc.outputs["Generated"], nz.inputs["Vector"])
add1 = N.new("ShaderNodeMath")
add1.operation = "ADD"
L.new(maprange(N, L, hi.outputs["Random"], 0.0, 1.0, -0.07, 0.07), add1.inputs[0])
L.new(maprange(N, L, nz.outputs["Fac"], 0.30, 0.70, 0.74, 0.90), add1.inputs[1])
add2 = N.new("ShaderNodeMath")
add2.operation = "ADD"
L.new(add1.outputs[0], add2.inputs[0])
L.new(maprange(N, L, sep.outputs[2], 0.14, 0.42, 0.13, 0.0), add2.inputs[1])       # Beine dunkler
add3 = N.new("ShaderNodeMath")
add3.operation = "SUBTRACT"
L.new(add2.outputs[0], add3.inputs[0])
L.new(maprange(N, L, sep.outputs[2], 0.56, 0.92, 0.0, 0.12), add3.inputs[1])       # Ruecken heller
add4 = N.new("ShaderNodeMath")
add4.operation = "SUBTRACT"
add4.use_clamp = True
L.new(add3.outputs[0], add4.inputs[0])
tip = N.new("ShaderNodeMath")
tip.operation = "ADD"
L.new(maprange(N, L, hi.outputs["Intercept"], 0.45, 1.0, 0.0, 0.2), tip.inputs[1])  # helle Spitzen
tip.inputs[0].default_value = 0.0
L.new(tip.outputs[0], add4.inputs[1])
L.new(add4.outputs[0], hb.inputs["Melanin"])
hb.inputs["Random Color"].default_value = 0.1
L.new(hb.outputs[0], N["Material Output"].inputs["Surface"])
body.data.materials.append(hm)


def fell(name, count, length, normal, align, dens, lng, kids, clump, rough1, rough2, radius, seed):
    body.modifiers.new(name, "PARTICLE_SYSTEM")
    ps = body.particle_systems[-1]
    ps.seed = seed
    st = ps.settings
    st.name = name
    st.type = "HAIR"
    st.use_advanced_hair = True
    st.count = count
    st.hair_length = length
    st.hair_step = 5
    st.display_step = 3
    st.emit_from = "FACE"
    st.normal_factor = normal
    st.object_align_factor = align
    st.factor_random = normal * 0.22
    st.brownian_factor = 0.002
    st.child_type = "INTERPOLATED"
    st.child_percent = 2
    st.rendered_child_count = kids
    st.child_length = 0.86
    st.child_length_threshold = 0.25
    st.clump_factor = clump
    st.clump_shape = 0.2
    st.use_clump_noise = clump > 0.3
    st.clump_noise_size = 0.45
    st.roughness_1 = rough1
    st.roughness_1_size = 0.55
    st.roughness_endpoint = rough1 * 1.1
    st.roughness_2 = rough2
    st.material_slot = "haar"
    st.root_radius = 1.0
    st.tip_radius = 0.03
    st.radius_scale = radius
    ps.vertex_group_density = dens
    ps.vertex_group_length = lng


if FELL_KOERPER > 0:
    _ff = FELL_KOERPER
    _kk_ = lambda k: max(4, int(k * _ff))
    fell("unterwolle", int(100000 * _ff), 0.098, 0.052, (-0.038, 0.0, -0.024), "d_koerper", "l_koerper", _kk_(18), 0.66, 0.009, 0.007, 0.0028, 11)
    fell("deckhaar", int(14000 * _ff), 0.15, 0.066, (-0.052, 0.0, -0.036), "d_koerper", "l_koerper", _kk_(9), 0.86, 0.013, 0.012, 0.0034, 12)
    fell("beinfell", int(60000 * _ff), 0.082, 0.046, (-0.012, 0.0, -0.028), "d_bein", "l_bein", _kk_(14), 0.56, 0.008, 0.005, 0.0029, 13)


def kopf_schutz(a, b, c):
    return feld_huelle(a, b, c)


if HAAR_FAKTOR > 0:
    t0 = time.time()
    pts, rad, W, gross, nrm = wachse(KV, KQ, haar_dichte, kopf_haar_werte, RNG, faktor=HAAR_FAKTOR, np_pts=6, schutz_fn=kopf_schutz, nachbes_fn=eye_ausschluss)
    dbg("Kopfhaar", len(pts), "Straehnen", "%.1fs" % (time.time() - t0))
    wk_root = kiefer_gewicht(pts[:, 0, 0], pts[:, 0, 1], pts[:, 0, 2], SPALT)
    pw = l2w(pts)
    _stufe = np.round(np.clip(wk_root, 0.0, 1.0) * 8.0).astype(int)
    for _n in range(9):
        sel_ = _stufe == _n
        if sel_.any():
            bn_ = "kopf" if _n == 0 else ("kiefer" if _n == 8 else "kiefer_%d" % _n)
            haar_objekt("haar_" + bn_, pw[sel_], rad[sel_], {"mel": W["mel"][sel_], "rot": W["rot"][sel_]}, bn_)

    # Lauf baer-pfoten: Pfotenhaar auf dem ganzen Pfotenfeld ausser Sohle/Ballen (nackt) und wo es im Koerper steckt (dort waechst
    # das Beinfell der Koerperhaut). Kurz auf den Zehen (1 cm), Fussruecken/Ferse 1,6-2,2 cm, am Unterschenkel bis 4,5 cm (Spielmass).
    from mathutils.bvhtree import BVHTree as _BVH
    _bm_k = bmesh.new()
    _bm_k.from_mesh(body.data)
    _bvh_k = _BVH.FromBMesh(_bm_k)
    _bm_k.free()

    def _im_koerper(C):
        aus = np.zeros(len(C), dtype=bool)
        for i_, c_ in enumerate(C):
            loc, nrm, _j, _d = _bvh_k.find_nearest(Vector(c_))
            if loc is not None:
                aus[i_] = (Vector(c_) - loc).dot(nrm) < 0.0
        return aus

    for bn, s, vh, V_, Q_, fn_ in PF_NETZE:
        K_ = PF_KRALLEN[vh]

        def z_dichte(C, vh=vh, s=s):
            xs, ys, zs = pf_h2s(C[:, 0], C[:, 1], C[:, 2])
            d = 300000.0 * sst(0.010, 0.020, zs) * (1.0 - sst(0.30, 0.35, zs))
            if "ballen" in PF_TEILE[vh]:
                b = PF_TEILE[vh]["ballen"]
                db = np.sqrt((xs - b["c"][0]) ** 2 + (ys * s - b["c"][1]) ** 2 + (zs - b["c"][2]) ** 2) - b["r"]
                d = d * sst(0.000, 0.008, db)
            kand = d > 0
            if kand.any():
                d[np.nonzero(kand)[0][_im_koerper(C[kand])]] = 0.0
            return d

        def z_werte(P, n, vh=vh, s=s, K_=K_):
            xs, ys, zs = pf_h2s(P[:, 0], P[:, 1], P[:, 2])
            vor = (xs - (np.mean(K_["x"]) - 0.06)) / 0.06          # > 0 auf den Zehen
            L_s = np.interp(zs, [0.0, 0.05, 0.10, 0.20, 0.30], [0.012, 0.017, 0.022, 0.032, 0.045])
            L_s = L_s * (1.0 - 0.40 * sst(0.0, 0.6, vor))
            L_ = L_s / PF_G * (0.95 + 0.15 * rauschen(P[:, 0], P[:, 1], P[:, 2], 80.0))
            F = np.zeros((len(P), 3))
            F[:, 0] = np.where(zs < 0.10, 0.9, -0.15)
            F[:, 2] = -1.0
            m = np.clip(0.84 + 0.04 * sst(0.25, 0.05, zs) + 0.05 * rauschen(P[:, 0], P[:, 1], P[:, 2], 60.0), 0, 1)
            return dict(L=L_, F=F, lift=np.full(len(P), 0.22), r0=np.full(len(P), 0.0011), kl=np.full(len(P), 0.30), mel=m,
                        rot=np.full(len(P), 0.30), zelle=0.014)

        zp, zr, zw, _, _ = wachse(V_, Q_, z_dichte, z_werte, RNG, faktor=HAAR_FAKTOR, np_pts=4, schutz_fn=fn_, schutz=0.0009)
        haar_objekt("haar_" + bn, zp, zr, {"mel": zw["mel"], "rot": zw["rot"]}, bn)
        print("BAER_PFOTENHAAR", bn, len(zp))
    dbg("Pfotenhaar fertig")

# ------------------------------------------------------------------ Boden und Licht wie ein Tag im Spiel
bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, 0))
gr = bpy.context.active_object
gm = bpy.data.materials.new("boden")
gm.use_nodes = True
N, L = gm.node_tree.nodes, gm.node_tree.links
bb = N["Principled BSDF"]
tc = N.new("ShaderNodeTexCoord")
nz = N.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 1.1
nz.inputs["Detail"].default_value = 12
nz.inputs["Roughness"].default_value = 0.68
L.new(tc.outputs["Object"], nz.inputs["Vector"])
nz2 = N.new("ShaderNodeTexNoise")
nz2.inputs["Scale"].default_value = 22
nz2.inputs["Detail"].default_value = 8
L.new(tc.outputs["Object"], nz2.inputs["Vector"])
gc = mix_rgba(N, L, maprange(N, L, nz.outputs["Fac"], 0.34, 0.66, 0, 1), (0.06, 0.08, 0.024), (0.15, 0.14, 0.05))
gc = mix_rgba(N, L, maprange(N, L, nz2.outputs["Fac"], 0.4, 0.66, 0, 0.7), gc, (0.05, 0.075, 0.022))
L.new(gc, bb.inputs["Base Color"])
bb.inputs["Roughness"].default_value = 0.95
bp2 = N.new("ShaderNodeBump")
bp2.inputs["Strength"].default_value = 0.6
L.new(nz2.outputs["Fac"], bp2.inputs["Height"])
L.new(bp2.outputs["Normal"], bb.inputs["Normal"])
gr.data.materials.append(gm)

world = bpy.data.worlds.new("himmel")
world.use_nodes = True
nt = world.node_tree
sky = nt.nodes.new("ShaderNodeTexGradient")
tcw = nt.nodes.new("ShaderNodeTexCoord")
mp = nt.nodes.new("ShaderNodeMapping")
mp.inputs["Rotation"].default_value = (0, -math.pi / 2, 0)
nt.links.new(tcw.outputs["Generated"], mp.inputs["Vector"])
nt.links.new(mp.outputs["Vector"], sky.inputs["Vector"])
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.5
ramp.color_ramp.elements[0].color = (0.78, 0.66, 0.5, 1)
ramp.color_ramp.elements[1].position = 0.86
ramp.color_ramp.elements[1].color = (0.2, 0.33, 0.56, 1)
nt.links.new(sky.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], nt.nodes["Background"].inputs[0])
nt.nodes["Background"].inputs[1].default_value = 1.5
scene.world = world
sun = bpy.data.lights.new("sonne", "SUN")
sun.energy = 3.0
sun.color = (1.0, 0.9, 0.78)
sun.angle = math.radians(2.2)
so = bpy.data.objects.new("sonne", sun)
col.objects.link(so)
so.rotation_euler = (math.radians(50), 0, math.radians(38))

# Gras auf dem Fahrweg des Baeren
bpy.ops.mesh.primitive_plane_add(size=26, location=(1.6, 0, 0.002))
wiese = bpy.context.active_object
wiese.name = "wiese"
wm = bpy.data.materials.new("wiesenboden")
wm.use_nodes = True
wm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.05, 0.022, 1)
wm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
gh = bpy.data.materials.new("halm")
gh.use_nodes = True
Ng, Lg = gh.node_tree.nodes, gh.node_tree.links
bg = Ng["Principled BSDF"]
hig = Ng.new("ShaderNodeHairInfo")
Lg.new(mix_rgba(Ng, Lg, maprange(Ng, Lg, hig.outputs["Random"], 0.2, 0.9, 0, 1), (0.085, 0.13, 0.03), (0.27, 0.27, 0.075)), bg.inputs["Base Color"])
bg.inputs["Roughness"].default_value = 0.55
wiese.data.materials.append(wm)
wiese.data.materials.append(gh)
sg = None
if GRAS > 0:
    wiese.modifiers.new("gras", "PARTICLE_SYSTEM")
    pg = wiese.particle_systems[-1]
    sg = pg.settings
    sg.type = "HAIR"
    sg.use_advanced_hair = True
    sg.count = int(120000 * GRAS)
    sg.hair_step = 4
    sg.normal_factor = 0.017
    sg.factor_random = 0.007
    sg.object_align_factor = (0.006, 0.004, 0)
    print("BAER_GRAS Laenge", sg.hair_length)
    sg.child_type = "INTERPOLATED"
    sg.rendered_child_count = max(3, int(6 * GRAS))
    sg.child_length = 0.8
    sg.child_length_threshold = 0.25
    sg.roughness_1 = 0.03
    sg.roughness_endpoint = 0.05
    sg.material_slot = "halm"
    sg.root_radius = 1.0
    sg.tip_radius = 0.02
    sg.radius_scale = 0.0028
    sg.use_modifier_stack = False

# Ferne Huegel, nur als weiche Silhouette
hilm = plain("huegel", (0.075, 0.095, 0.05), 1.0)
bpy.ops.mesh.primitive_plane_add(size=90, location=(0, 12.4, 20), rotation=(math.pi / 2, 0, 0))
wald = bpy.context.active_object
wald.name = "wald"
wbm = bpy.data.materials.new("wald")
wbm.use_nodes = True
Nw, Lw = wbm.node_tree.nodes, wbm.node_tree.links
Nw.remove(Nw["Principled BSDF"])
tw = Nw.new("ShaderNodeTexCoord")
n1 = Nw.new("ShaderNodeTexNoise")
n1.inputs["Scale"].default_value = 0.8
n1.inputs["Detail"].default_value = 5
n1.inputs["Roughness"].default_value = 0.62
Lw.new(tw.outputs["Object"], n1.inputs["Vector"])
fw = mix_rgba(Nw, Lw, maprange(Nw, Lw, n1.outputs["Fac"], 0.36, 0.64, 0, 1), (0.022, 0.05, 0.014), (0.2, 0.2, 0.03))
ew = Nw.new("ShaderNodeEmission")
Lw.new(fw, ew.inputs["Color"])
ew.inputs["Strength"].default_value = 0.75
Lw.new(ew.outputs[0], Nw["Material Output"].inputs["Surface"])
wald.data.materials.append(wbm)

scene.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "OPTIX"
print("BAER_GERAETE", [d.name for d in prefs.devices if d.use])
scene.cycles.device = "GPU"
scene.cycles.use_denoising = True
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"

# ------------------------------------------------------------------ Bewegung
pb = ao.pose.bones
for p in pb:
    p.rotation_mode = "QUATERNION"

# Fuss- und Pfotenziele, an denen die Beine haengen
TARGETS = {}
for s, n in ((-1, "R"), (1, "L")):
    for leg, chain_end, pawb in (("vorn", "unterarm" + n, "pranke" + n), ("hinten", "wade" + n, "fuss" + n)):
        e = bpy.data.objects.new("ziel_" + leg + n, None)
        col.objects.link(e)
        rest_tail = arm.bones[chain_end].tail_local
        e.location = rest_tail
        rest_rot = (ao.matrix_world @ arm.bones[pawb].matrix_local).to_quaternion()
        e.rotation_mode = "QUATERNION"
        e.rotation_quaternion = rest_rot
        TARGETS[leg + n] = (e, rest_tail.copy(), rest_rot.copy())
        ik = pb[chain_end].constraints.new("IK")
        ik.target = e
        ik.chain_count = 2
        ik.use_tail = True
        crot = pb[pawb].constraints.new("COPY_ROTATION")
        crot.target = e

WALK_END = 76          # bis hier zwei Gehzyklen
T = 1.25 * FPS         # Bilder je Zyklus
DUTY = 0.62
SPEED = 0.95 / FPS     # Meter je Bild
L_STEP = SPEED * T
PHASE = {"hintenL": 0.0, "vornL": 0.25, "hintenR": 0.5, "vornR": 0.75}

KF = {
    "stand": WALK_END + 8,
    "auf": WALK_END + 26,
    "aus": WALK_END + 32,
    "hieb": WALK_END + 39,
    "nach": WALK_END + 48,
    "ende": WALK_END + 70,
}
END_FRAME = KF["ende"] + 6


def smooth(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def foot_rel(phi):
    """Fuss relativ zum Koerper: Stuetzphase schiebt nach hinten, Schwung holt nach vorn."""
    if phi < DUTY:
        u = phi / DUTY
        return L_STEP * DUTY * (0.5 - u), 0.0, 0.0
    u = (phi - DUTY) / (1 - DUTY)
    x = L_STEP * DUTY * (u - 0.5)
    z = 0.13 * math.sin(math.pi * u)
    pitch = 28 * math.sin(math.pi * u * 1.1)
    return x, z, pitch


def set_rot(p, axis, deg):
    """Drehung um eine Weltachse, umgerechnet in das Ruhe-Achsenkreuz des Knochens."""
    r = p.bone.matrix_local.to_quaternion()
    q = Quaternion(axis, math.radians(deg))
    p.rotation_quaternion = r.inverted() @ q @ r


def combine(p, parts):
    r = p.bone.matrix_local.to_quaternion()
    tot = Quaternion()
    for axis, deg in parts:
        tot = Quaternion(axis, math.radians(deg)) @ tot
    p.rotation_quaternion = r.inverted() @ tot @ r


X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def pose_at(f):
    t = f
    # Fortbewegung, die ab WALK_END ausklingt
    if f <= WALK_END:
        travel = SPEED * f
    else:
        travel = SPEED * WALK_END + SPEED * 0.5 * min(f - WALK_END, 8) * (1 - min(f - WALK_END, 8) / 16.0)
    stopped = smooth(WALK_END, KF["stand"], f)

    # Abbremsen: Beine laufen in eine feste Stellung
    wt = 1.0 - stopped
    feet = {}
    for key, ph in PHASE.items():
        phi = ((f / T) + ph) % 1.0
        fx, fz, fp = foot_rel(phi)
        feet[key] = (fx * wt, fz * wt, fp * wt)

    # Wie weit steht er auf? Hiebablauf
    rise = smooth(KF["stand"], KF["auf"], f) * (1 - smooth(KF["nach"], KF["ende"], f))
    pitch = -27 * rise
    lift = 0.17 * rise
    swing = smooth(KF["aus"], KF["hieb"], f) * (1 - smooth(KF["nach"], KF["ende"], f))
    follow = smooth(KF["aus"], KF["hieb"], f) - smooth(KF["nach"] - 4, KF["ende"] - 6, f)

    gait = math.sin(2 * math.pi * f / T)
    gait2 = math.sin(4 * math.pi * f / T)
    bob = 0.018 * gait2 * wt
    ao.location = (travel, 0, 0)
    pb["wurzel"].location = (0, 0, 0)

    # Rumpf: Wiegen im Gehen, Aufrichten zum Hieb, Vorwerfen beim Schlag
    hieb_pitch = 22 * swing
    combine(pb["wurzel"], [(Y, pitch + hieb_pitch * 0.55), (X, 3.2 * gait * wt), (Z, 3.0 * gait * wt)])
    pb["wurzel"].location = pb["wurzel"].bone.matrix_local.to_quaternion().inverted() @ Vector((0.05 * rise - 0.08 * swing, 0, bob + lift - 0.05 * swing))
    combine(pb["ruecken"], [(Y, pitch * 0.35 + hieb_pitch * 0.35), (Z, -2.5 * gait * wt)])
    combine(pb["brust"], [(Y, pitch * 0.15 + hieb_pitch * 0.35), (Z, -3.5 * gait * wt), (X, -7 * swing)])
    # Kopf bleibt in der Waagerechten, im Hieb nach vorn
    combine(pb["hals"], [(Y, -pitch * 0.7 - hieb_pitch * 0.5 + 3.0 * gait2 * wt), (Z, 4.5 * gait * wt)])
    combine(pb["kopf"], [(Y, -pitch * 0.45 - hieb_pitch * 0.2 - 2 * gait2 * wt - 8 * follow), (Z, -2.5 * gait * wt)])
    # Maul oeffnet zum Bruellen
    roar = smooth(KF["stand"] + 4, KF["auf"], f) * (1 - smooth(KF["nach"], KF["ende"] - 6, f))
    combine(pb["kiefer"], [(Y, 32 * roar)])
    for _n in KIEFER_STUFEN:
        combine(pb["kiefer_%d" % _n], [(Y, 32 * (_n / 8.0) * roar)])
    combine(pb["schwanz"], [(Z, 8 * gait * wt), (Y, -6 * gait2 * wt)])

    # Beine
    for key, (fx, fz, fp) in feet.items():
        e, rest, rrot = TARGETS[key]
        e.location = Vector((rest.x + fx + travel, rest.y, rest.z + fz))
        e.rotation_quaternion = Quaternion(Y, math.radians(fp)) @ rrot

    # Hieb: rechte Pranke geht hoch, schlaegt schraeg nach unten, linke stuetzt in der Luft
    e, rest, rrot = TARGETS["vornR"]
    high = Vector((rest.x + 0.62, rest.y - 0.10, rest.z + 1.14))
    drive = Vector((rest.x + 1.08, rest.y + 0.30, rest.z + 0.16))
    hold = Vector((rest.x + 0.03, rest.y, rest.z)) + Vector((travel, 0, 0))
    up = smooth(KF["stand"], KF["aus"], f)
    down = smooth(KF["aus"], KF["hieb"], f)
    back = smooth(KF["nach"], KF["ende"], f)
    hi = high + Vector((travel, 0, 0))
    dr = drive + Vector((travel, 0, 0))
    pos = hold.lerp(hi, up).lerp(dr, down).lerp(hold, back)
    e.location = pos
    e.rotation_quaternion = Quaternion(Y, math.radians((-55 * up + 118 * down) * (1 - back))) @ rrot

    e, rest, rrot = TARGETS["vornL"]
    hold = Vector((rest.x + 0.02 + travel, rest.y, rest.z))
    tuck = Vector((rest.x + 0.34 + travel, rest.y + 0.03, rest.z + 0.30))
    land = Vector((rest.x + 0.40 + travel, rest.y, rest.z))
    p1 = hold.lerp(tuck, rise * (1 - 0.8 * down))
    p1 = p1.lerp(land, down * (1 - back))
    p1 = p1.lerp(hold, back)
    e.location = p1
    e.rotation_quaternion = Quaternion(Y, math.radians(-25 * rise * (1 - down))) @ rrot


# Jedes Bild vorab in Schluessel schreiben, sonst rechnet die Szene in der Tiefe nicht nach
def key_all(f):
    pose_at(f)
    ao.keyframe_insert("location", frame=f)
    for p in pb:
        p.keyframe_insert("rotation_quaternion", frame=f)
    pb["wurzel"].keyframe_insert("location", frame=f)
    for e, _, _ in TARGETS.values():
        e.keyframe_insert("location", frame=f)
        e.keyframe_insert("rotation_quaternion", frame=f)


for f in range(1, END_FRAME + 1):
    key_all(f)
scene.frame_start = 1
scene.frame_end = END_FRAME
dbg("Bewegung geschluesselt")


def camera(name, offs, tgt_offs, lens=None, ortho=None, fstop=1.8):
    cam = bpy.data.cameras.new(name)
    if ortho:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho
    else:
        cam.lens = lens
    co = bpy.data.objects.new(name, cam)
    col.objects.link(co)
    co.location = offs
    d = Vector(tgt_offs) - Vector(offs)
    co.rotation_mode = "QUATERNION"
    co.rotation_quaternion = d.to_track_quat("-Z", "Y")
    if not ortho:
        cam.dof.use_dof = True
        cam.dof.focus_distance = d.length * 0.94
        cam.dof.aperture_fstop = fstop
    # Kamera faehrt mit dem Baeren
    c = co.constraints.new("COPY_LOCATION")
    c.target = ao
    c.use_x = True
    c.use_y = False
    c.use_z = False
    c.use_offset = True
    return co


def fest_kamera(name, pos, ziel, lens, fstop=7.0, fokus=None):
    """Kamera ohne Mitfahren: fuer ein einzelnes Bild aus der gerechneten Pose."""
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    co = bpy.data.objects.new(name, cam)
    col.objects.link(co)
    co.location = pos
    d = Vector(ziel) - Vector(pos)
    co.rotation_mode = "QUATERNION"
    co.rotation_quaternion = d.to_track_quat("-Z", "Y")
    cam.dof.use_dof = True
    cam.dof.focus_distance = fokus if fokus else d.length
    cam.dof.aperture_fstop = fstop
    return co


def welt_von_rest(bname, frame, P):
    """Punkt in Welt-Ruhekoordinaten -> Welt in der Pose des Bilds."""
    scene.frame_set(frame)
    dg = bpy.context.evaluated_depsgraph_get()
    ae = ao.evaluated_get(dg)
    m = ae.matrix_world @ ae.pose.bones[bname].matrix @ arm.bones[bname].matrix_local.inverted()
    return m @ Vector(P)


CAM_SIDE = camera("seite", (3.5, -7.2, 0.78), (0.24, 0, 0.92), lens=74)
CAM_GAME = camera("spiel", (6, -6, 5.6), (0.4, 0, 0.55), ortho=4.6)
CAM_GANZ = camera("ganz", (1.1, -8.4, 0.92), (0.16, 0, 0.98), lens=70, fstop=5.6)

print("BAER_OK Dreiecke Koerper", body_tris, "vorher", start_tris, "Kopf Flaechen", len(KQ))


def render_still(name, frame, cam, res, samples):
    scene.camera = cam
    scene.frame_set(frame)
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.cycles.samples = samples
    scene.render.filepath = OUT + name + ".png"
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    dbg("BILD", name, "%.1fs" % (time.time() - t0))


def kopf_bilder(pref, res, samples, nur=None):
    F = 22
    _mitte = welt_von_rest("kopf", F, l2w((0.20, 0.0, 0.0)))
    _nase = welt_von_rest("kopf", F, l2w((0.46, 0.0, 0.0)))
    _dirk = (_nase - _mitte).normalized()
    mitte = np.array(_mitte)
    if nur is None or "profil" in nur:
        # Reine Seite; Kamera sitzt auf der rechten Seite des Baeren
        pos = _mitte + Vector((0.0, -3.7, 0.0))
        render_still(pref + "kopf_profil", F, fest_kamera("k_profil", pos, _mitte, 118, 8.0), res, samples)
    if nur is None or "34" in nur:
        ri = Vector((0.0, -1.0, 0.0))
        d = (_dirk * 0.78 + ri * 0.60 + Vector((0, 0, 0.14))).normalized()
        pos = _mitte + d * 3.4
        ziel = _mitte + _dirk * 0.05
        render_still(pref + "kopf_34", F, fest_kamera("k_34", pos, ziel, 108, 6.3, fokus=(pos - (_mitte + _dirk * 0.08 + ri * 0.08)).length), res, samples)
    if nur is None or "front" in nur:
        d = (_dirk * 1.0 + Vector((0, 0, 0.16))).normalized()
        pos = _mitte + d * 3.6
        render_still(pref + "kopf_front", F, fest_kamera("k_front", pos, _mitte + Vector((0, 0, 0.03)), 108, 8.0, fokus=(pos - _nase).length + 0.1), res, samples)
    if nur is None or "pfote" in nur:
        if sg is not None:
            sg.normal_factor = 0.0065
            sg.factor_random = 0.003
        _p = welt_von_rest("prankeR", F, (0.60, -0.283, 0.05))
        pos = _p + Vector((0.62, -1.75, 0.03))
        render_still(pref + "pfote", F, fest_kamera("k_pfote", pos, _p + Vector((0.0, 0.0, 0.035)), 118, 8.0), res, samples)
        if sg is not None:
            sg.normal_factor = 0.017
            sg.factor_random = 0.007
    if nur is None or "maul" in nur:
        H = KF["hieb"]
        _m = welt_von_rest("kopf", H, l2w((0.28, 0.0, -0.03)))
        _r = welt_von_rest("kopf", H, l2w((0.46, 0.0, -0.03)))
        dk = (_r - _m).normalized()
        d = (dk * 0.62 + Vector((0, -1, 0)) * 0.76 + Vector((0, 0, 0.05))).normalized()
        pos = _m + d * 3.2
        render_still(pref + "maul", H, fest_kamera("k_maul", pos, _m, 108, 7.0), res, samples)


if MODE == "form":
    scene.cycles.max_bounces = 4
    wiese.hide_render = False
    kopf_bilder("form_", (700, 525), 24)
elif MODE == "kopf":
    scene.cycles.max_bounces = 6
    kopf_bilder("", (700, 525), 40)
elif MODE == "nah":
    scene.cycles.max_bounces = 6
    F = 22
    _au = np.array(AUGE)
    _au[1] *= -1
    _a = welt_von_rest("kopf", F, l2w(_au))
    _dirk = (welt_von_rest("kopf", F, l2w((0.46, 0.0, 0.0))) - welt_von_rest("kopf", F, l2w((0.20, 0.0, 0.0)))).normalized()
    d = (_dirk * 0.72 + Vector((0, -1, 0)) * 0.66 + Vector((0, 0, 0.10))).normalized()
    render_still("nah_auge", F, fest_kamera("k_a", _a + d * 2.2, _a, 300, 11.0), (800, 600), 90)
    _n = welt_von_rest("kopf", F, l2w((0.47, 0.0, 0.0)))
    d = (_dirk * 0.92 + Vector((0, -1, 0)) * 0.36 + Vector((0, 0, 0.05))).normalized()
    render_still("nah_nase", F, fest_kamera("k_n", _n + d * 2.2, _n, 240, 11.0), (800, 600), 90)
    _s = welt_von_rest("kopf", F, l2w((0.12, -0.12, 0.08)))
    render_still("nah_schlaefe", F, fest_kamera("k_s", _s + Vector((0.0, -2.2, 0.0)), _s, 240, 11.0), (800, 600), 90)
    _h = welt_von_rest("kopf", F, l2w((0.03, -0.15, 0.14)))
    d = (_dirk * 0.8 + Vector((0, -1, 0)) * 0.6 + Vector((0, 0, 0.1))).normalized()
    render_still("nah_ohr", F, fest_kamera("k_o", _h + d * 2.2, _h, 240, 11.0), (800, 600), 90)
    kopf_bilder("nah_", (1000, 750), 90, nur=("34", "profil", "front", "maul"))
elif MODE == "ende":
    scene.cycles.max_bounces = 8
    kopf_bilder("", (1200, 900), 160)
    render_still("ganz", 22, CAM_GANZ, (1500, 1000), 160)
    H = KF["hieb"]
    _m = welt_von_rest("kopf", H, l2w((0.1, 0.0, -0.1)))
    pos = Vector((_m.x + 1.6, _m.y - 5.6, _m.z - 0.1))
    render_still("hieb", H, fest_kamera("k_hieb", pos, Vector((_m.x - 0.25, 0.0, _m.z - 0.28)), 62, 5.6), (1400, 1050), 160)
elif MODE == "still":
    scene.cycles.max_bounces = 8
    render_still("v3_gehen", 22, CAM_SIDE, (1500, 1000), 200)
    render_still("v3_hoch", KF["aus"], CAM_SIDE, (1500, 1000), 200)
    render_still("v3_hieb", KF["hieb"], CAM_SIDE, (1500, 1000), 200)
    kopf_bilder("v3_", (1200, 900), 200, nur=("34",))
else:
    bpy.ops.wm.save_as_mainfile(filepath=OUT + "baer.blend")
    scene.frame_step = int(os.environ.get("BAER_SCHRITT", "1"))
    scene.camera = CAM_SIDE
    scene.render.resolution_x, scene.render.resolution_y = (720, 500)
    scene.cycles.samples = 48
    scene.render.filepath = OUT + "seite/f_"
    bpy.ops.render.render(animation=True)
    # Die Spielansicht zeigt ehrlich die reduzierte Fassung: Koerper rund 1400 Dreiecke (Vanilla-Tiere: 400-930 Punkte)
    dm = body.modifiers.new("wenig", "DECIMATE")
    dm.ratio = 1400.0 / max(1, body_tris)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.modifier_move_to_index(modifier="wenig", index=0)
    dk = kopf.modifiers.new("wenig", "DECIMATE")
    dk.ratio = 700.0 / max(1, 2 * len(KQ))
    bpy.context.view_layer.objects.active = kopf
    bpy.ops.object.modifier_move_to_index(modifier="wenig", index=0)
    scene.frame_set(1)
    dg = bpy.context.evaluated_depsgraph_get()
    me = body.evaluated_get(dg).to_mesh()
    print("BAER_LOW Dreiecke", sum(len(q.vertices) - 2 for q in me.polygons), "Punkte", len(me.vertices))
    render_still("still_spiel_wenig", 22, CAM_GAME, (620, 465), 64)
    scene.camera = CAM_GAME
    scene.render.resolution_x, scene.render.resolution_y = (414, 311)
    scene.cycles.samples = 32
    scene.render.filepath = OUT + "spiel/f_"
    bpy.ops.render.render(animation=True)
    print("BAER_ANIM_OK")
dbg("FERTIG")
