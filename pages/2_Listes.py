import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

st.set_page_config(layout="wide")

st.title("Listes dans SISERI")

with st.expander("**Domaine, Secteur et Métier**"):
    # select domaine.code, domaine.libelle
    #        , secteur.code, secteur.libelle
    #        , m.code, m.libelle

    # from secteur_activite secteur
    # join secteur_activite domaine on domaine.id = secteur.id_parent
    # left join asso_meti_activ ama on ama.id_secteur_activite = secteur.id
    # join metier m on m.id = ama.id_metier

    # where     secteur.obsolete is FALSE
    #       and m.obsolete is FALSE

    # order by secteur.code, domaine.code, m.code
    # ;

    df_liste_domaine_secteur_metier = pd.read_csv(
        "pages/liste_domaine_secteur_metier.csv", sep=";"
    )
    gb = GridOptionsBuilder.from_dataframe(df_liste_domaine_secteur_metier)
    gb.configure_side_bar()
    gridOptions = gb.build()

    AgGrid(
        data=df_liste_domaine_secteur_metier,
        gridOptions=gridOptions,
        height=500,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        custom_css={
            "#gridToolBar": {
                "padding-bottom": "0px !important",
            }
        },
    )

with st.expander("**Type de contrat de travail**"):
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
    st.dataframe(type_contrat["detail"])
