# Merge the adjudicated documents into landings.csv, strata.csv, aquaculture.csv, trials.csv and qa/decisions.csv, check
# the printed totals against their parts (qa/totals_check.csv, a check only), and print the pilot numbers for RODADA.md
# Usage: python -X utf8 method/merge.py   (paths are relative to the pesca-piloto folder)
#
# Copied from batata/method/merge.py for the fisheries and aquaculture pilot (schema pesca-1.0-pilot), with the event
# inheritance of biodiversidade-piloto/method/merge.py. Changed: two kinds of document. Landing documents give strata.csv
# (one row per stratum, stratumID = doc_id#s1, a null field inherits from the nearest ancestor that prints it, written in
# `inherited`) and landings.csv; trial documents give trials.csv and aquaculture.csv, each record filled from its column,
# table and trial like the batata. A landing record with no statistic on the record or the column takes single_value, the
# landings default of the schema. Accuracy counts records, strata, trials, tables and species key entries, and names and
# numbers misread are counted apart. The self-checks and the long-copy check are the same
import ast
import csv
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "method"))
import compare  # noqa: E402  only for the compared field lists and the inheritance chains
MAX_QUOTE_WORDS = 15
LANDING_DEFAULT_STATISTIC = "single_value"

# Licence situation per document, read from sources.json (license_shown, license_scope, publisher_copyright_in_pdf)
REPOSITORY_FOOTER = "CC BY-NC-ND 4.0 (aviso geral do repositório {repo}, não é licença do item)"
LICENSE = {
	"albuquerque2010-scpesca-ms-2007-pantanal": REPOSITORY_FOOTER.format(repo="Infoteca-e") + "; o PDF imprime 'Todos os direitos reservados' (Embrapa Pantanal, p3)",
	"castro2009-producao-pesqueira-billings-sp": "nenhuma licença nem termo de uso impresso (Instituto de Pesca, página e PDF); tratado como todos os direitos reservados",
	"mamiraua2012-desembarque-tefe-am": "rodapé do site do Instituto Mamirauá: 'Todos os direitos reservados'; sem licença do item",
	"mai2010-currais-piaui": REPOSITORY_FOOTER.format(repo="Alice") + "; trabalho em anais, valem os termos do evento (não conferidos)",
	"martins2013-desembarque-tijucas-sc": "CC BY 4.0 (licença do artigo na página da Revista Biotemas)",
	"brandao2004-tambaqui-densidade-tanques-rede-am": REPOSITORY_FOOTER.format(repo="Alice") + "; artigo de periódico, valem os termos da revista (não conferidos)",
	"cartaxo2010-linhagens-tilapia-baixo-sao-francisco": REPOSITORY_FOOTER.format(repo="Alice") + "; trabalho em anais, valem os termos do evento (não conferidos)",
	"martinelli2013-jundia-densidade-frequencia-tanques-rede": REPOSITORY_FOOTER.format(repo="Alice") + "; artigo de periódico, valem os termos da revista (não conferidos)",
}

# Pairs per document in the adjudication summaries, checked against A minus the A-only records
EXPECTED_PAIRS = {"albuquerque2010-scpesca-ms-2007-pantanal": 441, "castro2009-producao-pesqueira-billings-sp": 490,
	"mamiraua2012-desembarque-tefe-am": 181, "mai2010-currais-piaui": 237, "martins2013-desembarque-tijucas-sc": 102,
	"brandao2004-tambaqui-densidade-tanques-rede-am": 72, "cartaxo2010-linhagens-tilapia-baixo-sao-francisco": 30,
	"martinelli2013-jundia-densidade-frequencia-tanques-rede": 112}
# martins2013: compare.py paired the p4 text records one row off; the adjudicator wrote these one-sided rows off as
# "Pairing artifact" and re-compared the true pairs as R001-R054. They are not omissions
ARTIFACT_EVIDENCE = "Pairing artifact"

# Stratum fields a child takes from its parent when it prints nothing of its own (rule 6 and end_checklist.strata).
# The label, dimension, coordinates, pages and notes belong to the stratum that prints them, and so does the effort: the
# survey's '4.268 guias' (albuquerque2010) is not the effort of each inspection post (biodiversity pilot, same rule)
INHERITED_STRATUM_FIELDS = ["landing_site_as_printed", "municipality", "stateProvince", "country", "water_body_as_printed",
	"period_as_printed", "fleet_or_fishery_as_printed", "gear_as_printed", "vessel_type_as_printed", "data_collection_method",
	"data_collection_method_as_printed", "collected_by_as_printed", "coverage_gaps_as_printed", "record_origin"]
# A capture area is itself the place: 'Localidade não informada' and 'OUTRAS' (mamiraua2012) must not take the survey's rivers
NOT_INHERITED_BY_DIMENSION = {"capture_area": {"water_body_as_printed"}}
# Column and table fields with no record field, copied to the record rows
LANDING_EXTRA_COLUMN = {"header_as_printed": "column_header_as_printed", "unit_source_place": "unit_source_place",
	"period_status": "column_period_status"}
LANDING_EXTRA_LABELS = {"table_period_as_printed": "table_period_as_printed", "unit_statement_as_printed": "table_unit_statement_as_printed",
	"quantity_meaning_as_printed": "table_quantity_meaning_as_printed", "source_inconsistency": "table_source_inconsistency"}
TRIAL_EXTRA_COLUMN = {"header_as_printed": "column_header_as_printed", "factor_level": "factor_level", "unit_source_place": "unit_source_place",
	"measurement_time_status": "measurement_time_status", "measurement_time_source_page": "measurement_time_source_page"}
TRIAL_EXTRA_LABELS = {"dispersion_meaning_as_printed": "dispersion_meaning_as_printed", "significance_test": "significance_test",
	"letters_meaning": "letters_meaning", "source_inconsistency": "table_source_inconsistency"}
NOT_SOURCE_TEXT = {"citation", "license", "record_id", "stratumID", "parentStratumID", "doc_id", "source_file", "decision_ids", "inherited"}

NAME_FIELDS = {"species_common_as_printed", "species_scientific_as_printed", "scientific_name_in_full_as_printed",
	"common_name_as_printed", "scientific_name_as_printed"}
NUMBER_FIELDS = {"value", "value_as_printed", "dispersion_as_printed", "significance_letter"}
ONE_SIDED_UNITS = {"stratum": "stratum", "strat": "stratum", "trial": "trial", "table": "table", "column": "column",
	"species_key_entry": "species_key"}
SUM_KINDS = ("row_total", "column_total", "grand_total", "subtotal")
SUMMARY_STATISTICS = {"mean", "median", "standard_deviation"}

# Quotes: 'x', "x", ‘x’, “x”. The single quote must not touch a letter, so "B's" is not a quote
QUOTE_PATTERN = re.compile(r"(?<![\w])'([^']{3,}?)'(?![\w])|\"([^\"]{3,}?)\"|‘([^’]+)’|“([^”]+)”")


def NormalizeWord(word):
	return re.sub(r"^[^\w]+|[^\w]+$", "", word.lower())


def LoadPdfWordShingles(pdf_path):
	# Text layer of the whole PDF, with line-break hyphens joined, as a set of 16-word sequences
	pdf_text = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf_path, "-"], capture_output=True).stdout.decode("utf-8", "replace")
	pdf_text = re.sub(r"-\s*\n\s*", "", pdf_text)
	pdf_words = [NormalizeWord(word) for word in pdf_text.split()]
	pdf_words = [word for word in pdf_words if word]
	shingle_size = MAX_QUOTE_WORDS + 1
	return {tuple(pdf_words[index:index + shingle_size]) for index in range(len(pdf_words) - shingle_size + 1)}


def CopiedRuns(text, pdf_shingles):
	# Word runs of the text found in the PDF text layer with more than MAX_QUOTE_WORDS words in a row
	words = text.split()
	normalized = [NormalizeWord(word) for word in words]
	shingle_size = MAX_QUOTE_WORDS + 1
	runs = []
	index = 0
	while index + shingle_size <= len(words):
		if tuple(normalized[index:index + shingle_size]) in pdf_shingles and "" not in normalized[index:index + shingle_size]:
			run_end = index + shingle_size
			while run_end < len(words) and tuple(normalized[run_end - shingle_size + 1:run_end + 1]) in pdf_shingles:
				run_end += 1
			runs.append(" ".join(words[index:run_end]))
			index = run_end
		else:
			index += 1
	return runs


def LongQuotes(text):
	return [quoted for quoted in (next(group for group in match.groups() if group) for match in QUOTE_PATTERN.finditer(text))
		if len(quoted.split()) > MAX_QUOTE_WORDS]


def StringLeaves(value):
	# A cell that holds a dict or list (JSON, or the Python repr the adjudicators wrote in a_value and b_value) is
	# checked string by string: the quotes around each string are syntax, not a quotation of the source
	if isinstance(value, str):
		if value[:1] in "{[":
			for parser in (json.loads, ast.literal_eval):
				try:
					return StringLeaves(parser(value))
				except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
					continue
		return [value]
	if isinstance(value, dict):
		return [leaf for each_value in value.values() for leaf in StringLeaves(each_value)]
	if isinstance(value, list):
		return [leaf for each_value in value for leaf in StringLeaves(each_value)]
	return []


def FindLongCopies(text, pdf_shingles):
	if not isinstance(text, str) or not text:
		return []
	return [copy for leaf in StringLeaves(text) for copy in CopiedRuns(leaf, pdf_shingles) + LongQuotes(leaf)]


def BuildCitation(document):
	# "(corporate author)" is our note in sources.json, not part of the name
	authors = "; ".join(author.replace(" (corporate author)", "") for author in document["authors"]).rstrip(".")
	title = document["title"].rstrip(".")
	return f"{authors}. {title}. {document['citation'].rstrip('.')}. Disponível em: {document['record_url']}"


def DecisionIds(item):
	ids = item.get("decision_ids")
	if isinstance(ids, list):
		return "; ".join(str(each_id) for each_id in ids)
	return ids or ""


def SideOfError(decision):
	# Which side a decision counts against
	if decision == "B_right":
		return ("A",)
	if decision == "A_right":
		return ("B",)
	if decision in ("both_wrong", "corrected"):
		return ("A", "B")
	return ()


def CategoryOf(row):
	# stratum, trial, species_key, column, label, record or inventory
	field, index = row["field"], row["a_index"] or row["b_index"]
	place = row["table_or_figure"]
	if place == "strata":
		return "stratum"
	if place == "trials":
		return "trial"
	if place == "species_key" or field == "species_key_entry":
		return "species_key"
	if field.startswith("columns.") or field == "column":
		return "column"
	if field.startswith("table_level_labels."):
		return "label"
	# table_id is also a record field: a record row carries the record index (r12), a table row the table id (k5)
	if field == "record" or index.lower().startswith("r"):
		return "record"
	return "inventory"


def CellText(value):
	if value is None:
		return ""
	if isinstance(value, (list, dict)):
		return json.dumps(value, ensure_ascii=False) if value else ""
	return value


def StratumRows(doc_id, strata, citation, license_text):
	strata_by_id = {stratum["stratum_id"]: stratum for stratum in strata}
	rows = []
	for stratum in strata:
		row = {"stratumID": f"{doc_id}#{stratum['stratum_id']}",
			"parentStratumID": f"{doc_id}#{stratum['parent_stratum_id']}" if stratum["parent_stratum_id"] else ""}
		for field in compare.STRATUM_FIELDS + ["notes"]:
			if field not in ("parent_stratum_id",):
				row[field] = CellText(stratum[field])
		# Null field: walk up to the first ancestor that prints it
		inherited = []
		for field in INHERITED_STRATUM_FIELDS:
			if field in NOT_INHERITED_BY_DIMENSION.get(stratum["stratum_dimension"], set()):
				continue
			ancestor = stratum
			while ancestor[field] is None and ancestor["parent_stratum_id"]:
				ancestor = strata_by_id[ancestor["parent_stratum_id"]]
			if ancestor is not stratum and ancestor[field] is not None:
				row[field] = CellText(ancestor[field])
				inherited.append(f"{field}:{ancestor['stratum_id']}")
		row["inherited"] = "; ".join(inherited)
		row["doc_id"] = doc_id
		row["origin"] = stratum.get("origin") or ""
		row["decision_ids"] = DecisionIds(stratum)
		row["citation"] = citation
		row["license"] = license_text
		rows.append(row)
	return rows


def EffectiveRecord(record, column, labels, trial):
	# Null on the record means "as the column, then the table (then the trial)": write that value and say where it came from
	chains = compare.TRIAL_INHERITED if record["record_type"] == "trial" else compare.LANDING_INHERITED
	sources = {"column": column, "labels": labels, "trial": trial or {}}
	effective = dict(record)
	inherited = []
	for field, chain in chains.items():
		if effective.get(field) is not None:
			continue
		for source, source_field in chain:
			if sources[source].get(source_field) is not None:
				effective[field] = sources[source][source_field]
				inherited.append(f"{field}:{source}")
				break
	if record["record_type"] == "landing" and effective.get("statistic") is None:
		effective["statistic"] = LANDING_DEFAULT_STATISTIC
		inherited.append("statistic:default")
	return effective, inherited


def FootnoteMeaning(record, labels):
	marker = record.get("footnote_marker")
	if not marker:
		return ""
	bare = marker.strip("()")
	for footnote in (labels.get("footnotes") or []) + (labels.get("symbols") or []):
		printed = footnote.get("marker") or footnote.get("symbol") or ""
		if printed.strip("()") == bare:
			return footnote.get("text") or footnote.get("meaning_as_printed") or ""
	return "(sem nota impressa)"


def Decimals(value_as_printed, value):
	# Decimal places as printed: after the comma, or after a point when the number is not whole
	text = (value_as_printed or "").strip().rstrip("%").strip()
	if "," in text:
		return len(re.sub(r"\D", "", text.rsplit(",", 1)[1]))
	if "." in text and value is not None and float(value) != int(float(value)):
		return len(re.sub(r"\D", "", text.rsplit(".", 1)[1]))
	return 0


def PartsOf(total, records, same_variable_only=True):
	# The printed cells a total adds up, by the position the total takes (rule TOTALS ARE RECORDS). Down a column the parts
	# share the total's variable, so a sample-size header row (martins2013 Tabela 1) never enters a catch total; across a row
	# they do not have to (albuquerque2010 Tabela 3 adds an estimated professional catch to the sport catch)
	same_table = [record for record in records if record is not total and record["table_id"] == total["table_id"] and record["page"] == total["page"]]
	kind = total["total_kind"]
	if kind == "row_total":
		return [record for record in same_table if record["column_block"] == total["column_block"] and record["row_index"] == total["row_index"]
			and not record["is_total"] and record["_column_role"] == "value" and record["statistic"] == LANDING_DEFAULT_STATISTIC]
	in_column = [record for record in same_table if record["column_id"] == total["column_id"]
		and (record["variable_standardized"] == total["variable_standardized"] or not same_variable_only)
		and record["statistic"] not in SUMMARY_STATISTICS and record.get("total_kind") not in ("column_total", "grand_total", "subtotal", "cumulative_total")]
	if kind == "grand_total":
		# Down the corner's column: the row totals when it is a total column, the plain cells otherwise
		return in_column
	if kind == "subtotal":
		# The plain cells above it, back to the previous total of the same column
		previous_totals = [record["row_index"] for record in same_table if record["column_id"] == total["column_id"] and record["is_total"]
			and record["row_index"] < total["row_index"]]
		floor = max(previous_totals, default=0)
		return [record for record in in_column if not record["is_total"] and floor < record["row_index"] < total["row_index"]]
	return [record for record in in_column if not record["is_total"]]


def SumStatus(total, parts):
	# exact, within_rounding or differs, with the sum, the difference and the rounding tolerance
	parts_sum = sum(float(part["value"]) for part in parts)
	difference = float(total["value"]) - parts_sum
	# Each printed number may be rounded by half a unit of the finest digit the total and its parts print. A whole number
	# among decimals is taken as printed without its zeros (castro2009 Tabela 2 prints 1354 among 600,5 and 954,5)
	finest_decimals = max(Decimals(record["value_as_printed"], record["value"]) for record in [total] + parts)
	tolerance = 0.5 * 10 ** -finest_decimals * (len(parts) + 1)
	if abs(difference) < 1e-6:
		status = "exact"
	elif abs(difference) <= tolerance + 1e-9:
		status = "within_rounding"
	else:
		status = "differs"
	return status, round(parts_sum, 6), round(difference, 6), round(tolerance, 6)


def TotalsCheck(doc_id, records):
	# Every printed sum (is_total, total_kind a sum) against the sum of its transcribed parts. A check, not data
	rows = []
	for total in records:
		if not total["is_total"] or total["total_kind"] not in SUM_KINDS:
			continue
		row = {"doc_id": doc_id, "record_id": total["_record_id"], "table_id": total["table_id"], "table_or_figure": total["table_or_figure"],
			"page": total["page"], "row_label_as_printed": total["row_label_as_printed"] or "", "column_header_as_printed": total["_column_header"],
			"total_kind": total["total_kind"], "variable_standardized": total["variable_standardized"], "unit": total.get("unit") or "",
			"total_as_printed": total["value_as_printed"], "n_parts": "", "parts_sum": "", "difference": "", "tolerance": "", "status": "",
			"across_sum": "", "note": "", "part_record_ids": ""}
		parts = PartsOf(total, records)
		row["n_parts"] = len(parts)
		row["part_record_ids"] = " ".join(part["_record_id"].split("#")[1] for part in parts)
		if total["table_or_figure"] == "text" and total["total_kind"] != "subtotal":
			row["status"] = "not_checkable_text"
			row["note"] = "a text total; its parts are not printed next to it"
		elif total["value"] is None:
			row["status"] = "not_checkable_total_not_numeric"
		elif not parts:
			row["status"] = "not_checkable_no_parts"
		elif any(part["value"] is None for part in parts):
			row["status"] = "not_checkable_part_not_numeric"
			row["note"] = "parts not numeric: " + ", ".join(part["value_as_printed"] for part in parts if part["value"] is None)
		else:
			row["status"], row["parts_sum"], row["difference"], row["tolerance"] = SumStatus(total, parts)
			if row["status"] == "differs" and total["total_kind"] != "row_total":
				# Does the total add up once the cells of another variable or unit in the same column are counted?
				every_part = [part for part in PartsOf(total, records, same_variable_only=False) if part["value"] is not None]
				if len(every_part) > len(parts) and SumStatus(total, every_part)[0] != "differs":
					row["note"] = "adds up only with " + ", ".join(f"{part['row_label_as_printed']} ({part['value_as_printed']} {part.get('unit') or ''})".strip()
						for part in every_part if part not in parts)
		if total["total_kind"] == "grand_total" and total["value"] is not None:
			# The corner cell also adds the column totals of its row
			across = [record for record in records if record["table_id"] == total["table_id"] and record["page"] == total["page"]
				and record["row_index"] == total["row_index"] and record["column_block"] == total["column_block"]
				and record.get("total_kind") == "column_total" and record["_column_role"] == "value" and record["value"] is not None]
			if across:
				row["across_sum"] = round(sum(float(record["value"]) for record in across), 6)
		rows.append(row)
	return rows


def main():
	schema = json.load(open(os.path.join(ROOT, "schema.json"), encoding="utf-8"))
	defs = schema["$defs"]
	sources = json.load(open(os.path.join(ROOT, "sources.json"), encoding="utf-8"))
	documents_by_id = {document["id"]: document for document in sources["documents"]}

	shingles_by_doc = {}
	stratum_rows, trial_rows, landing_rows, aquaculture_rows, totals_rows = [], [], [], [], []
	stats = defaultdict(dict)
	for adjudicated_path in sorted(glob.glob(os.path.join(ROOT, "adjudicated", "*.json"))):
		doc_id = os.path.basename(adjudicated_path)[:-5]
		document = documents_by_id[doc_id]
		shingles_by_doc[doc_id] = LoadPdfWordShingles(os.path.join(ROOT, document["pdf_path"]))
		adjudicated = json.load(open(adjudicated_path, encoding="utf-8"))
		assert adjudicated["doc_id"] == doc_id and adjudicated["document_kind"] == document["document_kind"], doc_id
		is_landings = adjudicated["document_kind"] == "landings"
		# A landings document has no trials and an aquaculture document no strata (rule TWO KINDS OF DOCUMENT)
		assert not (adjudicated["trials"] if is_landings else adjudicated["strata"]), doc_id
		citation, license_text = BuildCitation(document), LICENSE[doc_id]

		strata_by_id = {stratum["stratum_id"]: stratum for stratum in adjudicated["strata"]}
		for stratum in adjudicated["strata"]:
			assert all(field in stratum for field in defs["stratum"]["required"]), (doc_id, stratum.get("stratum_id"))
			assert stratum["parent_stratum_id"] is None or stratum["parent_stratum_id"] in strata_by_id, (doc_id, stratum["stratum_id"])
		stratum_rows += StratumRows(doc_id, adjudicated["strata"], citation, license_text)
		trials_by_id = {trial["trial_id"]: trial for trial in adjudicated["trials"]}
		for trial in adjudicated["trials"]:
			assert all(field in trial for field in defs["trial"]["required"]), (doc_id, trial.get("trial_id"))
			row = {"doc_id": doc_id}
			for field in defs["trial"]["required"]:
				row[field] = CellText(trial[field])
			row["origin"] = trial.get("origin") or ""
			row["decision_ids"] = DecisionIds(trial)
			row["citation"] = citation
			row["license"] = license_text
			trial_rows.append(row)

		tables_by_id = {table["table_id"]: table for table in adjudicated["tables"]}
		record_fields = defs["landing_record" if is_landings else "trial_record"]["required"]
		effective_records = []
		for record_number, record in enumerate(adjudicated["records"], start=1):
			# Every schema field is there, and the record points to a table, a column and its strata or trial in this document
			assert record["record_type"] == ("landing" if is_landings else "trial"), (doc_id, record_number)
			assert all(field in record for field in record_fields), (doc_id, record_number)
			assert record["table_id"] in tables_by_id, (doc_id, record_number, record["table_id"])
			table = tables_by_id[record["table_id"]]
			columns_by_id = {column["column_id"]: column for column in table.get("columns") or []}
			assert record["column_id"] in columns_by_id, (doc_id, record_number, record["table_id"], record["column_id"])
			column, labels = columns_by_id[record["column_id"]], table.get("table_level_labels") or {}
			if is_landings:
				assert record["stratum_ids"] and all(stratum_id in strata_by_id for stratum_id in record["stratum_ids"]), (doc_id, record_number)
				trial = None
			else:
				assert record["trial_id"] in trials_by_id and record["trial_id"] in table["trial_ids"], (doc_id, record_number, record["trial_id"])
				trial = trials_by_id[record["trial_id"]]
			effective, inherited = EffectiveRecord(record, column, labels, trial)
			row = {"record_id": f"{doc_id}#{record_number:04d}", "doc_id": doc_id}
			for field in record_fields:
				if field not in ("record_id", "record_type"):
					row[field] = CellText(effective[field])
			if is_landings:
				row["stratum_ids"] = "; ".join(record["stratum_ids"])
				row["stratum_labels"] = " | ".join(strata_by_id[stratum_id]["stratum_label_as_printed"] or "(estudo)" for stratum_id in record["stratum_ids"])
				extra_column, extra_labels = LANDING_EXTRA_COLUMN, LANDING_EXTRA_LABELS
			else:
				extra_column, extra_labels = TRIAL_EXTRA_COLUMN, TRIAL_EXTRA_LABELS
			for source_field, output_column in extra_column.items():
				row[output_column] = CellText(column.get(source_field))
			for source_field, output_column in extra_labels.items():
				row[output_column] = CellText(labels.get(source_field))
			row["footnote_meaning"] = FootnoteMeaning(record, labels)
			row["inherited"] = "; ".join(inherited)
			row["origin"] = record.get("origin") or ""
			row["decision_ids"] = DecisionIds(record)
			row["citation"] = citation
			row["license"] = license_text
			(landing_rows if is_landings else aquaculture_rows).append(row)
			effective.update(_record_id=row["record_id"], _column_role=column["role"], _column_header=column["header_as_printed"])
			effective_records.append(effective)
		if is_landings:
			totals_rows += TotalsCheck(doc_id, effective_records)
		stats[doc_id].update(kind=adjudicated["document_kind"], final=len(adjudicated["records"]), strata=len(adjudicated["strata"]),
			trials=len(adjudicated["trials"]), tables=len(adjudicated["tables"]), species_key=len(adjudicated["species_key"]),
			record_tables=sum(1 for table in adjudicated["tables"] if any(record["table_id"] == table["table_id"] for record in adjudicated["records"])),
			columns=sum(len(table.get("columns") or []) for table in adjudicated["tables"]),
			data_cells=sum(table["data_cells"] for table in adjudicated["tables"]),
			skipped_cells=sum(table["skipped_cells"] for table in adjudicated["tables"]))

	def WriteCsv(file_name, rows, columns=None):
		columns = columns or list(rows[0].keys())
		with open(os.path.join(ROOT, file_name), "w", encoding="utf-8", newline="") as output_file:
			writer = csv.DictWriter(output_file, fieldnames=columns)
			writer.writeheader()
			writer.writerows(rows)

	os.makedirs(os.path.join(ROOT, "qa"), exist_ok=True)
	WriteCsv("strata.csv", stratum_rows)
	WriteCsv("landings.csv", landing_rows)
	WriteCsv("trials.csv", trial_rows)
	WriteCsv("aquaculture.csv", aquaculture_rows)
	WriteCsv(os.path.join("qa", "totals_check.csv"), totals_rows)

	# Concatenate the decision files as they are, union of columns (the adjudicators wrote the label columns three ways)
	decision_rows = []
	decision_columns = ["source_file"]
	for decisions_path in sorted(glob.glob(os.path.join(ROOT, "adjudicated", "*_decisions.csv"))):
		for row in csv.DictReader(open(decisions_path, encoding="utf-8-sig", newline="")):
			row = {"source_file": "adjudicated/" + os.path.basename(decisions_path), **row}
			for key in row:
				if key not in decision_columns:
					decision_columns.append(key)
			decision_rows.append(row)
	for row in decision_rows:
		for column in decision_columns:
			row.setdefault(column, "")
	WriteCsv(os.path.join("qa", "decisions.csv"), decision_rows, decision_columns)

	# Source text copied past 15 words, or quoted past 15 words, anywhere in the output files
	long_copies = []
	for file_name, rows, key_of in (("strata.csv", stratum_rows, lambda row: row["stratumID"]),
			("trials.csv", trial_rows, lambda row: f"{row['doc_id']} {row['trial_id']}"),
			("landings.csv", landing_rows, lambda row: row["record_id"]),
			("aquaculture.csv", aquaculture_rows, lambda row: row["record_id"]),
			("qa/decisions.csv", decision_rows, lambda row: f"{row['source_file']} {row['diff_id']}")):
		for row in rows:
			for column, text in row.items():
				if column in NOT_SOURCE_TEXT:
					continue
				for copy in FindLongCopies(text, shingles_by_doc[row["doc_id"]]):
					long_copies.append((file_name, key_of(row), column, copy))
	unique_copies = sorted({(file_name, key.split("#")[0] if file_name.endswith("s.csv") and "#" in key else key, column, copy)
		for file_name, key, column, copy in long_copies})
	print(f"long copies: {len(long_copies)} cells, {len(unique_copies)} distinct")
	for copy in unique_copies:
		print("  COPY", copy)

	# Per side and per category: field errors, omissions, spurious entries, names and numbers misread
	field_errors_by_side = Counter()
	error_types = Counter()
	error_examples = {}
	misread_rows = []
	for doc_id in stats:
		a_document = json.load(open(os.path.join(ROOT, "A", doc_id + ".json"), encoding="utf-8"))
		b_document = json.load(open(os.path.join(ROOT, "B", doc_id + ".json"), encoding="utf-8"))
		doc_stats = stats[doc_id]
		doc_stats.update(a_records=len(a_document["records"]), b_records=len(b_document["records"]),
			a_tables=len(a_document["tables"]), b_tables=len(b_document["tables"]))
		counts = Counter()
		wrong = {(side, category): set() for side in "AB" for category in ("record", "stratum", "trial", "species_key", "label", "inventory", "column")}
		for row in decision_rows:
			if row["doc_id"] != doc_id:
				continue
			counts["decision_" + row["decision"]] += 1
			kind, field = row["kind"], row["field"]
			if kind.startswith("only_in") or kind == "missing_in_both":
				if row["evidence"].startswith(ARTIFACT_EVIDENCE):
					counts["artifact_rows"] += 1
					continue
				unit = ONE_SIDED_UNITS.get(field, "record")
				if kind == "missing_in_both":
					for side in ("both", "A", "B"):
						counts[f"{side}_{unit}_omitted"] += 1
					continue
				present_side = kind[-1]
				missing_side = "B" if present_side == "A" else "A"
				if row["decision"] in (present_side + "_right", "ambiguous_print"):
					counts[f"{missing_side}_{unit}_omitted"] += 1
					error_type = row[missing_side.lower() + "_error_type"] or row[present_side.lower() + "_error_type"] or f"{unit}_omitted"
					error_types[(missing_side, error_type)] += 1
					error_examples.setdefault((missing_side, error_type), f"{doc_id[:14]} {row['table_or_figure']} {field}: {row['evidence'][:120]}")
				elif row["decision"] == missing_side + "_right":
					counts[f"{present_side}_{unit}_spurious"] += 1
					error_type = row[present_side.lower() + "_error_type"] or f"{unit}_spurious"
					error_types[(present_side, error_type)] += 1
					error_examples.setdefault((present_side, error_type), f"{doc_id[:14]} {row['table_or_figure']} {field}: {row['evidence'][:120]}")
				else:
					counts[f"{present_side}_{unit}_optional"] += 1
				if unit == "record" and present_side == "A":
					counts["a_only_records"] += 1
				continue
			category = CategoryOf(row)
			for side in SideOfError(row["decision"]):
				counts[f"{side}_{category}_field_errors"] += 1
				wrong[(side, category)].add(row[side.lower() + "_index"] or row["a_index"] or row["b_index"])
				field_errors_by_side[(side, category, re.sub(r"^(columns\.[^.]+|table_level_labels)\.", "", field))] += 1
				error_type = row[side.lower() + "_error_type"] or "(sem tipo)"
				error_types[(side, error_type)] += 1
				error_examples.setdefault((side, error_type), f"{doc_id[:14]} {row['table_or_figure']} {field}: {row['evidence'][:120]}")
				if category in ("record", "species_key") and field in NAME_FIELDS:
					counts[f"{side}_name_errors"] += 1
					misread_rows.append(("name", side, row))
				if category == "record" and field in NUMBER_FIELDS:
					counts[f"{side}_number_errors"] += 1
					misread_rows.append(("number", side, row))
		doc_stats.update(counts)
		for (side, category), units in wrong.items():
			doc_stats[f"{side}_wrong_{category}"] = len(units)
		for side in "AB":
			# A table with a label, inventory or column error counts once
			doc_stats[f"{side}_wrong_table"] = len(wrong[(side, "label")] | wrong[(side, "inventory")] | wrong[(side, "column")])
		doc_stats["pairs"] = doc_stats["a_records"] - counts["a_only_records"]
		assert doc_stats["pairs"] == EXPECTED_PAIRS[doc_id], (doc_id, doc_stats["pairs"])
		doc_stats["required"] = doc_stats["pairs"] + counts["A_record_omitted"] + counts["B_record_omitted"] - counts["both_record_omitted"]

	totals = Counter()
	print("doc_id;kind;final;required;pairs;strata;trials;tables;key;A_rec;B_rec;A_wrong_rec;B_wrong_rec;A_omit;B_omit;A_spur;B_spur;"
		"A_wrong_stratum;B_wrong_stratum;A_wrong_trial;B_wrong_trial;A_wrong_table;B_wrong_table;A_tab_omit;B_tab_omit;A_key_omit;B_key_omit;"
		"A_errors;B_errors;A_names;B_names;A_numbers;B_numbers")
	for doc_id, doc_stats in sorted(stats.items()):
		for key, value in doc_stats.items():
			if isinstance(value, int):
				totals[key] += value
		a_errors = doc_stats.get("decision_B_right", 0) + doc_stats.get("decision_both_wrong", 0) + doc_stats.get("decision_corrected", 0)
		b_errors = doc_stats.get("decision_A_right", 0) + doc_stats.get("decision_both_wrong", 0) + doc_stats.get("decision_corrected", 0)
		print(f"{doc_id};{doc_stats['kind']};{doc_stats['final']};{doc_stats['required']};{doc_stats['pairs']};{doc_stats['strata']};{doc_stats['trials']};"
			f"{doc_stats['tables']};{doc_stats['species_key']};{doc_stats['a_records']};{doc_stats['b_records']};{doc_stats['A_wrong_record']};{doc_stats['B_wrong_record']};"
			f"{doc_stats.get('A_record_omitted', 0)};{doc_stats.get('B_record_omitted', 0)};{doc_stats.get('A_record_spurious', 0)};"
			f"{doc_stats.get('B_record_spurious', 0)};{doc_stats['A_wrong_stratum']};{doc_stats['B_wrong_stratum']};{doc_stats['A_wrong_trial']};"
			f"{doc_stats['B_wrong_trial']};{doc_stats['A_wrong_table']};{doc_stats['B_wrong_table']};{doc_stats.get('A_table_omitted', 0)};"
			f"{doc_stats.get('B_table_omitted', 0)};{doc_stats.get('A_species_key_omitted', 0)};{doc_stats.get('B_species_key_omitted', 0)};"
			f"{a_errors};{b_errors};{doc_stats.get('A_name_errors', 0)};{doc_stats.get('B_name_errors', 0)};"
			f"{doc_stats.get('A_number_errors', 0)};{doc_stats.get('B_number_errors', 0)}")
	print(dict(sorted(totals.items())))

	# Accuracy per record, stratum, trial, table and key entry, counting omissions, with and without the largest document
	largest_doc = max(stats, key=lambda doc_id: stats[doc_id]["required"])
	record_field_count = {"landings": len(compare.LANDING_RECORD_FIELDS), "aquaculture_trial": len(compare.TRIAL_RECORD_FIELDS)}
	compared_fields = sum(stats[doc_id]["pairs"] * record_field_count[stats[doc_id]["kind"]] for doc_id in stats)
	for side in ("A", "B"):
		for kind_name, kind_docs in (("all", list(stats)), ("landings", [d for d in stats if stats[d]["kind"] == "landings"]),
				("aquaculture", [d for d in stats if stats[d]["kind"] == "aquaculture_trial"])):
			required = sum(stats[d]["required"] for d in kind_docs)
			omitted = sum(stats[d].get(side + "_record_omitted", 0) for d in kind_docs)
			wrong_records = sum(stats[d][side + "_wrong_record"] for d in kind_docs)
			print(f"{side} records {kind_name}: right {required - omitted - wrong_records}/{required} = {100 * (required - omitted - wrong_records) / required:.1f}%"
				f" | omitted {omitted} | with error {wrong_records} | spurious {sum(stats[d].get(side + '_record_spurious', 0) for d in kind_docs)}")
		record_field_errors = totals[side + "_record_field_errors"]
		print(f"{side} record fields {record_field_errors}/{compared_fields} = {100 * record_field_errors / compared_fields:.2f}%"
			f" | names misread {totals[side + '_name_errors']} | numbers misread {totals[side + '_number_errors']}")
		largest = stats[largest_doc]
		required_rest = totals["required"] - largest["required"]
		right_rest = required_rest - (totals[side + "_record_omitted"] - largest.get(side + "_record_omitted", 0)) - (totals[side + "_wrong_record"] - largest[side + "_wrong_record"])
		print(f"{side} records without {largest_doc}: {right_rest}/{required_rest} = {100 * right_rest / required_rest:.1f}%")
		for unit, total_key, field_count in (("stratum", "strata", len(compare.STRATUM_FIELDS)), ("trial", "trials", len(compare.TRIAL_FIELDS)),
				("species_key", "species_key", len(compare.SPECIES_KEY_FIELDS))):
			unit_total = totals[total_key]
			unit_omitted = totals[f"{side}_{unit}_omitted"]
			wrong_units = totals[f"{side}_wrong_{unit}"]
			print(f"{side} {unit}: right {unit_total - unit_omitted - wrong_units}/{unit_total} = {100 * (unit_total - unit_omitted - wrong_units) / unit_total:.1f}%"
				f" | omitted {unit_omitted} | with error {wrong_units} | fields {totals[side + '_' + unit + '_field_errors']}/{(unit_total - unit_omitted) * field_count}")
		table_total = totals["tables"]
		table_omitted = totals[side + "_table_omitted"]
		wrong_tables = totals[side + "_wrong_table"]
		print(f"{side} tables: right {table_total - table_omitted - wrong_tables}/{table_total} = {100 * (table_total - table_omitted - wrong_tables) / table_total:.1f}%"
			f" | omitted {table_omitted} | spurious {totals[side + '_table_spurious']} | with error {wrong_tables}"
			f" | label fields {totals[side + '_label_field_errors']} | inventory fields {totals[side + '_inventory_field_errors']}"
			f" | column fields {totals[side + '_column_field_errors']} | columns omitted {totals[side + '_column_omitted']}")
	print("field errors by side:", sorted(field_errors_by_side.items(), key=lambda item: -item[1]))
	print("error types by side:", sorted(error_types.items(), key=lambda item: -item[1]))
	for key, example in sorted(error_examples.items()):
		print("  EXAMPLE", key, example)
	for what, side, row in misread_rows:
		print("  MISREAD", what, side, row["doc_id"][:14], row["diff_id"], row["table_or_figure"], row["field"], repr(row["a_value"])[:60], repr(row["b_value"])[:60],
			row[side.lower() + "_error_type"], "|", row["evidence"][:140])
	print("decision rows:", len(decision_rows), Counter(row["decision"] for row in decision_rows))
	print("decision rows by category:", sorted(Counter((CategoryOf(row), row["decision"]) for row in decision_rows).items()))
	print("both_acceptable fields:", Counter(row["field"] for row in decision_rows if row["decision"] == "both_acceptable").most_common(12))
	print("artifact rows (martins2013):", totals["artifact_rows"])
	print("data cells:", totals["data_cells"], "skipped cells:", totals["skipped_cells"], "record tables:", totals["record_tables"], "columns:", totals["columns"])

	# What the data hold
	for name, rows in (("landings", landing_rows), ("aquaculture", aquaculture_rows)):
		print(f"{name} origin:", Counter(row["origin"] for row in rows))
		print(f"{name} variable_standardized:", Counter(row["variable_standardized"] for row in rows).most_common())
		print(f"{name} statistic:", Counter(row["statistic"] for row in rows).most_common())
		print(f"{name} value_kind:", Counter(row["value_kind"] for row in rows).most_common())
		print(f"{name} unit:", Counter(row["unit"] for row in rows).most_common(20))
		print(f"{name} from text:", sum(1 for row in rows if row["table_or_figure"] == "text"),
			"source_inconsistency (record):", sum(1 for row in rows if row["source_inconsistency"]),
			"(record or table):", sum(1 for row in rows if row["source_inconsistency"] or row["table_source_inconsistency"]))
		print(f"{name} inherited:", Counter(entry for row in rows for entry in row["inherited"].split("; ") if entry))
		print(f"{name} empty decision_ids:", sum(1 for row in rows if not row["decision_ids"]))
	print("landings is_total:", Counter((row["is_total"], row["total_kind"]) for row in landing_rows))
	print("landings taxon_status:", Counter(row["taxon_status"] for row in landing_rows), "species_pairing:", Counter(row["species_pairing"] for row in landing_rows))
	print("landings period filled:", sum(1 for row in landing_rows if row["period_as_printed"]), "context:", sum(1 for row in landing_rows if row["period_context_as_printed"]))
	print("landings record_origin:", Counter(row["record_origin"] for row in landing_rows))
	print("distinct common names:", len({row["species_common_as_printed"] for row in landing_rows if row["species_common_as_printed"]}),
		"scientific:", len({row["species_scientific_as_printed"] for row in landing_rows if row["species_scientific_as_printed"]}))
	print("strata dimension:", Counter(row["stratum_dimension"] for row in stratum_rows), "inherited:",
		Counter(entry.split(":")[0] for row in stratum_rows for entry in row["inherited"].split("; ") if entry))
	print("aquaculture treatment_type:", Counter(row["treatment_type"] for row in aquaculture_rows), "significance letters:",
		sum(1 for row in aquaculture_rows if row["significance_letter"]), "dispersion:", sum(1 for row in aquaculture_rows if row["dispersion_as_printed"]),
		"is_marginal:", sum(1 for row in aquaculture_rows if row["is_marginal"] is True or row["is_marginal"] == "True"))
	status_counts = Counter(row["status"] for row in totals_rows)
	print("totals check:", len(totals_rows), status_counts)
	print("totals by doc and status:", sorted(Counter((row["doc_id"][:14], row["total_kind"], row["status"]) for row in totals_rows).items()))
	for row in totals_rows:
		if row["status"] not in ("exact", "within_rounding") or row["across_sum"] not in ("", row["parts_sum"]):
			print("  TOTAL", row["doc_id"][:14], row["table_or_figure"], row["record_id"].split("#")[1], row["row_label_as_printed"][:25], row["column_header_as_printed"][:25],
				row["total_kind"], row["total_as_printed"], row["parts_sum"], row["difference"], row["tolerance"], row["status"], row["n_parts"],
				"across", row["across_sum"], row["note"])

	# Self-check: every adjudicated record once, every record points to its strata or trial, and no long copy is left
	assert len(landing_rows) + len(aquaculture_rows) == sum(doc_stats["final"] for doc_stats in stats.values())
	assert len({row["record_id"] for row in landing_rows + aquaculture_rows}) == len(landing_rows) + len(aquaculture_rows)
	stratum_ids = {row["stratumID"] for row in stratum_rows}
	assert len(stratum_ids) == len(stratum_rows)
	assert all(not row["parentStratumID"] or row["parentStratumID"] in stratum_ids for row in stratum_rows)
	assert all(f"{row['doc_id']}#{stratum_id}" in stratum_ids for row in landing_rows for stratum_id in row["stratum_ids"].split("; "))
	trial_keys = {(row["doc_id"], row["trial_id"]) for row in trial_rows}
	assert len(trial_keys) == len(trial_rows)
	assert all((row["doc_id"], row["trial_id"]) in trial_keys for row in aquaculture_rows)
	assert all(row["statistic"] for row in landing_rows)
	assert len(decision_rows) == sum(sum(1 for _ in csv.DictReader(open(path, encoding="utf-8-sig"))) for path in glob.glob(os.path.join(ROOT, "adjudicated", "*_decisions.csv")))
	# Every printed sum in the landing records reaches the totals check
	assert len(totals_rows) == sum(1 for row in landing_rows if row["is_total"] is True and row["total_kind"] in SUM_KINDS)
	# A 16-word copy is caught, a 15-word copy is not, and a 16-word quote is caught even when it is not in the PDF
	test_words = [f"w{index}" for index in range(30)]
	test_shingles = {tuple(test_words[index:index + MAX_QUOTE_WORDS + 1]) for index in range(len(test_words) - MAX_QUOTE_WORDS)}
	assert CopiedRuns(" ".join(test_words[:16]) + " x", test_shingles) == [" ".join(test_words[:16])]
	assert CopiedRuns(" ".join(test_words[:15]) + " x", test_shingles) == []
	assert LongQuotes("as in '" + " ".join(["z"] * 16) + "' here") and not LongQuotes("B's and '" + " ".join(["z"] * 15) + "'")
	# A dict repr with a long string of our own words is not a quote, but a long quote inside one of its strings still is
	assert not FindLongCopies(repr({"notes": " ".join(["z"] * 16)}), set())
	assert FindLongCopies(repr({"notes": "p3 says '" + " ".join(["z"] * 16) + "'"}), set())
	# table_id on a record row (r51) is a record error, on a table row (k5) an inventory error; strata rows are strata
	table_id_row = {"field": "table_id", "table_or_figure": "Tabela 2", "kind": "wording", "a_index": "r51", "b_index": "r51"}
	assert CategoryOf(table_id_row) == "record"
	assert CategoryOf({**table_id_row, "a_index": "k5", "b_index": "k5"}) == "inventory"
	assert CategoryOf({**table_id_row, "table_or_figure": "strata", "a_index": "s2", "b_index": "s2"}) == "stratum"
	# A child stratum with no period takes its parent's and says so; coordinates never pass down
	test_strata = [{"stratum_id": "s1", "parent_stratum_id": None, **{field: None for field in compare.STRATUM_FIELDS + ["notes"]}},
		{"stratum_id": "s2", "parent_stratum_id": "s1", **{field: None for field in compare.STRATUM_FIELDS + ["notes"]}}]
	test_strata[0].update(period_as_printed="no ano de 2007", verbatimCoordinates="18°S")
	test_strata[1].update(parent_stratum_id="s1")
	test_strata[0].update(water_body_as_printed="rios Solimões, Japurá e Jutaí", sampling_effort_as_printed="4.268 guias")
	test_strata[1].update(stratum_dimension="capture_area")
	child = StratumRows("t", test_strata, "", "")[1]
	assert child["period_as_printed"] == "no ano de 2007" and child["inherited"] == "period_as_printed:s1"
	assert child["verbatimCoordinates"] == "" and child["water_body_as_printed"] == "" and child["sampling_effort_as_printed"] == ""
	# Totals: a row total adds its row's value cells, a column total its column's plain cells, a subtotal the cells above it
	def TestRecord(row_index, column_id, value, role="value", total_kind=None, statistic=LANDING_DEFAULT_STATISTIC):
		return {"_record_id": f"t#{row_index}{column_id}", "table_id": "k1", "page": 1, "column_block": 1, "row_index": row_index, "column_id": column_id,
			"variable_standardized": "catch_weight", "unit": "kg", "value": value, "value_as_printed": str(value), "is_total": total_kind is not None,
			"total_kind": total_kind, "statistic": statistic, "_column_role": role, "_column_header": column_id, "table_or_figure": "Tabela 1",
			"row_label_as_printed": str(row_index)}
	test_records = [TestRecord(1, "c2", 10), TestRecord(1, "c3", 5), TestRecord(1, "c4", 15, "total", "row_total"),
		TestRecord(2, "c2", 20), TestRecord(2, "c3", 1), TestRecord(2, "c4", 25, "total", "row_total"),
		TestRecord(3, "c2", 30, total_kind="column_total"), TestRecord(3, "c3", 6, total_kind="column_total"), TestRecord(3, "c4", 40, "total", "grand_total"),
		TestRecord(4, "c2", 15, statistic="mean")]
	test_status = {row["record_id"]: row["status"] for row in TotalsCheck("t", test_records)}
	assert test_status == {"t#1c4": "exact", "t#2c4": "differs", "t#3c2": "exact", "t#3c3": "exact", "t#3c4": "exact"}, test_status
	assert Decimals("1.166,00", 1166.0) == 2 and Decimals("150.560", 150560) == 0 and Decimals("0.30", 0.3) == 2
	assert not long_copies, f"{len(long_copies)} cells copy more than {MAX_QUOTE_WORDS} words of the source: rewrite them in adjudicated/"


if __name__ == "__main__":
	main()
