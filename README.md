# Atelier 2 : Choisir un modèle sur preuves (Classification de Tickets)
**Machine Learning Appliqué — 3e année DSI**

Ce projet met en place un protocole d'évaluation empirique pour sélectionner un modèle de langage (LLM) adapté au routage automatique de tickets de support client, sur des données réelles et déséquilibrées.

---

## 🎯 Objectif et Métrique de Décision

* **Jeu de données :** 72 tickets annotés manuellement répartis en 4 catégories déséquilibrées :
  * `facturation` : 22 tickets (30.6 %)
  * `technique` : 20 tickets (27.8 %)
  * `compte` : 16 tickets (22.2 %)
  * `commercial` : 14 tickets (19.4 %)
* **Métrique de décision :** **Macro-F1**, choisie *a priori*. L'accuracy est trompeuse car elle privilégie les classes majoritaires et ignore les classes rares (ex. commercial).
* **Règle de décision :** Un modèle n'est déclaré supérieur qu'à partir d'un écart d'au moins **5 tickets** (~7 points de Macro-F1). En-dessous, les modèles sont considérés statistiquement indiscernables.

---

## 📊 Résultats Expérimentaux Réels (API Groq)

| Modèle / Configuration | Accuracy | Macro-F1 | Tickets Corrects | Taux Invalides | Latence API seule | Durée Totale (avec pauses 2.1s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`qwen3.8-27b + 4 exemples`** (Few-Shot) | **0.972** | **0.971** | **70 / 72** | **0.0 %** | 66.3 s | 217.6 s |
| **`qwen/qwen3.8-27b`** (Zero-Shot) | 0.958 | 0.956 | 69 / 72 | 0.0 % | 112.4 s | 263.7 s |
| **`openai/gpt-oss-20b`** (Zero-Shot) | 0.944 | 0.948 | 68 / 72 | 1.4 % (1 tick) | 40.8 s | 192.0 s |
| **`openai/gpt-oss-120b`** (Zero-Shot) | 0.917 | 0.918 | 66 / 72 | 0.0 % | 39.4 s | 190.7 s |

---

## 🔍 Conclusions Clés

1. **Taille vs Performance :** Le grand modèle `gpt-oss-120b` (66/72) ne fait pas mieux que le petit modèle `gpt-oss-20b` (68/72). L'écart est de seulement 2 tickets ($2 < 5$) : le surcoût de calcul du gros modèle n'est donc pas justifié.
2. **Latence réelle :** Le modèle `gpt-oss-20b` est presque **3 fois plus rapide** à répondre que Qwen (40.8 s contre 112.4 s d'appels API cumulés).
3. **Apport du Few-Shot :** L'ajout de 4 exemples concrets bien formulés améliore le modèle Qwen (passage de 69 à 70 tickets corrects, Macro-F1 0.971), montrant que la qualité de la consigne (prompt engineering) est un levier aussi fort que le choix du modèle.

---

## 📁 Arborescence du Projet

```text
atelier2/
├── data/
│   └── tickets.csv                            # Les 72 tickets annotés
├── code/
│   ├── essai.py                               # Test de connectivité API Groq
│   ├── explorer.py                            # Exploration et distribution des classes
│   ├── classifieur.py                         # Client API Groq, JSON strict et retry RateLimit
│   ├── evaluation.py                          # Métriques à la main (accuracy, F1, matrice, etc.)
│   ├── test_classifieur.py                    # Test unitaire du classifieur
│   ├── test_evaluation.py                     # Test unitaire des métriques
│   ├── evaluer.py                             # Script d'évaluation sur tickets.csv
│   ├── comparer.py                            # Tableau comparatif et analyse des désaccords
│   ├── variante.py                            # Variante de consigne Few-Shot (+4 exemples)
│   └── generer_rapport_pdf.py                 # Génération du rapport PDF
├── resultats/                                 # Fichiers JSON de résultats réels
│   ├── openai_gpt-oss-20b.json
│   ├── openai_gpt-oss-120b.json
│   ├── qwen_qwen3.8-27b.json
│   └── qwen3.8-27b_4_exemples.json
└── README.md
```

---

## 🚀 Utilisation

1. Définir votre clé API Groq :
   ```powershell
   $env:GROQ_API_KEY = "gsk_votre_cle"
   ```
2. Lancer les évaluations :
   ```powershell
   python code/evaluer.py openai/gpt-oss-20b
   python code/evaluer.py openai/gpt-oss-120b
   python code/evaluer.py qwen/qwen3.8-27b
   python code/variante.py qwen/qwen3.8-27b
   ```
3. Afficher la comparaison et les désaccords :
   ```powershell
   python code/comparer.py
   ```
