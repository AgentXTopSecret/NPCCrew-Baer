# Zeichnet drei Entwuerfe fuer das Markierungs-Symbol "wildes Baerenjunges" im Stil der Bandits-Markierungen
# (96x96 RGBA, helles Piktogramm mit dunklen Details und weichem Schatten), plus ein Vorschau-Blatt.
import math, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 4                      # Ueberabtastung
W = 96 * S
LIGHT = (232, 232, 232, 255)
MID = (200, 200, 200, 255)
DARK = (70, 70, 70, 255)

def c(d, x, y, r, fill):
    d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill)

def e(d, x, y, rx, ry, fill, ang=0):
    if ang == 0:
        d.ellipse([(x - rx) * S, (y - ry) * S, (x + rx) * S, (y + ry) * S], fill=fill)
        return
    pts = []
    for i in range(64):
        t = 2 * math.pi * i / 64
        px, py = rx * math.cos(t), ry * math.sin(t)
        a = math.radians(ang)
        pts.append(((x + px * math.cos(a) - py * math.sin(a)) * S, (y + px * math.sin(a) + py * math.cos(a)) * S))
    d.polygon(pts, fill=fill)

def rr(d, x0, y0, x1, y1, r, fill):
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=fill)

def arc(d, x, y, r, a0, a1, w, fill):
    d.arc([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], a0, a1, fill=fill, width=int(w * S))

def finish(shape_fn):
    # Form in Hell, Details in Dunkel; Schatten = Form in Schwarz, versetzt, weichgezeichnet
    form = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    shape_fn(ImageDraw.Draw(form), form)
    alpha = form.split()[3]
    shadow = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, W), (0, 0, 0, 150))
    shadow.paste(sh, (int(1.5 * S), int(2 * S)), alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(2.2 * S))
    out = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    out.alpha_composite(shadow)
    out.alpha_composite(form)
    out = out.resize((96, 96), Image.LANCZOS)
    # auf Bandits-Groesse bringen: deren Piktogramme sind etwa 40 px breit/hoch in der 96er-Flaeche (friend/thief/raid)
    box = out.getbbox()
    part = out.crop(box)
    k = 44.0 / max(part.size)
    part = part.resize((max(1, round(part.size[0] * k)), max(1, round(part.size[1] * k))), Image.LANCZOS)
    res = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    res.alpha_composite(part, ((96 - part.size[0]) // 2, (96 - part.size[1]) // 2 + 1))
    return res

# --- V1: Kopf von vorn (rund, runde Ohren, helle Schnauze, Knopfaugen) ---
def v1(d, img):
    c(d, 33, 33, 8.5, LIGHT); c(d, 63, 33, 8.5, LIGHT)          # Ohren
    c(d, 48, 52, 19, LIGHT)                                     # Kopf
    c(d, 33, 33, 4.2, DARK); c(d, 63, 33, 4.2, DARK)            # Ohr innen
    e(d, 48, 60, 10.5, 8, MID)                                  # Schnauze
    c(d, 40.5, 49, 2.6, DARK); c(d, 55.5, 49, 2.6, DARK)        # Augen
    e(d, 48, 56.5, 4.6, 3.3, DARK)                              # Nase
    arc(d, 45, 61, 3.2, 20, 160, 1.2, DARK); arc(d, 51, 61, 3.2, 20, 160, 1.2, DARK)   # Maeulchen

# --- V2: ganzes Junges von der Seite (laeuft nach links) ---
def v2(d, img):
    e(d, 54, 55, 21, 13.5, LIGHT)                               # Rumpf
    c(d, 64, 48, 9, LIGHT)                                      # Buckel/Hinterteil oben
    rr(d, 37, 58, 45, 76, 3.5, LIGHT); rr(d, 47, 60, 54, 75, 3.5, LIGHT)     # Vorderbeine
    rr(d, 60, 58, 68, 76, 3.5, LIGHT); rr(d, 69, 58, 76, 74, 3.5, LIGHT)     # Hinterbeine
    c(d, 31, 46, 11.5, LIGHT)                                   # Kopf
    c(d, 31, 34.5, 4.8, LIGHT)                                  # Ohr
    c(d, 31, 34.5, 2.3, DARK)
    e(d, 20.5, 50, 7.5, 5.2, MID, ang=-8)                       # Schnauze
    e(d, 15.5, 49, 3, 2.4, DARK)                                # Nase
    c(d, 28.5, 44, 2.1, DARK)                                   # Auge
    c(d, 77, 50, 2.5, LIGHT)                                    # Stummelschwanz

# --- V3: Kopf von vorn + Wimmer-Laute (wie die Linien beim "friend"-Symbol) ---
def v3(d, img):
    ox, oy = -3, 4
    c(d, 31 + ox, 35 + oy, 7.5, LIGHT); c(d, 57 + ox, 35 + oy, 7.5, LIGHT)
    c(d, 44 + ox, 52 + oy, 16.5, LIGHT)
    c(d, 31 + ox, 35 + oy, 3.7, DARK); c(d, 57 + ox, 35 + oy, 3.7, DARK)
    e(d, 44 + ox, 59 + oy, 9, 7, MID)
    # traurige Augen (schraeg) + Nase
    e(d, 37.5 + ox, 49 + oy, 2.6, 2.2, DARK); e(d, 50.5 + ox, 49 + oy, 2.6, 2.2, DARK)
    d.line([(34.5 + ox) * S, (45 + oy) * S, (39.5 + ox) * S, (44 + oy) * S], fill=DARK, width=int(1.3 * S))
    d.line([(48.5 + ox) * S, (44 + oy) * S, (53.5 + ox) * S, (45 + oy) * S], fill=DARK, width=int(1.3 * S))
    e(d, 44 + ox, 56 + oy, 4, 2.9, DARK)
    arc(d, 44 + ox, 64.5 + oy, 3.4, 200, 340, 1.2, DARK)       # nach unten gezogener Mund
    # drei Laut-Bogen oben rechts
    for i, r in enumerate((7, 12, 17)):
        arc(d, 62, 34, r, 285, 345, 2.3 - 0.3 * i, LIGHT)

V = {"V1_kopf": v1, "V2_ganz": v2, "V3_wimmern": v3}
icons = {k: finish(f) for k, f in V.items()}
for k, im in icons.items():
    im.save(f"BanditsNPCBearCub_marker_{k}.png")

# --- Vorschau: wie Bandits zeichnet (farbiger Kreis eventMarkerBase + Ring mit Pfeil eventMarker + Symbol + Text) ---
BAN = sys.argv[1]
base = Image.open(f"{BAN}/eventMarkerBase.png").convert("RGBA")
ring = Image.open(f"{BAN}/eventMarker_medium.png").convert("RGBA") if True else None
COLOR = (1.0, 0.72, 0.30)       # Honig-Braun (NPC Crew nimmt fuer Ueberlebende Gruen 0.5/1/0.5)
def tint(img, col, a=1.0):
    r, g, b, al = img.split()
    r = r.point(lambda v: int(v * col[0])); g = g.point(lambda v: int(v * col[1])); b = b.point(lambda v: int(v * col[2]))
    return Image.merge("RGBA", (r, g, b, al))
def marker(icon, angle, scale=1.0):
    m = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    m.alpha_composite(tint(base, COLOR))
    m.alpha_composite(ring.rotate(-angle, resample=Image.BICUBIC))
    m.alpha_composite(icon)
    if scale != 1.0:
        m = m.resize((int(96 * scale), int(96 * scale)), Image.LANCZOS)
    return m
try:
    font = ImageFont.truetype("arial.ttf", 15); fbig = ImageFont.truetype("arialbd.ttf", 22)
except Exception:
    font = fbig = ImageFont.load_default()
colw = 420
sheet = Image.new("RGBA", (colw * 3, 700), (58, 62, 58, 255))
d = ImageDraw.Draw(sheet)
for i, (k, ic) in enumerate(icons.items()):
    x0 = i * colw
    d.text((x0 + 20, 14), ["1 - Kopf von vorn", "2 - ganzes Junges", "3 - Kopf + Wimmern"][i], fill=(255, 255, 255), font=fbig)
    big = Image.new("RGBA", (96, 96), (110, 110, 110, 255)); big.alpha_composite(ic)
    sheet.alpha_composite(big.resize((288, 288), Image.LANCZOS), (x0 + 66, 56))
    d.text((x0 + 20, 352), "so im Spiel (Originalgroesse, Pfeil zeigt zum Jungen):", fill=(220, 220, 220), font=font)
    for j, ang in enumerate((0, 135, 250)):
        mk = marker(ic, ang)
        sheet.alpha_composite(mk, (x0 + 40 + j * 120, 380))
    d.text((x0 + 40, 482), "Bear cub nearby", fill=(255, 255, 255), font=font)
    d.text((x0 + 20, 520), "doppelt so gross:", fill=(220, 220, 220), font=font)
    sheet.alpha_composite(marker(ic, 45, 2.0), (x0 + 110, 540 - 20))
sheet.convert("RGB").save(sys.argv[2])
print("ok", sys.argv[2])
