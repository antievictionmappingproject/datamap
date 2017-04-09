import os
from cantools.util import log, set_log, close_log, read, getxls
from model import db, data2building, Building, Eviction

def omi_row(row):
	eviction = Eviction()
	eviction.reason = "omi"
	eviction.petition = row[0]
	eviction.date = row[1]
	eviction.building = data2building({
		"address": row[2],
		"building_id": row[7],
		"zipcode": row[6],
		"latitude": row[8],
		"longitude": row[9]
	}).key
	return eviction

def ellis_row(row):
	eviction = Eviction()
	eviction.reason = "ellis"
	eviction.petition = row[1]
	eviction.date = row[0]
	eviction.building = data2building({
		"address": row[9],
		"building_id": row[6],
		"year": row[12],
		"latitude": row[11],
		"longitude": row[10]
	}).key
	return eviction

def demo_row(row):
	eviction = Eviction()
	eviction.reason = "demolition"
	eviction.petition = row[0]
	eviction.date = row[1]
	eviction.building = data2building({
		"address": row[3],
		"building_id": row[10],
		"zipcode": row[8],
		"latitude": row[13],
		"longitude": row[12]
	}).key
	return eviction

SCANROW = {
	"omi": omi_row,
	"ellis": ellis_row,
	"demolition": demo_row
}

def scan(etype):
	fname = "%s_1997_2015.xlsx"%(etype,)
	log("Scanning %s"%(fname,), important=True)
	xls = getxls(read(os.path.join("scrapers", "data", fname)))
	puts = []
	for row in xls[1:]:
		puts.append(SCANROW[etype](row))
	return puts

def full_scan():
	set_log(os.path.join("logs", "txt", "evictions.txt"))
	log("Scraping Evictions", important=True)
	omi = scan("omi")
	ellis = scan("ellis")
	demos = scan("demolition")
	log("saving evictions: %s omi, %s ellis, %s demolitions"%(len(omi), len(ellis), len(demos)), 1)
	db.put_multi(omi + ellis + demos)
	log("goodbye")
	close_log()