import requests
import json
from lxml import etree

_host = 'primo.nli.org.il'
PRIMO_URL = "http://{}/PrimoWebServices/xservice/search".format(_host)


def brief_query(query,facets = None,**query_params):
    _url = "%s/brief" % PRIMO_URL

    args = {
        "institution": "NNL",
        "indx": 1,
        "bulkSize": 1,
        "json": False
    }

    args.update(dict(query_params))

    q = 'any,contains,{}'.format(query)
    args['query'] = [q]

    if facets is not None:
        facet_q = 'facet_{},exact,{}'

        for fname, fvalue in facets:
            if fname == 'creationdate':
                try:
                    year = int(fvalue)
                    fvalue = '[{}+TO+{}]'.format(year,year)
                except TypeError:
                    pass

            args['query'].append(facet_q.format(fname,fvalue))

    res = requests.get(_url, args)
    print(res.url)
    if res.ok:
        return res.content.decode()

    res.raise_for_status()


def _facets_from_json(jsn_res, query_total):
    print("Trying to parse using JSON parser")
    _s = lambda x: "sear:%s" % x

    d = json.loads(jsn_res)

    try:
        facet_list = d[_s("SEGMENTS")][_s("JAGROOT")] \
            [_s("RESULT")][_s("FACETLIST")][_s("FACET")]
    except KeyError:
        return {}

    facets = {}
    for facet_d in facet_list:
        fd = {
            kv["@KEY"]: int(kv["@VALUE"]) for kv in facet_d[_s("FACET_VALUES")]
            }

        facets[facet_d['@NAME']] = fd

    if query_total:
        try:
            total = d[_s("SEGMENTS")][_s("JAGROOT")] \
            [_s("RESULT")][_s("DOCSET")]["@TOTALHITS"]

        except KeyError:
            total = -1

        facets = {
                "total" :   int(total),
                "facets"    :   facets
            }

    return facets


def _facets_from_xml(xml_res, query_total):
    print("Trying to parse using XML parser")
    _s = lambda x: "{http://www.exlibrisgroup.com/xsd/jaguar/search}%s" % x

    x = etree.fromstring(xml_res)

    facet_list = x.find(".//%s" % _s("FACETLIST"))

    if facet_list is None:
        return {}

    facets = {}
    for facet_el in facet_list.findall(_s("FACET")):
        fd = {
            kv.get("KEY"): int(kv.get("VALUE")) for kv in facet_el.findall(_s("FACET_VALUES"))
            }

        facets[facet_el.get("NAME")] = fd

    if query_total:
        total = -1
        docset = x.find(".//%s" % _s("DOCSET"))

        if docset is not None:
            total = docset.get("TOTALHITS")

            if total is None:
                total = int(total)

        facets = {
            "total" :   total,
            "facets"    :   facets
        }

    return facets


def parse_facets(res, query_total):
    try:
        facets = _facets_from_json(res, query_total)
    except ValueError:
        try:
            facets = _facets_from_xml(res, query_total)
        except etree.XMLSyntaxError:
            raise ValueError("Invalid primo response")

    return facets


def facet_query(query, facets = None, query_total = True, **query_params):
    res = brief_query(query,facets, **query_params)

    return parse_facets(res, query_total)
