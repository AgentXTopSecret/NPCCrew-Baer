# Prueft, was die Engine aus den GLB-Dateien liest (Dump.java -> Text): Clips, Knochen, Haut je Bild, Weg, Fussgleiten, Dehnung.
# Aufruf: python tier_pruef.py dump_main.txt [dump_deer.txt reh_ordner]
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from dumpread import lese

np.set_printoptions(precision=3, suppress=True)
A = sys.argv[1]
B = sys.argv[2] if len(sys.argv) > 2 else None
R = sys.argv[3] if len(sys.argv) > 3 else None


def skin(M, off, V):
    h = np.c_[V[:, :3], np.ones(len(V))]
    out = np.zeros((len(V), 3))
    for k in range(4):
        w = V[:, 3 + k]
        b = V[:, 7 + k].astype(int)
        S = np.einsum("nij,njk->nik", M[b], off[b])
        out += w[:, None] * np.einsum("nij,nj->ni", S, h)[:, :3]
    return out


def kanten(el):
    T = el.reshape(-1, 3)
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]), 0)
    E.sort(1)
    return np.unique(E, axis=0)


D = lese(A)
V = D["verts"]
E = kanten(D["el"])
rest = V[:, :3]
L0 = np.linalg.norm(rest[E[:, 0]] - rest[E[:, 1]], axis=1)
E = E[L0 > 0.004]
L0 = L0[L0 > 0.004]
HAUPT = np.argmax(V[:, 3:7], 1)
HAUPT = V[np.arange(len(V)), 7 + HAUPT].astype(int)
print("Knochen", len(D["names"]), D["names"])
print("Hierarchie", D["par"])
print("Punkte", len(V), "Dreiecke", len(D["el"]) // 3, "Ruhe-Ausmass", rest.min(0), rest.max(0))
wsum = V[:, 3:7].sum(1)
print("Gewichtssumme min/max %.4f %.4f, Einfluesse max %d" % (wsum.min(), wsum.max(), (V[:, 3:7] > 0).sum(1).max()))
idx = D["idx"]
for need in ("Dummy01", "Bip01", "Translation_Data", "Bip01_Head", "Bip01_Spine", "Bip01_L_Calf", "Bip01_R_Calf", "Bip01_L_Foot", "Bip01_R_Foot", "Bip01_Pelvis", "Bip01_Neck"):
    assert need in idx, need
print("Index Dummy01 %d Bip01 %d" % (idx["Dummy01"], idx["Bip01"]))
ball_b = {}
for nm in ("Bip01_L_Hand", "Bip01_R_Hand", "Bip01_L_Foot", "Bip01_R_Foot"):
    k = idx[nm]
    m = ((V[:, 7:11].astype(int) == k) & (V[:, 3:7] > 0.99)).any(1)
    p = rest[m]
    sohle = p[p[:, 1] < p[:, 1].min() + 0.012]
    ball_b[nm] = sohle[np.argmin(sohle[:, 2])]
ERG = {}
for name, c in sorted(D["clips"].items()):
    T = c["T"]
    M = c["M"]
    ti = idx["Translation_Data"]
    td = np.array([c["L"][fr][ti][:3] if ti in c["L"][fr] else [0, 0, 0] for fr in range(len(T))])   # lokal, so liest die Engine den Weg
    weg = -td[:, 2]
    dur = c["dur"]
    bb = []
    smax = 0
    s99 = 0
    smin = 9
    ymin = 9
    wo = {}
    for fr in range(len(T)):
        P = skin(M[fr], D["off"], V)
        bb.append((P.min(0), P.max(0)))
        Ln = np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1) / np.maximum(L0, 1e-6)
        if Ln.max() > smax:
            k = np.argmax(Ln)
            wo = dict(bild=fr, knochen=D["names"][HAUPT[E[k, 0]]], ort=np.round(rest[E[k, 0]], 3))
        for kk in np.nonzero(Ln > 1.6)[0]:
            nm_ = D["names"][HAUPT[E[kk, 0]]]
            wo.setdefault("ueber1_6", {}).setdefault(nm_, 0)
            wo["ueber1_6"][nm_] += 1
        smax = max(smax, Ln.max())
        s99 = max(s99, np.percentile(Ln, 99.5))
        smin = min(smin, Ln.min())
        ymin = min(ymin, P[:, 1].min())
    lo = np.min([b[0] for b in bb], 0)
    hi = np.max([b[1] for b in bb], 0)
    print("\nCLIP %s Dauer %.3f s, Abtastungen %d, ohne Schluessel: %s" % (name, dur, len(T), c["nokeys"] or "keiner"))
    print("  gehaeutet ueber den Clip %s .. %s ; Bild 0 %s .. %s" % (lo, hi, bb[0][0], bb[0][1]))
    print("  Weg Ende %.4f E, %.3f E/s = %.2f Kacheln/s; Seitenweg x %.4f" % (weg[-1], weg[-1] / dur, weg[-1] / dur * 1.6, td[-1, 0]))
    print("  Dehnung Kanten: max %.2f, 99,5%%-Wert %.2f, Stauchung min %.2f; tiefster Punkt y %.3f" % (smax, s99, smin, ymin))
    d01 = max(np.abs(M[0][i] - M[-1][i]).max() for i in range(len(D["names"])) if D["names"][i] != "Translation_Data")
    print("  schlimmste Dehnung", {k: v for k, v in wo.items() if k != "ueber1_6"}, "Kanten ueber 1,6 nach Knochen", wo.get("ueber1_6", {}))
    print("  erstes gegen letztes Bild (ohne Weg): max Abweichung %.5f" % d01)
    ERG[name] = dict(lo=lo, hi=hi, ymin=ymin, smax=smax, s99=s99)
    if weg[-1] > 0.01:
        for nm, b in ball_b.items():
            k = idx[nm]
            bw = np.array([(M[fr][k] @ D["off"][k] @ np.r_[b, 1])[:3] for fr in range(len(T))])
            vorn_welt = -bw[:, 2] * 1.5 + weg * 1.6
            st = bw[:, 1] < b[1] + 0.004
            seg = []
            cur = []
            for i in range(len(T)):
                if st[i]:
                    cur.append(i)
                elif cur:
                    seg.append(cur)
                    cur = []
            if cur:
                seg.append(cur)
            gl = [vorn_welt[sg].max() - vorn_welt[sg].min() for sg in seg if len(sg) >= 3]
            v = np.diff(vorn_welt) / np.diff(T)
            vs = v[st[:-1] & st[1:]]
            print("  %-13s Stuetze %2d/%d Bilder, Gleiten je Stuetze %s Kacheln, Tempo in der Stuetze %.3f Kacheln/s, Hub max %.3f E"
                  % (nm, st.sum(), len(T), np.round(gl, 3), np.abs(vs).mean() if len(vs) else -1, bw[:, 1].max() - b[1]))
if B:
    D2 = lese(B)
    V2 = D2["verts"]
    print("\nRUECKFALL Knochen", len(D2["names"]), "Punkte", len(V2), "gleich Haupt:", len(V2) == len(V))
    if R:
        RW = lese(os.path.join(R, "deer_walk.txt"))
        maxd = 0
        for i, nm in enumerate(D2["names"]):
            if nm in RW["idx"] and not np.allclose(RW["off"][RW["idx"][nm]], np.eye(4)) and not np.allclose(D2["off"][i], np.eye(4)):
                maxd = max(maxd, np.abs(RW["off"][RW["idx"][nm]] - D2["off"][i]).max())
        print("  Offset gegen Reh (Knochen mit Haut beim Reh): max Abweichung %.6f" % maxd)
        used = sorted(set(V2[:, 7:11][V2[:, 3:7] > 0].astype(int).ravel()))
        print("  benutzte Knochen", [D2["names"][u] for u in used])
        fehlt = [D2["names"][u] for u in used if D2["names"][u] not in RW["idx"]]
        print("  benutzte Knochen, die das Reh nicht hat:", fehlt or "keiner")
        E2 = kanten(D2["el"])
        L2 = np.linalg.norm(V2[E2[:, 0], :3] - V2[E2[:, 1], :3], axis=1)
        E2 = E2[L2 > 0.004]
        L2 = L2[L2 > 0.004]
        for f in ("deer_walk.txt", "deer_run.txt", "deer_idle.txt", "deer_death.txt", "deer_dead.txt"):
            p = os.path.join(R, f)
            if not os.path.exists(p):
                continue
            RD = lese(p)
            for cn, c in RD["clips"].items():
                bb = []
                smax = 0
                s99 = 0
                ymin = 9
                for fr in range(len(c["T"])):
                    M = np.tile(np.eye(4), (len(D2["names"]), 1, 1))
                    for i, nm in enumerate(D2["names"]):
                        if nm in RD["idx"]:
                            M[i] = c["M"][fr][RD["idx"][nm]]
                    P = skin(M, D2["off"], V2)
                    bb.append((P.min(0), P.max(0)))
                    Ln = np.linalg.norm(P[E2[:, 0]] - P[E2[:, 1]], axis=1) / np.maximum(L2, 1e-6)
                    smax = max(smax, Ln.max())
                    s99 = max(s99, np.percentile(Ln, 99.5))
                    ymin = min(ymin, P[:, 1].min())
                lo = np.min([b[0] for b in bb], 0)
                hi = np.max([b[1] for b in bb], 0)
                print("  Reh-Clip %-16s gehaeutet %s .. %s, Bild 0 %s..%s, Dehnung max %.2f 99,5%% %.2f, tiefster y %.3f"
                      % (cn, lo, hi, bb[0][0], bb[0][1], smax, s99, ymin))
