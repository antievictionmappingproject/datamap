from cantools import db

class Building(db.ModelBase):
    latitude = db.Float()
    longitude = db.Float()
    year = db.Integer()
    building_id = db.String()
    building_type = db.String()
    address = db.String()
    zipcode = db.ForeignKey(kind="zipcode")
    owner = db.ForeignKey(kind="owner")
    rent_control = db.Boolean()
    label = "address"
    # collections: parcels, values

def data2building(data):
    from cantools.geo import address2latlng, addr2zip
    changes = False
    b = None
    if data.get("address"):
        data["address"] = data["address"].strip().upper()
    if data.get("building_id"):
        b = Building.query(Building.building_id == data["building_id"]).get()
    if not b and data.get("address"):
        b = Building.query(Building.address == data["address"]).get()
    if not b:
        changes = True
        if data.get("zipcode"):
            data["zipcode"] = getzip(data["zipcode"]).key
        if data.get("year"):
            data["year"] = int(data["year"])
        data["latitude"] = data["latitude"] and float(data["latitude"])
        data["longitude"] = data["longitude"] and float(data["longitude"])
        b = Building(**data)
    addr = "%s, san francisco, CA"%(b.address,)
    if not b.zipcode:
        changes = True
        b.zipcode = getzip(addr2zip(addr)).key
    if not b.latitude:
        changes = True
        b.latitude, b.longitude = address2latlng(addr)
    if changes:
        b.put()
    return b

class Parcel(db.ModelBase):
    building = db.ForeignKey(kind="building")
    parcel_id = db.String()
    dwelling_units = db.Integer()
    from_addr = db.String()
    to_addr = db.String()
    label = "parcel_id"

class Eviction(db.ModelBase):
    building = db.ForeignKey(kind="building")
    petition = db.String()
    date = db.DateTime()
    reason = db.String() # omi|ellis
    label = "petition"

class PropertyValue(db.ModelBase):
    building = db.ForeignKey(kind="building")
    year = db.Integer()
    value = db.Integer()
    label = "year"

class Owner(db.ModelBase):
    name = db.String()
    address = db.String()
    zipcode = db.ForeignKey(kind="zipcode")
    owner = db.ForeignKey(kind="owner") # to map front trees...
    # collections: buildings, owners

class Fire(db.ModelBase):
    date = db.DateTime()
    building = db.ForeignKey(kind="building")
    battalion = db.String()
    alarms = db.Integer()
    units = db.Integer()
    persons = db.Integer()
    injuries = db.Integer()
    fatalities = db.Integer()
    losses = db.Integer()
    label = "date"

class PoliceShooting(db.ModelBase):
    date = db.DateTime()
    victim = db.String()
    age = db.Integer()
    race = db.String()
    photo = db.Binary()
    latitude = db.Float()
    longitude = db.Float()
    blurb = db.Text()
    label = "victim"

class ZipCode(db.ModelBase):
    code = db.String()
    city = db.String()
    state = db.String()
    county = db.String()
    label = "code"
    # collections: buildings, owners

    def __str__(self):
        return self.code

    def fullString(self):
        return "%s, %s, %s"%(self.city, self.state, self.code)

ZIPDOMAIN = "z.mariobalibrera.com"

def getzip(code):
    if len(code) < 5:
        from cantools.util import error
        error("invalid zip code: %s"%(code,))
    try:
        code = str(int(code.strip()[:5]))
        while len(code) < 5: # preceding 0's
            code = '0'+code
    except:
        from cantools.util import error
        error("invalid zip code: %s"%(code,))
    zipcode = ZipCode.query().filter(ZipCode.code == code).get()
    if not zipcode:
        from cantools.web import fetch
        city, state, county = fetch(ZIPDOMAIN, path="/%s"%(code,), asjson=True)
        zipcode = ZipCode(code=code, city=city, state=state, county=county)
        zipcode.put()
    return zipcode

def getzips(kwargs):
    zips = ZipCode.query()
    for key, val in kwargs.items():
        zips = zips.filter(db.GenericProperty(key) == val)
    return zips.fetch(1000)