import streamlit as st
import pandas as pd
import datetime as dt
import re
from unidecode import unidecode
import numpy as np
import datetime as dt


def verification(df: pd.DataFrame):
    df_verification = pd.DataFrame(
        columns=("Numero_Ligne", "NIR", "Nom_Colonne", "Valeur", "Erreur"),
        dtype="string",
    )

    with col1.expander("**Vérif.**", expanded=True):
        # for i in range(1, df.shape[0] + 1):
        for i in df.index:
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
                                        "Numero_Ligne": i,
                                        "NIR": df.loc[i, "NIR"],
                                        "Nom_Colonne": colonne,
                                        "Valeur": df.loc[i, colonne],
                                        "Erreur": "Numéro de sécurité sociale n'est pas au bon format",
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
                                            "Numero_Ligne": i,
                                            "NIR": df.loc[i, "NIR"],
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Numéro de SIRET n'est pas au bon format.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "TYPE_MESURE":
                    if df.loc[i, colonne] not in type_mesure["code"]:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i,
                                            "NIR": df.loc[i, "NIR"],
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le type de mesure n'est pas correct.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "TYPE_DOSIMETRE":
                    if df.loc[i, colonne] not in type_dosimetre:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i,
                                            "NIR": df.loc[i, "NIR"],
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Le type de dosimetre n'est pas correct.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne.startswith("DATE_"):
                    if df.loc[i, "DATE_DEBUT_PORT"] >= df.loc[i, "DATE_FIN_PORT"]:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i,
                                            "NIR": df.loc[i, "NIR"],
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": "Problème dans date+heure de port. La date+heure de fin de port doit être supérieure à la date+heure de début.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

                elif colonne == "VALEUR":
                    if round(float(df.loc[i, colonne]), 3) == 0.000:
                        df_verification = pd.concat(
                            [
                                df_verification,
                                pd.DataFrame(
                                    [
                                        {
                                            "Numero_Ligne": i,
                                            "NIR": df.loc[i, "NIR"],
                                            "Nom_Colonne": colonne,
                                            "Valeur": df.loc[i, colonne],
                                            "Erreur": f"Attention : La dose sera affichée dans SISERI telle quelle : {float(df.loc[i, colonne]):.3f} mSv.",
                                        }
                                    ]
                                ),
                            ],
                            ignore_index=True,
                        )

        st.write("**Veuillez modifier les erreurs dans le premier tableau.**")
        st.write(
            "D'autres erreurs ne sont détectables que dans SISERI, lors de l'importation."
        )
        st.dataframe(
            df_verification,
            use_container_width=True,
            hide_index=True,
            height=min(300 + len(data_fichier) * 60, 500),
        )


st.set_page_config(layout="wide")

st.title("Fichier CSV dosimétrie opérationnelle")

if "effacer_erreurs_fichiers_csv" not in st.session_state:
    st.session_state["effacer_erreurs_fichiers_csv"] = False

donnees_colonnes = {
    "Colonne": [
        "NIR",
        "SIRET",
        "LIEU",
        "ZONE",
        "TYPE_MESURE",
        "TYPE_DOSIMETRE",
        "DATE_DEBUT_PORT",
        "DATE_FIN_PORT",
        "VALEUR",
        "ACTIVITE",
        "CODE_METROLOGIE",
    ],
    "Description": [
        "Numéro de sécurité sociale (13 chiffres)",
        "SIRET de rattachement (14 chiffres)",
        "Lieu de l'activité dans l'INB",
        "Zone de l'activité dans l'INB",
        "Type de mesure (Hp(10), Hp(0.07), neutron, etc..)",
        "Type de dosimètre utilisé.",
        "Date et heure de début de port du dosimètre",
        "Date et heure de fin de port du dosimètre",
        "valeur de la dose en mSv",
        "Type d'activité dans l'INB",
        "Code 'C' si modification d'une dose reçue auparavant.",
    ],
    "Spécificités": [
        "-Obligatoire. -Numéro de sécurité sociale. -13 caractères. - Le NIA pour les travailleurs étrangers est également accepté.",
        "-Obligatoire. -SIRET de l'établissement, connu dans SISERI",
        "-Obligatoire.",
        "-Obligatoire.",
        "-Obligatoire.",
        "-Obligatoire.",
        "-Obligatoire. -Format jj/mm/aaaa hh:mm",
        "-Obligatoire. -Format jj/mm/aaaa hh:mm",
        "-Obligatoire. -séparateur décimal est un point. Les valeurs seront arrondies à 0.000 mSv",
        "-Obligatoire. -Zone de l'activité dans l'INB",
        'code "C" uniquement disponible.',
    ],
}

type_mesure = {
    "code": ("OPE-HP10-PHO", "OPE-HP10-NEURAP", "OPE-HP007"),
    "detail": ("Hp(10) photons", "Hp(10) neutrons rapides", "Hp(0,07)"),
}

type_dosimetre = (
    "DOSICARD",
    "EPD",
    "EPD MK3",
    "EPD N2",
    "Saphydose Gamma I",
    "DMC 2000 GN",
    "DMC 3000",
    "DMC",
    "DMC 2000",
    "DMC 2000 S",
    "DMC 2000 X",
    "DMC 2000 XB",
    "DMX 100",
    "DMX 90",
)

data_clean = pd.DataFrame(columns=donnees_colonnes["Colonne"], index=range(1, 1))

col1, col2 = st.columns([0.7, 0.3], gap="small")

with col1:
    uploaded_file = st.file_uploader(
        "**Importer un fichier .CSV au format attendu par SISERI** (sinon remplir le Tableau ci-dessous)",
        type=["csv"],
        accept_multiple_files=False,
    )

    if uploaded_file is None:
        data_fichier = data_clean.copy()

    elif uploaded_file is not None:
        data_fichier = pd.read_csv(uploaded_file, sep=";")

        if data_fichier.shape[1] != 13 and data_fichier.shape[1] != 11:
            st.error(
                "Le fichier importé ne contient pas les colonnes attendues. Veuillez vous référer à l'aide, à droite."
            )
            st.write("Colonnes affichées : ")
            st.write(data_fichier.columns.tolist())
            data_fichier = data_clean.copy()

        else:
            # st.dataframe(data_fichier, use_container_width=True)
            if data_fichier.shape[1] == 13:
                if (
                    col1.button(
                        "Effacer les lignes sans erreurs",
                        type="secondary",
                    )
                    or st.session_state["effacer_erreurs_fichiers_csv"] == True
                ):
                    data_fichier = data_fichier.dropna(subset=["CODE_ERREUR"])
                    st.session_state["effacer_erreurs_fichiers_csv"] = True

            if data_fichier.shape[1] == 11:
                data_fichier = data_fichier.set_axis(
                    donnees_colonnes["Colonne"], axis=1
                )  # renommer les colonnes
            data_fichier.index = data_fichier.index + 1  # change l'index
            data_fichier.index.name = "id"  # nomme l'index

            data_fichier["DATE_DEBUT_PORT"] = pd.to_datetime(
                arg=data_fichier["DATE_DEBUT_PORT"],
                format="%d/%m/%Y %H:%M",
                exact=False,
            )
            data_fichier["DATE_FIN_PORT"] = pd.to_datetime(
                arg=data_fichier["DATE_FIN_PORT"],
                format="%d/%m/%Y %H:%M",
                exact=False,
            )

            for colonne in [
                "NIR",
                "LIEU",
                "ZONE",
                "TYPE_MESURE",
                "TYPE_DOSIMETRE",
                "CODE_METROLOGIE",
            ]:
                try:
                    data_fichier[colonne] = data_fichier[colonne].apply(unidecode)
                except:
                    pass
                finally:
                    data_fichier[colonne] = (
                        data_fichier[colonne].astype("string", copy=False).str.upper()
                    )
            data_fichier["ACTIVITE"] = data_fichier["ACTIVITE"].astype(
                "string", copy=False
            )

            for colonne in [
                "SIRET",
            ]:
                data_fichier[colonne] = (
                    data_fichier[colonne]
                    .replace("--", 0)
                    .astype("int64", copy=False, errors="ignore")
                )
            data_fichier["SIRET"] = data_fichier["SIRET"].apply("{:0>14}".format)
            data_fichier["VALEUR"] = data_fichier["VALEUR"].apply("{:.3f}".format)

    with st.expander("**Tableau**", expanded=True):
        data_tableau = st.data_editor(
            data_fichier,
            use_container_width=True,
            hide_index=False,
            num_rows="dynamic",
            height=min(300 + len(data_fichier) * 60, 999),
            width=999,
            column_config={
                "id": st.column_config.Column(disabled=True, required=False),
                "NIR": st.column_config.TextColumn(
                    required=True,
                    help="Numéro de sécurité sociale",
                    max_chars=13,
                    validate="^[12][0-9]{2}[0-9]{2}(2[AB]|[0-9]{2})[0-9]{3}[0-9]{3}$",
                ),
                "SIRET": st.column_config.NumberColumn(
                    required=True,
                    help="SIRET",
                    format="%d",
                    min_value=0,
                    max_value=99999999999999,
                ),
                "LIEU": st.column_config.TextColumn(required=True),
                "ZONE": st.column_config.TextColumn(required=True),
                "TYPE_MESURE": st.column_config.SelectboxColumn(
                    required=True,
                    help="Type de mesure",
                    options=type_mesure["code"],
                ),
                "TYPE_DOSIMETRE": st.column_config.SelectboxColumn(
                    required=True,
                    help="Type de dosimetre",
                    options=type_dosimetre,
                ),
                "DATE_DEBUT_PORT": st.column_config.DatetimeColumn(
                    required=True,
                    help="Date de début de port (JJ/MM/AAAA HH:mm)",
                    max_value=dt.datetime.today(),
                    format="DD/MM/YYYY HH:mm",
                ),
                "DATE_FIN_PORT": st.column_config.DatetimeColumn(
                    required=True,
                    help="Date de fin de port (JJ/MM/AAAA HH:mm)",
                    format="DD/MM/YYYY HH:mm",
                    max_value=dt.datetime.today(),
                ),
                "VALEUR": st.column_config.NumberColumn(
                    required=True,
                    help="Valeur de la dose",
                    format="%.3f",
                    min_value=0,
                ),
                "CODE_METROLOGIE": st.column_config.SelectboxColumn(
                    required=False,
                    help="Correction d'une précédente dose ?",
                    options=["C"],
                ),
            },
        )


with col2:
    col21, col22, col23 = st.columns(3)
    container_verif = st.container()
    container_aide = st.container(border=True)

    with col21:
        if st.button("Mise en forme + Vérification", type="primary"):
            data_tableau["SIRET"] = data_tableau["SIRET"].apply("{:0>14}".format)

            col1.subheader("**Vérification :**", anchor="verification")
            container_verif.markdown(
                "## :arrow_right: Vérifier les modifications : [Vérification](#verification)"
            )
            verification(data_tableau)
            data_fichier = data_tableau.copy()

            with col22:
                if st.download_button(
                    label="Télécharger le tableau",
                    data=data_tableau[
                        [
                            "NIR",
                            "SIRET",
                            "LIEU",
                            "ZONE",
                            "TYPE_MESURE",
                            "TYPE_DOSIMETRE",
                            "DATE_DEBUT_PORT",
                            "DATE_FIN_PORT",
                            "VALEUR",
                            "ACTIVITE",
                        ]
                    ].to_csv(
                        sep=";",
                        index=False,
                        date_format="%d/%m/%Y %H:%M",
                        encoding="utf-8",
                    ),
                    file_name=f"dos_ope_{dt.datetime.now()}.csv",
                    mime="text/csv",
                    type="primary",
                ):
                    st.rerun()

    if col23.checkbox("Aide ?", value=True):
        container_aide.write("# Aide")
        col_aide_1, col_aide_2 = container_aide.columns(2)
        col_aide_1.link_button(
            "**Fichier .CSV au format attendu**",
            url="https://admin.docs.siseri.irsn.fr/sites/docssiseri/files/2024-05/Import-dosimetrie-operationnelle_modele.csv",
        )
        col_aide_2.link_button(
            "**Aide sur le site d'aide SISERI**",
            url="https://docs.siseri.irsn.fr/transmissions-de-donnees/format-et-contenu-des-fichiers/dosimetrie-operationnelle",
        )

        with container_aide.expander("**Colonnes attendues**"):
            st.dataframe(donnees_colonnes, use_container_width=True, height=450)

        with container_aide.expander("**Type de mesure**"):
            st.dataframe(type_mesure, use_container_width=True)
