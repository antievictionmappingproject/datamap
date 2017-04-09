import os
from cantools.db import dprep
from cantools.util import read, log, set_log, close_log
from model import db, PoliceMurder

def fixup(d):
	log(d)
	obj = {}
	if d.get("geometry", None):
		obj["longitude"], obj["latitude"] = d["geometry"]["coordinates"]
	d = d["properties"]
	for key, ptype in PoliceMurder._schema.items():
		if key in d:
			obj[key] = d[key]
	name, age = "", ""
	for c in obj["name"]:
		if c.isdigit():
			age += c
		else:
			name += c
	if age:
		obj["name"] = name.strip(" ,()\n")
		obj["age"] = int(age)
	return dprep(obj, PoliceMurder._schema)

def full_scan():
	set_log(os.path.join("logs", "txt", "police_murders.txt"))
	log("Scanning police_murders.geojson", important=True)
	data = read(os.path.join("scrapers", "data", "police_murders.geojson"), isjson=True)["features"]
	log("got %s murders"%(len(data),))
	mods = [PoliceMurder(**fixup(d)) for d in data]
	log("saving")
	db.put_multi(mods)
	log("goodbye")
	close_log()