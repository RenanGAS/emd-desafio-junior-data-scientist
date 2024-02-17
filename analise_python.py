!pip install basedosdados

import basedosdados as bd
import pandas as pd
import datetime

query_chamados_marco_abril = """
    SELECT tipo, id_bairro, data_inicio, data_particao FROM `datario.administracao_servicos_publicos.chamado_1746`
      WHERE data_particao BETWEEN '2023-03-01' AND '2023-04-01'"""
chamados_marco_abril = bd.read_sql(query_chamados_marco_abril, billing_project_id="emd-desafio-data-scientist")

query_bairros = "SELECT id_bairro, nome, subprefeitura FROM `datario.dados_mestres.bairro`"
bairros = bd.read_sql(query_bairros, billing_project_id="emd-desafio-data-scientist")

query_chamados_2021_2022_2023 = """
    SELECT tipo, subtipo, id_bairro, data_inicio, data_particao FROM `datario.administracao_servicos_publicos.chamado_1746`
      WHERE data_particao BETWEEN '2021-12-01' AND '2023-12-01'"""
chamados_2021_2022_2023 = bd.read_sql(query_chamados_2021_2022_2023, billing_project_id="emd-desafio-data-scientist")

query_eventos = "SELECT data_inicial, data_final, evento FROM `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`"
eventos = bd.read_sql(query_eventos, billing_project_id="emd-desafio-data-scientist")

# 1. Quantos chamados foram abertos no dia 01/04/2023?

chamados_marco_abril["data_particao"].astype("datetime64")

particao_abril = datetime.date(2023, 4, 1)
chamados_abril = chamados_marco_abril[chamados_marco_abril["data_particao"] == particao_abril]

dia_alvo = datetime.date(2023, 4, 1)
chamados_diaalvo = chamados_abril[(chamados_abril["data_inicio"].dt.date).values == dia_alvo]

numero_chamados_diaalvo = len(chamados_diaalvo)

print("1. Quantos chamados foram abertos no dia 01/04/2023?")
print(numero_chamados_diaalvo)

# 2. Qual o tipo de chamado que mais teve chamados abertos no dia 01/04/2023?

tipo_maior_soma = ""
maior_soma = 0
tipos_chamados_diaalvo = chamados_diaalvo["tipo"].unique()

for tipo in tipos_chamados_diaalvo:
  soma = (chamados_diaalvo["tipo"] == tipo).sum()
  if soma > maior_soma:
    maior_soma = soma
    tipo_maior_soma = tipo

print("2. Qual o tipo de chamado que mais teve chamados abertos no dia 01/04/2023?")
print(tipo_maior_soma)

# 3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?

ids_bairros = bairros["id_bairro"]

rank_bairros = {
    id_bairro: (chamados_diaalvo["id_bairro"] == id_bairro).sum()
    for id_bairro
    in ids_bairros
    }

rank_bairros = sorted(rank_bairros.items(), key = lambda bairro: bairro[1])

# iat: primeira linha, coluna Nome
top_3_bairros = [
    (bairros[bairros["id_bairro"] == bairro[0]].iat[0, 1], bairro[1])
    for bairro
    in rank_bairros[-3:]
    ]

print("3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?")
print(top_3_bairros)

# 4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?

subprefeituras = bairros["subprefeitura"].unique()
relacao_id_subprefeitura = bairros.set_index("id_bairro")["subprefeitura"].to_dict()

contagem_chamados_subprefeitura_diaalvo = {
    subprefeitura: 0
    for subprefeitura
    in subprefeituras
}

for i in range(numero_chamados_diaalvo):
  id_bairro = chamados_diaalvo.iat[i, 1]

  if id_bairro == None:
    continue

  subprefeitura = relacao_id_subprefeitura[id_bairro]
  contagem_chamados_subprefeitura_diaalvo[subprefeitura] += 1

contagem_chamados_subprefeitura_diaalvo = sorted(contagem_chamados_subprefeitura_diaalvo.items(), key = lambda contagem : contagem[1])

print("4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?")
print(contagem_chamados_subprefeitura_diaalvo[-1])

# 5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?

num_chamados_sem_bairro = 0

for i in range(numero_chamados_diaalvo):
  id_bairro = chamados_diaalvo.iat[i, 1]

  if id_bairro == None:
    num_chamados_sem_bairro += 1
    #print(chamados_diaalvo.iloc[i][0:2])

print("5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?")
print("\nNúmero de chamados sem bairro:", num_chamados_sem_bairro)

# 6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?

data_particoes = pd.date_range(start="01/01/2022",end="31/12/2023", freq="MS").date
chamados_2021_2022_2023["data_particao"].astype("datetime64")

contagem_chamados_particoes = [
    sum((chamados_2021_2022_2023["data_particao"] == particao).values.tolist()
      and (chamados_2021_2022_2023[chamados_2021_2022_2023["data_particao"] == particao]["subtipo"] == "Perturbação do sossego").values.tolist())
    for particao
    in data_particoes
]

print('6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?')
print(sum(contagem_chamados_particoes))

# 7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).

dados_reveillon = eventos.loc[eventos["evento"] == "Reveillon"]
dados_carnaval = eventos.loc[eventos["evento"] == "Carnaval"]
dados_rockrio = eventos.loc[eventos["evento"] == "Rock in Rio"]

periodo_reveillon = []
for i in range(len(dados_reveillon)):
  periodo_reveillon.append(pd.date_range(dados_reveillon.iat[i, 0], dados_reveillon.iat[i, 1]).date.tolist())

periodo_carnaval = []
for i in range(len(dados_carnaval)):
  periodo_carnaval.append(pd.date_range(dados_carnaval.iat[i, 0], dados_carnaval.iat[i, 1]).date.tolist())

periodo_rockrio = []
for i in range(len(dados_rockrio)):
  periodo_rockrio.append(pd.date_range(dados_rockrio.iat[i, 0], dados_rockrio.iat[i, 1]).date.tolist())

set_particoes_reveillon = set()
for i in range(len(periodo_reveillon)):
  particoes_periodo = [
      pd.to_datetime(data).to_numpy().astype('datetime64[M]')
      for data
      in periodo_reveillon[i]
  ]
  set_particoes_reveillon.update(particoes_periodo)

list_particoes_reveillon = list(set_particoes_reveillon)

set_particoes_carnaval = set()
for i in range(len(periodo_carnaval)):
  particoes_periodo = [
      pd.to_datetime(data).to_numpy().astype('datetime64[M]')
      for data
      in periodo_carnaval[i]
  ]
  set_particoes_carnaval.update(particoes_periodo)

list_particoes_carnaval = list(set_particoes_carnaval)

set_particoes_rockrio = set()
for i in range(len(periodo_rockrio)):
  particoes_periodo = [
      pd.to_datetime(data).to_numpy().astype('datetime64[M]')
      for data
      in periodo_rockrio[i]
  ]
  set_particoes_rockrio.update(particoes_periodo)

list_particoes_rockrio = list(set_particoes_rockrio)

selecao_chamados_subtipo_eventos = []

for particao in list_particoes_reveillon:
  dados_particao = chamados_2021_2022_2023[chamados_2021_2022_2023["data_particao"] == particao]

  for periodo in periodo_reveillon:
    for data in periodo:
      dados_data = dados_particao[dados_particao["data_inicio"].dt.date == data]
      selecao_chamados_subtipo_eventos.extend(dados_data[dados_data["subtipo"] == "Perturbação do sossego"].values.tolist())

for particao in list_particoes_carnaval:
  dados_particao = chamados_2021_2022_2023[chamados_2021_2022_2023["data_particao"] == particao]

  for periodo in periodo_carnaval:
    for data in periodo:
      dados_data = dados_particao[dados_particao["data_inicio"].dt.date == data]
      selecao_chamados_subtipo_eventos.extend(dados_data[dados_data["subtipo"] == "Perturbação do sossego"].values.tolist())
        
for particao in list_particoes_rockrio:
  dados_particao = chamados_2021_2022_2023[chamados_2021_2022_2023["data_particao"] == particao]

  for periodo in periodo_rockrio:
    for data in periodo:
      dados_data = dados_particao[dados_particao["data_inicio"].dt.date == data]
      selecao_chamados_subtipo_eventos.extend(dados_data[dados_data["subtipo"] == "Perturbação do sossego"].values.tolist())

df_selecao_chamados_subtipo_eventos = pd.DataFrame(selecao_chamados_subtipo_eventos, columns=["tipo", "subtipo", "id_bairro", "data_inicio", "data_particao"])

print("7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).")
print(df_selecao_chamados_subtipo_eventos.head())
print("Número de linhas: ", df_selecao_chamados_subtipo_eventos.shape[0])

# 8. Quantos chamados desse subtipo foram abertos em cada evento?
# 9. Qual evento teve a maior média diária de chamados abertos desse subtipo?

dados_reveillon = eventos.loc[eventos["evento"] == "Reveillon"]
dados_carnaval = eventos.loc[eventos["evento"] == "Carnaval"]
dados_rockrio = eventos.loc[eventos["evento"] == "Rock in Rio"]

periodo_reveillon = []
num_dias_reveillon = 0
for i in range(len(dados_reveillon)):
  datas_reveillon = pd.date_range(dados_reveillon.iat[i, 0], dados_reveillon.iat[i, 1]).date.tolist()
  periodo_reveillon.append(datas_reveillon)
  num_dias_reveillon += len(datas_reveillon)

num_dias_carnaval = 0
periodo_carnaval = []
for i in range(len(dados_carnaval)):
  datas_carnaval = pd.date_range(dados_carnaval.iat[i, 0], dados_carnaval.iat[i, 1]).date.tolist()
  periodo_carnaval.append(datas_carnaval)
  num_dias_carnaval += len(datas_carnaval)

num_dias_rockrio = 0
periodo_rockrio = []
for i in range(len(dados_rockrio)):
  datas_rockrio = pd.date_range(dados_rockrio.iat[i, 0], dados_rockrio.iat[i, 1]).date.tolist()
  periodo_rockrio.append(datas_rockrio)
  num_dias_rockrio += len(datas_rockrio)

set_particoes_reveillon = set()
for i in range(len(periodo_reveillon)):
  particoes_periodo = [
      pd.to_datetime(data).to_numpy().astype('datetime64[M]')
      for data
      in periodo_reveillon[i]
  ]
  set_particoes_reveillon.update(particoes_periodo)

list_particoes_reveillon = list(set_particoes_reveillon)

set_particoes_carnaval = set()
for i in range(len(periodo_carnaval)):
  particoes_periodo = [
      pd.to_datetime(data).to_numpy().astype('datetime64[M]')
      for data
      in periodo_carnaval[i]
  ]
  set_particoes_carnaval.update(particoes_periodo)

list_particoes_carnaval = list(set_particoes_carnaval)

set_particoes_rockrio = set()
for i in range(len(periodo_rockrio)):
  particoes_periodo = [
      pd.to_datetime(data).to_numpy().astype('datetime64[M]')
      for data
      in periodo_rockrio[i]
  ]
  set_particoes_rockrio.update(particoes_periodo)

list_particoes_rockrio = list(set_particoes_rockrio)

soma_reveillon = 0
for particao in list_particoes_reveillon:
  dados_particao = chamados_2021_2022_2023[chamados_2021_2022_2023["data_particao"] == particao]

  for periodo in periodo_reveillon:
    chamados_reveillon = [
        sum((dados_particao["data_inicio"].dt.date == data).values.tolist()
          and (dados_particao[dados_particao["data_inicio"].dt.date == data]["subtipo"] == "Perturbação do sossego").values.tolist())
        for data
        in periodo
    ]

    soma_reveillon += sum(chamados_reveillon)

soma_carnaval = 0
for particao in list_particoes_carnaval:
  dados_particao = chamados_2021_2022_2023[chamados_2021_2022_2023["data_particao"] == particao]

  for periodo in periodo_carnaval:
    chamados_carnaval = [
        sum((dados_particao["data_inicio"].dt.date == data).values.tolist()
          and (dados_particao[dados_particao["data_inicio"].dt.date == data]["subtipo"] == "Perturbação do sossego").values.tolist())
        for data
        in periodo
    ]

    soma_carnaval += sum(chamados_carnaval)

soma_rockrio = 0
for particao in list_particoes_rockrio:
  dados_particao = chamados_2021_2022_2023[chamados_2021_2022_2023["data_particao"] == particao]

  for periodo in periodo_rockrio:
    chamados_rockrio = [
        sum((dados_particao["data_inicio"].dt.date == data).values.tolist()
          and (dados_particao[dados_particao["data_inicio"].dt.date == data]["subtipo"] == "Perturbação do sossego").values.tolist())
        for data
        in periodo
    ]

    soma_rockrio += sum(chamados_rockrio)

print("8. Quantos chamados desse subtipo foram abertos em cada evento?")
print("Número de chamados no Reveillon: ", soma_reveillon)
print("Número de chamados no Carnaval: ", soma_carnaval)
print("Número de chamados no Rock in Rio: ", soma_rockrio)

print("9. Qual evento teve a maior média diária de chamados abertos desse subtipo?")
print("Média Reveillon: ", soma_reveillon/num_dias_reveillon)
print("Média Carnaval: ", soma_carnaval/num_dias_carnaval)
print("Média Rock in Rio: ", soma_rockrio/num_dias_rockrio)

# 10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.

data_particoes = pd.date_range(start="01/01/2022",end="31/12/2023", freq="MS").date

soma_chamados = 0
numero_dias = 0
for particao in data_particoes:
  dados_particao = chamados_2021_2022_2023[chamados_2021_2022_2023["data_particao"] == particao]
  dias = dados_particao["data_inicio"].dt.date.unique()

  chamados_subtipo_dia_mes = [
      sum((dados_particao["data_inicio"].dt.date == dia).values.tolist()
        and (dados_particao[dados_particao["data_inicio"].dt.date == dia]["subtipo"] == "Perturbação do sossego").values.tolist()
      )
      for dia
      in dias
  ]

  soma_chamados += sum(chamados_subtipo_dia_mes)
  numero_dias += len(chamados_subtipo_dia_mes) - chamados_subtipo_dia_mes.count(0)

print("10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.")
print("Média diária do subtipo de 01/01/2022 até 31/12/2023.", soma_chamados/numero_dias)