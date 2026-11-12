# Lauf baer-gen-junges-v2 (12.11.2026), Bauer BEINE: Skelett-Ruhe des Generator-Jungen mit KURZEN Beinen (PLAN.md 4.1).
# Neu (Vorbild baer_skelett_rig.py, nur Format und Rechenweg uebernommen). Ruhe-DREHUNGEN bleiben byte-gleich mit dem 2c (Knoten von
# quelle/2c/NCBear.glb); neu sind nur die Gelenk-LAGEN:
#   - Rumpf, Becken, Wirbel, Hals, Kopf, Kiefer, Schwanz, Schulterblatt: dz = -(1 - f) x (Huefte - Sprunggelenk) = -0,1652 m
#   - Huefte |y| +2,0 cm, Schulter |y| +1,8 cm (breitere Spur), Schulterblatt quer im selben Verhaeltnis
#   - Oberschenkel/Unterschenkel x f_h, Oberarm/Unterarm x f_v (Richtung wie heute) -> Sprung-/Handgelenk bleibt 0,100 / 0,097 ueber dem Boden
#   - Toe0 = Abrollpunkt der neuen Pfote (Toe0 des Standard-Jungen relativ zu seinem Sprunggelenk, Hoehe ueber der Sohle wie dort)
# lage_E (lokale Lagen, Dump-Raum E) aus den Weltlagen ueber die unveraenderten Ruhe-Drehungen (Probe FK < 1e-9 E).
# Aufruf: python baer_skelett_gj2.py AUS_SKELETT.json
# Rahmen tier-Meter (x vorn, y links, z oben, Boden z 0) im Skelettrahmen; Dump-Raum = (y, z, -x) x 0,544. Statisch, nicht gespielt.
import json
import pickle
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_export_gj2 as X  # noqa: E402

Q = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/quelle/"
F_H = 0.72          # Hinterbein: Oberschenkel + Unterschenkel
DY_H = 0.020        # Huefte quer nach aussen
DY_V = 0.018        # Schulter quer nach aussen


def main(aus):
    sk = json.load(open(Q + "gen/skelett_rig.json"))
    names, par = sk["namen"], sk["eltern"]
    nb = len(names)
    alt = {n: np.array(sk["ruhe_m"][n], float) for n in names}
    # Absenkung aus dem Hinterbein: Huefte z 0,690 -> Sprunggelenk z 0,100 bleibt, Kette x F_H
    hz, az = alt["Bip01_L_Thigh"][2], alt["Bip01_L_Foot"][2]
    dz = -(1.0 - F_H) * (hz - az)
    # Vorderbein: Faktor so, dass das Handgelenk auf seiner Hoehe bleibt, wenn die Schulter um dz sinkt
    sz, hdz = alt["Bip01_L_UpperArm"][2], alt["Bip01_L_Hand"][2]
    F_V = (sz + dz - hdz) / (sz - hdz)
    neu = {}
    for n in names:
        neu[n] = alt[n].copy()
        if n not in ("Dummy01", "Translation_Data"):
            neu[n][2] += dz
    for s, sg in (("L", 1.0), ("R", -1.0)):
        h, k, f, t = ("Bip01_%s_%s" % (s, x) for x in ("Thigh", "Calf", "Foot", "Toe0"))
        neu[h] = alt[h] + np.array((0.0, sg * DY_H, dz))
        neu[k] = neu[h] + F_H * (alt[k] - alt[h])
        neu[f] = neu[k] + F_H * (alt[f] - alt[k])
        u, fa, ha, cl = ("Bip01_%s_%s" % (s, x) for x in ("UpperArm", "Forearm", "Hand", "Clavicle"))
        neu[u] = alt[u] + np.array((0.0, sg * DY_V, dz))
        neu[fa] = neu[u] + F_V * (alt[fa] - alt[u])
        neu[ha] = neu[fa] + F_V * (alt[ha] - alt[fa])
        q = neu[u][1] / alt[u][1]
        neu[cl] = np.array((alt[cl][0], alt[cl][1] * q, alt[cl][2] + dz))
        neu[t] = None
    # Toe0 aus der neuen Pfote: Standard-Junges (Dump d9931d32, Ruhe aus OFFSET)
    sys.path.insert(0, "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/gegen/werkzeug")
    import g_lib as g
    std = g.lies("C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/plan/dump/std.txt")
    js = {n: g.tier(np.linalg.inv(std["off"][std["idx"][n]])[:3, 3]) for n in std["names"]}
    for s in "LR":
        f, t = "Bip01_%s_Foot" % s, "Bip01_%s_Toe0" % s
        d = js[t] - js[f]
        neu[t] = np.array((neu[f][0] + d[0], neu[f][1] + d[1], js[t][2]))
    # lage_E: Weltlagen (Dump) ueber die festen Ruhe-Drehungen in lokale Lagen
    J, _B = X.lade_json_glb()
    nodes = {n["name"]: n for n in J["nodes"]}
    R_loc = np.zeros((nb, 3, 3))
    for b, nm in enumerate(names):
        R_loc[b] = X.FZ @ X.quat_m(nodes[nm].get("rotation", [0, 0, 0, 1])) @ X.FZ
    Rw = np.zeros((nb, 3, 3))
    for b in range(nb):
        Rw[b] = R_loc[b] if par[b] < 0 else Rw[par[b]] @ R_loc[b]
    lage = {}
    pd = {n: X.dump(neu[n]) for n in names}
    for b, nm in enumerate(names):
        if par[b] < 0:
            lage[nm] = pd[nm]
        else:
            lage[nm] = np.linalg.solve(Rw[par[b]], pd[nm] - pd[names[par[b]]])
    # Wurzeln wie heute (Dummy01/Translation_Data 0; Bip01 nur z)
    for nm in ("Dummy01", "Translation_Data"):
        assert np.abs(lage[nm]).max() < 1e-12 or nm == "Translation_Data"
    # Probe FK
    W = np.zeros((nb, 4, 4))
    for b, nm in enumerate(names):
        T = np.eye(4)
        T[:3, :3] = R_loc[b]
        T[:3, 3] = lage[nm]
        W[b] = T if par[b] < 0 else W[par[b]] @ T
    fk = max(float(np.abs(W[b][:3, 3] - pd[nm]).max()) for b, nm in enumerate(names))
    assert fk < 1e-9, fk
    out = dict(sk)
    out["lage_E"] = {nm: [float(v) if abs(v) > 1e-15 else 0.0 for v in lage[nm]] for nm in names}
    out["ruhe_m"] = {nm: [float(v) for v in neu[nm]] for nm in names}
    # Probe nach dem Schreiben (volle Stellen)
    W2 = np.zeros((nb, 4, 4))
    for b, nm in enumerate(names):
        T = np.eye(4)
        T[:3, :3] = R_loc[b]
        T[:3, 3] = out["lage_E"][nm]
        W2[b] = T if par[b] < 0 else W2[par[b]] @ T
    fk2 = max(float(np.abs(W2[b][:3, 3] - X.dump(np.array(out["ruhe_m"][nm]))).max()) for b, nm in enumerate(names))
    out["ruhe_m_alt"] = sk["ruhe_m"]
    out["lage_E_alt"] = sk["lage_E"]
    out["faktoren"] = dict(sk["faktoren"], beine_hinten=F_H, beine_vorn=round(F_V, 6), dz_rumpf_m=round(dz, 6), dy_huefte_m=DY_H,
                           dy_schulter_m=DY_V)
    out["dx_m"] = sk["dx_m"]       # Huefte x unveraendert -> D.2-Versatz gleich; die Becken-Regel des Exports wird nicht benutzt (alle 15 Clips neu)
    out["gj2"] = dict(lauf="baer-gen-junges-v2", rolle="BEINE", fk_probe_E=fk, fk_probe_gerundet_E=fk2,
                      toe0_quelle="Standard-Junges d9931d32: Toe0 - Foot (x, y), Toe0-Hoehe wie dort",
                      hinweis="gelenke_im_netz, beinachsen, sp_rig, splitter_tausch sind die ALTEN Werte (Generator heute); neu misst BEINE.md")
    json.dump(out, open(aus, "w"), indent=1)
    print("SKELETT dz %.4f m, F_H %.4f, F_V %.5f, FK %.1e E (gerundet %.1e E)" % (dz, F_H, F_V, fk, fk2))
    for nm in ("Bip01", "Bip01_Pelvis", "Bip01_L_Thigh", "Bip01_L_Calf", "Bip01_L_Foot", "Bip01_L_Toe0", "Bip01_L_Clavicle",
               "Bip01_L_UpperArm", "Bip01_L_Forearm", "Bip01_L_Hand", "Bip01_Head", "Bip01_Jaw"):
        print("  %-18s alt %s -> neu %s" % (nm, np.round(alt[nm], 4).tolist(), np.round(out["ruhe_m"][nm], 5).tolist()))


if __name__ == "__main__":
    main(sys.argv[1])
