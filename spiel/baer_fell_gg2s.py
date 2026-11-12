# SCHMAL-KOPIE (Lauf baer-gen-gross-v2-schmal, 12.11.2026) von baer_fell_gg2.py (md5 a765e3e5, Original unveraendert).
# Aenderungen: Gesichts-Daten aus v2/schmal/gesicht/ (GA), Ausgaben nach v2/schmal/fell/ (FE) und v2/out_schmal/ (OUT),
# Uebergabe-MD5 der SCHMAL-Ebene (sm_md5_setzen.py). Alles andere woertlich gleich (amp 0,156 wie NACHBESSERUNG).
# Lauf baer-gen-gross-v2 (12.11.2026), Rolle BAUER FELL + EXPORT (PLAN.md 6 + 7): Grundton nahtlos aus dem Netz, Unterarme/Beine in
# Fellfarbe statt Schwarz-Block, Nacken-Kragen weg, Fell mit gerichtetem Strichmuster aus der 3D-Lage (nahtlos ueber UV-Naehte),
# Zusammensetzen mit der Gesichts-Ebene (v2/gesicht/ebene/gesicht_ebene.npz, Vertrag PLAN 5.3), beide Farbvarianten, Leerraum fuellen.
# Kevin (12.11.2026): "ja mach den eignen model lauf wo du den verbesserst besonders sein gesicht (nase) die ist voll schmall und so".
# Statisch/offline, nicht gespielt. Schreibt nur unter _arbeit/baer_gen_gross/v2/fell/ und v2/out/ (nichts in Test-Mods, NPC Crew, Spiel).
# Rahmen: tier-Meter (x vorn, y links, z oben, Boden 0). Nur numpy + PIL (kein scipy auf diesem PC).
# Aufruf: python baer_fell_gg2.py <befehl> [k=v ...]
#   attr      Knochen-Gruppen je Texel rastern (UV unveraendert) -> fell/karten/_fell_attr.npz
#   grund     Grundton je verschweisstem Punkt (fix1-Mittel, Laplace, Regionen-Faktoren) -> fell/grund/grund_*.npy (+ Vorschau)
#   feld      Strich-Richtung, Strich-Laenge, Amplituden je Texel -> fell/struktur/feld.npz (+ Vorschau)
#   struktur  Strich-Synthese (3D-Rauschen, Linien-Integral entlang des Felds) -> fell/struktur/S.npy (+ Vorschau)
#   tex       Zusammensetzen beider Varianten, Leerraum fuellen -> fell/tex/NCBearGen.png, NCBearGenFoto.png
#   liefern   GLB + Texturen nach v2/out/42/media/... (Namen wie heute in NCBearTest) + md5.txt
import hashlib
import json
import os
import shutil
import sys
import time

import numpy as np
from PIL import Image

R = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_gross/"
V2 = R + "v2/"
GS = V2 + "gesicht/"
# NACHBESSERUNG (12.11.2026, v2/NACHBESSERUNG.md): Vorgabe ist der nachgebesserte Stand -- Gesichts-Daten aus v2/nachbesserung/gesicht/
# (GA), Ausgaben unter v2/nachbesserung/fell/. "nb=0" auf der Befehlszeile = Stand BAUER FELL (v2/gesicht/, v2/fell/; nicht neu schreiben).
NB = "nb=0" not in sys.argv
assert NB, "SCHMAL-Kopie: nb=0 nicht vorgesehen (Stand BAUER = Original-Skript)"
GA = V2 + "schmal/gesicht/"                              # SCHMAL
FE = V2 + "schmal/fell/"                                 # SCHMAL
OUT = V2 + "out_schmal/"                                 # SCHMAL (nie v2/out/)
sys.path.insert(0, R + "fix1/werkzeug")
S = 1024
LW = np.array([0.299, 0.587, 0.114])
# Uebergabe GESICHT (GESICHT.md 6) -- MD5 wird geprueft
UEBERGABE = {GS + "form/E_gg2_basis.npz": "56febeb105db21d0edb3eb948e0a1cec",
             GS + "gewichte/E_gg2_gewichte.npz": "597bebb5b7c78e7d486b9456fb49c06b",
             GS + "karten/_karten_gg2.npz": "4e37ed6126e09df546c83c1aa8e7c9b8",
             GS + "ebene/gesicht_ebene.npz": "ebfc0cb8d8627494de953cad054e42fc",
             GS + "eingang/NCBearGen.png": "bd6a335e2a44f61fc4ac4c115dbf6a21",
             GS + "eingang/NCBearGenFoto.png": "da159718c058ee705f8cb242f3331a2b"}
if NB:                                                   # Uebergabe NACHBESSERUNG (NACHBESSERUNG.md, Abschnitt Dateien)
    UEBERGABE = {GA + "form/E_gg2_basis.npz": "dc092a5e140ee4bec6c947d542323dd7",
                 GA + "gewichte/E_gg2_gewichte.npz": "9965d2baedd39245cdae01bc7ef7929e",
                 GA + "karten/_karten_gg2.npz": "c0460b68cd9cca6ce1212a2dcd019d23",
                 GA + "ebene/gesicht_ebene.npz": "ced2c7e112031309350d96376aa18d02",
                 GS + "eingang/NCBearGen.png": "bd6a335e2a44f61fc4ac4c115dbf6a21",
                 GS + "eingang/NCBearGenFoto.png": "da159718c058ee705f8cb242f3331a2b"}
KARTE = FE + "karten/_karten_gg2.npz"
ATTR = FE + "karten/_fell_attr.npz"
GRUPPEN = [("unterarm", ("Bip01_L_Forearm", "Bip01_R_Forearm")), ("hand", ("Bip01_L_Hand", "Bip01_R_Hand")),
           ("oberarm", ("Bip01_L_UpperArm", "Bip01_R_UpperArm")), ("unterschenkel", ("Bip01_L_Calf", "Bip01_R_Calf")),
           ("fuss", ("Bip01_L_Foot", "Bip01_R_Foot", "Bip01_L_Toe0", "Bip01_R_Toe0")), ("oberschenkel", ("Bip01_L_Thigh", "Bip01_R_Thigh")),
           ("hals", ("Bip01_Neck",)), ("kopf", ("Bip01_Head", "Bip01_Jaw")), ("brustwirbel", ("Bip01_Spine1",)), ("wirbel", ("Bip01_Spine",)),
           ("becken", ("Bip01_Pelvis",)), ("schwanz", ("Bip01_Tail",))]
GI = {g[0]: i for i, g in enumerate(GRUPPEN)}
SCHUTZ = [(slice(0, 72), slice(0, 548)), (slice(12, 32), slice(598, 666))]     # Maul-Flecken, Krallen-Streifen (PLAN 5.5): unveraendert
# Schnauzen-Achse (GESICHT/PLAN 2.1): a = Auge -> Spitze
A_SCHNAUZE = np.array([1.150 - 0.967, 0.0, 0.636 - 0.740])
A_SCHNAUZE /= np.linalg.norm(A_SCHNAUZE)


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def pruef_uebergabe():
    for p, m in UEBERGABE.items():
        assert md5(p) == m, ("Uebergabe GESICHT geaendert", p)
    assert md5(KARTE) == UEBERGABE[GA + "karten/_karten_gg2.npz"], "Karten-Kopie != GESICHT"


def sst(a, b, v):
    t = np.clip((np.asarray(v, float) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def lum(c):
    return c @ LW


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


def mblur(img, m, r=3):
    w = m.astype(float)
    num = box(box(box(img * w[..., None], r), r), r)
    den = box(box(box(w, r), r), r)
    return num / np.maximum(den, 1e-6)[..., None]


def lade_basis():
    B = np.load(GA + "form/E_gg2_basis.npz")
    G = np.load(GA + "gewichte/E_gg2_gewichte.npz")
    assert np.array_equal(B["V"], G["V"])
    return B, G


def normalen(V, T):
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    NL = np.zeros_like(V)
    for k in range(3):
        np.add.at(NL, T[:, k], fn)
    NL /= np.maximum(np.linalg.norm(NL, axis=1, keepdims=True), 1e-12)
    vol = np.einsum("ij,ij->i", V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum()
    return -NL if vol < 0 else NL


def raster_attr(attr):
    argv0 = sys.argv
    sys.argv = [argv0[0], GA + "form/E_gg2_basis.npz"]           # uv_maske laedt beim Import argv[1] (nur lesen)
    from uv_maske import raster
    sys.argv = argv0
    B = np.load(GA + "form/E_gg2_basis.npz")
    return raster(B["UV"], B["T_glb"], S, attr[B["glb_punkt"]])


def karte():
    C = np.load(KARTE)
    L, N, Tt, KR, X = C["L"], C["N"], C["T"], C["KR"], C["X"]
    belegt = ~np.isnan(L[..., 0])
    aussen = belegt & (np.abs(np.nan_to_num(Tt[..., 0]) - 1) < 0.5)
    return dict(L=L, N=N, T=Tt, KR=KR, X=X, belegt=belegt, aussen=aussen)


# ------------------------------------------------------------------------------------------------ attr (Knochen-Gruppen je Texel)
def attr(kv):
    pruef_uebergabe()
    B, G = lade_basis()
    nm = [str(n) for n in G["namen"]]
    W = G["W"]
    A = np.stack([sum(W[:, nm.index(b)] for b in bs) for _, bs in GRUPPEN], 1)
    t0 = time.time()
    Ar = raster_attr(A)
    os.makedirs(os.path.dirname(ATTR), exist_ok=True)
    np.savez_compressed(ATTR, W=Ar.astype(np.float32), namen=np.array([g[0] for g in GRUPPEN]))
    print("attr", Ar.shape, round(time.time() - t0, 1), "s")


# ------------------------------------------------------------------------------------------------ grund (PLAN 6.3)
# Faktoren relativ zum eigenen Ruecken (Luminanz), Ziel laut PLAN 6.3 (Tabelle). Unterarm-Verlauf Ellbogen -> Handgelenk ueber die Hoehe z
# der Ruhe (2c-Ruhe: Ellbogen z ~0,41-0,45, Handgelenk ~0,12, Pfote darunter -- R/fix1/werkzeug/tex_fix1.py seg_abst).
PG = dict(lap=8, lam=0.5, brust=0.90, bauch=0.68, oberarm=0.87, achsel=0.84, oberschenkel=0.82, ua_ell=0.68, ua_hg=0.58, ua_innen=0.05,
          pfote=0.50, us_knie=0.66, us_hg=0.57, fuss=0.50, nacken_o=1.00, nacken_s=0.90, nacken_u=0.88, bein_chroma=0.6, flanke_max=0.95,
          kopf_rand=0.97, ohr=0.90, ohr_innen=0.06, kehle_plus=0.06)


def nachbar_kanten(T, frei):
    E = np.sort(np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]])), 1)
    E = np.unique(E, axis=0)
    ok = frei[E[:, 0]] & frei[E[:, 1]]
    return E[ok, 0], E[ok, 1]


def laplace(F, ei, ej, n, schritte, lam, frei):
    for _ in range(schritte):
        acc = np.zeros_like(F)
        cnt = np.zeros(n)
        np.add.at(acc, ei, F[ej])
        np.add.at(acc, ej, F[ei])
        np.add.at(cnt, ei, 1)
        np.add.at(cnt, ej, 1)
        ok = frei & (cnt > 0)
        avg = acc[ok] / cnt[ok][:, None]
        F[ok] = F[ok] + lam * (avg - F[ok])
    return F


def punkt_masken(V, NL, W, nm_g, B):
    """weiche Regionen-Masken je verschweisstem Punkt (Ruhe-Lage, Knochen-Gruppen, Normale)."""
    g = {k: W[:, i] for k, i in nm_g.items()}
    x, y, z = V[:, 0], V[:, 1], V[:, 2]
    nx, ny, nz = NL[:, 0], NL[:, 1], NL[:, 2]
    ay = np.abs(y)
    m = {}
    bein_u = np.clip(g["unterarm"] + g["hand"] + g["unterschenkel"] + g["fuss"], 0, 1)
    m["bein"] = bein_u
    # Brust vorn (Spine1/Neck, vorn-unten, unter dem Hals), Bauch (Unterseite)
    m["brust"] = np.clip(g["brustwirbel"] + g["hals"], 0, 1) * sst(0.25, 0.40, z) * (1 - sst(0.70, 0.80, z)) * sst(0.0, 0.4, nx - 0.5 * nz) \
        * (1 - sst(0.18, 0.28, ay)) * (1 - g["kopf"]) * (1 - bein_u)
    m["bauch"] = sst(0.15, 0.45, -nz) * sst(-0.60, -0.45, x) * (1 - sst(0.15, 0.30, x)) * (1 - sst(0.50, 0.60, z)) * (1 - bein_u)
    m["oberarm"] = g["oberarm"]
    m["oberschenkel"] = g["oberschenkel"] * (1 - bein_u)
    # Achsel innen: Uebergang Oberarm -> Brust/Rumpf an der Innenseite (|y| klein) -- das "Wellenband" beim Aufrichten
    m["achsel"] = np.clip(4 * g["oberarm"] * (1 - g["oberarm"]), 0, 1) * (1 - sst(0.20, 0.28, ay)) * (1 - g["kopf"])
    m["achsel"] = np.maximum(m["achsel"], sst(0.15, 0.6, g["oberarm"]) * (1 - sst(0.17, 0.25, ay)) * (1 - g["kopf"]))
    m["unterarm"] = g["unterarm"]
    m["hand"] = g["hand"]
    m["unterschenkel"] = g["unterschenkel"]
    m["fuss"] = g["fuss"]
    innen = sst(0.1, 0.5, -ny * np.sign(y))                          # Innenseite der Beine (zur Koerpermitte)
    m["innen"] = innen
    # Nacken/Hals-Kragen hinter dem Kopf (bis zur Gesichts-Ebene, die bei x 0,70-0,80 einblendet)
    m["nacken"] = sst(0.46, 0.56, x) * (1 - bein_u) * (1 - m["brust"]) * sst(0.40, 0.55, z)
    m["sohle"] = B["sohle"].astype(float)
    m["ohr"] = (B["ohr_l"] | B["ohr_r"]).astype(float) * sst(0.06, 0.09, ay)
    return m


def grund(kv):
    pruef_uebergabe()
    P = dict(PG)
    P.update({k: float(v) for k, v in kv.items()})
    B, G = lade_basis()
    V, T, gp, UV = B["V"], B["T"], B["glb_punkt"], B["UV"]
    n = len(V)
    tp = B["teil_punkt"].astype(str)
    aussen_p = tp == "aussen"
    NL = normalen(V, T)
    nm = [str(s) for s in G["namen"]]
    W = np.stack([sum(G["W"][:, nm.index(b)] for b in bs) for _, bs in GRUPPEN], 1)
    K = karte()
    m = punkt_masken(V, NL, W, GI, B)
    ruecken_p = aussen_p & (V[:, 2] > 0.85) & (V[:, 0] > -0.5) & (V[:, 0] < 0.5) & (NL[:, 2] > 0.6)
    ei, ej = nachbar_kanten(T, aussen_p)
    rep = {"parameter": P}
    os.makedirs(FE + "grund", exist_ok=True)
    for var, pfad in (("braun", GS + "eingang/NCBearGen.png"), ("foto", GS + "eingang/NCBearGenFoto.png")):
        img = np.asarray(Image.open(pfad).convert("RGB")).astype(float)
        bl = mblur(img, K["aussen"], 3)                              # ~1 cm weich, nur Haut-Texel
        uvp = np.clip((UV * S).astype(int), 0, S - 1)
        cg = bl[uvp[:, 1], uvp[:, 0]]                                # je GLB-Punkt (Bildzeile = v von oben)
        C = np.zeros((n, 3))
        cnt = np.zeros(n)
        np.add.at(C, gp, cg)
        np.add.at(cnt, gp, 1)
        C = C / np.maximum(cnt, 1)[:, None]
        C = laplace(C, ei, ej, n, int(P["lap"]), P["lam"], aussen_p)
        rf = np.median(C[ruecken_p], 0)
        Lr = lum(rf)
        Lc = np.maximum(lum(C), 1.0)
        F = Lc / Lr                                                   # Ist-Faktor (glatt)
        chroma = C / Lc[:, None]
        F0 = F.copy()
        # Regionen-Faktoren (PLAN 6.3), nacheinander weich eingeblendet
        F = F + (P["brust"] - F) * m["brust"]
        F = F + (P["bauch"] - F) * m["bauch"]
        F = np.minimum(F, P["flanke_max"] + (F - P["flanke_max"]) * (V[:, 2] > 0.9))   # Flanke nicht heller als 0,95
        F = F + (P["oberschenkel"] - F) * m["oberschenkel"]
        F = F + (P["oberarm"] - F) * m["oberarm"]
        F = F + (P["achsel"] - F) * m["achsel"]
        f_ua = P["ua_hg"] + (P["ua_ell"] - P["ua_hg"]) * sst(0.12, 0.42, V[:, 2]) + P["ua_innen"] * m["innen"]
        F = F + (f_ua - F) * m["unterarm"]
        F = F + (P["pfote"] + 0.03 * m["innen"] - F) * m["hand"]
        f_us = P["us_hg"] + (P["us_knie"] - P["us_hg"]) * sst(0.12, 0.42, V[:, 2]) + 0.03 * m["innen"]
        F = F + (f_us - F) * m["unterschenkel"]
        F = F + (P["fuss"] + 0.03 * m["innen"] - F) * m["fuss"]
        nz = NL[:, 2]
        f_u = P["nacken_u"] + P["kehle_plus"] * sst(0.60, 0.78, V[:, 0])      # Kehle zum Kinn hin heller (Ebene dort ~0,94)
        f_n = f_u + (P["nacken_s"] - f_u) * sst(-0.7, 0.0, nz) + (P["nacken_o"] - P["nacken_s"]) * sst(0.0, 0.7, nz)
        F = F + (f_n - F) * m["nacken"]
        # Kopf ausserhalb der Gesichts-Ebene (Ohr-Lappen, Hinterkopf-Rand): Rumpfton, nicht heller als kopf_rand
        kopf = W[:, GI["kopf"]]
        F = F + (np.minimum(F, P["kopf_rand"]) - F) * kopf
        # Ohr-Lappen (Maske wie GESICHT: Ohr-Flag und |y| > 6-9 cm): Fellton etwas dunkler, Innenseite (nach vorn) dunkler -> keine helle Scheibe
        f_o = P["ohr"] - P["ohr_innen"] * sst(0.2, 0.6, NL[:, 0])
        F = F + (f_o - F) * m["ohr"]
        # Farbe: Beine dunkelbraun (braun: Farbton/Saettigung des Rueckens), Fototon behaelt seinen Ton
        ch_r = rf / Lr
        wch = np.clip(P["bein_chroma"] * (m["bein"] + 0.5 * m["oberarm"]), 0, 1) if var == "braun" else 0.25 * m["bein"]
        chroma = chroma * (1 - np.asarray(wch)[:, None]) + ch_r[None, :] * np.asarray(wch)[:, None]
        Cn = chroma * (F * Lr)[:, None]
        Cn = laplace(Cn, ei, ej, n, 2, 0.5, aussen_p)                # Masken-Kanten nachglaetten
        Gr = raster_attr(Cn)
        np.save(FE + "grund/grund_%s.npy" % var, Gr.astype(np.float32))
        # Bericht: Punkt-Faktoren je Region (Mittel der Punkte mit Maske > 0,5)
        Fn = lum(Cn) / Lr
        rr = {}
        for k in ("brust", "bauch", "oberarm", "achsel", "unterarm", "hand", "unterschenkel", "fuss", "oberschenkel", "nacken"):
            mm = aussen_p & (m[k] > 0.5)
            rr[k] = [round(float(F0[mm].mean()), 3), round(float(Fn[mm].mean()), 3), int(mm.sum())]
        rep[var] = dict(ruecken_rgb=rf.round(1).tolist(), ruecken_L=round(float(Lr), 1), regionen_vorher_nachher_n=rr)
        vis = np.nan_to_num(Gr, nan=0)
        Image.fromarray(np.clip(vis, 0, 255).astype(np.uint8)).save(FE + "grund/grund_%s.png" % var)
    json.dump(rep, open(FE + "grund/grund.json", "w"), indent=1)
    print(json.dumps(rep, indent=0))


# ------------------------------------------------------------------------------------------------ Rauschen (3D, ganzzahliger Hash)
def _hash(ix, iy, iz, seed):
    h = (ix.astype(np.uint32) * np.uint32(73856093)) ^ (iy.astype(np.uint32) * np.uint32(19349663)) ^ \
        (iz.astype(np.uint32) * np.uint32(83492791)) ^ np.uint32(seed)
    h ^= h >> np.uint32(13)
    h *= np.uint32(0x5BD1E995)
    h ^= h >> np.uint32(15)
    h *= np.uint32(0x27D4EB2F)
    h ^= h >> np.uint32(16)
    return h.astype(np.float64) / 4294967296.0


def vnoise(Q, zelle, seed):
    """Wert-Rauschen 3D, trilinear mit glatter Ueberblendung, Werte 0..1 (Mittel 0,5). zelle: Skalar oder je Punkt."""
    q = Q / np.asarray(zelle)[..., None] if np.ndim(zelle) else Q / zelle
    i = np.floor(q)
    f = q - i
    f = f * f * (3 - 2 * f)
    i = i.astype(np.int64)
    out = np.zeros(len(Q))
    for dx in (0, 1):
        wx = f[:, 0] if dx else 1 - f[:, 0]
        for dy in (0, 1):
            wy = f[:, 1] if dy else 1 - f[:, 1]
            for dz in (0, 1):
                wz = f[:, 2] if dz else 1 - f[:, 2]
                out += wx * wy * wz * _hash(i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz, seed)
    return out


_GR = np.array([[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1], [1, 0, -1], [-1, 0, -1],
                [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1], [1, 1, 0], [-1, 1, 0], [0, -1, 1], [0, -1, -1]], float)


def gnoise(Q, zelle, seed):
    """Gradienten-Rauschen 3D (Perlin, 5. Ordnung Ueberblendung), Werte ca. -1..1 (Mittel 0) -- runde Flecken statt Wuerfel."""
    q = Q / np.asarray(zelle)[..., None] if np.ndim(zelle) else Q / zelle
    i = np.floor(q)
    f = q - i
    u = f * f * f * (f * (f * 6 - 15) + 10)
    i = i.astype(np.int64)
    out = np.zeros(len(Q))
    for dx in (0, 1):
        wx = u[:, 0] if dx else 1 - u[:, 0]
        for dy in (0, 1):
            wy = u[:, 1] if dy else 1 - u[:, 1]
            for dz in (0, 1):
                wz = u[:, 2] if dz else 1 - u[:, 2]
                hsh = (_hash(i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz, seed) * 16).astype(np.int64) & 15
                g = _GR[hsh]
                out += wx * wy * wz * ((f[:, 0] - dx) * g[:, 0] + (f[:, 1] - dy) * g[:, 1] + (f[:, 2] - dz) * g[:, 2])
    return out


# ------------------------------------------------------------------------------------------------ Strich-Synthese (PLAN 6.5)
# Straehnen ("Kometen"): duenne Flecken im 3D-Rauschen, entlang der Strich-Richtung zur Spitze hin heller gezogen (Maximum, damit
# einzelne Straehnen lesbar bleiben), kurzer Schatten hinter der Spitze. Haare: kurzes symmetrisches Linien-Integral feinen Rauschens.
PS = dict(k_str=16, k_sch=4, sch=0.30, sch_lang=0.22, spot_zelle=0.0140, spot_schwelle=0.20, spot_breite=0.16, spitz=0.22, wurzel=0.55,
          welle=0.45, welle_zelle=0.07, haar_zelle=0.0026, haar_k=6, haar_laenge=0.016, w_str=0.80, w_haar=0.45, var_zelle=0.06, var=0.30,
          band_zelle=0.025, band_k=8, band_lang=1.3, w_band=0.35, seed=1234)


def struktur_punkte(P, D, Lc, haar_amp, par, zelle_f=None, N=None, chunk=50000):
    """S je Punkt (Mittel 0, Std ~1). P Lage, D Strich-Richtung (Einheit, tangential), Lc Straehnen-Laenge (m), N Normale (fuer die Welle)."""
    n = len(P)
    st = np.zeros(n)
    ha = np.zeros(n)
    bd = np.zeros(n)
    K, Ks = int(par["k_str"]), int(par["k_sch"])
    Kh = int(par["haar_k"])
    seed = int(par["seed"])
    for a in range(0, n, chunk):
        b = min(n, a + chunk)
        p, d, lc = P[a:b], D[a:b].copy(), Lc[a:b]
        if par["welle"] > 0:                                          # Strich leicht wellig: Richtung mit glattem 3D-Rauschen drehen
            jit = np.stack([gnoise(p, par["welle_zelle"], seed + 11 + j) for j in range(3)], 1)
            if N is not None:
                nn = N[a:b]
                jit = jit - (jit * nn).sum(1, keepdims=True) * nn
            d = d + par["welle"] * jit
            d /= np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-9)
        zs = par["spot_zelle"] * (zelle_f[a:b] if zelle_f is not None else 1.0)
        best = np.zeros(b - a)
        for k in range(K + 1):
            q = p - (lc * k / K)[:, None] * d
            thr = par["spot_schwelle"] + par["spitz"] * (k / K) ** 1.5        # zur Spitze hin schmaler (spitz zulaufend)
            sp = sst(thr, thr + par["spot_breite"], gnoise(q, zs, seed))
            w = par["wurzel"] + (1 - par["wurzel"]) * (k / K)
            best = np.maximum(best, w * sp)
        sch = np.zeros(b - a)
        for k in range(1, Ks + 1):
            q = p - (lc * (1 + par["sch_lang"] * k / Ks))[:, None] * d
            thr = par["spot_schwelle"] + par["spitz"]
            sp = sst(thr, thr + par["spot_breite"], gnoise(q, zs, seed))
            sch = np.maximum(sch, sp * (1 - 0.5 * (k - 1) / Ks))
        v = 1 - par["var"] + 2 * par["var"] * vnoise(p, par["var_zelle"], seed + 7)    # Straehnen-Kontrast leicht wechselnd
        st[a:b] = (best - par["sch"] * sch * (1 - best)) * v
        acc = np.zeros(b - a)
        lh = par["haar_laenge"] * np.sqrt(np.clip(lc / 0.05, 0.2, 1.0))
        for k in range(-Kh, Kh + 1):
            q = p + (lh * k / (2 * Kh))[:, None] * d
            acc += vnoise(q, par["haar_zelle"], seed + 3)
        ha[a:b] = acc / (2 * Kh + 1)
        # breite Straehnen-Baender (hell/dunkel entlang des Strichs, 2-3 cm breit): lesbar auch bei Textur 256 und in Spielgroesse
        acc = np.zeros(b - a)
        Kb = int(par["band_k"])
        zb = par["band_zelle"] * (zelle_f[a:b] if zelle_f is not None else 1.0)
        for k in range(-Kb, Kb + 1):
            q = p + (lc * par["band_lang"] * k / (2 * Kb))[:, None] * d
            acc += gnoise(q, zb, seed + 5)
        bd[a:b] = acc / (2 * Kb + 1)
    info = dict(str_mittel=round(float(st.mean()), 4), str_std=round(float(st.std()), 4), haar_std=round(float(ha.std()), 4),
                str_bedeckt=round(float((st > 0.3).mean()), 3))
    st = (st - st.mean()) / max(st.std(), 1e-9)
    ha = (ha - ha.mean()) / max(ha.std(), 1e-9)
    bd = (bd - bd.mean()) / max(bd.std(), 1e-9)
    Sx = par["w_str"] * st + par["w_haar"] * ha * haar_amp + par["w_band"] * bd
    return Sx, info


# ------------------------------------------------------------------------------------------------ feld (PLAN 6.4)
PF = dict(l_rumpf=0.065, l_bein=0.65, l_oben_bein=0.85, fuss_zelle=0.7, l_kopf=0.5, l_ohr=0.30, amp_ohr=0.8, amp_kopf=0.90)


def feld(kv):
    pruef_uebergabe()
    P = dict(PF)
    P.update({k: float(v) for k, v in kv.items()})
    K = karte()
    A = np.load(ATTR)["W"]
    Eb = np.load(GA + "ebene/gesicht_ebene.npz")
    L, N, KR, Tt = K["L"], K["N"], K["KR"], K["T"]
    au = K["aussen"]
    x, y, z = [np.nan_to_num(L[..., i]) for i in range(3)]
    nx, ny, nz = [np.nan_to_num(N[..., i]) for i in range(3)]
    t, h = np.nan_to_num(KR[..., 0], nan=-9), np.nan_to_num(KR[..., 1], nan=-9)
    g = {k: np.clip(np.nan_to_num(A[..., i]), 0, 1) for k, i in GI.items()}
    ay = np.abs(y)
    bein = np.clip(g["unterarm"] + g["hand"] + g["unterschenkel"] + g["fuss"], 0, 1)
    oben_bein = np.clip(g["oberarm"] + g["oberschenkel"], 0, 1) * (1 - bein)
    kopf = g["kopf"]
    ohr = np.clip(np.nan_to_num(Tt[..., 1]), 0, 1) * sst(0.06, 0.09, ay)
    sohle = np.clip(np.nan_to_num(Tt[..., 2]), 0, 1)

    def vec(a, b, c):
        return np.broadcast_to(np.array([a, b, c], float), x.shape + (3,))

    def lerp(D, D2, w):
        return D + (D2 - D) * w[..., None]
    D = vec(-1, 0, -0.45)                                                         # Rumpf: nach hinten-unten
    D = lerp(D, vec(-1, 0, -0.85), sst(0.45, 0.85, np.abs(ny)) * (1 - bein))      # Flanke staerker nach unten
    unten = np.maximum(sst(0.2, 0.6, -nz), sst(0.3, 0.7, nx) * (1 - sst(0.72, 0.82, z)) * (1 - kopf))
    D = lerp(D, vec(-0.3, 0, -1), unten * (1 - bein))                             # Brust/Bauch
    D = lerp(D, vec(-0.35, 0, -1), oben_bein)                                    # Oberarm/Oberschenkel
    D = lerp(D, vec(0, 0, -1), bein)                                             # Beine nach unten
    D = lerp(D, vec(-1, 0, -0.1), g["hals"] * (1 - unten) * (1 - kopf))           # Nacken
    D = lerp(D, vec(-1, 0, -0.1), kopf)                                          # Oberkopf
    sy = np.sign(y)
    Dw = np.stack((np.full_like(x, -0.7), 0.3 * sy, np.full_like(x, -0.6)), -1)
    wange = kopf * (1 - sst(0.05, 0.25, t)) * sst(0.06, 0.10, ay) * sst(0.0, 0.04, -h)
    D = lerp(D, Dw, wange)
    schn = kopf * sst(0.05, 0.25, t)
    D = lerp(D, np.broadcast_to(-A_SCHNAUZE, x.shape + (3,)), schn)               # Schnauze: von der Kuppe zu den Augen
    D = lerp(D, vec(0.15, 0, 1), ohr)                                            # Ohr: kurz, zum Rand hin
    D = np.array(D)
    Nn = np.stack((nx, ny, nz), -1)
    Dt = D - (D * Nn).sum(-1, keepdims=True) * Nn
    mag = np.linalg.norm(Dt, axis=-1)
    fb = np.array([-1.0, 0, 0])[None, None, :] - Nn[..., 0:1] * Nn                # Ersatz, wo das Feld senkrecht zur Haut steht
    Dt = Dt + fb * (1 - sst(0.15, 0.35, mag))[..., None]
    Dt /= np.maximum(np.linalg.norm(Dt, axis=-1, keepdims=True), 1e-9)
    sl = Eb["strich_laenge"].astype(float)
    sl = np.where(sl > 0, sl, 1.0)
    sl = np.minimum(sl, 1 - (1 - P["l_kopf"]) * kopf)                            # ganzer Kopf kurz (auch um die Ohren, wo die Ebene 1 hat)
    sl = sl + (P["l_ohr"] - sl) * ohr
    Lc = P["l_rumpf"] * sl ** 0.7 * (1 - (1 - P["l_bein"]) * bein) * (1 - (1 - P["l_oben_bein"]) * oben_bein)
    # Strich-Amplitude: Ohr-Lappen kurz und etwas schwaecher (sonst glatte helle "Scheibe"), Sohle ohne; glatte Stellen der Ebene in tex
    amp = (1 - (1 - P["amp_ohr"]) * ohr) * (1 - sohle) * (1 - (1 - P["amp_kopf"]) * kopf)   # Kopf feiner -> etwas leiser (HP3 wie Nacken)
    zelle_f = sl * (1 - (1 - P["fuss_zelle"]) * bein * 0.5)                      # kurze Straehnen (Kopf, Ohr) schmaler als kuerzer: schlank
    # Texel-Groesse (m) aus der Lage-Karte (fuer Haar-Dichte: zu feines Rauschen flimmert sonst)
    du = np.linalg.norm(np.diff(np.nan_to_num(L), axis=1), axis=-1)
    dv = np.linalg.norm(np.diff(np.nan_to_num(L), axis=0), axis=-1)
    du = np.minimum(np.pad(du, ((0, 0), (0, 1)), mode="edge"), np.pad(du, ((0, 0), (1, 0)), mode="edge"))
    dv = np.minimum(np.pad(dv, ((0, 1), (0, 0)), mode="edge"), np.pad(dv, ((1, 0), (0, 0)), mode="edge"))
    fp = np.sqrt(np.clip(du, 0, 0.05) * np.clip(dv, 0, 0.05))
    haar_amp = amp * (1 - sst(0.0040, 0.0070, fp))
    os.makedirs(FE + "struktur", exist_ok=True)
    np.savez_compressed(FE + "struktur/feld.npz", D=Dt.astype(np.float32), Lc=Lc.astype(np.float32), amp=amp.astype(np.float32),
                        haar_amp=haar_amp.astype(np.float32), zelle_f=zelle_f.astype(np.float32), fp=fp.astype(np.float32))
    vis = (Dt * 0.5 + 0.5) * au[..., None]
    Image.fromarray((vis * 255).astype(np.uint8)).save(FE + "struktur/feld_richtung.png")
    rep = dict(parameter=P, texel_mm_median=round(float(np.median(fp[au]) * 1000), 2), texel_mm_p95=round(float(np.percentile(fp[au], 95) * 1000), 2),
               haar_amp_unter_05=round(float((haar_amp[au] < 0.5).mean()), 3), ersatz_richtung=round(float((mag[au] < 0.25).mean()), 4))
    json.dump(rep, open(FE + "struktur/feld.json", "w"), indent=1)
    print(rep)


def struktur(kv):
    pruef_uebergabe()
    P = dict(PS)
    P.update({k: float(v) for k, v in kv.items()})
    K = karte()
    Fd = np.load(FE + "struktur/feld.npz")
    au = K["aussen"]
    ii = np.nonzero(au)
    Pp = K["L"][ii]
    t0 = time.time()
    Sx, info = struktur_punkte(Pp, Fd["D"][ii].astype(float), Fd["Lc"][ii].astype(float), Fd["haar_amp"][ii].astype(float), P,
                               zelle_f=Fd["zelle_f"][ii].astype(float), N=np.nan_to_num(K["N"][ii]))
    Simg = np.zeros((S, S), np.float32)
    Simg[ii] = Sx
    np.save(FE + "struktur/S.npy", Simg)
    vis = np.clip(128 + 40 * Simg, 0, 255) * au
    Image.fromarray(vis.astype(np.uint8)).save(FE + "struktur/S.png")
    info.update(parameter=P, sekunden=round(time.time() - t0, 1), texel=int(au.sum()))
    json.dump(info, open(FE + "struktur/S.json", "w"), indent=1)
    print(info)


# ------------------------------------------------------------------------------------------------ tex (PLAN 6.6)
PT = dict(amp=0.153, rand=3)
if NB:
    PT["amp"] = 0.156                            # NACHBESSERUNG: Schnauze halb so stark (O2-04) senkt HP3 -> Gesamt-Amplitude +2 % (HP3 >= 11)


def fuellen(out, belegt, alt):
    """Insel-Rand 3 px nach aussen ziehen, Rest push-pull (Fellton); Schutzstreifen bleiben wie fix1."""
    m = belegt.astype(float)
    d = out.copy()
    for _ in range(int(PT["rand"])):
        dn = box(d * m[..., None], 1) / np.maximum(box(m, 1), 1e-6)[..., None]
        neu = (box(m, 1) > 0) & (m < 0.5)
        d = np.where(neu[..., None], dn, d)
        m = np.where(neu, 1.0, m)
    quelle = m > 0.5
    lv = [(d * quelle[..., None], quelle.astype(float))]
    while lv[-1][1].shape[0] > 1:
        a_, w_ = lv[-1]
        h_ = a_.shape[0] // 2
        lv.append((a_.reshape(h_, 2, h_, 2, 3).sum((1, 3)), w_.reshape(h_, 2, h_, 2).sum((1, 3))))
    farbe = lv[-1][0] / np.maximum(lv[-1][1], 1e-9)[..., None]
    for a_, w_ in reversed(lv[:-1]):
        up = np.repeat(np.repeat(farbe, 2, 0), 2, 1)
        farbe = np.where(w_[..., None] > 0, a_ / np.maximum(w_, 1e-9)[..., None], up)
    weich = mblur(np.where(quelle[..., None], d, farbe), np.ones(belegt.shape, bool), 4)
    d = np.where(quelle[..., None], d, weich)
    for ys, xs in SCHUTZ:
        d[ys, xs] = alt[ys, xs]
    return d


def tex(kv):
    pruef_uebergabe()
    P = dict(PT)
    aus = kv.pop("aus", FE + "tex/")
    P.update({k: float(v) for k, v in kv.items()})
    K = karte()
    au, belegt = K["aussen"], K["belegt"]
    Tt = K["T"]
    sohle = np.clip(np.nan_to_num(Tt[..., 2]), 0, 1)
    Eb = np.load(GA + "ebene/gesicht_ebene.npz")
    a_ton, a_glatt = Eb["a_ton"].astype(float), Eb["a_glatt"].astype(float)
    Fd = np.load(FE + "struktur/feld.npz")
    Sx = np.load(FE + "struktur/S.npy").astype(float) * Fd["amp"].astype(float)
    os.makedirs(aus, exist_ok=True)
    rep = {"parameter": P}
    for name, var, key in (("NCBearGen.png", "braun", "ton_braun"), ("NCBearGenFoto.png", "foto", "ton_foto")):
        alt = np.asarray(Image.open(GS + "eingang/" + name).convert("RGB")).astype(float)
        Gr = np.nan_to_num(np.load(FE + "grund/grund_%s.npy" % var).astype(float))
        g = Gr * (1 - a_ton[..., None]) + Eb[key].astype(float) * a_ton[..., None]
        f = 1 + P["amp"] * Sx * (1 - a_glatt)
        neu = g * np.clip(f, 0.2, 2.0)[..., None]
        # Sohle/Ballen bleiben wie fix1 (PLAN 6.3 'bleibt'), weich ueber den Sohlen-Anteil
        ws = sst(0.2, 0.8, sohle)[..., None]
        neu = neu * (1 - ws) + alt * ws
        out = np.where(au[..., None], neu, alt)                         # Maul innen / Krallen (Teil 2/3) unveraendert
        out = fuellen(out, belegt, alt)
        out = np.clip(np.round(out), 0, 255).astype(np.uint8)
        Image.fromarray(out, "RGB").save(aus + name)
        rep[name] = dict(md5=md5(aus + name), geaendert_texel=int((np.abs(out.astype(int) - alt.astype(int)).max(-1) > 2).sum()))
    json.dump(rep, open(aus + "tex.json", "w"), indent=1)
    print(rep)


# ------------------------------------------------------------------------------------------------ liefern (PLAN 7)
def liefern(kv):
    pruef_uebergabe()
    ziel = {"42/media/models_X/Skinned/NCBearGen.glb": FE + "glb/NCBearGen.glb",
            "42/media/textures/Body/NCBearGen.png": FE + "tex/NCBearGen.png",
            "42/media/textures/Body/NCBearGenFoto.png": FE + "tex/NCBearGenFoto.png"}
    zeilen = []
    for rel, q in ziel.items():
        os.makedirs(os.path.dirname(OUT + rel), exist_ok=True)
        shutil.copyfile(q, OUT + rel)
        assert md5(OUT + rel) == md5(q)
        zeilen.append("%s *%s" % (md5(OUT + rel), rel))
    with open(OUT + "md5.txt", "w", newline="\n") as fh:
        fh.write("\n".join(zeilen) + "\n")
    for wurzel, _, dateien in os.walk(OUT + "42"):
        for d in dateien:
            assert not d.endswith(".npy"), ("perm.npy unter out/42", wurzel, d)
    print("\n".join(zeilen))


if __name__ == "__main__":
    cmd = sys.argv[1]
    kv = dict(a.split("=", 1) for a in sys.argv[2:])
    kv.pop("nb", None)
    {"attr": attr, "grund": grund, "feld": feld, "struktur": struktur, "tex": tex, "liefern": liefern}[cmd](kv)
