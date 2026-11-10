# Lauf baer-baby (10.11.2026): Body-Textur NCBearCub.png (1024 x 1024 RGB) fuer den Entwurf des Jungen. Neu gebaut (nicht aus
# baer_textur_pfote.py kopiert: dort wird aus Fell-Ansichten des Hochmodells gebacken; das Junge hat dafuer kein Hochmodell).
# - Koerper-Rechteck: Textur des Erwachsenen (NCBearTest NCBear.png, nur gelesen) in das verkleinerte UV-Rechteck umgerechnet, Farbe je
#   Kanal auf den Soll-Ton des Jungen gezogen (SPEZ 4.3 Koerper (79,58,50)); Fell-Struktur bleibt die des Erwachsenen.
# - Kopfteile (U, J, Hals, Ohren): prozedural aus den Zahlen der SPEZ 4.3 -- je Texel Lage im Kopf-Rahmen (W) und Normale aus dem
#   Netz, Zonen (Gesicht, Stirn, Wange, Augenring, ueber dem Auge, Schnauze hell, Nase, Iris + gemalter Glanzpunkt, Unterlid, Mund,
#   Zunge, Ohrmulde/-rand/-haare, Hals -> Koerperton), Fell als Rauschen (Grund + 10-15 % helle Spitzen), Verdeckung aus der Form
#   (Kopf-Feld entlang der Normalen: Mulden werden dunkler, malt aber keine Form, die im Ton fehlt).
# KEIN Pixel der Vorlage: dieses Skript liest das Foto nicht; Farbziele sind die Zahlen aus SPEZ 4.3.
# fix1 (10.11.2026, Befunde M1-M4 aus pruef_baby.md): Fell jetzt als feine Straehnen per Linien-Integral-Faltung (LIC) im UV
#   entlang des Haarstrichs (Weltlaenge je Straehne fest, 3D-Rauschen als Grund -> gleiche Koernung auf allen Kopfteilen, keine
#   Kork-Flecken mehr), Kontrast am Koerperfell geeicht; Unterlid dunkel graubraun und schmal (statt hellgrau -> kein 'Augenweiss'),
#   Lippe/Unterkiefer-Vorderkante dunkel statt rot, Zunge nur hinten; Ohren: Rand Fell statt heller Ring, Mulde nur in der Mitte
#   dunkel, Innenhaare hell; Hals-Ende nimmt genau die Kopffarbe (verschweisster Uebergang ohne Farbbruch); Kopfgrund waermer.
# Aufruf: python baer_textur_baby.py NETZ.npz AUS.png [zonen.npz]
# Statisch/offline, nicht gespielt.
import json
import math
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_form_baby as bf  # noqa: E402

GR = 1024
POL = 4.0 / 1024
ZIEL = {   # SPEZ 4.3 (sRGB, Median)
    "gesicht": (82, 62, 52), "stirn_oben": (106, 82, 68), "wange": (88, 60, 42), "augenring": (53, 40, 36), "ueber_auge": (73, 54, 46),
    "schnauze_oben": (155, 131, 118), "schnauze_seite": (158, 125, 103), "nase": (23, 19, 20), "iris": (27, 22, 21),
    "ohr_mulde": (27, 15, 10), "ohr_rand": (146, 113, 93), "ohr_haar": (120, 92, 74), "koerper": (79, 58, 50),
    "maul_innen": (42, 24, 24), "zunge": (112, 62, 64), "lippe": (34, 24, 22), "unterlid": (78, 68, 63),
}
SPITZE = ((132, 110, 101), (160, 134, 112))
STRANG_3D = True         # fix1: Straehnen in 3D statt LIC im UV (LIC zeigte Naehte an den Kartenraendern)
FELL_AMP = 0.16          # Straehnen-Kontrast (Faktor um den Zonen-Median), geeicht am Koerperfell (fix1/log/textur_*.txt)
STRAEHNE_W = 0.055       # Straehnenlaenge in W (Kopfbreite); Kopffell kurz
SPITZE_W = 0.03
KOERPER_HELL = np.array((79.0, 58.0, 50.0)) / np.array((80.0, 63.0, 57.0))   # Koerper-Soll / Gesicht-Soll (SPEZ 4.3)


# ------------------------------------------------------------------ Rauschen (Wert-Rauschen 3D) ---------------------------------
def _hash(ix, iy, iz, seed):
    h = (ix * 73856093) ^ (iy * 19349663) ^ (iz * 83492791) ^ (seed * 2654435761)
    h = (h ^ (h >> 13)) * 1274126177
    h = h ^ (h >> 16)
    return (h & 0xFFFFFF).astype(np.float64) / float(0xFFFFFF)


def rauschen(P, f, seed=0):
    Q = P * f
    i = np.floor(Q).astype(np.int64)
    t = Q - i
    t = t * t * (3 - 2 * t)
    out = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (t[:, 0] if dx else 1 - t[:, 0]) * (t[:, 1] if dy else 1 - t[:, 1]) * (t[:, 2] if dz else 1 - t[:, 2])
                out = out + w * _hash(i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz, seed)
    return out


def fell(P, ziel, n_mid, n_hi, spitzen=0.12, hell=1.0):
    """Grund um den Ziel-Median (Faktor 0,62..1,30), dazu helle Spitzen (oberste 'spitzen'-Anteile des Feinrauschens)."""
    z = np.array(ziel, float) * hell
    u = np.clip(n_mid, 1e-4, 1 - 1e-4)
    zz = np.clip(np.log(u / (1 - u)) / 1.7, -2.5, 2.5)     # n_mid gleichverteilt -> etwa normalverteilt
    g = 1.0 + FELL_AMP * zz          # fix1: vorher 0,45..1,6 (grobe dunkle Kleckse, Befund M2)
    c = z[None, :] * g[:, None]
    sp = n_hi > 1.0 - spitzen
    tip = np.array(SPITZE[0], float) + (np.array(SPITZE[1], float) - np.array(SPITZE[0], float)) * ((n_hi - (1 - spitzen)) / spitzen)[:, None]
    tip = tip * (np.array(ziel, float) / np.array(ZIEL["gesicht"], float)).clip(0.6, 1.6) ** 0.5
    c[sp] = c[sp] * 0.55 + tip[sp] * 0.45          # fix1: Spitzen weicher (vorher 0,65 -> Sprenkel)
    return c


def sst(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ Rasterung der Kopfteile im UV -------------------------------
def rastern(UVp, X, Nn, F, sel):
    img_X = np.full((GR, GR, 3), np.nan)
    img_N = np.zeros((GR, GR, 3))
    img_i = np.full((GR, GR), -1, int)
    for t in np.where(sel)[0]:
        a, b, c = F[t]
        p = UVp[[a, b, c]]
        x0, y0 = np.floor(p.min(0)).astype(int)
        x1, y1 = np.ceil(p.max(0)).astype(int)
        x0, y0 = max(x0 - 1, 0), max(y0 - 1, 0)
        x1, y1 = min(x1 + 1, GR - 1), min(y1 + 1, GR - 1)
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        v0, v1 = p[1] - p[0], p[2] - p[0]
        den = v0[0] * v1[1] - v1[0] * v0[1]
        if abs(den) < 1e-12:
            continue
        dx, dy = xs - p[0, 0], ys - p[0, 1]
        l1 = (dx * v1[1] - v1[0] * dy) / den
        l2 = (v0[0] * dy - dx * v0[1]) / den
        l0 = 1 - l1 - l2
        m = (l0 >= -0.02) & (l1 >= -0.02) & (l2 >= -0.02)
        if not m.any():
            continue
        yy, xx = (ys[m] - 0.5).astype(int), (xs[m] - 0.5).astype(int)
        L = np.stack((l0[m], l1[m], l2[m]), 1)
        img_X[yy, xx] = L @ X[[a, b, c]]
        img_N[yy, xx] = L @ Nn[[a, b, c]]
        img_i[yy, xx] = t
    return img_X, img_N, img_i


def lic(m, iX, teilbild, fl, L_welt, f_rausch, seed, kmax=26):
    """fix1: Linien-Integral-Faltung im UV-Raster. Je Kopf-Texel: Richtung des Haarstrichs (3D, tangential) -> Texel-Richtung ueber
    die Jacobi-Matrix der Rasterung; Rauschen (3D, Frequenz f_rausch je W) entlang der Stromlinie gemittelt, Laenge L_welt (W) je
    Straehne unabhaengig von der Texeldichte. Rueckgabe: Wert je Kopf-Texel (Reihenfolge wie iX[m])."""
    ys, xs = np.nonzero(m)
    P0 = iX[ys, xs]

    def nb(dy, dx):
        y2, x2 = np.clip(ys + dy, 0, GR - 1), np.clip(xs + dx, 0, GR - 1)
        ok = m[y2, x2] & (teilbild[y2, x2] == teilbild[ys, xs])
        return np.nan_to_num(iX[y2, x2] - P0), ok
    a_, oa = nb(0, 1)
    b_, ob = nb(0, -1)
    Xu = np.where(oa[:, None], a_, np.where(ob[:, None], -b_, 0.0))
    a_, oa = nb(1, 0)
    b_, ob = nb(-1, 0)
    Xv = np.where(oa[:, None], a_, np.where(ob[:, None], -b_, 0.0))
    g11, g12, g22 = (Xu * Xu).sum(1), (Xu * Xv).sum(1), (Xv * Xv).sum(1)
    r1, r2 = (Xu * fl).sum(1), (Xv * fl).sum(1)
    det = g11 * g22 - g12 ** 2
    det = np.where(np.abs(det) < 1e-14, 1e-14, det)
    du, dv = (g22 * r1 - g12 * r2) / det, (g11 * r2 - g12 * r1) / det
    nrm = np.maximum(np.hypot(du, dv), 1e-12)
    du, dv = du / nrm, dv / nrm
    Lt = np.linalg.norm(Xu * du[:, None] + Xv * dv[:, None], axis=1)
    K = np.clip(0.5 * L_welt / np.maximum(Lt, 1e-6), 2, kmax)
    DX = np.zeros((GR, GR))
    DY = np.zeros((GR, GR))
    DX[ys, xs], DY[ys, xs] = du, dv
    NZ = np.zeros((GR, GR))
    NZ[ys, xs] = rauschen(P0, f_rausch, seed)
    acc = NZ[ys, xs].copy()
    ws = np.ones(len(ys))
    for sg in (1.0, -1.0):
        px, py = xs + 0.5, ys + 0.5
        vx, vy = sg * du, sg * dv
        lebt = np.ones(len(ys), bool)
        for k in range(1, kmax + 1):
            px, py = px + vx, py + vy
            ix, iy = np.clip(px.astype(int), 0, GR - 1), np.clip(py.astype(int), 0, GR - 1)
            lebt &= m[iy, ix] & (teilbild[iy, ix] == teilbild[ys, xs]) & (k <= K)
            nx_, ny_ = DX[iy, ix], DY[iy, ix]
            dreh = (nx_ * vx + ny_ * vy) < 0
            nx_, ny_ = np.where(dreh, -nx_, nx_), np.where(dreh, -ny_, ny_)
            vx, vy = np.where(lebt, nx_, vx), np.where(lebt, ny_, vy)
            w = (1.0 - k / (K + 1.0)) * lebt
            acc += w * NZ[iy, ix]
            ws += w
            if not lebt.any():
                break
    return acc / ws, K


def haarstrich(Q, tnam, P):
    """Haarstrich-Richtung (3D, Kopf-Rahmen, noch nicht tangential): von der Nasenspitze weg; Hals zum Koerper; Ohren radial."""
    fl = Q - np.array((0.30, 0.0, -0.14))
    fl = np.where((tnam == "H")[:, None], np.array((-0.82, 0.0, -0.57)), fl)
    for s_, nm_ in ((1.0, "Ol"), (-1.0, "Or")):
        mm_ = tnam == nm_
        fl[mm_] = Q[mm_] - np.array(P["ohr_c"]) * (1, s_, 1)
    return fl


def tangential(fl, Nn):
    fl = fl - Nn * (fl * Nn).sum(1)[:, None]
    leer = np.linalg.norm(fl, axis=1) < 1e-6
    fl[leer] = np.cross(Nn[leer], (0.0, 0.0, 1.0)) + 1e-3
    return fl / np.maximum(np.linalg.norm(fl, axis=1), 1e-9)[:, None]


def straehnen(Pm, Nm, gruppe_t, X, F, Nv, tnam_f, gruppe_f, P, L=0.05, breite=0.0028, abstand=0.0085, spitzen=0.13, seed=21):
    """fix1: 3D-Strang-Rauschen. Saat-Punkte flaechengleich auf den Kopf-Dreiecken (Abstand ~abstand W), je Saat eine Straehne
    (Laenge L, Breite 'breite', Richtung = Haarstrich tangential, Staerke zufaellig); 'spitzen'-Anteil der Saaten sind helle Spitzen
    (nur die vordere Haelfte der Straehne). Texel summieren alle Straehnen derselben Gruppe (Kopf / Ohr l / Ohr r) in 3D-Naehe mit
    passender Normale. Rueckgabe: Grundmuster S, Spitzen T je Texel."""
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
    Cf = tangential(haarstrich(C, tnam_f[t], P), Cn)
    Cg = gruppe_f[t]
    amp = rng.normal(0.0, 1.0, n_s)
    tip = rng.random(n_s) < spitzen
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
    return S, T, n_s


def normalen(P, F):
    key = np.round(P, 7)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    acc = np.zeros((wid.max() + 1, 3))
    for k in range(3):
        np.add.at(acc, wid[F[:, k]], fn)
    N = acc[wid]
    return N / np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]


def main(netz, aus, zonen_aus=None):
    N = np.load(netz)
    P = json.loads(str(N["param"]))
    atlas = json.loads(str(N["atlas"]))
    teil = N["teil"]
    tn = list(N["teil_namen"])
    karte = N["karte"]
    F = N["F"]
    X = np.nan_to_num(N["kopfX"])
    UVp = N["UV"] * GR
    kopf_t = teil > 0
    Nn = normalen(np.where(kopf_t[:, None], X, 0.0), F)
    sel = kopf_t[F].all(1)
    img = np.zeros((GR, GR, 3))
    # ---- Koerper: Textur des Erwachsenen ins Rechteck, Farbe auf den Soll-Ton
    alt = np.asarray(Image.open(bf.TEX_ALT).convert("RGB"), float)
    u0, v0, u1, v1 = atlas["koerper"]
    jj, ii = np.meshgrid(np.arange(GR), np.arange(GR))
    in_k = ((jj + 0.5) / GR < u1) & ((ii + 0.5) / GR < v1)
    su = (((jj + 0.5) / GR) - (u0 + POL)) / (u1 - u0 - 2 * POL) * GR - 0.5
    sv = (((ii + 0.5) / GR) - (v0 + POL)) / (v1 - v0 - 2 * POL) * GR - 0.5
    su, sv = np.clip(su, 0, GR - 1.001), np.clip(sv, 0, GR - 1.001)
    x0, y0 = su.astype(int), sv.astype(int)
    fx, fy = (su - x0)[..., None], (sv - y0)[..., None]
    samp = (alt[y0, x0] * (1 - fx) * (1 - fy) + alt[y0, x0 + 1] * fx * (1 - fy) + alt[y0 + 1, x0] * (1 - fx) * fy + alt[y0 + 1, x0 + 1] * fx * fy)
    # Median des Rumpfes beim Erwachsenen (101,71,49) -> Soll (79,58,50)
    gain = np.array(ZIEL["koerper"], float) / np.array((101.0, 71.0, 49.0))
    img[in_k] = samp[in_k] * gain
    # Rand-Farbe des Koerpers je Halsspalte (fuer den Hals-Loft)
    kb = teil == 0
    uvk = N["UV"][kb]
    pk = (uvk * GR).astype(int).clip(0, GR - 1)
    kfarbe = img[pk[:, 1], pk[:, 0]]
    # ---- Kopfteile rastern
    iX, iN, iI = rastern(UVp, X, Nn, F, sel)
    m = iI >= 0
    Pm = iX[m]
    Nm = iN[m]
    Nm /= np.maximum(np.linalg.norm(Nm, axis=1), 1e-9)[:, None]
    tri = iI[m]
    tteil = np.array([tn[k] for k in teil[F[tri, 0]]])
    tkarte = karte[F[tri, 0]]
    x, y, z = Pm[:, 0], Pm[:, 1], Pm[:, 2]
    ay = np.abs(y)
    # fix1: Haarstrich (3D, tangential): von der Nasenspitze weg; Hals zum Koerper; Ohren radial aus der Ohrmitte
    fl = Pm - np.array((0.30, 0.0, -0.14))
    fl = np.where((tteil == "H")[:, None], np.array((-0.82, 0.0, -0.57)), fl)
    for s_, nm_ in ((1.0, "Ol"), (-1.0, "Or")):
        mm_ = tteil == nm_
        fl[mm_] = Pm[mm_] - np.array(P["ohr_c"]) * (1, s_, 1)
    fl = fl - Nm * (fl * Nm).sum(1)[:, None]
    leer = np.linalg.norm(fl, axis=1) < 1e-6
    fl[leer] = np.cross(Nm[leer], (0.0, 0.0, 1.0)) + 1e-3
    fl /= np.maximum(np.linalg.norm(fl, axis=1), 1e-9)[:, None]
    tb = np.full((GR, GR), -1, int)
    tb[m] = teil[F[tri, 0]]
    if STRANG_3D:
        # fix1: Straehnen in 3D (kartenunabhaengig, keine Naehte); Gruppen: Kopf (U, J, H) / Ohr l / Ohr r
        gname = {"U": 0, "J": 0, "H": 0, "Ol": 1, "Or": 2}
        tnam_all = np.array([tn[k] for k in teil])
        sel_f = sel
        Fh = F[sel_f]
        gruppe_f = np.array([gname[tn[k]] for k in teil[Fh[:, 0]]])
        l1, l2, n_saat = straehnen(Pm, Nm, np.array([gname[k] for k in tteil]), X, Fh, Nn, tnam_all[Fh[:, 0]], gruppe_f, P)
        K1 = np.array([n_saat])
    else:
        l1, K1 = lic(m, iX, tb, fl, STRAEHNE_W, 260.0, 5)
        l2, _ = lic(m, iX, tb, fl, SPITZE_W, 330.0, 6)
    # fix1: an Kartenraendern enden die Stromlinien -> dort Straehnen-Kontrast ausblenden (sonst sichtbare Naht zwischen den Karten)
    kb_ = np.full((GR, GR), -1, int)
    kn_ = {k: i for i, k in enumerate(np.unique(tkarte))}
    kb_[m] = np.array([kn_[k] for k in tkarte])
    rand_d = np.zeros((GR, GR))
    innen = m.copy()
    for st in range(1, 9):
        nb_ok = innen.copy()
        for dy_, dx_ in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            sh = np.roll(np.roll(kb_, dy_, 0), dx_, 1)
            nb_ok &= (sh == kb_)
        rand_d[innen & ~nb_ok] = st
        innen = nb_ok
    rand_d[innen] = 9
    rand_f = sst(1.0, 8.0, rand_d[m])
    if not STRANG_3D:
        l1 = l1.mean() + (l1 - l1.mean()) * (0.35 + 0.65 * rand_f)
        l2 = l2.mean() + (l2 - l2.mean()) * (0.35 + 0.65 * rand_f)
    gross = rauschen(Pm, 9.0, 7)                                        # weiche Buendel (klein, keine Flecken)
    n_mid = np.argsort(np.argsort(l1 + 0.10 * (gross - 0.5))) / max(len(l1) - 1, 1)
    n_hi = np.argsort(np.argsort(l2 + 0.6 * (l1 - l1.mean()))) / max(len(l2) - 1, 1)
    print("TEXTUR Straehnen:", ("3D, Saaten %d" % K1[0]) if STRANG_3D else ("LIC Schritte median %.1f" % np.median(K1)))
    W = {}
    # Grundzonen (weich)
    W["gesicht"] = np.ones(len(Pm))
    W["stirn_oben"] = sst(0.14, 0.30, z) * sst(-0.05, 0.1, -x - 0.0 + 0.1)
    W["wange"] = sst(0.26, 0.40, ay) * sst(-0.02, -0.12, z) * sst(-0.55, -0.35, x)
    # Augen: Abstand in der Augen-Ebene zur Augenmitte (Oberflaechenpunkt)
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
    W["augenring"] = sst(2.6, 1.6, rho_aug) * (rho_aug > 0.98)
    W["ueber_auge"] = sst(3.6, 2.4, rho_aug) * sst(0.6, 1.6, unten_aug) * (1 - W["augenring"])
    # Schnauze hell: auf der Schnauze (x > Absatz) innerhalb der Schnauzenbreite, nach oben bis zum Absatz, Zunge bis zwischen die Augen
    hb = np.interp(x, *P["sn_breite"])
    zo = np.interp(x, *P["sn_oben"])
    sn = sst(0.0, 0.05, x) * sst(1.12, 0.92, ay / hb) * sst(zo + 0.035, zo - 0.005, z)
    zunge_hell = sst(0.05, -0.02, x) * sst(-0.06, 0.0, x) * sst(0.07, 0.045, ay) * sst(0.10, 0.04, z) * sst(-0.04, -0.01, z)
    zunge_hell = np.maximum(zunge_hell, sst(-0.08, 0.02, x) * sst(0.06, 0.035, ay) * sst(0.08, 0.03, z) * sst(-0.03, 0.0, z))
    hell = np.clip(np.maximum(sn, zunge_hell) * (tteil != "H") * (tteil != "Ol") * (tteil != "Or"), 0, 1)
    seitlich = sst(0.35, 0.8, ay / np.maximum(hb, 1e-3))
    W["schnauze_oben"] = hell * (1 - seitlich)
    W["schnauze_seite"] = hell * seitlich
    # Unterkiefer vorn/unter der Lippe: Schnauzenhell auch auf J vorn oben (Unterlippe), darunter Gesicht
    mlin = np.interp(x, *P["ma_linie"])
    jv = (tteil == "J")
    W["schnauze_seite"] = np.where(jv, sst(mlin - 0.07, mlin - 0.02, z) * sst(0.02, 0.08, x) * 0.8, W["schnauze_seite"])
    W["schnauze_oben"] = np.where(jv, 0.0, W["schnauze_oben"])
    # Nase
    dn = bf.nase(Pm, P)
    nasen = sst(0.006, -0.002, dn)
    W["nase"] = nasen
    # Mund: Lippenkante (Abstand zur Ebene z = m vorn), Gaumen, Zunge (J oben)
    gaumen = (tteil == "U") & (x > P["ma_xh"] - 0.005) & (z < mlin - 0.002) & (Nm[:, 2] < -0.3)
    lippe = (tteil == "U") & (x > P["ma_xh"] - 0.01) & (np.abs(z - mlin) < 0.010) & (Nm[:, 2] > -0.3)
    zunge = jv & (Nm[:, 2] > 0.5) & (z > mlin - 0.02) & (x < 0.15)          # fix1: nur hinten (vorn: dunkle Unterlippe)
    lippe_j = jv & (z > mlin - 0.035) & (x > 0.12) & ~zunge
    W["maul_innen"] = gaumen.astype(float) + (jv & (x < P["ma_xh"]) & (Nm[:, 2] > 0.2)).astype(float)
    W["zunge"] = zunge.astype(float)
    W["lippe"] = np.maximum(lippe * sst(0.010, 0.002, np.abs(z - mlin)), lippe_j.astype(float))
    # Augapfel, Loch-Wand, Unterlid
    auf_ball = np.zeros(len(Pm), bool)
    glanz = np.zeros(len(Pm))
    for mz, an in an_l:
        d = np.linalg.norm(Pm - mz, axis=1)
        ab = np.abs(d - P["au_ball_r"]) < 0.0025
        auf_ball |= ab
        hn = an + np.array((0.0, 0.0, 0.24))     # fix1: Glanzpunkt in die sichtbare Kappe (Oeffnung als Kegel enger, vorher 0,55 = verdeckt)
        hn /= np.linalg.norm(hn)
        gp = mz + hn * P["au_ball_r"]
        glanz = np.maximum(glanz, sst(0.0075, 0.0035, np.linalg.norm(Pm - gp, axis=1)) * ab)
    loch = (rho_aug < 1.02) & ~auf_ball & (tteil == "U")
    W["iris"] = auf_ball.astype(float) + loch.astype(float)
    W["unterlid"] = (sst(0.99, 1.03, rho_aug) * sst(1.22, 1.12, rho_aug) * sst(-0.35, -0.75, unten_aug)).astype(float)   # fix1: <= 0,005 W, nur unten
    # Ohren
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
    # fix1: Mulde nur in der Mitte dunkel, Innenhaare hell (Foto: 'innen heller'), Rand = Kopffell mit Spitzen statt heller Ring
    W["ohr_mulde"] = ohr * vorn * sst(mr * 0.62, mr * 0.38, r_ohr)
    W["ohr_haar"] = ohr * vorn * sst(mr * 0.35, mr * 0.65, r_ohr) * sst(mr * 1.15, mr * 0.95, r_ohr)
    W["ohr_rand"] = ohr * vorn * sst(mr * 1.0, R * 0.9, r_ohr) * (1 - W["ohr_mulde"]) * 0.35
    # Farben je Zone und Mischung (Reihenfolge = Vorrang)
    farbe = fell(Pm, ZIEL["gesicht"], n_mid, n_hi, 0.13)
    # Hinterkopf/Nacken einen Hauch waermer (Uebergang zum Koerperfell, SPEZ 4.3 Koerper/Wange)
    hk = (sst(-0.28, -0.50, x) * (tteil == "U"))[:, None]
    farbe = farbe * (1 - hk) + fell(Pm, (86, 62, 48), n_mid, n_hi, 0.13) * hk
    for zn in ("stirn_oben", "wange", "augenring", "ueber_auge", "schnauze_seite", "schnauze_oben"):
        sp = 0.13 if zn in ("stirn_oben", "wange") else 0.06
        c = fell(Pm, ZIEL[zn], n_mid, n_hi, sp)
        if zn.startswith("schnauze"):
            c = np.array(ZIEL[zn], float)[None, :] * (0.86 + 0.28 * n_mid)[:, None]
            lichter = rauschen(Pm, 120.0, 7) > 0.86
            c[lichter] = c[lichter] * 0.4 + np.array((190.0, 160.0, 140.0)) * 0.6
        farbe = farbe * (1 - W[zn][:, None]) + c * W[zn][:, None]
    # Hals: von der Koerper-Randfarbe (v = 0) zum Kopf (v = 1); Rueckseite der Ohren = Kopffell
    hals = tteil == "H"
    if hals.any():
        ah = atlas["hals"]
        pix = np.argwhere(m)[hals]
        vfr = ((pix[:, 0] + 0.5) / GR - (ah[1] + POL)) / (ah[3] - ah[1] - 2 * POL)
        Xh = Pm[hals]
        rf = np.zeros((hals.sum(), 3))
        # Koerperpunkte nahe dem Rand: Lage im Kopf-Rahmen ueber die Ruhe-Lage der Halspunkte (v=0) -> naechster Koerperpunkt
        Ph = N["P"][F[tri[hals], 0]]
        kP = N["P"][kb]
        for j0 in range(0, len(Ph), 4000):
            dd = np.linalg.norm(Ph[j0:j0 + 4000, None, :] - kP[None, ::3, :], axis=2)
            nn_ = np.argsort(dd, axis=1)[:, :6]
            rf[j0:j0 + 4000] = kfarbe[::3][nn_].mean(1)
        kopfc = farbe[hals].copy()          # fix1: genau die Kopffarbe an dieser Stelle (verschweisster Uebergang)
        u_ = np.clip(n_mid[hals], 1e-4, 1 - 1e-4)
        koerc = rf * (1.0 + FELL_AMP * np.clip(np.log(u_ / (1 - u_)) / 1.7, -2.5, 2.5))[:, None]
        sp_ = n_hi[hals] > 0.90
        koerc[sp_] = koerc[sp_] * 0.55 + np.array(SPITZE[0], float) * 0.45
        b = sst(0.10, 0.80, vfr)[:, None]
        farbe[hals] = koerc * (1 - b) + kopfc * b
    # Rueckseite der Ohren und Ohrrand
    for zn in ("ohr_rand", "ohr_haar", "ohr_mulde"):
        c = np.array(ZIEL[zn], float)[None, :] * (0.8 + 0.4 * n_mid)[:, None]
        if zn == "ohr_haar":
            c = c * (0.80 + 0.30 * (n_hi > 0.5))[:, None]
        farbe = farbe * (1 - W[zn][:, None]) + c * W[zn][:, None]
    for zn in ("unterlid", "lippe", "maul_innen", "zunge", "nase", "iris"):
        c = np.array(ZIEL[zn], float)[None, :] * (0.9 + 0.2 * n_mid)[:, None]
        if zn == "nase":
            c = c * 0.72          # Grund dunkler, damit der Median mit Oberkante/Glanz beim Soll (23,19,20) liegt
            # Oberkante (98,95,100)..(137,129,127) als Band, kleiner Glanzfleck oben vorn, Nasenloecher dunkler
            ca = np.array(P["na_c"])
            oben = sst(ca[2] + P["na_h"][2] - 0.022, ca[2] + P["na_h"][2] - 0.004, z)
            c = c * (1 - oben[:, None]) + np.array((110.0, 105.0, 108.0))[None, :] * oben[:, None]
            gl = sst(0.022, 0.008, np.linalg.norm((Pm - (ca + (P["na_h"][0], 0.0, P["na_h"][2] * 0.45))) / (1.0, 1.6, 1.0), axis=1))
            c = c * (1 - gl[:, None]) + np.array((150.0, 145.0, 150.0))[None, :] * gl[:, None]
            for s in (1.0, -1.0):
                nl = np.linalg.norm((Pm - (ca[0] + P["na_h"][0], s * P["na_loch_y"], ca[2] - P["na_loch_dz"])) / (1.0, 1.25, 0.8), axis=1)
                lo = sst(0.020, 0.010, nl)
                c = c * (1 - lo[:, None]) + np.array((6.0, 3.0, 3.0))[None, :] * lo[:, None]
        if zn == "iris":
            c = c * (1 - glanz[:, None]) + np.array((225.0, 230.0, 240.0))[None, :] * glanz[:, None]
            c = np.where(loch[:, None], np.array((24.0, 19.0, 17.0))[None, :], c)
        farbe = farbe * (1 - W[zn][:, None]) + c * W[zn][:, None]
    # Verdeckung aus der Form (nur Kopf-Feld, ohne Hals): Kopf-Feld eine Stueck entlang der Normalen
    ao = np.ones(len(Pm))
    # nicht auf gemalte Einzelheiten und nicht ins Maul-Innere (nur bei offenem Maul sichtbar, sonst dort nur dunkel)
    gemalt = np.zeros(len(Pm))
    for zn in ("unterlid", "iris", "nase", "maul_innen", "zunge", "lippe", "ueber_auge"):
        gemalt = np.maximum(gemalt, W[zn])
    kk = ~hals & ~ohr & (gemalt < 0.5)
    for dist, gw in ((0.012, 0.5), (0.03, 0.5)):
        f = bf.kopf_feld(Pm[kk] + Nm[kk] * dist, P)
        ao[kk] -= gw * (1 - np.clip(f / dist, 0, 1)) * 0.30
    farbe = farbe * np.clip(ao, 0.62, 1)[:, None]
    img[m] = farbe
    # Koerper-Ton an das Kopffell angleichen (Mittel/Streuung je Kanal, gemessen auf dem reinen Gesichtsfell)
    rein = np.ones(len(Pm), bool)
    for zn, w in W.items():
        if zn != "gesicht":
            rein &= w < 0.05
    rein &= ~hals & ~ohr
    mu_k, sd_k = farbe[rein].mean(0), farbe[rein].std(0)
    kb_pix = np.zeros((GR, GR), bool)
    pk2 = (N["UV"][kb] * GR).astype(int).clip(0, GR - 1)
    kb_pix[pk2[:, 1], pk2[:, 0]] = True
    mu_b, sd_b = img[kb_pix].mean(0), img[kb_pix].std(0)
    print("TEXTUR Fell Kopf mittel", np.round(mu_k, 1), "streu", np.round(sd_k, 1), "| Koerper (Punkt-UV) mittel", np.round(mu_b, 1), "streu", np.round(sd_b, 1))
    # ---- Polster: leere Texel neben Kopf-Karten mit Nachbarn fuellen (8 Runden)
    voll = m | in_k
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
    img[~voll] = np.array(ZIEL["gesicht"], float)
    out = np.clip(np.round(img), 0, 255).astype(np.uint8)
    Image.fromarray(out, "RGB").save(aus)
    if zonen_aus:
        zon = np.full((GR, GR), "", dtype=object)
        zmask = {}
        for zn, w in W.items():
            mm = np.zeros((GR, GR), bool)
            mm[m] = w > 0.85
            zmask[zn] = mm
        zmask["koerper_rumpf"] = in_k
        np.savez_compressed(zonen_aus, **zmask)
    print("TEXTUR", aus, out.shape, "Kopf-Texel", int(m.sum()), "Anteil Kopf an genutzter Flaeche %.3f" % (m.sum() / (m.sum() + in_k.sum())))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
