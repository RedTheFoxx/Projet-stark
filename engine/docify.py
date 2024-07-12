"""Module de génération de rapports au format docx."""

import json
from docx import Document
from docx.shared import Inches


def make_intervention_report(data, file_name):
    data = json.loads(data) # On s'assure de convertir la string en entrée en dictionnaire Python
    doc = Document()

    header_table = doc.add_table(
        rows=1, cols=2
    )  # Case 1 : la date d'intervention et case 2, le logo de stark
    header_table.cell(0, 0).text = (
        "Date d'intervention : " + data["Date d'intervention"]
    )
    logo_cell = header_table.cell(0, 1)
    logo_path = "ressources/data/logo_stark.png"
    logo_paragraph = logo_cell.paragraphs[0]
    logo_run = logo_paragraph.add_run()
    logo_run.add_picture(logo_path, width=Inches(2.5))

    doc.add_heading("Rapport d'intervention", 0)
    doc.add_heading("Informations client", 2)

    table = doc.add_table(rows=len(data) - 1, cols=2) # - 1 pour éviter d'avoir une ligne vide à la fin vu qu'on place "resume" plus bas

    for i, (key, value) in enumerate(data.items()):
        if key not in ["Resume", "Date d'intervention"]:
            table.cell(i, 0).text = key
            table.cell(i, 1).text = value


    doc.add_heading("Compte-rendu d'intervention", 2)
    doc.add_paragraph(data["Resume"])

    doc.save(f"output/{file_name}.docx")


if __name__ == "__main__":

    test_data = {
        "Date d'intervention": "04/05/2022",
        "Libellé du site": "Paris 75011 RESIDENCE DUQUN",
        "Ville": "PARIS",
        "Motif": "Chauffage - Autre motif à préciser",
        "Statut": "Un agent est intervenu hier, la chaudière a fonctionné 2 heures.\n\nUne nouvelle intervention ce matin, et à nouveau la chaudière ne fonctionne plus.",
        "Resume": """Bonjour,
        Je suis John Doe, technicien chez Stark Industries, et je me permets de vous écrire suite à mon intervention chez vous le 04/05/2022 à 14h47.
        Je me suis rendu à l'adresse suivante : Paris CAUX IMMOBILIER pour régler un problème de chauffage.
        En effet, vous avez fait appel à nos services pour signaler un manque de chauffage dans votre habitation.
        Après avoir examiné votre chaudière, j'ai constaté que l'horloge était complètement décalée.
        Je suis donc intervenu pour régler ce dysfonctionnement.
        Je suis ravi de vous informer que l'intervention a été un succès et que votre chaudière fonctionne à présent correctement.
        Nous tenons à vous remercier pour votre confiance et restons à votre disposition pour toute information complémentaire.
        N'hésitez pas à contacter le Centre de Relation Clients (CRC) au 0 800 80 93 00, disponible 24h/24 et 7j/7.""",
    }

    make_intervention_report(test_data, "test_rapport")
