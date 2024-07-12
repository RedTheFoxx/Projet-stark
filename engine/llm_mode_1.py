import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "",
)

def cook_report(data):

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL") or "",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                Tu es un assistant qui reçoit un JSON d'informations propres à une intervention 
                et génère un rapport structuré au format JSON en retour. 
                Tu ne dois pas inventer des informations que tu n'aurais pas eu dans le JSON d'entrée.
                Le champ "Resume" doit être un texte complet d'un paragraphe qui résume ce qui s'est passé dans l'intervention sans
                être trop créatif. Reste très factuel, adopte un ton professionnel, ne fais pas mention du nom d'un technicien intervenant.
                Tu ne dois pas produire de ```json et de ``` comme préfixe et suffixe de ton résultat, tu dois produire le format JSON suivant : 
                {
                    "Date d'intervention": "JJ-MM-AAAA HH:MM:SS", 
                    "Libellé du site": "[A COMPLETER]", 
                    "Ville": "[A COMPLETER]", 
                    "Motif": "[A COMPLETER]", 
                    "Statut": "[A COMPLETER]", 
                    "Resume": "[A COMPLETER]"
                }
                Le format JSON doit être strictement valide et conforme aux standards JSON.
                """,
            },
            {"role": "user", "content": json.dumps(data)},
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    prompt_data = [
        {
            "N° Demande": "F20225044634",
            "Statut de la DI": "Cloturée",
            "Libellé site": "Paris 75011 RESIDENCE DUQUN",
            "Ville": "PARIS",
            "Motif de sollicitation": "Chauffage - Autre motif à préciser",
            "Message du client": "Un agent est intervenu hier, la chaudière a fonctionné 2 heures.\n\nUne nouvelle intervention ce matin, et à nouveau la chaudière ne fonctionne plus.\n\nMerci de bien vouloir intervenir PAR RETOUR afin de ne pas laisser les résidents sans chauffage durant le week-end. Les températures sont très froides actuellement.\n\nCette situation est inadmissible. Nous exigeons un retour de votre part sur vos interventions.",
            "Date/heure fin d'intervention": "2022-04-02T13:01:00.000",
            "Date/heure de description du BI": "2022-04-02T13:02:00.000",
            "Problème réglé": "Oui",
            "Nom technicien": "Peter Parker",
            "Message au client": "Intervention effectué le 01/04  de 18h30 a 20h20.Defaut preventilation , nettoyage foyer ,remplacement electrodes, ouverture pied de cheminée",
        }
    ]

    report = cook_report(prompt_data[0])
    print(report)
