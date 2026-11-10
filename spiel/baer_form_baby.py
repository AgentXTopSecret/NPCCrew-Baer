# Lauf baer-baby (10.11.2026): Form des Baer-Jungen (Entwurf) -- Skelett, Koerper-Proportionen, Kopf-Form als implizite Flaeche.
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
DUMP = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_pfote/fix1/bau4/dump_final.txt.pkl"
GLB_ALT = r"C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/models_X/Skinned/NCBear.glb"   # nur lesen
TEX_ALT = r"C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/textures/Body/NCBear.png"       # nur lesen
ARB = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_baby/"
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
