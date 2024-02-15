import streamlit as st

def menu():
    st.sidebar.markdown(
        """
        <style>
        .st-emotion-cache-vk3wp9 {
            width: 240px !important;
            max-width: 240px !important;
        }
        .st-emotion-cache-1wyffs1 {
            width: 240px !important;
            max-width: 240px !important;
        }
        div[data-testid="stSidebarContent"] {
            background-image: linear-gradient(#02487c, #02487c);
            color: white;
            height: 100%;
            width: 240px;
        }
        .st-emotion-cache-pkbazv {
            color: white;
        }
        button[title="View fullscreen"]{
            visibility: hidden;
        }
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.image('assets/logo_rj_prefeitura.png')
    st.sidebar.page_link("Inicio.py", label="Início")
    st.sidebar.page_link("pages/0_Sobre_o_1746.py", label="Sobre o 1746")
    st.sidebar.page_link("pages/1_Desafio.py", label="Desafio")
    st.sidebar.page_link("pages/2_Servicos_do_1746.py", label="Serviços do 1746")