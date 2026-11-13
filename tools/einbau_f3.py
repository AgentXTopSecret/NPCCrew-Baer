# Einbau eines fertigen Staging-Stands in die Test-Mod NCBearTest (Vorlage einbau_look.py; diese Fassung: F3 Beduerfnisse, Schlaf, Vertrauen, Fenster B, Herz).
# Arten in der Liste: gleich | neu[ (Testhilfe ...)] | ueberschreibt[ (Stummel ...)|(Testhilfe ...)] | ueberschreibt (NICHT KOPIEREN ...) = uebersprungen |
#   ueberschreibt (nur kopieren, wenn die Test-Mod-Datei noch MD5 <8 Zeichen> hat ...) = nur dann, sonst Abbruch.
# --baer-nicht-geladen: Spiel laeuft, aber der geladene Spielstand hat NCBearTest nicht (von Hand in console.txt geprueft, CLAUDE.md 5).
import os, sys, zipfile, hashlib, shutil, subprocess, datetime
MOD = "C:/Users/Kevin/Zomboid/mods/NCBearTest"
SRC = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/mod_f3"
LISTE = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/f3/staging_dateien_f3.txt"
BAK = "C:/Users/Kevin/Zomboid/backups/NCBearTest"


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def zippen(name):
    ziel = os.path.join(BAK, name)
    n = 0
    with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as z:
        for w, ds, fs in os.walk(MOD):
            for f in fs:
                p = os.path.join(w, f)
                z.write(p, os.path.relpath(p, os.path.dirname(MOD)))
                n += 1
    with zipfile.ZipFile(ziel) as z:
        assert z.testzip() is None
    print("Zip", name, n, "Dateien")


t = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
if "projectzomboid" in t and "--baer-nicht-geladen" not in sys.argv:
    print("ABBRUCH: Spiel laeuft")
    sys.exit(2)

eintraege = []
for zeile in open(LISTE, encoding="utf-8"):
    zeile = zeile.strip()
    if not zeile or zeile.startswith("#"):
        continue
    teile = [x.strip() for x in zeile.split("|")]
    if len(teile) != 4:
        continue
    pfad, m, groesse, art = teile[0], teile[1], int(teile[2]), teile[3]
    NIE = ("NCBear.glb", "NCBear.png", "NCBearGen.glb", "NCBearGen.png", "NCBearGenFoto.png", "NCBearCub.glb", "NCBearCub.png")
    if os.path.basename(teile[0]) in NIE and not teile[3].strip().startswith("gleich"):
        print("uebersprungen (Modell, Maul-Lauf):", teile[0])
        continue
    if pfad.startswith(("42/media/models_X/", "42/media/textures/", "42/media/AnimSets/")) and not art.startswith("gleich"):
        print("uebersprungen (Modell-Datei):", pfad)
        continue
    if "NICHT KOPIEREN" in art:
        print("uebersprungen (NICHT KOPIEREN):", pfad)
        continue
    q = os.path.join(SRC, pfad)
    assert os.path.isfile(q), "Quelle fehlt: " + pfad
    assert md5(q) == m and os.path.getsize(q) == groesse, "Quelle weicht von der Liste ab: " + pfad
    z = os.path.join(MOD, pfad)
    if art.startswith("neu"):
        assert not os.path.exists(z), "als neu gefuehrt, liegt aber schon da: " + pfad
        art = "neu"
    elif art.startswith("gleich"):
        art = "gleich"
        assert md5(z) == m, "als gleich gefuehrt, ist aber anders: " + pfad
    elif False:
        assert md5(z) == m, "als gleich gefuehrt, ist aber anders: " + pfad
    else:
        assert art.startswith("ueberschreibt") and os.path.isfile(z), "Ziel fehlt: " + pfad
        if "nur kopieren, wenn die Test-Mod-Datei noch MD5" in art:
            soll = art.split("noch MD5 ")[1][:8]
            assert md5(z).startswith(soll), "bedingte Datei hat sich geaendert (" + md5(z)[:8] + " statt " + soll + "): " + pfad
        name = os.path.basename(pfad)
        assert (not name.startswith("NCBear")) or name.startswith("NCBearBench") or "Stummel" in art or "Testhilfe" in art,             "ueberschreibt eine alte NCBear-Datei: " + pfad
        art = "ueberschreibt"
    eintraege.append((pfad, m, art))
print("Liste:", len(eintraege), "Dateien,",
      sum(1 for e in eintraege if e[2] == "neu"), "neu,",
      sum(1 for e in eintraege if e[2] == "ueberschreibt"), "ueberschreibt,",
      sum(1 for e in eintraege if e[2] == "gleich"), "gleich")

st = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
zippen("NCBearTest_vor_f3_%s.zip" % st)
ok = True
for pfad, m, art in eintraege:
    if art == "gleich":
        continue
    z = os.path.join(MOD, pfad)
    os.makedirs(os.path.dirname(z), exist_ok=True)
    shutil.copyfile(os.path.join(SRC, pfad), z)
for pfad, m, art in eintraege:
    g = md5(os.path.join(MOD, pfad)) == m
    ok = ok and g
    if not g:
        print("UNGLEICH", pfad)
zippen("NCBearTest_mit_f3_%s.zip" % datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
print("ERGEBNIS", "OK" if ok else "FEHLER", len(eintraege), "Dateien nachgezaehlt")
