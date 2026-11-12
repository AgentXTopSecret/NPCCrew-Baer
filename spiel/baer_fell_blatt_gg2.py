# Lauf baer-gen-gross-v2 (12.11.2026), Rolle BAUER FELL: Blatt v2/bilder/fell.png (PLAN.md 9).
# Spalten: 2c | GEN heute (braun) | NEU braun | NEU Fototon | NEU braun mit Textur 256 (Spiel-Option "Max. Texturgroesse").
# Zeilen: 8 Seiten el 30 gross (230 px/m) und in Spielgroesse 100 px/m (1:1, links Grau, rechts Gras); Aufrichten Rear 48 aus Kevins
# Kamera (az 0 el 30) und von vorn-unten (el -15); Gehen Walk 7 / 20; Sitzen 60; Fressen 32; Fell nah 1000 px/m (Flanke, Unterarm,
# Nacken-Uebergang, Schnauze); Rear 48 Kevin-Kamera unbeleuchtet (nur Textur) fuer die Band-Messung.
# Render: v2/fell/werkzeug/fl_render.py (unveraenderte Kopie von gg2_render.py / fx_render.py, Blender-glTF, Cycles OPTIX) ueber
# fl_gpu.sh (Sperre _arbeit/baer_gen/gpu.lock). Statisch/offline, nicht gespielt. Schreibt nur v2/fell/r_*/ und v2/bilder/fell*.png.
# Aufruf: python baer_fell_blatt_gg2.py auftrag [aus=r_blatt] [satz=voll|probe] | zusammen [aus=r_blatt] [blatt=PFAD]
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

R = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_gross/"
FE = R + "v2/fell/"
T = "C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/"
SPALTEN = [("2c", "2c", "tex2c"), ("GEN heute (braun)", "heute", "heute_braun"), ("NEU braun", "neu", "neu_braun"),
           ("NEU Fototon", "neu", "neu_foto"), ("NEU braun, Textur 256", "neu", "neu_braun256")]
CW, CH = 520, 400
ZEILEN = []
for az in (0, 45, 90, 135, 180, 225, 270, 315):
    ZEILEN.append(("Seite az %d el 30" % az, "Idle01", 0, az, 30, 230, 520, 400, "bbox", "gross"))
for az in (0, 45, 90, 135, 180, 225, 270, 315):
    ZEILEN.append(("Spiel az %d (Grau | Gras)" % az, "Idle01", 0, az, 30, 100, 226, 174, "bbox", "spiel"))
ZEILEN += [("Aufrichten Rear 48 Kevin", "Rear", 48, 0, 30, 230, 520, 400, "bbox", "gross"),
           ("Aufrichten Rear 48 vorn-unten", "Rear", 48, 0, -15, 230, 520, 400, "bbox_ohne_boden", "gross"),
           ("Gehen Walk 7 az 30", "Walk", 7, 30, 30, 230, 520, 400, "bbox", "gross"),
           ("Gehen Walk 20 az 90", "Walk", 20, 90, 30, 230, 520, 400, "bbox", "gross"),
           ("Sitzen Sit 60 Kevin", "Sit", 60, 0, 30, 230, 520, 400, "bbox", "gross"),
           ("Fressen Eat 32 Kevin", "Eat", 32, 0, 30, 230, 520, 400, "bbox", "gross"),
           ("nah Flanke 1000 px/m", "Idle01", 0, 80, 15, 1000, 520, 400, ("Bip01_Spine", (0.0, 0.0, 0.0)), "nah"),
           ("nah Unterarm 1000 px/m", "Idle01", 0, 30, 10, 1000, 520, 400, ("Bip01_L_Forearm", (0.0, 0.0, -0.08)), "nah"),
           ("nah Nacken 1000 px/m", "Idle01", 0, 60, 30, 1000, 520, 400, ("Bip01_Neck", (0.0, 0.0, 0.08)), "nah"),
           ("nah Schnauze 1000 px/m", "Idle01", 0, 30, 15, 1000, 520, 400, ("Bip01_Head", (0.12, 0.0, -0.04)), "nah"),
           ("Rear 48 Kevin unbeleuchtet", "Rear", 48, 0, 30, 230, 520, 400, "bbox", "flach")]
PROBE = ["Seite az 0 el 30", "Seite az 90 el 30", "Aufrichten Rear 48 Kevin", "Spiel az 0 (Grau | Gras)", "nah Flanke 1000 px/m",
         "nah Unterarm 1000 px/m", "nah Nacken 1000 px/m", "Rear 48 Kevin unbeleuchtet"]


def tex256():
    for nm in ("NCBearGen.png",):
        Image.open(FE + "tex/" + nm).convert("RGB").resize((256, 256), Image.LANCZOS).save(FE + "tex/_256_" + nm)


def auftrag(kv):
    aus = FE + kv.get("aus", "r_blatt")
    satz = kv.get("satz", "voll")
    tex256()
    jobs = []
    for zi, (name, clip, f, az, el, pxm, w, h, mitte, art) in enumerate(ZEILEN):
        if satz == "probe" and name not in PROBE:
            continue
        for si, (tag, modell, mat) in enumerate(SPALTEN):
            if satz == "probe" and si in (0, 4):
                continue
            j = dict(name="z%02d_s%d" % (zi, si), modell=modell, mat=mat + ("_flach" if art == "flach" else ""), clip=clip, f=f, az=az, el=el,
                     w=w, h=h, pxm=pxm, boden=(mitte != "bbox_ohne_boden"))
            if isinstance(mitte, str):
                j["mitte"] = "bbox"
            else:
                j["mitte"], j["versatz"] = mitte[0], list(mitte[1])
            jobs.append(j)
    A = {"aus": aus, "samples": 40,
         "glb": {"2c": T + "models_X/Skinned/NCBear.glb", "heute": R + "out/42/media/models_X/Skinned/NCBearGen.glb",
                 "neu": FE + "glb/NCBearGen.glb"},
         "tex": {"tex2c": T + "textures/Body/NCBear.png", "heute_braun": R + "out/42/media/textures/Body/NCBearGen.png",
                 "neu_braun": FE + "tex/NCBearGen.png", "neu_foto": FE + "tex/NCBearGenFoto.png", "neu_braun256": FE + "tex/_256_NCBearGen.png"},
         "jobs": jobs}
    os.makedirs(aus, exist_ok=True)
    p = FE + "auftrag_%s.json" % kv.get("aus", "r_blatt")
    json.dump(A, open(p, "w"), indent=1)
    print(p, len(jobs))


def gras(w, h, seed=7):
    rng = np.random.default_rng(seed)
    base = np.array([82, 98, 52], float)
    n1 = rng.normal(0, 1, (h // 4 + 1, w // 4 + 1))
    n1 = np.kron(n1, np.ones((4, 4)))[:h, :w]
    n2 = rng.normal(0, 1, (h, w))
    img = base[None, None, :] * (1 + 0.10 * n1[..., None] + 0.07 * n2[..., None])
    img[..., 0] += 6 * n1
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def zusammen(kv):
    aus = FE + kv.get("aus", "r_blatt") + "/"
    blatt = kv.get("blatt", R + "v2/bilder/fell.png")
    kopf = 26
    links = 170
    W = links + CW * len(SPALTEN)
    hz = [190 if z[-1] == "spiel" else CH for z in ZEILEN]
    H = kopf + sum(hz) + 30
    bl = Image.new("RGB", (W, H), (34, 34, 34))
    d = ImageDraw.Draw(bl)
    for si, (txt, _, _) in enumerate(SPALTEN):
        d.text((links + si * CW + 6, 6), txt, fill=(255, 230, 120))
    y = kopf
    for zi, (name, clip, f, az, el, pxm, w, h, mitte, art) in enumerate(ZEILEN):
        d.text((6, y + 6), name, fill=(255, 255, 255))
        d.text((6, y + 22), "%s %d | az %d el %d" % (clip, f, az, el), fill=(180, 180, 180))
        d.text((6, y + 38), "%d px/m" % pxm + (" 1:1 Grau | Gras" if art == "spiel" else ""), fill=(180, 180, 180))
        if art == "flach":
            d.text((6, y + 54), "nur Textur (Emission)", fill=(180, 180, 180))
        for si in range(len(SPALTEN)):
            p = aus + "z%02d_s%d.png" % (zi, si)
            if not os.path.exists(p):
                continue
            im = Image.open(p).convert("RGBA")
            x0 = links + si * CW
            if art == "spiel":
                for k, hg in enumerate((Image.new("RGBA", im.size, (92, 96, 92, 255)), gras(*im.size).convert("RGBA"))):
                    c = Image.alpha_composite(hg, im).convert("RGB")
                    bl.paste(c, (x0 + 10 + k * (im.size[0] + 40), y + 8))
            else:
                hg = Image.new("RGBA", im.size, (92, 96, 92, 255))
                c = Image.alpha_composite(hg, im).convert("RGB")
                bl.paste(c, (x0 + (CW - c.size[0]) // 2, y + (CH - c.size[1]) // 2))
        d.line([(links, y + hz[zi] - 1), (W, y + hz[zi] - 1)], fill=(60, 60, 60))
        y += hz[zi]
    os.makedirs(os.path.dirname(blatt), exist_ok=True)
    bl.save(blatt)
    print("ok", blatt, bl.size)


if __name__ == "__main__":
    kv = dict(a.split("=", 1) for a in sys.argv[2:])
    {"auftrag": auftrag, "zusammen": zusammen}[sys.argv[1]](kv)
