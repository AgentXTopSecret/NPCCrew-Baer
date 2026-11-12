# Lauf baer-gen-junges-v2 (12.11.2026), Bauer BEINE: die 13 Clips ausser Gehen/Rennen vom heutigen Generator-Jungen (ee7a0cce,
# Importer-Dump plan/dump/gen.txt) auf die KURZEN Beine umrechnen (PLAN.md 4.5.2). Neu (Vorbild baer_sitz_jfuss.py nur gelesen).
# Dazu der gemeinsame numpy-Kern (Gerippe, FK, Zwei-Knochen-IK, Haut), den auch baer_clips_gj2.py (Gehen/Rennen) benutzt.
# Je Bild:
#   1. Drehungen von Rumpf, Hals, Kopf, Kiefer, Schwanz, Schulterblaettern = Quelle (lokal).
#   2. Becken: Weltlage der Quelle, abgesenkt um (1 - f_h) x mittlere senkrechte Hoehe Huefte -> Sprunggelenk der STUETZENDEN Hinterbeine
#      (verallgemeinerte Becken-Regel; ohne Stuetzbein Mittel beider). Liegt/sitzt die Quelle, ist diese Hoehe klein -> kaum Absenkung.
#   3. Beine per Zwei-Knochen-IK (Pol aus dem Knie/Ellbogen der Quelle), Pfoten-WELTdrehung = Quelle. Stuetzpfoten (Quelle < 1 cm ueber
#      dem Boden): Gelenk an die Quell-Lage + Spur quer; freie Pfoten: neue Huefte/Schulter + f x (Gelenk - Huefte/Schulter) der Quelle;
#      Uebergang ueber 3 Bilder (weiches Stuetz-Gewicht).
#   4. Boden an der HAUT (Endgewichte): Stuetzpfoten tiefster Punkt auf 0 (Gelenk-Ziel z nachgefuehrt), sonst nichts unter -0,5 cm
#      (Koerper gehoben); ueberstreckte Stuetzbeine -> Koerper tiefer; zeitlich geglaettet.
#   5. Sitz-Trio: Vorbeugen (Wirbel nicken), bis die Vorderpfoten den Boden erreichen; Kopf haelt seine Weltneigung.
#   6. Eat: Hals/Kopf nicken zusaetzlich, bis die Schnauze den Boden erreicht (0..+2 cm), Brust/Ellbogen helfen.
# Ausgabe npz: <Clip>_R (Bilder x 26 x 3 x 3 lokale Drehungen, Dump-Raum), <Clip>_pel (Bilder x 3 Becken-Lage im Bip01-Raum, Dump-Raum E),
#   <Clip>_stuetz (Bilder x 4 Stuetz-Gewicht VL VR HL HR), <Clip>_dz (Bilder, Koerper-Hub in m). Fuer baer_export_gj2.py: neu=...
# Aufruf: python baer_umrechnen_gj2.py --skelett SK.json --netz NETZ.npz --gewichte GEW.npz --aus CLIPS.npz [--nur Clip,Clip] [--alt ALT.npz]
#   --alt: vorhandene Clips-Datei, deren nicht neu gerechnete Clips uebernommen werden (GESICHT rechnet nur Eat/Death/Dead/Sitz neu).
# Rahmen tier-Meter (x vorn, y links, z oben); Dump-Raum = (y, z, -x) x 0,544. Statisch/offline, nicht gespielt.
import argparse
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_export_gj2 as X  # noqa: E402

M2U = 0.544
A_TD = np.array([[0, 0, -1.0], [1, 0, 0], [0, 1, 0]])      # Richtung dump -> tier
QUELLE_DUMP = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/plan/dump/gen.txt"
SKELETT_ALT = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/quelle/gen/skelett_rig.json"
CLIPS = ["DeerStag_Idle01", "DeerStag_Walk", "DeerStag_Run", "DeerStag_Death", "DeerStag_Dead", "NCBear_Rear", "NCBear_SwipeL",
         "NCBear_SwipeR", "NCBear_Slam", "NCBear_Bite", "NCBear_Maul", "NCBear_Eat", "NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp"]
UMRECHNEN = [c for c in CLIPS if c not in ("DeerStag_Walk", "DeerStag_Run")]
SITZ = ("NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp")
PF = ("VL", "VR", "HL", "HR")
BEIN = {"VL": ("Bip01_L_UpperArm", "Bip01_L_Forearm", "Bip01_L_Hand"), "VR": ("Bip01_R_UpperArm", "Bip01_R_Forearm", "Bip01_R_Hand"),
        "HL": ("Bip01_L_Thigh", "Bip01_L_Calf", "Bip01_L_Foot"), "HR": ("Bip01_R_Thigh", "Bip01_R_Calf", "Bip01_R_Foot")}
T0 = time.time()


def log(*a):
    print("UMR", round(time.time() - T0, 1), *a, flush=True)


def tier(P):
    P = np.asarray(P, float)
    return np.stack((-P[..., 2], P[..., 0], P[..., 1]), -1) / M2U


def dump(T):
    return X.dump(T)


def sst(a, b, x):
    t = np.clip((np.asarray(x, float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def rot(achse, grad):
    a = np.asarray(achse, float)
    a = a / np.linalg.norm(a)
    t = math.radians(grad)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K


def rx(g):
    return rot((1, 0, 0), g)


def ry(g):           # +g: Nase bzw. Zehe nach unten (wie baer_clips_rig.py)
    return rot((0, 1, 0), g)


def rz(g):           # +g: Nase nach links
    return rot((0, 0, 1), g)


def euler(yaw=0.0, pitch=0.0, roll=0.0):
    return rz(yaw) @ ry(pitch) @ rx(roll)


def orthonorm(R):
    u, _s, vt = np.linalg.svd(R)
    return u @ vt


class Gerippe:
    """Skelett des neuen Jungen (Ruhe-Drehungen 2c, Lagen skelett_gj2.json), FK, IK, Haut."""

    def __init__(self, skelett, netz=None, gewichte=None):
        self.sk = X.SkelettRig(skelett)
        s = self.sk
        self.names, self.par, self.idx, self.nb = s.names, s.par, s.idx, s.nb
        self.R_loc0 = s.R_loc.copy()
        self.t_j = s.t_j.copy()
        self.BW = s.BW_j.copy()
        self.BWr = np.array([m[:3, :3] for m in self.BW])
        self.BWr_inv = np.array([np.linalg.inv(m) for m in self.BWr])
        self.INV = np.array([np.linalg.inv(m) for m in self.BW])
        self.J = {n: tier(self.BW[self.idx[n]][:3, 3]) for n in self.names}
        js = json.load(open(skelett))
        self.f_h = js["faktoren"]["beine_hinten"]
        self.f_v = js["faktoren"]["beine_vorn"]
        self.leg = {}
        for k, (o, u, e) in BEIN.items():
            a = np.linalg.norm(self.J[u] - self.J[o])
            b = np.linalg.norm(self.J[e] - self.J[u])
            u0 = (self.J[u] - self.J[o]) / a
            v0 = (self.J[e] - self.J[u]) / b
            n0 = np.cross(u0, v0)
            n0 /= np.linalg.norm(n0)
            self.leg[k] = dict(o=o, u=u, e=e, a=a, b=b, F1=np.stack((u0, n0, np.cross(u0, n0)), 1),
                               F2=np.stack((v0, n0, np.cross(v0, n0)), 1), pol=np.array((-1.0, 0, 0)) if k[0] == "V" else np.array((1.0, 0, 0)))
        self.netz = None
        if netz is not None:
            N = np.load(netz)
            G = np.load(gewichte)
            nam = [str(n) for n in G["namen"]]
            W = np.zeros((len(N["V"]), self.nb))
            for i, n in enumerate(nam):
                W[:, self.idx[n]] = G["W"][:, i]
            self.V = N["V"].astype(float)
            self.W = W
            self.bi = np.nonzero(W.max(0) > 0)[0]
            self.H0 = np.c_[dump(self.V), np.ones(len(self.V))]
            self.netz = N
            self.pfote = {}
            for k in PF:
                e = BEIN[k][2]
                wsum = W[:, self.idx[e]] + (W[:, self.idx[e.replace("Foot", "Toe0")]] if "Foot" in e else 0)
                self.pfote[k] = np.nonzero(wsum >= 0.5)[0]
            self.kopf = np.nonzero(W[:, self.idx["Bip01_Head"]] + W[:, self.idx["Bip01_Jaw"]] >= 0.5)[0]

    # ---------------------------------------------------------------- FK / Weltdrehungen
    def fk(self, t_loc, R_loc):
        return self.sk.fk(t_loc, R_loc)

    def welt_aus_tier(self, b, Q):
        """Weltdrehung (Dump) von Knochen b aus der Drehung Q gegen die Ruhe (tier)."""
        return A_TD.T @ Q @ A_TD @ self.BWr[b]

    def tier_aus_welt(self, b, Wd):
        return A_TD @ Wd @ self.BWr_inv[b] @ A_TD.T

    def lokal(self, Wrot, b, Wpar):
        return np.linalg.solve(Wpar, Wrot)

    # ---------------------------------------------------------------- Zwei-Knochen-IK (tier)
    def ik(self, k, H, A, pol, ueber=None):
        """Huefte/Schulter H, Ziel-Gelenk A, Pol (tier). Rueckgabe Drehungen (tier, gegen Ruhe) oben/unten, Knie, erreichtes A, Streckung."""
        L = self.leg[k]
        a, b = L["a"], L["b"]
        d = A - H
        ln = float(np.linalg.norm(d))
        st = ln / (a + b)
        maxd = (a + b) * 0.998
        if ln > maxd:
            if ueber is not None:
                ueber.append((k, round(st, 4)))
            d = d * (maxd / ln)
            ln = maxd
        ln = max(ln, abs(a - b) * 1.002 + 1e-4)
        e = d / ln
        along = (a * a - b * b + ln * ln) / (2.0 * ln)
        h = math.sqrt(max(a * a - along * along, 0.0))
        p = pol - e * (pol @ e)
        if np.linalg.norm(p) < 1e-8:
            p = L["pol"] - e * (L["pol"] @ e)
        p /= np.linalg.norm(p)
        K = H + e * along + p * h
        A2 = H + e * ln
        y1 = (K - H) / a
        y2 = (A2 - K) / b
        n = np.cross(y1, y2)
        if np.linalg.norm(n) < 1e-8:
            n = np.cross(p, e)
        n /= np.linalg.norm(n)
        F1 = np.stack((y1, n, np.cross(y1, n)), 1)
        F2 = np.stack((y2, n, np.cross(y2, n)), 1)
        return F1 @ L["F1"].T, F2 @ L["F2"].T, K, A2, st

    # ---------------------------------------------------------------- Pose aus Weltdrehungen (tier) + Becken
    def pose(self, Qwelt, pel_tier):
        """Qwelt: {Knochen: 3x3 Drehung gegen Ruhe (tier)} fuer ALLE Knochen ausser Wurzeln (fehlende = Elterndrehung, d. h. lokal Ruhe).
        pel_tier: Beckengelenk (tier, Welt). Rueckgabe R_loc (nb x 3 x 3, Dump), t_loc, M (Welt 4x4)."""
        nb = self.nb
        R_loc = self.R_loc0.copy()
        t_loc = self.t_j.copy()
        Wd = np.zeros((nb, 3, 3))
        M = np.zeros((nb, 4, 4))
        ib, ip = self.idx["Bip01"], self.idx["Bip01_Pelvis"]
        for b, nm in enumerate(self.names):
            pa = self.par[b]
            if nm in ("Dummy01", "Bip01", "Translation_Data"):
                Wd[b] = self.BWr[b]
                M[b] = self.BW[b]
                continue
            if nm in Qwelt:
                Wd[b] = self.welt_aus_tier(b, Qwelt[nm])
            else:
                Wd[b] = Wd[pa] @ self.R_loc0[b]
            R_loc[b] = np.linalg.solve(Wd[pa], Wd[b])
            if b == ip:
                t_loc[b] = np.linalg.solve(M[ib][:3, :3], dump(pel_tier) - M[ib][:3, 3])
            m = np.eye(4)
            m[:3, :3] = R_loc[b]
            m[:3, 3] = t_loc[b]
            M[b] = M[pa] @ m
        return R_loc, t_loc, M

    def gelenk(self, M, nm):
        return tier(M[self.idx[nm]][:3, 3])

    def haut(self, M, nur=None):
        bi = self.bi
        Sk = np.einsum("bij,bjk->bik", M[bi], self.INV[bi])[:, :3, :]
        if nur is None:
            return tier(np.einsum("bij,nj,nb->ni", Sk, self.H0, self.W[:, bi], optimize=True))
        return tier(np.einsum("bij,nj,nb->ni", Sk, self.H0[nur], self.W[nur][:, bi], optimize=True))


# =================================================================================================================================
# Quelle: Generator-Junges heute (Dump), eigene Haut zum Messen der Stuetzpfoten
# =================================================================================================================================
def lade_quelle():
    sys.path.insert(0, "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/gegen/werkzeug")
    import g_lib as g
    d = g.lies(QUELLE_DUMP)
    pf = {}
    for k, (o, u, e) in BEIN.items():
        kn = [e] + ([e.replace("Foot", "Toe0")] if "Foot" in e else [])
        pf[k] = np.nonzero(g.gewicht(d, kn) >= 0.5)[0]
    d["pf_idx"] = pf
    d["g"] = g
    return d


def quelle_bild(Q, clip, f):
    M = Q["clips"][clip]["M"][f]
    g = Q["g"]
    names = Q["names"]
    R_loc = np.zeros((len(names), 3, 3))
    for b in range(len(names)):
        pa = Q["par"][b]
        L = M[b] if pa < 0 else np.linalg.solve(M[pa], M[b])
        R_loc[b] = L[:3, :3]
    J = {n: tier(M[b][:3, 3]) for b, n in enumerate(names)}
    Wt = {n: A_TD @ M[b][:3, :3] @ np.linalg.inv(np.linalg.inv(Q["off"][b])[:3, :3]) @ A_TD.T for b, n in enumerate(names)}
    P = g.haut(Q, M)
    tief = {k: float(P[Q["pf_idx"][k], 2].min()) for k in PF}
    return dict(M=M, R_loc=R_loc, J=J, Q=Wt, tief=tief, haut_min=float(P[:, 2].min()))


# =================================================================================================================================
# Umrechnen eines Clips
# =================================================================================================================================
def stuetz_gewicht(tief, schwelle=0.010, weich=0.012):
    """Stuetz-Gewicht je Bild aus der tiefsten Pfotenhaut der Quelle: 1 unter 1 cm, 0 ueber 2,2 cm; ueber 3 Bilder geglaettet."""
    s = 1.0 - sst(schwelle, schwelle + weich, np.asarray(tief))
    if len(s) >= 3:
        sp = np.pad(s, 1, mode="edge")
        s = np.convolve(sp, np.array((0.25, 0.5, 0.25)), mode="valid")
    return np.clip(s, 0, 1)


def glatt(x, n=5):
    if len(x) < n:
        return x
    k = np.array((1, 2, 3, 2, 1), float) / 9.0
    return np.convolve(np.pad(x, 2, mode="edge"), k, mode="valid")


def erw_schnauze(clip):
    """Tiefste Kopfhaut des 2c (Groesse 1,0) je Bild -- Bezug fuer Fressen (PLAN 3.2: Bilder, in denen der 2c < 1 cm hat)."""
    import pickle
    sys.path.insert(0, "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/gegen/werkzeug")
    import g_lib as g
    e = pickle.load(open(X.DUMP_ERW, "rb"))
    d = dict(V=np.asarray(e["verts"]), off=np.asarray(e["off"]), idx=e["idx"])
    kopf = np.nonzero(g.gewicht(d, ["Bip01_Head", "Bip01_Jaw"]) >= 0.5)[0]
    M = np.asarray(e["clips"][clip]["M"])
    return np.array([g.haut(d, M[f])[kopf, 2].min() for f in range(len(M))])


def umrechnen(G, Q, clip, par):
    """Gibt R (Bilder x nb x 3 x 3), pel (Bilder x 3), stuetz (Bilder x 4), dz (Bilder), info zurueck."""
    nf = len(Q["clips"][clip]["M"])
    QB = [quelle_bild(Q, clip, f) for f in range(nf)]
    alt = json.load(open(SKELETT_ALT))["ruhe_m"]
    J_alt = {n: np.array(v) for n, v in alt.items()}
    # Stuetze: Quell-Pfote am Boden UND Becken aufrecht (liegt/rollt die Quelle, sind alle Beine frei)
    auf = np.array([(qb["Q"]["Bip01_Pelvis"] @ np.array((0, 0, 1.0)))[2] for qb in QB])
    auf_w = sst(0.45, 0.75, auf)
    st = {k: stuetz_gewicht([qb["tief"][k] for qb in QB]) * auf_w for k in PF}
    info = dict(bilder=nf, ueber=[])
    # Absenkung je Bild: (1 - f_h) x senkrechte Hoehe Huefte -> Sprunggelenk (stuetzende Hinterbeine), geglaettet
    ab = np.zeros(nf)
    for f, qb in enumerate(QB):
        J = qb["J"]
        ws, hs = 1e-3, 0.0
        for k in ("HL", "HR"):
            o, u, e = BEIN[k]
            w = st[k][f] + 1e-3
            hs += w * max(J[o][2] - J[e][2], 0.0)
            ws += w
        ab[f] = -(1.0 - G.f_h) * hs / ws * auf_w[f]
    ab = glatt(ab)
    hub = np.zeros(nf)
    vorb = np.zeros(nf)
    nick = np.zeros(nf)
    zz = {k: np.zeros(nf) for k in PF}
    zug = {k: np.ones(nf) for k in PF}           # Stuetzziel zur Huefte ziehen (1 = Quell-Lage), wenn unerreichbar
    # Fressen: Ziel-Hoehe der Schnauze je Bild (2c < 1 cm -> 0,01 m; sonst 0,7 x 2c, hoechstens Quelle)
    eat_ziel = None
    if clip == "NCBear_Eat" and par.get("eat", True):
        e2c = erw_schnauze(clip)
        eat_ziel = np.where(e2c < 0.01, 0.010, 0.7 * e2c)
        info["eat_2c_boden_bilder"] = int((e2c < 0.01).sum())

    def los(f):
        return bild(G, QB[f], J_alt, ab[f] + hub[f], {k: st[k][f] for k in PF}, {k: zz[k][f] for k in PF},
                    {k: zug[k][f] for k in PF}, vorb[f], nick[f])
    for runde in range(par["runden"]):
        for f in range(nf):
            # Sitz: Vorbeugen, bis die stuetzenden Vorderbeine den Boden erreichen (Halbierung 0..vorbeug_max)
            if clip in SITZ and par.get("vorbeugen", True) and max(st["VL"][f], st["VR"][f]) > 0.5:
                lo, hi = 0.0, par["vorbeug_max"]
                vorb[f] = 0.0
                if los(f)[3]["v_streck"] > 0.97:
                    for _ in range(14):
                        mid = 0.5 * (lo + hi)
                        vorb[f] = mid
                        if los(f)[3]["v_streck"] > 0.97:
                            lo = mid
                        else:
                            hi = mid
                    vorb[f] = hi
            # Fressen: Nicken (Hals 0,55 + Kopf 1,0), bis die tiefste Kopfhaut die Ziel-Hoehe erreicht
            if eat_ziel is not None and runde == 0:
                # Abtasten 0..eat_max (5 Grad), dann fein: kleinster Winkel, der die Ziel-Hoehe erreicht, sonst der tiefste
                hs = []
                for n_ in np.arange(0.0, par["eat_max"] + 1e-9, 5.0):
                    nick[f] = n_
                    hs.append((float(G.haut(los(f)[2], G.kopf)[:, 2].min()), n_))
                ok_ = [n_ for h_, n_ in hs if h_ <= eat_ziel[f]]
                if ok_:
                    lo, hi = max(ok_[0] - 5.0, 0.0), ok_[0]
                    for _ in range(8):
                        mid = 0.5 * (lo + hi)
                        nick[f] = mid
                        if float(G.haut(los(f)[2], G.kopf)[:, 2].min()) > eat_ziel[f]:
                            lo = mid
                        else:
                            hi = mid
                    nick[f] = hi
                else:
                    nick[f] = min(hs)[1]
            R, pel, M, dd = los(f)
            P = G.haut(M)
            stz = []
            for k in PF:
                low = float(P[G.pfote[k], 2].min())
                if st[k][f] > 0.5:
                    zz[k][f] -= low
                    stz.append(low)
                    if dd["streck"][k] > 0.97:
                        zug[k][f] = max(zug[k][f] - 0.08, 0.3)
            pfoten = np.concatenate([G.pfote[k] for k in PF if st[k][f] > 0.5]) if stz else np.zeros(0, int)
            rest = np.ones(len(P), bool)
            rest[pfoten] = False
            low_r = float(P[rest, 2].min())
            if low_r < -0.003:
                hub[f] += -low_r
            elif not stz and low_r > 0.012 and auf_w[f] < 0.5:
                hub[f] -= low_r - 0.004                          # liegt: Koerper bis auf den Boden
        if runde < par["runden"] - 1:
            hub = glatt(hub)
            vorb = glatt(vorb)
            nick = glatt(nick)
    R_all = np.zeros((nf, G.nb, 3, 3))
    pel_all = np.zeros((nf, 3))
    pmin, pst, kz = [], [], []
    for f in range(nf):
        R, pel, M, dd = los(f)
        R_all[f], pel_all[f] = R, pel
        P = G.haut(M)
        pmin.append(float(P[:, 2].min()))
        pst += [float(P[G.pfote[k], 2].min()) for k in PF if st[k][f] > 0.5]
        kz.append(float(P[G.kopf, 2].min()))
        info["ueber"] += [(f,) + u for u in dd["ueber"]]
    info["ueber_n"] = len(info["ueber"])
    info["ueber"] = info["ueber"][:8]
    info["boden_min_cm"] = round(100 * min(pmin), 2)
    info["stuetz_cm"] = [round(100 * min(pst), 2), round(100 * max(pst), 2)] if pst else None
    info["hub_cm"] = [round(100 * float(hub.min()), 2), round(100 * float(hub.max()), 2)]
    info["absenk_cm"] = [round(100 * float(ab.min()), 2), round(100 * float(ab.max()), 2)]
    info["vorbeugen_grad_max"] = round(float(vorb.max()), 1)
    info["nick_grad_max"] = round(float(nick.max()), 1)
    info["kopf_min_cm"] = [round(100 * min(kz), 2), round(100 * max(kz), 2)]
    if eat_ziel is not None:
        kz = np.array(kz)
        m = eat_ziel <= 0.0101
        info["eat_schnauze_boden_cm"] = [round(100 * float(kz[m].min()), 2), round(100 * float(kz[m].max()), 2)]
    info["zug_min"] = {k: round(float(zug[k].min()), 2) for k in PF}
    return R_all, pel_all, np.stack([st[k] for k in PF], 1), ab + hub, info


def bild(G, qb, J_alt, dz, sw, zz, zug, vorbeug, nick):
    """Ein Bild: Rumpf aus der Quelle (Weltdrehungen), Becken abgesenkt, Beine per IK. Rueckgabe R, Becken-Lage lokal, M, Daten."""
    names = G.names
    Qw = {}
    Wd = {"Bip01": G.BWr[G.idx["Bip01"]]}
    Rq = qb["R_loc"]
    for b, nm in enumerate(names):
        if nm in ("Dummy01", "Bip01", "Translation_Data"):
            continue
        pa = names[G.par[b]]
        Wd[nm] = (Wd[pa] if pa in Wd else G.BWr[G.par[b]]) @ Rq[b]
        Qw[nm] = G.tier_aus_welt(b, Wd[nm])
    if vorbeug:
        # Sitz: ganzer Rumpf nach vorn (Becken 0,35 / Lende 0,65 / Brust 1,0 des Winkels, Welt), Hals/Kopf halten ihre Weltneigung
        Qw["Bip01_Pelvis"] = ry(0.35 * vorbeug) @ Qw["Bip01_Pelvis"]
        Qw["Bip01_Spine"] = ry(0.65 * vorbeug) @ Qw["Bip01_Spine"]
        for nm in ("Bip01_Spine1", "Bip01_L_Clavicle", "Bip01_R_Clavicle"):
            Qw[nm] = ry(vorbeug) @ Qw[nm]
    if nick:
        # Fressen: Hals 0,9 / Kopf 1,0 des Winkels nach unten, Brust bis 12 Grad mit (Schultern tiefer, Ellbogen beugen per IK)
        Qw["Bip01_Neck"] = ry(0.9 * nick) @ Qw["Bip01_Neck"]
        Qw["Bip01_Head"] = ry(nick) @ Qw["Bip01_Head"]
        Qw["Bip01_Jaw"] = ry(nick) @ Qw["Bip01_Jaw"]
        for nm in ("Bip01_Spine1", "Bip01_L_Clavicle", "Bip01_R_Clavicle"):
            Qw[nm] = ry(min(0.2 * nick, 12.0)) @ Qw[nm]
    pel = qb["J"]["Bip01_Pelvis"] + np.array((0.0, 0.0, dz))
    _R, _t, M0 = G.pose(Qw, pel)
    dd = dict(ueber=[], streck={})
    for k, (o, u, e) in BEIN.items():
        H = G.gelenk(M0, o)
        Ho, Ao, Ko = qb["J"][o], qb["J"][e], qb["J"][u]
        f_ = G.f_h if k[0] == "H" else G.f_v
        dy = G.J[o][1] - J_alt[o][1]
        frei = H + f_ * (Ao - Ho)
        steh = np.array((Ao[0], Ao[1] + dy, Ao[2] + zz[k]))
        # unerreichbar: waagerecht zur Huefte ziehen (zug < 1)
        steh[:2] = H[:2] + zug[k] * (steh[:2] - H[:2])
        w = sw[k]
        A = w * steh + (1 - w) * frei
        e_ = (Ao - Ho) / max(np.linalg.norm(Ao - Ho), 1e-9)
        pol = (Ko - Ho) - e_ * ((Ko - Ho) @ e_)
        if np.linalg.norm(pol) < 1e-4:
            pol = G.leg[k]["pol"]
        Ro, Ru, K, A2, stv = G.ik(k, H, A, pol, dd["ueber"])
        dd["streck"][k] = stv
        Qw[o], Qw[u], Qw[e] = Ro, Ru, qb["Q"][e]
        if k[0] == "H":
            Qw[e.replace("Foot", "Toe0")] = qb["Q"][e.replace("Foot", "Toe0")]
    dd["v_streck"] = max(dd["streck"]["VL"] if sw["VL"] > 0.5 else 0.0, dd["streck"]["VR"] if sw["VR"] > 0.5 else 0.0)
    R, t, M = G.pose(Qw, pel)
    return R, t[G.idx["Bip01_Pelvis"]], M, dd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skelett", required=True)
    ap.add_argument("--netz", required=True)
    ap.add_argument("--gewichte", required=True)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--nur", default="")
    ap.add_argument("--alt", default="")
    ap.add_argument("--info", default="")
    a = ap.parse_args()
    G = Gerippe(a.skelett, a.netz, a.gewichte)
    Q = lade_quelle()
    nur = [c for c in a.nur.split(",") if c] or UMRECHNEN
    out = dict(np.load(a.alt)) if a.alt else {}
    par = dict(runden=5, vorbeug_max=60.0, eat_max=70.0)
    infos = {}
    for clip in nur:
        R, pel, st, dz, info = umrechnen(G, Q, clip, par)
        out[clip + "_R"] = R
        out[clip + "_pel"] = pel
        out[clip + "_stuetz"] = st
        out[clip + "_dz"] = dz
        infos[clip] = info
        log(clip, json.dumps(info))
    np.savez(a.aus, **out)
    if a.info:
        json.dump(infos, open(a.info, "w"), indent=1)
    log("->", a.aus)


if __name__ == "__main__":
    main()
