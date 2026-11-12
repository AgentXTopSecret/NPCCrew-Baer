# Lauf baer-junges-fuss (12.11.2026), Bauer TEXTUR: NCBearCub.png (1024 x 1024 RGB) fuer das alte Junge mit Baerenfuessen/-beinen vom 2c.
# Kevin (ENTSCHEIDUNGEN.md, 11.11.): "genau das gesicht muss so bleiben das wirkt suess" -> Start ist die heutige PNG (2ee25f24); neu
# geschrieben werden NUR (a) das Koerper-Rechteck (Pixelmitte u < 0,62 und v < 0,62) und (b) der Hals-Streifen (ATLAS hals, v 0,78-0,885).
# Alle anderen Texel (Gesicht, Kopf, Ohren, Kiefer, deren Polster) bleiben byte-gleich (Selbstpruefung am Ende, sonst Abbruch).
# (a) Koerper: 2c-Fell (quelle/2c/NCBear_body1024.png, 4cfdb177) linear ins Rechteck wie die Koerper-UV des Netzes (FORM: 2c-Dump-UV mit
#     in_rect(ATLAS koerper, gleich=False), Polster 4 px), gefiltert mit Lanczos-3 (Verkleinerung 1024 -> 626,88 px, keine Treppen).
#     Fellfarbe auf das heutige Junge gezogen: Faktor je Kanal = geglaettetes Fell heute / geglaettetes 2c-Fell an derselben 3D-Stelle
#     (Ruhe des Jungen, Gauss SIGMA_M; heute ohne graue Menschen-Sohle) -> grosse Farbverlaeufe wie heute, Straehnen und Sohlen vom 2c.
#     Leder (Hinter-/Vordersohle mit Ballen; 2c-Leder-Maske quelle/2c_sohle) und Krallen behalten die 2c-Farbe; Vordersohle optional
#     dunkler (VORN_LEDER). Ungenutzte Texel im Rechteck (2c-Kopfinseln) werden aus dem Fell aufgefuellt (keine fremden Farben in den
#     Mip-Stufen). Krallen (UV fast Punkt) und der Unterarm-Streifen bekommen ihr 2x2-Lesefeld (1024 und 512 = 4x4) fest gesetzt.
# (b) Hals: die Hals-Routine von baer_textur_baby.py (main :434-455) wortgleich, mit den Straehnen-SAATEN von heute (fix1-Netz), damit das
#     Hals-Ende am festen Kopf (Lochrand) genau wie heute weiterlaeuft; Rand-Farbe = neuer Koerper. Polster im Streifen wie baby :504-518.
# Selbsttest (--selbsttest): dieselbe Rechnung mit dem HEUTIGEN Netz und Koerper liefert die heutige PNG (Kopf exakt, Hals +-1).
# Quellen nur aus _arbeit/baer_junges_fuss/quelle (MD5 geprueft); Originale baer_textur_baby.py / baer_form_baby.py nur importiert.
# Aufruf: python baer_textur_jfuss.py NETZ.npz AUS.png [--log LOG.json] [--selbsttest]
# Statisch/offline, nicht gespielt.
import hashlib
import json
import math
import pickle
import sys
import time

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_form_baby as bf  # noqa: E402  (nur Funktionen auge_lage, nase, kopf_feld)
import baer_textur_baby as bt  # noqa: E402  (nur Funktionen; main wird NICHT aufgerufen)

ARB = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges_fuss/"
Q = ARB + "quelle/"
QUELLEN = {   # Datei -> MD5 (quelle/md5_quelle.txt, md5_form.txt, md5_textur.txt)
    "cub/NCBearCub.png": "2ee25f24c4f0f05bfbb955d4d4b17aea",
    "2c/NCBear_body1024.png": "4cfdb177784758fc53eacd07a8319f45",
    "baby_netz/fix1.npz": None,           # MD5 aus md5_form.txt
    "2c_sohle/sohle_2c_2048.npz": None,   # MD5 aus md5_textur.txt
}
NAMEN_DUMP = ARB + "plan/dump/dump_2c.txt.pkl"     # nur Knochennamen (Reihenfolge = Bi-Indizes)
GR = 1024
POL = 4.0 / 1024
M2U = 0.544
RECHT = 635                 # Pixel 0..634 je Achse: Pixelmitte < 0,62 (wie in_k in baer_textur_baby.py :264)
SIGMA_M = 0.06              # Glaettung des Farbfeldes (m, Ruhe des Jungen)
ZELLE_M = 0.02              # Gitter dafuer
LEDER_HART = 0.30           # ab diesem Leder-Gewicht zaehlt ein 2c-Texel nicht zum Fell (Farbfeld)
VORN_LEDER = 0.55           # Vordersohle dunkler (2c dort hellgrau ~(120,111,98)): Farbton der Hintersohle, Luma x 0,55; None = wie 2c
GEWINN_GRENZE = (0.45, 1.60)
KLASSEN = True              # Farbfeld je Normalen-Klasse (unten / seitlich / oben)
STREIFEN = (799, 906)       # Zeilen des Hals-Streifens (Pixelmitte v in [0,78; 0,885))
LUMA = np.array((0.299, 0.587, 0.114))


def log(*a):
    print(*a, flush=True)


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def quellen_pruefen():
    soll = dict(QUELLEN)
    for f in ("md5_form.txt", "md5_textur.txt"):
        for z in open(Q + f):
            z = z.strip()
            if z and not z.startswith("#"):
                h, n = z.split()[:2]
                n = n.lstrip("*")
                if n in soll and soll[n] is None:
                    soll[n] = h
    ist = {}
    for n, h in soll.items():
        ist[n] = md5(Q + n)
        assert h is not None and ist[n] == h, "Quelle %s: MD5 %s statt %s" % (n, ist[n], h)
    return ist


def tier(P):
    P = np.asarray(P, float)
    return np.stack((-P[..., 2], P[..., 0], P[..., 1]), -1) / M2U


def bild_laden(p):
    return np.asarray(Image.open(p).convert("RGB"), float)


# ------------------------------------------------------------------ Lanczos-3 (Verkleinern mit Filter) ----------------------------
def lanczos(x, a=3):
    x = np.asarray(x, float)
    out = np.sinc(x) * np.sinc(x / a)
    return np.where(np.abs(x) < a, out, 0.0)


def resample_matrix(n_src, n_dst, off_px, skala, a=3):
    """Zielpixel j (Mitte j+0,5) liegt in der Quelle bei (j + 0,5 - off_px) * skala (Kanten-Koordinate). Filterbreite skala (Verkleinern),
    Rand geklemmt (wie np.clip in baer_textur_baby.py :267). Zeilensumme 1."""
    W = np.zeros((n_dst, n_src))
    f = max(skala, 1.0)
    for j in range(n_dst):
        c = (j + 0.5 - off_px) * skala - 0.5
        i0, i1 = int(math.floor(c - a * f)), int(math.ceil(c + a * f))
        ii = np.arange(i0, i1 + 1)
        w = lanczos((ii - c) / f, a)
        np.add.at(W[j], np.clip(ii, 0, n_src - 1), w)
    return W / W.sum(1, keepdims=True)


def ins_rechteck(img, n_src):
    """Quelle (n_src x n_src, UV 0..1) -> Rechteck RECHT x RECHT; UV-Abbildung = in_rect(..., ATLAS koerper, gleich=False)."""
    skala = n_src / ((0.62 - 2 * POL) * GR)
    W = resample_matrix(n_src, RECHT, POL * GR, skala)
    if img.ndim == 2:
        return W @ img @ W.T
    return np.stack([W @ img[..., k] @ W.T for k in range(img.shape[2])], -1)


# ------------------------------------------------------------------ Rasterung Koerper ---------------------------------------------
def koerper_raster(N):
    """Koerper-Dreiecke (teil 0) im UV: je Texel Lage (tier, m) und Normale (aussen); Dreieck-Index -1 = leer."""
    t, F = N["teil"], N["F"]
    P = tier(N["P"])
    Nv = bt.normalen(P, F)
    sel = (t[F] == 0).all(1)
    iX, iN, iI = bt.rastern(N["UV"] * GR, P, Nv, F, sel)
    m = iI >= 0
    nn = iN[m] / np.maximum(np.linalg.norm(iN[m], axis=1), 1e-9)[:, None]
    # tier = (-z, x, y) ist eine Spiegelung (Det -1): Umlaufsinn-Normalen zeigen dann nach innen -> pruefen und drehen
    z = iX[m][:, 2]
    oben = z > np.percentile(z, 98)
    if nn[oben, 2].mean() < 0:
        nn = -nn
    return m, iX[m], nn, iI[m]


# ------------------------------------------------------------------ Geglaettetes Farbfeld in 3D -----------------------------------
class Feld:
    """Trilinear ins Gitter gestreut, Gauss (getrennt je Achse) geglaettet; liefert gewichtetes Mittel (log-Farbe) an beliebigen Punkten."""

    def __init__(self, lo, hi, zelle=None, sigma=None):
        zelle = ZELLE_M if zelle is None else zelle
        sigma = SIGMA_M if sigma is None else sigma
        self.lo = np.asarray(lo, float) - 4 * sigma
        self.z = zelle
        self.shape = tuple(int(math.ceil(v)) + 2 for v in (np.asarray(hi, float) + 4 * sigma - self.lo) / zelle)
        self.sig = sigma / zelle

    def _ecken(self, P):
        g = (P - self.lo) / self.z
        i0 = np.floor(g).astype(np.int64)
        f = g - i0
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    w = (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                    idx = np.ravel_multi_index((i0[:, 0] + dx, i0[:, 1] + dy, i0[:, 2] + dz), self.shape)
                    yield idx, w

    def _blur(self, A):
        r = int(math.ceil(3 * self.sig))
        k = np.exp(-0.5 * (np.arange(-r, r + 1) / self.sig) ** 2)
        k /= k.sum()
        for ax in range(3):
            pad = [(0, 0)] * 3
            pad[ax] = (r, r)
            Ap = np.pad(A, pad)
            out = np.zeros_like(A)
            n = A.shape[ax]
            for o, kk in enumerate(k):
                sl = [slice(None)] * 3
                sl[ax] = slice(o, o + n)
                out += kk * Ap[tuple(sl)]
            A = out
        return A

    def setzen(self, P, werte, gew=None):
        n = int(np.prod(self.shape))
        S = np.zeros((werte.shape[1], n))
        W = np.zeros(n)
        g = np.ones(len(P)) if gew is None else gew
        for idx, w in self._ecken(P):
            W += np.bincount(idx, w * g, n)
            for k in range(werte.shape[1]):
                S[k] += np.bincount(idx, w * g * werte[:, k], n)
        self.W = self._blur(W.reshape(self.shape))
        self.S = [self._blur(s.reshape(self.shape)) for s in S]
        self.mittel = (werte.mean(0))

    def lesen(self, P):
        w = np.zeros(len(P))
        s = np.zeros((len(P), len(self.S)))
        Wf = self.W.ravel()
        Sf = [x.ravel() for x in self.S]
        for idx, ww in self._ecken(P):
            w += ww * Wf[idx]
            for k in range(len(Sf)):
                s[:, k] += ww * Sf[k][idx]
        return s, w


# ------------------------------------------------------------------ Kopf/Hals-Rechnung (Kopie baer_textur_baby.main) -------------
def saaten(X, F, Nv, tnam_f, gruppe_f, P, L=0.05, abstand=0.0085, spitzen=0.13, seed=21):
    """Erster Teil von bt.straehnen (:191-206) wortgleich: Saat-Punkte, Richtung, Staerke, Spitzen (gleiche Zufallsfolge)."""
    rng = np.random.default_rng(seed)
    A = X[F]
    fa = 0.5 * np.linalg.norm(np.cross(A[:, 1] - A[:, 0], A[:, 2] - A[:, 0]), axis=1)
    n_s = int(fa.sum() / abstand ** 2)
    t = rng.choice(len(F), n_s, p=fa / fa.sum())
    r1, r2 = rng.random(n_s), rng.random(n_s)
    sq = np.sqrt(r1)
    C = (1 - sq)[:, None] * A[t, 0] + (sq * (1 - r2))[:, None] * A[t, 1] + (sq * r2)[:, None] * A[t, 2]
    Cn = Nv[F[t, 0]] + Nv[F[t, 1]] + Nv[F[t, 2]]
    Cn /= np.maximum(np.linalg.norm(Cn, axis=1), 1e-9)[:, None]
    Cf = bt.tangential(bt.haarstrich(C, tnam_f[t], P), Cn)
    Cg = gruppe_f[t]
    amp = rng.normal(0.0, 1.0, n_s)
    tip = rng.random(n_s) < spitzen
    bary = np.stack((1 - sq, sq * (1 - r2), sq * r2), 1)
    return dict(C=C, Cn=Cn, Cf=Cf, Cg=Cg, amp=amp, tip=tip, n_s=n_s, L=L, ecken=F[t], bary=bary, tnam=tnam_f[t])


def saaten_uebertragen(Sd, H, N, KN):
    """Saaten von heute auf das neue Netz: Saaten auf U/J/Ol/Or bleiben (Kopf bit-gleich); Saaten auf dem Hals H wandern mit ihren
    Ecken (gleicher Punkt-Index im Hals-Loft, Lage/Normale des neuen Netzes, gleiche baryzentrische Lage) -> die Straehnen liegen wieder
    auf der neuen Halsflaeche, am festen Lochrand (Kopien bit-gleich) genau wie heute. Richtung neu tangential (Haarstrich Hals)."""
    th, tn_ = H["teil"], N["teil"]
    oh, on = np.where(th == 3)[0], np.where(tn_ == 3)[0]
    assert len(oh) == len(on)
    lok = -np.ones(len(th), int)
    lok[oh] = np.arange(len(oh))
    E = Sd["ecken"]
    hs = (th[E] == 3).all(1)
    assert ((th[E] == 3).any(1) == hs).all(), "Saat-Dreieck gemischt"
    neu = dict(Sd)
    Xn = KN["X"]
    En = on[lok[E[hs]]]
    C = Sd["C"].copy()
    Cn = Sd["Cn"].copy()
    Cf = Sd["Cf"].copy()
    C[hs] = (Sd["bary"][hs][:, :, None] * Xn[En]).sum(1)
    c_ = KN["Nn"][En].sum(1)
    Cn[hs] = c_ / np.maximum(np.linalg.norm(c_, axis=1), 1e-9)[:, None]
    Cf[hs] = bt.tangential(bt.haarstrich(C[hs], Sd["tnam"][hs], KN["P"]), Cn[hs])
    neu.update(C=C, Cn=Cn, Cf=Cf, hals_saaten=int(hs.sum()))
    return neu


def straehnen_werten(Pm, Nm, gruppe_t, Sd, breite=0.0028):
    """Zweiter Teil von bt.straehnen (:205-231) wortgleich: Summe aller Straehnen je Texel."""
    C, Cn, Cf, Cg, amp, tip, L = Sd["C"], Sd["Cn"], Sd["Cf"], Sd["Cg"], Sd["amp"], Sd["tip"], Sd["L"]
    g = L / 2
    key = np.floor(C / g).astype(np.int64)
    kc = (key[:, 0] * 73856093) ^ (key[:, 1] * 19349663) ^ (key[:, 2] * 83492791)
    o = np.argsort(kc)
    kc_s = kc[o]
    S = np.zeros(len(Pm))
    T = np.zeros(len(Pm))
    kt = np.floor(Pm / g).astype(np.int64)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                kk = ((kt[:, 0] + dx) * 73856093) ^ ((kt[:, 1] + dy) * 19349663) ^ ((kt[:, 2] + dz) * 83492791)
                a0 = np.searchsorted(kc_s, kk, "left")
                a1 = np.searchsorted(kc_s, kk, "right")
                cnt = a1 - a0
                for j in range(int(cnt.max()) if len(cnt) else 0):
                    w_ = np.where(cnt > j)[0]
                    si = o[a0[w_] + j]
                    d = Pm[w_] - C[si]
                    al = (d * Cf[si]).sum(1)
                    qu = np.linalg.norm(d - al[:, None] * Cf[si], axis=1)
                    u = al / g
                    ok = (np.abs(u) < 1) & (Cg[si] == gruppe_t[w_]) & ((Nm[w_] * Cn[si]).sum(1) > 0.3)
                    prof = np.exp(-(qu / breite) ** 2) * (1 - u ** 2) ** 2 * ok
                    S[w_] += amp[si] * prof * ~tip[si]
                    T[w_] += np.exp(-(qu / (0.7 * breite)) ** 2) * (1 - u ** 2) ** 2 * ok * tip[si] * np.clip((u - 0.2) / 0.5, 0, 1)
    return S, T


def kopf_vorbereiten(N):
    """bt.main :247-258 + Saat-Eingaben (:302-309)."""
    P = json.loads(str(N["param"]))
    teil = N["teil"]
    tn = list(N["teil_namen"])
    F = N["F"]
    X = np.nan_to_num(N["kopfX"])
    kopf_t = teil > 0
    Nn = bt.normalen(np.where(kopf_t[:, None], X, 0.0), F)
    sel = kopf_t[F].all(1)
    gname = {"U": 0, "J": 0, "H": 0, "Ol": 1, "Or": 2}
    tnam_all = np.array([tn[k] for k in teil])
    Fh = F[sel]
    gruppe_f = np.array([gname[tn[k]] for k in teil[Fh[:, 0]]])
    return dict(P=P, X=X, Nn=Nn, sel=sel, Fh=Fh, tnam_f=tnam_all[Fh[:, 0]], gruppe_f=gruppe_f, gname=gname)


def kopf_rechnung(N, kimg, Sd):
    """Kopie von bt.main :247-518 mit drei Aenderungen: (1) das Koerper-Bild kommt herein (kimg, float, gueltig im Rechteck) statt aus
    TEX_ALT; (2) die Straehnen-Saaten Sd kommen herein (heute: Saaten des fix1-Netzes); (3) Rueckgabe des float-Bildes (ganz, mit Polster)
    und der Kopf-Maske statt einer Datei. Alles andere wortgleich (Zeilennummern in Klammern)."""
    KV = kopf_vorbereiten(N)
    P = KV["P"]
    atlas = json.loads(str(N["atlas"]))
    teil = N["teil"]
    tn = list(N["teil_namen"])
    karte = N["karte"]
    F = N["F"]
    X = KV["X"]
    UVp = N["UV"] * GR
    Nn = KV["Nn"]
    sel = KV["sel"]
    img = np.zeros((GR, GR, 3))
    u0, v0, u1, v1 = atlas["koerper"]
    jj, ii = np.meshgrid(np.arange(GR), np.arange(GR))
    in_k = ((jj + 0.5) / GR < u1) & ((ii + 0.5) / GR < v1)                       # (:264)
    img[in_k] = kimg[in_k]                                                       # (1)
    kb = teil == 0                                                               # (:275-278)
    uvk = N["UV"][kb]
    pk = (uvk * GR).astype(int).clip(0, GR - 1)
    kfarbe = img[pk[:, 1], pk[:, 0]]
    iX, iN, iI = bt.rastern(UVp, X, Nn, F, sel)                                  # (:280-289)
    m = iI >= 0
    Pm = iX[m]
    Nm = iN[m]
    Nm /= np.maximum(np.linalg.norm(Nm, axis=1), 1e-9)[:, None]
    tri = iI[m]
    tteil = np.array([tn[k] for k in teil[F[tri, 0]]])
    tkarte = karte[F[tri, 0]]
    x, y, z = Pm[:, 0], Pm[:, 1], Pm[:, 2]
    ay = np.abs(y)
    gname = KV["gname"]                                                          # (:303-310) mit (2)
    l1, l2 = straehnen_werten(Pm, Nm, np.array([gname[k] for k in tteil]), Sd)
    gross = bt.rauschen(Pm, 9.0, 7)                                              # (:332-334)
    n_mid = np.argsort(np.argsort(l1 + 0.10 * (gross - 0.5))) / max(len(l1) - 1, 1)
    n_hi = np.argsort(np.argsort(l2 + 0.6 * (l1 - l1.mean()))) / max(len(l2) - 1, 1)
    W = {}                                                                       # (:336-420)
    W["gesicht"] = np.ones(len(Pm))
    W["stirn_oben"] = bt.sst(0.14, 0.30, z) * bt.sst(-0.05, 0.1, -x - 0.0 + 0.1)
    W["wange"] = bt.sst(0.26, 0.40, ay) * bt.sst(-0.02, -0.12, z) * bt.sst(-0.55, -0.35, x)
    rho_aug = np.full(len(Pm), 9.0)
    unten_aug = np.zeros(len(Pm))
    an_l = []
    for i, s in enumerate((1.0, -1.0)):
        ac, an = bf.auge_lage(P, s)
        fl = np.array(P["au_flaeche"][i])
        up = np.array((0.0, 0.0, 1.0))
        t_ = np.cross(up, an)
        t_ /= np.linalg.norm(t_)
        u_ = np.cross(an, t_)
        d = Pm - fl
        r = np.sqrt(((d @ t_) / P["au_b"]) ** 2 + ((d @ u_) / P["au_h"]) ** 2)
        nah = r < rho_aug
        rho_aug = np.where(nah, r, rho_aug)
        unten_aug = np.where(nah, (d @ u_) / P["au_h"], unten_aug)
        an_l.append((np.array(P["au_ball"][i]), an))
    W["augenring"] = bt.sst(2.6, 1.6, rho_aug) * (rho_aug > 0.98)
    W["ueber_auge"] = bt.sst(3.6, 2.4, rho_aug) * bt.sst(0.6, 1.6, unten_aug) * (1 - W["augenring"])
    hb = np.interp(x, *P["sn_breite"])
    zo = np.interp(x, *P["sn_oben"])
    sn = bt.sst(0.0, 0.05, x) * bt.sst(1.12, 0.92, ay / hb) * bt.sst(zo + 0.035, zo - 0.005, z)
    zunge_hell = bt.sst(0.05, -0.02, x) * bt.sst(-0.06, 0.0, x) * bt.sst(0.07, 0.045, ay) * bt.sst(0.10, 0.04, z) * bt.sst(-0.04, -0.01, z)
    zunge_hell = np.maximum(zunge_hell, bt.sst(-0.08, 0.02, x) * bt.sst(0.06, 0.035, ay) * bt.sst(0.08, 0.03, z) * bt.sst(-0.03, 0.0, z))
    hell = np.clip(np.maximum(sn, zunge_hell) * (tteil != "H") * (tteil != "Ol") * (tteil != "Or"), 0, 1)
    seitlich = bt.sst(0.35, 0.8, ay / np.maximum(hb, 1e-3))
    W["schnauze_oben"] = hell * (1 - seitlich)
    W["schnauze_seite"] = hell * seitlich
    mlin = np.interp(x, *P["ma_linie"])
    jv = (tteil == "J")
    W["schnauze_seite"] = np.where(jv, bt.sst(mlin - 0.07, mlin - 0.02, z) * bt.sst(0.02, 0.08, x) * 0.8, W["schnauze_seite"])
    W["schnauze_oben"] = np.where(jv, 0.0, W["schnauze_oben"])
    dn = bf.nase(Pm, P)
    nasen = bt.sst(0.006, -0.002, dn)
    W["nase"] = nasen
    gaumen = (tteil == "U") & (x > P["ma_xh"] - 0.005) & (z < mlin - 0.002) & (Nm[:, 2] < -0.3)
    lippe = (tteil == "U") & (x > P["ma_xh"] - 0.01) & (np.abs(z - mlin) < 0.010) & (Nm[:, 2] > -0.3)
    zunge = jv & (Nm[:, 2] > 0.5) & (z > mlin - 0.02) & (x < 0.15)
    lippe_j = jv & (z > mlin - 0.035) & (x > 0.12) & ~zunge
    W["maul_innen"] = gaumen.astype(float) + (jv & (x < P["ma_xh"]) & (Nm[:, 2] > 0.2)).astype(float)
    W["zunge"] = zunge.astype(float)
    W["lippe"] = np.maximum(lippe * bt.sst(0.010, 0.002, np.abs(z - mlin)), lippe_j.astype(float))
    auf_ball = np.zeros(len(Pm), bool)
    glanz = np.zeros(len(Pm))
    for mz, an in an_l:
        d = np.linalg.norm(Pm - mz, axis=1)
        ab = np.abs(d - P["au_ball_r"]) < 0.0025
        auf_ball |= ab
        hn = an + np.array((0.0, 0.0, 0.24))
        hn /= np.linalg.norm(hn)
        gp = mz + hn * P["au_ball_r"]
        glanz = np.maximum(glanz, bt.sst(0.0075, 0.0035, np.linalg.norm(Pm - gp, axis=1)) * ab)
    loch = (rho_aug < 1.02) & ~auf_ball & (tteil == "U")
    W["iris"] = auf_ball.astype(float) + loch.astype(float)
    W["unterlid"] = (bt.sst(0.99, 1.03, rho_aug) * bt.sst(1.22, 1.12, rho_aug) * bt.sst(-0.35, -0.75, unten_aug)).astype(float)
    on = np.array(P["ohr_n"], float)
    on /= np.linalg.norm(on)
    ohr = np.isin(tteil, ("Ol", "Or"))
    r_ohr = np.zeros(len(Pm))
    h_ohr = np.zeros(len(Pm))
    for s, nm in ((1.0, "Ol"), (-1.0, "Or")):
        c = np.array(P["ohr_c"]) * (1, s, 1)
        nn = on * (1, s, 1)
        mm = tteil == nm
        d = Pm[mm] - c
        h_ohr[mm] = d @ nn
        r_ohr[mm] = np.linalg.norm(d - np.outer(d @ nn, nn), axis=1)
    R = P["ohr_d"] / 2
    mr = P.get("ohr_mulde_r", 0.6) * R
    vorn = np.char.endswith(tkarte.astype(str), "vorn")
    W["ohr_mulde"] = ohr * vorn * bt.sst(mr * 0.62, mr * 0.38, r_ohr)
    W["ohr_haar"] = ohr * vorn * bt.sst(mr * 0.35, mr * 0.65, r_ohr) * bt.sst(mr * 1.15, mr * 0.95, r_ohr)
    W["ohr_rand"] = ohr * vorn * bt.sst(mr * 1.0, R * 0.9, r_ohr) * (1 - W["ohr_mulde"]) * 0.35
    farbe = bt.fell(Pm, bt.ZIEL["gesicht"], n_mid, n_hi, 0.13)                 # (:422-433)
    hk = (bt.sst(-0.28, -0.50, x) * (tteil == "U"))[:, None]
    farbe = farbe * (1 - hk) + bt.fell(Pm, (86, 62, 48), n_mid, n_hi, 0.13) * hk
    for zn in ("stirn_oben", "wange", "augenring", "ueber_auge", "schnauze_seite", "schnauze_oben"):
        sp = 0.13 if zn in ("stirn_oben", "wange") else 0.06
        c = bt.fell(Pm, bt.ZIEL[zn], n_mid, n_hi, sp)
        if zn.startswith("schnauze"):
            c = np.array(bt.ZIEL[zn], float)[None, :] * (0.86 + 0.28 * n_mid)[:, None]
            lichter = bt.rauschen(Pm, 120.0, 7) > 0.86
            c[lichter] = c[lichter] * 0.4 + np.array((190.0, 160.0, 140.0)) * 0.6
        farbe = farbe * (1 - W[zn][:, None]) + c * W[zn][:, None]
    hals = tteil == "H"                                                          # (:435-455) Hals-Routine
    vfr = None
    if hals.any():
        ah = atlas["hals"]
        pix = np.argwhere(m)[hals]
        vfr = ((pix[:, 0] + 0.5) / GR - (ah[1] + POL)) / (ah[3] - ah[1] - 2 * POL)
        rf = np.zeros((hals.sum(), 3))
        Ph = N["P"][F[tri[hals], 0]]
        kP = N["P"][kb]
        for j0 in range(0, len(Ph), 4000):
            dd = np.linalg.norm(Ph[j0:j0 + 4000, None, :] - kP[None, ::3, :], axis=2)
            nn_ = np.argsort(dd, axis=1)[:, :6]
            rf[j0:j0 + 4000] = kfarbe[::3][nn_].mean(1)
        kopfc = farbe[hals].copy()
        u_ = np.clip(n_mid[hals], 1e-4, 1 - 1e-4)
        koerc = rf * (1.0 + bt.FELL_AMP * np.clip(np.log(u_ / (1 - u_)) / 1.7, -2.5, 2.5))[:, None]
        sp_ = n_hi[hals] > 0.90
        koerc[sp_] = koerc[sp_] * 0.55 + np.array(bt.SPITZE[0], float) * 0.45
        b = bt.sst(0.10, 0.80, vfr)[:, None]
        farbe[hals] = koerc * (1 - b) + kopfc * b
    for zn in ("ohr_rand", "ohr_haar", "ohr_mulde"):                             # (:457-479)
        c = np.array(bt.ZIEL[zn], float)[None, :] * (0.8 + 0.4 * n_mid)[:, None]
        if zn == "ohr_haar":
            c = c * (0.80 + 0.30 * (n_hi > 0.5))[:, None]
        farbe = farbe * (1 - W[zn][:, None]) + c * W[zn][:, None]
    for zn in ("unterlid", "lippe", "maul_innen", "zunge", "nase", "iris"):
        c = np.array(bt.ZIEL[zn], float)[None, :] * (0.9 + 0.2 * n_mid)[:, None]
        if zn == "nase":
            c = c * 0.72
            ca = np.array(P["na_c"])
            oben = bt.sst(ca[2] + P["na_h"][2] - 0.022, ca[2] + P["na_h"][2] - 0.004, z)
            c = c * (1 - oben[:, None]) + np.array((110.0, 105.0, 108.0))[None, :] * oben[:, None]
            gl = bt.sst(0.022, 0.008, np.linalg.norm((Pm - (ca + (P["na_h"][0], 0.0, P["na_h"][2] * 0.45))) / (1.0, 1.6, 1.0), axis=1))
            c = c * (1 - gl[:, None]) + np.array((150.0, 145.0, 150.0))[None, :] * gl[:, None]
            for s in (1.0, -1.0):
                nl = np.linalg.norm((Pm - (ca[0] + P["na_h"][0], s * P["na_loch_y"], ca[2] - P["na_loch_dz"])) / (1.0, 1.25, 0.8), axis=1)
                lo = bt.sst(0.020, 0.010, nl)
                c = c * (1 - lo[:, None]) + np.array((6.0, 3.0, 3.0))[None, :] * lo[:, None]
        if zn == "iris":
            c = c * (1 - glanz[:, None]) + np.array((225.0, 230.0, 240.0))[None, :] * glanz[:, None]
            c = np.where(loch[:, None], np.array((24.0, 19.0, 17.0))[None, :], c)
        farbe = farbe * (1 - W[zn][:, None]) + c * W[zn][:, None]
    ao = np.ones(len(Pm))                                                        # (:481-491)
    gemalt = np.zeros(len(Pm))
    for zn in ("unterlid", "iris", "nase", "maul_innen", "zunge", "lippe", "ueber_auge"):
        gemalt = np.maximum(gemalt, W[zn])
    kk = ~hals & ~ohr & (gemalt < 0.5)
    for dist, gw in ((0.012, 0.5), (0.03, 0.5)):
        f = bf.kopf_feld(Pm[kk] + Nm[kk] * dist, P)
        ao[kk] -= gw * (1 - np.clip(f / dist, 0, 1)) * 0.30
    farbe = farbe * np.clip(ao, 0.62, 1)[:, None]
    img[m] = farbe
    voll = m | in_k                                                              # (:505-518) Polster
    for _ in range(10):
        leer = ~voll
        acc = np.zeros_like(img)
        cnt = np.zeros((GR, GR))
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            sh = np.roll(np.roll(img, dy, 0), dx, 1)
            sv_ = np.roll(np.roll(voll, dy, 0), dx, 1)
            acc += sh * sv_[..., None]
            cnt += sv_
        neu = leer & (cnt > 0)
        img[neu] = acc[neu] / cnt[neu][:, None]
        voll = voll | neu
    img[~voll] = np.array(bt.ZIEL["gesicht"], float)
    hals_pix = np.zeros((GR, GR), bool)
    hals_pix[tuple(np.argwhere(m)[hals].T)] = True
    return dict(img=img, m=m, hals_pix=hals_pix, in_k=in_k, n_kopf=int(m.sum()), n_hals=int(hals.sum()), l1=l1)


# ------------------------------------------------------------------ Koerper -------------------------------------------------------
def leder_karte():
    """2c-Leder-Gewicht (Hinter-/Vordersohle) als 2048er-Bild (Zeile 0 oben), dann wie das Fell ins Rechteck."""
    Z = np.load(Q + "2c_sohle/sohle_2c_2048.npz")
    L = {}
    for s in ("HL", "HR", "VL", "VR"):
        A = np.zeros((2048, 2048))
        A[2047 - Z[s + "_y"].astype(int), Z[s + "_x"].astype(int)] = Z[s + "_leder"]
        L[s] = np.clip(ins_rechteck(A, 2048), 0.0, 1.0)
    return L


def fuellen(img, voll, runden=400):
    """Leere Texel aus den Nachbarn (8er, gemittelt) Runde fuer Runde fuellen, bis alles voll ist (wie das Polster in bt.main)."""
    img = img.copy()
    voll = voll.copy()
    for r in range(runden):
        if voll.all():
            break
        acc = np.zeros_like(img)
        cnt = np.zeros(voll.shape)
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            vs = np.zeros_like(voll)
            sh = np.zeros_like(img)
            ys = slice(max(dy, 0), voll.shape[0] + min(dy, 0))
            yd = slice(max(-dy, 0), voll.shape[0] + min(-dy, 0))
            xs = slice(max(dx, 0), voll.shape[1] + min(dx, 0))
            xd = slice(max(-dx, 0), voll.shape[1] + min(-dx, 0))
            vs[ys, xs] = voll[yd, xd]
            sh[ys, xs] = img[yd, xd]
            acc += sh * vs[..., None]
            cnt += vs
        neu = ~voll & (cnt > 0)
        img[neu] = acc[neu] / cnt[neu][:, None]
        voll |= neu
    return img, r


def krallen_schalen(N, names):
    """Koerper-Dreiecke mit fast punktfoermiger UV (Dichte < 2 % des Medians): Krallen-Schalen und der Unterarm-Streifen (2c-Netz)."""
    t, F = N["teil"], N["F"]
    P = tier(N["P"])
    UV = N["UV"] * GR
    Fk = F[(t[F] == 0).all(1)]
    A3 = 0.5 * np.linalg.norm(np.cross(P[Fk[:, 1]] - P[Fk[:, 0]], P[Fk[:, 2]] - P[Fk[:, 0]]), axis=1)
    u = UV
    A2 = 0.5 * np.abs((u[Fk[:, 1], 0] - u[Fk[:, 0], 0]) * (u[Fk[:, 2], 1] - u[Fk[:, 0], 1]) - (u[Fk[:, 2], 0] - u[Fk[:, 0], 0]) * (u[Fk[:, 1], 1] - u[Fk[:, 0], 1]))
    r = A2 / np.maximum(A3, 1e-12)
    K = Fk[r < 0.02 * np.median(r)]
    par = np.arange(len(P))

    def w(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for tr in K:
        r0 = w(tr[0])
        for v in tr[1:]:
            r1 = w(v)
            if r1 != r0:
                par[r1] = r0
    vs = np.unique(K.ravel())
    wur = np.array([w(v) for v in vs])
    dom = N["Bi"][np.arange(len(N["Bi"])), N["Wt"].argmax(1)]
    out = []
    for s in np.unique(wur):
        mv = vs[wur == s]
        kn = np.array(names)[dom[mv]]
        art = "kralle" if np.isin(kn, ("Bip01_L_Foot", "Bip01_R_Foot", "Bip01_L_Hand", "Bip01_R_Hand", "Bip01_L_Toe0", "Bip01_R_Toe0")).all() and P[mv, 2].max() < 0.12 else "streifen"
        out.append(dict(v=mv, art=art, vorn=bool(P[mv, 0].mean() > 0), uv=UV[mv].mean(0), uvq=N["uv_quelle"][mv].mean(0), P=P[mv].mean(0)))
    return out


def lesefeld(uv_px):
    """Texel, die das Spiel fuer einen UV-Punkt liest: bilinear 2x2 in 1024 und in der 512er-Mip-Stufe (= 4x4 in 1024)."""
    ux, uy = uv_px
    pts = set()
    for res, f in ((GR, 1), (GR // 2, 2)):
        x0 = int(math.floor(ux / f - 0.5))
        y0 = int(math.floor(uy / f - 0.5))
        for dx in (0, 1):
            for dy in (0, 1):
                for ex in range(f):
                    for ey in range(f):
                        pts.add((min(max((y0 + dy) * f + ey, 0), GR - 1), min(max((x0 + dx) * f + ex, 0), GR - 1)))
    return sorted(pts)


def bilinear(img, x, y):
    x = np.clip(x - 0.5, 0, img.shape[1] - 1.001)
    y = np.clip(y - 0.5, 0, img.shape[0] - 1.001)
    x0, y0 = int(x), int(y)
    fx, fy = x - x0, y - y0
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy) + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def klassen(nz):
    """Weiche Normalen-Klassen (unten, seitlich, oben) je Texel, Summe 1: Bauch mischt sich nicht mit den Beinseiten."""
    if not KLASSEN:
        return np.ones((len(nz), 1))
    u = bt.sst(-0.15, -0.65, nz)
    o = bt.sst(0.15, 0.65, nz)
    return np.stack((u, 1 - u - o, o), 1)


def zonen(X, Nn):
    z, x, nz, ny = X[:, 2], X[:, 0], Nn[:, 2], Nn[:, 1]
    return {"ruecken": (z > 0.60) & (nz > 0.5) & (x < 0.35) & (x > -0.60),
            "flanke": (z > 0.40) & (z < 0.75) & (np.abs(nz) < 0.4) & (np.abs(ny) > 0.6) & (x > -0.55) & (x < 0.30),
            "bauch": (z > 0.25) & (z < 0.55) & (nz < -0.5) & (x > -0.45) & (x < 0.30),
            "beine": (z > 0.04) & (z < 0.30)}


def koerper(N, heute_png, heute_netz, info):
    names = pickle.load(open(NAMEN_DUMP, "rb"))["names"]
    assert len(names) == 26
    # --- 2c-Fell ins Rechteck (Lanczos-3); Pruefung der Abbildung: UV = POL + uv_quelle * (0,62 - 2 POL)
    t = N["teil"]
    kb = t == 0
    uvq = N["uv_quelle"][kb]
    d_uv = np.abs(N["UV"][kb] - (POL + uvq * (0.62 - 2 * POL))).max()
    assert d_uv < 1e-9, "Koerper-UV ist nicht linear aus der 2c-UV: %g" % d_uv
    T2 = bild_laden(Q + "2c/NCBear_body1024.png")
    B = np.clip(ins_rechteck(T2, 1024), 0, 255)
    L = leder_karte()
    leder = np.maximum.reduce([L[s] for s in L])
    hinten_l = np.maximum(L["HL"], L["HR"])
    vorn_l = np.maximum(L["VL"], L["VR"])
    # --- Rasterung neu (Rechteck) und heute
    m_n, X_n, N_n, tri_n = koerper_raster(N)
    pix_n = np.argwhere(m_n)
    assert pix_n[:, 0].max() < RECHT and pix_n[:, 1].max() < RECHT
    m_h, X_h, N_h, _ = koerper_raster(heute_netz)
    c_h = heute_png[m_h]
    c_n = B[pix_n[:, 0], pix_n[:, 1]]
    l_n = leder[pix_n[:, 0], pix_n[:, 1]]
    # heute ohne Menschen-Sohle (grau, unten) und helle Krallen: Sohle = Unterseite tief oder graue Texel im Fussbereich
    z_h = X_h[:, 2]
    grau_h = (c_h[:, 0] - c_h[:, 2]) < 4
    weg_h = ((z_h < 0.08) & (N_h[:, 2] < -0.3)) | ((z_h < 0.16) & grau_h)
    fell_n = l_n < LEDER_HART
    info["heute_ohne_sohle"] = dict(texel=int(m_h.sum()), weg=int(weg_h.sum()), median_weg=np.median(c_h[weg_h], 0).round(1).tolist())
    # --- Farbfelder (log), je Normalen-Klasse (unten / seitlich / oben, weich), Faktor je Texel
    lo = np.minimum(X_h.min(0), X_n.min(0))
    hi = np.maximum(X_h.max(0), X_n.max(0))
    kA = klassen(N_h[:, 2])
    kB = klassen(N_n[:, 2])
    vA = np.log(np.maximum(c_h, 1.0))
    vB = np.log(np.maximum(c_n, 1.0))
    sA = np.zeros((len(X_n), 3))
    wA = np.zeros(len(X_n))
    sB = np.zeros((len(X_n), 3))
    wB = np.zeros(len(X_n))
    FAk = []
    for kl in range(kA.shape[1]):
        FA = Feld(lo, hi)
        FA.setzen(X_h[~weg_h], vA[~weg_h], kA[~weg_h, kl])
        FB = Feld(lo, hi)
        FB.setzen(X_n[fell_n], vB[fell_n], kB[fell_n, kl])
        s_, w_ = FA.lesen(X_n)
        sA += kB[:, kl:kl + 1] * s_
        wA += kB[:, kl] * w_
        s_, w_ = FB.lesen(X_n)
        sB += kB[:, kl:kl + 1] * s_
        wB += kB[:, kl] * w_
        FAk.append(FA)
    gA = vA[~weg_h].mean(0)
    gB = vB[fell_n].mean(0)
    eps = 1e-3 * max(np.median(wA), 1e-12)
    muA = (sA + eps * gA) / (wA + eps)[:, None]
    epsB = 1e-3 * max(np.median(wB), 1e-12)
    muB = (sB + epsB * gB) / (wB + epsB)[:, None]
    g = np.clip(np.exp(muA - muB), *GEWINN_GRENZE)
    info["faktor"] = dict(median=np.median(g, 0).round(3).tolist(), p5=np.percentile(g, 5, 0).round(3).tolist(),
                          p95=np.percentile(g, 95, 0).round(3).tolist(), global_=np.exp(gA - gB).round(3).tolist(),
                          geklemmt=int(((g <= GEWINN_GRENZE[0]) | (g >= GEWINN_GRENZE[1])).any(1).sum()))
    k = np.clip(l_n, 0, 1)[:, None]
    neu = c_n * g ** (1 - k)
    if VORN_LEDER is not None:
        vl = vorn_l[pix_n[:, 0], pix_n[:, 1]][:, None]
        h_med = np.median(c_n[(hinten_l[pix_n[:, 0], pix_n[:, 1]] > 0.9)], 0)
        ton = h_med / max(h_med @ LUMA, 1e-6)
        dunkel = ton[None, :] * (c_n @ LUMA)[:, None] * VORN_LEDER
        neu = neu * (1 - vl) + dunkel * vl
    R = np.zeros((RECHT, RECHT, 3))
    R[pix_n[:, 0], pix_n[:, 1]] = neu
    voll = np.zeros((RECHT, RECHT), bool)
    voll[pix_n[:, 0], pix_n[:, 1]] = True
    R, runden = fuellen(R, voll)
    info["aufgefuellt"] = dict(texel=int((~voll).sum()), runden=runden)
    # --- Krallen und Unterarm-Streifen: Lesefeld fest
    feste = []
    for s in krallen_schalen(N, names):
        if s["art"] == "kralle":
            c = bilinear(T2, s["uvq"][0] * 1024, s["uvq"][1] * 1024)     # 2c-Krallenfarbe (wie der grosse Baer zeigt)
        else:
            sa = np.zeros(3)
            wa = 0.0
            for F_ in FAk:                                                  # Fell heute an dieser Stelle (alle Klassen, geglaettet)
                s_, w_ = F_.lesen(s["P"][None, :])
                sa += s_[0]
                wa += w_[0]
            c = np.exp((sa + eps * gA) / (wa + eps))
        felder = [(y, x) for y, x in lesefeld(s["uv"]) if y < RECHT and x < RECHT]
        ueber = int(sum(voll[y, x] for y, x in felder))
        for y, x in felder:
            if not voll[y, x]:                  # nie ein Fell-Texel ueberschreiben (sonst Fleck auf einer Fell-Insel)
                R[y, x] = c
        feste.append(dict(art=s["art"], vorn=s["vorn"], punkte=int(len(s["v"])), uv_px=s["uv"].round(2).tolist(), soll=np.round(c, 1).tolist(),
                          texel=len(felder), davon_fell_texel_behalten=ueber))
    for f_, s in zip(feste, krallen_schalen(N, names)):
        f_["gelesen_1024"] = np.round(bilinear(R, s["uv"][0], s["uv"][1]), 1).tolist()   # was das Spiel in Mip 0 liest
    info["krallen"] = feste
    # --- Messung Zonen (heute gegen neu), Leder
    Zh = zonen(X_h, N_h)
    Zn = zonen(X_n, N_n)
    neu_px = R[pix_n[:, 0], pix_n[:, 1]]
    zi = {}
    for zn in Zh:
        a = np.median(c_h[Zh[zn] & ~weg_h], 0)
        b = np.median(neu_px[Zn[zn] & fell_n], 0)
        c0 = np.median(c_n[Zn[zn] & fell_n], 0)
        zi[zn] = dict(heute=a.round(1).tolist(), neu=b.round(1).tolist(), c2=c0.round(1).tolist(), abw=(b - a).round(1).tolist(),
                      n_heute=int((Zh[zn] & ~weg_h).sum()), n_neu=int((Zn[zn] & fell_n).sum()))
    info["zonen"] = zi
    lh = hinten_l[pix_n[:, 0], pix_n[:, 1]] > 0.9
    lv = vorn_l[pix_n[:, 0], pix_n[:, 1]] > 0.9
    info["leder"] = dict(hinten=np.median(neu_px[lh], 0).round(1).tolist(), vorn=np.median(neu_px[lv], 0).round(1).tolist(),
                         hinten_texel=int(lh.sum()), vorn_texel=int(lv.sum()))
    return R, dict(m_n=m_n, pix_n=pix_n, X_n=X_n, N_n=N_n, fell_n=fell_n, leder=leder, m_h=m_h, X_h=X_h, weg_h=weg_h)


# ------------------------------------------------------------------ Hauptablauf ---------------------------------------------------
def main(netz, aus, log_aus=None, selbsttest=False):
    t0 = time.time()
    info = dict(netz=netz, netz_md5=md5(netz), quellen=quellen_pruefen(),
                skripte={n: md5(r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/%s" % n) for n in ("baer_textur_baby.py", "baer_form_baby.py", "baer_textur_jfuss.py")},
                parameter=dict(SIGMA_M=SIGMA_M, ZELLE_M=ZELLE_M, LEDER_HART=LEDER_HART, VORN_LEDER=VORN_LEDER, GEWINN_GRENZE=GEWINN_GRENZE,
                               KLASSEN=KLASSEN))
    N = np.load(netz)
    H = np.load(Q + "baby_netz/fix1.npz")
    heute = bild_laden(Q + "cub/NCBearCub.png")
    heute_u8 = np.asarray(Image.open(Q + "cub/NCBearCub.png").convert("RGB"))
    assert json.loads(str(N["atlas"])) == json.loads(str(H["atlas"])), "Atlas weicht ab"
    # Kopf-Teile muessen bit-gleich zu heute sein (FORM): U/J/Ol/Or Lage, UV, Dreiecke
    for k in (1, 2, 4, 5):
        a, b = N["teil"] == k, H["teil"] == k
        assert np.array_equal(N["UV"][a], H["UV"][b]) and np.array_equal(N["kopfX"][a], H["kopfX"][b]), "Kopfteil %d nicht gleich" % k
    # Straehnen-Saaten von heute (fix1-Netz) -- Hals-Ende laeuft genau wie heute in den Kopf
    KH = kopf_vorbereiten(H)
    Sd_heute = saaten(KH["X"], KH["Fh"], KH["Nn"], KH["tnam_f"], KH["gruppe_f"], KH["P"])
    Sd = saaten_uebertragen(Sd_heute, H, N, kopf_vorbereiten(N))
    info["saaten"] = dict(gesamt=int(Sd["n_s"]), hals_mitgewandert=Sd["hals_saaten"])
    if selbsttest:
        log("SELBSTTEST: heutiges Netz + heutiger Koerper -> muss die heutige PNG geben")
        Sd_h = saaten_uebertragen(Sd_heute, H, H, KH)          # Uebertragung auf sich selbst = Identitaet (mitgeprueft)
        KR = kopf_rechnung(H, heute, Sd_h)
        st = np.clip(np.round(KR["img"]), 0, 255).astype(np.uint8)
        d = np.abs(st.astype(int) - heute_u8.astype(int)).max(2)
        ausser = ~KR["in_k"]
        kopf = KR["m"] & ~KR["hals_pix"]
        info["selbsttest"] = dict(kopf_texel=int(kopf.sum()), kopf_verschieden=int((d[kopf] > 0).sum()),
                                  hals_texel=int(KR["hals_pix"].sum()), hals_max=int(d[KR["hals_pix"]].max()), hals_verschieden=int((d[KR["hals_pix"]] > 0).sum()),
                                  rest_ausserhalb_verschieden=int((d[ausser & ~KR["m"]] > 0).sum()), rest_max=int(d[ausser & ~KR["m"]].max()))
        log("SELBSTTEST", info["selbsttest"], "%.0fs" % (time.time() - t0))
    # (a) Koerper
    R, KI = koerper(N, heute, H, info)
    kimg = np.zeros((GR, GR, 3))
    kimg[:RECHT, :RECHT] = R
    log("KOERPER fertig %.0fs" % (time.time() - t0), "Faktor", info["faktor"])
    # (b) Hals: Kopf-Rechnung mit dem neuen Netz, neuem Koerper, Saaten von heute
    KR = kopf_rechnung(N, kimg, Sd)
    log("HALS fertig %.0fs" % (time.time() - t0), "Kopf-Texel", KR["n_kopf"], "Hals-Texel", KR["n_hals"])
    # Kopf-Texel ausserhalb des Hals-Streifens muessen in der Rechnung = heute sein (Kontrolle der Kopie, nicht geschrieben)
    kr8 = np.clip(np.round(KR["img"]), 0, 255).astype(np.uint8)
    streifen = np.zeros((GR, GR), bool)
    streifen[STREIFEN[0]:STREIFEN[1], :] = True
    kopf_aus = KR["m"] & ~streifen
    dk = np.abs(kr8.astype(int) - heute_u8.astype(int)).max(2)[kopf_aus]
    info["kopf_rechnung_gleich_heute"] = dict(texel=int(kopf_aus.sum()), verschieden=int((dk > 0).sum()), max=int(dk.max()),
                                              hinweis="nur Kontrolle der Kopie (nicht geschrieben): Raenge n_mid verschieben sich mit dem neuen Hals")
    assert not (KR["hals_pix"] & ~streifen).any(), "Hals-Texel ausserhalb des Streifens"
    assert not (KR["m"] & ~KR["hals_pix"] & streifen).any(), "Kopf-Texel im Hals-Streifen"
    # Zusammensetzen: heute + Rechteck + Streifen
    out = heute_u8.copy()
    out[:RECHT, :RECHT] = np.clip(np.round(R), 0, 255).astype(np.uint8)
    out[streifen] = kr8[streifen]
    neu_mask = np.zeros((GR, GR), bool)
    neu_mask[:RECHT, :RECHT] = True
    neu_mask |= streifen
    gleich = (out == heute_u8).all(2)
    info["byte_gleich_ausserhalb"] = dict(texel=int((~neu_mask).sum()), verschieden=int((~gleich & ~neu_mask).sum()))
    assert info["byte_gleich_ausserhalb"]["verschieden"] == 0
    info["geaendert"] = dict(rechteck=int((~gleich[:RECHT, :RECHT]).sum()), streifen=int((~gleich & streifen).sum()))
    Image.fromarray(out, "RGB").save(aus)
    info["aus"] = aus
    info["aus_md5"] = md5(aus)
    info["sekunden"] = round(time.time() - t0, 1)
    log("TEXTUR", aus, out.shape, info["aus_md5"], "Zonen", json.dumps(info["zonen"]), "Leder", info["leder"])
    if log_aus:
        json.dump(info, open(log_aus, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    return info


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    lg = sys.argv[sys.argv.index("--log") + 1] if "--log" in sys.argv else None
    if lg in a:
        a.remove(lg)
    main(a[0], a[1], lg, "--selbsttest" in sys.argv)
