from operator import itemgetter

def _top_facet_ratio(facet):
	ratios = facet.values()

	if len(ratios) < 2:
		return 0

	ratios.sort(reverse=True)

	return float(ratios[0])/ratios[1]

def max_split(facets,top=2):

	top_ratios = [(k,_top_facet_ratio(v)) for k,v in facets.items()	]
	top_ratios.sort(key=itemgetter(1),reverse=True)
	
	return top_ratios[:top] if len(top_ratios) >= top else top_ratios



