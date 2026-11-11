# Lauf baer-rig-junges (11.11.2026), Rolle SKELETT+GEWICHTE: Skelett des Generator-Jungen C (RIG_PLAN.md Abschnitt 3).
# Nur numpy. Liest die FORM-Abgabe rig/form/C_rig_basis.npz (Ruhelage, tier-Meter) und den gespielten Erwachsenen
# (_arbeit/baer_junges/eingang/NCBear.glb 08ec7806 = Gerippe, erw_2c.txt.pkl = sein Importer-Dump; nur gelesen).
# Regeln (RIG_PLAN 3.1, Lehre M6): 26 Knochen, Namen/Eltern/Reihenfolge und Ruhe-DREHUNGEN = Erwachsener; neu sind nur Lagen:
#   - Beine exakt 1,000 (Calf, Foot, Forearm, Hand = Erwachsener), Rumpf isotrop R (Thigh/Spine/Spine1/Clavicle/UpperArm in x/z),
#     Spur quer frei (Q_H, Q_V), Fuss (Toe0) am Ballen des Netzes, Hals (Neck = C7) und Kopf (Head = Atlas) frei, Kiefer am
#     Kiefergelenk (ohne Gewichte), Schwanz an der Stummelwurzel; Becken-Ruhe nach der Becken-Regel (Hueftmitte = Erwachsener + DX,
#     DX = 0,375 (1 - R)); das Netz wird in x so verschoben, dass seine Hueften auf den Hueften des Skeletts liegen.
#   - R, Q_H, Q_V und der Versatz kommen aus einer eigenen Achsmessung der Beine (exakte waagerechte Schnitte, Linie mit der
#     Knochenrichtung des Erwachsenen durch die Schnitt-Schwerpunkte).
# Aufruf: python baer_skelett_rig.py bauen [R=0.90,...]   -> rig/skelett/skelett_rig.json, netz_rig.npz, mess_rig.json, sp_rig.txt
# Rahmen: tier = Meter, x vorn, y links, z oben; dump = Modellraum des Importers (0,544 E je Meter): dump = (y, z, -x) * 0,544.
# "Formrahmen" = Rahmen von C_rig_basis.npz (x 0 = Mitte zwischen den Pfoten); "Skelettrahmen" = Formrahmen + (versatz_x, 0, 0).
# Statisch/offline gerechnet, nicht gespielt. Schreibt nur unter _arbeit/baer_gen/rig/skelett/.
import json
import os
import pickle
import struct
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/skelett/werkzeug")
import schnitt as S  # noqa: E402

M2U = 0.544
RIG = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/"
SK = RIG + "skelett/"
FORM_NPZ = RIG + "form/C_rig_basis.npz"
FORM_LM = RIG + "form/landmarken_rig.json"
EIN = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_junges/eingang/"
GLB_ERW = EIN + "NCBear.glb"          # 08ec7806 (= NCBearTest NCBear.glb, gespielt), nur lesen
DUMP_ERW = EIN + "erw_2c.txt.pkl"     # Importer-Dump davon
FZ = np.diag([1.0, 1.0, -1.0])
CLIPS = ["DeerStag_Idle01", "DeerStag_Walk", "DeerStag_Run", "DeerStag_Death", "DeerStag_Dead", "NCBear_Rear", "NCBear_SwipeL",
         "NCBear_SwipeR", "NCBear_Slam", "NCBear_Bite", "NCBear_Maul", "NCBear_Eat", "NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp"]

# Parameter (Lagen im FORMRAHMEN, Meter). Begruendung je Zeile in rig/SKELETT.md Abschnitt 1.
PARAM = dict(
    R=0.90,                         # Rumpf isotrop; Achsmessung ergibt 0,912 (Grenze des Plans 0,78-0,90) -> 0,90, Rest je Bein 0,45 cm
    atlas=(0.440, 0.0, 0.935),      # unter der Ohr-Hinterkante, Augenhoehe (0,955) - 0,045 W
    c7=(0.290, 0.0, 0.965),         # Halsansatz ueber dem Brustgelenk, 31 % der Tiefe unter der Oberlinie (1,188)
    kiefer=(0.610, 0.0, 0.865),     # Kiefergelenk unter/hinter dem Auge (0,676 / 0,955), keine Gewichte
    schwanz=(-0.585, 0.0, 0.748),   # Stummelwurzel (Stummel-Maske Mitte -0,630 / 0,755), 4 cm unter der Haut
    ballen_x=-0.277,                # Hinterpfote: Ballen (FORM-Landmarke) -> Toe0-Lage entlang der Fussrichtung des Erwachsenen
)


def log(*a):
    print("SKELETT", *a, flush=True)


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


A_TD = np.array([[0, 0, -1.0], [1, 0, 0], [0, 1, 0]])      # Richtung dump -> tier (ohne Massstab)


def lade_glb_json(pfad=GLB_ERW):
    b = open(pfad, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    return json.loads(b[20:20 + n])


class Erw:
    """Erwachsener: Knochenliste aus dem Dump, Ruhe aus den GLB-Knoten (Dump-Raum)."""

    def __init__(self):
        D = pickle.load(open(DUMP_ERW, "rb"))
        self.D = D
        self.names, self.par, self.idx = D["names"], D["par"], D["idx"]
        self.nb = len(self.names)
        J = lade_glb_json()
        nodes = {n["name"]: n for n in J["nodes"]}
        self.t_e = np.zeros((self.nb, 3))
        self.R_loc = np.zeros((self.nb, 3, 3))
        self.q_glb = {}
        for b, nm in enumerate(self.names):
            n = nodes[nm]
            self.t_e[b] = FZ @ np.array(n.get("translation", [0, 0, 0]), float)
            self.R_loc[b] = FZ @ quat_m(n.get("rotation", [0, 0, 0, 1])) @ FZ
            self.q_glb[nm] = n.get("rotation", [0, 0, 0, 1])
        self.BW_e = self.fk(self.t_e, self.R_loc)
        self.pos_e = {nm: tier(self.BW_e[b][:3, 3]) for b, nm in enumerate(self.names)}

    def fk(self, t_loc, R_loc):
        W = np.zeros((self.nb, 4, 4))
        for b in range(self.nb):
            T = np.eye(4)
            T[:3, :3] = R_loc[b]
            T[:3, 3] = t_loc[b]
            W[b] = T if self.par[b] < 0 else W[self.par[b]] @ T
        return W

    def lokal_erw(self, clip, bild):
        Lk = self.D["clips"][clip]["L"][bild]
        t = self.t_e.copy()
        R = self.R_loc.copy()
        for b in range(self.nb):
            if b in Lk:
                t[b] = Lk[b][:3]
                R[b] = quat_m(Lk[b][3:7])
        return t, R


# ---------------------------------------------------------------- Achsmessung der Beine (Formrahmen) ------------------------------
def bein_mitten(V, T, vorn, links, z0, z1, schritt=0.01):
    u, v = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
    out = []
    for z in np.arange(z0, z1 + 1e-9, schritt):
        for P in S.schleifen(S.segmente(V, T, np.array([0, 0, 1.0]), z)):
            A, c = S.flaeche_schwerpunkt(P, u, v)
            if A < 1e-4 or A > 0.1:
                continue
            if (c[0] > 0) == bool(vorn) and (c[1] > 0) == bool(links):
                out.append(c)
    return np.array(out)


def bein_messung(V, T, E):
    """Je Bein: Schnitt-Schwerpunkte z 0,12-0,34 (vorn) / 0,12-0,32 (hinten; darueber verschmelzen die Hinterbeine), freie
    Hauptachse, Winkel zur Knochenrichtung des Erwachsenen, Linie mit Knochenrichtung durch den Schwerpunkt."""
    pe = E.pos_e
    out = {}
    for nm, vorn, links, z0, z1, a, b in (("VL", 1, 1, 0.12, 0.34, "Bip01_L_Forearm", "Bip01_L_Hand"),
                                         ("VR", 1, 0, 0.12, 0.34, "Bip01_R_Forearm", "Bip01_R_Hand"),
                                         ("HL", 0, 1, 0.12, 0.32, "Bip01_L_Calf", "Bip01_L_Foot"),
                                         ("HR", 0, 0, 0.12, 0.32, "Bip01_R_Calf", "Bip01_R_Foot")):
        M = bein_mitten(V, T, vorn, links, z0, z1)
        c = M.mean(0)
        dr = pe[b] - pe[a]
        dr /= np.linalg.norm(dr)
        _, _, Vt = np.linalg.svd(M - c)
        fr = Vt[0] * -np.sign(Vt[0][2])
        q = M - c
        q -= np.outer(q @ dr, dr)
        rest = np.linalg.norm(q, axis=1)
        out[nm] = dict(n=len(M), mitte=c, richtung=dr, frei=fr, winkel=float(np.degrees(np.arccos(min(1.0, abs(fr @ dr))))),
                       vorn_hinten_frei=float(np.degrees(np.arctan2(fr[0], -fr[2]))), seitlich_frei=float(np.degrees(np.arctan2(fr[1], -fr[2]))),
                       rest_max_cm=float(100 * rest.max()), rest_mittel_cm=float(100 * rest.mean()), punkte=M)
    return out


def auf_linie(m, z):
    c, d = m["mitte"], m["richtung"]
    return c + d * (z - c[2]) / d[2]


# ---------------------------------------------------------------- Punkt-Dreieck-Abstand, Innen-Test ------------------------------
def abstand_dreiecke(p, V, T):
    """Kleinster Abstand Punkt p -> Dreiecksnetz (exakt, Ericson 5.1.5), vektorisiert ueber die Dreiecke."""
    a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    ab, ac, ap = b - a, c - a, p - a
    d1, d2 = (ab * ap).sum(1), (ac * ap).sum(1)
    bp = p - b
    d3, d4 = (ab * bp).sum(1), (ac * bp).sum(1)
    cp = p - c
    d5, d6 = (ab * cp).sum(1), (ac * cp).sum(1)
    va = d3 * d6 - d5 * d4
    vb = d5 * d2 - d1 * d6
    vc = d1 * d4 - d3 * d2
    den = np.where(np.abs(va + vb + vc) < 1e-18, 1e-18, va + vb + vc)
    v_ = vb / den
    w_ = vc / den
    q = a + ab * v_[:, None] + ac * w_[:, None]
    # Randfaelle
    m = (d1 <= 0) & (d2 <= 0)
    q[m] = a[m]
    m = (d3 >= 0) & (d4 <= d3)
    q[m] = b[m]
    m = (d6 >= 0) & (d5 <= d6)
    q[m] = c[m]
    m = (vc <= 0) & (d1 >= 0) & (d3 <= 0)
    t = d1 / np.where(np.abs(d1 - d3) < 1e-18, 1e-18, d1 - d3)
    q[m] = (a + ab * t[:, None])[m]
    m = (vb <= 0) & (d2 >= 0) & (d6 <= 0)
    t = d2 / np.where(np.abs(d2 - d6) < 1e-18, 1e-18, d2 - d6)
    q[m] = (a + ac * t[:, None])[m]
    m = (va <= 0) & ((d4 - d3) >= 0) & ((d5 - d6) >= 0)
    t = (d4 - d3) / np.where(np.abs((d4 - d3) + (d5 - d6)) < 1e-18, 1e-18, (d4 - d3) + (d5 - d6))
    q[m] = (b + (c - b) * t[:, None])[m]
    return float(np.sqrt(((p - q) ** 2).sum(1).min()))


def windungszahl(p, V, T):
    """Verallgemeinerte Windungszahl (1 = innen, 0 = aussen)."""
    a, b, c = V[T[:, 0]] - p, V[T[:, 1]] - p, V[T[:, 2]] - p
    la, lb, lc = np.linalg.norm(a, axis=1), np.linalg.norm(b, axis=1), np.linalg.norm(c, axis=1)
    det = np.einsum("ij,ij->i", a, np.cross(b, c))
    den = la * lb * lc + (a * b).sum(1) * lc + (b * c).sum(1) * la + (c * a).sum(1) * lb
    return float(np.arctan2(det, den).sum() / (2 * np.pi))


# ---------------------------------------------------------------- Skelett des Jungen ----------------------------------------------
def skelett(E, P, mess):
    """Ruhe-Gelenke (tier, Skelettrahmen) und lokale Lagen (E, Dump-Raum) des Jungen."""
    pe = E.pos_e
    R = float(P["R"])
    # Gelenke aus der Achsmessung (Formrahmen): Hand-/Sprunggelenk auf z der Kette, Ellbogen/Knie, dann Schulter/Huefte
    hm_e = 0.5 * (pe["Bip01_L_Thigh"] + pe["Bip01_R_Thigh"])
    sm_e = 0.5 * (pe["Bip01_L_UpperArm"] + pe["Bip01_R_UpperArm"])
    z_huefte = hm_e[2]
    z_schulter = hm_e[2] + R * (sm_e[2] - hm_e[2])
    o_th = pe["Bip01_L_Calf"] - pe["Bip01_L_Thigh"]
    o_ca = pe["Bip01_L_Foot"] - pe["Bip01_L_Calf"]
    o_ua = pe["Bip01_L_Forearm"] - pe["Bip01_L_UpperArm"]
    o_fa = pe["Bip01_L_Hand"] - pe["Bip01_L_Forearm"]
    gem = {}
    for s_ in "LR":
        sy = 1.0 if s_ == "L" else -1.0
        mh, mv = mess["H" + s_], mess["V" + s_]
        knie = auf_linie(mh, z_huefte + o_th[2])
        sprung = auf_linie(mh, z_huefte + o_th[2] + o_ca[2])
        huefte = 0.5 * ((knie - o_th * (1, sy, 1)) + (sprung - (o_th + o_ca) * (1, sy, 1)))
        elle = auf_linie(mv, z_schulter + o_ua[2])
        hand = auf_linie(mv, z_schulter + o_ua[2] + o_fa[2])
        schulter = 0.5 * ((elle - o_ua * (1, sy, 1)) + (hand - (o_ua + o_fa) * (1, sy, 1)))
        gem[s_] = dict(knie=knie, sprung=sprung, huefte=huefte, elle=elle, hand=hand, schulter=schulter)
    hx = 0.5 * (gem["L"]["huefte"][0] + gem["R"]["huefte"][0])
    sx = 0.5 * (gem["L"]["schulter"][0] + gem["R"]["schulter"][0])
    lat_h = 0.5 * (gem["L"]["huefte"][1] - gem["R"]["huefte"][1])
    lat_v = 0.5 * (gem["L"]["schulter"][1] - gem["R"]["schulter"][1])
    R_mess = (sx - hx) / (sm_e[0] - hm_e[0])
    DX = 0.5 * (1.0 - R) * (sm_e[0] - hm_e[0])
    # Skelett: Hueftmitte = Erwachsener + DX; Netz verschieben: Mitte Huefte/Schulter des Netzes auf die des Skeletts
    hx_j = hm_e[0] + DX
    sx_j = hx_j + R * (sm_e[0] - hm_e[0])
    versatz = 0.5 * (hx_j + sx_j) - 0.5 * (hx + sx)
    Q_H = lat_h / (R * pe["Bip01_L_Thigh"][1])
    lat_cl_e, lat_ua_e = pe["Bip01_L_Clavicle"][1], pe["Bip01_L_UpperArm"][1] - pe["Bip01_L_Clavicle"][1]
    Q_V = lat_v / (R * (lat_cl_e + lat_ua_e))
    vz = np.array((versatz, 0.0, 0.0))
    pos = {}
    pos["Dummy01"] = pe["Dummy01"].copy()
    pos["Bip01"] = pe["Bip01"].copy()
    pos["Translation_Data"] = pe["Translation_Data"].copy()
    hm_j = hm_e + np.array((DX, 0.0, 0.0))
    pos["Bip01_Pelvis"] = hm_j + R * (pe["Bip01_Pelvis"] - hm_e)
    for s_ in "LR":
        sy = 1.0 if s_ == "L" else -1.0
        o = pe["Bip01_%s_Thigh" % s_] - pe["Bip01_Pelvis"]
        pos["Bip01_%s_Thigh" % s_] = pos["Bip01_Pelvis"] + np.array((R * o[0], sy * lat_h, R * o[2]))
        for a, b in (("Thigh", "Calf"), ("Calf", "Foot")):
            pos["Bip01_%s_%s" % (s_, b)] = pos["Bip01_%s_%s" % (s_, a)] + (pe["Bip01_%s_%s" % (s_, b)] - pe["Bip01_%s_%s" % (s_, a)])
    pos["Bip01_Spine"] = pos["Bip01_Pelvis"] + R * (pe["Bip01_Spine"] - pe["Bip01_Pelvis"])
    pos["Bip01_Spine1"] = pos["Bip01_Spine"] + R * (pe["Bip01_Spine1"] - pe["Bip01_Spine"])
    for s_ in "LR":
        o = pe["Bip01_%s_Clavicle" % s_] - pe["Bip01_Spine1"]
        pos["Bip01_%s_Clavicle" % s_] = pos["Bip01_Spine1"] + np.array((R * o[0], R * Q_V * o[1], R * o[2]))
        o = pe["Bip01_%s_UpperArm" % s_] - pe["Bip01_%s_Clavicle" % s_]
        pos["Bip01_%s_UpperArm" % s_] = pos["Bip01_%s_Clavicle" % s_] + np.array((R * o[0], R * Q_V * o[1], R * o[2]))
        for a, b in (("UpperArm", "Forearm"), ("Forearm", "Hand")):
            pos["Bip01_%s_%s" % (s_, b)] = pos["Bip01_%s_%s" % (s_, a)] + (pe["Bip01_%s_%s" % (s_, b)] - pe["Bip01_%s_%s" % (s_, a)])
    # Toe0: Richtung = Fuss-Achse des Erwachsenen, Laenge so, dass x = Ballen des Netzes
    o_toe = pe["Bip01_L_Toe0"] - pe["Bip01_L_Foot"]
    f_fuss = (P["ballen_x"] + versatz - pos["Bip01_L_Foot"][0]) / o_toe[0]
    for s_ in "LR":
        pos["Bip01_%s_Toe0" % s_] = pos["Bip01_%s_Foot" % s_] + f_fuss * (pe["Bip01_%s_Toe0" % s_] - pe["Bip01_%s_Foot" % s_])
    pos["Bip01_Neck"] = np.array(P["c7"], float) + vz
    pos["Bip01_Head"] = np.array(P["atlas"], float) + vz
    pos["Bip01_Jaw"] = np.array(P["kiefer"], float) + vz
    pos["Bip01_Tail"] = np.array(P["schwanz"], float) + vz
    # lokale Lagen (Dump-Raum, E) aus den Weltlagen und den UNVERAENDERTEN Ruhe-Drehungen
    t_j = E.t_e.copy()
    for b, nm in enumerate(E.names):
        p = E.par[b]
        if p < 0:
            continue
        Rp = E.BW_e[p][:3, :3]
        t_j[b] = np.linalg.solve(Rp, dump(pos[nm]) - dump(pos[E.names[p]]))
    for nm in ("Bip01", "Dummy01", "Translation_Data"):
        t_j[E.idx[nm]] = E.t_e[E.idx[nm]]
    BW_j = E.fk(t_j, E.R_loc)
    fehler = max(float(np.abs(tier(BW_j[b][:3, 3]) - pos[nm]).max()) for b, nm in enumerate(E.names))
    assert fehler < 1e-9, fehler
    # Kontrolle der Regeln: Beinlaengen exakt, Rumpf isotrop
    for nm in ("Calf", "Foot", "Forearm", "Hand"):
        for s_ in "LR":
            b = E.idx["Bip01_%s_%s" % (s_, nm)]
            assert np.abs(t_j[b] - E.t_e[b]).max() < 1e-9, nm
    hals = pos["Bip01_Head"] - pos["Bip01_Neck"]
    erw_hals = pe["Bip01_Head"] - pe["Bip01_Neck"]
    delta = float(np.degrees(np.arctan2(hals[2], hals[0]) - np.arctan2(erw_hals[2], erw_hals[0])))
    info = dict(R=R, R_mess=float(R_mess), DX=float(DX), versatz=float(versatz), Q_H=float(Q_H), Q_V=float(Q_V), lat_h=float(lat_h),
                lat_v=float(lat_v), f_fuss=float(f_fuss), delta=delta, hals_m=float(np.linalg.norm(hals)),
                hals_neig=float(np.degrees(np.arctan2(hals[2], hals[0]))), gem=gem, hx=float(hx), sx=float(sx),
                bein_rest_cm={k: float(100 * v) for k, v in (("hinten_x", hx_j - (hx + versatz)), ("vorn_x", sx_j - (sx + versatz)))})
    return pos, t_j, BW_j, info


# ---------------------------------------------------------------- Becken-Regel ueber die Clips des Erwachsenen (sp_rig) -----------
class Junges:
    def __init__(self, E, t_j, DX):
        self.E, self.t_j, self.DX = E, t_j, DX
        ip = E.idx["Bip01_Pelvis"]
        self.t_mitte_e = 0.5 * (E.t_e[E.idx["Bip01_L_Thigh"]] + E.t_e[E.idx["Bip01_R_Thigh"]])
        self.t_mitte_j = 0.5 * (t_j[E.idx["Bip01_L_Thigh"]] + t_j[E.idx["Bip01_R_Thigh"]])
        self.ip = ip

    def lokal(self, clip, bild, dz=0.0):
        E = self.E
        t, R = E.lokal_erw(clip, bild)
        Me = E.fk(t, R)
        ip, ib = self.ip, E.idx["Bip01"]
        hm = Me[ip][:3, 3] + Me[ip][:3, :3] @ self.t_mitte_e
        tj = self.t_j.copy()
        tj[ib] = t[ib]
        tj[E.idx["Translation_Data"]] = t[E.idx["Translation_Data"]]
        p = hm + dump(np.array((self.DX, 0.0, dz))) - Me[ip][:3, :3] @ self.t_mitte_j
        tj[ip] = np.linalg.solve(Me[ib][:3, :3], p - Me[ib][:3, 3])
        return tj, R, Me


def seg_abst(p1, q1, p2, q2):
    d1, d2, r = q1 - p1, q2 - p2, p1 - p2
    a, e, f_ = d1 @ d1, d2 @ d2, d2 @ r
    c_ = d1 @ r
    b_ = d1 @ d2
    den = a * e - b_ * b_
    s = np.clip((b_ * f_ - c_ * e) / den, 0, 1) if den > 1e-12 else 0.0
    t = np.clip((b_ * s + f_) / e, 0, 1)
    s = np.clip((b_ * t - c_) / a, 0, 1)
    return float(np.linalg.norm(p1 + d1 * s - p2 - d2 * t))


def haut_erw(D, M):
    V = D["verts"]
    h = np.c_[V[:, :3], np.ones(len(V))]
    out = np.zeros((len(V), 3))
    for k in range(4):
        b = V[:, 7 + k].astype(int)
        Sm = np.einsum("nij,njk->nik", M[b], D["off"][b])
        out += V[:, 3 + k:4 + k] * np.einsum("nij,nj->ni", Sm, h)[:, :3]
    return tier(out)


def gewicht_erw(D, namen):
    V = D["verts"]
    w = np.zeros(len(V))
    for nm in namen:
        b = D["idx"][nm]
        w += np.where(V[:, 7:11].astype(int) == b, V[:, 3:7], 0.0).sum(1)
    return w


def sp_rig(E, J, aus):
    """Kopie von _arbeit/baer_junges/werkzeug/sp_skelett.py Abschnitt 2/3 mit Lage-Vektoren statt Faktoren."""
    D, idx = E.D, E.idx
    L = []
    G = {"VL": ["Bip01_L_Hand"], "VR": ["Bip01_R_Hand"], "HL": ["Bip01_L_Foot", "Bip01_L_Toe0"], "HR": ["Bip01_R_Foot", "Bip01_R_Toe0"]}
    SEL = {k: gewicht_erw(D, v) >= 0.5 for k, v in G.items()}
    GEL = {"VL": "Bip01_L_Hand", "VR": "Bip01_R_Hand", "HL": "Bip01_L_Foot", "HR": "Bip01_R_Foot"}
    L.append("== sp_rig: Becken-Regel (Hueftmitte = Erwachsener + DX %.4f m) ueber alle 15 Clips des Erwachsenen, Gelenk-Ebene, cm bei 1,0." % J.DX)
    L.append("   Stuetzbild = Haut der Pfote des Erwachsenen < 1,0 cm. dz = Hoehe stuetzendes Hand-/Sprunggelenk Junges - Erwachsener (vor dem Hub);")
    L.append("   gl = Gleiten der stuetzenden Vorderpfote (Spanne x_J - x_E je Stuetzphase); hi = Fehler hinten |x/z - DX|; quer = |y_J| - |y_E| (feste Querverschiebung)")
    res = {}
    for nm in CLIPS:
        c = D["clips"][nm]
        dzv, dzh, gl, hi, quer = [], [], [], [], []
        lauf = {"VL": [], "VR": []}
        for f in range(len(c["T"])):
            tj, R, Me = J.lokal(nm, f)
            Wn = E.fk(tj, R)
            P = haut_erw(D, c["M"][f])
            for kn in ("VL", "VR", "HL", "HR"):
                st = P[SEL[kn], 2].min() < 0.010
                a = tier(Me[idx[GEL[kn]]][:3, 3])
                n = tier(Wn[idx[GEL[kn]]][:3, 3])
                quer.append(abs(n[1]) - abs(a[1]))
                if kn[0] == "H":
                    hi.append(float(np.abs(n - a - np.array([J.DX, 0, 0]))[[0, 2]].max()))
                    if st:
                        dzh.append(n[2] - a[2])
                    continue
                if st:
                    dzv.append(n[2] - a[2])
                    lauf[kn].append(n[0] - a[0])
                else:
                    if len(lauf[kn]) > 1:
                        gl.append(max(lauf[kn]) - min(lauf[kn]))
                    lauf[kn] = []
            if f == len(c["T"]) - 1:
                for kn in ("VL", "VR"):
                    if len(lauf[kn]) > 1:
                        gl.append(max(lauf[kn]) - min(lauf[kn]))
        z = (100 * min(dzv), 100 * max(dzv)) if dzv else (0.0, 0.0)
        zh = (100 * min(dzh), 100 * max(dzh)) if dzh else (0.0, 0.0)
        res[nm] = dict(dz_vorn_cm=[round(z[0], 2), round(z[1], 2)], dz_hinten_cm=[round(zh[0], 2), round(zh[1], 2)],
                       gleiten_vorn_cm=round(100 * max(gl), 2) if gl else 0.0, hinten_max_cm=round(100 * max(hi), 2),
                       quer_cm=[round(100 * min(quer), 2), round(100 * max(quer), 2)])
        L.append("   %-16s dz vorn %+5.2f..%+5.2f | dz hinten %+5.2f..%+5.2f | gl %4.2f | hi %.2f | quer %+6.2f..%+6.2f" % (
            nm, z[0], z[1], zh[0], zh[1], res[nm]["gleiten_vorn_cm"], res[nm]["hinten_max_cm"], res[nm]["quer_cm"][0], res[nm]["quer_cm"][1]))
    L.append("== Kleinster Achsen-Abstand Hinterfuss (Sprunggelenk->Ballen) <-> Unterarm (Ellbogen->Handgelenk), gleiche Seite; und linkes <-> rechtes Bein")
    L.append("   (Unterschenkel+Fuss bzw. Unterarm, Achsen; Ruhe-Abstand Junges vorn/hinten in Klammern), cm bei 1,0:")
    t0, R0, _ = J.lokal("DeerStag_Idle01", 0)
    W0 = E.fk(J.t_j, E.R_loc)
    g0 = lambda k: tier(W0[idx[k]][:3, 3])
    ruhe_v = seg_abst(g0("Bip01_L_Forearm"), g0("Bip01_L_Hand"), g0("Bip01_R_Forearm"), g0("Bip01_R_Hand"))
    ruhe_h = seg_abst(g0("Bip01_L_Calf"), g0("Bip01_L_Foot"), g0("Bip01_R_Calf"), g0("Bip01_R_Foot"))
    for nm in CLIPS:
        c = D["clips"][nm]
        mj, ma, lrv, lrh = [], [], [], []
        for f in range(len(c["T"])):
            tj, R, Me = J.lokal(nm, f)
            Wn = E.fk(tj, R)
            for W_, m_ in ((Me, ma), (Wn, mj)):
                g = lambda k: tier(W_[idx[k]][:3, 3])
                m_.append(min(seg_abst(g(f"Bip01_{s}_Foot"), g(f"Bip01_{s}_Toe0"), g(f"Bip01_{s}_Forearm"), g(f"Bip01_{s}_Hand")) for s in "LR"))
            g = lambda k: tier(Wn[idx[k]][:3, 3])
            lrv.append(seg_abst(g("Bip01_L_Forearm"), g("Bip01_L_Hand"), g("Bip01_R_Forearm"), g("Bip01_R_Hand")))
            lrh.append(min(seg_abst(g("Bip01_L_Calf"), g("Bip01_L_Foot"), g("Bip01_R_Calf"), g("Bip01_R_Foot")),
                           seg_abst(g("Bip01_L_Foot"), g("Bip01_L_Toe0"), g("Bip01_R_Foot"), g("Bip01_R_Toe0"))))
        res[nm].update(hf_ua_min_cm=round(100 * min(mj), 1), hf_ua_min_erw_cm=round(100 * min(ma), 1), lr_vorn_min_cm=round(100 * min(lrv), 1),
                       lr_hinten_min_cm=round(100 * min(lrh), 1))
        L.append("   %-16s Hinterfuss-Unterarm min Junges %5.1f (Erw %5.1f) | links-rechts vorn min %5.1f (Ruhe %.1f) Bild %d | hinten min %5.1f (Ruhe %.1f) Bild %d" % (
            nm, 100 * min(mj), 100 * min(ma), 100 * min(lrv), 100 * ruhe_v, int(np.argmin(lrv)), 100 * min(lrh), 100 * ruhe_h, int(np.argmin(lrh))))
    open(aus, "w").write("\n".join(L) + "\n")
    for z_ in L:
        print(z_)
    return res


# ---------------------------------------------------------------- Splitter-Dreiecke: Kante tauschen -------------------------------
def qualitaet(V, tri):
    a, b, c = V[tri[..., 0]], V[tri[..., 1]], V[tri[..., 2]]
    L = np.stack((np.linalg.norm(b - a, axis=-1), np.linalg.norm(c - b, axis=-1), np.linalg.norm(a - c, axis=-1)), -1)
    A2 = np.linalg.norm(np.cross(b - a, c - a), axis=-1)
    return A2 / np.maximum(L.max(-1), 1e-12) ** 2, L.max(-1)          # Hoehe / laengste Kante


def splitter_tausch(V, T, Tg, q_max=0.08, l_min=0.02, runden=4):
    """Kante eines Splitter-Dreiecks (Hoehe/Laenge < q_max, laengste Kante > l_min) tauschen, wenn: die Kante keine UV-Naht ist
    (gleiche GLB-Punkte in beiden Dreiecken), die neue Kante noch nicht existiert, beide neuen Dreiecke besser sind als das schlechtere
    alte und die Normalen um < 30 Grad von der alten mittleren Normale abweichen. Punkte, UV und Textur bleiben unveraendert."""
    T, Tg = T.copy(), Tg.copy()
    getauscht = []
    for _ in range(runden):
        q, L = qualitaet(V, T)
        kanten = {}
        for t, tri in enumerate(T):
            for k in range(3):
                kanten.setdefault((tri[k], tri[(k + 1) % 3]), (t, k))
        n_neu = 0
        for t in np.argsort(q):
            if q[t] >= q_max or L[t] < l_min:
                continue
            tri = T[t]
            # laengste Kante (a -> b), c gegenueber
            Ls = [np.linalg.norm(V[tri[(k + 1) % 3]] - V[tri[k]]) for k in range(3)]
            k = int(np.argmax(Ls))
            a, b, c = tri[k], tri[(k + 1) % 3], tri[(k + 2) % 3]
            if (b, a) not in kanten:
                continue
            t2, k2 = kanten[(b, a)]
            tri2 = T[t2]
            d = tri2[(k2 + 2) % 3]
            if (c, d) in kanten or (d, c) in kanten or c == d:
                continue
            ga, gb, gc = Tg[t][k], Tg[t][(k + 1) % 3], Tg[t][(k + 2) % 3]
            ga2, gb2, gd = Tg[t2][(k2 + 1) % 3], Tg[t2][k2], Tg[t2][(k2 + 2) % 3]
            if ga != ga2 or gb != gb2:
                continue                                  # UV-Naht: nicht tauschen
            n3 = np.array([[c, a, d], [c, d, b]])
            q_alt = min(q[t], q[t2])
            q_neu, _ = qualitaet(V, n3)
            if q_neu.min() <= q_alt:
                continue
            nm = np.cross(V[b] - V[a], V[c] - V[a]) + np.cross(V[a] - V[b], V[d] - V[b])
            nm /= np.linalg.norm(nm)
            ok = True
            for tr in n3:
                nn = np.cross(V[tr[1]] - V[tr[0]], V[tr[2]] - V[tr[0]])
                if np.linalg.norm(nn) < 1e-14 or (nn / np.linalg.norm(nn)) @ nm < np.cos(np.radians(30)):
                    ok = False
            if not ok:
                continue
            T[t], T[t2] = n3[0], n3[1]
            Tg[t], Tg[t2] = np.array([gc, ga, gd]), np.array([gc, gd, gb])
            kanten = {}
            for tt, tr in enumerate(T):
                for kk in range(3):
                    kanten.setdefault((tr[kk], tr[(kk + 1) % 3]), (tt, kk))
            q[t], q[t2] = q_neu
            getauscht.append((int(t), int(t2), round(float(q_alt), 4), round(float(q_neu.min()), 4)))
            n_neu += 1
        if n_neu == 0:
            break
    return T, Tg, getauscht


def netz_pruef(T, n):
    E = np.sort(np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]])), axis=1)
    ue, ce = np.unique(E, axis=0, return_counts=True)
    return dict(offen=int((ce == 1).sum()), nicht_mannigfaltig=int((ce > 2).sum()), entartet=int((T[:, 0] == T[:, 1]).sum() + (T[:, 1] == T[:, 2]).sum() + (T[:, 0] == T[:, 2]).sum()))


# ---------------------------------------------------------------- bauen -----------------------------------------------------------
def bauen(P=PARAM):
    os.makedirs(SK, exist_ok=True)
    F = np.load(FORM_NPZ)
    V, T = F["V"], F["T"]
    E = Erw()
    mess = bein_messung(V, T, E)
    for k, m in mess.items():
        log("Beinachse %s: %d Schnitte, Winkel freie Achse <-> Knochen %.1f Grad (vorn/hinten frei %.1f, seitlich %.1f), Rest max %.2f / Mittel %.2f cm" % (
            k, m["n"], m["winkel"], m["vorn_hinten_frei"], m["seitlich_frei"], m["rest_max_cm"], m["rest_mittel_cm"]))
    pos, t_j, BW_j, info = skelett(E, P, mess)
    log("R gemessen %.4f, gesetzt %.3f; DX %.4f m; Netz-Versatz x %+.4f m; Q_H %.3f (Huefte |y| %.4f), Q_V %.3f (Schulter |y| %.4f); Fuss-Faktor %.3f;"
        " Hals %.3f m, Neigung %+.1f Grad, delta %+.1f Grad; Bein-Rest hinten %+.2f / vorn %+.2f cm" % (
            info["R_mess"], info["R"], info["DX"], info["versatz"], info["Q_H"], info["lat_h"], info["Q_V"], info["lat_v"], info["f_fuss"],
            info["hals_m"], info["hals_neig"], info["delta"], info["bein_rest_cm"]["hinten_x"], info["bein_rest_cm"]["vorn_x"]))
    Vs = V + np.array((info["versatz"], 0.0, 0.0))
    # Gelenke im Netz: Windungszahl und Abstand zur Haut
    innen = {}
    for nm in E.names:
        if nm in ("Dummy01", "Translation_Data", "Bip01"):
            continue
        p = pos[nm]
        innen[nm] = dict(windung=round(windungszahl(p, Vs, T), 3), haut_cm=round(100 * abstand_dreiecke(p, Vs, T), 2))
    for nm, v in innen.items():
        log("Gelenk %-18s (%6.3f %6.3f %6.3f) Windung %.3f, unter der Haut %5.2f cm" % (nm, *pos[nm], v["windung"], v["haut_cm"]))
    # Ausgaben
    pe = E.pos_e
    sk = {"faktoren": {"rumpf": info["R"], "beine": 1.0, "pfoten": round(info["f_fuss"], 5), "hals": "frei (C7 -> Atlas)", "kiefergelenk": "frei",
                       "dx_m": round(info["DX"], 5)},
          "namen": E.names, "eltern": [int(p) for p in E.par],
          "lage_E": {nm: [round(float(v), 6) for v in t_j[b]] for b, nm in enumerate(E.names)},
          "lage_E_erw": {nm: [round(float(v), 6) for v in E.t_e[b]] for b, nm in enumerate(E.names)},
          "ruhe_m": {nm: [round(float(v), 5) for v in pos[nm]] for nm in E.names},
          "ruhe_m_erw": {nm: [round(float(v), 5) for v in pe[nm]] for nm in E.names},
          "skala_m_je_roh": float(F["skala_m_je_roh"]), "R": info["R"], "R_gemessen": round(info["R_mess"], 4), "Q_H": round(info["Q_H"], 4),
          "Q_V": round(info["Q_V"], 4), "dx_m": round(info["DX"], 5), "delta_hals_grad": round(info["delta"], 2),
          "hals_neigung_grad": round(info["hals_neig"], 2), "fuss_faktor": round(info["f_fuss"], 4), "netz_versatz_x_m": round(info["versatz"], 5),
          "rahmen": "tier-Meter bei Groesse 1,0 (x vorn, y links, z oben), Skelettrahmen = Formrahmen + (netz_versatz_x_m, 0, 0); lage_E im Dump-Raum (E)",
          "param_formrahmen": {k: (list(v) if isinstance(v, tuple) else v) for k, v in P.items()},
          "gelenke_im_netz": innen,
          "beinachsen": {k: dict(winkel_grad=round(m["winkel"], 2), rest_max_cm=round(m["rest_max_cm"], 2), n=m["n"]) for k, m in mess.items()},
          "bein_rest_cm": info["bein_rest_cm"]}
    json.dump(sk, open(SK + "skelett_rig.json", "w"), indent=1)
    keep = {k: F[k] for k in F.files}
    # Splitter-Dreiecke (Hoehe < 8 % der laengsten Kante, Kante > 2 cm) per Kantentausch entschaerfen (Lauf 2 Optimierer: ein Splitter
    # an der rechten Flanke, Hoehe 5 mm / Laenge 12,5 cm, trug allein den Hoechstwert sigma1 5,4 in Rear); Punkte/UV/Textur bleiben
    q0, L0 = qualitaet(Vs, F["T"])
    T_neu, Tg_neu, getauscht = splitter_tausch(Vs, F["T"], F["T_glb"])
    q1, L1 = qualitaet(Vs, T_neu)
    pr0, pr1 = netz_pruef(F["T"], len(Vs)), netz_pruef(T_neu, len(Vs))
    assert (F["glb_punkt"][Tg_neu] == T_neu).all()
    assert pr1 == pr0, (pr0, pr1)
    log("Splitter: vorher %d Dreiecke mit Hoehe/Laenge < 0,08 und Kante > 2 cm, %d Kanten getauscht, nachher %d; Netz offen/nicht-mannigf./entartet %s -> %s" % (
        int(((q0 < 0.08) & (L0 > 0.02)).sum()), len(getauscht), int(((q1 < 0.08) & (L1 > 0.02)).sum()), pr0, pr1))
    keep["T"], keep["T_glb"] = T_neu, Tg_neu
    keep["T_form"], keep["T_glb_form"] = F["T"], F["T_glb"]
    keep["kantentausch"] = np.array(getauscht, dtype=np.float64).reshape(-1, 4)
    sk["splitter_tausch"] = dict(vorher=int(((q0 < 0.08) & (L0 > 0.02)).sum()), getauscht=len(getauscht), nachher=int(((q1 < 0.08) & (L1 > 0.02)).sum()),
                                 netz=pr1)
    json.dump(sk, open(SK + "skelett_rig.json", "w"), indent=1)
    keep["V"] = Vs
    keep["V_foto"] = F["V_foto"] + np.array((info["versatz"], 0.0, 0.0))
    keep["versatz_x"] = np.float64(info["versatz"])
    np.savez(SK + "netz_rig.npz", **keep)
    mj = {"beine": {k: {kk: (vv.tolist() if isinstance(vv, np.ndarray) else vv) for kk, vv in m.items()} for k, m in mess.items()},
          "gelenke_formrahmen": {s_: {k: v.round(5).tolist() for k, v in g.items()} for s_, g in info["gem"].items()}}
    json.dump(mj, open(SK + "mess_rig.json", "w"), indent=1)
    J = Junges(E, t_j, info["DX"])
    res = sp_rig(E, J, SK + "sp_rig.txt")
    sk["sp_rig"] = res
    json.dump(sk, open(SK + "skelett_rig.json", "w"), indent=1)
    log("geschrieben:", SK + "skelett_rig.json", SK + "netz_rig.npz", SK + "mess_rig.json", SK + "sp_rig.txt")
    return sk


if __name__ == "__main__":
    P = dict(PARAM)
    for a in sys.argv[2:]:
        k, v = a.split("=", 1)
        P[k] = tuple(float(x) for x in v.split(",")) if "," in v else float(v)
    if sys.argv[1] == "bauen":
        bauen(P)
