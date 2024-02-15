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

from typing import Any
import streamlit as st

st.set_page_config(page_title="Sobre o 1746", page_icon="📹")

st.markdown("# Sobre o 1746")
st.write(
"""
O projeto 1746 tem o objetivo de oferecer, através do número 1746, atendimento a serviços da prefeitura do Rio de Janeiro. Para isto, também possuem um site para
população solicitar serviços com o preenchimento de formulários online. Os atendimentos são conhecidos como "chamados", e no Google Cloud Platform está disponível a base de dados dos chamados realizados desde o início do projeto, contendo informações como tipo, categoria, status, situação e localização do problema (bairro, logradouro, coordenadas). 

O projeto começou em março de 2011, e tem melhorado o atendimento à população (citar notícia).
""")