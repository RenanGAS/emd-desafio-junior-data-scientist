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

# 1. Quantos chamados foram abertos no dia 01/04/2023?

chamados_marco_abril["data_particao"].astype("datetime64")

particao_abril = datetime.date(2023, 4, 1)
chamados_abril = chamados_marco_abril[chamados_marco_abril["data_particao"] == particao_abril]

dia_alvo = datetime.date(2023, 4, 1)
chamados_diaalvo = chamados_abril[(chamados_abril["data_inicio"].dt.date).values == dia_alvo]

numero_chamados_diaalvo = len(chamados_diaalvo)

print(numero_chamados_diaalvo)

# 2. Qual o tipo de chamado que mais teve chamados abertos no dia 01/04/2023?

tipo_maior_soma = ""
maior_soma = 0
tipos = chamados_diaalvo["tipo"].unique()

for tipo in tipos:
  soma = (chamados_diaalvo["tipo"] == tipo).sum()
  if soma > maior_soma:
    maior_soma = soma
    tipo_maior_soma = tipo

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

print(contagem_chamados_subprefeitura_diaalvo[-1])

# 5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?

num_chamados_sem_bairro = 0

for i in range(numero_chamados_diaalvo):
  id_bairro = chamados_diaalvo.iat[i, 1]

  if id_bairro == None:
    num_chamados_sem_bairro += 1
    print(chamados_diaalvo.iloc[i][0:2])

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

print(sum(contagem_chamados_particoes))