import streamlit as st
import pandas as pd
import datetime as dt

st.set_page_config(layout="wide")

st.write("# Fichier CSV travailleurs")


d = {
    "Colonne": [
        "NIR",
        "CLE",
        "NOM",
        "PRENOM",
        "DATENAISSANCE",
        "SEXE",
        "SIRET",
        "GROUPE",
        "CLASSEMENT",
        "AUTREEXPOSITION",
        "caractereActivite",
        "codeDomaineActivite",
        "codeSecteurActivite",
        "codeNuisanceRadiologique",
        "codeTypeContrat",
        "CodeMetier",
        "QUOTITE",
        "DATEDEBUT",
    ],
    "Description": [
        "Numéro de sécurité sociale (13 chiffres)",
        "Clé (2 chiffres)",
        "Nom en majuscule sans accent",
        "Prénom en majuscule sans accent",
        "Date de naissance JJ/MM/AAAA",
        "Sexe (F ou M)",
        "SIRET de rattachement (14 chiffres)",
        "Groupe de travailleurs",
        "Classement (A ou B ou vide)",
        "Autres expositions",
        "Caractère de l'activité",
        "Domaine d'activité",
        "Secteur d'activité",
        "Nuisance Radiologique",
        "Type de contrat",
        "Métier",
        "Quotité",
        "Date de début de contrat",
    ],
    "Spécificités": [],
}

data_clean = pd.DataFrame(columns=d["Colonne"], index=range(1, 2))
# st.data_editor(
#     data_clean,
#     num_rows="dynamic",
#     use_container_width=True,
#     hide_index=True,
# )

col1, col2 = st.columns([0.7, 0.3], gap="small")

with col1:
    uploaded_file = st.file_uploader(
        "**Importer un fichier .CSV au format attendu par SISERI**",
        type=["csv"],
        accept_multiple_files=False,
    )

    if uploaded_file is None:
        data_fichier = data_clean.copy()

    elif uploaded_file is not None:
        data_fichier = pd.read_csv(uploaded_file, sep=";")
        # st.dataframe(data_fichier, use_container_width=True)

        data_fichier["DATENAISSANCE"] = pd.to_datetime(
            arg=data_fichier["DATENAISSANCE"], format="%d/%m/%Y", dayfirst=True
        )
        data_fichier["DATEDEBUT"] = pd.to_datetime(
            arg=data_fichier["DATEDEBUT"], format="%d/%m/%Y", dayfirst=True
        )

        for colonne in ["NIR", "NOM", "PRENOM", "SEXE", "GROUPE", "CLASSEMENT"]:
            data_fichier[colonne] = data_fichier[colonne].astype("string", copy=False)

        for colonne in ["CLE", "SIRET", "codeDomaineActivite", "codeSecteurActivite"]:
            data_fichier[colonne] = (
                data_fichier[colonne]
                .replace("--", 0)
                .astype("int64", copy=False, errors="ignore")
            )
        data_fichier["CLE"] = data_fichier["CLE"].apply("{:0>2}".format)
        data_fichier["SIRET"] = data_fichier["SIRET"].apply("{:0>14}".format)

        data_fichier["QUOTITE"] = data_fichier["QUOTITE"].astype("float", copy=False)

    data_tableau = st.data_editor(
        data_fichier,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        height=999,
        width=999,
        column_config={
            "NIR": st.column_config.TextColumn(
                required=True,
                help="Numéro de sécurité sociale",
                max_chars=13,
                validate="^[12][0-9]{2}[0-9]{2}(2[AB]|[0-9]{2})[0-9]{3}[0-9]{3}$",
            ),
            "CLE": st.column_config.NumberColumn(
                required=True, help="Clé", format="%02d", min_value=0, max_value=99
            ),
            "NOM": st.column_config.TextColumn(
                required=True,
                help="nom de naissance, majuscule, sans accent (25 caractères maxi)",
                max_chars=25,
                validate="[a-zA-Z- ]+",
            ),
            "PRENOM": st.column_config.TextColumn(
                required=True,
                help="Prénom, majuscule, sans accent (25 caractères maxi)",
                max_chars=25,
                validate="[a-zA-Z-]+",
            ),
            "DATENAISSANCE": st.column_config.DateColumn(
                required=True,
                help="Date de naissance (JJ/MM/AAAA)",
                format="DD/MM/YYYY",
            ),
            "SEXE": st.column_config.SelectboxColumn(
                required=True, help="Genre", options=["F", "M"]
            ),
            "SIRET": st.column_config.NumberColumn(
                required=True,
                help="SIRET",
                format="%d",
                min_value=0,
                max_value=99999999999999,
            ),
            "GROUPE": st.column_config.TextColumn(
                required=True,
                help="Groupe de travailleurs",
                default="Groupe par défaut",
            ),
            "CLASSEMENT": st.column_config.SelectboxColumn(
                required=False, help="Classement A ou B", options=["A", "B"]
            ),
            "AUTREEXPOSITION": st.column_config.SelectboxColumn(
                required=False,
                help="Autres types d'exposition",
                options=["RADON", "RAY_COS", "SUR_GRP_1", "SUR_GRP_2"],
            ),
            "caractereActivite": st.column_config.SelectboxColumn(
                required=True,
                help="Caractère de l'activité",
                options=["Civil", "Militaire"],
            ),
            "codeDomaineActivite": st.column_config.SelectboxColumn(
                required=True,
                help="Domaine de l'activité.",
                options=[
                    "100000",
                    "200000",
                    "300000",
                    "400000",
                    "500000",
                    "600000",
                ],
            ),
            "codeSecteurActivite": st.column_config.NumberColumn(
                required=True,
                help="Secteur de l'activité.",
                format="%d",
                min_value=100000,
                max_value=699999,
                step=1,
            ),
            "codeNuisanceRadiologique": st.column_config.SelectboxColumn(
                required=True,
                help="Type de nuisance radiologique",
                options=[
                    "EXT",
                    "INT",
                    "EXTINT",
                ],
            ),
            "codeTypeContrat": st.column_config.SelectboxColumn(
                required=True,
                help="Type de contrat de travail",
                options=[
                    "CDI",
                    "CDD",
                    "CTT",
                    "STG",
                    "CAP",
                    "TFP",
                    "TVI",
                ],
            ),
            "QUOTITE": st.column_config.NumberColumn(
                required=True,
                help="temps de travail",
                format="%.1f",
                min_value=0.1,
                max_value=1,
                step=0.1,
            ),
            "DATEDEBUT": st.column_config.DateColumn(
                required=True,
                help="Date de naissance (JJ/MM/AAAA)",
                format="DD/MM/YYYY",
            ),
        },
    )


with col2:

    if st.button("Mise en forme", type="primary"):
        data_tableau["NOM"] = data_tableau["NOM"].str.upper()
        data_tableau["PRENOM"] = data_tableau["PRENOM"].str.upper()
        data_tableau["CLE"] = data_tableau["CLE"].apply("{:0>2}".format)
        data_tableau["SIRET"] = data_tableau["SIRET"].apply("{:0>14}".format)

        st.download_button(
            label="Télécharger le tableau",
            data=data_tableau.to_csv(
                sep=";",
                index=False,
                date_format="%d/%m/%Y",
                encoding="utf-8",
            ),
            file_name=f"import-trav_{dt.datetime.now()}.csv",
            mime="text/csv",
            type="primary",
        )

    with st.container(border=True):
        st.write("# Aide")

        with st.expander("**Colonnes attendues**"):
            st.table(d)

        with st.expander("**Domaine d'activité**"):
            st.write("ok")
