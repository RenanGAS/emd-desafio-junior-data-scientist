import streamlit as st
from streamlit.logger import get_logger

from menu import menu

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(page_title="Inicio")

    menu()

    st.write("## Desafio EMD-RJ")

    st.markdown(
      """
      Este site foi criado para o desafio técnico do Escritório Municipal de Dados do Rio de Janeiro, para concorrer à vaga de Cientista de Dados Júnior.
      """)

    st.write("## Menu")
    
    st.markdown(
      """
      - **Sobre o 1746**: apresentação do **Projeto 1746**.

      - **Desafio**: questionário sobre o banco de dados do **Projeto 1746**, resolvido através das plataformas **BigQuery** e **Google Colab**, utilizando SQL e Python. 
      Também foram adicionados gráficos e análises dentro do contexto das questões do questionário.

      - **Serviços do 1746**: análise da base de dados em relação ao agrupamento dos chamados como **Serviços**, presente no site [1746.rio](https://www.1746.rio/hc/pt-br).
      """)

if __name__ == "__main__":
    run()
