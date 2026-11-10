"""Bild -> 3D-Rohmodell (GLB) mit TRELLIS.2 ueber einen LOKAL laufenden ComfyUI-Server (127.0.0.1:8188).

Nur Standardbibliothek. Der Server muss schon laufen (siehe _arbeit/baer_gen/PROBELAUF.md, "Wiederholen").
Ablauf: Bild nach ComfyUI/input kopieren -> Ablauf (trellis2_ablauf_api.json daneben) anpassen -> POST /prompt
-> /history abfragen bis fertig -> GLB (+ Eingangsbild, Maske, Basisfarbe) in den Zielordner kopieren.
Waehrenddessen wird alle 2 s nvidia-smi abgefragt (hoechster belegter Grafikspeicher der ganzen Karte).

Beispiel:
  python gen_trellis.py --bild A_zuschnitt.png --name A_roh --aus C:/.../_arbeit/baer_gen/aus
  python gen_trellis.py --bild A_frei.png --name A_frei --ohne-entferner --aufloesung 1024
"""
import argparse, json, os, shutil, subprocess, sys, time, urllib.request, uuid

HIER = os.path.dirname(os.path.abspath(__file__))
COMFY = r"C:\Users\Kevin\Tools\ComfyUI\ComfyUI_windows_portable\ComfyUI"
SERVER = "http://127.0.0.1:8188"


def hole(pfad):
    with urllib.request.urlopen(SERVER + pfad, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def schicke(pfad, daten):
    req = urllib.request.Request(SERVER + pfad, data=json.dumps(daten).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("FEHLER vom Server:", e.read().decode("utf-8", "replace"))
        raise


def vram_mib():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=10).stdout
        return int(out.strip().splitlines()[0])
    except Exception:
        return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bild", required=True)
    ap.add_argument("--name", required=True, help="Name des Ergebnisses, z. B. A_roh")
    ap.add_argument("--aus", required=True, help="Zielordner fuer GLB und Bilder")
    ap.add_argument("--aufloesung", type=int, default=1536, help="Trellis2UpsampleStage target_resolution (1024..2048)")
    ap.add_argument("--seed", type=int, default=None, help="versetzt alle vier Seeds der Vorlage (56/42/42/43) um diesen Wert")
    ap.add_argument("--ohne-entferner", action="store_true", help="BiRefNet aus; Maske = Alpha des PNG")
    ap.add_argument("--textur", type=int, default=4096)
    ap.add_argument("--flaechen", type=int, default=700000, help="DecimateMesh target_face_count")
    ap.add_argument("--ablauf", default=os.path.join(HIER, "trellis2_ablauf_api.json"))
    a = ap.parse_args()

    with open(a.ablauf, encoding="utf-8") as f:
        g = json.load(f)
    eingabe = "baer_" + a.name + os.path.splitext(a.bild)[1]
    shutil.copyfile(a.bild, os.path.join(COMFY, "input", eingabe))
    g["122"]["inputs"]["image"] = eingabe
    g["248"]["inputs"]["switch"] = not a.ohne_entferner
    g["94"]["inputs"]["target_resolution"] = a.aufloesung
    g["196"]["inputs"]["resolution"] = a.textur
    g["147"]["inputs"]["texture_size"] = a.textur
    g["186"]["inputs"]["target_face_count"] = a.flaechen
    if a.seed is not None:
        for nid, s in (("3", 56), ("18", 42), ("23", 42), ("12", 43)):
            g[nid]["inputs"]["seed"] = s + a.seed
    if a.ohne_entferner:  # BiRefNet gar nicht erst laden
        del g["192"], g["193"]
        g["248"]["inputs"]["on_true"] = ["400", 0]
    for nid in g:
        fp = g[nid]["inputs"].get("filename_prefix")
        if fp:
            g[nid]["inputs"]["filename_prefix"] = fp.replace("NAME", a.name)
    seeds = {nid: g[nid]["inputs"]["seed"] for nid in ("3", "18", "23", "12")}
    print("Einstellungen:", json.dumps({"bild": a.bild, "aufloesung": a.aufloesung, "seeds": seeds,
                                        "schritte": {n: g[n]["inputs"]["steps"] for n in seeds},
                                        "entferner": not a.ohne_entferner, "textur": a.textur, "flaechen": a.flaechen}))

    t0 = time.time()
    pid = schicke("/prompt", {"prompt": g, "client_id": str(uuid.uuid4())})["prompt_id"]
    print("prompt_id", pid)
    spitze = vram_mib()
    while True:
        time.sleep(2)
        spitze = max(spitze, vram_mib())
        h = hole("/history/" + pid)
        if pid in h:
            h = h[pid]
            st = h.get("status", {})
            if st.get("completed") or st.get("status_str") in ("success", "error"):
                break
        if time.time() - t0 > 3600:
            print("ABBRUCH: laenger als 60 min")
            sys.exit(2)
    dauer = time.time() - t0
    print("Status:", h["status"].get("status_str"), "Dauer %.1f s" % dauer, "VRAM-Spitze (Karte) %d MiB" % spitze)
    if h["status"].get("status_str") != "success":
        for m in h["status"].get("messages", []):
            if m[0] == "execution_error":
                print(json.dumps(m[1], indent=1)[:4000])
        sys.exit(1)

    os.makedirs(a.aus, exist_ok=True)
    kopiert = []
    for nid, out in h["outputs"].items():
        for art in ("3d", "images", "result"):
            for e in out.get(art, []) or []:
                if not isinstance(e, dict) or "filename" not in e:
                    continue
                q = os.path.join(COMFY, e.get("type", "output"), e.get("subfolder", ""), e["filename"])
                if not os.path.isfile(q):
                    continue
                if q.lower().endswith(".glb"):
                    z = os.path.join(a.aus, a.name + ".glb")
                else:
                    z = os.path.join(a.aus, e["filename"])
                shutil.copyfile(q, z)
                kopiert.append(z)
    for z in kopiert:
        print("kopiert:", z)
    with open(os.path.join(a.aus, a.name + "_lauf.json"), "w", encoding="utf-8") as f:
        json.dump({"name": a.name, "bild": a.bild, "aufloesung": a.aufloesung, "seeds": seeds,
                   "entferner": not a.ohne_entferner, "textur": a.textur, "flaechen": a.flaechen,
                   "dauer_s": round(dauer, 1), "vram_spitze_mib": spitze, "dateien": kopiert}, f, indent=1)


if __name__ == "__main__":
    main()
