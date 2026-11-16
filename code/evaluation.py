CATEGORIES = ["facturation", "technique", "compte", "commercial"]

def accuracy(vrais, predits):
    if not vrais:
        return 0.0
    return sum(1 for v, p in zip(vrais, predits) if v == p) / len(vrais)

def scores_par_classe(vrais, predits, classes=CATEGORIES):
    resultat = {}
    for c in classes:
        vp = sum(1 for v, p in zip(vrais, predits) if v == c and p == c)
        fp = sum(1 for v, p in zip(vrais, predits) if v != c and p == c)
        fn = sum(1 for v, p in zip(vrais, predits) if v == c and p != c)
        precision = vp / (vp + fp) if (vp + fp) else 0.0
        recall = vp / (vp + fn) if (vp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) else 0.0)
        resultat[c] = {"precision": precision, "recall": recall,
                       "f1": f1, "support": vp + fn}
    return resultat

def f1_macro(scores):
    if not scores:
        return 0.0
    return sum(d["f1"] for d in scores.values()) / len(scores)

def taux_invalides(predits):
    if not predits:
        return 0.0
    return sum(1 for p in predits if p == "invalide") / len(predits)

def matrice_confusion(vrais, predits, classes=CATEGORIES):
    colonnes = classes + ["invalide"]
    m = {v: {p: 0 for p in colonnes} for v in classes}
    for v, p in zip(vrais, predits):
        if v in m and p in m[v]:
            m[v][p] += 1
        elif v in m:
            m[v]["invalide"] += 1
    return m

def afficher_rapport(etiquette, vrais, predits):
    acc = accuracy(vrais, predits)
    scores = scores_par_classe(vrais, predits)
    f1m = f1_macro(scores)
    inv = taux_invalides(predits)
    mat = matrice_confusion(vrais, predits)

    print(f"=== {etiquette} ===")
    print(f"accuracy : {acc:.3f}")
    print(f"macro-F1 : {f1m:.3f}")
    print(f"invalides : {inv:.3f}\n")
    print(f"{'categorie':<13}{'precision':>10}{'recall':>8}{'F1':>8}{'n':>4}")
    for c, d in scores.items():
        print(f"{c:<13}{d['precision']:>10.3f}{d['recall']:>8.3f}"
              f"{d['f1']:>8.3f}{d['support']:>4}")
    print("\nConfusion matrix (lignes = vérité, colonnes = prédiction)")
    cols = CATEGORIES + ["invalide"]
    print(" " * 13 + "".join(f"{c[:6]:>7}" for c in cols))
    for v in CATEGORIES:
        print(f"{v:<13}" + "".join(f"{mat[v][c]:>7}" for c in cols))

    return {"accuracy": acc, "macro_f1": f1m, "taux_invalides": inv,
            "scores": scores, "matrice": mat}
