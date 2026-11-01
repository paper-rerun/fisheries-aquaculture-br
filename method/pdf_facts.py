# Facts about each chosen PDF for sources.json: pages, sha256, bytes, text per page, encryption, rights lines and table captions
# Usage: py -3.12 -P pdf_facts.py ../pdfs/*.pdf > ../coleta/pdf_facts.json
import sys, re, json, hashlib, pathlib, fitz

facts = {}
for path in sys.argv[1:]:
	data = pathlib.Path(path).read_bytes()
	doc = fitz.open(path)
	texts = [page.get_text() for page in doc]
	rights = []
	captions = []
	for number, text in enumerate(texts, 1):
		flat = re.sub(r"\s+", " ", text)
		# Rights notices printed in the PDF
		for match in re.finditer(r".{0,60}(direitos reservados|©|copyright|Creative Commons|CC BY|reprodução n[ãa]o.autorizada|permitida a reprodução).{0,80}", flat, re.I):
			rights.append({"page": number, "text": match.group(0).strip()})
		# Table and figure captions
		for line in text.splitlines():
			stripped = line.strip()
			if re.match(r"(Tab\.|Tabela|TABELA|Quadro|QUADRO|Figura|FIGURA|Fig\.|Anexo|ANEXO)\s*[0-9IVX]", stripped):
				captions.append({"page": number, "caption": stripped[:120]})
	facts[pathlib.Path(path).stem] = {
		"pdf_sha256": hashlib.sha256(data).hexdigest(), "pdf_bytes": len(data), "pages": len(doc),
		"text_layer_chars_per_page": sum(len(t) for t in texts) // max(1, len(doc)),
		"pages_without_text": [i for i, t in enumerate(texts, 1) if len(t.strip()) < 50],
		"encrypted": doc.metadata.get("encryption"), "rights_lines": rights, "captions": captions,
	}
print(json.dumps(facts, ensure_ascii=False, indent=1))
