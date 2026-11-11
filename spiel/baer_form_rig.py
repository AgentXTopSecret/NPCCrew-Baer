# Lauf baer-rig-junges (11.11.2026), Rolle FORM, Stufe F2: das Generator-Junge in die RUHELAGE des Skeletts bringen.
# Nur numpy + PIL. Zwei Teile:
#   plan    -- misst am F1-Spielnetz (rig/form/f1/C_f1.glb, Fotopose) und legt die Umstellung fest:
#              1 Rumpf gerade (seitliche Scherung dy(x)), 2 Kopf gerade (Gier 49 Grad ueber Hals/Nacken verteilt, harmonische Gewichte,
#              Rollen zurueck, Nicken bleibt), 3 Beine: VR und HR (Standbeine) in die Ruhe des Erwachsenen (Unterarm 16,2 Grad vor,
#              Unterschenkel 22,8 Grad zurueck), Spur mit >= 4 cm Luecke; VL/HL entstehen als Spiegelbild (Koerper rechts -> links).
#              Schreibt plan.json/plan.npz und die umgerechneten Parameter fuer werkzeug/raw_ruhe.py, form2_rig.py, textur2_rig.py.
#   abgabe  -- liest das fertige Ruhe-Spielnetz (rig/form/f2/C_ruhe.glb, aus textur2_rig.py) und schreibt die FORM-Abgabe:
#              C_rig_basis.npz (massgeblich), C_rig_basis.glb + .png, landmarken_rig.json, pruef_form.json.
# Warum nicht "Punkte des F1-Netzes verschieben" (RIG_PLAN 2.2 Wortlaut): VL steht im Schritt 23 cm hinter VR, HR 4 cm zu nah an der
# Mitte; erster Versuch (f2_t1) faltete Brust/Schulter. Darum: Rohmodell verformen (glatt), bewaehrte Kette form2/textur2 in Ruhe neu
# laufen lassen (Fell/Malerei frisch, keine verzerrten Striche). Version 1 setzte die Beine im Abstandsfeld als Saeule um (Stufen an
# Knie/Ellbogen, render/ruhe_r1); Version 2 (diese): VR/HR im Rohmodell glatt umgestellt (bein_trafo.py), linke Seite = Spiegelbild.
# Rahmen "tier": x vorn, y links, z oben, Boden z = 0. "roh" = Einheit der Generator-Form (Blender-Koordinaten von form2.py:
# tier roh = (-by, bx, bz - ZB)); Meter bei Groesse 1,0 = roh x 1,31.
# Aufruf: python baer_form_rig.py plan|abgabe [cfg.json]
import json, sys, os, math, io, struct, time
import numpy as np
from PIL import Image

T0 = time.time()
W = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/"
sys.path.insert(0, W + "rig/form/werkzeug")
import bein_trafo as BT   # glatte Bein-Umstellung (gleicher Code wie werkzeug/raw_ruhe2.py)
VORGABE = {
    "glb_f1": W + "rig/form/f1/C_f1.glb",
    "glb_ruhe": W + "rig/form/f2/C_ruhe.glb", "form_info_ruhe": W + "rig/form/f2/form_ruhe/form_info.json",
    "raw_paare": W + "rig/form/f2/raw_paare.npz",
    "form_info_f1": W + "rig/form/f1/form_r3/form_info.json",
    "form_param": W + "rig/form/C_form_rig.json",
    "tex_param": W + "rig/form/C_tex_rig.json",
    "aus": W + "rig/form",
    "skala_m_je_roh": 1.31,
    "y_mitte_roh": -0.05,
    # 1 Rumpf
    "rumpf_z_roh": [0.45, 0.75], "rumpf_x_roh": [-0.46, 0.14], "rumpf_grad": 3,
    # 2 Kopf (roh): Atlas im Kopfrahmen (f, u), C7 tier; Kopf starr vor f_starr, Rumpf fest hinter x_fest bzw. unter z_fest
    "atlas_fu_roh": [-0.17, -0.03], "c7_roh": [0.16, -0.05, 0.69], "hals_laenge_faktor": 1.03,
    "kopf_starr_f_roh": -0.12, "kopf_starr_u_roh": -0.17, "rumpf_fest_x_roh": -0.04, "rumpf_fest_z_roh": 0.43,
    # 3 Beine (Meter; Erwachsener in Ruhe, skelett.json ruhe_m_erw)
    "knie_z": 0.41, "ellbogen_z": 0.41, "sprung_z": 0.10, "hand_z": 0.10,
    "unterarm_grad": 16.2, "unterschenkel_grad": 22.8,
    "achse_z_m": [0.13, 0.34], "luecke_min_m": 0.04, "luecke_zugabe_m": 0.006,
    "schnitt_alt_z_m": 0.37, "neu_oben_m": 0.08, "saeule_rand_roh": 0.012, "saeule_r_bis_m": 0.30,
    # Version 2 (glatte Umstellung im Rohmodell, werkzeug/bein_trafo.py): Spur halb (roh) aus RIG_PLAN Abschnitt 1,
    # Mischbaender in Metern bei 1,0 (unter/ueber Ellbogen-Knie, unter/ueber Hand-Sprung), Masken
    "spur_halb_roh": {"vorn": 0.095, "hinten": 0.1125}, "z_teil_m": 0.33,
    "band_dreh_m": [0.065, 0.065], "band_schieb_m": [0.09, 0.13], "band_unten_m": [0.04, 0.026],
    "rand_innen_m": 0.02, "rand_breite_m": 0.08, "pfote_extra_m": 0.08, "mitte_rand_m": 0.02,
    # Pfoten in Ruhe (Proben render/pfote_r2..r4): Knoechel so breit wie der Lauf (Hinterlauf am Sprung vorn-hinten ~0,09 roh),
    # weichere Sohle/Knoechel-Vereinigung, schmalere Sohle, runde Unterkante
    # helle Kratzer-Striche der Farbquelle am Hinterkopf/Hals (gefunden mit werkzeug/texel_flecken.py an f2/C_ruhe.glb, Blender-Koordinaten
    # der Ruhelage): glatt aus dem Ring fuellen, Fellstriche kommen darueber
    "flecken_ruhe": [{"mitte": [-0.18, -0.25, 0.368], "r_in": 0.032, "r_aus": 0.05}, {"mitte": [0.094, -0.308, 0.157], "r_in": 0.022, "r_aus": 0.04},
                     # Runde 2 (texel_flecken_koerper.py + Nahbilder render/flecken_probe.png: A, D, E, F, G, I waren echte helle Risse)
                     {"mitte": [0.025, -0.112, 0.376], "r_in": 0.032, "r_aus": 0.05}, {"mitte": [0.109, 0.344, 0.21], "r_in": 0.025, "r_aus": 0.042},
                     {"mitte": [0.145, -0.216, 0.008], "r_in": 0.02, "r_aus": 0.036}, {"mitte": [-0.249, 0.37, -0.123], "r_in": 0.02, "r_aus": 0.036},
                     {"mitte": [0.092, 0.059, 0.274], "r_in": 0.026, "r_aus": 0.044}, {"mitte": [0.0756, -0.0094, 0.2813], "r_in": 0.026, "r_aus": 0.044},
                     # Runde 3 (werkzeug/pixel_3d.py an render/blatt_tex/kopf_270 + kopf_315): Wange hinter dem rechten Auge
                     {"mitte": [-0.195, -0.279, 0.327], "r_in": 0.022, "r_aus": 0.04}],
    "pfoten_ruhe": {"r_max_vorn": 0.068, "r_max_hinten": 0.09, "knoechel_r": 1.0, "knoechel_k": 0.05, "sohle_breite": 0.88, "boden_k": 0.02},
    # Ausgabe
    "y_ursprung": "mitte", "x_ursprung": "pfoten",
}
CFG = dict(VORGABE)
MODUS = sys.argv[1] if len(sys.argv) > 1 else "plan"
if len(sys.argv) > 2:
    CFG.update(json.load(open(sys.argv[2], encoding="utf-8")))
AUS = CFG["aus"]; F2 = os.path.join(AUS, "f2"); os.makedirs(F2, exist_ok=True)
S = CFG["skala_m_je_roh"]; YM = CFG["y_mitte_roh"]


def log(*a):
    print("[%6.1f s]" % (time.time() - T0), *a, flush=True)


def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t)


def jdump(o, p):
    json.dump(o, open(p, "w", encoding="utf-8"), indent=1, default=lambda v: v.tolist() if hasattr(v, "tolist") else (float(v) if isinstance(v, np.floating) else str(v)))


# ------------------------------------------------------------------ GLB
def lade_glb(p):
    b = open(p, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + n]); o = 20 + n
    bl = struct.unpack("<I", b[o:o + 4])[0]
    B = b[o + 8:o + 8 + bl]

    def acc(i):
        a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
        dt = {5126: np.float32, 5123: np.uint16, 5125: np.uint32}[a["componentType"]]
        k = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]
        s = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        return np.frombuffer(B[s:s + a["count"] * k * np.dtype(dt).itemsize], dtype=dt).reshape(a["count"], k)
    pr = J["meshes"][0]["primitives"][0]
    out = {"P": acc(pr["attributes"]["POSITION"]).astype(np.float64), "T": acc(pr["indices"]).reshape(-1, 3).astype(np.int64)}
    if "TEXCOORD_0" in pr["attributes"]:
        out["UV"] = acc(pr["attributes"]["TEXCOORD_0"]).astype(np.float64)
    if J.get("images"):
        im = J["images"][0]; v = J["bufferViews"][im["bufferView"]]
        out["bild"] = np.array(Image.open(io.BytesIO(B[v.get("byteOffset", 0):v.get("byteOffset", 0) + v["byteLength"]])).convert("RGB"))
    return out


def netz_tier(p_glb):
    """GLB (glTF) -> tier roh (Boden = ZB des Generator-Rahmens) + Verschweissung"""
    G = lade_glb(p_glb)
    Vg = np.stack([G["P"][:, 2], G["P"][:, 0], G["P"][:, 1] - ZB], 1)
    _, i0, inv = np.unique(np.round(Vg, 6), axis=0, return_index=True, return_inverse=True)
    inv = inv.ravel()
    return G, Vg[i0], inv, inv[G["T"]]


def bl_tier(b):
    b = np.asarray(b, float); return np.stack([-b[..., 1], b[..., 0], b[..., 2] - ZB], -1)


def tier_bl(t):
    t = np.asarray(t, float); return np.stack([t[..., 1], -t[..., 0], t[..., 2] + ZB], -1)


def blv_tier(b):
    b = np.asarray(b, float); return np.stack([-b[..., 1], b[..., 0], b[..., 2]], -1)


def tierv_bl(t):
    t = np.asarray(t, float); return np.stack([t[..., 1], -t[..., 0], t[..., 2]], -1)


M_BL = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1.0]])   # tier = M_BL @ blender (Richtungen)


def rot_tier_zu_bl(R):
    return M_BL.T @ R @ M_BL


# ------------------------------------------------------------------ Netz-Werkzeuge (Laplace, harmonisch)
class Netz:
    def __init__(self, X, T):
        self.X, self.T, self.n = X, T, len(X)
        E_ = np.sort(np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), 1)
        self.E = np.unique(E_, axis=0)
        w = np.zeros(len(self.E)); key_e = self.E[:, 0] * self.n + self.E[:, 1]
        for a, b, c in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
            u = X[T[:, a]] - X[T[:, c]]; v = X[T[:, b]] - X[T[:, c]]
            cot = np.sum(u * v, 1) / (np.linalg.norm(np.cross(u, v), axis=1) + 1e-12)
            ek = np.sort(np.stack([T[:, a], T[:, b]], 1), 1)
            np.add.at(w, np.searchsorted(key_e, ek[:, 0] * self.n + ek[:, 1]), 0.5 * cot)
        self.w = np.clip(w, 1e-3, None)
        self.deg = np.zeros(self.n); np.add.at(self.deg, self.E[:, 0], self.w); np.add.at(self.deg, self.E[:, 1], self.w)

    def lap(self, x, frei):
        y = self.deg * x; a, b = self.E[:, 0], self.E[:, 1]
        np.subtract.at(y, a, self.w * x[b]); np.subtract.at(y, b, self.w * x[a]); y[~frei] = 0; return y

    def harmonisch(self, wert, fest, iters=4000, tol=1e-8):
        frei = ~fest
        g = np.where(fest, wert, 0.0)
        b = -self.lap(g, np.ones(self.n, bool)); b[fest] = 0
        x = np.zeros(self.n); r = b.copy(); Mi = np.where(frei, 1 / self.deg, 0)
        z = Mi * r; p = z.copy(); rz = r @ z; n0 = math.sqrt(b @ b) + 1e-30
        for it in range(iters):
            Ap = self.lap(p, frei); al = rz / (p @ Ap + 1e-30); x += al * p; r -= al * Ap
            if math.sqrt(r @ r) / n0 < tol:
                break
            z = Mi * r; rz2 = r @ z; p = z + (rz2 / rz) * p; rz = rz2
        return np.where(fest, wert, x + g * 0), it


def rot_achse(ax, ang):
    ax = np.asarray(ax, float); ax = ax / (np.linalg.norm(ax) + 1e-30)
    Kx = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(ang) * Kx + (1 - math.cos(ang)) * Kx @ Kx


def rot_log(R):
    c = np.clip((np.trace(R) - 1) / 2, -1, 1); ang = math.acos(c)
    if ang < 1e-9:
        return np.zeros(3)
    return np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2 * math.sin(ang)) * ang


def schnitt_kurven(X, T, h, ax=2):
    a = X[:, ax] - h
    sf = a[T] > 0; kr = (sf.sum(1) % 3) != 0
    seg = []
    for t in T[kr]:
        pts = []
        for i, j in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            if (a[i] > 0) != (a[j] > 0):
                pts.append((min(i, j), max(i, j)))
        if len(pts) == 2:
            seg.append(pts)
    nb = {}
    for p_, q_ in seg:
        nb.setdefault(p_, []).append(q_); nb.setdefault(q_, []).append(p_)
    seen = set(); out = []
    for st in nb:
        if st in seen:
            continue
        loop = [st]; seen.add(st); prev = None; cur = st
        while True:
            nx = [n for n in nb[cur] if n != prev and n not in seen]
            if not nx:
                break
            prev, cur = cur, nx[0]; seen.add(cur); loop.append(cur)
        if len(loop) < 5:
            continue
        pk = np.array([X[i] + a[i] / (a[i] - a[j]) * (X[j] - X[i]) for i, j in loop])
        u, v = pk[:, 0], pk[:, 1]
        A = 0.5 * np.sum(u * np.roll(v, -1) - np.roll(u, -1) * v)
        if abs(A) < 1e-7:
            continue
        cu = np.sum((u + np.roll(u, -1)) * (u * np.roll(v, -1) - np.roll(u, -1) * v)) / (6 * A)
        cv = np.sum((v + np.roll(v, -1)) * (u * np.roll(v, -1) - np.roll(u, -1) * v)) / (6 * A)
        out.append({"A": abs(A), "c": np.array([cu, cv]), "pts": pk})
    return sorted(out, key=lambda r: -r["A"])


# ================================================================== PLAN
def plan():
    global ZB
    BER = {"cfg": CFG}
    PFJ = json.load(open(CFG["form_param"], encoding="utf-8"))
    TPJ = json.load(open(CFG["tex_param"], encoding="utf-8"))
    I = json.load(open(CFG["form_info_f1"], encoding="utf-8"))
    G, V, inv, T = netz_tier(CFG["glb_f1"])
    log("F1-Netz", len(V), "Punkte", len(T), "Dreiecke; Boden ZB", ZB)
    N = Netz(V, T)
    # ---- 1 Rumpf gerade
    z0, z1 = CFG["rumpf_z_roh"]; xs, ms = [], []
    for x in np.arange(CFG["rumpf_x_roh"][0], CFG["rumpf_x_roh"][1] + 1e-9, 0.015):
        m = (np.abs(V[:, 0] - x) < 0.012) & (V[:, 2] > z0) & (V[:, 2] < z1)
        if m.sum() >= 6:
            xs.append(x); ms.append(0.5 * (np.percentile(V[m, 1], 2) + np.percentile(V[m, 1], 98)))
    xs, ms = np.array(xs), np.array(ms)
    koef = np.polyfit(xs, ms, CFG["rumpf_grad"]); x_lo, x_hi = float(xs.min()), float(xs.max())

    def dy(x):
        return YM - np.polyval(koef, np.clip(x, x_lo, x_hi))
    BER["rumpf"] = {"mitte_y_roh": {"%.3f" % a: round(float(b), 4) for a, b in zip(xs[::4], ms[::4])}, "bogen_roh": round(float(ms.max() - ms.min()), 4),
                    "polynom": koef.tolist(), "x_bereich": [x_lo, x_hi], "dy_vorn_roh": round(float(dy(x_hi)), 4), "dy_hinten_roh": round(float(dy(x_lo)), 4)}
    Vs = V.copy(); Vs[:, 1] += dy(V[:, 0])

    def sch(p):
        p = np.array(p, float); p[..., 1] = p[..., 1] + dy(p[..., 0]); return p
    log("Rumpf: Bogen", BER["rumpf"]["bogen_roh"], "roh; dy vorn", BER["rumpf"]["dy_vorn_roh"], "hinten", BER["rumpf"]["dy_hinten_roh"])
    # ---- 2 Kopf gerade
    K = I["kopf_rahmen_spiegel"]
    AM = sch(bl_tier(K["augen_mitte"])); FW = blv_tier(K["vorn"]); LAT = blv_tier(K["seitlich"]); UP = blv_tier(K["oben"])
    R_tot = np.stack([FW, LAT, UP], 1).T; u_, s_, vt_ = np.linalg.svd(R_tot); R_tot = u_ @ vt_
    A0 = AM + FW * CFG["atlas_fu_roh"][0] + UP * CFG["atlas_fu_roh"][1]
    C7 = sch(np.array(CFG["c7_roh"], float))
    hl = float(np.linalg.norm((A0 - C7)[:2])) * CFG["hals_laenge_faktor"]
    A_z = np.array([C7[0] + hl, YM, A0[2]])
    gier = math.atan2(FW[1], FW[0]); R_g = rot_achse([0, 0, 1], -gier)
    piv = np.zeros(3); piv[:2] = np.linalg.solve(np.eye(2) - R_g[:2, :2], A_z[:2] - R_g[:2, :2] @ A0[:2]); piv[2] = A0[2]
    R_r = R_tot @ R_g.T
    Q = Vs - AM; f_ = Q @ FW; u_k = Q @ UP
    ohr_m = np.zeros(len(Vs), bool)
    for o in I["ohren"]:
        ohr_m |= np.linalg.norm(Vs - sch(bl_tier(o["mitte"])), axis=1) < 0.10
    starr = ((f_ > CFG["kopf_starr_f_roh"]) & (u_k > CFG["kopf_starr_u_roh"]) & (np.linalg.norm(Q, axis=1) < 0.32)) | ohr_m
    fest_r = ((Vs[:, 0] < CFG["rumpf_fest_x_roh"]) | (Vs[:, 2] < CFG["rumpf_fest_z_roh"])) & ~starr
    w_h, it = N.harmonisch(starr.astype(float), starr | fest_r)
    w_h = np.clip(w_h, 0, 1)
    BER["kopf"] = {"gier_grad": round(math.degrees(gier), 2), "roll_grad": round(math.degrees(math.asin(np.clip(LAT[2], -1, 1))), 2),
                   "atlas_foto_roh": A0.round(4).tolist(), "atlas_ziel_roh": A_z.round(4).tolist(), "c7_roh": C7.round(4).tolist(),
                   "drehpunkt_gier_roh": piv.round(4).tolist(), "rest_drehung_grad": round(math.degrees(np.linalg.norm(rot_log(R_r))), 2),
                   "hals_laenge_roh": round(hl, 4), "punkte_starr": int(starr.sum()), "punkte_fest": int(fest_r.sum()),
                   "punkte_band": int((~starr & ~fest_r).sum()), "cg_iter": it}

    def kopf_t(p, w=1.0):
        """Kopf-Umstellung fuer Punkte p (tier roh, geschert) mit Gewicht w (Skalar oder je Punkt)"""
        p = np.atleast_2d(np.asarray(p, float)); w = np.broadcast_to(np.asarray(w, float), (len(p),))
        out = np.empty_like(p)
        rg = rot_log(R_g); rr = rot_log(R_r)
        for i in range(len(p)):
            Rg = rot_achse(rg, np.linalg.norm(rg) * w[i]) if np.linalg.norm(rg) > 0 else np.eye(3)
            Rr = rot_achse(rr, np.linalg.norm(rr) * w[i]) if np.linalg.norm(rr) > 0 else np.eye(3)
            y = piv + Rg @ (p[i] - piv); a = piv + Rg @ (A0 - piv)
            out[i] = a + Rr @ (y - a)
        return out
    log("Kopf: Gier", BER["kopf"]["gier_grad"], "Rollen", BER["kopf"]["roll_grad"], "Drehpunkt", BER["kopf"]["drehpunkt_gier_roh"],
        "Band", BER["kopf"]["punkte_band"], "CG", it)
    # ---- 3 Beine (auf dem gescherten Netz; der Kopf beruehrt die Beine nicht)
    zj = CFG["knie_z"] / S; zk = CFG["sprung_z"] / S; zje = CFG["ellbogen_z"] / S; zke = CFG["hand_z"] / S
    pf_ref = {}
    for p in I["pfoten"]:
        b = sch(bl_tier([p["bein"][0], p["bein"][1], p["boden"]]))
        nm = ("V" if p["art"] == "vorn" else "H") + ("L" if b[1] > YM else "R")
        pf_ref[nm] = b
    ax = {nm: [] for nm in pf_ref}; ref = {nm: v.copy() for nm, v in pf_ref.items()}
    for zm in np.arange(CFG["achse_z_m"][0], CFG["achse_z_m"][1] + 1e-9, 0.02):
        ks = schnitt_kurven(Vs, T, zm / S)
        for nm in ax:
            best = None
            for k in ks:
                if k["A"] > 0.04:
                    continue
                d = np.linalg.norm(k["c"] - ref[nm][:2])
                if best is None or d < best[0]:
                    best = (d, k)
            if best and best[0] < 0.09:
                k = best[1]; r_ = np.linalg.norm(k["pts"][:, :2] - k["c"][None], axis=1)
                ax[nm].append([k["c"][0], k["c"][1], zm / S, r_.max(), (k["pts"][:, 1].max() - k["pts"][:, 1].min()) / 2])
                ref[nm] = np.array([k["c"][0], k["c"][1], zm / S])
    ax = {nm: np.array(v) for nm, v in ax.items()}
    lin = {}
    BER["beine_foto"] = {}
    for nm, a in ax.items():
        cx = np.polyfit(a[:, 2], a[:, 0], 1); cy = np.polyfit(a[:, 2], a[:, 1], 1); lin[nm] = (cx, cy)
        BER["beine_foto"][nm] = {"schnitte": len(a), "vorneigung_grad": round(math.degrees(math.atan(-cx[0])), 1),
                                 "seitneigung_grad": round(math.degrees(math.atan(-cy[0])), 1), "r_max_roh": round(float(a[:, 3].max()), 4),
                                 "halbbreite_y_roh": round(float(np.median(a[:, 4])), 4)}

    def punkt(nm, z):
        cx, cy = lin[nm]; return np.array([np.polyval(cx, z), np.polyval(cy, z), z])
    beine = {}
    partner = {"VR": "VL", "HR": "HL"}
    for nm, art, zj_, zk_, gr in (("VR", "vorn", zje, zke, CFG["unterarm_grad"]), ("HR", "hinten", zj, zk, -CFG["unterschenkel_grad"])):
        J = punkt(nm, zj_); Kp = punkt(nm, zk_)
        hb = float(np.median(ax[nm][:, 4]))
        b_min = hb + (CFG["luecke_min_m"] + CFG["luecke_zugabe_m"]) / S / 2
        # Version 2: Spur aus RIG_PLAN Abschnitt 1 (Mittel links/rechts), mindestens b_min
        b = max(CFG["spur_halb_roh"][art], b_min)
        Jz = np.array([J[0], YM - b, zj_]); hz = zj_ - zk_
        Kz = Jz + np.array([hz * math.tan(math.radians(gr)), 0.0, -hz])
        Bd = BT.bein_def({"J": J, "K": Kp, "Jz": Jz, "Kz": Kz})
        a0, a1, sb, ang = Bd["a0"], Bd["a1"], Bd["s"], Bd["ang"]
        Rb = rot_achse(Bd["ax"], ang)
        r_src = float(ax[nm][ax[nm][:, 2] < CFG["saeule_r_bis_m"] / S, 3].max()) + CFG["saeule_rand_roh"]
        # Teilungslinie: Mitte der Luecke zum linken Partnerbein auf Hoehe z_teil (Fotopose)
        zt = CFG["z_teil_m"] / S
        innen_eigen = punkt(nm, zt)[1] + hb
        pa = partner[nm]; innen_partner = punkt(pa, zt)[1] - float(np.median(ax[pa][:, 4]))
        y_teil = 0.5 * (innen_eigen + innen_partner)
        band = {"dreh_oben": [zj_ - CFG["band_dreh_m"][0] / S, zj_ + CFG["band_dreh_m"][1] / S],
                "schieb_oben": [zj_ - CFG["band_schieb_m"][0] / S, zj_ + CFG["band_schieb_m"][1] / S],
                "unten": [zk_ - CFG["band_unten_m"][0] / S, zk_ + CFG["band_unten_m"][1] / S]}
        beine[nm] = {"art": art, "J": J, "K": Kp, "Jz": Jz, "Kz": Kz, "R": Rb, "s": sb, "a0": a0, "a1": a1, "r": r_src, "halb": hb, "b": b,
                     "r_bein": r_src, "y_teil": y_teil, "band": band, "innen_eigen": innen_eigen, "innen_partner": innen_partner,
                     "halb_partner": float(np.median(ax[pa][:, 4]))}
        BER.setdefault("beine_ruhe", {})[nm] = {"gelenk_foto_roh": J.round(4).tolist(), "gelenk_ruhe_roh": Jz.round(4).tolist(),
                                               "hand_sprung_foto_roh": Kp.round(4).tolist(), "hand_sprung_ruhe_roh": Kz.round(4).tolist(),
                                               "drehung_grad": round(math.degrees(ang), 2), "streckung": round(sb, 4),
                                               "spur_halb_roh": round(b, 4), "spur_halb_m": round(b * S, 4), "saeule_radius_roh": round(r_src, 4),
                                               "luecke_m_erwartet": round((2 * b - 2 * hb) * S, 4),
                                               "lateral_verschoben_cm": round(abs(Jz[1] - J[1]) * S * 100, 2),
                                               "hand_sprung_quer_cm": round(abs(Kz[1] - Kp[1]) * S * 100, 2),
                                               "y_teil_roh": round(y_teil, 4)}
    log("Beine Ruhe", BER["beine_ruhe"])
    # ---- 4 Parameter fuer form2_rig / textur2_rig (Blender-Koordinaten)
    rgk = rot_tier_zu_bl(R_tot)

    def kopf_bl(pb):   # Blender-Punkt (Fotopose, ungeschert) -> Blender-Punkt Ruhe (geschert + Kopf starr)
        return tier_bl(kopf_t(sch(bl_tier(pb)))[0])

    def sch_bl(pb):
        return tier_bl(sch(bl_tier(pb)))
    P2 = json.loads(json.dumps(PFJ))
    P2["name"] = "C_form"; P2["glb"] = W + "rig/form/f2/raw_ruhe_form.glb"; P2["dreh_z"] = 0.0; P2["aus"] = W + "rig/form/f2/form_ruhe"
    for k in ("kopf_mitte", "auge_l", "auge_r", "nase"):
        P2[k] = kopf_bl(PFJ[k]).round(5).tolist()
    for nm, re in P2["regionen"].items():
        if not re.get("kopfrahmen"):
            re["mitte"] = sch_bl(re["mitte"]).round(5).tolist()
    for nm, oh in P2["alte_ohren"].items():
        oh["mitte"] = kopf_bl(oh["mitte"]).round(5).tolist()
    AMr = tier_bl(kopf_t(AM)[0])
    P2["spiegel"]["normale_fest"] = [1.0, 0.0, 0.0]; P2["spiegel"]["ebene_fest"] = AMr.round(5).tolist()
    # Version 2: Beine werden im Rohmodell glatt umgestellt (werkzeug/raw_ruhe2.py), kein Saeulen-Tausch (e4) mehr
    P2.pop("beine_ruhe", None)
    P2["koerper_spiegel"] = {"x_mitte": YM, "naht": 0.02}
    P2["L_fest"] = I["hoch"]["L"]
    # Pfoten: Achsenpunkt auf Hoehe des Pfoten-Schnitts mit derselben Umstellung wie das Rohmodell; links = Spiegelbild,
    # Abdruck der linken Pfoten = Spiegelbild des rechten (form2_rig "fuss_spiegel")
    zs = PFJ["pfoten"]["z_schnitt"] - ZB + 0.012
    liste = []; BER["pfoten_ruhe"] = {}
    for nm, bd in beine.items():
        Bd = BT.bein_def(bd)
        c0 = punkt(nm, zs); c1 = BT.bein_voll(c0[None], Bd, bd["band"])[0]
        BER["pfoten_ruhe"][nm] = {"foto_roh": c0.round(4).tolist(), "ruhe_roh": c1.round(4).tolist()}
        for nm2 in (nm, nm[0] + "L"):
            c = c1 if nm2 == nm else np.array([c1[0], 2 * YM - c1[1], c1[2]])
            cb = tier_bl(c)
            liste.append({"name": nm2, "xy": [round(float(cb[0]), 5), round(float(cb[1]), 5)], "art": "vorn" if nm[0] == "V" else "hinten",
                          "boden": round(float(ZB), 5), "bein": [round(float(cb[0]), 5), round(float(cb[1]), 5)]})
    P2["pfoten"]["liste"] = liste; P2["pfoten"].pop("fuss_kreis", None)
    P2["pfoten"]["fuss_spiegel"] = {"x_mitte": YM, "paare": {"VL": "VR", "HL": "HR"}}
    P2["pfoten"].update(CFG["pfoten_ruhe"])
    # Knoechel-Regionen (laufen nach dem Spiegeln) auf die Mittelebene, damit links = rechts
    for grp in ("regionen", "regionen_nach", "regionen_ende"):
        for nm_r, re in P2.get(grp, {}).items():
            if nm_r in ("beine", "knoechel", "knoechel_glatt", "knoechel_fuellen"):
                re["mitte"][0] = YM
    # Spalt zwischen den Hinterbeinen: Mitte auf die Mittelebene, x zwischen die Ruhe-Hinterbeine
    hx = float(beine["HR"]["Jz"][0] + beine["HR"]["Kz"][0]) / 2
    for sp in P2.get("spalten", []):
        if "mitte" in sp:
            m_ = bl_tier(sp["mitte"]); m_[0] = hx; m_[1] = YM; sp["mitte"] = tier_bl(m_).round(5).tolist()
    # Heck + Stummel: Scherung am Heck
    dyh = float(dy(-0.5))
    HF = P2.get("heck_fit")
    if HF:   # nach dem Koerper-Spiegeln ist das Heck symmetrisch um YM -> Kern und Fenster auf die Mittelebene
        c0 = (HF["fx"][0] + HF["fx"][1]) / 2
        HF["fx"] = [HF["fx"][0] - c0 + YM, HF["fx"][1] - c0 + YM]; HF["kern"][0] = YM
    P2["stummel"]["x"] = YM
    for nm, re in P2.get("regionen_nach", {}).items():
        if not re.get("kopfrahmen"):
            re["mitte"] = sch_bl(re["mitte"]).round(5).tolist()
    for nm, re in P2.get("regionen_ende", {}).items():
        if not re.get("kopfrahmen"):
            re["mitte"] = sch_bl(re["mitte"]).round(5).tolist()
    jdump(P2, os.path.join(AUS, "C_form_ruhe.json"))
    T2 = json.loads(json.dumps(TPJ))
    T2.update({"name": "C_ruhe", "form_info": W + "rig/form/f2/form_ruhe/form_info.json", "dicht": W + "rig/form/f2/form_ruhe/C_form_dicht.npz",
               "aus": W + "rig/form/f2", "renderordner": W + "rig/form/f2/einzel", "hoch_glb": W + "rig/form/f2/raw_ruhe_tex.glb"})
    T2["schnauze"] = kopf_bl(TPJ["schnauze"]).round(5).tolist()
    T2["augen_fest"] = [kopf_bl(a).round(5).tolist() for a in TPJ["augen_fest"]]
    for hk in T2.get("heck_fuellen", []):
        if hk["mitte"] != "stummel":
            hk["mitte"] = sch_bl(hk["mitte"]).round(5).tolist()
    T2["L_fest"] = I["hoch"]["L"]
    T2["flecken_fuellen"] = list(T2.get("flecken_fuellen", [])) + CFG["flecken_ruhe"]
    jdump(T2, os.path.join(AUS, "C_tex_ruhe.json"))
    # ---- 5 Plan fuer raw_ruhe.py (Blender): Spielnetz-Punkte (Blender, geschert) + Kopfgewichte, Trafos
    Vsb = tier_bl(Vs)
    np.savez_compressed(os.path.join(F2, "plan.npz"), V_bl_geschert=Vsb, w_kopf=w_h, T=T)
    PL = {"ZB": ZB, "y_mitte_roh": YM, "dreh_z": PFJ["dreh_z"], "raw": PFJ["glb"], "scher_polynom": koef.tolist(), "scher_x": [x_lo, x_hi],
          "kopf": {"piv": piv.tolist(), "R_gier": R_g.tolist(), "R_rest": R_r.tolist(), "A0": A0.tolist()},
          "beine": {nm: {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in bd.items()} for nm, bd in beine.items()},
          "achsen_foto": {nm: {"cx": lin[nm][0].tolist(), "cy": lin[nm][1].tolist()} for nm in lin},
          "z_schnitt_alt_roh": CFG["schnitt_alt_z_m"] / S,
          "beine_glatt": {"rand_innen": CFG["rand_innen_m"] / S, "rand_breite": CFG["rand_breite_m"] / S, "pfote_extra": CFG["pfote_extra_m"] / S,
                          "mitte_rand": CFG["mitte_rand_m"] / S,
                          "x_paar": 0.5 * float(beine["VR"]["J"][0] + beine["HR"]["J"][0])}}
    jdump(PL, os.path.join(F2, "plan.json"))
    jdump(BER, os.path.join(F2, "plan_bericht.json"))
    log("PLAN fertig:", os.path.join(F2, "plan.json"))


# ================================================================== ABGABE
def nn_gitter(Q, P, h=0.02):
    """naechster Punkt aus P fuer jeden Punkt in Q (Gitter-Suche, numpy)"""
    key = lambda c: (c[:, 0] * 73856093) ^ (c[:, 1] * 19349663) ^ (c[:, 2] * 83492791)
    cP = np.floor(P / h).astype(np.int64); kP = key(cP); o = np.argsort(kP); kS = kP[o]
    cQ = np.floor(Q / h).astype(np.int64)
    best = np.full(len(Q), np.inf); bi = np.zeros(len(Q), np.int64)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                kq = key(cQ + np.array([dx, dy, dz]))
                lo = np.searchsorted(kS, kq, "left"); hi = np.searchsorted(kS, kq, "right")
                for i in np.nonzero(hi > lo)[0]:
                    c = o[lo[i]:hi[i]]; d = np.sum((P[c] - Q[i]) ** 2, 1); j = int(np.argmin(d))
                    if d[j] < best[i]:
                        best[i] = d[j]; bi[i] = c[j]
    best[best > h * h] = np.inf          # nur innerhalb h sicher (Nachbarzellen; Hash-Kollisionen sonst falsch)
    return bi, np.sqrt(best)


def schreibe_glb(pfad, pos, nrm, uv, tri, png_bytes, name="NCBearCub_basis"):
    """einfaches GLB: ein Netz, ein Primitiv, ein Material mit eingebetteter Textur (nur zum Ansehen)"""
    teile = []; views = []; acc = []; off = 0

    def anh(arr, ziel=None):
        nonlocal off
        b = arr.tobytes(); pad = (-len(b)) % 4
        views.append({"buffer": 0, "byteOffset": off, "byteLength": len(b), **({"target": ziel} if ziel else {})})
        teile.append(b + b"\0" * pad); off += len(b) + pad
        return len(views) - 1
    v = anh(pos.astype(np.float32), 34962)
    acc.append({"bufferView": v, "componentType": 5126, "count": len(pos), "type": "VEC3", "min": pos.min(0).tolist(), "max": pos.max(0).tolist()})
    v = anh(nrm.astype(np.float32), 34962); acc.append({"bufferView": v, "componentType": 5126, "count": len(nrm), "type": "VEC3"})
    v = anh(uv.astype(np.float32), 34962); acc.append({"bufferView": v, "componentType": 5126, "count": len(uv), "type": "VEC2"})
    it = tri.astype(np.uint16 if tri.max() < 65536 else np.uint32).ravel()
    v = anh(it, 34963); acc.append({"bufferView": v, "componentType": 5123 if it.dtype == np.uint16 else 5125, "count": len(it), "type": "SCALAR"})
    v_img = anh(np.frombuffer(png_bytes, np.uint8))
    J = {"asset": {"version": "2.0", "generator": "baer_form_rig.py"}, "scene": 0, "scenes": [{"nodes": [0]}],
         "nodes": [{"mesh": 0, "name": name}],
         "meshes": [{"name": name, "primitives": [{"attributes": {"POSITION": 0, "NORMAL": 1, "TEXCOORD_0": 2}, "indices": 3, "material": 0}]}],
         "materials": [{"name": "fell", "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.0, "roughnessFactor": 0.9}}],
         "textures": [{"source": 0, "sampler": 0}], "samplers": [{"magFilter": 9729, "minFilter": 9729}],
         "images": [{"bufferView": v_img, "mimeType": "image/png"}],
         "accessors": acc, "bufferViews": views, "buffers": [{"byteLength": off}]}
    js = json.dumps(J, separators=(",", ":")).encode(); js += b" " * ((-len(js)) % 4)
    bin_ = b"".join(teile)
    out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(bin_)) + struct.pack("<II", len(js), 0x4E4F534A) + js + \
        struct.pack("<II", len(bin_), 0x004E4942) + bin_
    open(pfad, "wb").write(out)


def abgabe():
    global ZB
    T0a = time.time()
    PLj = json.load(open(os.path.join(F2, "plan.json"), encoding="utf-8"))
    BERp = json.load(open(os.path.join(F2, "plan_bericht.json"), encoding="utf-8"))
    FI = json.load(open(CFG["form_info_ruhe"], encoding="utf-8"))
    PFR = json.load(open(os.path.join(AUS, "C_form_ruhe.json"), encoding="utf-8"))
    TXR = json.load(open(os.path.join(AUS, "C_tex_ruhe.json"), encoding="utf-8"))
    G, Vr, inv, Tw = netz_tier(CFG["glb_ruhe"])          # tier roh, verschweisst
    ER = {"quelle": CFG["glb_ruhe"]}
    # ---- Ursprung: y = Mittelebene, z = Boden, x = Mitte zwischen Vorder- und Hinterpfoten (vorlaeufig; SKELETT verschiebt)
    pf = {}
    for p in FI["pfoten"]:
        pf[p["name"]] = bl_tier([p["bein"][0], p["bein"][1], ZB])
    x0 = 0.5 * (0.5 * (pf["VR"][0] + pf["VL"][0]) + 0.5 * (pf["HR"][0] + pf["HL"][0]))
    ursprung = np.array([x0, YM, 0.0])

    def m_(p):
        return (np.asarray(p, float) - ursprung) * S
    V = m_(Vr)
    ER["ursprung_roh"] = ursprung.round(5).tolist()
    # ---- Masken
    KRm = FI["kopf_rahmen"]
    AMb = bl_tier(KRm["augen_mitte"]); FW = blv_tier(KRm["vorn"]); UPk = blv_tier(KRm["oben"]); LT = blv_tier(KRm["seitlich"])
    AM = m_(AMb)
    atl = m_(np.array(BERp["kopf"]["atlas_ziel_roh"])); c7 = m_(np.array(BERp["kopf"]["c7_roh"]) * np.array([1, 0, 1]) + np.array([0, YM, 0]))
    Q = V - AM; fk = Q @ FW; uk = Q @ UPk
    atl_f = float((atl - AM) @ FW)
    ohr_m = {}
    for o in FI["ohren"]:
        c = m_(bl_tier(o["mitte"])); nm = "ohr_l" if c[1] > 0 else "ohr_r"
        ohr_m[nm] = (np.linalg.norm(V - c, axis=1) < 0.075 * S) & (V[:, 2] > c[2] - 0.03 * S)
    # Kopf/Hals-Grenze: Ebene durch den Atlas und die Kehle (Kinn-Unterseite 3 cm zurueck), quer zur Mittelebene; Kopf = davor + 3 cm
    # (Regel SKELETT "Head 1,0 vor der Ebene Atlas - 0,03 m"), Ohren immer Kopf
    mid_k = (np.abs(V[:, 1]) < 0.02) & (fk > 0.0) & (fk < 0.12)
    kinn = V[mid_k][np.argmin(V[mid_k, 2])]
    kehle = np.array([kinn[0] - 0.03, 0.0, kinn[2]])
    t_ = kehle - atl; nk = np.array([-t_[2], 0.0, t_[0]]); nk /= np.linalg.norm(nk)
    if (AM - atl) @ nk < 0:
        nk = -nk
    kopf = (((V - atl) @ nk) > -0.03) & (np.linalg.norm(Q, axis=1) < 0.45) | ohr_m["ohr_l"] | ohr_m["ohr_r"]
    hals = (~kopf) & (V[:, 0] > c7[0] - 0.02) & (((V - atl) @ nk) > -0.03 - 0.12) & (V[:, 2] > kehle[2] - 0.12)
    z_pf = (PFR["pfoten"]["z_schnitt"] - ZB) * S + 0.02
    masken = {"kopf": kopf, "ohr_l": ohr_m["ohr_l"], "ohr_r": ohr_m["ohr_r"], "hals": hals}
    sohle = V[:, 2] < 0.012
    kralle = np.zeros(len(V), bool)
    for p in FI["pfoten"]:
        c = m_(bl_tier([p["bein"][0], p["bein"][1], ZB]))
        mk = (V[:, 2] < z_pf) & (np.hypot(V[:, 0] - c[0], V[:, 1] - c[1]) < 0.17)
        masken["pfote_" + p["name"]] = mk
        for z_ in p["zehen"]:
            zc_ = m_(bl_tier(z_[:3])); kralle |= mk & (np.linalg.norm(V - zc_, axis=1) < z_[3] * S * 1.7) & (V[:, 0] > zc_[0] - 0.005)
    masken["kralle"] = kralle; masken["sohle"] = sohle & np.any([masken["pfote_" + n] for n in ("VR", "VL", "HR", "HL")], axis=0)
    st = m_(bl_tier(FI["stummel"]["mitte"])); masken["stummel"] = np.linalg.norm(V - st, axis=1) < 0.05 * S
    ER["masken_punkte"] = {k: int(v.sum()) for k, v in masken.items()}
    # ---- V_foto (Fotopose nach Rumpf-Scherung) ueber das verformte Rohmodell
    RP = np.load(CFG["raw_paare"])
    links = Vr[:, 1] > YM            # linke Seite ist in der Form das Spiegelbild der rechten -> rechts suchen, zurueckspiegeln
    Vq = Vr.copy(); Vq[links, 1] = 2 * YM - Vq[links, 1]
    nn, dnn = nn_gitter(Vq, RP["P_ruhe"], 0.02)
    for h_ in (0.05, 0.12, 0.3):     # neu gebaute Teile (Ohren, Pfoten) liegen weiter weg -> groeberes Gitter
        weit = ~np.isfinite(dnn)
        if weit.any():
            nn2, d2 = nn_gitter(Vq[weit], RP["P_ruhe"], h_); nn[weit] = nn2; dnn[weit] = d2
    Vf = RP["P_foto"][nn] + (Vq - RP["P_ruhe"][nn]); Vf[links, 1] = 2 * YM - Vf[links, 1]
    V_foto = m_(Vf)
    ER["v_foto_abstand_roh"] = {"median": round(float(np.median(dnn)), 4), "p99": round(float(np.percentile(dnn, 99)), 4),
                                "max": round(float(dnn.max()), 4), "hinweis": "V_foto = Rohpunkt (Fotopose nach Rumpf-Scherung) + Versatz zum naechsten verformten Rohpunkt; linke Seite = Spiegelbild der rechten (wie die Form)"}
    # Verzerrung der Umstellung je Rohdreieck im Halsband (0,05 < w_kopf < 0,95)
    Fr = RP["F"]; Pa, Pb = RP["P_foto"], RP["P_ruhe"]; wkr = RP["w_kopf"][Fr].mean(1)
    band = (wkr > 0.05) & (wkr < 0.95)
    e1a = Pa[Fr[band, 1]] - Pa[Fr[band, 0]]; e2a = Pa[Fr[band, 2]] - Pa[Fr[band, 0]]
    e1b = Pb[Fr[band, 1]] - Pb[Fr[band, 0]]; e2b = Pb[Fr[band, 2]] - Pb[Fr[band, 0]]
    u_ = e1a / (np.linalg.norm(e1a, axis=1)[:, None] + 1e-12); n_ = np.cross(e1a, e2a); A2 = np.linalg.norm(n_, axis=1)
    la_ = np.linalg.norm(e1a, axis=1); lb_ = np.linalg.norm(e2a, axis=1); lc_ = np.linalg.norm(e2a - e1a, axis=1)
    hmin = A2 / np.maximum(np.maximum(np.maximum(la_, lb_), lc_), 1e-12)          # kleinste Hoehe (Splitter-Dreiecke ausnehmen)
    ok = (A2 > 1e-10) & (hmin > 0.25 * np.maximum(np.maximum(la_, lb_), lc_) * 0.5)
    v_ = np.cross(n_ / (A2[:, None] + 1e-12), u_)
    Ma = np.stack([np.stack([np.sum(e1a * u_, 1), np.sum(e2a * u_, 1)], 1), np.stack([np.sum(e1a * v_, 1), np.sum(e2a * v_, 1)], 1)], 1)
    Mb = np.stack([e1b, e2b], 2)
    Jm = Mb[ok] @ np.linalg.inv(Ma[ok])
    sv = np.linalg.svd(Jm, compute_uv=False); ratio = sv[:, 0] / np.maximum(sv[:, 1], 1e-9)
    ER["hals_verzerrung"] = {"dreiecke": int(ok.sum()), "p50": round(float(np.percentile(ratio, 50)), 3), "p90": round(float(np.percentile(ratio, 90)), 3),
                             "p99_sigma1_sigma2": round(float(np.percentile(ratio, 99)), 3),
                             "p99_9": round(float(np.percentile(ratio, 99.9)), 3), "max": round(float(ratio.max()), 3),
                             "grenze": 1.35, "hinweis": "Rohmodell = Farbquelle; Fell und Malerei werden auf dem Ruhe-Netz neu gezeichnet"}
    # ---- Technik
    E3 = np.sort(np.concatenate([Tw[:, [0, 1]], Tw[:, [1, 2]], Tw[:, [2, 0]]]), 1)
    _, cnt = np.unique(E3, axis=0, return_counts=True)
    fl = np.linalg.norm(np.cross(V[Tw[:, 1]] - V[Tw[:, 0]], V[Tw[:, 2]] - V[Tw[:, 0]]), axis=1) / 2
    bild = G.get("bild")
    ER["technik"] = {"glb_punkte": int(len(G["P"])), "punkte": int(len(V)), "dreiecke": int(len(Tw)), "offene_kanten": int((cnt == 1).sum()),
                     "nicht_mannigfaltig": int((cnt > 2).sum()), "entartet_lt_1e-9": int((fl < 1e-9).sum()),
                     "textur": list(bild.shape) if bild is not None else None}
    # ---- Kopf gerade
    nase = V[np.argmax(np.where(kopf & ~ohr_m["ohr_l"] & ~ohr_m["ohr_r"], fk, -9))]
    aug = [m_(bl_tier(a)) for a in TXR["augen_fest"]]
    an = nase - 0.5 * (aug[0] + aug[1])
    ER["kopf"] = {"augen_m": [a.round(4).tolist() for a in aug], "augen_hoehe_diff_cm": round(abs(aug[0][2] - aug[1][2]) * 100, 2),
                  "augen_mitte_y_cm": round(0.5 * (aug[0][1] + aug[1][1]) * 100, 2), "nase_y_cm": round(float(nase[1]) * 100, 2),
                  "augen_nase_linie_grad": round(math.degrees(math.atan2(an[2], math.hypot(an[0], an[1]))), 1),
                  "blick_gier_grad": round(math.degrees(math.atan2(an[1], an[0])), 2)}
    # ---- Symmetrie (Halbbreiten je Schnitt x alle 5 cm, z 0,3-0,8 m)
    sym = []
    for z in np.arange(0.30, 0.81, 0.05):          # exakte Schnittkurven (Ebene z), je x alle 5 cm die Kreuzungen y links/rechts
        ks = schnitt_kurven(V, Tw, z)
        if not ks:
            continue
        pk = ks[0]["pts"]; q = np.roll(pk, -1, 0)
        for x in np.arange(pk[:, 0].min() + 0.03, pk[:, 0].max() - 0.03, 0.05):
            kr = (pk[:, 0] - x) * (q[:, 0] - x) < 0
            if kr.sum() < 2:
                continue
            t_ = (x - pk[kr, 0]) / (q[kr, 0] - pk[kr, 0]); yk = pk[kr, 1] + t_ * (q[kr, 1] - pk[kr, 1])
            if yk.max() > 0.01 and yk.min() < -0.01:
                sym.append([abs(yk.max() + yk.min()), float(x), float(z)])
    sym = np.array(sym)
    ER["symmetrie"] = {"schnitte": len(sym), "max_unterschied_cm": round(float(sym[:, 0].max()) * 100, 2),
                       "p95_cm": round(float(np.percentile(sym[:, 0], 95)) * 100, 2), "ueber_1_5cm": int((sym[:, 0] > 0.015).sum()),
                       "schlechteste": [[round(a * 100, 2), round(b, 2), round(c, 2)] for a, b, c in sym[np.argsort(-sym[:, 0])[:3]]]}
    # ---- Beine: Luecke links/rechts je Hoehe, Achsenpunkte
    Vg = V; Tg = Tw
    luecke = {"vorn": [], "hinten": []}; achsen = {}
    xm_vh = 0.5 * (m_(pf["VR"])[0] + m_(pf["HR"])[0])
    for z in np.arange(0.03, 0.351, 0.02):
        ks = schnitt_kurven(Vg, Tg, z)
        for paar, sel in (("vorn", lambda c: c[0] > xm_vh), ("hinten", lambda c: c[0] <= xm_vh)):
            kk = [k for k in ks if sel(k["c"]) and k["A"] < 0.06]
            L_ = [k for k in kk if k["c"][1] > 0]; R_ = [k for k in kk if k["c"][1] < 0]
            if L_ and R_:
                l0 = max(L_, key=lambda k: k["A"]); r0 = max(R_, key=lambda k: k["A"])
                gap = float(l0["pts"][:, 1].min() - r0["pts"][:, 1].max())
                luecke[paar].append([round(float(z), 2), round(gap * 100, 2)])
                for nm, k in ((paar[0].upper() + "L", l0), (paar[0].upper() + "R", r0)):
                    achsen.setdefault(nm, []).append([round(float(k["c"][0]), 4), round(float(k["c"][1]), 4), round(float(z), 3)])
    ER["bein_luecke_cm"] = {k: {"min": min(g for _, g in v) if v else None, "min_bis_0_29m": min(g for z_, g in v if z_ <= 0.29) if v else None,
                                "je_hoehe": v} for k, v in luecke.items()}
    # ---- Masse Abschnitt 1 (bei 1,0)
    mid = np.abs(V[:, 1]) < 0.03
    def oben_bei(x):
        m = mid & (np.abs(V[:, 0] - x) < 0.012) & (~kopf); return float(V[m, 2].max()) if m.any() else None
    xV = float(m_(np.array(PLj["beine"]["VR"]["Jz"]))[0]); xH = float(m_(np.array(PLj["beine"]["HR"]["Jz"]))[0])
    mb = mid & (np.abs(V[:, 0] - 0.5 * (xV + xH)) < 0.10) & (V[:, 2] > 0.2)
    rumpf = (~kopf) & (V[:, 2] > 0.35)
    ER["masse_m"] = {"widerrist": oben_bei(xV), "kruppe": oben_bei(xH), "bauch_tief": round(float(V[mb, 2].min()), 4),
                     "rumpf_halbbreite_max": round(float(np.abs(V[rumpf, 1]).max()), 4),
                     "spur_halb_vorn": round(float(abs(m_(pf["VR"])[1])), 4), "spur_halb_hinten": round(float(abs(m_(pf["HR"])[1])), 4),
                     "laenge": round(float(V[:, 0].max() - V[:, 0].min()), 4), "hoehe_mit_ohren": round(float(V[:, 2].max()), 4),
                     "tiefster_punkt_cm": round(float(V[:, 2].min()) * 100, 2)}
    # ---- Ohren-Probe (von vorn, Blick entlang -x): Ohr ueber dem Umriss des Kopfes ohne Ohren
    PXM = 577 * 0.544 * 0.35
    ohren_pr = {}
    kopf_o = kopf & ~ohr_m["ohr_l"] & ~ohr_m["ohr_r"]
    wm_ = kopf_o & (np.abs(uk) < 0.04) & (fk > -0.12)          # Wangen auf Augenhoehe, vor den Ohren
    W_kopf = float(V[wm_, 1].max() - V[wm_, 1].min())
    for nm in ("ohr_l", "ohr_r"):
        om = ohr_m[nm]; oy = V[om, 1]; top = float(V[om, 2].max())
        y_top = float(V[om][np.argmax(V[om, 2]), 1])
        s_ = kopf_o & (np.abs(V[:, 1] - y_top) < 0.01)
        ueber = top - float(V[s_, 2].max())
        ohren_pr[nm] = {"ueber_umriss_m": round(ueber, 4), "ueber_umriss_anteil_W": round(ueber / W_kopf, 3), "ueber_px_spiel": round(ueber * PXM, 1),
                        "breite_m": round(float(oy.max() - oy.min()), 4), "breite_px_spiel": round(float(oy.max() - oy.min()) * PXM, 1),
                        "spitze_m": V[om][np.argmax(V[om, 2])].round(4).tolist()}
    ER["ohren_vorn"] = {"kopfbreite_W_m": round(W_kopf, 4), **ohren_pr, "grenzen": ">= 0,10 W, >= 15 px breit, >= 4 px ueber dem Umriss"}
    # ---- Landmarken
    LM = {"rahmen": "tier-Meter bei Groesse 1,0: x vorn, y links, z oben, Boden z 0, y 0 = Mittelebene, x 0 = Mitte zwischen Vorder- und Hinterpfoten (vorlaeufig)",
          "skala_m_je_roh": S, "ursprung_roh": ursprung.tolist(),
          "augen": [a.round(4).tolist() for a in aug], "nasenspitze": nase.round(4).tolist(),
          "ohr_spitzen": {k: v["spitze_m"] for k, v in ohren_pr.items()},
          "ohr_basen": {("ohr_l" if m_(bl_tier(o["oberflaeche"]))[1] > 0 else "ohr_r"): m_(bl_tier(o["oberflaeche"])).round(4).tolist() for o in FI["ohren"]},
          "atlas_schaetzung": atl.round(4).tolist(), "c7_schaetzung": c7.round(4).tolist(), "kopfbreite_W": round(W_kopf, 4),
          "kopfrahmen": {"augen_mitte": AM.round(4).tolist(), "vorn": FW.round(4).tolist(), "oben": UPk.round(4).tolist(), "seitlich": LT.round(4).tolist()},
          "stummel": st.round(4).tolist()}
    km = kopf_o & (np.abs(V[:, 1]) < 0.02)
    LM["krone"] = V[km][np.argmax(V[km, 2])].round(4).tolist()
    hk = (np.abs(V[:, 1]) < 0.02) & (np.abs(V[:, 0] - atl[0]) < 0.015)   # Nacken-Oberlinie ueber dem Atlas (der Kopf geht ohne Stufe in den dicken Nacken)
    LM["hinterkopf_ueber_atlas"] = V[hk][np.argmax(V[hk, 2])].round(4).tolist() if hk.any() else None
    LM["kinn"] = kinn.round(4).tolist(); LM["kehle"] = kehle.round(4).tolist(); LM["kopf_grenze_normale"] = nk.round(4).tolist()
    for nm_, x in (("widerrist", xV), ("kruppe", xH)):
        m = mid & (np.abs(V[:, 0] - x) < 0.012) & (~kopf); LM[nm_] = V[m][np.argmax(V[m, 2])].round(4).tolist()
    LM["bauch"] = V[mb][np.argmin(V[mb, 2])].round(4).tolist()
    mbug = mid & (np.abs(V[:, 2] - 0.45 * S) < 0.012) & (~kopf); LM["bug"] = V[mbug][np.argmax(V[mbug, 0])].round(4).tolist()
    mre = mid & (V[:, 2] > 0.3 * S) & (V[:, 2] < 0.7 * S) & ~masken["stummel"]; LM["rumpfende"] = V[mre][np.argmin(V[mre, 0])].round(4).tolist()
    LM["beine"] = {}
    for p in FI["pfoten"]:
        nm = p["name"]; mk = masken["pfote_" + nm]; pv = V[mk]; un = pv[pv[:, 2] < 0.03]
        b_rechts = PLj["beine"][nm[0] + "R"]
        sg = 1 if nm[1] == "R" else -1
        def sp(p_):
            q = m_(np.array(p_)); q[1] = q[1] * sg; return q.round(4).tolist()
        LM["beine"][nm] = {"achse": achsen.get(nm, []), "ellbogen_knie": sp(b_rechts["Jz"]), "hand_sprung": sp(b_rechts["Kz"]),
                           "pfote_mitte": m_(bl_tier([p["bein"][0], p["bein"][1], ZB])).round(4).tolist(),
                           "ferse": un[np.argmin(un[:, 0])].round(4).tolist(), "zehenspitze": pv[np.argmax(pv[:, 0])].round(4).tolist(),
                           "sohlenrand": {"x": [round(float(un[:, 0].min()), 4), round(float(un[:, 0].max()), 4)],
                                          "y": [round(float(un[:, 1].min()), 4), round(float(un[:, 1].max()), 4)]}}
        f_ = LM["beine"][nm]["ferse"]; z_ = LM["beine"][nm]["zehenspitze"]
        LM["beine"][nm]["ballen"] = [round(f_[0] + 0.75 * (z_[0] - f_[0]), 4), round(0.5 * (f_[1] + z_[1]), 4), 0.0]
    jdump(LM, os.path.join(AUS, "landmarken_rig.json"))
    # ---- npz (massgeblich)
    UVg = G["UV"]
    np.savez_compressed(os.path.join(AUS, "C_rig_basis.npz"), V=V, T=Tw, T_glb=G["T"], glb_punkt=inv, UV=UVg, V_foto=V_foto,
                        skala_m_je_roh=np.float64(S), y_mitte_roh=np.float64(YM), ursprung_roh=ursprung, **{k: v for k, v in masken.items()})
    # ---- GLB + PNG zum Ansehen
    bild_png = Image.fromarray(bild.astype(np.uint8), "RGB"); bild_png.save(os.path.join(AUS, "C_rig_basis.png"))
    bufp = io.BytesIO(); bild_png.save(bufp, format="PNG")
    fn = np.cross(V[Tw[:, 1]] - V[Tw[:, 0]], V[Tw[:, 2]] - V[Tw[:, 0]])
    NV = np.zeros_like(V)
    for k in range(3):
        np.add.at(NV, Tw[:, k], fn)
    NV /= np.linalg.norm(NV, axis=1)[:, None] + 1e-12
    Vglb = V[inv]; pos = np.stack([Vglb[:, 1], Vglb[:, 2], Vglb[:, 0]], 1); nrm = NV[inv]; nrm = np.stack([nrm[:, 1], nrm[:, 2], nrm[:, 0]], 1)
    schreibe_glb(os.path.join(AUS, "C_rig_basis.glb"), pos, nrm, UVg, G["T"], bufp.getvalue())
    ER["dateien"] = ["C_rig_basis.npz", "C_rig_basis.glb", "C_rig_basis.png", "landmarken_rig.json", "pruef_form.json"]
    ER["dauer_s"] = round(time.time() - T0a, 1)
    jdump(ER, os.path.join(AUS, "pruef_form.json"))
    log("ABGABE fertig", json.dumps({k: ER[k] for k in ("technik", "kopf", "symmetrie", "masse_m")}))
    log("Beine Luecke", json.dumps({k: v["min"] for k, v in ER["bein_luecke_cm"].items()}), "Ohren", json.dumps(ER["ohren_vorn"]))


if __name__ == "__main__":
    J_ = json.load(open(CFG["form_info_f1"], encoding="utf-8"))
    ZB = float(np.round(min(p["boden"] for p in J_["pfoten"]), 5))
    if MODUS == "plan":
        plan()
    elif MODUS == "abgabe":
        abgabe()
