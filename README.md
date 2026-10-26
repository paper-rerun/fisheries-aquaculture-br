# Fish landings and aquaculture trials in Brazil

Versão em português: [README.pt-BR.md](README.pt-BR.md)

1,672 records taken from the tables and text of 8 publications printed in Portuguese between 2004 and 2013. 1,458 are landing and catch records from 5 documents: the SCPESCA/MS 2007 bulletin of professional and sport fishing in the Pantanal (MS), artisanal fishing in the Billings reservoir in 2005-2007 (SP), landings at the port of Tefé from January to June 2012 (AM), the catch of 3 fish weirs on the coast of Piauí (PI) and artisanal gillnet landings at Tijucas (SC). 214 are treatment means from 3 aquaculture trials: tambaqui at 4 stocking densities in net cages (AM), 3 tilapia strains in raceways (AL) and jundiá in a 2 x 2 trial of stocking density and feeding frequency (RS). Each row is one printed cell or one number of the text, with the page and table it came from.

These numbers were printed as bulletins, technical reports, conference papers and journal articles, and none of them exists in structured form. Each document was checked before it was transcribed against FAO FishStat, the national fisheries bulletins, IBGE SIDRA, dados.gov.br and DataCite, and none of the 8 had its data there. FishStat has Brazil as one number per species and year; this dataset gives river, landing site, month and fleet for the places and years above.

Part of [Paper Rerun](https://paper-rerun.github.io), in its Open Tables line. The work was done by AI agents on a home computer and reviewed by a human before publication.

## What is in it

| | |
|---|---|
| Publications | 8, printed 2004 to 2013: 5 from Embrapa's open repositories (Alice and Infoteca-e), 1 report of the Instituto de Pesca (SP), 1 bulletin of the Instituto Mamirauá (AM) and 1 article in Revista Biotemas |
| Strata | 80 in 5 landing documents: 5 studies, 47 capture areas (rivers, lakes, localities), 13 inspection posts or landing sites, 7 vessel types, 2 fisheries (professional and sport), 2 data sources (port of Tefé and the Frigopeixe plant) and 4 fishing quality classes |
| Landing records | 1,458: catch weight 1,106, number of fish 119, fishers 65, number of records 45, estimated catch 41, CPUE 26, landings 18, fish sold 14, discards 9, fishing days 8, other 7. 186 of them are printed totals |
| Trials | 3, in Amazonas, Alagoas and Rio Grande do Sul |
| Trial records | 214 treatment means, 170 with a dispersion term and 78 with a significance letter |
| Species | 64 distinct common names and 126 distinct scientific names in the landing records, as printed |

| Document | What it is | State | Period, as printed | Strata or trial | Records | Availability check |
|---|---|---|---|---:|---:|---|
| albuquerque2010 | SCPESCA/MS 2007, professional and sport fishing catch in the Upper Paraguay basin, from the fish control slips of the environmental police; pages 12, 16, 17, 26 and 30 only | MS | no ano de 2007, with a 1994-2007 series | 27 strata | 441 | FishStat has Brazil only as a national total; the 2007 Ibama bulletin gives MS totals by species, in PDF; 0 hits for SCPESCA in DataCite and Redape |
| castro2009 | artisanal fishing in the Billings reservoir, from voluntary daily slips | SP | janeiro/2005 a dezembro/2007 | 1 stratum | 490 | the Instituto de Pesca's ProPesq covers marine and estuarine monitoring only; nothing on Billings in DataCite or Redape |
| mamiraua2012 | landings at the port of Tefé and fish received by the Frigopeixe plant | AM | janeiro a junho de 2012 | 44 strata | 181 | the bulletin says the data are in the institute's landing database (p2); no download or portal found |
| mai2010 | catch of 3 fish weirs (currais), scanned | PI | dezembro de 2008 a novembro de 2009 | 1 stratum | 237 | nothing on fish weirs in DataCite or Redape; no GBIF occurrence of *Opisthonema oglinum* in Piauí in 2008-2009 |
| martins2013 | artisanal gillnet landings at Barra do Rio | SC | entre setembro de 2010 e julho de 2011 | 7 strata | 109 | no supplementary material; the SC bulletins (UNIVALI/CEPSUL) cover the industrial fleet |
| brandao2004 | tambaqui juveniles at 4 densities in net cages, 60 days | AM | entre maio e julho de 2003 | 1 trial | 72 | trial means are in no national system (FishStat and SIDRA hold production); 0 hits by species and design in DataCite and Redape |
| cartaxo2010 | 3 tilapia strains in raceways, 160 days | AL | not printed | 1 trial | 30 | as above |
| martinelli2013 | jundiá, 2 x 2 of stocking density and feeding frequency in net cages, 60 days | RS | março a maio de 2010 | 1 trial | 112 | as above |

Files:
- `data/landings.csv`: one landing or catch record per row (1,458), with `doc_id`, `page` and `table_or_figure`. It carries what the record takes from its column and table (variable, unit, statistic, origin), the column header, the period and unit printed for the table, and the meaning of the footnote.
- `data/strata.csv`: one stratum per row (80). Strata nest through `parentStratumID`, from the study down to landing sites, capture areas, vessel types, fisheries and data sources. A field the child stratum does not print is taken from the nearest parent that does, and `inherited` says from which; effort, coordinates, label and pages are never passed down.
- `data/aquaculture.csv`: one trial record per row (214), with treatment, species, density, feed, duration, variable, value, dispersion and letter.
- `data/trials.csv`: one trial per row (3), with place, period, species, life stage, rearing unit, feed, water and design, as printed.
- `data/species_key.csv`: the 46 pairs of common and scientific names that 4 documents print as a species key (albuquerque2010 Tabela 1, castro2009 Tabela 5, martins2013 Tabela 1 and a text block of mai2010). They are kept apart: no record took a name from them.
- `data/sources.csv`: the 8 publications, with authors, record link and licence notice.
- `qa/decisions.csv`: every disagreement between the two independent transcriptions and how it was settled against the PDF (1,258 decisions, with page).
- `qa/totals_check.csv`: each printed total against the sum of its transcribed parts (186 totals). It is a check, not data; the dataset does not change with it.
- `method/`: the schema, the comparison script and the merge script.

### Columns

All files join `data/sources.csv` on `doc_id`. Landings join strata on `doc_id` and `stratum_ids`: `stratum_ids` lists the strata of the record within its document ("s2; s15"), and `stratumID` is `doc_id#s2`. A record belongs to all the strata it lists, such as a capture area and a fishery. Trial records join `data/trials.csv` on `doc_id` and `trial_id`. In `qa/totals_check.csv`, `record_id` is the total in `data/landings.csv` and `part_record_ids` lists the numbers after the `#` of the parts that were summed.

Names, periods and units are kept exactly as printed. Common and scientific names are in separate fields and are never paired by us: only 59 records carry both, because the same row (56) or the same cell (3) prints both. Anyone who wants to pair the others can use `data/species_key.csv`, knowing where each pair came from. A misspelling of the source stays: mai2010 prints "Anisostremus" (checked at 400 dpi), and that is what the dataset has. Printed totals are kept as records with `is_total` = True and are never recomputed; `total_kind` says if a total is a row, column, grand total or subtotal.

### Main columns

The files are UTF-8, with commas between columns. In every record, `doc_id` links the row to `data/sources.csv`, and `page` and `table_or_figure` say where it came from (PDF page counted from 1, and the table label as printed, "Tabela 4", "TABELA 01", or `text` for a number in the text). `record_id` is the record, as `doc_id#0001`.

- `stratum_ids` (landings) and `trial_id` (trial records): the strata or the trial the record belongs to.
- `stratumID`, `parentStratumID` and `stratum_dimension`: the stratum, the stratum above it and its kind (`study`, `landing_site`, `capture_area`, `vessel_type`, `fleet_or_fishery`, `data_source`, `other`).
- `period_as_printed`: the period of the record as printed ("1997", "janeiro a junho de 2012"). All landing records have one; 737 also have the wider period of the caption or methods in `period_context_as_printed`.
- `species_common_as_printed` and `species_scientific_as_printed`: the names exactly as printed, each in its own field. `taxon_status` says if the row is a taxon (830 landing records), an "Outros" category (69), a name incomplete in print (3) or not a species row at all, such as a post, month or total (556).
- `variable_standardized` and `variable_as_printed`: what was measured, in our list of terms (`catch_weight`, `cpue`, `final_weight`, `water_quality` and others in `method/schema.json`) and as the source names it.
- `value` and `value_as_printed`: the number ready for calculation, with a decimal point, and the cell as printed ("1.236", "18,47"). One cell is malformed in print ("8.14,8", albuquerque2010 Tabela 2) and has `value_kind` = `malformed`.
- `unit`: the unit as printed ("kg", "quilogramas", "toneladas", "%", "indivíduos").
- `statistic`: `single_value`, `total`, `percentage_share`, `cumulative_percentage`, `mean`, `median` or `standard_deviation`. All 214 trial records are means.
- `is_total` and `total_kind`: whether the record is a printed total, and of which kind.
- `treatment`, `treatment_type` and `is_marginal` (trial records): the treatment as printed, what it varies (`stocking_density`, `feeding_frequency`, `strain_or_genotype`, `combination`) and whether the mean is a main effect over the other factor (the 96 of martinelli2013).
- `dispersion_as_printed` and `significance_letter` (trial records): the term after ± and the letter printed with the mean.
- `inherited`: the fields the record or stratum took from its column, table or parent stratum, and from which ("unit:column", "period_as_printed:s1").

## How it was made

1. **Collection.** An agent harvested Embrapa's open repositories (Alice and Infoteca-e) through OAI-PMH: 2,767 records with a fisheries or aquaculture word, 567 candidates by title, 23 record pages and PDFs read. Embrapa has no landing statistics for the South and the Southeast, so the technical reports of the Instituto de Pesca (SP), the bulletins of the Instituto Mamirauá and an open-access journal were added. 26 candidates were read and left out, each with the reason: 11 to balance region, series or design, 6 with results only in figures or tables too thin, 3 already structured in Embrapa's Redape (doi:10.48432/XGCF7T), 3 in an archive that was offline (CEPSUL), 2 whose availability could not be settled and 1 with no treatments.
2. **Availability check.** Only documents whose data do not exist in structured form were taken. Each one went through FAO FishStat, the national bulletins (Ibama to 2007, MPA 2008-2011), IBGE SIDRA, dados.gov.br, DataCite (which registers Zenodo, figshare and Dryad DOIs), Embrapa's Redape and, when there is one, the producer's own database.
3. **Two independent transcriptions.** Two agents per publication transcribed the strata or the trial, an inventory of the tables and text blocks with numbers, the species key and every data cell into a fixed schema, without seeing each other's work, copying names, periods, units and numbers exactly as printed.
4. **Comparison and adjudication.** A script paired the two transcriptions stratum by stratum and record by record and listed every disagreement and every entry present in only one of them. Each one was settled by checking the PDF, with the page as evidence.
5. **Merge and totals check.** A script merged the adjudicated documents, filled each record from its column and table and each stratum from its parent, and summed the parts of each printed total. A landing record with no statistic printed takes `single_value`, the default of the schema (698 records). Nothing in the dataset was changed by the totals check.

## How accurate it is

- **Names and numbers:** no number and no name was misread in either transcription. In the 1,665 paired records, no digit, separator, dispersion term or significance letter was read differently from the print, including superscript markers glued to numbers (the text layer of albuquerque2010 Tabela 4 reads "19941" where the page prints 1994 with note 1), the malformed "8.14,8", the scrambled text layer of mamiraua2012 and the scan of mai2010. One transcription wrote what is not printed twice: the correct spelling *Anisotremus* where mai2010 prints "Anisostremus" (4 records), and four species named as examples in one sentence of castro2009 joined in one field (2 records). Both were set back to the print.
- **Whole records:** one transcription alone was fully correct on 98.3% of records, the other on 97.5%, counting the records each left out (7 and 0). The 7 are a header row of martins2013 Tabela 1 that prints the number of landings of each column, "(17) (20) (23) (13) (14) (22) (109)". Landings only: 98.4% and 97.2%; trial records only: 98.1% and 100%. castro2009 is 29% of the records; without it the two are 97.6% and 97.0%.
- **Strata and trials:** strata were where the two differed most. One transcription had all 80 right; the other 33 (41.2%). 43 of its 47 wrong strata are in mamiraua2012, from rules missed across the whole document: the page of each stratum label, printed in the table stub, left out (43 strata), the river of each capture area left empty although the label prints it, "Capivara (Paraná)" (33), and 16 capture areas that are Frigopeixe records marked as port monitoring. In the trials, one transcription had one field wrong in each of the 3, the other 3 fields wrong in 2 of them. All 1,258 disagreements were settled against the PDF, so the dataset does not depend on either transcription alone.
- **Printed totals:** of the 186 totals, 167 add up exactly to their transcribed parts, 10 add up within rounding, 7 do not add up and 2 cannot be checked. The two transcriptions agree on every cell involved in the 7, and so does the text layer: they are errors of the source, 5 in all. Do not use the acará row totals of castro2009 or the total of mamiraua2012 TABELA 01 as they are. Each case is in `qa/totals_check.csv`, in `status` and `note`.
  - albuquerque2010 Tabela 4, 1994: 301 t professional and 829 t sport fishing make 1,130 t; the total prints 1,152.
  - castro2009 Tabela 2, acará: the 12 months add up to 13,378.0 kg; the row total prints 13,375.0.
  - castro2009 Tabela 2, grand total: 31,498.5 matches the sum of the columns (31,498.54), not that of the row totals (31,495.54). The text (p3 and p7) gives 31,495 kg for 2005.
  - castro2009 Tabela 3, acará: the months add up to 15,810.5 kg; the row total prints 15,940.5, 130 kg more.
  - castro2009 Tabela 3, grand total: 38,391.3 matches the columns, not the row totals (38,521.3), because of the acará row above.
  - mamiraua2012 TABELA 01: the total of 534,393 kg adds the 499,763 kg of the species to the 34,630 *units* of acari-bodó, which the table marks as counted by unit.
  - mamiraua2012 TABELA 03: the percentage column adds up to 84.87, not 100. The "OUTRAS" row (81,382 kg) prints 0.15%, where 81,382 / 534,393 is 15.2%.
  - Cannot be checked: albuquerque2010 Tabela 2, column "Pescado comercializado", which has the malformed part "8.14,8"; and the text total of castro2009, 120,009 kg, which prints no parts next to it. It adds up another way: 31,499 + 38,391 + 50,119, the three yearly totals of Tabela 1, make 120,009.
- **Known limits:**
  - albuquerque2010 is a cut: 5 of its 50 pages (12, 16, 17, 26 and 30), with the species key, catch by post and fishery, the 1994-2007 series, monthly catch by species and fishers by river. The bulletin has 24 tables, about 2,000 cells.
  - mai2010 is a scan with an OCR layer, and mamiraua2012 has a layout that scrambles its text layer; both were read from the rendered page. The weir list of mai2010 prints scientific names only: its 237 records have no common name, and 9 common names are only in a text block, kept in `data/species_key.csv`.
  - Units are as printed: "kg", "quilogramas" and "Quilogramas" are the same unit in 843 records, and "toneladas" and "g" also appear. There is no standardized unit column yet, and no value was converted.
  - Periods are as printed, with no ISO dates. Only 1 stratum prints coordinates.
  - The 96 records of martinelli2013 are main effects, as the article prints them, not the means of the 4 cells of the 2 x 2.
  - The availability check has gaps: the dados.gov.br API answered 401, the Zenodo API answered 403 (Zenodo was searched through DataCite only) and SciELO Data asked for a robot challenge. None of the three was retried.
  - The coastal Southeast is missing. Its strongest candidate (Cananéia and Iguape, 1967-1994) could not be checked against the Instituto de Pesca's ProPesq, which asks for an email and a profile before showing anything.
  - One document, castro2009, holds 490 records, 29% of the dataset.

This is a pilot of 8 documents, run to settle the schema. A larger round, of 20 documents, is planned.

## Licence and citation

- The dataset (the CSV files, schema and scripts) is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the original publications listed in `data/sources.csv` as well as this dataset. Each row also carries its source in `citation` and the licence situation of its source in `license` (in Portuguese).
- The publications are not redistributed. martins2013 is the only one with an open licence: CC BY 4.0, on the article page of Revista Biotemas. Embrapa's repositories show a CC BY-NC-ND 4.0 notice on every record page, not an item licence, and albuquerque2010 prints "Todos os direitos reservados" (all rights reserved). The Instituto de Pesca prints no licence or terms for castro2009, and its PDF is password-protected; it is treated as all rights reserved. The Instituto Mamirauá site footer says "Todos os direitos reservados". The terms of the journal and proceedings of brandao2004, martinelli2013 (Pesquisa Agropecuária Brasileira), cartaxo2010 (SBZ) and mai2010 (Congresso Brasileiro de Oceanografia) were not checked. Only landing and trial numbers, which are facts, and short citations are used here.

Errors or missing records: please [open an issue](https://github.com/paper-rerun/fisheries-aquaculture-br/issues).

## How this dataset was made

This dataset was built by AI agents (Claude, by Anthropic) on a home computer and reviewed by a human before publication. No value was estimated or typed by hand: each one was transcribed from the source PDF twice, independently, and every disagreement was checked against the page. The method and scripts are in `method/`. How the wider project works: https://github.com/paper-rerun/paper-rerun/blob/main/METHOD.md

Contact: Filipe Tessaro, via issues on this repository.
