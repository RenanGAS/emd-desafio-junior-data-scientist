-- Quantos chamados foram abertos no dia 01/04/2023?

SELECT "01/04/2023" AS Dia, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE CAST(data_inicio AS DATE) = "2023-04-01";

-- Qual o tipo de chamado que teve mais reclamações no dia 01/04/2023?

SELECT tipo AS Tipo, SUM(reclamacoes) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" GROUP BY tipo ORDER BY SUM(reclamacoes) DESC LIMIT 1;

-- Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?

SELECT CHAMADO1746.id_bairro AS ID, BAIRRO.nome AS Nome, CHAMADO1746.NumeroChamados FROM (
  SELECT id_bairro, COUNT(*) as NumeroChamados FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" GROUP BY id_bairro ORDER BY NumeroChamados DESC LIMIT 3
) as CHAMADO1746, `datario.dados_mestres.bairro` as BAIRRO WHERE CHAMADO1746.id_bairro = BAIRRO.id_bairro;

-- Qual o nome da subprefeitura com mais chamados abertos nesse dia?

SELECT BAIRRO.subprefeitura AS Nome, COUNT(*) as Numero FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 INNER JOIN `datario.dados_mestres.bairro` AS BAIRRO ON CHAMADO1746.id_bairro = BAIRRO.id_bairro WHERE CHAMADO1746.data_particao = "2023-04-01" AND CAST(CHAMADO1746.data_inicio AS DATE) = "2023-04-01" GROUP BY BAIRRO.subprefeitura ORDER BY Numero DESC LIMIT 1;

-- Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?

SELECT tipo, subtipo, categoria FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" AND id_bairro IS NULL;
SELECT tipo, subtipo, categoria FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 INNER JOIN `datario.dados_mestres.bairro` AS BAIRRO ON CHAMADO1746.id_bairro = BAIRRO.id_bairro WHERE CHAMADO1746.data_particao = "2023-04-01" AND CAST(CHAMADO1746.data_inicio AS DATE) = "2023-04-01" AND BAIRRO.subprefeitura = "";

-- Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?

SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-01-01" AND "2023-12-01") AND subtipo = "Perturbação do sossego";

-- Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).

SELECT "Carnaval" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Reveillon" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-12-30" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Rock in Rio" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego";

-- Quantos chamados desse subtipo foram abertos em cada evento?

SELECT "Carnaval" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Reveillon" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-12-30" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Rock in Rio" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego";

-- Qual evento teve a maior média diária de chamados abertos desse subtipo?

SELECT Evento, Media FROM (
SELECT "Carnaval" AS Evento, AVG(Numero) AS Media FROM (
  SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE)
) UNION ALL
SELECT "Reveillon" AS Evento, AVG(Numero) AS Media FROM (
  SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-12-30" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE)
) UNION ALL
SELECT "Rock in Rio" AS Evento, AVG(Numero) AS Media FROM (
  SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE)
)) ORDER BY Media DESC LIMIT 1;

-- Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.

SELECT "De 01/01/2022 a 31/12/2023" AS Periodo, AVG(Numero) AS Media FROM (
  SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-01-01" AND "2023-12-01") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE));