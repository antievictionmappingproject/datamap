import os, json
from cantools.util import write, writejson, error, log, set_log, close_log, getcsv
from cantools.geo import address2latlng, addr2zip
from model import db, getzip, Building, Parcel, Owner

owners = {}
buildings = {}
parcels = {}
counts = {
	"buildings": 0,
	"parcels": 0,
	"dwelling_units": 0,
	"owners": 0,
	"owners_in_sf": 0
}
mosts = {
	"buildings": None,
	"parcels": None,
	"dwelling_units": None
}

def compMosts(ptype, owner, o):
	if not mosts[ptype] or mosts[ptype]["record"] < o[ptype]:
		if not owner:
			log("skipping %s record (%s) held by nameless owner"%(ptype, o[ptype]), 1)
		elif owner == "CITY PROPERTY":
			log("skipping %s record (%s) held by city ('CITY PROPERTY')"%(ptype, o[ptype]), 1)
		elif owner == "STATE PROPERTY":
			log("skipping %s record (%s) held by state ('STATE PROPERTY')"%(ptype, o[ptype]), 1)
		elif owner == "RECREATION AND PARK DEPARTMENT":
			log("skipping %s record (%s) held by parks and rec ('RECREATION AND PARK DEPARTMENT')"%(ptype, o[ptype]), 1)
		else:
			mosts[ptype] = {
				"name": owner,
				"address": o["address"],
				"record": o[ptype]
			}

def scan():
	csv = getcsv(os.path.join("scrapers", "data", "Buildings.csv"))
	log("Scanning Buildings.cvs (%s rows)"%(len(csv),), important=True)
	for row in csv[1:]:
		oname = row[18]
		building_id = row[0]
		parcel_id = row[1]
		dwelling_units = int(row[3])
		if oname not in owners:
			log("new owner: %s"%(oname,), 1)
			owners[oname] = {
				"buildings": set(),
				"parcels": set(),
				"dwelling_units": 0,
				"address": row[19],
				"in_sf": "SAN FRANCISCO" in row[19]
			}
			counts["owners"] += 1
			if owners[oname]["in_sf"]:
				counts["owners_in_sf"] += 1
				log("sf native!", 2)
#		owners[oname]["address"] = owners[oname]["address"] or row[19] # probably not necessary...
		if building_id not in buildings:
			addr = ("%s %s %s"%(row[7], row[9], row[10])).strip()
			zc = row[15].strip()
			log("new building: %s @ %s (%s)"%(building_id, addr, zc), 1)
			buildings[building_id] = {
				"owner": oname,
				"parcels": set(),
				"dwelling_units": 0,
				"year": int(row[4]),
				"building_type": row[2],
				"address": addr,
				"zipcode": zc
			}
		parcels[parcel_id] = {
			"building": building_id,
			"dwelling_units": dwelling_units,
			"from_addr": row[7],
			"to_addr": row[8]
		}

		owner = owners[oname]
		owner["buildings"].add(building_id)
		owner["parcels"].add(parcel_id)
		owner["dwelling_units"] += dwelling_units

		building = buildings[building_id]
		building["parcels"].add(parcel_id)
		building["dwelling_units"] += dwelling_units

		counts["dwelling_units"] += dwelling_units

def process():
	log("Processing %s Owners (%s w/ SF addresses)"%(counts["owners"],
		counts["owners_in_sf"]), important=True)
	for owner in owners:
		o = owners[owner]
		for ptype in ["buildings", "parcels"]:
			o[ptype] = len(o[ptype])
			counts[ptype] += o[ptype]
			compMosts(ptype, owner, o)
		compMosts("dwelling_units", owner, o)
	for building in buildings:
		b = buildings[building]
		b["parcels"] = len(b["parcels"])

def _zip(zc, addr):
	if not zc.isdigit() or len(zc) != 5:
		log("unsuitable zip (%s) -- deriving from address (%s)"%(zc, addr), important=True)
		if addr:
			zc = addr2zip(addr)
		else:
			return log("can't derive zip from blank address!!!", important=True)
	return zc and getzip(zc).key

def export_owners():
	i = 0
	olist = []
	oitems = owners.items()
	log("processing %s owners"%(len(oitems),), 1)
	for name, odata in oitems:
		if not name:
			log("no name for owner: %s"%(json.dumps(odata),), important=True)
		elif not Owner.query(Owner.name == name).get():
			log("Can't find owner '%s' -- creating new entry"%(name,), 2)
			owner = Owner(name=name)
			if odata["address"]:
				owner.address, zc = odata["address"].rsplit(" ", 1)
				zcode = _zip(zc, owner.address)
				if zcode:
					owner.zipcode = zcode
			else:
				log("no address for %s!"%(name,), important=True)
			olist.append(owner)
		i += 1
		if not i % 100:
			log("processed %s owners"%(i,), 2)
	log("saving %s owners"%(len(olist),), 1)
	db.put_multi(olist)

def export_buildings():
	i = 0
	blist = []
	bitems = buildings.items()
	log("processing %s buildings"%(len(bitems),), 1)
	for b_id, bdata in bitems:
		addr = bdata["address"]
		building = Building.query(Building.address == addr).get()
		owner = Owner.query(Owner.name == bdata["owner"]).get()
		byear = bdata["year"]
		btype = bdata["building_type"]
		if not building:
			log("Can't find building '%s' -- creating new entry"%(addr,), 2)
			building = Building(address=addr)
		if owner:
			building.owner = owner.key
		if byear:
			building.year = byear
		if btype:
			building.building_type = btype
		if b_id:
			building.building_id = b_id
		if not building.zipcode:
			zc = _zip(bdata["zipcode"], addr)
			if zc:
				building.zipcode = zc
		if not building.latitude or not building.longitude:
			building.latitude, building.longitude = address2latlng(building.address)
		blist.append(building)
		i += 1
		if not i % 100:
			log("processed %s buildings"%(i,), 2)
	log("saving buildings", 1)
	db.put_multi(blist)

def export_parcels():
	i = 0
	plist = []
	pitems = parcels.items()
	log("processing %s parcels"%(len(pitems),), 1)
	for p_id, pdata in pitems:
		if not Parcel.query(Parcel.parcel_id == p_id).get():
			log("Can't find parcel '%s' -- creating new entry"%(p_id,), 2)
			building = Building.query(Building.building_id == pdata["building"]).get()
			plist.append(Parcel(
				parcel_id=p_id,
				dwelling_units=pdata["dwelling_units"],
				from_addr=pdata["from_addr"],
				to_addr=pdata["to_addr"],
				building=building and building.key or None
			))
		i += 1
		if not i % 100:
			log("processed %s parcels"%(i,), 2)
	log("saving parcels", 1)
	db.put_multi(plist)

def export():
	log("Exporting Results", important=True)
	# this part is anything but conventional,
	# but justified because these functions take so long
	if raw_input("export owners? [N/y]").lower().startswith("y"):
		export_owners()
	if raw_input("export buildings? [N/y]").lower().startswith("y"):
		export_buildings()
	export_parcels()

def report():
	log("Reporting Results", important=True)
	log("reporting counts (json)", 1)
	writejson(counts, os.path.join("logs", "json", "counts"))
	log("reporting mosts (json)", 1)
	writejson(mosts, os.path.join("logs", "json", "mosts"))
	log("reporting buildings (json)", 1)
	write(buildings, os.path.join("logs", "json", "buildings.json"), True, True) # pretty only (utf-8)
	log("reporting parcels (json)", 1)
	writejson(parcels, os.path.join("logs", "json", "parcels"))
	log("reporting owners (json)", 1)
	write(owners, os.path.join("logs", "json", "owners.json"), True, True) # pretty only (utf-8 issue)

def full_scan():
	set_log(os.path.join("logs", "txt", "lords.txt"))
	scan()
	process()
	export()
	report()
	log("goodbye")
	close_log()

if __name__ == "__main__":
	full_scan()