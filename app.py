import streamlit as st
import engine.docify as docify
import engine.extractor as extractor
import engine.llm_mode_1 as llm_mode_1
import engine.llm_mode_3 as llm_mode_3

st.set_page_config(
    layout="wide", page_title="Stark - Compte-rendus"
)  # Mode large par défaut de streamlit et titre de page

# Markdown simple
st.image("ressources/data/logo_stark.png", width=100)   
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
                        docify.make_intervention_report(
                            generated_content, f"rapport_intervention_{i+1}"
                        )

                st.success(f"{nb_records} rapport(s) généré(s) avec succès !")

    if mode == "CR d'activité":
        filters = [
            "DIEPPE CHATEAU MUSEE",
            "DIEPPE COMMUN D'AGGLO SERVICE COLLECTE",
            "DIEPPE GYMNASE ROGE DESJARDIN MILLE CLUB",
            "NEUVILLE LES DIEPPE MATERNELLE MARIE CUR",
            "SERQUEUX MAIRIE ECOLE",
            "DIEPPE HOTEL WINDSOR"
        ]
        for file in uploaded_files or []:
            with st.spinner("Extraction des données ..."):
                
                    filter = filters[0]
                    customer_records = extractor.extract_per_customer(file, filter)
                    
                    if customer_records != [""]:
                        
                        st.write(f"Nombre d'interventions pour le client {filter} : {len(customer_records)}")
                        with st.spinner("Génération des rapports ..."):
                            
                            all_interventions = []
                            for i, data_to_process in enumerate(customer_records):
                                generated_interventions = llm_mode_3.cook_report_interventions(data_to_process)
                                all_interventions.append(generated_interventions)
                                
                            print(all_interventions)
                            st.stop()
                            
                            #TODO : On envoie tout le dico. des interventions au second prompt pour faire un bilan
                            # generated_content = llm_mode_3.cook_report_resume(all_interventions)
                            
                            #TODO : On créé le docx
                            # docify.make_activity_report(filter, all_interventions, generated_content, f"rapport_activite_{i+1}")
                    else:
                        st.error(f"Aucune donnée trouvée pour le client {filter}")
                        st.stop()

st.markdown("---")

# J'avais envie
st.caption(
    "Vince & Red - Stark © 2024 / Toute utilisation de système basé sur de l'IA générative implique des principes de précaution et de responsabilité."
)
