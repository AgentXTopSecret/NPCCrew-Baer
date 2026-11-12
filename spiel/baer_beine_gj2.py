# Lauf baer-gen-junges-v2 (12.11.2026), Bauer BEINE: Netz des Generator-Jungen auf KURZE Beine umstellen (PLAN.md 4.2) und die
# Baerenfuesse des Standard-Jungen ansetzen (PLAN.md 4.3, Weg A). Neu (Vorbilder nur gelesen: baer_netz_jfuss.py, baer_form_jfuss.py).
#   netz   : affine Knochen-Umstellung (LBS der Abbildungen je Knochen mit den HEUTIGEN Endgewichten), Rumpf breiter (Seitenfeld)
#   pfoten : Generator-Bein unter dem Schnitt weg, Pfoten des Standard-Jungen (GLB d9931d32) an das neue Gelenk, Naht-Band (Reissverschluss
#            zwischen den Ringen), Dreiecks-Budget (Halbkanten-Kollaps nur in der Std-Pfote), UV-Atlas (Gen x0,86, Pfoten-Inseln in den
#            freien Streifen), Textur (Gen nachgerechnet, Pfoten-Texel aus der Std-Textur je Dreieck uebertragen, Naht-Band gemischt)
# Aufruf: python baer_beine_gj2.py netz   SKELETT_GJ2.json AUS_NETZ1.npz
#         python baer_beine_gj2.py pfoten SKELETT_GJ2.json NETZ1.npz AUS_NETZ_GJ2.npz AUS_GEWICHTE_START.npz AUS_TEXTUR.png [AUS_ATLAS.json] [PARAM.json]
# Rahmen tier-Meter (x vorn, y links, z oben, Boden z 0) im Skelettrahmen; Dump-Raum = (y, z, -x) x 0,544. Nur numpy + PIL.
# Statisch/offline gerechnet, nicht gespielt. Liest nur _arbeit/baer_gen_junges/v2/quelle und v2/beine; schreibt nur die Ausgaben.
import json
import sys
import time

import numpy as np

Q = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/quelle/"
M2U = 0.544
T0 = time.time()
TORSO = ("Bip01_Pelvis", "Bip01_Spine", "Bip01_Spine1", "Bip01_Tail")
# Umstellung (PLAN 4.2): quer x1,05 am Oberschenkel/Oberarm, x1,14 am Unterschenkel/Unterarm; laengs der Kettenfaktor
QUER_OBEN = 1.05
QUER_UNTEN = 1.14
UEBERGANG = 0.04          # Oberschenkel/Oberarm: ueber dem Gelenk keine Laengs-/Querskalierung (weich +-4 cm)
BREIT = 0.05              # Rumpf-Seitenfeld (PLAN 4.2.2: 0,09; dazu kommt hier die Spur-Verschiebung bis 2 cm)


def log(*a):
    print("BEINE", round(time.time() - T0, 1), *a, flush=True)


def sst(a, b, x):
    t = np.clip((np.asarray(x, float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def tier(P):
    P = np.asarray(P, float)
    return np.stack((-P[..., 2], P[..., 0], P[..., 1]), -1) / M2U


def dump(T):
    T = np.asarray(T, float)
    return np.stack((T[..., 1], T[..., 2], -T[..., 0]), -1) * M2U


def skelett(pfad):
    sk = json.load(open(pfad))
    alt = {n: np.array(v, float) for n, v in sk["ruhe_m_alt"].items()}
    neu = {n: np.array(v, float) for n, v in sk["ruhe_m"].items()}
    return sk, alt, neu


def axial_oben(t, f, w=UEBERGANG):
    """Laengs-Abbildung am oberen Bein-Knochen: t' = Integral von s, s = 1 ueber dem Gelenk, f darunter (weich, monoton)."""
    tau = np.linspace(-0.6, 0.8, 14001)
    s = 1.0 + (f - 1.0) * sst(-w, w, tau)
    I = np.concatenate(([0.0], np.cumsum(0.5 * (s[1:] + s[:-1]) * np.diff(tau))))
    I -= np.interp(0.0, tau, I)
    return np.interp(t, tau, I)


def knochen_abbildung(nm, V, alt, neu, sk):
    """Abbildung der Ruhe-Punkte V (n x 3) fuer Knochen nm (PLAN 4.2.1)."""
    f_h = sk["faktoren"]["beine_hinten"]
    f_v = sk["faktoren"]["beine_vorn"]
    teile = nm.split("_")
    art = teile[-1] if len(teile) >= 3 else ""
    kind = {"Thigh": "Calf", "Calf": "Foot", "UpperArm": "Forearm", "Forearm": "Hand"}
    if art in kind:
        s = teile[1]
        j0, j1 = alt[nm], alt["Bip01_%s_%s" % (s, kind[art])]
        a = (j1 - j0) / np.linalg.norm(j1 - j0)
        f = f_h if art in ("Thigh", "Calf") else f_v
        r = V - j0
        t = r @ a
        perp = r - t[:, None] * a
        if art in ("Thigh", "UpperArm"):
            t2 = axial_oben(t, f)
            c = 1.0 + (QUER_OBEN - 1.0) * sst(-UEBERGANG, UEBERGANG, t)
        else:
            t2 = f * t
            c = np.full(len(V), QUER_UNTEN)
        return neu[nm] + t2[:, None] * a + c[:, None] * perp
    if art in ("Foot", "Toe0", "Hand"):
        # Pfote: unter dem Gelenk reine Verschiebung; UEBER dem Gelenk wie der Unterschenkel/Unterarm (sonst stauchen die Mischzonen
        # Unterschenkel/Pfote, weil die zwei Abbildungen auseinanderlaufen) -- weich zwischen Gelenk-z +1 und +4 cm
        s = teile[1]
        gel = "Bip01_%s_%s" % (s, "Foot" if art in ("Foot", "Toe0") else "Hand")
        ob = "Bip01_%s_%s" % (s, "Calf" if art in ("Foot", "Toe0") else "Forearm")
        u = sst(alt[gel][2] + 0.01, alt[gel][2] + 0.04, V[:, 2])[:, None]
        return (1.0 - u) * (V + (neu[gel] - alt[gel])[None, :]) + u * knochen_abbildung(ob, V, alt, neu, sk)
    # Rumpf, Kopf, Schwanz: reine Verschiebung mit dem eigenen Gelenk
    return V + (neu[nm] - alt[nm])[None, :]


BEIN_KN = {"VL": ("Bip01_L_UpperArm", "Bip01_L_Forearm", "Bip01_L_Hand"), "VR": ("Bip01_R_UpperArm", "Bip01_R_Forearm", "Bip01_R_Hand"),
           "HL": ("Bip01_L_Thigh", "Bip01_L_Calf", "Bip01_L_Foot"), "HR": ("Bip01_R_Thigh", "Bip01_R_Calf", "Bip01_R_Foot")}
BEIN_SPITZE = {"VL": "Bip01_L_Hand", "VR": "Bip01_R_Hand", "HL": "Bip01_L_Toe0", "HR": "Bip01_R_Toe0"}


def seg_abstand(P, a, b):
    ab = b - a
    t = np.clip(((P - a) @ ab) / max(ab @ ab, 1e-12), 0, 1)
    return np.linalg.norm(P - (a + t[:, None] * ab), axis=1)


def naechster_bein_knochen(P, alt):
    """Je Punkt: naechste Bein-Knochenstrecke (12 Strecken, altes Skelett) -> (Bein, Knochenname)."""
    kand = []
    for k, (o, u, f) in BEIN_KN.items():
        sp = alt[BEIN_SPITZE[k]] if k[0] == "H" else alt[f] + np.array((0.12, 0.0, -0.08))
        kand += [(k, o, alt[o], alt[u]), (k, u, alt[u], alt[f]), (k, f, alt[f], sp)]
    D = np.stack([seg_abstand(P, a, b) for _, _, a, b in kand], 1)
    j = np.argmin(D, 1)
    return [kand[i][0] for i in j], [kand[i][1] for i in j], D.min(1)


def abbildungs_gewichte(V0, W, namen, alt, z0=0.30, z1=0.40):
    WR = W.copy()
    torso = [namen.index(n) for n in namen if not any(k in n for k in ("Thigh", "Calf", "Foot", "Toe0", "UpperArm", "Forearm", "Hand"))]
    u = 1.0 - sst(z0, z1, V0[:, 2])
    beinw = 1.0 - WR[:, torso].sum(1)
    m = (u > 0) & (WR[:, torso].sum(1) > 0) & (beinw >= 0.25)     # nur Bein-Punkte (Bauch/Brust-Unterseite bleibt Rumpf)
    _, kn, _ = naechster_bein_knochen(V0[m], alt)
    idx = np.nonzero(m)[0]
    wt = WR[idx][:, torso].sum(1) * u[idx]
    WR[np.ix_(idx, torso)] *= (1.0 - u[idx])[:, None]
    WR[idx, [namen.index(k) for k in kn]] += wt
    return WR


# ---------------------------------------------------------------------------------------------------------------------------------
# RAUM-ABBILDUNG Phi (12.11., ersetzt die LBS der Knochen-Abbildungen): Haut UND Skelett-Gelenke laufen durch DIESELBE Abbildung,
# damit Haut und Gelenke deckungsgleich bleiben. Grund: mit Knochen-Abbildungen + Rumpf-Verschiebung lag der Spalt zwischen den Beinen
# (Rumpf-Gewicht bis z 0,34 hinten / 0,46 vorn) nach dem Absenken UNTER den Bein-Innenseiten -> 32..122 umgeklappte Dreiecke (gemessen).
#   Phi1 (senkrecht): z' = lam(x) Zc(x, z) + (1 - lam(x)) (z + dz)
#        Zc: zwischen Sprung-/Handgelenk (z_a) und Huefte/Schulter (z_j) mal f gestaucht (Ecken weich +-3 cm), darunter fest, darueber
#        z + dz (dz = -(1 - f)(z_j - z_a) = -0,1652 vorn und hinten gleich). lam = 1 an den Beinpaaren (Beine samt Spalt stauchen),
#        0 unter dem Bauch zwischen den Beinpaaren (Bauch bleibt tief: reine Verschiebung). lam haengt nur von x ab -> dz'/dz > 0
#        ueberall, die Abbildung klappt nichts um.
#   Phi2 (quer, Spur): y' = y + dy(x) tanh(y / 0,025) h(z'); h = 1 bis 2 cm ueber der neuen Huefte/Schulter, weich 0 bis +18 cm.
# Kein Laengs-Faktor an den Knochen-Achsen: die Beine werden SENKRECHT gestaucht (Knie/Ellbogen behalten ihr x) -- Knie und Ellbogen
# etwas staerker gebeugt als beim 2c (Gelenke = Phi(alte Gelenke), Skelett aus baer_skelett_gj2.py).
PHI = dict(f_h=0.72, f_v=None, za_h=0.100, za_v=0.097, zj_h=0.690, zj_v=0.717, ecke=0.03,
           bauch_x=(-0.24, -0.10, -0.06, 0.10), vh_x=(-0.10, 0.10), dy_h=0.020, dy_v=0.018, dy_brt=(0.025, 0.12),
           brt_z_h=(0.24, 0.34), brt_z_v=(0.36, 0.46), h_ueber=(0.02, 0.18))


def phi_para():
    p = dict(PHI)
    dz = -(1.0 - p["f_h"]) * (p["zj_h"] - p["za_h"])
    p["dz"] = dz
    p["f_v"] = 1.0 + dz / (p["zj_v"] - p["za_v"])
    return p


_ZC = {}


def _zc_tabelle(f, za, zj, w):
    key = (f, za, zj, w)
    if key not in _ZC:
        tau = np.linspace(-0.2, 1.6, 36001)
        s = 1.0 + (f - 1.0) * (sst(za - w, za + w, tau) - sst(zj - w, zj + w, tau))
        I = np.concatenate(([0.0], np.cumsum(0.5 * (s[1:] + s[:-1]) * np.diff(tau))))
        I += -0.2 - I[0]
        _ZC[key] = (tau, I)
    return _ZC[key]


def phi(P, p=None):
    """Raum-Abbildung Phi2 o Phi1 fuer Punkte P (n x 3, tier-m, alt) -> neu."""
    p = phi_para() if p is None else p
    P = np.asarray(P, float)
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    tv = sst(p["vh_x"][0], p["vh_x"][1], x)                    # 0 hinten, 1 vorn
    th, Ih = _zc_tabelle(p["f_h"], p["za_h"], p["zj_h"], p["ecke"])
    tv_, Iv = _zc_tabelle(p["f_v"], p["za_v"], p["zj_v"], p["ecke"])
    zc = (1.0 - tv) * np.interp(z, th, Ih) + tv * np.interp(z, tv_, Iv)
    b = p["bauch_x"]
    lam = 1.0 - sst(b[0], b[1], x) * (1.0 - sst(b[2], b[3], x))
    z2 = lam * zc + (1.0 - lam) * (z + p["dz"])
    # Spur: nur an den Beinpaaren (lam), Breite der tanh-Stufe unten im Spalt schmal (Spalt wird breiter), darueber breit (Ruecken-/
    # Steiss-Mitte nur x1,17 quer gedehnt statt x1,8)
    dy = ((1.0 - tv) * p["dy_h"] + tv * p["dy_v"]) * lam
    zj2 = (1.0 - tv) * (p["zj_h"] + p["dz"]) + tv * (p["zj_v"] + p["dz"])
    h = 1.0 - sst(zj2 + p["h_ueber"][0], zj2 + p["h_ueber"][1], z2)
    zb0 = (1.0 - tv) * p["brt_z_h"][0] + tv * p["brt_z_v"][0]
    zb1 = (1.0 - tv) * p["brt_z_h"][1] + tv * p["brt_z_v"][1]
    u = np.clip((z2 - zb0) / (zb1 - zb0), 0.0, 1.0)
    u = u * u * (3.0 - 2.0 * u)
    w = p["dy_brt"][0] + (p["dy_brt"][1] - p["dy_brt"][0]) * u
    y2 = y + dy * np.tanh(y / w) * h
    return np.stack((x, y2, z2), 1)


def tri_verzerrung(V0, V1, T):
    """sigma1, sigma2 der Abbildung alt -> neu je Dreieck (in der Dreiecksebene), umgeklappt (Normale dreht > 90 Grad)."""
    e1, e2 = V0[T[:, 1]] - V0[T[:, 0]], V0[T[:, 2]] - V0[T[:, 0]]
    f1, f2 = V1[T[:, 1]] - V1[T[:, 0]], V1[T[:, 2]] - V1[T[:, 0]]
    n0 = np.cross(e1, e2)
    n1 = np.cross(f1, f2)
    l1 = np.linalg.norm(e1, axis=1)
    u = e1 / np.maximum(l1, 1e-12)[:, None]
    nn = n0 / np.maximum(np.linalg.norm(n0, axis=1), 1e-15)[:, None]
    v = np.cross(nn, u)
    Rm = np.stack((np.stack(((e1 * u).sum(1), (e2 * u).sum(1)), 1), np.stack(((e1 * v).sum(1), (e2 * v).sum(1)), 1)), 1)
    gut = np.abs(np.linalg.det(Rm)) > 1e-12
    RI = np.zeros_like(Rm)
    RI[gut] = np.linalg.inv(Rm[gut])
    F = np.einsum("tij,tjk->tik", np.stack((f1, f2), 2), RI)
    sv = np.linalg.svd(F, compute_uv=False)
    um = (n0 * n1).sum(1) <= 0
    return sv[:, 0], sv[:, 1], um, gut


def netz(skp, aus):
    sk, alt, neu = skelett(skp)
    N = np.load(Q + "gen/netz_rig.npz")
    G = np.load(Q + "gen/gewichte_end.npz")
    namen = [str(n) for n in G["namen"]]
    assert namen == sk["namen"]
    V0 = N["V"].astype(float)
    T = N["T"]
    W = G["W"].astype(float)
    # 1. Raum-Abbildung Phi (Haut wie Gelenke)
    V1 = phi(V0)
    wsum = W.sum(1)
    assert np.abs(wsum - 1).max() < 1e-6
    # 2. Rumpf breiter: Seitenfeld (Flanke/Huefte/Schulterblatt), weich zum Ruecken-Grat, zum Hals und zum Stummel
    w_t = sum(W[:, namen.index(n)] for n in TORSO) + W[:, namen.index("Bip01_L_Thigh")] * 0.0
    x, y, z = V1[:, 0], V1[:, 1], V1[:, 2]
    # Ruecken-Grat je x: oberster Rumpfpunkt (Band 4 cm), geglaettet
    xs = np.arange(-0.80, 0.70, 0.02)
    top = np.full(len(xs), np.nan)
    for i, x0 in enumerate(xs):
        mm = (np.abs(x - x0) < 0.02) & (w_t > 0.3)
        if mm.any():
            top[i] = z[mm].max()
    ok = np.isfinite(top)
    top = np.interp(xs, xs[ok], top[ok])
    top = np.convolve(np.pad(top, 3, mode="edge"), np.ones(7) / 7, mode="valid")
    zt = np.interp(x, xs, top)
    m_z = 1.0 - sst(zt - 0.10, zt - 0.04, z)
    x_hals = neu["Bip01_L_UpperArm"][0] - 0.05          # ab hier zum Hals hin aus
    m_x = (1.0 - sst(x_hals, x_hals + 0.10, x)) * sst(neu["Bip01_L_Thigh"][0] - 0.30, neu["Bip01_L_Thigh"][0] - 0.18, x)
    stummel = N["stummel"].astype(bool)
    k = BREIT * m_z * m_x * np.clip(w_t + W[:, [namen.index("Bip01_L_Thigh"), namen.index("Bip01_R_Thigh"),
                                                 namen.index("Bip01_L_UpperArm"), namen.index("Bip01_R_UpperArm")]].sum(1) * 0.5, 0, 1)
    k[stummel] = 0.0
    V2 = V1.copy()
    V2[:, 1] = y * (1.0 + k)
    # Messen
    s1, s2, um, gut = tri_verzerrung(V0, V2, T)
    bein = np.zeros(len(V0))
    for s in "LR":
        for kk in ("Thigh", "Calf", "UpperArm", "Forearm"):
            bein += W[:, namen.index("Bip01_%s_%s" % (s, kk))]
    tb = bein[T].mean(1) >= 0.5
    tr = (w_t[T].mean(1) >= 0.5)
    info = dict(
        dreiecke=int(len(T)), umgeklappt=int((um & gut).sum()),
        bein_sig1_p99=round(float(np.percentile(s1[tb & gut], 99)), 3), bein_sig2_p1=round(float(np.percentile(s2[tb & gut], 1)), 3),
        bein_ratio_p99=round(float(np.percentile((s1 / np.maximum(s2, 1e-9))[tb & gut], 99)), 3),
        rumpf_sig1_p99=round(float(np.percentile(s1[tr & gut], 99)), 3),
        rumpf_ratio_p99=round(float(np.percentile((s1 / np.maximum(s2, 1e-9))[tr & gut], 99)), 3),
        rumpf_halbbreite_vorher=round(float(np.abs(V0[w_t >= 0.5, 1]).max()), 4),
        rumpf_halbbreite_nachher=round(float(np.abs(V2[w_t >= 0.5, 1]).max()), 4),
        seitenfeld_max=round(float(k.max()), 4))
    log("NETZ", info)
    out = {k_: N[k_] for k_ in N.files}
    out["V"] = V2
    out["V_alt"] = V0
    out["netz_info"] = np.array(json.dumps(info))
    np.savez(aus, **out)
    log("->", aus)
    return info


if __name__ == "__main__":
    if sys.argv[1] == "netz":
        netz(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "pfoten":
        import baer_pfoten_gj2 as PF          # noqa: E402  (Teil 4.3, eigene Datei wegen Laenge)
        PF.pfoten_ganz(*sys.argv[2:])
