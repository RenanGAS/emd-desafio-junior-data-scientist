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

st.set_page_config(page_title="Sobre o 1746", page_icon="📹")
st.markdown("# Sobre o 1746")
st.write(
    """This app shows how you can use Streamlit to build cool animations.
It displays an animated fractal based on the the Julia Set. Use the slider
to tune different parameters."""
)

st.write("1. Quantos chamados foram abertos no dia 01/04/2023?")

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

st.write("4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?")

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

st.write('6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023?')

fig_media_diaria_22_23, ax_media_diaria_22_23 = plt.subplots(figsize=(9,5))

media_diaria_por_mes_22_23 = pd.read_csv(f"./data/media_diaria_por_mes_22_23.csv")
media_diaria_por_mes_22_23 = media_diaria_por_mes_22_23.drop('data_particao', axis=1)
media_diaria_por_mes_22_23["Ano"] = ["2022"] * 12 + ["2023"] * 12
media_diaria_por_mes_22_23["Mes"] = ["Jan", "Fev", "Mar", "Abr", "Maio", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dec"] * 2

ax_media_diaria_22_23 = sns.lineplot(x = "Mes", y = "MediaDiaria", data = media_diaria_por_mes_22_23, hue = "Ano",
            style = "Ano", palette = "viridis", dashes = False, 
            markers = ["o", "o"],  legend="brief",)

ax_media_diaria_22_23.set(xlabel=None, ylabel=None)
ax_media_diaria_22_23.spines["top"].set_visible(False)
ax_media_diaria_22_23.spines["right"].set_visible(False)
ax_media_diaria_22_23.set_title(label='Média diária de chamados por mês, do tipo "Perturbação do sossego" em 2022 e 2023', fontdict={'fontsize': 18}, pad=40)

st.pyplot(fig_media_diaria_22_23)

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
ax_media_chamados_eventos_20_22_23.set_title(label='Média de chamados do tipo "Perturbação do sossego" no Carnaval e Reveillon de 2020, 2022 e 2023', fontdict={'fontsize': 22}, pad=40)

st.pyplot(fig_media_chamados_eventos_20_22_23)