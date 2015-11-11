import requests
import json
from lxml import etree

PRIMO_URL = "http://primo.nli.org.il/PrimoWebServices/xservice/search"

def brief_query(query,**query_params):

	_url = "%s/brief"%PRIMO_URL

	q = 'any,contains,{}'.format(query)

	args = {
		"institution"	:	"NNL",
		"indx"	:	1,
		"bulkSize"	:	1,
		"json"	:	False
	}

	args.update(dict(query_params))
	args['query'] = q


	res = requests.get(_url,args)

	if res.ok:
		return res.content

	res.raise_for_status()


def _facets_from_json(jsn_res):

	_s = lambda x: "sear:%s"%x

	d = json.loads(jsn_res)

	try:
		facet_list = d[_s("SEGMENTS")][_s("JAGROOT")]\
		[_s("RESULT")][_s("FACETLIST")][_s("FACET")]
	except KeyError:
		return {}

	facets = {}
	for facet_d in facet_list:
		fd = {
			"count"	:	int(facet_d['@COUNT']),
			"values"	:	{}
		}

		for kv in facet_d[_s("FACET_VALUES")]:
			fd["values"][kv["@KEY"]] = int(kv["@VALUE"])

		facets[facet_d['@NAME']] = fd

	return facets

def _facets_from_xml(xml_res):

	_s = lambda x: "{http://www.exlibrisgroup.com/xsd/jaguar/search}%s"%x

	x = etree.fromstring(xml_res)

	facet_list = x.find(".//%s"%_s("FACETLIST"))

	if facet_list is None:
		return {}

	facets = {}
	for facet_el in facet_list.findall(_s("FACET")):
		fd = {
			"count"	:	int(facet_el.get('COUNT')),
			"values"	:	{}
		}

		for kv in facet_el.findall(_s("FACET_VALUES")):
			fd["values"][kv.get("KEY")] = int(kv.get("VALUE"))

		facets[facet_el.get("NAME")] = fd

	return facets

def parse_facets(res):

	try:
		facets = _facets_from_json(res)
	except ValueError:
		try:
			facets = _facets_from_xml(res)
		except etree.XMLSyntaxError:
			raies("Invlalid primo response")

	return facets 

def facet_query(query,**query_params):

	res = brief_query(query,**query_params)

	return parse_facets(res)
