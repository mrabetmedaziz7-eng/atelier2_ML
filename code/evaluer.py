import csv, json, re, sys, time
from pathlib import Path
from classifieur import CONSIGNE, classer
from evaluation import afficher_rapport

PAUSE = 2.1
RACINE = Path(__file__).resolve().parent.parent

def charger(chemin=RACINE / "data" / "tickets.csv"):
    with open(chemin, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def evaluer(modele, lignes, consigne=CONSIGNE, etiquette=None):
    etiquette = etiquette or modele
    vrais, predits = [], []
    latences_appels = []
    debut_total = time.time()
    
    total = len(lignes)
    print(f"Démarrage de l'évaluation pour : {etiquette} ({total} tickets)")
    
    for idx, ligne in enumerate(lignes, 1):
        t0 = time.time()
        p = classer(ligne["texte"], modele, consigne=consigne)
        lat = time.time() - t0
        latences_appels.append(lat)
        predits.append(p)
        vrais.append(ligne["categorie"])
        print(f"[{idx}/{total}] Ticket {ligne['id']} -> Prédit: {p:<12} (Vérité: {ligne['categorie']:<12}) en {lat:.2f}s", flush=True)
        time.sleep(PAUSE)
        
    duree_totale = round(time.time() - debut_total, 1)
    duree_appels_seuls = round(sum(latences_appels), 1)
    
    print("\n" + "=" * 50)
    resume = afficher_rapport(etiquette, vrais, predits)
    resume.update(
        modele=modele,
        etiquette=etiquette,
        duree_s=duree_totale,
        latence_appels_s=duree_appels_seuls,
        latence_moyenne_ms=round((duree_appels_seuls / total) * 1000, 1) if total else 0,
        vrais=vrais,
        predits=predits,
        ids=[l["id"] for l in lignes]
    )

    dossier = RACINE / "resultats"
    dossier.mkdir(exist_ok=True)
    nom = re.sub(r"[^\w.-]+", "_", etiquette)       # "/" et espaces -> "_"
    sortie = dossier / f"{nom}.json"
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)
    print(f"\nRésultats enregistrés dans : {sortie}")
    print(f"Durée totale : {duree_totale}s (dont appels API seuls : {duree_appels_seuls}s, pauses : {round(total*PAUSE, 1)}s)")
    return resume

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluer.py <nom_modele> [etiquette]")
        sys.exit(1)
    etiquette = sys.argv[2] if len(sys.argv) > 2 else None
    evaluer(sys.argv[1], charger(), etiquette=etiquette)
