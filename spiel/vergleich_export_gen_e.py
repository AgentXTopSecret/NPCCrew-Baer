# Blender headless: grosser Generator-Baer (E_schoen*.glb) als Standmodell fuer die Test-Mod (Vergleich mit dem 2c-Baeren).
# Aufruf: blender --background --factory-startup --python export_gen_e.py -- <glb> <fbx_ziel> <laenge_m>
# Gleiche Konvention wie das 2c-Standmodell (baer/spiel/baer_export_2c.py:3065): Meter, x vorn, z oben, Boden z=0,
# FBX axis_forward -Z, axis_up Y, FBX_SCALE_ALL; im Skript scale = 0.544.
import bpy, sys, math
import numpy as np

args = sys.argv[sys.argv.index("--") + 1:]
glb, ziel, laenge = args[0], args[1], float(args[2])

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
obs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
assert len(obs) == 1, [o.name for o in obs]
ob = obs[0]
bpy.ops.object.select_all(action="DESELECT")
ob.select_set(True)
bpy.context.view_layer.objects.active = ob
# Eltern loesen und alles in die Ecken backen
bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
me = ob.data
V = np.array([v.co[:] for v in me.vertices])
print("ROH min", V.min(0), "max", V.max(0))
# E: vorn = Blender -Y (C_FEIN/E_FEIN) -> um +90 Grad um Z drehen, dann vorn = +X wie beim 2c-Modell
R = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
V = V @ R.T
L = V[:, 0].max() - V[:, 0].min()
s = laenge / L
V = V * s
V[:, 0] -= (V[:, 0].max() + V[:, 0].min()) / 2
V[:, 1] -= (V[:, 1].max() + V[:, 1].min()) / 2
V[:, 2] -= V[:, 2].min()
for i, v in enumerate(me.vertices):
    v.co = V[i]
me.update()
for p in me.polygons:
    p.use_smooth = True
print("MASSE Meter: Laenge %.3f Breite %.3f Hoehe %.3f; Dreiecke %d" % (
    V[:, 0].max() - V[:, 0].min(), V[:, 1].max() - V[:, 1].min(), V[:, 2].max(),
    sum(len(p.vertices) - 2 for p in me.polygons)))
bpy.ops.export_scene.fbx(filepath=ziel, use_selection=True, apply_unit_scale=True,
                         apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_anim=False,
                         mesh_smooth_type="FACE", use_mesh_modifiers=True, add_leaf_bones=False, path_mode="STRIP")
print("EXPORT_OK", ziel)
