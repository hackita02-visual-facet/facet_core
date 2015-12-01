import natsort
import csv

def javascript_d3histogram(domain, values):
    script = open('histogram.html', 'r')
    script_txt = script.read()
    script_txt = script_txt.replace('values_from_facet',list_as_str(values))
    script_txt = script_txt.replace('first_year', str(domain[0]))
    script_txt = script_txt.replace('last_year', str(domain[1]))
    return script_txt


def facets2csv(facet):
    with open('facet.csv', 'w', newline='') as csvfile:
        facet_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        facet_writer.writerow(['Keys']+['Values'])
        for key in facet:
            facet_writer.writerow([str(key)]+[str(facet[key])])


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
