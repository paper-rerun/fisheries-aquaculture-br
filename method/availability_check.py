# Look for each chosen document's numbers in structured form: DataCite (covers Zenodo, figshare, Dryad, Redape DOIs) and Embrapa's Redape Dataverse
# Usage: py -3.12 -P availability_check.py   (writes coleta/availability/<doc_id>.json, one query at a time)
import json, time, pathlib, urllib.parse, urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "coleta" / "availability"
UA = {"User-Agent": "PaperRerun-OpenTables/0.1 (research; one request at a time)"}

# Queries per document: title words, place and species words, authors
QUERIES = {
	"albuquerque2010-scpesca-ms-2007-pantanal": ["SCPESCA", "pesca Mato Grosso do Sul Pantanal desembarque", "Bacia do Alto Paraguai pescado capturado", "Catella pesca"],
	"castro2009-producao-pesqueira-billings-sp": ["Billings produção pesqueira", "Billings reservatório pesca", "pesca profissional continental São Paulo"],
	"mamiraua2012-desembarque-tefe-am": ["desembarque pesqueiro Tefé", "Tefé fish landings", "Mamirauá pesca desembarque", "Médio Solimões pesca"],
	"mai2010-currais-piaui": ["currais de pesca Piauí", "curral fish weir Piauí", "ictiofauna currais"],
	"martins2013-desembarque-tijucas-sc": ["desembarque pesca artesanal Tijucas", "Barra do Rio Tijucas", "Tijucas artisanal fishery"],
	"brandao2004-tambaqui-densidade-tanques-rede-am": ["tambaqui densidade de estocagem tanques-rede", "Colossoma macropomum stocking density cages", "tambaqui recria"],
	"cartaxo2010-linhagens-tilapia-baixo-sao-francisco": ["linhagens tilápia Baixo São Francisco", "tilápia GIFT tailandesa desempenho", "Nile tilapia strains São Francisco"],
	"martinelli2013-jundia-densidade-frequencia-tanques-rede": ["jundiá tanques-rede densidade", "Rhamdia quelen stocking density cage", "jundiá frequência alimentar"],
}


def get_json(url):
	request = urllib.request.Request(url, headers=UA)
	with urllib.request.urlopen(request, timeout=90) as response:
		return json.loads(response.read().decode("utf-8"))


for doc_id, queries in QUERIES.items():
	result = {"doc_id": doc_id, "checked": time.strftime("%Y-%m-%d"), "datacite": [], "redape": []}
	for query in queries:
		# DataCite: every DOI-registered dataset or file, any repository
		datacite_url = "https://api.datacite.org/dois?" + urllib.parse.urlencode({"query": query, "page[size]": 10})
		try:
			data = get_json(datacite_url)
			hits = [{"doi": item["id"], "type": item["attributes"].get("types", {}).get("resourceTypeGeneral"), "title": (item["attributes"].get("titles") or [{}])[0].get("title"), "publisher": item["attributes"].get("publisher"), "year": item["attributes"].get("publicationYear")} for item in data.get("data", [])]
			result["datacite"].append({"query": query, "total": data.get("meta", {}).get("total"), "hits": hits})
		except Exception as error:
			result["datacite"].append({"query": query, "error": str(error)})
		time.sleep(2)
		# Redape: Embrapa's research data repository
		redape_url = "https://www.redape.dados.embrapa.br/api/search?" + urllib.parse.urlencode({"q": query, "per_page": 10})
		try:
			data = get_json(redape_url)["data"]
			result["redape"].append({"query": query, "total": data.get("total_count"), "hits": [{"name": item.get("name"), "type": item.get("type"), "url": item.get("url")} for item in data.get("items", [])]})
		except Exception as error:
			result["redape"].append({"query": query, "error": str(error)})
		time.sleep(2)
	(OUT / f"{doc_id}.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
	print(doc_id, [(q["query"], q.get("total")) for q in result["datacite"]], [(q["query"], q.get("total")) for q in result["redape"]])
