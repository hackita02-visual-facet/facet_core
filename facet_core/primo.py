import requests
import json
from lxml import etree

PRIMO_URL = "http://primo.nli.org.il/PrimoWebServices/xservice/search"

def brief_query(query,json = False,**query_params):

	_url = "%s/brief"%PRIMO_URL

	q = 'any,contains,{}'.format(query)

	args = {
		"institution"	:	"NNL",
		"indx"	:	1,
		"bulkSize"	:	1,
	}

	args.update(dict(query_params))
	args['query'] = q

	if json:
		args['json'] = True

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
		return []

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

