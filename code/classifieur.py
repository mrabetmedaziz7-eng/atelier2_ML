import json, os, time
from groq import Groq, RateLimitError, BadRequestError

CATEGORIES = ["facturation", "technique", "compte", "commercial"]

client = None

def get_client():
    global client
    if client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY n'est pas définie dans les variables d'environnement.")
        client = Groq(api_key=api_key)
    return client

CONSIGNE = """Tu es un agent de tri du service client.
Classe le ticket dans exactement une catégorie :
- facturation : montant, facture, paiement, remboursement.
- technique : un service ne fonctionne pas comme prévu.
- compte : accès au compte ou données personnelles.
- commercial : choix d'offre, abonnement, résiliation.
Si plusieurs catégories semblent possibles, retiens l'intention
principale du client : ce qu'il veut obtenir.
Réponds uniquement par un objet JSON de la forme
{"categorie": "<une des quatre>"}."""

# Exemples pour le few-shot réécrits sans copier les tickets du test (évite la fuite de données)
CONSIGNE_EXEMPLES = CONSIGNE + """

Exemples :
"Pourquoi m'avez-vous prélevé 15 euros de trop le mois dernier ?" ->
{"categorie": "facturation"}
"L'écran reste noir quand je clique sur le bouton de lecture vidéo." ->
{"categorie": "technique"}
"J'ai oublié mon mot de passe et mon adresse email a changé." ->
{"categorie": "compte"}
"Je voudrais savoir quelles sont vos formules tarifaires pour les professionnels." ->
{"categorie": "commercial"}"""

def classer(texte, modele, consigne=CONSIGNE, temperature=0.0):
    cl = get_client()
    reponse = None
    for tentative in range(5):
        try:
            reponse = cl.chat.completions.create(
                model=modele,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=[{"role": "system", "content": consigne},
                          {"role": "user", "content": texte}],
            )
            break
        except RateLimitError:
            time.sleep(10 * (tentative + 1))   # attente croissante
        except BadRequestError:
            # Si le modèle a produit une sortie non-JSON (ex: refus de génération),
            # Groq lève BadRequestError -> comptabilisé comme "invalide"
            return "invalide"
        except Exception as e:
            raise e
            
    if reponse is None:
        return "invalide"
        
    try:
        categorie = json.loads(
            reponse.choices[0].message.content).get("categorie", "")
    except (json.JSONDecodeError, AttributeError, TypeError):
        return "invalide"
        
    categorie = str(categorie).strip().lower()
    return categorie if categorie in CATEGORIES else "invalide"
