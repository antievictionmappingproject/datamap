import os
from cantools.util import writejson, log, set_log, close_log, getcsv
from model import db, Building

buildings = {}
blds = []

def full_scan():
	set_log(os.path.join("logs", "txt", "buildings.txt"))
	log("Scanning BlockLot_with_LatLon.csv", important=True)
	csv = getcsv(os.path.join("scrapers", "data", "BlockLot_with_LatLon.csv"))
	winner = None
	for row in csv:
		addr = ("%s %s %s"%(row[21], row[19], row[18])).strip()
		if not addr:
			continue
		if addr not in buildings:
			buildings[addr] = 0
			building = Building.query(Building.address == addr).get()
			if not building:
				log("Can't find '%s' -- creating new entry"%(addr,), 2)
				building = Building(address=addr)
			# TODO: zipcode, year, building_id, owner
			btype = row[7].strip()
			lat = row[11].strip()
			lng = row[10].strip()
			if btype:
				building.building_type = btype
			if lat:
				building.latitude = float(lat)
			if lng:
				building.longitude = float(lng)
			blds.append(building)
		buildings[addr] += 1
		if not winner or buildings[addr] > buildings[winner]:
			winner = addr
	log("winner: %s (%s). scanned lines: %s"%(winner, buildings[winner], len(csv)), 1)
	log("writing bcounts", 1)
	writejson(buildings, os.path.join("logs", "json", "bcounts"))
	log("saving %s buildings to db"%(len(blds),), 1)
	db.put_multi(blds)
	log("goodbye")
	close_log()