# Lauf baer-gen-gross (11.11.2026), Rolle BAU FORM + TEXTUR: der neue grosse Baer E (Bild-zu-3D-Generator) in die RUHELAGE des 2c-Skeletts.
# Kopie-Abwandlung von baer_form_rig.py (Original unveraendert). Teile:
#   plan    -- gg_plan.py (Umstellung am Spielnetz E_schoen, tier-Meter): Massstab s 1,70 / dx 0,033, Rumpf quer q(x), Vorderkoerper vor,
#              Kopf STARR in die 2c-Kopflage + Hals als Kette, Kehle, Beine auf die 2c-Beinachsen -> form/f2/plan.json/.npz + Vorschau
#   param   -- rechnet die Parameter der bewaehrten Kette um (E_form_v9.json -> form/E_form_ruhe.json, E_tex_final/_fototon.json ->
#              form/E_tex_ruhe_braun.json / _foto.json): Kopfpunkte mit der starren Kopf-Trafo, Welt-Regionen mit der Verformung,
#              Pfoten neu am 2c-Fussabdruck, linke Seite (Fotoseite) ist Spiegel-Quelle
#   abgabe  -- R/form/werkzeug/gg_abgabe.py (Maul aus baer_maul_gengross.py, Masken, vorlaeufige Gewichte, Flecken in beide Texturen,
#              E_gen_basis.npz/.glb/.png), dann gg_maul_probe.py, gg_kontakt.py (Kontakt-Vorprobe), gg_pruef.py (pruef_form.json, landmarken_gen.json)
# Rahmen: "bl" Blender-roh der Generator-Kette (vorn = -Y), "tm" tier-Meter bei Groesse 1,0 (2c-Rahmen). gg_lib.py: tm = (1,70*(-by) + 0,033,
# 1,70*(bx + 0,0131), 1,70*(bz + 0,34443)).
# Aufruf: python baer_form_gengross.py plan <cfg.json> [vorschau.png] | param [param_cfg.json]
import json, sys, os, subprocess, math
import numpy as np

R = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen_gross/"
GEN = "C:/Users/Kevin/NPCCrew-Nebenprojekte/_arbeit/baer_gen/"
WZ = R + "form/werkzeug/"
sys.path.insert(0, WZ)
from gg_lib import bl2tm, tm2bl, blv2tm, tmv2bl, YM, ZB, S, DX, jdump   # noqa: E402

VORGABE = {
    "form_param": GEN + "nachbesserung/E_form_v9.json",
    "tex_braun": GEN + "nachbesserung/E_tex_final.json",
    "tex_foto": GEN + "nachbesserung/E_tex_fototon.json",
    "form_info_foto": GEN + "nachbesserung/form/E_v9/form_info.json",
    "L_fest": 0.9952,
    # Pfoten (tier-Meter): Achse auf Schnitthoehe = 2c-Beinachse; Masse so, dass der 2c-Fussabdruck herauskommt (vorn 28,5 x 20,
    # hinten 29 x 19,6 cm); Werte in roh (Generator-Einheit) wie form2 sie liest
    "pfote_z_achse_m": 0.135,
    "pfote_vorn": {"sohle_len": 0.092, "sohle_rx": 0.055, "zehen_rx": 0.058, "radien": [0.052, 0.049]},
    "pfote_hinten": {"sohle_len": 0.107, "sohle_rx": 0.054, "zehen_rx": 0.058, "radien": [0.054, 0.047]},
    "farbe_z_spiegel_m": 0.62,
    "glatt_ende": {},
    "naht": 0.04,
    "ziel_dreiecke": 19500,
}


def lade_cfg():
    c = dict(VORGABE)
    if len(sys.argv) > 2 and sys.argv[1] == "param":
        c.update(json.load(open(sys.argv[2], encoding="utf-8")))
    return c


def param():
    CFG = lade_cfg()
    from gg_verf import Verf
    VF = Verf()
    PFJ = json.load(open(CFG["form_param"], encoding="utf-8"))
    P2 = json.loads(json.dumps(PFJ))
    P2.update({"name": "E_form", "glb": R + "form/f2/raw_ruhe_form.glb", "aus": R + "form/f2/form_ruhe", "dreh_z": 0.0, "L_fest": CFG["L_fest"]})
    # Kopfpunkte starr (alle liegen im starren Kopf)
    for k in ("kopf_mitte", "schnauze", "auge_l", "auge_r", "nase"):
        P2[k] = VF.kopf_bl(PFJ[k])[0].round(5).tolist()
    # Augen als Spiegelpaar um die Mittelebene (auge_r = Fotoseite links; sonst kippt der Kopfrahmen vor dem Spiegeln um 7 Grad)
    ar = np.array(P2["auge_r"]); P2["auge_l"] = [round(float(2 * YM - ar[0]), 5), float(ar[1]), float(ar[2])]
    for k in ("kopf_mitte", "schnauze", "nase"):
        P2[k][0] = YM
    # alte Ohren, Welt-Regionen, Flicken: Mittelpunkt mit der vollen Verformung (liegen an der Kopf/Hals-Grenze bzw. am Rumpf)
    for nm, oh in P2["alte_ohren"].items():
        oh["mitte"] = VF.bl(PFJ["alte_ohren"][nm]["mitte"])[0].round(5).tolist()
    for grp in ("regionen", "regionen_nach", "regionen_ende"):
        for nm, re in P2.get(grp, {}).items():
            if not re.get("kopfrahmen"):
                re["mitte"] = VF.bl(re["mitte"])[0].round(5).tolist()
    for fk in P2.get("flicken", []):
        if not fk.get("kopfrahmen"):
            fk["mitte"] = VF.bl(fk["mitte"])[0].round(5).tolist()
    # Kopf-Mittelebene = Koerper-Mittelebene (Blender x = YM), Augenmitte aus der starren Kopf-Trafo
    am = 0.5 * (np.array(P2["auge_l"]) + np.array(P2["auge_r"]))
    P2["spiegel"]["normale_fest"] = [1.0, 0.0, 0.0]; P2["spiegel"]["ebene_fest"] = [YM, float(am[1]), float(am[2])]
    P2["koerper_spiegel"] = {"x_mitte": YM, "naht": CFG["naht"], "quelle": "links", "naht_sym": True}
    # Stummel auf die Mittelebene
    P2["stummel"]["x"] = YM
    # Pfoten am 2c-Fussabdruck (Achse 2c auf Schnitthoehe), links = Quelle, rechts gespiegelt
    A2 = json.load(open(R + "form/mess/achsen_2c.json"))
    za = CFG["pfote_z_achse_m"]
    liste = []
    for nm, art in (("VL", "vorn"), ("HL", "hinten")):
        s2c = np.array(A2[nm]["schnitte"]); cx = np.interp(za, s2c[:, 2], s2c[:, 0]); cy = np.interp(za, s2c[:, 2], s2c[:, 1])
        b = tm2bl(np.array([[cx, cy, 0.0]]))[0]
        pf = CFG["pfote_" + art]
        for nm2, bx in ((nm, b[0]), (nm[0] + "R", 2 * YM - b[0])):
            liste.append({"name": nm2, "xy": [round(float(bx), 5), round(float(b[1]), 5)], "art": art, "boden": ZB,
                          "bein": [round(float(bx), 5), round(float(b[1]), 5)], "radien": pf["radien"], "sohle_len": pf["sohle_len"],
                          "sohle_rx": pf["sohle_rx"], "zehen_rx": pf["zehen_rx"]})
    P2["pfoten"]["liste"] = liste
    P2["pfoten"]["fuss_spiegel"] = {"x_mitte": YM, "paare": {"VR": "VL", "HR": "HL"}, "quelle": "links"}
    P2["glatt_ende"] = CFG["glatt_ende"]
    if CFG.get("glaetten_je_bein_extra"):
        P2["pfoten"]["glaetten_je_bein"] = P2["pfoten"]["glaetten_je_bein"] + CFG["glaetten_je_bein_extra"]
    jdump(P2, R + "form/E_form_ruhe.json")
    # ---- Textur-Parameter (beide Farben aus EINER Form; Netz/UV gleich: gleiche saat + gleiche Form)
    for farbe, key in (("braun", "tex_braun"), ("foto", "tex_foto")):
        TP = json.load(open(CFG[key], encoding="utf-8"))
        T2 = json.loads(json.dumps(TP))
        T2.update({"name": "E_gen_" + farbe, "form_info": R + "form/f2/form_ruhe/form_info.json", "dicht": R + "form/f2/form_ruhe/E_form_dicht.npz",
                   "aus": R + "form/f2/tex_" + farbe, "renderordner": R + "form/f2/tex_" + farbe + "/einzel", "hoch_glb": R + "form/f2/raw_ruhe_tex.glb",
                   "L_fest": CFG["L_fest"], "ziel_dreiecke": CFG["ziel_dreiecke"]})
        if TP.get("nacken_weich"):
            T2["nacken_weich"]["mitte"] = VF.bl(TP["nacken_weich"]["mitte"])[0].round(5).tolist()
        for hk in T2.get("heck_fuellen", []):
            if hk["mitte"] != "stummel":
                hk["mitte"] = VF.bl(hk["mitte"])[0].round(5).tolist()
        for fd in T2.get("flecken_daempfen", []):
            for rg in fd.get("regionen", []):
                rg["mitte"] = VF.bl(rg["mitte"])[0].round(5).tolist()
        for k, v in CFG.get("tex_extra", {}).items():
            T2[k] = v
        for k, v in CFG.get("tex_anhaengen", {}).items():       # Listen verlaengern (z. B. flecken_daempfen)
            T2[k] = list(T2.get(k, [])) + list(v)
        for v in CFG.get("tex_malen_regionen_dazu", []):
            T2["malen"].setdefault("regionen", []).append(v)
        jdump(T2, R + "form/E_tex_ruhe_%s.json" % farbe)
    print("param fertig: E_form_ruhe.json, E_tex_ruhe_braun.json, E_tex_ruhe_foto.json")


if __name__ == "__main__":
    mod = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if mod == "plan":
        rc = subprocess.call([sys.executable, WZ + "gg_plan.py"] + sys.argv[2:])
        sys.exit(rc)
    elif mod == "param":
        param()
    elif mod == "abgabe":
        for sk in ("gg_abgabe.py", "gg_maul_probe.py", "gg_kontakt.py", "gg_pruef.py"):
            rc = subprocess.call([sys.executable, WZ + sk], cwd=WZ)
            if rc:
                sys.exit(rc)
