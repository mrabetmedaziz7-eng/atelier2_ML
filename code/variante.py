import sys
from classifieur import CONSIGNE_EXEMPLES
from evaluer import charger, evaluer

if __name__ == "__main__":
    modele = sys.argv[1] if len(sys.argv) > 1 else "openai/gpt-oss-120b"
    print(f"Évaluation de la variante few-shot sur le modèle : {modele}")
    evaluer(modele, charger(),
            consigne=CONSIGNE_EXEMPLES,
            etiquette=f"{modele.split('/')[-1]} + 4 exemples")
