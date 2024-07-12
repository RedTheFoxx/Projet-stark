import json
import streamlit as st
import engine.docify as docify
import engine.extractor as extractor
import engine.llm_mode_1 as llm_mode_1

st.set_page_config(
    layout="wide", page_title="Stark - Compte-rendus"
)  # Mode large par défaut de streamlit et titre de page

# Markdown simple
st.markdown(
    """
# Stark - Rapports et compte-rendus
*Bienvenue sur votre interface de génération automatisée de rapports.*
"""
)

st.markdown("---")  # Une barre de séparation en markdown

col1, col2 = st.columns(
    2
)  # Deux colonnes pour aligner le champs d'upload et les radio boutons

with col1:
    st.subheader("Mode")
    mode = st.radio(
        "Sélectionnez un mode :",
        ["CR d'intervention", "CR d'activité", "CR avec gammes (non-implémenté)"],
    )

with col2:
    st.subheader("Fichiers")
    uploaded_files = st.file_uploader(
        "Déposez vos fichiers au format .xlsx",
        type=["xlsx"],
        accept_multiple_files=True,
    )

st.markdown("---")


if st.button("Générer", type="primary", use_container_width=True):
    if mode == "CR d'intervention":
        with st.spinner("Génération d'un rapport ..."):
            for file in uploaded_files or []:
                st.write("Nombre d'enregistrements détectés : " + str(extractor.count_records(file))) # On liste le nombre total d'enregistrements du fichier (on proposera de sélectionner)
                data_to_process = (extractor.extract_all_lines(file))[0] # On sélectionne le premier enregistrement
                generated_content = llm_mode_1.cook_report(data_to_process) # On génère le json intermédiaire
                docify.make_intervention_report(generated_content) # On build le docx
                st.success("Rapport généré avec succès !")
                
    if mode == "CR d'activité":
        st.write("Mode d'activité non implémenté")
    if mode == "CR avec gammes (non-implémenté)":
        st.write("Mode gammes non implémenté")

st.markdown("---")

# J'avais envie
st.caption(
    "Vince & Red - Stark © 2024 / Toute utilisation de système basé sur de l'IA générative implique des principes de précaution et de responsabilité."
)