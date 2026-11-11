# Entwuerfe 2 fuer das Markierungs-Symbol "wildes Baerenjunges in der Naehe" (96x96 RGBA), Cartoon-Stil nach Kevins
# Stilvorlage (baer/begleiter/kevin_icon_vorlage.png, nur Stil -- eigene Zeichnung, nichts uebernommen):
# braunes Junges, dunkle Umrisslinie, zwei bis drei Brauntoene, grosse Glanzaugen, helle Schnauze, Fell-Zacken am Rand.
#   W1 Kopf von vorn (rundes Portrait, fuellt den Kreis)
#   W2 ganzes Junges sitzend von vorn (Fusssohlen mit Ballen)
#   W3 Kopf schraeg geneigt, neugieriger Blick
# Gezeichnet als Vektorformen mit 8-facher Ueberabtastung (PIL + numpy), dann auf 96 px verkleinert.
# Aufruf: python zeichne_icons_2.py <Bandits common/media/ui> <Blatt.png>
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 8                       # Ueberabtastung
N = 96 * SS
OUTW = 1.15                  # Umrisslinie in Endpixeln (unabhaengig von der Figurgroesse)
GY, GX = (np.mgrid[0:N, 0:N].astype(np.float32) + 0.5) / SS      # Pixelmitten in 96er-Einheiten

# Farben (eigene Palette)
OUT    = (48, 26, 16)
FUR    = (139, 82, 47)
FUR_D  = (106, 59, 33)
FUR_DD = (78, 41, 23)
FUR_L  = (176, 112, 66)
MUZ    = (241, 203, 158)
MUZ_D  = (215, 163, 113)
NOSE   = (40, 23, 17)
NOSE_H = (128, 96, 86)
EYE    = (24, 13, 9)
IRIS   = (92, 52, 30)
WHITE  = (255, 255, 255)
CHEST  = (224, 164, 103)
PAD    = (238, 156, 104)
PAD_D  = (206, 120, 78)
BLUSH  = (226, 120, 98)

# ---------------------------------------------------------------- Geometrie
def rot(pts, ang, cx=0.0, cy=0.0):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]

def angd(a, b):
    return (a - b + 180.0) % 360.0 - 180.0

def ell(cx, cy, rx, ry, ang=0.0, n=360, spikes=(), squash=None):
    """Ellipse als Punktliste; spikes = [(Mitte_Grad, Halbbreite_Grad, Anzahl, Tiefe, Schraege)] -> Fell-Zacken.
    Winkel im Bildsinn (0 = rechts, 90 = unten)."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        deg = math.degrees(t)
        r = 1.0
        if squash:
            r *= squash(deg)
        for tc, hw, k, depth, skew in spikes:
            d = angd(deg, tc)
            if abs(d) < hw:
                u = (d + hw) / (2 * hw)
                env = math.sin(math.pi * u) ** 0.6
                ph = (u * k) % 1.0
                f = ph / skew if ph < skew else (1 - ph) / (1 - skew)
                r += depth * env * f ** 1.25
        x, y = rx * r * math.cos(t), ry * r * math.sin(t)
        pts.append((x, y))
    if ang:
        pts = rot(pts, ang)
    return [(cx + x, cy + y) for x, y in pts]

def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; mt = 1 - t
        out.append((mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0],
                    mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1]))
    return out

class Xf:
    """Lokale Figur-Koordinaten -> 96er-Flaeche: skalieren, drehen, verschieben."""
    def __init__(self, ox, oy, s=1.0, ang=0.0):
        self.ox, self.oy, self.s, self.ang = ox, oy, s, ang
    def __call__(self, pts):
        a = math.radians(self.ang); ca, sa = math.cos(a), math.sin(a)
        return [(self.ox + self.s * (x * ca - y * sa), self.oy + self.s * (x * sa + y * ca)) for x, y in pts]

# ---------------------------------------------------------------- Leinwand
class Canvas:
    def __init__(self):
        self.C = np.zeros((N, N, 3), np.float32)
        self.A = np.zeros((N, N), np.float32)

    def mask(self, pts, stroke=0.0, closed=True):
        img = Image.new("L", (N, N), 0)
        d = ImageDraw.Draw(img)
        P = [(x * SS, y * SS) for x, y in pts]
        if closed:
            d.polygon(P, fill=255)
            if stroke > 0:
                # Umriss = Form um eine Kreisscheibe erweitert (Vereinigung verschobener Kopien; PILs breite Linien
                # fransen an spitzen Zacken aus)
                R = stroke * SS
                for rad, n in ((R, 40), (R * 0.66, 28), (R * 0.33, 16)):
                    for i in range(n):
                        t = 2 * math.pi * i / n
                        ox, oy = rad * math.cos(t), rad * math.sin(t)
                        d.polygon([(x + ox, y + oy) for x, y in P], fill=255)
        elif stroke > 0:
            w = max(1, int(round(stroke * SS)))
            d.line(P, fill=255, width=w, joint="curve")
            rr = w / 2.0
            for ex, ey in (P[0], P[-1]):
                d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=255)
        return np.asarray(img, np.float32) / 255.0

    def paint(self, m, col, op=1.0):
        a = m * op
        c = np.array(col[:3], np.float32) / 255.0
        self.C = self.C * (1 - a)[..., None] + c * a[..., None]
        self.A = self.A + a * (1 - self.A)

    def part(self, pts, fill, outline=True, ow=None):
        if outline:
            self.paint(self.mask(pts, stroke=OUTW if ow is None else ow), OUT)
        m = self.mask(pts)
        self.paint(m, fill)
        return m

    def shade(self, clip, pts, col, blur=0.0, op=1.0):
        r = self.mask(pts)
        if blur > 0:
            r = blurm(r, blur)
        self.paint(clip * r, col, op)

    def line(self, pts, w, col, clip=None, op=1.0):
        m = self.mask(pts, stroke=w, closed=False)
        if clip is not None:
            m = m * clip
        self.paint(m, col, op)

    def dot(self, x, y, r, col, clip=None, op=1.0):
        m = self.mask(ell(x, y, r, r, n=64))
        if clip is not None:
            m = m * clip
        self.paint(m, col, op)

def blurm(m, r):
    im = Image.fromarray(np.clip(m * 255, 0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r * SS)), np.float32) / 255.0

def finish(cv, shadow=(0.7, 1.1, 1.2, 0.55)):
    """Schatten unter die Figur, dann auf 96 und auf 288 verkleinern. Rueckgabe (96er, 288er) als RGBA-Bilder."""
    dx, dy, br, op = shadow
    sh = np.roll(np.roll(cv.A, int(round(dy * SS)), 0), int(round(dx * SS)), 1)
    sh = blurm(sh, br) * op
    A = cv.A + sh * (1 - cv.A)
    Cpm = cv.C * cv.A[..., None]                     # vormultipliziert; Schatten ist schwarz
    rgba = np.zeros((N, N, 4), np.float32)
    rgba[..., :3] = Cpm
    rgba[..., 3] = A
    def down(f):
        k = N // f
        R = rgba.reshape(f, k, f, k, 4).mean(axis=(1, 3))
        a = R[..., 3:4]
        rgb = np.where(a > 1e-4, R[..., :3] / np.maximum(a, 1e-4), 0)
        return Image.fromarray(np.clip(np.concatenate([rgb, a], -1) * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")
    big = Image.fromarray(np.clip(np.concatenate([np.where(A[..., None] > 1e-4, Cpm / np.maximum(A[..., None], 1e-4), 0),
                                                  A[..., None]], -1) * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA")
    # gross: Ausschnitt 15..79 der 96er-Flaeche (die Figur), auf 288 px
    big = big.crop((15 * SS, 14 * SS, 79 * SS, 78 * SS)).resize((288, 288), Image.LANCZOS)
    return down(96), big

# ---------------------------------------------------------------- Kopf (lokal: Mitte 0,0; Kopfbreite 40)
def head(cv, X, look=(0.0, 0.0), brow=0.0, mouth="smile", ear_tilt=(0.0, 0.0), eye_k=1.0, blush=0.0):
    # Ohren (hinter dem Kopf)
    for sx, et in ((-1, ear_tilt[0]), (1, ear_tilt[1])):
        ex, ey = sx * 14.6, -14.6 + et
        cv.part(X(ell(ex, ey, 7.9, 7.6)), FUR)
        m_in = cv.mask(X(ell(ex + sx * 0.3, ey - 0.2, 4.7, 4.4)))
        cv.paint(m_in, FUR_DD)
        # heller Rand innen unten (Fell vor der Ohrmuschel)
        cv.shade(m_in, X(ell(ex - sx * 1.2, ey + 3.4, 4.6, 2.4)), FUR_D, blur=0.25)

    # Kopf mit Fell-Zacken: Wangen links/rechts, kleiner Schopf oben
    sp = [(26, 32, 3, 0.16, 0.78), (154, 32, 3, 0.16, 0.22),             # Wangen (nach unten gekaemmt)
          (-90, 15, 3, 0.11, 0.5)]                                      # Schopf
    hp = ell(0, 1.0, 20.0, 17.6, spikes=sp,
             squash=lambda d: 1.0 + 0.035 * math.cos(math.radians(2 * (d - 90))) * (1 if 0 < d % 360 < 180 else 0.4))
    mh = cv.part(X(hp), FUR)

    # Schattierung: unten/seitlich dunkler, Grenze als Fell-Zacken, Stirn heller
    dark = 1.0 - cv.mask(X(ell(0, -2.6, 18.0, 17.0, spikes=[(90, 80, 10, 0.07, 0.5)])))
    cv.paint(mh * blurm(dark, 0.25), FUR_D)
    cv.shade(mh, X(ell(0, -6.5, 12.5, 8.5)), FUR_L, blur=1.6, op=0.85)
    # helle Augenhoefe
    for sx in (-1, 1):
        cv.shade(mh, X(ell(sx * 7.6, -1.0, 5.6, 5.8)), FUR_L, blur=0.9, op=0.9)
    # Fellstriche (Wangen, Stirn)
    for sx in (-1, 1):
        for (a, b, c) in (((15.2, 3.6), (17.0, 6.0), (18.6, 7.4)), ((13.6, 9.6), (15.2, 11.8), (16.6, 13.0))):
            cv.line(X(bez((sx * a[0], a[1]), (sx * b[0], b[1]), (sx * b[0], b[1]), (sx * c[0], c[1]), 10)),
                    0.5, FUR_DD, clip=mh, op=0.7)

    # Wangenroete (sehr leicht)
    if blush > 0:
        for sx in (-1, 1):
            cv.shade(mh, X(ell(sx * 11.5, 6.0, 3.4, 2.2)), BLUSH, blur=0.9, op=blush)

    # Brauen
    for sx in (-1, 1):
        by = -7.4 - brow * (1.3 if sx > 0 else 0.6)
        cv.line(X(bez((sx * 5.2, by + 0.6), (sx * 6.6, by - 0.6), (sx * 8.8, by - 0.6), (sx * 10.2, by + 0.3), 12)),
                0.75, FUR_DD, clip=mh, op=0.85)

    # Augen
    erx, ery = 3.35 * eye_k, 3.85 * eye_k
    for sx in (-1, 1):
        ex, ey = sx * 7.4, -1.3
        cv.part(X(ell(ex, ey, erx, ery)), EYE, ow=0.45)
        me = cv.mask(X(ell(ex, ey, erx, ery)))
        # Iris-Schimmer unten, Pupille dunkel
        cv.shade(me, X(ell(ex + look[0] * 0.6, ey + 1.9 + look[1] * 0.4, erx * 0.8, ery * 0.42)), IRIS, blur=0.4, op=0.9)
        cv.dot(*X([(ex + look[0], ey + look[1])])[0], 1.9 * eye_k * X.s, EYE, clip=me)
        hx, hy = X([(ex + 1.15 * eye_k + look[0] * 0.5, ey - 1.35 * eye_k + look[1] * 0.4)])[0]
        cv.dot(hx, hy, 1.45 * eye_k * X.s, WHITE)
        hx, hy = X([(ex - 1.25 * eye_k + look[0] * 0.4, ey + 1.6 * eye_k + look[1] * 0.3)])[0]
        cv.dot(hx, hy, 0.65 * eye_k * X.s, WHITE, op=0.9)

    # Schnauze (hell, ohne Umriss) + heller Steg zwischen den Augen
    cv.shade(mh, X(ell(0, 0.2, 3.6, 5.5)), FUR_L, blur=0.6, op=0.9)
    mm = cv.mask(X(ell(0, 7.8, 8.9, 6.8, squash=lambda d: 1.0 - 0.07 * math.sin(math.radians(d)) if d > 180 else 1.0)))
    cv.paint(mm * mh, MUZ_D)
    cv.shade(mm * mh, X(ell(0, 6.6, 8.3, 5.9)), MUZ, blur=0.5)
    # Nase
    npts = bez((-3.5, 4.0), (-3.7, 1.6), (3.7, 1.6), (3.5, 4.0), 16) + bez((3.5, 4.0), (3.2, 6.0), (0.9, 7.2), (0.0, 7.3), 10)[1:] \
        + bez((0.0, 7.3), (-0.9, 7.2), (-3.2, 6.0), (-3.5, 4.0), 10)[1:-1]
    cv.part(X(npts), NOSE, ow=0.4)
    mn = cv.mask(X(npts))
    cv.shade(mn, X(ell(-0.6, 3.2, 1.8, 0.8)), NOSE_H, blur=0.2, op=0.95)
    # Mund
    if mouth == "smile":
        cv.line(X([(0, 7.0), (0, 8.9)]), 0.75, NOSE)
        cv.line(X(bez((-4.6, 8.4), (-3.4, 11.4), (-0.9, 11.2), (0, 8.9), 14)), 0.75, NOSE)
        cv.line(X(bez((0, 8.9), (0.9, 11.2), (3.4, 11.4), (4.6, 8.4), 14)), 0.75, NOSE)
    elif mouth == "oh":
        cv.line(X([(0, 7.0), (0, 8.5)]), 0.7, NOSE)
        mo = ell(0.2, 10.4, 1.9, 1.7)
        cv.part(X(mo), (70, 28, 24), ow=0.4)
        cv.shade(cv.mask(X(mo)), X(ell(0.2, 11.6, 1.5, 0.9)), (214, 110, 110), blur=0.1)
    return mh

# ---------------------------------------------------------------- Entwuerfe
def w1():
    cv = Canvas()
    X = Xf(47.0, 49.0, 0.92)
    head(cv, X, eye_k=1.08, blush=0.25)
    return cv

def w2():
    cv = Canvas()
    K = 0.9                                   # Koerper etwas kleiner, damit Fuesse nicht in den Text ragen
    B = Xf(47 - 47 * K, 47 - 47 * K, K)       # Koerper-Koordinaten (wie 96er) um (47,47) skaliert
    # Rumpf (birnenfoermig, unten breiter) mit hellem Bauch und Brustfleck
    body = ell(47, 59.0, 13.0, 12.2, squash=lambda d: 1.0 + 0.08 * math.sin(math.radians(d)),
               spikes=[(-8, 22, 2, 0.09, 0.7), (188, 22, 2, 0.09, 0.3)])
    mb = cv.part(B(body), FUR)
    dark = 1.0 - cv.mask(B(ell(46.2, 56.5, 11.4, 12.0)))
    cv.paint(mb * blurm(dark, 0.5), FUR_D)
    cv.shade(mb, B(ell(47, 60.0, 7.5, 8.0)), FUR_L, blur=1.4, op=0.55)
    chest = bez((39.8, 50.0), (42.0, 53.2), (44.6, 55.8), (47.0, 58.4), 14) + \
        bez((47.0, 58.4), (49.4, 55.8), (52.0, 53.2), (54.2, 50.0), 14)[1:] + [(47, 48)]
    cv.shade(mb, B(chest), CHEST, blur=0.35)
    # Fuesse (Sohlen zum Betrachter) mit Ballen
    for sx in (-1, 1):
        fx, fy = 47 + sx * 12.4, 66.4
        fp = ell(fx, fy, 6.8, 5.8, ang=sx * 18)
        mf = cv.part(B(fp), FUR)
        cv.shade(mf, B(ell(fx - sx * 0.6, fy + 2.8, 6.6, 3.0, ang=sx * 18)), FUR_D, blur=0.3)
        cv.part(B(ell(fx + sx * 0.4, fy + 1.1, 3.6, 2.9, ang=sx * 18)), PAD, ow=0.4)
        for tx, ty in ((-3.0, -2.8), (0.0, -3.9), (3.0, -2.8)):
            px, py = rot([(tx, ty)], sx * 18)[0]
            cv.part(B(ell(fx + sx * 0.4 + px, fy + 1.1 + py, 1.25, 1.15)), PAD, ow=0.35)
    # Arme vorn: Umriss nur unten (oben gehen sie weich in die Schulter ueber)
    for sx in (-1, 1):
        acx, acy = 47 + sx * 6.2, 62.6
        ap = B(ell(acx, acy, 3.9, 7.2, ang=-sx * 10))
        bcx, bcy = B([(acx, acy)])[0]
        a = math.radians(-sx * 10)
        v = -(GX - bcx) * math.sin(a) + (GY - bcy) * math.cos(a)        # Lage entlang der Armachse (unten +)
        fade = np.clip((v + 1.5) / 3.0, 0, 1)
        cv.paint(cv.mask(ap, stroke=OUTW) * fade, OUT)
        ma = cv.mask(ap)
        cv.paint(ma, FUR)
        cv.shade(ma, B(ell(acx + sx * 1.8, acy + 0.5, 2.6, 7.4, ang=-sx * 10)), FUR_D, blur=0.5, op=0.75)
        cv.shade(ma, B(ell(acx - sx * 0.6, acy - 5.0, 3.4, 3.0)), FUR, blur=0.8)   # Schulteruebergang
        for dx in (-1.1, 1.1):
            cv.line(B([(acx + dx, acy + 5.0), (acx + dx * 1.1, acy + 6.9)]), 0.5, FUR_DD, clip=ma)
    # Kopf
    X = Xf(47.0, 39.4, 0.75)
    head(cv, X, eye_k=1.16, blush=0.25)
    return cv

def w3():
    cv = Canvas()
    X = Xf(47.0, 49.2, 0.9, ang=16.0)
    head(cv, X, look=(0.9, -0.7), brow=1.0, mouth="oh", ear_tilt=(1.4, -1.6), eye_k=1.12, blush=0.25)
    return cv

DESIGNS = [("W1", "1 - Kopf von vorn", w1), ("W2", "2 - sitzend von vorn", w2), ("W3", "3 - Kopf schraeg, neugierig", w3)]

# ---------------------------------------------------------------- Vorschau wie Bandits
def game_color(col, fade):
    # BanditEventMarkers.lua:147-157 (colorBlend) + :168-174: Farbe wird mit sich selbst multipliziert, Grund 0.22 grau
    base = 0.22
    out = []
    for v in col:
        fv = v * fade
        out.append(fv * fv + base * (1 - fade))
    return tuple(out)

def tint(img, col):
    r, g, b, a = img.split()
    r = r.point(lambda v: int(v * col[0])); g = g.point(lambda v: int(v * col[1])); b = b.point(lambda v: int(v * col[2]))
    return Image.merge("RGBA", (r, g, b, a))

def main():
    BAN = sys.argv[1]
    out_sheet = sys.argv[2]
    color = (1.0, 0.72, 0.30)            # Honig-Braun wie im ersten Blatt (Vorschlag des Koordinators)
    fade = 0.97                          # "in der Naehe": Abstand/Radius ~0.04 -> 0.2 + 0.8*0.96
    base = Image.open(os.path.join(BAN, "eventMarkerBase.png")).convert("RGBA")
    ring = Image.open(os.path.join(BAN, "eventMarker.png")).convert("RGBA")
    gc = game_color(color, fade)
    def marker(icon, angle, scale=1.0):
        m = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
        m.alpha_composite(tint(base, gc))
        m.alpha_composite(ring.rotate(-angle, resample=Image.BICUBIC))
        m.alpha_composite(icon)
        if scale != 1.0:
            m = m.resize((int(96 * scale), int(96 * scale)), Image.LANCZOS)
        return m
    try:
        font = ImageFont.truetype("arial.ttf", 15); fbig = ImageFont.truetype("arialbd.ttf", 22)
        fgame = ImageFont.truetype("arial.ttf", 13); fgame2 = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        font = fbig = fgame = fgame2 = ImageFont.load_default()
    icons = []
    dbg = sys.argv[3] if len(sys.argv) > 3 else None
    for key, title, fn in DESIGNS:
        cv = fn()
        small, big = finish(cv)
        if dbg:
            hi = np.concatenate([cv.C, cv.A[..., None]], -1)
            Image.fromarray(np.clip(hi * 255 + 0.5, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(dbg, f"hi_{key}.png"))
        small.save(os.path.join(HERE, f"BanditsNPCBearCub_marker_{key}.png"))
        big.save(os.path.join(HERE, f"gross_{key}.png"))
        icons.append((title, small, big))
    colw = 420
    sheet = Image.new("RGBA", (colw * 3, 740), (58, 62, 58, 255))
    d = ImageDraw.Draw(sheet)
    for i, (title, ic, big) in enumerate(icons):
        x0 = i * colw
        d.text((x0 + 20, 14), title, fill=(255, 255, 255), font=fbig)
        bg = Image.new("RGBA", (288, 288), (110, 110, 110, 255)); bg.alpha_composite(big)
        sheet.alpha_composite(bg, (x0 + 66, 52))
        d.text((x0 + 20, 352), "so im Spiel (Originalgroesse, Pfeil zeigt zum Jungen):", fill=(220, 220, 220), font=font)
        for j, ang in enumerate((0, 135, 250)):
            mx, my = x0 + 30 + j * 125, 374
            sheet.alpha_composite(marker(ic, ang), (mx, my))
            d.text((mx + 48, my + 48 + 25), "Bear cub nearby", fill=(255, 255, 255), font=fgame, anchor="ma")
        d.text((x0 + 20, 498), "doppelt so gross:", fill=(220, 220, 220), font=font)
        mx, my = x0 + 114, 516
        sheet.alpha_composite(marker(ic, 45, 2.0), (mx, my))
        d.text((mx + 96, my + 96 + 50), "Bear cub nearby", fill=(255, 255, 255), font=fgame2, anchor="ma")
    sheet.convert("RGB").save(out_sheet)
    print("ok", out_sheet)

if __name__ == "__main__":
    main()
