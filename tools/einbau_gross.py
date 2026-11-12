# Einbau grosser Baer (Laeufe baer-gross + baer-kopfnaht: neues Aufrichten/Bruellen, sauberer Uebergang Kopf->Nacken) in NCBearTest: 5 Modell-Dateien.
# Bricht ab, wenn das Spiel laeuft; Zip vorher/nachher nach Zomboid/backups/NCBearTest/, MD5 nachzaehlen. Nie loeschen.
import os, sys, zipfile, hashlib, shutil, subprocess, datetime
MOD = "C:/Users/Kevin/Zomboid/mods/NCBearTest"
SRC = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_kopfnaht/mod"
LISTE = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_kopfnaht/staging_dateien.txt"
BAK = "C:/Users/Kevin/Zomboid/backups/NCBearTest"
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
def zippen(name):
    with zipfile.ZipFile(os.path.join(BAK, name), "w", zipfile.ZIP_DEFLATED) as z:
        n = 0
        for w, ds, fs in os.walk(MOD):
            for f in fs:
                p = os.path.join(w, f); z.write(p, os.path.relpath(p, os.path.dirname(MOD))); n += 1
    with zipfile.ZipFile(os.path.join(BAK, name)) as z:
        assert z.testzip() is None
    print("Zip", name, n, "Dateien")
if "projectzomboid" in subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower():
    print("ABBRUCH: Spiel laeuft"); sys.exit(2)
liste = []
for z in open(LISTE, encoding="utf-8"):
    if not z.strip() or z.startswith("#"):
        continue
    t = [x.strip() for x in z.split("|")]
    p, m = "42/media/" + t[0], t[1]
    assert md5(os.path.join(SRC, p)) == m, p
    assert os.path.isfile(os.path.join(MOD, p)), "Ziel fehlt: " + p
    liste.append((p, m))
assert len(liste) == 5, len(liste)
st = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
zippen("NCBearTest_vor_gross_%s.zip" % st)
for p, m in liste:
    shutil.copyfile(os.path.join(SRC, p), os.path.join(MOD, p))
ok = all(md5(os.path.join(MOD, p)) == m for p, m in liste)
zippen("NCBearTest_mit_gross_%s.zip" % datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
print("ERGEBNIS", "OK" if ok else "FEHLER", len(liste), "Dateien")
