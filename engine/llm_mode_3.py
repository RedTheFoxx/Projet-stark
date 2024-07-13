import os
import json
from urllib import response
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "",
)


# PROMPT DES INTERVENTIONS : Génère un résumé par intervention et sera ensuite utilisé pour produire le bilan annuel
def cook_report_interventions(data: list) -> str:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL") or "",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                Tu es un assistant qui reçoit un fichier JSON et génère un résume structuré sous forme de string en retour. 
                Tu ne dois pas inventer des informations que tu n'aurais pas eues dans le JSON d'entrée.
                Le champ "Intervention du" fait référence à la Date et heure du début d'intervention
                Le champ "Durée" est égal au temps écoulé entre le début d'intervention et la fin d'intervention
                Le champ "Résumé" doit être un résumé en 70 mots maximum des informations issues uniquement des deux messages du client et du message au client 
                Si le message au client est "Demande traitée", indique que l'intervention a été effectuée sans remarque ou alerte particulière de la part du technicien.
                Reste très factuel, adopte un ton professionnel, ne fais pas mention du nom du technicien intervenant, emploie le pronom "Nous"
                Tu ne dois pas produire de ```json et de ``` comme préfixe et suffixe de ton résultat, tu dois produire le format JSON suivant : 
                {
                    "Intervention du ": "JJ-MM-AAAA HH:MM:SS",
                    "Durée" : "HH:MM:SS",
                    "Résumé": "[A COMPLETER]"
                }
                Le format JSON doit être strictement valide et conforme aux standards JSON.
                """,
            },
            {"role": "user", "content": json.dumps(data)},
        ],
    )

    return response.choices[0].message.content or ""


# PROMPT DES BILAN : Génère un bilan annuel à partir d'une liste d'interventions résumées
def cook_report_resume(data: list) -> str:
    all_interventions = "".join(data)
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL") or "",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                Tu es un assistant qui produit un bilan annuel sur la base d'une liste d'interventions résumées. Rédige un paragraphe argumenté
                sur les données qui te sont fournies en entrée. N'invente aucune information. Ton format de sortie doit être une string. 
                """,
            },
            {"role": "user", "content": all_interventions},
        ],
    )

    return response.choices[0].message.content or ""


if __name__ == "__main__":
    test_prompt = [
        {
            "N° Demande": "F2023453342834",
            "Statut de la DI": "Cloturée",
            "Demande avec STI": "OUI",
            "Libellé site": "DIEPPE HOTEL WINDSOR",
            "Date/heure création de la demande": "2023-12-08T03:06:00.000",
            "Type de demande": "Alarme",
            "Motif de sollicitation": "Autre - Alarme technique",
            "Message du client": "016080:MINI TEMPERATURE DEPART PRIMAIRE FELMAN",
            "statut OT": "Réalisé",
            "Date/heure du RDV": "08/12/2023 7-12H",
            "Date/heure début du processus d'attribution": "2023-12-08T03:06:00.000",
            "Pris en charge par": "Jason Ayers",
            "Date/heure affectation au tech": "2023-12-08T07:25:00.000",
            "Date/heure début d'intervention": "2023-12-08T07:25:00.000",
            "Message du Client 2": "",
            "Date/heure fin d'intervention": "2023-12-08T07:55:00.000",
            "Date/heure de description du BI": "2023-12-08T07:25:00.000",
            "Problème réglé": "Oui",
            "Message au client": "Demande traitée",
            "Commentaire interne": "",
        }
    ]

    print(cook_report_interventions(test_prompt))
