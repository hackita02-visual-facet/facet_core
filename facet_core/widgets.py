import natsort


def javascript_d3histogram(domain, values):
    script = open('histogram.html', 'r')
    script_txt = script.read()
    script_txt = script_txt.replace('values_from_facet',list_as_str(values))
    script_txt = script_txt.replace('first_year', str(domain[0]))
    script_txt = script_txt.replace('last_year', str(domain[1]))
    return script_txt


def sort_facet_by_key(facet):
    facet_tuple = [(key, facet[key]) for key in facet.keys()]

    def get_key(item):
        return item[0]

    return natsort.natsorted(facet_tuple, key=get_key)


def list_as_str(my_list):
    output_str = '['
    for x in my_list:
        output_str += str(x)
        output_str += ','
    print(output_str[:-1])
    print(output_str[:-1] + ']')
    return output_str[:-1] + ']'


def histogram_javascript_from_facet(facet):
    ordered_by_key = sort_facet_by_key(facet)
    domain = [ordered_by_key[0], ordered_by_key[-1]]
    values = [value[1] for value in ordered_by_key]
    return javascript_d3histogram(domain,values)

import requests
import json
from lxml import etree

PRIMO_URL = "http://primo.nli.org.il/PrimoWebServices/xservice/search"


def brief_query(query, **query_params):
    _url = "%s/brief" % PRIMO_URL

    q = 'any,contains,{}'.format(query)

    args = {
        "institution": "NNL",
        "indx": 1,
        "bulkSize": 1,
        "json": False
    }

    args.update(dict(query_params))
    args['query'] = q

    res = requests.get(_url, args)

    if res.ok:
        return res.content.decode()

    res.raise_for_status()


def _facets_from_json(jsn_res):
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

    return facets


def _facets_from_xml(xml_res):
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

    return facets


def parse_facets(res):
    try:
        facets = _facets_from_json(res)
    except ValueError:
        try:
            facets = _facets_from_xml(res)
        except etree.XMLSyntaxError:
            raise ValueError("Invalid primo response")

    return facets


def facet_query(query, **query_params):
    res = brief_query(query, **query_params)

    return parse_facets(res)


facets = facet_query('Ben')
facet = facets['creationdate']
s = histogram_javascript_from_facet(facet)
ab = open('ab.html','w')
ab.write(s)