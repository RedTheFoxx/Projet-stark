import streamlit as st

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
        "Déposez vos fichiers au format .xlsx ou .txt",
        type=["xlsx", "txt"],
        accept_multiple_files=True,
    )

st.markdown("---")


if st.button("Générer", type="primary", use_container_width=True):

    # 1. Ici, on insérera la logique cablée à un Langchain (ou autre) pour gérer deux pipes en fonction du mode sélectionné sur le radio button.
    # - Pour l'instant c'est du code de démo pour faire marcher l'interface joliment

    # Si on a le temps, on fait le pipe 3 avec les deux fichiers .txt

    with st.spinner("Génération du rapport en cours ..."):

        import time

        time.sleep(3)

        st.success("Rapport prêt au téléchargement")
        st.download_button(
            label="Télécharger le rapport",
            data="Contenu d'exemple",
            file_name="rapport.txt",
            mime="text/plain",
        )

# 2. A ce niveau, on pourrait ajouter une étape intermédiare pour prévisualiser le rapport avant de le télécharger
# - et proposer à l'utilisateur d'en regénérer un si ça ne convient pas.

st.markdown("---")

# J'avais envie
st.caption(
    "Vince & Red - Stark © 2024 / Toute utilisation de système basé sur de l'IA générative implique des principes de précaution et de responsabilité."
)
