# Lauf baer-baby (10.11.2026): GLB-Entwurf NCBearCub.glb aus dem Netz des Jungen (baer_netz_baby.py) -- reines Python/numpy, kein
# Blender-Export: die GLB des Erwachsenen (NCBearTest NCBear.glb MD5 5066fa67, nur gelesen) dient als Gerippe.
#   - gleiche 28 Knoten, gleiche Knochen-Reihenfolge/Namen/Eltern (Skin-Joints unveraendert), Knoten-Drehung/-Skalierung unveraendert,
#     Knoten-Lage = Lage des Jungen (baer_form_baby.Junges, Dump -> glTF: z gespiegelt)
#   - 15 Clips (SPEZ 3.3 c): Zeiten, Dreh- und Skalier-Schluessel BYTE-GLEICH kopiert; Lage-Schluessel neu: konstant = Lage des Jungen,
#     Bip01_Pelvis / Bip01 / Translation_Data = Schluessel des Erwachsenen mal diag(S_eltern) (Becken-Hub/-Senken, Weg)
#   - ein Netz, ein Primitiv, POSITION/NORMAL/TEXCOORD_0/JOINTS_0 (u8)/WEIGHTS_0, Indizes u16 (wie der Erwachsene), kein Material
# Aufruf: python baer_export_baby.py NETZ.npz AUS.glb
# Statisch/offline, nicht gespielt. Weder Test-Mod noch NPC Crew werden beschrieben.
import json
import struct
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_form_baby as bf  # noqa: E402

CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
F4 = np.diag([1.0, 1.0, -1.0, 1.0])
BODEN = True     # Bodenausgleich je Bild ueber die Becken-Lage (SPEZ 3.3 Punkt 4)
# fix1 (Befund 'Becken-Hub'): Bodenausgleich zeitlich glaetten (Fenster +-BODEN_GLATT Bilder, bei Schleifen-Clips zyklisch), damit
# das Junge mit kuerzeren Beinen nicht huepft; Bodenfehler bleibt <= 1,5 cm (log/export).
BODEN_GLATT = 2
SCHLEIFEN = ("DeerStag_Walk", "DeerStag_Run", "DeerStag_Idle01", "NCBear_Eat")
# fix1 (Befund M5 'Translation_Data x0,777'): Weg je Zyklus. "eltern" = Schluessel des Erwachsenen x diag(S_eltern) (heute: Faktor FH
# 0,777 auf der Laufachse = so weit, wie die kuerzeren Beine tragen); eine Zahl = gleichmaessiger Faktor (1.0 = Weg des Erwachsenen).
# KEVINS WORT in B1 (SPEZ 3.3 Punkt 4): bis dahin bleibt "eltern".
WEG_FAKTOR = "eltern"


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
    key = np.round(P, 7)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    acc = np.zeros((wid.max() + 1, 3))
    for k in range(3):
        np.add.at(acc, wid[F[:, k]], fn)
    N = acc[wid]
    return N / np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]


def main(netz, aus):
    N = np.load(netz)
    J, B = bf.lade_json_glb()
    E, Jg = bf.junges_standard()
    assert np.abs(Jg.BW - N["BW"]).max() < 1e-9
    names = E.names
    node_of = {n["name"]: i for i, n in enumerate(J["nodes"])}
    joints = J["skins"][0]["joints"]
    assert [J["nodes"][k]["name"] for k in joints] == names, "Skin-Reihenfolge != Dump-Reihenfolge"
    # ---- Netz
    P = N["P"]
    F = N["F"]
    Wt = N["Wt"].astype(np.float64)
    Bi = N["Bi"].astype(int)
    Wt = np.where(Wt < 1e-6, 0.0, Wt)
    Wt /= Wt.sum(1)[:, None]
    Bi = np.where(Wt > 0, Bi, 0)
    Nn = normalen(P, F)
    Pg = (P * (1, 1, -1)).astype(np.float32)
    Ng = (Nn * (1, 1, -1)).astype(np.float32)
    UV = N["UV"].astype(np.float32)
    Fg = F[:, ::-1].astype(np.uint16)
    assert len(P) < 65536
    vol = np.einsum("ij,ij->i", Pg[Fg[:, 0]].astype(float), np.cross(Pg[Fg[:, 1]].astype(float), Pg[Fg[:, 2]].astype(float))).sum() / 6
    assert vol > 0, vol
    # ---- inverse Bind (glTF: F4 inv(BW_dump) F4), spaltenweise
    IB = np.array([F4 @ np.linalg.inv(m) @ F4 for m in Jg.BW])
    # ---- neue Puffer
    neu = {}
    prim = J["meshes"][0]["primitives"][0]
    neu[prim["attributes"]["POSITION"]] = Pg
    neu[prim["attributes"]["NORMAL"]] = Ng
    neu[prim["attributes"]["TEXCOORD_0"]] = UV
    neu[prim["attributes"]["JOINTS_0"]] = Bi.astype(np.uint8)
    neu[prim["attributes"]["WEIGHTS_0"]] = Wt.astype(np.float32)
    neu[prim["indices"]] = Fg.reshape(-1, 1)
    neu[J["skins"][0]["inverseBindMatrices"]] = np.array([m.T.reshape(-1) for m in IB], np.float32)
    t_g = {nm: (bf.FZ @ Jg.t_loc[b]) for b, nm in enumerate(names)}
    S = Jg.S * Jg.U
    bewegt = {"Bip01_Pelvis", "Bip01", "Translation_Data"}
    lage_info = {}
    weg_info = {}
    boden_fehler = {}
    # Bodenausgleich je Bild (SPEZ 3.3 Punkt 4): Becken-Lage so verschieben, dass der tiefste Punkt des Jungen auf der Hoehe des
    # tiefsten Punkts des Erwachsenen im selben Bild liegt (Stuetzpfote/Rumpf auf dem Boden, nichts im Boden).
    inv_bind = np.array([np.linalg.inv(m) for m in Jg.BW])
    ip, ib = E.idx["Bip01_Pelvis"], E.idx["Bip01"]
    boden = {}
    for clip, c in E.D["clips"].items():
        dz = []
        for fr in range(len(c["T"])):
            Mj = Jg.welt(clip, fr)
            zj = bf.tier(bf.haut(Mj, inv_bind, P, Wt, Bi))[:, 2].min()
            ze = bf.tier(bf.haut(c["M"][fr], E.off, E.P, E.Wt, E.Bi))[:, 2].min()
            d_dump = bf.dump(np.array((0.0, 0.0, ze - zj)))
            dz.append((float(ze - zj), Mj[ib][:3, :3].T @ d_dump))
        boden[clip] = (np.array(c["T"]), dz)
    boden_info = {k: [round(min(d for d, _ in v[1]) * 100, 2), round(max(d for d, _ in v[1]) * 100, 2)] for k, v in boden.items()}
    if BODEN_GLATT > 0:
        for clip in boden:
            if clip not in SCHLEIFEN:      # nur Schleifen (Gang/Lauf/Stand/Fressen); Einzel-Clips behalten den exakten Ausgleich
                continue
            T_, dz = boden[clip]
            n_ = len(dz)
            vec = np.array([d_[1] for d_ in dz])
            sk = np.array([d_[0] for d_ in dz])
            idx = np.arange(-BODEN_GLATT, BODEN_GLATT + 1)
            gew = 1.0 + BODEN_GLATT - np.abs(idx)
            if clip in SCHLEIFEN and n_ > 2 * BODEN_GLATT + 1:
                # letztes Bild = erstes Bild bei Schleifen: zyklisch ueber n_-1 Bilder
                m_ = n_ - 1
                vg = np.array([sum(w_ * vec[(i + k_) % m_] for k_, w_ in zip(idx, gew)) / gew.sum() for i in range(m_)] + [None], dtype=object)
                vg[-1] = vg[0]
                sg = np.array([sum(w_ * sk[(i + k_) % m_] for k_, w_ in zip(idx, gew)) / gew.sum() for i in range(m_)] + [0.0])
                sg[-1] = sg[0]
            else:
                vg = np.array([sum(w_ * vec[min(max(i + k_, 0), n_ - 1)] for k_, w_ in zip(idx, gew)) / gew.sum() for i in range(n_)] + [None], dtype=object)[:-1]
                sg = np.array([sum(w_ * sk[min(max(i + k_, 0), n_ - 1)] for k_, w_ in zip(idx, gew)) / gew.sum() for i in range(n_)])
            boden_fehler[clip] = round(float(np.abs(sg - sk).max() * 100), 2)
            boden[clip] = (T_, [(float(sg[i]), vg[i]) for i in range(n_)])
    for a in J["animations"]:
        for ch in a["channels"]:
            if ch["target"]["path"] != "translation":
                continue
            nm = J["nodes"][ch["target"]["node"]]["name"]
            if nm not in names:
                continue
            smp = a["samplers"][ch["sampler"]]
            alt = acc_np(J, B, smp["output"]).astype(np.float64)
            b = E.idx[nm]
            if nm in bewegt:
                p = E.par[b]
                s = S[p] if p >= 0 else np.ones(3)
                if nm == "Translation_Data" and WEG_FAKTOR != "eltern":
                    s = np.full(3, float(WEG_FAKTOR))
                nv = alt * s[None, :]
                if nm == "Translation_Data":
                    weg_info[a["name"]] = [round(float(np.abs(alt).max()), 4), round(float(np.abs(nv).max()), 4)]
                if nm == "Bip01_Pelvis" and BODEN:
                    tz = acc_np(J, B, smp["input"]).ravel()
                    T_, dz = boden[a["name"]]
                    for k_, t_ in enumerate(tz):
                        fr = int(np.argmin(np.abs(T_ - t_)))
                        nv[k_] += bf.FZ @ dz[fr][1]
            else:
                nv = np.repeat(t_g[nm][None, :], len(alt), 0)
                lage_info.setdefault(nm, float(np.abs(alt - alt[0]).max()))
            neu[smp["output"]] = nv.astype(np.float32)
    # ---- JSON anpassen
    J2 = json.loads(json.dumps(J))
    for nm in names:
        n = J2["nodes"][node_of[nm]]
        if np.abs(t_g[nm]).max() > 0 or "translation" in n:
            n["translation"] = [float(v) for v in t_g[nm]]
    for n in J2["nodes"]:
        if n.get("mesh") == 0:
            n["name"] = "NCBearCub"
    J2["meshes"][0]["name"] = "NCBearCub"
    pa = J2["accessors"][prim["attributes"]["POSITION"]]
    pa["min"] = Pg.min(0).astype(float).tolist()
    pa["max"] = Pg.max(0).astype(float).tolist()
    for k, arr in neu.items():
        J2["accessors"][k]["count"] = int(arr.shape[0])
        if "min" in J2["accessors"][k] and k != prim["attributes"]["POSITION"]:
            J2["accessors"][k]["min"] = arr.min(0).astype(float).tolist()
            J2["accessors"][k]["max"] = arr.max(0).astype(float).tolist()
    # Puffer neu packen: je Accessor eine eigene BufferView (4-Byte-ausgerichtet), Ziele wie bisher
    bin_ = bytearray()
    views = []
    for i, a in enumerate(J2["accessors"]):
        if i in neu:
            data = np.ascontiguousarray(neu[i].astype(CT[a["componentType"]])).tobytes()
        else:
            data = acc_bytes(J, B, i)
        while len(bin_) % 4:
            bin_ += b"\0"
        v_alt = J["bufferViews"][J["accessors"][i]["bufferView"]]
        v = {"buffer": 0, "byteOffset": len(bin_), "byteLength": len(data)}
        if "target" in v_alt:
            v["target"] = v_alt["target"]
        views.append(v)
        a["bufferView"] = i
        a.pop("byteOffset", None)
        bin_ += data
    while len(bin_) % 4:
        bin_ += b"\0"
    J2["bufferViews"] = views
    J2["buffers"] = [{"byteLength": len(bin_)}]
    J2["asset"]["generator"] = "baer_export_baby.py (Lauf baer-baby, Gerippe NCBear.glb 5066fa67)"
    js = json.dumps(J2, separators=(",", ":")).encode()
    while len(js) % 4:
        js += b" "
    out = b"glTF" + struct.pack("<II", 2, 12 + 8 + len(js) + 8 + len(bin_))
    out += struct.pack("<I", len(js)) + b"JSON" + js + struct.pack("<I", len(bin_)) + b"BIN\0" + bytes(bin_)
    open(aus, "wb").write(out)
    # Selbstpruefung: Dreh-/Skalier-/Zeit-Schluessel byte-gleich
    gleich = 0
    alle = 0
    for a_alt, a_neu in zip(J["animations"], J2["animations"]):
        for ch, ch2 in zip(a_alt["channels"], a_neu["channels"]):
            s1, s2 = a_alt["samplers"][ch["sampler"]], a_neu["samplers"][ch2["sampler"]]
            if ch["target"]["path"] in ("rotation", "scale"):
                alle += 2
                gleich += acc_bytes(J, B, s1["output"]) == np.ascontiguousarray(neu.get(s2["output"], acc_np(J, B, s1["output"]))).tobytes()
                gleich += acc_bytes(J, B, s1["input"]) == acc_bytes(J, B, s2["input"])
    print("EXPORT", aus, "Punkte", len(Pg), "Dreiecke", len(Fg), "Bytes", len(out), "Dreh/Skal/Zeit byte-gleich", gleich, "/", alle)
    print("EXPORT Lage-Schluessel Erwachsener max. Schwankung (sonst konstant):", {k: round(v, 6) for k, v in lage_info.items() if v > 1e-6})
    print("EXPORT Bodenausgleich Becken je Clip (cm, min/max):", boden_info if BODEN else "aus")
    print("EXPORT Bodenausgleich geglaettet (+-%d Bilder): groesster Bodenfehler je Clip (cm):" % BODEN_GLATT, boden_fehler)
    print("EXPORT Translation_Data (WEG_FAKTOR=%s) max |Lage| Erwachsener -> Junges je Clip:" % WEG_FAKTOR, weg_info)
    return J2


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
