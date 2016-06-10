import sys, os
sys.path.append("..")
from math import sqrt
from datetime import datetime
from cantools.util import read, write, writejson, error, log, set_log, close_log, getxls, getcsv_from_data
from cantools.geo import addr2zip, address2latlng
from cantools import config
from model import db, getzip, Fire, Building
from demographics import getMap, getRentControl

obj = {}
alladdrs = []
fires = []
pnum = 1
PBRK = "Losses\n\n"
len2line = {
	78: 74, # page 32
	75: 68 # page 49
}
dswap65 = {
	"units": [0, 1, 4, 6, 7, 8, 12, 14],
	"people": [2, 3, 5, 9, 10, 11, 13, 15]
}
pagereps = {
	# messed up zips
	3: [["94105\n\n94112", "94105\n\n\n\n94112"]],
	64: [['94116\n94103\n94124\n\n94117\n94124\n94121\n94103\n94112\n94110\n94116\n94127\n94115\n\n94102',
		'\n94117\n94124\n94121\n94103\n94112\n94110\n94116\n94127\n94115\n\n94102\n\n\n94116\n94103\n94124\n'],
		["14\n\n 10", "14\n\n\n 10"],
		["43\n\n 32", "43\n\n\n 32"],
		["12\n\n 35", "12\n\n 13\n\n\n 11\n 11\n 12\n\n\n 11\n\n\n 35"],
		["40\n\n 13\n\n 42", "40\n\n 42"],
		["42\n\n 1\n\n 11\n 11\n 12", "42\n"],
		["37\n\n 11\n\n 37", "37\n\n\n 37"]],
	65: [["94124\n\n94115", "94124\n\n\n94115"]],
	# messed up displacement data (p62 especially is a mess)
	7: [[" 28\n\n 32\n ", " 28\n\n\n 32\n "]],
	62: [[" 75\n\n 220\n\n 4\n\n 17\n 13\n\n 41\n 41\n\n 11\n\n 33\n\n 14\n\n 44\n\n 25\n 13\n\n 14\n 14\n 14\n 13\n\n 60\n 39\n\n 40\n 41\n 40\n 34\n\n 119\n\n 38\n\n 1\n\n 1\n\n 1\n\n 1\n\n 15\n\n 44\n\n 13\n 19\n 13\n\n 39\n 44\n 39\n\n", "\n75\n\n\n\n\n\n\n\n\n\n17\n13\n\n\n\n11\n\n\n\n14\n\n25\n13\n\n14\n14\n14\n13\n\n119\n\n\n\n\n15\n\n13\n19\n13\n\n\n\n220\n\n\n\n\n\n\n\n\n\n41\n41\n\n\n\n33\n\n\n\n44\n\n60\n39\n\n40\n41\n40\n34\n\n38\n\n\n\n\n44\n\n39\n44\n39\n\n\n"]],
	# both :)
	63: [["94112\n\n94109", "94112\n\n\n94109"],
		["94110\n\n94117", "94110\n\n\n94117"],
		["38\n 53\n\n 70\n 75\n\n 73\n 50\n\n 46\n 49\n\n 42\n 38\n\n 2\n\n 1\n\n 15\n\n 43\n\n 15\n 14\n\n 45\n 35\n\n 1\n\n 16\n\n 47\n\n 1\n\n 19\n 12\n 15\n 13\n\n 15\n 19\n 18\n\n 14\n 12\n\n 44\n 39\n 46\n 42\n\n ", "15\n\n\n15\n14\n\n\n16\n\n\n\n19\n12\n15\n13\n\n\n\n\n\n15\n19\n18\n\n14\n12\n\n38\n53\n\n70\n75\n\n73\n50\n\n46\n49\n\n42\n38\n\n43\n\n\n45\n35\n\n\n47\n\n\n\n44\n39\n46\n42\n\n\n\n\n\n"]],
	# terrible
	16: [["1\n\n 1\n\n1", "1"]],
	26: [["1\n\n 1\n\n1", "1"]],
	28: [["1\n\n 1\n\n1", "1"]],
	38: [["\n\n 1\n\n 5\n\n", "\n\n"]],
	43: [["\n\n 1\n\n 1\n\n", "\n\n"]],
	45: [["\n\n 1\n\n", "\n\n"]],
	47: [["\n\n 5\n\n 1\n\n", "\n\n"]],
	51: [["\n\n 1\n\n", "\n\n"]],
	23: [["\nB02\nB10\nB10\nB09\nB06\nB06\nB03\nB06\nB01\nB09\nB06\nB08\nB06\nB10\nB06\nB01\nB01\nB10\nB04\nB03\nB04\nB06\nB02\nB10\nB06\nB08\nB04\nB07\nB02\nB10\nB09\nB08\nB10\nB02\nB04\nB06\nB04\nB05\nB10\nB02\nB09\n\n94124\n94124\n94112\n94114\n94110\n94130\n94110\n94133\n94112\n94110\n94122\n94131\n\n94114\n94111\n94102\n94124\n94123\n94104\n94109\n94110\n94114\n94107\n\n94116\n94115\n94121\n94110\n94124\n94112\n94122\n94124\n94103\n94115\n94131\n94109\n94117\n94124\n94102\n94112\n", "\n94124\n94124\n94112\n94114\n94110\n94130\n94110\n94133\n94112\n94110\n94122\n94131\n\n94114\n94111\n94102\n94124\n94123\n94104\n94109\n94110\n94114\n94107\n\n94116\n94115\n94121\n94110\n94124\n94112\n94122\n94124\n94103\n94115\n94131\n94109\n94117\n94124\n94102\n94112\n\nB02\nB10\nB10\nB09\nB06\nB06\nB03\nB06\nB01\nB09\nB06\nB08\nB06\nB10\nB06\nB01\nB01\nB10\nB04\nB03\nB04\nB06\nB02\nB10\nB06\nB08\nB04\nB07\nB02\nB10\nB09\nB08\nB10\nB02\nB04\nB06\nB04\nB05\nB10\nB02\nB09\n"]],
	32: [['\n1267 PAGE ST\n333 MONTICELLO ST\n1568 HAIGHT ST\n\n94117\n94132\n94117\n', '\n\n1267 PAGE ST\n94117\n333 MONTICELLO ST\n94132\n1568 HAIGHT ST\n94117\n'], ["\n\n 2\n\n 2\n\n 1\n\n", "\n\n"]]
}

STEST = False
config.geo.test = STEST # happens automatically based on ct.cfg unless scraper is run independent of web server
pbase = STEST and ".." or "."
def path(*components):
	return os.path.join(pbase, *components)

data = read(path("scrapers", "data", "fires.txt"))
pages = [p.split(PBRK)[1] for p in data.split("\x0c") if PBRK in p]

def getDates(page):
	datelines, page = page.split("\n\n", 1)
	dates = []
	for dateline in datelines.split("\n"):
		if "/" in dateline:
			ds = [int(d) for d in dateline.split(" ")[-1].split("/")]
			dates.append(datetime(ds[2], ds[0], ds[1]))
	log("got %s dates"%(len(dates),), 1)
	return dates, page

def a2z(addr):
	return addr2zip("%s, san francisco, CA"%(addr,))

def getAddrs(page):
	global alladdrs
	addrs, page = page.split("\n\n", 1)
	addrs = addrs.split("\n")
	# alen cases bc format changes throughout doc
	alen = len(addrs)
	log("getAddrs() - address entries: %s"%(alen,))
	if alen == 82 or alen == 75: # p12, p32 - zips intermingled w/ addrs (32 worse)
		log("unmingling addresses/zips (total: %s)"%(len(addrs),), important=True)
		log(addrs)
		zips = addrs[1::2]
		addrs = addrs[0::2]
		log(zips)
		log(addrs)
		log("unmingled! (%s zips, %s addrs)"%(len(zips), len(addrs)), important=True)
		if alen == 75: # p32 and also p49
			if pnum == 49:
				log("slicing stray addrs from zips array")
				for i in [-1, -3, -5]:
					addrs.insert(i, zips.pop())
				endzips, page = page.split("\n\n", 1)
				log("adding final zips")
				zips += endzips.split("\n")
			else: # p32
				log("grabbing additional zips/addrs", important=True)
				page = page.split("\n")
				zips.append(a2z(addrs[-1]))
				while len(zips) < 41:
					addrs.append(page.pop(0))
					zips.append(page.pop(0))
				log(zips)
				log(addrs)
				log("zips: %s. addrs: %s"%(len(zips), len(addrs)))
				page = "\n".join(page)
	elif alen == 81: # p50 - intermingled, malformed address
		zips = ['94110'] + addrs[1:][1::2]
	elif alen == 16: # p51 -- zips before and after addresses
		a, z, page = page.split("\n\n", 2)
		zips = addrs + [a2z("44 5TH ST")] + z.split("\n")
		addrs = a.split("\n")
	elif alen == 13: # p64 - unbelievably inconsistent
		# zips are split into 3 sections
		# - above addrs
		# - below addrs
		#   - these are OUT OF ORDER! wow.
		# - intermingled w/ addrs
		zips = addrs # why would they do this?
		zips.append(a2z("4646 3RD ST"))
		zips.append(a2z("502 VIDAL DR"))
		mixed, page = page.split("\n\n", 1)
		mixed = mixed.split("\n") # contains some zips
		addrs = []
		for addr in mixed:
			if addr.startswith("941"):
				zips.append(addr)
			else:
				addrs.append(addr)
		page = page.split("\n")
		for n in range(len(zips), len(addrs)):
			zips.append(page.pop(0) or a2z(addrs[n]))
		page = "\n".join(page)
	elif alen == 9: # p65 - order reversed -- why?
		zips = addrs
		pd, page = page.split("\n***10/14/14***\n")
		zipdata, addrs = pd.rsplit("\n\n", 1)
		zips.append("") # for extra line break
		zips += zipdata.split("\n")
		addrs = addrs.split("\n")
		for n in range(len(addrs)):
			if n == len(zips):
				zips.append(a2z(addrs[n]))
			elif not zips[n]:
				zips[n] = a2z(addrs[n])
	elif alen > 41: # some intermingled, others after
		n = len2line[alen]
		zips = addrs[:n][1::2]
		zips.append(a2z(addrs[n]))
		remzips, page = page.split("\n\n", 1)
		zips += remzips.split("\n")
	else: # zips after addrs, lots missing
#		if pnum == 23: # puts battalion #s before zips (????)
#			page = "\n" + page.split("\n\n", 1)[1]
		page = page.split("\n")
		zips = []
		for addr in addrs:
			zips.append(page.pop(0) or a2z(addr))
		page = "\n".join(page)
	log("got %s zips"%(len(zips),), 1)
	for zc in zips: # basic validation
		if len(zc) != 5:
			(STEST and log or error)("bad zipcode - '%s'"%(zc,))
	alladdrs += addrs
	log("added %s addresses to %s-entry-long addrs array"%(len(addrs), len(alladdrs)), 1)
	return zips, addrs, page

def linelist2numlist(linelist, count):
	print linelist
	arr = [int(n or 0) for n in "\n\n".join(linelist).split("\n")]
	while len(arr) < count:
		arr.append(0)
	return arr

def getDisplaced(page, count):
	units = []
	people = []
	if pnum == 65:
		lines = page.split("\n\n")
		for n in range(14):
			if n in dswap65["units"]:
				units.append(lines.pop(0))
			else:
				people.append(lines.pop(0))
		units.append("\n%s"%(lines.pop(0),))
		people.append("\n%s"%(lines.pop(0),))
		return linelist2numlist(units, count), linelist2numlist(people, count), "\n\n".join(lines)
	else:
		lines = page.split("\n")
		for n in range(count):
			units.append(int(lines.pop(0) or 0))
		lines.pop(0) # line break
		for n in range(count):
			people.append(int(lines.pop(0) or 0))
		return units, people, "\n".join(lines)

def fixPage(page):
	if pnum in pagereps: # uncollapse multiple rows
		for reps in pagereps[pnum]:
			page = page.replace(reps[0], reps[1])
	return page

def getBattsAlarms(page):
	page = page.split("\n\n")
	batts = [b for b in page.pop(0).split("\n") if b]
	alarms = page.pop(pnum > 63 and -4 or 0) # ridiculous
	return batts, [int(a) for a in alarms.split("\n")], "\n\n".join(page)

def scanPage(page):
	page = fixPage(page)
	dates, page = getDates(page)
	years = [d.year for d in dates]
	# throw away times
	times, page = page.split("\n\n", 1)
	zips, addrs, page = getAddrs(page)
	batts, alarms, page = getBattsAlarms(page)
	units, people, page = getDisplaced(page, len(zips))
	if pnum == 13: # wow...
		alarms = units
		units = people
		people = [int(l) for l in page.split("\n\n")[0].split("\n")[1:]]
	# TODO: correlate more stuff
	# - injuries/deaths

	log("zips %s addrs %s dates %s batts %s alarms %s units %s people %s"%(len(zips),
		len(addrs), len(dates), len(batts), len(alarms), len(units), len(people)))
	if STEST:
		return {
			"zips": zips,
			"addrs": addrs,
			"dates": dates,
			"batts": batts,
			"alarms": alarms,
			"units": units,
			"people": people
		}

	for n in range(len(zips)):
		if years[n] not in obj:
			obj[years[n]] = {"total": {
				"fires": 0,
				"units": 0,
				"people": 0
			}}
		if zips[n] not in obj[years[n]]:
			obj[years[n]][zips[n]] = {
				"fires": 0,
				"units": 0,
				"people": 0
			}
		obj[years[n]]["total"]["fires"] += 1
		obj[years[n]]["total"]["units"] += units[n]
		obj[years[n]]["total"]["people"] += people[n]
		obj[years[n]][zips[n]]["fires"] += 1
		obj[years[n]][zips[n]]["units"] += units[n]
		obj[years[n]][zips[n]]["people"] += people[n]

		# TODO: injuries, fatalities, losses
		building = Building.query(Building.address == addrs[n]).get()
		if not building:
			log("no building (%s) -- creating new one!"%(addrs[n],), important=True)
			building = Building(address=addrs[n], zipcode=getzip(zips[n] or addr2zip(addrs[n])).key)
			building.latitude, building.longitude = address2latlng(addrs[n])
			building.put()
		fires.append(Fire(
			building=building.key,
			date=dates[n],
			battalion=batts[n],
			alarms=alarms[n],
			units=units[n],
			persons=people[n]
		))

def scan():
	global pnum
	for page in pages:
		log("page %s"%(pnum,), important=True)
		scanPage(page)
		pnum += 1

def allUnits():
	csv = getcsv_from_data(read(path("scrapers", "data", "BlockLot_with_LatLon.csv")))
	buildings = {}
	winner = None
	for row in csv:
		addr = "%s %s %s"%(row[22], row[20], row[19])
		if not addr.strip():
			continue
		if addr not in buildings:
			buildings[addr] = 0
		buildings[addr] += 1
		if not winner or buildings[addr] > buildings[winner]:
			winner = addr
	return buildings, winner, len(csv)

def summary():
	log(obj.keys())
	for year in range(2005, 2016):
		log(year)
		for key in ["total", "94110", "94124"]:
			log("%s: %s"%(key, obj[year][key]), 1)

	rc = getRentControl()
	tf = len(alladdrs)
	rcf = len([a for a in alladdrs if a in rc])

	# count total units, buildings
	log("Building Breakdown", important=True)
	prop_obj, top_building, total_rows = allUnits()
	buildings = len(prop_obj.keys())
	units = sum(prop_obj.values())
	rc_total = getMap()["SF"]["rent_control"]
	log("using %s of %s rows (omitting blank entries)"%(units, total_rows), 1)
	log("found %s units in %s buildings"%(units, buildings), 1)
	log("building at %s has %s units"%(top_building, prop_obj[top_building]), 1)

	log("Rent Control Breakdown", important=True)
	log("%s of %s total buildings (%s%%) are rent-controlled"%(rc_total,
		buildings, str(100 * float(rc_total) / buildings)), 1)
	log("%s of %s total fires (%s%%) were at rent-controlled buildings"%(rcf,
		tf, str(100 * float(rcf) / tf)), 1)

def getPage(n):
	global pnum
	pnum = n
	return fixPage(pages[n - 1])

def fullScan():
	log("Performing Full Scan", important=True)
	scan()
	summary()
	writejson(obj, path("logs", "json", "zips_by_year"))

ARR_ANYL = [ # tuple array so we can order them (so we can calc average first)
	("average", lambda x, y : sum(x) / len(x)),
	("max_disparity", lambda x, y : max(x) - min(x)),
	("standard_deviation", lambda x, ave : sqrt(sum([(i - ave)**2 for i in x]) / len(x)))
]

def propertyValues():
	log("Analyzing Property Values", important=True)
	for year in range(2008, 2014):
		yobj = obj[year]
		tobj = yobj["total"]
		tobj["property_values"] = { "all": [] }
		log("parsing: %s"%(year,), 1)
		xls = getxls(read(path("scrapers", "data", "pvals",
			"SanFranciscoPropertyAssessmentRoll%s.xlsx"%(year,))), "%sSecured"%(year,), parse=False)
		for r in range(1, xls.nrows):
			row = xls.row(r)
			pval = row[7].value
			zipcode = row[8].value[:5]
			if zipcode not in yobj:
				yobj[zipcode] = { "fires": 0, "people": 0, "units": 0 }
			zobj = yobj[zipcode]
			if "property_values" not in zobj:
				zobj["property_values"] = { "all": [] }
			zobj["property_values"]["all"].append(pval)
			tobj["property_values"]["all"].append(pval)
		for zcode, zobj in yobj.items():
			if "property_values" in zobj:
				apv = zobj["property_values"]["all"]
				ave = None
				log("analyzing: %s"%(zcode,), 2)
				for conversion, func in ARR_ANYL:
					zobj["property_values"][conversion] = func(apv, ave)
					ave = ave or zobj["property_values"][conversion] # average happens first
					log("%s: %s"%(conversion, zobj["property_values"][conversion]), 3)
				del zobj["property_values"]["all"]
			else:
				log("%s: missing!"%(zcode,), 2)

def pvalcsv(obj):
	props = ["year", "fires", "people", "units"]
	pvprops = [t[0] for t in ARR_ANYL]
	allprops = props + ["property_value_%s"%(pname,) for pname in pvprops]
	years = {}

	# straight up values
	csv = [",".join(allprops)]
	for year in range(2008, 2014):
		syr = str(year)
		years[syr] = [obj[syr][p] for p in props[1:]] + [obj[syr]["property_values"][pname] for pname in pvprops]
		csv.append(",".join([str(i) for i in [year] + years[syr]]))

	# normalized values
	base = years["2008"]
	csv.append(",".join(allprops))
	csv.append(",".join(["2008"] + [n and "1" or "0" for n in base]))
	for year in range(2009, 2014):
		vrow = []
		syr = str(year)
		yrow = years[syr]
		for i in range(len(base)):
			if not base[i]:
				base[i] = yrow[i]
			vrow.append(base[i] and str(float(yrow[i]) / base[i]) or "0")
		csv.append(",".join([syr] + vrow))

	return "\n".join(csv)

def pvalsByYear(zmap):
	log("writing pval csvs")
	for zcode, zdata in zmap.items():
		if "property_values" in zdata["2008"]:
			log("writing %s.csv"%(zcode,), 1)
			write(pvalcsv(zdata), path("logs", "csv", "%s.csv"%(zcode,)))
		else:
			log("skipping %s"%(zcode,), 1)

def mergeDemographics():
	log("Merging Demographics", important=True)
	propertyValues()
	zmap = getMap()
	ztotal = zmap["SF"]["total"]
	log("adding fire data to demographics map")
	for year, year_data in obj.items():
		syear = str(year) # de-unicode
		for zcode, zip_data in year_data.items():
			if zcode == "total":
				for tcount in ztotal.keys():
					ztotal[tcount] += zip_data[tcount]
			elif zcode not in zmap:
				log("zipcode not found in demographics map: %s"%(zcode,), 1)
			else: # zipcode
				zmap[zcode][syear] = {} # de-unicode
				for zk, zv in zip_data.items():
					zmap[zcode][syear][str(zk)] = zv
				if not syear in zmap["SF"]:
					zmap["SF"][syear] = { "fires": 0, "people": 0, "units": 0 }
					if "property_values" in obj[year]["total"]:
						zmap["SF"][syear]["property_values"] = obj[year]["total"]["property_values"]
				for tcount in ztotal.keys():
					zmap[zcode]["total"][tcount] += zip_data[tcount]
					zmap["SF"][syear][tcount] += zip_data[tcount]
	log("calculating # fires, # peeps displaced, # units destroyed per 1000 people by neighborhood")
	for area, data in zmap.items():
		if "ad_hoc" in data: continue
		zav = data["per_1000"] = {}
		for key in ztotal.keys():
			zav[key] = 1000.0 * data["total"][key] / data["population"]
	log("writing demographics.json")
	writejson(zmap, path("logs", "json", "demographics"))
	pvalsByYear(zmap)

def export():
	log("Exporting Results", important=True)
	log("saving %s fires"%(len(fires),), 1)
	db.put_multi(fires)

def full_scan():
	set_log(path("logs", "txt", "fires.txt"))
	fullScan()
	mergeDemographics()
	export()
	log("goodbye")
	close_log()

if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser("python fires.py [-f]")
	parser.add_option("-f", "--full_scan", action="store_true", dest="full_scan", default=False,
		help="perform full scan of fire data (only necessary if that part of the code changes)")
	options, arguments = parser.parse_args()

	set_log(path("logs", "txt", "fires.txt"))

	if options.full_scan:
		fullScan()
	else:
		obj = read(path("logs", "json", "zips_by_year.json"), True)

	mergeDemographics()

	close_log()