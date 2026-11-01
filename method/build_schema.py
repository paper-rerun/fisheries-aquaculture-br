# Build ../schema.json (fisheries and aquaculture, version 2.0, for the round of 20)
# Copied from pesca-piloto/method/build_schema.py (pesca-1.0-pilot) with the 13 changes of pesca-piloto/RODADA.md
# ("O que mudar no schema antes da rodada de 20"); SCHEMA_2.md says what each one changed
# Usage: py -3.12 -I build_schema.py   (writes ../schema.json; then run check_schema.py)
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
# sources.json comes with the collection step; until then doc_id is checked by pattern only
SOURCES_PATH = ROOT / "sources.json"
DOC_IDS = [document["id"] for document in json.loads(SOURCES_PATH.read_text(encoding="utf-8"))["documents"]] if SOURCES_PATH.exists() else []
SCHEMA_VERSION = "2.0"


def text(description):
	return {"description": description, "type": ["string", "null"]}


def integer(description, minimum=0):
	return {"description": description, "type": ["integer", "null"], "minimum": minimum}


def enum(description, values, nullable=False):
	if nullable:
		return {"description": description, "type": ["string", "null"], "enum": values + [None]}
	return {"description": description, "type": "string", "enum": values}


def obj(properties, description=None):
	result = {"type": "object", "additionalProperties": False, "required": list(properties), "properties": properties}
	if description:
		result = {"description": description, **result}
	return result


PAGE = {"type": "integer", "minimum": 1}
PAGE_OR_NULL = {"type": ["integer", "null"], "minimum": 1}
PLACE = ["header", "stub", "caption", "footnote", "legend", "methods", "text", "other_table"]

# ---------- Vocabularies ----------

STRATUM_DIMENSIONS = ["study", "landing_site", "capture_area", "fleet_or_fishery", "gear", "vessel_type", "data_source", "administrative_area", "other"]
COLLECTION_METHODS = ["census_of_landings", "sampled_landings", "landing_forms_or_logbooks", "inspection_records", "buyer_or_plant_records", "interviews", "participatory_monitoring", "experimental_fishing", "mixed", "not_stated"]
RECORD_ORIGINS = ["monitoring_programme", "third_party_records", "cited_source", "mixed", "not_stated"]

LANDING_VARIABLES = [
	"catch_weight", "catch_weight_estimated", "commercialized_weight", "purchased_weight", "discard_weight",
	"catch_number", "discard_number", "catch_value", "price", "n_landings", "n_records", "n_trips", "n_fishing_days",
	"n_fishers", "n_boats", "cpue", "fishing_effort", "sample_size", "other",
]
TRIAL_VARIABLES = [
	"initial_weight", "final_weight", "weight_gain", "daily_weight_gain", "specific_growth_rate", "initial_length",
	"final_length", "length_gain", "condition_factor", "uniformity_or_cv", "survival_pct", "final_biomass", "biomass_gain",
	"productivity", "feed_intake", "feed_conversion_ratio", "feed_efficiency", "protein_efficiency_ratio", "carcass_yield",
	"fillet_yield", "body_composition", "organ_somatic_index", "blood_parameter", "water_quality", "economic",
	"sample_size", "other",
]
STATISTICS = ["single_value", "total", "mean", "median", "standard_deviation", "percentage_share", "cumulative_percentage", "relative_to_control", "other"]
TOTAL_KINDS = ["row_total", "column_total", "grand_total", "subtotal", "cumulative_total"]
TREATMENT_TYPES = [
	"stocking_density", "feeding_rate", "feeding_frequency", "feeding_regime_other", "diet_protein_or_energy_level",
	"diet_ingredient_or_substitution", "feed_additive", "strain_or_genotype", "sex_or_sex_reversal", "rearing_system",
	"water_or_environment", "size_grading", "transport_or_handling", "health_treatment", "control", "combination", "other",
]
ENVIRONMENTS = ["net_cage_in_reservoir_or_lake", "net_cage_in_pond", "earthen_pond", "concrete_tank_or_raceway", "circular_tank", "recirculating_system", "aquarium_or_laboratory", "hapa", "other"]
TABLE_KINDS = [
	"landing_results", "trial_results", "species_key", "stratum_context", "trial_design", "context", "anova",
	"comparison", "figure_labeled", "figure_unlabeled", "text",
]
COLUMN_ROLES = [
	"row_label", "species_common", "species_scientific", "value", "total", "percentage_share", "cumulative_percentage",
	"rank_or_order", "code", "statistic_test", "other",
]
VALUE_KINDS = ["numeric", "range", "class", "symbol", "malformed", "illegible"]
MEASUREMENT_TIME_REFERS_TO = ["days_of_trial", "sampling_event", "end_of_trial", "phase", "date", "other"]

# ---------- Rules ----------

RULES = [
	"1 SCOPE. Inventory and transcribe every page of the document, except when sources.json gives extract_pages for it. Then only those pages go to tables[] and records[]; the rest is read only to fill strata[], trials[] and species_key[] (methods, site descriptions, legends, defeso dates, collection method).",
	"2 TWO KINDS OF DOCUMENT. document_kind is 'landings' (catch and landing statistics, artisanal fishery surveys: strata[] and landing records) or 'aquaculture_trial' (growth, survival, feed conversion, yield by treatment: trials[] and trial records), as sources.json says. Every record says record_type. A landings document has trials = [] and an aquaculture document has strata = [].",
	"3 INVENTORY FIRST, EVERY TABLE AND FIGURE. Before writing any record, render every page in scope and list in tables[], in page order, every table, figure, map, photo, chart and species key, and every text block that gives records or pairs names (rule TEXT VALUES), with table_id, page, label, kind and data_cells. Every figure, map, photo and diagram is inventoried, with data_cells = 0 and kind figure_unlabeled when it prints no value. A table continued on the next page gets one entry per page. A block without its own number but with its own header (a second year under the same caption) is its own entry. At the end each entry closes: data_cells = transcribed + skipped_cells, and transcribed = number of records with that table_id.",
	"4 READ FROM THE RENDERED PAGE. The printed page is the source. Text layers of designed bulletins scramble captions and columns (mamiraua2012 p3 reads 'TABELA 01. Produção (kg)' then 'das principais esp'), glue superscript footnote markers to the number (albuquerque2010 Tabela 4, p17: the layer reads '19941' and '4392'; the page prints 1994 with marker 1 and 439 with marker 2) and lose the gap between cells (castro2009 Tabela 3, p11: '56,8 0.0' is two cells). Render at 150 dpi; go up only for one unreadable character.",
	"5 STRATA FIRST (landings). One strata[] entry for the whole survey (s1, stratum_dimension = study), then one per printed level of every axis that splits the numbers: landing site, port, inspection post or entreposto; capture area (river, lake, bay, fishing ground, locality of origin); fleet or fishery (profissional, esportiva, artesanal, industrial); gear; vessel type; data source when the document reports two sources side by side (Porto de Tefé and Frigorífico Frigopeixe in mamiraua2012). A level printed under another of the same dimension points to it in parent_stratum_id (a destacamento under its pelotão); every other level points to s1, except a capture area printed only in the table of one data source, which points to that data source (mamiraua2012 Tabela 04: the areas of the Frigopeixe records), so its record_origin comes down from it. A capture area is itself a place: its stub label goes to water_body_as_printed of its own stratum as printed ('Capivara (Paraná)', 'Tuiuca (lago)'), and a label with no water body ('Localidade não informada', 'OUTRAS') leaves it null instead of taking the survey's rivers. Period is not a stratum: it goes on the record (rule PERIOD). Fix the strata before writing records.",
	"6 STRATUM FIELDS ONCE, WITH PAGE. Fill each stratum field from wherever the document prints it (methods, site table, caption, footnote, map legend, abstract) and put the page in field_pages. The label of a stratum read from a table stub needs no field_pages entry: its page is the page of the table and the merge takes it from the first record of that stratum; field_pages holds the label page only when the label is printed outside the tables (methods, a site list). A field printed once for the whole survey goes on s1 and the others inherit it; a stratum repeats it only when its own value differs. null only when printed nowhere. Never take a place from the authors' affiliation, the publisher's address or the series name: Embrapa Pantanal, Corumbá is the publisher, not a landing site. data_collection_method_as_printed quotes the collection method (at most 15 words: 'preenchimento de fichas diárias', 'Guia de Controle de Pescado', 'acompanhamento do desembarque pesqueiro') and data_collection_method classifies it. coverage_gaps_as_printed holds printed gaps (defeso, months without data, 'Dados disponíveis a partir de maio').",
	"7 TABLE AXES BEFORE RECORDS. For every landing_results, trial_results, figure_labeled and text entry, fill table_level_labels before any record: what the rows are, what the columns are, the layout (single block, side-by-side blocks, transposed), the period and unit the caption gives the whole table, every printed total and summary row or column with its label, every symbol and footnote. Then fill columns[]: one entry per printed column with its header as printed and its role (rule COLUMN ROLES). A table printed in side-by-side blocks (mai2010, Tab. 1: two blocks of Taxa, N, P (g)) gets one columns[] entry per column of each block, and records carry column_block.",
	"8 FULL HEADERS. header_as_printed copies the whole header, top line to bottom line, spanning headers joined with ' / ' ('Pesca / Profissional / %', 'Nº de pescadores/mês', 'Densidade de estocagem (peixes/m3) / 300'), units and markers included. Never cut a header: in the biodiversity pilot a header cut in the middle cost 112 fields.",
	"9 COLUMN ROLES, closed examples. row_label = the stub (species, local de vistoria, mês, ano, tratamento); species_common and species_scientific = name columns; value = a column of numbers for one variable, period or stratum ('Mar.', 'Profissional', 'Produção (kg)', 'PF (g)'); total = a column that adds the others of its row ('Total', 'Total Geral'); percentage_share = '%', 'Porcentagem', 'Total relativo (%)'; cumulative_percentage = '% Ac.'; rank_or_order = a printed order number before the name (the 1 to 11 of the Araguaia table), not data; code = a printed code column; statistic_test = a CV, F, P or DMS column, counted and skipped; other.",
	"10 ONE RECORD PER PRINTED DATA CELL. Every body cell that prints a number (0 included), a class, a date or a defined symbol is a data cell and gives one record: values, totals, subtotals, means, medians and standard deviations printed as rows or columns, percentages and cumulative percentages. A line of sample sizes printed under the header is data, one record per cell, with the variable it counts: martins2013 Tabela 1 prints '(17) (20) (23) (13) (14) (22) (109)' under the months, the landings analysed per column, so 7 records of n_landings (sample_size when the document does not say what was counted), row_label_as_printed the header that explains them. A printed range is one record, never two: 'variou de 1 a 17' gives value_kind = range, value = null, value_min = 1, value_max = 17, value_as_printed '1 a 17'. Not data cells: headers, stub labels, heading rows, rank numbers, blank cells, and '-' or '--' unless the legend defines the dash (then value_kind = symbol, value = null, never converted to 0). ANOVA and test statistics (CV, F, P, DMS, residual standard deviation, 'ns' verdict rows, regression equations, R2) are counted and skipped (rule STATISTICS ARE NOT DATA).",
	"11 TOTALS ARE RECORDS, NEVER RECOMPUTED. A printed total ('Total', 'Total (ano)', 'Total Geral', 'Produção total', 'Total (T)', 'Somatório', 'Total Geral (T)') is recorded like any other cell, with is_total = true and total_kind (row_total = adds across its row, column_total = adds down its column, grand_total = the corner cell, subtotal = a partial sum, cumulative_total). A summary row that is not a sum ('Média', 'Desvio Padrão', 'Mediana') has is_total = false and its statistic. Never fix, recompute or check a total during transcription: a total that does not add up is kept as printed. The sums are checked by script after adjudication, and that check is why totals are kept.",
	"12 SPECIES AS PRINTED, TWO FIELDS, NEVER MATCHED. species_common_as_printed and species_scientific_as_printed each copy what that row of that table prints, with authorship, qualifiers ('sp.', 'spp', 'cf.'), spacing, typos and old spellings ('Dasyatjdae', 'Megalops at/anticus', 'Jau' and 'Jaú', 'Anisostremus' in mai2010 Tab. 1 where the valid genus is Anisotremus, 'Steliffer sp.' next to 'Stellifer stellifer' in the same table). Never correct a spelling, not even to the valid name. Names printed as examples of a group inside a sentence ('como a carpa (Cyprinus carpio), traíra...', castro2009 p7) are not record names: the record keeps the group the sentence counts, and the examples stay out. The scientific name is filled only when the same row or the same cell of the same table prints it ('Pacu (Piaractus mesopotamicus)'), and species_pairing says how. Never fill it from a species key, another table, the text or our own knowledge, even when the key sits on the facing page: the pairing is a later step outside the transcription. A row that is a catch-all ('Outros', 'OUTROS', 'Outras espécies', 'Diversos') has taxon_status = others_category. A row whose name cell holds no taxon name (only authorship, only '-', a group word such as 'Peixes de couro') has taxon_status = incomplete_in_print and the printed text stays in row_label_as_printed.",
	"13 RANK WORDS ARE NOT PART OF NAMES. A heading row 'Família Carcharhinidae' gives family_as_printed = 'Carcharhinidae'; 'ORDEM CHARACIFORMES' gives higher_group_as_printed = 'CHARACIFORMES'; a class heading ('Chondrychthyes', 'Osteichthyes', 'Crustáceos') goes to higher_group_as_printed as printed, joined top-down with ' / '. A heading row is not a data cell. Never infer a family from the genus.",
	"14 NAME PROBLEMS. A scientific name printed with the genus abbreviated ('M. ancylodon') keeps the abbreviation; scientific_name_in_full_as_printed and its page are filled only when the same document prints the full name in another table or the text. A name spelled differently in two tables of the same document (or in the text) gets source_inconsistency on every record of that name in both tables, with both spellings and pages. A footnote marker printed on a name ('Pinirampus pirinampu (Spix, 1829) 1') goes to footnote_marker, not into the name.",
	"15 SPECIES KEYS. A table or block that only pairs common names with scientific names (albuquerque2010 Tabela 1, p12; castro2009 Tabela 5, p12) is kind species_key, data_cells = 0, and each printed pair goes once to species_key[], one entry per scientific name (two names under 'Barbado' give two entries), with its markers. species_key[] is the only place where a common and a scientific name sit together without being on the same row of a results table.",
	"16 VARIABLE, UNIT, STATISTIC PER COLUMN. Each value column says variable_standardized (closed list), its unit as printed and where it was read (header, caption, footnote, methods, text, unit_source_place), and its statistic. Catch weight is catch_weight; a printed 'Estimativa de captura' is catch_weight_estimated; 'pescado comercializado' is commercialized_weight; 'Descarte' is discard_weight or discard_number as the unit says; 'N' of individuals is catch_number; 'Nº de registros' is n_records; 'Número de desembarques' is n_landings; 'NDP' is n_fishing_days; 'CAPPVG', 'CAPPD', 'kg/dia' and 'g/m2.hora' are cpue with the unit as printed; 'Nº de pescadores' is n_fishers. A '%' column keeps the variable it is a share of and statistic = percentage_share; '% Ac.' is cumulative_percentage. A row with its own unit (mamiraua2012 Tabela 01: Acari-bodó counted in units, '* Produção por unidade') carries unit on its records. When the caption or a note prints the whole unit ('em quilogramas por pano de rede de 50 m') and the stub or header only an abbreviation ('Média em kg'), the caption unit wins, with unit_source_place = caption; a unit printed only in the caption ('número de dias de pesca (NDP)' gives 'dias') counts as printed and is never not_printed. statistic null means single_value on landing tables and the table statistic on trial tables; a transcriber may write single_value or leave it null, compare.py and merge.py read both the same. Never convert t to kg, g to kg or units to weight: the merge adds unit_standardized (the same unit in one spelling) and never touches the value.",
	"17 PERIOD AS PRINTED, PER CELL. period_as_printed holds the most specific period printed for the cell, from its column header, its row label or the caption, exactly as printed ('Mar.', 'jan', 'Dez', '2005', '1º semestre de 2012', 'set/2010'); period_context_as_printed holds the broader period the caption or methods print when the cell's own period is narrower ('no ano de 2007' for a 'Mar.' column). A month printed only as a number in a stub ('3' in albuquerque2010 Tabela 13) is copied as printed. Never build a date, never add a year the cell does not print, never take a year from the publication date. Every value column says its period, or period_status = not_printed after header, caption, footnotes and methods were read. A text value with no narrower period of its own takes the period of its paragraph or, failing that, the study's period in period_as_printed, as printed, with that page in period_source_page; a phrase that only points to a period ('ao longo deste período', 'no mesmo período') is resolved to the printed period it points to, never copied as the period.",
	"18 STRATUM OF A CELL. stratum_ids lists every stratum the cell belongs to: the stratum of its row (a local de vistoria), the stratum of its column (Profissional) and the stratum the caption gives the whole table, one per dimension, most specific first. A record of a whole-survey table points to s1 only. The table entry lists in stratum_ids every stratum with a cell on that page.",
	"19 COPY NUMBERS EXACTLY. value_as_printed is the cell exactly as printed, without footnote markers, letters and dispersion term; value is the number. The only allowed changes are decimal comma to point and dropping a thousands point ('150.560' -> 150560, '1.166,00' -> 1166.0). A point that could be decimal or thousands is decided from the column's other cells and unit, with notes when not obvious. A table that mixes separators keeps each cell as printed ('0.0' among '0,0' cells). A number whose separators cannot be read as one number ('8.14,8', albuquerque2010 Tabela 2, p16) has value_kind = malformed, value = null and value_as_printed as printed; never guess the intended number. A superscript or footnote marker on a number goes to footnote_marker.",
	"20 NEVER COMPUTE OR INFER. No sums, no shares, no CPUE, no per-fisher or per-day values, no monthly values from annual ones, no conversions, no values read off a chart by eye, no value derived from a regression. If the document does not print the number, it does not go in.",
	"21 WHO RECORDED IT. record_origin says where the document says the numbers came from: monitoring_programme = the survey or monitoring the document reports (porto de Tefé, guias do SCPESCA, fichas diárias da Billings); third_party_records = records handed over by an organisation outside the monitoring (the Frigopeixe reception control in mamiraua2012); cited_source = another publication; mixed; not_stated. It is set on the stratum and on the table and repeated on a record only when that row differs.",
	"22 TEXT VALUES. A per-stratum or per-period value printed only in the body text is a mandatory record when no table or labelled figure prints it (mamiraua2012 p3 gives the monthly Frigopeixe receptions only in the text): table_or_figure = 'text', one tables[] entry with label 'text' per page, the quote (at most 15 words) in notes. Only text blocks with results of this study or a species key (scientific with common names) go to tables[]; numbers in methods, discussion, other studies and references give no entry. A text entry has one implicit column: columns = [{column_id 'c1', header_as_printed 'text', role value, variable, unit and statistic null}], every record of the block has column_id c1, row_index counts the values in reading order, and each record writes its own variable_standardized, unit and statistic. A and B are paired by the number cited, not by position. A text value that repeats a table cell is not recorded again. A text value that contradicts a table is not a record: it goes to source_inconsistency of the table record.",
	"23 CONTRADICTIONS THE DOCUMENT PRINTS. When the document contradicts itself (text against table, caption against methods, a name spelled two ways, two tables giving the same cell two values, a footnote that does not match), record the table value and fill source_inconsistency with both versions and pages, on the record, the table or the stratum it is about. A sum we would have computed is not a contradiction (rule TOTALS ARE RECORDS).",
	"24 ILLEGIBLE CELLS STAY IN. A data cell that cannot be read with confidence is a record with value_kind = illegible, value = null, the best reading in value_as_printed and the doubt in notes. It counts as transcribed.",
	"25 FIGURES. A figure gives records only when it prints the values at its bars, slices or points (kind figure_labeled); its series are its columns[]. Bar charts, pie charts, curves and maps without printed values are figure_unlabeled with data_cells = 0. Values are never read off an axis.",
	"26 AS-PRINTED FIELDS HOLD ONLY PRINTED WORDS. Every *_as_printed field and every place field holds only the printed words of that thing, at most 15 words: the locality without the municipality and state that have their own fields, the method without the sentence around it. Our own explanations go to notes, never into an as-printed field (the biodiversity pilot found glosses such as '(por ponto por campanha, p7)' inside samplingEffort). Symbol and code meanings are written once in table_level_labels.symbols, not on each record. notes, source_inconsistency and every other free-text field quote at most 15 words of the document.",
	"27 TRIALS FIRST (aquaculture). One trials[] entry per experiment: per site, per phase printed as its own block (recria and terminação), per system and per experiment number. A block of means pooled across trials gets its own trial with study_kind = joint_analysis and pooled_from. A demonstration unit or production case with one treatment is study_kind = production_case.",
	"28 TRIAL CONTEXT ONCE, WITH PAGE. Fill each trial field once from wherever the document prints it, with the page in context_source_pages: species, strain or origin of the fish, life stage and initial size, rearing unit and its size, stocking density, feed (type, crude protein, ration, frequency), duration, period, location, water supply, renewal and aeration, replicates and design. Long context is written in our own words. Management applied the same way to every unit of a trial whose treatment is something else (the same commercial feed, prophylactic baths, anaesthesia at biometry) is context in uniform_management, never a treatment and never on the records.",
	"29 TABLE AXES OF A TRIAL TABLE. column_axis_kind: variables = each column is a variable (the usual); treatments = the treatments are the columns and the variables are the rows (cartaxo2010 Tabela 1: Tailandesa A, Tailandesa B and GIFT as columns), one columns[] entry per treatment with factor_level and one record per cell, the variable taken from the row; evaluation_times = the same variable at several times (30 and 60 days in brandao2004 Tabela 2), one columns[] entry per time with its own measurement_time; treatment_factor = the columns are levels of a factor, joined to the row treatment with ' x '; trial_blocks = column blocks that are separate trials.",
	"30 MAIN EFFECTS ONLY. When the methods describe a factorial and the table prints only the mean of each level of one factor over the other, main_effects_only = true and every record has is_marginal = true with treatment_type = the class of that level's factor. Closed example, martinelli2013 Tabela 1 (p4): a 2 x 2 factorial of density and feeding frequency printed as four rows 'D–50', 'D–150', 'F–1', 'F–2'; the D rows are stocking_density and the F rows feeding_frequency, all is_marginal = true. Negative example: a one-factor table (brandao2004, four densities) is never marginal.",
	"31 TREATMENT AS PRINTED. treatment is the row or column label exactly as printed, with its level and unit when the stub prints them ('D–50, 50 jundiás por m3', '200', 'Tailandesa A'); a numeric stub whose unit is in the spanning header takes the header unit in stocking_density_as_printed or feeding_regime_as_printed, never in treatment. treatment_code holds a printed code ('D–50', 'T3'). Every special row (control, mean, a positive reference diet) is listed in row_identity.special_rows and carries treatment_type on its records.",
	"32 WHEN IT WAS MEASURED, PER COLUMN, NEVER INVENTED. Every trial column declares measurement_time_status. When the time is printed (header '30 dias', caption 'no período de 160 dias', methods 'aos 30 e 60 dias de criação foram capturados 30 peixes'), measurement_time holds it with its page and place. A final-weight or survival column takes the end of the trial only when the document prints the duration or the date of the final biometry; otherwise not_printed. A column with no time (feed composition, a whole-period mean of water quality) is not_applicable only when the document says it is a mean over the period; then measurement_time quotes that.",
	"33 STATISTICS ARE NOT DATA. CV, F, P or p-values, DMS, Tukey or Duncan values, residual standard deviation ('Desvio‑padrão residual'), effect verdict rows ('Efeito da densidade (D) ns', 'Interação D × F ns'), regression equations, R2, correlation matrices and fitted parameters are counted as data cells and skipped, with the count in skipped_reason. A table made only of them is kind anova.",
	"34 DISPERSION AND LETTERS. A dispersion term attached to a value ('± 3,06', '±0,03') goes to dispersion_as_printed of that record, never a separate record; what it is (erro-padrão, desvio-padrão) goes once in table_level_labels.dispersion_meaning_as_printed with the page. Significance letters and asterisks go to significance_letter exactly as printed ('a', 'ab', 'A', '*', 'ns' printed on a value); what they compare goes once in letters_meaning. Closed example, martinelli2013 (p4 to p6): 'ns' and '*' printed on the effect verdict rows are not letters; those rows are skipped (rule STATISTICS ARE NOT DATA), their meanings go to symbols, and letters_meaning stays null unless letters are printed on the values (Tabela 4, 'Médias seguidas de letras iguais...'). A footnote whose marker is '(1)' and whose text starts with 'ns' (Tabela 2) is one footnote: marker '(1)', text with the 'ns' definition, and 'ns' also in symbols. Two notes printed on one line ('*' Significativo..., 'ns' Não significativo, Tabela 5) are two footnotes[] entries, one per marker.",
	"35 WATER QUALITY. Water-quality values printed per treatment (brandao2004 Tabela 1, cartaxo2010 Tabela 2) are trial records with variable_standardized = water_quality and the parameter in the column or row label. Values printed only for the whole trial or for the water body outside the units (the açude in brandao2004 p2) are trial context in water_context_as_printed, not records. A sentence saying the water stayed within adequate limits, with no number, is also water_context_as_printed (cartaxo2010 p2); null only when the document says nothing about the water of the trial.",
	"36 DESIGN TABLES ARE CONTEXT. Diet formulation and composition tables, feeding-rate schedules, lists of treatments and sites are kind trial_design or stratum_context, data_cells = 0, and fill trials[], strata[] and the records' feed_as_printed and feeding_regime_as_printed. A diet composition measured as a result of the treatments (body composition of the fish) is trial_results.",
	"37 page is the PDF page number counted from 1 (first page of the file = 1), not the number printed on the page. table_or_figure is the label as printed ('Tabela 2', 'TABELA 01', 'Tab. 1', 'Quadro 1', 'Figura 3', 'text').",
	"38 TWO INDEPENDENT TRANSCRIPTIONS. Each document is transcribed twice, by A and B, each without seeing the other. A script diffs A and B record by record (landings key: table_id, column_block, row_index, column_id; trials key: table_id, row_index, column_id) and field by field, and an adjudicator decides every difference against the rendered page. Write transcriber = 'A' or 'B'.",
	"39 END-OF-TRANSCRIPTION CHECKLIST. Before closing, fill end_checklist: strata (each stratum field filled, inherited or not_printed), trials (each trial field likewise), tables (each entry closes), rows (taxon or stub lines printed against distinct row_index per block), totals (every printed total row and column found in table_level_labels.printed_totals and recorded with is_total), species (records whose scientific name was filled from outside their own row must be 0), markers (every footnote marker taken off a number or a name), units and periods (every value column with its unit and period or not_printed), measurement times (every trial column with its status), symbols (every symbol with its meaning or 'undefined') and the sums over tables[].",
]

CHANGES = [
	"From pesca-1.0-pilot, the 13 changes of pesca-piloto/RODADA.md:",
	"1 Default statistic: null = single_value on landing tables, applied by compare.py before comparing and by merge.py (rule 16).",
	"2 The label page of a stratum read from a table stub is no longer required in field_pages; merge.py takes it from the first record (rule 6, strata.csv label_page).",
	"3 A capture area is a place: its stub fills its own water_body_as_printed, and an area printed only in one data source's table points to that source (rule 5).",
	"4 Text period: a text value takes its paragraph's or the study's period, with period_source_page; pointing phrases are resolved (rule 17, new landing field period_source_page).",
	"5 A sample-size line under the header is data, closed example martins2013 Tabela 1 (rule 10).",
	"6 Ranges: value_kind range with value_min and value_max, one record ('variou de 1 a 17') (rule 10, new record fields value_min and value_max).",
	"7 Spelling as printed with examples (Anisostremus, Steliffer); names given as examples of a group in a sentence are not record names (rule 12).",
	"8 The caption unit wins over an abbreviation in the stub, and a unit printed only in the caption counts as printed (rule 16).",
	"9 unit_standardized derived in merge.py, the same unit in one spelling, values never converted (rule 16).",
	"10 Narrower text inventory: only text blocks with results of this study or a species key (rules 3 and 22).",
	"11 Closed example for trial footnotes and verdict symbols, martinelli2013 '(1)ns' and '*' (rule 34).",
	"12 A sentence saying the water stayed within adequate limits is water_context_as_printed (rule 35).",
	"13 A text block has one implicit column c1 and A and B text records are paired by the number cited, not by position (rule 22, compare.py).",
]

# ---------- Definitions ----------

symbol = obj({
	"symbol": {"description": "The code, letter, mark or abbreviation as printed ('*', 'S.I.', 'T', 'ns', 'Dois rios').", "type": "string"},
	"meaning_as_printed": text("Its meaning as printed, at most 15 words; null when the document defines it nowhere."),
	"page": {**PAGE_OR_NULL, "description": "PDF page where the meaning is printed; null when meaning_as_printed is null."},
	"place": enum("Where it is defined.", PLACE, nullable=True),
})

footnote = obj({
	"marker": text("Footnote marker as printed ('1', '2', '*', '(1)', 'ns'), or null for an unmarked note."),
	"text": {"description": "The note as printed, at most 15 words.", "type": "string"},
	"used_for": {"description": "Field or columns that took it, or 'nothing'.", "type": "string"},
})

printed_total = obj({
	"label_as_printed": {"description": "The total or summary label exactly as printed ('Total', 'Total (ano)', 'Total Geral (T)', 'Média', 'Desvio Padrão', 'Produção total').", "type": "string"},
	"axis": enum("row = a printed row; column = a printed column.", ["row", "column"]),
	"kind": enum("What it is: a sum (row_total, column_total, grand_total, subtotal, cumulative_total) or a summary statistic.", TOTAL_KINDS + ["mean", "median", "standard_deviation", "other"]),
	"cells": {"description": "Data cells in that row or column.", "type": "integer", "minimum": 0},
})

landing_labels = obj({
	"labels_kind": {"const": "landings", "type": "string"},
	"row_axis": enum("What the rows are.", ["species", "landing_sites", "capture_areas", "fleets_or_fisheries", "gear", "vessel_types", "months", "years", "periods", "variables", "categories", "mixed", "other"]),
	"row_axis_as_printed": text("The stub header as printed ('Espécie', 'Local de vistoria', 'Nome Peixe', 'Taxa', 'Mês'), or null when the stub has none."),
	"column_axis": enum("What the columns are.", ["variables", "periods", "landing_sites", "capture_areas", "fleets_or_fisheries", "gear", "vessel_types", "sampling_occasions", "species", "mixed", "other"]),
	"layout": enum("single_block; side_by_side_blocks = the same columns printed twice or more side by side (rule TABLE AXES); transposed = what is usually a row is a column; continued = this entry continues a table from the previous page.", ["single_block", "side_by_side_blocks", "transposed", "continued"]),
	"table_period_as_printed": text("Period the caption or a note gives the whole table, as printed ('no ano de 2007', '1º semestre de 2012', 'entre 2008 e 2009', 'jan/05 a dez/07')."),
	"table_period_place": enum("Where the table period was read.", PLACE, nullable=True),
	"unit_statement_as_printed": text("Unit the caption or a note gives the whole table, as printed ('(kg)', 'em quilogramas', 'peso em quilograma'), else null."),
	"quantity_meaning_as_printed": text("What the numbers are, as printed, with page and place when not in the caption ('Quantidade de pescado capturado (kg)', 'Quilogramas por espécie desembarcados em cada amostragem')."),
	"printed_totals": {"description": "Every printed total and summary row or column (rule TOTALS ARE RECORDS).", "type": "array", "items": printed_total},
	"heading_levels": {"description": "Printed heading rows that group the rows, top-down ('Chondrychthyes', 'Família', 'Osteichthyes').", "type": "array", "items": {"type": "string"}},
	"symbols": {"description": "Every symbol, code or mark used in the cells or stub, once (rule AS-PRINTED FIELDS HOLD ONLY PRINTED WORDS).", "type": "array", "items": symbol},
	"footnotes": {"description": "Every footnote and note under the table.", "type": "array", "items": footnote},
	"record_origin": enum("Rule WHO RECORDED IT, for the whole table.", RECORD_ORIGINS),
	"source_inconsistency": text("Contradiction the document prints about the table as a whole, both versions and pages (rule CONTRADICTIONS THE DOCUMENT PRINTS)."),
})

trial_labels = obj({
	"labels_kind": {"const": "aquaculture_trial", "type": "string"},
	"statistic": enum("What the body cells are, for every column that does not say otherwise.", STATISTICS, nullable=True),
	"statistic_stated": {"description": "true when the caption, header, footnote or methods say what the cells are ('Médias±erro-padrão seguidas...'); false when set from context.", "type": "boolean"},
	"statistic_source_page": {**PAGE_OR_NULL, "description": "Page of that statement; null when statistic_stated is false."},
	"statistic_source_place": enum("Where it was read; null when statistic_stated is false.", PLACE, nullable=True),
	"dispersion_meaning_as_printed": text("What the ± or parenthesis term is, as printed ('erro-padrão', 'desvio-padrão', 'Média±desvio‑padrão'), with page in footnote_summary when not in the caption; null when no dispersion is printed."),
	"transformation_stated": text("Transformation the document says was used for every column, as printed; null otherwise."),
	"treatment_type": enum("Class of the ordinary rows (or treatment columns).", TREATMENT_TYPES),
	"row_identity": obj({
		"axes": obj({
			"row_factors": {"description": "What the rows are, in printed order ('densidade de estocagem', 'tratamento (D e F)', 'parâmetro').", "type": "array", "items": {"type": "string"}},
			"column_axis_kind": enum("Rule TABLE AXES OF A TRIAL TABLE.", ["variables", "treatments", "evaluation_times", "treatment_factor", "trial_blocks"]),
			"column_factor": text("The factor on the columns when column_axis_kind is treatments or treatment_factor ('Densidade de estocagem (peixes/m3)', 'linhagem'); null otherwise."),
			"main_effects_only": {"description": "Rule MAIN EFFECTS ONLY.", "type": "boolean"},
		}),
		"row_label_form": enum("name_only, code_only, code_and_name, level_only (a number or level, the factor in the header).", ["name_only", "code_only", "code_and_name", "level_only"]),
		"rows_printed": {"description": "Treatment rows (or treatment columns when transposed) printed, excluding statistic rows.", "type": "integer", "minimum": 0},
		"special_rows": {"description": "Rows whose class differs from treatment_type (control, mean, reference diet), as printed.", "type": "array", "items": {"type": "string"}},
	}),
	"significance_test": text("Test named for the letters ('Tukey a 5%', 'Duncan, a 5%'), else null."),
	"letters_meaning": text("What the letters or asterisks compare, as printed (at most 15 words), else null."),
	"footnotes": {"description": "Every footnote and note under the table.", "type": "array", "items": footnote},
	"symbols": {"description": "Every abbreviation of the header or stub with its printed meaning ('PI, massa inicial', 'CAA').", "type": "array", "items": symbol},
	"source_inconsistency": text("Contradiction the document prints about the whole table, both versions and pages."),
})

column = obj({
	"column_id": {"description": "'c1', 'c2' ... left to right; across side-by-side blocks the numbering continues. For a transposed trial table, one entry per treatment column.", "type": "string", "pattern": "^c[0-9]+$"},
	"column_block": {"description": "Block of a side-by-side layout, from 1 at the left; 1 for every single-block table.", "type": "integer", "minimum": 1},
	"header_as_printed": {"description": "Rule FULL HEADERS.", "type": "string"},
	"role": enum("Rule COLUMN ROLES.", COLUMN_ROLES),
	"variable_standardized": enum("For value, total, percentage_share and cumulative_percentage columns: the variable (landing or trial list). null for label, name, rank, code and statistic_test columns, and for the treatment columns of a transposed trial table, whose variable comes from the row.", LANDING_VARIABLES + [v for v in TRIAL_VARIABLES if v not in LANDING_VARIABLES], nullable=True),
	"unit": text("Unit as printed for this column, from header, caption, footnote, methods or text ('kg', 'Ton.', 'T', 'g', 'kg/m3', 'peixes/m3', '%', 'mg/L', 'R$'); null when printed nowhere or not applicable."),
	"unit_source_place": enum("Where the unit was read, or not_printed after header, caption, footnotes, methods and text were searched; not_applicable for label columns.", ["header", "caption", "footnote", "methods", "text", "not_printed", "not_applicable"]),
	"statistic": enum("Null = as the table (trials) or single_value (landings); writing single_value is the same. Filled when the column is a total, a share, a mean or another statistic.", STATISTICS, nullable=True),
	"is_total_column": {"description": "true for a column that adds the others of its row (rule TOTALS ARE RECORDS).", "type": "boolean"},
	"period_as_printed": text("Landings: the period this column holds, as printed in its header ('Mar.', 'jan', '2006'), else null (rule PERIOD)."),
	"period_status": enum("Landings: filled when the column or the table prints its period, from_row when each row prints it, not_printed, not_applicable (label columns and trial tables).", ["filled", "from_row", "from_table", "not_printed", "not_applicable"]),
	"stratum_id": {"description": "Landings: the stratum this column holds (Profissional, Esportiva, a landing site), else null.", "type": ["string", "null"], "pattern": "^s[0-9]+$"},
	"factor_level": text("Trials: the treatment or factor level this column holds when the treatments or a factor are on the columns ('Tailandesa A', '300'), else null."),
	"measurement_time": text("Trials: when this column was measured, as printed (rule WHEN IT WAS MEASURED), else null."),
	"measurement_time_refers_to": enum("Trials: what measurement_time counts from.", MEASUREMENT_TIME_REFERS_TO, nullable=True),
	"measurement_time_source_page": {**PAGE_OR_NULL, "description": "Page where measurement_time was read; null when it is null."},
	"measurement_time_source_place": enum("Where it was read; null when measurement_time is null.", PLACE, nullable=True),
	"measurement_time_status": enum("Trials: filled, not_printed, not_applicable; landings: not_applicable.", ["filled", "not_printed", "not_applicable"]),
	"notes": text("What a header abbreviation means and the page of its key, what a share is a share of, at most 15 words quoted."),
})

table = obj({
	"table_id": {"description": "'k1', 'k2' ... in page order; one per page for a continued table.", "type": "string", "pattern": "^k[0-9]+$"},
	"page": {**PAGE, "description": "PDF page (from 1) of this entry."},
	"label": {"description": "Label as printed ('Tabela 2', 'TABELA 01', 'Tab. 1', 'Quadro 1', 'Figura 3'), or 'text'. A continuation keeps the label.", "type": "string"},
	"kind": enum("landing_results; trial_results; species_key (rule SPECIES KEYS); stratum_context = sites, coordinates, fleet lists; trial_design = diets, feeding schedules, treatment lists; context = methods, weather, water of the whole trial, collection forms; anova; comparison = other studies; figure_labeled; figure_unlabeled; text.", TABLE_KINDS),
	"caption_summary": text("The caption in our own words or quoted, at most 15 words quoted."),
	"stratum_ids": {"description": "Landings: strata with a cell in this entry, on this page. Empty for trials and for entries that give no records.", "type": "array", "items": {"type": "string", "pattern": "^s[0-9]+$"}},
	"trial_ids": {"description": "Trials whose values are in this entry. Empty for landings and for entries that give no records.", "type": "array", "items": {"type": "string", "pattern": "^t[0-9]+$"}},
	"data_cells": {"description": "Data cells in the body, counted before transcription (rule ONE RECORD PER PRINTED DATA CELL): values, totals, means, shares and statistic cells. Excludes headers, stub labels, heading rows, rank numbers, blank cells and undefined dashes. 0 for species_key, stratum_context, trial_design, context and figure_unlabeled.", "type": "integer", "minimum": 0},
	"transcribed": {"description": "Records written from this entry; must equal the records with this table_id.", "type": "integer", "minimum": 0},
	"skipped_cells": {"description": "data_cells - transcribed.", "type": "integer", "minimum": 0},
	"skipped_reason": text("Which cells were skipped and why, with counts ('CV row, 11 cells'; 'effect verdict rows, 33 cells'; 'outside extract_pages'). Null when skipped_cells = 0."),
	"species_key_pairs": {"description": "For kind species_key: the species_key[] entries taken from this entry; 0 otherwise.", "type": "integer", "minimum": 0},
	"table_level_labels": {"description": "Required for landing_results, trial_results, figure_labeled and text entries; null for the others.", "oneOf": [landing_labels, trial_labels, {"type": "null"}]},
	"columns": {"description": "One entry per printed column of an entry that gives records (rules TABLE AXES, FULL HEADERS, COLUMN ROLES); empty otherwise.", "type": "array", "items": column},
	"notes": text("Printed sideways, continues on the next page, text layer scrambled, at most 15 words quoted."),
})

stratum = obj({
	"stratum_id": {"description": "'s1' for the whole survey, then 's2', 's3' ... in the order the document presents them.", "type": "string", "pattern": "^s[0-9]+$"},
	"parent_stratum_id": {"description": "s1 for a level of an axis, or a broader stratum of the same dimension; null only for s1.", "type": ["string", "null"], "pattern": "^s[0-9]+$"},
	"stratum_dimension": enum("Rule STRATA FIRST.", STRATUM_DIMENSIONS),
	"stratum_label_as_printed": text("The label the document uses for this stratum, as printed ('Corumbá', 'R. Paraguai', 'Profissional', 'canoa rabeta S/C', 'Frigopeixe', 'Bororé'); null for s1 when it has none."),
	"landing_site_as_printed": text("Port, landing site, inspection post or entreposto as printed ('Entreposto de Pescado Antonio Castro (Barroso)', 'Barra do Rio'), at most 15 words."),
	"municipality": text("Municipality as printed, only when named as the place of this stratum ('Tefé', 'Tijucas', 'São Bernardo do Campo')."),
	"stateProvince": text("State as printed ('MS', 'Mato Grosso do Sul', 'SC', 'amazonas')."),
	"country": text("Country as printed; null when not printed."),
	"water_body_as_printed": text("River, reservoir, lake, bay or coast where the fish was caught, as printed ('Bacia do Alto Paraguai', 'Reservatório Billings', 'rios Solimões, Japurá e Jutaí', 'litoral do Piauí'); for a capture area, its own stub label ('Capivara (Paraná)'), at most 15 words."),
	"verbatimCoordinates": text("Coordinates exactly as printed, signs and hemisphere letters included; never converted."),
	"period_as_printed": text("Period of the survey or of this stratum as printed ('no ano de 2007', 'janeiro a junho de 2012', 'entre setembro de 2010 e julho de 2011', 'jan/05 a dez/07'); never normalized."),
	"fleet_or_fishery_as_printed": text("Fleet or fishery category as printed ('pesca profissional-artesanal', 'esportiva (amadora)', 'pesca artesanal profissional de pequena escala')."),
	"gear_as_printed": text("Gear as printed ('currais', 'rede de emalhe', 'cerco-flutuante'), at most 15 words."),
	"vessel_type_as_printed": text("Vessel type as printed ('canoa rabeta S/C', 'barco comprador')."),
	"data_collection_method": enum("Rule STRATUM FIELDS ONCE, WITH PAGE.", COLLECTION_METHODS, nullable=True),
	"data_collection_method_as_printed": text("The collection method as printed, at most 15 words."),
	"collected_by_as_printed": text("Who collected the data, as printed ('15º Batalhão de Polícia Militar Ambiental', 'coletores Audrin Bastos e Oscarlino Carvalho'); never the author list by default."),
	"sampling_effort_as_printed": text("Effort or coverage as printed ('83 dias de monitoramento', 'três dias consecutivos a cada dois meses', '39 pescadores profissionais'), at most 15 words."),
	"coverage_gaps_as_printed": text("Printed gaps: defeso, months without data, partial years, at most 15 words."),
	"record_origin": enum("Rule WHO RECORDED IT.", RECORD_ORIGINS),
	"field_pages": {"description": "Page of each filled field: {field name: page}. Inherited fields are not repeated, and a label read from a table stub needs no entry (rule 6).", "type": "object", "additionalProperties": {"type": "integer", "minimum": 1}},
	"source_inconsistency": text("Contradiction the document prints about this stratum, both versions and pages."),
	"notes": text("Anything else, at most 15 words quoted."),
})

trial = obj({
	"trial_id": {"description": "'t1', 't2' ... in order of first appearance.", "type": "string", "pattern": "^t[0-9]+$"},
	"trial_label": text("How the document names this trial when it has several ('recria', 'terminação', 'Experimento 1'); null when it has one."),
	"study_kind": enum("experiment = imposed treatments; production_case = one system followed without treatments; joint_analysis = means pooled across trials of the document.", ["experiment", "production_case", "joint_analysis"]),
	"pooled_from": {"description": "For joint_analysis, the trial_ids pooled; empty otherwise.", "type": "array", "items": {"type": "string", "pattern": "^t[0-9]+$"}},
	"environment": enum("Rearing unit of the whole trial.", ENVIRONMENTS),
	"location": text("Where it was run, as printed ('Pesque-Pague San Diego, Manaus, AM', 'Ceraqua-SF, Porto Real do Colégio/AL'); never the authors' address."),
	"affiliation": text("Institution that ran it, when printed with the trial; else null."),
	"period_as_printed": text("Dates or months of the trial as printed ('entre maio e julho de 2003', 'março a maio de 2010'); null when printed nowhere."),
	"species_common_as_printed": text("Common name of the cultured species as printed ('tambaqui', 'jundiá', 'tilápia do Nilo')."),
	"species_scientific_as_printed": text("Scientific name as printed in the document for this trial ('Rhamdia quelen', 'Oreochromis niloticus'); null when not printed."),
	"strain_or_origin_as_printed": text("Strain, lineage or origin of the fish as printed, when the same for the whole trial; null when it is the treatment."),
	"life_stage_as_printed": text("Life stage as printed ('juvenis', 'alevinos', 'machos revertidos')."),
	"initial_size_as_printed": text("Initial weight and length as printed ('2,47±0,05 cm e 0,24±0,01 g'), at most 15 words."),
	"rearing_unit_as_printed": text("Rearing unit and its size as printed ('tanques-rede com 1 m3', 'raceway de 2 m3 de volume útil')."),
	"stocking_density_as_printed": text("Stocking density of the whole trial as printed ('100 peixes/m3'); null when density is the treatment."),
	"feed_as_printed": text("Feed of the whole trial as printed ('ração comercial extrusada com 36% de PB'); null when the diet is the treatment."),
	"feeding_regime_as_printed": text("Ration and frequency of the whole trial as printed ('até a saciedade aparente três vezes por dia', '3% da biomassa por dia'); null when it is the treatment."),
	"duration_as_printed": text("Duration as printed ('60 dias', '160 dias')."),
	"water_system_as_printed": text("Water supply, renewal and aeration as printed, at most 15 words ('sem renovação de água, aeração mecânica')."),
	"water_context_as_printed": text("Water quality printed only for the whole trial or the water body (rule WATER QUALITY), our own words or at most 15 words quoted."),
	"uniform_management": text("Management applied the same way to every unit of a trial whose treatment is something else (rule TRIAL CONTEXT ONCE), in our own words."),
	"n_reps": integer("Replicates per treatment, only when printed ('três repetições' -> 3).", minimum=1),
	"sampled_per_unit_as_printed": text("Fish sampled per unit at each biometry as printed ('30 peixes de cada tanque-rede', '30% da população')."),
	"design_notes": text("Design in our own words ('inteiramente casualizado, fatorial 2x2, três repetições'), at most 15 words quoted."),
	"context_source_pages": {"description": "Page of each filled field: {field name: page}.", "type": "object", "additionalProperties": {"type": "integer", "minimum": 1}},
	"source_inconsistency": text("Contradiction the document prints about this trial's context, both versions and pages."),
	"notes": text("Anything else, at most 15 words quoted."),
})

species_key_entry = obj({
	"key_id": {"description": "'n1', 'n2' ... in printed order.", "type": "string", "pattern": "^n[0-9]+$"},
	"table_id": {"description": "Entry of kind species_key it was read from.", "type": "string", "pattern": "^k[0-9]+$"},
	"page": PAGE,
	"row_index": {"description": "Line of the key, from 1.", "type": "integer", "minimum": 1},
	"common_name_as_printed": text("Common name as printed on that line or the line it sits under."),
	"scientific_name_as_printed": text("Scientific name as printed, with authorship, without footnote markers."),
	"footnote_markers": {"description": "Markers printed on the names, as printed.", "type": "array", "items": {"type": "string"}},
	"notes": text("At most 15 words quoted."),
})

common_record = {
	"record_id": {"description": "'r1', 'r2' ... in reading order: table by table, block by block, row by row, left to right.", "type": "string", "pattern": "^r[0-9]+$"},
	"table_id": {"description": "tables[] entry of this record.", "type": "string", "pattern": "^k[0-9]+$"},
	"column_id": {"description": "columns[] entry of this record's cell.", "type": "string", "pattern": "^c[0-9]+$"},
	"page": {**PAGE, "description": "PDF page of the cell; the page of its table entry."},
	"table_or_figure": {"description": "Label as printed, or 'text'.", "type": "string"},
	"row_index": {"description": "Line of the cell inside its table entry and block, from 1, over data lines only (heading rows not counted, total and summary rows counted). For a transposed trial table, the variable row. The key that ties A and B together.", "type": "integer", "minimum": 1},
	"row_label_as_printed": {"description": "The stub cell of this row exactly as printed, footnote markers removed to footnote_marker ('Corumbá', 'Pintado', 'Total (ano)', 'D–50, 50 jundiás por m3', 'Peso final (g)').", "type": "string"},
	"value_kind": enum("numeric; range (a printed 'de 1 a 17', with value_min and value_max); class (a printed class or date); symbol (a defined symbol, value null); malformed (rule COPY NUMBERS EXACTLY); illegible.", VALUE_KINDS),
	"value": {"description": "The number, decimal point, thousands separator dropped. Null for range, class, symbol, malformed and illegible.", "type": ["number", "null"]},
	"value_as_printed": {"description": "The cell exactly as printed, without footnote markers, letters and dispersion term ('150.560', '28,12%', '8.14,8', '0.0', '474,08', '1 a 17').", "type": "string"},
	"value_min": {"description": "For value_kind = range: the lower number printed ('1' in 'variou de 1 a 17'); null otherwise.", "type": ["number", "null"]},
	"value_max": {"description": "For value_kind = range: the upper number printed; null otherwise.", "type": ["number", "null"]},
	"dispersion_as_printed": text("Dispersion term attached to the value, as printed ('± 54,56', '±0,03'); null if none."),
	"footnote_marker": text("Footnote or superscript marker printed on the value or the row label, as printed ('1', '2', '*', '(1)'); null if none."),
	"unit": text("Null = as the column. Filled when this row or cell prints its own unit (rule VARIABLE, UNIT, STATISTIC PER COLUMN)."),
	"statistic": enum("Null = as the column, then the table. Filled when this row differs ('Média', 'Desvio Padrão', 'Mediana', a percentage row).", STATISTICS, nullable=True),
	"source_inconsistency": text("Contradiction the document prints about this cell, both versions and pages."),
	"notes": text("Reading doubts, the decision on an ambiguous point, the quote for a text value (at most 15 words)."),
}

landing_record = obj({
	**{key: common_record[key] for key in ["record_id"]},
	"record_type": {"const": "landing", "type": "string"},
	**{key: common_record[key] for key in ["table_id", "column_id", "page", "table_or_figure"]},
	"column_block": {"description": "Block of a side-by-side layout, from 1; 1 for a single block.", "type": "integer", "minimum": 1},
	**{key: common_record[key] for key in ["row_index", "row_label_as_printed"]},
	"stratum_ids": {"description": "Rule STRATUM OF A CELL: one stratum per dimension, most specific first; ['s1'] for a whole-survey cell.", "type": "array", "minItems": 1, "items": {"type": "string", "pattern": "^s[0-9]+$"}},
	"period_as_printed": text("Rule PERIOD AS PRINTED, PER CELL; null only when the document prints no period for the cell."),
	"period_source_page": {**PAGE_OR_NULL, "description": "Page where period_as_printed was read when it is not the cell's own page (a text value that takes its paragraph's or the study's period, rule PERIOD); else null."},
	"period_context_as_printed": text("The broader period of the caption or methods when period_as_printed is narrower ('no ano de 2007'); else null."),
	"species_common_as_printed": text("Rule SPECIES AS PRINTED: common name printed on this row (or column), else null."),
	"species_scientific_as_printed": text("Rule SPECIES AS PRINTED: scientific name printed on this row or in this cell, else null. Never from a key, the text or another table."),
	"species_pairing": enum("same_row = the row prints both names in two columns; same_cell = one cell prints both; null when only one name or none is printed.", ["same_row", "same_cell"], nullable=True),
	"scientific_name_in_full_as_printed": text("Rule NAME PROBLEMS: the full name printed elsewhere in the document for an abbreviated genus, else null."),
	"scientific_name_in_full_page": {**PAGE_OR_NULL, "description": "Page of scientific_name_in_full_as_printed; null when it is null."},
	"taxon_status": enum("taxon = a species or taxon row; others_category = 'Outros', 'Outras espécies'; incomplete_in_print = the name cell holds no taxon name; not_a_taxon_row = the row is a site, month, year, fleet or total.", ["taxon", "others_category", "incomplete_in_print", "not_a_taxon_row"]),
	"family_as_printed": text("Rule RANK WORDS ARE NOT PART OF NAMES: the family printed in a heading row or column, without the rank word."),
	"higher_group_as_printed": text("Other printed headings above the row (class, order, 'Crustáceos'), without rank words, joined top-down with ' / '."),
	"variable_standardized": enum("Null = as the column. Filled for a transposed table or a row that measures something else.", LANDING_VARIABLES, nullable=True),
	"variable_as_printed": text("Null = the column header. Filled only when the cell's own row prints the variable."),
	**{key: common_record[key] for key in ["value_kind", "value", "value_min", "value_max", "value_as_printed", "dispersion_as_printed", "footnote_marker", "unit", "statistic"]},
	"is_total": {"description": "Rule TOTALS ARE RECORDS: true for a cell in a printed total row or column.", "type": "boolean"},
	"total_kind": enum("For is_total = true; null otherwise.", TOTAL_KINDS, nullable=True),
	"record_origin": enum("Null = as the table. Filled when this row differs (rule WHO RECORDED IT).", RECORD_ORIGINS, nullable=True),
	**{key: common_record[key] for key in ["source_inconsistency", "notes"]},
}, "One printed data cell of a landing or catch table, labelled figure or text value.")

trial_record = obj({
	**{key: common_record[key] for key in ["record_id"]},
	"record_type": {"const": "trial", "type": "string"},
	"trial_id": {"description": "One of its table's trial_ids.", "type": "string", "pattern": "^t[0-9]+$"},
	**{key: common_record[key] for key in ["table_id", "column_id", "page", "table_or_figure", "row_index", "row_label_as_printed"]},
	"treatment": {"description": "Rule TREATMENT AS PRINTED: the row label, or for a transposed table the column header, exactly as printed; levels joined with ' x ' for a factor on the columns.", "type": "string"},
	"treatment_code": text("Code printed in the row ('D–50', 'F–1', 'T3'); null when none."),
	"treatment_type": enum("Null = as the table, for ordinary rows only. Every special row and every record of a main-effects-only table carries its class.", TREATMENT_TYPES, nullable=True),
	"is_marginal": {"description": "true for printed marginal means (Média) and for every record of a table with main_effects_only = true.", "type": "boolean"},
	"species_common_as_printed": text("Null = as the trial. Filled when the species varies inside the trial."),
	"species_scientific_as_printed": text("Null = as the trial. Filled when the species varies inside the trial and the row prints it."),
	"strain_or_origin_as_printed": text("Null = as the trial. Filled when strain or origin is the treatment ('Tailandesa A', 'GIFT')."),
	"stocking_density_as_printed": text("Null = as the trial. Filled when density is the treatment, with the unit as printed in the stub or the header ('200 peixes/m3', '50 jundiás por m3')."),
	"feed_as_printed": text("Null = as the trial. Filled when the diet is the treatment, from the stub or the diet table."),
	"feeding_regime_as_printed": text("Null = as the trial. Filled when ration or frequency is the treatment ('alimentados uma vez ao dia')."),
	"duration_as_printed": text("Null = as the trial. Filled when this cell has its own duration."),
	"measurement_time": text("Null = as the column. Filled only when this one cell has its own time."),
	"variable_standardized": enum("Null = as the column. Filled for a transposed table (the variable is on the row) and for a row that measures something else.", TRIAL_VARIABLES, nullable=True),
	"variable_as_printed": text("Null = the column header. Filled when the variable is printed on the row (transposed table: 'Peso final (g)', 'Oxigênio dissolvido (mg/L)')."),
	**{key: common_record[key] for key in ["value_kind", "value", "value_min", "value_max", "value_as_printed", "dispersion_as_printed", "footnote_marker", "unit", "statistic"]},
	"statistic_stated": {"description": "Null = as the column, then the table. Filled together with a record-level statistic.", "type": ["boolean", "null"]},
	"significance_letter": text("Letters or asterisks printed with the value, exactly as printed; null if none."),
	"transformation_stated": text("Null = as the column, then the table."),
	**{key: common_record[key] for key in ["source_inconsistency", "notes"]},
}, "One printed data cell of an aquaculture trial table, labelled figure or text value.")


# A range record carries both ends and no single value (rule 10)
for record_definition in (landing_record, trial_record):
	record_definition["allOf"] = [{"if": {"properties": {"value_kind": {"const": "range"}}}, "then": {"properties": {"value": {"type": "null"}, "value_min": {"type": "number"}, "value_max": {"type": "number"}}}}]

field_status = lambda id_name, id_pattern, fields: {"type": "array", "items": obj({
	id_name: {"type": "string", "pattern": id_pattern},
	"field": enum("Field.", fields),
	"status": enum("filled, inherited (from the parent stratum), or not_printed after the whole document was read.", ["filled", "inherited", "not_printed"]),
	"page": {**PAGE_OR_NULL, "description": "Page where it is printed (of the parent when inherited); null when not_printed."},
})}

end_checklist = obj({
	"strata": {**field_status("stratum_id", "^s[0-9]+$", ["landing_site_as_printed", "municipality", "stateProvince", "water_body_as_printed", "period_as_printed", "fleet_or_fishery_as_printed", "gear_as_printed", "vessel_type_as_printed", "data_collection_method_as_printed", "collected_by_as_printed", "sampling_effort_as_printed", "coverage_gaps_as_printed"]), "description": "Landings: one entry per stratum and field. Empty for trials."},
	"trials": {**field_status("trial_id", "^t[0-9]+$", ["location", "period_as_printed", "species_common_as_printed", "species_scientific_as_printed", "strain_or_origin_as_printed", "life_stage_as_printed", "initial_size_as_printed", "rearing_unit_as_printed", "stocking_density_as_printed", "feed_as_printed", "feeding_regime_as_printed", "duration_as_printed", "water_system_as_printed", "n_reps"]), "description": "Trials: one entry per trial and field. Empty for landings."},
	"tables": {"description": "One entry per tables[] entry.", "type": "array", "items": obj({
		"table_id": {"type": "string", "pattern": "^k[0-9]+$"},
		"data_cells": {"type": "integer", "minimum": 0},
		"transcribed": {"type": "integer", "minimum": 0},
		"skipped_cells": {"type": "integer", "minimum": 0},
		"closes": {"description": "true only when data_cells = transcribed + skipped_cells and transcribed equals the records with this table_id.", "type": "boolean"},
	})},
	"rows": {"description": "One entry per entry that gives records and per block.", "type": "array", "items": obj({
		"table_id": {"type": "string", "pattern": "^k[0-9]+$"},
		"column_block": {"type": "integer", "minimum": 1},
		"lines_printed": {"description": "Data lines printed in the block (taxon, site, month, treatment, total and summary lines; heading rows excluded).", "type": "integer", "minimum": 0},
		"distinct_row_index_in_records": {"type": "integer", "minimum": 0},
		"lines_without_records": {"description": "row_index of lines that gave no record, with the reason ('7: every cell blank').", "type": "array", "items": {"type": "string"}},
		"rows_match": {"description": "true only when lines_printed = distinct_row_index_in_records + lines_without_records.", "type": "boolean"},
	})},
	"totals": {"description": "Landings and trials: one entry per entry that gives records.", "type": "array", "items": obj({
		"table_id": {"type": "string", "pattern": "^k[0-9]+$"},
		"printed_total_rows_and_columns": {"description": "Labels of every printed total row and column, as in table_level_labels.printed_totals.", "type": "array", "items": {"type": "string"}},
		"total_cells_printed": {"type": "integer", "minimum": 0},
		"records_with_is_total": {"type": "integer", "minimum": 0},
		"all_totals_recorded": {"description": "true only when the two counts are equal.", "type": "boolean"},
	})},
	"species": {"description": "Landings: one entry per entry that gives records and has a species axis.", "type": "array", "items": obj({
		"table_id": {"type": "string", "pattern": "^k[0-9]+$"},
		"rows_printing_scientific_name": {"type": "integer", "minimum": 0},
		"records_with_scientific_name": {"type": "integer", "minimum": 0},
		"records_with_scientific_name_from_elsewhere": {"description": "Records whose scientific name is not printed on their own row or cell. Must be 0.", "type": "integer", "minimum": 0},
		"others_category_rows": {"type": "array", "items": {"type": "string"}},
		"incomplete_in_print_rows": {"type": "array", "items": {"type": "string"}},
	})},
	"markers": {"description": "Every footnote or superscript marker taken off a number or a name.", "type": "array", "items": obj({
		"table_id": {"type": "string", "pattern": "^k[0-9]+$"},
		"marker": {"type": "string"},
		"records": {"description": "record_ids that carry it in footnote_marker.", "type": "array", "items": {"type": "string", "pattern": "^r[0-9]+$"}},
		"meaning_as_printed": text("Its footnote, at most 15 words; null when the document prints none."),
	})},
	"columns": {"description": "One entry per entry that gives records.", "type": "array", "items": obj({
		"table_id": {"type": "string", "pattern": "^k[0-9]+$"},
		"value_columns": {"type": "integer", "minimum": 0},
		"with_unit": {"type": "integer", "minimum": 0},
		"unit_from_methods_or_text": {"type": "array", "items": {"type": "string", "pattern": "^c[0-9]+$"}},
		"unit_not_printed": {"type": "array", "items": {"type": "string", "pattern": "^c[0-9]+$"}},
		"period_not_printed": {"description": "Landings: value columns whose period is printed nowhere.", "type": "array", "items": {"type": "string", "pattern": "^c[0-9]+$"}},
		"measurement_time_filled": {"description": "Trials: columns with measurement_time_status filled.", "type": "integer", "minimum": 0},
		"measurement_time_not_printed": {"type": "integer", "minimum": 0},
		"methods_searched": {"description": "true when the methods and text were read for every column's unit, period and time.", "type": "boolean"},
	})},
	"symbols": {"description": "Every distinct symbol or code in the document, with its meaning or 'undefined'.", "type": "array", "items": obj({
		"symbol": {"type": "string"},
		"table_ids": {"type": "array", "items": {"type": "string", "pattern": "^k[0-9]+$"}},
		"meaning_as_printed": {"type": "string"},
	})},
	"sums": obj({
		"tables": {"type": "integer", "minimum": 0},
		"data_cells": {"type": "integer", "minimum": 0},
		"transcribed": {"description": "Must equal records.", "type": "integer", "minimum": 0},
		"skipped_cells": {"type": "integer", "minimum": 0},
		"records": {"type": "integer", "minimum": 0},
		"species_key_entries": {"type": "integer", "minimum": 0},
		"every_table_closes": {"type": "boolean"},
	}),
})

schema = {
	"$schema": "https://json-schema.org/draft/2020-12/schema",
	"$id": "pesca/schema.json",
	"title": "Brazilian fisheries landing statistics and aquaculture trials in Portuguese-language technical literature, one record per printed data cell",
	"version": SCHEMA_VERSION,
	"description": "Fixed output format for every blind transcriber of the fisheries and aquaculture rounds of Open Tables (version 2.0, after the pilot of 8 documents). Each document gives one JSON object {doc_id, transcriber, schema_version, document_kind, strata, trials, species_key, tables, records, end_checklist}. A landings document fills strata[] (the survey, then each printed landing site, capture area, fleet, gear, vessel type or data source, with its fields and pages) and landing records: one per printed data cell, with the species as printed (common and scientific names in separate fields, never matched), the variable, unit, period and strata the cell refers to, and is_total for printed totals, which are kept and never recomputed. An aquaculture document fills trials[] (the trials block of batata/schema.json v8, rebuilt for fish culture) and trial records (treatment, species, system, stocking density, feed, duration, variable, value, unit, statistic, significance letter). Both share the inventory of every table and figure with a closed cell count, the table axes and labels declared before records, full headers, the species key, and the end-of-transcription checklist. The transcription copies what is printed and never computes, converts, infers or matches names. Carried over from the agricultural rounds and the biodiversity pilot (see changes_from_previous for what 2.0 changed from pesca-1.0-pilot): inventory first, read from the rendered page, copy exactly as printed, illegible cells stay in, contradictions with both versions, page from the PDF, 15-word limit on quotes and as-printed context, two independent transcriptions with diff and adjudication. Source PDFs and record pages are in sources.json.",
	"rules": RULES,
	"type": "object",
	"additionalProperties": False,
	"required": ["doc_id", "transcriber", "schema_version", "document_kind", "strata", "trials", "species_key", "tables", "records", "end_checklist"],
	"properties": {
		"doc_id": enum("Document id from sources.json (also the PDF file name without .pdf).", DOC_IDS) if DOC_IDS else {"description": "Document id from sources.json (also the PDF file name without .pdf).", "type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"},
		"transcriber": enum("Rule TWO INDEPENDENT TRANSCRIPTIONS.", ["A", "B", "adjudicated"]),
		"schema_version": {"description": "Version of this schema used.", "const": SCHEMA_VERSION, "type": "string"},
		"document_kind": enum("Rule TWO KINDS OF DOCUMENT; as sources.json documents[].document_kind.", ["landings", "aquaculture_trial"]),
		"strata": {"description": "Landings: one entry per stratum, s1 first (rules STRATA FIRST, STRATUM FIELDS ONCE). Empty for trials.", "type": "array", "items": {"$ref": "#/$defs/stratum"}},
		"trials": {"description": "Aquaculture: one entry per trial (rules TRIALS FIRST, TRIAL CONTEXT ONCE). Empty for landings.", "type": "array", "items": {"$ref": "#/$defs/trial"}},
		"species_key": {"description": "Rule SPECIES KEYS.", "type": "array", "items": {"$ref": "#/$defs/species_key_entry"}},
		"tables": {"description": "Rule INVENTORY FIRST, EVERY TABLE AND FIGURE, in page order.", "type": "array", "items": {"$ref": "#/$defs/table"}},
		"records": {"type": "array", "items": {"oneOf": [{"$ref": "#/$defs/landing_record"}, {"$ref": "#/$defs/trial_record"}]}},
		"end_checklist": {"$ref": "#/$defs/end_checklist"},
	},
	"$defs": {
		"stratum": stratum, "trial": trial, "species_key_entry": species_key_entry, "table": table, "column": column,
		"landing_table_labels": landing_labels, "trial_table_labels": trial_labels, "symbol": symbol,
		"landing_record": landing_record, "trial_record": trial_record, "end_checklist": end_checklist,
	},
	"changes_from_previous": CHANGES,
}

(ROOT / "schema.json").write_text(json.dumps(schema, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("schema.json written:", len(RULES), "rules,", len(DOC_IDS), "doc ids")

