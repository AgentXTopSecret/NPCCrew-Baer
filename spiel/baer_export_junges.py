# Lauf baer-junges (10.11.2026), Bau Koerper: GLB des Baeren-Jungen NCBearCub aus dem Spielnetz des Jungen (baer_form_junges.py).
# Reines Python/numpy, kein Blender-Export. Weg wie baer_export_baby.py (Lauf baer-baby): das GLB des ERWACHSENEN Stand 2c
# (eingang/NCBear.glb, MD5 08ec7806, nur gelesen) dient als Gerippe -- gleiche 28 Knoten, gleiche Knochen-Reihenfolge/Namen/Eltern,
# Skin-Joints, Knoten-Drehungen; getauscht werden nur Puffer:
#   - Netz: POSITION/NORMAL/TEXCOORD_0/JOINTS_0 (u8)/WEIGHTS_0, Indizes u16; ein Netz, ein Primitiv, kein Material
#   - inverse Bind = Ruhe des Jungen (Skelett SPEZ_JUNGES B.5: Beine/Pfoten 1,0, Rumpf 0,85, Hals 1,0, Kiefergelenk 1,2)
#   - 15 Clips: Zeiten und Skalier-Schluessel BYTE-GLEICH; Dreh-Schluessel der 12 Nicht-Sitz-Clips BYTE-GLEICH (ausser den
#     Abweichungen aus ABW.npz, SPEZ D.5); Lage-Schluessel neu: konstant = Lage des Jungen (B.5), Bip01_Pelvis je Bild nach der
#     Becken-Regel D.2 (Hueftmitte = Hueftmitte des Erwachsenen + DX + Hub dz), Translation_Data = Erwachsener x WEG_BEZUG (D.6)
#   - NCBear_SitDown / _Sit / _StandUp: Dreh-Schluessel und Becken-Lage aus SITZ.npz (baer_kampf_junges.py: die parametrischen
#     Sitz-Spuren von 2c mit den Gelenken des Jungen, an denselben Zeiten abgetastet)
# Aufruf: python baer_export_junges.py NETZ.npz GEWICHTE.npz AUS.glb [sitz=SITZ.npz] [hub=HUB.json] [abw=ABW.npz] [kopf=NPZ]
#   NETZ.npz      koerper/lp_junges.npz (V tier-Meter, T, UVT je Ecke) oder ein Endnetz mit denselben Feldern
#   GEWICHTE.npz  W (n x k), namen (k Knochen) -- eingang/gewichte_2c.npz (Start) oder koerper/gewichte_junges.npz
#   HUB.json      {Clip: [dz je Bild in Metern]} (Becken-Hub, an der Haut geloest: baer_boden_junges / werkzeug/kj_hub.py)
#   ABW.npz       {"<Clip>|<Knochen>": Bilder x 4 Quaternion lokal (Dump-Raum, x y z w)} -- ersetzt den Dreh-Schluessel
# Statisch/offline, nicht gespielt. Weder Test-Mod noch NPC Crew werden gelesen oder beschrieben.
import json
import struct
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_form_junges as fj  # noqa: E402

CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
F4 = np.diag([1.0, 1.0, -1.0, 1.0])
FZ = fj.FZ
# SPEZ D.6: Weg je Schritt = Erwachsener x Bein-Faktor (1,000) x Bezugsgroesse. Die Bewegung kennt die Groesse nicht
# (_arbeit/baer_spiel/dec/AnimationPlayer.java:1203-1240); der Code-Lauf setzt minSize = maxSize = 0,35. EINE Konstante.
WEG_BEZUG = 0.35
SITZ_CLIPS = ("NCBear_SitDown", "NCBear_Sit", "NCBear_StandUp")


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


def normalen(P, F):
    """Glatte Normalen ueber verschweisste Lagen (UV-Naehte bekommen dieselbe Normale)."""
    key = np.round(P, 7)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    acc = np.zeros((wid.max() + 1, 3))
    for k in range(3):
        np.add.at(acc, wid[F[:, k]], fn)
    N = acc[wid]
    return N / np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]


def netz_ecken(V, T, UVT):
    """Punkte an UV-Naehten teilen: je (Punkt, UV) ein GLB-Punkt. Rueckgabe: Punkt-Index je GLB-Punkt, UV, Dreiecke."""
    ecke = np.concatenate((np.repeat(T.reshape(-1, 1), 1, 1), np.round(UVT.reshape(-1, 2), 6)), 1)
    u, inv = np.unique(ecke, axis=0, return_inverse=True)
    return u[:, 0].astype(int), u[:, 1:3], inv.reshape(-1, 3)


def quat_folge(R):
    """Bilder x 3x3 -> Bilder x 4 (x, y, z, w), Vorzeichen fortlaufend."""
    Q = np.array([fj.m_quat(r) for r in R])
    for i in range(1, len(Q)):
        if Q[i] @ Q[i - 1] < 0:
            Q[i] = -Q[i]
    return Q


def baue(netz, gewichte, aus, sitz=None, hub=None, abw=None, weg_bezug=WEG_BEZUG, name="NCBearCub"):
    N = np.load(netz)
    G = np.load(gewichte)
    J, B = fj.lade_json_glb()
    sk = fj.Skelett()
    names = sk.names
    node_of = {n["name"]: i for i, n in enumerate(J["nodes"])}
    joints = J["skins"][0]["joints"]
    assert [J["nodes"][k]["name"] for k in joints] == names, "Skin-Reihenfolge != Dump-Reihenfolge"
    # ---- Netz
    V, T, UVT = N["V"], N["T"], N["UVT"]
    W = G["W"].astype(np.float64)
    gn = [str(x) for x in G["namen"]]
    assert len(W) == len(V), (W.shape, V.shape)
    pi, UV, F = netz_ecken(V, T, UVT)
    UV = np.c_[UV[:, 0], 1.0 - UV[:, 1]]          # glTF: v von oben (gegen eingang/NCBear.glb geprueft: 669 Ecken, Fehler 3e-8)
    # hoechstens 4 Einfluesse, Summe 1
    ordn = np.argsort(-W, axis=1)[:, :4]
    Wt = np.take_along_axis(W, ordn, 1)
    Wt = np.where(Wt < 1e-5, 0.0, Wt)
    Wt /= Wt.sum(1)[:, None]
    Bi = np.array([sk.idx[n] for n in gn])[ordn]
    Bi = np.where(Wt > 0, Bi, 0)
    Pd = fj.dump(V)[pi]
    Nn = normalen(Pd, F)
    Pg = (Pd * (1, 1, -1)).astype(np.float32)
    Ng = (Nn * (1, 1, -1)).astype(np.float32)
    Fg = F[:, ::-1]
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
    ip, itd = sk.idx["Bip01_Pelvis"], sk.idx["Translation_Data"]
    t_g = {nm: (FZ @ sk.t_j[b]) for b, nm in enumerate(names)}
    J2 = json.loads(json.dumps(J))
    neu_acc = []          # (Vorlage-Accessor, Daten)
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
        for ci, ch in enumerate(a["channels"]):
            nm = J["nodes"][ch["target"]["node"]]["name"]
            if nm not in sk.idx:
                continue
            b = sk.idx[nm]
            smp = a["samplers"][ch["sampler"]]
            tz = acc_np(J, B, smp["input"]).ravel()
            fr = np.array([int(np.argmin(np.abs(Tc - t_))) for t_ in tz])
            pfad = ch["target"]["path"]
            # jeder Kanal bekommt einen eigenen Sampler-Ausgang, wenn er geaendert wird (die Vorlage teilt Ausgaenge)
            def setze(daten):
                s2 = dict(a2["samplers"][ch["sampler"]])
                s2["output"] = neuer(smp["output"], daten)
                a2["samplers"].append(s2)
                a2["channels"][ci]["sampler"] = len(a2["samplers"]) - 1
            if pfad == "translation":
                alt = acc_np(J, B, smp["output"]).astype(np.float64)
                if b == itd:
                    nv = alt * weg_bezug
                    info["weg"][clip] = [round(float(np.abs(alt).max()), 5), round(float(np.abs(nv).max()), 5)]
                elif b == ip:
                    nv = np.zeros_like(alt)
                    if clip in SITZ_CLIPS and (clip + "_pel") in S:
                        for k_, f_ in enumerate(fr):
                            nv[k_] = FZ @ (S[clip + "_pel"][f_] + (np.array((0.0, (dz[f_] if dz else 0.0) * fj.M2U, 0.0))))
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
                if clip in SITZ_CLIPS and (clip + "_R") in S:
                    R = S[clip + "_R"][fr, b]
                    q = quat_folge(np.array([FZ @ r @ FZ for r in R]))
                elif key in A:
                    qd = A[key][fr]                                   # Dump-Raum (x, y, z, w)
                    q = quat_folge(np.array([FZ @ fj.quat_m(v) @ FZ for v in qd]))
                else:
                    info["dreh_gleich"] += 1
                    continue
                alt = acc_np(J, B, smp["output"]).astype(np.float64)
                if q[0] @ alt[0] < 0:
                    q = -q
                info["dreh_neu"].setdefault(clip, {})[nm] = round(float(np.degrees(2 * np.arccos(np.clip(np.abs((q * alt).sum(1)), 0, 1))).max()), 2)
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
    # benutzte Accessoren sammeln und neu nummerieren (die Vorlage-Ausgaenge der ersetzten Kanaele fallen weg)
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
    J2["asset"]["generator"] = "baer_export_junges.py (Lauf baer-junges, Gerippe NCBear.glb 08ec7806)"
    js = json.dumps(J2, separators=(",", ":")).encode()
    while len(js) % 4:
        js += b" "
    out = b"glTF" + struct.pack("<II", 2, 12 + 8 + len(js) + 8 + len(bin_))
    out += struct.pack("<I", len(js)) + b"JSON" + js + struct.pack("<I", len(bin_)) + b"BIN\0" + bytes(bin_)
    open(aus, "wb").write(out)
    print("EXPORT", aus, "GLB-Punkte", len(Pg), "Netz-Punkte", len(V), "Dreiecke", len(Fg), "Bytes", len(out), "Accessoren", len(accs))
    print("EXPORT Dreh-Kanaele byte-gleich mit dem Erwachsenen:", info["dreh_gleich"], "von", info["dreh_alle"], "| neu:", {k: len(v) for k, v in info["dreh_neu"].items()})
    for k, v in info["dreh_neu"].items():
        print("EXPORT   Dreh neu", k, "groesste Abweichung je Knochen (Grad):", {n.replace("Bip01_", ""): w for n, w in v.items() if w > 0.01})
    print("EXPORT Translation_Data (WEG_BEZUG %.3f) max |Lage| Erwachsener -> Junges:" % weg_bezug, {k: v for k, v in info["weg"].items() if v[0] > 0})
    print("EXPORT Sitz-Clips aus", sitz, "| Hub aus", hub, "| Abweichungen aus", abw)
    return info


if __name__ == "__main__":
    kw = dict(a.split("=", 1) for a in sys.argv[4:])
    baue(sys.argv[1], sys.argv[2], sys.argv[3], **kw)
