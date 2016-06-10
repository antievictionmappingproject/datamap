from cantools.db import *
from cantools.geo import addr2zip, address2latlng, savecache
from cantools.util import log
from model import *

def _zips(addrs):
    i = 0
    puts = []
    for b in addrs:
        z = addr2zip("%s, san francisco, CA"%(b.address,))
        if z and z.startswith("9"):
            b.zipcode = getzip(z).key
            puts.append(b)
            i += 1
            if not i % 100:
                log("processed %s"%(i,), important=True)
        else:
            log('no results -- (zip: %s) skipping %s!!'%(z, b.address), important=True)
    plen = len(puts)
    log("found %s zips (skipped %s). saving..."%(plen, len(addrs) - plen), important=True)
    return puts

def zips():
    bs = Building.query(Building.zipcode == None)
    log("found %s zipcodeless buildings"%(bs.count(),))
    put_multi(_process(bs.all()))
    log("done!")

def _ll(addrs):
    i = 0
    for b in addrs:
        b.latitude, b.longitude = address2latlng("%s, san francisco, CA"%(b.address,))
        i += 1
        if not i % 100:
            log("processed %s"%(i,), important=True)
    log("saving %s building records..."%(len(addrs),), important=True)
    return addrs

def ll():
    bs = Building.query(Building.latitude == None)
    log("found %s lat/lng -less buildings"%(bs.count(),))
    put_multi(_ll(bs.all()))
    log("writing prettified geocache")
    savecache(True)
    log("done!")

if __name__ == "__main__":
#    zips()
    ll()