# Macht aus dem Hochmodell (Entwurf C, baer_quelle.py) ein Spielmodell: ein Netz, eine gebackene Textur, FBX.
# Aufruf: blender --background --factory-startup --python baer_export.py -- STUFE
#   probe      eine schnelle Ansicht der Ruhehaltung ohne Fell und Masse ausgeben
#   ansichten  Hochmodell MIT Fell aus vielen Richtungen rendern (Grundlage der Textur)
#   netz       Fellhuelle aus den Silhouetten schaelen, verringern, abwickeln -> lowpoly.blend
#   backen     Ansichten auf die Abwicklung projizieren -> Textur, FBX, Icon
#   vorschau   die zwei Vorschaubilder mit dem fertigen Spielmodell
import json
import math
import os
import sys
import time

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

SP = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_spiel/"
HIER = r"C:/Users/Kevin/NPCCrew-Nebenprojekte/baer/spiel/"
MOD = r"C:/Users/Kevin/Zomboid/mods/NCBearTest/42/media/"
QUELLE = HIER + "baer_quelle.py"
MARKE = "# ------------------------------------------------------------------ Boden und Licht wie ein Tag im Spiel"
ANS = SP + "ansichten/"
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["probe"]
STUFE = ARGS[0]
T0 = time.time()


def log(*a):
    print("EXPORT %.1fs" % (time.time() - T0), *a, flush=True)


def quelle(modus):
    """Fuehrt das Hochmodell-Skript bis vor Boden und Licht aus: Ruhehaltung, alle Teile, kein Gang."""
    src = open(QUELLE, encoding="utf-8").read()
    assert src.count(MARKE) == 1
    alt = sys.argv
    sys.argv = [alt[0], "--", modus]
    Q = {"__name__": "baer_quelle", "__file__": QUELLE}
    exec(compile(src.split(MARKE)[0], QUELLE, "exec"), Q)
    sys.argv = alt
    return Q


def gpu(scene, samples, denoise=True):
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    used = []
    for d in prefs.devices:
        d.use = d.type == "OPTIX"
        if d.use:
            used.append(d.name)
    log("Geraete", used)
    scene.cycles.device = "GPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = denoise
    if denoise:
        scene.cycles.denoiser = "OPTIX"
        scene.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.max_bounces = 8
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"


def neutrale_welt(scene, oben=1.05, unten=0.72):
    """Graues Licht von allen Seiten, oben etwas mehr: keine Sonne, kein Klecks, keine Fremdfarbe."""
    w = bpy.data.worlds.new("backlicht")
    w.use_nodes = True
    nt = w.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sp = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.clamp = True
    mr.inputs["From Min"].default_value = -1.0
    mr.inputs["From Max"].default_value = 1.0
    mr.inputs["To Min"].default_value = unten
    mr.inputs["To Max"].default_value = oben
    nt.links.new(tc.outputs["Generated"], sp.inputs[0])
    nt.links.new(sp.outputs[2], mr.inputs["Value"])
    nt.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    nt.links.new(mr.outputs[0], nt.nodes["Background"].inputs[1])
    scene.world = w
    return w


# ------------------------------------------------------------------ Kameras
def kamera_daten():
    """Alle Blickrichtungen. Grob: ganzer Baer. Fein: nur der Kopf."""
    C_B = np.array((0.14, 0.0, 0.80))
    views = []
    def add(name, c, az, el, ortho, res):
        a, e = math.radians(az), math.radians(el)
        d = np.array((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
        views.append(dict(name=name, c=[float(x) for x in c], d=[float(x) for x in d], ortho=ortho, res=res))
    for az in range(0, 360, 45):
        add("k_h%03d" % az, C_B, az, 0, 3.5, 2048)
    for az in range(0, 360, 60):
        add("k_o%03d" % az, C_B, az, 42, 3.5, 2048)
    add("k_top", C_B, 0.0, 89.5, 3.5, 2048)
    for az in range(30, 390, 60):
        add("k_u%03d" % az, C_B, az, -38, 3.5, 2048)
    add("k_bot", C_B, 0.0, -89.5, 3.5, 2048)
    return views


def kopf_kameras(Q):
    c = np.array(Q["l2w"]((0.20, 0.0, -0.02)))
    views = []
    def add(name, az, el):
        a, e = math.radians(az), math.radians(el)
        d = np.array((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
        views.append(dict(name=name, c=[float(x) for x in c], d=[float(x) for x in d], ortho=0.92, res=1536))
    for az, el in ((0, 4), (30, 2), (-30, 2), (62, 2), (-62, 2), (95, 2), (-95, 2), (0, 42), (55, 38), (-55, 38), (118, 30), (-118, 30), (0, -32), (48, -30), (-48, -30)):
        add("h_a%+04d_e%+03d" % (az, el), az, el)
    return views


def kamera_setzen(scene, v):
    cam = bpy.data.cameras.new(v["name"])
    cam.type = "ORTHO"
    cam.ortho_scale = v["ortho"]
    cam.clip_start = 0.1
    cam.clip_end = 40.0
    co = bpy.data.objects.new(v["name"], cam)
    scene.collection.objects.link(co)
    c, d = Vector(v["c"]), Vector(v["d"])
    co.location = c + d * 12.0
    co.rotation_mode = "QUATERNION"
    co.rotation_quaternion = (-d).to_track_quat("-Z", "Y")
    scene.camera = co
    scene.render.resolution_x = v["res"]
    scene.render.resolution_y = v["res"]
    bpy.context.view_layer.update()
    return co


def stufe_probe():
    Q = quelle("form")
    scene = bpy.context.scene
    body, kopf = bpy.data.objects["baer_koerper"], bpy.data.objects["kopf"]
    for ob in (body, kopf):
        vs = np.array([ob.matrix_world @ v.co for v in ob.data.vertices])
        log("MASS", ob.name, "min", vs.min(0).round(3), "max", vs.max(0).round(3), "Punkte", len(vs))
    gpu(scene, 24)
    neutrale_welt(scene)
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    v = dict(name="p", c=[0.14, 0, 0.8], d=[0.0, -1.0, 0.04], ortho=3.5, res=900)
    v["d"] = [0.0, -0.999, 0.04]
    kamera_setzen(scene, v)
    scene.render.filepath = SP + "probe/form_seite.png"
    bpy.ops.render.render(write_still=True)
    log("PROBE_OK")


def stufe_ansichten():
    nur = ARGS[1] if len(ARGS) > 1 else None
    Q = quelle("spiel")
    log("Hochmodell steht")
    scene = bpy.context.scene
    gpu(scene, 96, True)
    neutrale_welt(scene)
    scene.render.film_transparent = True
    scene.render.use_persistent_data = True
    im = scene.render.image_settings
    im.file_format = "OPEN_EXR"
    im.color_mode = "RGBA"
    im.color_depth = "32"
    im.exr_codec = "ZIP"
    views = kamera_daten() + kopf_kameras(Q)
    json.dump(views, open(ANS + "kameras.json", "w"), indent=1)
    for v in views:
        if nur and not v["name"].startswith(nur):
            continue
        out = ANS + v["name"] + ".exr"
        if os.path.exists(out):
            continue
        kamera_setzen(scene, v)
        scene.render.filepath = out
        t = time.time()
        bpy.ops.render.render(write_still=True)
        log("ANSICHT", v["name"], "%.1fs" % (time.time() - t))
    log("ANSICHTEN_OK")


# ------------------------------------------------------------------ Bild lesen
def lade_exr(pfad):
    img = bpy.data.images.load(pfad)
    img.colorspace_settings.name = "Non-Color"
    w, h = img.size
    a = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(a)
    bpy.data.images.remove(img)
    return a.reshape(h, w, 4)


class Ansicht:
    """Rechnet Weltpunkte in Pixel einer gerenderten Ansicht. Zeile 0 ist unten, wie in Blender."""

    def __init__(self, v):
        self.v = v
        self.name = v["name"]
        self.res = v["res"]
        self.ortho = v["ortho"]
        c = np.array(v["c"])
        d = np.array(v["d"])
        self.c, self.d = c, d
        co = Vector(v["c"]) + Vector(v["d"]) * 12.0
        q = (-Vector(v["d"])).to_track_quat("-Z", "Y")
        M = q.to_matrix()
        self.x = np.array(M.col[0])
        self.y = np.array(M.col[1])
        self.z = np.array(M.col[2])
        self.co = np.array(co)
        self.s = self.res / self.ortho

    def pix(self, P):
        R = P - self.co
        u = (R @ self.x) * self.s + self.res * 0.5
        v = (R @ self.y) * self.s + self.res * 0.5
        tiefe = -(R @ self.z)
        return u, v, tiefe


def bilinear(img, u, v):
    """Bilinear in Pixelzentren; ausserhalb -> klemmt, Rueckgabe zusaetzlich Maske."""
    h, w = img.shape[:2]
    x = u - 0.5
    y = v - 0.5
    inn = (x >= 0) & (y >= 0) & (x < w - 1) & (y < h - 1)
    x0 = np.clip(np.floor(x).astype(np.int64), 0, w - 2)
    y0 = np.clip(np.floor(y).astype(np.int64), 0, h - 2)
    fx = np.clip(x - x0, 0.0, 1.0)
    fy = np.clip(y - y0, 0.0, 1.0)
    if img.ndim == 3:
        fx = fx[:, None]
        fy = fy[:, None]
    a = img[y0, x0] * (1 - fx) + img[y0, x0 + 1] * fx
    b = img[y0 + 1, x0] * (1 - fx) + img[y0 + 1, x0 + 1] * fx
    return a * (1 - fy) + b * fy, inn


# ------------------------------------------------------------------ Hilfen am Netz (numpy)
def netz_arrays(me):
    n = len(me.vertices)
    V = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("co", V)
    V = V.reshape(n, 3)
    me.calc_loop_triangles()
    m = len(me.loop_triangles)
    T = np.empty(m * 3, dtype=np.int64)
    me.loop_triangles.foreach_get("vertices", T)
    return V, T.reshape(m, 3)


def v_normalen(V, T):
    n = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    N = np.zeros_like(V)
    for i in range(3):
        for ax in range(3):
            N[:, ax] += np.bincount(T[:, i], weights=n[:, ax], minlength=len(V))
    return N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)


def kanten(T):
    E = np.concatenate((T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]), 0)
    E.sort(axis=1)
    return np.unique(E, axis=0)


def glatt_feld(F, E, n_v, runden, faktor=0.5):
    """Mittelung ueber die Kanten fuer ein Skalar- oder Vektorfeld."""
    F = F.copy()
    for _ in range(runden):
        cnt = np.bincount(E[:, 0], minlength=n_v) + np.bincount(E[:, 1], minlength=n_v)
        if F.ndim == 1:
            S = np.bincount(E[:, 0], weights=F[E[:, 1]], minlength=n_v) + np.bincount(E[:, 1], weights=F[E[:, 0]], minlength=n_v)
            F = F + (S / np.maximum(cnt, 1) - F) * faktor
        else:
            for ax in range(F.shape[1]):
                S = np.bincount(E[:, 0], weights=F[E[:, 1], ax], minlength=n_v) + np.bincount(E[:, 1], weights=F[E[:, 0], ax], minlength=n_v)
                F[:, ax] += (S / np.maximum(cnt, 1) - F[:, ax]) * faktor
    return F


# ------------------------------------------------------------------ Stufe netz: Fellhuelle
def neues_netz(name, V, F):
    me = bpy.data.meshes.new(name)
    me.from_pydata(np.asarray(V, dtype=float).tolist(), [], np.asarray(F).tolist() if hasattr(F, "tolist") else F)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    return o


def welt_netz(ob):
    me = ob.data
    n = len(me.vertices)
    V = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("co", V)
    V = V.reshape(n, 3)
    M = np.array(ob.matrix_world)
    V = V @ M[:3, :3].T + M[:3, 3]
    F = [tuple(p.vertices) for p in me.polygons]
    return V, F


def alpha_laden(views, schritt=2):
    A = []
    for v in views:
        rgba = lade_exr(ANS + v["name"] + ".exr")
        a = rgba[..., 3]
        h = a.shape[0] // schritt * schritt
        a = a[:h, :h].reshape(h // schritt, schritt, h // schritt, schritt).mean(axis=(1, 3))
        A.append(a.astype(np.float32))
    return A


def huelle_schaelen(V, N, dlim, views, alpha, schritt=2, dmax=0.15, stufen=16, schwelle=0.5):
    """Geht von der Haut nach aussen, solange der Punkt in JEDER Ansicht im Fell liegt und unter der Grenze bleibt."""
    D = np.linspace(0.0, dmax, stufen)
    d = np.zeros(len(V))
    lebt = np.ones(len(V), dtype=bool)
    objs = [Ansicht(v) for v in views]
    for k in range(1, stufen):
        idx = np.nonzero(lebt)[0]
        if not len(idx):
            break
        P = V[idx] + N[idx] * D[k]
        ok = D[k] <= dlim[idx]
        for av, a in zip(objs, alpha):
            u, v, _ = av.pix(P)
            r = a.shape[0]
            iu = np.floor(u / schritt).astype(np.int64)
            iv = np.floor(v / schritt).astype(np.int64)
            inn = (iu >= 0) & (iv >= 0) & (iu < r) & (iv < r)
            drin = np.zeros(len(idx), dtype=bool)
            drin[inn] = a[iv[inn], iu[inn]] >= schwelle
            if av.name.startswith("h_"):
                # Kopfansichten sehen nur den Kopf: ausserhalb des Bildes sagen sie nichts
                ok &= drin | ~inn
            else:
                ok &= drin
        lebt[idx] = ok
        d[idx[ok]] = D[k]
    return d


def _zotteln(s, q, y, ph0):
    r = np.zeros(len(s))
    for fs, fq, fy, ph, gew in ((6.3, 25.0, 21.0, 0.3, 1.0), (10.7, 39.0, 33.0, 2.1, 0.72), (3.9, 14.5, 13.0, 4.4, 0.85)):
        wn = np.sin(q * fq + 1.9 * np.sin(s * fs * 0.6 + ph + ph0)) * np.sin(y * fy + 1.5 * np.sin(s * fs * 0.8 + ph * 2.0) + ph + ph0)
        r = np.maximum(r, np.maximum(wn, 0.0) ** 1.4 * gew)
    return np.clip(r, 0.0, 1.0)


def buschel_rauschen(P, bein):
    """Spitze, in Strichrichtung gestreckte Zotteln, 0..1. Rumpf: nach hinten und unten. Bein: nach unten, sonst entstehen Ringe."""
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    rumpf = _zotteln(x * 0.86 + z * 0.51, -x * 0.51 + z * 0.86, y, 0.0)
    r_bein = _zotteln(z * 0.55, x * 0.8, y * 0.8, 1.3)
    return rumpf * (1.0 - bein) + r_bein * bein


def stufe_netz():
    Q = quelle("form")
    sst = Q["sst"]
    # 1. Teile sammeln: Koerper, Kopfhuelle OHNE Mund, Nase, Zehen
    KV, KQ = Q["netz_aus_feld"](Q["huelle_basis"], (-0.42, -0.27, -0.28), (0.535, 0.27, 0.235), 0.0040, grob=4)
    KV = Q["glaette"](KV, KQ, 0.35, 2)
    VS, FS = [], []
    off = 0

    def dazu(V_, F_):
        nonlocal off
        VS.append(np.asarray(V_))
        FS.extend([tuple(int(i) + off for i in f) for f in F_])
        off += len(V_)

    dazu(Q["l2w"](KV), np.asarray(KQ).tolist())
    teile = [bpy.data.objects["baer_koerper"], bpy.data.objects["nase"]] + [o for o in bpy.data.objects if o.name.startswith("zehen_")]
    for ob in teile:
        V_, F_ = welt_netz(ob)
        dazu(V_, F_)
    roh = neues_netz("roh", np.concatenate(VS, 0), FS)
    log("Rohteile", len(roh.data.vertices), "Punkte")
    # 2. Alles zu einer geschlossenen Haut
    rm = roh.modifiers.new("r", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = 0.0085
    rm.adaptivity = 0.0
    bpy.context.view_layer.objects.active = roh
    roh.select_set(True)
    bpy.ops.object.modifier_apply(modifier=rm.name)
    V, T = netz_arrays(roh.data)
    E = kanten(T)
    log("Voxelhaut", len(V), "Punkte", len(T), "Dreiecke", "min", V.min(0).round(3), "max", V.max(0).round(3))
    N = v_normalen(V, T)
    N = glatt_feld(N, E, len(V), 8, 0.6)
    N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)

    # 3. Grenze je Punkt: so weit darf die Huelle ueber die Haut. Am Gesicht fast nichts, Hoehlen bleiben Hoehlen
    L3 = Q["w2l"](V)
    a, b, c = L3[:, 0], L3[:, 1], L3[:, 2]
    hb = Q["huelle_basis"](a, b, c)
    L_, m_, r_, R_ = Q["haar_werte"](a, b, c)
    koerper_bein = 1.0 - sst(0.20, 0.50, V[:, 2])
    dlim_k = 0.112 - 0.022 * koerper_bein
    ze = Q["zehen_abstand"](V)
    dlim_k = np.minimum(dlim_k, 0.012 + 1.05 * np.maximum(ze, 0.0))
    kopf_g = 1.0 - sst(0.006, 0.17, hb)
    # Stummelschwanz: sonst liegt dort eine Kugel aus Fell
    dlim_k = np.minimum(dlim_k, 0.112 - 0.082 * sst(0.96, 1.08, -V[:, 0]))
    dlim_h = L_ * Q["KOPF_SK"] * 0.60 + 0.0015
    dlim = dlim_k + (dlim_h - dlim_k) * kopf_g

    # 4. Aus den Silhouetten schaelen
    views = json.load(open(ANS + "kameras.json"))
    t0 = time.time()
    alpha = alpha_laden(views)
    log("Alpha geladen", "%.1fs" % (time.time() - t0))
    d = huelle_schaelen(V, N, dlim, views, alpha)
    del alpha
    log("Schaelen fertig; d im Mittel %.3f, max %.3f" % (d.mean(), d.max()))
    d = glatt_feld(d, E, len(V), 4, 0.5)

    # 5. Zotteln: Rumpf, Nacken, Beine bekommen unregelmaessige Umrisskanten; Gesicht und Pfote nicht
    bein = 1.0 - sst(0.42, 0.62, V[:, 2])
    zott = buschel_rauschen(V, bein)
    gesicht = 1.0 - sst(0.0, 0.11, hb)
    pfote = 1.0 - sst(0.015, 0.09, ze)
    # Nicht ueberall gleich stark: grosse Flaechen mal zottiger, mal glatter
    grob = 0.5 + 0.5 * np.sin(V[:, 0] * 3.1 + 1.0) * np.sin(V[:, 1] * 4.3 + 0.4) * np.sin(V[:, 2] * 3.7 + 2.0)
    amp = (0.036 + 0.030 * grob) * (1.0 - gesicht) * (1.0 - pfote) * (1.0 - 0.25 * bein)
    d = d - amp * 0.42 + amp * zott
    d = np.maximum(d, 0.0015)
    W = V + N * d[:, None]
    W[:, 2] = np.maximum(W[:, 2], 0.004)  # Nie unter den Boden: die Sohle ist flach
    roh.data.vertices.foreach_set("co", W.ravel())
    roh.data.update()
    # Zweite Voxelrunde: schliesst schmale Falten und Selbstdurchdringungen der aufgeblasenen Huelle (sonst dunkle Risse)
    rm2 = roh.modifiers.new("r2", "REMESH")
    rm2.mode = "VOXEL"
    rm2.voxel_size = 0.0115
    rm2.adaptivity = 0.0
    bpy.ops.object.modifier_apply(modifier=rm2.name)
    W, T = netz_arrays(roh.data)
    W[:, 2] = np.maximum(W[:, 2], 0.004)
    roh.data.vertices.foreach_set("co", W.ravel())
    roh.data.update()
    roh.data.shade_smooth()
    log("Huelle nach zweiter Voxelrunde", len(W), "Punkte", len(T), "Dreiecke")

    # 6. Verringern. Die Fehlerquadrik misst Abstaende: wird eine Gegend vorher aufgeblasen, zaehlt dort jeder Fehler mehr
    # und es bleiben mehr Dreiecke stehen. Das Aufblasen ist eine umkehrbare radiale Abbildung, hinterher wieder heraus.
    ziel = int(float(ARGS[1])) if len(ARGS) > 1 else 13400
    kopf_anteil = 0.34
    mitte_kopf = np.array(Q["l2w"]((0.16, 0.0, 0.0)))
    pfoten = [np.array((xc - 0.05, yc, 0.07)) for _bn, _s, xc, yc, _g, _v, _q, _f in Q["ZEH_NETZE"]]

    def radial(R1, R2, s):
        r = np.linspace(0.0, 8.0, 8001)
        steig = 1.0 + (s - 1.0) * (1.0 - sst(R1, R2, r))
        rn = np.concatenate(([0.0], np.cumsum((steig[1:] + steig[:-1]) * 0.5 * np.diff(r))))
        return r, rn

    def abbilden(P_, s_kopf, zurueck=False):
        schritte = [(mitte_kopf, radial(0.42, 0.72, s_kopf))] + [(c_, radial(0.15, 0.30, 1.0 + (s_kopf - 1.0) * 0.45)) for c_ in pfoten]
        if zurueck:
            schritte = schritte[::-1]
        for c_, (r_, rn_) in schritte:
            D_ = P_ - c_
            ln = np.maximum(np.linalg.norm(D_, axis=1), 1e-9)
            neu_ = np.interp(ln, rn_, r_) if zurueck else np.interp(ln, r_, rn_)
            P_ = c_ + D_ * (neu_ / ln)[:, None]
        return P_

    def versuch(s_kopf):
        roh.data.vertices.foreach_set("co", abbilden(W, s_kopf).ravel())
        roh.data.update()
        dm = roh.modifiers.new("wenig", "DECIMATE")
        dm.decimate_type = "COLLAPSE"
        dm.ratio = ziel / len(T)
        dm.use_collapse_triangulate = True
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(roh.evaluated_get(dg))
        roh.modifiers.remove(dm)
        W2_, T2_ = netz_arrays(me)
        W2_ = abbilden(W2_, s_kopf, True)
        me.vertices.foreach_set("co", W2_.ravel())
        me.update()
        cen = W2_[T2_].mean(1)
        l2 = Q["w2l"](cen)
        hb2 = Q["huelle_basis"](l2[:, 0], l2[:, 1], l2[:, 2])
        return me, float((hb2 < 0.075).mean()), len(T2_)

    lo, hi = 1.0, 6.0
    best = None
    for it in range(7):
        f = 0.5 * (lo + hi)
        me, ant, n = versuch(f)
        log("Decimate Aufblasen %.3f -> Dreiecke %d, Kopfanteil %.3f" % (f, n, ant))
        best = me
        if abs(ant - kopf_anteil) < 0.015:
            break
        if ant < kopf_anteil:
            lo = f
        else:
            hi = f

    # 7. Krallen als kleine eigene Teile im selben Netz
    W2, T2 = netz_arrays(best)
    VS2, FS2 = [W2], [tuple(t_) for t_ in T2.tolist()]
    off2 = len(W2)
    n_haupt = len(W2)
    for ob in [o for o in bpy.data.objects if o.name.startswith("krallen_")]:
        dm = ob.modifiers.new("w", "DECIMATE")
        dm.ratio = 0.05
        dg = bpy.context.evaluated_depsgraph_get()
        me2 = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        ob.modifiers.remove(dm)
        Vk, Tk = netz_arrays(me2)
        Mw = np.array(ob.matrix_world)
        Vk = Vk @ Mw[:3, :3].T + Mw[:3, 3]
        FS2.extend([tuple(int(i) + off2 for i in t_) for t_ in Tk.tolist()])
        VS2.append(Vk)
        off2 += len(Vk)
    Vend = np.concatenate(VS2, 0)
    # Aufraeumen: einzelne Splitter weg, jede Schale nach aussen gedreht (das Spiel zeichnet nur Vorderseiten, Volumen muss positiv sein)
    Tall = np.array(FS2, dtype=np.int64)
    eltern_s = np.arange(len(Vend))

    def wurz_s(i):
        while eltern_s[i] != i:
            eltern_s[i] = eltern_s[eltern_s[i]]
            i = eltern_s[i]
        return i

    for t_ in Tall:
        a_ = wurz_s(t_[0])
        eltern_s[wurz_s(t_[1])] = a_
        eltern_s[wurz_s(t_[2])] = a_
    tw = np.array([wurz_s(int(i)) for i in Tall[:, 0]])
    behalten = np.zeros(len(Tall), dtype=bool)
    gedreht = 0
    splitter = 0
    for r_ in np.unique(tw):
        sel = np.nonzero(tw == r_)[0]
        if len(sel) < 12:
            splitter += 1
            continue
        behalten[sel] = True
        tt = Tall[sel]
        c_ = Vend[tt].reshape(-1, 3).mean(0)
        vol = np.einsum("ij,ij->i", Vend[tt[:, 0]] - c_, np.cross(Vend[tt[:, 1]] - c_, Vend[tt[:, 2]] - c_)).sum()
        if vol < 0:
            Tall[sel] = tt[:, ::-1]
            gedreht += 1
    Tall = Tall[behalten]
    benutzt = np.unique(Tall)
    neu_idx = np.full(len(Vend), -1, dtype=np.int64)
    neu_idx[benutzt] = np.arange(len(benutzt))
    n_haupt = int((benutzt < n_haupt).sum())
    Vend = Vend[benutzt]
    FS2 = [tuple(x) for x in neu_idx[Tall].tolist()]
    log("Aufgeraeumt: Splitter", splitter, "gedrehte Schalen", gedreht)
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    ob = neues_netz("NCBear", Vend, FS2)
    ob.data.shade_smooth()
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    V3, T3 = netz_arrays(ob.data)
    log("Spielnetz", len(V3), "Punkte", len(T3), "Dreiecke", "min", V3.min(0).round(3), "max", V3.max(0).round(3))

    # 8. Abwicklung auf einer geglaetteten Kopie: die Zotteln sollen keine Inselchen erzeugen
    E3 = kanten(T3)
    Vg = glatt_feld(V3, E3, len(V3), 24, 0.6)
    ob.data.vertices.foreach_set("co", Vg.ravel())
    ob.data.update()
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(72), island_margin=0.0, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
    bpy.context.tool_settings.use_uv_select_sync = True
    bpy.ops.uv.seams_from_islands(mark_seams=True, mark_sharp=False)
    from bpy_extras import bmesh_utils

    # Kleine Inseln mit ihrem laengsten Nachbarn verschmelzen: weniger Verschnitt, weniger Naehte
    bm = bmesh.from_edit_mesh(ob.data)
    uvl = bm.loops.layers.uv.active
    bm.faces.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    # Gegend je Flaeche: 0 Rumpf, 1 Kopf, 2 Pfote. An der Grenze immer eine Naht
    gegend = {}
    for f in bm.faces:
        c3 = np.array(f.calc_center_median())
        l3 = Q["w2l"](c3[None, :])
        hb3 = float(Q["huelle_basis"](l3[:, 0], l3[:, 1], l3[:, 2])[0])
        if hb3 < 0.075 and l3[0, 0] > -0.10:
            gegend[f.index] = 1
        elif c3[2] < 0.15:
            gegend[f.index] = 2
        else:
            gegend[f.index] = 0
    for e in bm.edges:
        if len(e.link_faces) == 2 and gegend[e.link_faces[0].index] != gegend[e.link_faces[1].index]:
            e.seam = True
    # Inseln ueber die Naehte (die UV kennt die neuen Naehte noch nicht)
    gehoert = {}
    inseln = []
    for f0 in bm.faces:
        if f0.index in gehoert:
            continue
        i = len(inseln)
        gehoert[f0.index] = i
        stapel = [f0]
        menge = []
        while stapel:
            f = stapel.pop()
            menge.append(f)
            for e in f.edges:
                if e.seam:
                    continue
                for g in e.link_faces:
                    if g.index not in gehoert:
                        gehoert[g.index] = i
                        stapel.append(g)
        inseln.append(menge)
    eltern = list(range(len(inseln)))
    insel_gegend = [gegend[x[0].index] for x in inseln]

    def wurzel(i):
        while eltern[i] != i:
            eltern[i] = eltern[eltern[i]]
            i = eltern[i]
        return i

    groesse = [len(x) for x in inseln]
    naht = [e for e in bm.edges if e.seam and len(e.link_faces) == 2 and all(v.index < n_haupt for v in e.verts)]
    MIN_FLAECHEN = 70
    for runde in range(40):
        zaehl = {}
        for e in naht:
            if not e.seam:
                continue
            a_ = wurzel(gehoert[e.link_faces[0].index])
            b_ = wurzel(gehoert[e.link_faces[1].index])
            if a_ == b_:
                e.seam = False
                continue
            if insel_gegend[a_] != insel_gegend[b_]:
                continue
            zaehl.setdefault(a_, {}).setdefault(b_, []).append(e)
            zaehl.setdefault(b_, {}).setdefault(a_, []).append(e)
        kleine = sorted([w for w in zaehl if groesse[w] < MIN_FLAECHEN], key=lambda w: groesse[w])
        if not kleine:
            break
        for w in kleine:
            w = wurzel(w)
            if groesse[w] >= MIN_FLAECHEN or w not in zaehl:
                continue
            kand = [(len(es), j) for j, es in zaehl[w].items() if wurzel(j) != w]
            if not kand:
                continue
            kand.sort(reverse=True)
            j = wurzel(kand[0][1])
            if j == w:
                continue
            for e in zaehl[w][kand[0][1]]:
                e.seam = False
            eltern[w] = j
            groesse[j] += groesse[w]
    bmesh.update_edit_mesh(ob.data)
    # Hauptnetz neu abwickeln; die Krallen bekommen je eine ebene Projektion von der Seite, vorn und hinten teilen sich die Flaeche
    bpy.ops.mesh.select_all(action="DESELECT")
    bm = bmesh.from_edit_mesh(ob.data)
    uvl = bm.loops.layers.uv.active
    for f in bm.faces:
        f.select = all(v.index < n_haupt for v in f.verts)
    bmesh.update_edit_mesh(ob.data)
    bpy.ops.uv.unwrap(method="ANGLE_BASED", fill_holes=True, correct_aspect=True, margin=0.002)
    bm = bmesh.from_edit_mesh(ob.data)
    uvl = bm.loops.layers.uv.active
    for f in bm.faces:
        if any(v.index < n_haupt for v in f.verts):
            continue
        for l in f.loops:
            co = l.vert.co
            l[uvl].uv = (co.x + co.y * 0.35, co.z)
    for e in bm.edges:
        if e.verts[0].index >= n_haupt:
            e.seam = False
    bmesh.update_edit_mesh(ob.data)
    # Inseln je Gegend auf ihre Dichte bringen
    bm = bmesh.from_edit_mesh(ob.data)
    uvl = bm.loops.layers.uv.active
    bm.faces.ensure_lookup_table()
    # Fuer die Krallen gibt es keine Gegend mit Bedeutung; sie zaehlen als Pfote
    inseln = bmesh_utils.bmesh_linked_uv_islands(bm, uvl)
    stat = []
    for insel in inseln:
        A3 = sum(f.calc_area() for f in insel)
        Auv = 0.0
        cu = np.zeros(2)
        n_ = 0
        cen3 = np.zeros(3)
        for f in insel:
            pts = [l[uvl].uv.copy() for l in f.loops]
            for i in range(1, len(pts) - 1):
                e1 = pts[i] - pts[0]
                e2 = pts[i + 1] - pts[0]
                Auv += abs(e1.x * e2.y - e1.y * e2.x) * 0.5
            for p in pts:
                cu += np.array((p.x, p.y))
                n_ += 1
            cen3 += np.array(f.calc_center_median())
        cu /= max(n_, 1)
        cen3 /= max(len(insel), 1)
        zaehl_g = [0, 0, 0]
        for f in insel:
            zaehl_g[gegend[f.index]] += 1
        dichte = (1.0, 2.4, 1.35)[zaehl_g.index(max(zaehl_g))]
        fak = dichte * math.sqrt(A3 / max(Auv, 1e-9))
        for f in insel:
            for l in f.loops:
                u_ = l[uvl].uv
                l[uvl].uv = (cu[0] + (u_.x - cu[0]) * fak, cu[1] + (u_.y - cu[1]) * fak)
        stat.append((len(insel), dichte))
    bmesh.update_edit_mesh(ob.data)
    log("UV Inseln", len(inseln), "groesste", sorted([s[0] for s in stat])[-5:], "kleine (<4 Flaechen)", sum(1 for s in stat if s[0] < 4))
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.pack_islands(rotate=True, scale=True, margin_method="SCALED", margin=0.0032, shape_method="CONCAVE")
    bpy.ops.object.mode_set(mode="OBJECT")
    ob.data.vertices.foreach_set("co", V3.ravel())
    ob.data.update()
    # Fuellgrad der Textur
    uv = np.empty(len(ob.data.loops) * 2, dtype=np.float64)
    ob.data.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    ar = 0.0
    for p in ob.data.polygons:
        ids = list(p.loop_indices)
        for i in range(1, len(ids) - 1):
            e1 = uv[ids[i]] - uv[ids[0]]
            e2 = uv[ids[i + 1]] - uv[ids[0]]
            ar += abs(e1[0] * e2[1] - e1[1] * e2[0]) * 0.5
    log("UV Fuellgrad %.3f" % ar, "uv min", uv.min(0).round(3), "max", uv.max(0).round(3))
    ob["n_haupt"] = int(n_haupt)
    bpy.ops.wm.save_as_mainfile(filepath=SP + "lowpoly.blend")
    log("NETZ_OK")


# ------------------------------------------------------------------ Stufe backen: Ansichten auf die Abwicklung
HELL = float(os.environ.get("BAER_HELL", "1.95"))    # Das Spiel rechnet Textur x (0.4 Umgebung + Licht), also duenkler als gebacken
GAMMA = float(os.environ.get("BAER_GAMMA", "0.92"))
TEX = 2048
GROESSE = float(os.environ.get("BAER_GROESSE", "0.75"))   # Hochmodell -> Meter


def raster_uv(UVt, T, Vt, Nt, res):
    pos = np.zeros((res, res, 3), dtype=np.float32)
    nrm = np.zeros((res, res, 3), dtype=np.float32)
    tri = np.full((res, res), -1, dtype=np.int32)
    UVp = UVt * res
    for i in range(len(T)):
        a, b, c = UVp[i]
        den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(den) < 1e-9:
            continue
        x0 = max(int(math.floor(min(a[0], b[0], c[0]) - 1.0)), 0)
        x1 = min(int(math.ceil(max(a[0], b[0], c[0]) + 1.0)), res - 1)
        y0 = max(int(math.floor(min(a[1], b[1], c[1]) - 1.0)), 0)
        y1 = min(int(math.ceil(max(a[1], b[1], c[1]) + 1.0)), res - 1)
        if x1 < x0 or y1 < y0:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        w0 = ((b[1] - c[1]) * (X - c[0]) + (c[0] - b[0]) * (Y - c[1])) / den
        w1 = ((c[1] - a[1]) * (X - c[0]) + (a[0] - c[0]) * (Y - c[1])) / den
        w2 = 1.0 - w0 - w1
        ad = abs(den)
        t0 = -0.75 * math.hypot(*(c - b)) / ad
        t1 = -0.75 * math.hypot(*(a - c)) / ad
        t2 = -0.75 * math.hypot(*(b - a)) / ad
        rand = (w0 >= t0) & (w1 >= t1) & (w2 >= t2)
        if not rand.any():
            continue
        drin = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        sub = tri[y0:y1 + 1, x0:x1 + 1]
        nimm = drin | (rand & (sub < 0))
        g0 = np.clip(w0, 0, 1)
        g1 = np.clip(w1, 0, 1)
        g2 = np.clip(w2, 0, 1)
        s = g0 + g1 + g2
        g0, g1, g2 = g0 / s, g1 / s, g2 / s
        tv = T[i]
        for ax in range(3):
            pos[y0:y1 + 1, x0:x1 + 1, ax][nimm] = (g0 * Vt[tv[0], ax] + g1 * Vt[tv[1], ax] + g2 * Vt[tv[2], ax])[nimm]
            nrm[y0:y1 + 1, x0:x1 + 1, ax][nimm] = (g0 * Nt[tv[0], ax] + g1 * Nt[tv[1], ax] + g2 * Nt[tv[2], ax])[nimm]
        sub[nimm] = i
    return pos, nrm, tri


def zbuffer(av, V, T, res):
    u, v, d = av.pix(V)
    k = res / av.res
    u = u * k
    v = v * k
    Z = np.full((res, res), np.inf, dtype=np.float32)
    # Rueckseiten weglassen: im geschlossenen Netz ist immer eine Vorderseite naeher
    du1, dv1 = u[T[:, 1]] - u[T[:, 0]], v[T[:, 1]] - v[T[:, 0]]
    du2, dv2 = u[T[:, 2]] - u[T[:, 0]], v[T[:, 2]] - v[T[:, 0]]
    vorn = (du1 * dv2 - dv1 * du2) > 0
    for t in T[vorn]:
        ax, bx, cx = u[t[0]], u[t[1]], u[t[2]]
        ay, by, cy = v[t[0]], v[t[1]], v[t[2]]
        x0 = max(int(math.floor(min(ax, bx, cx))), 0)
        x1 = min(int(math.ceil(max(ax, bx, cx))), res - 1)
        y0 = max(int(math.floor(min(ay, by, cy))), 0)
        y1 = min(int(math.ceil(max(ay, by, cy))), res - 1)
        if x1 < x0 or y1 < y0:
            continue
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        w0 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den
        w1 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den
        w2 = 1.0 - w0 - w1
        ins = (w0 >= -0.02) & (w1 >= -0.02) & (w2 >= -0.02)
        if not ins.any():
            continue
        dd = w0 * d[t[0]] + w1 * d[t[1]] + w2 * d[t[2]]
        sub = Z[y0:y1 + 1, x0:x1 + 1]
        sub[ins] = np.minimum(sub[ins], dd[ins])
    return Z


def minfilter(Z):
    out = Z.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            out = np.minimum(out, np.roll(np.roll(Z, dy, 0), dx, 1))
    return out


def srgb(x):
    x = np.clip(x, 0.0, None)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1.0 / 2.4) - 0.055)


def fuellen(col, frei, maske, runden):
    """Fuellt freie Texel von gefuellten Nachbarn, nur innerhalb der Maske."""
    H, W = frei.shape
    for it in range(runden):
        fy, fx = np.nonzero(frei & maske)
        if not len(fy):
            return it
        summe = np.zeros((len(fy), 3), dtype=np.float32)
        cnt = np.zeros(len(fy), dtype=np.float32)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            ny, nx = fy + dy, fx + dx
            ok = (ny >= 0) & (nx >= 0) & (ny < H) & (nx < W)
            idx = np.nonzero(ok)[0]
            ist = ~frei[ny[idx], nx[idx]]
            idx = idx[ist]
            summe[idx] += col[ny[idx], nx[idx]]
            cnt[idx] += 1
        neu = cnt > 0
        col[fy[neu], fx[neu]] = summe[neu] / cnt[neu][:, None]
        frei[fy[neu], fx[neu]] = False
        if not neu.any():
            return it
    return runden


def gesicht_nacharbeit(Q, S, P, kralle):
    """Macht Auge, Nase und Mundlinie im Bild lesbar und gleicht die Gegenden an. S ist sRGB je Texel in der Maske."""
    sst = Q["sst"]
    L = Q["w2l"](P)
    a, b, c = L[:, 0], L[:, 1], L[:, 2]
    B = np.abs(b)
    hb = Q["huelle_basis"](a, b, c)
    kopf = hb < 0.03
    # Gegenden: Kopf etwas dunkler, sonst Maske auf dunklem Koerper; Schnauze noch etwas; Unterbeine heller, sonst schwarz im Spiel
    kopfm = 1.0 - sst(0.0, 0.14, hb)
    R = Q["regionen"](a, b, c)
    S = S * (1.0 - 0.10 * kopfm[:, None])
    S = S * (1.0 - 0.13 * (R["schf"] * kopfm)[:, None])
    S = S * (1.0 + 0.30 * ((1.0 - sst(0.08, 0.50, P[:, 2])) * (1.0 - kopfm))[:, None])
    S = S * (1.0 + 0.42 * ((1.0 - sst(0.04, 0.30, P[:, 2])) * (1.0 - kopfm))[:, None])
    # Fell hinter den Ohren war dunkler als Kopf und Hals: ein Ring wie eine Kapuze
    ring = sst(0.15, -0.05, a) * (1.0 - sst(0.015, 0.11, hb))
    S = S * (1.0 + (0.20 * ring)[:, None] * np.array((1.12, 1.0, 0.82)))
    # Ohr innen dunkel: sonst eine helle Scheibe
    S = S * (1.0 - 0.45 * (R["innen"] * kopfm)[:, None])
    # Unterkiefer: von vorn sonst eine helle Schmollippe
    S = S * (1.0 - 0.24 * (R["unter"] * kopfm)[:, None])
    # Pfoten: Zehen und Ballen dunkel, sonst wirken sie nackt und rosa
    ze = Q["zehen_abstand"](P)
    pf = (1.0 - sst(0.005, 0.040, ze)) * (1.0 - kralle)
    lum = S @ np.array((0.3, 0.55, 0.15))
    dunkel = (lum * 0.62)[:, None] * np.array((1.0, 0.78, 0.60))
    S = S * (1.0 - pf[:, None]) + dunkel * pf[:, None]
    # Krallen: Horn, kein Blau aus dem Himmel
    lum = S @ np.array((0.3, 0.55, 0.15))
    horn = (lum * 0.86)[:, None] * np.array((1.0, 0.87, 0.70))
    S = S * (1.0 - kralle[:, None]) + horn * kralle[:, None]
    # Nase: tiefes Anthrazit statt Spiegelung des hellen Himmels
    fn = Q["feld_nase"](a, b, c)
    nase = (1.0 - sst(0.0005, 0.0070, fn)) * kopf
    S = S * (1.0 - nase[:, None]) + (S * 0.40 * np.array((1.0, 0.97, 0.97)) + 0.018) * nase[:, None]
    x_ = a - Q["NASE_C"][0]
    z_ = c - Q["NASE_C"][2]
    nl = Q["nasenloch"](x_, B, z_)
    loch = (1.0 - sst(-0.004, 0.0035, nl)) * nase
    S = S * (1.0 - 0.75 * loch[:, None])
    # Auge: tief und dunkel, mit Lidrand, kein Glanzpunkt
    AUGE, AU, AV, AW = Q["AUGE"], Q["AU"], Q["AV"], Q["AW"]
    x, y, z = Q["_acht"](a, B, c, AUGE, AU, AV, AW)
    sp = Q["spalt2d"](y, z)
    vorn = sst(-0.022, -0.005, x) * kopf
    schlitz = (1.0 - sst(-0.0005, 0.0026, sp)) * vorn
    lidrand = (1.0 - sst(0.0014, 0.0078, sp)) * vorn
    schatten = (1.0 - sst(0.006, 0.030, np.sqrt(y * y + z * z))) * vorn
    S = S * (1.0 - 0.16 * schatten[:, None])
    S = S * (1.0 - 0.50 * lidrand[:, None])
    S = S * (1.0 - schlitz[:, None]) + np.array((0.030, 0.019, 0.014)) * schlitz[:, None]
    # Mundlinie: nur eine dunkle Rille, keine gemalte Lippe
    dv = Q["lippe"](a, B) - c
    vorne = sst(Q["ECKE"] - 0.006, Q["ECKE"] + 0.034, a) * kopf
    linie = (1.0 - sst(0.0006, 0.0040, np.abs(dv))) * vorne
    saum = (1.0 - sst(0.001, 0.0085, np.abs(dv + 0.0030))) * vorne
    S = S * (1.0 - 0.18 * saum[:, None])
    S = S * (1.0 - 0.50 * linie[:, None])
    fur = Q["cap"](a, B, c, (0.497, 0.0, 0.010), (0.486, 0.0, -0.046), 0.0)
    rille = (1.0 - sst(0.0015, 0.0050, fur)) * kopf
    S = S * (1.0 - 0.30 * rille[:, None])
    return S


def unscharf(col, k, runden=2):
    """Kleine Unschaerfemaske im Texturraum: die Fellstriche sollen nach dem Mischen wieder Biss haben."""
    b = col.copy()
    for _ in range(runden):
        b = (np.roll(b, 2, 0) + np.roll(b, -2, 0) + np.roll(b, 2, 1) + np.roll(b, -2, 1) + b * 2.0) / 6.0
    if np.ndim(k) == 2:
        k = k[..., None]
    return np.clip(col + (col - b) * k, 0.0, 1.0)


def stufe_backen():
    Q = quelle("form")
    bpy.ops.wm.open_mainfile(filepath=SP + "lowpoly.blend")
    scene = bpy.context.scene
    ob = bpy.data.objects["NCBear"]
    me = ob.data
    V, T = netz_arrays(me)
    m = len(T)
    LT = np.empty(m * 3, dtype=np.int64)
    me.loop_triangles.foreach_get("loops", LT)
    LT = LT.reshape(m, 3)
    uv = np.empty(len(me.loops) * 2, dtype=np.float64)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    E = kanten(T)
    Vg = glatt_feld(V, E, len(V), 8, 0.6)
    N = v_normalen(Vg, T)
    t0 = time.time()
    pos, nrm, tri = raster_uv(uv[LT], T, V, N, TEX)
    maske = tri >= 0
    log("UV gerastert", "%.1fs" % (time.time() - t0), "Texel", int(maske.sum()), "Anteil %.3f" % maske.mean())
    P = pos[maske].astype(np.float64)
    Nn = nrm[maske].astype(np.float64)
    Nn /= np.maximum(np.linalg.norm(Nn, axis=1, keepdims=True), 1e-9)
    n_t = len(P)
    sum_c = np.zeros((n_t, 3), dtype=np.float32)
    sum_w = np.zeros(n_t, dtype=np.float32)
    views = json.load(open(ANS + "kameras.json"))
    L_ = Q["w2l"](P)
    kopf_maske = 1.0 - Q["sst"](0.02, 0.20, Q["huelle_basis"](L_[:, 0], L_[:, 1], L_[:, 2]))
    for v in views:
        t1 = time.time()
        av = Ansicht(v)
        kopf = av.name.startswith("h_")
        Z = minfilter(zbuffer(av, V, T, 1024))
        rgba = lade_exr(ANS + v["name"] + ".exr")
        u, vv, dep = av.pix(P)
        k = 1024.0 / av.res
        iu = np.clip(np.floor(u * k).astype(np.int64), 0, 1023)
        iv = np.clip(np.floor(vv * k).astype(np.int64), 0, 1023)
        tol = 0.014 if kopf else 0.030
        sicht = dep <= Z[iv, iu] + tol
        cs = np.clip(Nn @ av.d, 0.0, 1.0)
        w = cs ** 7
        if kopf:
            w = w * kopf_maske
        w[cs < 0.2] = 0.0
        w[~sicht] = 0.0
        idx = np.nonzero(w > 1e-5)[0]
        if len(idx):
            col, inn = bilinear(rgba, u[idx], vv[idx])
            al = col[:, 3]
            g = w[idx] * inn * (al > 0.45) * al * al
            if kopf:
                g *= 7.0
            c = col[:, :3] / np.maximum(al, 1e-3)[:, None]
            sum_c[idx] += (c * g[:, None]).astype(np.float32)
            sum_w[idx] += g.astype(np.float32)
        log("Projektion", v["name"], "Texel", len(idx), "%.1fs" % (time.time() - t1))
    gesehen = sum_w > 1e-5
    log("Gesehen %.4f der Texel" % gesehen.mean())
    lin = np.zeros_like(sum_c)
    lin[gesehen] = sum_c[gesehen] / sum_w[gesehen][:, None]
    # sRGB, heller gebacken
    S = srgb(lin)
    S = np.power(np.clip(S, 0.0, 1.0), GAMMA) * HELL
    n_haupt = int(ob.get("n_haupt", len(V)))
    kralle = (T[:, 0] >= n_haupt)[tri[maske]].astype(np.float64)
    S = gesicht_nacharbeit(Q, S, P, kralle)
    log("Abgeschnitten (Wert 1.0): %.4f der Texel" % float((S >= 1.0).any(axis=1).mean()))
    S = np.clip(S, 0.0, 1.0)
    col = np.zeros((TEX, TEX, 3), dtype=np.float32)
    frei = np.ones((TEX, TEX), dtype=bool)
    my, mx = np.nonzero(maske)
    col[my[gesehen], mx[gesehen]] = S[gesehen].astype(np.float32)
    frei[my[gesehen], mx[gesehen]] = False
    r = fuellen(col, frei, maske, 400)
    rest = int((frei & maske).sum())
    log("Innen gefuellt", r, "Runden; Rest", rest)
    if rest:
        col[frei & maske] = S[gesehen].mean(0)
        frei[frei & maske] = False
    # Rand ueber die Inseln hinaus: gegen helle oder schwarze Naehte beim Verkleinern
    alle = np.ones_like(maske)
    fuellen(col, frei, alle, 14)
    col[frei] = S[gesehen].mean(0)
    # Hinter den Ohren sind die Kopfhaare sehr fein: dort nicht schaerfen, sonst sieht es wie Schuppen aus
    L_2 = Q["w2l"](P)
    ring_k = Q["sst"](0.15, -0.05, L_2[:, 0]) * (1.0 - Q["sst"](0.015, 0.11, Q["huelle_basis"](L_2[:, 0], L_2[:, 1], L_2[:, 2])))
    kmap = np.full((TEX, TEX), 0.85, dtype=np.float32)
    kmap[my, mx] = (0.85 * (1.0 - 0.9 * ring_k)).astype(np.float32)
    col = unscharf(col, kmap)
    log("Textur Mittel sRGB", (col[maske].mean(0) * 255).round(1))
    img = bpy.data.images.new("NCBear", TEX, TEX, alpha=False)
    rgba = np.ones((TEX, TEX, 4), dtype=np.float32)
    rgba[..., :3] = col
    img.pixels.foreach_set(rgba.ravel())
    img.filepath_raw = MOD + "textures/WorldItems/NCBear.png"
    img.file_format = "PNG"
    img.save()
    log("Textur gespeichert")
    # Ein Material, nur die Textur
    me.materials.clear()
    mat = bpy.data.materials.new("NCBear")
    mat.use_nodes = True
    br = mat.node_tree.nodes["Principled BSDF"]
    tn = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tn.image = img
    mat.node_tree.links.new(tn.outputs["Color"], br.inputs["Base Color"])
    br.inputs["Roughness"].default_value = 1.0
    me.materials.append(mat)
    # In die Spielgroesse: Ursprung auf dem Boden unter der Koerpermitte
    mitte = V[T].mean(1)
    fl = 0.5 * np.linalg.norm(np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]), axis=1)
    x0 = float((mitte[:, 0] * fl).sum() / fl.sum())
    zmin = float(V[:, 2].min())
    Vn = (V - np.array((x0, 0.0, zmin))) * GROESSE
    me.vertices.foreach_set("co", Vn.ravel())
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    log("MASSE Meter: Laenge %.3f Breite %.3f Hoehe %.3f; Ursprung bei Hochmodell-x %.3f; Dreiecke %d" % (Vn[:, 0].max() - Vn[:, 0].min(), Vn[:, 1].max() - Vn[:, 1].min(), Vn[:, 2].max(), x0, m))
    log("x von %.3f bis %.3f, z von %.3f" % (Vn[:, 0].min(), Vn[:, 0].max(), Vn[:, 2].min()))
    bpy.ops.export_scene.fbx(filepath=MOD + "models_X/WorldItems/NCBear.fbx", use_selection=True, apply_unit_scale=True,
                             apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y", bake_anim=False,
                             mesh_smooth_type="FACE", use_mesh_modifiers=True, add_leaf_bones=False)
    bpy.ops.wm.save_as_mainfile(filepath=SP + "spielmodell.blend")
    log("BACKEN_OK")


# ------------------------------------------------------------------ Stufe vorschau: das fertige Modell aus der Mod-Datei
def stufe_vorschau():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    bpy.ops.import_scene.fbx(filepath=MOD + "models_X/WorldItems/NCBear.fbx")
    ob = [o for o in bpy.context.selected_objects if o.type == "MESH"][0]
    me = ob.data
    img = bpy.data.images.load(MOD + "textures/WorldItems/NCBear.png")
    img.colorspace_settings.name = "sRGB"
    me.materials.clear()
    mat = bpy.data.materials.new("spiel")
    mat.use_nodes = True
    br = mat.node_tree.nodes["Principled BSDF"]
    tn = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tn.image = img
    mat.node_tree.links.new(tn.outputs["Color"], br.inputs["Base Color"])
    br.inputs["Roughness"].default_value = 1.0
    br.inputs["Specular IOR Level"].default_value = 0.0
    me.materials.append(mat)
    log("FBX-Masse", tuple(round(x, 3) for x in ob.dimensions), "Skalierung", tuple(round(x, 3) for x in ob.scale), "Dreiecke", sum(len(p.vertices) - 2 for p in me.polygons))
    # Massstab: Kapsel 1,8 m
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.22, radius2=0.22, depth=1.36)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, 0.9))
    r2 = bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=0.22)
    bmesh.ops.translate(bm, verts=r2["verts"], vec=(0, 0, 0.22))
    r3 = bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=0.22)
    bmesh.ops.translate(bm, verts=r3["verts"], vec=(0, 0, 1.58))
    kme = bpy.data.meshes.new("kapsel")
    bm.to_mesh(kme)
    bm.free()
    kme.shade_smooth()
    kap = bpy.data.objects.new("kapsel", kme)
    scene.collection.objects.link(kap)
    kap.location = (0.2, 1.05, 0.0)
    km = bpy.data.materials.new("grau")
    km.use_nodes = True
    km.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.32, 0.32, 0.32, 1)
    kme.materials.append(km)
    # Boden dunkel
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    gr = bpy.context.active_object
    gm = bpy.data.materials.new("boden")
    gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.055, 0.055, 0.05, 1)
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    gr.data.materials.append(gm)
    # Licht ungefaehr wie im Spiel: viel Umgebung, eine weiche Hauptrichtung
    w = bpy.data.worlds.new("w")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.55
    scene.world = w
    sun = bpy.data.lights.new("s", "SUN")
    sun.energy = 1.7
    sun.angle = math.radians(25)
    so = bpy.data.objects.new("s", sun)
    scene.collection.objects.link(so)
    so.rotation_euler = (math.radians(48), 0, math.radians(40))
    gpu(scene, 64, True)
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"

    def foto(pos, ziel, ortho, res, pfad, lens=None):
        cam = bpy.data.cameras.new("c")
        if ortho:
            cam.type = "ORTHO"
            cam.ortho_scale = ortho
        else:
            cam.lens = lens
        co = bpy.data.objects.new("c", cam)
        scene.collection.objects.link(co)
        co.location = pos
        co.rotation_mode = "QUATERNION"
        co.rotation_quaternion = (Vector(ziel) - Vector(pos)).to_track_quat("-Z", "Y")
        scene.camera = co
        scene.render.resolution_x, scene.render.resolution_y = res
        scene.render.filepath = pfad
        bpy.ops.render.render(write_still=True)
        log("Bild", pfad.split("/")[-1])

    foto((6, -6, 5.6), (0.1, 0.25, 0.6), 3.9, (1100, 900), HIER + "vorschau_spiel.png")
    # Spielgroesse: so klein etwa zeigt es das Spiel bei Zoom 1 (ein Meter gut 100 Pixel)
    foto((6, -6, 5.6), (0.1, 0.25, 0.6), 3.9, (390, 320), SP + "probe/spielgroesse.png")
    # Nah: dreiviertel von vorn
    kap.hide_render = True
    foto((3.5, -2.55, 1.15), (0.55, 0.0, 0.62), None, (1200, 900), HIER + "vorschau_nah.png", lens=62)
    foto((0.0, -5.8, 0.75), (0.0, 0.0, 0.62), None, (1200, 700), SP + "probe/nah_seite.png", lens=62)
    foto((2.6, 0.0, 0.85), (0.95, 0.0, 0.62), None, (800, 800), SP + "probe/nah_kopfvorn.png", lens=85)
    # Wie das Spiel rechnet (basicEffect.frag, WorldItemAtlas RenderJob.renderModel): Textur x (0.4 + 0.375 x Lambert), Licht (0,5,-2), danach Kachellicht
    em = bpy.data.materials.new("wie_spiel")
    em.use_nodes = True
    nt = em.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    tx = nt.nodes.new("ShaderNodeTexImage")
    img2 = img.copy()
    img2.colorspace_settings.name = "Non-Color"
    tx.image = img2
    ge = nt.nodes.new("ShaderNodeNewGeometry")
    dp = nt.nodes.new("ShaderNodeVectorMath")
    dp.operation = "DOT_PRODUCT"
    lv = Vector((0.0, 2.0, 5.0)).normalized()
    dp.inputs[1].default_value = (lv.x, lv.y, lv.z)
    nt.links.new(ge.outputs["Normal"], dp.inputs[0])
    cl = nt.nodes.new("ShaderNodeMapRange")
    cl.clamp = True
    cl.inputs["From Min"].default_value = 0.0
    cl.inputs["From Max"].default_value = 1.0
    cl.inputs["To Min"].default_value = 0.4
    cl.inputs["To Max"].default_value = 0.775
    nt.links.new(dp.outputs["Value"], cl.inputs["Value"])
    mu = nt.nodes.new("ShaderNodeVectorMath")
    mu.operation = "SCALE"
    nt.links.new(tx.outputs["Color"], mu.inputs[0])
    nt.links.new(cl.outputs[0], mu.inputs["Scale"])
    ee = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(mu.outputs[0], ee.inputs["Color"])
    nt.links.new(ee.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    me.materials[0] = em
    scene.view_settings.view_transform = "Raw"
    kap.hide_render = False
    alt_w = scene.world.node_tree.nodes["Background"].inputs[1].default_value
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.0
    sun.energy = 0.0
    gm.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (0.20, 0.235, 0.14, 1)
    gm.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.0
    km.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (0.42, 0.42, 0.42, 1)
    km.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.0
    foto((6, -6, 5.6), (0.1, 0.25, 0.6), 3.9, (1100, 900), HIER + "vorschau_wie_spiel.png")
    me.materials[0] = mat
    scene.view_settings.view_transform = "Standard"
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = alt_w
    sun.energy = 1.7
    kap.hide_render = True
    # Icon: 32 x 32
    gr.hide_render = True
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = "RGBA"
    foto((6, -6, 5.6), (0.1, 0.0, 0.5), 2.75, (256, 256), SP + "probe/icon_gross.png")
    i2 = bpy.data.images.load(SP + "probe/icon_gross.png")
    i2.scale(32, 32)
    i2.filepath_raw = MOD + "textures/Item_NCBear.png"
    i2.file_format = "PNG"
    i2.save()
    log("VORSCHAU_OK")


def stufe_fellprobe():
    Q = quelle("spiel")
    log("Hochmodell steht")
    scene = bpy.context.scene
    gpu(scene, 48, True)
    neutrale_welt(scene)
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    koerper = kamera_daten()[0]["c"]
    kopf = kopf_kameras(Q)[0]["c"]
    for name, c, az, el, ortho, res in (
        ("seite", koerper, 270, 2, 3.5, 1000),
        ("spielwinkel", koerper, -45, 32, 3.5, 800),
        ("kopf34", kopf, -35, 10, 1.0, 800),
        ("kopfseite", kopf, -90, 2, 1.0, 800),
        ("kopfvorn", kopf, 0, 6, 1.0, 800),
    ):
        a, e = math.radians(az), math.radians(el)
        d = [math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)]
        kamera_setzen(scene, dict(name=name, c=list(c), d=d, ortho=ortho, res=res))
        scene.render.filepath = SP + "probe/fell_" + name + ".png"
        t = time.time()
        bpy.ops.render.render(write_still=True)
        log("BILD", name, "%.1fs" % (time.time() - t))
    log("FELLPROBE_OK")


if __name__ == "__main__" or True:
    if STUFE == "probe":
        stufe_probe()
    elif STUFE == "fellprobe":
        stufe_fellprobe()
    elif STUFE == "ansichten":
        stufe_ansichten()
    elif STUFE == "netz":
        stufe_netz()
    elif STUFE == "backen":
        stufe_backen()
    elif STUFE == "vorschau":
        stufe_vorschau()
