import bpy, math, os, sys
from mathutils import Vector
MOD = r"C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/"
OUT = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/pruef/"
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
n=0
for d in prefs.devices:
    d.use = d.type == "OPTIX"
    n += d.use
print("OPTIX Geraete", n)
scene.cycles.device = "GPU"
scene.cycles.samples = 24
scene.cycles.use_denoising = False
bpy.ops.import_scene.fbx(filepath=MOD + "models_X/WorldItems/NCBear.fbx")
ob = [o for o in bpy.context.selected_objects if o.type == "MESH"][0]
me = ob.data
img = bpy.data.images.load(MOD + "textures/WorldItems/NCBear.png")
img.colorspace_settings.name = "Non-Color"
em = bpy.data.materials.new("wie_spiel")
em.use_nodes = True
nt = em.node_tree
nt.nodes.remove(nt.nodes["Principled BSDF"])
tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = img
ge = nt.nodes.new("ShaderNodeNewGeometry")
dp = nt.nodes.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"
lv = Vector((0.0, 2.0, 5.0)).normalized(); dp.inputs[1].default_value = (lv.x, lv.y, lv.z)
nt.links.new(ge.outputs["Normal"], dp.inputs[0])
cl = nt.nodes.new("ShaderNodeMapRange"); cl.clamp = True
cl.inputs["From Min"].default_value = 0.0; cl.inputs["From Max"].default_value = 1.0
cl.inputs["To Min"].default_value = 0.4; cl.inputs["To Max"].default_value = 0.775
nt.links.new(dp.outputs["Value"], cl.inputs["Value"])
mu = nt.nodes.new("ShaderNodeVectorMath"); mu.operation = "SCALE"
nt.links.new(tx.outputs["Color"], mu.inputs[0]); nt.links.new(cl.outputs[0], mu.inputs["Scale"])
ee = nt.nodes.new("ShaderNodeEmission"); nt.links.new(mu.outputs[0], ee.inputs["Color"])
nt.links.new(ee.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
me.materials.clear(); me.materials.append(em)
scene.view_settings.view_transform = "Raw"
w = bpy.data.worlds.new("w"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.20, 0.235, 0.14, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
scene.world = w
cam = bpy.data.cameras.new("c"); cam.type = "ORTHO"; cam.ortho_scale = 3.0
co = bpy.data.objects.new("c", cam); scene.collection.objects.link(co); scene.camera = co
# Blick wie im Spiel: 30 Grad von oben, feste Richtung; der Baer dreht sich
el = math.radians(30)
d = 12.0
pos = Vector((d*math.cos(el)*0.7071, -d*math.cos(el)*0.7071, d*math.sin(el)))
ziel = Vector((0.1, 0, 0.5))
co.location = pos + ziel
co.rotation_mode = "QUATERNION"
co.rotation_quaternion = (ziel - co.location).to_track_quat("-Z", "Y")
scene.render.image_settings.file_format = "PNG"; scene.render.image_settings.color_mode = "RGB"
scene.render.resolution_x = scene.render.resolution_y = 600
for i in range(8):
    ob.rotation_euler = (0, 0, math.radians(45*i))
    scene.render.filepath = OUT + "acht_%d.png" % (45*i)
    bpy.ops.render.render(write_still=True)
# Spielgroesse: 1 m = 73.9 Pixel
cam.ortho_scale = 3.0 * 73.9 / 73.9
scene.render.resolution_x = scene.render.resolution_y = int(3.0 * 73.9)
for i in (0, 2, 4, 6):
    ob.rotation_euler = (0, 0, math.radians(45*i))
    scene.render.filepath = OUT + "klein_%d.png" % (45*i)
    bpy.ops.render.render(write_still=True)
# Kopf nah von beiden Seiten
ob.rotation_euler = (0, 0, 0)
scene.render.resolution_x = scene.render.resolution_y = 700
cam.ortho_scale = 0.95
for name, p in (("kopf_rechts", (1.6, -1.7, 1.0)), ("kopf_links", (1.6, 1.7, 1.0)), ("kopf_vorn", (3.0, 0, 0.9)), ("ruecken", (-2.5, -0.8, 2.2))):
    z = Vector((0.82, 0, 0.6)) if name != "ruecken" else Vector((-0.1, 0, 0.6))
    if name == "ruecken": cam.ortho_scale = 2.6
    co.location = p
    co.rotation_quaternion = (z - Vector(p)).to_track_quat("-Z", "Y")
    scene.render.filepath = OUT + name + ".png"
    bpy.ops.render.render(write_still=True)
print("FERTIG")
