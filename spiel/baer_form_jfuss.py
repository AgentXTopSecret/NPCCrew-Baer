# Lauf baer-junges-fuss (11.11.2026), Bauer FORM: Kopie von baer_form_baby.py (MD5 4e8f205b, unveraendert gelassen). Geaendert:
#   - Konstanten DUMP/GLB_ALT/TEX_ALT/ARB zeigen NUR auf feste Kopien (_arbeit/baer_junges_fuss/quelle, plan/dump): Erwachsener = 2c-Baer
#     (NCBear.glb 08ec7806, Importer-Dump plan/dump/dump_2c.txt); NCBearTest wird nicht mehr gelesen (PLAN_JFUSS.md 0.7).
#   - 2c-Skelett = pfote-Skelett (Dump-Offsets gleich, 0,0), daher ergibt Junges(E_2c) bit-gleich das Skelett von heute (fix1.npz BW).
#   - neu unten: rumpf_feld/rumpf_ausgleich (Rumpf-Querschnitte wie heute, Beine wie 2c), ring_angleich (Koerperrand auf den heutigen
#     geglaetteten Rand), pranke_vorn (Vorderpranken optional kleiner), Kopf-Teile fest aus fix1.npz (kopf_fest_laden).
# Davor Lauf baer-baby (10.11.2026): Form des Baer-Jungen (Entwurf) -- Skelett, Koerper-Proportionen, Kopf-Form als implizite Flaeche.
# Nur numpy; wird von baer_netz_baby.py (Blender), baer_textur_baby.py, baer_export_baby.py und den Mess-/Render-Werkzeugen geladen.
# Grundlage Erwachsener: NCBearTest NCBear.glb MD5 5066fa67 (nur gelesen) bzw. dessen Dump des Spiel-Importers
# _arbeit/baer_pfote/fix1/bau4/dump_final.txt.pkl (Kette fix1/log/kette13.txt:13-14 belegt dieselbe MD5).
# Soll: _arbeit/baer_baby/SPEZ_BABY.md (4.1 Kopf, 4.2 Teile, 4.4 Koerper, 4.5 Technik), werkzeug/ziel_kopf.json.
# Neu gebaut (nicht aus *_pfote.py kopiert): der Pfoten-Weg (Hochmodell, Surface Nets, Huelle, Backen) wird fuer das Junge nicht
# gebraucht -- der Koerper ist das heutige Spielnetz mit Junges-Proportionen (SPEZ 4.4/4.5), nur der Kopf ist neu.
# Statisch/offline, nicht gespielt.
#
# Raeume:
#   dump  = Modellraum des Importers (Dump.java, MAKE_LEFT_HANDED): Einheiten 0,544 je Meter
#   gltf  = Raum der GLB-Datei: (x, y, -z) des Dump-Raums
#   tier  = Meter, x vorn, y links, z oben: tier = (-z_d, x_d, y_d) / 0,544  (wie mess_kopf.py tier)
#   kopf  = Kopf-Rahmen in Einheiten der Kopfbreite W, Ursprung Augenmitte, x vorn entlang der Kopfachse, y links, z oben (SPEZ 4.1)
import json
import math
import os
import pickle
import struct

import numpy as np

M2U = 0.544
QUELLE = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges_fuss/quelle/"
DUMP = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges_fuss/plan/dump/dump_2c.txt.pkl"   # Importer-Dump von quelle/2c/NCBear.glb
GLB_ALT = QUELLE + "2c/NCBear.glb"                  # 08ec7806 (feste Kopie, nur lesen)
TEX_ALT = QUELLE + "2c/NCBear_body1024.png"         # 4cfdb177 (feste Kopie, nur lesen)
GLB_JUNGES = QUELLE + "cub/NCBearCub.glb"          # 6c3f0a96 (Gerippe, Kopf-Quelle)
NETZ_HEUTE = QUELLE + "baby_netz/fix1.npz"          # 5ecead50 = Netz von 6c3f0a96 (byte-gleich geprueft: POSITION/UV/Gewichte/Indizes)
PARAM_HEUTE = QUELLE + "baby_netz/fix1.json"        # 2734716b
ARB = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges_fuss/"
FZ = np.diag([1.0, 1.0, -1.0])

# ---------------------------------------------------------------- Soll (SPEZ 4.4) ----------------------------------------------
L_SOLL = 1.90          # Nasenspitze bis Rumpfende, Meter bei Groesse 1,0 (SPEZ 4.4: 1,90 +-0,08)
W_ZU_L = 0.34          # Kopfbreite W = 0,34 L_SOLL = 0,646 m (fest)
L_ZIEL = 1.84          # gebaut: L = 1,84 m (in der Toleranz): Ruecken dann 0,54 L wie Soll, Rumpf kuerzer (Kevin: "runder Rumpf");
                       # W = 0,646 m = 0,351 L (Soll 0,34 +-0,03)

# ---------------------------------------------------------------- Skelett-Faktoren -----------------------------------------------
# Je Knochen die Form-Skalierung im Knochen-Lokalraum (X quer, Y laengs, Z hoch -- fuer Rumpf und Beine in ex2 nachgemessen:
# Pelvis/Spine X = tier y, Y = vorn, Z = oben; Spine1 X/Z gespiegelt). Kinder-Gelenke erben diag(S_eltern) * Lage (wie
# baer_fell/baby/baby_vergleich.py welt_junges), die Drehungen bleiben die des Erwachsenen (bit-gleich in den Clips).
# Danach alles mal U (gleichmaessig), U so gewaehlt, dass L = 1,90 m. Pfoten: Groesse wie beim Erwachsenen bei gleichem L.
# Geloest mit werkzeug/koerper_mass.py (U = 1, tl = Rumpf laengs fuer L = 1,90 m, fh = Hueft-Hoehe fuer Boden in Idle Bild 0).
TL, FH = 1.0131, 0.7769
FAKTOR = {
    "Dummy01": (1.0, 1.0, FH),          # Z = Hoehe von Bip01 (Hueft-Faktor, Boden)
    "Bip01": (1.0, TL, FH),             # Y = Abstand Bip01 -> Becken (Rumpflaenge), Z = Beckenhoehe in den Clips
    "Bip01_Pelvis": (0.86, TL, 0.94),
    "Bip01_Spine": (0.86, TL, 0.94),
    "Bip01_Spine1": (0.86, TL, 0.94),
    "Bip01_Neck": (0.85, 0.45, 0.85),
    "Bip01_Tail": (0.8, 0.8, 0.8),
    "Bip01_L_Thigh": (0.95, 0.74, 0.95), "Bip01_R_Thigh": (0.95, 0.74, 0.95),
    "Bip01_L_Calf": (0.95, 0.74, 0.95), "Bip01_R_Calf": (0.95, 0.74, 0.95),
    "Bip01_L_UpperArm": (0.95, 0.74, 0.95), "Bip01_R_UpperArm": (0.95, 0.74, 0.95),
    "Bip01_L_Forearm": (0.95, 0.74, 0.95), "Bip01_R_Forearm": (0.95, 0.74, 0.95),
    "Bip01_L_Clavicle": (0.80, 0.80, 0.80), "Bip01_R_Clavicle": (0.80, 0.80, 0.80),
}
# Zusaetzliche Gelenk-Versaetze (tier-Meter in der Ruhe, nach dem Skalieren): Halsansatz hoeher, damit der Kopf oben auf dem
# Koerper sitzt (SPEZ 4.4: Kopf oben -0,03..+0,08 L gegen den Ruecken); die Clip-Drehungen bleiben unveraendert.
VERSATZ_TIER = {"Bip01_Neck": (0.0, 0.0, 0.05)}
PFOTEN = ("Bip01_L_Foot", "Bip01_R_Foot", "Bip01_L_Toe0", "Bip01_R_Toe0", "Bip01_L_Hand", "Bip01_R_Hand")


def lade_json_glb(pfad=GLB_ALT):
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


def tier(P):
    P = np.asarray(P, float)
    return np.stack((-P[..., 2], P[..., 0], P[..., 1]), -1) / M2U


def dump(T):
    T = np.asarray(T, float)
    return np.stack((T[..., 1], T[..., 2], -T[..., 0]), -1) * M2U


def tier_R(R):
    """Drehung/Achsen (Spalten) Dump -> tier (ohne Masstab)."""
    A = np.array([[0, 0, -1.0], [1, 0, 0], [0, 1, 0]])
    return A @ R


class Erwachsener:
    """Erwachsener aus dem Importer-Dump; Ruhe-Lokal aus den GLB-Knoten (Dump-Raum), FK geprueft gegen inv(Offset)."""

    def __init__(self):
        D = pickle.load(open(DUMP, "rb"))
        self.D = D
        self.names = D["names"]
        self.par = D["par"]
        self.idx = D["idx"]
        self.nb = len(self.names)
        J, _ = lade_json_glb()
        nodes = {n["name"]: n for n in J["nodes"]}
        self.t_loc = np.zeros((self.nb, 3))
        self.R_loc = np.zeros((self.nb, 3, 3))
        for b, nm in enumerate(self.names):
            n = nodes[nm]
            self.t_loc[b] = FZ @ np.array(n.get("translation", [0, 0, 0]), float)
            self.R_loc[b] = FZ @ quat_m(n.get("rotation", [0, 0, 0, 1])) @ FZ
        self.BW = self.fk(self.t_loc, self.R_loc)
        V = D["verts"]
        self.V = V
        self.P = V[:, :3].copy()
        self.Wt = V[:, 3:7].copy()
        self.Bi = V[:, 7:11].astype(int)
        self.UV = V[:, 11:13].copy()
        self.F = D["el"].reshape(-1, 3)
        self.off = D["off"]
        # Pruefung: gewichtete Knochen FK == inv(off)
        used = np.unique(self.Bi[self.Wt > 0])
        err = max(np.abs(self.BW[b] - np.linalg.inv(self.off[b])).max() for b in used)
        assert err < 1e-4, err

    def fk(self, t_loc, R_loc):
        W = np.zeros((self.nb, 4, 4))
        for b in range(self.nb):
            T = np.eye(4)
            T[:3, :3] = R_loc[b]
            T[:3, 3] = t_loc[b]
            W[b] = T if self.par[b] < 0 else W[self.par[b]] @ T
        return W

    def gewicht(self, namen):
        w = np.zeros(len(self.P))
        for nm in namen:
            b = self.idx[nm]
            w += np.where(self.Bi == b, self.Wt, 0.0).sum(1)
        return w

    def clip_lokal(self, clip, bild):
        """Lokale Schluessel (Dump-Raum) eines Clip-Bildes: Lage, Drehung (Matrix), Skalierung."""
        c = self.D["clips"][clip]
        Lk = c["L"][bild]
        t = np.zeros((self.nb, 3))
        R = np.zeros((self.nb, 3, 3))
        for b in range(self.nb):
            if b in Lk:
                k = Lk[b]
                t[b] = k[:3]
                R[b] = quat_m(k[3:7])
            else:
                t[b] = self.t_loc[b]
                R[b] = self.R_loc[b]
        return t, R


class Junges:
    """Skelett des Jungen: Knochenlaengen neu, Drehungen wie der Erwachsene. Alles in Dump-Einheiten."""

    def __init__(self, E, faktor=FAKTOR, U=1.0, pfote_soll=None, versatz=VERSATZ_TIER):
        self.E = E
        self.U = U
        S = np.ones((E.nb, 3))
        for nm, f in faktor.items():
            S[E.idx[nm]] = f
        if pfote_soll is not None:
            for nm in PFOTEN:
                S[E.idx[nm]] = pfote_soll / U
        self.S = S                                     # Form-Skalierung je Knochen (vor U)
        self.t_loc = np.zeros((E.nb, 3))
        for b in range(E.nb):
            p = E.par[b]
            self.t_loc[b] = U * (S[p] if p >= 0 else 1.0) * E.t_loc[b]
        BW0 = E.fk(self.t_loc, E.R_loc)
        for nm, v in (versatz or {}).items():
            b = E.idx[nm]
            p = E.par[b]
            dw = dump(np.array(v))                                    # Richtung im Dump-Raum (Meter -> Einheiten)
            self.t_loc[b] = self.t_loc[b] + BW0[p][:3, :3].T @ dw
        self.BW = E.fk(self.t_loc, E.R_loc)            # Ruhe-Welt des Jungen (starr, ohne Skalierung)
        self.inv_BW = np.array([np.linalg.inv(m) for m in self.BW])

    def lokal_aus_clip(self, clip, bild):
        """Lokale Lagen fuer ein Clip-Bild: Drehungen aus dem Clip, Lagen = Junges-Ruhe; Becken/Translation_Data aus dem Clip mal
        diag(S_eltern) * U (die einzigen Knochen mit bewegter Lage, SPEZ 3.3 Punkt 2)."""
        E = self.E
        t, R = E.clip_lokal(clip, bild)
        tl = self.t_loc.copy()
        for nm in ("Bip01_Pelvis", "Translation_Data", "Bip01"):
            b = E.idx[nm]
            p = E.par[b]
            tl[b] = self.U * (self.S[p] if p >= 0 else 1.0) * t[b]
        return tl, R

    def welt(self, clip=None, bild=0):
        if clip is None:
            return self.BW
        tl, R = self.lokal_aus_clip(clip, bild)
        return self.E.fk(tl, R)

    def koerper_ruhe(self, P, Wt, Bi):
        """Netzpunkte des Erwachsenen (Dump-Raum, Ruhe) -> Ruhe des Jungen: v' = sum w B'_k diag(U S_k) B_k^-1 v."""
        E = self.E
        h = np.c_[P, np.ones(len(P))]
        out = np.zeros((len(P), 3))
        for k in range(4):
            b = Bi[:, k]
            Mk = np.einsum("nij,njk->nik", self.BW[b], np.einsum("nij,njk->nik", self._diag4(self.U * self.S[b]), np.linalg.inv(E.BW)[b]))
            out += Wt[:, k:k + 1] * np.einsum("nij,nj->ni", Mk, h)[:, :3]
        return out

    @staticmethod
    def _diag4(s):
        d = np.zeros((len(s), 4, 4))
        d[:, 0, 0], d[:, 1, 1], d[:, 2, 2], d[:, 3, 3] = s[:, 0], s[:, 1], s[:, 2], 1.0
        return d


def haut(Mw, inv_bind, P, Wt, Bi):
    """Linear Blend Skinning wie im Spiel (Dump-Raum)."""
    h = np.c_[P, np.ones(len(P))]
    out = np.zeros((len(P), 3))
    for k in range(4):
        b = Bi[:, k]
        S = np.einsum("nij,njk->nik", Mw[b], inv_bind[b])
        out += Wt[:, k:k + 1] * np.einsum("nij,nj->ni", S, h)[:, :3]
    return out


# ---------------------------------------------------------------- Kopf-Rahmen am Kopfknochen -----------------------------------
# Erwachsener (ex5, mess_kopf-Konstanten): Augenmitte 0,288 m vor / 0,085 m ueber dem Kopfgelenk entlang der Kopfachse (= Knochen-Y,
# 15 Grad nach unten), d. h. Gelenk bei (-0,663 / -0,195) W_erw. Junges: Gelenk an der Schaedelbasis bei (-0,45 / -0,17) W.
GELENK_KOPF_W = np.array((-0.45, 0.0, -0.24))
GELENK_KIEFER_W = np.array((-0.25, 0.0, -0.21))


def kopf_rahmen_lokal():
    """Achsen des Kopf-Rahmens im Lokalraum des Kopfknochens (Dump): x = Knochen-Y, z = Knochen-Z, y = z x x.
    Hinweis: der Dump-Raum ist gegen die Welt gespiegelt, deshalb zeigt dieses y in der Welt (tier) nach RECHTS (= -Knochen-X).
    Fuer den symmetrischen Kopf ohne Belang; 'ohr_l' (y > 0) ist damit das rechte Ohr des Tieres."""
    ex = np.array((0.0, 1.0, 0.0))
    ez = np.array((0.0, 0.0, 1.0))
    ey = np.cross(ez, ex)
    return np.stack((ex, ey, ez), 1)   # Spalten


def kopf_zu_knochen(Q, W_dump):
    """Kopf-Rahmen (Einheiten W) -> Lokalraum des Kopfknochens (Dump-Einheiten)."""
    A = kopf_rahmen_lokal()
    return (np.asarray(Q) - GELENK_KOPF_W) @ A.T * W_dump


# ---------------------------------------------------------------- Kopf-Form (implizit, Einheiten W) --------------------------------
def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1 - h) + a * h - k * h * (1 - h)


def smax(a, b, k):
    return -smin(-a, -b, k)


def ell(Q, c, r):
    """Naeherungsweise Abstand zu einem Ellipsoid (Inigo-Quilez-Naeherung)."""
    d = (Q - np.asarray(c)) / np.asarray(r)
    k0 = np.linalg.norm(d, axis=-1)
    k1 = np.linalg.norm(d / np.asarray(r), axis=-1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)


def ell_asym(Q, c, rv, rh, r_y, r_z):
    """Ellipsoid mit vorderem/hinterem x-Radius."""
    rx = np.where(Q[..., 0] >= c[0], rv, rh)
    d = np.stack(((Q[..., 0] - c[0]) / rx, (Q[..., 1] - c[1]) / r_y, (Q[..., 2] - c[2]) / r_z), -1)
    k0 = np.linalg.norm(d, axis=-1)
    rr = np.stack((rx, np.full_like(rx, r_y), np.full_like(rx, r_z)), -1)
    k1 = np.linalg.norm(d / rr, axis=-1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)


def schaedel(Q, p):
    """Schaedel: Querschnitt (y, z) als Superellipse (Exponent n), laengs Ellipse mit vorderem/hinterem Radius."""
    c = p["sch_c"]
    x, y, z = Q[..., 0] - c[0], Q[..., 1], Q[..., 2] - c[2]
    rx = np.where(x >= 0, p["sch_rv"], p["sch_rh"])
    n = p["sch_n"]
    zr = np.where(z >= 0, p["sch_rz_o"], p["sch_rz_u"])
    rho = ((np.abs(y) / p["sch_ry"]) ** n + (np.abs(z) / zr) ** n) ** (1.0 / n)
    m = np.where(x >= 0, 2.0, p["sch_m_hinten"])
    f = ((np.abs(x) / rx) ** m + rho ** m) ** (1.0 / m)
    return (f - 1.0) * np.minimum(np.minimum(rx, p["sch_ry"]), zr)


def schnauze(Q, p):
    """Schnauze: Querschnitt-Loft entlang x vom Absatz bis vor die Nase; Oberkante = Nasenruecken, Unterkante = Lippe."""
    x, y, z = Q[..., 0], Q[..., 1], Q[..., 2]
    x0, x1 = p["sn_x0"], p["sn_x1"]
    t = np.clip((x - x0) / (x1 - x0), 0.0, 1.0)
    zo = np.interp(x, *p["sn_oben"])
    zu = np.interp(x, *p["sn_unten"])
    hb = np.interp(x, *p["sn_breite"])
    zc = (zo + zu) / 2
    hh = np.maximum((zo - zu) / 2, 1e-3)
    n = p["sn_n"]
    rho = ((np.abs(y) / hb) ** n + (np.abs(z - zc) / hh) ** n) ** (1.0 / n)
    # vorn: runde Kappe; hinten offen (steckt im Schaedel)
    dxv = np.maximum(x - x1, 0.0) / p["sn_kappe"]
    f = np.sqrt(rho ** 2 + dxv ** 2)
    d = (f - 1.0) * np.minimum(hb, hh)
    d = np.where(x < x0 - 0.15, np.maximum(d, (x0 - 0.15) - x), d)
    return d


def rbox(Q, c, h, r):
    q = np.abs(Q - np.asarray(c)) - np.asarray(h) + r
    return np.linalg.norm(np.maximum(q, 0.0), axis=-1) + np.minimum(np.max(q, axis=-1), 0.0) - r


def nase(Q, p):
    """Nasenpolster: abgerundeter Quader, unten schmaler (SPEZ 4.2: 0,165 x 0,105 vorn, unten 0,12), Vorderflaeche leicht nach unten."""
    c = np.array(p["na_c"])
    a = math.radians(p["na_kipp"])
    R = np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])
    L = (Q - c) @ R
    hz = p["na_h"][2]
    t = np.clip((hz - L[..., 2]) / (2 * hz), 0.0, 1.0)          # 0 oben, 1 unten
    hy = p["na_h"][1] * (1.0 - p["na_unten_schmal"] * t)
    q = np.stack((np.abs(L[..., 0]) - p["na_h"][0], np.abs(L[..., 1]) - hy, np.abs(L[..., 2]) - hz), -1) + p["na_r"]
    d = np.linalg.norm(np.maximum(q, 0.0), axis=-1) + np.minimum(np.max(q, axis=-1), 0.0) - p["na_r"]
    # Nasenloecher (kleine Mulden) und Mittelfurche
    for s in (1.0, -1.0):
        nl = ell(Q, (c[0] + p["na_h"][0] * 1.0, s * p["na_loch_y"], c[2] - p["na_loch_dz"]), (0.014, 0.017, 0.010))
        d = smax(d, -nl, 0.004)
    return d


def kopf_feld(Q, p, mit_auge=True, mit_maul=True, mit_hals=True):
    """Oberkopf-Schale U (Einheiten W, Kopf-Rahmen): < 0 innen."""
    d = schaedel(Q, p)
    for s in (1.0, -1.0):
        c = np.array(p["wa_c"]) * (1, s, 1)
        d = smin(d, ell(Q, c, p["wa_r"]), p["wa_k"])
    d = smin(d, ell(Q, p["un_c"], p["un_r"]), p["un_k"])
    ksn = np.interp(Q[..., 2], (-0.13, -0.03), (p["sn_k_unten"], p["sn_k"]))     # seitlich/unten weicher in die Wangen
    d = smin(d, schnauze(Q, p), ksn)
    d = smin(d, ell(Q, p["ki_c"], p["ki_r"]), p["ki_k"])
    if p.get("wz_amp", 0) > 0:
        d = d - wangen_zacken(Q, p)
    if mit_hals and "hals" in p:
        d = smin(d, hals_feld(Q, p["hals"]), p["hals"]["k"])
    d = smin(d, nase(Q, p), p["na_k"])
    if mit_auge:
        for i, s in enumerate((1.0, -1.0)):
            ac, an = auge_lage(p, s)
            if "au_flaeche" in p:   # Augenoeffnung: elliptischer Zylinder entlang der Blickachse ab der Oberflaeche, Tiefe au_tief
                mul = augen_loch(Q, np.array(p["au_flaeche"][i]), an, p)
                d = smax(d, -mul, p["au_mulde_k"])
                d = np.minimum(d, np.linalg.norm(Q - np.array(p["au_ball"][i]), axis=-1) - p["au_ball_r"])
            else:
                mul = mulde(Q, ac, an, p)
                d = smax(d, -mul, p["au_mulde_k"])
    if mit_maul:
        d = smax(d, -maul_raum(Q, p), p["ma_k"])
    return d


def wangen_zacken(Q, p):
    """fix1 (Befund 'Wangen-Fellzacken', SPEZ 4.2): leicht abstehende Wangen -- wenige grosse Fellzacken (Spitzen nach unten-aussen)
    am seitlichen Umriss zwischen z +0,18 und -0,24 W, Hoehe wz_amp (0,015-0,03 W). Sagezahn in z (langsam an, schnell ab), nur auf
    der Wangenseite (|y| gross) und um die breiteste Stelle in x. Gibt die Aufwoelbung (>= 0, Einheiten W) zurueck."""
    x, y, z = Q[..., 0], np.abs(Q[..., 1]), Q[..., 2]
    z0, z1 = p.get("wz_z", (0.18, -0.24))
    per = (z0 - z1) / p.get("wz_n", 3)
    s = np.clip((z0 - z) / per, 0.0, p.get("wz_n", 3) - 1e-6)
    f = s - np.floor(s)
    spitze = 0.78
    prof = np.where(f < spitze, (f / spitze) ** 1.3, ((1.0 - f) / (1.0 - spitze)) ** 0.8)
    prof = prof * np.clip((s + 0.25) / 0.25, 0, 1) * np.clip(((z0 - z1) / per - s + 0.0) / 0.25, 0, 1)
    seite = np.clip((y - 0.34) / 0.07, 0.0, 1.0)
    xm = p.get("wz_x", (-0.40, -0.24, -0.06))
    lx = np.clip((x - xm[0]) / (xm[1] - xm[0]), 0, 1) * np.clip((xm[2] - x) / (xm[2] - xm[1]), 0, 1)
    lx = lx * lx * (3 - 2 * lx)
    return p["wz_amp"] * prof * seite * lx


def maul_raum(Q, p):
    """Bereich des Unterkiefers vor der Mundwinkel-Ebene x_h und unter der Mundlinie m(x): < 0 innen.
    fix1 (Befund M4): seitlich begrenzt auf |y| < ma_breite(x) (<= 0,175 W, Kiefer <= 0,35 W breit) -- die Wangen und der Unterkopf
    neben dem Kinn bleiben am Oberkopf (Head); vorher ging der Schnitt ueber die ganze Kopfbreite (0,92 W, 'Entenschnabel')."""
    m = np.interp(Q[..., 0], *p["ma_linie"])
    a = Q[..., 2] - m
    b = p["ma_xh"] - Q[..., 0]
    d = smax(a, b, 0.012)
    if "ma_breite" in p:   # Seitenwand nach unten leicht nach aussen geneigt (ma_schraeg), damit die Schale sternfoermig bleibt
        yl = np.interp(Q[..., 0], *p["ma_breite"]) + p.get("ma_schraeg", 0.0) * np.maximum(m - Q[..., 2], 0.0)
        d = smax(d, np.abs(Q[..., 1]) - yl, 0.010)
    return d


def kiefer_feld(Q, p):
    """Unterkiefer-Schale J: Kopf ohne Maul-Schnitt, Aussenflaeche um 'ki_einzug' eingezogen (unter der Oberlippe mehr),
    oben abgeschnitten bei m + ki_ueber (Zunge, steckt geschlossen im Oberkopf), hinten bei x_h - ki_tief."""
    d0 = kopf_feld(Q, p, mit_auge=False, mit_maul=False, mit_hals=False)
    m = np.interp(Q[..., 0], *p["ma_linie"])
    unter_lippe = np.clip((Q[..., 2] - (m - p["ki_lippe_h"])) / p["ki_lippe_h"], 0.0, 1.0)
    d = d0 + p["ki_einzug"] + p["ki_lippe_ein"] * unter_lippe
    if p.get("ki_einzug_verdeckt", 0) > 0:
        # fix1: wo der Oberkopf NICHT geschnitten ist (Kiefer dort verdeckt), den Kiefer tiefer einziehen -- vorher lag er ueberall nur
        # 0,002 W unter der Oberkopf-Flaeche und die beiden Netze durchstachen sich unter dem Kinn (gezackter Rand, fix1/tmp/schnitt_a4.png)
        mr = maul_raum(Q, p)
        t = np.clip((mr + 0.010) / 0.022, 0.0, 1.0)
        d = d + p["ki_einzug_verdeckt"] * t * t * (3 - 2 * t)
    d = np.maximum(d, Q[..., 2] - (m + p["ki_ueber"]))
    d = np.maximum(d, (p["ma_xh"] - p["ki_tief"]) - Q[..., 0])
    if "ma_breite" in p:   # fix1 (M4): Kiefer nur so breit wie der Schnitt + verdeckter Rand ki_seite (steckt im Oberkopf)
        yl = np.interp(Q[..., 0], *p["ma_breite"]) + p.get("ma_schraeg", 0.0) * np.maximum(m - Q[..., 2], 0.0)
        d = np.maximum(d, np.abs(Q[..., 1]) - (yl + p.get("ki_seite", 0.015)))
    return d


def auge_lage(p, s):
    """Augenmitte auf der Oberflaeche und Blickrichtung (18 Grad aussen, 8 Grad hoch, SPEZ 4.2)."""
    a, e = math.radians(p["au_aussen"]), math.radians(p["au_hoch"])
    n = np.array((math.cos(e) * math.cos(a), s * math.cos(e) * math.sin(a), math.sin(e)))
    c = np.array((0.0, s * p["au_y"], 0.0))
    return c, n


def mulde(Q, c, n, p):
    """Augenmulde: Ellipsoid um die Augenoeffnung (Achsen: Blick n, quer, hoch)."""
    up = np.array((0.0, 0.0, 1.0))
    t = np.cross(up, n)
    t /= np.linalg.norm(t)
    u = np.cross(n, t)
    m = c + n * p["au_mulde_aus"]
    d = Q - m
    L = np.stack((d @ t, d @ u, d @ n), -1)
    return ell(L, (0, 0, 0), (p["au_mulde_b"], p["au_mulde_h"], p["au_mulde_t"]))


def hals_feld(Q, h):
    """Hals-Lappen (Kopf-Rahmen): Loft zwischen zwei Ellipsen (Achsen e1/e2) von a nach b, hinten offen ueber b hinaus um 'ueber'."""
    a, b = np.array(h["a"]), np.array(h["b"])
    ax = b - a
    Lh = np.linalg.norm(ax)
    ax /= Lh
    e1 = np.array(h["e1"])
    e1 = e1 - ax * (e1 @ ax)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(ax, e1)
    d = Q - a
    s = d @ ax
    t = np.clip(s / Lh, 0.0, 1.0)
    r1 = h["ra"][0] + (h["rb"][0] - h["ra"][0]) * t
    r2 = h["ra"][1] + (h["rb"][1] - h["ra"][1]) * t
    rho = np.sqrt(((d @ e1) / r1) ** 2 + ((d @ e2) / r2) ** 2)
    f = (rho - 1.0) * np.minimum(r1, r2)
    f = np.maximum(f, -s)                       # vorn (im Kopf) abgeschnitten
    f = np.maximum(f, s - (Lh + h["ueber"]))     # hinten (im Rumpf) abgeschnitten
    return f


# Grundparameter des Kopfes (Einheiten W). Profilwerte aus SPEZ 4.1 / ziel_kopf.json; Breiten aus 4.1/4.2.
KOPF_P = dict(
    sch_c=(-0.31, 0.0, 0.0), sch_rv=0.325, sch_rh=0.33, sch_ry=0.47, sch_rz_o=0.34, sch_rz_u=0.30, sch_n=2.5, sch_m_hinten=1.7,
    wa_c=(-0.22, 0.255, -0.17), wa_r=(0.24, 0.235, 0.24), wa_k=0.12,
    un_c=(-0.17, 0.0, -0.20), un_r=(0.34, 0.37, 0.20), un_k=0.08,
    sn_x0=0.02, sn_x1=0.235, sn_kappe=0.025, sn_n=2.2, sn_k=0.035, sn_k_unten=0.075,
    ki_c=(0.10, 0.0, -0.268), ki_r=(0.10, 0.13, 0.078), ki_k=0.03,
    sn_oben=([0.02, 0.04, 0.15, 0.235], [-0.005, -0.022, -0.06, -0.09]),
    sn_unten=([0.02, 0.15, 0.235], [-0.27, -0.26, -0.235]),
    sn_breite=([0.02, 0.10, 0.18, 0.235], [0.13, 0.15, 0.165, 0.16]),
    na_c=(0.255, 0.0, -0.148), na_h=(0.022, 0.083, 0.050), na_r=0.02, na_kipp=12.0, na_unten_schmal=0.28, na_k=0.012,
    na_loch_y=0.045, na_loch_dz=0.03,
    au_y=0.15, au_aussen=18.0, au_hoch=8.0, au_mulde_aus=0.008, au_mulde_b=0.040, au_mulde_h=0.031, au_mulde_t=0.040,
    au_mulde_k=0.004, au_ball_r=0.042, au_ball_tief=0.010, au_b=0.028, au_h=0.0215, au_tief=0.032,
    ma_xh=0.03, ma_linie=([0.0, 0.10, 0.20, 0.30], [-0.245, -0.240, -0.236, -0.236]), ma_k=0.006,
    ki_einzug=0.002, ki_lippe_ein=0.005, ki_lippe_h=0.03, ki_ueber=0.02, ki_tief=0.30,
    ohr_c=(-0.32, 0.35, 0.26), ohr_n=(0.85, 0.35, 0.40), ohr_d=0.245, ohr_dicke=0.09, ohr_mulde_t=0.022, ohr_mulde_r=0.55,
    # fix1: Wangen-Zacken (SPEZ 4.2). Kiefer-Schnitt seitlich begrenzt ('ma_breite') probiert und verworfen (gezackte Seitenwaende
    # unter dem Kinn, fix1/r_a2); der schmale Kiefer kommt jetzt aus den Gewichten (baer_netz_baby.py gewichte_kiefer, Befund M4).
    wz_amp=0.02, wz_n=3, wz_z=(0.18, -0.24), wz_x=(-0.34, -0.24, -0.13),
)


def ray_cast(feld, c, dirs, r_max, n_grob=160, n_bis=40):
    """Strahlen von c in Richtungen dirs: erster Austritt (feld wechselt von < 0 nach > 0)."""
    dirs = np.asarray(dirs, float)
    ts = np.linspace(0.0, r_max, n_grob)
    lo = np.zeros(len(dirs))
    hi = np.full(len(dirs), np.nan)
    prev = feld(c[None, :] + 0 * dirs)
    assert (prev < 0).all(), "Mittelpunkt nicht innen"
    for i in range(1, n_grob):
        val = feld(c[None, :] + dirs * ts[i])
        neu = np.isnan(hi) & (val >= 0)
        hi[neu] = ts[i]
        lo[neu] = ts[i - 1]
        if not np.isnan(hi).any():
            break
    assert not np.isnan(hi).any(), "Strahl ohne Austritt"
    for _ in range(n_bis):
        mid = (lo + hi) / 2
        v = feld(c[None, :] + dirs * mid[:, None])
        inn = v < 0
        lo = np.where(inn, mid, lo)
        hi = np.where(inn, hi, mid)
    return (lo + hi) / 2


def stern_pruef(feld, c, dirs, r_max, n=400):
    """Zaehlt Vorzeichenwechsel je Strahl (sternfoermig = genau 1)."""
    ts = np.linspace(0.0, r_max, n)
    vals = np.stack([feld(c[None, :] + dirs * t) >= 0 for t in ts], 0)
    return (np.diff(vals.astype(int), axis=0) != 0).sum(0)


# ---------------------------------------------------------------- Koerper-Netz des Jungen ---------------------------------------
def junges_standard(E=None):
    E = E or Erwachsener()
    return E, Junges(E, FAKTOR, 1.0, pfote_soll=L_ZIEL / 1.957)


def koerper_netz(E, J, grenze=0.5):
    """Erwachsenen-Netz ohne Kopf und Hals (Gewicht Head+Jaw+Neck >= grenze), in der Ruhe des Jungen (Dump-Raum).
    Rueckgabe: dict mit P (Ruhe Junges), F, UV, Wt, Bi, alt_index, rand (Randkanten), weg (entfernte Punkte, Ruhe Junges)."""
    wHJN = E.gewicht(["Bip01_Head", "Bip01_Jaw", "Bip01_Neck"])
    P0 = J.koerper_ruhe(E.P, E.Wt, E.Bi)       # falten_glaetten() probiert und verworfen (Dehnung max schlechter), bau_baby.md 6
    weg = wHJN >= grenze
    tri_ok = ~weg[E.F].any(1)
    F = E.F[tri_ok]
    benutzt = np.unique(F)
    neu = -np.ones(len(P0), int)
    neu[benutzt] = np.arange(len(benutzt))
    F2 = neu[F]
    # Randkanten (geschweisst nach Lage, damit UV-Naehte nicht als Rand zaehlen)
    key = np.round(P0, 6)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    Ew = np.sort(np.stack((wid[F[:, [0, 1]]], wid[F[:, [1, 2]]], wid[F[:, [2, 0]]]), 1).reshape(-1, 2), axis=1)
    u, c = np.unique(Ew, axis=0, return_counts=True)
    rand_w = u[c == 1]
    rand_pkt = np.unique(rand_w)
    # Lage je geschweisstem Punkt
    pos_w = np.zeros((wid.max() + 1, 3))
    pos_w[wid] = P0
    # Randschleife ordnen (groesste Schleife), je Randpunkt ein Vertreter im Koerpernetz und die Richtung "aus dem Koerper hinaus"
    nb = {}
    for a, b in rand_w:
        nb.setdefault(a, []).append(b)
        nb.setdefault(b, []).append(a)
    schleifen, gesehen = [], set()
    for st in nb:
        if st in gesehen:
            continue
        lp = [st]
        gesehen.add(st)
        prev, cur = None, st
        while True:
            nx = [q for q in nb[cur] if q != prev and q not in gesehen]
            if not nx:
                break
            prev, cur = cur, nx[0]
            lp.append(cur)
            gesehen.add(cur)
        schleifen.append(lp)
    loop = max(schleifen, key=len)
    vertreter = {}
    for i_alt in benutzt:
        vertreter.setdefault(wid[i_alt], i_alt)
    # Nachbarn (geschweisst) im Koerper
    adj = {}
    for f in F:
        for a, b in ((0, 1), (1, 2), (2, 0)):
            wa, wb = wid[f[a]], wid[f[b]]
            adj.setdefault(wa, set()).add(wb)
            adj.setdefault(wb, set()).add(wa)
    rs = set(loop)
    tang = []
    for w_ in loop:
        inn = [q for q in adj[w_] if q not in rs]
        if not inn:
            inn = list(adj[w_])
        v = pos_w[w_] - pos_w[inn].mean(0)
        tang.append(v / np.linalg.norm(v))
    loop_neu = np.array([neu[vertreter[w_]] for w_ in loop])
    return dict(P=P0[benutzt], F=F2, UV=E.UV[benutzt], Wt=E.Wt[benutzt], Bi=E.Bi[benutzt], alt=benutzt,
                rand=pos_w[rand_pkt], weg_P=P0[weg], weg_Wt=E.Wt[weg], weg_Bi=E.Bi[weg], wHJN=wHJN[benutzt],
                rand_loop=loop_neu, rand_loop_P=pos_w[loop], rand_tang=np.array(tang), n_schleifen=len(schleifen))


def koerper_netz_jfuss(E, J, grenze=0.5, ohren=True):
    """jfuss: wie koerper_netz, dazu 'ohren': Dreiecke mit zwei oder drei Randkanten (Zacken der Schnittkante, z. B. 2c-Kehlrand rechts:
    Dreieck aus drei Randpunkten) werden wiederholt entfernt -- sonst klappen sie beim Ring-Angleich auf die glatte Schleife um.
    Erwachsenen-Netz ohne Kopf und Hals (Gewicht Head+Jaw+Neck >= grenze), in der Ruhe des Jungen (Dump-Raum).
    Rueckgabe: dict mit P (Ruhe Junges), F, UV, Wt, Bi, alt_index, rand (Randkanten), weg (entfernte Punkte, Ruhe Junges)."""
    wHJN = E.gewicht(["Bip01_Head", "Bip01_Jaw", "Bip01_Neck"])
    P0 = J.koerper_ruhe(E.P, E.Wt, E.Bi)       # falten_glaetten() probiert und verworfen (Dehnung max schlechter), bau_baby.md 6
    weg = wHJN >= grenze
    tri_ok = ~weg[E.F].any(1)
    global OHREN_INFO
    OHREN_INFO = dict(entfernt=0, runden=0)
    if ohren:
        key0 = np.round(P0, 6)
        _, wid0 = np.unique(key0, axis=0, return_inverse=True)
        wid0 = wid0.ravel()
        for rd in range(20):
            Fk = wid0[E.F[tri_ok]]
            Ek = np.sort(np.stack((Fk[:, [0, 1]], Fk[:, [1, 2]], Fk[:, [2, 0]]), 1), axis=2)      # (n, 3, 2)
            flat = Ek.reshape(-1, 2)
            u_, inv_, c_ = np.unique(flat, axis=0, return_inverse=True, return_counts=True)
            rk = (c_[inv_.ravel()] == 1).reshape(-1, 3).sum(1)
            ohr = rk >= 2
            if not ohr.any():
                break
            ids = np.where(tri_ok)[0][ohr]
            tri_ok[ids] = False
            OHREN_INFO["entfernt"] += int(len(ids))
            OHREN_INFO["runden"] = rd + 1
    F = E.F[tri_ok]
    benutzt = np.unique(F)
    neu = -np.ones(len(P0), int)
    neu[benutzt] = np.arange(len(benutzt))
    F2 = neu[F]
    # Randkanten (geschweisst nach Lage, damit UV-Naehte nicht als Rand zaehlen)
    key = np.round(P0, 6)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    Ew = np.sort(np.stack((wid[F[:, [0, 1]]], wid[F[:, [1, 2]]], wid[F[:, [2, 0]]]), 1).reshape(-1, 2), axis=1)
    u, c = np.unique(Ew, axis=0, return_counts=True)
    rand_w = u[c == 1]
    rand_pkt = np.unique(rand_w)
    # Lage je geschweisstem Punkt
    pos_w = np.zeros((wid.max() + 1, 3))
    pos_w[wid] = P0
    # Randschleife ordnen (groesste Schleife), je Randpunkt ein Vertreter im Koerpernetz und die Richtung "aus dem Koerper hinaus"
    nb = {}
    for a, b in rand_w:
        nb.setdefault(a, []).append(b)
        nb.setdefault(b, []).append(a)
    schleifen, gesehen = [], set()
    for st in nb:
        if st in gesehen:
            continue
        lp = [st]
        gesehen.add(st)
        prev, cur = None, st
        while True:
            nx = [q for q in nb[cur] if q != prev and q not in gesehen]
            if not nx:
                break
            prev, cur = cur, nx[0]
            lp.append(cur)
            gesehen.add(cur)
        schleifen.append(lp)
    loop = max(schleifen, key=len)
    vertreter = {}
    for i_alt in benutzt:
        vertreter.setdefault(wid[i_alt], i_alt)
    # Nachbarn (geschweisst) im Koerper
    adj = {}
    for f in F:
        for a, b in ((0, 1), (1, 2), (2, 0)):
            wa, wb = wid[f[a]], wid[f[b]]
            adj.setdefault(wa, set()).add(wb)
            adj.setdefault(wb, set()).add(wa)
    rs = set(loop)
    tang = []
    for w_ in loop:
        inn = [q for q in adj[w_] if q not in rs]
        if not inn:
            inn = list(adj[w_])
        v = pos_w[w_] - pos_w[inn].mean(0)
        tang.append(v / np.linalg.norm(v))
    loop_neu = np.array([neu[vertreter[w_]] for w_ in loop])
    return dict(P=P0[benutzt], F=F2, UV=E.UV[benutzt], Wt=E.Wt[benutzt], Bi=E.Bi[benutzt], alt=benutzt,
                rand=pos_w[rand_pkt], weg_P=P0[weg], weg_Wt=E.Wt[weg], weg_Bi=E.Bi[weg], wHJN=wHJN[benutzt],
                rand_loop=loop_neu, rand_loop_P=pos_w[loop], rand_tang=np.array(tang), n_schleifen=len(schleifen))


def falten_glaetten(E, P0, runden=12, ring=2, lam=0.5):
    """Die Knochen-Skalierung (Rumpf quer/hoch anders als Beine laengs) knickt an Achsel/Leiste einzelne Dreiecke um. Hier werden
    nur die Punkte umgekippter oder stark geschrumpfter Dreiecke (Normale gegen den Erwachsenen cos < 0,3 oder Flaeche < 40 %) samt
    'ring' Nachbarringen geglaettet (Laplace, geschweisst ueber die Lage); alle anderen Punkte bleiben bit-gleich."""
    F = E.F
    key = np.round(E.P, 6)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    nw = wid.max() + 1
    Pw = np.zeros((nw, 3))
    Pw[wid] = P0
    Fw = wid[F]

    def kipp(Pw_):
        na = np.cross(E.P[F[:, 1]] - E.P[F[:, 0]], E.P[F[:, 2]] - E.P[F[:, 0]])
        nj = np.cross(Pw_[Fw[:, 1]] - Pw_[Fw[:, 0]], Pw_[Fw[:, 2]] - Pw_[Fw[:, 0]])
        aa, aj = np.linalg.norm(na, axis=1), np.linalg.norm(nj, axis=1)
        cos = (na * nj).sum(1) / np.maximum(aa * aj, 1e-12)
        return (cos < 0.3) | (aj < 0.25 * aa)
    schlecht = kipp(Pw)

    def umgekippt(Pw_):
        na = np.cross(E.P[F[:, 1]] - E.P[F[:, 0]], E.P[F[:, 2]] - E.P[F[:, 0]])
        nj = np.cross(Pw_[Fw[:, 1]] - Pw_[Fw[:, 0]], Pw_[Fw[:, 2]] - Pw_[Fw[:, 0]])
        return ((na * nj).sum(1) < 0).sum()
    umg0 = umgekippt(Pw)
    if not schlecht.any():
        return P0
    nb = [[] for _ in range(nw)]
    for a, b, c in Fw:
        nb[a] += [b, c]
        nb[b] += [a, c]
        nb[c] += [a, b]
    nb = [np.unique(n) for n in nb]
    frei = np.zeros(nw, bool)
    frei[np.unique(Fw[schlecht])] = True
    for _ in range(ring):
        neu = frei.copy()
        for i in np.where(frei)[0]:
            neu[nb[i]] = True
        frei = neu
    idx = np.where(frei)[0]
    for _ in range(runden):
        mittel = np.array([Pw[nb[i]].mean(0) for i in idx])
        Pw[idx] = Pw[idx] + lam * (mittel - Pw[idx])
    global FALTEN_INFO
    FALTEN_INFO = dict(dreiecke_vorher=int(schlecht.sum()), dreiecke_nachher=int(kipp(Pw).sum()), punkte_geglaettet=int(len(idx)),
                       umgekippt_vorher=int(umg0), umgekippt_nachher=int(umgekippt(Pw)))
    return Pw[wid]


FALTEN_INFO = {}
OHREN_INFO = {}


def kopf_welt(J, W_dump):
    """Abbildungen Kopf-Rahmen (W) <-> Dump-Welt in der Ruhe des Jungen."""
    ih = J.E.idx["Bip01_Head"]
    B = J.BW[ih]

    def k2w(Q):
        loc = kopf_zu_knochen(Q, W_dump)
        return (B[:3, :3] @ loc.T).T + B[:3, 3]

    A = kopf_rahmen_lokal()

    def w2k(P):
        loc = (np.linalg.inv(B[:3, :3]) @ (np.asarray(P) - B[:3, 3]).T).T
        return loc @ A / W_dump + GELENK_KOPF_W
    return k2w, w2k


# ---------------------------------------------------------------- Hals-Lappen aus dem Koerper-Rand ------------------------------
def hals_aus_rand(R, tief=0.30, ueber=0.10, ra=(0.30, 0.25), rand_luft=1.08, k=0.10):
    """Hals-Lappen (Kopf-Rahmen, W): Achse senkrecht zur Randebene, Ende b = Randmitte, Anfang a = b + tief * n (im Kopf).
    Radien am Ende so, dass jeder Randpunkt mit Luft (rand_luft) innen liegt."""
    c = R.mean(0)
    _, _, Vt = np.linalg.svd(R - c)
    n = Vt[2] if Vt[2][0] > 0 else -Vt[2]          # zeigt nach vorn in den Kopf
    a = c + tief * n
    ax = (c - a) / np.linalg.norm(c - a)
    e1 = np.array((0.0, 1.0, 0.0))
    e1 = e1 - ax * (e1 @ ax)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(ax, e1)
    d = R - a
    s = d @ ax
    Lh = tief
    t = np.clip(s / Lh, 0.0, 1.0)
    rb = np.array([0.3, 0.3])
    for _ in range(60):
        r1 = ra[0] + (rb[0] - ra[0]) * t
        r2 = ra[1] + (rb[1] - ra[1]) * t
        u1, u2 = (d @ e1) / r1, (d @ e2) / r2
        rho = np.sqrt(u1 ** 2 + u2 ** 2) * rand_luft
        if rho.max() <= 1.0:
            break
        i = rho.argmax()
        if abs(u1[i]) > abs(u2[i]):
            rb[0] *= 1.02
        else:
            rb[1] *= 1.02
    return dict(a=a.tolist(), b=c.tolist(), e1=e1.tolist(), ra=list(ra), rb=rb.tolist(), ueber=ueber, k=k, n_rand=n.tolist())


# ---------------------------------------------------------------- Karten (UV) und Abtastung ---------------------------------------
def basis(ax):
    ax = np.asarray(ax, float)
    ax = ax / np.linalg.norm(ax)
    ref = np.array((0.0, 0.0, -1.0)) if abs(ax[2]) < 0.9 else np.array((1.0, 0.0, 0.0))
    e1 = ref - ax * (ref @ ax)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(ax, e1)
    return ax, e1, e2


def richtung_aus_flaech(xy, ax):
    """Flaechentreue Azimutal-Projektion um ax: (x, y) mit rho = 2 sin(alpha/2) -> Einheitsrichtung."""
    a, e1, e2 = basis(ax)
    rho = np.linalg.norm(xy, axis=1)
    al = 2 * np.arcsin(np.clip(rho / 2, 0, 1))
    be = np.arctan2(xy[:, 1], xy[:, 0])
    return (np.cos(al)[:, None] * a + (np.sin(al) * np.cos(be))[:, None] * e1 + (np.sin(al) * np.sin(be))[:, None] * e2)


def flaech_aus_richtung(d, ax):
    a, e1, e2 = basis(ax)
    al = np.arccos(np.clip(d @ a, -1, 1))
    be = np.arctan2(d @ e2, d @ e1)
    rho = 2 * np.sin(al / 2)
    return np.stack((rho * np.cos(be), rho * np.sin(be)), 1)


def richtung_aus_band(ba, ax, sk):
    """Band-Karte: (beta * sk, alpha) -> Richtung (beta ab e1 = unten)."""
    a, e1, e2 = basis(ax)
    be = ba[:, 0] / sk
    al = ba[:, 1]
    return (np.cos(al)[:, None] * a + (np.sin(al) * np.cos(be))[:, None] * e1 + (np.sin(al) * np.sin(be))[:, None] * e2)


def quadbaum(lo, hi, h_fn, s0, tiefe=8, innen=None):
    """Quadtree-Punkte in [lo, hi]^2: Zelle teilen, solange Zellgroesse > h_fn(Mitte). innen(xy) -> bool filtert."""
    zellen = []
    nx = int(np.ceil((hi[0] - lo[0]) / s0))
    ny = int(np.ceil((hi[1] - lo[1]) / s0))
    xs = lo[0] + (np.arange(nx) + 0.5) * s0
    ys = lo[1] + (np.arange(ny) + 0.5) * s0
    C = np.array([(x, y) for x in xs for y in ys])
    s = s0
    fertig = []
    for _ in range(tiefe):
        if len(C) == 0:
            break
        h = h_fn(C)
        teil = s > h * 1.4
        fertig.append(C[~teil])
        C = C[teil]
        s = s / 2
        off = np.array([(-s / 2, -s / 2), (s / 2, -s / 2), (-s / 2, s / 2), (s / 2, s / 2)])
        C = (C[:, None, :] + off[None]).reshape(-1, 2)
    fertig.append(C)
    pts = np.concatenate(fertig, 0)
    if innen is not None:
        pts = pts[innen(pts)]
    return pts


def augen_loch(Q, fl, n, p):
    up = np.array((0.0, 0.0, 1.0))
    t = np.cross(up, n)
    t /= np.linalg.norm(t)
    u = np.cross(n, t)
    dq = Q - fl
    a, b, c = dq @ t, dq @ u, dq @ n
    rho = np.sqrt((a / p["au_b"]) ** 2 + (b / p["au_h"]) ** 2)
    d_zyl = (rho - 1.0) * min(p["au_b"], p["au_h"])
    if p.get("au_kegel", 0) > 0:   # fix1 (M3): Wand als Kegel (nach innen enger) -> von der Schalenmitte ganz sichtbar, runder Rand
        d_zyl = d_zyl + np.maximum(-c, 0.0) * math.tan(math.radians(p["au_kegel"]))
    return np.maximum(d_zyl, -p["au_tief"] - c)


def augen_setzen(p):
    """Augen-Oberflaechenpunkte (ohne Loch) und Augapfel-Mitten in p eintragen."""
    p = dict(p)
    p.pop("au_flaeche", None)
    p.pop("au_ball", None)
    fl, mz = [], []
    f0 = lambda Q: kopf_feld(Q, p, mit_auge=False, mit_maul=False, mit_hals=False)  # noqa: E731
    for s in (1.0, -1.0):
        ac, an = auge_lage(p, s)
        st = ac - an * 0.1
        tt = ray_cast(f0, st, an[None, :], 0.3)[0]
        f = st + an * tt
        fl.append(f.tolist())
        mz.append((f - an * (p["au_ball_tief"] + p["au_ball_r"])).tolist())
    p["au_flaeche"], p["au_ball"] = fl, mz
    return p


def augapfel_mitten(p):
    """Augapfel-Mitten: Oberflaeche (ohne Mulde) entlang der Blickrichtung suchen, dann au_ball_tief + Radius nach innen."""
    out = []
    f0 = lambda Q: kopf_feld(Q, p, mit_auge=False, mit_maul=False, mit_hals=False)  # noqa: E731
    for s in (1.0, -1.0):
        ac, an = auge_lage(p, s)
        st = ac - an * 0.1
        tt = ray_cast(f0, st, an[None, :], 0.3)[0]
        fl = st + an * tt
        out.append((fl - an * (p["au_ball_tief"] + p["au_ball_r"])).tolist())
    return out


# ================================================================ Lauf baer-junges-fuss (11.11.2026), Bauer FORM ===============
# Beine/Fuesse vom 2c-Baeren (Dump 08ec7806) in der Ruhe des Jungen (koerper_ruhe wie baer-baby, Skelett bit-gleich), Rumpf-Querschnitte
# wie heute (Rumpf-Ausgleich), Koerperrand auf den heutigen Rand (Ring-Angleich), Kopf-Teile U/J/Ol/Or fest aus fix1.npz.
# Alles in tier-Metern (x vorn, y links, z oben), Umrechnung mit tier()/dump(). Statisch/offline, nicht gespielt.

def lade_heute():
    """Netz des heutigen Jungen (fix1.npz = Netz von 6c3f0a96, byte-gleich geprueft) und seine Parameter (fix1.json)."""
    N = np.load(NETZ_HEUTE)
    return {k: N[k] for k in N.files}


def junges_jfuss(E=None):
    """Erwachsener = 2c, Junges = gleiche Faktoren wie baer-baby. Prueft: Skelett bit-gleich zu heute (fix1.npz BW, t_loc, S)."""
    E, J = junges_standard(E)
    H = np.load(NETZ_HEUTE)
    d_bw = float(np.abs(J.BW - H["BW"]).max())
    d_t = float(np.abs(J.t_loc - H["t_loc"]).max())
    d_s = float(np.abs(J.S - H["S"]).max())
    assert d_bw < 1e-12 and d_t < 1e-12 and d_s < 1e-12, (d_bw, d_t, d_s)
    return E, J, dict(skelett_abw_BW=d_bw, t_loc=d_t, S=d_s)


def schweiss_ids(P, nd=6):
    key = np.round(P, nd)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    return wid.ravel()


def schnitt_strecken(T, F, x0):
    """Strecken der Schnittlinie Netz (tier) mit der Ebene x = x0, als (n, 2, 2) in (y, z)."""
    d = T[:, 0] - x0
    dF = d[F]
    pos = dF > 0
    k = pos.sum(1)
    m = (k == 1) | (k == 2)
    Fm, dm, pm = F[m], dF[m], pos[m]
    out = []
    for (a, b) in ((0, 1), (1, 2), (2, 0)):
        sel = pm[:, a] != pm[:, b]
        t = dm[sel, a] / (dm[sel, a] - dm[sel, b])
        A = T[Fm[sel, a]][:, 1:]
        B = T[Fm[sel, b]][:, 1:]
        out.append((np.where(sel)[0], A + t[:, None] * (B - A)))
    # je Dreieck genau zwei Kreuzungspunkte
    idx = np.concatenate([o[0] for o in out])
    pts = np.concatenate([o[1] for o in out])
    o = np.argsort(idx, kind="stable")
    idx, pts = idx[o], pts[o]
    _, start, cnt = np.unique(idx, return_index=True, return_counts=True)
    ok = cnt == 2
    s = start[ok]
    return np.stack((pts[s], pts[s + 1]), 1)


def hb_auf_hoehe(seg, z):
    """max |y| der Schnittlinie auf der Hoehe z (Kreuzung der Strecken mit der Waagerechten), nan wenn keine."""
    za, zb = seg[:, 0, 1], seg[:, 1, 1]
    m = (za - z) * (zb - z) <= 0
    m &= za != zb
    if not m.any():
        return np.nan
    t = (z - za[m]) / (zb[m] - za[m])
    y = seg[m, 0, 0] + t * (seg[m, 1, 0] - seg[m, 0, 0])
    return float(np.abs(y).max())


def ruecken_auf(seg, y0=0.0):
    """hoechste und tiefste Kreuzung der Schnittlinie mit y = y0 (Ruecken- und Bauchlinie)."""
    ya, yb = seg[:, 0, 0], seg[:, 1, 0]
    m = ((ya - y0) * (yb - y0) <= 0) & (ya != yb)
    if not m.any():
        return np.nan, np.nan
    t = (y0 - ya[m]) / (yb[m] - ya[m])
    z = seg[m, 0, 1] + t * (seg[m, 1, 1] - seg[m, 0, 1])
    return float(z.max()), float(z.min())


RUMPF_PAR = dict(
    zc=0.50,                 # Grenze unten/oben (tier m): oben normierte Hoehe u = (z - zc) / (Ruecken - zc)
    z_lo=(0.40, 0.50),       # unten: Verhaeltnis der Halbbreiten auf echter Hoehe z in diesem Band gemessen
    zg=(0.30, 0.45),         # Ausblenden zu den Beinen: unter zg[0] kein Zug, ab zg[1] voll (smoothstep)
    u_max=0.90,              # ueber u_max Verhaeltnis wie bei u_max (Ruecken-Kamm: Halbbreite -> 0)
    x_bereich=(-0.79, 0.52), # gemessene Scheiben
    dx=0.01,
    sig_x=0.035, sig_u=0.10, # Glaettung der Verhaeltnis-Felder (Gauss, NaN-sicher)
    s_grenze=(0.85, 1.35),
    ruecken=True,            # Ruecken-Hoehe je Scheibe wie heute (z oben normiert)
    bauch=False,             # Bauch-Hoehe: nicht angeglichen (heutige Brust haengt als Sack zwischen den Vorderbeinen, PLAN 4.3)
)


def _glatt1(a, sig, dx):
    """NaN-sichere Gauss-Glaettung entlang Achse 0."""
    a = np.asarray(a, float)
    n = int(np.ceil(3 * sig / dx))
    k = np.exp(-0.5 * (np.arange(-n, n + 1) * dx / sig) ** 2)
    ok = np.isfinite(a)
    a0 = np.where(ok, a, 0.0)
    out = np.zeros_like(a0)
    wsum = np.zeros_like(a0)
    for i, w in zip(range(-n, n + 1), k):
        sh = np.roll(a0, i, 0)
        so = np.roll(ok, i, 0).astype(float)
        if i > 0:
            sh[:i] = 0
            so[:i] = 0
        elif i < 0:
            sh[i:] = 0
            so[i:] = 0
        out += w * sh
        wsum += w * so
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(wsum > 1e-6, out / wsum, np.nan)


def rumpf_feld(T_heute, F_heute, T_neu, F_neu, par=RUMPF_PAR):
    """Verhaeltnis-Felder heute/neu je x-Scheibe: s_lo(x, z) im Band z_lo, s_up(x, u) oben (normierte Hoehe), Ruecken R(x) beider."""
    xs = np.arange(par["x_bereich"][0], par["x_bereich"][1] + 1e-9, par["dx"])
    zl = np.linspace(par["z_lo"][0], par["z_lo"][1], 11)
    us = np.linspace(0.0, par["u_max"], 19)
    zc = par["zc"]
    Rh, R2, Bh, B2 = (np.full(len(xs), np.nan) for _ in range(4))
    Hl_h, Hl_2 = np.full((len(xs), len(zl)), np.nan), np.full((len(xs), len(zl)), np.nan)
    Hu_h, Hu_2 = np.full((len(xs), len(us)), np.nan), np.full((len(xs), len(us)), np.nan)
    for i, x0 in enumerate(xs):
        sh = schnitt_strecken(T_heute, F_heute, x0)
        s2 = schnitt_strecken(T_neu, F_neu, x0)
        if len(sh) == 0 or len(s2) == 0:
            continue
        Rh[i], Bh[i] = ruecken_auf(sh)
        R2[i], B2[i] = ruecken_auf(s2)
        for j, z in enumerate(zl):
            Hl_h[i, j] = hb_auf_hoehe(sh, z)
            Hl_2[i, j] = hb_auf_hoehe(s2, z)
        if np.isfinite(Rh[i]) and np.isfinite(R2[i]) and Rh[i] > zc + 0.05 and R2[i] > zc + 0.05:
            for j, u in enumerate(us):
                Hu_h[i, j] = hb_auf_hoehe(sh, zc + u * (Rh[i] - zc))
                Hu_2[i, j] = hb_auf_hoehe(s2, zc + u * (R2[i] - zc))
    with np.errstate(invalid="ignore", divide="ignore"):
        s_lo = Hl_h / Hl_2
        s_up = Hu_h / Hu_2
    g0, g1 = par["s_grenze"]
    s_lo = np.clip(s_lo, g0, g1)
    s_up = np.clip(s_up, g0, g1)
    roh = dict(s_lo=s_lo.copy(), s_up=s_up.copy())
    # glaetten: x (Gauss), u (Gauss); fehlende Werte -> 1 (kein Zug)
    s_lo = _glatt1(s_lo, par["sig_x"], par["dx"])
    s_up = _glatt1(s_up, par["sig_x"], par["dx"])
    s_up = _glatt1(s_up.T, par["sig_u"], us[1] - us[0]).T
    s_lo = np.where(np.isfinite(s_lo), s_lo, 1.0)
    s_up = np.where(np.isfinite(s_up), s_up, 1.0)
    # Ruecken nur, wo die Scheibe den ganzen Rumpf schneidet (Ruecken > zc + 0,1); sonst (Halsschnitt vorn) naechsten Wert halten
    gut = np.isfinite(Rh) & np.isfinite(R2) & (Rh > zc + 0.1) & (R2 > zc + 0.1)
    dR = _glatt1(np.where(gut, Rh - R2, np.nan), par["sig_x"], par["dx"])
    R2g = _glatt1(np.where(gut, R2, np.nan), par["sig_x"], par["dx"])
    ok = np.isfinite(dR) & np.isfinite(R2g)
    jn = np.where(ok)[0]
    near = jn[np.abs(np.arange(len(xs))[:, None] - jn[None]).argmin(1)]
    dR, R2g = dR[near], R2g[near]
    return dict(xs=xs, zl=zl, us=us, s_lo=s_lo, s_up=s_up, dR=dR, R2=R2g, Rh=Rh, R2roh=R2, Bh=Bh, B2=B2, roh=roh,
                Hl_h=Hl_h, Hl_2=Hl_2, Hu_h=Hu_h, Hu_2=Hu_2)


def _interp2(xs, ys, G, x, y):
    x = np.clip(x, xs[0], xs[-1])
    y = np.clip(y, ys[0], ys[-1])
    fi = (x - xs[0]) / (xs[1] - xs[0])
    fj = (y - ys[0]) / (ys[1] - ys[0])
    i0 = np.clip(np.floor(fi).astype(int), 0, len(xs) - 2)
    j0 = np.clip(np.floor(fj).astype(int), 0, len(ys) - 2)
    a = fi - i0
    b = fj - j0
    return ((1 - a) * (1 - b) * G[i0, j0] + a * (1 - b) * G[i0 + 1, j0] + (1 - a) * b * G[i0, j0 + 1] + a * b * G[i0 + 1, j0 + 1])


def sst(a, b, v):
    t = np.clip((v - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def rumpf_ausgleich(T, feld, par=RUMPF_PAR):
    """Punkte (tier) -> neue Lage: oben (z >= zc) normierte Hoehe auf den heutigen Ruecken, Halbbreite x s_up(x, u); unten Halbbreite
    x s_lo(x, z) mal Ausblendung g(z) zu den Beinen. Reine Funktion der Lage (UV-Naht-Doppelpunkte bleiben verschweisst)."""
    T = np.asarray(T, float)
    x, y, z = T[:, 0], T[:, 1], T[:, 2]
    zc = par["zc"]
    xs = feld["xs"]
    R2 = np.interp(x, xs, feld["R2"])
    dR = np.interp(x, xs, feld["dR"]) if par.get("ruecken", True) else np.zeros(len(T))
    oben = z >= zc
    u = np.where(oben, (z - zc) / np.maximum(R2 - zc, 1e-3), 0.0)
    s_up = _interp2(xs, feld["us"], feld["s_up"], x, np.clip(u, 0.0, par["u_max"]))
    s_lo = _interp2(xs, feld["zl"], feld["s_lo"], x, np.clip(z, feld["zl"][0], feld["zl"][-1]))
    g = sst(par["zg"][0], par["zg"][1], z)
    s = np.where(oben, s_up, 1.0 + (s_lo - 1.0) * g)
    zn = np.where(oben, z + u * dR, z)
    out = np.stack((x, y * s, zn), 1)
    return out, dict(s_min=float(s.min()), s_max=float(s.max()), dz_max_cm=float(np.abs(zn - z).max() * 100),
                     dy_max_cm=float(np.abs(y * s - y).max() * 100))


def rand_schleife(P, F, nd=6):
    """Groesste Randschleife (geschweisst nach Lage): Rueckgabe (Lagen in Reihenfolge, Vertreter-Index je Punkt, Schleifenzahl)."""
    wid = schweiss_ids(P, nd)
    Ew = np.sort(np.stack((wid[F[:, [0, 1]]], wid[F[:, [1, 2]]], wid[F[:, [2, 0]]]), 1).reshape(-1, 2), axis=1)
    u, c = np.unique(Ew, axis=0, return_counts=True)
    r = u[c == 1]
    nb = {}
    for a, b in r:
        nb.setdefault(a, []).append(b)
        nb.setdefault(b, []).append(a)
    loops, seen = [], set()
    for st in nb:
        if st in seen:
            continue
        lp, prev, cur = [st], None, st
        seen.add(st)
        while True:
            nx = [q for q in nb[cur] if q != prev and q not in seen]
            if not nx:
                break
            prev, cur = cur, nx[0]
            lp.append(cur)
            seen.add(cur)
        loops.append(lp)
    lp = max(loops, key=len)
    vert = {}
    for i in range(len(P)):
        vert.setdefault(wid[i], i)
    idx = np.array([vert[w] for w in lp])
    return P[idx], idx, len(loops)


def ring_angleich(T, T_rand, T_ziel, abfall=0.12, sig=0.03):
    """Koerperrand (tier, geordnet) auf die Zielschleife (tier, geordnet, heutiger geglaetteter Rand) ziehen: je Randpunkt der Punkt der
    Zielschleife mit gleichem Winkel um die Halsachse (Ebene der Zielschleife); Verschiebung weich (Gauss sig ueber die Randpunkte) in
    den Koerper, Abfall smoothstep bis 'abfall' m Abstand zum Rand. Rueckgabe neue Punkte, Verschiebung der Randpunkte."""
    c = T_ziel.mean(0)
    _, _, Vt = np.linalg.svd(T_ziel - c)
    n = Vt[2]
    e1 = Vt[0]
    e2 = np.cross(n, e1)

    def ang(Q):
        return np.arctan2((Q - c) @ e2, (Q - c) @ e1)
    # Zielschleife geschlossen, Winkel monoton (Umlaufsinn sgn)
    Z = np.vstack((T_ziel, T_ziel[:1]))
    aZ = np.unwrap(ang(Z))
    sgn = 1.0 if aZ[-1] > aZ[0] else -1.0
    aZ = sgn * (aZ - aZ[0])
    assert abs(aZ[-1] - 2 * math.pi) < 1e-6 and np.all(np.diff(aZ) > 0), "Zielschleife nicht monoton um die Halsachse"
    t = np.mod(sgn * (ang(T_rand) - ang(Z[:1])[0]), 2 * math.pi)
    # Bogenlaenge (PLAN 4.4): die gezackte 2c-Schleife ist um die Halsachse NICHT monoton (Rueckschritte bis 4,9 Grad am Kehlrand
    # rechts) -> Zuordnung nach Winkel klappte dort Dreiecke um (Probe v1/v2). Darum: Parameter = Bogenlaenge der (geglaetteten)
    # Randschleife, Versatz = Kreismittel der Winkel-Zuordnung -> monoton, gleiche Reihenfolge wie auf dem Koerper.
    sZ = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Z, axis=0), axis=1))]
    sZ /= sZ[-1]
    uA = np.interp(t, aZ, sZ)
    Rg = T_rand.copy()
    for _ in range(6):
        Rg = (np.roll(Rg, 1, 0) + 2 * Rg + np.roll(Rg, -1, 0)) / 4
    sR = np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.vstack((Rg, Rg[:1])), axis=0), axis=1))]
    sR = sR[:-1] / sR[-1]
    dU = np.angle(np.exp(2j * math.pi * (np.roll(uA, -1) - uA)))
    if (dU < 0).sum() > len(dU) / 2:          # Umlaufsinn der Koerperschleife gegen die Zielschleife
        sR = np.mod(-sR, 1.0)
    phi = np.angle(np.exp(2j * math.pi * (uA - sR)).mean()) / (2 * math.pi)
    u = np.mod(sR + phi, 1.0)
    ziel = np.stack([np.interp(u, sZ, Z[:, k]) for k in range(3)], 1)
    d_rand = ziel - T_rand
    # weich in den Koerper
    dist = np.linalg.norm(T[:, None, :] - T_rand[None], axis=2)
    w = np.exp(-0.5 * (dist / sig) ** 2)
    ws = w.sum(1)
    dmit = (w @ d_rand) / np.maximum(ws, 1e-12)[:, None]
    dmin = dist.min(1)
    f = 1.0 - sst(0.0, abfall, dmin)
    out = T + dmit * f[:, None]
    # Randpunkte exakt
    for i, p in enumerate(T_rand):
        m = np.all(np.abs(T - p) < 1e-9, axis=1)
        out[m] = ziel[i]
    return out, d_rand, ziel


def abstand_schleifen(A, B):
    """Abstand jedes Punkts von A zur geschlossenen Polylinie B (m)."""
    B2 = np.vstack((B, B[:1]))
    a, b = B2[:-1], B2[1:]
    ab = b - a
    t = np.clip(np.einsum("nkj,kj->nk", A[:, None, :] - a[None], ab) / np.maximum((ab * ab).sum(1), 1e-12)[None], 0, 1)
    q = a[None] + t[..., None] * ab[None]
    return np.linalg.norm(A[:, None, :] - q, axis=2).min(1)


def pranke_vorn(T, dom_hand_w, mitte, f_lb=1.0):
    """Vorderpranke optional kleiner: Massstab f_lb in der Sohlenebene (x, y) um 'mitte', Hoehe bleibt; Gewicht = Hand-Anteil
    (weich, damit das Handgelenk nicht reisst). f_lb = 1 -> unveraendert."""
    if f_lb == 1.0:
        return T.copy()
    out = T.copy()
    w = np.clip(dom_hand_w, 0, 1)[:, None]
    d = T[:, :2] - mitte[None, :2]
    out[:, :2] = T[:, :2] + w * (f_lb - 1.0) * d
    return out


def nachbarn(T, F, nd=6):
    """Nachbarschaft der geschweissten Punkte (Lage gerundet nd): wid je Punkt, Liste der Nachbar-wid je wid."""
    wid = schweiss_ids(T, nd)
    Fw = wid[F]
    E = np.concatenate((Fw[:, [0, 1]], Fw[:, [1, 2]], Fw[:, [2, 0]]))
    E = np.unique(np.sort(E, 1), axis=0)
    nw = wid.max() + 1
    nb = [[] for _ in range(nw)]
    for a, b in E:
        nb[a].append(b)
        nb[b].append(a)
    return wid, [np.array(n, int) for n in nb]


def glaetten_verschiebung(T0, T1, F, fest, zone, runden=40, lam=0.5):
    """Verschiebung D = T1 - T0 auf dem Netz glaetten (Laplace auf D, nicht auf der Lage -> die 2c-Form bleibt): nur Punkte in 'zone'
    (bool je Punkt), 'fest' (bool je Punkt, z. B. Randpunkte) bleiben exakt. Rueckgabe T0 + D_glatt."""
    wid, nb = nachbarn(T0, F)
    nw = wid.max() + 1
    D = np.zeros((nw, 3))
    D[wid] = T1 - T0
    fw = np.zeros(nw, bool)
    fw[wid[fest]] = True
    zw = np.zeros(nw, bool)
    zw[wid[zone]] = True
    frei = np.where(zw & ~fw)[0]
    nbf = [nb[i] for i in frei]
    for _ in range(runden):
        mit = np.array([D[n].mean(0) for n in nbf])
        D[frei] = D[frei] + lam * (mit - D[frei])
    T0w = np.zeros((nw, 3))
    T0w[wid] = T0
    return T0 + D[wid]


def umgekippt(TA, TB, F):
    """Dreiecke, deren Normale zwischen TA und TB umklappt (cos < 0)."""
    na = np.cross(TA[F[:, 1]] - TA[F[:, 0]], TA[F[:, 2]] - TA[F[:, 0]])
    nb_ = np.cross(TB[F[:, 1]] - TB[F[:, 0]], TB[F[:, 2]] - TB[F[:, 0]])
    return (na * nb_).sum(1) < 0


def falten_reparieren(T0, T, F, fest, ring=2, runden=10, lam=0.5, max_iter=12):
    """Nur wo Dreiecke gegen T0 umklappen: deren freie Punkte + 'ring' Nachbarringe (geschweisst) mit Laplace auf der LAGE glaetten,
    'fest' bleibt; wiederholen bis keine Falte mehr (oder max_iter). Alle anderen Punkte bleiben bit-gleich."""
    wid, nb = nachbarn(T0, F)
    nw = wid.max() + 1
    Tw = np.zeros((nw, 3))
    Tw[wid] = T
    T0w = np.zeros((nw, 3))
    T0w[wid] = T0
    Fw = wid[F]
    fw = np.zeros(nw, bool)
    fw[wid[fest]] = True
    info = []
    for it in range(max_iter):
        um = umgekippt(T0w, Tw, Fw)
        info.append(int(um.sum()))
        if not um.any():
            break
        frei = np.zeros(nw, bool)
        frei[np.unique(Fw[um])] = True
        for _ in range(ring + it // 3):
            neu = frei.copy()
            for i in np.where(frei)[0]:
                neu[nb[i]] = True
            frei = neu
        idx = np.where(frei & ~fw)[0]
        for _ in range(runden):
            mit = np.array([Tw[nb[i]].mean(0) for i in idx])
            Tw[idx] = Tw[idx] + lam * (mit - Tw[idx])
    out = T.copy()
    geaendert = np.any(Tw[wid] != T, axis=1)
    out[geaendert] = Tw[wid][geaendert]
    return out, dict(umgekippt_je_runde=info, punkte_geaendert=int(geaendert.sum()))
