# Lauf baer-gen-junges-v2 (12.11.2026), Bauer BEINE: Kopie von baer_export_rig.py (Original unveraendert, MD5 vorher/nachher gleich).
# Geaendert (mit "GJ2" markiert): Gerippe/Dump des 2c aus _arbeit/baer_gen_junges/v2/quelle/2c (feste Kopien 08ec7806 / b2952b5a),
# Vorgabe-Skelett v2/beine/skelett_gj2.json, Netzname als Parameter (name=, Vorgabe "NCBearCub"), alle 15 Clips aus neu= moeglich.
# Aufruf: python baer_export_gj2.py NETZ.npz GEWICHTE.npz AUS.glb skelett=SKELETT_GJ2.json neu=CLIPS_GJ2.npz [hub=HUB.json] [name=NCBearCub]
# Lauf baer-rig-junges (11.11.2026), Rolle SKELETT+GEWICHTE: VORSTUFE des Exports (RIG_PLAN 4.3 / 6.1). Kopie von
# baer_export_junges.py (Original unveraendert); die Rolle CLIPS+EXPORT uebernimmt und erweitert diese Datei.
# CLIPS+EXPORT (11.11.): neu=CLIPS_NEU.npz (rig/werkzeug/wandle.py aus baer_clips_rig.py): Walk (Trab), Run (Galopp), SitDown/Sit/StandUp
# bekommen Drehungen und Becken aus der Datei (Dummy01/Bip01/Translation_Data-Drehungen bleiben byte-gleich: dort stehen sie in Ruhe),
# Walk/Run ihren Weg (<Clip>_weg, E) statt Erwachsener x WEG_BEZUG; Hub dz wirkt als WELT-Hoehe (tier z) ueber die Bip01-Drehung.
# Reines Python/numpy, kein Blender-Export. Das GLB des ERWACHSENEN (_arbeit/baer_junges/eingang/NCBear.glb, MD5 08ec7806, nur gelesen)
# dient als Gerippe -- gleiche 28 Knoten, gleiche Knochen-Reihenfolge/Namen/Eltern, Skin-Joints, Knoten-DREHUNGEN; getauscht werden nur:
#   - Netz: POSITION/NORMAL/TEXCOORD_0/JOINTS_0 (u8)/WEIGHTS_0, Indizes u16; ein Netz, ein Primitiv, kein Material, kein Bild
#     (Netz = rig/skelett/netz_rig.npz: V verschweisst im Skelettrahmen, T_glb, glb_punkt, UV schon glTF -> NICHT spiegeln)
#   - Knoten-translation und inverse Bind = Ruhe des Jungen aus rig/skelett/skelett_rig.json (lage_E)
#   - 15 Clips: Zeiten, Skalier- und Dreh-Schluessel BYTE-GLEICH mit dem Erwachsenen (ausser SITZ/ABW, fuer CLIPS), Lage-Schluessel
#     konstant = lage_E, Bip01_Pelvis je Bild nach der Becken-Regel (Hueftmitte = Erwachsener + dx_m + Hub dz), Translation_Data =
#     Erwachsener x WEG_BEZUG (Vorab: die Gang-Clips des Erwachsenen; CLIPS ersetzt Walk/Run/Sitz)
# Aufruf: python baer_export_rig.py NETZ_RIG.npz GEWICHTE.npz AUS.glb [skelett=SKELETT_RIG.json] [neu=CLIPS_NEU.npz] [sitz=SITZ.npz] [hub=HUB.json] [abw=ABW.npz]
#   GEWICHTE.npz  W (n verschweisste Punkte x k), namen (k Knochen)
#   SITZ.npz      {"<Clip>_R": Bilder x 26 x 3 x 3 lokale Drehungen (Dump-Raum), "<Clip>_pel": Bilder x 3 Becken-Lage (Dump-Raum, E)}
#   HUB.json      {Clip: [dz je Bild in Metern]};  ABW.npz {"<Clip>|<Knochen>": Bilder x 4 Quaternion lokal (Dump-Raum, x y z w)}
# Statisch/offline, nicht gespielt. Weder Test-Mod noch NPC Crew werden gelesen oder beschrieben.
import json
import pickle
import struct
import sys

import numpy as np

EIN = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/quelle/2c/"   # GJ2: feste Kopien
GLB_ERW = EIN + "NCBear.glb"
DUMP_ERW = EIN + "erw_2c.txt.pkl"
SKELETT = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2/beine/skelett_gj2.json"   # GJ2
M2U = 0.544
CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
F4 = np.diag([1.0, 1.0, -1.0, 1.0])
FZ = np.diag([1.0, 1.0, -1.0])
# Weg je Schritt der byte-gleichen Gang-Clips = Erwachsener x Bezugsgroesse (SPEZ D.6); die neuen Clips (CLIPS) bringen ihren Weg selbst.
WEG_BEZUG = 0.35
SITZ_CLIPS = ("NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp")


def quat_m(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def m_quat(R):
    t = np.trace(R)
    if t > 0:
        s = np.sqrt(t + 1.0) * 2
        q = ((R[2, 1] - R[1, 2]) / s, (R[0, 2] - R[2, 0]) / s, (R[1, 0] - R[0, 1]) / s, 0.25 * s)
    else:
        i = int(np.argmax(np.diag(R)))
        j, k = (i + 1) % 3, (i + 2) % 3
        s = np.sqrt(1.0 + R[i, i] - R[j, j] - R[k, k]) * 2
        q = [0.0, 0.0, 0.0, 0.0]
        q[i] = 0.25 * s
        q[j] = (R[j, i] + R[i, j]) / s
        q[k] = (R[k, i] + R[i, k]) / s
        q[3] = (R[k, j] - R[j, k]) / s
    q = np.array(q)
    return q / np.linalg.norm(q)


def dump(T):
    T = np.asarray(T, float)
    return np.stack((T[..., 1], T[..., 2], -T[..., 0]), -1) * M2U


def lade_json_glb(pfad=GLB_ERW):
    b = open(pfad, "rb").read()
    assert b[:4] == b"glTF"
    n = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + n])
    o = 20 + n
    bl = struct.unpack("<I", b[o:o + 4])[0]
    return J, b[o + 8:o + 8 + bl]


class SkelettRig:
    """Erwachsener (Ruhe-Drehungen aus den GLB-Knoten, Clips aus seinem Dump) und Junges (lage_E aus skelett_rig.json)."""

    def __init__(self, skelett_json=SKELETT):
        D = pickle.load(open(DUMP_ERW, "rb"))
        self.D = D
        self.names, self.par, self.idx = D["names"], D["par"], D["idx"]
        self.nb = len(self.names)
        J, _ = lade_json_glb()
        nodes = {n["name"]: n for n in J["nodes"]}
        self.t_e = np.zeros((self.nb, 3))
        self.R_loc = np.zeros((self.nb, 3, 3))
        for b, nm in enumerate(self.names):
            n = nodes[nm]
            self.t_e[b] = FZ @ np.array(n.get("translation", [0, 0, 0]), float)
            self.R_loc[b] = FZ @ quat_m(n.get("rotation", [0, 0, 0, 1])) @ FZ
        sk = json.load(open(skelett_json))
        assert sk["namen"] == self.names and sk["eltern"] == list(self.par)
        self.sk = sk
        self.t_j = np.array([sk["lage_E"][nm] for nm in self.names], float)
        self.dx = float(sk["dx_m"])
        self.BW_e = self.fk(self.t_e, self.R_loc)
        self.BW_j = self.fk(self.t_j, self.R_loc)
        ih, ihr = self.idx["Bip01_L_Thigh"], self.idx["Bip01_R_Thigh"]
        self.t_mitte_e = 0.5 * (self.t_e[ih] + self.t_e[ihr])
        self.t_mitte_j = 0.5 * (self.t_j[ih] + self.t_j[ihr])

    def fk(self, t_loc, R_loc):
        W = np.zeros((self.nb, 4, 4))
        for b in range(self.nb):
            T = np.eye(4)
            T[:3, :3] = R_loc[b]
            T[:3, 3] = t_loc[b]
            W[b] = T if self.par[b] < 0 else W[self.par[b]] @ T
        return W

    def clip_lokal_erw(self, clip, bild):
        Lk = self.D["clips"][clip]["L"][bild]
        t = self.t_e.copy()
        R = self.R_loc.copy()
        for b in range(self.nb):
            if b in Lk:
                t[b] = Lk[b][:3]
                R[b] = quat_m(Lk[b][3:7])
        return t, R

    def lokal_junges(self, clip, bild, dz=0.0):
        """Lokale Schluessel des Jungen (Drehungen des Erwachsenen, Lagen lage_E, Becken-Regel D.2 mit dx_m und Hub dz)."""
        t, R = self.clip_lokal_erw(clip, bild)
        Me = self.fk(t, R)
        ip, ib = self.idx["Bip01_Pelvis"], self.idx["Bip01"]
        hm = Me[ip][:3, 3] + Me[ip][:3, :3] @ self.t_mitte_e
        tj = self.t_j.copy()
        tj[ib] = t[ib]
        tj[self.idx["Translation_Data"]] = t[self.idx["Translation_Data"]]
        p = hm + dump(np.array((self.dx, 0.0, dz))) - Me[ip][:3, :3] @ self.t_mitte_j
        tj[ip] = np.linalg.solve(Me[ib][:3, :3], p - Me[ib][:3, 3])
        return tj, R


def acc_bytes(J, B, i):
    a = J["accessors"][i]
    v = J["bufferViews"][a["bufferView"]]
    k = NC[a["type"]]
    sz = np.dtype(CT[a["componentType"]]).itemsize
    s = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    st = v.get("byteStride", k * sz)
    if st == k * sz:
        return B[s:s + a["count"] * k * sz]
    return b"".join(B[s + j * st: s + j * st + k * sz] for j in range(a["count"]))


def acc_np(J, B, i):
    a = J["accessors"][i]
    return np.frombuffer(acc_bytes(J, B, i), dtype=CT[a["componentType"]]).reshape(a["count"], NC[a["type"]])


def normalen_verschweisst(V, T):
    """Glatte Normalen ueber die verschweissten Punkte (UV-Naehte bekommen dieselbe Normale)."""
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    acc = np.zeros_like(V)
    for k in range(3):
        np.add.at(acc, T[:, k], fn)
    vol = np.einsum("ij,ij->i", V[T[:, 0]], np.cross(V[T[:, 1]], V[T[:, 2]])).sum()
    if vol < 0:                      # Dreiecke nach innen gewickelt -> Normalen nach aussen drehen
        acc = -acc
    return acc / np.maximum(np.linalg.norm(acc, axis=1), 1e-12)[:, None]


def quat_folge(R):
    """Bilder x 3x3 -> Bilder x 4 (x, y, z, w), Vorzeichen fortlaufend."""
    Q = np.array([m_quat(r) for r in R])
    for i in range(1, len(Q)):
        if Q[i] @ Q[i - 1] < 0:
            Q[i] = -Q[i]
    return Q


def baue(netz, gewichte, aus, skelett=SKELETT, sitz=None, hub=None, abw=None, weg_bezug=WEG_BEZUG, name="NCBearCub", neu=None):
    N = np.load(netz)
    G = np.load(gewichte)
    J, B = lade_json_glb()
    sk = SkelettRig(skelett)
    names = sk.names
    node_of = {n["name"]: i for i, n in enumerate(J["nodes"])}
    joints = J["skins"][0]["joints"]
    assert [J["nodes"][k]["name"] for k in joints] == names, "Skin-Reihenfolge != Dump-Reihenfolge"
    # ---- Netz (verschweisste Punkte V, GLB-Punkte = Paare (Punkt, UV))
    V, T = N["V"].astype(np.float64), N["T"]
    pi, UV, F = N["glb_punkt"], N["UV"].astype(np.float64), N["T_glb"]
    assert (pi[F] == T).all(), "T_glb passt nicht zu T"
    W = G["W"].astype(np.float64)
    gn = [str(x) for x in G["namen"]]
    assert len(W) == len(V), (W.shape, V.shape)
    ordn = np.argsort(-W, axis=1)[:, :4]
    Wt = np.take_along_axis(W, ordn, 1)
    Wt = np.where(Wt < 1e-5, 0.0, Wt)
    Wt /= Wt.sum(1)[:, None]
    Bi = np.array([sk.idx[n] for n in gn])[ordn]
    Bi = np.where(Wt > 0, Bi, 0)
    Pd = dump(V)[pi]
    Nn = dump(normalen_verschweisst(V, T))[pi] / M2U
    Pg = (Pd * (1, 1, -1)).astype(np.float32)
    Ng = (Nn * (1, 1, -1)).astype(np.float32)
    Fg = F.copy()
    vol = np.einsum("ij,ij->i", Pg[Fg[:, 0]].astype(float), np.cross(Pg[Fg[:, 1]].astype(float), Pg[Fg[:, 2]].astype(float))).sum() / 6
    if vol < 0:
        Fg = Fg[:, ::-1]
    assert len(Pg) < 65536
    IB = np.array([F4 @ np.linalg.inv(m) @ F4 for m in sk.BW_j])
    prim = J["meshes"][0]["primitives"][0]
    fest = {prim["attributes"]["POSITION"]: Pg, prim["attributes"]["NORMAL"]: Ng, prim["attributes"]["TEXCOORD_0"]: UV.astype(np.float32),
            prim["attributes"]["JOINTS_0"]: Bi[pi].astype(np.uint8), prim["attributes"]["WEIGHTS_0"]: Wt[pi].astype(np.float32),
            prim["indices"]: Fg.reshape(-1, 1).astype(np.uint16),
            J["skins"][0]["inverseBindMatrices"]: np.array([m.T.reshape(-1) for m in IB], np.float32)}
    # ---- Clips
    S = dict(np.load(sitz)) if sitz else {}
    H = json.load(open(hub)) if hub else {}
    A = dict(np.load(abw)) if abw else {}
    NEU = dict(np.load(neu)) if neu else {}
    ip, itd = sk.idx["Bip01_Pelvis"], sk.idx["Translation_Data"]
    R_bip = sk.BW_j[sk.idx["Bip01"]][:3, :3]          # Bip01 steht in allen Clips in Ruhe (gemessen: Lage/Drehung = Ruhe in 15/15)
    WURZEL = ("Dummy01", "Bip01", "Translation_Data")
    t_g = {nm: (FZ @ sk.t_j[b]) for b, nm in enumerate(names)}
    J2 = json.loads(json.dumps(J))
    neu_acc = []
    info = dict(weg={}, becken={}, dreh_neu={}, dreh_gleich=0, dreh_alle=0)

    def neuer(vorlage, daten):
        neu_acc.append((vorlage, np.ascontiguousarray(daten)))
        return len(J["accessors"]) + len(neu_acc) - 1

    for ai, a in enumerate(J["animations"]):
        clip = a["name"]
        c = sk.D["clips"][clip]
        Tc = np.array(c["T"])
        dz = H.get(clip)
        a2 = J2["animations"][ai]
        # GJ2: dichtester Zeit-Accessor des Clips (der 2c hat fuer viele Kanaele nur 2 Schluessel, z. B. Eat/Sit Becken und Beine);
        # Kanaele, die hier neu Bild fuer Bild gerechnet werden, bekommen DIESEN (vorhandenen, byte-gleichen) Accessor
        dicht = max({s_["input"] for s_ in a["samplers"]}, key=lambda i_: J["accessors"][i_]["count"])
        for ci, ch in enumerate(a["channels"]):
            nm = J["nodes"][ch["target"]["node"]]["name"]
            if nm not in sk.idx:
                continue
            b = sk.idx[nm]
            smp = a["samplers"][ch["sampler"]]
            pfad = ch["target"]["path"]
            eingang = smp["input"]
            if ((pfad == "rotation" and (clip + "_R") in NEU and nm not in WURZEL) or
                    (pfad == "translation" and b == ip and (clip + "_pel") in NEU)):
                eingang = dicht                                                      # GJ2
            tz = acc_np(J, B, eingang).ravel()
            fr = np.array([int(np.argmin(np.abs(Tc - t_))) for t_ in tz])

            def setze(daten):
                s2 = dict(a2["samplers"][ch["sampler"]])
                s2["input"] = eingang                                                # GJ2
                s2["output"] = neuer(smp["output"], daten)
                a2["samplers"].append(s2)
                a2["channels"][ci]["sampler"] = len(a2["samplers"]) - 1
            if pfad == "translation":
                alt = acc_np(J, B, smp["output"]).astype(np.float64)
                if b == itd:
                    if (clip + "_weg") in NEU:
                        w_alt = float(np.abs(alt[-1]).max())
                        nv = alt * (float(NEU[clip + "_weg"]) / w_alt)
                    else:
                        nv = alt * weg_bezug
                    info["weg"][clip] = [round(float(np.abs(alt).max()), 5), round(float(np.abs(nv).max()), 5)]
                elif b == ip:
                    nv = np.zeros((len(fr), 3))                                      # GJ2: Bilder je Zeit-Accessor (dicht)
                    if (clip + "_pel") in NEU:
                        for k_, f_ in enumerate(fr):
                            nv[k_] = FZ @ (NEU[clip + "_pel"][f_] + R_bip.T @ dump(np.array((0.0, 0.0, dz[f_] if dz else 0.0))))
                    elif clip in SITZ_CLIPS and (clip + "_pel") in S:
                        for k_, f_ in enumerate(fr):
                            nv[k_] = FZ @ (S[clip + "_pel"][f_] + np.array((0.0, (dz[f_] if dz else 0.0) * M2U, 0.0)))
                    else:
                        for k_, f_ in enumerate(fr):
                            tj, _R = sk.lokal_junges(clip, f_, dz[f_] if dz else 0.0)
                            nv[k_] = FZ @ tj[ip]
                    info["becken"][clip] = [round(float(v), 5) for v in (nv.min(0).tolist() + nv.max(0).tolist())]
                else:
                    nv = np.repeat(t_g[nm][None, :], len(alt), 0)
                setze(nv.astype(np.float32))
            elif pfad == "rotation":
                info["dreh_alle"] += 1
                key = clip + "|" + nm
                if key in A:
                    qd = A[key][fr]
                    q = quat_folge(np.array([FZ @ quat_m(v) @ FZ for v in qd]))
                elif (clip + "_R") in NEU and nm not in WURZEL:
                    R = NEU[clip + "_R"][fr, b]
                    q = quat_folge(np.array([FZ @ r @ FZ for r in R]))
                elif clip in SITZ_CLIPS and (clip + "_R") in S:
                    R = S[clip + "_R"][fr, b]
                    q = quat_folge(np.array([FZ @ r @ FZ for r in R]))
                elif key in A:
                    qd = A[key][fr]
                    q = quat_folge(np.array([FZ @ quat_m(v) @ FZ for v in qd]))
                else:
                    info["dreh_gleich"] += 1
                    continue
                alt = acc_np(J, B, smp["output"]).astype(np.float64)
                if q[0] @ alt[0] < 0:
                    q = -q
                if len(alt) == len(q):                                               # GJ2: bei verdichtetem Kanal kein Vergleich je Bild
                    info["dreh_neu"].setdefault(clip, {})[nm] = round(float(np.degrees(2 * np.arccos(np.clip(np.abs((q * alt).sum(1)), 0, 1))).max()), 2)
                else:
                    info["dreh_neu"].setdefault(clip, {})[nm] = "verdichtet %d->%d" % (len(alt), len(q))
                setze(q.astype(np.float32))
    # ---- JSON anpassen
    for nm in names:
        n = J2["nodes"][node_of[nm]]
        if np.abs(t_g[nm]).max() > 0 or "translation" in n:
            n["translation"] = [float(v) for v in t_g[nm]]
    for n in J2["nodes"]:
        if n.get("mesh") == 0:
            n["name"] = name
    J2["meshes"][0]["name"] = name
    for vorlage, daten in neu_acc:
        acc = dict(J["accessors"][vorlage])
        acc["count"] = int(daten.shape[0])
        acc.pop("min", None)
        acc.pop("max", None)
        J2["accessors"].append(acc)
    for k, arr in fest.items():
        J2["accessors"][k]["count"] = int(arr.shape[0])
        if "min" in J2["accessors"][k]:
            J2["accessors"][k]["min"] = arr.min(0).astype(float).tolist()
            J2["accessors"][k]["max"] = arr.max(0).astype(float).tolist()
    daten_von = dict(fest)
    for i, (vorlage, daten) in enumerate(neu_acc):
        daten_von[len(J["accessors"]) + i] = daten
    benutzt = set(prim["attributes"].values()) | {prim["indices"], J["skins"][0]["inverseBindMatrices"]}
    for a2 in J2["animations"]:
        kan = {ch["sampler"] for ch in a2["channels"]}
        neu_s, karte = [], {}
        for si, s2 in enumerate(a2["samplers"]):
            if si in kan:
                karte[si] = len(neu_s)
                neu_s.append(s2)
        for ch in a2["channels"]:
            ch["sampler"] = karte[ch["sampler"]]
        a2["samplers"] = neu_s
        for s2 in neu_s:
            benutzt |= {s2["input"], s2["output"]}
    ordn_a = sorted(benutzt)
    um = {alt_i: neu_i for neu_i, alt_i in enumerate(ordn_a)}
    bin_ = bytearray()
    views, accs = [], []
    for alt_i in ordn_a:
        a_ = dict(J2["accessors"][alt_i])
        if alt_i in daten_von:
            data = np.ascontiguousarray(daten_von[alt_i].astype(CT[a_["componentType"]])).tobytes()
            v_alt = J["bufferViews"][J["accessors"][alt_i]["bufferView"]] if alt_i < len(J["accessors"]) else {}
        else:
            data = acc_bytes(J, B, alt_i)
            v_alt = J["bufferViews"][J["accessors"][alt_i]["bufferView"]]
        while len(bin_) % 4:
            bin_ += b"\0"
        v = {"buffer": 0, "byteOffset": len(bin_), "byteLength": len(data)}
        if "target" in v_alt:
            v["target"] = v_alt["target"]
        views.append(v)
        a_["bufferView"] = len(views) - 1
        a_.pop("byteOffset", None)
        accs.append(a_)
        bin_ += data
    while len(bin_) % 4:
        bin_ += b"\0"
    for k in prim["attributes"]:
        J2["meshes"][0]["primitives"][0]["attributes"][k] = um[prim["attributes"][k]]
    J2["meshes"][0]["primitives"][0]["indices"] = um[prim["indices"]]
    J2["skins"][0]["inverseBindMatrices"] = um[J["skins"][0]["inverseBindMatrices"]]
    for a2 in J2["animations"]:
        for s2 in a2["samplers"]:
            s2["input"], s2["output"] = um[s2["input"]], um[s2["output"]]
    J2["accessors"] = accs
    J2["bufferViews"] = views
    J2["buffers"] = [{"byteLength": len(bin_)}]
    J2["asset"]["generator"] = "baer_export_gj2.py (Lauf baer-gen-junges-v2, Gerippe NCBear.glb 08ec7806)"   # GJ2
    js = json.dumps(J2, separators=(",", ":")).encode()
    while len(js) % 4:
        js += b" "
    out = b"glTF" + struct.pack("<II", 2, 12 + 8 + len(js) + 8 + len(bin_))
    out += struct.pack("<I", len(js)) + b"JSON" + js + struct.pack("<I", len(bin_)) + b"BIN\0" + bytes(bin_)
    open(aus, "wb").write(out)
    print("EXPORT", aus, "GLB-Punkte", len(Pg), "Netz-Punkte", len(V), "Dreiecke", len(Fg), "Bytes", len(out), "Accessoren", len(accs))
    print("EXPORT Dreh-Kanaele byte-gleich mit dem Erwachsenen:", info["dreh_gleich"], "von", info["dreh_alle"], "| neu:", {k: len(v) for k, v in info["dreh_neu"].items()})
    print("EXPORT Translation_Data (WEG_BEZUG %.3f) max |Lage| Erwachsener -> Junges:" % weg_bezug, {k: v for k, v in info["weg"].items() if v[0] > 0})
    print("EXPORT Skelett", skelett, "| Neu", neu, "| Sitz", sitz, "| Hub", hub, "| Abweichungen", abw)
    return info


if __name__ == "__main__":
    kw = dict(a.split("=", 1) for a in sys.argv[4:])
    baue(sys.argv[1], sys.argv[2], sys.argv[3], **kw)
