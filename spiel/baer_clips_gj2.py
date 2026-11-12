# Lauf baer-gen-junges-v2 (12.11.2026), Bauer BEINE: Gehen und Rennen des Generator-Jungen fuer die KURZEN Beine (PLAN.md 4.5.1).
# numpy-Umsetzung (statt Blender/mathutils) der Gang-Teile aus baer_clips_rig.py (Original unveraendert): fuss_bahn_j / gang_j /
# ballen_zu_ferse_j wortgetreu in den Formeln, Rumpf nach pose_walk (Gehen) bzw. pose_galopp (Rennen) mit den Werten aus PLAN 3.3;
# Gelenke/IK/Haut aus baer_umrechnen_gj2.Gerippe (dasselbe Skelett wie der Export). Neu: Abrollpunkt aus der neuen Pfote (Vorderkante
# der Sohle), Gehen = Baeren-Schritt/Passgang mit 2 Zyklen (T 13,5 Bilder), Boden an der HAUT (Stuetzpfote tiefster Punkt auf 0 nur
# ueber das Gelenk-z, x/y bleiben in der Welt stehen -> kein Gleiten), freie Pfoten nie unter den Boden.
# Ausgabe npz (fuer baer_export_gj2.py neu=...): <Clip>_R, <Clip>_pel, <Clip>_weg (Translation_Data-Ende, E), <Clip>_u (Phase je Bein
# VL VR HL HR), <Clip>_duty; dazu <Clip>_abroll (Bilder x 4 x 3 Abrollpunkt Welt, tier) fuer die Gleit-Messung.
# Aufruf: python baer_clips_gj2.py --skelett SK.json --netz NETZ.npz --gewichte GEW.npz --aus GANG.npz [--gang PARAM.json] [--gehen-zyklen 3]
# Tempo in Kacheln/s = Weg(E) x 1,6 / Dauer (rig RIG_PLAN 5.3: AnimationPlayer.java:1235, Defaults.xml:3). Statisch/offline, nicht gespielt.
import argparse
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_umrechnen_gj2 as U  # noqa: E402

FPS = 30
K_WELT = 1.6 / 1.5
WEG_GROESSE = 0.35
M2U = 0.544
T0 = time.time()
# Gehen: Baeren-Schritt (Passgang-Kontakte wie WALK des 2c), 2 Zyklen je 0,9 s; Werte PLAN 3.3
WALK_J = dict(name="DeerStag_Walk", T=13.5, N=2, duty=0.62,
              kontakt=dict(HL=0.00, VL=0.10, HR=0.50, VR=0.60),
              S=dict(H=0.33, V=0.33), mitte=dict(H=0.0, V=0.0), hub=dict(H=0.045, V=0.055),
              ab=dict(H=19.0, V=19.0), spitze=dict(H=30.0, V=32.0), aussen=0.012, senk=0.004, streck=dict(H=0.97, V=0.985),
              m0=dict(V=1.0, H=1.0), hexp=dict(V=0.85, H=0.85),
              becken_roll=4.5, brust_roll=6.0, becken_wipp=0.020, kopf_nick=2.5, kopf_grund=1.5, hals_grund=1.5, klav=10.0)
# Rennen: Galopp wie RUN_J des Generators (Kontakte RUN), an kurze Beine angepasst; 2 Zyklen je 0,5333 s (T 8)
RUN_J = dict(name="DeerStag_Run", T=8, N=2, duty=0.20,
             kontakt=dict(HL=0.00, HR=0.08, VL=0.42, VR=0.52),
             S=dict(H=0.42, V=0.42), mitte=dict(H=0.02, V=-0.01), hub=dict(H=0.08, V=0.09),
             ab=dict(H=22.0, V=20.0), spitze=dict(H=40.0, V=45.0), aussen=0.03, senk=0.010, streck=dict(H=0.97, V=0.985),
             m0=dict(V=0.3, H=1.0), hexp=dict(V=0.6, H=0.85), spur=dict(H=0.01, V=-0.005))


def log(*a):
    print("GANG", round(time.time() - T0, 1), *a, flush=True)


def ssf(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


def hermite(s, p0, p1, m0, m1):
    s2, s3 = s * s, s * s * s
    return (2 * s3 - 3 * s2 + 1) * p0 + (s3 - 2 * s2 + s) * m0 + (-2 * s3 + 3 * s2) * p1 + (s3 - s2) * m1


def c(x):
    return math.cos(2.0 * math.pi * x)


def weg_j(G_):
    """Translation_Data am Clip-Ende (E): N Zyklen, Weg je Zyklus S/duty (m bei Groesse 1,0) x M2U / K_WELT x WEG_GROESSE (wie baer_clips_rig.weg_j)."""
    return G_["N"] * G_["S"]["H"] / G_["duty"] * M2U / K_WELT * WEG_GROESSE


class Gang:
    def __init__(self, G):
        self.G = G
        N = G.netz
        # Abrollpunkt je Pfote: Vorderkante der Sohle (Sohlen-Maske der neuen Pfote), Hoehe 0,6 cm, quer am Gelenk
        self.abroll = {}
        for k in U.PF:
            e = U.BEIN[k][2]
            m = np.zeros(len(G.V), bool)
            m[G.pfote[k]] = True
            m &= N["sohle"].astype(bool)
            x_vorn = float(G.V[m, 0].max())
            self.abroll[k] = np.array((x_vorn, G.J[e][1], 0.006))

    def fuss_bahn(self, P, k, phi):
        art = k[0]
        s_ = 1.0 if k[1] == "L" else -1.0
        u = (phi - P["kontakt"][k]) % 1.0
        duty, S, cc = P["duty"], P["S"][art], P["mitte"][art]
        b = self.abroll[k]
        x0 = b[0] + cc
        spur = P.get("spur", {}).get(art, 0.0)
        if u < duty:
            w = u / duty
            x = x0 + S * 0.5 - S * w
            z = b[2]
            y = b[1] + s_ * spur
            pit = P["ab"][art] * ssf(0.60, 1.0, w)
        else:
            s = (u - duty) / (1.0 - duty)
            m = -S * min((1.0 - duty) / duty, 1.0)
            x = hermite(s, x0 - S * 0.5, x0 + S * 0.5, m * P.get("m0", {}).get(art, 1.0), m * P.get("m1", {}).get(art, 1.0))
            z = b[2] + P["hub"][art] * math.sin(math.pi * s ** P.get("hexp", {}).get(art, 0.85))
            y = b[1] + s_ * (spur + P["aussen"] * math.sin(math.pi * s))
            if s < 0.30:
                pit = P["ab"][art] + (P["spitze"][art] - P["ab"][art]) * ssf(0.0, 0.30, s)
            else:
                pit = P["spitze"][art] * (1.0 - ssf(0.30, 0.88, s)) - 7.0 * ssf(0.70, 0.90, s) * (1.0 - ssf(0.92, 1.0, s))
        return np.array((x, y, z)), pit, u

    def ziel(self, k, ball, pit):
        """Abrollpunkt + Neigung -> Gelenk (Sprung/Hand) und Pfoten-Drehung (wie ballen_zu_ferse_j)."""
        q = U.ry(pit)
        e = U.BEIN[k][2]
        return ball + q @ (self.G.J[e] - self.abroll[k]), q

    def bild(self, P, phi, rumpf, stat, dz_boden=None):
        G = self.G
        ziele = {}
        for k in U.PF:
            ball, pit, u = self.fuss_bahn(P, k, phi)
            ank, q = self.ziel(k, ball, pit)
            if dz_boden is not None:
                ank = ank + np.array((0.0, 0.0, dz_boden[k]))
            ziele[k] = (ank, q, u < P["duty"] + 0.05 or u > 0.96, u, ball)
        dz, dp = 0.0, 0.0
        for _ in range(8):
            Qw, pel = rumpf(dz, dp)
            _R, _t, M0 = G.pose(Qw, pel)
            bed = dict(V=0.0, H=0.0)
            for k, (ank, q, st, u, _b) in ziele.items():
                if not st:
                    continue
                L = G.leg[k]
                hip = G.gelenk(M0, L["o"])
                dmax = P["streck"][k[0]] * (L["a"] + L["b"])
                dxy2 = (hip[0] - ank[0]) ** 2 + (hip[1] - ank[1]) ** 2
                zreq = ank[2] + math.sqrt(max(dmax * dmax - dxy2, 0.0))
                bed[k[0]] = min(bed[k[0]], zreq - hip[2])
            if bed["H"] > -2e-4 and bed["V"] > -2e-4:
                break
            dz += bed["H"]
            dp += math.degrees(math.atan2(-bed["V"], 0.37))
        stat["absenk"] = min(stat.get("absenk", 0.0), dz)
        stat["neig"] = max(stat.get("neig", 0.0), dp)
        ueber = []
        for k, (ank, q, st, u, _b) in ziele.items():
            L = G.leg[k]
            H = G.gelenk(M0, L["o"])
            Ro, Ru, K, A2, sv = G.ik(k, H, ank, L["pol"], ueber)
            Qw[L["o"]] = Ro
            Qw[L["u"]] = Ru
            Qw[L["e"]] = q
            if k[0] == "H":
                Qw[L["e"].replace("Foot", "Toe0")] = q
        stat.setdefault("ueber", []).extend(ueber)
        R, t, M = G.pose(Qw, pel)
        return R, t, M, {k: v[3] for k, v in ziele.items()}, {k: v[4] for k, v in ziele.items()}

    def rumpf_schritt(self, P, phi):
        G = self.G
        J = G.J
        wieg = c(phi - 0.81)

        def rumpf(dz, dp):
            pel = J["Bip01_Pelvis"] + np.array((0.006 * c(phi * 2), -0.015 * wieg, -P["senk"] + 0.5 * P["becken_wipp"] * c(2 * (phi - 0.05)) + dz))
            Qw = {}
            Qw["Bip01_Pelvis"] = U.euler(yaw=-3.0 * c(phi), pitch=1.0 * c(2 * (phi - 0.10)), roll=P["becken_roll"] * wieg)
            Qw["Bip01_Spine"] = U.ry(dp * 0.6) @ U.euler(yaw=-1.0 * c(phi - 0.05), pitch=0.6 * c(2 * (phi - 0.14)), roll=0.7 * P["becken_roll"] * c(phi - 0.85))
            Qw["Bip01_Spine1"] = U.ry(dp) @ U.euler(yaw=-4.0 * c(phi - 0.10), pitch=-0.8 * c(2 * (phi - 0.20)), roll=P["brust_roll"] * c(phi - 0.91))
            Qw["Bip01_Neck"] = U.euler(yaw=1.0 * c(phi - 0.14), pitch=P["hals_grund"] + 1.0 * c(2 * (phi - 0.28)), roll=1.5 * c(phi - 0.95))
            Qw["Bip01_Head"] = U.euler(yaw=4.0 * c(phi - 0.20), pitch=P["kopf_grund"] + P["kopf_nick"] * c(2 * (phi - 0.34)), roll=-1.0 * c(phi - 0.20))
            Qw["Bip01_Jaw"] = Qw["Bip01_Head"]
            Qw["Bip01_Tail"] = U.euler(yaw=7.0 * c(phi - 0.30), pitch=-2.0 * c(2 * phi))
            for n, ph in (("L", P["kontakt"]["VL"]), ("R", P["kontakt"]["VR"])):
                Qw["Bip01_%s_Clavicle" % n] = Qw["Bip01_Spine1"] @ U.ry(-P["klav"] * math.cos(2.0 * math.pi * (phi - ph)))
            return Qw, pel
        return rumpf

    def rumpf_galopp(self, P, phi):
        J = self.G.J
        beug = c(phi - 0.97)
        kipp = c(phi - 0.18)

        def rumpf(dz, dp):
            pel = J["Bip01_Pelvis"] + np.array((0.035 * beug, 0.006 * c(phi - 0.2), -P["senk"] + 0.015 * c(phi - 0.86) + dz))
            Qw = {}
            Qw["Bip01_Pelvis"] = U.euler(yaw=2.0 * c(phi - 0.1), pitch=-8.0 * beug - 3.0 * kipp, roll=2.5 * c(phi - 0.05))
            Qw["Bip01_Spine"] = U.ry(dp * 0.6) @ U.euler(yaw=0.5 * c(phi - 0.15), pitch=-2.0 * beug - 3.0 * kipp, roll=1.2 * c(phi - 0.1))
            Qw["Bip01_Spine1"] = U.ry(dp) @ U.euler(yaw=-2.0 * c(phi - 0.45), pitch=5.0 * beug - 3.0 * kipp, roll=-2.5 * c(phi - 0.50))
            Qw["Bip01_Neck"] = U.euler(yaw=1.0 * c(phi - 0.5), pitch=2.0 + 2.0 * beug + 3.0 * kipp, roll=-1.0 * c(phi - 0.5))
            Qw["Bip01_Head"] = U.euler(yaw=1.5 * c(phi - 0.55), pitch=1.0 + 4.0 * kipp, roll=0.0)
            Qw["Bip01_Jaw"] = Qw["Bip01_Head"]
            Qw["Bip01_Tail"] = U.euler(yaw=5.0 * c(phi - 0.3), pitch=-10.0 * c(phi - 0.1))
            for n, ph in (("L", P["kontakt"]["VL"]), ("R", P["kontakt"]["VR"])):
                Qw["Bip01_%s_Clavicle" % n] = Qw["Bip01_Spine1"] @ U.ry(-12.0 * math.cos(2.0 * math.pi * (phi - ph)))
            return Qw, pel
        return rumpf

    def clip(self, P, art):
        G = self.G
        n = int(round(P["T"] * P["N"]))
        assert abs(n - P["T"] * P["N"]) < 1e-9, (P["T"], P["N"])
        stat = {}
        rf = self.rumpf_schritt if art == "schritt" else self.rumpf_galopp
        # Boden-Korrektur je Bein und Phase (zyklisch): Stuetze -> tiefste Pfotenhaut auf 0; frei -> nie unter 0
        dzb = np.zeros((n + 1, 4))
        for runde in range(3):
            out = []
            for i in range(n + 1):
                phi = i / P["T"]
                R, t, M, u, ball = self.bild(P, phi, rf(P, phi), stat if runde == 2 else {}, {k: dzb[i % n, j] for j, k in enumerate(U.PF)})
                Pk = G.haut(M)
                for j, k in enumerate(U.PF):
                    low = float(Pk[G.pfote[k], 2].min())
                    if u[k] < P["duty"]:
                        dzb[i % n, j] -= low
                    elif low < 0.0:
                        dzb[i % n, j] -= low
                out.append((R, t, M, u, ball))
            dzb[n] = dzb[0]
        ip = G.idx["Bip01_Pelvis"]
        R = np.array([o[0] for o in out])
        pel = np.array([o[1][ip] for o in out])
        Uu = np.array([[o[3][k] for k in U.PF] for o in out])
        # Abrollpunkt in Welt (starr an der Pfote)
        abr = np.zeros((n + 1, 4, 3))
        for i, o in enumerate(out):
            M = o[2]
            for j, k in enumerate(U.PF):
                b = G.idx[U.BEIN[k][2]]
                loc = G.INV[b] @ np.r_[U.dump(self.abroll[k]), 1.0]
                abr[i, j] = U.tier((M[b] @ loc)[:3])
        return dict(R=R, pel=pel, u=Uu, weg=weg_j(P), duty=P["duty"], abroll=abr, stat=stat, dzb=dzb, M=np.array([o[2] for o in out]))


def messen(G, res, P):
    """Boden, Gleiten (Welt bei Groesse 1,0 und im Spiel bei 0,35), Becken, Ueberstreckung."""
    n = len(res["R"])
    M = res["M"]
    d = res["weg"] * np.arange(n) / (n - 1) * 1.6 / (1.5 * 0.35) / M2U
    st = res["u"] < P["duty"]
    Ps = [G.haut(m) for m in M]
    erg = dict(bilder=n, weg_E=round(res["weg"], 5), tempo_kacheln_s=round(res["weg"] * 1.6 / ((n - 1) / FPS), 3),
               zyklen=P["N"], takt_hz=round(P["N"] / ((n - 1) / FPS), 2), ueberstreckt=len(res["stat"].get("ueber", [])),
               absenk_m=round(res["stat"].get("absenk", 0.0), 4), netz_min_cm=round(100 * min(p[:, 2].min() for p in Ps), 2))
    ip = G.idx["Bip01_Pelvis"]
    pz = np.array([U.tier(m[ip][:3, 3])[2] for m in M])
    erg["becken_z_pp_cm"] = round(100 * float(np.ptp(pz)), 2)
    erg["boden_stuetz_cm"], erg["gleiten_cm_gr1"], erg["gleiten_cm_spiel035"], erg["luft_min_cm"], erg["hub_cm"] = {}, {}, {}, {}, {}
    for j, k in enumerate(U.PF):
        z = np.array([p[G.pfote[k], 2].min() for p in Ps])
        erg["boden_stuetz_cm"][k] = [round(100 * float(z[st[:, j]].min()), 2), round(100 * float(z[st[:, j]].max()), 2)]
        erg["luft_min_cm"][k] = round(100 * float(z[~st[:, j]].min()), 2) if (~st[:, j]).any() else None
        erg["hub_cm"][k] = round(100 * float(z.max()), 2)
        m_ = n - 1
        start = [i for i in range(m_) if st[i, j] and not st[(i - 1) % m_, j]]
        sp = []
        for i0 in start:
            ph = [i0]
            while st[(ph[-1] + 1) % m_, j] and len(ph) < m_:
                ph.append((ph[-1] + 1) % m_)
            xs = [res["abroll"][i, j, 0] + d[i] + (d[-1] if i < ph[0] else 0.0) for i in ph]
            ys = [res["abroll"][i, j, 1] for i in ph]
            sp.append(max(np.ptp(xs), np.ptp(ys)))
        g = max(sp) if sp else 0.0
        erg["gleiten_cm_gr1"][k] = round(100 * g, 2)
        erg["gleiten_cm_spiel035"][k] = round(100 * g * 1.5 * 0.35, 2)
    return erg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skelett", required=True)
    ap.add_argument("--netz", required=True)
    ap.add_argument("--gewichte", required=True)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--gang", default="")
    ap.add_argument("--gehen-zyklen", type=int, default=2)
    ap.add_argument("--info", default="")
    a = ap.parse_args()
    G = U.Gerippe(a.skelett, a.netz, a.gewichte)
    gg = Gang(G)
    W, Rn = dict(WALK_J), dict(RUN_J)
    if a.gang:
        gp = json.load(open(a.gang))
        W.update(gp.get("WALK_J", {}))
        Rn.update(gp.get("RUN_J", {}))
    if a.gehen_zyklen != 2:
        W["N"] = a.gehen_zyklen
        W["T"] = 27.0 / a.gehen_zyklen
    out, infos = {}, {"abroll": {k: np.round(v, 4).tolist() for k, v in gg.abroll.items()}}
    for P, art in ((W, "schritt"), (Rn, "galopp")):
        res = gg.clip(P, art)
        nm = P["name"]
        out[nm + "_R"], out[nm + "_pel"], out[nm + "_u"] = res["R"], res["pel"], res["u"]
        out[nm + "_weg"], out[nm + "_duty"], out[nm + "_abroll"] = np.array(res["weg"]), np.array(res["duty"]), res["abroll"]
        e = messen(G, res, P)
        e["param"] = {k: v for k, v in P.items() if k != "name"}
        infos[nm] = e
        log(nm, json.dumps({k: v for k, v in e.items() if k != "param"}))
    np.savez(a.aus, **out)
    if a.info:
        json.dump(infos, open(a.info, "w"), indent=1)
    log("->", a.aus)


if __name__ == "__main__":
    main()
