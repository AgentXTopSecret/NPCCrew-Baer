# Lauf baer-gen-gross (11.11.2026), Rolle SKELETT+GEWICHTE+CLIPS: GLB des neuen grossen Baeren E (NCBearGen) per PUFFER-TAUSCH im
# 2c-GLB (PLAN_GEN.md 5). Weg wie baer_export_junges.py (Original unveraendert), aber strenger: NUR die 6 Netz-Puffer (POSITION, NORMAL,
# TEXCOORD_0, JOINTS_0 u8, WEIGHTS_0, Indizes u16) werden ersetzt. Alles andere bleibt BYTE-GLEICH: 28 Knoten (Namen, Eltern, Drehung,
# Lage, Skalierung), Skin (Joints + inverseBindMatrices), alle 15 Animationen (Sampler, Kanaele, Zeit-/Wert-Puffer). Der Rest des
# Binaerblocks ab dem Ende der Netz-Puffer wird unveraendert kopiert und nur als Ganzes verschoben (byteOffset + delta, delta % 4 == 0).
# Kein Material, kein Bild (wie 2c; die Textur kommt aus der Rasse). Netz- und Knoten-Name "NCBearGen".
# Rahmen: tier-Meter (x vorn, y links, z oben) -> glTF = (y, z, x) * 0,544 (am 2c-GLB geprueft: Hullkoerper 1e-8 gleich dem Dump).
# Aufruf: python baer_export_gengross.py BASIS.npz GEWICHTE.npz CONTAINER.glb AUS.glb [name=NCBearGen] [perm=PFAD.npy]
#   (fix1: perm.npy nie unter out/42/ -- Assert; ohne perm= liegt sie neben AUS.glb, also AUS dann nicht im Liefer-Baum)
#   BASIS.npz     FORM-Abgabe E_gen_basis.npz (V verschweisst, T_glb, glb_punkt, UV glTF -- NICHT spiegeln)
#   GEWICHTE.npz  W (n x 26, Reihenfolge = Dump/Skin), V (muss == BASIS V sein)
#   CONTAINER.glb plan/eingang/NCBear_2c.glb (MD5 08ec7806..., wird geprueft)
# Statisch/offline, nicht gespielt. Liest/schreibt weder Test-Mod noch NPC Crew.
import hashlib
import json
import os
import struct
import sys

import numpy as np

M2U = 0.544
MD5_2C = "08ec7806efd13181bcc6bfd99a11f3fa"
CT = {5126: np.float32, 5123: np.uint16, 5125: np.uint32, 5121: np.uint8}
NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
# 2c traegt Gewichte genau an diesen 19 Knochen (Dump des 2c-GLB); E muss dieselbe Menge haben (OFFSET-Block im Dump textgleich)
KNOCHEN_2C = ["Bip01_Pelvis", "Bip01_L_Thigh", "Bip01_L_Calf", "Bip01_L_Foot", "Bip01_R_Thigh", "Bip01_R_Calf", "Bip01_R_Foot", "Bip01_Spine",
              "Bip01_Spine1", "Bip01_L_UpperArm", "Bip01_L_Forearm", "Bip01_L_Hand", "Bip01_Neck", "Bip01_Head", "Bip01_Jaw", "Bip01_R_UpperArm",
              "Bip01_R_Forearm", "Bip01_R_Hand", "Bip01_Tail"]


def lade(p):
    b = open(p, "rb").read()
    assert b[:4] == b"glTF"
    n = struct.unpack("<I", b[12:16])[0]
    assert b[16:20] == b"JSON"
    J = json.loads(b[20:20 + n])
    o = 20 + n
    bl = struct.unpack("<I", b[o:o + 4])[0]
    assert b[o + 4:o + 8] == b"BIN\0"
    return J, b[o + 8:o + 8 + bl], b


def acc_np(J, B, i):
    a = J["accessors"][i]
    v = J["bufferViews"][a["bufferView"]]
    k = NC[a["type"]]
    sz = np.dtype(CT[a["componentType"]]).itemsize
    s = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    assert v.get("byteStride", k * sz) == k * sz
    return np.frombuffer(B[s:s + a["count"] * k * sz], dtype=CT[a["componentType"]]).reshape(a["count"], k)


def normalen(P, F):
    """Glatte Normalen ueber verschweisste Lagen (UV-Naehte und Lippen-Zwillinge bekommen dieselbe Normale)."""
    _, wid = np.unique(np.round(P, 7), axis=0, return_inverse=True)
    wid = wid.ravel()
    fn = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
    acc = np.zeros((wid.max() + 1, 3))
    for k in range(3):
        np.add.at(acc, wid[F[:, k]], fn)
    N = acc[wid]
    return N / np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]


def baue(basis, gewichte, container, aus, name="NCBearGen", perm=None):
    # fix1 (Nachbesserung M1): die Pruefdatei perm.npy gehoert nie in den Liefer-Baum out/42/... (wird in einem Zug in die Test-Mod kopiert)
    perm_pfad = perm if perm else aus + ".perm.npy"
    assert "/out/42/" not in os.path.abspath(perm_pfad).replace("\\", "/"), "perm.npy nicht in den Liefer-Baum legen (perm=<Pfad ausserhalb out/>)"
    md5 = hashlib.md5(open(container, "rb").read()).hexdigest()
    assert md5 == MD5_2C, "Container ist nicht NCBear.glb 2c: " + md5
    J, B, _ = lade(container)
    N = np.load(basis)
    G = np.load(gewichte)
    V = N["V"].astype(np.float64)
    assert np.array_equal(G["V"], N["V"]), "Gewichte gehoeren nicht zu diesem Netz"
    gp, Tg, UV = N["glb_punkt"], N["T_glb"], N["UV"].astype(np.float64)
    W = G["W"].astype(np.float64)
    namen = [str(s) for s in G["namen"]]
    joints = J["skins"][0]["joints"]
    skin_namen = [J["nodes"][k]["name"] for k in joints]
    assert skin_namen == namen, "Skin-Reihenfolge != Gewichts-Reihenfolge"
    # ---- Gewichte: hoechstens 4, Summe 1, nur die 19 2c-Knochen
    benutzt = [namen[b] for b in range(len(namen)) if (W[:, b] > 0).any()]
    assert sorted(benutzt) == sorted(KNOCHEN_2C), ("Knochenmenge != 2c", sorted(set(benutzt) ^ set(KNOCHEN_2C)))
    ordn = np.argsort(-W, axis=1, kind="stable")[:, :4]
    Wt = np.take_along_axis(W, ordn, 1)
    Wt = np.where(Wt < 1e-6, 0.0, Wt)
    Wt /= Wt.sum(1)[:, None]
    Bi = np.where(Wt > 0, ordn, 0)                      # Fuellplaetze: Joint 0 mit Gewicht 0 (wie 2c)
    # ---- Netz in glTF
    Pg = (np.stack((V[:, 1], V[:, 2], V[:, 0]), 1) * M2U)[gp]
    F = Tg.copy()
    vol = np.einsum("ij,ij->i", Pg[F[:, 0]], np.cross(Pg[F[:, 1]], Pg[F[:, 2]])).sum() / 6
    if vol < 0:
        F = F[:, ::-1]
    vol2 = np.einsum("ij,ij->i", Pg[F[:, 0]], np.cross(Pg[F[:, 1]], Pg[F[:, 2]])).sum() / 6
    # Importer-Falle (Dump-Vergleich OFFSET/BIND): Assimp gibt jedem Knochen ohne Gewicht ein Schein-Gewicht 0 an Punkt 0;
    # LIMIT_BONE_WEIGHTS laesst an Punkt 0 nur 4 Eintraege uebrig und entfernt leere Knochen. Beim 2c hat Punkt 0 genau EIN echtes
    # Gewicht (Tail 1,0) -> Dummy01, Bip01, L_Toe0 ueberleben mit ihrem OFFSET. Darum hier: GLB-Punkt 0 = ein Punkt mit genau einem
    # Gewicht (bevorzugt Tail, wie 2c), sonst waere L_Toe0 im Dump eine Einheitsmatrix (Probe 11.11.: OFFSET/BIND L_Toe0 anders).
    Wg_, Bg_ = Wt[gp], Bi[gp]
    n1 = (Wg_ > 0).sum(1) == 1
    i_tail = namen.index("Bip01_Tail")
    kand = np.nonzero(n1 & (Bg_[:, 0] == i_tail))[0]
    if not len(kand):
        kand = np.nonzero(n1)[0]
    assert len(kand), "kein GLB-Punkt mit genau einem Gewicht"
    k0 = int(kand[0])
    # Der Importer nummeriert die Punkte in der Reihenfolge ihres ersten Auftretens in der Dreiecksliste (Probe 11.11.: erster Dump-Punkt
    # = erste Ecke des ersten Dreiecks, beim 2c-GLB aus Blender identisch mit Punkt 0). Darum: ein Dreieck mit k0 an den Anfang, k0 als
    # erste Ecke (Drehung der Ecken, Umlaufsinn bleibt), dann alle Punkte nach erstem Auftreten neu nummerieren.
    t0 = int(np.nonzero((F == k0).any(1))[0][0])
    r = int(np.nonzero(F[t0] == k0)[0][0])
    F = np.concatenate((np.roll(F[t0], -r)[None], np.delete(F, t0, 0)), 0)
    _, erst = np.unique(F.ravel(), return_index=True)
    perm = np.unique(F.ravel())[np.argsort(erst)]          # neuer Punkt i = alter Punkt perm[i]
    assert len(perm) == len(gp) and perm[0] == k0
    inv = np.argsort(perm)
    Pg, UV, Wg_, Bg_ = Pg[perm], UV[perm], Wg_[perm], Bg_[perm]
    F = inv[F]
    Ng = normalen(Pg, F)
    assert len(Pg) < 65536 and len(F) <= 20000
    prim = J["meshes"][0]["primitives"][0]
    at = prim["attributes"]
    neu = {at["POSITION"]: Pg.astype(np.float32), at["NORMAL"]: Ng.astype(np.float32), at["TEXCOORD_0"]: UV.astype(np.float32),
           at["JOINTS_0"]: Bg_.astype(np.uint8), at["WEIGHTS_0"]: Wg_.astype(np.float32),
           prim["indices"]: F.reshape(-1, 1).astype(np.uint16)}
    assert sorted(neu) == [0, 1, 2, 3, 4, 5], sorted(neu)
    # ---- Binaerblock: Netz-Puffer neu (Views 0..5), Rest unveraendert verschoben
    netz_views = sorted(J["accessors"][i]["bufferView"] for i in neu)
    assert netz_views == [0, 1, 2, 3, 4, 5]
    alt_ende = max(J["bufferViews"][v].get("byteOffset", 0) + J["bufferViews"][v]["byteLength"] for v in netz_views)
    assert all(v.get("byteOffset", 0) >= alt_ende for k, v in enumerate(J["bufferViews"]) if k not in netz_views)
    J2 = json.loads(json.dumps(J))
    bin_ = bytearray()
    for i in sorted(neu):
        a = J2["accessors"][i]
        daten = np.ascontiguousarray(neu[i].astype(CT[a["componentType"]])).tobytes()
        while len(bin_) % 4:
            bin_ += b"\0"
        v = J2["bufferViews"][a["bufferView"]]
        v["byteOffset"] = len(bin_)
        v["byteLength"] = len(daten)
        a["count"] = int(neu[i].shape[0])
        if "min" in a:
            a["min"] = neu[i].min(0).astype(float).tolist()
            a["max"] = neu[i].max(0).astype(float).tolist()
        bin_ += daten
    while len(bin_) % 4:
        bin_ += b"\0"
    delta = len(bin_) - alt_ende
    assert delta % 4 == 0
    for k, v in enumerate(J2["bufferViews"]):
        if k not in netz_views:
            v["byteOffset"] = v.get("byteOffset", 0) + delta
    bin_ += B[alt_ende:]
    while len(bin_) % 4:
        bin_ += b"\0"
    J2["buffers"] = [{"byteLength": len(bin_)}]
    J2["meshes"][0]["name"] = name
    for nd in J2["nodes"]:
        if nd.get("mesh") == 0:
            nd["name"] = name
    J2["asset"]["generator"] = "baer_export_gengross.py (Lauf baer-gen-gross, Puffer-Tausch in NCBear.glb 08ec7806)"
    js = json.dumps(J2, separators=(",", ":")).encode()
    while len(js) % 4:
        js += b" "
    out = b"glTF" + struct.pack("<II", 2, 12 + 8 + len(js) + 8 + len(bin_))
    out += struct.pack("<I", len(js)) + b"JSON" + js + struct.pack("<I", len(bin_)) + b"BIN\0" + bytes(bin_)
    open(aus, "wb").write(out)
    # ---- Selbstprobe: alles ausser den 6 Netz-Accessoren byte-gleich
    J3, B3, _ = lade(aus)
    gleich = 0
    for i in range(len(J["accessors"])):
        if i in neu:
            continue
        a0, a1 = dict(J["accessors"][i]), dict(J3["accessors"][i])
        assert a0 == a1, i
        assert acc_np(J, B, i).tobytes() == acc_np(J3, B3, i).tobytes(), i
        gleich += 1
    for k in ("skins", "animations", "scenes", "samplers"):
        assert J.get(k) == J3.get(k), k
    for n0, n1 in zip(J["nodes"], J3["nodes"]):
        d0 = {k: v for k, v in n0.items() if not (n0.get("mesh") == 0 and k == "name")}
        d1 = {k: v for k, v in n1.items() if not (n1.get("mesh") == 0 and k == "name")}
        assert d0 == d1
    np.save(perm_pfad, perm)                              # GLB-Punkt i (Datei) = Abgabe-GLB-Punkt perm[i] (fuer Pruefungen)
    info = dict(aus=aus, bytes=len(out), glb_punkte=int(len(Pg)), dreiecke=int(len(F)), volumen_m3_glb=round(float(vol2), 5),
                punkt0=dict(abgabe_index=k0, knochen=namen[int(Bg_[0, 0])], gewicht=float(Wg_[0, 0])),
                winding_umgedreht=bool(vol < 0), accessoren_byte_gleich=gleich, accessoren_neu=6, knochen=benutzt,
                einfluesse_max=int((Wt > 0).sum(1).max()), summe=[float(Wt.sum(1).min()), float(Wt.sum(1).max())],
                md5=hashlib.md5(out).hexdigest())
    print("EXPORT", json.dumps(info))
    return info


if __name__ == "__main__":
    kw = dict(a.split("=", 1) for a in sys.argv[5:])
    baue(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], **kw)
