# Fish landings and aquaculture trials in Brazil

Versão em português: [README.pt-BR.md](README.pt-BR.md)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23680350.svg)](https://doi.org/10.5281/zenodo.23680350)

6,567 records taken from the tables and text of 28 publications printed in Portuguese between 2000 and 2020. 5,546 are landing and catch records from 17 documents, from the Pantanal, the Amazon, the Araguaia, the São Paulo and Paraná reservoirs, the Lagoa dos Patos and the coast from Pará to Santa Catarina. 1,021 are treatment means and other results of 14 aquaculture trials with tambaqui, matrinxã, tambatinga, tilapia, jundiá, cachara, pacu and carp. Each row is one printed cell or one number of the text, with the page and table it came from.

These numbers were printed as bulletins, technical reports, conference papers, journal articles and Embrapa leaflets, and none of them exists in structured form. Each document was checked before it was transcribed against FAO FishStat, the national fisheries bulletins, IBGE SIDRA, dados.gov.br, DataCite and, when there is one, the producer's own database. FishStat has Brazil as one number per species and year; this dataset gives river, landing site, month, gear and fleet for the places and years it covers.

Part of [Paper Rerun](https://paper-rerun.github.io), in its Open Tables line. The work was done by AI agents on a home computer and reviewed by a human before publication.

## Versions

- **v2.0.0** (November 2026): 28 documents. Adds a round of 20 documents to the 8 of the pilot, all merged with schema 2.0. The new schema applies the default statistic before comparing, keeps ranges ("variou de 1 a 17") with `value_min` and `value_max`, adds a `unit_standardized` column (spelling only, no value converted) and pairs text numbers by the number cited.
- **v1.0.0** (October 2026): pilot of 8 publications, 1,672 records.

## What is in it

| | |
|---|---|
| Publications | 28, printed 2000 to 2020: 15 from Embrapa's open repositories (Alice and Infoteca-e), 6 technical reports or journal articles of the Instituto de Pesca (SP), 1 bulletin of the Instituto Mamirauá (AM) and 6 articles in other journals or reports |
| Strata | 178 in 17 landing documents: studies, capture areas, gears, landing sites, administrative areas, vessel types, fisheries and data sources |
| Landing records | 5,546, among them catch weight 2,456, number of landings 345, number of fish 263, purchased weight 243, fishers 166, boats 114 and catch value 81. 558 are printed totals |
| Trials | 14, in AL, AM, AP, MS, PE, RS and SP |
| Trial records | 1,021, 487 with a dispersion term and 444 with a significance letter |
| States | 19: AL, AM, AP, BA, CE, MA, MS, PA, PB, PE, PI, PR, RN, RO, RS, SC, SE, SP and TO |

| Document | What it is | State | Strata or trials | Records |
|---|---|---|---:|---:|
| albuquerque2010 | SCPESCA/MS 2007, professional and sport fishing in the Upper Paraguay basin (5 pages) | MS | 27 strata | 441 |
| castro2009 | artisanal fishing in the Billings reservoir, 2005-2007 | SP | 1 stratum | 490 |
| mamiraua2012 | landings at the port of Tefé, January to June 2012 | AM | 44 strata | 181 |
| mai2010 | catch of 3 coastal fish weirs | PI | 1 stratum | 237 |
| martins2013 | artisanal gillnet landings at Tijucas | SC | 7 strata | 109 |
| moraes2001 | live-bait fishery of Corumbá, 1996 | MS | 7 strata | 443 |
| silva2017 | artisanal catch on the Araguaia, 2013-2014 | TO | 12 strata | 67 |
| tavaresdias2020 | ornamental fish caught in Amapá and authorised for export, 2014-2016 | AP | 1 stratum | 111 |
| miranda2007 | mullet landings in São Paulo by purse-seiners and other gears | SP | 16 strata | 268 |
| maruyama2010 | professional fishing in the middle Tietê reservoirs, 2003-2004 | SP | 4 strata | 231 |
| santos2016 | black drum fishery in the Lagoa dos Patos estuary | RS | 12 strata | 240 |
| okada2012 | species composition of the Itaipu reservoir landings, 2010 | PR | 4 strata | 463 |
| espiritosanto2012 | small-scale landings at 7 ports of Bragança, 2000-2001 | PA | 17 strata | 864 |
| almeida2011 | acoupa weakfish gillnet landings at Raposa, 2007 | MA | 1 stratum | 121 |
| nobrega2007 | 2,998 landings of 975 artisanal boats, 1998-2000 (REVIZEE) | BA to PI | 22 strata | 950 |
| novaes2015 | artisanal fishing in the Santa Cruz reservoir, 2012 | RN | 1 stratum | 79 |
| santanna2020 | fish landed at the Cai n'Água market, 2006-2019 | RO | 1 stratum | 251 |
| brandao2004 | tambaqui at 4 stocking densities in net cages | AM | 1 trial | 72 |
| cartaxo2010 | 3 tilapia strains in raceways | AL | 1 trial | 30 |
| martinelli2013 | jundiá, 2 x 2 of stocking density and feeding frequency | RS | 1 trial | 112 |
| brandao2005 | matrinxã at several stocking densities in net cages | AM | 1 trial | 78 |
| yoshioka2015 | tambatinga fed feed partly replaced by soybean and maize | AP | 1 trial | 93 |
| lima2016 | tilapia larvae, density and vitamin C during sex reversal | PE | 1 trial | 52 |
| nascimento2013 | cachara in net cages | MS | 1 trial | 130 |
| hisano2011 | tilapia fed cassava foliage in place of soybean meal | MS | 1 trial | 25 |
| bergamin2011 | Hungarian carp fed vegetable protein sources | RS | 1 trial | 130 |
| rodrigues2010 | pacu fed increasing crude fibre levels | SP | 1 trial | 72 |
| romagosa2000 | two batches of tilapia in ponds on a commercial feeding programme | SP | 4 trials | 227 |

What each document was checked against, and what was found, is in `availability_check` of `data/sources.csv`.

Files:
- `data/landings.csv`: one landing or catch record per row (5,546), with `doc_id`, `page` and `table_or_figure`. It carries what the record takes from its column and table (variable, unit, statistic, origin), the column header, the period and unit printed for the table, and the meaning of the footnote.
- `data/strata.csv`: one stratum per row (178). Strata nest through `parentStratumID`. A field the child stratum does not print is taken from the nearest parent that does, and `inherited` says from which; effort, coordinates, label and pages are never passed down.
- `data/aquaculture.csv`: one trial record per row (1,021), with treatment, species, density, feed, duration, variable, value, dispersion and letter.
- `data/trials.csv`: one trial per row (14), with place, period, species, life stage, rearing unit, feed, water and design, as printed.
- `data/species_key.csv`: the 293 pairs of common and scientific names that documents print as a species key. They are kept apart: no record took a name from them.
- `data/sources.csv`: the 28 publications, with authors, record link and licence notice.
- `qa/decisions.csv`: every disagreement between the two independent transcriptions and how it was settled against the PDF (6,298 decisions, with page).
- `qa/totals_check.csv`: each printed total against the sum of its transcribed parts (558 totals). It is a check, not data; the dataset does not change with it.
- `method/`: the schema (`schema.json`, built by `build_schema.py`), its self-check, the comparison and merge scripts and the availability check.

### Columns

All files join `data/sources.csv` on `doc_id`. Landings join strata on `doc_id` and `stratum_ids`: `stratum_ids` lists the strata of the record within its document ("s2; s15"), and `stratumID` is `doc_id#s2`. A record belongs to all the strata it lists, such as a capture area and a fishery. Trial records join `data/trials.csv` on `doc_id` and `trial_id`.

Names, periods and units are kept exactly as printed. Common and scientific names are in separate fields and are never paired by us; `data/species_key.csv` holds the pairs the documents print. A misspelling of the source stays. Printed totals are kept as records with `is_total` = True and are never recomputed; `total_kind` says if a total is a row, column, grand total or subtotal.

The main columns:
- `record_id`: the record, as `doc_id#0001`. `page` is the PDF page counted from 1; `table_or_figure` is the table label as printed, or `text` for a number in the text.
- `period_as_printed`: the period of the record as printed ("1997", "janeiro a junho de 2012"); `period_context_as_printed` holds the wider period of the caption or methods, and `period_source_page` the page of a period taken from the text.
- `species_common_as_printed` and `species_scientific_as_printed`: the names exactly as printed, each in its own field. `taxon_status` says if the row is a taxon, an "Outros" category, a name incomplete in print or not a species row at all.
- `variable_standardized` and `variable_as_printed`: what was measured, in our list of terms (`catch_weight`, `cpue`, `final_weight`, `water_quality` and others in `method/schema.json`) and as the source names it.
- `value`, `value_min`, `value_max` and `value_as_printed`: the number ready for calculation, with a decimal point; the two ends of a printed range (`value_kind` = `range`, 109 records, `value` empty); and the cell as printed.
- `unit` and `unit_standardized`: the unit as printed ("kg", "quilogramas", "toneladas") and the same unit in one spelling ("kg", "t", "g", "individuals"). No value is converted; a unit outside our list leaves `unit_standardized` empty.
- `statistic`: `single_value`, `total`, `percentage_share`, `mean`, `median`, `standard_deviation` and others. A landing record with no statistic printed takes `single_value`, the default of the schema.
- `treatment`, `treatment_type` and `is_marginal` (trial records): the treatment as printed, what it varies and whether the mean is a main effect over another factor.
- `dispersion_as_printed` and `significance_letter` (trial records): the term after ± and the letter printed with the mean.
- `inherited`: the fields the record or stratum took from its column, table or parent stratum, and from which.

## How it was made

1. **Collection.** Agents harvested Embrapa's open repositories through OAI-PMH and searched the reports and journals of the Instituto de Pesca (SP), the Instituto Mamirauá and other open-access journals, read the record pages and PDFs and recorded each candidate left out, with the reason.
2. **Availability check.** Only documents whose data do not exist in structured form were taken. Each one went through FAO FishStat, the national bulletins (Ibama to 2007, MPA 2008-2011), IBGE SIDRA, dados.gov.br, DataCite (which registers Zenodo, figshare and Dryad DOIs), Embrapa's Redape and, when there is one, the producer's own database.
3. **Two independent transcriptions.** Two agents per publication transcribed the strata or the trial, an inventory of the tables and text blocks with numbers, the species key and every data cell into a fixed schema, without seeing each other's work, copying names, periods, units and numbers exactly as printed.
4. **Comparison and adjudication.** A script paired the two transcriptions stratum by stratum and record by record and listed every disagreement and every entry present in only one of them. Each one was settled by checking the PDF, with the page as evidence. In the round, each document also got a separate pass that checked place, period, gear, fleet, unit, statistic and method of each table on its own, to catch context errors that both transcriptions make together.
5. **Merge and totals check.** A script merged the adjudicated documents, filled each record from its column and table and each stratum from its parent, and summed the parts of each printed total. Nothing in the dataset was changed by the totals check.

## How accurate it is

- **Names and numbers:** in the 6,541 paired records of both rounds, no digit and no letter of a name was misread in either transcription, including superscript markers glued to numbers, malformed numbers, scrambled text layers and scans.
- **Whole records:** counting the records each one left out, one transcription alone was fully correct on 91.7% of the round's records and the other on 82.8% (98.3% and 97.5% in the pilot). Almost all errors come from one rule missed across a whole document: in santanna2020 one transcription made up a data-source stratum and got 250 of 251 records wrong; in miranda2007 the other left the counting unit as not printed in 141 of 268 records. All 6,298 disagreements were settled against the PDF, so the dataset does not depend on either transcription alone.
- **Context errors:** in the round, 7 cases had both transcriptions agree on the wrong place, period, variable or unit for a block of records (for example 144 records of nobrega2007 left in the study stratum, with six states, when their tables print five). The context pass caught them and they were fixed. None of them touched a number.
- **Printed totals:** 14 totals of the sources do not add up to their parts, with both transcriptions agreeing on every cell involved: 5 in the pilot (albuquerque2010, castro2009 and mamiraua2012) and 9 in the round (espiritosanto2012 Tabela 6, silva2017 Tabela 1, tavaresdias2020 Tabela 1, the three phases of santanna2020 Tabela 1 and romagosa2000 Planilha 4). They are errors of the source; each one is described in `qa/totals_check.csv` or in `notes` of the total. In the round, 21 more totals show as not adding up only because of the checker itself (tables that run over two pages, two blocks on one line, a percentage row summed as a part); the data are right.
- **Known limits:**
  - albuquerque2010 is a cut: 5 of its 50 pages.
  - Periods are as printed, with no ISO dates, and almost no stratum prints coordinates.
  - The availability check has gaps: the Instituto de Pesca's ProPesq asks for an email and a profile before showing anything, which leaves miranda2007 and the coastal São Paulo series not fully checked; in the pilot the dados.gov.br and Zenodo APIs refused the queries.
  - The 96 records of martinelli2013 are main effects, as the article prints them, not the means of the 4 cells of the 2 x 2.

## Licence and citation

- The dataset (the CSV files, schema and scripts) is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the original publications listed in `data/sources.csv` as well as this dataset. Each row also carries its source in `citation` and the licence situation of its source in `license` (in Portuguese).
- The publications are not redistributed. Only martins2013, espiritosanto2012 and almeida2011 carry an open licence (CC BY 4.0, from the journal). Embrapa's repositories show a CC BY-NC-ND 4.0 notice on every record page, not an item licence, and several Embrapa PDFs print "Todos os direitos reservados" (all rights reserved). The Instituto de Pesca, the Instituto Mamirauá and the other sources print no open licence and are treated as all rights reserved. Only landing and trial numbers, which are facts, and short citations are used here.

Errors or missing records: please [open an issue](https://github.com/paper-rerun/fisheries-aquaculture-br/issues).

## How this dataset was made

This dataset was built by AI agents (Claude, by Anthropic) on a home computer and reviewed by a human before publication. No value was estimated or typed by hand: each one was transcribed from the source PDF twice, independently, and every disagreement was checked against the page. The method and scripts are in `method/`. How the wider project works: https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contact: Filipe Tessaro, via issues on this repository.
