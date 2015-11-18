from operator import itemgetter


def _top_facet_ratio(facet):
    ratios = list(facet.values())

    if len(ratios) < 2:
        return 0

    ratios.sort(reverse=True)

    return float(ratios[0]) / ratios[1]


def max_split(facets, top=None):
    top_ratios = [(k, _top_facet_ratio(v)) for k, v in facets.items()]
    top_ratios.sort(key=itemgetter(1), reverse=True)

    if top is not None and len(top_ratios) >= top:
        return top_ratios[:top]
    else:
        return top_ratios


def sort_by_max_result(facets):
    facet_names = facets.keys()
    facet_res = []

    for key, name in zip(facets, facet_names):
        facet_res.append((name, sum(facets[key].values())))

    def getkey(item):
        return item[1]

    return sorted(facet_res, key=getkey, reverse=True)  # sort facets by number of results


def sort_values_by_name(facets, facet2sort):
    return sorted(facets[facet2sort].keys())
