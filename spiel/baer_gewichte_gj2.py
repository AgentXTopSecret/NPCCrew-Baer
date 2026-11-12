# Lauf baer-gen-junges-v2 (12.11.2026), Bauer BEINE: Hautgewichte des Generator-Jungen mit kurzen Beinen und Std-Pfoten (PLAN.md 4.4).
# Neu; Messung "dehnung" wie baer_gewichte_rig.dehnung (Original unveraendert: gleiche Formel sigma1 der Dreiecks-Abbildung Ruhe ->
# Bild, gleiche Filter fuer kleine/entartete Dreiecke, Achsel/Brust aus den Regionen), hier mit dem numpy-Gerippe (= Importer, geprueft)
# oder einem Importer-Dump.
#   start  : Startgewichte (Gen-Endgewichte durch die Raum-Abbildung mitgenommen, Std-Pfoten-Gewichte, Schnitt-Ringe interpoliert) ->
#            Pfoten unter dem Gelenk starr (Hand/Fuss 1,0, weich ueber 4 cm), Krallen 1,0, Kopf/Ohren wie heute (starr), Toe0 ohne Gewicht,
#            Naht-Band und Ringnaehe (Gen 6 cm ueber, Std 3 cm unter dem Band) Laplace-geglaettet bei festem Rand, Innenbein: Rumpf-Gewicht
#            unter z 0,22 (neu) auf das Bein (der heutige Optimierer hatte es fuer die LANGEN Beine bis z 0,26 alt gelegt),
#            hoechstens 4 Einfluesse (wie der Export), Summe 1
#   dehnung: je Clip p99,5 / max sigma1, Achsel/Brust max, Region des Maximums
# Aufruf: python baer_gewichte_gj2.py start NETZ_GJ2.npz GEW_START.npz SKELETT.json AUS_GEW.npz
#         python baer_gewichte_gj2.py dehnung NETZ_GJ2.npz GEW.npz SKELETT.json CLIPS.npz [AUS.json]
#         python baer_gewichte_gj2.py opt NETZ_GJ2.npz GEW.npz SKELETT.json CLIPS.npz AUS_GEW.npz [k=v,...]   (~10 min CPU, Hintergrund)
# Statisch/offline, nicht gespielt.
import json
import sys
import time

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_umrechnen_gj2 as U  # noqa: E402

T0 = time.time()
M2U = 0.544
Q = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/quelle/"
REG_NAMEN = ["sonst", "achsel", "brust", "leiste", "hals", "kopf", "ohr", "pfote", "kralle", "stummel", "bauch"]


def log(*a):
    print("GEW", round(time.time() - T0, 1), *a, flush=True)


sst = U.sst


def kanten(T, n):
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]))
    E = np.unique(np.sort(E, 1), axis=0)
    return E


def laplace(W, E, frei, runden=60, lam=0.5):
    n = len(W)
    deg = np.bincount(E[:, 0], minlength=n) + np.bincount(E[:, 1], minlength=n)
    for _ in range(runden):
        acc = np.zeros_like(W)
        np.add.at(acc, E[:, 0], W[E[:, 1]])
        np.add.at(acc, E[:, 1], W[E[:, 0]])
        mit = acc / np.maximum(deg, 1)[:, None]
        W[frei] = (1 - lam) * W[frei] + lam * mit[frei]
    return W


def vier(W):
    """hoechstens 4 Einfluesse (groesste), Summe 1 -- wie baer_export_gj2 (dort < 1e-5 -> 0)."""
    o = np.argsort(-W, axis=1)[:, :4]
    W4 = np.zeros_like(W)
    r = np.arange(len(W))[:, None]
    W4[r, o] = W[r, o]
    W4[W4 < 1e-5] = 0.0
    return W4 / W4.sum(1, keepdims=True)


def regionen_neu(N):
    """Region je Dreieck: Gen-Teil ueber den Ursprungs-Punkt (Regionen der heutigen Endgewichte, je Punkt Mehrheit der alten Dreiecke),
    Std-Pfote = pfote / kralle, Band = pfote."""
    Go = np.load(Q + "gen/gewichte_end.npz")
    To, Ro = Go["T"], Go["regionen"]
    nv_alt = len(Go["V"])
    lab = np.zeros((nv_alt, len(REG_NAMEN)))
    for k in range(3):
        np.add.at(lab, (To[:, k], Ro), 1.0)
    vlab = np.argmax(lab, 1)
    q = N["quelle"]
    teil = N["teil"]
    pl = np.full(len(N["V"]), REG_NAMEN.index("pfote"))
    gen = (teil == 0) & (q >= 0) & (q < nv_alt)
    pl[gen] = vlab[q[gen]]
    # Schnittpunkte des Gen-Teils (neu entstanden) -> Bein = sonst
    pl[(teil == 0) & ~gen] = REG_NAMEN.index("sonst")
    pl[N["kralle"].astype(bool)] = REG_NAMEN.index("kralle")
    T = N["T"]
    a, b, c = pl[T[:, 0]], pl[T[:, 1]], pl[T[:, 2]]
    R = np.where(b == c, b, a)
    R[N["teil_T"] == 2] = REG_NAMEN.index("pfote")
    R[N["teil_T"] == 1] = np.where(R[N["teil_T"] == 1] == REG_NAMEN.index("kralle"), R[N["teil_T"] == 1], REG_NAMEN.index("pfote"))
    return R.astype(np.int32)


def start(netz, gew, skp, aus):
    N = np.load(netz)
    G0 = np.load(gew)
    nam = [str(n) for n in G0["namen"]]
    W = G0["W"].astype(float).copy()
    V = N["V"]
    T = N["T"]
    sk = json.load(open(skp))
    J = {n: np.array(v) for n, v in sk["ruhe_m"].items()}
    ix = {n: i for i, n in enumerate(nam)}
    teil = N["teil"]
    info = {}
    # Krallen: nur echte Krallen (krallen-artige UV UND Pfoten-Knochen dominant UND tief) -- die Std-Maske enthielt auch den Unterarm-Streifen
    kr = N["kralle"].astype(bool).copy()
    pfk = [ix[n] for n in ("Bip01_L_Hand", "Bip01_R_Hand", "Bip01_L_Foot", "Bip01_R_Foot", "Bip01_L_Toe0", "Bip01_R_Toe0")]
    kr &= (W[:, pfk].sum(1) > 0.5) & (V[:, 2] < 0.10)
    info["krallen"] = dict(maske_vorher=int(N["kralle"].sum()), krallen=int(kr.sum()))
    # Toe0 -> Foot
    for s in "LR":
        W[:, ix["Bip01_%s_Foot" % s]] += W[:, ix["Bip01_%s_Toe0" % s]]
        W[:, ix["Bip01_%s_Toe0" % s]] = 0.0
    # Naht-Band/Ringnaehe glaetten (Rand fest): Gen-Punkte bis 6 cm ueber dem Gen-Ring, Std-Punkte bis 3 cm unter dem Std-Ring
    E = kanten(T, len(V))
    zg = 0.165
    zs = 0.130
    zone = ((teil == 0) & (V[:, 2] < zg + 0.06) & (V[:, 2] > zg - 1e-6)) | ((teil == 1) & (V[:, 2] > zs - 0.03))
    zone &= ~kr
    rand = ((teil == 0) & (V[:, 2] >= zg + 0.06)) | ((teil == 1) & (V[:, 2] <= zs - 0.03))
    frei = zone & ~rand
    W = laplace(W, E, frei, runden=40)
    info["naht_glatt_punkte"] = int(frei.sum())
    # Innenbein: Rumpf-Gewicht unten auf das Bein (naechster Bein-Knochen), weich z 0,16..0,22
    torso = [ix[n] for n in nam if not any(k in n for k in ("Thigh", "Calf", "Foot", "Toe0", "UpperArm", "Forearm", "Hand"))]
    u = 1.0 - sst(0.16, 0.22, V[:, 2])
    m = (u > 0) & (W[:, torso].sum(1) > 1e-6) & (teil == 0)
    idx = np.nonzero(m)[0]
    if len(idx):
        import baer_beine_gj2 as BG
        _b, kn, _d = BG.naechster_bein_knochen(V[idx], J)
        wt = W[idx][:, torso].sum(1) * u[idx]
        W[np.ix_(idx, torso)] *= (1.0 - u[idx])[:, None]
        W[idx, [ix[k] for k in kn]] += wt
    info["innenbein_punkte"] = int(len(idx))
    # Beine an der Mittellinie aus (Brust-Kiel zwischen den Vorderbeinen, Schritt zwischen den Hinterbeinen): Bein-Anteil x
    # sst(0,005, 0,05, |y|), der Rest an den Rumpf (sonst ziehen linkes und rechtes Bein den schmalen Kiel auseinander: sigma1 bis 14)
    beinb = [ix[n] for n in nam if any(k in n for k in ("Thigh", "Calf", "Foot", "Toe0", "UpperArm", "Forearm", "Hand"))]
    fm = sst(0.005, 0.05, np.abs(V[:, 1]))
    fm[teil != 0] = 1.0
    wl = W[:, beinb].sum(1)
    W[:, beinb] *= fm[:, None]
    wt0 = W[:, torso].sum(1)
    add = wl * (1.0 - fm)
    W[:, torso] += np.where(wt0[:, None] > 1e-9, W[:, torso] / np.maximum(wt0, 1e-9)[:, None], 0.0) * add[:, None]
    nt_ = wt0 <= 1e-9
    W[nt_, ix["Bip01_Pelvis"]] += add[nt_] * (V[nt_, 0] < 0)
    W[nt_, ix["Bip01_Spine1"]] += add[nt_] * (V[nt_, 0] >= 0)
    info["mittellinie_punkte"] = int(((1.0 - fm) * wl > 1e-6).sum())
    # Bein-Zugehoerigkeit unten: an Punkten mit Bein-Anteil >= 0,2 geht der Rumpf-Anteil unter z 0,24 ganz, bis 0,34 weich auf das Bein
    # (anteilig nach den Bein-Gewichten des Punkts); der heutige Optimierer hatte Becken bis weit an die Innenseite der langen Beine gelegt
    wl = W[:, beinb].sum(1)
    wt_ = W[:, torso].sum(1)
    import baer_beine_gj2 as BG
    _bb, _kn, d_bein = BG.naechster_bein_knochen(V, J)
    u = (1.0 - sst(0.24, 0.34, V[:, 2])) * (wl >= 0.2) * (teil == 0) * sst(0.04, 0.07, np.abs(V[:, 1])) * (1.0 - sst(0.10, 0.14, d_bein))
    mv = wt_ * u
    W[:, torso] *= (1.0 - u)[:, None]
    W[:, beinb] += (W[:, beinb] / np.maximum(wl, 1e-9)[:, None]) * mv[:, None]
    info["bein_unten_punkte"] = int((mv > 1e-6).sum())
    # Unterglied nur am Unterglied: Unterarm/Hand bzw. Unterschenkel/Fuss-Anteil faellt hinter/ueber dem Ellbogen/Knie (Abstand entlang
    # der Achse s < 0, weich bis -6 cm) und seitlich weg von der Achse (10..16 cm) weg und geht an Oberarm/Oberschenkel. Gemessen (Start
    # v2): Bauch hinter dem Ellbogen trug Unterarm 0,3..0,4 -> sigma1 bis 14 im Hieb.
    for s_ in "LR":
        for ob, un, en in (("UpperArm", "Forearm", "Hand"), ("Thigh", "Calf", "Foot")):
            o_, u_, e_ = ("Bip01_%s_%s" % (s_, x) for x in (ob, un, en))
            a0, a1 = J[u_], J[e_]
            ax = (a1 - a0) / np.linalg.norm(a1 - a0)
            sv = (V - a0) @ ax
            lat = np.linalg.norm((V - a0) - sv[:, None] * ax[None, :], axis=1)
            fak = sst(-0.06, 0.0, sv) * (1.0 - sst(0.10, 0.16, lat))
            fak[teil != 0] = 1.0
            for kn in (u_, e_):
                w_ = W[:, ix[kn]]
                W[:, ix[o_]] += w_ * (1.0 - fak)
                W[:, ix[kn]] = w_ * fak
    # Punkte IM Unterglied (Kapsel um Knie->Sprunggelenk bzw. Ellbogen->Handgelenk, Radius 7,5..10,5 cm, ab 0..3 cm unter dem Gelenk)
    # tragen keinen Rumpf (gemessen: Unterarm-Innenseite mit Wirbel 0,1..0,2, Unterschenkel-Innenseite mit Becken 0,2..0,3 -> sigma1 7..8)
    for s_ in "LR":
        for un, en in (("Forearm", "Hand"), ("Calf", "Foot")):
            u_, e_ = "Bip01_%s_%s" % (s_, un), "Bip01_%s_%s" % (s_, en)
            a0, a1 = J[u_], J[e_]
            L_ = float(np.linalg.norm(a1 - a0))
            ax = (a1 - a0) / L_
            sv = (V - a0) @ ax
            lat = np.linalg.norm((V - a0) - sv[:, None] * ax[None, :], axis=1)
            m_in = sst(0.0, 0.03, sv) * (1.0 - sst(L_, L_ + 0.04, sv)) * (1.0 - sst(0.075, 0.105, lat)) * (teil == 0)
            mvt = W[:, torso].sum(1) * m_in
            W[:, torso] *= (1.0 - m_in)[:, None]
            W[:, ix[u_]] += mvt
    # Uebergaenge glaetten (Bein-Rumpf-Zone z 0,16..0,45, ohne Kopf), Rand fest
    zb = (V[:, 2] > 0.16) & (V[:, 2] < 0.45) & (teil == 0)
    W = laplace(W, E, zb, runden=12, lam=0.5)
    # Pfoten unter dem Gelenk starr: Hand/Fuss-Anteil -> 1 (weich von Gelenk-z +1 cm bis -3 cm), nur Std-Teil
    for k, (e, kette) in {"VL": ("Bip01_L_Hand", ("Bip01_L_Forearm", "Bip01_L_UpperArm")), "VR": ("Bip01_R_Hand", ("Bip01_R_Forearm", "Bip01_R_UpperArm")),
                          "HL": ("Bip01_L_Foot", ("Bip01_L_Calf", "Bip01_L_Thigh")), "HR": ("Bip01_R_Foot", ("Bip01_R_Calf", "Bip01_R_Thigh"))}.items():
        mm = N["pfote_" + k].astype(bool) | ((teil == 1) & (W[:, ix[e]] > 0.3))
        r = sst(J[e][2] + 0.01, J[e][2] - 0.03, V[:, 2]) * mm
        r = np.maximum(r, kr * (W[:, ix[e]] > 0.3))
        W[:, :] *= (1.0 - r)[:, None]
        W[:, ix[e]] += r
    # Kopf/Ohren starr wie heute (Head 1,0 fuer die starren Kopf-Punkte der heutigen Endgewichte)
    Go = np.load(Q + "gen/gewichte_end.npz")
    q = N["quelle"]
    gen = (teil == 0) & (q >= 0) & (q < len(Go["V"]))
    ks = np.zeros(len(V), bool)
    ks[gen] = Go["kopf_starr"][q[gen]].astype(bool)
    W[ks] = 0.0
    W[ks, ix["Bip01_Head"]] = 1.0
    info["kopf_starr"] = int(ks.sum())
    W = vier(W)
    info["einfluesse_max"] = int((W > 0).sum(1).max())
    info["summe_abw"] = float(np.abs(W.sum(1) - 1).max())
    R = regionen_neu(N)
    np.savez(aus, W=W, namen=np.array(nam), V=V, T=T, regionen=R, regionen_namen=np.array(REG_NAMEN), kralle=kr, kopf_starr=ks,
             info=np.array(json.dumps(info)))
    log("START", info, "->", aus)
    return info


# =================================================================================================================================
# DEHNUNG (Formel wie baer_gewichte_rig.dehnung)
# =================================================================================================================================
def dreieck_basis(V, T):
    P0 = U.dump(V)
    e1 = P0[T[:, 1]] - P0[T[:, 0]]
    e2 = P0[T[:, 2]] - P0[T[:, 0]]
    l01, l02 = np.linalg.norm(e1, axis=1), np.linalg.norm(e2, axis=1)
    l12 = np.linalg.norm(P0[T[:, 2]] - P0[T[:, 1]], axis=1)
    gt = np.minimum(np.minimum(l01, l02), l12) > 0.004
    gt &= np.linalg.norm(np.cross(e1, e2), axis=1) / np.maximum(np.maximum(l01, l02), l12) > 0.002 * M2U
    uu = e1 / l01[:, None]
    nn_ = np.cross(e1, e2)
    nn_ /= np.maximum(np.linalg.norm(nn_, axis=1, keepdims=True), 1e-12)
    vv = np.cross(nn_, uu)
    Rm = np.stack((np.stack(((e1 * uu).sum(1), (e2 * uu).sum(1)), 1), np.stack(((e1 * vv).sum(1), (e2 * vv).sum(1)), 1)), 1)
    RI = np.zeros_like(Rm)
    RI[gt] = np.linalg.inv(Rm[gt])
    return gt, RI


def sigma(P, T, RI):
    Pd = U.dump(P)
    a1 = Pd[T[:, 1]] - Pd[T[:, 0]]
    a2 = Pd[T[:, 2]] - Pd[T[:, 0]]
    F = np.einsum("tij,tjk->tik", np.stack((a1, a2), 2), RI)
    return np.linalg.svd(F, compute_uv=False)


def clip_bilder(G, Z, clip):
    ip = G.idx["Bip01_Pelvis"]
    out = []
    for f in range(len(Z[clip + "_R"])):
        t = G.t_j.copy()
        t[ip] = Z[clip + "_pel"][f]
        out.append(G.fk(t, Z[clip + "_R"][f]))
    return out


def dehnung(netz, gew, skp, clips, aus=None):
    G = U.Gerippe(skp, netz, gew)
    Gw = np.load(gew)
    Z = np.load(clips)
    T = G.netz["T"]
    gt, RI = dreieck_basis(G.V, T)
    RT = Gw["regionen"]
    RN = [str(s) for s in Gw["regionen_namen"]]
    za = np.isin(RT, [RN.index("achsel"), RN.index("brust")])
    out = {}
    for c in U.CLIPS:
        s1all, s2all = [], []
        for M in clip_bilder(G, Z, c):
            sv = sigma(G.haut(M), T, RI)
            s1all.append(sv[:, 0])
            s2all.append(sv[:, 1])
        s1 = np.array(s1all)[:, gt]
        s2 = np.array(s2all)[:, gt]
        rg = RT[gt]
        zone = za[gt]
        tot = s1.max(0)
        out[c] = dict(p995=round(float(np.percentile(s1, 99.5)), 3), max=round(float(s1.max()), 3),
                      achsel_brust_max=round(float(s1[:, zone].max()), 3) if zone.any() else 0.0,
                      falten_s2_unter_05=int((s2.min(0) < 0.5).sum()),
                      max_region=RN[int(rg[int(np.argmax(tot))])], max_bild=int(np.unravel_index(np.argmax(s1), s1.shape)[0]),
                      max_dreieck=int(np.nonzero(gt)[0][int(np.argmax(tot))]))
        log("DEHNUNG %-16s p99,5 %.3f max %.3f (Region %s, Bild %d) Achsel/Brust %.3f Falten(s2<0,5) %d" % (
            c, out[c]["p995"], out[c]["max"], out[c]["max_region"], out[c]["max_bild"], out[c]["achsel_brust_max"], out[c]["falten_s2_unter_05"]))
    if aus:
        json.dump(out, open(aus, "w"), indent=1)
    return out


# =================================================================================================================================
# OPT: projizierter Gradientenabstieg auf den Gewichten der freien Punkte gegen alle 15 Clips (numpy-Gerippe = Importer)
#   E = sum_Bilder sum_Dreiecke [ (sigma1 - s_hi)+^2 + hart (sigma1 - 3,5)+^2 + quetsch (s_lo - sigma2)+^2 ] / Bilder
#     + glatt * sum_Kanten |w_i - w_j|^2 + anker * |w - w_start|^2
#   frei: nicht Kopf (starr), nicht Krallen, nicht Pfote unter dem Gelenk, z < z_max; Kandidaten je Punkt = Knochen im 2-Ring der
#   Startgewichte (Gegenseite der Beine verboten); am Ende hoechstens 4 Einfluesse, Summe 1.
# =================================================================================================================================
def proj_simplex(Y, maske):
    """Zeilenweise Projektion auf {w >= 0, sum w = 1} nur ueber die erlaubten Spalten."""
    Y = np.where(maske, Y, -1e9)
    n, k = Y.shape
    s = -np.sort(-Y, axis=1)
    cs = np.cumsum(s, axis=1) - 1.0
    r = np.arange(1, k + 1)
    cond = s - cs / r > 0
    rho = k - 1 - np.argmax(cond[:, ::-1], axis=1)
    theta = cs[np.arange(n), rho] / (rho + 1)
    return np.where(maske, np.maximum(Y - theta[:, None], 0.0), 0.0)


def opt(netz, gew, skp, clips, aus, kv=""):
    P = dict(s_hi=1.9, s_lo=0.45, hart=10.0, quetsch=0.5, glatt=0.1, anker=0.01, runden=90, lr=0.05, schritt=4, z_max=0.80)
    if kv:
        for k_v in kv.split(","):
            k, v = k_v.split("=")
            P[k] = float(v)
    G = U.Gerippe(skp, netz, gew)
    Gw = np.load(gew)
    Z = np.load(clips)
    V, T = G.V, G.netz["T"]
    W0 = G.W.copy()
    nb = G.nb
    ix = G.idx
    kr = Gw["kralle"].astype(bool)
    ks = Gw["kopf_starr"].astype(bool)
    pfk = [ix[n] for n in ("Bip01_L_Hand", "Bip01_R_Hand", "Bip01_L_Foot", "Bip01_R_Foot")]
    starr = ks | kr | (W0[:, pfk].sum(1) > 0.97) | (V[:, 2] > P["z_max"])
    frei = ~starr
    fi = np.nonzero(frei)[0]
    brust0 = np.zeros(len(V), bool)
    if P.get("brust_arm0", 0) > 0:
        # Nachbesserung 12.11. (PRUEF_TECHNIK 7.4, Maengel T4): Brust-/Bauchunterseite in der Mitte (hinter dem Schultergelenk, unter
        # Schulterhoehe - 15 cm) bekommt kein Arm-Gewicht: |y| < 2,5 cm Arm 0, bis 6,5 cm weich zurueck; die Arm-Anteile gehen anteilig an
        # die Rumpf-Knochen des Punkts (sonst an Spine1). Der Prankenhieb zieht die Mitte dann nicht mehr mit (Spitze SwipeL 3,75).
        sh = G.J["Bip01_L_UpperArm"]
        armb = [ix[n] for n in ("Bip01_L_UpperArm", "Bip01_L_Forearm", "Bip01_R_UpperArm", "Bip01_R_Forearm")]
        torb = [b for b, n in enumerate(G.names) if not any(t_ in n for t_ in ("Thigh", "Calf", "Foot", "Toe0", "UpperArm", "Forearm", "Hand"))]
        zone = frei & (V[:, 2] < sh[2] - 0.15) & (V[:, 0] > sh[0] - 0.30) & (V[:, 0] < sh[0] + 0.06)
        fak = np.where(zone, sst(0.025, 0.065, np.abs(V[:, 1])), 1.0)
        W0 = W0.copy()
        weg = W0[:, armb].sum(1) * (1.0 - fak)
        W0[:, armb] *= fak[:, None]
        tw = W0[:, torb].sum(1)
        anteil = np.where(tw[:, None] > 1e-9, W0[:, torb] / np.maximum(tw[:, None], 1e-12), 0.0)
        anteil[tw <= 1e-9, torb.index(ix["Bip01_Spine1"])] = 1.0
        W0[:, torb] += weg[:, None] * anteil
        brust0 = zone & (np.abs(V[:, 1]) < 0.025)
        G.W = W0.copy()
        log("OPT brust_arm0: Zone %d Punkte, Arm 0 bei %d Punkten, Arm-Gewicht umgelegt %.2f" % (zone.sum(), brust0.sum(), weg.sum()))
    E = kanten(T, len(V))
    nbm = (W0 > 1e-6).astype(float)
    for _ in range(2):
        acc = nbm.copy()
        np.add.at(acc, E[:, 0], nbm[E[:, 1]])
        np.add.at(acc, E[:, 1], nbm[E[:, 0]])
        nbm = (acc > 0).astype(float)
    kand = nbm > 0
    for s, gs in (("L", -1), ("R", 1)):
        seite = V[:, 1] * gs > 0.02
        for b, n in enumerate(G.names):
            if ("_%s_" % s) in n:
                kand[seite, b] = False
    for n in ("Dummy01", "Bip01", "Translation_Data", "Bip01_L_Toe0", "Bip01_R_Toe0", "Bip01_L_Clavicle", "Bip01_R_Clavicle", "Bip01_Jaw"):
        kand[:, ix[n]] = False
    kand |= W0 > 1e-6
    if brust0.any():
        kand[np.ix_(brust0, armb)] = False
    if P.get("nur_traeger", 0) > 0:
        kand = W0 > 1e-6               # Feinschliff nach der 4-Einfluesse-Kappung: nur die vorhandenen (hoechstens 4) Knochen je Punkt
    kt = frei[T].any(1)
    T2 = T[kt]
    gt, RI = dreieck_basis(V, T2)
    T2, RI = T2[gt], RI[gt]
    bilder = []
    for c in U.CLIPS:
        n_ = len(Z[c + "_R"])
        fr = set(range(0, n_, int(P["schritt"]))) | {n_ - 1}
        if c in ("DeerStag_Walk", "DeerStag_Run"):
            fr = set(range(n_))
        if c in ("NCBear_SwipeL", "NCBear_SwipeR"):
            fr |= set(range(6, min(24, n_)))
        Ms = clip_bilder(G, Z, c)
        for f in sorted(fr):
            bilder.append(Ms[f])
    nfb = len(bilder)
    log("OPT frei %d Punkte, Kandidaten im Mittel %.1f, Dreiecke %d, Bilder %d, Parameter %s" % (
        len(fi), kand[fi].sum(1).mean(), len(T2), nfb, json.dumps(P)))
    used = np.unique(T2)
    pos_u = -np.ones(len(V), int)
    pos_u[used] = np.arange(len(used))
    T2u = pos_u[T2]
    Hu = G.H0[used]
    SK = [np.einsum("bij,bjk->bik", M, G.INV)[:, :3, :] for M in bilder]
    Eu_m = frei[E[:, 0]] | frei[E[:, 1]]

    def energie(W, grad=True):
        Etot = 0.0
        g = np.zeros((len(used), nb)) if grad else None
        Wu = W[used]
        s1max = 0.0
        for Sk in SK:
            Y = np.einsum("bij,nj->nbi", Sk, Hu)
            Pp = np.einsum("nb,nbi->ni", Wu, Y)
            a1 = Pp[T2u[:, 1]] - Pp[T2u[:, 0]]
            a2 = Pp[T2u[:, 2]] - Pp[T2u[:, 0]]
            F = np.einsum("tij,tjk->tik", np.stack((a1, a2), 2), RI)
            Uu, S, Vt = np.linalg.svd(F, full_matrices=False)
            s1, s2 = S[:, 0], S[:, 1]
            s1max = max(s1max, float(s1.max()))
            e1 = np.maximum(s1 - P["s_hi"], 0.0)
            e2 = np.maximum(s1 - 3.5, 0.0)
            e3 = np.maximum(P["s_lo"] - s2, 0.0)
            Etot += float((e1 * e1).sum() + P["hart"] * (e2 * e2).sum() + P["quetsch"] * (e3 * e3).sum())
            if grad:
                c1 = 2 * e1 + 2 * P["hart"] * e2
                c2 = -2 * P["quetsch"] * e3
                dF = (c1[:, None, None] * np.einsum("ti,tj->tij", Uu[:, :, 0], Vt[:, 0, :])
                      + c2[:, None, None] * np.einsum("ti,tj->tij", Uu[:, :, 1], Vt[:, 1, :]))
                dA = np.einsum("tik,tjk->tij", dF, RI)
                gP = np.zeros_like(Pp)
                np.add.at(gP, T2u[:, 1], dA[:, :, 0])
                np.add.at(gP, T2u[:, 2], dA[:, :, 1])
                np.add.at(gP, T2u[:, 0], -dA[:, :, 0] - dA[:, :, 1])
                g += np.einsum("ni,nbi->nb", gP, Y)
        Etot /= nfb
        d = W[E[Eu_m, 0]] - W[E[Eu_m, 1]]
        Eg = P["glatt"] * float((d * d).sum())
        Ea = P["anker"] * float(((W[frei] - W0[frei]) ** 2).sum())
        gfull = np.zeros_like(W)
        if grad:
            gfull[used] = g / nfb
            gg = np.zeros_like(W)
            np.add.at(gg, E[Eu_m, 0], 2 * P["glatt"] * d)
            np.add.at(gg, E[Eu_m, 1], -2 * P["glatt"] * d)
            gfull += gg
            gfull[frei] += 2 * P["anker"] * (W[frei] - W0[frei])
            gfull[~frei] = 0.0
        return Etot + Eg + Ea, gfull, (Etot, Eg, Ea, s1max)
    # projizierter Gradientenabstieg (Schritt = lr / max|Gradient|, Rueckschritt halbiert, Erfolg x1,15); das beste W zaehlt
    W = W0.copy()
    lr = P["lr"]
    Ecur, gcur, parts = energie(W)
    log("OPT Start E %.4f (Dehnung %.4f, Glaette %.4f, Anker %.4f, sigma1 max %.2f)" % ((Ecur,) + parts))
    for it in range(int(P["runden"])):
        gn = gcur[fi]
        sc = lr / max(np.abs(gn).max(), 1e-12)
        Wn = W.copy()
        Wn[fi] = proj_simplex(W[fi] - sc * gn, kand[fi])
        En, gnew, pn = energie(Wn)
        if En < Ecur:
            W, Ecur, gcur, parts = Wn, En, gnew, pn
            lr *= 1.15
        else:
            lr *= 0.5
        if it % 5 == 0 or it == int(P["runden"]) - 1:
            log("OPT Runde %d E %.4f (Dehnung %.4f, Glaette %.4f, Anker %.4f, sigma1 max %.2f) lr %.4f" % ((it, Ecur) + parts + (lr,)))
        if lr < 1e-5:
            break
    W4 = vier(W)
    E4, _g, p4 = energie(W4, grad=False)
    log("OPT nach 4-Einfluesse: E %.4f (sigma1 max %.2f)" % (E4, p4[3]))
    out = dict(Gw)
    out["W"] = W4
    out["W_vor_opt"] = W0
    out["opt_info"] = np.array(json.dumps(dict(P=P, E_end=E4, sigma1_max=p4[3])))
    np.savez(aus, **out)
    log("OPT ->", aus)


if __name__ == "__main__":
    if sys.argv[1] == "start":
        start(*sys.argv[2:6])
    elif sys.argv[1] == "dehnung":
        dehnung(*sys.argv[2:7])
    elif sys.argv[1] == "opt":
        opt(*sys.argv[2:8])
