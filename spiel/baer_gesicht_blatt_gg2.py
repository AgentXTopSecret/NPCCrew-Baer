# Lauf baer-gen-gross-v2 (12.11.2026), Rolle BAUER GESICHT: Blatt v2/bilder/gesicht.png (PLAN.md 9).
# Spalten: Foto-Ausschnitt | 2c | GEN heute | NEU braun | NEU Fototon | NEU Ton. Zeilen: Kopf nah vorn (el 0), schraeg 35/10, Seite 90/0,
# oben, Kevins Kamera Idle 0 / Eat 32 / Walk 7 gross (700 px/m) und Spielgroesse 100 px/m (2x nearest), Maul offen Rear 48 / Bite 13 nah,
# dazu Seite nah mit den Normalen des Original-Exports (Lippenlinie G-03).
# Render: v2/gesicht/werkzeug/gg2_render.py (Kopie von R/fix1/werkzeug/fx_render.py, Blender-glTF, Cycles OPTIX) ueber gg2_gpu.sh (Sperre
# _arbeit/baer_gen/gpu.lock). Statisch/offline, nicht gespielt. Schreibt nur v2/gesicht/r_blatt*/ und v2/bilder/gesicht.png.
# Aufruf: python baer_gesicht_blatt_gg2.py auftrag [aus=r_blatt] | zusammen [aus=r_blatt] [blatt=PFAD]
import json
import os
import sys

from PIL import Image, ImageDraw

R = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_gross/"
GS = R + "v2/gesicht/"
T = "C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/"
SPALTEN = [("2c", "2c", "tex2c"), ("GEN heute (braun)", "heute", "heute_braun"), ("NEU braun", "neu", "neu_braun"),
           ("NEU Fototon", "neu", "neu_foto"), ("NEU Ton", "neu", "ton")]
# name, clip, f, az, el, pxm, w, h, mitte (Knochen/Versatz), Foto
ZEILEN = [("vorn", "Idle01", 0, 0, 0, 700, 420, 380, ("Bip01_Head", (0.22, 0, -0.03)), "mutter"),
          ("schraeg 35/10", "Idle01", 0, 35, 10, 700, 420, 380, ("Bip01_Head", (0.22, 0, -0.03)), "E"),
          ("Seite 90/0", "Idle01", 0, 90, 0, 700, 420, 380, ("Bip01_Head", (0.22, 0, -0.03)), "E"),
          ("oben", "Idle01", 0, 0, 89, 700, 420, 380, ("Bip01_Head", (0.24, 0, 0.0)), None),
          ("Kevin Idle 0 (az0 el30)", "Idle01", 0, 0, 30, 700, 420, 380, ("Bip01_Head", (0.10, 0, -0.06)), None),
          ("Kevin Eat 32", "Eat", 32, 0, 30, 700, 420, 380, ("Bip01_Head", (0.10, 0, -0.08)), None),
          ("Kevin Walk 7", "Walk", 7, 0, 30, 700, 420, 380, ("Bip01_Head", (0.10, 0, -0.06)), None),
          ("Spiel Idle 100px/m", "Idle01", 0, 0, 30, 100, 210, 190, "bbox", None),
          ("Spiel Eat 100px/m", "Eat", 32, 0, 30, 100, 210, 190, "bbox", None),
          ("Maul Rear 48", "Rear", 48, 30, 5, 700, 420, 380, ("Bip01_Head", (0.10, 0, -0.04)), None),
          ("Maul Bite 13", "Bite", 13, 35, 10, 700, 420, 380, ("Bip01_Head", (0.10, 0, -0.05)), None)]
FOTO = {"mutter": R + "v2/plan/mutter_kopf.jpg", "E": R + "v2/plan/foto_E_kopf.jpg"}


def auftrag(kv):
    aus = GS + kv.get("aus", "r_blatt")
    jobs = []
    for zi, (name, clip, f, az, el, pxm, w, h, mitte, _) in enumerate(ZEILEN):
        for si, (tag, modell, mat) in enumerate(SPALTEN):
            j = dict(name="z%02d_s%d" % (zi, si), modell=modell, mat=mat, clip=clip, f=f, az=az, el=el, w=w, h=h, pxm=pxm, boden=True)
            if mitte == "bbox":
                j["mitte"] = "bbox"
            else:
                j["mitte"], j["versatz"] = mitte[0], list(mitte[1])
            jobs.append(j)
    # Lippenlinie: NEU mit Original-Export-Normalen (baer_export_gengross.py) gegen gg2-Export, Seite nah + schraeg nah
    for zi, (az, el) in enumerate(((90, 0), (35, 10))):
        for modell in ("neu", "neu_orig"):
            jobs.append(dict(name="lippe%d_%s" % (zi, modell), modell=modell, mat="neu_braun", clip="Idle01", f=0, az=az, el=el, w=420, h=300,
                             pxm=1600, mitte="Bip01_Head", versatz=[0.30, 0, -0.10], boden=False))
    A = {"aus": aus, "samples": 40,
         "glb": {"2c": T + "models_X/Skinned/NCBear.glb", "heute": R + "out/42/media/models_X/Skinned/NCBearGen.glb",
                 "neu": GS + "glb_vorschau/NCBearGen.glb", "neu_orig": GS + "glb_vorschau/orig/NCBearGen.glb"},
         "tex": {"tex2c": T + "textures/Body/NCBear.png", "heute_braun": R + "out/42/media/textures/Body/NCBearGen.png",
                 "neu_braun": GS + "tex_vorschau/NCBearGen.png", "neu_foto": GS + "tex_vorschau/NCBearGenFoto.png"},
         "jobs": jobs}
    os.makedirs(aus, exist_ok=True)
    p = GS + "auftrag_%s.json" % kv.get("aus", "r_blatt")
    json.dump(A, open(p, "w"), indent=1)
    print(p, len(jobs))


def zusammen(kv):
    aus = GS + kv.get("aus", "r_blatt") + "/"
    blatt = kv.get("blatt", R + "v2/bilder/gesicht.png")
    CW, CH = 420, 380
    kopf = 26
    links = 150
    W = links + CW * (1 + len(SPALTEN))
    Hz = [CH] * len(ZEILEN)
    H = kopf + sum(Hz) + 330
    bl = Image.new("RGB", (W, H), (34, 34, 34))
    d = ImageDraw.Draw(bl)
    for si, txt in enumerate(["Foto (Vorlage)"] + [s[0] for s in SPALTEN]):
        d.text((links + si * CW + 6, 6), txt, fill=(255, 230, 120))
    y = kopf
    for zi, (name, clip, f, az, el, pxm, w, h, mitte, foto) in enumerate(ZEILEN):
        d.text((6, y + 6), name, fill=(255, 255, 255))
        d.text((6, y + 22), "%s %d | az %d el %d" % (clip, f, az, el), fill=(180, 180, 180))
        d.text((6, y + 38), "%d px/m" % pxm + (" (2x nearest)" if pxm < 200 else ""), fill=(180, 180, 180))
        if foto:
            im = Image.open(FOTO[foto]).convert("RGB")
            im.thumbnail((CW, CH))
            bl.paste(im, (links + (CW - im.size[0]) // 2, y + (CH - im.size[1]) // 2))
        for si in range(len(SPALTEN)):
            p = aus + "z%02d_s%d.png" % (zi, si)
            if not os.path.exists(p):
                continue
            im = Image.open(p).convert("RGBA")
            hg = Image.new("RGBA", im.size, (92, 96, 92, 255))
            im = Image.alpha_composite(hg, im).convert("RGB")
            if pxm < 200:
                im = im.resize((im.size[0] * 2, im.size[1] * 2), Image.NEAREST)
            bl.paste(im, (links + (si + 1) * CW + (CW - im.size[0]) // 2, y + (CH - im.size[1]) // 2))
        y += CH
    d.text((6, y + 6), "Lippenlinie nah (NEU braun): links gg2-Export (Haut-Normalen), rechts Original-Export (alle Dreiecke)", fill=(255, 230, 120))
    for zi in range(2):
        for k, modell in enumerate(("neu", "neu_orig")):
            p = aus + "lippe%d_%s.png" % (zi, modell)
            if os.path.exists(p):
                im = Image.open(p).convert("RGBA")
                hg = Image.new("RGBA", im.size, (92, 96, 92, 255))
                bl.paste(Image.alpha_composite(hg, im).convert("RGB"), (links + (zi * 2 + k) * CW, y + 26))
    os.makedirs(os.path.dirname(blatt), exist_ok=True)
    bl.save(blatt)
    print("ok", blatt, bl.size)


if __name__ == "__main__":
    kv = dict(a.split("=", 1) for a in sys.argv[2:])
    {"auftrag": auftrag, "zusammen": zusammen}[sys.argv[1]](kv)
