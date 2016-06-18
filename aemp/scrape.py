from importlib import import_module
from cantools.web import respond, succeed, fail, cgi_get

def response():
	scrape_target = cgi_get("scraper", choices=["lords", "fires", "buildings", "rent_control", "evictions", "murders"])
	import_module("scrapers.%s"%(scrape_target,)).full_scan()

respond(response, threaded=True)