# Lauf baer-gen-junges-v2 (12.11.2026), Bauer BEINE: Netz des Generator-Jungen auf KURZE Beine umstellen (PLAN.md 4.2) und die
# Baerenfuesse des Standard-Jungen ansetzen (PLAN.md 4.3, Weg A). Neu (Vorbilder nur gelesen: baer_netz_jfuss.py, baer_form_jfuss.py).
#   netz   : affine Knochen-Umstellung (LBS der Abbildungen je Knochen mit den HEUTIGEN Endgewichten), Rumpf breiter (Seitenfeld)
#   pfoten : Generator-Bein unter dem Schnitt weg, Pfoten des Standard-Jungen (GLB d9931d32) an das neue Gelenk, Naht-Band (Reissverschluss
#            zwischen den Ringen), Dreiecks-Budget (Halbkanten-Kollaps nur in der Std-Pfote), UV-Atlas (Gen x0,86, Pfoten-Inseln in den
#            freien Streifen), Textur (Gen nachgerechnet, Pfoten-Texel aus der Std-Textur je Dreieck uebertragen, Naht-Band gemischt)
# Aufruf: python baer_beine_gj2.py netz   SKELETT_GJ2.json AUS_NETZ1.npz
#         python baer_beine_gj2.py pfoten SKELETT_GJ2.json NETZ1.npz AUS_NETZ_GJ2.npz AUS_TEXTUR.png [AUS_ATLAS.json]
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
BREIT = 0.09              # Rumpf-Seitenfeld (PLAN 4.2.2)


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
    # Rumpf, Kopf, Schwanz, Pfoten: reine Verschiebung mit dem eigenen Gelenk (Pfote = Sprung-/Handgelenk)
    return V + (neu[nm] - alt[nm])[None, :]


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
    # 1. affine Knochen-Umstellung (LBS der Abbildungen)
    V1 = np.zeros_like(V0)
    for b, nm in enumerate(namen):
        m = W[:, b] > 0
        if not m.any():
            continue
        V1[m] += W[m, b][:, None] * knochen_abbildung(nm, V0[m], alt, neu, sk)
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
        PF.pfoten(*sys.argv[2:])
