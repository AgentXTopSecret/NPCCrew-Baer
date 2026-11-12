# Lauf baer-junges-fuss (11.11.2026 nachts), Bauer CLIPS: GLB des alten Jungen mit neuem Netz (Beine/Fuesse vom 2c, Kopf bit-gleich)
# und neuen Sitz-Clips. Kopie/Abwandlung von baer_export_baby.py (Original unveraendert). Reines Python/numpy, kein Blender.
#   Gerippe = das HEUTIGE Junge quelle/cub/NCBearCub.glb (6c3f0a96): Knoten, Skin-Joints, inverse Bind, alle Clips bleiben, wie sie sind.
#   Neu sind nur (PLAN_JFUSS.md 5.3):
#     - die Netz-Puffer POSITION/NORMAL/TEXCOORD_0/JOINTS_0/WEIGHTS_0/Indizes (aus form/jfuss.npz, Gewichte wahlweise aus --gewichte)
#     - in NCBear_SitDown/_Sit/_StandUp die Dreh- und Lage-Schluessel, die baer_sitz_jfuss.py geaendert hat; fuer jeden geaenderten Kanal
#       ein NEUER Accessor (geteilte Accessoren anderer Clips werden nie ueberschrieben), Zeit-Accessoren und Skalier-Schluessel wie heute.
#   Alle anderen Accessoren werden als Bytes kopiert (je Accessor eine BufferView, 4-Byte-ausgerichtet, wie baer_export_baby.py).
# Aufruf: python baer_export_jfuss.py --netz N.npz --sitz S.npz --aus A.glb [--gewichte G.npz] [--gerippe J.glb]
# Selbstpruefung am Ende (Byte-Vergleich je Sampler der 12 anderen Clips, Knoten, Skin). Statisch/offline, nicht gespielt.
import argparse
import hashlib
import json
import struct
import sys

import numpy as np

sys.path.insert(0, r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel")
import baer_sitz_jfuss as bs  # noqa: E402

CT = bs.CT
NC = bs.NC
SITZ = bs.SITZ


def normalen(P, F):
    """wie baer_export_baby.normalen (Flaechennormalen ueber gleiche Lagen gemittelt)."""
    key = np.round(P, 7)
    _, wid = np.unique(key, axis=0, return_inverse=True)
    wid = wid.ravel()
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    acc = np.zeros((wid.max() + 1, 3))
    for k in range(3):
        np.add.at(acc, wid[F[:, k]], fn)
    N = acc[wid]
    return N / np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gerippe", default=bs.JUNGES_STD)
    ap.add_argument("--netz", default=bs.NETZ_STD)
    ap.add_argument("--gewichte", default=None)
    ap.add_argument("--sitz", required=True)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--alte_behalten", action="store_true",
                    help="fix1 (T7): nicht mehr benutzte alte Sitz-Ausgaben im Puffer lassen (wie vor fix1); Vorgabe: weglassen")
    a = ap.parse_args()
    J, B = bs.lade_glb(a.gerippe)
    N = np.load(a.netz)
    S = np.load(a.sitz)
    joints = J["skins"][0]["joints"]
    names = [J["nodes"][k]["name"] for k in joints]
    assert [str(x) for x in S["names"]] == names, "Knochen Sitz-Clips != Gerippe"
    # ---- Netz (wie baer_export_baby.main)
    P = N["P"].astype(np.float64)
    F = N["F"]
    if a.gewichte:
        Gz = np.load(a.gewichte)
        Wt, Bi = Gz["Wt"].astype(np.float64), Gz["Bi"].astype(int)
        assert Wt.shape == N["Wt"].shape
    else:
        Wt, Bi = N["Wt"].astype(np.float64), N["Bi"].astype(int)
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
    neu = {}
    prim = J["meshes"][0]["primitives"][0]
    neu[prim["attributes"]["POSITION"]] = Pg
    neu[prim["attributes"]["NORMAL"]] = Ng
    neu[prim["attributes"]["TEXCOORD_0"]] = UV
    neu[prim["attributes"]["JOINTS_0"]] = Bi.astype(np.uint8)
    neu[prim["attributes"]["WEIGHTS_0"]] = Wt.astype(np.float32)
    neu[prim["indices"]] = Fg.reshape(-1, 1)
    # ---- Sitz-Clips: geaenderte Kanaele bekommen neue Accessoren (angehaengt)
    J2 = json.loads(json.dumps(J))
    anh = []          # (accessor-JSON, Daten)
    n_acc = len(J["accessors"])
    info = {}
    G = bs.Gerippe(a.gerippe)
    for ai, an in enumerate(J2["animations"]):
        nm = an["name"]
        if nm not in SITZ:
            continue
        T = S[nm + "__T"]
        t_neu = S[nm + "__t"]
        q_neu = S[nm + "__q"]
        Tg, ia_N = G.zeiten(nm)
        assert len(Tg) == len(T) and np.array_equal(Tg, T), nm
        t_alt, q_alt, _ = G.werte(nm, Tg)
        geteilt = {}
        for ch in an["channels"]:
            geteilt[ch["sampler"]] = geteilt.get(ch["sampler"], 0) + 1
        assert max(geteilt.values()) == 1, "Sampler zwischen Kanaelen geteilt"
        ni = {"rotation": 0, "translation": 0, "gleich": 0}
        for ch in an["channels"]:
            path = ch["target"]["path"]
            bn = J["nodes"][ch["target"]["node"]]["name"]
            if path not in ("rotation", "translation") or bn not in names:
                continue
            b = names.index(bn)
            if path == "rotation":
                v = q_neu[:, b].astype(np.float32)
                alt = q_alt[:, b].astype(np.float32)
            else:
                v = t_neu[:, b].astype(np.float32)
                alt = t_alt[:, b].astype(np.float32)
            if np.array_equal(v, alt):
                ni["gleich"] += 1
                continue                                          # Kanal unveraendert: Sampler und Accessoren bleiben
            idx = n_acc + len(anh)
            anh.append(({"componentType": 5126, "count": int(len(v)), "type": "VEC4" if path == "rotation" else "VEC3"},
                        np.ascontiguousarray(v)))
            smp = an["samplers"][ch["sampler"]]
            smp["input"] = int(ia_N)
            smp["output"] = int(idx)
            smp["interpolation"] = "LINEAR"
            ni[path] += 1
        info[nm] = ni
    J2["accessors"].extend(acc for acc, _ in anh)
    for k, (acc, data) in enumerate(anh):
        neu[n_acc + k] = data
    # fix1 (Pruefer Technik T7): Accessoren, auf die nichts mehr zeigt (die alten Sitz-Ausgaben), weglassen; Indizes neu zaehlen.
    # quelle[i] = Index des Accessors im Gerippe-GLB (Bytes von dort), sonst kommen die Daten aus neu[].
    quelle = list(range(len(J2["accessors"])))
    if not a.alte_behalten:
        benutzt = set()
        for m in J2["meshes"]:
            for pr in m["primitives"]:
                benutzt |= set(pr["attributes"].values())
                if "indices" in pr:
                    benutzt.add(pr["indices"])
        for sk_ in J2.get("skins", []):
            if "inverseBindMatrices" in sk_:
                benutzt.add(sk_["inverseBindMatrices"])
        for an in J2["animations"]:
            for smp in an["samplers"]:
                benutzt |= {smp["input"], smp["output"]}
        behalten = [i for i in range(len(J2["accessors"])) if i in benutzt]
        neu_ix = {i: k for k, i in enumerate(behalten)}
        J2["accessors"] = [J2["accessors"][i] for i in behalten]
        for m in J2["meshes"]:
            for pr in m["primitives"]:
                pr["attributes"] = {k: neu_ix[v] for k, v in pr["attributes"].items()}
                if "indices" in pr:
                    pr["indices"] = neu_ix[pr["indices"]]
        for sk_ in J2.get("skins", []):
            if "inverseBindMatrices" in sk_:
                sk_["inverseBindMatrices"] = neu_ix[sk_["inverseBindMatrices"]]
        for an in J2["animations"]:
            for smp in an["samplers"]:
                smp["input"] = neu_ix[smp["input"]]
                smp["output"] = neu_ix[smp["output"]]
        neu = {neu_ix[i]: d for i, d in neu.items() if i in neu_ix}
        quelle = behalten
        prim = J2["meshes"][0]["primitives"][0]
        print("EXPORT fix1: unbenutzte Accessoren weggelassen: %d von %d" % (n_acc + len(anh) - len(behalten), n_acc + len(anh)))
    # ---- Netz-Accessoren anpassen
    pa = J2["accessors"][prim["attributes"]["POSITION"]]
    pa["min"] = Pg.min(0).astype(float).tolist()
    pa["max"] = Pg.max(0).astype(float).tolist()
    for k, arr in neu.items():
        J2["accessors"][k]["count"] = int(arr.shape[0])
        if "min" in J2["accessors"][k] and k != prim["attributes"]["POSITION"]:
            J2["accessors"][k]["min"] = arr.min(0).astype(float).tolist()
            J2["accessors"][k]["max"] = arr.max(0).astype(float).tolist()
    for n in J2["nodes"]:
        if n.get("mesh") == 0:
            n["name"] = "NCBearCub"
    J2["meshes"][0]["name"] = "NCBearCub"
    # ---- Puffer neu packen: je Accessor eine BufferView (4-Byte-ausgerichtet), Ziele wie bisher
    bin_ = bytearray()
    views = []
    for i, ac in enumerate(J2["accessors"]):
        if i in neu:
            data = np.ascontiguousarray(neu[i].astype(CT[ac["componentType"]])).tobytes()
        else:
            data = bs.acc_bytes(J, B, quelle[i])
        while len(bin_) % 4:
            bin_ += b"\0"
        v = {"buffer": 0, "byteOffset": len(bin_), "byteLength": len(data)}
        if quelle[i] < n_acc:
            v_alt = J["bufferViews"][J["accessors"][quelle[i]]["bufferView"]]
            if "target" in v_alt:
                v["target"] = v_alt["target"]
        views.append(v)
        ac["bufferView"] = i
        ac.pop("byteOffset", None)
        bin_ += data
    while len(bin_) % 4:
        bin_ += b"\0"
    J2["bufferViews"] = views
    J2["buffers"] = [{"byteLength": len(bin_)}]
    J2["asset"]["generator"] = "baer_export_jfuss.py (Lauf baer-junges-fuss, Gerippe NCBearCub.glb 6c3f0a96)"
    js = json.dumps(J2, separators=(",", ":")).encode()
    while len(js) % 4:
        js += b" "
    out = b"glTF" + struct.pack("<II", 2, 12 + 8 + len(js) + 8 + len(bin_))
    out += struct.pack("<I", len(js)) + b"JSON" + js + struct.pack("<I", len(bin_)) + b"BIN\0" + bytes(bin_)
    open(a.aus, "wb").write(out)
    # ---- Selbstpruefung
    J3, B3 = bs.lade_glb(a.aus)
    gleich = alle = 0
    for an_a, an_n in zip(J["animations"], J3["animations"]):
        assert an_a["name"] == an_n["name"]
        if an_a["name"] in SITZ:
            continue
        for s1, s2 in zip(an_a["samplers"], an_n["samplers"]):
            alle += 2
            gleich += bs.acc_bytes(J, B, s1["input"]) == bs.acc_bytes(J3, B3, s2["input"])
            gleich += bs.acc_bytes(J, B, s1["output"]) == bs.acc_bytes(J3, B3, s2["output"])
            assert s1.get("interpolation") == s2.get("interpolation")
        assert an_a["channels"] == an_n["channels"]
    assert gleich == alle, (gleich, alle)
    # Sitz-Clips: Zeiten und Skalier-Schluessel byte-gleich, Kanaele vollstaendig
    sk = 0
    for an_a, an_n in zip(J["animations"], J3["animations"]):
        if an_a["name"] not in SITZ:
            continue
        assert an_a["channels"] == an_n["channels"]
        for ch in an_a["channels"]:
            if ch["target"]["path"] == "scale":
                s1, s2 = an_a["samplers"][ch["sampler"]], an_n["samplers"][ch["sampler"]]
                assert bs.acc_bytes(J, B, s1["output"]) == bs.acc_bytes(J3, B3, s2["output"])
                sk += 1
    for i, (n1, n2) in enumerate(zip(J["nodes"], J3["nodes"])):
        assert {k: v for k, v in n1.items() if k != "name"} == {k: v for k, v in n2.items() if k != "name"}, i
    assert J["skins"] == J3["skins"]
    assert bs.acc_bytes(J, B, J["skins"][0]["inverseBindMatrices"]) == bs.acc_bytes(J3, B3, J3["skins"][0]["inverseBindMatrices"])
    md5 = hashlib.md5(out).hexdigest()
    print("EXPORT", a.aus, "MD5", md5, "Punkte", len(Pg), "Dreiecke", len(Fg), "Bytes", len(out))
    print("EXPORT 12 andere Clips: Sampler-Ein-/Ausgaenge byte-gleich %d/%d; Sitz-Clips Skalier-Schluessel byte-gleich %d" % (gleich, alle, sk))
    print("EXPORT Sitz-Clips neue Kanaele (Drehung/Lage, unveraendert):", info, "neue Accessoren", len(anh))
    print("EXPORT Knoten/Skin/inverse Bind wie Gerippe: ja")


if __name__ == "__main__":
    main()
