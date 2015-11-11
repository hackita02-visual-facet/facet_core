import click
import requests

import primo

@click.group()
def cli():
	pass

@cli.command()
@click.argument('query')
@click.option('--query-param','-qa','query_params',nargs=2,multiple=True)
@click.option('--json/--xml',default=False)
@click.option('--post','-p','post_to')
@click.option('--post-header','-ph','post_headers',nargs=2,multiple=True)
def brief(query,query_params,json,post_to,post_headers):
	
	res = primo.brief_query(query,json,**dict(query_params))
	click.echo(res)

	if post_to:

		headers = {
			"Content-Type"	:	"application/json" if json else "text/xml"
		}

		headers.update(dict(post_headers))

		if "http" not in post_to:
			post_to = "http://" + post_to

		requests.post(post_to,headers=headers,data=res)


if __name__ == "__main__":
	cli()



