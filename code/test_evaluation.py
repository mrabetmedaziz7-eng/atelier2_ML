from evaluation import (
    accuracy,
    scores_par_classe,
    f1_macro,
    taux_invalides,
    matrice_confusion,
    afficher_rapport,
)

vrais = ["compte", "technique", "compte", "commercial"]
predits = ["compte", "technique", "commercial", "commercial"]

print("Accuracy :", accuracy(vrais, predits))
scores = scores_par_classe(vrais, predits)
print("Scores :", scores)
print("Macro-F1 :", f1_macro(scores))
print("Taux invalides :", taux_invalides(predits))
print("Matrice :", matrice_confusion(vrais, predits))
print("\nRapport complet :")
afficher_rapport("Test synthétique", vrais, predits)
