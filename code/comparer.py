import json
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent.parent / "resultats"
fichiers = sorted(DOSSIER.glob("*.json"))

if not fichiers:
    print(f"Aucun résultat trouvé dans {DOSSIER}")
    exit(0)

res = [json.load(open(p, encoding="utf-8")) for p in fichiers]

print("=" * 85)
print("COMPARAISON DES MODÈLES")
print("=" * 85)
print(f"{'Modèle':<35}{'Accuracy':>9}{'Macro-F1':>10}{'Invalides':>10}{'Durée (s)':>11}{'API seul(s)':>10}")
print("-" * 85)
for r in sorted(res, key=lambda r: -r["macro_f1"]):
    lat_api = r.get("latence_appels_s", "-")
    print(f"{r['etiquette']:<35}{r['accuracy']:>9.3f}{r['macro_f1']:>10.3f}"
          f"{r['taux_invalides']:>10.3f}{r['duree_s']:>11}{str(lat_api):>10}")

print("\n" + "=" * 85)
print("DÉSACCORDS ENTRE MODÈLES")
print("=" * 85)
ids = res[0]["ids"]
vrais = res[0]["vrais"]

nb_desaccords = 0
for i, tid in enumerate(ids):
    preds = {r["etiquette"]: r["predits"][i] for r in res}
    if len(set(preds.values())) > 1:
        nb_desaccords += 1
        vrai = vrais[i]
        detail = " | ".join(f"{k} = {v}" for k, v in preds.items())
        print(f"{tid} (vérité : {vrai}) : {detail}")

print(f"\nTotal des tickets avec désaccord : {nb_desaccords} / {len(ids)}")
