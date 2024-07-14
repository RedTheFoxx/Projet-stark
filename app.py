import os
import streamlit as st
import zipfile
import io
from random import randint

# Modules persos
import engine.docify as docify          # Le compositeur de documents
import engine.extractor as extractor    # L'extracteur de données
import engine.llm_mode_1 as llm_mode_1  # Le LLM configuré pour le projet 1
import engine.llm_mode_3 as llm_mode_3  # Le LLM configuré pour le projet 3

# ------------------------------------------------------------------ #
# Initialisation, création des dossiers et nettoyage des dossiers le cas échéant

# Configuration de la page Streamlit
st.set_page_config(layout="wide", page_title="Stark - Compte-rendus", page_icon="⚡")

# Création des dossiers "temp" et "output" s'ils n'existent pas
repositories = ["temp", "output"]
for repository in repositories:
    if not os.path.exists(repository):
        os.makedirs(repository)

# A chaque refresh (Touche R ou "Rerun") de l'application on nettoie leurs contenus
for repository in repositories:
    for file in os.listdir(repository):
        os.remove(os.path.join(repository, file))

# ------------------------------------------------------------------ #

# En-tête de l'application
st.image("ressources/data/logo_stark_white.png", width=350)
st.markdown(
    """
# Rapports et compte-rendus
*Bienvenue sur votre interface de génération automatisée de rapports.*
"""
)

st.markdown("---")

# Section de sélection du mode et d'upload de fichiers
col1, col2 = st.columns(
    2
)  # Deux colonnes pour aligner le champs d'upload et les radio boutons

with col1:
    st.subheader("Mode")
    mode = st.radio(
        "Sélectionnez un mode :",
        [
            "CR d'intervention",
            "CR d'activité",
            "CR incluant des gammes (non-implémenté)",
        ],
        key="mode_selection"
    )

# On génère une nouvelle clef à la fois que l'état du widget au-dessus change (mode_selection)
if 'widget_key' not in st.session_state or st.session_state.mode_selection != st.session_state.get('previous_mode'):
    st.session_state.widget_key = str(randint(1000, 100000000))
    st.session_state.previous_mode = st.session_state.mode_selection

with col2:
    st.subheader("Fichier")
    uploaded_files = st.file_uploader(
        "Déposez votre fichier au format .xlsx",
        type=["xlsx"],
        accept_multiple_files=True,
        help="Attention, seuls les fichiers destinés au projet Stark fonctionnent !",
        
        # La key permet de gérer l'état du widget selon certaines conditions
        # Ici, dès que l'on change le mode des radios button, on envoie une nouvelle clef à ce widget qui est considéré comme "neuf"
        # et donc le widget est réinitialisé.
        key=st.session_state.widget_key
    )

st.markdown("---")

# Actions déclenchées par le bouton "Générer"
if st.button("Générer", type="primary", use_container_width=True):
    if mode == "CR d'intervention":
        with st.spinner("Traitement des interventions en cours ..."):
            generated_files = []
            for file in uploaded_files or []:
                nb_records = extractor.count_records(file)
                st.write(f"Nombre d'enregistrements détectés : {nb_records}")

                all_data = extractor.extract_all_lines(file)
                for i, data_to_process in enumerate(all_data):
                    with st.spinner(f"Génération du rapport {i+1}/{nb_records} ..."):
                        generated_content = llm_mode_1.cook_report(data_to_process)
                        completed_doc = docify.make_intervention_report(
                            str(generated_content)
                        )
                        output_file = f"output/RI_{i+1}.docx"
                        completed_doc.save(output_file)
                        generated_files.append(output_file)

                st.success(f"{nb_records} rapport(s) généré(s) avec succès !")
                # On a tout généré dans output, on va pouvoir les télécharger ci-dessous

                # Une ligne par fichier et son bouton de téléchargement personnel
                st.subheader("Télécharger les rapports individuels")
                for file in generated_files:
                    with open(file, "rb") as f:
                        st.download_button(
                            label=f"Télécharger {os.path.basename(file)}",
                            data=f,
                            file_name=os.path.basename(file),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )

                # Tous les rapports d'un coup en ZIP
                st.subheader("Tout télécharger (.zip)")
                zip_buffer = (
                    io.BytesIO()
                )  # On lui alloue un buffer qui servira de passe-plat vers le fichier .zip final
                with zipfile.ZipFile(
                    zip_buffer, "w"
                ) as zip_file:  # On se prépare à écrire dans le fichier .zip (mode w)
                    for file in generated_files:
                        zip_file.write(
                            file, os.path.basename(file)
                        )  # Pour chaque fichier, on l'ajoute dans le zip

                st.download_button(
                    label="Télécharger tous les rapports",
                    data=zip_buffer.getvalue(),
                    file_name="lot_rapports.zip",
                    mime="application/zip",
                )

    if mode == "CR d'activité":

        # COMMENTER LES FILTRES QUE L'ON NE SOUHAITE PAS PROCESSER : Le traitement est long sinon ...
        # -------------------------------------------------------------------------------------------- #

        filters = [
            "DIEPPE CHATEAU MUSEE",
            "DIEPPE COMMUN D'AGGLO SERVICE COLLECTE",
            "DIEPPE GYMNASE ROGE DESJARDIN MILLE CLUB",
            "NEUVILLE LES DIEPPE MATERNELLE MARIE CUR",
            "SERQUEUX MAIRIE ECOLE",
            "DIEPPE HOTEL WINDSOR"
        ]

        # -------------------------------------------------------------------------------------------- #

        generated_reports = []  # Liste pour stocker les noms des fichiers générés

        for file in uploaded_files or []:
            with st.spinner("Traitement en cours ..."):
                for filter in filters:
                    with st.spinner(
                        f"Extraction des données pour le client {filter}..."
                    ):
                        customer_records = extractor.extract_per_customer(file, filter)

                    if customer_records != [""]:
                        nb_interventions = len(customer_records)
                        st.success(f"Données extraites avec succès pour {filter}")
                        st.write(
                            f"Nombre d'interventions trouvées : {nb_interventions}"
                        )

                        progress_bar = st.progress(0)
                        all_interventions = []

                        for i, data_to_process in enumerate(customer_records):
                            with st.spinner(
                                f"Traitement de l'intervention {i+1}/{nb_interventions} pour {filter}..."
                            ):
                                generated_interventions = (
                                    llm_mode_3.cook_report_interventions(
                                        data_to_process
                                    )
                                )
                                all_interventions.append(generated_interventions)
                            progress_bar.progress((i + 1) / nb_interventions)

                        with st.spinner(
                            f"Génération du résumé annuel pour {filter}..."
                        ):
                            generated_content = llm_mode_3.cook_report_resume(
                                all_interventions
                            )

                        with st.spinner(
                            f"Création du rapport d'activité final pour {filter}..."
                        ):
                            completed_doc = docify.make_activity_report(
                                filter,
                                all_interventions,
                                generated_content,
                            )
                            completed_doc.save(f"output/RA_{filter}.docx")
                            generated_reports.append(f"RA_{filter}.docx") # On ajoute le fichier généré dans la liste des téléchargements finaux

                        st.success(f"Rapport d'activité généré pour {filter} !")
                    else:
                        st.warning(f"Aucune donnée trouvée pour le client {filter}")

        # Une fois que tous les rapports sont générés
        if generated_reports:
            st.subheader("Télécharger les rapports générés")
            
            # Téléchargement individuel des rapports
            for report in generated_reports:
                with open(f"output/{report}", "rb") as file:
                    st.download_button(
                        label=f"Télécharger {report}",
                        data=file,
                        file_name=report,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
            
            # Téléchargement de tous les rapports en ZIP
            st.subheader("Tout télécharger (.zip)")
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for report in generated_reports:
                    zip_file.write(f"output/{report}", report)

            st.download_button(
                label="Télécharger tous les rapports d'activité",
                data=zip_buffer.getvalue(),
                file_name="lot_rapports_activite.zip",
                mime="application/zip",
            )

    if mode == "CR avec gammes (non-implémenté)":
        st.warning("Ce mode n'est pas encore pris en charge !")

        # TODO : - On prends deux .txt en entrée qui sont des instructions pour des systèmes à dépanner
        # TODO : - On doit comparer ces instructions avec ce qui à été fait dans chaque interventions (une interv. par ligne)
        # TODO : -> On devra générer des rapports d'interventions incluant ces données ci-dessus


# Pied de page
st.markdown("---")

# Car il faut bien s'amuser
st.caption(
    "Vince & Red - Stark © 2024 / Toute utilisation de système basé sur de l'IA générative implique des principes de précaution et de responsabilité. Le système peut être sujet à des hallucinations et impose une vérification humaine des données produites."
)