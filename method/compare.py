# Compare the two blind transcriptions of the fisheries and aquaculture pilot (A/*.json and B/*.json, schema
# pesca-1.0-pilot: {strata, trials, species_key, tables, records, end_checklist})
# Output: method/diff_<doc_id>.csv (or diff.csv for every doc in both folders) with strata and trial disagreements
# first, then species key, table, label and column disagreements, then every record field disagreement and every
# record present on one side only
#
# Adapted from batata/method/compare.py (trials) and biodiversidade-piloto/method/compare.py (events, tables, columns).
# What changed for this schema:
# - field lists come from schema.json ($defs required, minus ids and free text), so the script follows the schema
# - strata pair like the biodiversity events (label, dimension, parent label) and B ids are rewritten to A ids;
#   trials pair by label and by the (page, table) cells their records sit in
# - tables pair by (page, label), same kind first; columns by the (row label, value) cells they share, then header
# - landing records pair inside (table, page) by species names, row label, strata and period; trial records by
#   row label, treatment, variable and column. The value is only a tie-breaker, so a misread value still pairs
# - trial and landing records are compared on the effective value (record, column, table, trial), like the batata,
#   and a field both sides inherited is not repeated on every record
# - text copied as printed is compared exactly (spaces collapsed); other text loosely (norm)
# - the prefix column says when one side's text is the start of the other's (biodiversity lesson 2: 112 cut fields)
# - end_checklist is not compared, it is recomputed from the final records
#
# Usage: python compare.py [doc_id ...]   (paths are relative to this file); python compare.py --check runs the asserts
import csv
import difflib
import glob
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
A_DIR = os.path.join(ROOT, "A")
B_DIR = os.path.join(ROOT, "B")

with open(os.path.join(ROOT, "schema.json"), encoding="utf-8") as schema_handle:
	SCHEMA_DEFS = json.load(schema_handle)["$defs"]


def fields_of(definition, skipped):
	return [field for field in SCHEMA_DEFS[definition]["required"] if field not in skipped]


# Ids are the pairing keys; notes, caption_summary, skipped_reason and context_source_pages are free text or bookkeeping
STRATUM_FIELDS = fields_of("stratum", {"stratum_id", "notes"})
TRIAL_FIELDS = fields_of("trial", {"trial_id", "notes", "context_source_pages"})
SPECIES_KEY_FIELDS = fields_of("species_key_entry", {"key_id", "notes"})
TABLE_FIELDS = fields_of("table", {"table_id", "page", "label", "caption_summary", "skipped_reason", "table_level_labels", "columns", "notes"})
LANDING_LABEL_FIELDS = fields_of("landing_table_labels", set())
TRIAL_LABEL_FIELDS = fields_of("trial_table_labels", set())
COLUMN_FIELDS = fields_of("column", {"column_id", "notes"})
LANDING_RECORD_FIELDS = fields_of("landing_record", {"record_id", "record_type", "notes"})
TRIAL_RECORD_FIELDS = fields_of("trial_record", {"record_id", "record_type", "notes"})

# Copied as printed, so compared character by character
EXACT_FIELDS = {"value_as_printed", "row_label_as_printed", "header_as_printed", "species_common_as_printed",
	"species_scientific_as_printed", "scientific_name_in_full_as_printed", "common_name_as_printed", "scientific_name_as_printed",
	"family_as_printed", "dispersion_as_printed", "footnote_marker", "significance_letter", "treatment", "treatment_code",
	"stratum_label_as_printed", "verbatimCoordinates", "period_as_printed", "factor_level"}
VALUE_FIELDS = {"value", "value_as_printed", "value_kind"}
NAME_FIELDS = {"species_common_as_printed", "species_scientific_as_printed", "common_name_as_printed", "scientific_name_as_printed",
	"scientific_name_in_full_as_printed"}

# Record field -> where a null inherits from, in order (schema rules: record, column, table, trial)
TRIAL_INHERITED = {
	"species_common_as_printed": [("trial", "species_common_as_printed")],
	"species_scientific_as_printed": [("trial", "species_scientific_as_printed")],
	"strain_or_origin_as_printed": [("trial", "strain_or_origin_as_printed")],
	"stocking_density_as_printed": [("trial", "stocking_density_as_printed")],
	"feed_as_printed": [("trial", "feed_as_printed")],
	"feeding_regime_as_printed": [("trial", "feeding_regime_as_printed")],
	"duration_as_printed": [("trial", "duration_as_printed")],
	"measurement_time": [("column", "measurement_time")],
	"variable_standardized": [("column", "variable_standardized")],
	"variable_as_printed": [("column", "header_as_printed")],
	"unit": [("column", "unit")],
	"statistic": [("column", "statistic"), ("labels", "statistic")],
	"statistic_stated": [("labels", "statistic_stated")],
	"transformation_stated": [("labels", "transformation_stated")],
	"treatment_type": [("labels", "treatment_type")],
}
LANDING_INHERITED = {
	"variable_standardized": [("column", "variable_standardized")],
	"variable_as_printed": [("column", "header_as_printed")],
	"unit": [("column", "unit")],
	"statistic": [("column", "statistic"), ("labels", "statistic")],
	"record_origin": [("labels", "record_origin")],
}
MIN_RECORD_SCORE = 2.5


def norm(text):
	if text is None:
		return ""
	# Lists and dicts (row_identity, symbols, footnotes, field_pages) are compared as sorted JSON
	if isinstance(text, (dict, list)):
		text = json.dumps(text, sort_keys=True, ensure_ascii=False)
	text = unicodedata.normalize("NFKD", str(text))
	text = "".join(ch for ch in text if not unicodedata.combining(ch))
	text = text.lower().replace("±", " pm ")
	return re.sub(r"[^a-z0-9]+", " ", text).strip()


def exact(text):
	if text is None:
		return ""
	return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(text))).strip()


def norm_label(text):
	return re.sub(r"^(?:fig(?:ura)?|tab(?:ela)?)\b", lambda match: "figura" if match.group(0).startswith("f") else "tabela", norm(text))


def similarity(a, b):
	a, b = norm(a), norm(b)
	if a == b:
		return 1.0
	return difflib.SequenceMatcher(None, a, b).ratio()


def number_tokens(text):
	return set(re.findall(r"\d+(?:[.,]\d+)?", text or ""))


def field_differs(field, value_a, value_b):
	if isinstance(value_a, bool) or isinstance(value_b, bool) or isinstance(value_a, (int, float)) or isinstance(value_b, (int, float)):
		return value_a != value_b
	if field.split(".")[-1] in EXACT_FIELDS:
		return exact(value_a) != exact(value_b)
	return norm(value_a) != norm(value_b)


def prefix_flag(value_a, value_b):
	# One side cut short: the shorter text is the start of the longer one
	if not isinstance(value_a, str) or not isinstance(value_b, str):
		return ""
	text_a, text_b = norm(value_a), norm(value_b)
	if not text_a or not text_b or text_a == text_b:
		return ""
	if text_b.startswith(text_a):
		return "A_prefix_of_B"
	if text_a.startswith(text_b):
		return "B_prefix_of_A"
	return ""


def kind_of(field, value_a, value_b):
	field = field.split(".")[-1]
	if field in VALUE_FIELDS:
		return "value_mismatch"
	if field in NAME_FIELDS:
		return "name_mismatch"
	if value_a in (None, "", [], {}) or value_b in (None, "", [], {}):
		return "null_vs_text"
	if number_tokens(str(value_a)) != number_tokens(str(value_b)):
		return "numbers_differ"
	return "wording"


def pair_strata(strata_a, strata_b):
	# Each A stratum takes the B stratum with the same label, dimension and parent label, best scores first. Returns {B id: A id}
	labels_a = {stratum["stratum_id"]: stratum.get("stratum_label_as_printed") for stratum in strata_a}
	labels_b = {stratum["stratum_id"]: stratum.get("stratum_label_as_printed") for stratum in strata_b}
	candidates = []
	for stratum_a in strata_a:
		for stratum_b in strata_b:
			score = 3.0 * similarity(stratum_a.get("stratum_label_as_printed"), stratum_b.get("stratum_label_as_printed"))
			score += 1.0 if stratum_a.get("stratum_dimension") == stratum_b.get("stratum_dimension") else 0.0
			score += 1.0 if norm(labels_a.get(stratum_a.get("parent_stratum_id"))) == norm(labels_b.get(stratum_b.get("parent_stratum_id"))) else 0.0
			score += 0.1 if stratum_a["stratum_id"] == stratum_b["stratum_id"] else 0.0
			if score >= 3.5:
				candidates.append((score, stratum_a["stratum_id"], stratum_b["stratum_id"]))
	return greedy_ids(candidates)


def pair_trials(trials_a, trials_b, records_a, records_b):
	# One trial on each side pairs at once; otherwise by label and by the (page, table) cells their records sit in
	if len(trials_a) == 1 and len(trials_b) == 1:
		return {trials_b[0]["trial_id"]: trials_a[0]["trial_id"]}

	def footprints(trials, records):
		cells = {trial["trial_id"]: set() for trial in trials}
		for record in records:
			if record.get("trial_id") in cells:
				cells[record["trial_id"]].add((record.get("page"), norm_label(record.get("table_or_figure"))))
		return cells
	cells_a, cells_b = footprints(trials_a, records_a), footprints(trials_b, records_b)
	candidates = []
	for trial_a in trials_a:
		for trial_b in trials_b:
			footprint_a, footprint_b = cells_a[trial_a["trial_id"]], cells_b[trial_b["trial_id"]]
			overlap = len(footprint_a & footprint_b) / max(1, len(footprint_a | footprint_b))
			score = 3.0 * similarity(trial_a.get("trial_label"), trial_b.get("trial_label")) + 2.0 * overlap
			score += 0.5 if trial_a.get("study_kind") == trial_b.get("study_kind") else 0.0
			score += 0.1 if trial_a["trial_id"] == trial_b["trial_id"] else 0.0
			if score >= 2.5:
				candidates.append((score, trial_a["trial_id"], trial_b["trial_id"]))
	return greedy_ids(candidates)


def greedy_ids(candidates):
	candidates.sort(key=lambda c: (-c[0], c[1], c[2]))
	new_id_for_b, used_a = {}, set()
	for score, id_a, id_b in candidates:
		if id_a in used_a or id_b in new_id_for_b:
			continue
		used_a.add(id_a)
		new_id_for_b[id_b] = id_a
	return new_id_for_b


def mapped(new_id_for_b, old_id):
	if not old_id:
		return old_id
	return new_id_for_b.get(old_id, old_id + "?B")


def rewrite_b_ids(new_stratum_for_b, new_trial_for_b, data_b):
	for stratum in data_b["strata"]:
		stratum["stratum_id"] = mapped(new_stratum_for_b, stratum["stratum_id"])
		stratum["parent_stratum_id"] = mapped(new_stratum_for_b, stratum.get("parent_stratum_id"))
	for trial in data_b["trials"]:
		trial["trial_id"] = mapped(new_trial_for_b, trial["trial_id"])
		trial["pooled_from"] = [mapped(new_trial_for_b, trial_id) for trial_id in trial.get("pooled_from") or []]
	for table in data_b["tables"]:
		table["stratum_ids"] = [mapped(new_stratum_for_b, stratum_id) for stratum_id in table.get("stratum_ids") or []]
		table["trial_ids"] = [mapped(new_trial_for_b, trial_id) for trial_id in table.get("trial_ids") or []]
		for column in table.get("columns") or []:
			column["stratum_id"] = mapped(new_stratum_for_b, column.get("stratum_id"))
	for record in data_b["records"]:
		if "stratum_ids" in record:
			record["stratum_ids"] = [mapped(new_stratum_for_b, stratum_id) for stratum_id in record.get("stratum_ids") or []]
		if "trial_id" in record:
			record["trial_id"] = mapped(new_trial_for_b, record.get("trial_id"))


def cell_key(record):
	return (norm(record.get("row_label_as_printed")), exact(record.get("value_as_printed")))


def pair_columns(table_a, table_b, records_a, records_b):
	# Columns pair by the (row label, value) cells their records share, best overlap first, then by header
	def footprints(table, records):
		cells = {column["column_id"]: set() for column in table.get("columns") or []}
		for record in records:
			if record.get("table_id") == table["table_id"] and record.get("column_id") in cells:
				cells[record["column_id"]].add(cell_key(record))
		return cells
	cells_a, cells_b = footprints(table_a, records_a), footprints(table_b, records_b)
	headers_b = {column["column_id"]: column.get("header_as_printed") for column in table_b.get("columns") or []}
	candidates = []
	for column_a in table_a.get("columns") or []:
		for column_id_b in cells_b:
			overlap = len(cells_a[column_a["column_id"]] & cells_b[column_id_b])
			header_score = similarity(column_a.get("header_as_printed"), headers_b[column_id_b])
			candidates.append((overlap, header_score, column_a["column_id"] == column_id_b, column_a["column_id"], column_id_b))
	candidates.sort(key=lambda c: (-c[0], -c[1], not c[2], c[3], c[4]))
	pairs, used_b = {}, set()
	for overlap, header_score, bSameId, column_id_a, column_id_b in candidates:
		if column_id_a in pairs or column_id_b in used_b:
			continue
		if overlap == 0 and header_score < 0.6:
			continue
		pairs[column_id_a] = column_id_b
		used_b.add(column_id_b)
	return pairs


def pair_tables(tables_a, tables_b):
	# (page, label) first, same kind first inside it. Returns {B table_id: A table_id}
	by_key_b = {}
	for table in tables_b:
		by_key_b.setdefault((table["page"], norm_label(table["label"])), []).append(table)
	new_table_for_b = {}
	for table_a in tables_a:
		candidates = by_key_b.get((table_a["page"], norm_label(table_a["label"])), [])
		same_kind = [table for table in candidates if table["kind"] == table_a["kind"]]
		table_b = (same_kind or candidates or [None])[0]
		if table_b is None:
			continue
		candidates.remove(table_b)
		new_table_for_b[table_b["table_id"]] = table_a["table_id"]
	return new_table_for_b


def compare_tables(doc_id, data_a, data_b):
	rows = []
	tables_a, tables_b, records_a, records_b = data_a["tables"], data_b["tables"], data_a["records"], data_b["records"]
	new_table_for_b = pair_tables(tables_a, tables_b)
	tables_by_id_b = {table["table_id"]: table for table in tables_b}
	paired_b = {table_id_a: tables_by_id_b[table_id_b] for table_id_b, table_id_a in new_table_for_b.items()}
	new_column_for_b = {}
	for table_a in tables_a:
		table_b = paired_b.get(table_a["table_id"])
		if table_b is None:
			rows.append(row(doc_id, table_a["page"], table_a["label"], "only_in_A", "table", table_a["table_id"], ""))
			continue
		fields = [(field, table_a.get(field), table_b.get(field)) for field in TABLE_FIELDS]
		labels_a, labels_b = table_a.get("table_level_labels"), table_b.get("table_level_labels")
		if labels_a is None or labels_b is None:
			fields.append(("table_level_labels", labels_a, labels_b))
		else:
			label_fields = LANDING_LABEL_FIELDS if labels_a.get("labels_kind") == "landings" else TRIAL_LABEL_FIELDS
			fields += [("table_level_labels." + field, labels_a.get(field), labels_b.get(field)) for field in label_fields]
		column_pairs = pair_columns(table_a, table_b, records_a, records_b)
		columns_b = {column["column_id"]: column for column in table_b.get("columns") or []}
		for column_a in table_a.get("columns") or []:
			column_b = columns_b.pop(column_pairs.get(column_a["column_id"]), None)
			if column_b is None:
				rows.append(row(doc_id, table_a["page"], table_a["label"], "only_in_A", "column", table_a["table_id"] + "." + column_a["column_id"], ""))
				continue
			new_column_for_b[(table_b["table_id"], column_b["column_id"])] = column_a["column_id"]
			fields += [("columns.%s.%s" % (column_a["column_id"], field), column_a.get(field), column_b.get(field)) for field in COLUMN_FIELDS]
		for column_id in columns_b:
			rows.append(row(doc_id, table_a["page"], table_a["label"], "only_in_B", "column", "", table_b["table_id"] + "." + column_id))
		for field, value_a, value_b in fields:
			if field_differs(field, value_a, value_b):
				rows.append(row(doc_id, table_a["page"], table_a["label"], kind_of(field, value_a, value_b), field,
					table_a["table_id"], table_b["table_id"], value_a=value_a, value_b=value_b))
	for table_b in tables_b:
		if table_b["table_id"] not in new_table_for_b:
			rows.append(row(doc_id, table_b["page"], table_b["label"], "only_in_B", "table", "", table_b["table_id"]))
	# B records and species key entries take the A table and column ids, so they only flag a cell that really sits elsewhere
	for record in records_b:
		record["_table_id_b"] = record.get("table_id")
		key = (record.get("table_id"), record.get("column_id"))
		if key in new_column_for_b:
			record["column_id"] = new_column_for_b[key]
		record["table_id"] = new_table_for_b.get(record.get("table_id"), str(record.get("table_id")) + "?B")
	for entry in data_b["species_key"]:
		entry["table_id"] = new_table_for_b.get(entry.get("table_id"), str(entry.get("table_id")) + "?B")
	return rows


def fill_effective(data):
	# Write the inherited value into every null record field, so A and B are compared on what the record means
	trials_by_id = {trial["trial_id"]: trial for trial in data["trials"]}
	tables_by_id = {table["table_id"]: table for table in data["tables"]}
	for record in data["records"]:
		table = tables_by_id.get(record.get("table_id")) or {}
		sources = {
			"trial": trials_by_id.get(record.get("trial_id")) or {},
			"labels": table.get("table_level_labels") or {},
			"column": next((column for column in table.get("columns") or [] if column.get("column_id") == record.get("column_id")), {}),
		}
		chains = TRIAL_INHERITED if record.get("record_type") == "trial" else LANDING_INHERITED
		record["_inherited"] = set()
		for field, chain in chains.items():
			if record.get(field) is not None:
				continue
			for source, source_field in chain:
				if sources[source].get(source_field) is not None:
					record[field] = sources[source][source_field]
					record["_inherited"].add(field)
					break


def record_label(record):
	if record.get("record_type") == "landing":
		return " / ".join(str(part) for part in (record.get("row_label_as_printed"), record.get("species_common_as_printed"), record.get("period_as_printed")) if part)
	return " / ".join(str(part) for part in (record.get("row_label_as_printed"), record.get("treatment")) if part)


def record_pair_score(a, b):
	score = 3.0 * similarity(a.get("row_label_as_printed"), b.get("row_label_as_printed"))
	score += 1.0 if a.get("column_id") == b.get("column_id") else 0.0
	score += 1.0 if a.get("row_index") == b.get("row_index") else 0.0
	score += 0.5 if exact(a.get("value_as_printed")) == exact(b.get("value_as_printed")) else 0.0
	if a.get("record_type") == "landing":
		score += 2.0 * similarity(a.get("species_common_as_printed"), b.get("species_common_as_printed"))
		score += 2.0 * similarity(a.get("species_scientific_as_printed"), b.get("species_scientific_as_printed"))
		score += 1.0 if sorted(a.get("stratum_ids") or []) == sorted(b.get("stratum_ids") or []) else 0.0
		score += 1.0 if norm(a.get("period_as_printed")) == norm(b.get("period_as_printed")) else 0.0
	else:
		score += 2.0 * similarity(a.get("treatment"), b.get("treatment"))
		score += 1.0 * similarity(a.get("variable_as_printed"), b.get("variable_as_printed"))
		score += 1.0 if a.get("trial_id") == b.get("trial_id") else 0.0
	return score


def pair_records(records_a, records_b):
	# Groups by (table, page); inside a group the best scores pair first, ties keep file order
	groups = {}
	for side, records in (("a", records_a), ("b", records_b)):
		for index, record in enumerate(records):
			groups.setdefault((str(record.get("table_id")), record.get("page") or 0), {"a": [], "b": []})[side].append(index)
	pairs, only_a, only_b = [], [], []
	for key in sorted(groups):
		indexes_a, indexes_b = groups[key]["a"], groups[key]["b"]
		candidates = []
		for ia in indexes_a:
			for ib in indexes_b:
				score = record_pair_score(records_a[ia], records_b[ib])
				if score >= MIN_RECORD_SCORE:
					candidates.append((score, ia, ib))
		candidates.sort(key=lambda c: (-c[0], c[1], c[2]))
		used_a, used_b = set(), set()
		for score, ia, ib in candidates:
			if ia in used_a or ib in used_b:
				continue
			used_a.add(ia)
			used_b.add(ib)
			pairs.append((score, ia, ib))
		only_a += [ia for ia in indexes_a if ia not in used_a]
		only_b += [ib for ib in indexes_b if ib not in used_b]
	return sorted(pairs, key=lambda p: p[1]), only_a, only_b


HEADER = ["diff_id", "doc_id", "page", "table_or_figure", "kind", "field", "a_index", "b_index", "label_a", "label_b",
	"a_value", "b_value", "value_as_printed_a", "value_as_printed_b", "prefix", "match_score"]


def row(doc_id, page, table_or_figure, kind, field, a_index, b_index, label_a="", label_b="", value_a="", value_b="",
	printed_a="", printed_b="", score=""):
	def cell(value):
		if isinstance(value, (dict, list)):
			return json.dumps(value, ensure_ascii=False, sort_keys=True)
		return "" if value is None else value
	return [doc_id, page, table_or_figure, kind, field, a_index, b_index, label_a, label_b, cell(value_a), cell(value_b),
		cell(printed_a), cell(printed_b), prefix_flag(value_a, value_b), score]


def compare_blocks(doc_id, name, items_a, items_b, id_field, fields, original_b_ids):
	rows = []
	items_by_id_b = {item[id_field]: item for item in items_b}
	for item_a in items_a:
		item_b = items_by_id_b.pop(item_a[id_field], None)
		if item_b is None:
			rows.append(row(doc_id, "", name, "only_in_A", name[:-1], item_a[id_field], ""))
			continue
		for field in fields:
			if field_differs(field, item_a.get(field), item_b.get(field)):
				rows.append(row(doc_id, "", name, kind_of(field, item_a.get(field), item_b.get(field)), field,
					item_a[id_field], original_b_ids.get(item_b[id_field], item_b[id_field]), value_a=item_a.get(field), value_b=item_b.get(field)))
	for item_id in items_by_id_b:
		rows.append(row(doc_id, "", name, "only_in_B", name[:-1], "", original_b_ids.get(item_id, item_id)))
	return rows


def compare_species_key(doc_id, key_a, key_b):
	# Key entries pair by (scientific, common) name, best first
	candidates = []
	for ia, entry_a in enumerate(key_a):
		for ib, entry_b in enumerate(key_b):
			score = 2.0 * similarity(entry_a.get("scientific_name_as_printed"), entry_b.get("scientific_name_as_printed"))
			score += similarity(entry_a.get("common_name_as_printed"), entry_b.get("common_name_as_printed"))
			score += 0.5 if entry_a.get("row_index") == entry_b.get("row_index") else 0.0
			if score >= 2.0:
				candidates.append((score, ia, ib))
	candidates.sort(key=lambda c: (-c[0], c[1], c[2]))
	rows, used_a, used_b = [], set(), set()
	for score, ia, ib in candidates:
		if ia in used_a or ib in used_b:
			continue
		used_a.add(ia)
		used_b.add(ib)
		entry_a, entry_b = key_a[ia], key_b[ib]
		for field in SPECIES_KEY_FIELDS:
			if field_differs(field, entry_a.get(field), entry_b.get(field)):
				rows.append(row(doc_id, entry_a.get("page"), "species_key", kind_of(field, entry_a.get(field), entry_b.get(field)), field,
					entry_a["key_id"], entry_b["key_id"], value_a=entry_a.get(field), value_b=entry_b.get(field)))
	rows += [row(doc_id, key_a[ia].get("page"), "species_key", "only_in_A", "species_key_entry", key_a[ia]["key_id"], "") for ia in range(len(key_a)) if ia not in used_a]
	rows += [row(doc_id, key_b[ib].get("page"), "species_key", "only_in_B", "species_key_entry", "", key_b[ib]["key_id"]) for ib in range(len(key_b)) if ib not in used_b]
	return rows


def compare_document(name):
	doc_id = name[:-5]
	with open(os.path.join(A_DIR, name), encoding="utf-8") as handle:
		data_a = json.load(handle)
	with open(os.path.join(B_DIR, name), encoding="utf-8") as handle:
		data_b = json.load(handle)
	rows = []
	for field in ("document_kind", "schema_version"):
		if data_a.get(field) != data_b.get(field):
			rows.append(row(doc_id, "", "document", "wording", field, "", "", value_a=data_a.get(field), value_b=data_b.get(field)))
	# Effective values before any id is rewritten, each side with its own trials, tables and columns
	fill_effective(data_a)
	fill_effective(data_b)
	# Strata and trials first, B ids rewritten to the paired A ids
	new_stratum_for_b = pair_strata(data_a["strata"], data_b["strata"])
	new_trial_for_b = pair_trials(data_a["trials"], data_b["trials"], data_a["records"], data_b["records"])
	original_b_ids = {mapped(new_stratum_for_b, stratum["stratum_id"]): stratum["stratum_id"] for stratum in data_b["strata"]}
	original_b_ids.update({mapped(new_trial_for_b, trial["trial_id"]): trial["trial_id"] for trial in data_b["trials"]})
	rewrite_b_ids(new_stratum_for_b, new_trial_for_b, data_b)
	rows += compare_blocks(doc_id, "strata", data_a["strata"], data_b["strata"], "stratum_id", STRATUM_FIELDS, original_b_ids)
	rows += compare_blocks(doc_id, "trials", data_a["trials"], data_b["trials"], "trial_id", TRIAL_FIELDS, original_b_ids)
	# Tables second (they rewrite the B table ids), then the species key and the records
	rows += compare_tables(doc_id, data_a, data_b)
	rows += compare_species_key(doc_id, data_a["species_key"], data_b["species_key"])
	records_a, records_b = data_a["records"], data_b["records"]
	pairs, only_a, only_b = pair_records(records_a, records_b)
	for score, ia, ib in pairs:
		a, b = records_a[ia], records_b[ib]
		fields = LANDING_RECORD_FIELDS if a.get("record_type") == "landing" else TRIAL_RECORD_FIELDS
		# A field both sides inherited is already one row at its trial, table or column
		inherited_both = a["_inherited"] & b["_inherited"]
		for field in fields:
			if field in inherited_both:
				continue
			if field_differs(field, a.get(field), b.get(field)):
				rows.append(row(doc_id, a["page"], a["table_or_figure"], kind_of(field, a.get(field), b.get(field)), field,
					a["record_id"], b["record_id"], record_label(a), record_label(b), a.get(field), b.get(field),
					a.get("value_as_printed"), b.get("value_as_printed"), round(score, 2)))
	for ia in only_a:
		a = records_a[ia]
		rows.append(row(doc_id, a["page"], a["table_or_figure"], "only_in_A", "record", a["record_id"], "", record_label(a), "",
			printed_a=a.get("value_as_printed")))
	for ib in only_b:
		b = records_b[ib]
		rows.append(row(doc_id, b["page"], b["table_or_figure"], "only_in_B", "record", "", b["record_id"], "", record_label(b),
			printed_b=b.get("value_as_printed")))
	return rows, len(records_a), len(records_b), len(pairs)


def main(doc_ids):
	if doc_ids:
		names = [doc_id + ".json" for doc_id in doc_ids]
		out_path = os.path.join(HERE, "diff_%s.csv" % doc_ids[0]) if len(doc_ids) == 1 else os.path.join(HERE, "diff_selected.csv")
	else:
		names = sorted(os.path.basename(p) for p in glob.glob(os.path.join(A_DIR, "*.json")) if os.path.exists(os.path.join(B_DIR, os.path.basename(p))))
		out_path = os.path.join(HERE, "diff.csv")
	out_rows = []
	for name in names:
		rows, count_a, count_b, count_pairs = compare_document(name)
		out_rows += rows
		print("%s: A records %d, B records %d, matched pairs %d, diff rows %d" % (name[:-5], count_a, count_b, count_pairs, len(rows)))
	with open(out_path, "w", encoding="utf-8", newline="") as handle:
		writer = csv.writer(handle)
		writer.writerow(HEADER)
		for number, out_row in enumerate(out_rows, 1):
			writer.writerow(["D%04d" % number] + out_row)
	print("wrote " + out_path)


def self_check():
	assert norm_label("Tab. 1") == norm_label("Tabela 1") and norm_label("FIG. 2") == norm_label("Figura 2")
	# Printed text is exact, the rest loose; numbers and booleans exact
	assert field_differs("value_as_printed", "28,12", "28.12") and not field_differs("value_as_printed", "28,12 ", "28,12")
	assert not field_differs("location", "Ceraqua-SF.", "ceraqua sf") and field_differs("n_reps", 5, 4)
	assert field_differs("statistic_stated", True, False) and not field_differs("row_identity", {"a": 1, "b": 2}, {"b": 2, "a": 1})
	# The prefix flag names the side that was cut
	assert prefix_flag("alevinos", "alevinos de tilápia tailandesa") == "A_prefix_of_B"
	assert prefix_flag("100 peixes/m3 inicial", "100 peixes/m3") == "B_prefix_of_A" and prefix_flag("a", "a") == ""
	# Strata numbered in another order pair by label
	strata_a = [{"stratum_id": "s1", "parent_stratum_id": None, "stratum_dimension": "survey", "stratum_label_as_printed": None},
		{"stratum_id": "s2", "parent_stratum_id": "s1", "stratum_dimension": "landing_site", "stratum_label_as_printed": "Corumbá"},
		{"stratum_id": "s3", "parent_stratum_id": "s1", "stratum_dimension": "landing_site", "stratum_label_as_printed": "Coxim"}]
	strata_b = [dict(strata_a[0]), dict(strata_a[2], stratum_id="s2"), dict(strata_a[1], stratum_id="s3")]
	assert pair_strata(strata_a, strata_b) == {"s1": "s1", "s2": "s3", "s3": "s2"}
	# Two trials swapped pair by the tables their records sit in
	trials_a = [{"trial_id": "t1", "trial_label": None, "study_kind": "experiment"}, {"trial_id": "t2", "trial_label": None, "study_kind": "experiment"}]
	records_a = [{"trial_id": "t1", "page": 2, "table_or_figure": "Tabela 1"}, {"trial_id": "t2", "page": 3, "table_or_figure": "Tabela 2"}]
	records_b = [{"trial_id": "t2", "page": 2, "table_or_figure": "Tabela 1"}, {"trial_id": "t1", "page": 3, "table_or_figure": "Tab. 2"}]
	assert pair_trials(trials_a, [dict(t) for t in trials_a], records_a, records_b) == {"t2": "t1", "t1": "t2"}
	# Trial records pair by row label and column; a misread value still pairs, a different row does not take its place
	records_a = [{"record_type": "trial", "table_id": "k2", "page": 2, "column_id": "c2", "row_index": 1, "row_label_as_printed": "Peso inicial (g)",
		"treatment": "Tailandesa A", "value_as_printed": "20,92"},
		{"record_type": "trial", "table_id": "k2", "page": 2, "column_id": "c2", "row_index": 2, "row_label_as_printed": "Peso final (g)",
		"treatment": "Tailandesa A", "value_as_printed": "474,08"}]
	records_b = [dict(records_a[1]), dict(records_a[0], value_as_printed="20,82")]
	pairs, only_a, only_b = pair_records(records_a, records_b)
	assert [(ia, ib) for score, ia, ib in pairs] == [(0, 1), (1, 0)] and only_a == [] and only_b == []
	# Inherited nulls take the column, table and trial value; a written value stays
	data = {"trials": [{"trial_id": "t1", "duration_as_printed": "160 dias"}],
		"tables": [{"table_id": "k2", "table_level_labels": {"statistic": "mean"}, "columns": [{"column_id": "c2", "header_as_printed": "GIFT", "unit": None}]}],
		"records": [{"record_type": "trial", "trial_id": "t1", "table_id": "k2", "column_id": "c2", "unit": "g", "statistic": None, "duration_as_printed": None}]}
	fill_effective(data)
	record = data["records"][0]
	assert record["statistic"] == "mean" and record["duration_as_printed"] == "160 dias" and record["unit"] == "g"
	assert record["_inherited"] == {"statistic", "duration_as_printed", "variable_as_printed"}


if __name__ == "__main__":
	self_check()
	if "--check" not in sys.argv:
		main([arg for arg in sys.argv[1:] if not arg.startswith("--")])
