# Lauf baer-gen-gross (11.11.2026), Rolle BAU FORM + TEXTUR: KOPIE von baer_maul_2c.py (Original unveraendert) fuer den neuen grossen
# Baeren E. Der E-Kopf steht nach der starren Kopf-Trafo im 2c-Kopfrahmen (Augenmitte, Auge-Nase-Linie -30,3 Grad) -> K_HO/K_HA/K_HB/K_HC,
# fbx2l, k_lippe, K_ECKE gelten unveraendert (Rahmen tier-Meter bei Groesse 1,0). Neu nur:
#   Q_B  = Querfaktor des Innenraums (E-Schnauze schmaler: Halbbreite auf Lippenhoehe a 0,35-0,45 gemessen 5,5-6,0 cm statt 7,2-7,9 -> 0,76)
#   Q_HU = Tiefenfaktor unten (E-Unterkiefer duenner: Haut 4,0-5,0 cm unter der Lippe statt 5,1-5,7; Probe: bei 0,80 stachen 6 Punkte
#          der Eckzahn-Tasche seitlich durchs Kinn, bei 0,70 noch 4 -> 0,64: 0 aussen), Q_HO oben (1,0); Q_ZL 0,72 (Eckzahn passt in die flachere Tasche)
#   Q_ZL = Laenge der Eckzaehne, Q_ZK = Kronen-Dicke min(1, Q_B + 0,1); DC = Versatz der Schnittflaeche (Start 0)
#   FLECK_* in den freien Streifen oben im 1024er Bild (textur2 uv_reserve_oben_px 74)
# Alles andere (Schnitt, Zwillinge, Ringe, Zaehne, Zunge, UV, Gewichtsteilung, Pruefungen) woertlich.
# Lauf baer-2c, Bau Gebiss (10.11.2026): Maul-Inneres (Schnitt an der Lippenlinie, Mundhoehle, Gebiss, Zunge) und die Flecken der
# Body-Textur als eigene Datei (SPEZ_2C.md 3.6), aufgerufen von baer_kampf_2c.py (maul_bauen bei netz_ersetzen, flecken_malen).
# Woertlich aus baer_kampf_2c.py/_pfote.py: Kopfrahmen (k_l2w .. k_lippe), fleck_uv, kiefer_anteil, der Schnitt in maul_bauen und
# die Gewichtsrechnung -> Lippenkante (M2) und Kopf-Aussenhaut bit-gleich. Neu: der Innenraum. Reines numpy (kein bpy).
# Statisch/offline geprueft, nicht gespielt.
import math

import numpy as np


def log(*a):
    print("TIER", *a, flush=True)


def sst(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


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
Q_B, Q_HO, Q_HU, Q_ZL, DC = 0.76, 1.0, 0.64, 0.72, 0.0      # gengross (siehe Kopf)
Q_ZK = min(1.0, Q_B + 0.1)
_QH = [1.0]


def k_lippe(a, B):
    return K_LIP(a) + 0.0055 * np.exp(-((B / 0.011) ** 2)) + DC



# ------------------------------------------------------------------ Maul: Schnitt an der Lippenlinie, Mundhoehle, Gebiss, Zunge
# Das Spielnetz hat ein geschlossenes Maul (bau_stehend.md). Hier wird es entlang c = lippe(a, |b|) vor dem Mundwinkel
# aufgeschnitten (Dreiecke an der Linie geteilt, Punkte auf der Linie verdoppelt: oben folgt dem Kopf, unten dem Kiefer) -- woertlich
# wie bisher. NEU (Lauf baer-2c, Bau Gebiss, SPEZ_2C.md 3): statt des flachen Beutels eine Mundhoehle aus Ringen je Kiefer (Lippe ->
# Lippeninnenseite/Vorhof -> Zahnfleisch aussen -> Zahnreihe -> Zahnfleisch innen -> Gaumen bzw. Mundboden), mit Taschen, in die
# beim Schliessen die Eckzaehne des anderen Kiefers greifen; hinten treffen sich beide an der Rachennaht zwischen den Mundwinkeln.
# Dazu vier gebogene Eckzaehne, je Kiefer sechs Schneidezaehne und zwei Backenzahn-Leisten, eine eigene Zunge. Alles EIN Netz mit
# EINEM Material; die Innenteile zeigen auf drei Flecken der 1024er Body-Textur, die die UV-Belegung frei laesst (Bau Koerper hat
# das UV neu gepackt: Flecken gegen die neue Karte geprueft, texturplatz_2c.py: frei 235 x 110 px bei (272, 0) mit 3 px Saum).
# Lagen: Plan in cm (X entlang der Schnauzenachse K_HA ab a = A_MITTE, Y = b seitlich, links positiv), h in cm ueber (oben) bzw.
# unter (unten) der Lippenhoehe K_LIP(a). Zahn-Masse aus SPEZ_2C.md 3.1 (Krone oben 4,6, unten 4,0 cm; Lage a 0,440 / 0,462).
FLECK_GAUMEN = (6, 4, 196, 64)      # gengross: freier Streifen oben (Bildpixel x, y von oben, Breite, Hoehe; 4 px Saum)
FLECK_ZUNGE = (212, 4, 196, 64)
FLECK_ZAHN = (418, 4, 120, 64)
TEX_R = 1024
FLECKEN = (FLECK_GAUMEN, FLECK_ZUNGE, FLECK_ZAHN)
ERGEBNIS = {}                        # Teil-Namen je Dreieck/Punkt fuer die Pruefer (nur Auskunft)


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



# ------------------------------------------------------------------ Bau Gebiss: Plan-Rechnung im Kopfrahmen
B_CM = K_FAKTOR * 100.0          # cm je b-/c-Einheit
A_MITTE = 0.37                   # Mitte der Ringe (Strahlen nach aussen)
N_HINTEN = 7                     # Punkte der Rachennaht zwischen den Mundwinkeln (vorher 5)
FUSS_TIEF = 0.35                 # cm, so tief sitzen Zahnfuesse mindestens hinter der Mundhoehle (im Fleisch)


def a_cm(a):
    return np.interp(a, _K_X, _K_Y) * B_CM


X_M = float(a_cm(A_MITTE))


def a_aus_x(X):
    return np.interp((np.asarray(X, dtype=float) + X_M) / B_CM, _K_Y, _K_X)


def lok_plan(X, Y, h):
    """Plan (cm) -> Kopfrahmen (a, b, c); h cm ueber K_LIP(a)"""
    X, Y, h = (np.asarray(v, dtype=float) for v in (X, Y, h))
    a = a_aus_x(X)
    return np.stack((a, Y / B_CM, K_LIP(a) + h / B_CM), -1)


def plan_lok(L):
    L = np.asarray(L, dtype=float)
    return a_cm(L[..., 0]) - X_M, L[..., 1] * B_CM


def winkel_lok(L):
    X, Y = plan_lok(L)
    return np.degrees(np.arctan2(Y, X))


def radius_lok(L):
    X, Y = plan_lok(L)
    return np.hypot(X, Y)


def rahmen_cm(v):
    """Kopfachsen (vorn, seitlich links, oben) in cm -> Tier-Meter"""
    v = np.asarray(v, dtype=float)
    return (v[..., 0:1] * K_HA + v[..., 1:2] * K_HB + v[..., 2:3] * K_HC) / 100.0


def rand_profil(th, r):
    """Abstand der Lippe/Naht von der Mitte je |theta| (beide Seiten gemittelt)"""
    ta = np.abs(np.asarray(th, dtype=float))
    o = np.argsort(ta)
    ta, rr = ta[o], np.asarray(r, dtype=float)[o]
    gx = np.linspace(0.0, 180.0, 181)
    gy = np.interp(gx, ta, rr)
    k = np.exp(-0.5 * (np.arange(-3, 4) / 1.5) ** 2)
    k /= k.sum()
    gy = np.convolve(np.pad(gy, 3, mode="edge"), k, mode="valid")
    return lambda t: np.interp(np.abs(np.asarray(t, dtype=float)), gx, gy)


def ring_tab(punkte):
    """Ring aus Stuetzpunkten (X, |Y|, h) von vorn (Y = 0) nach hinten (Y = 0) -> (theta, r, h) ueber 0..180 Grad"""
    P = np.array(punkte, dtype=float)
    P[:, 1] *= Q_B; P[:, 2] *= _QH[0]          # gengross: Innenraum quer/tief skaliert
    th = np.degrees(np.arctan2(P[:, 1], P[:, 0]))
    assert np.all(np.diff(th) > 0), ("Ring nicht sternfoermig um die Mitte", np.round(th, 1))
    return th, np.hypot(P[:, 0], P[:, 1]), P[:, 2]


def ring_lage(tab, th_s):
    th, r, h = tab
    th_s = np.asarray(th_s, dtype=float)
    ta = np.abs(th_s)
    rr, hh = np.interp(ta, th, r), np.interp(ta, th, h)
    return rr * np.cos(np.radians(th_s)), rr * np.sin(np.radians(th_s)), hh


def _dichte(ta):
    """Punktdichte je |theta|: vorn (Schneide-/Eckzaehne, Taschen) dicht, hinten duenn"""
    return 1.0 + 2.2 * np.exp(-0.5 * ((ta - 33.0) / 13.0) ** 2) + 2.5 * np.exp(-0.5 * ((ta - 38.0) / 4.0) ** 2) + 0.6 * np.exp(-0.5 * (ta / 10.0) ** 2) - 0.45 * sst(120.0, 160.0, ta)


def th_verteilung(n):
    """n (gerade) Winkel von -180 bis < 180, symmetrisch, mit 0 und 180"""
    tt = np.linspace(0.0, 180.0, 1801)
    w = _dichte(tt)
    cdf = np.concatenate(([0.0], np.cumsum((w[1:] + w[:-1]) * 0.5)))
    cdf /= cdf[-1]
    k = n // 2
    th_h = np.interp(np.arange(k + 1) / k, cdf, tt)
    return np.concatenate((-th_h[::-1][:-1], th_h[:-1]))


def zip_ringe(A, thA, B, thB):
    """Dreiecke zwischen zwei geschlossenen Schleifen (beide mit steigendem theta); n_A + n_B Dreiecke"""
    def aufrollen(ids, th):
        th = np.asarray(th, dtype=float)
        o = int(np.argmin(th))
        ids = list(ids[o:]) + list(ids[:o])
        t = list(th[o:]) + list(th[:o])
        tu = np.degrees(np.unwrap(np.radians(np.array(t))))      # nur echte Spruenge (> 180 Grad) zaehlen als Umlauf
        tu = list(np.maximum.accumulate(tu))                     # kleine Rueckschritte der Lippenlinie (Punkte fast gleich) glaetten
        return ids + [ids[0]], tu + [tu[0] + 360.0]
    a, ta = aufrollen(A, thA)
    b, tb = aufrollen(B, thB)
    i = j = 0
    tris = []
    while i < len(a) - 1 or j < len(b) - 1:
        if j == len(b) - 1 or (i < len(a) - 1 and ta[i + 1] <= tb[j + 1]):
            tris.append((a[i], a[i + 1], b[j]))
            i += 1
        else:
            tris.append((a[i], b[j + 1], b[j]))
            j += 1
    return tris


# ------------------------------------------------------------------ Bau Gebiss: Ringe (X, |Y|, h cm), rechts gleich links
# Oben (Kopf): U1 Vorhof aussen (Lippeninnenseite oben), U1b Vorhof innen, U2 Zahnfleisch aussen oben, U3 Zahnreihe (First),
# U4 Zahnfleisch innen, U5 Gaumenrand, Mitte = Gaumendach. Tasche fuer den unteren Eckzahn bei theta 22-40 (h bis 4,4 cm).
_QH[0] = Q_HO
RING_O = [
    ring_tab([(7.60, 0.00, 2.2), (7.55, 1.50, 2.2), (7.45, 2.50, 2.8), (7.30, 3.40, 3.8), (6.95, 4.20, 4.4), (6.40, 4.85, 4.4),
              (6.00, 5.65, 2.4), (5.30, 6.35, 1.7), (3.50, 6.60, 1.5), (1.40, 6.80, 1.5), (-1.00, 7.10, 1.5), (-3.50, 7.30, 1.3),
              (-5.50, 7.40, 1.1), (-7.30, 5.50, 1.0), (-7.60, 0.00, 1.0)]),
    ring_tab([(7.40, 0.00, 2.2), (7.35, 1.40, 2.2), (6.80, 2.30, 3.0), (5.80, 2.90, 4.4), (5.15, 3.50, 4.4), (5.10, 4.40, 4.4),
              (5.55, 5.75, 2.4), (5.20, 6.25, 1.6), (3.45, 6.45, 1.4), (1.40, 6.60, 1.4), (-1.00, 6.90, 1.4), (-3.50, 7.10, 1.25),
              (-5.40, 7.20, 1.1), (-7.10, 5.30, 1.0), (-7.40, 0.00, 1.0)]),
    ring_tab([(7.00, 0.00, 1.0), (6.98, 1.40, 1.0), (6.85, 2.30, 1.0), (5.55, 2.75, 1.0), (5.00, 3.40, 1.0), (4.95, 4.30, 1.0),
              (5.30, 5.55, 1.0), (4.00, 6.05, 0.9), (1.40, 6.30, 0.8), (-1.50, 6.30, 0.8), (-4.20, 6.30, 0.8), (-5.80, 4.80, 0.9),
              (-6.60, 0.00, 1.0)]),
    ring_tab([(6.55, 0.00, 0.35), (6.55, 0.50, 0.35), (6.50, 1.30, 0.35), (6.40, 2.05, 0.35), (5.15, 2.75, 0.5), (4.65, 3.60, 0.5),
              (4.79, 5.00, 0.4), (3.00, 5.50, 0.35), (1.40, 5.60, 0.35), (-1.50, 5.60, 0.35), (-4.20, 5.60, 0.35), (-5.50, 4.20, 0.6),
              (-6.00, 0.00, 0.8)]),
    ring_tab([(5.85, 0.00, 1.4), (5.85, 0.45, 1.4), (5.80, 1.15, 1.4), (5.70, 1.85, 1.4), (4.55, 2.40, 1.5), (4.05, 3.10, 1.5),
              (4.15, 4.25, 1.5), (2.60, 4.75, 1.5), (1.20, 4.85, 1.5), (-1.50, 4.85, 1.5), (-3.90, 4.85, 1.5), (-5.00, 3.60, 1.6),
              (-5.40, 0.00, 1.6)]),
    ring_tab([(4.80, 0.00, 2.0), (4.75, 1.00, 2.0), (4.50, 2.00, 2.0), (3.60, 2.80, 2.0), (2.40, 3.60, 2.0), (0.50, 3.80, 2.0),
              (-2.00, 3.80, 2.0), (-3.80, 3.20, 2.0), (-4.60, 0.00, 2.0)]),
]
N_RING_O = [28, 28, 24, 24, 22, 14]
TEILE_O = ["wand_o", "wand_o", "wand_o", "wand_o", "gaumen", "gaumen"]
MITTE_O = 2.2
# Unten (Kiefer): L05 Lippeninnenseite (Taschenwand halb zwischen Haut und oberem Eckzahn), L1 Vorhof aussen, L1b Vorhof innen, L2 Zahnfleisch aussen, L3 Zahnreihe, L4 Zahnfleisch innen, L5 Mundboden.
# Tasche fuer den oberen Eckzahn bei theta 38-54 (Tiefe bis 4,9 cm; Haut dort 5,1-5,7 cm unter der Lippe).
_QH[0] = Q_HU
RING_U = [
    ring_tab([(8.15, 0.00, 0.20), (8.10, 1.55, 0.20), (8.01, 2.68, 0.25), (7.78, 3.90, 0.30), (7.48, 4.73, 0.35),
              (6.35, 4.61, 1.30), (5.90, 4.95, 1.50), (5.50, 5.31, 1.50), (5.15, 5.72, 1.50), (4.77, 6.11, 1.30),
              (4.19, 6.22, 1.00), (1.57, 6.76, 0.80), (-1.00, 7.08, 0.75), (-3.89, 7.56, 0.70), (-6.18, 7.86, 0.60),
              (-8.06, 5.75, 0.50), (-8.20, 0.00, 0.50)]),
    ring_tab([(7.97, 0.00, 0.40), (7.90, 1.50, 0.38), (7.75, 2.60, 0.40), (7.55, 3.78, 0.60), (7.20, 4.55, 0.70),
              (6.07, 4.41, 1.80), (5.44, 4.33, 4.40), (5.09, 4.58, 4.70), (4.76, 4.93, 4.70), (4.44, 5.29, 4.40),
              (4.21, 5.59, 3.20), (3.40, 5.60, 2.00), (1.40, 6.00, 1.60), (-1.00, 6.30, 1.50), (-3.50, 6.80, 1.40),
              (-5.50, 7.00, 1.20), (-7.30, 5.20, 1.00), (-7.60, 0.00, 1.00)]),
    ring_tab([(7.90, 0.00, 0.40), (7.84, 1.45, 0.38), (7.70, 2.50, 0.40), (7.50, 3.65, 0.60), (7.15, 4.45, 0.65),
              (4.31, 3.25, 4.40), (3.90, 3.51, 4.75), (3.58, 3.84, 4.75), (3.40, 4.20, 4.40), (3.29, 4.53, 3.00),
              (3.00, 5.00, 1.80), (1.40, 5.30, 1.60), (-1.00, 5.60, 1.50), (-3.50, 6.20, 1.35), (-5.40, 6.60, 1.20),
              (-7.10, 5.00, 1.00), (-7.40, 0.00, 1.00)]),
    ring_tab([(7.85, 0.00, 0.30), (7.82, 1.40, 0.30), (7.75, 2.40, 0.45), (7.40, 3.55, 0.55), (7.10, 4.35, 0.60),
              (4.31, 3.25, 1.10), (3.90, 3.51, 1.15), (3.58, 3.84, 1.15), (3.40, 4.20, 1.10), (3.30, 4.55, 1.20),
              (2.90, 4.85, 1.10), (1.40, 4.85, 1.10), (-1.00, 4.85, 1.10), (-3.50, 4.85, 1.10), (-5.40, 4.50, 1.10),
              (-6.60, 0.00, 1.20)]),
    ring_tab([(7.40, 0.00, 0.20), (7.39, 0.45, 0.20), (7.35, 1.30, 0.20), (7.33, 2.15, 0.25), (6.29, 3.50, 0.60),
              (4.75, 3.05, 0.60), (3.10, 2.85, 0.60), (2.90, 4.00, 0.40), (-3.00, 4.00, 0.40), (-4.60, 3.00, 0.80),
              (-5.40, 0.00, 1.20)]),
    ring_tab([(6.85, 0.00, 1.90), (6.85, 0.45, 1.90), (6.80, 1.25, 1.90), (6.75, 2.05, 1.90), (5.50, 2.95, 1.60),
              (4.20, 2.50, 1.40), (2.75, 2.45, 1.30), (2.50, 3.35, 1.30), (-2.80, 3.30, 1.30), (-4.00, 2.40, 1.50),
              (-4.60, 0.00, 1.70)]),
    ring_tab([(6.20, 0.00, 2.10), (6.10, 1.30, 2.10), (5.70, 2.10, 2.10), (3.80, 2.30, 2.10), (2.00, 2.50, 2.10),
              (-2.50, 2.60, 2.10), (-3.60, 1.80, 2.10), (-4.00, 0.00, 2.10)]),
]
N_RING_U = [28, 28, 28, 24, 24, 22, 14]
TEILE_U = ["wand_u", "wand_u", "wand_u", "wand_u", "wand_u", "boden", "boden"]
MITTE_U = 2.2 * Q_HU

# ------------------------------------------------------------------ Bau Gebiss: Zaehne (rechte Seite +Y = links; gespiegelt)
# Eckzahn: Hals (X, Y, h ueber/unter der Lippe), Wurzelstumpf ins Zahnfleisch, Krone gebogen (Bogen nach hinten), 6 Seiten,
# Ringe Wurzel/Hals/0,45/0,8 + Spitze = 42 Dreiecke. Schneidezahn: Keil (4 Fuss- + 2 Spitzenpunkte, 6 Dreiecke). Backenzahn-Leiste:
# 5 + 5 Fusspunkte, 8 Hoecker im Kamm, 24 Dreiecke. Alle offen am Fuss (im Zahnfleisch), Gewicht 1,0 Kopf bzw. Kiefer.
ZAEHNE = [
    dict(name="eck_o", art="eck", kiefer="o", X=4.72, Y=4.80, h=0.6, wurzel=1.6, laenge=5.2, vor=10.0, ein=10.0, bogen=35.0, ra=1.05, rq=0.80),
    dict(name="eck_u", art="eck", kiefer="u", X=6.29, Y=3.50, h=0.6, wurzel=0.7, laenge=4.6, vor=15.0, ein=-8.0, bogen=45.0, ra=0.95, rq=0.75),
    dict(name="i1_o", art="schneide", kiefer="o", X=6.55, Y=0.47, h=0.35, wurzel=1.25, krone=1.20, breit=0.90, dick=0.85),
    dict(name="i2_o", art="schneide", kiefer="o", X=6.50, Y=1.37, h=0.35, wurzel=1.25, krone=1.30, breit=0.92, dick=0.90),
    dict(name="i3_o", art="schneide", kiefer="o", X=6.40, Y=2.20, h=0.35, wurzel=1.25, krone=1.45, breit=1.00, dick=1.00),
    dict(name="i1_u", art="schneide", kiefer="u", X=7.39, Y=0.42, h=0.25, wurzel=0.75, krone=0.95, breit=0.82, dick=0.70),
    dict(name="i2_u", art="schneide", kiefer="u", X=7.35, Y=1.25, h=0.25, wurzel=0.75, krone=1.00, breit=0.85, dick=0.70),
    dict(name="i3_u", art="schneide", kiefer="u", X=7.28, Y=2.10, h=0.30, wurzel=0.75, krone=1.10, breit=0.90, dick=0.65),
    dict(name="back_o", art="backe", kiefer="o", X0=1.60, X1=-3.70, Y=5.60, h=0.35, wurzel=0.9, krone=1.10, breit=1.30),
    dict(name="back_u", art="backe", kiefer="u", X0=2.90, X1=-3.00, Y=4.00, h=0.40, wurzel=0.9, krone=1.00, breit=1.20),
]
# Zunge (Kiefer): Querschnitte (X, halbe Breite, Tiefe Mitte oben, Rand hoeher um, Tiefe Unterseite), Spitze rund
ZUNGE = [(4.85, 2.10, 0.85, 0.25, 2.20), (3.90, 2.70, 0.80, 0.35, 2.25), (2.20, 3.00, 0.80, 0.40, 2.30), (0.00, 3.10, 0.85, 0.40, 2.35),
         (-2.20, 3.30, 0.95, 0.35, 2.40), (-4.20, 3.60, 1.10, 0.30, 2.50)]
ZUNGE_SPITZE = (5.40, 1.25)          # X, Tiefe
# gengross: Zaehne und Zunge quer/tief skaliert
for _z in ZAEHNE:
    if "Y" in _z:
        _z["Y"] *= Q_B
    for _k in ("ra", "rq", "breit", "dick"):
        if _k in _z:
            _z[_k] *= Q_ZK
    if _z["art"] == "eck":
        _z["laenge"] *= Q_ZL
    if _z["kiefer"] == "u":
        _z["h"] *= Q_HU
ZUNGE = [(X, hw * Q_B, ht * Q_HU, rd * Q_HU, hb * Q_HU) for X, hw, ht, rd, hb in ZUNGE]
ZUNGE_SPITZE = (ZUNGE_SPITZE[0], ZUNGE_SPITZE[1] * Q_HU)


def _ort(X, Y, h, kiefer):
    """Punkt im Plan (cm) -> Tier-Meter; h ueber (oben) bzw. unter (unten) der Lippenhoehe"""
    return l2fbx(lok_plan(X, Y, h if kiefer == "o" else -h))


def zahn_netz(z, sg):
    """Punkte (Tier-Meter), Dreiecke (lokal), Deckel-Ring (lokal), t je Punkt (0 Wurzel .. 1 Spitze), Art"""
    ab = 1.0 if z["kiefer"] == "o" else -1.0          # Krone zeigt nach unten (oben) bzw. nach oben (unten)
    if z["art"] == "eck":
        hals = _ort(z["X"], sg * z["Y"], z["h"], z["kiefer"])
        vor, ein, phi = math.radians(z["vor"]), math.radians(z["ein"]), math.radians(z["bogen"])
        d0 = np.array((math.sin(vor), -sg * math.sin(ein), -ab * math.cos(vor)))     # Kopfachsen (vorn, links, oben); ein > 0 nach innen
        d0 /= np.linalg.norm(d0)
        k = np.array((-1.0, 0.0, 0.0))
        k = k - (k @ d0) * d0
        k /= np.linalg.norm(k)
        q = np.cross(d0, k)
        n = 80
        c = np.zeros(3)
        mitte = [c.copy()]
        for i in range(n):
            t = (i + 0.5) / n
            c = c + (math.cos(phi * t) * d0 + math.sin(phi * t) * k) * z["laenge"] / n
            mitte.append(c.copy())
        P, tt = [], []
        for t, f in ((-1.0, 1.0), (0.0, 1.0), (0.45, (1 - 0.45) ** 0.6), (0.8, (1 - 0.8) ** 0.6)):      # kraeftige Krone, spitz erst am Ende
            if t < 0:
                cm = -d0 * z["wurzel"]
                e1 = k
                f = 0.85                                  # Wurzel etwas schmaler (bleibt im Fleisch)
            else:
                cm = mitte[int(round(t * n))]
                e1 = -math.sin(phi * t) * d0 + math.cos(phi * t) * k
            for s in range(6):
                w = 2 * math.pi * s / 6
                P.append(cm + f * (z["ra"] * math.cos(w) * e1 + z["rq"] * math.sin(w) * q))
                tt.append(0.05 if t < 0 else 0.25 + 0.75 * t)
        P.append(mitte[-1])
        tt.append(1.0)
        P = hals + rahmen_cm(np.array(P))
        tri = []
        for r in range(3):
            for s in range(6):
                a0, a1 = r * 6 + s, r * 6 + (s + 1) % 6
                b0, b1 = a0 + 6, a1 + 6
                tri += [(a0, a1, b1), (a0, b1, b0)]
        for s in range(6):
            tri.append((18 + s, 18 + (s + 1) % 6, 24))
        return P, tri, list(range(6)), tt, "eck"
    if z["art"] == "schneide":
        # Keil quer zur Zahnreihe: vorn = Richtung zur Lippe (+X, leicht seitlich nach aussen), breit entlang der Reihe
        winkel = math.atan2(sg * z["Y"], 9.0)            # Reihe biegt sich nach aussen
        vorn = np.array((math.cos(winkel), math.sin(winkel)))
        quer = np.array((-vorn[1], vorn[0]))
        m = np.array((z["X"], sg * z["Y"]))
        w2, d2 = z["breit"] / 2.0, z["dick"] / 2.0
        pts, tt = [], []
        for sv, sq in ((1, -1), (1, 1), (-1, 1), (-1, -1)):            # Fuss: vorn-rechts, vorn-links, hinten-links, hinten-rechts
            xy = m + vorn * d2 * sv + quer * w2 * sq
            pts.append(_ort(xy[0], xy[1], z["h"] + z["wurzel"] * (0.6 if (z["kiefer"] == "u" and sv > 0) else 1.0), z["kiefer"]))
            tt.append(0.05)
        for sq in (-1, 1):                                               # Schneide (vorn 0,1 cm hinter der Mitte, 0,7 der Breite)
            xy = m - vorn * 0.1 + quer * w2 * 0.55 * sq
            pts.append(_ort(xy[0], xy[1], z["h"] - z["krone"], z["kiefer"]))
            tt.append(1.0)
        P = np.array(pts)
        tri = [(0, 1, 5), (0, 5, 4), (2, 3, 4), (2, 4, 5), (3, 0, 4), (1, 2, 5)]
        return P, tri, [0, 1, 2, 3], tt, "schneide"
    # Backenzahn-Leiste entlang X, Hoecker im Kamm
    X0, X1 = z["X0"], z["X1"]
    pts, tt = [], []
    for seite in (1, -1):                               # aussen (|Y| groesser), innen
        for i in range(5):
            x = X0 + (X1 - X0) * i / 4.0
            pts.append(_ort(x, sg * (z["Y"] + seite * z["breit"] / 2.0), z["h"] + z["wurzel"], z["kiefer"]))
            tt.append(0.05)
    for i in range(8):
        x = X0 + (X1 - X0) * (0.03 + 0.94 * i / 7.0)
        hk = z["krone"] * (1.0 if i % 2 == 0 else 0.72)
        pts.append(_ort(x, sg * z["Y"], z["h"] - hk, z["kiefer"]))
        tt.append(1.0 if i % 2 == 0 else 0.8)
    P = np.array(pts)

    def strip(fuss, kamm):
        tris, i, j = [], 0, 0
        while i < len(fuss) - 1 or j < len(kamm) - 1:
            if j == len(kamm) - 1 or (i < len(fuss) - 1 and (i + 1) / (len(fuss) - 1) <= (j + 1) / (len(kamm) - 1)):
                tris.append((fuss[i], fuss[i + 1], kamm[j]))
                i += 1
            else:
                tris.append((fuss[i], kamm[j + 1], kamm[j]))
                j += 1
        return tris
    aus, inn, kamm = list(range(5)), list(range(5, 10)), list(range(10, 18))
    tri = strip(aus, kamm) + [(b, a, c) for a, b, c in strip(inn, kamm)]
    tri += [(inn[0], aus[0], kamm[0]), (aus[-1], inn[-1], kamm[-1])]
    return P, tri, aus + inn[::-1], tt, "backe"


def zungen_netz():
    """Geschlossene Zunge (Kiefer): 6 Querschnitte zu je 8 Punkten, runde Spitze, Wurzel zu. Rueckgabe Punkte, Dreiecke, [], UV-Plan"""
    pts, uvp = [], []
    for (X, hw, ht, rand, hb) in ZUNGE:
        quer = [(-hw, ht - rand), (-0.5 * hw, ht - 0.3 * rand), (0.0, ht), (0.5 * hw, ht - 0.3 * rand), (hw, ht - rand),
                (0.8 * hw, hb - 0.1), (0.0, hb), (-0.8 * hw, hb - 0.1)]
        for Y, t in quer:
            pts.append(_ort(X, Y, t, "u"))
            uvp.append((X, Y))
    Xs, ts = ZUNGE_SPITZE
    pts.append(_ort(Xs, 0.0, ts, "u"))
    uvp.append((Xs, 0.0))
    ns = len(ZUNGE)
    tri = []
    for r in range(ns - 1):
        for s in range(8):
            a0, a1 = r * 8 + s, r * 8 + (s + 1) % 8
            b0, b1 = a0 + 8, a1 + 8
            tri += [(a0, a1, b1), (a0, b1, b0)]
    sp = ns * 8
    tri += [(s, sp, (s + 1) % 8) for s in range(8)]
    w0 = (ns - 1) * 8
    w_m = len(pts)
    X, hw, ht, rand, hb = ZUNGE[-1]
    pts.append(_ort(X - 0.4, 0.0, 0.5 * (ht + hb), "u"))
    uvp.append((X - 0.4, 0.0))
    tri += [(w0 + (s + 1) % 8, w_m, w0 + s) for s in range(8)]
    return np.array(pts), tri, [], uvp


# ------------------------------------------------------------------ Bau Gebiss: UV je Dreieck (Flecken siehe flecken_malen)
V_WAND = 9.0      # cm Weg von der Lippe, der in den Wand-Teil eines Flecks passt
ZEILE_WAND = 0.40  # Anteil der Fleck-Hoehe fuer die Waende (oben), darunter Gaumen bzw. Zunge
GAUMEN_X = (6.6, -6.2)
ZUNGE_X = (5.5, -4.6)


def uv_dreieck(teil, pts):
    """pts: je Ecke (X, Y, h, theta, v) bzw. bei Zaehnen v = t, bei der Zunge (X, Y). Rueckgabe 3 x 2 UV"""
    P = np.array(pts, dtype=float)
    if teil in ("wand_o", "wand_u", "boden"):
        fl = FLECK_GAUMEN if teil == "wand_o" else FLECK_ZUNGE
        th = np.abs(P[:, 3])
        if np.isnan(th).any():               # Mittelpunkt: Winkel der beiden anderen Ecken
            th = np.where(np.isnan(th), np.nanmean(th), th)
        s = th / 180.0
        t = np.clip(P[:, 4] / V_WAND, 0.0, 1.0) * ZEILE_WAND
        return fleck_uv(fl, s, t)
    if teil == "gaumen":
        s = (P[:, 1] + 7.0) / 14.0
        t = ZEILE_WAND + 0.03 + (GAUMEN_X[0] - P[:, 0]) / (GAUMEN_X[0] - GAUMEN_X[1]) * (0.97 - ZEILE_WAND)
        return fleck_uv(FLECK_GAUMEN, s, t)
    if teil == "zunge":
        s = (P[:, 1] + 4.0) / 8.0
        t = ZEILE_WAND + 0.03 + (ZUNGE_X[0] - P[:, 0]) / (ZUNGE_X[0] - ZUNGE_X[1]) * (0.97 - ZEILE_WAND)
        return fleck_uv(FLECK_ZUNGE, s, t)
    # Zaehne: Spalte je Art, Zeile = t (0 Wurzel .. 1 Spitze)
    spalte = 0.17 if teil.startswith("zahn_eck") else (0.5 if teil.startswith("zahn_i") else 0.83)
    return fleck_uv(FLECK_ZAHN, np.full(3, spalte), P[:, 4])



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

    # ================================================================ Bau Gebiss (Lauf baer-2c): Innenraum neu (SPEZ_2C.md 3)
    # Ab hier neu. Bis hierher (Schnitt, Zwillinge, UV der Lippenkante) woertlich wie baer_kampf_pfote.py:1898-2005 -> Zone M2 bit-gleich.
    VS, WS, US, TEIL = [], [], [], []      # Lage (Spielnetz), Kieferanteil, (Fleck, s, t) je Punkt, Teil-Name
    ih = namen.index("Bip01_Head")

    def dazu(p_fbx, wj, teil):
        VS.append(np.asarray(p_fbx, dtype=float))
        WS.append(float(wj))
        TEIL.append(teil)
        return n_ken + len(VS) - 1

    LCk = fbx2l(V1)
    pa, pb = LCk[kette_[0]], LCk[kette_[-1]]
    hinten = []
    for k in range(1, N_HINTEN + 1):
        q = pb + (pa - pb) * (k / (N_HINTEN + 1.0))      # von der linken Ecke (Kettenende) zur rechten (Kettenanfang)
        q = np.array((q[0], q[1], float(K_LIP(q[0]))))
        hinten.append(dazu(l2fbx(q), 0.5, "naht"))

    def lok_von(i):
        return LCk[i] if i < n_ken else fbx2l(VS[i - n_ken])

    # Randschleifen: oben Oberlippe (rechts -> vorn -> links) + Naht (links -> rechts), unten ebenso mit den Unterlippen-Zwillingen
    schl_o = list(kette_) + hinten
    schl_u = list(lo_) + hinten
    th_rand = np.array([winkel_lok(lok_von(i)) for i in schl_o])
    r_rand = np.array([radius_lok(lok_von(i)) for i in schl_o])
    rand_r = rand_profil(th_rand, r_rand)
    PT = {}                              # Punkt-Index -> (Plan X, Y, h, theta, v) fuer UV

    for i in schl_o + schl_u:
        L_ = lok_von(i)
        X_, Y_ = plan_lok(L_)
        PT[i] = (float(X_), float(Y_), 0.0, float(winkel_lok(L_)), 0.0)

    def schale(schleife, th_schl, ringe, seite, teile, mitte_h):
        """Ringe von der Lippe nach innen (Zickzack nach theta), Faecher zur Mitte. v = Weg von der Lippe ueber die Ringe (cm)."""
        tabs = [t for t, _n in ringe]

        def lage(k, th):
            th = np.atleast_1d(np.asarray(th, dtype=float))
            if k < 0:
                r = rand_r(th)
                return r * np.cos(np.radians(th)), r * np.sin(np.radians(th)), np.zeros_like(th)
            return ring_lage(tabs[k], th)

        def v_von(k, th):
            v = 0.0
            for j in range(k + 1):
                X1, Y1, h1 = lage(j, th)
                X0, Y0, h0 = lage(j - 1, th)
                v += float(np.sqrt((X1 - X0) ** 2 + (Y1 - Y0) ** 2 + (h1 - h0) ** 2)[0])
            return v
        tris = {t: [] for t in dict.fromkeys(teile)}       # feste Reihenfolge (set() waere je Lauf anders)
        A, thA = schleife, th_schl
        for k, ((tab, n), teil) in enumerate(zip(ringe, teile)):
            th_s = th_verteilung(n)
            X_, Y_, h_ = ring_lage(tab, th_s)
            B = []
            for j in range(n):
                L_ = lok_plan(X_[j], Y_[j], seite * h_[j])
                f_ = float(L_[2] - k_lippe(L_[0], abs(L_[1])))
                wj = float(kiefer_anteil(np.array([L_[0]]), np.array([f_]), np.array([seite]))[0])
                i = dazu(l2fbx(L_), wj, teil)
                PT[i] = (float(X_[j]), float(Y_[j]), float(seite * h_[j]), float(th_s[j]), v_von(k, th_s[j]))
                B.append(i)
            tris[teil] += zip_ringe(A, thA, B, th_s)
            A, thA = B, th_s
        XA = np.array([PT[i][0] for i in A])
        mx = float(0.5 * (XA.max() + XA.min()))
        L_ = lok_plan(mx, 0.0, seite * mitte_h)
        f_ = float(L_[2] - k_lippe(L_[0], 0.0))
        wj = float(kiefer_anteil(np.array([L_[0]]), np.array([f_]), np.array([seite]))[0])
        m = dazu(l2fbx(L_), wj, teile[-1])
        PT[m] = (mx, 0.0, seite * mitte_h, float("nan"), float(np.mean([PT[i][4] for i in A])) + 2.0)
        tris[teile[-1]] += [(A[j], A[(j + 1) % len(A)], m) for j in range(len(A))]
        return tris

    th_o = np.array([PT[i][3] for i in schl_o])
    th_u = np.array([PT[i][3] for i in schl_u])
    oben = schale(schl_o, th_o, [(RING_O[k], N_RING_O[k]) for k in range(len(RING_O))], +1, TEILE_O, MITTE_O)
    unten = schale(schl_u, th_u, [(RING_U[k], N_RING_U[k]) for k in range(len(RING_U))], -1, TEILE_U, MITTE_U)
    aussen = {(t[m], t[(m + 1) % 3]) for t in T2 for m in range(3)}

    def ausrichten(tris, x, y):
        d = {(t[m], t[(m + 1) % 3]) for t in tris for m in range(3)}
        if (x, y) in aussen:
            dreh = (x, y) in d
        else:
            assert (y, x) in aussen
            dreh = (y, x) in d
        return dreh

    alle_o = [t for k in oben for t in oben[k]]
    alle_u = [t for k in unten for t in unten[k]]
    if ausrichten(alle_o, kette_[1], kette_[2]):
        oben = {k: [(t[0], t[2], t[1]) for t in v] for k, v in oben.items()}
    if ausrichten(alle_u, lo_[1], lo_[2]):
        unten = {k: [(t[0], t[2], t[1]) for t in v] for k, v in unten.items()}

    # ---- Zaehne und Zunge: eigene Schalen, starr (oben Kopf, unten Kiefer), offen am Boden im Zahnfleisch
    schalen = []                                   # (Teil, Dreiecke, Deckel-Ring fuer die Volumenprobe)
    for z in ZAEHNE:
        for sg in (1.0, -1.0):
            P, tri, deckel, tt, art = zahn_netz(z, sg)
            wj = 1.0 if z["kiefer"] == "u" else 0.0
            ids = []
            for p_, t_ in zip(P, tt):
                i = dazu(p_, wj, "zahn_" + z["name"])
                PT[i] = (0.0, 0.0, 0.0, 0.0, float(t_))
                ids.append(i)
            schalen.append(("zahn_" + z["name"], [(ids[a_], ids[b_], ids[c_]) for a_, b_, c_ in tri], [ids[k] for k in deckel], art))
    P, tri, deckel, uvz = zungen_netz()
    ids = []
    for p_, u_ in zip(P, uvz):
        i = dazu(p_, 1.0, "zunge")
        PT[i] = (float(u_[0]), float(u_[1]), 0.0, 0.0, 0.0)
        ids.append(i)
    schalen.append(("zunge", [(ids[a_], ids[b_], ids[c_]) for a_, b_, c_ in tri], [ids[k] for k in deckel], "zunge"))

    # Zahnfuesse (offener Ring) muessen im Fleisch liegen: senkrecht zur Lippenebene (Kopf-c) gesucht wird die eigene Mundhoehle
    # direkt ueber/unter dem Fusspunkt; liegt der Fuss nicht mindestens FUSS_TIEF dahinter, wird er nur dorthin verschoben.
    VB = np.array(VS)
    V2 = np.vstack((V1, VB))
    LCa = fbx2l(V2)
    for nm, tri, deckel, art in schalen:
        if not deckel or nm == "zunge":
            continue
        seite = 1.0 if nm.endswith("_o") else -1.0
        hohle = [t for k in (oben if seite > 0 else unten) for t in (oben if seite > 0 else unten)[k]]
        A3 = LCa[np.array(hohle)]
        for v in deckel:
            p = LCa[v]
            q = A3[:, :, :2]
            d = (q[:, 1, 0] - q[:, 0, 0]) * (q[:, 2, 1] - q[:, 0, 1]) - (q[:, 2, 0] - q[:, 0, 0]) * (q[:, 1, 1] - q[:, 0, 1])
            ok = np.abs(d) > 1e-14
            d = np.where(ok, d, 1.0)
            l1 = ((p[0] - q[:, 0, 0]) * (q[:, 2, 1] - q[:, 0, 1]) - (q[:, 2, 0] - q[:, 0, 0]) * (p[1] - q[:, 0, 1])) / d
            l2 = ((q[:, 1, 0] - q[:, 0, 0]) * (p[1] - q[:, 0, 1]) - (p[0] - q[:, 0, 0]) * (q[:, 1, 1] - q[:, 0, 1])) / d
            tr_ = ok & (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
            if not tr_.any():
                continue
            cs = A3[tr_, 0, 2] + l1[tr_] * (A3[tr_, 1, 2] - A3[tr_, 0, 2]) + l2[tr_] * (A3[tr_, 2, 2] - A3[tr_, 0, 2])
            c_h = cs[np.argmin(np.abs(cs - p[2]))]
            soll = c_h + seite * FUSS_TIEF / B_CM
            if seite * (p[2] - soll) < 0:
                q2 = p.copy()
                q2[2] = soll
                V2[v] = l2fbx(q2)
                VS[v - n_ken] = V2[v]
    n2 = len(V2)
    # Ausrichtung der Schalen wie der Koerper (Vorzeichen des Volumens mit gedachtem Deckel)
    T_haupt = [list(t) for t in T2] + [list(t) for k in oben for t in oben[k]] + [list(t) for k in unten for t in unten[k]]

    def vol(tris):
        A_ = V2[np.array(tris)]
        return float(np.einsum("ij,ij->i", A_[:, 0], np.cross(A_[:, 1], A_[:, 2])).sum() / 6.0)

    vz_haupt = np.sign(vol(T_haupt))
    T_schalen, TEIL_D = [], []
    for nm, tri, deckel, art in schalen:
        if deckel:
            mitte = V2[deckel].mean(0)
            n_ = len(V2)
            V2x = np.vstack((V2, mitte[None]))
            A_ = V2x[np.array(tri + [(deckel[(k + 1) % len(deckel)], deckel[k], n_) for k in range(len(deckel))])]
            # Deckel-Richtung passend zur Schale: Kanten des Rings laufen in der Schale in einer Richtung; der Deckel braucht die Gegenrichtung
            d = {(t[m], t[(m + 1) % 3]) for t in tri for m in range(3)}
            if (deckel[0], deckel[1]) in d:
                A_ = V2x[np.array(tri + [(deckel[(k + 1) % len(deckel)], deckel[k], n_) for k in range(len(deckel))])]
            else:
                A_ = V2x[np.array(tri + [(deckel[k], deckel[(k + 1) % len(deckel)], n_) for k in range(len(deckel))])]
            v_ = float(np.einsum("ij,ij->i", A_[:, 0], np.cross(A_[:, 1], A_[:, 2])).sum() / 6.0)
        else:
            v_ = vol(tri)
        if np.sign(v_) != vz_haupt:
            tri = [(t[0], t[2], t[1]) for t in tri]
        T_schalen += [list(t) for t in tri]
        TEIL_D += [nm] * len(tri)
    # ---- Gewichte: der Kopfanteil teilt sich in Kopf und Kiefer (wie bisher; neue Punkte: Kieferanteil aus WS)
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
    T_innen, TEIL_I = [], []
    for k in oben:
        T_innen += [list(t) for t in oben[k]]
        TEIL_I += [k] * len(oben[k])
    for k in unten:
        T_innen += [list(t) for t in unten[k]]
        TEIL_I += [k] * len(unten[k])
    T_all = [list(t) for t in T2] + T_innen + T_schalen
    teil_dreieck = ["aussen"] * len(T2) + TEIL_I + TEIL_D
    UVm = [np.array(u) for u in UV2]
    for t, nm in zip(T_innen + T_schalen, TEIL_I + TEIL_D):
        UVm.append(uv_dreieck(nm, [PT[i] for i in t]))
    T_all = np.array(T_all, dtype=np.int64)
    UVm = np.array(UVm)
    # ---- Pruefung: Koerper geschlossen und gleich ausgerichtet; Schalen ohne doppelte Kanten, offen nur am Deckel-Ring
    gk = {}
    for t in T_haupt:
        for m in range(3):
            e = (int(t[m]), int(t[(m + 1) % 3]))
            gk[e] = gk.get(e, 0) + 1
    doppelt = sum(1 for v in gk.values() if v > 1)
    offen = sum(1 for e in gk if (e[1], e[0]) not in gk)
    assert doppelt == 0 and offen == 0, ("Netz offen oder verdreht", doppelt, offen)
    for nm, tri, deckel, art in schalen:
        g2 = {}
        for t in tri:
            for m in range(3):
                e = (int(t[m]), int(t[(m + 1) % 3]))
                g2[e] = g2.get(e, 0) + 1
        assert max(g2.values()) == 1, ("Schale mit doppelter Kante", nm)
        rand = {e for e in g2 if (e[1], e[0]) not in g2}
        assert {v for e in rand for v in e} <= set(deckel), ("Schale offen ausserhalb des Deckels", nm)
    scharf = [(kette_[i], kette_[i + 1]) for i in range(len(kette_) - 1)] + [(lo_[i], lo_[i + 1]) for i in range(len(lo_) - 1)]
    hk = [kette_[-1]] + hinten + [kette_[0]]
    scharf += [(hk[i], hk[i + 1]) for i in range(len(hk) - 1)]
    zaehl = {}
    for nm in teil_dreieck[len(T2):]:
        k_ = nm.split("_")[0] if nm.startswith("zahn") else nm
        zaehl[k_] = zaehl.get(k_, 0) + 1
    info = dict(kette=len(kette_), innen=len(T_all) - len(T2), teile=zaehl, punkte=n2, dreiecke=len(T_all),
                kiefer_punkte=int((W2[:, -1] > 0.5).sum()))
    log("Maul:", info)
    ERGEBNIS.clear()
    ERGEBNIS.update(dict(n_aussen=len(T2), n_ken=n_ken, teil_dreieck=teil_dreieck, teil_punkt=["aussen"] * n_ken + TEIL,
                         kette=list(kette_), lo=list(lo_), hinten=list(hinten), schalen=[(nm, art) for nm, _t, _d, art in schalen],
                         deckel={nm: d for nm, _t, d, _a in schalen}))
    return V2, T_all, UVm, W2, namen + ["Bip01_Jaw"], scharf


# ------------------------------------------------------------------ Flecken in der 1024er Body-Textur (kl: Bildfeld h x w x 4, Zeile 0 = unten)
# Farben sRGB 0..1 nach SPEZ_2C.md 3.3: Lefze schwarz (28/24/24) -> rosa, Schleimhaut/Zahnfleisch (110/62/68 -> 140/85/90),
# Gaumen (135-165/80-100/92-112) mit 8 gemalten Querrillen, Rachen dunkel (40/20/22), Zunge rosa-mauve (175-205/98-125/110-135) mit
# Mittelrinne, Zaehne Zahnfleisch dunkel -> Hals 190/170/120 -> Spitze 235/228/210.
def _c(*rgb):
    return np.array(rgb, dtype=float) / 255.0


def _mix(a, b, t):
    return a + (b - a) * np.asarray(t)[..., None]


SCHWARZ, SCHLEIM, FLEISCH, RACHEN = _c(28, 24, 24), _c(150, 84, 94), _c(122, 66, 74), _c(40, 20, 22)


def _wand(s, v):
    lippe = sst(1.3, 2.3, v)                                   # schwarzer Lippenstreifen (Innenseite steil: 1,3 cm Weg sichtbar), dann rosa
    c = _mix(SCHWARZ, SCHLEIM, lippe)
    c = _mix(c, FLEISCH, 0.35 * sst(2.5, 6.0, v))              # tiefer im Vorhof/am Zahnfleisch etwas dunkler
    return _mix(c, RACHEN, sst(0.66, 0.92, s))                 # hinten Rachen


def flecken_malen(kl):
    def fleck_malen(fl, farbe):
        """Malt einen Fleck (Bildpixel von oben) samt 4 px Saum in kl; farbe(s, t) -> (h, w, 3) sRGB 0..1."""
        x0, y0, w, h = fl
        ys = np.arange(y0 - 4, y0 + h + 4)
        xs = np.arange(x0 - 4, x0 + w + 4)
        s = (xs + 0.5 - (x0 + 2.0)) / (w - 4.0)
        t = (ys + 0.5 - (y0 + 2.0)) / (h - 4.0)
        S_, T_ = np.meshgrid(np.clip(s, 0, 1), np.clip(t, 0, 1))
        kl[(TEX_R - 1 - ys)[:, None], xs[None, :], :3] = farbe(S_, T_)

    def oben(s, t):
        wand = _wand(s, t / ZEILE_WAND * V_WAND)
        tp = np.clip((t - ZEILE_WAND - 0.03) / (0.97 - ZEILE_WAND), 0.0, 1.0)     # 0 vorn .. 1 hinten
        X = GAUMEN_X[0] - tp * (GAUMEN_X[0] - GAUMEN_X[1])
        Y = s * 14.0 - 7.0
        g = _c(152, 90, 104)
        rillen = np.maximum(np.cos(2 * math.pi * (X - 6.0) / 1.15), 0.0) ** 2 * sst(-2.6, -0.5, X)     # 8 Querrillen vorn
        rillen *= 1.0 - sst(2.8, 3.8, np.abs(Y))
        naht = np.exp(-(Y / 0.18) ** 2) * sst(-2.0, 0.0, X)
        g = g * (1.0 + 0.16 * rillen + 0.08 * naht)[..., None]
        g = _mix(g, FLEISCH, sst(3.6, 4.8, np.abs(Y)))           # Zahnfleisch am Rand
        g = _mix(g, RACHEN, 1.0 - sst(-5.6, -3.0, X))          # hinten Rachen
        return np.where((t < ZEILE_WAND + 0.015)[..., None], wand, g)

    def unten(s, t):
        wand = _wand(s, t / ZEILE_WAND * V_WAND)
        wand = _mix(wand, _c(140, 78, 96), 0.4 * sst(4.0, 7.5, t / ZEILE_WAND * V_WAND) * (1.0 - sst(0.66, 0.92, s)))
        tp = np.clip((t - ZEILE_WAND - 0.03) / (0.97 - ZEILE_WAND), 0.0, 1.0)
        X = ZUNGE_X[0] - tp * (ZUNGE_X[0] - ZUNGE_X[1])
        Y = s * 8.0 - 4.0
        z = _c(192, 112, 124)
        z = _mix(z, _c(204, 124, 132), sst(3.5, 5.3, X))          # Spitze heller
        z = z * (1.0 - 0.18 * np.exp(-(Y / 0.32) ** 2) * sst(-3.5, 3.5, X))[..., None]      # Mittelrinne
        z = z * (1.0 - 0.12 * sst(2.2, 3.4, np.abs(Y)))[..., None]                        # Raender
        pap = 1.0 + 0.04 * np.sin(X * 23.0) * np.sin(Y * 19.0)
        z = z * pap[..., None]
        z = _mix(z, _c(120, 62, 72), 1.0 - sst(-4.6, -2.0, X))     # Zungengrund dunkler
        return np.where((t < ZEILE_WAND + 0.015)[..., None], wand, z)

    def zahn(s, t):
        hals, spitze, fleisch = _c(190, 170, 120), _c(235, 228, 210), _c(112, 62, 68)
        c = _mix(hals, spitze, sst(0.3, 0.95, t))
        c = _mix(c, _c(208, 192, 150), (s > 0.66) * 0.5)          # Backenzaehne gelblicher
        return _mix(c, fleisch, 1.0 - sst(0.12, 0.27, t))

    fleck_malen(FLECK_GAUMEN, oben)
    fleck_malen(FLECK_ZUNGE, unten)
    fleck_malen(FLECK_ZAHN, zahn)
