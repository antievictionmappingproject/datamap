import os
from cantools.util import read, writejson, log, set_log, close_log
from model import db, Building

def full_scan():
	set_log(os.path.join("logs", "txt", "rent_control.txt"))
	log("Scanning rent_control.geojson", important=True)
	rcd = read(os.path.join("scrapers", "data",
		"rent_control.geojson"), isjson=True)["features"]
	rcp = [rc["properties"] for rc in rcd if rc["properties"]["address"]]
	log("using %s of %s rows (omitting blank entries)"%(len(rcp), len(rcd)), 1)

	blds = []
	bset = set()
	for d in rcp:
		addr = d["address"]
		if addr not in bset:
			building = Building.query(Building.address == addr).get()
			if not building:
				log("Can't find '%s' -- creating new entry"%(addr,), 2)
				building = Building(address=addr)
			building.rent_control = True
			blds.append(building)
			bset.add(addr)

	log("saving %s rent-control buildings to db"%(len(blds),), 1)
	db.put_multi(blds)
	log("goodbye")
	close_log()