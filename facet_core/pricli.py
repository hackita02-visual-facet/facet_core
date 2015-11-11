import json

import click
import requests

import primo

@click.group()
def cli():
	pass

@cli.command()
@click.argument('query')
@click.option('--query-param','-qa','query_params',nargs=2,multiple=True)
@click.option('--json','-j','use_json',is_flag=True)
@click.option('--facets','-f',is_flag=True)
@click.option('--post','-p','post_to')
@click.option('--post-header','-ph','post_headers',nargs=2,multiple=True)
def brief(query,query_params,use_json,facets,post_to,post_headers):
			
	qps = dict(query_params)
	if use_json:
		qps['json'] = True

	res = primo.brief_query(query,**qps)

	if facets:
		res = json.dumps(primo.parse_facets(res))

	click.echo(res)

	if post_to:

		headers = {
			"Content-Type"	:	"application/json" if use_json else "text/xml"
		}

		headers.update(dict(post_headers))

		if "http" not in post_to:
			post_to = "http://" + post_to

		requests.post(post_to,headers=headers,data=res)


if __name__ == "__main__":
	cli()



