import streamlit as st
import pandas as pd
import datetime as dt
import re
from unidecode import unidecode
import numpy as np


def verification(df: pd.DataFrame):
    df_verification = pd.DataFrame(
        columns=("Numero_Ligne", "Nom_Colonne", "Valeur", "Erreur"), dtype="string"
    )

    with col1.expander("**Vérif.**", expanded=True):
        for i in range(df.shape[0]):
            for colonne in donnees_colonnes["Colonne"]:
                if (
                    colonne == "NIR"
                    and re.search(
                        "^[12][0-9]{2}[0-9]{2}(2[AB]|[0-9]{2})[0-9]{3}[0-9]{3}$",
                        df.loc[i, colonne],
                    )
                    is None
                ):

                    df_verification = pd.concat(
                        [
                            df_verification,
                            pd.DataFrame(
                                [
                                    {
                                        "Numero_Ligne": i + 1,
                                        "Nom_Colonne": colonne,
                                        "Valeur": df.loc[i, colonne],
                                        "Erreur": "Numéro de sécurité sociale n'est pas au bon format",
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )

                elif colonne == "CLE":
                    nir = int(df.loc[i, "NIR"].replace("2A", "19").replace("2B", "18"))
                    cle = 97 - nir % 97
                    if int(df.loc[i, colonne]) != cle:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": f"La clé de contrôle ne semble pas correcte. Valeur suggérée : {cle}",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "DATENAISSANCE":
                    if df.loc[i, "NIR"][1:3] != str(df.loc[i, colonne].year)[-2:]:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "L'année de naissance ne correspond pas avec le NIR.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )
                    if df.loc[i, "NIR"][3:5] != str(df.loc[i, colonne].month):
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le mois de naissance ne correspond pas avec le NIR.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "SEXE":
                    if (
                        (df.loc[i, "NIR"][0:1] == "1" and df.loc[i, colonne] != "M")
                        or (df.loc[i, "NIR"][0:1] == "2" and df.loc[i, colonne] != "F")
                        or (df.loc[i, "NIR"][0:1] not in ["1", "2"])
                    ):
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le sexe ne correspond pas avec le NIR.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "SIRET":
                    if re.search("[0-9]{14}", str(df.loc[i, colonne])) is None:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Numéro de SIRET n'est pas au bon format.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "CLASSEMENT":
                    if pd.isna(df.loc[i, colonne]) and pd.isna(
                        df.loc[i, "AUTREEXPOSITION"]
                    ):
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Classement et Autres Expositions ne peuvent pas être vides en même temps.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )
                    elif df.loc[i, colonne] not in ["A", "B"]:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le classement n'est ni A, ni B.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "AUTREEXPOSITION":
                    if not pd.isna(df.loc[i, colonne]):
                        if df.loc[i, colonne] not in [
                            "RADON",
                            "RAY_COS",
                            "SUR_GRP_1",
                            "SUR_GRP_2",
                        ]:
                            df_verification = pd.concat(
                                [
                                    df_verification,
                                    pd.DataFrame(
                                        [
                                            {
                                                "Numero_Ligne": i + 1,
                                                "Nom_Colonne": colonne,
                                                "Valeur": df.loc[i, colonne],
                                                "Erreur": "L'autre exposition saisie n'est pas valide.",
                                            }
                                        ]
                                    ),
                                ],
                                ignore_index=True,
                            )

                elif colonne == "caractereActivite":
                    if df.loc[i, colonne] not in ["Civil", "Militaire"]:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le caractère de l'activité saisie n'est pas valide.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "codeDomaineActivite":
                    if (
                        df.loc[i, colonne]
                        not in df_liste_domaine_secteur_metier["code_domaine"].unique()
                    ):
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le code domaine de l'activité saisie n'est pas valide.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "codeSecteurActivite":
                    if (
                        df.loc[i, colonne]
                        not in df_liste_domaine_secteur_metier["code_secteur"].unique()
                    ):
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le code secteur de l'activité saisie n'est pas valide.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                    if (
                        str(df.loc[i, colonne])[0]
                        != str(df.loc[i, "codeDomaineActivite"])[0]
                    ):
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le code secteur de l'activité saisie n'est pas cohérent avec le domaine.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "codeNuisanceRadiologique":
                    if df.loc[i, colonne] not in ["EXT", "INT", "EXTINT"]:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le code Nuisance Radiologique saisie n'est pas valide.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "codeTypeContrat":
                    if df.loc[i, colonne] not in type_contrat["code"]:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le code Type de Contrat saisie n'est pas valide.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "CodeMetier":
                    if (
                        df.loc[i, colonne]
                        not in df_liste_domaine_secteur_metier["code_metier"].unique()
                    ):
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le code Metier saisie n'est pas valide.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                    code_domaine_query = df.loc[i, "codeDomaineActivite"]
                    code_secteur_query = df.loc[i, "codeSecteurActivite"]
                    code_metier_query = df.loc[i, "CodeMetier"]

                    if (
                        len(
                            df_liste_domaine_secteur_metier.query(
                                f"code_domaine == {code_domaine_query} and code_secteur == {code_secteur_query} and code_metier == '{code_metier_query}'"
                            )
                        )
                        != 1
                    ):
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i + 1,
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le code Metier saisie n'est pas cohérent avec le secteur et le domaine.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

        st.write("**Veuillez modifier les erreurs dans le premier tableau.**")
        st.dataframe(df_verification, use_container_width=True, hide_index=True)


st.set_page_config(layout="wide")

st.title("Fichier CSV travailleurs")


donnees_colonnes = {
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

data_clean = pd.DataFrame(columns=donnees_colonnes["Colonne"], index=range(1, 2))
df_liste_domaine_secteur_metier = pd.read_csv(
    "pages/liste_domaine_secteur_metier.csv", sep=";"
)

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
                donnees_colonnes["Colonne"], axis=1
            )  # renommer les colonnes

            data_fichier["DATENAISSANCE"] = pd.to_datetime(
                arg=data_fichier["DATENAISSANCE"]
            )
            data_fichier["DATEDEBUT"] = pd.to_datetime(arg=data_fichier["DATEDEBUT"])

            for colonne in [
                "NIR",
                "NOM",
                "PRENOM",
                "SEXE",
                "GROUPE",
                "CLASSEMENT",
                "AUTREEXPOSITION",
                "caractereActivite",
                "codeNuisanceRadiologique",
                "codeTypeContrat",
                "CodeMetier",
            ]:
                data_fichier[colonne] = data_fichier[colonne].astype(
                    "string", copy=False
                )

            for colonne in [
                "NOM",
                "PRENOM",
                "SEXE",
                "CLASSEMENT",
                "AUTREEXPOSITION",
                "codeNuisanceRadiologique",
                "codeTypeContrat",
                "CodeMetier",
            ]:
                data_fichier[colonne] = (
                    data_fichier[colonne].apply(unidecode).str.upper()
                )
            data_fichier["caractereActivite"] = (
                data_fichier["caractereActivite"].apply(unidecode).str.capitalize()
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

    with st.expander("**Tableau**"):
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
                    options=df_liste_domaine_secteur_metier["code_domaine"]
                    .unique()
                    .astype(pd.StringDtype, copy=False),
                ),
                "codeSecteurActivite": st.column_config.SelectboxColumn(
                    required=True,
                    help="Secteur de l'activité.",
                    options=df_liste_domaine_secteur_metier["code_secteur"]
                    .unique()
                    .astype(pd.StringDtype, copy=False),
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
                "CodeMetier": st.column_config.SelectboxColumn(
                    required=True,
                    help="Métier",
                    options=df_liste_domaine_secteur_metier["code_metier"].unique(),
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
    container_verif = st.container()
    container_aide = st.container(border=True)

    with col21:
        if st.button("Mise en forme + Vérification", type="primary"):
            data_tableau["NOM"] = data_tableau["NOM"].str.upper()
            data_tableau["PRENOM"] = data_tableau["PRENOM"].str.upper()
            data_tableau["CLE"] = data_tableau["CLE"].apply("{:0>2}".format)
            data_tableau["SIRET"] = data_tableau["SIRET"].apply("{:0>14}".format)
            data_tableau["DATENAISSANCE"] = pd.to_datetime(
                arg=data_tableau["DATENAISSANCE"]
            )
            data_tableau["DATEDEBUT"] = pd.to_datetime(arg=data_tableau["DATEDEBUT"])

            col1.subheader("**Vérification :**", anchor="verification")
            container_verif.markdown(
                "## :arrow_right: Vérifier les modifications : [Vérification](#verification)"
            )
            verification(data_tableau)
            data_fichier = data_tableau.copy()

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

    if col23.checkbox("Aide ?", value=True):
        container_aide.write("# Aide")
        container_aide.link_button(
            "**Fichier .CSV au format attendu**",
            url="https://docs.siseri.irsn.fr/sites/docssiseri/files/2023-11/Import-travailleur_modele.csv",
        )

        with container_aide.expander("**Colonnes attendues**"):
            st.table(donnees_colonnes)

        with container_aide.expander("**Domaines, Secteurs et Métiers**"):
            st.write(
                "Les 3 informations doivent être cohérents. Vous trouverez les combinaisons possibles sur la page suivante :"
            )
            st.link_button(url="Listes", label="Listes")

        with container_aide.expander("**Autres Expositions**"):
            st.write("RADON")

        with container_aide.expander("**Type de contrat de travail**"):
            st.dataframe(type_contrat["detail"])
