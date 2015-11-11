from operator import itemgetter

def _top_facet_ratio(facet):
	ratios = list(facet.values())

	if len(ratios) < 2:
		return 0

	ratios.sort(reverse=True)

	return float(ratios[0])/ratios[1]

def max_split(facets,top=None):

	top_ratios = [(k,_top_facet_ratio(v)) for k,v in facets.items()	]
	top_ratios.sort(key=itemgetter(1),reverse=True)
	
	if top is not None and len(top_ratios) >= top:
		return top_ratios[:top]
	else:
		return top_ratios


