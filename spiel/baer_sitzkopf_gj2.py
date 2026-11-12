# Lauf baer-gen-junges-v2 (12.11.2026), Bauer GESICHT: Kopf im Sitzen nicken (PLAN 4.5.2.4: Augen-Nase-Linie im Sitzen -36..-26 Grad
# "mit dem gehobenen Kopf aus 5.1"). Neu. baer_umrechnen_gj2.py (BEINE, nur aufgerufen) laesst den Kopf im Sitzen seine Weltneigung
# halten; mit dem um 8 Grad gehobenen und vorn gestreckten Kopf stand die Linie im Sitzen bei -21 Grad (Blick nach oben).
# Hier: nur die lokale Drehung von Bip01_Head wird um den Kopf-eigenen Querachse genickt (R_loc = R_loc . B^-1 . A^T ry(w.GRAD) A . B,
# B = Ruhe-Weltdrehung des Kopfes; Drehpunkt = Kopfgelenk, Kiefer folgt), Gewicht w je Bild: SitDown 0 -> 1 (smoothstep ueber den
# Clip, Bild 48 = 1), Sit = 1, StandUp 1 -> 0 (Bild 39 = 0). Damit aendern sich die Nahtstellen SitDown 48 / Sit 0 / StandUp 0 /
# Sit 120 nicht (dort w = 1, gleiche Rechnung) und SitDown 0 / StandUp 39 = Haltung wie vorher. Andere Clips und Becken unveraendert.
# Aufruf: python baer_sitzkopf_gj2.py SKELETT.json CLIPS_EIN.npz CLIPS_AUS.npz [grad=7]
# Statisch/offline, deterministisch, nicht gespielt.
import json
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_umrechnen_gj2 as U  # noqa: E402


def nicken(skp, ein, aus, grad=7.0):
    G = U.Gerippe(skp)
    ih = G.idx["Bip01_Head"]
    B = G.BWr[ih]
    Rn = np.linalg.inv(B) @ U.A_TD.T @ U.ry(grad) @ U.A_TD @ B
    Z = dict(np.load(ein))
    info = {"grad": grad}
    for c in U.SITZ:
        R = Z[c + "_R"].copy()
        n = len(R)
        if c == "NCBear_SitDown":
            w = U.sst(0.0, n - 1.0, np.arange(n))
        elif c == "NCBear_StandUp":
            w = 1.0 - U.sst(0.0, n - 1.0, np.arange(n))
        else:
            w = np.ones(n)
        for f in range(n):
            if w[f] <= 0.0:
                continue
            Rf = Rn if w[f] >= 1.0 else (np.linalg.inv(B) @ U.A_TD.T @ U.ry(grad * float(w[f])) @ U.A_TD @ B)
            R[f, ih] = R[f, ih] @ Rf
        Z[c + "_R"] = R
        info[c] = dict(bilder=n, w_erst=float(w[0]), w_letzt=float(w[-1]))
    # Nahtstellen SitDown 48 / Sit 0 / StandUp 0 / Sit 120: groesste Abweichung der lokalen Drehungen vorher und nachher (der Eingang
    # von baer_umrechnen_gj2.py ist dort schon nicht ganz bitgleich; das Nicken aendert die Abweichung nicht, weil w dort 1 ist)
    Z0 = np.load(ein)
    for nm, ZZ in (("vorher", Z0), ("nachher", Z)):
        a, b, s = ZZ["NCBear_SitDown_R"], ZZ["NCBear_StandUp_R"], ZZ["NCBear_Sit_R"]
        info["naht_" + nm] = dict(sitdown48_sit0=float(np.abs(a[-1] - s[0]).max()), standup0_sit0=float(np.abs(b[0] - s[0]).max()),
                                  sit120_sit0=float(np.abs(s[-1] - s[0]).max()))
    np.savez(aus, **Z)
    print("SITZKOPF", json.dumps(info))
    return info


if __name__ == "__main__":
    kv = dict(x.split("=", 1) for x in sys.argv[4:])
    nicken(sys.argv[1], sys.argv[2], sys.argv[3], float(kv.get("grad", 7.0)))
