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
        with st.spinner("Traitement du lot en cours ..."):
            for file in uploaded_files or []:
                nb_records = extractor.count_records(file)
                st.write(f"Nombre d'enregistrements détectés : {nb_records}")
                
                all_data = extractor.extract_all_lines(file)
                for i, data_to_process in enumerate(all_data):
                    with st.spinner(f"Génération du rapport {i+1}/{nb_records} ..."):
                        generated_content = llm_mode_1.cook_report(data_to_process)
                        docify.make_intervention_report(generated_content, f"rapport_intervention_{i+1}")
                
                st.success(f"{nb_records} rapport(s) généré(s) avec succès !")

    if mode == "CR d'activité":
        st.write("Mode d'activité non implémenté")
    if mode == "CR avec gammes (non-implémenté)":
        st.write("Mode gammes non implémenté")

st.markdown("---")

# J'avais envie
st.caption(
    "Vince & Red - Stark © 2024 / Toute utilisation de système basé sur de l'IA générative implique des principes de précaution et de responsabilité."
)