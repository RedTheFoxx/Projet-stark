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


#TODO : Un résumé par ligne (par intervention)
def cook_report_interventions(data):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL") or "",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                TODO PROMPT 
                """
            },
            {"role": "user", "content": json.dumps(data)}
        ],
    )

    return response.choices[0].message.content

#TODO : Un résumé qui est généré à partir d'une liste entière d'interventions
#TODO : Penser à récupérer la fréquence des interventions
def cook_report_resume(data):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL") or "",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
                TODO PROMPT 
                """
            },
            {"role": "user", "content": json.dumps(data)}
        ],
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    pass