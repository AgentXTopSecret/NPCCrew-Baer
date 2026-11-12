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
#      Nachbesserung 12.11. (PRUEF_TECHNIK 7.2, Maengel T2): die Quelle schiebt beim Hinsetzen/Aufstehen beide Hinterpfoten 0,2-1,0 cm
#      UEBER dem Boden nach vorn/hinten (2-8 cm je Bild); die Boden-Regel drueckte sie auf 0 -> Schleifen auf der Ferse ~40 cm. Jetzt
#      "umsetzen": bewegt sich das Quell-Gelenk einer Stuetz-Hinterpfote waagerecht, wird ihre tiefste Haut auf bis zu PAR umsetzen
#      (2,5 cm) gehoben (weich ueber die Geschwindigkeit 0,4..1,2 cm je Bild, zeitlich geglaettet) -- sie setzt um statt zu wischen.
#   6. Eat: Fress-Grad s (0..1) je Bild -- Brust/Lende beugen nach vorn (Brust bis PAR_EAT brust), vorn kauern (Ellbogen beugen per IK),
#      Hals und Kopf folgen der Brust; die Vorderpfoten stehen im GANZEN Clip gleich etwas weiter hinten und weiter auseinander (fest je
#      Clip, also kein Rutschen), damit die Schnauze VOR den Pfoten den Boden erreicht (0..+2 cm) ohne Kopf im Unterarm. (12.11.,
#      Nachbesserung: das reine Kopf-Nicken bis 50 Grad kam nur bis 20,7 cm ueber den Boden -- der Hals der kurzbeinigen Form ist zu kurz.)
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
SCHLEIFEN = ("DeerStag_Idle01", "NCBear_Eat", "NCBear_Sit")
PF = ("VL", "VR", "HL", "HR")
BEIN = {"VL": ("Bip01_L_UpperArm", "Bip01_L_Forearm", "Bip01_L_Hand"), "VR": ("Bip01_R_UpperArm", "Bip01_R_Forearm", "Bip01_R_Hand"),
        "HL": ("Bip01_L_Thigh", "Bip01_L_Calf", "Bip01_L_Foot"), "HR": ("Bip01_R_Thigh", "Bip01_R_Calf", "Bip01_R_Foot")}
T0 = time.time()
# Fressen (Probe log/eat_probe4.json im Bauer-BEINE-Ordner): Brust 40 Grad + 8 cm kauern erreicht den Boden 1,2 cm mit Kopf/Unterarm 2,8 cm
# (Hoechstwerte 45 Grad / 9 cm, damit der Fress-Grad s < 1 bleibt),
# Vorderpfoten fest 12 cm zurueck / 4 cm weiter aussen; Schnauze dann vor den Pfotenspitzen
PAR_EAT = dict(brust=45.0, lende=0.4, kauern=-0.09, hals=0.0, kopf=0.0, pfote_dx=-0.12, pfote_dy=0.04, kopf_arm_min=0.010)


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
            self.gew_pfad = gewichte
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


def normalen(P, T):
    fn = np.cross(P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]])
    acc = np.zeros_like(P)
    for k in range(3):
        np.add.at(acc, T[:, k], fn)
    return acc / np.maximum(np.linalg.norm(acc, axis=1, keepdims=True), 1e-12)


def pfoten_ineinander(P, Nv, ia, ib, tol=0.002):
    """Punkte der Pfote a, die in Pfote b liegen (naechster b-Punkt, Normale zeigt weg) -- und umgekehrt; nur nahe Punkte (< 3 cm)."""
    n = 0
    for x, y in ((ia, ib), (ib, ia)):
        A, B = P[x], P[y]
        d = ((A[:, None, :] - B[None, :, :]) ** 2).sum(2)
        j = d.argmin(1)
        nah = np.sqrt(d[np.arange(len(A)), j]) < 0.03
        innen = ((A - B[j]) * Nv[y][j]).sum(1) < -tol
        n += int((nah & innen).sum())
    return n


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
    # Sitz-Trio: Stuetz-Hinterpfote, deren Quell-Gelenk waagerecht wandert, umsetzen (heben) statt am Boden schleifen
    lift = {k: np.zeros(nf) for k in PF}
    if clip in SITZ and par.get("umsetzen", 0.0) > 0 and nf >= 3:
        for k in ("HL", "HR"):
            A_ = np.array([qb["J"][BEIN[k][2]] for qb in QB])
            v_ = np.zeros(nf)
            v_[1:-1] = 0.5 * np.linalg.norm(A_[2:, :2] - A_[:-2, :2], axis=1)
            lift[k] = par["umsetzen"] * np.clip(glatt(sst(0.004, 0.012, v_)), 0.0, 1.0)
            lift[k][[0, nf - 1]] = 0.0
        info["umsetzen_cm_max"] = {k: round(100 * float(lift[k].max()), 2) for k in ("HL", "HR")}
        info["umsetzen_bilder"] = {k: [int(i) for i in np.nonzero(lift[k] > 0.001)[0]] for k in ("HL", "HR")}
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
    weg = {k: np.zeros((nf, 3)) for k in PF}     # Liegen: freie Pfote von der anderen weg (3D)
    if not hasattr(G, "pfote_ok"):
        kr_ = np.zeros(len(G.V), bool)
        try:
            kr_ = np.load(G.gew_pfad)["kralle"].astype(bool)
        except Exception:
            pass
        G.pfote_ok = {k: G.pfote[k][~kr_[G.pfote[k]]] for k in PF}
    # Fressen: Ziel-Hoehe der Schnauze je Bild (2c < 1 cm -> 0,01 m; sonst 0,7 x 2c, hoechstens Quelle)
    eat_ziel = None
    if clip == "NCBear_Eat" and par.get("eat", True):
        e2c = erw_schnauze(clip)
        eat_ziel = np.where(e2c < 0.01, 0.010, 0.7 * e2c)
        info["eat_2c_boden_bilder"] = int((e2c < 0.01).sum())

    def los(f):
        return bild(G, QB[f], J_alt, ab[f] + hub[f], {k: st[k][f] for k in PF}, {k: zz[k][f] for k in PF},
                    {k: zug[k][f] for k in PF}, vorb[f], nick[f], {k: weg[k][f] for k in PF}, fress=eat_ziel is not None)
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
            # Fressen: Fress-Grad s (Brust beugen + vorn kauern, PAR_EAT), bis die tiefste Kopfhaut die Ziel-Hoehe erreicht
            if eat_ziel is not None and runde == 0:
                # Abtasten 0..1 (0,1), dann fein: kleinster Grad, der die Ziel-Hoehe erreicht, sonst der tiefste; Kopf nie naeher als
                # kopf_arm_min an Unterarm/Vorderpfote (sonst steckt er drin) und Schnauze vor den Handgelenken
                hs = []
                for n_ in np.arange(0.0, 1.0 + 1e-9, 0.1):
                    nick[f] = n_
                    Mk = los(f)[2]
                    Pk = G.haut(Mk, G.kopf)
                    i_ = int(np.argmin(Pk[:, 2]))
                    x_pf = max(float(G.gelenk(Mk, "Bip01_L_Hand")[0]), float(G.gelenk(Mk, "Bip01_R_Hand")[0]))
                    if n_ > 0 and (Pk[i_, 0] < x_pf + 0.10 or kopf_arm_abstand(G, Mk, Pk) < PAR_EAT["kopf_arm_min"]):
                        break
                    hs.append((float(Pk[i_, 2]), n_))
                ok_ = [n_ for h_, n_ in hs if h_ <= eat_ziel[f]]
                if ok_:
                    lo, hi = max(ok_[0] - 0.1, 0.0), ok_[0]
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
                    zz[k][f] -= low - lift[k][f]
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
            # Liegen: Pfoten nicht ineinander (Kevin 12.11. zum Standard-Jungen: "die beine stecken ineinander") -- die hoehere Pfote
            # eines Paars (L/R) wird angehoben, bis keine ihrer Punkte mehr in der anderen liegen
            if auf_w[f] < 0.5:
                Nv = normalen(P, G.netz["T"])
                for a_, b_ in (("HL", "HR"), ("VL", "VR")):
                    n_in = pfoten_ineinander(P, Nv, G.pfote_ok[a_], G.pfote_ok[b_])
                    if n_in > 0:
                        hoch, tief = (a_, b_) if P[G.pfote[a_], 2].mean() > P[G.pfote[b_], 2].mean() else (b_, a_)
                        if st[hoch][f] < 0.5:
                            r_ = P[G.pfote[hoch]].mean(0) - P[G.pfote[tief]].mean(0)
                            r_ = r_ / max(np.linalg.norm(r_), 1e-9)
                            weg[hoch][f] += 0.015 * r_
        if runde < par["runden"] - 1:
            hub = glatt(hub)
            vorb = glatt(vorb)
            nick = glatt(nick)
    # Schleifen (Idle, Eat, Sit): letztes Bild = erstes -- die je Bild gefundenen Groessen laufen ueber die letzten 8 Bilder weich auf Bild 0
    if clip in SCHLEIFEN:
        n8 = min(8, nf - 1)
        arrs = [hub, vorb, nick] + [zz[k] for k in PF] + [zug[k] for k in PF]
        for arr in arrs:
            d0 = arr[0] - arr[nf - 1]
            for i in range(n8):
                arr[nf - 1 - i] += d0 * (1.0 - i / n8)
    # Liegen: je Bild nachschieben, bis keine Pfote mehr in der anderen steckt (hoechstens 10 Schritte a 1,5 cm), dann zeitlich glaetten
    for f in range(nf):
        if auf_w[f] >= 0.5:
            continue
        for _ in range(10):
            P = G.haut(los(f)[2])
            Nv = normalen(P, G.netz["T"])
            fertig = True
            for a_, b_ in (("HL", "HR"), ("VL", "VR")):
                if pfoten_ineinander(P, Nv, G.pfote_ok[a_], G.pfote_ok[b_], tol=0.003) > 0:
                    fertig = False
                    hoch, tief = (a_, b_) if P[G.pfote[a_], 2].mean() > P[G.pfote[b_], 2].mean() else (b_, a_)
                    r_ = P[G.pfote[hoch]].mean(0) - P[G.pfote[tief]].mean(0)
                    r_[2] = max(r_[2], 0.0) + 0.02
                    weg[hoch][f] += 0.015 * r_ / max(np.linalg.norm(r_), 1e-9)
            if fertig:
                break
    for k in PF:
        for c_ in range(3):
            weg[k][:, c_] = np.maximum.reduce([weg[k][:, c_], glatt(weg[k][:, c_])]) if False else glatt(weg[k][:, c_]) * 0.5 + weg[k][:, c_] * 0.5
    R_all = np.zeros((nf, G.nb, 3, 3))
    pel_all = np.zeros((nf, 3))
    pmin, pst, kz, pin = [], [], [], []
    for f in range(nf):
        R, pel, M, dd = los(f)
        R_all[f], pel_all[f] = R, pel
        P = G.haut(M)
        pmin.append(float(P[:, 2].min()))
        if auf_w[f] < 0.5:
            Nv = normalen(P, G.netz["T"])
            pin.append(sum(pfoten_ineinander(P, Nv, G.pfote_ok[a_], G.pfote_ok[b_], tol=0.003) for a_, b_ in (("HL", "HR"), ("VL", "VR"))))
        pst += [float(P[G.pfote[k], 2].min()) for k in PF if st[k][f] > 0.5 and lift[k][f] < 0.001]
        kz.append(float(P[G.kopf, 2].min()))
        info["ueber"] += [(f,) + u for u in dd["ueber"]]
    if clip in SCHLEIFEN:
        # die je Bild gesuchten Groessen schliessen Idle nur auf 3e-4 E (Quelle exakt) -> letztes Bild = erstes Bild exakt
        info["schleife_abw_vorher_E"] = float(max(np.abs(R_all[-1] - R_all[0]).max(), np.abs(pel_all[-1] - pel_all[0]).max()))
        R_all[-1] = R_all[0]
        pel_all[-1] = pel_all[0]
    info["ueber_n"] = len(info["ueber"])
    info["ueber"] = info["ueber"][:8]
    info["boden_min_cm"] = round(100 * min(pmin), 2)
    info["liegen_pfote_in_pfote_punkte_max"] = int(max(pin)) if pin else 0
    info["stuetz_cm"] = [round(100 * min(pst), 2), round(100 * max(pst), 2)] if pst else None
    info["hub_cm"] = [round(100 * float(hub.min()), 2), round(100 * float(hub.max()), 2)]
    info["absenk_cm"] = [round(100 * float(ab.min()), 2), round(100 * float(ab.max()), 2)]
    info["vorbeugen_grad_max"] = round(float(vorb.max()), 1)
    info["nick_grad_max"] = round(float(nick.max()) * (PAR_EAT["brust"] if eat_ziel is not None else 1.0), 1)
    if eat_ziel is not None:
        info["eat_grad_max"] = round(float(nick.max()), 3)
        info["eat_par"] = PAR_EAT
        info["eat_kopf_arm_min_cm"] = round(100 * min(kopf_arm_abstand(G, los(f)[2]) for f in range(0, nf, 4)), 2)
    info["kopf_min_cm"] = [round(100 * min(kz), 2), round(100 * max(kz), 2)]
    if eat_ziel is not None:
        kz = np.array(kz)
        m = eat_ziel <= 0.0101
        info["eat_schnauze_boden_cm"] = [round(100 * float(kz[m].min()), 2), round(100 * float(kz[m].max()), 2)]
    info["zug_min"] = {k: round(float(zug[k].min()), 2) for k in PF}
    return R_all, pel_all, np.stack([st[k] for k in PF], 1), ab + hub, info


def kopf_arm_abstand(G, M, Pk=None):
    """Kleinster Abstand Kopfhaut -> Haut von Unterarm/Vorderpfote (jeder 3. Punkt), in m."""
    if not hasattr(G, "arm_idx"):
        W, ix = G.W, G.idx
        G.arm_idx = np.nonzero((W[:, ix["Bip01_L_Forearm"]] + W[:, ix["Bip01_R_Forearm"]] + W[:, ix["Bip01_L_Hand"]]
                                + W[:, ix["Bip01_R_Hand"]]) >= 0.5)[0][::3]
    if Pk is None:
        Pk = G.haut(M, G.kopf)
    Pa = G.haut(M, G.arm_idx)
    return min(float(np.sqrt(((Pk[j:j + 400, None, :] - Pa[None]) ** 2).sum(-1)).min()) for j in range(0, len(Pk), 400))


def bild(G, qb, J_alt, dz, sw, zz, zug, vorbeug, nick, weg=None, fress=False):
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
    kauern = 0.0
    if fress and nick:
        # Fressen (nick = Fress-Grad 0..1): Lende/Brust nach vorn beugen (Welt), Hals und Kopf folgen der Brust, vorn kauern
        pe = PAR_EAT
        br = pe["brust"] * nick
        Qw["Bip01_Spine"] = ry(pe["lende"] * br) @ Qw["Bip01_Spine"]
        for nm in ("Bip01_Spine1", "Bip01_L_Clavicle", "Bip01_R_Clavicle"):
            Qw[nm] = ry(br) @ Qw[nm]
        Qw["Bip01_Neck"] = ry(br + pe["hals"] * nick) @ Qw["Bip01_Neck"]
        for nm in ("Bip01_Head", "Bip01_Jaw"):
            Qw[nm] = ry(br + (pe["hals"] + pe["kopf"]) * nick) @ Qw[nm]
        kauern = pe["kauern"] * nick
    pel = qb["J"]["Bip01_Pelvis"] + np.array((0.0, 0.0, dz + kauern))
    _R, _t, M0 = G.pose(Qw, pel)
    dd = dict(ueber=[], streck={})
    for k, (o, u, e) in BEIN.items():
        H = G.gelenk(M0, o)
        Ho, Ao, Ko = qb["J"][o], qb["J"][e], qb["J"][u]
        f_ = G.f_h if k[0] == "H" else G.f_v
        dy = G.J[o][1] - J_alt[o][1]
        frei = H + f_ * (Ao - Ho) + (weg[k] if weg is not None else 0.0)    # weg: Liegen, Pfoten nicht ineinander
        steh = np.array((Ao[0], Ao[1] + dy, Ao[2] + zz[k]))
        if fress and k[0] == "V":
            # Fressen: Vorderpfoten im ganzen Clip fest etwas zurueck und nach aussen (Platz fuer den Kopf vor/zwischen den Pfoten)
            steh += np.array((PAR_EAT["pfote_dx"], np.sign(steh[1]) * PAR_EAT["pfote_dy"], 0.0))
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
    par = dict(runden=5, vorbeug_max=60.0, eat_max=50.0, umsetzen=0.025)
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
