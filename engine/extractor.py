"""Gestion des extractions de données d'un fichier Excel et leur conversions."""

import pandas as pd
import json
import os

def extract_all_lines(file) -> dict:
    """Extrait toutes les lignes d'un fichier Excel et les convertit en un dictionnaire.

    Cette fonction lit un fichier Excel, le convertit en JSON, puis charge ce JSON
    en mémoire sous forme de dictionnaire Python.

    Args:
        path_excel_file: Chemin vers le fichier Excel à traiter.

    Returns:
        Un dictionnaire contenant toutes les données du fichier Excel.

    Note:
        Cette fonction crée un fichier JSON temporaire dans le dossier 'temp/'
        avec le même nom que le fichier Excel d'entrée.
    """
    df = pd.read_excel(file)
    df.to_json(
        f"temp/extracted_data.json",
        orient="records",
        force_ascii=False,
        date_format="iso",
    )
    with open(f"temp/extracted_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def count_records(file) -> int:
    """Compte le nombre de lignes d'un fichier Excel.

    Args:
        path_excel_file: Chemin vers le fichier Excel à traiter.

    Returns:
        Le nombre de lignes du fichier Excel.
    """
    df = pd.read_excel(file)
    return len(df)

def extract_per_customer(file, filter : str) -> dict:
    """Extrait les données d'un fichier Excel filtrées par client.

    Args:
        file: Le fichier à traiter.
        filter: Une string qui représente la valeur de colonne "Libellé site" que l'on veut considérer.
        
    Returns:
        Un dictionnaire orientation RECORDS contenant les données filtrées par client.
    """
    
    df = pd.read_excel(file)
    df = df[df["Libellé site"] == filter]
    df.to_json(
        f"temp/extracted_data_per_customer.json",
        orient="records",
        force_ascii=False,
        date_format="iso",
    )
    with open(f"temp/extracted_data_per_customer.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

if __name__ == "__main__":
    print(extract_per_customer(os.path.join("ressources/data/extraits-Data-Interventions-annuels_1.xlsx"), "DIEPPE CHATEAU MUSEE"))