import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # En-tête (sauf page 1) : pas de mention DSI/Machine Learning Appliqué
        if self._pageNumber > 1:
            self.drawString(40, 810, "Atelier 2 — Choisir un modèle sur preuves")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(40, 804, 555, 804)
            
        # Pied de page
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(40, 45, 555, 45)
        self.drawString(40, 32, "Rapport d'exécution et preuves expérimentales — API Groq")
        self.drawRightString(555, 32, f"Page {self._pageNumber} sur {page_count}")
        self.restoreState()

def creer_bloc_terminal(titre, commande, sortie, duree=None):
    """Crée un bloc visuel sous forme de tableau hermétique avec texte noir net et très lisible"""
    titre_text = f"<font color='#CBD5E1'>● ● ●</font>&nbsp;&nbsp;&nbsp;<b>{titre}</b>"
    if duree:
        titre_text += f"&nbsp;&nbsp;&nbsp;<font color='#94A3B8'><i>[Durée réelle : {duree}]</i></font>"
        
    header_p = Paragraph(titre_text, ParagraphStyle(
        'TermHeader',
        fontName='Helvetica',
        fontSize=8.5,
        textColor=colors.white,
    ))
    
    prompt = "PS C:\\Users\\MRAET MOHAMED AZIZ\\Desktop\\dsi3\\machine learning\\atelier2> "
    contenu = f"{prompt}{commande}\n\n{sortie.strip()}"
    
    body_pre = Preformatted(contenu, ParagraphStyle(
        'TermBody',
        fontName='Courier',
        fontSize=7.2,
        leading=9.6,
        textColor=colors.HexColor("#000000"),
    ))
    
    t = Table([[header_p], [body_pre]], colWidths=[515])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#1E293B")),
        ('TOPPADDING', (0,0), (0,0), 5),
        ('BOTTOMPADDING', (0,0), (0,0), 5),
        ('LEFTPADDING', (0,0), (0,0), 10),
        ('RIGHTPADDING', (0,0), (0,0), 10),
        
        ('BACKGROUND', (0,1), (0,1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0,1), (0,1), 8),
        ('BOTTOMPADDING', (0,1), (0,1), 8),
        ('LEFTPADDING', (0,1), (0,1), 10),
        ('RIGHTPADDING', (0,1), (0,1), 10),
        
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#64748B")),
        ('LINEBELOW', (0,0), (0,0), 1, colors.HexColor("#64748B")),
    ]))
    return KeepTogether([t, Spacer(1, 10)])

def generer_pdf(chemin_sortie):
    doc = SimpleDocTemplate(
        chemin_sortie,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=55
    )
    
    styles = getSampleStyleSheet()
    
    titre_style = ParagraphStyle(
        'TitreDoc',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    p_style = ParagraphStyle(
        'Paragraphe',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=8
    )

    story = []

    # Page 1 : Titre uniquement (sans mention académique ni bloc méta)
    story.append(Paragraph("Atelier 2 : Choisir un modèle sur preuves", titre_style))
    story.append(Spacer(1, 10))

    # Section 0 & 1
    story.append(Paragraph("1. Étape 0 & 1 — Vérification de l'API et Exploration des données", h1_style))
    story.append(Paragraph("Test de connectivité avec Groq et analyse de la distribution des 72 tickets annotés.", p_style))
    
    story.append(creer_bloc_terminal(
        "Capture 1 : Test de connexion API Groq (essai.py)",
        "python .\\code\\essai.py",
        "OK"
    ))

    story.append(creer_bloc_terminal(
        "Capture 2 : Distribution des 72 tickets réels (explorer.py)",
        "python .\\code\\explorer.py",
        "facturation   22  30.6 % ######################\n"
        "technique     20  27.8 % ####################\n"
        "compte        16  22.2 % ################\n"
        "commercial    14  19.4 % ##############"
    ))

    # Section 2 & 3
    story.append(Paragraph("2. Étape 2 & 3 — Tests unitaires : Classifieur et Métriques écrites à la main", h1_style))
    story.append(Paragraph("Validation du classifieur sur 5 exemples et test unitaire synthétique des métriques.", p_style))

    story.append(creer_bloc_terminal(
        "Capture 3 : Test unitaire du classifieur (test_classifieur.py)",
        "python .\\code\\test_classifieur.py",
        "Ticket : Ma facture est trop élevée\n"
        "Catégorie : facturation\n\n"
        "Ticket : Je ne peux plus me connecter à mon compte\n"
        "Catégorie : compte\n\n"
        "Ticket : L'application ne fonctionne plus\n"
        "Catégorie : technique\n\n"
        "Ticket : Je souhaite changer mon abonnement\n"
        "Catégorie : commercial\n\n"
        "Ticket :  bonjour ! \n"
        "Catégorie : commercial"
    ))

    story.append(creer_bloc_terminal(
        "Capture 4 : Test unitaire synthétique des métriques (test_evaluation.py)",
        "python .\\code\\test_evaluation.py",
        "=== Test synthétique ===\n"
        "accuracy : 0.750\n"
        "macro-F1 : 0.583\n"
        "invalides : 0.000\n\n"
        "categorie     precision    recall        F1     n\n"
        "facturation       0.000     0.000     0.000     0\n"
        "technique         1.000     1.000     1.000     1\n"
        "compte            1.000     0.500     0.667     2\n"
        "commercial        0.500     1.000     0.667     1\n\n"
        "Confusion matrix (lignes = vérité, colonnes = prédiction)\n"
        "              factur techni compte commer invali\n"
        "facturation        0      0      0      0      0\n"
        "technique          0      1      0      0      0\n"
        "compte             0      0      1      1      0\n"
        "commercial         0      0      0      1      0"
    ))

    story.append(PageBreak())

    # Section 4 & 5
    story.append(Paragraph("3. Étape 4 & 5 — Évaluations réelles des trois modèles candidats", h1_style))
    story.append(Paragraph("Protocole standardisé : même jeu de test (72 tickets), température 0, pause de 2.1 s.", p_style))

    story.append(creer_bloc_terminal(
        "Capture 5 : Évaluation du modèle openai/gpt-oss-20b (Modèle compact)",
        "python .\\code\\evaluer.py openai/gpt-oss-20b",
        "=== openai/gpt-oss-20b ===\n"
        "accuracy : 0.944\n"
        "macro-F1 : 0.948\n"
        "invalides : 0.014\n\n"
        "categorie     precision    recall        F1     n\n"
        "facturation       1.000     0.955     0.977    22\n"
        "technique         0.950     0.950     0.950    20\n"
        "compte            0.938     0.938     0.938    16\n"
        "commercial        0.929     0.929     0.929    14\n\n"
        "Confusion matrix (lignes = vérité, colonnes = prédiction)\n"
        "              factur techni compte commer invali\n"
        "facturation       21      0      0      1      0\n"
        "technique          0     19      1      0      0\n"
        "compte             0      1     15      0      0\n"
        "commercial         0      0      0     13      1\n\n"
        "Résultats enregistrés dans : resultats\\openai_gpt-oss-20b.json\n"
        "Durée totale : 192.0s (dont appels API seuls : 40.8s, pauses : 151.2s)",
        duree="192.0s"
    ))

    story.append(creer_bloc_terminal(
        "Capture 6 : Évaluation du modèle openai/gpt-oss-120b (Modèle 6x plus gros)",
        "python .\\code\\evaluer.py openai/gpt-oss-120b",
        "=== openai/gpt-oss-120b ===\n"
        "accuracy : 0.917\n"
        "macro-F1 : 0.918\n"
        "invalides : 0.000\n\n"
        "categorie     precision    recall        F1     n\n"
        "facturation       0.840     0.955     0.894    22\n"
        "technique         1.000     0.850     0.919    20\n"
        "compte            0.941     1.000     0.970    16\n"
        "commercial        0.923     0.857     0.889    14\n\n"
        "Confusion matrix (lignes = vérité, colonnes = prédiction)\n"
        "              factur techni compte commer invali\n"
        "facturation       21      0      0      1      0\n"
        "technique          2     17      1      0      0\n"
        "compte             0      0     16      0      0\n"
        "commercial         2      0      0     12      0\n\n"
        "Résultats enregistrés dans : resultats\\openai_gpt-oss-120b.json\n"
        "Durée totale : 190.7s (dont appels API seuls : 39.4s, pauses : 151.2s)",
        duree="190.7s"
    ))

    story.append(PageBreak())

    story.append(creer_bloc_terminal(
        "Capture 7 : Évaluation du modèle qwen/qwen3.8-27b (Autre famille)",
        "python .\\code\\evaluer.py qwen/qwen3.8-27b",
        "=== qwen/qwen3.8-27b ===\n"
        "accuracy : 0.958\n"
        "macro-F1 : 0.956\n"
        "invalides : 0.000\n\n"
        "categorie     precision    recall        F1     n\n"
        "facturation       0.917     1.000     0.957    22\n"
        "technique         1.000     0.950     0.974    20\n"
        "compte            0.941     1.000     0.970    16\n"
        "commercial        1.000     0.857     0.923    14\n\n"
        "Confusion matrix (lignes = vérité, colonnes = prédiction)\n"
        "              factur techni compte commer invali\n"
        "facturation       22      0      0      0      0\n"
        "technique          0     19      1      0      0\n"
        "compte             0      0     16      0      0\n"
        "commercial         2      0      0     12      0\n\n"
        "Résultats enregistrés dans : resultats\\qwen_qwen3.8-27b.json\n"
        "Durée totale : 263.7s (dont appels API seuls : 112.4s, pauses : 151.2s)",
        duree="263.7s"
    ))

    # Section 6
    story.append(Paragraph("4. Étape 6 — Variante de consigne : Few-Shot (+ 4 exemples)", h1_style))
    story.append(Paragraph("Évaluation sur le modèle en tête (Qwen 27B) avec 4 exemples ajoutés à la consigne sans fuite de données.", p_style))

    story.append(creer_bloc_terminal(
        "Capture 8 : Évaluation de la variante Few-Shot (variante.py)",
        "python .\\code\\variante.py qwen/qwen3.8-27b",
        "=== qwen3.8-27b + 4 exemples ===\n"
        "accuracy : 0.972\n"
        "macro-F1 : 0.971\n"
        "invalides : 0.000\n\n"
        "categorie     precision    recall        F1     n\n"
        "facturation       0.957     1.000     0.978    22\n"
        "technique         1.000     0.950     0.974    20\n"
        "compte            0.941     1.000     0.970    16\n"
        "commercial        1.000     0.929     0.963    14\n\n"
        "Confusion matrix (lignes = vérité, colonnes = prédiction)\n"
        "              factur techni compte commer invali\n"
        "facturation       22      0      0      0      0\n"
        "technique          0     19      1      0      0\n"
        "compte             0      0     16      0      0\n"
        "commercial         1      0      0     13      0\n\n"
        "Résultats enregistrés dans : resultats\\qwen3.8-27b_4_exemples.json\n"
        "Durée totale : 217.6s (dont appels API seuls : 66.3s, pauses : 151.2s)",
        duree="217.6s"
    ))

    story.append(PageBreak())

    # Section 5 & Synthèse
    story.append(Paragraph("5. Synthèse comparative globale et analyse des désaccords", h1_style))
    story.append(Paragraph("Exécution du script <code>comparer.py</code> intégrant l'ensemble des 4 évaluations réelles.", p_style))

    story.append(creer_bloc_terminal(
        "Capture 9 : Tableau comparatif global et désaccords (comparer.py)",
        "python .\\code\\comparer.py",
        "=====================================================================================\n"
        "COMPARAISON DES MODÈLES\n"
        "=====================================================================================\n"
        "Modèle                              Accuracy  Macro-F1 Invalides  Durée (s) API seul(s)\n"
        "-------------------------------------------------------------------------------------\n"
        "qwen3.8-27b + 4 exemples               0.972     0.971     0.000      217.6      66.3\n"
        "qwen/qwen3.8-27b                       0.958     0.956     0.000      263.7     112.4\n"
        "openai/gpt-oss-20b                     0.944     0.948     0.014      192.0      40.8\n"
        "openai/gpt-oss-120b                    0.917     0.918     0.000      190.7      39.4\n\n"
        "=====================================================================================\n"
        "DÉSACCORDS ENTRE MODÈLES\n"
        "=====================================================================================\n"
        "T004 (vérité : commercial)  : 120b = facturation | 20b = commercial  | qwen+4ex = facturation | qwen = facturation\n"
        "T006 (vérité : commercial)  : 120b = commercial  | 20b = invalide    | qwen+4ex = commercial  | qwen = commercial\n"
        "T023 (vérité : compte)      : 120b = compte      | 20b = technique   | qwen+4ex = compte      | qwen = compte\n"
        "T039 (vérité : technique)   : 120b = facturation | 20b = technique   | qwen+4ex = technique   | qwen = technique\n"
        "T040 (vérité : commercial)  : 120b = facturation | 20b = commercial  | qwen+4ex = commercial  | qwen = facturation\n"
        "T061 (vérité : technique)   : 120b = facturation | 20b = technique   | qwen+4ex = technique   | qwen = technique\n"
        "T066 (vérité : facturation) : 120b = commercial  | 20b = commercial  | qwen+4ex = facturation | qwen = facturation\n\n"
        "Total des tickets avec désaccord : 7 / 72"
    ))

    # Tableau récapitulatif stylisé
    story.append(Paragraph("<b>Tableau récapitulatif des livrables :</b>", p_style))
    table_data = [
        ["Configuration", "Accuracy", "Macro-F1", "Tickets corrects", "Invalides", "Latence API"],
        ["qwen3.8-27b + 4 ex", "0.972", "0.971", "70 / 72", "0.0 %", "66.3 s"],
        ["qwen/qwen3.8-27b", "0.958", "0.956", "69 / 72", "0.0 %", "112.4 s"],
        ["openai/gpt-oss-20b", "0.944", "0.948", "68 / 72", "1.4 % (1 tick)", "40.8 s"],
        ["openai/gpt-oss-120b", "0.917", "0.918", "66 / 72", "0.0 %", "39.4 s"]
    ]
    t = Table(table_data, colWidths=[150, 65, 65, 85, 75, 75])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Rapport généré avec succès dans : {chemin_sortie}")

if __name__ == "__main__":
    sortie = Path(__file__).resolve().parent.parent / "Rapport_Atelier2_Executions.pdf"
    generer_pdf(str(sortie))
