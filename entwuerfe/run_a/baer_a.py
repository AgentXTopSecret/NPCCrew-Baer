# Bauweise A: Koerper aus Metabaellen wie gehabt, KOPF aus einer Schnittfolge (Querschnittsringe mit
# Tabelle fuer Profil oben/unten und Breite, danach analytische Verschiebungen), echter Mundschlitz mit
# Mundhoehle im selben Netz, Augen in Lidern, Nasenpolster als eigenes feines Netz, Krallen als gebogene Rohre.
# Aufruf: blender --background --factory-startup --python baer_a.py -- kopf|ende|still|anim [schuesse]
import math
import random
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Euler, Matrix, Quaternion, Vector

OUT = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/blender_test/baer/run_a/"
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
MODE = ARGS[0] if ARGS else "still"
SHOTS = ARGS[1].split(",") if len(ARGS) > 1 else None
random.seed(3)
np.random.seed(3)

# Fell-Stufen: in den Probeschleifen weniger Haare, damit sich die Grafikkarte nicht fuellt
FUR_BODY = 0.22 if MODE == "kopf" else 1.0
FUR_HEAD = 0.55 if MODE == "kopf" else 1.0
FUR_GRAS = 0.2 if MODE == "kopf" else 1.0

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = scene.collection
FPS = 30
scene.render.fps = FPS

# ------------------------------------------------------------------ Koerper aus Metabaellen
mb = bpy.data.metaballs.new("baer")
mb.resolution = 0.024
mb.render_resolution = 0.024
mb.threshold = 0.62
mo = bpy.data.objects.new("baer", mb)
col.objects.link(mo)


def lz(z):
    t = max(0.0, min(1.0, (z - 0.13) / 0.33))
    return z + 0.33 * t * t * (3 - 2 * t)


def ball(x, y, z, r):
    e = mb.elements.new(type="BALL")
    e.co = (x, y, lz(z))
    e.radius = r


def chain(p0, p1, r0, r1, n):
    for i in range(n):
        t = i / max(1, n - 1)
        ball(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t, p0[2] + (p1[2] - p0[2]) * t, r0 + (r1 - r0) * t)


# Rumpf: Kruppe tiefer als der Schulterbuckel, tiefe Brust
chain((-0.78, 0, 0.75), (-0.52, 0, 0.77), 0.42, 0.50, 3)
chain((-0.40, 0, 0.74), (0.12, 0, 0.74), 0.50, 0.53, 4)
chain((0.20, 0, 0.73), (0.46, 0, 0.74), 0.48, 0.38, 3)
ball(0.33, 0, 1.03, 0.34)    # Buckel
ball(0.15, 0, 1.02, 0.36)
ball(-0.05, 0, 0.95, 0.28)
# Dicker Hals, der nach vorn abfaellt. Der Kopf ist kein Metaball mehr: er kommt aus der Schnittfolge,
# der Hals endet stumpf im Innern des Schaedels.
chain((0.52, 0, 0.86), (0.82, 0, 0.73), 0.40, 0.31, 3)
for s in (-1, 1):
    # Vorderbein: lang und saeulig, Pranken leicht einwaerts
    chain((0.30, s * 0.29, 0.78), (0.33, s * 0.32, 0.40), 0.30, 0.235, 3)
    chain((0.33, s * 0.32, 0.40), (0.35, s * 0.31, 0.14), 0.25, 0.205, 6)
    chain((0.37, s * 0.31, 0.10), (0.52, s * 0.28, 0.075), 0.20, 0.17, 3)
    # Hinterbein: maechtige Keule, Sohlengaenger mit langem Fuss
    chain((-0.72, s * 0.33, 0.72), (-0.57, s * 0.36, 0.42), 0.35, 0.26, 3)
    chain((-0.58, s * 0.35, 0.40), (-0.71, s * 0.33, 0.16), 0.26, 0.20, 6)
    chain((-0.75, s * 0.33, 0.10), (-0.42, s * 0.32, 0.075), 0.195, 0.17, 4)
# Stummelschwanz
chain((-1.06, 0, 0.70), (-1.15, 0, 0.68), 0.11, 0.08, 2)

depsgraph = bpy.context.evaluated_depsgraph_get()
bpy.context.view_layer.objects.active = mo
mo.select_set(True)
bpy.ops.object.convert(target="MESH")
body = bpy.context.active_object
body.name = "baer_koerper"

# Gleichmaessiges Netz: keine Splitter-Dreiecke, die beim Biegen reissen
start_tris = sum(len(p.vertices) - 2 for p in body.data.polygons)
rm = body.modifiers.new("gleich", "REMESH")
rm.mode = "VOXEL"
rm.voxel_size = 0.052
rm.use_smooth_shade = True
bpy.ops.object.modifier_apply(modifier=rm.name)
sm = body.modifiers.new("glatt", "SMOOTH")
sm.factor = 0.6
sm.iterations = 8
bpy.ops.object.modifier_apply(modifier=sm.name)
for p in body.data.polygons:
    p.use_smooth = True


# ------------------------------------------------------------------ Materialien
def mix_rgba(N, L, fac, a, b):
    m = N.new("ShaderNodeMix")
    m.data_type = "RGBA"
    fi = [i for i in m.inputs if i.type == "VALUE" and i.name == "Factor"][0]
    ai = [i for i in m.inputs if i.type == "RGBA" and i.name == "A"][0]
    bi = [i for i in m.inputs if i.type == "RGBA" and i.name == "B"][0]
    out = [o for o in m.outputs if o.type == "RGBA"][0]
    if hasattr(fac, "links"):
        L.new(fac, fi)
    else:
        fi.default_value = fac
    for sock, val in ((ai, a), (bi, b)):
        if hasattr(val, "links"):
            L.new(val, sock)
        else:
            sock.default_value = (val[0], val[1], val[2], 1)
    return out


def maprange(N, L, v, a, b, c, d):
    m = N.new("ShaderNodeMapRange")
    m.clamp = True
    L.new(v, m.inputs["Value"])
    m.inputs["From Min"].default_value = a
    m.inputs["From Max"].default_value = b
    m.inputs["To Min"].default_value = c
    m.inputs["To Max"].default_value = d
    return m.outputs[0]


fur = bpy.data.materials.new("fell")
fur.use_nodes = True
N, L = fur.node_tree.nodes, fur.node_tree.links
b = N["Principled BSDF"]
tc = N.new("ShaderNodeTexCoord")
sep = N.new("ShaderNodeSeparateXYZ")
L.new(tc.outputs["Generated"], sep.inputs[0])
# Grob: Fleckung im Fell. Fein: Haarstriche, gestaucht entlang des Koerpers.
mapg = N.new("ShaderNodeMapping")
mapg.inputs["Scale"].default_value = (24, 118, 118)
L.new(tc.outputs["Generated"], mapg.inputs["Vector"])
hair = N.new("ShaderNodeTexNoise")
hair.inputs["Scale"].default_value = 3.6
hair.inputs["Detail"].default_value = 11
hair.inputs["Roughness"].default_value = 0.72
L.new(mapg.outputs["Vector"], hair.inputs["Vector"])
big = N.new("ShaderNodeTexNoise")
big.inputs["Scale"].default_value = 11
big.inputs["Detail"].default_value = 7
L.new(tc.outputs["Generated"], big.inputs["Vector"])
base = mix_rgba(N, L, maprange(N, L, big.outputs["Fac"], 0.32, 0.68, 0, 1), (0.035, 0.018, 0.008), (0.06, 0.03, 0.013))
tips = mix_rgba(N, L, maprange(N, L, hair.outputs["Fac"], 0.42, 0.64, 0, 1), (0.02, 0.011, 0.005), (0.09, 0.05, 0.022))
col1 = mix_rgba(N, L, 0.56, base, tips)
# Beine und Bauch dunkler, Oberseite heller
legs = maprange(N, L, sep.outputs[2], 0.12, 0.36, 0.62, 0.0)
col2 = mix_rgba(N, L, legs, col1, (0.02, 0.011, 0.007))
top = maprange(N, L, sep.outputs[2], 0.68, 0.98, 0.0, 0.42)
col3 = mix_rgba(N, L, top, col2, (0.07, 0.038, 0.016))
L.new(col3, b.inputs["Base Color"])
L.new(maprange(N, L, hair.outputs["Fac"], 0.3, 0.7, 0.86, 0.66), b.inputs["Roughness"])
b.inputs["Sheen Weight"].default_value = 0.0
bp = N.new("ShaderNodeBump")
bp.inputs["Strength"].default_value = 1.0
bp.inputs["Distance"].default_value = 0.05
L.new(hair.outputs["Fac"], bp.inputs["Height"])
L.new(bp.outputs["Normal"], b.inputs["Normal"])


def plain(name, rgb, rough=0.5, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes["Principled BSDF"]
    n.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1)
    n.inputs["Roughness"].default_value = rough
    return m


def attr_color(mat, name, rough):
    """Grundfarbe aus einem Farbattribut des Netzes."""
    Nn, Ln = mat.node_tree.nodes, mat.node_tree.links
    a = Nn.new("ShaderNodeAttribute")
    a.attribute_type = "GEOMETRY"
    a.attribute_name = name
    p = Nn["Principled BSDF"]
    Ln.new(a.outputs["Color"], p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = rough
    return a


# Haut unter dem Fell des Kopfes: Farbe kommt je Punkt aus dem Netz
KOPFHAUT = plain("kopfhaut", (0.1, 0.06, 0.03), 0.78)
attr_color(KOPFHAUT, "hautfarbe", 0.86)
KOPFHAUT.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.2
# Nasse Teile: Lippen und Mundhoehle
MUND = plain("mund", (0.1, 0.03, 0.03), 0.34)
attr_color(MUND, "hautfarbe", 0.38)
MUND.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.35

# Nase: Anthrazit, ledrig-feuchte feine Koernung (Pflaster aus Zellen), Farbe je Punkt (Nasenloecher dunkel)
NASE = plain("nase", (0.03, 0.028, 0.028), 0.36)
attr_color(NASE, "hautfarbe", 0.36)
_nb = NASE.node_tree.nodes
_nl = NASE.node_tree.links
_tc = _nb.new("ShaderNodeTexCoord")
_vo = _nb.new("ShaderNodeTexVoronoi")
_vo.feature = "SMOOTH_F1"
_vo.inputs["Scale"].default_value = 420
_vo.inputs["Randomness"].default_value = 0.85
_nl.new(_tc.outputs["Object"], _vo.inputs["Vector"])
_nz = _nb.new("ShaderNodeTexNoise")
_nz.inputs["Scale"].default_value = 900
_nl.new(_tc.outputs["Object"], _nz.inputs["Vector"])
_bp1 = _nb.new("ShaderNodeBump")
_bp1.inputs["Strength"].default_value = 0.9
_bp1.inputs["Distance"].default_value = 0.0016
_nl.new(_vo.outputs["Distance"], _bp1.inputs["Height"])
_bp2 = _nb.new("ShaderNodeBump")
_bp2.inputs["Strength"].default_value = 0.35
_bp2.inputs["Distance"].default_value = 0.0005
_nl.new(_nz.outputs["Fac"], _bp2.inputs["Height"])
_nl.new(_bp1.outputs["Normal"], _bp2.inputs["Normal"])
_nl.new(_bp2.outputs["Normal"], _nb["Principled BSDF"].inputs["Normal"])
_nl.new(maprange(_nb, _nl, _vo.outputs["Distance"], 0.0, 0.7, 0.27, 0.46), _nb["Principled BSDF"].inputs["Roughness"])

LID = plain("lid", (0.006, 0.0052, 0.005), 0.5)
LID.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.3
TOOTH = plain("zahn", (0.52, 0.46, 0.33), 0.38)
ZUNGE = plain("zunge", (0.30, 0.085, 0.095), 0.36)

# Auge: dunkelbraune bis bernsteinfarbene Iris, runde Pupille, sonst fast schwarz. Sehachse = lokale +Z.
AUGE = bpy.data.materials.new("auge")
AUGE.use_nodes = True
_n = AUGE.node_tree.nodes
_l = AUGE.node_tree.links
_p = _n["Principled BSDF"]
_tc = _n.new("ShaderNodeTexCoord")
_sp = _n.new("ShaderNodeSeparateXYZ")
_l.new(_tc.outputs["Object"], _sp.inputs[0])
_cb = _n.new("ShaderNodeCombineXYZ")
_l.new(_sp.outputs[0], _cb.inputs[0])
_l.new(_sp.outputs[1], _cb.inputs[1])
_ln = _n.new("ShaderNodeVectorMath")
_ln.operation = "LENGTH"
_l.new(_cb.outputs[0], _ln.inputs[0])
_rp = _n.new("ShaderNodeValToRGB")
_rp.color_ramp.interpolation = "LINEAR"
_e = _rp.color_ramp.elements
_e[0].position = 0.0
_e[0].color = (0.002, 0.0016, 0.0014, 1)
_e[1].position = 1.0
_e[1].color = (0.006, 0.004, 0.003, 1)
for pos, rgb in ((0.33, (0.0015, 0.0012, 0.001)), (0.37, (0.072, 0.032, 0.009)), (0.48, (0.05, 0.021, 0.0065)),
                 (0.60, (0.024, 0.0105, 0.004)), (0.68, (0.005, 0.0035, 0.003))):
    el = _e.new(pos)
    el.color = (rgb[0], rgb[1], rgb[2], 1)
_map = _n.new("ShaderNodeMapRange")
_map.clamp = True
_l.new(_ln.outputs["Value"], _map.inputs["Value"])
_map.inputs["From Min"].default_value = 0.0
_map.inputs["From Max"].default_value = 0.0185 * 1.05
_map.inputs["To Min"].default_value = 0.0
_map.inputs["To Max"].default_value = 1.0
_l.new(_map.outputs[0], _rp.inputs["Fac"])
_l.new(_rp.outputs["Color"], _p.inputs["Base Color"])
_p.inputs["Roughness"].default_value = 0.11
_p.inputs["Specular IOR Level"].default_value = 0.22

# Horn: dunkelbraune Wurzel, zur Spitze elfenbein-grau, matt mit etwas Glanz; Laengsstreifen durch gedehntes Rauschen
HORN = bpy.data.materials.new("horn")
HORN.use_nodes = True
_n = HORN.node_tree.nodes
_l = HORN.node_tree.links
_p = _n["Principled BSDF"]
_at = _n.new("ShaderNodeAttribute")
_at.attribute_type = "GEOMETRY"
_at.attribute_name = "horn"
_rp = _n.new("ShaderNodeValToRGB")
_e = _rp.color_ramp.elements
_e[0].position = 0.0
_e[0].color = (0.009, 0.0048, 0.0026, 1)
_e[1].position = 1.0
_e[1].color = (0.46, 0.40, 0.30, 1)
for pos, rgb in ((0.45, (0.016, 0.0088, 0.0048)), (0.72, (0.06, 0.038, 0.022)), (0.9, (0.24, 0.195, 0.14))):
    el = _e.new(pos)
    el.color = (rgb[0], rgb[1], rgb[2], 1)
_l.new(_at.outputs["Fac"], _rp.inputs["Fac"])
_tc = _n.new("ShaderNodeTexCoord")
_mp = _n.new("ShaderNodeMapping")
_mp.inputs["Scale"].default_value = (30, 400, 400)
_l.new(_tc.outputs["Object"], _mp.inputs["Vector"])
_nz = _n.new("ShaderNodeTexNoise")
_nz.inputs["Scale"].default_value = 3
_nz.inputs["Detail"].default_value = 6
_l.new(_mp.outputs["Vector"], _nz.inputs["Vector"])
_cm = mix_rgba(_n, _l, maprange(_n, _l, _nz.outputs["Fac"], 0.38, 0.66, 0.0, 0.35), _rp.outputs["Color"], (0.01, 0.007, 0.005))
_l.new(_cm, _p.inputs["Base Color"])
_p.inputs["Roughness"].default_value = 0.52
_p.inputs["Specular IOR Level"].default_value = 0.22
_bpz = _n.new("ShaderNodeBump")
_bpz.inputs["Strength"].default_value = 0.35
_bpz.inputs["Distance"].default_value = 0.0012
_l.new(_nz.outputs["Fac"], _bpz.inputs["Height"])
_l.new(_bpz.outputs["Normal"], _p.inputs["Normal"])


# ------------------------------------------------------------------ Kopf-Rahmen: a nach vorn, y seitlich, c nach oben
HO = np.array((0.965, 0.0, 1.092))
_pit = math.radians(-9.0)
HA = np.array((math.cos(_pit), 0.0, math.sin(_pit)))
HY = np.array((0.0, 1.0, 0.0))
HU = np.array((-math.sin(_pit), 0.0, math.cos(_pit)))


KOPF_S = 1.05


def l2w(q):
    q = np.asarray(q, dtype=float) * KOPF_S
    return HO + q[..., 0:1] * HA + q[..., 1:2] * HY + q[..., 2:3] * HU


def w2l(p):
    d = np.asarray(p, dtype=float) - HO
    return np.stack((d @ HA, d @ HY, d @ HU), axis=-1) / KOPF_S


def rot_l2w(q):
    q = np.asarray(q, dtype=float)
    return q[..., 0:1] * HA + q[..., 1:2] * HY + q[..., 2:3] * HU


def rot_w2l(p):
    p = np.asarray(p, dtype=float)
    return np.stack((p @ HA, p @ HY, p @ HU), axis=-1)


def ss(a, b, x):
    t = np.clip((np.asarray(x, dtype=float) - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def unit(v):
    return np.asarray(v, dtype=float) / np.linalg.norm(v)


def bone_z(zw):
    """Knochen-Hilfe: bone() streckt z mit lz; oberhalb der Beine ist das genau +0.33."""
    return zw - 0.33


# ------------------------------------------------------------------ Skelett
arm = bpy.data.armatures.new("skelett")
ao = bpy.data.objects.new("skelett", arm)
col.objects.link(ao)
bpy.context.view_layer.objects.active = ao
bpy.ops.object.mode_set(mode="EDIT")
EB = arm.edit_bones
BONES = {}


def bone(name, head, tail, parent=None, connect=False):
    e = EB.new(name)
    e.head = (head[0], head[1], lz(head[2]))
    e.tail = (tail[0], tail[1], lz(tail[2]))
    e.roll = 0
    if parent:
        e.parent = EB[parent]
        e.use_connect = connect
    BONES[name] = e
    return e


bone("wurzel", (-0.58, 0, 0.66), (-0.16, 0, 0.66))
bone("ruecken", (-0.16, 0, 0.66), (0.26, 0, 0.78), "wurzel", True)
bone("brust", (0.26, 0, 0.78), (0.58, 0, 0.84), "ruecken", True)
bone("hals", (0.58, 0, 0.84), (0.86, 0, 0.80), "brust", True)
bone("kopf", (0.86, 0, 0.80), (1.38, 0, 0.66), "hals", True)
# Das Kiefergelenk liegt unter dem Ohr/hinter dem Auge; Knochen bis zum Kinn
_kg = l2w((0.15, 0.0, -0.078))
_kk = l2w((0.47, 0.0, -0.088))
bone("kiefer", (_kg[0], 0, bone_z(_kg[2])), (_kk[0], 0, bone_z(_kk[2])), "kopf")
bone("schwanz", (-1.02, 0, 0.72), (-1.26, 0, 0.72), "wurzel")
for s, n in ((-1, "R"), (1, "L")):
    bone("oberarm" + n, (0.30, s * 0.30, 0.76), (0.33, s * 0.32, 0.38), "brust")
    bone("unterarm" + n, (0.33, s * 0.32, 0.38), (0.35, s * 0.31, 0.13), "oberarm" + n, True)
    bone("pranke" + n, (0.35, s * 0.31, 0.13), (0.56, s * 0.29, 0.06), "unterarm" + n, True)
    bone("schenkel" + n, (-0.70, s * 0.335, 0.72), (-0.55, s * 0.35, 0.38), "wurzel")
    bone("wade" + n, (-0.55, s * 0.35, 0.38), (-0.72, s * 0.33, 0.13), "schenkel" + n, True)
    bone("fuss" + n, (-0.72, s * 0.33, 0.13), (-0.42, s * 0.32, 0.06), "wade" + n, True)
bpy.ops.object.mode_set(mode="OBJECT")

# ------------------------------------------------------------------ Gewichte des Koerpers: nah am Knochen zaehlt
NAMES = [b.name for b in arm.bones if b.name != "kiefer"]
SEG = {b.name: (b.head_local.copy(), b.tail_local.copy()) for b in arm.bones}


def seg_dist(p, a, c):
    ac = c - a
    t = max(0.0, min(1.0, (p - a).dot(ac) / ac.length_squared))
    return (p - (a + ac * t)).length


def side_of(nm):
    return {"R": -1, "L": 1}.get(nm[-1]) if nm not in ("kopf", "hals", "brust", "ruecken", "wurzel", "schwanz") else 0


WEIGHTS = []
for v in body.data.vertices:
    p = v.co
    cand = []
    for nm in NAMES:
        sd = side_of(nm)
        if sd and p.y * sd < -0.05:
            continue
        d = seg_dist(p, *SEG[nm])
        if sd:
            d *= 1.1
        cand.append((d, nm))
    cand.sort()
    cand = cand[:3]
    w = [1.0 / max(d, 0.03) ** 3 for d, _ in cand]
    tot = sum(w)
    WEIGHTS.append({nm: wt / tot for (d, nm), wt in zip(cand, w)})

nb = [[] for _ in body.data.vertices]
for e in body.data.edges:
    a, c = e.vertices
    nb[a].append(c)
    nb[c].append(a)
for _ in range(7):
    new = []
    for i, wmap in enumerate(WEIGHTS):
        out = {k: v * 0.45 for k, v in wmap.items()}
        n = nb[i]
        if n:
            f = 0.55 / len(n)
            for j in n:
                for k, v in WEIGHTS[j].items():
                    out[k] = out.get(k, 0.0) + v * f
        new.append(out)
    WEIGHTS = new


def sstep(a, c, x):
    t = max(0.0, min(1.0, (x - a) / (c - a)))
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ Schnittfolge des Kopfes
# Spalten: a (Blickachse), T (Oberlinie), B (Unterlinie), W (halbe Breite), Cw (Hoehe der breitesten Stelle,
# ab dem Mundwinkel zugleich die Lippenlinie), nU/nL (Superellipse oben/unten). Masse in Metern.
RINGE = np.array([
    # a       T       B       W      Cw     nU   nL
    [-0.165, 0.112, -0.205, 0.168, -0.040, 2.3, 2.2],
    [-0.085, 0.136, -0.212, 0.174, -0.038, 2.4, 2.2],
    [-0.015, 0.150, -0.205, 0.177, -0.034, 2.8, 2.2],
    [0.055, 0.155, -0.190, 0.175, -0.034, 2.9, 2.3],
    [0.120, 0.156, -0.170, 0.160, -0.042, 2.8, 2.4],
    [0.175, 0.153, -0.153, 0.140, -0.054, 2.7, 2.4],
    [0.208, 0.142, -0.142, 0.122, -0.063, 2.5, 2.4],
    [0.235, 0.118, -0.135, 0.108, -0.070, 2.4, 2.4],
    [0.258, 0.092, -0.130, 0.098, -0.074, 2.5, 2.4],
    [0.280, 0.073, -0.127, 0.090, -0.074, 2.7, 2.5],
    [0.305, 0.063, -0.121, 0.084, -0.072, 2.9, 2.6],
    [0.345, 0.058, -0.116, 0.080, -0.067, 3.1, 2.7],
    [0.395, 0.055, -0.112, 0.078, -0.062, 3.1, 2.7],
    [0.440, 0.053, -0.108, 0.076, -0.057, 3.1, 2.8],
    [0.465, 0.050, -0.104, 0.073, -0.053, 3.0, 2.8],
    [0.482, 0.044, -0.098, 0.066, -0.048, 2.8, 2.6],
    [0.492, 0.034, -0.090, 0.058, -0.044, 2.6, 2.5],
    [0.497, 0.021, -0.083, 0.049, -0.041, 2.4, 2.3],
    [0.5005, 0.006, -0.074, 0.039, -0.039, 2.3, 2.2],
    [0.502, -0.008, -0.064, 0.028, -0.038, 2.2, 2.2],
    [0.501, -0.021, -0.052, 0.015, -0.037, 2.1, 2.1],
    [0.4985, -0.031, -0.043, 0.006, -0.0365, 2.0, 2.0],
    [0.497, -0.036, -0.036, 0.0, -0.036, 2.0, 2.0],
])
A_WINKEL = 0.255      # Mundwinkel
A_RACHEN = 0.135      # Hinterwand der Mundhoehle
NSUB = 14             # feine Ringe je Tabellenabschnitt
MU = 100              # Spalten auf der oberen (und der unteren) Haelfte
KI = 30               # Spalten der Mundhoehle (gerade)
AUGE_L = np.array((0.236, 0.066, 0.058))     # Augenmitte, lokal (+y-Seite)
AUGE_R_ = 0.0185
NASE_C = 0.008


def pchip(x, y, xq):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    h = np.diff(x)
    d = np.diff(y) / h
    m = np.zeros_like(y)
    m[0] = d[0]
    m[-1] = d[-1]
    for k in range(1, len(y) - 1):
        if d[k - 1] * d[k] <= 0:
            m[k] = 0.0
        else:
            w1 = 2 * h[k] + h[k - 1]
            w2 = h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    idx = np.clip(np.searchsorted(x, xq, side="right") - 1, 0, len(h) - 1)
    t = (xq - x[idx]) / h[idx]
    t2 = t * t
    t3 = t2 * t
    return (2 * t3 - 3 * t2 + 1) * y[idx] + (t3 - 2 * t2 + t) * h[idx] * m[idx] + (-2 * t3 + 3 * t2) * y[idx + 1] + (t3 - t2) * h[idx] * m[idx + 1]


def glaette(v, n=3):
    v = v.copy()
    for _ in range(n):
        v[1:-1] = 0.25 * v[:-2] + 0.5 * v[1:-1] + 0.25 * v[2:]
    return v


def bogen(W, h, n, mu, dicht=0.62):
    """Superellipsen-Bogen von y=-W ueber die Hoehe h nach y=+W, gleichmaessig nach Bogenlaenge,
    zu den Enden hin (Lippe) dichter."""
    u = np.linspace(0.0, 1.0, mu + 1)
    if W < 1e-7 and h < 1e-7:
        return np.zeros(mu + 1), np.zeros(mu + 1)
    phi = np.linspace(-math.pi / 2, math.pi / 2, 1201)
    sp = np.sin(phi)
    cp = np.cos(phi)
    yy = W * np.sign(sp) * np.abs(sp) ** (2.0 / n)
    zz = h * np.abs(cp) ** (2.0 / n)
    ll = np.concatenate(([0.0], np.cumsum(np.hypot(np.diff(yy), np.diff(zz)))))
    ll /= max(ll[-1], 1e-9)
    su = u - dicht * np.sin(2 * math.pi * u) / (2 * math.pi)
    return np.interp(su, ll, yy), np.interp(su, ll, zz)


# Querschnitt der Mundhoehle von der Lippe zur Mitte: u (Anteil Spalten), Einzug, Hoehe.
# Erst die Lippentasche nach oben, dann der Zahnfleischwall (Zeile 4), dann das Gaumengewoelbe.
_IB_U = np.array((0.0, 0.07, 0.17, 0.27, 0.38, 0.50, 0.64, 1.0))
_IB_Y = np.array((0.0, 0.0035, 0.0065, 0.012, 0.020, 0.030, 0.042, 1.0))   # Einzug, Wert 1.0 = Mitte
_IB_Z = np.array((0.0, 0.0065, 0.0165, 0.0195, 0.0135, 0.0175, 0.030, 1.0))  # Hoehe, Wert 1.0 = Gewoelbehoehe


def innenbogen(w, h, kn):
    """Liefert y (von -w nach +w) und Hoehe z, Spalten symmetrisch, dazu den Fortschritt 0 Lippe .. 1 Mitte."""
    hk = kn // 2
    u = np.linspace(0.0, 1.0, hk + 1)
    sc = min(1.0, w / 0.06) if w > 1e-7 else 0.0
    n_ = len(_IB_U) - 1
    ei = np.interp(u, _IB_U[:n_], _IB_Y[:n_])
    zi = np.interp(u, _IB_U[:n_], _IB_Z[:n_])
    # letzte Stuetzstelle: Gewoelbe bis zur Mitte
    tt = np.clip((u - _IB_U[n_ - 1]) / (1.0 - _IB_U[n_ - 1]), 0.0, 1.0)
    e0 = _IB_Y[n_ - 1] * sc
    z0 = _IB_Z[n_ - 1] * sc
    yy = np.where(u < _IB_U[n_ - 1], w - ei * sc, max(w - e0, 0.0) * (1.0 - tt))
    zz = np.where(u < _IB_U[n_ - 1], zi * sc, z0 + (max(h, z0) - z0) * np.sin(tt * math.pi / 2))
    yy = np.maximum(yy, 0.0)
    return np.concatenate((-yy, yy[::-1][1:])), np.concatenate((zz, zz[::-1][1:])), np.concatenate((u, u[::-1][1:]))


class Netz:
    """Sammelt Punkte (lokal oder Welt), Flaechen und je Punkt die Felder fuer Farbe und Fell."""

    def __init__(self):
        self.v = []
        self.n = 0
        self.f = []
        self.ftag = []

    def add(self, arr):
        arr = np.asarray(arr, dtype=float)
        shp = arr.shape[:-1]
        cnt = int(np.prod(shp)) if shp else 1
        self.v.append(arr.reshape(-1, 3))
        idx = self.n + np.arange(cnt)
        self.n += cnt
        return idx.reshape(shp) if shp else int(idx[0])

    def quad(self, a, b, c, d, tag):
        s = []
        for q in (int(a), int(b), int(c), int(d)):
            if q not in s:
                s.append(q)
        if len(s) >= 3:
            self.f.append(tuple(s))
            self.ftag.append(tag)

    def pos(self):
        return np.concatenate(self.v, axis=0)


AUGE_UH = math.radians(41.0)
AUGE_VU = math.radians(15.0)
AUGE_VD = math.radians(16.0)
AUGE_KIPP = math.radians(9.0)   # Aussenwinkel hoeher


def augen_rahmen(sd):
    E = np.array((AUGE_L[0], sd * AUGE_L[1], AUGE_L[2]))
    g = unit((0.90, sd * 0.30, 0.20))
    up = np.array((0.0, 0.0, 1.0))
    e1 = unit(np.cross(g, up))
    if e1[1] * sd < 0:
        e1 = -e1        # e1 zeigt vom Nasenwinkel zum Aussenwinkel
    e2 = np.cross(e1, g)
    if e2[2] < 0:
        e2 = -e2
    return E, g, e1, e2


def augen_abstand(Q, sd):
    """Winkelabstand (Bogenmass) eines Punktes vom Mandel-Rand, gesehen von der Augenmitte; negativ innen.
    Liefert ausserdem Abstand zur Mitte, Richtung und Kosinus zur Sehachse."""
    E, g, e1, e2 = augen_rahmen(sd)
    r = Q - E
    dist = np.linalg.norm(r, axis=-1)
    d_ = r / np.maximum(dist[..., None], 1e-7)
    cw = np.sum(d_ * g, axis=-1)
    uu = np.arctan2(np.sum(d_ * e1, axis=-1), np.maximum(cw, 1e-3))
    vv = np.arctan2(np.sum(d_ * e2, axis=-1), np.maximum(cw, 1e-3))
    # Kippung herausdrehen
    ck, sk = math.cos(AUGE_KIPP), math.sin(AUGE_KIPP)
    u2 = uu * ck + vv * sk
    v2 = -uu * sk + vv * ck
    vh = np.where(v2 > 0, AUGE_VU, AUGE_VD)
    m = np.sqrt((u2 / AUGE_UH) ** 2 + (v2 / vh) ** 2)
    rho = np.sqrt(u2 * u2 + v2 * v2)
    sdist = rho * (1.0 - 1.0 / np.maximum(m, 1e-4))
    # hinter der Sehebene zaehlt der Punkt als weit weg
    sdist = np.where(cw > 0.05, sdist, 9.0)
    return sdist, dist, d_, cw


def nasen_e(y, z):
    """Radiale Koordinate des Nasenumrisses: 1 am Rand. z relativ zur Polstermitte."""
    un = np.clip(-z / 0.0305, 0.0, 1.0)
    hw = 0.0425 * (1.0 - 0.46 * un ** 1.2)
    hz = np.where(z > 0, 0.0265, 0.0305)
    return (np.abs(y / hw) ** 3 + np.abs(z / hz) ** 3) ** (1.0 / 3.0)


def ringnormalen(P):
    di = np.gradient(P, axis=0)
    dj = np.roll(P, -1, axis=1) - np.roll(P, 1, axis=1)
    nn = np.cross(di, dj)
    ln = np.linalg.norm(nn, axis=-1, keepdims=True)
    nn = nn / np.maximum(ln, 1e-12)
    cen = P.mean(axis=1, keepdims=True)
    if ((P - cen) * nn).sum() < 0:
        nn = -nn
    return nn


def baue_kopf():
    x = np.arange(len(RINGE), dtype=float)
    xq = np.linspace(0.0, len(RINGE) - 1.0, (len(RINGE) - 1) * NSUB + 1)
    a_, T_, B_, W_, Cw_, nU_, nL_ = [glaette(pchip(x, RINGE[:, k], xq), 3) for k in range(7)]
    Nn = len(xq)
    W_[-1] = 0.0
    Cw_ = Cw_ - 0.0015 * np.exp(-(((a_ - 0.40) / 0.045) ** 2)) * ss(A_WINKEL, A_WINKEL + 0.04, a_)
    ic = int(np.argmax(a_ >= A_WINKEL))
    it = int(np.argmax(a_ >= A_RACHEN))
    rec = 0.021 * ss(0.38, 0.49, a_)                     # Unterkiefer vorn zurueckgesetzt
    nar = np.minimum(0.0085 * ss(A_WINKEL, A_WINKEL + 0.05, a_) + 0.010 * ss(0.38, 0.47, a_), 0.34 * W_)  # Unterlippe und Kinn sitzen innen
    dl = 0.0028 * ss(A_WINKEL, A_WINKEL + 0.035, a_) * (1 - ss(0.49, 0.497, a_))
    rec[: ic + 1] = 0.0
    nar[: ic + 1] = 0.0
    dl[: ic + 1] = 0.0

    Mu = MU
    Up = np.zeros((Nn, Mu + 1, 3))
    Lo = np.zeros((Nn, Mu + 1, 3))
    for i in range(Nn):
        yy, zz = bogen(W_[i], max(T_[i] - Cw_[i], 0.0), nU_[i], Mu)
        Up[i, :, 0] = a_[i]
        Up[i, :, 1] = yy
        Up[i, :, 2] = Cw_[i] + zz
        c0 = Cw_[i] + dl[i]
        yy, zz = bogen(W_[i] - nar[i], max(c0 - B_[i], 0.0), nL_[i], Mu)
        Lo[i, :, 0] = a_[i] - rec[i]
        Lo[i, :, 1] = -yy
        Lo[i, :, 2] = c0 - zz
    PU = Up[-1, 0].copy()
    PL = Lo[-1, 0].copy()
    Up[-1, :] = PU
    Lo[-1, :] = PL
    Mm = 2 * Mu
    P = np.concatenate((Up, Lo[:, 1:Mu]), axis=1)
    E_p = Lo[:, 0].copy()      # Unterlippe +y
    E_m = Lo[:, Mu].copy()     # Unterlippe -y

    # Abstand zur Lippe je Punkt: Bogenlaenge zum Schlitz, und zum Mundwinkel
    sl = np.full((Nn, Mm), 9.0)
    for i in range(ic, Nn):
        du = np.linalg.norm(np.diff(Up[i], axis=0), axis=1)
        s0 = np.concatenate(([0.0], np.cumsum(du)))
        su = np.minimum(s0, s0[-1] - s0)
        dv = np.linalg.norm(np.diff(Lo[i], axis=0), axis=1)
        s1 = np.concatenate(([0.0], np.cumsum(dv)))
        sv = np.minimum(s1, s1[-1] - s1)
        sl[i, : Mu + 1] = su
        sl[i, Mu + 1 :] = sv[1:Mu]
    CR = Up[ic, 0].copy()
    CL = Up[ic, Mu].copy()
    dc = np.minimum(np.linalg.norm(P - CR, axis=-1), np.linalg.norm(P - CL, axis=-1))
    dlip = np.minimum(sl, dc)

    # ---------------------------------------------- analytische Verschiebungen
    a = P[..., 0]
    y = P[..., 1]
    c = P[..., 2]
    ay = np.abs(y)
    istoben = np.zeros((Nn, Mm), dtype=bool)
    istoben[:, : Mu + 1] = True

    def g3(a0, sa, y0, sy, c0, sc):
        return np.exp(-(((a - a0) / sa) ** 2 + ((ay - y0) / sy) ** 2 + ((c - c0) / sc) ** 2))

    nase_e = nasen_e(y, c - NASE_C)
    nase_vorn = ss(0.455, 0.475, a)
    d = np.zeros((Nn, Mm))
    d += 0.012 * g3(0.205, 0.024, 0.073, 0.036, 0.100, 0.028)        # Brauenwulst
    d -= 0.004 * g3(0.262, 0.018, 0.068, 0.018, 0.052, 0.016)        # Augenhoehle unten/vorn etwas tiefer
    d -= 0.0045 * g3(0.215, 0.055, 0.0, 0.015, 0.115, 0.055)         # Stirnfurche
    d += 0.013 * g3(0.115, 0.05, 0.165, 0.05, -0.005, 0.045)         # Jochbogen
    d -= 0.007 * g3(0.06, 0.05, 0.122, 0.028, 0.125, 0.03)           # Schlaefe
    d += 0.009 * g3(0.11, 0.06, 0.115, 0.05, -0.135, 0.03)           # Kaumuskel unten
    # Nasenruecken: ganz flache Mittelleiste, seitlich davon leichte Rinne
    d += 0.0016 * np.exp(-(y / 0.024) ** 2) * ss(0.30, 0.34, a) * (1 - ss(0.44, 0.47, a)) * ss(0.0, 0.02, c)
    # Lippe: Polster ueber dem Rand, weiche Falte darueber (nur Oberkiefer, Bereich Schnauze)
    bandS = ss(0.27, 0.31, a) * (1 - ss(0.46, 0.49, a))
    obl = 0.0042 * np.exp(-(((sl - 0.017) / 0.011) ** 2)) * bandS * (y * 0 + 1)
    falte = -0.0016 * np.exp(-(((sl - 0.040) / 0.008) ** 2)) * bandS
    d += (obl + falte) * istoben
    d += 0.0022 * np.exp(-(((sl - 0.011) / 0.008) ** 2)) * bandS * (~istoben)
    # Mittelfurche von der Nase zur Lippe
    d -= 0.0042 * np.exp(-((y / 0.0044) ** 2)) * ss(-0.014, -0.024, c) * ss(0.48, 0.494, a) * istoben
    # Sitz des Nasenpolsters: Schnauze dort etwas eingesenkt
    d -= 0.0045 * (1 - ss(0.82, 1.1, nase_e)) * nase_vorn
    d *= ss(0.0, 0.006, dlip)
    nn = ringnormalen(P)
    P = P + nn * d[..., None]
    # Auge: Haut auf eine Schale um die Kugel ziehen. Innerhalb der Mandel taucht sie weg, das Lid ueberdeckt die Kante.
    for sd_ in (-1, 1):
        sdist, dist, d_, cw = augen_abstand(P, sd_)
        tt = ss(0.03, 0.22, sdist)
        rt = lerp(AUGE_R_ - 0.004, AUGE_R_ + 0.0032, tt)
        wgt = (1.0 - ss(0.0235, 0.041, dist)) * ss(-0.15, 0.25, cw)
        E_ = augen_rahmen(sd_)[0]
        P = E_ + d_ * (dist * (1 - wgt) + rt * wgt)[..., None]

    # ---------------------------------------------- Mundhoehle
    Ki = KI
    K_WALL_IDX = int(round(0.38 * (Ki // 2)))
    InU = np.zeros((Nn, Ki + 1, 3))
    InL = np.zeros((Nn, Ki + 1, 3))
    prog = None
    w_ic = W_[ic]
    hP_ic = min(0.040, 0.42 * (T_[ic] - Cw_[ic]))
    hF_ic = min(0.038, 0.55 * (Cw_[ic] - B_[ic]))
    for i in range(it, Nn):
        if i >= ic:
            wu = W_[i]
            wl = W_[i] - nar[i]
            hP = min(0.042, 0.42 * max(T_[i] - Cw_[i], 0.0))
            hF = min(0.040, 0.62 * max(Cw_[i] + dl[i] - B_[i], 0.0))
            cU = Cw_[i]
            cL = Cw_[i] + dl[i]
            aU = a_[i]
            aL = a_[i] - rec[i]
        else:
            q = (a_[ic] - a_[i]) / max(a_[ic] - a_[it], 1e-6)
            wu = wl = lerp(w_ic - 0.006, 0.034, q)
            hP = lerp(hP_ic, 0.026, q)
            hF = lerp(hF_ic, 0.026, q)
            cU = cL = lerp(Cw_[ic], Cw_[ic] + 0.008, q)
            aU = aL = a_[i]
        yy, zz, prog = innenbogen(wu, hP, Ki)
        zur = 0.016 * ss(0.43, 0.49, aU) * ss(0.0, 0.2, prog)      # vorn nach hinten versetzt, Lippenkante bleibt
        InU[i, :, 0] = aU - zur
        InU[i, :, 1] = yy
        InU[i, :, 2] = cU + zz
        # Gaumenfalten: feine Querwuelste im Mittelbereich
        InU[i, :, 2] -= 0.0016 * np.sin(aU * 230.0) ** 2 * ss(0.6, 0.8, prog) * ss(0.28, 0.32, aU)
        yy, zz, prog = innenbogen(wl, hF, Ki)
        zur = 0.016 * ss(0.43, 0.49, aL + rec[i]) * ss(0.0, 0.2, prog)
        InL[i, :, 0] = aL - zur
        InL[i, :, 1] = -yy
        InL[i, :, 2] = cL - zz
    InU[-1, :] = PU
    InL[-1, :] = PL

    # ---------------------------------------------- Netz zusammensetzen
    nz = Netz()
    # Hinterster Ring wird mit einem Mittelpunkt geschlossen (liegt im Hals)
    idxP = nz.add(P)
    # Pol vorn: alle Punkte des letzten Rings fallen zusammen
    pol_o = idxP[-1, 0]
    idxP[-1, : Mu + 1] = pol_o
    pol_u = nz.add(PL)
    idxP[-1, Mu + 1 :] = pol_u
    # Unterlippe: eigene Punkte ab dem Mundwinkel
    idxLp = idxP[:, Mu].copy()
    idxLm = idxP[:, 0].copy()
    if ic + 1 < Nn - 1:
        idxLp[ic + 1 : Nn - 1] = nz.add(E_p[ic + 1 : Nn - 1])
        idxLm[ic + 1 : Nn - 1] = nz.add(E_m[ic + 1 : Nn - 1])
    idxLp[-1] = pol_u
    idxLm[-1] = pol_u

    def low(i, j):
        if j == Mu:
            return idxLp[i]
        if j == Mm:
            return idxLm[i]
        return idxP[i, j]

    for i in range(Nn - 1):
        for j in range(Mu):
            nz.quad(idxP[i, j], idxP[i + 1, j], idxP[i + 1, j + 1], idxP[i, j + 1], 1)
        for j in range(Mu, Mm):
            nz.quad(low(i, j), low(i + 1, j), low(i + 1, j + 1), low(i, j + 1), 1)
    hinten = nz.add(np.array((a_[0] - 0.01, 0.0, Cw_[0])))
    for j in range(Mm):
        nz.quad(idxP[0, j], idxP[0, (j + 1) % Mm], hinten, hinten, 1)

    # Mundhoehle: Oberseite und Unterseite, vorn am Lippenrand angeschlossen, hinten ein Schlauch
    idxU = nz.add(InU[it:])
    idxL = nz.add(InL[it:])

    def U_(i, k):
        ii = i - it
        if i >= ic:
            if k == 0:
                return idxP[i, 0]
            if k == Ki:
                return idxP[i, Mu]
        if i == Nn - 1:
            return pol_o
        return idxU[ii, k]

    def L_(i, k):
        ii = i - it
        if i >= ic:
            if k == 0:
                return idxLp[i]
            if k == Ki:
                return idxLm[i]
        else:
            if k == 0:
                return U_(i, Ki)
            if k == Ki:
                return U_(i, 0)
        if i == Nn - 1:
            return pol_u
        return idxL[ii, k]

    for i in range(it, Nn - 1):
        for k in range(Ki):
            nz.quad(U_(i, k), U_(i + 1, k), U_(i + 1, k + 1), U_(i, k + 1), 2)
            nz.quad(L_(i, k), L_(i + 1, k), L_(i + 1, k + 1), L_(i, k + 1), 2)
    rachen = nz.add(np.array((a_[it] - 0.012, 0.0, InU[it, 0, 2])))
    ring = [U_(it, k) for k in range(Ki)] + [L_(it, k) for k in range(Ki)]
    for k in range(len(ring)):
        nz.quad(ring[k], ring[(k + 1) % len(ring)], rachen, rachen, 2)

    # ---------------------------------------------- Felder je Punkt
    V = nz.pos()
    nv = len(V)
    ext = np.zeros(nv, dtype=bool)
    ext[idxP.reshape(-1)] = True
    ext[idxLp] = True
    ext[idxLm] = True
    dl_all = np.full(nv, 9.0)
    dl_all[idxP.reshape(-1)] = dlip.reshape(-1)
    dl_all[idxLp[ic + 1 :]] = 0.0
    dl_all[idxLm[ic + 1 :]] = 0.0
    dl_all[pol_o] = 0.0
    dl_all[pol_u] = 0.0
    a = V[:, 0]
    y = V[:, 1]
    c = V[:, 2]
    ay = np.abs(y)
    _s1, _d1, _, _ = augen_abstand(V, -1)
    _s2, _d2, _, _ = augen_abstand(V, 1)
    # Meter vom Lidrand. Glatt: der Winkel zaehlt nur nah am Auge und vor der Sehebene,
    # sonst der Abstand zur Kugel; entlang der Sehachse waere der Winkel auch weit vorn auf der Schnauze null.
    _cw = lambda Q_, sd_: np.sum((Q_ - augen_rahmen(sd_)[0]) / np.maximum(np.linalg.norm(Q_ - augen_rahmen(sd_)[0], axis=1, keepdims=True), 1e-7) * augen_rahmen(sd_)[1], axis=1)
    _k1 = np.maximum(_d1 - 0.0205, np.minimum(np.maximum(_s1, 0.0), 1.1) * 0.022 * ss(0.05, 0.3, _cw(V, -1)) * (_s1 < 8))
    _k2 = np.maximum(_d2 - 0.0205, np.minimum(np.maximum(_s2, 0.0), 1.1) * 0.022 * ss(0.05, 0.3, _cw(V, 1)) * (_s2 < 8))
    de = np.minimum(_k1, _k2)
    nase_e = nasen_e(y, c - NASE_C)
    nase_vorn = ss(0.455, 0.475, a)
    dn = np.where(a > 0.40, np.maximum(nase_e - 0.92, 0.0) * 0.032, 9.0)
    # Master-Laenge in Metern
    hoch = ss(-0.06, 0.05, c)
    Lst = lerp(0.115, 0.034, ss(-0.10, 0.165, a))
    Lwa = lerp(0.150, 0.058, ss(-0.09, 0.235, a))
    Lk = lerp(Lwa, Lst, hoch)
    oben = c > lerp(-0.06, -0.05, ss(0.2, 0.45, a))
    tm = np.where(oben, ss(0.235, 0.345, a), ss(0.225, 0.37, a))
    Lm = lerp(Lk, 0.0125, tm)
    # Deckel statt fester Werte: nah an Nase, Auge, Lippe kuerzer, weiter weg frei
    Lm = np.minimum(Lm, 0.0065 + 0.14 * dn)
    Lm = np.minimum(Lm, 0.0065 + 0.95 * np.maximum(de - 0.002, 0.0))
    Lm = np.minimum(Lm, 0.006 + 0.42 * dl_all)
    _ohr = np.linalg.norm(np.stack((a - 0.026, ay - 0.157, c - 0.133), axis=1), axis=1)
    Lm = np.minimum(Lm, 0.026 + 0.6 * np.maximum(_ohr - 0.05, 0.0))
    # Maske: wo gar kein Haar waechst
    mp = 1.0 - np.exp(-((y / 0.0030) ** 2)) * ss(-0.010, -0.022, c) * ss(0.48, 0.494, a)
    mask = ss(0.0015, 0.0065, dl_all) * ss(0.88, 0.98, nase_e + (1 - nase_vorn) * 9.0) * ss(0.0016, 0.0042, de) * mp
    mask = mask * ext
    # Farbe: Melanin und Roetung
    mel = lerp(0.76, 0.665, ss(-0.10, 0.20, a))
    mst = lerp(0.76, 0.59, ss(-0.08, 0.20, a))
    mel = lerp(mel, mst, hoch)
    mel = mel - 0.075 * np.exp(-(((a - 0.195) / 0.042) ** 2 + ((ay - 0.075) / 0.05) ** 2 + ((c - 0.105) / 0.04) ** 2))
    mel = lerp(mel, 0.475, tm)
    mel = lerp(mel, 0.50, tm * (~oben))
    # Nasenruecken eine Spur dunkler als die Seiten
    mel = mel + 0.05 * tm * oben * np.exp(-((y / 0.035) ** 2))
    mel = lerp(mel, 0.76, 1.0 - ss(0.0, 0.030, dn))
    mel = lerp(mel, 0.72, 1.0 - ss(0.003, 0.017, de))
    mel = lerp(mel, 0.80, 1.0 - ss(0.002, 0.012, dl_all))
    red = lerp(0.26, 0.18, np.maximum(tm, 0.5 * ss(-0.05, 0.2, a)))
    # Haut
    fawn = np.array((0.30, 0.20, 0.12))
    dark = np.array((0.035, 0.022, 0.014))
    tm2 = ss(0.38, 0.64, mel)[:, None]
    skin = fawn * (1 - tm2) + dark * tm2
    schwarz = (1.0 - ss(0.0, 0.0075 + 0.002 * np.sin(a * 90.0), dl_all))[:, None]
    skin = skin * (1 - schwarz) + np.array((0.010, 0.009, 0.009)) * schwarz
    # um die Nase ebenfalls dunkle Haut
    sn = (1.0 - ss(0.0, 0.006, dn))[:, None]
    skin = skin * (1 - sn) + np.array((0.016, 0.014, 0.014)) * sn
    # Haut um das Auge fast schwarz
    sa = (1.0 - ss(0.005, 0.014, de))[:, None]
    skin = skin * (1 - sa) + np.array((0.007, 0.006, 0.006)) * sa
    # Mittelfurche dunkel
    sp = (np.exp(-((y / 0.0042) ** 2)) * ss(-0.010, -0.022, c) * ss(0.48, 0.494, a))[:, None]
    skin = skin * (1 - sp) + np.array((0.010, 0.009, 0.009)) * sp
    # Mundhoehle
    iu = idxU.reshape(-1)
    il = idxL.reshape(-1)
    prog2 = np.tile(prog, (Nn - it, 1))
    a_tab = np.repeat(a_[it:], Ki + 1)
    for idx, gaumen in ((iu, True), (il, False)):
        pp = prog2.reshape(-1)
        rand = (1.0 - ss(0.06, 0.17, pp))[:, None]
        zahnfl = np.array((0.30, 0.06, 0.07))
        innen = np.array((0.46, 0.15, 0.15)) if gaumen else np.array((0.24, 0.06, 0.07))
        t = ss(0.45, 0.72, pp)[:, None]
        cc = zahnfl * (1 - t) + innen * t
        cc = cc * (1 - rand) + np.array((0.012, 0.01, 0.01)) * rand
        tief = (1.0 - ss(A_RACHEN + 0.02, 0.27, a_tab))[:, None]
        cc = cc * (1 - tief) + np.array((0.012, 0.003, 0.004)) * tief
        skin[idx] = cc
    # Gesichts-Faerbung fuer Lippenband-Flaechen: Material "mund"
    skin[pol_o] = (0.01, 0.009, 0.009)
    skin[pol_u] = (0.01, 0.009, 0.009)

    # Gewichte Kiefer: zum Mundwinkel hin weich, damit die Wange als Haut mitgeht
    wk = np.zeros(nv)
    # Exterior untere Haelfte
    psi = np.zeros((Nn, Mm))
    for j in range(Mu + 1, Mm):
        t = (j - Mu) / float(Mu)
        psi[:, j] = 1.0 - np.abs(2.0 * t - 1.0)   # 0 am Rand, 1 unten in der Mitte
    a0 = A_WINKEL - 0.03 - 0.11 * psi
    a1 = A_WINKEL + 0.035 - 0.015 * psi
    aa = np.repeat(a_[:, None], Mm, axis=1)
    wl = ss(0.0, 1.0, np.clip((aa - a0) / (a1 - a0), 0, 1))
    wl[:, : Mu + 1] = 0.0
    # Oberlippe nahe dem Winkel geht ein Stueck mit (lose Haut, Winkel wird rund)
    wob = 0.42 * (1.0 - ss(A_WINKEL - 0.005, A_WINKEL + 0.085, aa)) * ss(A_WINKEL - 0.07, A_WINKEL - 0.02, aa) * (1.0 - ss(0.0, 0.035, sl))
    wl[:, : Mu + 1] = wob[:, : Mu + 1]
    wk[idxP.reshape(-1)] = wl.reshape(-1)
    # Unterlippe und untere Mundhoehle
    wk[idxLp[ic + 1 :]] = ss(A_WINKEL - 0.03, A_WINKEL + 0.035, a_[ic + 1 :])
    wk[idxLm[ic + 1 :]] = ss(A_WINKEL - 0.03, A_WINKEL + 0.035, a_[ic + 1 :])
    wk[pol_u] = 1.0
    wk[pol_o] = 0.0
    wk[il] = ss(A_WINKEL - 0.05, A_WINKEL + 0.03, a_tab)
    # Oberseite der Mundhoehle nahe dem Winkel folgt der Oberlippe
    wk[iu] = 0.42 * (1.0 - ss(A_WINKEL - 0.005, A_WINKEL + 0.085, a_tab)) * ss(A_WINKEL - 0.07, A_WINKEL - 0.02, a_tab) * (1.0 - ss(0.1, 0.5, prog2.reshape(-1)))
    # Punkte zwischen den Lippen hinter dem Winkel bleiben beim Kopf
    # (der Mundwinkel selbst liegt gemischt, damit er sich dehnt statt zu reissen)
    wk[idxP[ic, 0]] = 0.40
    wk[idxP[ic, Mu]] = 0.40
    return {
        "V": V, "F": nz.f, "T": np.array(nz.ftag), "ext": ext, "dlip": dl_all, "Lm": Lm, "mask": mask, "mel": mel,
        "red": red, "skin": skin, "wk": wk, "a_": a_, "W_": W_, "Cw_": Cw_, "T_": T_, "B_": B_, "nar": nar, "rec": rec,
        "ic": ic,
        "wallU": (InU[:, K_WALL_IDX, :].copy(), InU[:, Ki - K_WALL_IDX, :].copy()),
        "wallL": (InL[:, Ki - K_WALL_IDX, :].copy(), InL[:, K_WALL_IDX, :].copy()),
    }


KOPF = baue_kopf()
print("BAER_KOPF Punkte", len(KOPF["V"]), "Flaechen", len(KOPF["F"]))


def ring_wert(key, aa):
    """Tabellenwert an der Stelle a (nur der monotone Teil vor der Spitze)."""
    ax = KOPF["a_"]
    k = int(np.argmax(ax)) + 1
    return float(np.interp(aa, ax[:k], KOPF[key][:k]))


# ------------------------------------------------------------------ Ohren: Schalen, Oeffnung nach vorn-aussen
def baue_ohr(sd):
    E = np.array((0.026, sd * 0.157, 0.133))
    O = unit((0.62, sd * 0.60, 0.50))
    up = np.array((0.0, 0.0, 1.0))
    e1 = unit(np.cross(up, O))
    e2 = np.cross(O, e1)
    nu = 56
    R, D = 0.056, 0.044
    Ri, Di = 0.047, 0.018
    th = np.linspace(0.0, 2 * math.pi, nu, endpoint=False)
    # etwas hoeher als breit, unten versinkt der Rand im Kopffell
    rad = (np.outer(np.cos(th), e1) + np.outer(np.sin(th), e2) * 1.06)
    rows = []
    kind = []
    for sv in np.linspace(0.08, 1.0, 16):
        ang = sv * math.pi / 2
        rows.append(E - O * D * math.cos(ang) + rad * R * math.sin(ang))
        kind.append(3)
    for ang in np.linspace(0.3, 2.8, 6):   # gerundeter Rand
        rr = (R + Ri) / 2 + (R - Ri) / 2 * math.cos(ang)
        rows.append(E + O * 0.008 * math.sin(ang) + rad * rr)
        kind.append(3 if ang < 1.5 else 4)
    for sv in np.linspace(1.0, 0.1, 14):
        ang = sv * math.pi / 2
        rows.append(E - O * Di * math.cos(ang) + rad * Ri * math.sin(ang))
        kind.append(4)
    rows = np.array(rows)
    pol_a = E - O * D
    pol_i = E - O * Di
    return rows, np.array(kind), pol_a, pol_i, O


# ------------------------------------------------------------------ Zehen und Krallen
ZEHEN = []
for sd, nm in ((-1, "R"), (1, "L")):
    for k in range(-2, 3):
        # Vorderpfote
        ZEHEN.append(dict(bone="pranke" + nm, c=np.array((0.572 - 0.012 * k * k, sd * 0.292 + k * 0.046, 0.035)),
                          ax=unit((1.0, 0.17 * k, -0.03)), ln=0.048, rl=0.0245, rv=0.033,
                          krallen=(0.100 - 0.009 * abs(k) - 0.006 * max(0, -k * sd), 0.0135), sd=sd))
        # Hinterfuss
        ZEHEN.append(dict(bone="fuss" + nm, c=np.array((-0.352 - 0.010 * k * k, sd * 0.318 + k * 0.042, 0.031)),
                          ax=unit((1.0, 0.13 * k, -0.03)), ln=0.043, rl=0.0225, rv=0.030,
                          krallen=(0.060 - 0.005 * abs(k), 0.0115), sd=sd))


def baue_zeh(z):
    nu, nv = 22, 16
    ax = z["ax"]
    upv = np.array((0.0, 0.0, 1.0))
    lat = unit(np.cross(upv, ax))
    up = np.cross(ax, lat)
    pts = []
    for v in np.linspace(0.12, math.pi - 0.12, nv):
        ring = []
        for u in np.linspace(0.0, 2 * math.pi, nu, endpoint=False):
            sv = math.sin(v)
            q = z["c"] + ax * z["ln"] * math.cos(v) + lat * z["rl"] * sv * math.cos(u) + up * z["rv"] * sv * math.sin(u)
            ring.append(q)
        pts.append(ring)
    pts = np.array(pts)
    # Sohle flach, nie unter den Boden
    pts[..., 2] = np.maximum(pts[..., 2], 0.004)
    return pts


# ------------------------------------------------------------------ Alles in EIN Netz: Koerper + Kopf + Ohren + Zehen
nb_body = len(body.data.vertices)
_bv = np.zeros(nb_body * 3)
body.data.vertices.foreach_get("co", _bv)
_bv = _bv.reshape(-1, 3)
_bpoly = [tuple(p.vertices) for p in body.data.polygons]

HV = l2w(KOPF["V"])
off_kopf = nb_body
all_v = [_bv, HV]
all_f = list(_bpoly)
ftag = [0] * len(_bpoly)

# Normalen des Kopfes (ohne Koerper) ueber bmesh richten: die Flaechen des Kopfes bilden eine geschlossene Huelle
_tmp = bpy.data.meshes.new("tmp")
_tmp.from_pydata(HV.tolist(), [], KOPF["F"])
_bm = bmesh.new()
_bm.from_mesh(_tmp)
bmesh.ops.recalc_face_normals(_bm, faces=_bm.faces)
_kf = [tuple(v.index for v in f.verts) for f in _bm.faces]
_bm.free()
bpy.data.meshes.remove(_tmp)
for fc, tg in zip(_kf, KOPF["T"].tolist()):
    all_f.append(tuple(i + off_kopf for i in fc))
    ftag.append(tg)
cnt = off_kopf + len(HV)

# Felder ueber alle Punkte (Koerper = 0)
PF = {}


def feld(n):
    return np.zeros(n)


ear_info = []
extra_L = []     # (Laenge, Dichte, Melanin, Roetung, Haut r,g,b) je Zusatzpunkt, Gruppe
extra_grp = []   # d_ohr_aussen, d_ohr_innen, d_zeh
extra_flow = []  # Richtung je Punkt (Welt)
extra_bone = []
for sd in (-1, 1):
    rows, kind, pol_a, pol_i, O = baue_ohr(sd)
    nr, nu = rows.shape[:2]
    vr = l2w(rows).reshape(-1, 3)
    va = l2w(pol_a)
    vi = l2w(pol_i)
    start = cnt
    all_v.append(vr)
    all_v.append(va[None])
    all_v.append(vi[None])
    ia = start + nr * nu
    ii = ia + 1
    cnt += nr * nu + 2
    W_o = rot_l2w(O)
    for r in range(nr):
        for u in range(nu):
            p = vr[r * nu + u]
            if kind[r] == 3:
                extra_L.append((0.013, 1.0, 0.74, 0.27, 0.03, 0.02, 0.014))
                extra_grp.append(0)
                extra_flow.append(p - va)
            else:
                _r0 = int(np.argmax(kind == 4))
                tt = (r - _r0) / float(max(nr - 1 - _r0, 1))
                extra_L.append((lerp(0.036, 0.016, float(ss(0.1, 0.7, tt))), 1.0 - 0.5 * float(ss(0.4, 0.9, tt)), lerp(0.60, 0.84, float(ss(0.1, 0.55, tt))), 0.25,
                                lerp(0.07, 0.012, float(ss(0.1, 0.6, tt))), lerp(0.045, 0.009, float(ss(0.1, 0.6, tt))), lerp(0.03, 0.008, float(ss(0.1, 0.6, tt)))))
                extra_grp.append(1)
                extra_flow.append(unit(p - vi) + W_o * 0.6)
            extra_bone.append("kopf")
    for lst, q in ((extra_L, (0.02, 1.0, 0.86, 0.33, 0.03, 0.02, 0.014)), (extra_L, (0.03, 1.0, 0.74, 0.31, 0.05, 0.03, 0.02))):
        lst.append(q)
    extra_grp += [0, 1]
    extra_flow += [W_o, W_o]
    extra_bone += ["kopf", "kopf"]
    for r in range(nr - 1):
        for u in range(nu):
            q = (start + r * nu + u, start + (r + 1) * nu + u, start + (r + 1) * nu + (u + 1) % nu, start + r * nu + (u + 1) % nu)
            all_f.append(q)
            ftag.append(3 if kind[r] == 3 else 4)
    for u in range(nu):
        all_f.append((ia, start + (u + 1) % nu, start + u))
        ftag.append(3)
        all_f.append((ii, start + (nr - 1) * nu + u, start + (nr - 1) * nu + (u + 1) % nu))
        ftag.append(4)

zeh_gr = {}
for z in ZEHEN:
    pts = baue_zeh(z)
    nr, nu = pts.shape[:2]
    start = cnt
    pa = z["c"] + z["ax"] * z["ln"]
    pb_ = z["c"] - z["ax"] * z["ln"]
    pa[2] = max(pa[2], 0.004)
    all_v.append(pts.reshape(-1, 3))
    all_v.append(pa[None])
    all_v.append(pb_[None])
    ia = start + nr * nu
    ib = ia + 1
    cnt += nr * nu + 2
    for q in pts.reshape(-1, 3):
        unten = q[2] < z["c"][2] - 0.012
        vorn = float(ss(0.018, 0.043, (q - z["c"]).dot(z["ax"])))
        extra_L.append((lerp(0.019, 0.010, vorn), 0.0 if unten else 1.0, 0.70, 0.22,
                        0.012 if unten else 0.03, 0.01 if unten else 0.02, 0.01 if unten else 0.014))
        extra_grp.append(2)
        extra_flow.append(z["ax"] + np.array((0.0, 0.0, -0.08)))
        extra_bone.append(z["bone"])
    for lst in range(2):
        extra_L.append((0.012, 0.0, 0.88, 0.32, 0.012, 0.01, 0.01))
        extra_grp.append(2)
        extra_flow.append(z["ax"])
        extra_bone.append(z["bone"])
    # Flaechen so gewickelt, dass die Normale nach aussen zeigt (wird unten global geprueft)
    for r in range(nr - 1):
        for u in range(nu):
            all_f.append((start + r * nu + u, start + r * nu + (u + 1) % nu, start + (r + 1) * nu + (u + 1) % nu, start + (r + 1) * nu + u))
            ftag.append(5)
    for u in range(nu):
        all_f.append((ia, start + u, start + (u + 1) % nu))
        ftag.append(5)
        all_f.append((ib, start + (nr - 1) * nu + (u + 1) % nu, start + (nr - 1) * nu + u))
        ftag.append(5)

ALLV = np.concatenate(all_v, axis=0)
n_all = len(ALLV)
n_head = len(HV)
n_extra = n_all - nb_body - n_head
ftag = np.array(ftag)
print("BAER_NETZ Punkte", n_all, "Koerper", nb_body, "Kopf", n_head, "Zusatz", n_extra, "Flaechen", len(all_f))

me = bpy.data.meshes.new("baer_netz")
me.from_pydata(ALLV.tolist(), [], all_f)
me.update()
me.shade_smooth()
_alt = body.data
body.data = me
bpy.data.meshes.remove(_alt)
# Ohren und Zehen nach aussen richten
_bm = bmesh.new()
_bm.from_mesh(me)
_bm.faces.ensure_lookup_table()
bmesh.ops.recalc_face_normals(_bm, faces=[f for f, t in zip(_bm.faces, ftag.tolist()) if t >= 3])
_bm.to_mesh(me)
_bm.free()
me.update()
me.materials.append(fur)             # 0 Koerperhaut
hm_slot = bpy.data.materials.new("haar")
me.materials.append(hm_slot)         # 1 Koerperhaar
me.materials.append(KOPFHAUT)        # 2
me.materials.append(MUND)            # 3
hk_slot = bpy.data.materials.new("haar_kopf")
me.materials.append(hk_slot)         # 4 Kopfhaar
body_tris = sum(len(p.vertices) - 2 for p in me.polygons)

# Material je Flaeche
loop_vi = np.zeros(len(me.loops), dtype=np.int32)
me.loops.foreach_get("vertex_index", loop_vi)
p_start = np.zeros(len(me.polygons), dtype=np.int32)
p_tot = np.zeros(len(me.polygons), dtype=np.int32)
me.polygons.foreach_get("loop_start", p_start)
me.polygons.foreach_get("loop_total", p_tot)
p_nor = np.zeros(len(me.polygons) * 3)
me.polygons.foreach_get("normal", p_nor)
p_nor = p_nor.reshape(-1, 3)
Pall = ALLV
_lp = Pall[loop_vi]
_cen = np.add.reduceat(_lp, p_start, axis=0) / p_tot[:, None]

dl_v = np.full(n_all, 9.0)
dl_v[off_kopf:off_kopf + n_head] = KOPF["dlip"]
_dlf = np.minimum.reduceat(dl_v[loop_vi], p_start)
matidx = np.zeros(len(me.polygons), dtype=np.int32)
matidx[ftag == 1] = 2
matidx[ftag == 2] = 3
matidx[ftag >= 3] = 2
me.polygons.foreach_set("material_index", matidx)

# ------------------------------------------------------------------ Strich je Flaeche: UV so gelegt, dass +V die Fellrichtung ist
ey = np.array((AUGE_L[0], AUGE_L[1], AUGE_L[2]))


def fluss_kopf(cen_l, nor_l):
    a, y, c = cen_l[:, 0], cen_l[:, 1], cen_l[:, 2]
    D = np.zeros_like(cen_l)
    D[:, 0] = -1.0
    # Stirnseite der Schnauze: strahlig von der Lippenmitte weg
    w = ss(0.46, 0.497, a)[:, None]
    rad = np.stack((0.0 * a, y, c + 0.002), axis=1)
    rad = rad / np.maximum(np.linalg.norm(rad, axis=1, keepdims=True), 1e-6)
    D = D * (1 - w) + rad * w
    # Wange und Hals: nach hinten-unten
    wd = (1 - ss(0.14, 0.30, a)) * (1 - ss(-0.08, 0.05, c))
    D[:, 2] -= 0.9 * wd
    # Hinterkopf: leicht auseinander
    wl = (1 - ss(0.06, 0.24, a)) * ss(0.02, 0.1, c)
    D[:, 1] += np.sign(y) * 0.32 * wl
    # Seitlich an der Schnauze: minimal nach unten
    wz = ss(0.28, 0.34, a) * (1 - w[:, 0]) * ss(0.012, 0.05, np.abs(y))
    D[:, 2] -= 0.16 * wz
    # Oberlippe: Haar faellt ueber die Lippenlinie
    wo = ss(0.27, 0.33, a) * (1 - ss(0.47, 0.495, a)) * (1 - ss(-0.03, 0.0, c)) * ss(-0.06, -0.04, c)
    D[:, 2] -= 0.55 * wo
    # Um die Augen: strahlig weg vom Auge
    for s_ in (-1, 1):
        E = np.array((ey[0], s_ * ey[1], ey[2]))
        r = cen_l - E
        rl = np.linalg.norm(r, axis=1, keepdims=True)
        wr = (0.8 * (1 - ss(0.022, 0.040, rl[:, 0])) * (1 - 0.85 * ss(0.002, 0.02, r[:, 2])))[:, None]
        D = D * (1 - wr) + (r / np.maximum(rl, 1e-5)) * wr
    D = D - (D * nor_l).sum(axis=1, keepdims=True) * nor_l
    return D / np.maximum(np.linalg.norm(D, axis=1, keepdims=True), 1e-6)


F_D = np.zeros((len(me.polygons), 3))
F_D[:, 0] = -1.0
_mk = ftag == 1
if _mk.any():
    _dl = fluss_kopf(w2l(_cen[_mk]), rot_w2l(p_nor[_mk]))
    F_D[_mk] = rot_l2w(_dl)
# Ohren und Zehen: Richtung je Punkt gemittelt
fv = np.zeros((n_all, 3))
fv[off_kopf + n_head:] = np.array(extra_flow)
_mk2 = ftag >= 3
if _mk2.any():
    _fm = np.add.reduceat(fv[loop_vi], p_start, axis=0)
    _fm = _fm - (_fm * p_nor).sum(axis=1, keepdims=True) * p_nor
    _fm = _fm / np.maximum(np.linalg.norm(_fm, axis=1, keepdims=True), 1e-6)
    F_D[_mk2] = _fm[_mk2]
# UV: v = P*D, u = P*(N x D), je Flaeche fuer sich
f_of_loop = np.repeat(np.arange(len(me.polygons)), p_tot)
_D = F_D[f_of_loop]
_Nn = p_nor[f_of_loop]
_uv = np.stack(((_lp * np.cross(_Nn, _D)).sum(axis=1), (_lp * _D).sum(axis=1)), axis=1) * 8.0
uvl = me.uv_layers.new(name="strich")
uvl.data.foreach_set("uv", _uv.reshape(-1))
me.uv_layers.active = uvl

# ------------------------------------------------------------------ Farbattribute und Gruppen
skin_all = np.zeros((n_all, 4))
skin_all[:, 3] = 1.0
skin_all[off_kopf:off_kopf + n_head, :3] = KOPF["skin"]
fell_all = np.zeros((n_all, 4))
fell_all[:, 3] = 1.0
fell_all[off_kopf:off_kopf + n_head, 0] = KOPF["mel"]
fell_all[off_kopf:off_kopf + n_head, 1] = KOPF["red"]
_ex = np.array(extra_L)
skin_all[off_kopf + n_head:, :3] = _ex[:, 4:7]
fell_all[off_kopf + n_head:, 0] = _ex[:, 2]
fell_all[off_kopf + n_head:, 1] = _ex[:, 3]
ch = me.color_attributes.new("hautfarbe", "FLOAT_COLOR", "POINT")
ch.data.foreach_set("color", skin_all.reshape(-1))
cf = me.color_attributes.new("fellfarbe", "BYTE_COLOR", "CORNER")
cf.data.foreach_set("color", fell_all[loop_vi].reshape(-1))

# Knochengewichte
for nm in NAMES + ["kiefer"]:
    body.vertex_groups.new(name=nm)
VG = body.vertex_groups
for i, wmap in enumerate(WEIGHTS):
    top = sorted(wmap.items(), key=lambda kv: -kv[1])[:4]
    tot = sum(v for _, v in top)
    for k, v in top:
        VG[k].add([i], v / tot, "REPLACE")
# Kopf: hinten wie der Koerper ueber den Abstand zu den Knochen, vorn ganz am Kopfknochen
_seg_np = {k: (np.array(SEG[k][0]), np.array(SEG[k][1])) for k in ("brust", "hals", "kopf")}


def segd_np(p, a, c):
    ac = c - a
    t = np.clip(((p - a) @ ac) / (ac @ ac), 0.0, 1.0)
    return np.linalg.norm(p - (a + t[:, None] * ac), axis=1)


_ww = {}
for k in _seg_np:
    _ww[k] = 1.0 / np.maximum(segd_np(HV, *_seg_np[k]), 0.03) ** 3
_tot = sum(_ww.values())
_ha = KOPF["V"][:, 0]
_tk = ss(-0.04, 0.07, _ha)
_final = {}
for k in _ww:
    _final[k] = _ww[k] / _tot * (1 - _tk)
_final["kopf"] = _final["kopf"] + _tk
_wk = KOPF["wk"]
for k in _final:
    _final[k] = _final[k] * (1 - _wk)
_final["kiefer"] = _wk
for k, arr in _final.items():
    g = VG[k]
    for i in np.nonzero(arr > 0.002)[0].tolist():
        g.add([off_kopf + i], float(arr[i]), "REPLACE")
for i, bn in enumerate(extra_bone):
    VG[bn].add([off_kopf + n_head + i], 1.0, "REPLACE")

mod = body.modifiers.new("skelett", "ARMATURE")
mod.object = ao
body.parent = ao

# ------------------------------------------------------------------ Fell-Gruppen
GN = ("d_koerper", "d_bein", "l_koerper", "l_bein", "d_sch", "l_sch", "d_kop", "l_kop", "d_wan", "l_wan", "d_oa", "l_oa", "d_oi", "l_oi", "d_zeh", "l_zeh")
G = {n: body.vertex_groups.new(name=n) for n in GN}
_paw = [(np.array((0.555, sd * 0.292, 0.035)), 0.13) for sd in (-1, 1)] + [(np.array((-0.37, sd * 0.318, 0.03)), 0.12) for sd in (-1, 1)]
_bl = w2l(_bv)
for i in range(nb_body):
    c = _bv[i]
    al = _bl[i, 0]
    head = sstep(-0.13, -0.035, al)
    leg = (1.0 - sstep(lz(0.22), lz(0.56), c[2])) * (1.0 - head)
    # Die Bauchlinie zwischen den Beinen bleibt Koerperfell
    if -0.25 < c[0] < 0.12:
        leg *= 0.15
    rest = max(0.0, 1.0 - head - leg)
    G["d_koerper"].add([i], rest, "REPLACE")
    G["d_bein"].add([i], leg, "REPLACE")
    # Laengen: Nackenmaehne und Bauchfransen lang, Ruecken mittel
    lk = 0.72
    lk += 0.28 * sstep(0.1, 0.45, c[0]) * sstep(lz(0.62), lz(0.95), c[2]) * (1 - sstep(0.75, 0.95, c[0]))
    lk += 0.28 * (1 - sstep(lz(0.34), lz(0.48), c[2])) * (1 - sstep(0.12, 0.3, abs(c[0] + 0.1)))
    lk *= 1.0 - 0.60 * sstep(0.50, 0.93, c[0])
    G["l_koerper"].add([i], min(1.0, lk), "REPLACE")
    lb = 0.26 + 0.74 * sstep(0.09, lz(0.34), c[2])
    # An der Pfotenvorderkante kurz, sonst deckt das Beinfell die Zehen zu
    for q, rr in _paw:
        d = float(np.linalg.norm(c - q))
        lb *= 0.42 + 0.58 * sstep(0.05, rr, d)
    G["l_bein"].add([i], lb, "REPLACE")

_Lm = KOPF["Lm"]
_ms = KOPF["mask"]
# Drei Systeme mit fliessendem Uebergang: je Haarlaenge passende Dichte
_ds = (1 - ss(0.016, 0.030, _Lm)) * _ms
_dk = ss(0.016, 0.028, _Lm) * (1 - ss(0.066, 0.10, _Lm)) * _ms
_dw = ss(0.042, 0.066, _Lm) * _ms
_ls = np.clip(_Lm / 0.018, 0.2, 1.0)
_lk = np.clip(_Lm / 0.075, 0.2, 1.0)
_lw = np.clip(_Lm / 0.155, 0.2, 1.0)
for i in range(n_head):
    j = off_kopf + i
    if _ds[i] > 0.002:
        G["d_sch"].add([j], float(_ds[i]), "REPLACE")
    if _dk[i] > 0.002:
        G["d_kop"].add([j], float(_dk[i]), "REPLACE")
    if _dw[i] > 0.002:
        G["d_wan"].add([j], float(_dw[i]), "REPLACE")
    G["l_sch"].add([j], float(_ls[i]), "REPLACE")
    G["l_kop"].add([j], float(_lk[i]), "REPLACE")
    G["l_wan"].add([j], float(_lw[i]), "REPLACE")
_o0 = off_kopf + n_head
for i in range(n_extra):
    j = _o0 + i
    q = _ex[i]
    gn = extra_grp[i]
    if gn == 0:
        G["d_oa"].add([j], float(q[1]), "REPLACE")
        G["l_oa"].add([j], float(q[0] / 0.024), "REPLACE")
    elif gn == 1:
        G["d_oi"].add([j], float(q[1]), "REPLACE")
        G["l_oi"].add([j], float(q[0] / 0.05), "REPLACE")
    else:
        if q[1] > 0:
            G["d_zeh"].add([j], float(q[1]), "REPLACE")
        G["l_zeh"].add([j], float(q[0] / 0.02), "REPLACE")

# ------------------------------------------------------------------ Haarmaterial Koerper
hm = hm_slot
hm.use_nodes = True
N, L = hm.node_tree.nodes, hm.node_tree.links
N.remove(N["Principled BSDF"])
hb = N.new("ShaderNodeBsdfHairPrincipled")
hb.parametrization = "MELANIN"
hb.inputs["Melanin Redness"].default_value = 0.26
hb.inputs["Roughness"].default_value = 0.34
hb.inputs["Radial Roughness"].default_value = 0.8
hb.inputs["Coat"].default_value = 0.0
hi = N.new("ShaderNodeHairInfo")
tc = N.new("ShaderNodeTexCoord")
sep = N.new("ShaderNodeSeparateXYZ")
L.new(tc.outputs["Generated"], sep.inputs[0])
nz = N.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 9
nz.inputs["Detail"].default_value = 6
L.new(tc.outputs["Generated"], nz.inputs["Vector"])
add1 = N.new("ShaderNodeMath")
add1.operation = "ADD"
L.new(maprange(N, L, hi.outputs["Random"], 0.0, 1.0, -0.07, 0.07), add1.inputs[0])
L.new(maprange(N, L, nz.outputs["Fac"], 0.30, 0.70, 0.71, 0.89), add1.inputs[1])
add2 = N.new("ShaderNodeMath")
add2.operation = "ADD"
L.new(add1.outputs[0], add2.inputs[0])
L.new(maprange(N, L, sep.outputs[2], 0.14, 0.42, 0.12, 0.0), add2.inputs[1])       # Beine dunkler
add3 = N.new("ShaderNodeMath")
add3.operation = "SUBTRACT"
L.new(add2.outputs[0], add3.inputs[0])
L.new(maprange(N, L, sep.outputs[2], 0.56, 0.92, 0.0, 0.12), add3.inputs[1])       # Ruecken heller
add4 = N.new("ShaderNodeMath")
add4.operation = "SUBTRACT"
add4.use_clamp = True
L.new(add3.outputs[0], add4.inputs[0])
kopfhell = N.new("ShaderNodeMath")
kopfhell.operation = "ADD"
L.new(maprange(N, L, hi.outputs["Intercept"], 0.45, 1.0, 0.0, 0.2), kopfhell.inputs[0])  # helle Spitzen
L.new(maprange(N, L, sep.outputs[0], 0.72, 0.82, 0.0, 0.08), kopfhell.inputs[1])
L.new(kopfhell.outputs[0], add4.inputs[1])
L.new(add4.outputs[0], hb.inputs["Melanin"])
hb.inputs["Random Color"].default_value = 0.1
L.new(hb.outputs[0], N["Material Output"].inputs["Surface"])

# Haarmaterial Kopf: Melanin und Roetung kommen je Haarwurzel aus dem Netz
hk = hk_slot
hk.use_nodes = True
N, L = hk.node_tree.nodes, hk.node_tree.links
N.remove(N["Principled BSDF"])
hbk = N.new("ShaderNodeBsdfHairPrincipled")
hbk.parametrization = "MELANIN"
hbk.inputs["Roughness"].default_value = 0.5
hbk.inputs["Radial Roughness"].default_value = 0.8
hbk.inputs["Coat"].default_value = 0.0
hbk.inputs["Random Color"].default_value = 0.08
hik = N.new("ShaderNodeHairInfo")
atk = N.new("ShaderNodeAttribute")
atk.attribute_type = "GEOMETRY"
atk.attribute_name = "fellfarbe"
spk = N.new("ShaderNodeSeparateColor")
spk.mode = "RGB"
L.new(atk.outputs["Color"], spk.inputs[0])
tck = N.new("ShaderNodeTexCoord")
nzk = N.new("ShaderNodeTexNoise")
nzk.inputs["Scale"].default_value = 60
nzk.inputs["Detail"].default_value = 5
L.new(tck.outputs["Object"], nzk.inputs["Vector"])
ak1 = N.new("ShaderNodeMath")
ak1.operation = "ADD"
L.new(spk.outputs[0], ak1.inputs[0])
L.new(maprange(N, L, hik.outputs["Random"], 0.0, 1.0, -0.055, 0.055), ak1.inputs[1])
ak2 = N.new("ShaderNodeMath")
ak2.operation = "ADD"
L.new(ak1.outputs[0], ak2.inputs[0])
L.new(maprange(N, L, nzk.outputs["Fac"], 0.32, 0.68, -0.035, 0.035), ak2.inputs[1])
ak3 = N.new("ShaderNodeMath")
ak3.operation = "SUBTRACT"
ak3.use_clamp = True
L.new(ak2.outputs[0], ak3.inputs[0])
L.new(maprange(N, L, hik.outputs["Intercept"], 0.5, 1.0, 0.0, 0.13), ak3.inputs[1])     # helle Spitzen
L.new(ak3.outputs[0], hbk.inputs["Melanin"])
L.new(spk.outputs[1], hbk.inputs["Melanin Redness"])
L.new(hbk.outputs[0], N["Material Output"].inputs["Surface"])


def fell(name, count, length, normal, align, dens, lng, kids, clump, rough1, rough2, radius, seed):
    body.modifiers.new(name, "PARTICLE_SYSTEM")
    ps = body.particle_systems[-1]
    ps.seed = seed
    st = ps.settings
    st.name = name
    st.type = "HAIR"
    st.use_advanced_hair = True
    st.count = max(10, int(count * FUR_BODY))
    st.userjit = 24
    st.hair_length = length
    st.hair_step = 5
    st.display_step = 3
    st.emit_from = "FACE"
    st.normal_factor = normal
    st.object_align_factor = align
    st.factor_random = normal * 0.22
    st.brownian_factor = 0.002
    st.child_type = "INTERPOLATED"
    st.child_percent = 2
    st.rendered_child_count = kids
    st.child_length = 0.86
    st.child_length_threshold = 0.25
    st.clump_factor = clump
    st.clump_shape = 0.2
    st.use_clump_noise = clump > 0.3
    st.clump_noise_size = 0.45
    st.roughness_1 = rough1
    st.roughness_1_size = 0.55
    st.roughness_endpoint = rough1 * 1.1
    st.roughness_2 = rough2
    st.material_slot = "haar"
    st.root_radius = 1.0
    st.tip_radius = 0.03
    st.radius_scale = radius
    ps.vertex_group_density = dens
    ps.vertex_group_length = lng


def fell_strich(name, count, lang, anteil_n, dens, lng, kids, clump, rough1, rough2, radius, seed, align=(0.0, 0.0, 0.0), rnd=0.18, render_step=3):
    """Haar, das dem UV-Strich folgt: lang = Meter bei Gruppengewicht 1, anteil_n = Anteil der Flaechennormale."""
    body.modifiers.new(name, "PARTICLE_SYSTEM")
    ps = body.particle_systems[-1]
    ps.seed = seed
    st = ps.settings
    st.name = name
    st.type = "HAIR"
    st.use_advanced_hair = True
    st.count = max(10, int(count * FUR_HEAD))
    st.hair_step = 4
    st.display_step = 2
    st.render_step = render_step
    st.emit_from = "FACE"
    v = lang / 4.0
    st.normal_factor = v * anteil_n
    st.tangent_factor = v * math.sqrt(max(0.0, 1.0 - anteil_n * anteil_n))
    st.tangent_phase = 0.0
    st.object_align_factor = align
    st.factor_random = v * rnd
    st.brownian_factor = v * 0.015
    st.child_type = "INTERPOLATED"
    st.child_percent = 2
    st.rendered_child_count = kids
    st.child_length = 0.88
    st.child_length_threshold = 0.3
    st.clump_factor = clump
    st.clump_shape = 0.1
    st.use_clump_noise = clump > 0.25
    st.clump_noise_size = 0.5
    st.roughness_1 = rough1
    st.roughness_1_size = 0.5
    st.roughness_endpoint = rough1 * 1.1
    st.roughness_2 = rough2
    st.material_slot = "haar_kopf"
    st.root_radius = 1.0
    st.tip_radius = 0.05
    st.radius_scale = radius
    ps.vertex_group_density = dens
    ps.vertex_group_length = lng


fell("unterwolle", 100000, 0.098, 0.052, (-0.038, 0.0, -0.024), "d_koerper", "l_koerper", 18, 0.66, 0.009, 0.007, 0.0028, 11)
fell("deckhaar", 14000, 0.15, 0.066, (-0.052, 0.0, -0.036), "d_koerper", "l_koerper", 9, 0.86, 0.013, 0.012, 0.0034, 12)
fell("beinfell", 60000, 0.082, 0.046, (-0.012, 0.0, -0.028), "d_bein", "l_bein", 14, 0.56, 0.008, 0.005, 0.0029, 13)
# Gesicht: Schnauze sehr kurz und ohne Klumpen, Stirn mittel, Wange und Nacken lang
fell_strich("schnauzenfell", 9000, 0.018, 0.30, "d_sch", "l_sch", 9, 0.0, 0.0007, 0.0004, 0.00085, 21, render_step=2)
fell_strich("stirnfell", 14000, 0.075, 0.30, "d_kop", "l_kop", 8, 0.2, 0.0034, 0.0022, 0.00145, 22, rnd=0.22)
fell_strich("wangenfell", 11000, 0.17, 0.52, "d_wan", "l_wan", 11, 0.62, 0.016, 0.012, 0.0026, 23, align=(-0.005, 0.0, -0.004), rnd=0.34)
fell_strich("ohr_aussen", 3000, 0.024, 0.16, "d_oa", "l_oa", 6, 0.1, 0.001, 0.0006, 0.0011, 24)
fell_strich("ohr_innen", 3000, 0.05, 0.68, "d_oi", "l_oi", 8, 0.25, 0.002, 0.0012, 0.0012, 25)
fell_strich("zehenfell", 7000, 0.024, 0.34, "d_zeh", "l_zeh", 9, 0.08, 0.001, 0.0006, 0.00125, 26, render_step=2)


# ------------------------------------------------------------------ Teile, die am Knochen haengen
def on_bone(o, bname):
    bn = arm.bones[bname]
    mw = o.matrix_world.copy()
    o.parent = ao
    o.parent_type = "BONE"
    o.parent_bone = bname
    bpy.context.view_layer.update()
    tail_world = ao.matrix_world @ bn.matrix_local @ Matrix.Translation((0, bn.length, 0))
    o.matrix_parent_inverse = tail_world.inverted()
    o.matrix_basis = mw


def teil(name, verts, faces, mat, smooth=True):
    m = bpy.data.meshes.new(name)
    m.from_pydata(np.asarray(verts).tolist(), [], faces)
    m.update()
    m.materials.append(mat)
    if smooth:
        m.shade_smooth()
    o = bpy.data.objects.new(name, m)
    col.objects.link(o)
    return o


def rohr(pts, ra, rb, lat_ref, nseg=12):
    """Rohr entlang einer Mittellinie: ra quer (seitlich), rb hoch. Spitze und Wurzel geschlossen."""
    pts = np.asarray(pts)
    n = len(pts)
    t_ = np.gradient(pts, axis=0)
    t_ = t_ / np.maximum(np.linalg.norm(t_, axis=1, keepdims=True), 1e-9)
    lat = np.asarray(lat_ref) - (t_ @ np.asarray(lat_ref))[:, None] * t_
    lat = lat / np.maximum(np.linalg.norm(lat, axis=1, keepdims=True), 1e-9)
    nor = np.cross(t_, lat)
    v = []
    fp = []
    th = np.linspace(0.0, 2 * math.pi, nseg, endpoint=False)
    for i in range(n):
        for tt in th:
            v.append(pts[i] + lat[i] * ra[i] * math.cos(tt) + nor[i] * rb[i] * math.sin(tt))
    wur = len(v)
    v.append(pts[0])
    spi = len(v)
    v.append(pts[-1] + t_[-1] * rb[-1])
    for i in range(n - 1):
        for k in range(nseg):
            fp.append((i * nseg + k, i * nseg + (k + 1) % nseg, (i + 1) * nseg + (k + 1) % nseg, (i + 1) * nseg + k))
    for k in range(nseg):
        fp.append((wur, (k + 1) % nseg, k))
        fp.append((spi, (n - 1) * nseg + k, (n - 1) * nseg + (k + 1) % nseg))
    return np.array(v), fp


def bez(p0, p1, p2, p3, n):
    t = np.linspace(0.0, 1.0, n)[:, None]
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


# Nasenpolster: Polarnetz mit Umriss, Woelbung, Mittelfurche und kommafoermigen Nasenloechern
def baue_nase():
    nr, nt = 110, 320
    c0 = NASE_C
    a_rim = 0.488
    dep = 0.0255
    rr = np.linspace(0.0, 1.0, nr + 1)
    th = np.linspace(0.0, 2 * math.pi, nt, endpoint=False)
    R, Th = np.meshgrid(rr, th, indexing="ij")
    ct = np.cos(Th)
    st = np.sin(Th)
    nn = 3.0
    rho = (np.abs(ct) ** nn + np.abs(st) ** nn) ** (-1.0 / nn)
    unten = np.maximum(-st, 0.0)
    hw = 0.0425 * (1.0 - 0.46 * unten ** 1.2)
    Y = R * rho * ct * hw
    Z = R * rho * st * np.where(st > 0, 0.0265, 0.0305)
    Z = Z - 0.0035 * np.exp(-((Y / 0.012) ** 2)) * ss(0.45, 1.0, R * np.maximum(st, 0.0))   # leichte Kerbe oben
    A = a_rim + dep * np.maximum(1.0 - R ** 3.0, 0.0) ** 0.55
    # Oberseite laeuft nach hinten in den Nasenruecken
    A = A - 0.009 * ss(0.002, 0.026, Z)
    # Seitlich rundet es sich nach hinten
    A = A - 0.006 * (np.abs(Y) / 0.0425) ** 2
    farbe = np.zeros(R.shape + (3,))
    farbe[...] = (0.030, 0.0285, 0.0285)
    # Nasenloecher: je ein Komma, Kopf innen, Schweif laeuft nach aussen und leicht nach unten aus
    tiefe = np.zeros_like(R)
    wulst = np.zeros_like(R)
    for sd in (-1.0, 1.0):
        p0 = np.array((sd * 0.0155, 0.0015))
        p1 = np.array((sd * 0.0275, 0.0060))
        p2 = np.array((sd * 0.0375, -0.0020))
        p3 = np.array((sd * 0.0408, -0.0105))
        best = np.full(R.shape, 9.0)
        dmax = np.zeros_like(R)
        for t in np.linspace(0.0, 1.0, 40):
            b = (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3
            rad = lerp(0.0086, 0.0016, t ** 0.75)
            dpt = lerp(0.013, 0.0022, t ** 0.8)
            dd = np.hypot(Y - b[0], (Z - b[1]) * 1.05) / rad
            bess = dd < best
            best = np.where(bess, dd, best)
            dmax = np.where(bess, dpt, dmax)
        tiefe = np.maximum(tiefe, dmax * (1.0 - ss(0.45, 1.05, best)))
        wulst = np.maximum(wulst, np.exp(-(((best - 1.45) / 0.6) ** 2)))
        farbe = farbe * (1 - (1 - ss(0.5, 1.1, best))[..., None]) + np.array((0.0018, 0.0016, 0.0016)) * (1 - ss(0.5, 1.1, best))[..., None]
    A = A - tiefe + 0.0012 * wulst
    # Mittelfurche: von der Mitte nach unten, oben nur angedeutet
    furche = np.exp(-((Y / 0.0034) ** 2)) * (0.0035 * (1 - ss(-0.016, 0.0, Z)) + 0.0009 * ss(-0.01, 0.02, Z))
    A = A - furche
    farbe = farbe * (1 - 0.6 * (furche / 0.0035)[..., None]) + np.array((0.006, 0.005, 0.005)) * 0.6 * (furche / 0.0035)[..., None]
    q = np.stack((A, Y, Z + c0), axis=-1)
    V = l2w(q).reshape(-1, 3)
    faces = []
    nrr = nr + 1
    for i in range(nr):
        for j in range(nt):
            a = i * nt + j
            b = i * nt + (j + 1) % nt
            cc = (i + 1) * nt + (j + 1) % nt
            d = (i + 1) * nt + j
            if i == 0:
                faces.append((a, cc, d))
            else:
                faces.append((a, b, cc, d))
    o = teil("nase", V, faces, NASE)
    ca = o.data.color_attributes.new("hautfarbe", "FLOAT_COLOR", "POINT")
    fl = np.concatenate((farbe.reshape(-1, 3), np.ones((farbe.size // 3, 1))), axis=1)
    ca.data.foreach_set("color", fl.reshape(-1))
    # Ausrichtung pruefen: Normalen nach vorn
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bm.normal_update()
    sm_ = sum(f.normal.x for f in bm.faces)
    if sm_ < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(o.data)
    bm.free()
    return o


# Auge und Lid
def baue_auge(sd):
    E, g, _e1, _e2 = augen_rahmen(sd)
    E_w = l2w(E)
    g_w = rot_l2w(g)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=AUGE_R_ * KOPF_S, location=tuple(E_w))
    aug = bpy.context.active_object
    aug.name = "auge_l" if sd > 0 else "auge_r"
    aug.rotation_mode = "QUATERNION"
    aug.rotation_quaternion = Vector(tuple(g_w)).to_track_quat("Z", "Y")
    aug.data.materials.append(AUGE)
    for p in aug.data.polygons:
        p.use_smooth = True
    # Lid: Haube mit Mandelschlitz; der aeussere Teil liegt unter der Haut
    E, g, e1, e2 = augen_rahmen(sd)
    nt, nr = 96, 22
    pts = []
    for j in range(nt):
        tw = 2 * math.pi * j / nt
        st = math.sin(tw)
        u0 = AUGE_UH * math.cos(tw)
        v0 = (AUGE_VU if st > 0 else AUGE_VD) * math.copysign(abs(st) ** 1.2, st)
        ck, sk = math.cos(AUGE_KIPP), math.sin(AUGE_KIPP)
        u1 = u0 * ck - v0 * sk
        v1 = u0 * sk + v0 * ck
        ring = []
        for k in range(nr + 1):
            q = k / nr
            uu, vv = u1 * (1.0 + 1.1 * q), v1 * (1.0 + 1.1 * q)
            rho = math.hypot(uu, vv)
            d = g * math.cos(rho) + (e1 * uu + e2 * vv) / max(rho, 1e-6) * math.sin(rho)
            # kleiner Lidrand am Schlitz, oben etwas staerker: das Oberlid schneidet die Kugel ab
            rim = 0.0017 * math.sin(math.pi * min(q / 0.34, 1.0)) ** 0.8
            ober = 0.0017 * max(st, 0.0) * math.sin(math.pi * min(q / 0.5, 1.0))
            rr = AUGE_R_ + 0.0005 + rim + ober + 0.0006 * q
            ring.append(E + d * rr)
        pts.append(ring)
    pts = l2w(np.array(pts)).reshape(-1, 3)
    faces = []
    for j in range(nt):
        for k in range(nr):
            a = j * (nr + 1) + k
            b = ((j + 1) % nt) * (nr + 1) + k
            faces.append((a, b, b + 1, a + 1))
    lid = teil("lid", pts, faces, LID)
    bm = bmesh.new()
    bm.from_mesh(lid.data)
    bm.normal_update()
    cen = Vector(tuple(E_w))
    if sum((f.calc_center_median() - cen).dot(f.normal) for f in bm.faces) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(lid.data)
    bm.free()
    return aug, lid


# Zaehne in zwei Netzen (Oberkiefer, Unterkiefer). Sie sitzen auf dem Zahnfleischwall der Mundhoehle
def baue_zaehne():
    vo, fo = [], []
    vu, fu = [], []
    RU = KOPF["wallU"]
    RL = KOPF["wallL"]
    aa_ = KOPF["a_"]
    ia = int(np.argmax(aa_))

    def add(vl, fl, v, f):
        o = sum(len(x) for x in vl)
        vl.append(v)
        fl.extend(tuple(i + o for i in q) for q in f)

    def zahn(vl, fl, p, lang, r, richtung, krumm=0.0, stumpf=False):
        p0 = p + np.array((0.0, 0.0, richtung * 0.012))
        p3 = p + np.array((krumm * 0.3, 0.0, -richtung * lang))
        p1 = p0 + np.array((krumm * 0.05, 0.0, -richtung * lang * 0.5))
        p2 = p3 + np.array((krumm * 0.35, 0.0, richtung * lang * 0.4))
        pts = bez(p0, p1, p2, p3, 10)
        t = np.linspace(0.0, 1.0, 10)
        if stumpf:
            ra = r * np.maximum(1.0 - t ** 7, 0.02) ** 0.5
        else:
            ra = r * (1 - t) ** 0.62 + 0.0004
        v, f = rohr(l2w(pts), ra, ra * 1.12, (0.0, 1.0, 0.0), 10)
        add(vl, fl, v, f)

    def am(R_, aa, seite):
        i = int(np.argmax(aa_ >= aa))
        return R_[seite][i].copy()

    for sd_ in (0, 1):
        # Oberkiefer: zwei grosse stumpfe Backenzaehne, ein kleiner Vorbackenzahn, dann der Eckzahn
        for aa, ln, r in ((0.292, 0.0035, 0.0088), (0.325, 0.003, 0.008)):
            zahn(vo, fo, am(RU, aa, sd_), ln, r, 1.0, stumpf=True)
        zahn(vo, fo, am(RU, 0.385, sd_), 0.0075, 0.0052, 1.0)
        zahn(vo, fo, am(RU, 0.430, sd_), 0.036, 0.0108, 1.0, krumm=-0.03)
        # Unterkiefer
        for aa, ln, r in ((0.288, 0.003, 0.0082), (0.320, 0.0035, 0.0082)):
            zahn(vu, fu, am(RL, aa, sd_), ln, r, -1.0, stumpf=True)
        zahn(vu, fu, am(RL, 0.378, sd_), 0.0065, 0.0048, -1.0)
        zahn(vu, fu, am(RL, 0.447, sd_), 0.030, 0.0098, -1.0, krumm=-0.02)
        # Schneidezaehne: entlang des Walls im vorderen Bogen, gewaehlt ueber die Breite
        for yy, ln, r in ((0.010, 0.0135, 0.0052), (0.023, 0.0135, 0.0052), (0.036, 0.015, 0.0058)):
            for Rr, vl, fl, ri, f_ in ((RU, vo, fo, 1.0, 1.0), (RL, vu, fu, -1.0, 0.86)):
                w_ = np.abs(Rr[sd_][ia:, 1])
                j = ia + int(np.argmin(np.abs(w_ - yy * f_)))
                q_ = Rr[sd_][j].copy()
                q_[0] -= (0.017 if yy < 0.015 else 0.011 if yy < 0.03 else 0.006) if ri > 0 else 0.004
                zahn(vl, fl, q_, ln * (0.72 if ri > 0 else 0.7), r * (0.95 if ri > 0 else 0.84), ri, stumpf=True)
    oo = teil("zaehne_oben", np.concatenate(vo), fo, TOOTH)
    uu = teil("zaehne_unten", np.concatenate(vu), fu, TOOTH)
    return oo, uu


def baue_zunge():
    nu, nv = 40, 28
    v = []
    cen = np.array((0.368, 0.0, ring_wert("Cw_", 0.368) - 0.019))
    for i in range(nv + 1):
        t = i / nv * math.pi
        for j in range(nu):
            p = j / nu * 2 * math.pi
            a = 0.098 * math.cos(t)
            y = 0.043 * math.sin(t) * math.cos(p)
            c = 0.015 * math.sin(t) * math.sin(p)
            # Rille in der Mitte, vorn etwas breiter
            if c > 0:
                c -= 0.0028 * math.exp(-((y / 0.009) ** 2))
            y *= 1.0 + 0.12 * math.cos(t)
            v.append(cen + np.array((a, y, c)))
    faces = []
    for i in range(nv):
        for j in range(nu):
            a = i * nu + j
            b = i * nu + (j + 1) % nu
            faces.append((a, b, b + nu, a + nu))
    o = teil("zunge", l2w(np.array(v)), faces, ZUNGE)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data)
    bm.free()
    return o


def baue_krallen():
    out = []
    for bn in ("prankeR", "prankeL", "fussR", "fussL"):
        vv, ff, hh = [], [], []
        nn = 0
        for z in ZEHEN:
            if z["bone"] != bn:
                continue
            L0, R0 = z["krallen"]
            ax = z["ax"]
            upv = np.array((0.0, 0.0, 1.0))
            lat = unit(np.cross(upv, ax))
            root = z["c"] + ax * z["ln"] * 0.55 + upv * z["rv"] * 0.42
            tip = root + ax * L0 * 0.84
            tip[2] = 0.007
            # Bogen: erst fast waagerecht aus dem Zeh, dann nach unten, Spitze zielt zum Boden
            p1 = root + ax * L0 * 0.36 + upv * 0.012
            p2 = root + ax * L0 * 0.76 + upv * 0.005
            pts = bez(root, p1, p2, tip, 20)
            t = np.linspace(0.0, 1.0, 20)
            rv = R0 * (1 - t) ** 0.78 + 0.00035
            ra = rv * lerp(0.60, 0.82, t)
            v, f = rohr(pts, ra, rv, lat, 14)
            vv.append(v)
            ff.extend(tuple(i + nn for i in q) for q in f)
            h = np.concatenate((np.repeat(t, 14), [0.0, 1.0]))
            hh.append(h)
            nn += len(v)
        o = teil("krallen_" + bn, np.concatenate(vv), ff, HORN)
        at = o.data.attributes.new("horn", "FLOAT", "POINT")
        at.data.foreach_set("value", np.concatenate(hh))
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(o.data)
        bm.free()
        out.append((o, bn))
    return out


extras = []
extras.append((baue_nase(), "kopf"))
for sd in (-1, 1):
    aug, lid = baue_auge(sd)
    extras.append((aug, "kopf"))
    extras.append((lid, "kopf"))
_zo, _zu = baue_zaehne()
extras.append((_zo, "kopf"))
extras.append((_zu, "kiefer"))
extras.append((baue_zunge(), "kiefer"))
extras.extend(baue_krallen())
for o, bn in extras:
    on_bone(o, bn)

# ------------------------------------------------------------------ Boden und Licht wie ein Tag im Spiel
bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, 0))
gr = bpy.context.active_object
gm = bpy.data.materials.new("boden")
gm.use_nodes = True
N, L = gm.node_tree.nodes, gm.node_tree.links
bb = N["Principled BSDF"]
tc = N.new("ShaderNodeTexCoord")
nz = N.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 1.1
nz.inputs["Detail"].default_value = 12
nz.inputs["Roughness"].default_value = 0.68
L.new(tc.outputs["Object"], nz.inputs["Vector"])
nz2 = N.new("ShaderNodeTexNoise")
nz2.inputs["Scale"].default_value = 22
nz2.inputs["Detail"].default_value = 8
L.new(tc.outputs["Object"], nz2.inputs["Vector"])
gc = mix_rgba(N, L, maprange(N, L, nz.outputs["Fac"], 0.34, 0.66, 0, 1), (0.06, 0.08, 0.024), (0.15, 0.14, 0.05))
gc = mix_rgba(N, L, maprange(N, L, nz2.outputs["Fac"], 0.4, 0.66, 0, 0.7), gc, (0.05, 0.075, 0.022))
L.new(gc, bb.inputs["Base Color"])
bb.inputs["Roughness"].default_value = 0.95
bp2 = N.new("ShaderNodeBump")
bp2.inputs["Strength"].default_value = 0.6
L.new(nz2.outputs["Fac"], bp2.inputs["Height"])
L.new(bp2.outputs["Normal"], bb.inputs["Normal"])
gr.data.materials.append(gm)

world = bpy.data.worlds.new("himmel")
world.use_nodes = True
nt = world.node_tree
sky = nt.nodes.new("ShaderNodeTexGradient")
tcw = nt.nodes.new("ShaderNodeTexCoord")
mp = nt.nodes.new("ShaderNodeMapping")
mp.inputs["Rotation"].default_value = (0, -math.pi / 2, 0)
nt.links.new(tcw.outputs["Generated"], mp.inputs["Vector"])
nt.links.new(mp.outputs["Vector"], sky.inputs["Vector"])
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.5
ramp.color_ramp.elements[0].color = (0.78, 0.66, 0.5, 1)
ramp.color_ramp.elements[1].position = 0.86
ramp.color_ramp.elements[1].color = (0.2, 0.33, 0.56, 1)
nt.links.new(sky.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], nt.nodes["Background"].inputs[0])
nt.nodes["Background"].inputs[1].default_value = 1.5
scene.world = world
sun = bpy.data.lights.new("sonne", "SUN")
sun.energy = 3.0
sun.color = (1.0, 0.9, 0.78)
sun.angle = math.radians(2.2)
so = bpy.data.objects.new("sonne", sun)
col.objects.link(so)
so.rotation_euler = (math.radians(50), 0, math.radians(38))

# Gras auf dem Fahrweg des Baeren
bpy.ops.mesh.primitive_plane_add(size=26, location=(1.6, 0, 0.002))
wiese = bpy.context.active_object
wiese.name = "wiese"
wm = bpy.data.materials.new("wiesenboden")
wm.use_nodes = True
wm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.05, 0.022, 1)
wm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
gh = bpy.data.materials.new("halm")
gh.use_nodes = True
Ng, Lg = gh.node_tree.nodes, gh.node_tree.links
bg = Ng["Principled BSDF"]
hig = Ng.new("ShaderNodeHairInfo")
Lg.new(mix_rgba(Ng, Lg, maprange(Ng, Lg, hig.outputs["Random"], 0.2, 0.9, 0, 1), (0.085, 0.13, 0.03), (0.27, 0.27, 0.075)), bg.inputs["Base Color"])
bg.inputs["Roughness"].default_value = 0.55
wiese.data.materials.append(wm)
wiese.data.materials.append(gh)
wiese.modifiers.new("gras", "PARTICLE_SYSTEM")
pg = wiese.particle_systems[-1]
sg = pg.settings
sg.type = "HAIR"
sg.use_advanced_hair = True
sg.count = int(120000 * FUR_GRAS)
sg.hair_step = 4
sg.normal_factor = 0.017
sg.factor_random = 0.007
sg.object_align_factor = (0.006, 0.004, 0)
sg.child_type = "INTERPOLATED"
sg.rendered_child_count = 6
sg.child_length = 0.8
sg.child_length_threshold = 0.25
sg.roughness_1 = 0.03
sg.roughness_endpoint = 0.05
sg.material_slot = "halm"
sg.root_radius = 1.0
sg.tip_radius = 0.02
sg.radius_scale = 0.0028
sg.use_modifier_stack = False

# Dichtes kurzes Gras nur fuer die Nahaufnahme der Pfote
bpy.ops.mesh.primitive_plane_add(size=3.0, location=(0.9, -0.5, 0.0035))
nahgras = bpy.context.active_object
nahgras.name = "nahgras"
nahgras.data.materials.append(wm)
nahgras.data.materials.append(gh)
nahgras.modifiers.new("nah", "PARTICLE_SYSTEM")
_sn = nahgras.particle_systems[-1].settings
_sn.type = "HAIR"
_sn.use_advanced_hair = True
_sn.count = 26000
_sn.hair_step = 3
_sn.normal_factor = 0.0032
_sn.factor_random = 0.0014
_sn.object_align_factor = (0.002, 0.0015, 0)
_sn.child_type = "INTERPOLATED"
_sn.rendered_child_count = 5
_sn.child_length = 0.8
_sn.child_length_threshold = 0.3
_sn.roughness_1 = 0.006
_sn.roughness_endpoint = 0.012
_sn.material_slot = "halm"
_sn.root_radius = 1.0
_sn.tip_radius = 0.03
_sn.radius_scale = 0.0012
nahgras.hide_render = True

# Ferne Huegel, nur als weiche Silhouette
hilm = plain("huegel", (0.075, 0.095, 0.05), 1.0)
bpy.ops.mesh.primitive_plane_add(size=90, location=(0, 12.4, 20), rotation=(math.pi / 2, 0, 0))
wald = bpy.context.active_object
wald.name = "wald"
wbm = bpy.data.materials.new("wald")
wbm.use_nodes = True
Nw, Lw = wbm.node_tree.nodes, wbm.node_tree.links
Nw.remove(Nw["Principled BSDF"])
tw = Nw.new("ShaderNodeTexCoord")
n1 = Nw.new("ShaderNodeTexNoise")
n1.inputs["Scale"].default_value = 0.8
n1.inputs["Detail"].default_value = 5
n1.inputs["Roughness"].default_value = 0.62
Lw.new(tw.outputs["Object"], n1.inputs["Vector"])
fw = mix_rgba(Nw, Lw, maprange(Nw, Lw, n1.outputs["Fac"], 0.36, 0.64, 0, 1), (0.022, 0.05, 0.014), (0.2, 0.2, 0.03))
ew = Nw.new("ShaderNodeEmission")
Lw.new(fw, ew.inputs["Color"])
ew.inputs["Strength"].default_value = 0.75
Lw.new(ew.outputs[0], Nw["Material Output"].inputs["Surface"])
wald.data.materials.append(wbm)

scene.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
for d in prefs.devices:
    d.use = d.type == "OPTIX"
print("BAER_GERAETE", [d.name for d in prefs.devices if d.use])
scene.cycles.device = "GPU"
scene.cycles.use_denoising = True
scene.render.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"

# ------------------------------------------------------------------ Bewegung
pb = ao.pose.bones
for p in pb:
    p.rotation_mode = "QUATERNION"

# Fuss- und Pfotenziele, an denen die Beine haengen
TARGETS = {}
for s, n in ((-1, "R"), (1, "L")):
    for leg, chain_end, pawb in (("vorn", "unterarm" + n, "pranke" + n), ("hinten", "wade" + n, "fuss" + n)):
        e = bpy.data.objects.new("ziel_" + leg + n, None)
        col.objects.link(e)
        rest_tail = arm.bones[chain_end].tail_local
        e.location = rest_tail
        rest_rot = (ao.matrix_world @ arm.bones[pawb].matrix_local).to_quaternion()
        e.rotation_mode = "QUATERNION"
        e.rotation_quaternion = rest_rot
        TARGETS[leg + n] = (e, rest_tail.copy(), rest_rot.copy())
        ik = pb[chain_end].constraints.new("IK")
        ik.target = e
        ik.chain_count = 2
        ik.use_tail = True
        crot = pb[pawb].constraints.new("COPY_ROTATION")
        crot.target = e

WALK_END = 76          # bis hier zwei Gehzyklen
T = 1.25 * FPS         # Bilder je Zyklus
DUTY = 0.62
SPEED = 0.95 / FPS     # Meter je Bild
L_STEP = SPEED * T
PHASE = {"hintenL": 0.0, "vornL": 0.25, "hintenR": 0.5, "vornR": 0.75}

KF = {
    "stand": WALK_END + 8,
    "auf": WALK_END + 26,
    "aus": WALK_END + 32,
    "hieb": WALK_END + 39,
    "nach": WALK_END + 48,
    "ende": WALK_END + 70,
}
END_FRAME = KF["ende"] + 6


def smooth(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def foot_rel(phi):
    """Fuss relativ zum Koerper: Stuetzphase schiebt nach hinten, Schwung holt nach vorn."""
    if phi < DUTY:
        u = phi / DUTY
        return L_STEP * DUTY * (0.5 - u), 0.0, 0.0
    u = (phi - DUTY) / (1 - DUTY)
    x = L_STEP * DUTY * (u - 0.5)
    z = 0.13 * math.sin(math.pi * u)
    pitch = 28 * math.sin(math.pi * u * 1.1)
    return x, z, pitch


def set_rot(p, axis, deg):
    """Drehung um eine Weltachse, umgerechnet in das Ruhe-Achsenkreuz des Knochens."""
    r = p.bone.matrix_local.to_quaternion()
    q = Quaternion(axis, math.radians(deg))
    p.rotation_quaternion = r.inverted() @ q @ r


def combine(p, parts):
    r = p.bone.matrix_local.to_quaternion()
    tot = Quaternion()
    for axis, deg in parts:
        tot = Quaternion(axis, math.radians(deg)) @ tot
    p.rotation_quaternion = r.inverted() @ tot @ r


X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def pose_at(f):
    t = f
    # Fortbewegung, die ab WALK_END ausklingt
    if f <= WALK_END:
        travel = SPEED * f
    else:
        travel = SPEED * WALK_END + SPEED * 0.5 * min(f - WALK_END, 8) * (1 - min(f - WALK_END, 8) / 16.0)
    stopped = smooth(WALK_END, KF["stand"], f)

    # Abbremsen: Beine laufen in eine feste Stellung
    wt = 1.0 - stopped
    feet = {}
    for key, ph in PHASE.items():
        phi = ((f / T) + ph) % 1.0
        fx, fz, fp = foot_rel(phi)
        feet[key] = (fx * wt, fz * wt, fp * wt)

    # Wie weit steht er auf? Hiebablauf
    rise = smooth(KF["stand"], KF["auf"], f) * (1 - smooth(KF["nach"], KF["ende"], f))
    pitch = -27 * rise
    lift = 0.17 * rise
    swing = smooth(KF["aus"], KF["hieb"], f) * (1 - smooth(KF["nach"], KF["ende"], f))
    follow = smooth(KF["aus"], KF["hieb"], f) - smooth(KF["nach"] - 4, KF["ende"] - 6, f)

    gait = math.sin(2 * math.pi * f / T)
    gait2 = math.sin(4 * math.pi * f / T)
    bob = 0.018 * gait2 * wt
    ao.location = (travel, 0, 0)
    pb["wurzel"].location = (0, 0, 0)

    # Rumpf: Wiegen im Gehen, Aufrichten zum Hieb, Vorwerfen beim Schlag
    hieb_pitch = 22 * swing
    combine(pb["wurzel"], [(Y, pitch + hieb_pitch * 0.55), (X, 3.2 * gait * wt), (Z, 3.0 * gait * wt)])
    pb["wurzel"].location = pb["wurzel"].bone.matrix_local.to_quaternion().inverted() @ Vector((0.05 * rise - 0.08 * swing, 0, bob + lift - 0.05 * swing))
    combine(pb["ruecken"], [(Y, pitch * 0.35 + hieb_pitch * 0.35), (Z, -2.5 * gait * wt)])
    combine(pb["brust"], [(Y, pitch * 0.15 + hieb_pitch * 0.35), (Z, -3.5 * gait * wt), (X, -7 * swing)])
    # Kopf bleibt in der Waagerechten, im Hieb nach vorn
    combine(pb["hals"], [(Y, -pitch * 0.7 - hieb_pitch * 0.5 + 3.0 * gait2 * wt), (Z, 4.5 * gait * wt)])
    combine(pb["kopf"], [(Y, -pitch * 0.45 - hieb_pitch * 0.2 - 2 * gait2 * wt - 8 * follow), (Z, -2.5 * gait * wt)])
    # Maul oeffnet zum Bruellen
    roar = smooth(KF["stand"] + 4, KF["auf"], f) * (1 - smooth(KF["nach"], KF["ende"] - 6, f))
    combine(pb["kiefer"], [(Y, 34 * roar)])
    combine(pb["schwanz"], [(Z, 8 * gait * wt), (Y, -6 * gait2 * wt)])

    # Beine
    for key, (fx, fz, fp) in feet.items():
        e, rest, rrot = TARGETS[key]
        e.location = Vector((rest.x + fx + travel, rest.y, rest.z + fz))
        e.rotation_quaternion = Quaternion(Y, math.radians(fp)) @ rrot

    # Hieb: rechte Pranke geht hoch, schlaegt schraeg nach unten, linke stuetzt in der Luft
    e, rest, rrot = TARGETS["vornR"]
    high = Vector((rest.x + 0.62, rest.y - 0.10, rest.z + 1.14))
    drive = Vector((rest.x + 1.08, rest.y + 0.30, rest.z + 0.16))
    hold = Vector((rest.x + 0.03, rest.y, rest.z)) + Vector((travel, 0, 0))
    up = smooth(KF["stand"], KF["aus"], f)
    down = smooth(KF["aus"], KF["hieb"], f)
    back = smooth(KF["nach"], KF["ende"], f)
    hi = high + Vector((travel, 0, 0))
    dr = drive + Vector((travel, 0, 0))
    pos = hold.lerp(hi, up).lerp(dr, down).lerp(hold, back)
    e.location = pos
    e.rotation_quaternion = Quaternion(Y, math.radians((-55 * up + 118 * down) * (1 - back))) @ rrot

    e, rest, rrot = TARGETS["vornL"]
    hold = Vector((rest.x + 0.02 + travel, rest.y, rest.z))
    tuck = Vector((rest.x + 0.34 + travel, rest.y + 0.03, rest.z + 0.30))
    land = Vector((rest.x + 0.40 + travel, rest.y, rest.z))
    p1 = hold.lerp(tuck, rise * (1 - 0.8 * down))
    p1 = p1.lerp(land, down * (1 - back))
    p1 = p1.lerp(hold, back)
    e.location = p1
    e.rotation_quaternion = Quaternion(Y, math.radians(-25 * rise * (1 - down))) @ rrot


# Jedes Bild vorab in Schluessel schreiben, sonst rechnet die Szene in der Tiefe nicht nach
def key_all(f):
    pose_at(f)
    ao.keyframe_insert("location", frame=f)
    for p in pb:
        p.keyframe_insert("rotation_quaternion", frame=f)
    pb["wurzel"].keyframe_insert("location", frame=f)
    for e, _, _ in TARGETS.values():
        e.keyframe_insert("location", frame=f)
        e.keyframe_insert("rotation_quaternion", frame=f)


for f in range(1, END_FRAME + 1):
    key_all(f)
scene.frame_start = 1
scene.frame_end = END_FRAME


def camera(name, offs, tgt_offs, lens=None, ortho=None, fstop=1.8):
    cam = bpy.data.cameras.new(name)
    if ortho:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho
    else:
        cam.lens = lens
    co = bpy.data.objects.new(name, cam)
    col.objects.link(co)
    co.location = offs
    d = Vector(tgt_offs) - Vector(offs)
    co.rotation_mode = "QUATERNION"
    co.rotation_quaternion = d.to_track_quat("-Z", "Y")
    if not ortho:
        cam.dof.use_dof = True
        cam.dof.focus_distance = d.length * 0.94
        cam.dof.aperture_fstop = fstop
    # Kamera faehrt mit dem Baeren
    c = co.constraints.new("COPY_LOCATION")
    c.target = ao
    c.use_x = True
    c.use_y = False
    c.use_z = False
    c.use_offset = True
    return co


def kopf_mitte(frame, ort=(0.27, 0.0, -0.02)):
    """Weltlage eines Kopf-Punktes im Pose-Zustand eines Bildes."""
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    pbk = ao.pose.bones["kopf"]
    bm_ = ao.matrix_world @ pbk.matrix @ pbk.bone.matrix_local.inverted()
    return bm_ @ Vector(tuple(l2w(ort)))


def camera_fest(name, pos, ziel, lens, fstop=11.0):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    co = bpy.data.objects.new(name, cam)
    col.objects.link(co)
    co.location = pos
    d = Vector(ziel) - Vector(pos)
    co.rotation_mode = "QUATERNION"
    co.rotation_quaternion = d.to_track_quat("-Z", "Y")
    cam.dof.use_dof = True
    cam.dof.focus_distance = d.length * 0.97
    cam.dof.aperture_fstop = fstop
    return co


CAM_SIDE = camera("seite", (3.5, -7.2, 0.78), (0.24, 0, 0.92), lens=74)
CAM_GAME = camera("spiel", (6, -6, 5.6), (0.4, 0, 0.55), ortho=4.6)

print("BAER_OK Dreiecke Netz", body_tris, "vorher", start_tris, "gesamt",
      sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in col.objects if o.type == "MESH" and o is not gr))


def render_still(name, frame, cam, res, samples):
    if SHOTS and name not in SHOTS:
        return
    scene.camera = cam
    scene.frame_set(frame)
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.cycles.samples = samples
    scene.render.filepath = OUT + name + ".png"
    bpy.ops.render.render(write_still=True)
    print("BAER_BILD", name)


def bilder(res, samples, gruss, ganz=True):
    # Standbild fuer die Nahansichten: der Lauf am Anfang, Kopf fast in Ruhelage
    f0 = 1
    k = kopf_mitte(f0)
    CAM_P = camera_fest("profil", (k.x, k.y - 2.05, k.z + 0.02), (k.x, k.y, k.z), 85)
    CAM_D = camera_fest("drei", (k.x + 1.28, k.y - 1.02, k.z + 0.16), (k.x + 0.02, k.y, k.z), 85)
    CAM_F = camera_fest("front", (k.x + 1.72, k.y, k.z + 0.10), (k.x + 0.05, k.y, k.z), 85)
    render_still("kopf_profil", f0, CAM_P, res, samples)
    render_still("kopf_34", f0, CAM_D, res, samples)
    render_still("kopf_front", f0, CAM_F, res, samples)
    # Pfote: Gras niedrig, Kamera auf Bodenhoehe
    pw = Vector((0.0, 0.0, 0.0))
    scene.frame_set(f0)
    bpy.context.view_layer.update()
    pbp = ao.pose.bones["prankeR"]
    pw = ao.matrix_world @ pbp.tail
    CAM_Z = camera_fest("pfote", (pw.x + 0.56, pw.y - 0.56, 0.085), (pw.x + 0.03, pw.y, 0.05), 85, fstop=8.0)
    if not SHOTS or "pfote" in SHOTS:
        alt = sg.normal_factor
        sg.normal_factor = 0.0045
        sg.factor_random = 0.002
        sg.radius_scale = 0.0013
        _r1, _re = sg.roughness_1, sg.roughness_endpoint
        sg.roughness_1 = 0.004
        sg.roughness_endpoint = 0.006
        nahgras.hide_render = False
        scene.view_settings.exposure = 0.7
        render_still("pfote", f0, CAM_Z, res, samples)
        scene.view_settings.exposure = 0.0
        nahgras.hide_render = True
        sg.roughness_1, sg.roughness_endpoint = _r1, _re
        sg.normal_factor = alt
        sg.factor_random = 0.007
        sg.radius_scale = 0.0028
    if ganz:
        render_still("ganz", 22, CAM_SIDE, res, samples)
        render_still("hieb", KF["hieb"], CAM_SIDE, res, samples)
    # Nur zur Kontrolle: Auge und Nase ganz nah
    if SHOTS and ("auge" in SHOTS or "nase" in SHOTS):
        scene.frame_set(f0)
        au = kopf_mitte(f0, (AUGE_L[0], -AUGE_L[1], AUGE_L[2]))
        CAM_A = camera_fest("auge_c", (au.x + 0.34, au.y - 0.30, au.z + 0.06), (au.x, au.y, au.z), 85, fstop=16)
        render_still("auge", f0, CAM_A, res, samples)
        na = kopf_mitte(f0, (0.50, 0.0, -0.01))
        CAM_N = camera_fest("nase_c", (na.x + 0.40, na.y - 0.20, na.z + 0.04), (na.x, na.y, na.z), 85, fstop=16)
        render_still("nase", f0, CAM_N, res, samples)
    # Offenes Maul von nah
    h = KF["hieb"]
    m = kopf_mitte(h, (0.36, 0.0, -0.05))
    CAM_M = camera_fest("maul", (m.x + 0.82, m.y - 0.88, m.z - 0.10), (m.x, m.y, m.z), 85)
    render_still("maul", h, CAM_M, res, samples)


if MODE == "kopf":
    scene.cycles.max_bounces = 6
    bilder((700, 525), 36, "kopf", ganz=bool(SHOTS and ("ganz" in SHOTS or "hieb" in SHOTS)))
elif MODE == "ende":
    scene.cycles.max_bounces = 8
    bilder((1200, 900), 150, "ende", ganz=True)
elif MODE == "still":
    scene.cycles.max_bounces = 8
    render_still("v3_gehen", 22, CAM_SIDE, (1500, 1000), 200)
    render_still("v3_hoch", KF["aus"], CAM_SIDE, (1500, 1000), 200)
    render_still("v3_hieb", KF["hieb"], CAM_SIDE, (1500, 1000), 200)
    CAM_HEAD = camera("kopf", (3.9, -1.5, 1.2), (1.14, 0, 1.03), lens=85)
    render_still("v3_kopf", 22, CAM_HEAD, (1200, 900), 200)
else:
    bpy.ops.wm.save_as_mainfile(filepath=OUT + "baer.blend")
    scene.camera = CAM_SIDE
    scene.render.resolution_x, scene.render.resolution_y = (720, 500)
    scene.cycles.samples = 48
    scene.render.filepath = OUT + "seite/f_"
    if len(ARGS) > 1 and ARGS[1].isdigit():
        scene.frame_end = scene.frame_start + int(ARGS[1])
    bpy.ops.render.render(animation=True)
    # Die Spielansicht zeigt ehrlich die reduzierte Fassung: Koerper rund 1400 Dreiecke (Vanilla-Tiere: 400-930 Punkte)
    dm = body.modifiers.new("wenig", "DECIMATE")
    dm.ratio = 1400.0 / max(1, body_tris)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.modifier_move_to_index(modifier="wenig", index=0)
    scene.frame_set(1)
    dg = bpy.context.evaluated_depsgraph_get()
    me2 = body.evaluated_get(dg).to_mesh()
    print("BAER_LOW Dreiecke", sum(len(q.vertices) - 2 for q in me2.polygons), "Punkte", len(me2.vertices))
    render_still("still_spiel_wenig", 22, CAM_GAME, (620, 465), 64)
    scene.camera = CAM_GAME
    scene.render.resolution_x, scene.render.resolution_y = (414, 311)
    scene.cycles.samples = 32
    scene.render.filepath = OUT + "spiel/f_"
    bpy.ops.render.render(animation=True)
    print("BAER_ANIM_OK")
