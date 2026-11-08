# Probe: Baer aus Metabaellen, reduziert auf spieltaugliche Dreieckszahl, mit Skelett,
# Gehzyklus und Krallenhieb. Aufruf: blender --background --factory-startup --python baer.py -- still|anim
import math
import random
import sys

import bmesh
import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

OUT = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/blender_test/baer/"
MODE = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "still"
random.seed(3)

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
# Dicker Hals, der nach vorn abfaellt, Kopf tief getragen
chain((0.52, 0, 0.86), (0.82, 0, 0.73), 0.40, 0.31, 3)
ball(1.00, 0, 0.75, 0.32)
ball(1.06, 0, 0.84, 0.18)    # Stirnabsatz
chain((1.19, 0, 0.70), (1.375, 0, 0.655), 0.19, 0.155, 5)
for s in (-1, 1):
    # Breiter Schaedel, Backen, runde kleine Ohren weit aussen
    ball(0.98, s * 0.12, 0.77, 0.24)
    ball(0.93, s * 0.19, 0.67, 0.19)
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
body_tris = sum(len(p.vertices) - 2 for p in body.data.polygons)

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
# Heller Schnauzenbereich
muzzle = maprange(N, L, sep.outputs[0], 0.885, 0.925, 0.0, 0.8)
col4 = mix_rgba(N, L, muzzle, col3, (0.09, 0.055, 0.03))
L.new(col4, b.inputs["Base Color"])
L.new(maprange(N, L, hair.outputs["Fac"], 0.3, 0.7, 0.86, 0.66), b.inputs["Roughness"])
b.inputs["Sheen Weight"].default_value = 0.0
bp = N.new("ShaderNodeBump")
bp.inputs["Strength"].default_value = 1.0
bp.inputs["Distance"].default_value = 0.05
L.new(hair.outputs["Fac"], bp.inputs["Height"])
L.new(bp.outputs["Normal"], b.inputs["Normal"])
body.data.materials.append(fur)


def plain(name, rgb, rough=0.5, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes["Principled BSDF"]
    n.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1)
    n.inputs["Roughness"].default_value = rough
    return m


BLACK = plain("nase", (0.016, 0.013, 0.012), 0.36)
_nb = BLACK.node_tree.nodes
_nz = _nb.new("ShaderNodeTexNoise")
_nz.inputs["Scale"].default_value = 340
_bp = _nb.new("ShaderNodeBump")
_bp.inputs["Strength"].default_value = 0.9
_bp.inputs["Distance"].default_value = 0.004
BLACK.node_tree.links.new(_nz.outputs["Fac"], _bp.inputs["Height"])
BLACK.node_tree.links.new(_bp.outputs["Normal"], _nb["Principled BSDF"].inputs["Normal"])
EYE = plain("auge", (0.006, 0.003, 0.002), 0.06)
CLAW = plain("kralle", (0.018, 0.015, 0.012), 0.5)
FURSKIN = plain("kieferfell", (0.05, 0.028, 0.014), 0.7)
MOUTH = plain("maul", (0.11, 0.012, 0.012), 0.5)
SOOTY = plain("schwarz", (0.001, 0.001, 0.001), 0.8)
TOOTH = plain("zahn", (0.62, 0.56, 0.42), 0.4)

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
bone("kiefer", (1.00, 0, 0.665), (1.32, 0, 0.60), "kopf")
bone("schwanz", (-1.02, 0, 0.72), (-1.26, 0, 0.72), "wurzel")
for s, n in ((-1, "R"), (1, "L")):
    bone("oberarm" + n, (0.30, s * 0.30, 0.76), (0.33, s * 0.32, 0.38), "brust")
    bone("unterarm" + n, (0.33, s * 0.32, 0.38), (0.35, s * 0.31, 0.13), "oberarm" + n, True)
    bone("pranke" + n, (0.35, s * 0.31, 0.13), (0.56, s * 0.29, 0.06), "unterarm" + n, True)
    bone("schenkel" + n, (-0.70, s * 0.335, 0.72), (-0.55, s * 0.35, 0.38), "wurzel")
    bone("wade" + n, (-0.55, s * 0.35, 0.38), (-0.72, s * 0.33, 0.13), "schenkel" + n, True)
    bone("fuss" + n, (-0.72, s * 0.33, 0.13), (-0.42, s * 0.32, 0.06), "wade" + n, True)
bpy.ops.object.mode_set(mode="OBJECT")

# ------------------------------------------------------------------ Gewichte: nah am Knochen zaehlt
NAMES = [b.name for b in arm.bones if b.name != "kiefer"]
SEG = {b.name: (b.head_local.copy(), b.tail_local.copy()) for b in arm.bones}
for nm in NAMES:
    body.vertex_groups.new(name=nm)


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
for i, wmap in enumerate(WEIGHTS):
    top = sorted(wmap.items(), key=lambda kv: -kv[1])[:4]
    tot = sum(v for _, v in top)
    for k, v in top:
        body.vertex_groups[k].add([i], v / tot, "REPLACE")

mod = body.modifiers.new("skelett", "ARMATURE")
mod.object = ao
body.parent = ao


def sstep(a, c, x):
    t = max(0.0, min(1.0, (x - a) / (c - a)))
    return t * t * (3 - 2 * t)


def front_at(y0, z0, tol=0.035):
    xs = [v.co.x for v in body.data.vertices if abs(v.co.y - y0) < tol and abs(v.co.z - z0) < tol and v.co.x > 0.8]
    return max(xs)


def top_at(x0, y0, tol=0.04):
    zs = [v.co.z for v in body.data.vertices if abs(v.co.x - x0) < tol and abs(v.co.y - y0) < tol]
    return max(zs)


tipv = max((v for v in body.data.vertices if abs(v.co.y) < 0.03), key=lambda v: v.co.x)
NOSE = Vector((tipv.co.x - 0.012, 0, tipv.co.z + 0.022))
EYE_Z = NOSE.z + 0.135
EYE_Y = 0.098
EYE_X = front_at(EYE_Y, EYE_Z) - 0.006
EAR_X, EAR_Y = 0.955, 0.205
EAR_Z = top_at(EAR_X, EAR_Y)
print("BAER_LAGE Nase", tuple(round(c, 3) for c in NOSE), "Auge", round(EYE_X, 3), round(EYE_Z, 3), "Ohr", round(EAR_Z, 3))
EYES = [Vector((EYE_X, sy * EYE_Y, EYE_Z)) for sy in (-1, 1)]

G = {n: body.vertex_groups.new(name=n) for n in ("d_koerper", "d_bein", "d_kopf", "l_koerper", "l_bein", "l_kopf")}
for v in body.data.vertices:
    c = v.co
    head = sstep(0.84, 1.08, c.x)
    leg = (1.0 - sstep(lz(0.22), lz(0.56), c.z)) * (1.0 - head)
    # Die Bauchlinie zwischen den Beinen bleibt Koerperfell
    if -0.25 < c.x < 0.12:
        leg *= 0.15
    rest = max(0.0, 1.0 - head - leg)
    G["d_koerper"].add([v.index], rest, "REPLACE")
    G["d_bein"].add([v.index], leg, "REPLACE")
    free = 1.0
    near = 1.0
    for q, r0, r1 in ((NOSE, 0.044, 0.085), (EYES[0], 0.019, 0.06), (EYES[1], 0.019, 0.06)):
        d = (c - q).length
        free = min(free, sstep(r0, r0 + 0.012, d))
        near = min(near, 0.35 + 0.65 * sstep(r0, r1, d))
    G["d_kopf"].add([v.index], head * free, "REPLACE")
    # Laengen: Nackenmaehne und Bauchfransen lang, Ruecken mittel
    lk = 0.72
    lk += 0.28 * sstep(0.1, 0.45, c.x) * sstep(lz(0.62), lz(0.95), c.z) * (1 - sstep(0.75, 0.95, c.x))
    lk += 0.28 * (1 - sstep(lz(0.34), lz(0.48), c.z)) * (1 - sstep(0.12, 0.3, abs(c.x + 0.1)))
    G["l_koerper"].add([v.index], min(1.0, lk), "REPLACE")
    G["l_bein"].add([v.index], 0.26 + 0.74 * sstep(0.09, lz(0.34), c.z), "REPLACE")
    # Kopf: Wange laenger, Nasenruecken kurz, Nasenspitze ganz kurz
    lh = 1.0 - 0.55 * sstep(1.04, 1.2, c.x) - 0.28 * sstep(1.2, 1.32, c.x)
    G["l_kopf"].add([v.index], max(0.26, lh) * near, "REPLACE")

hm = bpy.data.materials.new("haar")
hm.use_nodes = True
N, L = hm.node_tree.nodes, hm.node_tree.links
N.remove(N["Principled BSDF"])
hb = N.new("ShaderNodeBsdfHairPrincipled")
hb.parametrization = "MELANIN"
hb.inputs["Melanin Redness"].default_value = 0.40
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
L.new(maprange(N, L, nz.outputs["Fac"], 0.30, 0.70, 0.68, 0.87), add1.inputs[1])
add2 = N.new("ShaderNodeMath")
add2.operation = "ADD"
L.new(add1.outputs[0], add2.inputs[0])
L.new(maprange(N, L, sep.outputs[2], 0.14, 0.42, 0.26, 0.0), add2.inputs[1])       # Beine dunkler
add3 = N.new("ShaderNodeMath")
add3.operation = "SUBTRACT"
L.new(add2.outputs[0], add3.inputs[0])
L.new(maprange(N, L, sep.outputs[2], 0.56, 0.92, 0.0, 0.12), add3.inputs[1])       # Ruecken heller
add4 = N.new("ShaderNodeMath")
add4.operation = "SUBTRACT"
add4.use_clamp = True
L.new(add3.outputs[0], add4.inputs[0])
tip = N.new("ShaderNodeMath")
tip.operation = "ADD"
L.new(maprange(N, L, sep.outputs[0], 0.915, 0.955, 0.0, 0.2), tip.inputs[0])       # helle Schnauze
L.new(maprange(N, L, hi.outputs["Intercept"], 0.45, 1.0, 0.0, 0.2), tip.inputs[1])  # helle Spitzen
kopfhell = N.new("ShaderNodeMath")
kopfhell.operation = "ADD"
L.new(tip.outputs[0], kopfhell.inputs[0])
L.new(maprange(N, L, sep.outputs[0], 0.72, 0.82, 0.0, 0.12), kopfhell.inputs[1])
L.new(kopfhell.outputs[0], add4.inputs[1])
L.new(add4.outputs[0], hb.inputs["Melanin"])
hb.inputs["Random Color"].default_value = 0.1
L.new(hb.outputs[0], N["Material Output"].inputs["Surface"])
body.data.materials.append(hm)
def fell(name, count, length, normal, align, dens, lng, kids, clump, rough1, rough2, radius, seed):
    body.modifiers.new(name, "PARTICLE_SYSTEM")
    ps = body.particle_systems[-1]
    ps.seed = seed
    st = ps.settings
    st.name = name
    st.type = "HAIR"
    st.use_advanced_hair = True
    st.count = count
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


fell("unterwolle", 100000, 0.098, 0.052, (-0.038, 0.0, -0.024), "d_koerper", "l_koerper", 18, 0.66, 0.009, 0.007, 0.0028, 11)
fell("deckhaar", 14000, 0.15, 0.066, (-0.052, 0.0, -0.036), "d_koerper", "l_koerper", 9, 0.86, 0.013, 0.012, 0.0034, 12)
fell("beinfell", 60000, 0.082, 0.046, (-0.012, 0.0, -0.028), "d_bein", "l_bein", 14, 0.56, 0.008, 0.005, 0.0029, 13)
fell("kopffell", 22000, 0.056, 0.026, (-0.016, 0.0, -0.006), "d_kopf", "l_kopf", 12, 0.3, 0.004, 0.003, 0.0026, 14)

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


def sphere(name, loc, r, mat, scale=(1, 1, 1), seg=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), radius=r, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def cone(name, a, c, r, mat, verts=8):
    a, c = Vector(a), Vector(c)
    d = c - a
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=0.002, depth=d.length, location=(a + c) / 2)
    o = bpy.context.active_object
    o.name = name
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = d.to_track_quat("Z", "Y")
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = len(p.vertices) == 3
    return o


hd = bpy.data.materials.new("haar_dunkel")
hd.use_nodes = True
Nd, Ld = hd.node_tree.nodes, hd.node_tree.links
Nd.remove(Nd["Principled BSDF"])
hbd = Nd.new("ShaderNodeBsdfHairPrincipled")
hbd.parametrization = "MELANIN"
hbd.inputs["Melanin"].default_value = 0.76
hbd.inputs["Melanin Redness"].default_value = 0.34
hbd.inputs["Roughness"].default_value = 0.4
hbd.inputs["Random Color"].default_value = 0.12
Ld.new(hbd.outputs[0], Nd["Material Output"].inputs["Surface"])


def ohr(name, y):
    o = sphere(name, (EAR_X, y, EAR_Z + 0.022), 0.056, FURSKIN, (0.42, 1.0, 1.0), 20)
    o.rotation_euler = (0, math.radians(-14), 0)
    bpy.context.view_layer.objects.active = o
    o.modifiers.new("ohrfell", "PARTICLE_SYSTEM")
    st = o.particle_systems[-1].settings
    st.type = "HAIR"
    st.use_advanced_hair = True
    st.count = 2600
    st.hair_step = 4
    st.normal_factor = 0.012
    st.factor_random = 0.004
    st.child_type = "INTERPOLATED"
    st.rendered_child_count = 6
    st.roughness_1 = 0.003
    st.root_radius = 1.0
    st.tip_radius = 0.03
    st.radius_scale = 0.0024
    o.data.materials.append(hd)
    st.material_slot = "haar_dunkel"
    return o


extras = []
for o, bn in (
    (ohr("ohr_r", -EAR_Y), "kopf"),
    (ohr("ohr_l", EAR_Y), "kopf"),
    (sphere("nase", tuple(NOSE), 0.046, BLACK, (0.6, 1.2, 0.68)), "kopf"),
    (sphere("nasenloch_r", (NOSE.x + 0.024, -0.026, NOSE.z - 0.006), 0.0105, SOOTY, (0.5, 1.15, 0.7)), "kopf"),
    (sphere("nasenloch_l", (NOSE.x + 0.024, 0.026, NOSE.z - 0.006), 0.0105, SOOTY, (0.5, 1.15, 0.7)), "kopf"),
    (sphere("auge_r", tuple(EYES[0]), 0.0165, EYE), "kopf"),
    (sphere("auge_l", tuple(EYES[1]), 0.0165, EYE), "kopf"),
    (sphere("kieferhaut", (1.135, 0, lz(0.615)), 0.135, FURSKIN, (1.24, 0.70, 0.27)), "kiefer"),
    (sphere("zunge", (1.145, 0, lz(0.641)), 0.09, MOUTH, (1.34, 0.72, 0.13)), "kiefer"),
    (sphere("gaumen", (1.18, 0, lz(0.664)), 0.112, MOUTH, (1.32, 0.80, 0.22)), "kopf"),
):
    extras.append((o, bn))
# Zaehne im geschlossenen Maul verborgen
for k in range(6):
    t = k / 5.0
    x = 1.135 + t * 0.155
    wy = 0.105 * (1 - t * 0.45)
    for s in (-1, 1):
        extras.append((cone("zahn", (x, s * wy, lz(0.668)), (x + 0.008, s * wy, lz(0.63)), 0.0125, TOOTH, 6), "kopf"))
        extras.append((cone("zahn", (x - 0.02, s * wy * 0.92, lz(0.615)), (x - 0.012, s * wy * 0.92, lz(0.65)), 0.011, TOOTH, 6), "kiefer"))
    if k == 4:
        for s in (-1, 1):
            extras.append((cone("fangzahn", (x, s * wy * 1.03, lz(0.70)), (x + 0.010, s * wy * 1.03, lz(0.625)), 0.020, TOOTH, 8), "kopf"))
# Krallen
for s, n in ((-1, "R"), (1, "L")):
    for pre, x0 in (("pranke", 0.545), ("fuss", -0.41)):
        for k in range(5):
            y = s * (0.28 if pre == "pranke" else 0.32) + (k - 2) * 0.05
            lift = 0.012 * abs(k - 2)
            xx = x0 - 0.016 * abs(k - 2)
            extras.append((cone("kralle", (xx, y, 0.055 + lift), (xx + 0.118, y, 0.016 + lift * 0.5), 0.02, CLAW, 8), pre + n))
def lefze(pts):
    c = bpy.data.curves.new("lefze", "CURVE")
    c.dimensions = "3D"
    c.bevel_depth = 0.0042
    c.bevel_resolution = 2
    c.use_fill_caps = True
    sp = c.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for bp, q in zip(sp.bezier_points, pts):
        bp.co = q
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    c.materials.append(SOOTY)
    o = bpy.data.objects.new("lefze", c)
    col.objects.link(o)
    return o


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
sg.count = 120000
sg.hair_step = 4
sg.normal_factor = 0.017
sg.factor_random = 0.007
sg.object_align_factor = (0.006, 0.004, 0)
print("BAER_GRAS Laenge", sg.hair_length)
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


def camera(name, offs, tgt_offs, lens=None, ortho=None):
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
        cam.dof.aperture_fstop = 1.8
    # Kamera faehrt mit dem Baeren
    c = co.constraints.new("COPY_LOCATION")
    c.target = ao
    c.use_x = True
    c.use_y = False
    c.use_z = False
    c.use_offset = True
    return co


CAM_SIDE = camera("seite", (3.5, -7.2, 0.78), (0.24, 0, 0.92), lens=74)
CAM_GAME = camera("spiel", (6, -6, 5.6), (0.4, 0, 0.55), ortho=4.6)

print("BAER_OK Dreiecke Koerper", body_tris, "vorher", start_tris, "gesamt",
      sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in col.objects if o.type == "MESH" and o is not gr))


def render_still(name, frame, cam, res, samples):
    scene.camera = cam
    scene.frame_set(frame)
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.cycles.samples = samples
    scene.render.filepath = OUT + name + ".png"
    bpy.ops.render.render(write_still=True)


if MODE == "still":
    scene.cycles.max_bounces = 8
    render_still("v3_gehen", 22, CAM_SIDE, (1500, 1000), 200)
    render_still("v3_hoch", KF["aus"], CAM_SIDE, (1500, 1000), 200)
    render_still("v3_hieb", KF["hieb"], CAM_SIDE, (1500, 1000), 200)
    CAM_HEAD = camera("kopf", (3.9, -1.5, 1.2), (1.14, 0, 1.03), lens=85)
    render_still("v3_kopf", 22, CAM_HEAD, (1200, 900), 200)
    pass
else:
    bpy.ops.wm.save_as_mainfile(filepath=OUT + "baer.blend")
    scene.camera = CAM_SIDE
    scene.render.resolution_x, scene.render.resolution_y = (720, 500)
    scene.cycles.samples = 48
    scene.render.filepath = OUT + "seite/f_"
    bpy.ops.render.render(animation=True)
    # Die Spielansicht zeigt ehrlich die reduzierte Fassung: Koerper rund 1400 Dreiecke (Vanilla-Tiere: 400-930 Punkte)
    dm = body.modifiers.new("wenig", "DECIMATE")
    dm.ratio = 1400.0 / max(1, body_tris)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.modifier_move_to_index(modifier="wenig", index=0)
    scene.frame_set(1)
    dg = bpy.context.evaluated_depsgraph_get()
    me = body.evaluated_get(dg).to_mesh()
    print("BAER_LOW Dreiecke", sum(len(q.vertices) - 2 for q in me.polygons), "Punkte", len(me.vertices))
    render_still("still_spiel_wenig", 22, CAM_GAME, (620, 465), 64)
    scene.camera = CAM_GAME
    scene.render.resolution_x, scene.render.resolution_y = (414, 311)
    scene.cycles.samples = 32
    scene.render.filepath = OUT + "spiel/f_"
    bpy.ops.render.render(animation=True)
    print("BAER_ANIM_OK")
