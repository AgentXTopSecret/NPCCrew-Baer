# Einbau eines fertigen Staging-Stands in die Test-Mod NCBearTest (Vorlage: Einbau F1 am 12.11.2026 04:04).
# Fuer einen neuen Stand SRC, LISTE und die Zip-Namen (vor_f1 / mit_f1) anpassen. Bricht ab, wenn das Spiel laeuft.
# Prueft: neu = darf noch nicht da sein, gleich = muss gleich sein, ueberschreibt = nie eine alte NCBear*-Datei ausser NCBearBench*.
# Danach: mod.info + 42/mod.info description= ersetzen (LF), Trockenlauf tools/baer_uebernahme.py --vor-b5a, sichern.py, Commit+Push.
import os, sys, zipfile, hashlib, shutil, subprocess, datetime
MOD = "C:/Users/Kevin/Zomboid/mods/NCBearTest"
SRC = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/mod_f1_fertig"
LISTE = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_zaehmen/staging_dateien_f1.txt"
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
if "projectzomboid" in t:
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
    q = os.path.join(SRC, pfad)
    assert os.path.isfile(q), "Quelle fehlt: " + pfad
    assert md5(q) == m and os.path.getsize(q) == groesse, "Quelle weicht von der Liste ab: " + pfad
    z = os.path.join(MOD, pfad)
    if art == "neu":
        assert not os.path.exists(z), "als neu gefuehrt, liegt aber schon da: " + pfad
    elif art == "gleich":
        assert md5(z) == m, "als gleich gefuehrt, ist aber anders: " + pfad
    else:
        assert art == "ueberschreibt" and os.path.isfile(z), "Ziel fehlt: " + pfad
        assert not os.path.basename(pfad).startswith("NCBear") or os.path.basename(pfad).startswith("NCBearBench"), \
            "ueberschreibt eine alte NCBear-Datei: " + pfad
    eintraege.append((pfad, m, art))
print("Liste:", len(eintraege), "Dateien,",
      sum(1 for e in eintraege if e[2] == "neu"), "neu,",
      sum(1 for e in eintraege if e[2] == "ueberschreibt"), "ueberschreibt,",
      sum(1 for e in eintraege if e[2] == "gleich"), "gleich")

st = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
zippen("NCBearTest_vor_f1_%s.zip" % st)
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
zippen("NCBearTest_mit_f1_%s.zip" % datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
print("ERGEBNIS", "OK" if ok else "FEHLER", len(eintraege), "Dateien nachgezaehlt")
