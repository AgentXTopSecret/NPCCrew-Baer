# Lauf baer-gen-gross-v2 (12.11.2026), Rolle BAUER GESICHT, Teil Textur (PLAN.md 5): Lage-Karte fuer das neue V, Gesichts-Ebene als
# Vertrag fuer FELL (5.3) und Vorschau-Texturen (fix1-Struktur x neuer Ton, NUR zum Ansehen -- nicht die Abgabe).
# Gemalt wird im 3D (Ruhe-Lage je Texel, tier-Meter), nie im UV von Hand -> nahtlos ueber UV-Naehte.
# Statisch/offline, nicht gespielt. Schreibt nur unter _arbeit/baer_gen_gross/v2/gesicht/.
# Aufruf: python baer_gesicht_tex_gg2.py karten | ebene [k=v ...] | vorschau [nacken=1]
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baer_gesicht_gg2 as GG  # noqa: E402

R, GS = GG.R, GG.GS
sys.path.insert(0, R + "fix1/werkzeug")
S = 1024
KARTE = GS + "karten/_karten_gg2.npz"
EBENE = GS + "ebene/gesicht_ebene.npz"


def sst(a, b, v):
    return GG.sst(a, b, v)


# ------------------------------------------------------------------------------------------------ Lage-Karte (PLAN 5.1)
def karten():
    argv0 = sys.argv
    sys.argv = [argv0[0], GS + "form/E_gg2_basis.npz"]          # uv_maske laedt beim Import argv[1] (nur lesen)
    from uv_maske import raster
    sys.argv = argv0
    B = np.load(GS + "form/E_gg2_basis.npz")
    G = np.load(GS + "gewichte/E_gg2_gewichte.npz")
    V, T, Tg, gp, UV = B["V"], B["T"], B["T_glb"], B["glb_punkt"], B["UV"]
    tp = B["teil_punkt"].astype(str)
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    NL = np.zeros_like(V)
    for k in range(3):
        np.add.at(NL, T[:, k], fn)
    NL /= np.maximum(np.linalg.norm(NL, axis=1, keepdims=True), 1e-12)
    vol = np.einsum("ij,ij->i", V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum()
    if vol < 0:
        NL = -NL
    teil_id = {"aussen": 1, "kralle": 2}
    tid = np.array([teil_id.get(t, 3) for t in tp], float)
    ohr = (B["ohr_l"] | B["ohr_r"]).astype(float)
    sohle = B["sohle"].astype(float)
    nm = [str(n) for n in G["namen"]]
    hj = G["W"][:, nm.index("Bip01_Head")] + G["W"][:, nm.index("Bip01_Jaw")]
    attr = np.c_[V[gp], NL[gp], tid[gp], ohr[gp], sohle[gp], B["kiefer_anteil"][gp], hj[gp]]
    A_ = raster(UV, Tg, S, attr)
    L, N, Tt, X = A_[..., 0:3], A_[..., 3:6], A_[..., 6:9], A_[..., 9:11]
    t, h = GG.rahmen(np.nan_to_num(L.reshape(-1, 3), nan=0.0))
    KR = np.stack((t.reshape(S, S), h.reshape(S, S), L[..., 1]), -1)
    KR[np.isnan(L[..., 0])] = np.nan
    os.makedirs(GS + "karten", exist_ok=True)
    np.savez_compressed(KARTE, L=L, N=N, T=Tt, KR=KR, X=X)
    info = dict(belegt_prozent=round(float((~np.isnan(L[..., 0])).mean() * 100), 2), schluessel=dict(
        L="Ruhe-Lage tier-Meter des NEUEN V je Texel (nan = leer)", N="Normale (Aussenhaut, nach aussen)",
        T="Teil-ID (1 aussen, 2 kralle, 3 Maul innen), Ohr-Anteil, Sohle-Anteil (wie R/fix1/tex_final/_karten.npz)",
        KR="Kopf-Rahmen t (Auge 0 -> Spitze 1), h (oben +), y", X="Kiefer-Anteil (FORM), Head+Jaw-Gewicht"))
    json.dump(info, open(KARTE + ".json", "w"), indent=1)
    print(json.dumps(info))


# ------------------------------------------------------------------------------------------------ Hilfen
def box(a, r):
    for ax in (0, 1):
        pad = [(0, 0)] * a.ndim
        pad[ax] = (r + 1, r)
        c = np.cumsum(np.pad(a, pad, mode="edge"), axis=ax)
        hi = [slice(None)] * a.ndim
        lo = [slice(None)] * a.ndim
        hi[ax] = slice(2 * r + 1, None)
        lo[ax] = slice(None, -2 * r - 1)
        a = (c[tuple(hi)] - c[tuple(lo)]) / (2 * r + 1)
    return a


def mblur(img, m, r=6):
    w = m.astype(float)
    num = box(box(box(img * w[..., None], r), r), r)
    den = box(box(box(w, r), r), r)
    return num / np.maximum(den, 1e-6)[..., None]


def lum(c):
    return 0.299 * c[..., 0] + 0.587 * c[..., 1] + 0.114 * c[..., 2]


def rgb2hsv(c):
    c = np.asarray(c, float) / 255.0
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    mx, mn = c.max(-1), c.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-9
    rr = m & (mx == r)
    gg = m & (mx == g) & ~rr
    bb = m & ~rr & ~gg
    h[rr] = ((g - b)[rr] / d[rr]) % 6
    h[gg] = (b - r)[gg] / d[gg] + 2
    h[bb] = (r - g)[bb] / d[bb] + 4
    return np.stack((h * 60.0, np.where(mx > 0, d / np.maximum(mx, 1e-9), 0), mx), -1)


def hsv2rgb(hsv):
    h, s, v = hsv[..., 0] % 360, hsv[..., 1], hsv[..., 2]
    c = v * s
    x = c * (1 - np.abs((h / 60.0) % 2 - 1))
    m = v - c
    z = np.zeros_like(h)
    k = (h // 60).astype(int) % 6
    r = np.choose(k, [c, x, z, z, x, c])
    g = np.choose(k, [x, c, c, x, z, z])
    b = np.choose(k, [z, z, x, c, c, x])
    return np.stack((r + m, g + m, b + m), -1) * 255.0


def lippen_linie(V, lo):
    """Polylinie des Lippenschnitts (Zwillinge der Oberlippe), sortiert um einen Punkt hinter dem Maul."""
    P = V[lo]
    th = np.arctan2(P[:, 1], P[:, 0] - 0.90)
    return P[np.argsort(th)]


def abst_polylinie(Q, Pl):
    best = np.full(len(Q), 9.0)
    for a, b in zip(Pl[:-1], Pl[1:]):
        ab = b - a
        L2 = max(ab @ ab, 1e-12)
        t = np.clip(((Q - a) @ ab) / L2, 0, 1)
        best = np.minimum(best, np.linalg.norm(Q - (a + t[:, None] * ab), axis=1))
    return best


# Parameter der Ebene (Faktoren auf den eigenen Ruecken-Median je Farbvariante, PLAN 3.4; Masse in Metern)
PE = dict(f_stirn=0.94, f_wange=0.84, f_seite=1.05, f_bruecke=1.16, f_kinn=0.88, f_ring=0.68, hue_braun=7.0, sat_braun=0.03,
          kinn_grau=0.20, kuppe_cx=1.140, kuppe_cz=0.632, kuppe_b=0.035, kuppe_a=0.0500, kuppe_p=3.0, kuppe_rand=0.0025,
          loch_y=0.025, loch_z=0.624, loch_a=0.0165, loch_b=0.0070, loch_dreh=25.0, rinne_b=0.0018,
          aug_a=0.0130, aug_b=0.0072, iris_r=0.0058, ring_r=0.020, lippe_b=0.00175, lippe_rand=0.0013)


def ebene(kv):
    P = dict(PE)
    P.update({k: float(v) for k, v in kv.items()})
    C = np.load(KARTE)
    L, N, Tt, KR, X = C["L"], C["N"], C["T"], C["KR"], C["X"]
    B = np.load(GS + "form/E_gg2_basis.npz")
    V = B["V"]
    belegt = ~np.isnan(L[..., 0])
    aussen = belegt & (np.abs(np.nan_to_num(Tt[..., 0]) - 1) < 0.5)
    x, y, z = [np.nan_to_num(L[..., i], nan=-9) for i in range(3)]
    nx, ny, nz = [np.nan_to_num(N[..., i]) for i in range(3)]
    t, h = np.nan_to_num(KR[..., 0], nan=-9), np.nan_to_num(KR[..., 1], nan=-9)
    ohr = np.clip(np.nan_to_num(Tt[..., 1]), 0, 1)
    jaw = np.clip(np.nan_to_num(X[..., 0]), 0, 1)
    ay = np.abs(y)
    Pq = np.stack((x, y, z), -1)
    # Hoehe im Schnauzen-Querschnitt (neues V, Kopf-Punkte)
    G = np.load(GS + "gewichte/E_gg2_gewichte.npz")
    kopf = GG.kopfmaske(G)
    tg, ob, un = GG.hoehen_profil(V, kopf)
    top, bot = np.interp(t, tg, ob), np.interp(t, tg, un)
    hn = np.clip((h - bot) / np.maximum(top - bot, 1e-3), 0, 1)
    halb_t = np.interp(t, GG.TT, GG.profil(V, kopf)[:, 0])
    # ---------------- Masken (alle weich, >= 2 cm Uebergang ausser Kuppe/Augen/Lippe)
    # Ohr-Flags der FORM reichen ueber den ganzen Oberkopf (|y| ab 0) -> nur die Ohr-Lappen (|y| > ~7 cm) behalten ihren Ton
    kopfzone = sst(0.70, 0.80, x) * (z > 0.45) * (1 - ohr * sst(0.06, 0.09, ay))
    schnauze = sst(0.10, 0.30, t) * kopfzone
    # helle Schnauzen-Oberseite ueber die GANZE Breite (aus Kevins Kamera sieht man Oberseite + obere Flanken) -> liest sich breit
    bruecke = schnauze * sst(0.40, 0.70, hn) * (1 - sst(0.95, 1.15, ay / np.maximum(halb_t, 0.03)))
    # Nasenruecken zwischen den Augen schmal auslaufen lassen (Foto frontal: helles Band bis zur Stirn, 0,19 Kopfbreite)
    bruecke = np.maximum(bruecke, sst(-0.05, 0.12, t) * (1 - sst(0.10, 0.30, t)) * (1 - sst(0.022, 0.040, ay)) * sst(0.70, 0.90, hn) * kopfzone * 0.8)
    kinn = sst(0.05, 0.25, t) * sst(0.4, 0.8, jaw) * kopfzone
    bruecke = bruecke * (1 - kinn)
    wange = (1 - sst(0.05, 0.20, t)) * sst(0.06, 0.11, ay) * (1 - sst(0.5, 0.8, hn)) * kopfzone * (1 - kinn)
    d_aug = np.minimum(np.linalg.norm(Pq - GG.AUGEN[0], axis=-1), np.linalg.norm(Pq - GG.AUGEN[1], axis=-1))
    ring = (1 - sst(P["ring_r"] * 0.45, P["ring_r"] * 1.35, d_aug)) * kopfzone
    # ---------------- Nasenkuppe: Superellipse in (y, Abstand in der x-z-Ebene zum Kuppen-Zentrum)
    rxz = np.hypot(x - P["kuppe_cx"], z - P["kuppe_cz"])
    se = (ay / P["kuppe_a"]) ** P["kuppe_p"] + (rxz / P["kuppe_b"]) ** P["kuppe_p"]
    rand_rel = P["kuppe_rand"] / P["kuppe_b"]
    kuppe = (1 - sst(1 - 2 * rand_rel, 1 + 2 * rand_rel, se)) * (x > 1.05) * aussen
    # Lichtstreif oben auf der Kuppe (matt), ~4 x 1,5 cm
    streif = kuppe * (1 - sst(0.012, 0.022, ay)) * sst(0.55, 0.75, nz + 0.2 * nx) * (1 - sst(0.006, 0.012, np.abs(z - 0.655)))
    # Nasenloecher: Kommaform auf der Vorderflaeche (y-z-Ebene), aussen nach unten gebogen
    loch = np.zeros_like(x)
    dr = np.radians(P["loch_dreh"])
    for s in (1, -1):
        du, dv = (y - s * P["loch_y"]), (z - P["loch_z"])
        u_ = du * np.cos(dr) * s + dv * np.sin(dr) * 1.0
        v_ = -du * np.sin(dr) * s + dv * np.cos(dr)
        # Komma: aussen (u_ > 0) schmaler und nach unten gebogen
        v_k = v_ + 0.25 * (u_ / P["loch_a"]) ** 2 * P["loch_b"]
        b_ = P["loch_b"] * (1 - 0.35 * np.clip(u_ / P["loch_a"], 0, 1))
        e_ = (u_ / P["loch_a"]) ** 2 + (v_k / b_) ** 2
        loch = np.maximum(loch, (1 - sst(0.75, 1.15, e_)) * sst(0.15, 0.45, nx) * (x > 1.10))
    loch *= aussen
    # Rinne (Philtrum): von der Kuppenmitte bis zur Oberlippe
    lo = B["lippe_ober"]
    z_lip = float(np.median(V[lo][np.abs(V[lo, 1]) < 0.02, 2])) if (np.abs(V[lo, 1]) < 0.02).any() else 0.587
    rinne = (1 - sst(P["rinne_b"], P["rinne_b"] * 2.2, ay)) * sst(z_lip - 0.002, z_lip + 0.002, z) * (1 - sst(0.618, 0.628, z)) \
        * sst(0.15, 0.45, nx) * (x > 1.08) * aussen
    # Lippenlinie (Abstand zur Polylinie der Zwillinge)
    Pl = lippen_linie(V, lo)
    kand = aussen & (x > 0.90) & (z > 0.54) & (z < 0.68)
    d_lip = np.full(x.shape, 9.0)
    ii = np.nonzero(kand)
    d_lip[ii] = abst_polylinie(Pq[ii], Pl)
    lippe = (1 - sst(P["lippe_b"], P["lippe_b"] + P["lippe_rand"], d_lip)) * aussen
    # Augen: Mandel in der Tangentialebene um die gemalte Mitte
    auge = np.zeros_like(x)
    iris = np.zeros_like(x)
    pupille = np.zeros_like(x)
    lid = np.zeros_like(x)
    for au in GG.AUGEN:
        near = aussen & (np.linalg.norm(Pq - au, axis=-1) < 0.03)
        n0 = np.median(np.stack((nx[near], ny[near], nz[near]), -1), 0)
        n0 /= np.linalg.norm(n0)
        e1 = np.cross(n0, np.array([0, 0, 1.0]))
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(e1, n0)
        q = Pq - au
        u_, v_ = q @ e1, q @ e2
        dn = np.abs(q @ n0)
        ok = (dn < 0.02) & (np.linalg.norm(q, axis=-1) < 0.03)
        un = np.clip(np.abs(u_) / P["aug_a"], 0, 1.5)
        breite = P["aug_b"] * np.clip(1 - un ** 2, 0, 1) ** 0.7
        innen = np.abs(v_) - breite                       # < 0 innen
        a_m = (1 - sst(-0.0010, 0.0012, innen)) * (un < 1.05) * ok
        auge = np.maximum(auge, a_m)
        r_i = np.hypot(u_, v_)
        iris = np.maximum(iris, a_m * (1 - sst(P["iris_r"] * 0.8, P["iris_r"] * 1.15, r_i)))
        pupille = np.maximum(pupille, a_m * (1 - sst(P["iris_r"] * 0.35, P["iris_r"] * 0.6, r_i)))
        lid = np.maximum(lid, a_m * sst(-0.0022, -0.0008, innen))
    auge *= aussen
    # ---------------- Faktoren -> Ton je Variante
    F = np.full(x.shape, P["f_stirn"])
    F = F + (P["f_wange"] - F) * wange
    F = F + (P["f_seite"] - F) * schnauze * (1 - kinn)
    F = F + (P["f_bruecke"] - F) * bruecke
    F = F + (P["f_kinn"] - F) * kinn
    F = F + (P["f_ring"] - F) * ring * (1 - bruecke * 0.6)
    a_ton = kopfzone * aussen
    a_glatt = np.clip(np.maximum.reduce([kuppe, loch, auge, lippe, 0.5 * rinne]), 0, 1)
    strich = 1 - 0.5 * kopfzone - 0.2 * schnauze
    masken = ((kuppe > 0.5) * 1 + (loch > 0.5) * 2 + (auge > 0.5) * 4 + (lippe > 0.5) * 8 + (bruecke > 0.5) * 16).astype(np.uint8)
    rep = {"parameter": P, "z_lippe_mitte": round(z_lip, 4)}
    out = {}
    for var, pfad in (("braun", GS + "eingang/NCBearGen.png"), ("foto", GS + "eingang/NCBearGenFoto.png")):
        img = np.asarray(Image.open(pfad).convert("RGB")).astype(float)
        basis = mblur(img, aussen, 6)
        ruecken = aussen & (z > 0.85) & (x > -0.5) & (x < 0.5) & (nz > 0.6)
        rf = np.median(basis[ruecken], 0)
        ton = rf[None, None, :] * F[..., None]
        hsv = rgb2hsv(ton)
        if var == "braun":                                    # Schnauze/Nasenruecken etwas gelber und satter (nur braun)
            wsch = np.clip(bruecke + 0.6 * schnauze * (1 - kinn), 0, 1)
            hsv[..., 0] = hsv[..., 0] + P["hue_braun"] * wsch
            hsv[..., 1] = np.clip(hsv[..., 1] + P["sat_braun"] * wsch, 0, 1)
        hsv[..., 1] = hsv[..., 1] * (1 - P["kinn_grau"] * kinn)
        ton = hsv2rgb(hsv)
        # Augenring dunkelbraun (Ton leicht waermer)
        # Lippenlinie L ~0,20
        lip_rgb = np.array((54, 45, 40)) if var == "braun" else np.array((52, 47, 47))
        ton = ton * (1 - lippe[..., None]) + lip_rgb * lippe[..., None]
        # Kuppe fast schwarz, blaugrau; Lichtstreif; Nasenloecher; Rinne
        ton = ton * (1 - kuppe[..., None]) + np.array((24, 24, 29.0)) * kuppe[..., None]
        ton = ton * (1 - streif[..., None]) + np.array((55, 55, 62.0)) * streif[..., None]
        ton = ton * (1 - loch[..., None]) + np.array((6, 6, 8.0)) * loch[..., None]
        rin = rinne * (1 - kuppe)
        ton = ton * (1 - rin[..., None]) + np.array((30, 28, 30.0)) * rin[..., None]
        # Augen: Lidrand/Pupille fast schwarz, Iris dunkelbraun
        aug_rgb = np.array((14, 11, 10.0))
        ton = ton * (1 - auge[..., None]) + aug_rgb * auge[..., None]
        ton = ton * (1 - (iris * (1 - lid))[..., None]) + np.array((40, 26, 18.0)) * (iris * (1 - lid))[..., None]
        ton = ton * (1 - pupille[..., None]) + np.array((10, 8, 8.0)) * pupille[..., None]
        ton[0:72, 0:548] = 0
        ton[12:32, 598:666] = 0
        out["ton_" + ("braun" if var == "braun" else "foto")] = np.where(a_ton[..., None] > 0, ton, 0).astype(np.float32)
        rep[var] = dict(ruecken_rgb=rf.round(1).tolist(), ruecken_L=round(float(lum(rf)), 1))
    for arr in (a_ton, a_glatt, masken):                      # Schutzstreifen (PLAN 5.5): Maul-Flecken und Krallen nie anfassen
        arr[0:72, 0:548] = 0
        arr[12:32, 598:666] = 0
    os.makedirs(GS + "ebene", exist_ok=True)
    np.savez_compressed(EBENE, ton_braun=out["ton_braun"], ton_foto=out["ton_foto"], a_ton=a_ton.astype(np.float32),
                        a_glatt=a_glatt.astype(np.float32), strich_laenge=strich.astype(np.float32), masken=masken)
    # Masse der gemalten Kuppe/Nasenloecher/Augen im 3D (Texel-Lagen)
    def ausdehnung(m):
        if not m.any():
            return None
        Q = Pq[m]
        return dict(texel=int(m.sum()), breite_cm=round(float(Q[:, 1].max() - Q[:, 1].min()) * 100, 2),
                    hoehe_z_cm=round(float(Q[:, 2].max() - Q[:, 2].min()) * 100, 2), x=[round(float(Q[:, 0].min()), 3), round(float(Q[:, 0].max()), 3)],
                    hoehe_u_cm=round(float(h[m].max() - h[m].min()) * 100, 2), t_von=round(float(t[m].min()), 3))
    rep["kuppe"] = ausdehnung(kuppe > 0.5)
    rep["nasenloch_links"] = ausdehnung((loch > 0.5) & (y > 0))
    rep["nasenloch_rechts"] = ausdehnung((loch > 0.5) & (y < 0))
    rep["auge_links"] = ausdehnung((auge > 0.5) & (y > 0))
    rep["auge_rechts"] = ausdehnung((auge > 0.5) & (y < 0))
    rep["lippe_texel"] = int((lippe > 0.5).sum())
    rep["rinne_texel"] = int((rinne > 0.5).sum())
    json.dump(rep, open(EBENE + ".json", "w"), indent=1)
    # Vorschau der Ebene
    vis = np.zeros((S, S * 3, 3))
    vis[:, :S] = a_ton[..., None]
    vis[:, S:2 * S] = a_glatt[..., None]
    col = np.zeros((S, S, 3))
    col[..., 0] = np.maximum(kuppe, lippe)
    col[..., 1] = np.maximum(bruecke, loch)
    col[..., 2] = np.maximum(auge, ring * 0.5)
    vis[:, 2 * S:] = col
    Image.fromarray((np.clip(vis, 0, 1) * 255).astype(np.uint8)).resize((1536, 512)).save(GS + "ebene/gesicht_ebene_vorschau.png")
    print(json.dumps({k: v for k, v in rep.items() if k != "parameter"}, indent=0))


# ------------------------------------------------------------------------------------------------ Vorschau-Texturen (PLAN 5.4)
def vorschau(kv):
    C = np.load(KARTE)
    L, N, Tt = C["L"], C["N"], C["T"]
    Eb = np.load(EBENE)
    a_ton, a_glatt = Eb["a_ton"].astype(float), Eb["a_glatt"].astype(float)
    belegt = ~np.isnan(L[..., 0])
    aussen = belegt & (np.abs(np.nan_to_num(Tt[..., 0]) - 1) < 0.5)
    x, y, z = [np.nan_to_num(L[..., i], nan=-9) for i in range(3)]
    nz = np.nan_to_num(N[..., 2])
    nacken = kv.get("nacken", "1") == "1"
    os.makedirs(GS + "tex_vorschau", exist_ok=True)
    rep = {}
    for name, key in (("NCBearGen.png", "ton_braun"), ("NCBearGenFoto.png", "ton_foto")):
        alt = np.asarray(Image.open(GS + "eingang/" + name).convert("RGB")).astype(float)
        basis = mblur(alt, aussen, 6)
        detail = np.clip(lum(alt) / np.maximum(lum(basis), 4.0), 0.35, 2.2)
        # alte gemalte Kuppe/Augen/Lippe (dunkle Flecken) aus der Grundfarbe nehmen, sonst tragen ihre hellen Hoefe als "Fell" weiter
        dunkel = aussen & (lum(alt) < 0.5 * lum(basis))
        basis_s = mblur(alt, aussen & ~dunkel, 6)
        det_s = np.clip(lum(alt) / np.maximum(lum(basis_s), 4.0), 0.8, 1.2)      # alte helle Naht-Linien nicht verstaerken (nur Vorschau)
        det_s = np.where(dunkel, 1.0, det_s) ** (0.5 + 0.5 * Eb["strich_laenge"].astype(float))   # kurzes Fell im Gesicht: flacher
        detail = np.where(a_ton > 0, det_s, detail)
        nah_kuppe = box(((Eb["masken"] & 3) > 0).astype(float), 3) > 0      # alte Kuppen-Kontur nicht weitertragen (nur Vorschau)
        detail = np.where(nah_kuppe, 1.0, detail)
        ton = Eb[key].astype(float)
        neu_g = ton * (1 + (detail[..., None] - 1) * (1 - a_glatt[..., None]))
        img = alt * (1 - a_ton[..., None]) + neu_g * a_ton[..., None]
        if nacken:
            # NUR VORSCHAU (Nacken-Kragen gehoert FELL, PLAN 6.3): heller Ring hinter dem Kopf auf ~1,0 x Ruecken
            ruecken = aussen & (z > 0.85) & (x > -0.5) & (x < 0.5) & (nz > 0.6)
            Lr = np.median(lum(basis)[ruecken])
            b2 = mblur(img, aussen, 8)
            f = np.clip(1.0 * Lr / np.maximum(lum(b2), 4.0), 0.70, 1.0)
            w = sst(0.46, 0.56, x) * (1 - a_ton) * sst(0.60, 0.72, z) * aussen
            img = img * (1 - w[..., None] * (1 - f[..., None]))
        out = np.where(aussen[..., None], img, alt)
        # Aenderung 4 px in den Leerraum ziehen (gegen Saeume beim Filtern)
        d = out - alt
        m = aussen.astype(float)
        for _ in range(4):
            dn = box(d * m[..., None], 1) / np.maximum(box(m, 1), 1e-6)[..., None]
            mn = box(m, 1) > 0
            neu = mn & (m < 0.5) & ~belegt
            d = np.where(neu[..., None], dn, d)
            m = np.where(neu, 1.0, m)
        out = alt + d
        out[0:72, 0:548] = alt[0:72, 0:548]                    # Maul-Flecken-Streifen (PLAN 5.5)
        out[12:32, 598:666] = alt[12:32, 598:666]              # Krallen-Streifen
        out = np.clip(np.round(out), 0, 255).astype(np.uint8)
        Image.fromarray(out, "RGB").save(GS + "tex_vorschau/" + name)
        rep[name] = dict(geaendert_texel=int((np.abs(out.astype(int) - alt.astype(int)).max(-1) > 2).sum()))
    print(rep)


if __name__ == "__main__":
    cmd = sys.argv[1]
    kv = dict(a.split("=", 1) for a in sys.argv[2:])
    {"karten": lambda kv: karten(), "ebene": ebene, "vorschau": vorschau}[cmd](kv)
