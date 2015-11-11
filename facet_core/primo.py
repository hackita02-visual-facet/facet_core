import requests

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
