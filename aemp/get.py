from cantools.web import respond, succeed, cgi_get
from cantools.db import get_page

def response():
	import model # load up all models
	succeed(get_page(cgi_get("model"), cgi_get("limit", default=20), cgi_get("offset", default=0)))

respond(response)