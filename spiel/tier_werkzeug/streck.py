# schlimmste Kanten je Clip und Bild, in Tier-Metern (x vorn, y links, z oben)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dumpread import lese
from tier_pruef_lib import skin, kanten
import numpy as np
D = lese(sys.argv[1]); clip = sys.argv[2]; fr = int(sys.argv[3]); n = int(sys.argv[4]) if len(sys.argv) > 4 else 25
V = D["verts"]; E = kanten(D["el"]); rest = V[:, :3]
L0 = np.linalg.norm(rest[E[:, 0]] - rest[E[:, 1]], axis=1); E = E[L0 > 0.004]; L0 = L0[L0 > 0.004]
P = skin(D["clips"][clip]["M"][fr], D["off"], V)
r = np.linalg.norm(P[E[:, 0]] - P[E[:, 1]], axis=1) / L0
o = np.argsort(-r)
def tier(p): return np.round(np.array((-p[2], p[0], p[1])) / 0.544, 3)
def gw(i):
    w = V[i, 3:7]; b = V[i, 7:11].astype(int); s = np.argsort(-w)
    return " ".join("%s:%.2f" % (D["names"][b[k]].replace("Bip01_", ""), w[k]) for k in s if w[k] > 0.02)
print("Perzentile Dehnung 50/90/99/99.9:", np.round(np.percentile(r, [50, 90, 99, 99.9]), 2), "Stauchung 1%:", np.round(np.percentile(r, 1), 2))
for k in o[:n]:
    a, b = E[k]
    print("%.2f  %s  [%s]  |  %s [%s]" % (r[k], tier(rest[a]), gw(a), tier(rest[b]), gw(b)))
