# Desembarque pesqueiro e ensaios de aquicultura no Brasil

English version: [README.md](README.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23680350.svg)](https://doi.org/10.5281/zenodo.23680350)

1.672 registros tirados das tabelas e do texto de 8 publicações em português impressas entre 2004 e 2013. 1.458 são registros de desembarque e captura de 5 documentos: o boletim SCPESCA/MS 2007 da pesca profissional e esportiva no Pantanal (MS), a pesca artesanal na represa Billings em 2005-2007 (SP), o desembarque no porto de Tefé de janeiro a junho de 2012 (AM), a captura de 3 currais no litoral do Piauí (PI) e o desembarque da pesca artesanal de emalhe em Tijucas (SC). 214 são médias de tratamento de 3 ensaios de aquicultura: tambaqui em 4 densidades de estocagem em tanque-rede (AM), 3 linhagens de tilápia em raceway (AL) e jundiá num ensaio 2 x 2 de densidade de estocagem e frequência alimentar (RS). Cada linha é uma célula impressa ou um número do texto, com a página e a tabela de onde saiu.

Esses números foram impressos como boletins, relatórios técnicos, trabalhos de congresso e artigos de periódico, e nenhum deles existe em forma estruturada. Antes de ser transcrito, cada documento foi conferido no FAO FishStat, nos boletins nacionais de estatística da pesca, no IBGE SIDRA, no dados.gov.br e no DataCite, e nenhum dos 8 tinha os seus dados lá. O FishStat tem o Brasil como um número por espécie e ano; este dataset dá rio, local de desembarque, mês e frota para os lugares e anos acima.

Faz parte do [Paper Rerun](https://paper-rerun.github.io), na linha Open Tables. O trabalho foi feito por agentes de IA num computador doméstico e revisado por uma pessoa antes da publicação.

## O que tem

| | |
|---|---|
| Publicações | 8, impressas de 2004 a 2013: 5 dos repositórios abertos da Embrapa (Alice e Infoteca-e), 1 relatório do Instituto de Pesca (SP), 1 boletim do Instituto Mamirauá (AM) e 1 artigo da Revista Biotemas |
| Estratos | 80 em 5 documentos de desembarque: 5 estudos, 47 áreas de captura (rios, lagos, localidades), 13 postos de vistoria ou locais de desembarque, 7 tipos de embarcação, 2 pescas (profissional e esportiva), 2 fontes de dado (porto de Tefé e o frigorífico Frigopeixe) e 4 classes de qualidade da pesca |
| Registros de desembarque | 1.458: peso capturado 1.106, número de peixes 119, pescadores 65, número de registros 45, captura estimada 41, CPUE 26, desembarques 18, pescado comercializado 14, descarte 9, dias de pesca 8, outros 7. 186 deles são totais impressos |
| Ensaios | 3, no Amazonas, em Alagoas e no Rio Grande do Sul |
| Registros de ensaio | 214 médias de tratamento, 170 com termo de dispersão e 78 com letra de significância |
| Espécies | 64 nomes populares e 126 nomes científicos distintos nos registros de desembarque, como impressos |

| Documento | O que é | UF | Período, como impresso | Estratos ou ensaio | Registros | Conferência de disponibilidade |
|---|---|---|---|---:|---:|---|
| albuquerque2010 | SCPESCA/MS 2007, captura da pesca profissional e esportiva na Bacia do Alto Paraguai, das guias de controle de pescado da Polícia Militar Ambiental; só as páginas 12, 16, 17, 26 e 30 | MS | no ano de 2007, com uma série de 1994 a 2007 | 27 estratos | 441 | o FishStat tem o Brasil só como total nacional; o boletim do Ibama de 2007 dá o total de MS por espécie, em PDF; 0 resultado para SCPESCA no DataCite e no Redape |
| castro2009 | pesca artesanal na represa Billings, de fichas diárias voluntárias | SP | janeiro/2005 a dezembro/2007 | 1 estrato | 490 | o ProPesq do Instituto de Pesca cobre só o monitoramento marinho e estuarino; nada da Billings no DataCite nem no Redape |
| mamiraua2012 | desembarque no porto de Tefé e pescado recebido pelo frigorífico Frigopeixe | AM | janeiro a junho de 2012 | 44 estratos | 181 | o boletim diz que os dados estão no banco de desembarque do instituto (p2); não achamos download nem portal |
| mai2010 | captura de 3 currais, documento escaneado | PI | dezembro de 2008 a novembro de 2009 | 1 estrato | 237 | nada de curral no DataCite nem no Redape; nenhuma ocorrência de *Opisthonema oglinum* no Piauí em 2008-2009 no GBIF |
| martins2013 | desembarque da pesca artesanal de emalhe na Barra do Rio | SC | entre setembro de 2010 e julho de 2011 | 7 estratos | 109 | sem material suplementar; os boletins de SC (UNIVALI/CEPSUL) cobrem a frota industrial |
| brandao2004 | juvenis de tambaqui em 4 densidades em tanque-rede, 60 dias | AM | entre maio e julho de 2003 | 1 ensaio | 72 | média de ensaio não está em sistema nacional nenhum (FishStat e SIDRA têm produção); 0 resultado pela espécie e pelo desenho no DataCite e no Redape |
| cartaxo2010 | 3 linhagens de tilápia em raceway, 160 dias | AL | não impresso | 1 ensaio | 30 | como acima |
| martinelli2013 | jundiá, 2 x 2 de densidade de estocagem e frequência alimentar em tanque-rede, 60 dias | RS | março a maio de 2010 | 1 ensaio | 112 | como acima |

Arquivos:
- `data/landings.csv`: um registro de desembarque ou captura por linha (1.458), com `doc_id`, `page` e `table_or_figure`. Traz o que o registro recebe da coluna e da tabela (variável, unidade, estatística, origem), o cabeçalho da coluna, o período e a unidade impressos para a tabela e o significado da nota de rodapé.
- `data/strata.csv`: um estrato por linha (80). Os estratos se encaixam por `parentStratumID`, do estudo para baixo: local de desembarque, área de captura, tipo de embarcação, pesca e fonte de dado. Um campo que o estrato filho não imprime vem do estrato acima mais próximo que imprime, e `inherited` diz de qual; esforço, coordenada, rótulo e páginas nunca descem.
- `data/aquaculture.csv`: um registro de ensaio por linha (214), com tratamento, espécie, densidade, ração, duração, variável, valor, dispersão e letra.
- `data/trials.csv`: um ensaio por linha (3), com local, período, espécie, fase, unidade de cultivo, ração, água e desenho, como impressos.
- `data/species_key.csv`: os 46 pares de nome popular e nome científico que 4 documentos imprimem como chave de espécies (albuquerque2010 Tabela 1, castro2009 Tabela 5, martins2013 Tabela 1 e um bloco de texto de mai2010). Ficam à parte: nenhum registro tirou nome deles.
- `data/sources.csv`: as 8 publicações, com autores, link do registro e aviso de licença.
- `qa/decisions.csv`: cada divergência entre as duas transcrições independentes e como ela foi resolvida conferindo o PDF (1.258 decisões, com a página).
- `qa/totals_check.csv`: cada total impresso contra a soma das partes transcritas (186 totais). É conferência, não dado; o dataset não muda com ela.
- `method/`: o schema, o script de comparação e o script de junção.

### Colunas

Todos os arquivos se ligam a `data/sources.csv` por `doc_id`. Os desembarques se ligam aos estratos por `doc_id` e `stratum_ids`: `stratum_ids` lista os estratos do registro dentro do documento ("s2; s15"), e `stratumID` é `doc_id#s2`. Um registro pertence a todos os estratos que lista, como uma área de captura e uma pesca. Os registros de ensaio se ligam a `data/trials.csv` por `doc_id` e `trial_id`. Em `qa/totals_check.csv`, `record_id` é o total em `data/landings.csv`, e `part_record_ids` lista os números depois do `#` das partes que foram somadas.

Nomes, períodos e unidades ficam exatamente como impressos. Nome popular e nome científico ficam em campos separados e nunca são casados por nós: só 59 registros trazem os dois, porque a mesma linha (56) ou a mesma célula (3) imprime os dois. Quem quiser casar os outros pode usar `data/species_key.csv`, sabendo de onde veio cada par. Erro de grafia da fonte fica: mai2010 imprime "Anisostremus" (conferido a 400 dpi), e é isso que o dataset tem. Os totais impressos ficam como registros com `is_total` = True e nunca são recalculados; `total_kind` diz se o total é de linha, de coluna, geral ou subtotal.

### Principais colunas

Os arquivos estão em UTF-8, com vírgula separando as colunas. Em todo registro, `doc_id` liga a linha a `data/sources.csv`, e `page` e `table_or_figure` dizem de onde ela saiu (página do PDF contada a partir de 1, e o rótulo da tabela como impresso, "Tabela 4", "TABELA 01", ou `text` para um número do texto). `record_id` é o registro, no formato `doc_id#0001`.

- `stratum_ids` (desembarque) e `trial_id` (ensaio): os estratos ou o ensaio a que o registro pertence.
- `stratumID`, `parentStratumID` e `stratum_dimension`: o estrato, o estrato acima dele e o seu tipo (`study`, `landing_site`, `capture_area`, `vessel_type`, `fleet_or_fishery`, `data_source`, `other`).
- `period_as_printed`: o período do registro como impresso ("1997", "janeiro a junho de 2012"). Todo registro de desembarque tem um; 737 têm também o período mais largo da legenda ou do método em `period_context_as_printed`.
- `species_common_as_printed` e `species_scientific_as_printed`: os nomes exatamente como impressos, cada um no seu campo. `taxon_status` diz se a linha é um táxon (830 registros de desembarque), uma categoria "Outros" (69), um nome incompleto na impressão (3) ou uma linha que não é de espécie, como posto, mês ou total (556).
- `variable_standardized` e `variable_as_printed`: o que foi medido, na nossa lista de termos (`catch_weight`, `cpue`, `final_weight`, `water_quality` e outros em `method/schema.json`) e como a fonte chama.
- `value` e `value_as_printed`: o número pronto para cálculo, com ponto decimal, e a célula como impressa ("1.236", "18,47"). Uma célula vem malformada na impressão ("8.14,8", albuquerque2010 Tabela 2) e tem `value_kind` = `malformed`.
- `unit`: a unidade como impressa ("kg", "quilogramas", "toneladas", "%", "indivíduos").
- `statistic`: `single_value`, `total`, `percentage_share`, `cumulative_percentage`, `mean`, `median` ou `standard_deviation`. Os 214 registros de ensaio são médias.
- `is_total` e `total_kind`: se o registro é um total impresso, e de que tipo.
- `treatment`, `treatment_type` e `is_marginal` (ensaio): o tratamento como impresso, o que ele varia (`stocking_density`, `feeding_frequency`, `strain_or_genotype`, `combination`) e se a média é efeito principal sobre o outro fator (os 96 de martinelli2013).
- `dispersion_as_printed` e `significance_letter` (ensaio): o termo depois do ± e a letra impressa com a média.
- `inherited`: os campos que o registro ou o estrato recebeu da coluna, da tabela ou do estrato acima, e de qual ("unit:column", "period_as_printed:s1").

## Como foi feito

1. **Coleta.** Um agente percorreu os repositórios abertos da Embrapa (Alice e Infoteca-e) pelo OAI-PMH: 2.767 registros com palavra de pesca ou aquicultura, 567 candidatos pelo título, 23 páginas de registro e PDFs lidos. A Embrapa não tem estatística de desembarque do Sul e do Sudeste, então entraram os relatórios técnicos do Instituto de Pesca (SP), os boletins do Instituto Mamirauá e uma revista de acesso aberto. 26 candidatos foram lidos e ficaram de fora, cada um com o motivo: 11 para equilibrar região, série ou desenho, 6 com resultado só em figura ou tabela fina demais, 3 já estruturados no Redape da Embrapa (doi:10.48432/XGCF7T), 3 num acervo que estava fora do ar (CEPSUL), 2 cuja disponibilidade não deu para resolver e 1 sem tratamento.
2. **Conferência de disponibilidade.** Só entrou documento cujos dados não existem em forma estruturada. Cada um passou pelo FAO FishStat, pelos boletins nacionais (Ibama até 2007, MPA 2008-2011), pelo IBGE SIDRA, pelo dados.gov.br, pelo DataCite (que registra os DOIs do Zenodo, do figshare e do Dryad), pelo Redape da Embrapa e, quando existe, pela base do próprio produtor.
3. **Duas transcrições independentes.** Dois agentes por publicação transcreveram os estratos ou o ensaio, um inventário das tabelas e dos blocos de texto com número, a chave de espécies e cada célula de dado num schema fixo, sem ver o trabalho um do outro, copiando nomes, períodos, unidades e números exatamente como impressos.
4. **Comparação e arbitragem.** Um script pareou as duas transcrições estrato por estrato e registro por registro e listou cada divergência e cada item presente em só uma delas. Cada caso foi resolvido conferindo o PDF, com a página como evidência.
5. **Junção e conferência dos totais.** Um script juntou os documentos arbitrados, completou cada registro com a sua coluna e a sua tabela e cada estrato com o estrato acima, e somou as partes de cada total impresso. Registro de desembarque sem estatística impressa recebe `single_value`, o padrão do schema (698 registros). Nada no dataset mudou com a conferência dos totais.

## Qual a precisão

- **Nomes e números:** nenhum número e nenhum nome foi lido errado em nenhuma das duas transcrições. Nos 1.665 registros pareados, nenhum algarismo, separador, termo de dispersão ou letra de significância foi lido diferente do impresso, incluindo marcadores sobrescritos colados no número (a camada de texto da albuquerque2010 Tabela 4 lê "19941" onde a página imprime 1994 com a nota 1), o malformado "8.14,8", a camada de texto embaralhada de mamiraua2012 e o scan de mai2010. Uma transcrição escreveu duas vezes o que não está impresso: a grafia correta *Anisotremus* onde mai2010 imprime "Anisostremus" (4 registros), e quatro espécies citadas como exemplo numa frase de castro2009 juntadas num campo só (2 registros). As duas voltaram para o impresso.
- **Registros inteiros:** sozinha, uma transcrição estava totalmente correta em 98,3% dos registros, e a outra em 97,5%, contando os registros que cada uma deixou de fora (7 e 0). Os 7 são uma linha de cabeçalho da martins2013 Tabela 1 que imprime o número de desembarques de cada coluna, "(17) (20) (23) (13) (14) (22) (109)". Só desembarque: 98,4% e 97,2%; só ensaio: 98,1% e 100%. castro2009 tem 29% dos registros; sem ele, as duas ficam em 97,6% e 97,0%.
- **Estratos e ensaios:** foi nos estratos que as duas mais divergiram. Uma transcrição acertou os 80; a outra, 33 (41,2%). 43 dos seus 47 estratos errados estão em mamiraua2012, por regras perdidas no documento inteiro: a página do rótulo de cada estrato, impresso no stub da tabela, deixada de fora (43 estratos), o rio de cada área de captura deixado vazio embora o rótulo o imprima, "Capivara (Paraná)" (33), e 16 áreas de captura que são registro do Frigopeixe marcadas como monitoramento do porto. Nos ensaios, uma transcrição errou um campo em cada um dos 3, a outra errou 3 campos em 2 deles. As 1.258 divergências foram resolvidas conferindo o PDF, então o dataset não depende de nenhuma das duas transcrições sozinha.
- **Totais impressos:** dos 186 totais, 167 fecham exatamente com as partes transcritas, 10 fecham no arredondamento, 7 não fecham e 2 não têm como ser conferidos. As duas transcrições concordam em toda célula envolvida nos 7, e a camada de texto também: são erros da fonte, 5 ao todo. Não use os totais de linha do acará em castro2009 nem o total da mamiraua2012 TABELA 01 como estão. Cada caso está em `qa/totals_check.csv`, em `status` e `note`.
  - albuquerque2010 Tabela 4, 1994: 301 t da pesca profissional e 829 t da esportiva dão 1.130 t; o total imprime 1.152.
  - castro2009 Tabela 2, acará: os 12 meses somam 13.378,0 kg; o total da linha imprime 13.375,0.
  - castro2009 Tabela 2, total geral: 31.498,5 bate com a soma das colunas (31.498,54), não com a dos totais de linha (31.495,54). O texto (p3 e p7) dá 31.495 kg para 2005.
  - castro2009 Tabela 3, acará: os meses somam 15.810,5 kg; o total da linha imprime 15.940,5, 130 kg a mais.
  - castro2009 Tabela 3, total geral: 38.391,3 bate com as colunas, não com os totais de linha (38.521,3), por causa da linha do acará acima.
  - mamiraua2012 TABELA 01: o total de 534.393 kg soma os 499.763 kg das espécies com as 34.630 *unidades* de acari-bodó, que a tabela marca como contadas por unidade.
  - mamiraua2012 TABELA 03: a coluna de porcentagem soma 84,87, não 100. A linha "OUTRAS" (81.382 kg) imprime 0,15%, e 81.382 / 534.393 dá 15,2%.
  - Sem como conferir: albuquerque2010 Tabela 2, coluna "Pescado comercializado", que tem a parcela malformada "8.14,8"; e o total de texto de castro2009, 120.009 kg, que não imprime as parcelas ao lado. Ele fecha por outro caminho: 31.499 + 38.391 + 50.119, os três totais anuais da Tabela 1, dão 120.009.
- **Limites conhecidos:**
  - albuquerque2010 é um recorte: 5 das suas 50 páginas (12, 16, 17, 26 e 30), com a chave de espécies, a captura por posto e por pesca, a série 1994-2007, a captura mensal por espécie e os pescadores por rio. O boletim tem 24 tabelas, umas 2.000 células.
  - mai2010 é um scan com camada de OCR, e mamiraua2012 tem um leiaute que embaralha a camada de texto; os dois foram lidos pela página renderizada. A lista dos currais de mai2010 imprime só o nome científico: os seus 237 registros não têm nome popular, e 9 nomes populares estão só num bloco de texto, guardados em `data/species_key.csv`.
  - As unidades estão como impressas: "kg", "quilogramas" e "Quilogramas" são a mesma unidade em 843 registros, e "toneladas" e "g" também aparecem. Ainda não há coluna de unidade padronizada, e nenhum valor foi convertido.
  - Os períodos estão como impressos, sem data ISO. Só 1 estrato imprime coordenada.
  - Os 96 registros de martinelli2013 são efeitos principais, como o artigo imprime, e não as médias das 4 células do 2 x 2.
  - A conferência de disponibilidade tem buracos: a API do dados.gov.br respondeu 401, a do Zenodo respondeu 403 (o Zenodo foi buscado só pelo DataCite) e o SciELO Data pediu desafio de robô. Nenhum dos três foi tentado de novo.
  - Falta o Sudeste costeiro. O candidato mais forte (Cananéia e Iguape, 1967-1994) não pôde ser conferido no ProPesq do Instituto de Pesca, que pede e-mail e perfil antes de mostrar qualquer coisa.
  - Um documento, castro2009, tem 490 registros, 29% do dataset.

Este é um piloto de 8 documentos, feito para acertar o schema. Uma rodada maior, de 20 documentos, está planejada.

## Licença e citação

- O dataset (os arquivos CSV, o schema e os scripts) é publicado sob a licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Por favor, cite as publicações originais listadas em `data/sources.csv` e também este dataset. Cada linha também traz a sua fonte em `citation` e a situação de licença da fonte em `license`.
- As publicações não são redistribuídas. martins2013 é a única com licença aberta: CC BY 4.0, na página do artigo na Revista Biotemas. Os repositórios da Embrapa exibem um aviso CC BY-NC-ND 4.0 na página de todo registro, e não uma licença do item, e albuquerque2010 traz "Todos os direitos reservados". O Instituto de Pesca não imprime licença nem termo de uso para castro2009, e o PDF dele é protegido por senha; ele é tratado como todos os direitos reservados. O rodapé do site do Instituto Mamirauá diz "Todos os direitos reservados". Os termos da revista e dos anais de brandao2004, martinelli2013 (Pesquisa Agropecuária Brasileira), cartaxo2010 (SBZ) e mai2010 (Congresso Brasileiro de Oceanografia) não foram conferidos. Aqui são usados só os números de desembarque e de ensaio, que são fatos, e citações curtas.

Erros ou registros que faltam: por favor, [abra uma issue](https://github.com/paper-rerun/fisheries-aquaculture-br/issues).

## Como este dataset foi feito

Este dataset foi montado por agentes de IA (Claude, da Anthropic) num computador doméstico e revisado por uma pessoa antes da publicação. Nenhum valor foi estimado ou digitado à mão: cada um foi transcrito do PDF original duas vezes, de forma independente, e cada divergência foi conferida na página. O método e os scripts estão em `method/`. Como funciona o projeto como um todo (em inglês): https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contato: Filipe Tessaro, pelas issues deste repositório.
