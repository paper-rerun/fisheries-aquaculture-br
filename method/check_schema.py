# Check ../schema.json: the schema is valid, a tiny transcription passes and broken ones fail. Given files, validate each
# one against the schema, ignoring the adjudication provenance (origin, decision_ids, adjudicated_on, origin_rule)
# Usage: py -3.12 -I check_schema.py [file.json ...]   (no file: self-test only; exit code 1 when a file fails)
import copy
import json
import pathlib
import site
import sys

sys.path.append(site.getusersitepackages())
import jsonschema  # noqa: E402  lives in the user site-packages

SCHEMA_PATH = pathlib.Path(__file__).resolve().parent.parent / "schema.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)
PROVENANCE_FIELDS = {"origin", "decision_ids", "adjudicated_on", "origin_rule"}


def WithoutProvenance(document):
	# The adjudicators add these at the top and on strata, trials, tables, species key entries and records
	cleaned = {key: value for key, value in document.items() if key not in PROVENANCE_FIELDS}
	for block in ("strata", "trials", "species_key", "tables", "records"):
		if isinstance(cleaned.get(block), list):
			cleaned[block] = [{key: value for key, value in item.items() if key not in PROVENANCE_FIELDS} if isinstance(item, dict) else item
				for item in cleaned[block]]
	return cleaned


def Errors(document):
	return ["%s: %s" % ("/".join(str(part) for part in error.absolute_path), error.message[:200]) for error in VALIDATOR.iter_errors(document)]


def TinyLandingDocument():
	doc_id = (SCHEMA["properties"]["doc_id"].get("enum") or ["exemplo2026-teste"])[0]
	empty_checklist = {"strata": [], "trials": [], "tables": [], "rows": [], "totals": [], "species": [], "markers": [], "columns": [], "symbols": [],
		"sums": {"tables": 1, "data_cells": 1, "transcribed": 1, "skipped_cells": 0, "records": 1, "species_key_entries": 0, "every_table_closes": True}}
	column = {"column_id": "c2", "column_block": 1, "header_as_printed": "Mar.", "role": "value", "variable_standardized": "catch_weight", "unit": "kg",
		"unit_source_place": "caption", "statistic": None, "is_total_column": False, "period_as_printed": "Mar.", "period_status": "filled", "stratum_id": None,
		"factor_level": None, "measurement_time": None, "measurement_time_refers_to": None, "measurement_time_source_page": None,
		"measurement_time_source_place": None, "measurement_time_status": "not_applicable", "notes": None}
	labels = {"labels_kind": "landings", "row_axis": "species", "row_axis_as_printed": "Espécie", "column_axis": "periods", "layout": "single_block",
		"table_period_as_printed": "no ano de 2007", "table_period_place": "caption", "unit_statement_as_printed": "(kg)", "quantity_meaning_as_printed": None,
		"printed_totals": [{"label_as_printed": "Total", "axis": "row", "kind": "column_total", "cells": 9}], "heading_levels": [], "symbols": [], "footnotes": [],
		"record_origin": "monitoring_programme", "source_inconsistency": None}
	stratum = {"stratum_id": "s1", "parent_stratum_id": None, "stratum_dimension": "study", "stratum_label_as_printed": None, "landing_site_as_printed": None,
		"municipality": None, "stateProvince": "MS", "country": None, "water_body_as_printed": "Bacia do Alto Paraguai", "verbatimCoordinates": None,
		"period_as_printed": "no ano de 2007", "fleet_or_fishery_as_printed": None, "gear_as_printed": None, "vessel_type_as_printed": None,
		"data_collection_method": "inspection_records", "data_collection_method_as_printed": "Guia de Controle de Pescado", "collected_by_as_printed": None,
		"sampling_effort_as_printed": None, "coverage_gaps_as_printed": None, "record_origin": "monitoring_programme", "field_pages": {"water_body_as_printed": 9},
		"source_inconsistency": None, "notes": None}
	record = {"record_id": "r1", "record_type": "landing", "table_id": "k1", "column_id": "c2", "page": 26, "table_or_figure": "Tabela 8", "column_block": 1,
		"row_index": 1, "row_label_as_printed": "Pintado", "stratum_ids": ["s1"], "period_as_printed": "Mar.", "period_source_page": None,
		"period_context_as_printed": "no ano de 2007", "species_common_as_printed": "Pintado", "species_scientific_as_printed": None, "species_pairing": None,
		"scientific_name_in_full_as_printed": None, "scientific_name_in_full_page": None, "taxon_status": "taxon", "family_as_printed": None,
		"higher_group_as_printed": None, "variable_standardized": None, "variable_as_printed": None, "value_kind": "numeric", "value": 6756.4,
		"value_min": None, "value_max": None, "value_as_printed": "6.756,4", "dispersion_as_printed": None, "footnote_marker": None, "unit": None,
		"statistic": None, "is_total": False, "total_kind": None, "record_origin": None, "source_inconsistency": None, "notes": None}
	table = {"table_id": "k1", "page": 26, "label": "Tabela 8", "kind": "landing_results", "caption_summary": None, "stratum_ids": ["s1"], "trial_ids": [],
		"data_cells": 1, "transcribed": 1, "skipped_cells": 0, "skipped_reason": None, "species_key_pairs": 0, "table_level_labels": labels, "columns": [column],
		"notes": None}
	return {"doc_id": doc_id, "transcriber": "A", "schema_version": SCHEMA["version"], "document_kind": "landings", "strata": [stratum], "trials": [],
		"species_key": [], "tables": [table], "records": [record], "end_checklist": empty_checklist}


def SelfTest():
	jsonschema.Draft202012Validator.check_schema(SCHEMA)
	document = TinyLandingDocument()
	assert not Errors(document), Errors(document)[:3]
	# Provenance is ignored, but only after it is taken off
	with_provenance = copy.deepcopy(document)
	with_provenance.update(adjudicated_on="2026-11-01", origin_rule="test")
	with_provenance["records"][0].update(origin="both", decision_ids=["D0001"])
	assert Errors(with_provenance) and not Errors(WithoutProvenance(with_provenance))
	# A range is one record with both ends and no single value
	range_document = copy.deepcopy(document)
	range_document["records"][0].update(value_kind="range", value=None, value_min=1, value_max=17, value_as_printed="1 a 17")
	assert not Errors(range_document), Errors(range_document)[:3]
	broken_documents = {
		"record_type trial on a landing record": ("record_type", "trial"),
		"value written as text": ("value", "6.756,4"),
		"range without its upper end": ("value_kind", "range"),
		"missing value_min (a 1.0 record)": ("value_min", KeyError),
	}
	for reason, (field, new_value) in broken_documents.items():
		broken = copy.deepcopy(range_document if field == "value_kind" else document)
		if field == "value_kind":
			broken["records"][0]["value_max"] = None
		elif new_value is KeyError:
			del broken["records"][0][field]
		else:
			broken["records"][0][field] = new_value
		assert Errors(broken), reason + " was accepted"
	# The pilot's version string fails: a 1.0 file is not a 2.0 file
	old_version = dict(document, schema_version="pesca-1.0-pilot")
	assert Errors(old_version)
	print("self-test ok: schema %s valid, tiny transcription passes, %d broken ones fail" % (SCHEMA["version"], len(broken_documents) + 1))


if __name__ == "__main__":
	SelfTest()
	failed = 0
	for path in sys.argv[1:]:
		errors = Errors(WithoutProvenance(json.loads(pathlib.Path(path).read_text(encoding="utf-8"))))
		print("%s: %s" % (path, "ok" if not errors else "%d errors" % len(errors)))
		for error in errors[:20]:
			print("  " + error)
		failed += bool(errors)
	sys.exit(1 if failed else 0)
