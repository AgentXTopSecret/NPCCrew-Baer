# Lauf baer-gen-junges-v2 (12.11.2026), Bauer GESICHT: Kopf-Form des Generator-Jungen (PLAN.md 5.1). Neu.
# Nur Punkte werden verschoben -- Topologie, UV, Gewichte bleiben (Netz-Felder wie beine/netz_gj2.npz, nur V neu).
# Reihenfolge (alle Masse in tier-Metern, Ruhe, Skelettrahmen):
#   1. Kopf gesamt x KOPF um das Head-Gelenk, Faktor mit dem Head(+Jaw)-Gewicht wk gemischt (Hals uebernimmt den Rest).
#   2. Schnauze: Gewicht ws = smoothstep(Augenebene - 4 cm .. + 2 cm) x (1 - smoothstep(Augenhoehe .. + 6 cm)) x wk, dazu quer ein
#      weicher Abfall ausserhalb der Schnauzen-Halbbreite (sonst blaehen die Wangen an der Augenebene); skaliert um den Punkt
#      (Augenebene, Mitte, 5 cm unter Augenhoehe) vorn SX, quer SY, hoch SZ (Abstaende x KOPF).
#   2b. (Nachbesserung 12.11., PRUEF_OPTIK M1: Schnauze nur 55 % der Flaeche / 75 % der Breite des Standard-Jungen, "Knopf" mit Delle zur
#      Wange) Schnauzen-WURZEL quer breiter: Gewicht wb = smoothstep(Augenebene - wz_hinten .. + wz_vorn) x (1 - smoothstep(Augenhoehe
#      - wz_oben0 .. - wz_oben1)) x quer-Abfall (wz_halb .. + wz_halb_weich) x wk; quer skaliert um y = 0 mit 1 + wz_quer. Die Augen (auf
#      Augenhoehe) bleiben stehen; Wange und Schnauzen-Wurzel fuellen den Uebergang (statt Delle), die Schnauze wird unten breit und kastig.
#   3. Ohren (vor dem Heben, im Kopfrahmen): je Ohr um die Mitte seines Ansatzrings gieren (Oeffnung nach aussen), nach hinten
#      kippen und um ohr_heben anheben; Ohr-Gewicht we = smoothstep ueber den geodaetischen Abstand zum Ansatzring (ohr_innen 5 cm ins
#      Ohr, ohr_aussen 3 cm in den Kopf); danach das Verschiebungsfeld im Ohr-Band harmonisch geglaettet (Drehung ueber die Basis verteilt).
#   4. Heben um das Head-Gelenk (Winkel x wk).
#   5. Glatte Uebergaenge: Verschiebungsfeld im Band (0 < w < 1 von wk/ws/we, + 1 Ring) Jacobi-geglaettet bei festem Rand
#      (die Oberflaechen-Form bleibt, nur der Uebergang wird weich).
# Messung je Schritt (Augenabstand, Auge->Nase, Augen-Nase-Linie, Kopfbreite mit Ohren) und am Ende Verzerrung (sigma1/sigma2 je
# Dreieck alt -> neu, je Band), umgeklappte Dreiecke, Oeffnungsrichtung der Ohrmuscheln. (Kopf-in-Koerper je Clip prueft
# gesicht/werkzeug/kopf_wirt_alle.py am Importer-Dump.) Ausgabe zusaetzlich: w_kopf, w_schnauze, w_ohr, V_vor_kopf (fuer die Textur).
# Aufruf: python baer_kopf_gj2.py NETZ_GJ2.npz GEWICHTE.npz SKELETT.json AUS_NETZ.npz AUS_INFO.json [k=v,...]
# Statisch/offline, deterministisch (keine Zufallszahlen), nicht gespielt.
import json
import math
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/rig/gegen/werkzeug")
import baer_umrechnen_gj2 as U  # noqa: E402

# Gewaehlt nach den Proben (gesicht/test, Bericht GESICHT.md 2): Kopf x1,12 und Schnauze 1,45/1,35/1,25 (Plan-Obergrenzen) -- mit 1,10 und
# 1,40/1,30/1,20 blieb das Gesicht aus Kevins Kamera bei 0,032 m2 / 5,5 % (Soll >= 0,035 / 6 %); Heben 8 Grad (10 Grad wuerde die
# Augen-Nase-Linie ueber -28 Grad heben). Wurzel quer 1,45 (Nachbesserung, Proben nachbesserung/probe/kopf: 0,2 / 0,3 / 0,45 -- erst 0,45
# fuellt die Delle sichtbar; Augenabstand 0,156 -> 0,168, im Plan 0,14-0,17; 0 umgeklappt). Ohren: Gier 16, Kipp 0 -- die Muschel oeffnet heute schon 26-27 Grad nach aussen -> 35-37 Grad
# (Plan 35-50); mehr Gier oder Kipp 6-12 Grad senkt das Ohr aus Kevins Kamera unter 4 px ueber dem Kopfumriss und klappt Dreiecke um.
PAR = dict(kopf=1.12, sx=1.45, sy=1.35, sz=1.25, heben=8.0, ohr_gier=16.0, ohr_kipp=0.0,
           sn_hinten=0.04, sn_vorn=0.02, sn_oben=0.06, sn_mitte_unter=0.05, sn_halb=0.085, sn_halb_weich=0.05,
           ohr_innen=0.05, ohr_aussen=0.03, ohr_heben=0.0, glatt_runden=40, ohr_glatt_runden=300,
           wz_quer=0.45, wz_hinten=0.08, wz_vorn=0.03, wz_oben0=0.05, wz_oben1=0.010, wz_halb=0.11, wz_halb_weich=0.05)
# Landmarken (Ruhe des Generator-Jungen aus plan/log/mess.json kopf_lm, Rumpf dz -0,1652 wie skelett_gj2): naechster Netzpunkt
LM_REF = {"auge_l": (0.596, 0.0643, 0.7893), "auge_r": (0.5982, -0.0613, 0.7873), "nasenspitze": (0.6873, -0.0004, 0.7047),
          "kinn": (0.6138, 0.0037, 0.6328), "krone": (0.2849, 0.0007, 1.0379), "ohr_l": (0.4277, 0.1529, 1.0885),
          "ohr_r": (0.4268, -0.1417, 1.0884)}
sst = U.sst


def kanten(T):
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]))
    return np.unique(np.sort(E, 1), axis=0)


def geo_abstand(V, E, quelle, runden=400):
    """geodaetischer Abstand (ueber Kanten) zur Punktmenge quelle (bool)"""
    L = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1)
    d = np.where(quelle, 0.0, np.inf)
    for _ in range(runden):
        d2 = d.copy()
        np.minimum.at(d2, E[:, 0], d[E[:, 1]] + L)
        np.minimum.at(d2, E[:, 1], d[E[:, 0]] + L)
        if np.array_equal(d2, d):
            break
        d = d2
    return d


def ry(a):   # Drehung um y (tier): +a hebt vorn (x -> z)
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])


def rz(a):   # Drehung um z: +a dreht x -> y
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def dreh_gemischt(P, piv, achse, winkel):
    """jeder Punkt um piv mit eigenem Winkel (Feld) um die Achse 'y' oder 'z' gedreht"""
    d = P - piv
    c, s = np.cos(winkel), np.sin(winkel)
    out = P.copy()
    if achse == "y":
        out[:, 0] = piv[0] + c * d[:, 0] - s * d[:, 2]
        out[:, 2] = piv[2] + s * d[:, 0] + c * d[:, 2]
    else:
        out[:, 0] = piv[0] + c * d[:, 0] - s * d[:, 1]
        out[:, 1] = piv[1] + s * d[:, 0] + c * d[:, 1]
    return out


def normalen(P, T):
    fn = np.cross(P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]])
    acc = np.zeros_like(P)
    for k in range(3):
        np.add.at(acc, T[:, k], fn)
    return acc / np.maximum(np.linalg.norm(acc, axis=1, keepdims=True), 1e-12)


def verzerrung(V0, V1, T):
    """sigma1, sigma2 der Abbildung Dreieck alt -> neu (in der Ebene), umgeklappt (Normale gedreht > 90 Grad)"""
    e1, e2 = V0[T[:, 1]] - V0[T[:, 0]], V0[T[:, 2]] - V0[T[:, 0]]
    n0 = np.cross(e1, e2)
    a0 = np.linalg.norm(n0, axis=1)
    uu = e1 / np.maximum(np.linalg.norm(e1, axis=1, keepdims=True), 1e-12)
    nn = n0 / np.maximum(a0[:, None], 1e-12)
    vv = np.cross(nn, uu)
    Rm = np.stack((np.stack(((e1 * uu).sum(1), (e2 * uu).sum(1)), 1), np.stack(((e1 * vv).sum(1), (e2 * vv).sum(1)), 1)), 1)
    ok = a0 > 1e-10
    RI = np.zeros_like(Rm)
    RI[ok] = np.linalg.inv(Rm[ok])
    f1, f2 = V1[T[:, 1]] - V1[T[:, 0]], V1[T[:, 2]] - V1[T[:, 0]]
    F = np.einsum("tij,tjk->tik", np.stack((f1, f2), 2), RI)
    S = np.linalg.svd(F, compute_uv=False)
    n1 = np.cross(f1, f2)
    um = (n1 * n0).sum(1) < 0
    return S[:, 0], np.maximum(S[:, 1], 1e-12), um, ok


def landmarken(V):
    return {k: int(np.argmin(np.linalg.norm(V - np.array(p), axis=1))) for k, p in LM_REF.items()}


def kopf_zahlen(V, lm, kopf_ohr):
    al, ar, na = V[lm["auge_l"]], V[lm["auge_r"]], V[lm["nasenspitze"]]
    am = 0.5 * (al + ar)
    v = na - am
    return dict(augenabstand=round(float(np.linalg.norm(al - ar)), 4), auge_nase_m=round(float(np.linalg.norm(v)), 4),
                auge_nase_grad=round(math.degrees(math.atan2(v[2], v[0])), 1),
                kopfbreite_mit_ohren=round(float(np.ptp(V[kopf_ohr, 1])), 4), kopf_hoehe_oben=round(float(V[kopf_ohr, 2].max()), 4),
                nase=[round(float(x), 4) for x in na], kinn_z=round(float(V[lm["kinn"], 2]), 4))


def baue(netz, gew, skp, aus, info_aus, kv=""):
    P = dict(PAR)
    if kv:
        for k_v in kv.split(","):
            k, v = k_v.split("=")
            P[k] = float(v)
    N = np.load(netz)
    G = U.Gerippe(skp, netz, gew)
    V0 = N["V"].astype(float)
    T = N["T"]
    E = kanten(T)
    W = G.W
    wk = np.clip(W[:, G.idx["Bip01_Head"]] + W[:, G.idx["Bip01_Jaw"]], 0.0, 1.0)
    H = G.J["Bip01_Head"].copy()
    lm = landmarken(V0)
    kopf_ohr = N["kopf"] | N["ohr_l"] | N["ohr_r"]
    info = dict(par=P, landmarken=lm, head_gelenk=[round(float(x), 4) for x in H], schritte={})
    info["schritte"]["0_vorher"] = kopf_zahlen(V0, lm, kopf_ohr)
    ks = P["kopf"]
    # ---- 1. Kopf gesamt
    V1 = V0 + (ks - 1.0) * wk[:, None] * (V0 - H)
    info["schritte"]["1_kopf_x%.2f" % ks] = kopf_zahlen(V1, lm, kopf_ohr)
    # ---- 2. Schnauze
    am = 0.5 * (V1[lm["auge_l"]] + V1[lm["auge_r"]])
    ax, az = float(am[0]), float(am[2])
    x, y, z = V1[:, 0], V1[:, 1], V1[:, 2]
    ws = sst(ax - P["sn_hinten"] * ks, ax + P["sn_vorn"] * ks, x) * (1.0 - sst(az, az + P["sn_oben"] * ks, z)) * wk
    ws *= 1.0 - sst(P["sn_halb"] * ks, (P["sn_halb"] + P["sn_halb_weich"]) * ks, np.abs(y))
    c0 = np.array([ax, 0.0, az - P["sn_mitte_unter"] * ks])
    S = np.array([P["sx"], P["sy"], P["sz"]]) - 1.0
    V2 = V1 + ws[:, None] * (V1 - c0) * S[None, :]
    info["schritte"]["2_schnauze"] = kopf_zahlen(V2, lm, kopf_ohr)
    info["schnauze_punkte"] = dict(voll=int((ws > 0.99).sum()), band=int(((ws > 0.01) & (ws < 0.99)).sum()))
    # ---- 2b. Schnauzen-Wurzel quer breiter (Nachbesserung 12.11.); Augenhoehe ausgenommen
    wb = np.zeros(len(V0))
    if P["wz_quer"] > 0:
        x2, z2 = V2[:, 0], V2[:, 2]
        wb = (sst(ax - P["wz_hinten"] * ks, ax + P["wz_vorn"] * ks, x2) * (1.0 - sst(az - P["wz_oben0"] * ks, az - P["wz_oben1"] * ks, z2))
              * (1.0 - sst(P["wz_halb"] * ks, (P["wz_halb"] + P["wz_halb_weich"]) * ks, np.abs(V2[:, 1]))) * wk)
        V2 = V2.copy()
        V2[:, 1] = V2[:, 1] * (1.0 + P["wz_quer"] * wb)
        info["schritte"]["2b_wurzel"] = kopf_zahlen(V2, lm, kopf_ohr)
        info["wurzel_punkte"] = dict(voll=int((wb > 0.99).sum()), band=int(((wb > 0.01) & (wb < 0.99)).sum()))
    # ---- 3. Ohren
    V3 = V2.copy()
    we_ges = np.zeros(len(V0))
    ohr_info = {}
    for o, sg in (("ohr_l", 1.0), ("ohr_r", -1.0)):
        m = N[o].astype(bool)
        aussen = np.zeros(len(V0), bool)
        mm = m[E[:, 0]] != m[E[:, 1]]
        aussen[E[mm][~m[E[mm, 0]], 0]] = True
        aussen[E[mm][~m[E[mm, 1]], 1]] = True
        innen = np.zeros(len(V0), bool)
        innen[E[mm][m[E[mm, 0]], 0]] = True
        innen[E[mm][m[E[mm, 1]], 1]] = True
        piv = 0.5 * (V2[aussen].mean(0) + V2[innen].mean(0))
        d_in = geo_abstand(V2, E, ~m)          # fuer Ohrpunkte: Abstand zum Kopf
        d_out = geo_abstand(V2, E, m)          # fuer Kopfpunkte: Abstand zum Ohr
        s = np.where(m, d_in, -d_out)
        we = sst(-P["ohr_aussen"], P["ohr_innen"], s) * (wk > 0.99)
        Q = dreh_gemischt(V3, piv, "z", sg * math.radians(P["ohr_gier"]) * we)
        Q = dreh_gemischt(Q, piv, "y", math.radians(P["ohr_kipp"]) * we)   # + = Oberkante nach hinten (-x)
        Q = Q + np.array([0.0, 0.0, P["ohr_heben"]])[None, :] * we[:, None]   # Ohr etwas hoeher auf den Kopf (Foto C: Ohren oben)
        V3 = np.where(we[:, None] > 0, Q, V3)
        we_ges = np.maximum(we_ges, we)
        ohr_info[o] = dict(drehpunkt=[round(float(v), 4) for v in piv], punkte_voll=int((we > 0.99).sum()),
                           band=int(((we > 0.01) & (we < 0.99)).sum()))
    info["ohren"] = ohr_info
    info["schritte"]["3_ohren"] = kopf_zahlen(V3, lm, kopf_ohr)
    # ---- 4. Heben
    V4 = dreh_gemischt(V3, H, "y", math.radians(P["heben"]) * wk)
    info["schritte"]["4_heben_%g" % P["heben"]] = kopf_zahlen(V4, lm, kopf_ohr)
    # ---- 5. Uebergaenge glaetten (Verschiebungsfeld)
    band = ((wk > 0.01) & (wk < 0.99)) | ((ws > 0.01) & (ws < 0.99)) | ((we_ges > 0.01) & (we_ges < 0.99)) | ((wb > 0.01) & (wb < 0.99))
    b2 = band.copy()
    b2[E[band[E[:, 0]], 1]] = True
    b2[E[band[E[:, 1]], 0]] = True
    band = b2
    d = V4 - V0
    for _ in range(int(P["glatt_runden"])):
        acc = np.zeros_like(d)
        cnt = np.zeros(len(d))
        np.add.at(acc, E[:, 0], d[E[:, 1]])
        np.add.at(acc, E[:, 1], d[E[:, 0]])
        np.add.at(cnt, E[:, 0], 1)
        np.add.at(cnt, E[:, 1], 1)
        d = np.where(band[:, None], 0.5 * d + 0.5 * acc / cnt[:, None], d)
    # Ohr-Band zusaetzlich bis zur harmonischen Loesung glaetten (Drehung ueber die ganze Ohrbasis verteilt, fester Rand)
    ob = (we_ges > 0.01) & (we_ges < 0.99)
    for _ in range(int(P["ohr_glatt_runden"])):
        acc = np.zeros_like(d)
        cnt = np.zeros(len(d))
        np.add.at(acc, E[:, 0], d[E[:, 1]])
        np.add.at(acc, E[:, 1], d[E[:, 0]])
        np.add.at(cnt, E[:, 0], 1)
        np.add.at(cnt, E[:, 1], 1)
        d = np.where(ob[:, None], acc / cnt[:, None], d)
    V5 = V0 + d
    info["schritte"]["5_glatt"] = kopf_zahlen(V5, lm, kopf_ohr)
    info["band_punkte"] = int(band.sum())
    # ---- Pruefen: Verzerrung, umgeklappt
    s1, s2, um, ok = verzerrung(V0, V5, T)
    tb = band[T].any(1) & ok
    r = s1 / s2
    info["verzerrung"] = dict(band_p99=round(float(np.percentile(r[tb], 99)), 3), band_max=round(float(r[tb].max()), 3),
                              kopf_p99=round(float(np.percentile(r[kopf_ohr[T].any(1) & ok], 99)), 3),
                              flaeche_kopf_median=round(float(np.median((s1 * s2)[kopf_ohr[T].all(1) & ok])), 3),
                              umgeklappt=int(um.sum()), dreiecke_band=int(tb.sum()))
    ohr_t = (ob | N["ohr_l"] | N["ohr_r"])[T].any(1)
    for nm, mm in (("band_hals_wangen", tb & ~ohr_t), ("band_ohr", ohr_t & ok)):
        info["verzerrung"][nm + "_p99"] = round(float(np.percentile(r[mm], 99)), 3)
        info["verzerrung"][nm + "_max"] = round(float(r[mm].max()), 3)
        info["verzerrung"][nm + "_dreiecke"] = int(mm.sum())
    info["ohr_oeffnung"] = {}
    for o, sg in (("ohr_l", 1.0), ("ohr_r", -1.0)):
        tm = N[o][T].all(1)
        n0 = np.cross(V0[T[:, 1]] - V0[T[:, 0]], V0[T[:, 2]] - V0[T[:, 0]])[tm]
        vorn = n0[:, 0] / np.linalg.norm(n0, axis=1) > 0.2       # Vorderseite der Muschel im Ausgangsnetz
        res = {}
        for nm, VV, hb in (("vorher", V0, 0.0), ("nachher", V5, P["heben"])):
            n1 = np.cross(VV[T[:, 1]] - VV[T[:, 0]], VV[T[:, 2]] - VV[T[:, 0]])[tm][vorn].sum(0)
            n1 = ry(-math.radians(hb)) @ (n1 / np.linalg.norm(n1))  # im Kopfrahmen (Heben herausgerechnet)
            res[nm] = dict(gier_aussen_grad=round(math.degrees(math.atan2(sg * n1[1], n1[0])), 1),
                           neigung_oben_grad=round(math.degrees(math.asin(n1[2])), 1))
        info["ohr_oeffnung"][o] = res
    info["bewegt_max_cm"] = round(100 * float(np.linalg.norm(V5 - V0, axis=1).max()), 2)
    info["rumpf_bewegt_max_cm"] = round(100 * float(np.linalg.norm((V5 - V0)[(wk < 0.001) & ~band], axis=1).max()), 4)
    out = {k: N[k] for k in N.files}
    out["V"] = V5
    out["w_kopf"] = wk
    out["w_schnauze"] = ws
    out["w_wurzel"] = wb
    out["w_ohr"] = we_ges
    out["V_vor_kopf"] = V0
    out["info_kopf"] = np.array(json.dumps(info))
    np.savez(aus, **out)
    json.dump(info, open(info_aus, "w"), indent=1)
    for k, v in info["schritte"].items():
        print("KOPF", k, json.dumps(v))
    print("KOPF ohr_oeffnung", json.dumps(info["ohr_oeffnung"]))
    print("KOPF verzerrung", json.dumps(info["verzerrung"]), "band", info["band_punkte"], "bewegt max cm", info["bewegt_max_cm"],
          "rumpf", info["rumpf_bewegt_max_cm"])
    return info


if __name__ == "__main__":
    baue(*sys.argv[1:6], kv=sys.argv[6] if len(sys.argv) > 6 else "")
