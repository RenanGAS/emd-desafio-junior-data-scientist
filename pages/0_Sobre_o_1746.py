import streamlit as st

from menu import menu

st.set_page_config(page_title="Sobre o 1746", page_icon="📹")

menu()

st.write("## Sobre o 1746")
st.markdown(
"""
O Projeto 1746 tem o objetivo de oferecer atendimento a serviços da prefeitura do Rio de Janeiro. Para isto, possuem o número de telefone 1746, e uma plataforma com site ([1746.rio](https://www.1746.rio/hc/pt-br)) e aplicativo
para população solicitar serviços através de formulários online. Os atendimentos são conhecidos como **chamados**, e no **Google Cloud Platform** está disponível a base de dados dos
chamados realizados desde o início do projeto, contendo informações como tipo, categoria, status, situação e localização do problema (bairro, logradouro, coordenadas geográficas). 

O projeto começou em março de 2011, e tem melhorado o atendimento à população ([Chamadas do 1746 Alcancam Maior Nível de Encerramento no Prazo desde 2021](https://www.dados.rio/post/chamadas-do-1746-alcancam-maior-nivel-de-encerramento-no-prazo-desde-2021)).""")