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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
from shapely import wkt
from geopandas.plotting import plot_polygon_collection
import matplotlib.patches as mpatches

import streamlit as st
from streamlit.hello.utils import show_code

st.set_page_config(page_title="Serviços do 1746")

st.write("## Serviços do 1746")
st.markdown(
    """
    No site do projeto 1746 (1746.rio), são apresentados 28 serviços que enquadram um ou mais tipos de chamados de acordo com seu tema. Por exemplo, o serviço "Meio Ambiente" inclui os tipos "Arborização", "Danos ao meio ambiente", "Poluição", "Educação Ambiental", etc. Como os tipos dos chamados se referem a um problema em específico, havendo muitos para serem abordados, o agrupamento por tema torna viável uma análise dos serviços mais requisitados pela população. Nesta seção apresenta-se a porcentagem de utilização de 8 serviços em 2011, 2015, 2019 e 2023, bem como uma comparação da média diária de chamados para o serviço "Limpeza Urbana" nestes anos.""")

st.write("#### Comparação da utilização dos serviços ")

st.markdown(
    """
    Os 8 serviços selecionados são: Conservação, Iluminação Pública, Limpeza Urbana, Meio Ambiente, Obras e Imóveis, Saúde e Vigilância Sanitária, Trânsito e Transporte. Para obtenção da porcentagem de utilização de um serviço num ano, consultou-se os tipos que ele enquadra no site do projeto, fez-se a contagem dos chamados com estes tipos, e dividiu-se o resultado pelo número total de chamados abertos no ano em questão. Destaca-se os serviços Limpeza Urbana, Trânsito e Iluminação Pública como os serviços mais requisitados nos quatro anos. Abaixo são apresentados os gráficos.""")

fig_porcentagem_servicos = plt.figure(figsize=(14,12))

ax_porcentagem_servicos_11 = fig_porcentagem_servicos.add_subplot(221)
ax_porcentagem_servicos_15 = fig_porcentagem_servicos.add_subplot(222)
ax_porcentagem_servicos_19 = fig_porcentagem_servicos.add_subplot(223)
ax_porcentagem_servicos_23 = fig_porcentagem_servicos.add_subplot(224)

porcentagem_servicos_11 = pd.read_csv(f"./data/porcentagem_servicos_11.csv")
servicos_11_sum = porcentagem_servicos_11["Razao"].sum()
porcentagem_servicos_11.loc[8] = {"Servico": "Outro", "Razao": 1 - servicos_11_sum}

porcentagem_servicos_15 = pd.read_csv(f"./data/porcentagem_servicos_15.csv")
servicos_15_sum = porcentagem_servicos_15["Razao"].sum()
porcentagem_servicos_15.loc[8] = {"Servico": "Outro", "Razao": 1 - servicos_15_sum}

porcentagem_servicos_19 = pd.read_csv(f"./data/porcentagem_servicos_19.csv")
servicos_19_sum = porcentagem_servicos_19["Razao"].sum()
porcentagem_servicos_19.loc[8] = {"Servico": "Outro", "Razao": 1 - servicos_19_sum}

porcentagem_servicos_23 = pd.read_csv(f"./data/porcentagem_servicos_23.csv")
servicos_23_sum = porcentagem_servicos_23["Razao"].sum()
porcentagem_servicos_23.loc[8] = {"Servico": "Outro", "Razao": 0}

ax_porcentagem_servicos_11.pie(porcentagem_servicos_11["Razao"], autopct='%1.1f%%', pctdistance=0.83, radius=1.4, textprops={'fontsize': 16}, colors=['rosybrown', 'gray', 'orange', 'cyan', 'olivedrab', 'violet', 'firebrick', 'yellow', 'lightgreen'])
ax_porcentagem_servicos_15.pie(porcentagem_servicos_15["Razao"], autopct='%1.1f%%', pctdistance=0.83, radius=1.4, textprops={'fontsize': 16}, colors=['rosybrown', 'gray', 'orange', 'cyan', 'olivedrab', 'violet', 'firebrick', 'yellow', 'lightgreen'])
ax_porcentagem_servicos_19.pie(porcentagem_servicos_19["Razao"], autopct='%1.1f%%', pctdistance=0.83, radius=1.4, textprops={'fontsize': 16}, colors=['rosybrown', 'gray', 'orange', 'cyan', 'olivedrab', 'violet', 'firebrick', 'yellow', 'lightgreen'])
ax_porcentagem_servicos_23.pie(porcentagem_servicos_23["Razao"], autopct='%1.1f%%', pctdistance=0.83, radius=1.4, textprops={'fontsize': 16}, colors=['rosybrown', 'gray', 'orange', 'cyan', 'olivedrab', 'violet', 'firebrick', 'yellow', 'lightgreen'])

ax_porcentagem_servicos_11.set_title("2011", pad=30, loc="left", fontdict={"fontsize": 20})
ax_porcentagem_servicos_15.set_title("2015", pad=30, loc="left", fontdict={"fontsize": 20})
ax_porcentagem_servicos_19.set_title("2019", pad=30, loc="left", fontdict={"fontsize": 20})
ax_porcentagem_servicos_23.set_title("2023", pad=30, loc="left", fontdict={"fontsize": 20})

ax_porcentagem_servicos_11.legend([mpatches.Patch(color='rosybrown'),
                mpatches.Patch(color='gray'),
                mpatches.Patch(color='orange'),
                mpatches.Patch(color='cyan'),
                mpatches.Patch(color='olivedrab'),
                mpatches.Patch(color='violet'),
                mpatches.Patch(color='yellow'),
                mpatches.Patch(color='firebrick'),
                mpatches.Patch(color='lightgreen')],
                ["Conservação",
                "Iluminação Pública",
                "Limpeza Urbana",
                "Meio Ambiente",
                "Obras e Imóveis",
                "Saúde e Vigilância Sanitária",
                "Trânsito",
                "Transporte",
                "Outros",], fancybox=True, framealpha=0, prop = { "size": 20 }, loc="upper right", bbox_to_anchor=(4.1, 0.5))

fig_porcentagem_servicos.subplots_adjust(top=0.8)

fig_porcentagem_servicos.suptitle('Porcentagem de chamados abertos por serviço em 2011, 2015, 2019 e 2023', fontsize=26, y=0.95)

st.pyplot(fig_porcentagem_servicos)

exp_sql_graph5 = st.expander(
    """Script SQL
    \nObservação: No script é possível identificar que o tipo "Endereços" está presente em mais de um serviço, afetando a precisão dos gráficos acima.""")
sql_graph5 = '''
DECLARE Total INT64 DEFAULT 0;
SET Total = (SELECT COUNT(*) FROM `datario.administracao_servicos_publicos.chamado_1746` 
    WHERE (data_particao BETWEEN "2023-01-01" AND "2023-12-01") AND tipo IS NOT NULL);

WITH DADOSANO AS (SELECT tipo FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2023-01-01" AND "2023-12-01"))
SELECT "Limpeza Urbana" AS Servico, COUNT(*)/Total AS Razao FROM DADOSANO 
    WHERE tipo IN("Acidente com veículos e equipamentos", "Atendimento ao empregado", "Coleta Seletiva", "Comlurb - Coleta Domiciliar", "Comlurb - Vetores", 
        "Fiscalização de Grande Gerador", "Informações sobre caçamba legal", "Limpeza", "Manejo Arbóreo", "Remoção Gratuita", "Remoção de Caçamba de empresa particular", "Remoção de carcaça de veículo", "Resíduos Sólidos")
UNION ALL
SELECT "Iluminação Pública" AS Servico, COUNT(*)/Total AS Razao FROM DADOSANO WHERE tipo = "Iluminação Pública"
UNION ALL
SELECT "Trânsito" AS Servico, COUNT(*)/Total AS Razao FROM DADOSANO 
    WHERE tipo IN("Endereços", "Engenharia de tráfego", "Estacionamento", "Estacionamento Irregular", "Fiscalização Eletrônica", "Multas", "Regulamentações Viárias", 
        "Semáforo", "Sinalização Gráfica", "Trânsito")
UNION ALL
SELECT "Meio Ambiente" AS Servico, COUNT(*)/Total AS Razao FROM DADOSANO 
    WHERE tipo IN("Adoção de áreas públicas na Fundação Parques e Jardins", "Arborização", "Danos ao meio ambiente", "Educação Ambiental", "Emissão de CMCC - Certidão Municipal de Cumprimento de Condicionantes", 
    "Emissão do Certificado de Adequação de Imóvel - CAI", "Endereços", "Juntada de documentos nos processos administrativos localizados no setor de fiscalização ambiental", "Licença Ambiental", "Manejo Arbóreo", 
    "Mapa de Cobertura Vegetal e Uso do Solo", "Meio Ambiente", "Monitoramento e Fiscalização Ambiental", "Parques urbanos, jardins e praças da Fundação Parques e Jardins", "Poluição", "Vistorias na orla marítima e das lagoas")
UNION ALL
SELECT "Conservação" AS Servico, COUNT(*)/Total AS Razao FROM DADOSANO 
    WHERE tipo IN("Drenagem e Saneamento", "Endereços", "Fiscalização de Instalações Mecânicas", "Mobiliário Urbano", "Monumentos e Chafarizes", "Parques", "Pavimentação", 
    "Praças", "Vias Públicas")
UNION ALL
SELECT "Saúde e Vigilância Sanitária" AS Servico, COUNT(*)/Total AS Razao FROM DADOSANO 
    WHERE tipo IN("Alimentos e estabelecimentos de ensino", "Atendimento Médico", "Atendimento em Unidades de Atenção Secundária", "Atendimento em Unidades de Atenção Terciária", 
    "Atendimento em Unidades de Saúde", "Atividade Física em Unidades de Saúde", "Benefícios / Auxílios", "Concursos Públicos", "Cursos", "Dengue", "Endereços", "Estabelecimentos e serviços de saúde", 
    "Leite Materno", "Mandado Judicial para SMS", "Medicina Veterinária", "Mercados, supermercados e agroindústrias", "Outros estabelecimentos", "Programa Cegonha Carioca", "Programa de Saúde", "Reabilitação Física", "Reabilitação Visual", 
    "Riocard - SMS", "Saúde", "Visa Processos / Licenciamentos", "Zoonoses")
UNION ALL
SELECT "Transporte" AS Servico, COUNT(*)/Total AS Razao FROM DADOSANO 
    WHERE tipo IN("BRT (Corredor expresso de ônibus)", "Bilhetagem eletrônica", "Ciclovias", "Endereços", "Gratuidade de transporte", "Transporte Especial Complementar - TEC", 
    "Transportes", "Táxi", "Táxi.Rio", "Veículo", "Vistoria Anual", "Ônibus")
UNION ALL
SELECT "Obras e Imóveis" AS Servico, COUNT(*)/Total AS Razao FROM DADOSANO 
    WHERE tipo IN("Cópia de projetos", "Drenagem e Saneamento", "Endereços", "Fiscalização de obras", "Imóveis do Patrimônio Municipal", "Imóveis protegidos", "Interdição de imóvel", 
    "Leilão", "Licença de obras", "Obras em prédios públicos - RioUrbe", "Planejamento Urbano - SMPU", "Regularização Urbanística e Fundiária", "Solicitação de obra", "Vias públicas");
'''
exp_sql_graph5.code(sql_graph5, language="sql")

exp_code_graph5 = st.expander("Código")
code_graph5 = '''
fig_porcentagem_servicos = plt.figure(figsize=(14,12))

ax_porcentagem_servicos_11 = fig_porcentagem_servicos.add_subplot(221)
ax_porcentagem_servicos_15 = fig_porcentagem_servicos.add_subplot(222)
ax_porcentagem_servicos_19 = fig_porcentagem_servicos.add_subplot(223)
ax_porcentagem_servicos_23 = fig_porcentagem_servicos.add_subplot(224)

porcentagem_servicos_11 = pd.read_csv(f"./data/porcentagem_servicos_11.csv")
servicos_11_sum = porcentagem_servicos_11["Razao"].sum()
porcentagem_servicos_11.loc[8] = {"Servico": "Outro", "Razao": 1 - servicos_11_sum}

porcentagem_servicos_15 = pd.read_csv(f"./data/porcentagem_servicos_15.csv")
servicos_15_sum = porcentagem_servicos_15["Razao"].sum()
porcentagem_servicos_15.loc[8] = {"Servico": "Outro", "Razao": 1 - servicos_15_sum}

porcentagem_servicos_19 = pd.read_csv(f"./data/porcentagem_servicos_19.csv")
servicos_19_sum = porcentagem_servicos_19["Razao"].sum()
porcentagem_servicos_19.loc[8] = {"Servico": "Outro", "Razao": 1 - servicos_19_sum}

porcentagem_servicos_23 = pd.read_csv(f"./data/porcentagem_servicos_23.csv")
servicos_23_sum = porcentagem_servicos_23["Razao"].sum()
porcentagem_servicos_23.loc[8] = {"Servico": "Outro", "Razao": 0}

ax_porcentagem_servicos_11.pie(porcentagem_servicos_11["Razao"], autopct='%1.1f%%', pctdistance=0.83, radius=1.4, textprops={'fontsize': 16}, colors=['rosybrown', 'gray', 'orange', 'cyan', 'olivedrab', 'violet', 'firebrick', 'yellow', 'lightgreen'])
ax_porcentagem_servicos_15.pie(porcentagem_servicos_15["Razao"], autopct='%1.1f%%', pctdistance=0.83, radius=1.4, textprops={'fontsize': 16}, colors=['rosybrown', 'gray', 'orange', 'cyan', 'olivedrab', 'violet', 'firebrick', 'yellow', 'lightgreen'])
ax_porcentagem_servicos_19.pie(porcentagem_servicos_19["Razao"], autopct='%1.1f%%', pctdistance=0.83, radius=1.4, textprops={'fontsize': 16}, colors=['rosybrown', 'gray', 'orange', 'cyan', 'olivedrab', 'violet', 'firebrick', 'yellow', 'lightgreen'])
ax_porcentagem_servicos_23.pie(porcentagem_servicos_23["Razao"], autopct='%1.1f%%', pctdistance=0.83, radius=1.4, textprops={'fontsize': 16}, colors=['rosybrown', 'gray', 'orange', 'cyan', 'olivedrab', 'violet', 'firebrick', 'yellow', 'lightgreen'])

ax_porcentagem_servicos_11.set_title("2011", pad=30, loc="left", fontdict={"fontsize": 20})
ax_porcentagem_servicos_15.set_title("2015", pad=30, loc="left", fontdict={"fontsize": 20})
ax_porcentagem_servicos_19.set_title("2019", pad=30, loc="left", fontdict={"fontsize": 20})
ax_porcentagem_servicos_23.set_title("2023", pad=30, loc="left", fontdict={"fontsize": 20})

ax_porcentagem_servicos_11.legend([mpatches.Patch(color='rosybrown'),
                mpatches.Patch(color='gray'),
                mpatches.Patch(color='orange'),
                mpatches.Patch(color='cyan'),
                mpatches.Patch(color='olivedrab'),
                mpatches.Patch(color='violet'),
                mpatches.Patch(color='yellow'),
                mpatches.Patch(color='firebrick'),
                mpatches.Patch(color='lightgreen')],
                ["Conservação",
                "Iluminação Pública",
                "Limpeza Urbana",
                "Meio Ambiente",
                "Obras e Imóveis",
                "Saúde e Vigilância Sanitária",
                "Trânsito",
                "Transporte",
                "Outros",], fancybox=True, framealpha=0, prop = { "size": 20 }, loc="upper right", bbox_to_anchor=(4.1, 0.5))

fig_porcentagem_servicos.subplots_adjust(top=0.8)

fig_porcentagem_servicos.suptitle('Porcentagem de chamados abertos por serviço em 2011, 2015, 2019 e 2023', fontsize=26, y=0.95)

st.pyplot(fig_porcentagem_servicos)
'''
exp_code_graph5.code(code_graph5, language="python")

st.write('#### Análise do serviço "Limpeza Urbana"')
st.markdown(
    """
    O serviço com mais chamados abertos nos quatro anos, entitulado "Limpeza Urbana", enquadra os seguintes tipos de chamados: 

    - Acidente com veículos e equipamentos
    - Atendimento ao empregado
    - Coleta Seletiva
    - Comlurb - Coleta Domiciliar
    - Comlurb - Vetores
    - Fiscalização de Grande Gerador
    - Informações sobre caçamba legal
    - Limpeza
    - Manejo Arbóreo
    - Remoção Gratuita
    - Remoção de Caçamba de empresa particular
    - Remoção de carcaça de veículo
    - Resíduos Sólidos""")

st.markdown(
    """
    Para análise da utilização deste serviço nos quatro anos, fez-se gráficos com dados da média diária, por mês, de chamados abertos em cada ano. Do resultado, observa-se que a média, de modo geral, diminui do ano de 2015 para 2019, até 2023. Nota-se que o gráfico de 2011 apresenta o primeiro valor mensal em março, pois foi quando se iniciou o projeto. Abaixo apresenta-se o resultado.""")

fig_media_diaria_por_mes_limpeza_urbana, ax_media_diaria_por_mes_limpeza_urbana = plt.subplots(figsize=(9,5))

media_diaria_por_mes_limpeza_urbana = pd.read_csv(f"./data/media_diaria_por_mes_limpeza_urbana.csv")
media_diaria_por_mes_limpeza_urbana = media_diaria_por_mes_limpeza_urbana.drop('data_particao', axis=1)

missing_11_months = []
missing_11_months.insert(0, {'MediaDiaria': 0.0})
missing_11_months.insert(0, {'MediaDiaria': 0.0})
media_diaria_por_mes_limpeza_urbana = pd.concat([pd.DataFrame(missing_11_months), media_diaria_por_mes_limpeza_urbana], ignore_index=True)

media_diaria_por_mes_limpeza_urbana["Ano"] = ["2011"] * 12 + ["2015"] * 12 + ["2019"] * 12 + ["2023"] * 12
media_diaria_por_mes_limpeza_urbana["Mes"] = ["Jan", "Fev", "Mar", "Abr", "Maio", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dec"] * 4

ax_media_diaria_por_mes_limpeza_urbana = sns.lineplot(x = "Mes", y = "MediaDiaria", data = media_diaria_por_mes_limpeza_urbana, hue = "Ano",
            style = "Ano", palette = "bright", dashes = False, 
            markers = ["o", "o"],  legend="brief")

ax_media_diaria_por_mes_limpeza_urbana.set(xlabel=None, ylabel=None)
ax_media_diaria_por_mes_limpeza_urbana.spines["top"].set_visible(False)
ax_media_diaria_por_mes_limpeza_urbana.spines["right"].set_visible(False)
ax_media_diaria_por_mes_limpeza_urbana.set_title(label='Média diária de chamados por mês, do serviço "Limpeza Urbana" em 2011, 2015, 2019 e 2023', fontdict={'fontsize': 18}, pad=40)

st.pyplot(fig_media_diaria_por_mes_limpeza_urbana)

exp_sql_graph6 = st.expander("Script SQL")
sql_graph6 = '''
SELECT data_particao, COUNT(*)/30 AS MediaDiaria FROM `datario.administracao_servicos_publicos.chamado_1746` 
    WHERE (data_particao BETWEEN "2011-01-01" AND "2011-12-01") AND tipo IN("Acidente com veículos e equipamentos", "Atendimento ao empregado", "Coleta Seletiva", "Comlurb - Coleta Domiciliar", 
    "Comlurb - Vetores", "Fiscalização de Grande Gerador", "Informações sobre caçamba legal", "Limpeza", "Manejo Arbóreo", "Remoção Gratuita", "Remoção de Caçamba de empresa particular", "Remoção de carcaça de veículo", "Resíduos Sólidos") GROUP BY data_particao
UNION ALL
SELECT data_particao, COUNT(*)/30 AS MediaDiaria FROM `datario.administracao_servicos_publicos.chamado_1746` 
    WHERE (data_particao BETWEEN "2015-01-01" AND "2015-12-01") AND tipo IN("Acidente com veículos e equipamentos", "Atendimento ao empregado", "Coleta Seletiva", "Comlurb - Coleta Domiciliar", 
    "Comlurb - Vetores", "Fiscalização de Grande Gerador", "Informações sobre caçamba legal", "Limpeza", "Manejo Arbóreo", "Remoção Gratuita", "Remoção de Caçamba de empresa particular", "Remoção de carcaça de veículo", "Resíduos Sólidos") GROUP BY data_particao
UNION ALL
SELECT data_particao, COUNT(*)/30 AS MediaDiaria FROM `datario.administracao_servicos_publicos.chamado_1746` 
    WHERE (data_particao BETWEEN "2019-01-01" AND "2019-12-01") AND tipo IN("Acidente com veículos e equipamentos", "Atendimento ao empregado", "Coleta Seletiva", "Comlurb - Coleta Domiciliar", 
    "Comlurb - Vetores", "Fiscalização de Grande Gerador", "Informações sobre caçamba legal", "Limpeza", "Manejo Arbóreo", "Remoção Gratuita", "Remoção de Caçamba de empresa particular", "Remoção de carcaça de veículo", "Resíduos Sólidos") GROUP BY data_particao
UNION ALL
SELECT data_particao, COUNT(*)/30 AS MediaDiaria FROM `datario.administracao_servicos_publicos.chamado_1746` 
    WHERE (data_particao BETWEEN "2023-01-01" AND "2023-12-01") AND tipo IN("Acidente com veículos e equipamentos", "Atendimento ao empregado", "Coleta Seletiva", "Comlurb - Coleta Domiciliar", 
    "Comlurb - Vetores", "Fiscalização de Grande Gerador", "Informações sobre caçamba legal", "Limpeza", "Manejo Arbóreo", "Remoção Gratuita", "Remoção de Caçamba de empresa particular", "Remoção de carcaça de veículo", "Resíduos Sólidos") GROUP BY data_particao;
'''
exp_sql_graph6.code(sql_graph6, language="sql")

exp_code_graph6 = st.expander("Código")
code_graph6 = '''
fig_media_diaria_por_mes_limpeza_urbana, ax_media_diaria_por_mes_limpeza_urbana = plt.subplots(figsize=(9,5))

media_diaria_por_mes_limpeza_urbana = pd.read_csv(f"./data/media_diaria_por_mes_limpeza_urbana.csv")
media_diaria_por_mes_limpeza_urbana = media_diaria_por_mes_limpeza_urbana.drop('data_particao', axis=1)

missing_11_months = []
missing_11_months.insert(0, {'MediaDiaria': 0.0})
missing_11_months.insert(0, {'MediaDiaria': 0.0})
media_diaria_por_mes_limpeza_urbana = pd.concat([pd.DataFrame(missing_11_months), media_diaria_por_mes_limpeza_urbana], ignore_index=True)

media_diaria_por_mes_limpeza_urbana["Ano"] = ["2011"] * 12 + ["2015"] * 12 + ["2019"] * 12 + ["2023"] * 12
media_diaria_por_mes_limpeza_urbana["Mes"] = ["Jan", "Fev", "Mar", "Abr", "Maio", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dec"] * 4

ax_media_diaria_por_mes_limpeza_urbana = sns.lineplot(x = "Mes", y = "MediaDiaria", data = media_diaria_por_mes_limpeza_urbana, hue = "Ano",
            style = "Ano", palette = "bright", dashes = False, 
            markers = ["o", "o"],  legend="brief")

ax_media_diaria_por_mes_limpeza_urbana.set(xlabel=None, ylabel=None)
ax_media_diaria_por_mes_limpeza_urbana.spines["top"].set_visible(False)
ax_media_diaria_por_mes_limpeza_urbana.spines["right"].set_visible(False)
ax_media_diaria_por_mes_limpeza_urbana.set_title(label='Média diária de chamados por mês, do serviço "Limpeza Urbana" em 2011, 2015, 2019 e 2023', fontdict={'fontsize': 18}, pad=40)

st.pyplot(fig_media_diaria_por_mes_limpeza_urbana)
'''
exp_code_graph6.code(code_graph6, language="python")
