"""Tonschnitt fuer den Baeren (NC Bear Test).

Schneidet die Spieltoene aus den drei gemeinfreien Aufnahmen unter roh/ (Herkunft: roh/QUELLEN.txt):
NCBear_Roar, NCBear_Growl1/2/3, NCBear_Pain, NCBear_Huff.

Wiederholbar: gleiche Eingabe gibt byte-gleiche Ausgabe (Dither mit festem Samen je Datei).
Format wie Vanillas lose Toene (media/sound/fzombierand5.wav): Mono, 44,1 kHz, 16 Bit.

Aufruf:
  python schnitt.py                 -> Ausgabe nach AUS_VORGABE (Scratchpad des Baer-Kampf-Laufs)
  python schnitt.py --out ORDNER    -> Ausgabe in einen anderen Ordner (z. B. NCBearTest/42/media/sound)
  python schnitt.py --keine-bilder  -> ohne Spektrogramm-Bilder

Braucht numpy und PIL (nur fuer die Bilder). Kein scipy: Filter und Umtastung laufen ueber die FFT.
Die Auswahl der Stuecke ist ueber Huellkurve und Spektrum getroffen, NICHT nach Gehoer.
"""
import os
import sys
import wave
import zlib

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
ROH = os.path.join(HIER, "roh")
AUS_VORGABE = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_kampf/mod/42/media/sound"
BILDER = HIER
SR_AUS = 44100
SPITZE_MAX_DB = -1.0          # Obergrenze Abtastwert-Spitze (dBFS)

# Je Ton: Quelle, Sekunde von/bis (in der Rohdatei), Ziel-Pegel (rms95 der 50-ms-Fenster, dBFS),
# Hochpass (Hz, Ordnung), Tiefpass (Hz, Ordnung), Ein-/Ausblenden (s), Obertonsperre (Jungtier-Summen).
TOENE = [
    # Nur der erste Stoss mit Ausklang (Fixer 08.11.): im Clip NCBear_Rear setzt der Ton bei 0,81 s ein, das Maul ist bis 2,07 s
    # offen; der zweite Stoss (12,28-13,00) lag bei 2,0-2,74 s, als er schon mit geschlossenem Maul auf alle vier ging
    # (kampf_review_technik.md Fund 3). Schnitt in der leisesten Stelle vor dem zweiten Stoss (12,25-12,27, -23 dBFS).
    dict(name="NCBear_Roar", datei="soundbible_242.wav", von=11.08, bis=12.26, ziel=-11.0,
         hp=(110, 4), tp=(7000, 2), ein=0.015, aus=0.120,
         notiz="lautester Ruf der Aufnahme: Stoss 11,13-11,92 mit Ausklang bis 12,26 (der zweite Stoss 12,28-13,00 nicht)"),
    dict(name="NCBear_Growl1", datei="soundbible_242.wav", von=14.86, bis=15.92, ziel=-12.0,
         hp=(110, 4), tp=(7000, 2), ein=0.015, aus=0.080,
         notiz="einzelner Stoss 14,90-15,85, endet natuerlich"),
    dict(name="NCBear_Growl2", datei="soundbible_242.wav", von=16.29, bis=17.28, ziel=-12.0,
         hp=(110, 4), tp=(7000, 2), ein=0.015, aus=0.080,
         notiz="einzelner Stoss 16,32-17,18, harter Einsatz"),
    dict(name="NCBear_Growl3", datei="soundbible_242.wav", von=19.37, bis=20.42, ziel=-12.0,
         hp=(110, 4), tp=(7000, 2), ein=0.015, aus=0.080,
         notiz="einzelner Stoss 19,41-20,37, hellster der drei"),
    dict(name="NCBear_Pain", datei="soundbible_241.wav", von=2.91, bis=3.56, ziel=-13.0,
         hp=(110, 4), tp=(7000, 2), ein=0.020, aus=0.080,
         notiz="tonaler Klagelaut um 490 Hz (kein Knurren) - als Schmerzlaut gedacht"),
    dict(name="NCBear_Huff", datei="soundbible_868.wav", von=3.165, bis=3.37, ziel=-20.0,
         hp=(120, 2), tp=(6000, 2), ein=0.010, aus=0.060, oberton=True, entclip=True,
         notiz="lauter Atemstoss 3,16-3,31 (tief + breitbandig); das gleichzeitig einsetzende "
               "Summen eines Jungtiers (Grundton 420-480 Hz) ist je Obertonlinie um 20 dB gedaempft; "
               "Hochpass 120 Hz nimmt dem Mikrofon-Wumms unter 100 Hz etwas Gewicht"),
]


def lese(pfad):
    w = wave.open(pfad)
    ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
    raw = w.readframes(n)
    w.close()
    if sw != 2:
        raise SystemExit("%s: nur 16 Bit erwartet, ist %d Byte" % (pfad, sw))
    a = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    a = a.reshape(-1, ch)
    return a.mean(axis=1), sr


def entclippe(x, schwelle=0.985, max_lauf=30):
    """Ersetzt kurze Laeufe an der Vollaussteuerung durch ein kubisches Polynom aus je 8 Nachbarn."""
    y = x.copy()
    hoch = np.abs(y) >= schwelle
    laeufe = []
    i = 0
    n = len(y)
    while i < n:
        if hoch[i]:
            j = i
            while j < n and hoch[j]:
                j += 1
            laeufe.append((i, j))
            i = j
        else:
            i += 1
    ersetzt = 0
    for i, j in laeufe:
        if j - i > max_lauf or i < 8 or j + 8 > n:
            continue
        idx = np.r_[i - 8:i, j:j + 8]
        p = np.polyfit(idx.astype(float), y[idx], 3)
        y[i:j] = np.polyval(p, np.arange(i, j, dtype=float))
        ersetzt += j - i
    return y, len(laeufe), ersetzt


def filtere_und_taste(x, sr_ein, sr_aus, hp, tp):
    """Nullphasiger Butterworth-Betrag (Hoch- und Tiefpass) und Umtastung in einer FFT.
    0,5 s Stille an beiden Enden, damit der Kreisschluss der FFT keine Nutzstelle trifft."""
    pad = int(round(0.5 * sr_ein))
    xp = np.concatenate([np.zeros(pad), x, np.zeros(pad)])
    n = len(xp)
    X = np.fft.rfft(xp)
    f = np.fft.rfftfreq(n, 1.0 / sr_ein)
    fs = np.maximum(f, 1e-3)
    g = 1.0 / np.sqrt(1.0 + (hp[0] / fs) ** (2 * hp[1]))
    g = g / np.sqrt(1.0 + (fs / tp[0]) ** (2 * tp[1]))
    g[0] = 0.0
    X = X * g
    if sr_aus == sr_ein:
        y = np.fft.irfft(X, n)
        return y[pad:pad + len(x)]
    m = int(round(n * sr_aus / sr_ein))
    Y = np.zeros(m // 2 + 1, dtype=complex)
    k = min(len(Y), len(X))
    Y[:k] = X[:k]
    y = np.fft.irfft(Y, m) * (m / n)
    pad_aus = int(round(0.5 * sr_aus))
    laenge = int(round(len(x) * sr_aus / sr_ein))
    return y[pad_aus:pad_aus + laenge]


def obertonsperre(x, sr, f0_von=380.0, f0_bis=520.0, harmonische=10, breite=32.0, rand=16.0, tiefe=0.1):
    """Daempft je STFT-Fenster die Linien k*f0 eines tonalen Summens (f0 im Fenster gesucht).
    Fenster ohne deutliche Linie bleiben unberuehrt. Hann/Hann, Hop 1/8, WOLA-Normierung."""
    nfft, hop = 2048, 256
    w = np.hanning(nfft)
    pad = nfft
    xp = np.concatenate([np.zeros(pad), x, np.zeros(pad)])
    nfr = 1 + (len(xp) - nfft) // hop
    y = np.zeros(len(xp))
    wsum = np.zeros(len(xp))
    f = np.fft.rfftfreq(nfft, 1.0 / sr)
    such = (f >= f0_von) & (f <= f0_bis)
    umfeld = (f >= 250) & (f <= 800)
    gesperrt = 0
    for i in range(nfr):
        a = i * hop
        fr = xp[a:a + nfft] * w
        X = np.fft.rfft(fr)
        mag = np.abs(X)
        ks = np.where(such)[0]
        kp = ks[np.argmax(mag[ks])]
        if mag[kp] > 6.0 * np.median(mag[umfeld]) and 1 <= kp < len(mag) - 1:
            # Parabel durch die drei Nachbarn (log), genauere Lage der Linie
            l0, l1, l2 = np.log(mag[kp - 1] + 1e-20), np.log(mag[kp] + 1e-20), np.log(mag[kp + 1] + 1e-20)
            d = 0.5 * (l0 - l2) / (l0 - 2 * l1 + l2) if (l0 - 2 * l1 + l2) != 0 else 0.0
            f0 = (kp + d) * sr / nfft
            g = np.ones_like(f)
            for h in range(1, harmonische + 1):
                fh = h * f0
                if fh > sr / 2:
                    break
                dist = np.abs(f - fh)
                voll = dist <= breite
                weich = (dist > breite) & (dist <= breite + rand)
                g[voll] = np.minimum(g[voll], tiefe)
                t = (dist[weich] - breite) / rand
                g[weich] = np.minimum(g[weich], tiefe + (1 - tiefe) * 0.5 * (1 - np.cos(np.pi * t)))
            X = X * g
            gesperrt += 1
        y[a:a + nfft] += np.fft.irfft(X, nfft) * w
        wsum[a:a + nfft] += w * w
    y = y / np.maximum(wsum, 1e-8)
    return y[pad:pad + len(x)], gesperrt, nfr


def blende(x, sr, ein, aus):
    y = x.copy()
    ne, na = int(round(ein * sr)), int(round(aus * sr))
    if ne > 0:
        y[:ne] *= 0.5 * (1 - np.cos(np.pi * np.arange(ne) / ne))
    if na > 0:
        y[-na:] *= 0.5 * (1 + np.cos(np.pi * (np.arange(na) + 1) / na))
    return y


def rms95(x, sr):
    n = int(0.05 * sr)
    h = int(0.01 * sr)
    if len(x) < n:
        return float(np.sqrt(np.mean(x ** 2)))
    r = [np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n + 1, h)]
    return float(np.percentile(r, 95))


def db(v):
    return 20.0 * np.log10(max(v, 1e-12))


def schreibe(pfad, y, sr, samen):
    rng = np.random.default_rng(samen)
    d = rng.random(len(y)) - rng.random(len(y))          # TPDF-Dither, +-1 LSB
    q = np.clip(np.round(y * 32767.0 + d), -32768, 32767).astype("<i2")
    w = wave.open(pfad, "wb")
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(q.tobytes())
    w.close()
    return q


def bild(q, sr, titel, pfad):
    from PIL import Image, ImageDraw
    x = q.astype(np.float64) / 32768.0
    nfft, hop = 2048, 64
    win = np.hanning(nfft)
    pad = np.concatenate([np.zeros(nfft // 2), x, np.zeros(nfft // 2)])
    nfr = 1 + (len(pad) - nfft) // hop
    idx = np.arange(nfft)[None, :] + hop * np.arange(nfr)[:, None]
    S = np.abs(np.fft.rfft(pad[idx] * win, axis=1)) ** 2
    fr = np.fft.rfftfreq(nfft, 1.0 / sr)
    H, W = 300, 1000
    fmin, fmax = 40.0, 10000.0
    lf = np.exp(np.linspace(np.log(fmax), np.log(fmin), H))
    cols = np.array([np.interp(lf, fr, S[i]) for i in range(nfr)])
    dbm = 10 * np.log10(cols + 1e-14)
    top = dbm.max()
    v = np.clip((dbm.T - (top - 75)) / 75.0, 0, 1)
    stops = np.array([[0, 0, 4], [40, 11, 84], [101, 21, 110], [159, 42, 99],
                      [212, 72, 66], [245, 125, 21], [250, 193, 39], [252, 255, 164]], float)
    s = v * (len(stops) - 1)
    i = np.clip(np.floor(s).astype(int), 0, len(stops) - 2)
    t = (s - i)[..., None]
    img = (stops[i] * (1 - t) + stops[i + 1] * t).astype(np.uint8)
    im = Image.fromarray(img).resize((W, H), Image.BILINEAR)
    He = 140
    can = Image.new("RGB", (W + 60, H + He + 45), (20, 20, 20))
    can.paste(im, (50, 10))
    d = ImageDraw.Draw(can)
    dur = len(x) / sr
    step = 0.01 if dur <= 0.5 else (0.05 if dur <= 1.5 else 0.1)
    teil = 20 if dur <= 0.5 else 4          # Beschriftung alle 0,05 s bzw. 0,25 s
    k = 0
    while k * step <= dur + 1e-9:
        ta = k * step
        px = 50 + int(ta / dur * (W - 1))
        major = abs(ta * teil - round(ta * teil)) < 1e-6
        d.line([(px, 10), (px, 10 + H + He)], fill=(150, 150, 150) if major else (65, 65, 65))
        if major:
            d.text((px - 10, 10 + H + He + 6), "%.2f" % ta, fill=(230, 230, 230))
        k += 1
    for fq in (50, 100, 200, 400, 800, 1600, 3200, 6400):
        py = 10 + int((np.log(fmax) - np.log(fq)) / (np.log(fmax) - np.log(fmin)) * H)
        d.line([(45, py), (50 + W, py)], fill=(60, 120, 60))
        d.text((2, py - 6), str(fq), fill=(150, 220, 150))
    # Huellkurve 10 ms in dBFS
    h = int(0.01 * sr)
    n = max(1, len(x) // h)
    r = np.sqrt(np.mean(x[:n * h].reshape(n, h) ** 2, axis=1) + 1e-14)
    y0 = 10 + H + 5
    pts = []
    for j, rv in enumerate(r):
        px = 50 + int((j + 0.5) / n * (W - 1))
        py = y0 + int(min(60.0, -db(rv)) / 60.0 * (He - 10))
        pts.append((px, py))
    for lv in (-6, -12, -20, -30, -40, -50):
        py = y0 + int(-lv / 60.0 * (He - 10))
        d.line([(50, py), (50 + W, py)], fill=(50, 50, 85))
        d.text((10, py - 6), "%d" % lv, fill=(150, 150, 220))
    if len(pts) > 1:
        d.line(pts, fill=(255, 220, 80))
    d.text((60, 12), titel, fill=(255, 255, 255))
    can.save(pfad)


def main():
    out = AUS_VORGABE
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    mit_bildern = "--keine-bilder" not in sys.argv
    os.makedirs(out, exist_ok=True)
    roh = {}
    zeilen = []
    for t in TOENE:
        if t["datei"] not in roh:
            roh[t["datei"]] = lese(os.path.join(ROH, t["datei"]))
        x, sr = roh[t["datei"]]
        a, b = int(round(t["von"] * sr)), int(round(t["bis"] * sr))
        if not (0 <= a < b <= len(x)):
            raise SystemExit("%s: Ausschnitt ausserhalb der Datei" % t["name"])
        # 0,3 s Rand zu beiden Seiten mitnehmen, damit Filter und Sperre am Schnitt eingeschwungen sind
        r = int(round(0.3 * sr))
        a0, b0 = max(0, a - r), min(len(x), b + r)
        seg = x[a0:b0]
        info = []
        if t.get("entclip"):
            seg, laeufe, ersetzt = entclippe(seg)
            info.append("Vollaussteuerung: %d Lauf/Laeufe, %d Abtastwerte ersetzt" % (laeufe, ersetzt))
        if t.get("oberton"):
            seg, gesp, nfr = obertonsperre(seg, sr)
            info.append("Obertonsperre in %d von %d Fenstern" % (gesp, nfr))
        y = filtere_und_taste(seg, sr, SR_AUS, t["hp"], t["tp"])
        sa = int(round((a - a0) * SR_AUS / sr))
        sb = sa + int(round((b - a) * SR_AUS / sr))
        y = y[sa:sb]
        y = blende(y, SR_AUS, t["ein"], t["aus"])
        pegel = rms95(y, SR_AUS)
        spitze = float(np.max(np.abs(y)))
        gain = 10 ** (t["ziel"] / 20.0) / max(pegel, 1e-12)
        gedeckelt = False
        if spitze * gain > 10 ** (SPITZE_MAX_DB / 20.0):
            gain = 10 ** (SPITZE_MAX_DB / 20.0) / spitze
            gedeckelt = True
        y = y * gain
        samen = zlib.crc32(t["name"].encode("ascii"))
        pfad = os.path.join(out, t["name"] + ".wav")
        q = schreibe(pfad, y, SR_AUS, samen)
        qf = q.astype(np.float64) / 32768.0
        sp, pg = float(np.max(np.abs(qf))), rms95(qf, SR_AUS)
        rand_ms = int(0.002 * SR_AUS)
        kante = max(abs(int(q[0])), abs(int(q[-1])))
        kante2 = max(int(np.max(np.abs(q[:rand_ms]))), int(np.max(np.abs(q[-rand_ms:]))))
        zeile = dict(name=t["name"], datei=t["datei"], von=t["von"], bis=t["bis"], dauer=len(q) / SR_AUS,
                     spitze=db(sp), rms95=db(pg), ziel=t["ziel"], gedeckelt=gedeckelt,
                     verstaerkung=db(gain), kante=kante, kante2=kante2, info=info, notiz=t["notiz"],
                     hp=t["hp"], tp=t["tp"], ein=t["ein"], aus=t["aus"])
        zeilen.append(zeile)
        print("%-14s %s %6.2f-%6.2f s  %.2f s  Spitze %5.1f dBFS  rms95 %5.1f dBFS (Ziel %5.1f%s)  "
              "Verst. %+5.1f dB  Rand: erster/letzter Wert %d LSB, erste/letzte 2 ms max %d LSB  %s" % (
                  t["name"], t["datei"], t["von"], t["bis"], zeile["dauer"], zeile["spitze"], zeile["rms95"],
                  t["ziel"], ", Spitze gedeckelt" if gedeckelt else "", zeile["verstaerkung"], kante, kante2,
                  "; ".join(info)))
        if mit_bildern:
            titel = "%s  <- %s %.2f-%.2f s  |  %.2f s  Spitze %.1f dBFS  rms95 %.1f dBFS" % (
                t["name"], t["datei"], t["von"], t["bis"], zeile["dauer"], zeile["spitze"], zeile["rms95"])
            bild(q, SR_AUS, titel, os.path.join(BILDER, "schnitt_%s.png" % t["name"]))
    return zeilen


if __name__ == "__main__":
    main()
