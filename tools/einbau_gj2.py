# Einbau Lauf baer-gen-junges-v2 (Generator-Junges v2, NUR Testhilfe NCBearBench*: NCBear_CubGen()) in NCBearTest: 5 neue Dateien.
# Bricht ab, wenn das Spiel laeuft; Zip vorher/nachher nach Zomboid/backups/NCBearTest/, MD5 nachzaehlen. Nur hinzufuegen, nie loeschen.
import os, sys, zipfile, hashlib, shutil, subprocess, datetime
MOD = "C:/Users/Kevin/Zomboid/mods/NCBearTest"
V2 = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_junges/v2"
LISTE = V2 + "/staging_dateien.txt"
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
# --baer-nicht-geladen: Spiel laeuft, aber der geladene Spielstand hat NCBearTest nicht (console.txt von Hand geprueft, CLAUDE.md 5).
if "projectzomboid" in subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower() and "--baer-nicht-geladen" not in sys.argv:
    print("ABBRUCH: Spiel laeuft"); sys.exit(2)
out_md5 = {}
for z in open(V2 + "/out/md5.txt", encoding="utf-8"):
    m, p = z.strip().split(" *"); out_md5[p] = m
liste = []
for z in open(LISTE, encoding="utf-8"):
    if not z.strip() or z.startswith("#"):
        continue
    t = [x.strip() for x in z.split("|")]
    p, m, art, quelle = t[0], t[1], t[3], t[4]
    assert art == "neu", p
    q = quelle if quelle.endswith(os.path.basename(p)) else os.path.join(quelle, p)
    if not os.path.isfile(q):
        q = os.path.join(V2, "mod", p) if os.path.isfile(os.path.join(V2, "mod", p)) else os.path.join(V2, "out", p)
    assert os.path.isfile(q), "Quelle fehlt: " + p
    assert md5(q) == m, "Quelle weicht ab: " + p
    if p in out_md5:
        assert out_md5[p] == m, "md5.txt weicht ab: " + p
    assert not os.path.exists(os.path.join(MOD, p)), "liegt schon da: " + p
    assert os.path.basename(p).startswith("NCBearBench"), "keine Testhilfe: " + p
    liste.append((p, m, q))
assert len(liste) == 5, len(liste)
st = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
zippen("NCBearTest_vor_gj2_%s.zip" % st)
for p, m, q in liste:
    os.makedirs(os.path.dirname(os.path.join(MOD, p)), exist_ok=True)
    shutil.copyfile(q, os.path.join(MOD, p))
ok = all(md5(os.path.join(MOD, p)) == m for p, m, q in liste)
zippen("NCBearTest_mit_gj2_%s.zip" % datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
print("ERGEBNIS", "OK" if ok else "FEHLER", len(liste), "Dateien")
