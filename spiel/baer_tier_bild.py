# Rendert den Baeren so, wie die Engine ihn aus der GLB liest: Punkte, Gewichte, Offsets und Clip-Matrizen kommen aus Dump.java
# (Assimp mit den Schritten des Spiels). Gehaeutet wird hier in numpy, gerendert mit Cycles auf der RTX 4090 (OptiX).
# Aufruf: blender --background --factory-startup --python baer_tier_bild.py -- AUFTRAG.json
#   AUFTRAG: {"netz": dump.txt, "textur": png, "aus": ordner, "folge": [[clipdump_oder_null, clip, bilder, mitlaufen], ...],
#             "einzel": [[clip, bild, name], ...], "kamera": "spiel"|"seite", "aufl": [w, h], "samples": n}
#   clipdump null: Clips aus dem Netz-Dump selbst; sonst Reh-Dump (Rueckfall: Knochen per Name).
# Statisch geprueft und offline gemessen, nicht gespielt.
import json
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

AUF = json.load(open(sys.argv[sys.argv.index("--") + 1]))
sys.path.insert(0, AUF["werkzeug"])
from dumpread import lese  # noqa: E402

K_WELT = 1.6 / 1.5
D = lese(AUF["netz"])
V = D["verts"]
EL = D["el"].reshape(-1, 3)[:, ::-1]      # die Engine dreht die Reihenfolge um (ImportedSkinnedMesh), hier zurueck
CLIPS = {}


def clips_von(pfad):
    if pfad is None:
        return D, D["clips"]
    if pfad not in CLIPS:
        CLIPS[pfad] = lese(pfad)
    return CLIPS[pfad], CLIPS[pfad]["clips"]


def matrizen(quelle, c, fr):
    if quelle is D:
        return c["M"][fr]
    M = np.tile(np.eye(4), (len(D["names"]), 1, 1))
    for i, nm in enumerate(D["names"]):
        if nm in quelle["idx"]:
            M[i] = c["M"][fr][quelle["idx"][nm]]
    return M


def skin(M):
    h = np.c_[V[:, :3], np.ones(len(V))]
    out = np.zeros((len(V), 3))
    for k in range(4):
        w = V[:, 3 + k]
        b = V[:, 7 + k].astype(int)
        S = np.einsum("nij,njk->nik", M[b], D["off"][b])
        out += w[:, None] * np.einsum("nij,nj->ni", S, h)[:, :3]
    return out


def weg_von(quelle, c, fr):
    ti = quelle["idx"].get("Translation_Data")
    if ti is None or ti not in c["L"][fr]:
        return 0.0
    return -c["L"][fr][ti][2]


def zu_blender(P):
    # Modell (x, y oben, z hinten) -> Blender (x, y = z, z = y)
    return np.stack((P[:, 0], P[:, 2], P[:, 1]), 1)


bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
me = bpy.data.meshes.new("baer")
me.from_pydata(zu_blender(V[:, :3]).tolist(), [], EL.tolist())
me.update()
uvl = me.uv_layers.new(name="UV")
loops_v = np.empty(len(me.loops), dtype=np.int64)
me.loops.foreach_get("vertex_index", loops_v)
uv = np.stack((V[loops_v, 11], 1.0 - V[loops_v, 12]), 1)   # die Engine speichert 1 - v
uvl.data.foreach_set("uv", uv.ravel())
me.shade_smooth()
ob = bpy.data.objects.new("baer", me)
scene.collection.objects.link(ob)
# Volumen pruefen: aussen muss positiv sein
P0 = zu_blender(V[:, :3])
vol = np.einsum("ij,ij->i", P0[EL[:, 0]], np.cross(P0[EL[:, 1]], P0[EL[:, 2]])).sum() / 6.0
print("BILD Volumen", vol)
if vol < 0:
    me.flip_normals()
img = bpy.data.images.load(AUF["textur"])
mat = bpy.data.materials.new("fell")
mat.use_nodes = True
br = mat.node_tree.nodes["Principled BSDF"]
tx = mat.node_tree.nodes.new("ShaderNodeTexImage")
tx.image = img
mat.node_tree.links.new(tx.outputs["Color"], br.inputs["Base Color"])
br.inputs["Roughness"].default_value = 1.0
br.inputs["Specular IOR Level"].default_value = 0.0
me.materials.append(mat)

# Boden mit Kachelraster: eine Kachel ist 1/1,5 Modelleinheiten
bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, 0))
gr = bpy.context.active_object
gm = bpy.data.materials.new("boden")
gm.use_nodes = True
N, L = gm.node_tree.nodes, gm.node_tree.links
bsdf = N["Principled BSDF"]
tc = N.new("ShaderNodeTexCoord")
mp = N.new("ShaderNodeMapping")
mp.inputs["Scale"].default_value = (1.5, 1.5, 1.5)
L.new(tc.outputs["Object"], mp.inputs["Vector"])
ck = N.new("ShaderNodeTexChecker")
ck.inputs["Scale"].default_value = 1.0
ck.inputs["Color1"].default_value = (0.20, 0.22, 0.13, 1)
ck.inputs["Color2"].default_value = (0.15, 0.17, 0.10, 1)
L.new(mp.outputs["Vector"], ck.inputs["Vector"])
L.new(ck.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 1.0
gr.data.materials.append(gm)

w = bpy.data.worlds.new("w")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.6
scene.world = w
sun = bpy.data.lights.new("s", "SUN")
sun.energy = 2.2
sun.angle = math.radians(20)
so = bpy.data.objects.new("s", sun)
scene.collection.objects.link(so)
so.rotation_euler = (math.radians(42), 0, math.radians(-30))

scene.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "OPTIX"
print("BILD Geraete", [d.name for d in prefs.devices if d.use])
scene.cycles.device = "GPU"
scene.cycles.samples = AUF.get("samples", 24)
scene.cycles.use_denoising = True
scene.cycles.denoiser = "OPTIX"
scene.cycles.max_bounces = 4
scene.view_settings.view_transform = "Standard"
scene.render.image_settings.file_format = "PNG"
scene.render.resolution_x, scene.render.resolution_y = AUF.get("aufl", (960, 540))

cam = bpy.data.cameras.new("c")
cam.type = "ORTHO"
cam.ortho_scale = AUF.get("ortho", 2.2)
co = bpy.data.objects.new("c", cam)
scene.collection.objects.link(co)
scene.camera = co
art = AUF.get("kamera", "spiel")


def kamera(mitte):
    # Spielwinkel: 30 Grad von oben, schraeg (Core.DoPushIsoStuff dreht 30 Grad um X und 135 Grad um Y)
    if art == "seite":
        d = Vector((-1.0, 0.0, 0.10)).normalized()
    elif art == "vorn":
        d = Vector((0.25, -1.0, 0.25)).normalized()
    elif art == "hinten":
        d = Vector((-0.3, 1.0, 0.35)).normalized()
    else:
        el, az = math.radians(30), math.radians(-45 + AUF.get("dreh", 0))
        d = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    m = Vector(mitte)
    co.location = m + d * 12
    co.rotation_mode = "QUATERNION"
    co.rotation_quaternion = (-d).to_track_quat("-Z", "Y")


def setze(P, versatz):
    B = zu_blender(P)
    B[:, 1] -= versatz
    me.vertices.foreach_set("co", B.ravel())
    me.update()


aus = AUF["aus"]
os.makedirs(aus, exist_ok=True)
nr = 0
for clipdump, cname, bilder, mitlaufen in AUF.get("folge", []):
    q, cl = clips_von(clipdump)
    c = cl[cname]
    n = len(c["T"])
    schleife = n > 2 and np.allclose(c["M"][0], c["M"][-1], atol=1e-4)
    w_runde = weg_von(q, c, n - 1)
    for i in range(bilder):
        if schleife:
            fr = i % (n - 1)
            runde = i // (n - 1)
        else:
            fr = min(i, n - 1)
            runde = 0
        weg = (runde * w_runde + weg_von(q, c, fr)) * K_WELT if mitlaufen else 0.0
        setze(skin(matrizen(q, c, fr)), weg)
        kamera((0.0, -weg, 0.30))
        nr += 1
        scene.render.filepath = os.path.join(aus, "f_%04d.png" % nr)
        bpy.ops.render.render(write_still=True)
    print("BILD Folge", cname, bilder, "Bilder")
for cname, fr, name in AUF.get("einzel", []):
    q, cl = clips_von(AUF.get("einzel_quelle"))
    c = cl[cname]
    setze(skin(matrizen(q, c, min(fr, len(c["T"]) - 1))), 0.0)
    kamera((0.0, 0.0, 0.28))
    scene.render.filepath = os.path.join(aus, name + ".png")
    bpy.ops.render.render(write_still=True)
print("BILD_OK", nr)
