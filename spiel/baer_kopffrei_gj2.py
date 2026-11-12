# Lauf baer-gen-junges-v2 (12.11.2026), Bauer GESICHT: Kopf frei von Brust/Hals-Falte (PLAN 5.1.5: "Kopf darf in keinem Clip in Brust/
# Unterarm stecken"). Neu. Der groessere Kopf (x1,12, Schnauze) drueckt in Maul (Kopf tief zur Brust) und Rear (Kehle an der Brust)
# mit dem STARREN Kopf (Head+Jaw >= 0,999) in die Brust-/Halshaut (Windungszahl; vorher 13 Punkte, mit dem neuen Kopf 28-29).
# Hier je Bild der kleinste Hebewinkel des Kopfes (0..MAX Grad in 1-Grad-Schritten, Drehung nur von Bip01_Head um seine Querachse,
# Drehpunkt Kopfgelenk, wie baer_sitzkopf_gj2.py mit umgekehrtem Vorzeichen), bei dem kein starrer Kopfpunkt mehr im Koerper steckt
# (sonst der Winkel mit den wenigsten); danach zeitlich geglaettet (gleitendes Maximum +-3 Bilder, dann Mittel +-2), erstes und letztes
# Bild unveraendert (Uebergang zu Idle). Nur die genannten Clips; Becken und alle anderen Knochen unveraendert.
# Aufruf: python baer_kopffrei_gj2.py SKELETT.json NETZ.npz GEWICHTE.npz CLIPS_EIN.npz CLIPS_AUS.npz INFO.json [clips=A,B] [max=15]
# Statisch/offline, deterministisch, nicht gespielt.
import json
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/gegen/werkzeug")
import baer_umrechnen_gj2 as U  # noqa: E402
import g_durch as gd  # noqa: E402


def drin_zahl(G, M, T, starr, rest):
    P = G.haut(M)
    nr = np.cross(P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]])
    vn = np.zeros_like(P)
    for k in range(3):
        np.add.at(vn, T[:, k], nr)
    vn /= np.linalg.norm(vn, axis=1, keepdims=True) + 1e-12
    vol = np.einsum("ij,ij->i", P[T[:, 0]], np.cross(P[T[:, 1]], P[T[:, 2]])).sum()
    if vol < 0:
        vn = -vn
    A = P[rest][::3]
    q = P[starr]
    dd = (q * q).sum(1)[:, None] - 2 * q @ A.T + (A * A).sum(1)[None]
    kk = starr[np.sqrt(np.maximum(dd.min(1), 0)) < 0.06]
    if not len(kk):
        return 0
    Q = P[kk] + 0.002 * vn[kk]
    wz = np.abs(gd._exakt(Q, P[T[:, 0]], P[T[:, 1]], P[T[:, 2]]) / (4 * np.pi))
    return int((wz > 0.5).sum())


def main():
    skp, netz, gew, ein, aus, info_aus = sys.argv[1:7]
    kv = dict(x.split("=", 1) for x in sys.argv[7:])
    clips = kv.get("clips", "NCBear_Maul,NCBear_Rear").split(",")
    mx = int(kv.get("max", 15))
    G = U.Gerippe(skp, netz, gew)
    T = G.netz["T"]
    wk = G.W[:, G.idx["Bip01_Head"]] + G.W[:, G.idx["Bip01_Jaw"]]
    starr = np.nonzero(wk >= 0.999)[0]
    rest = np.nonzero(wk < 0.5)[0]
    ih, ip = G.idx["Bip01_Head"], G.idx["Bip01_Pelvis"]
    B = G.BWr[ih]
    Binv = np.linalg.inv(B)

    def heb(g_):
        return Binv @ U.A_TD.T @ U.ry(-float(g_)) @ U.A_TD @ B

    Z = dict(np.load(ein))
    info = {"max_grad": mx}
    for c in clips:
        R0, pel = Z[c + "_R"], Z[c + "_pel"]
        n = len(R0)
        need = np.zeros(n)
        vorher = []
        for f in range(n):
            t = G.t_j.copy()
            t[ip] = pel[f]
            Rl = R0[f].copy()
            z0 = drin_zahl(G, G.fk(t, Rl), T, starr, rest)
            vorher.append(z0)
            if z0 == 0:
                continue
            best = (z0, 0)
            for g_ in range(1, mx + 1):
                Rl = R0[f].copy()
                Rl[ih] = Rl[ih] @ heb(g_)
                z = drin_zahl(G, G.fk(t, Rl), T, starr, rest)
                if z < best[0]:
                    best = (z, g_)
                if z == 0:
                    break
            need[f] = best[1]
        # glaetten: gleitendes Maximum +-3, dann Mittel +-2; erstes/letztes Bild 0
        m3 = np.array([need[max(0, f - 3):f + 4].max() for f in range(n)])
        sm = np.array([m3[max(0, f - 2):f + 3].mean() for f in range(n)])
        sm[0] = sm[-1] = 0.0
        R = R0.copy()
        nachher = []
        for f in range(n):
            if sm[f] > 0:
                R[f, ih] = R0[f, ih] @ heb(sm[f])
            t = G.t_j.copy()
            t[ip] = pel[f]
            nachher.append(drin_zahl(G, G.fk(t, R[f]), T, starr, rest))
        Z[c + "_R"] = R
        info[c] = dict(bilder=n, hebe_grad_max=round(float(sm.max()), 2), bilder_gehoben=int((sm > 0).sum()),
                       starr_drin_vorher_max=int(max(vorher)), starr_drin_nachher_max=int(max(nachher)),
                       hebe_grad=[round(float(x), 2) for x in sm])
        print("KOPFFREI", c, json.dumps({k: v for k, v in info[c].items() if k != "hebe_grad"}), flush=True)
    np.savez(aus, **Z)
    json.dump(info, open(info_aus, "w"), indent=1)


if __name__ == "__main__":
    main()
