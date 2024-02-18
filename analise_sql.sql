-- Desafio Técnico
-- Recomenda-se realizar a execução dos scripts na plataforma **BigQuery**. As instruções para execução estão em [InstrucoesExecucao.md](InstrucoesExecucao.md)

-- 1. Quantos chamados foram abertos no dia 01/04/2023?

SELECT "01/04/2023" AS Dia, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01";

-- 2. Qual o tipo de chamado que mais teve chamados abertos no dia 01/04/2023?

SELECT tipo AS Tipo, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" GROUP BY tipo ORDER BY Numero DESC LIMIT 1;

-- 3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?

SELECT CHAMADO1746.id_bairro AS ID, BAIRRO.nome AS Nome, CHAMADO1746.NumeroChamados FROM (
  SELECT id_bairro, COUNT(*) as NumeroChamados FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" GROUP BY id_bairro ORDER BY NumeroChamados DESC LIMIT 3
) as CHAMADO1746, `datario.dados_mestres.bairro` as BAIRRO WHERE CHAMADO1746.id_bairro = BAIRRO.id_bairro;

-- 4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?

SELECT BAIRRO.subprefeitura AS Nome, COUNT(*) as Numero FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 INNER JOIN `datario.dados_mestres.bairro` AS BAIRRO ON CHAMADO1746.id_bairro = BAIRRO.id_bairro WHERE CHAMADO1746.data_particao = "2023-04-01" AND CAST(CHAMADO1746.data_inicio AS DATE) = "2023-04-01" GROUP BY BAIRRO.subprefeitura ORDER BY Numero DESC LIMIT 1;

-- 5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?

SELECT tipo, subtipo, categoria, id_bairro FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-04-01" AND CAST(data_inicio AS DATE) = "2023-04-01" AND id_bairro IS NULL;
SELECT tipo, subtipo, categoria FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 INNER JOIN `datario.dados_mestres.bairro` AS BAIRRO ON CHAMADO1746.id_bairro = BAIRRO.id_bairro WHERE CHAMADO1746.data_particao = "2023-04-01" AND CAST(CHAMADO1746.data_inicio AS DATE) = "2023-04-01" AND BAIRRO.subprefeitura = "";

-- 6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?

SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-01-01" AND "2023-12-01") AND subtipo = "Perturbação do sossego";

-- 7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio).

-- Script com as datas colocadas manualmente
SELECT "Carnaval" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Reveillon" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-12-30" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Rock in Rio" AS Evento, id_chamado, tipo, subtipo, id_bairro, situacao, tipo_situacao, status FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego";

-- Script com as datas colocadas automaticamente
SELECT EVENTOS.evento, CHAMADO1746.id_chamado, CHAMADO1746.tipo, CHAMADO1746.subtipo, CHAMADO1746.id_bairro, CHAMADO1746.situacao, CHAMADO1746.tipo_situacao, CHAMADO1746.status FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) WHERE CHAMADO1746.data_particao = "2023-02-01" AND EVENTOS.evento = "Carnaval" AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT EVENTOS.evento, CHAMADO1746.id_chamado, CHAMADO1746.tipo, CHAMADO1746.subtipo, CHAMADO1746.id_bairro, CHAMADO1746.situacao, CHAMADO1746.tipo_situacao, CHAMADO1746.status FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) WHERE (CHAMADO1746.data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND EVENTOS.evento = "Reveillon" AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT EVENTOS.evento, CHAMADO1746.id_chamado, CHAMADO1746.tipo, CHAMADO1746.subtipo, CHAMADO1746.id_bairro, CHAMADO1746.situacao, CHAMADO1746.tipo_situacao, CHAMADO1746.status FROM `datario.administracao_servicos_publicos.chamado_1746` AS CHAMADO1746 INNER JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` AS EVENTOS ON (CAST(CHAMADO1746.data_inicio AS DATE) BETWEEN EVENTOS.data_inicial AND EVENTOS.data_final) WHERE CHAMADO1746.data_particao = "2022-09-01" AND EVENTOS.evento = "Rock in Rio" AND subtipo = "Perturbação do sossego";

-- 8. Quantos chamados desse subtipo foram abertos em cada evento?

-- Script com as datas colocadas manualmente
SELECT "Carnaval" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Reveillon" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Rock in Rio" AS Evento, COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego";

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

-- 9. Qual evento teve a maior média diária de chamados abertos desse subtipo?

-- Solução 1
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

-- Solução 2
DECLARE DiasCarnaval INT64 DEFAULT 0;
DECLARE DiasReveillon INT64 DEFAULT 0;
DECLARE DiasRockRio INT64 DEFAULT 0;

SET DiasCarnaval = (SELECT DATE_DIFF(DATE "2023-02-21", DATE "2023-02-18", DAY) + 1);
SET DiasReveillon = (SELECT DATE_DIFF(DATE "2023-01-01", DATE "2022-12-30", DAY) + 1);
SET DiasRockRio = (SELECT DATE_DIFF(DATE "2022-09-04", DATE "2022-09-02", DAY) + DATE_DIFF(DATE "2022-09-11", DATE "2022-09-08", DAY) + 2);

SELECT Evento, Media FROM (
SELECT "Carnaval" AS Evento, COUNT(*)/DiasCarnaval AS Media FROM `datario.administracao_servicos_publicos.chamado_1746` 
    WHERE data_particao = "2023-02-01" AND (CAST(data_inicio AS DATE) BETWEEN "2023-02-18" AND "2023-02-21") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Reveillon" AS Evento, COUNT(*)/DiasReveillon AS Media FROM `datario.administracao_servicos_publicos.chamado_1746` 
    WHERE (data_particao BETWEEN "2022-12-01" AND "2023-01-01") AND (CAST(data_inicio AS DATE) BETWEEN "2022-12-30" AND "2023-01-01") AND subtipo = "Perturbação do sossego"
UNION ALL
SELECT "Rock in Rio" AS Evento, COUNT(*)/DiasRockRio AS Media FROM `datario.administracao_servicos_publicos.chamado_1746` 
    WHERE data_particao = "2022-09-01" AND ((CAST(data_inicio AS DATE) BETWEEN "2022-09-02" AND "2022-09-04") OR (CAST(data_inicio AS DATE) BETWEEN "2022-09-08" AND "2022-09-11")) AND subtipo = "Perturbação do sossego"
) ORDER BY Media DESC LIMIT 1;

-- 10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023.

SELECT "De 01/01/2022 a 31/12/2023" AS Periodo, AVG(Numero) AS Media FROM (
  SELECT COUNT(*) AS Numero FROM `datario.administracao_servicos_publicos.chamado_1746` WHERE (data_particao BETWEEN "2022-01-01" AND "2023-12-01") AND subtipo = "Perturbação do sossego" GROUP BY CAST(data_inicio AS DATE));
