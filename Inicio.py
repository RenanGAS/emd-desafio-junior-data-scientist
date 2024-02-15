# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(page_title="Inicio")

    st.write("# Desafio EMD-RJ")

    st.markdown(
      """
      Este site foi criado para o desafio técnico do Escritório Municipal de Dados do Rio de Janeiro, para concorrer à vaga de Cientista de Dados Júnior.
      """)

    st.write("# Estrutura do App")

    st.markdown(
      """
      - Sobre o 1746: apresenta-se o projeto 1746.

      - Desafio: questionário sobre o banco de dados do projeto 1746, resolvido através da plataforma BigQuery, utilizando SQL. 
      Também foram adicionados gráficos e análises dentro do contexto das questões do questionário. 

      - Serviços do 1746: análise da base de dados em relação ao agrupamento dos chamados como "Serviços", presente no site 1746.rio.
      """)

if __name__ == "__main__":
    run()
