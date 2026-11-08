# Probe: Baer aus Metabaellen fuer den Koerper, Kopf und Zehen als Kontrollkaefig (Bauweise B), mit Skelett,
# Gehzyklus und Krallenhieb. Aufruf: blender --background --factory-startup --python baer_b.py -- clay|kopf|ende|still|anim
import math
import random
import sys

import bmesh
import bpy
from mathutils import Euler, Matrix, Quaternion, Vector, kdtree

OUT = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/blender_test/baer/run_b/"
MODE = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "still"
random.seed(3)
# Felldichte je Modus: clay ganz ohne Fell, kopf mit reduziertem Fell fuer schnelle Schleifen
FUR = {"clay": 0.0, "kopf": 0.22}.get(MODE, 1.0)
FUR_K = {"kopf": 0.55}.get(MODE, 1.0)   # eigener Faktor fuer Kopf- und Zehenfell (im Nahbild muss es stimmen)
TAG = sys.argv[sys.argv.index("--") + 2] if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 2 else ""


def smooth_(a, c, x):
    t = max(0.0, min(1.0, (x - a) / (c - a)))
    return t * t * (3 - 2 * t)


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
ball(0.90, 0, 0.73, 0.27)     # Halsstumpf: der Kopf selbst ist ein eigener Kaefig
for s in (-1, 1):
    # Vorderbein: lang und saeulig, Pranken leicht einwaerts
    chain((0.30, s * 0.29, 0.78), (0.33, s * 0.32, 0.40), 0.30, 0.235, 3)
    chain((0.33, s * 0.32, 0.40), (0.35, s * 0.31, 0.14), 0.25, 0.205, 6)
    chain((0.37, s * 0.31, 0.10), (0.50, s * 0.285, 0.078), 0.20, 0.165, 3)
    # Hinterbein: maechtige Keule, Sohlengaenger mit langem Fuss
    chain((-0.72, s * 0.33, 0.72), (-0.57, s * 0.36, 0.42), 0.35, 0.26, 3)
    chain((-0.58, s * 0.35, 0.40), (-0.71, s * 0.33, 0.16), 0.26, 0.20, 6)
    chain((-0.75, s * 0.33, 0.10), (-0.44, s * 0.32, 0.078), 0.195, 0.165, 4)
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
L.new(col3, b.inputs["Base Color"])
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


FURSKIN = plain("kieferfell", (0.05, 0.028, 0.014), 0.7)
MOUTH = plain("maul", (0.11, 0.012, 0.012), 0.5)
SOOTY = plain("schwarz", (0.001, 0.001, 0.001), 0.8)
TOOTH = plain("zahn", (0.50, 0.42, 0.29), 0.42)

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


G = {n: body.vertex_groups.new(name=n) for n in ("d_koerper", "d_deck", "d_bein", "l_koerper", "l_bein")}
for v in body.data.vertices:
    c = v.co
    # Am Halsstumpf steckt der Koerper im Kopf: dort kein Koerperfell, sonst stuende es durch den Schaedel
    head = sstep(0.83, 0.93, c.x)
    leg = (1.0 - sstep(lz(0.22), lz(0.56), c.z)) * (1.0 - head)
    # Die Bauchlinie zwischen den Beinen bleibt Koerperfell
    if -0.25 < c.x < 0.12:
        leg *= 0.15
    rest = max(0.0, 1.0 - head - leg)
    G["d_koerper"].add([v.index], rest, "REPLACE")
    G["d_deck"].add([v.index], rest * (1.0 - 0.9 * sstep(0.30, 0.62, c.x) * (1.0 - sstep(lz(0.78), lz(0.98), c.z))), "REPLACE")
    G["d_bein"].add([v.index], leg, "REPLACE")
    # Laengen: Nackenmaehne und Bauchfransen lang, Ruecken mittel
    lk = 0.72
    lk += 0.28 * sstep(0.1, 0.45, c.x) * sstep(lz(0.62), lz(0.95), c.z) * (1 - sstep(0.75, 0.95, c.x))
    lk += 0.28 * (1 - sstep(lz(0.34), lz(0.48), c.z)) * (1 - sstep(0.12, 0.3, abs(c.x + 0.1)))
    G["l_koerper"].add([v.index], min(1.0, lk), "REPLACE")
    G["l_bein"].add([v.index], 0.26 + 0.74 * sstep(0.09, lz(0.34), c.z), "REPLACE")

hm = bpy.data.materials.new("haar")
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
L.new(maprange(N, L, nz.outputs["Fac"], 0.30, 0.70, 0.68, 0.87), add1.inputs[1])
add2 = N.new("ShaderNodeMath")
add2.operation = "ADD"
L.new(add1.outputs[0], add2.inputs[0])
L.new(maprange(N, L, sep.outputs[2], 0.14, 0.42, 0.13, 0.0), add2.inputs[1])       # Beine dunkler
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
tip.inputs[0].default_value = 0.0
L.new(maprange(N, L, hi.outputs["Intercept"], 0.45, 1.0, 0.0, 0.2), tip.inputs[1])  # helle Spitzen
kopfhell = N.new("ShaderNodeMath")
kopfhell.operation = "ADD"
L.new(tip.outputs[0], kopfhell.inputs[0])
L.new(maprange(N, L, sep.outputs[0], 0.86, 0.96, 0.0, 0.10), kopfhell.inputs[1])
L.new(kopfhell.outputs[0], add4.inputs[1])
L.new(add4.outputs[0], hb.inputs["Melanin"])
hb.inputs["Random Color"].default_value = 0.1
L.new(hb.outputs[0], N["Material Output"].inputs["Surface"])
body.data.materials.append(hm)
def fell(name, count, length, normal, align, dens, lng, kids, clump, rough1, rough2, radius, seed):
    if FUR <= 0:
        return
    count = int(count * FUR)
    kids = max(3, int(kids * (0.5 + 0.5 * FUR)))
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
fell("deckhaar", 14000, 0.15, 0.066, (-0.052, 0.0, -0.036), "d_deck", "l_koerper", 9, 0.86, 0.013, 0.012, 0.0034, 12)
fell("beinfell", 60000, 0.082, 0.046, (-0.012, 0.0, -0.028), "d_bein", "l_bein", 14, 0.56, 0.008, 0.005, 0.0029, 13)

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


# ==================================================================================================
# KOPF ALS KONTROLLKAEFIG (Bauweise B): rund 300 von Hand gesetzte Punkte, gespiegelt, Quads,
# Subdivision Stufe 3 mit Crease an Lippe, Nasenpolster und Augenrand. Augenhoehle, Lippenspalte und
# Maulinneres sind echte Geometrie. Der Kopfrahmen: x nach vorn (0 = Ohrbasis, 0.50 = Nasenspitze),
# z nach oben (0 = Hoehe des Lippenansatzes hinten), y nach links.
# ==================================================================================================
HEAD_O = Vector((0.955, 0.0, 1.052))
HEAD_P = math.radians(7.0)            # Nase leicht nach unten
_hc, _hs = math.cos(HEAD_P), math.sin(HEAD_P)


def hw(x, y, z):
    return Vector((HEAD_O.x + x * _hc + z * _hs, y, HEAD_O.z - x * _hs + z * _hc))


def hv(x, y, z):
    return Vector((x * _hc + z * _hs, y, -x * _hs + z * _hc))


def wh(v):
    dx, dz = v.x - HEAD_O.x, v.z - HEAD_O.z
    return Vector((dx * _hc - dz * _hs, v.y, dx * _hs + dz * _hc))


class Cage:
    """Kontrollkaefig: benannte Punkte auf der +y-Seite, Spiegelung beim Bauen."""

    def __init__(self):
        self.v = {}
        self.kw = {}
        self.f = []
        self.cr = []

    def add(self, name, x, y, z, kw=0.0):
        self.v[name] = (x, y, z)
        self.kw[name] = kw
        return name

    def q(self, *names, mat=0):
        self.f.append((names, mat))

    def crease(self, names, val):
        for a, c in zip(names, names[1:]):
            self.cr.append((a, c, val))

    def build(self, objname, xform=hw, mirror=True, flip_y=False):
        bm = bmesh.new()
        cl = bm.edges.layers.float.new("crease_edge")
        vm = {}
        for n, (x, y, z) in self.v.items():
            yy = -y if flip_y else y
            vm[(n, 1)] = bm.verts.new(xform(x, yy, z))
            if mirror and abs(y) > 1e-7:
                vm[(n, -1)] = bm.verts.new(xform(x, -yy, z))
            else:
                vm[(n, -1)] = vm[(n, 1)]
        bm.verts.index_update()
        for names, mat in self.f:
            for s in ((1, -1) if mirror else (1,)):
                vs = [vm[(n, s)] for n in names]
                if s == -1:
                    if all(vm[(n, 1)] is vm[(n, -1)] for n in names):
                        continue
                    vs.reverse()
                try:
                    fa = bm.faces.new(vs)
                    fa.material_index = mat
                except ValueError:
                    print("KAEFIG Doppelflaeche", names)
        bm.edges.index_update()
        for a, c, val in self.cr:
            for s in ((1, -1) if mirror else (1,)):
                e = bm.edges.get((vm[(a, s)], vm[(c, s)]))
                if e is None:
                    print("KAEFIG keine Kante", a, c)
                else:
                    e[cl] = val
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        me = bpy.data.meshes.new(objname)
        bm.to_mesh(me)
        idx = {key: v.index for key, v in vm.items()}
        bm.free()
        o = bpy.data.objects.new(objname, me)
        col.objects.link(o)
        return o, idx


def subsurf_apply(o, level):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    m = o.modifiers.new("ss", "SUBSURF")
    m.levels = level
    m.render_levels = level
    m.use_creases = True
    m.boundary_smooth = "ALL"
    bpy.ops.object.modifier_apply(modifier=m.name)
    for p in o.data.polygons:
        p.use_smooth = True


# ---- Materialien des Kopfes
def uv_mask(N, L):
    u = N.new("ShaderNodeUVMap")
    u.uv_map = "maske"
    s = N.new("ShaderNodeSeparateXYZ")
    L.new(u.outputs[0], s.inputs[0])
    return s


SKIN = bpy.data.materials.new("kopfhaut")
SKIN.use_nodes = True
Ns, Ls = SKIN.node_tree.nodes, SKIN.node_tree.links
_s = uv_mask(Ns, Ls)
# Haut in Fellfarbe, ueber Melanin aus der Maske (x); y dunkelt zur schwarzen Lippen- und Lidhaut ab
_ramp = Ns.new("ShaderNodeValToRGB")
_ramp.color_ramp.elements[0].position = 0.28
_ramp.color_ramp.elements[0].color = (0.10, 0.065, 0.038, 1)
_ramp.color_ramp.elements[1].position = 0.92
_ramp.color_ramp.elements[1].color = (0.018, 0.012, 0.009, 1)
Ls.new(_s.outputs[0], _ramp.inputs["Fac"])
_skcol = mix_rgba(Ns, Ls, _s.outputs[1], _ramp.outputs["Color"], (0.012, 0.0105, 0.01))
Ls.new(_skcol, Ns["Principled BSDF"].inputs["Base Color"])
Ns["Principled BSDF"].inputs["Roughness"].default_value = 0.72
Ns["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.08

# Nase: Anthrazit, ledrig-feucht, feine Koernung
NOSEM = bpy.data.materials.new("nasenleder")
NOSEM.use_nodes = True
Nn, Ln = NOSEM.node_tree.nodes, NOSEM.node_tree.links
_b = Nn["Principled BSDF"]
_b.inputs["Base Color"].default_value = (0.021, 0.0185, 0.018, 1)
_b.inputs["Specular IOR Level"].default_value = 0.36
_nz = Nn.new("ShaderNodeTexNoise")
_nz.inputs["Scale"].default_value = 620
_nz.inputs["Detail"].default_value = 3
_nz2 = Nn.new("ShaderNodeTexVoronoi")
_nz2.inputs["Scale"].default_value = 330
_bpn = Nn.new("ShaderNodeBump")
_bpn.inputs["Strength"].default_value = 0.65
_bpn.inputs["Distance"].default_value = 0.0022
Ln.new(_nz2.outputs["Distance"], _bpn.inputs["Height"])
Ln.new(_bpn.outputs["Normal"], _b.inputs["Normal"])
Ln.new(maprange(Nn, Ln, _nz.outputs["Fac"], 0.35, 0.65, 0.26, 0.40), _b.inputs["Roughness"])

LIPM = bpy.data.materials.new("lippe")
LIPM.use_nodes = True
Nl_, Ll_ = LIPM.node_tree.nodes, LIPM.node_tree.links
_ls = uv_mask(Nl_, Ll_)
# Aussen schwarze Lippe, nach innen Uebergang ins Zahnfleisch (Maske y)
Ll_.new(mix_rgba(Nl_, Ll_, _ls.outputs[1], (0.09, 0.024, 0.028), (0.010, 0.009, 0.0085)), Nl_["Principled BSDF"].inputs["Base Color"])
Nl_["Principled BSDF"].inputs["Roughness"].default_value = 0.6
Nl_["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.22
GUM = bpy.data.materials.new("zahnfleisch")
GUM.use_nodes = True
Ng_, Lg_ = GUM.node_tree.nodes, GUM.node_tree.links
_gb = Ng_["Principled BSDF"]
_gt = Ng_.new("ShaderNodeTexCoord")
_gs = Ng_.new("ShaderNodeSeparateXYZ")
Lg_.new(_gt.outputs["Generated"], _gs.inputs[0])
# Rachen dunkel, vorn rosa-dunkel (Generated.x laeuft ueber die Kopflaenge)
_gc = mix_rgba(Ng_, Lg_, maprange(Ng_, Lg_, _gs.outputs[0], 0.60, 0.76, 0.0, 1.0), (0.012, 0.004, 0.005), (0.125, 0.030, 0.036))
Lg_.new(_gc, _gb.inputs["Base Color"])
_gb.inputs["Roughness"].default_value = 0.52
_gb.inputs["Specular IOR Level"].default_value = 0.35
_gw = Ng_.new("ShaderNodeTexWave")
_gw.wave_type = "BANDS"
_gw.bands_direction = "X"
_gw.inputs["Scale"].default_value = 26
_gw.inputs["Distortion"].default_value = 1.5
_gbp = Ng_.new("ShaderNodeBump")
_gbp.inputs["Strength"].default_value = 0.55
_gbp.inputs["Distance"].default_value = 0.004
Lg_.new(_gt.outputs["Generated"], _gw.inputs["Vector"])
Lg_.new(_gw.outputs["Fac"], _gbp.inputs["Height"])
Lg_.new(_gbp.outputs["Normal"], _gb.inputs["Normal"])
TONGUE = plain("zunge", (0.155, 0.040, 0.047), 0.52)
_tn = TONGUE.node_tree.nodes
_tnz = _tn.new("ShaderNodeTexNoise")
_tnz.inputs["Scale"].default_value = 170
_tnz.inputs["Detail"].default_value = 3
_tbp = _tn.new("ShaderNodeBump")
_tbp.inputs["Strength"].default_value = 0.7
_tbp.inputs["Distance"].default_value = 0.003
TONGUE.node_tree.links.new(_tnz.outputs["Fac"], _tbp.inputs["Height"])
TONGUE.node_tree.links.new(_tbp.outputs["Normal"], _tn["Principled BSDF"].inputs["Normal"])
LIDM = plain("lidhaut", (0.007, 0.0058, 0.0055), 0.78)
LIDM.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.12
PADM = plain("ballen", (0.013, 0.011, 0.010), 0.9)
PADM.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.18

# Auge: Pupille, Iris (dunkles Bernstein), dunkler Rand; ein kleiner Glanzpunkt ueber die Rauheit
EYEM = bpy.data.materials.new("augapfel")
EYEM.use_nodes = True
Ne_, Le_ = EYEM.node_tree.nodes, EYEM.node_tree.links
_tc = Ne_.new("ShaderNodeTexCoord")
_sp = Ne_.new("ShaderNodeSeparateXYZ")
Le_.new(_tc.outputs["Object"], _sp.inputs[0])
_cb = Ne_.new("ShaderNodeCombineXYZ")
Le_.new(_sp.outputs[0], _cb.inputs[0])
Le_.new(_sp.outputs[1], _cb.inputs[1])
_ln = Ne_.new("ShaderNodeVectorMath")
_ln.operation = "LENGTH"
Le_.new(_cb.outputs[0], _ln.inputs[0])
_rp = Ne_.new("ShaderNodeValToRGB")
_cr = _rp.color_ramp
_cr.elements[0].position = 0.0
_cr.elements[0].color = (0.001, 0.001, 0.001, 1)
_cr.elements[1].position = 1.0
_cr.elements[1].color = (0.004, 0.003, 0.003, 1)
for _pos, _c in ((0.27, (0.001, 0.001, 0.001, 1)), (0.33, (0.05, 0.02, 0.006, 1)), (0.5, (0.105, 0.043, 0.011, 1)), (0.68, (0.032, 0.013, 0.005, 1)), (0.78, (0.004, 0.003, 0.003, 1))):
    _el = _cr.elements.new(_pos)
    _el.color = _c
_mr = Ne_.new("ShaderNodeMapRange")
_mr.inputs["From Min"].default_value = 0.0
_mr.inputs["From Max"].default_value = 0.0175
Le_.new(_ln.outputs["Value"], _mr.inputs["Value"])
Le_.new(_mr.outputs[0], _rp.inputs["Fac"])
Le_.new(_rp.outputs["Color"], Ne_["Principled BSDF"].inputs["Base Color"])
Ne_["Principled BSDF"].inputs["Roughness"].default_value = 0.11
Ne_["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.26

# Kopfhaar: Melanin aus der Maske (x), dazu Streuung je Haar und helle Spitzen
HK = bpy.data.materials.new("haar_kopf")
HK.use_nodes = True
Nh, Lh = HK.node_tree.nodes, HK.node_tree.links
Nh.remove(Nh["Principled BSDF"])
_hb = Nh.new("ShaderNodeBsdfHairPrincipled")
_hb.parametrization = "MELANIN"
_hb.inputs["Melanin Redness"].default_value = 0.28
_hb.inputs["Roughness"].default_value = 0.42
_hb.inputs["Radial Roughness"].default_value = 0.8
_hb.inputs["Coat"].default_value = 0.0
_hb.inputs["Random Color"].default_value = 0.12
_hi = Nh.new("ShaderNodeHairInfo")
_s2 = uv_mask(Nh, Lh)
_add = Nh.new("ShaderNodeMath")
_add.operation = "ADD"
_tch = Nh.new("ShaderNodeTexCoord")
_nzh = Nh.new("ShaderNodeTexNoise")
_nzh.inputs["Scale"].default_value = 16
_nzh.inputs["Detail"].default_value = 5
Lh.new(_tch.outputs["Generated"], _nzh.inputs["Vector"])
_addm = Nh.new("ShaderNodeMath")
_addm.operation = "ADD"
Lh.new(_s2.outputs[0], _addm.inputs[0])
Lh.new(maprange(Nh, Lh, _nzh.outputs["Fac"], 0.32, 0.68, -0.05, 0.05), _addm.inputs[1])
Lh.new(_addm.outputs[0], _add.inputs[0])
Lh.new(maprange(Nh, Lh, _hi.outputs["Random"], 0.0, 1.0, -0.06, 0.06), _add.inputs[1])
_sub = Nh.new("ShaderNodeMath")
_sub.operation = "SUBTRACT"
_sub.use_clamp = True
Lh.new(_add.outputs[0], _sub.inputs[0])
Lh.new(maprange(Nh, Lh, _hi.outputs["Intercept"], 0.5, 1.0, 0.0, 0.14), _sub.inputs[1])
Lh.new(_sub.outputs[0], _hb.inputs["Melanin"])
Lh.new(maprange(Nh, Lh, _s2.outputs[0], 0.32, 0.60, 0.46, 0.27), _hb.inputs["Melanin Redness"])
Lh.new(_hb.outputs[0], Nh["Material Output"].inputs["Surface"])

M_SKIN, M_NOSE, M_LIP, M_GUM, M_LID, M_SOOT = 0, 1, 2, 3, 4, 5

# ---- Die Ringe des Kopfes: x, dann (y, z) je Laengslinie von der Mittellinie oben bis unten
#        k0 Scheitel, k1 Dachkante, k2 Braue/Oberseite, k3 Seite, k3b Lefzenwulst, k4 Oberlippe,
#        k5 Unterlippe (nur vor dem Mundwinkel), k6 Kieferseite, k7 Kieferunterkante, k8 Kehle
RINGS = [
    (-0.26, [(0, .215), (.080, .205), (.130, .150), (.155, .070), (.155, .005), (.142, -.060)], None, [(.100, -.130), (.050, -.160), (0, -.170)]),
    (-0.13, [(0, .235), (.090, .225), (.148, .170), (.172, .080), (.175, .012), (.160, -.060)], None, [(.118, -.140), (.056, -.175), (0, -.185)]),
    (-0.02, [(0, .240), (.095, .230), (.155, .180), (.180, .090), (.183, .020), (.168, -.050)], None, [(.120, -.125), (.056, -.158), (0, -.168)]),
    (0.07, [(0, .243), (.090, .232), (.148, .188), (.176, .100), (.178, .032), (.160, -.035)], None, [(.105, -.105), (.050, -.135), (0, -.145)]),
    (0.15, [(0, .238), (.080, .228), (.128, .192), (.158, .112), (.158, .040), (.140, -.030)], None, [(.090, -.090), (.044, -.115), (0, -.122)]),
    (0.21, [(0, .222), (.062, .214), (.103, .185), (.125, .108), (.124, .040), (.112, -.024)], None, [(.078, -.075), (.038, -.098), (0, -.105)]),
    (0.255, [(0, .190), (.042, .184), (.073, .166), (.095, .096), (.100, .032), (.098, -.034)], None, [(.074, -.068), (.036, -.090), (0, -.096)]),
    (0.30, [(0, .128), (.032, .125), (.057, .117), (.074, .075), (.085, .022), (.081, -.031)], (.077, -.033), [(.069, -.060), (.037, -.083), (0, -.088)]),
    (0.345, [(0, .103), (.030, .101), (.055, .091), (.072, .063), (.083, .014), (.079, -.028)], (.075, -.030), [(.067, -.060), (.037, -.082), (0, -.086)]),
    (0.39, [(0, .095), (.030, .093), (.055, .083), (.071, .057), (.082, .010), (.078, -.026)], (.074, -.028), [(.066, -.061), (.036, -.082), (0, -.085)]),
    (0.435, [(0, .091), (.030, .089), (.054, .079), (.069, .053), (.078, .007), (.075, -.025)], (.069, -.027), [(.062, -.062), (.034, -.082), (0, -.085)]),
    (0.468, [(0, .088), (.029, .086), (.052, .076), (.065, .050), (.072, .006), (.068, -.025)], (.059, -.027), [(.051, -.062), (.027, -.078), (0, -.081)]),
]
UPPER = ["k0", "k1", "k2", "k3", "k3b", "k4"]
LOWER = ["k6", "k7", "k8"]
# Anteil des Kiefers je Ring an den unteren Linien (Stufe nach hinten: Backe und Kehle dehnen sich)
JAWW = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.10, 4: 0.34, 5: 0.64, 6: 0.90}
HEAD = Cage()
for i, (x, up, lip, low) in enumerate(RINGS):
    jw = JAWW.get(i, 1.0)
    for name, (y, z) in zip(UPPER, up):
        kw = 0.0
        if name == "k4" and i <= 6:
            kw = {3: 0.04, 4: 0.12, 5: 0.28, 6: 0.5}.get(i, 0.0)
        HEAD.add("%s_%d" % (name, i), x, y, z, kw)
    if lip:
        HEAD.add("k5_%d" % i, x, lip[0], lip[1], 1.0)
    for name, (y, z) in zip(LOWER, low):
        HEAD.add("%s_%d" % (name, i), x, y, z, jw)

CORNER = "k4_6"
# Der Unterkiefer ist kuerzer als der Oberkiefer: die Oberlippe steht vorn ueber
for k_ in ("k5", "k6", "k7", "k8"):
    for i_, dx_ in ((11, -0.012), (10, -0.007), (9, -0.002)):
        n_ = "%s_%d" % (k_, i_)
        x_, y_, z_ = HEAD.v[n_]
        HEAD.v[n_] = (x_ + dx_, y_, z_)
for nm_, w_ in (("k4_7", 0.13), ("k4_8", 0.04), ("k5_7", 0.87), ("k5_8", 0.97), ("k3b_7", 0.05), ("k3b_6", 0.11), ("k3b_5", 0.06)):
    HEAD.kw[nm_] = w_


def rname(k, i):
    return "%s_%d" % (k, i)


EYE_BLOCK = {(5, "k2"), (6, "k2")}
for i in range(len(RINGS) - 1):
    seq = UPPER + LOWER if i < 6 else None
    if i < 6:
        for a, c in zip(seq, seq[1:]):
            if (i, a) in EYE_BLOCK:
                continue
            HEAD.q(rname(a, i), rname(a, i + 1), rname(c, i + 1), rname(c, i))
    elif i == 6:
        for a, c in zip(UPPER, UPPER[1:]):
            if (i, a) in EYE_BLOCK:
                continue
            if c == "k4":
                HEAD.q(rname(a, 6), rname(a, 7), rname("k4", 7), CORNER)
            else:
                HEAD.q(rname(a, 6), rname(a, 7), rname(c, 7), rname(c, 6))
        HEAD.q(CORNER, rname("k5", 7), rname("k6", 7), rname("k6", 6))
        for a, c in zip(LOWER, LOWER[1:]):
            HEAD.q(rname(a, 6), rname(a, 7), rname(c, 7), rname(c, 6))
    else:
        for a, c in zip(UPPER, UPPER[1:]):
            HEAD.q(rname(a, i), rname(a, i + 1), rname(c, i + 1), rname(c, i))
        seq2 = ["k5"] + LOWER
        for a, c in zip(seq2, seq2[1:]):
            HEAD.q(rname(a, i), rname(a, i + 1), rname(c, i + 1), rname(c, i))

# ---- Vorn: Oberlippe bis zur Mittelfurche, Nasenpolster, Unterlippe, Kinn
HEAD.add("f1", 0.481, 0.043, -0.0270)
HEAD.add("f0", 0.490, 0.0, -0.0205)
HEAD.add("g1", 0.465, 0.0345, -0.0285, 1.0)
HEAD.add("g0", 0.477, 0.0, -0.0245, 1.0)
HEAD.add("h1", 0.463, 0.0310, -0.0610, 1.0)
HEAD.add("h0", 0.474, 0.0, -0.0635, 1.0)

# Nasenpolster: Aussenkante A (Fellgrenze), B (Polsterkante), Mittelfurche m, Nasenloecher N
for n, x, y, z in (
    ("a0", 0.487, 0.0, 0.0775), ("a1", 0.487, 0.025, 0.0765), ("a2", 0.484, 0.042, 0.0690), ("a3", 0.479, 0.0495, 0.0530),
    ("a4", 0.479, 0.0460, 0.0345), ("a5", 0.482, 0.034, 0.0210), ("a6", 0.486, 0.016, 0.0145), ("a7", 0.488, 0.0, 0.0115),
    ("b0", 0.496, 0.0, 0.0745), ("b1", 0.497, 0.023, 0.0735), ("b2", 0.494, 0.0385, 0.0665), ("b3", 0.488, 0.0455, 0.0525),
    ("b4", 0.487, 0.0420, 0.0365), ("b5", 0.489, 0.0305, 0.0250), ("b6", 0.492, 0.0140, 0.0185), ("b7", 0.494, 0.0, 0.0155),
    ("m0", 0.502, 0.0, 0.0625), ("m1", 0.501, 0.0, 0.0490), ("m2", 0.4985, 0.0, 0.0365), ("m3", 0.4965, 0.0, 0.0260),
    ("n0", 0.5075, 0.0105, 0.0490), ("n1", 0.5065, 0.0225, 0.0545), ("n2", 0.4985, 0.0370, 0.0590),
    ("n3", 0.4985, 0.0355, 0.0475), ("n4", 0.5015, 0.0235, 0.0365), ("n5", 0.5045, 0.0105, 0.0340),
    ("o0", 0.4955, 0.0125, 0.0470), ("o1", 0.4945, 0.0215, 0.0505), ("o2", 0.4905, 0.0335, 0.0555),
    ("o3", 0.4905, 0.0320, 0.0490), ("o4", 0.4915, 0.0220, 0.0405), ("o5", 0.4935, 0.0125, 0.0380),
    ("oc", 0.4845, 0.0195, 0.0450),
):
    HEAD.add(n, x, y, z)
LOOP_U = [rname(k, 11) for k in UPPER] + ["f1", "f0"]
LOOP_A = ["a%d" % k for k in range(8)]
LOOP_B = ["b%d" % k for k in range(8)]
for k in range(7):
    HEAD.q(LOOP_U[k], LOOP_U[k + 1], LOOP_A[k + 1], LOOP_A[k], mat=M_SKIN)
    HEAD.q(LOOP_A[k], LOOP_A[k + 1], LOOP_B[k + 1], LOOP_B[k], mat=M_NOSE)
# Das Polsterfeld um das Nasenloch (siehe Plan: 6 Streifen plus 3 Eckquads)
for fa in (
    ("n0", "n1", "b1", "b0"), ("n1", "n2", "b2", "b1"), ("n2", "b2", "b3", "b4"), ("n2", "b4", "b5", "n3"),
    ("n3", "b5", "b6", "n4"), ("n4", "b6", "b7", "m3"), ("n4", "m3", "m2", "n5"), ("n5", "m2", "m1", "m0"),
    ("n5", "m0", "b0", "n0"),
):
    HEAD.q(*fa, mat=M_NOSE)
NO = ["n%d" % k for k in range(6)]
NI = ["o%d" % k for k in range(6)]
for k in range(6):
    a, c = k, (k + 1) % 6
    HEAD.q(NO[a], NO[c], NI[c], NI[a], mat=M_SOOT)
    HEAD.q(NI[a], NI[c], "oc", mat=M_SOOT)

# ---- Unterlippe und Kinn
HEAD.q(rname("k5", 11), "g1", "h1", rname("k6", 11))
HEAD.q("g1", "g0", "h0", "h1")
HEAD.q(rname("k6", 11), "h1", "h0", rname("k8", 11), rname("k7", 11))

# ---- Maulinneres: Lippe rollt nach innen, Zahnfleisch, Gaumen und Boden bis zur Rueckwand
EDGE_U = [rname("k4", i) for i in range(7, 12)] + ["f1", "f0"]
EDGE_L = [rname("k5", i) for i in range(7, 12)] + ["g1", "g0"]
U1, U2, L1, L2 = [], [], [], []
for nm_e, nm_i, lst1, lst2, sgn in ((EDGE_U, "u", U1, U2, 1), (EDGE_L, "l", L1, L2, -1)):
    for k, e in enumerate(nm_e):
        x, y, z = HEAD.v[e]
        kw = 0.0 if sgn > 0 else 1.0
        if k == 0:
            kw = 0.10 if sgn > 0 else 0.90
        if k < 5:
            a = HEAD.add("%s1_%d" % (nm_i, k), x, y - 0.0065, z + sgn * 0.006, kw)
            c = HEAD.add("%s2_%d" % (nm_i, k), x, y - 0.015, z + sgn * 0.022, kw)
        else:
            a = HEAD.add("%s1_%d" % (nm_i, k), x - 0.0065, y * 0.86, z + sgn * 0.006, kw)
            c = HEAD.add("%s2_%d" % (nm_i, k), x - 0.016, y * 0.72, z + sgn * 0.022, kw)
        lst1.append(a)
        lst2.append(c)
P_, Q_ = [], []
for k in range(5):
    xu, yu, zu = HEAD.v[EDGE_U[k]]
    xl, yl, zl = HEAD.v[EDGE_L[k]]
    P_.append(HEAD.add("p_%d" % k, xu, 0.0, zu + 0.040, 0.0))
    Q_.append(HEAD.add("q_%d" % k, xl, 0.0, zl - 0.032, 1.0))
for k in range(6):
    HEAD.q(EDGE_U[k], EDGE_U[k + 1], U1[k + 1], U1[k], mat=M_LIP)
    HEAD.q(U1[k], U1[k + 1], U2[k + 1], U2[k], mat=M_GUM)
    HEAD.q(EDGE_L[k], EDGE_L[k + 1], L1[k + 1], L1[k], mat=M_LIP)
    HEAD.q(L1[k], L1[k + 1], L2[k + 1], L2[k], mat=M_GUM)
for k in range(4):
    HEAD.q(U2[k], U2[k + 1], P_[k + 1], P_[k], mat=M_GUM)
    HEAD.q(L2[k], L2[k + 1], Q_[k + 1], Q_[k], mat=M_GUM)
HEAD.q(U2[4], U2[5], U2[6], P_[4], mat=M_GUM)
HEAD.q(L2[4], L2[5], L2[6], Q_[4], mat=M_GUM)
cx, cy, cz = HEAD.v[CORNER]
HEAD.add("cu", cx - 0.002, cy - 0.013, cz, 0.5)
HEAD.q(CORNER, EDGE_U[0], U1[0], "cu", mat=M_LIP)
HEAD.q(CORNER, "cu", L1[0], EDGE_L[0], mat=M_LIP)
HEAD.add("w_t", 0.215, 0.0, 0.030, 0.0)
HEAD.add("w_u", 0.222, 0.050, 0.012, 0.0)
HEAD.add("w_m", 0.210, 0.052, -0.024, 0.5)
HEAD.add("w_l", 0.222, 0.048, -0.052, 1.0)
HEAD.add("w_b", 0.215, 0.0, -0.064, 1.0)
HEAD.add("w_c", 0.195, 0.0, -0.018, 0.5)
HEAD.q(U1[0], U2[0], "w_u", "cu", mat=M_GUM)
HEAD.q(U2[0], P_[0], "w_t", "w_u", mat=M_GUM)
HEAD.q(L1[0], "cu", "w_l", L2[0], mat=M_GUM)
HEAD.q(L2[0], "w_l", "w_b", Q_[0], mat=M_GUM)
HEAD.q("cu", "w_u", "w_m", "w_l", mat=M_SOOT)
HEAD.q("w_t", "w_u", "w_m", "w_c", mat=M_SOOT)
HEAD.q("w_c", "w_m", "w_l", "w_b", mat=M_SOOT)

# ---- Auge: Hoehle als echtes Loch im Kaefig. Vier Schlaufen um das Auge, die letzte faellt nach innen.
EYE_C = Vector((0.262, 0.0745, 0.1235))
EYE_N = Vector((0.68, 0.67, 0.29)).normalized()     # Flaechennormale an der Augenstelle
_ea = Vector((0.86, -0.30, -0.27))
EYE_A = (_ea - EYE_N * _ea.dot(EYE_N)).normalized()  # Richtung aeusserer -> innerer Augenwinkel
EYE_B = EYE_N.cross(EYE_A).normalized()
if EYE_B.z < 0:
    EYE_B = -EYE_B
EYE_G = Vector((0.86, 0.49, 0.12)).normalized()    # Blickrichtung
RIM = [(-0.0170, 0.0036), (-0.0010, 0.0086), (0.0160, 0.0002), (0.0170, -0.0028), (0.0, -0.0062), (-0.0175, 0.0006)]
LOOP0 = [rname("k2", 5), rname("k2", 6), rname("k2", 7), rname("k3", 7), rname("k3", 6), rname("k3", 5)]
EYE_LOOPS = (
    ("e1", 1.65, 2.60, (0.0110, 0.0130, 0.0085, 0.0015, 0.0020, 0.0040)),     # Orbita: oben der Brauenwulst
    ("e2", 1.26, 1.55, (0.0080, 0.0090, 0.0050, 0.0010, 0.0015, 0.0025)),     # Lid aussen
    ("e3", 1.00, 1.00, (0.0050, 0.0065, 0.0030, 0.0000, 0.0005, 0.0010)),     # Lidrand (Crease)
    ("e4", 0.88, 0.95, (-0.012, -0.012, -0.012, -0.012, -0.012, -0.012)),     # faellt in die Hoehle
)


def eye_pt(al, be, ga):
    return EYE_C + EYE_A * al + EYE_B * be + EYE_N * ga


prev = LOOP0
for tag, sa, sb, gam in EYE_LOOPS:
    cur = []
    for k, (al, be) in enumerate(RIM):
        p = eye_pt(al * sa, be * sb, gam[k])
        cur.append(HEAD.add("%s_%d" % (tag, k), p.x, p.y, p.z))
    mat = M_SKIN if tag == "e1" else M_LID
    if tag == "e2":
        mat = M_SKIN
    for k in range(6):
        c = (k + 1) % 6
        HEAD.q(prev[k], prev[c], cur[c], cur[k], mat=mat)
    prev = cur
HEAD.q(*prev, mat=M_LID)

# ---- Falten und Kanten
HEAD.crease([CORNER] + EDGE_U, 0.95)
HEAD.crease([CORNER] + EDGE_L, 0.95)
HEAD.crease(["e3_%d" % k for k in range(6)] + ["e3_0"], 0.92)
HEAD.crease(LOOP_B, 0.55)
HEAD.crease(NO + [NO[0]], 0.90)
HEAD.crease(["b0", "m0", "m1", "m2", "m3", "b7", "a7", "f0"], 0.72)

head_cage, head_idx = HEAD.build("baer_kopf")
head = head_cage
for m_ in (SKIN, NOSEM, LIPM, GUM, LIDM, SOOTY, HK):
    head.data.materials.append(m_)

# ---- Gewichte im Kaefig: der Unterkiefer haengt ganz am Knochen "kiefer", nach hinten laeuft die Backe aus
hg = {n: head.vertex_groups.new(name=n) for n in ("kopf", "hals", "brust", "kiefer")}
for (name, s), i_ in head_idx.items():
    x, y, z = HEAD.v[name]
    jw = HEAD.kw[name]
    wh_ = 1.0 - smooth_(-0.17, 0.02, x)
    wb_ = (1.0 - smooth_(-0.33, -0.2, x)) * 0.4
    rest = max(0.0, 1.0 - jw)
    wk = rest * (1.0 - wh_)
    wh2 = rest * wh_ * (1.0 - wb_)
    wb2 = rest * wh_ * wb_
    hg["kiefer"].add([i_], jw, "REPLACE")
    hg["kopf"].add([i_], wk, "REPLACE")
    hg["hals"].add([i_], wh2, "REPLACE")
    hg["brust"].add([i_], wb2, "REPLACE")

subsurf_apply(head, 3)
head_me = head.data
head_me.update()
print("KOPF Netz: Kaefig", len(HEAD.v), "Punkte halb,", len(head_idx) // 2, "; nach Stufe 3:", len(head_me.vertices), "Punkte", len(head_me.polygons), "Flaechen")
# Normalen muessen nach aussen zeigen
_topv = max(head_me.vertices, key=lambda v: v.co.z)
if _topv.normal.z < 0:
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = head
    head.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode="OBJECT")
    head_me.update()
    print("KOPF Normalen gedreht")

# ---- Felder je Punkt des fertigen Netzes: Abstand zu Nase, Lippe, Lid; daraus Farbe und Haarlaenge
NOSE_C = Vector((0.497, 0.0, 0.045))
EYE_L = EYE_C.copy()
EYE_R = Vector((EYE_C.x, -EYE_C.y, EYE_C.z))
nv = len(head_me.vertices)
matof = [set() for _ in range(nv)]
for p in head_me.polygons:
    for vi in p.vertices:
        matof[vi].add(p.material_index)


def kd_of(mats):
    idxs = [i for i in range(nv) if matof[i] & mats]
    t = kdtree.KDTree(len(idxs))
    for n_, i in enumerate(idxs):
        t.insert(head_me.vertices[i].co, i)
    t.balance()
    return t


KD_NOSE = kd_of({M_NOSE, M_SOOT})
KD_LIP = kd_of({M_LIP})
KD_LID = kd_of({M_LID})
KD_GUM = kd_of({M_GUM})
F_FUR, F_MEL, F_DARK, F_LEN, F_FLOW = [0.0] * nv, [0.0] * nv, [0.0] * nv, [0.0] * nv, [None] * nv


def mix_(a, c, t):
    return a + (c - a) * t


for i, v in enumerate(head_me.vertices):
    pw = v.co
    p = wh(pw)
    x, y, z = p.x, p.y, p.z
    is_fur = matof[i] == {M_SKIN}
    F_FUR[i] = 1.0 if is_fur else 0.0
    dn = KD_NOSE.find(pw)[2]
    dl = KD_LIP.find(pw)[2]
    de = KD_LID.find(pw)[2]
    deye = min((p - EYE_L).length, (p - EYE_R).length)
    muz = smooth_(0.255, 0.365, x)              # 1 auf der Schnauze, 0 am Schaedel
    top = smooth_(0.03, 0.125, z)
    # Melanin (dunkler = hoeher): Stirn goldbraun, Wange und Nacken wie der Koerper, Schnauze hell
    mh = mix_(0.62, 0.53, top)
    mh += 0.03 * (1.0 - smooth_(-0.12, 0.08, x))
    mm = mix_(0.335, 0.40, smooth_(0.045, 0.085, z))
    mm = mix_(mm, 0.47, 1.0 - smooth_(-0.055, -0.03, z))
    m = mix_(mh, mm, muz)
    m += 0.12 * (1.0 - smooth_(0.020, 0.060, deye))
    m = mix_(m, 0.74, 1.0 - smooth_(0.006, 0.040, dn))
    m = mix_(m, 0.68, 1.0 - smooth_(0.001, 0.012, dl))
    F_MEL[i] = max(0.2, min(0.95, m))
    F_DARK[i] = max(1.0 - smooth_(0.0010, 0.0065, dl), 1.0 - smooth_(0.001, 0.013, de), 1.0 - smooth_(0.001, 0.007, dn))
    if M_LIP in matof[i]:
        F_DARK[i] = smooth_(0.0, 0.0075, KD_GUM.find(pw)[2])
    # Haarlaenge in Metern
    side = 1.0 - smooth_(0.02, 0.115, z)
    lh = mix_(0.036, mix_(0.098, 0.046, smooth_(0.10, 0.27, x)), side)
    lh = mix_(lh, 0.118, 1.0 - smooth_(-0.03, 0.11, x))
    ln = mix_(lh, 0.0165, smooth_(0.235, 0.375, x))
    ln = mix_(0.0135, ln, smooth_(0.012, 0.055, de))
    ln = mix_(0.006, ln, smooth_(0.002, 0.040, dn))
    ln = mix_(0.0085, ln, smooth_(0.001, 0.016, dl))
    F_LEN[i] = ln
    # Strich: von der Nase nach hinten, am Polster strahlig, an der Wange nach hinten-unten, um das Auge herum
    fl = Vector((-1.0, 0.0, 0.0))
    fl.z -= 0.42 * side * (1.0 - muz)
    fl.y += (1.0 if y >= 0 else -1.0) * 0.30 * side * (1.0 - muz)
    fl.z -= 0.16 * (1.0 - top) * muz
    fl.y += (1.0 if y >= 0 else -1.0) * 0.20 * smooth_(0.0, 0.06, abs(y)) * top * (1.0 - muz)
    rn = p - NOSE_C
    wn = 1.0 - smooth_(0.035, 0.115, rn.length)
    fl = fl.lerp(rn.normalized(), wn * 0.92)
    reye = p - (EYE_L if y >= 0 else EYE_R)
    we = 1.0 - smooth_(0.018, 0.06, reye.length)
    if we > 0:
        fl = fl.lerp(reye.normalized(), we * 0.28)
    fl = hv(fl.x, fl.y, fl.z)
    F_FLOW[i] = fl.normalized()

# UV-Schicht "maske": u = Melanin, v = schwarze Haut. Kommt in Cycles auch am Haar an (geprueft).
_uvl = head_me.uv_layers.new(name="maske")
for li, l in enumerate(head_me.loops):
    _uvl.uv[li].vector = (F_MEL[l.vertex_index], F_DARK[l.vertex_index])

# Dichtegruppen je Fellart aus der Haarlaenge
HGD = {n: head.vertex_groups.new(name=n) for n in ("d_kurz", "d_mittel", "d_lang")}
for i in range(nv):
    ln = F_LEN[i]
    fur_ = F_FUR[i]
    # Breite Ueberlappung, damit zwischen Schnauze und Wange keine Kante im Fell steht
    wk = (1.0 - smooth_(0.017, 0.040, ln)) * fur_
    wm = smooth_(0.017, 0.040, ln) * (1.0 - smooth_(0.050, 0.074, ln)) * fur_
    wl = smooth_(0.050, 0.074, ln) * fur_
    HGD["d_kurz"].add([i], wk, "REPLACE")
    HGD["d_mittel"].add([i], wm, "REPLACE")
    HGD["d_lang"].add([i], wl, "REPLACE")

KD_HEAD = kdtree.KDTree(nv)
for i, v in enumerate(head_me.vertices):
    KD_HEAD.insert(v.co, i)
KD_HEAD.balance()

mh_ = head.modifiers.new("skelett", "ARMATURE")
mh_.object = ao
head.parent = ao


def hair_system(o, name, count, kids, dens, radius, clump, rough, slot, seed, tip=0.04):
    """Haarsystem, dessen Elternhaare danach per Python gekaemmt werden."""
    o.modifiers.new(name, "PARTICLE_SYSTEM")
    ps = o.particle_systems[-1]
    ps.seed = seed
    st = ps.settings
    st.name = name
    st.type = "HAIR"
    st.use_advanced_hair = True
    st.count = max(10, int(count))
    st.hair_step = 4
    st.display_step = 2
    st.emit_from = "FACE"
    st.normal_factor = 0.01
    st.child_type = "INTERPOLATED"
    st.child_percent = 2
    st.rendered_child_count = kids
    st.child_length = 0.9
    st.child_length_threshold = 0.3
    st.clump_factor = clump
    st.clump_shape = 0.2
    st.roughness_1 = rough
    st.roughness_1_size = 0.5
    st.roughness_endpoint = rough
    st.material_slot = slot
    st.root_radius = 1.0
    st.tip_radius = tip
    st.radius_scale = radius
    if dens:
        ps.vertex_group_density = dens
    return ps


def comb(o, name, field, jitter=0.2, lift0=34.0, lift1=9.0, lenvar=0.2):
    """Kaemmt die Elternhaare: field(root) -> (Normale, Strichrichtung, Laenge). Geht ohne Editmodus-Bedienung:
    einmal rein und raus fuellt die Originaldaten, dann setzt co_object_set die Schluessel."""
    idx = [i for i, p in enumerate(o.particle_systems) if o.modifiers[name].particle_system == p][0]
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    o.particle_systems.active_index = idx
    bpy.context.evaluated_depsgraph_get().update()
    bpy.ops.particle.particle_edit_toggle()
    bpy.ops.particle.particle_edit_toggle()
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    oe = o.evaluated_get(dg)
    mde = oe.modifiers[name]
    pse = mde.particle_system
    pso = o.modifiers[name].particle_system
    n_ = 0
    for po, pe in zip(pso.particles, pse.particles):
        root = pe.hair_keys[0].co_object(oe, mde, pe)
        nrm, flow, ln = field(root)
        if ln <= 0.0:
            ln = 0.001
        # seitlich streuen
        side = nrm.cross(flow)
        flow2 = (flow + side * random.gauss(0.0, jitter)).normalized()
        ln2 = ln * (1.0 + random.uniform(-lenvar, lenvar))
        a0 = math.radians(lift0 + random.uniform(-8, 8))
        a1 = math.radians(lift1 + random.uniform(-5, 5))
        keys = po.hair_keys
        cnt = len(keys)
        pos = root.copy()
        for j, k in enumerate(keys):
            if j > 0:
                t = (j - 0.5) / (cnt - 1)
                an = a0 + (a1 - a0) * t
                d = flow2 * math.cos(an) + nrm * math.sin(an)
                pos = pos + d * (ln2 / (cnt - 1))
            k.co_object_set(oe, mde, po, pos)
        n_ += 1
    print("GEKAEMMT", name, n_)


def head_field(root):
    i = KD_HEAD.find(root)[1]
    nrm = head_me.vertices[i].normal
    fl = F_FLOW[i]
    t = fl - nrm * fl.dot(nrm)
    if t.length < 0.05:
        t = nrm.cross(Vector((0, 1, 0)))
    return nrm.copy(), t.normalized(), F_LEN[i]


if FUR > 0:
    bpy.context.view_layer.update()
    hair_system(head, "fell_kurz", 60000 * FUR_K, 3, "d_kurz", 0.00085, 0.0, 0.0008, "haar_kopf", 21)
    hair_system(head, "fell_mittel", 22000 * FUR_K, 4, "d_mittel", 0.00145, 0.08, 0.002, "haar_kopf", 22)
    hair_system(head, "fell_lang", 12000 * FUR_K, 7, "d_lang", 0.0026, 0.55, 0.009, "haar_kopf", 23, tip=0.03)
    comb(head, "fell_kurz", head_field, jitter=0.14, lift0=17.0, lift1=4.0, lenvar=0.2)
    comb(head, "fell_mittel", head_field, jitter=0.22, lift0=30.0, lift1=9.0)
    comb(head, "fell_lang", head_field, jitter=0.30, lift0=46.0, lift1=12.0, lenvar=0.3)

extras = []

# ---- Auge: echte Kugel, tief in der Hoehle; zu sehen ist nur, was die Lider freilassen
for sy, nm in ((1, "auge_l"), (-1, "auge_r")):
    c_ = EYE_C - EYE_N * 0.0145
    c_w = hw(c_.x, sy * c_.y, c_.z)
    g_ = hv(EYE_G.x, sy * EYE_G.y, EYE_G.z)
    o_ = sphere(nm, tuple(c_w), 0.0175, EYEM, seg=32)
    o_.rotation_mode = "QUATERNION"
    o_.rotation_quaternion = g_.to_track_quat("Z", "Y")
    extras.append((o_, "kopf"))


# ---- Ohr als Schale mit Oeffnung nach vorn-aussen
def make_ear(flip):
    c = Cage()
    N_ = 10
    ec = Vector((-0.020, 0.160, 0.226))
    n_ = Vector((0.70, 0.60, 0.30)).normalized()
    up = Vector((0, 0, 1))
    t1 = (up - n_ * up.dot(n_)).normalized()
    t2 = n_.cross(t1).normalized()
    prof = [("c1", .014, -.015), ("c2", .027, -.009), ("c3", .037, .000), ("rim", .0435, .007), ("o1", .0475, .000), ("o2", .046, -.015), ("o3", .032, -.030)]
    for tag, rad, dep in prof:
        for k in range(N_):
            th = 2 * math.pi * k / N_
            st_ = 1.04 if math.sin(th) > 0 else 0.92
            p = ec + t2 * rad * math.cos(th) + t1 * rad * st_ * math.sin(th) + n_ * dep
            c.add("%s_%d" % (tag, k), p.x, p.y, p.z)
    p0 = ec + n_ * -0.018
    p1 = ec + n_ * -0.037
    c.add("ci", p0.x, p0.y, p0.z)
    c.add("co", p1.x, p1.y, p1.z)
    for a_, b_ in zip(prof, prof[1:]):
        for k in range(N_):
            k2 = (k + 1) % N_
            mat = 0
            c.q("%s_%d" % (a_[0], k), "%s_%d" % (a_[0], k2), "%s_%d" % (b_[0], k2), "%s_%d" % (b_[0], k), mat=mat)
    for k in range(N_):
        k2 = (k + 1) % N_
        c.q("ci", "c1_%d" % k, "c1_%d" % k2)
        c.q("co", "o3_%d" % k2, "o3_%d" % k)
    o, _ = c.build("ohr_r" if flip else "ohr_l", mirror=False, flip_y=flip)
    o.data.materials.append(SKIN)
    o.data.materials.append(HK)
    subsurf_apply(o, 2)
    me = o.data
    me.update()
    uvl = me.uv_layers.new(name="maske")
    nv_ = len(me.vertices)
    inner = [0.0] * nv_
    ec_w = hw(ec.x, -ec.y if flip else ec.y, ec.z)
    n_w = hv(n_.x, -n_.y if flip else n_.y, n_.z)
    for i, v in enumerate(me.vertices):
        rel = v.co - ec_w
        dep = rel.dot(n_w)
        rad = (rel - n_w * dep).length
        # innen: Mulde vor der Mittelebene und innerhalb des Rands
        inner[i] = smooth_(0.046, 0.038, rad) * smooth_(-0.025, -0.010, dep) if v.normal.dot(n_w) > 0 else 0.0
    for li, l in enumerate(me.loops):
        w = inner[l.vertex_index]
        uvl.uv[li].vector = (mix_(0.80, 0.44, w), 0.0)
    gi = o.vertex_groups.new(name="d_innen")
    ga = o.vertex_groups.new(name="d_aussen")
    for i in range(nv_):
        gi.add([i], inner[i], "REPLACE")
        ga.add([i], 1.0 - inner[i], "REPLACE")
    if FUR > 0:
        kd = kdtree.KDTree(nv_)
        for i, v in enumerate(me.vertices):
            kd.insert(v.co, i)
        kd.balance()

        def field_o(root):
            i = kd.find(root)[1]
            nrm = me.vertices[i].normal.copy()
            rel = root - ec_w
            t = rel - nrm * rel.dot(nrm)
            if t.length < 0.002:
                t = nrm.cross(Vector((0, 1, 0)))
            return nrm, t.normalized(), 0.017

        def field_i(root):
            i = kd.find(root)[1]
            nrm = me.vertices[i].normal.copy()
            rel = root - ec_w
            t = rel - nrm * rel.dot(nrm)
            if t.length < 0.002:
                t = nrm.cross(Vector((0, 1, 0)))
            return nrm, t.normalized(), 0.026

        hair_system(o, "ohr_aussen", 1800 * FUR_K, 6, "d_aussen", 0.0013, 0.1, 0.002, "haar_kopf", 31)
        hair_system(o, "ohr_innen", 1500 * FUR_K, 6, "d_innen", 0.0011, 0.05, 0.004, "haar_kopf", 32)
        comb(o, "ohr_aussen", field_o, jitter=0.25, lift0=30.0, lift1=10.0)
        comb(o, "ohr_innen", field_i, jitter=0.35, lift0=42.0, lift1=14.0, lenvar=0.3)
    return o


extras.append((make_ear(False), "kopf"))
extras.append((make_ear(True), "kopf"))


# ---- Rohrform entlang einer gebogenen Mittellinie: Krallen und Zaehne
def rohr(bm, uvl, p0, h, a0, a1, length, r0, flat, expo=0.75, nseg=14, nring=10):
    """Rohr ab p0 in Richtung h (Waagerechte), Bogen von a0 nach a1 Grad nach unten.
    Querschnitt oval: flat = Breite/Hoehe. uv.x = 0 an der Wurzel, 1 an der Spitze."""
    h = h.normalized()
    s = h.cross(Vector((0, 0, 1))).normalized()
    if s.length < 0.5:
        s = Vector((0, 1, 0))
    pos = Vector(p0)
    rings = []
    tips = []
    for i in range(nseg + 1):
        t = i / nseg
        an = math.radians(a0 + (a1 - a0) * t)
        d = h * math.cos(an) + Vector((0, 0, -1)) * math.sin(an)
        up = s.cross(d).normalized()
        rad = r0 * (1.0 - t) ** expo
        if i < nseg:
            ring = []
            for k in range(nring):
                ph = 2 * math.pi * k / nring
                ring.append(bm.verts.new(pos + s * rad * flat * math.cos(ph) + up * rad * math.sin(ph)))
            rings.append((ring, t))
        else:
            tip = bm.verts.new(pos)
            tips.append(tip)
        pos = pos + d * (length / nseg)
    faces = []
    for (ra, ta), (rc, tc_) in zip(rings, rings[1:]):
        for k in range(nring):
            k2 = (k + 1) % nring
            f = bm.faces.new((ra[k], ra[k2], rc[k2], rc[k]))
            faces.append((f, (ta, ta, tc_, tc_)))
    ra, ta = rings[-1]
    for k in range(nring):
        k2 = (k + 1) % nring
        f = bm.faces.new((ra[k], ra[k2], tips[0]))
        faces.append((f, (ta, ta, 1.0)))
    f = bm.faces.new(list(reversed(rings[0][0])))
    faces.append((f, (0.0,) * nring))
    if uvl is not None:
        for f, vals in faces:
            for lo, val in zip(f.loops, vals):
                lo[uvl].uv = (val, 0.0)
    return pos


def mesh_obj(name, bm, mats, smooth=True):
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    col.objects.link(o)
    for m_ in mats:
        me.materials.append(m_)
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return o


# ---- Zaehne im Maul: auf den Zahnfleischreihen, im geschlossenen Maul verborgen. Wie beim Baeren:
#      grosser Eckzahn, dahinter eine Luecke, kleine Vorbackenzaehne, hinten breite Backenzaehne.
def teeth():
    for jaw, lst, base_bone in (("oben", U2, "kopf"), ("unten", L2, "kiefer")):
        bm = bmesh.new()
        sgn = 1 if jaw == "oben" else -1
        down = 90.0 if sgn > 0 else -90.0

        def pos(u):
            k = min(int(u), len(lst) - 2)
            f = u - k
            xa, ya, za = HEAD.v[lst[k]]
            xb, yb, zb = HEAD.v[lst[k + 1]]
            return xa + (xb - xa) * f, ya + (yb - ya) * f, za + (zb - za) * f

        row = (
            (0.30, 0.034, 0.0105, 0.75, 0.40), (0.85, 0.034, 0.0105, 0.75, 0.40), (1.40, 0.032, 0.0095, 0.75, 0.40),
            (2.05, 0.027, 0.0058, 0.8, 0.55),
        )
        for u, ln, rd, fl, ex in row:
            x, y, z = pos(u)
            for s_ in (1, -1):
                rohr(bm, None, hw(x, s_ * y, z), Vector((1, 0, 0)), down, down, ln, rd, fl, expo=ex, nseg=5, nring=8)
        # Fangzaehne: kraeftig, leicht nach hinten gebogen; der untere steht vor dem oberen
        x, y, z = pos(2.75 if sgn > 0 else 3.15)
        a0, a1 = (74.0, 102.0) if sgn > 0 else (-74.0, -102.0)
        for s_ in (1, -1):
            rohr(bm, None, hw(x, s_ * (y - 0.009), z + sgn * 0.004), Vector((1, 0, 0)), a0, a1, 0.060 if sgn > 0 else 0.050, 0.0125, 0.80, expo=0.8, nseg=8, nring=8)
        # Schneidezaehne vorn, klein
        for u in (4.5, 5.0, 5.6):
            x, y, z = pos(u)
            for s_ in (1, -1):
                rohr(bm, None, hw(x, s_ * max(y, 0.006), z), Vector((1, 0, 0)), down, down, 0.018 if sgn > 0 else 0.016, 0.0056, 0.85, expo=0.5, nseg=4, nring=6)
        o = mesh_obj("zaehne_" + jaw, bm, [TOOTH])
        extras.append((o, base_bone))


teeth()
# Zunge: flacher Kaefig auf dem Maulboden
_z0 = hw(0.350, 0.0, -0.045)
_zo = sphere("zunge", tuple(_z0), 0.09, TONGUE, (1.30, 0.50, 0.21), seg=24)
_zo.rotation_euler = (0, math.radians(7.0), 0)
extras.append((_zo, "kiefer"))

# ==================================================================================================
# KRALLEN UND ZEHEN: fuenf Zehen im Bogen, jede mit Ballen im Netz und kurzem Fell, gebogene Hornkrallen
# ==================================================================================================
CLAWM = bpy.data.materials.new("horn")
CLAWM.use_nodes = True
Nc, Lc = CLAWM.node_tree.nodes, CLAWM.node_tree.links
_bc = Nc["Principled BSDF"]
_uv = Nc.new("ShaderNodeUVMap")
_uv.uv_map = "kralle"
_spc = Nc.new("ShaderNodeSeparateXYZ")
Lc.new(_uv.outputs[0], _spc.inputs[0])
_rc = Nc.new("ShaderNodeValToRGB")
_ec = _rc.color_ramp
_ec.elements[0].position = 0.10
_ec.elements[0].color = (0.020, 0.012, 0.007, 1)
_ec.elements[1].position = 0.98
_ec.elements[1].color = (0.52, 0.47, 0.38, 1)
_em = _ec.elements.new(0.58)
_em.color = (0.055, 0.036, 0.022, 1)
_em2 = _ec.elements.new(0.82)
_em2.color = (0.17, 0.135, 0.095, 1)
Lc.new(_spc.outputs[0], _rc.inputs["Fac"])
# feine Laengsriefen im Horn
_tcc = Nc.new("ShaderNodeTexCoord")
_mpc = Nc.new("ShaderNodeMapping")
_mpc.inputs["Scale"].default_value = (500, 900, 70)
Lc.new(_tcc.outputs["Object"], _mpc.inputs["Vector"])
_nzc = Nc.new("ShaderNodeTexNoise")
_nzc.inputs["Scale"].default_value = 1.0
_nzc.inputs["Detail"].default_value = 4
Lc.new(_mpc.outputs[0], _nzc.inputs["Vector"])
_cc = mix_rgba(Nc, Lc, maprange(Nc, Lc, _nzc.outputs["Fac"], 0.3, 0.7, 0.0, 0.32), _rc.outputs["Color"], (0.02, 0.014, 0.01))
Lc.new(_cc, _bc.inputs["Base Color"])
_bc.inputs["Roughness"].default_value = 0.5
_bc.inputs["Specular IOR Level"].default_value = 0.3
_bpc = Nc.new("ShaderNodeBump")
_bpc.inputs["Strength"].default_value = 0.35
_bpc.inputs["Distance"].default_value = 0.0012
Lc.new(_nzc.outputs["Fac"], _bpc.inputs["Height"])
Lc.new(_bpc.outputs["Normal"], _bc.inputs["Normal"])


def make_paw(name, bonename, px, cy, spread, zs, claw_l, claw_r, fur_len, sgn_side):
    """Fuenf Zehen und Krallen fuer eine Pfote. px: x der Zehenwurzel des Mittelzehs, cy: Pfotenmitte."""
    bm_t = bmesh.new()
    bm_c = bmesh.new()
    uv_c = bm_c.loops.layers.uv.new("kralle")
    Nr = 8
    # (t entlang des Zehs, halbe Breite, halbe Hoehe, Mittelhoehe)
    prof = [(-0.055, 0.0215, 0.034, 0.066), (-0.018, 0.0215, 0.037, 0.055), (0.015, 0.0215, 0.035, 0.047), (0.042, 0.0185, 0.028, 0.046), (0.059, 0.0145, 0.0195, 0.050), (0.068, 0.0075, 0.0095, 0.052)]
    pad_faces = []
    tips = []
    fwd = []
    for k in range(5):
        off = k - 2
        yaw = math.radians(off * 8.5)
        h = Vector((math.cos(yaw), math.sin(yaw), 0))
        sv = Vector((-h.y, h.x, 0))
        scale = zs * (1.0 - 0.04 * abs(off))
        base = Vector((px - 0.015 * off * off, cy + off * spread, 0.0))
        rings = []
        for t, w, hh, cz in prof:
            ring = []
            pc = base + h * (t * scale)
            for j in range(Nr):
                ph = 2 * math.pi * j / Nr
                sq = 1.0
                # Unterseite flacher, Ballen als Wulst
                zz = cz * scale + hh * scale * math.sin(ph)
                if math.sin(ph) < -0.3:
                    zz = max(zz, 0.012)
                ring.append(bm_t.verts.new(pc + sv * (w * scale * math.cos(ph)) + Vector((0, 0, zz))))
            rings.append(ring)
        for a_, c_ in zip(rings, rings[1:]):
            for j in range(Nr):
                j2 = (j + 1) % Nr
                f = bm_t.faces.new((a_[j], a_[j2], c_[j2], c_[j]))
                ph = 2 * math.pi * (j + 0.5) / Nr
                f.material_index = 1 if math.sin(ph) < -0.8 and rings.index(a_) >= 1 else 0
        cap = bm_t.faces.new(list(rings[-1]))
        cap.material_index = 0
        # Kralle: Wurzel oben im Zehenende, Bogen zum Boden, Spitze knapp ueber dem Boden
        t_root = prof[-2][0] * scale
        root = base + h * t_root + Vector((0, 0, (prof[-2][3] + 0.004) * scale))
        ln = claw_l * (1.0 - 0.10 * abs(off))
        # Bogenenden so waehlen, dass die Spitze bei z = 0.008 endet
        a0, a1 = 8.0, 72.0
        for _try in range(12):
            z = root.z
            for i in range(14):
                t = (i + 0.5) / 14
                z -= math.sin(math.radians(a0 + (a1 - a0) * t)) * ln / 14
            if z < 0.008:
                a1 -= 4.0
                a0 -= 1.0
            elif z > 0.022:
                a1 += 3.0
            else:
                break
        tip = rohr(bm_c, uv_c, root, h, a0, a1, ln, claw_r * (1.0 - 0.07 * abs(off)), 0.74, expo=0.78)
        tips.append(tip)
        fwd.append((base, h))
    o_t = mesh_obj(name + "_zehen", bm_t, [FURSKIN, PADM, HK])
    subsurf_apply(o_t, 2)
    me = o_t.data
    me.update()
    uvl = me.uv_layers.new(name="maske")
    for li, l in enumerate(me.loops):
        uvl.uv[li].vector = (0.58, 0.0)
    nv_ = len(me.vertices)
    gd = o_t.vertex_groups.new(name="d_zeh")
    gw = [0.0] * nv_
    mo_ = [set() for _ in range(nv_)]
    for p in me.polygons:
        for vi in p.vertices:
            mo_[vi].add(p.material_index)
    for i, v in enumerate(me.vertices):
        gw[i] = 1.0 if mo_[i] == {0} else 0.0
        gd.add([i], gw[i], "REPLACE")
    o_c = mesh_obj(name + "_krallen", bm_c, [CLAWM])
    extras.append((o_t, bonename))
    extras.append((o_c, bonename))
    if FUR > 0:
        kd = kdtree.KDTree(nv_)
        for i, v in enumerate(me.vertices):
            kd.insert(v.co, i)
        kd.balance()
        dirx = Vector((1, 0, 0))

        def field(root):
            i = kd.find(root)[1]
            nrm = me.vertices[i].normal.copy()
            t = dirx - nrm * dirx.dot(nrm)
            if t.length < 0.05:
                t = nrm.cross(Vector((0, 1, 0)))
            # Fell wird zur Kralle hin kuerzer
            front = max(tips, key=lambda q: -(q - root).length)
            ln = fur_len * smooth_(0.030, 0.085, (front - root).length) + 0.004
            return nrm, t.normalized(), ln

        hair_system(o_t, "zehfell", 3200 * FUR_K, 5, "d_zeh", 0.0013, 0.12, 0.002, "haar_kopf", 41)
        comb(o_t, "zehfell", field, jitter=0.25, lift0=28.0, lift1=8.0)


for s_, n_ in ((-1, "R"), (1, "L")):
    make_paw("vorn" + n_, "pranke" + n_, 0.600, s_ * 0.292, 0.046, 1.0, 0.088, 0.0138, 0.022, s_)
    make_paw("hinten" + n_, "fuss" + n_, -0.358, s_ * 0.322, 0.042, 0.88, 0.056, 0.0112, 0.020, s_)

bpy.context.view_layer.update()
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
bpy.ops.mesh.primitive_plane_add(size=90, location=(-16, 0, 20), rotation=(0, math.pi / 2, 0))
wald2 = bpy.context.active_object
wald2.name = "wald2"
wald2.data.materials.append(wbm)

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


def camera(name, offs, tgt_offs, lens=None, ortho=None, fstop=1.8, focus=None):
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
        cam.dof.focus_distance = focus if focus else d.length * 0.94
        cam.dof.aperture_fstop = fstop
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
if FUR <= 0:
    pass


def render_still(name, frame, cam, res, samples):
    scene.camera = cam
    scene.frame_set(frame)
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.cycles.samples = samples
    scene.render.filepath = OUT + name + ".png"
    bpy.ops.render.render(write_still=True)


F_STAND = KF["stand"]
SUN_NORMAL = so.rotation_euler.copy()
SUN_FRONT = Euler((math.radians(52), 0, math.radians(72)))   # nur fuer die Ansicht von vorn: sonst liegt die halbe Stirn im Schatten
FACE = Vector((1.26, 0, 1.02))         # Mitte des Gesichts in der Ruhelage


def face_cams():
    prof = camera("kopf_profil", (FACE.x - 0.06, -2.55, FACE.z + 0.02), (FACE.x - 0.06, 0, FACE.z + 0.02), lens=90, fstop=7.0)
    tq = camera("kopf_34", (FACE.x + 1.42, -1.24, FACE.z + 0.22), (FACE.x + 0.02, 0, FACE.z + 0.02), lens=92, fstop=8.0)
    fr = camera("kopf_front", (FACE.x + 2.30, -0.05, FACE.z + 0.24), (FACE.x, 0, FACE.z + 0.03), lens=100, fstop=9.0)
    paw = camera("pfote", (1.74, -0.80, 0.135), (0.64, -0.29, 0.052), lens=88, fstop=9.0)
    return prof, tq, fr, paw


def front_light(on):
    # Haar von vorn beleuchtet wirkt dunkel: fuer die Frontansicht Sonne nach vorn und etwas mehr Belichtung
    so.rotation_euler = SUN_FRONT if on else SUN_NORMAL
    scene.view_settings.exposure = 0.55 if on else 0.0


def hieb_cam():
    # Nahkamera aufs offene Maul: fragt die Pose des Kopfes im Hiebbild ab
    scene.frame_set(KF["hieb"])
    bpy.context.view_layer.update()
    t = ao.matrix_world @ pb["kopf"].tail
    ax = ao.location.x
    return camera("hieb_nah", (t.x - ax + 0.75, t.y - 1.75, t.z + 0.05), (t.x - ax - 0.10, t.y, t.z - 0.06), lens=78, fstop=8.0)


# Dichter niedriger Rasen nur fuer das Pfotenbild
bpy.ops.mesh.primitive_plane_add(size=5, location=(3.02, -0.3, 0.003))
rasen = bpy.context.active_object
rasen.name = "rasen"
rasen.data.materials.append(wm)
rasen.data.materials.append(gh)
rasen.modifiers.new("rasen", "PARTICLE_SYSTEM")
_sr = rasen.particle_systems[-1].settings
_sr.type = "HAIR"
_sr.use_advanced_hair = True
_sr.count = 60000
_sr.hair_step = 3
_sr.normal_factor = 0.0052
_sr.factor_random = 0.002
_sr.object_align_factor = (0.002, 0.001, 0)
_sr.child_type = "INTERPOLATED"
_sr.rendered_child_count = 6
_sr.child_length = 0.8
_sr.roughness_1 = 0.002
_sr.material_slot = "halm"
_sr.root_radius = 1.0
_sr.tip_radius = 0.02
_sr.radius_scale = 0.0012
rasen.hide_render = True


def low_grass(on):
    # Niedriges Gras, damit die Pfote frei steht (Laenge = 4 x normal_factor)
    sg.normal_factor = 0.0048 if on else 0.014
    rasen.hide_render = not on
    sg.factor_random = 0.002 if on else 0.007
    sg.object_align_factor = (0.002, 0.001, 0) if on else (0.006, 0.004, 0)
    sg.roughness_1 = 0.002 if on else 0.03
    sg.roughness_endpoint = 0.003 if on else 0.05
    sg.radius_scale = 0.0014 if on else 0.0028
    sg.rendered_child_count = 16 if on else 6


def clay_look():
    # Nur zur Formkontrolle: alle Haut in hellem Ton, Fell gibt es in diesem Modus nicht
    for m in (SKIN, FURSKIN, fur):
        nb_ = m.node_tree.nodes["Principled BSDF"]
        for l_ in list(nb_.inputs["Base Color"].links):
            m.node_tree.links.remove(l_)
        nb_.inputs["Base Color"].default_value = (0.42, 0.36, 0.30, 1)


if MODE == "clay":
    clay_look()
    scene.cycles.max_bounces = 4
    prof, tq, fr, paw = face_cams()
    low_grass(True)
    render_still("clay_profil" + TAG, F_STAND, prof, (640, 480), 24)
    render_still("clay_34" + TAG, F_STAND, tq, (640, 480), 24)
    render_still("clay_front" + TAG, F_STAND, fr, (640, 480), 24)
    render_still("clay_pfote" + TAG, F_STAND, paw, (640, 480), 24)
    render_still("clay_hieb" + TAG, KF["hieb"], CAM_SIDE, (800, 533), 24)
elif MODE == "kopf":
    scene.cycles.max_bounces = 6
    prof, tq, fr, paw = face_cams()
    low_grass(True)
    render_still("n_profil" + TAG, F_STAND, prof, (700, 525), 40)
    render_still("n_34" + TAG, F_STAND, tq, (700, 525), 40)
    front_light(True)
    render_still("n_front" + TAG, F_STAND, fr, (700, 525), 40)
    front_light(False)
    scene.view_settings.exposure = 0.45
    render_still("n_pfote" + TAG, F_STAND, paw, (700, 525), 40)
    scene.view_settings.exposure = 0.0
    render_still("n_hieb" + TAG, KF["hieb"], hieb_cam(), (700, 525), 40)
elif MODE == "probe":
    scene.cycles.max_bounces = 8
    prof, tq, fr, paw = face_cams()
    render_still("p_34" + TAG, F_STAND, tq, (1000, 750), 100)
    render_still("p_profil" + TAG, F_STAND, prof, (1000, 750), 100)
    front_light(True)
    render_still("p_front" + TAG, F_STAND, fr, (1000, 750), 100)
    front_light(False)
    render_still("p_hieb" + TAG, KF["hieb"], hieb_cam(), (1000, 750), 100)
    low_grass(True)
    render_still("p_pfote" + TAG, F_STAND, paw, (1000, 750), 100)
    low_grass(False)
    render_still("p_ganz" + TAG, 22, CAM_SIDE, (1200, 800), 100)
elif MODE == "ende":
    scene.cycles.max_bounces = 8
    prof, tq, fr, paw = face_cams()
    low_grass(True)
    scene.view_settings.exposure = 0.45
    render_still("pfote", F_STAND, paw, (1200, 900), 200)
    scene.view_settings.exposure = 0.0
    low_grass(False)
    render_still("kopf_profil", F_STAND, prof, (1200, 900), 200)
    render_still("kopf_34", F_STAND, tq, (1200, 900), 200)
    front_light(True)
    render_still("kopf_front", F_STAND, fr, (1200, 900), 200)
    front_light(False)
    render_still("ganz", 22, CAM_SIDE, (1500, 1000), 200)
    render_still("hieb", KF["hieb"], CAM_SIDE, (1500, 1000), 200)
    render_still("hieb_nah", KF["hieb"], hieb_cam(), (1200, 900), 200)
elif MODE == "still":
    scene.cycles.max_bounces = 8
    render_still("v3_gehen", 22, CAM_SIDE, (1500, 1000), 200)
    render_still("v3_hoch", KF["aus"], CAM_SIDE, (1500, 1000), 200)
    render_still("v3_hieb", KF["hieb"], CAM_SIDE, (1500, 1000), 200)
else:
    bpy.ops.wm.save_as_mainfile(filepath=OUT + "baer.blend")
    if TAG == "kurz":
        # Probelauf: nur drei Bilder rund um den Hieb statt der ganzen Folge
        scene.frame_start, scene.frame_end = KF["aus"], KF["aus"] + 14
        scene.frame_step = 7
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
