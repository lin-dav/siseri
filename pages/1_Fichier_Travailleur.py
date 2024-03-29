import streamlit as st
import pandas as pd
import datetime as dt

st.set_page_config(layout="wide")

st.title("Fichier CSV travailleurs")


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
        "Nom",
        "Prénom",
        "Date de naissance (JJ/MM/AAAA)",
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
    "Spécificités": [
        "-Obligatoire. -Numéro de sécurité sociale. -13 caractères. - Le NIA pour les travailleurs étrangers est également accepté.",
        "-Obligatoire. -2 chiffres.",
        "-Obligatoire. -En majuscule, sans accent.",
        "-Obligatoire. -En majuscule, sans accent.",
        "-Obligatoire. ",
        "-Obligatoire. ",
        "-Obligatoire. -SIRET de l'établissement, connu dans SISERI",
        "-Optionnel. -Groupe de travailleurs présent dans l'établissement. Si inconnu ou non rempli, Groupe par défaut.",
        '-Obligatoire. -Catégorie du travailleur. Peut être vide si "AUTREEXPOSITION" est rempli.',
        "-Optionnel, sauf si Catégorie est vide.",
        "-Obligatoire. Civil ou Militaire.",
        "-Obligatoire. ",
        "-Obligatoire. ",
        "-Obligatoire. Externe, Interne ou les deux.",
        "-Obligatoire. ",
        "-Obligatoire. ",
        "-Obligatoire. Temps de travail.",
        "-Obligatoire. ",
    ],
}

type_contrat = {
    "code": ("CDI", "CDD", "CTT", "STG", "CAP", "TFP", "TVI"),
    "detail": {
        "CDI": "Contrat à Durée Indéterminée",
        "CDD": "Contrat à Durée Déterminée",
        "CTT": "Contrat de Travail Temporaire",
        "STG": "Stagiaire ou étudiant",
        "CAP": "Contrat d’apprentissage",
        "TFP": "Titulaire de la fonction publique",
        "TVI": "Travailleur indépendant non salarié",
    },
}

data_clean = pd.DataFrame(columns=d["Colonne"], index=range(1, 2))

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

        if data_fichier.shape[1] != 18:
            st.error(
                "Le fichier importé ne contient pas les colonnes attendues. Veuillez vous référer à l'aide, à droite."
            )
            st.write("Colonnes affichées : ")
            st.write(data_fichier.columns.tolist())
            data_fichier = data_clean.copy()

        else:
            # st.dataframe(data_fichier, use_container_width=True)
            data_fichier = data_fichier.set_axis(
                d["Colonne"], axis=1
            )  # renommer les colonnes

            data_fichier["DATENAISSANCE"] = pd.to_datetime(
                arg=data_fichier["DATENAISSANCE"], format="%d/%m/%Y", dayfirst=True
            )
            data_fichier["DATEDEBUT"] = pd.to_datetime(
                arg=data_fichier["DATEDEBUT"], format="%d/%m/%Y", dayfirst=True
            )

            for colonne in [
                "NIR",
                "NOM",
                "PRENOM",
                "SEXE",
                "GROUPE",
                "CLASSEMENT",
            ]:
                data_fichier[colonne] = data_fichier[colonne].astype(
                    "string", copy=False
                )

            for colonne in [
                "CLE",
                "SIRET",
                "codeDomaineActivite",
                "codeSecteurActivite",
                "QUOTITE",
            ]:
                data_fichier[colonne] = (
                    data_fichier[colonne]
                    .replace("--", 0)
                    .astype("int64", copy=False, errors="ignore")
                )
            data_fichier["CLE"] = data_fichier["CLE"].apply("{:0>2}".format)
            data_fichier["SIRET"] = data_fichier["SIRET"].apply("{:0>14}".format)

    data_tableau = st.data_editor(
        data_fichier,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        height=min(300 + len(data_fichier) * 60, 999),
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
                required=False,
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
                min_value=101000,
                max_value=605000,
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
                options=type_contrat["code"],
            ),
            "QUOTITE": st.column_config.SelectboxColumn(
                required=True,
                help="temps de travail",
                options=[1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
            ),
            "DATEDEBUT": st.column_config.DateColumn(
                required=True,
                help="Date de naissance (JJ/MM/AAAA)",
                format="DD/MM/YYYY",
            ),
        },
    )


with col2:
    col21, col22, col23 = st.columns(3)
    container_aide = st.container(border=True)

    with col21:
        if st.button("Mise en forme", type="primary"):
            data_tableau["NOM"] = data_tableau["NOM"].str.upper()
            data_tableau["PRENOM"] = data_tableau["PRENOM"].str.upper()
            data_tableau["CLE"] = data_tableau["CLE"].apply("{:0>2}".format)
            data_tableau["SIRET"] = data_tableau["SIRET"].apply("{:0>14}".format)
            data_tableau["DATENAISSANCE"] = pd.to_datetime(
                arg=data_tableau["DATENAISSANCE"]
            )
            data_tableau["DATEDEBUT"] = pd.to_datetime(arg=data_tableau["DATEDEBUT"])

            with col22:
                if st.download_button(
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
                ):
                    st.rerun()

        if col23.checkbox("Aide ?"):
            container_aide.write("# Aide")

            with container_aide.expander("**Colonnes attendues**"):
                st.table(d)

            with container_aide.expander("**Domaines, Secteurs et Métiers**"):
                st.link_button(url="Listes", label="Listes")

            with container_aide.expander("**Type de contrat de travail**"):
                st.dataframe(type_contrat["detail"])
