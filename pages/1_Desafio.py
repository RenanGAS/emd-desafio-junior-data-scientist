import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
from shapely import wkt
from geopandas.plotting import plot_polygon_collection
import matplotlib.patches as mpatches

from menu import menu

st.set_page_config(page_title="Desafio")

menu()

st.write("## Desafio")
st.markdown(
    """
    Como desafio foi proposto a solução de questões sobre a base de dados do 1746, utilizando SQL, e a criação de visualizações de dados para as perguntas e para 
    análises criadas por conta do candidato.""")

st.write("## Questionário")
st.markdown(
    """
    Para solução das questões foi utilizado o atributo `data_particao` para otimização das consultas. O conjunto se encontra particionado por mês, e esse atributo 
    é utilizado para registrar a data da partição de um chamado (ex. 2024-01-01, 2024-02-01, 2024-03-01, etc.). Assim, ao ser definido uma data de partição na cláusula 
    `WHERE` de uma consulta, o espaço de busca diminui consideravelmente.
    
    Acompanhado das respostas está disponível o script SQL utilizado. Da mesma forma, também se encontra os scripts SQLs para obtenção dos dados exibidos nos gráficos.""")

with st.container(border=True):
    st.write("##### 1. Quantos chamados foram abertos no dia 01/04/2023?")

    ans1 = st.container(border=True)
    ans1.markdown(
        """
        Neste dia foram abertos 73 chamados. Para obter este resultado, procurou-se por chamados com `data_inicio` = "2023-04-01", e contou-se as ocorrências.""")

    exp_sql_ans1 = st.expander("Script SQL")
    sql_ans1 = '''
    SELECT "01/04/2023" AS Dia, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01";
    '''
    exp_sql_ans1.code(sql_ans1, language="sql")

    with st.container(border=True):
        st.markdown(
            """
            Destes 73 chamados, 24 são do tipo "Poluição Sonora", 9 são de "Estacionamento Irregular" e 8 de "Iluminação Pública". O restante dos chamados tiveram 
            proporções menores. No gráfico abaixo são exibidos os tipos e a quantidade de chamados de cada um neste dia.""")

        st.markdown("###### Gráfico 1")

        num_tipos_chamados = pd.read_csv(f"./data/num_tipos_chamados_diaalvo.csv")

        plt.style.use('_mpl-gallery')

        num_rows = num_tipos_chamados.shape[0]
        num_cols = num_tipos_chamados.shape[1]

        x = 1 + np.arange(num_rows)
        y = num_tipos_chamados["Numero"].values

        fig_num_tipos, ax_num_tipos = plt.subplots(figsize=(9,5))
        ax_num_tipos = sns.barplot(num_tipos_chamados, x="Tipo", y="Numero")
        ax_num_tipos.bar_label(ax_num_tipos.containers[0], fontsize=10);
        ax_num_tipos.grid(False)
        ax_num_tipos.set(xlabel=None, ylabel=None, yticklabels=[])
        ax_num_tipos.spines[:].set_visible(False)
        ax_num_tipos.set_title(label="Número de chamados por tipo em 01/04/2023", fontdict={'fontsize': 16}, pad=22)
        ax_num_tipos.tick_params(axis="x", labelrotation=90)

        st.pyplot(fig_num_tipos)

    exp_sql_graph1 = st.expander("Script SQL")
    sql_graph1 = '''
    SELECT tipo AS Tipo, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" GROUP BY tipo;
    '''
    exp_sql_graph1.code(sql_graph1, language="sql")

    exp_code_graph1 = st.expander("Código")
    code_graph1 = '''
    num_tipos_chamados = pd.read_csv(f"./data/num_tipos_chamados_diaalvo.csv")

    plt.style.use('_mpl-gallery')

    num_rows = num_tipos_chamados.shape[0]
    num_cols = num_tipos_chamados.shape[1]

    x = 1 + np.arange(num_rows)
    y = num_tipos_chamados["Numero"].values

    fig_num_tipos, ax_num_tipos = plt.subplots(figsize=(9,5))
    ax_num_tipos = sns.barplot(num_tipos_chamados, x="Tipo", y="Numero")
    ax_num_tipos.bar_label(ax_num_tipos.containers[0], fontsize=10);
    ax_num_tipos.grid(False)
    ax_num_tipos.set(xlabel=None, ylabel=None, yticklabels=[])
    ax_num_tipos.spines[:].set_visible(False)
    ax_num_tipos.set_title(label="Número de chamados por tipo em 01/04/2023", fontdict={'fontsize': 16}, pad=22)
    ax_num_tipos.tick_params(axis="x", labelrotation=90)

    st.pyplot(fig_num_tipos)
    '''
    exp_code_graph1.code(code_graph1, language="python")

    st.write("##### 2. Qual o tipo de chamado que teve mais reclamações no dia 01/04/2023?")

    ans2 = st.container(border=True)
    ans2.markdown(
        """
        Nenhum chamado teve reclamações neste dia. Para verificação, agrupou-se os chamados por `tipo`, fez-se a soma do campo `reclamacoes` de cada grupo, em seguida a 
        ordenação decrescente dos tipos por soma de reclamações (do tipo com mais reclamações para o com menos) e selecionou-se o primeiro.""")

    exp_sql_ans2 = st.expander("Script SQL")
    sql_ans2 = '''
    SELECT tipo AS Tipo, SUM(reclamacoes) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" GROUP BY tipo ORDER BY Numero DESC LIMIT 1;
    '''
    exp_sql_ans2.code(sql_ans2, language="sql")

    st.write("##### 3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?")

    ans3 = st.container(border=True)
    ans3.markdown(
        """
        Os bairros que mais tiveram chamados neste dia foram Engenho de Dentro (8 chamados), Leblon (6 chamados) e Campo Grande (6 chamados). Para obter estes resultados, 
        agrupou-se os chamados por `id_bairro`, ordenou-se por ordem decrescente de quantidade de chamados, e selecionou-se os 3 primeiros. Em seguida, foi feito o `JOIN` da 
        tabela de bairros com o resultado anterior pela combinação do campo `id_bairro`, obtendo os nomes dos bairros selecionados.""")

    exp_sql_ans3 = st.expander("Script SQL")
    sql_ans3 = '''
    SELECT CHAMADO1746.id_bairro AS ID, BAIRRO.nome AS Nome, CHAMADO1746.NumeroChamados FROM (
        SELECT id_bairro, COUNT(*) as NumeroChamados FROM `datario.administracao_servicos_publicos.chamado_1746` 
            WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" GROUP BY id_bairro ORDER BY NumeroChamados DESC LIMIT 3
    ) as CHAMADO1746, `datario.dados_mestres.bairro` as BAIRRO WHERE CHAMADO1746.id_bairro = BAIRRO.id_bairro;
    '''
    exp_sql_ans3.code(sql_ans3, language="sql")

    st.write("##### 4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?")

    ans4 = st.container(border=True)
    ans4.markdown(
        """
        A subprefeitura com mais chamados abertos neste dia é a Zona Norte com 25 chamados. Utilizou-se um procedimento diferente da questão anterior, associando cada chamado
        ao seu respectivo bairro na tabela de bairros, através de um `INNER JOIN` sob a combinação do campo `id_bairro`, em seguida agrupando os chamados por subprefeitura, e
        ordenando os grupos por soma de chamados, selecionando o primeiro resultado.""")

    exp_sql_ans4 = st.expander("Script SQL")
    sql_ans4 = '''
    SELECT BAIRRO.subprefeitura AS Nome, COUNT(*) as Numero FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 
        INNER JOIN `datario.dados_mestres.bairro` AS BAIRRO ON CHAMADO1746.id_bairro = BAIRRO.id_bairro 
        WHERE CHAMADO1746.data_particao = "2023-04-01" AND CAST(CHAMADO1746.data_inicio AS DATE) = "2023-04-01" GROUP BY BAIRRO.subprefeitura ORDER BY Numero DESC LIMIT 1;
    '''
    exp_sql_ans4.code(sql_ans4, language="sql")

    with st.container(border=True):
        st.markdown(
            """
            A cidade do Rio de Janeiro possui 8 subprefeituras. Um modo interessante de visualizar a distribuição geográfica dos chamados por estas regiões é identificando 
            a localização dos chamados com marcações no mapa do Rio de Janeiro, destacando também os limites de cada subprefeitura. Com isto em mente, utilizou-se o atributo 
            `geometry` dos chamados para mapeá-los no arquivo `Shapefile` da cidade (tipo especial de arquivo com dados geoespaciais) encontrado no site [data.rio](https://datariov2-pcrj.hub.arcgis.com/) 
            ([Limites Coordenadorias Especiais dos Bairros - Subprefeituras](https://datariov2-pcrj.hub.arcgis.com/datasets/e178d4b87fc94d389c73992263024e79_0/explore)). 
            Abaixo encontra-se o resultado.""")

        st.markdown("###### Gráfico 2")

        fig_mapa_subprefeitura, ax_mapa_subprefeitura = plt.subplots(figsize=(9,5))

        localizacao_chamados = pd.read_csv(f"./data/localizacao_chamados_diaalvo.csv")
        crs = {'proj': 'latlong', 'ellps': 'WGS84', 'datum': 'WGS84', 'no_defs': True}
        geo_localizacao_chamados = gpd.GeoDataFrame(localizacao_chamados,crs=crs,geometry=localizacao_chamados["geometry"].apply(wkt.loads))

        rj_subprefeituras=gpd.read_file('./data/rj_subprefeituras.shx')
        rj_subprefeituras["colors"] = ['#bfafb2', '#a3896b', '#3399ff', '#bada55', '#f6546a','#00ff00', '#66cdaa', '#468499', '#ffa500']
        rj_subprefeituras = rj_subprefeituras.set_crs("EPSG:4326")

        rj_subprefeituras = rj_subprefeituras.to_crs('EPSG:5530')
        geo_localizacao_chamados = geo_localizacao_chamados.to_crs('EPSG:5530')

        ax_mapa_subprefeitura = rj_subprefeituras.plot(color=rj_subprefeituras['colors'], edgecolor='black', figsize=(20,20), legend=True)
        ax_mapa_subprefeitura.set_axis_off()

        ax_mapa_subprefeitura.legend([mpatches.Patch(color='#bfafb2'),
                        mpatches.Patch(color='#a3896b'),
                        mpatches.Patch(color='#3399ff'),
                        mpatches.Patch(color='#bada55'),
                        mpatches.Patch(color='#f6546a'),
                        mpatches.Patch(color='#00ff00'),
                        mpatches.Patch(color='#66cdaa'),
                        mpatches.Patch(color='#468499'),
                        mpatches.Patch(color='#ffa500')],
                        ["Centro",
                        "Zona Sul",
                        "Tijuca",
                        "Zona Norte",
                        "Barra da Tijuca",
                        "Jacarepaguá",
                        "Zona Oeste",
                        "Ilhas",
                        "Grande Bangu"], fancybox=True, framealpha=0, prop = { "size": 30 }, loc="upper left", bbox_to_anchor=(-0.2, 1))

        fig_points_chamados, ax_points_chamados = plt.subplots(figsize=(9,5))

        ax_points_chamados=geo_localizacao_chamados.plot(ax=ax_mapa_subprefeitura,color='#8B0000',alpha=1)

        ax_points_chamados.set_title(label="Localização dos chamados feitos no dia 01/04/2023", fontdict={'fontsize': 42}, pad=50, loc="left")

        st.pyplot(ax_points_chamados.figure)

    exp_sql_graph2 = st.expander("Script SQL")
    sql_graph2 = '''
    SELECT tipo, longitude, latitude, geometry FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" AND geometry IS NOT NULL;
    '''
    exp_sql_graph2.code(sql_graph2, language="sql")

    exp_code_graph2 = st.expander("Código")
    code_graph2 = '''
    fig_mapa_subprefeitura, ax_mapa_subprefeitura = plt.subplots(figsize=(9,5))

    localizacao_chamados = pd.read_csv(f"./data/localizacao_chamados_diaalvo.csv")
    crs = {'proj': 'latlong', 'ellps': 'WGS84', 'datum': 'WGS84', 'no_defs': True}
    geo_localizacao_chamados = gpd.GeoDataFrame(localizacao_chamados,crs=crs,geometry=localizacao_chamados["geometry"].apply(wkt.loads))

    rj_subprefeituras=gpd.read_file('./data/rj_subprefeituras.shx')
    rj_subprefeituras["colors"] = ['#bfafb2', '#a3896b', '#3399ff', '#bada55', '#f6546a','#00ff00', '#66cdaa', '#468499', '#ffa500']
    rj_subprefeituras = rj_subprefeituras.set_crs("EPSG:4326")

    rj_subprefeituras = rj_subprefeituras.to_crs('EPSG:5530')
    geo_localizacao_chamados = geo_localizacao_chamados.to_crs('EPSG:5530')

    ax_mapa_subprefeitura = rj_subprefeituras.plot(color=rj_subprefeituras['colors'], edgecolor='black', figsize=(20,20), legend=True)
    ax_mapa_subprefeitura.set_axis_off()

    ax_mapa_subprefeitura.legend([mpatches.Patch(color='#bfafb2'),
                    mpatches.Patch(color='#a3896b'),
                    mpatches.Patch(color='#3399ff'),
                    mpatches.Patch(color='#bada55'),
                    mpatches.Patch(color='#f6546a'),
                    mpatches.Patch(color='#00ff00'),
                    mpatches.Patch(color='#66cdaa'),
                    mpatches.Patch(color='#468499'),
                    mpatches.Patch(color='#ffa500')],
                    ["Centro",
                    "Zona Sul",
                    "Tijuca",
                    "Zona Norte",
                    "Barra da Tijuca",
                    "Jacarepaguá",
                    "Zona Oeste",
                    "Ilhas",
                    "Grande Bangu"], fancybox=True, framealpha=0, prop = { "size": 30 }, loc="upper left", bbox_to_anchor=(-0.2, 1))

    fig_points_chamados, ax_points_chamados = plt.subplots(figsize=(9,5))

    ax_points_chamados=geo_localizacao_chamados.plot(ax=ax_mapa_subprefeitura,color='#8B0000',alpha=1)

    ax_points_chamados.set_title(label="Localização dos chamados feitos no dia 01/04/2023", fontdict={'fontsize': 42}, pad=50, loc="left")

    st.pyplot(ax_points_chamados.figure)
    '''
    exp_code_graph2.code(code_graph2, language="python")

    st.write("##### 5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?")

    ans5 = st.container(border=True)
    ans5.markdown(
        """
        Sim, existe um chamado sem associação a um bairro:""")

    chamado_sem_bairro = pd.read_csv(f"./data/chamado_sem_bairro.csv")
    ans5.dataframe(chamado_sem_bairro)

    ans5.markdown(
        """
        A causa para este chamado em específico, do tipo "Ônibus", pode ser pela vulnerabilidade no formulário de cadastro 
        no site, que permite tanto registros sem a informação do bairro, como com valores incorretos. Outro fator pode ser a opção de fazer chamados anônimos, 
        o que impede a associação do bairro em que o usuário mora (obtido no cadastro da conta) ao bairro do chamado. A presença de chamados sem a identificação do bairro 
        pode causar imprecisões em análises, caso não sejam feitas de forma consciente dos diversos fatores que podem afetar a integridade de um conjunto de dados.""")

    exp_sql_ans5 = st.expander("Script SQL")
    sql_ans5 = '''
    SELECT tipo, subtipo, categoria, id_bairro FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" AND id_bairro IS NULL;

    SELECT tipo, subtipo, categoria FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 
        INNER JOIN `datario.dados_mestres.bairro` AS BAIRRO ON CHAMADO1746.id_bairro = BAIRRO.id_bairro 
        WHERE CHAMADO1746.data_particao = "2023-04-01" AND CAST(CHAMADO1746.data_inicio AS DATE) = "2023-04-01" AND BAIRRO.subprefeitura = "";
    '''
    exp_sql_ans5.code(sql_ans5, language="sql")

    st.write('##### 6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023?')

    ans6 = st.container(border=True)
    ans6.markdown(
        """
        Dentro deste período foram abertos 42.408 chamados deste subtipo. Para obter este resultado, procurou-se chamados com `data_inicio` dentro deste intervalo de tempo e 
        com o subtipo "Perturbação do sossego".""")

    exp_sql_ans6 = st.expander("Script SQL")
    sql_ans6 = '''
    SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2022-01-01" AND "2023-12-01") AND subtipo = "Perturbação do sossego";
    '''
    exp_sql_ans6.code(sql_ans6, language="sql")

    with st.container(border=True):
        st.markdown(
            """
            Deste total de 42.408 chamados, 31.113 foram feitos em 2022, e 11.295 em 2023. Para comparação dos dois anos (2022 e 2023) sobre este aspecto, uma visualização 
            da média diária de chamados deste subtipo por mês, pode ilustrar os períodos no ano de 2023 que tiveram menos chamados em relação a 2022. Com a construção deste 
            gráfico, observou-se que a partir do mês de abril houve uma queda significativa no número de chamados em 2023. Abaixo mostra-se o resultado.""")

        st.markdown("###### Gráfico 3")

        fig_media_diaria_22_23, ax_media_diaria_22_23 = plt.subplots(figsize=(9,5))

        media_diaria_por_mes_22_23 = pd.read_csv(f"./data/media_diaria_por_mes_22_23.csv")
        media_diaria_por_mes_22_23 = media_diaria_por_mes_22_23.drop('data_particao', axis=1)
        media_diaria_por_mes_22_23["Ano"] = ["2022"] * 12 + ["2023"] * 12
        media_diaria_por_mes_22_23["Mes"] = ["Jan", "Fev", "Mar", "Abr", "Maio", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dec"] * 2

        ax_media_diaria_22_23 = sns.lineplot(x = "Mes", y = "MediaDiaria", data = media_diaria_por_mes_22_23, hue = "Ano",
            style = "Ano", palette = "bright", dashes = False, 
            markers = ["o", "o"],  legend="brief")

        ax_media_diaria_22_23.set(xlabel=None, ylabel=None)
        ax_media_diaria_22_23.spines["top"].set_visible(False)
        ax_media_diaria_22_23.spines["right"].set_visible(False)
        ax_media_diaria_22_23.set_title(label='Média diária de chamados por mês, do subtipo "Perturbação do sossego" em 2022 e 2023', fontdict={'fontsize': 18}, pad=40)

        st.pyplot(fig_media_diaria_22_23)

    exp_sql_graph3 = st.expander("Script SQL")
    sql_graph3 = '''
    SELECT data_particao, COUNT(*)/30 AS MediaDiaria FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2022-01-01" AND "2023-12-01") AND subtipo = "Perturbação do sossego" GROUP BY data_particao;
    '''
    exp_sql_graph3.code(sql_graph3, language="sql")

    exp_code_graph3 = st.expander("Código")
    code_graph3 = '''
    fig_media_diaria_22_23, ax_media_diaria_22_23 = plt.subplots(figsize=(9,5))

    media_diaria_por_mes_22_23 = pd.read_csv(f"./data/media_diaria_por_mes_22_23.csv")
    media_diaria_por_mes_22_23 = media_diaria_por_mes_22_23.drop('data_particao', axis=1)
    media_diaria_por_mes_22_23["Ano"] = ["2022"] * 12 + ["2023"] * 12
    media_diaria_por_mes_22_23["Mes"] = ["Jan", "Fev", "Mar", "Abr", "Maio", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dec"] * 2

    ax_media_diaria_22_23 = sns.lineplot(x = "Mes", y = "MediaDiaria", data = media_diaria_por_mes_22_23, hue = "Ano",
        style = "Ano", palette = "bright", dashes = False, 
        markers = ["o", "o"],  legend="brief")

    ax_media_diaria_22_23.set(xlabel=None, ylabel=None)
    ax_media_diaria_22_23.spines["top"].set_visible(False)
    ax_media_diaria_22_23.spines["right"].set_visible(False)
    ax_media_diaria_22_23.set_title(label='Média diária de chamados por mês, do subtipo "Perturbação do sossego" em 2022 e 2023', fontdict={'fontsize': 18}, pad=40)

    st.pyplot(fig_media_diaria_22_23)
    '''
    exp_code_graph3.code(code_graph3, language="python")

    st.write('##### 7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).')

    ans7 = st.container(border=True)
    ans7.markdown(
        """
        Primeiras 5 linhas:""")

    selecao_questao7 = pd.read_csv(f"./data/selecao_questao7.csv")
    ans7.dataframe(selecao_questao7.head())

    ans7.markdown(
        """
        Para obter estes chamados, consultou-se o período em que ocorreram estes eventos na tabela de eventos, e procurou-se por chamados deste subtipo que possuiam 
        `data_inicio` dentro dos determinados intervalos de tempo.""")

    exp_sql_ans7 = st.expander("Script SQL")
    sql_ans7 = '''
    -- Script com as datas colocadas manualmente
    SELECT "Carnaval" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT "Reveillon" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT "Rock in Rio" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego";
    
    -- Script com as datas colocadas automaticamente
    SELECT EVENTOS.evento, CHAMADO1746.id_chamado, CHAMADO1746.tipo, CHAMADO1746.subtipo, CHAMADO1746.id_bairro, CHAMADO1746.situacao, CHAMADO1746.tipo_situacao, CHAMADO1746.status 
        FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 
        INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) 
        WHERE CHAMADO1746.data_particao = "2023-02-01" AND EVENTOS.evento = "Carnaval" AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT EVENTOS.evento, CHAMADO1746.id_chamado, CHAMADO1746.tipo, CHAMADO1746.subtipo, CHAMADO1746.id_bairro, CHAMADO1746.situacao, CHAMADO1746.tipo_situacao, CHAMADO1746.status 
        FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 
        INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) 
        WHERE (CHAMADO1746.data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND EVENTOS.evento = "Reveillon" AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT EVENTOS.evento, CHAMADO1746.id_chamado, CHAMADO1746.tipo, CHAMADO1746.subtipo, CHAMADO1746.id_bairro, CHAMADO1746.situacao, CHAMADO1746.tipo_situacao, CHAMADO1746.status 
        FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 
        INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) 
        WHERE CHAMADO1746.data_particao = "2022-09-01" AND EVENTOS.evento = "Rock in Rio" AND subtipo = "Perturbação do sossego";
    '''
    exp_sql_ans7.code(sql_ans7, language="sql")

    st.write('##### 8. Quantos chamados desse subtipo foram abertos em cada evento?')

    ans8 = st.container(border=True)
    ans8.markdown(
        """
        No Reveillon foram abertos 137 chamados, no Carnaval 241, e no Rock in Rio 834 chamados. Para obter este resultado, fez-se um procedimento parecido com o utilizado na questão acima, com a diferença da criação de seleções separadas para cada evento, para ser feita a contagem do número de chamados abertos em cada um.""")

    exp_sql_ans8 = st.expander("Script SQL")
    sql_ans8 = '''
    -- Script com as datas colocadas manualmente
    SELECT "Carnaval" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT "Reveillon" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT "Rock in Rio" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego";
    
    -- Script com as datas colocadas automaticamente
    SELECT "Carnaval" AS Evento, COUNT(*) AS Numero
        FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 
        INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) 
        WHERE CHAMADO1746.data_particao = "2023-02-01" AND EVENTOS.evento = "Carnaval" AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT "Reveillon" AS Evento, COUNT(*) AS Numero 
        FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 
        INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) 
        WHERE (CHAMADO1746.data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND EVENTOS.evento = "Reveillon" AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT "Rock in Rio" AS Evento, COUNT(*) AS Numero 
        FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 
        INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) 
        WHERE CHAMADO1746.data_particao = "2022-09-01" AND EVENTOS.evento = "Rock in Rio" AND subtipo = "Perturbação do sossego";
    '''
    exp_sql_ans8.code(sql_ans8, language="sql")

    st.write('##### 9. Qual evento teve a maior média diária de chamados abertos desse subtipo?')

    ans9 = st.container(border=True)
    ans9.markdown(
        """
        O evento que teve a maior média diária de chamados foi o Rock in Rio (2022) com 119 chamados por dia. Em seguida está o Carnaval (de 2023) com 60, e o 
        Reveillon (de 2022) com 45. Para obter este resultado, incrementou-se ao procedimento da questão anterior, o agrupamento dos chamados por `data_inicio` 
        em cada seleção, para soma dos chamados feitos em cada dia, e média destes resultados de cada grupo. Uma alternativa mais eficiente 
        seria selecionar todos chamados feitos durante o período de um evento e dividir a quantidade de chamadas pelo número de dias do período, no entanto, a quantidade 
        de dias teria que ser colocada manualmente na consulta ou calculada anteriormente e armazenada numa variável. A primeira solução se torna mais custosa se o 
        agrupamento opera sobre uma quantidade grande de dados, mas evita a contagem de dias.""")

    exp_sql_ans9 = st.expander("Script SQL")
    sql_ans9 = '''
    -- Solução 1
    SELECT Evento, Media FROM (
    SELECT "Carnaval" AS Evento, AVG(Numero) AS Media FROM (
      SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE)
    ) UNION ALL
    SELECT "Reveillon" AS Evento, AVG(Numero) AS Media FROM (
      SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE)
    ) UNION ALL
    SELECT "Rock in Rio" AS Evento, AVG(Numero) AS Media FROM (
      SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE)
    )) ORDER BY Media DESC LIMIT 1;

    -- Solução 2
    DECLARE DiasCarnaval INT64 DEFAULT 0;
    DECLARE DiasReveillon INT64 DEFAULT 0;
    DECLARE DiasRockRio INT64 DEFAULT 0;

    SET DiasCarnaval = (SELECT DATE_DIFF(DATE "2023-02-21", DATE "2023-02-18", DAY) + 1);
    SET DiasReveillon = (SELECT DATE_DIFF(DATE "2023-01-01", DATE "2022-12-30", DAY) + 1);
    SET DiasRockRio = (SELECT DATE_DIFF(DATE "2022-09-04", DATE "2022-09-02", DAY) + DATE_DIFF(DATE "2022-09-11", DATE "2022-09-08", DAY) + 2);

    SELECT "Carnaval" AS Evento, COUNT(*)/DiasCarnaval AS Media FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT "Reveillon" AS Evento, COUNT(*)/DiasReveillon AS Media FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego"
    UNION ALL
    SELECT "Rock in Rio" AS Evento, COUNT(*)/DiasRockRio AS Media FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego";
    '''
    exp_sql_ans9.code(sql_ans9, language="sql")

    with st.container(border=True):
        st.markdown(
            """
            Elaborou-se uma comparação da média diária de chamados deste subtipo no Carnaval e Reveillon em 2020, 2022 e 2023. Abaixo mostra-se o resultado. (O ano de 
            2021 não foi incluído pelo cancelamento do Carnaval)""")

        st.markdown("###### Gráfico 4")

        fig_media_chamados_eventos_20_22_23, ax_media_chamados_eventos_20_22_23 = plt.subplots(figsize=(11,7))

        media_chamados_eventos_20_22_23 = pd.read_csv(f"./data/media_chamados_eventos_20_22_23.csv")

        ax_media_chamados_eventos_20_22_23 = sns.barplot(media_chamados_eventos_20_22_23, x="Evento", y="Media", hue="Ano", palette="hls")
        ax_media_chamados_eventos_20_22_23.legend(title="Ano", loc="upper left", bbox_to_anchor=(-0.1, 1), title_fontsize="20", prop={ "size": 20 })

        ax_media_chamados_eventos_20_22_23.bar_label(ax_media_chamados_eventos_20_22_23.containers[0], fontsize=20);
        ax_media_chamados_eventos_20_22_23.bar_label(ax_media_chamados_eventos_20_22_23.containers[1], fontsize=20);
        ax_media_chamados_eventos_20_22_23.bar_label(ax_media_chamados_eventos_20_22_23.containers[2], fontsize=20);

        ax_media_chamados_eventos_20_22_23.grid(False)
        ax_media_chamados_eventos_20_22_23.set(xlabel=None, ylabel=None, yticklabels=[])
        ax_media_chamados_eventos_20_22_23.tick_params(axis="x", labelsize=20)
        ax_media_chamados_eventos_20_22_23.spines[:].set_visible(False)
        ax_media_chamados_eventos_20_22_23.set_title(label='Média diária de chamados do subtipo "Perturbação do sossego" no Carnaval e Reveillon de 2020, 2022 e 2023', fontdict={'fontsize': 22}, pad=40)

        st.pyplot(fig_media_chamados_eventos_20_22_23)

    exp_sql_graph4 = st.expander("Script SQL")
    sql_graph4 = '''
    SELECT "Carnaval" AS Evento, "2020" AS Ano, IFNULL(AVG(Numero), 0) AS Media FROM(
    SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2020-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2020-02-22" AND "2020-02-25") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE))
    UNION ALL
    SELECT "Carnaval" AS Evento, "2022" AS Ano, IFNULL(AVG(Numero), 0) AS Media FROM(
    SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2022-04-01" AND (CAST(data_inicio AS DATE) BETWEEN "2022-04-20" AND "2022-04-23") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE))
    UNION ALL
    SELECT "Carnaval" AS Evento, "2023" AS Ano, IFNULL(AVG(Numero), 0) AS Media FROM(
    SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE))
    UNION ALL
    SELECT "Reveillon" AS Evento, "2020" AS Ano, IFNULL(AVG(Numero), 0) AS Media FROM(
    SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2020-12-01" AND "2021-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2020-12-30" AND "2021-01-01") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE))
    UNION ALL
    SELECT "Reveillon" AS Evento, "2022" AS Ano, IFNULL(AVG(Numero), 0) AS Media FROM(
    SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE))
    UNION ALL
    SELECT "Reveillon" AS Evento, "2023" AS Ano, IFNULL(AVG(Numero), 0) AS Media FROM(
    SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` 
        WHERE (data_particao BETWEEN "2023-12-01" AND "2024-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2023-12-30" AND "2024-01-01") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE));
    '''
    exp_sql_graph4.code(sql_graph4, language="sql")

    exp_code_graph4 = st.expander("Código")
    code_graph4 = '''
    fig_media_chamados_eventos_20_22_23, ax_media_chamados_eventos_20_22_23 = plt.subplots(figsize=(11,7))

    media_chamados_eventos_20_22_23 = pd.read_csv(f"./data/media_chamados_eventos_20_22_23.csv")

    ax_media_chamados_eventos_20_22_23 = sns.barplot(media_chamados_eventos_20_22_23, x="Evento", y="Media", hue="Ano", palette="hls")
    ax_media_chamados_eventos_20_22_23.legend(title="Ano", loc="upper left", bbox_to_anchor=(-0.1, 1), title_fontsize="20", prop={ "size": 20 })

    ax_media_chamados_eventos_20_22_23.bar_label(ax_media_chamados_eventos_20_22_23.containers[0], fontsize=20);
    ax_media_chamados_eventos_20_22_23.bar_label(ax_media_chamados_eventos_20_22_23.containers[1], fontsize=20);
    ax_media_chamados_eventos_20_22_23.bar_label(ax_media_chamados_eventos_20_22_23.containers[2], fontsize=20);

    ax_media_chamados_eventos_20_22_23.grid(False)
    ax_media_chamados_eventos_20_22_23.set(xlabel=None, ylabel=None, yticklabels=[])
    ax_media_chamados_eventos_20_22_23.tick_params(axis="x", labelsize=20)
    ax_media_chamados_eventos_20_22_23.spines[:].set_visible(False)
    ax_media_chamados_eventos_20_22_23.set_title(label='Média de chamados do subtipo "Perturbação do sossego" no Carnaval e Reveillon de 2020, 2022 e 2023', fontdict={'fontsize': 22}, pad=40)

    st.pyplot(fig_media_chamados_eventos_20_22_23)
    '''
    exp_code_graph4.code(code_graph4, language="python")

    st.write('##### 10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.')

    ans10 = st.container(border=True)
    ans10.markdown(
        """
        A média diária de chamados deste subtipo entre 01/01/2022 e 31/12/2023 foi de 63. Pode-se afirmar que chegou a este valor por causa do ano de 2022, o primeiro ano 
        pós-pandemia, em que houve a diminuição de restrições quanto a promoção de atividades recreativas de interação social (festas e ocupação de bares e clubes). 
        Observa-se no [Gráfico 3](#94141e44) que em 2022 houve uma constância por volta de 80 chamados por dia, com pico de 120 no mês de julho (período de férias escolares). Com isto 
        em mente, pode-se considerar os resultados de 2022 como casos especiais. Nota-se também que nos primeiros meses (janeiro, fevereiro, março e abril), a média 
        diária do subtipo é semelhante nos dois anos (2022 e 2023), resultado que pode ser explicado pelo evento de Carnaval.""")

    exp_sql_ans10 = st.expander("Script SQL")
    sql_ans10 = '''
    SELECT "De 01/01/2022 a 31/12/2023" AS Periodo, AVG(Numero) AS Media FROM (
        SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746`
            WHERE (data_particao BETWEEN "2022-01-01" AND "2023-12-01") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE));
    '''
    exp_sql_ans10.code(sql_ans10, language="sql")
