# Desembarque pesqueiro e ensaios de aquicultura no Brasil

English version: [README.md](README.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23680350.svg)](https://doi.org/10.5281/zenodo.23680350)

6.567 registros tirados das tabelas e do texto de 28 publicações impressas em português entre 2000 e 2020. 5.546 são registros de desembarque e captura de 17 documentos, do Pantanal, da Amazônia, do Araguaia, dos reservatórios de São Paulo e do Paraná, da Lagoa dos Patos e do litoral do Pará a Santa Catarina. 1.021 são médias de tratamento e outros resultados de 14 ensaios de aquicultura com tambaqui, matrinxã, tambatinga, tilápia, jundiá, cachara, pacu e carpa. Cada linha é uma célula impressa ou um número do texto, com a página e a tabela de onde saiu.

Esses números foram impressos em boletins, relatórios técnicos, anais, artigos de periódico e folhetos da Embrapa, e nenhum deles existe em forma estruturada. Antes da transcrição, cada documento foi conferido no FAO FishStat, nos boletins nacionais de pesca, no SIDRA do IBGE, no dados.gov.br, no DataCite e, quando existe, na base do próprio produtor do dado. O FishStat traz o Brasil como um número por espécie e ano; este dataset dá rio, local de desembarque, mês, aparelho e frota nos lugares e anos que cobre.

Faz parte do [Paper Rerun](https://paper-rerun.github.io), na linha Open Tables. O trabalho foi feito por agentes de IA num computador doméstico e revisado por uma pessoa antes da publicação.

## Versões

- **v2.0.0** (novembro de 2026): 28 documentos. Junta uma rodada de 20 documentos aos 8 do piloto, todos fundidos com o schema 2.0. O schema novo aplica a estatística padrão antes de comparar, guarda faixa ("variou de 1 a 17") em `value_min` e `value_max`, cria a coluna `unit_standardized` (só a grafia, nenhum valor convertido) e pareia número de texto pelo número citado.
- **v1.0.0** (outubro de 2026): piloto de 8 publicações, 1.672 registros.

## O que tem

| | |
|---|---|
| Publicações | 28, de 2000 a 2020: 15 dos repositórios abertos da Embrapa (Alice e Infoteca-e), 6 relatórios técnicos ou artigos do Instituto de Pesca (SP), 1 boletim do Instituto Mamirauá (AM) e 6 artigos de outras revistas ou relatórios |
| Estratos | 178 em 17 documentos de desembarque: estudos, áreas de captura, aparelhos, locais de desembarque, áreas administrativas, tipos de embarcação, pescarias e fontes de dado |
| Registros de desembarque | 5.546, entre eles peso capturado 2.456, número de desembarques 345, número de peixes 263, peso comprado 243, pescadores 166, barcos 114 e valor da captura 81. 558 são totais impressos |
| Ensaios | 14, em AL, AM, AP, MS, PE, RS e SP |
| Registros de ensaio | 1.021, 487 com termo de dispersão e 444 com letra de significância |
| Estados | 19: AL, AM, AP, BA, CE, MA, MS, PA, PB, PE, PI, PR, RN, RO, RS, SC, SE, SP e TO |

| Documento | O que é | UF | Estratos ou ensaios | Registros |
|---|---|---|---:|---:|
| albuquerque2010 | SCPESCA/MS 2007, pesca profissional e esportiva na bacia do Alto Paraguai (5 páginas) | MS | 27 estratos | 441 |
| castro2009 | pesca artesanal na represa Billings, 2005-2007 | SP | 1 estrato | 490 |
| mamiraua2012 | desembarque no porto de Tefé, janeiro a junho de 2012 | AM | 44 estratos | 181 |
| mai2010 | captura de 3 currais de pesca no litoral | PI | 1 estrato | 237 |
| martins2013 | desembarque artesanal de rede de emalhe em Tijucas | SC | 7 estratos | 109 |
| moraes2001 | pesca de iscas vivas em Corumbá, 1996 | MS | 7 estratos | 443 |
| silva2017 | captura artesanal no Araguaia, 2013-2014 | TO | 12 estratos | 67 |
| tavaresdias2020 | peixes ornamentais capturados no Amapá e autorizados para exportação, 2014-2016 | AP | 1 estrato | 111 |
| miranda2007 | desembarque de tainha em São Paulo, por cerco e outros aparelhos | SP | 16 estratos | 268 |
| maruyama2010 | pesca profissional nos reservatórios do médio Tietê, 2003-2004 | SP | 4 estratos | 231 |
| santos2016 | pesca da miragaia no estuário da Lagoa dos Patos | RS | 12 estratos | 240 |
| okada2012 | composição do desembarque no reservatório de Itaipu, 2010 | PR | 4 estratos | 463 |
| espiritosanto2012 | desembarque de pequena escala em 7 portos de Bragança, 2000-2001 | PA | 17 estratos | 864 |
| almeida2011 | desembarque de pescada-amarela por rede de emalhe na Raposa, 2007 | MA | 1 estrato | 121 |
| nobrega2007 | 2.998 desembarques de 975 barcos artesanais, 1998-2000 (REVIZEE) | BA a PI | 22 estratos | 950 |
| novaes2015 | pesca artesanal no reservatório Santa Cruz, 2012 | RN | 1 estrato | 79 |
| santanna2020 | peixe desembarcado no mercado Cai n'Água, 2006-2019 | RO | 1 estrato | 251 |
| brandao2004 | tambaqui em 4 densidades em tanques-rede | AM | 1 ensaio | 72 |
| cartaxo2010 | 3 linhagens de tilápia em raceways | AL | 1 ensaio | 30 |
| martinelli2013 | jundiá, 2 x 2 de densidade e frequência alimentar | RS | 1 ensaio | 112 |
| brandao2005 | matrinxã em várias densidades em tanques-rede | AM | 1 ensaio | 78 |
| yoshioka2015 | tambatinga com ração parcialmente trocada por soja e milho | AP | 1 ensaio | 93 |
| lima2016 | larvas de tilápia, densidade e vitamina C na reversão sexual | PE | 1 ensaio | 52 |
| nascimento2013 | cachara em tanques-rede | MS | 1 ensaio | 130 |
| hisano2011 | tilápia com folha de mandioca no lugar do farelo de soja | MS | 1 ensaio | 25 |
| bergamin2011 | carpa-húngara com fontes de proteína vegetal | RS | 1 ensaio | 130 |
| rodrigues2010 | pacu com níveis crescentes de fibra bruta | SP | 1 ensaio | 72 |
| romagosa2000 | dois lotes de tilápia em viveiro num programa comercial de alimentação | SP | 4 ensaios | 227 |

Onde cada documento foi conferido, e o que se achou, está em `availability_check` de `data/sources.csv`.

Arquivos:
- `data/landings.csv`: um registro de desembarque ou captura por linha (5.546), com `doc_id`, `page` e `table_or_figure`. Traz o que o registro recebe da coluna e da tabela (variável, unidade, estatística, origem), o cabeçalho da coluna, o período e a unidade impressos para a tabela e o significado da nota de rodapé.
- `data/strata.csv`: um estrato por linha (178). Os estratos se encaixam por `parentStratumID`. Um campo que o estrato filho não imprime vem do estrato acima mais próximo que imprime, e `inherited` diz de qual; esforço, coordenada, rótulo e páginas nunca descem.
- `data/aquaculture.csv`: um registro de ensaio por linha (1.021), com tratamento, espécie, densidade, ração, duração, variável, valor, dispersão e letra.
- `data/trials.csv`: um ensaio por linha (14), com local, período, espécie, fase de vida, unidade de cultivo, ração, água e delineamento, como impressos.
- `data/species_key.csv`: os 293 pares de nome popular e científico que os documentos imprimem como chave de espécies. Ficam à parte: nenhum registro tirou nome deles.
- `data/sources.csv`: as 28 publicações, com autores, link do registro, aviso de licença e a conferência de disponibilidade.
- `qa/decisions.csv`: cada divergência entre as duas transcrições independentes e como ela foi resolvida conferindo o PDF (6.298 decisões, com a página).
- `qa/totals_check.csv`: cada total impresso contra a soma das partes transcritas (558 totais). É conferência, não dado; o dataset não muda com ela.
- `method/`: o schema (`schema.json`, gerado por `build_schema.py`), o autoteste dele, os scripts de comparação e de junção e a conferência de disponibilidade.

### Colunas

Todos os arquivos se ligam a `data/sources.csv` por `doc_id`. Desembarques se ligam aos estratos por `doc_id` e `stratum_ids`: `stratum_ids` lista os estratos do registro dentro do documento ("s2; s15"), e `stratumID` é `doc_id#s2`. Um registro pertence a todos os estratos que lista, como uma área de captura e uma pescaria. Registros de ensaio se ligam a `data/trials.csv` por `doc_id` e `trial_id`.

Nomes, períodos e unidades ficam exatamente como impressos. Nome popular e científico ficam em campos separados e nunca são casados por nós; `data/species_key.csv` guarda os pares que os documentos imprimem. Erro de grafia da fonte fica. Total impresso é guardado como registro com `is_total` = True e nunca é recalculado; `total_kind` diz se é total de linha, de coluna, total geral ou subtotal.

As principais colunas:
- `record_id`: o registro, no formato `doc_id#0001`. `page` é a página do PDF contada a partir de 1; `table_or_figure` é o rótulo da tabela como impresso, ou `text` para número no texto.
- `period_as_printed`: o período do registro como impresso ("1997", "janeiro a junho de 2012"); `period_context_as_printed` guarda o período mais largo da legenda ou do método, e `period_source_page` a página de um período tirado do texto.
- `species_common_as_printed` e `species_scientific_as_printed`: os nomes exatamente como impressos, cada um no seu campo. `taxon_status` diz se a linha é um táxon, uma categoria "Outros", um nome incompleto na impressão ou nem é linha de espécie.
- `variable_standardized` e `variable_as_printed`: o que foi medido, na nossa lista de termos (`catch_weight`, `cpue`, `final_weight`, `water_quality` e outros em `method/schema.json`) e como a fonte chama.
- `value`, `value_min`, `value_max` e `value_as_printed`: o número pronto para cálculo, com ponto decimal; as duas pontas de uma faixa impressa (`value_kind` = `range`, 109 registros, com `value` vazio); e a célula como impressa.
- `unit` e `unit_standardized`: a unidade como impressa ("kg", "quilogramas", "toneladas") e a mesma unidade numa grafia só ("kg", "t", "g", "individuals"). Nenhum valor é convertido; unidade fora da nossa lista deixa `unit_standardized` vazio.
- `statistic`: `single_value`, `total`, `percentage_share`, `mean`, `median`, `standard_deviation` e outros. Registro de desembarque sem estatística impressa recebe `single_value`, o padrão do schema.
- `treatment`, `treatment_type` e `is_marginal` (registros de ensaio): o tratamento como impresso, o que ele varia e se a média é efeito principal sobre outro fator.
- `dispersion_as_printed` e `significance_letter` (registros de ensaio): o termo depois do ± e a letra impressa com a média.
- `inherited`: os campos que o registro ou o estrato recebeu da coluna, da tabela ou do estrato acima, e de qual.

## Como foi feito

1. **Coleta.** Os agentes percorreram os repositórios abertos da Embrapa pelo OAI-PMH e buscaram nos relatórios e revistas do Instituto de Pesca (SP), do Instituto Mamirauá e de outras revistas de acesso aberto, leram a página do registro e o PDF e registraram cada candidato que ficou de fora, com o motivo.
2. **Conferência de disponibilidade.** Só entrou documento cujos dados não existem em forma estruturada. Cada um passou pelo FAO FishStat, pelos boletins nacionais (Ibama até 2007, MPA de 2008 a 2011), pelo SIDRA do IBGE, pelo dados.gov.br, pelo DataCite (que registra os DOIs do Zenodo, do figshare e do Dryad), pelo Redape da Embrapa e, quando existe, pela base do próprio produtor.
3. **Duas transcrições independentes.** Dois agentes por publicação transcreveram os estratos ou o ensaio, um inventário das tabelas e blocos de texto com número, a chave de espécies e cada célula de dado num schema fixo, sem ver o trabalho um do outro, copiando nomes, períodos, unidades e números exatamente como impressos.
4. **Comparação e arbitragem.** Um script pareou as duas transcrições estrato por estrato e registro por registro e listou cada divergência e cada item presente em só uma delas. Cada caso foi resolvido conferindo o PDF, com a página como evidência. Na rodada, cada documento ainda passou por uma conferência à parte do local, do período, do aparelho, da frota, da unidade, da estatística e do método de cada tabela, para pegar o erro de contexto que as duas transcrições cometem juntas.
5. **Junção e conferência de totais.** Um script juntou os documentos arbitrados, completou cada registro com a coluna e a tabela e cada estrato com o estrato acima, e somou as partes de cada total impresso. Nada no dataset mudou com a conferência de totais.

## Qual a precisão

- **Nomes e números:** nos 6.541 registros pareados das duas rodadas, nenhum algarismo e nenhuma letra de nome foi lido errado em nenhuma das duas transcrições, incluindo nota sobrescrita colada no número, número malformado, camada de texto embaralhada e documento escaneado.
- **Registros inteiros:** contando os registros que cada uma deixou de fora, uma transcrição sozinha acertou por inteiro 91,7% dos registros da rodada, e a outra 82,8% (98,3% e 97,5% no piloto). Quase todo erro vem de uma regra perdida num documento inteiro: em santanna2020 uma transcrição inventou um estrato de fonte de dado e errou 250 de 251 registros; em miranda2007 a outra deu a unidade de contagem como não impressa em 141 de 268 registros. As 6.298 divergências foram resolvidas conferindo o PDF, então o dataset não depende de nenhuma das duas transcrições sozinha.
- **Erros de contexto:** na rodada, em 7 casos as duas transcrições concordaram no lugar, no período, na variável ou na unidade errada de um bloco de registros (por exemplo, 144 registros de nobrega2007 deixados no estrato do estudo, com seis estados, quando as tabelas deles imprimem cinco). A conferência de contexto pegou os 7, e todos foram corrigidos. Nenhum mexia em número.
- **Totais impressos:** 14 totais das fontes não batem com a soma das partes, com as duas transcrições concordando em toda célula envolvida: 5 no piloto (albuquerque2010, castro2009 e mamiraua2012) e 9 na rodada (espiritosanto2012 Tabela 6, silva2017 Tabela 1, tavaresdias2020 Tabela 1, as três fases de santanna2020 Tabela 1 e romagosa2000 Planilha 4). São erros da fonte; cada um está descrito em `qa/totals_check.csv` ou nas `notes` do total. Na rodada, outros 21 totais aparecem como não fechando só por causa do próprio conferidor (tabela que continua em outra página, dois blocos na mesma linha, linha de porcentagem somada como parte); o dado está certo.
- **Limites conhecidos:**
  - albuquerque2010 é um recorte: 5 das 50 páginas.
  - Os períodos ficam como impressos, sem data ISO, e quase nenhum estrato imprime coordenada.
  - A conferência de disponibilidade tem lacunas: o ProPesq do Instituto de Pesca pede e-mail e cadastro antes de mostrar qualquer coisa, o que deixa miranda2007 e a série do litoral de São Paulo sem conferência completa; no piloto, as APIs do dados.gov.br e do Zenodo recusaram as consultas.
  - Os 96 registros de martinelli2013 são efeitos principais, como o artigo imprime, e não as médias das 4 células do 2 x 2.

## Licença e citação

- O dataset (os arquivos CSV, o schema e os scripts) é publicado sob a licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Por favor, cite as publicações originais listadas em `data/sources.csv` e também este dataset. Cada linha também traz a sua fonte em `citation` e a situação de licença da fonte em `license`.
- As publicações não são redistribuídas. Só martins2013, espiritosanto2012 e almeida2011 têm licença aberta (CC BY 4.0, da revista). Os repositórios da Embrapa exibem um aviso CC BY-NC-ND 4.0 na página de todo registro, e não uma licença do item, e vários PDFs da Embrapa trazem "Todos os direitos reservados". O Instituto de Pesca, o Instituto Mamirauá e as outras fontes não imprimem licença aberta e são tratados como todos os direitos reservados. Aqui são usados só os números de desembarque e de ensaio, que são fatos, e citações curtas.

Erros ou registros que faltam: por favor, [abra uma issue](https://github.com/paper-rerun/fisheries-aquaculture-br/issues).

## Como este dataset foi feito

Este dataset foi montado por agentes de IA (Claude, da Anthropic) num computador doméstico e revisado por uma pessoa antes da publicação. Nenhum valor foi estimado ou digitado à mão: cada um foi transcrito do PDF original duas vezes, de forma independente, e cada divergência foi conferida na página. O método e os scripts estão em `method/`. Como funciona o projeto como um todo (em inglês): https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contato: Filipe Tessaro, pelas issues deste repositório.
